/* Xem tuổi, xem ngày, xem giờ, thần số học, cung hoàng đạo.
 * Mô-đun thuần hàm: không đụng DOM, không ngẫu nhiên, không giờ hệ thống.
 * Quy tắc theo docs/game/xem-ngay.md (chưa có người am hiểu soát: xem mục "Chưa đối chiếu" cuối tệp).
 * Đổi dương sang âm: thuật toán của Hồ Ngọc Đức, múi giờ +7.
 * Mọi nhận định đều trả kèm "nguon" ("theo lịch âm"…) và "vi_sao" để giao diện giải thích. */

export const CAN = ['Giáp', 'Ất', 'Bính', 'Đinh', 'Mậu', 'Kỷ', 'Canh', 'Tân', 'Nhâm', 'Quý'];
export const CHI = ['Tý', 'Sửu', 'Dần', 'Mão', 'Thìn', 'Tỵ', 'Ngọ', 'Mùi', 'Thân', 'Dậu', 'Tuất', 'Hợi'];
const TZ = 7;
const PI = Math.PI;
const INT = Math.floor;

/* ---------- Ngày Julius và đổi dương → âm ---------- */
export function jdFromDate(dd, mm, yy) {
  const a = INT((14 - mm) / 12);
  const y = yy + 4800 - a;
  const m = mm + 12 * a - 3;
  let jd = dd + INT((153 * m + 2) / 5) + 365 * y + INT(y / 4) - INT(y / 100) + INT(y / 400) - 32045;
  if (jd < 2299161) jd = dd + INT((153 * m + 2) / 5) + 365 * y + INT(y / 4) - 32083;
  return jd;
}
export function jdToDate(jd) {
  let a, b, c;
  if (jd > 2299160) { a = jd + 32044; b = INT((4 * a + 3) / 146097); c = a - INT((b * 146097) / 4); }
  else { b = 0; c = jd + 32082; }
  const d = INT((4 * c + 3) / 1461);
  const e = c - INT((1461 * d) / 4);
  const m = INT((5 * e + 2) / 153);
  return { day: e - INT((153 * m + 2) / 5) + 1, month: m + 3 - 12 * INT(m / 10), year: b * 100 + d - 4800 + INT(m / 10) };
}
function newMoon(k) {
  const T = k / 1236.85, T2 = T * T, T3 = T2 * T, dr = PI / 180;
  let Jd1 = 2415020.75933 + 29.53058868 * k + 0.0001178 * T2 - 0.000000155 * T3;
  Jd1 += 0.00033 * Math.sin((166.56 + 132.87 * T - 0.009173 * T2) * dr);
  const M = 359.2242 + 29.10535608 * k - 0.0000333 * T2 - 0.00000347 * T3;
  const Mpr = 306.0253 + 385.81691806 * k + 0.0107306 * T2 + 0.00001236 * T3;
  const F = 21.2964 + 390.67050646 * k - 0.0016528 * T2 - 0.00000239 * T3;
  let C1 = (0.1734 - 0.000393 * T) * Math.sin(M * dr) + 0.0021 * Math.sin(2 * dr * M);
  C1 = C1 - 0.4068 * Math.sin(Mpr * dr) + 0.0161 * Math.sin(dr * 2 * Mpr);
  C1 -= 0.0004 * Math.sin(dr * 3 * Mpr);
  C1 += 0.0104 * Math.sin(dr * 2 * F) - 0.0051 * Math.sin(dr * (M + Mpr));
  C1 -= 0.0074 * Math.sin(dr * (M - Mpr)) + 0.0004 * Math.sin(dr * (2 * F + M));
  C1 -= 0.0004 * Math.sin(dr * (2 * F - M)) - 0.0006 * Math.sin(dr * (2 * F + Mpr));
  C1 += 0.0010 * Math.sin(dr * (2 * F - Mpr)) + 0.0005 * Math.sin(dr * (2 * Mpr + M));
  const dt = T < -11
    ? 0.001 + 0.000839 * T + 0.0002261 * T2 - 0.00000845 * T3 - 0.000000081 * T * T3
    : -0.000278 + 0.000265 * T + 0.000262 * T2;
  return Jd1 + C1 - dt;
}
function sunLongitude(jdn) {
  const T = (jdn - 2451545.0) / 36525, T2 = T * T, dr = PI / 180;
  const M = 357.5291 + 35999.0503 * T - 0.0001559 * T2 - 0.00000048 * T * T2;
  const L0 = 280.46645 + 36000.76983 * T + 0.0003032 * T2;
  let DL = (1.9146 - 0.004817 * T - 0.000014 * T2) * Math.sin(dr * M);
  DL += (0.019993 - 0.000101 * T) * Math.sin(dr * 2 * M) + 0.00029 * Math.sin(dr * 3 * M);
  let L = L0 + DL;
  const omega = 125.04 - 1934.136 * T;
  L = L - 0.00569 - 0.00478 * Math.sin(omega * dr);
  L *= dr;
  return L - PI * 2 * INT(L / (PI * 2));
}
const sunLong = (dayNumber) => INT((sunLongitude(dayNumber - 0.5 - TZ / 24) / PI) * 6);
const newMoonDay = (k) => INT(newMoon(k) + 0.5 + TZ / 24);
function lunarMonth11(yy) {
  const off = jdFromDate(31, 12, yy) - 2415021;
  const k = INT(off / 29.530588853);
  let nm = newMoonDay(k);
  if (sunLong(nm) >= 9) nm = newMoonDay(k - 1);
  return nm;
}
function leapMonthOffset(a11) {
  const k = INT((a11 - 2415021.076998695) / 29.530588853 + 0.5);
  let last = 0, i = 1, arc = sunLong(newMoonDay(k + i));
  do { last = arc; i++; arc = sunLong(newMoonDay(k + i)); } while (arc !== last && i < 14);
  return i - 1;
}

