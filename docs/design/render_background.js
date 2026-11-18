// Xuất hình nền WebP từ SVG nguồn (docs/design/.build/scene-*.svg) vào assets/bg/.
//   python3 docs/design/build_background.py && node docs/design/render_background.js
// Mỗi cảnh có hai bản: ngang cho máy tính (2000×1250) và dọc cho điện thoại (900×1950, cắt phần giữa).
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const SRC = path.join(__dirname, '.build');
const OUT = path.resolve(__dirname, '..', '..', 'assets', 'bg');

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage();
  for (const mode of ['day', 'night']) {
    const svg = 'data:image/svg+xml;base64,' + fs.readFileSync(path.join(SRC, `scene-${mode}.svg`)).toString('base64');
    for (const [suffix, w, h, q] of [['', 2000, 1250, 0.8], ['-m', 900, 1950, 0.78]]) {
      const b64 = await page.evaluate(async ({ svg, w, h, q }) => {
        const img = new Image();
        img.src = svg;
        await img.decode();
        const c = document.createElement('canvas');
        c.width = w; c.height = h;
        const scale = Math.max(w / 1600, h / 1000);          // phủ kín, neo đáy, canh giữa
        const dw = 1600 * scale, dh = 1000 * scale;
        c.getContext('2d').drawImage(img, (w - dw) / 2, h - dh, dw, dh);
        return c.toDataURL('image/webp', q).split(',')[1];
      }, { svg, w, h, q });
      const file = path.join(OUT, `scene-${mode}${suffix}.webp`);
      fs.writeFileSync(file, Buffer.from(b64, 'base64'));
      console.log(path.basename(file), Math.round(fs.statSync(file).size / 1024) + ' KB');
    }
  }
  await browser.close();
})();
