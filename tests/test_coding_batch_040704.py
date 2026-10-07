"""Owned assets, product/period boundaries and unretrievable certificate guards."""
import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from company_work_priority import read_csv,generate_company_work_priority
from score_work_queue import generate_score_work_queue
from select_coding_batch import select_batch
from run_pipeline import build_outputs,build_score_readiness
from score_companies import SCORE_FIELDS
from export_web_data import build_web_payload
CIDS=['P56','P57','P58','P59','P61','P63','P64','P66','P68','P70','P75','P76']
COUNTS=[5,1,9,4,4,4,5,3,6,4,2,8]
class ContinuousBatch04Tests(unittest.TestCase):
    def setUp(self):
        self.rows=read_csv(ROOT/'data/score_coding_proposals.csv')
        self.p={(r['company_id'],r['score_field']):r for r in self.rows}
        self.s={r['source_id']:r for r in read_csv(ROOT/'evidence/source_register.csv')}
        self.c={(r['candidate_id'],r['standard']):r for r in read_csv(ROOT/'evidence/certificate_register.csv')}

    def test_frozen_rank_reproduces_before_attribution_corrections(self):
        companies,_,research=build_outputs(ROOT)
        source=read_csv(ROOT/'tests/fixtures/source_register_before_nbcc040704.csv')
        process=read_csv(ROOT/'tests/fixtures/company_process_map_before_nbcc040704.csv')
        queue=generate_score_work_queue(companies,build_score_readiness(ROOT,companies),process,source,read_csv(ROOT/'evidence/qa_review.csv'),read_csv(ROOT/'data/pilot_coded.csv'),research,[r for r in self.rows if r['company_id'] not in CIDS])
        selected=select_batch(generate_company_work_priority(queue,source,process),'NBCC-2026-10-07-04','2026-10-07',size=12)
        manifest=[r for r in read_csv(ROOT/'data/coding_batch_selections.csv') if r['batch_id']=='NBCC-2026-10-07-04']
        self.assertEqual(selected,manifest)
        self.assertEqual([r['company_id'] for r in manifest],CIDS)
        self.assertEqual([r['verified_source_count'] for r in manifest],['2']*12)

    def test_all180_fields_preserve_unknown_and_real_review_gate(self):
        for cid,n in zip(CIDS,COUNTS):
            rows=[r for r in self.rows if r['company_id']==cid]
            self.assertEqual({r['score_field'] for r in rows},set(SCORE_FIELDS))
            self.assertEqual(sum(bool(r['proposed_value']) for r in rows),n)
            for r in rows:
                self.assertFalse(r['reviewer'] or r['review_date'] or r['review_note'])
                self.assertIn('AI-assisted',r['coder'])
                if r['proposed_value']:self.assertEqual(r['proposal_status'],'AWAITING_HUMAN_REVIEW')
                else:
                    self.assertEqual((r['proposal_status'],r['proposal_confidence']),('NEEDS_RESEARCH','UNKNOWN'))
                    self.assertTrue(r['missing_fact'])
            self.assertNotIn(cid,{r['company_id'] for r in read_csv(ROOT/'data/pilot_coded.csv')})

    def test_stock_theory_and_external_toolshops_do_not_become_own_drives(self):
        self.assertEqual(self.p['P57','motor_drive_score']['proposal_status'],'NEEDS_RESEARCH')
        self.assertEqual(self.p['P57','automation_control_score']['proposal_status'],'NEEDS_RESEARCH')
        self.assertIn('theoretical',self.s['S-P57-04']['evidence_fact'])
        self.assertIn('Stock imagery',self.s['S-P57-03']['evidence_fact'])
        self.assertEqual(self.p['P76','motor_drive_score']['proposed_value'],'2')
        for cid in ['P57','P76']:
            m=next(r for r in read_csv(ROOT/'data/company_process_map.csv') if r['company_id']==cid)
            self.assertIn('external partners',m['process_name_raw'])
        self.assertEqual(self.p['P56','motor_drive_score']['proposed_value'],'8')
        self.assertEqual(self.p['P58','motor_drive_score']['proposed_value'],'8')

    def test_battery_not_thermal_store_or_invented_commission(self):
        self.assertEqual(self.p['P58','onsite_integration_score']['proposed_value'],'3')
        self.assertEqual(self.p['P58','thermal_storage_flex_score']['proposal_status'],'NEEDS_RESEARCH')
        self.assertEqual(self.p['P58','investment_gap_score']['proposed_value'],'2')
        self.assertIn('undated',self.p['P58','investment_gap_score']['evidence_basis'])
        self.assertIn('950kWh',self.s['S-P58-03']['evidence_fact'])
        self.assertEqual(self.p['P59','thermal_storage_flex_score']['proposal_status'],'NEEDS_RESEARCH')

    def test_certificate_bodies_annex_and_404_claim_are_separate(self):
        for cid,num,start,end in [('P58','171116123/3','2025-11-28','2028-11-27'),('P76','001048.U','2025-11-29','2028-11-28')]:
            c=self.c[cid,'ISO 14001'];self.assertEqual((c['certificate_status'],c['certificate_number'],c['valid_from'],c['valid_until']),('VALID',num,start,end))
            self.assertEqual(self.p[cid,'management_gap_score']['proposed_value'],'2')
        self.assertIn('Annex page2 includes Siemens15',self.s['S-P76-05']['evidence_fact'])
        c=self.c['P70','ISO 14001']
        self.assertEqual((c['certificate_status'],c['direct_certificate_url'],c['valid_until']),('CLAIM_ONLY','',''))
        self.assertEqual(self.s['S-P70-04']['link_check_status'],'NOT_FOUND')
        self.assertEqual(self.p['P70','management_gap_score']['proposed_value'],'3')
        self.assertIn('not expiry proof',self.p['P70','management_gap_score']['evidence_basis'])

    def test_biolpg_biogas_customer_heaters_and_lapsed_plan_not_interchangeable(self):
        self.assertIn('BIO-LPG',self.s['S-P68-05']['evidence_fact'])
        self.assertIn('4436litres',self.s['S-P68-05']['evidence_fact'])
        for f in ['process_electrification_score','fossil_heat_displacement_score','automation_control_score']:
            self.assertEqual(self.p['P68',f]['proposal_status'],'NEEDS_RESEARCH')
        self.assertEqual(self.p['P68','investment_gap_score']['proposed_value'],'2')
        self.assertIn('could precede2021-10-07',self.p['P68','investment_gap_score']['evidence_basis'])

    def test_test_temperatures_recovery_outlets_and_customer_energy_do_not_cross_scope(self):
        self.assertIn('250C',self.s['S-P61-04']['evidence_fact'])
        self.assertEqual(self.p['P61','temperature_fit_score']['proposal_status'],'NEEDS_RESEARCH')
        self.assertEqual(self.p['P61','onsite_integration_score']['proposal_status'],'NEEDS_RESEARCH')
        self.assertEqual(self.p['P66','temperature_fit_score']['proposed_value'],'3')
        self.assertIn('980C/high firing1420C',self.p['P66','temperature_fit_score']['evidence_basis'])
        self.assertIn('110C',self.p['P66','temperature_fit_score']['evidence_basis'])
        self.assertEqual(self.p['P66','process_electrification_score']['proposal_status'],'NEEDS_RESEARCH')
        self.assertEqual(self.p['P64','onsite_integration_score']['proposal_status'],'NEEDS_RESEARCH')
        self.assertEqual(self.p['P75','investment_gap_score']['proposal_status'],'NEEDS_RESEARCH')
        self.assertEqual(self.p['P75','thermal_storage_flex_score']['proposal_status'],'NEEDS_RESEARCH')
        for sid in ['S-P61-02','S-P63-02']:self.assertEqual(self.s[sid]['link_check_status'],'CONTENT_REVIEW_REQUIRED')

    def test_web_full_batch_and_all_sources_without_aggregate_score(self):
        p=build_web_payload(ROOT);batch=next(b for b in p['coding_batches'] if b['batch_id']=='NBCC-2026-10-07-04')
        self.assertEqual([r['company_id'] for r in batch['companies']],CIDS)
        for r,n in zip(batch['companies'],COUNTS):
            self.assertEqual((r['awaiting_human_review_fields'],r['needs_research_fields']),(n,15-n))
            self.assertEqual(r['current_workflow_action'],'RESEARCH_FIRST')
            self.assertNotIn('score',r);self.assertNotIn('proposal_total',r)
        self.assertEqual(p['company_work_summary']['next_best_company']['unassessed_field_count'],15)
        self.assertEqual(p['source_audit_summary']['checked_company_count'],100)
