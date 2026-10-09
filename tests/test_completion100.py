"""Complete documentary coverage without manufactured deployment or approval."""
import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from company_work_priority import read_csv, generate_company_work_priority
from export_web_data import build_web_payload, field_assessment_summary
from run_pipeline import build_outputs, build_score_readiness
from score_work_queue import generate_score_work_queue
from score_companies import SCORE_FIELDS
from select_coding_batch import select_batch
from validate_score_coding_proposals import validate

REGULAR = ['P71','P72','P73','P74','P78','P82','P85','P86','P89','P96','P99','P102','P103','P107','P62','P03']
GATED = {'P07','P10','P104','P32','P34','P40','P42','P46','P47','P65','P67','P88'}


class Completion100Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = read_csv(ROOT / 'data/score_coding_proposals.csv')
        cls.p = {(r['company_id'],r['score_field']):r for r in cls.rows}
        cls.payload = build_web_payload(ROOT)
        cls.certs = {(r['candidate_id'],r['standard']):r for r in read_csv(ROOT/'evidence/certificate_register.csv')}

    def test_exactly100_unique_complete15_field_assessments(self):
        sample = {r['company_id'] for r in read_csv(ROOT/'data/company_intelligence.csv')}
        self.assertEqual(len(sample),100)
        self.assertEqual(len(self.rows),1500)
        self.assertEqual(len(self.p),1500)
        self.assertEqual({r['company_id'] for r in self.rows},sample)
        for cid in sample:
            self.assertEqual({r['score_field'] for r in self.rows if r['company_id']==cid},set(SCORE_FIELDS))
        self.assertEqual(validate(ROOT),[])

    def test_blank_fields_and_review_records_remain_honest(self):
        for r in self.rows:
            self.assertFalse(r['reviewer'] or r['review_date'] or r['review_note'])
            if r['proposed_value']:
                self.assertEqual(r['proposal_status'],'CHECKED')
            else:
                self.assertEqual((r['proposal_status'],r['proposal_confidence']),('NEEDS_RESEARCH','UNKNOWN'))
                self.assertTrue(r['missing_fact'])
        s=self.payload['field_assessment_summary']
        self.assertEqual((s['complete_company_count'],s['assessed_field_count']),(100,1500))
        self.assertEqual((s['checked_fields'],s['needs_research_fields'],s['approved_fields']),(599,901,0))
        self.assertEqual(s['awaiting_human_review_fields'],0)

    def test_duplicate_or_unknown_fields_cannot_inflate_completion(self):
        companies=[{'company_id':'X','legal_entity':'Example'}]
        rows=[dict(company_id='X',score_field=f,proposal_status='NEEDS_RESEARCH') for f in SCORE_FIELDS]
        self.assertEqual(field_assessment_summary(companies,rows,[])['complete_company_count'],1)
        duplicate=rows+[copy.deepcopy(rows[0])]
        summary=field_assessment_summary(companies,duplicate,[])
        self.assertEqual((summary['complete_company_count'],summary['assessed_field_count']),(0,14))
        rows[0]['score_field']='invented_field'
        self.assertEqual(field_assessment_summary(companies,rows,[])['assessed_field_count'],14)

    def test_final_ranked16_reproduce_frozen_pre_enrichment_selection(self):
        companies,_,research=build_outputs(ROOT)
        source=read_csv(ROOT/'tests/fixtures/source_register_before_completion100.csv')
        process=read_csv(ROOT/'tests/fixtures/company_process_map_before_completion100.csv')
        work=generate_score_work_queue(companies,build_score_readiness(ROOT,companies),process,source,
            read_csv(ROOT/'evidence/qa_review.csv'),read_csv(ROOT/'data/pilot_coded.csv'),research,
            [r for r in read_csv(ROOT/'data/history/score_coding_proposals_before_recheck_20261007.csv') if r['company_id'] not in set(REGULAR)|GATED])
        selected=select_batch(generate_company_work_priority(work,source,process),'NBCC-2026-10-07-07','2026-10-07',size=16)
        frozen=[r for r in read_csv(ROOT/'data/coding_batch_selections.csv') if r['batch_id']=='NBCC-2026-10-07-07']
        self.assertEqual(selected,frozen)
        self.assertEqual([r['company_id'] for r in selected],REGULAR)

    def test_gate_cohort_is_separate_and_still_blocked_after15_fields(self):
        regular={r['company_id'] for r in read_csv(ROOT/'data/coding_batch_selections.csv')}
        gate=read_csv(ROOT/'data/eligibility_coding_selections.csv')
        self.assertEqual({r['company_id'] for r in gate},GATED)
        self.assertEqual(len(gate),12)
        self.assertFalse(regular&GATED)
        initial={'P04','P05','P11','P12','P16','P18','P19','P20','P22','P23','P24','P53'}
        self.assertEqual(len(regular|GATED|initial),100)
        self.assertFalse(regular&initial)
        company={c['company_id']:c for c in self.payload['companies']}
        for cid in GATED:
            self.assertEqual(company[cid]['score_readiness']['score_status'],'NOT_SCOREABLE_ELIGIBILITY')
            self.assertEqual(company[cid]['workflow_priority']['workflow_action'],'ELIGIBILITY_FIRST')
            for row in [r for r in self.rows if r['company_id']==cid]:
                self.assertIn('upstream group eligibility remains OPEN_GATE',row['evidence_basis'])
        self.assertEqual(self.payload['field_assessment_summary']['eligibility_gate_company_count'],12)

    def test_all_first_passes_exhaust_code_now_but_not_research(self):
        summary=self.payload['company_work_summary']
        self.assertEqual(summary['next_best_company']['company_id'],'')
        self.assertEqual(summary['workflow_action_counts'],{'ELIGIBILITY_FIRST':12,'RESEARCH_FIRST':88})
        self.assertNotIn('READY_TO_CODE',self.payload['score_work_summary']['task_status_counts'])
        with self.assertRaises(ValueError):
            select_batch(read_csv(ROOT/'outputs/company_work_priority.csv'),'empty','2026-10-07')

    def test_swiss_group_temperature_and_certificate_not_inherited(self):
        for f in ['temperature_fit_score','management_gap_score','fossil_heat_displacement_score']:
            self.assertEqual(self.p['P88',f]['proposal_status'],'NEEDS_RESEARCH')
        self.assertEqual(self.p['P88','process_electrification_score']['proposed_value'],'7')
        self.assertNotEqual(self.certs['P88','ISO 14001']['certificate_status'],'VALID')

    def test_owner_equipment_page_confirms_furnaces_without_inheriting_max_temperature(self):
        mapping=next(r for r in read_csv(ROOT/'data/company_process_map.csv') if r['company_id']=='P89')
        self.assertEqual(mapping['process_id'],'PR007')
        c=next(c for c in self.payload['companies'] if c['company_id']=='P89')
        self.assertTrue(c['opportunities'])
        self.assertTrue(c['sources'])
        for f in ['temperature_fit_score','fossil_heat_displacement_score']:
            self.assertEqual(self.p['P89',f]['proposal_status'],'NEEDS_RESEARCH')
        self.assertEqual(self.p['P89','process_electrification_score']['proposed_value'],'7')
        self.assertIn('Inert-gas atmosphere',self.p['P89','power_conversion_score']['evidence_basis'])

    def test_certificates_use_actual_bodies_and_distinct_expiries(self):
        for cid,standard,end in [('P47','ISO 50001','2028-06-04'),('P47','ISO 14001','2028-03-14'),('P62','ISO 50001','2027-11-27'),('P07','ISO 14001','2029-07-25'),('P96','ISO 14001','2029-04-30'),('P104','ISO 14001','2026-11-14')]:
            r=self.certs[cid,standard]
            self.assertEqual((r['certificate_status'],r['valid_until']),('VALID',end))
        r=self.certs['P42','ISO 14001']
        self.assertEqual((r['certificate_status'],r['valid_until']),('EXPIRED','2026-07-27'))
        self.assertEqual(self.p['P42','management_gap_score']['proposed_value'],'3')
        self.assertEqual(self.certs['P46','ISO 50001']['valid_from'],'')
        for cid in ['P46','P47','P62','P104']:
            self.assertEqual(self.p[cid,'management_gap_score']['proposed_value'],'0')

    def test_building_heat_and_dated_awards_do_not_become_recent_process_investments(self):
        self.assertEqual(self.p['P71','investment_gap_score']['proposed_value'],'2')
        for f in ['temperature_fit_score','fossil_heat_displacement_score','thermal_storage_flex_score']:
            self.assertEqual(self.p['P71',f]['proposal_status'],'NEEDS_RESEARCH')
        for cid in ['P73','P10','P40']:
            self.assertEqual(self.p[cid,'investment_gap_score']['proposal_status'],'NEEDS_RESEARCH')
        self.assertEqual(self.p['P03','temperature_fit_score']['proposed_value'],'10')

    def test_zero_fossil_displacement_requires_affirmative_heat_baseline(self):
        row=self.p['P32','fossil_heat_displacement_score']
        self.assertEqual(row['proposed_value'],'0')
        self.assertIn('all brewery heat from woodchips',row['evidence_basis'])
        for cid in ['P40','P73','P107']:
            self.assertEqual(self.p[cid,'fossil_heat_displacement_score']['proposal_status'],'NEEDS_RESEARCH')


if __name__=='__main__':
    unittest.main()
