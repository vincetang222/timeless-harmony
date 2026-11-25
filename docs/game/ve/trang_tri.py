# Trang trí theo lớp (bước thử): từ ảnh mô hình trả về → nền trống, hình rời có bóng chân, mặt nạ đổi tông, hình thẻ.
# Chạy trong thư mục chứa nen-ho.png, nen-langque.png, cong-tron.png, ban-dai.png:   python3 trang_tri.py <thư mục bản chơi>
# Không gọi AI. Mọi con số neo, cỡ là số đo trên chính các ảnh này.
import json, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

DICH = sys.argv[1] if len(sys.argv) > 1 else '.'
ANH = os.path.join(DICH, 'anh'); TT = os.path.join(ANH, 'tt'); os.makedirs(TT, exist_ok=True)


def buoc(x, a, b):
    t = np.clip((x - a) / (b - a), 0, 1); return t * t * (3 - 2 * t)


# ---------- 1. Tách nền xanh dương ----------
def tach(path, d0=22, d1=78, giu_xanh=False, bo_xam_xanh=False):
    """Alpha theo khoảng cách màu tới màu nền thật (nền rất phẳng); viền thì gỡ màu nền lẫn vào (un-mix).
    giu_xanh: đồ có màu xanh dương thật (khi đó nên vẽ trên nền màu khác). bo_xam_xanh: xoá vệt tối ngả xanh mô hình để sót giữa chân ghế."""
    a = np.asarray(Image.open(path).convert('RGB')).astype(np.float32)
    k = a[..., 2] - np.maximum(a[..., 0], a[..., 1])
    bg = np.median(a[k > 125], 0)
    d = np.sqrt(((a - bg) ** 2).sum(2))
    al = np.clip((d - d0) / (d1 - d0), 0, 1)
    if bo_xam_xanh: al = al * (1 - buoc(k, 10, 26) * (1 - buoc(np.maximum(a[..., 0], a[..., 1]), 120, 165)))
    dac = Image.fromarray(((al > 0.5) * 255).astype('uint8'))
    mo = np.asarray(dac.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.MaxFilter(5))).astype(np.float32) / 255
    al = al * np.maximum(mo, (al > 0.98))                         # bỏ điểm lẻ giữa nền
    al[:4] = 0; al[-4:] = 0; al[:, :4] = 0; al[:, -4:] = 0        # mép ảnh mô hình trả về hay có một hàng sáng hơn
    A = np.maximum(al, 1e-3)[..., None]
    fg = np.clip((a - (1 - A) * bg) / A, 0, 255)
    if not giu_xanh:                                              # mô hình hay vẽ lá ngoài rìa nhuốm màu nền: xanh dương không được vượt xanh lá
        r, g, b = fg[..., 0], fg[..., 1], fg[..., 2]
        fg[..., 2] = np.minimum(b, np.where(g >= r, g - 0.10 * (g - r), np.maximum(r, g) + 3))
    im = Image.fromarray(np.dstack([fg, al * 255]).astype('uint8'), 'RGBA')
    dd = np.asarray(im)[..., 3] > 20; ys = np.nonzero(dd.sum(1) >= 12)[0]; xs = np.nonzero(dd.sum(0) >= 12)[0]
    box = (int(max(xs.min() - 6, 0)), int(max(ys.min() - 6, 0)), int(min(xs.max() + 6, im.size[0])), int(min(ys.max() + 6, im.size[1])))
    return im.crop(box)


