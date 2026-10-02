# F01 closure — Windows add-on hard-peak instrument run (handoff)

Purpose: close the only remaining F01 item that cannot be produced on Ubuntu: an add-on-only
hard-peak memory instrument on the bound Windows Desktop target. Everything else in F01 is
closed or reused ([closure2.md](closure2.md)). Authorization: WS-EA-20261001-03
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
- Reuse trials: with minimize, the string-pulse delta must not be materially below the logical
  string bytes; record the without-minimize value to show sensitivity, as on Ubuntu.
- Baseline repeat without operation: peak delta small relative to 8 MiB (record value).
- Contrasts: reporters see Map and IndexedDB data, release returns to baseline.
- Two complete runs with consistent results. If nested assignment, peak semantics or extension
  process identification fail, record the failure as OPEN evidence; do not substitute sampling.

## Deliver

Add `features/WS-E01-F01/evidence/closure2-windows-run1.json`, `-run2.json`, an artifact-hash
file and a short `closure2-windows.md` (environment, results, limits). Run
`python3 tools/foundation.py check` and the qualification tests, commit only those paths plus
the instrument source, push the new branch, open a PR to main, and stop. No verdict, no
acceptance, no merge.
