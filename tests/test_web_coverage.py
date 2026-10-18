"""Verify complete register/history export without changing canonical facts."""
import sys
import unittest
from pathlib import Path
from collections import Counter
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from export_web_data import build_web_payload, read_csv
from score_companies import DIMENSIONS

class WebCoverageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p = build_web_payload(ROOT)

    def test_full_register_keys_and_sample_boundaries(self):
        sources = [s for c in self.p['companies'] for s in c['sources']] + self.p['additional_sources']
        expected = read_csv(ROOT, 'evidence/source_register.csv')
        self.assertEqual(Counter(s['source_id'] for s in sources), Counter(s['source_id'] for s in expected))
        self.assertEqual(len(sources), 673)
        self.assertEqual(len(self.p['additional_sources']), 26)
        sample = {c['company_id'] for c in self.p['companies']}
        self.assertTrue(all(s['company_id'] not in sample and not s['sample_member'] for s in self.p['additional_sources']))
        certs = [(c['company_id'], r['standard']) for c in self.p['companies'] for r in c['certificate_checks']]
        certs += [(r['company_id'], r['standard']) for r in self.p['additional_certificate_checks']]
        self.assertEqual(Counter(certs), Counter((r['candidate_id'],r['standard']) for r in read_csv(ROOT,'evidence/certificate_register.csv')))
        self.assertEqual(len(certs),321)
        self.assertEqual(len(self.p['additional_certificate_checks']),21)

    def test_findings_and_all_field_checks_preserve_history(self):
        self.assertEqual(self.p['research_findings'],read_csv(ROOT,'data/research_results.csv'))
        self.assertEqual(len(self.p['research_findings']),105)
        self.assertEqual(sum(r['resulting_value']=='YES' for r in self.p['research_findings']),16)
        checks = [r for c in self.p['companies'] for p in c['score_proposals'] for r in p['check_history']]
        originals = read_csv(ROOT,'evidence/score_proposal_checks.csv')
        self.assertEqual(Counter(tuple(sorted(r.items())) for r in checks if not r.get('is_reassessment')),Counter(tuple(sorted(r.items())) for r in originals))
        self.assertEqual(len(checks),685)
        self.assertEqual(sum(r['outcome']=='REASSESSED' for r in checks),8)
        self.assertEqual(sum(p['proposal_status']=='NEEDS_RESEARCH' for c in self.p['companies'] for p in c['score_proposals']),830)

    def test_methodology_libraries_qa_and_canonical_values(self):
        self.assertEqual(self.p['scoring_methodology']['dimensions'],DIMENSIONS)
        self.assertEqual(self.p['scoring_methodology']['maximum_total'],100)
        for key,file,count in [('technologies','technology_library',8),('processes','process_library',13),('opportunity_rules','opportunity_rules',9)]:
            self.assertEqual(self.p['reference_libraries'][key],read_csv(ROOT,f'data/{file}.csv'))
            self.assertEqual(len(self.p['reference_libraries'][key]),count)
        q=self.p['quality_assurance']
        self.assertEqual(q['company_checks'],read_csv(ROOT,'evidence/qa_review.csv'))
        self.assertEqual(sum(q['independent_review_status_counts'].values()),100)
        self.assertEqual(len(q['reliability']),16)
        self.assertTrue(all(r['completed_pairs']=='0' and r['percent_agreement']=='UNKNOWN' and r['cohens_kappa']==('NOT_APPLICABLE' if r['field']=='__OVERALL__' else 'UNKNOWN') for r in q['reliability']))
        canonical={r['company_id']:r for r in read_csv(ROOT,'data/company_intelligence.csv')}
        for c in self.p['companies']:
            for k,v in c['canonical_deployments'].items(): self.assertEqual(v,canonical[c['company_id']][k])
            self.assertEqual(c['last_verified_date'],canonical[c['company_id']]['last_verified_date'])
        self.assertEqual(len(self.p['documentation_links']),15)
        self.assertIn('evidence/decision_research_followup_20261017c.md', {r['path'] for r in self.p['documentation_links']})

if __name__=='__main__': unittest.main()
