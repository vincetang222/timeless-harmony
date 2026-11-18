// Xuất PNG/PDF từ các file SVG của logo. Chạy sau build_logo.py:
//   node docs/logo/export.js
// Cần Playwright + Chromium (đã có sẵn trong môi trường cloud).
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', '..');
const KIT = __dirname;
const INK = '#18301F';
const SKY = 'linear-gradient(180deg,#6DB5EE 0%,#9CD0F5 40%,#CFE9FA 75%,#DDF1E2 100%)';

const kit = (name) => fs.readFileSync(path.join(KIT, 'svg', `${name}.svg`), 'utf8');
const site = (name) => fs.readFileSync(path.join(ROOT, 'assets', 'brand', `${name}.svg`), 'utf8');
const viewBox = (svg) => svg.match(/viewBox="([^"]+)"/)[1].split(/\s+/).map(Number);
const sized = (svg, w, h) => svg.replace('<svg ', `<svg width="${w}" height="${h}" `);
const fluid = (svg) => svg.replace('<svg ', '<svg style="width:100%;height:auto;display:block" ');

async function png(page, svg, out, width, { bg = null } = {}) {
  const vb = viewBox(svg);
  const H = Math.round(width * vb[3] / vb[2]);
  await page.setViewportSize({ width, height: H });
  await page.setContent(`<html><body style="margin:0;background:${bg || 'transparent'}">${sized(svg, width, H)}</body></html>`);
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
  const P = (...a) => path.join(KIT, ...a);

  // Bản màu (quả cầu): PNG nền trong suốt
  const color = { 'logo-orb': 1024, 'logo-lockup-color': 1600, 'logo-lockup-color-light': 1600, 'logo-horizontal-color': 2000, 'logo-horizontal-color-light': 2000 };
  for (const [name, w] of Object.entries(color)) await png(page, kit(name), P('png', `${name}.png`), w);
  // Bản một màu: mực lá / trắng
  const mono = { 'logo-lockup': 2400, 'logo-horizontal': 2400, 'logo-wordmark': 2400, 'logo-mark': 2000, 'logo-mark-medium': 1200, 'logo-compact': 512 };
  for (const [name, w] of Object.entries(mono)) for (const c of ['ink', 'white']) await png(page, kit(`${name}-${c}`), P('png', `${name}-${c}.png`), w);

  // PDF vector cho in ấn
  await pdf(page, kit('logo-lockup-color'), P('pdf', 'logo-lockup-color.pdf'), 120);
  await pdf(page, kit('logo-horizontal-color'), P('pdf', 'logo-horizontal-color.pdf'), 160);
  await pdf(page, kit('logo-orb'), P('pdf', 'logo-orb.pdf'), 100);
  await pdf(page, kit('logo-lockup-ink'), P('pdf', 'logo-lockup-ink.pdf'), 120);
  await pdf(page, kit('logo-horizontal-ink'), P('pdf', 'logo-horizontal-ink.pdf'), 160);
  await pdf(page, kit('logo-mark-ink'), P('pdf', 'logo-mark-ink.pdf'), 100);

  // Ảnh đại diện mạng xã hội (tràn khung, tự cắt tròn), icon iPhone, logo vuông cho Google
  await png(page, kit('app-icon'), P('social', 'avatar-orb.png'), 1080);
  await png(page, kit('app-icon'), path.join(ROOT, 'apple-touch-icon.png'), 180);
  await png(page, kit('logo-orb'), path.join(ROOT, 'assets', 'brand', 'logo-512.png'), 512);

  // Trang xem trước toàn bộ bộ logo
  const cell = (svg, w, bg, fg, label) => `<figure style="margin:0;background:${bg};color:${fg};border-radius:22px;padding:34px 24px 16px;display:flex;flex-direction:column;align-items:center;justify-content:space-between;gap:18px;border:1px solid rgba(255,255,255,.8)"><div style="width:${w}px;max-width:100%">${fluid(svg)}</div><figcaption style="font:500 13px system-ui,sans-serif;opacity:.8">${label}</figcaption></figure>`;
  const row = (items) => `<div style="display:flex;gap:18px;align-items:center">${items}</div>`;
  const box = (svg, s) => `<div style="width:${s}px">${fluid(svg)}</div>`;
  const glass = 'rgba(255,255,255,.6)';
  const preview = `<html><body style="margin:0;padding:28px;background:${SKY};font-family:system-ui,sans-serif;color:${INK}">
    <h1 style="font:600 22px system-ui;margin:0 0 18px">Timeless Harmony — bộ logo "Vườn kính"</h1>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
      ${cell(kit('logo-lockup-color'), 330, glass, INK, 'Bản đầy đủ · logo-lockup-color')}
      ${cell(kit('logo-lockup-color-light'), 330, '#0E2233', '#fff', 'Trên nền tối · logo-lockup-color-light')}
      ${cell(kit('logo-horizontal-color'), 470, glass, INK, 'Bản ngang · logo-horizontal-color')}
      ${cell(kit('logo-horizontal-color-light'), 470, '#123A2B', '#fff', 'Bản ngang trên nền tối')}
      ${cell(site('logo-infinity-color'), 330, glass, INK, 'Dấu vô cực màu · logo-infinity-color')}
      ${cell(kit('logo-lockup-ink'), 300, '#fff', INK, 'Bản một màu (in, khắc, dập nổi) · logo-lockup-ink')}
    </div>
    <div style="margin-top:16px;background:${glass};border:1px solid rgba(255,255,255,.8);border-radius:22px;padding:22px;display:flex;gap:40px;align-items:flex-end;flex-wrap:wrap">
      <div><p style="font:500 13px system-ui;margin:0 0 10px;opacity:.8">Quả cầu · mọi cỡ từ 16px</p>${row([160, 96, 64, 40, 32, 24, 16].map((s) => box(kit('logo-orb'), s)).join(''))}</div>
      <div><p style="font:500 13px system-ui;margin:0 0 10px;opacity:.8">Biểu tượng nét (một màu)</p>${row(box(kit('logo-mark-ink'), 130) + box(kit('logo-mark-medium-ink'), 72) + box(kit('logo-compact-ink'), 32))}</div>
      <div><p style="font:500 13px system-ui;margin:0 0 10px;opacity:.8">Biểu tượng ứng dụng</p>${row(`<div style="width:96px;border-radius:22px;overflow:hidden">${fluid(kit('app-icon'))}</div>`)}</div>
    </div></body></html>`;
  await page.setViewportSize({ width: 1200, height: 900 });
  await page.setContent(preview);
  await page.screenshot({ path: P('preview.png'), fullPage: true });

  // So sánh bản nét một màu với artwork gốc, cùng tỉ lệ và vị trí
  const K = 470 / 215.72, CX = 538.39, CY = 473.83;           // 1 px ảnh gốc = K đơn vị logo
  const crop = { x: 230, y: 235, w: 620, h: 625 };
  const vb = [(crop.x - CX) * K + 500, (crop.y - CY) * K + 500, crop.w * K, crop.h * K].map((v) => v.toFixed(1)).join(' ');
  const lock = site('logo-lockup').match(/ d="([^"]+)"/)[1];
  const src = 'data:image/jpeg;base64,' + fs.readFileSync(path.join(ROOT, 'assets', 'brand', 'source-coming-soon.jpg')).toString('base64');
  const S = 560, SH = Math.round(S * crop.h / crop.w);
  const compare = `<html><body style="margin:0;padding:24px;background:#fff;font:500 15px system-ui,sans-serif;color:${INK};display:flex;gap:20px">
    <figure style="margin:0"><svg width="${S}" height="${SH}" viewBox="${crop.x} ${crop.y} ${crop.w} ${crop.h}"><image href="${src}" width="1079" height="1077"/></svg><figcaption style="margin-top:8px">Bản gốc (ảnh 1080px)</figcaption></figure>
    <figure style="margin:0"><svg width="${S}" height="${SH}" viewBox="${vb}" style="background:#D6CEC1"><path fill="#2F3523" d="${lock}"/></svg><figcaption style="margin-top:8px">Bản nét vẽ lại (vector)</figcaption></figure>
  </body></html>`;
  await page.setViewportSize({ width: S * 2 + 68, height: 700 });
  await page.setContent(compare);
  await page.screenshot({ path: P('so-sanh-ban-goc.png'), fullPage: true });

  await browser.close();
  console.log('Đã xuất PNG, PDF, ảnh đại diện, apple-touch-icon.png, logo-512.png, preview.png, so-sanh-ban-goc.png');
})();
