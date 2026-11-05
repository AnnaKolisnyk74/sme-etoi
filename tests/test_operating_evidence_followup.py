"""Operating evidence cannot silently become dispatch, savings or new equipment."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
import decision_research as d


class OperatingEvidenceFollowupTests(unittest.TestCase):
    def test_only_two_exact_unknown_fields_change(self):
        before = {(r['company_id'], r['score_field']): r for r in d.rows(
            ROOT, 'data/history/score_coding_proposals_before_followup_20261105b.csv')}
        now = {(r['company_id'], r['score_field']): r for r in d.rows(
            ROOT, 'data/score_coding_proposals.csv')}
        self.assertEqual({k for k in before if before[k] != now[k]},
                         {('P38', 'automation_control_score'), ('P108', 'measures_gap_score')})
        self.assertEqual(sum(p['proposal_status'] == 'CHECKED' for p in before.values()), 674)
        for k, p in before.items():
            if p['proposal_status'] == 'CHECKED':
                self.assertEqual(now[k], p)
        self.assertEqual(d.validate(ROOT), [])

    def test_full_kilns_and_automatic_lines_do_not_assert_dispatch_or_savings(self):
        rows = {(r['company_id'], r['score_field']): r for r in d.rows(
            ROOT, 'data/score_coding_proposals.csv')}
        self.assertEqual(rows['P108', 'scheduling_flex_score']['proposed_value'], '2')
        for cid in ('P38', 'P108'):
            for field in ('thermal_storage_flex_score', 'investment_gap_score',
                          'fossil_heat_displacement_score', 'motor_drive_score'):
                self.assertEqual(rows[cid, field]['proposed_value'], '')
        self.assertIn('No quantified savings', rows['P108', 'measures_gap_score']['evidence_basis'])
        self.assertIn('No coordinated', rows['P38', 'automation_control_score']['evidence_basis'])


if __name__ == '__main__':
    unittest.main()
