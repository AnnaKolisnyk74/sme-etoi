"""Correct later source scope while retaining dated profiles and open gates."""
import json,shutil,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
import decision_research as d
from export_web_data import build_web_payload

class DecisionFollowupTests(unittest.TestCase):
    def test_followup_retains_exact_previous_profile_and_does_not_inflate_field_work(self):
        self.assertEqual(d.validate(ROOT),[])
        old={p['company_id']:p for p in json.loads((ROOT/'data/history/decision_profiles_before_followup_20261017c.json').read_text())}
        latest={p['company_id']:p for p in d.profiles(ROOT)}
        for cid,p in old.items():
            self.assertEqual(latest[cid]['previous_profile_sha256'],d.profile_digest(p))
            self.assertEqual(latest[cid]['workstream'],p['workstream'])
            self.assertEqual(latest[cid]['final_score_approval'],'NOT_GRANTED')
        s=d.summary(ROOT)
        self.assertEqual((s['profile_count'],s['field_attempt_count'],s['new_checked_field_count']),(100,904,71))
        self.assertEqual((s['followup_count'],s['latest_followup']['company_count'],s['latest_followup']['entity_clarified_company_count']),(27,3,0))

    def test_complete_embedded_imprint_supersedes_footer_conflict_without_moving_assets(self):
        p=next(p for p in d.profiles(ROOT) if p['company_id']=='P95')
        self.assertEqual(p['outcome'],'ENTITY_IDENTIFIED_ASSET_SCOPE_OPEN')
        self.assertEqual(p['verified_legal_entity'],'Winkler Bräu GmbH & Co. KG')
        self.assertIn('HRB8374',p['finding']);self.assertIn('HRA13022',p['finding'])
        self.assertIn('separat',p['finding'])
        b=d.source_checks(ROOT)['S-P95-09'];self.assertIn('api.text.bnamic.com',b['source_url'])
        shell=d.source_checks(ROOT)['S-P95-07'];self.assertIn('loading placeholder',shell['relevant_location'])
        historic=next(p for _,ps in d.batches(ROOT) for p in ps if p['company_id']=='P95')
        self.assertEqual(historic['outcome'],'ENTITY_CONFLICT')
        payload=build_web_payload(ROOT);c=next(c for c in payload['companies'] if c['company_id']=='P95')
        self.assertEqual(c['legal_entity'],'Winkler-Bräu GmbH & Co. KG')
        self.assertEqual((payload['field_assessment_summary']['checked_fields'],payload['field_assessment_summary']['needs_research_fields']),(667,833))

    def test_two_headcounts_and_partial_gates_remain_distinct_from_annual_work_units(self):
        payload=build_web_payload(ROOT);by={c['company_id']:c for c in payload['companies']}
        for cid in ['P07','P10','P104','P47']:
            task=next(t for t in by[cid]['research_tasks'] if t['missing_fact']=='sme_eligibility')
            self.assertEqual(task['task_status'],'RECHECK_DUE');self.assertEqual(task['last_resulting_value'],'UNRESOLVED')
        p=by['P47']['decision_research_profile'];self.assertIn('1181',p['finding']);self.assertIn('1180',p['finding']);self.assertIn('Jahresarbeitseinheiten',p['finding'])
        attempts=d.rows(ROOT,'evidence/research_source_attempts_followup_20261017c.csv')
        challenge=next(a for a in attempts if 'eur-lex' in a['source_url'])
        self.assertEqual((challenge['http_status'],challenge['content_kind'],challenge['content_review_status'],challenge['selected_source_id']),('202','HTML','ACCESS_CHALLENGE',''))
        code=next(a for a in attempts if a['content_kind']=='JAVASCRIPT')
        self.assertEqual(code['content_review_status'],'DISCOVERY_CODE_ONLY');self.assertFalse(code['selected_source_id'])

    def test_followup_rejects_rewritten_history_new_identity_and_false_approval(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t)
            for f in ['data','evidence']:shutil.copytree(ROOT/f,root/f)
            path=root/'evidence/decision_research_followups_20261017c.json';original=json.loads(path.read_text())
            for change,expected in [(lambda p:p.update(previous_profile_sha256='0'*64),'follow-up provenance'),(lambda p:p.update(company_id='P999'),'follow-up provenance'),(lambda p:p.update(final_score_approval='GRANTED'),'personal approval')]:
                rows=json.loads(json.dumps(original));change(rows[0]);path.write_text(json.dumps(rows));self.assertTrue(any(expected in e for e in d.validate(root)))

if __name__=='__main__':unittest.main()
