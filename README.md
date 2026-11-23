# dev-workflow-skills

A set of four independent, cross-agent **Agent Skills** (open Agent Skills format: a folder with `SKILL.md` + optional `references/`) that cover the path from a rough idea to planned, implemented, tested and audited code. Works with Claude Code, Cursor, Gemini CLI, Codex and any agent that reads `SKILL.md`.

## Skills

| Skill | Role | Status |
|-------|------|--------|
| `dev-lifecycle` | Orchestrator for 5 phases with hard stops | ready |
| `feature-plan-writer` | Audits old plans, writes `plan/NNN-*.md`, git-ignores `plan/` | ready |
| `test-case-writer` | Designs, writes and runs tests | coming |
| `codebase-auditor` | Read-only audit of an existing codebase | coming |

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
```

`codebase-auditor` can also be used standalone to audit a legacy repo (read-only).

Each `dev-lifecycle` reply starts with a `[Phase X/5: ...]` label so the agent does not forget the rules.

## Layout

```
skills/
├── dev-lifecycle/        SKILL.md, references/{phase-templates,formatter-setup}.md
├── feature-plan-writer/  SKILL.md
├── test-case-writer/     SKILL.md
└── codebase-auditor/     SKILL.md, references/{backend,frontend,security-and-ops}.md
```

Skills reference each other by name only, so install all four together.

## Installation

Pick the skills directory your agent reads, then copy or symlink each folder under `skills/`.

| Agent | Project scope | User scope |
|-------|---------------|------------|
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| Cursor | `.cursor/skills/` (or `.agents/skills/`) | `~/.cursor/skills/` |
| Gemini CLI | `.gemini/skills/` (or `.agents/skills/`) | `~/.gemini/skills/` |
| Codex | `.agents/skills/` | `~/.agents/skills/` |

Directory names vary by agent version; check your agent's docs if a skill is not discovered. The folder name must equal the `name` in the frontmatter.

### macOS / Linux (symlink)

```bash
git clone <this-repo> ~/dev-workflow-skills
mkdir -p ~/.claude/skills
for d in ~/dev-workflow-skills/skills/*/; do ln -s "$d" ~/.claude/skills/$(basename "$d"); done
```

Replace `~/.claude/skills` with the path from the table.

### Windows (PowerShell)

```powershell
git clone <this-repo> $HOME\dev-workflow-skills
New-Item -ItemType Directory -Force "$HOME\.claude\skills" | Out-Null
Get-ChildItem "$HOME\dev-workflow-skills\skills" -Directory | ForEach-Object {
  New-Item -ItemType Junction -Path "$HOME\.claude\skills\$($_.Name)" -Target $_.FullName
}
```

Junctions need no admin rights; use `-ItemType SymbolicLink` if you prefer (requires Developer Mode or admin). Or simply copy the folders.

## Usage

- "Tôi muốn làm một ứng dụng học tiếng Anh" → `dev-lifecycle` starts Phase 1.
- "Lên plan cho tính năng đăng nhập" → `feature-plan-writer`.
- "Viết test cho module này" → `test-case-writer`.
- "Audit giúp tôi codebase này" → `codebase-auditor`.

## About `plan/`

Plans are saved in `plan/` and `plan/` is added to `.gitignore` automatically. To share or version them, delete the `plan/` line from `.gitignore`.
