# WS-E01-F01 qualification result

STOP: **WS-E01-F01_BLOCKED__QUALIFICATION_GATE_FAILED**.
Partial platform evidence and the continuation package are preserved. The final required npm
audit encountered registry maintenance HTTP 503 twice; the earlier zero-finding audit remains
valid historical evidence for the unchanged lock, not a successful final live check.
Run WS-E01-F01-START-20260919-01 under original WS-EA-20260919-06.
No feature completion, independent technical acceptance, Feature Acceptance or merge.
F02/F03/F04/F05 remain unstarted. All WindowSafe product implementation remains closed.

## Exact subject and traceability

Repository felixvonvollmer-png/Firefox---WindowSafe, public, ID 1374094477 verified remotely.
Start main SHA `3bdd7439c221b8f8c83e7374c8bb29898891a4fd`, tree
`034b79c80d9e1e6ae2b57268e6dbaf94bfb31b58`; clean local main fast-forwarded from its
ancestor, then `feature/ws-e01-f01-qualification` created at exactly this base.
No intervening non-feature changes. End candidate is the commit containing this report;
the delivery report supplies exact Head/Tree, Draft PR and subsequent Exact-Head CI evidence.
The full changed-path inventory is [changed-paths.json](changed-paths.json).

Nine package files passed SHA-256 and byte-length verification before six feature originals
were copied unchanged. Original [manifest](start-package-manifest.json) SHA-256:
`e448735a9a98c88b6f0e634050b2667e0af18a3cc089ba4cf63d34ddfc10e87b`.
[Handoff](execution-handoff.md) and authorization are preserved as exact inputs.
Epic WS-E01 remains READY_FOR_AGENT, reviewed Preparation at
`644b81f63dcc1990bc894a9c2c9bd8dc24a98c04`, result WS-E01-EPR-20260919-02 unchanged.

Product anchors: WS-RESTORE, WS-QUALITY, WS-OL-01/03, WS-AC-08/09/11.
Technical Foundation §§7/7.1, 9.1/9.3, 10.2, 11; Foundation 2 §31.
Epic preparation F01 and dependency F01 -> F02 -> {F03,F04} -> F05.
[Original acceptance criteria](../acceptance-criteria.md) remain the complete checklist.

## Results and limits

- JIT harness: valid feature lifecycle/evidence namespace, exact original authorization/start
  hashes and base/tree, current accepted Epic and Product/Foundation/Review traceability,
  minimum ELEVATED risk, strict product path exclusions and no premature Acceptance Subject.
  Current feature state cannot issue an independent verdict. Historical result cardinality,
  original bytes, cumulative bases and all intermediate history checks remain in force.
- [Toolchain](toolchain-decision.md): exact Node/npm/TypeScript/web-ext/declaration pins and
  locked scoped image-size patch; reproducible install/compile, both web-ext lints, audit and
  registry signature evidence. No product runtime dependencies/framework/bundler.
- [Platform matrix](platform-matrix.md): actual Ubuntu Stable API observations, testbuild-only
  permanent restart, documented boundaries and explicit unexecuted cases. Windows Desktop
  runtime is missing. Documentation, static CI and testbuild restart are distinct evidence.
- [Measurement protocol](measurement-method.md): r6/T05-R2 workload and five-pair acceptance
  design, synthetic generator, real Ubuntu process/cgroup instrumentation dry-runs, explicit
  attribution uncertainty. No product threshold or F05 PASS. Windows accounting and native
  addon memory/peak qualification remain open.
- Own profiles were newly generated and removed. Process/profile IDs were checked before
  extension installation. Stable signature policy was unchanged. The Developer signature
  preference was restricted to its owned disposable profile. No user profile, browser data,
  login, AMO, signing, distribution, production or unrelated-process termination.

## Verification and interaction coverage

Local Foundation check; full 105-test regression suite; repeated deterministic inventory build;
canonical review/schema compatibility; append-only history against exact start and cumulative
historical bases; typecheck/repeated compile; probe/helper lint; npm audit; package signatures;
actual synthetic Ubuntu browser/restart and process/cgroup measurements. Exact command outputs
are recorded separately. The source changes do not implement a WindowSafe product module.

The committed head runs both static Ubuntu/Windows CI jobs. Failed mandatory checks keep the
qualification gate closed; a Draft PR is permitted to preserve and review this blocked work. CI results are queried at the exact published head and
reported with run URLs at delivery; this pre-CI record does not assert future green CI.
Windows CI uses windows-2025 Server and is never Windows Desktop GUI evidence.

The bounded general self-review checked original immutability, hidden/private data boundaries,
profile/process isolation, fail-closed gates, declared permissions and measurement limits.
It is not an independent technical PASS. Known qualification gaps remain blocking completion.
Linked work item: WS-E01-F01; the Draft PR is a delivery locator, not integration authority.
No specialized or independent reviewer has been used in this implementation run.

## Risk, open gates and continuation

Cumulative risk **ELEVATED**: this feature gates later recovery correctness and browser/privacy
assumptions and extends lifecycle/history enforcement. Required review coverage: independent
technical review of the cumulative delta, with specific attention to harness trust boundaries,
process/profile cleanup, security override, platform interpretation and measurement attribution.
Only subsequent technical convergence can lead to separately authorized Feature Acceptance.

Blocking qualification gaps (not fabricated external review findings):

1. Required live npm audit unavailable (HTTP 503); no audit-gate bypass.
2. Windows Desktop Firefox 156 runtime, native cases, restart and measurements.
3. Special-window/private/Split View/geometry and remaining API-combination native fixtures.
4. Persistent restart on an exact release-equivalent Firefox 156 test build.
5. Windows Job accounting and addon-attributable memory/peak trace qualification.

These are retained as OPEN gates before affected product implementation. No material Product
scope decision or fallback was silently accepted. If a later test demonstrates an actual
Product/platform conflict, stop for a material decision instead of weakening the requirement.

Executable, hash-bound [continuation](../../../qualification/ws-e01-f01/README.md) and
[manifest](continuation-manifest.json) preserve the current sources and evidence. The archive
is created in build/f01 and its SHA-256 is supplied in the delivery report. New target evidence
must be additive. Living routing documents point to this partial state; historical accepted
subjects and reviewer findings are untouched. Ordinary toolchain deprecation notices are
tracked in the supply-chain record for the next tool upgrade.
