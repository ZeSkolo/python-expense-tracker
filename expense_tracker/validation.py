from datetime import date, datetime
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP


def parse_amount(value: str) -> int:
    """Validate a positive currency amount and return integer cents."""
    try:
        amount = Decimal(value.strip())
    except (InvalidOperation, AttributeError):
        raise ValueError("Amount must be a valid number.")
    if not amount.is_finite() or amount <= 0:
        raise ValueError("Amount must be greater than zero.")
    amount = amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    if amount > Decimal("999999999.99"):
        raise ValueError("Amount is too large.")
    return int(amount * 100)


def parse_date(value: str) -> str:
    """Validate YYYY-MM-DD and return a normalized ISO date."""
    try:
        return datetime.strptime(value.strip(), "%Y-%m-%d").date().isoformat()
    except (ValueError, AttributeError):
        raise ValueError("Date must use YYYY-MM-DD and be a real calendar date.")


def parse_month(value: str) -> str:
    """Validate YYYY-MM."""
    try:
        return datetime.strptime(value.strip(), "%Y-%m").strftime("%Y-%m")
    except (ValueError, AttributeError):
        raise ValueError("Month must use YYYY-MM.")


def clean_category(value: str) -> str:
    category = " ".join(value.strip().split())
    if not category:
        raise ValueError("Category cannot be empty.")
    if len(category) > 50:
        raise ValueError("Category must be 50 characters or fewer.")
    return category


def clean_description(value: str) -> str:
    description = " ".join(value.strip().split())
    if len(description) > 200:
        raise ValueError("Description must be 200 characters or fewer.")
    return description


def today_iso() -> str:
    return date.today().isoformat()
