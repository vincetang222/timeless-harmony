# Ghép cảnh từ đồ tự vẽ (0 lượt), ngày 25/11: nền Vườn Hồ (ngày, đêm bằng mã), khung cổng bằng mã, bộ bàn tròn 3D.
# Khăn nhiều lớp và đệm ghế đổi màu bằng ảnh mặt nạ và ảnh toạ độ khăn do 3D xuất ra (không khoanh tay như trên tranh cũ).
# Chạy: python3 canh_3d.py <thư mục bàn 3D (ban-tron-*.png, -id.png, -uv.png, ban-tron.json)> <nen-ho.webp> <nen-ho-dem.webp> → canh-3d.jpg
import sys, os, json
import numpy as np
import png   # pypng: đọc ảnh toạ độ 16 bit
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hoa_van import p_ren, p_kimsa, p_tron, p_caro
import khung_ma as K

DIR = sys.argv[1] if len(sys.argv) > 1 else '.'
SO = json.load(open(os.path.join(DIR, 'ban-tron.json'))) if os.path.exists(os.path.join(DIR, 'ban-tron.json')) else {}
SANG_DEM = np.array([0.304, 0.364, 0.552])      # hệ số chỉnh sáng đo ở dem_ma.py


def doc_uv(f):
    w, h, rows, info = png.Reader(f).asDirect(); a = np.vstack([np.array(r, np.float32) for r in rows]).reshape(h, w, info['planes'])
    return a / 65535.0


def buoc(x, a_, b_): t = np.clip((x - a_) / (b_ - a_), 0, 1); return t * t * (3 - 2 * t)


def nhuom(tong, q):
    lt = (tong @ np.array([0.299, 0.587, 0.114], np.float32)) / 255
    return np.minimum(255, q ** (1 + (1 - lt) * 1.6)[..., None] * tong)


def bo_ban(ten, lop, dem_mau=None, sang=None, thu_muc=None, so=None, nhuom_id=None):
    """Tranh 3D + khăn nhiều lớp (lop: [(hình, chất, độ đục)] từ dưới lên) + màu đệm + nhuộm thêm theo màu ID
    (nhuom_id: {màu ID (r, g, b): tông}, ví dụ đĩa lót lam → bạc). Trả ảnh RGBA."""
    thu_muc = thu_muc or DIR; m = so or SO[ten]; Rm = m.get('khan_uv_Rm', m.get('Rm')); R = m['R']
    im = np.asarray(Image.open(os.path.join(thu_muc, ten + '.png')).convert('RGBA')).astype(np.float32)
    idm = np.asarray(Image.open(os.path.join(thu_muc, ten + '-id.png')).convert('RGB')).astype(np.float32) / 255
    uv = doc_uv(os.path.join(thu_muc, ten + '-uv.png'))
    rgb = im[..., :3]
    khan = idm[..., 0] * (1 - idm[..., 2]); dem = idm[..., 1]
    if lop:
        X = (uv[..., 0] - 0.5) * 2 * Rm; Z = (uv[..., 1] - 0.5) * 2 * Rm; tren = np.hypot(X, Z) <= 1.0
        goc = np.percentile(rgb[khan > 0.9], 85, axis=0); q = np.minimum(1.06, rgb / goc)
        col = None
        for hinh, chat, duc in lop:
            f = hinh(X, Z, tren); ton, lap = chat(Z * R, X * R); c = nhuom(ton, q)
            if np.any(lap): c = np.minimum(255, c + np.asarray(lap)[..., None] * 255 * np.clip(q.mean(-1, keepdims=True), 0, 1))
            if col is None: col = c; continue
            ngoai = np.clip(1 + f / 0.06, 0, 1) * (f < 0); col = col * (1 - ngoai * np.where(tren, 0.10, 0.30))[..., None]
            tr = buoc(f, -0.004, 0.006)[..., None] * duc; vien = 1 - 0.14 * (np.clip(1 - f / 0.012, 0, 1) * (f > 0))[..., None]
            col = col * (1 - tr) + c * vien * tr
        rgb = rgb * (1 - khan[..., None]) + col * khan[..., None]
    if dem_mau is not None:
        gd = np.percentile(im[..., :3][dem > 0.9], 85, axis=0); qd = np.minimum(1.06, im[..., :3] / gd)
        rgb = rgb * (1 - dem[..., None]) + nhuom(np.broadcast_to(np.array(dem_mau, np.float32), rgb.shape), qd) * dem[..., None]
    for mau_id, tong in (nhuom_id or {}).items():
        k = np.clip(1 - np.abs(idm - np.array(mau_id, np.float32)).sum(-1) * 2, 0, 1)   # gần đúng màu ID
        if k.max() == 0: continue
        g0 = np.percentile(im[..., :3][k > 0.9], 85, axis=0); qq = np.minimum(1.06, im[..., :3] / g0)
        rgb = rgb * (1 - k[..., None]) + nhuom(np.broadcast_to(np.array(tong, np.float32), rgb.shape), qq) * k[..., None]
    if sang is not None: rgb = rgb * sang
    return Image.fromarray(np.dstack([np.clip(rgb, 0, 255), im[..., 3]]).astype('uint8'), 'RGBA')


