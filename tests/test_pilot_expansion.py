import csv
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_csv(relative_path):
    with open(ROOT / relative_path, newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


class PilotExpansionDataTests(unittest.TestCase):
    def test_first_expansion_batch_contains_five_canonical_companies(self):
        companies = read_csv("data/company_intelligence.csv")
        by_id = {row["company_id"]: row for row in companies}
        self.assertEqual(set(by_id), {"P03", "P04", "P05", "P07", "P10"})
        self.assertEqual(
            by_id["P04"]["legal_entity"],
            "Neumarkter Lammsbräu Gebr. Ehrnsperger KG",
        )
        self.assertEqual(by_id["P05"]["legal_entity"], "Einbecker Brauhaus AG")

    def test_company_intelligence_never_uses_no_for_unchecked_deployment(self):
        companies = read_csv("data/company_intelligence.csv")
        deployment_fields = [
            "heat_recovery_deployed",
            "energy_management_deployed",
            "flexibility_solution_deployed",
            "thermal_storage_deployed",
            "battery_storage_deployed",
            "power_quality_solution_deployed",
            "industrial_heat_electrification_deployed",
        ]
        for company in companies:
            for field in deployment_fields:
                self.assertIn(company[field], {"YES", "UNKNOWN"})

    def test_process_map_references_known_companies_and_processes(self):
        company_ids = {row["company_id"] for row in read_csv("data/company_intelligence.csv")}
        process_ids = {row["process_id"] for row in read_csv("data/process_library.csv")}
        mappings = read_csv("data/company_process_map.csv")
        self.assertTrue(mappings)
        for mapping in mappings:
            self.assertIn(mapping["company_id"], company_ids)
            self.assertIn(mapping["process_id"], process_ids)
            self.assertTrue(mapping["process_evidence_url"].startswith("https://"))


if __name__ == "__main__":
    unittest.main()
