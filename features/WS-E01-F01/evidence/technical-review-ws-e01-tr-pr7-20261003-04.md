# WS-E01-TR-PR7-20261003-04: Independent Technical Rereview of PR #7

- Reviewer identity: CLAUDE_SUBAGENT_INDEPENDENT_TECHNICAL_REVIEWER_WS_E01_TR_PR7_20261003_04
- Review type: technical review (Foundation 2 §30, ELEVATED risk increment). This is not a Feature
  Acceptance and not an epic verdict.
- Repository: felixvonvollmer-png/Firefox---WindowSafe, PR #7, branch `feature/ws-e01-f01-closure`
- Reviewed head SHA: `09a484f08765a8a707adb5b5964b8ba0eda5efec`
- Base (main): `f83845a1dd4b78bd010e6477612d95a99b1a8152`
- Reviewed diff: `git diff f83845a1dd4b78bd010e6477612d95a99b1a8152 09a484f08765a8a707adb5b5964b8ba0eda5efec`
  (136 files; commits `8ae803d`, `d2fd8c9`, `9b017dd`, `9bbbb1b`, `09a484f`, single-parent chain on `f83845a`)
- Date: 2026-10-03

## Independence statement

I am a freshly started subagent with no prior context on this change. I did not author,
materialize or contribute to PR #7, PR #3, PR #6, the earlier technical reviews
(WS-E01-TR-PR6-20261001-01/-02, WS-E01-TR-PR7-20261002-01/-02/-03) or any WS-E01 preparation,
correction, rebinding or authorization artifact. I read the earlier reviews only as committed
subject files. There was no expected outcome.

Worktree hygiene: `/home/felix/projekte/windowsafe-review-pr7d` was used read-only.
`git rev-parse HEAD` was `09a484f08765a8a707adb5b5964b8ba0eda5efec` and
`git status --porcelain --ignored` was empty before and after the review. CLI gates ran with
`PYTHONDONTWRITEBYTECODE=1`. The full test suite ran in a disposable clone and all mutants ran in
a second disposable clone, both under `/home/felix/projekte/windowsafe-review-out/scratch-tr04/`
(each mutant reverted with `git checkout`; mutation clone clean afterwards).
`/home/felix/projekte/firefox WindowsSaver addon` was not touched. No pushes, no gh mutations,
no browser launched.

## 1. Commands run (python3 3.14.4)

In the worktree at the reviewed head:

| Command | Exit |
| --- | --- |
| `python3 tools/foundation.py check` | 0 (CHECK OK) |
| `python3 tools/foundation.py history --base f83845a1dd4b78bd010e6477612d95a99b1a8152` | 0 (HISTORY OK) |
| `python3 tools/foundation.py history --base 1cb82c926903b2fd6b497d008db61c71c5d92aca` | 0 (HISTORY OK) |
| `python3 tools/foundation.py request --sha HEAD --subject epics/WS-E01/deltas/WS-E01-EP-DELTA-20260929-04/subject.json` | 0 |
| `python3 tools/foundation.py request --sha HEAD --subject epics/WS-E01/deltas/WS-E01-EP-DELTA-20260929-03/subject.json` | 0 |
| `python3 tools/foundation.py request --sha HEAD --subject epics/WS-E01/deltas/WS-E01-EP-DELTA-20260929-02/subject.json` | 0 |
| `python3 tools/foundation.py request --sha HEAD --subject epics/WS-E01/subject.json` | 0 |
| `python3 tools/foundation.py request --sha HEAD --subject foundation/deltas/WS-PFDELTA-MAT-20260928-01/subject.json` | 0 |
| `git diff --quiet f83845a HEAD -- <each of the five subject.json>` | 0 for all five (byte-identical to base) |
| `python3 tools/foundation.py schema-preflight --sha HEAD --schema reviews/review-contract.json` | 0 (SCHEMA-PREFLIGHT OK) |
| `git diff --check f83845a HEAD` | 0 |

In scratch clones at the reviewed head:

| Command | Exit |
| --- | --- |
| `python3 -m unittest discover -s tests` (full suite) | 0 (Ran 219 tests in 816 s, OK skipped=6; clone `git status --porcelain --ignored` empty afterwards) |
| `python3 -m unittest tests.test_closure_probe` (unmutated) | 0 (10 tests OK) |
| 16 mutants against `tests.test_closure_probe` (table §5) | see table |
| Deterministic rebuild of the calibration XPI from the HEAD `DRIVER`/manifest | SHA-256 `dbc6fd21...e06ad`, equal to `probe_sha256` of all four smoke3 runs |

