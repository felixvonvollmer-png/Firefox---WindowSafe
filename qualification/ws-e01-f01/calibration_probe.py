"""F01 measurement calibration on the visible Ubuntu desktop; synthetic disposable profiles only.

A/A calibration: every run is WITHOUT WindowSafe; pair differences estimate noise and known
uncertainty of the bound CPU protocol (L10 600 s, B300 10 s window, idle 600 s) for R500/R2000.
Also repeats the free-but-resident reuse trials with alternating order and a fresh-state control.
The driver add-on is the identical synthetic workload in both runs of a pair; it is test-only and
never a product capability. No result here is a WindowSafe performance claim.
"""
import argparse
import configparser
import functools
import http.server
import json
import os
from pathlib import Path
import platform
import shutil
import socket
import statistics
import tempfile
import threading
import time
import zipfile

from run_probe import Marionette, UserCgroupProcess, digest, preserve_driver_sources
from target_probe import execute
from closure_probe import api as _unused_api, extension_process, reset_high_water, status_kib  # noqa: F401
import fixtures

ROOT = Path(__file__).resolve().parents[2]
SOURCE = Path(__file__).resolve().parent
ID = 'f01-calibration@windowsafe.invalid'
MIB = 1024 * 1024
DRIVER = r'''
const wait = ms => new Promise(r => setTimeout(r, ms));
let observed = 0;
browser.tabs.onUpdated.addListener(() => { observed++; });
browser.tabs.onMoved.addListener(() => { observed++; });
const hex = b => Array.from(b, x => x.toString(16).padStart(2, '0')).join('');
window.calibrationOperation = async (op, arg) => {
  if (op === 'realize') {
    // arg: {tabs:[...fixture rows], base:url}; containers 1..3 created, 0 = default.
    const stores = ['firefox-default'];
    for (let i = 1; i < 4; i++) stores.push((await browser.contextualIdentities.create(
      {name:'Synthetic ' + i, color:'blue', icon:'circle'})).cookieStoreId);
    const byWindow = new Map();
    for (const t of arg.tabs) { if (!byWindow.has(t.window)) byWindow.set(t.window, []); byWindow.get(t.window).push(t); }
    let created = 0, windows = 0;
    for (const rows of byWindow.values()) {
      const w = await browser.windows.create({type:'normal', url:rows[0].url}); windows++;
      const first = (await browser.tabs.query({windowId:w.id}))[0];
      const ids = new Map([[rows[0].syntheticId, first.id]]);
      for (const t of rows.slice(1)) {
        const spec = {windowId:w.id, url:t.url, active:false, cookieStoreId:stores[t.container]};
        if (t.pinned) spec.pinned = true; else if (!arg.discardAfterGroup) { spec.discarded = true; if (!arg.noTitle) spec.title = t.title; }
        const tab = await browser.tabs.create(spec); ids.set(t.syntheticId, tab.id); created++;
        if (t.muted) await browser.tabs.update(tab.id, {muted:true});
      }
      const groups = new Map();
      for (const t of rows) if (t.group !== null && !t.pinned) {
        if (!groups.has(t.group)) groups.set(t.group, []); groups.get(t.group).push(ids.get(t.syntheticId)); }
      for (const tabIds of groups.values()) { try { await browser.tabs.group({tabIds}); } catch (e) {} }
      if (arg.discardAfterGroup) {
        await wait(2000);
        const loaded = rows.filter(t => !t.pinned && t.syntheticId !== rows[0].syntheticId).map(t => ids.get(t.syntheticId));
        try { await browser.tabs.discard(loaded); } catch (e) {}
      }
    }
    const all = await browser.tabs.query({});
    window.workload = all.filter(t => /synthetic=/.test(t.url)).map(t => t.id);
    return {windows, created: created + windows, tabsTotal: all.length, workloadTabs: window.workload.length};
  }
  if (op === 'adopt') {
    // After a native session restore: the workload is every non-extension tab now present.
    const all = await browser.tabs.query({});
    window.workload = all.filter(t => /synthetic=/.test(t.url)).map(t => t.id);
    const groups = await browser.tabGroups.query({});
    const containers = (await browser.contextualIdentities.query({})).length;
    const ids = all.map(t => (t.url.match(/synthetic=(\d+)/) || [])[1]).filter(Boolean).map(Number);
    return {containers, tabsTotal: all.length, workloadTabs: window.workload.length, groups: groups.length, syntheticIds: ids,
            nonSynthetic: all.filter(t => !/synthetic=/.test(t.url)).map(t => t.url.slice(0, 60)),
            discarded: all.filter(t => t.discarded).length, windows: (await browser.windows.getAll()).length};
  }
  if (op === 'front') {
    // Deterministic stacking: on Wayland all windows overlap at the same position, and the
    // visible window decides how much tab-strip repainting the workload costs.
    const tabs = await browser.tabs.query({});
    const anchor = tabs.find(t => /synthetic=000000/.test(t.url));
    await browser.windows.update(anchor.windowId, {focused: true});
    await wait(500);
    const focused = (await browser.windows.getLastFocused()).id;
    return {frontWindow: anchor.windowId, focusedWindow: focused, ok: focused === anchor.windowId};
  }
  if (op === 'run-schedule') {
    // arg: {kind, schedule:[{at_ms}]} executes relevant changes at their scheduled offsets.
    const start = performance.now(); let delivered = 0, failed = 0, late = 0; const before = observed;
    for (const [i, e] of arg.schedule.entries()) {
      const delay = start + e.at_ms - performance.now();
      if (delay > 0) await wait(delay); else if (delay < -100) late++;
      const id = window.workload[(i * 7) % window.workload.length];
      try {
        if (i % 10 === 9) await browser.tabs.move(id, {index: -1});
        else { const t = await browser.tabs.get(id); await browser.tabs.update(id, {muted: !t.mutedInfo.muted}); }
        delivered++;
      } catch (err) { failed++; }
    }
    return {kind: arg.kind, scheduled: arg.schedule.length, delivered, failed, late,
            observedEvents: observed - before, elapsedMs: performance.now() - start};
  }
  if (op === 'hold-strings') { window.held = []; const b = new Uint8Array(512);
    for (let i = 0; i < arg * 1024; i++) { crypto.getRandomValues(b); window.held.push(hex(b)); } return {n: window.held.length}; }
  if (op === 'drop') { delete window.held; return {dropped: true}; }
  if (op === 'pulse-strings') { const x = []; const b = new Uint8Array(512);
    for (let i = 0; i < arg * 1024; i++) { crypto.getRandomValues(b); x.push(hex(b)); } await wait(50);
    return {n: x.length}; }
  throw Error('unknown finite calibration operation');
};
'''


