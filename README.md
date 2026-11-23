# dev-workflow-skills

Five independent, cross-agent **Agent Skills** (open Agent Skills format: a folder with `SKILL.md` + optional `references/` and `scripts/`) covering the path from a rough idea to planned, implemented, tested, debugged and audited code. Works with Claude Code, Cursor, Gemini CLI, Codex and any agent that reads `SKILL.md`.

## Skills

| Skill | Role |
|-------|------|
| [`dev-lifecycle`](dev-lifecycle) | Orchestrator for 5 phases with hard stops, plus a light mode for small tasks |
| [`feature-plan-writer`](feature-plan-writer) | Audits old plans, writes `plan/NNN-*.md`, git-ignores `plan/` (via `scripts/init-plan.py`) |
| [`test-case-writer`](test-case-writer) | Designs, writes and runs tests (happy / boundary / negative) |
| [`codebase-auditor`](codebase-auditor) | Read-only audit of an existing codebase with `file:line` evidence |
| [`bug-investigator`](bug-investigator) | Reproduce → evidence → root cause → minimal fix with regression test |

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

- `codebase-auditor` can be used standalone to audit a legacy repo (read-only).
- `bug-investigator` handles bugs; `dev-lifecycle` hands over to it when a failure is unexplained.
- Each `dev-lifecycle` reply starts with a `[Phase X/5: ...]` label so the agent does not forget the rules.
- **Light mode:** trivial edits skip the workflow; small ones get a mini-plan and a quick test. Say "chạy đủ quy trình" to force all 5 phases or "làm nhanh thôi" to force light mode.

## Related skills: PR workflow

The optional last step uses two skills from a separate repo: **[Lolisuki18/pull-request-skills](https://github.com/Lolisuki18/pull-request-skills)**

- `pre-pr-self-review`: checks your diff against the plan's requirements (R1..Rn) before opening a PR.
- `pr-description-writer`: writes the PR title and description.

They are not required. Install them the same way as below if you want `dev-lifecycle` to offer them at the end of Phase 5.

## Layout

```
dev-lifecycle/        SKILL.md, references/{phase-templates,formatter-setup,architecture-guide}.md
feature-plan-writer/  SKILL.md, scripts/init-plan.py, references/{plan-template,architecture-conventions}.md
test-case-writer/     SKILL.md, references/lessons-learned.md
codebase-auditor/     SKILL.md, references/{backend,frontend,security-and-ops,architecture-rules,lessons-learned}.md
bug-investigator/     SKILL.md, references/debug-playbook.md
scripts/validate-skills.py   # repo checker (not a skill)
scripts/install.py           # links/copies the skills into an agent's skills folder
scripts/plan-gate.py         # optional Claude Code hook: blocks code edits while the plan is Draft
AGENTS.md  CHANGELOG.md  .gitattributes
evals/                       # trigger tests + scenarios with pass/fail checklists
tests/test_scripts.py        # automated tests for init-plan.py and plan-gate.py
docs/hard-stop-enforcement.md
LICENSE  README.md
```

Skills reference each other by name only, so install them together.

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
python scripts/install.py                  # links every skill into ~/.claude/skills
python scripts/install.py --target ~/.cursor/skills   # another agent
python scripts/install.py --dry-run        # preview; --copy to copy; --uninstall to remove
```

It uses junctions on Windows (no admin) and symlinks elsewhere, and never overwrites an existing skill. Manual options below.

Pick the skills directory your agent reads, then copy or link each skill folder (every folder that contains a `SKILL.md`).

| Agent | Project scope | User scope |
|-------|---------------|------------|
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| Cursor | `.cursor/skills/` (or `.agents/skills/`) | `~/.cursor/skills/` |
| Gemini CLI | `.gemini/skills/` (or `.agents/skills/`) | `~/.gemini/skills/` |
| Codex | `.agents/skills/` | `~/.agents/skills/` |

Directory names vary by agent version; check your agent's docs if a skill is not discovered. The folder name must equal the `name` in the frontmatter.

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

## About `plan/`

Plans are saved in `plan/` and `plan/` is added to `.gitignore` automatically, so they stay local (the Resume point will not follow you to another machine). To share them with a team run `python feature-plan-writer/scripts/init-plan.py --share` (or just say "dự án làm nhóm, push plan lên git"). If git already tracks files in `plan/`, the script leaves `.gitignore` alone.

## Hard stops: how they are enforced

Written rules can be ignored in long contexts, so approval is also stored in the plan file (`Status: Draft` → `Approved`) and checked before coding. An optional hook can block edits mechanically. See [docs/hard-stop-enforcement.md](docs/hard-stop-enforcement.md).

## Evals

[`evals/`](evals) holds trigger tests (including prompts that must NOT trigger any skill) and six scenarios with MUST/SHOULD checklists. Run them on a real agent after editing a skill.

## Validate the skills

After editing any skill:

```bash
python scripts/validate-skills.py
```

It checks name = folder, `Do NOT use` in the description, ≤ 250 lines, that every referenced file exists, and that scripts compile. Test the helper scripts with:

```bash
python -m unittest discover -s tests -v
```

## License

[MIT](LICENSE)
