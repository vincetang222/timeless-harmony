# Bộ logo Timeless Harmony

Logo được **vẽ lại thành vector** (tháng 11, 2026) từ artwork gốc `assets/brand/source-coming-soon.jpg`, giữ đúng bố cục và tỉ lệ. Xem `so-sanh-ban-goc.png` để đối chiếu, `preview.png` để xem toàn bộ.

## Dùng tệp nào

| Nhu cầu | Tệp |
|---|---|
| In ấn (thiệp, bao bì, bảng hiệu) | `pdf/logo-lockup-forest.pdf`, `pdf/logo-horizontal-forest.pdf`, `pdf/logo-mark-forest.pdf` — vector, phóng bao nhiêu cũng nét |
| Gửi designer, Canva, Figma | `svg/*-forest.svg` (màu Rừng) hoặc `svg/*-ivory.svg` (màu Ngà, cho nền tối) |
| Word, PowerPoint, email, web không hỗ trợ SVG | `png/*.png` — nền trong suốt |
| Ảnh đại diện Instagram, Facebook, Zalo | `social/avatar-linen.png` hoặc `social/avatar-forest.png` (1080×1080) |
| Chữ ký email | `png/logo-horizontal-forest.png`, hiển thị rộng 200px |
| Website | `assets/brand/*.svg` (dùng `currentColor`, tự đổi màu theo chữ) |

## Các phiên bản

- **logo-lockup**: bản đầy đủ (biểu tượng, chữ, tagline). Ưu tiên dùng. Rộng ≥ 150px hoặc ≥ 32mm.
- **logo-horizontal**: bản ngang, dùng biểu tượng nét vừa. Rộng ≥ 200px hoặc ≥ 45mm.
- **logo-mark**: biểu tượng đầy đủ có chữ T, H. Từ 120px (25mm) trở lên.
- **logo-mark-medium**: biểu tượng nét vừa, không có T, H. Cỡ 48–120px.
- **logo-compact**: bản thu nhỏ, nét dày. Dưới 48px (thanh menu, favicon).
- **logo-wordmark** và **logo-tagline**: chữ "TIMELESS HARMONY" và "hold us together".
- **logo-infinity**: riêng dấu vô cực có nụ tulip, dùng làm hoạ tiết hoặc dấu ngắt đoạn.

Màu chỉ có hai: **Rừng `#2F3523`** trên nền sáng, **Ngà `#F3EEE5`** hoặc **Vải lanh `#D6CEC1`** trên nền tối.

## Cấu trúc

- Dấu vô cực là **một nét liền, không cắt nhau**. Hai đầu nét nở thành hai nụ tulip giống hệt nhau. Cả hình đối xứng khi xoay 180°.
- Nét mảnh ở hai nụ, đầy dần về điểm giữa.
- Vòng tròn ngắt ở hai bên cho chữ T và H. Nét đứng của T, H bằng độ dày vòng tròn; nét ngang bằng nét viền cánh hoa.
- Chữ logo dùng **Belleza**, làm đậm nhẹ cho khớp artwork gốc. Tagline dùng **Lora** độ đậm 540. Cả hai phông theo giấy phép SIL Open Font License và đã chuyển thành đường nét, nên mở tệp không cần cài phông. Belleza không có dấu tiếng Việt: chỉ dùng trong logo.

## Dựng lại

Các tệp được sinh bằng script; không sửa SVG bằng tay.

```bash
pip install fonttools brotli skia-pathops uharfbuzz numpy scipy
mkdir -p /tmp/fonts && cd /tmp/fonts && npm pack @fontsource/belleza @fontsource-variable/lora && for f in *.tgz; do mkdir -p "${f%.tgz}" && tar xzf "$f" -C "${f%.tgz}"; done && cd -
python3 docs/logo/build_logo.py --fonts /tmp/fonts   # SVG: assets/brand/, docs/logo/svg/, favicon.svg
node docs/logo/export.js                             # PNG, PDF, ảnh đại diện, apple-touch-icon.png, ảnh xem trước
python3 docs/build_brand_guidelines.py .             # cập nhật docs/brand-guidelines.html
```

Mọi thông số (độ dày nét, kích thước nụ, khoảng cách chữ) nằm ở đầu `build_logo.py`.
