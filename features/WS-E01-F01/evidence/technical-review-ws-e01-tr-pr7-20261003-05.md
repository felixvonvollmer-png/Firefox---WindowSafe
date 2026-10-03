# WS-E01-TR-PR7-20261003-05: Independent Technical Rereview of PR #7

- Reviewer identity: CLAUDE_SUBAGENT_INDEPENDENT_TECHNICAL_REVIEWER_WS_E01_TR_PR7_20261003_05
- Review type: technical review (Foundation 2 §30, ELEVATED risk increment). This is not a Feature
  Acceptance and not an epic verdict.
- Repository: felixvonvollmer-png/Firefox---WindowSafe, PR #7, branch `feature/ws-e01-f01-closure`
- Reviewed head SHA: `87d83c3650a09b66bf2d8311a236ad26ce7750ad`
- Base (main): `f83845a1dd4b78bd010e6477612d95a99b1a8152`
- Reviewed diff: `git diff f83845a1dd4b78bd010e6477612d95a99b1a8152 87d83c3650a09b66bf2d8311a236ad26ce7750ad`
  (137 files; commits `8ae803d`, `d2fd8c9`, `9b017dd`, `9bbbb1b`, `09a484f`, `87d83c3`,
  single-parent chain on `f83845a`). Focus of this round: `87d83c3` (response to TR-PR7-04),
  plus the cumulative claims.
- Date: 2026-10-03

## Independence statement

I am a freshly started subagent with no prior context on this change. I did not author,
materialize or contribute to PR #7, PR #3, PR #6, the earlier technical reviews
(WS-E01-TR-PR6-20261001-01/-02, WS-E01-TR-PR7-20261002-01/-02/-03, WS-E01-TR-PR7-20261003-04) or
any WS-E01 preparation, correction, rebinding or authorization artifact. I read the earlier
reviews only as committed subject files. There was no expected outcome.

Worktree hygiene: `/home/felix/projekte/windowsafe-review-pr7e` was used read-only.
`git rev-parse HEAD` was `87d83c3650a09b66bf2d8311a236ad26ce7750ad` and
`git status --porcelain --ignored` was empty before the review. Disclosure: I additionally ran
`python3 tools/foundation.py build --verify-repeat` (a CI step, not in the requested gate list) in
the worktree; it wrote the ignored file `build/foundation-inventory.json`, which I removed.
`git status --porcelain --ignored` was empty again afterwards and at the end of the review. The
full test suite ran in a disposable clone under
`/home/felix/projekte/windowsafe-review-out/scratch-tr05/repo` (status empty afterwards).
`/home/felix/projekte/firefox WindowsSaver addon` was not touched. No pushes, no gh mutations,
no browser launched, no probes run.

## 1. Commands run (python3 3.14.4, `PYTHONDONTWRITEBYTECODE=1`)

In the worktree at the reviewed head:

| Command | Exit |
| --- | --- |
| `python3 tools/foundation.py check` | 0 |
| `python3 tools/foundation.py history --base f83845a1dd4b78bd010e6477612d95a99b1a8152` | 0 |
| `python3 tools/foundation.py history --base 1cb82c926903b2fd6b497d008db61c71c5d92aca` | 0 (HISTORY OK) |
| `python3 tools/foundation.py request --sha HEAD --subject epics/WS-E01/deltas/WS-E01-EP-DELTA-20260929-04/subject.json` | 0 |
| `python3 tools/foundation.py request --sha HEAD --subject epics/WS-E01/deltas/WS-E01-EP-DELTA-20260929-03/subject.json` | 0 |
| `python3 tools/foundation.py request --sha HEAD --subject epics/WS-E01/deltas/WS-E01-EP-DELTA-20260929-02/subject.json` | 0 |
| `python3 tools/foundation.py request --sha HEAD --subject epics/WS-E01/subject.json` | 0 |
| `python3 tools/foundation.py request --sha HEAD --subject foundation/deltas/WS-PFDELTA-MAT-20260928-01/subject.json` | 0 |
| `git diff --quiet f83845a HEAD -- <each of the five subject.json>` | 0 for all five (byte-identical to base) |
| `python3 tools/foundation.py schema-preflight --sha HEAD --schema reviews/review-contract.json` | 0 (SCHEMA-PREFLIGHT OK) |
| `python3 tools/foundation.py build --verify-repeat` | 0 (output removed, see above) |
| `git diff --check f83845a HEAD` | 0 |

