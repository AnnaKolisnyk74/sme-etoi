"""Compare an independent sample double-code with the canonical SME-ETOI data."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANONICAL_PATH = "data/company_intelligence.csv"
PROCESS_MAP_PATH = "data/company_process_map.csv"
REVIEW_PATH = "data/pilot_double_code.csv"
RESULT_PATH = "outputs/inter_rater_reliability.csv"
CONFLICT_PATH = "outputs/double_code_conflicts.csv"

CERTIFICATE_VALUES = {
    "VALID",
    "EXPIRED",
    "DOCUMENT_FOUND_VALIDITY_UNCLEAR",
    "CLAIM_ONLY",
    "NOT_FOUND_AFTER_CHECK",
    "UNKNOWN",
}
DEPLOYMENT_VALUES = {"YES", "UNKNOWN"}

FIELDS = (
    "entity_check",
    "sme_status",
    "group_check",
    "process_ids",
    "iso_50001_status",
    "iso_14001_status",
    "emas_status",
    "heat_recovery_deployed",
    "energy_management_deployed",
    "flexibility_solution_deployed",
    "thermal_storage_deployed",
    "battery_storage_deployed",
    "power_quality_solution_deployed",
    "industrial_heat_electrification_deployed",
    "evidence_confidence",
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def normalize_process_ids(value: str) -> str:
    return "|".join(sorted(part.strip() for part in value.split("|") if part.strip()))


def canonical_values(
    companies: list[dict[str, str]], process_rows: list[dict[str, str]]
) -> dict[str, dict[str, str]]:
    processes: dict[str, list[str]] = {}
    for row in process_rows:
        processes.setdefault(row["company_id"], []).append(row["process_id"])

    values: dict[str, dict[str, str]] = {}
    for company in companies:
        company_id = company["company_id"]
        values[company_id] = {
            "entity_check": "CONFIRMED",
            "sme_status": company["sme_status"],
            "group_check": company["group_check"],
            "process_ids": normalize_process_ids("|".join(processes.get(company_id, []))),
            "iso_50001_status": company["iso_50001_status"],
            "iso_14001_status": company["iso_14001_status"],
            "emas_status": company["emas_status"],
            "heat_recovery_deployed": company["heat_recovery_deployed"],
            "energy_management_deployed": company["energy_management_deployed"],
            "flexibility_solution_deployed": company["flexibility_solution_deployed"],
            "thermal_storage_deployed": company["thermal_storage_deployed"],
            "battery_storage_deployed": company["battery_storage_deployed"],
            "power_quality_solution_deployed": company["power_quality_solution_deployed"],
            "industrial_heat_electrification_deployed": company[
                "industrial_heat_electrification_deployed"
            ],
            "evidence_confidence": company["evidence_confidence"],
        }
    return values


def validate_review(
    reviews: list[dict[str, str]], canonical: dict[str, dict[str, str]], known_process_ids: set[str]
) -> list[str]:
    errors: list[str] = []
    ids = [row["company_id"] for row in reviews]
    duplicate_ids = sorted(company_id for company_id, count in Counter(ids).items() if count > 1)
    if duplicate_ids:
        errors.append(f"duplicate review rows: {duplicate_ids}")
    if set(ids) != set(canonical):
        errors.append("double-code file must contain exactly the canonical company ids")

    allowed_by_field = {
        "entity_check": {"CONFIRMED", "CORRECTION_REQUIRED", "UNKNOWN"},
        "sme_status": {"eligible", "probable", "ineligible", "UNKNOWN"},
        "group_check": {value["group_check"] for value in canonical.values()} | {"UNKNOWN"},
        "iso_50001_status": CERTIFICATE_VALUES,
        "iso_14001_status": CERTIFICATE_VALUES,
        "emas_status": CERTIFICATE_VALUES,
        "heat_recovery_deployed": DEPLOYMENT_VALUES,
        "energy_management_deployed": DEPLOYMENT_VALUES,
        "flexibility_solution_deployed": DEPLOYMENT_VALUES,
        "thermal_storage_deployed": DEPLOYMENT_VALUES,
        "battery_storage_deployed": DEPLOYMENT_VALUES,
        "power_quality_solution_deployed": DEPLOYMENT_VALUES,
        "industrial_heat_electrification_deployed": DEPLOYMENT_VALUES,
        "evidence_confidence": {"A", "B", "C", "UNKNOWN"},
    }

    for row in reviews:
        company_id = row["company_id"]
        if company_id not in canonical:
            continue
        if row["review_status"] not in {"PENDING", "COMPLETE"}:
            errors.append(f"invalid review_status for {company_id}: {row['review_status']}")
            continue
        if row["review_status"] == "PENDING":
            continue
        for required in ("reviewer", "review_date", "source_ids_checked"):
            if not row[required].strip():
                errors.append(f"completed review missing {required} for {company_id}")
        for field in FIELDS:
            if not row[field].strip():
                errors.append(f"completed review missing {field} for {company_id}")
        for field, allowed in allowed_by_field.items():
            if row[field] and row[field] not in allowed:
                errors.append(f"invalid {field} for {company_id}: {row[field]}")
        process_ids = set(filter(None, normalize_process_ids(row["process_ids"]).split("|")))
        unknown_process_ids = sorted(process_ids - known_process_ids)
        if unknown_process_ids:
            errors.append(f"unknown process ids for {company_id}: {unknown_process_ids}")
    return errors


def cohens_kappa(pairs: list[tuple[str, str]]) -> str:
    if len(pairs) < 2:
        return "UNKNOWN"
    total = len(pairs)
    observed = sum(left == right for left, right in pairs) / total
    left_counts = Counter(left for left, _ in pairs)
    right_counts = Counter(right for _, right in pairs)
    categories = set(left_counts) | set(right_counts)
    expected = sum(
        (left_counts[category] / total) * (right_counts[category] / total)
        for category in categories
    )
    if expected == 1:
        return "NOT_DEFINED_SINGLE_CATEGORY"
    return f"{(observed - expected) / (1 - expected):.4f}"


def interpret_kappa(value: str) -> str:
    if value == "UNKNOWN":
        return "INSUFFICIENT_COMPLETED_REVIEWS"
    if value == "NOT_DEFINED_SINGLE_CATEGORY":
        return "PERCENT_AGREEMENT_ONLY"
    number = float(value)
    if number < 0:
        return "POOR"
    if number < 0.20:
        return "SLIGHT"
    if number < 0.40:
        return "FAIR"
    if number < 0.60:
        return "MODERATE"
    if number < 0.80:
        return "SUBSTANTIAL"
    return "ALMOST_PERFECT"


def analyze(
    reviews: list[dict[str, str]], canonical: dict[str, dict[str, str]]
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    complete = {row["company_id"]: row for row in reviews if row["review_status"] == "COMPLETE"}
    results: list[dict[str, str]] = []
    conflicts: list[dict[str, str]] = []
    total_pairs = 0
    total_agreements = 0

    for field in FIELDS:
        pairs: list[tuple[str, str]] = []
        for company_id, review in complete.items():
            reference = canonical[company_id][field]
            reviewed = review[field]
            if field == "process_ids":
                reviewed = normalize_process_ids(reviewed)
            pairs.append((reference, reviewed))
            if reference != reviewed:
                conflicts.append(
                    {
                        "company_id": company_id,
                        "field": field,
                        "canonical_value": reference,
                        "reviewer_value": reviewed,
                        "reviewer": review["reviewer"],
                        "review_date": review["review_date"],
                        "resolution_status": "OPEN",
                    }
                )
        agreements = sum(left == right for left, right in pairs)
        total_pairs += len(pairs)
        total_agreements += agreements
        kappa = cohens_kappa(pairs)
        results.append(
            {
                "field": field,
                "completed_pairs": str(len(pairs)),
                "agreements": str(agreements),
                "disagreements": str(len(pairs) - agreements),
                "percent_agreement": f"{agreements / len(pairs):.4f}" if pairs else "UNKNOWN",
                "cohens_kappa": kappa,
                "interpretation": interpret_kappa(kappa),
            }
        )

    results.append(
        {
            "field": "__OVERALL__",
            "completed_pairs": str(total_pairs),
            "agreements": str(total_agreements),
            "disagreements": str(total_pairs - total_agreements),
            "percent_agreement": (
                f"{total_agreements / total_pairs:.4f}" if total_pairs else "UNKNOWN"
            ),
            "cohens_kappa": "NOT_APPLICABLE",
            "interpretation": "FIELD_LEVEL_KAPPA_ONLY",
        }
    )
    return results, conflicts


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: tuple[str, ...]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def run(root: Path = ROOT) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    companies = read_csv(root / CANONICAL_PATH)
    process_rows = read_csv(root / PROCESS_MAP_PATH)
    reviews = read_csv(root / REVIEW_PATH)
    canonical = canonical_values(companies, process_rows)
    known_process_ids = {row["process_id"] for row in read_csv(root / "data/process_library.csv")}
    errors = validate_review(reviews, canonical, known_process_ids)
    if errors:
        raise ValueError("; ".join(errors))
    results, conflicts = analyze(reviews, canonical)
    write_csv(
        root / RESULT_PATH,
        results,
        (
            "field",
            "completed_pairs",
            "agreements",
            "disagreements",
            "percent_agreement",
            "cohens_kappa",
            "interpretation",
        ),
    )
    write_csv(
        root / CONFLICT_PATH,
        conflicts,
        (
            "company_id",
            "field",
            "canonical_value",
            "reviewer_value",
            "reviewer",
            "review_date",
            "resolution_status",
        ),
    )
    return results, conflicts


def main() -> int:
    try:
        results, conflicts = run()
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1
    completed = next(row for row in results if row["field"] == "entity_check")[
        "completed_pairs"
    ]
    total = len(read_csv(ROOT / REVIEW_PATH))
    print(f"Double-code analysis complete: {completed}/{total} company reviews completed.")
    print(f"Open field conflicts: {len(conflicts)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
