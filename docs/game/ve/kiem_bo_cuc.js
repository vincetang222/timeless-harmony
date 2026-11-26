// Kiểm bố cục tự động (bo-cuc-canh.md mục 6), 26/11: mọi mẫu, hai nơi, Lễ và Tiệc, 1280 và 390, sáng và tối.
// Đọc window.thBoCuc() của trang thử, báo lỗi khi món che trục nhìn, đứng vào vùng cấm, bị mép cắt, ghế đè lan can, dây đèn thiếu chỗ bám hoặc vắt qua phông.
// Chạy: phục vụ game/lab/xuong (python3 -m http.server 8772), rồi node kiem_bo_cuc.js [địa chỉ trang, mặc định http://localhost:8772/index.html]
const { chromium } = require('playwright');
const giao = (a, b) => a[0] < b[2] && a[2] > b[0] && a[1] < b[3] && a[3] > b[1];
const hop = m => [m.x, m.y, m.x + m.w, m.y + m.h];
function dungCam(cam, x0, y0, x1, y1) { return (cam || []).some(c => { if (c[0] === 'cay' || c[0] === 'cot') { const dx = Math.max(x0 - c[1], 0, c[1] - x1), dy = Math.max(y0 - c[2], 0, c[2] - y1); return dx * dx + dy * dy < c[3] * c[3] - 1e-9; } return x0 < c[3] && x1 > c[1] && y0 < c[4] && y1 > c[2]; }); }
function soat(r, ten) {
  const loi = [];
  r.mon.forEach(m => {
    const b = hop(m);
    if (m.loai === 'ban') {
      if (giao(b, [r.truc[0] + 1, r.truc[1], r.truc[2] - 1, r.truc[3]])) loi.push(`bàn che trục nhìn (${b.map(v => v.toFixed(1))})`);
      if (b[0] < -0.12 * m.w || b[2] > 100 + 0.12 * m.w) loi.push(`bàn bị mép khung cắt quá 12% (${b[0].toFixed(1)}–${b[2].toFixed(1)})`);
      if (m.chanSau < r.sau + 0.4) loi.push(`chân ghế sau (${m.chanSau.toFixed(2)}%) chạm hoặc vượt chân lan can, tường (${r.sau.toFixed(2)}%)`);
      if (m.dat) { const g = m.g, hw = g.hinh === 'tron' ? g.R + 0.55 : 0, hh = hw; if (hw && dungCam(r.cam.filter(c => c[0] !== 'cot' || true), m.dat[0] - hw, m.dat[1] - hh, m.dat[0] + hw, m.dat[1] + hh)) loi.push(`bàn đứng vào vùng cấm ở (${m.dat.map(v => v.toFixed(1))})`);
        if (hw && m.dat[1] - hh < r.le - 1e-6) loi.push('bàn lấn lối đi dọc lan can, tường'); }
      else loi.push('không tìm được chỗ của bàn trên mặt bằng');
    }
    if ((m.loai === 'loa' || m.loai === 'led') && m.dat && Math.abs(m.dat[0]) < 3.5 && m.dat[1] > r.cy - 2.5 && m.dat[1] < r.cy + 1.6) loi.push(`${m.loai} đứng trong khoảng làm lễ`);
    if (m.loai === 'led' && r.canhDep && r.phong && giao(b, r.phong)) loi.push('màn LED che phông cảnh đẹp');
    if ((m.loai === 'loa' || m.loai === 'led') && m.dat) { const rr = m.loai === 'led' ? 1.5 : 0.35; r.mon.filter(t => t.loai === 'ban' && t.dat && t.g.hinh === 'tron').forEach(t => { const R = t.g.R + 0.55; if (Math.abs(t.dat[0] - m.dat[0]) < R + rr && Math.abs(t.dat[1] - m.dat[1]) < R + 0.2) loi.push(`${m.loai} đè lên bàn trên mặt bằng`); }); }
    if (m.loai === 'cot' && giao(b, [r.truc[0], r.truc[1], r.truc[2], r.truc[3]])) loi.push('cột đèn đứng trong trục nhìn');
  });
  r.day.forEach((q, k) => {
    if (!q.neo.every(n => ['cay', 'cot', 'cong'].includes(n))) loi.push(`dây ${k + 1} không có chỗ bám`);
    if (r.phong && q.ds.some(p => p[0] > r.phong[0] && p[0] < r.phong[2] && p[1] > r.phong[1] && p[1] < r.phong[3])) loi.push(`dây ${k + 1} vắt qua phông sau cặp đôi`);
  });
  r.ghe.forEach(g => { if (dungCam(r.cam, g[0] - 0.25, g[1] - 0.25, g[0] + 0.25, g[1] + 0.25)) loi.push(`ghế dự lễ đứng vào vùng cấm (${g.map(v => v.toFixed(1))})`); if (g[1] < r.le) loi.push('ghế dự lễ lấn lối dọc lan can'); });
  return loi.map(l => ten + ': ' + l);
}
(async () => { const b = await chromium.launch(); const errs = [], loi = []; let so = 0;
  for (const [ten, vp, toi] of [['d', { width: 1280, height: 860 }, 0], ['m', { width: 390, height: 760 }, 0], ['dt', { width: 1280, height: 860 }, 1], ['mt', { width: 390, height: 760 }, 1]]) {
    const pg = await b.newPage({ viewport: vp, colorScheme: toi ? 'dark' : 'light' }); pg.on('pageerror', e => errs.push(e.stack));
    await pg.goto(process.argv[2] || 'http://localhost:8772/index.html'); await pg.evaluate(() => localStorage.clear()); await pg.reload(); await pg.waitForTimeout(800);
    await pg.locator('#mo-xuong').click(); await pg.waitForTimeout(600);
    const N = t => pg.locator('section.nhom').filter({ has: pg.locator('h3', { hasText: new RegExp('^' + t + '$') }) });
    const chip = async (g, c) => { await N(g).locator('.loc button:visible', { hasText: c }).first().click(); await pg.waitForTimeout(150); };
    const the = async (g, c) => { await N(g).locator('.o-vuong', { hasText: c }).first().click(); await pg.waitForTimeout(150); };
    const kiem = async n => { const r = await pg.evaluate(() => window.thBoCuc()); so++; loi.push(...soat(r, `${ten} ${n}`)); return r; };
    for (const m of ['Vườn trắng xanh', 'Đêm kim sa', 'Bàn dài gia đình', 'Sân quê đỏ thắm', 'Mộc mạc']) {
      await N('Mẫu có sẵn').locator('button', { hasText: m }).click(); await pg.waitForTimeout(300); await kiem(m);
      if (!(await N('Ánh sáng').locator('button', { hasText: 'Dây đèn' }).getAttribute('aria-pressed') === 'true')) { await chip('Ánh sáng', 'Dây đèn'); await kiem(m + ' + dây đèn'); }
      for (const k of ['50', '200']) { await chip('Số khách', k); await kiem(m + ' ' + k + ' khách'); } await chip('Số khách', '100');
      for (const ban of ['Tròn 6 khách', 'Tròn 12 khách', 'Dài 8 khách', 'Dài 20 khách', 'Dài xếp chéo']) { await the('Bàn tiệc', ban); await kiem(m + ' · ' + ban); }
      await chip('Phần', 'Lễ'); for (const x of ['Thẳng hàng', 'Hình quạt', 'Khối chéo', 'Vòng tròn']) { await chip('Xếp ghế dự lễ', x); await kiem(m + ' · lễ ' + x); } await chip('Phần', 'Tiệc');
    }
    const r = await pg.evaluate(() => ({ cuon: document.documentElement.scrollWidth > window.innerWidth }));
    if (r.cuon) loi.push(ten + ': có cuộn ngang');
    await pg.close();
  }
  console.log(so + ' cảnh đã soát; ' + (loi.length ? loi.length + ' lỗi:\n' + [...new Set(loi)].slice(0, 60).join('\n') : 'không có lỗi bố cục'));
  console.log(errs.join('\n') || 'no errors'); await b.close(); })();
