/* Chương 5 (gom tiền), 6 (ngày cưới), tổng kết và kết thúc. */
import { h, nut, lam, thanh, the, khung, ghi, store } from './ui.js';
import * as G from './logic.js';
import * as L from './lich.js';

const { D } = G;
const f = G.fmtTien;
const doi = (s, id, extra = {}) => { s.scene = { id, ...extra }; };

/* ---------- Sự kiện ngẫu nhiên có hạt giống ---------- */
function suKien(s) {
  if (s.sit || s.ch !== 5) return;
  const cl = G.conLai(s);
  if (G.thoaDK(s, ['cang_cao']) && !s.seen.cang_thang) return G.mo(s, 'cang_thang');
  if (cl <= 75 && !s.seen.ncc_bo_ngang && G.thoaDK(s, ['ncc_bo_ngang'])) return G.mo(s, 'ncc_bo_ngang');
  if (G.rng(s) < 0.4) {
    const ds = ['cai_nhau', 'xe_hong', 'vay_nong'].filter((id) => !s.seen[id]);
    if (ds.length) G.mo(s, ds[Math.floor(G.rng(s) * ds.length)]);
  }
}
function vaoNgayCuoi(s) {
  if (!s.daDangKy) { s.daDangKy = true; G.ap(s, { tien: -0.2 }); s.nhatKy.unshift('Bạn đăng ký kết hôn vội ở phút chót.'); }
  s.ch = 6; s.nghiIdx = 0; s.dungGio = 0;
  const ncc = (id) => G.nccBy(id), q = Object.values(s.hd).map((x) => ncc(x.ncc).diem.chat_luong);
  const tb = q.reduce((t, x) => t + x, 0) / q.length;
  s.khachDiem = G.kep(Math.round(40 + tb * 4 + Math.max(0, Object.keys(s.hd).length - 2) * 3));
  const khac = ['am_thanh', 'quen_nhan', 'phat_bieu_dai'];
  const thu3 = G.thoaDK(s, ['ngoai_troi']) ? 'mua' : 'khach_lech';
  s.suCo = [{ sau: 1, id: 'ket_xe' }, { sau: 2, id: thu3 }, { sau: 3, id: khac[Math.floor(G.rng(s) * khac.length)] }];
  doi(s, 'ngay_cuoi');
}
function ketThucTuan(s) { G.ap(s, { cang_minh: s.ngayCuoi && G.conLai(s) < 30 ? 2 : 1, cang_ay: 1 }); if (Math.max(s.cangMinh, s.cangAy) >= 90) G.ap(s, { tinh_cam: -3 }); suKien(s); kiemNgayCuoi(s); }
function kiemNgayCuoi(s) { if (!s.sit && s.ch === 5 && G.conLai(s) <= 0) vaoNgayCuoi(s); }

const TUAN = [
  { id: 'kiem-them', nhan: 'Tuần này kiếm thêm', mo: 'Chạy xe và bán hàng các buổi tối. Thu thêm khoảng 1,6 triệu, nhưng mệt và ít thời gian bên nhau.', e: { tien: 1.6, cang_minh: 6, tinh_cam: -3 } },
  { id: 'ben-nhau', nhan: 'Tuần này dành cho nhau', mo: 'Đi ăn, đi dạo, không bàn chuyện cưới. Tốn khoảng 0,9 triệu.', e: { tien: -0.9, tinh_cam: 7, cang: -6 } },
  { id: 'nghi', nhan: 'Tuần này nghỉ ngơi', mo: 'Ngủ đủ, tập nhẹ, thư giãn. Tốn khoảng 0,3 triệu.', e: { tien: -0.3, cang_minh: -9, cang_ay: -4 } },
  { id: 'lo-viec', nhan: 'Tuần này lo việc cưới', mo: 'Thăm hỏi hai họ, chốt chi tiết với người ấy. Tốn khoảng 0,6 triệu.', e: { tien: -0.6, ho: 2, cang_minh: 3, tinh_cam: 1 } },
];
function chayTuan(s, t) { G.ap(s, t.e); G.tuaNgay(s, 7); s.tuan += 1; ketThucTuan(s); }

