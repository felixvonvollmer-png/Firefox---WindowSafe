# WindowSafe — F01 Windows Desktop continuation

```text
RUN_ID: WS-E01-F01-WIN-20260924-01
AUTHORIZATION: WS-EA-20260919-08
WORKSPACE: D:\Projekt\WindowSafe-F01-Windows
BRANCH: feature/ws-e01-f01-qualification
START_HEAD: 7b52f6655e4478caa4864801b24877d22c33fa83
START_TREE: b5107a356aa5f86645a110a029adb2b11072af1f
MAIN: 3bdd7439c221b8f8c83e7374c8bb29898891a4fd
LOCKFILE_SHA256: 1d6f6b41f6a87d1890695247e6610f60199518b22e87f12f1ee1002661563834
PR: #3 Draft/unmerged
ROLE: CODING_AGENT_QUALIFICATION__NOT_REVIEWER
MERGE_AUTHORIZED: NO
```

This is a Windows-host continuation of the already authorized WS-E01-F01 target qualification.
It does not expand WS-EA-20260919-08.

## Preflight

Before mutation or browser launch verify repo/root/origin/repo ID 1374094477, exact branch/head/tree,
origin/main and main, clean worktree/index, exact lock hash, PR #3 Draft/unmerged, and current
`WS-E01-F01_PARTIAL_QUALIFICATION__TARGET_ENVIRONMENT_REQUIRED` state with the four open gates:
WINDOWS_DESKTOP, SPECIAL_NATIVE_GUI_CASES, TARGET_EQUIVALENT_RESTART,
MEASUREMENT_FINAL_ATTRIBUTION.

Read `features/WS-E01-F01/evidence/target-continuation.md` and current state/evidence from Git.
Collect current Windows identity again. Drift => STOP.

## Browser isolation

The installed normal Firefox is 156.0.1 at
`C:\Program Files\Mozilla Firefox\firefox.exe`. Treat this as context only.

Primary F01 evidence must use workspace-local verified official Mozilla artifacts:
- exact Firefox 156.0 Stable target build;
- the repository-located official win64 add-on-devel/unbranded release-equivalent 156 artifact
  from `features/WS-E01-F01/evidence/target-windows-build-locator.json`.

The locator currently binds:
- source revision `a80bd15ddee3b4bf3679aeba340e9d2db933c467`
- build ID `20260909172920`
- task `OSCRr3diR7SXwQr0i6Y1dQ`
- artifact `public/build/target.zip`
- advertised SHA-256 `30a3444f7416479ec78d03bc48ad63f0a669aa91b40481943c7de426ba8fa25f`

Re-fetch Mozilla metadata, verify archive hash and full extracted installation before execution.
Do not use third-party mirrors. Never open the user's normal Firefox profile. Never modify system
Firefox/defaults. Never kill unrelated Firefox processes. Every probe uses a new disposable profile
and localhost/synthetic data only.

## Windows Desktop matrix

Execute independently on the real interactive Windows Desktop:
- event-page startup/background behavior;
- normal/popup;
- native private-window exclusion;
- hidden tabs with TEST_ONLY helper;
- containers, missing/collision/cross-profile semantics;
- native groups/group-ID limitations;
- actual Split View membership/events if available;
- reader/discarded/pinned/muted/active/container/group combinations;
- privileged/non-openable URLs;
- geometry/state/display cases;
- session values/startup signals;
- native DevTools/PiP and WebApp/PWA-like cases where exposed.

Classify evidence explicitly as OBSERVED, NOT_AVAILABLE,
NOT_REPRODUCIBLE_WITH_DOCUMENTED_TARGET_CAPABILITY or OPEN.

## Target-equivalent restart

Using only the verified official Windows unbranded/release-equivalent 156 artifact:
- fixed synthetic add-on ID;
- disposable profile;
- signature pref only inside that profile if required;
- persistent install;
- graceful quit/relaunch;
- real `onStartup`;
- marker 1 -> 2 and session-hint persistence;
- exact artifact/build/profile/PID evidence;
- cleanup of owned processes/profile only.

No AMO/signing/account use.

## Windows Job Object accounting

Implement/qualify without new package dependencies:
- create/assign owned Firefox before relevant child workload;
- non-breakaway policy where valid;
- prove descendant containment or fail closed;
- PID + creation identity diagnostics;
- lifetime aggregate user+kernel CPU;
- aggregate I/O accounting;
- explicit memory/private/working-set semantics;
- detect nesting/breakaway/assignment failure;
- short-lived child and cleanup/failure tests.

Use Win32 APIs through standard-library `ctypes` or equivalent built-in facilities.
Sampled-only CPU is not an equivalent fallback.

## Memory / hard-peak attribution

Pair controlled A/B OS counters with Firefox-native memory/profiler evidence. Separate explicit
add-on JS/DOM/cache from whole-browser/shared/native residual. Qualify peak coverage rather than
assuming point samples capture hard peaks. Record instrumentation overhead and uncertainty.
Do not run or claim F05 performance acceptance. If hard peak/add-on attribution remains unproven,
keep MEASUREMENT_FINAL_ATTRIBUTION OPEN.

## Cross-OS closure

Compare Windows results with existing Ubuntu evidence. Close a global gate only when all applicable
target-OS requirements are evidenced or an explicit safe Product-compatible unsupported boundary
is justified. If Ubuntu still has an applicable open subcase, remain PARTIAL.

## Mutations

Allowed under WS-EA-08: qualification-only scripts/tests, additive Windows/cross-OS evidence,
mutable F01 state/current report, minimal current routing/PR text.

Do not change package.json/package-lock/dependencies/toolchain versions, Product/Foundation inputs,
Epic subject/binding, historical review results or prior F01 evidence. No final V6 migration.

## Verification

Require Python 3.14.4, relevant tests, Foundation check/build/history/schema/request, unchanged
live npm audit, unchanged typecheck/lint/toolchain checks, Windows qualification regressions,
`git diff --check`, exact changed-path review, exact-head push and PR CI with logs inspected.

Windows Server CI remains static evidence only.

## End state

If all four global gates close:
- state -> `WS-E01-F01_READY_FOR_INDEPENDENT_TECHNICAL_REVIEW`
- add technical-review handoff/evidence inventory
- update PR #3 body truthfully
- keep Draft/unmerged
- STOP.

If any gate remains:
- preserve additive evidence
- remain PARTIAL or truthful BLOCKED
- produce exact continuation evidence
- STOP.

No independent verdict, Feature Acceptance, merge, F02, V6 migration, product implementation,
signing/release or Production.
