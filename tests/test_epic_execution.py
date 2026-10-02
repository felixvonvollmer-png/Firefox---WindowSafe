"""WS-E01 execution phase after the integration merge: scope, append-only, PR merges, feature requests."""

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

SOURCE = f.ROOT  # Fixtures patch f.ROOT; materialized bytes still come from here.
EXECUTION_FILES = {f.EPIC_EXECUTION_AUTH, "tools/foundation.py", "tests/test_epic_execution.py",
                   ".github/workflows/foundation.yml", "AGENTS.md", "README.md", "epics/README.md",
                   "foundation/context.md", "foundation/engineering.md", "reviews/README.md"}
FEATURE = "features/WS-E01-F01/subject.json"


def dump(value):
    return (json.dumps(value, indent=2) + "\n").encode()


class ExecutionScopeTests(unittest.TestCase):

    def test_product_and_feature_paths(self):
        for path in ("addon/manifest.json", "addon/src/capture/model.ts", "addon/ui/popup.html", "addon/icons/ws.svg",
                     "addon/package-lock.json", "qualification/ws-e01-f01/probe/manifest.json",
                     "features/WS-E01-F01/subject.json", "features/WS-E01-F05/evidence/r500-ubuntu.json"):
            with self.subTest(path=path):
                f.scope(path)
        for path in ("addon/icons/ws.png", "addon/node_modules/x/index.js", "manifest.json", "src/x.ts",
                     "features/WS-E02-F01/subject.json", "features/WS-E01-F06/subject.json", "addon/../x.ts",
                     "addon/a/b/c/d/e/f.ts", "qualification/ws-e02-f01/x.py", "secrets.txt"):
            with self.subTest(path=path), self.assertRaises(f.Invalid):
                f.scope(path)

    def test_self_verdict_normalizes_like_the_request(self):
        req = {"implementer": " Lead ", "review_excluded_identities": ["LEAD", "worker"]}
        self.assertTrue(f.self_verdict("lead", req))
        self.assertTrue(f.self_verdict(" WORKER ", req))
        self.assertFalse(f.self_verdict("independent", req))
        with self.assertRaisesRegex(f.Invalid, "exclusion set"):
            f.self_verdict("x", {"implementer": "other", "review_excluded_identities": ["LEAD"]})

    def test_authorization_is_pinned_and_bound_to_rebinding(self):
        data = {p.relative_to(f.ROOT).as_posix(): p.read_bytes() for p in f.files(f.ROOT)}
        f.execution_authorization_integrity(data.__getitem__)
        changed = dict(data)
        changed[f.EPIC_EXECUTION_AUTH] = data[f.EPIC_EXECUTION_AUTH] + b"\n"
        with self.assertRaisesRegex(f.Invalid, "hash"):
            f.execution_authorization_integrity(changed.__getitem__)
        changed = dict(data)
        changed[f.EPIC_REBINDING] = data[f.EPIC_REBINDING] + b"\n"
        with self.assertRaisesRegex(f.Invalid, "broad execution authorization"):
            f.execution_authorization_integrity(changed.__getitem__)