## 2. Exact-head CI

`gh run list --commit 09a484f08765a8a707adb5b5964b8ba0eda5efec`, waited with `gh run watch`
until completed, then read-only `gh run view <id> --json ...` and `gh run view <id> --log`:

| Run ID | Event | Workflow | headSha | Conclusion | Notes |
| --- | --- | --- | --- | --- | --- |
| 37110183343 | pull_request | Foundation | `09a484f...` | success | checkout `HEAD is now at 09a484f`; CHECK OK; Ran 219 tests OK (skipped=6, 1213 s); SCHEMA-PREFLIGHT OK; 8x VALIDATE-RESULT OK; five exact request steps success; BUILD OK; HISTORY OK; whitespace/clean-tree step success; all 17 steps success |
| 37110180804 | push | Foundation | `09a484f...` | success | same 17 steps all success; Ran 219 tests OK (skipped=6, 1224 s) |

## 3. Transfer, bookkeeping and evidence binding

- Byte-identical transfer: for every path in the cumulative diff the blob at `09a484f` was
  compared with `7d66ca5`. All transferred F01/qualification paths are blob-identical. Paths that
  differ from or are absent in `7d66ca5` are exactly the expected continuation files
  (`state.json`, `closure2*`, the three smoke JSONs, the three TR-PR7 review copies,
  `closure_probe.py`, `calibration_probe.py`, `tests/test_closure_probe.py`) and the non-feature
  harness paths (`tools/foundation.py`, `tests/test_epic_execution.py`, `foundation/engineering.md`,
  `epics/WS-E01/evidence/technical-review-ws-e01-tr-pr6-20261001-02.md`).
- `technical-review-ws-e01-tr-pr7-20261002-03.md` is byte-identical to
  `/home/felix/projekte/windowsafe-review-out/WS-E01-TR-PR7-20261002-03.md` (`cmp` equal).
- `state.json.evidence_paths`: 134 entries, all exist; the only tracked F01/qualification file not
  listed is `state.json` itself.
- `closure2-artifacts.json` now lists `calibration.json`, per-run `run.json` and `calibration.xpi`
  for the three smoke directories. The three `calibration.json` hashes equal the SHA-256 of the
  committed `closure2-calibration-smoke{,2,3}.json`; the per-run XPI hashes equal the runs'
  `probe_sha256`.
- Instrument provenance: smoke `calibration_probe_sha256` `a6d98706...` = blob at `9bbbb1b`;
  smoke3 `a90b632a...` = blob at HEAD (and the XPI rebuild above matches); smoke2 `01e654d5...`
  matches no committed revision (intermediate, uncommitted instrument version; see F4).
  `driver_sources` hashes in all three equal the committed `run_probe.py`, `target_probe.py`,
  `measure.py`, `windows_job.py`.
- F01 status: `WS-E01-F01_OPEN__CALIBRATION_AND_WINDOWS_RUNS_REQUIRED`,
  `product_implementation_started: false`, `merge_authorized: false`, three open measurement
  gates (Ubuntu calibration; Windows add-on hard peak; Windows calibration/intervals/PID coverage).
  F01 is correctly NOT complete; no F02 product code exists; no gate is closed beyond evidence.
- TF r6 ordering (§§7.1, 9.1, 9.3, 10.2; preparation `WS-E01-EP-DELTA-20260929-02` §4): measurement
  tool, warm-up, interval and known uncertainty remain pre-implementation items in F01
  `open_gates`; only real-add-on A/B runs are bound to F05. Consistent.

## 4. Claims versus committed JSON

