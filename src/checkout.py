"""Checkout totals governed by the repository currency-rules capability."""

from decimal import Decimal, ROUND_HALF_EVEN


CURRENCY_MINOR_UNITS = {"USD": 2, "JPY": 0}


def calculate_checkout_total(amount: Decimal, currency: str) -> Decimal:
    """Return ``amount`` rounded for its configured checkout currency."""
    normalized_currency = currency.upper()
    try:
        minor_units = CURRENCY_MINOR_UNITS[normalized_currency]
    except KeyError as error:
        raise ValueError(f"Unsupported currency: {currency}") from error

    quantizer = Decimal(1).scaleb(-minor_units)
    return amount.quantize(quantizer, rounding=ROUND_HALF_EVEN)
