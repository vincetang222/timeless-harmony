// Xuất PNG/PDF từ các file SVG của logo. Chạy sau build_logo.py:
//   node docs/logo/export.js
// Cần Playwright + Chromium (đã có sẵn trong môi trường cloud).
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', '..');
const KIT = __dirname;
const COLORS = { forest: '#2F3523', ivory: '#F3EEE5', linen: '#D6CEC1' };

const svgFile = (name) => fs.readFileSync(path.join(KIT, 'svg', `${name}.svg`), 'utf8');
const viewBox = (svg) => svg.match(/viewBox="([^"]+)"/)[1].split(/\s+/).map(Number);
const sized = (svg, w, h) => svg.replace('<svg ', `<svg width="${w}" height="${h}" `);

async function png(page, svg, out, width, { bg = null, pad = 0, square = false } = {}) {
  const vb = viewBox(svg);
  const innerW = width - pad * 2;
  const innerH = Math.round(innerW * vb[3] / vb[2]);
  const W = width;
  const H = square ? width : innerH + pad * 2;
  await page.setViewportSize({ width: W, height: H });
  await page.setContent(`<html><body style="margin:0;width:${W}px;height:${H}px;display:flex;align-items:center;justify-content:center;background:${bg || 'transparent'}">${sized(svg, innerW, innerH)}</body></html>`);
  await page.screenshot({ path: out, omitBackground: !bg });
}

async function pdf(page, svg, out, widthMm) {
  const vb = viewBox(svg);
  const hMm = widthMm * vb[3] / vb[2];
  await page.setContent(`<html><head><style>@page{size:${widthMm}mm ${hMm}mm;margin:0}html,body{margin:0}</style></head><body>${sized(svg, `${widthMm}mm`, `${hMm}mm`)}</body></html>`);
  await page.pdf({ path: out, width: `${widthMm}mm`, height: `${hMm}mm`, printBackground: true, pageRanges: '1' });
}