def dat(canh, sprite, m, X, Y):
    W, H = canh.size; cao = 0.307 * (m['h'] / m['pxm']) * (Y - 44) / 100 * H; rg = cao * m['w'] / m['h']
    s = sprite.resize((round(rg), round(cao)), Image.LANCZOS)
    canh.alpha_composite(s, (round(X / 100 * W - m['ax'] * rg), round(Y / 100 * H - m['ay'] * cao)))


vuong_cheo = lambda s: (lambda X, Z, t: s - (np.abs(X) + np.abs(Z)))
chay_ban = lambda w, d: (lambda X, Z, t: np.minimum(w / 2 - np.abs(X), d - np.abs(Z)))
ca_ban = lambda X, Z, t: np.full(X.shape, 9.0)
tron_ = lambda c: (lambda u, v: p_tron(u, v, c))

if __name__ == '__main__':
    NGAY = Image.open(sys.argv[2]).convert('RGB'); DEM = Image.open(sys.argv[3]).convert('RGB')
    PHOI = [
        ('Ngày: khăn trắng một lớp, đệm trắng', None, None),
        ('Ngày: nền xanh xô thơm + vuông chéo góc ren, đệm xanh', [(ca_ban, tron_((150, 170, 140)), 1), (vuong_cheo(1.42), lambda u, v: p_ren(u, v, (238, 234, 222), (254, 253, 250)), 1)], (150, 170, 140)),
        ('Đêm: nền xanh than + vuông chéo góc kim sa bạc', [(ca_ban, tron_((34, 44, 70)), 1), (vuong_cheo(1.4), lambda u, v: p_kimsa(u, v, (200, 204, 210)), 1)], (200, 204, 210)),
        ('Đêm: nền trắng + chạy bàn đỏ đô, đệm đỏ', [(ca_ban, tron_((246, 244, 238)), 1), (chay_ban(0.34, 1.5), tron_((120, 24, 34)), 1)], (120, 24, 34)),
    ]
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 20)
    W, H = NGAY.size; tw, th = W // 2, H // 2
    G = Image.new('RGB', (tw * 2 + 30, (th + 36) * 2 + 20), (236, 240, 228)); d = ImageDraw.Draw(G)
    for i, (ten, lop, dm) in enumerate(PHOI):
        dem = ten.startswith('Đêm')
        canh = (DEM if dem else NGAY).convert('RGBA')
        k, ax_, ay_ = K.khung('lục giác', K.MAU['vàng đồng' if dem else 'đen mờ'])
        if dem: k = Image.fromarray(np.dstack([np.asarray(k)[..., :3] * SANG_DEM, np.asarray(k)[..., 3]]).astype('uint8'), 'RGBA')
        canh.alpha_composite(k, (round(K.X / 100 * W - ax_), round(K.Y / 100 * H - ay_)))
        for ten_ban, X, Y in [('ban-tron-10', 19, 95), ('ban-tron-10', 81, 95)]:   # tâm bàn trên sàn
            dat(canh, bo_ban(ten_ban, lop, dm, SANG_DEM if dem else None), SO[ten_ban], X, Y)
        x0 = 10 + (i % 2) * (tw + 10); y0 = 10 + (i // 2) * (th + 36)
        G.paste(canh.convert('RGB').resize((tw, th), Image.LANCZOS), (x0, y0 + 30)); d.text((x0 + 4, y0 + 4), f'{i + 1}. {ten}', fill=(18, 38, 28), font=font)
        if i == 1: canh.convert('RGB').save('canh-3d-ngay.jpg', quality=90)
    G.save('canh-3d.jpg', quality=88)
    print('xong', G.size)
