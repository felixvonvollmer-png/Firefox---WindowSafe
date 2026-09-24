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


class EpicPreparationTests(unittest.TestCase):
    """Generic preparation bindings; disposable local Git, no browser/reviewer."""

    BASELINE = "dc9c1c37a264cc80f79ec08bf166ec42cdd73b95"
    REVIEWED = "644b81f63dcc1990bc894a9c2c9bd8dc24a98c04"
    SUBJECT = "epics/WS-E01/subject.json"

    def setUp(self):
        # Keep the pending-state regressions on the immutable pre-acceptance fixture.
        paths = f.git("ls-tree", "-r", "--name-only", self.REVIEWED, "--", "epics/WS-E01").decode().splitlines()
        self.data = {p: f.at(self.REVIEWED, p) for p in paths}

    def read(self, name):
        return self.data[name] if name in self.data else f.at(self.BASELINE, name)

    def update(self, path, **values):
        record = f.parse(self.data[path])
        record.update(values)
        self.data[path] = (json.dumps(record) + "\n").encode()

    def validate(self):
        return f.epic_preparation(self.SUBJECT, self.read, f.commit("HEAD"))

    def test_materialized_preparation_is_bound_and_pending(self):
        baseline, reviewed, reference = self.validate()
        self.assertEqual(self.BASELINE, baseline)
        self.assertEqual("fc3ee73c9bf1fab3878c480a0299fda4119e363b", reviewed)
        self.assertEqual("reviews/results/WS-PFR-20260918-02.json", reference)

    def test_other_valid_epic_id_uses_same_validator_with_own_authorization(self):
        # Synthetic input only: no real authorization or verdict is created.
        self.data = {p.replace("WS-E01", "SYNTHETIC_E02"): raw.replace(b"WS-E01", b"SYNTHETIC_E02")
                     for p, raw in self.data.items()}
        path = "epics/SYNTHETIC_E02/evidence/preparation-authorization.json"
        anchors = {path: f.sha256(self.data[path])}
        with patch.object(f, "PREPARATION_AUTHORIZATIONS", anchors):
            f.epic_preparation("epics/SYNTHETIC_E02/subject.json", self.read, f.commit("HEAD"))

    def test_scope_preparation_only_and_safe_ids(self):
        for epic in ("WS-E01", "SYNTHETIC_E02", "another-epic"):
            for name in ("subject.json", "binding.json", "preparation.md", "evidence/research.md", "evidence/auth.json"):
                f.scope("epics/" + epic + "/" + name)
        for path in ("epics/../subject.json", "epics/bad id/subject.json", "epics/E/src.ts",
                     "epics/E/evidence/nested/auth.json", "epics/E/evidence/manifest.json",
                     "epics/E/manifest.json", "features/F/subject.json", "src/background.ts"):
            with self.subTest(path=path), self.assertRaises(f.Invalid):
                f.scope(path)

    def test_subject_lifecycle_and_claims_fail_closed(self):
        original = self.data[self.SUBJECT]
        for key, value in (
            ("subject_id", "OTHER"), ("review_type", "FEATURE_ACCEPTANCE_REVIEW"),
            ("status", "READY_FOR_AGENT"), ("implementer", ""),
            ("ready_for_agent", True), ("ready_for_agent", 0),
            ("product_features_started", True), ("browser_profile_tests_executed", True),
            ("epic_preparation_critical_self_review_status", "PENDING"),
            ("epic_research_reuse_or_delta_status", "UNKNOWN"),
            ("open_material_user_decisions_required_before_start", ["open"]),
            ("external_project_context_sync", "ASSUMED"),
            ("current_canonical_baseline_or_main_sha", "HEAD"),
            ("current_canonical_baseline_or_main_sha", "4ba2c473fe4d90c85d94ee2b2f5cc5777d115109"),
        ):
            with self.subTest(field=key, value=value):
                self.data[self.SUBJECT] = original
                self.update(self.SUBJECT, **{key: value})
                with self.assertRaises(f.Invalid):
                    self.validate()

    def test_evidence_missing_unsafe_duplicate_and_incomplete(self):
        original = self.data[self.SUBJECT]
        evidence = f.parse(original)["evidence_paths"]
        for changed in ([], evidence * 2, evidence[1:], evidence + ["../outside"],
                        evidence + ["epics/WS-E01/evidence/missing.md"]):
            with self.subTest(evidence=changed):
                self.data[self.SUBJECT] = original
                self.update(self.SUBJECT, evidence_paths=changed)
                with self.assertRaises((f.Invalid, subprocess.CalledProcessError)):
                    self.validate()

    def test_binding_cannot_invent_acceptance_or_diverge(self):
        path = "epics/WS-E01/binding.json"
        original = self.data[path]
        for key, value in (
            ("status", "READY_FOR_AGENT"), ("ready_for_agent", True),
            ("epic_preparation_review_result_reference", "reviews/results/FAKE.json"),
            ("epic_id", "OTHER"), ("epic_preparation_subject_id", "OTHER"),
            ("epic_preparation_id", "OTHER"),
            ("current_canonical_baseline_or_main_sha", "0" * 40),
            ("project_foundation_review_result_reference", "reviews/results/OTHER.json"),
            ("open_critical_blocking_major_findings", "NONE"),
            ("open_material_user_decisions_required_before_start", "PENDING"),
            ("execution_authorization_reference", "foundation/evidence/followup-authorization.json"),
            ("approved_product_definition_reference", "README.md"),
            ("project_technical_foundation_reference", "README.md"),
        ):
            with self.subTest(field=key):
                self.data[path] = original
                self.update(path, **{key: value})
                with self.assertRaises(f.Invalid):
                    self.validate()

    def test_authorization_cannot_be_rewritten_to_select_a_baseline(self):
        auth = "epics/WS-E01/evidence/preparation-authorization.json"
        self.update(auth, BASELINE_MAIN_SHA=f.commit("HEAD"), AUTHORITY="CODING_AGENT")
        with self.assertRaisesRegex(f.Invalid, "authorization hash"):
            self.validate()

    def test_foundation_pass_must_be_exactly_present_in_bound_main(self):
        ref = "reviews/results/WS-PFR-20260918-02.json"
        self.data[ref] = self.read(ref) + b"\n"
        with self.assertRaisesRegex(f.Invalid, "bound main"):
            self.validate()

    def test_blocked_foundation_result_cannot_enable_preparation(self):
        ref = "reviews/results/WS-PFR-20260918-01.json"
        subject = f.parse(self.data[self.SUBJECT])
        self.update(self.SUBJECT, project_foundation_review_result_reference=ref,
                    evidence_paths=subject["evidence_paths"] + [ref])
        self.update("epics/WS-E01/binding.json", project_foundation_review_result_reference=ref)
        with self.assertRaisesRegex(f.Invalid, "PASS required"):
            self.validate()

    def test_orphan_preparation_rejected(self):
        for paths in ({"epics/E/binding.json"}, {"epics/E/evidence/auth.json"}):
            with self.assertRaises(f.Invalid):
                f.epic_subject_paths(paths)
        self.assertEqual(["epics/E/subject.json"], f.epic_subject_paths({"epics/E/subject.json"}))

    def test_original_preparation_bytes_are_append_only(self):
        for path, raw in self.data.items():
            with self.subTest(path=path):
                with self.assertRaises(f.Invalid):
                    f.check_history_maps({path: raw}, {path: raw + b"\n"})
                with self.assertRaises(f.Invalid):
                    f.check_history_maps({path: raw}, {})


