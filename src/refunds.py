"""Refund totals implemented with the repository currency-rules capability."""

from decimal import Decimal

from checkout import calculate_checkout_total


def calculate_refund_total(amount: Decimal, currency: str) -> Decimal:
    """Return a refund total using the same configured currency policy as checkout."""
    return calculate_checkout_total(amount, currency)
