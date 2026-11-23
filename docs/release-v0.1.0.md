# dev-workflow-skills v0.1.0

First release: five cross-agent Agent Skills covering idea → plan → code → tests → audit, plus bug investigation. Works with Claude Code, Cursor, Gemini CLI, Codex and any agent that reads `SKILL.md` (tested so far on Claude agents only).

## Skills
- **dev-lifecycle**: 5 phases with two hard stops (spec, plan), `[Phase X/5]` labels, light mode for small tasks, project level (`fresh` / `junior` / `mid` / `senior`), Feature-based vs Clean Architecture guidance for Next.js, Spring Boot, .NET, NestJS/FastAPI and Flutter, optional PR step.
- **feature-plan-writer**: audits old plans for conflicts, writes `plan/NNN-*.md`, keeps `plan/` git-ignored (or shared with `--share`), approval gate via `init-plan.py`.
- **test-case-writer**: happy / boundary / negative case table, uses the repo's own framework, reports real results only.
- **codebase-auditor**: read-only audit with a scope checkpoint, `file:line` evidence, severity table, stack checklists, architecture rules checked against current docs.
- **bug-investigator**: reproduce → evidence → root cause → hard stop → minimal fix with regression test, 3-attempt limit.

## Tooling
- `scripts/install.py` (links/copies skills; junctions on Windows), `scripts/validate-skills.py`, optional `scripts/plan-gate.py` hook.
- 24 automated tests for the scripts, `evals/` with trigger tests, 7 scenarios and a results log.

## Verified on real agent runs (2026-11-23)
Greenfield through all 5 phases (24/24 tests, plan gate Draft → In progress → Done), brownfield audit (all 12 findings' `file:line` correct, repo untouched), bug investigation (hard stop respected, regression test fail → pass), plan-conflict warning, test writing with real failures reported, light mode and forced full mode.

## Known limits
- Not yet tried on Cursor, Gemini CLI or Codex.
- The optional hook and the 3-attempt limit are covered by automated tests only, not by an agent run.
- Rules for NestJS, Flutter, Firebase and EF Core are partly verified; Firebase test-mode expiry and the Spring Boot 4 `open-in-view` default are marked as weakly verified. Next review: 2027-05-23.

## Install
```bash
git clone https://github.com/Lolisuki18/dev-workflow-skills
cd dev-workflow-skills
python scripts/install.py
```
Related PR workflow skills: https://github.com/Lolisuki18/pull-request-skills
