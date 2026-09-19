# WindowSafe – WS-E01-F01 Qualification Plan

```text
FEATURE_ID: WS-E01-F01
EPIC_ID: WS-E01
RUN_ID: WS-E01-F01-START-20260919-01
START_BASELINE_SHA: 3bdd7439c221b8f8c83e7374c8bb29898891a4fd
TARGET_BRANCH: feature/ws-e01-f01-qualification
FEATURE_TYPE: TECHNICAL_ENABLER
RISK_FLOOR: ELEVATED
PRODUCT_IMPLEMENTATION: PROHIBITED
```

## Objective

Close the mandatory **preimplementation** gates for the later WindowSafe capture/recovery
features without building those product features.

F01 must produce durable, reviewable evidence for:

1. Firefox-156 / Windows / Ubuntu platform and detection boundaries.
2. Minimal manifest/permission direction.
3. Reproducible Node/TypeScript/web-ext toolchain and supply-chain baseline.
4. Disposable-profile/restart test path.
5. R500/R2000/H and T05-R2 measurement methodology.
6. Safe fallbacks and explicit blockers for capabilities that cannot be proven.

F01 itself does **not** implement the canonical IndexedDB recovery store, normal capture,
startup reconciliation, named windows, restore UI, daily backups or import.

## Required traceability

Product:
- WS-RESTORE
- WS-QUALITY
- WS-OL-01 / WS-OL-03
- WS-AC-08 / WS-AC-09 / WS-AC-11

Technical Foundation:
- §7 / §7.1 platform qualification
- §9.1 / §9.3 measurement-method binding
- §10.2 evidence separation
- §11 Epic direction

Epic:
- `epics/WS-E01/preparation.md`, F01 section and `F01 -> F02 -> {F03,F04} -> F05`.

## Workstreams

### A. JIT feature/lifecycle support

Materialize a narrow generic `features/<FEATURE_ID>/` channel suitable for:
- start/baseline records;
- feature plan/test envelope/evidence;
- future `features/<FEATURE_ID>/subject.json` only when the full feature becomes
  `READY_FOR_ACCEPTANCE_REVIEW`;
- future `FEATURE_ACCEPTANCE_REVIEW` request through the already defined V3 contract.

The harness must continue to reject arbitrary product paths and fabricated acceptance.
Historical Product/Foundation/Epic/review originals remain append-only.

### B. Toolchain qualification

Start from these **current candidates**, but bind only after actual compatibility checks:

- Node.js **24.21.0 LTS**.
- `web-ext` **10.6.0**.
- TypeScript **7.0.2**.
- Type definitions: evaluate the current Firefox/WebExtension type packages against the actual
  Firefox-156 APIs used by the probe. Do not treat a stale package version as API truth.

Requirements:
- exact `package.json` / lockfile / package-manager version;
- no production dependency unless technically necessary and justified;
- dependency provenance/license/security notes;
- deterministic typecheck/build/lint/probe commands;
- no bundler/framework merely for convenience;
- if TypeScript 7 causes a real tooling incompatibility, document it and qualify the smallest
  compatible TS6 side-by-side/fallback rather than silently downgrading;
- `web-ext lint` is supplementary only: its current release schema may lag Firefox 156, so actual
  Firefox-156 runtime/API qualification remains mandatory.

### C. Minimal permission/manifest direction

Qualify the Foundation direction without expanding it:

Expected product-direction permissions:
`tabs`, `storage`, `sessions`, `alarms`, `downloads`, `tabGroups`, `cookies`,
`contextualIdentities`, `unlimitedStorage`.

Expected negative boundary:
no general host permissions, no `scripting`, `webRequest`, `history`, `browsingData`,
`nativeMessaging`; no fictional `windows` permission.

Private mode direction:
`incognito: "not_allowed"` plus runtime context checks.

Qualification probes may request **additional test-only helper permissions** only when required to
create a synthetic state (for example `tabHide` in a separate helper probe). Such permissions must
be marked TEST_ONLY and must never leak into the product manifest direction.

### D. Firefox-156 platform matrix

