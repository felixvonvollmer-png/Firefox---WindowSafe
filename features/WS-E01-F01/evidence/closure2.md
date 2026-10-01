# F01 closure after WS-P05 — Ubuntu qualification complete, Windows peak instrument OPEN

Run WS-E01-F01-CLOSURE2-20261001 under the broad WS-E01 execution authorization
WS-EA-20261001-03 (`epics/WS-E01/evidence/broad-execution-authorization.json`) after the
independent Epic PASS WS-E01-EPR-DELTA-20260930-05 and exact rebinding integrated in main
`714b440c26167f6411420fbbda4be69deb2e9670`. Coding-agent qualification evidence; no
independent verdict, no Feature Acceptance, no product implementation. Risk ELEVATED.

The historical F01 files from PR #3 head `7d66ca5b025c8f748d7f97b961c496ee450daaa7` were
transferred byte-identically; their historical BLOCKED wording is not rewritten. The material
cause (WebApp boundary) is answered by WS-P05; this report records only the remaining scope
named by the Epic delta: (a) WS-P05 fallback, (b) Ubuntu display/geometry/state,
(c) cross-OS memory/peak method.

## Environment and instrument

Ubuntu 26.04.1, GNOME on Wayland (`windowProtocol: wayland`), one 1920x1080 display, scale 1.
Firefox 156.0 Stable, build 20260909172920, binary SHA-256
`7ea3daf0cdbe5ec27e4f2e7c644c25032169f8a2f2f15e438ff4379bf737a78a` (same bound archive as the
earlier F01 runs). Instrument `qualification/ws-e01-f01/closure_probe.py`: one new disposable
synthetic profile per run, localhost fixture pages, owned transient `systemd-run --user` cgroup,
temporary qualification-only add-on with `tabs` and `unlimitedStorage`; native chrome calls are
TEST_ONLY fixture control. Two complete runs:
[run 1](closure2-ubuntu-run1.json), [run 2](closure2-ubuntu-run2.json),
[raw artifact hashes](closure2-artifacts.json). Profiles removed, cgroups exited.

## (a) WS-P05 fallback — QUALIFIED on Ubuntu, Windows reused

The enabled synthetic Taskbar Tab window (native `taskbartab` attribute set) is returned by
`windows.getAll({populate:true})` as `type: normal` with its tab URL, title, active, pinned,
muted, discarded, container and group fields readable through the public API. Restoring it via
`windows.create({type:'normal'})` plus `tabs.create({discarded:true, active:false})` produced an
ordinary window without `taskbartab`, active tab loaded, background tab discarded, URLs intact.
No WebApp discriminator, private interface or URL/title heuristic is needed or used. Windows
already showed the same `normal` classification for its Taskbar Tab and the same public
`windows.create` path in the bound Windows runs; no new Windows hypothesis arises, so no Windows
replay is requested for (a). The visible general limitation is a product/UX obligation for F03/F05.

## (b) Ubuntu display/geometry/state — QUALIFIED with observed limits

- Topology: `nsIScreenManager.screens` is not exposed in 156; `primaryScreen` and
  `screenForRect` work. One display; far-away rects map to the primary screen.
- Wayland: reported window `left/top` is always 0; requested positions (including off-screen
  -1800/-10000) and requested sizes after creation are ignored by the compositor. Initial size at
  creation is honored (952x702 for a 900x650 request including decorations).
- States: `maximized`, `normal` and `fullscreen` transitions complete and report correctly.
  `windows.update({state:'minimized'})` **never resolves** on this Wayland session (30 s script
  timeout, reproduced in both runs); the window remains usable afterwards.

Product consequences (within existing Product Truth, no new decision): on Wayland, position is
not restorable and the compositor's placement is the safe visible default; size best-effort at
creation; restore must not await `minimized` (bounded, non-blocking, never a reason to fail the
restore). Multi-monitor, monitor removal and mixed DPI cannot be produced on this single-display
host; Windows already covered two monitors. These are recorded limits, not claims.

## (c) Memory / peak method — Ubuntu QUALIFIED, Windows hard-peak instrument OPEN

Method WS-E01-F01-METHOD-02 extends METHOD-01 (thresholds unchanged, r6 §§9.1/9.3, T05-R2):

1. **Resting attributable add-on memory:** `nsIMemoryReporterManager.minimizeMemoryUsage`
   (GC/CC in all processes) immediately before reporting; sum disjoint `explicit/` leaves of the
   add-on origin; cross-check against all explicit leaves of the single `extension` process
   (identified by `ChromeUtils.requestProcInfo`, verified inside the owned cgroup) as a paired
   B−A difference, because built-in add-ons share that process.
2. **Coverage contrasts (both runs):** 8 MiB of flat Map strings: origin +11.0 MB, process
   +11.4 MB; 8 MiB IndexedDB records read back: further +8.7 MB origin; after release +
   minimize: back to baseline within 0.06 MB. IndexedDB parent-process explicit memory is
   reported separately (+0.19 MB). A first attempt with `padEnd`-generated strings produced
   shared ropes, not real bytes; that fixture is invalid and documented, not a reporter gap.
3. **Additional peak (Linux):** reset the extension process high-water mark via
   `/proc/<pid>/clear_refs` (`5`), run the operation, read `VmHWM`. A 24 MiB held-only pulse
   (25,165,824 bytes) gave +25,481,216 / +25,563,136 bytes; the point reporter sample after the
   pulse saw nothing. VmHWM delta is a conservative upper bound (includes allocator/native
   overhead); a pass against 8/16 MiB on it is sound, a failure must be investigated rather
   than assumed.
4. **Native/shared residual:** paired A/B cgroup `memory.current`/`memory.peak` and process RSS,
   reported separately and never as zero; not interchangeable with (1) or (3).
5. CPU/I-O/latency/load protocol unchanged from METHOD-01 (cgroup v2 on Ubuntu, Windows Job
   lifetime accounting already exercised natively).

**Windows gap:** Linux `clear_refs` has no Windows equivalent; whole-Job commit peak is
qualified but not add-on-only. Candidate: assign the extension process to an additional nested
measurement Job immediately before the operation and read its `PeakProcessMemoryUsed` minus the
commit at assignment, qualified by the same 24 MiB pulse and baseline contrasts. Nested Jobs
already worked on the bound Windows host. This needs one run on the Windows target; it cannot
be produced on this Ubuntu host. Handoff: [closure2-windows-handoff.md](closure2-windows-handoff.md).

## Gate dispositions

| Gate | Disposition |
|---|---|
| WS-P05 fallback | CLOSED on Ubuntu; Windows reused (same API class and path) |
| SPECIAL_NATIVE_GUI_CASES (Ubuntu display/state) | CLOSED with recorded Wayland limits |
| WINDOWS_DESKTOP | WebApp boundary answered by WS-P05; remaining Windows item is (c) |
| MEASUREMENT_FINAL_ATTRIBUTION | Ubuntu CLOSED (METHOD-02); Windows add-on hard peak OPEN |
| TARGET_EQUIVALENT_RESTART | Remains CLOSED, not repeated |

Pre-implementation consequence (TF §§9.1/9.3): the measurement method must be bound for both
target OSes before the affected product implementation (F02). F01 therefore stays open until
the Windows peak instrument run is recorded. No F02 product code starts before that.
