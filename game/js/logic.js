/* Luật chơi: trạng thái, thời gian, tiền, hiệu ứng. Không đụng DOM.
 * Mọi số tiền tính bằng triệu đồng và là SỐ CỦA GAME (xem data/cau-hinh.json). */
import * as L from './lich.js';

export const KHOA = 'vcmn-save-v1';
export const KHOA_CAI_DAT = 'vcmn-settings-v1';
export const PHIEN_BAN = 1;
export const D = {}; // dữ liệu nạp từ data/*.json

export async function napDuLieu() {
  const tep = ['tam-ly', 'cau-hinh', 'nha-cung-cap', 'tinh-huong'];
  const kq = await Promise.all(tep.map((t) => fetch(`data/${t}.json`).then((r) => r.json())));
  D.tamLy = kq[0]; D.ch = kq[1]; D.ncc = kq[2]; D.th = kq[3];
}

export const lamTron = (x, n = 1) => Math.round(x * 10 ** n) / 10 ** n;
export const kep = (x, a = 0, b = 100) => Math.max(a, Math.min(b, x));
export const fmtTien = (x) => `${lamTron(x, 1).toLocaleString('vi-VN')} triệu`;

/* ---------- Trạng thái ---------- */
export function trangThaiMoi(giuTien = null) {
  return {
    v: PHIEN_BAN, seed: (Date.now() % 2147483647) || 12345, scene: { id: 'bat_dau' }, sit: null, ch: 0,
    vai: null, ten: '', nghe: 'van_phong', tietKiem: 'vua', kieuMinh: 'can_than', sinhMinh: '', ban: null, xemNgay: true,
    tien: giuTien ?? 0, no: 0, tienGiu: giuTien,
    ngay: D.ch.ngay_bat_dau, buoi: 0, ngayLuong: 30,
    tinhCam: 25, hoTrai: 50, hoGai: 50, cangMinh: 20, cangAy: 20,
    heDa: 0, raMat: false, khu: 'tp', khach: 80, ngayCuoi: null, ngay_sub: 'khu', thayXem: false, daChotKH: false,
    nganSach: 0, hd: {}, ky: 'ky_quy', daKy: false, moc: [], daHoi: {}, daDangKy: false, toiGian: false,
    thuNghiem: false, daThay: {}, thayDaThay: false, seen: {}, khachDiem: 50, nhatKy: [], ketThuc: null, tuan: 0,
    suCo: [], suCoIdx: 0, nghiIdx: 0, dungGio: 0, tienMung: 0,
  };
}
export function khoiTao(s, { vai, ten, nghe, tietKiem, kieuMinh, sinhMinh, xemNgay }) {
  const cfg = D.ch;
  Object.assign(s, { vai, ten, nghe, tietKiem, kieuMinh, sinhMinh, xemNgay });
  if (s.tienGiu == null) s.tien = cfg.tiet_kiem.find((t) => t.id === tietKiem).tien;
  s.ch = 1;
}
export const luong = (s) => D.ch.nghe.find((n) => n.id === s.nghe).luong;
export const khuVuc = (s) => (s.khu === 'que' ? 'quê' : 'thành phố');

/* ---------- Số ngẫu nhiên có hạt giống, lưu trong trạng thái ---------- */
export function rng(s) {
  s.seed = (s.seed + 0x6d2b79f5) | 0;
  let t = s.seed;
  t = Math.imul(t ^ (t >>> 15), t | 1);
  t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
  return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
}
export const rngKhoang = (s, [a, b]) => a + (b - a) * rng(s);

/* ---------- Tâm lý (đọc từ tam-ly.json) ---------- */
export const kieuCua = (id) => D.tamLy.kieu.find((k) => k.id === id);
/** Độ khớp -1..1 giữa người ấy và một lựa chọn nghiêng về cực `huong` (-1 hoặc +1) của trục `truc`. */
export function khop(s, truc, huong, ai = 'ban') {
  const kieu = kieuCua(ai === 'ban' ? s.ban.kieu : s.kieuMinh);
  return 1 - Math.abs(kieu.diem[truc] - 2 * huong) / 2;
}
export const tenTruc = (id) => D.tamLy.truc.find((t) => t.id === id);

