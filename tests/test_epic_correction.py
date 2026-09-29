"""Bound correction of the CORRECTION_REQUIRED WS-E01 delta; offline inputs and disposable Git only."""

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

PF_REVIEWED = "bbca750fab1e760714cf409b8751287db6b93041"
HISTORICAL = "epics/WS-E01/subject.json"
OTHER = "epics/WS-E01/deltas/WS-E01-EP-DELTA-20260929-04/subject.json"
TRUNCATED_BLOB = "930b4c3176a9601e44f7a4b04ff1d4530488b6"
SOURCE = f.ROOT  # Fixtures patch f.ROOT; materialized bytes still come from here.


class EpicCorrectionIntegrityTests(unittest.TestCase):
    """Exact materialized bytes; every mutation is an in-memory fixture."""

    def setUp(self):
        self.data = {p.relative_to(f.ROOT).as_posix(): p.read_bytes() for p in f.files(f.ROOT)}

    def validate(self):
        f.epic_correction_integrity(self.data.__getitem__)

    def update(self, path, **changes):
        value = f.parse(self.data[path])
        value.update(changes)
        self.data[path] = (json.dumps(value, indent=2) + "\n").encode()

    def rejected(self, path, pattern, **changes):
        original = self.data[path]
        self.update(path, **changes)
        with self.assertRaisesRegex(f.Invalid, pattern):
            self.validate()
        self.data[path] = original

    def test_materialized_correction_is_bound_and_pending(self):
        self.validate()
        subject = f.parse(self.data[f.EPIC_CORR_SUBJECT])
        binding = f.parse(self.data[f.EPIC_CORR_BINDING])
        self.assertEqual(f.EPIC_CORR_EXCLUDED, subject["review_excluded_identities"])
        self.assertEqual(f.EPIC_CORR_EXCLUDED, binding["review_excluded_identities"])
        self.assertEqual(("REVIEW_REQUIRED", False, None), (binding["status"], binding["ready_for_agent"],
                                                            binding["epic_preparation_review_result_reference"]))
        self.assertEqual(40, len(subject["historical_epic_binding_git_blob"]))
        self.assertEqual(f.EPIC_DELTA_REVIEWED, subject["superseded_subject"]["end_sha"])

    def test_originals_and_source_review_reject_byte_drift(self):
        for path in list(f.EPIC_CORR_ORIGINALS) + [f.EPIC_DELTA_RESULT]:
            with self.subTest(path=path):
                original = self.data[path]
                self.data[path] = original + b"\n"
                with self.assertRaises(f.Invalid):
                    self.validate()
                self.data[path] = original

    def test_exclusion_set_missing_extra_wrong_or_reordered(self):
        excluded = f.EPIC_CORR_EXCLUDED
        for changed in (excluded[:2], excluded[1:], excluded + ["CODING_AGENT_OTHER"],
                        [excluded[0], excluded[1], "CODING_AGENT_WS_E01_EPDELTA_CORR_20260929_02"],
                        list(reversed(excluded)), [value.lower() for value in excluded], []):
            with self.subTest(changed=changed):
                self.rejected(f.EPIC_CORR_SUBJECT, "subject boundary", review_excluded_identities=changed)
                self.rejected(f.EPIC_CORR_BINDING, "pending", review_excluded_identities=changed)
        original = self.data[f.EPIC_CORR_SUBJECT]
        value = f.parse(original)
        del value["review_excluded_identities"]
        self.data[f.EPIC_CORR_SUBJECT] = (json.dumps(value, indent=2) + "\n").encode()
        with self.assertRaises(f.Invalid):
            self.validate()

    def test_truncated_or_wrong_historical_binding_blob_rejected(self):
        for blob in (TRUNCATED_BLOB, "930b4c3176a9601e44f7a4b04ff1d4530488b6e0", TRUNCATED_BLOB + "E1"):
            with self.subTest(blob=blob):
                self.rejected(f.EPIC_CORR_SUBJECT, "subject boundary", historical_epic_binding_git_blob=blob)
                self.rejected(f.EPIC_CORR_BINDING, "pending", historical_epic_binding_git_blob=blob)
        # The immutable historical binding bytes themselves are checked against the full blob.
        original = self.data["epics/WS-E01/binding.json"]
        self.data["epics/WS-E01/binding.json"] = original + b"\n"
        with self.assertRaisesRegex(f.Invalid, "historical binding blob"):
            self.validate()

    def test_architecture_and_final_v6_evidence_required(self):
        evidence = f.parse(self.data[f.EPIC_CORR_SUBJECT])["evidence_paths"]
        for path in list(f.EPIC_CORR_PREWRITE) + [f.EPIC_DELTA_RESULT, f.EPIC_DELTA_SUBJECT,
                                                  "tests/test_epic_correction.py", f.EPIC_CORR_BINDING]:
            with self.subTest(path=path):
                self.rejected(f.EPIC_CORR_SUBJECT, "evidence incomplete",
                              evidence_paths=[p for p in evidence if p != path])
        for changed in (evidence + [evidence[0]], evidence + [f.EPIC_CORR_SUBJECT]):
            self.rejected(f.EPIC_CORR_SUBJECT, "evidence incomplete", evidence_paths=changed)
        self.rejected(f.EPIC_CORR_SUBJECT, "scope", evidence_paths=evidence + ["product.ts"])

    def test_prewrite_source_drift_rejected(self):
        original = self.data["foundation/architecture.md"]
        self.data["foundation/architecture.md"] = original + b"\n"
        with self.assertRaisesRegex(f.Invalid, "pre-write source drift"):
            self.validate()

    def test_subject_identity_lifecycle_and_claims_cannot_drift(self):
        mutations = {
            "implementer": "PROJECT_LLM_WS_E01_EP_DELTA_20260929_02",
            "materializer": "CODING_AGENT_WS_E01_EPDELTA_MAT_20260929_01",
            "status": "READY_FOR_AGENT", "ready_for_agent": True, "independent_review_status": "PASS",
            "exact_epic_rebinding_created": True, "f01_continuation_authorized": True,
            "product_features_started": True, "product_truth_change": "UPDATED",
            "execution_authorization_path": f.EPIC_DELTA_AUTH,
            "superseded_subject": dict(f.parse(self.data[f.EPIC_CORR_SUBJECT])["superseded_subject"],
                                       review_verdict="PASS"),
            "mandatory_prewrite_reads": f.DELTA_SOURCES,
            "extra": True,
        }
        for key, value in mutations.items():
            with self.subTest(key=key):
                self.rejected(f.EPIC_CORR_SUBJECT, "subject boundary|fields mismatch", **{key: value})

    def test_binding_cannot_become_ready_or_accepted_before_rereview(self):
        for changes in ({"status": "READY_FOR_AGENT"}, {"ready_for_agent": True},
                        {"epic_preparation_review_result_reference": f.EPIC_DELTA_RESULT},
                        {"independent_epic_preparation_review": "PASS"}, {"exact_epic_rebinding": "CREATED"},
                        {"broad_ws_e01_execution_authorization": "AUTHORIZED"},
                        {"superseded_review_verdict": "PASS"}, {"extra": True}):
            with self.subTest(changes=changes):
                self.rejected(f.EPIC_CORR_BINDING, "pending", **changes)

    def test_old_delta_namespace_drift_rejected(self):
        for path in sorted(f.EPIC_DELTA_FILES):
            with self.subTest(path=path):
                original = self.data[path]
                self.data[path] = original + b"\n"
                with self.assertRaisesRegex(f.Invalid, "reviewed delta namespace drift"):
                    self.validate()
                self.data[path] = original

    def test_scope_allows_only_the_exact_correction_files(self):
        for name in f.EPIC_CORR_FILES:
            f.scope(name)
        for name in (OTHER, f.EPIC_CORR_DIR + "extra.md", f.EPIC_CORR_DIR + "preparation.md",
                     "epics/WS-E02/deltas/" + f.EPIC_CORR_ID + "/subject.json"):
            with self.subTest(name=name), self.assertRaises(f.Invalid):
                f.scope(name)

    def test_check_requires_correction_ci_request(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for path, data in self.data.items():
                (root / path).parent.mkdir(parents=True, exist_ok=True)
                (root / path).write_bytes(data)
            f.check(root)
            workflow = root / ".github/workflows/foundation.yml"
            workflow.write_text(workflow.read_text().replace(" --subject " + f.EPIC_CORR_SUBJECT, " --subject " + HISTORICAL))
            with self.assertRaisesRegex(f.Invalid, "epic correction CI"):
                f.check(root)


class EpicCorrectionHistoryTests(unittest.TestCase):
    """Real Git continuation from the exact CORRECTION_REQUIRED head."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="windowsafe-synthetic-epic-correction-")
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name) / "repo"
        subprocess.run(["git", "clone", "--shared", "--no-checkout", str(f.ROOT), str(self.repo)],
                       check=True, capture_output=True)
        self.git("checkout", "--detach", f.EPIC_DELTA_REVIEWED)
        self.git("config", "user.name", "Synthetic Fixture")
        self.git("config", "user.email", "synthetic@example.invalid")
        self.git("switch", "-c", "synthetic-epic-correction")
        self.copy(f.EPIC_CORR_ALLOWED)
        self.first = self.save()
        patcher = patch.object(f, "ROOT", self.repo)
        patcher.start()
        self.addCleanup(patcher.stop)

    def git(self, *args):
        return subprocess.check_output(["git", "-C", str(self.repo), *args],
                                       stderr=subprocess.PIPE).decode().strip()

    def copy(self, names):
        for name in names:
            target = self.repo / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(SOURCE / name, target)

    def save(self):
        self.git("add", "--all")  # Only the disposable synthetic fixture.
        self.git("-c", "commit.gpgsign=false", "commit", "-m", "synthetic epic correction")
        return self.git("rev-parse", "HEAD")

    def edit(self, path, data):
        (self.repo / path).parent.mkdir(parents=True, exist_ok=True)
        (self.repo / path).write_bytes(data)
        return self.save()

    def rejected(self, pattern, path=f.EPIC_CORR_SUBJECT, head=None):
        with self.assertRaisesRegex(f.Invalid, pattern):
            f.request(head or self.git("rev-parse", "HEAD"), path)

    def result(self, req, identity):
        return {
            "schema_version": 3, "review_id": "WS-E01-EPR-DELTA-SYNTHETIC", "review_type": req["review_type"],
            "reviewer": {"authority": req["required_authority"], "identity": identity,
                         "run_reference": "synthetic fixture", "independence": "FRESH_OR_SUFFICIENTLY_ISOLATED"},
            "provenance": {"source_reference": "synthetic fixture", "transport": "EXACT_AUTHORIZED_TRANSFER"},
            "subject": req["subject"], "verdict": "PASS", "findings": [],
            "reviewed_evidence": req["reviewed_evidence"],
            "result_reference": "reviews/results/WS-E01-EPR-DELTA-SYNTHETIC.json",
        }

    def verdict(self, req, identity):
        f.validate_result(self.result(req, identity), req, f.parse(f.at(req["subject"]["end_sha"], f.CONTRACT_PATH)),
                          "WS-E01-EPR-DELTA-SYNTHETIC.json")

    def sidecar(self, req, identity):
        result = self.result(req, identity)
        record = {"result_sha256": "a" * 64, "subject": result["subject"],
                  "reviewed_evidence": result["reviewed_evidence"], "original_provenance": result["provenance"],
                  "reviewer": result["reviewer"], "provenance": result["provenance"], "decisions": []}
        f.validate_semantic_disposition(record, result, req, [], "a" * 64)

    def test_corrected_request_transports_exact_exclusion_set(self):
        req = f.request(self.first, f.EPIC_CORR_SUBJECT)
        subject = f.parse(f.at(self.first, f.EPIC_CORR_SUBJECT))
        self.assertEqual({"id": f.EPIC_CORR_ID, "path": f.EPIC_CORR_SUBJECT, "end_sha": self.first}, req["subject"])
        self.assertEqual(f.EPIC_CORR_EXCLUDED, req["review_excluded_identities"])
        self.assertEqual(f.EPIC_CORR_EXCLUDED[0], req["implementer"])
        self.assertEqual(sorted(subject["evidence_paths"]), sorted(e["path"] for e in req["reviewed_evidence"]))
        self.assertIn("foundation/architecture.md", {e["path"] for e in req["reviewed_evidence"]})

    def test_historical_requests_unchanged(self):
        old = f.request(f.EPIC_DELTA_REVIEWED, f.EPIC_DELTA_SUBJECT)
        self.assertEqual(old, f.request(self.first, f.EPIC_DELTA_SUBJECT))
        self.assertEqual(35, len(old["reviewed_evidence"]))
        self.assertEqual(f.request(f.EPIC_DELTA_BASE, HISTORICAL), f.request(self.first, HISTORICAL))
        self.assertEqual(f.request(PF_REVIEWED, f.DELTA_SUBJECT), f.request(self.first, f.DELTA_SUBJECT))
        for req in (old, f.request(self.first, HISTORICAL), f.request(self.first, f.DELTA_SUBJECT)):
            self.assertNotIn("review_excluded_identities", req)

    def test_every_excluded_author_rejected_as_reviewer_and_sidecar(self):
        req = f.request(self.first, f.EPIC_CORR_SUBJECT)
        for identity in f.EPIC_CORR_EXCLUDED:
            for variant in (identity, identity.lower(), " " + identity.title() + "\n"):
                with self.subTest(identity=variant):
                    with self.assertRaisesRegex(f.Invalid, "self verdict"):
                        self.verdict(req, variant)
                    with self.assertRaisesRegex(f.Invalid, "semantic self"):
                        self.sidecar(req, variant)

    def test_distinct_independent_reviewer_passes_identity_guard(self):
        req = f.request(self.first, f.EPIC_CORR_SUBJECT)
        # Naming excluded authors in a longer statement is not equality with one of them.
        for identity in ("INDEPENDENT_EPIC_REREVIEWER_SYNTHETIC",
                         "Reviewer, weder " + " noch ".join(f.EPIC_CORR_EXCLUDED)):
            self.verdict(req, identity)
            self.sidecar(req, identity)

    def test_historical_request_keeps_implementer_only_rule(self):
        old = f.request(self.first, f.EPIC_DELTA_SUBJECT)
        with self.assertRaisesRegex(f.Invalid, "self verdict"):
            self.verdict(old, old["implementer"].lower())
        # Unchanged historical semantics; the corrected subject closes this gap.
        self.verdict(old, f.EPIC_CORR_EXCLUDED[1])

    def test_request_exclusion_set_itself_is_validated(self):
        req = f.request(self.first, f.EPIC_CORR_SUBJECT)
        for changed in ([], f.EPIC_CORR_EXCLUDED[1:], "PROJECT_LLM_WS_E01_EP_DELTA_20260929_03",
                        f.EPIC_CORR_EXCLUDED + [" "]):
            with self.subTest(changed=changed):
                with self.assertRaisesRegex(f.Invalid, "exclusion set"):
                    self.verdict(dict(req, review_excluded_identities=changed), "INDEPENDENT_SYNTHETIC")

    def test_check_history_and_cli_gates(self):
        f.check(self.repo)
        for base in ("0" * 40, f.EPIC_DELTA_BASE, f.EPIC_DELTA_REVIEWED):
            f.history(base)
        for args in (["request", "--sha", "HEAD", "--subject", f.EPIC_CORR_SUBJECT],
                     ["request", "--sha", "HEAD", "--subject", f.EPIC_DELTA_SUBJECT],
                     ["validate-result", "--file", f.EPIC_DELTA_RESULT],
                     ["schema-preflight", "--sha", "HEAD", "--schema", f.CONTRACT_PATH],
                     ["history", "--base", f.EPIC_DELTA_REVIEWED]):
            with self.subTest(args=args):
                result = subprocess.run([sys.executable, "tools/foundation.py", *args], cwd=self.repo,
                                        capture_output=True, text=True)
                self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_old_delta_and_review_original_are_append_only_even_when_reverted(self):
        for path in sorted(f.EPIC_DELTA_FILES) + [f.EPIC_DELTA_RESULT, "epics/WS-E01/binding.json"]:
            with self.subTest(path=path):
                self.git("checkout", "--detach", self.first)
                original = (self.repo / path).read_bytes()
                self.edit(path, original + b"\n")
                self.edit(path, original)
                self.rejected("scope|append-only")
                self.rejected("scope|append-only", f.EPIC_DELTA_SUBJECT)

    def test_other_delta_path_and_out_of_scope_files_rejected(self):
        raw = (self.repo / f.EPIC_CORR_SUBJECT).read_bytes()
        self.edit(OTHER, raw)
        self.rejected("locator", OTHER)
        self.rejected("scope")
        for path in ("product.ts", "features/WS-E01-F01/subject.json", "tests/test_foundation.py",
                     "reviews/results/WS-E01-EPR-DELTA-20260929-02.json"):
            with self.subTest(path=path):
                self.git("checkout", "--detach", self.first)
                self.edit(path, b"# synthetic\n")
                self.rejected("scope")

    def test_merge_in_correction_section_rejected(self):
        self.git("switch", "-c", "synthetic-side")
        self.edit("README.md", b"synthetic side\n")
        self.git("checkout", "--detach", self.first)
        self.git("-c", "commit.gpgsign=false", "merge", "--no-ff", "synthetic-side", "-m", "synthetic merge")
        self.rejected("merges prohibited")
        self.rejected("merges prohibited", f.EPIC_DELTA_SUBJECT)

    def test_fresh_ready_binding_rejected_without_history_help(self):
        value = f.parse((self.repo / f.EPIC_CORR_BINDING).read_bytes())
        value.update(status="READY_FOR_AGENT", ready_for_agent=True)
        (self.repo / f.EPIC_CORR_BINDING).write_text(json.dumps(value, indent=2) + "\n")
        self.git("add", "--all")
        self.git("-c", "commit.gpgsign=false", "commit", "--amend", "-m", "synthetic tampered")
        self.rejected("pending")

    def test_correction_without_reviewed_head_ancestry_rejected(self):
        # Same correction files directly on main: the CORRECTION_REQUIRED head is not an ancestor.
        self.git("checkout", "--detach", f.EPIC_DELTA_BASE)
        self.copy(f.EPIC_DELTA_FILES | f.EPIC_CORR_ALLOWED)
        head = self.save()
        with self.assertRaises((f.Invalid, subprocess.CalledProcessError)):
            f.request(head, f.EPIC_CORR_SUBJECT)


if __name__ == "__main__":
    unittest.main()
