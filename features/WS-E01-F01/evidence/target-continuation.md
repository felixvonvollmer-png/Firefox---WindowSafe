# Exact F01 target continuation

This handoff belongs to WS-E01-F01-TARGET-QUAL-20260919-01 / WS-EA-20260919-08.
Use the exact unmerged commit/tree and manifest SHA-256 from the delivery report, PR #3,
branch feature/ws-e01-f01-qualification. One branch writer only; verify clean worktree/index,
repository ID 1374094477 and unchanged main 3bdd7439c221b8f8c83e7374c8bb29898891a4fd.
Lock SHA-256 must remain 1d6f6b41f6a87d1890695247e6610f60199518b22e87f12f1ee1002661563834.
Do not reinterpret stale historical BLOCKED reports as the current state; use state.json.

Verify the exact input inventory (no browser is launched):

```sh
python3 qualification/ws-e01-f01/continuation.py --manifest features/WS-E01-F01/evidence/target-continuation-manifest.json --manifest-sha256 DELIVERY_MANIFEST_SHA256
```

Rebuild the archive with the same command plus --build only if the destination does not exist.
It never overwrites an existing archive. The manifest excludes itself to avoid a hash cycle;
its external delivery hash binds it. This package contains sources/evidence, not browser binaries.

## Ubuntu repeat commands

Use Python 3.14.4 and the already pinned dev toolchain. Verify exact official Stable 156
archive/binary provenance as in the prior download record. For release-equivalent execution,
download only the artifact_url in target-unbranded-download.json; verify its exact SHA-256
and official checksums before extracting into a fresh workspace-local folder. Never run an
installer or overwrite an existing installation. The runner verifies every extracted file
against the hash-bound record, not just the shared launcher hash.

```sh
python3 qualification/ws-e01-f01/toolchain.py
python3 qualification/ws-e01-f01/target_probe.py --firefox build/f01/firefox/firefox --firefox-sha256 7ea3daf0cdbe5ec27e4f2e7c644c25032169f8a2f2f15e438ff4379bf737a78a
python3 qualification/ws-e01-f01/run_probe.py --firefox build/f01/target-unbranded/firefox/firefox --firefox-sha256 7ea3daf0cdbe5ec27e4f2e7c644c25032169f8a2f2f15e438ff4379bf737a78a --release-equivalent-binding features/WS-E01-F01/evidence/target-unbranded-download.json --release-equivalent-binding-sha256 39856ddb2f4b8133ca842b8d7ab325da32cff38ddc8c30b6e592aa4cdedb12e4
```

No existing profile path is accepted. The native runner requires Ubuntu/Wayland and a real
visible Desktop. It uses privileged chrome automation only inside the verified owned process.
Every failure/attempt is retained; only owned processes/profiles may be cleaned.

## Remaining Windows work

No Windows Desktop is currently supplied. Before executing, bind an actual interactive
Windows client host, OS/build, CPU/RAM/storage/power/display and official Stable Firefox 156.
No Server-CI, Wine, Linux or Developer 157 surrogate. The
[unbranded Windows locator](target-windows-build-locator.json) is only an official metadata
lead; the archive was not downloaded or executed. Verify it, full installation and equivalent
build metadata on that host. The current unbranded validator intentionally allows only the
actually qualified Linux artifact; a Windows extension needs its own verified binding/tests.

Before counting Windows measurements, implement and qualify the owned native Job launcher:
create Firefox suspended; establish non-breakaway job limits; assign before resuming; fail
closed on assignment/nesting/containment errors. Verify every descendant and PID creation
identity. Query lifetime basic+I/O counters including exited children, explicit memory/peak
semantics and post-exit cleanup. Exercise short-lived children, rejected breakaway, nesting
and failure cleanup. Never fall back to sampled-only CPU or broad taskkill.

Run the full Windows matrix independently: ordinary/popup/private, hidden tabs, container
collision/missing cases, groups, actual splits/events, reader/state interactions, privileged
URLs, geometry/states, session/startup hints, native DevTools/WebApp/PiP. Complete remaining
Ubuntu enabled-WebApp/safe-boundary and geometry/display coverage separately. No OS evidence
substitution and no user Firefox/default/profile changes.

## Memory and lifecycle closure

Resolve cache and shared/native attribution and continuous peak coverage on both OSes.
Pair controlled synthetic A/B OS counters with Firefox-native reports/traces; declare gaps,
driver overhead and uncertainty. Neither point samples nor total process memory close the
addon hard-peak gate. No F05 product thresholds are accepted in this feature.

Run relevant regressions, Foundation check/build/history/schema/request, exact unchanged
toolchain/audit, named-path review and both new-head CI workflows. Add evidence; never rewrite
prior records. Remove a gate only with both applicable Desktop results. All four gates remain
globally open in this delivery. Risk ELEVATED; only after convergence prepare independent
technical review. No self-review verdict, Feature Acceptance, final V6 migration, merge or F02.
