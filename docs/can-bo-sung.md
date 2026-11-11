# Những thứ cần bạn bổ sung

Danh sách này gom mọi thứ website và bộ thương hiệu đang chờ từ bạn. Đánh dấu `[x]` khi xong.

## 1. Thương hiệu

- [ ] **Tệp logo gốc dạng vector** (AI, SVG, EPS hoặc PDF). Hiện logo và tulip được tách từ ảnh 1080px — đủ đẹp cho web, chưa đủ cho in khổ lớn.
      → Đặt vào `assets/brand/`, giữ nguyên tên tệp (`logo-mark.svg`, `logo-lockup.svg`, `logo-wordmark.svg`, `logo-tagline.svg`, `tulip-*.svg`). Website tự cập nhật.
- [ ] **Xác nhận ý nghĩa biểu tượng** (mục 01 của brand guideline): vô cực, hai nụ tulip, vòng tròn T · H.
- [ ] **Xác nhận màu Tulip `#86432D`.** Artwork gốc chỉ có hai màu; đây là màu nhấn được đề xuất thêm. Nếu muốn giữ thuần hai màu: đổi `--th-tulip` trong `theme.css`.
- [ ] **Xác nhận phông chữ** Philosopher / Be Vietnam Pro / Lora, và phông của chữ logo nếu bạn còn nhớ.
- [ ] **Xưng hô:** "chúng mình" hay "chúng tôi" (xem Giọng thương hiệu → Câu hỏi mở).

## 2. Hình ảnh

- [ ] **Ảnh nhà cung cấp** — mỗi hồ sơ 1 ảnh bìa ngang (tối thiểu 1600×1000) + 3–6 ảnh sản phẩm. Hiện đang là nền màu theo hạng mục.
- [ ] **Ảnh bìa 8 bài Cẩm nang** (1200×630). Hiện trang Cẩm nang dùng ảnh ngẫu nhiên từ picsum.photos — nên thay sớm.
- [ ] **Ảnh cặp đôi thật** cho trang chủ và mạng xã hội, kèm văn bản đồng ý.

## 3. Thông tin doanh nghiệp

- [ ] Email liên hệ chính thức (hiện dùng `hello@timeless-harmony.com` — hộp thư này đã hoạt động chưa?).
- [ ] Số điện thoại/Zalo, địa chỉ (nếu muốn hiển thị).
- [ ] Liên kết Instagram, TikTok, Facebook, Zalo OA, Pinterest → thêm vào chân trang.
- [ ] Tên pháp nhân, mã số thuế cho trang Điều khoản (nếu đã có).

## 4. Kỹ thuật

- [ ] **`ANTHROPIC_API_KEY`** trong Vercel → Settings → Environment Variables. Thiếu biến này, Harmony AI chỉ trả lời theo mẫu soạn sẵn.
- [ ] **Chọn project Supabase** (có sẵn hay tạo mới) để lưu form đăng ký nhà cung cấp, form liên hệ và đăng ký nhận tin. Hiện ba form này **chưa lưu dữ liệu**.
- [ ] Kiểm tra tên miền `timeless-harmony.com` đã trỏ về Vercel (sitemap và ảnh chia sẻ đang dùng tên miền này).
- [ ] Công cụ đo lường truy cập (Vercel Analytics, Plausible hoặc Google Analytics).

## 5. Nội dung & dữ liệu

- [ ] **24 hồ sơ nhà cung cấp hiện là dữ liệu mẫu** (kể cả đánh giá, số đám cưới, nhãn "Đã xác minh"). Quyết định: gắn nhãn "minh họa" hay gỡ trước khi quảng bá.
- [ ] 4 bài Cẩm nang đang ghi "Sắp ra mắt": tiền bạc trước khi cưới · đám cưới 50 triệu · 5 buổi hẹn hò · giao tiếp trong hôn nhân.
- [ ] Ba dịch vụ độc đáo "Sắp có" (mùi hương, trải nghiệm khách mời, bản đồ sao): giữ làm lời mời nhà cung cấp, hay bỏ.

## 6. Quyết định marketing (xem mục 15 của playbook)

- [ ] Thành phố ra mắt đầu tiên.
- [ ] Mục tiêu 90 ngày và ngân sách.
- [ ] Ai phụ trách nội dung, tuyển nhà cung cấp, chăm sóc.
