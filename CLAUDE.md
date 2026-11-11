# Timeless Harmony

Nền tảng kết nối dịch vụ cưới tại Việt Nam (đám cưới nhỏ, ký quỹ, trợ lý Harmony AI). Website tĩnh, deploy trên Vercel. Người dùng viết tiếng Việt; nội dung site bằng tiếng Việt.

## Cấu trúc

- `*.html` — mỗi trang tự chứa CSS/JS riêng trong `<style>`/`<script>`. Không có bước build.
- `theme.css` — **nguồn duy nhất cho màu và phông**. Nạp sau `<style>` của mỗi trang nên biến ở đây thắng.
- `suppliers.js` — **nguồn duy nhất cho dữ liệu nhà cung cấp** (+ `supplierPriceFrom`, `getSupplier`). Hiện là dữ liệu mẫu.
- `api/chat.js` — Vercel Edge Function cho Harmony AI. Prompt hệ thống nằm ở server; khi sửa `suppliers.js` phải cập nhật `SUPPLIER_LIST` trong file này.
- `assets/brand/` — logo và tulip dạng SVG một màu (`currentColor`), tách từ artwork gốc.
- `docs/`, `.claude/`, `CLAUDE.md` — nội bộ, đã loại khỏi deploy bằng `.vercelignore`.

## Thương hiệu — bắt buộc tuân theo

Đọc trước khi làm giao diện hay viết nội dung:
- `docs/brand-guidelines.html` — logo, màu, chữ, tulip, thành phần giao diện.
- `.claude/brand-voice-guidelines.md` — giọng viết, xưng hô, thuật ngữ.
- `docs/marketing-playbook.md` — định vị, chân dung khách hàng, kế hoạch.

Quy tắc ngắn:
- **Màu:** chỉ dùng biến trong `theme.css` (`--bg`, `--text`, `--accent`, `--tulip`, `--card-bg`, `--tint-*`…). Không viết mã màu trực tiếp trong trang. Nền Vải lanh `#D6CEC1`, mực Rừng `#2F3523`, Tulip `#86432D` chỉ để nhấn.
- **Chữ:** `var(--font-display)` Philosopher cho tiêu đề, `var(--font-body)` Be Vietnam Pro cho giao diện, `var(--font-serif)` Lora cho tagline/trích dẫn. Chữ nhấn trong tiêu đề đặt trong `<em>`.
- **Chế độ sáng là mặc định.** `<body class="light">` do script đầu `<body>` gắn; không có class = chế độ tối "Rừng đêm". Khoá lưu: `localStorage['th-mode']`.
- **Logo/hình vẽ:** dùng class `.th-art .th-art-*` (mask theo `currentColor`). Dưới 64px dùng `logo-compact.svg`.
- **Icon SVG cũ** có `stroke="#c9a96e"` được `theme.css` đổi sang `--icon`; icon mới dùng `stroke="currentColor"`.
- **Giọng:** xưng "mình/chúng mình" – "bạn"; viết "nhà cung cấp" (không "supplier"), "ký quỹ"; không dùng số liệu hay đánh giá chưa có thật.
- Thẻ `<nav>` có CSS chung `position: fixed` — không dùng `<nav>` cho thứ khác ngoài thanh menu trên cùng.

## Kiểm tra

Không có test trong repo. Trước khi push: chạy `python3 -m http.server` ở thư mục gốc và kiểm tra bằng Playwright (đã cài sẵn trong môi trường cloud) ở 1280px và 390px, cả hai chế độ sáng/tối; không được có cuộn ngang trên điện thoại. `/api/chat` không chạy ở local — trang Kế hoạch sẽ tự dùng câu trả lời mẫu.

## Đang chờ

Xem `docs/can-bo-sung.md`. Việc lớn tiếp theo: lưu dữ liệu form (Supabase), tài khoản, thay dữ liệu mẫu bằng nhà cung cấp thật.
