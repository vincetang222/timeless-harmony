# Timeless Harmony

Nền tảng kết nối dịch vụ cưới tại Việt Nam (đám cưới nhỏ, ký quỹ, trợ lý Harmony AI). Website tĩnh, deploy trên Vercel. Người dùng viết tiếng Việt; nội dung site bằng tiếng Việt.

**Cách làm việc & chọn model: đọc `docs/quy-tac-lam-viec.md`** (Sonnet hằng ngày, Opus advisor, Fable cho việc thiết kế, Haiku tra cứu; tìm trước–đọc ít; nháp để ở scratchpad).

## Cấu trúc

- `*.html` — mỗi trang tự chứa CSS/JS riêng. Không có bước build.
- `theme.css` — **nguồn duy nhất cho màu, phông và chất liệu kính**; nạp sau `<style>` của trang nên luôn thắng. `liquid.js` — vệt sáng theo con trỏ trên kính và bộ điều tiết độ mượt (mọi trang đều nạp).
- `assets/bg/` — hình nền WebP: cảnh 3D dựng sẵn bằng Blender (`docs/design/build_scene3d.py` rồi `post_scene3d.py`, cách chạy ở `docs/design/README.md`; bản `-m` cho điện thoại). Trình duyệt chỉ tải ảnh tĩnh, không chạy 3D. `assets/brand/` — logo (sinh bằng `docs/logo/build_logo.py` + `node docs/logo/export.js`; không sửa SVG bằng tay).
- `suppliers.js` — nguồn duy nhất cho dữ liệu nhà cung cấp (dữ liệu mẫu). Sửa thì cập nhật `SUPPLIER_LIST` trong `api/chat.js`.
- `api/chat.js` — Vercel Edge Function cho Harmony AI.
- `docs/`, `.claude/`, `CLAUDE.md` — nội bộ, không deploy (`.vercelignore`).

## Thương hiệu "Vườn kính" — bắt buộc

Chi tiết: `docs/brand-guidelines.html` (hình ảnh), `.claude/brand-voice-guidelines.md` (giọng), `docs/marketing-playbook.md`.

- **Nền:** khung cảnh 3D cố định `body::before`: lễ cưới trong vườn biệt thự bên hồ ở Ý, pháo bông cầu vồng sau cổng hoa (bản đêm cho chế độ tối). `body` luôn trong suốt. **Không đặt chữ trực tiếp lên cảnh**: mọi nội dung, kể cả khối tiêu đề đầu trang, nằm trong kính.
- **Kính lỏng, ba cấp:** TẤM = khối lớn (tự áp dụng cho `section`, hoặc class `.glass` / `.glass-strong`); THẺ bên trong dùng `var(--card-bg)` + `var(--card-border)`, không thêm `backdrop-filter`; GIỌT = thanh menu, nút, ô tìm kiếm, nhãn (viên nang, class `.liquid`). Viền bắt sáng dùng `var(--rim)`.
- **Mượt:** làm mờ nền là phần tốn máy nhất. Không lồng hai lớp làm mờ (tấm đặt `--drop: none`, giọt bên trong dùng `backdrop-filter: var(--drop, …)`); không đặt animation chuyển động lên phần tử đang làm mờ; không thêm 3D/video chạy thật vào nền. `html.lite` (mục 9 `theme.css`) là chế độ nhẹ, `liquid.js` tự bật khi máy yếu: thành phần mới phải đọc được cả khi không có làm mờ.
- **Tương phản:** độ đục của kính và bộ lọc nền (`--backdrop` có `contrast(.62)` để vùng tối như hàng bách sáng lên sau kính) đã đo trên cảnh thật để chữ đạt AA (thấp nhất 4,6:1). Không giảm alpha của `--pane`, không bỏ `contrast()` hay dựng lại cảnh nền mà không đo lại.
- **Màu:** chỉ dùng biến trong `theme.css` (`--text`, `--accent`, `--tulip`, `--card-bg`, `--pane`, `--edge`, `--tint-*`…). Mực ngọc lục `#12261C`, nút ngọc lục `#1E5A40`, vàng đồng `#765225` cho chữ nhấn/liên kết/icon, champagne `#C7A262` chỉ để trang trí. Hồng tulip chỉ nằm trong hình vẽ và logo.
- **Chữ:** `--font-display` Cormorant Garamond (tiêu đề; chữ nhấn đặt trong `<em>` → nghiêng, ánh vàng), `--font-body` Be Vietnam Pro, `--font-serif` Lora.
- **Chế độ:** sáng là mặc định (`<body class="light">` do script đầu `<body>` gắn); không class = "Đêm vườn". Khoá: `localStorage['th-mode']`.
- **Logo:** màn hình dùng quả cầu ngọc lục – vàng `logo-orb.svg` / `logo-*-color.svg`; bản nét một màu (`.th-art .th-art-*`, theo `currentColor`) cho in ấn và trên kính đậm.
- **Giọng:** "mình/chúng mình" – "bạn"; "nhà cung cấp", "ký quỹ"; không dùng số liệu hay đánh giá chưa có thật.
- Thẻ `<nav>` chỉ dùng cho thanh menu trên cùng (CSS chung biến nó thành thanh kính nổi).

## Kiểm tra

Không có test trong repo. Trước khi push: `python3 -m http.server`, soát bằng Playwright ở 1280px và 390px, cả sáng/tối; không được có cuộn ngang trên điện thoại. `/api/chat` không chạy ở local (trang Kế hoạch tự dùng câu trả lời mẫu).

## Đang chờ

Xem `docs/can-bo-sung.md`. Việc lớn tiếp theo: lưu dữ liệu form (Supabase), tài khoản, thay dữ liệu mẫu bằng nhà cung cấp thật.
