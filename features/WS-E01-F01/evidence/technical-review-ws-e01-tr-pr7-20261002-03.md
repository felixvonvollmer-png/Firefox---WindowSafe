# WS-E01-TR-PR7-20261002-03: Independent Technical Rereview of PR #7

- Reviewer identity: CLAUDE_SUBAGENT_INDEPENDENT_TECHNICAL_REVIEWER_WS_E01_TR_PR7_20261002_03
- Review type: technical review (Foundation 2 §30, ELEVATED risk increment). This is not a Feature
  Acceptance and not an epic verdict.
- Repository: felixvonvollmer-png/Firefox---WindowSafe, PR #7, branch `feature/ws-e01-f01-closure`
- Reviewed head SHA: `9bbbb1bcccb338980fc0019b194ea6d19e313c3f`
- Base (main): `f83845a1dd4b78bd010e6477612d95a99b1a8152`
- Reviewed diff: `git diff f83845a1dd4b78bd010e6477612d95a99b1a8152 9bbbb1bcccb338980fc0019b194ea6d19e313c3f`
  (133 files; commits `8ae803d`, `d2fd8c9`, `9b017dd`, `9bbbb1b`, single-parent chain on `f83845a`)
- Date: 2026-10-02

## Independence statement

I am a freshly started subagent with no prior context on this change. I did not author,
materialize or contribute to PR #7, PR #3, PR #6, the earlier technical reviews
(WS-E01-TR-PR6-20261001-01/-02, WS-E01-TR-PR7-20261002-01/-02) or any WS-E01 preparation,
correction, rebinding or authorization artifact. I read TR-PR7-01/-02 only as committed subject
files. There was no expected outcome.

Worktree hygiene: `/home/felix/projekte/windowsafe-review-pr7c` was used read-only.
`git rev-parse HEAD` was `9bbbb1bcccb338980fc0019b194ea6d19e313c3f` and
`git status --porcelain --ignored` was empty before and after the review. CLI gates ran with
`PYTHONDONTWRITEBYTECODE=1`. The full test suite and all mutants ran only in disposable clones
under the session scratchpad; each mutant was reverted with `git checkout` and the mutation clone
was left clean. `/home/felix/projekte/firefox WindowsSaver addon` was not touched. No pushes, no
gh mutations, no browser launched (the optional calibration run was not performed; see §6).

## 1. Commands run (python3 3.14.4)

In the worktree at the reviewed head:

| Command | Exit |
| --- | --- |
| `python3 tools/foundation.py check` | 0 (CHECK OK) |
| `python3 tools/foundation.py history --base f83845a1dd4b78bd010e6477612d95a99b1a8152` | 0 |
| `python3 tools/foundation.py history --base 1cb82c926903b2fd6b497d008db61c71c5d92aca` | 0 |
| `python3 tools/foundation.py request --sha HEAD --subject epics/WS-E01/deltas/WS-E01-EP-DELTA-20260929-04/subject.json` | 0 |
| `python3 tools/foundation.py request --sha HEAD --subject epics/WS-E01/deltas/WS-E01-EP-DELTA-20260929-03/subject.json` | 0 |
| `python3 tools/foundation.py request --sha HEAD --subject epics/WS-E01/deltas/WS-E01-EP-DELTA-20260929-02/subject.json` | 0 |
| `python3 tools/foundation.py request --sha HEAD --subject epics/WS-E01/subject.json` | 0 |
| `python3 tools/foundation.py request --sha HEAD --subject foundation/deltas/WS-PFDELTA-MAT-20260928-01/subject.json` | 0 |
| `python3 tools/foundation.py schema-preflight --sha HEAD --schema reviews/review-contract.json` | 0 (SCHEMA-PREFLIGHT OK) |
| `git diff --check f83845a HEAD` | 0 |
| `git diff --quiet f83845a HEAD -- <each of the five subject.json>` | 0 for all five (byte-identical to base) |

In scratch clones at the reviewed head:

