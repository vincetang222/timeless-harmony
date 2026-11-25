# Thử khăn nhiều lớp trên bàn tròn bằng mã (0 lượt vẽ), ngày 25/11.
# Bàn lấy từ tranh cũ "cảnh gọn" (bàn tròn phủ khăn trắng chấm đất, ghế trắng phía trước).
# Ý: mỗi điểm trên khăn được "trải phẳng" về toạ độ trên mặt phẳng bàn (X, Z; đơn vị = bán kính bàn).
#   Mặt bàn: toạ độ elip. Phần rủ: điểm ở góc θ, rủ xuống t thì là điểm vải cách tâm 1 + t·L (L = độ rủ / bán kính).
#   Nhờ vậy mỗi lớp khăn chỉ là một hình phẳng (tròn, vuông, vuông chéo góc, dải chạy bàn): phần vượt ra ngoài mép bàn
#   tự rủ xuống đúng chỗ (khăn vuông chéo góc rủ thành bốn mũi nhọn). Mỗi lớp có chất vải riêng; nếp vải và bóng lấy từ tranh.
# Chạy: python3 khan_lop.py   → khan-lop.jpg. Đầu vào mặc định: mau/ban-tron-gon.webp (bàn cắt sẵn từ ảnh gốc 2736×1520 của cảnh gọn,
#   không nén mất dữ liệu). Mọi số đo, danh sách mảnh là của riêng tấm này; bàn vẽ mới (T8, T9) không có ghế dính liền nên không cần.
import sys, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from scipy import ndimage as nd
from scipy.interpolate import griddata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hoa_van import p_ren, p_kimsa, p_gam, p_hoa, p_tron, mau

DAY = os.path.dirname(os.path.abspath(__file__))
NGUON = sys.argv[1] if len(sys.argv) > 1 else os.path.join(DAY, 'mau', 'ban-tron-gon.webp')
src = Image.open(NGUON).convert('RGB')
W0, H0 = src.size
if (W0, H0) != (834, 440):   # ảnh cảnh đầy đủ 2736×1520 thì cắt bàn bên phải; mọi số đo dưới đây là trên ảnh cắt 834×440
    src = src.crop((int(W0 * 0.655), int(H0 * 0.70), int(W0 * 0.96), int(H0 * 0.99)))
a = np.asarray(src).astype(np.float32)
H, W = a.shape[:2]