def api(client, operation, arg=None, timeout_ms=900000):
    client.command('Marionette:SetContext', {'value': 'content'})
    # The shared client has a 30 s socket timeout; long realize/schedule calls need the script timeout.
    client.sock.settimeout(timeout_ms / 1000 + 30)
    try:
        result = client.command('WebDriver:ExecuteAsyncScript', {
            'script': 'const done=arguments[arguments.length-1]; window.wrappedJSObject.calibrationOperation(arguments[0],arguments[1])'
                  '.then(x=>done(JSON.stringify(x)),e=>done(JSON.stringify({error:String(e)})));',
        'args': [operation, arg], 'newSandbox': True, 'sandbox': 'default', 'scriptTimeout': timeout_ms})
    finally:
        client.sock.settimeout(30)
    value = result.get('value', result) if isinstance(result, dict) else result
    return json.loads(value)


def cpu_usec(group):
    for line in (group / 'cpu.stat').read_text().splitlines():
        if line.startswith('usage_usec '):
            return int(line.split()[1])
    raise RuntimeError('cpu.stat usage_usec missing')


def host_busy():
    fields = [int(x) for x in Path('/proc/stat').read_text().splitlines()[0].split()[1:]]
    idle = fields[3] + fields[4]
    return sum(fields), idle


