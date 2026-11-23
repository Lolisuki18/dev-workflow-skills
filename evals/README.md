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
| 2026-11-23 | same | 01 full run (Python stdlib CLI, phases 1-5) + 07a approval gate | PASS (MUST) | Asked batch incl. level and architecture; plan stayed Draft with no code until "ok, code đi"; status went Draft → In progress → Done; 24/24 unittest verified independently; real bug found by running it (cp1252 console) fixed with a regression test. Findings: the agent stalled once on its own shell heredoc error (not a skill problem) and resumed; final plan checklist left `Quality scan: pending` and a stale Resume point (fixed in dev-lifecycle Phase 5). |
| 2026-11-23 | same | 03b small task | PASS (behavior a) | No skill triggered; direct edit with tests at 50/51 and whitespace case; no plan, no questionnaire. Eval wording relaxed to accept (a) or (b). |
| 2026-11-23 | same | 03d force full mode | PASS | "chạy đủ quy trình" on a typo: ran Phase 1, asked questions, noted light mode was available, no files created. |
| 2026-11-23 | same | 04 plan conflict | PASS | Read plan/001, warned about token storage and table name conflicts, gave options with a recommendation, wrote nothing, left .gitignore alone because plan/ was tracked (also exercised skipped-tracked). |
| 2026-11-23 | same | 06 test writing | PASS | Table by category, real run (12 tests, 2 failures at the 5 kg and 500000 boundaries), production code untouched (verified by git diff), proposed a lessons-learned rule without writing it. |
| 2026-11-23 | same | 05 bug | PASS | Reproduced, root cause cart.py:14, hard stop, regression test failed then passed, 1-line fix. 5b (attempt limit) not run. |
