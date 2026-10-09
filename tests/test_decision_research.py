"""Decision ranking, ownership boundaries and newly closed evidence gaps."""
import copy
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from decision_research import profiles, rows, select_companies, validate, summary
from export_web_data import build_web_payload


class DecisionResearchTests(unittest.TestCase):
    def test_frozen_decision_queue_selects_ten_unique_unblocked_firms(self):
        queue = rows(ROOT, 'data/history/research_queue_before_deep_20261008.csv')
        chosen = select_companies(queue, identity_blocks={'P109', 'P110'})
        self.assertEqual([r['company_id'] for r in chosen],
                         ['P04','P05','P100','P12','P18','P25','P29','P76','P77','P78'])
        example = [{'company_id': c, 'missing_fact': f, 'research_rank': str(i)}
                   for i, (c, f) in enumerate([('G', 'sme_eligibility'),
                     ('I', 'heat'), ('G', 'heat'), ('A', 'heat'),
                     ('A', 'storage'), ('B', 'heat')], 1)]
        self.assertEqual([r['company_id'] for r in select_companies(example, 2, {'I'})],
                         ['A', 'B'])

    def test_all_fifty_selected_gaps_have_an_attributed_attempt(self):
        self.assertEqual(validate(ROOT), [])
        s = summary(ROOT)
        self.assertEqual((s['profile_count'], s['technical_company_count'],
                          s['eligibility_company_count'], s['identity_company_count']),
                         (34, 20, 12, 2))
        self.assertEqual((s['field_attempt_count'], s['new_checked_field_count'],
                          s['still_unknown_field_count']), (146, 8, 138))
        baseline = rows(ROOT, 'data/history/score_coding_proposals_before_deep_20261008.csv')
        current = {(p['company_id'], p['score_field']): p
                   for p in rows(ROOT, 'data/score_coding_proposals.csv')}
        for p in baseline:
            if p['proposal_status'] == 'CHECKED':
                self.assertEqual(current[p['company_id'], p['score_field']], p)
        new = [p for p in current.values() if p['company_id'] == 'P18'
               and p['score_field'] in {'motor_drive_score', 'automation_control_score'}]
        self.assertEqual({p['score_field']: p['proposed_value'] for p in new},
                         {'motor_drive_score': '5', 'automation_control_score': '3'})

    def test_ownership_signals_and_current_names_are_visible_without_false_sme_approval(self):
        data = build_web_payload(ROOT)
        by = {c['company_id']: c for c in data['companies']}
        for cid in ['P47', 'P88']:
            self.assertEqual(by[cid]['decision_research_profile']['outcome'], 'EXCLUSION_SIGNAL')
            self.assertEqual(by[cid]['score_readiness']['eligibility_gate'], 'UNRESOLVED')
        self.assertIn('Königliche', by['P109']['decision_research_profile']['verified_legal_entity'])
        self.assertEqual(by['P110']['decision_research_profile']['outcome'], 'ENTITY_CONFLICT')
        self.assertEqual(data['field_assessment_summary']['approved_fields'], 0)

    def test_found_deployment_is_not_an_unknown_to_non_deployment_inference(self):
        queue = rows(ROOT, 'outputs/research_queue.csv')
        found = {(q['company_id'], q['missing_fact']): q for q in queue
                 if q['task_status'] == 'EVIDENCE_FOUND'}
        self.assertEqual(set(found), {('P79','energy_management_deployed'), ('P100','heat_recovery_deployed'),
            ('P77','heat_recovery_deployed'), ('P77','energy_management_deployed')})
        self.assertTrue(all(q['last_resulting_value'] == 'YES' for q in found.values()))
        results = [r for r in rows(ROOT, 'data/research_results.csv')
                   if r['checked_date'] == '2026-10-08' and r['research_status'] == 'EVIDENCE_FOUND']
        self.assertEqual(len(results), 5)
        self.assertTrue(all(r['resulting_value'] == 'YES' for r in results))
        self.assertTrue(all(q['commercial_status'] != 'WHITE_SPACE_POSSIBLE' for q in queue))

    def test_foreign_sources_and_fabricated_personal_approval_fail_closed(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            for rel in ['evidence/decision_research_profiles_20261008.json',
                        'evidence/decision_source_checks_20261008.csv',
                        'evidence/source_register.csv', 'evidence/field_research_deep_20261008.csv',
                        'data/decision_research_selections_20261008.csv',
                        'data/history/research_queue_before_deep_20261008.csv',
                        'data/history/score_coding_proposals_before_deep_20261008.csv',
                        'data/score_coding_proposals.csv']:
                dest = root / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / rel, dest)
            self.assertEqual(validate(root), [])
            data = copy.deepcopy(profiles(root))
            data[0]['source_ids'] = ['S-P18-06']
            data[0]['final_score_approval'] = 'Anna approved'
            (root / 'evidence/decision_research_profiles_20261008.json').write_text(json.dumps(data))
            errors = validate(root)
            self.assertTrue(any('attributable body' in e for e in errors))
            self.assertTrue(any('personal approval' in e for e in errors))

    def test_later_block_preserves_checked_baseline_and_covers_every_selected_gap(self):
        baseline = rows(ROOT, 'data/history/score_coding_proposals_before_deep_20261009.csv')
        current = {(p['company_id'], p['score_field']): p
                   for p in rows(ROOT, 'data/score_coding_proposals.csv')}
        for p in baseline:
            if p['proposal_status'] == 'CHECKED':
                self.assertEqual(current[p['company_id'], p['score_field']], p)
        s = summary(ROOT)
        self.assertEqual(s['batches'][0]['field_attempt_count'], 50)
        self.assertEqual(s['latest_batch']['field_attempt_count'], 96)
        self.assertEqual(s['latest_batch']['new_checked_field_count'], 6)
        self.assertEqual(s['latest_batch']['still_unknown_field_count'], 90)
        self.assertEqual(validate(ROOT), [])

    def test_period_and_claim_boundaries_survive_pipeline_export(self):
        payload = build_web_payload(ROOT)
        by = {c['company_id']: c for c in payload['companies']}
        proposals = {(p['company_id'], p['score_field']): p
                     for p in rows(ROOT, 'data/score_coding_proposals.csv')}
        self.assertEqual(proposals['P03', 'investment_gap_score']['proposal_status'], 'NEEDS_RESEARCH')
        self.assertEqual(proposals['P99', 'scheduling_flex_score']['proposal_status'], 'NEEDS_RESEARCH')
        self.assertEqual(proposals['P97', 'management_gap_score']['proposed_value'], '3')
        self.assertEqual(by['P97']['certifications']['iso_50001'], 'NOT_FOUND_AFTER_CHECK')
        self.assertEqual(proposals['P98', 'investment_gap_score']['proposed_value'], '2')
        task = next(t for t in by['P79']['research_tasks']
                    if t['missing_fact'] == 'energy_management_deployed')
        self.assertEqual(task['task_status'], 'EVIDENCE_FOUND')
        self.assertEqual(task['last_resulting_value'], 'YES')
        canonical = next(c for c in rows(ROOT, 'data/company_intelligence.csv') if c['company_id'] == 'P79')
        self.assertEqual(canonical['energy_management_deployed'], 'UNKNOWN')

    def test_missing_later_snapshot_does_not_silently_drop_a_research_block(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            paths = [ROOT / 'evidence/source_register.csv', ROOT / 'data/score_coding_proposals.csv']
            for pattern in ['evidence/decision_research_profiles_*.json',
                            'evidence/decision_source_checks_*.csv',
                            'evidence/field_research_deep_*.csv',
                            'data/decision_research_selections_*.csv',
                            'data/history/*_before_deep_*.csv']:
                paths.extend(ROOT.glob(pattern))
            for source in paths:
                dest = root / source.relative_to(ROOT)
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, dest)
            self.assertEqual(validate(root), [])
            (root / 'data/history/research_queue_before_deep_20261009.csv').unlink()
            self.assertTrue(any('missing frozen selection or queue' in e for e in validate(root)))


if __name__ == '__main__':
    unittest.main()
