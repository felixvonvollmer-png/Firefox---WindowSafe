"""Bound WS-E01 epic preparation delta regressions; offline inputs and disposable Git only."""

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
PF_INTEGRATION_HEAD = "1fb16ff993a303d2b4af95a0be77616b4940edfa"
HISTORICAL = "epics/WS-E01/subject.json"
SECOND = "epics/WS-E01/deltas/WS-E01-EP-DELTA-20260929-03/subject.json"
SOURCE = f.ROOT  # Fixtures patch f.ROOT; materialized bytes still come from here.


class EpicDeltaIntegrityTests(unittest.TestCase):
    """Exact materialized bytes; every mutation is an in-memory fixture."""

    def setUp(self):
        self.data = {p.relative_to(f.ROOT).as_posix(): p.read_bytes() for p in f.files(f.ROOT)}

    def validate(self):
        f.epic_delta_integrity(self.data.__getitem__)

    def update(self, path, **changes):
        value = f.parse(self.data[path])
        value.update(changes)
        self.data[path] = (json.dumps(value, indent=2) + "\n").encode()

    def test_materialized_subject_is_bound_and_pending(self):
        self.validate()
        subject = f.parse(self.data[f.EPIC_DELTA_SUBJECT])
        binding = f.parse(self.data[f.EPIC_DELTA_BINDING])
        self.assertEqual(("WS-E01", "EPIC_PREPARATION_REVIEW"), (subject["epic_id"], subject["review_type"]))
        self.assertEqual(("REVIEW_REQUIRED", False), (binding["status"], binding["ready_for_agent"]))
        self.assertIsNone(binding["epic_preparation_review_result_reference"])

    def test_every_original_and_pinned_reference_rejects_byte_drift(self):
        for path in list(f.EPIC_DELTA_ORIGINALS) + list(f.EPIC_DELTA_PINNED_BLOBS):
            with self.subTest(path=path):
                original = self.data[path]
                self.data[path] = original + b"\n"
                with self.assertRaises(f.Invalid):
                    self.validate()
                self.data[path] = original

    def test_subject_lifecycle_references_and_claims_cannot_drift(self):
        inputs = f.DELTA_INPUTS
        mutations = {
            "subject_id": "WS-E01-EP-DELTA-20260929-03", "epic_id": "WS-E02",
            "review_type": "FEATURE_ACCEPTANCE_REVIEW", "status": "READY_FOR_AGENT",
            "current_canonical_baseline_or_main_sha": f.DELTA_BASE,
            "independent_review_status": "PASS", "risk": "LOW",
            "ready_for_agent": True, "product_features_started": True,
            "browser_profile_tests_executed": True, "f01_continuation_authorized": True,
            "exact_epic_rebinding_created": True, "broad_ws_e01_execution_authorization_created": True,
            "feature_acceptance_started": 0,
            "open_material_user_decisions_required_before_start": ["UNRESOLVED"],
            "project_foundation_binding_reference": "epics/WS-E01/binding.json",
            "project_foundation_review_result_reference": "reviews/results/WS-PFR-20260918-02.json",
            "external_project_context_sync": "NOT_APPLICABLE",
            "external_project_context_sync_reference": f.EPIC_DELTA_DIR + "execution-direction.json",
            "approved_product_delta_reference": "foundation/inputs/inputs/WindowSafe_Product_Definition_WS-PD-20260917-01.md",
            "technical_foundation_delta_reference":
                inputs + "WindowSafe_Technical_Foundation_Delta_Preparation_WS-TFP-DELTA-20260928-01.md",
            "epic_research_reuse_or_delta_status": "UPDATED",
            "execution_authorization_sha256": "a" * 64,
            "f01_evidence_reference": {"pr": 3, "head": "a" * 40, "role": "READ_ONLY_EXTERNAL_QUALIFICATION_EVIDENCE"},
            "extra": True,
        }
        original = self.data[f.EPIC_DELTA_SUBJECT]
        for key, value in mutations.items():
            with self.subTest(key=key):
                self.update(f.EPIC_DELTA_SUBJECT, **{key: value})
                with self.assertRaises(f.Invalid):
                    self.validate()
                self.data[f.EPIC_DELTA_SUBJECT] = original

    def test_evidence_missing_unsafe_duplicate_or_self_referential(self):
        evidence = f.parse(self.data[f.EPIC_DELTA_SUBJECT])["evidence_paths"]
        for changed in ([p for p in evidence if p != f.EPIC_DELTA_BINDING], evidence + [evidence[0]],
                        evidence + ["../outside.md"], evidence + [f.EPIC_DELTA_SUBJECT], evidence + ["product.ts"]):
            with self.subTest(changed=changed[-1]):
                self.update(f.EPIC_DELTA_SUBJECT, evidence_paths=changed)
                with self.assertRaises((f.Invalid, KeyError)):
                    self.validate()

    def test_binding_cannot_become_ready_or_accepted_before_review(self):
        mutations = (
            {"status": "READY_FOR_AGENT"}, {"ready_for_agent": True}, {"ready_for_agent": 0},
            {"epic_preparation_review_result_reference": "reviews/results/WS-E01-EPR-DELTA.json"},
            {"independent_epic_preparation_review": "PASS"}, {"exact_epic_rebinding": "CREATED"},
            {"f01_continuation_authorized": True}, {"broad_ws_e01_execution_authorization": "AUTHORIZED"},
            {"open_critical_blocking_major_findings": "NONE"},
            {"open_material_user_decisions_required_before_start": "OPEN"},
            {"external_project_context_sync": "PENDING"}, {"historical_epic_binding": "REPLACED"},
            {"extra": True},
        )
        original = self.data[f.EPIC_DELTA_BINDING]
        for changes in mutations:
            with self.subTest(changes=changes):
                self.update(f.EPIC_DELTA_BINDING, **changes)
                with self.assertRaisesRegex(f.Invalid, "pending"):
                    self.validate()
                self.data[f.EPIC_DELTA_BINDING] = original

    def test_scope_allows_only_the_exact_delta_files(self):
        for name in f.EPIC_DELTA_FILES:
            f.scope(name)
        for name in (SECOND, f.EPIC_DELTA_DIR + "extra.md", "epics/WS-E01/deltas/subject.json",
                     f.EPIC_DELTA_DIR + "manifest.json", "epics/WS-E02/deltas/" + f.EPIC_DELTA_ID + "/subject.json"):
            with self.subTest(name=name), self.assertRaises(f.Invalid):
                f.scope(name)

    def test_check_rejects_second_delta_and_missing_ci_request(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for path, data in self.data.items():
                (root / path).parent.mkdir(parents=True, exist_ok=True)
                (root / path).write_bytes(data)
            f.check(root)
            (root / SECOND).parent.mkdir(parents=True)
            (root / SECOND).write_bytes(self.data[f.EPIC_DELTA_SUBJECT])
            with self.assertRaisesRegex(f.Invalid, "scope"):
                f.check(root)
            shutil.rmtree((root / SECOND).parent)
            workflow = root / ".github/workflows/foundation.yml"
            workflow.write_text(workflow.read_text().replace(
                " --subject " + f.EPIC_DELTA_SUBJECT, " --subject " + HISTORICAL))
            with self.assertRaisesRegex(f.Invalid, "epic delta CI"):
                f.check(root)


class EpicDeltaHistoryTests(unittest.TestCase):
    """Real Git continuation from the integrated foundation merge."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="windowsafe-synthetic-epic-delta-")
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name) / "repo"
        subprocess.run(["git", "clone", "--shared", "--no-checkout", str(f.ROOT), str(self.repo)],
                       check=True, capture_output=True)
        self.git("checkout", "--detach", f.EPIC_DELTA_BASE)
        self.git("config", "user.name", "Synthetic Fixture")
        self.git("config", "user.email", "synthetic@example.invalid")
        self.git("switch", "-c", "synthetic-epic-delta")
        self.copy(f.EPIC_DELTA_FILES | f.EPIC_DELTA_SUPPORT)
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
        self.git("-c", "commit.gpgsign=false", "commit", "-m", "synthetic epic delta")
        return self.git("rev-parse", "HEAD")

    def edit(self, path, data):
        (self.repo / path).parent.mkdir(parents=True, exist_ok=True)
        (self.repo / path).write_bytes(data)
        return self.save()

    def rejected(self, pattern, path=f.EPIC_DELTA_SUBJECT, head=None):
        with self.assertRaisesRegex(f.Invalid, pattern):
            f.request(head or self.git("rev-parse", "HEAD"), path)

    def test_exact_request_historical_requests_check_and_history(self):
        req = f.request(self.first, f.EPIC_DELTA_SUBJECT)
        subject = f.parse(f.at(self.first, f.EPIC_DELTA_SUBJECT))
        self.assertEqual({"id": f.EPIC_DELTA_ID, "path": f.EPIC_DELTA_SUBJECT, "end_sha": self.first}, req["subject"])
        self.assertEqual(("EPIC_PREPARATION_REVIEW", "INDEPENDENT_EPIC_PREPARATION_REVIEWER"),
                         (req["review_type"], req["required_authority"]))
        self.assertEqual(subject["implementer"], req["implementer"])
        self.assertEqual(sorted(subject["evidence_paths"]), sorted(e["path"] for e in req["reviewed_evidence"]))
        self.assertEqual(f.request(f.EPIC_DELTA_BASE, HISTORICAL), f.request(self.first, HISTORICAL))
        self.assertEqual(f.request(PF_REVIEWED, f.DELTA_SUBJECT), f.request(self.first, f.DELTA_SUBJECT))
        self.assertEqual(PF_REVIEWED, f.delta_history(self.first))
        self.assertEqual({f.EPIC_DELTA_BASE}, f.delta_integration_merges(self.first))
        f.check(self.repo)
        for base in ("0" * 40, f.EPIC_DELTA_BASE, f.DELTA_BASE):
            f.history(base)

    def test_cli_gates_on_the_synthetic_head(self):
        for args in (["check"], ["request", "--sha", "HEAD", "--subject", f.EPIC_DELTA_SUBJECT],
                     ["request", "--sha", "HEAD", "--subject", HISTORICAL],
                     ["schema-preflight", "--sha", "HEAD", "--schema", f.CONTRACT_PATH],
                     ["history", "--base", f.EPIC_DELTA_BASE]):
            with self.subTest(args=args):
                result = subprocess.run([sys.executable, "tools/foundation.py", *args], cwd=self.repo,
                                        capture_output=True, text=True)
                self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_second_or_mislocated_delta_subject_rejected(self):
        raw = (self.repo / f.EPIC_DELTA_SUBJECT).read_bytes()
        second = dict(f.parse(raw), subject_id="WS-E01-EP-DELTA-20260929-03")
        self.edit(SECOND, (json.dumps(second, indent=2) + "\n").encode())
        self.rejected("locator", SECOND)
        self.rejected("scope")
        self.git("checkout", "--detach", self.first)
        self.edit("epics/WS-E01/deltas/OTHER/subject.json", raw)
        self.rejected("locator", "epics/WS-E01/deltas/OTHER/subject.json")

    def test_committed_delta_files_are_append_only_even_when_reverted(self):
        for path in (f.EPIC_DELTA_SUBJECT, f.EPIC_DELTA_BINDING, f.EPIC_DELTA_EVIDENCE, f.EPIC_DELTA_AUTH):
            with self.subTest(path=path):
                self.git("checkout", "--detach", self.first)
                original = (self.repo / path).read_bytes()
                self.edit(path, original + b"\n")
                self.edit(path, original)
                self.rejected("append-only")

    def test_historical_epic_and_foundation_files_cannot_change(self):
        for path in list(f.EPIC_DELTA_PINNED_BLOBS) + ["epics/WS-E01/evidence/research.md", "foundation/subject.json"]:
            with self.subTest(path=path):
                self.git("checkout", "--detach", self.first)
                original = (self.repo / path).read_bytes()
                self.edit(path, original + b"\n")
                self.edit(path, original)
                self.rejected("scope|append-only")
                # The foundation acceptance cannot be used to admit the same edit.
                self.rejected("scope|append-only", f.DELTA_SUBJECT)

    def test_fresh_ready_binding_rejected_without_history_help(self):
        # Amended into the first delta commit, so only the exact pending-binding guard applies.
        value = f.parse((self.repo / f.EPIC_DELTA_BINDING).read_bytes())
        value.update(status="READY_FOR_AGENT", ready_for_agent=True)
        (self.repo / f.EPIC_DELTA_BINDING).write_text(json.dumps(value, indent=2) + "\n")
        self.git("add", "--all")
        self.git("-c", "commit.gpgsign=false", "commit", "--amend", "-m", "synthetic tampered")
        self.rejected("pending")

    def test_out_of_scope_verdict_product_and_reverted_paths_rejected(self):
        for path in ("product.ts", "reviews/results/WS-E01-EPR-DELTA-20260929-01.json",
                     "features/WS-E01-F01/subject.json", "tests/test_foundation.py"):
            with self.subTest(path=path):
                self.git("checkout", "--detach", self.first)
                existed = (self.repo / path).exists()
                original = (self.repo / path).read_bytes() if existed else b""
                self.edit(path, original + b"# synthetic\n")
                if existed:
                    (self.repo / path).write_bytes(original)
                else:
                    (self.repo / path).unlink()
                self.save()
                self.rejected("scope")

    def test_merge_in_continuation_rejected(self):
        self.git("switch", "-c", "synthetic-side")
        self.edit("README.md", b"synthetic side\n")
        self.git("checkout", "--detach", self.first)
        self.git("-c", "commit.gpgsign=false", "merge", "--no-ff", "synthetic-side", "-m", "synthetic merge")
        self.rejected("merges prohibited")
        self.rejected("merges prohibited", HISTORICAL)

    def test_delta_without_integrated_foundation_ancestry_rejected(self):
        # Same delta files on the pre-merge integration head: 1cb82c9 is not an ancestor.
        self.git("checkout", "--detach", PF_INTEGRATION_HEAD)
        self.copy(f.EPIC_DELTA_FILES | f.EPIC_DELTA_SUPPORT)
        head = self.save()
        with self.assertRaises((f.Invalid, subprocess.CalledProcessError)):
            f.request(head, f.EPIC_DELTA_SUBJECT)


if __name__ == "__main__":
    unittest.main()
