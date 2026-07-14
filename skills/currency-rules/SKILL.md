---
name: currency-rules
description: Apply Prodomi Loop's checkout-currency rounding rules when editing monetary calculations.
---

# Currency rules

Use this capability for checkout, refund, and invoice totals in this repository.

## Non-negotiable rules

1. Represent money with `decimal.Decimal`; never construct a monetary value from
   a binary float.
2. Round exactly once, at the output boundary, with `ROUND_HALF_EVEN`
   (banker's rounding).
3. Quantize to the currency's configured minor-unit precision:

   | Currency | Minor units | Quantizer |
   | --- | ---: | --- |
   | USD | 2 | `Decimal("0.01")` |
   | JPY | 0 | `Decimal("1")` |

4. Reject currencies that are not explicitly configured. Do not silently apply
   the USD precision to another currency.

## Implementation checklist

- Normalize the currency code before lookup.
- Derive the quantizer from the minor-unit map instead of hard-coding cents.
- Preserve the required Decimal exponent in the returned amount.
- Verify with the independent contract:

  ```sh
  python3 -m unittest acceptance/test_task_a_currency_rules.py
  ```

## Why this exists

Task A showed that a plausible two-decimal, round-half-up implementation passes
ordinary examples but violates repository policy at currency and half-way
boundaries. This capability makes that previously missing rule reusable.
