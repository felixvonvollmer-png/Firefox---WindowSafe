# F01 measurement-method binding — PARTIAL, preimplementation gate OPEN

Method ID: WS-E01-F01-METHOD-01. This document and the scripts are byte-bound by
[continuation manifest](continuation-manifest.json). Normative targets remain Technical
Foundation r6 §§9.1/9.3 and the exact T05-R2 input; no threshold is changed.
This binds the protocol and the executed Ubuntu instrumentation substeps. It does not
claim complete Windows instrument qualification or F05 product performance acceptance.

## Systems and workload identity

Ubuntu system: [environment](environment.json); exact browser build/binary/archive hashes
and GUI mode: [Stable evidence](ubuntu-stable-cgroup.json), [download](firefox-stable-download.json).
Windows Desktop OS/build, CPU topology/model, RAM, storage/filesystem, exact Firefox
binary/build and display configuration MUST be filled from the target environment before
measurement. Windows Server CI is static toolchain evidence only. The six-core Ubuntu host
is not a surrogate for Windows. Power governor, AC/battery state, thermal state and concurrent
background load must be recorded at every final measurement; do not silently tune the host.

`qualification/ws-e01-f01/fixtures.py` generates deterministic R500 (10 windows) and
R2000 (20 windows): each URL 160 UTF-8 bytes, title 80 ASCII characters, distinct synthetic
identities, active/pinned/muted/container/group mixture. H adds 14 distinct checkpoints,
5% changed tab records per checkpoint, and 50 closed windows containing 50/100 tabs.
These are test inputs, not a product schema or recovery implementation. Browser realization
must verify actual window/tab/group/container counts and preserve semantic equality between A/B.
Long Unicode addresses, duplicate URLs with distinct IDs, unresolved histories and large imports
form separate adversarial fixtures; never use URL equality to reduce identity cardinality.

## Paired final protocol

For each OS and each R500/R2000 profile, both without and with H where relevant, collect
at least FIVE valid A/B pairs. A is the identical synthetic browser workload without the
future WindowSafe addon; B differs only by that addon. Fix OS/browser/hardware, fixture hash,
permissions, native restore preferences, page contents and cache policy. Use fresh synthetic
profiles cloned only from the generated synthetic seed. Alternate pair order AB/BA, record seed,
and keep all attempts, including invalid and failed runs. Do not pool OSes or profiles.

Warm up for 60 seconds after synthetic fixture realization, then wait for explicit driver
readiness and documented quiescent application acknowledgements. A wall-clock timeout is a
failure, never proof that native restore completed. No CPU benchmark begins during startup.
Record non-test system CPU and load for 30 seconds before and during each run. Predeclare
background-load interference (>5% of total machine CPU sustained 5 seconds), driver disconnect,
incomplete counter coverage, lost fixture events, wrong counts/builds or trace loss as invalid
measurement attempts; retain their raw results. Product loss/late persistence is a product
failure, not an exclusion. OS pauses, suspend and I/O failures are separately reported and may
not be used to discard slow normal runs after seeing results.

## CPU, process attribution and OS counters

Normalize as `100 * (CPU_B_seconds - CPU_A_seconds) / wall_seconds`, in percent of ONE
CPU core, without dividing by logical processor count. Preserve negative/noisy differences;
report pair values and uncertainty, not clipped zero. Pair CPU deltas cover the same interval.

Ubuntu final direction: launch ONLY the owned Firefox instance in a unique transient
`systemd-run --user` service with CPU/Memory/IOAccounting enabled. Read its ControlGroup and
MainPID; verify the Marionette process and disposable profile against the launcher. All Firefox
children must remain in that cgroup. Read cgroup v2 cpu.stat usage_usec at interval boundaries;
this includes exited children and avoids /proc polling loss. Read memory.current/memory.peak,
io.stat, and cgroup.procs separately. A failed delegation, child escape or missing counter
is an OPEN instrument gate, not zero consumption. No sudo, host tuning or global unit.
`cgroup_dry_run.py` demonstrates counter deltas for an owned 0.5 CPU-second / 4-MiB synthetic
worker and stops only its unique transient unit. [Actual dry-run](ubuntu-cgroup-dry-run.json).
The same cgroup launcher was then exercised with actual Firefox Stable and a two-launch Developer
restart. [Stable cgroup evidence](ubuntu-stable-cgroup.json) and
[restart cgroup evidence](ubuntu-restart-cgroup.json) bind interval deltas and raw samples.
These short synthetic intervals qualify accounting, not the final product workload.

