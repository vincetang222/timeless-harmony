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


from hoa_van import *   # hoạ tiết dùng chung

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
