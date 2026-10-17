"""Repeated field research retains frozen scope and closes only supported gaps."""
import json,csv,shutil,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
import decision_research as d
import source_content_review as review

class FieldFollowupTests(unittest.TestCase):
    def test_22_frozen_gaps_close_only_two_brewery_pv_fields(self):
        self.assertEqual(d.validate(ROOT),[])
        fields=d.rows(ROOT,'evidence/field_research_followup_20261017d.csv')
        self.assertEqual(len(fields),22)
        closed={(r['company_id'],r['score_field']) for r in fields if r['outcome']=='NEW_EVIDENCE'}
        self.assertEqual(closed,{('P32','onsite_integration_score'),('P32','investment_gap_score')})
        before={(p['company_id'],p['score_field']):p for p in d.rows(ROOT,'data/history/score_coding_proposals_before_followup_20261017d.csv')}
        now={(p['company_id'],p['score_field']):p for p in d.rows(ROOT,'data/score_coding_proposals.csv')}
        self.assertTrue(all(p==now[k] for k,p in before.items() if p['proposal_status']=='CHECKED'))
        for k in closed:
            self.assertEqual((before[k]['proposal_status'],now[k]['proposed_value'],now[k]['proposal_status']),('NEEDS_RESEARCH','2','CHECKED'))
            self.assertFalse(now[k]['reviewer']);self.assertIn('OPEN_GATE',now[k]['evidence_basis'])
        s=d.summary(ROOT);self.assertEqual((s['profile_count'],s['field_attempt_count'],s['new_checked_field_count'],s['still_unknown_field_count']),(100,863,67,796))

    def test_plans_badge_and_social_lead_do_not_become_owned_commissioned_assets(self):
        current={(p['company_id'],p['score_field']):p for p in d.rows(ROOT,'data/score_coding_proposals.csv')}
        for field in ['management_gap_score','thermal_storage_flex_score','targets_gap_score']:
            self.assertEqual(current['P32',field]['proposal_status'],'NEEDS_RESEARCH')
        for p in current.values():
            if p['company_id']=='P13' and p['score_field'] in {'onsite_integration_score','investment_gap_score'}:self.assertEqual(p['proposal_status'],'NEEDS_RESEARCH')
        self.assertEqual(review.checks(ROOT)['S-P13-10']['content_review_status'],'CONTEXT_ONLY')
        self.assertIn('planned',review.checks(ROOT)['S-P32-04']['scope_note'])
        profiles={p['company_id']:p for p in d.profiles(ROOT)}
        self.assertIn('arc GmbH',profiles['P42']['finding']);self.assertEqual(profiles['P40']['outcome'],'FINANCIAL_AND_OWNERSHIP_OPEN')
        self.assertTrue(all(p['final_score_approval']=='NOT_GRANTED' for p in profiles.values()))

    def test_dropped_field_attempt_or_missing_baseline_fails_closed(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t)
            for name in ['data','evidence']:shutil.copytree(ROOT/name,root/name)
            path=root/'evidence/field_research_followup_20261017d.csv';rs=d.rows(root,str(path.relative_to(root)));rs.pop()
            with path.open('w',newline='') as h:
                w=csv.DictWriter(h,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)
            self.assertTrue(any('follow-up field attempts' in e for e in d.validate(root)))
            (root/'data/history/score_coding_proposals_before_followup_20261017d.csv').unlink()
            self.assertTrue(any('follow-up field attempts' in e for e in d.validate(root)))

if __name__=='__main__':unittest.main()
