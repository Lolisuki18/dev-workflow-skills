---
name: codebase-auditor
description: "Audits an existing codebase in strictly read-only mode: surveys structure and stack, agrees on 3-5 key modules with the user, deep-scans using stack-specific checklists, and reports evidence-backed findings (file:line) with severity and a cleanup roadmap. Use when the user says 'audit this codebase', 'review the whole project', 'find bugs and tech debt', 'security check my repo', 'is this production ready', 'audit codebase giúp tôi', 'rà soát dự án', 'kiểm tra chất lượng code', 'tìm lỗi bảo mật và nợ kỹ thuật', 'đánh giá đồ án'. Do NOT use for fixing a specific bug (use bug-investigator), changing code (use dev-lifecycle), writing plans (use feature-plan-writer), writing tests (use test-case-writer), or reviewing a single PR diff."
---

# Codebase Auditor (read-only)

## Absolute rules

- **READ-ONLY.** Never edit, create, delete, format or auto-fix any project file while auditing. Do not run commands that modify the repo (formatters with write mode, migrations, installs, `git commit`). Running read-only commands (list files, lint/test in check mode, `git log`) is allowed. The only output is the report, in chat or, if the user asks, as a new file outside the source tree.
- **Evidence or silence.** Every finding carries `file:line` (or `file:start-end`) that you actually opened. No evidence → do not report it; put it under "Could not verify" instead.
- **No invented facts.** Never claim a library, framework or config exists unless found in manifests/lockfiles/code. Do not recommend a fix that relies on tools not installed without marking it as a NEW dependency.
- Reply in the user's language. Be agent-agnostic: "inspect the repo", "search the code".

## Step 1 — Survey & scope (CHECKPOINT)

1. Read the directory tree (depth 2–3), root configs and manifests (package.json, pyproject.toml, requirements, pom.xml/build.gradle, *.csproj, pubspec.yaml, Dockerfile, CI files, .env.example, README).
2. Classify:
   - **Stack type:** Frontend / Backend / Full-stack (and framework, language, DB).
   - **Scale:** MVP / student project vs Production. Evidence: tests, CI, deploy config, users, logging, migrations. Calibrate severity to scale (a missing rate limiter is Low for a coursework demo, High for a public API).
3. Propose **3–5 critical modules** to deep-scan (e.g. auth, payment, data access, main API layer, core UI state), each with one line of why.
4. **STOP and ask** the user to approve or change the list (and the scale if unsure). Do not deep-scan before the answer. If the user said "scan everything", still confirm the module list in one message.

## Step 2 — Deep scan with the matching references

Load ONLY the files that match the detected stack:

| Detected | Load |
|----------|------|
| Backend / API / services / DB | `references/backend.md` |
| Frontend / UI / mobile client | `references/frontend.md` |
| Any stack (secrets, auth, config, deploy, logging, deps) | `references/security-and-ops.md` |

ALWAYS also load `references/architecture-rules.md` (judge against the project's declared or evident style, only the sections for the detected stack) and `references/lessons-learned.md` (the user's own recurring-mistake rules; check each rule against the scoped modules and report hits as normal findings).

Full-stack → load all three stack files. Pure frontend with no server → frontend + security-and-ops. Do not load files that are not relevant.

Method:
- Work module by module from the approved list. Read the real code; follow calls across layers.
- Use search to confirm patterns (hard-coded secrets, raw SQL string concatenation, unused exports, `console.log`/`print` leftovers, TODO/FIXME).
- Run existing read-only checks if available (lint, type-check, tests, dependency audit) and cite the output; if you cannot run them, say so.
- Record each finding as you go: severity, file:line, what, why it matters, suggested fix (describe it, do not apply it).

Severity guide:
- **Critical:** exploitable now or data loss (auth bypass, injection, committed live secret, destructive bug).
- **High:** likely bug or serious weakness (missing authz check, broken transaction, N+1 on hot path, no input validation on public endpoint).
- **Medium:** maintainability/robustness (god classes, duplicated logic, swallowed errors, missing tests on core logic).
- **Low:** style/cleanliness (dead code, debug logs, naming, small inconsistencies).

## Step 3 — Report

Use exactly this structure:

```markdown
# Audit report — <project>
Stack: ... | Scale: ... | Scope: <approved modules> | Date: YYYY-MM-DD
Commands run: <list with real results, or "none">

## Highlights (2–3 strengths)
- <strength> (file:line)

## Findings
| # | Severity | file:line | Issue | Impact | Suggested fix |
|---|----------|-----------|-------|--------|---------------|
| 1 | Critical | src/auth.ts:42 | ... | ... | ... |
(sorted Critical → Low; every row has file:line)

## Cleanup roadmap
**Quick wins (≤ 1 day each, low risk):** ...
**Structural debt (needs design / plan):** ...

## Could not verify / out of scope
- <area not scanned, reason>

## Suggested new rules (only for repeat habits)
- [area] <rule as a ready-to-paste bullet for references/lessons-learned.md>
```

Do not edit `references/lessons-learned.md` yourself; ask the user, and append only after a yes.

Rules for the report:
- Always include 2–3 genuine highlights; do not invent praise.
- Group duplicate occurrences into one row listing several `file:line`.
- Keep it proportionate to scale; no padding with generic advice.
- End with: "Audit is read-only; no files were changed. To fix items, I can plan them with feature-plan-writer / dev-lifecycle." Offer, do not start.

## Use inside dev-lifecycle Phase 5

When called for a quick scan of newly written code, skip the module checkpoint, limit the scope to files changed in this session, load the relevant references, and report only the findings table plus verdict.
