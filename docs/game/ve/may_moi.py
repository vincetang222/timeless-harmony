# Sửa lỗi lông mày dính tóc, không dùng AI:
#  1) chú rể tóc Vuốt ngược: xoá lông mày gốc khỏi 9 đầu, lông mày mới là lớp chỉ có nét (cắt từ bên mày không bị tóc che, lật cho bên kia);
#  2) (thử, không dùng) cô dâu tóc Dài thẳng: mảnh lông mày bỏ lọn tóc mái của kiểu Búi cao. Lọn tóc vắt thẳng qua lông mày mảnh,
#     nhạt nên tách không sạch, làm đứt lông mày; bản chơi giữ mảnh của bản 13. Giữ mã để thử lại khi có tranh nguồn tốt hơn.
# Kết quả ghi vào out3/: dau-*.webp (9 đầu), manh/*.png (mảnh), may_moi.json (vị trí).
import sys, os, json; sys.path.insert(0, '.')
import numpy as np
from PIL import Image, ImageOps
from may_lib import *
from may_xoa import *
from may_net import net_may, lop_net, KHUNG
from may_xoa import _mem
try: from may_sua import SUA, SUA_NET
except Exception: SUA, SUA_NET = {}, {}
os.makedirs('out3/manh', exist_ok=True)
H = 2736; KQ = {'nam': {'mayA': {}, 'vitriA': {}}, 'nu': {'mayS': {}}}
def ramp(a, b, h): y = np.arange(h, dtype=float)[:, None]; return np.clip((y - a) / (b - a), 0, 1)
def xuat(im, g): s = META[g]['s']; return im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)

# ---------- 1a) nét lông mày chú rể ----------
CHI_NU = '--nu' in sys.argv
if CHI_NU: KQ = json.load(open('out3/may_moi.json')); KQ['nu'] = {'mayS': {}}
g = 'nam'; s = META[g]['s']; box = META[g]['box']; Wc = box[2] - box[0]
for face in ([] if CHI_NU else ['goc', 'tron', 'vuong']):
    for kind in ['manh', 'tunhien', 'dam']:
        # mặt vuông, lông mày Đậm: cả hai bên trong tranh nguồn đều bị lọn tóc vắt qua, không tách sạch được; dùng nét Đậm của mặt trái xoan
        n = f'may-{g}-{"goc" if (face, kind) == ("vuong", "dam") else face}-{kind}'; im, r, S, tamm = net_may(n, g, 1, SUA_NET.get((n, 1)))
        # ảnh xuất bị lật ngang: bên 1 (phải trong ảnh nguồn) lật, bên 0 là bản lật của bên 1 nên giữ nguyên chiều
        for ben, anh in ((1, ImageOps.mirror(im)), (0, im)):
            o = xuat(anh, g); f = f'mayA-{g}-{face}-{kind}-{ben}'; o.save(f'out3/manh/{f}.png')
            KQ[g]['mayA'].setdefault(face, {}).setdefault(kind, [None, None])[ben] = {'f': f, 'w': o.width, 'h': o.height}
        print(n, flush=True)

# ---------- 1b) xoá lông mày gốc trên 9 đầu vuốt ngược ----------
cy, f_ = 600, 18; headbox = (box[0], box[1], box[2], min(box[3], 1500))
def lop_dau(a):
    a = a.copy(); al = a[..., 3] / 255; dac = (al > 0.9).astype(float); h = a.shape[0]
    keep = dac * (1 - ramp(cy - f_, cy + f_, h)) + (1 - dac) * (1 - ramp(cy + f_, cy + f_ + 6, h)); a[..., 3] = al * keep * 255
    c = Image.fromarray(a.astype('uint8'), 'RGBA').crop(headbox); c = ImageOps.mirror(c)
    return c.resize((round(c.width * s), round(c.height * s)), Image.LANCZOS)
