import argparse
import csv
from pathlib import Path


CONFIDENCE_ORDER = {"A": 0, "B": 1, "C": 2, "UNKNOWN": 3, "": 3}

DEPLOYMENT_FIELDS = {
    "energy_management": "energy_management_deployed",
    "industrial_heat": "industrial_heat_electrification_deployed",
    "heat_recovery": "heat_recovery_deployed",
    "thermal_storage": "thermal_storage_deployed",
    "battery_storage": "battery_storage_deployed",
    "power_quality": "power_quality_solution_deployed",
}


def read_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "company_id",
        "legal_entity",
        "rule_id",
        "opportunity_type",
        "opportunity_level",
        "technical_status",
        "commercial_status",
        "priority",
        "why_now",
        "next_action",
        "confidence",
        "process_id",
        "process_name",
        "reason",
        "company_signal",
        "process_signal",
        "deployment_field",
        "deployment_value",
        "engine_version",
    ]
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def truthy(value):
    return str(value or "").strip().upper() in {"YES", "TRUE", "1", "VALID", "PRESENT"}


def company_signal_present(company, signal):
    if not signal:
        return True
    if signal == "iso_50001_valid":
        return str(company.get("iso_50001_status", "")).strip().upper() == "VALID"
    return truthy(company.get(signal, ""))


def process_signal_present(process, signal):
    if not signal:
        return True
    for field in (
        "drive_relevance",
        "process_heat_relevance",
        "cooling_relevance",
        "schedulability",
        "thermal_inertia_storage",
        "power_electronics_relevance",
        "power_quality_relevance",
    ):
        value = str(process.get(field, "")).strip().upper()
        if signal == f"{value}_{field}":
            return True
    return False


def worst_confidence(*grades):
    normalised = [str(g or "").strip().upper() for g in grades]
    return max(normalised, key=lambda g: CONFIDENCE_ORDER.get(g, 3)) if normalised else "UNKNOWN"


def commercial_status(company, opportunity_type):
    deployment_field = DEPLOYMENT_FIELDS.get(opportunity_type, "")
    if not deployment_field:
        return "RESEARCH_REQUIRED", "", "NOT_MODELLED"

    value = str(company.get(deployment_field, "UNKNOWN") or "UNKNOWN").strip().upper()
    if value == "YES":
        return "ALREADY_DEPLOYED", deployment_field, value
    if value == "NO":
        return "WHITE_SPACE_POSSIBLE", deployment_field, value
    return "RESEARCH_REQUIRED", deployment_field, value


def prioritise(company, opportunity_type, opportunity_level, commercial, confidence):
    if commercial == "ALREADY_DEPLOYED":
        return "LOW", "Relevant technology is already publicly documented as deployed.", "Monitor for expansion, replacement or optimisation signals rather than treating this as greenfield white-space."

    if commercial == "RESEARCH_REQUIRED":
        signals = []
        if truthy(company.get("three_shift_operation")):
            signals.append("three-shift operation")
        if truthy(company.get("multi_shift_or_batch_signal")):
            signals.append("multi-shift or batch production")
        targets = str(company.get("public_targets_summary", "")).strip()
        if targets and "no separate target" not in targets.lower():
            signals.append("public transition target")
        why = ", ".join(signals) if signals else "Technical relevance is visible, but deployment evidence is incomplete."
        next_action = f"Verify whether {opportunity_type.replace('_', ' ')} is already deployed using company reports, project references, vendor cases and recent press releases."
        return "RESEARCH", why, next_action

    score = 0
    if str(opportunity_level).upper() == "HIGH":
        score += 2
    elif str(opportunity_level).upper() == "MEDIUM":
        score += 1
    if str(confidence).upper() in {"A", "B"}:
        score += 1
    if truthy(company.get("three_shift_operation")):
        score += 1
    if truthy(company.get("multi_shift_or_batch_signal")):
        score += 1
    targets = str(company.get("public_targets_summary", "")).strip()
    if targets and "no separate target" not in targets.lower():
        score += 1

    priority = "HIGH" if score >= 5 else "MEDIUM" if score >= 3 else "LOW"
    why_parts = []
    if str(opportunity_level).upper() in {"HIGH", "MEDIUM"}:
        why_parts.append(f"{opportunity_level.upper()} technical relevance")
    if truthy(company.get("three_shift_operation")):
        why_parts.append("three-shift operation")
    if truthy(company.get("multi_shift_or_batch_signal")):
        why_parts.append("multi-shift/batch production")
    if targets and "no separate target" not in targets.lower():
        why_parts.append("public transition target")
    why = "; ".join(why_parts) if why_parts else "Possible white-space with limited urgency signals."
    next_action = f"Validate site-specific need, incumbent solution and decision context for {opportunity_type.replace('_', ' ')} before sales outreach."
    return priority, why, next_action


