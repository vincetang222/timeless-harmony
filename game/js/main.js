/* Khởi động, vẽ lại theo trạng thái, thanh chỉ số, hộp thoại Nạp tiền và Cài đặt. */
import { h, nut, thanh, store } from './ui.js';
import * as G from './logic.js';
import s1 from './scenes1.js';
import s2 from './scenes2.js';
import s3 from './scenes3.js';

const CANH = { ...s1, ...s2, ...s3 };
const app = document.getElementById('app');
const hop = document.getElementById('hop');

/* Mã quản trị: CHỈ LÀ CÔNG CỤ THỬ GAME, KHÔNG PHẢI BẢO MẬT. Nó nằm ngay trong mã nguồn nên ai mở mã cũng thấy,
 * và chỉ có tác dụng trên máy này (lưu ở localStorage). Khi có tài khoản, quyền này phải gắn với tài khoản
 * và kiểm ở máy chủ (xem mục 7 của docs/game/spec.md). */
const MA_QUAN_TRI = 'THU-GAME-2027';

function doc(k) { try { return JSON.parse(localStorage.getItem(k)); } catch { return null; } }
function ghi(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch { /* bộ nhớ đầy hoặc bị chặn: bỏ qua */ } }
const laQuanTri = () => !!(doc(G.KHOA_CAI_DAT) || {}).quanTri;

function luu() { if (store.s) ghi(G.KHOA, store.s); }
store.save = luu; store.render = ve;

function thanhChiSo(s) {
  const dem = G.conLai(s);
  return h('header', { cls: 'chi-so' },
    h('div', { cls: 'hang-chi-so' },
      h('div', { cls: 'tien' }, h('span', {}, 'Ví'), h('b', { 'data-stat': 'tien' }, G.fmtTien(s.tien)), s.no > 0 ? h('small', { cls: 'no', 'data-stat': 'no' }, `Nợ ${G.fmtTien(s.no)}`) : null),
      h('div', { cls: 'ngay' }, h('span', {}, 'Thời gian'), h('b', { 'data-stat': 'ngay' }, G.ngayVN(s.ngay)), h('small', {}, `Buổi ${G.tenBuoi[s.buoi].toLowerCase()}${dem != null ? `, còn ${dem} ngày tới ngày cưới` : ''}`)),
      h('div', { cls: 'nut-goc' }, nut('Nạp tiền', () => moNapTien(), { id: 'nap-tien', cls: 'nho' }), nut('Cài đặt', () => moCaiDat(), { id: 'cai-dat', cls: 'nho' }))),
    s.thuNghiem ? h('p', { cls: 'che-do-thu' }, 'Chế độ thử: lượt chơi này có nạp tiền kiểu quản trị, không tính vào số liệu.') : null,
    s.ban ? h('div', { cls: 'thanh-nhom' },
      thanh(`Tình cảm với ${s.ban.ten}`, s.tinhCam), thanh('Lòng nhà trai', s.hoTrai), thanh('Lòng nhà gái', s.hoGai),
      thanh('Căng thẳng của bạn', s.cangMinh, { cls: 'cang' }), thanh(`Căng thẳng của ${s.ban.ten}`, s.cangAy, { cls: 'cang' })) : null);
}

/* ---------- Tình huống đang mở ---------- */
function veSit(s) {
  const sit = s.sit, t = G.thTheoId(sit.id);
  if (sit.kind === 'kq') {
    return h('section', { cls: 'khung tinh-huong', role: 'dialog', 'aria-label': 'Kết quả' }, h('h2', {}, t.tieu_de), h('p', {}, sit.ket), sit.them ? h('p', { cls: 'ghi' }, sit.them) : null,
      nut('Tiếp tục', () => { G.dongSit(s); luu(); ve(); }, { id: 'sit-tiep', cls: 'chinh' }));
  }
  return h('section', { cls: 'khung tinh-huong', role: 'dialog', 'aria-label': t.tieu_de }, h('h2', {}, t.tieu_de), h('p', {}, t.noi),
    h('div', { cls: 'hang doc' }, t.lua_chon.map((lc, i) => nut(lc.nhan, () => { G.chonTH(s, i); luu(); ve(); }, { id: `sit-${i}` }))));
}

function ve() {
  const s = store.s;
  app.replaceChildren();
  if (!s.ban && !['bat_dau', 'tao_nv'].includes(s.scene.id) && s.ch === 0) s.scene = { id: 'bat_dau' };
  const bd = ['bat_dau', 'tao_nv'].includes(s.scene.id);
  if (!bd) app.append(thanhChiSo(s));
  const main = h('main', { id: 'noidung' });
  const fn = s.sit ? null : CANH[s.scene.id];
  if (s.sit) main.append(veSit(s)); else if (fn) main.append(fn()); else main.append(h('p', {}, 'Màn hình không tồn tại: ' + s.scene.id));
  app.append(main);
  window.scrollTo(0, 0);
}

