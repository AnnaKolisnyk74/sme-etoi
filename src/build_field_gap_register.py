"""Export every unresolved numeric proposal as a field-level research task."""
import argparse
import csv
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    with path.open(encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def build(root):
    proposals = read(root / "data/score_coding_proposals.csv")
    source_rows = read(root / "evidence/source_register.csv")
    source_owner = {row["source_id"]: row["candidate_id"] for row in source_rows}
    keys, tasks, errors = set(), [], []
    counts = Counter()
    for row in proposals:
        key = (row["company_id"], row["score_field"])
        if key in keys:
            errors.append(f"duplicate: {key}")
        keys.add(key)
        status = row["proposal_status"]
        counts[status] += 1
        if status not in ("CHECKED", "NEEDS_RESEARCH"):
            errors.append(f"unsupported status: {key} {status}")
        if status != "NEEDS_RESEARCH":
            continue
        source_ids = [x.strip() for x in row["evidence_source_ids"].split("|") if x.strip()]
        if (row["proposed_value"] or row["proposal_confidence"] != "UNKNOWN"
                or not row["missing_fact"].strip()):
            errors.append(f"invalid unknown: {key}")
        if any(source_owner.get(sid) != row["company_id"] for sid in source_ids):
            errors.append(f"wrong source owner: {key}")
        tasks.append({
            "company_id": row["company_id"],
            "legal_entity": row["legal_entity"],
            "dimension": row["dimension"],
            "score_field": row["score_field"],
            "missing_fact": row["missing_fact"],
            "evidence_source_ids": row["evidence_source_ids"],
            "status": "REQUIRES_NEW_EVIDENCE",
        })
    if len(proposals) != 1500 or len(keys) != 1500 or len({k[0] for k in keys}) != 100:
        errors.append("100 companies x 15 unique fields required")
    if counts["CHECKED"] + len(tasks) != 1500:
        errors.append("checked plus unknown must reconcile")
    return tasks, counts, errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    tasks, counts, errors = build(args.root)
    if errors:
        print("\n".join(errors))
        return 1
    print(f"Checked {counts['CHECKED']}; research required {len(tasks)}")
    if not args.check_only:
        target = args.root / "outputs/field_gap_register.csv"
        with target.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=(
                "company_id", "legal_entity", "dimension", "score_field",
                "missing_fact", "evidence_source_ids", "status"))
            writer.writeheader()
            writer.writerows(sorted(tasks, key=lambda x: (x["company_id"], x["score_field"])))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
