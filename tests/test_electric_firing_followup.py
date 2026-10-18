"""Installed heat equipment must not become invented new grid demand."""
import csv,json,shutil,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
import decision_research as d
from export_web_data import build_web_payload
class ElectricFiringFollowupTests(unittest.TestCase):
 def test_four_exact_new_anchors_and_only_five_declared_prior_reassessments(self):
  before={(r['company_id'],r['score_field']):r for r in d.rows(ROOT,'data/history/score_coding_proposals_before_followup_20261018.csv')}
  now={(r['company_id'],r['score_field']):r for r in d.rows(ROOT,'data/score_coding_proposals.csv')}
  fields=d.rows(ROOT,'evidence/field_research_followup_20261018.csv')
  closed={(r['company_id'],r['score_field']) for r in fields if r['outcome']=='NEW_EVIDENCE'}
  self.assertEqual(closed,{('P43','temperature_fit_score'),('P43','process_electrification_score'),('P43','power_conversion_score'),('P65','fossil_heat_displacement_score')})
  self.assertEqual(len(fields),25)
  reass=d.rows(ROOT,'evidence/checked_field_reassessments_20261018.csv');keys={(r['company_id'],r['score_field']) for r in reass}
  changed={k for k,p in before.items() if p['proposal_status']=='CHECKED' and p!=now[k]}
  self.assertEqual(changed,keys);self.assertEqual(len(changed),5)
  self.assertEqual(sum(p['proposal_status']=='CHECKED' and p==now[k] for k,p in before.items()),659)
  for k in closed:self.assertEqual(before[k]['proposal_status'],'NEEDS_RESEARCH');self.assertEqual(now[k]['proposal_status'],'CHECKED')
  self.assertEqual(d.validate(ROOT),[])
 def test_actual_electric_kilns_reopen_extra_load_without_zero_or_fossil_absence(self):
  p={(r['company_id'],r['score_field']):r for r in d.rows(ROOT,'data/score_coding_proposals.csv')}
  self.assertEqual((p['P109','incremental_load_score']['proposal_status'],p['P109','incremental_load_score']['proposed_value'],p['P109','incremental_load_score']['proposal_confidence']),('NEEDS_RESEARCH','','UNKNOWN'))
  self.assertTrue(p['P109','incremental_load_score']['missing_fact'])
  self.assertEqual(p['P109','temperature_fit_score']['proposed_value'],'10')
  self.assertEqual(p['P109','fossil_heat_displacement_score']['proposal_status'],'NEEDS_RESEARCH')
  checks={r['source_id']:r for r in d.rows(ROOT,'evidence/decision_source_checks_20261018.csv')}
  self.assertIn('TF3-1600',checks['S-P43-14']['scope_note']);self.assertIn('6800/8000W',checks['S-P43-15']['scope_note'])
  self.assertIn('not an actual current production setpoint',p['P43','temperature_fit_score']['evidence_basis'])
  self.assertEqual(p['P43','investment_gap_score']['proposal_status'],'NEEDS_RESEARCH')
  self.assertIn('OPEN_GATE',p['P65','fossil_heat_displacement_score']['evidence_basis'])
 def test_withdrawal_requires_matching_status_gap_and_before_after_provenance(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp)
   for f in ['data','evidence']:shutil.copytree(ROOT/f,root/f)
   path=root/'data/score_coding_proposals.csv';rows=d.rows(root,'data/score_coding_proposals.csv');r=next(p for p in rows if (p['company_id'],p['score_field'])==('P109','incremental_load_score'));r['missing_fact']=''
   with path.open('w',newline='') as h:
    w=csv.DictWriter(h,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
   self.assertTrue(any('reassessment provenance' in e for e in d.validate(root)))
   shutil.copyfile(ROOT/'data/score_coding_proposals.csv',path)
   (root/'evidence/checked_field_reassessments_20261018.csv').unlink()
   self.assertTrue(any('without a later reassessment' in e for e in d.validate(root)))
 def test_web_exposes_reopening_and_keeps_approval_and_canonical_flags_separate(self):
  p=build_web_payload(ROOT);s=p['decision_research_summary'];f=s['latest_followup']
  self.assertEqual((s['field_attempt_count'],s['new_checked_field_count'],s['still_unknown_field_count']),(933,74,859))
  self.assertEqual((f['company_count'],f['field_attempt_count'],f['new_checked_field_count'],f['still_unknown_field_count'],f['reassessed_checked_field_count'],f['reopened_field_count']),(3,29,3,26,0,0))
  c=next(c for c in p['companies'] if c['company_id']=='P109');r=next(r for r in c['score_proposals'] if r['score_field']=='incremental_load_score')
  self.assertIsNone(r['proposed_value']);self.assertEqual(r['check_history'][-1]['outcome'],'NEEDS_RESEARCH')
  self.assertEqual(r['check_history'][-1]['original_value'],'5');self.assertTrue(r['check_history'][-1]['original_evidence_basis'])
  self.assertEqual((p['field_assessment_summary']['checked_fields'],p['field_assessment_summary']['needs_research_fields'],p['field_assessment_summary']['approved_fields']),(670,830,0))
  self.assertTrue(all(c['score_readiness']['score_status']!='FINAL_SCORE_READY' for c in p['companies']))
if __name__=='__main__':unittest.main()
