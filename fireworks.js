/* Timeless Harmony — pháo hoa chuyển động trên cảnh nền.
   liquid.js chỉ tải tệp này khi người dùng bấm "Bắn pháo hoa" hoặc chạm vào bầu trời lúc đang ngắm cảnh.

   Cách vẽ: một <canvas> ghim ngay trên ảnh nền, dưới mọi nội dung. Pháo bay theo vật lý thật (mét, giây: trọng lực,
   sức cản không khí), quy đổi ra điểm ảnh bằng đúng thông số máy ảnh của cảnh 3D, nên nó bắn lên từ sau cổng hoa và
   to nhỏ đúng tỉ lệ với khu vườn. Mặt nạ assets/bg/lake-*-mask.webp (kênh đỏ = vật đứng trước pháo, kênh lục = mặt hồ)
   xoá phần pháo bị cổng hoa, cây và khách che, và giới hạn ánh pháo hắt xuống đúng mặt hồ.
   Canvas chỉ chạy khi còn tia lửa; hết pháo thì dừng hẳn, không tốn máy.

   Dùng: THFire.volley() — một loạt pháo;  THFire.shellAt(x, y) — một quả nổ tại điểm (toạ độ màn hình);
         THFire.onidle = fn — gọi khi tia lửa cuối cùng tắt. */
