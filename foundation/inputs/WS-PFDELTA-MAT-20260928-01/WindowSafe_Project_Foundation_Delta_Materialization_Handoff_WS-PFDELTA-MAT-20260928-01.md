# WindowSafe — Project Foundation Delta Materialization Handoff

```text
RUN_ID: WS-PFDELTA-MAT-20260928-01
AUTHORIZATION: WS-EA-20260928-01
ROLE: CODING_AGENT__PROJECT_FOUNDATION_DELTA_MATERIALIZATION
REPOSITORY: felixvonvollmer-png/Firefox---WindowSafe
REPOSITORY_ID: 1374094477
START_MAIN_SHA: 3bdd7439c221b8f8c83e7374c8bb29898891a4fd
NEW_BRANCH: foundation/ws-pf-delta-20260928-01
PR_TARGET: main
CURRENT_F01_PR: #3
CURRENT_F01_HEAD: 7d66ca5b025c8f748d7f97b961c496ee450daaa7
F01_PR_POLICY: READ_ONLY__KEEP_DRAFT_UNMERGED
END_STATE: PROJECT_FOUNDATION_READY_FOR_REVIEW
MERGE_AUTHORIZED: NO
```

## 1. Preflight

Before mutation:

- verify repository root, repository ID, origin and public visibility;
- verify `main == 3bdd7439c221b8f8c83e7374c8bb29898891a4fd` locally and remotely;
- verify clean worktree/index/untracked state;
- verify branch `foundation/ws-pf-delta-20260928-01` does not contain foreign work; if it already exists unexpectedly, STOP;
- verify PR #3 remains Draft/open/unmerged with head `7d66ca5b025c8f748d7f97b961c496ee450daaa7`;
- verify all package files against `SHA256SUMS.json`;
- verify exact Technical Foundation Delta Binding
  `WS-TFP-DELTA-BIND-20260928-01@sha256:684e759d4f66b8ac73a2e191b6ccaedf1416c9360619f2d89dc1ef2366b60e21`;
- verify independent review
  `WS-TFPR-DELTA-20260928-02@sha256:ce2b893e6f3c6777bb1e22c51442684d360d05508978963c7da29d9700d597c8`
  has `PASS`, verified subject integrity, no findings and no open material decisions.

No writes until every binding passes.

## 2. Canonical inputs

The package contains exact external bytes for the newly approved/reviewed delta chain.
Materialize them **append-only** in a versioned project-foundation delta input namespace
consistent with the repository's existing `foundation/inputs` conventions.

At minimum preserve exact bytes and durable locators for:

- approved Product Delta `WS-PD-DELTA-20260924-01`;
- Product Delta Approval `WS-PD-DELTA-APPROVAL-20260928-01`;
- corrected reviewed TF Delta `WS-TFP-DELTA-20260928-02`;
- Exact Binding `WS-TFP-DELTA-BIND-20260928-01`;
- independent PASS `WS-TFPR-DELTA-20260928-02`;
- prior `CORRECTION_REQUIRED` review and correction trace needed to explain the immutable chain.

Do not edit the supplied bytes when materializing originals.

## 3. Final V6 active routing

Read from `felixvonvollmer-png/projektbeschreibung-und-geruest` at the observed current main `0dc8f145d27f796ea8ae230fae6ec4b21d6aa921`:

- `foundations/v6/README.md` blob `c9c0a47d108268059ca5b5825d2d445b44179775`;
- final F1 blob `0c10e10eebcb2b23336cc9cdf4a88305a209fd22`;
- final F2 blob `3034da0fbee6ab79318da25ed65ccdc0933074e5`;
- `docs/existing_project_v6_migration_start.md` blob `5884c85334dc083171a9f7976f445e7c22fa7123`;
- `docs/target_project_llm_base_description.md` blob `043b3fe15b24a805aa15a0a78eb0f9924405fec1`;
- `docs/chatgpt_project_description.md` blob `47cffb9187017fc66e22808dbcc11167c3313c43`;
- `docs/ai_agent_playbook.md` blob `1f49fe8a8b50b28da48f1110b7fa0fe5a522727a`.

The target repository currently contains historical old V6 copies at
`foundation/sources/foundation-1.md` and `foundation/sources/foundation-2.md`.
**Never overwrite them.**

Materialize the final active F1/F2 additively (or create equally durable exact blob locators)
and update active routing so new project work no longer treats the old blobs as the active V6 basis.
Historical references remain historical.

