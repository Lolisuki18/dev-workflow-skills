---
name: refactor-planner
description: "Plans and performs a behavior-preserving refactor in small verified steps: pins current behavior with characterization tests first, splits the change into steps that each keep the build green, applies one step at a time and re-runs the checks after every step. Use when the user says 'refactor this', 'clean up this module', 'pay down tech debt', 'split this god class', 'extract this logic', 'remove duplication', 'dọn code giúp tôi', 'refactor module này', 'tách hàm quá dài', 'giảm nợ kỹ thuật', 'làm sạch code cũ'. Do NOT use for adding features or changing behavior (use dev-lifecycle), finding what is wrong in a codebase (use codebase-auditor), fixing a bug (use bug-investigator), or only writing tests (use test-case-writer)."
---

# Refactor Planner

Change the structure of code without changing what it does. The failure mode this skill prevents: a "quick cleanup" that silently changes behavior and cannot be reviewed.

## Anchor rule

Begin EVERY response with a step label: `[Refactor 1/5: Scope]` · `[Refactor 2/5: Safety net]` · `[Refactor 3/5: Step plan]` · `[Refactor 4/5: Execute]` · `[Refactor 5/5: Report]`.

## Ground rules

- Reply in the user's language; keep identifiers in English.
- Behavior is frozen. A refactor never mixes with a feature or bug fix. If you find a bug on the way, list it and leave it, unless the user agrees to a separate step.
- Every claim about code cites `file:line`. Never report a check as passing unless you ran it.
- Work on a branch or a clean working tree. If `git status` is dirty, ask the user to commit or stash first.
- Agent-agnostic: "run the tests", "search the code" mean whatever tools you have.

## Step 1 — Scope

1. Get the target (files, module, function) and the goal in one sentence: readability, duplication, testability, a smaller class, a dependency direction. If the user pasted an audit report, take the findings from it.
2. Read the target and its callers. List the public surface that must not change (exports, routes, DB columns, CLI flags, event names).
3. Estimate size and risk: lines touched, callers, test coverage today. Write "out of scope" items explicitly.

## Step 2 — Safety net

1. Run the existing tests and record the real baseline (pass/fail counts, command). If they already fail, stop and tell the user: a refactor on a red build cannot be verified.
2. Find the uncovered behavior of the target. Write **characterization tests** that pin what the code does today, even when that looks odd. Use the repo's own framework and style (see `test-case-writer` for conventions). Name each test after the behavior it pins.
3. Confirm each new test passes on the unchanged code. A characterization test that fails on current code is wrong.
4. If tests cannot be written (UI-only, no seam), say what manual check will stand in and mark confidence as lower.

### HARD STOP
Show the baseline, the new tests and the gaps. Wait for "ok" before planning the steps.

## Step 3 — Step plan

Write the plan as numbered steps, each small enough to review alone and each leaving the build green. Use `references/refactor-catalog.md` to pick the move (extract, inline, move, rename, introduce seam, replace conditional, break dependency).

For each step: what moves, files touched, the check that proves it (command), and how to revert (one commit per step). Order steps so risky ones come after the safety net is wider.

### HARD STOP
Present the plan and wait for approval. If the plan has more than about 8 steps, propose splitting it into separate PRs.

## Step 4 — Execute

- One step at a time: change, run the checks, report the real result, then commit-ready state before the next step.
- No drive-by changes: no formatting churn, renames or dependency upgrades outside the step.
- If a check fails: revert the step to green, find out why, and adjust the plan. After 3 distinct failed attempts on one step, STOP and ask the user.
- Never edit, delete or weaken a characterization test to make a step pass. If a test must change, the step changed behavior: stop and say so.

## Step 5 — Report

```
[Refactor 5/5: Report]
Goal: ...
Steps done: N of M (one line each, file:line)
Checks: <commands + real results, before vs after>
Behavior changes: none | <list, with the user's approval>
Left alone on purpose: <bugs, smells outside scope, file:line>
Follow-ups: <next refactor, separate PR candidates>
```

Compare size before and after only with numbers you measured (lines, function length, number of branches). Do not claim "better performance" or "cleaner" without evidence.
