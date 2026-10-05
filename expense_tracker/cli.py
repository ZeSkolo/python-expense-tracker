from pathlib import Path
from .db import ExpenseDatabase
from .validation import clean_category, clean_description, parse_amount, parse_date, parse_month, today_iso


def money(cents: int) -> str:
    return f"₹{cents / 100:,.2f}"


def prompt(label: str, default: str | None = None) -> str:
    suffix = f" [{default}]" if default else ""
    value = input(f"{label}{suffix}: ").strip()
    return value or (default or "")


def add_expense(db: ExpenseDatabase) -> None:
    try:
        amount = parse_amount(prompt("Amount"))
        category = clean_category(prompt("Category"))
        description = clean_description(prompt("Description (optional)"))
        expense_date = parse_date(prompt("Date", today_iso()))
        expense_id = db.add_expense(amount, category, description, expense_date)
        print(f"Added expense #{expense_id}.\n")
    except ValueError as error:
        print(f"Validation error: {error}\n")


def view_expenses(db: ExpenseDatabase) -> None:
    rows = db.list_expenses()
    if not rows:
        print("No expenses recorded.\n")
        return
    print("\nID   Date         Category             Amount       Description")
    print("-" * 78)
    for row in rows:
        print(f"{row['id']:<4} {row['expense_date']:<12} {row['category'][:20]:<20} "
              f"{money(row['amount_cents']):>12}   {row['description']}")
    print()


def delete_expense(db: ExpenseDatabase) -> None:
    try:
        expense_id = int(prompt("Expense ID to delete"))
        print("Deleted.\n" if db.delete_expense(expense_id) else "Expense not found.\n")
    except ValueError:
        print("Expense ID must be an integer.\n")


def monthly_report(db: ExpenseDatabase) -> None:
    rows = db.monthly_totals()
    print("\nMonth     Expenses     Total")
    print("-" * 34)
    for row in rows:
        print(f"{row['month']:<10} {row['expense_count']:>8} {money(row['total_cents']):>14}")
    if not rows:
        print("No expenses recorded.")
    print()


def category_report(db: ExpenseDatabase) -> None:
    try:
        raw = prompt("Month YYYY-MM (leave blank for all)")
        month = parse_month(raw) if raw else None
    except ValueError as error:
        print(f"Validation error: {error}\n")
        return
    rows = db.category_totals(month)
    print("\nCategory                 Expenses        Total")
    print("-" * 49)
    for row in rows:
        print(f"{row['category'][:24]:<24} {row['expense_count']:>8} {money(row['total_cents']):>14}")
    if not rows:
        print("No matching expenses.")
    print()


def run(database_path: str | Path = "expenses.db") -> None:
    actions = {
        "1": ("Add expense", add_expense),
        "2": ("View expenses", view_expenses),
        "3": ("Delete expense", delete_expense),
        "4": ("Monthly totals", monthly_report),
        "5": ("Category totals", category_report),
    }
    with ExpenseDatabase(database_path) as db:
        while True:
            print("=== Python Expense Tracker ===")
            for key, (label, _) in actions.items():
                print(f"{key}. {label}")
            print("0. Exit")
            choice = input("Choose an option: ").strip()
            if choice == "0":
                print("Goodbye!")
                return
            action = actions.get(choice)
            if action:
                action[1](db)
            else:
                print("Invalid option.\n")
