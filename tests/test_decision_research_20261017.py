"""Regression checks for an honest zero-anchor continuation and source boundaries."""
import sys,unittest,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
import decision_research as d
from export_web_data import build_web_payload

class ResearchOctober17Tests(unittest.TestCase):
    def test_frozen_selection_and_all_75_gaps_preserve_unknown(self):
        selected=d.rows(ROOT,'data/decision_research_selections_20261017.csv')
        self.assertEqual([r['company_id'] for r in selected],['P84','P85','P86','P89','P91','P92','P93','P94','P95','P22'])
        fields=d.rows(ROOT,'evidence/field_research_deep_20261017.csv')
        self.assertEqual(len(fields),75);self.assertTrue(all(r['outcome']=='STILL_UNKNOWN' for r in fields))
        before={(r['company_id'],r['score_field']):r for r in d.rows(ROOT,'data/history/score_coding_proposals_before_deep_20261017.csv')}
        current={(r['company_id'],r['score_field']):r for r in d.rows(ROOT,'data/history/score_coding_proposals_before_followup_20261017e.csv')}
        for key,row in before.items():
            if row['proposal_status']=='CHECKED':self.assertEqual(row,current[key])
        for f in fields:
            p=current[f['company_id'],f['score_field']]
            self.assertEqual(p['proposed_value'],'');self.assertEqual(p['proposal_confidence'],'UNKNOWN');self.assertEqual(p['missing_fact'],f['remaining_fact'])
        self.assertEqual(d.validate(ROOT),[])

    def test_raw_access_failure_is_not_a_new_reviewed_body(self):
        profiles=json.loads((ROOT/'evidence/decision_research_profiles_20261017.json').read_text())
        p=next(p for p in profiles if p['company_id']=='P89')
        self.assertTrue(p['outcome'].startswith('SOURCE_ACCESS_'));self.assertEqual(p['source_ids'],[])
        attempts=d.rows(ROOT,'evidence/research_source_attempts_deep_20261017.csv')
        self.assertEqual(len(attempts),58)
        raw=[r for r in attempts if r['company_id']=='P89' and r['content_kind']!='EXTRACTED_WEB_TEXT']
        self.assertTrue(raw);self.assertTrue(all(r['http_status']=='466' and not r['selected_source_id'] for r in raw))
        extract=[r for r in attempts if r['content_kind']=='EXTRACTED_WEB_TEXT']
        self.assertEqual(len(extract),1);self.assertEqual(extract[0]['http_status'],'');self.assertEqual(extract[0]['selected_source_id'],'')
        self.assertFalse(any(r['company_id']=='P89' for r in d.rows(ROOT,'evidence/decision_source_checks_20261017.csv')))

    def test_date_entity_and_thermal_boundaries_are_visible_without_approval(self):
        p=build_web_payload(ROOT);by={c['company_id']:c for c in p['companies']}
        self.assertIn('2021',by['P92']['decision_research_profile']['finding']);self.assertIn('2023',by['P92']['decision_research_profile']['finding'])
        self.assertEqual(by['P95']['decision_research_profile']['outcome'],'ENTITY_IDENTIFIED_ASSET_SCOPE_OPEN')
        self.assertEqual(by['P95']['decision_research_profile']['verified_legal_entity'],'Winkler Bräu GmbH & Co. KG')
        self.assertNotEqual(by['P95']['legal_entity'],'Winkler Bräustüberl GmbH')
        self.assertEqual((p['field_assessment_summary']['checked_fields'],p['field_assessment_summary']['needs_research_fields']),(667,833))
        for cid in ['P84','P85','P86','P89','P91','P92','P93','P94','P95','P22']:
            self.assertEqual(by[cid]['decision_research_profile']['final_score_approval'],'NOT_GRANTED')
        latest=p['decision_research_summary']['batches'][-2];self.assertEqual((latest['field_attempt_count'],latest['new_checked_field_count'],latest['still_unknown_field_count']),(75,0,75))

if __name__=='__main__':unittest.main()
