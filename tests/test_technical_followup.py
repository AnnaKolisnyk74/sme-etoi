"""Technical follow-up keeps historical/office/planned evidence from becoming numbers."""
import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
import decision_research as d
from export_web_data import build_web_payload
class TechnicalFollowupTests(unittest.TestCase):
 def test_exact_frozen_gaps_and_all664_checked_rows_preserved(self):
  old={(p['company_id'],p['score_field']):p for p in d.rows(ROOT,'data/history/score_coding_proposals_before_followup_20261017f.csv')}
  now={(p['company_id'],p['score_field']):p for p in d.rows(ROOT,'data/score_coding_proposals.csv')}
  fields=d.rows(ROOT,'evidence/field_research_followup_20261017f.csv');keys={(r['company_id'],r['score_field']) for r in fields}
  expected={k for k,p in old.items() if k[0] in {'P29','P50','P77'} and p['proposal_status']=='NEEDS_RESEARCH'}
  self.assertEqual(keys,expected);self.assertEqual(len(fields),16)
  self.assertEqual(sum(p['proposal_status']=='CHECKED' for p in old.values()),664)
  for k,p in old.items():
   if p['proposal_status']=='CHECKED':self.assertEqual(p,now[k])
  for r in fields:
   p=now[r['company_id'],r['score_field']];self.assertEqual(r['outcome'],'STILL_UNKNOWN')
   self.assertEqual((p['proposal_status'],p['proposed_value'],p['proposal_confidence']),('NEEDS_RESEARCH','','UNKNOWN'))
   self.assertTrue(r['remaining_fact']);self.assertFalse(any(p[f] for f in ['reviewer','review_date','review_note']))
  self.assertEqual(d.validate(ROOT),[])
 def test_historical_store_and_office_ratings_have_explicit_source_boundaries(self):
  checks={r['source_id']:r for r in d.rows(ROOT,'evidence/decision_source_checks_20261017f.csv')}
  self.assertEqual(len(checks),8)
  for r in checks.values():
   self.assertEqual(r['content_review_status'],'RECHECKED');self.assertEqual(len(r['content_sha256']),64)
  self.assertIn('does not prove',checks['S-P29-05']['scope_note'])
  self.assertIn('minus14K',checks['S-P29-07']['scope_note']);self.assertIn('office',checks['S-P29-07']['scope_note'])
  self.assertIn('2023–2030',checks['S-P50-07']['scope_note'])
 def test_current_payload_contains_every_latest_field_and_source(self):
  p=build_web_payload(ROOT);s=p['decision_research_summary']
  self.assertEqual((s['field_attempt_count'],s['new_checked_field_count'],s['still_unknown_field_count']),(879,67,812))
  self.assertEqual((s['followup_count'],s['latest_followup']['company_count'],s['latest_followup']['field_attempt_count']),(24,3,16))
  self.assertEqual(s['latest_followup']['new_checked_field_count'],0)
  self.assertEqual((p['field_assessment_summary']['checked_fields'],p['field_assessment_summary']['needs_research_fields'],p['field_assessment_summary']['approved_fields']),(664,836,0))
if __name__=='__main__':unittest.main()
