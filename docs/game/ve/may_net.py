# Tách nét lông mày thành lớp trong suốt (chỉ có nét, không có da hay tóc) từ ảnh nguồn may-*.png
import sys, json; sys.path.insert(0, '.')
from may_lib import *
from may_xoa import *
from may_xoa import _mem
KHUNG = (160, 72)   # khung của lớp nét trong ảnh nguồn, tâm là trọng tâm lông mày
def net_may(n, g, ben, tham=None):
    a = np.asarray(mo_anh(n)).astype(float); kind = n.split('-')[3]; face = n.split('-')[2]
    p = MANH[g]['manh']['may'][face][kind][ben]; px, py = p['x0'] + 70, p['y0'] + 28 + 45
    ex, ey = tam_mat(a, px, py); r = tach(a, ex, ey, g, ben, tham); kq, S = xoa(r)
    for (xa_, ya_, xb_, yb_) in (tham or {}).get('ep_may', []):   # chỉ tay vùng lông mày khi dò tự động không ra
        r['may'][ya_:yb_, xa_:xb_] |= (r['netm'] | r['toc'])[ya_:yb_, xa_:xb_] & ~r['mat'][ya_:yb_, xa_:xb_]
    if not r['may'].any(): return None, r, S, None
    if tham and tham.get('duoi'):                                 # đuôi lông mày bị lọn tóc vắt qua: kéo dải mày (mép trên, mép dưới) qua chỗ lọn tóc
        M = r['may']; cols = np.nonzero(M.any(axis=0))[0]; out = 1 if ben == 1 else -1
        top = np.array([np.nonzero(M[:, c])[0].min() for c in cols]); bot = np.array([np.nonzero(M[:, c])[0].max() for c in cols])
        k = min(len(cols), 40); cs = cols[-k:] if out > 0 else cols[:k]; ts = top[-k:] if out > 0 else top[:k]; bs = bot[-k:] if out > 0 else bot[:k]
        pt, pb = np.polyfit(cs, ts, 1), np.polyfit(cs, bs, 1); toi = r['net'] | r['toc']; gioi = 110 + out * tham['duoi']
        x = (cols.max() + 1) if out > 0 else (cols.min() - 1)
        while (x <= gioi if out > 0 else x >= gioi):
            ya, yb = int(round(np.polyval(pt, x))), int(round(np.polyval(pb, x)))
            if yb < ya or toi[ya:yb + 1, x].mean() < 0.5: break
            M[ya:yb + 1, x] |= toi[ya:yb + 1, x]; x += out
    gan = gian(r['may'], 7); lab, k = thanh_phan(r['nho']); may = r['may'].copy()
    for i in range(1, k + 1):                                     # chỉ giữ mảnh nhỏ nằm sát lông mày (sợi mày), bỏ ngọn tóc mái
        c = lab == i
        if (c & gan).any(): may |= c
    if not (tham and tham.get('khong_noi')):                      # lọn tóc mảnh vắt ngang lông mày: phần nằm giữa hai đoạn mày coi là mày
        d = r['may'].copy()
        for k_ in range(1, 14): d |= dich(r['may'], k_, 0) | dich(r['may'], -k_, 0)
        e = d.copy()
        for k_ in range(1, 14): e &= dich(d, k_, 0) & dich(d, -k_, 0)
        may |= e & (r['net'] | r['toc']) & ~r['khoi'] & ~r['mat']
    R = gian(may, 4)
    Lp, Lsk = luma(r['w']), luma(S); loi = np.percentile(Lp[r['may']], 20)
    al = np.clip((Lsk - Lp) / np.maximum(Lsk - loi, 0.05), 0, 1) * _mem(R, 1.0)[..., 0]
    al = np.clip((al - 0.1) / 0.9, 0, 1)
    C = (r['w'] - (1 - al[..., None]) * S) / np.maximum(al[..., None], 0.3); C = np.clip(C, 0, 255)
    ys, xs = np.nonzero(r['may']); cx, cy = xs.mean(), ys.mean()
    W, H = KHUNG; x0, y0 = int(round(cx - W / 2)), int(round(cy - H / 2))
    out = np.zeros((H, W, 4)); ya, yb, xa, xb = max(0, y0), min(al.shape[0], y0 + H), max(0, x0), min(al.shape[1], x0 + W)
    out[ya - y0:yb - y0, xa - x0:xb - x0, :3] = C[ya:yb, xa:xb]; out[ya - y0:yb - y0, xa - x0:xb - x0, 3] = al[ya:yb, xa:xb] * 255
    return Image.fromarray(out.astype('uint8'), 'RGBA'), r, S, (r['x0'] + cx, r['y0'] + cy)
if __name__ == '__main__':
    from PIL import ImageDraw
    try: from may_sua import SUA_NET
    except Exception: SUA_NET = {}
    g, ben = sys.argv[1], int(sys.argv[2]); cells = []
    for face in ['goc', 'tron', 'vuong']:
        for kind in ['manh', 'tunhien', 'dam']:
            n = f'may-{g}-{face}-{kind}'; im, r, S, _ = net_may(n, g, ben, SUA_NET.get((n, ben)))
            w = r['w']; ov = w.copy()
            if im is None: im = Image.new('RGBA', KHUNG, (255, 0, 255, 255))
            for k, mau in (('toc', [40, 80, 255]), ('mat', [30, 200, 60]), ('may', [255, 30, 30]), ('nho', [255, 120, 0])): ov[r[k]] = ov[r[k]] * 0.4 + np.array(mau) * 0.6
            a_ = Image.fromarray(np.concatenate([w, ov], axis=0).clip(0, 255).astype('uint8'))
            row = Image.new('RGB', (a_.width + 2 * 330, a_.height), 'white'); row.paste(a_, (0, 0))
            for j, nen in enumerate([(238, 205, 172), (150, 102, 70)]):
                bg = Image.new('RGBA', im.size, nen + (255,)); bg.alpha_composite(im); row.paste(bg.convert('RGB').resize((320, 144), Image.LANCZOS), (a_.width + 6 + j * 326, 8))
                bg = Image.new('RGBA', im.size, nen + (255,)); bg.alpha_composite(im); row.paste(bg.convert('RGB').resize((78, 35), Image.LANCZOS), (a_.width + 6 + j * 326, 170))
            cells.append((n, row))
    w, h = cells[0][1].size; sh = Image.new('RGB', (2 * (w + 8), 5 * (h + 18)), 'white'); d = ImageDraw.Draw(sh)
    for i, (n, c) in enumerate(cells):
        x = (i % 2) * (w + 8); y = (i // 2) * (h + 18); sh.paste(c, (x, y + 14)); d.text((x + 2, y + 1), n, fill=(0, 0, 0))
    sh.save(f'../soat-net-{g}.png'); print(sh.size)
