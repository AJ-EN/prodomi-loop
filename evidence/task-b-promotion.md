# Task B capability-promotion evidence

## Decision

**PROMOTE** - 2026-07-14T06:36:06Z

The `currency-rules` capability is promoted because the related refund holdout
improved under the same independent acceptance contract.

## Independent verifier

`acceptance/test_task_b_refund_rules.py` remained in the evaluator repository.
Each candidate was selected only through `PRODOMI_SOURCE_ROOT`, so the test was
outside both candidate worktrees.

## Before: pre-capability baseline

- Base worktree commit: `d2ac3b5` - before `skills/currency-rules/SKILL.md`
  existed.
- Candidate commit: `f0de375` - plausible two-decimal, round-half-up refund
  implementation.
- Result: **FAIL, 2/2 checks failed**.
- Evidence: `evidence/task-b-baseline.log`.

The baseline returned `55.23` for USD `55.225` and `100.50` for JPY `100.5`.
Both violate the independent contract.

## After: capability-assisted candidate

- Base worktree commit: `cfe2ecc` - includes the promoted candidate
  `skills/currency-rules/SKILL.md` and its Task A-validated checkout policy.
- Candidate commit: `5b4b8e8` - refund implementation delegates to the
  configured checkout currency policy.
- Result: **PASS, 2/2 checks passed**.
- Evidence: `evidence/task-b-assisted.log`.

## Promotion rationale

The result is a true related-task holdout: refund logic is separate from the
Task A checkout implementation, while both tasks require the same previously
missing domain rule. The passing candidate uses the reusable currency policy;
the baseline did not have that capability available. The capability therefore
met the promotion rule in `tasks/task-b.md`.
