import sys
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from score_companies import opportunity_band, score_row


class ScoringTests(unittest.TestCase):
    def base_row(self):
        return {
            "sector_energy_profile_score": "15",
            "process_evidence_score": "15",
            "site_scale_score": "10",
            "low_temp_fit_score": "10",
            "electrification_fit_score": "10",
            "flexibility_fit_score": "10",
            "measures_gap_score": "12",
            "management_gap_score": "6",
            "targets_gap_score": "6",
            "investment_gap_score": "6",
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
        row["management_gap_score"] = "7"
        with self.assertRaises(ValueError):
            score_row(row, date(2026, 9, 12))


if __name__ == "__main__":
    unittest.main()