/* ---------- Hiệu ứng ---------- */
export function ap(s, e) {
  const nk = [];
  if (e.tien) { s.tien = lamTron(s.tien + e.tien); }
  if (e.no) s.no = lamTron(s.no + e.no);
  if (e.tinh_cam) s.tinhCam = kep(s.tinhCam + e.tinh_cam);
  if (e.ho) { s.hoTrai = kep(s.hoTrai + e.ho); s.hoGai = kep(s.hoGai + e.ho); }
  if (e.ho_trai) s.hoTrai = kep(s.hoTrai + e.ho_trai);
  if (e.ho_gai) s.hoGai = kep(s.hoGai + e.ho_gai);
  if (e.cang) { s.cangMinh = kep(s.cangMinh + e.cang); s.cangAy = kep(s.cangAy + e.cang); }
  if (e.cang_minh) s.cangMinh = kep(s.cangMinh + e.cang_minh);
  if (e.cang_ay) s.cangAy = kep(s.cangAy + e.cang_ay);
  if (e.khach) s.khachDiem = kep(s.khachDiem + e.khach);
  if (e.khop) {
    const k = e.khop, m = khop(s, k.truc, k.huong);
    if (k.tinh_cam) s.tinhCam = kep(s.tinhCam + Math.round(k.tinh_cam * m));
    if (k.cang) {
      const he = D.tamLy.luat.he_so_khop_cang;
      // khớp cao thì giảm căng thẳng nhiều hơn (cang âm) hoặc tăng ít hơn (cang dương)
      const d = k.cang < 0 ? k.cang * (0.5 + 0.5 * (m + 1) / 1) * he * 1.6 : k.cang * (1 - 0.5 * (m + 1) / 1) * he * 1.6;
      s.cangAy = kep(s.cangAy + Math.round(d));
      s.cangMinh = kep(s.cangMinh + Math.round(d * 0.7));
    }
    nk.push(m);
  }
  if (e.tg) dungBuoi(s, e.tg);
  return nk;
}

/* ---------- Thời gian ---------- */
export const laNgayThuong = (ngay) => { const t = L.thongTinNgay(ngay).thu; return t >= 1 && t <= 5; };
export const conLai = (s) => (s.ngayCuoi ? L.khoangCachNgay(s.ngay, s.ngayCuoi) : null);
export const tenBuoi = ['Sáng', 'Chiều', 'Tối'];
export function ngayVN(ngay) {
  const t = L.thongTinNgay(ngay), thu = ['Chủ nhật', 'Thứ hai', 'Thứ ba', 'Thứ tư', 'Thứ năm', 'Thứ sáu', 'Thứ bảy'][t.thu];
  const [y, m, d] = ngay.split('-');
  return `${thu}, ${Number(d)}/${Number(m)}/${y}`;
}
/** Bỏ qua các buổi đi làm (ngày thường, sáng và chiều) để tới buổi trống. */
export function chuanBuoi(s) {
  while (laNgayThuong(s.ngay) && s.buoi < 2 && s.ch >= 1) s.buoi = 2;
}
export function dungBuoi(s, n = 1) {
  chuanBuoi(s);
  s.buoi += n;
  while (s.buoi >= 3) { s.buoi -= 3; quaNgay(s); if (s.sit) return; }
  chuanBuoi(s);
}
/** Một ngày trôi qua: sinh hoạt phí, lương, lãi, mốc đóng tiền. Dừng nếu có tình huống mở ra. */
export function quaNgay(s) {
  s.ngay = L.congNgay(s.ngay, 1);
  s.tien = lamTron(s.tien - D.ch.sinh_hoat_thang / 30, 2);
  if (s.tien < 0) { // hết tiền trong ví: vay tạm để đủ sinh hoạt, không để ví âm
    const thieu = lamTron(-s.tien + 0.5, 1); s.no = lamTron(s.no + thieu); s.tien = lamTron(s.tien + thieu, 2);
    s.nhatKy.unshift(`Ví cạn: bạn vay tạm ${fmtTien(thieu)} để sinh hoạt.`);
  }
  s.ngayLuong -= 1;
  if (s.ngayLuong <= 0) {
    s.ngayLuong = 30;
    s.tien = lamTron(s.tien + luong(s));
    if (s.no > 0) s.no = lamTron(s.no * (1 + D.ch.vay.lai_nam / 12));
    s.nhatKy.unshift(`Tới kỳ lương: nhận ${fmtTien(luong(s))}.`);
  }
  if (s.ch === 5) kiemMoc(s);
  if (s.tinhCam <= 0) ketThuc(s, 'chia_tay');
}
function kiemMoc(s) {
  for (let i = 0; i < s.moc.length; i++) {
    const m = s.moc[i];
    if (m.daTra || m.sauTiec) continue;
    if (L.khoangCachNgay(m.han, s.ngay) >= 0) {
      if (s.tien >= m.so) { s.tien = lamTron(s.tien - m.so); m.daTra = true; s.nhatKy.unshift(`Đã đóng "${m.nhan}": ${fmtTien(m.so)}.`); }
      else { s.sit = { kind: 'th', id: 'khong_kip_moc', moc: i }; return; }
    }
  }
}
export function tuaNgay(s, n) { for (let i = 0; i < n && !s.sit && s.ch === 5 && s.scene.id !== 'ending'; i++) { dungBuoi(s, 3); if (s.ngayCuoi && conLai(s) <= 0) break; } }

