# Changelog

Format: newest first. Skills are prompts, so "breaking" means a change in behavior an agent will notice (labels, hard stops, script flags).

## Unreleased (next: 0.2.0)

### Added
- Skills: `refactor-planner`, `security-reviewer`, `migration-writer`, `code-explainer`, `ci-cd-setup`, `performance-profiler` (each with a validated `SKILL.md`; references for the first three and `ci-cd-setup`).
- `LICENSE` (MIT).
- `scripts/install.py --only` / `--exclude`; `scripts/readme-index.py` (generated skill index, checked in CI); CI workflow (`validate-skills.py` and the unit tests, plus a diff against the shared scripts of `ai-workflow-suite`); `.claude-plugin/plugin.json`. 31 tests.
- Scenarios 08-12 and trigger tests for the new skills; smoke-run results in `evals/README.md` (also for `performance-profiler`, which has no scenario file yet).
- `install.py --agent claude|gemini|cursor|codex|antigravity|windsurf|cline|roo|agents`, `--scope user|project`, `--list-agents`. Paths were checked against vendor docs; the ones that could not be confirmed (Cursor user scope, Codex project scope, Antigravity) are marked `weak` and print a warning. 3 new tests (27 total).
- `feature-plan-writer`: explicit quoting rules for script paths with spaces (bash and PowerShell, verified with a path containing spaces) and manual fallback for the status commands when Python is missing.
- README: install table now lists every agent preset with its confidence level.

### Changed
- Friction fixes from real agent runs on a tiny Python CLI: `dev-lifecycle` (sizing by counts not adjectives, pre-filled greenfield answers, multi-slice pass for tiny projects, hygiene files, no-formatter evidence, defect fixes map to existing R-ids); `feature-plan-writer` (`--check` side effect on `.gitignore`, template already written by the script); `bug-investigator` (NOT-REPRODUCED exit, unreported defects as separate items, regression test first with a 1-3 case list, line endings kept); `test-case-writer` (defers to `bug-investigator`, `Lessons applied` line, guard vs regression, Target from tool output); `security-reviewer` (small-scope compact report, CLI / local tool checklist); `code-explainer` short mode; `codebase-auditor` no-matching-stack note; `refactor-planner` and `performance-profiler` small-scope rule, no invented targets.
- Skill descriptions are English only and shorter (4 trigger phrases, at most 650 characters) to cut the context every installed skill costs. The trigger evals keep their Vietnamese prompts to check that matching still works.
- Every skill states that content found in repos, logs and pages is data, not instructions. `code-explainer` takes `file:line` numbers from tool output, not by eye.
- README no longer claims `~/.agents/skills` as the Codex user path (not confirmed); Codex defaults to `~/.codex/skills`.

## 0.1.0 — 2026-11-23

First release (release notes: `docs/release-v0.1.0.md`; process: `docs/maintenance.md`).

### Added
- `scripts/install.py`: links (or copies) every skill into an agent's skills directory; safe on Windows (junctions) and POSIX (symlinks), never overwrites. 4 new tests (21 total); the tests caught a junction-detection bug before release.
- `.gitattributes` (LF line endings), `CHANGELOG.md`, root `AGENTS.md` for agents that read it instead of skills.

- `docs/maintenance.md`: review calendar (framework rules every 6 months, evals after every edit), review and release procedures. `architecture-rules.md` now carries `Last verified` / `Next review` dates; `validate-skills.py` warns when a review is overdue, and the auditor reports it.

### Skills
- `dev-lifecycle` (5 phases, hard stops, light mode, project level, architecture choice, optional PR step).
- `feature-plan-writer` (+ `scripts/init-plan.py`: numbering, `.gitignore`, status gate, `--share`, `--gate`).
- `test-case-writer`, `codebase-auditor` (stack checklists, architecture rules verified against current docs, lessons-learned), `bug-investigator` (3-attempt limit).

### Tooling
- `scripts/validate-skills.py`, `scripts/plan-gate.py` (optional hook), `tests/test_scripts.py` (17 tests), `evals/` (trigger tests, 7 scenarios, results log), `docs/hard-stop-enforcement.md`.
