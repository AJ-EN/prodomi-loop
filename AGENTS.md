# Prodomi Loop

## Product focus

Build one deterministic, Codex-native capability-promotion loop. It must turn a
concrete failed coding task into a small repository capability, prove that the
capability improves a fresh related task, and let a human promote or reject it.

## MVP boundaries

- One prepared TypeScript or Python repository.
- One domain: checkout currency calculations.
- Two related tasks: Task A exposes the missing rule; Task B is the holdout.
- One capability type: a repository-local currency-rules skill plus focused
  regression tests.
- Real Git worktrees, diffs, commands, and deterministic test output.

Do not add generic agent orchestration, production deployment, multi-repository
support, model-learning claims, or dashboard features before the full proof
works.

## Evidence rules

- Keep implementation and acceptance decisions separate.
- Store the focused acceptance contract outside the initial candidate path.
- A visible test suite passing is not sufficient evidence of correctness.
- Promote a capability only after a clean-worktree holdout task improves with it.
- Preserve before/after logs and the capability diff for the demo.

## Demo invariant

The core story must remain legible without narration:

`Task A failure -> diagnosis -> candidate capability -> Task B holdout improves -> PROMOTE`

