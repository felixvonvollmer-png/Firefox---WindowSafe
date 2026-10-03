# WS-E01-TR-PR6-20261001-02: Independent Technical Rereview of PR #6

- Reviewer identity: CLAUDE_SUBAGENT_INDEPENDENT_TECHNICAL_REVIEWER_WS_E01_TR_PR6_20261001_02
- Review type: technical review (Foundation 2 §30, ELEVATED risk increment). This is not a feature acceptance and not an epic verdict.
- Repository: felixvonvollmer-png/Firefox---WindowSafe, PR #6 (OPEN, not draft), branch `exec/ws-e01-broad-authorization`
- Reviewed head SHA: `fcb5178691adf07a7ca0a89119cb20a94aa1c274` (matches `gh pr view 6` headRefOid)
- Base (main): `714b440c26167f6411420fbbda4be69deb2e9670` (matches baseRefOid)
- Reviewed diff: `git diff 714b440c26167f6411420fbbda4be69deb2e9670 fcb5178691adf07a7ca0a89119cb20a94aa1c274` (11 files, +818/-19; commits `03ae327`, `fcb5178`)
- Date: 2026-10-01

## Independence statement

I am a freshly started subagent with no prior context on this change. I did not author,
materialize or contribute to PR #6, to the earlier review WS-E01-TR-PR6-20261001-01, or to any
WS-E01 preparation, correction, rebinding or authorization artifact. There was no expected
outcome. I treated the worktree `/home/felix/projekte/windowsafe-review-pr6b` as read-only. All
tests, probes and mutations ran in disposable clones under the session scratchpad. I made no
pushes and no gh mutations, used no browser and touched no real profiles.

Worktree hygiene: before and after the review, `git rev-parse HEAD` was
`fcb5178691adf07a7ca0a89119cb20a94aa1c274`, `git status --porcelain --ignored` was empty, and
there were 0 `__pycache__` directories. CLI gates ran with `PYTHONDONTWRITEBYTECODE=1`. The main
repository `/home/felix/projekte/firefox WindowsSaver addon` was not modified.

## Commands run (python3 3.14.4)

In the worktree at the reviewed head:

| Command | Exit |
| --- | --- |
| `python3 tools/foundation.py check` | 0 |
| `python3 tools/foundation.py history --base 714b440c26167f6411420fbbda4be69deb2e9670` | 0 |
| `python3 tools/foundation.py history --base 1cb82c926903b2fd6b497d008db61c71c5d92aca` | 0 |
| `python3 tools/foundation.py schema-preflight --sha HEAD --schema reviews/review-contract.json` | 0 |
| `python3 tools/foundation.py request --sha HEAD --subject epics/WS-E01/deltas/WS-E01-EP-DELTA-20260929-04/subject.json` | 0 |
| `python3 tools/foundation.py request --sha HEAD --subject epics/WS-E01/deltas/WS-E01-EP-DELTA-20260929-03/subject.json` | 0 |
| `python3 tools/foundation.py request --sha HEAD --subject epics/WS-E01/deltas/WS-E01-EP-DELTA-20260929-02/subject.json` | 0 |
| `python3 tools/foundation.py request --sha HEAD --subject epics/WS-E01/subject.json` | 0 |
| `python3 tools/foundation.py request --sha HEAD --subject foundation/deltas/WS-PFDELTA-MAT-20260928-01/subject.json` | 0 |

Historical request equivalence: I ran the same five `request` commands with the base tool in a
clean clone at `714b440`. All exited 0, and the base `check` also exited 0. `cmp` shows the
outputs are byte-identical between base and head:

| Subject | Request output SHA-256 (base == head) |
| --- | --- |
| `epics/WS-E01/deltas/WS-E01-EP-DELTA-20260929-04/subject.json` | `d1fd5fad655148a50598dcaa449a055fb581855ed0d1c03597e4a15e9e243807` |
| `epics/WS-E01/deltas/WS-E01-EP-DELTA-20260929-03/subject.json` | `a28727275e3db9a4f54929a4f9bbce299888a7c2e3d96ed4ecb3d9c11f314579` |
| `epics/WS-E01/deltas/WS-E01-EP-DELTA-20260929-02/subject.json` | `07ac5dcd476dbc403f020036dbc6d9fde627d6e62aca1b55436ac6bb9ec32f16` |
| `epics/WS-E01/subject.json` | `3703af82dc7da732861b90bc13c97bcc2ed4a2fd76357afd7278ebfdf69dc338` |
| `foundation/deltas/WS-PFDELTA-MAT-20260928-01/subject.json` | `588d9ecc678702938302a124b168eaeea2db97a5547652c1b280d7930f957987` |

