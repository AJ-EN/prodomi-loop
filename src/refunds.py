"""Plausible baseline candidate for the Task B refund calculation."""

from decimal import Decimal, ROUND_HALF_UP


def calculate_refund_total(amount: Decimal, currency: str) -> Decimal:
    """Return a refund total using the common two-decimal convention."""
    del currency
    return amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
