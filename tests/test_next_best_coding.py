"""Behavioral tests for documentary priority, safeguards and frozen batch selection."""
import copy
import csv
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from company_work_priority import generate_company_work_priority, read_csv
from run_pipeline import build_outputs, build_score_readiness
from score_work_queue import generate_score_work_queue
from score_companies import DIMENSIONS, SCORE_FIELDS


def tasks(cid, confidence='B', qa='PASS', status='READY_TO_CODE'):
    return [dict(company_id=cid, legal_entity=cid, evidence_confidence=confidence,
                 process_confidence=confidence, qa_result=qa, task_status=status,
                 work_priority='P2', work_rank=str(i), company_work_rank='999',
                 task_type='CODE_DIMENSION', missing_fields=' | '.join(fields),
                 proposal_covered_fields='', dimension=dimension)
            for i, (dimension, fields) in enumerate(DIMENSIONS.items(), 1)]


def source(cid, url, kind='company_profile', verified=True):
    return dict(candidate_id=cid, source_id=f'{cid}-{url}', source_link=url,
                final_url=url, evidence_fact='Documented scope', source_type=kind,
                link_check_status='VERIFIED' if verified else 'EXISTS_ACCESS_CHALLENGE')


def mapping(cid, url):
    return dict(company_id=cid, process_evidence_url=url,
                process_evidence_note='Firm-specific process', confidence='B')


