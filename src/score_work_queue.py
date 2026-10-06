"""Build the SME-ETOI scoring work queue.

The queue operationalises score readiness without inventing numeric values.
Eligibility gates stay upstream. Scoreable companies are then ordered by
evidence readiness and receive one work package per SME-ETOI dimension.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from score_companies import DIMENSIONS
import score_readiness


ROOT = Path(__file__).resolve().parents[1]

CONFIDENCE_ORDER = {"A": 0, "B": 1, "C": 2, "UNKNOWN": 3, "": 3}

DIMENSION_ORDER = tuple(DIMENSIONS.keys())

DIMENSION_INSTRUCTIONS = {
    "process_electrification_potential": (
        "Code temperature/technology fit, process-electrification maturity and "
        "fossil-heat displacement from explicit process evidence. Use UNKNOWN, "
        "not zero, when the evidence does not support a numeric anchor."
    ),
    "power_electronics_relevance": (
        "Code motor/drive intensity, power-conversion intensity and automation/"
        "control relevance from firm-specific process and equipment evidence."
    ),
    "load_flexibility_potential": (
        "Code scheduling flexibility and thermal-storage flexibility from "
        "documented batch, buffer, refrigeration or operating-pattern evidence."
    ),
    "grid_power_quality_relevance": (
        "Code ordinal incremental-load, power-quality and onsite-integration "
        "relevance only. Do not infer kW, MW, MWh, voltage level or grid cost."
    ),
    "observed_transition_gap": (
        "Code the publicly observed measures, management-system, target and "
        "investment gaps only after the defined evidence checks. Missing public "
        "evidence is not proof of internal absence."
    ),
}

OUTPUT_FIELDS = [
    "work_rank",
    "company_work_rank",
    "task_key",
    "company_id",
    "legal_entity",
    "workstream",
    "task_type",
    "dimension",
    "required_fields",
    "missing_fields",
    "missing_field_count",
    "task_status",
    "work_priority",
    "evidence_confidence",
    "process_confidence",
    "source_count",
    "qa_result",
    "independent_human_review_status",
    "score_status",
    "research_rank",
    "queue_reason",
    "next_action",
    "work_queue_version",
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


def confidence_rank(value: object) -> int:
    return CONFIDENCE_ORDER.get(normalise(value).upper(), 3)


def worst_process_confidence(rows: list[dict[str, str]]) -> str:
    if not rows:
        return "UNKNOWN"
    grades = [normalise(row.get("confidence")).upper() or "UNKNOWN" for row in rows]
    return max(grades, key=confidence_rank)


def coding_priority(evidence_confidence: str, process_confidence: str) -> str:
    worst = max(
        confidence_rank(evidence_confidence),
        confidence_rank(process_confidence),
    )
    if worst == 0:
        return "P1"
    if worst == 1:
        return "P2"
    return "P3"


def missing_fields_for_dimension(
    coded_row: dict[str, str] | None,
    dimension: str,
) -> list[str]:
    fields = list(DIMENSIONS[dimension].keys())
    if not coded_row:
        return fields
    return [field for field in fields if not normalise(coded_row.get(field))]


def generate_score_work_queue(
    companies: list[dict[str, str]],
    readiness_rows: list[dict[str, str]],
    process_map: list[dict[str, str]],
    source_register: list[dict[str, str]],
    qa_review: list[dict[str, str]],
    coded_rows: list[dict[str, str]],
    research_queue_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    company_by_id = {
        normalise(row.get("company_id")): row
        for row in companies
        if normalise(row.get("company_id"))
    }
    readiness_by_id = {
        normalise(row.get("company_id")): row
        for row in readiness_rows
        if normalise(row.get("company_id"))
    }

    process_by_company: dict[str, list[dict[str, str]]] = {}
    for row in process_map:
        process_by_company.setdefault(normalise(row.get("company_id")), []).append(row)

    source_ids_by_company: dict[str, set[str]] = {}
    for row in source_register:
        company_id = normalise(row.get("candidate_id"))
        source_id = normalise(row.get("source_id"))
        if company_id and source_id:
            source_ids_by_company.setdefault(company_id, set()).add(source_id)

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

    eligibility_research_rank: dict[str, str] = {}
    for row in research_queue_rows:
        if normalise(row.get("queue_rule_id")) != "RQ00_SME_ELIGIBILITY_GATE":
            continue
        company_id = normalise(row.get("company_id"))
        rank = normalise(row.get("research_rank"))
        if company_id:
            eligibility_research_rank[company_id] = rank

    active_company_ids = [
        company_id
        for company_id in company_by_id
        if readiness_by_id.get(company_id, {}).get("score_status") != "EXCLUDED"
    ]

    def company_sort_key(company_id: str) -> tuple:
        readiness = readiness_by_id.get(company_id, {})
        status = normalise(readiness.get("score_status"))
        if status == "NOT_SCOREABLE_ELIGIBILITY":
            rank_text = eligibility_research_rank.get(company_id, "")
            rank = int(rank_text) if rank_text.isdigit() else 10**9
            return (0, rank, *natural_company_key(company_id))

        company = company_by_id[company_id]
        process_conf = worst_process_confidence(process_by_company.get(company_id, []))
        evidence_conf = normalise(company.get("evidence_confidence")).upper()
        qa = normalise(qa_by_company.get(company_id, {}).get("qa_result")).upper()
        qa_rank = 0 if qa == "PASS" else 1
        source_count = len(source_ids_by_company.get(company_id, set()))
        return (
            1,
            confidence_rank(evidence_conf),
            confidence_rank(process_conf),
            qa_rank,
            -source_count,
            *natural_company_key(company_id),
        )

    ordered_company_ids = sorted(active_company_ids, key=company_sort_key)
    company_work_rank = {
        company_id: index
        for index, company_id in enumerate(ordered_company_ids, start=1)
    }

    tasks: list[dict[str, str]] = []

    for company_id in ordered_company_ids:
        company = company_by_id[company_id]
        readiness = readiness_by_id.get(company_id, {})
        status = normalise(readiness.get("score_status"))
        process_rows = process_by_company.get(company_id, [])
        process_conf = worst_process_confidence(process_rows)
        evidence_conf = normalise(company.get("evidence_confidence")).upper() or "UNKNOWN"
        qa_row = qa_by_company.get(company_id, {})
        source_count = len(source_ids_by_company.get(company_id, set()))
        common = {
            "company_work_rank": str(company_work_rank[company_id]),
            "company_id": company_id,
            "legal_entity": normalise(company.get("legal_entity")),
            "evidence_confidence": evidence_conf,
            "process_confidence": process_conf,
            "source_count": str(source_count),
            "qa_result": normalise(qa_row.get("qa_result")) or "NOT_RECORDED",
            "independent_human_review_status": normalise(
                readiness.get("independent_human_review_status")
            ),
            "score_status": status,
            "work_queue_version": "1.0.0",
        }

        if status == "NOT_SCOREABLE_ELIGIBILITY":
            tasks.append(
                {
                    **common,
                    "task_key": f"{company_id}|ELIGIBILITY_GATE",
                    "workstream": "ELIGIBILITY",
                    "task_type": "ELIGIBILITY_GATE",
                    "dimension": "",
                    "required_fields": "sme_status | group_check",
                    "missing_fields": "group_check",
                    "missing_field_count": "1",
                    "task_status": "OPEN_GATE",
                    "work_priority": "GATE",
                    "research_rank": eligibility_research_rank.get(company_id, ""),
                    "queue_reason": (
                        "SME/group eligibility is an upstream validity gate. "
                        "Do not spend further scoring effort until it is resolved."
                    ),
                    "next_action": normalise(readiness.get("next_action")),
                }
            )
            continue

        if status == "NOT_SCOREABLE_PROCESS":
            tasks.append(
                {
                    **common,
                    "task_key": f"{company_id}|PROCESS_MAPPING",
                    "workstream": "SCORING_PREREQUISITE",
                    "task_type": "PROCESS_MAPPING",
                    "dimension": "",
                    "required_fields": "company_process_map",
                    "missing_fields": "company_process_map",
                    "missing_field_count": "1",
                    "task_status": "OPEN_PREREQUISITE",
                    "work_priority": "P1",
                    "research_rank": "",
                    "queue_reason": "Firm-specific process evidence is required before numeric scoring.",
                    "next_action": normalise(readiness.get("next_action")),
                }
            )
            continue

        if status == "NOT_SCOREABLE_CERTIFICATES":
            tasks.append(
                {
                    **common,
                    "task_key": f"{company_id}|CERTIFICATE_CHECK",
                    "workstream": "SCORING_PREREQUISITE",
                    "task_type": "CERTIFICATE_CHECK",
                    "dimension": "",
                    "required_fields": "ISO 50001 | ISO 14001 | EMAS",
                    "missing_fields": "pending certificate checks",
                    "missing_field_count": "1",
                    "task_status": "OPEN_PREREQUISITE",
                    "work_priority": "P1",
                    "research_rank": "",
                    "queue_reason": (
                        "Management-gap coding is invalid until all mandatory "
                        "certificate checks are non-pending."
                    ),
                    "next_action": normalise(readiness.get("next_action")),
                }
            )
            continue

        coded_row = coded_by_company.get(company_id)

        if status == "NEEDS_NUMERIC_CODING":
            work_priority = coding_priority(evidence_conf, process_conf)
            for dimension in DIMENSION_ORDER:
                missing = missing_fields_for_dimension(coded_row, dimension)
                if not missing:
                    continue
                required = list(DIMENSIONS[dimension].keys())
                tasks.append(
                    {
                        **common,
                        "task_key": f"{company_id}|{dimension}",
                        "workstream": "NUMERIC_CODING",
                        "task_type": "CODE_DIMENSION",
                        "dimension": dimension,
                        "required_fields": " | ".join(required),
                        "missing_fields": " | ".join(missing),
                        "missing_field_count": str(len(missing)),
                        "task_status": "READY_TO_CODE",
                        "work_priority": work_priority,
                        "research_rank": "",
                        "queue_reason": (
                            "Eligibility, process mapping and certificate gates pass. "
                            "Explicit numeric anchors remain uncoded; higher-evidence "
                            "companies are queued first."
                        ),
                        "next_action": DIMENSION_INSTRUCTIONS[dimension],
                    }
                )
            continue

        if status == "PROVISIONAL_SCORE_ONLY":
            tasks.append(
                {
                    **common,
                    "task_key": f"{company_id}|HUMAN_REVIEW",
                    "workstream": "HUMAN_REVIEW",
                    "task_type": "INDEPENDENT_REVIEW",
                    "dimension": "",
                    "required_fields": "independent_human_review_status",
                    "missing_fields": "independent_human_review_status",
                    "missing_field_count": "1",
                    "task_status": "AWAITING_HUMAN_REVIEW",
                    "work_priority": "P1",
                    "research_rank": "",
                    "queue_reason": (
                        "Numeric coding is complete, but the score cannot be final "
                        "until independent human review is recorded."
                    ),
                    "next_action": normalise(readiness.get("next_action")),
                }
            )
            continue

        if status == "FINAL_SCORE_READY":
            tasks.append(
                {
                    **common,
                    "task_key": f"{company_id}|FINAL_SCORE",
                    "workstream": "FINAL_SCORING",
                    "task_type": "RUN_FINAL_SCORE",
                    "dimension": "",
                    "required_fields": "",
                    "missing_fields": "",
                    "missing_field_count": "0",
                    "task_status": "READY_FOR_FINAL_SCORE",
                    "work_priority": "P1",
                    "research_rank": "",
                    "queue_reason": "All explicit score-readiness gates are complete.",
                    "next_action": normalise(readiness.get("next_action")),
                }
            )

    dimension_index = {dimension: index for index, dimension in enumerate(DIMENSION_ORDER)}
    tasks.sort(
        key=lambda row: (
            int(row["company_work_rank"]),
            0 if row["task_type"] == "ELIGIBILITY_GATE" else 1,
            dimension_index.get(row["dimension"], 99),
            row["task_type"],
        )
    )

    for index, row in enumerate(tasks, start=1):
        row["work_rank"] = str(index)

    return tasks


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def run(root: Path = ROOT, output: Path | None = None) -> list[dict[str, str]]:
    companies = read_csv(root / "data" / "company_intelligence.csv")
    readiness = score_readiness.generate_score_readiness(
        companies,
        read_csv(root / "data" / "company_process_map.csv"),
        read_csv(root / "evidence" / "certificate_register.csv"),
        read_csv(root / "evidence" / "qa_review.csv"),
        read_csv(root / "data" / "pilot_coded.csv"),
        read_csv(root / "outputs" / "pilot_scored.csv"),
    )
    rows = generate_score_work_queue(
        companies,
        readiness,
        read_csv(root / "data" / "company_process_map.csv"),
        read_csv(root / "evidence" / "source_register.csv"),
        read_csv(root / "evidence" / "qa_review.csv"),
        read_csv(root / "data" / "pilot_coded.csv"),
        read_csv(root / "outputs" / "research_queue.csv"),
    )
    write_csv(output or root / "outputs" / "score_work_queue.csv", rows)
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate the ordered SME-ETOI score/coding work queue."
    )
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    rows = run(args.root, args.output)
    counts: dict[str, int] = {}
    for row in rows:
        counts[row["workstream"]] = counts.get(row["workstream"], 0) + 1
    summary = ", ".join(f"{key}={counts[key]}" for key in sorted(counts))
    print(f"Wrote {len(rows)} score-work rows. {summary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