/** Dương → âm. Trả {ngay, thang, nam, nhuan, jd}. */
export function duongSangAm(dd, mm, yy) {
  const dayNumber = jdFromDate(dd, mm, yy);
  const k = INT((dayNumber - 2415021.076998695) / 29.530588853);
  let monthStart = newMoonDay(k + 1);
  if (monthStart > dayNumber) monthStart = newMoonDay(k);
  let a11 = lunarMonth11(yy), b11 = a11, lunarYear;
  if (a11 >= monthStart) { lunarYear = yy; a11 = lunarMonth11(yy - 1); }
  else { lunarYear = yy + 1; b11 = lunarMonth11(yy + 1); }
  const lunarDay = dayNumber - monthStart + 1;
  const diff = INT((monthStart - a11) / 29);
  let lunarLeap = 0, lunarMonth = diff + 11;
  if (b11 - a11 > 365) {
    const leapDiff = leapMonthOffset(a11);
    if (diff >= leapDiff) { lunarMonth = diff + 10; if (diff === leapDiff) lunarLeap = 1; }
  }
  if (lunarMonth > 12) lunarMonth -= 12;
  if (lunarMonth >= 11 && diff < 4) lunarYear -= 1;
  return { ngay: lunarDay, thang: lunarMonth, nam: lunarYear, nhuan: lunarLeap === 1, jd: dayNumber };
}

/* ---------- Can chi ---------- */
/** Can chi của năm âm lịch. 2020 → Canh Tý. */
export function canChiNam(namAm) {
  const can = (((namAm - 4) % 10) + 10) % 10, chi = (((namAm - 4) % 12) + 12) % 12;
  return { can, chi, ten: CAN[can] + ' ' + CHI[chi], conGiap: CHI[chi] };
}
/** Can chi của ngày, từ số ngày Julius. */
export function canChiNgay(jd) {
  const chi = (jd + 1) % 12, can = (jd + 9) % 10;
  return { can, chi, ten: CAN[can] + ' ' + CHI[chi] };
}
export const tuoiMu = (namXemAm, namSinhAm) => namXemAm - namSinhAm + 1;