function gomTien() {
  const s = store.s;
  G.chuanBuoi(s);
  const cl = G.conLai(s);
  const mocDS = h('ul', {}, s.moc.map((m) => h('li', {}, `${m.nhan}: ${f(m.so)}${m.daTra ? ' (đã đóng)' : m.sauTiec ? ' (sau tiệc)' : `, hạn ${G.ngayVN(m.han)}`}`)));
  const don = (id, nhan, mo, e, tat, extra) => the(h('h3', {}, nhan), h('p', {}, mo), nut('Làm', lam((st) => { e(st); G.dungBuoi(st, 1); if (extra !== 'giu') { suKien(st); kiemNgayCuoi(st); } }), { id, tat }));
  return h('div', {},
    khung('Chương 5. Gom tiền và chuẩn bị',
      h('p', {}, `${G.ngayVN(s.ngay)}, buổi ${G.tenBuoi[s.buoi].toLowerCase()}. Còn ${cl} ngày tới ngày cưới (${G.ngayVN(s.ngayCuoi)}).`),
      ghi('Ngày thường bạn đi làm sáng và chiều (lương nhận tự động mỗi tháng), nên chỉ buổi tối và cuối tuần là thời gian của bạn.'),
      mocDS,
      h('p', {}, `Đăng ký kết hôn: ${s.daDangKy ? 'đã xong' : 'chưa'}.`),
      s.nhatKy.slice(0, 3).map((t) => h('p', { cls: 'ghi' }, t))),
    khung('Cả tuần một lần', h('p', {}, 'Cách nhanh nhất để đi qua thời gian chờ. Bạn chọn trọng tâm của tuần.'),
      h('div', { cls: 'luoi' }, TUAN.map((t) => the(h('h3', {}, t.nhan), h('p', {}, t.mo), nut('Chọn', lam((st) => chayTuan(st, t)), { id: `tuan-${t.id}` }))))),
    khung('Từng buổi',
      h('div', { cls: 'luoi' },
        the(h('h3', {}, 'Chạy xe công nghệ'), h('p', {}, 'Một buổi tối, ba cuốc.'), nut('Bắt đầu', lam((st) => doi(st, 'tro_nho', { game: 'xe_cong_nghe', i: 0, tong: 0, log: [], ve: 'gom_tien' })), { id: 'tn-xe' })),
        the(h('h3', {}, 'Bán hàng ở chợ đêm'), h('p', {}, 'Nhập hàng, định giá.'), nut('Bắt đầu', lam((st) => doi(st, 'tro_nho', { game: 'cho_dem', i: 0, tong: 0, log: [], ve: 'gom_tien' })), { id: 'tn-cho' })),
        don('hen-ho', 'Hẹn hò, không bàn chuyện cưới', 'Tốn 0,6 triệu.', (st) => G.ap(st, { tien: -0.6, tinh_cam: 5, cang: -5 }), s.tien < 0.6),
        don('tap-luyen', 'Tập luyện: khoẻ và tự tin', 'Tốn 0,5 triệu. Tập đều thì tốt, không cần ép cân.', (st) => G.ap(st, { tien: -0.5, cang_minh: -4, tinh_cam: 1 }), s.tien < 0.5),
        don('nghi-ngoi', 'Nghỉ ngơi', 'Ở nhà, ngủ sớm.', (st) => G.ap(st, { cang_minh: -8, cang_ay: -2 }), false),
        don('tham-ho', 'Thăm hỏi hai họ', 'Tốn 0,5 triệu.', (st) => G.ap(st, { tien: -0.5, ho: 2, cang_minh: 2 }), s.tien < 0.5),
        the(h('h3', {}, 'Đăng ký kết hôn ở uỷ ban'), h('p', {}, 'Xin nghỉ nửa ngày, tốn 0,3 triệu.'), nut('Đi đăng ký', lam((st) => { G.ap(st, { tien: -0.3 }); st.daDangKy = true; G.dungBuoi(st, 1); st.nhatKy.unshift('Đã đăng ký kết hôn.'); kiemNgayCuoi(st); }), { id: 'dang-ky', tat: s.daDangKy })))),
    G.baoNhieu(s, 'dot2') && G.baoNhieu(s, 'dot2').daTra && s.daDangKy
      ? khung('Mọi thứ đã xong', h('p', {}, 'Đã đóng đợt hai và đăng ký kết hôn. Bạn có thể chờ tới ngày cưới.'),
        nut('Chờ tới ngày cưới', lam((st) => { while (!st.sit && G.conLai(st) > 0) { G.dungBuoi(st, 3); } kiemNgayCuoi(st); }), { id: 'toi-ngay-cuoi', cls: 'chinh' })) : null);
}

