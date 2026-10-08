# Historical first-pass assertions use the immutable pre-recheck snapshot.
"""Regression guards for entity, thermal, certificate and project attribution."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))

from company_work_priority import read_csv, generate_company_work_priority
from score_work_queue import generate_score_work_queue
from select_coding_batch import select_batch
from run_pipeline import build_outputs, build_score_readiness
from score_companies import SCORE_FIELDS
from export_web_data import build_web_payload

CIDS = ['P77', 'P79', 'P80', 'P81', 'P83', 'P84', 'P87', 'P90', 'P91', 'P92', 'P93', 'P94']


class ContinuousBatch05Tests(unittest.TestCase):
    def setUp(self):
        self.rows = read_csv(ROOT / 'data/history/score_coding_proposals_before_recheck_20261007.csv')
        self.p = {(r['company_id'], r['score_field']): r for r in self.rows}
        self.s = {r['source_id']: r for r in read_csv(ROOT / 'evidence/source_register.csv')}
        self.c = {(r['candidate_id'], r['standard']): r for r in read_csv(ROOT / 'evidence/certificate_register.csv')}

    def test_frozen_selection_reproduces_before_scope_corrections(self):
        companies, _, research = build_outputs(ROOT)
        source = read_csv(ROOT / 'tests/fixtures/source_register_before_nbcc040705.csv')
        process = read_csv(ROOT / 'tests/fixtures/company_process_map_before_nbcc040705.csv')
        queue = generate_score_work_queue(
            companies, build_score_readiness(ROOT, companies), process, source,
            read_csv(ROOT / 'evidence/qa_review.csv'), read_csv(ROOT / 'data/pilot_coded.csv'),
            research, [r for r in self.rows if r['company_id'] not in CIDS])
        selected = select_batch(generate_company_work_priority(queue, source, process),
                                'NBCC-2026-10-07-05', '2026-10-07', size=12)
        manifest = [r for r in read_csv(ROOT / 'data/coding_batch_selections.csv')
                    if r['batch_id'] == 'NBCC-2026-10-07-05']
        self.assertEqual(selected, manifest)
        self.assertEqual([r['company_id'] for r in selected], CIDS)

    def test_all_fields_keep_unknown_and_independent_review(self):
        for cid in CIDS:
            rows = [r for r in self.rows if r['company_id'] == cid]
            self.assertEqual({r['score_field'] for r in rows}, set(SCORE_FIELDS))
            self.assertEqual(len(rows), 15)
            for r in rows:
                self.assertFalse(r['reviewer'] or r['review_date'] or r['review_note'])
                self.assertIn('AI-assisted', r['coder'])
                if r['proposed_value']:
                    self.assertEqual(r['proposal_status'], 'AWAITING_HUMAN_REVIEW')
                else:
                    self.assertEqual((r['proposal_status'], r['proposal_confidence']),
                                     ('NEEDS_RESEARCH', 'UNKNOWN'))
                    self.assertTrue(r['missing_fact'])

    def test_foreign_holder_cannot_supply_german_site_assets(self):
        rows = [r for r in self.rows if r['company_id'] == 'P87']
        self.assertTrue(all(not r['proposed_value'] for r in rows))
        self.assertIn('Yixing', self.s['S-P87-04']['evidence_fact'])
        self.assertIn('2029-05-26', self.s['S-P87-04']['evidence_fact'])
        mapping = next(r for r in read_csv(ROOT / 'data/company_process_map.csv') if r['company_id'] == 'P87')
        self.assertEqual(mapping['process_id'], 'PR012')
        companies, opportunities, _ = build_outputs(ROOT)
        self.assertIn('P87', {r['company_id'] for r in companies})
        self.assertNotIn('P87', {r['company_id'] for r in opportunities})

    def test_supplier_firing_and_sales_do_not_become_owned_kiln(self):
        for field in ['temperature_fit_score', 'process_electrification_score', 'fossil_heat_displacement_score']:
            self.assertEqual(self.p['P90', field]['proposal_status'], 'NEEDS_RESEARCH')
        self.assertEqual(self.p['P90', 'motor_drive_score']['proposed_value'], '2')
        self.assertIn('supplier KITO', self.s['S-P90-03']['evidence_fact'])
        self.assertIn('not owned', self.s['S-P90-04']['evidence_fact'])
        self.assertEqual(self.p['P81', 'temperature_fit_score']['proposal_status'], 'NEEDS_RESEARCH')
        self.assertIn('COATING resistance', self.s['S-P81-04']['evidence_fact'])

    def test_certificate_body_dates_override_old_filenames_and_previous_expiry(self):
        for cid, standard, start, end, number in [
            ('P77', 'ISO 50001', '2026-09-23', '2029-09-22', '001117.E'),
            ('P77', 'ISO 14001', '2026-09-23', '2029-09-22', '001117.U'),
            ('P79', 'ISO 50001', '2024-11-19', '2027-11-18', '181115129/2'),
            ('P79', 'ISO 14001', '2024-11-19', '2027-11-18', '171115241/3'),
            ('P80', 'ISO 14001', '2025-12-02', '2028-12-01', '12 104 20882 TMS')]:
            c = self.c[cid, standard]
            self.assertEqual((c['certificate_status'], c['valid_from'], c['valid_until'], c['certificate_number']),
                             ('VALID', start, end, number))
        self.assertEqual(self.p['P80', 'management_gap_score']['proposed_value'], '2')
        self.assertEqual(self.c['P91', 'EMAS']['valid_from'], '2025-12-17')
        self.assertEqual(self.c['P91', 'EMAS']['valid_until'], '')

    def test_calendar_or_grant_does_not_complete_energy_investments(self):
        self.assertEqual(self.p['P79', 'onsite_integration_score']['proposed_value'], '2')
        self.assertIn('not proven complete', self.p['P79', 'onsite_integration_score']['evidence_basis'])
        self.assertEqual(self.p['P79', 'thermal_storage_flex_score']['proposal_status'], 'NEEDS_RESEARCH')
        self.assertEqual(self.p['P83', 'investment_gap_score']['proposal_status'], 'NEEDS_RESEARCH')
        self.assertIn('planned', self.s['S-P83-03']['evidence_fact'])
        self.assertIn('2024', self.p['P79', 'investment_gap_score']['evidence_basis'])
        self.assertIn('Future12/2025', self.p['P91', 'investment_gap_score']['evidence_basis'])
        self.assertIn('unit inconsistent', self.p['P91', 'fossil_heat_displacement_score']['evidence_basis'])

    def test_purchased_hydro_and_bounded_biomass_heat_are_distinct(self):
        self.assertEqual(self.p['P80', 'onsite_integration_score']['proposal_status'], 'NEEDS_RESEARCH')
        self.assertIn('purchased electricity', self.s['S-P80-07']['evidence_fact'])
        self.assertEqual(self.p['P92', 'fossil_heat_displacement_score']['proposed_value'], '0')
        self.assertIn('ALL operating heat', self.p['P92', 'fossil_heat_displacement_score']['evidence_basis'])
        self.assertIn('discrepancy retained', self.s['S-P92-03']['evidence_fact'])
        self.assertEqual(self.p['P92', 'investment_gap_score']['proposal_status'], 'NEEDS_RESEARCH')

    def test_room_heat_and_battery_do_not_become_process_heat_or_thermal_store(self):
        self.assertEqual(self.p['P94', 'onsite_integration_score']['proposed_value'], '3')
        for field in ['temperature_fit_score', 'process_electrification_score', 'thermal_storage_flex_score']:
            self.assertEqual(self.p['P94', field]['proposal_status'], 'NEEDS_RESEARCH')
        self.assertEqual(self.p['P94', 'investment_gap_score']['proposed_value'], '2')
        self.assertIn('one recentintegratedproject', self.p['P94', 'investment_gap_score']['evidence_basis'])
        self.assertEqual(self.p['P93', 'thermal_storage_flex_score']['proposal_status'], 'NEEDS_RESEARCH')

    def test_full_web_batch_and_zero_match_firms_retain_research_work(self):
        p = build_web_payload(ROOT)
        batch = next(b for b in p['coding_batches'] if b['batch_id'] == 'NBCC-2026-10-07-05')
        self.assertEqual([r['company_id'] for r in batch['companies']], CIDS)
        self.assertEqual(sum(r['checked_fields'] for r in batch['companies']), 70)
        self.assertEqual(sum(r['needs_research_fields'] for r in batch['companies']), 110)
        for r in batch['companies']:
            self.assertEqual(r['current_workflow_action'], 'RESEARCH_FIRST')
            self.assertNotIn('score', r)
            self.assertNotIn('proposal_total', r)
        for cid in ['P87', 'P90']:
            company = next(c for c in p['companies'] if c['company_id'] == cid)
            self.assertEqual(company['opportunities'], [])
            self.assertTrue(company['sources'])
            self.assertEqual(len(company['score_work_tasks']), 5)
        self.assertIsNone(p['company_work_summary']['next_best_company']['unassessed_field_count'])
        self.assertEqual(p['source_audit_summary']['checked_company_count'], 100)
