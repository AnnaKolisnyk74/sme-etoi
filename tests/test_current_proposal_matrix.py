"""Regression checks for the current 100-company research proposal matrix.

These tests check coverage and uncertainty only, not independent approval.
Historical snapshots retain their original terminology and are not rewritten.
"""
import csv
import sys
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from score_companies import SCORE_FIELDS


class CurrentProposalMatrixTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with (ROOT / "data" / "score_coding_proposals.csv").open(
            newline="", encoding="utf-8-sig"
        ) as handle:
            cls.rows = list(csv.DictReader(handle))

    def test_exactly_one_entry_per_field_for_each_company(self):
        by_company = {}
        for row in self.rows:
            by_company.setdefault(row["company_id"], []).append(row["score_field"])
        self.assertEqual(len(by_company), 100)
        self.assertEqual(len(self.rows), 1500)
        expected = set(SCORE_FIELDS)
        self.assertEqual(len(expected), 15)
        for company, fields in by_company.items():
            with self.subTest(company=company):
                self.assertEqual(len(fields), 15)
                self.assertEqual(set(fields), expected)

    def test_unknown_fields_remain_non_numeric(self):
        for row in self.rows:
            with self.subTest(company=row["company_id"], field=row["score_field"]):
                if row["proposal_status"] == "NEEDS_RESEARCH":
                    self.assertEqual(row["proposed_value"], "")
                    self.assertEqual(row["proposal_confidence"], "UNKNOWN")
                    self.assertTrue(row["missing_fact"].strip())
                elif row["proposal_status"] == "CHECKED":
                    self.assertNotEqual(row["proposed_value"], "")
                    self.assertIn(row["proposal_confidence"], {"A", "B", "C"})
                    self.assertFalse(row.get("reviewer", "").strip())
                    self.assertFalse(row.get("review_date", "").strip())
                    self.assertFalse(row.get("review_note", "").strip())
                else:
                    self.fail("Unexpected current proposal status: " + row["proposal_status"])

    def test_current_snapshot_has_no_implicit_approval(self):
        counts = Counter(row["proposal_status"] for row in self.rows)
        self.assertEqual(sum(counts.values()), 1500)
        self.assertEqual(set(counts), {"CHECKED", "NEEDS_RESEARCH"})
        self.assertTrue(all(not row.get("reviewer", "").strip() for row in self.rows))
        self.assertTrue(all(not row.get("review_date", "").strip() for row in self.rows))


if __name__ == "__main__":
    unittest.main()
