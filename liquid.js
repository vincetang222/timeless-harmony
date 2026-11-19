/* Timeless Harmony — kính lỏng. Bốn phần, phần nào hỏng thì trang vẫn dùng được:
   1. Vệt sáng chạy theo con trỏ trên các tấm kính (chỉ thiết bị có chuột).
   2. Bộ điều tiết độ mượt: máy yếu → html.lite.
   3. Kính dựng sẵn: tấm kính lớn dùng ảnh nền đã làm mờ sẵn thay cho backdrop-filter → html.pre.
   4. Sân khấu: nút "Bắn pháo hoa" và "Ngắm cảnh" (pháo hoa nằm ở /fireworks.js, chỉ tải khi cần). */

/* 1. Vệt sáng: đặt biến --lx/--ly (px, tính từ góc trên-trái của tấm) để theme.css vẽ quầng sáng. */
(function () {
  var doc = document;
  if (!window.matchMedia || !matchMedia('(hover: hover) and (pointer: fine)').matches) return;
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var SHINE = '.glass, .glass-strong, .hero-copy, .hero, .page-header, .page-hero, .article-hero, body > section, .cats-section, .sup-section, #pageContent > .wrap, .articles, .article-body, .related, .content, .welcome, .planner-box, .newsletter-box, footer';
  var current = null, raf = 0, last = null;
  function clear() { if (current) { current.style.removeProperty('--lx'); current.style.removeProperty('--ly'); current = null; } }
  function paint() {
    raf = 0;
    if (!last) return;
    if (doc.documentElement.classList.contains('lite')) { clear(); return; }   // chế độ nhẹ: không vẽ vệt sáng
    var t = last.target, el = t && t.closest ? t.closest(SHINE) : null;
    if (current !== el) clear();
    current = el;
    if (!el) return;
    var r = el.getBoundingClientRect();
    el.style.setProperty('--lx', (last.clientX - r.left) + 'px');
    el.style.setProperty('--ly', (last.clientY - r.top) + 'px');
  }
  doc.addEventListener('pointermove', function (e) { last = e; if (!raf) raf = requestAnimationFrame(paint); }, { passive: true });
  doc.documentElement.addEventListener('pointerleave', clear);
})();

/* Bộ điều tiết độ mượt: máy yếu thì chuyển sang "chế độ nhẹ" (html.lite — bỏ làm mờ nền, xem theme.css mục 9).
   Bật ngay nếu trình duyệt báo tiết kiệm dữ liệu hoặc RAM ≤ 2 GB. Ngoài ra đo nhịp khung hình trong lúc người dùng
   cuộn trang: hai lượt đo liên tiếp dưới ~28 khung/giây (khoảng 2–3 giây cuộn giật) thì bật và ghi nhớ 7 ngày. */
(function () {
  var root = document.documentElement, KEY = 'th-lite';
  if (root.classList.contains('lite') || !window.requestAnimationFrame) return;
  function lite(remember) {
    root.classList.add('lite');
    if (remember) try { localStorage.setItem(KEY, String(Date.now())); } catch (e) {}
  }
  var conn = navigator.connection || {};
  if (conn.saveData || (navigator.deviceMemory && navigator.deviceMemory <= 2)) { lite(false); return; }
  var WINDOW = 30, SLOW_MS = 36, NEEDED = 2;      // 2 cửa sổ × 30 khung hình chậm liên tiếp ≈ 2–3 giây cuộn giật
  var started = performance.now(), lastScroll = 0, prev = 0, n = 0, sum = 0, slow = 0, raf = 0, done = false;
  function tick(t) {
    raf = 0;
    if (done) return;
    if (t - lastScroll > 140 || document.hidden) { prev = 0; return; }       // hết cuộn: nghỉ đo
    if (prev && t - started > 2000) {
      var d = t - prev;
      if (d < 250) { sum += d; n++; }                                          // bỏ qua khoảng dừng bất thường
      if (n >= WINDOW) {
        slow = sum / n > SLOW_MS ? slow + 1 : 0;
        n = 0; sum = 0;
        if (slow >= NEEDED) { done = true; lite(true); return; }
      }
    }
    prev = t;
    raf = requestAnimationFrame(tick);
  }
  addEventListener('scroll', function () {
    lastScroll = performance.now();
    if (!raf && !done) raf = requestAnimationFrame(tick);
  }, { passive: true });
})();

/* 3. Kính dựng sẵn (theme.css mục 7b). Chèn <i class="gl"><b></b></i> vào từng tấm kính lớn đang làm mờ nền; khi ảnh mờ
   sẵn đã tải xong thì bật html.pre: các tấm đó chuyển từ backdrop-filter sang ảnh ghim (<b>, position: fixed).
   Tự kiểm: ảnh ghim phải phủ đúng khung nhìn. Nếu một phần tử bao ngoài có transform/filter (hoặc trình duyệt xử lý
   khác đi), ảnh sẽ bám theo phần tử đó và lệch khỏi cảnh; lớp như vậy bị gỡ và tấm kính tự quay về backdrop-filter.
   Tấm nào mất lớp .gl (nội dung bị ghi đè) cũng vậy. Thêm ?glass=live vào địa chỉ để tắt (khi so sánh hoặc gỡ lỗi). */
