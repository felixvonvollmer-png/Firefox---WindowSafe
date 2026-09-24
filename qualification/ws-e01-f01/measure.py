"""Synthetic instrumentation. OS counters are NOT attributable addon memory."""
import os
from pathlib import Path
import time


def linux_tree(root_pid):
    rows = {}
    for path in Path('/proc').glob('[0-9]*/stat'):
        try:
            text = path.read_text(); fields = text[text.rfind(')') + 2:].split()
            pid = int(path.parent.name)
            rows[pid] = {'pid': pid, 'ppid': int(fields[1]), 'identity': fields[19],
                         'cpu_seconds': (int(fields[11]) + int(fields[12])) / os.sysconf('SC_CLK_TCK'),
                         'rss_bytes': int(fields[21]) * os.sysconf('SC_PAGE_SIZE')}
        except (OSError, ValueError, IndexError):
            continue
    own = {root_pid}
    while True:
        expanded = own | {pid for pid, row in rows.items() if row['ppid'] in own}
        if expanded == own:
            break
        own = expanded
    result = []
    for pid in sorted(own & rows.keys()):
        row = rows[pid]
        try:
            counters = dict(line.split(': ') for line in Path(f'/proc/{pid}/io').read_text().splitlines())
            row['io'] = {k: int(counters[k]) for k in ('rchar', 'wchar', 'read_bytes', 'write_bytes', 'syscr', 'syscw')}
        except OSError:
            row['io'] = None
        result.append(row)
    return result


def windows_tree(root_pid):
    # Native standard-library ctypes: no provider, WMI agent or external package.
    import ctypes as c
    from ctypes import wintypes as w
    class Entry(c.Structure):
        _fields_ = [('size', w.DWORD), ('usage', w.DWORD), ('pid', w.DWORD), ('heap', c.c_size_t),
                    ('module', w.DWORD), ('threads', w.DWORD), ('ppid', w.DWORD), ('priority', w.LONG),
                    ('flags', w.DWORD), ('exe', w.WCHAR * 260)]
    class Memory(c.Structure):
        _fields_ = [('cb', w.DWORD), ('faults', w.DWORD)] + [(n, c.c_size_t) for n in
            ('peakWorkingSet', 'workingSet', 'peakPagedPool', 'pagedPool', 'peakNonPagedPool',
             'nonPagedPool', 'pagefile', 'peakPagefile', 'privateUsage')]
    class IO(c.Structure):
        _fields_ = [(n, c.c_ulonglong) for n in ('read_operations', 'write_operations', 'other_operations',
            'read_transfer_bytes', 'write_transfer_bytes', 'other_transfer_bytes')]
    k = c.WinDLL('kernel32', use_last_error=True); ps = c.WinDLL('psapi', use_last_error=True)
    k.CreateToolhelp32Snapshot.argtypes = [w.DWORD, w.DWORD]; k.CreateToolhelp32Snapshot.restype = w.HANDLE
    k.OpenProcess.argtypes = [w.DWORD, w.BOOL, w.DWORD]; k.OpenProcess.restype = w.HANDLE
    k.CloseHandle.argtypes = [w.HANDLE]
    k.Process32FirstW.argtypes = [w.HANDLE, c.POINTER(Entry)]; k.Process32NextW.argtypes = [w.HANDLE, c.POINTER(Entry)]
    k.GetProcessTimes.argtypes = [w.HANDLE] + [c.POINTER(w.FILETIME)] * 4
    k.GetProcessIoCounters.argtypes = [w.HANDLE, c.POINTER(IO)]
    ps.GetProcessMemoryInfo.argtypes = [w.HANDLE, c.POINTER(Memory), w.DWORD]
    snapshot = k.CreateToolhelp32Snapshot(2, 0)
    if snapshot == c.c_void_p(-1).value: raise OSError('process snapshot failed')
    entry = Entry(); entry.size = c.sizeof(entry); parents = {}
    try:
        ok = k.Process32FirstW(snapshot, c.byref(entry))
        while ok:
            parents[entry.pid] = entry.ppid
            ok = k.Process32NextW(snapshot, c.byref(entry))
    finally:
        k.CloseHandle(snapshot)
    own = {root_pid}
    while True:
        expanded = own | {pid for pid, ppid in parents.items() if ppid in own}
        if expanded == own: break
        own = expanded
    rows = []
    ticks = lambda t: (t.dwHighDateTime << 32) | t.dwLowDateTime
    for pid in sorted(own & parents.keys()):
        handle = k.OpenProcess(0x0400 | 0x0010, False, pid)
        if not handle: raise OSError('owned process counter access unavailable')
        try:
            creation, end, kernel, user = (w.FILETIME() for _ in range(4))
            if not k.GetProcessTimes(handle, c.byref(creation), c.byref(end), c.byref(kernel), c.byref(user)):
                raise OSError('process times unavailable')
            memory = Memory(); memory.cb = c.sizeof(memory); io = IO()
            if not ps.GetProcessMemoryInfo(handle, c.byref(memory), c.sizeof(memory)):
                raise OSError('process memory unavailable')
            if not k.GetProcessIoCounters(handle, c.byref(io)): raise OSError('process IO unavailable')
            rows.append({'pid': pid, 'ppid': parents[pid], 'identity': str(ticks(creation)),
                'cpu_seconds': (ticks(kernel) + ticks(user)) / 10000000,
                'rss_bytes': memory.workingSet, 'private_bytes': memory.privateUsage,
                'io': {n: getattr(io, n) for n, _ in IO._fields_}})
        finally:
            k.CloseHandle(handle)
    return rows


def sample(root_pid):
    return {'monotonic': time.monotonic(), 'processes':
        windows_tree(root_pid) if os.name == 'nt' else linux_tree(root_pid)}


def summarize(samples):
    if len(samples) < 2: raise ValueError('at least two samples required')
    first, last = samples[0], samples[-1]
    baseline = {(p['pid'], p['identity']): p['cpu_seconds'] for p in first['processes']}
    maxima = dict(baseline)
    for s in samples:
        for p in s['processes']:
            key = (p['pid'], p['identity']); maxima[key] = max(maxima.get(key, 0), p['cpu_seconds'])
    elapsed = last['monotonic'] - first['monotonic']
    cpu = sum(v - baseline.get(k, 0) for k, v in maxima.items())
    return {'evidence_class': 'SYNTHETIC_DRY_RUN_MEASUREMENT', 'wall_seconds': elapsed,
            'observed_cpu_seconds': cpu, 'percent_one_core': 100 * cpu / elapsed,
            'peak_sum_rss_bytes': max(sum(p['rss_bytes'] for p in s['processes']) for s in samples),
            'observed_process_identities': len(maxima),
            'limitation': 'Sampled CPU lower bound: short-lived processes/final ticks may be missed. RSS sums shared pages. Not attributable addon JS/DOM RAM. Not final acceptance instrumentation.',
            'product_performance_verdict': 'NOT_EVALUATED'}
