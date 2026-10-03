# WS-E01-TR-PR7-20261002-02: Independent Technical Rereview of PR #7

- Reviewer identity: CLAUDE_SUBAGENT_INDEPENDENT_TECHNICAL_REVIEWER_WS_E01_TR_PR7_20261002_02
- Review type: technical review (Foundation 2 §30, ELEVATED risk increment). This is not a Feature
  Acceptance and not an epic verdict.
- Repository: felixvonvollmer-png/Firefox---WindowSafe, PR #7, branch `feature/ws-e01-f01-closure`
- Reviewed head SHA: `9b017ddbd88a94addee2c17638caf020eecbd818`
- Base (main): `f83845a1dd4b78bd010e6477612d95a99b1a8152`
- Reviewed diff: `git diff f83845a1dd4b78bd010e6477612d95a99b1a8152 9b017ddbd88a94addee2c17638caf020eecbd818`
  (130 files; commits `8ae803d`, `d2fd8c9`, `9b017dd`, single-parent chain on `f83845a`)
- Date: 2026-10-02

## Independence statement

I am a freshly started subagent with no prior context on this change. I did not author,
materialize or contribute to PR #7, PR #3, PR #6, the earlier technical reviews
(WS-E01-TR-PR6-20261001-01/-02, WS-E01-TR-PR7-20261002-01) or any WS-E01 preparation,
correction, rebinding or authorization artifact. I read TR-PR7-01 only as the committed
subject file in the PR. There was no expected outcome.

Worktree hygiene: `/home/felix/projekte/windowsafe-review-pr7b` was read-only. `git rev-parse HEAD`
was `9b017ddbd88a94addee2c17638caf020eecbd818` and `git status --porcelain --ignored` was empty
before and after the review. CLI gates ran with `PYTHONDONTWRITEBYTECODE=1`. Tests, mutants and
the closure-probe rerun ran only in disposable clones under the session scratchpad. The main
repository `/home/felix/projekte/firefox WindowsSaver addon` was not modified (its Firefox 156
binary was only hashed and executed). No pushes, no gh mutations, no real browser profile
(`--no-remote --new-instance`, new synthetic profile, clone-local `build/`).

## Commands run (python3 3.14.4)

In the worktree at the reviewed head:

| Command | Exit |
| --- | --- |
| `python3 tools/foundation.py check` | 0 |
| `python3 tools/foundation.py history --base f83845a1dd4b78bd010e6477612d95a99b1a8152` | 0 |
| `python3 tools/foundation.py history --base 1cb82c926903b2fd6b497d008db61c71c5d92aca` | 0 |
| `python3 tools/foundation.py schema-preflight --sha HEAD --schema reviews/review-contract.json` | 0 |
| `python3 tools/foundation.py request --subject epics/WS-E01/deltas/WS-E01-EP-DELTA-20260929-04/subject.json` | 0 |
| `python3 tools/foundation.py request --subject epics/WS-E01/deltas/WS-E01-EP-DELTA-20260929-03/subject.json` | 0 |
| `python3 tools/foundation.py request --subject epics/WS-E01/deltas/WS-E01-EP-DELTA-20260929-02/subject.json` | 0 |
| `python3 tools/foundation.py request --subject epics/WS-E01/subject.json` | 0 |
| `python3 tools/foundation.py request --subject foundation/deltas/WS-PFDELTA-MAT-20260928-01/subject.json` | 0 |
| `git diff --check f83845a HEAD` | 0 |

Request equivalence: the same five `request` commands with the base tool in a clean clone at
`f83845a` exit 0 and `cmp` shows byte-identical output between base and head (SHA-256 prefixes
`d1fd5fad65514`, `a28727275e3db`, `07ac5dcd476db`, `3703af82dc7da`, `588d9ecc67870`, identical
to the values recorded in TR-PR6-02 and TR-PR7-01). The five subject files themselves are
byte-identical to base.

In scratch clones at the reviewed head:

| Command | Exit |
| --- | --- |
| `python3 -m unittest discover -s tests` (full suite) | 0 (Ran 213 tests in 876 s, OK skipped=6: Windows-only `test_windows_job`) |
| 12 mutants (see mutation table), each restored afterwards; clone left clean | see table |
| Rerun x2 `qualification/ws-e01-f01/closure_probe.py --firefox ".../build/f01/firefox/firefox" --firefox-sha256 7ea3daf0...a78a` | 0, 0 (status `OBSERVATIONS_COLLECTED__NO_GATE_SELF_ACCEPTANCE`, cleanup `OWN_PROFILE_REMOVED__OWN_CGROUP_EXITED`; evidence.json SHA-256 `c45c684d864540e1e198a5c56a0aad7b110a21d50cab504aa11fe9af8d49b189` and `c613d793ccd247cc8beb4ca1a85a3e72970616e633016a19ef2c9c9744b6e314`, scratchpad only; `closure_probe_sha256` `b32ef418...` = committed file) |

The local Firefox binary hashed to `7ea3daf0cdbe5ec27e4f2e7c644c25032169f8a2f2f15e438ff4379bf737a78a`.

## Exact-head CI

`gh run list --commit 9b017ddbd88a94addee2c17638caf020eecbd818`, waited with `gh run watch`
until completed, then read-only `gh run view <id> --json ...` and `gh run view <id> --log`:

| Run ID | Event | Workflow | headSha | Conclusion | Notes |
| --- | --- | --- | --- | --- | --- |
| 37049259830 | pull_request | Foundation | `9b017dd...` | success | checkout `9b017dd`; CHECK OK; Ran 213 tests OK (skipped=6, 1018 s); SCHEMA-PREFLIGHT OK; 8x VALIDATE-RESULT OK; all five exact request steps success; BUILD OK; history and whitespace/clean-tree steps success |
| 37049253184 | push | Foundation | `9b017dd...` | success | same 17 steps all success; Ran 213 tests OK (skipped=6, 1037 s) |

## 1. Byte-identical transfer from PR #3 head `7d66ca5`

For every path in the cumulative diff I compared the blob at `9b017dd` with `7d66ca5`. All
transferred paths are blob-identical. Paths differing from or absent in `7d66ca5`:
`features/WS-E01-F01/state.json` (living, changed), new `closure2.md`, `closure2-artifacts.json`,
`closure2-ubuntu-run1..4.json`, `closure2-windows-handoff.md`,
`technical-review-ws-e01-tr-pr7-20261002-01.md`, `qualification/ws-e01-f01/closure_probe.py`,
`tests/test_closure_probe.py`, and the non-feature paths `tools/foundation.py`,
`tests/test_epic_execution.py`, `foundation/engineering.md` (3-line addition vs base) and
`epics/WS-E01/evidence/technical-review-ws-e01-tr-pr6-20261001-02.md`. All 127
`state.json.evidence_paths` entries exist; the only tracked F01/qualification files not listed are
`state.json` and the TR-PR7-01 copy (see F5).

Run-record binding: committed `closure2-ubuntu-run{1,2,3,4}.json` SHA-256 equal the
`evidence.json` hashes in `closure2-artifacts.json`; runs 3/4 carry `closure_probe_sha256`
`b32ef418...`, equal to the committed instrument; runs 1/2 carry the earlier `d07f83c1...`
(historical, labeled "first instrument"). All four: same binary hash, Wayland/GNOME session,
own profile removed, own cgroup exited, extension PID inside the owned cgroup.

## 2. Ubuntu closure evidence (claims vs run JSON)

