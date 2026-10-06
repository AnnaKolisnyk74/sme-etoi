"""Export public SME-ETOI repository data for the static web prototype."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_csv(root: Path, relative_path: str) -> list[dict[str, str]]:
    path = root / relative_path
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def normalise(value: object) -> str:
    return str(value or "").strip()


def numeric_or_none(value: object):
    text = normalise(value)
    if not text:
        return None
    try:
        number = float(text)
    except ValueError:
        return text
    return int(number) if number.is_integer() else number


def compact_source(row: dict[str, str]) -> dict[str, str]:
    return {
        "source_id": normalise(row.get("source_id")),
        "source_type": normalise(row.get("source_type")),
        "publisher": normalise(row.get("publisher")),
        "document_title": normalise(row.get("document_title")),
        "final_url": normalise(row.get("final_url") or row.get("source_link")),
        "evidence_fact": normalise(row.get("evidence_fact")),
        "review_status": normalise(row.get("review_status")),
    }


def build_web_payload(root: Path = ROOT) -> dict:
    companies = read_csv(root, "data/company_intelligence.csv")
    candidates = read_csv(root, "data/pilot_candidates.csv")
    process_map = read_csv(root, "data/company_process_map.csv")
    process_library = read_csv(root, "data/process_library.csv")
    opportunities = read_csv(root, "outputs/opportunities.csv")
    pilot_scores = read_csv(root, "outputs/pilot_scored.csv")
    score_readiness = read_csv(root, "outputs/score_readiness.csv")
    score_work_queue = read_csv(root, "outputs/score_work_queue.csv")
    research_queue = read_csv(root, "outputs/research_queue.csv")
    sources = read_csv(root, "evidence/source_register.csv")

    score_by_id = {
        row["company_id"]: row
        for row in pilot_scores
        if row.get("company_id")
    }
    readiness_by_id = {
        row["company_id"]: row
        for row in score_readiness
        if row.get("company_id")
    }
    candidate_by_id = {
        row["candidate_id"]: row
        for row in candidates
        if row.get("candidate_id")
    }
    process_by_id = {
        row["process_id"]: row
        for row in process_library
        if row.get("process_id")
    }

    mappings_by_company: dict[str, list[dict[str, str]]] = {}
    for row in process_map:
        mappings_by_company.setdefault(row["company_id"], []).append(row)

    opportunities_by_company: dict[str, list[dict[str, str]]] = {}
    for row in opportunities:
        opportunities_by_company.setdefault(row["company_id"], []).append(row)

    queue_by_company: dict[str, list[dict[str, str]]] = {}
    for row in research_queue:
        queue_by_company.setdefault(row["company_id"], []).append(row)

    score_work_by_company: dict[str, list[dict[str, str]]] = {}
    for row in score_work_queue:
        score_work_by_company.setdefault(row["company_id"], []).append(row)

    sources_by_company: dict[str, list[dict[str, str]]] = {}
    for row in sources:
        sources_by_company.setdefault(row["candidate_id"], []).append(row)

    web_companies: list[dict] = []
    for company in sorted(companies, key=lambda row: row["legal_entity"].lower()):
        company_id = company["company_id"]
        candidate = candidate_by_id.get(company_id, {})
        score = score_by_id.get(company_id, {})
        readiness = readiness_by_id.get(company_id, {})
        mappings = mappings_by_company.get(company_id, [])

        processes = []
        for mapping in mappings:
            generic = process_by_id.get(mapping.get("process_id", ""), {})
            processes.append(
                {
                    "process_id": normalise(mapping.get("process_id")),
                    "process_name": normalise(generic.get("process_name")),
                    "process_family": normalise(generic.get("process_family")),
                    "process_name_raw": normalise(mapping.get("process_name_raw")),
                    "confidence": normalise(mapping.get("confidence")),
                    "evidence_url": normalise(mapping.get("process_evidence_url")),
                }
            )

        company_opportunities = sorted(
            opportunities_by_company.get(company_id, []),
            key=lambda row: (
                normalise(row.get("opportunity_type")),
                normalise(row.get("rule_id")),
            ),
        )
        web_opportunities = [
            {
                "rule_id": normalise(row.get("rule_id")),
                "opportunity_type": normalise(row.get("opportunity_type")),
                "opportunity_level": normalise(row.get("opportunity_level")),
                "technical_status": normalise(row.get("technical_status")),
                "commercial_status": normalise(row.get("commercial_status")),
                "priority": normalise(row.get("priority")),
                "confidence": normalise(row.get("confidence")),
                "actionability_status": normalise(row.get("actionability_status")),
                "sample_eligibility_status": normalise(row.get("sample_eligibility_status")),
                "eligibility_next_action": normalise(row.get("eligibility_next_action")),
                "why_now": normalise(row.get("why_now")),
                "next_action": normalise(row.get("next_action")),
                "process_name": normalise(row.get("process_name")),
                "deployment_value": normalise(row.get("deployment_value")),
            }
            for row in company_opportunities
        ]

        company_tasks = sorted(
            queue_by_company.get(company_id, []),
            key=lambda row: int(normalise(row.get("research_rank")) or 999999),
        )
        web_tasks = [
            {
                "research_rank": numeric_or_none(row.get("research_rank")),
                "opportunity_type": normalise(row.get("opportunity_type")),
                "missing_fact": normalise(row.get("missing_fact")),
                "research_priority": normalise(row.get("research_priority")),
                "decision_impact": normalise(row.get("decision_impact")),
                "task_status": normalise(row.get("task_status")),
                "research_question": normalise(row.get("research_question")),
                "queue_reason": normalise(row.get("queue_reason")),
                "last_research_status": normalise(row.get("last_research_status")),
                "last_resulting_value": normalise(row.get("last_resulting_value")),
                "last_finding": normalise(row.get("last_finding")),
            }
            for row in company_tasks
        ]
        company_score_work = sorted(
            score_work_by_company.get(company_id, []),
            key=lambda row: int(normalise(row.get("work_rank")) or 999999),
        )
        web_score_work = [
            {
                "work_rank": numeric_or_none(row.get("work_rank")),
                "company_work_rank": numeric_or_none(row.get("company_work_rank")),
                "task_key": normalise(row.get("task_key")),
                "workstream": normalise(row.get("workstream")),
                "task_type": normalise(row.get("task_type")),
                "dimension": normalise(row.get("dimension")),
                "required_fields": normalise(row.get("required_fields")),
                "missing_fields": normalise(row.get("missing_fields")),
                "missing_field_count": numeric_or_none(row.get("missing_field_count")),
                "task_status": normalise(row.get("task_status")),
                "work_priority": normalise(row.get("work_priority")),
                "evidence_confidence": normalise(row.get("evidence_confidence")),
                "process_confidence": normalise(row.get("process_confidence")),
                "source_count": numeric_or_none(row.get("source_count")),
                "research_rank": numeric_or_none(row.get("research_rank")),
                "queue_reason": normalise(row.get("queue_reason")),
                "next_action": normalise(row.get("next_action")),
            }
            for row in company_score_work
        ]


        web_companies.append(
            {
                "company_id": company_id,
                "legal_entity": normalise(company.get("legal_entity")),
                "website": normalise(company.get("website")),
                "city": normalise(company.get("city")),
                "state": normalise(company.get("state")),
                "nace_code": normalise(company.get("nace_code")),
                "nace_label": normalise(company.get("nace_label")),
                "employees": numeric_or_none(company.get("employees")),
                "revenue_eur_m": numeric_or_none(company.get("revenue_eur_m")),
                "balance_sheet_eur_m": numeric_or_none(company.get("balance_sheet_eur_m")),
                "sme_status": normalise(company.get("sme_status")),
                "group_check": normalise(company.get("group_check")),
                "candidate_eligibility_status": normalise(candidate.get("eligibility_status")),
                "opportunity_score": numeric_or_none(score.get("opportunity_score")),
                "opportunity_band": normalise(score.get("opportunity_band")),
                "score_confidence_grade": normalise(score.get("confidence_grade")),
                "score_classification_status": normalise(score.get("classification_status")),
                "score_readiness": {
                    "score_status": normalise(readiness.get("score_status")),
                    "eligibility_gate": normalise(readiness.get("eligibility_gate")),
                    "process_mapping_status": normalise(readiness.get("process_mapping_status")),
                    "certificate_check_status": normalise(readiness.get("certificate_check_status")),
                    "numeric_coding_status": normalise(readiness.get("numeric_coding_status")),
                    "independent_human_review_status": normalise(readiness.get("independent_human_review_status")),
                    "existing_score_status": normalise(readiness.get("existing_score_status")),
                    "blocking_reasons": normalise(readiness.get("blocking_reasons")),
                    "next_action": normalise(readiness.get("next_action")),
                },
                "process_stratum": normalise(candidate.get("process_stratum")),
                "evidence_confidence": normalise(company.get("evidence_confidence")),
                "review_status": normalise(company.get("review_status")),
                "last_verified_date": normalise(company.get("last_verified_date")),
                "next_review_date": normalise(company.get("next_review_date")),
                "certifications": {
                    "iso_50001": normalise(company.get("iso_50001_status")),
                    "iso_14001": normalise(company.get("iso_14001_status")),
                    "emas": normalise(company.get("emas_status")),
                },
                "public_signals": {
                    "three_shift_operation": normalise(company.get("three_shift_operation")),
                    "pv_present": normalise(company.get("pv_present")),
                    "public_fossil_heat_signal": normalise(company.get("public_fossil_heat_signal")),
                    "refrigeration_or_compressor_signal": normalise(
                        company.get("refrigeration_or_compressor_signal")
                    ),
                    "rectifier_converter_furnace_signal": normalise(
                        company.get("rectifier_converter_furnace_signal")
                    ),
                    "public_targets_summary": normalise(company.get("public_targets_summary")),
                    "public_investments_summary": normalise(company.get("public_investments_summary")),
                },
                "processes": processes,
                "opportunities": web_opportunities,
                "research_tasks": web_tasks,
                "score_work_tasks": web_score_work,
                "sources": [
                    compact_source(source)
                    for source in sources_by_company.get(company_id, [])
                ],
            }
        )

    opportunity_type_counts = Counter(
        row.get("opportunity_type", "") for row in opportunities if row.get("opportunity_type")
    )
    opportunity_types = [
        {"opportunity_type": name, "count": count}
        for name, count in sorted(
            opportunity_type_counts.items(),
            key=lambda item: (-item[1], item[0]),
        )
    ]

    task_status_counts = Counter(
        normalise(row.get("task_status")) or "OPEN"
        for row in research_queue
    )
    priority_counts = Counter(
        normalise(row.get("research_priority")) or "UNKNOWN"
        for row in research_queue
    )

    score_status_counts = Counter(
        normalise(row.get("score_status")) or "UNKNOWN"
        for row in score_readiness
    )

    score_workstream_counts = Counter(
        normalise(row.get("workstream")) or "UNKNOWN"
        for row in score_work_queue
    )
    score_work_priority_counts = Counter(
        normalise(row.get("work_priority")) or "UNKNOWN"
        for row in score_work_queue
    )

    verified_dates = [
        normalise(row.get("last_verified_date"))
        for row in companies
        if normalise(row.get("last_verified_date"))
    ]
    eligibility_gate_count = sum(
        normalise(row.get("queue_rule_id")) == "RQ00_SME_ELIGIBILITY_GATE"
        for row in research_queue
    )
    eligibility_blocked_companies = {
        row["company_id"]
        for row in opportunities
        if normalise(row.get("actionability_status")) == "ELIGIBILITY_BLOCKED"
    }

    return {
        "meta": {
            "project": "SME-ETOI",
            "subtitle": "Energy Transition Opportunity Index for German SMEs",
            "source_snapshot_date": max(verified_dates) if verified_dates else "",
            "company_count": len(web_companies),
            "opportunity_count": len(opportunities),
            "research_task_count": len(research_queue),
            "score_work_task_count": len(score_work_queue),
            "numeric_coding_task_count": sum(
                normalise(row.get("workstream")) == "NUMERIC_CODING"
                for row in score_work_queue
            ),
            "eligibility_gate_count": eligibility_gate_count,
            "eligibility_blocked_company_count": len(eligibility_blocked_companies),
            "data_scope": "Public repository evidence only",
        },
        "opportunity_types": opportunity_types,
        "research_summary": {
            "task_status_counts": dict(sorted(task_status_counts.items())),
            "priority_counts": dict(sorted(priority_counts.items())),
        },
        "score_readiness_summary": dict(sorted(score_status_counts.items())),
        "score_work_summary": {
            "workstream_counts": dict(sorted(score_workstream_counts.items())),
            "priority_counts": dict(sorted(score_work_priority_counts.items())),
            "task_count": len(score_work_queue),
        },
        "companies": web_companies,
    }


def write_web_payload(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Export current public SME-ETOI outputs for the static web prototype."
    )
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "web" / "data" / "sme_etoi.json",
    )
    args = parser.parse_args()

    payload = build_web_payload(args.root)
    write_web_payload(args.output, payload)
    print(
        f"Wrote web payload: {payload['meta']['company_count']} companies, "
        f"{payload['meta']['opportunity_count']} opportunities, "
        f"{payload['meta']['research_task_count']} research tasks -> {args.output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
