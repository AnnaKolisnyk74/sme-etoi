import argparse
import csv
from pathlib import Path


QUEUE_FIELDS = [
    "research_rank",
    "company_id",
    "legal_entity",
    "opportunity_type",
    "technical_status",
    "commercial_status",
    "current_priority",
    "current_confidence",
    "missing_fact",
    "current_value",
    "research_question",
    "research_priority",
    "decision_impact",
    "decision_impact_reason",
    "queue_rule_id",
    "queue_reason",
    "recommended_source_types",
    "evidence_urls",
    "process_name",
    "opportunity_rule_id",
    "task_status",
    "engine_version",
]

PRIORITY_ORDER = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
CONFIDENCE_ORDER = {"A": 0, "B": 1, "C": 2, "UNKNOWN": 3, "": 3}
OPPORTUNITY_LEVEL_ORDER = {"HIGH": 0, "MEDIUM": 1, "LOW": 2, "RESEARCH_REQUIRED": 3, "": 4}

OPPORTUNITY_TERMS = {
    "battery_storage": ("battery", "bess", "storage"),
    "energy_management": ("energy management", "energy monitoring", "iso 50001", "ems"),
    "flexibility": ("flexibility", "load management", "demand response", "peak management"),
    "heat_recovery": ("heat recovery", "waste heat"),
    "industrial_heat": ("heat pump", "electric boiler", "electrification"),
    "thermal_storage": ("thermal storage", "heat storage", "cold storage"),
    "power_quality": ("power quality", "harmonics", "reactive power"),
}


def read_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=QUEUE_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def normalise(value, default=""):
    value = str(value or "").strip()
    return value if value else default


def company_by_id(companies):
    indexed = {}
    for company in companies:
        company_id = normalise(company.get("company_id"))
        if not company_id:
            continue
        if company_id in indexed:
            raise ValueError(f"Duplicate company_id in company intelligence: {company_id}")
        indexed[company_id] = company
    return indexed


def announced_deployment_signal(company, opportunity_type):
    text = " ".join(
        normalise(company.get(field)).lower()
        for field in ("public_investments_summary", "public_targets_summary")
    )
    if not any(marker in text for marker in ("announced", "planned", "commission", "under construction")):
        return False
    return any(term in text for term in OPPORTUNITY_TERMS.get(opportunity_type, ()))


def missing_fact_for(row):
    deployment_field = normalise(row.get("deployment_field"))
    deployment_value = normalise(row.get("deployment_value"), "UNKNOWN").upper()
    opportunity_type = normalise(row.get("opportunity_type"))

    if deployment_field and deployment_value in {"UNKNOWN", "NOT_FOUND_AFTER_CHECK", "NOT_MODELLED"}:
        return deployment_field, deployment_value
    if not deployment_field:
        return f"deployment_evidence_model_for_{opportunity_type}", "NOT_MODELLED"
    return "", deployment_value


def research_question_for(row, company, missing_fact):
    opportunity_type = normalise(row.get("opportunity_type"))
    legal_entity = normalise(company.get("legal_entity"), normalise(row.get("legal_entity")))

    if opportunity_type == "energy_management":
        return (
            f"Does {legal_entity} have a publicly documented operational energy-management or "
            "energy-monitoring system, and is there a currently valid ISO 50001 certificate or direct register record?"
        )
    if opportunity_type == "battery_storage":
        if announced_deployment_signal(company, opportunity_type):
            return (
                f"Was the publicly announced battery-storage project at {legal_entity} commissioned, "
                "and what direct evidence documents its operational status and scope?"
            )
        return f"Is an operational battery-storage system publicly documented for {legal_entity}?"
    if opportunity_type == "flexibility":
        return (
            f"Are load-management, demand-response or documented controllable-load arrangements "
            f"already operating at {legal_entity}?"
        )
    if missing_fact.startswith("deployment_evidence_model_for_"):
        return f"Which public evidence is sufficient to classify deployment for {opportunity_type}?"
    return f"Is {opportunity_type.replace('_', ' ')} publicly documented as deployed at {legal_entity}?"


def recommended_source_types_for(opportunity_type):
    base = [
        "official company project or sustainability page",
        "annual or sustainability report",
        "recent official press release",
        "vendor or project case study",
    ]
    if opportunity_type == "energy_management":
        base.extend(["direct ISO 50001 certificate", "authoritative certificate register"])
    elif opportunity_type == "battery_storage":
        base.extend(["commissioning announcement", "BESS integrator reference"])
    elif opportunity_type == "flexibility":
        base.extend(["load-management reference", "demand-response programme record"])
    return " | ".join(base)


