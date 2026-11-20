/* Tiện ích giao diện nhỏ: tạo phần tử, nút, thanh chỉ số. Trạng thái dùng chung nằm trong `store`. */
export const store = { s: null, save: () => {}, render: () => {}, moHop: () => {} };

export function h(tag, props, ...kids) {
  const e = document.createElement(tag);
  for (const [k, v] of Object.entries(props || {})) {
    if (v == null || v === false) continue;
    if (k === 'cls') e.className = v;
    else if (k.startsWith('on')) e.addEventListener(k.slice(2), v);
    else if (k === 'html') e.innerHTML = v;
    else e.setAttribute(k, v === true ? '' : v);
  }
  for (const c of kids.flat(Infinity)) {
    if (c == null || c === false) continue;
    e.append(c.nodeType ? c : document.createTextNode(String(c)));
  }
  return e;
}
/** Nút. `id` thành data-act để kiểm thử không phụ thuộc chữ. */
export function nut(nhan, fn, { id, cls = '', tat = false, phu } = {}) {
  const b = h('button', { type: 'button', cls: 'nut ' + cls, 'data-act': id, disabled: tat ? '' : null, onclick: () => { fn(); } }, nhan);
  if (phu) return h('div', { cls: 'nut-phu' }, b, h('small', {}, phu));
  return b;
}
/** Chạy một thao tác làm đổi trạng thái rồi lưu và vẽ lại. */
export function lam(fn) { return () => { fn(store.s); store.save(); store.render(); }; }
export function thanh(nhan, v, { cls = '', dao = false } = {}) {
  const pct = Math.max(0, Math.min(100, v));
  return h('div', { cls: 'thanh ' + cls },
    h('span', { cls: 'thanh-nhan' }, nhan),
    h('span', { cls: 'thanh-nen', role: 'img', 'aria-label': `${nhan}: ${Math.round(v)} trên 100` }, h('i', { style: `width:${pct}%` })),
    h('b', {}, Math.round(v)));
}
export const the = (...k) => h('div', { cls: 'the' }, ...k);
export const khung = (tieu, ...k) => h('section', { cls: 'khung' }, tieu ? h('h2', {}, tieu) : null, ...k);
export const ghi = (t) => h('p', { cls: 'ghi' }, t);
