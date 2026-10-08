# Historical first-pass assertions use the immutable pre-recheck snapshot.
"""Evidence-scope regression checks for the first batch after the full URL audit."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from company_work_priority import read_csv, generate_company_work_priority
from run_pipeline import build_outputs, build_score_readiness
from score_work_queue import generate_score_work_queue
from select_coding_batch import select_batch
from score_companies import SCORE_FIELDS
from export_web_data import build_web_payload


class CodingBatch03Tests(unittest.TestCase):
    def test_frozen_batch_reproduces_before_content_corrections(self):
        manifest = [r for r in read_csv(ROOT / 'data/coding_batch_selections.csv')
                    if r['batch_id'] == 'NBCC-2026-10-06-03']
        companies, _, research = build_outputs(ROOT)
        sources = read_csv(ROOT / 'tests/fixtures/source_register_before_nbcc03.csv')
        process = read_csv(ROOT / 'tests/fixtures/company_process_map_before_nbcc03.csv')
        proposals = [r for r in read_csv(ROOT / 'data/history/score_coding_proposals_before_recheck_20261007.csv')
                     if r['company_id'] not in {'P43', 'P13'}]
        work = generate_score_work_queue(companies, build_score_readiness(ROOT, companies),
            process, sources, read_csv(ROOT / 'evidence/qa_review.csv'),
            read_csv(ROOT / 'data/pilot_coded.csv'), research, proposals)
        ranking = generate_company_work_priority(work, sources, process)
        self.assertEqual(select_batch(ranking, 'NBCC-2026-10-06-03', '2026-10-06'), manifest)
        self.assertEqual([r['company_id'] for r in manifest], ['P43', 'P13'])

    def test_each_field_has_pending_review_or_a_precise_blank_valued_gap(self):
        rows = read_csv(ROOT / 'data/history/score_coding_proposals_before_recheck_20261007.csv')
        for cid in ['P43', 'P13']:
            assessment = [r for r in rows if r['company_id'] == cid]
            self.assertEqual({r['score_field'] for r in assessment}, set(SCORE_FIELDS))
            self.assertEqual(len(assessment), 15)
            self.assertEqual(sum(r['proposal_status'] == 'AWAITING_HUMAN_REVIEW'
                                 for r in assessment), 6)
            for row in assessment:
                self.assertFalse(row['reviewer'] or row['review_date'])
                if row['proposal_status'] == 'NEEDS_RESEARCH':
                    self.assertEqual(row['proposed_value'], '')
                    self.assertEqual(row['proposal_confidence'], 'UNKNOWN')
                    self.assertTrue(row['missing_fact'])
            for file in ['data/pilot_coded.csv', 'outputs/pilot_scored.csv']:
                self.assertNotIn(cid, {r['company_id'] for r in read_csv(ROOT / file)})

    def test_generic_homepage_is_blocked_but_named_profile_and_process_are_preserved(self):
        sources = {r['source_id']: r for r in read_csv(ROOT / 'evidence/source_register.csv')}
        self.assertEqual(sources['S-P43-02']['link_check_status'], 'CONTENT_REVIEW_REQUIRED')
        self.assertIn('/wzr-ceramic-solutions-gmbh', sources['S-P43-03']['source_link'])
        mapping = next(r for r in read_csv(ROOT / 'data/company_process_map.csv')
                       if r['company_id'] == 'P43')
        self.assertEqual(mapping['process_evidence_url'], sources['S-P43-04']['source_link'])

    def test_current_environment_certificate_does_not_become_an_enms_or_human_approval(self):
        certificates = {(r['candidate_id'], r['standard']): r
                        for r in read_csv(ROOT / 'evidence/certificate_register.csv')}
        certificate = certificates['P13', 'ISO 14001']
        self.assertEqual(certificate['certificate_status'], 'VALID')
        self.assertEqual(certificate['certificate_holder'], 'Schmalriede-Zink GmbH')
        self.assertEqual(certificate['certificate_number'], 'UM 22107-Z05101')
        self.assertEqual(certificate['valid_until'], '2029-02-20')
        self.assertEqual(certificate['review_status'], 'RESEARCHED')
        for standard in ['ISO 50001', 'EMAS']:
            self.assertEqual(certificates['P13', standard]['certificate_status'], 'NOT_FOUND_AFTER_CHECK')
        company = next(r for r in read_csv(ROOT / 'data/company_intelligence.csv')
                       if r['company_id'] == 'P13')
        self.assertEqual(company['energy_management_deployed'], 'UNKNOWN')
        proposals = {(r['company_id'], r['score_field']): r
                     for r in read_csv(ROOT / 'data/history/score_coding_proposals_before_recheck_20261007.csv')}
        self.assertEqual(proposals['P13', 'management_gap_score']['proposed_value'], '2')
        self.assertIn('achievement is UNKNOWN', proposals['P13', 'targets_gap_score']['evidence_basis'])

    def test_customer_savings_generic_ai_and_research_assets_do_not_close_site_gaps(self):
        proposals = {(r['company_id'], r['score_field']): r
                     for r in read_csv(ROOT / 'data/history/score_coding_proposals_before_recheck_20261007.csv')}
        for cid in ['P13', 'P43']:
            for field in ['temperature_fit_score', 'process_electrification_score',
                          'fossil_heat_displacement_score', 'thermal_storage_flex_score',
                          'incremental_load_score', 'onsite_integration_score', 'investment_gap_score']:
                self.assertEqual(proposals[cid, field]['proposal_status'], 'NEEDS_RESEARCH')
        self.assertEqual(proposals['P13', 'automation_control_score']['proposal_status'], 'NEEDS_RESEARCH')
        self.assertIn('customer PT-Keramik', proposals['P43', 'measures_gap_score']['evidence_basis'])
        self.assertIn('lower bounds', proposals['P43', 'temperature_fit_score']['missing_fact'])

    def test_web_history_distinguishes_frozen_rank_from_current_research_workflow(self):
        payload = build_web_payload(ROOT)
        batch = next(b for b in payload['coding_batches'] if b['batch_id'] == 'NBCC-2026-10-06-03')
        self.assertEqual([r['company_id'] for r in batch['companies']], ['P43', 'P13'])
        for r in batch['companies']:
            self.assertEqual(r['current_workflow_action'], 'RESEARCH_FIRST')
            self.assertEqual(r['checked_fields'], 6)
            self.assertEqual(r['needs_research_fields'], 9)
            self.assertNotIn('score', r)
            self.assertNotIn('proposal_total', r)

