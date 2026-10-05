# Python Expense Tracker

A menu-based command-line expense tracker built with Python and SQLite. It stores expenses persistently, validates user input, and generates monthly and category-wise spending reports using SQL aggregation.

## Features

- Add, view, and delete expenses
- Persistent SQLite database
- Date, amount, category, and description validation
- Monthly totals using `SUM` and `GROUP BY`
- Category totals for all time or a selected month
- Money stored as integer cents to avoid floating-point errors
- Parameterized SQL queries and database indexes
- Automated tests for CRUD operations, validation, filters, and reports

## Requirements

- Python 3.10 or newer
- No third-party packages

## Run

```bash
python -m expense_tracker
```

Use another database file:

```bash
python -m expense_tracker --database data/my_expenses.db
```

## Menu

```text
1. Add expense
2. View expenses
3. Delete expense
4. Monthly totals
5. Category totals
0. Exit
```

## Test

```bash
python -m unittest discover -s tests -v
```

## Database schema

| Column | Type | Purpose |
|---|---|---|
| `id` | INTEGER | Auto-incrementing expense ID |
| `amount_cents` | INTEGER | Exact positive amount in cents |
| `category` | TEXT | Normalized spending category |
| `description` | TEXT | Optional expense note |
| `expense_date` | TEXT | ISO date (`YYYY-MM-DD`) |
| `created_at` | TEXT | SQLite creation timestamp |

## Report queries

Monthly and category reports are produced inside SQLite using `SUM(amount_cents)`, `COUNT(*)`, and `GROUP BY`, rather than loading all rows and aggregating them in Python.

## Project structure

```text
expense_tracker/
├── __init__.py
├── __main__.py
├── cli.py
├── db.py
└── validation.py
tests/
└── test_expense_tracker.py
```

## Future improvements

- Edit existing expenses
- CSV import/export
- Budget alerts
- Charts and a desktop/web interface
- Recurring expense support
