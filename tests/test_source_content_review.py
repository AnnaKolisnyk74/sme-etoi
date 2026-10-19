"""Offline regressions for source identity, boundaries and complete coverage."""
import csv
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
import source_content_review as review


class SourceContentReviewTests(unittest.TestCase):
    def test_inventory_coverage_includes_excluded_candidates_and_is_not_approval(self):
        self.assertEqual(review.validate(ROOT), [])
        result = review.build(ROOT)
        self.assertEqual(result['coverage_status'], 'COMPLETE')
        self.assertEqual(result['registered_source_count'], 677)
        self.assertEqual(result['assessed_source_count'], 677)
        self.assertEqual(result['missing_source_ids'], [])
        self.assertEqual(result['human_review_status'], 'PENDING')
        self.assertEqual(len(review.new_checks(ROOT)), 231)
        self.assertEqual(len(result['boundary_sources']), 63)
        # A current Chinese quality holder is not the sampled German entity.
        foreign = review.checks(ROOT)['S-P87-04']
        self.assertEqual(foreign['content_review_status'], 'CONTEXT_ONLY')
        self.assertIn('2029', foreign['scope_note'])

    def copy_and_mutate(self, change):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        shutil.copytree(ROOT / 'evidence', root / 'evidence')
        shutil.copytree(ROOT / 'data', root / 'data')
        path = root / 'evidence/source_content_checks_20261012.csv'
        with path.open() as f:
            rows = list(csv.DictReader(f))
        fields = list(rows[0])
        change(rows)
        with path.open('w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader(); writer.writerows(rows)
        return root

    def test_dropped_record_reopens_coverage_and_fails_preflight(self):
        root = self.copy_and_mutate(lambda rs: rs.pop(0))
        self.assertEqual(review.build(root)['coverage_status'], 'INCOMPLETE')
        self.assertEqual(review.build(root)['missing_source_count'], 1)
        self.assertTrue(any('missing' in e for e in review.validate(root)))

    def test_newer_technical_body_review_supersedes_inventory_pass_by_timestamp(self):
        older = review.new_checks(ROOT)['S-P50-07']
        newest = review.checks(ROOT)['S-P50-07']
        self.assertGreater(newest['checked_at'], older['checked_at'])
        self.assertIn('printed pages18–21', newest['relevant_location'])
        self.assertIn('keinen abgeschlossenen Speicher', newest['scope_note'])
        self.assertIn('geplante Sudhaussteuerung', newest['scope_note'])
        # File category order cannot hide a newer technical review.
        self.assertNotEqual(newest['scope_note'], older['scope_note'])

    def test_wrong_entity_url_and_missing_body_fingerprint_fail_closed(self):
        def change(rs):
            rs[0]['company_id'] = 'P99'
            rs[1]['source_url'] = 'https://unrelated.invalid/'
            rs[2]['content_sha256'] = ''
        root = self.copy_and_mutate(change)
        errors = review.validate(root)
        self.assertEqual(sum('mismatched' in e for e in errors), 2)
        self.assertTrue(any('fingerprint' in e for e in errors))

    def test_context_and_unavailable_require_boundaries_without_human_approval(self):
        def change(rs):
            context = next(r for r in rs if r['content_review_status'] == 'CONTEXT_ONLY')
            context['remaining_gap'] = ''
            context['reviewer'] = 'Invented approval'
            unavailable = next(r for r in rs if r['content_review_status'] == 'UNAVAILABLE')
            unavailable['retrieval_status'] = 'RETRIEVABLE'
        root = self.copy_and_mutate(change)
        errors = review.validate(root)
        self.assertTrue(any('boundary' in e for e in errors))
        self.assertTrue(any('human review' in e for e in errors))
        self.assertTrue(any('claimed retrievable' in e for e in errors))