In a scratch clone at the reviewed head:

| Command | Exit |
| --- | --- |
| `python3 -m unittest discover -s tests` (190 tests, 1034 s) | 0 |
| 25 guard-removal mutants, each running `python3 -m unittest tests.test_epic_execution` (16 tests) | see mutation table |

Pinned hashes verified:
- `broad-execution-authorization.json` has SHA-256
  `cced59563b38d5356097ecc2f1efe3da385897023b8ac323882c0d3c5761db6d`, which equals
  `EPIC_EXECUTION_AUTH_SHA`.
- `rebinding.json` has SHA-256 `aacc8cce51e0ef7caf29d8d85bc3b5a2df7c8a628d255e6edd47a50d8796528f`,
  which equals `REQUIRED_EPIC_REBINDING.sha256`.

Preserved earlier review: `epics/WS-E01/evidence/technical-review-ws-e01-tr-pr6-20261001-01.md`
is byte-identical (`cmp`) to the original
`/home/felix/projekte/windowsafe-review-out/WS-E01-TR-PR6-20261001-01.md`. Both have SHA-256
`688148641810f7ffeda89f6c70cf9decd1e4cf889b984aa0d2a2e52a9a481d2a`.

## Exact-head CI

I ran `gh run list --commit fcb5178691adf07a7ca0a89119cb20a94aa1c274` (read-only), waited with
`gh run watch --exit-status` (exit 0 for both runs) and read the logs with `gh run view <id> --log`.

| Run ID | Event | Workflow | Conclusion | Notes |
| --- | --- | --- | --- | --- |
| 36894645038 | pull_request | Foundation | success | checkout `fcb5178`; CHECK OK; Ran 190 tests OK (1181 s); SCHEMA-PREFLIGHT OK; 8x VALIDATE-RESULT OK; inventory `c8abc11ce136ab501cac69f7ef6a5e80a18fdc92cf6c1c9fc47dd2867d69dfb6`; HISTORY OK; all steps success |
| 36894637184 | push | Foundation | success | same steps; Ran 190 tests OK (1008 s); same inventory SHA-256; all steps success |

The test step takes about 17-20 minutes, so the new 45-minute job timeout leaves a margin of
roughly 25 minutes.

## Status of earlier findings (WS-E01-TR-PR6-20261001-01)

