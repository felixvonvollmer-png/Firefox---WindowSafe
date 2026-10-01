"""Exact epic rebinding of -04 after its independent PASS and the single normal PR #5 merge."""

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

HISTORICAL = "epics/WS-E01/subject.json"
SOURCE = f.ROOT  # Fixtures patch f.ROOT; materialized bytes still come from here.


def reader(data):
    def read(name):
        if name not in data:
            raise FileNotFoundError(name)
        return data[name]
    return read


def dump(value):
    return (json.dumps(value, indent=2) + "\n").encode()


class RebindingIntegrityTests(unittest.TestCase):
    """Exact materialized bytes; every mutation is an in-memory fixture."""

    def setUp(self):
        self.data = {p.relative_to(f.ROOT).as_posix(): p.read_bytes() for p in f.files(f.ROOT)}

    def rejected(self, data, pattern):
        with self.assertRaisesRegex(f.Invalid, pattern):
            f.epic_rebinding_integrity(reader(data))

    def test_rebinding_is_ready_and_bound_to_the_reviewed_pass(self):
        f.epic_rebinding_integrity(reader(self.data))
        rebinding = f.parse(self.data[f.EPIC_REBINDING])
        self.assertEqual(("READY_FOR_AGENT", True, "PASS"),
                         (rebinding["status"], rebinding["ready_for_agent"], rebinding["independent_epic_preparation_review"]))
        self.assertEqual(f.EPIC_CORR2_REVIEWED, rebinding["epic_preparation_subject_immutable_reference"]["end_sha"])
        self.assertIs(False, rebinding["f01_continuation_authorized"])
        self.assertEqual("REVIEW_REQUIRED", f.parse(self.data[f.EPIC_CORR2_BINDING])["status"])

    def test_result_authorization_and_reviewed_namespaces_reject_drift(self):
        for path in [f.EPIC_REBIND_RESULT, f.EPIC_REBIND_AUTH, f.EPIC_CORR2_BINDING, f.EPIC_CORR2_SUBJECT,
                     *f.EPIC_CORR_RESULTS, f.EPIC_DELTA_RESULT, *sorted(f.EPIC_CORR_FILES)]:
            with self.subTest(path=path):
                data = dict(self.data)
                data[path] = self.data[path] + b"\n"
                with self.assertRaises(f.Invalid):
                    f.epic_rebinding_integrity(reader(data))

    def test_rebinding_cannot_claim_more_than_the_bound_transition(self):
        rebinding = f.parse(self.data[f.EPIC_REBINDING])
        mutations = {
            "ready_for_agent": 1, "f01_continuation_authorized": True,
            "broad_ws_e01_execution_authorization": "AUTHORIZED",
            "execution_scope": "WS_E01_FEATURE_EXECUTION",
            "epic_preparation_subject_immutable_reference": dict(
                rebinding["epic_preparation_subject_immutable_reference"], end_sha=f.EPIC_CORR_REVIEWED),
            "open_nonblocking_finding_ids": [], "open_critical_blocking_major_findings": "NONE_CLAIMED",
            "review_excluded_identities": rebinding["review_excluded_identities"][1:],
            "extra": True,
        }
        for key, value in mutations.items():
            with self.subTest(key=key):
                data = dict(self.data)
                data[f.EPIC_REBINDING] = dump(dict(rebinding, **{key: value}))
                self.rejected(data, "rebinding mismatch")

    def test_scope_and_check(self):
        for name in (f.EPIC_REBINDING, f.EPIC_REBIND_AUTH, f.EPIC_REBIND_RESULT):
            f.scope(name)
        with self.assertRaises(f.Invalid):
            f.scope(f.EPIC_CORR2_DIR + "rebinding-2.json")
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for path, data in self.data.items():
                (root / path).parent.mkdir(parents=True, exist_ok=True)
                (root / path).write_bytes(data)
            f.check(root)
            (root / f.EPIC_REBINDING).write_bytes(dump(dict(f.parse(self.data[f.EPIC_REBINDING]), status="ACCEPTED")))
            with self.assertRaisesRegex(f.Invalid, "rebinding mismatch"):
                f.check(root)


