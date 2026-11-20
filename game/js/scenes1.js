/* Chương 0–2: bắt đầu, tạo nhân vật, làm quen, hẹn hò, yêu, cầu hôn. */
import { h, nut, lam, the, khung, ghi, store } from './ui.js';
import * as G from './logic.js';
import * as L from './lich.js';

const { D } = G;
const di = (s, id, extra = {}) => { s.scene = { id, ...extra }; };

function batDau() {
  return khung('Về chung một nhà',
    h('p', {}, 'Mình đồng hành cùng bạn đi qua một đám cưới: gặp người ấy, cầu hôn, bàn với hai họ, chọn nhà cung cấp, xoay tiền và bước vào ngày cưới.'),
    ghi('Đây là bản chơi thử, dùng hình khối tạm. Tiền, giá và nhà cung cấp là số của game (nhà cung cấp là nhân vật hư cấu), không phải dữ liệu thị trường. Game không dùng tiền thật.'),
    nut('Bắt đầu', lam((s) => di(s, 'tao_nv')), { id: 'bat-dau', cls: 'chinh' }));
}

function taoNhanVat() {
  const s = store.s;
  const f = { vai: 'chu_re', kieu: 'can_than', tk: 'vua', nghe: 'van_phong' };
  const raVai = h('div', { cls: 'hang' });
  const raKieu = h('div', { cls: 'luoi' });
  const raTK = h('div', { cls: 'hang' });
  const ten = h('input', { type: 'text', id: 'ten', value: 'Minh', maxlength: 24, 'aria-label': 'Tên của bạn' });
  const sinh = h('input', { type: 'date', id: 'sinh', value: D.ch.ngay_sinh_mac_dinh.chu_re, 'aria-label': 'Ngày sinh dương lịch của bạn' });
  const nghe = h('select', { id: 'nghe', 'aria-label': 'Nghề' }, D.ch.nghe.map((n) => h('option', { value: n.id }, `${n.ten} (lương ${n.luong} triệu/tháng)`)));
  const xem = h('input', { type: 'checkbox', id: 'xem', checked: '' });
  xem.checked = true;
  const chon = (box, val, key, cls) => { f[key] = val; for (const b of box.children) b.classList.toggle('chon', b.dataset.val === val); };
  const nutChon = (box, key, val, nhan, mota) => {
    const b = h('button', { type: 'button', cls: 'lua' + (f[key] === val ? ' chon' : ''), 'data-val': val, 'data-act': `${key}-${val}`, onclick: () => chon(box, val, key) }, h('b', {}, nhan), mota ? h('small', {}, mota) : null);
    box.append(b);
  };
  nutChon(raVai, 'vai', 'chu_re', 'Chú rể'); nutChon(raVai, 'vai', 'co_dau', 'Cô dâu');
  raVai.addEventListener('click', () => { sinh.value = D.ch.ngay_sinh_mac_dinh[f.vai]; ten.value = f.vai === 'chu_re' ? 'Minh' : 'Lan'; });
  D.tamLy.kieu.forEach((k) => nutChon(raKieu, 'kieu', k.id, k.ten, k.mo_ta));
  D.ch.tiet_kiem.forEach((t) => nutChon(raTK, 'tk', t.id, `${t.ten}: ${t.tien} triệu`));
  return khung('Tạo nhân vật',
    h('label', {}, 'Bạn là', raVai),
    h('label', {}, 'Tên', ten),
    h('label', {}, 'Ngày sinh dương lịch (lưu trên máy, không gửi đi đâu)', sinh),
    h('label', {}, 'Nghề', nghe),
    h('label', {}, 'Tiền tiết kiệm', raTK),
    h('label', {}, 'Tính cách của bạn', raKieu),
    h('label', { cls: 'ngang' }, xem, 'Có xem tuổi, xem ngày theo lịch âm (tắt thì hai họ trong game cũng không nhắc tới)'),
    nut('Vào game', lam((st) => {
      G.khoiTao(st, { vai: f.vai, ten: ten.value.trim() || 'Bạn', nghe: nghe.value, tietKiem: f.tk, kieuMinh: f.kieu, sinhMinh: sinh.value || D.ch.ngay_sinh_mac_dinh[f.vai], xemNgay: xem.checked });
      di(st, 'gap_go');
    }), { id: 'vao-game', cls: 'chinh' }));
}