# ---------- 2. Mặt nạ phần đổi tông ----------
def mat_na_hoa(im):
    """Cánh hoa trắng, kem. Hai mức: "hạt chắc" (màu rõ là cánh hoa) phải đủ dày mới thành mảng; trong mảng nhận cả điểm gần đúng (bóng, nếp).
    Nhờ vậy cỏ lau và khung vàng (chỉ lác đác vài điểm giống màu hoa) không bị nhuộm."""
    a = np.asarray(im).astype(np.float32); r, g, b, al = a[..., 0], a[..., 1], a[..., 2], a[..., 3]
    mn = np.minimum(np.minimum(r, g), b); la = buoc(g - np.maximum(r, b), 2, 10)
    chac = (mn > 130) & (r - g <= 17) & (r - b <= 60) & (g - np.maximum(r, b) < 4) & (al > 200)
    gan = buoc(mn, 96, 135) * (1 - buoc(r - g, 24, 31)) * (1 - buoc(r - b, 74, 90)) * (1 - la)
    day = np.asarray(Image.fromarray((chac * 255).astype('uint8')).filter(ImageFilter.BoxBlur(12))).astype(np.float32) / 255
    mang = Image.fromarray(((day > 0.42) * 255).astype('uint8')).filter(ImageFilter.MaxFilter(19)).filter(ImageFilter.GaussianBlur(2.5))
    w = gan * (np.asarray(mang).astype(np.float32) / 255) * (al / 255)
    return Image.fromarray(np.clip(w * 255, 0, 255).astype('uint8')).filter(ImageFilter.GaussianBlur(0.6))


def mat_na_vung(im, da_giac):
    """Vải khăn: gỗ sáng màu, đĩa và khăn có màu quá gần nhau nên không tách bằng màu được; khoanh tay vùng khăn (toạ độ trên hình rời đã cắt gọn),
    trong vùng đó lấy mọi điểm sáng (cả ly đứng trên khăn, vì nhìn xuyên ly là thấy khăn)."""
    a = np.asarray(im).astype(np.float32); mn = a[..., :3].min(2); al = a[..., 3]
    v = Image.new('L', im.size, 0); d = ImageDraw.Draw(v)
    for p in da_giac: d.polygon(p, fill=255)
    v = np.asarray(v.filter(ImageFilter.GaussianBlur(1.5))).astype(np.float32) / 255
    return Image.fromarray(np.clip(buoc(mn, 96, 132) * v * (al / 255) * 255, 0, 255).astype('uint8'))


# ---------- 3. Bóng chạm đất, nướng sẵn vào hình rời ----------
def co_bong(im, tu=0.5, mo=0.022, do=0.36, xuong=0.012, le=None):
    """Bóng = phần dưới của hình bóng vật (từ tỉ lệ chiều cao `tu` trở xuống), làm mờ, dời xuống một chút. Màu tối ngả lục để hợp cỏ, cát, gạch.
    Bóng nằm ngay dưới vật (gần như không lệch ngang) nên lật gương vẫn dùng được."""
    w, h = im.size; le = le if le is not None else int(w * mo * 2.2)
    al = np.asarray(im)[..., 3].astype(np.float32) / 255
    y = np.arange(h)[:, None] / h; chan = al * buoc(y, tu - 0.12, tu + 0.05)
    to = Image.new('L', (w + 2 * le, h + le), 0); to.paste(Image.fromarray((chan * 255).astype('uint8')), (le, int(h * xuong)))
    b = np.asarray(to.filter(ImageFilter.GaussianBlur(w * mo))).astype(np.float32) / 255
    b = np.clip(b * 1.7, 0, 1) * do
    lop = Image.fromarray(np.dstack([np.full(b.shape, 22), np.full(b.shape, 40), np.full(b.shape, 22), b * 255]).astype('uint8'), 'RGBA')
    lop.alpha_composite(im, (le, 0))
    return lop, le


