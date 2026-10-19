"""Operational process proof must not become invented current fuel or new assets."""
import sys, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
import decision_research as d
from export_web_data import build_web_payload


class FactoryProcessFollowupTests(unittest.TestCase):
    def test_exact_frozen_scope_three_closures_and_all_checked_rows_preserved(self):
        before = {(p['company_id'], p['score_field']): p for p in d.rows(
            ROOT, 'data/history/score_coding_proposals_before_followup_20261018b.csv')}
        now = {(p['company_id'], p['score_field']): p for p in d.rows(
            ROOT, 'data/score_coding_proposals.csv')}
        attempts = d.rows(ROOT, 'evidence/field_research_followup_20261018b.csv')
        expected = {k for k, p in before.items() if k[0] in {'P16', 'P19', 'P20'}
                    and p['proposal_status'] == 'NEEDS_RESEARCH'}
        self.assertEqual({(r['company_id'], r['score_field']) for r in attempts}, expected)
        self.assertEqual(len(attempts), 29)
        closed = {(r['company_id'], r['score_field']) for r in attempts
                  if r['outcome'] == 'NEW_EVIDENCE'}
        self.assertEqual(closed, {('P16', 'fossil_heat_displacement_score'),
                                  ('P19', 'motor_drive_score'),
                                  ('P19', 'automation_control_score')})
        checked = [k for k, p in before.items() if p['proposal_status'] == 'CHECKED']
        self.assertEqual(len(checked), 667)
        for k in checked:
            self.assertEqual(now[k], before[k])
        for k in expected - closed:
            self.assertEqual((now[k]['proposed_value'], now[k]['proposal_confidence']),
                             ('', 'UNKNOWN'))
            self.assertTrue(now[k]['missing_fact'])
        self.assertEqual(d.validate(ROOT), [])

    def test_historical_gas_project_notice_and_staffing_do_not_settle_current_mix(self):
        p = {(r['company_id'], r['score_field']): r for r in d.rows(
            ROOT, 'data/score_coding_proposals.csv')}
        for f in ['fossil_heat_displacement_score', 'investment_gap_score',
                  'process_electrification_score', 'incremental_load_score',
                  'thermal_storage_flex_score', 'scheduling_flex_score',
                  'onsite_integration_score', 'power_conversion_score']:
            self.assertEqual(p['P19', f]['proposal_status'], 'NEEDS_RESEARCH')
        checks = {r['source_id']: r for r in d.rows(
            ROOT, 'evidence/decision_source_checks_20261018b.csv')}
        self.assertIn('2021', checks['S-P19-08']['scope_note'])
        self.assertIn('not a2026 fuel inventory', checks['S-P19-08']['scope_note'])
        self.assertIn('No project dates', checks['S-P19-11']['scope_note'])
        self.assertIn('not load flexibility', checks['S-P19-12']['scope_note'])
        self.assertIn('2020 twelveGWh', p['P16', 'fossil_heat_displacement_score']['evidence_basis'])
        self.assertEqual((p['P19', 'motor_drive_score']['proposed_value'],
                          p['P19', 'automation_control_score']['proposed_value']), ('2', '3'))
        self.assertEqual(sum(r['proposal_status'] == 'NEEDS_RESEARCH'
                             for (cid, _), r in p.items() if cid == 'P20'), 9)

    def test_web_exposes_latest_attempts_sources_and_approval_boundary(self):
        p = build_web_payload(ROOT)
        s = p['decision_research_summary']['latest_followup']
        self.assertEqual((s['field_attempt_count'], s['new_checked_field_count'],
                          s['still_unknown_field_count']), (23, 1, 22))
        by = {c['company_id']: c for c in p['companies']}
        self.assertEqual(by['P19']['decision_research_profile']['followup_id'],
                         'DRFU-20261018b-P19')
        self.assertNotIn('S-P19-09', by['P18']['decision_research_profile']['source_ids'])
        self.assertEqual(p['field_assessment_summary']['approved_fields'], 0)
        self.assertTrue(all(c['score_readiness']['score_status'] != 'FINAL_SCORE_READY'
                            for c in p['companies']))


if __name__ == '__main__':
    unittest.main()
