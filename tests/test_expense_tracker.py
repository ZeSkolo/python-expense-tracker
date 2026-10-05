import tempfile
import unittest
from pathlib import Path
from expense_tracker.db import ExpenseDatabase
from expense_tracker.validation import clean_category, parse_amount, parse_date, parse_month


class ExpenseTrackerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.db = ExpenseDatabase(Path(self.temp.name) / "test.db")

    def tearDown(self):
        self.db.close()
        self.temp.cleanup()

    def test_add_list_and_delete(self):
        expense_id = self.db.add_expense(12550, "Food", "Lunch", "2026-10-01")
        rows = self.db.list_expenses()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["amount_cents"], 12550)
        self.assertTrue(self.db.delete_expense(expense_id))
        self.assertFalse(self.db.delete_expense(expense_id))
        self.assertEqual(self.db.list_expenses(), [])

    def test_month_and_category_reports(self):
        self.db.add_expense(10000, "Food", "Groceries", "2026-09-02")
        self.db.add_expense(2500, "Food", "Snack", "2026-09-12")
        self.db.add_expense(8000, "Travel", "Bus", "2026-09-15")
        self.db.add_expense(5000, "Travel", "Train", "2026-10-01")
        monthly = {row["month"]: row["total_cents"] for row in self.db.monthly_totals()}
        self.assertEqual(monthly["2026-09"], 20500)
        september = {row["category"]: row["total_cents"] for row in self.db.category_totals("2026-09")}
        self.assertEqual(september, {"Food": 12500, "Travel": 8000})

    def test_filters(self):
        self.db.add_expense(100, "Food", "A", "2026-10-01")
        self.db.add_expense(200, "Travel", "B", "2026-11-01")
        self.assertEqual(len(self.db.list_expenses(month="2026-10")), 1)
        self.assertEqual(len(self.db.list_expenses(category="food")), 1)

    def test_validation(self):
        self.assertEqual(parse_amount("12.345"), 1235)
        self.assertEqual(parse_date("2026-02-28"), "2026-02-28")
        self.assertEqual(parse_month("2026-10"), "2026-10")
        self.assertEqual(clean_category("  Food   and Drinks "), "Food and Drinks")
        for invalid in ("0", "-1", "abc", "NaN"):
            with self.assertRaises(ValueError):
                parse_amount(invalid)
        with self.assertRaises(ValueError):
            parse_date("2026-02-30")


if __name__ == "__main__":
    unittest.main()
