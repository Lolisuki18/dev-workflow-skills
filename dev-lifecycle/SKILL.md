---
name: dev-lifecycle
description: "Orchestrates a 5-phase software development workflow (Discovery, Planning, Implementation, Testing, Final Audit) from a raw idea or a feature request in an existing repo to finished, tested code, with hard stops for user approval. Use when the user says 'build me an app', 'I want to make...', 'add a feature', 'implement end to end', 'start a new project', 'tôi muốn làm một ứng dụng', 'làm tính năng này từ đầu đến cuối', 'khởi tạo dự án', 'code giúp tôi cả quy trình', or gives a vague idea needing clarification. Do NOT use for trivial edits (one file or a few lines, typo, rename, config tweak) which need no workflow, debugging or fixing a bug (use bug-investigator), only writing a plan file (use feature-plan-writer), only writing tests (use test-case-writer), or only auditing existing code without changing it (use codebase-auditor)."
---

# Dev Lifecycle — 5-Phase Orchestrator

Drive work through five phases in order. Never skip a phase, never merge two hard stops into one.

## Anchor rule (anti-forgetting)

Begin EVERY response with a phase label, exactly one of:

`[Phase 1/5: Discovery & Clarification]` · `[Phase 2/5: Planning]` · `[Phase 3/5: Implementation]` · `[Phase 4/5: Testing & Verification]` · `[Phase 5/5: Final Audit & Wrap-up]`

If the label is missing from your last reply, you have drifted: re-read this file and restate the current phase.

## Ground rules

- Reply in the user's language (Vietnamese in, Vietnamese out). Keep code identifiers in English.
- Agent-agnostic: say "inspect the repo", "run the lint/test commands" — use whatever tools your environment offers.
- Anti-hallucination: every claim about existing code cites `file:line`. Never import or recommend a library that is not installed or declared in the manifest unless you flag it as a NEW dependency and ask first.
- Templates for each phase output live in `references/phase-templates.md`. Load it when producing a phase output.

## Size the task first (light mode)

Before Phase 1, judge the size from the request and a quick look at the repo:

- **Trivial** (one file or a few lines; typo, rename, copy change, config tweak, obvious one-line bug): do NOT run the 5 phases. Say in one line that you are using light mode, make the change, run the project's format/lint/test commands for that file, and report. No plan file, no labels.
- **Small** (one self-contained behavior, ≤ ~3 files, no schema/API/contract change): light mode with a mini-plan: state in 3–5 bullets what you will change, wait for the user's "ok", implement, then run or add the relevant tests (`test-case-writer`). Use `[Light mode]` as the label. Skip `plan/` files and the final audit.
- **Normal / Large** (new feature, several modules, new data model or API, greenfield, anything the user calls a project): run all 5 phases below.

When unsure, ask the user in one line: "Việc này nhỏ, làm nhanh luôn hay chạy đủ quy trình 5 pha?" The user can always force full mode ("chạy đủ quy trình") or light mode ("làm nhanh thôi"). If light mode work grows beyond its size (more files, contract changes), stop and switch to the full flow.

## Phase 1 — Discovery & Clarification

First decide the mode by inspecting the repo:

- **Greenfield** (empty directory, or only a raw idea such as "I want an English-learning app").
- **Brownfield** (repo already has code).

### Greenfield
Ask ONE batched message of 4–5 questions covering: platform (web/mobile/desktop/CLI), MVP scope (3–5 must-have features), tech stack, data & storage, and auth/deployment. Give every question lettered options with a recommended default (A/B/C) so the user can answer with e.g. "1A 2B 3A". Use the template in `references/phase-templates.md`.

**Architecture choice:** when the stack is known, read `references/architecture-guide.md`. Briefly explain Feature-based vs Clean Architecture (what each is), recommend one for the user's stack with the reason, and let them choose (A/B/C). Skip the lecture if they already named a style. Record it as `Architecture: <style> — <reason>` in the Spec Summary.