/* ---------- Ngày cưới, xem ngày ---------- */
export const sinhCoDau = (s) => (s.vai === 'chu_re' ? s.ban.sinh : s.sinhMinh);
export const sinhChuRe = (s) => (s.vai === 'chu_re' ? s.sinhMinh : s.ban.sinh);
export function chiHai(s) {
  return { cd: L.thongTinNgay(sinhCoDau(s)).canChiNam.chi, cr: L.thongTinNgay(sinhChuRe(s)).canChiNam.chi };
}
export function diemCuaNgay(s, ngay) { const { cd, cr } = chiHai(s); return L.diemNgay(ngay, cd, cr); }
export function heSoNgay(s, ngay) {
  const cfg = D.ch.ngay_dep_gia, dn = diemCuaNgay(s, ngay);
  let h = 0;
  if (s.xemNgay && dn.diem >= 70) h += cfg.hoang_dao;
  if (dn.cuoiTuan) h += cfg.cuoi_tuan; else if (dn.info.thu >= 1 && dn.info.thu <= 4) h += cfg.ngay_thuong;
  return h;
}
export function tuoiKhongOn(s) {
  const nc = L.xemNamCuoi(sinhCoDau(s), sinhChuRe(s), s.ngayCuoi);
  const dem = [];
  if (nc.tuoi.muc === 'xung') dem.push('tuoi_xung');
  if (nc.kimLau.pham) dem.push('kim_lau');
  if (nc.tamTaiCoDau.pham || nc.tamTaiChuRe.pham) dem.push('tam_tai');
  return { ds: dem, nc };
}
export function ungVien(s) {
  // Mỗi tuần một ngày tốt nhất (điểm cao nhất, hòa thì ngày sớm), trong khoảng 100-190 ngày kể từ nay.
  const tu = L.congNgay(s.ngay, 100), kq = [];
  for (let w = 0; w < 13; w++) {
    let tot = null;
    for (let d = 0; d < 7; d++) {
      const ng = L.congNgay(tu, w * 7 + d), dn = diemCuaNgay(s, ng);
      const diem = s.xemNgay ? dn.diem : (dn.cuoiTuan ? 60 : 50);
      if (!tot || diem > tot.diem) tot = { ngay: ng, diem, dn };
    }
    kq.push(tot);
  }
  return kq;
}

