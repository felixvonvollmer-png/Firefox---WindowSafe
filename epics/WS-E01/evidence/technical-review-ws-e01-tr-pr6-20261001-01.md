# WS-E01-TR-PR6-20261001-01: Independent Technical Review of PR #6

- Reviewer identity: CLAUDE_SUBAGENT_INDEPENDENT_TECHNICAL_REVIEWER_WS_E01_TR_PR6_20261001_01
- Review type: technical review (Foundation 2 §30, ELEVATED risk increment); not a feature acceptance, not an epic verdict
- Repository: felixvonvollmer-png/Firefox---WindowSafe, PR #6, branch `exec/ws-e01-broad-authorization`
- Reviewed head SHA: `03ae327da2e564412cbd812a4efdc2c96a89d2ba`
- Base (main): `714b440c26167f6411420fbbda4be69deb2e9670`
- Reviewed diff: `git diff 714b440c26167f6411420fbbda4be69deb2e9670 03ae327da2e564412cbd812a4efdc2c96a89d2ba` (10 files, +393/-13, single commit `03ae327`)
- Date: 2026-10-01

## Independence statement

I am a freshly started subagent with no prior context on this change. I did not author,
materialize or contribute to PR #6 or to any WS-E01 preparation, correction, rebinding or
authorization artifact. There was no expected outcome. I worked read-only on the detached
worktree `/home/felix/projekte/windowsafe-review-pr6`; all tests, probes and mutations ran in
disposable clones under the session scratchpad. No pushes, no gh mutations, no browser, no
real profiles.

Worktree hygiene: before and after the review `git rev-parse HEAD` was
`03ae327da2e564412cbd812a4efdc2c96a89d2ba` and `git status --porcelain --ignored` was empty.
CLI gates in the worktree ran with `PYTHONDONTWRITEBYTECODE=1`; no `__pycache__` was
created there, so nothing had to be removed (verified: 0 `__pycache__` directories).

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

Historical request equivalence: the same five `request` commands were run with the base
tool in a clean clone at `714b440` (all exit 0, base `check` exit 0). Outputs are
byte-identical between base and head (`cmp`):

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
| `python3 -m unittest discover -s tests` (181 tests, 890 s) | 0 |
| `python3 -m unittest tests.test_epic_execution` (7 tests, baseline before mutations) | 0 |

Pinned hashes verified: `broad-execution-authorization.json` SHA-256
`cced59563b38d5356097ecc2f1efe3da385897023b8ac323882c0d3c5761db6d` equals
`EPIC_EXECUTION_AUTH_SHA`; `rebinding.json` SHA-256
`aacc8cce51e0ef7caf29d8d85bc3b5a2df7c8a628d255e6edd47a50d8796528f` equals
`REQUIRED_EPIC_REBINDING.sha256` in the record.

## Exact-head CI

`gh run list --commit 03ae327da2e564412cbd812a4efdc2c96a89d2ba` (read-only), both runs
completed, logs read with `gh run view <id> --log`:

| Run ID | Event | Workflow | Conclusion | Notes |
| --- | --- | --- | --- | --- |
| 36885971134 | pull_request | Foundation | success | checkout of exact `03ae327…`; CHECK OK; Ran 181 tests OK; SCHEMA-PREFLIGHT OK; 8x VALIDATE-RESULT OK; BUILD OK (inventory `45158a0622df4e2a6519cd631168c69869e053c9fa96188507c4de46a2f3df7f`); HISTORY OK; all steps success |
| 36885964336 | push | Foundation | success | same steps, same inventory SHA-256, Ran 181 tests OK; all steps success |

## Adversarial probes (disposable clones from the reviewed head)