| Command | Exit |
| --- | --- |
| `python3 -m unittest discover -s tests -v` (full suite) | 0 (Ran 215 tests in 846 s, OK skipped=6; clone clean afterwards) |
| 8 mutants against `tests.test_closure_probe` (table §5) | see table |
| direct calls of `calibration_probe.summarize()` with synthetic run records (§4, F1) | 0 (behavior recorded in F1) |

## 2. Exact-head CI

`gh run list --commit 9bbbb1bcccb338980fc0019b194ea6d19e313c3f`, waited with `gh run watch`
until completed, then read-only `gh run view <id> --json ...` and `gh run view <id> --log`:

| Run ID | Event | Workflow | headSha | Conclusion | Notes |
| --- | --- | --- | --- | --- | --- |
| 37064362626 | pull_request | Foundation | `9bbbb1b...` | success | checkout `HEAD is now at 9bbbb1b`; CHECK OK; Ran 215 tests OK (skipped=6, 1214 s); SCHEMA-PREFLIGHT OK; 8x VALIDATE-RESULT OK; five exact request steps success; BUILD OK; history and whitespace/clean-tree steps success |
| 37064357246 | push | Foundation | `9bbbb1b...` | success | same 17 steps all success; Ran 215 tests OK (skipped=6, 1212 s) |

## 3. Transfer, bookkeeping and evidence binding

- Byte-identical transfer: for every path in the cumulative diff I compared the blob at
  `9bbbb1b` with `7d66ca5`. All transferred F01/qualification paths are blob-identical. Paths
  differing from or absent in `7d66ca5` are exactly the expected continuation files:
  `state.json`, `closure2*.{md,json}`, `closure2-calibration-smoke.json`, the two TR-PR7 review
  copies, `closure_probe.py`, `calibration_probe.py`, `tests/test_closure_probe.py`, and the
  non-feature harness paths `tools/foundation.py`, `tests/test_epic_execution.py`,
  `foundation/engineering.md`, `epics/WS-E01/evidence/technical-review-ws-e01-tr-pr6-20261001-02.md`.
  (`tests/test_feature.py` from PR #3 is a non-F01 harness file not carried over; not a transfer
  defect.)
- Review copies: `technical-review-ws-e01-tr-pr7-20261002-01.md` and `-02.md` are byte-identical
  to `/home/felix/projekte/windowsafe-review-out/WS-E01-TR-PR7-20261002-01.md` / `-02.md`
  (SHA-256 `3872ccdf...` / `815daeed...`).
- `state.json.evidence_paths`: 131 entries, all exist; the only tracked F01/qualification file
  not listed is `state.json` itself.
- `calibration_probe_sha256` in `closure2-calibration-smoke.json` is
  `a6d987063581e763ef64bad5006274495d3b6500d3dbd7a8ede6fa552ac9a831`, equal to the committed
  `calibration_probe.py`; its `driver_sources` hashes equal the committed `run_probe.py`,
  `target_probe.py`, `measure.py`, `windows_job.py`. Run records 1-4 still match
  `closure2-artifacts.json`. The smoke run has no entry in `closure2-artifacts.json` (F6).
- F01 status: `WS-E01-F01_OPEN__CALIBRATION_AND_WINDOWS_RUNS_REQUIRED`,
  `product_implementation_started: false`, `merge_authorized: false`, three open measurement
  gates. F01 is correctly NOT complete, and no F02 product code exists.

## 4. Claims versus committed JSON (`closure2-calibration-smoke.json`)

