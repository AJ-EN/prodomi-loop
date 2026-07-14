"""Ordinary examples visible to the Task A implementation candidate.

These tests intentionally cover only common USD checkout examples. They show
why a plausible patch can appear correct before the independent acceptance
contract checks currency-specific and half-way boundaries.
"""

from decimal import Decimal
import os
from pathlib import Path
import sys
import unittest


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = Path(os.environ.get("PRODOMI_SOURCE_ROOT", REPOSITORY_ROOT / "src"))
sys.path.insert(0, str(SOURCE_ROOT))

from checkout import calculate_checkout_total  # noqa: E402


class CheckoutVisibleExamplesTest(unittest.TestCase):
    def test_usd_non_boundary_value_rounds_to_cents(self) -> None:
        result = calculate_checkout_total(Decimal("10.234"), "USD")

        self.assertEqual(Decimal("10.23"), result)

    def test_usd_exact_value_keeps_two_minor_units(self) -> None:
        result = calculate_checkout_total(Decimal("7.10"), "USD")

        self.assertEqual(Decimal("7.10"), result)
        self.assertEqual(-2, result.as_tuple().exponent)


if __name__ == "__main__":
    unittest.main()
