# WS-E01-TR-PR7-20261002-01: Independent Technical Review of PR #7

- Reviewer identity: CLAUDE_SUBAGENT_INDEPENDENT_TECHNICAL_REVIEWER_WS_E01_TR_PR7_20261002_01
- Review type: technical review (Foundation 2 §30, ELEVATED risk increment). This is not a Feature
  Acceptance and not an epic verdict.
- Repository: felixvonvollmer-png/Firefox---WindowSafe, PR #7 (OPEN, not draft), branch
  `feature/ws-e01-f01-closure`
- Reviewed head SHA: `d2fd8c95f41fc274aa12e5aee2b2675677953d55` (matches `gh pr view 7` headRefOid)
- Base (main): `f83845a1dd4b78bd010e6477612d95a99b1a8152` (matches baseRefOid)
- Reviewed diff: `git diff f83845a1dd4b78bd010e6477612d95a99b1a8152 d2fd8c95f41fc274aa12e5aee2b2675677953d55`
  (126 files, 123 added, 3 modified; commits `8ae803d`, `d2fd8c9`, single-parent, parent chain
  `d2fd8c9 -> 8ae803d -> f83845a`)
- Date: 2026-10-02

## Independence statement

I am a freshly started subagent with no prior context on this change. I did not author,
materialize or contribute to PR #7, PR #3, PR #6, the earlier technical reviews
WS-E01-TR-PR6-20261001-01/-02, or any WS-E01 preparation, correction, rebinding or authorization
artifact. A previous reviewer attempt for this PR was aborted before producing a result; I did
not see any output of it. There was no expected outcome.

Worktree hygiene: `/home/felix/projekte/windowsafe-review-pr7` was treated as read-only. Before
and after the review `git rev-parse HEAD` was `d2fd8c95f41fc274aa12e5aee2b2675677953d55`,
`git status --porcelain --ignored` was empty and there were 0 `__pycache__` directories. CLI
gates ran with `PYTHONDONTWRITEBYTECODE=1`. Tests, mutants, adversarial probes and the optional
closure-probe rerun ran only in disposable clones under the session scratchpad. The main
repository `/home/felix/projekte/firefox WindowsSaver addon` was not modified (its Firefox 156
binary was only read and executed). No pushes, no gh mutations. No real browser profile was
used; the user's running snap Firefox was not touched (`--no-remote --new-instance`, new
synthetic profile, clone-local `build/`).

## Commands run (python3 3.14.4)

In the worktree at the reviewed head:

| Command | Exit |
| --- | --- |
| `python3 tools/foundation.py check` | 0 |
| `python3 tools/foundation.py history --base f83845a1dd4b78bd010e6477612d95a99b1a8152` | 0 |
| `python3 tools/foundation.py history --base 1cb82c926903b2fd6b497d008db61c71c5d92aca` | 0 |
| `python3 tools/foundation.py schema-preflight --sha HEAD --schema reviews/review-contract.json` | 0 |
| `python3 tools/foundation.py request --sha HEAD --subject epics/WS-E01/deltas/WS-E01-EP-DELTA-20260929-04/subject.json` | 0 |
| `python3 tools/foundation.py request --sha HEAD --subject epics/WS-E01/deltas/WS-E01-EP-DELTA-20260929-03/subject.json` | 0 |
| `python3 tools/foundation.py request --sha HEAD --subject epics/WS-E01/deltas/WS-E01-EP-DELTA-20260929-02/subject.json` | 0 |
| `python3 tools/foundation.py request --sha HEAD --subject epics/WS-E01/subject.json` | 0 |
| `python3 tools/foundation.py request --sha HEAD --subject foundation/deltas/WS-PFDELTA-MAT-20260928-01/subject.json` | 0 |

Historical request equivalence: the same five `request` commands with the base tool in a clean
clone at `f83845a` all exited 0 (base `check` also 0), and `cmp` shows byte-identical output
between base and head:

