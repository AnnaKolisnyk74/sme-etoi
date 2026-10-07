"""Validity, historical continuity and evidence boundaries for the October 7 batch."""
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


class CodingBatch0407Tests(unittest.TestCase):
    def test_frozen_selection_reproduces_before_evidence_enrichment(self):
        manifest = [r for r in read_csv(ROOT / 'data/coding_batch_selections.csv')
                    if r['batch_id'] == 'NBCC-2026-10-07-01']
        companies, _, research = build_outputs(ROOT)
        sources = read_csv(ROOT / 'tests/fixtures/source_register_before_nbcc0407.csv')
        process = read_csv(ROOT / 'tests/fixtures/company_process_map_before_nbcc0407.csv')
        proposals = [r for r in read_csv(ROOT / 'data/score_coding_proposals.csv')
                     if r['company_id'] not in {'P25', 'P15'}]
        work = generate_score_work_queue(companies, build_score_readiness(ROOT, companies),
            process, sources, read_csv(ROOT / 'evidence/qa_review.csv'),
            read_csv(ROOT / 'data/pilot_coded.csv'), research, proposals)
        ranking = generate_company_work_priority(work, sources, process)
        self.assertEqual(select_batch(ranking, 'NBCC-2026-10-07-01', '2026-10-07'), manifest)
        self.assertEqual([r['company_id'] for r in manifest], ['P25', 'P15'])
        self.assertEqual([r['verified_source_count'] for r in manifest], ['3', '2'])

    def test_fifteen_fields_preserve_pending_review_and_blank_research_contracts(self):
        all_rows = read_csv(ROOT / 'data/score_coding_proposals.csv')
        for cid, count in [('P25', 8), ('P15', 4)]:
            rows = [r for r in all_rows if r['company_id'] == cid]
            self.assertEqual(len(rows), 15)
            self.assertEqual({r['score_field'] for r in rows}, set(SCORE_FIELDS))
            self.assertEqual(sum(r['proposal_status'] == 'AWAITING_HUMAN_REVIEW' for r in rows), count)
            for row in rows:
                self.assertFalse(row['reviewer'] or row['review_date'])
                self.assertIn('AI-assisted', row['coder'])
                if row['proposal_status'] == 'NEEDS_RESEARCH':
                    self.assertEqual(row['proposed_value'], '')
                    self.assertEqual(row['proposal_confidence'], 'UNKNOWN')
                    self.assertTrue(row['missing_fact'])
            for f in ['data/pilot_coded.csv', 'outputs/pilot_scored.csv']:
                self.assertNotIn(cid, {r['company_id'] for r in read_csv(ROOT / f)})

    def test_direct_successor_preserves_expired_history_without_claiming_an_enms(self):
        sources = {r['source_id']: r for r in read_csv(ROOT / 'evidence/source_register.csv')}
        certs = {(r['candidate_id'], r['standard']): r
                 for r in read_csv(ROOT / 'evidence/certificate_register.csv')}
        cert = certs['P25', 'ISO 14001']
        self.assertEqual(cert['certificate_status'], 'VALID')
        self.assertEqual(cert['certificate_number'], '12 104 23864 TMS')
        self.assertEqual(cert['valid_from'], '2024-03-06')
        self.assertEqual(cert['valid_until'], '2027-02-26')
        self.assertEqual(cert['review_status'], 'RESEARCHED')
        self.assertEqual(cert['direct_certificate_url'], sources['S-P25-06']['source_link'])
        self.assertEqual(sources['S-P25-04']['link_check_status'], 'VERIFIED_EXPIRED')
        self.assertEqual(certs['P25', 'ISO 50001']['certificate_status'], 'NOT_FOUND_AFTER_CHECK')
        company = next(r for r in read_csv(ROOT / 'data/company_intelligence.csv') if r['company_id'] == 'P25')
        for field in ['energy_management_deployed', 'thermal_storage_deployed',
                      'battery_storage_deployed', 'industrial_heat_electrification_deployed',
                      'heat_recovery_deployed', 'power_quality_solution_deployed']:
            self.assertEqual(company[field], 'UNKNOWN')

    def test_retrievable_old_extract_does_not_become_current_quantitative_proof(self):
        sources = {r['source_id']: r for r in read_csv(ROOT / 'evidence/source_register.csv')}
        self.assertEqual(sources['S-P25-02']['link_check_status'], 'CONTENT_REVIEW_REQUIRED')
        recovery = next(r for r in read_csv(ROOT / 'evidence/source_recovery.csv') if r['company_id'] == 'P25')
        self.assertEqual(recovery['resolution_status'], 'PARTIAL_REPLACEMENT')
        self.assertIn('not reproduced', recovery['remaining_gap'])
        self.assertEqual(recovery['reviewer'], '')
        proposals = {(r['company_id'], r['score_field']): r
                     for r in read_csv(ROOT / 'data/score_coding_proposals.csv')}
        for field in ['temperature_fit_score', 'process_electrification_score',
                      'fossil_heat_displacement_score', 'thermal_storage_flex_score',
                      'incremental_load_score', 'investment_gap_score']:
            self.assertEqual(proposals['P25', field]['proposal_status'], 'NEEDS_RESEARCH')
        self.assertIn('closing force', proposals['P25', 'temperature_fit_score']['missing_fact'])

    def test_historical_cooling_and_self_report_do_not_close_deployment_or_investment_gaps(self):
        proposals = {(r['company_id'], r['score_field']): r
                     for r in read_csv(ROOT / 'data/score_coding_proposals.csv')}
        for field in ['temperature_fit_score', 'process_electrification_score',
                      'thermal_storage_flex_score', 'measures_gap_score',
                      'automation_control_score', 'investment_gap_score']:
            self.assertEqual(proposals['P15', field]['proposal_status'], 'NEEDS_RESEARCH')
        investment = proposals['P15', 'investment_gap_score']['missing_fact']
        self.assertIn('2016', investment)
        self.assertIn('2021-10-07 to 2026-10-07', investment)
        management = proposals['P15', 'management_gap_score']
        self.assertEqual(management['proposed_value'], '3')
        self.assertEqual(management['proposal_confidence'], 'C')
        self.assertIn('self-reported', management['evidence_basis'])
        self.assertIn('not a certified EnMS', management['evidence_basis'])
        company = next(r for r in read_csv(ROOT / 'data/company_intelligence.csv') if r['company_id'] == 'P15')
        self.assertEqual(company['energy_management_deployed'], 'UNKNOWN')
        self.assertEqual(company['thermal_storage_deployed'], 'UNKNOWN')

    def test_web_history_keeps_original_rank_and_field_counts_without_score_total(self):
        payload = build_web_payload(ROOT)
        batch = next(b for b in payload['coding_batches'] if b['batch_id'] == 'NBCC-2026-10-07-01')
        self.assertEqual([r['company_id'] for r in batch['companies']], ['P25', 'P15'])
        for r, numeric, gaps in zip(batch['companies'], [8, 4], [7, 11]):
            self.assertEqual(r['current_workflow_action'], 'RESEARCH_FIRST')
            self.assertEqual(r['awaiting_human_review_fields'], numeric)
            self.assertEqual(r['needs_research_fields'], gaps)
            self.assertEqual(r['expected_information_gain_at_selection'], 'MEDIUM')
            self.assertNotIn('score', r)
            self.assertNotIn('proposal_total', r)
        self.assertEqual(payload['company_work_summary']['next_best_company']['company_id'], 'P35')
