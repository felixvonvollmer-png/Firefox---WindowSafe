# WS-E01-F01 – Browser / Profile / Runtime Test Envelope

## Allowed environment

- Synthetic disposable Firefox profiles created specifically for F01.
- Synthetic localhost pages and locally generated test data.
- Official Firefox 156 Stable for target runtime checks.
- Official Mozilla unbranded Release-equivalent / Developer / Nightly test build only when a
  persistent restart test cannot legally/technically be performed on signed Stable.
- Stable deterministic test add-on ID for restart evidence.

## Hard prohibitions

- Do not open, copy, inspect, modify or reuse the user's normal Firefox profile.
- Do not read real history, cookies, sessions, bookmarks, passwords, tabs or backups.
- Do not sign in to Firefox Sync or any website/account.
- Do not upload/sign through AMO and do not use Mozilla credentials.
- Do not globally disable signature enforcement.
- Do not change the user's installed Firefox preferences.
- Do not kill or close unrelated Firefox processes.
- Do not use content scripts or host permissions to inspect real webpages.
- Do not turn qualification probes into WindowSafe product implementation.

## Process isolation

Every browser launch must record:
- binary path/version/build ID;
- profile path;
- launcher PID and process-tree membership;
- created temp/output paths;
- exact probe package hash.

Only processes demonstrably spawned for this test may be terminated/cleaned.

If isolation from an already-running Firefox cannot be proven, STOP that runtime probe.

## Test-only permissions

A separate helper probe may request permissions not intended for WindowSafe only to synthesize a
required condition. Example: `tabHide` to create a hidden tab for observation by the WindowSafe
capability probe.

Each such permission must be labeled `TEST_ONLY`, isolated to the helper manifest and excluded
from the product permission-direction record.

## Persistence/restart

Temporary extensions disappear at Firefox restart. Restart evidence therefore requires a
persistent test installation path and fixed add-on ID.

Permitted only in a disposable profile on an appropriate Mozilla test build:
`xpinstall.signatures.required=false`.

This is not permission to disable signing in the user's normal Firefox or to distribute an
unsigned add-on.

## Network

Prefer localhost synthetic pages. External network requests from test pages are unnecessary and
should be absent.

Network access for obtaining exact official tool/browser binaries and npm dev dependencies is
allowed by the execution authorization. Record package/binary provenance and hashes where
available.

## Evidence labels

Keep evidence classes explicit:
- PRIMARY_DOCUMENTATION
- LOCAL_STATIC_TOOLCHAIN
- UBUNTU_RUNTIME_VERIFIED
- WINDOWS_RUNTIME_VERIFIED
- SYNTHETIC_DRY_RUN_MEASUREMENT
- CI_VERIFIED
- NOT_EXECUTED / OPEN

Documentation is never relabeled as runtime evidence.
