"""Batch ordering, immutable history and field-level uncertainty contracts."""
import copy
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from select_coding_batch import select_batch, append_selection
from company_work_priority import generate_company_work_priority, read_csv
from run_pipeline import build_outputs, build_score_readiness
from score_work_queue import generate_score_work_queue
from score_companies import SCORE_FIELDS
from export_web_data import build_web_payload


def candidate(cid, rank=1):
    return dict(company_id=cid, coding_rank=str(rank), workflow_action='CODE_NOW',
                qa_result='PASS', open_gate_tasks='0', priority_version='2.0.0')


class BatchSelectionTests(unittest.TestCase):
    def test_selection_uses_live_rank_and_ignores_blocked_workflows(self):
        blocked = dict(candidate('P01'), workflow_action='ELIGIBILITY_FIRST', coding_rank='')
        rows = select_batch([candidate('P31', 2), blocked, candidate('P30', 1)], 'batch', '2026-10-06')
        self.assertEqual([r['company_id'] for r in rows], ['P30', 'P31'])
        self.assertEqual([r['selection_rank'] for r in rows], ['1', '2'])
        self.assertTrue(all('reviewer' not in r and 'proposed_value' not in r for r in rows))

    def test_selection_rejects_failed_qa_or_open_gates(self):
        for change in [{'qa_result': 'FAIL'}, {'qa_result': 'UNKNOWN'}, {'open_gate_tasks': '1'}]:
            with self.assertRaises(ValueError):
                select_batch([dict(candidate('P30'), **change)], 'batch', '2026-10-06')

    def test_selection_rejects_missing_or_duplicate_ranks_and_companies(self):
        for rows in [[candidate('P30', 2)], [candidate('P30'), candidate('P31')],
                     [candidate('P30'), candidate('P30', 2)]]:
            with self.assertRaises(ValueError):
                select_batch(rows, 'batch', '2026-10-06')

    def test_invalid_batch_parameters_and_empty_queue_fail_closed(self):
        for batch_id, day, size in [('', '2026-10-06', 2), ('x', '2026-02-30', 2), ('x', '2026-10-06', 0)]:
            with self.assertRaises(ValueError):
                select_batch([candidate('P30')], batch_id, day, size)
        with self.assertRaises(ValueError):
            select_batch([], 'x', '2026-10-06')

    def test_small_remaining_queue_produces_a_smaller_batch(self):
        self.assertEqual(len(select_batch([candidate('P30')], 'x', '2026-10-06', 5)), 1)

    def test_append_keeps_earlier_batches_and_exact_retry_preserves_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'selections.csv'
            first = select_batch([candidate('P21')], 'first', '2026-10-06')
            second = select_batch([candidate('P30')], 'second', '2026-10-06')
            append_selection(path, first)
            append_selection(path, second)
            frozen = path.read_bytes()
            append_selection(path, first)
            self.assertEqual(path.read_bytes(), frozen)
            self.assertEqual(read_csv(path), first + second)
            changed = copy.deepcopy(first)
            changed[0]['company_id'] = 'P99'
            with self.assertRaises(ValueError):
                append_selection(path, changed)
            self.assertEqual(path.read_bytes(), frozen)

    def test_second_batch_reconstructs_before_new_source_enrichment(self):
        manifest = [r for r in read_csv(ROOT / 'data/coding_batch_selections.csv')
                    if r['batch_id'] == 'NBCC-2026-10-06-02']
        self.assertEqual(len(manifest), 2)
        companies, _, queue = build_outputs(ROOT)
        process = read_csv(ROOT / 'tests/fixtures/company_process_map_before_20261006_audit.csv')
        new_sources = {'S-P30-03', 'S-P30-04', 'S-P30-05', 'S-P31-03', 'S-P31-04'}
        sources = [r for r in read_csv(ROOT / 'tests/fixtures/source_register_before_20261006_audit.csv') if r['source_id'] not in new_sources]
        work = generate_score_work_queue(companies, build_score_readiness(ROOT, companies), process, sources,
            read_csv(ROOT / 'evidence/qa_review.csv'), read_csv(ROOT / 'data/pilot_coded.csv'), queue,
            [r for r in read_csv(ROOT / 'data/score_coding_proposals.csv') if r['company_id'] not in {'P30', 'P31'}])
        priority = generate_company_work_priority(work, sources, process)
        self.assertEqual(select_batch(priority, 'NBCC-2026-10-06-02', '2026-10-06'), manifest)

    def test_new_assessments_preserve_review_and_research_gates(self):
        all_rows = read_csv(ROOT / 'data/score_coding_proposals.csv')
        for cid in ['P30', 'P31']:
            rows = [r for r in all_rows if r['company_id'] == cid]
            self.assertEqual(len(rows), 15)
            self.assertEqual({r['score_field'] for r in rows}, set(SCORE_FIELDS))
            self.assertEqual(sum(r['proposal_status'] == 'AWAITING_HUMAN_REVIEW' for r in rows), 7)
            for row in rows:
                self.assertEqual(row['reviewer'], '')
                self.assertEqual(row['review_date'], '')
                if row['proposal_status'] == 'NEEDS_RESEARCH':
                    self.assertEqual(row['proposed_value'], '')
                    self.assertEqual(row['proposal_confidence'], 'UNKNOWN')
                    self.assertTrue(row['missing_fact'])
            for path in ['data/pilot_coded.csv', 'outputs/pilot_scored.csv']:
                self.assertNotIn(cid, {r['company_id'] for r in read_csv(ROOT / path)})

    def test_emas_claim_and_temperature_constrained_maturation_do_not_close_gaps(self):
        rows = {(r['company_id'], r['score_field']): r for r in read_csv(ROOT / 'data/score_coding_proposals.csv')}
        self.assertEqual(rows['P30', 'management_gap_score']['proposed_value'], '3')
        self.assertIn('validity remains unresolved', rows['P30', 'management_gap_score']['evidence_basis'])
        for cid in ['P30', 'P31']:
            self.assertEqual(rows[cid, 'thermal_storage_flex_score']['proposal_status'], 'NEEDS_RESEARCH')
            self.assertEqual(rows[cid, 'process_electrification_score']['proposal_status'], 'NEEDS_RESEARCH')
        self.assertEqual(rows['P31', 'fossil_heat_displacement_score']['proposed_value'], '0')
        self.assertIn('documented baseline', rows['P31', 'fossil_heat_displacement_score']['evidence_basis'])

    def test_web_history_separates_frozen_selection_from_live_status_without_scores(self):
        batches = build_web_payload(ROOT)['coding_batches']
        self.assertEqual(len(batches), 3)
        batch = next(b for b in batches if b["batch_id"] == "NBCC-2026-10-06-02")
        self.assertEqual([r['company_id'] for r in batch['companies']], ['P30', 'P31'])
        for company in batch['companies']:
            self.assertEqual(company['selection_rank'], 1 if company['company_id'] == 'P30' else 2)
            self.assertEqual(company['current_workflow_action'], 'RESEARCH_FIRST')
            self.assertEqual(company['awaiting_human_review_fields'], 7)
            self.assertEqual(company['needs_research_fields'], 8)
            self.assertEqual(company['expected_information_gain_at_selection'], 'HIGH')
            self.assertNotIn('score', company)
            self.assertNotIn('proposal_total', company)