/** Phân tích chuỗi 'YYYY-MM-DD'. */
export function parseNgay(s) {
  const [y, m, d] = s.split('-').map(Number);
  return { d, m, y };
}
export function thongTinNgay(s) {
  const { d, m, y } = parseNgay(s);
  const am = duongSangAm(d, m, y);
  const cc = canChiNgay(am.jd);
  const thu = (am.jd + 1) % 7; // 0 = Chủ nhật
  return { duong: s, am, canChiNam: canChiNam(am.nam), canChiNgay: cc, thu, cuoiTuan: thu === 0 || thu === 6 };
}
export function congNgay(s, n) {
  const { d, m, y } = parseNgay(s);
  const t = jdToDate(jdFromDate(d, m, y) + n);
  return `${t.year}-${String(t.month).padStart(2, '0')}-${String(t.day).padStart(2, '0')}`;
}
export function khoangCachNgay(a, b) {
  const x = parseNgay(a), y = parseNgay(b);
  return jdFromDate(y.d, y.m, y.y) - jdFromDate(x.d, x.m, x.y);
}

/* ---------- Xem tuổi ---------- */
const TAM_HOP = [[8, 0, 4], [2, 6, 10], [5, 9, 1], [11, 3, 7]];
const LUC_HOP = [[0, 1], [2, 11], [3, 10], [4, 9], [5, 8], [6, 7]];
const LUC_XUNG = [[0, 6], [1, 7], [2, 8], [3, 9], [4, 10], [5, 11]];
const coCap = (ds, a, b) => ds.some(([x, y]) => (x === a && y === b) || (x === b && y === a));

/** Hai con giáp (chỉ số chi 0-11) hợp hay xung. Trả {muc: 'rat_hop'|'hop'|'xung'|'binh_thuong', nhan, vi_sao}. */
export function xemTuoi(chiA, chiB) {
  const ten = `${CHI[chiA]} và ${CHI[chiB]}`;
  if (TAM_HOP.some((g) => g.includes(chiA) && g.includes(chiB) && chiA !== chiB))
    return { muc: 'rat_hop', nhan: 'Rất hợp', vi_sao: `${ten} nằm trong một nhóm tam hợp`, nguon: 'theo lịch âm (tam hợp)' };
  if (coCap(LUC_HOP, chiA, chiB))
    return { muc: 'hop', nhan: 'Hợp', vi_sao: `${ten} là một cặp lục hợp`, nguon: 'theo lịch âm (lục hợp)' };
  if (coCap(LUC_XUNG, chiA, chiB))
    return { muc: 'xung', nhan: 'Xung', vi_sao: `${ten} là một cặp lục xung`, nguon: 'theo lịch âm (lục xung)' };
  return { muc: 'binh_thuong', nhan: 'Bình thường', vi_sao: `${ten} không thuộc nhóm hợp hay xung nào`, nguon: 'theo lịch âm' };
}

