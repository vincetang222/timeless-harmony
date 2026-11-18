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
