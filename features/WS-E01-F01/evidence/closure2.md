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
without testing undercount, and it said sizes requested after creation are ignored, which no
committed run supports (an error of the report, not of the runs). After the second review
WS-E01-TR-PR7-20261002-02 the deferral of measurement-uncertainty and Windows interval items to
F05 was withdrawn: they are F01 pre-implementation work (TF §§9.3/10.2). Runs 3 and 4 use a
corrected instrument; runs 1 and 2 remain as historical evidence.

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
  decorations); sizes requested later are applied in all four runs (800x600, then 850x600; in
  runs 3/4 immediate and settled read-backs are equal).
- States: `maximized`, `normal`, `fullscreen` complete and report correctly. The maximized size
  was 1920x1080 in runs 1/2 and 1853x1048 in runs 3/4; the cause is not determined.
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
     a 24 MiB small-string pulse gave +29.1/+29.2 MB **without** minimize before the reset, but
     +39.9/+40.9 MB **with** minimize (an independent rerun: 32.2/36.1 vs 40.9/41.4 MB). Reuse of
     resident freed memory causes real undercount; the condition **reduced** it in these trials.
     Runs 3/4 had no fresh-state control and a fixed order. The 12 committed calibration smoke runs
     add alternating order and a fresh-state control: with-minimize was between 1.23 MB below and
     2.97 MB above the fresh-state control and 9.6 to 16.7 MB above without-minimize; all 12 meet
     the declared reuse pass rule by manual evaluation (the instrument does not evaluate it yet).
     Small n; absence of residual undercount is not shown.
   - Status: a measured procedure with a stated condition and demonstrated sensitivity, **not** a
     proven upper bound. Binding cross-check rule for every later peak claim: the paired
     whole-cgroup `memory.peak` difference (B−A, same operation) is reported next to the VmHWM
     delta; if it exceeds the VmHWM delta by more than max(2 MiB, 25 %), the peak claim is not a
     PASS until the difference is explained.
4. **Native/shared residual:** paired A/B cgroup `memory.current`/`memory.peak` and process RSS,
   reported separately and never as zero; not interchangeable with (1) or (3).
5. CPU/I-O/latency/load protocol unchanged from METHOD-01.

## (d) Platform finding: API-created discarded tabs in tab groups load the browser

Recorded in the calibration smoke runs ([smoke](closure2-calibration-smoke.json),
[smoke2](closure2-calibration-smoke2.json), [smoke3](closure2-calibration-smoke3.json); fields
`api_realized_settled_10s` and `native_restored_settled_10s`, smoke2/3 also with parent-process CPU):
after an extension realizes R500 with `tabs.create({discarded:true})` and groups those tabs, the
owned browser stays at about 110-115 % of one core after 60 s of rest in all 12 smoke runs, and in
smoke2/3 the parent process carries essentially all of it (e.g. 114.1 of 114.5 %). After a normal
quit and native session restore of the same windows, groups and discarded tabs it was near idle in
11 of 12 runs (0.05-1.2 %), but in one run (smoke2 `p1-second`) the same load appeared after the
native restore (124 %, parent 124 %) and persisted through all later intervals. The trigger is
therefore not shown to be exclusive to the API path.

Exploratory isolation runs during development (one window; group size, collapse, containers, mute,
titles, discard-after-grouping) are LOCAL_AGENT_REPORTED only and were not committed; they are not
evidence here. Their indications (a group of about nine such tabs suffices; grouping loaded tabs and
discarding afterwards stays quiet) must be reproduced as committed evidence before anything relies
on them.

Consequences, within existing Product Truth and Technical Foundation (no new decision):
- Calibration and later A/B workloads realize R500/R2000 through a native restart, so the measured
  browser is in a state after start; the load is recorded in every run, and a run that is not
  quiescent before the intervals is invalid (smoke2 `p1-second` was rejected this way).
- **Bound F03 pre-implementation obligation (TF §7.1):** before the F03 restore implementation
  starts, qualify a restore order that keeps background tabs unloaded (WS-RESTORE) **and** leaves
  the browser quiet (r6 §9.1 idle target). If no such order exists on the target builds, F03 restore
  of grouped background tabs STOPs for a user decision; neither silent mass loading nor leaving the
  browser loaded is an allowed agent fallback.
- Windows was not tested for this; the Windows handoff includes it.

## (e) Measurement-method finding: the same workload runs in two cost modes (cause undetermined)

