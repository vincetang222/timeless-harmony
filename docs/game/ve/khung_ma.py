# Thử vẽ khung cổng kim loại đơn giản bằng mã (0 lượt), ngày 25/11: thay tấm T1 (khung lục giác trần) nếu trông đủ giống tranh vẽ tay.
# Vẽ ở 4× rồi thu nhỏ: ống kim loại = viền mực + màu nền + vệt sáng + vệt tối, đường hơi rung tay, phủ vân giấy; chân đế và bóng chạm đất.
# Đặt vào nền trống Vườn Hồ bằng đúng thước phối cảnh của game (1 m ở chân Y% = 0,307·(Y − 44)% chiều cao khung).
# Chạy: python3 khung_ma.py <nen-ho.webp 1600×889> <cong-tron.webp (hình rời cổng tròn vẽ tay)>   → khung-ma.jpg
import sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1600, 889                      # cỡ nền trống trong bản chơi (ảnh nền đọc ở phần chạy, để tệp này nhập được từ tệp khác)
X, Y = 50.3, 78.6                      # điểm neo cổng ở Vườn Hồ (% khung)
MET = 0.307 * (Y - 44) / 100 * H       # số px của 1 m ở chân cổng
S = 4                                  # vẽ ở 4×

MAU = {  # (viền mực, tối, nền, sáng)
    'đen mờ': ((22, 20, 22), (30, 29, 32), (58, 56, 60), (122, 120, 126)),
    'vàng đồng': ((104, 74, 36), (156, 116, 54), (206, 168, 92), (246, 224, 160)),
    'trắng': ((120, 112, 100), (198, 194, 186), (236, 234, 228), (255, 255, 252)),
    'gỗ': ((74, 48, 28), (128, 86, 52), (172, 124, 80), (212, 170, 120)),
}
rng = np.random.RandomState(7)


def rung(pts, bien):
    """Đường hơi rung như nét tay: chia nhỏ rồi cộng nhiễu tần số thấp (biên độ theo px ở cỡ cuối)."""
    out = []
    for (x0, y0), (x1, y1) in zip(pts[:-1], pts[1:]):
        n = max(2, int(math.hypot(x1 - x0, y1 - y0) / (6 * S)))
        for t in np.linspace(0, 1, n, endpoint=False):
            out.append((x0 + (x1 - x0) * t, y0 + (y1 - y0) * t))
    out.append(pts[-1])
    out = np.array(out); k = len(out)
    nz = np.convolve(rng.randn(k + 8), np.ones(9) / 9, 'same')[4:4 + k] * bien * S
    d = np.gradient(out, axis=0); nrm = np.stack([-d[:, 1], d[:, 0]], 1); nrm /= np.maximum(np.linalg.norm(nrm, axis=1, keepdims=True), 1e-6)
    return [tuple(p) for p in out + nrm * nz[:, None]]


def ong(d, pts, rong, mau, sang_huong=(-0.6, -0.8)):
    """Một ống kim loại: 4 nét chồng nhau. sang_huong: hướng ánh sáng (sáng ở phía trên trái)."""
    vien, toi, nen, sang = mau
    p = rung(pts, 0.35)
    d.line(p, fill=vien + (235,), width=int((rong + 1.6) * S), joint='curve')
    d.line(p, fill=nen + (255,), width=int(rong * S), joint='curve')
    q = np.array(p); dd = np.gradient(q, axis=0); nrm = np.stack([-dd[:, 1], dd[:, 0]], 1); nrm /= np.maximum(np.linalg.norm(nrm, axis=1, keepdims=True), 1e-6)
    huong = np.sign((nrm * np.array(sang_huong)).sum(1, keepdims=True) + 1e-6)
    d.line([tuple(v) for v in q + nrm * huong * rong * 0.26 * S], fill=sang + (210,), width=max(1, int(rong * 0.28 * S)), joint='curve')
    d.line([tuple(v) for v in q - nrm * huong * rong * 0.28 * S], fill=toi + (200,), width=max(1, int(rong * 0.3 * S)), joint='curve')


