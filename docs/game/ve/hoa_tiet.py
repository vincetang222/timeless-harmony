# Thử phủ hoạ tiết lên khăn chạy bàn bằng mã (0 lượt vẽ), ngày 25/11.
# Chạy trong thư mục có ban-dai.png (ảnh mô hình trả về ở tấm 3), cạnh trang_tri.py:   python3 hoa_tiet.py
# Ý: mỗi điểm ảnh trên khăn có toạ độ vải (u dọc khăn, v ngang khăn, đơn vị mét) theo phối cảnh của chính tấm vẽ;
# hoạ tiết sinh theo (u, v) thành "tông từng điểm", rồi nhuộm bằng đúng công thức đang dùng trong game: tông × (điểm/màu gốc)^γ,
# nên nếp vải, bóng đổ, ly trên khăn vẫn giữ nguyên. Số đo hình học là số đo tay trên tấm bàn dài (1635×814 sau khi tách nền).
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
if not os.path.exists('ban-rgba.png'):
    import trang_tri as tr
    _b = tr.tach('ban-dai.png', bo_xam_xanh=True); _b.save('ban-rgba.png')
    KHAN = [[(212, 93), (400, 80), (600, 131), (900, 206), (1100, 261), (1304, 318), (1304, 528), (1078, 562), (1070, 376), (900, 307), (700, 247), (550, 204), (400, 156), (212, 113)],
            [(231, 183), (302, 183), (305, 324), (233, 324)]]   # như trong trang_tri.py
    tr.mat_na_vung(_b, KHAN).save('ban-khan.png')

im = Image.open('ban-rgba.png'); A = np.asarray(im).astype(np.float32)
MN = np.asarray(Image.open('ban-khan.png')).astype(np.float32) / 255
DIA = [(578, 121, 704, 153), (760, 169, 898, 207), (1012, 229, 1158, 272), (1162, 264, 1318, 312)]   # đĩa ở hàng sau đè lên mép khăn
_d = Image.new('L', (MN.shape[1], MN.shape[0]), 0); _g = ImageDraw.Draw(_d)
for e in DIA: _g.ellipse(e, fill=255)
MN = MN * (1 - np.asarray(_d.filter(ImageFilter.GaussianBlur(1.2))).astype(np.float32) / 255)
H, W = MN.shape
GOC = np.array([246, 234, 204], np.float32)
RONG = 0.42           # bề ngang khăn chạy bàn (m)
DAI = 3.4             # chiều dài phần nằm trên mặt bàn (m), ước theo bàn 12 ghế

# ---- hình học, đo trên tấm vẽ (1635×814) ----
B1, B2 = np.array([400., 80.]), np.array([1298., 318.])     # mép sau
F1, F2 = np.array([400., 156.]), np.array([1070., 376.])    # mép trước
D = B2 - F2                                                  # hướng ngang khăn (nếp gấp đầu gần)


def cat(p, d, a, b):
    """giao của đường p + t·d với đường qua a, b → trả điểm (mảng N×2)"""
    e = b - a; den = d[0] * e[1] - d[1] * e[0]
    t = ((a[0] - p[..., 0]) * e[1] - (a[1] - p[..., 1]) * e[0]) / den
    return p + t[..., None] * d


# điểm tụ của hai mép
def giao(a1, a2, b1, b2):
    return cat(a1[None], a2 - a1, b1, b2)[0]


V = giao(B1, B2, F1, F2)
M_GAN = (B2 + F2) / 2
s_gan = np.linalg.norm(M_GAN - V)
M_XA = cat(np.array([[212., 102.]]), D, V, M_GAN)[0]; s_xa = np.linalg.norm(M_XA - V)


def uv_mat(p):
    b = cat(p, D, B1, B2); f = cat(p, D, F1, F2); c = cat(p, D, V, M_GAN)
    v = ((p - b) * (f - b)).sum(-1) / ((f - b) ** 2).sum(-1)
    s = np.linalg.norm(c - V, axis=-1)
    u = DAI * (s_gan / s - 1) / (s_gan / s_xa - 1)
    return u, v * RONG


def nep_y(x):  # đường gấp ở đầu gần
    return F2[1] + (x - F2[0]) * (B2[1] - F2[1]) / (B2[0] - F2[0])


def uv(px, py):
    p = np.stack([px, py], -1)
    u, v = uv_mat(p)
    # phần rủ đầu gần: mặt gần đứng; ngang theo x, dọc theo khoảng cách dưới nếp gấp
    roi = (px > F2[0] - 12) & (px < B2[0] + 12) & (py > nep_y(px))
    xl = F2[0] + (py - F2[1]) * (8 / 174); xr = B2[0] - (py - B2[1]) * (3 / 197)
    vr = (1 - (px - xl) / (xr - xl)) * RONG
    ur = -(py - nep_y(px)) / (228 / RONG)
    u = np.where(roi, ur, u); v = np.where(roi, vr, v)
    # phần rủ đầu xa (khuất sau ghế)
    xa = (px > 225) & (px < 312) & (py > 178)
    u = np.where(xa, DAI + (py - 183) / (74 / RONG), u); v = np.where(xa, (px - 231) / 74 * RONG, v)
    return u, v


# ---- hoạ tiết: trả (tông RGB 0..255, độ lấp lánh 0..1) theo (u, v) mét ----
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


