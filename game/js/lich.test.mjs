// Chạy: node game/js/lich.test.mjs
import assert from 'node:assert/strict';
import * as L from './lich.js';
let n = 0;
const ok = (c, m) => { assert.ok(c, m); n++; };
const eq = (a, b, m) => { assert.deepEqual(a, b, m); n++; };
const am = (s) => { const { d, m, y } = L.parseNgay(s); const a = L.duongSangAm(d, m, y); return [a.ngay, a.thang, a.nam, a.nhuan]; };

// Mùng 1 Tết (mốc ngoài công thức: lịch in)
eq(am('2020-01-25'), [1, 1, 2020, false]);
eq(am('2023-01-22'), [1, 1, 2023, false]);
eq(am('2024-02-10'), [1, 1, 2024, false]);
eq(am('2025-01-29'), [1, 1, 2025, false]);
eq(am('2026-02-17'), [1, 1, 2026, false]);
// Ngày trước Tết vẫn thuộc năm âm cũ (giao thừa)
eq(am('2024-02-09'), [30, 12, 2023, false]);
eq(am('2025-01-28'), [29, 12, 2024, false]);   // tháng Chạp 2024 thiếu (29 ngày)
// Rằm
eq(am('2023-09-29'), [15, 8, 2023, false]);   // Trung thu 2023
eq(am('2024-09-17'), [15, 8, 2024, false]);   // Trung thu 2024
// Tháng nhuận: 2020 nhuận 4, 2023 nhuận 2, 2025 nhuận 6
ok(am('2020-05-23')[3] === true && am('2020-05-23')[1] === 4, 'nhuận 4/2020');
ok(am('2023-03-22')[3] === true && am('2023-03-22')[1] === 2, 'nhuận 2/2023');
ok(am('2025-07-25')[3] === true && am('2025-07-25')[1] === 6, 'nhuận 6/2025');
eq(am('2023-03-21'), [30, 2, 2023, false]);   // nhuận 2 bắt đầu 22/3/2023
// Đầu tháng 1 dương vẫn là cuối năm âm trước
eq(am('2020-01-01')[2], 2019);
eq(am('1997-01-20')[2], 1996);                 // sinh trước Tết 1997 → năm âm 1996

// Can chi năm
eq(L.canChiNam(2020).ten, 'Canh Tý');
eq(L.canChiNam(2024).ten, 'Giáp Thìn');
eq(L.canChiNam(1984).ten, 'Giáp Tý');
eq(L.canChiNam(1996).ten, 'Bính Tý');
eq(L.thongTinNgay('1997-01-20').canChiNam.ten, 'Bính Tý');
// Can chi ngày: 2000-01-01 là Mậu Ngọ (mốc đã biết); cách nhau 60 ngày thì cùng can chi
eq(L.thongTinNgay('2000-01-01').canChiNgay.ten, 'Mậu Ngọ');
eq(L.thongTinNgay('2000-03-01').canChiNgay.ten, 'Mậu Ngọ');
// Thứ trong tuần
eq(L.thongTinNgay('2000-01-01').thu, 6);
eq(L.thongTinNgay('2026-11-19').thu, 4);        // thứ Năm
// Cộng ngày
eq(L.congNgay('2024-02-28', 2), '2024-03-01');
eq(L.khoangCachNgay('2026-11-19', '2027-01-01'), 43);

// Xem tuổi
eq(L.xemTuoi(0, 4).muc, 'rat_hop');   // Tý – Thìn
eq(L.xemTuoi(0, 1).muc, 'hop');       // Tý – Sửu
eq(L.xemTuoi(0, 6).muc, 'xung');      // Tý – Ngọ
eq(L.xemTuoi(0, 2).muc, 'binh_thuong');
eq(L.xemTuoi(3, 3).muc, 'binh_thuong');
// Kim Lâu: 1, 3, 6, 8 phạm
for (const t of [1, 3, 6, 8, 10, 12, 15, 17]) ok(L.kimLau(t).pham, 'KL ' + t);
for (const t of [2, 4, 5, 7, 9, 11, 13, 18]) ok(!L.kimLau(t).pham, 'không KL ' + t);
// Tam Tai: tuổi Tý gặp Dần, Mão, Thìn
ok(L.tamTai(0, 2).pham && L.tamTai(0, 3).pham && L.tamTai(0, 4).pham && !L.tamTai(0, 5).pham);
ok(L.tamTai(6, 8).pham && L.tamTai(11, 5).pham && L.tamTai(5, 11).pham);
// Năm cưới 2027 (Đinh Mùi), cô dâu sinh 1997-03-08 (Đinh Sửu, tuổi mụ 31 → dư 4: không phạm)
const nc = L.xemNamCuoi('1997-03-08', '1996-05-12', '2027-05-01');
eq(nc.namCuoi, 'Đinh Mùi');
eq(nc.kimLau.tuoiMu, 31);
ok(!nc.kimLau.pham);

