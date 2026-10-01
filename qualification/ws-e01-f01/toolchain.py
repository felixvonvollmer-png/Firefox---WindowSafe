"""Pinned user/workspace-only toolchain bootstrap and qualification checks."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tarfile
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[2]
SOURCE = Path(__file__).resolve().parent
BUILD = ROOT / 'build/f01'
NODE = '24.21.0'
PINS = {
    'linux-x64.tar.xz': 'fd8e59d5a511510f6a298afb548f18c7d2b1be404d8b4a27d94fbe49f56cb2d6',
    'win-x64.zip': '158f7685b44de51f6c0df1d153526cbcd3e1bc739a8dfc607721cef75de9e541',
}


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--setup', action='store_true'); args = parser.parse_args()
    import platform
    if platform.machine().lower() not in {'amd64', 'x86_64'} or platform.system() not in {'Windows', 'Linux'}:
        raise ValueError('only authorized x64 Windows/Ubuntu toolchain path is qualified')
    flavor = 'win-x64.zip' if os.name == 'nt' else 'linux-x64.tar.xz'
    name = 'node-v' + NODE + '-' + flavor
    folder = BUILD / name.removesuffix('.tar.xz').removesuffix('.zip')
    node = folder / ('node.exe' if os.name == 'nt' else 'bin/node')
    npm = folder / ('node_modules/npm/bin/npm-cli.js' if os.name == 'nt' else 'lib/node_modules/npm/bin/npm-cli.js')
    BUILD.mkdir(parents=True, exist_ok=True)
    if args.setup and not node.exists():
        payload = urllib.request.urlopen('https://nodejs.org/dist/v' + NODE + '/' + name, timeout=60).read()
        if hashlib.sha256(payload).hexdigest() != PINS[flavor]: raise ValueError('Node archive hash mismatch')
        archive = BUILD / name; archive.write_bytes(payload)
        if os.name == 'nt':
            with zipfile.ZipFile(archive) as z:
                for member in z.namelist():
                    if not (BUILD / member).resolve().is_relative_to(BUILD.resolve()): raise ValueError('archive path escape')
                z.extractall(BUILD)
        else:
            with tarfile.open(archive) as t: t.extractall(BUILD, filter='data')
    if subprocess.check_output([str(node), '--version'], text=True).strip() != 'v' + NODE: raise ValueError('Node pin')
    env = dict(os.environ, PATH=str(node.parent) + os.pathsep + os.environ.get('PATH', ''))
    if subprocess.check_output([str(node), str(npm), '--version'], text=True, env=env).strip() != '11.19.0': raise ValueError('npm pin')
    dev = BUILD / 'dev'; dev.mkdir(exist_ok=True)
    if args.setup:
        for name in ('package.json', 'package-lock.json'): shutil.copyfile(SOURCE / name, dev / name)
        subprocess.run([str(node), str(npm), 'ci', '--prefix', str(dev), '--ignore-scripts', '--no-fund', '--no-audit',
                        '--registry=https://registry.npmjs.org', '--cache', str(BUILD / 'npm-cache')], check=True, env=env)
    for name in ('package.json', 'package-lock.json'):
        if (SOURCE / name).read_bytes() != (dev / name).read_bytes(): raise ValueError('installed toolchain binding drift')
    tsc = dev / 'node_modules/typescript/bin/tsc'
    subprocess.run([str(node), str(tsc), '--project', str(SOURCE / 'tsconfig.json')], check=True, env=env)
    compiled = BUILD / 'compiled/background.js'; first = compiled.read_bytes()
    subprocess.run([str(node), str(tsc), '--project', str(SOURCE / 'tsconfig.json')], check=True, env=env)
    if compiled.read_bytes() != first: raise ValueError('nondeterministic TypeScript output')
    lint = BUILD / 'lint-probe'; lint.mkdir(exist_ok=True)
    shutil.copyfile(compiled, lint / 'background.js'); shutil.copyfile(SOURCE / 'probe/manifest.json', lint / 'manifest.json')
    (lint / 'config.js').write_text('const F01_CONFIG = {url: "http://127.0.0.1:8000/article.html", run: "static-lint"};\n')
    webext = dev / 'node_modules/web-ext/bin/web-ext.js'
    for kind, path in [('probe', lint), ('helper', SOURCE / 'helper')]:
        result = subprocess.run([str(node), str(webext), 'lint', '--source-dir', str(path), '--output', 'json'], capture_output=True, env=env)
        (BUILD / (kind + '-lint.json')).write_bytes(result.stdout)
        result.check_returncode()
    # Qualify the security override against a tiny local malformed ICNS input.
    script = """const {imageSize}=require(process.argv[1]);
const b=Buffer.alloc(16); b.write('icns'); b.writeUInt32BE(16,4); b.write('ic07',8);
let rejected=false; try { imageSize(b); } catch { rejected=true; }
if(!rejected) process.exit(1);
const png=Buffer.from('89504e470d0a1a0a0000000d4948445200000001000000010806000000','hex');
const size=imageSize(png); if(size.width!==1 || size.height!==1) process.exit(2);
"""
    subprocess.run([str(node), '-e', script, str(dev / 'node_modules/image-size')], check=True, env=env, timeout=5)
    audit = subprocess.run([str(node), str(npm), 'audit', '--prefix', str(dev), '--json', '--registry=https://registry.npmjs.org',
                            '--cache', str(BUILD / 'npm-cache')], capture_output=True, env=env)
    audit_data = json.loads(audit.stdout)
    if 'metadata' not in audit_data:
        audit_data = {'status': 'AUDIT_SERVICE_ERROR', 'http_status': audit_data.get('statusCode'), 'exit_code': audit.returncode}
    (BUILD / 'npm-audit-final.json').write_text(json.dumps(audit_data, indent=2) + '\n')
    if audit.returncode:
        print(json.dumps({'gate': 'NPM_AUDIT', 'exit_code': audit.returncode,
            'http_status': audit_data.get('http_status'),
            'vulnerabilities': audit_data.get('metadata', {}).get('vulnerabilities')}))
    audit.check_returncode()
    print(json.dumps({'toolchain': 'STATIC_CHECKS_PASS', 'lock_sha256': hashlib.sha256((SOURCE / 'package-lock.json').read_bytes()).hexdigest(),
                      'compiled_sha256': hashlib.sha256(first).hexdigest(), 'runtime_claim': False}))


if __name__ == '__main__': main()
