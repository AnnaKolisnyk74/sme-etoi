import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from run_pipeline import (
    build_outputs,
    pipeline_summary,
    run_pipeline,
    validate_generated_outputs,
)


class PipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.companies, cls.opportunities, cls.queue = build_outputs(ROOT)

    def test_current_pilot_passes_cross_output_validation(self):
        self.assertEqual(
            validate_generated_outputs(
                self.companies,
                self.opportunities,
                self.queue,
            ),
            [],
        )

    def test_check_only_pipeline_runs_without_writing(self):
        summary = run_pipeline(
            ROOT,
            write_outputs=False,
            include_reliability=False,
        )
        self.assertEqual(summary["companies"], 100)
        self.assertEqual(summary["eligibility_gates"], 12)
        self.assertGreater(summary["opportunities"], 0)
        self.assertGreater(summary["research_tasks"], 0)
        self.assertEqual(summary["score_readiness_rows"], 100)
        self.assertEqual(summary["final_score_ready"], 0)
        self.assertEqual(summary["score_work_tasks"], 452)
        self.assertEqual(summary["numeric_coding_tasks"], 440)
        self.assertEqual(summary["ready_to_code_tasks"], 430)
        self.assertEqual(summary["research_needed_tasks"], 5)
        self.assertEqual(summary["awaiting_human_review_tasks"], 5)
        self.assertIsNone(summary["double_code_conflicts"])

    def test_summary_matches_generated_eligibility_blocks(self):
        summary = pipeline_summary(
            self.companies,
            self.opportunities,
            self.queue,
        )
        blocked = sum(
            row["actionability_status"] == "ELIGIBILITY_BLOCKED"
            for row in self.opportunities
        )
        gates = sum(
            row["queue_rule_id"] == "RQ00_SME_ELIGIBILITY_GATE"
            for row in self.queue
        )
        self.assertEqual(summary["eligibility_blocked_opportunities"], blocked)
        self.assertEqual(summary["eligibility_gates"], gates)

    def test_missing_eligibility_gate_fails_generated_output_qa(self):
        reduced_queue = [
            row
            for row in self.queue
            if not (
                row["company_id"] == "P07"
                and row["queue_rule_id"] == "RQ00_SME_ELIGIBILITY_GATE"
            )
        ]
        errors = validate_generated_outputs(
            self.companies,
            self.opportunities,
            reduced_queue,
        )
        self.assertTrue(
            any("eligibility gates differ" in error for error in errors)
        )

    def test_pending_company_cannot_look_actionable(self):
        opportunities = [dict(row) for row in self.opportunities]
        target = next(
            row
            for row in opportunities
            if row["sample_eligibility_status"] == "ELIGIBILITY_PENDING"
        )
        target["actionability_status"] = "ACTIONABLE"
        errors = validate_generated_outputs(
            self.companies,
            opportunities,
            self.queue,
        )
        self.assertTrue(
            any("not eligibility-blocked" in error for error in errors)
        )

    def test_unknown_deployment_cannot_become_white_space(self):
        opportunities = [dict(row) for row in self.opportunities]
        target = next(
            row
            for row in opportunities
            if row["deployment_value"] == "UNKNOWN"
        )
        target["commercial_status"] = "WHITE_SPACE_POSSIBLE"
        errors = validate_generated_outputs(
            self.companies,
            opportunities,
            self.queue,
        )
        self.assertTrue(
            any("converts uncertainty to white space" in error for error in errors)
        )


if __name__ == "__main__":
    unittest.main()
