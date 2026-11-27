# Phase Output Templates (Phase 1)

Copy the structure, translate headings to the user's language. Replace `<...>`. Keep outputs short.

## Phase 1 — Greenfield question batch

```
[Phase 1/5: Discovery & Clarification]

Để chốt nền tảng, bạn trả lời nhanh (VD: "1A 2B 3A 4A 5C"):

1. Nền tảng?  A) Web (khuyên dùng) B) Mobile C) Desktop D) CLI
2. MVP gồm? A) <tính năng cốt lõi 1> B) <bộ 2–3 tính năng> C) Tôi tự liệt kê
   Mức dự án (level)? A) fresh: đồ án/học tập B) junior: luận văn/portfolio C) mid: production vừa D) senior: production phức tạp
3. Tech stack (chỉ framework/ngôn ngữ, KHÔNG gộp database vì đã có câu 4)? A) <stack gợi ý phù hợp ý tưởng> B) <lựa chọn nhẹ hơn> C) Khác
   (+ sau khi chốt stack: giải thích Feature-based vs Clean Architecture và đề xuất theo
   references/architecture-guide.md, để người dùng chọn)
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
- Level: fresh | junior | mid | senior — <lý do>
- Architecture: <Feature-based | Clean | Hybrid> — <lý do>
```
