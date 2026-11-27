# Phase Output Templates (Phases 2-5)

Copy the structure, translate headings to the user's language. Replace `<...>`. Keep outputs short.

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
