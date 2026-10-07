"""Entity, mechanical power, certificate-body and current-unit boundaries."""
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

CIDS = ['P95','P97','P98','P100','P101','P105','P106','P108','P109','P110','P37','P60']
COUNTS = [1,7,5,11,9,5,4,6,8,0,8,4]


class ContinuousBatch06Tests(unittest.TestCase):
    def setUp(self):
        self.rows = read_csv(ROOT / 'data/score_coding_proposals.csv')
        self.p = {(r['company_id'], r['score_field']): r for r in self.rows}
        self.s = {r['source_id']: r for r in read_csv(ROOT / 'evidence/source_register.csv')}
        self.c = {(r['candidate_id'], r['standard']): r for r in read_csv(ROOT / 'evidence/certificate_register.csv')}

    def test_frozen_ranking_reproduces_before_enrichment_and_scope_changes(self):
        companies, _, research = build_outputs(ROOT)
        source = read_csv(ROOT / 'tests/fixtures/source_register_before_nbcc040706.csv')
        process = read_csv(ROOT / 'tests/fixtures/company_process_map_before_nbcc040706.csv')
        queue = generate_score_work_queue(
            companies, build_score_readiness(ROOT, companies), process, source,
            read_csv(ROOT / 'evidence/qa_review.csv'), read_csv(ROOT / 'data/pilot_coded.csv'),
            research, [r for r in self.rows if r['company_id'] not in CIDS])
        selected = select_batch(generate_company_work_priority(queue, source, process),
                                'NBCC-2026-10-07-06', '2026-10-07', size=12)
        manifest = [r for r in read_csv(ROOT / 'data/coding_batch_selections.csv')
                    if r['batch_id'] == 'NBCC-2026-10-07-06']
        self.assertEqual(selected, manifest)
        self.assertEqual([r['company_id'] for r in selected], CIDS)

    def test_all180_fields_preserve_unknown_and_independent_review(self):
        for cid, n in zip(CIDS, COUNTS):
            rows = [r for r in self.rows if r['company_id'] == cid]
            self.assertEqual(len(rows), 15)
            self.assertEqual({r['score_field'] for r in rows}, set(SCORE_FIELDS))
            self.assertEqual(sum(bool(r['proposed_value']) for r in rows), n)
            for r in rows:
                self.assertFalse(r['reviewer'] or r['review_date'] or r['review_note'])
                self.assertIn('AI-assisted', r['coder'])
                if r['proposed_value']:
                    self.assertEqual(r['proposal_status'], 'AWAITING_HUMAN_REVIEW')
                else:
                    self.assertEqual((r['proposal_status'], r['proposal_confidence']),
                                     ('NEEDS_RESEARCH', 'UNKNOWN'))
                    self.assertTrue(r['missing_fact'])

    def test_spc_news_cannot_supply_dornstetten_investments(self):
        self.assertIn('NOT attributed', self.s['S-P100-06']['evidence_fact'])
        self.assertIn('Kläger SPC', self.s['S-P100-06']['evidence_fact'])
        self.assertEqual(self.p['P100','investment_gap_score']['proposal_status'], 'NEEDS_RESEARCH')
        self.assertEqual(self.p['P100','temperature_fit_score']['proposed_value'], '3')
        self.assertIn('1400/1650', self.p['P100','temperature_fit_score']['evidence_basis'])
        self.assertIn('Dornstetten', self.s['S-P100-05']['evidence_fact'])
        self.assertIn('PR007', {r['process_id'] for r in read_csv(ROOT / 'data/company_process_map.csv') if r['company_id']=='P100'})

    def test_mechanical_water_power_is_not_owned_electric_generation(self):
        for field in ['motor_drive_score','onsite_integration_score']:
            self.assertEqual(self.p['P109',field]['proposal_status'], 'NEEDS_RESEARCH')
        self.assertIn('mechanical belt', self.s['S-P109-04']['evidence_fact'])
        self.assertIn('NOT evidence of owned hydroelectric', self.s['S-P109-04']['evidence_fact'])
        self.assertEqual(self.p['P109','fossil_heat_displacement_score']['proposal_status'], 'NEEDS_RESEARCH')
        self.assertEqual(self.p['P109','investment_gap_score']['proposal_status'], 'NEEDS_RESEARCH')

    def test_certificate_body_overrides_filename_and_previous_expiry(self):
        for cid, start, end, number in [('P37','2025-07-31','2028-07-28','170813086/4'),
                                       ('P105','2025-12-23','2028-12-22','170121011/3')]:
            c = self.c[cid,'ISO 14001']
            self.assertEqual((c['certificate_status'],c['valid_from'],c['valid_until'],c['certificate_number']),
                             ('VALID',start,end,number))
        c = self.c['P101','EMAS']
        self.assertEqual((c['certificate_status'],c['valid_until'],c['certificate_number']),
                         ('VALID','2029-09-30','DE-130-00026'))
        self.assertEqual(c['valid_from'], '')  # Issue date is not an explicit validity start.
        self.assertIn('issued 2026-01-15', c['notes'])
        self.assertIn('NOT certified', self.c['P101','ISO 50001']['notes'])
        self.assertEqual(self.p['P101','management_gap_score']['proposed_value'], '2')

    def test_unverified_continuity_and_cold_machining_remove_false_kiln_matches(self):
        mappings={r['company_id']:r for r in read_csv(ROOT / 'data/company_process_map.csv')}
        self.assertEqual(mappings['P106']['process_id'],'PR013')
        self.assertEqual(mappings['P110']['process_id'],'PR012')
        self.assertTrue(all(not r['proposed_value'] for r in self.rows if r['company_id']=='P110'))
        for field in ['temperature_fit_score','process_electrification_score','fossil_heat_displacement_score']:
            self.assertEqual(self.p['P106',field]['proposal_status'],'NEEDS_RESEARCH')
        for sid in ['S-P110-01','S-P110-03']:
            self.assertEqual(self.s[sid]['link_check_status'],'CONTENT_REVIEW_REQUIRED')
            self.assertIn('Eschenbach Porzellan GmbH',self.s[sid]['evidence_fact'])
        p=build_web_payload(ROOT)
        for cid in ['P106','P110']:
            company=next(c for c in p['companies'] if c['company_id']==cid)
            self.assertEqual(company['opportunities'],[])
            self.assertTrue(company['sources'])
            self.assertEqual(len(company['score_work_tasks']),5)

    def test_units_room_heat_and_operation_dates_do_not_fill_other_fields(self):
        self.assertIn('not generated kWh',self.s['S-P37-02']['evidence_fact'])
        self.assertIn('NOT voltage, kW',self.s['S-P60-04']['evidence_fact'])
        for cid in ['P37','P60','P101','P100']:
            self.assertEqual(self.p[cid,'investment_gap_score']['proposal_status'],'NEEDS_RESEARCH')
            self.assertEqual(self.p[cid,'thermal_storage_flex_score']['proposal_status'],'NEEDS_RESEARCH')
        self.assertEqual(self.p['P37','temperature_fit_score']['proposal_status'],'NEEDS_RESEARCH')
        self.assertEqual(self.p['P97','investment_gap_score']['proposed_value'],'0')
        self.assertEqual(self.p['P97','scheduling_flex_score']['proposal_status'],'NEEDS_RESEARCH')

    def test_web_batch_preserves_history_without_aggregate_score(self):
        p=build_web_payload(ROOT)
        batch=next(b for b in p['coding_batches'] if b['batch_id']=='NBCC-2026-10-07-06')
        self.assertEqual([r['company_id'] for r in batch['companies']],CIDS)
        self.assertEqual(sum(r['awaiting_human_review_fields'] for r in batch['companies']),68)
        self.assertEqual(sum(r['needs_research_fields'] for r in batch['companies']),112)
        for r in batch['companies']:
            self.assertEqual(r['current_workflow_action'],'RESEARCH_FIRST')
            self.assertNotIn('score',r)
            self.assertNotIn('proposal_total',r)
        self.assertEqual(p['source_audit_summary']['checked_company_count'],100)