function gapGo() {
  const s = store.s, ds = s.vai === 'chu_re' ? D.ch.nguoi_ay.cho_chu_re : D.ch.nguoi_ay.cho_co_dau;
  return khung('Chương 1. Gặp gỡ',
    h('p', {}, `Bạn bè giới thiệu ba người. Bạn chỉ có thời gian làm quen kỹ với một người. Cung hoàng đạo bên dưới chỉ là chuyện trò cho vui (theo cung hoàng đạo).`),
    h('div', { cls: 'luoi' }, ds.map((n, i) => {
      const cung = L.cungHoangDao(n.sinh);
      return the(h('h3', {}, n.ten), h('p', {}, n.mo_ta), s.xemNgay ? ghi(`Cung ${cung.ten} (${cung.nhom}), ${cung.nguon}.`) : null,
        nut(`Làm quen với ${n.ten}`, lam((st) => { st.ban = { ten: n.ten, sinh: n.sinh, kieu: n.kieu }; st.tinhCam = 25; st.heDa = 0; di(st, 'hen_ho'); }), { id: `chon-nguoi-${i}` }));
    })));
}

function henHo() {
  const s = store.s, ban = s.ban;
  const biet = s.biet || (s.biet = {});
  const nhat = s.nhatKy.slice(0, 2);
  return khung(`Chương 1. Hẹn hò với ${ban.ten}`,
    h('p', {}, 'Mỗi buổi hẹn tốn một buổi tối và một ít tiền. Bạn thử vài kiểu hẹn để hiểu người ấy.'),
    nhat.length ? h('div', { cls: 'nhat-ky' }, nhat.map((t) => h('p', {}, t))) : null,
    Object.keys(biet).length ? h('p', { cls: 'ghi' }, 'Bạn bắt đầu nhận ra: ' + Object.entries(biet).map(([k, v]) => `${G.tenTruc(k).ten}: ${v}`).join('; ') + '.') : null,
    h('div', { cls: 'luoi' }, D.ch.hen_ho.map((a) => the(h('h3', {}, a.ten), h('p', {}, a.mo_ta), ghi(`Tốn ${G.fmtTien(a.phi)}, một buổi tối.`),
      nut('Rủ đi', lam((st) => {
        const m = G.khop(st, a.truc, a.huong), mm = (m + 1) / 2;
        const d = Math.round(a.tinh_cam * 1.4 * (0.4 + 0.6 * mm));
        G.ap(st, { tien: -a.phi, tinh_cam: d, cang: a.cang });
        G.dungBuoi(st, 1);
        st.heDa += 1;
        const t = G.tenTruc(a.truc), cuc = a.huong < 0 ? t.trai : t.phai;
        st.biet = st.biet || {};
        if (m >= 0.5) { st.biet[a.truc] = `người ấy hợp với "${cuc}"`; st.nhatKy.unshift(`${a.ten}: người ấy thoải mái, vui ra mặt (tình cảm +${d}).`); }
        else if (m <= -0.5) { st.biet[a.truc] = `người ấy không nghiêng về "${cuc}"`; st.nhatKy.unshift(`${a.ten}: người ấy lịch sự nhưng có vẻ không hẳn là kiểu người ấy thích (tình cảm +${d}).`); }
        else st.nhatKy.unshift(`${a.ten}: một buổi dễ chịu (tình cảm +${d}).`);
      }), { id: `hen-${a.id}`, tat: s.tien < a.phi })))),
    s.tinhCam >= 55 ? nut(`Chính thức yêu ${ban.ten}`, lam((st) => { st.ch = 2; st.nhatKy.unshift(`Bạn và ${st.ban.ten} chính thức yêu nhau.`); di(st, 'yeu'); }), { id: 'chinh-thuc', cls: 'chinh' }) : null,
    s.heDa >= 4 && s.tinhCam < 55 ? nut('Làm quen người khác', lam((st) => { st.ban = null; st.heDa = 0; st.biet = {}; di(st, 'gap_go'); }), { id: 'nguoi-khac' }) : null);
}