| Claim in `closure2.md` | Status |
| --- | --- |
| (a) Taskbar Tab window is `type: normal` via `windows.getAll`; ordinary restore without `taskbartab`, active tab loaded, background discarded, URLs intact; all four runs | Supported (runs 1-4 and both reruns) |
| (b) `screens` undefined, one 1920x1080 display | Supported |
| (b) `left/top` always 0; requested positions have no observable effect | Supported (wording now "no observable effect") |
| (b) later sizes applied (800x600, 850x600 in runs 3/4, stable after three equal read-backs) | Supported for runs 3/4 and both reruns (`immediate == settled`, `settledStable: true`) |
| (b) "Run 2's immediate read-back of 952x702 was a race" | NOT supported; see F3 |
| (b) `minimized` does not resolve within 3 s (runs 3/4) / 30 s (runs 1/2), window stays `normal` | Supported |
| (c)2 process +11.4 MB (Map), further +8.8 MB (IDB), release within 0.07 MB, largest 0.066 MB run 2 | Supported (Map 11,451,376 / 11,441,152 / 11,435,648 / 11,440,032; release deltas 59,008 / 66,432 / 51,216 / 56,432 bytes) |
| (c)3 typed-array pulse +25.5 to +25.8 MB, point reporter never sees it | Supported for runs 1-4 (25,481,216 .. 25,759,744); my reruns 25,600,000 and 25,329,664 (slightly below the stated range, above 25,165,824 logical) |
| (c)3 reuse: without minimize +29.1/+29.2 MB, with minimize +39.9/+40.9 MB | Supported numerically (29,114,368 / 29,220,864 vs 39,915,520 / 40,906,752). Reruns: without 32,206,848 / 36,073,472, with 40,919,040 / 41,435,136 |
| (c)3 "the minimize condition removed it in these trials" | Overstated; see F2 |
| (c)3 "measured procedure with a stated condition, not a proven upper bound"; F05 cross-check | Sound as wording; cross-check not operationalized, see F2 |
| F01 not complete; Windows hard-peak instrument OPEN; no F02 product code | Supported (`status` `WS-E01-F01_OPEN__WINDOWS_PEAK_INSTRUMENT_RUN_REQUIRED`, `product_implementation_started: false`, `merge_authorized: false`) |
| Dispositions table (A/B, overhead/uncertainty, Windows intervals) | See F1 |

## 3. Harness changes

- `execution_history`: `ancestor(parents[0], parents[1])` plus tree equality means every accepted
  merge equals a descendant of its first parent; NUL-parsed `git diff-tree -r -z --no-renames
  --ignore-submodules=none --name-status` (two-tree form, no header line; trailing empty element
  handled by the `zip` of even/odd slices).
- `check()`: `git ls-files --cached -s -z`, mode must be `100644`/`100755`, now covered by
  `test_check_rejects_non_regular_tracked_modes` (ROOT patched to the fixture, so the
  `root == ROOT` branch runs).
- `self_verdict`: strip+casefold on implementer membership and identity. The legacy branch
  without `review_excluded_identities` still uses casefold without strip (unchanged; not a
  regression).
- `feature_path` admits `features/<ID>/start.json`.
- `foundation/engineering.md` wording matches the code.

Mutation table (scratch clone; targeted tests named in parentheses):

| Mutant | Result |
| --- | --- |
| M1 drop `check()` tracked-mode `require` (`test_check_rejects_non_regular_tracked_modes`) | killed |
| M2 drop `ancestor(parents[0], parents[1])` (`test_hand_built_merge_cannot_drop_main_changes`) | killed |
| M3 porcelain `git diff` instead of `diff-tree` (`test_gitlink_rejected_even_with_permissive_diff_config`) | killed |
| M4 `self_verdict` identity without strip (`test_self_verdict_normalizes_like_the_request`) | killed |
| M5 implementer membership unnormalized (same test) | killed |
| M6 drop merge tree-equality `require` (`tests.test_epic_execution`) | killed |
| M7 `storage_rows` without `/storage/` (`tests.test_closure_probe`) | killed |
| M8 `process_explicit` without `units == 0` (`tests.test_closure_probe`) | killed |
| M9 `origin_explicit` without `explicit/` prefix (`tests.test_closure_probe`) | survived (F5) |
| M10 remove `minimize()` immediately before `reset_high_water` (`tests.test_closure_probe`) | survived (F5; instrument flow untested) |
| M11 reuse trial never minimizes (`tests.test_closure_probe`) | survived (F5) |
| M12 drop `start.json` from `feature_path` | `check` exit 1 (FOUNDATION_GATE_FAILED) |