# ---------- 1. Mặt nạ khăn: vùng sáng bị nét vẽ chia thành mảnh; chọn mảnh là vải ----------
r, g, b = a[..., 0], a[..., 1], a[..., 2]; lum = 0.299 * r + 0.587 * g + 0.114 * b
sat = (a.max(2) - a.min(2)) / np.maximum(a.max(2), 1)
net = (lum - nd.gaussian_filter(lum, 2.5)) < -9                       # nét mảnh (viền ghế, viền đĩa, nếp vải)
lab, n = nd.label(((lum > 140) & (sat < 0.25) & (g - np.maximum(r, b) < 4)) & ~nd.binary_dilation(net))
idx = np.arange(1, n + 1); cy_, cx_ = np.array(nd.center_of_mass(np.ones_like(lab), lab, idx)).T
sz = nd.sum(np.ones_like(lab), lab, idx)
CX, CY, A, B = 385.0, 192.0, 247.0, 64.0          # elip mặt bàn (đo trên ảnh cắt)
A2, B2, DH = 266.0, 80.0, 135.0                   # elip gấu khăn ở chân, độ cao phần rủ trên ảnh
yy, xx = np.mgrid[:H, :W].astype(np.float32)
o_mat = ((xx - CX) / A) ** 2 + ((yy - CY) / B) ** 2 <= 1
chinh = lab[int(CY), int(CX)]                     # mảnh lớn nhất: mặt bàn và phần rủ
# Ghế: mảnh nằm trong hộp ghế là đệm, nan ghế; khe giữa nan là vải. Phân biệt bằng vị trí: khe nằm giữa hai nét dọc của lưng ghế,
# đệm nằm ngang ở tầm ngồi. Danh sách mảnh do người soát chọn một lần trên ảnh nhãn (giống khoanh tay đa giác khăn bàn dài).
GHE_HOP = [(140, 175, 292, 440), (393, 188, 537, 440), (0, 90, 140, 380), (608, 95, 770, 430)]
trong_ghe = np.zeros((H, W), bool)
for x0, y0, x1, y1 in GHE_HOP: trong_ghe[y0:y1, x0:x1] = True
dem = np.zeros((H, W), bool)                      # đệm ghế: mảnh sáng, ngang, ở tầm ngồi trong hộp ghế
chon = [chinh]
for i in range(1, n + 1):
    if i == chinh or sz[i - 1] < 30: continue
    x, y = cx_[i - 1], cy_[i - 1]
    m_i = lab == i
    if not (118 < x < 680 and 120 < y < 395): continue
    ys_, xs_ = np.nonzero(m_i); w_, h_ = np.ptp(xs_) + 1, np.ptp(ys_) + 1
    in_ghe = any(x0 <= x < x1 and y0 <= y < y1 for x0, y0, x1, y1 in GHE_HOP)
    am = (r - b)[m_i].mean()
    if in_ghe and w_ > 1.3 * h_ and am > 28 and sz[i - 1] > 150 and 215 < y < 330:   # mảng ngang, màu kem ấm, ở tầm ngồi: đệm
        dem |= m_i; continue
    if y < 200: continue                                                 # trên mép sau bàn: ghế phía sau, không phải khăn
    if in_ghe and w_ <= 1.6 * h_ and h_ < 12: continue                    # mẩu nhỏ trên khung ghế
    if not in_ghe and o_mat[int(y), int(x)]: continue                    # đĩa, ly trên mặt bàn
    chon.append(i)
M0 = np.isin(lab, chon)
D = nd.binary_dilation(M0, iterations=3)
M = M0 | (net & D & ~trong_ghe & ~o_mat & (yy > 200))                # nếp vải ở phần rủ cũng là vải
nau = (r - b) > 30                                                    # viền ghế vẽ màu nâu; nếp vải màu xám
khe = nd.binary_dilation(M0, iterations=2) & ~nd.binary_dilation(dem, iterations=2)
M = M | (trong_ghe & ~o_mat & (yy > 200) & khe & ~nau & (lum > 120))   # nếp vải xám lọt giữa chân ghế, nan ghế
M = (M | (nd.binary_closing(M, iterations=2) & ~trong_ghe & ~o_mat)) & (a.min(2) > 60)
MN = np.asarray(Image.fromarray((M * 255).astype('uint8')).filter(ImageFilter.GaussianBlur(0.7))).astype(np.float32) / 255
MD = np.asarray(Image.fromarray((nd.binary_dilation(dem, iterations=1) * 255).astype('uint8')).filter(ImageFilter.GaussianBlur(0.7))).astype(np.float32) / 255

# ---------- 2. Trải phẳng: mỗi điểm ảnh → (X, Z) trên mặt phẳng bàn ----------
L_RU = 0.84                                        # độ rủ chấm đất / bán kính bàn (bàn cao 0,76 m, bán kính 0,9 m)
th = np.linspace(-np.pi / 2, np.pi / 2, 721); tt = np.linspace(0, 1.06, 160)
TH, TT = np.meshgrid(th, tt)
FX = CX + (A + (A2 - A) * TT) * np.sin(TH); FY = CY + (B + (B2 - B) * TT) * np.cos(TH) + TT * DH