class RebindingHistoryTests(unittest.TestCase):
    """Real Git: rebinding commit after the reviewed head and the one normal merge into main."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="windowsafe-synthetic-epic-rebinding-")
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name) / "repo"
        subprocess.run(["git", "clone", "--shared", "--no-checkout", str(f.ROOT), str(self.repo)],
                       check=True, capture_output=True)
        self.git("checkout", "--detach", f.EPIC_CORR2_REVIEWED)
        self.git("config", "user.name", "Synthetic Fixture")
        self.git("config", "user.email", "synthetic@example.invalid")
        self.copy(f.EPIC_REBIND_ALLOWED)
        self.rebound = self.save("synthetic rebinding")
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

    def save(self, message="synthetic"):
        self.git("add", "--all")  # Only the disposable synthetic fixture.
        self.git("-c", "commit.gpgsign=false", "commit", "-m", message)
        return self.git("rev-parse", "HEAD")

    def merge(self, onto, other):
        self.git("checkout", "--detach", onto)
        self.git("-c", "commit.gpgsign=false", "merge", "--no-ff", other, "-m", "synthetic normal merge")
        return self.git("rev-parse", "HEAD")

    def reviewed_requests(self, head):
        for path, reviewed in ((f.EPIC_CORR2_SUBJECT, f.EPIC_CORR2_REVIEWED), (f.EPIC_CORR_SUBJECT, f.EPIC_CORR_REVIEWED),
                               (f.EPIC_DELTA_SUBJECT, f.EPIC_DELTA_REVIEWED), (HISTORICAL, f.EPIC_DELTA_BASE)):
            with self.subTest(path=path, head=head):
                self.assertEqual(f.request(reviewed, path), f.request(head, path))

    def test_rebound_head_requests_check_and_history(self):
        self.reviewed_requests(self.rebound)
        f.check(self.repo)
        for base in ("0" * 40, f.EPIC_DELTA_BASE, f.EPIC_CORR2_REVIEWED):
            f.history(base)
        self.assertEqual(set(), f.epic_delta_merges(self.rebound))

    def test_exactly_one_normal_merge_into_bound_main_is_recognized(self):
        merge = self.merge(f.EPIC_DELTA_BASE, self.rebound)
        self.reviewed_requests(merge)
        self.assertEqual({merge}, f.epic_delta_merges(merge))
        self.assertEqual({f.EPIC_DELTA_BASE}, f.delta_integration_merges(merge))
        self.assertEqual(f.request("bbca750fab1e760714cf409b8751287db6b93041", f.DELTA_SUBJECT),
                         f.request(merge, f.DELTA_SUBJECT))
        f.check(self.repo)
        for base in ("0" * 40, f.EPIC_DELTA_BASE):
            f.history(base)
        for args in (["check"], ["history", "--base", f.EPIC_DELTA_BASE],
                     ["request", "--sha", "HEAD", "--subject", f.EPIC_CORR2_SUBJECT],
                     ["validate-result", "--file", f.EPIC_REBIND_RESULT]):
            with self.subTest(args=args):
                result = subprocess.run([sys.executable, "tools/foundation.py", *args], cwd=self.repo,
                                        capture_output=True, text=True)
                self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_merge_without_rebinding_or_into_other_base_rejected(self):
        merge = self.merge(f.EPIC_DELTA_BASE, f.EPIC_CORR2_REVIEWED)
        with self.assertRaisesRegex(f.Invalid, "merges prohibited"):
            f.request(merge, f.EPIC_CORR2_SUBJECT)
        self.git("checkout", "--detach", f.EPIC_CORR_REVIEWED)
        self.git("switch", "-c", "synthetic-other-base")
        (self.repo / "README.md").write_bytes((self.repo / "README.md").read_bytes() + b"other\n")
        other = self.save()
        merge = self.merge(other, self.rebound)
        with self.assertRaisesRegex(f.Invalid, "authorized epic delta merge required"):
            f.request(merge, f.EPIC_CORR2_SUBJECT)

    def test_merge_tree_drift_second_merge_and_later_commit_rejected(self):
        self.git("checkout", "--detach", f.EPIC_DELTA_BASE)
        self.git("-c", "commit.gpgsign=false", "merge", "--no-ff", "--no-commit", self.rebound)
        (self.repo / "README.md").write_bytes((self.repo / "README.md").read_bytes() + b"drift\n")
        drifted = self.save("synthetic drifted merge")
        with self.assertRaisesRegex(f.Invalid, "tree drift"):
            f.request(drifted, f.EPIC_CORR2_SUBJECT)
        merge = self.merge(f.EPIC_DELTA_BASE, self.rebound)
        (self.repo / "README.md").write_bytes((self.repo / "README.md").read_bytes() + b"after\n")
        later = self.save()
        with self.assertRaises(f.Invalid):
            f.request(later, f.EPIC_CORR2_SUBJECT)
        self.git("checkout", "--detach", self.rebound)
        self.git("switch", "-c", "synthetic-second")
        (self.repo / "README.md").write_bytes((self.repo / "README.md").read_bytes() + b"second\n")
        second = self.save()
        again = self.merge(merge, second)
        with self.assertRaises(f.Invalid):
            f.request(again, f.EPIC_CORR2_SUBJECT)

    def test_rebinding_files_are_append_only_even_when_reverted(self):
        for path in (f.EPIC_REBINDING, f.EPIC_REBIND_AUTH, f.EPIC_REBIND_RESULT, f.EPIC_CORR2_BINDING):
            with self.subTest(path=path):
                self.git("checkout", "--detach", self.rebound)
                original = (self.repo / path).read_bytes()
                (self.repo / path).write_bytes(original + b"\n")
                self.save()
                (self.repo / path).write_bytes(original)
                head = self.save()
                with self.assertRaisesRegex(f.Invalid, "scope|append-only"):
                    f.request(head, f.EPIC_CORR2_SUBJECT)

    def test_rebinding_without_reviewed_ancestry_rejected(self):
        self.git("checkout", "--detach", f.EPIC_CORR_REVIEWED)
        self.copy(f.EPIC_CORR2_ALLOWED | f.EPIC_REBIND_ALLOWED)
        head = self.save()
        with self.assertRaises((f.Invalid, subprocess.CalledProcessError)):
            f.request(head, f.EPIC_CORR2_SUBJECT)


if __name__ == "__main__":
    unittest.main()