| Subject | Request output SHA-256 (base == head) |
| --- | --- |
| `epics/WS-E01/deltas/WS-E01-EP-DELTA-20260929-04/subject.json` | `d1fd5fad655148a50598dcaa449a055fb581855ed0d1c03597e4a15e9e243807` |
| `epics/WS-E01/deltas/WS-E01-EP-DELTA-20260929-03/subject.json` | `a28727275e3db9a4f54929a4f9bbce299888a7c2e3d96ed4ecb3d9c11f314579` |
| `epics/WS-E01/deltas/WS-E01-EP-DELTA-20260929-02/subject.json` | `07ac5dcd476dbc403f020036dbc6d9fde627d6e62aca1b55436ac6bb9ec32f16` |
| `epics/WS-E01/subject.json` | `3703af82dc7da732861b90bc13c97bcc2ed4a2fd76357afd7278ebfdf69dc338` |
| `foundation/deltas/WS-PFDELTA-MAT-20260928-01/subject.json` | `588d9ecc678702938302a124b168eaeea2db97a5547652c1b280d7930f957987` |

These are also identical to the values recorded in WS-E01-TR-PR6-20261001-02.

In scratch clones at the reviewed head:

| Command | Exit |
| --- | --- |
| `python3 -m unittest discover -s tests -v` (208 tests, 907 s, OK skipped=6: Windows-only `test_windows_job`) | 0 |
| 9 mutants, each `python3 -m unittest tests.test_epic_execution` | see mutation table |
| Adversarial history probes (`request` / `check` / `history --base f83845a`) | see probe table |
| Optional rerun `qualification/ws-e01-f01/closure_probe.py --firefox ".../build/f01/firefox/firefox" --firefox-sha256 7ea3daf0...a78a` | 0 (status `OBSERVATIONS_COLLECTED__NO_GATE_SELF_ACCEPTANCE`, cleanup `OWN_PROFILE_REMOVED__OWN_CGROUP_EXITED`; evidence.json SHA-256 `6867ae9a87866743b7f52be74ba17a674ca0b9e9fd6a574cd46b129cc9eb815f`, retained in the session scratchpad only) |

The local Firefox binary hashed to `7ea3daf0cdbe5ec27e4f2e7c644c25032169f8a2f2f15e438ff4379bf737a78a`
before the rerun.

## Exact-head CI

Read-only `gh run view <id>` and `gh run view <id> --log`:

| Run ID | Event | Workflow | Conclusion | Notes |
| --- | --- | --- | --- | --- |
| 36903482353 | pull_request | Foundation | success | checkout `d2fd8c9`; CHECK OK; Ran 208 tests OK (skipped=6, 1015 s); SCHEMA-PREFLIGHT OK; 8x VALIDATE-RESULT OK; all five exact request steps success; BUILD OK; HISTORY OK; whitespace/clean-tree step success |
| 36903475913 | push | Foundation | success | same steps; Ran 208 tests OK (skipped=6, 1008 s); all steps success |

## 1. Byte-identical transfer from PR #3 head `7d66ca5`

For every path in the diff I compared blob ID and mode at `d2fd8c9` with `7d66ca5`. The file
lists of `features/WS-E01-F01/**`, `qualification/ws-e01-f01/**`,
`tests/test_target_qualification.py` and `tests/test_windows_job.py` at both commits differ only
by the six new paths (`closure2-artifacts.json`, `closure2.md`, `closure2-ubuntu-run1.json`,
`closure2-ubuntu-run2.json`, `closure2-windows-handoff.md`, `closure_probe.py`). Every other
transferred path is blob- and mode-identical to `7d66ca5`. Paths that differ from `7d66ca5`:
`features/WS-E01-F01/state.json` (living, modified), the six new closure files, and the
non-feature changes `tools/foundation.py`, `tests/test_epic_execution.py`,
`foundation/engineering.md` and the new preserved review
`epics/WS-E01/evidence/technical-review-ws-e01-tr-pr6-20261001-02.md`. Result: transfer
verified byte-identical. Every tracked F01/qualification file except `state.json` itself is
listed in `state.json.evidence_paths` (all 125 entries exist).

## 2. Ubuntu closure evidence

Verified against the run JSON (and my rerun):