Use the Brownfield rule: `KEEP | SIMPLIFY | REMOVE_FROM_ACTIVE_ROUTING`.
Do not rewrite functioning mechanisms merely for naming conformity.

## 4. Minimum Project-Foundation delta

Make only the durable changes earned by the reviewed delta:

- route Product Truth to base Product + approved WS-P05 delta;
- route Project Technical Foundation to r6 + reviewed/bound TF delta;
- route active V6 to the final frozen F1/F2 pair;
- update `AGENTS.md`, `README.md`, `foundation/context.md`, `foundation/architecture.md`,
  `reviews/README.md`, `epics/README.md` **only where actually needed**; do not mechanically
  touch every file;
- preserve hard recovery/privacy/container/resource invariants;
- preserve the F01 branch as an external exact evidence locator, not as content to merge here;
- preserve the required lifecycle:

```text
PROJECT_FOUNDATION_READY_FOR_REVIEW
-> INDEPENDENT_PROJECT_FOUNDATION_REVIEW
-> PASS_ONLY
-> REQUIRED_EXTERNAL_REVIEW_BOOTSTRAP_INSTALL_SYNC_OR_NOT_APPLICABLE
-> WS-E01_EPIC_PREPARATION_DELTA
-> CRITICAL_SELF_REVIEW
-> INDEPENDENT_EPIC_PREPARATION_REVIEW
-> EXACT_EPIC_REBINDING
-> NEW_F01_EXECUTION_AUTHORIZATION
-> F01_REMAINDER_QUALIFICATION
```

Do not perform any step after `PROJECT_FOUNDATION_READY_FOR_REVIEW`.

## 5. Project Foundation review subject

Create a **new versioned** Project Foundation delta subject/evidence channel.
Do not overwrite `foundation/subject.json`, because that is historical reviewed evidence.

The new subject must bind at least:

- exact start main `3bdd7439c221b8f8c83e7374c8bb29898891a4fd`;
- Product base + Product Delta + Approval;
- TF r6 + TF Delta + Binding;
- independent TF review PASS;
- final active V6 F1/F2 provenance;
- exact repository end-candidate SHA / subject path at delivery;
- exact F01 evidence locator `PR #3 @ 7d66ca5b025c8f748d7f97b961c496ee450daaa7` as motivating external evidence only;
- changed paths and checks/CI evidence;
- risk and no-product-implementation boundary;
- external Project Context Sync status `PENDING_AFTER_PROJECT_FOUNDATION_REVIEW_PASS`;
- no open material user decision unless actual new evidence requires one.

Use the current repository review contract/harness rather than inventing a competing review schema.
Extend it minimally only if necessary for a versioned Project Foundation delta subject, preserving
all historical V1/V2/V3 compatibility and append-only behavior.

## 6. External ChatGPT Project Context

There is an external ChatGPT Project channel in use, but this run **must not perform or claim**
its sync.

The meta V6 now provides `docs/chatgpt_project_description.md` as the format/persistence contract.
Use it only to ensure the repository leaves a clear durable locator for the later sync gate if
needed. Do not hardcode current delivery SHAs/status into a long-lived external description.

After a later independent Project Foundation Review PASS, the Project-LLM/user will perform or
explicitly disposition:
`REQUIRED_EXTERNAL_REVIEW_BOOTSTRAP_INSTALL_SYNC_OR_NOT_APPLICABLE`.

## 7. Verification

At minimum:

- preserve exact hashes/bytes of all historical bound originals;
- verify the newly materialized external originals byte-for-byte against package hashes;
- run all existing Foundation checks/unit tests;
- run deterministic Foundation build if supported;
- validate review request/schema/history compatibility for the new subject;
- `git diff --check`;
- inspect exact changed paths and staged diff;
- commit normally;
- push only the new branch;
- create/update a separate PR to `main`;
- inspect exact-head CI and preserve run/job references.

Do not weaken guards because the delta exposes a failure.

## 8. Stop / return

Success stop:

`PROJECT_FOUNDATION_READY_FOR_REVIEW`

Return:

- branch, PR number/URL;
- exact start SHA;
- exact end HEAD/tree;
- subject path/blob/SHA and evidence locator;
- exact changed paths;
- new input/hash inventory;
- local checks and exact-head CI;
- proof historical originals unchanged;
- proof PR #3/F01 branch unchanged;
- any findings/open material decisions;
- explicit statement that no merge, external context sync, Epic delta or F01 continuation occurred.

If a material conflict or unsupported lifecycle issue appears, STOP before hiding it.
