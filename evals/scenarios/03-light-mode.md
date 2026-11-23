# Scenario 03 — Light mode (dev-lifecycle sizing)

**Setup:** any small repo with tests and a lint/format command, new session.

## 3a — Trivial
**User:** `Sửa lỗi chính tả "recieve" thành "receive" trong README.md`
- MUST: makes the edit directly; no questionnaire, no `plan/` file, no `[Phase X/5]` label.
- MUST: reports what changed in a line or two.
- FAIL: any plan file, any multi-question message.

## 3b — Small
**User:** `Thêm validate độ dài tối đa 50 ký tự cho trường tên trong form đăng ký`
Two acceptable behaviors (a one-function change sits on the line between "trivial" and "small", and dev-lifecycle's description excludes trivial edits, so the skill may legitimately not trigger):
- (a) No skill triggers: the agent edits directly. MUST: adds boundary tests at 50/51, runs them and reports real results, creates no `plan/` file and no questionnaire.
- (b) dev-lifecycle triggers in light mode: MUST show a 3–5 bullet mini-plan (label `[Light mode]` or a one-line note), wait for "ok", then implement and test as above.
- FAIL: full 5-phase flow, a `plan/` file, or a multi-question batch for this size of change.
- SHOULD: asks the size question only if genuinely ambiguous.

## 3c — Grows beyond light
**User (after 3b):** `Thêm luôn bảng lịch sử đăng ký, API lọc theo ngày, và phân quyền admin`
- MUST: recognizes the size change and switches to the full flow (Phase 1 label or explicit statement), not continuing in light mode.

## 3d — Force modes
- `chạy đủ quy trình` on a trivial task → MUST run the full 5 phases.
- `làm nhanh thôi` on a large task → MUST use light mode but may warn about risk once.
