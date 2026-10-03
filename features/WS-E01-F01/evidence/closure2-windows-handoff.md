# F01 closure — Windows add-on hard-peak instrument run (handoff)

> **PAUSED (2026-10-03):** user decision WS-UD-20261003-01
> (`epics/WS-E01/evidence/user-decision-ws-ud-20261003-01.json`, option 2) would remove Windows
> performance/resource evidence if the resulting Technical Foundation delta, WS-E01 Epic Preparation
> delta, independent rereview and exact rebinding complete. Until then, do not start any section of
> this handoff (including the closure2 (d) platform check); it may be superseded afterwards.

Purpose: close the F01 items that need the bound Windows Desktop target: an add-on-only
hard-peak memory instrument, Windows calibration (known uncertainty), measurement interval
boundaries and short-lived PID identity coverage. Status of all F01 items: [closure2.md](closure2.md). Authorization: WS-EA-20261001-03
(`epics/WS-E01/evidence/broad-execution-authorization.json`). Qualification only: synthetic
disposable profile, no real profile, no product code, no installer/default/signing changes.

## Start

On the Windows host previously bound for F01 (Windows 11, host `Boss`), in a clean checkout of
`felixvonvollmer-png/Firefox---WindowSafe`: create a new branch from the current `main` (which
contains this handoff). Verify repository, main head, clean worktree/index, Python 3.14.4.
Use the already bound Firefox 156.0 Stable Windows binary (build 20260909172920, SHA-256
`ce320f543a353bb55c6804af320df0b7807eb3feb822ea093a1ae7164c066970`, see
[win-stable-download.json](win-stable-download.json)); re-download into `build/f01` only with
that exact hash if absent.

## Instrument to add (qualification/ws-e01-f01/, Windows branch of closure_probe.py or a sibling)

Reuse `closure_probe.py` (driver operations `map-cache`, `idb-fill`, `release`, `pulse`) and
`windows_job.py` (owned launch Job). Add for Windows:

1. Identify the single `extension` child via `ChromeUtils.requestProcInfo()`; verify it belongs to
   the owned launch Job (`IsProcessInJob`).
2. Before each measured operation, call `minimizeMemoryUsage` and immediately afterwards (nothing
   in between) create a new measurement Job, assign only the extension process to it (nested Job),
   read `PagefileUsage`/`PrivateUsage` at assignment, run the operation, then read
   `JOBOBJECT_EXTENDED_LIMIT_INFORMATION.PeakProcessMemoryUsed`. Report
   `peak - commit_at_assignment` as the measured additional peak under that condition (not a proven
   upper bound). Close the measurement Job without kill-on-close.
3. Same coverage contrasts as Ubuntu with `minimizeMemoryUsage` before each report: baseline,
   8 MiB flat Map strings, 8 MiB IndexedDB read-back, release (back to baseline), a 24 MiB
   held-only typed-array pulse, and the two reuse trials of runs 3/4 (`hold-strings` 32 MiB,
   `drop`, then a 24 MiB `pulse-strings`, once without and once with minimize before the Job
   assignment).

## Pass criteria for the instrument (not a product claim)

- Pulse: measurement-Job peak delta >= 25,165,824 bytes and the post-pulse point reporter
  sample does not see the pulse (shows peak capture beyond sampling).
- Reuse trials (at least three repetitions, alternating order, plus a fresh-state control
  without prior hold/drop): the with-minimize delta must be >= the fresh-state control delta
  minus 2 MiB and >= the without-minimize delta; record all values. A with-minimize delta below
  the fresh-state control by more than 2 MiB is residual undercount and keeps the gate OPEN.
- Baseline repeat without operation: peak delta small relative to 8 MiB (record value).
- Contrasts: reporters see Map and IndexedDB data, release returns to baseline.
- Two complete runs with consistent results. If nested assignment, peak semantics or extension
  process identification fail, record the failure as OPEN evidence; do not substitute sampling.

## Windows calibration and intervals (same session)

**Precondition:** do not run this section until the Ubuntu calibration instrument is qualified,
in particular until the two-mode workload cost of closure2 (e) is explained and controlled or
detected as an invalidity, and the instrument revision that does so is on `main`. The peak
instrument above and the platform check below do not depend on this and may run first.

`calibration_probe.py` is a Linux-only (cgroup v2, /proc, Wayland compositor), not yet qualified
candidate (see closure2 dispositions). Port the qualified revision for Windows before running it,
keeping its protocol constants and invalidity rules unchanged: owned launch Job
(`windows_job.py`) instead of the cgroup; Job basic accounting (`TotalUserTime+TotalKernelTime`) at
exact interval boundaries instead of `cpu.stat`; parent-process CPU via `GetProcessTimes`; the
desktop compositor (`dwm.exe`) reported separately instead of gnome-shell/Xwayland; foreign host load
from `GetSystemTimes` over 5 s windows. Then run it: A/A pairs (both without
add-on) for R500 and R2000 over L10 600 s, the B300 window and idle 600 s (both profiles), at least five
pairs each, alternating order, host load recorded. Record interval boundaries as Job counter
reads (`QueryInformationJobObject` basic accounting) at exact start/end, and the lifetime vs
sampled process identity counts per interval; any uncovered short-lived process is reported,
not dropped. Quiet visible desktop, no other user activity during runs.

## Discarded tabs in groups (platform finding check)

Repeat the closure2 (d) observation on Windows with a Windows port of the current candidate (values
count as platform observation only, not calibration; this check is not behind the calibration
precondition), recording
whole-Job and parent-process CPU 60 s after API realization of R500 (discarded tabs, groups) and again
after a normal quit and native session restore (fields `api_realized_settled_10s`,
`native_restored_settled_10s`). Record the values; do not rely on the uncommitted Ubuntu isolation
indications.

## Deliver

Add `features/WS-E01-F01/evidence/closure2-windows-run1.json`, `-run2.json`, an artifact-hash
file and a short `closure2-windows.md` (environment, results, limits). Run
`python3 tools/foundation.py check` and the qualification tests, commit only those paths plus
the instrument source, push the new branch, open a PR to main, and stop. No verdict, no
acceptance, no merge.
