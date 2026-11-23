# Evals

Manual test suite for the skills. Skills are prompts, so the only real test is running them on an agent and checking behavior. Re-run after every meaningful edit to a SKILL.md.

## Files

- [`trigger-tests.md`](trigger-tests.md): one-line prompts. Checks the RIGHT skill triggers, and none triggers when it should not (typo, chit-chat).
- [`scenarios/`](scenarios): multi-turn scenarios with setup, scripted user turns, and a pass/fail checklist.

## How to run

1. Install the skills (see the root README) and open a fresh session in the folder named in each scenario's **Setup** (use a throwaway copy, never a real project).
2. Send the prompt exactly as written; answer follow-up turns using the scripted replies.
3. Tick each checklist line PASS / FAIL. A scenario passes only if every **MUST** line passes; **SHOULD** lines are quality signals.
4. Record the date, agent, model and result in the table below.

## Scoring

| Level | Meaning |
|-------|---------|
| MUST | Hard rule from the SKILL.md (hard stops, read-only, file:line evidence, labels). Any FAIL = scenario fails. |
| SHOULD | Quality: concise, right language, good defaults. Track, fix when it repeats. |

When a FAIL repeats across runs, fix the SKILL.md wording (shorter, more explicit, move the rule higher) and re-run; do not just retry.

## Results log

| Date | Agent / model | Scenario | Result | Notes |
|------|---------------|----------|--------|-------|
|      |               |          |        |       |