function yeu() {
  const s = store.s, ban = s.ban;
  return khung('Chương 2. Yêu nhau',
    h('p', {}, `Bạn đang yêu ${ban.ten}. Trước khi cầu hôn, bạn nên ra mắt hai bên bố mẹ và vun thêm tình cảm.`),
    s.nhatKy.slice(0, 2).map((t) => h('p', { cls: 'ghi' }, t)),
    h('div', { cls: 'luoi' },
      the(h('h3', {}, 'Ra mắt hai bên bố mẹ'), h('p', {}, s.raMat ? 'Bạn đã ra mắt.' : 'Một bữa cơm hai gia đình gặp nhau.'),
        nut('Tổ chức bữa cơm', lam((st) => { st.raMat = true; G.dungBuoi(st, 1); G.mo(st, 'ra_mat'); }), { id: 'ra-mat', tat: s.raMat })),
      the(h('h3', {}, 'Dành buổi tối bên nhau'), h('p', {}, 'Không bàn chuyện cưới.'), ghi('Tốn 0,6 triệu, một buổi tối.'),
        nut('Đi ăn cùng nhau', lam((st) => { G.ap(st, { tien: -0.6, tinh_cam: 6, cang: -5 }); G.dungBuoi(st, 1); st.nhatKy.unshift('Một buổi tối yên ả bên nhau (tình cảm +6).'); }), { id: 'toi-ben-nhau', tat: s.tien < 0.6 })),
      the(h('h3', {}, 'Cầu hôn'), h('p', {}, s.raMat && s.tinhCam >= 50 ? 'Bạn thấy đã tới lúc.' : 'Cần ra mắt hai họ và tình cảm từ 50 trở lên.'),
        nut('Chọn bối cảnh cầu hôn', lam((st) => di(st, 'cau_hon')), { id: 'toi-cau-hon', tat: !(s.raMat && s.tinhCam >= 50) }))));
}

const NGOAI_TROI = ['san_thuong', 'bai_bien', 'truc_thang', 'du_thuyen'];
function cauHon() {
  const s = store.s;
  return khung('Chương 2. Cầu hôn',
    h('p', {}, 'Chọn nơi bạn muốn nói lời cầu hôn. Nơi lãng mạn đến đâu cũng cần hợp với người ấy.'),
    h('div', { cls: 'luoi' }, D.ch.cau_hon.map((o) => the(h('h3', {}, o.ten), h('p', {}, `Điểm mạnh: ${o.manh}.`), h('p', {}, `Rủi ro: ${o.rui_ro}.`), ghi(`Chi phí: ${G.fmtTien(o.phi)}.`),
      nut('Chọn nơi này', lam((st) => {
        const m = G.khop(st, o.truc, o.huong);
        let diem = st.tinhCam * 0.55 + ((st.hoTrai + st.hoGai) / 2) * 0.15 + o.diem + 20 * m + 10;
        const nguong = D.ch.nhan_cau_hon.nguong;
        let mua = false;
        if (NGOAI_TROI.includes(o.id) && G.rng(st) < 0.25) { diem -= 6; mua = true; }
        G.ap(st, { tien: -o.phi }); G.dungBuoi(st, 1);
        const ok = diem >= nguong;
        if (ok) { st.nhatKy.unshift(`${st.ban.ten} nhận lời cầu hôn.`); st.tinhCam = G.kep(st.tinhCam + 10); }
        else st.tinhCam = G.kep(st.tinhCam - 4);
        const gi = m >= 0.5 ? 'Nơi này đúng điều người ấy thích.' : m <= -0.5 ? 'Nơi này không hẳn hợp với người ấy.' : '';
        di(st, 'cau_hon_kq', { ok, mua, gi, ten: o.ten });
      }), { id: `cau-hon-${o.id}`, tat: s.tien < o.phi, phu: s.tien < o.phi ? 'Chưa đủ tiền. Bấm "Nạp tiền" để xem cách xoay tiền.' : null })))));
}
function cauHonKq() {
  const s = store.s, sc = s.scene;
  return khung(sc.ok ? 'Người ấy nhận lời' : 'Người ấy xin thêm thời gian',
    h('p', {}, sc.ok ? `Tại "${sc.ten}", ${s.ban.ten} gật đầu và cười. ${sc.gi}` : `Tại "${sc.ten}", ${s.ban.ten} nói cần thêm thời gian. ${sc.gi} Bạn có thể thử lại một cách khác.`),
    sc.mua ? ghi('Hôm đó trời có mưa nên không khí kém đi một chút.') : null,
    sc.ok
      ? nut('Sang chuyện hai họ', lam((st) => { st.ch = 3; st.ngay_sub = 'khu'; di(st, 'ke_hoach'); G.mo(st, 'sinh_le'); }), { id: 'sang-hai-ho', cls: 'chinh' })
      : nut('Thử lại', lam((st) => di(st, 'cau_hon')), { id: 'thu-lai', cls: 'chinh' }));
}

export default { bat_dau: batDau, tao_nv: taoNhanVat, gap_go: gapGo, hen_ho: henHo, yeu, cau_hon: cauHon, cau_hon_kq: cauHonKq };
