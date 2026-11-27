# Scenario 04 — Plan audit and conflict warning (feature-plan-writer)

**Setup:** repo containing `plan/001-auth.md` that states: JWT in httpOnly cookie, table `users(id, email, password_hash)`, snake_case columns, error format `{ "error": { "code", "message" } }`. `plan/` is NOT yet in `.gitignore`.

**Turn 1 (user):** `Lên plan cho tính năng đăng nhập bằng Google, chưa code. Lưu token vào localStorage cho nhanh, bảng tên là UserAccount.`

Checklist
- MUST: reads `plan/001-auth.md` before writing anything (cites it).
- MUST: warns about the conflicts BEFORE writing the plan: token storage (cookie vs localStorage), table name/naming (`users` snake_case vs `UserAccount`), possibly duplicate user entity.
- MUST: gives 2–3 options with a recommendation and asks which to lock in; does not write the new plan yet.
- MUST: `plan/` is added to `.gitignore` (by the plan-creation call of the script, not by `--check`, which is read-only) without duplicating it.

**Turn 2 (user):** `Theo đề xuất của bạn, giữ cookie và bảng users`

Checklist
- MUST: creates `plan/002-*.md` (next number, not overwriting 001) with R1..Rn, "Related plans: plan/001-auth.md", files/contract/edge cases/test plan.
- MUST: replies with the one-line notice about `.gitignore` and how to remove the line.
- MUST: no source code written; asks for approval.
- SHOULD: references existing code with `file:line` for any claim about current implementation.

**Fail signs:** writes plan before warning, hand-numbers the file wrongly, duplicates `plan/` in `.gitignore`, silently adopts the conflicting concept.
