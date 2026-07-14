"""Independent holdout acceptance contract for Task B.

Set ``PRODOMI_SOURCE_ROOT`` to the ``src`` directory of the candidate
worktree. Keeping this verifier in the evaluator repository ensures the same
contract is applied to the baseline and capability-assisted candidates.
"""

from decimal import Decimal
import os
from pathlib import Path
import sys
import unittest


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = Path(os.environ.get("PRODOMI_SOURCE_ROOT", REPOSITORY_ROOT / "src"))
sys.path.insert(0, str(SOURCE_ROOT))

from refunds import calculate_refund_total  # noqa: E402


class TaskBRefundRulesAcceptanceTest(unittest.TestCase):
    def test_usd_halfway_refund_uses_bankers_rounding(self) -> None:
        result = calculate_refund_total(Decimal("55.225"), "USD")

        self.assertEqual(Decimal("55.22"), result)
        self.assertEqual(-2, result.as_tuple().exponent)

    def test_jpy_refund_uses_zero_minor_units_and_bankers_rounding(self) -> None:
        result = calculate_refund_total(Decimal("100.5"), "JPY")

        self.assertEqual(Decimal("100"), result)
        self.assertEqual(0, result.as_tuple().exponent)


if __name__ == "__main__":
    unittest.main()