| Claim | Status |
| --- | --- |
| Smoke: R500, 2 pairs, L10 20 s, idle 10 s; all 2000 events on time | Supported (4 runs x (200 L10 + 300 B300), `delivered == scheduled`, `late == 0`) |
| Valid pair differs by 0.27 % (L10), 0.10 % (B300), 0.001 % (idle) of one core | Supported (0.2687 / 0.0968 / 0.00096) |
| Other pair rejected for 5-11 % foreign host load | Supported (p0 `other_host_pct_all_cores` 5.1-10.8) |
| Reuse: "with-minimize equals the fresh-state control within 1 MB" | NOT supported in 3 of 4 runs; see F3 |
| Reuse: "without-minimize is about 11 MB lower" | Approximately supported (9.7 / 11.0 / 11.5 / 12.0 MB below fresh-control) |
| (d) API-realized vs native-restored contrast | Core contrast supported at cgroup level: `api_realized_settled_10s` 110.1-114.5 % of one core (60 s rest) vs `native_restored_settled_10s` 0.066-0.094 % |
| (d) "parent process at about 113-134 %", "15 s to 240 s of rest", per-process isolation (9-tab group suffices, 2-tab group quiet, loaded-then-discarded quiet, collapse/container/mute/title invariance), "45-451 pending tabs", "0.1-1.4 %" | NOT in any committed record; see F2 |

TF ordering: the last commit returns Ubuntu calibration (overhead and known uncertainty), Windows
calibration, interval boundaries and PID identity coverage to F01 `open_gates`, keeps only the
real-add-on A/B runs for F05, and states that no F02 product code starts before these are
recorded. This matches r6 §§9.1/9.3/10.2 and preparation §4 item 3. No gate is closed beyond
evidence at this head.

## 5. Mutation probes (scratch clone, `python3 -m unittest tests.test_closure_probe`)

| Mutant | Result |
| --- | --- |
| M9 `origin_explicit` without the `explicit/` prefix filter | survived |
| M10 remove `minimize()` immediately before the closure pulse `reset_high_water` | killed (new structural test) |
| M11 `closure_probe.py` reuse trial never minimizes (`if clean: pass`) | survived |
| M13 `calibration_probe.py` with-minimize arm never minimizes | killed (new structural test) |
| M14 `summarize()` without the late/lost-event invalidity | survived |
| M15 `summarize()` without the interference invalidity | survived |
| M16 fresh-control also does hold/drop | survived |
| M17 pair difference forced to 0 | survived |

## 6. Status of earlier findings

TR-PR7-01: F2-F6 were resolved per TR-PR7-02 and nothing at this head reopens them. TR-PR7-01-F1
(VmHWM delta claimed as upper bound) was PARTIALLY RESOLVED in TR-PR7-02 under the condition that
the F05 cross-check be operationalized and carried as a binding open item. That condition is now
met (max(2 MiB, 25 %) rule in `closure2.md` (c)3, carried in
`bound_obligations_for_later_features.F05`), and the residual-undercount wording is handled under
TR-PR7-02-F2. TR-PR7-01-F1 is therefore RESOLVED. The small consistent residual visible in the
smoke run is new F3.

| TR-PR7-02 finding | Status | Evidence |
| --- | --- | --- |
| F1 MAJOR: overhead/uncertainty and Windows intervals deferred to F05 | RESOLVED | `open_gates` now holds `MEASUREMENT_UBUNTU_CALIBRATION__OVERHEAD_AND_KNOWN_UNCERTAINTY`, `MEASUREMENT_FINAL_ATTRIBUTION__WINDOWS_ADDON_HARD_PEAK`, `MEASUREMENT_WINDOWS_CALIBRATION_INTERVALS_AND_PID_COVERAGE`; `open_for_f05` replaced by `bound_obligations_for_later_features` with only real-add-on A/B for F05; `required_next_gate` names the Ubuntu calibration and Windows session; handoff extended. The instrument offered for the returned gates has its own defects (new F1, F4). |
| F2 MINOR: reuse wording; F05 cross-check not operationalized | RESOLVED | "reduced ... absence of residual undercount is not shown"; cross-check rule now concrete (paired cgroup `memory.peak` B-A vs VmHWM delta, block if larger by more than max(2 MiB, 25 %)) and carried in the F05 obligation. |
| F3 MINOR: Windows reuse pass rule non-discriminating | RESOLVED in substance | Fresh-state control with a 2 MiB tolerance and three alternating repetitions; the "with >= without" part is non-discriminating but harmless. Opening sentence aligned. |
| F4 MINOR: run-2 952x702 race misattribution | RESOLVED | Race sentence removed; maximized 1920x1080 vs 1853x1048 recorded as undetermined. |
| F5 NIT | PARTIALLY RESOLVED | TR-PR7-01 copy added to `evidence_paths`; M10 now killed. M9 and M11 still survive; `ancestor()` still raises `CalledProcessError` (no harness change in the last commit). Carried in new F6. |