/* ---------- Giá, hợp đồng, mốc đóng tiền ---------- */
export const nccBy = (id) => D.ncc.nha_cung_cap.find((n) => n.id === id);
export const soBan = (s) => Math.ceil(s.khach / 10);
export function giaGoi(s, nccId, goiId) {
  const n = nccBy(nccId), g = n.goi.find((x) => x.id === goiId);
  let co = n.don_vi === 'ban' ? g.gia * soBan(s) + (g.co_dinh || 0) : n.don_vi === 'khach' ? g.gia * s.khach : g.gia;
  if (n.nhay_ngay && s.ngayCuoi) co *= 1 + heSoNgay(s, s.ngayCuoi);
  return lamTron(co, 1);
}
export function datGoi(s, loai, nccId, goiId) {
  const n = nccBy(nccId);
  s.hd[loai] = { ncc: nccId, goi: goiId, gia: giaGoi(s, nccId, goiId), phatSinh: (n.yeu_an.phat_sinh || 0) };
}
export const tongHD = (s) => lamTron(Object.values(s.hd).reduce((t, h) => t + h.gia, 0), 1);
export function tongPhai(s) {
  const t = tongHD(s);
  return lamTron(s.ky === 'ky_quy' ? t * (1 + D.ch.ky_quy_phi) : t * (1 - D.ch.tra_thang_giam), 1);
}
export function xepMoc(s) {
  const tong = tongPhai(s);
  s.moc = D.ch.moc_dong_tien.map((m) => ({
    id: m.id, nhan: m.nhan, so: lamTron(tong * m.ty_le, 1), daTra: false,
    han: m.ngay === 'ky' ? s.ngay : (typeof m.ngay === 'number' ? L.congNgay(s.ngayCuoi, m.ngay) : s.ngayCuoi),
    sauTiec: m.ngay === 'sau_tiec', tyLe: m.ty_le,
  }));
}
/** Tính lại các mốc chưa đóng theo tổng mới (sau khi hạ gói). */
export function tinhLaiMoc(s) {
  const tong = tongPhai(s);
  for (const m of s.moc) if (!m.daTra) m.so = lamTron(tong * m.tyLe, 1);
}
export function haMotBac(s) {
  const bac = ['tron', 'du', 'gon'];
  const ds = Object.entries(s.hd).filter(([, h]) => h.goi !== 'gon').sort((a, b) => b[1].gia - a[1].gia);
  if (!ds.length) return false;
  const [loai, h] = ds[0];
  datGoi(s, loai, h.ncc, bac[bac.indexOf(h.goi) + 1]);
  tinhLaiMoc(s);
  return true;
}
export const baoNhieu = (s, id) => s.moc.find((m) => m.id === id);
export function daTraDen(s) { return lamTron(s.moc.filter((m) => m.daTra).reduce((t, m) => t + m.so, 0), 1); }
export function vay(s, so) { s.no = lamTron(s.no + so); s.tien = lamTron(s.tien + so); }

/* ---------- Điều kiện của tình huống ---------- */
export function thoaDK(s, dk = []) {
  return dk.every((d) => {
    switch (d) {
      case 'xem_ngay': return s.xemNgay;
      case 'tuoi_khong_on': return s.ngayCuoi && tuoiKhongOn(s).ds.length > 0;
      case 'it_khach': return s.khach <= 80;
      case 'vuot_ngan_sach': return tongPhai(s) > s.nganSach;
      case 'cang_cao': return Math.max(s.cangMinh, s.cangAy) >= 70;
      case 'ncc_bo_ngang': return !!s.hd.anh && s.daKy;
      case 'ngoai_troi': return s.hd.tiec && s.hd.tiec.ncc === 'ncc_vuon' && !(nccBy('ncc_vuon').nha_bat || []).includes(s.hd.tiec.goi);
      case 'co_gio_moc': return true;
      case 'he_thong': return false;
      default: return true;
    }
  });
}
export const thTheoId = (id) => D.th.tinh_huong.find((t) => t.id === id) || D.th.su_co.find((t) => t.id === id);
export function mo(s, id, ngoai = {}) { s.sit = { kind: 'th', id, ...ngoai }; }

