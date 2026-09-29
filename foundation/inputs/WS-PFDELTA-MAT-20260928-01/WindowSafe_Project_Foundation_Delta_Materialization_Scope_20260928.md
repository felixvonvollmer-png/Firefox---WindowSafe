# WindowSafe — Project Foundation Delta Materialization Scope

```text
STATUS: READY_FOR_EXECUTION_AUTHORIZATION
BOUND_TF_DELTA: WS-TFP-DELTA-20260928-02
BOUND_TF_DELTA_SHA256: 8c687681f9a46cf0782212ebfa5be5d6e22cac77d890b1f436a8395f7b1c5d2c
BINDING_ID: WS-TFP-DELTA-BIND-20260928-01
BINDING_SHA256: 684e759d4f66b8ac73a2e191b6ccaedf1416c9360619f2d89dc1ef2366b60e21
INDEPENDENT_REVIEW: WS-TFPR-DELTA-20260928-02
INDEPENDENT_REVIEW_SHA256: ce2b893e6f3c6777bb1e22c51442684d360d05508978963c7da29d9700d597c8
INDEPENDENT_VERDICT: PASS
```

## Materialization objective

Materialize only the minimum Brownfield Project-Foundation delta needed to make the
approved WS-P05 Product Truth and reviewed Technical Foundation Delta durable and routable.

The Coding Agent must start from current `main`
`3bdd7439c221b8f8c83e7374c8bb29898891a4fd` on a separate short-lived foundation-delta
branch. PR #3 / F01 remains Draft, unmerged, and read-only context.

## Required result

- append-only Product Delta + Approval locators;
- append-only Technical Foundation Delta + Binding locators;
- minimal active routing/context/guard update;
- no historical rewrite;
- no F01 execution;
- no product feature implementation;
- no WS-E01 Epic Preparation Delta;
- end at `PROJECT_FOUNDATION_READY_FOR_REVIEW`;
- independent `PROJECT_FOUNDATION_REVIEW` is the next gate.

## External Project Context Sync

Do **not** perform or claim it during materialization.

Only after `PROJECT_FOUNDATION_REVIEW = PASS`:

`REQUIRED_EXTERNAL_REVIEW_BOOTSTRAP_INSTALL_SYNC_OR_NOT_APPLICABLE`

must receive a real disposition before WS-E01 Epic Preparation Delta begins.
