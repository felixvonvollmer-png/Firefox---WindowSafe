# WS-E01-TR-PR8-20261003-01: Independent Technical Review of PR #8

- Reviewer identity: CLAUDE_SUBAGENT_INDEPENDENT_TECHNICAL_REVIEWER_WS_E01_TR_PR8_20261003_01
- Review type: technical review of a narrow documentation/state follow-up to PR #7. This is not a
  Feature Acceptance and not an epic verdict.
- Repository: felixvonvollmer-png/Firefox---WindowSafe, PR #8, branch
  `feature/ws-e01-f01-closure-followup`
- Reviewed head SHA: `a237b73a5266289344fd50e0468838dd2c34c202`
- Base (main): `a15b4f9122cce09789843e490add9c93482ba4dc` (merge of PR #7)
- Reviewed diff: `git diff a15b4f9122cce09789843e490add9c93482ba4dc a237b73a5266289344fd50e0468838dd2c34c202`
  (single commit `a237b73`, parent `a15b4f9`; 4 files: `closure2.md`,
  `closure2-windows-handoff.md`, `state.json`, added
  `technical-review-ws-e01-tr-pr7-20261003-05.md`, all under `features/WS-E01-F01/`)
- Date: 2026-10-03

## Independence statement

I am a freshly started subagent with no prior context on this change. I did not author,
materialize or contribute to PR #8, PR #7, PR #6, PR #3, any earlier technical review
(WS-E01-TR-PR6-20261001-01/-02, WS-E01-TR-PR7-20261002-01/-02/-03, WS-E01-TR-PR7-20261003-04/-05)
or any WS-E01 preparation, correction, rebinding or authorization artifact. I read the earlier
reviews only as files. There was no expected outcome.

Worktree hygiene: `/home/felix/projekte/windowsafe-review-pr8` was used read-only.
`git rev-parse HEAD` was `a237b73a5266289344fd50e0468838dd2c34c202` and
`git status --porcelain --ignored` was empty before the review and again at the end. `build` was
not run. `/home/felix/projekte/firefox WindowsSaver addon` was not touched. No pushes, no gh
mutations, no browser launched, no probes run.

## 1. Commands run (python3 3.14.4, `PYTHONDONTWRITEBYTECODE=1`, in the worktree)

| Command | Exit |
| --- | --- |
| `python3 tools/foundation.py check` | 0 (CHECK OK) |
| `python3 tools/foundation.py history --base a15b4f9122cce09789843e490add9c93482ba4dc` | 0 (HISTORY OK) |
| `python3 tools/foundation.py schema-preflight --sha HEAD --schema reviews/review-contract.json` | 0 (SCHEMA-PREFLIGHT OK) |
| `python3 tools/foundation.py request --sha HEAD --subject epics/WS-E01/deltas/WS-E01-EP-DELTA-20260929-04/subject.json` | 0 |
| `git diff --quiet a15b4f9 HEAD -- epics/WS-E01/deltas/WS-E01-EP-DELTA-20260929-04/subject.json` | 0 (byte-identical to base) |
| `git diff --check a15b4f9 HEAD` | 0 |
| `cmp features/WS-E01-F01/evidence/technical-review-ws-e01-tr-pr7-20261003-05.md /home/felix/projekte/windowsafe-review-out/WS-E01-TR-PR7-20261003-05.md` | 0 (identical) |
| `sha256sum` of both files | both `ed5f28f5076639697cfbd8b0c069bf0c1a66903a01ee9fe4c0f345841fd2694d` |
| `git status --porcelain --ignored` (start and end) | empty |

Not rerun: the full test suite and the mutation probes. `a237b73` changes no code and no test, and
`git diff --stat 09a484f HEAD -- qualification/ws-e01-f01 tests/test_closure_probe.py
tools/foundation.py` is empty (TR-PR7-04 reviewed head `09a484f`; `a15b4f9` merges `87d83c3`
into `f83845a`). The TR-PR7-04 §5 mutant results therefore still describe `calibration_probe.py`,
`closure_probe.py` and `tests/test_closure_probe.py` at this head. The suite ran in exact-head CI (§2).

## 2. Exact-head CI

`gh run list --commit a237b73a5266289344fd50e0468838dd2c34c202`, waited with
`gh run watch <id> --exit-status` (exit 0 for both), then read-only
`gh run view <id> --json headSha,event,status,conclusion,jobs` and `gh run view <id> --log`:

| Run ID | Event | Workflow | headSha | Conclusion | Notes |
| --- | --- | --- | --- | --- | --- |
| 37113080422 | pull_request | Foundation | `a237b73...` | success | checkout `HEAD is now at a237b73`; CHECK OK; Ran 219 tests OK (skipped=6, 1208 s); SCHEMA-PREFLIGHT OK; 8x VALIDATE-RESULT OK; five exact request steps success; BUILD OK; HISTORY OK; whitespace/clean-tree step success; all 17 steps success |
| 37113078127 | push | Foundation | `a237b73...` | success | same 17 steps all success; Ran 219 tests OK (skipped=6, 1217 s) |

## 3. Scope and bookkeeping

- `git diff --name-only a15b4f9 HEAD` lists exactly the four files above. No code, test, harness,
  subject, review result or transferred PR #3 path is changed.
- The added `technical-review-ws-e01-tr-pr7-20261003-05.md` is byte-identical to the original
  review output (§1). The commit-message claim "Preserves WS-E01-TR-PR7-20261003-05 ...
  byte-identically" holds.
- `state.json.evidence_paths`: 136 unique entries, all exist. The new review copy is listed. The
  only tracked `features/WS-E01-F01/**` or `qualification/ws-e01-f01/**` file not listed is
  `state.json` itself.
- F01 status is unchanged: `status` `WS-E01-F01_OPEN__CALIBRATION_AND_WINDOWS_RUNS_REQUIRED`,
  `product_implementation_started: false`, `merge_authorized: false`, the same three
  `open_gates` (Ubuntu calibration; Windows add-on hard peak; Windows calibration, intervals and
  PID coverage). `target_environments` is unchanged and still marks the Ubuntu instrument as NOT
  qualified. No gate is closed or removed.
- F02: the new `required_next_gate` orders 1) Ubuntu (e) resolution, instrument gaps and
  calibration, 2) the Windows session, 3) independent F01 technical review and Feature
  Acceptance, and ends with "No F02 product code before." Nothing in the diff permits F02 to
  start.

