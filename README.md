# Prodomi Loop

> Coding agents do not fail because they cannot write plausible code. They fail
> because repositories do not teach them the rules they are missing.

Prodomi Loop turns a failed coding task into a small, reviewable repository
capability and promotes it only after that capability improves a fresh related
task.

This MVP is a controlled currency-regression scenario, deliberately scoped for
a deterministic 90-second demo. It uses real Git worktrees, repository-local
guidance, an independent acceptance contract, and stored test evidence.

GitHub Actions independently runs the acceptance contracts and clean-worktree
replay on every push or pull request targeting `main`.

## The demonstrated loop

| Stage | Evidence |
| --- | --- |
| Task A failure | A plausible checkout candidate used two-decimal, round-half-up rounding and failed its independent currency contract. |
| Diagnosis | The missing capability was a domain/specification rule: banker’s rounding plus currency-specific minor units. |
| Capability | [`skills/currency-rules/SKILL.md`](skills/currency-rules/SKILL.md) encodes the reusable rule. |
| Task B holdout | A pre-capability refund candidate failed 2/2 checks; the capability-assisted candidate passed 2/2 under the same external contract. |
| Decision | The evidence satisfies the promotion rule in [`evidence/task-b-promotion.md`](evidence/task-b-promotion.md). |

## Verify the proof

Run every independent acceptance check:

```sh
python3 -m unittest discover -s acceptance -p 'test_*.py'
```

Expected result: `Ran 4 tests ... OK`.

Replay the complete failure-to-promotion proof with temporary real Git
worktrees:

```sh
python3 scripts/replay_loop.py
```

Expected sequence: visible Task A examples pass, Task A's independent contract
fails for the pre-capability candidate, Task B's baseline fails, and the
capability-assisted Task B passes. The command exits nonzero if this evidence
does not hold.

The preserved Task B before/after logs are:

- [`evidence/task-b-baseline.log`](evidence/task-b-baseline.log) - baseline failed 2/2.
- [`evidence/task-b-assisted.log`](evidence/task-b-assisted.log) - capability-assisted candidate passed 2/2.

## Live Review Hub

The no-dependency local application runs the real worktree replay, streams the
verifier evidence into the browser, and unlocks Promote/Reject only after the
fresh holdout improves.

```sh
python3 review-hub/server.py
```

Open `http://127.0.0.1:8000` and click `RUN LIVE PROOF`.

For the exact 90-second narration, preflight commands, and terminal fallback,
use [`docs/demo-runbook.md`](docs/demo-runbook.md).

The first-principles competitive positioning behind this interaction is in
[`docs/winning-demo-strategy.md`](docs/winning-demo-strategy.md).

## Scope boundaries

This is not a generic agent dashboard, autonomous deployment system, or model
weight-learning claim. The MVP proves one narrow proposition: a repository
capability is valuable only after it improves a fresh related task under an
independent acceptance contract.
