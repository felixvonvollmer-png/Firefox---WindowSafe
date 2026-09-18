"""Synthetic harness regression tests, never Firefox or session tests."""

import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import foundation as f


class ReviewContractTests(unittest.TestCase):
    def setUp(self):
        self.contract = f.parse((f.ROOT / f.CONTRACT_PATH).read_bytes())
        self.request = {
            "review_type": "PROJECT_FOUNDATION_REVIEW",
            "subject": {"id": "SYNTHETIC", "path": "foundation/subject.json", "end_sha": "a" * 40},
            "implementer": "synthetic-implementer",
            "required_authority": "INDEPENDENT_PROJECT_LLM",
            "reviewed_evidence": [{"path": "foundation/evidence/synthetic.md", "sha256": "b" * 64}],
        }
        self.result = {
            "schema_version": self.contract["contract_version"], "review_id": "SYNTHETIC-R1",
            "review_type": self.request["review_type"],
            "reviewer": {"authority": "INDEPENDENT_PROJECT_LLM", "identity": "synthetic-reviewer", "run_reference": "synthetic-run", "independence": "FRESH_OR_SUFFICIENTLY_ISOLATED"},
            "provenance": {"source_reference": "SYNTHETIC_TEST_ONLY_NOT_A_REAL_REVIEW", "transport": "EXACT_AUTHORIZED_TRANSFER"},
            "subject": copy.deepcopy(self.request["subject"]),
            "verdict": "PASS", "findings": [],
            "reviewed_evidence": copy.deepcopy(self.request["reviewed_evidence"]),
            "result_reference": "reviews/results/SYNTHETIC-R1.json",
        }

    def validate(self, result=None):
        f.validate_result(result or self.result, self.request, self.contract, "SYNTHETIC-R1.json")

    def test_valid_verdicts(self):
        for verdict in self.contract["verdicts"]:
            with self.subTest(verdict=verdict):
                self.result["verdict"] = verdict
                self.validate()

    def test_each_semantic_field_required(self):
        for key in f.RESULT_FIELDS:
            with self.subTest(field=key):
                result = copy.deepcopy(self.result)
                del result[key]
                with self.assertRaises(f.Invalid):
                    self.validate(result)

    def test_unknown_fields_rejected(self):
        self.result["hidden_approval"] = True
        with self.assertRaises(f.Invalid):
            self.validate()

    def test_boolean_version_rejected(self):
        self.result["schema_version"] = True
        with self.assertRaises(f.Invalid):
            self.validate()

    def test_subject_and_evidence_binding(self):
        for mutation in ("sha", "subject", "evidence", "duplicate", "missing"):
            with self.subTest(mutation=mutation):
                result = copy.deepcopy(self.result)
                if mutation == "sha":
                    result["subject"]["end_sha"] = "c" * 40
                elif mutation == "subject":
                    result["subject"]["id"] = "WRONG"
                elif mutation == "evidence":
                    result["reviewed_evidence"][0]["sha256"] = "d" * 64
                elif mutation == "duplicate":
                    result["reviewed_evidence"] *= 2
                else:
                    result["reviewed_evidence"] = []
                with self.assertRaises(f.Invalid):
                    self.validate(result)

    def test_authority_independence_and_provenance(self):
        for field, value in [("authority", "CODING_AGENT"), ("identity", "synthetic-implementer"), ("run_reference", ""), ("independence", "SAME_CONTEXT")]:
            with self.subTest(field=field):
                result = copy.deepcopy(self.result)
                result["reviewer"][field] = value
                with self.assertRaises(f.Invalid):
                    self.validate(result)
        self.result["provenance"]["source_reference"] = ""
        with self.assertRaises(f.Invalid):
            self.validate()

    def test_result_id_filename_locator(self):
        for field in ("review_id", "result_reference"):
            result = copy.deepcopy(self.result)
            result[field] = "WRONG"
            with self.assertRaises(f.Invalid):
                self.validate(result)

    def test_pass_rejects_open_blockers(self):
        for severity in ("CRITICAL", "BLOCKING", "MAJOR"):
            self.result["findings"] = [{"id": "F1", "severity": severity, "status": "OPEN", "description": "synthetic finding", "disposition": "tracked but still blocking"}]
            with self.assertRaises(f.Invalid):
                self.validate()
            self.result["findings"][0]["status"] = "RESOLVED"
            self.validate()

    def test_minor_requires_disposition(self):
        self.result["findings"] = [{"id": "F1", "severity": "MINOR", "status": "OPEN", "description": "synthetic", "disposition": ""}]
        with self.assertRaises(f.Invalid):
            self.validate()
        self.result["findings"][0]["disposition"] = "EXPLICIT_NONBLOCKING_FOLLOW_UP: nonblocking follow-up with next-review trigger"
        self.validate()

    def test_duplicate_findings_rejected(self):
        self.result["findings"] = [{"id": "F1", "severity": "MINOR", "status": "RESOLVED", "description": "synthetic", "disposition": "fixed"}] * 2
        with self.assertRaises(f.Invalid):
            self.validate()

    def test_schema_preflight_full_contract(self):
        f.schema_preflight(self.contract, copy.deepcopy(self.contract))
        for key in self.contract:
            changed = copy.deepcopy(self.contract)
            del changed[key]
            with self.assertRaises(f.Invalid):
                f.schema_preflight(self.contract, changed)
        changed = copy.deepcopy(self.contract)
        changed["required_fields"].remove("reviewed_evidence")
        with self.assertRaises(f.Invalid):
            f.schema_preflight(changed, changed)

    def test_all_review_types(self):
        for kind, authority in f.AUTHORITIES.items():
            self.request["review_type"] = self.result["review_type"] = kind
            self.request["required_authority"] = self.result["reviewer"]["authority"] = authority
            self.validate()

    def test_history_cardinality(self):
        history = {}
        for i in range(9):
            result = copy.deepcopy(self.result)
            result["review_id"] = "SYNTHETIC-" + str(i)
            filename = result["review_id"] + ".json"
            result["result_reference"] = "reviews/results/" + filename
            f.validate_result(result, self.request, self.contract, filename)
            new = dict(history)
            new[result["result_reference"]] = json.dumps(result).encode()
            f.check_history_maps(history, new)
            history = new

    def test_history_modification_and_deletion_rejected(self):
        before = {"reviews/results/OLD.json": b"original", "foundation/inputs/source.md": b"source"}
        for path in before:
            modified = dict(before)
            modified[path] = b"changed"
            with self.assertRaises(f.Invalid):
                f.check_history_maps(before, modified)
            del modified[path]
            with self.assertRaises(f.Invalid):
                f.check_history_maps(before, modified)


