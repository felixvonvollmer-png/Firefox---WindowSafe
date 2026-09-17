# WindowSafe – V6 Project Foundation Coding-Agent Start Handoff

```text
DOCUMENT_TYPE: COMPACT_PROJECT_FOUNDATION_AGENT_START_HANDOFF
HANDOFF_ID: WS-PFBOOT-20260917-01
DATE: 2026-09-17
PROJECT: WindowSafe
TARGET_REPOSITORY: felixvonvollmer-png/Firefox---WindowSafe
TARGET_REPOSITORY_ID: 1374094477
MODE: V6_GREENFIELD_PROJECT_FOUNDATION_BOOTSTRAP_ONLY
END_STATE: PROJECT_FOUNDATION_READY_FOR_REVIEW
NORMAL_PRODUCT_FEATURES_IN_THIS_RUN: PROHIBITED
```

## 1. Authority and exact inputs

User execution authorization:
`WindowSafe_Execution_Authorization_WS-EA-20260917-01.json@sha256:1bf8db7bf47c46806951e31801747b37b4d37653cb46aa2ee8b2ef5bd21e79f8`

Load and verify these exact inputs from this package:

- Product Definition: `WindowSafe_Product_Definition_WS-PD-20260917-01.md@sha256:fff235b7591f483b9b31c945911a6b5950d29fac931b9136438ae5586c756900`
- Product Approval: `WindowSafe_Approval_Record_WS-PD-20260917-01.json@sha256:a655d1fb0a594997e1f6da00c7e8a36bb6c5807ac844ce9fbf04ccb7d1afd4a5`
- Technical Foundation Preparation r6: `WindowSafe_Technical_Foundation_WS-TFP-20260917-01_r6.md@sha256:c461c45c5bd20f12dcffb400acd6f7d5c0f0de0a75616eef3eb1d78dd175dcb6`
- Technical Decision Record: `WindowSafe_Technical_Decisions_WS-TD-20260917-03.json@sha256:36bc4954a4aa9046be381a3095bc3f3574cb6ef2527e7bd060be15eda925f2e3`
- T05-R2 decision subject: `WindowSafe_Last_CPU_Decision_WS-T05-R2-20260917-01.md@sha256:8d2b565beb28ca47e63df59b5d7d9236dd99c6f1967dba1190553c0a66b5800c`
- Independent Preparation PASS: `WS-TFPR-20260917-04.json@sha256:6121620284e78cee45d670565a9eadf67506fef5d09afbbe33afb1526fa26d6d`
- READY_FOR_AGENT binding: `WindowSafe_Preparation_Binding_WS-TFP-20260917-01_READY_FOR_AGENT.json@sha256:08f5c24402b4deaabb5fd3b3b0b1025daea0905b66e52795c1b4b0513e3b87b8`
- V6 Foundation 1 blob: `3b139a7dfd70da3ae6c83bbdfa703cb98ef94193`
- V6 Foundation 2 blob: `ff49e56aba09881e9e4a22dc8225949fbc4b54f6`

Foundation 2 is the Coding-Agent operating foundation. Load it from `felixvonvollmer-png/projektbeschreibung-und-geruest` by the exact blob above. Do not substitute a moving branch copy.

## 2. Repository baseline

Read-only preflight immediately before this handoff observed:

```text
repository: felixvonvollmer-png/Firefox---WindowSafe
repository_id: 1374094477
visibility: public
default_branch_name_configured: main
branches: []
bindable_start_commit: NONE
baseline_kind: EMPTY_REPOSITORY_NO_BRANCH_OR_COMMIT
```

Exact baseline record: `WindowSafe_Current_Repository_Baseline_WS-RB-20260917-01.json@sha256:9089b01742c29d496e6ba9b2f339ae18c592db8c113752372d692d7f175f1b40`.

**Fail closed before mutation:** re-read the repository. If any branch/commit now exists, do not overwrite, reset, force-push, or assume it is yours. Stop before write and return the observed state for rebinding/explicit disposition.

Because the authorized expected state is an empty Greenfield repository, creation of the initial repository commit/main baseline as needed by the bootstrap is within the execution authorization.

## 3. Execute Foundation 2 Greenfield Bootstrap only

Use Foundation 2 §8 and the exact bound Product/Technical inputs. Perform adaptive delta discovery only where needed and materialize a lean Project Foundation that provides or explicitly justifies `NOT_APPLICABLE` for the Foundation-2 project-foundation capabilities.

The repository must become the system of record and allow a new agent/reviewer to locate Product Truth, bound Technical Foundation, architecture/decisions, engineering/Git rules, review/risk/evidence contracts, canonical Project Foundation + Feature review result channel, Epic Preparation locator/result channel, development/verification commands, and the initial Epic map.

Do **not** pre-plan files/classes/functions/tasks/PRs for product implementation. Concrete repository layout, tool versions, package choices, CI details and reversible engineering choices are Coding-Agent-owned subject to the exact boundaries.

## 4. Hard scope boundaries

This run may build the **Project Foundation only**. It must not implement a normal WindowSafe product feature, tab/window capture, recovery behavior, backup/import functionality, or user-facing product workflow.

The pre-implementation stop-gates in Technical Foundation §7.1 and §§9.1/9.3 remain hard. The bootstrap may create the mechanism/context needed to satisfy those gates later; it may not treat Foundation setup as permission to implement the affected product behavior.

No real Firefox profile or real user browser/session data. No Mozilla AMO upload/signing. No production/release. No new paid provider/contract, material cost, cross-provider routing, secret/credential or data-disclosure boundary without a new user decision.

Repository visibility remains public. Never commit real URLs/session exports, browser profiles, cookies, secrets or credentials.

## 5. Git / integration envelope

Repository initialization, commits, short-lived branches, PRs, CI/guards and project-foundation integration into the development `main` are authorized where the Coding Agent determines they are needed for a healthy Project Foundation. A commit or merge is not external acceptance and not release authorization.

No force-push/history rewrite, repository rename/delete/visibility change, admin/secret mutation, or deletion of foreign work.

## 6. Required end state

Stop when the repository is genuinely:

```text
PROJECT_FOUNDATION_READY_FOR_REVIEW
```

Before stopping, perform the internal foundation review required by Foundation 2. Do not self-issue the independent `PROJECT_FOUNDATION_REVIEW` verdict.

Return at minimum:

1. exact repository end SHA/immutable end-state reference;
2. project-foundation capabilities materialized and any justified `NOT_APPLICABLE` items;
3. build/lint/test/CI/mechanical-guard evidence with evidence classes kept distinct;
4. open findings by severity and any material deviations/decisions;
5. canonical Project Foundation Review subject/evidence/result-channel locator and schema/contract needed by the independent reviewer;
6. confirmation that no normal product feature was started.

After `PROJECT_FOUNDATION_READY_FOR_REVIEW`, stop. The next V6 action is an independent `PROJECT_FOUNDATION_REVIEW`, not the first Epic or feature.