function troNho() {
  const s = store.s, sc = s.scene, g = D.ch.tro_nho.find((x) => x.id === sc.game);
  if (sc.i >= g.vong.length) {
    return khung(g.ten, h('div', { cls: 'nhat-ky' }, sc.log.map((t) => h('p', {}, t))),
      h('p', {}, `Tổng thu sau chi phí: ${f(G.lamTron(sc.tong, 2))}.`),
      nut('Xong buổi tối', lam((st) => { G.ap(st, { tien: sc.tong, cang_minh: g.cang }); G.dungBuoi(st, 1); doi(st, sc.ve || 'gom_tien'); if (st.ch === 5) { suKien(st); kiemNgayCuoi(st); } }), { id: 'tn-xong', cls: 'chinh' }));
  }
  const v = g.vong[sc.i];
  return khung(g.ten, h('p', {}, g.mo_ta), sc.log.map((t) => h('p', { cls: 'ghi' }, t)), h('h3', {}, v.cau_hoi),
    h('div', { cls: 'hang' }, v.chon.map((c, j) => nut(c.nhan, lam((st) => {
      const th = G.lamTron(G.rngKhoang(st, c.thu), 2), phi = c.phi || 0;
      st.scene.tong = G.lamTron(st.scene.tong + th - phi, 2);
      st.scene.log = [...st.scene.log, `${c.ket} (thu ${f(th)}${phi ? `, chi ${f(phi)}` : ''})`];
      st.scene.i += 1;
    }), { id: `tn-chon-${j}` }))));
}

/* ---------- Chương 6: ngày cưới ---------- */
function gioHD(s, idx) {
  const t = L.thongTinNgay(s.ngayCuoi), gs = L.gioHoangDao(t.canChiNgay.chi);
  const ban = gs.filter((g) => g.tu >= 5 && g.tu <= 15);
  const ds = ban.length >= 3 ? ban : gs;
  return ds[Math.min(idx, ds.length - 1)];
}
function ngayCuoi() {
  const s = store.s, ds = D.th.nghi_le, i = s.nghiIdx, st = ds[i];
  let gioIdx = ds.slice(0, i + 1).filter((x) => x.gio_moc).length - 1;
  const gio = st.gio_moc && s.xemNgay ? gioHD(s, gioIdx) : null;
  return khung(`Chương 6. Ngày cưới: ${st.ten}`,
    h('p', { cls: 'ghi' }, `Bước ${i + 1} trên ${ds.length}, ${G.ngayVN(s.ngayCuoi)}.`),
    h('p', {}, st.mo_ta),
    gio ? h('p', { cls: 'ghi' }, `Giờ hoàng đạo gợi ý cho bước này: ${gio.nhan} (${gio.than}), theo lịch âm.`) : null,
    h('div', { cls: 'hang' }, st.lua_chon.map((lc, j) => nut(lc.nhan, lam((so) => {
      G.ap(so, lc);
      so.nhatKy.unshift(lc.ket);
      if (lc.co === 'dung_gio') so.dungGio += 1;
      so.nghiIdx += 1;
      const sc = so.suCo.find((x) => x.sau === so.nghiIdx);
      if (sc) {
        const t = G.thTheoId(sc.id);
        if (t.co_san && ((t.co_san.khi === 'nha_bat' && so.hd.tiec && (G.nccBy(so.hd.tiec.ncc).nha_bat || []).includes(so.hd.tiec.goi)) || (t.co_san.khi === 'nhac' && so.hd.nhac))) {
          G.ap(so, { khach: t.co_san.khach }); so.sit = { kind: 'kq', id: sc.id, ket: t.co_san.ket };
        } else G.mo(so, sc.id);
      }
      if (so.nghiIdx >= ds.length) tongKet(so);
    }), { id: `nl-${j}` }))),
    s.nhatKy.slice(0, 1).map((t) => h('p', {}, t)));
}

