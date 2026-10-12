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
from decision_research import profiles, rows, select_companies, validate, summary, checked_reassessments
from export_web_data import build_web_payload

REASSESSMENT_KEYS = {(r['company_id'], r['score_field']) for r in checked_reassessments(ROOT)}


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
                         (54, 40, 12, 2))
        self.assertEqual((s['field_attempt_count'], s['new_checked_field_count'],
                          s['still_unknown_field_count']), (325, 26, 299))
        baseline = rows(ROOT, 'data/history/score_coding_proposals_before_deep_20261008.csv')
        current = {(p['company_id'], p['score_field']): p
                   for p in rows(ROOT, 'data/score_coding_proposals.csv')}
        for p in baseline:
            if p['proposal_status'] == 'CHECKED' and (p['company_id'], p['score_field']) not in REASSESSMENT_KEYS:
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
                        'data/score_coding_proposals.csv',
                        'data/history/score_coding_proposals_before_deep_20261011.csv',
                        'evidence/checked_field_reassessments_20261011.csv',
                        'evidence/decision_source_checks_20261011.csv']:
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
            if p['proposal_status'] == 'CHECKED' and (p['company_id'], p['score_field']) not in REASSESSMENT_KEYS:
                self.assertEqual(current[p['company_id'], p['score_field']], p)
        s = summary(ROOT)
        self.assertEqual(s['batches'][0]['field_attempt_count'], 50)
        self.assertEqual(s['batches'][1]['field_attempt_count'], 96)
        self.assertEqual(s['batches'][1]['new_checked_field_count'], 6)
        self.assertEqual(s['batches'][1]['still_unknown_field_count'], 90)
        self.assertEqual((s['latest_batch']['field_attempt_count'],
                          s['latest_batch']['new_checked_field_count'],
                          s['latest_batch']['still_unknown_field_count']), (78, 5, 73))
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
                            'evidence/checked_field_reassessments_*.csv',
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

    def test_new_sources_correct_only_explicitly_audited_checked_anchors(self):
        old = {(p['company_id'], p['score_field']): p for p in rows(
            ROOT, 'data/history/score_coding_proposals_before_deep_20261011.csv')}
        current = {(p['company_id'], p['score_field']): p for p in rows(
            ROOT, 'data/score_coding_proposals.csv')}
        decisions = {(r['company_id'], r['score_field']): r for r in checked_reassessments(ROOT)}
        changed = {k for k in old if old[k]['proposal_status'] == 'CHECKED' and old[k] != current[k]}
        self.assertEqual(changed, set(decisions))
        self.assertEqual({k[1]: (r['previous_value'], r['checked_value']) for k, r in decisions.items()},
                         {'automation_control_score': ('1','3'), 'measures_gap_score': ('7','0'),
                          'targets_gap_score': ('3','2'), 'investment_gap_score': ('3','2')})
        for key, r in decisions.items():
            self.assertEqual(r['previous_evidence_basis'], old[key]['evidence_basis'])
            self.assertEqual(r['checked_evidence_basis'], current[key]['evidence_basis'])
        self.assertEqual(summary(ROOT)['batches'][2]['reassessed_checked_field_count'], 4)

    def test_historical_machine_data_are_not_current_fuel_or_recent_capex(self):
        proposals = {(p['company_id'], p['score_field']): p for p in rows(ROOT, 'data/score_coding_proposals.csv')}
        for field in ['fossil_heat_displacement_score', 'thermal_storage_flex_score', 'investment_gap_score']:
            self.assertEqual(proposals['P21', field]['proposal_status'], 'NEEDS_RESEARCH')
        self.assertEqual(proposals['P21', 'temperature_fit_score']['proposal_confidence'], 'C')
        self.assertIn('historical', proposals['P21', 'temperature_fit_score']['evidence_basis'])
        finding = next(p for p in profiles(ROOT) if p['company_id'] == 'P21')['finding']
        self.assertIn('30.11.2018', finding)
        self.assertIn('außerhalb', finding)

    def test_historical_cooling_does_not_become_present_fuel_storage_or_capex(self):
        proposals = {(p['company_id'], p['score_field']): p
                     for p in rows(ROOT, 'data/score_coding_proposals.csv')}
        for field in ['motor_drive_score', 'power_conversion_score', 'power_quality_score']:
            row = proposals['P30', field]
            self.assertEqual(row['proposal_status'], 'CHECKED')
            self.assertEqual(row['proposal_confidence'], 'C')
            self.assertIn('S-P30-08', row['evidence_source_ids'])
        for field in ['fossil_heat_displacement_score', 'thermal_storage_flex_score',
                      'temperature_fit_score', 'process_electrification_score']:
            row = proposals['P30', field]
            self.assertEqual((row['proposal_status'], row['proposed_value']), ('NEEDS_RESEARCH', ''))
        # The older, separately supported cellar investment is not rewritten by the BHKW case.
        baseline = {(p['company_id'], p['score_field']): p for p in rows(
            ROOT, 'data/history/score_coding_proposals_before_deep_20261012.csv')}
        self.assertEqual(proposals['P30', 'investment_gap_score'],
                         baseline['P30', 'investment_gap_score'])

    def test_network_intent_and_second_staging_portal_do_not_assert_operating_assets(self):
        proposals = {(p['company_id'], p['score_field']): p
                     for p in rows(ROOT, 'data/score_coding_proposals.csv')}
        intent = proposals['P33', 'measures_gap_score']
        self.assertEqual((intent['proposed_value'], intent['proposal_confidence']), ('7', 'C'))
        self.assertIn('intention tier', intent['evidence_basis'])
        self.assertEqual(proposals['P33', 'investment_gap_score']['proposal_status'], 'NEEDS_RESEARCH')
        staging = [p for (cid, _), p in proposals.items() if cid == 'P38'
                   and p['proposal_status'] == 'NEEDS_RESEARCH']
        self.assertEqual(len(staging), 13)
        self.assertTrue(all(not p['proposed_value'] and p['proposal_confidence'] == 'UNKNOWN'
                            for p in staging))
        canonical = next(r for r in rows(ROOT, 'data/company_intelligence.csv')
                         if r['company_id'] == 'P38')
        self.assertEqual(canonical['pv_present'], 'UNKNOWN')
        profile = next(p for p in profiles(ROOT) if p['company_id'] == 'P38')
        self.assertIn('TEST-SYSTEM', profile['finding'])
        self.assertIn('S-P38-05', profile['source_ids'])

    def test_changed_checked_baseline_requires_an_explicit_before_after_trail(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            for pattern in ['evidence/decision_research_profiles_*.json', 'evidence/decision_source_checks_*.csv',
                            'evidence/field_research_deep_*.csv', 'data/decision_research_selections_*.csv',
                            'data/history/*_before_deep_*.csv', 'evidence/source_register.csv',
                            'data/score_coding_proposals.csv']:
                for source in ROOT.glob(pattern):
                    dest = root / source.relative_to(ROOT)
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(source, dest)
            self.assertTrue(any('without a later reassessment' in e for e in validate(root)))
            path = 'evidence/checked_field_reassessments_20261011.csv'
            shutil.copyfile(ROOT / path, root / path)
            self.assertEqual(validate(root), [])


if __name__ == '__main__':
    unittest.main()