**Code-format suggestion:** once the stack is known (or proposed), read `references/formatter-setup.md` and recommend the extensions/config for that stack. Ask whether the user wants you to generate `.editorconfig`, `.vscode/extensions.json` and the formatter config (Prettier/Ruff/etc.) during scaffolding. Do not create them without a yes.

### Brownfield
Before asking anything:
1. Inspect the repo layout, manifests (package.json, pyproject.toml, pom.xml, *.csproj, pubspec.yaml...), and code related to the request.
2. Read existing files in `plan/` (if any) to learn established architecture, naming, data model and decisions.
3. Only then ask about what is genuinely ambiguous. Do not ask what the code already answers; state what you found with `file:line`.

### Proactive Advisor (always include)
End the clarification with a short section **Cố vấn chủ động / Proactive Advisor**:
- a cleaner or simpler solution than what the user described, if one exists;
- risks (security, scaling, data loss, scope creep, licensing);
- existing code/utilities that should be reused (cite `file:line`).

### HARD STOP
Stop after the questions + advisor notes. Wait until the user confirms the spec ("chốt", "ok", answers given). Then write a 5–10 line **Spec Summary** and ask for a final yes only if answers were partial. Do not start Phase 2 before that.

## Phase 2 — Planning

1. Invoke the `feature-plan-writer` skill with the confirmed spec. It audits old plans, writes `plan/NNN-name.md`, and ensures `plan/` is git-ignored.
2. Present a short summary of the plan (requirements R1..Rn, files to touch, risks).

### HARD STOP
Do NOT create or modify any source file until the user approves the plan ("ok", "code đi", "approved", "go"). If the user requests changes, update the plan file and ask again. Scaffolding config files (formatter, `.editorconfig`) count as code: wait for approval too, unless the user already said yes in Phase 1.

## Phase 3 — Implementation

- Work in small **vertical slices** (one requirement end to end: data → logic → API/UI), in the order set by the approved plan.
- Stay inside the plan's file list. If you discover a needed change outside it, stop and tell the user; update the plan first.
- No unrelated refactors, no drive-by renames, no new dependencies that are not in the plan.
- After each slice run, using the project's own commands: formatter, linter, type-check/compile. Fix issues you introduced before moving on. Report commands run and real results.
- Keep the plan's checklist current (mark Rn done) so context survives long sessions.

## Phase 4 — Testing & Verification

1. Invoke the `test-case-writer` skill to design, write and run tests: happy path, boundary, negative.
2. Build a **traceability table**: each Rn → implementing `file:line` → test name → pass/fail.
3. Any requirement without code or without a passing test is reported as a gap and fixed (back to Phase 3 for that slice) or explicitly accepted by the user.
4. Never fabricate results. If tests cannot be run, say so and why.

## Phase 5 — Final Audit & Wrap-up

Quick scan of ONLY the code written in this session using the `codebase-auditor` checklists (read its `references/` files matching the stack; stay read-only in this phase except for fixing issues you introduced, which you list):

- architecture & layering consistent with `plan/` concepts;
- security basics (secrets, input validation, authz, injection);
- leftover debug logs, dead code, commented-out blocks, stray TODOs.

Then deliver the wrap-up using the template: what was built, files changed, how to run, test results, remaining risks/tech debt, suggested next steps. Remind the user that `plan/` is git-ignored (see `feature-plan-writer`).

### Optional PR step (separate skills, never required)

If the user is about to open a pull request, offer the two skills from https://github.com/Lolisuki18/pull-request-skills when they are installed: `pre-pr-self-review` (check the diff against the plan's R1..Rn) and `pr-description-writer` (title and description). If they are not installed, mention the repo link once and move on. Do not block the wrap-up on them.

## Bugs found along the way

If a failing test or runtime error reveals a bug you cannot explain in one look, hand over to the `bug-investigator` skill instead of patching blindly, then resume the phase.

## Resuming

If invoked mid-project, determine the phase from evidence (is there an approved plan? code? tests?), announce it with the label, and continue from there rather than restarting.