def trai(px, py):
    X = (px - CX) / A; Z = (py - CY) / B; tren = X ** 2 + Z ** 2 <= 1
    q = np.stack([px[~tren], py[~tren]], -1)
    th_ = griddata((FX.ravel(), FY.ravel()), TH.ravel(), q, 'linear'); t_ = griddata((FX.ravel(), FY.ravel()), TT.ravel(), q, 'linear')
    bad = np.isnan(th_)
    if bad.any():
        th_[bad] = griddata((FX.ravel(), FY.ravel()), TH.ravel(), q[bad], 'nearest'); t_[bad] = griddata((FX.ravel(), FY.ravel()), TT.ravel(), q[bad], 'nearest')
    rho = 1 + np.clip(t_, 0, None) * L_RU
    X = X.copy(); Z = Z.copy(); X[~tren] = rho * np.sin(th_); Z[~tren] = rho * np.cos(th_)
    return X, Z, tren


ys, xs = np.nonzero((MN > 0.004) | (MD > 0.004))
SS = 2; off = (np.arange(SS) + 0.5) / SS - 0.5
MAU_MAU = [trai(xs + ox, ys + oy) for oy in off for ox in off]
px0 = a[ys, xs]; mk = MN[ys, xs][:, None]; md = MD[ys, xs][:, None]
GOC = np.percentile(a[M & (lum > np.percentile(lum[M], 60))], 75, axis=0)
GOC_D = np.percentile(a[dem], 80, axis=0) if dem.any() else GOC
R_M = 0.9                                          # bán kính bàn (m) để đổi sang mét cho hoạ tiết


# ---------- 3. Các lớp ----------
def tron_hinh(rho0):   return lambda X, Z, tren: rho0 - np.hypot(X, Z)                    # khăn tròn (rho0 > 1 thì rủ)
def vuong_cheo(s):     return lambda X, Z, tren: s - (np.abs(X) + np.abs(Z))              # vuông chéo góc: mũi ở trước, sau, hai bên
def vuong(s):          return lambda X, Z, tren: s - np.maximum(np.abs(X), np.abs(Z))     # vuông thẳng: mũi ở bốn góc chéo
def chay_ban(w, dai):  return lambda X, Z, tren: np.minimum(w / 2 - np.abs(X), dai - np.abs(Z))   # dải chạy từ sau ra trước
def chay_ngang(w, dai): return lambda X, Z, tren: np.minimum(w / 2 - np.abs(Z), dai - np.abs(X))
def ca_ban(X, Z, tren): return np.full(X.shape, 9.0)


def buoc(x, a_, b_): t = np.clip((x - a_) / (b_ - a_), 0, 1); return t * t * (3 - 2 * t)


def nhuom(tong, q):
    lumt = (tong @ np.array([0.299, 0.587, 0.114], np.float32)) / 255
    return np.minimum(255, q ** (1 + (1 - lumt) * 1.6)[:, None] * tong)


def ve(lop, dem_mau=None):
    """lop: danh sách (hình, chất vải, độ đục) từ dưới lên; lớp đầu là khăn nền. dem_mau: màu đệm ghế."""
    q = np.minimum(1.06, px0 / GOC)
    out = 0
    for X, Z, tren in MAU_MAU:
        col = None
        for k, (hinh, chat, duc) in enumerate(lop):
            f = hinh(X, Z, tren)
            ton, lap = chat(Z * R_M, X * R_M)
            c = nhuom(ton, q)
            if np.any(lap): c = np.minimum(255, c + np.asarray(lap)[:, None] * 255 * np.clip(q.mean(1, keepdims=True), 0, 1))
            if col is None: col = c; continue
            # bóng của lớp trên đổ xuống lớp dưới ngay ngoài mép (phần rủ đậm hơn mặt bàn)
            ngoai = np.clip(1 + f / 0.06, 0, 1) * (f < 0)
            col = col * (1 - ngoai * np.where(tren, 0.10, 0.30))[:, None]
            trong = buoc(f, -0.004, 0.006)[:, None] * duc
            vien = 1 - 0.14 * (np.clip(1 - f / 0.012, 0, 1) * (f > 0))[:, None]      # đường viền gấu
            col = col * (1 - trong) + c * vien * trong
        out = out + col
    out = out / len(MAU_MAU)
    res = a.copy()
    res[ys, xs] = px0 * (1 - mk) + out * mk
    if dem_mau is not None:
        qd = np.minimum(1.06, px0 / GOC_D)
        cd = nhuom(np.broadcast_to(mau(*dem_mau), px0.shape).copy(), qd)
        res[ys, xs] = res[ys, xs] * (1 - md) + cd * md
    return Image.fromarray(np.clip(res, 0, 255).astype('uint8'))


