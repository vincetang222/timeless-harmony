# Xuất đồ tự vẽ cho màn "Trang trí theo lớp" của trang thử (0 lượt), ngày 26/11:
#   - khung cổng vẽ bằng mã: 6 hình × 4 màu, vẽ ở 2× thước cũ để phóng gần vẫn nét; lớp hoa Canva (T14) đặt sẵn theo từng khung, kèm mặt nạ đổi tông;
#   - nền đêm (cỡ 1600, 900 và hình thẻ);
#   - bộ bàn 3D: tranh, mặt nạ 3 lớp (đỏ = khăn, lục = đệm, lam = khung ghế; không nén mất dữ liệu), toạ độ khăn gói 12 bit vào RGB;
#   - cận cảnh bàn Âu, Việt: tranh, mặt nạ (đỏ = khăn, lục = đĩa lót, lam = dao nĩa), toạ độ khăn.
# Chạy: python3 xuat_lab.py <thư mục bản chơi> <thư mục nền đêm> <bàn tròn 3D> <bàn dài 3D> <cận cảnh 3D> <t14-xuat.png> [phần: nen,khung,ban,gan,vai,loa]
#   - ô hoạ tiết vải (ren, kim sa, gấm) lặp liền mạch, để bản chơi trải lên khăn theo toạ độ khăn;
# Ra: <bản chơi>/anh/..., <bản chơi>/anh/tt/..., số đo tt-lab.json (chép vào TT3 trong index.html), ảnh kiểm tra xuat-lab-*.jpg
import sys, os, json, math
import numpy as np
import png   # pypng: đọc ảnh toạ độ 16 bit
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage as nd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import khung_ma as K
import trang_tri as T

LAB, DEM, TRON, DAI, GAN, T14 = sys.argv[1:7]
PHAN = set((sys.argv[7] if len(sys.argv) > 7 else 'nen,khung,ban,gan,vai,loa').split(','))   # chạy riêng từng phần, ví dụ: khung,vai
ANH = os.path.join(LAB, 'anh'); TT = os.path.join(ANH, 'tt'); os.makedirs(TT, exist_ok=True)
NEN_THE = (236, 240, 228)
so = json.load(open('tt-lab.json')) if os.path.exists('tt-lab.json') else {}


def luu_webp(im, ten, mat=False, q=86):
    """mat=True: không nén mất dữ liệu, ảnh RGB không kênh alpha, không hồ sơ màu (để trình duyệt đọc đúng từng số)."""
    f = os.path.join(TT, ten)
    if mat: im.convert('RGB').save(f, lossless=True, quality=100, method=6)
    else: im.save(f, quality=q, method=6)
    return os.path.getsize(f) // 1024


