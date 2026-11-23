# Trigger tests

Send each prompt in a fresh session inside a small repo (or empty folder where noted). Expected = the ONLY skill that should activate. `none` = no workflow skill should activate; the agent just answers or makes the small edit.

| # | Prompt | Context | Expected |
|---|--------|---------|----------|
| 1 | Tôi muốn làm 1 ứng dụng học tiếng Anh | empty folder | dev-lifecycle |
| 2 | I want to build a habit tracker app | empty folder | dev-lifecycle |
| 3 | Thêm tính năng đăng nhập bằng Google cho app này | existing web app | dev-lifecycle |
| 4 | Lên plan cho tính năng giỏ hàng, chưa code | existing repo | feature-plan-writer |
| 5 | Write a plan for adding CSV export, don't implement yet | existing repo | feature-plan-writer |
| 6 | Viết test case cho hàm tính tiền trong `cart.ts` | repo with tests | test-case-writer |
| 7 | Add unit tests covering edge cases for `validateEmail` | repo with tests | test-case-writer |
| 8 | Audit giúp tôi codebase này | existing repo | codebase-auditor |
| 9 | Is this repo production ready? Check security and tech debt | existing repo | codebase-auditor |
| 10 | Debug giúp tôi: bấm Lưu thì báo lỗi 500 | repo with a bug | bug-investigator |
| 11 | Why is this test failing intermittently? | repo with flaky test | bug-investigator |
| 12 | Sửa lỗi chính tả "recieve" thành "receive" trong README | any | none (trivial edit) |
| 13 | Đổi tên biến `tmp` thành `total` trong `cart.ts` | any | none (light mode, at most dev-lifecycle light mode) |
| 14 | Giải thích hàm này làm gì | any | none |
| 15 | Đổi màu nút Submit sang xanh lá | existing UI | none (light mode) |
| 16 | Review PR này giúp tôi (dán diff) | any | none from this repo (belongs to pr-review-writer) |
| 17 | Fix bug khiến đơn hàng bị tính tiền hai lần | repo with bug | bug-investigator (NOT dev-lifecycle) |
| 18 | Tìm hết lỗi trong cả dự án | existing repo | codebase-auditor (NOT bug-investigator) |
| 19 | Refactor module `billing` cho gọn, đừng đổi hành vi | repo with tests | refactor-planner |
| 20 | Split this 600-line `OrderService` class safely | repo with tests | refactor-planner |
| 21 | Kiểm tra bảo mật phần đăng nhập và phân quyền | existing repo | security-reviewer |
| 22 | Is this endpoint vulnerable to injection or IDOR? | existing repo | security-reviewer (NOT codebase-auditor) |
| 23 | Thêm cột `phone` vào bảng users mà không downtime | repo with migrations | migration-writer |
| 24 | Upgrade this project from Spring Boot 2.7 to 3.x | existing repo | migration-writer |
| 25 | Giải thích repo này cho tôi, bắt đầu đọc từ đâu | unfamiliar repo | code-explainer |
| 26 | Walk me through how a login request flows through this code | existing repo | code-explainer |
| 27 | Viết GitHub Actions chạy test và Dockerfile cho dự án này | existing repo | ci-cd-setup |
| 28 | CI trên PR của tôi bị đỏ, xem log giúp | PR with failing check | none from this repo (belongs to ci-failure-triager in pull-request-skills) |

## Pass criteria

- Rows 1–11, 17–27: the expected skill activates and no other workflow skill competes with it.
- Rows 12–16 and 28: no phase label, no plan file, no questionnaire. Trivial edits are done directly (row 13 and 15 may show a one-line "light mode" note).

## Record

For any miss note the prompt, what activated instead, and whether the description's trigger keywords or its "Do NOT use for" clause needs adjusting.
