# WS-E01-F01 – Qualification Acceptance Criteria

F01 is ready for independent technical review only when all applicable criteria below are
evidenced, with Windows/Ubuntu gaps explicitly blocking completion.

## Toolchain
- Exact Node LTS, npm, TypeScript, web-ext and type strategy are pinned.
- Lockfile is reproducible and dependency/provenance/license notes exist.
- Typecheck and qualification build succeed on both target OSes or OS-specific gaps are explicit.
- `web-ext lint` status and its Firefox-schema-version limitation are recorded.
- No unnecessary production dependency/framework/bundler has been introduced.

## Manifest/permissions
- MV3/Event-Page direction is proven compatible with Firefox 156.
- Minimal product permission direction matches Technical Foundation §7.
- `incognito: not_allowed` is verified.
- Any helper-only permission is isolated and cannot enter the product direction.

## Platform matrix
- Normal/special-window classification has a safe, evidence-backed rule.
- Hidden tabs are not misclassified as absent.
- Containers, missing/cross-profile containers and `cookieStoreId` boundaries are qualified.
- Group identity and group restore limitations are qualified.
- Split View observation/recreation boundary is explicit.
- Reader/discarded/pinned/muted combinations have a proven or safely bounded behavior.
- Privileged/non-openable URL behavior is explicit.
- Session-value/startup/restart evidence does not invent a restore-complete signal.
- Every unsupported/uncertain case has a safe Product-compatible fallback or a material-decision
  STOP.

## Test envelope / restart
- No real user profile/data was used.
- Persistent restart path is reproducible in a disposable profile with fixed add-on ID.
- Stable-target vs test-build-only evidence is distinguished.
- No AMO/signing/global signature changes occurred.

## Measurement method
- Exact Windows and Ubuntu A/B methods are bound.
- Process attribution, CPU normalization, RAM/I/O/DB/logical-size/latency methods are explicit.
- R500/R2000/H, L10, B300, idle, UI-list and export/import methods are specified.
- At least one small synthetic dry-run per available target OS proves instrumentation operates.
- No dry-run is mislabeled as T02/T05-R2 product PASS.

## Governance
- Feature start baseline is exact.
- Epic READY_FOR_AGENT and reviewed Preparation remain immutable.
- F02/F03/F04/F05 have not started.
- Current branch is unmerged.
- Cumulative risk is at least ELEVATED.
- Independent general technical review is the next gate.
