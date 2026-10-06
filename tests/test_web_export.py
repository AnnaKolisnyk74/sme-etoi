import json
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
        self.assertEqual(meta["opportunity_count"], 203)
        self.assertEqual(meta["research_task_count"], 198)
        self.assertEqual(meta["eligibility_gate_count"], 12)
        self.assertEqual(meta["eligibility_blocked_company_count"], 12)
        self.assertEqual(len(self.payload["companies"]), 100)

    def test_every_company_has_public_evidence_and_opportunity_output(self):
        for company in self.payload["companies"]:
            self.assertTrue(company["company_id"])
            self.assertTrue(company["legal_entity"])
            self.assertTrue(company["sources"])
            self.assertTrue(company["opportunities"])
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
        self.assertEqual(committed["meta"], self.payload["meta"])
        self.assertEqual(
            [row["company_id"] for row in committed["companies"]],
            [row["company_id"] for row in self.payload["companies"]],
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
        bad_patterns = [
            '$(".nav-row").forEach',
            '$("#functionalContent [data-company-id]").forEach',
            '$("#companyRows tr[data-id]").forEach',
            '$("#researchRows tr[data-id]").forEach',
            '$(".note-item[data-company-id]").forEach',
            '$("[data-nav]").forEach',
        ]
        for pattern in bad_patterns:
            self.assertNotIn(pattern, app)
        self.assertIn('$("[data-nav]").forEach', app)
        self.assertIn('$("#researchRows tr[data-id]").forEach', app)



if __name__ == "__main__":
    unittest.main()
