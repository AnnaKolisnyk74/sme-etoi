"""Continuous fieldwise batch: attribution, process mismatch and temporal guards."""
import unittest, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from company_work_priority import read_csv,generate_company_work_priority
from score_work_queue import generate_score_work_queue
from select_coding_batch import select_batch
from run_pipeline import build_outputs,build_score_readiness,validate_generated_outputs
from score_companies import SCORE_FIELDS
from export_web_data import build_web_payload
CIDS=['P35','P36','P38','P39','P41','P44','P45','P50','P51','P52','P54','P55']
COUNTS=[9,8,2,6,4,2,8,9,4,1,5,9]

class ContinuousBatchTests(unittest.TestCase):
    def setUp(self):
        self.rows=read_csv(ROOT/'data/score_coding_proposals.csv')
        self.p={(r['company_id'],r['score_field']):r for r in self.rows}
        self.s={r['source_id']:r for r in read_csv(ROOT/'evidence/source_register.csv')}
        self.c={(r['candidate_id'],r['standard']):r for r in read_csv(ROOT/'evidence/certificate_register.csv')}

    def test_twelve_frozen_candidates_reproduce_before_content_and_process_corrections(self):
        companies,_,research=build_outputs(ROOT)
        sources=read_csv(ROOT/'tests/fixtures/source_register_before_nbcc040703.csv')
        process=read_csv(ROOT/'tests/fixtures/company_process_map_before_nbcc040703.csv')
        work=generate_score_work_queue(companies,build_score_readiness(ROOT,companies),process,sources,read_csv(ROOT/'evidence/qa_review.csv'),read_csv(ROOT/'data/pilot_coded.csv'),research,[r for r in self.rows if r['company_id'] not in CIDS])
        ranking=generate_company_work_priority(work,sources,process)
        selected=select_batch(ranking,'NBCC-2026-10-07-03','2026-10-07',size=12)
        manifest=[r for r in read_csv(ROOT/'data/coding_batch_selections.csv') if r['batch_id']=='NBCC-2026-10-07-03']
        self.assertEqual(selected,manifest)
        self.assertEqual([r['company_id'] for r in selected],CIDS)
        self.assertEqual([r['verified_source_count'] for r in selected],['2']*12)

    def test_all180_fields_keep_real_human_review_and_blank_research_values(self):
        for cid,n in zip(CIDS,COUNTS):
            rows=[r for r in self.rows if r['company_id']==cid]
            self.assertEqual({r['score_field'] for r in rows},set(SCORE_FIELDS))
            self.assertEqual(sum(bool(r['proposed_value']) for r in rows),n)
            for r in rows:
                self.assertFalse(r['reviewer'] or r['review_date'] or r['review_note'])
                self.assertIn('AI-assisted',r['coder'])
                self.assertTrue(r['evidence_source_ids'])
                if r['proposed_value']:self.assertEqual(r['proposal_status'],'AWAITING_HUMAN_REVIEW')
                else:
                    self.assertEqual((r['proposal_status'],r['proposal_confidence']),('NEEDS_RESEARCH','UNKNOWN'))
                    self.assertTrue(r['missing_fact'])
            for f in ['data/pilot_coded.csv','outputs/pilot_scored.csv']:
                self.assertNotIn(cid,{r['company_id'] for r in read_csv(ROOT/f)})

    def test_certificate_bodies_and_register_have_distinct_dates_and_scopes(self):
        for cid,num,end in [('P35','Z-24-10213-14','2027-03-18'),('P36','44 104 141717','2027-01-17'),('P39','12 104 35301 TMS','2026-12-28'),('P41','DE016081','2028-05-17'),('P55','12-023','2026-10-15')]:
            r=self.c[cid,'ISO 14001'];self.assertEqual((r['certificate_status'],r['certificate_number'],r['valid_until']),('VALID',num,end))
        self.assertEqual(self.c['P55','ISO 14001']['valid_from'],'')
        self.assertIn('2025',self.s['S-P36-06']['evidence_fact'])
        r=self.c['P50','EMAS']
        self.assertEqual((r['certificate_status'],r['certificate_number'],r['valid_from'],r['valid_until']),('VALID','DE-155-00168','2023-06-28',''))
        self.assertIn('not expiry',r['notes'])
        self.assertEqual(self.c['P51','ISO 14001']['certificate_status'],'CLAIM_ONLY')
        self.assertEqual(self.p['P51','management_gap_score']['proposed_value'],'3')

    def test_staging_generic_sources_and_group_assets_do_not_close_fields(self):
        for sid in ['S-P36-02','S-P38-01','S-P38-02','S-P41-02','S-P44-02']:
            self.assertEqual(self.s[sid]['link_check_status'],'CONTENT_REVIEW_REQUIRED')
        self.assertIn('280',self.s['S-P38-03']['evidence_fact'])
        self.assertEqual(self.p['P38','process_electrification_score']['proposal_status'],'NEEDS_RESEARCH')
        self.assertIn('future',self.s['S-P41-05']['evidence_fact'])
        self.assertEqual(self.p['P41','process_electrification_score']['proposal_status'],'NEEDS_RESEARCH')
        self.assertEqual(self.p['P44','temperature_fit_score']['proposal_status'],'NEEDS_RESEARCH')
        self.assertEqual(self.p['P44','power_conversion_score']['proposal_status'],'NEEDS_RESEARCH')
        self.assertIn('1893',self.p['P52','targets_gap_score']['evidence_basis'])
        self.assertEqual(self.p['P52','motor_drive_score']['proposal_status'],'NEEDS_RESEARCH')

    def test_actual_thermoforming_cannot_inherit_injection_flexibility_or_force_opportunity(self):
        m=next(r for r in read_csv(ROOT/'data/company_process_map.csv') if r['company_id']=='P35')
        self.assertEqual(m['process_id'],'PR010')
        a=next(r for r in read_csv(ROOT/'data/process_library.csv') if r['process_id']=='PR010')
        self.assertEqual((a['schedulability'],a['thermal_inertia_storage']),('UNKNOWN','UNKNOWN'))
        companies,opportunities,queue=build_outputs(ROOT)
        self.assertFalse([r for r in opportunities if r['company_id']=='P35'])
        self.assertEqual(validate_generated_outputs(companies,opportunities,queue),[])
        bad=opportunities+[dict(opportunities[0],company_id='OUTSIDE')]
        self.assertTrue(validate_generated_outputs(companies,bad,queue))
        self.assertEqual(self.p['P35','investment_gap_score']['proposed_value'],'2')
        self.assertEqual(self.p['P35','process_electrification_score']['proposal_status'],'NEEDS_RESEARCH')

    def test_preflight_rejects_unresolved_process_id_instead_of_accepting_empty_output(self):
        from unittest.mock import patch
        import validate_pilot
        original=validate_pilot.read_csv
        def changed(root, path):
            rows=original(root,path)
            if path=='data/company_process_map.csv':
                rows=[dict(r, process_id='MISSING') if r['company_id']=='P35' else r for r in rows]
            return rows
        with patch.object(validate_pilot,'read_csv',side_effect=changed):
            self.assertIn('unknown process mapping for P35',validate_pilot.validate(ROOT))

    def test_own_electric_glass_furnaces_are_not_temperature_dispatch_or_new_load(self):
        self.assertEqual(self.p['P45','process_electrification_score']['proposed_value'],'10')
        for f in ['temperature_fit_score','scheduling_flex_score','thermal_storage_flex_score','incremental_load_score','investment_gap_score']:
            self.assertEqual(self.p['P45',f]['proposal_status'],'NEEDS_RESEARCH')
        self.assertIn('130 kg',self.p['P45','process_electrification_score']['evidence_basis'])
        self.assertEqual(self.p['P36','power_conversion_score']['proposed_value'],'2')
        self.assertEqual(self.p['P36','onsite_integration_score']['proposed_value'],'1')
        self.assertIn('does not establish owned PV',self.p['P36','onsite_integration_score']['evidence_basis'])

    def test_heat_pump_report_and_percent_denominators_do_not_invent_storage_or_recent_projects(self):
        self.assertEqual(self.p['P50','temperature_fit_score']['proposed_value'],'10')
        self.assertIn('150 kW thermal not electrical',self.p['P50','temperature_fit_score']['evidence_basis'])
        for f in ['targets_gap_score','investment_gap_score','thermal_storage_flex_score','fossil_heat_displacement_score']:
            self.assertEqual(self.p['P50',f]['proposal_status'],'NEEDS_RESEARCH')
        self.assertIn('2020-2024',self.p['P50','targets_gap_score']['missing_fact'])
        self.assertIn('not75%',self.p['P54','onsite_integration_score']['evidence_basis'])
        self.assertEqual(self.p['P54','investment_gap_score']['proposal_status'],'NEEDS_RESEARCH')
        self.assertEqual(self.p['P55','investment_gap_score']['proposed_value'],'0')
        for f in ['thermal_storage_flex_score','fossil_heat_displacement_score']:
            self.assertEqual(self.p['P55',f]['proposal_status'],'NEEDS_RESEARCH')

    def test_web_keeps_all_companies_and_live_batch_without_aggregate_score(self):
        p=build_web_payload(ROOT);batch=next(b for b in p['coding_batches'] if b['batch_id']=='NBCC-2026-10-07-03')
        self.assertEqual([r['company_id'] for r in batch['companies']],CIDS)
        for r,n in zip(batch['companies'],COUNTS):
            self.assertEqual((r['awaiting_human_review_fields'],r['needs_research_fields']),(n,15-n))
            self.assertEqual(r['current_workflow_action'],'RESEARCH_FIRST')
            self.assertNotIn('score',r);self.assertNotIn('proposal_total',r)
        self.assertEqual(p['company_work_summary']['next_best_company']['company_id'],'P77')
        self.assertEqual(len(p['companies']),100)
        m=next(c for c in p['companies'] if c['company_id']=='P35')
        self.assertEqual(m['opportunities'],[])
        self.assertTrue(m['score_readiness']);self.assertTrue(m['sources'])