`measure.py` additionally records timestamped process-tree identities, user+kernel CPU, RSS,
and process I/O. Ubuntu uses /proc PID+starttime; Windows uses Toolhelp32, creation FILETIME,
GetProcessTimes, GetProcessMemoryInfo and GetProcessIoCounters. The live Firefox dry-run proves
Ubuntu collection works; it does not prove final acceptance accuracy. Sampled CPU is a lower
bound when short-lived processes/final ticks are missed; RSS sums can double-count shared pages.

Windows final direction: a dedicated Job Object containing the Firefox root and every child,
with lifetime user+kernel accounting at both boundaries, plus per-process handles/creation times
for memory and I/O. Assignment must precede execution; breakaway/disallowed assignment is a
hard instrumentation failure. QueryInformationJobObject aggregate CPU prevents lost exited-child
CPU. Job launch/accounting has NOT been implemented or qualified in this run. The supplied
Windows process sampler is executable diagnostic continuation tooling, never a substitute for
that final collector. Windows Job qualification is explicitly OPEN before affected implementation.

## Memory, storage, I/O and latency

- Addon JS/DOM/cache: collect verbose Firefox about:memory reports after quiescence, with the
  probe/addon origin identified inside the disposable profile. Record JS compartments, DOM and
  caches separately from native/process memory. Avoid attributing shared/native residual to the
  addon as zero. Use matched A/B process RSS/private bytes plus cgroup charged memory or Windows
  working set/private bytes. Unexplained material overhead prevents an unqualified resource PASS.
- Logical data: byte length of compact UTF-8 JSON, current state separate from H and complete
  uncompressed reference export. Do not infer RAM from JSON bytes. Instrument product write
  record count and logical bytes separately from OS I/O calls/transfer bytes and physical device
  I/O. Windows transfer counts and Linux wchar are not SSD writes. Missing io.stat device
  attribution is UNKNOWN. Read only the test profile's IndexedDB files after a checkpoint and
  clean close; report file bytes/allocated blocks before and after, WAL/journal separately.
- Future persistence latency: monotonically timestamp event receipt, transaction submission and
  successful commit acknowledgement; record event identity through coalescing and maximum age.
  An API request or error response is not persistence success. Report nearest-rank p95 and max,
  every input event accounted for. No IndexedDB product path exists in F01.
- L10: 600 seconds, 10 actually processed relevant changes/second (6000), predeclared schedule.
  Count delivered, observed and persisted changes; CPU PASS with loss/delay is invalid.
  Pair medians <=10% / <=20%; every valid pair <=15% / <=30% (R500/R2000).
  The 5% / 10% soft targets alone never fail acceptance.
- B300: 300 relevant changes over 3 seconds; fixed 10-second measurement window including
  trailing time. Average additional CPU <=20% / <=40%; persist within 2/3 seconds after the last
  event and maximum unsaved age 5/6 seconds. No shifting the time window after measurement.
- Idle: 600 seconds of responding browser, no synthetic events or open addon UI; average
  additional CPU <=0.1% one core. Record any addon work, scans and writes rather than hiding them.
- UI-list: future user activation to visible AND operable window list, at least 20 activations per
  pair; nearest-rank p95 <=250/500 ms, without eagerly loading every historical tab detail.
- Export/import: record resting addon-attributable baseline, continuous allocation/profile trace
  and OS peak counters through completion; additional peak <=8/16 MiB. Sampling alone cannot
  prove a hard peak; trace coverage, overhead control and addon attribution remain OPEN.

Unchanged r6 memory/logical thresholds: live attributable JS/DOM/cache 8/24 MiB; current compact
logical data 1/4 MiB; recovery data including H and uncompressed reference export each 8/32 MiB.
Ordinary persistence latency p95 1/2 seconds and max 2/3 seconds. 1 MiB = 1,048,576 bytes.
Safety and every resource/latency target apply simultaneously.

## Uncertainty and closure

Report timer resolution, sampling interval, profiler overhead, pair variance, OS accounting
semantics, missing attribution and all trace gaps. Do not claim that synthetic worker memory
or Firefox's total RSS meets an addon threshold. No real product benchmark has run.

OPEN: Windows Desktop/job accounting; addon-attributable memory
and peak trace qualification; full hardware/background/power binding for both final systems.
The executable diagnostic/dry-run tools and protocol are ready for continuation; the overall
WS-GATE-MEASUREMENT remains REQUIRED_BEFORE_AFFECTED_PRODUCT_IMPLEMENTATION.