| Claim in `closure2.md` | Status |
| --- | --- |
| Probe binding: `closure_probe_sha256` `d07f83c1...` equals the committed file; `driver_sources` hashes equal committed `run_probe.py`, `target_probe.py`, `measure.py`, `windows_job.py`; binary SHA and build ID match | Supported |
| WS-P05: Taskbar Tab window with native `taskbartab` is `type: normal` via `windows.getAll`; ordinary restore gives a window without `taskbartab`, active tab loaded, background tab `discarded: true`, URLs intact | Supported (both runs and rerun) |
| Windows reused for (a) | Supported by `win-qualification.md` (Taskbar Tab exposed as `normal`, public create path exercised) |
| `nsIScreenManager.screens` undefined, one 1920x1080 display, far rect maps to primary | Supported |
| Wayland `left/top` always 0; positions not restorable | Supported as observed (reported values); see F2 for wording |
| Requested sizes after creation are ignored | NOT supported; see F2 |
| maximized/normal/fullscreen complete; `minimized` update times out after 30 s in both runs; window usable afterwards | Supported (step 2 OPEN script timeout, step 3 completes; reproduced in rerun) |
| Map +11.0 MB origin / +11.4 MB process; IDB +8.7 MB origin; IDB-bucket +0.19 MB | Supported numerically (run1 10,996,656 / 11,451,376 / 8,699,760 / 192,512 bytes); see F5 for the IDB label |
| Release back to baseline within 0.06 MB | Origin yes; process 0.059 MB (run1) and 0.066 MB (run2); see F5 |
| 24 MiB pulse: VmHWM delta 25,481,216 / 25,563,136 bytes; point reporter unchanged after pulse | Supported (rerun 25,751,552; unchanged reporter totals) |
| VmHWM delta is a conservative upper bound; a pass against 8/16 MiB on it is sound | NOT supported; see F1 |
| F01 not complete; Windows add-on hard-peak instrument OPEN; no F02 product code | Supported; `state.json` status `WS-E01-F01_OPEN__WINDOWS_PEAK_INSTRUMENT_RUN_REQUIRED`, `product_implementation_started: false`, `merge_authorized: false`, review/acceptance pending |
| Boundaries: synthetic disposable profile, localhost fixtures, owned transient cgroup, chrome automation TEST_ONLY, profile removed | Supported by the instrument code, run records and my rerun (no profile left; cgroup exited) |

## 3. Harness changes and TR-PR6-02 findings

| TR-PR6-02 finding | Status | Evidence |
| --- | --- | --- |
| F1 MINOR: merges could drop main-side changes | RESOLVED | `ancestor(parents[0], parents[1])` added. Probes A1 (second parent ancestor of first), A2 (stale theirs-tree merge dropping a main-only `tests/` file) and A3 (merge reverting a later `tests/` commit) are all REJECTED by request/check/history; a normal up-to-date `--no-ff` merge stays ACCEPTED (0/0/0). Mutant N1 killed by `test_hand_built_merge_cannot_drop_main_changes`. Structurally, every accepted merge now has the tree of a descendant of its first parent, so all content changes appear in checked single-parent commits. `engineering.md` wording now matches. |
| F2 MINOR: M08 (authorization integrity in `epic_delta_history`) untested | RESOLVED | `test_forged_initial_authorization_rejected`; mutant N6 killed (regex `authorization hash` no longer matches). |
| F3 NIT: porcelain `git diff` honours `diff.ignoreSubmodules` | RESOLVED | `git diff-tree -r -z --no-renames --ignore-submodules=none --name-status`, NUL-parsed. Probe D1 (gitlink with `GIT_CONFIG_*` `diff.ignoreSubmodules=all`) REJECTED; D0 and a symlink REJECTED. Mutant N2 (back to porcelain) killed by `test_gitlink_rejected_even_with_permissive_diff_config`. N3 (drop `--ignore-submodules=none`) survives as an equivalent mutant (plumbing does not read the porcelain config). |
| F4 NIT: `self_verdict` exact implementer match | RESOLVED | strip+casefold on both sides; mutant N5 killed by `test_self_verdict_normalizes_like_the_request`. |

Other harness changes: `feature_path` admits `features/<ID>/start.json` (needed for the
transferred `start.json`; mutant N7 survives the unit tests but is killed by `check` at HEAD).
`check()` now rejects tracked non-regular modes via `git ls-files -s`; see F6.

Additional probes (all at current head harness): deleting `tests/test_windows_job.py` REJECTED;
editing `foundation/subject.json` REJECTED; adding a new feature evidence JSON ACCEPTED.

Mutation table (`tests.test_epic_execution`):