def tron_(c): return lambda u, v: p_tron(u, v, c)


TRANG = tron_((248, 246, 238))
MAU_LOP = [
    ('Gốc: một lớp khăn trắng', None, None),
    ('Nền xanh xô thơm + khăn phủ vuông chéo góc bằng ren', [(ca_ban, tron_((150, 170, 140)), 1), (vuong_cheo(1.42), lambda u, v: p_ren(u, v, (238, 234, 222), (254, 253, 250)), 1)], (150, 170, 140)),
    ('Nền đỏ + khăn phủ vuông gấm vàng (kiểu sảnh tiệc)', [(ca_ban, tron_((150, 30, 36)), 1), (vuong(1.12), lambda u, v: p_gam(u, v), 1)], (196, 150, 70)),
    ('Nền hồng phấn + khăn phủ tròn ngắn kim sa', [(ca_ban, tron_((226, 182, 178)), 1), (tron_hinh(1 + 0.42 * L_RU), lambda u, v: p_kimsa(u, v, (214, 186, 140)), 1)], (226, 182, 178)),
    ('Ba lớp: nền trắng + vuông hồng đất + chạy bàn nhung', [(ca_ban, TRANG, 1), (vuong_cheo(1.38), tron_((192, 128, 112)), 1), (chay_ban(0.34, 1 + 0.5 * L_RU), tron_((26, 84, 66)), 1)], (26, 84, 66)),
    ('Nền vàng bơ + voan trắng mỏng phủ chấm đất', [(ca_ban, tron_((236, 206, 120)), 1), (tron_hinh(1 + 0.97 * L_RU), tron_((252, 252, 250)), 0.5)], (236, 206, 120)),
    ('Nền chàm + phủ tròn hoa nhí + chạy bàn chữ thập', [(ca_ban, tron_((40, 56, 104)), 1), (tron_hinh(1 + 0.3 * L_RU), lambda u, v: p_hoa(u, v, (244, 238, 226), (40, 56, 104)), 1),
                                                                 (chay_ngang(0.24, 1 + 0.55 * L_RU), tron_((200, 160, 84)), 1), (chay_ban(0.24, 1 + 0.55 * L_RU), tron_((200, 160, 84)), 1)], (200, 160, 84)),
    ('Nền xanh than + vuông chéo góc bạc + dải chạy bàn ngang', [(ca_ban, tron_((34, 44, 70)), 1), (vuong_cheo(1.4), lambda u, v: p_kimsa(u, v, (200, 204, 210)), 1), (chay_ngang(0.30, 1 + 0.6 * L_RU), tron_((240, 236, 226)), 1)], (200, 204, 210)),
]

if __name__ == '__main__':
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 22)
    SC = 0.86; tw, th_ = int(W * SC), int(H * SC)
    G = Image.new('RGB', (tw * 2 + 30, (th_ + 40) * 4 + 20), (236, 240, 228)); d = ImageDraw.Draw(G)
    for i, (ten, lop, dm) in enumerate(MAU_LOP):
        im = Image.fromarray(a.astype('uint8')) if lop is None else ve(lop, dm)
        x0 = 10 + (i % 2) * (tw + 10); y0 = 10 + (i // 2) * (th_ + 40)
        G.paste(im.resize((tw, th_), Image.LANCZOS), (x0, y0 + 34)); d.text((x0 + 4, y0 + 5), f'{i + 1}. {ten}', fill=(18, 38, 28), font=font)
    G.save('khan-lop.jpg', quality=86)
    print('xong', G.size, 'mảnh vải', len(chon), 'GOC', GOC.round(), 'GOC đệm', GOC_D.round())
