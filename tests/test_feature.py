"""Fail-closed feature lifecycle and synthetic qualification invariants."""
import copy
import importlib.util
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import foundation as f


class FeatureTests(unittest.TestCase):
    def setUp(self):
        self.data = {p.relative_to(f.ROOT).as_posix(): p.read_bytes() for p in f.files(f.ROOT)}
        self.base = '3bdd7439c221b8f8c83e7374c8bb29898891a4fd'
        self.prefix = 'features/WS-E01-F01/'

    def check(self):
        def read(p):
            if p not in self.data: raise FileNotFoundError(p)
            return self.data[p]
        f.feature_check(f, self.data, read, self.base)

    def test_exact_start_and_accepted_epic(self):
        self.check()

    def test_supplied_originals_immutable(self):
        for name in f.FEATURE_ORIGINALS:
            with self.subTest(name=name):
                old = self.data[self.prefix + name]
                self.data[self.prefix + name] = old + b'\n'
                with self.assertRaises(f.Invalid): self.check()
                self.data[self.prefix + name] = old

    def test_missing_or_rewritten_authority(self):
        p = self.prefix + 'evidence/execution-authorization.json'; old = self.data.pop(p)
        with self.assertRaises(f.Invalid): self.check()
        self.data[p] = old + b'\n'
        with self.assertRaises(f.Invalid): self.check()

    def test_orphan_other_feature(self):
        self.data['features/WS-E01-F02/start.json'] = b'{}'
        with self.assertRaises(f.Invalid): self.check()

    def test_no_self_acceptance_or_lower_risk(self):
        p = self.prefix + 'state.json'; original = json.loads(self.data[p])
        for key, value in [('risk_class', 'LOW'), ('independent_technical_review', 'PASS'),
                           ('feature_acceptance_review', 'PASS'), ('product_implementation_started', True),
                           ('status', 'READY_FOR_ACCEPTANCE_REVIEW'), ('status', 'WS-E01-F01_READY_FOR_INDEPENDENT_TECHNICAL_REVIEW'), ('evidence_paths', [])]:
            with self.subTest(key=key):
                modified = dict(original); modified[key] = value
                self.data[p] = json.dumps(modified).encode()
                with self.assertRaises(f.Invalid): self.check()
        self.data[p] = json.dumps(original).encode()

    def test_premature_acceptance_subject_even_with_ready_claim(self):
        for status in ('IN_PROGRESS', 'READY_FOR_ACCEPTANCE_REVIEW'):
            self.data[self.prefix + 'subject.json'] = json.dumps({'status': status}).encode()
            with self.assertRaises(f.Invalid): self.check()

    def test_epic_binding_remains_immutable(self):
        self.data['epics/WS-E01/binding.json'] += b'\n'
        with self.assertRaises(f.Invalid): self.check()

    def test_product_and_arbitrary_paths_closed(self):
        for p in ['src/capture.ts', 'manifest.json', 'features/WS-E01-F01/capture.ts',
                  'features/../src/capture.ts', 'qualification/ws-e01-f02/probe/manifest.json',
                  'qualification/ws-e01-f01/src/capture.ts', 'qualification/ws-e01-f01/probe/recovery.ts']:
            with self.subTest(path=p), self.assertRaises(f.Invalid): f.scope(p)
        f.scope('qualification/ws-e01-f01/probe/manifest.json')

    def test_feature_evidence_append_only(self):
        p = self.prefix + 'evidence/synthetic.json'
        with self.assertRaises(f.Invalid): f.check_history_maps({p: b'first'}, {p: b'rewrite'})
        with self.assertRaises(f.Invalid): f.check_history_maps({p: b'first'}, {})


class SyntheticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.modules = {}
        for name in ('fixtures', 'measure'):
            spec = importlib.util.spec_from_file_location(name, f.ROOT / 'qualification/ws-e01-f01' / (name + '.py'))
            module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module); cls.modules[name] = module

    def test_bound_population_history_and_utf8_lengths(self):
        fixture = self.modules['fixtures']
        for size in (500, 2000):
            p = fixture.profile(size)
            self.assertEqual(size, len(p['tabs']))
            self.assertEqual(size, len({t['syntheticId'] for t in p['tabs']}))
            self.assertTrue(all(len(t['url'].encode()) == 160 and len(t['title']) == 80 for t in p['tabs']))
            self.assertEqual(14, len(p['H']['checkpoints']))
            self.assertTrue(all(len(c['changed']) == size // 20 for c in p['H']['checkpoints']))
            self.assertEqual(50, len(p['H']['closedWindows']))
            self.assertEqual(fixture.compact(p), fixture.compact(fixture.profile(size)))

    def test_load_windows(self):
        fixture = self.modules['fixtures']
        self.assertEqual(6000, len(fixture.schedule('L10')))
        self.assertEqual(599900, fixture.schedule('L10')[-1]['at_ms'])
        self.assertEqual(300, len(fixture.schedule('B300')))
        self.assertEqual(3000, fixture.schedule('B300')[-1]['at_ms'])

    def test_cpu_one_core_and_pid_reuse(self):
        rows = [{'monotonic': 10, 'processes': [{'pid': 1, 'identity': 'old', 'cpu_seconds': 20, 'rss_bytes': 100}]},
                {'monotonic': 12, 'processes': [{'pid': 1, 'identity': 'old', 'cpu_seconds': 21, 'rss_bytes': 100},
                                             {'pid': 2, 'identity': 'new', 'cpu_seconds': 1, 'rss_bytes': 50}]}]
        result = self.modules['measure'].summarize(rows)
        self.assertEqual(100, result['percent_one_core'])
        self.assertEqual(150, result['peak_sum_rss_bytes'])
        self.assertEqual('NOT_EVALUATED', result['product_performance_verdict'])

    def test_permission_separation(self):
        root = f.ROOT / 'qualification/ws-e01-f01'
        probe = json.loads((root / 'probe/manifest.json').read_text())
        helper = json.loads((root / 'helper/manifest.json').read_text())
        self.assertEqual('not_allowed', probe['incognito'])
        self.assertNotIn('host_permissions', probe)
        self.assertNotIn('tabHide', probe['permissions'])
        self.assertEqual({'tabs', 'tabHide'}, set(helper['permissions']))
        self.assertEqual({'scripts'}, set(probe['background']))


class FeatureHistoryCliTests(unittest.TestCase):
    """Run real current CLI over an exact-base disposable feature commit."""
    def setUp(self):
        import tempfile
        import subprocess
        self.subprocess = subprocess
        self.temp = tempfile.TemporaryDirectory(prefix='windowsafe-synthetic-feature-')
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name) / 'repo'
        subprocess.run(['git', 'clone', '--shared', '--no-checkout', str(f.ROOT), str(self.repo)], check=True, capture_output=True)
        self.git('checkout', '--detach', '3bdd7439c221b8f8c83e7374c8bb29898891a4fd')
        self.git('config', 'user.name', 'Synthetic Feature Fixture')
        self.git('config', 'user.email', 'synthetic@example.invalid')
        for source in f.files(f.ROOT):
            target = self.repo / source.relative_to(f.ROOT)
            target.parent.mkdir(parents=True, exist_ok=True); target.write_bytes(source.read_bytes())
        self.save()

    def git(self, *args):
        return self.subprocess.check_output(['git', '-C', str(self.repo), *args], stderr=self.subprocess.PIPE).decode().strip()

    def save(self):
        self.git('add', '--all')  # Only the newly created synthetic fixture.
        self.git('-c', 'commit.gpgsign=false', 'commit', '-m', 'synthetic feature history')

    def cli(self, *args, ok=True):
        result = self.subprocess.run([sys.executable, 'tools/foundation.py', *args], cwd=self.repo, text=True, capture_output=True)
        self.assertEqual(0 if ok else 1, result.returncode, result.stdout + result.stderr)

    def test_current_feature_keeps_original_epic_request_and_history(self):
        self.cli('check')
        self.cli('request', '--sha', 'HEAD', '--subject', 'epics/WS-E01/subject.json')
        self.cli('history', '--base', '3bdd7439c221b8f8c83e7374c8bb29898891a4fd')
        self.cli('history', '--base', '0000000000000000000000000000000000000000')

    def test_intermediate_original_rewrite_cannot_hide_behind_revert(self):
        p = self.repo / 'features/WS-E01-F01/evidence/research-start.md'; original = p.read_bytes()
        p.write_bytes(original + b'\n'); self.save()
        p.write_bytes(original); self.save()
        self.cli('history', '--base', '3bdd7439c221b8f8c83e7374c8bb29898891a4fd', ok=False)
