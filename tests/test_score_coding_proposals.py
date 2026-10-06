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


if __name__ == "__main__":
    unittest.main()