COMPOSITOR = ('gnome-shell', 'Xwayland')


def compositor_ticks():
    """CPU ticks of the display compositor, whose work the visible test itself induces."""
    total = 0
    for stat in Path('/proc').glob('[0-9]*/stat'):
        try:
            head, rest = stat.read_text().rsplit(')', 1)
            if head.split('(', 1)[1] in COMPOSITOR:
                fields = rest.split(); total += int(fields[11]) + int(fields[12])
        except (OSError, IndexError):
            continue
    return total


# Declared protocol constants (METHOD-01/02 calibration); changing them is a method change.
LATE_TOLERANCE = 0.001        # at most 0.1 % of scheduled events may start >100 ms late
INTERFERENCE_WINDOW_S = 5     # foreign host load is judged over every 5 s window
QUIESCENT_PCT = 3.0           # quiescence acknowledgement: owned cgroup below 3 % of one core over 10 s
QUIESCENT_ATTEMPTS = 6


def proc_ticks(pid):
    try:
        fields = Path('/proc', str(pid), 'stat').read_text().rsplit(')', 1)[1].split()
        return int(fields[11]) + int(fields[12])
    except (OSError, IndexError):
        return None


def interval(proc, seconds, during=None, parent_pid=None):
    """Owned-cgroup CPU over a fixed wall interval with 1 s samples of cgroup, compositor, host and parent.

    The workload call runs in a thread so sampling continues; its result or error is returned as driver.
    """
    holder = {}
    thread = None
    if during:
        def run():
            try:
                holder['value'] = during()
            except Exception as error:  # Recorded; makes the run invalid.
                holder['value'] = {'error': repr(error)}
        thread = threading.Thread(target=run, daemon=True)
    tick = os.sysconf('SC_CLK_TCK'); cpus = os.cpu_count()
    snap = lambda: (time.monotonic(), *host_busy(), cpu_usec(proc.group), compositor_ticks(),
                    proc_ticks(parent_pid) if parent_pid else None)
    self0 = time.process_time()
    samples = [snap()]
    if thread: thread.start()
    while True:
        time.sleep(1)
        samples.append(snap())
        elapsed = samples[-1][0] - samples[0][0]
        if elapsed >= seconds and (not thread or not thread.is_alive()):
            break
        if thread and elapsed > seconds + 900:
            holder['value'] = {'error': 'workload exceeded interval by 900 s'}
            break
    (t0, tot0, idl0, cpu0, cmp0, par0), (t1, tot1, idl1, cpu1, cmp1, par1) = samples[0], samples[-1]
    wall = t1 - t0
    def other(a, b):
        host = b[1] - a[1]
        busy = 100 * (host - (b[2] - a[2])) / host if host else 0
        dt = b[0] - a[0]
        return busy - (100 * (b[3] - a[3]) / 1e6 / dt + 100 * (b[4] - a[4]) / tick / dt) / cpus
    window = [other(samples[i], samples[i + INTERFERENCE_WINDOW_S])
              for i in range(len(samples) - INTERFERENCE_WINDOW_S)] or [other(samples[0], samples[-1])]
    cgroup_pct = 100 * (cpu1 - cpu0) / 1e6 / wall
    compositor_pct = 100 * (cmp1 - cmp0) / tick / wall
    host_pct = 100 * ((tot1 - tot0) - (idl1 - idl0)) / (tot1 - tot0) if tot1 - tot0 else None
    return {'wall_s': wall, 'samples': len(samples), 'cgroup_cpu_s': (cpu1 - cpu0) / 1e6,
            'cgroup_cpu_pct_one_core': cgroup_pct, 'compositor_cpu_pct_one_core': compositor_pct,
            'parent_cpu_pct_one_core': None if par0 is None or par1 is None else 100 * (par1 - par0) / tick / wall,
            'host_busy_pct_all_cores': host_pct,
            'other_host_pct_all_cores': None if host_pct is None else host_pct - (cgroup_pct + compositor_pct) / cpus,
            'other_host_max_window_pct_all_cores': max(window),
            # The sampler runs outside the owned cgroup; its own CPU is the instrument's host overhead.
            'instrument_self_cpu_pct_one_core': 100 * (time.process_time() - self0) / wall,
            'driver': holder.get('value')}