(function () {
  'use strict';
  if (window.THFire) return;
  var doc = document, root = doc.documentElement;

  /* Hình học của cảnh, lấy từ docs/design (post_scene3d.py in ra oy và ppm mỗi lần xuất ảnh):
     ox, oy = gốc pháo trong ảnh (tỉ lệ); ppm = số điểm ảnh của ảnh ứng với 1 mét ở khoảng cách đó;
     fan = nửa góc xoè của dàn phun; vk = hệ số tốc độ (khung dọc bắn cao hơn cho đầy màn hình). */
  var SCENES = {
    land: { w: 2000, h: 1250, ox: 0.5, oy: 0.668, ppm: 23.7, fan: 60, vk: 1.0 },
    port: { w: 900, h: 1950, ox: 0.5, oy: 0.672, ppm: 23.4, fan: 44, vk: 1.22 }
  };
  var G = 9.81;
  var RAINBOW = [[255, 45, 111], [255, 59, 48], [255, 138, 31], [255, 208, 36], [128, 226, 52], [22, 220, 156],
                 [36, 172, 255], [84, 110, 255], [166, 96, 255], [240, 82, 214]];
  // màu của bông pháo: [ban ngày (đậm, nổi trên trời sáng), ban đêm (sáng, rực trên trời tối)]
  var TONES = {
    gold:   [[255, 168, 28], [255, 190, 78]],
    pink:   [[255, 64, 138], [255, 84, 150]],
    jade:   [[0, 196, 136], [40, 226, 160]],
    sky:    [[40, 134, 255], [70, 156, 255]],
    violet: [[150, 84, 255], [168, 110, 255]],
    coral:  [[255, 98, 64], [255, 112, 78]],
    white:  [[255, 246, 226], [255, 244, 222]]
  };

  var small = false, night = false, eco = root.classList.contains('lite');
  var scene, cv, cx, rc, rx, cw = 0, ch = 0, Q = 1;
  var dx = 0, dy = 0, dw = 0, dh = 0, X0 = 0, Y0 = 0, M = 1;          // ảnh nền trên màn hình; gốc pháo; điểm ảnh mỗi mét
  var masks = {}, mask = null, maskKey = '';
  var parts = [], rockets = [], emitters = [], queue = [];
  var now = 0, last = 0, raf = 0, tail = 0, shots = 0, slowFrames = 0, frames = 0;
  var api = { volley: volley, shellAt: shellAt, onidle: null, busy: function () { return !!raf; } };

  function rnd(a, b) { return a + Math.random() * (b - a); }
  function gauss() { return (Math.random() + Math.random() + Math.random() + Math.random() - 2) * 0.866; }   // ≈ N(0,1)
  function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }
  function css(c) { return 'rgb(' + (c[0] | 0) + ',' + (c[1] | 0) + ',' + (c[2] | 0) + ')'; }
  function mix(a, b, t) { return [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t]; }
  function tone(name) { return TONES[name][night ? 1 : 0]; }
  function rainbow(h) {
    var x = clamp(h, 0, 1) * (RAINBOW.length - 1), i = Math.min(x | 0, RAINBOW.length - 2);
    var c = mix(RAINBOW[i], RAINBOW[i + 1], x - i);
    return night ? mix(c, [255, 255, 255], 0.08) : c;
  }

  /* ── khung vẽ ── */
  function layout() {
    small = matchMedia('(max-width: 640px)').matches;
    scene = small ? SCENES.port : SCENES.land;
    var r = cv.getBoundingClientRect(), w = Math.round(r.width), h = Math.round(r.height);
    var q = eco ? 1 : Math.min(window.devicePixelRatio || 1, 1.5);
    if (w !== cw || h !== ch || q !== Q) {
      cw = w; ch = h; Q = q;
      cv.width = Math.round(cw * Q); cv.height = Math.round(ch * Q);
    }
    var s = Math.max(cw / scene.w, ch / scene.h);                      // background-size: cover
    dw = scene.w * s; dh = scene.h * s;
    dx = (cw - dw) / 2; dy = ch - dh;                                  // background-position: center bottom
    X0 = dx + scene.ox * dw; Y0 = dy + scene.oy * dh; M = scene.ppm * s;
    cx.lineCap = 'round';
    fitReflection();
  }
  function fitReflection() {
    if (!mask || !mask.band) { rc.style.display = 'none'; return; }
    var top = dy + mask.band[0] * dh, h = mask.band[1] * dh;
    rc.style.display = '';
    rc.style.top = top + 'px'; rc.style.height = h + 'px';
    rc.width = Math.max(2, Math.round(cw * 0.5)); rc.height = Math.max(2, Math.round(h * 0.4));     // độ phân giải thấp = ánh hắt mềm
    rc._top = top; rc._h = h;
  }
  function ensure() {
    if (cv) return;
    rc = doc.createElement('canvas'); cv = doc.createElement('canvas');
    rc.className = cv.className = 'th-sky th-keep';
    rc.setAttribute('aria-hidden', 'true'); cv.setAttribute('aria-hidden', 'true');
    doc.body.insertBefore(cv, doc.body.firstChild);
    doc.body.insertBefore(rc, cv);                                     // ánh hắt nằm dưới pháo
    cx = cv.getContext('2d'); rx = rc.getContext('2d');
    var t = 0;
    addEventListener('resize', function () { clearTimeout(t); t = setTimeout(function () { if (raf) layout(); else cw = 0; }, 120); }, { passive: true });
  }

  /* ── mặt nạ: tách kênh đỏ (vật che) và kênh lục (mặt hồ) của ảnh thành hai lớp alpha ── */
  function loadMask(done) {
    var key = (night ? 'night' : 'day') + (small ? '-m' : '');
    maskKey = key;
    if (masks[key]) { mask = masks[key]; return done(); }
    var img = new Image(), called = false;
    function go() { if (!called) { called = true; done(); } }
    mask = {};                                                         // chưa có mặt nạ
    setTimeout(go, 2500);                                              // mạng chậm: bắn luôn, mặt nạ về sau thì dùng ngay
    img.onload = function () {
      try {
        var w = img.naturalWidth, h = img.naturalHeight, tmp = doc.createElement('canvas');
        tmp.width = w; tmp.height = h;
        var g = tmp.getContext('2d', { willReadFrequently: true });
        g.drawImage(img, 0, 0);
        var a = g.getImageData(0, 0, w, h).data;
        var occ = g.createImageData(w, h), lake = g.createImageData(w, h), o = occ.data, l = lake.data;
        var y0 = h, y1 = 0, row, any, i, n = w * h;
        for (i = 0; i < n; i++) { o[i * 4 + 3] = a[i * 4]; l[i * 4 + 3] = a[i * 4 + 1]; }
        for (row = 0; row < h; row++) {                                // dải mặt hồ: hàng đầu và hàng cuối có nước
          any = false;
          for (i = row * w; i < row * w + w; i += 4) if (a[i * 4 + 1] > 128) { any = true; break; }
          if (any) { if (row < y0) y0 = row; y1 = row; }
        }
        var c1 = doc.createElement('canvas'), c2 = doc.createElement('canvas');
        c1.width = c2.width = w; c1.height = c2.height = h;
        c1.getContext('2d').putImageData(occ, 0, 0); c2.getContext('2d').putImageData(lake, 0, 0);
        masks[key] = { occ: c1, lake: c2, w: w, h: h, band: y1 > y0 ? [y0 / h, (y1 - y0 + 1) / h] : null };
        if (maskKey === key) { mask = masks[key]; if (raf) fitReflection(); }
      } catch (e) {}
      go();
    };
    img.onerror = go;
    img.src = '/assets/bg/lake-' + key + '-mask.webp';
  }

  /* ── tia lửa ── */
  function spark(x, z, vx, vz, life, col, w, o) {
    if (parts.length >= (small ? 1000 : 1700)) return;
    o = o || {};
    parts.push({ x: x, z: z, vx: vx, vz: vz, ax: x, az: z, bx: x, bz: z, age: 0, life: life, col: css(col), w: w,
                 k: o.k == null ? 0.55 : o.k, g: o.g == null ? 1 : o.g, a: o.a == null ? 1 : o.a, tw: o.tw || 0 });
  }

  /* Dàn phun cầu vồng: 13 họng xoè hình quạt sau cổng hoa, màu chạy từ hồng qua vàng, lục, lam tới tím. */
  function fan(sweep, reverse) {
    var visible = (Y0 - 24) / M, want = 29 * Math.pow(scene.vk, 1.6);
    var vk = scene.vk * Math.pow(Math.min(1, visible / want), 0.62);
    var half = Math.min(scene.fan, Math.atan2(cw / 2 / M * 1.15, want * 0.8) * 180 / Math.PI) * Math.PI / 180;
    var n = 13, rate = (small ? 26 : 40) * (eco ? 0.6 : 1), i, u, a0, d;
    for (i = 0; i < n; i++) {
      u = i / (n - 1); a0 = (u * 2 - 1) * half; d = Math.abs(u * 2 - 1);
      emitters.push({ a0: a0, ox: (u * 2 - 1) * 3, hue: reverse ? 1 - u : u, acc: 0, rate: rate * (1 - 0.33 * d), vk: vk * (1 - 0.1 * d * d),
                      t0: now + (sweep ? (reverse ? n - 1 - i : i) * 0.07 : 0), dur: 1.5 });
    }
  }
  function emit(e, dt) {
    if (now < e.t0) return true;
    if (now > e.t0 + e.dur) return false;
    e.acc += e.rate * dt;
    while (e.acc >= 1) {
      e.acc -= 1;
      var a = e.a0 + gauss() * 0.052, v = e.vk * rnd(26, 37);
      spark(e.ox, 0, Math.sin(a) * v, Math.cos(a) * v, rnd(1.7, 2.7), rainbow(e.hue + gauss() * 0.035), 0.16, { k: 0.55, tw: 0.25 });
    }
    return true;
  }

  /* Pháo bông: quả pháo bay lên rồi nổ thành một kiểu bông. */
  function launch(tx, tz, kind, delay) {
    var T = clamp(Math.sqrt(Math.max(tz, 6) / 26), 0.6, 1.25) * rnd(0.9, 1.08);
    rockets.push({ t0: now + (delay || 0), T: T, sx: tx * 0.22 + rnd(-1.5, 1.5), tx: tx, tz: tz, kind: kind, px: null, pz: 0 });
  }
  function skyRoom() { return clamp((Y0 - 46) / M, 12, 46); }                      // chiều cao bầu trời còn thấy được phía trên gốc pháo (mét)
  function sideRoom() { return clamp(cw / 2 / M * 0.78, 4, 22); }
  function burstSpeed() { return clamp(Math.min(skyRoom() * 0.3, sideRoom() * 0.62) * 1.55, 8.5, 17); }
  function burst(x, z, kind) {
    var V = burstSpeed(), n = Math.round((small ? 62 : 104) * (eco ? 0.65 : 1)), i, t, s, cth, sth, ph, v, c1, c2;
    var names = ['gold', 'pink', 'jade', 'sky', 'violet', 'coral'];
    flash(x, z, tone(kind === 'heart' ? 'pink' : kind === 'willow' ? 'gold' : 'white'), V);
    if (kind === 'heart') {                                                        // trái tim: tia bay theo đường cong hình tim, gần như không rơi
      c1 = tone('pink'); c2 = mix(c1, [255, 255, 255], 0.3);
      for (s = 0; s < 2; s++) for (i = 0; i < n * 0.6; i++) {
        t = (i / (n * 0.6)) * Math.PI * 2;
        v = V * (s ? 0.62 : 1.08) * rnd(0.97, 1.03) / 17;
        spark(x, z, 16 * Math.pow(Math.sin(t), 3) * v, (13 * Math.cos(t) - 5 * Math.cos(2 * t) - 2 * Math.cos(3 * t) - Math.cos(4 * t)) * v,
              rnd(1.7, 2.1), s ? c2 : c1, 0.2, { k: 1.7, g: 0.16, tw: 0.5 });
      }
      return;
    }
    if (kind === 'willow') {                                                       // liễu rủ: tia vàng rơi dài
      c1 = tone('gold');
      for (i = 0; i < n; i++) {
        cth = rnd(-1, 1); sth = Math.sqrt(1 - cth * cth); ph = rnd(0, Math.PI * 2); v = V * 0.82 * rnd(0.55, 1);
        spark(x, z, sth * Math.cos(ph) * v, cth * v, rnd(2.2, 3.0), mix(c1, tone('white'), rnd(0, 0.35)), 0.15, { k: 1.0, g: 0.5, tw: 0.8 });
      }
      return;
    }
    c1 = tone(kind && TONES[kind] ? kind : names[(Math.random() * names.length) | 0]);
    c2 = kind === 'duo' ? tone(names[(Math.random() * names.length) | 0]) : mix(c1, tone('white'), 0.6);
    for (i = 0; i < n; i++) {                                                      // cầu: hướng rải đều trên mặt cầu → dày ở viền như bông pháo thật
      cth = rnd(-1, 1); sth = Math.sqrt(1 - cth * cth); ph = rnd(0, Math.PI * 2);
      v = V * rnd(0.86, 1);
      spark(x, z, sth * Math.cos(ph) * v, cth * v, rnd(1.35, 1.9), c1, 0.19, { k: 1.35, g: 0.42, tw: 0.6 });
    }
    for (i = 0; i < n * 0.35; i++) {                                               // lõi sáng bên trong
      cth = rnd(-1, 1); sth = Math.sqrt(1 - cth * cth); ph = rnd(0, Math.PI * 2);
      v = V * 0.45 * rnd(0.7, 1);
      spark(x, z, sth * Math.cos(ph) * v, cth * v, rnd(0.9, 1.3), c2, 0.15, { k: 1.5, g: 0.42, tw: 0.3 });
    }
  }
  function flash(x, z, col, V) {
    var X = X0 + x * M, Y = Y0 - z * M, R = V * 0.5 * M, g = cx.createRadialGradient(X, Y, 0, X, Y, R);
    g.addColorStop(0, 'rgba(255,255,255,' + (night ? 0.9 : 0.75) + ')');
    g.addColorStop(0.25, 'rgba(' + (col[0] | 0) + ',' + (col[1] | 0) + ',' + (col[2] | 0) + ',0.45)');
    g.addColorStop(1, 'rgba(' + (col[0] | 0) + ',' + (col[1] | 0) + ',' + (col[2] | 0) + ',0)');
    cx.globalCompositeOperation = 'lighter'; cx.globalAlpha = 1; cx.fillStyle = g;
    cx.fillRect(X - R, Y - R, R * 2, R * 2);
    if (night) {                                                                   // đêm: cả vùng trời quanh bông pháo sáng lên một nhịp
      R *= 4.2; g = cx.createRadialGradient(X, Y, 0, X, Y, R);
      g.addColorStop(0, 'rgba(' + (col[0] | 0) + ',' + (col[1] | 0) + ',' + (col[2] | 0) + ',0.16)');
      g.addColorStop(0.35, 'rgba(' + (col[0] | 0) + ',' + (col[1] | 0) + ',' + (col[2] | 0) + ',0.07)');
      g.addColorStop(0.7, 'rgba(' + (col[0] | 0) + ',' + (col[1] | 0) + ',' + (col[2] | 0) + ',0.018)');
      g.addColorStop(1, 'rgba(' + (col[0] | 0) + ',' + (col[1] | 0) + ',' + (col[2] | 0) + ',0)');
      cx.fillStyle = g; cx.fillRect(X - R, Y - R, R * 2, R * 2);
    }
  }

  /* ── mỗi khung hình ── */
  function frame(t) {
    raf = 0;
    var dt = last ? (t - last) / 1000 : 0.016, i, p, e, r, u, x, z, f, a;
    last = t;
    if (dt > 0.05) { slowFrames++; dt = 0.034; }
    frames++;
    if (!eco && frames === 45 && slowFrames > 22) { eco = true; layout(); }       // máy đuối: giảm độ phân giải và số tia
    now += dt;

    while (queue.length && queue[0].t <= now) queue.shift().fn();
    for (i = emitters.length - 1; i >= 0; i--) if (!emit(emitters[i], dt)) emitters.splice(i, 1);

    // vệt cũ mờ dần (đuôi sao chổi), rồi vẽ đoạn đường mới của từng tia
    cx.setTransform(Q, 0, 0, Q, 0, 0);
    cx.globalCompositeOperation = 'destination-out'; cx.globalAlpha = 1 - Math.pow(0.8, dt * 60); cx.fillStyle = '#000';
    cx.fillRect(0, 0, cw, ch);
    cx.globalCompositeOperation = 'lighter';

    for (i = rockets.length - 1; i >= 0; i--) {
      r = rockets[i];
      if (now < r.t0) continue;
      u = (now - r.t0) / r.T;
      if (u >= 1) { rockets.splice(i, 1); burst(r.tx, r.tz, r.kind); continue; }
      f = 1 - Math.pow(1 - u, 2.1);
      x = r.sx + (r.tx - r.sx) * f + Math.sin(u * 16 + r.tx) * 0.12; z = r.tz * f;
      if (r.px !== null) {
        cx.globalAlpha = 0.9; cx.strokeStyle = css(tone('gold')); cx.lineWidth = Math.max(1.4, 0.2 * M);
        cx.beginPath(); cx.moveTo(X0 + r.px * M, Y0 - r.pz * M); cx.lineTo(X0 + x * M, Y0 - z * M); cx.stroke();
        if (Math.random() < 0.7) spark(x, z, rnd(-1.6, 1.6), rnd(-3, 0), rnd(0.25, 0.5), tone('gold'), 0.09, { k: 2, g: 0.6, a: 0.8 });
      }
      r.px = x; r.pz = z;
    }

    for (i = parts.length - 1; i >= 0; i--) {
      p = parts[i];
      p.age += dt;
      if (p.age >= p.life || p.z < -1.4) { parts[i] = parts[parts.length - 1]; parts.pop(); continue; }
      p.bx = p.ax; p.bz = p.az; p.ax = p.x; p.az = p.z;
      e = Math.exp(-p.k * dt);
      p.vx *= e; p.vz = p.vz * e - G * p.g * dt;
      p.x += p.vx * dt; p.z += p.vz * dt;
      f = p.age / p.life;
      a = p.a * (f < 0.08 ? 0.35 + f * 8 : 1) * (f > 0.72 ? (1 - f) / 0.28 : 1);
      if (p.tw && f > 0.55 && Math.random() < p.tw * 0.5) a *= 0.25;              // lấp lánh trước khi tắt
      cx.globalAlpha = a; cx.strokeStyle = p.col; cx.lineWidth = Math.max(1.1, p.w * M * (1 - 0.55 * f));
      cx.beginPath(); cx.moveTo(X0 + p.bx * M, Y0 - p.bz * M); cx.lineTo(X0 + p.x * M, Y0 - p.z * M); cx.stroke();
    }

    if (mask && mask.occ) {                                                        // cổng hoa, cây, khách… đứng trước pháo
      cx.globalCompositeOperation = 'destination-out'; cx.globalAlpha = 1;
      cx.drawImage(mask.occ, dx, dy, dw, dh);
    }
    if (mask && mask.lake && rc._h) reflect();

    if (parts.length || rockets.length || emitters.length || queue.length) tail = now;
    if (now - tail < 0.5) raf = requestAnimationFrame(frame);
    else stop();
  }
  /* Ánh pháo hắt xuống hồ: bản lật ngược, ép dẹt và làm mềm của bầu trời phía trên bờ xa, chỉ hiện trên mặt nước. */
  function reflect() {
    var w = rc.width, h = rc.height, srcH = Math.min(rc._top, rc._h / 0.3);
    rx.setTransform(1, 0, 0, 1, 0, 0);
    rx.globalCompositeOperation = 'source-over'; rx.clearRect(0, 0, w, h);
    if (srcH < 4) return;
    rx.globalAlpha = night ? 0.6 : 0.34;
    rx.setTransform(1, 0, 0, -1, 0, h);
    rx.drawImage(cv, 0, (rc._top - srcH) * Q, cw * Q, srcH * Q, 0, 0, w, h);
    rx.setTransform(1, 0, 0, 1, 0, 0);
    rx.globalCompositeOperation = 'destination-in'; rx.globalAlpha = 1;
    rx.drawImage(mask.lake, -dx / dw * mask.w, mask.band[0] * mask.h, cw / dw * mask.w, mask.band[1] * mask.h, 0, 0, w, h);
  }
  function stop() {
    cx.setTransform(1, 0, 0, 1, 0, 0); cx.clearRect(0, 0, cv.width, cv.height);
    rx.setTransform(1, 0, 0, 1, 0, 0); rx.clearRect(0, 0, rc.width, rc.height);
    cv.style.display = rc.style.display = 'none';
    last = 0; frames = slowFrames = 0;
    if (typeof api.onidle === 'function') api.onidle();
  }
  function run(fn) {
    ensure();
    var wasNight = night, wasSmall = small;
    night = !doc.body.classList.contains('light');
    cv.style.display = '';
    if (!raf) { if (!cw) layout(); else if (small !== matchMedia('(max-width: 640px)').matches) layout(); }
    var ready = function () {
      if (!raf) { layout(); tail = now; raf = requestAnimationFrame(frame); }
      fn();
    };
    if (mask && wasNight === night && wasSmall === small) ready(); else loadMask(ready);
  }

  /* ── kịch bản ── */
  function at(delay, fn) {
    queue.push({ t: now + delay, fn: fn });
    queue.sort(function (a, b) { return a.t - b.t; });
  }
  function shells(kinds, t0, gap) {
    var room = skyRoom(), side = sideRoom(), n = kinds.length;
    kinds.forEach(function (kind, i) {
      var u = n > 1 ? i / (n - 1) * 2 - 1 : 0;                                    // rải đều từ trái sang phải
      var high = kind === 'heart' ? 0.84 : rnd(0.55, 0.9) - Math.abs(u) * 0.1;
      launch(u * side * 0.82 + rnd(-1.5, 1.5), room * high, kind, t0 + i * gap + rnd(0, 0.12));
    });
  }
  function volley() {
    run(function () {
      shots++;
      var k = shots % 3;
      if (parts.length > (small ? 650 : 1100)) { shells([null, 'heart'], 0, 0.3); return; }      // đang dày tia: chỉ thêm bông pháo
      if (shots === 1) { fan(false, false); shells(['gold', 'heart', 'jade'], 0.55, 0.36); }
      else if (k === 2) { shells(['pink', 'duo', 'willow', 'sky', 'violet'].sort(function () { return Math.random() - 0.5; }), 0, 0.26); at(1.5, function () { shells(['heart'], 0, 0); }); }
      else if (k === 0) { fan(true, shots % 2 === 0); shells(['willow', 'willow'], 0.9, 0.5); at(1.9, function () { shells(['heart'], 0, 0); }); }
      else { fan(false, false); shells(['coral', 'heart', 'sky'], 0.5, 0.34); }
    });
  }
  function shellAt(clientX, clientY) {
    run(function () {
      var x = (clientX - X0) / M, z = (Y0 - clientY) / M;
      var kinds = [null, 'duo', 'heart', 'willow', null];
      launch(clamp(x, -sideRoom() * 1.3, sideRoom() * 1.3), clamp(z, 9, skyRoom() * 1.05), kinds[(Math.random() * kinds.length) | 0], 0);
    });
  }

  window.THFire = api;
})();
