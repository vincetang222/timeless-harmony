# Xoá lông mày gốc khỏi một đầu (ảnh nguồn 1520 px ngang) và tách nét lông mày thành lớp trong suốt.
# Không dùng AI: tách điểm tối, loại tóc (khối cao hoặc lọn dốc), lấp da bằng nội suy Laplace.
import numpy as np
from PIL import Image, ImageFilter
from may_lib import luma

def dich(M, dx, dy):
    o = np.zeros_like(M); H, W = M.shape
    ys = slice(max(0, dy), min(H, H + dy)); yt = slice(max(0, -dy), min(H, H - dy))
    xs = slice(max(0, dx), min(W, W + dx)); xt = slice(max(0, -dx), min(W, W - dx))
    o[ys, xs] = M[yt, xt]; return o
def duong(goc, L):
    t = np.deg2rad(goc); return sorted(set((int(round(k * np.cos(t))), int(round(k * np.sin(t)))) for k in np.arange(-(L - 1) / 2, (L - 1) / 2 + 0.01, 0.5)))
def mo_duong(M, goc, L):  # phép mở theo một đoạn thẳng: giữ lại những gì dài ít nhất L theo hướng đó
    P = duong(goc, L); E = np.ones_like(M)
    for dx, dy in P: E &= dich(M, dx, dy)
    O = np.zeros_like(M)
    for dx, dy in P: O |= dich(E, -dx, -dy)
    return O
def gian(M, r):
    O = M.copy()
    for _ in range(r): O = O | dich(O, 1, 0) | dich(O, -1, 0) | dich(O, 0, 1) | dich(O, 0, -1)
    return O
def co(M, r): return ~gian(~M, r)
def thanh_phan(M):
    lab = np.zeros(M.shape, np.int32); n = 0; H, W = M.shape
    for y0, x0 in zip(*np.nonzero(M)):
        if lab[y0, x0]: continue
        n += 1; st = [(y0, x0)]; lab[y0, x0] = n
        while st:
            y, x = st.pop()
            for yy, xx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1), (y - 1, x - 1), (y - 1, x + 1), (y + 1, x - 1), (y + 1, x + 1)):
                if 0 <= yy < H and 0 <= xx < W and M[yy, xx] and not lab[yy, xx]: lab[yy, xx] = n; st.append((yy, xx))
    return lab, n
def lap(A, U, n=900):  # nội suy Laplace: lấp vùng U bằng màu của viền xung quanh
    A = A.copy(); K = ~U
    for c in range(A.shape[2]): A[..., c][U] = A[..., c][K].mean() if K.any() else 0
    for _ in range(n):
        P = np.pad(A, ((1, 1), (1, 1), (0, 0)), mode='edge')
        N = (P[:-2, 1:-1] + P[2:, 1:-1] + P[1:-1, :-2] + P[1:-1, 2:]) / 4
        A[U] = N[U]
    return A

THAM = {'nam': dict(manh=0.17, khoi=0.26, L=34, dy=42, dai=(-56, 78)), 'nu': dict(manh=0.15, manh13=0.055, khoi=0.2, L=30, dy=52, dai=(-56, 78), cat_tu=42, cat_den=24)}
def _loc(L, cls, k):
    return np.asarray(Image.fromarray((L * 255).clip(0, 255).astype('uint8')).filter(cls(k))).astype(float) / 255
def dong(L, k):  # phép đóng: lấp mọi nét tối hẹp hơn k điểm, giữ nguyên mảng tối lớn và bậc sáng tối của da
    return _loc(_loc(L, ImageFilter.MaxFilter, k), ImageFilter.MinFilter, k)
def hsv_(w):
    r, g, b = [w[..., i] / 255 for i in range(3)]; mx = np.maximum(np.maximum(r, g), b); mn = np.minimum(np.minimum(r, g), b); d = mx - mn + 1e-6
    h = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) * 60
    return h, (mx - mn) / (mx + 1e-6), mx
def tam_mat(a, px, py):
    """tâm mắt thật quanh tâm mảnh (px, py): trọng tâm tròng mắt (nâu, đậm màu), không lẫn với lông mày đen"""
    x0, y0 = int(px - 70), int(py - 40); w = a[y0:y0 + 100, x0:x0 + 140, :3]; L = luma(w); h, s, v = hsv_(w)
    yy, xx = np.mgrid[0:100, 0:140]
    trong = ((h < 45) | (h > 340)) & (s > 0.32) & (L > 0.1) & (L < 0.5)
    cx, cy = px, py + 4
    for _ in range(4):
        wt = trong * np.exp(-(((xx + x0 - cx) / 26) ** 2 + ((yy + y0 - cy) / 18) ** 2))
        if wt.sum() < 8: break
        cx, cy = (wt * (xx + x0)).sum() / wt.sum(), (wt * (yy + y0)).sum() / wt.sum()
    return cx, cy
