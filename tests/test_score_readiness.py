import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from score_readiness import (
    evaluate_company,
    generate_score_readiness,
    read_csv,
)


class ScoreReadinessUnitTests(unittest.TestCase):
    def base_company(self):
        return {
            "company_id": "PX",
            "legal_entity": "Example GmbH",
            "sme_status": "probable",
            "group_check": "independent",
        }

    def complete_certificates(self):
        return {
            "ISO 50001": "NOT_FOUND_AFTER_CHECK",
            "ISO 14001": "NOT_FOUND_AFTER_CHECK",
            "EMAS": "NOT_FOUND_AFTER_CHECK",
        }

    def complete_coded_row(self):
        return {
            "temperature_fit_score": "7",
            "process_electrification_score": "7",
            "fossil_heat_displacement_score": "2",
            "motor_drive_score": "5",
            "power_conversion_score": "5",
            "automation_control_score": "3",
            "scheduling_flex_score": "5",
            "thermal_storage_flex_score": "5",
            "incremental_load_score": "5",
            "power_quality_score": "3",
            "onsite_integration_score": "2",
            "measures_gap_score": "3",
            "management_gap_score": "3",
            "targets_gap_score": "3",
            "investment_gap_score": "3",
        }

    def test_unresolved_group_blocks_score_even_if_numeric_score_exists(self):
        company = self.base_company()
        company["group_check"] = "partner_or_linked_sme"
        row = evaluate_company(
            company,
            process_rows=[{"process_id": "PR001"}],
            certificate_rows=self.complete_certificates(),
            qa_row={"independent_human_review_status": "APPROVED"},
            coded_row=self.complete_coded_row(),
            scored_row={
                "opportunity_score": "70",
                "opportunity_band": "HIGH",
                "confidence_grade": "B",
            },
        )
        self.assertEqual(row["score_status"], "NOT_SCOREABLE_ELIGIBILITY")
        self.assertEqual(row["existing_score"], "70")
        self.assertEqual(
            row["existing_score_status"],
            "LEGACY_PROVISIONAL_NOT_FINAL",
        )

    def test_pending_certificate_check_blocks_numeric_scoring(self):
        certificates = self.complete_certificates()
        certificates["EMAS"] = "PENDING_CHECK"
        row = evaluate_company(
            self.base_company(),
            process_rows=[{"process_id": "PR001"}],
            certificate_rows=certificates,
            qa_row={"independent_human_review_status": "APPROVED"},
            coded_row=self.complete_coded_row(),
            scored_row=None,
        )
        self.assertEqual(row["score_status"], "NOT_SCOREABLE_CERTIFICATES")
        self.assertEqual(row["certificate_check_status"], "PENDING")

    def test_numeric_coding_is_required_after_method_gates(self):
        row = evaluate_company(
            self.base_company(),
            process_rows=[{"process_id": "PR001"}],
            certificate_rows=self.complete_certificates(),
            qa_row={"independent_human_review_status": "APPROVED"},
            coded_row=None,
            scored_row=None,
        )
        self.assertEqual(row["score_status"], "NEEDS_NUMERIC_CODING")
        self.assertEqual(row["numeric_coding_status"], "MISSING")

    def test_human_review_is_required_for_final_score(self):
        row = evaluate_company(
            self.base_company(),
            process_rows=[{"process_id": "PR001"}],
            certificate_rows=self.complete_certificates(),
            qa_row={"independent_human_review_status": "PENDING"},
            coded_row=self.complete_coded_row(),
            scored_row={
                "opportunity_score": "55",
                "opportunity_band": "MEDIUM",
                "confidence_grade": "A",
            },
        )
        self.assertEqual(row["score_status"], "PROVISIONAL_SCORE_ONLY")
        self.assertIn("independent human review=PENDING", row["blocking_reasons"])

    def test_final_score_ready_requires_all_gates(self):
        row = evaluate_company(
            self.base_company(),
            process_rows=[{"process_id": "PR001"}],
            certificate_rows=self.complete_certificates(),
            qa_row={"independent_human_review_status": "APPROVED"},
            coded_row=self.complete_coded_row(),
            scored_row={
                "opportunity_score": "55",
                "opportunity_band": "MEDIUM",
                "confidence_grade": "A",
            },
        )
        self.assertEqual(row["score_status"], "FINAL_SCORE_READY")
        self.assertEqual(row["existing_score_status"], "FINAL_ELIGIBLE")


class ScoreReadinessIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = generate_score_readiness(
            read_csv(ROOT / "data" / "company_intelligence.csv"),
            read_csv(ROOT / "data" / "company_process_map.csv"),
            read_csv(ROOT / "evidence" / "certificate_register.csv"),
            read_csv(ROOT / "evidence" / "qa_review.csv"),
            read_csv(ROOT / "data" / "pilot_coded.csv"),
            read_csv(ROOT / "outputs" / "pilot_scored.csv"),
        )
        cls.by_id = {row["company_id"]: row for row in cls.rows}

    def test_readiness_covers_exactly_the_100_company_sample(self):
        self.assertEqual(len(self.rows), 100)
        self.assertEqual(len(self.by_id), 100)

    def test_p07_and_p10_scores_remain_visible_but_not_final(self):
        self.assertEqual(self.by_id["P07"]["existing_score"], "63")
        self.assertEqual(self.by_id["P10"]["existing_score"], "70")
        for company_id in ("P07", "P10"):
            self.assertEqual(
                self.by_id[company_id]["score_status"],
                "NOT_SCOREABLE_ELIGIBILITY",
            )
            self.assertEqual(
                self.by_id[company_id]["existing_score_status"],
                "LEGACY_PROVISIONAL_NOT_FINAL",
            )

    def test_every_unresolved_group_check_is_score_blocked(self):
        unresolved = {
            row["company_id"]
            for row in self.rows
            if row["eligibility_gate"] == "UNRESOLVED"
        }
        blocked = {
            row["company_id"]
            for row in self.rows
            if row["score_status"] == "NOT_SCOREABLE_ELIGIBILITY"
        }
        self.assertEqual(unresolved, blocked)
        self.assertEqual(len(unresolved), 12)

    def test_final_ready_rows_satisfy_all_explicit_gates(self):
        for row in self.rows:
            if row["score_status"] != "FINAL_SCORE_READY":
                continue
            self.assertEqual(row["eligibility_gate"], "PROVISIONAL_PASS")
            self.assertEqual(row["process_mapping_status"], "PRESENT")
            self.assertEqual(row["certificate_check_status"], "COMPLETE")
            self.assertEqual(row["numeric_coding_status"], "COMPLETE")
            self.assertIn(
                row["independent_human_review_status"],
                {"APPROVED", "COMPLETE", "COMPLETED", "REVIEWED", "DONE"},
            )


if __name__ == "__main__":
    unittest.main()