def generate_opportunities(companies, process_map, processes, rules):
    companies_by_id = {row["company_id"]: row for row in companies}
    processes_by_id = {row["process_id"]: row for row in processes}
    outputs = []

    for mapping in process_map:
        company = companies_by_id.get(mapping.get("company_id"))
        process = processes_by_id.get(mapping.get("process_id"))
        if not company or not process:
            continue

        for rule in rules:
            if str(rule.get("rule_status", "")).upper() not in {"DRAFT", "ACTIVE"}:
                continue
            required_process = rule.get("required_process_signal", "").strip()
            required_company = rule.get("required_company_signal", "").strip()
            blocking_signal = rule.get("blocking_signal", "").strip()

            if not process_signal_present(process, required_process):
                continue
            if not company_signal_present(company, required_company):
                continue
            if blocking_signal and company_signal_present(company, blocking_signal):
                continue

            confidence = worst_confidence(
                rule.get("confidence_cap", "C"),
                company.get("evidence_confidence", "C"),
                mapping.get("confidence", "C"),
            )
            commercial, deployment_field, deployment_value = commercial_status(
                company, rule.get("opportunity_type", "")
            )
            priority, why_now, next_action = prioritise(
                company,
                rule.get("opportunity_type", ""),
                rule.get("output_level", ""),
                commercial,
                confidence,
            )
            outputs.append(
                {
                    "company_id": company["company_id"],
                    "legal_entity": company.get("legal_entity", ""),
                    "rule_id": rule.get("rule_id", ""),
                    "opportunity_type": rule.get("opportunity_type", ""),
                    "opportunity_level": rule.get("output_level", ""),
                    "technical_status": "TECHNICALLY_RELEVANT",
                    "commercial_status": commercial,
                    "priority": priority,
                    "why_now": why_now,
                    "next_action": next_action,
                    "confidence": confidence,
                    "process_id": process.get("process_id", ""),
                    "process_name": process.get("process_name", ""),
                    "reason": rule.get("reason_template", ""),
                    "company_signal": required_company,
                    "process_signal": required_process,
                    "deployment_field": deployment_field,
                    "deployment_value": deployment_value,
                    "engine_version": "0.3.0",
                }
            )

    return sorted(outputs, key=lambda r: (r["company_id"], r["priority"], r["opportunity_type"], r["rule_id"]))


def main():
    parser = argparse.ArgumentParser(description="Generate transparent SME-ETOI technical, commercial and prioritisation signals.")
    parser.add_argument("--companies", default="data/company_intelligence.csv")
    parser.add_argument("--process-map", default="data/company_process_map.csv")
    parser.add_argument("--processes", default="data/process_library.csv")
    parser.add_argument("--rules", default="data/opportunity_rules.csv")
    parser.add_argument("--output", default="outputs/opportunities.csv")
    args = parser.parse_args()

    rows = generate_opportunities(
        read_csv(args.companies),
        read_csv(args.process_map),
        read_csv(args.processes),
        read_csv(args.rules),
    )
    write_csv(args.output, rows)
    print(f"Wrote {len(rows)} opportunity rows to {args.output}")


if __name__ == "__main__":
    main()