In the scratch clone at the reviewed head:

| Command | Exit |
| --- | --- |
| `python3 -m unittest discover -s tests -v` (full suite) | 0 (Ran 219 tests in 839 s, OK skipped=6; clone `git status --porcelain --ignored` empty afterwards) |

Mutation probes were not repeated: `87d83c3` changes no code or test (only `closure2.md`,
`closure2-windows-handoff.md`, `state.json` and the added review copy). The TR-PR7-04 §5 mutant
results therefore still describe the code at this head.

## 2. Exact-head CI

`gh run list --commit 87d83c3650a09b66bf2d8311a236ad26ce7750ad`; waited until both runs
completed, then read-only `gh run view <id> --json headSha,event,status,conclusion,jobs` and
`gh run view <id> --log`:

| Run ID | Event | Workflow | headSha | Conclusion | Notes |
| --- | --- | --- | --- | --- | --- |
| 37111575392 | pull_request | Foundation | `87d83c3...` | success | checkout `HEAD is now at 87d83c3`; CHECK OK; Ran 219 tests OK (skipped=6, 797 s); SCHEMA-PREFLIGHT OK; 8x VALIDATE-RESULT OK; five exact request steps success; BUILD OK; HISTORY OK; whitespace/clean-tree step success; all 17 steps success |
| 37111572060 | push | Foundation | `87d83c3...` | success | same 17 steps all success; Ran 219 tests OK (skipped=6, 1322 s) |

## 3. Scope, transfer and bookkeeping

- `git diff --name-only 09a484f HEAD` lists exactly `closure2-windows-handoff.md`, `closure2.md`,
  `technical-review-ws-e01-tr-pr7-20261003-04.md` and `state.json` under
  `features/WS-E01-F01/`. None of these is a transferred PR #3 path. The byte-identical PR #3
  transfer was verified per blob by TR-PR7-04 §3 at `09a484f` and is unaffected by this commit; I
  did not repeat the per-blob comparison.
- The committed `technical-review-ws-e01-tr-pr7-20261003-04.md` is byte-identical to
  `/home/felix/projekte/windowsafe-review-out/WS-E01-TR-PR7-20261003-04.md` (`cmp` exit 0), so the
  commit-message claim "Preserves WS-E01-TR-PR7-20261003-04 byte-identically" holds.
- `state.json.evidence_paths`: 135 unique entries, all exist; the only tracked
  `features/WS-E01-F01/**` or `qualification/ws-e01-f01/**` file not listed is `state.json` itself.
- F01 status unchanged: three `open_gates` (Ubuntu calibration; Windows add-on hard peak; Windows
  calibration/intervals/PID coverage), `merge_authorized: false`, no product code in the diff.
  `target_environments.Ubuntu Desktop` now reads "instrument candidate NOT qualified (unexplained
  two-mode workload cost, gaps per TR-PR7-04)". No gate was closed or added by `87d83c3`.
- Harness changes (`tools/foundation.py`, `tests/test_epic_execution.py`,
  `foundation/engineering.md`) are unchanged since TR-PR7-04. I re-read them: the
  case-/whitespace-insensitive exclusion-set check, `start.json` in `feature_path`, the added
  `ancestor(parents[0], parents[1])` for execution merges, `diff-tree -z --no-renames` path
  enumeration (NUL-split status/path pairs, no rename triples) and the tracked-file-mode check
  only tighten gates. No weakening found.

## 4. TF r6 ordering

- TF r6 §9.3: measurement tool, warm-up, interval and known measurement uncertainty are bound
  "vor Beginn der betroffenen Produktimplementierung"; results are due before Feature Acceptance.
  §7.1: hard stop before the affected product implementation. Preparation
  `WS-E01-EP-DELTA-20260929-02` §4 keeps F01 a non-productive enabler that must finish the
  cross-OS measurement methodology, with order `F01 -> F02 -> {F03, F04} -> F05`.
