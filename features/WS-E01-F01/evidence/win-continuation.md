# Windows F01 continuation after WS-E01-F01-WIN-20260924-01

Use the exact delivery Head/Tree on feature/ws-e01-f01-qualification, PR #3
Draft/unmerged; repository ID 1374094477. Main must remain
3bdd7439c221b8f8c83e7374c8bb29898891a4fd. Verify a clean worktree/index and sole
branch writer before mutation. Authorization remains WS-EA-20260919-08.

Read state.json and [current report](win-qualification.md), then verify the new
inventory using its externally delivered SHA-256:

```sh
python qualification/ws-e01-f01/continuation.py --manifest features/WS-E01-F01/evidence/win-continuation-manifest.json --manifest-sha256 DELIVERY_MANIFEST_SHA256
```

Add --build only when build/f01/WS-E01-F01-windows-continuation.zip does not exist.
The archive contains inputs/evidence/scripts, not browser binaries or profiles.
The manifest excludes itself; the external delivery hash binds it.

Lock SHA-256 remains
1d6f6b41f6a87d1890695247e6610f60199518b22e87f12f1ee1002661563834.
Use Python 3.14.4 and the existing pinned workspace toolchain; no dependency updates.
The unchanged Foundation inventory writer requires qualified POSIX no-follow/dir_fd
capabilities. Do not weaken that guard to make Windows build checks pass.

## Verified Windows replay

Recollect host/desktop identity. Use only the verified local installations bound by
win-stable-download.json and win-unbranded-download.json; reverify every installed file.
Never execute the installer or use installed system Firefox or a real profile.
Official Stable source is the bound Mozilla installer URL/checksums. Extract its
embedded 7z payload (observed offset 131665) into a fresh workspace directory using
Windows tar; validate members for traversal before extraction. Unbranded is the
exact Mozilla Taskcluster target.zip; check SHA-256, official checksums, metadata
and full installation before running. Paths below refer to this host's retained
workspace artifacts; a new host must obtain and verify its own copies.

```powershell
python -m unittest discover -s tests -p test_windows_job.py -v
python qualification/ws-e01-f01/windows_job_dry_run.py
python qualification/ws-e01-f01/run_probe.py --firefox build/f01/windows-download/stable/core/firefox.exe --firefox-sha256 ce320f543a353bb55c6804af320df0b7807eb3feb822ea093a1ae7164c066970
python qualification/ws-e01-f01/target_probe.py --firefox build/f01/windows-download/stable/core/firefox.exe --firefox-sha256 ce320f543a353bb55c6804af320df0b7807eb3feb822ea093a1ae7164c066970
python qualification/ws-e01-f01/run_probe.py --firefox build/f01/windows-download/unbranded/firefox/firefox.exe --firefox-sha256 9c7ddb862168fe2bc8f5ae93c6b6126f3c490c580de29e69572f4a75184e8a55 --release-equivalent-binding features/WS-E01-F01/evidence/win-unbranded-download.json --release-equivalent-binding-sha256 c939a23b2a891c27e3ac6719bea00e476919fed314cc6a8076086b19977d2496
```

## Remaining work

1. Establish a supported, Product-compatible special-window rule. Windows WebApp
   taskbar windows currently appear as normal to the extension API. A native chrome
   discriminator is not a product permission. Do not silently accept full support;
   keep affected implementation stopped if a material Product decision is required.
2. Execute Ubuntu enabled-WebApp and remaining geometry/display cases on Ubuntu
   Desktop. This host supplied Windows evidence only.
3. Qualify complete descendant identity coverage and final measurement intervals;
   do not treat sampled PID identities or lifetime Job totals alone as final proof.
4. Resolve cache/shared/native attribution and continuous addon hard-peak coverage
   on both OSes, with measured driver overhead and declared uncertainty. Keep
   whole-job commit/working-set/private/native-addon measures separate.

Exact 156 restart is now evidenced on both OSes. Three global gates remain OPEN:
WINDOWS_DESKTOP, SPECIAL_NATIVE_GUI_CASES, MEASUREMENT_FINAL_ATTRIBUTION.
Keep PARTIAL until all applicable evidence and mandatory checks converge; then
prepare independent technical review only. No acceptance subject, self-verdict,
merge, V6 migration, F02/product work, signing, release or Production.