| Probe | Result |
| --- | --- |
| Octopus merge after the integration merge | REJECTED (`execution octopus merge prohibited`) |
| Merge back to an older tree (`eeddbcf`, `714b440`) | REJECTED |
| Side branch based on old main `1cb82c9` merged into main | REJECTED |
| Merge of main into a feature branch ("update branch"), and that branch merged into main | REJECTED (`execution merge must be up to date`) |
| Simple up-to-date `--no-ff` PR merge; `history(714b440)` | ACCEPTED (expected) |
| Degenerate merge with both parents equal to HEAD | ACCEPTED (no content change) |
| Rename `reviews/review-contract.json` -> `addon/review-contract.json` | `git diff --name-only` lists only `addon/review-contract.json`; rejected later only because the contract is missing |
| Overwrite `foundation/subject.json` (historical foundation subject) | ACCEPTED by `request`, `check`, `history`; `request --subject foundation/subject.json` output changes |
| Delete `tests/test_epic_rebinding.py` | ACCEPTED by `request`, `check`, `history` |
| Modify `tools/foundation.py` to disable the frozen check | ACCEPTED |
| Symlink `addon/link.js` | history ACCEPTED; `check()` REJECTED at head (`symlink prohibited`) |
| Gitlink (mode 160000) at `addon/sub.js` | ACCEPTED by `request`, `check`, `history` |
| Feature subject with `"contributors": "WORKER"` and exclusion list `["LEAD","W","O","R","K","E"]` | request ACCEPTED; `self_verdict("WORKER")` is False (worker could PASS) |
| Feature subject with implementer `LEAD`, exclusions `["lead"]` | request ACCEPTED; `self_verdict` raises for every reviewer (fail-closed) |
| Feature subject `WS-E02-F01` | REJECTED |

## Mutation testing (scope: `tests.test_epic_execution` only, not the full suite)

Each mutation was applied to `tools/foundation.py` in its own scratch clone.

| Mutation | `test_epic_execution` |
| --- | --- |
| M01 remove frozen-prefix check | killed |
| M02 remove `scope(path)` in `execution_history` | killed |
| M03 remove up-to-date tree equality | killed |
| M04 remove per-parent `check_history_maps` | killed |
| M05 remove octopus `require` | SURVIVED (backstopped by `history()` "authorized epic normal merge required", not by `request`) |
| M06 remove `ancestor(EPIC_INTEGRATION_MERGE, parents[0])` | SURVIVED |
| M07 remove feature exclusion subset | killed |
| M08 remove `execution_authorization_integrity` in `epic_delta_history` | SURVIVED |
| M09 remove `EPIC_INTEGRATION_MERGE in merges` | SURVIVED |
| M10 remove `delta_history(sha)` in feature request | SURVIVED |
| M11 remove feature ID/phase `require` in request | SURVIVED |
| M12 remove manifest guard in `scope()` | SURVIVED |
| M13 allow `node_modules` | killed |
| M14 drop `review_excluded_identities` transport for features | killed |
| M15 remove `execution_authorization_integrity` in `check()` | SURVIVED |
| M16 enter execution phase without the authorization file | killed |

## Findings

### WS-E01-TR-PR6-F1

- Severity: MAJOR
- Status: OPEN
- Description: The execution phase allows overwriting the historical foundation subject
  `foundation/subject.json`. It matches `scope()` (`foundation/[a-z-]+\.(md|json)`), is not
  in `EXECUTION_FROZEN_PREFIXES` and not in `protected()`. A single-parent commit after the
  integration merge that changes its `implementer` is accepted by `request`, `check` and
  `history`, and `request --sha HEAD --subject foundation/subject.json` then returns a
  different request. Before this PR every post-merge commit was rejected. Earlier phases
  froze this file through exact allowlists and the explicit "historical foundation subject
  drift" check in `delta_history`. This regresses the record's own hard limit ("historical
  originals append-only"), AGENTS.md ("Kein Überschreiben historischer … Subjects") and the
  claim that no governance is weakened. Other historical, unprotected foundation documents
  (for example `foundation/reviewer-environment.md`) are equally open.
- Recommended fix: freeze `foundation/subject.json` during execution. Add it to
  `EXECUTION_FROZEN_PREFIXES` or `protected()`, and preferably freeze every pre-existing
  historical `foundation/*.json` / record file except the routers that are meant to change.
  Add a test that rejects an execution commit modifying `foundation/subject.json`, both
  directly and through a merge.

### WS-E01-TR-PR6-F2