- The PR keeps the Ubuntu calibration as **F01 OPEN** ("TF §9.3: bound before F02"), keeps both
  Windows measurement gates open, binds only real-add-on A/B runs to F05, and states that no
  calibration result from the current instrument can bind the known uncertainty until (e) is
  resolved. Nothing in the diff allows F02 to start. Consistent.
- F03 obligation (`state.json`): qualify an unloaded and quiet restore order for grouped
  background tabs before F03 restore implementation, otherwise STOP for a user decision.
  Consistent with Product WS-RESTORE, TF §6.3 and §7.1 (as in TR-PR7-04).

## 5. Claims versus committed JSON (changed text in `87d83c3`)

| Claim | Status |
| --- | --- |
| (c)3: with-minimize between 1.23 MB below and 2.97 MB above fresh-state control, 9.6-16.7 MB above without-minimize; all 12 meet the declared reuse pass rule by manual evaluation | Supported. Recomputed from `reuse_trials` of the 12 runs in `closure2-calibration-smoke{,2,3}.json`: with-minus-fresh -1.23 to +2.97 MB, with-minus-without 9.64 to 16.69 MB, pass rule (with >= fresh - 2 MiB and >= without) met 12/12 |
| (c)3: runs 3/4 had no fresh-state control and fixed order | Correctly scoped now |
| (e): smoke2 p0 L10 2.18 % vs 24.05 % of one core; the mixed pair was accepted as valid (21.9 pp) | Supported: smoke2 `summary.L10.valid_pair_diffs_pct_one_core = [21.874]`; run values 2.18 / 24.05 |
| (e): smoke3 `p0-first` 1.95 % despite `front.ok` | Supported: L10 1.95 %, `front = {frontWindow: 1, focusedWindow: 1, ok: true}`; listed invalid only for "foreign host load" |
| (e): cause undetermined, not controlled, not detected; `front` reads only Firefox focus | Correctly framed; matches TR-PR7-04-F1 |
| (e): no calibration result from this instrument can bind the known uncertainty until resolved | Correct and consistent with the open gate |
| Handoff: idle 600 s for both profiles | Aligned with `closure2.md` and the instrument |

Observation (no separate finding): smoke2 also accepted a B300 pair with a 12.27 pp difference
(p0: 3.58 % vs 15.85 %). It belongs to the same two-mode effect that (e) now discloses for L10.
Across smoke2 and smoke3 the low mode appeared in 3 of 8 L10 runs (smoke2 `p0-first` 2.18 %,
`p1-first` 2.30 %; smoke3 `p0-first` 1.95 %). Two of the three were excluded only under the
foreign-host-load rule, not detected as a mode. This supports the (e) statement that the mode is
not detected.

## 6. Status of earlier findings

TR-PR7-01, TR-PR7-02 and TR-PR7-03 findings: as dispositioned in TR-PR7-04 §6; nothing at this
head reopens them.

| TR-PR7-04 finding | Status | Evidence |
| --- | --- | --- |
| F1 MAJOR: two-mode workload cost presented as controlled | RESOLVED as a claim | (e) now states the cause is undetermined, not controlled and not detected, names the accepted mixed smoke2 pair and the `front.ok` low-mode run, and bars binding the known uncertainty until resolved. `state.json` marks the instrument NOT qualified. The technical defect itself (no mode detection) remains honest open work inside the open Ubuntu calibration gate. Residual wording issues: F1 and F2 below. |
| F2 MINOR: adopt/restore checks non-discriminating, producers untested | PARTIALLY RESOLVED | Container baseline, window count, per-tab state, extra tabs and `observedEvents` are now listed as known gaps. The untested producers (surviving mutants M18-M20, M22, M23, M26, M27) are not listed, and the same table cell still claims "unit-tested per rule" and that container/window mismatches invalidate the pair (F1 below). |
| F3 MINOR: reuse wording not supported | RESOLVED | Numbers recomputed (§5); runs 3/4 sentence scoped; pass rule evaluated manually and the missing automatic evaluation disclosed. |
| F4 NIT | PARTIALLY RESOLVED | Handoff idle wording aligned; 601 s / 10.1 s, smoke2 provenance, power/thermal state and timer resolution listed as known gaps. Not listed: the restored driver tab in the measured state, surviving M9/M11, `ancestor()` surfacing merge-ancestry rejection as `CalledProcessError` (only referenced through "gaps per TR-PR7-04" in `state.json`). |