for n in ([] if CHI_NU else [x for x in META[g]['dau'] if x.endswith('vuot')]):
    a = np.asarray(mo_anh(n)).astype(float)
    if '--thu' in sys.argv and n == 'nam-toc-vuot':   # kiểm: dựng lại không xoá phải trùng với tệp đang dùng
        cu = np.asarray(Image.open(f'out2/dau-{n}.webp').convert('RGBA')).astype(int); lop_dau(a).save('/tmp/_d.webp', quality=84, method=6)
        moi = np.asarray(Image.open('/tmp/_d.webp').convert('RGBA')).astype(int); print('lech toi da so voi ban cu:', np.abs(cu - moi).max())
    vt = []
    for ben, (px, py) in enumerate(tam(g, 'dau-' + n, 'mat')):
        ex, ey = tam_mat(a, px, py); r = tach(a, ex, ey, g, ben, SUA.get((n, ben))); kq, S = xoa(r)
        hh, ww = kq.shape[:2]; a[r['y0']:r['y0'] + hh, r['x0']:r['x0'] + ww, :3] = kq
        ys, xs = np.nonzero(r['may']); mx, my = r['x0'] + xs.mean(), r['y0'] + ys.mean()      # trọng tâm lông mày cũ, ảnh nguồn
        X, Y = (Wc - (mx - box[0])) * s, (my - box[1]) * s                                    # sang toạ độ ảnh xuất (đã lật)
        vt.append([round(X - KHUNG[0] * s / 2, 1), round(Y - KHUNG[1] * s / 2, 1)])
    lop_dau(a).save(f'out3/dau-{n}.webp', quality=84, method=6); KQ[g]['vitriA']['dau-' + n] = vt; print(n, vt, flush=True)

# ---------- 2) mảnh lông mày cô dâu, bỏ lọn tóc mái vắt qua trán ----------
g = 'nu'; s = META[g]['s']; hw, hh_ = NUA['may']
yy, xx = np.mgrid[-hh_:hh_, -hw:hw]; rr = np.sqrt((xx / hw) ** 2 + (yy / hh_) ** 2); mask = np.clip((1 - rr) / 0.35, 0, 1)
for face in ['goc', 'tron', 'vuong']:
    for kind in ['manh', 'tunhien', 'dam']:
        n = f'may-{g}-{face}-{kind}'; a = np.asarray(mo_anh(n)).astype(float)
        for ben in (0, 1):
            p = MANH[g]['manh']['may'][face][kind][ben]; x0, y0 = p['x0'], p['y0']
            ex, ey = tam_mat(a, x0 + 70, y0 + 28 + 45); r = tach(a, ex, ey, g, ben, SUA_NET.get((n, ben)))
            # quanh lông mày (trừ mảng tóc lớn và vùng mắt): lấp da để mất cả lông mày lẫn lọn tóc mái, rồi đặt lại riêng nét lông mày
            kqx, S = xoa(r); Hh, Ww = S.shape[:2]; yyw = np.mgrid[0:Hh, 0:Ww][0]
            vung = r['bao'] & ~gian(r['khoi'], 2) & (yyw < r['hang'])
            m = _mem(vung, 2.0); kq = r['w'] * (1 - m) + S * m
            ln = lop_net(r, S, ben, SUA_NET.get((n, ben)))
            if ln is not None: al = ln[0][..., None]; kq = kq * (1 - al) + ln[1] * al
            else: kq = r['w']; print('  giu nguyen manh cu:', n, ben)   # không dò được lông mày: giữ mảnh cũ còn hơn mất lông mày
            b = a.copy(); b[r['y0']:r['y0'] + Hh, r['x0']:r['x0'] + Ww, :3] = kq
            crop = b[y0:y0 + 2 * hh_, x0:x0 + 2 * hw].copy(); crop[..., 3] *= mask
            im = ImageOps.mirror(Image.fromarray(crop.astype('uint8'), 'RGBA')).resize((p['w'], p['h']), Image.LANCZOS)
            f = f'mayS-{g}-{face}-{kind}-{ben}'; im.save(f'out3/manh/{f}.png')
            KQ[g]['mayS'].setdefault(face, {}).setdefault(kind, [None, None])[ben] = {'f': f, 'w': p['w'], 'h': p['h']}
        print(n, flush=True)
json.dump(KQ, open('out3/may_moi.json', 'w'))
