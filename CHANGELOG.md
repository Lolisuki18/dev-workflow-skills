# Changelog

Format: newest first. Skills are prompts, so "breaking" means a change in behavior an agent will notice (labels, hard stops, script flags).

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
