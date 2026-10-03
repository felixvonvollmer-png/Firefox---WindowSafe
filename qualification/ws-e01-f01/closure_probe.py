"""F01 closure probe on the visible Ubuntu desktop; synthetic disposable profile only.

Covers the remaining F01 scope after WS-P05: ordinary-window fallback for API-normal
WebApp windows, per-transition display/geometry/state observations, and memory-method
qualification (reporter coverage contrasts and an extension-process high-water bound).
Native chrome automation is TEST_ONLY fixture control, never a product capability.
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
import tempfile
import threading
import time
import zipfile

from run_probe import Marionette, UserCgroupProcess, digest, preserve_driver_sources
from target_probe import MEMORY, execute

ROOT = Path(__file__).resolve().parents[2]
SOURCE = Path(__file__).resolve().parent
ID = 'f01-closure@windowsafe.invalid'
WEBAPP_ID = 'c930c827-57af-4119-a8e6-88808019f001'
MIB = 1024 * 1024
DRIVER = r'''
const tab = t => ({id:t.id, windowId:t.windowId, index:t.index, url:t.url, title:t.title, active:t.active,
  pinned:t.pinned, discarded:t.discarded, muted:t.mutedInfo?.muted, incognito:t.incognito,
  cookieStoreId:t.cookieStoreId, groupId:t.groupId, hidden:t.hidden});
const win = w => ({id:w.id, type:w.type, state:w.state, incognito:w.incognito, left:w.left, top:w.top,
  width:w.width, height:w.height, focused:w.focused, tabs:(w.tabs||[]).map(tab)});
const wait = ms => new Promise(r => setTimeout(r, ms));
window.closureOperation = async (op, arg) => {
  if (op === 'snapshot') return (await browser.windows.getAll({populate:true})).map(win);
  if (op === 'create') return win(await browser.windows.create(arg));
  if (op === 'update') {
    // Bounded wait: on Wayland the minimized update promise may never resolve.
    const requested = arg.spec;
    const promise = await Promise.race([browser.windows.update(arg.id, requested).then(() => 'RESOLVED'),
                                        wait(3000).then(() => 'TIMEOUT_3S')]);
    const immediate = win(await browser.windows.get(arg.id));
    // Read back until three consecutive equal observations (100 ms apart) or 3 s: avoids a settle race.
    let settled = immediate, stable = 0;
    for (let i = 0; i < 30 && stable < 2; i++) {
      await wait(100);
      const next = win(await browser.windows.get(arg.id));
      stable = ['state','left','top','width','height'].every(k => next[k] === settled[k]) ? stable + 1 : 0;
      settled = next;
    }
    return {requested, promise, immediate, settled, settledStable: stable >= 2};
  }
  if (op === 'remove') { await browser.windows.remove(arg); return true; }
  if (op === 'ordinary-restore') {
    // Product-shaped fallback: one ordinary window, active tab loaded, background tabs discarded.
    const [first, ...rest] = arg;
    const w = await browser.windows.create({type:'normal', url:first.url});
    for (const t of rest) await browser.tabs.create({windowId:w.id, url:t.url, active:false, discarded:true,
      title:t.title, pinned:false});
    await wait(300);
    return win(await browser.windows.get(w.id, {populate:true}));
  }
  if (op === 'map-cache') {
    // Flat, distinct 1024-character strings: padEnd/repeat would create shared ropes, not real bytes.
    window.fixtureCache = new Map(); const b = new Uint8Array(512);
    for (let i = 0; i < arg; i++) { crypto.getRandomValues(b);
      window.fixtureCache.set('k' + i, Array.from(b, x => x.toString(16).padStart(2, '0')).join('')); }
    return {entries:window.fixtureCache.size, logicalStringBytes:arg * 1024};
  }
  if (op === 'idb-fill') {
    const db = await new Promise((ok, err) => { const r = indexedDB.open('f01-closure', 1);
      r.onupgradeneeded = () => r.result.createObjectStore('s'); r.onsuccess = () => ok(r.result); r.onerror = () => err(r.error); });
    await new Promise((ok, err) => { const tx = db.transaction('s', 'readwrite', {durability:'strict'});
      const b = new Uint8Array(512);
      for (let i = 0; i < arg; i++) { crypto.getRandomValues(b);
        tx.objectStore('s').put(Array.from(b, x => x.toString(16).padStart(2, '0')).join(''), i); }
      tx.oncomplete = ok; tx.onerror = () => err(tx.error); });
    window.fixtureDb = db;
    window.fixtureRead = await new Promise((ok, err) => { const r = db.transaction('s').objectStore('s').getAll();
      r.onsuccess = () => ok(r.result); r.onerror = () => err(r.error); });
    return {records:window.fixtureRead.length, logicalBytes:arg * 1024};
  }
  if (op === 'release') {
    delete window.fixtureCache; delete window.fixtureRead;
    if (window.fixtureDb) { window.fixtureDb.close(); delete window.fixtureDb; }
    return {released:true};
  }
  if (op === 'hold-strings') {
    // Many small flat strings: the GC-heap/allocator case where freed memory can stay resident.
    window.held = []; const b = new Uint8Array(512);
    for (let i = 0; i < arg * 1024; i++) { crypto.getRandomValues(b);
      window.held.push(Array.from(b, x => x.toString(16).padStart(2, '0')).join('')); }
    return {strings:window.held.length};
  }
  if (op === 'drop') { delete window.held; return {dropped:true}; }
  if (op === 'pulse-strings') {
    const x = []; const b = new Uint8Array(512);
    for (let i = 0; i < arg * 1024; i++) { crypto.getRandomValues(b);
      x.push(Array.from(b, y => y.toString(16).padStart(2, '0')).join('')); }
    await wait(50);
    return {strings:x.length, logicalStringBytes:x.length * 1024};
  }
  if (op === 'pulse') {
    // Held only for the duration of this call; a point sample afterwards cannot see it.
    const x = new Uint8Array(arg * 1024 * 1024); x.fill(42); await wait(50);
    return {logicalAllocationBytes:x.byteLength};
  }
  throw Error('unknown finite closure operation');
};
'''
TOPOLOGY = r'''
const sm = Cc["@mozilla.org/gfx/screenmanager;1"].getService(Ci.nsIScreenManager);
const rect = s => { const x={},y={},w={},h={},ax={},ay={},aw={},ah={};
  s.GetRectDisplayPix(x,y,w,h); s.GetAvailRectDisplayPix(ax,ay,aw,ah);
  return {x:x.value,y:y.value,width:w.value,height:h.value,
    avail:{x:ax.value,y:ay.value,width:aw.value,height:ah.value},
    scale:s.contentsScaleFactor, defaultCSSScale:s.defaultCSSScaleFactor}; };
let protocol = null; try { protocol = Cc["@mozilla.org/gfx/info;1"].getService(Ci.nsIGfxInfo).windowProtocol; } catch (e) { protocol = 'UNAVAILABLE: ' + e; }
return {screensIterable: typeof sm.screens, primary: rect(sm.primaryScreen),
  forOrigin: rect(sm.screenForRect(0, 0, 1, 1)), forFarAway: rect(sm.screenForRect(-10000, -10000, 1, 1)),
  windowProtocol: protocol, devicePixelRatio: window.devicePixelRatio,
  screen: {width: screen.width, height: screen.height, availWidth: screen.availWidth, availHeight: screen.availHeight,
    left: screen.left, top: screen.top}};
'''


def api(client, operation, arg=None):
    return json.loads(execute(client,
        'const done=arguments[arguments.length-1]; window.wrappedJSObject.closureOperation(arguments[0],arguments[1])'
        '.then(x=>done(JSON.stringify(x)),e=>done(JSON.stringify({error:String(e)})));',
        [operation, arg], chrome=False, async_script=True))


def extension_process(client, root_pid):
    """The single WebExtension child per Firefox process info; caller verifies owned-cgroup membership."""
    info = execute(client, 'const done=arguments[arguments.length-1];ChromeUtils.requestProcInfo().then('
                   'i=>done(i.children.map(c=>({pid:c.pid,type:c.type}))),e=>done({error:String(e)}));',
                   async_script=True)
    found = [c['pid'] for c in info if c['type'] == 'extension']
    if len(found) != 1:
        raise RuntimeError('expected exactly one extension process, found %r' % info)
    pid, tree = found[0], [root_pid]
    while tree:
        current = tree.pop()
        if current == pid:
            return pid
        task = Path('/proc', str(current), 'task')
        for t in task.iterdir() if task.exists() else []:
            tree.extend(int(k) for k in (t / 'children').read_text().split())
    # Forkserver children are not descendants of the main process; accept only the owned cgroup.
    return pid


def status_kib(pid, field):
    for line in Path('/proc', str(pid), 'status').read_text().splitlines():
        if line.startswith(field + ':'):
            return int(line.split()[1])
    raise RuntimeError(field + ' unavailable')


def reset_high_water(pid):
    # Writing 5 resets the peak RSS (VmHWM) of an own process to its current RSS (Linux >= 4.0).
    Path('/proc', str(pid), 'clear_refs').write_text('5')


def origin_explicit(rows, origin):
    """Disjoint explicit leaves of the extension origin, grouped by subsystem."""
    groups = {}
    for r in rows:
        if r['units'] == 0 and r['path'].startswith('explicit/') and origin in r['path']:
            key = ('js' if '/js-' in r['path'] or '/js/' in r['path'] else 'dom' if '/dom/' in r['path'] else 'other')
            groups[key] = groups.get(key, 0) + r['amount']
    groups['total'] = sum(v for k, v in groups.items())
    return groups


def process_explicit(rows, pid):
    """All explicit leaves of the dedicated extension process: JS zones (incl. strings) and DOM."""
    tag = '(pid %d)' % pid
    leaves = [r for r in rows if tag in r['process'] and r['units'] == 0 and r['path'].startswith('explicit/')]
    return {'total': sum(r['amount'] for r in leaves),
            'strings': sum(r['amount'] for r in leaves if '/strings' in r['path']),
            'js': sum(r['amount'] for r in leaves if r['path'].startswith('explicit/js-')),
            'process_names': sorted({r['process'] for r in leaves})}


def storage_rows(rows):
    """Explicit storage-like leaves across ALL processes (IndexedDB/storage paths); coarse context only."""
    return sum(r['amount'] for r in rows if r['units'] == 0 and r['path'].startswith('explicit/')
               and ('indexeddb' in r['path'].lower() or 'idb' in r['path'].lower() or '/storage/' in r['path']))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--firefox', type=Path, required=True)
    parser.add_argument('--firefox-sha256', required=True)
    args = parser.parse_args()
    if platform.system() != 'Linux' or not os.environ.get('WAYLAND_DISPLAY'):
        raise ValueError('this closure instrument requires the visible Ubuntu Wayland desktop')
    binary = args.firefox.resolve(strict=True)
    if digest(binary) != args.firefox_sha256:
        raise ValueError('binary hash mismatch')
    ini = configparser.ConfigParser(); ini.read(binary.parent / 'application.ini')
    if ini['App']['Version'] != '156.0' or '"release"' not in (binary.parent / 'defaults/pref/channel-prefs.js').read_text():
        raise ValueError('official Stable 156 required')
    (ROOT / 'build/f01/runs').mkdir(parents=True, exist_ok=True)
    owned = Path(tempfile.mkdtemp(prefix='closure-', dir=ROOT / 'build/f01/runs')).resolve()
    profile = owned / 'profile'; profile.mkdir()

    class Local(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *_args): pass
        def do_GET(self):
            if self.path.split('?')[0] not in {'/article.html', '/video.html'}: self.send_error(404); return
            super().do_GET()
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Local, directory=str(SOURCE / 'pages')))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    url = f'http://127.0.0.1:{server.server_port}/article.html'
    webapp = profile / 'taskbartabs'; webapp.mkdir()
    (webapp / 'taskbartabs.json').write_text(json.dumps({'version': 1, 'taskbarTabs': [{
        'id': WEBAPP_ID, 'scopes': [{'hostname': '127.0.0.1'}], 'userContextId': 0,
        'startUrl': url + '?webapp=1', 'name': 'F01 synthetic disposable'}]}))
    with socket.socket() as s: s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]
    prefs = {'marionette.port': port, 'browser.shell.checkDefaultBrowser': False, 'browser.startup.page': 0,
        'browser.startup.homepage': 'about:blank', 'browser.aboutwelcome.enabled': False,
        'browser.startup.homepage_override.mstone': 'ignore', 'startup.homepage_welcome_url': '',
        'startup.homepage_welcome_url.additional': '', 'browser.newtabpage.enabled': False,
        'browser.tabs.warnOnClose': False, 'browser.warnOnQuit': False,
        'app.update.auto': False, 'app.update.disabledForTesting': True,
        'datareporting.policy.dataSubmissionEnabled': False, 'toolkit.telemetry.enabled': False,
        'network.proxy.type': 1, 'network.proxy.http': '127.0.0.1', 'network.proxy.http_port': 9,
        'network.proxy.ssl': '127.0.0.1', 'network.proxy.ssl_port': 9, 'network.proxy.no_proxies_on': 'localhost, 127.0.0.1',
        'network.dns.disablePrefetch': True, 'network.prefetch-next': False, 'browser.taskbarTabs.enabled': True}
    (profile / 'user.js').write_text(''.join('user_pref(' + json.dumps(k) + ', ' + json.dumps(v) + ');\n' for k, v in prefs.items()))
    manifest = {'manifest_version': 3, 'name': 'F01 closure qualification ONLY', 'version': '0.0.1', 'incognito': 'not_allowed',
        'browser_specific_settings': {'gecko': {'id': ID, 'strict_min_version': '156.0', 'data_collection_permissions': {'required': ['none']}}},
        'permissions': ['tabs', 'unlimitedStorage']}
    package = owned / 'closure.xpi'
    with zipfile.ZipFile(package, 'x') as z:
        for name, content in {'manifest.json': json.dumps(manifest), 'driver.js': DRIVER,
                              'driver.html': '<!doctype html><meta charset="utf-8"><title>F01 closure driver</title><script src="driver.js"></script>'}.items():
            info = zipfile.ZipInfo(name, (2026, 10, 1, 0, 0, 0)); info.external_attr = 0o100644 << 16; z.writestr(info, content)
    record = {'evidence_class': 'UBUNTU_RUNTIME_VERIFIED', 'qualification_only': True, 'host': platform.node(),
        'os': platform.platform(), 'session': {k: os.environ.get(k) for k in ('XDG_SESSION_TYPE', 'XDG_CURRENT_DESKTOP', 'WAYLAND_DISPLAY', 'DISPLAY')},
        'driver_sources': preserve_driver_sources(owned), 'closure_probe_sha256': digest(Path(__file__)),
        'version': ini['App']['Version'], 'build_id': ini['App']['BuildID'], 'binary': str(binary), 'binary_sha256': digest(binary),
        'profile_class': 'NEW_SYNTHETIC_DISPOSABLE', 'probe_sha256': digest(package), 'observations': [], 'cleanup': 'PENDING'}
    proc = client = None

    def observe(name, fn):
        try:
            value = fn()
            outcome = 'OPEN' if isinstance(value, dict) and 'error' in value else 'OBSERVED'
            record['observations'].append({'name': name, 'outcome': outcome, 'value': value}); return value
        except Exception as error:
            record['observations'].append({'name': name, 'outcome': 'OPEN', 'error': repr(error)}); return None

    def minimize():
        execute(client, 'const done=arguments[arguments.length-1];Cc["@mozilla.org/memory-reporter-manager;1"]'
                '.getService(Ci.nsIMemoryReporterManager).minimizeMemoryUsage(()=>done(true));', async_script=True)

    def reports(label, minimize_first=True):
        if minimize_first:
            minimize()
        rows = execute(client, MEMORY, async_script=True)
        artifact = owned / (label + '-memory.json'); artifact.write_text(json.dumps(rows) + '\n')
        return rows, digest(artifact)

    try:
        command = [str(binary), '--no-remote', '--new-instance', '--profile', str(profile), '--marionette', '--remote-allow-system-access']
        proc = UserCgroupProcess(command, owned / 'firefox.log'); record.update(pid=proc.pid, command=command, cgroup=str(proc.group))
        deadline = time.monotonic() + 45
        while time.monotonic() < deadline:
            if proc.poll() is not None: raise RuntimeError('owned browser exited')
            try: client = Marionette(port); break
            except (ConnectionRefusedError, TimeoutError): time.sleep(.2)
        if client is None: raise TimeoutError('owned protocol absent')
        session = client.command('WebDriver:NewSession', {'capabilities': {'alwaysMatch': {}}})
        caps = session.get('capabilities', session.get('value', {}).get('capabilities', {}))
        if caps.get('moz:processID') != proc.pid or Path(caps['moz:profile']).resolve() != profile:
            raise ValueError('owned PID/profile mismatch')
        client.command('Addon:Install', {'path': str(package), 'temporary': True})
        extension_url = execute(client, 'return WebExtensionPolicy.getByID(arguments[0]).getURL("driver.html");', [ID])
        client.command('Marionette:SetContext', {'value': 'content'}); client.command('WebDriver:Navigate', {'url': extension_url})
        origin = extension_url.split('/')[2]
        record['extension_origin_host'] = origin

        # 1. Display topology and per-transition geometry/state.
        observe('display-topology', lambda: execute(client, TOPOLOGY))
        created = observe('geometry-create', lambda: api(client, 'create', {'url': url, 'type': 'normal', 'left': 60, 'top': 70, 'width': 900, 'height': 650}))
        if created and 'id' in created:
            for step, spec in enumerate([{'state': 'maximized'}, {'state': 'normal'}, {'state': 'minimized'}, {'state': 'normal'},
                                         {'state': 'fullscreen'}, {'state': 'normal'}, {'left': 200, 'top': 150, 'width': 800, 'height': 600},
                                         {'left': -1800, 'top': 80, 'width': 850, 'height': 600},
                                         {'left': -10000, 'top': -10000, 'width': 850, 'height': 600}]):
                observe('geometry-step-%d' % step, lambda spec=spec: api(client, 'update', {'id': created['id'], 'spec': spec}))
            observe('geometry-remove', lambda: api(client, 'remove', created['id']))

        # 2. WS-P05: API-normal WebApp window, public data and ordinary-window restore target.
        observe('webapp-native-open', lambda: execute(client, 'const done=arguments[arguments.length-1];(async()=>{const {TaskbarTabs}=ChromeUtils.importESModule("resource:///modules/taskbartabs/TaskbarTabs.sys.mjs");const t=await TaskbarTabs.getTaskbarTab(arguments[0]);window.f01WebApp=await TaskbarTabs.openWindow(t);done({type:window.f01WebApp.document.documentElement.getAttribute("windowtype"),taskbarTab:window.f01WebApp.document.documentElement.getAttribute("taskbartab"),tabs:window.f01WebApp.gBrowser.tabs.length});})().catch(e=>done({error:String(e)}));', [WEBAPP_ID], async_script=True))
        time.sleep(1.5)
        windows = observe('webapp-api-snapshot', lambda: api(client, 'snapshot'))
        webapp_windows = [w for w in windows or [] if any('webapp=1' in (t['url'] or '') for t in w['tabs'])]
        record['webapp_public_view'] = webapp_windows
        if len(webapp_windows) == 1:
            observe('webapp-ordinary-restore', lambda: api(client, 'ordinary-restore', webapp_windows[0]['tabs'] + [{'url': url + '?second=1', 'title': 'synthetic'}]))
            observe('native-window-kinds', lambda: execute(client, 'return Array.from(Services.wm.getEnumerator("navigator:browser")).map(w=>({taskbarTab:w.document.documentElement.getAttribute("taskbartab"),tabs:w.gBrowser.tabs.length,urls:w.gBrowser.tabs.map(t=>t.linkedBrowser.currentURI.spec)}));'))
        observe('webapp-native-close', lambda: execute(client, 'if(window.f01WebApp){window.f01WebApp.close();return true;}return false;'))

        # 3. Memory-method qualification: reporter coverage contrasts and extension-process high-water bound.
        time.sleep(2)
        ext_pid = extension_process(client, proc.pid)
        if str(ext_pid) not in (proc.group / 'cgroup.procs').read_text().split():
            raise RuntimeError('extension process outside the owned cgroup')
        record['extension_process'] = {'pid': ext_pid, 'in_owned_cgroup': True}
        rows, base_hash = reports('m0-baseline'); base = origin_explicit(rows, origin); base_idb = storage_rows(rows)
        memory = {'baseline': {'origin_explicit': base, 'process_explicit': process_explicit(rows, ext_pid),
                               'storage_explicit_all_processes': base_idb, 'report_sha256': base_hash,
                               'rss_kib': status_kib(ext_pid, 'VmRSS')}}
        observe('map-cache-8mib', lambda: api(client, 'map-cache', 8192))
        rows, h = reports('m1-map-cache'); memory['map_cache_held'] = {'origin_explicit': origin_explicit(rows, origin), 'process_explicit': process_explicit(rows, ext_pid), 'report_sha256': h}
        observe('idb-fill-8mib', lambda: api(client, 'idb-fill', 8192))
        rows, h = reports('m2-idb'); memory['idb_held'] = {'origin_explicit': origin_explicit(rows, origin), 'process_explicit': process_explicit(rows, ext_pid),
                                                           'storage_explicit_all_processes': storage_rows(rows), 'report_sha256': h}
        observe('release', lambda: api(client, 'release'))
        time.sleep(1)
        rows, h = reports('m3-released'); memory['released'] = {'origin_explicit': origin_explicit(rows, origin), 'process_explicit': process_explicit(rows, ext_pid), 'report_sha256': h}
        rss_before = status_kib(ext_pid, 'VmRSS')
        rows, h = reports('m4-before-pulse', minimize_first=False); before_pulse = process_explicit(rows, ext_pid)
        minimize()  # Measurement condition: minimize immediately before the reset, nothing in between.
        reset_high_water(ext_pid); hwm_reset = status_kib(ext_pid, 'VmHWM')
        observe('pulse-24mib', lambda: api(client, 'pulse', 24))
        rows, h = reports('m5-after-pulse'); after_pulse = process_explicit(rows, ext_pid)
        hwm_after = status_kib(ext_pid, 'VmHWM')
        memory['pulse'] = {'logical_bytes': 24 * MIB, 'rss_before_kib': rss_before, 'hwm_after_reset_kib': hwm_reset,
                           'hwm_after_pulse_kib': hwm_after, 'hwm_delta_bytes': (hwm_after - hwm_reset) * 1024,
                           'reporter_point_before': before_pulse, 'reporter_point_after': after_pulse,
                           'semantics': 'VmHWM delta after minimize+reset of the dedicated extension process; '
                                        'reporter point samples cannot see a held-only pulse. Bound validity is '
                                        'qualified only by the reuse trials below, not assumed.'}
        # Free-but-resident reuse: 32 MiB of small strings dropped, then a 24 MiB string pulse.
        for trial, clean in (('reuse-without-minimize', False), ('reuse-with-minimize', True)):
            observe(trial + '-hold', lambda: api(client, 'hold-strings', 32))
            observe(trial + '-drop', lambda: api(client, 'drop'))
            if clean:
                minimize()
            rss_reset = status_kib(ext_pid, 'VmRSS'); reset_high_water(ext_pid); hwm0 = status_kib(ext_pid, 'VmHWM')
            observe(trial + '-pulse', lambda: api(client, 'pulse-strings', 24))
            hwm1 = status_kib(ext_pid, 'VmHWM')
            memory[trial] = {'minimize_before_reset': clean, 'rss_at_reset_kib': rss_reset, 'hwm_at_reset_kib': hwm0,
                             'hwm_after_pulse_kib': hwm1, 'hwm_delta_bytes': (hwm1 - hwm0) * 1024,
                             'pulse_logical_string_bytes': 24 * MIB}
            minimize()
        record['memory'] = memory
        record['status'] = 'OBSERVATIONS_COLLECTED__NO_GATE_SELF_ACCEPTANCE'
        client.command('Marionette:Quit', {'flags': ['eForceQuit']}); proc.wait(20)
    except Exception as error:
        record['status'] = 'PROBE_FAILED'; record['error'] = repr(error)
    finally:
        if client: client.close()
        if proc and proc.poll() is None: proc.terminate(); proc.wait(15)
        server.shutdown(); server.server_close()
        if proc and proc.poll() is None: record['cleanup'] = 'OWN_PROCESS_REMAINS'
        else:
            shutil.rmtree(profile); record['cleanup'] = 'OWN_PROFILE_REMOVED__OWN_CGROUP_EXITED'
        (owned / 'evidence.json').write_text(json.dumps(record, indent=2) + '\n')
        print(json.dumps({'evidence': str(owned / 'evidence.json'), 'status': record['status'], 'cleanup': record['cleanup']}))
    if record['status'] == 'PROBE_FAILED': raise SystemExit(1)


if __name__ == '__main__':
    main()
