# F01 synthetic qualification continuation

Current stop: WS-E01-F01-UBUNTU-CLOSURE-20260924-01 / WS-EA-20260919-08.
**BLOCKED__MATERIAL_USER_DECISION_REQUIRED**. Read the
[closure report and options](../../features/WS-E01-F01/evidence/ubuntu-closure.md).
No further qualification execution until the material WebApp decision and required
rebinding. Existing exact-156 restart evidence on both OSes is retained.

The `target_probe.py --closure-only` mode creates only enabled native WebApp and
remaining display/state fixtures in a new disposable profile. It does not repeat
restart/private/DevTools/PiP/Split/memory runs. Its recorded Ubuntu topology API
error and geometry timeout remain unresolved; exit 0 is not probe success.
The exact executed driver and errors are in the closure artifact pack.

For read-only input verification use `continuation.py --manifest
features/WS-E01-F01/evidence/ubuntu-closure-manifest.json --manifest-sha256 HASH`
with the external delivery hash. The historical commands below are provenance,
not authority to resume the blocked run.

## Historical Ubuntu handoff

The older commands/manifests below describe historical snapshots. For current inputs pass
`--manifest features/WS-E01-F01/evidence/win-continuation-manifest.json` to continuation.py
with the hash from the delivery report. At the prior handoff no Windows Desktop was supplied.
The historical target_probe.py ran only on the qualified Ubuntu/Wayland setup and uses privileged
Marionette chrome commands solely to construct fixtures. It does not expose those capabilities
to product code. No package, lockfile or toolchain version change is authorized.

These tools are qualification-only, never the WindowSafe product. They accept no existing
profile path and create their own disposable profile. Run from an exact checkout of the
published unmerged candidate with Python 3.14.4. Do not overwrite foreign work.

First verify the continuation manifest using the SHA-256 supplied in the delivery report:

```sh
python qualification/ws-e01-f01/continuation.py --manifest-sha256 MANIFEST_SHA256
python qualification/ws-e01-f01/toolchain.py --setup
```

This installs only the hash-pinned Node archive and exact locked dev packages in build/f01.
On Ubuntu, `python3` may be used. On Windows, use the actual Python 3.14.4 executable;
no Store launcher assumption. Windows CI checks static build/lint only, without a browser.

Provide an official Mozilla Firefox 156.0 Stable binary already present on the target system
or extracted into a workspace-local directory from the official distribution. Bind archive
URL/SHA256SUMS and actual binary hash before running. Do not use a guessed binary or change
system Firefox preferences/defaults. The installed binary can be used with the new test profile;
the real profile must never be opened or inspected. Do not run an installer that changes system
settings. If no qualified binary/extraction path exists, keep the environment gate OPEN.

Ubuntu GUI example using this run's verified official binary:

```sh
python3 qualification/ws-e01-f01/run_probe.py --firefox build/f01/firefox/firefox --firefox-sha256 7ea3daf0cdbe5ec27e4f2e7c644c25032169f8a2f2f15e438ff4379bf737a78a
python3 qualification/ws-e01-f01/cgroup_dry_run.py
```

Ubuntu requires an available user systemd manager/cgroup v2. No fallback silently replaces
complete cgroup CPU counters with sampled process CPU. The process samples are retained as a
separate diagnostic. Only the uniquely named test service may be stopped.

Windows PowerShell example (substitute the verified binary and independently recorded hash):

```powershell
python qualification/ws-e01-f01/run_probe.py --firefox 'C:\qualified-firefox\firefox.exe' --firefox-sha256 VERIFIED_BINARY_SHA256
```

The script checks the binary hash, release channel and version before creating a profile.
After launch it verifies Marionette's process ID and exact profile path before addon installation.
Use visible Desktop execution; `--headless` is diagnostic only and cannot close native GUI gates.
Windows process counters use standard-library ctypes. Their final Job Object accounting upgrade
is still an explicit continuation task. If cleanup fails, preserve the owned path/PIDs and report
it; never run a broad taskkill or delete a normal profile.

For persistent restart mechanics use only an explicitly qualified official Developer/Nightly
build with a fixed addon ID. This run's Developer archive is 157.0b3, while application.ini
Version is 157.0. The narrow signature preference is written only in the new disposable profile:

```sh
python3 qualification/ws-e01-f01/run_probe.py --firefox build/f01/developer/firefox/firefox --firefox-sha256 3ba77228cea10dd8797724d1979dfe4bf8083122d5f5342c2e477d9a1c506979 --persistent-test-build-version 157.0
```

The restart is a graceful native browser exit/relaunch, not an extension reload or simulated
startup. Marker ordinal 2 and onStartup must be observed. This testbuild is not exact 156
restart evidence. A release-equivalent unbranded 156 persistent path remains to be qualified;
never disable signature enforcement on a normal Stable installation or global profile.

Each run writes `build/f01/runs/synthetic-*/evidence.json`, samples, exact probe XPIs and browser
log; it removes only its created profile and exits only its owned process/service. Reports contain
synthetic state, not real browsing data. The packages contain no product Capture/Recovery/IDB/UI.
Evidence statuses are observations, not independent PASS. Preserve failures alongside successes.

Remaining native fixture work on both Desktop OSes: DevTools/Web-App/PiP classification;
manual private-window visibility; actual Split View membership/events; active/pinned/discarded/
muted/container/group combinations; custom missing/cross-profile container collisions;
geometry/state/multi-monitor cases. Use only new artificial profiles and local pages. Do not
infer unsupported native recreation from API existence or produce product implementations.

Bind the target environment record and execute the diagnostic sampler, then qualify Windows
Job accounting and addon memory/peak attribution under the
[measurement protocol](../../features/WS-E01-F01/evidence/measurement-method.md).
Generate deterministic metadata/schedules in a new owned output directory:

```sh
python qualification/ws-e01-f01/fixtures.py --output build/f01/continuation-fixtures
```

No full product benchmark, threshold PASS, F02, Feature Acceptance result or merge is authorized.
Return new additive evidence with exact code/head, build, profile class, commands, package hashes,
results and cleanup. Preserve all original start inputs and historical reviews. Only after BOTH
OSes and all gates converge may status advance to technical-review-ready; an independent general
technical review then precedes any separate Feature Acceptance preparation.