class FoundationGuardsTests(unittest.TestCase):
    def test_json_duplicate_and_nonfinite_rejected(self):
        for value in ('{"x": 1, "x": 2}', '{"x": NaN}', '{"x": Infinity}'):
            with self.assertRaises(f.Invalid):
                f.parse(value)

    def test_unsafe_paths(self):
        for path in ("../outside", "/tmp/file", "a/../b", "a\\b", "a:b", "./a"):
            with self.assertRaises(f.Invalid):
                f.safe_path(path)

    def test_product_files_rejected(self):
        for path in ("src/capture.ts", "extension/manifest.json", "manifest.json", "profile/cookies.sqlite", ".env"):
            with self.assertRaises(f.Invalid):
                f.scope(path)

    def test_original_inputs_and_blobs(self):
        f.input_integrity(f.ROOT)

    def test_tampered_input_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            shutil.copytree(f.ROOT / "foundation", root / "foundation")
            target = root / "foundation/inputs/README.md"
            target.write_bytes(target.read_bytes() + b"tamper")
            with self.assertRaises(f.Invalid):
                f.input_integrity(root)

    def test_symlink_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "link").symlink_to("missing-target")
            with self.assertRaises(f.Invalid):
                list(f.files(root))

    def test_build_is_deterministic_and_content_sensitive(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "README.md").write_text("synthetic\n")
            original = f.build_bytes(root)
            self.assertEqual(original, f.build_bytes(root))
            (root / "README.md").write_text("changed\n")
            self.assertNotEqual(original, f.build_bytes(root))

    def test_lifecycle_and_ci_gate_drift_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for path in f.files(f.ROOT):
                target = root / path.relative_to(f.ROOT)
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(path.read_bytes())
            f.check(root)
            subject_path = root / "foundation/subject.json"
            original = subject_path.read_bytes()
            for field, value in [("product_features_started", True), ("platform_qualification", "PASS"), ("performance_method_binding", "PASS"), ("independent_review_status", "PASS"), ("runtime_evidence", "PASS")]:
                subject = f.parse(original)
                subject[field] = value
                subject_path.write_text(json.dumps(subject) + "\n")
                with self.subTest(field=field), self.assertRaises(f.Invalid):
                    f.check(root)
            subject_path.write_bytes(original)
            workflow = root / ".github/workflows/foundation.yml"
            original_workflow = workflow.read_text()
            workflow.write_text(original_workflow.replace("  contents: read", "  contents: read\n  issues: write"))
            with self.assertRaises(f.Invalid):
                f.check(root)
            workflow.write_text(original_workflow.replace("foundation.py check", "foundation.py request"))
            with self.assertRaises(f.Invalid):
                f.check(root)

    def test_git_bound_request_ignores_worktree_tampering(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "reviews").mkdir()
            (root / "foundation/evidence").mkdir(parents=True)
            shutil.copyfile(f.ROOT / f.CONTRACT_PATH, root / f.CONTRACT_PATH)
            subject = {"subject_id": "SYNTHETIC", "review_type": "PROJECT_FOUNDATION_REVIEW", "implementer": "synthetic-implementer", "evidence_paths": ["foundation/evidence/synthetic.md"]}
            (root / "foundation/subject.json").write_text(json.dumps(subject))
            evidence = root / "foundation/evidence/synthetic.md"
            evidence.write_text("original synthetic evidence\n")
            def run(*args):
                return subprocess.check_output(["git", "-C", str(root), *args], stderr=subprocess.PIPE)
            run("init", "--initial-branch=main")
            run("add", "foundation", "reviews")
            run("-c", "user.name=Synthetic Fixture", "-c", "user.email=fixture@example.invalid", "-c", "commit.gpgsign=false", "commit", "-m", "synthetic fixture")
            with patch.object(f, "ROOT", root):
                first = f.request("HEAD")
                f.history("0" * 40)
                result = {
                    "schema_version": first["schema_version"], "review_id": "SYNTHETIC-INTEGRATION",
                    "review_type": first["review_type"], "subject": first["subject"],
                    "reviewer": {"authority": first["required_authority"], "identity": "synthetic-independent", "run_reference": "synthetic-run", "independence": "FRESH_OR_SUFFICIENTLY_ISOLATED"},
                    "provenance": {"source_reference": "SYNTHETIC_ONLY", "transport": "EXACT_AUTHORIZED_TRANSFER"},
                    "verdict": "PASS", "findings": [], "reviewed_evidence": first["reviewed_evidence"],
                    "result_reference": "reviews/results/SYNTHETIC-INTEGRATION.json",
                }
                result_path = root / "SYNTHETIC-INTEGRATION.json"
                result_path.write_text(json.dumps(result))
                f.validate_result_file(result_path)
                evidence.write_text("uncommitted tampering\n")
                self.assertEqual(first, f.request("HEAD"))
                run("add", "foundation/evidence/synthetic.md")
                run("-c", "user.name=Synthetic Fixture", "-c", "user.email=fixture@example.invalid", "-c", "commit.gpgsign=false", "commit", "-m", "new synthetic evidence")
                second = f.request("HEAD")
                self.assertNotEqual(first["subject"]["end_sha"], second["subject"]["end_sha"])
                self.assertNotEqual(first["reviewed_evidence"], second["reviewed_evidence"])
                f.validate_result_file(result_path)  # Old SHA/evidence remains legitimate history.
                result["subject"] = second["subject"]  # New SHA with old evidence must fail.
                result_path.write_text(json.dumps(result))
                with self.assertRaises(f.Invalid):
                    f.validate_result_file(result_path)
                with self.assertRaises(f.Invalid):
                    f.history("0" * 40)


if __name__ == "__main__":
    unittest.main()
