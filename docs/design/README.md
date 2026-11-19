# Thiết kế "Vườn kính"

## Cảnh nền 3D

Hình nền của website là **một cảnh 3D dựng sẵn thành ảnh tĩnh**: lễ cưới trong vườn biệt thự bên hồ ở Ý. Trình duyệt chỉ tải một ảnh WebP, không chạy 3D. Pháo hoa **không** nằm trong ảnh: nó là chuyển động, vẽ bằng `fireworks.js` khi người xem bấm nút (xem mục "Sân khấu").

- `build_scene3d.py` — dựng cảnh bằng Blender (module `bpy`) và kết xuất bằng Cycles. Mọi thứ sinh bằng mã, không dùng mô hình hay ảnh ngoài: núi và hồ (nhiễu Perlin), làng ven hồ, bãi cỏ (từng lá cỏ), cây bách, hàng rào, lan can đá, cổng hoa, ghế, khách, cô dâu chú rể. Bản đêm thêm trăng, sao, dây đèn, nến và đèn rọi. Thêm `--fireworks` thì vẽ sẵn chùm pháo cầu vồng vào ảnh (chỉ dùng cho ảnh chia sẻ link).
- `post_scene3d.py` — hậu kỳ: sương xa theo khoảng cách, độ sâu trường ảnh, quầng sáng quanh đèn, tông màu AgX, rồi xuất vào `assets/bg/` hai tệp: ảnh nền `lake-<day|night>[-m].webp` và mặt nạ pháo hoa `…-mask.webp`.
- `build_glass.js` — đưa từng ảnh nền qua đúng bộ lọc của tấm kính bằng Chromium, xuất `…-glass.webp` ở 1/4 kích thước (xem mục "Kính lỏng và độ mượt").

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

```bash
node docs/design/build_glass.js
```

Máy 4 nhân mất khoảng 9 phút cho khung ngang và 5 phút cho khung dọc. Xem thử nhanh (khoảng 40 giây): thêm `--scale 0.5 --spp 32`. `bpy` nặng khoảng 1 GB; thư mục `.venv3d/` và `docs/design/.build/` không commit.

Chỉnh ở đâu:

| Muốn đổi | Sửa trong `build_scene3d.py` |
|---|---|
| Góc máy, khung hình | `CAM`, `build_camera()` |
| Hướng và độ cao mặt trời | `SUN_AZ`, `SUN_EL` |
| Hình dáng hồ và núi | `lake_cx()`, `lake_hw()`, `height()` |
| Màu hoa, trang phục khách | `FLOWERS`, `DRESS`, `SUITS` |
| Đèn ban đêm | `build_night_lights()` |
| Độ sáng, sương, quầng sáng | `post_scene3d.py` (`gain`, `D`, `glow`) |

Nếu đổi góc máy hoặc vị trí gốc pháo (`FIRE_O`): sửa các hằng số tương ứng ở cuối `post_scene3d.py`, chạy lại, rồi chép dòng `fireworks.js: oy=… ppm=…` mà nó in ra vào bảng `SCENES` trong `fireworks.js`.

## Sân khấu: ngắm cảnh và pháo hoa

`liquid.js` gắn hai nút nổi ở góc dưới phải của mọi trang (kiểu dáng ở mục 10 của `theme.css`):

- **Bắn pháo hoa** — nội dung trang mờ đi để lộ trọn cảnh, một loạt pháo bắn lên từ sau cổng hoa, hết pháo thì nội dung hiện lại. Bấm liên tiếp được; các lần bấm xoay vòng qua dàn phun cầu vồng, bông cầu, liễu rủ và trái tim.
- **Ngắm cảnh** (hình con mắt) — ẩn nội dung cho tới khi bấm "Quay lại", nhấn Esc hoặc cuộn trang. Lúc này chạm vào đâu trên bầu trời thì một quả pháo nổ ở đó.

`fireworks.js` chỉ được tải ở lần bấm đầu tiên. Nó vẽ lên một `<canvas>` ghim ngay trên ảnh nền, dưới mọi nội dung:

- Tia lửa bay theo vật lý thật (mét, giây), quy đổi ra điểm ảnh bằng thông số máy ảnh của cảnh 3D (bảng `SCENES`), nên pháo đúng tỉ lệ với khu vườn ở mọi cỡ màn hình.
- Mặt nạ `lake-*-mask.webp`: kênh đỏ là những thứ đứng trước pháo (vườn, cổng hoa, cây, khách, dây đèn), pháo bị xoá ở đó nên trông như bay phía sau; kênh lục là mặt hồ, nơi vẽ ánh pháo hắt xuống.
- Canvas chỉ chạy khi còn tia lửa. Máy đuối (nhiều khung hình chậm) thì tự giảm độ phân giải và số tia.

Chỉnh ở đâu trong `fireworks.js`: màu ở `RAINBOW` và `TONES`; kiểu bông ở `burst()`; dàn phun ở `fan()`; thứ tự các loạt ở `volley()`.

## Ảnh chia sẻ link

`og-image.html` — ảnh 1200×630, dùng `og-scene.webp` (cảnh ngày có vẽ sẵn pháo cầu vồng; dựng lại bằng `build_scene3d.py --fireworks` rồi `post_scene3d.py --webp docs/design/og-scene.webp --no-mask`). Mở bằng Chromium ở khung 1200×630 và chụp thành `og-image.jpg` ở gốc repo (JPEG để tệp dưới 200 KB, các ứng dụng nhắn tin mới hiện ảnh xem trước):