// Ngày hoàng đạo: bảng — tháng Giêng, ngày Tý là Thanh Long; tháng Hai ngày Dần
ok(L.hoangDao(0, 1).than === 'Thanh Long' && L.hoangDao(2, 2).than === 'Thanh Long' && L.hoangDao(8, 5).than === 'Thanh Long');
eq([0, 1, 4, 5, 7, 10].map((c) => L.hoangDao(c, 1).hoangDao), [true, true, true, true, true, true]);
eq(L.hoangDao(2, 1).hoangDao, false);
// Mỗi tháng đúng sáu chi hoàng đạo
for (let t = 1; t <= 12; t++) eq([...Array(12).keys()].filter((c) => L.hoangDao(c, t).hoangDao).length, 6);
// Giờ hoàng đạo: ngày Tý có Tý, Sửu, Mão, Ngọ, Thân, Dậu (theo xem-ngay.md)
eq(L.gioHoangDao(0).map((g) => g.chi), [0, 1, 3, 6, 8, 9]);
eq(L.gioHoangDao(0)[0].nhan, 'giờ Tý (23:00–01:00)');
for (let c = 0; c < 12; c++) eq(L.gioHoangDao(c).length, 6);
// Điểm ngày
const dn = L.diemNgay('2024-02-10'); // mùng 1 Tết Giáp Thìn, thứ Bảy
ok(dn.diem >= 0 && dn.diem <= 100);
ok(dn.chiTiet.reduce((s, x) => s + x.d, 0) >= dn.diem, 'cộng chi tiết khớp (trước khi kẹp)');
ok(dn.cuoiTuan);
// Mùng 3 âm là Tam Nương
eq(am('2024-02-12')[0], 3);
ok(L.diemNgay('2024-02-12').kieng);
// Tháng Bảy âm
ok(L.diemNgay('2024-08-20').thangBay); // 17/7 âm
// Quy tắc công khai, không ngẫu nhiên
eq(L.diemNgay('2027-05-01', 0, 6).diem, L.diemNgay('2027-05-01', 0, 6).diem);

// Thần số học (tính tay)
eq(L.conSoChuDao('1990-01-01').so, 3);   // 1 + 1 + 19 = 21 → 3
eq(L.conSoChuDao('2000-10-10').so, 4);   // 1 + 1 + 2 = 4
eq(L.conSoChuDao('1980-02-29').so, 4);   // 11 + 2 + 18 = 31 → 4
eq(L.conSoChuDao('1992-02-29').so, 7);   // 11 + 2 + 21 = 34 → 7
eq(L.conSoChuDao('1996-05-12').so, 6);   // 3 + 5 + 25 = 33 → 6
eq(L.conSoChuDao('2007-01-01').so, 11);  // 1 + 1 + 9 = 11, giữ số 11
eq(L.namCaNhan('1996-05-12', 2027).so, 1); // 3 + 5 + 11 = 19 → 10 → 1
// Cung hoàng đạo
eq(L.cungHoangDao('1996-05-12').ten, 'Kim Ngưu');
eq(L.cungHoangDao('1997-03-08').ten, 'Song Ngư');
eq(L.cungHoangDao('1990-01-19').ten, 'Ma Kết');
eq(L.cungHoangDao('1990-01-20').ten, 'Bảo Bình');
eq(L.cungHoangDao('1990-12-25').ten, 'Ma Kết');
eq(L.cungHoangDao('1990-12-21').ten, 'Nhân Mã');
ok(L.cungHop('Lửa', 'Khí').hop && L.cungHop('Đất', 'Nước').hop && !L.cungHop('Lửa', 'Nước').hop);

console.log(n + ' kiểm tra đạt');
