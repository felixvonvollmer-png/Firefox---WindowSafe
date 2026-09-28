"""Bound Foundation delta regressions; offline inputs and disposable Git only."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import foundation as f


class DeltaIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.data = {p.relative_to(f.ROOT).as_posix(): p.read_bytes() for p in f.files(f.ROOT)}

    def test_bound_originals_and_subject(self):
        f.delta_integrity(self.data.__getitem__)

    def test_every_original_and_source_rejects_byte_drift(self):
        paths = [p for p in self.data if p.startswith(f.DELTA_INPUTS)] + list(f.DELTA_SOURCES)
        for path in paths:
            with self.subTest(path=path):
                changed = dict(self.data, **{path: self.data[path] + b"\n"})
                with self.assertRaises(f.Invalid):
                    f.delta_integrity(changed.__getitem__)

    def test_lifecycle_baseline_authority_and_evidence_cannot_drift(self):
        original = f.parse(self.data[f.DELTA_SUBJECT])
        mutations = {
            "start_baseline_sha": "a" * 40, "work_branch": "main",
            "subject_id": "UNAUTHORIZED", "execution_authorization_sha256": "b" * 64,
            "independent_review_status": "PASS", "risk": "LOW",
            "product_features_started": True, "integration_authorized": True,
            "epic_delta_started": True, "f01_continuation_authorized": True,
            "feature_acceptance_started": True, "operations_policy": "ACTIVE",
            "external_project_context_sync": "NOT_APPLICABLE",
            "open_material_user_decisions": ["UNRESOLVED"], "evidence_paths": [],
            "f01_evidence_reference": {"pr": 3, "head": "a" * 40},
        }
        for key, value in mutations.items():
            with self.subTest(key=key):
                changed = dict(self.data)
                changed[f.DELTA_SUBJECT] = json.dumps(dict(original, **{key: value})).encode()
                with self.assertRaises(f.Invalid):
                    f.delta_integrity(changed.__getitem__)

    def test_unknown_input_inventory_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for path, data in self.data.items():
                target = root / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
            (root / f.DELTA_INPUTS / "unbound.json").write_text('{}\n')
            with self.assertRaisesRegex(f.Invalid, "inventory"):
                f.input_integrity(root)

    def test_new_subject_history_is_append_only(self):
        for path in (f.DELTA_SUBJECT, f.DELTA_EVIDENCE):
            before = {path: self.data[path]}
            for after in ({}, {path: self.data[path] + b"\n"}):
                with self.assertRaises(f.Invalid):
                    f.check_history_maps(before, after)


class DeltaHistoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="windowsafe-synthetic-foundation-delta-")
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name) / "repo"
        subprocess.run(["git", "clone", "--shared", "--no-checkout", str(f.ROOT), str(self.repo)],
                       check=True, capture_output=True)
        self.git("checkout", "--detach", f.DELTA_BASE)
        self.git("config", "user.name", "Synthetic Fixture")
        self.git("config", "user.email", "synthetic@example.invalid")
        for source in f.files(f.ROOT):
            target = self.repo / source.relative_to(f.ROOT)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(source.read_bytes())
        self.first = self.save()

    def git(self, *args):
        return subprocess.check_output(["git", "-C", str(self.repo), *args],
                                       stderr=subprocess.PIPE).decode().strip()

    def save(self):
        self.git("add", "--all")  # Only the disposable synthetic fixture.
        self.git("-c", "commit.gpgsign=false", "commit", "-m", "synthetic delta")
        return self.git("rev-parse", "HEAD")

    def test_exact_request_historical_request_and_full_history(self):
        with patch.object(f, "ROOT", self.repo):
            req = f.request(self.first, f.DELTA_SUBJECT)
            self.assertEqual(req["subject"]["end_sha"], self.first)
            self.assertEqual(req["required_authority"], "INDEPENDENT_PROJECT_LLM")
            self.assertEqual(f.request(self.first, "epics/WS-E01/subject.json"),
                             f.request(f.DELTA_BASE, "epics/WS-E01/subject.json"))
            self.assertEqual(f.request(self.first)["subject"]["id"], "WS-HC-20260918-01")
            f.history(f.DELTA_BASE)
            f.history("0" * 40)
            f.check()
            with self.assertRaises(subprocess.CalledProcessError):
                f.request(self.first, "foundation/deltas/UNBOUND/subject.json")

    def test_reverted_out_of_scope_commit_is_still_rejected(self):
        path = self.repo / "product.ts"
        path.write_text('// synthetic forbidden product file\n')
        self.save()
        path.unlink()
        final = self.save()
        with patch.object(f, "ROOT", self.repo), self.assertRaisesRegex(f.Invalid, "scope"):
            f.request(final, f.DELTA_SUBJECT)

    def test_reverted_original_edit_is_still_rejected(self):
        path = self.repo / f.DELTA_EVIDENCE
        original = path.read_bytes()
        path.write_bytes(original + b"\n")
        self.save()
        path.write_bytes(original)
        final = self.save()
        with patch.object(f, "ROOT", self.repo), self.assertRaisesRegex(f.Invalid, "append-only"):
            f.request(final, f.DELTA_SUBJECT)

    def test_extra_epic_edit_cannot_use_foundation_authorization(self):
        path = self.repo / "epics/WS-E01/preparation.md"
        path.write_bytes(path.read_bytes() + b"\n")
        final = self.save()
        with patch.object(f, "ROOT", self.repo), self.assertRaisesRegex(f.Invalid, "scope"):
            f.request(final, f.DELTA_SUBJECT)


if __name__ == "__main__":
    unittest.main()