| Earlier finding | Status | Evidence |
| --- | --- | --- |
| F1 MAJOR: `foundation/subject.json` editable during execution | RESOLVED | `EXECUTION_FROZEN_PREFIXES` now starts with `foundation/`; only `foundation/context.md` and `foundation/engineering.md` are living. Test `test_historical_foundation_records_frozen_but_living_routers_open` covers `foundation/subject.json`, `foundation/reviewer-environment.md`, `foundation/architecture.md` and a rename source. Mutants M01 and M22 are killed. The merge path is closed structurally, not by coincidence. Any side branch based before `eeddbcf` lacks `epics/WS-E01/deltas/WS-E01-EP-DELTA-20260929-04/rebinding.json` and would have to add it under a frozen prefix, which is rejected. Any base at or after `eeddbcf` has frozen content identical to `714b440`. Frozen prefixes cannot gain files during execution, so this holds for the whole phase. Probe B4 (side branch from `eeddbcf` restoring the execution files plus a `foundation/subject.json` edit, then merged) is REJECTED. |
| F2 MINOR: 8 of 16 mutants survived | PARTIALLY_RESOLVED | M05, M06, M10, M11, M12 and M15 are now killed. M08 (authorization integrity inside `epic_delta_history`) still survives; see WS-E01-TR-PR6-02-F2. M09 survives but is redundant by construction: the integration merge is the only boundary merge processed by the pre-execution loop. |
| F3 MINOR: contributors type confusion | PARTIALLY_RESOLVED | `contributors` must now be a list, and every author must be a non-empty string. Test `test_feature_contributors_must_be_a_list` covers this (M21 killed). The related NIT remains: `self_verdict` still requires an exact `req["implementer"] in excluded`, while `request` compares strip+casefold values. This fails closed but is inconsistent; carried as WS-E01-TR-PR6-02-F4. |
| F4 MINOR: harness/tests/workflow editable | DISPOSITIONED (documented residual) | Gate code under `tools/`, `tests/` and `.github/workflows/` cannot be deleted by single-parent commits (M18 killed). `foundation/engineering.md` now states that every harness, test or CI change is an ELEVATED increment with independent technical review before integration. Judgment: for an ELEVATED increment this residual is acceptable only as documented policy. A self-hosted harness cannot be its own trust root, and CI runs the PR's own harness. However, the mechanical "undeletable" half of the mitigation can be bypassed through merges (WS-E01-TR-PR6-02-F1). |
| F5 MINOR: up-to-date merge edge | DISPOSITIONED (documented residual) | `engineering.md` documents the merge flow: feature concurrency ONE, branch from current main, `gh pr merge --merge --match-head-commit`, no "Update branch", rebuild a stale PR from current main. `--match-head-commit` only guards the PR head, not movement of main; the document acknowledges this ("solange main nicht weitergezogen ist"). A GitHub branch-protection "require up to date" setting is still not recorded. The failure mode is fail-closed: a stale merge permanently blocks the gates and needs a reviewed harness change. Judgment: acceptable for ELEVATED with concurrency ONE; residual risk MINOR, no new finding. |
| F6 MINOR: object modes not checked | RESOLVED (with an environment caveat) | `execution_history` requires blob modes 100644 or 100755 for every non-deleted changed path. Test `test_only_regular_files_symlinks_and_submodules_rejected` covers both a symlink and a gitlink (M19 killed). Caveat: the check relies on porcelain `git diff`, which hides gitlinks under `diff.ignoreSubmodules=all`; see WS-E01-TR-PR6-02-F3. |
| F7 MINOR: routers inconsistent | RESOLVED | `README.md`, `AGENTS.md`, `epics/README.md` and `foundation/context.md` now state that execution under WS-EA-20261001-03 is current, mark PR #3 as historical read-only evidence and route worker scope to WS-EA-20261001-03. The remaining "Kein Featurestart" sentences in `epics/README.md` (lines 64 and 95) are scoped to historical WS-EA-20260919-05 and locator creation, so they are correct. |
| F8 NIT: rename detection, contract not protected, degenerate merge | PARTIALLY_RESOLVED | `--no-renames` is adopted (rename source caught; M20 killed), and degenerate merges are rejected. Porcelain `git diff` is retained instead of the plumbing `diff-tree` (see F3 below). `reviews/review-contract.json` is still not `protected()`. Merges cannot revert it today, for the same structural reason as F1. The degenerate-merge guard is untested (M17 survives; harmless, because such a merge has an identical tree). |

## Adversarial probes (disposable clones from the reviewed head, current harness)

| Probe | request / check / history |
| --- | --- |
| A1: commits add `tests/test_extra_guard.py` and `addon/x.ts`; then `commit-tree` merge with parents `(C2, fcb5178)` and tree `fcb5178^{tree}` (second parent is an ancestor of the first) | 0 / 0 / 0, ACCEPTED: the execution-added test is deleted by the merge |
| A2: main adds a gate test and a product file; a stale side branch from `fcb5178` adds `addon/y.ts`; merge with parents `(main, side)` and tree equal to the side tree | 0 / 0 / 0, ACCEPTED: main-only gate test and product file silently dropped |
| A3: a harness hardening commit (adds `features/` to `EXECUTION_UNDELETABLE_PREFIXES`, valid on its own) is reverted by a merge with parents `(H, fcb5178)` and tree `fcb5178^{tree}` | 0 / 0 / 0, ACCEPTED: reviewed hardening silently reverted, with no single-parent diff showing it |
| A1-A3 rerun against a scratch harness with `ancestor(parents[0], parents[1])` added | all REJECTED; a normal up-to-date `--no-ff` PR merge and linear commits stay ACCEPTED |
| B1: merge with an orphan root commit carrying an identical tree | REJECTED |
| B3: merge taking the pre-integration tree (`714b440^2`) | REJECTED (drops the protected authorization) |
| B4: side branch from `eeddbcf` re-adding the execution files plus a `foundation/subject.json` edit, merged | REJECTED |
| D0: gitlink `addon/sub.js` (mode 160000), default git config | REJECTED |
| D1: same gitlink with `diff.ignoreSubmodules=all` (via `GIT_CONFIG_*`) | 0 / 0 / 0, ACCEPTED |
| Forged authorization added on a branch from `714b440` (HARD_LIMITS shortened) | `request` REJECTED (`broad execution authorization hash`) |

