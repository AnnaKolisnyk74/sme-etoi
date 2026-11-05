"""New evidence closes exact gaps without moving assets or bypassing gates."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
import decision_research as d
from export_web_data import build_web_payload


class NewFieldEvidenceTests(unittest.TestCase):
    def test_four_exact_closures_preserve_every_other_proposal(self):
        before = {(r['company_id'], r['score_field']): r for r in d.rows(
            ROOT, 'data/history/score_coding_proposals_before_followup_20261105.csv')}
        now = {(r['company_id'], r['score_field']): r for r in d.rows(
            ROOT, 'data/history/score_coding_proposals_before_followup_20261105b.csv')}
        expected = {('P34', 'measures_gap_score'), ('P34', 'management_gap_score'),
                    ('P38', 'measures_gap_score'), ('P38', 'onsite_integration_score')}
        self.assertEqual({k for k in before if before[k] != now[k]}, expected)
        for key in expected:
            self.assertEqual(before[key]['proposal_status'], 'NEEDS_RESEARCH')
            self.assertEqual(now[key]['proposal_status'], 'CHECKED')
            self.assertFalse(now[key]['reviewer'])
        attempts = d.rows(ROOT, 'evidence/field_research_followup_20261105.csv')
        self.assertEqual(len(attempts), 25)
        self.assertEqual({(r['company_id'], r['score_field']) for r in attempts
                          if r['outcome'] == 'NEW_EVIDENCE'}, expected)
        self.assertEqual(d.validate(ROOT), [])

    def test_external_network_assets_and_2013_chp_do_not_become_recent_capex(self):
        proposals = {(r['company_id'], r['score_field']): r for r in d.rows(
            ROOT, 'data/score_coding_proposals.csv')}
        for cid in ('P34', 'P38'):
            for field in ('investment_gap_score', 'thermal_storage_flex_score',
                          'temperature_fit_score', 'fossil_heat_displacement_score'):
                self.assertEqual(proposals[cid, field]['proposed_value'], '')
        payload = build_web_payload(ROOT)
        kts = next(c for c in payload['companies'] if c['company_id'] == 'P34')
        self.assertTrue(any(t['missing_fact'] == 'sme_eligibility'
                            for t in kts['research_tasks']))
        self.assertNotEqual(kts['score_readiness']['score_status'], 'FINAL_SCORE_READY')
        self.assertEqual(payload['field_assessment_summary']['approved_fields'], 0)

    def test_certificate_dates_and_representation_provenance_are_not_invented(self):
        cert = next(r for r in d.rows(ROOT, 'evidence/certificate_register.csv')
                    if (r['candidate_id'], r['standard']) == ('P34', 'ISO 50001'))
        self.assertEqual((cert['certificate_number'], cert['valid_from'], cert['valid_until']),
                         ('2024-0103418', '', '2027-12-01'))
        bodies = {r['source_id']: r for r in d.rows(
            ROOT, 'evidence/decision_source_checks_20261105.csv')}
        self.assertIn('NOT original PDF bytes', bodies['S-P34-10']['retrieval_note'])
        self.assertIn('only enabled', bodies['S-P38-06']['scope_note'])
        self.assertIn('2013', bodies['S-P38-07']['scope_note'])


if __name__ == '__main__':
    unittest.main()
