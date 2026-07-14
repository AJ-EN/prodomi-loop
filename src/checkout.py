"""Checkout calculation candidate used to demonstrate Task A failure."""

from decimal import Decimal, ROUND_HALF_UP


def calculate_checkout_total(amount: Decimal, currency: str) -> Decimal:
    """Return a display total for a checkout amount.

    This deliberately plausible baseline only handles the common two-decimal
    checkout case. Task A's independent contract exposes the missing rule.
    """
    del currency
    return amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