- Severity: MINOR
- Status: OPEN
- Description: `tests/test_epic_execution.py` does not kill 8 of 16 guard-removal mutations
  (M05, M06, M08, M09, M10, M11, M12, M15 above). Missing tests:
  - octopus merge (M05);
  - merge whose first parent does not descend from `714b440` (M06);
  - authorization wiring in history and `check()`: a fixture whose committed authorization
    bytes differ from the pin must fail `request`/`check` (M08, M15);
  - the integration-merge requirement (M09);
  - a feature request on a head with invalid execution history, e.g. a frozen-path commit
    (M10);
  - feature subject `WS-E01-F06` or one without the authorization, asserting the specific
    message (M11). The current check uses `assertRaises(f.Invalid)` on a head that already
    fails for other reasons;
  - a scoped non-product `manifest.json`, e.g. `foundation/manifest.json` or
    `features/WS-E01-F01/manifest.json` (M12). The root `manifest.json` case is already
    rejected by the scope regex.

  The guards work today (probes), but the harness is editable during execution (F4), so
  these tests are the regression net.
- Recommended fix: add the listed negative tests with specific error-message assertions.

### WS-E01-TR-PR6-F3

- Severity: MINOR
- Status: OPEN
- Description: Feature author exclusion has a type-confusion gap. `request()` expands
  `*s.get("contributors", [])` without requiring a list of strings. With
  `"contributors": "WORKER"` and a crafted exclusion list of single characters, the request
  is accepted and `self_verdict("WORKER")` is False, so the worker could issue a PASS. The
  natural mistake (string contributor plus natural exclusion list) fails closed, so
  exploiting this needs a deliberately crafted subject. Related NIT: `self_verdict` requires
  exact `req["implementer"] in excluded`, while `request` compares case-folded values. A
  case variant passes `request` and then makes every result fail (fail-closed but
  inconsistent).
- Recommended fix: require `contributors` (when present) to be a list of non-empty strings
  and `materializer` to be a string. Make the implementer-membership check in `self_verdict`
  use the same strip+casefold normalization. Add tests.

### WS-E01-TR-PR6-F4

- Severity: MINOR
- Status: OPEN
- Description: During execution the gate harness and its regression tests can change
  freely. `tools/*.py`, `tests/*.py` and `.github/workflows/foundation.yml` are in
  `scope()` and neither frozen nor protected. Probes: a commit disabling the frozen check in
  `tools/foundation.py`, and a commit deleting `tests/test_epic_rebinding.py`, are both
  accepted by `request`, `check` and `history`. CI runs the PR's own harness. The pattern
  existed before (`EPIC_DELTA_SUPPORT` included `tools/foundation.py`), but the execution
  phase is long-running and autonomous, so mechanically nothing prevents a later commit from
  weakening the gates. The hard limit "No weakening of … gates" is enforced only by review.
- Recommended fix: during execution, freeze `tools/foundation.py`, existing `tests/test_*.py`
  and the workflow, or require each harness/test/workflow diff to carry its own independent
  technical review reference checked by the harness. At minimum, document in
  `foundation/engineering.md` that harness diffs need separate review, and forbid deleting
  existing test modules (append-only for `tests/`).

### WS-E01-TR-PR6-F5

- Severity: MINOR
- Status: OPEN
- Description: The "up to date" merge rule is fail-closed but has a sharp operational edge.
  A GitHub "Update branch" merge (main into the feature branch) is rejected. More
  importantly, if a PR that is not up to date is merged on GitHub, the resulting merge commit
  on main permanently fails `request`/`history` for every later head. History rewrite is
  prohibited, so recovery would need a harness change. Nothing in the PR documents or
  enforces a branch-protection "require branches to be up to date" setting or a
  rebase-free update workflow (force-push is prohibited).
- Recommended fix: document the required workflow in `foundation/engineering.md` (new branch
  from current main plus cherry-pick, or squash merge, which yields a scoped single-parent
  commit), and enable or record the GitHub branch-protection "require up to date" setting.
  Consider an explicit, user-authorized recovery path instead of an ad hoc harness edit.

