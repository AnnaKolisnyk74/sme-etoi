"""Attribution, certificate validity and temporal/temperature boundaries of batch 02."""
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from company_work_priority import read_csv, generate_company_work_priority
from run_pipeline import build_outputs, build_score_readiness
from score_work_queue import generate_score_work_queue
from select_coding_batch import select_batch
from score_companies import SCORE_FIELDS
from export_web_data import build_web_payload
CIDS={'P26','P28','P29','P33'}

class CodingBatch040702Tests(unittest.TestCase):
    def setUp(self):
        self.proposals={(r['company_id'],r['score_field']):r for r in read_csv(ROOT/'data/score_coding_proposals.csv')}
        self.sources={r['source_id']:r for r in read_csv(ROOT/'evidence/source_register.csv')}
        self.certs={(r['candidate_id'],r['standard']):r for r in read_csv(ROOT/'evidence/certificate_register.csv')}

    def test_four_ranked_selections_reproduce_before_evidence_and_attribution_corrections(self):
        manifest=[r for r in read_csv(ROOT/'data/coding_batch_selections.csv') if r['batch_id']=='NBCC-2026-10-07-02']
        companies,_,research=build_outputs(ROOT)
        sources=read_csv(ROOT/'tests/fixtures/source_register_before_nbcc040702.csv')
        process=read_csv(ROOT/'tests/fixtures/company_process_map_before_nbcc040702.csv')
        work=generate_score_work_queue(companies,build_score_readiness(ROOT,companies),process,sources,
            read_csv(ROOT/'evidence/qa_review.csv'),read_csv(ROOT/'data/pilot_coded.csv'),research,
            [r for r in self.proposals.values() if r['company_id'] not in CIDS])
        ranking=generate_company_work_priority(work,sources,process)
        self.assertEqual(select_batch(ranking,'NBCC-2026-10-07-02','2026-10-07',size=4),manifest)
        self.assertEqual([r['company_id'] for r in manifest],['P26','P28','P29','P33'])
        self.assertEqual([r['verified_source_count'] for r in manifest],['2']*4)

    def test_all_sixty_fields_preserve_review_gate_and_blank_valued_gaps(self):
        for cid,numeric in [('P26',8),('P28',10),('P29',11),('P33',6)]:
            rows=[r for (cc,_),r in self.proposals.items() if cc==cid]
            self.assertEqual({r['score_field'] for r in rows},set(SCORE_FIELDS))
            self.assertEqual(sum(r['proposal_status']=='AWAITING_HUMAN_REVIEW' for r in rows),numeric)
            for r in rows:
                self.assertFalse(r['reviewer'] or r['review_date'] or r['review_note'])
                self.assertIn('AI-assisted',r['coder'])
                self.assertTrue(r['evidence_source_ids'])
                if r['proposal_status']=='NEEDS_RESEARCH':
                    self.assertEqual(r['proposed_value'],'');self.assertEqual(r['proposal_confidence'],'UNKNOWN')
                    self.assertTrue(r['missing_fact'])
            for f in ['data/pilot_coded.csv','outputs/pilot_scored.csv']:
                self.assertNotIn(cid,{r['company_id'] for r in read_csv(ROOT/f)})

    def test_current_direct_certificates_use_body_holder_dates_not_legacy_url_or_neighbour(self):
        for cid,standard,sid,number,start,end in [
            ('P26','ISO 50001','S-P26-04','10000407436-MSC-RvA-DEU','2024-06-26','2027-06-25'),
            ('P26','ISO 14001','S-P26-05','2024-11089','2024-03-20','2027-03-20'),
            ('P33','ISO 14001','S-P33-05','000804.U','2025-01-28','2027-07-09')]:
            r=self.certs[cid,standard]
            self.assertEqual((r['certificate_status'],r['certificate_number'],r['valid_from'],r['valid_until']),('VALID',number,start,end))
            self.assertEqual(r['direct_certificate_url'],self.sources[sid]['source_link'])
            self.assertEqual(r['review_status'],'RESEARCHED')
        self.assertIn('03-2024',self.certs['P26','ISO 14001']['direct_certificate_url'])
        self.assertEqual(self.certs['P33','ISO 50001']['certificate_status'],'NOT_FOUND_AFTER_CHECK')
        self.assertIn('neighbouring',self.sources['S-P33-08']['evidence_fact'])
        self.assertEqual(self.proposals['P26','management_gap_score']['proposed_value'],'0')
        self.assertEqual(self.proposals['P33','management_gap_score']['proposed_value'],'2')

    def test_emas_validation_does_not_invent_expiry_repair_or_future_project_completion(self):
        c=self.certs['P29','EMAS']
        self.assertEqual((c['certificate_status'],c['certificate_number'],c['valid_from'],c['valid_until']),('VALID','DE-147-00005','2026-06-19',''))
        self.assertIn('due dates',c['notes'])
        self.assertIn('2024 narrative / 2025 tables / 2026 validation',self.sources['S-P29-03']['reporting_period'])
        self.assertIn('defective',self.proposals['P29','process_electrification_score']['missing_fact'])
        self.assertEqual(self.proposals['P29','process_electrification_score']['proposal_status'],'NEEDS_RESEARCH')
        for f in ['thermal_storage_flex_score','incremental_load_score','temperature_fit_score']:
            self.assertEqual(self.proposals['P29',f]['proposal_status'],'NEEDS_RESEARCH')
        self.assertIn('prospective fleet projects are excluded',self.proposals['P29','investment_gap_score']['evidence_basis'])
        self.assertIn('not achievement',self.proposals['P29','targets_gap_score']['evidence_basis'])

    def test_berg_real_cold_buffer_does_not_turn_suspect_temperature_building_heat_or_award_into_heat_evidence(self):
        self.assertEqual(self.proposals['P28','thermal_storage_flex_score']['proposed_value'],'5')
        self.assertEqual(self.proposals['P28','scheduling_flex_score']['proposed_value'],'5')
        self.assertIn('90-deg-C',self.proposals['P28','temperature_fit_score']['missing_fact'])
        self.assertIn('excluded',self.proposals['P28','thermal_storage_flex_score']['evidence_basis'])
        for f in ['temperature_fit_score','process_electrification_score','fossil_heat_displacement_score','management_gap_score']:
            self.assertEqual(self.proposals['P28',f]['proposal_status'],'NEEDS_RESEARCH')
        self.assertIn('hospitality',self.proposals['P28','management_gap_score']['missing_fact'])
        self.assertEqual(self.proposals['P28','investment_gap_score']['proposed_value'],'2')

    def test_gindele_generic_municipality_and_counter_zeros_cannot_supply_missing_energy_facts(self):
        self.assertEqual(self.sources['S-P33-02']['link_check_status'],'CONTENT_REVIEW_REQUIRED')
        mapping=next(r for r in read_csv(ROOT/'data/company_process_map.csv') if r['company_id']=='P33')
        self.assertEqual(mapping['process_evidence_url'],self.sources['S-P33-03']['source_link'])
        case=next(r for r in read_csv(ROOT/'evidence/source_recovery.csv') if r['company_id']=='P33')
        self.assertEqual(case['resolution_status'],'REPLACEMENT_FOUND');self.assertFalse(case['reviewer'])
        self.assertIn('animated zero counters',self.proposals['P33','scheduling_flex_score']['missing_fact'])
        self.assertIn('2017',self.proposals['P33','investment_gap_score']['missing_fact'])
        self.assertEqual(self.proposals['P33','measures_gap_score']['proposal_status'],'NEEDS_RESEARCH')
        self.assertIn('HV is hardness',self.proposals['P26','temperature_fit_score']['missing_fact'])

    def test_web_preserves_frozen_batch_and_live_field_counts_without_total_or_approval(self):
        payload=build_web_payload(ROOT)
        batch=next(b for b in payload['coding_batches'] if b['batch_id']=='NBCC-2026-10-07-02')
        self.assertEqual([r['company_id'] for r in batch['companies']],['P26','P28','P29','P33'])
        for r,n,g in zip(batch['companies'],[8,10,11,6],[7,5,4,9]):
            self.assertEqual((r['awaiting_human_review_fields'],r['needs_research_fields']),(n,g))
            self.assertEqual(r['current_workflow_action'],'RESEARCH_FIRST')
            self.assertNotIn('score',r);self.assertNotIn('proposal_total',r)
        self.assertEqual(payload['company_work_summary']['next_best_company']['unassessed_field_count'],15)
        for company in read_csv(ROOT/'data/company_intelligence.csv'):
            if company['company_id'] in CIDS:
                for field in [k for k in company if k.endswith('_deployed')]:
                    self.assertEqual(company[field],'UNKNOWN')