| Mutant | Result |
| --- | --- |
| N1 remove `ancestor(parents[0], parents[1])` | killed |
| N2 revert to porcelain `git diff` | killed |
| N3 drop `--ignore-submodules=none` | survived (equivalent) |
| N4 remove `check()` tracked-mode `require` | survived (see F6) |
| N5 revert `self_verdict` normalization | killed |
| N6 remove `execution_authorization_integrity` in `epic_delta_history` (old M08) | killed |
| N7 remove `start.json` from `feature_path` | survived unit tests; killed by `check` at HEAD |
| N8 remove execution file-mode `require` | killed |
| N9 remove merge tree-equality `require` | killed |

## Findings

### WS-E01-TR-PR7-F1

- Severity: MAJOR
- Status: OPEN
- Description: `state.json` closes `MEASUREMENT_FINAL_ATTRIBUTION__UBUNTU` with basis
  "METHOD-02 coverage contrasts and VmHWM peak bound", and `closure2.md` §(c)3 states without
  condition that the VmHWM delta "is a conservative upper bound ... a pass against 8/16 MiB on it
  is sound". The run records themselves only call it an "upper-bound candidate" (`semantics`
  field). The evidence demonstrates sensitivity only: one freshly mapped 24 MiB pulse yields a
  delta of at least its logical size. Nothing demonstrates the property a pass rule needs,
  namely that the delta cannot undercount:
  - Baseline mismatch: r6 §9.1 defines additional peak above the resting attributable add-on
    value; the instrument measures process RSS growth above the RSS at `clear_refs` time.
  - Undercount paths are neither excluded nor tested: resident but free memory at reset
    (allocator dirty pages, retained GC chunks, garbage not yet collected) can be reused by the
    operation without raising RSS, and reclamation during the operation offsets growth. A large
    `Uint8Array` is freshly mapped and cannot show this; an export made of many small
    allocations can.
  - The precondition that would make the claim plausible is not part of the method. The method
    text in `closure2.md` §(c)3 ("reset ... run the operation, read VmHWM") does not require
    minimize before the reset. The committed run did minimize at `m3-released`, but then took a
    full, non-minimized memory report (`m4-before-pulse`, which itself allocates) before
    `clear_refs`. So even there the reset baseline is not the quiesced state.
  Because §§9.1/10.2 require the method to be bound before the affected implementation, closing
  the Ubuntu measurement gate on an unproven pass rule is a gate claimed beyond evidence. The
  Windows handoff copies the same sensitivity-only pass criterion.
- Recommended fix: reword the bound as conditional; require `minimizeMemoryUsage` immediately
  before `clear_refs`; record allocator/GC free-but-resident figures (for example
  `heap-unclassified`, `heap-dirty`/`page-cache`, GC unused chunks) at reset; add a reuse
  contrast (allocate N small objects, release, do not minimize, reset, allocate N again, compare
  the delta with the first) and an offset contrast. Until then either keep the Ubuntu peak item
  OPEN or label it "candidate bound pending reuse/offset contrast", and apply the same criteria to
  `closure2-windows-handoff.md`.

### WS-E01-TR-PR7-F2

- Severity: MINOR
- Status: OPEN
- Description: `closure2.md` (b) says "requested sizes after creation are ignored by the
  compositor". The committed runs contradict this: step 6 (request 800x600) reports 800x600 and
  step 8 reports 850x600 in both runs, while step 7 reports 800x600. My rerun at the same head
  reports 952x702 for steps 6-8. The instrument explains the inconsistency: the driver's `update`
  operation breaks out of its wait loop immediately when no `state` is requested, so
  geometry-only updates are read back before the compositor settles. The readback is a race,
  and the claim is not supported either way. Separately, `left/top = 0` is what Firefox reports
  on Wayland; it shows positions are not observable/restorable, not that the compositor ignored
  them. The product consequence (size best-effort, position left to the compositor) remains
  reasonable.
- Recommended fix: wait for geometry-only updates to settle (poll until two equal readings or a
  bounded timeout, and record the timeline). Then restate the observation, for example "size
  updates after creation are applied nondeterministically / not reliably observable", and phrase
  the position finding as "not reported/observable on Wayland".

### WS-E01-TR-PR7-F3

