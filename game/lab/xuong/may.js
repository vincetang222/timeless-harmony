/* Máy dựng nhân vật cho "Về chung một nhà": ghép các lớp tranh vẽ tay, nắn dáng, đổi màu, vẽ vào cảnh.
   Không chứa giao diện. Mọi thứ ở đây chạy trong trình duyệt, không gọi dịch vụ ngoài.

   Cách giữ cho nhẹ:
   - mỗi lớp (thân, đầu, cổ áo) được dựng và nhớ riêng, đổi tóc không phải dựng lại thân;
   - mặt nạ da, tóc tính một lần cho mỗi tranh rồi nhớ lại; đổi màu da, đánh sáng dùng phép ghép có sẵn của canvas;
   - thẻ hình nhỏ dựng từ một tấm ghép cỡ nhỏ (nv/nho-*.webp), không phải tải từng tranh nét. */
var NV = (function () {
  'use strict';

  var META = { nam: { w: 594, h: 1300, hdau: 701, dinh: 0.0083, cx: 0.5424 }, nu: { w: 751, h: 1300, hdau: 697, dinh: 0.0315, cx: 0.5013 } };
  var MANH = null, khiDoi = function () {};

  var CHON = {
    vb: { manh: 'Mảnh', vua: 'Vừa', day: 'Đầy đặn' },
    dang: { nam: { can: 'Cân đối', vairong: 'Vai rộng, eo gọn', vaibung: 'Vai rộng, có bụng', bung: 'Vai xuôi, có bụng', hong: 'Vai hẹp, hông rộng', tron: 'To chắc' },
      nu: { can: 'Cân đối', dongho: 'Eo thon', vairong: 'Vai rộng', hong: 'Hông rộng', bung: 'Có bụng', tron: 'Đầy đặn đều' } },
    mat: { goc: 'Trái xoan', tron: 'Tròn', vuong: 'Vuông' },
    mt: { hanh: 'Hạnh nhân', motmi: 'Một mí', to: 'To tròn', phuong: 'Phượng' },
    may: { manh: 'Mảnh, cong', tunhien: 'Tự nhiên', dam: 'Đậm, ngang' },
    toc: { nam: { goc: 'Rẽ ngôi', vuot: 'Vuốt ngược', xoan: 'Xoăn ngắn' }, nu: { goc: 'Búi cao', dai: 'Dài thẳng', ngan: 'Ngang cằm' } },
    ao: { nam: { vest: 'Vest ngọc lục', aodai: 'Áo dài gấm' }, nu: { vest: 'Váy cưới', aodai: 'Áo dài đỏ' } }
  };
  // Bảng màu: đổi màu không đổi hình. Da: màu đích cho vùng da trung bình. Tóc, mắt: ba nấc tối, vừa, sáng.
  var DA = { goc: { ten: 'Như tranh vẽ', m: null }, trang: { ten: 'Trắng hồng', m: [246, 214, 196] }, sang: { ten: 'Sáng', m: [240, 205, 170] }, trung: { ten: 'Trung bình', m: [222, 176, 134] },
    ngam: { ten: 'Ngăm', m: [190, 138, 98] }, nau: { ten: 'Nâu', m: [150, 102, 70] }, dam: { ten: 'Nâu đậm', m: [108, 72, 50] } };
  var MTOC = { goc: { ten: 'Như tranh vẽ', m: null }, den: { ten: 'Đen', m: [[14, 12, 14], [40, 34, 36], [92, 84, 88]] }, naude: { ten: 'Nâu đen', m: [[24, 16, 12], [62, 42, 32], [128, 98, 80]] },
    hatde: { ten: 'Hạt dẻ', m: [[36, 18, 10], [104, 58, 32], [182, 128, 88]] }, nausang: { ten: 'Nâu sáng', m: [[58, 36, 20], [150, 104, 64], [222, 182, 138]] },
    ruou: { ten: 'Đỏ rượu', m: [[34, 8, 14], [104, 30, 42], [184, 92, 104]] }, khoi: { ten: 'Xám khói', m: [[44, 42, 46], [118, 114, 120], [204, 200, 206]] } };
  var MMAT = { goc: { ten: 'Như tranh vẽ', m: null }, den: { ten: 'Nâu đen', m: [[18, 10, 8], [52, 32, 22], [110, 78, 58]] }, nau: { ten: 'Nâu', m: [[30, 16, 8], [96, 58, 30], [170, 120, 76]] },
    hophach: { ten: 'Hổ phách', m: [[44, 24, 6], [150, 96, 36], [222, 172, 96]] }, xam: { ten: 'Xám', m: [[26, 28, 32], [82, 88, 96], [158, 164, 172]] } };
  var GOC = {
    'co-dau': { gt: 'nu', ten: 'Mai', cao: 158, vb: 'vua', dang: 'can', vai: 0, bung: 0, hong: 0, mat: 'goc', mt: 'to', may: 'manh', toc: 'goc', ao: 'vest', da: 'goc', mtoc: 'goc', mm: 'goc' },
    'chu-re': { gt: 'nam', ten: 'Nam', cao: 172, vb: 'vua', dang: 'can', vai: 0, bung: 0, hong: 0, mat: 'goc', mt: 'hanh', may: 'tunhien', toc: 'goc', ao: 'vest', da: 'goc', mtoc: 'goc', mm: 'goc' }
  };

  /* ---------- ảnh ---------- */
  var anh = {};
  function lay(n) { var im = anh[n]; if (!im) { im = anh[n] = new Image(); im.decoding = 'async'; im.onload = function () { khiDoi(); }; im.src = 'nv/' + n + '.webp'; } return im; }
  function san(im) { return im.complete && im.naturalWidth > 0; }
  function tao(w, h) { var c = document.createElement('canvas'); c.width = Math.max(1, Math.round(w)); c.height = Math.max(1, Math.round(h)); return c; }
  var bangTam = {};
  function tam(ten, w, h) { // canvas dùng lại theo tên, đã xoá trắng
    var c = bangTam[ten] || (bangTam[ten] = tao(w, h)); w = Math.max(1, Math.round(w)); h = Math.max(1, Math.round(h));
    if (c.width !== w || c.height !== h) { c.width = w; c.height = h; } else { var x = c.getContext('2d'); x.setTransform(1, 0, 0, 1, 0, 0); x.globalAlpha = 1; x.globalCompositeOperation = 'source-over'; x.clearRect(0, 0, w, h); }
    return c;
  }
  function tenDau(p) {
    var g = p.gt, v = p.vb, m = p.mat, t = p.toc;
    if (v === 'vua') return 'dau-' + (m === 'goc' && t === 'goc' ? g + '-goc' : m === 'goc' ? g + '-toc-' + t : t === 'goc' ? g + '-mat-' + m : g + '-' + m + '-' + t);
    return 'dau-' + g + '-' + v + (m !== 'goc' ? '-' + m : '') + (t !== 'goc' ? '-' + t : '');
  }
  function tenThan(p) { return (p.ao === 'aodai' ? 'ad-' : 'than-') + p.gt + '-' + (p.vb === 'vua' ? 'goc' : p.vb) + '-' + p.dang; }

  // Nguồn của một lớp: ô trong tấm ghép cỡ nhỏ khi vẽ nhỏ, tranh nét khi vẽ lớn. Lớp cổ áo trong tấm nhỏ chỉ giữ phần trên.
  var PHAN_CO = 0.34;
  function tiNho(gt) { return MANH && MANH[gt].nho ? MANH[gt].nho.ti : 0; }
  function nguon(gt, ten, ti) {
    var N = MANH && MANH[gt].nho, o = N && ti <= N.ti * 1.15 && N.o[ten];
    if (o) return { im: lay(N.f), x: o[0], y: o[1], w: o[2], h: o[3], phan: ten.indexOf('co-') === 0 ? PHAN_CO : 1 };
    return { im: lay(ten), x: 0, y: 0, w: 0, h: 0, phan: 1 };
  }
  function veNguon(x, s, dx, dy, dw, dh) { x.drawImage(s.im, s.x, s.y, s.w || s.im.naturalWidth, s.h || s.im.naturalHeight, dx, dy, dw, dh * s.phan); }

  /* ---------- bộ nhớ có giới hạn ---------- */
  var KHOA_DANG = ['gt', 'vb', 'dang', 'mat', 'mt', 'may', 'toc', 'ao', 'da', 'mtoc', 'mm', 'vai', 'bung', 'hong']; // không có chiều cao, tên
  function khoa(p) { return KHOA_DANG.map(function (k) { return p[k] == null ? 0 : p[k]; }).join('|'); }
  function Nho(toiDa) { this.m = new Map(); this.toiDa = toiDa; }
  Nho.prototype.lay = function (k) { var v = this.m.get(k); if (v !== undefined) { this.m.delete(k); this.m.set(k, v); } return v; };
  Nho.prototype.ghi = function (k, v) { this.m.delete(k); this.m.set(k, v); if (this.m.size > this.toiDa) this.m.delete(this.m.keys().next().value); return v; };
  Nho.prototype.xoa = function () { this.m.clear(); };
  // Hai cỡ: tranh nét (ít, vì mỗi tấm vài MB) và tranh nhỏ cho thẻ hình (nhiều).
  function HaiCo(lon, nhoCo) { this.lon = new Nho(lon); this.nho = new Nho(nhoCo); }
  HaiCo.prototype.cho = function (ti) { return ti >= 0.9 ? this.lon : this.nho; };
  HaiCo.prototype.xoa = function () { this.lon.xoa(); this.nho.xoa(); };
  var nGhep = new HaiCo(4, 80), nDau = new HaiCo(3, 60), nThan = new HaiCo(3, 60), nThanMau = new HaiCo(2, 40), nCo = new HaiCo(2, 30), nMatNa = new HaiCo(5, 80), nThumb = new Nho(120);

  /* ---------- màu ---------- */
  function luma(r, g, b) { return (0.3 * r + 0.59 * g + 0.11 * b) / 255; }
  var HS = [0, 0, 0];
  function sacDo(r, g, b) { // ghi [sắc độ°, độ đậm, độ sáng] vào HS (không tạo mảng mới cho từng điểm)
    var mx = r > g ? (r > b ? r : b) : (g > b ? g : b), mn = r < g ? (r < b ? r : b) : (g < b ? g : b), dd = mx - mn || 1e-6, h;
    if (mx === r) h = ((g - b) / dd) % 6; else if (mx === g) h = (b - r) / dd + 2; else h = (r - g) / dd + 4;
    h *= 60; if (h < 0) h += 360; HS[0] = h; HS[1] = mx ? (mx - mn) / mx : 0; HS[2] = mx / 255;
  }
  var C3 = [0, 0, 0];
  function bac3(st3, l) { // độ sáng l (0..1) → ba nấc màu, ghi vào C3
    var t = l < 0 ? 0 : l > 1 ? 1 : l, a, b, u;
    if (t < 0.5) { a = st3[0]; b = st3[1]; u = t / 0.5; } else { a = st3[1]; b = st3[2]; u = (t - 0.5) / 0.5; }
    C3[0] = a[0] + (b[0] - a[0]) * u; C3[1] = a[1] + (b[1] - a[1]) * u; C3[2] = a[2] + (b[2] - a[2]) * u;
  }
  function doc(v, a, b) { var t = (v - a) / (b - a); return t < 0 ? 0 : t > 1 ? 1 : t; }
  function mem(v, a, b) { var t = doc(v, a, b); return t * t * (3 - 2 * t); }
  var nhap = new Float32Array(1);
  function mo(w, W, H, r) { // làm mờ hộp tách hai chiều
    var n = W * H; if (nhap.length < n) nhap = new Float32Array(n);
    var t = nhap, x, y, s, o, k = 1 / (2 * r + 1);
    for (y = 0; y < H; y++) { s = 0; o = y * W;
      for (x = -r; x <= r; x++) s += w[o + (x < 0 ? 0 : x > W - 1 ? W - 1 : x)];
      for (x = 0; x < W; x++) { t[o + x] = s * k; s += w[o + (x + r + 1 > W - 1 ? W - 1 : x + r + 1)] - w[o + (x - r < 0 ? 0 : x - r)]; } }
    for (x = 0; x < W; x++) { s = 0;
      for (y = -r; y <= r; y++) s += t[(y < 0 ? 0 : y > H - 1 ? H - 1 : y) * W + x];
      for (y = 0; y < H; y++) { w[y * W + x] = s * k; s += t[(y + r + 1 > H - 1 ? H - 1 : y + r + 1) * W + x] - t[(y - r < 0 ? 0 : y - r) * W + x]; } }
  }
  var DA_GOC = { nam: [232, 190, 150], nu: [244, 210, 182] }; // màu da trung bình của tranh gốc (đo trên ảnh)
  // Một điểm ảnh giống da tới đâu: LN[0] = lõi chắc chắn là da; LN[1] = mảng sáng ít màu (chỉ tính là da khi nằm trong vùng da).
  var LN = [0, 0];
  function daDiem(r, g, b, al) {
    sacDo(r, g, b); var hh = HS[0], ss = HS[1], vv = HS[2];
    var cv = doc(hh, 32, 36) * (1 - doc(hh, 46, 50)) * doc(ss, 0.22, 0.27) * (1 - doc(vv, 0.8, 0.86)); // cà vạt, chỉ thêu vàng
    var sac = doc(hh, 4, 12) * (1 - doc(hh, 48, 54)) * (1 - cv), sang = doc(vv, 0.28, 0.42) * doc(al, 160, 230);
    LN[0] = sac * doc(ss, 0.17, 0.22) * (1 - doc(ss, 0.6, 0.72)) * sang;
    var n1 = 1 - doc(ss, 0.04, 0.08), n2 = doc(hh, 0, 6) * (1 - doc(hh, 58, 66)); LN[1] = (n1 > n2 ? n1 : n2) * (1 - cv) * sang;
  }
  function coTheLaToc(r, g, b, l) { sacDo(r, g, b); return (HS[0] <= 55 || HS[0] >= 330) && (l < 0.5 || HS[1] > 0.25) || HS[1] < 0.2 && l < 0.5; } // tối, ấm hoặc xám

  /* Mặt nạ của một lớp (không phụ thuộc màu được chọn, nên tính một lần rồi nhớ lại; đổi màu chỉ còn là phép nhân).
     Công thức giữ nguyên như bản trước, chỉ khác là không tính lại mỗi lần đổi màu.
     Da: lõi chắc chắn là da, rồi lấp các mảng sáng ít màu nằm trong vùng da (vai, ngực bắt nắng). */
  function matNaDa(a, W, H, ti) {
    var n = W * H, i, j, y, v;
    function R(px) { return Math.max(1, Math.round(px * ti)); }
    var loi = new Float32Array(n), nhat = new Float32Array(n), dong = new Float32Array(n);
    for (i = 0, j = 0; i < n; i++, j += 4) { if (a[j + 3] < 160) continue; daDiem(a[j], a[j + 1], a[j + 2], a[j + 3]); loi[i] = dong[i] = LN[0]; nhat[i] = LN[1]; }
    mo(dong, W, H, R(14)); for (i = 0; i < n; i++) dong[i] = dong[i] > 0.04 ? 1 : 0;
    mo(dong, W, H, R(10)); for (i = 0; i < n; i++) if (dong[i] > 0.9 && nhat[i] > loi[i]) loi[i] = nhat[i];
    mo(loi, W, H, R(2));
    var d = new Uint8Array(n), ya = H, yb = 0; for (i = 0; i < n; i++) { v = loi[i] * 1.15 * 255; if (v >= 2.5) { d[i] = v > 255 ? 255 : v + 0.5; y = (i / W) | 0; if (y < ya) ya = y; if (y > yb) yb = y; } }
    return { d: d, w: W, h: H, ya: ya, yb: Math.min(H, yb + 1) };
  }
  /* Tóc (chỉ lớp đầu, nên màu tóc không thể loang sang trang phục): điểm tối, ấm hoặc xám, loang từ đỉnh đầu qua khối dày,
     rồi đi tiếp một quãng ngắn theo nét mảnh (tóc mai, lọn rủ) để không chạy dọc viền mặt. Lông mày theo màu tóc, mắt thì không.
     Tròng mắt: chỉ quanh tâm mảnh mắt. manh: vị trí mảnh mắt, lông mày trên lớp này. */
  function matNaToc(a, W, H, manh, top, ti) {
    var n = W * H, i, j, k, v, l, u, xx;
    function R(px) { return Math.max(1, Math.round(px * ti)); }
    var can = new Uint8Array(n), e = new Float32Array(n);
    for (i = 0, j = 0; i < n; i++, j += 4) { if (a[j + 3] < 90) continue; l = luma(a[j], a[j + 1], a[j + 2]); if (l > 0.62) continue; if (coTheLaToc(a[j], a[j + 1], a[j + 2], l)) { can[i] = 1; e[i] = 1; } }
    mo(e, W, H, R(2)); // e cao = nằm trong khối dày (tóc), e thấp = nét mảnh (viền mặt, lông mi)
    var toc = new Uint8Array(n), q = new Int32Array(n), dau = 0, cuoi = 0;
    top = Math.min(H, top);
    for (i = 0; i < W * top; i++) if (can[i] && e[i] > 0.7) { toc[i] = 1; q[cuoi++] = i; }
    while (dau < cuoi) { u = q[dau++]; xx = u % W;
      v = u - W; if (v >= 0 && !toc[v] && can[v] && e[v] > 0.7) { toc[v] = 1; q[cuoi++] = v; }
      v = u + W; if (v < n && !toc[v] && can[v] && e[v] > 0.7) { toc[v] = 1; q[cuoi++] = v; }
      if (xx > 0) { v = u - 1; if (!toc[v] && can[v] && e[v] > 0.7) { toc[v] = 1; q[cuoi++] = v; } }
      if (xx < W - 1) { v = u + 1; if (!toc[v] && can[v] && e[v] > 0.7) { toc[v] = 1; q[cuoi++] = v; } } }
    var xa = new Uint16Array(n), gh = R(70); dau = 0;
    while (dau < cuoi) { u = q[dau++]; if (xa[u] >= gh) continue; xx = u % W; k = xa[u] + 1;
      v = u - W; if (v >= 0 && !toc[v] && can[v]) { toc[v] = 1; xa[v] = k; q[cuoi++] = v; }
      v = u + W; if (v < n && !toc[v] && can[v]) { toc[v] = 1; xa[v] = k; q[cuoi++] = v; }
      if (xx > 0) { v = u - 1; if (!toc[v] && can[v]) { toc[v] = 1; xa[v] = k; q[cuoi++] = v; } }
      if (xx < W - 1) { v = u + 1; if (!toc[v] && can[v]) { toc[v] = 1; xa[v] = k; q[cuoi++] = v; } } }
    var trong = [];
    manh.forEach(function (qq) {
      var x0 = Math.max(0, Math.floor(qq.x)), x1 = Math.min(W, Math.ceil(qq.x + qq.w)), y0 = Math.max(0, Math.floor(qq.y)), y1 = Math.min(H, Math.ceil(qq.y + qq.h)), x, y, t, j2;
      for (y = y0; y < y1; y++) for (x = x0; x < x1; x++) { t = y * W + x;
        if (qq.loai === 'mat') { var ex = (x - qq.x - qq.w / 2) / (qq.w * 0.4), ey = (y - qq.y - qq.h / 2) / (qq.h * 0.4); if (ex * ex + ey * ey < 1) toc[t] = 0; } // không tô mắt bằng màu tóc
        else if (can[t] && luma(a[t * 4], a[t * 4 + 1], a[t * 4 + 2]) < 0.42) toc[t] = 1; }                                                       // lông mày theo màu tóc
      if (qq.loai !== 'mat') return;
      var cx = qq.x + qq.w / 2, cy = qq.y + qq.h / 2, rx = qq.w * 0.24, ry = qq.h * 0.14, bx = Math.max(0, Math.floor(cx - rx)), by = Math.max(0, Math.floor(cy - ry)), ex1 = Math.min(W, Math.ceil(cx + rx)), ey1 = Math.min(H, Math.ceil(cy + ry));
      if (ex1 <= bx || ey1 <= by) return;
      var wt = new Float32Array((ex1 - bx) * (ey1 - by));
      for (y = by; y < ey1; y++) for (x = bx; x < ex1; x++) { j2 = (y * W + x) * 4; l = luma(a[j2], a[j2 + 1], a[j2 + 2]); sacDo(a[j2], a[j2 + 1], a[j2 + 2]);
        if (l > 0.16 && l < 0.62 && HS[1] > 0.3 && (HS[0] < 50 || HS[0] > 340)) wt[(y - by) * (ex1 - bx) + x - bx] = doc(l, 0.16, 0.24) * (1 - doc(l, 0.52, 0.62)); }
      trong.push({ x: bx, y: by, w: ex1 - bx, h: ey1 - by, wt: wt });
    });
    var wt2 = e, ya = H, yb = 0, y; for (i = 0; i < n; i++) { wt2[i] = toc[i]; if (toc[i]) { y = (i / W) | 0; if (y < ya) ya = y; if (y > yb) yb = y; } }
    mo(wt2, W, H, 1);
    var d = new Uint8Array(n); for (i = 0; i < n; i++) { v = wt2[i] * 1.6 * 255; d[i] = v > 255 ? 255 : v + 0.5; }
    return { d: d, w: W, h: H, ya: Math.max(0, ya - 2), yb: Math.min(H, yb + 3), trong: trong };
  }
  // Tô màu lên điểm ảnh a (rộng W, cao H, cùng khung với mặt nạ). Thứ tự như bản trước: da, rồi tóc, rồi tròng mắt; cùng công thức trộn.
  function toMau(a, W, H, p, mn) {
    var da = DA[p.da].m, bt = MTOC[p.mtoc].m, bm = MMAT[p.mm].m, g0 = DA_GOC[p.gt], x, y, i, j, w, l, v, r0, g_, b0, R, G, B;
    var md = da && mn.da, mt = (bt || bm) && mn.toc, t0 = da ? da[0] / g0[0] : 1, t1 = da ? da[1] / g0[1] : 1, t2 = da ? da[2] / g0[2] : 1;
    var y0 = Math.min(md ? md.ya : H, mt && bt ? mt.ya : H), y1 = Math.max(md ? md.yb : 0, mt && bt ? mt.yb : 0);
    var lumTrong = bm ? mt.trong.map(function (t) { var L = new Float32Array(t.w * t.h); for (y = 0; y < t.h; y++) for (x = 0; x < t.w; x++) { j = ((t.y + y) * W + t.x + x) * 4; L[y * t.w + x] = luma(a[j], a[j + 1], a[j + 2]); } return L; }) : null;
    for (y = y0; y < y1; y++) for (x = 0, i = y * W, j = i * 4; x < W; x++, i++, j += 4) {
      if (a[j + 3] < 10) continue; r0 = R = a[j]; g_ = G = a[j + 1]; b0 = B = a[j + 2];
      if (md && md.d[i]) { w = md.d[i] / 255; v = r0 * t0; R += ((v > 255 ? 255 : v) - r0) * w; v = g_ * t1; G += ((v > 255 ? 255 : v) - g_) * w; v = b0 * t2; B += ((v > 255 ? 255 : v) - b0) * w; }
      if (bt && mt.d[i] > 2) { l = luma(r0, g_, b0); w = mt.d[i] / 255 * (1 - doc(l, 0.5, 0.64)); if (w > 0) { bac3(bt, l / 0.5); R += (C3[0] - R) * w; G += (C3[1] - G) * w; B += (C3[2] - B) * w; } }
      a[j] = R; a[j + 1] = G; a[j + 2] = B;
    }
    if (bm) mt.trong.forEach(function (t, k) { for (y = 0; y < t.h; y++) for (x = 0; x < t.w; x++) { w = t.wt[y * t.w + x]; if (w < 0.01) continue; j = ((t.y + y) * W + t.x + x) * 4;
      bac3(bm, lumTrong[k][y * t.w + x] / 0.55); /* độ sáng lấy từ màu gốc, như bản trước */ a[j] += (C3[0] - a[j]) * w; a[j + 1] += (C3[1] - a[j + 1]) * w; a[j + 2] += (C3[2] - a[j + 2]) * w; } });
  }

  /* ---------- nắn dáng: vai, eo-bụng, hông, 7 mức mỗi trục (−3…+3) ----------
     Mỗi hàng điểm ảnh của lớp thân được co giãn quanh trục người. Trong vùng có cánh tay, chỉ phần thân giữa co giãn,
     phần ngoài (tay, bàn tay) dời theo nguyên hình. Tỉ lệ "thân giữa" chuyển mềm ở hai đầu vùng tay nên không có bậc. */
  var DAI = { nam: { vai: [0.225, 0.05], bung: [0.40, 0.055], hong: [0.50, 0.05], tay: [0.19, 0.6], loi: 0.62 },
    nu: { vai: [0.235, 0.045], bung: [0.37, 0.05], hong: [0.47, 0.055], tay: [0.21, 0.5], loi: 0.55 } };
  var MUC = { vai: 0.05, bung: 0.065, hong: 0.05 };
  var bien = {};
  function bienHang(a, W, H, key) { // mép trái, phải của người ở từng hàng (a: điểm ảnh của lớp thân chưa nắn)
    var r = new Float32Array(H * 2);
    for (var y = 0; y < H; y++) { var x0 = -1, x1 = -1, o = y * W * 4 + 3, x; for (x = 0; x < W; x++) if (a[o + x * 4] > 100) { x0 = x; break; }
      if (x0 >= 0) for (x = W - 1; x >= x0; x--) if (a[o + x * 4] > 100) { x1 = x; break; } r[y * 2] = x0; r[y * 2 + 1] = x1; }
    return (bien[key] = r);
  }
  function chuong(f, d) { var z = (f - d[0]) / d[1]; return Math.exp(-0.5 * z * z); }
  function nan(x, nguonC, ms, p, bh) { // vẽ canvas nguồn (cỡ ms) đã nắn vào x; các hàng không đổi được vẽ gộp một lượt
    var a = p.vai | 0, b = p.bung | 0, c = p.hong | 0, n = Math.min(ms.h, nguonC.height), D = DAI[p.gt], cx = ms.cx * ms.w, y = 0, y2;
    function heSo(y) { var f = y / ms.h, k = 1 + MUC.vai * a * chuong(f, D.vai) + MUC.bung * b * chuong(f, D.bung) + MUC.hong * c * chuong(f, D.hong);
      if (c > 0 && p.gt === 'nu' && f > D.hong[0]) k = Math.max(k, 1 + 0.03 * c); // váy xoè theo hông
      return bh[y * 2] < 0 || Math.abs(k - 1) < 0.002 ? 1 : k; }
    while (y < n) {
      var k = heSo(y);
      if (k === 1) { y2 = y + 1; while (y2 < n && heSo(y2) === 1) y2++; x.drawImage(nguonC, 0, y, ms.w, y2 - y, 0, y, ms.w, y2 - y); y = y2; continue; }
      var f = y / ms.h, x0 = bh[y * 2], x1 = bh[y * 2 + 1] + 1, s = mem(f, D.tay[0] - 0.03, D.tay[0] + 0.03) * (1 - mem(f, D.tay[1] - 0.03, D.tay[1] + 0.03));
      var e = Math.max(cx - x0, x1 - cx) + 1, T = e * (1 - (1 - D.loi) * s), L = Math.max(x0, cx - T), Rr = Math.min(x1, cx + T), d = T * (k - 1);
      x.drawImage(nguonC, L, y, Rr - L, 1, cx - (cx - L) * k, y, (Rr - L) * k, 1);
      if (L > x0) x.drawImage(nguonC, x0, y, L - x0, 1, x0 - d, y, L - x0, 1);
      if (Rr < x1) x.drawImage(nguonC, Rr, y, x1 - Rr, 1, Rr + d, y, x1 - Rr, 1);
      y++;
    }
  }

  /* Lật ngang và đánh sáng trong một lượt. Tranh nguồn đã lật ngang từ trước, lật lại cho đúng chi tiết trang phục (hoa cài áo, vạt áo).
     Tranh vẽ nắng từ trái, cảnh có nắng từ sau bên phải: tối dần sang trái, sáng dần sang phải theo bề ngang của người ở từng hàng,
     và một viền nắng ấm ở mép phải. a: điểm ảnh nguồn; o: điểm ảnh đích (cùng cỡ). */
  function latSang(a, o, W, H) {
    var vien = Math.max(2, W * 0.012), y, i, x0, x1, row, js, jd, t, k, r, al, f0, f1, rong;
    for (y = 0; y < H; y++) {
      row = y * W * 4; x0 = -1; x1 = -1;
      for (i = 0; i < W; i++) if (a[row + i * 4 + 3] > 128) { x0 = i; break; }
      if (x0 < 0) continue;
      for (i = W - 1; i >= x0; i--) if (a[row + i * 4 + 3] > 128) { x1 = i; break; }
      f0 = W - 1 - x1; f1 = W - 1 - x0; rong = f1 - f0; // mép của người sau khi lật
      for (i = 0; i < W; i++) { js = row + (W - 1 - i) * 4; al = a[js + 3]; if (!al) continue; jd = row + i * 4;
        if (rong < 4 || al < 10) { o[jd] = a[js]; o[jd + 1] = a[js + 1]; o[jd + 2] = a[js + 2]; o[jd + 3] = al; continue; }
        t = (i - f0) / rong; k = 0.9 + 0.2 * (t < 0 ? 0 : t > 1 ? 1 : t); r = 1 - (f1 - i) / vien; r = r > 0 ? (r > 1 ? 0.3 : r * 0.3) : 0;
        o[jd] = a[js] * k + (255 - a[js]) * r; o[jd + 1] = a[js + 1] * k + (236 - a[js + 1]) * r * 0.9; o[jd + 2] = a[js + 2] * k + (205 - a[js + 2]) * r * 0.7; o[jd + 3] = al; }
    }
  }

  /* ---------- các lớp của một nhân vật ---------- */
  function coTi(p, ti) { var m = META[p.gt]; return { w: Math.round(m.w * ti), h: Math.round(m.h * ti), hdau: Math.ceil(m.hdau * ti), cx: m.cx }; }
  // Mảnh mắt, lông mày đặt lên đầu p (toạ độ ở tỉ lệ ti). Kiểu lông mày tuỳ kiểu tóc:
  //  - chú rể Vuốt ngược: đầu đã xoá lông mày gốc, dùng lớp nét không dính tóc (mayA) đặt đúng chỗ lông mày cũ;
  //  - cô dâu Dài thẳng: mảnh đã bỏ lọn tóc mái của kiểu Búi cao (mayS); cô dâu Ngang cằm: tóc mái che, không vẽ;
  //  - còn lại: mảnh cắt nguyên từ tranh có cùng kiểu tóc mái.
  function manhCua(p, ti) {
    var out = [], M = MANH && MANH[p.gt]; if (!M) return out;
    var td = tenDau(p), vt = M.vitri[td]; if (!vt) return out;
    function them(bo, cho, loai) { if (bo && cho) bo.forEach(function (o, i) { if (o && cho[i]) out.push({ sx: o.x, sy: o.y, sw: o.w, sh: o.h, x: cho[i][0] * ti, y: cho[i][1] * ti, w: o.w * ti, h: o.h * ti, loai: loai }); }); }
    function bo(goc) { return goc && goc[p.mat] && goc[p.mat][p.may]; }
    if (p.gt === 'nam' && p.toc === 'vuot' && M.mayA && M.vitriA[td]) them(bo(M.mayA), M.vitriA[td], 'may');
    else if (p.gt === 'nu' && p.toc === 'dai' && M.mayS) them(bo(M.mayS), vt.may, 'may');
    else if (!(p.gt === 'nu' && p.toc === 'ngan')) them(bo(M.manh.may), vt.may, 'may');
    them(M.manh.mat[p.mat] && M.manh.mat[p.mat][p.mt], vt.mat, 'mat');
    return out;
  }
  function veManh(x, tamAnh, manh, dx, dy) { manh.forEach(function (q) { x.drawImage(tamAnh, q.sx, q.sy, q.sw, q.sh, q.x - dx, q.y - dy, q.w, q.h); }); }
  function canMau(p) { return p.da !== 'goc' || p.mtoc !== 'goc' || p.mm !== 'goc'; }
  // Lớp đầu: đầu + mảnh mắt, lông mày; mặt nạ tính trên chính lớp này (nhớ theo đầu + kiểu mắt + kiểu lông mày), rồi tô màu.
  function lopDau(p, ti) {
    var td = tenDau(p), key = td + '|' + p.mt + '|' + p.may + '|' + p.da + '|' + p.mtoc + '|' + p.mm + '@' + ti, kho = nDau.cho(ti), c = kho.lay(key); if (c) return c;
    var s = nguon(p.gt, td, ti), M = MANH && MANH[p.gt], ta = M && lay(M.tam);
    if (!san(s.im) || !ta || !san(ta)) return null;
    var ms = coTi(p, ti), manh = manhCua(p, ti), mau = canMau(p); c = tao(ms.w, ms.hdau); var x = c.getContext('2d', { willReadFrequently: mau });
    veNguon(x, s, 0, 0, ms.w, META[p.gt].hdau * ti); veManh(x, ta, manh, 0, 0);
    if (mau) {
      var img = x.getImageData(0, 0, ms.w, ms.hdau), a = img.data, kmn = td + '|' + p.mt + '|' + p.may + '@' + ti, khoM = nMatNa.cho(ti), mn = khoM.lay(kmn) || khoM.ghi(kmn, {});
      if (p.da !== 'goc' && !mn.da) mn.da = matNaDa(a, ms.w, ms.hdau, ti);
      if ((p.mtoc !== 'goc' || p.mm !== 'goc') && !mn.toc) mn.toc = matNaToc(a, ms.w, ms.hdau, manh, Math.round(ms.h * 0.08), ti);
      toMau(a, ms.w, ms.hdau, p, mn); x.putImageData(img, 0, 0);
    }
    return kho.ghi(key, c);
  }
  // Lớp thân: tranh thân đã đổi màu da (nhớ theo tranh + màu), rồi nắn dáng (nhớ theo các nấc). laCo: lớp cổ áo dài, nắn cùng công thức.
  function lopThan(p, ti, laCo) {
    var tT = tenThan(p), ten = (laCo ? 'co-' : '') + tT, da = !laCo && DA[p.da].m, co = (p.vai | 0) || (p.bung | 0) || (p.hong | 0);
    var kn = ten + '|' + (da ? p.da : '') + '|' + (p.vai | 0) + '|' + (p.bung | 0) + '|' + (p.hong | 0) + '@' + ti, kho = (laCo ? nCo : nThan).cho(ti), c = kho.lay(kn); if (c) return c;
    var s = nguon(p.gt, ten, ti), sT = laCo ? nguon(p.gt, tT, ti) : s; if (!san(s.im) || !san(sT.im)) return null;
    var ms = coTi(p, ti), km = ten + '|' + (da ? p.da : '') + '@' + ti, khoM = nThanMau.cho(ti), g = khoM.lay(km), kb = tT + '@' + ms.w, a = null;
    if (!g) { g = tao(ms.w, ms.h); var gx = g.getContext('2d', { willReadFrequently: !!da }); gx.imageSmoothingQuality = 'medium'; veNguon(gx, s, 0, 0, ms.w, ms.h);
      if (da) { var img = gx.getImageData(0, 0, ms.w, ms.h), khoD = nMatNa.cho(ti), mn = khoD.lay(ten + '@' + ti) || khoD.ghi(ten + '@' + ti, { da: matNaDa(img.data, ms.w, ms.h, ti) });
        if (co && !bien[kb]) bienHang(img.data, ms.w, ms.h, kb);
        toMau(img.data, ms.w, ms.h, { gt: p.gt, da: p.da, mtoc: 'goc', mm: 'goc' }, mn); gx.putImageData(img, 0, 0); }
      khoM.ghi(km, g); }
    if (!co) return kho.ghi(kn, g);
    if (!bien[kb]) { var tb = tam('doc', ms.w, ms.h), bx = tb.getContext('2d', { willReadFrequently: true }); veNguon(bx, sT, 0, 0, ms.w, ms.h); bienHang(bx.getImageData(0, 0, ms.w, ms.h).data, ms.w, ms.h, kb); }
    c = tao(ms.w, ms.h); nan(c.getContext('2d'), g, ms, p, bien[kb]);
    return kho.ghi(kn, c);
  }

  /* ---------- ghép một nhân vật ----------
     Thứ tự: thân → đầu → cổ áo dài, rồi lật ngang và đánh sáng. o.ti: tỉ lệ (mặc định 1 = tranh nét). Trả về null nếu tranh chưa tải xong. */
  function ghep(p, o) {
    if (!MANH) return null;
    var ti = o && o.ti || 1, key = khoa(p) + '@' + ti, kho = nGhep.cho(ti), f = kho.lay(key); if (f) return f;
    var than = lopThan(p, ti), dau = lopDau(p, ti), co = p.ao === 'aodai' ? lopThan(p, ti, true) : null; // gọi cả ba để tranh tải song song
    if (!than || !dau || (p.ao === 'aodai' && !co)) return null;
    var ms = coTi(p, ti), c = tam('ghep', ms.w, ms.h), x = c.getContext('2d', { willReadFrequently: true });
    // Ảnh áo dài được mô hình vẽ thấp hơn đầu khoảng 14/2600 chiều cao (đo bằng tương quan vùng mặt): kéo lên cho khớp cằm, giữ chân.
    var dy = p.ao === 'aodai' ? ms.h * 14 / 2600 : 0;
    if (dy) x.drawImage(than, 0, -dy, ms.w, ms.h + dy); else x.drawImage(than, 0, 0);
    x.drawImage(dau, 0, 0);
    if (co) x.drawImage(co, 0, -dy, ms.w, ms.h + dy); // cổ áo cao che cổ sơ mi và voan của lớp đầu
    f = tao(ms.w, ms.h); var fx = f.getContext('2d'), ra = fx.createImageData(ms.w, ms.h);
    latSang(x.getImageData(0, 0, ms.w, ms.h).data, ra.data, ms.w, ms.h); fx.putImageData(ra, 0, 0);
    return kho.ghi(key, f);
  }
  // Hình tốt nhất đang có: tranh nét, hoặc bản cỡ nhỏ nếu tấm ghép nhỏ đã tải mà tranh nét chưa về. tam = true khi là bản tạm.
  function nhoSan(gt) { var N = MANH && MANH[gt].nho; return N && anh[N.f] && san(anh[N.f]); }
  function hinh(p, ti) {
    var c = ghep(p, ti ? { ti: ti } : null); if (c) return { c: c, tam: false };
    if (nhoSan(p.gt) && (!ti || ti > tiNho(p.gt) * 1.15)) { c = ghep(p, { ti: tiNho(p.gt) }); if (c) return { c: c, tam: true }; }
    return null;
  }

  /* ---------- hình xem trước cho thẻ chọn ---------- */
  function vungMat(p, asp) { // cận cảnh đôi mắt và lông mày ở cỡ thật: cắt từ lớp đầu cỡ thật (đã tô màu), lật cho đúng chiều
    var M = MANH && MANH[p.gt], td = tenDau(p), vt = M && M.vitri[td], bo = M && M.manh.mat[p.mat] && M.manh.mat[p.mat][p.mt], m = META[p.gt];
    var d = M && lopDau(p, 1); if (!d) return null;
    var sw, sh, sx, sy;
    if (vt && bo && bo[0] && bo[1]) { var xa = vt.mat[0][0] + bo[0].w / 2, xb = vt.mat[1][0] + bo[1].w / 2, yc = (vt.mat[0][1] + bo[0].h / 2 + vt.mat[1][1] + bo[1].h / 2) / 2;
      sw = Math.abs(xa - xb) * 2.9; sh = sw / asp; sx = (xa + xb) / 2 - sw / 2; sy = yc - sh * 0.62; }
    else { sw = m.w * 0.3; sh = sw / asp; sx = m.cx * m.w - sw / 2; sy = m.h * 0.08; }
    var f = tao(sw, sh), fx = f.getContext('2d'); fx.translate(sw, 0); fx.scale(-1, 1); fx.drawImage(d, -sx, -Math.max(0, sy)); return f;
  }
  // Vẽ thẻ hình. Trả về true khi đã vẽ bản đủ nét; false khi còn chờ tranh (có thể đã vẽ bản tạm).
  function veThumb(cv, p, khung) {
    var key = khoa(p) + '#' + khung + '#' + cv.width + 'x' + cv.height, t = nThumb.lay(key), xong = true;
    if (!t) {
      var m = META[p.gt], asp = cv.width / cv.height, c, sx, sy, sw, sh, k, r;
      if (khung === 'mat') { c = vungMat(p, asp); if (!c) return false; sx = 0; sy = 0; sw = c.width; sh = c.height; }
      else if (khung === 'nguoi') { r = hinh(p, tiNho(p.gt) || 0.18); if (!r) return false; c = r.c; k = c.height / m.h; sh = c.height; sw = sh * asp; sx = (1 - m.cx) * c.width - sw / 2; sy = 0; }
      else { r = hinh(p, Math.min(1, Math.max(0.3, cv.height / (0.27 * m.h)))); if (!r) return false; c = r.c; xong = !r.tam; k = c.height / m.h; sh = 0.27 * m.h * k; sw = sh * asp; sx = (1 - m.cx) * c.width - sw / 2; sy = 0; }
      t = tao(cv.width, cv.height); var tx = t.getContext('2d'); tx.imageSmoothingQuality = 'high'; tx.drawImage(c, sx, sy, sw, sh, 0, 0, cv.width, cv.height);
      if (xong) nThumb.ghi(key, t);
    }
    var x = cv.getContext('2d'); x.clearRect(0, 0, cv.width, cv.height); x.drawImage(t, 0, 0); return xong;
  }

  /* ---------- vẽ vào cảnh ----------
     Phối cảnh đo trên tranh nền: 1 m tại chân y (% khung) cao 0,307 × (y − 44) % chiều cao khung. */
  var CHAN_TROI = 44, MOT_MET = 0.307, CAO_GOC = { nam: 172, nu: 158 }, CO = { nam: 0.194, nu: 0.2 };
  // Chân ở (X, Y) px, k px mỗi cm. Đầu gần như không đổi cỡ theo chiều cao (∝ cao^0,3); phần dưới cổ co giãn bù vào.
  // Bề ngang chuyển mềm qua cổ để không có bậc giữa đầu và thân. Trả về null nếu chưa có tranh nào để vẽ.
  function ve(x, p, X, Y, k) {
    var m = META[p.gt], tn = tiNho(p.gt), nhoDu = tn && nhoSan(p.gt) && p.cao * k <= m.h * tn * 1.3 && ghep(p, { ti: tn }); // vẽ nhỏ thì dùng bản nhỏ: nhẹ và không răng cưa
    var hh = nhoDu ? { c: nhoDu, tam: false } : hinh(p); if (!hh) return null;
    var c = hh.c, q = c.height / m.h, cw = c.width, chh = c.height;
    var r = p.cao / CAO_GOC[p.gt], Hg = CAO_GOC[p.gt] * k / (1 - m.dinh), Wg = Hg * m.w / m.h;
    var sd = Math.pow(r, 0.3), hDau = Hg * CO[p.gt] * sd, wDau = Wg * sd;
    var hThan = p.cao * k / (1 - m.dinh) - hDau, wThan = Wg * Math.pow(r, 0.6), H = hDau + hThan;
    var cut = m.h * CO[p.gt] * q, ax = 1 - m.cx, sy1 = hDau / cut, sy2 = hThan / (chh - cut), T = Y - H;
    if (Math.abs(wDau - wThan) < 0.4) {
      x.drawImage(c, 0, 0, cw, cut, X - ax * wDau, T, wDau, hDau + 0.5);
      x.drawImage(c, 0, cut, cw, chh - cut, X - ax * wThan, Y - hThan, wThan, hThan);
    } else {
      var b = m.h * 0.014 * q, N = 8, y0 = cut - b, y1 = cut + b, i;
      x.drawImage(c, 0, 0, cw, y0, X - ax * wDau, T, wDau, y0 * sy1 + 0.5);
      for (i = 0; i < N; i++) {
        var s0 = y0 + (y1 - y0) * i / N, s1 = y0 + (y1 - y0) * (i + 1) / N, t = (i + 0.5) / N, w = wDau + (wThan - wDau) * (t * t * (3 - 2 * t));
        var d0 = s0 < cut ? s0 * sy1 : hDau + (s0 - cut) * sy2, d1 = s1 <= cut ? s1 * sy1 : hDau + (s1 - cut) * sy2;
        x.drawImage(c, 0, s0, cw, s1 - s0, X - ax * w, T + d0, w, d1 - d0 + 0.5);
      }
      var dT = hDau + (y1 - cut) * sy2; x.drawImage(c, 0, y1, cw, chh - y1, X - ax * wThan, T + dT, wThan, H - dT);
    }
    return { w: Math.max(wDau, wThan), h: H, tam: hh.tam };
  }
  function bongChan(x, cx, cy, rx) { // bóng tiếp xúc dưới chân
    var ry = rx * 0.2, g = x.createRadialGradient(0, 0, 0, 0, 0, 1);
    g.addColorStop(0, 'rgba(34,44,26,.62)'); g.addColorStop(0.6, 'rgba(34,44,26,.28)'); g.addColorStop(1, 'rgba(34,44,26,0)');
    x.save(); x.translate(cx - rx * 0.12, cy + ry * 0.1); x.scale(rx, ry); x.fillStyle = g; x.beginPath(); x.arc(0, 0, 1, 0, Math.PI * 2); x.fill(); x.restore();
  }
  // Bóng ngả dựng từ chính hình vẽ: (x, độ cao u) → (x − 0,75u, chân + 0,2u), cùng hướng với bóng bàn ghế trong tranh nền.
  // Dựng ở cỡ thu nhỏ rồi phóng lại: bóng vốn mờ nên không cần nét, mà đỡ tốn nhiều.
  function bongNga(x, ds, w, h) {
    var cao = ds[0].p.cao * ds[0].k, g_ = Math.max(1, Math.min(8, Math.pow(2, Math.round(Math.log2(Math.max(1, cao * 0.012)))))), sw = Math.ceil(w / g_), sh = Math.ceil(h / g_);
    var off = tam('bong', sw, sh), o = off.getContext('2d'); o.imageSmoothingQuality = 'high';
    ds.forEach(function (d) { o.setTransform(1 / g_, 0, 0.75 / g_, -0.2 / g_, -0.75 * d.y / g_, 1.2 * d.y / g_); ve(o, d.p, d.x, d.y, d.k); });
    o.setTransform(1, 0, 0, 1, 0, 0); o.globalCompositeOperation = 'source-in';
    var fy = ds[0].y / g_, dai = cao * 0.2 / g_, g = o.createLinearGradient(0, fy, 0, fy + dai);
    g.addColorStop(0, 'rgba(40,54,30,1)'); g.addColorStop(1, 'rgba(40,54,30,.4)'); o.fillStyle = g; o.fillRect(0, 0, sw, sh); o.globalCompositeOperation = 'source-over';
    var nua = tam('bong2', Math.ceil(sw / 2), Math.ceil(sh / 2)), nx = nua.getContext('2d'); nx.imageSmoothingQuality = 'high'; nx.drawImage(off, 0, 0, nua.width, nua.height);
    x.save(); x.globalAlpha = 0.62; x.imageSmoothingQuality = 'high'; x.drawImage(nua, 0, 0, nua.width, nua.height, 0, 0, nua.width * 2 * g_, nua.height * 2 * g_); x.restore();
  }
  // Nửa bề ngang vai thật (cm), không tính voan hay khoảng trống của ảnh.
  function nuaVai(p) { return (p.gt === 'nam' ? 23 : 19) * ({ manh: 0.92, vua: 1, day: 1.15 })[p.vb] * (1 + 0.05 * (p.vai | 0)) * Math.pow(p.cao / CAO_GOC[p.gt], 0.6); }

  // Tải trước lúc rảnh: tấm ghép cỡ nhỏ (cho thẻ hình) của một hay hai bên.
  function taiTruoc(gts) { if (MANH) (gts || ['nu', 'nam']).forEach(function (g) { if (MANH[g].nho) lay(MANH[g].nho.f); }); else choTai = gts || ['nu', 'nam']; }
  var choTai = null;

  fetch('nv/manh.json').then(function (r) { return r.json(); }).then(function (j) {
    MANH = j; [nGhep, nDau, nThan, nThanMau, nCo, nMatNa].forEach(function (k) { k.xoa(); }); nThumb.xoa();
    lay(j.nu.tam); lay(j.nam.tam); if (choTai) taiTruoc(choTai); khiDoi();
  }).catch(function () {});

  return { META: META, CHON: CHON, DA: DA, MTOC: MTOC, MMAT: MMAT, GOC: GOC, CO: CO, CAO_GOC: CAO_GOC, MOT_MET: MOT_MET, CHAN_TROI: CHAN_TROI,
    ghep: ghep, hinh: hinh, ve: ve, veThumb: veThumb, bongChan: bongChan, bongNga: bongNga, nuaVai: nuaVai, taiTruoc: taiTruoc,
    khiDoi: function (fn) { khiDoi = fn; } };
})();
