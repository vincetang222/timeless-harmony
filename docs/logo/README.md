# Bộ logo Timeless Harmony

Logo được **vẽ lại thành vector** (tháng 11, 2026) từ artwork gốc `assets/brand/source-coming-soon.jpg`, giữ đúng bố cục và tỉ lệ. Xem `so-sanh-ban-goc.png` để đối chiếu, `preview.png` để xem toàn bộ.

## Dùng tệp nào

| Nhu cầu | Tệp |
|---|---|
| Màn hình, mạng xã hội, tài liệu màu | `png/logo-lockup-color.png`, `png/logo-horizontal-color.png`, `png/logo-orb.png` (bản `-light` cho nền tối) |
| In màu | `pdf/logo-lockup-color.pdf`, `pdf/logo-horizontal-color.pdf`, `pdf/logo-orb.pdf` — vector |
| In một màu, khắc, dập nổi | `pdf/*-ink.pdf`, `svg/*-ink.svg` (mực lá `#18301F`), `svg/*-white.svg` (trắng) |
| Gửi designer, Canva, Figma | thư mục `svg/` |
| Ảnh đại diện Instagram, Facebook, Zalo | `social/avatar-orb.png` (1080×1080, tràn khung) |
| Chữ ký email | `png/logo-horizontal-color.png`, hiển thị rộng 200px |
| Website | `assets/brand/*.svg` |

## Các phiên bản

- **logo-orb**: quả cầu trời–cỏ, dấu vô cực trắng, nụ tulip hồng. Dùng được từ 16px. Đây là biểu tượng chính.
- **logo-lockup-color / logo-horizontal-color**: quả cầu + chữ (dọc / ngang); bản `-light` chữ trắng cho nền tối.
- **logo-infinity-color**: dấu vô cực thân mực, nụ hồng, nền trong suốt — đặt trên kính sáng.
- **Bản nét một màu** (vẽ lại đúng artwork gốc): `logo-lockup`, `logo-horizontal`, `logo-mark` (≥ 120px), `logo-mark-medium` (48–120px), `logo-compact` (< 48px), `logo-wordmark`, `logo-tagline`, `logo-infinity`.

Màu: gradient quả cầu `#2F7FD6 → #57ADE2 → #55B77A → #2F8F55`; mực `#18301F`; nụ tulip `#E0567A`.

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
