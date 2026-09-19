# WindowSafe – WS-E01-F01 execution handoff

```text
RUN_ID: WS-E01-F01-START-20260919-01
AUTHORIZATION_ID: WS-EA-20260919-06
FEATURE_ID: WS-E01-F01
EPIC_ID: WS-E01
START_BASELINE_SHA: 3bdd7439c221b8f8c83e7374c8bb29898891a4fd
START_BASELINE_TREE: 034b79c80d9e1e6ae2b57268e6dbaf94bfb31b58
TARGET_BRANCH: feature/ws-e01-f01-qualification
TARGET_END_STATE: WS-E01-F01_READY_FOR_INDEPENDENT_TECHNICAL_REVIEW
                    OR explicit partial/blocking stop state
MERGE_AUTHORIZED: NO
FEATURE_ACCEPTANCE_SELF_VERDICT: PROHIBITED
WS-E01-F02_START_AUTHORIZED: NO
```

## 0. First principle

This is the mandatory preimplementation qualification feature. It may build **qualification-only
test tooling/probes**, but it must not build WindowSafe's real capture/recovery/storage/UI/backup
features.

## 1. Git preflight

Before mutation:
- verify repo root/origin and GitHub repo ID 1374094477/public;
- remote main must equal `3bdd7439c221b8f8c83e7374c8bb29898891a4fd`;
- expected tree `034b79c80d9e1e6ae2b57268e6dbaf94bfb31b58`;
- fetch read-only;
- if local main is behind but clean and an ancestor of exact `origin/main`, a local-only
  fast-forward to `3bdd7439c221b8f8c83e7374c8bb29898891a4fd` is authorized;
- if local main diverged, has local-only commits, or worktree/index/untracked state risks foreign
  work: STOP;
- branch `feature/ws-e01-f01-qualification` must be absent or exactly attributable to this run; never overwrite foreign
  branch work.

Create the branch from exact `3bdd7439c221b8f8c83e7374c8bb29898891a4fd`.

## 2. Materialize supplied feature-start artifacts exactly

Under `features/WS-E01-F01/`:
- `start.json`
- `qualification-plan.md`
- `test-envelope.md`
- `acceptance-criteria.md`
- `evidence/execution-authorization.json`
- `evidence/research-start.md`

Verify package SHA256SUMS before copying. Do not semantically rewrite Project-LLM-supplied files.

## 3. JIT generic feature lifecycle support

The repository already defines V3 `FEATURE_ACCEPTANCE_REVIEW` request semantics but does not yet
materialize a feature channel.

Add the **minimum generic** support required for this feature:
- narrowly allow `features/<valid FEATURE_ID>/` lifecycle/evidence paths;
- keep arbitrary product code paths closed until explicitly authorized by a later feature;
- allow a future `features/<FEATURE_ID>/subject.json` only at
  `READY_FOR_ACCEPTANCE_REVIEW`;
- require exact start baseline, current accepted Epic binding, Product/Foundation/Epic
  traceability, sufficient execution authorization and evidence paths;
- prevent the implementer from marking its own independent Feature Acceptance PASS;
- preserve review-history cardinality and all old canonical results;
- add fail-closed regression tests.

Do not create a dummy acceptance result.

## 4. Toolchain work

Research and qualify the current candidates from `evidence/research-start.md`.
A reasonable initial hypothesis is:
- Node 24.21.0 LTS;
- web-ext 10.6.0;
- TypeScript 7.0.2.

But the agent owns the evidence-based reversible decision.

Rules:
- user/workspace scoped installs only; no sudo/global install;
- exact versions and lockfile;
- inspect package provenance/licenses/dependency tree and relevant security advisories;
- no unnecessary bundler/framework;
- choose a type strategy only after comparing it with target APIs;
- preserve a compact decision record with alternatives rejected and why.

## 5. Qualification probes

Create qualification-only code under a clearly named location such as
`qualification/ws-e01-f01/`; no product `src/` implementation yet.

At minimum produce:
- capability probe extension;
- optional separate helper extension(s) to synthesize hidden-tab or other states;
- synthetic localhost pages/data;
- deterministic launcher/probe scripts;
- evidence collectors;
- Windows and Ubuntu instructions/scripts.

The capability probe must never access real profile data and must report only synthetic test state.

## 6. Runtime evidence

Execute the authorized disposable-profile probes on every target OS actually available.

Record exact:
- OS/build;
- Firefox binary/version/build ID/hash where feasible;
- probe package hash;
- profile path/class (disposable);
- commands;
- results;
- cleanup.

Do not fabricate Windows evidence from Ubuntu or vice versa.

If Windows is unavailable, finish portable Windows tooling/handoff and stop PARTIAL.

## 7. Measurement method

Bind the final F05 measurement methodology now and prove the instrumentation in small dry-runs.
Do not run full product benchmarks or claim threshold PASS.

Method must satisfy Technical Foundation §9.1/§9.3 exactly, including five paired runs per
profile/OS in the eventual acceptance measurement.

## 8. Feature evidence / end state

Maintain cumulative evidence matching Foundation 2 §31 as applicable:
- feature/start baseline;
- Product/Foundation/Epic refs;
- changeset refs;
- acceptance criteria;
- verification;
- current risk;
- required technical review;
- runtime evidence;
- open findings;
- material deviations;
- known follow-ups.

If BOTH target OSes and all F01 gates converge:
- create the feature candidate/evidence necessary for technical review;
- status `WS-E01-F01_READY_FOR_INDEPENDENT_TECHNICAL_REVIEW`;
- keep branch/PR unmerged;
- do NOT issue `FEATURE_ACCEPTANCE_REVIEW` yet;
- STOP.

If not:
- preserve truthful partial evidence;
- generate a compact continuation package for the missing environment/decision;
- STOP at the corresponding explicit state.

## 9. CI and PR

A Draft PR against main is allowed.
CI may run static/toolchain/qualification model tests that do not require GUI/native OS evidence.
Do not label missing Windows/native GUI evidence as CI PASS.

Existing Foundation checks remain green.

## 10. Explicit STOP

No merge.
No auto-merge.
No F02.
No product implementation.
No user profile.
No release/signing/AMO/production.
