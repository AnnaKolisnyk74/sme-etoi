import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from opportunity_engine import (
    commercial_status,
    generate_opportunities,
    prioritise,
    process_signal_present,
    worst_confidence,
)


class OpportunityEngineTests(unittest.TestCase):
    def setUp(self):
        self.companies = [
            {
                "company_id": "P10",
                "legal_entity": "Oskar Lehmann GmbH & Co. KG",
                "three_shift_operation": "YES",
                "multi_shift_or_batch_signal": "YES",
                "pv_present": "UNKNOWN",
                "public_load_profile_available": "NO",
                "iso_50001_status": "NOT_FOUND_AFTER_CHECK",
                "energy_management_deployed": "UNKNOWN",
                "flexibility_solution_deployed": "UNKNOWN",
                "heat_recovery_deployed": "UNKNOWN",
                "battery_storage_deployed": "UNKNOWN",
                "public_targets_summary": "Climate-neutrality-by-2030 initiative is publicly visible.",
                "evidence_confidence": "B",
            }
        ]
        self.process_map = [
            {"company_id": "P10", "process_id": "PR001", "confidence": "B"}
        ]
        self.processes = [
            {
                "process_id": "PR001",
                "process_name": "injection_moulding",
                "drive_relevance": "HIGH",
                "process_heat_relevance": "MEDIUM",
                "cooling_relevance": "HIGH",
                "schedulability": "MEDIUM",
                "thermal_inertia_storage": "MEDIUM",
                "power_electronics_relevance": "HIGH",
                "power_quality_relevance": "MEDIUM",
            }
        ]

    def test_process_signal_matching(self):
        self.assertTrue(process_signal_present(self.processes[0], "HIGH_drive_relevance"))
        self.assertTrue(process_signal_present(self.processes[0], "MEDIUM_schedulability"))
        self.assertFalse(process_signal_present(self.processes[0], "HIGH_process_heat_relevance"))

    def test_three_shift_injection_moulding_triggers_technical_relevance(self):
        rules = [
            {
                "rule_id": "R001",
                "opportunity_type": "energy_management",
                "required_process_signal": "HIGH_drive_relevance",
                "required_company_signal": "three_shift_operation",
                "blocking_signal": "",
                "output_level": "HIGH",
                "reason_template": "test reason",
                "confidence_cap": "B",
                "rule_status": "DRAFT",
            }
        ]
        rows = generate_opportunities(self.companies, self.process_map, self.processes, rules)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["technical_status"], "TECHNICALLY_RELEVANT")
        self.assertEqual(rows[0]["commercial_status"], "RESEARCH_REQUIRED")
        self.assertEqual(rows[0]["priority"], "RESEARCH")
        self.assertEqual(rows[0]["confidence"], "B")

    def test_deployed_technology_is_not_white_space(self):
        company = dict(self.companies[0])
        company["heat_recovery_deployed"] = "YES"
        status, field, value = commercial_status(company, "heat_recovery")
        self.assertEqual(status, "ALREADY_DEPLOYED")
        self.assertEqual(field, "heat_recovery_deployed")
        self.assertEqual(value, "YES")
        priority, _, action = prioritise(company, "heat_recovery", "HIGH", status, "B")
        self.assertEqual(priority, "LOW")
        self.assertIn("Monitor", action)

    def test_explicit_no_can_create_high_priority_white_space(self):
        company = dict(self.companies[0])
        company["energy_management_deployed"] = "NO"
        status, _, _ = commercial_status(company, "energy_management")
        priority, why, _ = prioritise(company, "energy_management", "HIGH", status, "B")
        self.assertEqual(status, "WHITE_SPACE_POSSIBLE")
        self.assertEqual(priority, "HIGH")
        self.assertIn("three-shift operation", why)
        self.assertIn("public transition target", why)

    def test_unknown_deployment_requires_research(self):
        status, _, value = commercial_status(self.companies[0], "energy_management")
        self.assertEqual(status, "RESEARCH_REQUIRED")
        self.assertEqual(value, "UNKNOWN")
        priority, _, action = prioritise(self.companies[0], "energy_management", "HIGH", status, "B")
        self.assertEqual(priority, "RESEARCH")
        self.assertIn("Verify whether energy management", action)

    def test_unmodelled_opportunity_requires_research(self):
        status, field, value = commercial_status(self.companies[0], "unmodelled_type")
        self.assertEqual(status, "RESEARCH_REQUIRED")
        self.assertEqual(field, "")
        self.assertEqual(value, "NOT_MODELLED")

    def test_flexibility_has_explicit_deployment_mapping(self):
        status, field, value = commercial_status(self.companies[0], "flexibility")
        self.assertEqual(status, "RESEARCH_REQUIRED")
        self.assertEqual(field, "flexibility_solution_deployed")
        self.assertEqual(value, "UNKNOWN")

    def test_blocking_signal_prevents_rule(self):
        company = dict(self.companies[0])
        company["pv_present"] = "YES"
        company["public_load_profile_available"] = "YES"
        rules = [
            {
                "rule_id": "R007",
                "opportunity_type": "battery_storage",
                "required_process_signal": "",
                "required_company_signal": "pv_present",
                "blocking_signal": "public_load_profile_available",
                "output_level": "RESEARCH_REQUIRED",
                "reason_template": "test reason",
                "confidence_cap": "C",
                "rule_status": "DRAFT",
            }
        ]
        rows = generate_opportunities([company], self.process_map, self.processes, rules)
        self.assertEqual(rows, [])

    def test_confidence_never_exceeds_weakest_input(self):
        self.assertEqual(worst_confidence("A", "B", "A"), "B")
        self.assertEqual(worst_confidence("A", "B", "C"), "C")


if __name__ == "__main__":
    unittest.main()
