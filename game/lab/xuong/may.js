/* Máy dựng nhân vật cho "Về chung một nhà": ghép các lớp tranh vẽ tay, nắn dáng, đổi màu, vẽ vào cảnh.
   Không chứa giao diện. Mọi thứ ở đây chạy trong trình duyệt, không gọi dịch vụ ngoài. */
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
  function lay(n) { if (!anh[n]) { anh[n] = new Image(); anh[n].onload = function () { khiDoi(); }; anh[n].src = 'nv/' + n + '.webp'; } return anh[n]; }
  function san(im) { return im.complete && im.naturalWidth; }
  function tao(w, h) { var c = document.createElement('canvas'); c.width = Math.max(1, Math.round(w)); c.height = Math.max(1, Math.round(h)); return c; }
  function tenDau(p) {
    var g = p.gt, v = p.vb, m = p.mat, t = p.toc;
    if (v === 'vua') return 'dau-' + (m === 'goc' && t === 'goc' ? g + '-goc' : m === 'goc' ? g + '-toc-' + t : t === 'goc' ? g + '-mat-' + m : g + '-' + m + '-' + t);
    return 'dau-' + g + '-' + v + (m !== 'goc' ? '-' + m : '') + (t !== 'goc' ? '-' + t : '');
  }
  function tenThan(p) { return (p.ao === 'aodai' ? 'ad-' : 'than-') + p.gt + '-' + (p.vb === 'vua' ? 'goc' : p.vb) + '-' + p.dang; }

  /* ---------- bộ nhớ có giới hạn ---------- */
  var KHOA_DANG = ['gt', 'vb', 'dang', 'mat', 'mt', 'may', 'toc', 'ao', 'da', 'mtoc', 'mm', 'vai', 'bung', 'hong']; // không có chiều cao, tên
  function khoa(p) { return KHOA_DANG.map(function (k) { return p[k] == null ? 0 : p[k]; }).join('|'); }
  function nho(map, key, val, max) { map.delete(key); map.set(key, val); if (map.size > max) map.delete(map.keys().next().value); }
  var nhoLon = new Map(), nhoNho = new Map();

  /* ---------- màu ---------- */
  function luma(r, g, b) { return (0.3 * r + 0.59 * g + 0.11 * b) / 255; }
  function sacDo(r, g, b) { // [sắc độ°, độ đậm, độ sáng]
    var mx = Math.max(r, g, b), mn = Math.min(r, g, b), dd = mx - mn || 1e-6, h;
    if (mx === r) h = ((g - b) / dd) % 6; else if (mx === g) h = (b - r) / dd + 2; else h = (r - g) / dd + 4;
    h *= 60; if (h < 0) h += 360; return [h, mx ? (mx - mn) / mx : 0, mx / 255];
  }
  function bac3(st3, l) { // độ sáng l (0..1) → ba nấc màu
    var t = Math.min(1, Math.max(0, l)), a, b, u;
    if (t < 0.5) { a = st3[0]; b = st3[1]; u = t / 0.5; } else { a = st3[1]; b = st3[2]; u = (t - 0.5) / 0.5; }
    return [a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u, a[2] + (b[2] - a[2]) * u];
  }
  function doc(v, a, b) { return Math.min(1, Math.max(0, (v - a) / (b - a))); }
  function mem(v, a, b) { var t = doc(v, a, b); return t * t * (3 - 2 * t); }
  function mo(w, W, H, r) { // làm mờ hộp tách hai chiều
    var t = new Float32Array(w.length), x, y, s;
    for (y = 0; y < H; y++) { s = 0; var o = y * W;
      for (x = -r; x <= r; x++) s += w[o + Math.min(W - 1, Math.max(0, x))];
      for (x = 0; x < W; x++) { t[o + x] = s / (2 * r + 1); s += w[o + Math.min(W - 1, x + r + 1)] - w[o + Math.max(0, x - r)]; } }
    for (x = 0; x < W; x++) { s = 0;
      for (y = -r; y <= r; y++) s += t[Math.min(H - 1, Math.max(0, y)) * W + x];
      for (y = 0; y < H; y++) { w[y * W + x] = s / (2 * r + 1); s += t[Math.min(H - 1, y + r + 1) * W + x] - t[Math.max(0, y - r) * W + x]; } }
  }
  var DA_GOC = { nam: [232, 190, 150], nu: [244, 210, 182] }; // màu da trung bình của tranh gốc (đo trên ảnh)

  /* Đổi màu trên MỘT lớp. Tóc và mắt chỉ được gọi trên lớp đầu, nên không thể loang sang trang phục.
     o: { da, toc, mat, top } ; r: tỉ lệ thu nhỏ của lớp (để bán kính làm mờ co theo). */
  function doiMau(x, W, H, p, manh, o, r) {
    var da = o.da && DA[p.da].m, bt = o.toc && MTOC[p.mtoc].m, bm = o.mat && MMAT[p.mm].m;
    if (!da && !bt && !bm) return;
    var img = x.getImageData(0, 0, W, H), a = img.data, n = W * H, i, j, k, v, l, hs;
    function R(px) { return Math.max(1, Math.round(px * r)); }
    var wToc = null, wTrong = null, wDa = null;
    if (bt) {
      // 1) điểm có thể là tóc: tối, ấm hoặc xám
      var can = new Uint8Array(n), e = new Float32Array(n);
      for (i = 0; i < n; i++) { j = i * 4; if (a[j + 3] < 90) continue; l = luma(a[j], a[j + 1], a[j + 2]); if (l > 0.62) continue; hs = sacDo(a[j], a[j + 1], a[j + 2]);
        if ((hs[0] <= 55 || hs[0] >= 330) && (l < 0.5 || hs[1] > 0.25) || hs[1] < 0.2 && l < 0.5) { can[i] = 1; e[i] = 1; } }
      mo(e, W, H, R(2)); // e cao = nằm trong khối dày (tóc), e thấp = nét mảnh (viền mặt, lông mi)
      // 2) loang từ đỉnh đầu qua khối dày
      var toc = new Uint8Array(n), q = new Int32Array(n), dau = 0, cuoi = 0, top = Math.min(H, o.top || Math.round(H * 0.12));
      for (i = 0; i < W * top; i++) if (can[i] && e[i] > 0.7) { toc[i] = 1; q[cuoi++] = i; }
      function ke(k) { var xx = k % W; return [k - W, k + W, xx > 0 ? k - 1 : -1, xx < W - 1 ? k + 1 : -1]; }
      while (dau < cuoi) { k = ke(q[dau++]); for (i = 0; i < 4; i++) { v = k[i]; if (v >= 0 && v < n && !toc[v] && can[v] && e[v] > 0.7) { toc[v] = 1; q[cuoi++] = v; } } }
      // 3) đi tiếp theo nét mảnh (tóc mai, lọn rủ) nhưng chỉ một quãng ngắn, để không chạy dọc viền mặt
      var xa = new Uint16Array(n), gh = R(70); dau = 0;
      while (dau < cuoi) { var u = q[dau++]; if (xa[u] >= gh) continue; k = ke(u); for (i = 0; i < 4; i++) { v = k[i]; if (v >= 0 && v < n && !toc[v] && can[v]) { toc[v] = 1; xa[v] = xa[u] + 1; q[cuoi++] = v; } } }
      manh.forEach(function (qq) {
        var x0 = Math.max(0, Math.floor(qq.x)), x1 = Math.min(W, Math.ceil(qq.x + qq.w)), y0 = Math.max(0, Math.floor(qq.y)), y1 = Math.min(H, Math.ceil(qq.y + qq.h)), xx, yy, t;
        for (yy = y0; yy < y1; yy++) for (xx = x0; xx < x1; xx++) { t = yy * W + xx;
          if (qq.loai === 'mat') { var ex = (xx - qq.x - qq.w / 2) / (qq.w * 0.4), ey = (yy - qq.y - qq.h / 2) / (qq.h * 0.4); if (ex * ex + ey * ey < 1) toc[t] = 0; } // không tô mắt bằng màu tóc
          else if (can[t] && luma(a[t * 4], a[t * 4 + 1], a[t * 4 + 2]) < 0.42) toc[t] = 1; }          // lông mày theo màu tóc
      });
      wToc = new Float32Array(n); for (i = 0; i < n; i++) wToc[i] = toc[i];
      mo(wToc, W, H, 1); for (i = 0; i < n; i++) wToc[i] = Math.min(1, wToc[i] * 1.6);
    }
    if (bm) { wTrong = new Float32Array(n); manh.forEach(function (qq) { if (qq.loai !== 'mat') return; // tròng mắt: chỉ quanh tâm mảnh mắt
      var cx = qq.x + qq.w / 2, cy = qq.y + qq.h / 2, rx = qq.w * 0.24, ry = qq.h * 0.14, xx, yy;
      for (yy = Math.max(0, Math.floor(cy - ry)); yy < Math.min(H, cy + ry); yy++) for (xx = Math.max(0, Math.floor(cx - rx)); xx < Math.min(W, cx + rx); xx++) {
        var t = yy * W + xx, j2 = t * 4, l2 = luma(a[j2], a[j2 + 1], a[j2 + 2]), h2 = sacDo(a[j2], a[j2 + 1], a[j2 + 2]);
        if (l2 > 0.16 && l2 < 0.62 && h2[1] > 0.3 && (h2[0] < 50 || h2[0] > 340)) wTrong[t] = doc(l2, 0.16, 0.24) * (1 - doc(l2, 0.52, 0.62)); } }); }
    if (da) { // da: lõi chắc chắn là da, rồi lấp các mảng sáng ít màu nằm trong vùng da (vai, ngực bắt nắng)
      var loi = new Float32Array(n), nhat = new Float32Array(n); wDa = new Float32Array(n);
      for (i = 0; i < n; i++) { j = i * 4; if (a[j + 3] < 160) continue; hs = sacDo(a[j], a[j + 1], a[j + 2]);
        var cv = doc(hs[0], 32, 36) * (1 - doc(hs[0], 46, 50)) * doc(hs[1], 0.22, 0.27) * (1 - doc(hs[2], 0.8, 0.86)); // cà vạt, chỉ thêu vàng
        var sac = doc(hs[0], 4, 12) * (1 - doc(hs[0], 48, 54)) * (1 - cv), sang = doc(hs[2], 0.28, 0.42) * doc(a[j + 3], 160, 230);
        loi[i] = sac * doc(hs[1], 0.17, 0.22) * (1 - doc(hs[1], 0.6, 0.72)) * sang;
        nhat[i] = Math.max(1 - doc(hs[1], 0.04, 0.08), doc(hs[0], 0, 6) * (1 - doc(hs[0], 58, 66))) * (1 - cv) * sang; }
      var dong = new Float32Array(loi); mo(dong, W, H, R(14));
      for (i = 0; i < n; i++) dong[i] = dong[i] > 0.04 ? 1 : 0;
      mo(dong, W, H, R(10));
      for (i = 0; i < n; i++) wDa[i] = Math.max(loi[i], (dong[i] > 0.9 ? 1 : 0) * nhat[i]);
      mo(wDa, W, H, R(2));
    }
    var tl = da ? [da[0] / DA_GOC[p.gt][0], da[1] / DA_GOC[p.gt][1], da[2] / DA_GOC[p.gt][2]] : null;
    for (i = 0; i < n; i++) {
      j = i * 4; if (a[j + 3] < 10) continue; var r0 = a[j], g0 = a[j + 1], b0 = a[j + 2], Rr = r0, G = g0, B = b0, w;
      if (tl && wDa[i] > 0.01) { w = Math.min(1, wDa[i] * 1.15); Rr += (Math.min(255, r0 * tl[0]) - r0) * w; G += (Math.min(255, g0 * tl[1]) - g0) * w; B += (Math.min(255, b0 * tl[2]) - b0) * w; }
      if (bt && wToc[i] > 0.01) { var lt = luma(r0, g0, b0), c3 = bac3(bt, lt / 0.5); w = wToc[i] * (1 - doc(lt, 0.5, 0.64)); Rr += (c3[0] - Rr) * w; G += (c3[1] - G) * w; B += (c3[2] - B) * w; }
      if (bm && wTrong[i] > 0.01) { var c4 = bac3(bm, luma(r0, g0, b0) / 0.55); Rr += (c4[0] - Rr) * wTrong[i]; G += (c4[1] - G) * wTrong[i]; B += (c4[2] - B) * wTrong[i]; }
      a[j] = Rr; a[j + 1] = G; a[j + 2] = B;
    }
    x.putImageData(img, 0, 0);
  }

  /* ---------- nắn dáng: vai, eo-bụng, hông, 7 mức mỗi trục (−3…+3) ----------
     Mỗi hàng điểm ảnh của lớp thân được co giãn quanh trục người. Trong vùng có cánh tay, chỉ phần thân giữa co giãn,
     phần ngoài (tay, bàn tay) dời theo nguyên hình. Tỉ lệ "thân giữa" chuyển mềm ở hai đầu vùng tay nên không có bậc. */
  var DAI = { nam: { vai: [0.225, 0.05], bung: [0.40, 0.055], hong: [0.50, 0.05], tay: [0.19, 0.6], loi: 0.62 },
    nu: { vai: [0.235, 0.045], bung: [0.37, 0.05], hong: [0.47, 0.055], tay: [0.21, 0.5], loi: 0.55 } };
  var MUC = { vai: 0.05, bung: 0.065, hong: 0.05 };
  var bien = {}, tam = tao(1, 1);
  function bienHang(img, ms, key) { // mép trái, phải của người ở từng hàng
    if (bien[key]) return bien[key];
    var c = tao(ms.w, ms.h), t = c.getContext('2d'); t.drawImage(img, 0, 0, ms.w, ms.h);
    var a = t.getImageData(0, 0, ms.w, ms.h).data, r = new Float32Array(ms.h * 2);
    for (var y = 0; y < ms.h; y++) { var x0 = -1, x1 = -1; for (var x = 0; x < ms.w; x++) if (a[(y * ms.w + x) * 4 + 3] > 100) { if (x0 < 0) x0 = x; x1 = x; } r[y * 2] = x0; r[y * 2 + 1] = x1; }
    return (bien[key] = r);
  }
  function chuong(f, d) { var z = (f - d[0]) / d[1]; return Math.exp(-0.5 * z * z); }
  function nan(x, img, ms, p, bh, yMax) {
    var a = p.vai | 0, b = p.bung | 0, c = p.hong | 0;
    if (!a && !b && !c) { x.drawImage(img, 0, 0, ms.w, ms.h); return; }
    tam.width = ms.w; tam.height = ms.h; var t = tam.getContext('2d'); t.clearRect(0, 0, ms.w, ms.h); t.drawImage(img, 0, 0, ms.w, ms.h);
    var D = DAI[p.gt], cx = ms.cx * ms.w, n = Math.min(ms.h, Math.ceil(yMax));
    for (var y = 0; y < n; y++) {
      var f = y / ms.h, k = 1 + MUC.vai * a * chuong(f, D.vai) + MUC.bung * b * chuong(f, D.bung) + MUC.hong * c * chuong(f, D.hong);
      if (c > 0 && p.gt === 'nu' && f > D.hong[0]) k = Math.max(k, 1 + 0.03 * c); // váy xoè theo hông
      var x0 = bh[y * 2], x1 = bh[y * 2 + 1];
      if (x0 < 0 || Math.abs(k - 1) < 0.002) { x.drawImage(tam, 0, y, ms.w, 1, 0, y, ms.w, 1); continue; }
      var s = mem(f, D.tay[0] - 0.03, D.tay[0] + 0.03) * (1 - mem(f, D.tay[1] - 0.03, D.tay[1] + 0.03));
      var e = Math.max(cx - x0, x1 - cx) + 1, T = e * (1 - (1 - D.loi) * s), L = Math.max(0, cx - T), Rr = Math.min(ms.w, cx + T), d = T * (k - 1);
      x.drawImage(tam, L, y, Rr - L, 1, cx - (cx - L) * k, y, (Rr - L) * k, 1);
      if (L > 0) x.drawImage(tam, 0, y, L, 1, -d, y, L, 1);
      if (Rr < ms.w) x.drawImage(tam, Rr, y, ms.w - Rr, 1, Rr + d, y, ms.w - Rr, 1);
    }
  }

  function danhSang(x, W, H) { // tranh vẽ nắng từ trái; đánh lại: tối dần sang trái, viền nắng ấm ở mép phải, khớp nắng của cảnh
    var img = x.getImageData(0, 0, W, H), a = img.data, vien = Math.max(2, W * 0.012);
    for (var y = 0; y < H; y++) {
      var o = y * W, x0 = -1, x1 = -1, i;
      for (i = 0; i < W; i++) if (a[(o + i) * 4 + 3] > 128) { if (x0 < 0) x0 = i; x1 = i; }
      if (x0 < 0 || x1 - x0 < 4) continue;
      for (i = x0; i <= x1; i++) {
        var j = (o + i) * 4; if (a[j + 3] < 10) continue;
        var t = (i - x0) / (x1 - x0), k = 0.9 + 0.2 * t, r = Math.max(0, 1 - (x1 - i) / vien) * 0.3;
        a[j] = Math.min(255, a[j] * k + (255 - a[j]) * r); a[j + 1] = Math.min(255, a[j + 1] * k + (236 - a[j + 1]) * r * 0.9); a[j + 2] = Math.min(255, a[j + 2] * k + (205 - a[j + 2]) * r * 0.7);
      }
    }
    x.putImageData(img, 0, 0);
  }

  /* ---------- ghép một nhân vật ----------
     Thứ tự: thân (đã nắn, đổi màu da) → đầu (đầu + lông mày + mắt; đổi màu da, tóc, mắt trên riêng lớp này) → cổ áo dài.
     o.ti: thu nhỏ; o.cao: chỉ dựng phần trên (0..1). Bản đủ cỡ được nhớ lại. */
  function manhCua(p, ti, ds) {
    var out = []; if (!MANH) return out;
    var M = MANH[p.gt], vt = M.vitri[tenDau(p)]; if (!vt) return out;
    [['may', p.may], ['mat', p.mt]].forEach(function (k) {
      if (k[0] === 'may' && p.gt === 'nu' && p.toc === 'ngan') return; // tóc mái che lông mày
      var bo = M.manh[k[0]] && M.manh[k[0]][p.mat] && M.manh[k[0]][p.mat][k[1]]; if (!bo) return;
      bo.forEach(function (mm, i) { if (mm) { var im = lay(mm.f); ds.push(im); out.push({ im: im, x: vt[k[0]][i][0] * ti, y: vt[k[0]][i][1] * ti, w: mm.w * ti, h: mm.h * ti, loai: k[0] }); } });
    });
    return out;
  }
  function ghep(p, o) {
    o = o || {}; var ti = o.ti || 1, frac = o.cao || 1, du = ti === 1 && frac === 1, key = khoa(p);
    if (du && nhoLon.has(key)) { var cu = nhoLon.get(key); nho(nhoLon, key, cu, 6); return cu; }
    var m = META[p.gt], tT = tenThan(p), th = lay(tT), d = lay(tenDau(p)), ds = [th, d], co = null;
    if (p.ao === 'aodai') { co = lay('co-' + tT); ds.push(co); }
    var manh = manhCua(p, ti, ds);
    if (!ds.every(san)) return null;
    var ms = { w: Math.round(m.w * ti), h: Math.round(m.h * ti), hdau: m.hdau * ti, cx: m.cx };
    var Hc = Math.max(1, Math.round(ms.h * frac)), c = tao(ms.w, Hc), x = c.getContext('2d');
    var bh = bienHang(th, ms, tT + '@' + ms.w);
    // Ảnh áo dài được mô hình vẽ thấp hơn đầu khoảng 14/2600 chiều cao (đo bằng tương quan vùng mặt): kéo lên cho khớp cằm, giữ chân.
    var dy = p.ao === 'aodai' ? ms.h * 14 / 2600 : 0;
    function lopThan(img) {
      if (!dy) { nan(x, img, ms, p, bh, Hc); return; }
      var tb = tao(ms.w, ms.h); nan(tb.getContext('2d'), img, ms, p, bh, Hc + dy + 2); x.drawImage(tb, 0, -dy, ms.w, ms.h + dy);
    }
    lopThan(th);
    doiMau(x, ms.w, Hc, p, [], { da: 1 }, ti);
    var hH = Math.min(Hc, Math.ceil(ms.hdau)), hc = tao(ms.w, hH), hx = hc.getContext('2d');
    hx.drawImage(d, 0, 0, ms.w, ms.hdau);
    manh.forEach(function (q) { hx.drawImage(q.im, q.x, q.y, q.w, q.h); });
    doiMau(hx, ms.w, hH, p, manh, { da: 1, toc: 1, mat: 1, top: Math.round(ms.h * 0.08) }, ti);
    x.drawImage(hc, 0, 0);
    if (co) lopThan(co); // cổ áo cao che cổ sơ mi và voan của lớp đầu; nắn cùng công thức với thân
    // Tranh nguồn đã lật ngang từ trước; lật lại cho đúng chi tiết trang phục (hoa cài áo, vạt áo), rồi đánh sáng theo cảnh.
    var f = tao(ms.w, Hc), fx = f.getContext('2d');
    fx.translate(ms.w, 0); fx.scale(-1, 1); fx.drawImage(c, 0, 0); fx.setTransform(1, 0, 0, 1, 0, 0);
    danhSang(fx, ms.w, Hc);
    if (du) nho(nhoLon, key, f, 6);
    return f;
  }

  /* ---------- hình xem trước cho thẻ chọn ---------- */
  function veThumb(cv, p, khung) {
    var key = khoa(p) + '#' + khung + '#' + cv.width + 'x' + cv.height, t = nhoNho.get(key);
    if (!t) {
      var m = META[p.gt], asp = cv.width / cv.height, c, sx, sy, sw, sh, ti;
      if (khung === 'nguoi') { ti = Math.min(1, Math.max(0.2, cv.height * 1.05 / m.h)); c = ghep(p, { ti: ti }); if (!c) return false; sh = c.height; sw = sh * asp; sx = (1 - m.cx) * c.width - sw / 2; sy = 0; }
      else if (khung === 'mat') {
        c = ghep(p, { cao: 0.215 }); if (!c) return false;
        var vt = MANH && MANH[p.gt].vitri[tenDau(p)], bo = MANH && MANH[p.gt].manh.mat[p.mat] && MANH[p.gt].manh.mat[p.mat][p.mt];
        if (vt && bo && bo[0] && bo[1]) { var xa = vt.mat[0][0] + bo[0].w / 2, xb = vt.mat[1][0] + bo[1].w / 2, yc = (vt.mat[0][1] + bo[0].h / 2 + vt.mat[1][1] + bo[1].h / 2) / 2;
          sw = Math.abs(xa - xb) * 2.9; sh = sw / asp; sx = m.w - (xa + xb) / 2 - sw / 2; sy = yc - sh * 0.62; }
        else { sw = m.w * 0.3; sh = sw / asp; sx = (1 - m.cx) * m.w - sw / 2; sy = m.h * 0.08; }
      } else { ti = Math.min(1, Math.max(0.3, cv.height / (0.27 * m.h))); c = ghep(p, { ti: ti, cao: 0.3 }); if (!c) return false; sh = 0.27 * m.h * ti; sw = sh * asp; sx = (1 - m.cx) * c.width - sw / 2; sy = 0; }
      t = tao(cv.width, cv.height); var tx = t.getContext('2d'); tx.imageSmoothingQuality = 'high'; tx.drawImage(c, sx, sy, sw, sh, 0, 0, cv.width, cv.height);
      nho(nhoNho, key, t, 90);
    }
    var x = cv.getContext('2d'); x.clearRect(0, 0, cv.width, cv.height); x.drawImage(t, 0, 0); return true;
  }

  /* ---------- vẽ vào cảnh ----------
     Phối cảnh đo trên tranh nền: 1 m tại chân y (% khung) cao 0,307 × (y − 44) % chiều cao khung. */
  var CHAN_TROI = 44, MOT_MET = 0.307, CAO_GOC = { nam: 172, nu: 158 }, CO = { nam: 0.194, nu: 0.2 };
  // Chân ở (X, Y) px, k px mỗi cm. Đầu gần như không đổi cỡ theo chiều cao (∝ cao^0,3); phần dưới cổ co giãn bù vào.
  // Bề ngang chuyển mềm qua cổ để không có bậc giữa đầu và thân.
  function ve(x, p, X, Y, k) {
    var m = META[p.gt], c = ghep(p); if (!c) return null;
    var r = p.cao / CAO_GOC[p.gt], Hg = CAO_GOC[p.gt] * k / (1 - m.dinh), Wg = Hg * m.w / m.h;
    var sd = Math.pow(r, 0.3), hDau = Hg * CO[p.gt] * sd, wDau = Wg * sd;
    var hThan = p.cao * k / (1 - m.dinh) - hDau, wThan = Wg * Math.pow(r, 0.6), H = hDau + hThan;
    var cut = m.h * CO[p.gt], ax = 1 - m.cx, sy1 = hDau / cut, sy2 = hThan / (m.h - cut), T = Y - H;
    if (Math.abs(wDau - wThan) < 0.4) {
      x.drawImage(c, 0, 0, m.w, cut, X - ax * wDau, T, wDau, hDau + 0.5);
      x.drawImage(c, 0, cut, m.w, m.h - cut, X - ax * wThan, Y - hThan, wThan, hThan);
    } else {
      var b = m.h * 0.014, N = 8, y0 = cut - b, y1 = cut + b, i;
      x.drawImage(c, 0, 0, m.w, y0, X - ax * wDau, T, wDau, y0 * sy1 + 0.5);
      for (i = 0; i < N; i++) {
        var s0 = y0 + (y1 - y0) * i / N, s1 = y0 + (y1 - y0) * (i + 1) / N, t = (i + 0.5) / N, w = wDau + (wThan - wDau) * (t * t * (3 - 2 * t));
        var d0 = s0 < cut ? s0 * sy1 : hDau + (s0 - cut) * sy2, d1 = s1 <= cut ? s1 * sy1 : hDau + (s1 - cut) * sy2;
        x.drawImage(c, 0, s0, m.w, s1 - s0, X - ax * w, T + d0, w, d1 - d0 + 0.5);
      }
      var dT = hDau + (y1 - cut) * sy2; x.drawImage(c, 0, y1, m.w, m.h - y1, X - ax * wThan, T + dT, wThan, H - dT);
    }
    return { w: Math.max(wDau, wThan), h: H };
  }
  function bongChan(x, cx, cy, rx) { // bóng tiếp xúc dưới chân
    var ry = rx * 0.2, g = x.createRadialGradient(0, 0, 0, 0, 0, 1);
    g.addColorStop(0, 'rgba(34,44,26,.62)'); g.addColorStop(0.6, 'rgba(34,44,26,.28)'); g.addColorStop(1, 'rgba(34,44,26,0)');
    x.save(); x.translate(cx - rx * 0.12, cy + ry * 0.1); x.scale(rx, ry); x.fillStyle = g; x.beginPath(); x.arc(0, 0, 1, 0, Math.PI * 2); x.fill(); x.restore();
  }
  // Bóng ngả dựng từ chính hình vẽ: (x, độ cao u) → (x − 0,75u, chân + 0,2u), cùng hướng với bóng bàn ghế trong tranh nền.
  var off = tao(1, 1), dsMo = [];
  function bongNga(x, ds, w, h) {
    off.width = w; off.height = h; var o = off.getContext('2d');
    ds.forEach(function (d) { o.setTransform(1, 0, 0.75, -0.2, -0.75 * d.y, 1.2 * d.y); ve(o, d.p, d.x, d.y, d.k); });
    o.setTransform(1, 0, 0, 1, 0, 0); o.globalCompositeOperation = 'source-in';
    var fy = ds[0].y, dai = ds[0].p.cao * ds[0].k * 0.2, g = o.createLinearGradient(0, fy, 0, fy + dai);
    g.addColorStop(0, 'rgba(40,54,30,1)'); g.addColorStop(1, 'rgba(40,54,30,.4)'); o.fillStyle = g; o.fillRect(0, 0, w, h);
    // Làm mờ bằng cách thu nhỏ một nửa nhiều lần rồi phóng lại (mượt, chạy được cả trên Safari); bóng càng to càng mờ.
    var buoc = Math.max(1, Math.min(4, Math.round(Math.log2(ds[0].p.cao * ds[0].k * 0.012)) + 1)), nguon = off, cw = w, ch = h, i;
    for (i = 0; i < buoc; i++) { var dich = dsMo[i] || (dsMo[i] = tao(1, 1)); cw = Math.max(1, Math.ceil(cw / 2)); ch = Math.max(1, Math.ceil(ch / 2)); dich.width = cw; dich.height = ch;
      var dx = dich.getContext('2d'); dx.imageSmoothingQuality = 'high'; dx.drawImage(nguon, 0, 0, cw, ch); nguon = dich; }
    x.save(); x.globalAlpha = 0.62; x.imageSmoothingQuality = 'high'; x.drawImage(nguon, 0, 0, w, h); x.restore();
  }
  // Nửa bề ngang vai thật (cm), không tính voan hay khoảng trống của ảnh.
  function nuaVai(p) { return (p.gt === 'nam' ? 23 : 19) * ({ manh: 0.92, vua: 1, day: 1.15 })[p.vb] * (1 + 0.05 * (p.vai | 0)) * Math.pow(p.cao / CAO_GOC[p.gt], 0.6); }

  fetch('nv/manh.json').then(function (r) { return r.json(); }).then(function (j) { MANH = j; nhoLon.clear(); nhoNho.clear(); khiDoi(); }).catch(function () {});

  return { META: META, CHON: CHON, DA: DA, MTOC: MTOC, MMAT: MMAT, GOC: GOC, CO: CO, CAO_GOC: CAO_GOC, MOT_MET: MOT_MET, CHAN_TROI: CHAN_TROI,
    ghep: ghep, ve: ve, veThumb: veThumb, bongChan: bongChan, bongNga: bongNga, nuaVai: nuaVai,
    khiDoi: function (fn) { khiDoi = fn; } };
})();
