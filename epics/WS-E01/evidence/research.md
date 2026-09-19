# WS-E01 – Research Reuse / Delta Check

```text
EPIC_ID: WS-E01
EPIC_PREPARATION_ID: WS-E01-EP-20260919-01
DATE: 2026-09-19
STATUS: UPDATED
SCOPE: current primary-source delta + narrow open-source reference check
```

## Primary-source conclusions

1. **Firefox 156 current target remains valid.**
   MDN's Firefox 156 developer notes state release on 2026-09-15. The listed add-on-developer
   change concerns theme `backgrounds_area`; no material WindowSafe API change was identified.
   Consequence: keep Firefox Desktop 156 as target/reference; do not reopen T01.

   Source:
   https://developer.mozilla.org/en-US/docs/Mozilla/Firefox/Releases/156

2. **Firefox MV3 Event Page architecture remains correct.**
   MDN documents that Firefox does not support `background.service_worker`; MV3 background
   scripts/pages run nonpersistently as Event Pages.
   Consequence: keep Technical Foundation Event Page direction; state must survive suspension
   outside process memory.

   Sources:
   https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/manifest.json/background
   https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/Background_scripts

3. **Tab Groups are available but browser IDs are not durable identity.**
   `tabGroups` exposes group metadata/events; `tabs.group()` creates groups. MDN explicitly notes
   restored groups can receive different IDs.
   Consequence: preserve WindowSafe-owned stable group identity; never use native `groupId` as
   durable canonical identity.

   Sources:
   https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/tabGroups
   https://developer.mozilla.org/docs/Mozilla/Add-ons/WebExtensions/API/tabs/group
   https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/tabGroups/TabGroup

4. **Split View remains observational rather than fully recreatable.**
   Current MDN documents `splitViewId` and update/move observations, while explicit create/remove
   APIs remain under development.
   Consequence: retain the approved fallback: preserve relationship metadata; recreate native
   split only if a supported API is actually proven, otherwise restore ordinary tabs with visible
   limitation.

   Source:
   https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/Working_with_the_Tabs_API

5. **Restore-relevant tab creation properties remain documented.**
   `tabs.create()` exposes `cookieStoreId`, `discarded`, `muted`, `openInReaderMode`, `pinned`,
   index/window placement, and rejects unsupported privileged URLs.
   Consequence: these Product Truth fields remain technically plausible, but combinations must
   still be qualified on Firefox 156 before affected implementation.

   Source:
   https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/tabs/create

6. **Hidden/private/window-type handling still needs runtime qualification.**
   `tabs.Tab`/`tabs.query` expose hidden state and `windows.Window` exposes `incognito`.
   `windows.WindowType` documents `normal`, `popup`, `panel`, `devtools`, but does not by itself
   establish a safe classification for every Web-App/Picture-in-Picture case.
   Firefox's `incognito` manifest mode can deny private-window access entirely.
   Consequence: F01 must bind the safe window classifier and private-data exclusion strategy;
   Product Truth must not be weakened by assuming type coverage.

   Sources:
   https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/tabs/Tab
   https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/tabs/query
   https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/windows/Window
   https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/windows/WindowType
   https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/manifest.json/incognito

7. **Session values remain hints, not canonical storage.**
   `sessions.setWindowValue()` / `setTabValue()` associate extension-private values with current
   Firefox entities, but they are asynchronous browser-owned metadata.
   Consequence: retain Foundation rule that IndexedDB is canonical and Session values are hints.

   Sources:
   https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/sessions/setWindowValue
   https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/sessions/setTabValue

8. **Backup lifecycle assumptions remain valid.**
   Downloads accept a relative filename below the default downloads directory; `downloads.onChanged`
   exposes completion/state changes; `downloads.removeFile()` deletes the known downloaded file
   but not its history record.
   Consequence: keep completion-gated backup success and conservative known-ID cleanup.

   Sources:
   https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/downloads/download
   https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/downloads/onChanged
   https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/downloads/removeFile

9. **Restart evidence cannot rely on a temporary add-on.**
   Mozilla documentation states temporary installations remain only until Firefox restarts.
   Consequence: F01 must bind a suitable persistent test-install path in disposable profiles
   before native restart/restore evidence is attempted.

   Sources:
   https://extensionworkshop.com/documentation/develop/temporary-installation-in-firefox/
   https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/Your_first_WebExtension

10. **Performance tooling is available, but the project still needs its own bound A/B method.**
    Firefox Profiler supports local capture/analysis/comparison; Mozilla performance tooling also
    supports Gecko profiling with extensions. These references do not directly prove WindowSafe's
    T02/T05-R2 methodology.
    Consequence: F01 defines exact OS/browser/hardware/process-attribution and paired-run method
    rather than copying a generic profiler recipe.

    Sources:
    https://profiler.firefox.com/docs/
    https://firefox-source-docs.mozilla.org/testing/perfdocs/webextension.html

## Open-source / reuse delta

- Mozilla `mdn/webextensions-examples` is maintained by Mozilla's Add-ons team and includes
  small reference examples such as session-state, tabs-tabs-tabs and window-manipulator.
  Use: **REFERENCE_OR_CONCEPTUAL_ADAPTATION** for API idioms only.
  Source: https://github.com/mdn/webextensions-examples

- `Drive4ik/simple-tab-groups` demonstrates a mature Firefox tab-group extension with backup,
  containers and sessions, but its product model and permission envelope are materially broader
  than WindowSafe (including tab hiding, broader host access and optional Native Messaging).
  Use: **NO_COMPONENT_ADOPTION_BY_DEFAULT**; it is not an architecture substitute and no code is
  copied by this Preparation.
  Source: https://github.com/drive4ik/simple-tab-groups

## Net result

```text
MATERIAL_PRODUCT_DELTA: NONE
MATERIAL_FOUNDATION_DELTA: NONE
REFERENCE_OR_CONCEPTUAL_ADAPTATION: Mozilla WebExtension examples only
PROPOSE_COMPONENT: NONE
JUSTIFIED_CUSTOM_IMPLEMENTATION: YES, within the already approved lean Firefox-only architecture
PREIMPLEMENTATION_RUNTIME_QUALIFICATION_STILL_REQUIRED: YES
```