def p_hoa(u, v):  # hoa nhí in khuôn, xếp so le
    c = 0.06; ui = np.floor(u / c); vv = v / c + 0.5 * (ui % 2); vi = np.floor(vv)
    du = (fr(u / c) - 0.5); dv = (vv - vi - 0.5)
    r = np.hypot(du, dv); th = np.arctan2(dv, du) + hx(ui, vi) * 6
    canh = r < 0.30 * (0.55 + 0.45 * np.abs(np.cos(2.5 * th)))
    nhuy = r < 0.07
    la = (np.abs(du - 0.32) < 0.09) & (np.abs(dv + 0.28) < 0.05)
    t = np.broadcast_to(mau(244, 236, 218), u.shape + (3,)).copy()
    t[canh] = mau(52, 70, 128); t[la] = mau(108, 134, 88); t[nhuy] = mau(214, 170, 72)
    return t, 0


def p_ren(u, v):  # ren trắng phủ trên nền hồng đất
    c = 0.05; ui = np.floor(u / c); vv = v / c + 0.5 * (ui % 2); vi = np.floor(vv)
    du = fr(u / c) - 0.5; dv = vv - vi - 0.5; r = np.hypot(du, dv)
    vong = np.exp(-((r - 0.34) / 0.045) ** 2) + np.exp(-((r - 0.16) / 0.035) ** 2)
    th = np.arctan2(dv, du); canh = (r < 0.27) & (np.cos(6 * th) > 0.3) & (r > 0.2)
    luoi = (np.abs(np.sin(u / 0.004 * np.pi)) < 0.25) | (np.abs(np.sin(v / 0.004 * np.pi)) < 0.25)
    k = np.clip(vong * 0.95 + canh * 0.9 + luoi * 0.32, 0, 0.95)
    return tron(np.broadcast_to(mau(196, 140, 134), u.shape + (3,)), mau(252, 250, 246), k), 0


def p_kimsa(u, v):  # kim sa vàng champagne: mỗi hạt bắt sáng khác nhau, vài hạt loé
    c = 0.006; ui = np.floor(u / c); vi = np.floor(v / c + 0.5 * (ui % 2)); h = hx(ui, vi)
    t = mau(214, 182, 120)[None] * (0.62 + 0.62 * h)[..., None]
    return t, (h > 0.965).astype(np.float32)


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


MAU = [('Kẻ ca rô', p_caro), ('Sọc', p_soc), ('Hoa nhí in khuôn', p_hoa), ('Ren trắng trên nền hồng', p_ren),
       ('Kim sa vàng', p_kimsa), ('Nhuộm loang', p_loang), ('Hoa văn hình học, nền chàm', p_thocam), ('Nhung xanh ngọc', p_nhung)]

# ---- chạy ----
ys, xs = np.nonzero(MN > 0.004)
SS = 4; off = (np.arange(SS) + 0.5) / SS - 0.5
px0 = A[ys, xs, :3]; m = MN[ys, xs][:, None]
UV = [uv(xs + ox, ys + oy) for oy in off for ox in off]


def nhuom(fn, ten):
    tong = 0; lap = 0
    for u, v in UV:
        t, s = fn(u, v); tong = tong + t; lap = lap + s
    tong = tong / len(UV); lap = lap / len(UV)
    lum = (tong @ np.array([0.299, 0.587, 0.114], np.float32)) / 255
    gam = (1 + (1 - lum) * 1.6)[:, None]
    q = np.minimum(1.06, px0 / GOC)
    moi = np.minimum(255, q ** gam * tong)
    if fn is p_nhung:   # ánh nhung: chỗ sáng của nếp vải ngả sang màu nhạt hơn
        sang = np.clip((q.mean(1, keepdims=True) - 0.93) / 0.12, 0, 1)
        moi = moi + (mau(120, 190, 160) - moi) * sang * 0.55
    if np.any(lap):
        moi = np.minimum(255, moi + (lap[:, None] * 255 * np.clip(q.mean(1, keepdims=True), 0, 1)))
    out = A.copy(); out[ys, xs, :3] = px0 * (1 - m) + moi * m
    return Image.fromarray(out.astype('uint8'), 'RGBA')


font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 26)   # phông có dấu tiếng Việt
CROP = (150, 30, 1350, 600); SC = 0.62
tw, th = int((CROP[2] - CROP[0]) * SC), int((CROP[3] - CROP[1]) * SC)
G = Image.new('RGB', (tw * 2 + 30, (th + 46) * 4 + 20), (236, 240, 228))
for i, (ten, fn) in enumerate(MAU):
    r = nhuom(fn, ten); bg = Image.new('RGBA', r.size, (226, 230, 216, 255)); bg.alpha_composite(r)
    t = bg.convert('RGB').crop(CROP).resize((tw, th), Image.LANCZOS)
    x0 = 10 + (i % 2) * (tw + 10); y0 = 10 + (i // 2) * (th + 46)
    G.paste(t, (x0, y0 + 40)); ImageDraw.Draw(G).text((x0 + 4, y0 + 6), f'{i + 1}. {ten}', fill=(18, 38, 28), font=font)
G.save('khan-hoatiet.jpg', quality=86)
print('xong', G.size)