(function () {
  var doc = document, root = doc.documentElement;
  if (root.classList.contains('lite') || /[?&]glass=live\b/.test(location.search)) return;
  if (!window.CSS || !CSS.supports || !CSS.supports('clip-path', 'inset(0 round 1px)') || !CSS.supports('selector(:has(> i))')) return;
  // Tấm kính đứng yên trong dòng nội dung. Bong bóng trò chuyện, hộp thoại và thanh menu không nằm ở đây: chúng nhỏ,
  // hoặc nổi trên nội dung khác, hoặc có hiệu ứng trượt, nên vẫn làm mờ trực tiếp.
  var PANES = '.glass, .glass-strong, .hero-copy, body > .hero, #form-section > .hero, .page-header, .page-hero, .article-hero, ' +
    'body > .article-cover, #featuredWrap > .featured, body > section, .cats-section, .sup-section, #pageContent > .wrap, .articles, ' +
    'body > .article-body, body > .article-body ~ .related, .page-hero + .content, .chat-inner > .welcome, #success-section, footer, ' +
    '.planner-box, .cta-box, .newsletter-box, .form-wrap .step, .featured-card, .featured-inner, .hint';
  var layers = [], skipped = window.WeakSet ? new WeakSet() : null;
  function dress() {
    var found = [];
    doc.querySelectorAll(PANES).forEach(function (el) {
      var first = el.firstElementChild;
      if ((first && first.className === 'gl') || (skipped && skipped.has(el))) return;
      var cs = getComputedStyle(el), bf = cs.backdropFilter || cs.webkitBackdropFilter;
      if (!bf || bf === 'none' || cs.position === 'fixed') {                  // không làm mờ (nằm trong tấm khác) hoặc là lớp nổi
        if (skipped) skipped.add(el);
        return;
      }
      found.push([el, cs.position === 'static', cs.borderRadius || cs.borderTopLeftRadius || '0px']);
    });
    found.forEach(function (f) {
      var g = doc.createElement('i');
      g.className = 'gl'; g.setAttribute('aria-hidden', 'true');
      g.appendChild(doc.createElement('b'));
      g.style.setProperty('--gl-r', f[2]);
      if (f[1]) f[0].classList.add('gl-rel');
      f[0].insertBefore(g, f[0].firstChild);
      layers.push(g);
    });
    if (found.length && root.classList.contains('pre')) verify();
  }
  function verify() {                             // ảnh ghim có thật sự bám theo khung nhìn không?
    var vw = root.clientWidth, bad = [];
    layers.forEach(function (g) {
      if (!g.isConnected) return;
      var r = g.firstChild.getBoundingClientRect();
      if (!r.width) return;                       // tấm đang ẩn: chưa đo được
      if (Math.abs(r.left) > 1.5 || Math.abs(r.top) > 1.5 || Math.abs(r.width - vw) > 3) bad.push(g);
    });
    bad.forEach(function (g) {
      var el = g.parentNode;
      el.removeChild(g); el.classList.remove('gl-rel');
      if (skipped) skipped.add(el);
    });
  }
  function refit() {                              // bo góc của tấm đổi theo cỡ màn hình
    verify();
    layers = layers.filter(function (g) { return g.isConnected; });
    var r = layers.map(function (g) { var cs = getComputedStyle(g.parentNode); return cs.borderRadius || cs.borderTopLeftRadius || '0px'; });
    layers.forEach(function (g, i) { g.style.setProperty('--gl-r', r[i]); });
  }
  function urlOf(v) { var m = /url\(["']?([^"')]+)["']?\)/.exec(v || ''); return m && m[1]; }
  function start() {
    var src = urlOf(getComputedStyle(doc.body).getPropertyValue('--bg-glass'));
    if (!src) return;
    dress();
    var img = new Image();
    img.onload = function () {
      root.classList.add('pre');
      verify();
      var other = src.indexOf('-day') > -1 ? src.replace('-day', '-night') : src.replace('-night', '-day');
      new Image().src = other;                      // ảnh của chế độ còn lại, để đổi sáng/tối không bị chớp
    };
    img.src = src;
    var t = 0;
    addEventListener('resize', function () { clearTimeout(t); t = setTimeout(refit, 180); }, { passive: true });
    if (window.MutationObserver) {
      var queued = false;
      new MutationObserver(function () {
        if (queued) return;
        queued = true;
        requestAnimationFrame(function () { queued = false; dress(); });
      }).observe(doc.body, { childList: true, subtree: true });
    }
  }
  if (doc.body) start(); else doc.addEventListener('DOMContentLoaded', start);
})();