Path tricks (traversal, backslash, colon, case variants, dot-prefixed or non-ASCII names,
`node_modules`, binary extensions, `.gitmodules`) are rejected by `safe_path`, the case-sensitive
`scope()`/`product_path()` regexes and the root allowlist. C-quoted paths in `git diff` output
fail `scope()`, so they fail closed.

## Mutation testing (`tests.test_epic_execution`, 16 tests; one scratch clone per mutant)

| Mutation | Result |
| --- | --- |
| M01 remove frozen-prefix check | killed |
| M02 remove `scope(path)` in `execution_history` | killed |
| M03 remove up-to-date tree equality | killed |
| M04 remove per-parent `check_history_maps` | killed |
| M05 remove octopus `require` | killed |
| M06 remove `ancestor(EPIC_INTEGRATION_MERGE, parents[0])` | killed |
| M07 remove feature exclusion subset | killed |
| M08 remove `execution_authorization_integrity` in `epic_delta_history` | SURVIVED |
| M09 remove `EPIC_INTEGRATION_MERGE in merges` | SURVIVED (redundant by construction) |
| M10 remove `delta_history(sha)` in feature request | killed |
| M11 remove feature ID/phase `require` | killed |
| M12 remove manifest guard in `scope()` | killed |
| M13 allow `node_modules` | killed |
| M14 drop `review_excluded_identities` transport for features | killed |
| M15 remove authorization integrity in `check()` | killed |
| M17 remove degenerate-merge `require` | SURVIVED (harmless: identical tree) |
| M18 remove gate-code deletion `require` | killed |
| M19 remove file-mode `require` | killed |
| M20 replace `--no-renames` with `-M` | killed |
| M21 remove contributors-list `require` | killed |
| M22 narrow frozen `foundation/` to the four historical subtrees | killed |
| M23 remove authorization STOP_AT/flag field checks | SURVIVED (equivalent under the hash pin) |
| M24 remove READY_FOR_AGENT check | SURVIVED (equivalent under the pinned rebinding hash) |
| M25 widen `FEATURE_ID_PATTERN` | killed |
| M26 remove author-string check | SURVIVED (removing it gives an AttributeError or subset failure instead of `Invalid`; still fails closed) |

One mutant was first killed by an artifact of my own mutation (trailing whitespace). I re-ran it
cleanly, and the table shows the clean result.

## New findings

### WS-E01-TR-PR6-02-F1

- Severity: MINOR
- Status: OPEN
- Description: An execution merge does not have to be an "up to date" PR merge. In
  `execution_history`, a two-parent commit is accepted when its tree equals `parents[1]`'s tree,
  `parents[0]` descends from `714b440`, and the parents differ. The rule never requires
  `ancestor(parents[0], parents[1])`, i.e. that the PR head contains main. As a result, a merge
  can discard every non-protected main-side change since the fork point: gate code under
  `tools/`, `tests/` and `.github/workflows/` added or hardened during execution, product files,
  `features/` evidence and living routers. Probes A1-A3 show the following, all with
  request/check/history exit 0:
  - an execution-added test module is deleted;
  - main-only gate and product files are dropped by a stale theirs-tree merge;
  - a harness hardening commit is silently reverted, with no single-parent diff showing it.

  This bypasses the "tools/, tests/, workflows cannot be deleted" guarantee that
  `foundation/engineering.md` cites as the mechanical half of the F4 mitigation. The
  `engineering.md` wording "PR-Merges sind nur up to date zulässig (Merge-Baum = PR-Head-Baum)"
  overstates what is enforced.

  Why this is not MAJOR:
  - It needs a hand-crafted `commit-tree` merge pushed to main outside the documented
    `gh pr merge` flow.
  - Protected history, frozen paths, scope and modes stay intact; every commit on the merged
    side is still checked.
  - The five historical `request` outputs are unaffected.
  - Harness modification is already permitted under the documented F4 policy.

  It should still be fixed before the first product PR merge.
