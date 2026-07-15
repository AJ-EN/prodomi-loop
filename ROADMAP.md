# Prodomi Loop roadmap

The next milestone is not a larger dashboard. It is stronger evidence that the
promotion mechanism transfers beyond the prepared currency example.

## v0.1 - Reproducible proof

- [x] Detect a false-positive Task A result with an independent contract.
- [x] Encode the missing currency policy as a repository-local capability.
- [x] Compare baseline and capability-assisted Task B in clean Git worktrees.
- [x] Preserve evidence and require an explicit human promotion decision.
- [x] Replay the proof through CI and a minimal Review Hub.

## v0.2 - Cross-domain validation

- [ ] Add two controlled domains with different capability types.
- [ ] Define a manifest for tasks, capabilities, verifiers, and evidence.
- [ ] Run each capability against both positive and negative holdouts.
- [ ] Measure transfer success, regression rate, and verifier disagreement.
- [ ] Publish reproducible experiment results, including failed promotions.

Candidate domains should expose genuinely different repository gaps, such as a
timezone boundary rule, an authorization invariant, or an API compatibility
contract. Adding more currency examples alone would not establish transfer.

## v0.3 - Real repository pilot

- [ ] Pilot the loop on at least three external repositories.
- [ ] Import a real issue and preserve the original failure evidence.
- [ ] Support capability rejection, supersession, and rollback.
- [ ] Add provenance and tamper-evident promotion records.
- [ ] Document maintainer time saved and repeated-failure reduction.

## Research questions

1. What is the smallest useful capability unit: rule, test, tool, or workflow?
2. How far may a holdout task differ before transfer evidence becomes weak?
3. How do we detect overfitted capabilities that pass one holdout?
4. When should a capability be repository-local versus shared across projects?
5. What evidence should be mandatory before an automated system may propose a
   promotion?

## Non-goals for the next milestone

- model fine-tuning or weight-learning claims;
- a generic multi-agent framework;
- autonomous merging or deployment;
- enterprise dashboards;
- broad platform work before cross-domain evidence exists.
