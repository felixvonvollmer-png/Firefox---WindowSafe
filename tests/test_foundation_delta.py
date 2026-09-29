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

REVIEWED = "bbca750fab1e760714cf409b8751287db6b93041"
RESULT = "reviews/results/WS-PFR-DELTA-20260928-01.json"


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
        # Pre-acceptance fixture: exact reviewed tree, independent of later acceptance files.
        for name in f.git("ls-tree", "-r", "--name-only", REVIEWED).decode().splitlines():
            target = self.repo / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(f.at(REVIEWED, name))
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
            f.check(self.repo)
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


class AcceptedDeltaIntegrationTests(unittest.TestCase):
    """Only the bound post-review transition and one exact normal merge are accepted."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="windowsafe-synthetic-delta-acceptance-")
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name) / "repo"
        subprocess.run(["git", "clone", "--shared", "--no-checkout", str(f.ROOT), str(self.repo)],
                       check=True, capture_output=True)
        self.git("checkout", "--detach", REVIEWED)
        self.git("config", "user.name", "Synthetic Fixture")
        self.git("config", "user.email", "synthetic@example.invalid")
        self.git("switch", "-c", "synthetic-integration")
        for name in f.DELTA_SUPPORT | {f.DELTA_BINDING, f.DELTA_INTEGRATION_AUTH, RESULT}:
            target = self.repo / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((f.ROOT / name).read_bytes())
        self.first = self.save()
        patcher = patch.object(f, "ROOT", self.repo)
        patcher.start()
        self.addCleanup(patcher.stop)

    git = DeltaHistoryTests.git
    save = DeltaHistoryTests.save

    def edit(self, path, data):
        (self.repo / path).parent.mkdir(parents=True, exist_ok=True)
        (self.repo / path).write_bytes(data)
        return self.save()

    def update_binding(self, **changes):
        value = f.parse((self.repo / f.DELTA_BINDING).read_bytes())
        value.update(changes)
        return self.edit(f.DELTA_BINDING, (json.dumps(value, indent=2) + "\n").encode())

    def merge(self, base=f.DELTA_BASE, branch="synthetic-integration"):
        self.git("checkout", "--detach", base)
        self.git("-c", "commit.gpgsign=false", "merge", "--no-ff", branch, "-m", "synthetic normal merge")
        return self.git("rev-parse", "HEAD")

    def rejected(self, pattern, head=None):
        with self.assertRaisesRegex(f.Invalid, pattern):
            f.request(head or self.git("rev-parse", "HEAD"), f.DELTA_SUBJECT)

    def test_accepted_head_keeps_reviewed_request_result_and_history(self):
        original = f.request(REVIEWED, f.DELTA_SUBJECT)
        self.assertEqual(original["subject"]["end_sha"], REVIEWED)
        self.assertEqual(original, f.request(self.first, f.DELTA_SUBJECT))
        self.assertEqual(REVIEWED, f.delta_history(self.first))
        self.assertEqual(set(), f.delta_integration_merges(self.first))
        f.validate_result_file(self.repo / RESULT)
        f.check(self.repo)
        for base in ("0" * 40, f.DELTA_BASE, REVIEWED):
            f.history(base)
        self.assertEqual(f.request(self.first, "epics/WS-E01/subject.json"),
                         f.request(f.DELTA_BASE, "epics/WS-E01/subject.json"))

    def test_exact_normal_merge_is_the_only_recognized_integration(self):
        merge = self.merge()
        self.assertEqual(self.git("rev-parse", self.first + "^{tree}"), self.git("rev-parse", "HEAD^{tree}"))
        self.assertEqual(f.request(REVIEWED, f.DELTA_SUBJECT), f.request(merge, f.DELTA_SUBJECT))
        self.assertEqual({merge}, f.delta_integration_merges(merge))
        f.check(self.repo)
        f.history(f.DELTA_BASE)
        f.request(merge, "epics/WS-E01/subject.json")

    def test_result_bytes_cannot_drift(self):
        self.edit(RESULT, (self.repo / RESULT).read_bytes() + b"\n")
        self.rejected("append-only|result mismatch")

    def test_binding_values_and_types_cannot_drift(self):
        for changes in ({"external_project_context_sync": "NOT_APPLICABLE"}, {"next_gate": "FIRST_EPIC_PREPARATION"},
                        {"f01_continuation_authorized": True}, {"epic_delta_started": 0},
                        {"independent_review_verdict": "PASS", "extra": True}):
            with self.subTest(changes=changes):
                self.git("checkout", "--detach", self.first)
                self.update_binding(**changes)
                self.rejected("append-only|binding mismatch")

    def test_fresh_tampered_binding_is_rejected_without_history_help(self):
        # Squashed into the first integration commit, so only the exact binding guard applies.
        value = f.parse((self.repo / f.DELTA_BINDING).read_bytes())
        value["external_project_context_sync"] = "NOT_APPLICABLE"
        (self.repo / f.DELTA_BINDING).write_text(json.dumps(value, indent=2) + "\n")
        self.git("add", "--all")
        self.git("-c", "commit.gpgsign=false", "commit", "--amend", "-m", "synthetic tampered")
        self.rejected("accepted binding mismatch")

    def test_authorization_subject_and_evidence_are_immutable(self):
        for path in (f.DELTA_INTEGRATION_AUTH, f.DELTA_SUBJECT, f.DELTA_EVIDENCE):
            with self.subTest(path=path):
                self.git("checkout", "--detach", self.first)
                self.edit(path, (self.repo / path).read_bytes() + b"\n")
                self.rejected("append-only|hash|drift|scope")

    def test_out_of_scope_and_reverted_integration_edits_rejected(self):
        for path in ("product.ts", "epics/WS-E01/preparation.md", "foundation/subject.json"):
            with self.subTest(path=path):
                self.git("checkout", "--detach", self.first)
                original = (self.repo / path).read_bytes() if (self.repo / path).exists() else None
                self.edit(path, (original or b"") + b"// synthetic\n")
                if original is None:
                    (self.repo / path).unlink()
                else:
                    (self.repo / path).write_bytes(original)
                self.save()
                self.rejected("scope|append-only")

    def test_binding_rewrite_then_revert_cannot_hide(self):
        original = (self.repo / f.DELTA_BINDING).read_bytes()
        self.edit(f.DELTA_BINDING, original + b"\n")
        self.edit(f.DELTA_BINDING, original)
        self.rejected("append-only")

    def test_merge_with_wrong_parent_tree_drift_or_second_merge_rejected(self):
        self.rejected("normal merge", self.merge(base=REVIEWED))
        self.git("checkout", "--detach", f.DELTA_BASE)
        self.git("-c", "commit.gpgsign=false", "merge", "--no-ff", "--no-commit", "synthetic-integration")
        (self.repo / "README.md").write_text("synthetic drift\n")
        self.git("add", "README.md")
        self.git("-c", "commit.gpgsign=false", "commit", "-m", "synthetic drifted merge")
        self.rejected("tree drift")
        merge = self.merge()
        self.git("switch", "-c", "synthetic-side")
        (self.repo / "README.md").write_text("synthetic side\n")
        self.save()
        self.rejected("normal merge", self.merge(base=merge, branch="synthetic-side"))

    def test_binding_is_invalid_without_the_authorized_reviewed_original(self):
        # Same final tree, but rebuilt directly on main: the reviewed head is not an ancestor.
        self.git("checkout", "--detach", f.DELTA_BASE)
        for name in self.git("ls-tree", "-r", "--name-only", self.first).splitlines():
            (self.repo / name).parent.mkdir(parents=True, exist_ok=True)
            (self.repo / name).write_bytes(f.at(self.first, name))
        self.save()
        with self.assertRaises((f.Invalid, subprocess.CalledProcessError)):
            f.request(self.git("rev-parse", "HEAD"), f.DELTA_SUBJECT)


if __name__ == "__main__":
    unittest.main()
