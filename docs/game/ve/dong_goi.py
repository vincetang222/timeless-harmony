# Đóng gói tranh cho bản chơi: gom mảnh nhỏ thành tấm ghép để trình duyệt tải ít tệp.
#   manh-{gt}.webp : mọi mảnh mắt, lông mày (trước đây 84 tệp rời)
#   nho-{gt}.webp  : mọi đầu, thân, cổ áo ở cỡ nhỏ, dùng cho thẻ hình và lúc tranh nét chưa tải xong
#   manh.json      : vị trí từng ô trong tấm ghép, vị trí mắt và lông mày trên từng đầu
# Chạy: python3 dong_goi.py <thư mục đích>   (đọc out2/ và out3/)
import sys, os, json, glob, shutil
from PIL import Image
DICH = sys.argv[1]; NV = os.path.join(DICH, 'nv'); ANH = os.path.join(DICH, 'anh'); os.makedirs(NV, exist_ok=True)
meta = json.load(open('out2/meta.json')); manh = json.load(open('out2/manh.json')); moi = json.load(open('out3/may_moi.json'))
TN = 0.18
def mo(f):
    p = f'out3/{f}.webp'
    return Image.open(p if os.path.exists(p) else f'out2/{f}.webp').convert('RGBA')
def xep(ds, rong_toi_da):   # xếp các ô thành hàng, trả về kích thước và vị trí
    x = y = cao = 0; vt = {}; W = 0
    for ten, w, h in ds:
        if x + w > rong_toi_da: x = 0; y += cao + 2; cao = 0
        vt[ten] = [x, y, w, h]; x += w + 2; cao = max(cao, h); W = max(W, x)
    return W, y + cao, vt
kq = {}
for g in ['nam', 'nu']:
    m = meta[g]; M = manh[g]; out = {'vitri': M['vitri'], 'manh': {'mat': {}, 'may': {}}}
    # ---- tấm mảnh mắt, lông mày ----
    o = []
    def them(nhom, d, thu_muc):
        for face in d:
            for kind in d[face]:
                for ben, p in enumerate(d[face][kind]):
                    im = Image.open(f"{thu_muc}/{p['f']}.{'png' if thu_muc.endswith('manh') else 'webp'}").convert('RGBA')
                    o.append((nhom, face, kind, ben, im))
    them('mat', M['manh']['mat'], 'out2'); them('may', M['manh']['may'], 'out2')
    if 'mayA' in moi[g]: them('mayA', moi[g]['mayA'], 'out3/manh'); out['mayA'] = {}; out['vitriA'] = moi[g]['vitriA']
    # mayS (lông mày cô dâu bỏ lọn tóc) đã thử nhưng làm đứt lông mày, không dùng; cô dâu giữ mảnh của bản 13
    W, H, vt = xep([(i, im.width, im.height) for i, (_, _, _, _, im) in enumerate(o)], 600)
    tam = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    for i, (nhom, face, kind, ben, im) in enumerate(o):
        x, y, w, h = vt[i]; tam.paste(im, (x, y))
        goc = out['manh'][nhom] if nhom in ('mat', 'may') else out[nhom]
        goc.setdefault(face, {}).setdefault(kind, [None, None])[ben] = {'x': x, 'y': y, 'w': w, 'h': h}
    tam.save(f'{NV}/manh-{g}.webp', quality=92, method=6, exact=True); out['tam'] = f'manh-{g}'
    # ---- tấm cỡ nhỏ ----
    ds = []
    def nho(f, cat=1.0):
        im = mo(f)
        if cat < 1: im = im.crop((0, 0, im.width, round(im.height * cat)))
        return im.resize((max(1, round(im.width * TN)), max(1, round(im.height * TN))), Image.LANCZOS)
    for n in m['dau']: ds.append(('dau-' + n, nho('dau-' + n)))
    than = sorted(os.path.basename(p)[:-5] for p in glob.glob(f'out2/than-{g}-*.webp')) + sorted(os.path.basename(p)[:-5] for p in glob.glob(f'out2/ad-{g}-*.webp'))
    for n in than: ds.append((n, nho(n)))
    for n in sorted(os.path.basename(p)[:-5] for p in glob.glob(f'out2/co-ad-{g}-*.webp')): ds.append((n, nho(n, 0.34)))
    W, H, vt = xep([(n, im.width, im.height) for n, im in ds], 1700)
    tam = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    for n, im in ds: tam.paste(im, tuple(vt[n][:2]))
    tam.save(f'{NV}/nho-{g}.webp', quality=80, method=6); out['nho'] = {'f': f'nho-{g}', 'ti': TN, 'o': vt}
    kq[g] = out
    # ---- tranh nét: chép nguyên ----
    for n in ['dau-' + x for x in m['dau']] + than + [os.path.basename(p)[:-5] for p in glob.glob(f'out2/co-ad-{g}-*.webp')]:
        src = f'out3/{n}.webp' if os.path.exists(f'out3/{n}.webp') else f'out2/{n}.webp'; shutil.copyfile(src, f'{NV}/{n}.webp')
    print(g, 'manh', os.path.getsize(f'{NV}/manh-{g}.webp') // 1024, 'KB; nho', tam.size, os.path.getsize(f'{NV}/nho-{g}.webp') // 1024, 'KB', flush=True)
json.dump(kq, open(f'{NV}/manh.json', 'w'), separators=(',', ':'))
for p in glob.glob(f'{NV}/mat-*.webp') + glob.glob(f'{NV}/may-*.webp'): shutil.move(p, p.replace('/nv/', '/_bo/')) if os.path.isdir(os.path.join(DICH, '_bo')) else os.remove(p)
print('manh.json', os.path.getsize(f'{NV}/manh.json') // 1024, 'KB; tep trong nv:', len(os.listdir(NV)))
# ---- hình người phục vụ: thu nhỏ một nửa (trên màn hình chỉ cao chừng 90–180 điểm) ----
for n in ['mc-b', 'ban-nhac-b', 'tho-anh-b']:
    goc = f'{ANH}/{n}.webp'; luu = f'goc-anh/{n}.webp'; os.makedirs('goc-anh', exist_ok=True)
    if not os.path.exists(luu): shutil.copyfile(goc, luu)
    im = Image.open(luu).convert('RGBA'); im = im.resize((im.width // 2, im.height // 2), Image.LANCZOS); im.save(goc, quality=82, method=6)
    print(n, im.size, os.path.getsize(goc) // 1024, 'KB')
# ---- hình thẻ địa điểm, gói: cắt vùng giữa của tranh nền cỡ nhỏ ----
tong = 0
for p in sorted(glob.glob(f'{ANH}/*-m.webp')):
    im = Image.open(p).convert('RGB'); w, h = im.size; cw = w / 2.5; chh = cw * 10 / 16; x0 = (w - cw) * 0.5; y0 = (h - chh) * 0.45
    t = im.crop((round(x0), round(y0), round(x0 + cw), round(y0 + chh))).resize((320, 200), Image.LANCZOS)
    f = os.path.join(ANH, 't-' + os.path.basename(p)[:-7] + '.webp'); t.save(f, quality=76, method=6); tong += os.path.getsize(f)
print('the dia diem:', len(glob.glob(f'{ANH}/t-*.webp')), 'tep', tong // 1024, 'KB')
