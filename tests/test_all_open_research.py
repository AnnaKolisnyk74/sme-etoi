"""Coverage, retrieval/claim separation and approval boundaries of the continuation."""
import csv
from collections import Counter
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from audit_source_links import inventory


def rows(path):
    with (ROOT / path).open(newline='', encoding='utf-8') as handle:
        return list(csv.DictReader(handle))


class AllOpenResearchTests(unittest.TestCase):
    def test_every_previously_open_field_has_exactly_one_attempt(self):
        baseline = rows('data/history/score_coding_proposals_before_all_open_20261008.csv')
        attempts = rows('evidence/field_research_all_open_20261008.csv')
        expected = {(r['company_id'], r['score_field']) for r in baseline
                    if r['proposal_status'] == 'NEEDS_RESEARCH'}
        actual = {(r['company_id'], r['score_field']) for r in attempts}
        self.assertEqual(actual, expected)
        self.assertEqual(len(attempts), len(actual))
        self.assertEqual(len(actual), 929)
        self.assertEqual(len({r['company_id'] for r in attempts}), 100)
        self.assertEqual(Counter(r['outcome'] for r in attempts),
                         {'NEW_EVIDENCE': 26, 'STILL_UNKNOWN': 870, 'SOURCE_ACCESS_LIMITED': 33})
        self.assertTrue(all(r['checked_by'] == 'Codex' for r in attempts))

    def test_access_errors_and_test_systems_cannot_support_new_values(self):
        attempts = rows('evidence/research_source_attempts_20261008.csv')
        by_id = {r['attempt_id']: r for r in attempts}
        self.assertEqual(len(by_id), len(attempts))
        self.assertEqual(len(attempts), 536)
        checks = {r['check_id']: r for r in rows('evidence/score_proposal_checks.csv')}
        sources = {r['source_id']: r for r in rows('evidence/source_register.csv')}
        for field in rows('evidence/field_research_all_open_20261008.csv'):
            linked = [by_id[rid] for rid in field['source_attempt_ids'].split(' | ')]
            self.assertTrue(all(r['company_id'] == field['company_id'] for r in linked))
            if field['outcome'] == 'NEW_EVIDENCE':
                self.assertEqual(checks[field['attempt_id']]['outcome'], 'NEW_EVIDENCE')
                for sid in field['reviewed_source_ids'].split(' | '):
                    fetched = next(r for r in linked if r['source_url'] == sources[sid]['source_link'])
                    self.assertEqual(fetched['content_review_status'], 'SELECTED_ANCHOR_RECHECK')
                    self.assertFalse(fetched['retrieval_error'])
                    self.assertRegex(fetched['content_sha256'], r'^[0-9a-f]{64}$')
            else:
                self.assertTrue(field['remaining_fact'])
        self.assertTrue(any(r['content_review_status'] == 'TEST_SYSTEM_EXCLUDED' for r in attempts))
        self.assertTrue(any(r['content_review_status'] == 'FAILED' for r in attempts))

    def test_prior_checked_values_and_personal_review_are_preserved(self):
        baseline = rows('data/history/score_coding_proposals_before_all_open_20261008.csv')
        current = {(r['company_id'], r['score_field']): r for r in rows('data/score_coding_proposals.csv')}
        for old in baseline:
            new = current[old['company_id'], old['score_field']]
            if old['proposal_status'] == 'CHECKED':
                self.assertEqual(new, old)
            if new['proposal_status'] == 'NEEDS_RESEARCH':
                self.assertEqual((new['proposed_value'], new['proposal_confidence']), ('', 'UNKNOWN'))
            self.assertTrue(all(not new[f] for f in ['reviewer', 'review_date', 'review_note']))

    def test_discovery_pool_is_not_inspected_evidence_but_retrievals_are_audited(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'evidence').mkdir()
            (root / 'evidence/research_queries_example.csv').write_text(
                'company_id,discovered_urls,source_url\n'
                'P01,https://candidate.test/,https://cited.test/\n')
            (root / 'evidence/research_source_attempts_example.csv').write_text(
                'company_id,source_url\nP01,https://retrieved.test/\n')
            self.assertEqual(set(inventory(root)), {'https://cited.test/', 'https://retrieved.test/'})
