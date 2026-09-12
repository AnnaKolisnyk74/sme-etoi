import argparse
import csv
from pathlib import Path

PRIORITY_SCORE = {"HIGH": 3, "MEDIUM": 2, "RESEARCH": 2, "LOW": 1, "": 0}
CONFIDENCE_SCORE = {"A": 3, "B": 2, "C": 1, "UNKNOWN": 0, "": 0}


def read_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "research_rank",
        "company_id",
        "legal_entity",
        "opportunity_type",
        "missing_fact",
        "research_priority",
        "information_gain_score",
        "why_it_matters",
        "recommended_sources",
        "current_confidence",
        "commercial_status",
        "process_name",
        "engine_version",
    ]
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def missing_fact_for(row):
    deployment_field = (row.get("deployment_field") or "").strip()
    deployment_value = (row.get("deployment_value") or "").strip().upper()
    opportunity_type = (row.get("opportunity_type") or "").strip()

    if deployment_field and deployment_value in {"UNKNOWN", "", "NOT_MODELLED"}:
        return f"Resolve {deployment_field} for {opportunity_type}"
    if not deployment_field:
        return f"Define deployment evidence model for {opportunity_type}"
    return ""


def recommended_sources_for(row):
    opportunity_type = (row.get("opportunity_type") or "").strip()
    base = ["company website", "annual/sustainability report", "recent press releases", "vendor/project references"]
    if opportunity_type == "energy_management":
        base.append("ISO 50001 / EMS references")
    elif opportunity_type == "battery_storage":
        base.extend(["storage project announcements", "PV/BESS integrator references"])
    elif opportunity_type == "flexibility":
        base.extend(["load-management references", "demand-response or flexibility programme mentions"])
    return " | ".join(base)


def information_gain(row):
    # Research is most valuable when technical relevance is already visible,
    # commercial status is unresolved and confidence is not too weak.
    score = 0
    if (row.get("technical_status") or "").upper() == "TECHNICALLY_RELEVANT":
        score += 3
    if (row.get("commercial_status") or "").upper() == "RESEARCH_REQUIRED":
        score += 3
    score += PRIORITY_SCORE.get((row.get("priority") or "").upper(), 0)
    score += CONFIDENCE_SCORE.get((row.get("confidence") or "").upper(), 0)
    if (row.get("deployment_value") or "").upper() in {"UNKNOWN", "NOT_MODELLED", ""}:
        score += 2
    return score


def generate_research_queue(opportunities):
    candidates = []
    for row in opportunities:
        if (row.get("commercial_status") or "").upper() != "RESEARCH_REQUIRED":
            continue
        missing_fact = missing_fact_for(row)
        if not missing_fact:
            continue
        score = information_gain(row)
        candidates.append(
            {
                "company_id": row.get("company_id", ""),
                "legal_entity": row.get("legal_entity", ""),
                "opportunity_type": row.get("opportunity_type", ""),
                "missing_fact": missing_fact,
                "research_priority": "HIGH" if score >= 10 else "MEDIUM" if score >= 8 else "LOW",
                "information_gain_score": str(score),
                "why_it_matters": row.get("why_now", "") or row.get("reason", ""),
                "recommended_sources": recommended_sources_for(row),
                "current_confidence": row.get("confidence", ""),
                "commercial_status": row.get("commercial_status", ""),
                "process_name": row.get("process_name", ""),
                "engine_version": "0.1.0",
            }
        )

    candidates.sort(
        key=lambda r: (-int(r["information_gain_score"]), r["company_id"], r["opportunity_type"])
    )
    for index, row in enumerate(candidates, start=1):
        row["research_rank"] = str(index)
    return candidates


def main():
    parser = argparse.ArgumentParser(description="Build a prioritised research queue from SME-ETOI opportunity outputs.")
    parser.add_argument("--input", default="outputs/opportunities.csv")
    parser.add_argument("--output", default="outputs/research_queue.csv")
    args = parser.parse_args()

    rows = generate_research_queue(read_csv(args.input))
    write_csv(args.output, rows)
    print(f"Wrote {len(rows)} research tasks to {args.output}")


if __name__ == "__main__":
    main()