/* ---------- Xem năm cưới ---------- */
/** Kim Lâu theo tuổi mụ của cô dâu (tuổi mụ chia 9 dư 1, 3, 6, 8). */
export function kimLau(tuoiMuCoDau) {
  const du = tuoiMuCoDau % 9;
  return { pham: [1, 3, 6, 8].includes(du), tuoiMu: tuoiMuCoDau, vi_sao: `Tuổi mụ ${tuoiMuCoDau}, chia 9 dư ${du}${[1, 3, 6, 8].includes(du) ? ' (dư 1, 3, 6 hoặc 8 là phạm)' : ''}`, nguon: 'theo lịch âm (Kim Lâu)' };
}
const TAM_TAI = [
  { tuoi: [8, 0, 4], nam: [2, 3, 4] },
  { tuoi: [2, 6, 10], nam: [8, 9, 10] },
  { tuoi: [5, 9, 1], nam: [11, 0, 1] },
  { tuoi: [11, 3, 7], nam: [5, 6, 7] },
];
/** Tam Tai: chi của người và chi của năm xem. */
export function tamTai(chiNguoi, chiNam) {
  const nhom = TAM_TAI.find((g) => g.tuoi.includes(chiNguoi));
  const pham = nhom.nam.includes(chiNam);
  return { pham, vi_sao: `Tuổi ${CHI[chiNguoi]} gặp năm ${CHI[chiNam]}${pham ? ': nằm trong ba năm Tam Tai' : ': không nằm trong ba năm Tam Tai'}`, nguon: 'theo lịch âm (Tam Tai)' };
}
/** Gộp xem năm cưới. sinhCoDau, sinhChuRe: 'YYYY-MM-DD' (dương). ngayCuoi: 'YYYY-MM-DD'. */
export function xemNamCuoi(sinhCoDau, sinhChuRe, ngayCuoi) {
  const nc = thongTinNgay(ngayCuoi);
  const cd = thongTinNgay(sinhCoDau), cr = thongTinNgay(sinhChuRe);
  const kl = kimLau(tuoiMu(nc.am.nam, cd.am.nam));
  const ttCd = tamTai(cd.canChiNam.chi, nc.canChiNam.chi);
  const ttCr = tamTai(cr.canChiNam.chi, nc.canChiNam.chi);
  return { namCuoi: nc.canChiNam.ten, kimLau: kl, tamTaiCoDau: ttCd, tamTaiChuRe: ttCr, tuoi: xemTuoi(cd.canChiNam.chi, cr.canChiNam.chi) };
}

/* ---------- Xem ngày ---------- */
/** Sáu ngày hoàng đạo theo chi của ngày, theo tháng âm (bảng trong xem-ngay.md; tháng nhuận dùng số tháng của nó). */
const THANH_LONG_THANG = { 1: 0, 7: 0, 2: 2, 8: 2, 3: 4, 9: 4, 4: 6, 10: 6, 5: 8, 11: 8, 6: 10, 12: 10 };
const VI_TRI_HOANG_DAO = [0, 1, 4, 5, 7, 10];
const TEN_THAN = ['Thanh Long', 'Minh Đường', 'Kim Quỹ', 'Bảo Quang', 'Ngọc Đường', 'Tư Mệnh'];
export function hoangDao(chiNgay, thangAm) {
  const goc = THANH_LONG_THANG[thangAm];
  const vt = (((chiNgay - goc) % 12) + 12) % 12;
  const i = VI_TRI_HOANG_DAO.indexOf(vt);
  return { hoangDao: i >= 0, than: i >= 0 ? TEN_THAN[i] : null };
}
const TAM_NUONG = [3, 7, 13, 18, 22, 27];
const NGUYET_KY = [5, 14, 23];

/** Điểm của một ngày (0–100). chiCoDau, chiChuRe: chỉ số chi con giáp của hai người (hoặc null để bỏ qua xung tuổi).
 *  Trả điểm kèm danh sách "chi_tiet" để người chơi bấm xem vì sao. */
