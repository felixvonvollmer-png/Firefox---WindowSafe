# Windows F01 qualification — PARTIAL / STOP

WS-E01-F01-WIN-20260924-01 continues WS-EA-20260919-08 from
`7b52f6655e4478caa4864801b24877d22c33fa83`, tree
`b5107a356aa5f86645a110a029adb2b11072af1f`. Feature/main basis remains
`3bdd7439c221b8f8c83e7374c8bb29898891a4fd`. This is Coding-Agent qualification
evidence, not an independent verdict. Risk remains ELEVATED.

## Host, inputs and isolation

[Preflight](win-preflight.json), [host](win-host.json), [displays](win-displays.json)
and [verified attached inputs](win-input-package.json) bind the actual Windows client.
Windows 11 Pro 23H2, build 22631.6199, x64; Ryzen 5 3600, six reported logical
processors, 17,100,005,376 bytes RAM; GTX 980 Ti driver 32.0.15.8228; NTFS workspace.
Two 1920x1080 monitors span x=-1920 through 1920. Interactive session 1 and input
desktop access were observed. The registry still says Windows 10 Pro; this does
not supersede the numeric build or Win32_OperatingSystem caption.

Only workspace-extracted official Mozilla browsers were launched. Installed
Firefox 156.0.1 was read as version context only. No normal Firefox profile was
opened, inspected or reused. No installer, default-browser change, signing or
pin-to-taskbar operation was performed. Every run created and removed its own
synthetic profile; final owned Job active-process counts are zero.

- [Stable binding](win-stable-download.json): Firefox 156.0, build 20260909172920,
  official installer SHA-256 `86a027237f7408e8a4d18637c57d487455a704cbb2466a32d0d14c2207d2699a`;
  the embedded 7z payload was extracted with Windows tar, never executed as an installer.
- [Unbranded binding](win-unbranded-download.json): same version/build/source,
  official task OSCRr3diR7SXwQr0i6Y1dQ, archive SHA-256
  `30a3444f7416479ec78d03bc48ad63f0a669aa91b40481943c7de426ba8fa25f`.
  Mozilla SHA-512 and chain-of-trust artifact SHA-256 match. The signature of that
  chain-of-trust document was not independently verified.
- Both use release revision `a80bd15ddee3b4bf3679aeba340e9d2db933c467`.
  Bindings inventory all 73 Stable / 69 unbranded installation files. The Windows
  release-equivalent validator requires the exact task, archive pin, build, platform,
  official unsigned-compatible metadata, binary and entire installation inventory.

## Gate disposition by OS

| Gate | Windows Desktop | Existing Ubuntu Desktop | Global disposition |
|---|---|---|---|
| WINDOWS_DESKTOP | Actual visible matrix executed; WebApp safe classification remains unresolved | Not a substitute for Windows | OPEN |
| SPECIAL_NATIVE_GUI_CASES | Private, DevTools, PiP, Split View, WebApp and two-monitor geometry observed; WebApp appears normal to extension APIs | Native evidence exists; enabled WebApp classification and display/state coverage remain incomplete | OPEN |
| TARGET_EQUIVALENT_RESTART | Exact official release-equivalent 156; persistent onInstalled -> onStartup, ordinal 1 -> 2, prior marker and tab session hint retained; both exits 0 | Same exact-156 restart already evidenced | CLOSED_BY_QUALIFICATION_EVIDENCE; no acceptance verdict |
| MEASUREMENT_FINAL_ATTRIBUTION | Native Job lifetime counters and synthetic regressions executed; addon cache/shared attribution, hard peak and complete short-lived PID identity coverage not qualified | Origin JS/DOM reporters and cgroup evidence exist; cache/shared/hard-peak gaps remain | OPEN |

Ubuntu was not re-executed from this Windows host. Its exact prior evidence remains
[native/memory](target-ubuntu-native-memory.json), [restart](target-ubuntu-restart.json)
and [prior report](target-qualification.md). No Windows observation closes an Ubuntu gap.

## Windows matrix and supported boundaries

[Stable MV3 event-page probe](win-stable.json) and [native probe](win-native-memory.json)
are actual WINDOWS_RUNTIME_VERIFIED observations. Chrome automation is TEST_ONLY
fixture creation inside the verified owned browser, never a product capability.

- Normal and popup windows, hidden-helper tabs, native groups, reader intent,
  pinned/muted/discarded combinations, session hints and install/startup behavior
  were observed. Unsupported active+discarded and pinned+discarded requests reject.
  Hidden tabs remain returned by the API. Grouping a pinned tab unpins it; group IDs
  are observed identifiers, not a durable cross-profile identity contract.
- Native private windows exist while the incognito-disallowed probe cannot see them.
  The extension's direct private-window request rejects. Detached DevTools and PiP
  are native windows excluded from the extension's normal windows listing.
- Actual split tabs share a splitViewId and emit onUpdated split changes. No public
  split-creation API was established; Product Truth's ordinary-tab fallback remains
  the boundary, not privileged reconstruction in product code.
- Two containers with identical name/color/icon receive distinct IDs (8 and 9).
  Independent fresh profiles reuse custom container ID 6. Missing/removed container
  IDs reject. Neither presentation equality nor numeric ID equality proves identity.
- A privileged chrome URL rejects. No bypass was attempted. The probe does not claim
  exhaustive classification of every non-openable URL scheme.
