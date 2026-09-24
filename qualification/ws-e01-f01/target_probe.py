"""Ubuntu visible-desktop special-case and memory instrument probe; synthetic only.

Native chrome automation is privileged TEST_ONLY fixture creation. It is not an
extension API capability and must never be imported into product implementation.
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
from measure import sample

ROOT = Path(__file__).resolve().parents[2]
SOURCE = Path(__file__).resolve().parent
ID = 'f01-target@windowsafe.invalid'
DRIVER = r'''
const events = [];
browser.tabs.onUpdated.addListener((id, change) => events.push({id, change}));
const tab = t => ({id:t.id, windowId:t.windowId, active:t.active, incognito:t.incognito,
  pinned:t.pinned, discarded:t.discarded, muted:t.mutedInfo?.muted, hidden:t.hidden,
  cookieStoreId:t.cookieStoreId, groupId:t.groupId, splitViewId:t.splitViewId,
  isInReaderMode:t.isInReaderMode});
window.targetOperation = async (op, url) => {
  if(op === 'snapshot') return {windows:await browser.windows.getAll({populate:true}),
    tabs:(await browser.tabs.query({})).map(tab), events:events.slice(),
    privateAllowed:await browser.extension.isAllowedIncognitoAccess()};
  if(op === 'allocate') {
    window.fixtureBytes=new Uint8Array(4*1024*1024); window.fixtureBytes.fill(123);
    window.fixtureCache=new Map(Array.from({length:1024},(_,i)=>[i,'synthetic-'+i+'x'.repeat(256)]));
    for(let i=0;i<1000;i++){const e=document.createElement('p');e.textContent='synthetic node '+i;document.body.append(e);}
    return {typedArrayBytes:window.fixtureBytes.byteLength,domNodes:1000,cacheEntries:1024};
  }
  if(op === 'pulse') {
    const x=new Uint8Array(12*1024*1024);x.fill(42);
    return {logicalAllocationBytes:x.byteLength,heldUntilReturn:true,hardPeakProof:false};
  }
  if(op === 'release') {delete window.fixtureBytes;delete window.fixtureCache;document.body.replaceChildren();return {released:true};}
  if(op === 'geometry') {
    const w=await browser.windows.create({url,type:'normal',left:60,top:70,width:900,height:650});
    const rows=[];
    try {
      for(const state of ['normal','maximized','minimized','normal','fullscreen','normal']) {
        await browser.windows.update(w.id,{state});
        for(let i=0;i<40;i++){if((await browser.windows.get(w.id)).state===state)break;await new Promise(r=>setTimeout(r,50));}
        rows.push({requested:state,result:await browser.windows.get(w.id)});
      }
      for(const bounds of [{left:-1800,top:80,width:850,height:600},{left:-10000,top:-10000,width:850,height:600}]) {
        await browser.windows.update(w.id,bounds);
        await new Promise(r=>setTimeout(r,200));
        rows.push({requested:bounds,result:await browser.windows.get(w.id)});
      }
    } finally {await browser.windows.remove(w.id);}
    return rows;
  }
  if(op === 'collisions') {
    const spec={name:'F01 duplicate',color:'blue',icon:'circle'};
    const a=await browser.contextualIdentities.create(spec),b=await browser.contextualIdentities.create(spec);
    return {a,b,samePresentationDifferentIds:a.cookieStoreId!==b.cookieStoreId,
      matches:await browser.contextualIdentities.query({name:spec.name})};
  }
  if(op === 'interactions') {
    const rows=[];const c=await browser.contextualIdentities.create({name:'F01 synthetic custom',color:'blue',icon:'circle'});
    for(const active of [false,true]) for(const discarded of [false,true]) for(const pinned of [false,true]) {
      try {
        const t=await browser.tabs.create({url,active,discarded,pinned,cookieStoreId:c.cookieStoreId});
        await browser.tabs.update(t.id,{muted:true});
        let group;
        try {group=await browser.tabs.group({tabIds:[t.id]});}catch(e){group=String(e);}
        rows.push({requested:{active,discarded,pinned,muted:true,container:c.cookieStoreId},group,result:tab(await browser.tabs.get(t.id))});
      } catch(e){rows.push({requested:{active,discarded,pinned},error:String(e)});}
    }
    const reader=await browser.tabs.create({url,active:false,openInReaderMode:true,cookieStoreId:c.cookieStoreId});
    for(let i=0;i<100;i++){if((await browser.tabs.get(reader.id)).isInReaderMode)break;await new Promise(r=>setTimeout(r,50));}
    const group=await browser.tabs.group({tabIds:[reader.id]});
    rows.push({readerContainerGroup:tab(await browser.tabs.get(reader.id)),group});
    const missing=await browser.contextualIdentities.create({name:'F01 removed',color:'red',icon:'circle'});
    await browser.contextualIdentities.remove(missing.cookieStoreId);
    try {await browser.tabs.create({url,cookieStoreId:missing.cookieStoreId});rows.push({missingContainer:'UNEXPECTED_CREATE'});}
    catch(e){rows.push({missingContainer:'REJECTED',error:String(e)});}
    return {rows,customContainer:c};
  }
  throw Error('unknown finite target operation');
};
'''
MEMORY = r'''
const done=arguments[arguments.length-1];
const mgr=Cc['@mozilla.org/memory-reporter-manager;1'].getService(Ci.nsIMemoryReporterManager);
const rows=[];mgr.getReports({callback(process,path,kind,units,amount,description){
  rows.push({process,path,kind,units,amount});
}},null,()=>done(rows),null,false);
'''


def memory_categories(rows, origin):
    """Disjoint explicit reporter leaves only; do not add summary trees twice."""
    totals = dict(js=0, dom=0, layout=0, other_explicit=0, driver_sandbox=0)
    for row in rows:
        path = row['path']
        if not origin or origin not in path or row['units'] != 0 or not path.startswith('explicit/'):
            continue
        category = ('driver_sandbox' if '[anonymous sandbox]' in path else
                    'js' if '/js-' in path or '/js/' in path else
                    'dom' if '/dom/' in path else 'layout' if '/layout/' in path else 'other_explicit')
        totals[category] += row['amount']
    return {'explicit_origin_leaf_bytes': totals, 'cache_separately_attributed': False,
            'shared_native_residual_attributed': False, 'hard_peak_qualified': False}


def execute(client, script, args=None, chrome=True, async_script=False):
    client.command('Marionette:SetContext', {'value': 'chrome' if chrome else 'content'})
    result = client.command('WebDriver:ExecuteAsyncScript' if async_script else 'WebDriver:ExecuteScript',
        {'script': script, 'args': args or [], 'newSandbox': True, 'sandbox': 'default', 'scriptTimeout': 30000})
    return result.get('value', result) if isinstance(result, dict) else result


def api(client, operation, url):
    return json.loads(execute(client,
        'const done=arguments[arguments.length-1]; window.wrappedJSObject.targetOperation(arguments[0],arguments[1]).then(x=>done(JSON.stringify(x)),e=>done(JSON.stringify({error:String(e)})));',
        [operation, url], chrome=False, async_script=True))


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--firefox', type=Path, required=True)
    parser.add_argument('--firefox-sha256', required=True); args = parser.parse_args()
    if os.name != 'nt' and (platform.system() != 'Linux' or not os.environ.get('DISPLAY') or not os.environ.get('WAYLAND_DISPLAY')):
        raise ValueError('this instrument requires the available Ubuntu visible Wayland Desktop')
    binary = args.firefox.resolve(strict=True)
    if digest(binary) != args.firefox_sha256: raise ValueError('binary hash mismatch')
    ini = configparser.ConfigParser(); ini.read(binary.parent / 'application.ini')
    if ini['App']['Version'] != '156.0' or '"release"' not in (binary.parent / 'defaults/pref/channel-prefs.js').read_text():
        raise ValueError('official Stable 156 required')
    owned = Path(tempfile.mkdtemp(prefix='target-', dir=ROOT/'build/f01/runs')).resolve()
    profile = owned/'profile'; profile.mkdir()
    class Local(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *_args): pass
        def do_GET(self):
            if self.path.split('?')[0] not in {'/article.html', '/video.html'}: self.send_error(404); return
            super().do_GET()
    server = http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Local,directory=str(SOURCE/'pages')))
    threading.Thread(target=server.serve_forever,daemon=True).start()
    url=f'http://127.0.0.1:{server.server_port}/article.html'
    if os.name == 'nt':
        # Preseed only this new profile; native openWindow avoids the pin/install path.
        webapp=profile/'taskbartabs';webapp.mkdir()
        (webapp/'taskbartabs.json').write_text(json.dumps({'version':1,'taskbarTabs':[{
            'id':'c930c827-57af-4119-a8e6-88808019f001','scopes':[{'hostname':'127.0.0.1'}],
            'userContextId':0,'startUrl':url,'name':'F01 synthetic disposable'}]}))
    with socket.socket() as s: s.bind(('127.0.0.1',0)); port=s.getsockname()[1]
    prefs={'marionette.port':port,'browser.shell.checkDefaultBrowser':False,'browser.startup.page':0,
        'browser.startup.homepage':'about:blank','browser.aboutwelcome.enabled':False,
        'browser.startup.homepage_override.mstone':'ignore','startup.homepage_welcome_url':'',
        'startup.homepage_welcome_url.additional':'','browser.newtabpage.enabled':False,
        'browser.tabs.warnOnClose':False,'browser.warnOnQuit':False,
        'app.update.auto':False,'app.update.disabledForTesting':True,
        'datareporting.policy.dataSubmissionEnabled':False,'toolkit.telemetry.enabled':False,
        'network.proxy.type':1,'network.proxy.http':'127.0.0.1','network.proxy.http_port':9,
        'network.proxy.ssl':'127.0.0.1','network.proxy.ssl_port':9,'network.proxy.no_proxies_on':'localhost, 127.0.0.1',
        'network.dns.disablePrefetch':True,'network.prefetch-next':False,'media.autoplay.default':0}
    (profile/'user.js').write_text(''.join('user_pref('+json.dumps(k)+', '+json.dumps(v)+');\n' for k,v in prefs.items()))
    manifest={'manifest_version':3,'name':'F01 target qualification ONLY','version':'0.0.1','incognito':'not_allowed',
        'browser_specific_settings':{'gecko':{'id':ID,'strict_min_version':'156.0','data_collection_permissions':{'required':['none']}}},
        'permissions':['tabs','cookies','contextualIdentities','tabGroups']}
    package=owned/'target.xpi'
    with zipfile.ZipFile(package,'x') as z:
        for name,content in {'manifest.json':json.dumps(manifest),'driver.html':'<!doctype html><meta charset="utf-8"><title>F01 synthetic driver</title><script src="driver.js"></script>','driver.js':DRIVER}.items():
            info=zipfile.ZipInfo(name,(2026,9,19,0,0,0));info.external_attr=0o100644<<16;z.writestr(info,content)
    record={'evidence_class':'WINDOWS_RUNTIME_VERIFIED' if os.name == 'nt' else 'UBUNTU_RUNTIME_VERIFIED','qualification_only':True,'host':platform.node(),'os':platform.platform(),
        'driver_sources':preserve_driver_sources(owned),
        'version':ini['App']['Version'],'build_id':ini['App']['BuildID'],'binary':str(binary),'binary_sha256':digest(binary),
        'profile':str(profile),'profile_class':'NEW_SYNTHETIC_DISPOSABLE','probe_sha256':digest(package),
        'headless':False,'driver_source_sha256':digest(Path(__file__)),'observations':[],'memory':[], 'cleanup':'PENDING'}
    proc=None;client=None
    def observe(name, fn):
        try:
            value=fn(); outcome='OPEN' if isinstance(value,dict) and 'error' in value else 'OBSERVED'
            record['observations'].append({'name':name,'outcome':outcome,'value':value});return value
        except Exception as e: record['observations'].append({'name':name,'outcome':'OPEN','error':str(e)});return None
    def memory(label, origin=''):
        started=time.monotonic()
        rows=execute(client,MEMORY,async_script=True)
        artifact=owned/(label+'-memory.json');artifact.write_text(json.dumps(rows,indent=2)+'\n')
        try:
            diagnostics=sample(proc.pid)
        except OSError as error:
            diagnostics={'status':'UNAVAILABLE','error':str(error)}
        record['memory'].append({'label':label,'native_report_sha256':digest(artifact),'native_report_count':len(rows),
            'addon_rows':[r for r in rows if origin and origin in r['path']],
            'categories':memory_categories(rows,origin),'reporter_wall_seconds':time.monotonic()-started,
            'os_job' if os.name == 'nt' else 'os_cgroup':proc.counters(),
            'process_diagnostics':diagnostics,
            'semantics':'Firefox point-in-time native reporters; OS total/shared/charged memory is not addon-attributable memory or a hard addon peak.'})
    try:
        command=[str(binary),'--no-remote','--new-instance','--profile',str(profile),'--marionette','--remote-allow-system-access']
        if os.name == 'nt':
            from windows_job import WindowsJobProcess
            proc=WindowsJobProcess(command)
            record.update(pid=proc.pid,command=command,job_before_resume=proc.before_resume,
                          launcher_in_parent_job=proc.launcher_in_job)
        else:
            proc=UserCgroupProcess(command,owned/'firefox.log');record.update(pid=proc.pid,command=command,cgroup=str(proc.group))
        deadline=time.monotonic()+45
        while time.monotonic()<deadline:
            if proc.poll() is not None: raise RuntimeError('owned browser exited')
            try:client=Marionette(port);break
            except (ConnectionRefusedError,TimeoutError):time.sleep(.2)
        if client is None:raise TimeoutError('owned protocol absent')
        session=client.command('WebDriver:NewSession',{'capabilities':{'alwaysMatch':{}}})
        caps=session.get('capabilities',session.get('value',{}).get('capabilities',{}))
        if os.name == 'nt':
            record['browser_job_binding']=proc.bind_browser(caps.get('moz:processID'),binary)
        elif caps.get('moz:processID')!=proc.pid:
            raise ValueError('owned PID mismatch')
        if Path(caps['moz:profile']).resolve()!=profile:raise ValueError('owned profile mismatch')
        record['session_binding']=caps
        observe('desktop',lambda:execute(client,'return {mozHeadlessEnvironment:Services.env.get("MOZ_HEADLESS"),windowState:window.windowState,screen:{width:screen.width,height:screen.height},platform:Services.appinfo.OS,profilerFeatures:Services.profiler.GetFeatures()};'))
        memory('a-no-addon')
        client.command('Addon:Install',{'path':str(package),'temporary':True})
        extension_url=execute(client,'return WebExtensionPolicy.getByID(arguments[0]).getURL("driver.html");',[ID])
        record['extension_url']=extension_url
        client.command('Marionette:SetContext',{'value':'content'});client.command('WebDriver:Navigate',{'url':extension_url})
        origin=extension_url.split('/')[2]
        observe('initial-api',lambda:api(client,'snapshot',url));memory('b-addon-idle',origin)
        observe('synthetic-allocation',lambda:api(client,'allocate',url));memory('b-addon-held',origin)
        observe('synthetic-short-pulse',lambda:api(client,'pulse',url));memory('b-after-pulse',origin)
        observe('synthetic-release',lambda:api(client,'release',url))
        observe('private-native-create',lambda:execute(client,'window.f01Private=window.OpenBrowserWindow({private:true}); return true;'))
        time.sleep(1)
        observe('private-native-windows',lambda:execute(client,'return Array.from(Services.wm.getEnumerator(null)).map(w=>({type:w.document.documentElement.getAttribute("windowtype"),private:ChromeUtils.importESModule("resource://gre/modules/PrivateBrowsingUtils.sys.mjs").PrivateBrowsingUtils.isWindowPrivate(w)}));'))
        observe('private-api-exclusion',lambda:api(client,'snapshot',url))
        observe('private-native-close',lambda:execute(client,'window.f01Private.close();return true;'))
        observe('split-native',lambda:execute(client,'const b=window.gBrowser;const a=b.addTab(arguments[0],{triggeringPrincipal:Services.scriptSecurityManager.getSystemPrincipal()});const c=b.addTab(arguments[0],{triggeringPrincipal:Services.scriptSecurityManager.getSystemPrincipal()});const v=b.addTabSplitView([a,c]);return {id:v.splitViewId,tabs:v.tabs.length,pref:Services.prefs.getBoolPref("browser.tabs.splitView.enabled",false)};',[url]))
        time.sleep(.5)
        observe('split-api-events',lambda:api(client,'snapshot',url))
        observe('interactions',lambda:api(client,'interactions',url))
        observe('container-collisions',lambda:api(client,'collisions',url))
        observe('geometry-states',lambda:api(client,'geometry',url))
        observe('devtools',lambda:execute(client,'const done=arguments[arguments.length-1];const {loader}=ChromeUtils.importESModule("resource://devtools/shared/loader/Loader.sys.mjs");loader.require("devtools/client/framework/devtools").gDevTools.showToolboxForTab(window.gBrowser.selectedTab,{toolId:"webconsole",hostType:"window"}).then(t=>{window.f01Toolbox=t;done({host:t.hostType});},e=>done({error:String(e)}));',async_script=True))
        observe('special-native-windows',lambda:execute(client,'return Array.from(Services.wm.getEnumerator(null)).map(w=>({type:w.document.documentElement.getAttribute("windowtype"),uri:w.document.documentURI}));'))
        observe('special-api-windows',lambda:api(client,'snapshot',url))
        observe('devtools-close',lambda:execute(client,'const done=arguments[arguments.length-1];if(window.f01Toolbox)window.f01Toolbox.destroy().then(()=>done(true));else done(false);',async_script=True))
        observe('pip-video-tab',lambda:execute(client,'const t=window.gBrowser.addTab(arguments[0],{triggeringPrincipal:Services.scriptSecurityManager.getSystemPrincipal()});window.f01VideoTab=t;window.gBrowser.selectedTab=t;return true;',[url.replace('/article.html','/video.html')]))
        observe('pip-request',lambda:execute(client,'const done=arguments[arguments.length-1];const b=window.f01VideoTab.linkedBrowser;const start=Date.now();const poll=()=>{if(b.currentURI.spec.endsWith("/video.html")&&!b.webProgress.isLoadingDocument){b.browsingContext.currentWindowGlobal.getActor("PictureInPictureLauncher").sendAsyncMessage("PictureInPicture:KeyToggle");done(true);}else if(Date.now()-start>10000)done({error:"synthetic video load deadline"});else setTimeout(poll,100);};poll();',async_script=True))
        observe('pip-native-window',lambda:execute(client,'const done=arguments[arguments.length-1];const start=Date.now();const poll=()=>{const ws=Array.from(Services.wm.getEnumerator(null));const p=ws.find(w=>w.document.documentURI.includes("pictureinpicture"));if(p)done({type:p.document.documentElement.getAttribute("windowtype"),uri:p.document.documentURI});else if(Date.now()-start>10000)done({error:"no native PiP window observed"});else setTimeout(poll,100);};poll();',async_script=True))
        observe('pip-api-exclusion',lambda:api(client,'snapshot',url))
        observe('pip-native-close',lambda:execute(client,'for(const w of Services.wm.getEnumerator(null)){if(w.document.documentURI.includes("pictureinpicture"))w.close();}return true;'))
        observe('webapp-surface',lambda:execute(client,'return {os:Services.appinfo.OS,webAppWindow:typeof window.openWebApp,webAppMenu:!!document.getElementById("appMenu-installSite-button"),taskbarTabsEnabled:Services.prefs.getBoolPref("browser.taskbarTabs.enabled",false)};'))
        if os.name == 'nt':
            observe('webapp-native-open',lambda:execute(client,'const done=arguments[arguments.length-1];(async()=>{const {TaskbarTabs}=ChromeUtils.importESModule("resource:///modules/taskbartabs/TaskbarTabs.sys.mjs");const t=await TaskbarTabs.getTaskbarTab("c930c827-57af-4119-a8e6-88808019f001");window.f01WebApp=await TaskbarTabs.openWindow(t);done({id:t.id,type:window.f01WebApp.document.documentElement.getAttribute("windowtype"),uri:window.f01WebApp.document.documentURI,taskbarTab:window.f01WebApp.document.documentElement.getAttribute("taskbartab"),tabs:window.f01WebApp.gBrowser.tabs.length});})().catch(e=>done({error:String(e)}));',async_script=True))
            observe('webapp-api-classification',lambda:api(client,'snapshot',url))
            observe('webapp-native-close',lambda:execute(client,'if(window.f01WebApp){window.f01WebApp.close();return true;}return false;'))
        record['status']='PARTIAL_OBSERVATIONS__NO_GATE_SELF_ACCEPTANCE'
        client.command('Marionette:Quit',{'flags':['eForceQuit']});proc.wait(20)
    except Exception as e:record['status']='PROBE_FAILED';record['error']=str(e)
    finally:
        if client:client.close()
        if proc and proc.poll() is None:proc.terminate();proc.wait(15)
        server.shutdown();server.server_close()
        if proc and proc.poll() is None:record['cleanup']='OWN_PROCESS_REMAINS'
        else:
            if os.name == 'nt' and proc:
                record['job_final']=proc.counters()
                record['observed_job_identities']=[list(k) for k in proc.identities]
                proc.close()
            shutil.rmtree(profile);record['cleanup']='OWN_PROFILE_REMOVED__OWN_JOB_EXITED' if os.name == 'nt' else 'OWN_PROFILE_REMOVED__OWN_CGROUP_EXITED'
        (owned/'evidence.json').write_text(json.dumps(record,indent=2)+'\n')
        print(json.dumps({'evidence':str(owned/'evidence.json'),'status':record['status'],'cleanup':record['cleanup']}))
    if record['status']=='PROBE_FAILED':raise SystemExit(1)


if __name__=='__main__':main()
