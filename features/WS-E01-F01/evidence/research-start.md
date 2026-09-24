# WS-E01-F01 – Current research snapshot (2026-09-19)

This is a starting research snapshot, not a substitute for the Coding Agent's own current-source
verification and runtime qualification.

## Firefox target

- Firefox 156 Stable was released 2026-09-15.
- Its published add-on-developer release note does not introduce a WindowSafe-relevant API
  contract change beyond the listed theme change.
- Firefox MV3 still uses background scripts/pages as Event Pages; `background.service_worker`
  is not supported.

Primary sources:
- https://developer.mozilla.org/en-US/docs/Mozilla/Firefox/Releases/156
- https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/manifest.json/background

## Persistent restart testing

Mozilla's Extension Workshop documents that temporary extensions, including `web-ext` temporary
runs, are unloaded at Firefox restart. It recommends a fixed add-on ID and persistent test
installation; signature enforcement may be disabled only in appropriate test builds/profiles.

Source:
- https://extensionworkshop.com/documentation/develop/testing-persistent-and-restart-features/

## Node

As of 2026-09-19:
- Node 24 (Krypton) is LTS.
- latest listed v24 release: 24.21.0.
- Node 26 is Current, not LTS.

Source:
- https://nodejs.org/en/about/previous-releases

## web-ext

Current candidate checked from Mozilla's repository:
- web-ext 10.6.0, released 2026-08-04.
- package engine: Node >=20, npm >=8.
- release notes say `web-ext lint` added a Firefox 154.0b4 schema.

Consequence:
- 10.6.0 is the current tool candidate;
- lint is useful but cannot be the sole Firefox-156 qualification oracle.

Source:
- https://github.com/mozilla/web-ext/releases/tag/10.6.0

## TypeScript

- TypeScript 7.0 is stable; current npm latest observed: 7.0.2.
- TS7 is the new native compiler and 7.0 does not expose the old compiler API.
- CLI-only WindowSafe usage may fit well, but actual supporting-tool compatibility must be tested.
- If a real tool needs the TS6 programmatic API, Microsoft documents side-by-side TS6 support;
  do not downgrade silently.

Sources:
- https://devblogs.microsoft.com/typescript/announcing-typescript-7-0/
- https://www.npmjs.com/package/typescript

## WebExtension TypeScript declarations

Observed candidates:
- `@types/firefox-webext-browser` latest published package observed as 143.0.0, older than the
  Firefox-156 target.
- `@types/webextension-polyfill` observed as 0.12.6 and recently updated, but its module/type
  shape must be checked against native Firefox-only use and the exact APIs WindowSafe needs.
- The `webextension-polyfill` runtime itself is not required for a Firefox-only product and its
  Mozilla repository was archived in 2026.

Consequence:
Do not equate a typings package with API truth. Compare the chosen type surface to Firefox-156
primary docs/schema/runtime and add the smallest local augmentation only if necessary.

Sources:
- https://www.npmjs.com/package/@types/firefox-webext-browser
- https://www.npmjs.com/package/@types/webextension-polyfill
- https://github.com/mozilla/webextension-polyfill

## GitHub Actions candidates

Current observed releases:
- `actions/setup-node` v7.0.0 -> commit `820762786026740c76f36085b0efc47a31fe5020`
- `actions/checkout` v7.0.1 -> commit `3d3c42e5aac5ba805825da76410c181273ba90b1`

The repository already has its own pinned Foundation workflow. Any new Node/qualification CI
workflow or update must preserve least privilege, exact commit pinning and no secrets.

These are candidates, not an instruction to rewrite existing historical workflow pins without
need.
