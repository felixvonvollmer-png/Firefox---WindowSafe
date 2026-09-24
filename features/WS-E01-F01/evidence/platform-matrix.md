# F01 platform qualification matrix

Status: PARTIAL. Ubuntu Desktop 26.04.1 / Firefox 156.0 / build 20260909172920
is the executed Stable target. Windows Desktop is NOT_EXECUTED for every row.
The separate Developer Edition 157.0b3 archive reports application version 157.0,
build 20260918091356; it proves test-install/restart mechanics only.

Evidence: [Stable](ubuntu-stable-cgroup.json), [test-build restart](ubuntu-restart-cgroup.json),
[original probe packages](runtime-artifacts.json), [primary sources](primary-sources.json).
OBSERVED means an actual returned value, not an independent PASS.

| Area / source API | Ubuntu Stable evidence / supported boundary | Safe handling / remaining gate |
|---|---|---|
| MV3 Event Page | Actual onInstalled probe executes background scripts; no service worker | Keep Firefox event page direction. No product manifest exists. |
| Normal / popup, windows.create | Returns normal / popup respectively | Ordinary type distinction proven only for these cases. |
| DevTools / Web-App / PiP | NOT_EXECUTED native special-window fixtures | OPEN: do not equate all type=normal windows with eligible ordinary windows. No capture implementation until safe classification on target environments. |
| Private mode | isAllowedIncognitoAccess=false; inIncognitoContext=false; private window creation rejected | Keep incognito:not_allowed and context checks. A manually created private window exclusion test remains in the native GUI continuation. |
| Foreign hidden tabs | Separate TEST_ONLY helper hides one localhost tab; main probe sees hidden=true | Hidden is not absent or private; do not reproduce foreign hide rules. |
| Containers / cookieStoreId | Existing container-1 supports discarded synthetic tab; invalid container ID rejected | Never create/delete containers in product. Missing container must remain unresolved/visible. |
| Cross-profile identity | Independent fresh profiles have the same default container-1 identifier | Numerical equality is not provenance; no cross-profile rebinding inferred. Custom container collision/missing cases remain in continuation. |
| Native groups | group/update/query round trip observed, title/color and membership preserved during run | Group ID is an ephemeral hint. MDN does not guarantee ID reuse on restoration. The restored group retained its ID in the observed testbuild restart; no stable durable identity claim. |
| Split View | split constant exists, ordinary tabs report splitViewId=-1; MDN describes observation without general creation/removal API | Record intent; preserve tabs independently with visible limitation. Actual split membership/onUpdated combination remains OPEN. |
| Reader mode | openInReaderMode followed by bounded single-navigation completion reports isInReaderMode=true | Store intent, never infer original address from page content. Reader/container/group combinations remain OPEN. |
| discarded / pinned / muted | Six valid combinations observed; both pinned+discarded create requests reject | Preserve pin/mute intent; cannot promise a pinned tab can be created unloaded. No fallback that eagerly loads all pages. Active/container/group combinations require remaining tests. |
| Privileged URLs | chrome://browser/content/browser.xhtml rejected | Preserve original address as inert metadata in future product; only validated opening on explicit action. No javascript/data/external-handler probes. |
| Geometry/state | Request 800x600 returned 852x652 (OS decorations/constraints); normal state observed; bounds-change event unavailable | Leave safe position to Firefox/OS when screen bounds cannot be qualified. Do not promise exact geometry; no polling workaround. Multi-monitor/minimized/maximized cases OPEN. |
| sessions tab/window values | Both setters/getters return synthetic marker | Hints only; no recovery store. Testbuild restart retains a tab marker; no exact 156 persistence claim. |
| startup/restart/native restore | Developer onStartup runs after persistent installation; ordinal increases 1 to 2, marker retained | Test-build-only restart mechanics. No restore-complete API established; no timer-based inference. Exact target-equivalent restart remains OPEN. |

All unresolved combinations keep the corresponding preimplementation gate closed.
No material Product boundary was weakened, and no unsupported case has been accepted.
The current limitation is incomplete qualification, not an inferred impossibility of Product Truth.
No technical or Feature Acceptance verdict is issued.

The initial Stable run is retained in [initial evidence](ubuntu-stable-initial.json).
Its helper attempted to inspect a tab before localhost navigation finished. The final probe
waits for that specific navigation with an explicit failure deadline. This deadline has no
native-restore semantics. The initial run also used an overlong qualification name, corrected
before final successful lint. It is not the final qualification subject.