class EpicHistoryCliTests(unittest.TestCase):
    """Real CLI gates across accepted merge and unaccepted preparation commits."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="windowsafe-synthetic-epic-")
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name) / "repo"
        subprocess.run(["git", "clone", "--shared", "--no-checkout", str(f.ROOT), str(self.repo)],
                       check=True, capture_output=True)
        self.git("checkout", "--detach", EpicPreparationTests.BASELINE)
        self.git("config", "user.name", "Synthetic Fixture")
        self.git("config", "user.email", "synthetic@example.invalid")
        for name in ("tools/foundation.py", ".github/workflows/foundation.yml"):
            shutil.copyfile(f.ROOT / name, self.repo / name)
        for name in f.git("ls-tree", "-r", "--name-only", EpicPreparationTests.REVIEWED,
                          "--", "epics/WS-E01").decode().splitlines():
            target = self.repo / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(f.at(EpicPreparationTests.REVIEWED, name))
        self.first = self.save()

    def git(self, *args):
        return subprocess.check_output(["git", "-C", str(self.repo), *args], stderr=subprocess.PIPE).decode().strip()

    def save(self):
        self.git("add", "--all")  # Disposable synthetic fixture only.
        self.git("-c", "commit.gpgsign=false", "commit", "-m", "synthetic preparation")
        return self.git("rev-parse", "HEAD")

    def cli(self, *args, ok=True):
        result = subprocess.run([sys.executable, "tools/foundation.py", *args], cwd=self.repo,
                                capture_output=True, text=True)
        self.assertEqual(0 if ok else 1, result.returncode, result.stdout + result.stderr)
        return result

    def test_exact_request_check_and_history_baselines(self):
        self.cli("check")
        result = json.loads(self.cli("request", "--sha", "HEAD", "--subject", EpicPreparationTests.SUBJECT).stdout)
        self.assertEqual(self.first, result["subject"]["end_sha"])
        self.assertEqual("INDEPENDENT_EPIC_PREPARATION_REVIEWER", result["required_authority"])
        self.assertEqual(23, len(result["reviewed_evidence"]))
        for base in ("0" * 40, EpicPreparationTests.BASELINE, "4ba2c473fe4d90c85d94ee2b2f5cc5777d115109",
                     "9b6dd621deec1193bfdfbdfa730e8f9349c73fd6"):
            self.cli("history", "--base", base)
        self.cli("history", "--base", self.first, ok=False)

    def test_request_uses_committed_bytes_and_rejects_committed_drift(self):
        path = self.repo / EpicPreparationTests.SUBJECT
        subject = json.loads(path.read_text())
        subject["ready_for_agent"] = True
        path.write_text(json.dumps(subject) + "\n")
        self.cli("request", "--sha", "HEAD", "--subject", EpicPreparationTests.SUBJECT)
        self.cli("check", ok=False)
        self.save()
        self.cli("request", "--sha", "HEAD", "--subject", EpicPreparationTests.SUBJECT, ok=False)

    def test_old_and_new_original_mutations_cannot_hide_behind_later_event_base(self):
        for name in ("reviews/results/WS-PFR-20260918-02.json", "epics/WS-E01/preparation.md"):
            path = self.repo / name
            original = path.read_bytes()
            path.write_bytes(original + b"\n")
            changed = self.save()
            path.write_bytes(original)
            self.save()
            self.cli("history", "--base", changed, ok=False)
            self.cli("history", "--base", "0" * 40, ok=False)

    def test_unrelated_merge_is_still_rejected(self):
        self.git("switch", "-c", "synthetic-side")
        (self.repo / "README.md").write_text("synthetic side\n")
        self.save()
        self.git("checkout", "--detach", self.first)
        self.git("-c", "commit.gpgsign=false", "merge", "--no-ff", "synthetic-side", "-m", "synthetic unauthorized merge")
        self.cli("history", "--base", EpicPreparationTests.BASELINE, ok=False)

    def test_missing_or_changed_authorization_and_uncommitted_binding_rejected(self):
        path = self.repo / "epics/WS-E01/evidence/preparation-authorization.json"
        original = path.read_bytes()
        path.write_bytes(original + b"\n")
        self.cli("history", "--base", "0" * 40, ok=False)
        path.unlink()
        self.save()
        self.cli("history", "--base", "0" * 40, ok=False)

    def test_removing_exact_head_request_or_schema_ci_gate_rejected(self):
        path = self.repo / ".github/workflows/foundation.yml"
        original = path.read_text()
        for value in ("foundation.py request --sha HEAD --subject epics/WS-E01/subject.json",
                      "foundation.py schema-preflight --sha HEAD --schema reviews/review-contract.json",
                      "ref: ${{ github.event.pull_request.head.sha || github.sha }}"):
            path.write_text(original.replace(value, "REMOVED"))
            self.cli("check", ok=False)


class AcceptedEpicTests(unittest.TestCase):
    """Acceptance consumes real original bytes; mutations are in-memory fixtures."""

    SUBJECT = EpicPreparationTests.SUBJECT
    BINDING = "epics/WS-E01/binding.json"
    AUTH = "epics/WS-E01/evidence/integration-authorization.json"
    RESULT = "reviews/results/WS-E01-EPR-20260919-02.json"

    def setUp(self):
        self.data = {p.relative_to(f.ROOT).as_posix(): p.read_bytes() for p in f.files(f.ROOT)}

    def validate(self):
        return f.epic_preparation(self.SUBJECT, self.data.__getitem__, f.commit("HEAD"))

    def update(self, path, **changes):
        value = f.parse(self.data[path])
        value.update(changes)
        self.data[path] = (json.dumps(value) + "\n").encode()

    def test_accepted_binding_keeps_reviewed_subject_and_nonblocking_finding(self):
        self.assertEqual(EpicPreparationTests.BASELINE, self.validate()[0])
        original = f.request(EpicPreparationTests.REVIEWED, self.SUBJECT)
        result = f.parse(self.data[self.RESULT])
        self.assertEqual(original["subject"], result["subject"])
        self.assertEqual(original["reviewed_evidence"], result["reviewed_evidence"])
        binding = f.parse(self.data[self.BINDING])
        self.assertEqual([item["id"] for item in result["findings"] if item["status"] == "OPEN"],
                         binding["open_nonblocking_finding_ids"])

    def test_missing_or_changed_original_result_and_authorization_rejected(self):
        for path in (self.AUTH, self.RESULT):
            original = self.data[path]
            self.data[path] += b"\n"
            with self.subTest(path=path), self.assertRaises(f.Invalid):
                self.validate()
            del self.data[path]
            with self.subTest(missing=path), self.assertRaises(KeyError):
                self.validate()
            self.data[path] = original

    def test_binding_cannot_hide_findings_change_baselines_or_enable_execution(self):
        original = self.data[self.BINDING]
        for changes in (
            {"ready_for_agent": False}, {"ready_for_agent": 1},
            {"epic_preparation_subject_immutable_reference": {"end_sha": f.commit("HEAD")}},
            {"epic_preparation_review_result_reference": "reviews/results/OTHER.json"},
            {"current_canonical_baseline_or_main_sha": "0" * 40},
            {"approved_product_definition_reference": "README.md"},
            {"project_foundation_review_result_reference": "reviews/results/WS-PFR-20260918-01.json"},
            {"open_nonblocking_finding_ids": []}, {"open_critical_blocking_major_findings": "PENDING"},
            {"open_material_user_decisions_required_before_start": "OPEN"},
            {"nonblocking_follow_up_reference": "../outside"},
            {"execution_scope": "FEATURE_EXECUTION"}, {"product_features_started": True},
        ):
            self.data[self.BINDING] = original
            self.update(self.BINDING, **changes)
            with self.subTest(changes=changes), self.assertRaises(f.Invalid):
                self.validate()

    def test_original_subject_and_preparation_evidence_remain_immutable(self):
        for path in (self.SUBJECT, "epics/WS-E01/preparation.md",
                     "epics/WS-E01/evidence/research.md", "epics/WS-E01/evidence/self-review.md",
                     "epics/WS-E01/evidence/preparation-authorization.json"):
            original = self.data[path]
            self.data[path] += b"\n"
            with self.subTest(path=path), self.assertRaises(f.Invalid):
                self.validate()
            self.data[path] = original

    def test_canonical_result_validation_cannot_be_replaced_by_authorization(self):
        original = self.data[self.RESULT]
        for mutation in ("BLOCKED", "MAJOR", "evidence", "self-review", "subject", "marker"):
            result = f.parse(original)
            if mutation == "BLOCKED":
                result["verdict"] = "BLOCKED"
            elif mutation == "MAJOR":
                result["findings"][0]["severity"] = "MAJOR"
            elif mutation == "evidence":
                result["reviewed_evidence"][0]["sha256"] = "0" * 64
            elif mutation == "self-review":
                result["reviewer"]["identity"] = f.parse(self.data[self.SUBJECT])["implementer"]
            elif mutation == "subject":
                result["subject"]["end_sha"] = EpicPreparationTests.BASELINE
            else:
                result["findings"][0]["disposition"] = "nonblocking"
            self.data[self.RESULT] = (json.dumps(result) + "\n").encode()
            auth = f.parse(self.data[self.AUTH])
            auth["EXACT_RESULT_BINDING"] = {"bytes": len(self.data[self.RESULT]),
                                            "sha256": f.sha256(self.data[self.RESULT])}
            self.data[self.AUTH] = (json.dumps(auth) + "\n").encode()
            # Only a disposable fixture trusts these synthetic pins. The real pin is unchanged.
            with patch.object(f, "INTEGRATION_AUTHORIZATIONS", {self.AUTH: f.sha256(self.data[self.AUTH])}):
                with self.subTest(mutation=mutation), self.assertRaises(f.Invalid):
                    self.validate()

    def test_history_requires_exact_one_way_transition_and_present_evidence(self):
        old = f.at(EpicPreparationTests.REVIEWED, self.BINDING)
        new = self.data[self.BINDING]
        required = {p: self.data[p] for p in (self.SUBJECT, self.AUTH, self.RESULT)}
        transitions = {self.BINDING: (old, new, required)}
        before = {self.BINDING: old}
        after = dict(required, **{self.BINDING: new})
        f.check_history_maps(before, after, transitions)
        for changed in ({self.BINDING: new}, dict(after, **{self.BINDING: new + b"\n"}),
                        dict(after, **{self.RESULT: self.data[self.RESULT] + b"\n"})):
            with self.assertRaises(f.Invalid):
                f.check_history_maps(before, changed, transitions)
        with self.assertRaises(f.Invalid):
            f.check_history_maps(after, dict(after, **{self.BINDING: old}), transitions)


class AcceptedEpicHistoryCliTests(unittest.TestCase):
    """Full CLI on disposable integration commits and a normal local merge."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="windowsafe-synthetic-acceptance-")
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name) / "repo"
        subprocess.run(["git", "clone", "--shared", "--no-checkout", str(f.ROOT), str(self.repo)],
                       check=True, capture_output=True)
        self.git("checkout", "--detach", EpicPreparationTests.REVIEWED)
        self.git("config", "user.name", "Synthetic Fixture")
        self.git("config", "user.email", "synthetic@example.invalid")
        self.git("switch", "-c", "synthetic-integration")
        for name in f.INTEGRATION_SUPPORT_PATHS | {AcceptedEpicTests.BINDING, AcceptedEpicTests.AUTH,
                                                  AcceptedEpicTests.RESULT}:
            target = self.repo / name
            target.parent.mkdir(parents=True, exist_ok=True)
            if name.endswith(".md") and name in f.INTEGRATION_SUPPORT_PATHS:
                # This fixture models the historical Epic integration, before F01.
                # Keep its docs at that exact phase while exercising the current CLI.
                target.write_bytes(f.at("3bdd7439c221b8f8c83e7374c8bb29898891a4fd", name))
            else:
                shutil.copyfile(f.ROOT / name, target)
        self.first = self.save()

    git = EpicHistoryCliTests.git
    save = EpicHistoryCliTests.save
    cli = EpicHistoryCliTests.cli

    def test_accepted_head_preserves_original_request_and_all_history_bases(self):
        self.cli("check")
        current = json.loads(self.cli("request", "--sha", "HEAD", "--subject", AcceptedEpicTests.SUBJECT).stdout)
        original = json.loads(self.cli("request", "--sha", EpicPreparationTests.REVIEWED,
                                       "--subject", AcceptedEpicTests.SUBJECT).stdout)
        self.assertEqual(original, current)
        self.assertEqual(23, len(current["reviewed_evidence"]))
        self.cli("validate-result", "--file", AcceptedEpicTests.RESULT)
        for base in ("0" * 40, EpicPreparationTests.BASELINE, EpicPreparationTests.REVIEWED):
            self.cli("history", "--base", base)

    def test_normal_merge_retains_accepted_tree_and_history(self):
        self.git("checkout", "--detach", EpicPreparationTests.BASELINE)
        self.git("-c", "commit.gpgsign=false", "merge", "--no-ff", "synthetic-integration", "-m", "synthetic normal merge")
        self.assertEqual(self.git("rev-parse", self.first + "^{tree}"), self.git("rev-parse", "HEAD^{tree}"))
        self.cli("check")
        self.cli("history", "--base", EpicPreparationTests.BASELINE)
        self.cli("request", "--sha", "HEAD", "--subject", AcceptedEpicTests.SUBJECT)

    def test_binding_rewrite_then_revert_cannot_hide_in_history(self):
        path = self.repo / AcceptedEpicTests.BINDING
        original = path.read_bytes()
        path.write_bytes(original + b"\n")
        changed = self.save()
        path.write_bytes(original)
        self.save()
        self.cli("history", "--base", changed, ok=False)

    def test_result_rewrite_then_revert_cannot_hide_in_history(self):
        path = self.repo / AcceptedEpicTests.RESULT
        original = path.read_bytes()
        path.write_bytes(original + b"\n")
        changed = self.save()
        path.write_bytes(original)
        self.save()
        self.cli("history", "--base", changed, ok=False)

    def test_acceptance_binding_cannot_be_committed_before_its_original(self):
        self.git("checkout", "--detach", EpicPreparationTests.REVIEWED)
        shutil.copyfile(f.ROOT / "tools/foundation.py", self.repo / "tools/foundation.py")
        shutil.copyfile(f.ROOT / AcceptedEpicTests.BINDING, self.repo / AcceptedEpicTests.BINDING)
        changed = self.save()
        for name in (AcceptedEpicTests.AUTH, AcceptedEpicTests.RESULT):
            shutil.copyfile(f.ROOT / name, self.repo / name)
        self.save()
        self.cli("history", "--base", changed, ok=False)

    def test_unrelated_merge_and_product_delta_still_rejected(self):
        self.git("switch", "-c", "synthetic-unrelated")
        (self.repo / "README.md").write_text("synthetic side\n")
        self.save()
        self.git("checkout", "--detach", self.first)
        self.git("-c", "commit.gpgsign=false", "merge", "--no-ff", "synthetic-unrelated", "-m", "synthetic unrelated merge")
        self.cli("history", "--base", EpicPreparationTests.BASELINE, ok=False)
        (self.repo / "manifest.json").write_text("{}\n")
        self.save()
        self.cli("check", ok=False)


if __name__ == "__main__":
    unittest.main()
