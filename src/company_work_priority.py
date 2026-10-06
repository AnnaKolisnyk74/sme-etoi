"""Build a company-level workflow priority view from the score work queue."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


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
    "open_gate_tasks",
    "other_tasks",
    "evidence_confidence",
    "process_confidence",
    "source_count",
    "qa_result",
    "work_priority",
    "next_action",
    "priority_reason",
    "priority_version",
]

WORKFLOW_ORDER = {
    "CODE_NOW": 0,
    "RESEARCH_FIRST": 1,
    "REVIEW_PROPOSALS": 2,
    "ELIGIBILITY_FIRST": 3,
    "IN_PROGRESS": 4,
    "FINALIZE_SCORE": 5,
    "OTHER": 6,
}

PRIORITY_ORDER = {"GATE": 0, "P1": 1, "P2": 2, "P3": 3, "": 9}


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
    if statuses & {"AWAITING_HUMAN_REVIEW", "AWAITING_CANONICAL_UPDATE"}:
        return "REVIEW_PROPOSALS"
    if statuses == {"READY_TO_CODE"}:
        return "CODE_NOW"
    if "IN_PROGRESS" in statuses:
        return "IN_PROGRESS"
    if statuses & {"READY_FOR_FINAL_SCORE"}:
        return "FINALIZE_SCORE"
    return "OTHER"


def action_next_step(action: str, rows: list[dict[str, str]]) -> str:
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
    return normalise(rows[0].get("next_action"))


def priority_reason(action: str, rows: list[dict[str, str]]) -> str:
    first = rows[0]
    if action == "CODE_NOW":
        return (
            "All five numeric-coding packages are untouched and ready; ranking "
            "inherits evidence/process confidence, QA state and source coverage "
            "from the canonical score-work ordering."
        )
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
                "priority_version": "1.0.0",
            }
        )

    def overall_key(row: dict[str, str]) -> tuple:
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
    code_now.sort(
        key=lambda row: (
            PRIORITY_ORDER.get(row["work_priority"], 9),
            integer(row["company_work_rank"]),
            integer(row["first_work_rank"]),
            row["company_id"],
        )
    )
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
        read_csv(root / "outputs" / "score_work_queue.csv")
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