(async () => {
  for (const d of ['png', 'pdf', 'social']) fs.mkdirSync(path.join(KIT, d), { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage();

  // PNG nền trong suốt, hai màu
  const sizes = { 'logo-lockup': 2400, 'logo-horizontal': 2400, 'logo-wordmark': 2400, 'logo-mark': 2000, 'logo-mark-medium': 1200, 'logo-compact': 512 };
  for (const [name, w] of Object.entries(sizes)) {
    for (const c of ['forest', 'ivory']) {
      await png(page, svgFile(`${name}-${c}`), path.join(KIT, 'png', `${name}-${c}.png`), w);
    }
  }

  // PDF vector cho in ấn (màu Rừng)
  await pdf(page, svgFile('logo-lockup-forest'), path.join(KIT, 'pdf', 'logo-lockup-forest.pdf'), 120);
  await pdf(page, svgFile('logo-horizontal-forest'), path.join(KIT, 'pdf', 'logo-horizontal-forest.pdf'), 160);
  await pdf(page, svgFile('logo-mark-forest'), path.join(KIT, 'pdf', 'logo-mark-forest.pdf'), 100);

  // Ảnh đại diện mạng xã hội 1080×1080 (Instagram, Facebook, Zalo cắt tròn)
  await png(page, svgFile('logo-mark-medium-forest'), path.join(KIT, 'social', 'avatar-linen.png'), 1080, { bg: COLORS.linen, pad: 170, square: true });
  await png(page, svgFile('logo-mark-medium-ivory'), path.join(KIT, 'social', 'avatar-forest.png'), 1080, { bg: COLORS.forest, pad: 170, square: true });

  // Biểu tượng cho màn hình chính iPhone: nền vuông (iOS tự bo góc)
  const fav = fs.readFileSync(path.join(ROOT, 'favicon.svg'), 'utf8')
    .replace(/<circle[^>]*\/>/, `<rect width="1000" height="1000" fill="${COLORS.forest}"/>`);
  await page.setViewportSize({ width: 180, height: 180 });
  await page.setContent(`<html><body style="margin:0">${sized(fav, 180, 180)}</body></html>`);
  await page.screenshot({ path: path.join(ROOT, 'apple-touch-icon.png') });

  // Logo vuông cho dữ liệu có cấu trúc (Google cần ảnh raster ≥ 112px)
  await png(page, svgFile('logo-mark-medium-forest'), path.join(ROOT, 'assets', 'brand', 'logo-512.png'), 512);

  // Trang xem trước toàn bộ bộ logo
  const site = (name) => fs.readFileSync(path.join(ROOT, 'assets', 'brand', `${name}.svg`), 'utf8')
    .replace('<svg ', '<svg style="width:100%;height:auto;display:block" ');
  const cell = (name, w, bg, fg, label) => `<figure style="margin:0;background:${bg};color:${fg};border-radius:14px;padding:34px 24px 16px;display:flex;flex-direction:column;align-items:center;justify-content:space-between;gap:18px"><div style="width:${w}px;max-width:100%">${site(name)}</div><figcaption style="font:500 13px system-ui,sans-serif;opacity:.75">${label}</figcaption></figure>`;
  const favSvg = fs.readFileSync(path.join(ROOT, 'favicon.svg'), 'utf8').replace('<svg ', '<svg style="width:100%;height:100%;display:block" ');
  const row = (items) => `<div style="display:flex;gap:18px;align-items:center">${items}</div>`;
  const preview = `<html><body style="margin:0;padding:28px;background:#F3EEE5;font-family:system-ui,sans-serif;color:#2F3523">
    <h1 style="font:600 22px system-ui;margin:0 0 18px">Timeless Harmony — bộ logo vẽ lại</h1>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
      ${cell('logo-lockup', 380, COLORS.linen, COLORS.forest, 'Bản đầy đủ · logo-lockup')}
      ${cell('logo-lockup', 380, COLORS.forest, COLORS.ivory, 'Bản đầy đủ trên nền Rừng')}
      ${cell('logo-horizontal', 480, '#E8E2D7', COLORS.forest, 'Bản ngang · logo-horizontal')}
      ${cell('logo-horizontal', 480, '#1F2618', COLORS.linen, 'Bản ngang trên nền Rừng đêm')}
      ${cell('logo-wordmark', 460, COLORS.linen, COLORS.forest, 'Logo chữ · logo-wordmark')}
      ${cell('logo-infinity', 360, COLORS.linen, COLORS.forest, 'Dấu vô cực riêng · logo-infinity')}
    </div>
    <div style="margin-top:16px;background:#E8E2D7;border-radius:14px;padding:22px;display:flex;gap:34px;align-items:flex-end;flex-wrap:wrap">
      <div><p style="font:500 13px system-ui;margin:0 0 10px;opacity:.75">Biểu tượng đầy đủ · ≥ 120px</p>${row(`<div style="width:160px">${site('logo-mark')}</div><div style="width:120px">${site('logo-mark')}</div>`)}</div>
      <div><p style="font:500 13px system-ui;margin:0 0 10px;opacity:.75">Nét vừa · 48–120px</p>${row(`<div style="width:96px">${site('logo-mark-medium')}</div><div style="width:64px">${site('logo-mark-medium')}</div><div style="width:48px">${site('logo-mark-medium')}</div>`)}</div>
      <div><p style="font:500 13px system-ui;margin:0 0 10px;opacity:.75">Thu nhỏ · dưới 48px</p>${row([40, 32, 24, 16].map((s) => `<div style="width:${s}px">${site('logo-compact')}</div>`).join(''))}</div>
      <div><p style="font:500 13px system-ui;margin:0 0 10px;opacity:.75">Favicon</p>${row([48, 32, 16].map((s) => `<div style="width:${s}px;height:${s}px">${favSvg}</div>`).join(''))}</div>
    </div></body></html>`;
  await page.setViewportSize({ width: 1200, height: 900 });
  await page.setContent(preview);
  await page.screenshot({ path: path.join(KIT, 'preview.png'), fullPage: true });

  // So sánh với artwork gốc, cùng tỉ lệ và vị trí
  const K = 470 / 215.72, CX = 538.39, CY = 473.83;           // 1 px ảnh gốc = K đơn vị logo
  const crop = { x: 230, y: 235, w: 620, h: 625 };
  const vb = [(crop.x - CX) * K + 500, (crop.y - CY) * K + 500, crop.w * K, crop.h * K].map((v) => v.toFixed(1)).join(' ');
  const lock = fs.readFileSync(path.join(ROOT, 'assets', 'brand', 'logo-lockup.svg'), 'utf8').match(/ d="([^"]+)"/)[1];
  const src = 'data:image/jpeg;base64,' + fs.readFileSync(path.join(ROOT, 'assets', 'brand', 'source-coming-soon.jpg')).toString('base64');
  const S = 560;
  const compare = `<html><body style="margin:0;padding:24px;background:#fff;font:500 15px system-ui,sans-serif;color:#2F3523;display:flex;gap:20px">
    <figure style="margin:0"><svg width="${S}" height="${Math.round(S * crop.h / crop.w)}" viewBox="${crop.x} ${crop.y} ${crop.w} ${crop.h}"><image href="${src}" width="1079" height="1077"/></svg><figcaption style="margin-top:8px">Bản gốc (ảnh 1080px)</figcaption></figure>
    <figure style="margin:0"><svg width="${S}" height="${Math.round(S * crop.h / crop.w)}" viewBox="${vb}" style="background:${COLORS.linen}"><path fill="${COLORS.forest}" d="${lock}"/></svg><figcaption style="margin-top:8px">Bản vẽ lại (vector)</figcaption></figure>
  </body></html>`;
  await page.setViewportSize({ width: S * 2 + 68, height: 700 });
  await page.setContent(compare);
  await page.screenshot({ path: path.join(KIT, 'so-sanh-ban-goc.png'), fullPage: true });

  await browser.close();
  console.log('Đã xuất PNG, PDF, ảnh đại diện, apple-touch-icon.png, preview.png và so-sanh-ban-goc.png');
})();
