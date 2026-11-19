/* Timeless Harmony — kính lỏng: vệt sáng chạy theo con trỏ trên các tấm kính.
   Đặt biến --lx/--ly (px, tính từ góc trên-trái của tấm) để theme.css vẽ quầng sáng.
   Chỉ chạy trên thiết bị có chuột; không ảnh hưởng nội dung nếu tệp này không tải được. */
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
