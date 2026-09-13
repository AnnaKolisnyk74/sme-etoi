import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from research_queue import generate_research_queue


class ResearchQueueTests(unittest.TestCase):
    def setUp(self):
        self.companies = [
            {
                "company_id": "P07",
                "legal_entity": "VARIOPLAST Konrad Däbritz GmbH",
                "public_investments_summary": "Battery storage announced for 2025.",
                "source_urls": "https://example.com/company | https://example.com/announcement",
            },
            {
                "company_id": "P10",
                "legal_entity": "Oskar Lehmann GmbH & Co. KG",
                "iso_50001_status": "NOT_FOUND_AFTER_CHECK",
                "source_urls": "https://example.com/downloads",
            },
        ]
        self.rows = [
            {
                "company_id": "P10",
                "legal_entity": "Wrong market name",
                "rule_id": "R001",
                "opportunity_type": "energy_management",
                "opportunity_level": "HIGH",
                "technical_status": "TECHNICALLY_RELEVANT",
                "commercial_status": "RESEARCH_REQUIRED",
                "priority": "RESEARCH",
                "confidence": "B",
                "process_name": "injection_moulding",
                "deployment_field": "energy_management_deployed",
                "deployment_value": "UNKNOWN",
            },
            {
                "company_id": "P10",
                "legal_entity": "Oskar Lehmann GmbH & Co. KG",
                "rule_id": "R008",
                "opportunity_type": "flexibility",
                "opportunity_level": "MEDIUM",
                "technical_status": "TECHNICALLY_RELEVANT",
                "commercial_status": "RESEARCH_REQUIRED",
                "priority": "RESEARCH",
                "confidence": "B",
                "process_name": "injection_moulding",
                "deployment_field": "flexibility_solution_deployed",
                "deployment_value": "UNKNOWN",
            },
            {
                "company_id": "P07",
                "legal_entity": "VARIOPLAST Konrad Däbritz GmbH",
                "rule_id": "R007",
                "opportunity_type": "battery_storage",
                "opportunity_level": "RESEARCH_REQUIRED",
                "technical_status": "TECHNICALLY_RELEVANT",
                "commercial_status": "RESEARCH_REQUIRED",
                "priority": "RESEARCH",
                "confidence": "C",
                "process_name": "injection_moulding",
                "deployment_field": "battery_storage_deployed",
                "deployment_value": "UNKNOWN",
            },
            {
                "company_id": "P07",
                "legal_entity": "VARIOPLAST Konrad Däbritz GmbH",
                "rule_id": "R004",
                "opportunity_type": "heat_recovery",
                "opportunity_level": "HIGH",
                "technical_status": "TECHNICALLY_RELEVANT",
                "commercial_status": "ALREADY_DEPLOYED",
                "priority": "LOW",
                "confidence": "B",
                "process_name": "injection_moulding",
                "deployment_field": "heat_recovery_deployed",
                "deployment_value": "YES",
            },
        ]

    def test_only_unresolved_commercial_cases_enter_queue(self):
        queue = generate_research_queue(self.companies, self.rows)
        self.assertEqual(len(queue), 3)
        self.assertNotIn("heat_recovery", {task["opportunity_type"] for task in queue})

    def test_company_intelligence_supplies_canonical_legal_entity_and_urls(self):
        queue = generate_research_queue(self.companies, self.rows)
        energy_task = next(task for task in queue if task["opportunity_type"] == "energy_management")
        self.assertEqual(energy_task["legal_entity"], "Oskar Lehmann GmbH & Co. KG")
        self.assertEqual(energy_task["evidence_urls"], "https://example.com/downloads")

    def test_high_relevance_unknown_deployment_is_high_priority(self):
        queue = generate_research_queue(self.companies, self.rows)
        task = next(task for task in queue if task["opportunity_type"] == "energy_management")
        self.assertEqual(task["queue_rule_id"], "RQ03_HIGH_RELEVANCE_DEPLOYMENT_CHECK")
        self.assertEqual(task["research_priority"], "HIGH")
        self.assertEqual(task["decision_impact"], "HIGH")

    def test_public_announcement_creates_time_sensitive_verification_task(self):
        queue = generate_research_queue(self.companies, self.rows)
        task = next(task for task in queue if task["opportunity_type"] == "battery_storage")
        self.assertEqual(task["queue_rule_id"], "RQ01_ANNOUNCED_DEPLOYMENT_CHECK")
        self.assertEqual(task["research_priority"], "HIGH")
        self.assertIn("commissioned", task["research_question"])

    def test_medium_relevance_is_medium_priority_but_high_decision_impact(self):
        queue = generate_research_queue(self.companies, self.rows)
        task = next(task for task in queue if task["opportunity_type"] == "flexibility")
        self.assertEqual(task["queue_rule_id"], "RQ04_RELEVANT_DEPLOYMENT_CHECK")
        self.assertEqual(task["research_priority"], "MEDIUM")
        self.assertEqual(task["decision_impact"], "HIGH")

    def test_unknown_is_preserved_and_never_becomes_white_space(self):
        queue = generate_research_queue(self.companies, self.rows)
        for task in queue:
            self.assertEqual(task["current_value"], "UNKNOWN")
            self.assertEqual(task["commercial_status"], "RESEARCH_REQUIRED")
            self.assertNotIn("WHITE_SPACE", task.values())

    def test_missing_company_record_is_not_silently_invented(self):
        orphan = dict(self.rows[0], company_id="P99")
        self.assertEqual(generate_research_queue(self.companies, [orphan]), [])

    def test_duplicate_company_ids_fail_loudly(self):
        with self.assertRaisesRegex(ValueError, "Duplicate company_id"):
            generate_research_queue(self.companies + [dict(self.companies[0])], self.rows)

    def test_ranking_is_deterministic(self):
        first = generate_research_queue(self.companies, self.rows)
        second = generate_research_queue(list(reversed(self.companies)), list(reversed(self.rows)))
        self.assertEqual(first, second)
        self.assertEqual([task["research_rank"] for task in first], ["1", "2", "3"])


if __name__ == "__main__":
    unittest.main()