For each item record:
`SOURCE/API`, `TARGET BUILD/OS`, `PROBE OR PRIMARY-DOC EVIDENCE`, `SUPPORTED BOUNDARY`,
`SAFE FALLBACK`, `STATUS`.

At minimum:
- normal vs popup vs devtools vs Web-App/PiP handling;
- private/incognito exclusion;
- hidden tabs created by another synthetic helper add-on;
- containers / `cookieStoreId`, missing container, cross-profile identity non-equivalence;
- native tab groups and group-id durability;
- split-view observation vs native recreation availability;
- reader-mode intent;
- `discarded`, `pinned`, `muted` combinations;
- privileged/non-openable URLs;
- window geometry/state and safe fallback;
- sessions window/tab values as hints;
- startup/restart event and native restore signals, especially the absence of any unsafe
  "restore complete because a timer expired" inference.

If a material Product capability cannot be safely supported on the target matrix, STOP the
affected work and return a material user-decision request; do not weaken Product Truth.

### E. Restart/persistence test path

Use only disposable profiles.

For tests that do not need persistence, exact Firefox 156 Stable is preferred.

For restart persistence:
- use a fixed test add-on ID;
- use an official Mozilla test build capable of persistent unsigned test installation
  (e.g. official/unbranded Release-equivalent or Developer/Nightly as justified);
- any `xpinstall.signatures.required=false` change is allowed only inside the dedicated disposable
  profile of that test build, never in the user's normal profile;
- no AMO signing/upload;
- clearly distinguish target-Stable runtime evidence from test-build-only restart mechanics.

If exact target-equivalent restart evidence cannot be established, leave that gate visibly open.

### F. Measurement-method binding

Do **not** run or claim the final F05 performance acceptance here. F01 binds and validates the
method.

The method must define, separately for Windows and Ubuntu:
- exact Firefox build and OS build;
- hardware/CPU/RAM/storage identity;
- synthetic profile generation for R500, R2000 and H;
- identical A/B workload without/with the future add-on;
- at least five valid pairs per profile/OS for final measurements;
- warm-up, background-load controls and invalid-run criteria;
- process-tree attribution for Firefox;
- CPU normalization in `% of one CPU core`;
- attributable/observable RAM, with native/unattributable memory separately reported;
- logical data size, IndexedDB file growth and backup size;
- write counts/logical bytes vs actual I/O separated;
- event-to-successful-persistence latency measurement;
- L10 and B300 workload generation and timing windows;
- idle 10-minute method;
- UI-list latency method;
- export/import peak-memory method;
- uncertainty/measurement limitations.

F01 must execute small dry-runs sufficient to prove the instrumentation works on each available
target OS, but must not present those dry-runs as T02/T05-R2 PASS.

### G. OS completion rule

Full F01 convergence requires both **Ubuntu Desktop** and **Windows** target evidence.

If the executing environment has only one OS:
- complete all shared work and that OS's evidence;
- generate a byte/hash-bound continuation package/scripts for the missing OS;
- stop as `WS-E01-F01_PARTIAL_QUALIFICATION__TARGET_ENVIRONMENT_REQUIRED`;
- do not create a `READY_FOR_ACCEPTANCE_REVIEW` Subject.

## Risk and reviews

Cumulative F01 risk floor: **ELEVATED** because its outputs gate later recovery correctness and
browser/runtime assumptions.

Before any F01 branch integration:
- independent general technical review is required;
- findings must be fixed/rereviewed as required;
- only after technical convergence may the feature be prepared for independent
  `FEATURE_ACCEPTANCE_REVIEW`.

This execution run itself must stop before merge and before external Feature Acceptance.

## Success state for this run

If complete on both target OSes:
`WS-E01-F01_READY_FOR_INDEPENDENT_TECHNICAL_REVIEW`

If a target OS is missing:
`WS-E01-F01_PARTIAL_QUALIFICATION__TARGET_ENVIRONMENT_REQUIRED`

If Product/Platform conflict requires the user:
`WS-E01-F01_BLOCKED__MATERIAL_USER_DECISION_REQUIRED`

No later feature may start from any of these states.
