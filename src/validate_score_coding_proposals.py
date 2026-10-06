"""Validate non-canonical SME-ETOI score coding proposals.

Proposals are review artifacts only. They may suggest numeric anchors, but they
must never become canonical scores without explicit human review and a separate
canonical update.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from score_companies import DIMENSIONS


ROOT = Path(__file__).resolve().parents[1]

ALLOWED_ANCHORS = {
    "temperature_fit_score": {0, 3, 7, 10},
    "process_electrification_score": {0, 3, 7, 10},
    "fossil_heat_displacement_score": {0, 2, 4, 5},
    "motor_drive_score": {0, 2, 5, 8},
    "power_conversion_score": {0, 2, 5, 8},
    "automation_control_score": {0, 1, 3, 4},
    "scheduling_flex_score": {0, 2, 5, 8},
    "thermal_storage_flex_score": {0, 2, 5, 7},
    "incremental_load_score": {0, 2, 5, 8},
    "power_quality_score": {0, 1, 3, 4},
    "onsite_integration_score": {0, 1, 2, 3},
    "measures_gap_score": {0, 3, 7, 10},
    "management_gap_score": {0, 2, 3, 5},
    "targets_gap_score": {0, 2, 3, 5},
    "investment_gap_score": {0, 2, 3, 5},
}

FIELD_TO_DIMENSION = {
    field: dimension
    for dimension, fields in DIMENSIONS.items()
    for field in fields
}

ALLOWED_STATUSES = {
    "AWAITING_HUMAN_REVIEW",
    "NEEDS_RESEARCH",
    "APPROVED",
    "REJECTED",
    "SUPERSEDED",
}

ALLOWED_CONFIDENCE = {"A", "B", "C", "UNKNOWN"}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def split_source_ids(raw: str) -> list[str]:
    return [part.strip() for part in str(raw or "").split("|") if part.strip()]


def validate(
    root: Path = ROOT,
    proposal_path: Path | None = None,
) -> list[str]:
    proposal_path = proposal_path or root / "data" / "score_coding_proposals.csv"
    rows = read_csv(proposal_path)
    sources = read_csv(root / "evidence" / "source_register.csv")

    source_owner = {
        row["source_id"]: row["candidate_id"]
        for row in sources
        if row.get("source_id") and row.get("candidate_id")
    }

    errors: list[str] = []
    seen: set[tuple[str, str]] = set()

    for line_number, row in enumerate(rows, start=2):
        company_id = str(row.get("company_id", "")).strip()
        field = str(row.get("score_field", "")).strip()
        dimension = str(row.get("dimension", "")).strip()
        status = str(row.get("proposal_status", "")).strip().upper()
        confidence = str(row.get("proposal_confidence", "")).strip().upper()
        reviewer = str(row.get("reviewer", "")).strip()
        review_date = str(row.get("review_date", "")).strip()
        value_raw = str(row.get("proposed_value", "")).strip()
        missing_fact = str(row.get("missing_fact", "")).strip()

        key = (company_id, field)
        if key in seen:
            errors.append(f"line {line_number}: duplicate proposal key {key}")
        seen.add(key)

        if field not in ALLOWED_ANCHORS:
            errors.append(f"line {line_number}: unknown score field {field!r}")
            continue

        expected_dimension = FIELD_TO_DIMENSION[field]
        if dimension != expected_dimension:
            errors.append(
                f"line {line_number}: {field} belongs to {expected_dimension}, "
                f"not {dimension}"
            )

        if status == "NEEDS_RESEARCH":
            if value_raw:
                errors.append(
                    f"line {line_number}: NEEDS_RESEARCH must not carry a numeric proposed_value"
                )
            if not missing_fact:
                errors.append(
                    f"line {line_number}: NEEDS_RESEARCH requires missing_fact"
                )
        else:
            try:
                value = int(value_raw)
            except ValueError:
                errors.append(
                    f"line {line_number}: {field} proposed_value={value_raw!r} is not an integer"
                )
            else:
                if value not in ALLOWED_ANCHORS[field]:
                    errors.append(
                        f"line {line_number}: {field} proposed_value={value} is not an allowed anchor"
                    )

        try:
            max_value = int(str(row.get("max_value", "")).strip())
        except ValueError:
            errors.append(f"line {line_number}: invalid max_value")
        else:
            expected_max = max(ALLOWED_ANCHORS[field])
            if max_value != expected_max:
                errors.append(
                    f"line {line_number}: {field} max_value={max_value}, expected {expected_max}"
                )

        if confidence not in ALLOWED_CONFIDENCE:
            errors.append(
                f"line {line_number}: invalid proposal_confidence={confidence!r}"
            )
        elif status == "NEEDS_RESEARCH" and confidence != "UNKNOWN":
            errors.append(
                f"line {line_number}: NEEDS_RESEARCH requires proposal_confidence=UNKNOWN"
            )
        elif status != "NEEDS_RESEARCH" and confidence == "UNKNOWN":
            errors.append(
                f"line {line_number}: numeric/review proposal cannot use UNKNOWN confidence"
            )

        source_ids = split_source_ids(row.get("evidence_source_ids", ""))
        if not source_ids:
            errors.append(f"line {line_number}: no evidence source IDs")
        for source_id in source_ids:
            owner = source_owner.get(source_id)
            if owner is None:
                errors.append(
                    f"line {line_number}: unknown evidence source ID {source_id}"
                )
            elif owner != company_id:
                errors.append(
                    f"line {line_number}: source {source_id} belongs to {owner}, not {company_id}"
                )

        if not str(row.get("anchor_interpretation", "")).strip():
            errors.append(f"line {line_number}: anchor_interpretation is blank")

        if not str(row.get("evidence_basis", "")).strip():
            errors.append(f"line {line_number}: evidence_basis is blank")

        if status not in ALLOWED_STATUSES:
            errors.append(f"line {line_number}: invalid proposal_status={status!r}")
        elif status in {"AWAITING_HUMAN_REVIEW", "NEEDS_RESEARCH"}:
            if reviewer or review_date:
                errors.append(
                    f"line {line_number}: unresolved proposal cannot claim reviewer/date"
                )
        elif status in {"APPROVED", "REJECTED"}:
            if not reviewer or not review_date:
                errors.append(
                    f"line {line_number}: {status} requires reviewer and review_date"
                )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--proposals", type=Path)
    args = parser.parse_args()

    errors = validate(args.root, args.proposals)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("Score coding proposals passed validation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
