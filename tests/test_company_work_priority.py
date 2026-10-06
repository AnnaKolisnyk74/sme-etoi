import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from company_work_priority import generate_company_work_priority, read_csv


class CompanyWorkPriorityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = generate_company_work_priority(
            read_csv(ROOT / "outputs" / "score_work_queue.csv"),
            read_csv(ROOT / "evidence" / "source_register.csv"),
            read_csv(ROOT / "data" / "company_process_map.csv"),
        )
        cls.by_id = {row["company_id"]: row for row in cls.rows}

    def test_current_sample_has_one_priority_row_per_company(self):
        self.assertEqual(len(self.rows), 100)
        self.assertEqual(len(self.by_id), 100)

    def test_current_workflow_action_counts(self):
        counts = {}
        for row in self.rows:
            action = row["workflow_action"]
            counts[action] = counts.get(action, 0) + 1
        self.assertEqual(
            counts,
            {
                "CODE_NOW": 72,
                "RESEARCH_FIRST": 13,
                "REVIEW_PROPOSALS": 3,
                "ELIGIBILITY_FIRST": 12,
            },
        )

    def test_p43_is_next_best_company_to_code(self):
        next_rows = [
            row for row in self.rows if row["is_next_to_code"] == "YES"
        ]
        self.assertEqual(len(next_rows), 1)
        self.assertEqual(next_rows[0]["company_id"], "P43")
        self.assertEqual(next_rows[0]["legal_entity"], "WZR ceramic solutions GmbH")
        self.assertEqual(next_rows[0]["coding_rank"], "1")
        self.assertEqual(next_rows[0]["workflow_action"], "CODE_NOW")

    def test_code_now_ranks_are_dense(self):
        rows = [
            row for row in self.rows if row["workflow_action"] == "CODE_NOW"
        ]
        ranks = sorted(int(row["coding_rank"]) for row in rows)
        self.assertEqual(ranks, list(range(1, 73)))

    def test_research_first_companies_are_exactly_known_gap_cases(self):
        self.assertEqual(
            {
                row["company_id"]
                for row in self.rows
                if row["workflow_action"] == "RESEARCH_FIRST"
            },
            {"P11", "P12", "P16", "P18", "P19", "P20", "P23", "P24", "P53", "P21", "P27", "P30", "P31"},
        )

    def test_p11_moves_from_code_now_to_research_first(self):
        row = self.by_id["P11"]
        self.assertEqual(row["workflow_action"], "RESEARCH_FIRST")
        self.assertEqual(row["is_next_to_code"], "NO")
        self.assertEqual(row["coding_rank"], "")
        self.assertEqual(row["research_needed_tasks"], "4")
        self.assertEqual(row["awaiting_human_review_tasks"], "1")

    def test_p53_moves_from_code_now_to_research_first(self):
        row = self.by_id["P53"]
        self.assertEqual(row["workflow_action"], "RESEARCH_FIRST")
        self.assertEqual(row["is_next_to_code"], "NO")
        self.assertEqual(row["coding_rank"], "")
        self.assertEqual(row["research_needed_tasks"], "4")
        self.assertEqual(row["awaiting_human_review_tasks"], "1")

    def test_p20_moves_from_code_now_to_research_first(self):
        row = self.by_id["P20"]
        self.assertEqual(row["workflow_action"], "RESEARCH_FIRST")
        self.assertEqual(row["is_next_to_code"], "NO")
        self.assertEqual(row["coding_rank"], "")
        self.assertEqual(row["research_needed_tasks"], "5")

    def test_review_proposal_companies_are_fully_covered_cases(self):
        self.assertEqual(
            {
                row["company_id"]
                for row in self.rows
                if row["workflow_action"] == "REVIEW_PROPOSALS"
            },
            {"P04", "P05", "P22"},
        )

    def test_eligibility_gate_never_becomes_code_now(self):
        for row in self.rows:
            if row["workflow_action"] == "ELIGIBILITY_FIRST":
                self.assertEqual(row["coding_rank"], "")
                self.assertEqual(row["is_next_to_code"], "NO")
                self.assertGreater(int(row["open_gate_tasks"]), 0)


if __name__ == "__main__":
    unittest.main()
