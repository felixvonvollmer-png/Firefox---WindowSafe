"""Finite, synthetic-only Firefox run. Creates its own profile; never accepts one."""
import argparse
import configparser
import functools
import hashlib
import http.server
import json
import os
from pathlib import Path
import shutil
import signal
import socket
import subprocess
import tempfile
import threading
import time
import zipfile
import uuid

from measure import sample, summarize

ROOT = Path(__file__).resolve().parents[2]
SOURCE = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class Marionette:
    def __init__(self, port):
        self.sock = socket.create_connection(('127.0.0.1', port), timeout=30)
        self.serial = 0
        self.hello = self.receive()
        if self.hello.get('marionetteProtocol') != 3: raise ValueError('unexpected protocol')

    def receive(self):
        size = b''
        while True:
            b = self.sock.recv(1)
            if not b: raise EOFError('Marionette disconnected')
            if b == b':': break
            size += b
            if len(size) > 12: raise ValueError('invalid frame length')
        remaining = int(size); data = b''
        if remaining > 10000000: raise ValueError('oversize frame')
        while remaining:
            b = self.sock.recv(remaining)
            if not b: raise EOFError('incomplete frame')
            data += b; remaining -= len(b)
        return json.loads(data)

    def command(self, name, args=None):
        self.serial += 1
        data = json.dumps([0, self.serial, name, args or {}]).encode()
        self.sock.sendall(str(len(data)).encode() + b':' + data)
        result = self.receive()
        if result[:2] != [1, self.serial]: raise ValueError('response identity mismatch')
        if result[2]: raise RuntimeError(json.dumps(result[2]))
        return result[3]

    def close(self):
        self.sock.close()


class UserCgroupProcess:
    """Own unique transient service; complete descendant CPU accounting on Ubuntu."""
    def __init__(self, command, log_path):
        self.unit = 'windowsafe-f01-browser-' + uuid.uuid4().hex + '.service'
        launch = ['systemd-run', '--user', '--unit=' + self.unit, '--property=Type=exec',
            '--property=CPUAccounting=yes', '--property=MemoryAccounting=yes', '--property=IOAccounting=yes',
            '--property=StandardOutput=append:' + str(log_path), '--property=StandardError=inherit']
        for name in ('DISPLAY', 'WAYLAND_DISPLAY', 'XDG_RUNTIME_DIR', 'DBUS_SESSION_BUS_ADDRESS'):
            if name in os.environ: launch.append('--setenv=' + name + '=' + os.environ[name])
        subprocess.run(launch + command, check=True, capture_output=True)
        self.pid = int(self.property('MainPID'))
        if self.pid <= 0: raise ValueError('owned Firefox service did not start')
        group = self.property('ControlGroup')
        if not group.startswith('/user.slice/') or self.unit not in group: raise ValueError('owned Firefox cgroup mismatch')
        self.group = Path('/sys/fs/cgroup') / group.lstrip('/')
        self.returncode = None

    def property(self, name):
        return subprocess.check_output(['systemctl', '--user', 'show', self.unit, '-p', name, '--value'], text=True).strip()

    def poll(self):
        if not (self.group / 'cgroup.procs').exists() or not (self.group / 'cgroup.procs').read_text().strip():
            self.returncode = int(self.property('ExecMainStatus') or '0')
        return self.returncode

    def wait(self, timeout):
        deadline = time.monotonic() + timeout
        while self.poll() is None:
            if time.monotonic() >= deadline: raise TimeoutError('own cgroup did not exit')
            time.sleep(.1)
        return self.returncode

    def terminate(self):
        subprocess.run(['systemctl', '--user', 'stop', self.unit], check=True, capture_output=True)

    def counters(self):
        return {name: (self.group / name).read_text() if (self.group / name).exists() else None
                for name in ('cpu.stat', 'memory.current', 'memory.peak', 'io.stat', 'cgroup.procs')}


