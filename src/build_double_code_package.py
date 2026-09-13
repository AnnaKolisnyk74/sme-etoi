"""Build a neutral source manifest for independent pilot double-coding."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_FIELDS = (
    "company_id",
    "legal_entity",
    "source_id",
    "source_type",
    "publisher",
    "document_title",
    "reporting_period",
    "publication_date",
    "source_url",
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def build_manifest(root: Path = ROOT) -> list[dict[str, str]]:
    companies = read_csv(root / "data/company_intelligence.csv")
    sources = read_csv(root / "evidence/source_register.csv")
    company_by_id = {row["company_id"]: row for row in companies}
    rows: list[dict[str, str]] = []
    for source in sources:
        company_id = source["candidate_id"]
        if company_id not in company_by_id:
            continue
        rows.append(
            {
                "company_id": company_id,
                "legal_entity": company_by_id[company_id]["legal_entity"],
                "source_id": source["source_id"],
                "source_type": source["source_type"],
                "publisher": source["publisher"],
                "document_title": source["document_title"],
                "reporting_period": source["reporting_period"],
                "publication_date": source["publication_date"],
                "source_url": source["source_link"],
            }
        )
    return sorted(rows, key=lambda row: (row["company_id"], row["source_id"]))


def write_manifest(root: Path = ROOT) -> list[dict[str, str]]:
    rows = build_manifest(root)
    output_path = root / "data/pilot_review_sources.csv"
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    return rows


def main() -> int:
    rows = write_manifest()
    companies = len({row["company_id"] for row in rows})
    print(f"Wrote {len(rows)} neutral source rows for {companies} pilot companies.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
