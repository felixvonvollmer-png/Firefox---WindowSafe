"""Verify/build exact F01 continuation inputs. Never launches a browser implicitly."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = 'features/WS-E01-F01/evidence/continuation-manifest.json'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--manifest-sha256', required=True)
    parser.add_argument('--build', action='store_true')
    args = parser.parse_args()
    raw = (ROOT / MANIFEST).read_bytes()
    if hashlib.sha256(raw).hexdigest() != args.manifest_sha256: raise ValueError('continuation manifest hash mismatch')
    binding = json.loads(raw)
    payloads = {MANIFEST: raw}
    for name, exact in binding['files'].items():
        path = ROOT / name
        if path.is_symlink() or not path.resolve().is_relative_to(ROOT): raise ValueError('unsafe continuation path')
        content = path.read_bytes()
        if len(content) != exact['bytes'] or hashlib.sha256(content).hexdigest() != exact['sha256']:
            raise ValueError('continuation input mismatch: ' + name)
        payloads[name] = content
    result = {'status': 'HASH_BOUND_INPUTS_VERIFIED', 'files': len(payloads), 'runtime_evidence': False}
    if args.build:
        target = ROOT / 'build/f01/WS-E01-F01-continuation.zip'
        with zipfile.ZipFile(target, 'x') as archive:
            for name, content in sorted(payloads.items()):
                info = zipfile.ZipInfo(name, (2026, 9, 19, 0, 0, 0)); info.external_attr = 0o100644 << 16
                archive.writestr(info, content)
        result.update(archive=str(target), archive_sha256=hashlib.sha256(target.read_bytes()).hexdigest())
    print(json.dumps(result))


if __name__ == '__main__': main()
