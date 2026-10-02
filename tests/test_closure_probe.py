"""Pure helpers of the F01 closure instrument; no browser, synthetic report rows only."""

from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "qualification/ws-e01-f01"))
import closure_probe as c

ROWS = [
    {"process": "extension (pid 42)", "path": "explicit/js-non-window/zones/zone(0x1)/strings/x", "units": 0, "amount": 100},
    {"process": "extension (pid 42)", "path": "explicit/js-non-window/realm(moz-extension://abc/driver.html)/objects", "units": 0, "amount": 30},
    {"process": "extension (pid 42)", "path": "explicit/window-objects/top(moz-extension://abc/driver.html)/dom/x", "units": 0, "amount": 7},
    {"process": "extension (pid 42)", "path": "resident", "units": 0, "amount": 999999},
    {"process": "extension (pid 42)", "path": "explicit/js-non-window/count", "units": 1, "amount": 5},
    {"process": "", "path": "explicit/dom/indexedDB/memory", "units": 0, "amount": 11},
    {"process": "webIsolated (pid 7)", "path": "explicit/storage/sqlite/x", "units": 0, "amount": 13},
    {"process": "extension (pid 420)", "path": "explicit/js-non-window/other", "units": 0, "amount": 1000},
]


class ClosureHelperTests(unittest.TestCase):

    def test_origin_explicit_counts_only_explicit_byte_leaves_of_the_origin(self):
        groups = c.origin_explicit(ROWS, "abc")
        self.assertEqual({"js": 30, "dom": 7, "total": 37}, groups)

    def test_process_explicit_is_exact_pid_and_explicit_bytes_only(self):
        total = c.process_explicit(ROWS, 42)
        self.assertEqual((137, 100, 130), (total["total"], total["strings"], total["js"]))
        self.assertEqual(["extension (pid 42)"], total["process_names"])

    def test_storage_bucket_spans_all_processes(self):
        self.assertEqual(24, c.storage_rows(ROWS))

    def test_status_parsing_and_missing_field(self):
        with tempfile.TemporaryDirectory() as temp:
            status = Path(temp, "1", "status"); status.parent.mkdir()
            status.write_text("Name:\tx\nVmHWM:\t  1234 kB\nVmRSS:\t   99 kB\n")
            real = Path
            with patch.object(c, "Path", lambda *parts: real(temp, *parts[1:]) if parts[0] == "/proc" else real(*parts)):
                self.assertEqual(1234, c.status_kib(1, "VmHWM"))
                self.assertEqual(99, c.status_kib(1, "VmRSS"))
                with self.assertRaises(RuntimeError):
                    c.status_kib(1, "VmPeak")


if __name__ == "__main__":
    unittest.main()
