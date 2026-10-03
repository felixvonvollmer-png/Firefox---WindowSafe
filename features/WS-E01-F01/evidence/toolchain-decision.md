# Toolchain decision / supply chain

Evidence class: LOCAL_STATIC_TOOLCHAIN. Reversible qualification decision, no product dependency.

Exact pins: Node 24.21.0, bundled npm 11.19.0, TypeScript 7.0.2,
web-ext 10.6.0, @types/firefox-webext-browser 143.0.0; scoped override
addons-linter -> image-size 2.0.4. All are dev-only. package-lock v3 SHA-256:
`1d6f6b41f6a87d1890695247e6610f60199518b22e87f12f1ee1002661563834`.

Node official linux-x64 archive SHA-256:
`fd8e59d5a511510f6a298afb548f18c7d2b1be404d8b4a27d94fbe49f56cb2d6`;
win-x64 archive pin from the same official SHASUMS256.txt:
`158f7685b44de51f6c0df1d153526cbcd3e1bc739a8dfc607721cef75de9e541`.
`toolchain.py --setup` downloads only into build/f01 and runs npm ci --ignore-scripts.
No global install, sudo, shell/profile edits or production dependencies. No bundler/framework.
Windows-specific optional TS7 native binaries are retained in the cross-platform lock.

The initial npm audit reported two image-size <=2.0.2 parser DoS advisories, propagated to
addons-linter and web-ext (three high-severity dependency nodes). It is retained in
[supply-chain-initial-audit.json](supply-chain-initial-audit.json).
An exact patch-level override to 2.0.4 retains the web-ext candidate and its linter API.
Final [audit](supply-chain-final-audit.json) has zero findings. Lint, valid PNG parsing and
bounded malformed zero-length ICNS rejection qualify the override locally. Inspected installed
ICNS/HEIF parser code includes length/progress guards. An attempted raw upstream tag URL returned
HTTP error; it is recorded as unavailable, not used as proof. Registry integrity and signatures,
installed source inspection and executable checks are the evidence here.

Primary advisory locators:
- https://github.com/advisories/GHSA-w3rx-r6r6-pgpr
- https://github.com/advisories/GHSA-5p2g-fcmc-qvqq

Registry signature verification: 332 packages; 34 attestations, as reported by
[npm audit signatures](supply-chain-signatures.md). This does not assert every package has a
publisher provenance attestation. Exact versions, registry URLs, SRI and declared licenses:
[dependency inventory](dependency-inventory.json). Node MIT; TypeScript Apache-2.0;
web-ext/addons-linter MPL-2.0; declaration package and image-size MIT. Transitive alternative
licenses remain recorded verbatim; no source is copied into a WindowSafe release. Registry
license metadata is provenance, not a legal approval. Toolchain-only deprecation notices for
whatwg-encoding and ESLint remain visible in the installation output; audit found no advisory
for those resolved versions. Future upgrades require requalification, not silent latest pins.

Native Firefox declarations were selected over webextension-polyfill module declarations:
Firefox-only global browser APIs match the probe; no runtime shim is required. Both candidates
were queried (143.0.0 vs 0.12.6); declarations are not API truth. Group APIs are present; the
newer splitViewId field uses a narrow optional structural observation. No native split creation
API is invented. Full type-surface equivalence to Firefox 156 is not asserted.

TS7 CLI compilation succeeds. Initial config needed module=preserve (none is unsupported)
and an explicit rootDir; no supporting tool needs the old TS compiler API, so a TS6 fallback
was unnecessary. Two compilations produce identical JavaScript. web-ext lint passes both probe
manifests after shortening the qualification name. web-ext's Firefox 154-era schema is only a
supplement; actual Firefox 156 observations are separate evidence.

Bootstrap/check commands from repository root:

```sh
python3 qualification/ws-e01-f01/toolchain.py --setup
python3 qualification/ws-e01-f01/toolchain.py
```

The installer and CI run only static compiler/lint/security checks. They do not prove native
Windows Desktop browser behavior, restart or product performance.