The optional calibration/closure probe run was not performed: the committed smoke JSON already
establishes the core (d) contrast, the instrument records cgroup-level CPU only and so could not
confirm the per-process/isolation claims, and running it would have competed for host CPU with
the test suite and the visible desktop.

## Findings

### WS-E01-TR-PR7-03-F1

- Severity: MAJOR
- Status: OPEN
- Description: `closure2.md` declares the calibration instrument "ready" for the open gate
  `MEASUREMENT_UBUNTU_CALIBRATION__OVERHEAD_AND_KNOWN_UNCERTAINTY`, but `calibration_probe.py`
  deviates from the bound METHOD-01 protocol, mostly in fail-open directions. Running the
  planned multi-hour calibration with it as-is would produce evidence that does not conform to
  the method it is meant to calibrate:
  1. Invalidity rules (METHOD-01: "driver disconnect, incomplete counter coverage, lost fixture
     events, wrong counts/builds ... invalid measurement attempts; retain their raw results").
     Verified by calling `summarize()` with synthetic records:
     - a driver result `{error: ...}` (no `scheduled` key) makes `late()` falsy, so the pair is
       counted VALID;
     - `realize_mismatch` / `adopt_mismatch` are recorded but never consulted, so wrong counts
       stay VALID; group and container counts are not checked against the fixture at all;
     - a FAILED run without the interval makes the pair disappear from the summary (`continue`),
       neither valid nor listed as invalid;
     - 60 of 6000 events late by more than 100 ms is still VALID (an undeclared 1 % tolerance;
       METHOD-01 says a CPU result with loss/delay is invalid).
  2. Interference rule: METHOD-01 defines ">5% of total machine CPU sustained 5 seconds". The
     instrument compares an interval average with 5 %. In a 600 s interval a sustained 5-30 s
     burst is averaged away. Excluding compositor CPU from "foreign" load is a reasonable but
     undeclared change to the rule.
  3. Warm-up and readiness: METHOD-01 requires warm-up after realization "then wait for explicit
     driver readiness and documented quiescent application acknowledgements. A wall-clock
     timeout is a failure, never proof that native restore completed." The instrument uses only
     `sleep(15)`, `adopt` and `sleep(warmup)` after the native restart, with no restore/quiescence
     acknowledgement.
  4. Undeclared state change: `minimizeMemoryUsage` runs before `pre_host_30s` and the L10/B300/
     idle intervals. This is not part of METHOD-01 or METHOD-02 for CPU. It also contradicts the
     stated rationale that the measured browser is "in the state a user's browser has after
     start" (r6 §10.2: forced cleanup must be declared as a measurement condition).
  5. The gate is named "overhead and known uncertainty", but the A/A design measures only pair
     noise. No step measures instrument/driver overhead (e.g. driver or boundary readers on/off),
     and no argument is recorded that the overhead cancels in A/B (the driver page and its event
     listeners run inside the measured cgroup).
  6. Scope inconsistencies: `closure2.md` plans idle 600 s "for R500 and R2000", but the
     instrument defaults R2000 idle to 0 and the Windows handoff says "(R500) idle". The L10
     interval is `l10_seconds + 1` (601 s) and not declared. The restarted session also restores
     the realize-session driver tab (`nonSynthetic` lists two `moz-extension://.../driver.`
     entries, `windows: 11`); its state in the measured browser is not verified or declared.
  None of this closes a gate at this head. The defect is that the instrument is declared ready
  and the next planned step depends on it.
- Recommended fix: make `summarize()` fail closed: driver `error` or missing counts, any
  `realize`/`adopt` mismatch, group/container count mismatch and FAILED/missing intervals become
  listed invalid pairs. Declare (or remove) the late-event tolerance. Implement the 5-second
  sustained interference rule with periodic host samples inside each interval and declare the
  compositor separation. Add a restore/quiescence acknowledgement instead of wall-clock waits
  only. Drop or declare the pre-interval `minimizeMemoryUsage`. Add an overhead step or a recorded
  argument for why overhead cancels. Align R2000 idle across `closure2.md`, the instrument and the
  handoff. Add unit tests for `summarize()` (M14-M17 should be killed). Then re-record a smoke run.

### WS-E01-TR-PR7-03-F2

- Severity: MINOR
- Status: OPEN
- Description: The new platform finding (d) states more than the committed evidence records. The
  only committed record, `closure2-calibration-smoke.json`, supports the core contrast at
  cgroup level: whole owned cgroup 110.1-114.5 % of one core 60 s after API realization, versus
  0.066-0.094 % after native restore (4 runs, R500). The following are not in any committed
  record:
  - attribution to the parent process (the instrument reads cgroup `cpu.stat` only);
  - the 113-134 % range;
  - "15 s to 240 s of rest";
  - every isolation result: one 9-tab group suffices, a 2-tab group is quiet, loaded-then-discarded
    groups are quiet, collapse/container/mute/title invariance;
  - "45-451 pending tabs" (only 451 is recorded);
  - "0.1-1.4 %" (recorded native values are 0.07-0.09 %; 1.2 % is the post-minimize
    `pre_host_30s`).
  The driver's `noTitle` / `discardAfterGroup` switches are never set by `main()`, so the
  isolation experiments were run with an uncommitted harness. This matters because the Windows
  replication protocol ("one tab group of 9 tabs ... 10 s parent-process CPU") rests on the
  unrecorded isolation result. A Windows false negative from that reduced case could be read as
  "Windows unaffected". The F03 remedy design also depends on whether the cost is in the parent
  process.
- Recommended fix: commit the isolation records (per-process CPU samples, configuration,
  harness source), or reword (d) to the recorded cgroup-level contrast and mark the rest as
  unrecorded exploratory observations. Make the Windows check also repeat the recorded
  configuration (full R500 API realization vs native restore) and not only the 9-tab reduction.

### WS-E01-TR-PR7-03-F3

- Severity: MINOR
- Status: OPEN
- Description: The `closure2.md` dispositions table says "with-minimize equals the fresh-state
  control within 1 MB". The smoke JSON shows with-minimize below fresh-control by 53,248 /
  1,232,896 / 1,212,416 / 1,122,304 bytes. Three of four runs exceed 1 MB, and the sign is
  consistent. This is within the 2 MiB tolerance later set for Windows, but it is a small
  systematic residual, not equality. The Ubuntu calibration has no stated pass criterion for the
  repeated reuse trials (the Windows handoff now has one).
- Recommended fix: report "with-minimize 0.05-1.23 MB below the fresh-state control (consistent
  sign), without-minimize 9.7-12.0 MB below". Bind the same reuse criterion (fresh-control minus
  2 MiB, repetitions, alternating order) for the Ubuntu calibration.

