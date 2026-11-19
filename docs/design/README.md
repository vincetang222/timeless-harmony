# Thiết kế "Vườn kính"

## Cảnh nền 3D

Hình nền của website là **một cảnh 3D dựng sẵn thành ảnh tĩnh**: lễ cưới trong vườn biệt thự bên hồ ở Ý, pháo bông cầu vồng sau cổng hoa. Trình duyệt chỉ tải một ảnh WebP, không chạy 3D, nên trang nhẹ như trước.

- `build_scene3d.py` — dựng cảnh bằng Blender (module `bpy`) và kết xuất bằng Cycles. Mọi thứ sinh bằng mã, không dùng mô hình hay ảnh ngoài: núi và hồ (nhiễu Perlin), làng ven hồ, bãi cỏ (từng lá cỏ), cây bách, hàng rào, lan can đá, cổng hoa, ghế, khách, cô dâu chú rể, pháo bông. Bản đêm thêm trăng, sao, dây đèn, nến và đèn rọi.
- `post_scene3d.py` — hậu kỳ: sương xa theo khoảng cách, quầng sáng quanh pháo bông và đèn, tông màu AgX, rồi xuất WebP vào `assets/bg/`.

Bốn khung hình: `day` / `night` × `land` (2000×1250, máy tính) / `port` (900×1950, điện thoại, tệp có đuôi `-m`).

```bash
python3 -m venv .venv3d
```

```bash
.venv3d/bin/pip install bpy numpy scipy OpenEXR pillow
```

```bash
for m in day night; do for f in land port; do .venv3d/bin/python docs/design/build_scene3d.py --mode $m --frame $f --out docs/design/.build/$m-$f.exr && .venv3d/bin/python docs/design/post_scene3d.py docs/design/.build/$m-$f.exr --mode $m --frame $f; done; done
```

Máy 4 nhân mất khoảng 8 phút cho khung ngang và 5 phút cho khung dọc. Xem thử nhanh (khoảng 40 giây): thêm `--scale 0.5 --spp 32`. `bpy` nặng khoảng 1 GB; thư mục `.venv3d/` và `docs/design/.build/` không commit.

Chỉnh ở đâu:

| Muốn đổi | Sửa trong `build_scene3d.py` |
|---|---|
| Góc máy, khung hình | `CAM`, `build_camera()` |
| Hướng và độ cao mặt trời | `SUN_AZ`, `SUN_EL` |
| Hình dáng hồ và núi | `lake_cx()`, `lake_hw()`, `height()` |
| Màu hoa, trang phục khách | `FLOWERS`, `DRESS`, `SUITS` |
| Pháo bông (độ xoè, số tia, màu) | `build_fireworks()`, `hue()` |
| Đèn ban đêm | `build_night_lights()` |
| Độ sáng, sương, quầng sáng | `post_scene3d.py` (`gain`, `D`, `glow`) |

## Ảnh chia sẻ link

`og-image.html` — ảnh 1200×630. Mở bằng Chromium ở khung 1200×630 và chụp thành `og-image.jpg` ở gốc repo (JPEG để tệp dưới 200 KB, các ứng dụng nhắn tin mới hiện ảnh xem trước):

```bash
node -e "const{chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1200,height:630}});await p.goto('file://'+process.cwd()+'/docs/design/og-image.html',{waitUntil:'networkidle'});await p.screenshot({path:'og-image.jpg',quality:88});await b.close()})()"
```

## Kính lỏng và độ mượt

Chất liệu kính (tấm, thẻ, giọt) nằm ở mục 7 của `theme.css`; vệt sáng theo con trỏ và bộ điều tiết độ mượt ở `liquid.js`; logo ở `docs/logo/`.

Làm mờ nền (`backdrop-filter`) là phần tốn máy nhất, nên có ba quy tắc:

1. **Không lồng hai lớp làm mờ.** Tấm kính đặt biến `--drop: none`; nút, nhãn, ô tìm kiếm bên trong đọc biến này và tự thôi làm mờ.
2. **Điện thoại (≤ 640px)**: giọt kính nhỏ không làm mờ, bù bằng nền đục hơn; tấm kính giảm bán kính mờ còn 16px.
3. **Chế độ nhẹ** (`<html class="lite">`, mục 9 của `theme.css`): bỏ toàn bộ làm mờ, kính đục hơn. `liquid.js` tự bật khi trình duyệt báo tiết kiệm dữ liệu, máy có RAM ≤ 2 GB, hoặc khi đo thấy cuộn trang dưới khoảng 28 khung hình/giây trong hai lượt đo liên tiếp, tức khoảng 2–3 giây cuộn giật (ghi nhớ 7 ngày trong `localStorage['th-lite']`).

Không đặt animation chuyển động lên phần tử đang làm mờ nền: mỗi khung hình trình duyệt phải làm mờ lại.

Ảnh nền được trình duyệt giữ lại 7 ngày (`vercel.json`, đường dẫn `/assets/bg/`), nên chuyển trang không phải tải lại. Hệ quả: sau khi thay ảnh nền, khách cũ có thể còn thấy ảnh cũ tối đa 7 ngày; muốn đổi ngay thì đổi tên tệp.

## Tương phản

Độ đục của kính và bộ lọc nền được chỉnh theo số đo trên cảnh thật để chữ đạt AA. Cách đo: phủ một phần tử kính lên toàn cảnh, chụp ảnh, lấy vùng xấu nhất (tối nhất ở chế độ sáng, sáng nhất ở chế độ tối), làm cho tấm kính, thanh menu và giọt kính, ở cả máy tính và điện thoại.

| Vùng xấu nhất, tấm kính | Chữ chính | Chữ phụ | Chữ mờ | Chữ nhấn |
|---|---|---|---|---|
| Chế độ sáng | 10,6 | 7,1 | 5,2 | 4,65 |
| Chế độ tối | 9,2 | 7,3 | 5,3 | 6,6 |

Thấp nhất trên mọi thành phần: 4,6:1 (chữ vàng đồng trên nút phụ, chế độ sáng). Chế độ nhẹ (không làm mờ) cao hơn: từ 5,9:1.

Ở chế độ sáng, `--backdrop` có `contrast(.62) brightness(1.24)`: cảnh phía sau kính bị nén tương phản nên vùng tối (hàng bách) không kéo tối tấm kính. Nếu đổi `--pane`, bỏ bộ lọc này, hoặc dựng lại cảnh nền, hãy đo lại.