def classify_task(row, company, current_value):
    """Apply the first matching rule; no hidden or aggregate score is used."""
    opportunity_type = normalise(row.get("opportunity_type"))
    opportunity_level = normalise(row.get("opportunity_level")).upper()
    confidence = normalise(row.get("confidence"), "UNKNOWN").upper()
    deployment_field = normalise(row.get("deployment_field"))

    if announced_deployment_signal(company, opportunity_type):
        return {
            "queue_rule_id": "RQ01_ANNOUNCED_DEPLOYMENT_CHECK",
            "research_priority": "HIGH",
            "decision_impact": "HIGH",
            "queue_reason": (
                "A dated public deployment signal exists, but operational status is unresolved; "
                "checking commissioning is the next time-sensitive fact check."
            ),
            "decision_impact_reason": (
                "Confirmation can change the commercial status from RESEARCH_REQUIRED to "
                "ALREADY_DEPLOYED; no result leaves the value UNKNOWN."
            ),
        }

    if not deployment_field or current_value == "NOT_MODELLED":
        return {
            "queue_rule_id": "RQ02_EVIDENCE_MODEL_REQUIRED",
            "research_priority": "MEDIUM",
            "decision_impact": "MEDIUM",
            "queue_reason": (
                "The opportunity engine has no complete deployment-evidence mapping for this case, "
                "so the evidence model must be made explicit before company status can change."
            ),
            "decision_impact_reason": (
                "The result enables a later commercial classification but does not itself establish "
                "deployment or white space."
            ),
        }

    if opportunity_level == "HIGH" and confidence in {"A", "B"}:
        return {
            "queue_rule_id": "RQ03_HIGH_RELEVANCE_DEPLOYMENT_CHECK",
            "research_priority": "HIGH",
            "decision_impact": "HIGH",
            "queue_reason": (
                "Technical relevance is HIGH, evidence confidence is A or B, and the mapped deployment "
                "fact remains unresolved."
            ),
            "decision_impact_reason": (
                "Direct deployment evidence can change the commercial status and therefore the next "
                "research or business-development action."
            ),
        }

    if opportunity_level in {"HIGH", "MEDIUM"}:
        return {
            "queue_rule_id": "RQ04_RELEVANT_DEPLOYMENT_CHECK",
            "research_priority": "MEDIUM",
            "decision_impact": "HIGH",
            "queue_reason": (
                "Technical relevance is visible, but either its level or the evidence confidence does "
                "not meet the high-priority rule."
            ),
            "decision_impact_reason": (
                "Direct deployment evidence can still change the commercial status, while technical "
                "importance determines when the research should be performed."
            ),
        }

    return {
        "queue_rule_id": "RQ05_PROVISIONAL_DEPLOYMENT_CHECK",
        "research_priority": "LOW",
        "decision_impact": "MEDIUM",
        "queue_reason": (
            "The opportunity itself is provisional or research-required, so deployment research follows "
            "better-supported technical cases."
        ),
        "decision_impact_reason": (
            "The fact may refine the case, but further technical evidence is also needed before a strong "
            "decision can be supported."
        ),
    }


def preferred_opportunity_row(row):
    return (
        OPPORTUNITY_LEVEL_ORDER.get(normalise(row.get("opportunity_level")).upper(), 5),
        CONFIDENCE_ORDER.get(normalise(row.get("confidence")).upper(), 3),
        normalise(row.get("rule_id")),
    )


def generate_research_queue(companies, opportunities):
    companies_by_id = company_by_id(companies)
    candidates_by_key = {}

    for row in opportunities:
        if normalise(row.get("commercial_status")).upper() != "RESEARCH_REQUIRED":
            continue
        company_id = normalise(row.get("company_id"))
        company = companies_by_id.get(company_id)
        if not company:
            continue
        missing_fact, current_value = missing_fact_for(row)
        if not missing_fact:
            continue

        key = (company_id, normalise(row.get("opportunity_type")), missing_fact)
        current = candidates_by_key.get(key)
        if current is None or preferred_opportunity_row(row) < preferred_opportunity_row(current):
            candidates_by_key[key] = row

    candidates = []
    for (company_id, opportunity_type, missing_fact), row in candidates_by_key.items():
        company = companies_by_id[company_id]
        _, current_value = missing_fact_for(row)
        classification = classify_task(row, company, current_value)
        candidates.append(
            {
                "company_id": company_id,
                "legal_entity": normalise(company.get("legal_entity"), normalise(row.get("legal_entity"))),
                "opportunity_type": opportunity_type,
                "technical_status": normalise(row.get("technical_status"), "UNKNOWN"),
                "commercial_status": normalise(row.get("commercial_status"), "UNKNOWN"),
                "current_priority": normalise(row.get("priority"), "UNKNOWN"),
                "current_confidence": normalise(row.get("confidence"), "UNKNOWN"),
                "missing_fact": missing_fact,
                "current_value": current_value,
                "research_question": research_question_for(row, company, missing_fact),
                "research_priority": classification["research_priority"],
                "decision_impact": classification["decision_impact"],
                "decision_impact_reason": classification["decision_impact_reason"],
                "queue_rule_id": classification["queue_rule_id"],
                "queue_reason": classification["queue_reason"],
                "recommended_source_types": recommended_source_types_for(opportunity_type),
                "evidence_urls": normalise(company.get("source_urls")),
                "process_name": normalise(row.get("process_name")),
                "opportunity_rule_id": normalise(row.get("rule_id")),
                "task_status": "OPEN",
                "engine_version": "0.2.0",
            }
        )

    candidates.sort(
        key=lambda task: (
            PRIORITY_ORDER[task["research_priority"]],
            PRIORITY_ORDER[task["decision_impact"]],
            task["company_id"],
            task["opportunity_type"],
            task["missing_fact"],
        )
    )
    for index, row in enumerate(candidates, start=1):
        row["research_rank"] = str(index)
    return candidates


def main():
    parser = argparse.ArgumentParser(
        description="Build an explainable research queue from SME-ETOI company and opportunity intelligence."
    )
    parser.add_argument("--companies", default="data/company_intelligence.csv")
    parser.add_argument("--opportunities", default="outputs/opportunities.csv")
    parser.add_argument("--output", default="outputs/research_queue.csv")
    args = parser.parse_args()

    rows = generate_research_queue(read_csv(args.companies), read_csv(args.opportunities))
    write_csv(args.output, rows)
    print(f"Wrote {len(rows)} research tasks to {args.output}")


if __name__ == "__main__":
    main()
