# Hoạ tiết vải sinh bằng mã, dùng chung cho hoa_tiet.py (khăn chạy bàn) và khan_lop.py (khăn nhiều lớp).
# Mỗi hàm nhận toạ độ trên vải (u, v, đơn vị mét) và trả (tông RGB 0..255 từng điểm, độ lấp lánh 0..1).
import numpy as np


def hx(*a):
    h = np.zeros_like(a[0], dtype=np.float64)
    for i, x in enumerate(a): h = h + x * (12.9898 + 61.7 * i)
    return np.modf(np.abs(np.sin(h) * 43758.5453))[0]


def fr(x): return x - np.floor(x)


def mau(*c): return np.array(c, np.float32)


def tron(a, b, t): return a + (b - a) * t[..., None]


def bang(x, w):  # dải lặp: 1 trong dải bề rộng w (tỉ lệ chu kỳ)
    f = fr(x); return (f < w).astype(np.float32)


def p_caro(u, v):
    c = 0.03; su = bang(u / c, 0.5); sv = bang(v / c, 0.5); k = (su + sv) / 2
    return tron(np.broadcast_to(mau(250, 248, 242), u.shape + (3,)), mau(86, 128, 176), k), 0


def p_soc(u, v):
    c = 0.07; f = fr(v / c + 0.25)
    k = ((f < 0.42) * 1.0 + ((f > 0.55) & (f < 0.6)) * 1.0).astype(np.float32)
    return tron(np.broadcast_to(mau(246, 238, 222), u.shape + (3,)), mau(196, 104, 72), k), 0


def p_hoa(u, v, nen=(244, 236, 218), hoa=(52, 70, 128)):  # hoa nhí in khuôn, xếp so le
    c = 0.06; ui = np.floor(u / c); vv = v / c + 0.5 * (ui % 2); vi = np.floor(vv)
    du = (fr(u / c) - 0.5); dv = (vv - vi - 0.5)
    r = np.hypot(du, dv); th = np.arctan2(dv, du) + hx(ui, vi) * 6
    canh = r < 0.30 * (0.55 + 0.45 * np.abs(np.cos(2.5 * th)))
    nhuy = r < 0.07
    la = (np.abs(du - 0.32) < 0.09) & (np.abs(dv + 0.28) < 0.05)
    t = np.broadcast_to(mau(*nen), u.shape + (3,)).copy()
    t[canh] = mau(*hoa); t[la] = mau(108, 134, 88); t[nhuy] = mau(214, 170, 72)
    return t, 0


def p_ren(u, v, nen=(196, 140, 134), ren=(252, 250, 246)):  # ren trắng phủ trên nền hồng đất
    c = 0.05; ui = np.floor(u / c); vv = v / c + 0.5 * (ui % 2); vi = np.floor(vv)
    du = fr(u / c) - 0.5; dv = vv - vi - 0.5; r = np.hypot(du, dv)
    vong = np.exp(-((r - 0.34) / 0.045) ** 2) + np.exp(-((r - 0.16) / 0.035) ** 2)
    th = np.arctan2(dv, du); canh = (r < 0.27) & (np.cos(6 * th) > 0.3) & (r > 0.2)
    luoi = (np.abs(np.sin(u / 0.004 * np.pi)) < 0.25) | (np.abs(np.sin(v / 0.004 * np.pi)) < 0.25)
    k = np.clip(vong * 0.95 + canh * 0.9 + luoi * 0.32, 0, 0.95)
    return tron(np.broadcast_to(mau(*nen), u.shape + (3,)), mau(*ren), k), 0


def p_kimsa(u, v, goc=(214, 182, 120)):  # kim sa vàng champagne: mỗi hạt bắt sáng khác nhau, vài hạt loé
    c = 0.006; ui = np.floor(u / c); vv = v / c + 0.5 * (ui % 2); vi = np.floor(vv); h = hx(ui, vi)
    du = fr(u / c) - 0.5; dv = vv - vi - 0.5; r = np.hypot(du, dv)
    hat = np.clip((0.5 - r) / 0.08, 0, 1)                     # hạt tròn, kẽ giữa các hạt tối hơn (nhìn gần mới thấy)
    t = mau(*goc)[None] * ((0.62 + 0.62 * h) * (0.55 + 0.45 * hat))[..., None]
    return t, ((h > 0.965) * hat * (r < 0.25)).astype(np.float32)


def p_loang(u, v):  # nhuộm loang: đậm ở đầu rủ, nhạt dần về xa
    k = np.clip(1 - (u + 0.35) / 2.6, 0, 1) ** 1.3
    k = k * (0.9 + 0.1 * np.sin(v * 40 + u * 7))
    return tron(np.broadcast_to(mau(246, 236, 230), u.shape + (3,)), mau(150, 70, 92), k), 0


def p_thocam(u, v):  # dải hoa văn hình học (kiểu dệt thổ cẩm) chạy dọc mép, nền chàm
    t = np.broadcast_to(mau(40, 52, 92), u.shape + (3,)).copy()
    for v0 in (0.06, 0.36):
        dv = np.abs(v - v0); band = dv < 0.035
        zz = np.abs(fr(u / 0.04) - 0.5) * 0.07   # răng cưa
        thoi = band & (dv < 0.035 - zz)
        t[band] = mau(196, 62, 52); t[thoi] = mau(236, 196, 92)
        t[(dv > 0.035) & (dv < 0.042)] = mau(240, 232, 214)
    tam = (np.abs(v - 0.21) < 0.012) & (fr(u / 0.03) < 0.5)
    t[tam] = mau(232, 226, 208)
    return t, 0


def p_nhung(u, v):  # nhung xanh ngọc lục (màu đậm; ánh nhung thêm ở bước nhuộm)
    return np.broadcast_to(mau(30, 92, 74), u.shape + (3,)).copy(), 0


def p_gam(u, v, nen=(170, 120, 52), hoa=(214, 172, 92)):  # gấm hoa cùng tông: hoa văn chỉ đậm nhạt hơn nền một chút
    c = 0.11; ui = np.floor(u / c); vv = v / c + 0.5 * (ui % 2); vi = np.floor(vv)
    du = fr(u / c) - 0.5; dv = vv - vi - 0.5; r = np.hypot(du, dv); th = np.arctan2(dv, du)
    canh = r < 0.36 * (0.5 + 0.5 * np.abs(np.cos(2 * th))) ** 0.7
    vien = np.abs(r - 0.44) < 0.025
    k = np.clip(canh * 1.0 + vien * 0.8, 0, 1)
    return tron(np.broadcast_to(mau(*nen), u.shape + (3,)), mau(*hoa), k), 0


def p_tron(u, v, c=(240, 240, 240)):  # vải trơn một màu
    return np.broadcast_to(mau(*c), u.shape + (3,)).copy(), 0
