"""Deterministic synthetic metadata/workload, not a WindowSafe data model."""
import argparse
import hashlib
import json
from pathlib import Path


def compact(value):
    return json.dumps(value, ensure_ascii=False, separators=(',', ':'), sort_keys=True).encode()


def profile(size):
    if size not in (500, 2000): raise ValueError('bound profiles are R500 and R2000')
    windows = 10 if size == 500 else 20
    tabs = []
    for i in range(size):
        url = f'http://127.0.0.1:8000/article.html?synthetic={i:06d}&padding='
        url += 'x' * (160 - len(url.encode()))
        tabs.append({'syntheticId': i, 'window': i // (size // windows), 'url': url,
            'title': (f'Synthetic tab {i:06d} ' + 'x' * 80)[:80],
            'active': i % (size // windows) == 0, 'pinned': i % 10 == 1,
            'muted': i % 7 == 0, 'container': i % 4,
            'group': None if i % 10 == 1 else (i // 10)})
    checkpoints = []
    for checkpoint in range(14):
        changed = []
        for offset in range(size // 20):
            i = (checkpoint * (size // 20) + offset) % size
            row = dict(tabs[i]); row['title'] = (f'Checkpoint {checkpoint:02d} tab {i:06d} ' + 'x' * 80)[:80]
            changed.append(row)
        checkpoints.append({'checkpoint': checkpoint, 'changed': changed})
    closed = [{'window': i, 'tabs': [dict(tabs[(i * 31 + j) % size], syntheticId=size + i * 100 + j)
                 for j in range(50 if size == 500 else 100)]} for i in range(50)]
    return {'class': 'SYNTHETIC_FIXTURE_NOT_PRODUCT_SCHEMA', 'profile': f'R{size}',
            'tabs': tabs, 'H': {'checkpoints': checkpoints, 'closedWindows': closed}}


def schedule(kind):
    if kind == 'L10': return [{'ordinal': i, 'at_ms': i * 100} for i in range(6000)]
    if kind == 'B300': return [{'ordinal': i, 'at_ms': i * 3000 / 299} for i in range(300)]
    raise ValueError('unknown workload')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--output', type=Path, required=True); args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    for size in (500, 2000):
        data = compact(profile(size)); (args.output / f'R{size}-H.json').write_bytes(data)
        print(json.dumps({'profile': f'R{size}', 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
                          'evidence_class': 'LOCAL_STATIC_TOOLCHAIN', 'product_size_pass': False}))
    for kind in ('L10', 'B300'): (args.output / (kind + '.json')).write_bytes(compact(schedule(kind)))
