"""Existing electric joining is distinct from new load, current CAPEX and flexibility."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
import decision_research as d
from export_web_data import build_web_payload


class PlasticsJoiningFollowupTests(unittest.TestCase):
    def test_frozen_scope_single_closure_and_unchanged_670_checked_rows(self):
        before = {(p['company_id'], p['score_field']): p for p in d.rows(
            ROOT, 'data/history/score_coding_proposals_before_followup_20261019.csv')}
        now = {(p['company_id'], p['score_field']): p for p in d.rows(
            ROOT, 'data/score_coding_proposals.csv')}
        attempts = d.rows(ROOT, 'evidence/field_research_followup_20261019.csv')
        expected = {k for k, p in before.items() if k[0] in {'P23','P24','P33'}
                    and p['proposal_status'] == 'NEEDS_RESEARCH'}
        self.assertEqual(len(attempts), 23)
        self.assertEqual({(r['company_id'], r['score_field']) for r in attempts}, expected)
        closed = {(r['company_id'], r['score_field']) for r in attempts
                  if r['outcome'] == 'NEW_EVIDENCE'}
        self.assertEqual(closed, {('P33','process_electrification_score')})
        checked = [k for k,p in before.items() if p['proposal_status'] == 'CHECKED']
        self.assertEqual(len(checked), 670)
        for k in checked:
            self.assertEqual(now[k], before[k])
        for k in expected - closed:
            self.assertEqual((now[k]['proposed_value'],now[k]['proposal_confidence']),('', 'UNKNOWN'))
        changed = {k for k in before if before[k] != now[k]}
        self.assertEqual(changed, closed)
        p = now['P33','process_electrification_score']
        self.assertEqual((p['proposed_value'],p['proposal_confidence']), ('7','B'))
        self.assertFalse(p['reviewer'])
        self.assertEqual(d.validate(ROOT), [])

    def test_mechanism_only_historical_plan_and_failed_pdf_boundaries(self):
        checks = {c['source_id']:c for c in d.rows(ROOT, 'evidence/decision_source_checks_20261019.csv')}
        self.assertIn('not SONOTRONIC equipment', checks['S-P33-11']['scope_note'])
        self.assertIn('not a commissioning date', checks['S-P33-10']['scope_note'])
        self.assertIn('2013 plan', checks['S-P23-06']['scope_note'])
        self.assertIn('not completion proof', checks['S-P24-05']['scope_note'])
        attempts = d.rows(ROOT, 'evidence/research_source_attempts_followup_20261019.csv')
        self.assertEqual(len(attempts),12)
        failed = [r for r in attempts if r['content_review_status'] == 'UNAVAILABLE']
        self.assertEqual(len(failed),1)
        self.assertEqual(failed[0]['http_status'],'404')
        self.assertFalse(failed[0]['selected_source_id'])
        recovery = next(r for r in d.rows(ROOT, 'evidence/source_recovery.csv')
                        if r['original_url'] == failed[0]['source_url'])
        self.assertEqual(recovery['resolution_status'],'PARTIAL_REPLACEMENT')
        self.assertTrue(recovery['remaining_gap'])
        self.assertFalse(recovery['reviewer'])

    def test_new_block_visible_and_all_approval_gates_remain(self):
        p = build_web_payload(ROOT)
        s = p['decision_research_summary']['latest_followup']
        self.assertEqual((s['field_attempt_count'],s['new_checked_field_count'],
                          s['still_unknown_field_count']),(23,1,22))
        c = next(c for c in p['companies'] if c['company_id'] == 'P33')
        self.assertEqual(c['decision_research_profile']['followup_id'],'DRFU-20261019-P33')
        self.assertEqual(c['decision_research_profile']['final_score_approval'],'NOT_GRANTED')
        f = p['field_assessment_summary']
        self.assertEqual((f['checked_fields'],f['needs_research_fields'],f['approved_fields']),(671,829,0))
        self.assertTrue(all(c['score_readiness']['score_status'] != 'FINAL_SCORE_READY' for c in p['companies']))


if __name__ == '__main__':
    unittest.main()
