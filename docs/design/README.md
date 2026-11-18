# Thiết kế "Vườn kính"

- `build_background.py` — vẽ hình nền vector (trời, mây, đồi, thảm cỏ, hoa; bản ngày và đêm) → `assets/bg/`. Đổi màu, mật độ hoa, vị trí mặt trăng ở đầu tệp rồi chạy `python3 docs/design/build_background.py`.
- `og-image.html` — ảnh chia sẻ link 1200×630. Mở bằng Chromium ở khung 1200×630 và chụp thành `og-image.png` ở gốc repo:

```bash
node -e "const{chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1200,height:630}});await p.goto('file://'+process.cwd()+'/docs/design/og-image.html',{waitUntil:'networkidle'});await p.screenshot({path:'og-image.png'});await b.close()})()"
```

Chất liệu kính (tấm, thẻ, nút, ô nhập) nằm ở mục 7 của `theme.css`; logo ở `docs/logo/`.
