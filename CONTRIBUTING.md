# Contributing to Prodomi Loop

Prodomi Loop is intentionally narrow. Contributions should strengthen the
evidence-backed capability-promotion loop rather than turn the repository into
a general agent platform.

## Before opening a change

Open an issue describing:

- the concrete failure the change addresses;
- the independent acceptance contract;
- the fresh holdout task;
- the before/after evidence required for promotion.

Bug fixes and documentation improvements may use a smaller scope, but must
still include a reproducible verification command.

## Development checks

Use Python 3.10 or newer. The MVP has no third-party runtime dependencies.

```sh
python3 -m unittest discover -s tests -p 'test_*.py'
python3 -m unittest discover -s acceptance -p 'test_*.py'
python3 scripts/replay_loop.py
python3 scripts/smoke_review_hub.py
```

For changes to the complete demo path, also run:

```sh
python3 scripts/rehearse.py --runs 3 --max-seconds 90
```

## Pull-request contract

A pull request should include:

1. a concise problem statement;
2. the implementation or capability diff;
3. the exact verification commands and output;
4. before/after holdout evidence when capability behavior changes;
5. confirmation that implementation and acceptance authority remain separate.

Do not include secrets, personal data, generated dependency folders, or claims
that the model learned or improved unless the evidence supports that claim.

## Scope boundaries

Changes are in scope when they improve one of these properties:

- deterministic replay;
- acceptance-test independence;
- clean-worktree isolation;
- evidence preservation;
- human promotion decisions;
- transfer to an additional repository-specific rule.

Generic orchestration, dashboards, deployment infrastructure, and autonomous
merging are out of scope until the core proof works across multiple controlled
domains.

## License

By submitting a contribution, you agree that it may be licensed under the
[Apache License 2.0](LICENSE), as described in Section 5 of that license.
