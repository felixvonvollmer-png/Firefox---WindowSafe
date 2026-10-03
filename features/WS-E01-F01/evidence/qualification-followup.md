# F01 additive closure record after first-head CI

Current STOP: **WS-E01-F01_BLOCKED__QUALIFICATION_GATE_FAILED**.
Cumulative start remains `3bdd7439c221b8f8c83e7374c8bb29898891a4fd`.
The exact current Head/Tree and CI run URLs are in the terminal delivery record;
this record is bound by the commit containing it. Draft PR:
https://github.com/felixvonvollmer-png/Firefox---WindowSafe/pull/3 .

The [original qualification report](qualification-report.md), original browser evidence,
toolchain pins and lock hash remain unchanged. This additive record supersedes its test count
and continuation locator. It does not overwrite historical evidence or declare independent PASS.

[First-head CI](first-head-ci.json) at `eb7e93b3fcc89089ebd05682b70082d82129b441`
completed with failure in both push and PR runs. Ubuntu reached two failing existing negative
assertions: after entering the Feature phase, the accepted-Epic validator delegated to the exact
base without comparing the current canonical Epic review result. The general result/history
guards remained, but this standalone consumer could overlook a replaced/missing current result.
The correction explicitly compares current result bytes with the accepted base before delegation.
Existing assertions are unchanged; an additional Feature-phase regression exercises this path.
The prior local 105-test run was before the first commit, when HEAD still equalled the start base;
that did not exercise the post-base branch of this consumer. This discrepancy is retained rather
than presenting the prior local run as committed-head evidence.

Local corrected suite: 106 tests PASS, including synthetic Git-history tests and the explicit
Feature-phase review-byte regression. Foundation check, schema/request compatibility,
append-only history and deterministic inventory are required again on the corrected commit.
No qualification runtime source changed; the Stable/Developer cgroup probes remain applicable.
Only the continuation locator and sanitized audit-failure reporting changed in toolchain utilities.

Windows Server CI reached the mandatory npm audit and failed. The final local audit attempts
returned HTTP 503 maintenance twice. Earlier zero-advisory evidence for the unchanged lock is
retained but cannot replace the failed live gate. Audit failures now print only categorical status
and vulnerability counts, never HTTP response headers. The audit remains mandatory in both CI
jobs. No retry result or future green CI is asserted here.

Current continuation: [hash manifest](continuation-followup-manifest.json), built archive
`build/f01/WS-E01-F01-continuation-followup.zip`. The original manifest/archive remain bound to
the first head. The corrected source set is complete in the new manifest; its hash and the
archive hash are delivered separately. [Cumulative changed paths](followup-changed-paths.json).

Open gates remain: live audit/CI; Windows Desktop runtime and measurements; remaining native
GUI/API combinations; exact-156 persistent restart; Windows Job and addon memory/peak attribution.
Risk remains ELEVATED. After these converge, an independent general technical review is required,
then separately authorized Feature Acceptance. No product implementation, F02, self-verdict,
Acceptance Subject, merge, release or production operation.
