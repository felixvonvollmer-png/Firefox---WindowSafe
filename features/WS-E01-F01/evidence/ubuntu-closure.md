# F01 Ubuntu/Cross-OS closure — BLOCKED, material user decision required

Run **WS-E01-F01-UBUNTU-CLOSURE-20260924-01**, authorization WS-EA-20260919-08
plus the user's explicit execution request in this session. Start Head
`ead93411b37dcb0885be018f0a865f236dc52ff2`, tree
`8c63505204527bc23b1da26ee301b35737d52720`; branch
`feature/ws-e01-f01-qualification`; unchanged main/feature basis
`3bdd7439c221b8f8c83e7374c8bb29898891a4fd`. Risk ELEVATED.
Coding-Agent qualification evidence, no independent verdict or acceptance subject.

## Decision and evidence

**WS-E01-F01_BLOCKED__MATERIAL_USER_DECISION_REQUIRED.** On both targets,
a native Taskbar Tab/WebApp is exposed as a normal window. No reliable public
WebExtension discriminator was established within the accepted permission direction.
Product WS-RESTORE and Technical Foundation r6 §7.1 require a resolved safe boundary
before productive capture. No option below has been chosen or implemented.

[Original package bytes](ubuntu-closure-inputs.json), [preflight](ubuntu-closure-preflight.json),
[new Ubuntu runtime](ubuntu-closure-runtime.json), [exact runtime artifacts](ubuntu-closure-artifacts.json)
and [bounded primary-source research](ubuntu-closure-research.json) bind this finding.
The preflight reverified all 176 Windows-continuation inputs, repository ID, full
Head/Tree/branch/remote/main, Python 3.14.4, unchanged lock, clean index/worktree,
Draft/unmerged PR #3 and successful start-head CI 35988797467. One agent/writer;
no delegation. All 51 installed Stable files match the previously bound official
archive. Firefox 156.0, build 20260909172920, exact source revision
`a80bd15ddee3b4bf3679aeba340e9d2db933c467`.

Ubuntu 26.04.1, actual GNOME/Wayland session, visible 1920x1080 screen. The command
`python3 qualification/ws-e01-f01/target_probe.py --firefox build/f01/firefox/firefox --firefox-sha256 7ea3daf0cdbe5ec27e4f2e7c644c25032169f8a2f2f15e438ff4379bf737a78a --closure-only`
created one disposable synthetic profile and localhost fixture. It enabled
`browser.taskbarTabs.enabled` only there and reused the existing test-only registry
preseed/openWindow route; no OS pin/install/default change. Native observation:
`navigator:browser`, nonempty `taskbartab`, one tab. Public `windows.getAll` then
returned the additional fixture window (ID 29) as `normal`, without WebApp metadata.
The driver window and timed-out geometry window were separately present. Native
fixture control and before/after observations identify the synthetic WebApp;
its title/URL is not proposed as a product discriminator.

The exact-revision `toolkit/components/extensions/parent/ext-tabs-base.js`, lines
1077–1089, classifies windows using dialog/toolbar Chrome flags; lines 1106–1125
serialize the public fields without `taskbartab`. TaskbarTabsWindowManager opens
with toolbar features and sets the native attribute (including a Linux path).
The Window/Tab schemas offer no supported WebApp identity. The `app` enum value
does not mean Firefox Taskbar Tabs are returned as `app`.
[Public Window contract](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/windows/Window),
[WindowType](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/windows/WindowType)
and [Tab contract](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/tabs/Tab)
were read currently. This is a bounded negative finding, not a claim about every
future Firefox version or privileged interface.

## Gate dispositions and retained failures

| Gate | Disposition |
|---|---|
| WINDOWS_DESKTOP | OPEN: prior actual Windows runtime reused; shared public WebApp boundary unresolved. No new Windows replay needed for this finding. |
| SPECIAL_NATIVE_GUI_CASES | BLOCKED: enabled Ubuntu WebApp now observed, same ambiguity as Windows. Display/state probes incomplete. |
| MEASUREMENT_FINAL_ATTRIBUTION | OPEN: prior native reporter/cgroup/Job observations reused; final method not qualified. |
| TARGET_EQUIVALENT_RESTART | Remains CLOSED_BY_QUALIFICATION_EVIDENCE on both OSes; not repeated. |

The Ubuntu topology attempt failed because `nsIScreenManager.screens` was undefined.
The geometry/state sequence timed out after 30 seconds; a remaining synthetic
window was observed maximized, but this does not prove completion of any requested
sequence. Raw errors and exact executed driver bytes are retained. Exit 0 means
partial observations were collected, not that those probes passed. No topology,
monitor-removal, mixed-DPI or completed geometry claim is made. After the WebApp
material stop, neither probe was repaired/replayed. Own profile is absent, own
cgroup is absent; no existing browser/profile was touched. An auxiliary zipfile
read of optimized omni.ja failed; no extraction occurred. One guessed source path
returned 404; the actual ext-tabs-base.js source was then located and inspected.

