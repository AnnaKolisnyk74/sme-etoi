import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from export_web_data import build_web_payload


class WebExportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = build_web_payload(ROOT)

    def test_web_payload_covers_exactly_current_pilot(self):
        meta = self.payload["meta"]
        self.assertEqual(meta["company_count"], 100)
        self.assertEqual(meta["opportunity_count"], 198)
        self.assertEqual(meta["research_task_count"], 192)
        self.assertEqual(meta["score_work_task_count"], 452)
        self.assertEqual(meta["numeric_coding_task_count"], 440)
        self.assertEqual(meta["code_now_company_count"], 16)
        self.assertEqual(meta["eligibility_gate_count"], 12)
        self.assertEqual(meta["eligibility_blocked_company_count"], 12)
        self.assertEqual(len(self.payload["companies"]), 100)
        self.assertEqual(
            self.payload["score_readiness_summary"]["NEEDS_NUMERIC_CODING"],
            88,
        )
        self.assertEqual(
            self.payload["score_readiness_summary"]["NOT_SCOREABLE_ELIGIBILITY"],
            12,
        )

    def test_every_company_has_public_evidence_and_opportunity_output(self):
        for company in self.payload["companies"]:
            self.assertTrue(company["company_id"])
            self.assertTrue(company["legal_entity"])
            self.assertTrue(company["sources"])
            self.assertIsInstance(company["opportunities"], list)
            if company["company_id"] in {"P35", "P87", "P90", "P106", "P110"}:
                self.assertEqual(company["opportunities"], [])
            for source in company["sources"]:
                self.assertTrue(source["source_id"])
                self.assertTrue(source["final_url"].startswith("https://"))

    def test_eligibility_pending_companies_are_not_actionable(self):
        pending = []
        for company in self.payload["companies"]:
            for opportunity in company["opportunities"]:
                if opportunity["sample_eligibility_status"] == "ELIGIBILITY_PENDING":
                    pending.append(company["company_id"])
                    self.assertEqual(
                        opportunity["actionability_status"],
                        "ELIGIBILITY_BLOCKED",
                    )
        self.assertEqual(len(set(pending)), 12)

    def test_committed_web_snapshot_matches_exported_summary(self):
        path = ROOT / "web" / "data" / "sme_etoi.json"
        with path.open(encoding="utf-8") as handle:
            committed = json.load(handle)
        self.assertEqual(committed, self.payload)
        self.assertEqual(committed["meta"], self.payload["meta"])
        self.assertEqual(
            [row["company_id"] for row in committed["companies"]],
            [row["company_id"] for row in self.payload["companies"]],
        )

    def test_score_work_queue_is_exported_without_numeric_inference(self):
        summary = self.payload["score_work_summary"]
        self.assertEqual(summary["task_count"], 452)
        self.assertEqual(summary["workstream_counts"]["ELIGIBILITY"], 12)
        self.assertEqual(summary["workstream_counts"]["NUMERIC_CODING"], 440)

        all_tasks = [
            task
            for company in self.payload["companies"]
            for task in company["score_work_tasks"]
        ]
        self.assertEqual(len(all_tasks), 452)
        self.assertEqual(
            sorted(
                task["work_rank"]
                for task in all_tasks
                if task["work_rank"] <= 12
            ),
            list(range(1, 13)),
        )
        numeric_tasks = [
            task
            for task in all_tasks
            if task["workstream"] == "NUMERIC_CODING"
        ]
        status_counts = {}
        for task in numeric_tasks:
            status = task["task_status"]
            status_counts[status] = status_counts.get(status, 0) + 1
        self.assertEqual(
            status_counts,
            {
                "AWAITING_HUMAN_REVIEW": 61,
                "READY_TO_CODE": 80,
                "RESEARCH_NEEDED": 299,
            },
        )
        self.assertTrue(
            all(
                task["research_gap_fields"]
                for task in numeric_tasks
                if task["task_status"] == "RESEARCH_NEEDED"
            )
        )
        self.assertTrue(
            all(
                task["proposal_covered_fields"]
                for task in numeric_tasks
                if task["task_status"] == "AWAITING_HUMAN_REVIEW"
            )
        )
        self.assertTrue(
            all("opportunity_score" not in task for task in all_tasks)
        )

    def test_company_work_priority_exposes_next_best_company(self):
        summary = self.payload["company_work_summary"]
        self.assertEqual(summary["company_count"], 100)
        self.assertEqual(
            summary["workflow_action_counts"],
            {
                "CODE_NOW": 16,
                "ELIGIBILITY_FIRST": 12,
                "RESEARCH_FIRST": 69,
                "REVIEW_PROPOSALS": 3,
            },
        )
        next_best = summary["next_best_company"]
        self.assertEqual(next_best["company_id"], "P71")
        self.assertEqual(next_best["legal_entity"], "Flötzinger Brauerei Franz Steegmüller GmbH & Co. KG")
        self.assertEqual(next_best["coding_rank"], 1)
        self.assertEqual(next_best["priority_version"], "2.0.0")
        self.assertEqual(next_best["qa_result"], "PASS")
        self.assertEqual(next_best["expected_information_gain"], "MEDIUM")
        self.assertIn("PROCESS", next_best["source_coverage"])
        self.assertNotIn("ENERGY_TRANSITION", next_best["source_coverage"])
        self.assertTrue(next_best["coverage_source_ids"])
        self.assertNotIn("opportunity_score", next_best)

        companies = {
            company["company_id"]: company
            for company in self.payload["companies"]
        }
        self.assertEqual(
            companies["P11"]["workflow_priority"]["workflow_action"],
            "RESEARCH_FIRST",
        )
        self.assertEqual(
            companies["P11"]["workflow_priority"]["is_next_to_code"],
            "NO",
        )
        self.assertEqual(
            companies["P11"]["workflow_priority"]["coding_rank"],
            None,
        )
        self.assertTrue(
            all(
                company["workflow_priority"]["workflow_action"]
                for company in self.payload["companies"]
            )
        )
        self.assertEqual(
            companies["P71"]["workflow_priority"]["workflow_action"],
            "CODE_NOW",
        )
        self.assertEqual(
            companies["P71"]["workflow_priority"]["is_next_to_code"],
            "YES",
        )
        self.assertEqual(
            companies["P71"]["workflow_priority"]["coding_rank"],
            1,
        )
        self.assertEqual(
            companies["P20"]["workflow_priority"]["workflow_action"],
            "RESEARCH_FIRST",
        )
        self.assertEqual(
            companies["P20"]["workflow_priority"]["is_next_to_code"],
            "NO",
        )
        self.assertEqual(
            companies["P20"]["workflow_priority"]["coding_rank"],
            None,
        )
        self.assertEqual(
            companies["P53"]["workflow_priority"]["workflow_action"],
            "RESEARCH_FIRST",
        )
        self.assertEqual(
            companies["P53"]["workflow_priority"]["is_next_to_code"],
            "NO",
        )
        self.assertEqual(
            companies["P53"]["workflow_priority"]["coding_rank"],
            None,
        )

    def test_every_company_exposes_score_readiness(self):
        for company in self.payload["companies"]:
            readiness = company["score_readiness"]
            self.assertTrue(readiness["score_status"])
            self.assertTrue(readiness["next_action"])
        self.assertEqual(
            {
                company["company_id"]
                for company in self.payload["companies"]
                if company["score_readiness"]["score_status"]
                == "NOT_SCOREABLE_ELIGIBILITY"
            },
            {
                company["company_id"]
                for company in self.payload["companies"]
                if any(o["sample_eligibility_status"] == "ELIGIBILITY_PENDING"
                       for o in company["opportunities"])
            },
        )

    def test_static_ui_assets_exist_and_use_local_data(self):
        index = (ROOT / "web" / "index.html").read_text(encoding="utf-8")
        app = (ROOT / "web" / "app.js").read_text(encoding="utf-8")
        styles = (ROOT / "web" / "styles.css").read_text(encoding="utf-8")
        self.assertIn("SME-ETOI", index)
        self.assertIn('fetch("data/sme_etoi.json"', app)
        self.assertIn("--navy:", styles)
        self.assertNotIn("cdn.", index.lower())


    def test_sidebar_navigation_has_real_view_handlers(self):
        index = (ROOT / "web" / "index.html").read_text(encoding="utf-8")
        app = (ROOT / "web" / "app.js").read_text(encoding="utf-8")
        expected_views = {
            "home",
            "recent",
            "pinned",
            "dashboard",
            "tasks",
            "notes",
            "companies",
            "research",
            "opportunities",
            "analysis",
            "market",
            "regions",
            "sectors",
            "technologies",
            "methodology",
            "documentation",
        }
        for view in expected_views:
            self.assertIn(f'data-nav="{view}"', index)
        for functional_view in expected_views - {"dashboard", "companies", "research"}:
            self.assertIn(f'view==="{functional_view}"', app)
        self.assertIn("function showNav(view)", app)
        self.assertIn("localStorage", app)



    def test_collection_dom_queries_use_query_selector_all(self):
        app = (ROOT / "web" / "app.js").read_text(encoding="utf-8")
        collection_selectors = [
            ".nav-row",
            "#functionalContent [data-company-id]",
            "#companyRows tr[data-id]",
            "#researchRows tr[data-id]",
            ".note-item[data-company-id]",
            "[data-nav]",
        ]
        for selector in collection_selectors:
            self.assertIn(f'$$("{selector}").forEach', app)
            bad = rf'(?<!\$)\$\("{re.escape(selector)}"\)\.forEach'
            self.assertIsNone(re.search(bad, app))


if __name__ == "__main__":
    unittest.main()
