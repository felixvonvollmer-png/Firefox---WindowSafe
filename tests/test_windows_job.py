"""Native fail-closed launcher checks on disposable synthetic children only."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'qualification/ws-e01-f01'))
from windows_job import WindowsJobProcess


@unittest.skipUnless(os.name == 'nt', 'Windows native accounting only')
class WindowsJobTests(unittest.TestCase):
    def launch(self, code, **kwargs):
        proc = WindowsJobProcess([sys.executable, '-c', code], **kwargs)
        self.addCleanup(proc.close)
        return proc

    def test_lifetime_exited_child_cpu_io_and_peak(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = str(Path(tmp) / 'synthetic.bin')
            child = ('import time; from pathlib import Path; '
                     'x=bytearray(32*1024*1024); '
                     f'Path({output!r}).write_bytes(x); '
                     'start=time.process_time(); '
                     '\nwhile time.process_time()-start<0.2: pass')
            code = f'import subprocess,sys; subprocess.run([sys.executable,"-c",{child!r}],check=True)'
            p = self.launch(code)
            self.assertEqual(p.before_resume['active_processes'], 1)
            self.assertEqual(p.wait(30), 0)
            final = p.counters()
            self.assertEqual(final['active_processes'], 0)
            # Windows may also attach its console host to the job.
            self.assertGreaterEqual(final['total_processes'], 2)
            self.assertGreater(final['user_seconds'] + final['kernel_seconds'], .15)
            self.assertGreaterEqual(final['io']['write_bytes'], 32*1024*1024)
            self.assertGreaterEqual(final['peak_job_commit_bytes'], 32*1024*1024)

    def test_breakaway_rejected(self):
        p = self.launch('import subprocess,sys\ntry:\n subprocess.run([sys.executable,"-c","pass"],creationflags=0x1000000)\nexcept OSError as e:\n sys.exit(0 if e.winerror==5 else 2)\nelse:\n sys.exit(3)')
        self.assertEqual(p.wait(20), 0)
        self.assertEqual(p.counters()['active_processes'], 0)

    def test_assignment_failure_never_runs_child(self):
        with tempfile.TemporaryDirectory() as tmp:
            marker = Path(tmp) / 'must-not-exist'
            with self.assertRaises(OSError):
                self.launch(f'from pathlib import Path; Path({str(marker)!r}).touch()', _fail_assignment=True)
            self.assertFalse(marker.exists())

    def test_owned_job_cleanup(self):
        p = self.launch('import time; time.sleep(60)')
        p.terminate()
        self.assertEqual(p.wait(15), 125)
        self.assertEqual(p.counters()['active_processes'], 0)

    def test_protocol_binding_rejects_foreign_pid_and_binary(self):
        p = self.launch('import time; time.sleep(60)')
        self.assertEqual(p.bind_browser(p.pid, sys.executable)['pid'], p.pid)
        with self.assertRaises(ValueError):
            p.bind_browser(os.getpid(), sys.executable)
        with self.assertRaises(ValueError):
            p.bind_browser(p.pid, str(Path(sys.executable).parent/'foreign.exe'))

    def test_nested_job_rolls_up(self):
        source = str(Path(__file__).resolve().parents[1] / 'qualification/ws-e01-f01')
        code = (f'import sys;sys.path.insert(0,{source!r});from windows_job import WindowsJobProcess;'
                'p=WindowsJobProcess([sys.executable,"-c","sum(range(1000000))"]);'
                'assert p.launcher_in_job; assert p.wait(20)==0;p.close()')
        p = self.launch(code)
        self.assertEqual(p.wait(30), 0)
        self.assertGreaterEqual(p.counters()['total_processes'], 2)


if __name__ == '__main__':
    unittest.main()
