# F01 closure after WS-P05 — Ubuntu qualification, Windows peak instrument OPEN

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

**Correction after independent technical review WS-E01-TR-PR7-20261002-01.** The first version
of this report overstated two results: it called the VmHWM delta a conservative upper bound
without testing undercount, and it said sizes requested after creation are ignored (a read-back
race). Runs 3 and 4 below use a corrected instrument; runs 1 and 2 remain as historical evidence.

## Environment and instrument

Ubuntu 26.04.1, GNOME on Wayland (`windowProtocol: wayland`), one 1920x1080 display, scale 1.
Firefox 156.0 Stable, build 20260909172920, binary SHA-256
`7ea3daf0cdbe5ec27e4f2e7c644c25032169f8a2f2f15e438ff4379bf737a78a` (same bound archive as the
earlier F01 runs). Instrument `qualification/ws-e01-f01/closure_probe.py`: one new disposable
synthetic profile per run, localhost fixture pages, owned transient `systemd-run --user` cgroup,
temporary qualification-only add-on with `tabs` and `unlimitedStorage`; native chrome calls are
TEST_ONLY fixture control. Runs: [1](closure2-ubuntu-run1.json), [2](closure2-ubuntu-run2.json)
(first instrument), [3](closure2-ubuntu-run3.json), [4](closure2-ubuntu-run4.json) (corrected:
bounded update wait, settle-aware read-back, reuse trials); [raw artifact hashes](closure2-artifacts.json).
Profiles removed, cgroups exited in every run.

## (a) WS-P05 fallback — QUALIFIED on Ubuntu, Windows reused

In all four runs the enabled synthetic Taskbar Tab window (native `taskbartab` attribute set) is
returned by `windows.getAll({populate:true})` as `type: normal` with URL, title, active, pinned,
muted, discarded, container and group fields readable through the public API. Restoring it via
`windows.create({type:'normal'})` plus `tabs.create({discarded:true, active:false})` produced an
ordinary window without `taskbartab`, active tab loaded, background tab discarded, URLs intact.
No WebApp discriminator, private interface or URL/title heuristic is used. Windows already showed
the same `normal` classification and uses the same public `windows.create` path in the bound
Windows runs; no new Windows hypothesis arises, so no Windows replay is requested for (a). The
visible general limitation remains a product/UX obligation for F03/F05.

## (b) Ubuntu display/geometry/state — QUALIFIED with observed limits

- Topology: `nsIScreenManager.screens` is not exposed in 156; `primaryScreen` and
  `screenForRect` work. One display; far-away rects map to the primary screen.
- Position: reported `left/top` is always 0 on this Wayland session; requested positions
  (including off-screen -1800/-10000) have no observable effect.
- Size: initial size at creation is honored (952x702 for a 900x650 request including
  decorations); sizes requested later are applied (800x600, 850x600 in runs 3/4, stable after
  three equal read-backs 100 ms apart). Run 2's immediate read-back of 952x702 was a race.
- States: `maximized`, `normal`, `fullscreen` complete and report correctly.
  `windows.update({state:'minimized'})` does not resolve within 3 s (runs 3/4) or 30 s (runs 1/2)
  and the window stays `normal`; the browser remains usable.

Product consequences (within existing Product Truth, no new decision): on Wayland, position is not
restorable and the compositor's placement is the safe visible default; size is best-effort; restore
must never await `minimized` without a bound and never fail a restore because of it.
Multi-monitor, monitor removal and mixed DPI cannot be produced on this single-display host;
Windows covered two monitors. These are recorded limits, not claims.

## (c) Memory / peak method — Ubuntu QUALIFIED WITH CONDITIONS, Windows OPEN

Method WS-E01-F01-METHOD-02 extends METHOD-01 (thresholds unchanged, r6 §§9.1/9.3, T05-R2).
Measurement conditions are part of the method (r6 §10.2: forced cleanup is a stated measurement
condition, not claimed everyday behavior):

