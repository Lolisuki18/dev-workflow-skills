# dev-workflow-skills

Ten independent, cross-agent **Agent Skills** (open Agent Skills format: a folder with `SKILL.md` + optional `references/` and `scripts/`) covering the path from a rough idea to planned, implemented, tested, debugged and audited code. Works with Claude Code, Cursor, Gemini CLI, Codex and any agent that reads `SKILL.md`.

## Skills

| Skill                                        | Role                                                                                       |
| -------------------------------------------- | ------------------------------------------------------------------------------------------ |
| [`dev-lifecycle`](dev-lifecycle)             | Orchestrator for 5 phases with hard stops, plus a light mode for small tasks               |
| [`feature-plan-writer`](feature-plan-writer) | Audits old plans, writes `plan/NNN-*.md`, git-ignores `plan/` (via `scripts/init-plan.py`) |
| [`test-case-writer`](test-case-writer)       | Designs, writes and runs tests (happy / boundary / negative)                               |
| [`codebase-auditor`](codebase-auditor)       | Read-only audit of an existing codebase with `file:line` evidence                          |
| [`bug-investigator`](bug-investigator)       | Reproduce → evidence → root cause → minimal fix with regression test                       |
| [`refactor-planner`](refactor-planner)       | Behavior-preserving refactor: characterization tests first, then small verified steps      |
| [`security-reviewer`](security-reviewer)     | Read-only security review (auth, authorization, injection, secrets) with exploit scenarios |
| [`migration-writer`](migration-writer)       | Safe schema and framework/dependency migrations with rollback (expand → migrate → contract) |
| [`code-explainer`](code-explainer)           | Read-only onboarding map of an unfamiliar repo, with one traced flow                       |
| [`ci-cd-setup`](ci-cd-setup)                 | CI pipeline, Dockerfile and deploy/rollback guide from the repo's real commands            |

## Flow

```
Idea / feature request
        │
[Phase 1/5] Discovery & Clarification ── HARD STOP: user locks spec
        │
[Phase 2/5] Planning (feature-plan-writer) ── HARD STOP: user approves plan
        │
[Phase 3/5] Implementation (vertical slices + format/lint/type-check)
        │
[Phase 4/5] Testing & Verification (test-case-writer, requirement traceability)
        │
[Phase 5/5] Final Audit & Wrap-up (codebase-auditor checklists)
        │
(optional) PR step → pre-pr-self-review + pr-description-writer
```

- `codebase-auditor` can be used standalone to audit a legacy repo (read-only). Its findings feed `refactor-planner` (tech debt) and `security-reviewer` (deeper security pass).
- `refactor-planner` and `migration-writer` can be used standalone or called from Phase 3; `code-explainer` is for reading, `ci-cd-setup` for automation files.
- `bug-investigator` handles bugs; `dev-lifecycle` hands over to it when a failure is unexplained.
- Each `dev-lifecycle` reply starts with a `[Phase X/5: ...]` label so the agent does not forget the rules.
- **Light mode:** trivial edits skip the workflow; small ones get a mini-plan and a quick test. Say "chạy đủ quy trình" to force all 5 phases or "làm nhanh thôi" to force light mode.

## Related skills: PR workflow