function tongKet(s) {
  const cfg = D.ch.tien_mung_khach, [a, b] = cfg[s.khu];
  const tb = (a + b) / 2, bien = 0.8 + 0.4 * G.rng(s);
  const tm = G.lamTron(s.khach * tb * bien, 1);
  s.tienMung = tm;
  let conLai = 0;
  const m = s.moc.find((x) => x.sauTiec); if (m) conLai += m.so;
  let phatSinh = 0;
  for (const hd of Object.values(s.hd)) if (hd.phatSinh && !s.daHoi[hd.ncc]) phatSinh += hd.gia * hd.phatSinh;
  phatSinh = G.lamTron(phatSinh, 1); conLai = G.lamTron(conLai + phatSinh, 1);
  s.phatSinh = phatSinh;
  s.conLai = conLai;
  const dd = G.chamDiem(s, tm, conLai);
  s.diem = dd;
  s.ketThuc = G.chonKetThuc(s, dd, dd.rong);
  s.ch = 7; doi(s, 'tong_ket');
}
function tongKetUI() {
  const s = store.s, d = s.diem, kt = D.ch.ket_thuc[s.ketThuc];
  return h('div', {},
    khung('Tổng kết', s.thuNghiem ? h('p', { cls: 'ghi canh-bao' }, 'Lượt chơi này có nạp tiền ở chế độ thử, không tính vào số liệu.') : null,
      h('div', { cls: 'thanh-nhom' },
        thanh('Cặp đôi', d.cap), thanh('Nhà trai', d.nhaTrai), thanh('Nhà gái', d.nhaGai), thanh('Khách mời', d.khach), thanh('Tài chính', d.taiChinh))),
    khung('Chuyện tiền',
      h('ul', {}, h('li', {}, `Tiền mừng nhận được: ${f(s.tienMung)} (khoảng ${s.khach} khách, số tạm của game).`),
        h('li', {}, `Phần còn lại phải đóng sau tiệc: ${f(s.conLai)}${s.phatSinh ? `, trong đó ${f(s.phatSinh)} là phụ thu mà bạn không hỏi trước` : ''}.`),
        h('li', {}, `Nợ còn lại: ${f(s.no)}.`),
        h('li', {}, `Sau tất cả, bạn còn ${f(d.rong)} (tiền mặt cộng tiền mừng, trừ phần còn lại và nợ).`))),
    khung(`Kết thúc: ${kt.ten}`, h('p', {}, kt.mo),
      nut('Xem kết thúc', lam((st) => doi(st, 'ending')), { id: 'xem-ket-thuc', cls: 'chinh' })));
}

function toiGian() {
  const s = store.s;
  return khung('Tối giản', h('p', {}, 'Hai bạn đi đăng ký kết hôn, rồi cùng hai bên bố mẹ ăn một bữa cơm ấm cúng. Tốn khoảng 3 triệu.'),
    nut('Hoàn tất', lam((st) => { G.ap(st, { tien: -3, tinh_cam: 8, ho: -2 }); st.diem = G.chamDiem(st, 0, 0); st.tienMung = 0; st.conLai = 0; st.phatSinh = 0; st.khachDiem = 60; st.ch = 7; G.ketThuc(st, 'toi_gian'); }), { id: 'toi-gian-xong', cls: 'chinh' }));
}

function ending() {
  const s = store.s, kt = D.ch.ket_thuc[s.ketThuc];
  const dd = s.diem;
  const hoan = s.ketThuc === 'hoan_cuoi', chia = s.ketThuc === 'chia_tay';
  return khung(`Kết thúc: ${kt.ten}`, h('p', {}, kt.mo),
    s.thuNghiem ? ghi('Lượt chơi này có nạp tiền ở chế độ thử, không tính vào số liệu.') : null,
    dd && !hoan && !chia ? h('div', { cls: 'thanh-nhom' }, thanh('Cặp đôi', dd.cap), thanh('Nhà trai', dd.nhaTrai), thanh('Nhà gái', dd.nhaGai), thanh('Khách mời', dd.khach), thanh('Tài chính', dd.taiChinh)) : null,
    hoan ? nut('Chơi tiếp, chọn lại ngày', lam((st) => G.choiTiepSauHoan(st)), { id: 'choi-tiep', cls: 'chinh' }) : null,
    chia ? nut('Bắt đầu lại, giữ số tiền đang có', lam((st) => { const giu = Math.max(0, G.lamTron(st.tien - st.no, 1)); const moi = G.trangThaiMoi(giu); const luu = st.thuNghiem; Object.keys(st).forEach((k) => delete st[k]); Object.assign(st, moi, { thuNghiem: luu, scene: { id: 'tao_nv' } }); }), { id: 'bat-dau-lai-giu-tien', cls: 'chinh' }) : null,
    nut('Chơi lại từ đầu', lam((st) => { const luu = st.thuNghiem; const moi = G.trangThaiMoi(); Object.keys(st).forEach((k) => delete st[k]); Object.assign(st, moi, { scene: { id: 'tao_nv' }, thuNghiem: false }); }), { id: 'choi-lai' }),
    ghi('Bản chơi thử mốc 1: tiền, giá, tâm lý đều là số tạm của game và sẽ chỉnh khi có dữ liệu thật.'));
}

export default { gom_tien: gomTien, tro_nho: troNho, ngay_cuoi: ngayCuoi, tong_ket: tongKetUI, toi_gian: toiGian, ending };
