"""Build a company-level workflow priority view from the score work queue."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from score_work_queue import confidence_rank, natural_company_key


ROOT = Path(__file__).resolve().parents[1]

OUTPUT_FIELDS = [
    "company_rank",
    "coding_rank",
    "company_id",
    "legal_entity",
    "workflow_action",
    "is_next_to_code",
    "company_work_rank",
    "first_work_rank",
    "ready_to_code_tasks",
    "research_needed_tasks",
    "awaiting_human_review_tasks",
    "checked_tasks",
    "open_gate_tasks",
    "other_tasks",
    "evidence_confidence",
    "process_confidence",
    "source_count",
    "qa_result",
    "verified_source_count",
    "source_coverage",
    "coverage_source_ids",
    "unassessed_field_count",
    "expected_information_gain",
    "information_gain_basis",
    "work_priority",
    "next_action",
    "priority_reason",
    "priority_version",
]

WORKFLOW_ORDER = {
    "CODE_NOW": 0,
    "RESEARCH_FIRST": 1,
    "REVIEW_PROPOSALS": 2,
    "CHECKED_PROPOSALS": 2,
    "ELIGIBILITY_FIRST": 3,
    "IN_PROGRESS": 4,
    "FINALIZE_SCORE": 5,
    "OTHER": 6,
    "QA_FIRST": 7,
}

PRIORITY_ORDER = {"GATE": 0, "P1": 1, "P2": 2, "P3": 3, "": 9}

# Documentary coverage, not score-field sufficiency or current deployment.
TRANSITION_SOURCE_TYPES = {
    "company_energy_page", "company_sustainability_page", "company_sustainability",
    "company_process_and_energy_page", "sustainability_report", "emas_document",
    "emas_environmental_statement", "government_case", "public_agency_case",
    "supplier_case_study", "company_hosted_technical_report", "company_research_page",
    "company_investment_page", "company_project_page", "regional_transformation_report",
}
MANAGEMENT_SOURCE_TYPES = {
    "direct_iso_certificate", "direct_combined_iso_certificate", "direct_emas_certificate",
    "energy_management_certificate", "environmental_management_certificate",
    "emas_document", "emas_environmental_statement",
}
GAIN_ORDER = {"HIGH": 0, "MEDIUM": 1, "LOW": 2, "UNKNOWN": 3}
VERSION = "2.0.0"


def evidence_metrics(
    company_id: str,
    rows: list[dict[str, str]],
    source_register: list[dict[str, str]],
    process_map: list[dict[str, str]],
) -> dict[str, str]:
    sources = [s for s in source_register
               if normalise(s.get("candidate_id")) == company_id
               and normalise(s.get("link_check_status")).upper() in {"VERIFIED", "REDIRECT_VERIFIED"}
               and normalise(s.get("source_link"))]
    # URLs are deduplicated: multiple register rows never buy a higher rank.
    urls = {normalise(s.get("final_url")) or normalise(s.get("source_link")) for s in sources}
    process_urls = {normalise(p.get("process_evidence_url")) for p in process_map
                    if normalise(p.get("company_id")) == company_id
                    and normalise(p.get("process_evidence_note"))
                    and confidence_rank(p.get("confidence")) < 3}
    coverage = set()
    coverage_ids = set()
    for source in sources:
        domains = set()
        if process_urls & {normalise(source.get("source_link")), normalise(source.get("final_url"))}:
            domains.add("PROCESS")
        kind = normalise(source.get("source_type"))
        if normalise(source.get("evidence_fact")):
            if kind in TRANSITION_SOURCE_TYPES:
                domains.add("ENERGY_TRANSITION")
            if kind in MANAGEMENT_SOURCE_TYPES:
                domains.add("MANAGEMENT")
        coverage.update(domains)
        if domains:
            coverage_ids.add(normalise(source.get("source_id")))
    unassessed = set()
    for row in rows:
        if row.get("task_type") != "CODE_DIMENSION":
            continue
        missing = {v.strip() for v in normalise(row.get("missing_fields")).split("|") if v.strip()}
        covered = {v.strip() for v in normalise(row.get("proposal_covered_fields")).split("|") if v.strip()}
        unassessed.update(missing - covered)
    if not sources:
        gain = "UNKNOWN"
    elif {"PROCESS", "ENERGY_TRANSITION"} <= coverage:
        gain = "HIGH"
    elif "PROCESS" in coverage:
        gain = "MEDIUM"
    else:
        gain = "LOW"
    basis = (
        f"Documentary gain proxy {gain}: {len(unassessed)} unassessed fields; "
        f"verified coverage={','.join(sorted(coverage)) or 'NONE'}; "
        "process coverage requires a source-linked firm-specific mapping. "
        "Energy/management coverage uses explicit source types, not inferred facts. "
        "Historical projects may inform coding but do not prove current deployment. "
        "This is not a predicted numeric-field yield or an SME-ETOI score."
    )
    return {
        "verified_source_count": str(len(urls)),
        "source_coverage": " | ".join(sorted(coverage)),
        "coverage_source_ids": " | ".join(sorted(coverage_ids)),
        "unassessed_field_count": str(len(unassessed)),
        "expected_information_gain": gain,
        "information_gain_basis": basis,
    }


def coding_key(row: dict[str, str]) -> tuple:
    return (
        max(confidence_rank(row["evidence_confidence"]), confidence_rank(row["process_confidence"])),
        confidence_rank(row["evidence_confidence"]),
        confidence_rank(row["process_confidence"]),
        GAIN_ORDER.get(row["expected_information_gain"], 3),
        -len([v for v in row["source_coverage"].split(" | ") if v]),
        -integer(row["unassessed_field_count"], 0),
        -min(integer(row["verified_source_count"], 0), 4),
        natural_company_key(row["company_id"]),
    )


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def normalise(value: object) -> str:
    return str(value or "").strip()


def integer(value: object, default: int = 10**9) -> int:
    text = normalise(value)
    if not text:
        return default
    try:
        return int(text)
    except ValueError:
        return default


def company_action(rows: list[dict[str, str]]) -> str:
    statuses = {normalise(row.get("task_status")) for row in rows}

    if "OPEN_GATE" in statuses:
        return "ELIGIBILITY_FIRST"
    if statuses & {"RESEARCH_NEEDED", "REWORK_REQUIRED", "OPEN_PREREQUISITE"}:
        return "RESEARCH_FIRST"
    if "IN_PROGRESS" in statuses or ("READY_TO_CODE" in statuses and len(statuses) > 1):
        return "IN_PROGRESS"
    if statuses & {"AWAITING_HUMAN_REVIEW", "AWAITING_CANONICAL_UPDATE"}:
        return "REVIEW_PROPOSALS"
    if statuses == {"CHECKED"}:
        return "CHECKED_PROPOSALS"
    if statuses == {"READY_TO_CODE"}:
        return "CODE_NOW"
    if statuses & {"READY_FOR_FINAL_SCORE"}:
        return "FINALIZE_SCORE"
    return "OTHER"


def action_next_step(action: str, rows: list[dict[str, str]]) -> str:
    if action == "CHECKED_PROPOSALS":
        return "Source and anchor checks are complete. Final-score approval remains a separate gate."
    if action == "CODE_NOW":
        return (
            "Open the company dossier and code the five SME-ETOI dimensions "
            "from source-linked evidence."
        )
    if action == "RESEARCH_FIRST":
        target = next(
            (
                row
                for row in rows
                if normalise(row.get("task_status"))
                in {"RESEARCH_NEEDED", "REWORK_REQUIRED", "OPEN_PREREQUISITE"}
            ),
            rows[0],
        )
        return normalise(target.get("next_action"))
    if action == "REVIEW_PROPOSALS":
        return (
            "Review the existing field-level proposals and evidence; approve, "
            "reject or request rework before any canonical update."
        )
    if action == "ELIGIBILITY_FIRST":
        target = next(
            (row for row in rows if normalise(row.get("task_status")) == "OPEN_GATE"),
            rows[0],
        )
        return normalise(target.get("next_action"))
    if action == "FINALIZE_SCORE":
        return "Run the frozen score calculation after all review gates pass."
    if action == "IN_PROGRESS":
        return "Complete the remaining first-pass coding before reviewing the full proposal set."
    return normalise(rows[0].get("next_action"))


def priority_reason(action: str, rows: list[dict[str, str]]) -> str:
    if action == "CHECKED_PROPOSALS":
        return "All field proposals in the current work package have documented source checks."
    first = rows[0]
    if action == "RESEARCH_FIRST":
        gaps = []
        for row in rows:
            value = normalise(row.get("research_gap_fields"))
            if value:
                gaps.append(value)
        unique = []
        for gap in gaps:
            if gap not in unique:
                unique.append(gap)
        suffix = "; ".join(unique[:3])
        return (
            "At least one score dimension contains an explicit unresolved fact"
            + (f": {suffix}" if suffix else ".")
        )
    if action == "REVIEW_PROPOSALS":
        return (
            "Field-level proposals already cover the remaining numeric work; "
            "the next valid step is human review, not additional first-pass coding."
        )
    if action == "ELIGIBILITY_FIRST":
        return (
            "SME/group eligibility is an upstream validity gate and blocks "
            "numeric scoring."
        )
    return normalise(first.get("queue_reason"))


def generate_company_work_priority(
    work_queue: list[dict[str, str]],
    source_register: list[dict[str, str]] | None = None,
    process_map: list[dict[str, str]] | None = None,
) -> list[dict[str, str]]:
    by_company: dict[str, list[dict[str, str]]] = {}
    for row in work_queue:
        company_id = normalise(row.get("company_id"))
        if company_id:
            by_company.setdefault(company_id, []).append(row)

    records: list[dict[str, str]] = []

    for company_id, rows in by_company.items():
        rows = sorted(rows, key=lambda row: integer(row.get("work_rank")))
        first = rows[0]
        action = company_action(rows)
        if action == "CODE_NOW" and any(normalise(r.get("qa_result")).upper() != "PASS" for r in rows):
            action = "QA_FIRST"
        statuses = [normalise(row.get("task_status")) for row in rows]

        priorities = [normalise(row.get("work_priority")) for row in rows]
        work_priority = min(
            priorities,
            key=lambda value: PRIORITY_ORDER.get(value, 9),
        )

        records.append(
            {
                "company_rank": "",
                "coding_rank": "",
                "company_id": company_id,
                "legal_entity": normalise(first.get("legal_entity")),
                "workflow_action": action,
                "is_next_to_code": "NO",
                "company_work_rank": normalise(first.get("company_work_rank")),
                "first_work_rank": str(min(integer(row.get("work_rank")) for row in rows)),
                "ready_to_code_tasks": str(statuses.count("READY_TO_CODE")),
                "checked_tasks": str(statuses.count("CHECKED")),
                "research_needed_tasks": str(
                    sum(
                        status
                        in {"RESEARCH_NEEDED", "REWORK_REQUIRED", "OPEN_PREREQUISITE"}
                        for status in statuses
                    )
                ),
                "awaiting_human_review_tasks": str(
                    sum(
                        status
                        in {"AWAITING_HUMAN_REVIEW", "AWAITING_CANONICAL_UPDATE"}
                        for status in statuses
                    )
                ),
                "open_gate_tasks": str(statuses.count("OPEN_GATE")),
                "other_tasks": str(
                    sum(
                        status
                        not in {
                            "CHECKED",
                            "READY_TO_CODE",
                            "RESEARCH_NEEDED",
                            "REWORK_REQUIRED",
                            "OPEN_PREREQUISITE",
                            "AWAITING_HUMAN_REVIEW",
                            "AWAITING_CANONICAL_UPDATE",
                            "OPEN_GATE",
                        }
                        for status in statuses
                    )
                ),
                "evidence_confidence": normalise(first.get("evidence_confidence")),
                "process_confidence": normalise(first.get("process_confidence")),
                "source_count": normalise(first.get("source_count")),
                "qa_result": normalise(first.get("qa_result")),
                "work_priority": work_priority,
                "next_action": action_next_step(action, rows),
                "priority_reason": priority_reason(action, rows),
                "priority_version": VERSION,
                **evidence_metrics(company_id, rows, source_register or [], process_map or []),
            }
        )

    for record in records:
        if record["workflow_action"] == "CODE_NOW":
            record["priority_reason"] = (
                "QA PASS; rank by worst confidence, evidence/process confidence, documentary gain, "
                "coverage breadth, unassessed fields, verified URLs (cap 4), then company ID. "
                + record["information_gain_basis"]
            )
        elif record["workflow_action"] == "QA_FIRST":
            record["next_action"] = "Resolve deterministic QA before starting first-pass numeric coding."
            record["priority_reason"] = "QA is not PASS; this company cannot enter the coding batch."

    def overall_key(row: dict[str, str]) -> tuple:
        if row["workflow_action"] == "CODE_NOW":
            return (0, *coding_key(row))
        return (
            WORKFLOW_ORDER.get(row["workflow_action"], 99),
            PRIORITY_ORDER.get(row["work_priority"], 9),
            integer(row["company_work_rank"]),
            integer(row["first_work_rank"]),
            row["company_id"],
        )

    records.sort(key=overall_key)

    for index, row in enumerate(records, start=1):
        row["company_rank"] = str(index)

    code_now = [row for row in records if row["workflow_action"] == "CODE_NOW"]
    code_now.sort(key=coding_key)
    for index, row in enumerate(code_now, start=1):
        row["coding_rank"] = str(index)
        if index == 1:
            row["is_next_to_code"] = "YES"

    return records


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def run(root: Path = ROOT, output: Path | None = None) -> list[dict[str, str]]:
    rows = generate_company_work_priority(
        read_csv(root / "outputs" / "score_work_queue.csv"),
        read_csv(root / "evidence" / "source_register.csv"),
        read_csv(root / "data" / "company_process_map.csv"),
    )
    write_csv(output or root / "outputs" / "company_work_priority.csv", rows)
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate company-level SME-ETOI workflow priority."
    )
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    rows = run(args.root, args.output)
    counts: dict[str, int] = {}
    for row in rows:
        counts[row["workflow_action"]] = counts.get(row["workflow_action"], 0) + 1
    next_to_code = next(
        (row for row in rows if row["is_next_to_code"] == "YES"),
        None,
    )
    summary = ", ".join(f"{key}={counts[key]}" for key in sorted(counts))
    if next_to_code:
        print(
            f"Wrote {len(rows)} company-priority rows. {summary}. "
            f"Next to code: {next_to_code['company_id']} "
            f"{next_to_code['legal_entity']}."
        )
    else:
        print(f"Wrote {len(rows)} company-priority rows. {summary}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