The optional last step uses two skills from a separate repo: **[Lolisuki18/pull-request-skills](https://github.com/Lolisuki18/pull-request-skills)**

- `pre-pr-self-review`: checks your diff against the plan's requirements (R1..Rn) before opening a PR.
- `pr-description-writer`: writes the PR title and description.

They are not required. Install them the same way as below if you want `dev-lifecycle` to offer them at the end of Phase 5. If they are missing, `dev-lifecycle` mentions the link once and moves on.

## Sibling repos

| Repo | Covers |
|---|---|
| [`dev-workflow-skills`](https://github.com/Lolisuki18/dev-workflow-skills) (this one) | idea → plan → code → tests → audit, bug investigation |
| [`pull-request-skills`](https://github.com/Lolisuki18/pull-request-skills) | PR description, PR review, review replies, pre-PR self-review, code comments |
| [`qa-workflow-skills`](https://github.com/Lolisuki18/qa-workflow-skills) | QA/STLC: test plan, test matrix, E2E, API, non-functional, regression, defects, summary report |
| [`docs-workflow-skills`](https://github.com/Lolisuki18/docs-workflow-skills) | README, diagrams, API docs, ADRs, changelog, runbook, SDLC reports, Review 2 pack |
| `ai-workflow-suite` | `delivery-lifecycle` orchestrator across all four (build → PR → QA → docs → release), shared `CONVENTIONS.md`, `install-all.py` |

Each repo is self-contained; install only what you need.

## Layout

```
dev-lifecycle/        SKILL.md, references/{phase-templates,formatter-setup,architecture-guide}.md
feature-plan-writer/  SKILL.md, scripts/init-plan.py, references/{plan-template,architecture-conventions}.md
test-case-writer/     SKILL.md, references/lessons-learned.md
codebase-auditor/     SKILL.md, references/{backend,frontend,security-and-ops,architecture-rules,lessons-learned}.md
bug-investigator/     SKILL.md, references/debug-playbook.md
refactor-planner/     SKILL.md, references/refactor-catalog.md
security-reviewer/    SKILL.md, references/security-checklist.md
migration-writer/     SKILL.md, references/migration-patterns.md
code-explainer/       SKILL.md
ci-cd-setup/          SKILL.md, references/pipeline-templates.md
scripts/validate-skills.py   # repo checker (not a skill)
scripts/install.py           # links/copies the skills into an agent's skills folder
scripts/plan-gate.py         # optional Claude Code hook: blocks code edits while the plan is Draft
AGENTS.md  CHANGELOG.md  .gitattributes
evals/                       # trigger tests + 7 scenarios with pass/fail checklists
tests/test_scripts.py        # automated tests for init-plan.py, plan-gate.py and install.py
docs/                        # hard-stop-enforcement.md, maintenance.md, release notes
README.md
```

Skills reference each other by name only, so install them together. Suite-wide rules are in the sibling `ai-workflow-suite` repo (`CONVENTIONS.md`).

### Architecture choice (Feature-based vs Clean)

For greenfield projects `dev-lifecycle` explains both styles, recommends one for the chosen stack (Next.js, Spring Boot, .NET, NestJS/FastAPI, Flutter) and lets you pick. The choice is stored in the plan and used by `codebase-auditor` later.

### Project level (fresh / junior / mid / senior)

One setting that scales the whole workflow: architecture default, test depth, audit strictness and task size (table in `dev-lifecycle/references/architecture-guide.md`). Asked in Phase 1 for new projects, inferred for existing ones, stored in the plan header, and used by `test-case-writer` and `codebase-auditor`.

### Safety rails

- 3-attempt limit: build/lint failures (Phase 3) and bug fixes (`bug-investigator`) stop after 3 distinct failed attempts and ask the user.
- Skipped tests or quality scans are recorded in the plan (`skipped by user`) and repeated as a risk in the final report.
- The plan has a **Resume point** (section 10) updated after each slice so a new session can continue from the file alone.

### Lessons learned (your own rules)

`references/lessons-learned.md` in `codebase-auditor` and `test-case-writer` is a personal list of recurring mistakes. Skills check every rule and suggest new ones at the end of a report (`bug-investigator` suggests too); they only append after you approve.

## Installation

Easiest (any OS, Python 3 only): from the cloned repo run

```bash
python scripts/install.py                              # links every skill into ~/.claude/skills
python scripts/install.py --agent gemini               # preset for another agent
python scripts/install.py --agent cursor --scope project   # ./.cursor/skills of the current project
python scripts/install.py --list-agents                # all presets and how well each path is verified
python scripts/install.py --target ~/some/skills       # any directory
python scripts/install.py --dry-run                    # preview; --copy to copy; --uninstall to remove
```

It uses junctions on Windows (no admin) and symlinks elsewhere, and never overwrites an existing skill. Manual options below.

Skills directories (checked against each vendor's docs on 2026-11-23; agents move these paths between releases, so use `--list-agents` and your agent's docs if a skill is not found):

| Agent | `--agent` | User scope | Project scope | Confidence |
| ----- | --------- | ---------- | ------------- | ---------- |
| Claude Code | `claude` | `~/.claude/skills/` | `.claude/skills/` | documented |
| Gemini CLI | `gemini` | `~/.gemini/skills/` (alias `~/.agents/skills/`) | `.gemini/skills/` (alias `.agents/skills/`) | documented |
| Cursor | `cursor` | `~/.cursor/skills/` | `.cursor/skills/` or `.agents/skills/` | project documented; user path third-party only. Cursor also reads `~/.claude/skills/` |
| Codex | `codex` | `~/.codex/skills/` | `.agents/skills/` | user path long-standing; project path not confirmed |
| Antigravity | `antigravity` | `~/.gemini/config/skills/` (legacy `~/.gemini/antigravity/skills/`) | `.agents/skills/` | docs conflict between pages; does not read `~/.gemini/skills/` |
| Windsurf | `windsurf` | `~/.codeium/windsurf/skills/` | `.windsurf/skills/` | documented |
| Cline | `cline` | `~/.cline/skills/` | `.cline/skills/` | documented |
| Roo Code | `roo` | `~/.roo/skills/` | `.roo/skills/` | documented |
| Cross-agent | `agents` | `~/.agents/skills/` | `.agents/skills/` | read by several tools |

The folder name must equal the `name` in the frontmatter. Gemini CLI skills are marked experimental in its docs: enable them in its settings if skills do not show up (`/skills list`).

### macOS / Linux (symlink)

```bash
git clone https://github.com/Lolisuki18/dev-workflow-skills ~/dev-workflow-skills
mkdir -p ~/.claude/skills
for d in ~/dev-workflow-skills/*/; do
  [ -f "$d/SKILL.md" ] && ln -s "${d%/}" ~/.claude/skills/$(basename "$d")
done
```

Replace `~/.claude/skills` with the path from the table.

### Windows (PowerShell)

```powershell
git clone https://github.com/Lolisuki18/dev-workflow-skills $HOME\dev-workflow-skills
New-Item -ItemType Directory -Force "$HOME\.claude\skills" | Out-Null
Get-ChildItem "$HOME\dev-workflow-skills" -Directory |
  Where-Object { Test-Path (Join-Path $_.FullName "SKILL.md") } |
  ForEach-Object {
    New-Item -ItemType Junction -Path "$HOME\.claude\skills\$($_.Name)" -Target $_.FullName
  }
```

Junctions need no admin rights; use `-ItemType SymbolicLink` if you prefer (requires Developer Mode or admin). Or simply copy the folders. Do not use `ln -s` in Git Bash on Windows: it silently makes copies.

## Usage

- "Tôi muốn làm một ứng dụng học tiếng Anh" → `dev-lifecycle` starts Phase 1.
- "Lên plan cho tính năng đăng nhập" → `feature-plan-writer`.
- "Viết test cho module này" → `test-case-writer`.
- "Audit giúp tôi codebase này" → `codebase-auditor`.
- "Debug giúp tôi lỗi này" → `bug-investigator`.
- "Dọn code module này nhưng đừng đổi hành vi" → `refactor-planner`.
- "Kiểm tra bảo mật phần đăng nhập" → `security-reviewer`.
- "Thêm cột vào bảng users an toàn" → `migration-writer`.
- "Giải thích repo này cho tôi" → `code-explainer`.
- "Viết pipeline CI và Dockerfile" → `ci-cd-setup`.

## About `plan/`

Plans are saved in `plan/` and `plan/` is added to `.gitignore` automatically, so they stay local (the Resume point will not follow you to another machine). To share them with a team run `python feature-plan-writer/scripts/init-plan.py --share` (or just say "dự án làm nhóm, push plan lên git"). If git already tracks files in `plan/`, the script leaves `.gitignore` alone.

## Hard stops: how they are enforced

Written rules can be ignored in long contexts, so approval is also stored in the plan file (`Status: Draft` → `Approved`) and checked before coding. An optional hook can block edits mechanically. See [docs/hard-stop-enforcement.md](docs/hard-stop-enforcement.md).

## Evals

[`evals/`](evals) holds trigger tests (including prompts that must NOT trigger any skill) and twelve scenarios with MUST/SHOULD checklists. Run them on a real agent after editing a skill; results are logged in [`evals/README.md`](evals/README.md). So far they were run on Claude agents only, not yet on Cursor, Gemini CLI or Codex.

## Keeping it current

Framework rules are re-verified on a schedule (last verified 2026-11-23, next review 2027-05-23). See [docs/maintenance.md](docs/maintenance.md) for the review calendar, the prompt-drift routine and the release steps; version history is in [CHANGELOG.md](CHANGELOG.md).

## Validate the skills

After editing any skill:

```bash
python scripts/validate-skills.py
```

It checks name = folder, `Do NOT use` in the description, ≤ 250 lines, that every referenced file exists, and that scripts compile. Test the helper scripts with:

```bash
python -m unittest discover -s tests -v
```
