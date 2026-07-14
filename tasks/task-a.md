# Task A - Checkout currency rounding

## Status

Planned baseline failure scenario.

## Objective

Implement the checkout total calculation so it respects both of these rules:

1. Monetary values use banker’s rounding (round half to even).
2. The result uses the configured currency’s minor-unit precision.

## Intended failure

The first candidate should plausibly fix the visible examples while still failing
an independent boundary-case acceptance check. The expected diagnosis is a
missing domain rule / specification gap: the repository has not made its
currency-rounding policy explicit or enforceable.

The visible examples are deliberately incomplete ordinary USD cases in
`tests/test_checkout_visible.py`. They must pass for the baseline candidate;
the independent contract is the authority for half-way and currency-specific
boundaries.

## Acceptance contract

The eventual focused acceptance test must be independent from the initial
candidate’s visible tests and must cover:

- a half-way rounding boundary that distinguishes banker’s rounding from
  round-half-up;
- a currency-specific minor-unit rule;
- deterministic money representation, without floating-point ambiguity.

## Required loop evidence

1. Create the first candidate in an isolated Git worktree.
2. Record the independent acceptance failure.
3. Produce a small `currency-rules` repository capability and a regression test.
4. In a fresh worktree, run related Task B both without and with the capability.
5. Promote only if the capability-assisted Task B passes its independent check.

## Out of scope

Tax engines, exchange-rate conversion, payment-provider integration, multiple
applications, and general-purpose currency support.
