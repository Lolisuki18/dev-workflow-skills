# Phase Output Templates

Copy the structure, translate headings to the user's language. Replace `<...>`. Keep outputs short.

## Phase 1 — Greenfield question batch

```
[Phase 1/5: Discovery & Clarification]

Để chốt nền tảng, bạn trả lời nhanh (VD: "1A 2B 3A 4A 5C"):

1. Nền tảng?  A) Web (khuyên dùng) B) Mobile C) Desktop D) CLI
2. MVP gồm? A) <tính năng cốt lõi 1> B) <bộ 2–3 tính năng> C) Tôi tự liệt kê
3. Tech stack? A) <stack gợi ý phù hợp ý tưởng> B) <lựa chọn nhẹ hơn> C) Khác
4. Dữ liệu? A) SQLite/file local B) PostgreSQL/MySQL C) Cloud (Firebase/Supabase)
5. Auth & triển khai? A) Chưa cần auth, chạy local B) Email/password C) OAuth, deploy cloud

Mặc định nếu bạn không chọn: 1A 2B 3A 4A 5A.

**Format code:** với stack đã chọn tôi gợi ý <extensions/config>. Bạn có muốn tôi tạo sẵn
`.editorconfig`, `.vscode/extensions.json` và config formatter khi khởi tạo không? (Có/Không)

**Cố vấn chủ động**
- Giải pháp gọn hơn: ...
- Rủi ro: ...
- Nên tái sử dụng: ... (file:line nếu brownfield)

⏸ Dừng tại đây — chờ bạn chốt spec.
```

## Phase 1 — Brownfield findings

```
[Phase 1/5: Discovery & Clarification]

**Đã đọc:** <files> và plan/<old plans>
**Hiện trạng liên quan:** <fact> (src/x.ts:42), <fact> (src/y.ts:10)
**Câu hỏi còn mơ hồ (chỉ những gì code chưa trả lời):**
1. ... A) ... B) ...
**Cố vấn chủ động:** ...
⏸ Chờ bạn chốt spec.
```

## Phase 1 — Spec Summary

```
**Spec đã chốt**
- Mục tiêu: ...
- Phạm vi MVP: ... | Ngoài phạm vi: ...
- Stack: ... | Dữ liệu: ...
- Ràng buộc: ...
```

## Phase 2 — Plan hand-off message

```
[Phase 2/5: Planning]
Plan: plan/001-<name>.md (đã thêm plan/ vào .gitignore)
- Requirements: R1 ..., R2 ..., R3 ...
- File tạo/sửa: <n> file (xem plan)
- Rủi ro chính: ...
⏸ Bạn duyệt plan chứ? Trả lời "ok" / "code đi" để bắt đầu viết code, hoặc nêu chỗ cần sửa.
```

## Phase 3 — Slice report

```
[Phase 3/5: Implementation]
Slice <k>/<n>: R<x> — <title>
- Đã sửa: path/a.ts, path/b.ts
- Chạy: format ✔ | lint ✔ | type-check ✔   (ghi rõ lệnh và kết quả thật)
- Tiếp theo: R<y>
```

## Phase 4 — Traceability table

```
[Phase 4/5: Testing & Verification]
| Req | Code (file:line) | Test | Kết quả |
|-----|------------------|------|---------|
| R1  | src/a.ts:12      | a.test.ts › creates item | PASS |
| R2  | —                | —    | GAP: chưa cài đặt |
Tổng: <pass>/<total> pass. Lệnh chạy: `<cmd>`.
```

## Phase 5 — Wrap-up

```
[Phase 5/5: Final Audit & Wrap-up]
**Đã làm:** ...
**File thay đổi:** ...
**Cách chạy:** `<cmd>`
**Kết quả test:** <pass>/<total>
**Audit nhanh:**
| Mức | Vấn đề | file:line |
|-----|--------|-----------|
**Rủi ro còn lại / nợ kỹ thuật:** ...
**Bước tiếp theo gợi ý:** ...
Lưu ý: plan/ đang được git-ignore; xóa dòng `plan/` khỏi .gitignore nếu muốn đưa lên GitHub.
```
