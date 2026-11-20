/* Chương 3 (hai họ và kế hoạch) và chương 4 (nhà cung cấp). */
import { h, nut, lam, the, khung, ghi, store } from './ui.js';
import * as G from './logic.js';
import * as L from './lich.js';

const { D } = G;
const f = G.fmtTien;
const SUB = [['khu', 'Nơi cưới'], ['khach', 'Số khách'], ['ngay', 'Xem tuổi, chọn ngày'], ['ngan_sach', 'Ngân sách'], ['chot', 'Chốt']];

function lichAm(ng) {
  const t = L.thongTinNgay(ng);
  return `${t.am.ngay}/${t.am.thang}${t.am.nhuan ? ' (nhuận)' : ''} năm ${t.canChiNam.ten}, ngày ${t.canChiNgay.ten}`;
}
function panelTuoi(s) {
  const cd = L.thongTinNgay(G.sinhCoDau(s)), cr = L.thongTinNgay(G.sinhChuRe(s));
  const t = L.xemTuoi(cd.canChiNam.chi, cr.canChiNam.chi);
  const cung1 = L.cungHoangDao(G.sinhCoDau(s)), cung2 = L.cungHoangDao(G.sinhChuRe(s));
  const cc = L.cungHop(cung1.nhom, cung2.nhom);
  const so1 = L.conSoChuDao(G.sinhCoDau(s)), so2 = L.conSoChuDao(G.sinhChuRe(s));
  return the(h('h3', {}, 'Xem tuổi hai người'),
    h('p', {}, `Cô dâu tuổi ${cd.canChiNam.ten}, chú rể tuổi ${cr.canChiNam.ten}. Kết quả: ${t.nhan.toLowerCase()} (${t.nguon}).`),
    h('details', {}, h('summary', {}, 'Vì sao?'),
      h('p', {}, t.vi_sao + '.'), h('p', {}, `Con số chủ đạo: cô dâu ${so1.so} (${so1.vi_sao}), chú rể ${so2.so} (${so2.vi_sao}), ${so1.nguon}.`),
      h('p', {}, `Cung hoàng đạo: ${cung1.ten} và ${cung2.ten}, ${cc.hop ? 'hợp nhau' : 'không thuộc nhóm hợp'} theo quy ước (${cc.nguon}).`)),
    ghi('Tử vi, thần số học và cung hoàng đạo là tín ngưỡng và thói quen văn hoá, không phải khoa học kiểm chứng được. Game chỉ dùng chúng như một phần của phong tục.'));
}

function cardNgay(s, u, i, thay) {
  const t = u.dn.info, hs = G.heSoNgay(s, u.ngay);
  const nhan = s.xemNgay ? (u.diem >= 70 ? 'Ngày đẹp' : u.diem >= 50 ? 'Ngày bình thường' : 'Ngày chưa thuận') : (u.dn.cuoiTuan ? 'Cuối tuần' : 'Ngày thường');
  const gia = hs === 0 ? 'giá ngày như thường' : `giá tiệc ${hs > 0 ? 'cao hơn' : 'thấp hơn'} khoảng ${Math.abs(Math.round(hs * 100))}%`;
  return the(h('h3', {}, G.ngayVN(u.ngay)),
    s.xemNgay ? h('p', {}, `Âm lịch: ${lichAm(u.ngay)}.`) : null,
    h('p', {}, s.xemNgay ? `${nhan}, ${u.diem}/100 (theo lịch âm); ${gia}.` : `${nhan}; ${gia}.`),
    s.xemNgay ? h('details', {}, h('summary', {}, 'Vì sao điểm này?'),
      h('ul', {}, u.dn.chiTiet.map((c) => h('li', {}, `${c.y}: ${c.d > 0 && c.y !== 'Điểm khởi đầu' ? '+' : ''}${c.d}`))),
      thay ? h('p', {}, 'Giờ hoàng đạo: ' + L.gioHoangDao(t.canChiNgay.chi).map((g) => g.nhan).join('; ') + '.') : null) : null,
    nut('Chọn ngày này', lam((st) => {
      st.ngayCuoi = u.ngay;
      const luat = D.tamLy.luat;
      if (st.xemNgay && u.diem < 50) {
        const c1 = D.tamLy.gia_dinh.nha_trai.tin_tam_linh, c2 = D.tamLy.gia_dinh.nha_gai.tin_tam_linh;
        G.ap(st, { ho_trai: -luat.tin_tam_linh_ho_khi_ngay_xau * c1 / 2, ho_gai: -luat.tin_tam_linh_ho_khi_ngay_xau * c2 / 2 });
        const k = G.kieuCua(st.ban.kieu).tin_tam_linh;
        if (k > 0) G.ap(st, { cang_ay: luat.tin_tam_linh_cang_khi_ngay_xau * k / 2 });
        st.nhatKy.unshift('Ngày bạn chọn bị coi là chưa thuận theo lịch âm: bên tin sẽ lấn cấn (người không tin thì không sao).');
      }
      st.ngay_sub = 'ngan_sach';
      if (st.xemNgay && G.thoaDK(st, ['tuoi_khong_on'])) G.mo(st, 'tuoi_xung');
    }), { id: `ngay-${i}` }));
}

