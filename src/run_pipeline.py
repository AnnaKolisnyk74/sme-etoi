"""Run the SME-ETOI research pipeline as one deterministic workflow."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import export_web_data
import inter_rater_reliability
import opportunity_engine
import research_queue
import score_readiness
import score_work_queue
import validate_pilot
import validate_score_coding_proposals


ROOT = Path(__file__).resolve().parents[1]


def read_csv(root: Path, relative_path: str) -> list[dict[str, str]]:
    with (root / relative_path).open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def build_outputs(
    root: Path = ROOT,
) -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
    companies = read_csv(root, "data/company_intelligence.csv")
    process_map = read_csv(root, "data/company_process_map.csv")
    processes = read_csv(root, "data/process_library.csv")
    rules = read_csv(root, "data/opportunity_rules.csv")
    research_results_path = root / "data/research_results.csv"
    research_results = (
        read_csv(root, "data/research_results.csv")
        if research_results_path.exists()
        else []
    )

    opportunities = opportunity_engine.generate_opportunities(
        companies,
        process_map,
        processes,
        rules,
    )
    queue = research_queue.generate_research_queue(
        companies,
        opportunities,
        research_results,
    )
    return companies, opportunities, queue


def validate_generated_outputs(
    companies: list[dict[str, str]],
    opportunities: list[dict[str, str]],
    queue: list[dict[str, str]],
) -> list[str]:
    errors: list[str] = []
    company_ids = {row["company_id"] for row in companies}
    opportunity_company_ids = {row["company_id"] for row in opportunities}

    if opportunity_company_ids != company_ids:
        missing = sorted(company_ids - opportunity_company_ids)
        unexpected = sorted(opportunity_company_ids - company_ids)
        errors.append(
            "opportunity coverage differs from canonical sample: "
            f"missing={missing}, unexpected={unexpected}"
        )

    expected_eligibility_ids = {
        row["company_id"]
        for row in companies
        if str(row.get("group_check", "")).strip().lower()
        in research_queue.UNRESOLVED_GROUP_CHECKS
    }
    eligibility_tasks = [
        row for row in queue if row.get("queue_rule_id") == "RQ00_SME_ELIGIBILITY_GATE"
    ]
    eligibility_ids = {row["company_id"] for row in eligibility_tasks}

    if eligibility_ids != expected_eligibility_ids:
        missing = sorted(expected_eligibility_ids - eligibility_ids)
        unexpected = sorted(eligibility_ids - expected_eligibility_ids)
        errors.append(
            "eligibility gates differ from unresolved group checks: "
            f"missing={missing}, unexpected={unexpected}"
        )

    ranked_queue = sorted(queue, key=lambda row: int(row["research_rank"]))
    first_tasks = ranked_queue[: len(expected_eligibility_ids)]
    if any(
        row.get("queue_rule_id") != "RQ00_SME_ELIGIBILITY_GATE"
        for row in first_tasks
    ):
        errors.append("SME eligibility gates do not occupy the first queue ranks")

    for row in opportunities:
        if row["company_id"] in expected_eligibility_ids:
            if row.get("sample_eligibility_status") != "ELIGIBILITY_PENDING":
                errors.append(
                    f"{row['company_id']} opportunity is missing ELIGIBILITY_PENDING"
                )
            if row.get("actionability_status") != "ELIGIBILITY_BLOCKED":
                errors.append(
                    f"{row['company_id']} opportunity is not eligibility-blocked"
                )
        if (
            str(row.get("deployment_value", "")).upper()
            in {"UNKNOWN", "NOT_FOUND_AFTER_CHECK", "NOT_MODELLED"}
            and row.get("commercial_status") == "WHITE_SPACE_POSSIBLE"
        ):
            errors.append(
                f"{row['company_id']} {row['opportunity_type']} converts uncertainty to white space"
            )

    return errors



def build_score_readiness(
    root: Path,
    companies: list[dict[str, str]],
) -> list[dict[str, str]]:
    return score_readiness.generate_score_readiness(
        companies,
        read_csv(root, "data/company_process_map.csv"),
        read_csv(root, "evidence/certificate_register.csv"),
        read_csv(root, "evidence/qa_review.csv"),
        read_csv(root, "data/pilot_coded.csv"),
        read_csv(root, "outputs/pilot_scored.csv"),
    )



def build_score_work_queue(
    root: Path,
    companies: list[dict[str, str]],
    readiness: list[dict[str, str]],
    research_tasks: list[dict[str, str]],
) -> list[dict[str, str]]:
    return score_work_queue.generate_score_work_queue(
        companies,
        readiness,
        read_csv(root, "data/company_process_map.csv"),
        read_csv(root, "evidence/source_register.csv"),
        read_csv(root, "evidence/qa_review.csv"),
        read_csv(root, "data/pilot_coded.csv"),
        research_tasks,
        read_csv(root, "data/score_coding_proposals.csv"),
    )


def validate_score_work_queue(
    readiness: list[dict[str, str]],
    work_queue: list[dict[str, str]],
) -> list[str]:
    errors: list[str] = []
    ranks = [int(row["work_rank"]) for row in work_queue]
    if ranks != list(range(1, len(work_queue) + 1)):
        errors.append("score-work queue ranks are not dense and ordered")

    task_keys = [row["task_key"] for row in work_queue]
    if len(task_keys) != len(set(task_keys)):
        errors.append("score-work queue contains duplicate task keys")

    blocked_ids = {
        row["company_id"]
        for row in readiness
        if row.get("score_status") == "NOT_SCOREABLE_ELIGIBILITY"
    }
    gate_rows = [
        row for row in work_queue if row.get("workstream") == "ELIGIBILITY"
    ]
    gate_ids = {row["company_id"] for row in gate_rows}
    if gate_ids != blocked_ids:
        errors.append("score-work eligibility gates differ from score-readiness blocks")

    if any(
        row.get("workstream") != "ELIGIBILITY"
        for row in work_queue[: len(blocked_ids)]
    ):
        errors.append("score-work eligibility gates do not occupy the first ranks")

    coding_ids = {
        row["company_id"]
        for row in work_queue
        if row.get("workstream") == "NUMERIC_CODING"
    }
    expected_coding_ids = {
        row["company_id"]
        for row in readiness
        if row.get("score_status") == "NEEDS_NUMERIC_CODING"
    }
    if coding_ids != expected_coding_ids:
        errors.append("score-work numeric-coding coverage differs from score readiness")

    if blocked_ids & coding_ids:
        errors.append("eligibility-blocked companies received numeric coding tasks")

    allowed_numeric_statuses = {
        "READY_TO_CODE",
        "IN_PROGRESS",
        "RESEARCH_NEEDED",
        "REWORK_REQUIRED",
        "AWAITING_HUMAN_REVIEW",
        "AWAITING_CANONICAL_UPDATE",
    }
    for row in work_queue:
        if row.get("workstream") == "NUMERIC_CODING":
            if int(row.get("missing_field_count", "0")) <= 0:
                errors.append(
                    f"{row['task_key']} is a numeric-coding task without missing fields"
                )
            if row.get("task_status") not in allowed_numeric_statuses:
                errors.append(
                    f"{row['task_key']} has invalid numeric-coding task status "
                    f"{row.get('task_status')}"
                )
            if (
                row.get("task_status") == "RESEARCH_NEEDED"
                and not row.get("research_gap_fields")
            ):
                errors.append(
                    f"{row['task_key']} requires research but has no research_gap_fields"
                )
            if (
                row.get("task_status") == "AWAITING_HUMAN_REVIEW"
                and not row.get("proposal_covered_fields")
            ):
                errors.append(
                    f"{row['task_key']} awaits review but has no proposal coverage"
                )

    return errors


def validate_score_readiness(
    companies: list[dict[str, str]],
    readiness: list[dict[str, str]],
) -> list[str]:
    errors: list[str] = []
    company_ids = {row["company_id"] for row in companies}
    readiness_ids = {row["company_id"] for row in readiness}

    if readiness_ids != company_ids:
        missing = sorted(company_ids - readiness_ids)
        unexpected = sorted(readiness_ids - company_ids)
        errors.append(
            "score readiness differs from canonical sample: "
            f"missing={missing}, unexpected={unexpected}"
        )

    unresolved_ids = {
        row["company_id"]
        for row in companies
        if str(row.get("group_check", "")).strip().lower()
        in score_readiness.UNRESOLVED_GROUP_CHECKS
    }
    blocked_ids = {
        row["company_id"]
        for row in readiness
        if row.get("score_status") == "NOT_SCOREABLE_ELIGIBILITY"
    }
    if unresolved_ids != blocked_ids:
        errors.append(
            "unresolved SME/group cases do not match score-readiness eligibility blocks"
        )

    for row in readiness:
        if row.get("score_status") == "FINAL_SCORE_READY":
            if row.get("certificate_check_status") != "COMPLETE":
                errors.append(
                    f"{row['company_id']} is FINAL_SCORE_READY with incomplete certificate checks"
                )
            if row.get("numeric_coding_status") != "COMPLETE":
                errors.append(
                    f"{row['company_id']} is FINAL_SCORE_READY without complete numeric coding"
                )
            if row.get("independent_human_review_status") not in score_readiness.HUMAN_REVIEW_COMPLETE:
                errors.append(
                    f"{row['company_id']} is FINAL_SCORE_READY without completed independent human review"
                )

    return errors


def pipeline_summary(
    companies: list[dict[str, str]],
    opportunities: list[dict[str, str]],
    queue: list[dict[str, str]],
    readiness: list[dict[str, str]] | None = None,
    score_work: list[dict[str, str]] | None = None,
    conflict_count: int | None = None,
) -> dict[str, int | None]:
    return {
        "companies": len(companies),
        "opportunities": len(opportunities),
        "research_tasks": len(queue),
        "eligibility_gates": sum(
            row.get("queue_rule_id") == "RQ00_SME_ELIGIBILITY_GATE"
            for row in queue
        ),
        "eligibility_blocked_opportunities": sum(
            row.get("actionability_status") == "ELIGIBILITY_BLOCKED"
            for row in opportunities
        ),
        "score_readiness_rows": len(readiness or []),
        "final_score_ready": sum(
            row.get("score_status") == "FINAL_SCORE_READY"
            for row in (readiness or [])
        ),
        "score_work_tasks": len(score_work or []),
        "numeric_coding_tasks": sum(
            row.get("workstream") == "NUMERIC_CODING"
            for row in (score_work or [])
        ),
        "double_code_conflicts": conflict_count,
    }


def run_pipeline(
    root: Path = ROOT,
    *,
    write_outputs: bool = True,
    include_reliability: bool = True,
) -> dict[str, int | None]:
    preflight_errors = validate_pilot.validate(root)
    proposal_errors = validate_score_coding_proposals.validate(root)
    preflight_errors.extend(
        f"score coding proposal: {error}" for error in proposal_errors
    )
    if preflight_errors:
        raise ValueError("Preflight QA failed: " + "; ".join(preflight_errors))

    companies, opportunities, queue = build_outputs(root)
    readiness = build_score_readiness(root, companies)
    score_work = build_score_work_queue(root, companies, readiness, queue)
    generated_errors = validate_generated_outputs(companies, opportunities, queue)
    generated_errors.extend(validate_score_readiness(companies, readiness))
    generated_errors.extend(validate_score_work_queue(readiness, score_work))
    if generated_errors:
        raise ValueError("Generated-output QA failed: " + "; ".join(generated_errors))

    conflict_count: int | None = None
    if write_outputs:
        opportunity_engine.write_csv(root / "outputs/opportunities.csv", opportunities)
        research_queue.write_csv(root / "outputs/research_queue.csv", queue)
        score_readiness.write_csv(root / "outputs/score_readiness.csv", readiness)
        score_work_queue.write_csv(root / "outputs/score_work_queue.csv", score_work)
        if include_reliability:
            _, conflicts = inter_rater_reliability.run(root)
            conflict_count = len(conflicts)
        web_payload = export_web_data.build_web_payload(root)
        export_web_data.write_web_payload(
            root / "web" / "data" / "sme_etoi.json",
            web_payload,
        )

    return pipeline_summary(
        companies,
        opportunities,
        queue,
        readiness=readiness,
        score_work=score_work,
        conflict_count=conflict_count,
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Run SME-ETOI preflight QA, opportunity generation, research-queue "
            "generation and cross-output validation as one workflow."
        )
    )
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Validate and build outputs in memory without writing generated files.",
    )
    parser.add_argument(
        "--skip-reliability",
        action="store_true",
        help="Skip inter-rater reliability output generation.",
    )
    args = parser.parse_args()

    try:
        summary = run_pipeline(
            args.root,
            write_outputs=not args.check_only,
            include_reliability=not args.skip_reliability,
        )
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1

    mode = "check-only" if args.check_only else "write"
    print(
        "SME-ETOI pipeline passed "
        f"({mode}): {summary['companies']} companies, "
        f"{summary['opportunities']} opportunities, "
        f"{summary['research_tasks']} research tasks, "
        f"{summary['eligibility_gates']} eligibility gates, "
        f"{summary['eligibility_blocked_opportunities']} eligibility-blocked opportunity rows, "
        f"{summary['score_readiness_rows']} score-readiness rows, "
        f"{summary['final_score_ready']} final-score-ready companies, "
        f"{summary['score_work_tasks']} score-work tasks, "
        f"{summary['numeric_coding_tasks']} numeric-coding tasks."
    )
    if summary["double_code_conflicts"] is not None:
        print(f"Open double-code conflicts: {summary['double_code_conflicts']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