### WS-E01-TR-PR7-03-F4

- Severity: MINOR
- Status: OPEN
- Description: The Windows handoff is not executable as written for its two new sections.
  "Windows calibration and intervals" says to run `calibration_probe.py` on Windows "with the
  owned launch Job", and the (d) section says "`calibration_probe.py` records both values per
  run". But `calibration_probe.py` raises unless `platform.system() == 'Linux'` and
  `WAYLAND_DISPLAY` is set. It depends on `systemd-run` cgroups, `/proc/stat`, `/proc/<pid>/stat`
  (gnome-shell/Xwayland compositor) and `/proc/<pid>/clear_refs`/`VmHWM`. It never realizes the
  9-tab single-group case and never samples parent-process CPU. The Windows session would have
  to author a Windows calibration instrument with no specification for host-load sampling,
  compositor (DWM) separation or the invalidity rules. Unlike the hard-peak section, the handoff
  presents this as existing. The failure would be loud, not silent.
- Recommended fix: either add a Windows branch of the calibration instrument (Job boundary
  counters, host-load sampling, DWM separation, same fail-closed invalidity rules as fixed under
  F1) before the Windows session, or rewrite the handoff as "instrument to add" with an explicit
  specification and pass/invalidity criteria, as was done for the hard-peak instrument.