function uocTinh(s, mau) {
  let t = 0, du = true;
  for (const [loai, [nid, gid]] of Object.entries(mau.gom)) {
    t += G.giaGoi(s, nid, gid);
    if (loai === 'tiec' && G.nccBy(nid).suc_chua < s.khach) du = false;
  }
  return { tong: G.lamTron(t, 1), du };
}

function keHoach() {
  const s = store.s;
  const sub = s.ngay_sub || 'khu';
  const dau = h('ol', { cls: 'cac-buoc' }, SUB.map(([id, ten]) => h('li', { cls: id === sub ? 'hien-tai' : '' }, ten)));
  const out = [khung('Chương 3. Hai họ và kế hoạch', dau)];
  if (sub === 'khu') {
    out.push(khung('Cưới ở đâu?', h('p', {}, 'Hai nhà bàn nhau. Mỗi nơi có nhà cung cấp và mức giá khác nhau.'),
      h('div', { cls: 'luoi' },
        the(h('h3', {}, 'Thành phố'), h('p', {}, 'Nhà hàng hoặc sân vườn, tiện cho bạn bè đồng nghiệp.'), nut('Cưới ở thành phố', lam((st) => { st.khu = 'tp'; st.ngay_sub = 'khach'; }), { id: 'khu-tp' })),
        the(h('h3', {}, 'Ở quê'), h('p', {}, 'Dựng rạp nhà, họ hàng đông, ấm cúng, giá dễ chịu hơn.'), nut('Cưới ở quê', lam((st) => { st.khu = 'que'; st.ngay_sub = 'khach'; }), { id: 'khu-que' })))));
  } else if (sub === 'khach') {
    out.push(khung('Mời bao nhiêu khách?', h('p', {}, 'Mỗi bàn mười khách. Khách càng đông thì càng tốn, mà hai họ cũng khó từ chối.'),
      h('div', { cls: 'hang' }, D.ch.khach.map((k) => nut(k.nhan, lam((st) => {
        st.khach = k.so; st.ngay_sub = 'ngay';
        if (k.so <= 80 && !st.seen.muon_400) G.mo(st, 'muon_400');
      }), { id: `khach-${k.so}` }))),
      h('hr'), h('p', {}, 'Hoặc bạn chọn cách nhẹ nhất:'),
      nut('Chỉ đăng ký kết hôn và một bữa cơm gia đình', lam((st) => { st.toiGian = true; st.khach = 12; st.scene = { id: 'toi_gian' }; }), { id: 'toi-gian' })));
  } else if (sub === 'ngay') {
    const thay = s.thayDaThay;
    const ds = G.ungVien(s);
    out.push(khung('Xem tuổi, chọn ngày',
      s.xemNgay ? panelTuoi(s) : ghi('Bạn đã tắt phần xem tuổi, xem ngày: hai họ trong game cũng không nhắc tới. Ngày chỉ khác nhau ở giá.'),
      s.xemNgay ? the(h('h3', {}, 'Nhờ thầy xem ngày'), h('p', {}, `Thầy xem kỹ hơn, kèm giờ hoàng đạo cho từng ngày (phí ${f(D.ch.thay_xem_ngay_phi)} tiền trong game). Ứng dụng trên điện thoại thì miễn phí và gọn hơn.`),
        thay ? ghi('Bạn đã nhờ thầy: mỗi ngày dưới đây có thêm giờ hoàng đạo.') : nut('Nhờ thầy xem', lam((st) => { G.ap(st, { tien: -D.ch.thay_xem_ngay_phi }); st.thayDaThay = true; }), { id: 'nho-thay', tat: s.tien < D.ch.thay_xem_ngay_phi })) : null,
      h('p', {}, 'Mỗi tuần mình chọn ra một ngày để bạn cân nhắc, trong khoảng ba đến sáu tháng tới.'),
      h('div', { cls: 'luoi' }, ds.map((u, i) => cardNgay(s, u, i, thay)))));
  } else if (sub === 'ngan_sach') {
    const mau = D.ch.tiec_mau.map((m) => ({ m, ...uocTinh(s, m) }));
    const re = Math.min(...mau.filter((x) => x.du).map((x) => x.tong), Infinity);
    const goiY = Number.isFinite(re) ? Math.ceil(re * 1.15) : 100;
    const inp = h('input', { type: 'number', id: 'ngan-sach', min: 10, max: 2000, value: s.nganSach || goiY, 'aria-label': 'Ngân sách (triệu đồng)' });
    out.push(khung('Ngân sách',
      h('p', {}, `Ngày cưới: ${G.ngayVN(s.ngayCuoi)}${s.xemNgay ? ` (âm lịch ${lichAm(s.ngayCuoi)})` : ''}. Khoảng ${s.khach} khách, ${G.soBan(s)} bàn, cưới ở ${G.khuVuc(s)}.`),
      h('p', {}, 'Giá tham khảo cho ba kiểu tiệc nhanh với số khách và ngày bạn chọn (số tạm của game, gồm ảnh, trang phục, nhạc tuỳ mẫu):'),
      h('ul', {}, mau.map((x) => h('li', {}, `${x.m.ten}: khoảng ${f(x.tong)}${x.du ? '' : ' (không đủ chỗ cho số khách này)'}`))),
      ghi(`Gợi ý ngân sách: ${f(goiY)} (kiểu tiệc nhanh rẻ nhất cộng khoảng 15% dự phòng).`),
      h('label', {}, 'Ngân sách của bạn (triệu đồng)', inp),
      nut('Chốt kế hoạch', lam((st) => { st.nganSach = Math.max(10, Number(inp.value) || goiY); st.daChotKH = true; st.ch = 4; st.scene = { id: 'ncc', tab: 'nhanh' }; st.nhatKy.unshift('Kế hoạch được chốt, sang bước chọn nhà cung cấp.'); }), { id: 'chot-ke-hoach', cls: 'chinh' }),
      nut('Chọn lại ngày', lam((st) => { st.ngay_sub = 'ngay'; st.ngayCuoi = null; }), { id: 'chon-lai-ngay' })));
  }
  return h('div', {}, ...out);
}

