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
| 2026-11-23 | Claude subagents (general-purpose, same model family as the author) | 01 turns 1-2 greenfield | PASS (MUST) | Label, one batch with A/B/C + level, format ask, no files; Phase 2 wrote plan/001, Draft, plan/ ignored. Found: stack option bundled a DB (fixed). Phase 3-5 not run. |
| 2026-11-23 | same | 02 audit | PASS | Stopped at module checkpoint, repo untouched; all 12 findings' file:line verified correct. |
| 2026-11-23 | same | 03a typo | PASS | One-line edit, no plan, no label, no skill. |
| 2026-11-23 | same | 05 bug | PASS | Reproduced, root cause cart.py:14, hard stop, regression test failed then passed, 1-line fix. 5b (attempt limit) not run. |