class ExecutionHistoryTests(unittest.TestCase):
    """Real Git continuation from the integration merge on main."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="windowsafe-synthetic-execution-")
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name) / "repo"
        subprocess.run(["git", "clone", "--shared", "--no-checkout", str(f.ROOT), str(self.repo)],
                       check=True, capture_output=True)
        self.git("checkout", "--detach", f.EPIC_INTEGRATION_MERGE)
        self.git("config", "user.name", "Synthetic Fixture")
        self.git("config", "user.email", "synthetic@example.invalid")
        self.git("switch", "-c", "synthetic-main")
        for name in EXECUTION_FILES:
            target = self.repo / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(SOURCE / name, target)
        self.authorized = self.save("synthetic execution authorization")
        patcher = patch.object(f, "ROOT", self.repo)
        patcher.start()
        self.addCleanup(patcher.stop)

    def git(self, *args):
        return subprocess.check_output(["git", "-C", str(self.repo), *args],
                                       stderr=subprocess.PIPE).decode().strip()

    def save(self, message="synthetic"):
        self.git("add", "--all")  # Only the disposable synthetic fixture.
        self.git("-c", "commit.gpgsign=false", "commit", "-m", message)
        return self.git("rev-parse", "HEAD")

    def write(self, path, data):
        (self.repo / path).parent.mkdir(parents=True, exist_ok=True)
        (self.repo / path).write_bytes(data)

    def valid(self, head=None):
        head = head or self.git("rev-parse", "HEAD")
        self.assertEqual(f.request(f.EPIC_CORR2_REVIEWED, f.EPIC_CORR2_SUBJECT), f.request(head, f.EPIC_CORR2_SUBJECT))
        return head

    def rejected(self, pattern, head=None):
        with self.assertRaisesRegex(f.Invalid, pattern):
            f.request(head or self.git("rev-parse", "HEAD"), f.EPIC_CORR2_SUBJECT)

    def test_authorized_head_and_product_commits_pass_all_gates(self):
        self.valid(self.authorized)
        self.write("addon/manifest.json", b'{"manifest_version": 3}\n')
        self.write("addon/src/model.ts", b"export const x = 1;\n")
        head = self.valid(self.save())
        self.assertIn(f.EPIC_INTEGRATION_MERGE, f.epic_delta_merges(head))
        f.check(self.repo)
        for base in ("0" * 40, f.EPIC_DELTA_BASE, f.EPIC_INTEGRATION_MERGE):
            f.history(base)
        for args in (["check"], ["history", "--base", f.EPIC_INTEGRATION_MERGE],
                     ["request", "--sha", "HEAD", "--subject", f.EPIC_CORR2_SUBJECT]):
            with self.subTest(args=args):
                result = subprocess.run([sys.executable, "tools/foundation.py", *args], cwd=self.repo,
                                        capture_output=True, text=True)
                self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_without_authorization_no_commit_after_the_merge(self):
        self.git("checkout", "--detach", f.EPIC_INTEGRATION_MERGE)
        self.write("addon/src/model.ts", b"export const x = 1;\n")
        self.rejected("scope|merge", self.save())

    def test_frozen_append_only_and_out_of_scope_paths_rejected(self):
        cases = (
            ("foundation/inputs/inputs/WindowSafe_Product_Definition_WS-PD-20260917-01.md", "frozen|append-only"),
            (f.EPIC_CORR2_DIR + "evidence.md", "frozen|append-only"),
            (f.EPIC_REBINDING, "frozen|append-only"),
            ("reviews/review-contract.json", "frozen|append-only"),
            ("reviews/results/WS-E01-EPR-DELTA-20260930-05.json", "append-only"),
            ("epics/WS-E01/binding.json", "append-only"),
            ("addon/icons/ws.png", "scope"), ("secrets.txt", "scope"),
        )
        for path, pattern in cases:
            with self.subTest(path=path):
                self.git("checkout", "--detach", self.authorized)
                existing = (self.repo / path).exists()
                self.write(path, ((self.repo / path).read_bytes() if existing else b"") + b"x\n")
                self.save()
                if existing:
                    self.git("checkout", self.authorized, "--", path)
                    self.save("synthetic revert")
                self.rejected(pattern)

    def commit_change(self, path, data=None, delete=False):
        self.git("checkout", "--detach", self.authorized)
        if delete:
            self.git("rm", "-q", path)
        else:
            self.write(path, data if data is not None else (self.repo / path).read_bytes() + b"x\n")
        return self.save()

    def test_historical_foundation_records_frozen_but_living_routers_open(self):
        for path in ("foundation/subject.json", "foundation/reviewer-environment.md"):
            with self.subTest(path=path):
                self.rejected("frozen", self.commit_change(path))
        # architecture.md is additionally blob-pinned as mandatory review evidence.
        self.rejected("frozen|drift", self.commit_change("foundation/architecture.md"))
        self.valid(self.commit_change("foundation/context.md"))
        # A rename is a deletion plus an addition; the frozen source side is caught.
        self.git("checkout", "--detach", self.authorized)
        (self.repo / "features/WS-E01-F01").mkdir(parents=True, exist_ok=True)
        self.git("mv", "foundation/subject.json", "features/WS-E01-F01/subject.json")
        self.rejected("frozen", self.save())

    def test_gate_code_cannot_be_deleted(self):
        self.rejected("gate code deleted", self.commit_change("tests/test_epic_rebinding.py", delete=True))
        # Bound evidence reads already fail closed before the deletion guard for these.
        for path in ("tools/foundation.py", ".github/workflows/foundation.yml", "tools/fixture_helper.py"):
            with self.subTest(path=path):
                if path == "tools/fixture_helper.py":
                    self.git("checkout", "--detach", self.authorized)
                    self.write(path, b"VALUE = 1\n")
                    self.save()
                    self.git("rm", "-q", path)
                    head = self.save()
                    self.rejected("gate code deleted", head)
                else:
                    with self.assertRaises((f.Invalid, subprocess.CalledProcessError)):
                        f.request(self.commit_change(path, delete=True), f.EPIC_CORR2_SUBJECT)

    def test_only_regular_files_symlinks_and_submodules_rejected(self):
        self.git("checkout", "--detach", self.authorized)
        (self.repo / "addon").mkdir(exist_ok=True)
        (self.repo / "addon/link.js").symlink_to("../README.md")
        self.rejected("file mode", self.save())
        self.git("checkout", "--detach", self.authorized)
        self.git("update-index", "--add", "--cacheinfo", "160000," + f.EPIC_INTEGRATION_MERGE + ",addon/sub.js")
        self.git("-c", "commit.gpgsign=false", "commit", "-m", "synthetic gitlink")
        self.rejected("file mode")

    def test_octopus_and_foreign_first_parent_merges_rejected(self):
        heads = []
        for name in ("a", "b"):
            self.git("checkout", "--detach", self.authorized)
            self.write("addon/" + name + ".ts", b"export {};\n")
            heads.append(self.save())
        self.git("checkout", "--detach", self.authorized)
        self.git("-c", "commit.gpgsign=false", "merge", "--no-ff", *heads, "-m", "synthetic octopus")
        self.rejected("octopus")
        # First parent outside the execution lineage (pre-merge main) is not an accepted PR merge.
        self.git("checkout", "--detach", f.EPIC_DELTA_BASE)
        self.git("-c", "commit.gpgsign=false", "merge", "--no-ff", self.authorized, "-m", "synthetic foreign base")
        with self.assertRaises((f.Invalid, subprocess.CalledProcessError)):
            f.request(self.git("rev-parse", "HEAD"), f.EPIC_CORR2_SUBJECT)

    def test_authorization_outside_the_integrated_lineage_rejected(self):
        # Same execution files directly on the rebound head, without the integration merge.
        self.git("checkout", "--detach", f.EPIC_INTEGRATION_MERGE + "^2")
        for name in EXECUTION_FILES:
            shutil.copyfile(SOURCE / name, self.repo / name)
        head = self.save()
        with self.assertRaises((f.Invalid, subprocess.CalledProcessError)):
            f.request(head, f.EPIC_CORR2_SUBJECT)

    def test_check_validates_the_authorization_record(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for p in f.files(self.repo):
                target = root / p.relative_to(self.repo)
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(p.read_bytes())
            (root / f.EPIC_EXECUTION_AUTH).write_bytes((root / f.EPIC_EXECUTION_AUTH).read_bytes() + b"\n")
            with self.assertRaisesRegex(f.Invalid, "authorization hash"):
                f.check(root)

    def test_manifest_only_inside_product_paths(self):
        f.scope("addon/manifest.json")
        with self.assertRaisesRegex(f.Invalid, "manifest"):
            f.scope("features/WS-E01-F01/evidence/manifest.json")

    def test_feature_request_rechecks_history_and_phase(self):
        subject = {"subject_id": "WS-E01-F01", "review_type": "FEATURE_ACCEPTANCE_REVIEW",
                   "implementer": "LEAD", "review_excluded_identities": ["LEAD"],
                   "evidence_paths": [f.EPIC_EXECUTION_AUTH]}
        self.commit_change("foundation/subject.json")
        self.write(FEATURE, dump(subject))
        with self.assertRaisesRegex(f.Invalid, "frozen"):
            f.request(self.save(), FEATURE)
        # The phase check holds on its own, even if history validation were bypassed.
        self.git("checkout", "--detach", f.EPIC_INTEGRATION_MERGE)
        self.write(FEATURE, dump(subject))
        head = self.save()
        with patch.object(f, "delta_history", lambda sha: sha):
            with self.assertRaisesRegex(f.Invalid, "bound WS-E01 execution"):
                f.request(head, FEATURE)

    def test_feature_contributors_must_be_a_list(self):
        subject = {"subject_id": "WS-E01-F01", "review_type": "FEATURE_ACCEPTANCE_REVIEW",
                   "implementer": "L", "contributors": "WORKER",
                   "review_excluded_identities": ["L", "W", "O", "R", "K", "E"],
                   "evidence_paths": [f.EPIC_EXECUTION_AUTH]}
        self.git("checkout", "--detach", self.authorized)
        self.write(FEATURE, dump(subject))
        with self.assertRaisesRegex(f.Invalid, "contributors must be a list"):
            f.request(self.save(), FEATURE)

    def test_check_rejects_non_regular_tracked_modes(self):
        # Only staged, not committed: isolates the check() mode guard from the history guards.
        self.git("checkout", "--detach", self.authorized)
        self.git("update-index", "--add", "--cacheinfo", "160000," + f.EPIC_INTEGRATION_MERGE + ",addon/sub.js")
        with self.assertRaisesRegex(f.Invalid, "tracked file mode"):
            f.check(self.repo)

    def test_hand_built_merge_cannot_drop_main_changes(self):
        # main gains a test module; a stale branch is merged with its own tree via commit-tree.
        self.write("tests/test_execution_marker.py", b"VALUE = 1\n")
        main = self.save()
        self.git("checkout", "--detach", self.authorized)
        self.write("addon/src/x.ts", b"export {};\n")
        stale = self.save()
        tree = self.git("rev-parse", stale + "^{tree}")
        merge = self.git("-c", "commit.gpgsign=false", "commit-tree", tree, "-p", main, "-p", stale, "-m", "synthetic drop")
        with self.assertRaises((f.Invalid, subprocess.CalledProcessError)):
            f.request(merge, f.EPIC_CORR2_SUBJECT)

    def test_forged_initial_authorization_rejected(self):
        self.git("checkout", "--detach", f.EPIC_INTEGRATION_MERGE)
        for name in EXECUTION_FILES:
            shutil.copyfile(SOURCE / name, self.repo / name)
        value = f.parse((self.repo / f.EPIC_EXECUTION_AUTH).read_bytes())
        value["RELEASE_OR_PRODUCTION_AUTHORIZED"] = True
        self.write(f.EPIC_EXECUTION_AUTH, dump(value))
        self.rejected("authorization hash", self.save())

    def test_gitlink_rejected_even_with_permissive_diff_config(self):
        self.git("config", "diff.ignoreSubmodules", "all")
        self.git("checkout", "--detach", self.authorized)
        self.git("update-index", "--add", "--cacheinfo", "160000," + f.EPIC_INTEGRATION_MERGE + ",addon/sub.js")
        self.git("-c", "commit.gpgsign=false", "commit", "-m", "synthetic gitlink")
        self.rejected("file mode")

    def test_up_to_date_pr_merge_accepted_and_stale_merge_rejected(self):
        self.git("switch", "-c", "synthetic-feature")
        self.write("addon/src/a.ts", b"export const a = 1;\n")
        feature = self.save()
        self.git("switch", "synthetic-main")
        self.git("-c", "commit.gpgsign=false", "merge", "--no-ff", feature, "-m", "synthetic PR merge")
        merge = self.valid()
        self.assertIn(merge, f.epic_delta_merges(merge))
        f.history(f.EPIC_INTEGRATION_MERGE)
        self.write("addon/src/b.ts", b"export const b = 1;\n")
        self.save()
        self.git("switch", "-c", "synthetic-stale", feature)
        self.write("addon/src/c.ts", b"export const c = 1;\n")
        stale = self.save()
        self.git("switch", "synthetic-main")
        self.git("-c", "commit.gpgsign=false", "merge", "--no-ff", stale, "-m", "synthetic stale merge")
        self.rejected("up to date")

    def test_feature_request_requires_complete_author_exclusion(self):
        subject = {"subject_id": "WS-E01-F01", "review_type": "FEATURE_ACCEPTANCE_REVIEW",
                   "implementer": "CODING_AGENT_SYNTHETIC_LEAD", "materializer": "CODING_AGENT_SYNTHETIC_LEAD",
                   "contributors": ["CODING_AGENT_SYNTHETIC_WORKER"],
                   "review_excluded_identities": ["CODING_AGENT_SYNTHETIC_LEAD"],
                   "evidence_paths": [f.EPIC_EXECUTION_AUTH]}
        self.write(FEATURE, dump(subject))
        head = self.save()
        with self.assertRaisesRegex(f.Invalid, "feature author exclusion incomplete"):
            f.request(head, FEATURE)
        subject["review_excluded_identities"].append("coding_agent_synthetic_worker")
        self.write(FEATURE, dump(subject))
        head = self.save()
        req = f.request(head, FEATURE)
        self.assertEqual(subject["review_excluded_identities"], req["review_excluded_identities"])
        result = {
            "schema_version": 3, "review_id": "WS-E01-FAR-SYNTHETIC", "review_type": req["review_type"],
            "reviewer": {"authority": req["required_authority"], "identity": " CODING_AGENT_SYNTHETIC_WORKER ",
                         "run_reference": "synthetic", "independence": "FRESH_OR_SUFFICIENTLY_ISOLATED"},
            "provenance": {"source_reference": "synthetic", "transport": "EXACT_AUTHORIZED_TRANSFER"},
            "subject": req["subject"], "verdict": "PASS", "findings": [], "reviewed_evidence": req["reviewed_evidence"],
            "result_reference": "reviews/results/WS-E01-FAR-SYNTHETIC.json",
        }
        contract = f.parse(f.at(head, f.CONTRACT_PATH))
        with self.assertRaisesRegex(f.Invalid, "self verdict"):
            f.validate_result(result, req, contract, "WS-E01-FAR-SYNTHETIC.json")
        result["reviewer"]["identity"] = "INDEPENDENT_FEATURE_REVIEWER_SYNTHETIC"
        f.validate_result(result, req, contract, "WS-E01-FAR-SYNTHETIC.json")
        # Feature subjects are bound to the authorized execution phase only.
        self.git("checkout", "--detach", f.EPIC_INTEGRATION_MERGE)
        self.write(FEATURE, dump(subject))
        with self.assertRaises(f.Invalid):
            f.request(self.save(), FEATURE)


if __name__ == "__main__":
    unittest.main()
