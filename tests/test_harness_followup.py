"""Versioned review and real CLI history regressions; synthetic local Git only."""

import copy
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import foundation as f
import reviewer_environment as env


BASE = "4ba2c473fe4d90c85d94ee2b2f5cc5777d115109"
START = "9b6dd621deec1193bfdfbdfa730e8f9349c73fd6"
PRIOR_TRANSFER = "48224840e68da6c66c0f129f0564fcaad9c1ad8e"


class LegacySemanticTests(unittest.TestCase):
    def setUp(self):
        self.contracts = [f.parse(f.at(sha, f.CONTRACT_PATH)) for sha in (BASE, START)]
        self.contracts.append(f.parse((f.ROOT / f.CONTRACT_PATH).read_bytes()))
        self.req = f.request(BASE)
        self.result = f.parse((f.ROOT / "reviews/results/WS-PFR-20260917-01.json").read_bytes())

    def validate(self, contract, sidecar=None, raw_sha=None):
        self.result["schema_version"] = contract["contract_version"]
        f.validate_result(self.result, self.req, contract, self.result["review_id"] + ".json", sidecar, raw_sha)

    def test_markerless_v1_positive_all_types_verdicts_but_not_v2_v3(self):
        for kind, authority in f.AUTHORITIES.items():
            self.req["review_type"] = self.result["review_type"] = kind
            self.req["required_authority"] = self.result["reviewer"]["authority"] = authority
            for verdict in ("PASS", "BLOCKED", "CORRECTION_REQUIRED"):
                self.result["verdict"] = verdict
                self.result["findings"][0]["disposition"] = f.LEGACY_POSITIVE
                self.validate(self.contracts[0])
                for contract in self.contracts[1:]:
                    with self.assertRaises(f.Invalid):
                        self.validate(contract)

    def test_unclear_v1_is_semantic_gate_not_v2_syntax(self):
        self.result["findings"][0]["disposition"] = "Needs a separately reasoned disposition"
        with self.assertRaises(f.SemanticDispositionRequired):
            self.validate(self.contracts[0])
        for contract in self.contracts[1:]:
            with self.assertRaises(f.Invalid) as caught:
                self.validate(contract)
            self.assertNotIsInstance(caught.exception, f.SemanticDispositionRequired)

    def sidecar(self):
        self.result["findings"][0]["disposition"] = "Legacy prose requiring independent interpretation"
        raw_sha = f.sha256(json.dumps(self.result).encode())
        record = {
            "result_sha256": raw_sha, "subject": copy.deepcopy(self.result["subject"]),
            "reviewed_evidence": copy.deepcopy(self.result["reviewed_evidence"]),
            "original_provenance": copy.deepcopy(self.result["provenance"]),
            "reviewer": copy.deepcopy(self.result["reviewer"]),
            "provenance": {"source_reference": "SYNTHETIC_SEMANTIC_REVIEW_ONLY", "transport": "EXACT_AUTHORIZED_TRANSFER"},
            "decisions": [{"finding_id": self.result["findings"][0]["id"],
                           "original_disposition_sha256": f.sha256(self.result["findings"][0]["disposition"].encode()),
                           "decision": "NONBLOCKING_FOLLOW_UP", "rationale": "Synthetic rationale",
                           "follow_up": "Synthetic tracked task", "trigger": "Next independent review"}],
        }
        return record, raw_sha

    def test_bound_independent_semantic_record_and_binding_failures(self):
        record, digest = self.sidecar()
        self.validate(self.contracts[0], record, digest)
        mutations = [
            lambda r: r.update(result_sha256="0" * 64),
            lambda r: r["subject"].update(end_sha="0" * 40),
            lambda r: r["reviewed_evidence"][0].update(sha256="0" * 64),
            lambda r: r["original_provenance"].update(source_reference="wrong source"),
            lambda r: r["reviewer"].update(authority="CODING_AGENT"),
            lambda r: r["reviewer"].update(identity=self.req["implementer"]),
            lambda r: r["reviewer"].update(independence="SAME_CONTEXT"),
            lambda r: r["reviewer"].update(run_reference=""),
            lambda r: r["provenance"].update(source_reference=""),
            lambda r: r["decisions"][0].update(original_disposition_sha256="0" * 64),
            lambda r: r["decisions"][0].update(finding_id="WRONG"),
            lambda r: r["decisions"][0].update(decision="BLOCKING"),
            lambda r: r["decisions"][0].update(trigger=" "),
            lambda r: r.update(decisions=[]),
        ]
        for mutation in mutations:
            changed = copy.deepcopy(record)
            mutation(changed)
            with self.assertRaises(f.Invalid):
                self.validate(self.contracts[0], changed, digest)
        with self.assertRaises(f.Invalid):
            self.validate(self.contracts[0], record, None)

    def test_semantic_record_cannot_override_other_gates(self):
        record, digest = self.sidecar()
        for value in ("", " \n", "BLOCKING: must fix first", "EXPLICIT_NONBLOCKING_FOLLOW_UP: BLOCKING: contradiction"):
            self.result["findings"][0]["disposition"] = value
            with self.assertRaises(f.Invalid):
                self.validate(self.contracts[0], record, digest)
        for contract in self.contracts:
            for severity in ("MAJOR", "BLOCKING", "CRITICAL"):
                self.result["findings"][0].update(severity=severity, disposition=f.NONBLOCKING_PREFIX + "still blocking")
                with self.assertRaises(f.Invalid):
                    self.validate(contract)

    def test_exact_historical_results_contracts_and_version_pairing(self):
        for name, digest in (("WS-PFR-20260917-01", "c4c908eb70c99252f185ee89d077919ecc9598cc2842b2f0b1209734f115c19f"),
                             ("WS-PFR-20260918-01", "0275bfcbad98bd727b861bd5b972af635139cc0986ef99eed1965331eda5f6b2")):
            path = f.ROOT / "reviews/results" / (name + ".json")
            self.assertEqual(digest, f.sha256(path.read_bytes()))
            f.validate_result_file(path)
        for a in self.contracts:
            for b in self.contracts:
                if a == b:
                    f.schema_preflight(a, b)
                else:
                    with self.assertRaises(f.Invalid):
                        f.schema_preflight(a, b)

    def test_original_subject_evidence_authority_still_gate_v1_positive(self):
        self.result["findings"][0]["disposition"] = f.LEGACY_POSITIVE
        original = copy.deepcopy(self.result)
        for mutation in (lambda r: r["subject"].update(id="WRONG"),
                         lambda r: r["reviewed_evidence"][0].update(sha256="0" * 64),
                         lambda r: r["reviewer"].update(authority="CODING_AGENT")):
            self.result = copy.deepcopy(original)
            mutation(self.result)
            with self.assertRaises(f.Invalid):
                self.validate(self.contracts[0])

    def test_marker_matrix_including_historical_v2_all_types_and_verdicts(self):
        for contract in self.contracts:
            for kind, authority in f.AUTHORITIES.items():
                self.req["review_type"] = self.result["review_type"] = kind
                self.req["required_authority"] = self.result["reviewer"]["authority"] = authority
                for verdict in contract["verdicts"]:
                    self.result["verdict"] = verdict
                    for value in ("", " \n", "later", "BLOCKING: must fix", f.NONBLOCKING_PREFIX,
                                  f.NONBLOCKING_PREFIX + "NONBLOCKING: duplicate"):
                        self.result["findings"][0]["disposition"] = value
                        with self.assertRaises(f.Invalid):
                            self.validate(contract)
                    self.result["findings"][0]["disposition"] = f.NONBLOCKING_PREFIX + "tracked follow-up with trigger"
                    self.validate(contract)

    def test_cli_unclear_request_bound_sidecar_and_exact_byte_tampering(self):
        record, digest = self.sidecar()
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            result_path = directory / (self.result["review_id"] + ".json")
            result_path.write_bytes(json.dumps(self.result).encode())
            sidecar_path = directory / "synthetic-disposition.json"
            sidecar_path.write_text(json.dumps(record))
            argv = [sys.executable, str(f.ROOT / "tools/foundation.py"), "validate-result", "--file", str(result_path)]
            pending = subprocess.run(argv, capture_output=True, text=True)
            self.assertEqual(1, pending.returncode)
            unresolved = json.loads(pending.stdout)
            self.assertEqual("V1_SEMANTIC_DISPOSITION_REQUIRED", unresolved["status"])
            self.assertEqual(digest, unresolved["result_sha256"])
            self.assertEqual(self.result["provenance"], unresolved["original_provenance"])
            argv += ["--semantic-disposition", str(sidecar_path)]
            accepted = subprocess.run(argv, capture_output=True, text=True)
            self.assertEqual(0, accepted.returncode, accepted.stderr)
            result_path.write_bytes(result_path.read_bytes() + b"\n")
            changed = subprocess.run(argv, capture_output=True, text=True)
            self.assertEqual(1, changed.returncode)


class HistoryCliTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="windowsafe-synthetic-history-")
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name) / "repo"
        subprocess.run(["git", "clone", "--shared", "--no-checkout", str(f.ROOT), str(self.repo)], check=True, capture_output=True)
        self.git("checkout", "--detach", START)
        self.git("config", "user.name", "Synthetic Fixture")
        self.git("config", "user.email", "synthetic@example.invalid")
        for name in ("tools/foundation.py", f.FOLLOWUP_AUTH, "foundation/subject.json"):
            shutil.copyfile(f.ROOT / name, self.repo / name)
        self.first = self.save()

    def git(self, *args):
        return subprocess.check_output(["git", "-C", str(self.repo), *args], stderr=subprocess.PIPE).decode().strip()

    def save(self):
        self.git("add", "--all")  # Only this disposable synthetic fixture.
        self.git("commit", "-m", "synthetic history test")
        return self.git("rev-parse", "HEAD")

    def cli(self, base="0" * 40, ok=False):
        result = subprocess.run([sys.executable, "tools/foundation.py", "history", "--event-base"], cwd=self.repo,
                                env=dict(os.environ, FOUNDATION_EVENT_BASE=base), capture_output=True, text=True)
        self.assertEqual(0 if ok else 1, result.returncode, result.stdout + result.stderr)

    def subject(self, **changes):
        path = self.repo / "foundation/subject.json"
        data = json.loads(path.read_text())
        data.update(changes)
        path.write_text(json.dumps(data) + "\n")
        self.save()

    def test_valid_zero_pr_previous_push_and_additive_history(self):
        self.cli(ok=True)
        self.cli(BASE, ok=True)
        self.cli(START, ok=True)
        for i in range(4):
            (self.repo / f"reviews/results/SYNTHETIC-{i}.json").write_text('{"synthetic_history_only": true}\n')
            previous = self.git("rev-parse", "HEAD")
            self.save()
            self.cli(previous, ok=True)
            self.cli(ok=True)

    def test_self_and_unapproved_ancestor_event_bases_rejected(self):
        self.cli(self.first)
        self.cli(PRIOR_TRANSFER)
        self.cli("")
        self.cli("HEAD")
        self.cli("f" * 40)

    def test_subject_cannot_select_head_or_later_ancestor(self):
        for value in ("HEAD", self.first, START):
            self.subject(start_baseline_sha=value, cumulative_review_and_history_base_sha=value)
            self.cli()

    def test_missing_or_changed_authorization_and_digest_rejected(self):
        path = self.repo / f.FOLLOWUP_AUTH
        original = path.read_bytes()
        path.unlink()
        self.save()
        self.cli()
        altered = json.loads(original)
        altered["repository_binding"]["cumulative_review_and_history_base_sha"] = self.first
        path.write_text(json.dumps(altered) + "\n")
        self.subject(execution_authorization_sha256=f.sha256(path.read_bytes()), start_baseline_sha=self.first,
                     cumulative_review_and_history_base_sha=self.first)
        self.cli()

    def test_run_binding_and_uncommitted_subject_rejected(self):
        self.subject(run_start_head_sha=BASE)
        self.cli()
        self.subject(run_start_head_sha=START)
        path = self.repo / "foundation/subject.json"
        path.write_bytes(path.read_bytes() + b"\n")
        self.cli()

    def test_changed_deleted_protected_bytes_cannot_hide_behind_later_base(self):
        for name in ("foundation/sources/foundation-1.md", "reviews/results/WS-PFR-20260917-01.json"):
            path = self.repo / name
            data = path.read_bytes()
            path.write_bytes(data + b"\n")
            tampered = self.save()
            (self.repo / "README.md").write_text("synthetic later commit\n" + name)
            self.save()
            self.cli(tampered)
            self.cli()
            path.unlink()
            self.save()
            self.cli()
            path.write_bytes(data)
            self.save()
        self.cli()  # Reverting bytes cannot erase the intervening append-only violation.

    def test_full_history_and_writer_source_preserved(self):
        current = (f.ROOT / "tools/foundation.py").read_text()
        previous = f.at(START, "tools/foundation.py").decode()
        for source in (current, previous):
            self.assertIn("def write_inventory", source)
        self.assertEqual(previous.split("def write_inventory", 1)[1].split("\ndef protected", 1)[0],
                         current.split("def write_inventory", 1)[1].split("\ndef protected", 1)[0])
        self.assertEqual(f.at(START, "tests/test_harness_correction.py"), (f.ROOT / "tests/test_harness_correction.py").read_bytes())

    def test_result_introduced_inside_delta_cannot_be_rewritten(self):
        path = self.repo / "reviews/results/SYNTHETIC-ADDED.json"
        path.write_bytes(b'{"synthetic": "original"}\n')
        self.save()
        path.write_bytes(b'{"synthetic": "rewritten"}\n')
        self.save()
        self.cli()

    def test_actual_cli_root_bootstrap_without_authorization(self):
        root = Path(self.temp.name) / "root-bootstrap"
        (root / "tools").mkdir(parents=True)
        shutil.copyfile(f.ROOT / "tools/foundation.py", root / "tools/foundation.py")
        subprocess.run(["git", "init", "--initial-branch=synthetic", str(root)], check=True, capture_output=True)
        subprocess.run(["git", "-C", str(root), "add", "tools/foundation.py"], check=True, capture_output=True)
        subprocess.run(["git", "-C", str(root), "-c", "user.name=Synthetic", "-c", "user.email=synthetic@example.invalid",
                        "-c", "commit.gpgsign=false", "commit", "-m", "synthetic root"], check=True, capture_output=True)
        result = subprocess.run([sys.executable, "tools/foundation.py", "history", "--event-base"], cwd=root,
                                env=dict(os.environ, FOUNDATION_EVENT_BASE="0" * 40), capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stderr)


class EnvironmentGuardTests(unittest.TestCase):
    def test_wrong_runtime_never_creates_destination(self):
        with tempfile.TemporaryDirectory() as parent:
            target = Path(parent) / "must-not-exist"
            with patch.object(sys, "version_info", (3, 13, 0)), self.assertRaises(ValueError):
                env.prepare(target, START)
            self.assertFalse(target.exists())

    def test_existing_destination_never_cloned_or_overwritten(self):
        with tempfile.TemporaryDirectory() as parent:
            target = Path(parent)
            sentinel = target / "sentinel"
            sentinel.write_bytes(b"synthetic")
            with patch.object(subprocess, "run") as run, self.assertRaises(FileExistsError):
                env.prepare(target, START)
            run.assert_not_called()
            self.assertEqual(b"synthetic", sentinel.read_bytes())


if __name__ == "__main__":
    unittest.main()