class NextBestCodingTests(unittest.TestCase):
    def test_documentary_gain_outweighs_raw_source_volume_and_company_id(self):
        work = tasks('P01') + tasks('P99')
        sources = [source('P01', str(i)) for i in range(20)] + [source('P99', 'technical', 'company_energy_page')]
        rows = generate_company_work_priority(work, sources, [mapping('P01', '0'), mapping('P99', 'technical')])
        self.assertEqual(rows[0]['company_id'], 'P99')
        self.assertEqual(rows[0]['expected_information_gain'], 'HIGH')
        self.assertEqual(rows[0]['unassessed_field_count'], '15')

    def test_stronger_confidence_precedes_documentary_gain(self):
        rows = generate_company_work_priority(tasks('P01', 'A') + tasks('P99', 'C'),
            [source('P99', 'x', 'company_energy_page')], [mapping('P99', 'x')])
        self.assertEqual(rows[0]['company_id'], 'P01')

    def test_qa_failure_or_missing_qa_blocks_next_flag(self):
        for qa in ['FAIL', 'NOT_RECORDED', '']:
            rows = generate_company_work_priority(tasks('P01', qa=qa) + tasks('P99'))
            by_id = {r['company_id']: r for r in rows}
            self.assertEqual(by_id['P01']['workflow_action'], 'QA_FIRST')
            self.assertEqual(by_id['P01']['coding_rank'], '')
            self.assertEqual(by_id['P99']['is_next_to_code'], 'YES')

    def test_duplicate_urls_do_not_inflate_priority(self):
        work = tasks('P01')
        sources = [source('P01', 'same', 'company_energy_page')]
        before = generate_company_work_priority(work, sources, [mapping('P01', 'same')])
        after = generate_company_work_priority(work, sources * 20, [mapping('P01', 'same')])
        self.assertEqual(before, after)
        self.assertEqual(after[0]['verified_source_count'], '1')

    def test_unverified_or_foreign_sources_do_not_create_coverage(self):
        row = generate_company_work_priority(tasks('P01'),
            [source('P01', 'x', 'company_energy_page', False), source('P99', 'y', 'company_energy_page')],
            [mapping('P01', 'x'), mapping('P01', 'y')])[0]
        self.assertEqual(row['source_coverage'], '')
        self.assertEqual(row['expected_information_gain'], 'UNKNOWN')

    def test_identity_only_sources_do_not_prove_process_coverage(self):
        row = generate_company_work_priority(tasks('P01'), [source('P01', 'identity')], [mapping('P01', 'different')])[0]
        self.assertEqual(row['expected_information_gain'], 'LOW')
        self.assertEqual(row['coverage_source_ids'], '')

    def test_partial_coding_does_not_claim_complete_review(self):
        work = tasks('P01')
        work[0]['task_status'] = 'AWAITING_HUMAN_REVIEW'
        row = generate_company_work_priority(work)[0]
        self.assertEqual(row['workflow_action'], 'IN_PROGRESS')
        self.assertEqual(row['is_next_to_code'], 'NO')

    def test_input_order_and_inherited_ranks_cannot_change_coding_order(self):
        work = tasks('P99') + tasks('P02')
        before = generate_company_work_priority(work)
        changed = copy.deepcopy(work)
        for r in changed:
            r['company_work_rank'] = '1' if r['company_id'] == 'P99' else '100'
            r['work_rank'] = str(100 - int(r['work_rank']))
        after = generate_company_work_priority(list(reversed(changed)))
        self.assertEqual([r['company_id'] for r in before], [r['company_id'] for r in after])
        self.assertEqual(before[0]['company_id'], 'P02')

    def test_priority_never_mutates_facts_or_produces_numeric_scores(self):
        work = tasks('P01')
        original = copy.deepcopy(work)
        rows = generate_company_work_priority(work)
        self.assertEqual(work, original)
        self.assertTrue(set(SCORE_FIELDS).isdisjoint(rows[0]))
        self.assertNotIn('opportunity_score', rows[0])

    def test_frozen_batch_reconstructs_from_pre_assessment_inputs(self):
        manifest = [r for r in read_csv(ROOT / 'data/coding_batch_selections.csv') if r['batch_id'] == 'NBCC-2026-10-06-01']
        selected = {r['company_id'] for r in manifest}
        companies, _, queue = build_outputs(ROOT)
        process = read_csv(ROOT / 'data/company_process_map.csv')
        sources = [r for r in read_csv(ROOT / 'evidence/source_register.csv') if r['source_id'] not in {'S-P21-04', 'S-P27-04'}]
        work = generate_score_work_queue(companies, build_score_readiness(ROOT, companies), process, sources,
            read_csv(ROOT / 'evidence/qa_review.csv'), read_csv(ROOT / 'data/pilot_coded.csv'), queue,
            [r for r in read_csv(ROOT / 'data/score_coding_proposals.csv') if r['company_id'] not in selected])
        ranking = generate_company_work_priority(work, sources, process)
        for selection, row in zip(manifest, ranking):
            self.assertEqual(selection['company_id'], row['company_id'])
            self.assertEqual(selection['selection_rank'], row['coding_rank'])
            for field in ['priority_version', 'expected_information_gain', 'source_coverage', 'verified_source_count', 'coverage_source_ids', 'priority_reason']:
                self.assertEqual(selection[field], row[field])
        self.assertEqual(selected, {'P21', 'P27'})

    def test_batch_assessments_keep_unknowns_and_human_review_separate(self):
        rows = read_csv(ROOT / 'data/score_coding_proposals.csv')
        for cid, count in [('P21', 4), ('P27', 5)]:
            proposals = [r for r in rows if r['company_id'] == cid]
            self.assertEqual(len(proposals), 15)
            self.assertEqual({r['score_field'] for r in proposals}, set(SCORE_FIELDS))
            self.assertEqual(sum(r['proposal_status'] == 'AWAITING_HUMAN_REVIEW' for r in proposals), count)
            for row in proposals:
                self.assertEqual(row['reviewer'], '')
                self.assertEqual(row['review_date'], '')
                if row['proposal_status'] == 'NEEDS_RESEARCH':
                    self.assertEqual(row['proposed_value'], '')
                    self.assertEqual(row['proposal_confidence'], 'UNKNOWN')
                    self.assertTrue(row['missing_fact'])
            for path in ['data/pilot_coded.csv', 'outputs/pilot_scored.csv']:
                self.assertNotIn(cid, {r['company_id'] for r in read_csv(ROOT / path)})
