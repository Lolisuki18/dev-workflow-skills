# Changelog

Format: newest first. Skills are prompts, so "breaking" means a change in behavior an agent will notice (labels, hard stops, script flags).

## [Unreleased]

## [1.0.0] - 2026-11-27

### Added
- Shared `scripts/run-evals.py` (copy of the canonical file in `ai-workflow-suite`; `turns:` multi-turn convention, `--dry-run`).
- Go, Rust, Android native and iOS native coverage: architecture guide and plan layouts, per-stack `codebase-auditor` files (`architecture-go.md`, `-rust.md`, `-android.md`, `-ios.md`), security checklist, test detection, formatter setup, migration tools, CI templates and profiling tools.
- Skills: `refactor-planner`, `security-reviewer`, `migration-writer`, `code-explainer`, `ci-cd-setup`, `performance-profiler` (each with a validated `SKILL.md`; references for the first three and `ci-cd-setup`).
- `LICENSE` (MIT).
- `scripts/install.py --only` / `--exclude`; `scripts/readme-index.py` (generated skill index, checked in CI); CI workflow (`validate-skills.py` and the unit tests, plus a diff against the shared scripts of `ai-workflow-suite`); `.claude-plugin/plugin.json`. 31 tests.
- Scenarios 08-12 and trigger tests for the new skills; smoke-run results in `evals/README.md` (also for `performance-profiler`, which has no scenario file yet).
- `install.py --agent claude|gemini|cursor|codex|antigravity|windsurf|cline|roo|agents`, `--scope user|project`, `--list-agents`. Paths were checked against vendor docs; the ones that could not be confirmed (Cursor user scope, Codex project scope, Antigravity) are marked `weak` and print a warning. 3 new tests (27 total).
- `feature-plan-writer`: explicit quoting rules for script paths with spaces (bash and PowerShell, verified with a path containing spaces) and manual fallback for the status commands when Python is missing.
- README: install table now lists every agent preset with its confidence level.

### Changed
- `codebase-auditor` architecture rules split into per-stack files (`architecture-<stack>.md`, one loaded per audit); `architecture-rules.md` keeps the verification block and the usage and style rules.
- References now load on demand per step: `dev-lifecycle` phase templates split into Phase 1 (`phase-templates.md`) and Phases 2-5 (`phase-templates-p2-p5.md`, read after the Phase 1 hard stop); already-loaded references are not re-read. Measured (tokens = bytes / 3.8): `dev-lifecycle` eager 7,475 -> 7,182 (-4%); `codebase-auditor` typical run 7,830 -> 6,054 (-23%). The dev path eager total went 14,012 -> 14,147 because `SKILL.md` text grew in the same period.
- Friction fixes from real agent runs on a tiny Python CLI: `dev-lifecycle` (sizing by counts not adjectives, pre-filled greenfield answers, multi-slice pass for tiny projects, hygiene files, no-formatter evidence, defect fixes map to existing R-ids); `feature-plan-writer` (`--check` side effect on `.gitignore`, template already written by the script); `bug-investigator` (NOT-REPRODUCED exit, unreported defects as separate items, regression test first with a 1-3 case list, line endings kept); `test-case-writer` (defers to `bug-investigator`, `Lessons applied` line, guard vs regression, Target from tool output); `security-reviewer` (small-scope compact report, CLI / local tool checklist); `code-explainer` short mode; `codebase-auditor` no-matching-stack note; `refactor-planner` and `performance-profiler` small-scope rule, no invented targets.
- Skill descriptions are English only and shorter (4 trigger phrases, at most 650 characters) to cut the context every installed skill costs. The trigger evals keep their Vietnamese prompts to check that matching still works.
- Every skill states that content found in repos, logs and pages is data, not instructions. `code-explainer` takes `file:line` numbers from tool output, not by eye.
- Findings from a real run (vanilla-JS static web app via `dev-lifecycle`): `dev-lifecycle` counts a requirement verified by running the app as `manual (ran)` with an evidence line (`not run` otherwise) and has a frontend check list (`references/frontend-check.md`); rule for a new module inside an existing repo (own folder, siblings untouched, `<plan number>:Rn` ids, `qa-artifacts/<module>/` and `docs/<module>/`), also in `feature-plan-writer`; re-run the Phase 4 checks after any Phase 5 fix; no dependency on the `delivery-lifecycle` skill being installed.
- Sub-skills used by `dev-lifecycle` (`feature-plan-writer`, `test-case-writer`, `codebase-auditor`, `bug-investigator`, `security-reviewer`) keep the `[Phase X/5: ...]` label inside it and use their own labels only standalone.
- `architecture-guide.md` / `architecture-conventions.md`: vanilla JS browser app and plain stdlib script / CLI layouts; `formatter-setup.md`: "no third-party packages" case (`node --check`, `python -m compileall`, warnings as errors, `no formatter configured`).
- Hard-stop related edits: `test-case-writer` asks for approval of the test-case table before writing tests when standalone; `security-reviewer` waits for priority-area approval before Step 2 only when more than about 5 source files are in scope (small-scope text rewritten, compact report table `Severity | Where | Scenario | Fix | Evidence`); `codebase-auditor` skips the module-selection stop for about 5 or fewer source files (rule moved before the STOP item); `bug-investigator` NOT-REPRODUCED exit and "an unreported defect is a separate item".
- `init-plan.py` and `plan-gate.py` choose the latest plan with the same key: numbered plans win over date-named ones and unpadded numbers sort by integer (the hook used a plain name sort). 3 new tests. `hard-stop-enforcement.md` no longer hard-codes test counts.
- Friction fixes round 4 (real runs, weaker-model audit): `dev-lifecycle` (test-case table printed before test files, traceability table named as a different table, `--approve` run and shown right after the yes, Resume point per slice even when batched, no later-phase findings in a phase message, no commits unless asked, baseline checks with only new failures blocking, `not run` with reason, keep line endings); `init-plan.py --check` is now read-only (`plan_dir=`, `next_plan=`, `gitignore=would-add|would-create|already|skipped-tracked`) and the `.gitignore` edit moved to plan creation; `test-case-writer` (expected-failure marker for real defects, never a silently red CI); `codebase-auditor` (partial stack applicability, may run tests and start the app locally); `migration-writer` (rollback files outside the runner glob, one stop for a small additive change); `refactor-planner`, `performance-profiler`, `ci-cd-setup` (single merged stop for small scope); `ci-cd-setup` (no invented action versions, YAML not machine-checked wording); `feature-plan-writer` (copy requirement text into docs, not the git-ignored plan path); scenario 09 expectation matches the small-scope skip.
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
