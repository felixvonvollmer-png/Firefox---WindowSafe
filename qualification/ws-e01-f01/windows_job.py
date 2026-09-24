"""Owned, non-breakaway Windows Job launcher; qualification only.

CPU/IO are lifetime job counters, including exited children. PeakJobMemoryUsed
is OS commit accounting, never addon-attributable RAM. Identity diagnostics are
point samples and cannot identify every short-lived child.
"""
import ctypes as c
from ctypes import wintypes as w
import os
import subprocess
import time


class BasicLimits(c.Structure):
    _fields_ = [('process_time', c.c_longlong), ('job_time', c.c_longlong),
                ('flags', w.DWORD), ('min_ws', c.c_size_t), ('max_ws', c.c_size_t),
                ('active_limit', w.DWORD), ('affinity', c.c_size_t),
                ('priority', w.DWORD), ('scheduling', w.DWORD)]


class IO(c.Structure):
    _fields_ = [(n, c.c_ulonglong) for n in ('read_ops', 'write_ops', 'other_ops',
                                          'read_bytes', 'write_bytes', 'other_bytes')]


class Extended(c.Structure):
    _fields_ = [('basic', BasicLimits), ('io', IO)] + [(n, c.c_size_t) for n in
        ('process_memory_limit', 'job_memory_limit', 'peak_process_commit', 'peak_job_commit')]


class Accounting(c.Structure):
    _fields_ = [(n, c.c_longlong) for n in ('user', 'kernel', 'period_user', 'period_kernel')] + [
        (n, w.DWORD) for n in ('page_faults', 'total_processes', 'active_processes', 'terminated_processes')]


class BasicIO(c.Structure):
    _fields_ = [('basic', Accounting), ('io', IO)]


def api():
    if os.name != 'nt':
        raise OSError('Windows native Job APIs required')
    k = c.WinDLL('kernel32', use_last_error=True)
    signatures = {
        'CreateJobObjectW': ([c.c_void_p, w.LPCWSTR], w.HANDLE),
        'SetInformationJobObject': ([w.HANDLE, c.c_int, c.c_void_p, w.DWORD], w.BOOL),
        'QueryInformationJobObject': ([w.HANDLE, c.c_int, c.c_void_p, w.DWORD, c.c_void_p], w.BOOL),
        'AssignProcessToJobObject': ([w.HANDLE, w.HANDLE], w.BOOL),
        'IsProcessInJob': ([w.HANDLE, w.HANDLE, c.POINTER(w.BOOL)], w.BOOL),
        'GetCurrentProcess': ([], w.HANDLE),
        'ResumeThread': ([w.HANDLE], w.DWORD),
        'TerminateProcess': ([w.HANDLE, w.UINT], w.BOOL),
        'TerminateJobObject': ([w.HANDLE, w.UINT], w.BOOL),
        'WaitForSingleObject': ([w.HANDLE, w.DWORD], w.DWORD),
        'GetExitCodeProcess': ([w.HANDLE, c.POINTER(w.DWORD)], w.BOOL),
        'OpenProcess': ([w.DWORD, w.BOOL, w.DWORD], w.HANDLE),
        'GetProcessTimes': ([w.HANDLE] + [c.POINTER(w.FILETIME)] * 4, w.BOOL),
        'QueryFullProcessImageNameW': ([w.HANDLE, w.DWORD, w.LPWSTR, c.POINTER(w.DWORD)], w.BOOL),
        'CloseHandle': ([w.HANDLE], w.BOOL),
    }
    for name, (args, result) in signatures.items():
        getattr(k, name).argtypes = args
        getattr(k, name).restype = result
    return k


def checked(ok):
    if not ok:
        raise c.WinError(c.get_last_error())