def run_invalid_reasons(record, name):
    """Why a run cannot contribute the named interval to a valid A/A pair (empty list: valid)."""
    reasons = []
    if record.get('status') != 'COMPLETED':
        reasons.append('run status ' + str(record.get('status')))
    for flag in ('realize_mismatch', 'adopt_mismatch', 'not_quiescent'):
        if record.get(flag):
            reasons.append(flag)
    i = record.get('intervals', {}).get(name)
    if not i:
        reasons.append('interval missing')
        return reasons
    d = i.get('driver')
    if isinstance(d, dict) and 'error' in d:
        reasons.append('driver error')
    elif isinstance(d, dict) and d.get('scheduled'):
        if d['delivered'] < d['scheduled'] or d.get('failed'):
            reasons.append('lost workload events')
        if d['late'] > LATE_TOLERANCE * d['scheduled']:
            reasons.append('late workload events')
    if (i.get('other_host_max_window_pct_all_cores') or 0) > record.get('interference_pct', 5.0):
        reasons.append('foreign host load')
    return reasons


def one_run(binary, profile_name, settings, run_label, owned_root):
    owned = Path(tempfile.mkdtemp(prefix=run_label + '-', dir=owned_root)).resolve()
    profile = owned / 'profile'; profile.mkdir()

    class Local(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *_args): pass
        def do_GET(self):
            if self.path.split('?')[0] not in {'/article.html'}: self.send_error(404); return
            super().do_GET()
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Local, directory=str(SOURCE / 'pages')))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    with socket.socket() as s: s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]
    prefs = {'marionette.port': port, 'browser.shell.checkDefaultBrowser': False,
        'browser.startup.homepage': 'about:blank', 'browser.aboutwelcome.enabled': False,
        'browser.startup.homepage_override.mstone': 'ignore', 'browser.newtabpage.enabled': False,
        'browser.tabs.warnOnClose': False, 'browser.warnOnQuit': False, 'app.update.auto': False,
        'app.update.disabledForTesting': True, 'datareporting.policy.dataSubmissionEnabled': False,
        'toolkit.telemetry.enabled': False, 'network.proxy.type': 1, 'network.proxy.http': '127.0.0.1',
        'network.proxy.http_port': 9, 'network.proxy.ssl': '127.0.0.1', 'network.proxy.ssl_port': 9,
        'network.proxy.no_proxies_on': 'localhost, 127.0.0.1', 'privacy.userContext.enabled': True,
        # Realization ends with a normal quit and native session restore (restore on demand).
        'browser.startup.page': 3, 'browser.sessionstore.restore_on_demand': True,
        # The workload driver must keep its schedule even when its tab is in the background.
        'dom.min_background_timeout_value': 4, 'dom.timeout.enable_budget_timer_throttling': False,
        'dom.min_background_timeout_value_without_budget_throttling': 4}
    (profile / 'user.js').write_text(''.join('user_pref(' + json.dumps(k) + ', ' + json.dumps(v) + ');\n' for k, v in prefs.items()))
    manifest = {'manifest_version': 3, 'name': 'F01 calibration ONLY', 'version': '0.0.1', 'incognito': 'not_allowed',
        'browser_specific_settings': {'gecko': {'id': ID, 'strict_min_version': '156.0', 'data_collection_permissions': {'required': ['none']}}},
        'permissions': ['tabs', 'tabGroups', 'cookies', 'contextualIdentities']}
    package = owned / 'calibration.xpi'
    with zipfile.ZipFile(package, 'x') as z:
        for name, content in {'manifest.json': json.dumps(manifest), 'driver.js': DRIVER,
                              'driver.html': '<!doctype html><meta charset="utf-8"><title>F01 calibration driver</title><script src="driver.js"></script>'}.items():
            info = zipfile.ZipInfo(name, (2026, 10, 2, 0, 0, 0)); info.external_attr = 0o100644 << 16; z.writestr(info, content)
    rows = fixtures.profile(int(profile_name[1:]))['tabs']
    base = f'http://127.0.0.1:{server.server_port}/article.html'
    for r in rows:
        r['url'] = r['url'].replace('http://127.0.0.1:8000/article.html', base)
    record = {'run': run_label, 'profile': profile_name, 'addon_under_test': 'NONE_A_A_CALIBRATION',
              'probe_sha256': digest(package), 'fixture_tabs': len(rows), 'settings': settings, 'intervals': {}}
    proc = client = None

    def launch(log):
        command = [str(binary), '--no-remote', '--new-instance', '--profile', str(profile), '--marionette', '--remote-allow-system-access']
        p = UserCgroupProcess(command, owned / log); c = None
        deadline = time.monotonic() + 90
        while time.monotonic() < deadline:
            if p.poll() is not None: raise RuntimeError('owned browser exited')
            try: c = Marionette(port); break
            except (ConnectionRefusedError, TimeoutError): time.sleep(.2)
        if c is None: raise TimeoutError('owned protocol absent')
        session = c.command('WebDriver:NewSession', {'capabilities': {'alwaysMatch': {}}})
        caps = session.get('capabilities', session.get('value', {}).get('capabilities', {}))
        if caps.get('moz:processID') != p.pid or Path(caps['moz:profile']).resolve() != profile:
            raise ValueError('owned PID/profile mismatch')
        # Marionette applies the session script timeout, not a per-call value.
        c.command('WebDriver:SetTimeouts', {'script': 900000})
        c.command('Addon:Install', {'path': str(package), 'temporary': True})
        url = execute(c, 'return WebExtensionPolicy.getByID(arguments[0]).getURL("driver.html");', [ID])
        c.command('Marionette:SetContext', {'value': 'content'})
        # Never navigate a restored fixture tab: the driver always gets its own new tab.
        handle = c.command('WebDriver:NewWindow', {'type': 'tab', 'focus': True})
        handle = handle.get('handle', handle.get('value', {}).get('handle')) if isinstance(handle, dict) else handle
        c.command('WebDriver:SwitchToWindow', {'handle': handle, 'focus': True})
        c.command('WebDriver:Navigate', {'url': url})
        return p, c

    try:
        proc, client = launch('firefox-realize.log'); record['cgroup_realize'] = str(proc.group)
        t0 = time.monotonic(); record['realize'] = api(client, 'realize', {'tabs': rows}); record['realize']['seconds'] = time.monotonic() - t0
        expected_windows = len({r['window'] for r in rows})
        # The immediate workload count is a snapshot while tabs initialize; the restored count is binding.
        if record['realize'].get('created') != len(rows) or record['realize'].get('windows') != expected_windows:
            record['realize_mismatch'] = True
        time.sleep(60)
        # F01 platform finding: API-created discarded tabs in groups load the parent process.
        record['intervals']['api_realized_settled_10s'] = interval(proc, 10, parent_pid=proc.pid)
        client.command('Marionette:Quit', {'flags': ['eAttemptQuit']}); proc.wait(90); client.close(); client = None
        proc, client = launch('firefox.log'); record['cgroup'] = str(proc.group)
        time.sleep(15)
        record['adopted'] = api(client, 'adopt')
        record['adopted']['missingSyntheticIds'] = sorted(set(r['syntheticId'] for r in rows) - set(record['adopted'].pop('syntheticIds')))
        expected_groups = len({(r['window'], r['group']) for r in rows if r['group'] is not None and not r['pinned']})
        record['expected_groups'] = expected_groups
        if (record['adopted']['missingSyntheticIds'] or record['adopted'].get('groups') != expected_groups
                or record['adopted'].get('containers', 0) < 3):
            record['adopt_mismatch'] = True
        time.sleep(settings['warmup'])
        record['intervals']['native_restored_settled_10s'] = interval(proc, 10, parent_pid=proc.pid)
        record['front'] = api(client, 'front')
        if not record['front'].get('ok'):
            record['adopt_mismatch'] = True
        # Declared measurement condition: minimize (GC/CC/purge) once before the CPU intervals,
        # then a quiescence acknowledgement instead of a bare timer.
        execute(client, 'const done=arguments[arguments.length-1];Cc["@mozilla.org/memory-reporter-manager;1"].getService(Ci.nsIMemoryReporterManager).minimizeMemoryUsage(()=>done(true));', async_script=True)
        record['quiescence'] = []
        for _ in range(QUIESCENT_ATTEMPTS):
            q = interval(proc, 10); record['quiescence'].append(q['cgroup_cpu_pct_one_core'])
            if q['cgroup_cpu_pct_one_core'] < QUIESCENT_PCT:
                break
        else:
            record['not_quiescent'] = True
        record['intervals']['pre_host_30s'] = interval(proc, 30)
        l10 = fixtures.schedule('L10'); l10 = [e for e in l10 if e['at_ms'] < settings['l10_seconds'] * 1000]
        record['intervals']['L10'] = interval(proc, settings['l10_seconds'] + 1,
                                              lambda: api(client, 'run-schedule', {'kind': 'L10', 'schedule': l10}))
        record['intervals']['B300'] = interval(proc, 10, lambda: api(client, 'run-schedule',
                                                                       {'kind': 'B300', 'schedule': fixtures.schedule('B300')}))
        if settings['idle_seconds']:
            record['intervals']['idle'] = interval(proc, settings['idle_seconds'])
        if settings['reuse_trials']:
            ext = extension_process(client, proc.pid)
            if str(ext) not in (proc.group / 'cgroup.procs').read_text().split():
                raise RuntimeError('extension process outside the owned cgroup')
            minimize = lambda: execute(client, 'const done=arguments[arguments.length-1];Cc["@mozilla.org/memory-reporter-manager;1"].getService(Ci.nsIMemoryReporterManager).minimizeMemoryUsage(()=>done(true));', async_script=True)
            trials = []
            order = settings['reuse_order']
            for kind in order:
                minimize()
                if kind != 'fresh-control':
                    api(client, 'hold-strings', 32); api(client, 'drop')
                    if kind == 'with-minimize':
                        minimize()
                reset_high_water(ext); h0 = status_kib(ext, 'VmHWM')
                api(client, 'pulse-strings', 24); h1 = status_kib(ext, 'VmHWM')
                trials.append({'kind': kind, 'hwm_delta_bytes': (h1 - h0) * 1024})
            record['reuse_trials'] = trials
        record['status'] = 'COMPLETED'
        client.command('Marionette:Quit', {'flags': ['eForceQuit']}); proc.wait(30)
    except Exception as error:
        record['status'] = 'FAILED'; record['error'] = repr(error)
    finally:
        if client: client.close()
        if proc and proc.poll() is None: proc.terminate(); proc.wait(20)
        server.shutdown(); server.server_close()
        record['cleanup'] = 'OWN_PROCESS_REMAINS' if proc and proc.poll() is None else 'OWN_PROFILE_REMOVED__OWN_CGROUP_EXITED'
        if record['cleanup'] != 'OWN_PROCESS_REMAINS':
            shutil.rmtree(profile)
        (owned / 'run.json').write_text(json.dumps(record, indent=2) + '\n')
    return record