- Severity: MINOR
- Status: OPEN
- Description: `state.json` bookkeeping is inaccurate after the transfer:
  - `WINDOWS_DESKTOP` leaves `open_gates` but is not in `closed_gates` and has no disposition
    entry. Only a prose row in `closure2.md` covers it. Preparation §4 states that the earlier
    gates are "nicht automatisch geschlossen".
  - `non_feature_intervening_changes: "NONE"` with `feature_changeset:
    3bdd7439...candidate` is false at this head. That range now contains the whole epic delta and
    rebinding and this PR's own harness changes (`tools/foundation.py`, `tests/`, 192 files).
  - `continuation_start_head` `ead9341` is not an ancestor of the head (PR #3 history was
    transferred, not merged), and `continuation_manifest` still points to the earlier
    `ubuntu-closure-manifest.json`.
  A later Feature Acceptance that binds to these fields would be misled.
- Recommended fix: add an explicit `WINDOWS_DESKTOP` disposition (for example "superseded:
  WebApp boundary answered by WS-P05; remaining item folded into
  MEASUREMENT_FINAL_ATTRIBUTION__WINDOWS_ADDON_HARD_PEAK", with evidence path). Correct
  `non_feature_intervening_changes` to list the intervening non-feature changes (or rebase the
  changeset on `f83845a`). Mark `continuation_start_head`/`continuation_manifest` as historical
  PR #3 references or update them for the CLOSURE2 run.

### WS-E01-TR-PR7-F4

- Severity: MINOR
- Status: OPEN
- Description: Narrowing `open_gates` to the single Windows hard-peak item drops remaining work
  recorded in the transferred evidence without any disposition:
  - `ubuntu-closure.md` says instrumentation on/off overhead and paired uncertainty "remain
    unmeasured". closure2 does not address this.
  - METHOD-02 step 4 (paired A/B cgroup/RSS native residual) is described but was not executed
    in the closure2 runs, which have no without-add-on arm.
  - `win-continuation.md` item 3 (complete descendant identity coverage and final measurement
    intervals on Windows) is not mentioned. The handoff covers only the hard peak plus contrasts.
  Some of these may legitimately belong to F05 implementation measurements. That must be stated,
  not implied.
- Recommended fix: give each item an explicit disposition in `closure2.md`/`state.json` (closed
  with evidence, deferred to a named later gate with rationale, or kept in `open_gates`), or
  extend the Windows handoff where it applies.

### WS-E01-TR-PR7-F5

- Severity: NIT_OR_SUGGESTION
- Status: OPEN
- Description: Smaller imprecisions in the method/report:
  - `indexeddb_rows` sums every explicit path containing `indexeddb`, `idb` or `/storage/`
    across all processes. "IndexedDB parent-process explicit memory" overstates its specificity:
    the baseline value is 7.2 MB.
  - "back to baseline within 0.06 MB": run2 process delta is 66,432 bytes (0.066 MB).
  - The `extension_process` docstring says "verified in /proc", but the /proc walk returns the
    PID regardless; the real verification is the subsequent cgroup membership check.
  - The METHOD-02 resting value uses forced `minimizeMemoryUsage`. Per r6 §10.2 this should be
    stated as a measurement condition, not as everyday behaviour.
  - `closure_probe.py` pure helpers (`origin_explicit`, `process_explicit`, `indexeddb_rows`)
    have no unit coverage.
- Recommended fix: rename/narrow the IDB bucket; correct the tolerance figure; fix the
  docstring; state the forced-cleanup condition; add small helper tests with synthetic report
  rows.

### WS-E01-TR-PR7-F6

- Severity: NIT_OR_SUGGESTION
- Status: OPEN
- Description: The new `check()` tracked-mode guard (`git ls-files -s`) has no test. Mutant N4
  survives the suite because tests call `f.check(self.repo)` with a non-`ROOT` root, which skips
  the block. Removing it in a scratch clone still leaves `check` failing on gitlink/symlink
  commits through other guards, so it is defence in depth and fails closed today.
- Recommended fix: add a test that exercises the `ls-files -s` mode branch (for example by
  factoring it into a function taking the `ls-files` bytes), or document it as untested
  defence in depth.

## Other observations (no finding)

- The harness changes do not alter any of the five historical request outputs.
- `features/` paths remain non-`protected()`, as previously noted in TR-PR6-02. `state.json`
  is living by design here.
- `test_windows_job` (6 tests) is skipped on Linux CI and locally; Windows-native accounting is
  evidenced only by the transferred Windows run records.

TECHNICAL_REVIEW_OUTCOME: CHANGES_REQUIRED