The instrument code was read: `minimize()` is now called after the non-minimized
`m4-before-pulse` report and immediately before `clear_refs`, with nothing in between, which
addresses the reset-baseline defect named in TR-PR7-01-F1.

## 4. Status of TR-PR7-01 findings

| TR-PR7-01 finding | Status | Evidence |
| --- | --- | --- |
| F1 MAJOR: VmHWM delta claimed as upper bound; Ubuntu gate closed on it | PARTIALLY RESOLVED | The unconditional bound claim is gone from `closure2.md`, the run `semantics` and the Windows handoff; the method now requires minimize immediately before reset (verified in code); reuse trials were added and show real undercount without the condition; the gate is renamed `MEASUREMENT_FINAL_ATTRIBUTION__UBUNTU_METHOD` with basis "qualified with conditions ... not a proven upper bound; F05 cross-check required". I judge "measured procedure with a stated condition" an honest characterization and "method qualified with conditions" an acceptable Ubuntu status, because a minimized reset baseline lies at or below the r6 §9.1 resting value (direction is conservative) and the residual risk is declared. This acceptance is conditional: it holds only if the F05 cross-check is operationalized and carried as a binding open item. At this head it is not (new F2). Remaining defects: the trials do not show that the condition removes undercount, and the Windows pass rule cannot detect the demonstrated undercount (new F2, F3). TR-PR7-01's further suggestions (free-but-resident figures at reset, offset contrast) were not adopted. I do not raise them separately: after `minimizeMemoryUsage` there is little free-but-resident memory left to reclaim, so the offset/reuse path is covered by the reuse trials plus the fresh-state control recommended in F2. |
| F2 MINOR: geometry size race, position wording | RESOLVED in substance | Bounded update wait plus settle-aware read-back; runs 3/4 and both of my reruns show 800x600/850x600/850x600 with `settledStable: true`; position wording now "no observable effect". A residual misattribution in the text is new F4. |
| F3 MINOR: `state.json` bookkeeping | RESOLVED | `WINDOWS_DESKTOP__WEBAPP_BOUNDARY` closed entry with evidence; `feature_changeset` split into the historical PR #3 range and `f83845a..candidate`; `non_feature_intervening_changes` lists PR #6 and this PR's harness changes; `continuation_start_head` is `f83845a` (ancestor of head); `continuation_manifest` points to `closure2-artifacts.json`. |
| F4 MINOR: missing dispositions | DISPOSITIONED, but the disposition is not acceptable for two items | A dispositions table and `open_for_f05` now exist. The A/B with-real-add-on deferral to F05 matches r6 §9.1. Deferring instrument overhead/paired uncertainty and the Windows interval/identity item past the start of F02 conflicts with r6 §9.3/§10.2; see new F1. |
| F5 NIT: IDB label, 0.06 MB, docstring, forced-cleanup condition, helper tests | RESOLVED | `storage_rows`/`storage_explicit_all_processes` "context only"; "within 0.07 MB ... largest 0.066 MB"; docstring corrected; r6 §10.2 condition stated; `tests/test_closure_probe.py` (M7, M8 killed; M9 survives, F5 below). |
| F6 NIT: `check()` mode guard untested | RESOLVED | `test_check_rejects_non_regular_tracked_modes`; mutant M1 killed. |

## Findings

### WS-E01-TR-PR7-02-F1

