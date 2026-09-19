# F01 target qualification: partial, no acceptance

Run WS-E01-F01-TARGET-QUAL-20260919-01 under [WS-EA-08](target-authorization.json),
starting at 0f83be2550f34698fe95da4df88b5eb918649973, tree
2db2d133b8aeb43f8ce7444d6192e55aa2d49c12. Main and the exact lockfile remain unchanged.
The [machine-readable record](target-qualification.json) binds host, methods, sources and limits.
All historical evidence remains byte-identical. This is Coding-Agent evidence, not independent review.

## Executed hosts and scopes

Ubuntu host felix-A320M-S2H-V2: Ubuntu Desktop 26.04.1 LTS, Linux 7.0.0-31-generic,
x86_64, GNOME/Wayland, visible 1920x1080 display. Stable Firefox 156.0 build
20260909172920 executed native fixtures. No Windows Desktop was provided, as explicitly
confirmed by the user. Windows Server CI remains static evidence only.

| Gate | Ubuntu actual evidence | Windows |
|---|---|---|
| WINDOWS_DESKTOP | Not applicable | OPEN: no host/build/runtime |
| SPECIAL_NATIVE_GUI_CASES | Native private, detached DevTools, PiP and real Split View observed; interactions expanded. Enabled WebApp classification and multi-monitor/state coverage incomplete. | OPEN: not executed |
| TARGET_EQUIVALENT_RESTART | Official unbranded release-equivalent 156: real onStartup and marker 1 -> 2, clean exits and profile removal | OPEN: not executed |
| MEASUREMENT_FINAL_ATTRIBUTION | Native origin JS/DOM leaves + same-run OS counters; cache/shared separation and hard peak still OPEN | OPEN: no Job accounting/attribution run |

## Native fixtures and API observations

[Final native record](target-ubuntu-native-memory.json) is UBUNTU_RUNTIME_VERIFIED.
The temporary qualification extension has a fixed synthetic ID and incognito:not_allowed.
Privileged chrome automation creates the actual native fixtures in the owned process;
the extension document independently calls WebExtension APIs. These chrome commands are
TEST_ONLY and are not product API capabilities or evidence of a general creation API.

- The normal Firefox private-window command produced a native private window; extension
  windows.getAll/tabs.query still excluded it. This is automated native-command evidence,
  not a claimed human manual interaction.
- Detached DevTools had native type devtools:toolbox and was absent from extension windows.
- A localhost canvas-generated video produced Toolkit:PictureInPicture; it too was absent
  from extension windows. No external media was fetched.
- A native split contained two tabs sharing splitViewId=1. Both emitted actual onUpdated
  changes with splitViewId=1. This does not establish a public split-creation API.
- Active/discarded/pinned/muted/custom-container/group combinations ran. Active+discarded
  and pinned+discarded creation rejected. Grouping a pinned tab visibly unpinned it: do not
  assume both intents can survive the same operation unchanged. Reader+container+group
  was observed. A removed custom container ID rejected. Fresh profiles reused numerical
  custom container IDs; IDs alone are not cross-profile identity.
- WebApp/taskbar-tabs was disabled in the tested default profile. The absence of its UI is
  not proof that the implementation cannot exist or be enabled. Enabled-mode classification
  stays open; no OS pin/install/default changes were performed.

## Exact 156 restart

[Official build provenance](target-unbranded-download.json) binds Mozilla task
fXVSnCllT3yplCRhcnFWYw at release source a80bd15ddee3b4bf3679aeba340e9d2db933c467,
version 156.0/build 20260909172920, official=true, release_or_beta=true,
require_signing=false. It is not Developer 157. Archive SHA-256:
214dad1f7e5569026e7222c2ddf2f975b06925e6f431580a9c58102578325c3a.
Official SHA-512 and chain-of-trust artifact digest match; no independent verification
of the chain-of-trust signature is claimed. All 47 extracted files are bound, because the
launcher executable alone has the same hash as Stable and cannot distinguish the engines.

[Final restart record](target-ubuntu-restart.json) binds both owned launcher PIDs/profiles,
fixed probe IDs/XPI hashes and cgroups. The signature pref changed only in that new synthetic
profile. Native graceful quit/relaunch yielded onInstalled/ordinal 1 then onStartup/ordinal 2;
the exact previous marker and synthetic session hint remained. Both exits were 0.
No timer is interpreted as restore completion. No Stable signing bypass or signing occurred.

## Memory/accounting result

SYNTHETIC_DRY_RUN_MEASUREMENT only: A with no addon, B with the idle extension document,
B with 4 MiB held typed-array data, 1000 DOM nodes and 1024 JS Map entries, then a 12 MiB pulse.
Native nsIMemoryReporterManager reports are the Firefox-native measurement evidence.
Only disjoint explicit origin leaves are reduced; duplicate summary trees and Marionette
sandbox allocations are kept separate. The final observed held totals were JS 5,042,664 bytes,
DOM 326,848 bytes and layout 838,480 bytes. These are fixture observations, not product limits.

The JS Map cache is not separately attributed. Native/shared residual is unknown. The pulse
was visible in a later report, but this cannot prove coverage of arbitrary shorter peaks.
The browser advertised jsallocations but not nativeallocations profiling support; no continuous
allocation trace was qualified. cgroup memory.peak measures the whole charged process tree,
not an addon-only peak. Sequential same-process A/B also has startup/order/background and
instrument overhead confounders. MEASUREMENT_FINAL_ATTRIBUTION remains OPEN.

Windows Job Object assignment, lifetime CPU/I/O, process identity, nesting/breakaway tests,
memory semantics and hard-peak attribution were neither implemented nor executed here.
Existing sampled Windows process diagnostics are not an equivalent fallback.

## Reproducibility, validation and next step

[Exact runtime artifact pack](target-runtime-artifacts.json) preserves all five synthetic
runs, including development observations, native memory reports, XPIs, logs, samples and
official public build metadata. Each gzip-base64 entry binds original bytes, length and SHA-256.
Every owned profile was removed and every owned cgroup was absent at final verification.
The first restart's cumulative PID diagnostic was corrected to per-launch scope; its original
evidence remains retained. Final restart also fails closed without real onStartup/prior-marker proof.

See [local checks](target-local-verification.json) and the
[hash-bound continuation](target-continuation.md). Exact post-push CI is reported at the new
Head; green CI cannot qualify Windows Desktop. Risk remains ELEVATED. Independent general
technical review is pending until qualification convergence; Feature Acceptance is NOT_READY.
No final V6 migration, product work, F02, independent verdict, merge, signing or release.

STOP: WS-E01-F01_PARTIAL_QUALIFICATION__TARGET_ENVIRONMENT_REQUIRED.
