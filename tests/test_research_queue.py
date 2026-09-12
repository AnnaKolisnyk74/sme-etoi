import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from research_queue import generate_research_queue, information_gain


class ResearchQueueTests(unittest.TestCase):
    def setUp(self):
        self.rows = [
            {
                "company_id": "P10",
                "legal_entity": "Oskar Lehmann GmbH & Co. KG",
                "opportunity_type": "energy_management",
                "technical_status": "TECHNICALLY_RELEVANT",
                "commercial_status": "RESEARCH_REQUIRED",
                "priority": "RESEARCH",
                "why_now": "three-shift operation and public transition target",
                "confidence": "B",
                "process_name": "injection_moulding",
                "deployment_field": "energy_management_deployed",
                "deployment_value": "UNKNOWN",
            },
            {
                "company_id": "P07",
                "legal_entity": "VARIOPLAST Konrad Däbritz GmbH",
                "opportunity_type": "heat_recovery",
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
        queue = generate_research_queue(self.rows)
        self.assertEqual(len(queue), 1)
        self.assertEqual(queue[0]["company_id"], "P10")

    def test_rank_and_missing_fact_are_created(self):
        queue = generate_research_queue(self.rows)
        self.assertEqual(queue[0]["research_rank"], "1")
        self.assertIn("energy_management_deployed", queue[0]["missing_fact"])
        self.assertEqual(queue[0]["research_priority"], "HIGH")

    def test_information_gain_rewards_resolvable_uncertainty(self):
        self.assertGreaterEqual(information_gain(self.rows[0]), 10)

    def test_deployed_case_scores_lower(self):
        self.assertLess(information_gain(self.rows[1]), information_gain(self.rows[0]))


if __name__ == "__main__":
    unittest.main()
