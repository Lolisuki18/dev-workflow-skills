---
name: feature-plan-writer
description: "Plans a feature or project by first auditing existing plan/ files for concept consistency, then writing a numbered plan (requirements R1..Rn, architecture impact, files to change, DB/API contract, edge cases, test plan) into plan/ and adding plan/ to .gitignore. Use when the user says 'write a plan', 'plan this feature', 'design before coding', 'update the plan', 'lên kế hoạch', 'viết plan cho tính năng', 'lập kế hoạch triển khai', 'soạn plan trước khi code', or when dev-lifecycle reaches Phase 2. Do NOT use for writing code (use dev-lifecycle Phase 3), writing test cases (use test-case-writer), auditing existing code quality (use codebase-auditor), or PR descriptions."
---

# Feature Plan Writer

Produce a plan that is consistent with every earlier plan, concrete enough to code from, and never pushed to GitHub by accident. This skill writes ONLY plan files (and the `.gitignore` line). It never edits source code.

## Ground rules

- Reply in the user's language; write the plan in the same language (keep identifiers in English).
- Anti-hallucination: cite `file:line` for every statement about existing code. Do not name libraries, tables or endpoints that do not exist unless marked **NEW**. Mark unknowns as "Open question", never guess.
- Agent-agnostic: "inspect the repo", "list the files" — use whatever tools your environment has.

## Step 1 — Audit old plans (MANDATORY)

1. Check whether a `plan/` directory exists and list its files.
2. If files exist, read ALL of them. Extract and keep a short internal digest of:
   - overall architecture and module boundaries;
   - naming conventions (files, classes, DB tables/columns, routes);
   - data model / schema;
   - design decisions and constraints (auth approach, error format, state management...).
3. Compare the new request against the digest. If it **contradicts or drifts** from earlier concepts (e.g. new entity duplicates an existing one, different naming, different auth approach, changes a prior contract), STOP and warn the user BEFORE writing:
   - what conflicts, citing the old plan file and section;
   - 2–3 resolution options with a recommendation;
   - ask which direction to lock in. Resume only after the answer.
4. If `plan/` is empty or absent, say so in one line and continue. For brownfield repos with no plans, inspect the code to establish the baseline and note it in "Architecture impact".

## Step 2 — Write the plan

Use this structure (full template with filler hints in the example below). Omit nothing; write "None" where a section does not apply.

```markdown
# <NNN> — <Feature name>
Status: Draft | Approved | In progress | Done
Date: YYYY-MM-DD
Related plans: plan/00X-...md (or "none")

## 1. Goal & Requirements
Goal: <one sentence, user value>
- R1: <testable requirement>
- R2: ...
Out of scope: <explicit exclusions>

## 2. Impact on current architecture / concepts
<What stays consistent, what changes, any decision that differs from older plans and why.
Cite plan/00X section and file:line of existing code.>

## 3. Files to create / modify
| Action | Path | Purpose | Req |
|--------|------|---------|-----|
| create | src/... | ... | R1 |
| modify | src/x.ts:40-80 | ... | R2 |

## 4. DB / API contract changes
<Tables/columns/migrations; endpoints with method, path, request, response, errors.
Mark NEW vs CHANGED; note backward compatibility.>

## 5. Edge cases to block
- <empty input, max length, duplicates, concurrency, unauthorized, offline, timezone...>

## 6. Test plan
| Req | Happy | Boundary | Negative |
|-----|-------|----------|----------|
| R1  | ...   | ...      | ...      |

## 7. Implementation order (vertical slices)
1. Slice 1 — R1: ...
2. Slice 2 — R2: ...

## 8. Open questions / Risks
- ...

## 9. Progress checklist
- [ ] R1  - [ ] R2
```

Quality bar: every R is verifiable by a test; every file in section 3 maps to an R; every R appears in the test plan and in a slice.

## Step 3 — Save the file & configure .gitignore

1. Create `plan/` if missing. Pick the naming scheme already used in `plan/`; if none, default to `plan/NNN-feature-name.md` (zero-padded, next number after the highest existing; kebab-case name). Date style `plan/YYYY-MM-DD-feature-name.md` is acceptable if the user prefers or existing plans use it. Never mix schemes.
2. Do NOT overwrite an existing plan for a different feature. For a change to the same feature, update that file and bump its Status/Date, or create a new numbered plan that references it.
3. Open the repo-root `.gitignore` (create it if absent). If no line equals `plan/` (or `/plan/`), append `plan/` on its own line. Never duplicate it; never remove other entries.
4. Always tell the user, in one short line:

> Đã lưu plan tại `plan/<file>.md` và đưa `plan/` vào `.gitignore` để không đẩy lên GitHub. Nếu bạn muốn chia sẻ hoặc lưu lịch sử plan trên GitHub, chỉ cần xóa dòng `plan/` khỏi `.gitignore`.

(If the user writes in English, give the same sentence in English. If `plan/` was already ignored, say it was already ignored.)

## Step 4 — Hand-off

Summarize in ≤10 lines: requirement list, files touched count, main risks, any open question. Then ask the user to approve. Do not begin implementation; approval and coding belong to the caller (`dev-lifecycle` Phase 2 → 3) or the user. When approved, set the plan's Status to `Approved`.

## Updating plans during implementation

If implementation reveals a needed change, edit the plan first (add a dated line under "Open questions / Risks" or a "Changelog" section), tell the user what changed, and keep the progress checklist current so later sessions inherit accurate context.
