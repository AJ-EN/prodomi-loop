"""Independent acceptance contract for Task A.

This test intentionally lives outside ``src`` so an implementation candidate
cannot treat it as part of its visible test suite. It is the verifier's contract,
not the implementer's definition of done.
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


class TaskACurrencyRulesAcceptanceTest(unittest.TestCase):
    def test_usd_halfway_value_uses_bankers_rounding(self) -> None:
        result = calculate_checkout_total(Decimal("10.225"), "USD")

        self.assertEqual(Decimal("10.22"), result)
        self.assertEqual(-2, result.as_tuple().exponent)

    def test_jpy_uses_zero_minor_units_and_bankers_rounding(self) -> None:
        result = calculate_checkout_total(Decimal("100.5"), "JPY")

        self.assertEqual(Decimal("100"), result)
        self.assertEqual(0, result.as_tuple().exponent)


if __name__ == "__main__":
    unittest.main()
