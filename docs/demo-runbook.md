# Prodomi Loop 90-second demo runbook

## Preflight

Run this before opening the Review Hub:

```sh
python3 -m unittest discover -s acceptance -p 'test_*.py'
python3 scripts/replay_loop.py
python3 scripts/rehearse.py --runs 3 --max-seconds 90
```

The replay command must end with `PROMOTE`. The rehearsal command must end with
`REHEARSAL READY`.

Start the Review Hub:

```sh
python3 review-hub/server.py
```

Open `http://127.0.0.1:8000`. The page must begin with the promotion gate locked.

## Live narration

| Time | Show | Say |
| --- | --- | --- |
| 0:00-0:08 | Locked evidence gate; click `RUN LIVE PROOF` | “A coding-agent patch can look correct before it has earned our trust.” |
| 0:08-0:22 | Visible Task A examples turn green; independent contract turns red | “The visible suite passes. Our independent currency contract catches the hidden rule.” |
| 0:22-0:38 | Diagnosis and capability artifact activate | “Prodomi does not retry. It converts the failure into a reusable repository capability: banker's rounding and currency-specific minor units.” |
| 0:38-0:53 | Task B baseline turns red | “We still do not promote it. A fresh refund task fails without that capability.” |
| 0:53-1:08 | Capability-assisted Task B turns green; gate unlocks | “The same holdout passes in a separate clean worktree when Codex can use the new capability.” |
| 1:08-1:22 | Click `PROMOTE CAPABILITY` | “Only now does a human promote it for future runs. Generated guidance is not learning; proven transfer is.” |
| 1:22-1:30 | Promoted state and audit line | “We do not measure code output. We measure whether the repository environment got better.” |

## Backup and fallback

Record one clean 90-second screen capture from this runbook after the three
rehearsals pass. The recording must show the page beginning locked, the live
verifier stream, the gate unlocking, and the human promotion click. If the
browser is unavailable, use the replay command and show:

1. `skills/currency-rules/SKILL.md`
2. `evidence/task-b-baseline.log`
3. `evidence/task-b-assisted.log`
4. `evidence/task-b-promotion.md`

Do not claim model-weight learning, a general orchestration platform, or
production deployment. The demonstrated result is one promoted repository
capability with fresh-task evidence.