/** Xử lý các cờ `co` của lựa chọn. Trả về chuỗi bổ sung cho kết quả (nếu có). */
export function xuLyCo(s, co, sit) {
  switch (co) {
    case 'them_khach': s.khach = 250; return 'Số khách tăng lên khoảng 250.';
    case 'chon_lai_ngay': s.ngayCuoi = null; s.ngay_sub = 'ngay'; s.scene = { id: 'ke_hoach' }; return 'Bạn quay lại bước chọn ngày.';
    case 'ha_goi': return haMotBac(s) ? 'Một hạng mục được hạ xuống một gói.' : 'Mọi hạng mục đã ở gói gọn, không hạ thêm được.';
    case 'nang_ngan_sach': s.nganSach = Math.max(s.nganSach, tongPhai(s)); return null;
    case 'vay_du': {
      const m = s.moc[sit.moc], thieu = lamTron(m.so - s.tien + 0.05, 1);
      vay(s, Math.max(thieu, 0)); s.tien = lamTron(s.tien - m.so); m.daTra = true; return `Vay thêm ${fmtTien(thieu)} và đóng đủ.`;
    }
    case 'gia_han': {
      const m = s.moc[sit.moc], phi = lamTron(m.so * D.ch.gia_han.phi, 1);
      s.no = lamTron(s.no + phi); m.han = L.congNgay(s.ngay, D.ch.gia_han.ngay); return `Phí gia hạn ${fmtTien(phi)} cộng vào nợ; mốc dời tới ${ngayVN(m.han)}.`;
    }
    case 'ha_goi_het': {
      const m = s.moc[sit.moc];
      let n = 0; while (s.tien < m.so && haMotBac(s)) n++;
      if (s.tien < m.so) { const t = lamTron(m.so - s.tien + 0.05, 1); vay(s, t); }
      s.tien = lamTron(s.tien - m.so); m.daTra = true; return `Đã hạ ${n} hạng mục xuống một bậc và đóng đủ.`;
    }
    case 'hoan_cuoi': hoanCuoi(s); return null;
    case 'bo_ngang_xu_ly': {
      const h = s.hd.anh; const coc = lamTron(h.gia * 0.3, 1);
      if (s.ky === 'ky_quy') return 'Vì đã ký quỹ, phần cọc được hoàn và một nhà cung cấp khác thay vào.';
      s.tien = lamTron(s.tien - coc); return `Vì trả thẳng, bạn mất ${fmtTien(coc)} tiền cọc và phải đặt người khác.`;
    }
    case 'tuy_nguoi_tin': {
      const luat = D.tamLy.luat;
      let ghi = [];
      if (D.tamLy.gia_dinh.nha_trai.tin_tam_linh > 0) { s.hoTrai = kep(s.hoTrai - 2 * D.tamLy.gia_dinh.nha_trai.tin_tam_linh); ghi.push('nhà trai'); }
      if (D.tamLy.gia_dinh.nha_gai.tin_tam_linh > 0) { s.hoGai = kep(s.hoGai - 2 * D.tamLy.gia_dinh.nha_gai.tin_tam_linh); ghi.push('nhà gái'); }
      return luat ? `Bên coi trọng chuyện này còn lấn cấn: ${ghi.join(', ')}.` : null;
    }
    default: return null;
  }
}
/** Chọn một lựa chọn của tình huống đang mở. */
export function chonTH(s, i) {
  const t = thTheoId(s.sit.id), lc = t.lua_chon[i];
  const sit = s.sit;
  ap(s, lc);
  const them = lc.co ? xuLyCo(s, lc.co, sit) : null;
  s.seen[sit.id] = true;
  s.sit = { kind: 'kq', id: sit.id, ket: lc.ket, them };
  if (s.tinhCam <= 0) ketThuc(s, 'chia_tay');
}
export function dongSit(s) { s.sit = null; }

export function hoanCuoi(s) {
  const da = daTraDen(s);
  s.tien = lamTron(s.tien + da * 0.5);
  s.hd = {}; s.moc = []; s.daKy = false; s.ngayCuoi = null; s.daChotKH = false; s.ngay_sub = 'ngay';
  s.ch = 3; s.hoTrai = kep(s.hoTrai - 6); s.hoGai = kep(s.hoGai - 6);
  s.nhatKy.unshift('Đã hoãn cưới: nhà cung cấp giữ lại một nửa tiền đã đóng; hai họ cần được báo.');
  ketThuc(s, 'hoan_cuoi');
}
/** Sau kết thúc "Hoãn cưới": chơi tiếp từ bước chọn ngày. */
export function choiTiepSauHoan(s) { s.ketThuc = null; s.scene = { id: 'ke_hoach' }; }
export function ketThuc(s, id) { s.ketThuc = id; s.scene = { id: 'ending' }; s.sit = null; }

/* ---------- Tổng kết ---------- */
export function chamDiem(s, tienMung, conLai_) {
  const cang = (s.cangMinh + s.cangAy) / 2;
  const cap = kep(Math.round(s.tinhCam * 0.6 + (100 - cang) * 0.4));
  const rong = lamTron(s.tien + tienMung - conLai_ - s.no, 1);
  const taiChinh = kep(Math.round(50 + rong / 2));
  return { cap, nhaTrai: Math.round(s.hoTrai), nhaGai: Math.round(s.hoGai), khach: Math.round(s.khachDiem), taiChinh, rong };
}
export function chonKetThuc(s, dd, rong) {
  const no = s.no > 0 || rong < 0;
  const dk = {
    nho_am: s.khach <= 80 && !no && s.tinhCam >= 60 && rong >= 20,
    tron_ven: !no && s.tinhCam >= 60 && s.hoTrai >= 55 && s.hoGai >= 55 && dd.khach >= 55,
    rinh_rang_no: no,
  };
  if (dk.nho_am) return 'nho_am';
  if (dk.tron_ven) return 'tron_ven';
  if (dk.rinh_rang_no) return 'rinh_rang_no';
  return s.khach <= 80 ? 'nho_am' : 'tron_ven';
}
