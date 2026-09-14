import csv
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from validate_pilot import validate


def read_csv(relative_path):
    with open(ROOT / relative_path, newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


class PilotExpansionDataTests(unittest.TestCase):
    def test_current_expansion_contains_forty_canonical_companies(self):
        companies = read_csv("data/company_intelligence.csv")
        by_id = {row["company_id"]: row for row in companies}
        self.assertEqual(len(by_id), 40)

        candidates = read_csv("data/pilot_candidates.csv")
        included = {
            row["candidate_id"] for row in candidates if row["eligibility_status"] == "INCLUDE"
        }
        self.assertEqual(set(by_id), included)

        strata = {}
        for row in candidates:
            if row["candidate_id"] in included:
                strata[row["process_stratum"]] = strata.get(row["process_stratum"], 0) + 1
        self.assertEqual(
            strata,
            {
                "food_beverage": 10,
                "plastics_processing": 10,
                "metal_surface_heat": 10,
                "glass_ceramics": 10,
            },
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
        self.assertEqual(
            by_id["P22"]["legal_entity"],
            "RIEDENBURGER BRAUHAUS Michael Krieger GmbH & Co. KG",
        )
        self.assertEqual(by_id["P24"]["legal_entity"], "H&K Müller GmbH & Co. KG")

    def test_current_direct_certificates_drive_only_supported_facts(self):
        companies = {
            row["company_id"]: row for row in read_csv("data/company_intelligence.csv")
        }
        certificates = read_csv("evidence/certificate_register.csv")
        by_key = {(row["candidate_id"], row["standard"]): row for row in certificates}

        for company_id in ("P16", "P18", "P19", "P24"):
            self.assertEqual(companies[company_id]["iso_50001_status"], "VALID")
            self.assertEqual(companies[company_id]["energy_management_deployed"], "YES")
            certificate = by_key[(company_id, "ISO 50001")]
            self.assertEqual(certificate["certificate_status"], "VALID")
            self.assertTrue(certificate["direct_certificate_url"].startswith("https://"))

        self.assertEqual(companies["P12"]["emas_status"], "VALID")
        self.assertEqual(companies["P12"]["pv_present"], "UNKNOWN")
        self.assertEqual(companies["P12"]["heat_recovery_deployed"], "UNKNOWN")
        self.assertEqual(companies["P11"]["iso_50001_status"], "VALID")
        self.assertEqual(companies["P11"]["iso_14001_status"], "VALID")
        self.assertEqual(companies["P23"]["iso_50001_status"], "VALID")
        self.assertEqual(companies["P25"]["iso_14001_status"], "EXPIRED")

    def test_second_pass_qa_finds_no_cross_file_errors(self):
        self.assertEqual(validate(ROOT), [])

    def test_certificate_register_has_one_row_per_candidate_and_standard(self):
        certificates = read_csv("evidence/certificate_register.csv")
        keys = [(row["candidate_id"], row["standard"]) for row in certificates]
        self.assertEqual(len(keys), len(set(keys)))

    def test_uncertain_process_mappings_are_strengthened_without_deployment_inference(self):
        companies = {
            row["company_id"]: row for row in read_csv("data/company_intelligence.csv")
        }
        mappings = {
            row["company_id"]: row for row in read_csv("data/company_process_map.csv")
            if row["company_id"] in {"P20", "P27"}
        }
        for company_id in ("P20", "P27"):
            self.assertEqual(mappings[company_id]["confidence"], "B")
            self.assertEqual(mappings[company_id]["review_status"], "QA_REVIEWED")
            self.assertEqual(
                companies[company_id]["industrial_heat_electrification_deployed"],
                "UNKNOWN",
            )

    def test_qa_matrix_keeps_independent_human_review_explicit(self):
        qa_rows = read_csv("evidence/qa_review.csv")
        self.assertEqual(len(qa_rows), 40)
        self.assertEqual(
            {row["independent_human_review_status"] for row in qa_rows},
            {"PENDING"},
        )

    def test_every_pilot_company_has_a_generated_opportunity(self):
        companies = {row["company_id"] for row in read_csv("data/company_intelligence.csv")}
        opportunity_companies = {row["company_id"] for row in read_csv("outputs/opportunities.csv")}
        self.assertEqual(opportunity_companies, companies)

        fm_plast = [
            row
            for row in read_csv("outputs/opportunities.csv")
            if row["company_id"] == "P23" and row["opportunity_type"] == "heat_recovery"
        ]
        self.assertEqual(len(fm_plast), 1)
        self.assertEqual(fm_plast[0]["commercial_status"], "ALREADY_DEPLOYED")
        self.assertEqual(fm_plast[0]["priority"], "LOW")

    def test_every_selected_company_has_auditable_evidence_assets(self):
        company_ids = {row["company_id"] for row in read_csv("data/company_intelligence.csv")}

        source_ids = {
            row["candidate_id"] for row in read_csv("evidence/source_register.csv")
        }
        self.assertTrue(company_ids.issubset(source_ids))

        certificate_rows = read_csv("evidence/certificate_register.csv")
        certificate_keys = {
            (row["candidate_id"], row["standard"]) for row in certificate_rows
        }
        for company_id in company_ids:
            for standard in ("ISO 50001", "ISO 14001", "EMAS"):
                self.assertIn((company_id, standard), certificate_keys)

        dossier_ids = {
            path.parent.name.split("_", 1)[0]
            for path in (ROOT / "evidence" / "companies").glob("*/evidence.md")
        }
        self.assertTrue(company_ids.issubset(dossier_ids))

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