| Claim (`closure2.md`) | Status |
| --- | --- |
| (d) API-realized R500: about 110-115 % of one core after 60 s rest in all 12 smoke runs | Supported (109.9-115.3 %) |
| (d) smoke2/3: parent process carries essentially all of it (e.g. 114.1 of 114.5 %) | Supported; smoke3 (HEAD instrument) alone shows parent 111.6-113.6 % of 111.9-113.9 % |
| (d) native restore near idle in 11 of 12 runs (0.05-1.2 %) | Supported (0.053-1.166 %) |
| (d) smoke2 `p1-second`: 124 % after native restore, parent 124 %, persisted; rejected as not quiescent | Supported by smoke2 (123.99/123.95 %; later intervals 119-123.5 %; `not_quiescent`); smoke2 instrument source not committed (F4) |
| (d) isolation runs only LOCAL_AGENT_REPORTED, not evidence | Correctly framed |
| (e) smoke2 L10 about 2 % or about 24 % depending on run | Supported (2.18 / 24.05 / 2.30 / 121.2 [loaded]) |
| (e) cause "consistent with whether the windows ... were visible"; `front` verified in every smoke3 run | Hypothesis only; no visibility/stacking datum is recorded. `front.ok` is true in all smoke3 runs, yet `p0-first` is again in the low mode (F1) |
| (e) valid smoke3 pairs differ by 0.01 % (L10), 0.3 % (B300), 0.08/0.03 % (idle) | Supported (0.0064 / -0.297 / -0.077, 0.033) |
| (e) remaining low-cost run "coincided with foreign host load ... and was rejected" | Factually true (`maxwin` 6.32 > 5), but foreign load cannot make the workload 12x cheaper; the low mode is unexplained (F1) |
| (c)3 "with-minimize was 1.1-1.2 MB below the fresh-state control and about 11 MB above without-minimize" in the calibration smoke runs | NOT supported across the committed smoke runs (F3) |
| Constants: 0.1 % late tolerance, 5 s interference windows, 3 % / 10 s quiescence, 6 attempts, minimize before CPU intervals | Match `calibration_probe.py` |
| "driver errors, lost events, tab/window/group/container mismatches and failed runs make the pair invalid" | Partly: container and window checks are non-discriminating or absent (F2) |

Observation (no separate finding): the absolute A/A idle level differs between runs, 0.26-0.34 %
(smoke3 p0) versus 2.67-3.54 % (smoke2, smoke3 p1), while within-pair differences are small. This
is calibration data, not an instrument defect, but the between-run spread is about 25x the r6
§9.1 idle target and should be reported with the calibration, not only within-pair diffs.

## 5. Mutation probes (scratch clone, `python3 -m unittest tests.test_closure_probe`)

| Mutant | Result |
| --- | --- |
| M9 `origin_explicit` without the `explicit/` prefix filter | survived |
| M11 `closure_probe.py` reuse trial never minimizes | survived |
| M14 `run_invalid_reasons` without the late-event rule | killed |
| M15 without the foreign-host-load rule | killed |
| M16 fresh-control also does hold/drop | survived |
| M17 pair difference forced to 0 | killed |
| M18 adopt container check removed | survived |
| M19 `not_quiescent` never set | survived |
| M20 interference uses the whole-interval average instead of the max 5 s window | survived |
| M21 `LATE_TOLERANCE` 0.001 -> 0.01 | killed |
| M22 `front` failure ignored | survived |
| M23 missing synthetic IDs ignored | survived |
| M24 FAILED status not invalid | killed |
| M25 lost events ignored | killed |
| M26 `QUIESCENT_PCT` 3 -> 200 | survived |
| M27 `INTERFERENCE_WINDOW_S` 5 -> 60 | survived |

The `summarize()`/`run_invalid_reasons()` consumption of each invalidity reason is tested
(TR-PR7-03 M14/M15/M17 now killed). The producers of those reasons (5 s windowing, quiescence
flag, front check, adopt/realize mismatch flags, constants other than the late tolerance) are not
tested.

## 6. Status of earlier findings

TR-PR7-01 and TR-PR7-02 findings: resolved as recorded in TR-PR7-03; nothing at this head
reopens them except the carried NIT items below.

