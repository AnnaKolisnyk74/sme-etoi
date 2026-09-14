import copy
import csv
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from build_double_code_package import OUTPUT_FIELDS, build_manifest
from inter_rater_reliability import (
    FIELDS,
    analyze,
    canonical_values,
    cohens_kappa,
    normalize_process_ids,
    read_csv,
    validate_review,
)


class InterRaterReliabilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.companies = read_csv(ROOT / "data/company_intelligence.csv")
        cls.process_rows = read_csv(ROOT / "data/company_process_map.csv")
        cls.reviews = read_csv(ROOT / "data/pilot_double_code.csv")
        cls.canonical = canonical_values(cls.companies, cls.process_rows)
        with (ROOT / "data/process_library.csv").open(
            newline="", encoding="utf-8-sig"
        ) as handle:
            cls.known_process_ids = {
                row["process_id"] for row in csv.DictReader(handle)
            }

    def test_pending_template_covers_exactly_current_sample(self):
        self.assertEqual(len(self.reviews), 100)
        self.assertEqual(
            {row["company_id"] for row in self.reviews}, set(self.canonical)
        )
        self.assertEqual(
            validate_review(self.reviews, self.canonical, self.known_process_ids),
            [],
        )

    def test_neutral_source_manifest_has_no_prior_coding_fields(self):
        rows = build_manifest(ROOT)
        self.assertEqual({row["company_id"] for row in rows}, set(self.canonical))
        self.assertEqual(tuple(rows[0]), OUTPUT_FIELDS)
        self.assertNotIn("evidence_fact", rows[0])
        self.assertNotIn("review_status", rows[0])

    def test_kappa_is_calculated_from_field_specific_marginals(self):
        pairs = [("A", "A"), ("A", "B"), ("B", "B"), ("B", "B")]
        self.assertEqual(cohens_kappa(pairs), "0.5000")
        self.assertEqual(cohens_kappa([("A", "A")]), "UNKNOWN")
        self.assertEqual(
            cohens_kappa([("A", "A"), ("A", "A")]),
            "NOT_DEFINED_SINGLE_CATEGORY",
        )

    def test_analysis_creates_a_conflict_without_changing_canonical_data(self):
        company_id = "P03"
        review = {
            "company_id": company_id,
            "reviewer": "Independent reviewer",
            "review_date": "2026-09-14",
            "review_status": "COMPLETE",
        }
        review.update(self.canonical[company_id])
        review["evidence_confidence"] = "C"
        results, conflicts = analyze([review], self.canonical)
        self.assertEqual(len(conflicts), 1)
        self.assertEqual(conflicts[0]["field"], "evidence_confidence")
        self.assertEqual(self.canonical[company_id]["evidence_confidence"], "B")
        evidence_result = next(
            row for row in results if row["field"] == "evidence_confidence"
        )
        self.assertEqual(evidence_result["disagreements"], "1")

    def test_completed_review_requires_reviewer_date_sources_and_all_fields(self):
        reviews = copy.deepcopy(self.reviews)
        first = reviews[0]
        first["review_status"] = "COMPLETE"
        for field in FIELDS:
            first[field] = self.canonical[first["company_id"]][field]
        first["source_ids_checked"] = "S-P03-01"
        errors = validate_review(reviews, self.canonical, self.known_process_ids)
        self.assertIn("completed review missing reviewer for P03", errors)
        self.assertIn("completed review missing review_date for P03", errors)

    def test_process_id_order_does_not_create_false_disagreement(self):
        self.assertEqual(normalize_process_ids("PR004|PR003"), "PR003|PR004")


if __name__ == "__main__":
    unittest.main()
