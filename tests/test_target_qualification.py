"""Qualification trust-boundary and non-overlapping memory accounting regressions."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'qualification/ws-e01-f01'))
from run_probe import digest, release_equivalent, verify_restart
from target_probe import memory_categories


class TargetQualificationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        self.folder = root / 'browser'; self.folder.mkdir()
        self.binary = self.folder / 'firefox'; self.binary.write_bytes(b'synthetic launcher')
        (self.folder / 'libxul.so').write_bytes(b'synthetic unsigned-compatible engine')
        self.binding = root / 'binding.json'
        self.record = {
            'version': '156.0', 'source_stamp': 'a80bd15ddee3b4bf3679aeba340e9d2db933c467',
            'source_repository': 'https://hg.mozilla.org/releases/mozilla-release',
            'task_state': 'completed', 'task_id': 'synthetic',
            'task_url': 'https://firefox-ci-tc.services.mozilla.com/api/queue/v1/task/synthetic',
            'task_name': 'build-linux64-add-on-devel/opt',
            'mozinfo': {'official': True, 'require_signing': False, 'release_or_beta': True,
                        'devedition': False, 'nightly_build': False},
            'chain_of_trust_artifact_hash_verified': True, 'binary_sha256': digest(self.binary),
            'installation_files': {p.name: digest(p) for p in self.folder.iterdir()},
        }

    def bind(self, record=None):
        self.binding.write_text(json.dumps(record or self.record))
        return digest(self.binding)

    def test_exact_full_installation_binding(self):
        self.assertEqual(release_equivalent(self.binary, self.binding, self.bind()), self.record)

    def test_same_launcher_different_engine_fails(self):
        pin = self.bind()
        (self.folder / 'libxul.so').write_bytes(b'synthetic signed-only engine')
        with self.assertRaisesRegex(ValueError, 'installation drift'):
            release_equivalent(self.binary, self.binding, pin)

    def test_added_installation_file_fails(self):
        pin = self.bind(); (self.folder / 'extra').write_bytes(b'extra')
        with self.assertRaisesRegex(ValueError, 'installation drift'):
            release_equivalent(self.binary, self.binding, pin)

    def test_unbound_or_changed_record_fails(self):
        pin = self.bind(); self.binding.write_text(self.binding.read_text() + '\n')
        for bad in [None, pin]:
            with self.assertRaisesRegex(ValueError, 'binding hash'):
                release_equivalent(self.binary, self.binding, bad)

    def test_wrong_target_or_origin_fails_even_with_matching_record_hash(self):
        for key, value in [('version', '157.0'), ('source_stamp', '0' * 40),
                           ('task_url', 'https://example.invalid/task/synthetic'),
                           ('task_state', 'failed')]:
            with self.subTest(key=key):
                record = copy.deepcopy(self.record); record[key] = value
                with self.assertRaises(ValueError):
                    release_equivalent(self.binary, self.binding, self.bind(record))
        for key, value in [('official', False), ('require_signing', True), ('devedition', True),
                           ('nightly_build', True), ('release_or_beta', False)]:
            with self.subTest(key=key):
                record = copy.deepcopy(self.record); record['mozinfo'][key] = value
                with self.assertRaises(ValueError):
                    release_equivalent(self.binary, self.binding, self.bind(record))

    def test_reporter_summary_excludes_duplicate_trees_and_instrumentation(self):
        rows = [dict(path=p, units=u, amount=n) for p,u,n in [
            ('explicit/window/origin/js-realm/objects',0,100),
            ('explicit/window/origin/dom/element-nodes',0,50),
            ('explicit/window/origin/layout/frames',0,20),
            ('explicit/window/origin/[anonymous sandbox]/js-realm/objects',0,80),
            ('js-main-runtime/origin/objects',0,100),
            ('explicit/window/other/js-realm/objects',0,999),
            ('explicit/window/origin/dom/count',1,200),
        ]]
        result = memory_categories(rows, 'origin')
        self.assertEqual(result['explicit_origin_leaf_bytes'],
                         dict(js=100, dom=50, layout=20, other_explicit=0, driver_sandbox=80))
        self.assertFalse(result['hard_peak_qualified'])
        self.assertFalse(result['cache_separately_attributed'])
        self.assertEqual(sum(memory_categories(rows, '')['explicit_origin_leaf_bytes'].values()), 0)

    def test_restart_requires_real_startup_and_exact_prior_marker(self):
        marker = dict(run='synthetic', ordinal=1, trigger='onInstalled')
        reports = [dict(trigger='onInstalled', marker=marker),
                   dict(trigger='onStartup', marker=dict(run='synthetic', ordinal=2),
                        observations=[dict(name='previous-probe-marker', value=dict(syntheticMarker=marker))])]
        verify_restart(reports, 'synthetic')
        bad = copy.deepcopy(reports); bad[1]['trigger'] = 'onInstalled'
        with self.assertRaises(ValueError): verify_restart(bad, 'synthetic')
        bad = copy.deepcopy(reports); bad[1]['observations'][0]['value']['syntheticMarker']['run'] = 'foreign'
        with self.assertRaises(ValueError): verify_restart(bad, 'synthetic')


if __name__ == '__main__': unittest.main()