/* ---------- Chương 4 ---------- */
function thongTinNcc(s, n, loai) {
  const da = s.hd[loai];
  const phiDa = s.daHoi[n.id];
  return the(h('h3', {}, n.ten), h('p', {}, n.phong_cach),
    h('p', { cls: 'diem' }, `Chất lượng ${n.diem.chat_luong}/5 · Đúng hẹn ${n.diem.dung_hen}/5 · Linh hoạt ${n.diem.linh_hoat}/5 · Rõ chi phí ${n.diem.ro_chi_phi}/5 (điểm của game)`),
    h('p', {}, `Điểm mạnh: ${n.manh.join('; ')}. Điểm yếu: ${n.yeu.join('; ')}.`),
    n.suc_chua ? ghi(`Sức chứa tối đa: ${n.suc_chua} khách.`) : null,
    phiDa ? h('p', { cls: 'ghi canh-bao' }, `Cặp đã dùng kể lại: ${n.yeu_an.mo}`) : nut('Hỏi cặp đã dùng (một buổi)', lam((st) => { st.daHoi[n.id] = true; G.dungBuoi(st, 1); }), { id: `hoi-${n.id}`, cls: 'nho' }),
    h('div', { cls: 'hang goi' }, n.goi.map((g) => {
      const gia = G.giaGoi(s, n.id, g.id), chon = da && da.ncc === n.id && da.goi === g.id;
      return h('button', { type: 'button', cls: 'lua' + (chon ? ' chon' : ''), 'data-act': `goi-${n.id}-${g.id}`, onclick: lam((st) => G.datGoi(st, loai, n.id, g.id)) },
        h('b', {}, `${g.ten}: ${f(gia)}`), h('small', {}, g.gom));
    })));
}

