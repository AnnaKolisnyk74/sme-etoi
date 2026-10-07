import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from score_companies import SCORE_FIELDS
from score_readiness import generate_score_readiness, read_csv as read_readiness_csv
from score_work_queue import generate_score_work_queue


class ScoreWorkQueueTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.companies = read_readiness_csv(ROOT / "data" / "company_intelligence.csv")
        cls.process_map = read_readiness_csv(ROOT / "data" / "company_process_map.csv")
        cls.readiness = generate_score_readiness(
            cls.companies,
            cls.process_map,
            read_readiness_csv(ROOT / "evidence" / "certificate_register.csv"),
            read_readiness_csv(ROOT / "evidence" / "qa_review.csv"),
            read_readiness_csv(ROOT / "data" / "pilot_coded.csv"),
            read_readiness_csv(ROOT / "outputs" / "pilot_scored.csv"),
        )
        cls.rows = generate_score_work_queue(
            cls.companies,
            cls.readiness,
            cls.process_map,
            read_readiness_csv(ROOT / "evidence" / "source_register.csv"),
            read_readiness_csv(ROOT / "evidence" / "qa_review.csv"),
            read_readiness_csv(ROOT / "data" / "pilot_coded.csv"),
            read_readiness_csv(ROOT / "outputs" / "research_queue.csv"),
            read_readiness_csv(ROOT / "data" / "score_coding_proposals.csv"),
        )

    def test_current_sample_produces_expected_workload(self):
        self.assertEqual(len(self.rows), 452)
        self.assertEqual(
            sum(row["workstream"] == "ELIGIBILITY" for row in self.rows),
            12,
        )
        self.assertEqual(
            sum(row["workstream"] == "NUMERIC_CODING" for row in self.rows),
            440,
        )

    def test_eligibility_gates_are_first_and_follow_research_rank(self):
        gates = [row for row in self.rows if row["workstream"] == "ELIGIBILITY"]
        self.assertEqual([int(row["work_rank"]) for row in gates], list(range(1, 13)))
        research_ranks = [int(row["research_rank"]) for row in gates]
        self.assertEqual(research_ranks, sorted(research_ranks))

    def test_blocked_companies_never_receive_numeric_coding_tasks(self):
        blocked = {
            row["company_id"]
            for row in self.readiness
            if row["score_status"] == "NOT_SCOREABLE_ELIGIBILITY"
        }
        coding_companies = {
            row["company_id"]
            for row in self.rows
            if row["workstream"] == "NUMERIC_CODING"
        }
        self.assertTrue(blocked.isdisjoint(coding_companies))

    def test_each_ready_company_receives_five_dimension_packages(self):
        expected = {
            row["company_id"]
            for row in self.readiness
            if row["score_status"] == "NEEDS_NUMERIC_CODING"
        }
        by_company = {}
        for row in self.rows:
            if row["workstream"] != "NUMERIC_CODING":
                continue
            by_company.setdefault(row["company_id"], []).append(row)
        self.assertEqual(set(by_company), expected)
        self.assertEqual(len(expected), 88)
        for company_id, rows in by_company.items():
            self.assertEqual(len(rows), 5, company_id)

    def test_dimension_packages_cover_all_numeric_fields_once(self):
        by_company = {}
        for row in self.rows:
            if row["workstream"] != "NUMERIC_CODING":
                continue
            by_company.setdefault(row["company_id"], []).append(row)

        expected_fields = set(SCORE_FIELDS)
        for company_id, rows in by_company.items():
            fields = []
            for row in rows:
                fields.extend(
                    field.strip()
                    for field in row["missing_fields"].split("|")
                    if field.strip()
                )
            self.assertEqual(set(fields), expected_fields, company_id)
            self.assertEqual(len(fields), len(expected_fields), company_id)

    def test_proposal_state_advances_work_without_mutating_canonical_fields(self):
        numeric = [
            row for row in self.rows
            if row["workstream"] == "NUMERIC_CODING"
        ]
        p04 = [row for row in numeric if row["company_id"] == "P04"]
        p19 = [row for row in numeric if row["company_id"] == "P19"]
        p12 = [row for row in numeric if row["company_id"] == "P12"]
        p16 = [row for row in numeric if row["company_id"] == "P16"]
        p05 = [row for row in numeric if row["company_id"] == "P05"]
        p18 = [row for row in numeric if row["company_id"] == "P18"]
        p22 = [row for row in numeric if row["company_id"] == "P22"]
        p24 = [row for row in numeric if row["company_id"] == "P24"]
        p23 = [row for row in numeric if row["company_id"] == "P23"]
        p11 = [row for row in numeric if row["company_id"] == "P11"]
        p53 = [row for row in numeric if row["company_id"] == "P53"]
        p20 = [row for row in numeric if row["company_id"] == "P20"]
        remaining = [
            row for row in numeric
            if row["company_id"] not in {"P04", "P19", "P12", "P16", "P05", "P18", "P22", "P24", "P23", "P11", "P53", "P20", "P21", "P27", "P30", "P31", "P43", "P13", "P25", "P15", "P26", "P28", "P29", "P33", "P35", "P36", "P38", "P39", "P41", "P44", "P45", "P50", "P51", "P52", "P54", "P55", "P56", "P57", "P58", "P59", "P61", "P63", "P64", "P66", "P68", "P70", "P75", "P76"}
        ]

        self.assertEqual(len(p04), 5)
        self.assertEqual(
            {row["task_status"] for row in p04},
            {"AWAITING_HUMAN_REVIEW"},
        )
        self.assertTrue(
            all(row["proposal_covered_fields"] for row in p04)
        )
        self.assertTrue(
            all(not row["research_gap_fields"] for row in p04)
        )

        self.assertEqual(len(p19), 5)
        self.assertEqual(
            {row["task_status"] for row in p19},
            {"RESEARCH_NEEDED"},
        )
        self.assertTrue(
            all(row["research_gap_fields"] for row in p19)
        )

        self.assertEqual(len(p12), 5)
        self.assertEqual(
            sum(row["task_status"] == "AWAITING_HUMAN_REVIEW" for row in p12),
            4,
        )
        self.assertEqual(
            sum(row["task_status"] == "RESEARCH_NEEDED" for row in p12),
            1,
        )
        p12_flex = next(
            row for row in p12
            if row["dimension"] == "load_flexibility_potential"
        )
        self.assertEqual(p12_flex["task_status"], "RESEARCH_NEEDED")
        self.assertIn("thermal_storage_flex_score", p12_flex["research_gap_fields"])

        self.assertEqual(len(p16), 5)
        self.assertEqual(
            {row["task_status"] for row in p16},
            {"RESEARCH_NEEDED"},
        )
        self.assertTrue(
            all(row["research_gap_fields"] for row in p16)
        )

        self.assertEqual(len(p05), 5)
        self.assertEqual(
            {row["task_status"] for row in p05},
            {"AWAITING_HUMAN_REVIEW"},
        )
        self.assertTrue(all(row["proposal_covered_fields"] for row in p05))

        self.assertEqual(len(p18), 5)
        self.assertEqual(
            {row["task_status"] for row in p18},
            {"RESEARCH_NEEDED"},
        )
        self.assertTrue(all(row["research_gap_fields"] for row in p18))

        self.assertEqual(len(p22), 5)
        self.assertEqual(
            {row["task_status"] for row in p22},
            {"AWAITING_HUMAN_REVIEW"},
        )
        self.assertTrue(all(row["proposal_covered_fields"] for row in p22))
        self.assertTrue(all(not row["research_gap_fields"] for row in p22))

        self.assertEqual(len(p24), 5)
        self.assertEqual(
            {row["task_status"] for row in p24},
            {"RESEARCH_NEEDED"},
        )
        self.assertTrue(all(row["research_gap_fields"] for row in p24))

        self.assertEqual(len(p23), 5)
        self.assertEqual(
            {row["task_status"] for row in p23},
            {"RESEARCH_NEEDED"},
        )
        self.assertTrue(all(row["research_gap_fields"] for row in p23))

        self.assertEqual(len(p11), 5)
        self.assertEqual(
            sum(row["task_status"] == "RESEARCH_NEEDED" for row in p11),
            4,
        )
        self.assertEqual(
            sum(row["task_status"] == "AWAITING_HUMAN_REVIEW" for row in p11),
            1,
        )
        p11_gap = next(
            row for row in p11
            if row["dimension"] == "grid_power_quality_relevance"
        )
        self.assertIn("power_quality_score", p11_gap["research_gap_fields"])
        p11_transition = next(
            row for row in p11
            if row["dimension"] == "observed_transition_gap"
        )
        self.assertEqual(
            p11_transition["task_status"],
            "AWAITING_HUMAN_REVIEW",
        )

        self.assertEqual(len(p53), 5)
        self.assertEqual(
            sum(row["task_status"] == "RESEARCH_NEEDED" for row in p53),
            4,
        )
        self.assertEqual(
            sum(row["task_status"] == "AWAITING_HUMAN_REVIEW" for row in p53),
            1,
        )
        p53_flex = next(
            row for row in p53
            if row["dimension"] == "load_flexibility_potential"
        )
        self.assertEqual(
            p53_flex["task_status"],
            "AWAITING_HUMAN_REVIEW",
        )

        self.assertEqual(len(p20), 5)
        self.assertEqual(
            {row["task_status"] for row in p20},
            {"RESEARCH_NEEDED"},
        )
        self.assertTrue(all(row["research_gap_fields"] for row in p20))

        self.assertEqual(len(remaining), 200)
        self.assertEqual(
            {row["task_status"] for row in remaining},
            {"READY_TO_CODE"},
        )

    def test_queue_never_assigns_numeric_values(self):
        forbidden_columns = set(SCORE_FIELDS)
        for row in self.rows:
            self.assertTrue(forbidden_columns.isdisjoint(row))
            self.assertNotIn("opportunity_score", row)

    def test_work_ranks_are_dense_and_unique(self):
        ranks = [int(row["work_rank"]) for row in self.rows]
        self.assertEqual(ranks, list(range(1, len(self.rows) + 1)))


if __name__ == "__main__":
    unittest.main()
