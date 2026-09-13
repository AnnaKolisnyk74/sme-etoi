"""Deterministic cross-file validation for the provisional SME-ETOI pilot."""

from __future__ import annotations

import csv
from collections import Counter
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECK_DATE = date(2026, 9, 13)
STANDARDS = ("ISO 50001", "ISO 14001", "EMAS")
DEPLOYMENT_FIELDS = (
    "heat_recovery_deployed",
    "energy_management_deployed",
    "flexibility_solution_deployed",
    "thermal_storage_deployed",
    "battery_storage_deployed",
    "power_quality_solution_deployed",
    "industrial_heat_electrification_deployed",
)


def read_csv(root: Path, relative_path: str) -> list[dict[str, str]]:
    with (root / relative_path).open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def duplicate_keys(rows: list[dict[str, str]], fields: tuple[str, ...]) -> list[tuple[str, ...]]:
    counts = Counter(tuple(row[field] for field in fields) for row in rows)
    return sorted(key for key, count in counts.items() if count > 1)


def validate(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    companies = read_csv(root, "data/company_intelligence.csv")
    candidates = read_csv(root, "data/pilot_candidates.csv")
    process_map = read_csv(root, "data/company_process_map.csv")
    sources = read_csv(root, "evidence/source_register.csv")
    certificates = read_csv(root, "evidence/certificate_register.csv")
    qa_rows = read_csv(root, "evidence/qa_review.csv")
    double_code_rows = read_csv(root, "data/pilot_double_code.csv")
    review_sources = read_csv(root, "data/pilot_review_sources.csv")

    company_duplicates = duplicate_keys(companies, ("company_id",))
    if company_duplicates:
        errors.append(f"duplicate company ids: {company_duplicates}")
    company_by_id = {row["company_id"]: row for row in companies}
    company_ids = set(company_by_id)
    if len(company_ids) != 20:
        errors.append(f"expected 20 canonical companies, found {len(company_ids)}")

    included_rows = [row for row in candidates if row["eligibility_status"] == "INCLUDE"]
    included_ids = {row["candidate_id"] for row in included_rows}
    if included_ids != company_ids:
        errors.append("INCLUDE candidates and canonical company ids differ")
    strata = Counter(row["process_stratum"] for row in included_rows)
    expected_strata = {
        "food_beverage": 5,
        "plastics_processing": 5,
        "metal_surface_heat": 5,
        "glass_ceramics": 5,
    }
    if dict(strata) != expected_strata:
        errors.append(f"unbalanced selected sample: {dict(strata)}")

    candidate_by_id = {row["candidate_id"]: row for row in candidates}
    for company_id, company in company_by_id.items():
        candidate = candidate_by_id.get(company_id)
        if candidate and candidate["legal_entity"] != company["legal_entity"]:
            errors.append(f"legal entity mismatch for {company_id}")
        for field in DEPLOYMENT_FIELDS:
            if company[field] not in {"YES", "UNKNOWN"}:
                errors.append(f"unsupported deployment value {company_id}.{field}={company[field]}")

    certificate_duplicates = duplicate_keys(certificates, ("candidate_id", "standard"))
    if certificate_duplicates:
        errors.append(f"duplicate certificate checks: {certificate_duplicates}")
    certificate_by_key = {
        (row["candidate_id"], row["standard"]): row for row in certificates
    }
    company_status_field = {
        "ISO 50001": "iso_50001_status",
        "ISO 14001": "iso_14001_status",
        "EMAS": "emas_status",
    }
    for company_id, company in company_by_id.items():
        for standard in STANDARDS:
            certificate = certificate_by_key.get((company_id, standard))
            if certificate is None:
                errors.append(f"missing {standard} check for {company_id}")
                continue
            if certificate["certificate_status"] == "PENDING_CHECK":
                errors.append(f"unfinished {standard} check for {company_id}")
            if company[company_status_field[standard]] != certificate["certificate_status"]:
                errors.append(f"certificate status mismatch for {company_id} {standard}")
            if certificate["certificate_status"] in {"VALID", "EXPIRED"}:
                if not certificate["direct_certificate_url"].startswith("https://"):
                    errors.append(f"missing direct certificate URL for {company_id} {standard}")
                if standard != "EMAS" and not certificate["valid_until"]:
                    errors.append(f"missing validity end for {company_id} {standard}")
                elif certificate["valid_until"]:
                    valid_until = date.fromisoformat(certificate["valid_until"])
                    if certificate["certificate_status"] == "VALID" and valid_until < CHECK_DATE:
                        errors.append(f"expired certificate marked VALID for {company_id} {standard}")
                    if certificate["certificate_status"] == "EXPIRED" and valid_until >= CHECK_DATE:
                        errors.append(f"current certificate marked EXPIRED for {company_id} {standard}")

    if duplicate_keys(sources, ("source_id",)):
        errors.append("duplicate source ids")
    sourced_ids = {row["candidate_id"] for row in sources}
    if not company_ids.issubset(sourced_ids):
        errors.append("one or more canonical companies have no source-register evidence")
    mapped_ids = {row["company_id"] for row in process_map}
    if not company_ids.issubset(mapped_ids):
        errors.append("one or more canonical companies have no process mapping")

    if duplicate_keys(qa_rows, ("company_id",)):
        errors.append("duplicate QA-review rows")
    qa_by_id = {row["company_id"]: row for row in qa_rows}
    if set(qa_by_id) != company_ids:
        errors.append("QA-review matrix does not cover exactly the canonical sample")
    for company_id, qa in qa_by_id.items():
        company = company_by_id[company_id]
        if qa["legal_entity"] != company["legal_entity"]:
            errors.append(f"QA legal entity mismatch for {company_id}")
        for field, expected in (
            ("legal_entity_check", "VERIFIED"),
            ("process_check", "SUPPORTED"),
            ("certificate_check", "COMPLETE"),
            ("evidence_traceability_check", "COMPLETE"),
            ("qa_result", "PASS"),
        ):
            if qa[field] != expected:
                errors.append(f"QA field {field} is not {expected} for {company_id}")
        if qa["independent_human_review_status"] != "PENDING":
            errors.append(f"unsupported human-review claim for {company_id}")

    if duplicate_keys(double_code_rows, ("company_id",)):
        errors.append("duplicate independent double-code rows")
    double_code_by_id = {row["company_id"]: row for row in double_code_rows}
    if set(double_code_by_id) != company_ids:
        errors.append("independent double-code template does not cover the canonical sample")
    for company_id, row in double_code_by_id.items():
        if row["legal_entity"] != company_by_id[company_id]["legal_entity"]:
            errors.append(f"double-code legal entity mismatch for {company_id}")
        if row["source_manifest_filter"] != company_id:
            errors.append(f"incorrect source-manifest filter for {company_id}")
        if row["review_status"] not in {"PENDING", "COMPLETE"}:
            errors.append(f"invalid double-code status for {company_id}")

    review_source_ids = {row["company_id"] for row in review_sources}
    if review_source_ids != company_ids:
        errors.append("neutral review-source manifest does not cover the canonical sample")
    forbidden_review_source_fields = {"evidence_fact", "review_status"}
    if review_sources and forbidden_review_source_fields.intersection(review_sources[0]):
        errors.append("neutral review-source manifest leaks prior coding fields")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("Pilot QA passed: 20 companies, balanced strata, unique evidence and certificate checks.")
    print("Independent human review remains explicitly PENDING for all 20 records.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