/* ---------- Hộp thoại ---------- */
function dongHop() { hop.replaceChildren(); hop.hidden = true; }
function moHopNoiDung(tieu, ...nd) {
  hop.replaceChildren(h('div', { cls: 'hop-nen', onclick: dongHop }),
    h('div', { cls: 'hop-nd', role: 'dialog', 'aria-modal': 'true', 'aria-label': tieu }, h('h2', {}, tieu), ...nd, nut('Đóng', dongHop, { id: 'hop-dong' })));
  hop.hidden = false;
}
function moNapTien() {
  const s = store.s, cfg = D().ch, nd = [];
  nd.push(h('p', {}, 'Bản chơi thử không thu tiền thật. Đây là các cách kiếm tiền ngay trong game:'));
  nd.push(h('ul', { cls: 'cach' },
    h('li', {}, h('b', {}, 'Lương theo nghề: '), `${G.fmtTien(G.luong(s))} mỗi tháng, nhận tự động (ngày thường bạn đi làm sáng và chiều).`),
    h('li', {}, h('b', {}, 'Việc làm thêm buổi tối: '), 'chạy xe công nghệ hoặc bán hàng chợ đêm. ', nut('Chạy xe một buổi', () => { dongHop(); s.scene = { id: 'tro_nho', game: 'xe_cong_nghe', i: 0, tong: 0, log: [], ve: s.scene.id }; luu(); ve(); }, { id: 'nap-xe', cls: 'nho' }), nut('Bán chợ đêm một buổi', () => { dongHop(); s.scene = { id: 'tro_nho', game: 'cho_dem', i: 0, tong: 0, log: [], ve: s.scene.id }; luu(); ve(); }, { id: 'nap-cho', cls: 'nho' })),
    h('li', {}, h('b', {}, 'Bố mẹ hỗ trợ: '), `${G.fmtTien(cfg.ho_tro_bo_me.so_tien)}, một lần. Đổi lại bố mẹ có tiếng nói hơn trong các quyết định. `, nut('Hỏi xin bố mẹ', () => { if (!s.daXinBoMe) { s.daXinBoMe = true; G.ap(s, { tien: cfg.ho_tro_bo_me.so_tien, gia_dinh: 0 }); s.hoTrai = G.kep(s.hoTrai + 2); s.hoGai = G.kep(s.hoGai + 2); s.nhatKy.unshift('Bố mẹ hỗ trợ bạn một khoản.'); } dongHop(); luu(); ve(); }, { id: 'nap-bo-me', cls: 'nho', tat: !!s.daXinBoMe })),
    h('li', {}, h('b', {}, 'Vay ngân hàng: '), `${G.fmtTien(cfg.vay.moi_lan)} mỗi lần, lãi ${cfg.vay.lai_nam * 100}% một năm (số của game), nợ kéo qua cả sau cưới. `, nut('Vay thêm', () => { G.vay(s, cfg.vay.moi_lan); s.nhatKy.unshift(`Vay ${G.fmtTien(cfg.vay.moi_lan)}.`); dongHop(); luu(); ve(); }, { id: 'nap-vay', cls: 'nho' })),
    h('li', {}, h('b', {}, 'Tiền mừng: '), 'chỉ nhận sau tiệc, không dùng được để đóng cọc.')));
  nd.push(h('p', { cls: 'ghi' }, 'Game không có cờ bạc, cá độ hay vay nóng. Nếu có ai rủ, từ chối là lựa chọn đúng.'));
  if (laQuanTri()) {
    const inp = h('input', { type: 'number', id: 'nap-so', min: 1, max: 5000, value: 100, 'aria-label': 'Số tiền nạp (triệu)' });
    nd.push(h('div', { cls: 'quan-tri' }, h('h3', {}, 'Nạp tiền (quản trị, chế độ thử)'), h('label', {}, 'Số tiền (triệu)', inp),
      nut('Nạp', () => { const v = Math.max(0, Number(inp.value) || 0); s.tien = G.lamTron(s.tien + v); s.thuNghiem = true; dongHop(); luu(); ve(); }, { id: 'nap-quan-tri', cls: 'nho' })));
  }
  moHopNoiDung('Nạp tiền', ...nd);
}
function moCaiDat() {
  const s = store.s;
  const xem = h('input', { type: 'checkbox', id: 'cd-xem' }); xem.checked = s.xemNgay;
  xem.addEventListener('change', () => { s.xemNgay = xem.checked; luu(); });
  const ma = h('input', { type: 'password', id: 'cd-ma', autocomplete: 'off', 'aria-label': 'Mã quản trị' });
  const tt = h('p', { cls: 'ghi', id: 'cd-tt' }, laQuanTri() ? 'Quyền quản trị đang bật trên máy này.' : '');
  moHopNoiDung('Cài đặt',
    h('label', { cls: 'ngang' }, xem, 'Xem tuổi, xem ngày theo lịch âm (tắt thì hai họ cũng không nhắc tới; ngày đã chọn giữ nguyên)'),
    h('label', {}, 'Mã quản trị (công cụ thử game, chỉ có tác dụng trên máy này)', ma),
    nut('Mở quyền quản trị', () => { if (ma.value === MA_QUAN_TRI) { ghi(G.KHOA_CAI_DAT, { quanTri: true }); tt.textContent = 'Đã bật quyền quản trị trên máy này.'; } else tt.textContent = 'Mã chưa đúng.'; }, { id: 'cd-mo-qt', cls: 'nho' }),
    tt,
    nut('Chơi lại từ đầu (xoá tiến độ)', () => { const moi = G.trangThaiMoi(); store.s = moi; moi.scene = { id: 'bat_dau' }; luu(); dongHop(); ve(); }, { id: 'cd-reset', cls: 'nho' }));
}

/* ---------- Khởi động ---------- */
async function khoiDong() {
  await G.napDuLieu();
  let s = doc(G.KHOA);
  if (!s || s.v !== G.PHIEN_BAN) s = G.trangThaiMoi();
  store.s = s;
  ve();
  window.__game = { store, G };
}
khoiDong().catch((e) => { app.textContent = 'Không nạp được dữ liệu game: ' + e.message; });