def khung(hinh, mau, cao_m=2.35):
    """Trả (ảnh RGBA cỡ thật, điểm neo x, y = giữa chân đế) của khung đứng ở mặt đất."""
    r_ong = 0.05 * MET                                  # ống 5 cm
    if hinh == 'lục giác':
        R = 1.45; dinh = [(R * math.cos(math.radians(a)), R * math.sin(math.radians(a)) + R * 0.866 + 0.12) for a in (0, 60, 120, 180, 240, 300, 360)]
    elif hinh == 'tròn':
        R = 1.45; dinh = [(R * math.cos(t), R * math.sin(t) + R + 0.12) for t in np.linspace(0, 2 * math.pi, 73)]   # cỡ như cổng tròn vẽ tay
    elif hinh == 'tam giác':
        dinh = [(-1.35, 0.12), (0, 2.6), (1.35, 0.12), (-1.35, 0.12)]
    elif hinh == 'vòm':          # hai cột và nửa vòng tròn
        R = 1.2; dinh = [(-R, 0.12)] + [(R * math.cos(t), 1.4 + R * math.sin(t)) for t in np.linspace(math.pi, 0, 37)] + [(R, 0.12)]
    elif hinh == 'vòm nhọn':     # vòm kiểu nhà thờ: hai cung gặp nhau ở đỉnh
        R = 1.9; c = 0.75; dinh = [(-1.15, 0.12)] + [(-1.15 + R - R * math.cos(t), 1.5 + R * math.sin(t)) for t in np.linspace(0, math.acos(c / R + 0.0), 18)]
        dinh += [(-x, y) for x, y in reversed(dinh[1:])] + [(1.15, 0.12)]
    elif hinh == 'chữ nhật':     # cột và xà, xà nhô ra hai đầu
        dinh = [(-1.2, 0.12), (-1.2, 2.45), (1.2, 2.45), (1.2, 0.12)]
    cao = max(y for _, y in dinh) + 0.3; rong = 2 * max(abs(x) for x, _ in dinh) + 0.9
    w, h = int(rong * MET * S), int(cao * MET * S)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    P = lambda x, y: (w / 2 + x * MET * S, h - (y + 0.08) * MET * S)
    # bóng chạm đất: hai vệt mờ dưới chân
    bong = Image.new('L', (w, h), 0); db = ImageDraw.Draw(bong)
    day = min(y for _, y in dinh); thap = [p for p in dinh if p[1] < day + 0.02]
    chan = [min(thap), max(thap)] if hinh != 'tròn' else [(0, day)]   # khung tròn đứng trên một chân đế ở giữa
    for x, _ in chan:
        cx, cy = P(x, 0); db.ellipse((cx - 0.38 * MET * S, cy - 0.06 * MET * S, cx + 0.38 * MET * S, cy + 0.07 * MET * S), fill=150)
    bong = bong.filter(ImageFilter.GaussianBlur(0.05 * MET * S))
    lop_b = Image.new('RGBA', (w, h), (22, 40, 22, 0)); lop_b.putalpha(bong.point(lambda v: int(v * 0.55)))
    im.alpha_composite(lop_b)
    # chân đế: tấm phẳng hình thang (nhìn hơi từ trên)
    for x, _ in chan:
        a, b_ = P(x - 0.3, 0.0), P(x + 0.3, 0.0)
        top = [(a[0] + 0.05 * MET * S, a[1] - 0.07 * MET * S), (b_[0] - 0.05 * MET * S, b_[1] - 0.07 * MET * S)]
        d.polygon([a, b_, top[1], top[0]], fill=mau[2] + (255,), outline=mau[0] + (235,), width=int(1.3 * S))
        d.line([top[0], top[1]], fill=mau[3] + (200,), width=int(0.8 * S))
        # cột nối chân đế với khung
        ong(d, [P(x, 0.04), P(x, 0.12)], r_ong, mau)
    ong(d, [P(*p) for p in dinh], r_ong * (2.6 if hinh == 'chữ nhật' else 1), mau)
    if hinh == 'chữ nhật': ong(d, [P(-1.5, 2.5), P(1.5, 2.5)], r_ong * 2.8, mau)   # xà gỗ đặt trên đầu cột, nhô ra hai bên
    for p in (dinh[:-1] if hinh in ('lục giác', 'tam giác') else []):     # khớp nối ở đỉnh
        cx, cy = P(*p); rr = r_ong * 0.85 * S
        d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), fill=mau[2] + (255,), outline=mau[0] + (235,), width=int(1.2 * S))
    im = im.resize((w // S, h // S), Image.LANCZOS)
    # vân giấy: nhiễu mịn nhân vào phần đã vẽ
    a = np.asarray(im).astype(np.float32)
    nz = np.asarray(Image.fromarray((rng.rand(a.shape[0], a.shape[1]) * 255).astype('uint8')).filter(ImageFilter.GaussianBlur(0.8))).astype(np.float32) / 255
    a[..., :3] *= (0.94 + 0.12 * nz)[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype('uint8')), w // S / 2, h // S - 0.08 * MET


def dat(nen, hinh_anh, ax_px, ay_px):
    out = nen.convert('RGBA'); x = int(X / 100 * W - ax_px); y = int(Y / 100 * H - ay_px)
    out.alpha_composite(hinh_anh, (x, y)); return out.convert('RGB')


if __name__ == '__main__':
    NEN = Image.open(sys.argv[1] if len(sys.argv) > 1 else 'nen-ho.webp').convert('RGB')
    CONG = Image.open(sys.argv[2] if len(sys.argv) > 2 else 'cong-tron.webp').convert('RGBA')
    assert NEN.size == (W, H)
    # cổng tròn vẽ tay, đặt theo số đo TT trong bản chơi
    cw, ch, pxm, axr, ayr = 760, 676, 180.17, 0.5571, 0.9088
    cao = 0.307 * (ch / pxm) * (Y - 44) / 100 * H; rg = cao * cw / ch
    c = CONG.resize((round(rg), round(cao)), Image.LANCZOS)
    o = NEN.convert('RGBA'); o.alpha_composite(c, (round(X / 100 * W - axr * rg), round(Y / 100 * H - ayr * cao)))
    bang = [('Cổng tròn vẽ tay (tấm 2, có hoa)', o.convert('RGB'))]
    for ten, hinh, mau in [('Mã: khung lục giác đen mờ (thay T1)', 'lục giác', 'đen mờ'), ('Mã: khung tròn vàng đồng', 'tròn', 'vàng đồng'),
                           ('Mã: khung tam giác trắng', 'tam giác', 'trắng'), ('Mã: vòm cong trắng', 'vòm', 'trắng'),
                           ('Mã: vòm nhọn kiểu nhà thờ, vàng đồng', 'vòm nhọn', 'vàng đồng'), ('Mã: khung chữ nhật gỗ (cột và xà)', 'chữ nhật', 'gỗ')]:
        k, ax_, ay_ = khung(hinh, MAU[mau]); bang.append((ten, dat(NEN, k, ax_, ay_)))
    hop = (int(W * 0.25), int(H * 0.3), int(W * 0.75), int(H * 0.86))
    tw, th = hop[2] - hop[0], hop[3] - hop[1]
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 20)
    G = Image.new('RGB', (tw * 2 + 30, (th + 36) * ((len(bang) + 1) // 2) + 20), (236, 240, 228)); dg = ImageDraw.Draw(G)
    for i, (ten, im) in enumerate(bang):
        x0 = 10 + (i % 2) * (tw + 10); y0 = 10 + (i // 2) * (th + 36)
        G.paste(im.crop(hop), (x0, y0 + 30)); dg.text((x0 + 4, y0 + 4), ten, fill=(18, 38, 28), font=font)
    G.save('khung-ma.jpg', quality=88)
    print('xong', G.size, '1 m =', round(MET, 1), 'px')