1. **Resting attributable add-on memory:** `nsIMemoryReporterManager.minimizeMemoryUsage`
   (GC/CC and purge in all processes) immediately before reporting; disjoint `explicit/` leaves of
   the add-on origin; cross-checked against all explicit leaves of the single `extension` process
   (identified via `ChromeUtils.requestProcInfo`, membership verified in the owned cgroup) as a
   paired B−A difference, because built-in add-ons share that process.
2. **Coverage contrasts (runs 1–4):** 8 MiB of flat Map strings: process +11.4 MB; 8 MiB of
   IndexedDB records read back: further +8.8 MB; after release + minimize back to baseline within
   0.07 MB in every run (largest 0.066 MB, run 2). The storage bucket in the run JSON
   (`storage_explicit_all_processes`, `indexeddb_explicit` in runs 1/2) sums storage-like paths of
   all processes and is context only. A first `padEnd` fixture produced shared ropes; invalid.
3. **Additional peak (Linux):** condition: `minimizeMemoryUsage` immediately before resetting the
   extension process high-water mark (`/proc/<pid>/clear_refs` = 5), nothing in between; then run
   the operation and read `VmHWM`. Baseline is the process RSS at reset, which after minimize is the
   resting process state; the add-on's resting attributable value comes from (1).
   - Detection: a 24 MiB typed-array pulse gave +25.5 to +25.8 MB (runs 1–4); a point reporter
     sample after the pulse never sees it.
   - Undercount risk (free-but-resident reuse), runs 3/4: after dropping 32 MiB of small strings,
     a 24 MiB small-string pulse gave only +29.1/+29.2 MB **without** minimize before the reset,
     but +39.9/+40.9 MB **with** minimize. Reuse of resident freed memory therefore causes real
     undercount, and the minimize condition removed it in these trials.
   - Status: a measured procedure with a stated condition and demonstrated sensitivity, **not** a
     proven upper bound. Final F05 peak claims must additionally cross-check against paired
     whole-cgroup `memory.peak`/RSS evidence; an unexplained discrepancy blocks a PASS.
4. **Native/shared residual:** paired A/B cgroup `memory.current`/`memory.peak` and process RSS,
   reported separately and never as zero; not interchangeable with (1) or (3).
5. CPU/I-O/latency/load protocol unchanged from METHOD-01.

## Dispositions of remaining measurement work

| Item | Disposition |
|---|---|
| A/B paired runs without/with WindowSafe | Bound protocol (METHOD-01/02); executed with the real add-on in F05 (r6 §9.1: implementation measurements follow later, before Feature Acceptance). Not run here. |
| Instrument overhead and paired uncertainty | Minimize/report run outside measured intervals by protocol; `clear_refs` is a single write. Overhead on/off and pair variance are measured and reported in F05; OPEN until then. |
| Windows add-on hard-peak instrument | OPEN — the only F01 gate left; [handoff](closure2-windows-handoff.md). |
| Windows complete short-lived PID identity coverage, final interval boundaries | OPEN for F05 Windows measurements; Job aggregate lifetime accounting is already qualified. |

## Gate dispositions

| Gate | Disposition |
|---|---|
| WS-P05 fallback | CLOSED on Ubuntu; Windows reused (same API class and path) |
| SPECIAL_NATIVE_GUI_CASES (Ubuntu display/state) | CLOSED with recorded Wayland limits |
| WINDOWS_DESKTOP | Its WebApp boundary part is answered by WS-P05 and (a); its remaining measurement part is tracked as the Windows peak gate below |
| MEASUREMENT_FINAL_ATTRIBUTION | Ubuntu: method qualified with conditions (METHOD-02); Windows add-on hard peak OPEN |
| TARGET_EQUIVALENT_RESTART | Remains CLOSED, not repeated |

Pre-implementation consequence (TF §§9.1/9.3): the measurement method must be bound for both
target OSes before the affected product implementation (F02). F01 therefore stays open until the
Windows peak instrument run is recorded. No F02 product code starts before that.