- Normal/maximized/minimized/fullscreen transitions were observed. A requested
  x=-1800 placement reached the left monitor. An offscreen (-10000,-10000) request
  was constrained to (-1920,0). These observations support best-effort placement;
  they do not prove behavior under monitor removal, topology changes or mixed DPI.
- Enabled native Taskbar Tab/WebApp opened from a synthetic registry JSON preseeded
  inside the disposable profile, using the exact target's TaskbarTabs.openWindow.
  Its native taskbartab attribute was present, but windows.getAll exposed it as
  type `normal` with one ordinary tab. No public reliable WebApp discriminator was
  established. Merely checking `window.type === normal` is insufficient evidence
  for the Product special-window boundary. This is a material unresolved platform
  finding; affected product implementation stays stopped pending an evidence-backed
  rule or an explicitly authorized Product decision. Product Truth was not changed.

The last WebApp path was selected by reading Mozilla's exact-revision
TaskbarTabs/WindowManager/Registry source. It bypasses the creation-and-pinning
entry point, not Firefox security restrictions; it uses a test-only preseed.
It establishes window/API classification, not a normal user install workflow.

## Restart

[Final restart](win-restart.json) uses fixed helper/probe IDs and persistent installs
only in an unbranded disposable profile. The signature preference exists only there.
Both launches bind the exact executable, returned Marionette profile, browser PID
and creation FILETIME within the owned Job. Windows Firefox's initial launcher PID
differs from the browser PID; requiring launcher equality initially failed closed.
The corrected binding verifies actual Job membership and exact executable path
before installing anything. The failed attempt is retained in the artifact pack.

Graceful native quit/relaunch produced onInstalled/1 then onStartup/2, exact prior
storage marker, and at least one matching persisted synthetic tab session hint.
Both jobs emptied and exited 0. No timer is interpreted as restore completion.

## Job accounting, memory and uncertainty

The native launcher creates a suspended root, sets KILL_ON_JOB_CLOSE without either
breakaway flag, assigns and verifies membership, then resumes. It fails closed on
assignment/binding failures. Existing parent-job nesting and Firefox sandbox jobs
worked on this host. Cleanup only terminates the owned Job or its suspended root.
Lifetime user+kernel CPU and aggregate I/O include exited children; working-set
and private-byte point samples remain separate diagnostics, never a CPU fallback.

Six native regression cases exercise lifetime child CPU/I/O/peak, breakaway denial,
failed assignment before marker execution, owned cleanup, nested accounting and
foreign PID/executable rejection. [Synthetic dry-run](win-job-dry-run.json) retained
a 64 MiB transient allocation in the post-exit whole-job peak without intermediate
memory samples: idle 19,349,504 versus pulse 86,810,624 bytes. The 100-query idle-job
median was about 0.1235 ms, maximum 0.4526 ms. Driver CPU rounded to zero at this
short duration; zero overhead is not inferred. Console-host membership explains
why initial exact process-count assertions (1/2) failed; they were replaced with
workload/exit/CPU/I/O/peak assertions and lower bounds. Original failures are recorded.

Live PID creation identities are sampled. The final Stable Job counted 18 lifetime
processes but retained only 17 identities. Therefore complete per-descendant identity
qualification is OPEN, even though native aggregate lifetime accounting operates.
These counters are synthetic qualification evidence, not final accepted F05 metrics.
Normalize future interval CPU as 100*(user+kernel delta)/wall_seconds per one core;
do not divide by six. I/O transfer counters are not physical disk-write bytes.

Native memory reporters were paired with same-run OS Job and process diagnostics:
A without addon, B idle, B holding 4 MiB typed-array/1000 DOM nodes/1024 Map entries,
then a 12 MiB pulse. Held disjoint origin leaves were JS 5,052,088, DOM 328,800 and
layout 847,392 bytes. Driver sandbox leaves were separately 64,008 bytes at that
point and increased with reports. Reporting plus diagnostic collection took about
177–208 ms per point. Private bytes and working-set sums are retained separately;
shared pages can appear in multiple working sets.

The Map cache is not separately attributed. Shared/native residual remains unknown.
Windows advertised jsallocations but not nativeallocations. No continuous addon
allocation trace was qualified; a later report seeing the pulse does not prove
arbitrary short-peak coverage. Whole-job commit peaks cannot establish addon-only
hard RAM peaks. Sequential A/B includes order/startup/background/instrumentation
confounders; no five-pair product workload or F05 threshold acceptance is claimed.

## Verification and continuation

[Local verification](win-local-verification.json) records actual command results and
platform limitations. Package/lock/toolchain versions remain unchanged. The Windows
CI job adds only binding and synthetic Job regressions; Server CI remains incapable
of establishing Desktop GUI evidence. Final delivery reports new Head/Tree and
exact-head push/PR CI separately, avoiding a self-referential evidence hash.

[Runtime artifact pack](win-runtime-artifacts.json) retains attempts, raw reports,
samples, native memory reports, XPI bytes, public metadata and exact driver snapshots
for the final runs. The JSON summaries are LF-normalized views; packed raw bytes are
individually hashed. Windows browser stdout was not captured; empty log files do
not imply an error-free browser log. Earlier development runs bind source hashes
but do not all retain full source snapshots; final runs do.

Continue only from [the new handoff](win-continuation.md). No independent review
readiness, Feature Acceptance subject, merge, F02, product implementation, V6 migration,
AMO/signing/release or Production action is prepared.

STOP: WS-E01-F01_PARTIAL_QUALIFICATION__TARGET_ENVIRONMENT_REQUIRED.