## 4. New statements versus code and committed evidence

Checked against `qualification/ws-e01-f01/calibration_probe.py`, `tests/test_closure_probe.py`,
`closure2-calibration-smoke{,2,3}.json` and TR-PR7-04 §5.

| Statement (`closure2.md` Ubuntu-calibration row, `a237b73`) | Status |
| --- | --- |
| "What is implemented: the summary's evaluation of each invalidity reason, unit-tested per rule" | Supported. `CalibrationSummaryTests.test_each_invalidity_rule_rejects_the_pair` covers driver error, lost and late events, foreign host load, `realize_mismatch`, `adopt_mismatch`, `not_quiescent` and FAILED status through `summarize()`/`run_invalid_reasons()`; `test_failed_run_without_intervals_is_listed_not_dropped` exercises the missing-interval path (it asserts the listed pair, not the `interval missing` reason string). |
| "the code that produces the invalidity reasons (post-restart state comparison, foreign-load windows, front step) is untested" | Supported, but incomplete: the quiescence producer is also untested (M19 `not_quiescent` never set and M26 `QUIESCENT_PCT` 3 -> 200 survive per TR-PR7-04 §5). See F2. |
| "(surviving mutants per TR-PR7-05)" | The mutants were run in TR-PR7-04 §5; TR-PR7-05 only cites them. See F2. |
| "the previous session's restored driver tab is not declared" | Matches TR-PR7-04-F4. |
| "two closure-probe order mutants (M9/M11) survive" | M9 and M11 do survive per TR-PR7-04 §5. M11 (reuse trial never minimizes) is an ordering/condition mutant. M9 (`origin_explicit` without the `explicit/` prefix filter) is a filter mutant, not an order mutant. See F2. |
| "`ancestor()` keeps raising `CalledProcessError` by historical design" | Factually correct: `tools/foundation.py:1735` runs `git merge-base --is-ancestor` with `check=True`. "by historical design" reads as a justification for a listed gap; the item stays open. See F2. |
| "driver errors, lost or late events, missing fixture tabs, group-count mismatches, non-quiescence and failed runs make the pair invalid and are listed" | Supported. `run_invalid_reasons()` lines 232-254; `adopt_mismatch` set on `missingSyntheticIds` or `groups != expected_groups` (lines 338-343); `not_quiescent` (line 358). Front failure also sets `adopt_mismatch` (line 347) and realize created-count mismatch sets `realize_mismatch` (line 329); neither is named, which understates. |
| "(container and window-count checks are not yet effective, see gaps)" | Container: correct (`containers < 3` cannot trip; smoke2/3 record 7). Window count: correct for the post-restart state, but the realize step does compare `windows` with the expected fixture window count (line 329, `realize_mismatch`). Understatement, not overstatement. See F2. |
| Smoke evidence | All 12 committed smoke runs have `missingSyntheticIds: []`, `groups: 50`, `windows: 11`; smoke2/3 `containers: 7`, `expected_groups: 50`; smoke3 `front.ok: true` in all four runs; smoke2 `p1-second` is the only `not_quiescent` run. Consistent with the row. |

| Statement (`closure2-windows-handoff.md`, `state.json`) | Status |
| --- | --- |
| Precondition: no Windows calibration until the Ubuntu instrument is qualified, (e) explained and controlled or detected as an invalidity, and that revision is on `main` | Matches closure2 (e) and the TR-PR7-05-F2 intent. Stricter than the recommended "results count only after". |
| "Port the qualified revision ... keeping its protocol constants and invalidity rules unchanged" | Carries over a future mode-detection invalidity rule. If (e) is resolved by a Wayland-specific control rather than a rule, the port needs an equivalent Windows control; the handoff does not say so, but that cannot be specified before the Ubuntu fix exists. No finding. |
| "The peak instrument above and the platform check below do not depend on this and may run first" | Contradicts the platform-check section, which runs "with the ported calibration instrument". See F1. |
| `state.json` 2): "Windows calibration only after 1) is on main" | Stricter than the handoff (1) includes the Ubuntu calibration run, the handoff requires only the qualified instrument revision on `main`). Not a weakening; observation only. |
| Commit message: "the calibration row now states exactly which invalidity checks are effective and tested" | Substantially, with the small omissions and the window-count understatement listed in F2. |

