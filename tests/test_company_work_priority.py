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
                                "RESEARCH_FIRST": 88,
                "ELIGIBILITY_FIRST": 12,
            },
        )

    def test_no_next_company_after_all_first_passes(self):
        self.assertFalse(any(row['is_next_to_code'] == 'YES' for row in self.rows))
        self.assertEqual(self.by_id['P71']['workflow_action'], 'RESEARCH_FIRST')

    def test_code_now_ranks_are_dense(self):
        rows = [
            row for row in self.rows if row["workflow_action"] == "CODE_NOW"
        ]
        ranks = sorted(int(row["coding_rank"]) for row in rows)
        self.assertEqual(ranks, [])

    def test_research_first_companies_are_exactly_known_gap_cases(self):
        self.assertEqual(
            {
                row["company_id"]
                for row in self.rows
                if row["workflow_action"] == "RESEARCH_FIRST"
            },
            {"P04", "P05", "P22", "P11", "P12", "P16", "P18", "P19", "P20", "P23", "P24", "P53", "P21", "P27", "P30", "P31", "P43", "P13", "P25", "P15", "P26", "P28", "P29", "P33", "P35", "P36", "P38", "P39", "P41", "P44", "P45", "P50", "P51", "P52", "P54", "P55", "P56", "P57", "P58", "P59", "P61", "P63", "P64", "P66", "P68", "P70", "P75", "P76", "P77", "P79", "P80", "P81", "P83", "P84", "P87", "P90", "P91", "P92", "P93", "P94", "P95", "P97", "P98", "P100", "P101", "P105", "P106", "P108", "P109", "P110", "P37", "P60", "P71", "P72", "P73", "P74", "P78", "P82", "P85", "P86", "P89", "P96", "P99", "P102", "P103", "P107", "P62", "P03"},
        )

    def test_p11_moves_from_code_now_to_research_first(self):
        row = self.by_id["P11"]
        self.assertEqual(row["workflow_action"], "RESEARCH_FIRST")
        self.assertEqual(row["is_next_to_code"], "NO")
        self.assertEqual(row["coding_rank"], "")
        self.assertEqual(row["research_needed_tasks"], "4")
        self.assertEqual(row["checked_tasks"], "1")

    def test_p53_moves_from_code_now_to_research_first(self):
        row = self.by_id["P53"]
        self.assertEqual(row["workflow_action"], "RESEARCH_FIRST")
        self.assertEqual(row["is_next_to_code"], "NO")
        self.assertEqual(row["coding_rank"], "")
        self.assertEqual(row["research_needed_tasks"], "4")
        self.assertEqual(row["checked_tasks"], "1")

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
            set(),
        )

    def test_eligibility_gate_never_becomes_code_now(self):
        for row in self.rows:
            if row["workflow_action"] == "ELIGIBILITY_FIRST":
                self.assertEqual(row["coding_rank"], "")
                self.assertEqual(row["is_next_to_code"], "NO")
                self.assertGreater(int(row["open_gate_tasks"]), 0)


if __name__ == "__main__":
    unittest.main()
