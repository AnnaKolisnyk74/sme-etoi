#!/usr/bin/env python3
"""Calculate SME-ETOI from coded public evidence."""

from __future__ import annotations

import argparse
import csv
from datetime import date, datetime
from pathlib import Path


DIMENSIONS = {
    "process_electrification_potential": {
        "temperature_fit_score": 10,
        "process_electrification_score": 10,
        "fossil_heat_displacement_score": 5,
    },
    "power_electronics_relevance": {
        "motor_drive_score": 8,
        "power_conversion_score": 8,
        "automation_control_score": 4,
    },
    "load_flexibility_potential": {
        "scheduling_flex_score": 8,
        "thermal_storage_flex_score": 7,
    },
    "grid_power_quality_relevance": {
        "incremental_load_score": 8,
        "power_quality_score": 4,
        "onsite_integration_score": 3,
    },
    "observed_transition_gap": {
        "measures_gap_score": 10,
        "management_gap_score": 5,
        "targets_gap_score": 5,
        "investment_gap_score": 5,
    },
}

SCORE_FIELDS = {
    field: maximum
    for components in DIMENSIONS.values()
    for field, maximum in components.items()
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
    dimension_scores = {
        dimension: sum(values[field] for field in components)
        for dimension, components in DIMENSIONS.items()
    }
    total = sum(dimension_scores.values())

    checks = [parse_int(row, field, 1) for field in SOURCE_CHECK_FIELDS]
    coverage = 20 * sum(checks)

    latest_text = row.get("latest_evidence_date", "").strip()
    evidence_age_months = ""
    confidence = "C"
    if latest_text:
        latest = datetime.strptime(latest_text, "%Y-%m-%d").date()
        age = months_between(latest, as_of)
        if age < 0:
            raise ValueError("latest_evidence_date is after the as-of date")
        evidence_age_months = str(age)
        if coverage >= 80 and age <= 24:
            confidence = "A"
        elif coverage >= 60 and age <= 48:
            confidence = "B"

    band = opportunity_band(total) if confidence in {"A", "B"} else ""
    status = "CLASSIFIED" if band else "RESEARCH_REQUIRED"

    result = dict(row)
    result.update({key: str(value) for key, value in dimension_scores.items()})
    result.update({
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
        *DIMENSIONS.keys(), "opportunity_score", "evidence_coverage",
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