## Findings

### WS-E01-TR-PR7-05-F1

- Severity: MINOR
- Status: OPEN
- Description: The Ubuntu-calibration row of the `closure2.md` dispositions table lists "further
  known gaps from TR-PR7-04" and then, in the same cell, says "Already implemented and unit-tested
  per rule" and "driver errors, lost events, tab/window/group/container mismatches and failed runs
  make the pair invalid". These two sentences contradict the listed gaps. The container check
  cannot trip with the default identities and the window count is not compared. TR-PR7-04 §5
  shows that the producers of the invalidity reasons are untested (M18-M20, M22, M23, M26, M27
  survive; this commit changes no code). The explicit gap list also reads as complete but omits
  the untested producers, the restored driver tab, M9/M11 and `ancestor()`. `state.json`
  (`gaps per TR-PR7-04`) is honest by reference, and the instrument is clearly marked NOT
  qualified, so no gate is affected. The cell still overstates what is implemented and tested.
- Recommended fix: Replace "Already implemented and unit-tested per rule" with "implemented; the
  consumption of each invalidity reason is unit-tested, its producers are not". Mark the
  container/window part of the mismatch sentence as declared but not yet enforced. Either complete
  the gap list (untested producers, restored driver tab, M9/M11, `ancestor()`) or say explicitly
  that the full list is TR-PR7-04 F2/F4.

### WS-E01-TR-PR7-05-F2

- Severity: MINOR
- Status: OPEN
- Description: The Windows prerequisite and the next-gate text are weaker than (e). (e) says no
  calibration result from this instrument can bind the known uncertainty until the two-mode cause
  is identified and controlled, or detected as an invalidity. `closure2-windows-handoff.md`
  "Windows calibration and intervals" says to port the instrument "keeping the protocol constants
  and invalidity rules unchanged" and "Then run it". It refers to closure2 only through "see
  closure2 dispositions". It does not require that the mode issue be resolved first, or that a
  mode observable and invalidity rule be ported, before the Windows A/A runs are taken as
  calibration. A Windows session run from this handoff would inherit the undetected mode split.
  Its A/A results could then be presented as the bound Windows uncertainty. Likewise,
  `state.json.required_next_gate` says "Ubuntu calibration runs (multi-hour quiet visible
  desktop) and the Windows session ...". It omits the prerequisite that (e) and the instrument
  gaps must be resolved before those runs can count. No gate is closed by this, and the later
  independent F01 review remains a backstop. The handoff is still the executable instruction.
- Recommended fix: In the handoff, state that Windows calibration results count only after the
  (e) mode issue is resolved: identified and controlled, or detected per interval as an
  invalidity, with the observable ported to Windows (for example DWM occlusion/visibility). Until
  then, Windows A/A runs are instrument evidence only. In `state.json.required_next_gate`, prefix
  "resolve closure2 (e) and the TR-PR7-04 instrument gaps, then ...".

### WS-E01-TR-PR7-05-F3

- Severity: NIT_OR_SUGGESTION
- Status: OPEN
- Description: `closure2-windows-handoff.md` line 53 says "Linux-only" twice in one sentence
  ("is a Linux-only, not yet qualified candidate (...); it is Linux-only (cgroup v2, ...)"). The
  line is also far longer than the surrounding wrapped lines.
- Recommended fix: "`calibration_probe.py` is a not yet qualified candidate (see closure2
  dispositions) and Linux-only (cgroup v2, /proc, Wayland compositor)." Rewrap the paragraph.

## Fitness as an intermediate state

The PR does not claim a completed F01 or a qualified calibration. All three measurement gates
stay open, `merge_authorized` is false in the F01 state, and no F02 product code exists. The
restatement in `87d83c3` removes the earlier claim that the two-mode effect was controlled.
Every changed numeric claim I checked matches the committed JSON. The harness changes only tighten
gates. The remaining findings are wording and handoff precision issues, and none of them closes or
weakens a gate. In my view this is an honest intermediate qualification state, suitable for main
as the development line. Merging it does not accept F01.

TECHNICAL_REVIEW_OUTCOME: NO_OPEN_CRITICAL_BLOCKING_MAJOR