- Severity: MAJOR
- Status: OPEN
- Description: The new dispositions table in `closure2.md` and `state.json.open_for_f05` move
  "instrument overhead and paired uncertainty" ("measured and reported in F05; OPEN until then")
  and "Windows complete short-lived PID identity coverage, final interval boundaries" out of F01
  into F05. `open_gates` now contains only the Windows hard-peak item, and `required_next_gate`
  goes from the single Windows peak run directly to F01 technical review and Feature Acceptance.
  `closure2.md` itself states that the measurement method must be bound for both target OSes
  before the affected product implementation (F02). r6 §9.3 lists "Messwerkzeug ...,
  Warm-up, Messintervall und bekannte Messunsicherheit" among what is bound "vor Beginn der
  betroffenen Produktimplementierung"; only the actual results come later. §10.2 repeats that
  the concrete measurement method is bound before the affected implementation and that later
  evidence does not move these duties to acceptance. Preparation §4 item 3 asks F01 to finish
  qualifying the cross-OS measurement method and attribution. The transferred F01 scope said the
  same: `win-continuation.md` item 4 requires "measured driver overhead and declared uncertainty"
  on both OSes, and `ubuntu-closure.md` lists "(c) final cross-OS cache/residual/peak/overhead
  method qualification" as remaining F01 work, noting that on/off overhead and paired uncertainty
  "remain unmeasured". `closure2.md` moves these items to F05 without any rebinding.
  `qualification-plan.md` §F only requires F01 to *define* "uncertainty/measurement limitations".
  METHOD-01 does that ("Report ... profiler overhead, pair variance"), so §F is not the issue. The
  issue is the §9.3 requirement that the *known* uncertainty and the measurement interval be
  bound beforehand, together with the inherited F01 scope. The disposition's justification
  ("minimize/report run outside measured intervals; `clear_refs` is a single write") covers only
  the memory-peak instrument. It does not cover CPU/I-O driver overhead for L10/B300, which is
  the context of §9.3. The A/B runs with the real add-on legitimately belong to F05 (r6 §9.1). Instrument overhead
  and pair variance can be measured now with the synthetic probe add-on, for example with
  instrumentation on/off and repeated identical synthetic pairs, on both OSes. The Windows
  interval and identity-coverage question concerns the measurement interval of the bound
  instrument, not product behavior. As written, the plan lets F01 close and F02 start with
  these items unbound. That narrows a TF pre-implementation duty by agent disposition. This
  PR closes no gate on these items, so the problem is the planned route and the F01 completion
  criterion, not a false closure claim. Its effect is the same, though: the next step after the
  Windows run would be F01 acceptance with the items unbound.
- Recommended fix: return "instrument overhead and paired uncertainty" (memory peak and CPU/I-O
  driver overhead, pair variance with the synthetic probe on both OSes) and "Windows
  measurement-interval boundaries / identity coverage" to F01 `open_gates`. Extend
  `closure2-windows-handoff.md` and the Ubuntu plan so these are measured and declared before
  F01 completes. Alternatively obtain an explicit user decision and rebinding that allows the
  deferral. Keep only the real-add-on A/B results in `open_for_f05`.

### WS-E01-TR-PR7-02-F2

- Severity: MINOR
- Status: OPEN
- Description: The reuse-trial conclusion is stronger than the data supports, and the
  safeguard the Ubuntu method gate depends on is not operationalized:
  - `closure2.md` (c)3 says the minimize condition "removed" the undercount "in these trials".
    The commit message says "none with it". The trials show only that the with-minimize delta
    (39,915,520 / 40,906,752) exceeds the without-minimize delta (29,114,368 / 29,220,864). No
    fresh-state control exists (a string pulse with no prior hold/drop). The order is fixed
    (without always first), and there is no repeat. My two reruns at this head give
    without-minimize 32,206,848 / 36,073,472 and with-minimize 40,919,040 / 41,435,136, so the
    without arm varies by about 4 MB and the gap is 5-9 MB, not about 11 MB. "Reduced relative to
    the unminimized reset" is supported. "Removed" and "none" are not.
  - The closed gate's basis and (c)3 depend on "Final F05 peak claims must additionally
    cross-check against paired whole-cgroup `memory.peak`/RSS evidence; an unexplained
    discrepancy blocks a PASS". It states no compared quantities, tolerance or decision rule, and
    `open_for_f05` does not list it. The condition the gate was closed under is therefore not
    bound as a checkable obligation.
  - Minor: the pulse range "+25.5 to +25.8 MB (runs 1-4)" is correct for the committed runs. My
    rerun gave 25,329,664, so the range should not be read as a stable property.