Existing per-OS private/DevTools/PiP/Split/container/group/restart evidence remains
unchanged: [Windows report](win-qualification.md), [Ubuntu report](target-qualification.md).
Their historical open-gate wording is not rewritten.

## Measurement interpretation and exact remaining work

Technical Foundation r6 §9.1 requires attributable living JS/DOM/cache memory after
quiescence, separate native/unattributable reporting, paired process measurements,
and additional export/import peak above the resting value. It does not explicitly
mandate a separate byte counter for every JS Map, exhaustive PID identities or a
particular continuous-trace technology. This run adds no such requirement.

- A JS Map's representation can fall within origin JS totals; absence of a separate
  Map counter does not imply that cache memory is omitted. The existing fixture
  does not isolate all cache channels/backing stores or prove their accounting.
  Next evidence must establish reporter coverage with cache-only allocate/release
  contrasts and identify excluded channels, without double counting.
- Shared/native residual remains **unknown**, not zero. Whole-cgroup charged memory,
  Job commit peak, summed RSS and private bytes have different meanings; none is
  an add-on-only peak or a direct interchangeable residual subtraction.
- Existing cgroup/Job lifetime CPU includes exited children. The Windows difference
  between 18 lifetime processes and 17 sampled identities is a diagnostic coverage
  gap; it does not alone invalidate aggregate accounting in a securely bound Job.
  F05 still needs interval boundaries, containment and driver/background uncertainty.
- Both targets advertise `jsallocations`; neither prior target advertises
  `nativeallocations`. Availability alone proves no recorder coverage.
  [Mozilla's profiler memory documentation](https://firefox-source-docs.mozilla.org/tools/profiler/memory.html)
  describes sampled native allocation profiling and its Nightly restriction.
  [Debugger.Memory](https://firefox-source-docs.mozilla.org/devtools-user/debugger-api/debugger.memory/index.html)
  provides allocation logging/census, with sampling and overflow controls. Neither
  source establishes a complete add-on live JS/DOM/cache/native peak channel.
- A future method may use a defensible bound rather than an exact continuous trace,
  if its coverage and uncertainty satisfy the unchanged threshold. A sampled value
  after a pulse is insufficient. No proof of impossibility or new Foundation
  decision is claimed here. Controlled instrumentation-on/off overhead and paired
  uncertainty remain unmeasured beyond the prior point-query observations.

The user-directed material WebApp stop was reached before new allocation/profiler
experiments. Therefore cross-OS memory/peak closure is **not completed** and is not
presented as a second required product decision. No F05 performance claim.

## Material options — none selected

1. **Explicit ordinary-tab fallback for API-normal windows, including WebApps.**
   Keep their observable tabs/data and restore into ordinary windows, with a clear
   general limitation that native WebApp identity, scoping and integration are not
   preserved. No automatic claim of identifying WebApps. This changes the special-
   window contract and requires explicit Product/Technical-Foundation/Preparation
   rebinding plus later fallback/UX qualification; it does not grant F02 authority.
2. **Restrict the supported environment to demonstrably disabled native WebApps.**
   Establish an enforceable external configuration prerequisite and requalify it.
   WindowSafe cannot certify that prerequisite through the currently established
   API. User assurance alone is not a technical detector. This narrows supported
   environments on both OSes, requires an enforcement/maintenance concept and
   explicit Product/Technical-Foundation/Preparation rebinding.
3. **Keep the current boundary and pause affected implementation until a supported
   public discriminator is available.** No product-scope reduction now; schedule
   remains blocked. A changed Firefox target/API will need a separately approved
   version/environment binding and fresh qualification. No browser upgrade here.

## Minimal continuation and verification

First obtain the material decision and required exact rebinding. Then execute only:
(a) qualification of the chosen boundary; (b) repaired Ubuntu screen topology and
bounded per-transition geometry/state observations on the actual host; (c) final
cross-OS cache/residual/peak/overhead method qualification described above. Reuse
existing Windows/runtime/restart evidence. Request a Windows probe only if a new
hypothesis cannot be answered by the bound Windows observations/source.

[Local verification](ubuntu-closure-verification.json) records commands, results,
limits and exact log hashes; [continuation inventory](ubuntu-closure-manifest.json)
binds current files. Historical schema/request checks remain bound to the accepted
Epic; they do not prepare Feature Acceptance. Exact post-commit CI and delivery
Head/Tree are reported externally after publication to avoid self-reference.

STOP with PR #3 Draft/unmerged. No Feature Acceptance, independent verdict, merge,
V6 migration, F02/product implementation, dependency/toolchain change, signing,
release or Production.
