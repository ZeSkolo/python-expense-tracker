import sqlite3
from pathlib import Path
from typing import Optional


class ExpenseDatabase:
    def __init__(self, path: str | Path = "expenses.db") -> None:
        self.path = str(path)
        self.connection = sqlite3.connect(self.path)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA foreign_keys = ON")
        self._create_schema()

    def _create_schema(self) -> None:
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount_cents INTEGER NOT NULL CHECK(amount_cents > 0),
                category TEXT NOT NULL CHECK(length(category) BETWEEN 1 AND 50),
                description TEXT NOT NULL DEFAULT '',
                expense_date TEXT NOT NULL CHECK(length(expense_date) = 10),
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self.connection.execute(
            "CREATE INDEX IF NOT EXISTS idx_expense_date ON expenses(expense_date)"
        )
        self.connection.execute(
            "CREATE INDEX IF NOT EXISTS idx_expense_category ON expenses(category)"
        )
        self.connection.commit()

    def add_expense(self, amount_cents: int, category: str, description: str, expense_date: str) -> int:
        cursor = self.connection.execute(
            "INSERT INTO expenses(amount_cents, category, description, expense_date) VALUES (?, ?, ?, ?)",
            (amount_cents, category, description, expense_date),
        )
        self.connection.commit()
        return int(cursor.lastrowid)

    def list_expenses(self, month: Optional[str] = None, category: Optional[str] = None) -> list[sqlite3.Row]:
        sql = "SELECT id, amount_cents, category, description, expense_date FROM expenses"
        clauses, params = [], []
        if month:
            clauses.append("substr(expense_date, 1, 7) = ?")
            params.append(month)
        if category:
            clauses.append("category = ? COLLATE NOCASE")
            params.append(category)
        if clauses:
            sql += " WHERE " + " AND ".join(clauses)
        sql += " ORDER BY expense_date DESC, id DESC"
        return list(self.connection.execute(sql, params))

    def delete_expense(self, expense_id: int) -> bool:
        cursor = self.connection.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        self.connection.commit()
        return cursor.rowcount == 1

    def monthly_totals(self) -> list[sqlite3.Row]:
        return list(self.connection.execute(
            """SELECT substr(expense_date, 1, 7) AS month,
                      SUM(amount_cents) AS total_cents,
                      COUNT(*) AS expense_count
               FROM expenses GROUP BY month ORDER BY month DESC"""
        ))

    def category_totals(self, month: Optional[str] = None) -> list[sqlite3.Row]:
        if month:
            return list(self.connection.execute(
                """SELECT category, SUM(amount_cents) AS total_cents, COUNT(*) AS expense_count
                   FROM expenses WHERE substr(expense_date, 1, 7) = ?
                   GROUP BY category COLLATE NOCASE ORDER BY total_cents DESC, category""",
                (month,),
            ))
        return list(self.connection.execute(
            """SELECT category, SUM(amount_cents) AS total_cents, COUNT(*) AS expense_count
               FROM expenses GROUP BY category COLLATE NOCASE
               ORDER BY total_cents DESC, category"""
        ))

    def close(self) -> None:
        self.connection.close()

    def __enter__(self) -> "ExpenseDatabase":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
