# Task B - Refund currency rounding holdout

## Status

Completed. The capability-assisted clean-worktree candidate passed the
independent contract after the pre-capability baseline failed. See
`evidence/task-b-promotion.md`.

## Objective

Implement a refund-total calculation for the same supported currencies as Task
A. This task is intentionally related but is not a re-run of checkout code.

## Independent contract

The verifier checks a USD half-way boundary and a JPY zero-minor-unit boundary.
It runs from `acceptance/` and receives a candidate worktree's `src` directory
through `PRODOMI_SOURCE_ROOT`; the test does not live in either candidate
worktree.

## Comparison protocol

1. Run a plausible two-decimal, round-half-up refund candidate in a clean
   worktree created from the pre-capability commit.
2. Run a fresh refund candidate in another clean worktree created from the
   currency-rules capability commit.
3. Use the same independent contract for both runs.
4. Promote only if the capability-assisted candidate passes and the baseline
   candidate fails.

## Decision rule

`PROMOTE` requires the recorded baseline failure, the passing holdout result,
and a reviewable capability diff. A Task A pass alone is not enough.