### WS-E01-TR-PR6-F6

- Severity: MINOR
- Status: OPEN
- Description: Git object modes are not checked. A gitlink (mode 160000) at `addon/sub.js`
  is accepted by `request`, `check` and `history`. `files()` does not see it, and the
  `ls-files` scope check only matches the name. Symlinks are rejected at head by `check()`
  but accepted in intermediate execution commits. This contradicts "Produktquellen … nur
  Textdateien".
- Recommended fix: in `execution_history` (and in `check()` via `git ls-files -s`), require
  mode `100644` (or `100644`/`100755` where justified) for every changed or tracked path
  under `addon/`, `qualification/` and `features/`. Add tests for gitlink and symlink.

### WS-E01-TR-PR6-F7

- Severity: MINOR
- Status: OPEN
- Description: The routers are inconsistent with the new authorization:
  - `README.md` lines 22-23 still say F01 "gestoppt und wird nicht fortgesetzt. Kein
    Produktcode oder Feature Acceptance."
  - `foundation/context.md` line 50 still says "Danach unabhängiger Rereview, Rebinding und
    separate breite WS-E01-Autorisierung." directly after "Aktuell: autonome
    WS-E01-Ausführung".
  - `AGENTS.md` says "F01 ist gestoppt." immediately followed by "Ab WS-EA-20261001-03 wird
    F01 … fortgesetzt", and still scopes workers/subagents/reviewers under WS-EA-20260930-01
    instead of WS-EA-20261001-03.
  - `epics/README.md` line 41 still says F01 "gestoppt".
- Recommended fix: mark these sentences as historical or replace them with the current
  state, and route worker scope to WS-EA-20261001-03.

### WS-E01-TR-PR6-F8

- Severity: NIT_OR_SUGGESTION
- Status: OPEN
- Description: `execution_history` uses porcelain `git diff --name-only`, which by default
  (`diff.renames`) reports only the destination of a rename. Renaming a frozen file shows
  only the new path, so the frozen-prefix check never sees the source. This is currently
  backstopped: frozen paths except `reviews/review-contract.json` are `protected()`, and a
  missing contract fails `request`. The output also depends on user git config. Also:
  `reviews/review-contract.json` is frozen only for single-parent commits (not
  `protected()`); reverting it through a merge was shown infeasible with the current history
  but relies on that coincidence. A degenerate merge with identical parents is accepted.
- Recommended fix: use plumbing with fixed options, e.g.
  `git diff-tree -r --no-renames --no-ext-diff -z --name-only <parent> <rev>`, and parse NUL
  separators. Add `reviews/review-contract.json` to `protected()` or check frozen prefixes
  for merges against `parents[0]`. Reject merges whose parents are identical.

## Other observations (no finding)

- The authorization record is honestly labeled: `RECORDED_BY` names the lead coding agent,
  and `RECORDING_LIMITATION` states that it is a structured transcription, not byte-identical,
  and that the decision predates the rebinding. It carries `SELF_PASS_ALLOWED: false`,
  `RELEASE_OR_PRODUCTION_AUTHORIZED: false` and `NEXT_EPIC_SELECTION_BY_AGENT: false`, and it
  creates no verdict or acceptance. Its `HARD_LIMITS` are consistent with Product Truth as
  routed. The verbatim excerpts cannot be verified against the original chat by this
  reviewer.
- `execution_authorization_integrity` checks the hash pin, the exact rebinding hash, the
  integration merge, the feature direction, STOP_AT and the false flags, and that the
  rebinding is READY_FOR_AGENT.
- Commits on side branches are covered, because `rev-list 714b440..head` includes every
  commit not reachable from the integration merge. Path traversal, backslashes, colons,
  `..`, case variants (`Foundation/…`) and dot-prefixed names are rejected by `safe_path`
  and the case-sensitive regexes. C-quoted non-ASCII paths fail `scope()` (fail-closed).
- CI timeout 20 -> 45 minutes is consistent with the measured suite duration (831-1101 s in
  CI).

TECHNICAL_REVIEW_OUTCOME: CHANGES_REQUIRED