class WindowsJobProcess:
    def __init__(self, command, log_path=None, *, _fail_assignment=False):
        import _winapi
        self.k = api()
        self.job = self.k.CreateJobObjectW(None, None)
        checked(self.job)
        self.handle = None
        self.returncode = None
        self.identities = {}
        thread = None
        try:
            limits = Extended()
            limits.basic.flags = 0x2000  # KILL_ON_JOB_CLOSE; no breakaway flags.
            checked(self.k.SetInformationJobObject(self.job, 9, c.byref(limits), c.sizeof(limits)))
            parent = w.BOOL()
            checked(self.k.IsProcessInJob(self.k.GetCurrentProcess(), None, c.byref(parent)))
            self.launcher_in_job = bool(parent.value)
            startup = subprocess.STARTUPINFO()
            self.handle, thread, self.pid, _ = _winapi.CreateProcess(
                command[0], subprocess.list2cmdline(command), None, None, False,
                0x4 | 0x08000000, None, None, startup)  # SUSPENDED, NO_WINDOW (console only).
            checked(self.k.AssignProcessToJobObject(None if _fail_assignment else self.job, self.handle))
            membership = w.BOOL()
            checked(self.k.IsProcessInJob(self.handle, self.job, c.byref(membership)))
            if not membership.value:
                raise OSError('suspended root containment not proven')
            self.before_resume = self.counters()
            if self.before_resume['active_processes'] != 1:
                raise OSError('unexpected pre-resume job membership')
            if self.k.ResumeThread(thread) == 0xffffffff:
                raise c.WinError(c.get_last_error())
        except BaseException:
            if self.handle:
                checked(self.k.TerminateProcess(self.handle, 125))
                if self.k.WaitForSingleObject(self.handle, 15000) != 0:
                    raise OSError('failed suspended root cleanup')
                self.k.CloseHandle(self.handle)
            self.k.CloseHandle(self.job)
            self.job = None
            raise
        finally:
            if thread:
                self.k.CloseHandle(thread)

    def query(self, kind, cls):
        value = cls()
        checked(self.k.QueryInformationJobObject(self.job, kind, c.byref(value), c.sizeof(value), None))
        return value

    def members(self):
        # Variable-sized ULONG_PTR list; retry if children arrive during query.
        for capacity in (64, 256, 1024, 4096):
            class Pids(c.Structure):
                _fields_ = [('assigned', w.DWORD), ('count', w.DWORD), ('pids', c.c_size_t * capacity)]
            value = Pids()
            if self.k.QueryInformationJobObject(self.job, 3, c.byref(value), c.sizeof(value), None):
                return list(value.pids[:value.count])
            if c.get_last_error() != 234:
                raise c.WinError(c.get_last_error())
        raise OSError('job member list exceeded bound')

    def counters(self):
        a = self.query(8, BasicIO)
        limits = self.query(9, Extended)
        if limits.basic.flags != 0x2000:
            raise OSError('job containment policy drift')
        identities = []
        for pid in self.members():
            h = self.k.OpenProcess(0x1000, False, pid)
            if not h:
                if pid not in self.members():
                    continue  # Exited race; lifetime accounting is unaffected.
                raise c.WinError(c.get_last_error())
            try:
                member = w.BOOL()
                checked(self.k.IsProcessInJob(h, self.job, c.byref(member)))
                if not member.value:
                    raise OSError('PID identity changed outside owned job')
                creation, end, kernel, user = (w.FILETIME() for _ in range(4))
                checked(self.k.GetProcessTimes(h, c.byref(creation), c.byref(end), c.byref(kernel), c.byref(user)))
                identity = (creation.dwHighDateTime << 32) | creation.dwLowDateTime
                image = c.create_unicode_buffer(32768)
                size = w.DWORD(len(image))
                checked(self.k.QueryFullProcessImageNameW(h, 0, image, c.byref(size)))
                self.identities[(pid, identity)] = True
                identities.append({'pid': pid, 'creation_filetime': identity, 'in_job': True,
                                   'image': image.value})
            finally:
                self.k.CloseHandle(h)
        return {'monotonic': time.monotonic(),
                'user_seconds': a.basic.user / 1e7, 'kernel_seconds': a.basic.kernel / 1e7,
                'total_processes': a.basic.total_processes, 'active_processes': a.basic.active_processes,
                'io': {n: getattr(a.io, n) for n, _ in IO._fields_},
                'peak_job_commit_bytes': limits.peak_job_commit,
                'peak_process_commit_bytes': limits.peak_process_commit,
                'members': identities, 'limit_flags': limits.basic.flags,
                'semantics': 'Lifetime job CPU/IO including exited children; OS commit peaks, not working set or addon peak.'}

    def poll(self):
        if self.query(8, BasicIO).basic.active_processes == 0:
            code = w.DWORD()
            checked(self.k.GetExitCodeProcess(self.handle, c.byref(code)))
            self.returncode = code.value
        return self.returncode

    def bind_browser(self, pid, binary):
        from pathlib import Path
        matches = [p for p in self.counters()['members'] if p['pid'] == pid]
        if len(matches) != 1 or Path(matches[0]['image']).resolve() != Path(binary).resolve():
            raise ValueError('browser protocol PID not in owned job with exact executable')
        return matches[0]

    def wait(self, timeout):
        deadline = time.monotonic() + timeout
        while self.poll() is None:
            if time.monotonic() >= deadline:
                raise TimeoutError('owned job did not empty')
            time.sleep(.05)
        return self.returncode

    def terminate(self):
        checked(self.k.TerminateJobObject(self.job, 125))

    def close(self):
        if self.job:
            if self.poll() is None:
                self.terminate()
                self.wait(15)
            self.k.CloseHandle(self.handle)
            self.k.CloseHandle(self.job)
            self.job = None
