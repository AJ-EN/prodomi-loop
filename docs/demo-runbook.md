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
python3 -m http.server 8000 --directory review-hub
```

Open `http://localhost:8000`.

## Live narration

| Time | Show | Say |
| --- | --- | --- |
| 0:00-0:12 | Task A visible examples pass | “Plausible patches often look correct because ordinary examples are green.” |
| 0:12-0:28 | Task A independent failure in replay output | “The independent currency contract catches the rule the candidate missed.” |
| 0:28-0:42 | Diagnosis and candidate capability card | “The problem is not arithmetic; it is a missing repository capability: banker's rounding and currency-specific minor units.” |
| 0:42-0:58 | Task B baseline fail card | “We do not promote on Task A. A fresh related refund task still fails without the capability.” |
| 0:58-1:15 | Task B capability-assisted pass card | “The same independent contract passes in a separate clean worktree when the fresh task uses the capability.” |
| 1:15-1:30 | Click `REVIEW DECISION`, then `PROMOTE CAPABILITY` | “We promote only after the environment improved on a new task. We measure whether the agent earned the right to ship.” |

## Backup and fallback

Record one clean 90-second screen capture from this runbook after the three
rehearsals pass. If the browser is unavailable, use the replay command and show:

1. `skills/currency-rules/SKILL.md`
2. `evidence/task-b-baseline.log`
3. `evidence/task-b-assisted.log`
4. `evidence/task-b-promotion.md`

Do not claim model-weight learning, a general orchestration platform, or
production deployment. The demonstrated result is one promoted repository
capability with fresh-task evidence.
