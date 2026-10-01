// Qualification only: finite synthetic cases, no WindowSafe capture/recovery store.
declare const F01_CONFIG: { url: string; run: string };
type Observation = { name: string; outcome: "OBSERVED" | "REJECTED"; value?: unknown; error?: string };
const observations: Observation[] = [];
let running = false;
const observe = async (name: string, operation: () => Promise<unknown>) => {
  try { observations.push({ name, outcome: "OBSERVED", value: await operation() }); }
  catch (error) { observations.push({ name, outcome: "REJECTED", error: String(error) }); }
};
// Types 143 lack splitViewId. Narrow observation only; never invent a creation API.
const snapshot = (tab: browser.tabs.Tab) => ({
  id: tab.id, windowId: tab.windowId, incognito: tab.incognito, hidden: tab.hidden,
  discarded: tab.discarded, pinned: tab.pinned, muted: tab.mutedInfo?.muted,
  cookieStoreId: tab.cookieStoreId, groupId: tab.groupId,
  splitViewId: (tab as browser.tabs.Tab & { splitViewId?: number }).splitViewId,
  isInReaderMode: tab.isInReaderMode, isArticle: tab.isArticle,
});
async function loaded(id: number): Promise<browser.tabs.Tab> {
  // Bounded wait for this one synthetic navigation; never a native-restore signal.
  for (let i = 0; i < 100; i++) {
    const tab = await browser.tabs.get(id);
    if (tab.status === "complete" && tab.url && tab.url !== "about:blank") return tab;
    await new Promise(resolve => setTimeout(resolve, 50));
  }
  throw new Error("Synthetic navigation did not complete");
}
async function run(trigger: string) {
  if (running) return;
  running = true;
  if (browser.extension.inIncognitoContext || !/^http:\/\/127\.0\.0\.1:\d+\/article\.html$/.test(F01_CONFIG.url)) return;
  const before = await browser.storage.local.get("syntheticMarker");
  await observe("previous-probe-marker", async () => before);
  await observe("previous-session-hints", async () => {
    if (!before.syntheticMarker) return { initial: true };
    const tabs = await browser.tabs.query({});
    return Promise.all(tabs.map(async tab => ({ tab: snapshot(tab), marker: await browser.sessions.getTabValue(tab.id!, "f01") })));
  });
  await observe("private-access", async () => ({ allowed: await browser.extension.isAllowedIncognitoAccess(), context: browser.extension.inIncognitoContext }));
  const normal = await browser.windows.create({ url: F01_CONFIG.url, type: "normal", width: 800, height: 600 });
  await observe("normal-window", async () => ({ type: normal.type, incognito: normal.incognito, width: normal.width, height: normal.height, state: normal.state }));
  await observe("popup-window", async () => {
    const popup = await browser.windows.create({ url: F01_CONFIG.url, type: "popup" });
    const result = { type: popup.type, incognito: popup.incognito };
    await browser.windows.remove(popup.id!); return result;
  });
  await observe("private-window-exclusion", async () => {
    const p = await browser.windows.create({ url: "about:blank", incognito: true });
    const visible = await browser.windows.getAll();
    const result = { returned: !!p, visiblePrivateCount: visible.filter(w => w.incognito).length };
    if (p?.id) await browser.windows.remove(p.id); return result;
  });
  const created: number[] = [];
  for (const pinned of [false, true]) for (const discarded of [false, true]) for (const muted of [false, true]) {
    await observe(`combination-p${pinned}-d${discarded}-m${muted}`, async () => {
      const tab = await browser.tabs.create({ windowId: normal.id, url: F01_CONFIG.url, active: false, pinned, discarded });
      created.push(tab.id!); await browser.tabs.update(tab.id!, { muted });
      return snapshot(await browser.tabs.get(tab.id!));
    });
  }
  await observe("hidden-by-helper", async () => {
    const tab = await browser.tabs.create({ windowId: normal.id, url: F01_CONFIG.url, active: false });
    await loaded(tab.id!);
    await browser.runtime.sendMessage("f01-helper@windowsafe.invalid", { operation: "hide", tabId: tab.id });
    return snapshot(await browser.tabs.get(tab.id!));
  });
  await observe("container", async () => {
    const containers = await browser.contextualIdentities.query({});
    const first = containers[0]; if (!first) return { available: false };
    const tab = await browser.tabs.create({ windowId: normal.id, url: F01_CONFIG.url, active: false, discarded: true, cookieStoreId: first.cookieStoreId });
    return { available: true, count: containers.length, tab: snapshot(tab) };
  });
  await observe("missing-container", async () => snapshot(await browser.tabs.create({ url: F01_CONFIG.url, active: false, cookieStoreId: "firefox-container-99999" })));
  await observe("native-group", async () => {
    const tabs = await browser.tabs.query({ windowId: normal.id, pinned: false });
    const groupId = await browser.tabs.group({ tabIds: tabs.filter(t => !t.hidden).slice(0, 2).map(t => t.id!) });
    await browser.tabGroups.update(groupId, { title: "F01 synthetic", color: "blue" });
    return { group: await browser.tabGroups.get(groupId), tabs: (await browser.tabs.query({ groupId })).map(snapshot) };
  });
  await observe("reader-intent", async () => {
    const tab = await browser.tabs.create({ url: F01_CONFIG.url, active: false, openInReaderMode: true });
    return snapshot(await loaded(tab.id!));
  });
  await observe("privileged-url-rejection", async () => snapshot(await browser.tabs.create({ url: "chrome://browser/content/browser.xhtml", active: false })));
  await observe("session-hints", async () => {
    const id = normal.tabs![0].id!;
    await browser.sessions.setTabValue(id, "f01", F01_CONFIG.run);
    await browser.sessions.setWindowValue(normal.id!, "f01", F01_CONFIG.run);
    return { tab: await browser.sessions.getTabValue(id, "f01"), window: await browser.sessions.getWindowValue(normal.id!, "f01") };
  });
  await observe("surface", async () => ({
    windowsOnBoundsChanged: "onBoundsChanged" in browser.windows,
    splitConstant: "SPLIT_VIEW_ID_NONE" in browser.tabs,
    nativeGroup: typeof browser.tabs.group === "function",
    startupEvent: typeof browser.runtime.onStartup.addListener === "function",
    restoreCompleteSignal: "NOT_ESTABLISHED__NO_TIMER_INFERENCE",
  }));
  const marker = { run: F01_CONFIG.run, trigger, ordinal: Number(before.syntheticMarker?.ordinal || 0) + 1 };
  await browser.storage.local.set({ syntheticMarker: marker });
  const report = { qualificationOnly: true, trigger, marker, browser: await browser.runtime.getBrowserInfo(), observations };
  const url = URL.createObjectURL(new Blob([JSON.stringify(report, null, 2)], { type: "application/json" }));
  await browser.downloads.download({ url, filename: `f01-${marker.ordinal}.json`, saveAs: false, conflictAction: "uniquify" });
}
browser.runtime.onInstalled.addListener(() => { void run("onInstalled"); });
browser.runtime.onStartup.addListener(() => { void run("onStartup"); });
