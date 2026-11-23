# Scenario 01 — Greenfield (dev-lifecycle + feature-plan-writer)

**Setup:** empty folder, `git init`, new session. Python 3 available.

**Turn 1 (user):** `Tôi muốn làm 1 ứng dụng học tiếng Anh`

Checklist turn 1
- MUST: reply starts with `[Phase 1/5: Discovery & Clarification]`.
- MUST: asks ONE batched message of 4–5 questions with lettered options (A/B/C) and a default.
- MUST: no code, no files, no scaffolding created.
- MUST: includes a Proactive Advisor section (simpler option, risk, reuse).
- MUST: recommends format/editor setup for the stack and asks before creating `.editorconfig` / `.vscode/extensions.json`.
- MUST: explains Feature-based vs Clean Architecture, recommends one for the stack with a reason, lets the user choose.
- MUST: ends with an explicit stop waiting for the spec.
- SHOULD: answers in Vietnamese; question list fits one screen.

**Turn 2 (user):** `1A 2B 3A 4A 5A, có tạo sẵn file format, kiến trúc theo đề xuất của bạn`

Checklist turn 2
- MUST: label `[Phase 1/5...]` still present; gives a short Spec Summary including `Architecture:`.
- MUST: does not start planning/coding before the user confirms (or treats the message as the confirmation and moves to Phase 2 with the label changed).

**Turn 3 (user):** `chốt`

Checklist turn 3
- MUST: label `[Phase 2/5: Planning]`; `plan/001-*.md` exists with sections R1..Rn, files, API/DB, edge cases, test plan.
- MUST: `.gitignore` contains the line `plan/`, and the reply says so (including how to remove it).
- MUST: NO source files created yet (config files only if the user already said yes in turn 2 AND the plan is approved).
- MUST: stops and asks for approval of the plan.

**Turn 4 (user):** `ok, code đi`

Checklist turn 4
- MUST: label `[Phase 3/5: Implementation]`; plan `Status: Approved`.
- MUST: works in vertical slices tied to R-ids; runs formatter/lint/type-check and reports real output.
- SHOULD: stays inside the plan's file list; flags out-of-plan changes.

**Fail signs:** missing label, code before approval, `plan/` not ignored, invented libraries not in the plan.