/* 4. Sân khấu (theme.css mục 10). Hai nút nổi ở góc dưới phải:
   • "Bắn pháo hoa": nội dung trang tạm ẩn để lộ trọn cảnh nền, pháo bắn lên, hết pháo thì nội dung hiện lại.
   • "Ngắm cảnh": ẩn nội dung cho tới khi bấm "Quay lại" (hoặc Esc, hoặc cuộn trang). Lúc này chạm vào đâu trên
     bầu trời thì một quả pháo nổ ở đó. */
(function () {
  var doc = document, root = doc.documentElement;
  if (!doc.body || !window.requestAnimationFrame || !doc.body.classList) return;
  var FIRE = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" aria-hidden="true"><path d="M12 2.5v4M12 13v8.5M4.2 5.2l3 3M19.8 5.2l-3 3M2.5 12.5h4M17.5 12.5h4M6 18l2.4-2.6M18 18l-2.4-2.6"/><circle cx="12" cy="10" r="1.5" fill="currentColor" stroke="none"/></svg>';
  var EYE = '<svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2.5 12S6 5.5 12 5.5 21.5 12 21.5 12 18 18.5 12 18.5 2.5 12 2.5 12z"/><circle cx="12" cy="12" r="3"/></svg>';
  var BACK = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.1" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>';

  var box = doc.createElement('div');
  box.className = 'th-stage th-keep';
  box.setAttribute('role', 'group'); box.setAttribute('aria-label', 'Cảnh nền');
  box.innerHTML = '<span class="th-tip" aria-hidden="true">Chạm vào bầu trời để bắn thêm</span>' +
    '<button type="button" class="th-fire" aria-label="Bắn pháo hoa">' + FIRE + '<span>Bắn pháo hoa</span></button>' +
    '<button type="button" class="th-view" aria-pressed="false"></button>';
  var fireBtn = box.querySelector('.th-fire'), viewBtn = box.querySelector('.th-view');
  doc.body.appendChild(box);

  var on = false, sticky = false, y0 = 0, t1 = 0, t2 = 0, loading = false, waiting = [];
  function label() {
    viewBtn.innerHTML = sticky ? BACK + '<span>Quay lại</span>' : EYE;
    viewBtn.setAttribute('aria-label', sticky ? 'Quay lại trang' : 'Ngắm toàn cảnh');
    viewBtn.title = sticky ? '' : 'Ngắm toàn cảnh';
    viewBtn.setAttribute('aria-pressed', sticky ? 'true' : 'false');
    box.classList.toggle('is-view', sticky);
  }
  function enter() {
    if (on) return;
    on = true; y0 = window.scrollY || 0;
    clearTimeout(t1); clearTimeout(t2);
    root.classList.add('stage-anim');
    void box.offsetWidth;                                   // để trình duyệt nhận trạng thái đầu của hiệu ứng mờ dần
    root.classList.add('stage');
    t1 = setTimeout(function () { root.classList.add('stage-done'); }, 520);
  }
  function leave() {
    if (!on) return;
    on = false; sticky = false; label();
    clearTimeout(t1); clearTimeout(t2);
    root.classList.remove('stage-done');
    void box.offsetWidth;
    root.classList.remove('stage');
    t1 = setTimeout(function () { root.classList.remove('stage-anim'); }, 600);
  }
  function idle() {                                         // hết pháo: nếu chỉ tạm ẩn để xem pháo thì trả lại trang
    if (on && !sticky) t2 = setTimeout(function () { if (on && !sticky) leave(); }, 650);
  }
  function engine(fn) {
    if (window.THFire) { window.THFire.onidle = idle; return fn(window.THFire); }
    waiting.push(fn);
    if (loading) return;
    loading = true;
    var s = doc.createElement('script');
    s.src = '/fireworks.js'; s.async = true;
    s.onload = function () {
      var q = waiting; waiting = [];
      if (!window.THFire) { idle(); return; }
      window.THFire.onidle = idle;
      q.forEach(function (f) { f(window.THFire); });
    };
    s.onerror = function () { loading = false; waiting = []; idle(); };
    doc.head.appendChild(s);
  }

  fireBtn.addEventListener('click', function () {
    clearTimeout(t2);
    enter();
    box.classList.add('fired');
    engine(function (fx) { fx.volley(); });
  });
  viewBtn.addEventListener('click', function () {
    if (on && sticky) { leave(); return; }
    sticky = true; label();
    clearTimeout(t2);
    enter();
  });
  box.addEventListener('click', function (e) { e.thStage = true; });   // (nút tự đổi biểu tượng nên không dò ngược từ e.target được)
  doc.addEventListener('click', function (e) {              // đang ngắm cảnh: chạm vào trời là bắn một quả ở đó
    if (!on || e.thStage) return;
    clearTimeout(t2);
    engine(function (fx) { fx.shellAt(e.clientX, e.clientY); });
  });
  doc.addEventListener('keydown', function (e) { if (on && (e.key === 'Escape' || e.key === 'Esc')) leave(); });
  addEventListener('scroll', function () { if (on && Math.abs((window.scrollY || 0) - y0) > 48) leave(); }, { passive: true });
  label();
})();
