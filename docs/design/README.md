# Thiết kế "Vườn kính"

- `build_background.py` — vẽ hình nền vector: lễ cưới trong vườn biệt thự bên hồ ở Ý, pháo bông nhiều màu sau cổng hoa (bản ngày và đêm). Sinh SVG nguồn vào `docs/design/.build/` (không commit).
- `render_background.js` — xuất SVG nguồn thành WebP trong `assets/bg/` (bản ngang 2000×1250 và bản dọc `-m` 900×1950 cho điện thoại). Chạy: `python3 docs/design/build_background.py && node docs/design/render_background.js`.
- `og-image.html` — ảnh chia sẻ link 1200×630. Mở bằng Chromium ở khung 1200×630 và chụp thành `og-image.png` ở gốc repo:

```bash
node -e "const{chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1200,height:630}});await p.goto('file://'+process.cwd()+'/docs/design/og-image.html',{waitUntil:'networkidle'});await p.screenshot({path:'og-image.png'});await b.close()})()"
```

Chất liệu kính lỏng (tấm, thẻ, giọt) nằm ở mục 7 của `theme.css`; vệt sáng theo con trỏ ở `liquid.js`; logo ở `docs/logo/`.

Độ đục của kính được đo trên nền cỏ để chữ đạt AA (chữ phụ `#40574A` ≥ 5,2:1, vàng đồng `#765225` ≥ 4,7:1 ở vùng xấu nhất, đo với tấm kính phủ toàn cảnh). Nếu đổi `--pane` hoặc màu cảnh nền, hãy đo lại bằng ảnh chụp thật.
