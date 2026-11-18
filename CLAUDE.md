# Timeless Harmony

Nền tảng kết nối dịch vụ cưới tại Việt Nam (đám cưới nhỏ, ký quỹ, trợ lý Harmony AI). Website tĩnh, deploy trên Vercel. Người dùng viết tiếng Việt; nội dung site bằng tiếng Việt.

**Cách làm việc & chọn model: đọc `docs/quy-tac-lam-viec.md`** (Sonnet hằng ngày, Opus advisor, Fable cho việc thiết kế, Haiku tra cứu; tìm trước–đọc ít; nháp để ở scratchpad).

## Cấu trúc

- `*.html` — mỗi trang tự chứa CSS/JS riêng. Không có bước build.
- `theme.css` — **nguồn duy nhất cho màu, phông và chất liệu kính**; nạp sau `<style>` của trang nên luôn thắng.
- `assets/bg/` — hình nền vector (sinh bằng `docs/design/build_background.py`). `assets/brand/` — logo (sinh bằng `docs/logo/build_logo.py` + `node docs/logo/export.js`; không sửa SVG bằng tay).
- `suppliers.js` — nguồn duy nhất cho dữ liệu nhà cung cấp (dữ liệu mẫu). Sửa thì cập nhật `SUPPLIER_LIST` trong `api/chat.js`.
- `api/chat.js` — Vercel Edge Function cho Harmony AI.
- `docs/`, `.claude/`, `CLAUDE.md` — nội bộ, không deploy (`.vercelignore`).

## Thương hiệu "Vườn kính" — bắt buộc

Chi tiết: `docs/brand-guidelines.html` (hình ảnh), `.claude/brand-voice-guidelines.md` (giọng), `docs/marketing-playbook.md`.

- **Nền:** khung cảnh cố định `body::before` (trời + cỏ hoa). `body` luôn trong suốt. Chữ chỉ được nằm trực tiếp trên nền ở khối đầu trang; mọi nội dung khác nằm trong kính.
- **Kính:** khối lớn = tấm kính (tự áp dụng cho `section`, hoặc thêm class `.glass` / `.glass-strong`); thẻ bên trong dùng `var(--card-bg)` + `var(--card-border)`, không thêm `backdrop-filter` (không lồng hai lớp làm mờ).
- **Màu:** chỉ dùng biến trong `theme.css` (`--text`, `--accent`, `--tulip`, `--card-bg`, `--pane`, `--edge`, `--tint-*`…). Mực `#18301F`, lá `#226340`, tulip chữ `#A32545`.
- **Chữ:** `--font-display` Philosopher (tiêu đề, chữ nhấn đặt trong `<em>`), `--font-body` Be Vietnam Pro, `--font-serif` Lora.
- **Chế độ:** sáng là mặc định (`<body class="light">` do script đầu `<body>` gắn); không class = "Đêm vườn". Khoá: `localStorage['th-mode']`.
- **Logo:** màn hình dùng quả cầu màu `logo-orb.svg` / `logo-*-color.svg`; bản nét một màu (`.th-art .th-art-*`, theo `currentColor`) cho in ấn và trên kính đậm.
- **Giọng:** "mình/chúng mình" – "bạn"; "nhà cung cấp", "ký quỹ"; không dùng số liệu hay đánh giá chưa có thật.
- Thẻ `<nav>` chỉ dùng cho thanh menu trên cùng (CSS chung biến nó thành thanh kính nổi).

## Kiểm tra

Không có test trong repo. Trước khi push: `python3 -m http.server`, soát bằng Playwright ở 1280px và 390px, cả sáng/tối; không được có cuộn ngang trên điện thoại. `/api/chat` không chạy ở local (trang Kế hoạch tự dùng câu trả lời mẫu).

## Đang chờ

Xem `docs/can-bo-sung.md`. Việc lớn tiếp theo: lưu dữ liệu form (Supabase), tài khoản, thay dữ liệu mẫu bằng nhà cung cấp thật.
