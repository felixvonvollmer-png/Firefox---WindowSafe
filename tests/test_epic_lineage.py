"""Lineage-closure reviewer exclusion of the second WS-E01 delta correction; offline, disposable Git only."""

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
OTHER = "epics/WS-E01/deltas/WS-E01-EP-DELTA-20260929-05/subject.json"
SOURCE = f.ROOT  # Fixtures patch f.ROOT; materialized bytes still come from here.
EXPECTED_LINEAGE = {
    "PROJECT_LLM_WS_E01_PREPARATION_20260919_01", "PROJECT_LLM_WS_E01_EP_DELTA_20260929_02",
    "PROJECT_LLM_WS_E01_EP_DELTA_20260929_03", "PROJECT_LLM_WS_E01_EP_DELTA_20260929_04",
    "CODING_AGENT_WS_E01_EPDELTA_MAT_20260929_01", "CODING_AGENT_WS_E01_EPDELTA_CORR_20260929_01",
    "CODING_AGENT_WS_E01_EPDELTA_CORR_20260929_02",
}


def reader(data):
    def read(name):
        if name not in data:
            raise FileNotFoundError(name)
        return data[name]
    return read


def dump(value):
    return (json.dumps(value, indent=2) + "\n").encode()


class LineageClosureTests(unittest.TestCase):
    """The derivation itself, on the materialized bytes and on synthetic lineages."""

    def setUp(self):
        self.data = {p.relative_to(f.ROOT).as_posix(): p.read_bytes() for p in f.files(f.ROOT)}

    def test_materialized_lineage_is_derived_mechanically(self):
        derived = f.review_exclusion_closure(reader(self.data), f.EPIC_CORR2_SUBJECT)
        self.assertEqual(EXPECTED_LINEAGE, derived)
        self.assertLessEqual(set(f.EPIC_CORR2_MINIMUM_EXCLUDED), derived)
        subject = f.parse(self.data[f.EPIC_CORR2_SUBJECT])
        self.assertLessEqual(derived, set(subject["review_excluded_identities"]))

    def test_closure_is_transitive_and_cardinality_free(self):
        base = "epics/SYN/"
        data = {
            base + "subject.json": dump({"review_type": "EPIC_PREPARATION_REVIEW", "implementer": "A0",
                                         "evidence_paths": ["epics/SYN/deltas/D9/notes.md"]}),
            base + "deltas/D1/subject.json": dump({"review_type": "EPIC_PREPARATION_REVIEW", "implementer": "A1",
                                                   "materializer": "M1", "prep": {"path": base + "preparation.md"}}),
            base + "deltas/D2/subject.json": dump({"review_type": "EPIC_PREPARATION_REVIEW", "implementer": "A2",
                                                   "review_excluded_identities": ["X2"],
                                                   "refs": [base + "deltas/D1/preparation.md"]}),
            base + "deltas/D3/subject.json": dump({"review_type": "EPIC_PREPARATION_REVIEW", "implementer": "A3",
                                                   "materializer": "M3", "superseded": {"path": base + "deltas/D2/subject.json"},
                                                   "product": "foundation/inputs/x.md", "result": "reviews/results/R.json",
                                                   "evidence_paths": [base + "deltas/D9/subject.json"]}),
            base + "deltas/D9/subject.json": dump({"review_type": "EPIC_PREPARATION_REVIEW", "implementer": "EVIDENCE_ONLY"}),
        }
        data[base + "deltas/D3/subject.json"] = dump(dict(f.parse(data[base + "deltas/D3/subject.json"]),
                                                          review_excluded_identities=["SELF_LISTED_ONLY"]))
        derived = f.review_exclusion_closure(reader(data), base + "deltas/D3/subject.json")
        # Evidence-only and product/review inputs are not authorship; depth is unbounded.
        self.assertEqual({"A3", "M3", "A2", "X2", "A1", "M1", "A0"}, derived)
        data[base + "deltas/D1/subject.json"] = dump(dict(f.parse(data[base + "deltas/D1/subject.json"]),
                                                          materializer="M1_NEW"))
        self.assertIn("M1_NEW", f.review_exclusion_closure(reader(data), base + "deltas/D3/subject.json"))

    def test_lineage_reference_without_preparation_owner_fails_closed(self):
        data = {"epics/SYN/deltas/D1/subject.json": dump({"review_type": "EPIC_PREPARATION_REVIEW",
                                                          "implementer": "A1", "ref": "epics/OTHER/x.md"})}
        with self.assertRaisesRegex(f.Invalid, "owning subject"):
            f.review_exclusion_closure(reader(data), "epics/SYN/deltas/D1/subject.json")
        data["epics/OTHER/subject.json"] = dump({"review_type": "FEATURE_ACCEPTANCE_REVIEW", "implementer": "F"})
        with self.assertRaisesRegex(f.Invalid, "owner type"):
            f.review_exclusion_closure(reader(data), "epics/SYN/deltas/D1/subject.json")

    def test_removing_any_derived_identity_fails_integrity_and_check(self):
        subject = f.parse(self.data[f.EPIC_CORR2_SUBJECT])
        binding = f.parse(self.data[f.EPIC_CORR2_BINDING])
        for identity in sorted(EXPECTED_LINEAGE):
            with self.subTest(identity=identity):
                data = dict(self.data)
                kept = [v for v in subject["review_excluded_identities"] if v != identity]
                data[f.EPIC_CORR2_SUBJECT] = dump(dict(subject, review_excluded_identities=kept))
                data[f.EPIC_CORR2_BINDING] = dump(dict(binding, review_excluded_identities=kept))
                with self.assertRaisesRegex(f.Invalid, "closure incomplete"):
                    f.epic_correction2_integrity(reader(data))

    def test_exclusion_set_shape_and_binding_consistency(self):
        subject = f.parse(self.data[f.EPIC_CORR2_SUBJECT])
        excluded = subject["review_excluded_identities"]
        for changed in (excluded + [excluded[0].lower()], excluded + [" PADDED "], excluded + [""], "NOT_A_LIST"):
            with self.subTest(changed=changed):
                data = dict(self.data)
                data[f.EPIC_CORR2_SUBJECT] = dump(dict(subject, review_excluded_identities=changed))
                with self.assertRaises(f.Invalid):
                    f.epic_correction2_integrity(reader(data))
        data = dict(self.data)
        data[f.EPIC_CORR2_BINDING] = dump(dict(f.parse(self.data[f.EPIC_CORR2_BINDING]),
                                               review_excluded_identities=excluded[1:]))
        with self.assertRaisesRegex(f.Invalid, "binding exclusions"):
            f.epic_correction2_integrity(reader(data))
        # A superset beyond the derived lineage is allowed; no cardinality is fixed.
        data = dict(self.data)
        wider = excluded + ["CODING_AGENT_ADDITIONAL_SYNTHETIC"]
        data[f.EPIC_CORR2_SUBJECT] = dump(dict(subject, review_excluded_identities=wider))
        data[f.EPIC_CORR2_BINDING] = dump(dict(f.parse(self.data[f.EPIC_CORR2_BINDING]),
                                               review_excluded_identities=wider))
        f.epic_correction2_integrity(reader(data))

    def test_materialized_bytes_and_claims_cannot_drift(self):
        f.epic_correction2_integrity(reader(self.data))
        for path in [f.EPIC_CORR2_AUTH, *f.EPIC_CORR_RESULTS, *sorted(f.EPIC_CORR_FILES), *sorted(f.EPIC_DELTA_FILES)]:
            with self.subTest(path=path):
                data = dict(self.data)
                data[path] = self.data[path] + b"\n"
                with self.assertRaises(f.Invalid):
                    f.epic_correction2_integrity(reader(data))
        subject = f.parse(self.data[f.EPIC_CORR2_SUBJECT])
        for key, value in {"status": "READY_FOR_AGENT", "ready_for_agent": True,
                           "implementer": "PROJECT_LLM_WS_E01_EP_DELTA_20260929_03",
                           "superseded_subject": dict(subject["superseded_subject"], end_sha=f.EPIC_DELTA_REVIEWED),
                           "extra": True}.items():
            with self.subTest(key=key):
                data = dict(self.data)
                data[f.EPIC_CORR2_SUBJECT] = dump(dict(subject, **{key: value}))
                with self.assertRaises(f.Invalid):
                    f.epic_correction2_integrity(reader(data))
        binding = f.parse(self.data[f.EPIC_CORR2_BINDING])
        for changes in ({"status": "READY_FOR_AGENT"}, {"ready_for_agent": True},
                        {"epic_preparation_review_result_reference": "reviews/results/X.json"}):
            with self.subTest(changes=changes):
                data = dict(self.data)
                data[f.EPIC_CORR2_BINDING] = dump(dict(binding, **changes))
                with self.assertRaisesRegex(f.Invalid, "pending"):
                    f.epic_correction2_integrity(reader(data))

    def test_scope_allows_only_the_exact_second_correction_files(self):
        for name in f.EPIC_CORR2_FILES:
            f.scope(name)
        for name in (OTHER, f.EPIC_CORR2_DIR + "extra.md", f.EPIC_CORR2_DIR + "correction.md"):
            with self.subTest(name=name), self.assertRaises(f.Invalid):
                f.scope(name)

    def test_check_requires_second_correction_ci_request(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for path, data in self.data.items():
                (root / path).parent.mkdir(parents=True, exist_ok=True)
                (root / path).write_bytes(data)
            f.check(root)
            workflow = root / ".github/workflows/foundation.yml"
            workflow.write_text(workflow.read_text().replace(" --subject " + f.EPIC_CORR2_SUBJECT, " --subject " + HISTORICAL))
            with self.assertRaisesRegex(f.Invalid, "second epic correction CI"):
                f.check(root)


class LineageHistoryTests(unittest.TestCase):
    """Real Git continuation from the reviewed -03 head."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="windowsafe-synthetic-epic-lineage-")
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name) / "repo"
        subprocess.run(["git", "clone", "--shared", "--no-checkout", str(f.ROOT), str(self.repo)],
                       check=True, capture_output=True)
        self.git("checkout", "--detach", f.EPIC_CORR_REVIEWED)
        self.git("config", "user.name", "Synthetic Fixture")
        self.git("config", "user.email", "synthetic@example.invalid")
        self.git("switch", "-c", "synthetic-epic-lineage")
        for name in f.EPIC_CORR2_ALLOWED:
            target = self.repo / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(SOURCE / name, target)
        self.first = self.save()
        patcher = patch.object(f, "ROOT", self.repo)
        patcher.start()
        self.addCleanup(patcher.stop)

    def git(self, *args):
        return subprocess.check_output(["git", "-C", str(self.repo), *args],
                                       stderr=subprocess.PIPE).decode().strip()

    def save(self, amend=False):
        self.git("add", "--all")  # Only the disposable synthetic fixture.
        self.git("-c", "commit.gpgsign=false", "commit", *(["--amend"] if amend else []), "-m", "synthetic lineage")
        return self.git("rev-parse", "HEAD")

    def edit(self, path, data, amend=False):
        (self.repo / path).parent.mkdir(parents=True, exist_ok=True)
        (self.repo / path).write_bytes(data)
        return self.save(amend)

    def result(self, req, identity, review_id="WS-E01-EPR-DELTA-SYNTHETIC"):
        return {
            "schema_version": 3, "review_id": review_id, "review_type": req["review_type"],
            "reviewer": {"authority": req["required_authority"], "identity": identity,
                         "run_reference": "synthetic fixture", "independence": "FRESH_OR_SUFFICIENTLY_ISOLATED"},
            "provenance": {"source_reference": "synthetic fixture", "transport": "EXACT_AUTHORIZED_TRANSFER"},
            "subject": req["subject"], "verdict": "PASS", "findings": [],
            "reviewed_evidence": req["reviewed_evidence"],
            "result_reference": "reviews/results/" + review_id + ".json",
        }

    def verdict(self, req, identity, review_id="WS-E01-EPR-DELTA-SYNTHETIC"):
        f.validate_result(self.result(req, identity, review_id), req,
                          f.parse(f.at(req["subject"]["end_sha"], f.CONTRACT_PATH)), review_id + ".json")

    def sidecar(self, req, identity):
        result = self.result(req, identity)
        record = {"result_sha256": "a" * 64, "subject": result["subject"],
                  "reviewed_evidence": result["reviewed_evidence"], "original_provenance": result["provenance"],
                  "reviewer": result["reviewer"], "provenance": result["provenance"], "decisions": []}
        f.validate_semantic_disposition(record, result, req, [], "a" * 64)

    def test_request_transports_the_closed_exclusion_set(self):
        req = f.request(self.first, f.EPIC_CORR2_SUBJECT)
        self.assertEqual({"id": f.EPIC_CORR2_ID, "path": f.EPIC_CORR2_SUBJECT, "end_sha": self.first}, req["subject"])
        self.assertLessEqual(EXPECTED_LINEAGE, set(req["review_excluded_identities"]))
        self.assertEqual("PROJECT_LLM_WS_E01_EP_DELTA_20260929_04", req["implementer"])
        self.assertIn("foundation/architecture.md", {e["path"] for e in req["reviewed_evidence"]})

    def test_every_lineage_identity_rejected_including_variants(self):
        req = f.request(self.first, f.EPIC_CORR2_SUBJECT)
        for identity in sorted(EXPECTED_LINEAGE):
            for variant in (identity, identity.lower(), "\t" + identity.title() + "  "):
                with self.subTest(identity=variant):
                    with self.assertRaisesRegex(f.Invalid, "self verdict"):
                        self.verdict(req, variant)
                    with self.assertRaisesRegex(f.Invalid, "semantic self"):
                        self.sidecar(req, variant)

    def test_longer_identities_containing_excluded_names_remain_valid(self):
        req = f.request(self.first, f.EPIC_CORR2_SUBJECT)
        for identity in ("INDEPENDENT_EPIC_REREVIEWER_SYNTHETIC",
                         "Reviewer, weder " + " noch ".join(sorted(EXPECTED_LINEAGE)),
                         "PROJECT_LLM_WS_E01_EP_DELTA_20260929_04_REVIEWER"):
            self.verdict(req, identity)
            self.sidecar(req, identity)
        # Cardinality-free history: several distinct legitimate results for one subject validate.
        for review_id in ("WS-E01-EPR-DELTA-SYN-A", "WS-E01-EPR-DELTA-SYN-B", "WS-E01-EPR-DELTA-SYN-C"):
            self.verdict(req, "INDEPENDENT_" + review_id, review_id)

    def test_request_fails_when_a_derived_identity_is_missing(self):
        for identity in sorted(EXPECTED_LINEAGE):
            with self.subTest(identity=identity):
                self.git("checkout", "--detach", self.first)
                for path in (f.EPIC_CORR2_SUBJECT, f.EPIC_CORR2_BINDING):
                    value = f.parse((self.repo / path).read_bytes())
                    value["review_excluded_identities"] = [v for v in value["review_excluded_identities"] if v != identity]
                    (self.repo / path).write_bytes(dump(value))
                head = self.save(amend=True)
                with self.assertRaisesRegex(f.Invalid, "closure incomplete"):
                    f.request(head, f.EPIC_CORR2_SUBJECT)

    def test_old_requests_reproducible_and_namespaces_unchanged(self):
        self.assertEqual(f.request(f.EPIC_CORR_REVIEWED, f.EPIC_CORR_SUBJECT), f.request(self.first, f.EPIC_CORR_SUBJECT))
        self.assertEqual(f.request(f.EPIC_DELTA_REVIEWED, f.EPIC_DELTA_SUBJECT), f.request(self.first, f.EPIC_DELTA_SUBJECT))
        self.assertEqual(f.request(f.EPIC_DELTA_BASE, HISTORICAL), f.request(self.first, HISTORICAL))
        self.assertEqual(45, len(f.request(self.first, f.EPIC_CORR_SUBJECT)["reviewed_evidence"]))
        for name in f.EPIC_DELTA_FILES | f.EPIC_CORR_FILES:
            self.assertEqual(f.at(f.EPIC_CORR_REVIEWED, name), f.at(self.first, name))

    def test_check_history_and_cli_gates(self):
        f.check(self.repo)
        for base in ("0" * 40, f.EPIC_DELTA_BASE, f.EPIC_CORR_REVIEWED):
            f.history(base)
        for args in (["request", "--sha", "HEAD", "--subject", f.EPIC_CORR2_SUBJECT],
                     ["request", "--sha", "HEAD", "--subject", f.EPIC_CORR_SUBJECT],
                     *(["validate-result", "--file", path] for path in f.EPIC_CORR_RESULTS),
                     ["schema-preflight", "--sha", "HEAD", "--schema", f.CONTRACT_PATH],
                     ["history", "--base", f.EPIC_CORR_REVIEWED]):
            with self.subTest(args=args):
                result = subprocess.run([sys.executable, "tools/foundation.py", *args], cwd=self.repo,
                                        capture_output=True, text=True)
                self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_previous_namespaces_append_only_even_when_reverted(self):
        for path in sorted(f.EPIC_CORR_FILES) + [f.EPIC_DELTA_RESULT, f.EPIC_DELTA_SUBJECT]:
            with self.subTest(path=path):
                self.git("checkout", "--detach", self.first)
                original = (self.repo / path).read_bytes()
                self.edit(path, original + b"\n")
                self.edit(path, original)
                with self.assertRaisesRegex(f.Invalid, "scope|append-only"):
                    f.request(self.git("rev-parse", "HEAD"), f.EPIC_CORR2_SUBJECT)

    def test_other_delta_path_merge_and_missing_ancestry_rejected(self):
        self.edit(OTHER, (self.repo / f.EPIC_CORR2_SUBJECT).read_bytes())
        with self.assertRaisesRegex(f.Invalid, "locator"):
            f.request(self.git("rev-parse", "HEAD"), OTHER)
        with self.assertRaisesRegex(f.Invalid, "scope"):
            f.request(self.git("rev-parse", "HEAD"), f.EPIC_CORR2_SUBJECT)
        self.git("checkout", "--detach", self.first)
        self.git("switch", "-c", "synthetic-side")
        self.edit("README.md", b"synthetic side\n")
        self.git("checkout", "--detach", self.first)
        self.git("-c", "commit.gpgsign=false", "merge", "--no-ff", "synthetic-side", "-m", "synthetic merge")
        with self.assertRaisesRegex(f.Invalid, "merges prohibited"):
            f.request(self.git("rev-parse", "HEAD"), f.EPIC_CORR2_SUBJECT)
        # Same files directly on the -02 reviewed head: -03's reviewed head is not an ancestor.
        self.git("checkout", "--detach", f.EPIC_DELTA_REVIEWED)
        for name in f.EPIC_CORR_FILES | f.EPIC_CORR2_ALLOWED | {f.EPIC_DELTA_RESULT}:
            target = self.repo / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(SOURCE / name, target)
        head = self.save()
        with self.assertRaises((f.Invalid, subprocess.CalledProcessError)):
            f.request(head, f.EPIC_CORR2_SUBJECT)


if __name__ == "__main__":
    unittest.main()
