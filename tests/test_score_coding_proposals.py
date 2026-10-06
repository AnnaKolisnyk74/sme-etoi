import csv
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from score_companies import SCORE_FIELDS
from validate_score_coding_proposals import validate


def read_csv(path: Path):
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


class ScoreCodingProposalTests(unittest.TestCase):
    def test_current_proposals_pass_validation(self):
        self.assertEqual(validate(ROOT), [])

    def test_p04_covers_all_15_score_fields_once(self):
        rows = [
            row
            for row in read_csv(ROOT / "data" / "score_coding_proposals.csv")
            if row["company_id"] == "P04"
        ]
        self.assertEqual(len(rows), 15)
        self.assertEqual(
            {row["score_field"] for row in rows},
            set(SCORE_FIELDS),
        )

    def test_p04_provisional_sum_is_53_if_all_proposals_were_accepted(self):
        rows = [
            row
            for row in read_csv(ROOT / "data" / "score_coding_proposals.csv")
            if row["company_id"] == "P04"
        ]
        self.assertEqual(sum(int(row["proposed_value"]) for row in rows), 53)

    def test_unresolved_proposals_do_not_claim_human_approval(self):
        rows = read_csv(ROOT / "data" / "score_coding_proposals.csv")
        for row in rows:
            if row["proposal_status"] in {"AWAITING_HUMAN_REVIEW", "NEEDS_RESEARCH"}:
                self.assertEqual(row["reviewer"], "")
                self.assertEqual(row["review_date"], "")

    def test_p19_preserves_field_level_uncertainty(self):
        rows = [
            row
            for row in read_csv(ROOT / "data" / "score_coding_proposals.csv")
            if row["company_id"] == "P19"
        ]
        self.assertEqual(len(rows), 15)
        self.assertEqual(
            {row["score_field"] for row in rows},
            set(SCORE_FIELDS),
        )
        numeric = [
            row for row in rows
            if row["proposal_status"] == "AWAITING_HUMAN_REVIEW"
        ]
        research = [
            row for row in rows
            if row["proposal_status"] == "NEEDS_RESEARCH"
        ]
        self.assertEqual(len(numeric), 3)
        self.assertEqual(len(research), 12)
        self.assertTrue(all(row["proposed_value"] for row in numeric))
        self.assertTrue(all(row["proposal_confidence"] != "UNKNOWN" for row in numeric))
        self.assertTrue(all(row["proposed_value"] == "" for row in research))
        self.assertTrue(all(row["proposal_confidence"] == "UNKNOWN" for row in research))
        self.assertTrue(all(row["missing_fact"] for row in research))

    def test_p19_gap_rows_enforce_blank_values_and_missing_fact(self):
        rows = [
            row
            for row in read_csv(ROOT / "data" / "score_coding_proposals.csv")
            if row["company_id"] == "P19"
        ]
        numeric = [
            row for row in rows
            if row["proposal_status"] == "AWAITING_HUMAN_REVIEW"
        ]
        gaps = [
            row for row in rows
            if row["proposal_status"] == "NEEDS_RESEARCH"
        ]
        self.assertEqual(len(numeric), 3)
        self.assertEqual(len(gaps), 12)
        for row in gaps:
            self.assertEqual(row["proposed_value"], "")
            self.assertEqual(row["proposal_confidence"], "UNKNOWN")
            self.assertTrue(row["missing_fact"])
        for row in numeric:
            self.assertTrue(row["proposed_value"])
            self.assertNotEqual(row["proposal_confidence"], "UNKNOWN")

    def test_p19_only_numeric_proposals_sum_to_observed_gap_partial_total(self):
        rows = [
            row
            for row in read_csv(ROOT / "data" / "score_coding_proposals.csv")
            if row["company_id"] == "P19"
            and row["proposal_status"] == "AWAITING_HUMAN_REVIEW"
        ]
        self.assertEqual(sum(int(row["proposed_value"]) for row in rows), 12)
        self.assertEqual(
            {row["score_field"] for row in rows},
            {"measures_gap_score", "management_gap_score", "targets_gap_score"},
        )

    def test_p12_is_14_numeric_proposals_plus_one_research_gap(self):
        rows = [
            row
            for row in read_csv(ROOT / "data" / "score_coding_proposals.csv")
            if row["company_id"] == "P12"
        ]
        self.assertEqual(len(rows), 15)
        self.assertEqual({row["score_field"] for row in rows}, set(SCORE_FIELDS))
        numeric = [
            row for row in rows
            if row["proposal_status"] == "AWAITING_HUMAN_REVIEW"
        ]
        gaps = [
            row for row in rows
            if row["proposal_status"] == "NEEDS_RESEARCH"
        ]
        self.assertEqual(len(numeric), 14)
        self.assertEqual(len(gaps), 1)
        self.assertEqual(
            gaps[0]["score_field"],
            "thermal_storage_flex_score",
        )
        self.assertEqual(gaps[0]["proposed_value"], "")
        self.assertEqual(gaps[0]["proposal_confidence"], "UNKNOWN")
        self.assertTrue(gaps[0]["missing_fact"])
        self.assertEqual(
            sum(int(row["proposed_value"]) for row in numeric),
            50,
        )

    def test_p16_is_four_numeric_proposals_plus_eleven_research_gaps(self):
        rows = [
            row
            for row in read_csv(ROOT / "data" / "score_coding_proposals.csv")
            if row["company_id"] == "P16"
        ]
        self.assertEqual(len(rows), 15)
        self.assertEqual({row["score_field"] for row in rows}, set(SCORE_FIELDS))
        numeric = [
            row for row in rows
            if row["proposal_status"] == "AWAITING_HUMAN_REVIEW"
        ]
        gaps = [
            row for row in rows
            if row["proposal_status"] == "NEEDS_RESEARCH"
        ]
        self.assertEqual(len(numeric), 4)
        self.assertEqual(len(gaps), 11)
        self.assertEqual(
            {row["score_field"] for row in numeric},
            {
                "temperature_fit_score",
                "scheduling_flex_score",
                "management_gap_score",
                "targets_gap_score",
            },
        )
        self.assertEqual(
            sum(int(row["proposed_value"]) for row in numeric),
            13,
        )
        for row in gaps:
            self.assertEqual(row["proposed_value"], "")
            self.assertEqual(row["proposal_confidence"], "UNKNOWN")
            self.assertTrue(row["missing_fact"])

    def test_p05_complete_proposals_cover_all_fields_and_sum_to_59(self):
        rows = [
            row
            for row in read_csv(ROOT / "data" / "score_coding_proposals.csv")
            if row["company_id"] == "P05"
        ]
        self.assertEqual(len(rows), 15)
        self.assertEqual({row["score_field"] for row in rows}, set(SCORE_FIELDS))
        self.assertEqual(
            {row["proposal_status"] for row in rows},
            {"AWAITING_HUMAN_REVIEW"},
        )
        self.assertEqual(sum(int(row["proposed_value"]) for row in rows), 59)
        self.assertTrue(all(row["proposal_confidence"] != "UNKNOWN" for row in rows))

    def test_p18_is_seven_numeric_proposals_plus_eight_research_gaps(self):
        rows = [
            row
            for row in read_csv(ROOT / "data" / "score_coding_proposals.csv")
            if row["company_id"] == "P18"
        ]
        self.assertEqual(len(rows), 15)
        self.assertEqual({row["score_field"] for row in rows}, set(SCORE_FIELDS))
        numeric = [
            row for row in rows
            if row["proposal_status"] == "AWAITING_HUMAN_REVIEW"
        ]
        gaps = [
            row for row in rows
            if row["proposal_status"] == "NEEDS_RESEARCH"
        ]
        self.assertEqual(len(numeric), 7)
        self.assertEqual(len(gaps), 8)
        self.assertEqual(
            sum(int(row["proposed_value"]) for row in numeric),
            22,
        )
        for row in gaps:
            self.assertEqual(row["proposed_value"], "")
            self.assertEqual(row["proposal_confidence"], "UNKNOWN")
            self.assertTrue(row["missing_fact"])

    def test_p22_complete_proposals_cover_all_fields_and_sum_to_74(self):
        rows = [
            row
            for row in read_csv(ROOT / "data" / "score_coding_proposals.csv")
            if row["company_id"] == "P22"
        ]
        self.assertEqual(len(rows), 15)
        self.assertEqual({row["score_field"] for row in rows}, set(SCORE_FIELDS))
        self.assertEqual(
            {row["proposal_status"] for row in rows},
            {"AWAITING_HUMAN_REVIEW"},
        )
        self.assertEqual(sum(int(row["proposed_value"]) for row in rows), 74)

    def test_p24_is_two_numeric_proposals_plus_thirteen_research_gaps(self):
        rows = [
            row
            for row in read_csv(ROOT / "data" / "score_coding_proposals.csv")
            if row["company_id"] == "P24"
        ]
        self.assertEqual(len(rows), 15)
        self.assertEqual({row["score_field"] for row in rows}, set(SCORE_FIELDS))
        numeric = [
            row for row in rows
            if row["proposal_status"] == "AWAITING_HUMAN_REVIEW"
        ]
        gaps = [
            row for row in rows
            if row["proposal_status"] == "NEEDS_RESEARCH"
        ]
        self.assertEqual(len(numeric), 2)
        self.assertEqual(len(gaps), 13)
        self.assertEqual(
            {row["score_field"] for row in numeric},
            {"management_gap_score", "targets_gap_score"},
        )
        self.assertEqual(sum(int(row["proposed_value"]) for row in numeric), 5)
        for row in gaps:
            self.assertEqual(row["proposed_value"], "")
            self.assertEqual(row["proposal_confidence"], "UNKNOWN")
            self.assertTrue(row["missing_fact"])

    def test_p04_proposals_do_not_mutate_canonical_scoring_inputs_or_outputs(self):
        coded_ids = {
            row["company_id"]
            for row in read_csv(ROOT / "data" / "pilot_coded.csv")
        }
        scored_ids = {
            row["company_id"]
            for row in read_csv(ROOT / "outputs" / "pilot_scored.csv")
        }
        self.assertNotIn("P04", coded_ids)
        self.assertNotIn("P04", scored_ids)
        self.assertNotIn("P19", coded_ids)
        self.assertNotIn("P19", scored_ids)
        self.assertNotIn("P12", coded_ids)
        self.assertNotIn("P12", scored_ids)
        self.assertNotIn("P16", coded_ids)
        self.assertNotIn("P16", scored_ids)
        self.assertNotIn("P05", coded_ids)
        self.assertNotIn("P05", scored_ids)
        self.assertNotIn("P18", coded_ids)
        self.assertNotIn("P18", scored_ids)
        self.assertNotIn("P22", coded_ids)
        self.assertNotIn("P22", scored_ids)
        self.assertNotIn("P24", coded_ids)
        self.assertNotIn("P24", scored_ids)


if __name__ == "__main__":
    unittest.main()
