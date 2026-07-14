# Winning demo strategy

## The uncomfortable competitive fact

“Self-improving agents” is not a sufficient novelty claim. Prior Codex
hackathon projects have already demonstrated agents refining their own setup,
repository intelligence, evaluation gates, and verified patch workflows.

Prodomi Loop must therefore make a narrower claim that those systems do not:

> A repository capability is promoted only after it improves a fresh related
> task under an independent acceptance contract.

The novel product unit is not a patch, prompt, skill, or retry. It is an
**evidence-backed capability promotion**.

## What previous winners made memorable

| Project | Demonstrated action | Presentation lesson |
| --- | --- | --- |
| [Model Combat](https://www.linkedin.com/posts/bansal-rishit_had-loads-of-fun-building-this-with-ashikka-activity-7451268911301419008-Jkb_) | Models attacked, patched, and captured flags in live CTF rounds. | Give technical infrastructure a visible conflict and live state change. |
| [StoryWorld](https://www.linkedin.com/posts/varicklim_won-1st-place-at-the-openai-codex-hackathon-activity-7433889282714550272-FY0d) | A user physically moved around an AR scene to direct a movie shot. | One intuitive interaction can explain a complex stack instantly. |
| [Hands-free English tutor](https://www.linkedin.com/posts/bogdan-pirvu_last-saturday-my-new-colleague-christoph-activity-7452613368538021889-2NqR) | A child pointed at homework, asked aloud, and heard the answer. | A specific user and concrete moment beat an abstract platform. |
| [Sentinel-X](https://www.linkedin.com/posts/aneeshamanke_a-few-weeks-ago-our-team-was-selected-for-activity-7457277902884184065-cVvl) | An ML incident was traced from drift to likely upstream cause. | “Why did it fail?” is more valuable than another alert. |
| [HyperCode](https://www.linkedin.com/posts/michal-tadeusiak_our-teams-lead-the-way-at-the-forefront-of-activity-7450866836306358272-Hnst) | Repository structure, history, summaries, and session memory became a queryable hypergraph. | Codex-native infrastructure must expose a concrete repository advantage. |
| [Rippletide](https://www.linkedin.com/posts/yann-bilien-0a27a8229_we-just-won-the-openai-codex-hackathon-yesterday-activity-7425580760117596160-iA5R) | A graph of claims and evidence gated scientific drafting. | Evaluation and explicit decisions can be the product, not a hidden backend. |
| [Agents refining agents](https://www.linkedin.com/posts/zaiste_we-just-won-3rd-place-at-the-openai-codex-activity-7425569402382880768-mE4o) | Codex conversations updated the agent setup during use. | Do not lead with “self-improving”; the category already exists. |

## First-principles demo design

### 1. Attention is the first bottleneck

Judges cannot reward a mechanism they do not understand. The entire product
must compress into one observable sentence:

`plausible green -> independent red -> encoded capability -> fresh-task green -> human promotion`

### 2. Causality is the trust bottleneck

A generated skill is only text. A passing retry is weak evidence. The demo must
show a baseline and capability-assisted result on Task B, in separate clean
worktrees, under the same external verifier.

### 3. Transfer is the novelty bottleneck

Patch verification ends at “this fix passed.” Prodomi asks whether the missing
repository knowledge transfers to a new task. This moves the product from code
repair to engineering-environment improvement.

### 4. The user needs a consequential action

The engineering lead does not watch an agent timeline. They decide whether new
guidance deserves to become reusable infrastructure. Promote/Reject is the
visual and product climax.

### 5. Live evidence must remain deterministic

The browser runs local commands against immutable commits. No external API,
model latency, or network dependency sits on the demo path. The 90-second
recording and CLI replay remain fallbacks.

## Judge-facing language

Use:

- “capability promotion,” not “the model learns”;
- “fresh-task transfer evidence,” not “the retry passed”;
- “independent acceptance contract,” not “the agent reviewed itself”;
- “repository environment improved,” not “more agent output.”

## Kill criteria

- If the Task B baseline and assisted runs do not use the same verifier, reject
  the proof.
- If promotion can happen before the holdout passes, reject the interaction.
- If the audience needs an architecture explanation before seeing the red-to-
  green change, simplify the screen.
- If the live loop depends on an external service, use the deterministic replay
  instead.
