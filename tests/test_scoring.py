import sys
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from score_companies import opportunity_band, score_row


class ScoringTests(unittest.TestCase):
    def base_row(self):
        return {
            "temperature_fit_score": "10",
            "process_electrification_score": "10",
            "fossil_heat_displacement_score": "5",
            "motor_drive_score": "8",
            "power_conversion_score": "8",
            "automation_control_score": "4",
            "scheduling_flex_score": "8",
            "thermal_storage_flex_score": "7",
            "incremental_load_score": "8",
            "power_quality_score": "4",
            "onsite_integration_score": "3",
            "measures_gap_score": "10",
            "management_gap_score": "5",
            "targets_gap_score": "5",
            "investment_gap_score": "5",
            "company_website_checked": "1",
            "report_checked": "1",
            "official_register_checked": "1",
            "certification_source_checked": "1",
            "independent_source_checked": "1",
            "latest_evidence_date": "2026-01-01",
        }

    def test_maximum_score_and_a_confidence(self):
        result = score_row(self.base_row(), date(2026, 9, 12))
        self.assertEqual(result["opportunity_score"], "100")
        self.assertEqual(result["process_electrification_potential"], "25")
        self.assertEqual(result["power_electronics_relevance"], "20")
        self.assertEqual(result["load_flexibility_potential"], "15")
        self.assertEqual(result["grid_power_quality_relevance"], "15")
        self.assertEqual(result["observed_transition_gap"], "25")
        self.assertEqual(result["confidence_grade"], "A")
        self.assertEqual(result["opportunity_band"], "HIGH")

    def test_low_coverage_blocks_classification(self):
        row = self.base_row()
        row["report_checked"] = "0"
        row["official_register_checked"] = "0"
        row["certification_source_checked"] = "0"
        result = score_row(row, date(2026, 9, 12))
        self.assertEqual(result["confidence_grade"], "C")
        self.assertEqual(result["classification_status"], "RESEARCH_REQUIRED")

    def test_band_boundaries(self):
        self.assertEqual(opportunity_band(39), "LOW")
        self.assertEqual(opportunity_band(40), "MEDIUM")
        self.assertEqual(opportunity_band(69), "MEDIUM")
        self.assertEqual(opportunity_band(70), "HIGH")

    def test_invalid_component_rejected(self):
        row = self.base_row()
        row["power_quality_score"] = "5"
        with self.assertRaises(ValueError):
            score_row(row, date(2026, 9, 12))

    def test_future_evidence_date_rejected(self):
        row = self.base_row()
        row["latest_evidence_date"] = "2027-01-01"
        with self.assertRaises(ValueError):
            score_row(row, date(2026, 9, 12))


if __name__ == "__main__":
    unittest.main()
