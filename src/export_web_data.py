"""Export public SME-ETOI repository data for the static web prototype."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path
import source_audit_summary
import proposal_checks
import decision_research
from score_companies import SCORE_FIELDS


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


def compact_source(row: dict[str, str], audit: dict | None = None, recheck: dict | None = None) -> dict[str, str]:
    audit = audit or {}
    recheck = recheck or {}
    return {
        "source_id": normalise(row.get("source_id")),
        "source_type": normalise(row.get("source_type")),
        "publisher": normalise(row.get("publisher")),
        "document_title": normalise(row.get("document_title")),
        "final_url": normalise(row.get("final_url") or row.get("source_link")),
        "evidence_fact": normalise(row.get("evidence_fact")),
        "review_status": normalise(row.get("review_status")),
        "source_link": normalise(row.get("source_link")),
        "link_check_status": normalise(row.get("link_check_status")),
        "link_check_date": normalise(row.get("link_check_date")),
        "retrieval_status": normalise(audit.get("retrieval_status") or 'NOT_CHECKED'),
        "retrieval_checked_at": normalise(audit.get("checked_at")),
        "content_review_status": normalise(recheck.get("content_review_status")),
        "content_checked_at": normalise(recheck.get("checked_at")),
        "content_scope_note": normalise(recheck.get("scope_note")),
    }


def priority_evidence(row: dict[str, str]) -> dict:
    return {
        "source_count": numeric_or_none(row.get("source_count")),
        "verified_source_count": numeric_or_none(row.get("verified_source_count")),
        "unassessed_field_count": numeric_or_none(row.get("unassessed_field_count")),
        **{field: normalise(row.get(field)) for field in (
            "qa_result", "source_coverage", "coverage_source_ids",
            "evidence_confidence", "process_confidence",
            "expected_information_gain", "information_gain_basis", "priority_version",
        )},
    }


def coding_batch_history(selections, proposals, priority_rows):
    """Show frozen workflow decisions and live field states, without score sums."""
    by_company = {r['company_id']: r for r in priority_rows}
    field_states = {}
    for proposal in proposals:
        field_states.setdefault(proposal['company_id'], Counter())[proposal['proposal_status']] += 1
    groups = {}
    for selection in selections:
        groups.setdefault(selection['batch_id'], []).append(selection)
    batches = []
    for batch_id, rows in groups.items():
        batches.append({
            'batch_id': batch_id,
            'selected_date': rows[0]['selected_date'],
            'companies': [{
                'company_id': r['company_id'], 'legal_entity': r['legal_entity'],
                'selection_rank': numeric_or_none(r['selection_rank']),
                'priority_version': r['priority_version'],
                'expected_information_gain_at_selection': r['expected_information_gain'],
                'source_coverage_at_selection': r['source_coverage'],
                'coverage_source_ids_at_selection': r['coverage_source_ids'],
                'priority_reason_at_selection': r['priority_reason'],
                'current_workflow_action': by_company.get(r['company_id'], {}).get('workflow_action', 'UNKNOWN'),
                'awaiting_human_review_fields': field_states.get(r['company_id'], {}).get('AWAITING_HUMAN_REVIEW', 0),
                'checked_fields': field_states.get(r['company_id'], {}).get('CHECKED', 0),
                'needs_research_fields': field_states.get(r['company_id'], {}).get('NEEDS_RESEARCH', 0),
            } for r in sorted(rows, key=lambda r: int(r['selection_rank']))],
        })
    return sorted(batches, key=lambda b: (b['selected_date'], b['batch_id']))


def field_assessment_summary(companies, proposals, priority_rows):
    """Count unique assessed fields; documentary coverage is not score approval."""
    expected = set(SCORE_FIELDS)
    priority = {r['company_id']: r for r in priority_rows}
    groups = {}
    for row in proposals:
        groups.setdefault(row['company_id'], {}).setdefault(row['score_field'], []).append(row)
    result = []
    for company in companies:
        cid = company['company_id']
        fields = groups.get(cid, {})
        assessed = [rows[0] for field, rows in fields.items()
                    if field in expected and len(rows) == 1
                    and rows[0]['proposal_status'] in
                    {'NEEDS_RESEARCH', 'AWAITING_HUMAN_REVIEW', 'CHECKED', 'APPROVED'}]
        states = Counter(r['proposal_status'] for r in assessed)
        result.append({
            'company_id': cid, 'legal_entity': company['legal_entity'],
            'assessed_field_count': len(assessed), 'expected_field_count': len(expected),
            'complete_first_pass': len(assessed) == len(expected),
            'awaiting_human_review_fields': states['AWAITING_HUMAN_REVIEW'],
            'checked_fields': states['CHECKED'],
            'needs_research_fields': states['NEEDS_RESEARCH'],
            'approved_fields': states['APPROVED'],
            'eligibility_gate_open': priority.get(cid, {}).get('workflow_action') == 'ELIGIBILITY_FIRST',
        })
    return {
        'company_count': len(result),
        'complete_company_count': sum(r['complete_first_pass'] for r in result),
        'expected_field_count': len(result) * len(expected),
        'assessed_field_count': sum(r['assessed_field_count'] for r in result),
        'awaiting_human_review_fields': sum(r['awaiting_human_review_fields'] for r in result),
        'checked_fields': sum(r['checked_fields'] for r in result),
        'needs_research_fields': sum(r['needs_research_fields'] for r in result),
        'approved_fields': sum(r['approved_fields'] for r in result),
        'eligibility_gate_company_count': sum(r['eligibility_gate_open'] for r in result),
        'companies': result,
    }


def build_web_payload(root: Path = ROOT) -> dict:
    companies = read_csv(root, "data/company_intelligence.csv")
    decision_profiles = {p['company_id']: p for p in decision_research.profiles(root)}
    proposals = read_csv(root, "data/score_coding_proposals.csv")
    proposals_by_company = {}
    for proposal in proposals:
        proposals_by_company.setdefault(proposal['company_id'], []).append(proposal)
    candidates = read_csv(root, "data/pilot_candidates.csv")
    process_map = read_csv(root, "data/company_process_map.csv")
    process_library = read_csv(root, "data/process_library.csv")
    opportunities = read_csv(root, "outputs/opportunities.csv")
    pilot_scores = read_csv(root, "outputs/pilot_scored.csv")
    score_readiness = read_csv(root, "outputs/score_readiness.csv")
    score_work_queue = read_csv(root, "outputs/score_work_queue.csv")
    company_work_priority = read_csv(root, "outputs/company_work_priority.csv")
    research_queue = read_csv(root, "outputs/research_queue.csv")
    sources = read_csv(root, "evidence/source_register.csv")
    source_rechecks = {r['source_id']: r for r in read_csv(root, "evidence/proposal_source_checks.csv")}
    source_rechecks.update(decision_research.source_checks(root))
    certificates_by_company = {}
    for row in read_csv(root, "evidence/certificate_register.csv"):
        certificates_by_company.setdefault(row['candidate_id'], []).append(row)
    audits = {r['url']: r for r in read_csv(root, 'evidence/source_link_audit.csv')}
    audit_summary = source_audit_summary.build(root)
    audit_by_company = {r['company_id']: r for r in audit_summary['companies']}

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

    company_priority_by_id = {
        row["company_id"]: row
        for row in company_work_priority
        if row.get("company_id")
    }

    sources_by_company: dict[str, list[dict[str, str]]] = {}
    for row in sources:
        sources_by_company.setdefault(row["candidate_id"], []).append(row)

    web_companies: list[dict] = []
    for company in sorted(companies, key=lambda row: row["legal_entity"].lower()):
        company_id = company["company_id"]
        candidate = candidate_by_id.get(company_id, {})
        score = score_by_id.get(company_id, {})
        readiness = readiness_by_id.get(company_id, {})
        company_priority = company_priority_by_id.get(company_id, {})
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
                "proposal_covered_fields": normalise(row.get("proposal_covered_fields")),
                "research_gap_fields": normalise(row.get("research_gap_fields")),
                "proposal_status_summary": normalise(row.get("proposal_status_summary")),
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
                "certificate_checks": [{key: normalise(row.get(key)) for key in (
                    "standard", "certificate_status", "certificate_holder",
                    "certificate_number", "valid_from", "valid_until", "issuer",
                    "direct_certificate_url", "certificate_index_url", "checked_date", "notes",
                )} for row in certificates_by_company.get(company_id, [])],
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
                "score_proposals": [{
                    "score_field": p['score_field'],
                    "proposed_value": numeric_or_none(p['proposed_value']),
                    "proposal_status": p['proposal_status'],
                    "proposal_confidence": p['proposal_confidence'],
                    "evidence_source_ids": p['evidence_source_ids'],
                    "evidence_basis": p['evidence_basis'],
                    "missing_fact": p['missing_fact'],
                } for p in proposals_by_company.get(company_id, [])],
                "workflow_priority": {
                    **priority_evidence(company_priority),
                    "company_rank": numeric_or_none(company_priority.get("company_rank")),
                    "coding_rank": numeric_or_none(company_priority.get("coding_rank")),
                    "workflow_action": normalise(company_priority.get("workflow_action")),
                    "is_next_to_code": normalise(company_priority.get("is_next_to_code")),
                    "first_work_rank": numeric_or_none(company_priority.get("first_work_rank")),
                    "ready_to_code_tasks": numeric_or_none(company_priority.get("ready_to_code_tasks")),
                    "research_needed_tasks": numeric_or_none(company_priority.get("research_needed_tasks")),
                    "awaiting_human_review_tasks": numeric_or_none(company_priority.get("awaiting_human_review_tasks")),
                    "checked_tasks": numeric_or_none(company_priority.get("checked_tasks")),
                    "open_gate_tasks": numeric_or_none(company_priority.get("open_gate_tasks")),
                    "work_priority": normalise(company_priority.get("work_priority")),
                    "next_action": normalise(company_priority.get("next_action")),
                    "priority_reason": normalise(company_priority.get("priority_reason")),
                },
                "sources": [
                    compact_source(source, audits.get(source['source_link']), source_rechecks.get(source['source_id']))
                    for source in sources_by_company.get(company_id, [])
                ],
                "source_audit": audit_by_company.get(company_id, {}),
                "decision_research_profile": decision_profiles.get(company_id),
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
    score_work_status_counts = Counter(
        normalise(row.get("task_status")) or "UNKNOWN"
        for row in score_work_queue
    )

    company_work_action_counts = Counter(
        normalise(row.get("workflow_action")) or "UNKNOWN"
        for row in company_work_priority
    )
    next_best_company = next(
        (
            row
            for row in company_work_priority
            if normalise(row.get("is_next_to_code")) == "YES"
        ),
        {},
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
        "field_assessment_summary": field_assessment_summary(companies, proposals, company_work_priority),
        "proposal_check_summary": proposal_checks.summary(root),
        "decision_research_summary": decision_research.summary(root),
        "eligibility_coding_selections": read_csv(root, "data/eligibility_coding_selections.csv"),
        "source_audit_summary": audit_summary,
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
            "code_now_company_count": sum(
                normalise(row.get("workflow_action")) == "CODE_NOW"
                for row in company_work_priority
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
            "task_status_counts": dict(sorted(score_work_status_counts.items())),
            "task_count": len(score_work_queue),
        },
        "company_work_summary": {
            "workflow_action_counts": dict(sorted(company_work_action_counts.items())),
            "company_count": len(company_work_priority),
            "next_best_company": {
                **priority_evidence(next_best_company),
                "company_id": normalise(next_best_company.get("company_id")),
                "legal_entity": normalise(next_best_company.get("legal_entity")),
                "coding_rank": numeric_or_none(next_best_company.get("coding_rank")),
                "work_priority": normalise(next_best_company.get("work_priority")),
                "evidence_confidence": normalise(next_best_company.get("evidence_confidence")),
                "process_confidence": normalise(next_best_company.get("process_confidence")),
                "source_count": numeric_or_none(next_best_company.get("source_count")),
                "next_action": normalise(next_best_company.get("next_action")),
                "priority_reason": normalise(next_best_company.get("priority_reason")),
            },
        },
        "coding_batches": coding_batch_history(
            read_csv(root, "data/coding_batch_selections.csv"),
            proposals, company_work_priority,
        ),
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