export function diemNgay(ngayDuong, chiCoDau = null, chiChuRe = null) {
  const t = thongTinNgay(ngayDuong);
  const chiTiet = [{ y: 'Điểm khởi đầu', d: 50 }];
  const hd = hoangDao(t.canChiNgay.chi, t.am.thang);
  chiTiet.push(hd.hoangDao
    ? { y: `Ngày ${t.canChiNgay.ten} là ngày hoàng đạo (${hd.than}) theo lịch âm`, d: 25 }
    : { y: `Ngày ${t.canChiNgay.ten} là ngày hắc đạo theo lịch âm`, d: -15 });
  const kieng = [];
  if (TAM_NUONG.includes(t.am.ngay)) kieng.push(`mùng ${t.am.ngay} là ngày Tam Nương`);
  if (NGUYET_KY.includes(t.am.ngay)) kieng.push(`mùng ${t.am.ngay} là ngày Nguyệt Kỵ`);
  if (kieng.length) chiTiet.push({ y: `Ngày kiêng theo lịch âm: ${kieng.join(', ')}`, d: -25 });
  const xung = [];
  if (chiCoDau != null && coCap(LUC_XUNG, t.canChiNgay.chi, chiCoDau)) xung.push('cô dâu');
  if (chiChuRe != null && coCap(LUC_XUNG, t.canChiNgay.chi, chiChuRe)) xung.push('chú rể');
  if (xung.length) chiTiet.push({ y: `Chi của ngày (${CHI[t.canChiNgay.chi]}) xung với tuổi ${xung.join(' và ')} theo lịch âm`, d: -25 });
  if (t.am.thang === 7) chiTiet.push({ y: 'Tháng Bảy âm lịch, nhiều nhà tránh cưới', d: -15 });
  if (t.cuoiTuan) chiTiet.push({ y: 'Cuối tuần, thuận cho khách (không liên quan tín ngưỡng)', d: 10 });
  const diem = Math.max(0, Math.min(100, chiTiet.reduce((s, x) => s + x.d, 0)));
  return {
    diem, ngayDep: diem >= 70, hoangDao: hd.hoangDao, than: hd.than,
    kieng: kieng.length > 0, xungTuoi: xung, thangBay: t.am.thang === 7, cuoiTuan: t.cuoiTuan,
    chiTiet, nguon: 'theo lịch âm', info: t,
  };
}

/* ---------- Xem giờ ---------- */
const GIO_THANH_LONG = { 2: 0, 8: 0, 3: 2, 9: 2, 4: 4, 10: 4, 5: 6, 11: 6, 0: 8, 6: 8, 1: 10, 7: 10 };
/** Sáu giờ hoàng đạo của một ngày (theo chi của ngày). Mỗi giờ: {chi, ten, tu, den} (giờ Tý 23:00–1:00). */
export function gioHoangDao(chiNgay) {
  const goc = GIO_THANH_LONG[chiNgay];
  return VI_TRI_HOANG_DAO.map((v, i) => {
    const chi = (goc + v) % 12;
    const tu = (chi * 2 + 23) % 24, den = (tu + 2) % 24;
    return { chi, ten: CHI[chi], than: TEN_THAN[i], tu, den, nhan: `giờ ${CHI[chi]} (${String(tu).padStart(2, '0')}:00–${String(den).padStart(2, '0')}:00)` };
  }).sort((a, b) => a.chi - b.chi);
}