## 5. Status of TR-PR7-05 findings

| TR-PR7-05 finding | Status | Evidence |
| --- | --- | --- |
| F1 MINOR: calibration row overstated what is implemented/tested | RESOLVED (residual wording NIT in F2) | "Already implemented and unit-tested per rule" is replaced by "What is implemented: the summary's evaluation of each invalidity reason, unit-tested per rule", and the untested producers are named. The mismatch sentence now lists only effective checks and marks container and window-count checks as not yet effective. The gap list adds the untested producers, the restored driver tab, M9/M11 and `ancestor()`. No overstatement remains; the residual items understate or mislabel. |
| F2 MINOR: Windows handoff did not require resolving (e) before a Windows calibration run | RESOLVED | The handoff has an explicit precondition that forbids running the Windows calibration section until the qualified Ubuntu instrument revision that resolves (e) is on `main`, and the port must use that revision. `required_next_gate` now puts (e) and the instrument gaps first and lets Windows calibration follow only after them. The new contradiction about the platform check (F1) is a separate issue introduced by the fix, not a residual of this finding. |
| F3 NIT: duplicated "Linux-only" wording | RESOLVED | The sentence now says "Linux-only (cgroup v2, /proc, Wayland compositor), not yet qualified candidate" once, and the paragraph is rewrapped to the surrounding line length. |

## Findings

### WS-E01-TR-PR8-F1

- Severity: MINOR
- Status: OPEN
- Description: The new handoff precondition says "The peak instrument above and the platform
  check below do not depend on this and may run first", and `state.json.required_next_gate` 2)
  says "hard-peak instrument and platform check may run first". The platform-check section
  ("Discarded tabs in groups") says to repeat the closure2 (d) observation "with the ported
  calibration instrument". The only porting instruction is in the gated section: "Port the
  qualified revision for Windows before running it". An operator cannot follow both. Either the
  platform check waits for the qualified revision, which contradicts "may run first", or it
  uses a port of the current unqualified candidate, which the handoff does not authorize or
  scope. The handoff is the executable instruction for the Windows session. No F01 gate is closed
  or weakened: the (d) check feeds the F03 obligation and is not one of the three `open_gates`,
  and its effect size (about 110 % of one core after API realization against near idle after
  native restore) is far larger than the about 22 pp two-mode split.
- Recommended fix: In the handoff, state that the platform check may use a Windows port of the
  current candidate instrument (fields `api_realized_settled_10s`, `native_restored_settled_10s`).
  Its values are platform-observation evidence only and are not calibration. Alternatively, move
  the platform check behind the precondition and drop it from "may run first" in both the
  handoff and `state.json`.

### WS-E01-TR-PR8-F2

- Severity: NIT_OR_SUGGESTION
- Status: OPEN
- Description: Small inaccuracies in the new `closure2.md` Ubuntu-calibration cell:
  - The untested producers list "(post-restart state comparison, foreign-load windows, front
    step)" omits the quiescence producer (M19 and M26 survive).
  - "surviving mutants per TR-PR7-05": the mutant runs are in TR-PR7-04 §5; TR-PR7-05 cites them.
  - "two closure-probe order mutants (M9/M11)": M9 is the `explicit/` prefix-filter mutant of
    `origin_explicit`, not an order mutant.
  - "container and window-count checks are not yet effective": the realize step does compare the
    window count (`realize_mismatch`, `calibration_probe.py:329`); only the post-restart window
    count is not compared. Front failure and the realize created-count check also make a run
    invalid but are not named. These understate, they do not overstate.
  - "`ancestor()` keeps raising `CalledProcessError` by historical design" reads as a
    justification although the item is listed as an open gap.
- Recommended fix: Add the quiescence flag to the untested producers. Cite "TR-PR7-04 §5" for
  the mutants. Say "M9 (prefix filter) and M11 (minimize order)". Say "post-restart container
  and window-count checks". Drop "by historical design" or say "is unchanged".

## Fitness

The follow-up removes the overstatement in the calibration row, adds an explicit precondition
that stops a Windows calibration on the unqualified instrument, and orders the remaining F01
steps with F02 explicitly excluded. All three F01 measurement gates stay open,
`merge_authorized` stays false, no code changes, and the review copy is byte-identical. The new
findings are an instruction inconsistency for the non-gating platform check (MINOR) and wording
precision (NIT). Neither closes or weakens a gate.

TECHNICAL_REVIEW_OUTCOME: NO_OPEN_CRITICAL_BLOCKING_MAJOR