In the smoke runs the same R500 L10 workload cost either about 2 % or about 24 % of one core per
run (smoke2: both modes inside one pair, p0 at 2.18 % vs 24.05 %; smoke3 `p0-first` 1.95 %). On
this Wayland session all browser windows report and keep position 0,0 and overlap; a plausible
but **unverified** explanation is whether the windows whose tab strips the workload changes are
actually visible (other application windows or browser stacking). The instrument's `front` step
asks Firefox to focus a fixed fixture window and reads Firefox's own focus state; it does **not**
verify what is on top of the desktop, and smoke3 `p0-first` ran in the low mode despite
`front.ok`. The cause is therefore undetermined and **not controlled**; the instrument does not
detect the mode, and smoke2 even accepted the mixed pair p0 as valid (21.9 pp difference). Until
the cause is identified and either controlled or detected as an invalidity, no calibration result
from this instrument can bind the known uncertainty. Working condition for that investigation and
for the calibration: an exclusive, quiet desktop with no other application windows or workloads.

## Dispositions of remaining measurement work

| Item | Disposition |
|---|---|
| A/B paired runs with the real add-on | Executed in F05 against the bound protocol (r6 §9.1: implementation measurements before Feature Acceptance). |
| Ubuntu calibration: instrument/driver overhead and known uncertainty | **F01 OPEN** (TF §9.3: bound before F02). Instrument **candidate, not qualified**: the unexplained two-mode workload cost (e) must be resolved first; further known gaps from TR-PR7-04: post-restart state checks are incomplete (container baseline, window count, per-tab container/pinned/muted/discarded state, extra tabs, `observedEvents` not compared), the reuse pass rule is not evaluated by the summary, L10 runs 601 s and B300 ends on a 1 s sample (10.1 s) without declaration, power/thermal state and timer resolution are not recorded, and smoke2 was produced by an uncommitted instrument version (calibration probe SHA-256 `01e654d5…` in its record). Also not yet covered: the code that produces the invalidity reasons (post-restart state comparison, quiescence acknowledgement, foreign-load windows, front step) is untested (surviving mutants per TR-PR7-04 §5), the previous session's restored driver tab is not declared, and two closure-probe mutants survive (M9 prefix filter, M11); `ancestor()` still raises `CalledProcessError` instead of a named rejection (open; historical tests expect it). What is implemented: the summary's evaluation of each invalidity reason, unit-tested per rule ([smoke run](closure2-calibration-smoke.json), shortened intervals; smoke values are instrument evidence, not the calibration). Declared calibration constants: at most 0.1 % of scheduled events late by more than 100 ms; foreign host load (beyond the owned cgroup and the compositor) judged over every 5 s window against 5 % of all cores; quiescence acknowledgement below 3 % of one core over 10 s (max 6 attempts) instead of a bare timer; one `minimizeMemoryUsage` before the CPU intervals as a declared condition; driver errors, lost or late events, missing fixture tabs, group-count mismatches, non-quiescence and failed runs make the pair invalid and are listed (the container check and the window count after the restart are not yet effective; the window count at realization is compared). Instrument overhead: the sampler runs outside the owned cgroup and reports its own CPU per interval (`instrument_self_cpu_pct_one_core`); Marionette's idle session inside the browser is identical in A and B and is not separately quantified. Reuse-trial pass rule (Ubuntu and Windows): with-minimize >= fresh-state control − 2 MiB and >= without-minimize; A/A pairs (both without add-on) over the real L10 600 s interval, B300 window and idle 600 s for R500 and R2000, plus repeated reuse trials with order alternation and a fresh-state control; instrument [calibration_probe.py](../../../qualification/ws-e01-f01/calibration_probe.py). Needs a multi-hour quiet visible-desktop window on the Ubuntu host. |
| Windows add-on hard-peak instrument | **F01 OPEN**; [handoff](closure2-windows-handoff.md). |
| Windows calibration, interval boundaries, short-lived PID identity coverage | **F01 OPEN**; same handoff. Job aggregate lifetime accounting is already qualified. |

## Gate dispositions

| Gate | Disposition |
|---|---|
| WS-P05 fallback | CLOSED on Ubuntu; Windows reused (same API class and path) |
| SPECIAL_NATIVE_GUI_CASES (Ubuntu display/state) | CLOSED with recorded Wayland limits |
| WINDOWS_DESKTOP | Its WebApp boundary part is answered by WS-P05 and (a); its remaining measurement part is tracked as the Windows peak gate below |
| MEASUREMENT_FINAL_ATTRIBUTION | Ubuntu: memory method defined with conditions (METHOD-02), calibration OPEN; Windows OPEN |
| TARGET_EQUIVALENT_RESTART | Remains CLOSED, not repeated |

Pre-implementation consequence (TF §§9.1/9.3): the measurement method must be bound for both
target OSes, including known uncertainty, before the affected product implementation (F02). F01
therefore stays open until the Ubuntu calibration and the Windows runs are recorded. No F02 product
code starts before that.