/* ---------- Thần số học ---------- */
function rutGon(n, giuSo = [11, 22]) {
  while (n > 9 && !giuSo.includes(n)) n = String(n).split('').reduce((s, c) => s + Number(c), 0);
  return n;
}
const tongChuSo = (n) => String(n).split('').reduce((s, c) => s + Number(c), 0);
const YNGHIA_SO = {
  1: 'tự lập, thích dẫn đầu', 2: 'nhạy cảm, thích hoà hợp', 3: 'vui vẻ, thích gặp gỡ', 4: 'chắc chắn, thích ngăn nắp',
  5: 'ưa thay đổi, thích khám phá', 6: 'chu đáo, coi trọng gia đình', 7: 'thích suy ngẫm, cần yên tĩnh', 8: 'có chí, coi trọng thành quả',
  9: 'rộng lượng, thích giúp người', 11: 'trực giác tốt, nhiều ý tưởng', 22: 'thích xây dựng việc lớn',
};
/** Con số chủ đạo: cộng mọi chữ số ngày, tháng, năm sinh dương lịch, rút về 1–9, giữ 11 và 22. */
export function conSoChuDao(ngaySinh) {
  const { d, m, y } = parseNgay(ngaySinh);
  const tong = tongChuSo(d) + tongChuSo(m) + tongChuSo(y);
  const so = rutGon(tong);
  return { so, nghia: YNGHIA_SO[so], vi_sao: `${tongChuSo(d)} + ${tongChuSo(m)} + ${tongChuSo(y)} = ${tong}${tong !== so ? ` → ${so}` : ''}`, nguon: 'theo thần số học' };
}
/** Năm cá nhân: ngày sinh + tháng sinh + năm đang xét. */
export function namCaNhan(ngaySinh, namXet) {
  const { d, m } = parseNgay(ngaySinh);
  const tong = tongChuSo(d) + tongChuSo(m) + tongChuSo(namXet);
  return { so: rutGon(tong, []), vi_sao: `${tongChuSo(d)} + ${tongChuSo(m)} + ${tongChuSo(namXet)} = ${tong}`, nguon: 'theo thần số học' };
}
/** Một dòng nhận xét về ngày cưới, theo số chủ đạo của hai người và số của ngày cưới. */
export function nhanXetNgayCuoi(sinhA, sinhB, ngayCuoi) {
  const a = conSoChuDao(sinhA).so, b = conSoChuDao(sinhB).so;
  const { d, m, y } = parseNgay(ngayCuoi);
  const soNgay = rutGon(tongChuSo(d) + tongChuSo(m) + tongChuSo(y), []);
  const chung = a === b || rutGon(a + b, []) === soNgay;
  return {
    soNgay, chung,
    nhan_xet: chung ? `Số của ngày cưới là ${soNgay}, khớp với con số của hai bạn (${a} và ${b}) theo thần số học.` : `Số của ngày cưới là ${soNgay}; con số của hai bạn là ${a} và ${b}. Theo thần số học đây chỉ là một nét thêm, không có nghĩa tốt hay xấu.`,
    nguon: 'theo thần số học',
  };
}

/* ---------- Cung hoàng đạo ---------- */
const CUNG = [
  ['Ma Kết', 'Đất', 1, 19], ['Bảo Bình', 'Khí', 2, 18], ['Song Ngư', 'Nước', 3, 20], ['Bạch Dương', 'Lửa', 4, 19],
  ['Kim Ngưu', 'Đất', 5, 20], ['Song Tử', 'Khí', 6, 20], ['Cự Giải', 'Nước', 7, 22], ['Sư Tử', 'Lửa', 8, 22],
  ['Xử Nữ', 'Đất', 9, 22], ['Thiên Bình', 'Khí', 10, 22], ['Bọ Cạp', 'Nước', 11, 21], ['Nhân Mã', 'Lửa', 12, 21],
];
/** Cung theo ngày sinh dương lịch. Mỗi cung kết thúc ở (tháng, ngày) cuối cùng ghi trong bảng; sau đó sang cung kế. */
export function cungHoangDao(ngaySinh) {
  const { d, m } = parseNgay(ngaySinh);
  const i = d <= CUNG[m - 1][3] ? m - 1 : m % 12;
  return { ten: CUNG[i][0], nhom: CUNG[i][1], nguon: 'theo cung hoàng đạo' };
}
/** Hợp nhau theo quy ước: Lửa với Khí, Đất với Nước, và cùng nhóm. */
export function cungHop(nhomA, nhomB) {
  const hop = nhomA === nhomB || (nhomA === 'Lửa' && nhomB === 'Khí') || (nhomA === 'Khí' && nhomB === 'Lửa') || (nhomA === 'Đất' && nhomB === 'Nước') || (nhomA === 'Nước' && nhomB === 'Đất');
  return { hop, nguon: 'theo cung hoàng đạo' };
}

/* ---------- Chưa đối chiếu (báo chủ dự án) ----------
 * - Bảng ngày hoàng đạo ở đây khoá theo THÁNG ÂM như xem-ngay.md; nhiều lịch in khoá theo tiết khí. Tháng nhuận dùng số tháng của nó.
 * - Cung hoàng đạo dùng ngày đổi cung phổ biến, các sách lệch nhau một ngày.
 * - Can chi ngày kiểm tra bằng ngày 2000-01-01 (Mậu Ngọ); các ngày khác mới là tính, chưa so lịch in. */