def summarize(runs, interference_pct):
    """Pair differences (second minus first) per interval; every invalid pair is listed with reasons."""
    out = {}
    for run in runs:
        run.setdefault('interference_pct', interference_pct)
    for name in ('L10', 'B300', 'idle'):
        diffs, invalid = [], []
        for a, b in zip(runs[0::2], runs[1::2]):
            if all(r.get('status') == 'COMPLETED' and name not in r.get('intervals', {}) for r in (a, b)):
                continue  # Interval not part of this calibration (e.g. idle disabled).
            reasons = {r['run']: run_invalid_reasons(r, name) for r in (a, b)}
            if any(reasons.values()):
                ia, ib = (r.get('intervals', {}).get(name) for r in (a, b))
                diff = ib['cgroup_cpu_pct_one_core'] - ia['cgroup_cpu_pct_one_core'] if ia and ib else None
                invalid.append({'diff': diff, 'reasons': {k: v for k, v in reasons.items() if v}})
            else:
                diffs.append(b['intervals'][name]['cgroup_cpu_pct_one_core'] - a['intervals'][name]['cgroup_cpu_pct_one_core'])
        out[name] = {'valid_pair_diffs_pct_one_core': diffs, 'invalid': invalid,
                     'median': statistics.median(diffs) if diffs else None,
                     'max_abs': max(abs(x) for x in diffs) if diffs else None,
                     'stdev': statistics.stdev(diffs) if len(diffs) > 1 else None}
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--firefox', type=Path, required=True)
    parser.add_argument('--firefox-sha256', required=True)
    parser.add_argument('--profile', choices=['R500', 'R2000'], required=True)
    parser.add_argument('--pairs', type=int, default=5)
    parser.add_argument('--l10-seconds', type=int, default=600)
    parser.add_argument('--idle-seconds', type=int, default=None)
    parser.add_argument('--warmup', type=int, default=60)
    parser.add_argument('--interference-pct', type=float, default=5.0)
    args = parser.parse_args()
    if platform.system() != 'Linux' or not os.environ.get('WAYLAND_DISPLAY'):
        raise ValueError('this calibration instrument requires the visible Ubuntu Wayland desktop')
    binary = args.firefox.resolve(strict=True)
    if digest(binary) != args.firefox_sha256:
        raise ValueError('binary hash mismatch')
    ini = configparser.ConfigParser(); ini.read(binary.parent / 'application.ini')
    if ini['App']['Version'] != '156.0':
        raise ValueError('Firefox 156 required')
    idle = args.idle_seconds if args.idle_seconds is not None else 600  # Idle belongs to the protocol for both profiles.
    (ROOT / 'build/f01/runs').mkdir(parents=True, exist_ok=True)
    owned_root = Path(tempfile.mkdtemp(prefix='calibration-' + args.profile + '-', dir=ROOT / 'build/f01/runs')).resolve()
    orders = [['without-minimize', 'with-minimize', 'fresh-control'], ['fresh-control', 'with-minimize', 'without-minimize'],
              ['with-minimize', 'fresh-control', 'without-minimize']]
    runs = []
    for pair in range(args.pairs):
        for half in range(2):
            index = pair * 2 + half
            settings = {'warmup': args.warmup, 'l10_seconds': args.l10_seconds, 'idle_seconds': idle,
                        'reuse_trials': True, 'reuse_order': orders[index % len(orders)]}
            runs.append(one_run(binary, args.profile, settings, 'p%d-%s' % (pair, 'first' if half == 0 else 'second'), owned_root))
    report = {'evidence_class': 'UBUNTU_RUNTIME_VERIFIED', 'qualification_only': True, 'kind': 'A_A_CALIBRATION',
              'host': platform.node(), 'os': platform.platform(), 'cpus': os.cpu_count(),
              'session': {k: os.environ.get(k) for k in ('XDG_SESSION_TYPE', 'XDG_CURRENT_DESKTOP')},
              'firefox': {'version': ini['App']['Version'], 'build_id': ini['App']['BuildID'], 'binary_sha256': digest(binary)},
              'driver_sources': preserve_driver_sources(owned_root), 'calibration_probe_sha256': digest(Path(__file__)),
              'profile': args.profile, 'pairs': args.pairs, 'interference_pct': args.interference_pct,
              'runs': runs, 'summary': summarize(runs, args.interference_pct),
              'semantics': 'A/A pair differences estimate noise of the bound CPU protocol; not a WindowSafe result.'}
    (owned_root / 'calibration.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'report': str(owned_root / 'calibration.json'), 'summary': report['summary'],
                      'statuses': [r['status'] for r in runs]}))


if __name__ == '__main__':
    main()
