import csv
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_csv(relative_path):
    with open(ROOT / relative_path, newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


class PilotExpansionDataTests(unittest.TestCase):
    def test_second_expansion_batch_contains_ten_canonical_companies(self):
        companies = read_csv("data/company_intelligence.csv")
        by_id = {row["company_id"]: row for row in companies}
        self.assertEqual(
            set(by_id),
            {"P03", "P04", "P05", "P07", "P10", "P12", "P13", "P16", "P18", "P19"},
        )
        self.assertEqual(
            by_id["P04"]["legal_entity"],
            "Neumarkter Lammsbräu Gebr. Ehrnsperger KG",
        )
        self.assertEqual(by_id["P05"]["legal_entity"], "Einbecker Brauhaus AG")
        self.assertEqual(by_id["P13"]["legal_entity"], "Schmalriede-Zink GmbH")
        self.assertEqual(
            by_id["P19"]["legal_entity"],
            "Glasfabrik Lamberts GmbH & Co. KG",
        )

    def test_current_direct_certificates_drive_only_supported_facts(self):
        companies = {
            row["company_id"]: row for row in read_csv("data/company_intelligence.csv")
        }
        certificates = read_csv("evidence/certificate_register.csv")
        by_key = {(row["candidate_id"], row["standard"]): row for row in certificates}

        for company_id in ("P16", "P18", "P19"):
            self.assertEqual(companies[company_id]["iso_50001_status"], "VALID")
            self.assertEqual(companies[company_id]["energy_management_deployed"], "YES")
            certificate = by_key[(company_id, "ISO 50001")]
            self.assertEqual(certificate["certificate_status"], "VALID")
            self.assertTrue(certificate["direct_certificate_url"].startswith("https://"))

        self.assertEqual(companies["P12"]["emas_status"], "VALID")
        self.assertEqual(companies["P12"]["pv_present"], "UNKNOWN")
        self.assertEqual(companies["P12"]["heat_recovery_deployed"], "UNKNOWN")

    def test_new_process_strata_are_represented(self):
        processes = {row["process_id"]: row for row in read_csv("data/process_library.csv")}
        mappings = read_csv("data/company_process_map.csv")
        process_ids = {row["process_id"] for row in mappings if row["company_id"] in {"P12", "P13", "P16", "P18", "P19"}}
        self.assertEqual(process_ids, {"PR005", "PR007", "PR008", "PR009"})
        self.assertEqual(processes["PR009"]["process_name"], "powder_coating")

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
