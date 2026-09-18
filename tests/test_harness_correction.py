"""WS-HC regression evidence using only isolated synthetic filesystem objects."""

import copy
from contextlib import contextmanager
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import foundation as f


BASE = "4ba2c473fe4d90c85d94ee2b2f5cc5777d115109"
PAYLOAD = "reviews/results/WS-PFR-20260917-01.json"


@contextmanager
def intercept_open(callback):
    """Keep the declared dir_fd capability when substituting a syscall in a test."""
    original = os.open
    supported = os.supports_dir_fd
    with patch.object(os, "open", side_effect=lambda *a, **k: callback(original, *a, **k)) as mocked:
        with patch.object(os, "supports_dir_fd", supported | {mocked}):
            yield


class OutputWriterTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.parent = Path(self.temp.name)
        self.root = self.parent / "synthetic-repo"
        self.root.mkdir()
        (self.root / "README.md").write_text("synthetic\n")
        self.build = self.root / "build"
        self.leaf = self.build / "foundation-inventory.json"
        self.outside = self.parent / "synthetic-outside"

    def test_repeated_build_deterministic_and_shorter_output(self):
        data = f.build_bytes(self.root)
        f.write_inventory(self.root, data)
        self.assertEqual(data, self.leaf.read_bytes())
        self.assertEqual(data, f.build_bytes(self.root))
        f.write_inventory(self.root, data)
        self.assertEqual(data, self.leaf.read_bytes())
        f.write_inventory(self.root, b"{}\n")
        self.assertEqual(b"{}\n", self.leaf.read_bytes())

    def test_existing_leaf_symlink_preserves_outside_target_and_link(self):
        self.build.mkdir()
        self.outside.write_bytes(b"synthetic sentinel")
        self.leaf.symlink_to(self.outside)
        with self.assertRaises(OSError):
            f.write_inventory(self.root, b"forbidden")
        self.assertEqual(b"synthetic sentinel", self.outside.read_bytes())
        self.assertTrue(self.leaf.is_symlink())

    def test_dangling_leaf_does_not_create_target(self):
        self.build.mkdir()
        self.leaf.symlink_to(self.outside)
        with self.assertRaises(OSError):
            f.write_inventory(self.root, b"forbidden")
        self.assertFalse(self.outside.exists())
        self.assertTrue(self.leaf.is_symlink())

    def test_linked_output_directory_preserved(self):
        self.outside.mkdir()
        sentinel = self.outside / "foundation-inventory.json"
        sentinel.write_bytes(b"synthetic sentinel")
        self.build.symlink_to(self.outside, target_is_directory=True)
        with self.assertRaises(OSError):
            f.write_inventory(self.root, b"forbidden")
        self.assertEqual(b"synthetic sentinel", sentinel.read_bytes())
        self.assertTrue(self.build.is_symlink())

    def test_wrong_directory_and_leaf_types(self):
        self.build.write_bytes(b"not a directory")
        with self.assertRaises(OSError):
            f.write_inventory(self.root, b"forbidden")
        self.assertEqual(b"not a directory", self.build.read_bytes())
        self.build.unlink()  # Synthetic fixture cleanup, not writer behavior.
        self.leaf.mkdir(parents=True)
        with self.assertRaises(OSError):
            f.write_inventory(self.root, b"forbidden")
        self.assertTrue(self.leaf.is_dir())

    def test_fifo_rejected_without_waiting_or_removing(self):
        self.build.mkdir()
        os.mkfifo(self.leaf)
        with self.assertRaises((OSError, f.Invalid)):
            f.write_inventory(self.root, b"forbidden")
        self.assertTrue(self.leaf.exists())

    def test_hardlink_rejected_before_truncation(self):
        self.build.mkdir()
        self.outside.write_bytes(b"synthetic sentinel")
        os.link(self.outside, self.leaf)
        with self.assertRaises(f.Invalid):
            f.write_inventory(self.root, b"forbidden")
        self.assertEqual(b"synthetic sentinel", self.outside.read_bytes())

    def test_leaf_swap_at_open_rejected(self):
        self.build.mkdir()
        self.leaf.write_bytes(b"old synthetic output")
        self.outside.write_bytes(b"synthetic sentinel")
        def replace_before_open(original, path, *args, **kwargs):
            if path == "foundation-inventory.json":
                self.leaf.unlink()
                self.leaf.symlink_to(self.outside)
            return original(path, *args, **kwargs)
        with intercept_open(replace_before_open), self.assertRaises(OSError):
            f.write_inventory(self.root, b"forbidden")
        self.assertEqual(b"synthetic sentinel", self.outside.read_bytes())
        self.assertTrue(self.leaf.is_symlink())

    def test_directory_swap_before_open_rejected(self):
        self.build.mkdir()
        self.outside.mkdir()
        def replace_before_open(original, path, *args, **kwargs):
            if path == "build":
                self.build.rename(self.root / "original-build")
                self.build.symlink_to(self.outside, target_is_directory=True)
            return original(path, *args, **kwargs)
        with intercept_open(replace_before_open), self.assertRaises(OSError):
            f.write_inventory(self.root, b"forbidden")
        self.assertFalse((self.outside / "foundation-inventory.json").exists())
        self.assertTrue(self.build.is_symlink())

    def test_directory_swap_after_open_cannot_redirect_write(self):
        self.build.mkdir()
        self.outside.mkdir()
        def replace_after_directory_open(original, path, *args, **kwargs):
            if path == "foundation-inventory.json":
                self.build.rename(self.root / "original-build")
                self.build.symlink_to(self.outside, target_is_directory=True)
            return original(path, *args, **kwargs)
        with intercept_open(replace_after_directory_open):
            f.write_inventory(self.root, b"anchored synthetic output")
        self.assertFalse((self.outside / "foundation-inventory.json").exists())
        self.assertEqual(b"anchored synthetic output", (self.root / "original-build/foundation-inventory.json").read_bytes())
        self.assertTrue(self.build.is_symlink())

    def test_permission_error_before_truncate_preserves_file(self):
        self.build.mkdir()
        self.leaf.write_bytes(b"old synthetic output")
        def deny_leaf(original, path, *args, **kwargs):
            if path == "foundation-inventory.json":
                raise PermissionError("synthetic denial")
            return original(path, *args, **kwargs)
        with intercept_open(deny_leaf), self.assertRaises(PermissionError):
            f.write_inventory(self.root, b"forbidden")
        self.assertEqual(b"old synthetic output", self.leaf.read_bytes())

    def test_unsupported_environment_fails_before_mutation(self):
        with patch.object(os, "supports_dir_fd", set()), self.assertRaises(f.Invalid):
            f.write_inventory(self.root, b"forbidden")
        self.assertFalse(self.build.exists())

    def test_short_writes_and_io_errors(self):
        original_write = os.write
        with patch.object(os, "write", side_effect=lambda fd, data: original_write(fd, data[:2])):
            f.write_inventory(self.root, b"synthetic data")
        self.assertEqual(b"synthetic data", self.leaf.read_bytes())
        with patch.object(os, "write", return_value=0), self.assertRaises(f.Invalid):
            f.write_inventory(self.root, b"synthetic")
        with patch.object(os, "write", side_effect=OSError("synthetic I/O error")), self.assertRaises(OSError):
            f.write_inventory(self.root, b"synthetic")
        # A failed regenerable build is not reported as success; next build repairs it.
        f.write_inventory(self.root, b"recovered")
        self.assertEqual(b"recovered", self.leaf.read_bytes())