- Recommended fix: in `execution_history`, for two-parent commits add
  `ancestor(parents[0], parents[1])` next to the existing first-parent check. In a scratch copy
  this rejects A1-A3 and keeps normal `--no-ff` PR merges and linear commits valid. Add tests
  that reject:
  - a merge whose second parent is an ancestor of the first;
  - a theirs-tree merge of a stale branch that drops a main-only `tests/` file.

### WS-E01-TR-PR6-02-F2

- Severity: MINOR
- Status: OPEN
- Description: The authorization-integrity wiring in `request` history is not covered by
  tests. Removing `execution_authorization_integrity(...)` from `epic_delta_history` (M08)
  passes `tests.test_epic_execution`. Only the `check()` path (M15) and the function itself are
  tested. The guard works today: a forged authorization added on a branch from `714b440` is
  rejected by `request` with `broad execution authorization hash`. But `request` at a non-HEAD
  SHA (feature acceptance) relies on this call alone. Earlier finding F2 listed this case
  explicitly (M08), so the commit message claim "targeted tests cover each previously
  unexercised guard" is not fully accurate.
- Recommended fix: add a fixture that commits authorization bytes differing from the pin on a
  branch from `714b440`. Assert that `request(head, EPIC_CORR2_SUBJECT)` and a feature request
  raise `broad execution authorization hash`. Optionally add a test for the degenerate-merge
  guard (M17).

### WS-E01-TR-PR6-02-F3

- Severity: NIT_OR_SUGGESTION
- Status: OPEN
- Description: The changed-path enumeration in `execution_history` uses porcelain
  `git diff --name-status --no-renames`, which honors user and system git configuration. With
  `diff.ignoreSubmodules=all`, a gitlink addition is hidden, so the mode guard never sees it.
  Probe D1 is accepted by request/check/history. `check()` cannot see gitlinks through
  `files()`. CI runs with default configuration and rejects the gitlink (D0), so the
  authoritative gate fails closed, but local reviewer or agent results can differ from CI.
- Recommended fix: use plumbing with fixed options, as F8 originally suggested:
  `git diff-tree -r --no-renames --no-ext-diff -z --name-status <parent> <rev>`, parsed on NUL.
  Also check modes in `check()` with `git ls-files -s` (reject 120000/160000 under scope).

### WS-E01-TR-PR6-02-F4

- Severity: NIT_OR_SUGGESTION
- Status: OPEN
- Description: This is the carried-over residual of earlier F3. For feature requests, `request`
  accepts the exclusion set with strip+casefold comparison. `self_verdict` then requires an
  exact `req["implementer"] in excluded`. For example, implementer `LEAD` with exclusions
  `["lead"]` or `["LEAD "]` passes `request`, after which every result fails
  `review exclusion set`. This fails closed but is inconsistent.
- Recommended fix: use the same strip+casefold normalization for the implementer-membership
  check in `self_verdict`, or require an exact match in `request`, and add a test.

## Other observations (no finding)

- Authorization record:
  - `RECORDED_BY` names the lead coding agent, and `RECORDING_LIMITATION` states that the
    record is a structured transcription, not byte-identical, of a decision that predates the
    rebinding.
  - It carries `SELF_PASS_ALLOWED: false`, `RELEASE_OR_PRODUCTION_AUTHORIZED: false`,
    `NEXT_EPIC_SELECTION_BY_AGENT: false` and `STOP_AT: EPIC_CONVERGED`, and it creates no
    verdict or acceptance.
  - Its `HARD_LIMITS` and `STOP_AND_REPORT_ON` are consistent with AGENTS.md and the routed
    Product Truth.
  - This reviewer cannot verify the verbatim excerpts against the original chat.
- Routers: `engineering.md` first lists the frozen subtrees and later states "Ganz `foundation/`
  ist eingefroren außer context.md/engineering.md". This is redundant but consistent with the
  code. Its "up to date" merge sentence is inaccurate as described in F1.
- `features/` paths are not `protected()`, so feature subjects and evidence can be edited or
  deleted after acceptance. Acceptance binds to an exact SHA, so the accepted bytes stay in Git
  history. Before the first feature acceptance, consider whether accepted feature subjects
  should become append-only (as `epics/<ID>/` is) or versioned.
- Commits on side branches are covered, because `rev-list 714b440..head` includes every commit
  not reachable from the integration merge. Orphan parents fail the single-parent requirement.

TECHNICAL_REVIEW_OUTCOME: NO_OPEN_CRITICAL_BLOCKING_MAJOR