def the(im, ten, nen=NEN_THE):
    t = Image.new('RGBA', (320, 240), nen + (255,)); q = min(292 / im.size[0], 216 / im.size[1])
    z = im.resize((round(im.size[0] * q), round(im.size[1] * q)), Image.LANCZOS); t.alpha_composite(z, ((320 - z.size[0]) // 2, (240 - z.size[1]) // 2))
    t.convert('RGB').save(os.path.join(TT, 't-' + ten + '.webp'), quality=80, method=6)


# ---------- 1. Nền đêm ----------
for noi in (('ho', 'langque') if 'nen' in PHAN else ()):
    nen = Image.open(os.path.join(DEM, f'nen-{noi}-dem.webp')).convert('RGB'); assert nen.size == (1600, 889)
    nen.save(os.path.join(ANH, f'nen-{noi}-dem.webp'), quality=82, method=6)
    nho = nen.resize((900, 500), Image.LANCZOS); nho.save(os.path.join(ANH, f'nen-{noi}-dem-m.webp'), quality=80, method=6)
    w, h = nho.size; cw = w / 2.5; chh = cw * 10 / 16; x0 = (w - cw) * 0.5; y0 = (h - chh) * 0.45   # cùng cách cắt hình thẻ như trang_tri.py
    nho.crop((round(x0), round(y0), round(x0 + cw), round(y0 + chh))).resize((320, 200), Image.LANCZOS).save(os.path.join(ANH, f't-nen-{noi}-dem.webp'), quality=76, method=6)

# ---------- 2. Cụm hoa Canva (T14): tách nền, cắt 4 cụm, mặt nạ cánh hoa ----------
def mat_na_canh(im):
    """Cánh mẫu đơn hồng, trắng của tấm Canva (mat_na_hoa của trang_tri.py làm cho hoa trắng nên bỏ sót cánh hồng).
    Cánh: hồng (đỏ trội hơn lục, lam xấp xỉ lục) hoặc gần trắng. Lá bạch đàn (lục, lam trội), cỏ lau (be: lam thấp hẳn) không được nhuộm."""
    a = np.asarray(im).astype(np.float32); r, g, b, al = a[..., 0], a[..., 1], a[..., 2], a[..., 3]
    hong = T.buoc(r - g, 4, 14) * (1 - T.buoc(g - b, 4, 12)) * T.buoc(r, 120, 160)
    trang = T.buoc(np.minimum(np.minimum(r, g), b), 196, 220) * (1 - T.buoc(r - b, 26, 40)) * (1 - T.buoc(g - r, 0, 6))
    w = np.maximum(hong, trang) * (1 - T.buoc(g - r, 0, 8)) * (al / 255)
    w = nd.grey_opening(w, size=3)                                                      # bỏ chấm lẻ trên lá
    return Image.fromarray(np.clip(nd.gaussian_filter(w, 0.7) * 255, 0, 255).astype('uint8'))


roi = T.tach(T14) if 'khung' in PHAN else None
CUM = {}
if roi is not None:
  a = np.asarray(roi)
  lab, n = nd.label(nd.binary_dilation(a[..., 3] > 30, iterations=12))
  sz = nd.sum(np.ones_like(lab), lab, range(1, n + 1)); CUM = {}
  for k in np.argsort(-sz)[:4] + 1:
      ys, xs = np.nonzero(lab == k); bb = (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)
      c = np.asarray(roi.crop(bb)).copy(); c[..., 3] = (c[..., 3] * (lab == k)[bb[1]:bb[3], bb[0]:bb[2]]).astype('uint8')
      cx, cy = (bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2   # nhận dạng theo vị trí trong tấm Canva, như t14_so.py
      ten = 'chan' if (cy > 0.55 * a.shape[0] and cx > 0.5 * a.shape[1]) else 'tron' if cx > 0.6 * a.shape[1] else 'goc' if cx < 0.3 * a.shape[1] else 'ru'
      CUM[ten] = Image.fromarray(c)
  print('cụm hoa:', {k: v.size for k, v in CUM.items()})

# ---------- 3. Khung cổng bằng mã + lớp hoa ----------
MET1 = K.MET; K.MET = MET2 = 2 * MET1          # khung_ma đọc K.MET lúc vẽ
HINH = {'luc-giac': 'lục giác', 'tron': 'tròn', 'tam-giac': 'tam giác', 'vom': 'vòm', 'vom-nhon': 'vòm nhọn', 'chu-nhat': 'chữ nhật'}
MAU = {'den': 'đen mờ', 'dong': 'vàng đồng', 'trang': 'trắng', 'go': 'gỗ'}
R6 = 1.45; y6 = R6 * 0.866 + 0.12
# chỗ gắn cụm hoa (m, gốc toạ độ = giữa chân khung trên mặt đất): (cụm, x, y, rộng m, neo x, neo y, lật gương)
GAN_HOA = {
    'luc-giac': [('goc', -0.725, 2 * y6 - 0.12, 2.0, 0.42, 0.38, 0), ('ru', R6 + 0.02, y6 + 0.45, 1.05, 0.55, 0.22, 0), ('chan', 0.875, 0.1, 1.9, 0.5, 0.86, 0)],
    'tron': [('goc', -0.83, 2.76, 2.0, 0.42, 0.38, 0), ('ru', 1.47, 2.0, 1.05, 0.55, 0.22, 0), ('chan', 0.8, 0.1, 1.9, 0.5, 0.86, 0)],
    'tam-giac': [('goc', -0.05, 2.5, 2.0, 0.42, 0.38, 0), ('chan', 1.35, 0.1, 1.9, 0.5, 0.86, 0)],
    'vom': [('goc', -0.77, 2.32, 2.0, 0.42, 0.38, 0), ('ru', 1.22, 1.85, 1.05, 0.55, 0.22, 0), ('chan', 1.25, 0.1, 1.9, 0.5, 0.86, 0)],
    'vom-nhon': [('goc', -0.7, 2.72, 2.0, 0.42, 0.38, 0), ('ru', 1.17, 1.95, 1.05, 0.55, 0.22, 0), ('chan', 1.2, 0.1, 1.9, 0.5, 0.86, 0)],
    'chu-nhat': [('goc', -1.2, 2.5, 2.0, 0.42, 0.38, 0), ('ru', 1.22, 2.5, 1.05, 0.55, 0.22, 0), ('chan', 1.3, 0.1, 1.9, 0.5, 0.86, 0)],
}
kiem_khung = []
for slug, hinh in (HINH.items() if 'khung' in PHAN else ()):
    k0, ax0, ay0 = K.khung(hinh, K.MAU['vàng đồng'])
    # đặt cụm hoa theo toạ độ px của tấm khung, rồi nới khung vẽ cho vừa cả hoa
    dat = []
    for c, x, y, rm, axc, ayc, lat in GAN_HOA[slug]:
        im = CUM[c]; s = rm * MET2 / im.size[0]; im = im.resize((max(1, round(im.size[0] * s)), max(1, round(im.size[1] * s))), Image.LANCZOS)
        if lat: im = im.transpose(Image.FLIP_LEFT_RIGHT)
        px, py = k0.size[0] / 2 + x * MET2, k0.size[1] - (y + 0.08) * MET2     # cùng phép đổi P(x, y) của khung_ma
        dat.append((im, round(px - axc * im.size[0]), round(py - ayc * im.size[1])))
    x_min = min([0] + [d[1] for d in dat]); y_min = min([0] + [d[2] for d in dat])
    x_max = max([k0.size[0]] + [d[1] + d[0].size[0] for d in dat]); y_max = max([k0.size[1]] + [d[2] + d[0].size[1] for d in dat])
    W, H = x_max - x_min, y_max - y_min; ox, oy = -x_min, -y_min
    hoa = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    for im, x, y in dat: hoa.alpha_composite(im, (x + ox, y + oy))
    mn = mat_na_canh(hoa)
    kb = {}
    for ms, mau in MAU.items():
        k, _, _ = K.khung(hinh, K.MAU[mau]); full = Image.new('RGBA', (W, H), (0, 0, 0, 0)); full.alpha_composite(k, (ox, oy))
        kb[ms] = luu_webp(full, f'khung-{slug}-{ms}.webp')
        if ms == 'dong': the_im = full.copy(); the_im.alpha_composite(hoa); the(the_im, 'khung-' + slug)
    kh = luu_webp(hoa, f'hoa-{slug}.webp'); Image.merge('RGB', (mn, mn, mn)).save(os.path.join(TT, f'hoa-{slug}-mn.webp'), quality=70, method=6)
    mh = np.asarray(mn).astype(np.float32) / 255; hg = np.percentile(np.asarray(hoa).astype(np.float32)[..., :3][mh > 0.9], 85, axis=0)
    so['khung-' + slug] = dict(w=W, h=H, pxm=round(MET2, 2), ax=round((ox + ax0) / W, 4), ay=round((oy + ay0) / H, 4), hoa_goc=[round(float(v), 1) for v in hg], kb=kb, hoa_kb=kh)
    kiem_khung.append((slug, hoa, mn, W, H, ox, oy, ax0, ay0))
print('khung:', {k: (v['w'], v['h'], sum(v['kb'].values()), v['hoa_kb'], v['hoa_goc']) for k, v in so.items() if k.startswith('khung-')})

# ảnh kiểm tra: 6 khung vàng đồng + hoa trên nền Vườn Hồ, và mặt nạ hoa (đỏ = phần được đổi tông)
NEN = Image.open(os.path.join(ANH, 'nen-ho.webp')).convert('RGBA')
o = []
for slug, hoa, mn, W, H, ox, oy, ax0, ay0 in kiem_khung:
    c = NEN.copy(); f = Image.open(os.path.join(TT, f'khung-{slug}-dong.webp')).convert('RGBA')
    s = MET1 / MET2; f = f.resize((round(W * s), round(H * s)), Image.LANCZOS); hh = hoa.resize(f.size, Image.LANCZOS)
    x = round(K.X / 100 * 1600 - (ox + ax0) * s); y = round(K.Y / 100 * 889 - (oy + ay0) * s); c.alpha_composite(f, (x, y)); c.alpha_composite(hh, (x, y))
    m = np.asarray(mn.resize(f.size, Image.LANCZOS)).astype(np.float32) / 255; hm = np.asarray(hh).astype(np.float32)
    hm[..., :3] = hm[..., :3] * (1 - m[..., None] * 0.7) + np.array([255, 40, 60]) * m[..., None] * 0.7
    c2 = NEN.copy(); c2.alpha_composite(f, (x, y)); c2.alpha_composite(Image.fromarray(hm.astype('uint8')), (x, y))
    hop = (380, 200, 1220, 760); o += [c.crop(hop).convert('RGB'), c2.crop(hop).convert('RGB')]
if o:
    tw, th = o[0].size; G = Image.new('RGB', (tw * 2, th * 3), (240, 240, 240))
    for i, im in enumerate(o): G.paste(im.resize((tw // 2, th // 2)), ((i % 4) * tw // 2, (i // 4) * th // 2))
    G.save('xuat-lab-khung.jpg', quality=85)


# ---------- 4. Bộ bàn 3D ----------
def doc_uv(f):
    w, h, rows, info = png.Reader(f).asDirect(); a = np.vstack([np.array(r, np.float32) for r in rows]).reshape(h, w, info['planes'])
    return a[..., :2] / 65535.0


def goi_uv(uv, khan):
    """u, v (0..1) → 12 bit mỗi số: R = 8 bit cao của u, G = 8 bit cao của v, B = 4 bit thấp của u | 4 bit thấp của v. Ngoài khăn để 0."""
    q = np.clip(np.round(uv * 4095), 0, 4095).astype(np.int32) * (khan > 0.02)[..., None]
    u, v = q[..., 0], q[..., 1]
    return np.dstack([u >> 4, v >> 4, ((u & 15) << 4) | (v & 15)]).astype('uint8')


def goc_lop(rgb, w):
    sel = rgb[w > 0.9]
    return [round(float(x), 1) for x in np.percentile(sel, 85, axis=0)] if len(sel) > 50 else None


def mot_mau(mn, uvp):
    """Một điểm mẫu chắc chắn nằm trên khăn: bản chơi đọc lại để kiểm trình duyệt có giữ đúng từng số không."""
    ys, xs = np.nonzero(mn[..., 0] > 250); i = len(ys) // 2; y, x = int(ys[i]), int(xs[i])
    return [x, y, [int(v) for v in uvp[y, x]]]


def xuat_bo(thu_muc, ten, m, lop_id, the_ten=None, nen_the=NEN_THE):
    im = Image.open(os.path.join(thu_muc, ten + '.png')).convert('RGBA'); rgb = np.asarray(im).astype(np.float32)[..., :3]
    idm = np.asarray(Image.open(os.path.join(thu_muc, ten + '-id.png')).convert('RGB')).astype(np.float32) / 255
    mn = lop_id(idm)                                     # H×W×3, 0..1
    mn = np.where(mn < 0.03, 0, np.where(mn > 0.97, 1, mn))   # nhiễu lấy mẫu của lượt ID: gần 0, gần 1 thì làm tròn (tệp nhẹ hơn nhiều)
    uv = doc_uv(os.path.join(thu_muc, ten + '-uv.png')); uvp = goi_uv(uv, mn[..., 0])
    mn8 = np.clip(np.round(mn * 255), 0, 255).astype('uint8')
    kb = luu_webp(im, ten + '.webp'); kbm = luu_webp(Image.fromarray(mn8), ten + '-mn.webp', mat=True); kbu = luu_webp(Image.fromarray(uvp), ten + '-uv.webp', mat=True)
    if the_ten: the(im, the_ten, nen_the)
    m = dict(m); m.update(goc=[goc_lop(rgb, mn[..., i]) for i in range(3)], mau=mot_mau(mn8, uvp), kb=[kb, kbm, kbu])
    return m


ID_BAN = lambda idm: idm                                  # bàn: màu ID đã là một kênh cho mỗi lớp (khăn đỏ, đệm lục, khung ghế lam)
for thu_muc, tep in (((TRON, 'ban-tron.json'), (DAI, 'ban-dai.json')) if 'ban' in PHAN else ()):
    for ten, m in json.load(open(os.path.join(thu_muc, tep))).items():
        so[ten] = xuat_bo(thu_muc, ten, m, ID_BAN, ten)
        print(ten, so[ten]['w'], so[ten]['h'], so[ten]['kb'], 'KB', so[ten]['goc'])

# cận cảnh: màu ID có màu pha (dao nĩa vàng, ly lục lam, khăn ăn tím) và ly trong suốt (độ đục 0,28) đè lên khăn, đĩa.
# Bóc phần ly trước: ly cộng 0,28 vào lục và lam của thứ nằm sau nên tổng R+G+B > 1 (mép đĩa giáp đĩa lót thì tổng = 1).
# Phần còn lại pha tối đa hai lớp: dao nĩa = R+G−1, khăn ăn = R+B−1, phần dư của đỏ là khăn, của lam là đĩa lót.
# Trọng số nhân (1 − phần ly): nhìn xuyên ly vẫn thấy khăn đổi màu, vệt sáng của ly giữ nguyên.
def ID_GAN(idm):
    r, g, b = idm[..., 0], idm[..., 1], idm[..., 2]
    ly = np.minimum(g, b) * np.clip((r + g + b - 1.02) / 0.12, 0, 1); ly = np.minimum(ly, 0.95)
    R, G, B = r / (1 - ly), (g - ly) / (1 - ly), (b - ly) / (1 - ly)
    kl = np.clip(R + G - 1, 0, 1); tim = np.clip(R + B - 1, 0, 1)
    khan = np.clip(R - kl - tim, 0, 1); lot = np.clip(B - tim, 0, 1)
    return np.dstack([khan, lot, kl]) * (1 - ly)[..., None]


for kieu in (('au', 'viet') if 'gan' in PHAN else ()):
    ten = 'can-canh-' + kieu; m = json.load(open(os.path.join(GAN, ten + '.json')))
    im = Image.open(os.path.join(GAN, ten + '.png')); m.update(w=im.size[0], h=im.size[1])
    so[ten] = xuat_bo(GAN, ten, m, ID_GAN, ten)
    print(ten, so[ten]['kb'], 'KB', so[ten]['goc'])

# ---------- 4b. Loa (loa_3d.py): tranh cùng thước với bàn; thư mục loa lấy từ biến LOA_3D hoặc <bàn tròn>/../loa ----------
if 'loa' in PHAN:
    LOA = os.environ.get('LOA_3D') or os.path.join(os.path.dirname(os.path.abspath(TRON)), 'loa')
    for ten, m in json.load(open(os.path.join(LOA, 'loa.json'))).items():
        im = Image.open(os.path.join(LOA, ten + '.png')).convert('RGBA'); kb = luu_webp(im, ten + '.webp')
        m = dict(m); m.pop('mo', None); m['kb'] = kb; so[ten] = m; print(ten, m)

# ---------- 5. Ô hoạ tiết vải: lặp liền mạch (chu kỳ hoạ tiết chia hết cạnh ô), 512 px và bản 128 px cho bàn nhìn xa ----------
# Kênh: R = tỉ lệ pha màu thứ hai (ren trắng, hoa gấm), G = độ sáng hạt (÷1,3), B = điểm loé. Cùng công thức với hoa_van.py.
if 'vai' in PHAN:
    from hoa_van import hx, fr
    def o_vai(ten, T_m, ham, N=512, ss=2):
        g = (np.arange(N * ss) + 0.5) / (N * ss) * T_m; u, v = np.meshgrid(g, g)
        k, gg, sp = ham(u, v); kenh = np.dstack([k, gg / 1.3, sp]).reshape(N, ss, N, ss, 3).mean((1, 3))
        im = Image.fromarray(np.clip(np.round(kenh * 255), 0, 255).astype('uint8'))
        kb = luu_webp(im, f'vai-{ten}.webp', mat=True); luu_webp(im.resize((128, 128), Image.BOX), f'vai-{ten}-128.webp', mat=True)
        so.setdefault('vai', {})[ten] = dict(met=T_m, n=N, kb=kb)
    def ren(u, v):
        c = 0.05; ui = np.floor(u / c); vv = v / c + 0.5 * (ui % 2); vi = np.floor(vv)
        du = fr(u / c) - 0.5; dv = vv - vi - 0.5; r = np.hypot(du, dv)
        vong = np.exp(-((r - 0.34) / 0.045) ** 2) + np.exp(-((r - 0.16) / 0.035) ** 2)
        th = np.arctan2(dv, du); canh = (r < 0.27) & (np.cos(6 * th) > 0.3) & (r > 0.2)
        luoi = (np.abs(np.sin(u / 0.004 * np.pi)) < 0.25) | (np.abs(np.sin(v / 0.004 * np.pi)) < 0.25)
        return np.clip(vong * 0.95 + canh * 0.9 + luoi * 0.32, 0, 0.95), np.ones_like(u), np.zeros_like(u)
    def kimsa(u, v, n=84):
        c = 0.006; ui = np.floor(u / c); vv = v / c + 0.5 * (ui % 2); vi = np.floor(vv); h = hx(ui % n, vi % n)
        du = fr(u / c) - 0.5; dv = vv - vi - 0.5; r = np.hypot(du, dv); hat = np.clip((0.5 - r) / 0.08, 0, 1)
        return np.zeros_like(u), (0.62 + 0.62 * h) * (0.55 + 0.45 * hat), ((h > 0.965) * hat * (r < 0.25)).astype(np.float64)
    def gam(u, v):
        c = 0.11; ui = np.floor(u / c); vv = v / c + 0.5 * (ui % 2); vi = np.floor(vv)
        du = fr(u / c) - 0.5; dv = vv - vi - 0.5; r = np.hypot(du, dv); th = np.arctan2(dv, du)
        canh = r < 0.36 * (0.5 + 0.5 * np.abs(np.cos(2 * th))) ** 0.7; vien = np.abs(r - 0.44) < 0.025
        return np.clip(canh * 1.0 + vien * 0.8, 0, 1), np.ones_like(u), np.zeros_like(u)
    o_vai('ren', 0.5, ren); o_vai('kimsa', 0.504, kimsa); o_vai('gam', 0.44, gam)
    print('vải:', so['vai'])

json.dump(so, open('tt-lab.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print('xong; số đo ở tt-lab.json')