### WS-E01-TR-PR7-03-F5

- Severity: MINOR
- Status: OPEN
- Description: The F03 consequence of (d) is framed as "within existing Product Truth ... no new
  decision", with the obligation "qualify an unloaded and quiet restore order ... or show the
  limitation". The "no silent mass loading" part is correct (Product WS-RESTORE "Entladene Tabs",
  TF §6.3). Two gaps remain:
  - The "show the limitation" branch is not covered by existing Product Truth. Product Truth
    allows visibly limited property combinations, not leaving the browser parent at more than
    one core after a WindowSafe restore. That CPU would be attributed to WindowSafe in A/B and
    collides with the r6 §9.1 idle target ("durch WindowSafe verursachte CPU ... 0,1 %"). Under
    r6 §7.1 / §9.3 that branch needs a visible material user decision, not an agent-chosen
    limitation.
  - r6 §7.1/§10.2 make API-combination qualification (discarded x group, TF §7 matrix
    "Kombinationen ... tatsächlich prüfen") a pre-implementation duty. The `state.json`
    obligation does not say it must be done before F03 product implementation starts.
  No new material decision is claimed at this head, and nothing is silently loaded. The problem
  is how the obligation is worded.
- Recommended fix: reword the F03 obligation: "Before F03 restore implementation: qualify an
  unloaded and quiet restore order for grouped background tabs on both target OSes. If none
  exists, stop for a material user decision (no silent mass loading, no silent persistent CPU
  load)." Mirror this in `closure2.md` (d).

### WS-E01-TR-PR7-03-F6

- Severity: NIT_OR_SUGGESTION
- Status: OPEN
- Description:
  - `state.json.target_environments` is stale: "Ubuntu Desktop": `QUALIFIED_FOR_F01_SCOPE`,
    although the Ubuntu calibration gate is open, and "Windows Desktop":
    `QUALIFIED_EXCEPT_ADDON_HARD_PEAK_INSTRUMENT`, although the Windows calibration/interval/PID
    gate is also open.
  - The smoke run has no raw-artifact hash entry in `closure2-artifacts.json` (per-run `run.json`,
    logs, `calibration.json`). `evidence_class: UBUNTU_RUNTIME_VERIFIED` is self-stamped by the
    script.
  - Carried from TR-PR7-02-F5: M9 and M11 (closure_probe reuse arm) still survive; the new
    structural tests are source-text matches (brittle to formatting). `ancestor()` still
    surfaces merge-ancestry rejection as `CalledProcessError`.
  - Commit message says "~110-134 %", `closure2.md` says "113-134 %", recorded values are
    110.1-114.5 % (cgroup).
- Recommended fix: update `target_environments`, add the smoke artifacts to the hash manifest,
  add an M9-killing fixture row and a closure-probe reuse-arm order test, and optionally map
  `CalledProcessError` from `ancestor` to `Invalid`.

## Other observations (no finding)

- The cross-check rule (max(2 MiB, 25 %)) and the A/B-only F05 obligation are consistent with
  r6 §9.1.
- Test-only chrome/Marionette automation is confined to `qualification/`. The calibration
  add-on is a temporary synthetic driver ("F01 calibration ONLY"). Disposable profiles are
  created under `build/f01/runs` and removed. No product capability is introduced.
- `contextualIdentities.create` in the calibration driver is test-fixture setup only; the TF §7
  "no container creation" rule applies to the product, not to this qualification driver.

TECHNICAL_REVIEW_OUTCOME: CHANGES_REQUIRED
