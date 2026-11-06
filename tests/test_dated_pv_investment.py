"""Dated PV evidence cannot resolve process heat or conflicting EnMS claims."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
import decision_research as d


class DatedPVInvestmentTests(unittest.TestCase):
    def test_one_investment_closes_without_changing_prior_checks(self):
        before = {(r['company_id'], r['score_field']): r for r in d.rows(
            ROOT, 'data/history/score_coding_proposals_before_followup_20261106.csv')}
        current = {(r['company_id'], r['score_field']): r for r in d.rows(
            ROOT, 'data/score_coding_proposals.csv')}
        self.assertEqual({k for k in before if before[k] != current[k]},
                         {('P37', 'investment_gap_score')})
        new = current['P37', 'investment_gap_score']
        self.assertEqual((new['proposed_value'], new['proposal_confidence']), ('2', 'B'))
        self.assertIn('2024', new['evidence_basis'])
        self.assertIn('not assigned wholesale', new['evidence_basis'])
        self.assertFalse(new['reviewer'])
        self.assertEqual(d.validate(ROOT), [])

    def test_conflicting_management_claim_and_pv_leave_operating_gaps_open(self):
        current = {(r['company_id'], r['score_field']): r for r in d.rows(
            ROOT, 'data/score_coding_proposals.csv')}
        for key in [('P10', 'management_gap_score'),
                    ('P37', 'process_electrification_score'),
                    ('P37', 'thermal_storage_flex_score'),
                    ('P37', 'scheduling_flex_score')]:
            self.assertEqual((current[key]['proposal_status'], current[key]['proposed_value']),
                             ('NEEDS_RESEARCH', ''))
        checks = d.source_checks(ROOT)
        self.assertIn('absent from this direct body', checks['S-P10-12']['scope_note'])
        self.assertIn('does not establish absence', checks['S-P10-13']['scope_note'])


if __name__ == '__main__':
    unittest.main()
