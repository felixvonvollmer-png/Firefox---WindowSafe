"""Pure helpers of the F01 closure instrument; no browser, synthetic report rows only."""

from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "qualification/ws-e01-f01"))
import closure_probe as c
import calibration_probe as cal

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


class MeasurementConditionTests(unittest.TestCase):
    """The method's peak condition: minimize immediately before the high-water reset."""

    def source(self, name):
        return (Path(__file__).resolve().parents[1] / "qualification/ws-e01-f01" / name).read_text()

    def test_closure_pulse_minimizes_immediately_before_reset(self):
        lines = [l.strip() for l in self.source("closure_probe.py").splitlines() if l.strip()]
        resets = [i for i, l in enumerate(lines) if l.startswith("reset_high_water(ext_pid); hwm_reset")]
        self.assertEqual(1, len(resets))
        self.assertTrue(lines[resets[0] - 1].startswith("minimize()"), lines[resets[0] - 1])

    def test_calibration_with_minimize_trial_minimizes_before_reset(self):
        text = self.source("calibration_probe.py")
        block = text[text.index("for kind in order:"):text.index("trials.append(")]
        self.assertIn("if kind == 'with-minimize':\n                        minimize()", block)
        self.assertLess(block.index("if kind == 'with-minimize'"), block.index("reset_high_water(ext)"))


def run(name, l10=1.0, **overrides):
    interval = {"cgroup_cpu_pct_one_core": l10, "other_host_max_window_pct_all_cores": 1.0,
                "driver": {"scheduled": 1000, "delivered": 1000, "failed": 0, "late": 0}}
    interval.update(overrides.pop("interval", {}))
    record = {"run": name, "status": "COMPLETED", "intervals": {"L10": interval}}
    record.update(overrides)
    return record


class CalibrationSummaryTests(unittest.TestCase):
    """METHOD-01 invalidity rules of the A/A calibration summary."""

    def summary(self, a, b):
        return cal.summarize([a, b], 5.0)["L10"]

    def test_valid_pair_difference(self):
        out = self.summary(run("a", 25.0), run("b", 25.5))
        self.assertEqual([0.5], out["valid_pair_diffs_pct_one_core"])
        self.assertEqual([], out["invalid"])

    def test_each_invalidity_rule_rejects_the_pair(self):
        cases = {
            "driver error": {"interval": {"driver": {"error": "boom"}}},
            "lost workload events": {"interval": {"driver": {"scheduled": 1000, "delivered": 999, "failed": 0, "late": 0}}},
            "late workload events": {"interval": {"driver": {"scheduled": 1000, "delivered": 1000, "failed": 0, "late": 2}}},
            "foreign host load": {"interval": {"other_host_max_window_pct_all_cores": 6.0}},
            "realize_mismatch": {"realize_mismatch": True},
            "adopt_mismatch": {"adopt_mismatch": True},
            "not_quiescent": {"not_quiescent": True},
            "run status FAILED": {"status": "FAILED"},
        }
        for reason, overrides in cases.items():
            with self.subTest(reason=reason):
                out = self.summary(run("a"), run("b", **overrides))
                self.assertEqual([], out["valid_pair_diffs_pct_one_core"])
                self.assertIn(reason, out["invalid"][0]["reasons"]["b"])

    def test_failed_run_without_intervals_is_listed_not_dropped(self):
        failed = {"run": "b", "status": "FAILED", "intervals": {}}
        out = self.summary(run("a"), failed)
        self.assertEqual(1, len(out["invalid"]))
        self.assertIsNone(out["invalid"][0]["diff"])

    def test_late_tolerance_boundary(self):
        ok = run("b", interval={"driver": {"scheduled": 1000, "delivered": 1000, "failed": 0, "late": 1}})
        self.assertEqual(1, len(self.summary(run("a"), ok)["valid_pair_diffs_pct_one_core"]))


if __name__ == "__main__":
    unittest.main()
