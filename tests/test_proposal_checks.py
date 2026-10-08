"""Meaningful safeguards for evidence rechecks, corrections and unchanged approval gates."""
import copy
import csv
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
import proposal_checks
from validate_score_coding_proposals import validate
from company_work_priority import company_action
from score_work_queue import proposal_state_for_dimension
from export_web_data import build_web_payload


def write(path, rows):
    with path.open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


class ProposalCheckTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.current = proposal_checks.rows(ROOT / 'data/score_coding_proposals.csv')
        cls.by_key = {(r['company_id'], r['score_field']): r for r in cls.current}
        cls.checks = proposal_checks.rows(ROOT / 'evidence/score_proposal_checks.csv')

    def test_all554_original_numeric_decisions_are_accounted_for(self):
        self.assertEqual(validate(ROOT), [])
        summary = proposal_checks.summary(ROOT)
        self.assertEqual(summary['reviewed_proposal_count'], 554)
        self.assertEqual(summary['outcome_counts'], {'CONFIRMED': 507, 'CORRECTED': 42, 'NEEDS_RESEARCH': 5})
        self.assertEqual(summary['source_check_count'], 269)
        self.assertEqual(summary['retrievable_source_count'], 266)
        self.assertEqual(summary['checked_by'], 'Codex')
        self.assertEqual(summary['final_score_approval'], 'NOT_GRANTED')
        self.assertEqual(sum(r['proposal_status'] == 'CHECKED' for r in self.current), 549)
        self.assertFalse(any(r['proposal_status'] == 'AWAITING_HUMAN_REVIEW' for r in self.current))
        self.assertTrue(all(not r['reviewer'] and not r['review_date'] and not r['review_note'] for r in self.current))

    def test_drive_and_unproven_buffers_no_longer_support_numeric_heat_values(self):
        missing = {('P23', 'temperature_fit_score'), ('P23', 'process_electrification_score'),
                   ('P04', 'thermal_storage_flex_score'), ('P05', 'thermal_storage_flex_score'),
                   ('P22', 'fossil_heat_displacement_score')}
        self.assertEqual({(r['company_id'], r['score_field']) for r in self.checks if r['outcome'] == 'NEEDS_RESEARCH'}, missing)
        for key in missing:
            row = self.by_key[key]
            self.assertEqual((row['proposal_status'], row['proposed_value'], row['proposal_confidence']),
                             ('NEEDS_RESEARCH', '', 'UNKNOWN'))
            self.assertTrue(row['missing_fact'])

    def test_planned_project_components_and_unknown2021_dates_are_not_recent_completed_projects(self):
        self.assertEqual(self.by_key['P22', 'measures_gap_score']['proposed_value'], '7')
        self.assertEqual(self.by_key['P22', 'investment_gap_score']['proposed_value'], '3')
        self.assertEqual(self.by_key['P93', 'investment_gap_score']['proposed_value'], '2')
        self.assertEqual(self.by_key['P04', 'investment_gap_score']['proposed_value'], '2')
        self.assertIn('planned', self.by_key['P22', 'process_electrification_score']['evidence_basis'])
        self.assertEqual(self.by_key['P05', 'fossil_heat_displacement_score']['proposed_value'], '4')
        for cid in ['P04', 'P05', 'P12', 'P16', 'P20']:
            self.assertEqual(self.by_key[cid, 'scheduling_flex_score']['proposed_value'], '2')

    def test_exact_expiry_updates_certificate_and_entity_flag_without_inventing_discontinuation(self):
        cert = next(r for r in proposal_checks.rows(ROOT / 'evidence/certificate_register.csv')
                    if r['candidate_id'] == 'P12' and r['standard'] == 'EMAS')
        company = next(r for r in proposal_checks.rows(ROOT / 'data/company_intelligence.csv') if r['company_id'] == 'P12')
        self.assertEqual((cert['certificate_status'], cert['valid_until'], company['emas_status']),
                         ('EXPIRED', '2026-09-11', 'EXPIRED'))
        self.assertEqual(self.by_key['P12', 'management_gap_score']['proposed_value'], '2')
        self.assertIn('discontinuation', cert['notes'])
        self.assertEqual(company['pv_present'], 'UNKNOWN')
        self.assertEqual(company['industrial_heat_electrification_deployed'], 'UNKNOWN')

    def test_checked_values_are_exported_separately_and_never_final_scores(self):
        payload = build_web_payload(ROOT)
        self.assertEqual(payload['field_assessment_summary']['checked_fields'], 549)
        self.assertEqual(payload['field_assessment_summary']['approved_fields'], 0)
        for company in payload['companies']:
            self.assertEqual(len(company['score_proposals']), 15)
            self.assertNotEqual(company['score_readiness']['independent_human_review_status'], 'APPROVED')
            self.assertNotEqual(company['score_readiness']['score_status'], 'FINAL_SCORE_READY')
        by_id = {c['company_id']: c for c in payload['companies']}
        row = next(p for p in by_id['P23']['score_proposals'] if p['score_field'] == 'temperature_fit_score')
        self.assertIsNone(row['proposed_value'])
        self.assertEqual(row['proposal_status'], 'NEEDS_RESEARCH')
        self.assertIn('S-P45-05', self.by_key['P45', 'onsite_integration_score']['evidence_source_ids'])
        self.assertEqual(payload['proposal_check_summary']['reviewed_proposal_count'], 554)

    def test_checked_work_does_not_reopen_first_pass_or_bypass_upstream_gate(self):
        proposals = {('X', 'motor_drive_score'): {'proposal_status': 'CHECKED'}}
        result = proposal_state_for_dimension('X', ['motor_drive_score'], proposals)
        self.assertEqual(result[0], 'CHECKED')
        self.assertEqual(company_action([{'task_status': 'CHECKED'}]), 'CHECKED_PROPOSALS')
        self.assertEqual(company_action([{'task_status': 'CHECKED'}, {'task_status': 'OPEN_GATE'}]), 'ELIGIBILITY_FIRST')
        proposals['X', 'power_conversion_score'] = {'proposal_status': 'NEEDS_RESEARCH', 'missing_fact': 'No converter evidence'}
        self.assertEqual(proposal_state_for_dimension('X', ['motor_drive_score', 'power_conversion_score'], proposals)[0], 'RESEARCH_NEEDED')
        proposals['X', 'power_conversion_score']['proposal_status'] = 'AWAITING_HUMAN_REVIEW'
        self.assertEqual(proposal_state_for_dimension('X', ['motor_drive_score', 'power_conversion_score'], proposals)[0], 'AWAITING_HUMAN_REVIEW')

    def _copy_validation_data(self, root):
        for rel in ['data/score_coding_proposals.csv', 'data/history/score_coding_proposals_before_recheck_20261007.csv',
                    'evidence/source_register.csv', 'evidence/score_proposal_checks.csv', 'evidence/proposal_source_checks.csv']:
            dest = root / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / rel, dest)

    def test_missing_ledger_or_body_hash_cannot_create_checked_status(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._copy_validation_data(root)
            checks = proposal_checks.rows(root / 'evidence/score_proposal_checks.csv')
            write(root / 'evidence/score_proposal_checks.csv', checks[1:])
            self.assertTrue(any('coverage' in e for e in validate(root)))
            write(root / 'evidence/score_proposal_checks.csv', checks)
            bodies = proposal_checks.rows(root / 'evidence/proposal_source_checks.csv')
            next(r for r in bodies if r['source_id'] == 'S-P03-03')['content_sha256'] = ''
            write(root / 'evidence/proposal_source_checks.csv', bodies)
            self.assertTrue(any('provenance' in e or 'reviewed attributable' in e for e in validate(root)))

    def test_stale_value_foreign_owner_and_fake_personal_review_fail_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._copy_validation_data(root)
            changed = copy.deepcopy(self.current)
            row = next(r for r in changed if r['company_id'] == 'P03' and r['score_field'] == 'temperature_fit_score')
            row['proposed_value'] = '7'
            write(root / 'data/score_coding_proposals.csv', changed)
            self.assertTrue(any('differs from check record' in e for e in validate(root)))
            row['proposed_value'] = '10'
            row['reviewer'], row['review_date'] = 'Anna', '2026-10-07'
            write(root / 'data/score_coding_proposals.csv', changed)
            self.assertTrue(any('personal approval' in e for e in validate(root)))
            write(root / 'data/score_coding_proposals.csv', self.current)
            bodies = proposal_checks.rows(root / 'evidence/proposal_source_checks.csv')
            next(r for r in bodies if r['source_id'] == 'S-P03-03')['company_id'] = 'P12'
            write(root / 'evidence/proposal_source_checks.csv', bodies)
            self.assertTrue(any('owner' in e for e in validate(root)))

    def test_http200_alone_and_unavailable_certificate_cannot_authenticate_maturity(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._copy_validation_data(root)
            bodies = proposal_checks.rows(root / 'evidence/proposal_source_checks.csv')
            next(r for r in bodies if r['source_id'] == 'S-P03-03')['content_review_status'] = 'NOT_CHECKED'
            write(root / 'evidence/proposal_source_checks.csv', bodies)
            self.assertTrue(any('reviewed attributable' in e for e in validate(root)))
            write(root / 'evidence/proposal_source_checks.csv', proposal_checks.rows(ROOT / 'evidence/proposal_source_checks.csv'))
            changed = copy.deepcopy(self.current)
            row = next(r for r in changed if r['company_id'] == 'P70' and r['score_field'] == 'management_gap_score')
            row['proposed_value'] = '0'
            checks = copy.deepcopy(self.checks)
            next(r for r in checks if r['company_id'] == 'P70' and r['score_field'] == 'management_gap_score')['checked_value'] = '0'
            write(root / 'data/score_coding_proposals.csv', changed)
            write(root / 'evidence/score_proposal_checks.csv', checks)
            self.assertTrue(any('reviewed attributable' in e for e in validate(root)))


if __name__ == '__main__':
    unittest.main()