class DispositionCompatibilityTests(unittest.TestCase):
    def setUp(self):
        self.old = f.parse(f.at(BASE, f.CONTRACT_PATH))
        self.current = f.parse((f.ROOT / f.CONTRACT_PATH).read_bytes())
        self.payload = f.parse((f.ROOT / PAYLOAD).read_bytes())
        self.req = f.request(BASE)

    def validate(self, result, req, contract):
        f.validate_result(result, req, contract, result["review_id"] + ".json")

    def test_real_payload_unchanged_and_legacy_consumer(self):
        data = (f.ROOT / PAYLOAD).read_bytes()
        self.assertEqual(10136, len(data))
        self.assertEqual("c4c908eb70c99252f185ee89d077919ecc9598cc2842b2f0b1209734f115c19f", f.sha256(data))
        f.validate_result_file(f.ROOT / PAYLOAD)
        self.assertEqual("PASS", self.payload["verdict"])
        self.assertEqual("OPEN", self.payload["findings"][0]["status"])

    def test_negative_minor_matrix_both_contracts_all_types_and_verdicts(self):
        invalid = ["", " \t\n", "später", "follow-up planned", "nonblocking follow-up",
                   "BLOCKING: Nicht freigeben.", "EXPLICIT_NONBLOCKING_FOLLOW_UP:",
                   "EXPLICIT_NONBLOCKING_FOLLOW_UP: \n\t", "EXPLICIT_NONBLOCKING: reason",
                   " EXPLICIT_NONBLOCKING_FOLLOW_UP: reason", "explicit_nonblocking_follow_up: reason",
                   "EXPLICIT_NONBLOCKING_FOLLOW_UP: BLOCKING: must fix first",
                   "EXPLICIT_NONBLOCKING_FOLLOW_UP: reason; EXPLICIT_NONBLOCKING_FOLLOW_UP: duplicate",
                   "EXPLICIT_NONBLOCKING_FOLLOW_UP: reason; NONBLOCKING: duplicate"]
        for contract in (self.old, self.current):
            for kind, authority in f.AUTHORITIES.items():
                for verdict in contract["verdicts"]:
                    for disposition in invalid:
                        result = copy.deepcopy(self.payload)
                        req = copy.deepcopy(self.req)
                        result["schema_version"] = contract["contract_version"]
                        result["review_type"] = req["review_type"] = kind
                        result["reviewer"]["authority"] = req["required_authority"] = authority
                        result["verdict"] = verdict
                        result["findings"][0]["disposition"] = disposition
                        with self.subTest(version=contract["contract_version"], kind=kind, verdict=verdict, disposition=disposition), self.assertRaises(f.Invalid):
                            self.validate(result, req, contract)

    def test_positive_states_and_blockers_across_types_and_versions(self):
        for contract in (self.old, self.current):
            for kind, authority in f.AUTHORITIES.items():
                result = copy.deepcopy(self.payload)
                req = copy.deepcopy(self.req)
                result["schema_version"] = contract["contract_version"]
                result["review_type"] = req["review_type"] = kind
                result["reviewer"]["authority"] = req["required_authority"] = authority
                self.validate(result, req, contract)
                for severity in ("MAJOR", "BLOCKING", "CRITICAL"):
                    result["findings"][0]["severity"] = severity
                    with self.assertRaises(f.Invalid):
                        self.validate(result, req, contract)
                result["verdict"] = "CORRECTION_REQUIRED"
                self.validate(result, req, contract)
                result["verdict"] = "PASS"
                result["findings"][0].update(status="RESOLVED", disposition="Fixed with evidence")
                self.validate(result, req, contract)
                result["findings"] = []
                self.validate(result, req, contract)

    def test_no_grandfathering_by_old_id_or_subject(self):
        result = copy.deepcopy(self.payload)
        result["findings"][0]["disposition"] = "später"
        with self.assertRaises(f.Invalid):
            self.validate(result, self.req, self.old)

    def test_schema_version_pairing_and_preflight(self):
        for contract in (self.old, self.current):
            f.schema_preflight(contract, copy.deepcopy(contract))
        with self.assertRaises(f.Invalid):
            f.schema_preflight(self.old, self.current)
        with self.assertRaises(f.Invalid):
            self.validate(self.payload, self.req, self.current)
        invalid = copy.deepcopy(self.current)
        invalid["minor_open_disposition"]["prefix"] = "anything: "
        with self.assertRaises(f.Invalid):
            f.schema_preflight(invalid, invalid)

    def test_additive_history_with_real_payload_and_new_reviews(self):
        history = {PAYLOAD: (f.ROOT / PAYLOAD).read_bytes()}
        for i in range(5):
            result = copy.deepcopy(self.payload)
            result["review_id"] = "SYNTHETIC-ADDITIVE-" + str(i)
            result["result_reference"] = "reviews/results/" + result["review_id"] + ".json"
            self.validate(result, self.req, self.old)
            extended = dict(history)
            extended[result["result_reference"]] = json.dumps(result).encode()
            f.check_history_maps(history, extended)
            history = extended
        changed = dict(history)
        changed[PAYLOAD] += b"\n"
        with self.assertRaises(f.Invalid):
            f.check_history_maps(history, changed)


if __name__ == "__main__":
    unittest.main()