| TR-PR7-03 finding | Status | Evidence |
| --- | --- | --- |
| F1 MAJOR: instrument does not conform to METHOD-01 though "ready" | PARTIALLY RESOLVED | Fail-closed `run_invalid_reasons` (driver error, missing interval, FAILED runs listed, mismatch flags, lost/late events) with tests; declared late tolerance; 1 s sampling with the workload in a thread and max-of-5 s-window interference; compositor separation declared; quiescence acknowledgement replaces bare timer, not-quiescent invalid; minimize before CPU intervals declared; sampler self-CPU recorded and Marionette argument recorded; R2000 idle default 600 s. Remaining: the new declared exclusive-desktop/stacking condition is not enforced and the evidence shows the fail-open case (F1); container/window verification non-discriminating (F2); handoff idle wording and L10 601 s (F4). |
| F2 MINOR: (d) overstated | RESOLVED | (d) restated to recorded smoke values; isolation runs marked LOCAL_AGENT_REPORTED; Windows check now repeats the recorded R500 configuration. |
| F3 MINOR: reuse "equals within 1 MB" | NOT RESOLVED | New wording is again not supported by the committed data (F3). The Ubuntu reuse pass rule is now bound (resolved part). |
| F4 MINOR: Windows handoff not executable | RESOLVED | Handoff states the instrument is Linux-only and specifies the port (Job accounting, GetProcessTimes, dwm.exe separation, GetSystemTimes 5 s windows, unchanged constants and invalidity rules). |
| F5 MINOR: F03 obligation wording | RESOLVED | `state.json` F03 obligation and `closure2.md` (d) now require qualification before F03 implementation and a STOP for a user decision; consistent with Product WS-RESTORE, TF §6.3 and §7.1. |
| F6 NIT | PARTIALLY RESOLVED | `target_environments` updated; smoke artifacts hashed; commit-message range no longer repeated. M9/M11 still survive; `ancestor()` unchanged. Carried in F4. |

## Findings

### WS-E01-TR-PR7-04-F1

- Severity: MAJOR
- Status: OPEN
- Description: Finding (e) declares "an exclusive desktop with no other application window above
  the browser" as a calibration and A/B condition, and `state.json` calls the instrument
  "candidate ready" for the multi-hour calibration. The instrument does not enforce that condition,
  and the committed smoke evidence shows the resulting fail-open case:
  - smoke2 pair `p0`: L10 2.18 % vs 24.05 % of one core, B300 3.58 % vs 15.85 %; both runs pass
    every invalidity rule, and the pair is VALID with an L10 difference of 21.87 pp (more than
    the R500 single-run limit of 15 % and twice the 10 % median limit of r6 §9.3).
  - smoke3 `p0-first`: `front.ok == true`, yet L10 1.95 % vs 24.67-24.77 % in the other three
    runs and B300 5.84 % vs 16.3-19.9 %. It was rejected only because `maxwin` was 6.32 % (> 5 %).
    Foreign host load cannot make the measured workload twelve times cheaper, so "coincided with
    foreign host load" does not explain it. Had the foreign load stayed below 5 %, the pair would
    have been valid with an L10 difference of about 22.8 pp.
  - The `front` operation verifies `windows.getLastFocused()`, which is Firefox's focus state, not
    compositor stacking or occlusion. The one smoke3 run with a verified front window still ran in
    the low mode, so `front` is not shown to make the workload deterministic.
  The cause of the bimodal workload cost is therefore not determined at this head. No invalidity
  rule detects it. The only guard that can catch it is the foreign-host-load rule, and only by
  chance. In the calibration, an undetected mode split would distort the bound "known uncertainty".
  Rejecting low-mode runs under another reason, as in smoke3, would hide it. In F05 A/B, a split of
  about 22 pp could mask or invent add-on CPU of the size of the r6 §9.3 limits. The (e) text
  ("valid smoke3 pairs differ by 0.01 %") presents the effect as controlled.
- Recommended fix: record a per-interval observable for the mode and make a change an invalidity
  rule. Examples: anchor-window visibility/occlusion (`document.visibilityState` of a tab in the
  anchor window, `windows.get(...).focused` and state) before and after each interval; the
  per-interval compositor CPU; or an explicit mode classifier on L10/B300 cost with a declared
  threshold. Re-run the smoke with the operator away from the desktop to show that the low mode
  disappears or is detected. Reword (e): the cause is a hypothesis, the low mode recurred with
  `front.ok`, and the smoke2 `p0` pair was a valid mode split. Until then, do not call the
  instrument ready for the calibration.

### WS-E01-TR-PR7-04-F2

- Severity: MINOR
- Status: OPEN
- Description: `closure2.md` says "tab/window/group/container mismatches ... make the pair
  invalid", and METHOD-01 requires that "browser realization must verify actual
  window/tab/group/container counts". The adopt check is partly non-discriminating:
  - `record['adopted'].get('containers', 0) < 3` can never trip in a Firefox profile with the four
    default contextual identities. smoke2/3 record `containers: 7` (4 default + 3 synthetic).
    Losing all synthetic containers would still pass. Per-tab container assignment is not read.
  - The window count after restore (11 recorded) is not compared. Pinned, muted and discarded
    counts are recorded or available but not compared. Only missing synthetic IDs are checked;
    extra or duplicated synthetic tabs are not.
  - `observedEvents` (218 for 200 scheduled L10 events, 306 for 300 B300) is recorded but not
    checked, although METHOD-01 L10 says to count delivered **and observed** changes.
  - The commit message says "unit tests cover each invalidity rule". That holds for the
    consumption in `run_invalid_reasons()`. The producers are untested: mutants M18, M19, M20,
    M22, M23, M26 and M27 survive.