- Recommended fix: reword to "reduced the observed reuse undercount; residual undercount not
  excluded". Optionally add a fresh-state string-pulse control and counterbalanced or repeated
  trials. Operationalize the F05 cross-check (which cgroup/RSS quantity, which comparison with
  the VmHWM delta, what discrepancy blocks) and add it to `open_for_f05` (or the method
  document) so it is binding.

### WS-E01-TR-PR7-02-F3

- Severity: MINOR
- Status: OPEN
- Description: The Windows handoff pass rule for the reuse trials is "with minimize, the
  string-pulse delta must not be materially below the logical string bytes". On Ubuntu the
  without-minimize arm, which `closure2.md` itself presents as the undercount case, already
  meets this rule: 29,114,368 / 29,220,864 (and 32-36 MB in my reruns) is above 25,165,824
  logical bytes. The rule therefore cannot detect the undercount the trials were added to
  detect. The without-minimize value is only "recorded", with no comparison required. The
  handoff also does not repeat the F05 cross-check obligation, and its opening says "Everything
  else in F01 is closed or reused", which conflicts with the dispositions table.
- Recommended fix: make the criterion discriminating. For example, require the with-minimize
  delta to exceed the without-minimize delta by a stated margin, and/or to be at least a
  fresh-state string-pulse delta within a stated tolerance, over repeated trials. Add the F05
  cross-check obligation and align the opening sentence with the open items.

### WS-E01-TR-PR7-02-F4

- Severity: MINOR
- Status: OPEN
- Description: `closure2.md` (b) says "Run 2's immediate read-back of 952x702 was a race". Run 2
  JSON shows steps 6/7/8 as 800x600 / 800x600 / 850x600, and 952x702 does not occur there at
  all. The 952x702 observation came from TR-PR7-01's rerun, not run 2. In runs 3/4 and my two
  reruns, `immediate == settled` at every step, so the data do not show that a settle race
  explains that observation. The race explanation fits the run 1/2 step 7 lag (800 instead of
  850). Not mentioned: `maximized` reports 1920x1080 in runs 1/2 but 1853x1048 in runs 3/4 and
  my reruns. The product consequence ("size is best-effort") is unaffected.
- Recommended fix: correct the sentence: runs 1/2 show a one-step lag at step 7 (old instrument,
  no settle wait), and an earlier independent rerun reported 952x702, which remains unexplained.
  Record the maximized-size difference as an observation.

### WS-E01-TR-PR7-02-F5

- Severity: NIT_OR_SUGGESTION
- Status: OPEN
- Description:
  - `technical-review-ws-e01-tr-pr7-20261002-01.md` is not in `state.json.evidence_paths`, unlike
    every other tracked F01 file except `state.json` itself.
  - The measurement-condition ordering in `closure_probe.py` `main()` (minimize immediately before
    reset; minimize only in the "with" reuse arm) has no unit or structural test. Mutants M10/M11
    survive, as does M9 (`origin_explicit` without the `explicit/` filter). Instrument flow is
    evidenced only by run records.
  - `ancestor()` raises `subprocess.CalledProcessError`, not `Invalid`, so a merge-ancestry
    rejection surfaces as an unnamed subprocess failure. It fails closed, and the test accepts
    either exception type.
  - The legacy `self_verdict` branch without `review_excluded_identities` still casefolds without
    strip (unchanged from base).
- Recommended fix: add the TR-PR7-01 copy to `evidence_paths`. Optionally factor the measurement
  sequence so a test can assert its order, add an M9-killing row, and map `CalledProcessError`
  from `ancestor` to `Invalid("execution merge ancestry")`.

## Other observations (no finding)

- No product code. No F02 start. `merge_authorized: false`; review and acceptance pending. F01
  correctly remains NOT complete.
- WS-P05 fallback and Ubuntu display/state evidence reproduce in my reruns. The Wayland
  `minimized` non-resolution reproduces (TIMEOUT_3S, window stays `normal`).
- The five historical request outputs are unchanged by the harness changes.

TECHNICAL_REVIEW_OUTCOME: CHANGES_REQUIRED