```bash
node -e "const{chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1200,height:630}});await p.goto('file://'+process.cwd()+'/docs/design/og-image.html',{waitUntil:'networkidle'});await p.screenshot({path:'og-image.jpg',quality:88});await b.close()})()"
```

## Kính lỏng và độ mượt

Chất liệu kính (tấm, thẻ, giọt) nằm ở mục 7 của `theme.css`; logo ở `docs/logo/`. `liquid.js` lo bốn việc: vệt sáng theo con trỏ, bộ điều tiết độ mượt, kính dựng sẵn, và hai nút sân khấu.

Làm mờ nền trực tiếp (`backdrop-filter`) là phần tốn máy nhất: mỗi khung hình khi cuộn, trình duyệt phải làm mờ lại cảnh sau từng tấm kính. Vì cảnh nền đứng yên, website làm mờ **một lần, từ trước**:

1. **Kính dựng sẵn** (`<html class="pre">`, mục 7b của `theme.css`). `liquid.js` chèn vào mỗi tấm kính lớn một lớp `<i class="gl"><b></b></i>` hiển thị `lake-*-glass.webp` (ảnh nền đã qua đúng bộ lọc của kính), ghim theo khung nhìn (`position: fixed`) và cắt theo hình tấm kính (`clip-path`). Tấm đó thôi dùng `backdrop-filter`. Nhìn như cũ, nhưng khi cuộn trình duyệt chỉ việc ghép lớp. Thanh menu, hộp thoại, bong bóng trò chuyện và giọt kính nhỏ vẫn làm mờ trực tiếp (diện tích nhỏ).
2. **Không lồng hai lớp làm mờ.** Tấm kính đặt biến `--drop: none`; nút, nhãn, ô tìm kiếm bên trong đọc biến này và tự thôi làm mờ.
3. **Điện thoại (≤ 640px)**: giọt kính nhỏ không làm mờ, bù bằng nền đục hơn.
4. **Chế độ nhẹ** (`<html class="lite">`, mục 9 của `theme.css`): bỏ toàn bộ làm mờ và lớp kính dựng sẵn, kính đục hơn. `liquid.js` tự bật khi trình duyệt báo tiết kiệm dữ liệu, máy có RAM ≤ 2 GB, hoặc khi đo thấy cuộn trang dưới khoảng 28 khung hình/giây trong hai lượt đo liên tiếp (ghi nhớ 7 ngày trong `localStorage['th-lite']`).

Ràng buộc của kính dựng sẵn:

- Tấm có lớp `.gl`, và mọi phần tử bao ngoài nó, **không được có `transform`, `filter`, `perspective` hay `will-change`**: các thuộc tính này làm ảnh ghim bám theo phần tử thay vì khung nhìn, ảnh sau kính sẽ lệch khỏi cảnh. `theme.css` đã tắt `transform` trên chính tấm kính và trên hiệu ứng hiện dần `[data-r]` chứa tấm kính. `liquid.js` còn tự đo từng lớp sau khi chèn và khi đổi cỡ cửa sổ: lớp nào không phủ đúng khung nhìn thì bị gỡ, tấm kính đó quay về `backdrop-filter` (đúng hình, chỉ là nặng hơn).
- Tấm kính mới muốn dùng kính dựng sẵn thì thêm bộ chọn của nó vào `PANES` trong `liquid.js`. Không thêm cũng không hỏng: nó làm mờ trực tiếp như trước.
- Đổi `--backdrop` trong `theme.css` thì đổi cùng giá trị trong `build_glass.js` rồi chạy lại.
- Để so sánh hoặc gỡ lỗi, thêm `?glass=live` vào địa chỉ trang: trang dùng lại `backdrop-filter`.

Không đặt animation chuyển động lên phần tử đang làm mờ nền: mỗi khung hình trình duyệt phải làm mờ lại.

Ảnh nền được trình duyệt giữ lại 7 ngày (`vercel.json`, đường dẫn `/assets/bg/`), nên chuyển trang không phải tải lại. Hệ quả: sau khi thay ảnh nền, khách cũ có thể còn thấy ảnh cũ tối đa 7 ngày; muốn đổi ngay thì đổi tên tệp (lần này đã đổi từ `scene-*` sang `lake-*`).

## Tương phản

Độ đục của kính và bộ lọc nền được chỉnh theo số đo trên cảnh thật để chữ đạt AA. Cách đo: phủ một phần tử kính lên toàn cảnh, chụp ảnh, lấy vùng xấu nhất (tối nhất ở chế độ sáng, sáng nhất ở chế độ tối), làm cho tấm kính, thanh menu và giọt kính, ở máy tính, màn hình rộng và điện thoại.

| Vùng xấu nhất, tấm kính | Chữ chính | Chữ phụ | Chữ mờ | Chữ nhấn |
|---|---|---|---|---|
| Chế độ sáng | 10,5 | 7,1 | 5,2 | 4,6 |
| Chế độ tối | 10,1 | 8,1 | 5,8 | 7,3 |

Thấp nhất trên mọi thành phần: 4,6:1 (chữ vàng đồng trên tấm kính và nút phụ, chế độ sáng). Chế độ nhẹ (không làm mờ) cao hơn: từ 5,9:1.

Ở chế độ sáng, bộ lọc của kính có `contrast(.62) brightness(1.24)`: cảnh phía sau kính bị nén tương phản nên vùng tối (hàng bách) không kéo tối tấm kính. Nếu đổi `--pane`, bỏ bộ lọc này, hoặc dựng lại cảnh nền, hãy đo lại.