- Recommended fix: compare the restored state with the fixture: windows; per-tab synthetic-ID
  multiset; per-tab cookieStoreId, mapped to the three synthetic identities by name; pinned,
  muted and discarded counts; groups per window. Require `observedEvents >= delivered`. Factor the
  adopt comparison and the 5 s window computation into pure functions with unit tests, so that
  M18-M20, M23 and M27 are killed.

### WS-E01-TR-PR7-04-F3

- Severity: MINOR
- Status: OPEN
- Description: TR-PR7-03-F3 is not resolved. `closure2.md` (c)3 now says "In the calibration
  smoke runs with-minimize was 1.1-1.2 MB below the fresh-state control and about 11 MB above
  without-minimize". The 12 committed smoke runs show:
  - with-minimize minus fresh-control: -0.05, -1.23, -1.21, -1.12 MB (smoke);
    -0.95, -0.50, +1.21, -0.06 MB (smoke2); +2.97, +0.51, +0.38, -0.16 MB (smoke3).
    The range is -1.23 to +2.97 MB, with no consistent sign.
  - with-minimize minus without-minimize: 9.6 to 16.7 MB.
  The next sentence, "There is no fresh-state control, the trial order was fixed and n is small",
  refers to runs 3/4 but now reads as contradicting the smoke sentence before it. The declared
  reuse pass rule (with-minimize >= fresh-control - 2 MiB and >= without-minimize) is not evaluated
  by `summarize()`; the report has no reuse verdict. Computed by hand, all 12 smoke runs pass it.
- Recommended fix: report "with-minimize -1.23 to +2.97 MB relative to the fresh-state control,
  9.6-16.7 MB above without-minimize (12 smoke runs)". Scope the "no fresh-state control" sentence
  explicitly to runs 3/4. Add the pass-rule evaluation per run to the calibration summary.

### WS-E01-TR-PR7-04-F4

- Severity: NIT_OR_SUGGESTION
- Status: OPEN
- Description:
  - `closure2-windows-handoff.md` line 59 still says "(R500) idle 600 s". The instrument and
    `closure2.md` use idle for R500 and R2000 (TR-PR7-03-F1.6 alignment incomplete).
  - The L10 interval is `l10_seconds + 1` (601 s), and the B300 window ends at the first 1 s
    sample after 10 s (10.1 s in smoke). Neither is declared next to the constants.
  - smoke2 was produced by an uncommitted instrument version (`01e654d5...`). The only recorded
    native-restore occurrence in (d) rests on it. smoke3 independently supports the
    parent-process attribution.
  - The restored realize-session driver tab (two `moz-extension://.../driver.` entries) is still
    not declared as part of the measured state.
  - METHOD-01 asks for power governor, AC/battery and thermal state at every final measurement,
    and for timer resolution in the uncertainty report. The calibration instrument records
    neither.
  - Carried from TR-PR7-03-F6: M9 and M11 survive; `ancestor()` still surfaces merge-ancestry
    rejection as `CalledProcessError`.
- Recommended fix: align the handoff idle wording; declare the 601 s and sampled-window
  boundaries; note the smoke2 provenance in (d); declare or close the restored driver tab; record
  governor, power and thermal state and timer resolution; address M9/M11 and `ancestor()`.

## Other observations (no finding)

- Test-only chrome/Marionette automation and the calibration add-on ("F01 calibration ONLY") stay
  in `qualification/`; disposable synthetic profiles under `build/f01/runs` are removed after each
  run. No product capability is introduced.
- The declared deviations (0.1 % late tolerance; foreign load net of compositor; CPU-threshold
  quiescence acknowledgement; minimize before CPU intervals) are operationalizations stated next to
  METHOD-01, not threshold changes.
- The (d) and (e) consequences are framed within existing Product Truth/TF; no new material
  decision is claimed. The F03 STOP-for-user-decision wording matches TF §7.1.

TECHNICAL_REVIEW_OUTCOME: CHANGES_REQUIRED