class LocalOnly(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass

    def do_GET(self):
        if self.path.split('?', 1)[0] != '/article.html':
            self.send_error(404); return
        super().do_GET()


def package(kind, target, url, run):
    data = {p.name: p.read_bytes() for p in (SOURCE / kind).iterdir() if p.is_file() and p.suffix != '.ts'}
    if kind == 'probe':
        data['background.js'] = (ROOT / 'build/f01/compiled/background.js').read_bytes()
        data['config.js'] = ('const F01_CONFIG = ' + json.dumps({'url': url, 'run': run}) + ';\n').encode()
    with zipfile.ZipFile(target, 'x', compression=zipfile.ZIP_DEFLATED) as archive:
        for name, content in sorted(data.items()):
            info = zipfile.ZipInfo(name, (2026, 9, 19, 0, 0, 0)); info.external_attr = 0o100644 << 16
            archive.writestr(info, content)
    return digest(target)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--firefox', type=Path, required=True)
    parser.add_argument('--firefox-sha256', required=True)
    parser.add_argument('--persistent-test-build-version')
    parser.add_argument('--headless', action='store_true')
    args = parser.parse_args()
    binary = args.firefox.resolve(strict=True)
    if digest(binary) != args.firefox_sha256: raise ValueError('binary hash mismatch')
    ini = configparser.ConfigParser(); ini.read(binary.parent / 'application.ini')
    version = ini['App']['Version']
    channel = (binary.parent / 'defaults/pref/channel-prefs.js').read_text()
    persistent = args.persistent_test_build_version is not None
    if persistent:
        if version != args.persistent_test_build_version or not any('"' + c + '"' in channel for c in ('aurora', 'nightly')):
            raise ValueError('explicit official Developer/Nightly test build required')
    elif version != '156.0' or '"release"' not in channel:
        raise ValueError('exact Firefox 156.0 Stable required')
    outroot = ROOT / 'build/f01/runs'; outroot.mkdir(parents=True, exist_ok=True)
    owned = Path(tempfile.mkdtemp(prefix='synthetic-', dir=outroot)).resolve()
    profile = owned / 'profile'; profile.mkdir()
    downloads = owned / 'downloads'; downloads.mkdir()
    run_id = owned.name
    handler = functools.partial(LocalOnly, directory=str(SOURCE / 'pages'))
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
    with socket.socket() as reservation:
        reservation.bind(('127.0.0.1', 0)); port = reservation.getsockname()[1]
    prefs = {
        'marionette.port': port, 'browser.shell.checkDefaultBrowser': False,
        'browser.startup.homepage': 'about:blank', 'browser.startup.page': 3 if persistent else 0,
        'browser.sessionstore.resume_from_crash': False,
        'browser.startup.homepage_override.mstone': 'ignore', 'startup.homepage_welcome_url': '',
        'startup.homepage_welcome_url.additional': '', 'browser.aboutwelcome.enabled': False,
        'browser.newtabpage.enabled': False, 'browser.tabs.warnOnClose': False,
        'browser.warnOnQuit': False, 'browser.download.folderList': 2,
        'browser.download.dir': str(downloads), 'browser.download.useDownloadDir': True,
        'browser.download.always_ask_before_handling_new_types': False,
        'app.update.auto': False, 'app.update.disabledForTesting': True,
        'datareporting.policy.dataSubmissionEnabled': False, 'toolkit.telemetry.enabled': False,
        'browser.newtabpage.activity-stream.feeds.telemetry': False,
        'network.proxy.type': 1, 'network.proxy.http': '127.0.0.1', 'network.proxy.http_port': 9,
        'network.proxy.ssl': '127.0.0.1', 'network.proxy.ssl_port': 9,
        'network.proxy.no_proxies_on': 'localhost, 127.0.0.1',
        'network.dns.disablePrefetch': True, 'network.prefetch-next': False,
        'extensions.autoDisableScopes': 0,
    }
    if persistent: prefs['xpinstall.signatures.required'] = False
    (profile / 'user.js').write_text(''.join('user_pref(' + json.dumps(k) + ', ' + json.dumps(v) + ');\n' for k, v in prefs.items()))
    evidence = {'run_id': run_id, 'profile_class': 'NEW_SYNTHETIC_DISPOSABLE', 'profile': str(profile),
        'binary': str(binary), 'binary_sha256': digest(binary), 'version': version,
        'build_id': ini['App']['BuildID'], 'source_stamp': ini['App']['SourceStamp'],
        'evidence_class': ('WINDOWS_RUNTIME_VERIFIED' if os.name == 'nt' else 'UBUNTU_RUNTIME_VERIFIED'),
        'runtime_scope': 'TEST_BUILD_ONLY_RESTART' if persistent else 'TARGET_STABLE',
        'headless': args.headless, 'prefs_sha256': digest(profile / 'user.js'), 'launches': [],
        'probe_packages': {}, 'reports': [], 'cleanup': 'PENDING', 'status': 'RUNNING'}
    for kind in ('helper', 'probe'):
        evidence['probe_packages'][kind] = package(kind, owned / (kind + '.xpi'),
            f'http://127.0.0.1:{server.server_port}/article.html', run_id)
    samples = []
    try:
        for ordinal in range(1, 3 if persistent else 2):
            command = [str(binary), '--no-remote', '--new-instance', '--profile', str(profile), '--marionette']
            if args.headless: command.append('--headless')
            client = None
            with (owned / f'firefox-{ordinal}.log').open('wb') as log:
                proc = (UserCgroupProcess(command, owned / f'firefox-{ordinal}.log') if os.name != 'nt' else
                        subprocess.Popen(command, stdout=log, stderr=subprocess.STDOUT))
                launch = {'command': command, 'pid': proc.pid}; evidence['launches'].append(launch)
                if os.name != 'nt': launch['cgroup'] = str(proc.group)
                def collect():
                    value = sample(proc.pid)
                    if os.name != 'nt':
                        value['cgroup'] = proc.counters()
                        value['cgroup_path'] = str(proc.group)
                    samples.append(value)
                try:
                    deadline = time.monotonic() + 45
                    while time.monotonic() < deadline:
                        if proc.poll() is not None: raise RuntimeError('owned Firefox exited before protocol')
                        try:
                            client = Marionette(port); break
                        except (ConnectionRefusedError, TimeoutError): time.sleep(0.2)
                    if client is None: raise TimeoutError('owned Firefox protocol unavailable')
                    session = client.command('WebDriver:NewSession', {'capabilities': {'alwaysMatch': {'acceptInsecureCerts': False}}})
                    capabilities = session.get('capabilities', session.get('value', {}).get('capabilities', {}))
                    if capabilities.get('moz:processID') != proc.pid:
                        raise ValueError('protocol process identity mismatch')
                    if Path(capabilities['moz:profile']).resolve() != profile:
                        raise ValueError('protocol profile identity mismatch')
                    launch['session_binding'] = {k: capabilities.get(k) for k in ('browserVersion', 'moz:processID', 'moz:profile', 'moz:buildID')}
                    if ordinal == 1:
                        for kind in ('helper', 'probe'):
                            client.command('Addon:Install', {'path': str(owned / (kind + '.xpi')), 'temporary': not persistent})
                    deadline = time.monotonic() + 60
                    report_path = downloads / f'f01-{ordinal}.json'
                    while time.monotonic() < deadline:
                        collect()
                        if report_path.exists() and not list(downloads.glob('*.part')):
                            # Firefox may create the final filename before writing the JSON.
                            try: report = json.loads(report_path.read_text())
                            except json.JSONDecodeError: report = None
                            if report is not None:
                                if report.get('qualificationOnly') is not True or report.get('marker', {}).get('run') != run_id or report['marker']['ordinal'] != ordinal:
                                    raise ValueError('synthetic report binding mismatch')
                                evidence['reports'].append(report); break
                        if proc.poll() is not None: raise RuntimeError('owned Firefox exited before report')
                        time.sleep(0.25)
                    else: raise TimeoutError('synthetic report absent')
                    for _ in range(12): collect(); time.sleep(0.25)
                    launch['observed_processes'] = sorted({p['pid'] for s in samples for p in s['processes']})
                    client.command('Marionette:Quit', {'flags': ['eForceQuit']})
                    proc.wait(timeout=20)
                finally:
                    if client: client.close()
                    if proc.poll() is None:
                        proc.terminate()
                        proc.wait(timeout=15)
                    launch['exit_code'] = proc.returncode
        evidence['status'] = 'OBSERVATIONS_COLLECTED__MATRIX_REVIEW_REQUIRED'
    except Exception as error:
        evidence['status'] = 'PROBE_FAILED'; evidence['error'] = str(error)
    finally:
        server.shutdown(); server.server_close()
        evidence['measurement'] = summarize(samples) if len(samples) > 1 else {'status': 'NOT_EXECUTED'}
        groups = {}
        for entry in samples:
            if 'cgroup_path' in entry: groups.setdefault(entry['cgroup_path'], []).append(entry)
        intervals = []
        for group, rows in groups.items():
            if len(rows) < 2: continue
            usage = lambda row: int(dict(line.split() for line in row['cgroup']['cpu.stat'].splitlines())['usage_usec'])
            seconds = rows[-1]['monotonic'] - rows[0]['monotonic']
            cpu = (usage(rows[-1])-usage(rows[0])) / 1000000
            intervals.append({'cgroup': group, 'wall_seconds': seconds, 'cpu_seconds': cpu,
                              'percent_one_core': 100 * cpu / seconds,
                              'coverage': 'OWN_FIREFOX_CGROUP_INCLUDING_EXITED_DESCENDANTS'})
        evidence['cgroup_measurement_intervals'] = intervals
        # Keep failure evidence, but never retain the disposable browser data itself.
        try:
            residual = []
            for launch in evidence['launches']:
                residual.extend(sample(launch['pid'])['processes'])
            if residual: raise OSError('own descendant cleanup not proven')
            evidence['remaining_owned_processes'] = []
            shutil.rmtree(profile); evidence['cleanup'] = 'OWN_PROFILE_REMOVED__OWN_LAUNCHES_EXITED'
        except OSError:
            evidence['cleanup'] = 'OWN_PROFILE_CLEANUP_INCOMPLETE'
        (owned / 'samples.json').write_text(json.dumps(samples, indent=2) + '\n')
        (owned / 'evidence.json').write_text(json.dumps(evidence, indent=2) + '\n')
        print(json.dumps({'evidence': str(owned / 'evidence.json'), 'status': evidence['status'], 'cleanup': evidence['cleanup']}))
    if evidence['status'] == 'PROBE_FAILED': raise SystemExit(1)


if __name__ == '__main__':
    main()