function ncc() {
  const s = store.s, sc = s.scene, tab = sc.tab || 'nhanh';
  const cacLoai = D.ncc.loai;
  const tong = G.tongHD(s), phai = G.tongPhai(s);
  const thieuBB = cacLoai.filter((l) => l.bat_buoc && !s.hd[l.id]);
  const coc = G.lamTron(phai * D.ch.moc_dong_tien[0].ty_le, 1);
  const tabs = h('div', { cls: 'hang' },
    nut('Dựng tiệc nhanh', lam((st) => { st.scene.tab = 'nhanh'; }), { id: 'tab-nhanh', cls: tab === 'nhanh' ? 'chon' : '' }),
    nut('Gói sẵn từng hạng mục', lam((st) => { st.scene.tab = 'goi'; }), { id: 'tab-goi', cls: tab === 'goi' ? 'chon' : '' }));
  const nhanh = tab === 'nhanh' ? khung('Dựng tiệc nhanh',
    h('p', {}, 'Chọn một mẫu, game xếp sẵn gói gọn của các nhà cung cấp hợp với số khách và ngày bạn đã chọn. Bạn vẫn đổi được từng chỗ ở tab bên cạnh.'),
    h('div', { cls: 'luoi' }, D.ch.tiec_mau.map((m) => { const u = uocTinh(s, m); return the(h('h3', {}, m.ten), h('p', {}, m.mo_ta), h('p', {}, `Khoảng ${f(u.tong)} cho ${s.khach} khách.`), u.du ? null : ghi('Không đủ chỗ cho số khách này.'),
      nut('Dùng mẫu này', lam((st) => { st.hd = {}; for (const [loai, [nid, gid]] of Object.entries(m.gom)) G.datGoi(st, loai, nid, gid); st.khu = nid_khu(m); st.scene.tab = 'goi'; }), { id: `mau-${m.id}`, tat: !u.du })); }))) : null;
  const goi = tab === 'goi' ? cacLoai.map((l) => {
    const ds = D.ncc.nha_cung_cap.filter((n) => n.loai === l.id && (l.id !== 'tiec' || n.khu === s.khu));
    return khung(`${l.ten}${l.bat_buoc ? ' (bắt buộc)' : ' (tuỳ chọn)'}`,
      h('div', { cls: 'luoi' }, ds.map((n) => thongTinNcc(s, n, l.id))),
      !l.bat_buoc && s.hd[l.id] ? nut('Bỏ hạng mục này', lam((st) => { delete st.hd[l.id]; }), { id: `bo-${l.id}`, cls: 'nho' }) : null);
  }) : null;
  const tomTat = khung('Hợp đồng của bạn',
    Object.keys(s.hd).length ? h('ul', {}, Object.entries(s.hd).map(([l, hd]) => h('li', {}, `${cacLoai.find((x) => x.id === l).ten}: ${G.nccBy(hd.ncc).ten}, gói ${G.nccBy(hd.ncc).goi.find((g) => g.id === hd.goi).ten}, ${f(hd.gia)}`))) : h('p', {}, 'Chưa chọn hạng mục nào.'),
    h('p', {}, `Tổng giá: ${f(tong)}. Ngân sách của bạn: ${f(s.nganSach)}.`),
    thieuBB.length ? ghi(`Còn thiếu hạng mục bắt buộc: ${thieuBB.map((x) => x.ten).join(', ')}.`) : null,
    h('div', { cls: 'hang' },
      h('button', { type: 'button', cls: 'lua' + (s.ky === 'ky_quy' ? ' chon' : ''), 'data-act': 'ky-quy', onclick: lam((st) => { st.ky = 'ky_quy'; }) }, h('b', {}, 'Ký quỹ'), h('small', {}, `Tiền nằm ở bên thứ ba, trả theo mốc. Phí ${D.ch.ky_quy_phi * 100}%. Nhà cung cấp bỏ ngang thì được hoàn.`)),
      h('button', { type: 'button', cls: 'lua' + (s.ky === 'tra_thang' ? ' chon' : ''), 'data-act': 'tra-thang', onclick: lam((st) => { st.ky = 'tra_thang'; }) }, h('b', {}, 'Trả thẳng'), h('small', {}, `Giảm ${D.ch.tra_thang_giam * 100}% nhưng mất cọc nếu nhà cung cấp bỏ ngang.`))),
    h('p', {}, `Thanh toán theo ba mốc: cọc khi ký (${f(coc)}), đợt hai trước cưới 30 ngày, phần còn lại sau tiệc. Tổng phải trả: ${f(phai)}.`),
    s.tien < coc && !thieuBB.length ? ghi(`Ví hiện có ${f(s.tien)}, còn thiếu ${f(coc - s.tien)} để đóng cọc. Bấm "Nạp tiền" ở góc trên để xem cách xoay tiền (vay, xin bố mẹ, làm thêm).`) : null,
    nut('Ký hợp đồng và đóng cọc', lam((st) => {
      if (G.tongPhai(st) > st.nganSach && !st.seen.vuot_ngan_sach) { G.mo(st, 'vuot_ngan_sach'); return; }
      st.daKy = true; G.xepMoc(st);
      const c = st.moc[0]; st.tien = G.lamTron(st.tien - c.so); c.daTra = true;
      st.ch = 5; st.scene = { id: 'gom_tien' }; st.nhatKy.unshift(`Đã ký hợp đồng, đóng cọc ${f(c.so)}.`);
    }), { id: 'ky-hop-dong', cls: 'chinh', tat: thieuBB.length > 0 || s.tien < coc }));
  return h('div', {}, khung('Chương 4. Nhà cung cấp', h('p', {}, 'Các nhà cung cấp dưới đây là nhân vật hư cấu trong game, giá là số tạm của game.'), tabs), nhanh, goi, tomTat);
}
function nid_khu(m) { return m.id === 'rap_que' ? 'que' : 'tp'; }

export default { ke_hoach: keHoach, ncc };
