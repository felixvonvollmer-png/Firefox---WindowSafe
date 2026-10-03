"""Finite synthetic job-counter/short-pulse qualification, no browser or product."""
import json
from pathlib import Path
import statistics
import sys
import tempfile
import time

from windows_job import WindowsJobProcess


def main():
    root = Path(__file__).resolve().parents[2] / 'build/f01/runs'
    root.mkdir(parents=True, exist_ok=True)
    owned = Path(tempfile.mkdtemp(prefix='job-', dir=root))
    record = {'evidence_class': 'SYNTHETIC_DRY_RUN_MEASUREMENT', 'runs': [],
              'limitation': 'Job commit peak is whole-job, not addon RAM; live PID identities are sampled, not complete exit-event identity evidence.'}
    for size in (0, 64*1024*1024):
        child = ('import time; x=bytearray(' + str(size) + '); '
                 'start=time.process_time();\nwhile time.process_time()-start<0.2: pass\ndel x')
        code = f'import subprocess,sys;subprocess.run([sys.executable,"-c",{child!r}],check=True)'
        proc = WindowsJobProcess([sys.executable, '-c', code])
        try:
            before = proc.before_resume
            proc.wait(30)
            after = proc.counters()
            assert after['active_processes'] == 0 and after['total_processes'] >= 2
            assert after['user_seconds'] + after['kernel_seconds'] >= .15
            if size:
                assert after['peak_job_commit_bytes'] >= size
            record['runs'].append({'allocation_bytes': size, 'before_resume': before, 'post_exit': after,
                                   'exit_code': proc.returncode, 'no_intermediate_samples': True})
        finally:
            proc.close()
    proc = WindowsJobProcess([sys.executable, '-c', 'import time;time.sleep(30)'])
    try:
        time.sleep(.3)
        timings = []
        cpu = time.process_time()
        for _ in range(100):
            start = time.perf_counter()
            snapshot = proc.counters()
            timings.append(time.perf_counter()-start)
        record['query_overhead'] = {'queries': len(timings), 'driver_cpu_seconds': time.process_time()-cpu,
            'median_wall_seconds': statistics.median(timings), 'max_wall_seconds': max(timings),
            'live_members': snapshot['members'], 'scope': 'Native counter queries on idle Python job only; not browser instrumentation overhead.'}
    finally:
        proc.terminate()
        proc.wait(15)
        record['cleanup'] = proc.counters()
        proc.close()
    path = owned/'evidence.json'
    path.write_text(json.dumps(record, indent=2)+'\n', encoding='utf-8')
    print(path)


if __name__ == '__main__':
    main()
