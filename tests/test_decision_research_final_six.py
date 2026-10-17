"""Exhausted opportunity queues must not hide firms with open field work."""
import csv,json,shutil,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
import decision_research as d
import source_content_review as review

class FinalSixTests(unittest.TestCase):
    def test_work_rank_fallback_blocks_gates_prior_and_duplicates(self):
        def row(cid,rank,status='RESEARCH_NEEDED',gap='heat'):
            return dict(company_id=cid,work_rank=str(rank),task_status=status,research_gap_fields=gap)
        queue=[row('A',5),row('G',1,'OPEN_GATE'),row('G',2),row('I',3),row('A',6),row('B',7),row('C',4,'READY_TO_CODE')]
        actual=d.select_field_companies(queue,2,{'I'})
        self.assertEqual([(r['company_id'],r['research_rank']) for r in actual],[('A','5'),('B','7')])
        self.assertTrue(all(r['queue_source']=='SCORE_WORK_QUEUE' for r in actual))

    def test_all_sample_firms_profiled_with_exactly_60_frozen_gaps(self):
        self.assertEqual(d.validate(ROOT),[])
        self.assertEqual({r['company_id'] for r in d.profiles(ROOT)},{r['company_id'] for r in d.rows(ROOT,'data/company_intelligence.csv')})
        selected=d.rows(ROOT,'data/decision_research_selections_20261017b.csv')
        self.assertEqual([r['company_id'] for r in selected],['P24','P23','P35','P87','P90','P106'])
        fields=d.rows(ROOT,'evidence/field_research_deep_20261017b.csv')
        self.assertEqual(len(fields),60);self.assertTrue(all(r['outcome']=='STILL_UNKNOWN' for r in fields))
        before={(r['company_id'],r['score_field']):r for r in d.rows(ROOT,'data/history/score_coding_proposals_before_deep_20261017b.csv')}
        current={(r['company_id'],r['score_field']):r for r in d.rows(ROOT,'data/score_coding_proposals.csv')}
        for key,p in before.items():
            if p['proposal_status']=='CHECKED' and key not in {(r['company_id'],r['score_field']) for r in d.checked_reassessments(ROOT)}:self.assertEqual(p,current[key])
        for f in fields:
            p=current[f['company_id'],f['score_field']];self.assertEqual(p['proposed_value'],'');self.assertEqual(p['proposal_confidence'],'UNKNOWN')
        for p in json.loads((ROOT/'evidence/decision_research_profiles_20261017b.json').read_text()):
            self.assertEqual(p['selection_count'],6);self.assertEqual(p['queue_source'],'SCORE_WORK_QUEUE');self.assertEqual(p['final_score_approval'],'NOT_GRANTED')
        for sid in ('S-P87-04','S-P87-05','S-P90-02'):
            self.assertEqual(review.checks(ROOT)[sid]['content_review_status'],'CONTEXT_ONLY')

    def test_fallback_rejects_unconsumed_opportunity_and_hidden_rank_origin(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            for name in ('data','evidence'):shutil.copytree(ROOT/name,root/name)
            p=root/'data/history/research_queue_before_deep_20261017b.csv'
            rs=d.rows(root,str(p.relative_to(root)));r=rs[0].copy();r.update(company_id='P24',missing_fact='heat',research_rank='0');rs.append(r)
            with p.open('w',newline='') as f:
                w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)
            self.assertTrue(any('requires exhausted' in e for e in d.validate(root)))
            p=root/'data/decision_research_selections_20261017b.csv';rs=d.rows(root,str(p.relative_to(root)));rs[0]['queue_source']='RESEARCH_QUEUE'
            with p.open('w',newline='') as f:
                w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)
            self.assertTrue(any('work-rank provenance' in e for e in d.validate(root)))

if __name__=='__main__':unittest.main()
