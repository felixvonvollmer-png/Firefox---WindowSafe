# WindowSafe — WS-E01-F01 target-environment qualification handoff

RUN_ID: WS-E01-F01-TARGET-QUAL-20260919-01
AUTHORIZATION_ID: WS-EA-20260919-08
FEATURE_ID: WS-E01-F01
PR: #3
BRANCH: feature/ws-e01-f01-qualification
START_HEAD: 0f83be2550f34698fe95da4df88b5eb918649973
START_TREE: 2db2d133b8aeb43f8ce7444d6192e55aa2d49c12
MAIN: 3bdd7439c221b8f8c83e7374c8bb29898891a4fd
LOCKFILE_SHA256: 1d6f6b41f6a87d1890695247e6610f60199518b22e87f12f1ee1002661563834
RISK_FLOOR: ELEVATED
TARGET_SUCCESS: WS-E01-F01_READY_FOR_INDEPENDENT_TECHNICAL_REVIEW
MERGE_AUTHORIZED: NO

## Start preflight
Verify repo ID 1374094477, PR #3 open/Draft/unmerged, exact branch/head/tree,
remote main, clean worktree/index, exact lockfile hash and current state
`WS-E01-F01_PARTIAL_QUALIFICATION__TARGET_ENVIRONMENT_REQUIRED` with exactly:
WINDOWS_DESKTOP, SPECIAL_NATIVE_GUI_CASES, TARGET_EQUIVALENT_RESTART,
MEASUREMENT_FINAL_ATTRIBUTION. Any drift => STOP before mutation.

## Agent/host
Still a Coding-Agent qualification role, not a reviewer. Same F01 agent is preferred if it has
direct target-Desktop access. A fresh Windows-capable Coding-Agent is allowed; only one branch
writer at a time and it must reconstruct context from Git.

## Windows Desktop
Use real interactive Windows Desktop, official Mozilla Firefox 156.0 Stable, new disposable
synthetic profile, localhost pages, qualification probes only. Do not install/change normal
Firefox/defaults/profile/global settings. Do not kill existing Firefox. Prove owned PID/profile.

Execute relevant matrix rows on Windows rather than inheriting Ubuntu:
normal/popup/event page; private exclusion; hidden tabs; containers/collisions; native groups;
actual split-view observation/events where creatable; reader/discarded/pinned/muted/active/
container/group combinations; privileged URLs; geometry/state; session values/startup signals;
special windows. Missing capability stays OPEN.

## Special GUI cases on both OSes
Close only by actual Desktop evidence or an explicitly documented safe unsupported boundary:
DevTools, Web-App/PWA-like case if present, Picture-in-Picture, manual private-window exclusion,
actual Split View membership/events, remaining interaction cases. Ubuntu evidence still required
where the existing matrix says OPEN. Windows is not a substitute.

## Target-equivalent restart
Firefox 157 Developer evidence is insufficient. Attempt persistent restart with a verifiably
official Mozilla unbranded Release-equivalent Firefox 156 build. Fixed synthetic add-on ID;
disposable profile; signature pref only inside that profile; no AMO/signing; bind exact build and
artifact/binary hashes; graceful exit/relaunch; observe real onStartup/marker persistence.
If a trustworthy exact 156-equivalent build cannot be located, keep the gate OPEN.

## Measurement attribution
This is method/instrument qualification only, not F05 threshold acceptance.

Windows: qualify Job Object-based owned-Firefox accounting with fail-closed child containment,
aggregate lifetime CPU and I/O, per-process identity diagnostics, explicit memory semantics and
breakaway/nesting failure detection. Sampled-only CPU is not an equivalent fallback.

Memory/peak: qualify a reproducible synthetic-probe method separating addon-attributable
JS/DOM/cache from total/shared Firefox memory, pair with OS A/B counters and Firefox-native
memory/profiler evidence where available, document peak coverage and uncertainty. If hard peak
attribution cannot be demonstrated, keep MEASUREMENT_FINAL_ATTRIBUTION OPEN.

## Mutation
Allowed: qualification-only scripts/probes, deterministic tests, additive evidence, mutable
F01 state. Keep package.json/lock/toolchain unchanged. Keep Product/Foundation/Epic/review
originals and prior F01 evidence append-only. Minimal generic guard/CI/router changes only if
strictly required and without weakening.

## Verification
Run all relevant local tests, Foundation check/build/history/schema/request, unchanged npm audit,
deterministic toolchain checks, git diff --check, changed-path review, then push same branch and
require exact-head push/PR CI. Windows Server CI remains static only.

## End state
If all four gates close on both target Desktop OSes:
- state -> WS-E01-F01_READY_FOR_INDEPENDENT_TECHNICAL_REVIEW
- add compact technical-review handoff/evidence inventory
- update PR #3 body to truthful current status
- keep Draft/unmerged
- STOP before independent review.

If anything remains:
- preserve partial evidence
- remain PARTIAL or truthful BLOCKED
- add exact continuation record
- STOP.

Explicitly excluded: final V6 migration, F02/product implementation, real user data/profile,
Feature Acceptance, independent verdict, merge/rebase/squash/auto-merge/force push,
signing/release/production.