def luu_roi(ten, im, mn, rong, pxm_goc, ax_goc, ay_goc, bong):
    """Thu nhỏ, thêm bóng, lưu hình rời + mặt nạ + hình thẻ. Trả về số đo để bản chơi đặt vào cảnh."""
    k = rong / im.size[0]; s = im.resize((rong, round(im.size[1] * k)), Image.LANCZOS); m = mn.resize(s.size, Image.LANCZOS)
    co, le = co_bong(s, **bong); mm = Image.new('L', co.size, 0); mm.paste(m, (le, 0))
    co.save(os.path.join(TT, ten + '.webp'), quality=86, method=6)
    Image.merge('RGB', (mm, mm, mm)).save(os.path.join(TT, ten + '-mn.webp'), quality=70, method=6)
    # hình thẻ 320×240 trên nền kính sáng
    t = Image.new('RGBA', (320, 240), (236, 240, 228, 255)); q = min(292 / s.size[0], 216 / s.size[1]); z = s.resize((round(s.size[0] * q), round(s.size[1] * q)), Image.LANCZOS)
    t.alpha_composite(z, ((320 - z.size[0]) // 2, (240 - z.size[1]) // 2)); t.convert('RGB').save(os.path.join(TT, 't-' + ten + '.webp'), quality=80, method=6)
    W, H = co.size
    return {'f': 'anh/tt/' + ten + '.webp', 'mn': 'anh/tt/' + ten + '-mn.webp', 'the': 'anh/tt/t-' + ten + '.webp', 'w': W, 'h': H,
            'pxm': round(pxm_goc * k, 2), 'ax': round((le + ax_goc * s.size[0]) / W, 4), 'ay': round(ay_goc * s.size[1] / H, 4)}


if __name__ == '__main__':
    # nền trống: cỡ như các cảnh khác (1600 và 900 px), hình thẻ cắt vùng giữa
    for ten in ('nen-ho', 'nen-langque'):
        if not os.path.exists(ten + '.png'): continue
        nen = Image.open(ten + '.png').convert('RGB')
        nen.resize((1600, 889), Image.LANCZOS).save(os.path.join(ANH, ten + '.webp'), quality=82, method=6)
        nho = nen.resize((900, 500), Image.LANCZOS); nho.save(os.path.join(ANH, ten + '-m.webp'), quality=80, method=6)
        w, h = nho.size; cw = w / 2.5; chh = cw * 10 / 16; x0 = (w - cw) * 0.5; y0 = (h - chh) * 0.45
        nho.crop((round(x0), round(y0), round(x0 + cw), round(y0 + chh))).resize((320, 200), Image.LANCZOS).save(os.path.join(ANH, 't-' + ten + '.webp'), quality=76, method=6)

    so = {}
    # cổng tròn: vòng rộng 950 px trong hình rời = 2,7 m; tâm vòng ở 56,2% bề ngang; mép dưới đế ở 95,1% chiều cao
    cong = tach('cong-tron.png')
    so['cong-tron'] = luu_roi('cong-tron', cong, mat_na_hoa(cong), 700, 950 / 2.7, 0.562, 0.951, dict(tu=0.93, mo=0.02, do=0.34, xuong=0.006))
    so['cong-tron'].update(goc=[250, 246, 232])
    # bàn dài: ghế gần nhất cao 584 px trong hình rời ≈ 1,0 m (gồm cả phần thấy mặt ghế do nhìn từ trên xuống); chân gần nhất ở 98,5% chiều cao
    ban = tach('ban-dai.png', bo_xam_xanh=True)
    KHAN = [[(212, 93), (400, 80), (600, 131), (900, 206), (1100, 261), (1304, 318), (1304, 528), (1078, 562), (1070, 376), (900, 307), (700, 247), (550, 204), (400, 156), (212, 113)],
            [(231, 183), (302, 183), (305, 324), (233, 324)]]   # khăn chạy bàn trên mặt bàn và phần rủ đầu gần; phần rủ đầu xa
    so['ban-dai'] = luu_roi('ban-dai', ban, mat_na_vung(ban, KHAN), 820, 584 / 1.0, 0.5, 0.985, dict(tu=0.55, mo=0.022, do=0.4, xuong=0.02))
    so['ban-dai'].update(goc=[246, 234, 204])
    json.dump(so, open('tt.json', 'w'), ensure_ascii=False, indent=1)   # số đo để chép vào TT trong index.html của bản chơi
    for k, v in so.items(): print(k, v)
    print('tệp:', {f: os.path.getsize(os.path.join(TT, f)) // 1024 for f in sorted(os.listdir(TT))}, 'KB | nền:', {f: os.path.getsize(os.path.join(ANH, f)) // 1024 for f in sorted(os.listdir(ANH)) if 'nen-' in f}, 'KB')
