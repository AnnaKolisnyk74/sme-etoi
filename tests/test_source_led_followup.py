"""Repeat evidence research preserves old checks and separates public gaps from facts."""
import csv,json,shutil,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
import decision_research as d
from export_web_data import build_web_payload

REASSESSMENT_KEYS={(r['company_id'],r['score_field']) for r in d.checked_reassessments(ROOT)}

class SourceLedFollowupTests(unittest.TestCase):
    def test_ten_new_checks_have_frozen_unknown_predecessors_and_preserve_all654(self):
        before={(r['company_id'],r['score_field']):r for r in d.rows(ROOT,'data/history/score_coding_proposals_before_followup_20261017e.csv')}
        now={(r['company_id'],r['score_field']):r for r in d.rows(ROOT,'data/score_coding_proposals.csv')}
        attempts=d.rows(ROOT,'evidence/field_research_followup_20261017e.csv')
        closed={(r['company_id'],r['score_field']) for r in attempts if r['outcome']=='NEW_EVIDENCE'}
        expected={('P74','automation_control_score'),('P96','measures_gap_score'),('P107','fossil_heat_displacement_score'),('P107','investment_gap_score')}
        expected|={(c,'management_gap_score') for c in ['P28','P54','P57','P72','P84','P85']}
        self.assertEqual((len(before),len(attempts),len(closed)),(1500,85,10));self.assertEqual(closed,expected)
        self.assertEqual(sum(p['proposal_status']=='CHECKED' for p in before.values()),654)
        for key,p in before.items():
            if p['proposal_status']=='CHECKED' and key not in REASSESSMENT_KEYS:self.assertEqual(p,now[key])
        for key in closed:
            self.assertEqual(before[key]['proposal_status'],'NEEDS_RESEARCH');self.assertEqual(now[key]['proposal_status'],'CHECKED')
            self.assertFalse(any(now[key][f] for f in ['reviewer','review_date','review_note']))
        self.assertEqual(d.validate(ROOT),[])

    def test_public_gap_fives_do_not_authenticate_absent_internal_systems(self):
        scopes=d.rows(ROOT,'evidence/management_gap_checks_20261017e.csv');self.assertEqual(len(scopes),6)
        proposals={(p['company_id'],p['score_field']):p for p in d.rows(ROOT,'data/score_coding_proposals.csv')}
        sources={s['source_id']:s for s in d.rows(ROOT,'evidence/source_register.csv')}
        for row in scopes:
            cid=row['company_id'];p=proposals[cid,'management_gap_score']
            self.assertEqual(row['internal_system_status'],'UNKNOWN');self.assertEqual(row['final_score_approval'],'NOT_GRANTED')
            self.assertEqual(row['emas_register_date'],'2026-10-01');self.assertTrue(row['discovery_query'])
            self.assertEqual(sources[row['emas_source_id']]['candidate_id'],cid)
            self.assertEqual(p['proposal_confidence'],'C');self.assertEqual(p['proposed_value'],'2' if cid=='P72' else '5')
            self.assertIn('unknown',p['evidence_basis'].lower())
        p=proposals['P72','management_gap_score'];self.assertIn('not a verified current',p['evidence_basis'])
        self.assertIn('DEHOGA',proposals['P28','management_gap_score']['evidence_basis'])

    def test_project_publication_and_catalogue_ratings_do_not_close_other_fields(self):
        p={(r['company_id'],r['score_field']):r for r in d.rows(ROOT,'data/score_coding_proposals.csv')}
        for c,f in [('P04','thermal_storage_flex_score'),('P74','investment_gap_score'),('P74','thermal_storage_flex_score'),('P96','investment_gap_score'),('P96','temperature_fit_score'),('P96','thermal_storage_flex_score'),('P107','temperature_fit_score')]:
            self.assertEqual((p[c,f]['proposal_status'],p[c,f]['proposed_value']),('NEEDS_RESEARCH',''))
        self.assertEqual(p['P107','fossil_heat_displacement_score']['proposed_value'],'4')
        self.assertIn('2027',p['P107','investment_gap_score']['evidence_basis'])
        web=build_web_payload(ROOT);s=web['decision_research_summary']['latest_followup']
        self.assertEqual((s['company_count'],s['field_attempt_count'],s['new_checked_field_count'],s['still_unknown_field_count']),(3,29,3,26))
        self.assertEqual(web['field_assessment_summary']['approved_fields'],0)
        self.assertTrue(all(c['score_readiness']['score_status']!='FINAL_SCORE_READY' for c in web['companies']))

    def test_new_followup_rejects_dropped_attempt_and_rewritten_predecessor(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t)
            for name in ['data','evidence']:shutil.copytree(ROOT/name,root/name)
            path=root/'evidence/field_research_followup_20261017e.csv';rows=d.rows(root,str(path.relative_to(root)));rows.pop()
            with path.open('w',newline='') as h:
                w=csv.DictWriter(h,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
            self.assertTrue(any('follow-up field attempts' in e for e in d.validate(root)))
            profile=root/'evidence/decision_research_followups_20261017e.json';ps=json.loads(profile.read_text());ps[0]['previous_profile_sha256']='0'*64;profile.write_text(json.dumps(ps))
            self.assertTrue(any('follow-up provenance' in e for e in d.validate(root)))

if __name__=='__main__':unittest.main()