def tach(a, ex, ey, g, ben, tham=None):
    """a: mảng RGBA float của cả ảnh; (ex, ey): tâm mắt thật; ben: 0 = mắt bên trái ảnh, 1 = bên phải.
    Cửa sổ từ trên trán xuống tới giữa mắt. Trả về cửa sổ và các mặt nạ."""
    T = dict(THAM[g]); T.update(tham or {})
    hw, len_, xuong = 110, 150, 6
    x0, x1, y0, y1 = int(ex - hw), int(ex + hw), int(ey - len_), int(ey + xuong)
    w = a[y0:y1, x0:x1, :3].astype(float); L = luma(w); al = a[y0:y1, x0:x1, 3] / 255
    L = np.where(al > 0.5, L, 0)
    Ld = dong(L, 31); bth = Ld - L                              # độ tối của nét hẹp so với nền quanh nó
    Ls = np.percentile(L[al > 0.9], 78)                         # độ sáng chung của da
    net = (bth > T['manh']) & (al > 0.5)                        # nét hẹp: lông mày, lọn tóc, mi mắt
    netm = (bth > T['manh'] * 0.4) & (al > 0.5)                 # cả viền mềm
    if 'manh13' in T:                                           # nét rất mảnh và nhạt (lông mày cô dâu): lọc bằng cửa sổ nhỏ để không lẫn bóng mí mắt
        b13 = dong(L, 13) - L; net |= (b13 > T['manh13']) & (al > 0.5); netm |= (b13 > T['manh13'] * 0.5) & (al > 0.5)
    khoi = (Ld < Ls - T['khoi'])                                # mảng tóc lớn
    H, W = net.shape; cy, cx = ey - y0, ex - x0
    yy, xx = np.mgrid[0:H, 0:W]
    def elip(dx, dy, rx, ry): return ((xx - cx - dx) / rx) ** 2 + ((yy - cy - dy) / ry) ** 2 < 1
    # lọn tóc: nét dốc, dài hơn bề dày lông mày
    tat = net | khoi; doc = np.zeros_like(net)
    for goc in (55, 65, 75, 90, 105, 115, 125): doc |= mo_duong(tat, goc, T['L'])
    lon = gian(doc, 2) & net
    # lọn tóc phải dính vào mảng tóc hoặc đi lên tới mép trên cửa sổ; nét dốc đứng riêng lẻ là sợi lông mày
    labl, nl = thanh_phan(lon); gk = gian(khoi, 3); lon = np.zeros_like(net)
    for i in range(1, nl + 1):
        c = labl == i
        if (c & gk).any() or c[:6].any(): lon |= c
    con = net & ~lon & ~khoi
    # tách lông mày khỏi mi mắt: cắt tại hàng ít điểm tối nhất giữa hai thứ
    if 'cat' in T: hang = int(cy - T['cat'])
    else:
        ya_, yb_ = int(cy - T.get('cat_tu', 27)), int(cy - T.get('cat_den', 14)); dem = (net & ~lon)[ya_:yb_, max(0, int(cx - 60)):int(cx + 60)].sum(axis=1).astype(float)
        dem = np.convolve(dem, np.ones(3) / 3, mode='same'); thap = np.nonzero(dem <= dem.min() + 1)[0]; hang = ya_ + int(thap[len(thap) // 2])
    con[hang:hang + 2] = False
    lab, n = thanh_phan(con)
    mat = np.zeros_like(net)
    for i in np.unique(lab[elip(0, 0, 40, 12) & (lab > 0)]): mat |= lab == i
    mat[:hang] = False
    by = -T['dy'] + T.get('by', 0); bx = T.get('bx', 0)
    trong = elip(bx, by, T.get('rx', 62), T.get('ry', 22)); bao = elip(bx, by, T.get('Rx', 98), T.get('Ry', 36)) & (yy < hang)
    out = -1 if ben == 0 else 1; ua, ub = T['dai']; u = (xx - cx) * out; bao &= (u > ua - 6) & (u < ub + 14)
    # lông mày chắc chắn: mảnh dài nằm ngang ngay trên mắt
    may = np.zeros_like(net); ung = []; nho = np.zeros_like(net)
    for i in range(1, n + 1):
        c = lab == i; sz = c.sum()
        if (c & mat).any() or sz < 6: continue
        ys, xs = np.nonzero(c); bw, bh = xs.max() - xs.min() + 1, ys.max() - ys.min() + 1
        k = (c & trong).sum()
        if k >= 0.3 * sz and bw >= 22 and bw >= 1.4 * bh and ys.max() < hang + 2 and sz >= 25: ung.append((k, i))
        elif sz < 420 and (c & bao).sum() >= 0.9 * sz and ys.max() < hang + 2: nho |= c       # mảnh nhỏ nằm trọn trong vùng lông mày
    for k, i in sorted(ung, reverse=True)[:T.get('so_manh', 3)]: may |= lab == i
    may &= bao
    if may.sum() > 40:                                           # sợi mày dựng ở đầu trong của lông mày
        ys, xs = np.nonzero(may); dau_trong = xs.max() if out < 0 else xs.min()
        xa_, xb_ = sorted((dau_trong - out * 4, dau_trong - out * 30)); vung = (xx >= xa_) & (xx <= xb_) & (yy >= ys.min() - 8) & (yy <= min(hang, ys.max() + 8))
        lab4, n4 = thanh_phan(net & ~khoi & ~mat & ~may & (yy < hang))
        for i in np.unique(lab4[vung & (lab4 > 0)]):
            c = lab4 == i
            if c.sum() < 300 and (c & vung).sum() >= 0.75 * c.sum(): nho |= c
    # phần lông mày vẽ đè lên mảng tóc (đen trên nền tóc xám): tìm trong dải kéo dài của lông mày
    tren_toc = np.zeros_like(net)
    if may.sum() > 40 and not T.get('khong_toc'):
        cols = np.nonzero(may.any(axis=0))[0]; ym = np.array([yy[:, c][may[:, c]].mean() for c in cols]); day = np.array([may[:, c].sum() for c in cols])
        p = np.polyfit(cols, ym, 1); h = np.percentile(day, 70) / 2 + 2
        xa, xb = sorted((cx + out * ua, cx + out * ub))
        for x in list(range(int(cols.max()) + 1, int(min(W - 2, xb, cols.max() + 50)))) + list(range(int(max(1, xa, cols.min() - 50)), int(cols.min()))):
            y = np.polyval(p, x); ya, yb = int(round(y - h)), int(round(y + h)) + 1
            if ya < 2 or yb > hang: continue
            tren_toc[ya:yb, x] = khoi[ya:yb, x] & (bth[ya:yb, x] > T.get('tren_toc', 0.05))
        # chỉ giữ phần dính liền với lông mày
        lab3, n3 = thanh_phan(tren_toc | may); giu = np.zeros_like(net)
        for i in np.unique(lab3[may]): giu |= lab3 == i
        tren_toc &= giu & ~may
    xoa_ = gian(may | nho, 3) & ~gian(lon, 1) & ~gian(khoi, 1)
    xoa_ &= ~gian(mat, 2); xoa_[hang + 1:] = False
    for (xa_, ya_, xb_, yb_) in T.get('ep_xoa', []): xoa_[ya_:yb_, xa_:xb_] = True
    for (xa_, ya_, xb_, yb_) in T.get('ep_giu', []): xoa_[ya_:yb_, xa_:xb_] = False; tren_toc[ya_:yb_, xa_:xb_] = False
    return dict(x0=x0, y0=y0, w=w, L=L, bth=bth, net=net, netm=netm, khoi=khoi, toc=lon | khoi, may=may, nho=nho, mat=mat, xoa=xoa_, tren_toc=tren_toc, hang=hang, bao=bao)
def _mem(M, s=1.2):
    m = np.asarray(Image.fromarray((M * 255).astype('uint8')).filter(ImageFilter.GaussianBlur(s))).astype(float) / 255
    return np.maximum(m, M * 1.0)[..., None]
def xoa(r):
    """trả về cửa sổ RGB đã xoá lông mày, lớp da đã lấp"""
    U = gian(r['netm'], 2) | gian(r['khoi'], 3) | r['xoa']
    S = lap(r['w'], U)
    kq = r['w'] * (1 - _mem(r['xoa'])) + S * _mem(r['xoa'])
    if r['tren_toc'].any():                                      # phần đè lên tóc: lấp bằng màu tóc xung quanh
        tt = gian(r['tren_toc'], 2) & r['khoi']
        biet = r['khoi'] & ~gian(r['bth'] > 0.03, 1) & ~tt
        if biet.sum() > 50:
            St = lap(r['w'], ~biet, 400); m = _mem(tt, 1.0); kq = kq * (1 - m) + St * m
    return kq, S
