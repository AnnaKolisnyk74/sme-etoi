"""Assess whether each canonical SME-ETOI company is ready for scoring.

This module does not invent scores. It checks the gates required by the existing
methodology and exposes the exact blocker that must be resolved next.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from score_companies import SCORE_FIELDS


ROOT = Path(__file__).resolve().parents[1]

UNRESOLVED_GROUP_CHECKS = {
    "unknown",
    "linked_enterprise_check",
    "partner_or_linked_sme",
    "state_owned_sme_check",
}

EXCLUDED_SME_STATUSES = {
    "excluded",
    "not_sme",
    "ineligible",
}

REQUIRED_CERTIFICATES = ("ISO 50001", "ISO 14001", "EMAS")

PENDING_CERTIFICATE_STATUSES = {
    "",
    "PENDING",
    "PENDING_CHECK",
    "NOT_REVIEWED",
    "TO_RESEARCH",
    "UNKNOWN",
}

HUMAN_REVIEW_COMPLETE = {
    "APPROVED",
    "COMPLETE",
    "COMPLETED",
    "REVIEWED",
    "DONE",
}

OUTPUT_FIELDS = [
    "company_id",
    "legal_entity",
    "sme_status",
    "group_check",
    "eligibility_gate",
    "process_mapping_status",
    "certificate_check_status",
    "numeric_coding_status",
    "independent_human_review_status",
    "score_status",
    "existing_score",
    "existing_band",
    "existing_confidence_grade",
    "existing_score_status",
    "blocking_reasons",
    "next_action",
    "readiness_version",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def normalise(value: object) -> str:
    return str(value or "").strip()


def natural_company_key(company_id: str) -> tuple[int, str]:
    text = normalise(company_id)
    if text.startswith("P") and text[1:].isdigit():
        return int(text[1:]), text
    return 10**9, text


def certificate_status_by_company(
    certificate_rows: list[dict[str, str]],
) -> dict[str, dict[str, str]]:
    output: dict[str, dict[str, str]] = {}
    for row in certificate_rows:
        company_id = normalise(row.get("candidate_id"))
        standard = normalise(row.get("standard"))
        if not company_id or not standard:
            continue
        output.setdefault(company_id, {})[standard] = normalise(
            row.get("certificate_status")
        ).upper()
    return output


def numeric_coding_complete(row: dict[str, str] | None) -> bool:
    if not row:
        return False
    return all(normalise(row.get(field)) != "" for field in SCORE_FIELDS)


def evaluate_company(
    company: dict[str, str],
    *,
    process_rows: list[dict[str, str]],
    certificate_rows: dict[str, str],
    qa_row: dict[str, str] | None,
    coded_row: dict[str, str] | None,
    scored_row: dict[str, str] | None,
) -> dict[str, str]:
    company_id = normalise(company.get("company_id"))
    legal_entity = normalise(company.get("legal_entity"))
    sme_status = normalise(company.get("sme_status")).lower()
    group_check = normalise(company.get("group_check")).lower()

    blocking: list[str] = []

    if sme_status in EXCLUDED_SME_STATUSES:
        eligibility_gate = "EXCLUDED"
        blocking.append(f"sme_status={sme_status}")
    elif group_check in UNRESOLVED_GROUP_CHECKS:
        eligibility_gate = "UNRESOLVED"
        blocking.append(f"group_check={group_check}")
    else:
        eligibility_gate = "PROVISIONAL_PASS"

    if process_rows:
        process_mapping_status = "PRESENT"
    else:
        process_mapping_status = "MISSING"
        blocking.append("no company_process_map row")

    missing_certificate_checks: list[str] = []
    pending_certificate_checks: list[str] = []
    for standard in REQUIRED_CERTIFICATES:
        status = normalise(certificate_rows.get(standard)).upper()
        if not status:
            missing_certificate_checks.append(standard)
        elif status in PENDING_CERTIFICATE_STATUSES:
            pending_certificate_checks.append(f"{standard}:{status}")

    if missing_certificate_checks:
        certificate_check_status = "MISSING"
        blocking.append(
            "missing certificate checks: " + ", ".join(missing_certificate_checks)
        )
    elif pending_certificate_checks:
        certificate_check_status = "PENDING"
        blocking.append(
            "pending certificate checks: " + ", ".join(pending_certificate_checks)
        )
    else:
        certificate_check_status = "COMPLETE"

    if numeric_coding_complete(coded_row):
        numeric_coding_status = "COMPLETE"
    elif coded_row:
        numeric_coding_status = "INCOMPLETE"
        missing_numeric = [
            field for field in SCORE_FIELDS if not normalise(coded_row.get(field))
        ]
        blocking.append("numeric coding incomplete: " + ", ".join(missing_numeric))
    else:
        numeric_coding_status = "MISSING"
        blocking.append("numeric ETOI coding missing")

    human_review = normalise(
        (qa_row or {}).get("independent_human_review_status")
    ).upper() or "NOT_RECORDED"
    human_review_ready = human_review in HUMAN_REVIEW_COMPLETE
    if not human_review_ready:
        blocking.append(f"independent human review={human_review}")

    if eligibility_gate == "EXCLUDED":
        score_status = "EXCLUDED"
        next_action = (
            "Keep the company out of the SME scoring sample and preserve the "
            "exclusion evidence."
        )
    elif eligibility_gate == "UNRESOLVED":
        score_status = "NOT_SCOREABLE_ELIGIBILITY"
        next_action = (
            "Resolve ownership, linked-enterprise aggregation and EU SME "
            "eligibility before treating any ETOI score as valid."
        )
    elif process_mapping_status == "MISSING":
        score_status = "NOT_SCOREABLE_PROCESS"
        next_action = (
            "Add firm-specific process evidence and a company-process mapping."
        )
    elif certificate_check_status != "COMPLETE":
        score_status = "NOT_SCOREABLE_CERTIFICATES"
        next_action = (
            "Complete ISO 50001, ISO 14001 and EMAS checks before coding the "
            "management-system gap."
        )
    elif numeric_coding_status != "COMPLETE":
        score_status = "NEEDS_NUMERIC_CODING"
        next_action = (
            "Code the existing methodology v0.2 numeric anchors with source-linked "
            "justifications; do not infer missing values from generic process data."
        )
    elif not human_review_ready:
        score_status = "PROVISIONAL_SCORE_ONLY"
        next_action = (
            "Complete independent human review before treating the score or band as "
            "final."
        )
    else:
        score_status = "FINAL_SCORE_READY"
        next_action = (
            "Run the frozen score calculation and publish the score with its "
            "confidence grade and evidence trail."
        )

    existing_score = normalise((scored_row or {}).get("opportunity_score"))
    existing_band = normalise((scored_row or {}).get("opportunity_band"))
    existing_confidence = normalise((scored_row or {}).get("confidence_grade"))

    if existing_score:
        if score_status == "FINAL_SCORE_READY":
            existing_score_status = "FINAL_ELIGIBLE"
        else:
            existing_score_status = "LEGACY_PROVISIONAL_NOT_FINAL"
    else:
        existing_score_status = "NONE"

    return {
        "company_id": company_id,
        "legal_entity": legal_entity,
        "sme_status": normalise(company.get("sme_status")),
        "group_check": normalise(company.get("group_check")),
        "eligibility_gate": eligibility_gate,
        "process_mapping_status": process_mapping_status,
        "certificate_check_status": certificate_check_status,
        "numeric_coding_status": numeric_coding_status,
        "independent_human_review_status": human_review,
        "score_status": score_status,
        "existing_score": existing_score,
        "existing_band": existing_band,
        "existing_confidence_grade": existing_confidence,
        "existing_score_status": existing_score_status,
        "blocking_reasons": " | ".join(blocking),
        "next_action": next_action,
        "readiness_version": "1.0.0",
    }


def generate_score_readiness(
    companies: list[dict[str, str]],
    process_map: list[dict[str, str]],
    certificate_register: list[dict[str, str]],
    qa_review: list[dict[str, str]],
    coded_rows: list[dict[str, str]],
    scored_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    process_by_company: dict[str, list[dict[str, str]]] = {}
    for row in process_map:
        process_by_company.setdefault(normalise(row.get("company_id")), []).append(row)

    certificates_by_company = certificate_status_by_company(certificate_register)
    qa_by_company = {
        normalise(row.get("company_id")): row
        for row in qa_review
        if normalise(row.get("company_id"))
    }
    coded_by_company = {
        normalise(row.get("company_id")): row
        for row in coded_rows
        if normalise(row.get("company_id"))
    }
    scored_by_company = {
        normalise(row.get("company_id")): row
        for row in scored_rows
        if normalise(row.get("company_id"))
    }

    rows = []
    for company in companies:
        company_id = normalise(company.get("company_id"))
        rows.append(
            evaluate_company(
                company,
                process_rows=process_by_company.get(company_id, []),
                certificate_rows=certificates_by_company.get(company_id, {}),
                qa_row=qa_by_company.get(company_id),
                coded_row=coded_by_company.get(company_id),
                scored_row=scored_by_company.get(company_id),
            )
        )

    return sorted(rows, key=lambda row: natural_company_key(row["company_id"]))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def run(root: Path = ROOT, output: Path | None = None) -> list[dict[str, str]]:
    rows = generate_score_readiness(
        read_csv(root / "data" / "company_intelligence.csv"),
        read_csv(root / "data" / "company_process_map.csv"),
        read_csv(root / "evidence" / "certificate_register.csv"),
        read_csv(root / "evidence" / "qa_review.csv"),
        read_csv(root / "data" / "pilot_coded.csv"),
        read_csv(root / "outputs" / "pilot_scored.csv"),
    )
    write_csv(output or root / "outputs" / "score_readiness.csv", rows)
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate score-readiness gates for the canonical SME-ETOI sample."
    )
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    rows = run(args.root, args.output)
    counts: dict[str, int] = {}
    for row in rows:
        counts[row["score_status"]] = counts.get(row["score_status"], 0) + 1

    summary = ", ".join(f"{key}={counts[key]}" for key in sorted(counts))
    print(f"Wrote {len(rows)} score-readiness rows. {summary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
