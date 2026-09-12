#!/usr/bin/env python3
"""Calculate the Energy Transition Opportunity Index from coded public evidence."""

from __future__ import annotations

import argparse
import csv
from datetime import date, datetime
from pathlib import Path


SCORE_FIELDS = {
    "sector_energy_profile_score": 15,
    "process_evidence_score": 15,
    "site_scale_score": 10,
    "low_temp_fit_score": 10,
    "electrification_fit_score": 10,
    "flexibility_fit_score": 10,
    "measures_gap_score": 12,
    "management_gap_score": 6,
    "targets_gap_score": 6,
    "investment_gap_score": 6,
}

SOURCE_CHECK_FIELDS = (
    "company_website_checked",
    "report_checked",
    "official_register_checked",
    "certification_source_checked",
    "independent_source_checked",
)


def parse_int(row: dict[str, str], field: str, maximum: int) -> int:
    raw = row.get(field, "").strip()
    if raw == "":
        raise ValueError(f"{field} is blank")
    value = int(raw)
    if not 0 <= value <= maximum:
        raise ValueError(f"{field}={value} is outside 0..{maximum}")
    return value


def months_between(earlier: date, later: date) -> int:
    months = (later.year - earlier.year) * 12 + later.month - earlier.month
    return months - (1 if later.day < earlier.day else 0)


def opportunity_band(score: int) -> str:
    if score < 40:
        return "LOW"
    if score < 70:
        return "MEDIUM"
    return "HIGH"


def score_row(row: dict[str, str], as_of: date) -> dict[str, str]:
    values = {
        field: parse_int(row, field, maximum)
        for field, maximum in SCORE_FIELDS.items()
    }

    demand = sum(values[field] for field in (
        "sector_energy_profile_score", "process_evidence_score", "site_scale_score"
    ))
    applicability = sum(values[field] for field in (
        "low_temp_fit_score", "electrification_fit_score", "flexibility_fit_score"
    ))
    gap = sum(values[field] for field in (
        "measures_gap_score", "management_gap_score", "targets_gap_score",
        "investment_gap_score"
    ))
    total = demand + applicability + gap

    checks = [parse_int(row, field, 1) for field in SOURCE_CHECK_FIELDS]
    coverage = 20 * sum(checks)

    latest_text = row.get("latest_evidence_date", "").strip()
    evidence_age_months = ""
    confidence = "C"
    if latest_text:
        latest = datetime.strptime(latest_text, "%Y-%m-%d").date()
        age = months_between(latest, as_of)
        evidence_age_months = str(age)
        if coverage >= 80 and age <= 24:
            confidence = "A"
        elif coverage >= 60 and age <= 48:
            confidence = "B"

    band = opportunity_band(total) if confidence in {"A", "B"} else ""
    status = "CLASSIFIED" if band else "RESEARCH_REQUIRED"

    result = dict(row)
    result.update({
        "demand_potential_score": str(demand),
        "solution_applicability_score": str(applicability),
        "observed_transition_gap_score": str(gap),
        "opportunity_score": str(total),
        "evidence_coverage": str(coverage),
        "evidence_age_months": evidence_age_months,
        "confidence_grade": confidence,
        "opportunity_band": band,
        "classification_status": status,
    })
    return result


def run(input_path: Path, output_path: Path, as_of: date) -> None:
    with input_path.open("r", encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        if reader.fieldnames is None:
            raise ValueError("Input CSV has no header")
        rows = []
        for line_number, row in enumerate(reader, start=2):
            try:
                rows.append(score_row(row, as_of))
            except Exception as exc:
                company = row.get("company_id") or row.get("company_name") or "unknown"
                raise ValueError(f"Row {line_number} ({company}): {exc}") from exc

    extra_fields = [
        "demand_potential_score", "solution_applicability_score",
        "observed_transition_gap_score", "opportunity_score", "evidence_coverage",
        "evidence_age_months", "confidence_grade", "opportunity_band",
        "classification_status",
    ]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as target:
        writer = csv.DictWriter(target, fieldnames=list(reader.fieldnames) + extra_fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_csv", type=Path)
    parser.add_argument("output_csv", type=Path)
    parser.add_argument("--as-of", default=date.today().isoformat())
    args = parser.parse_args()
    run(args.input_csv, args.output_csv, datetime.strptime(args.as_of, "%Y-%m-%d").date())


if __name__ == "__main__":
    main()
