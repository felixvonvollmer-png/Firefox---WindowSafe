"""Ubuntu user-service cgroup CPU counter qualification; tiny synthetic worker."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import uuid

ROOT = Path(__file__).resolve().parents[2]


def main():
    if sys.platform != 'linux': raise SystemExit('Ubuntu user systemd environment required')
    outroot = ROOT / 'build/f01'; outroot.mkdir(parents=True, exist_ok=True)
    owned = Path(tempfile.mkdtemp(prefix='cgroup-dry-', dir=outroot)).resolve()
    unit = 'windowsafe-f01-dry-' + uuid.uuid4().hex + '.service'
    worker = '''import pathlib,time,sys,os
p=pathlib.Path(sys.argv[1]); (p/'ready').write_text(str(os.getpid()))
while not (p/'go').exists(): time.sleep(.05)
start=time.process_time(); memory=bytearray(4*1024*1024)
while time.process_time()-start < .5:
 for i in range(0,len(memory),4096): memory[i]=(memory[i]+1)%256
with (p/'synthetic.bin').open('wb') as f: f.write(memory); f.flush(); os.fsync(f.fileno())
(p/'done').write_text(str(time.process_time()-start))
while not (p/'finish').exists(): time.sleep(.05)
'''
    command = ['systemd-run', '--user', '--unit=' + unit, '--property=Type=exec',
        '--property=CPUAccounting=yes', '--property=MemoryAccounting=yes', '--property=IOAccounting=yes',
        sys.executable, '-c', worker, str(owned)]
    subprocess.run(command, check=True, capture_output=True)
    evidence = {'evidence_class': 'SYNTHETIC_DRY_RUN_MEASUREMENT', 'unit': unit,
        'command': command, 'product_performance_verdict': 'NOT_EVALUATED'}
    try:
        deadline = time.monotonic() + 15
        while not (owned / 'ready').exists():
            if time.monotonic() > deadline: raise TimeoutError('synthetic worker not ready')
            time.sleep(.05)
        group = subprocess.check_output(['systemctl', '--user', 'show', unit, '-p', 'ControlGroup', '--value'], text=True).strip()
        if unit not in group or not group.startswith('/user.slice/'): raise ValueError('own user cgroup required')
        base = Path('/sys/fs/cgroup') / group.lstrip('/')
        def counters():
            return {p: (base / p).read_text() if (base / p).exists() else None
                    for p in ('cpu.stat', 'memory.current', 'memory.peak', 'io.stat', 'cgroup.procs')}
        def cpu(c): return int(dict(l.split() for l in c['cpu.stat'].splitlines())['usage_usec'])
        initial = counters(); start = time.monotonic(); (owned / 'go').touch()
        while not (owned / 'done').exists():
            if time.monotonic() > deadline: raise TimeoutError('synthetic worker stalled')
            time.sleep(.05)
        final = counters(); elapsed = time.monotonic() - start
        evidence.update(cgroup=group, before=initial, after=final, elapsed_seconds=elapsed,
            cpu_delta_seconds=(cpu(final)-cpu(initial))/1000000,
            percent_one_core=100*(cpu(final)-cpu(initial))/1000000/elapsed,
            worker_cpu_seconds=float((owned/'done').read_text()),
            status='COUNTERS_OBSERVED', limitation='Synthetic Python worker, not Firefox or product. cgroup memory includes native/shared charges; io.stat may be unavailable/empty for the storage layer.')
        if not .45 <= evidence['cpu_delta_seconds'] <= 2: raise ValueError('CPU accounting dry-run outside sanity bounds')
    finally:
        (owned / 'finish').touch()
        subprocess.run(['systemctl', '--user', 'stop', unit], check=True, capture_output=True)
        evidence['cleanup'] = 'OWN_TRANSIENT_UNIT_STOPPED'
        (owned / 'synthetic.bin').unlink(missing_ok=True)
        (owned / 'evidence.json').write_text(json.dumps(evidence, indent=2)+'\n')
    print(json.dumps({'evidence': str(owned / 'evidence.json'), 'status': evidence['status']}))


if __name__ == '__main__': main()
