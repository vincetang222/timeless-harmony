# Thử trang trí ghế theo lớp bằng mã (0 lượt vẽ), ngày 25/11, trên cùng bàn tròn của khan_lop.py.
# Lớp ghế: khung (đổi màu: vàng đồng, đen mờ, bạc, gỗ óc chó) · đệm (đổi màu theo khăn) · đai vải quấn lưng ghế, thắt nút rủ đuôi
# (vẽ bằng mã theo hai cột lưng ghế đo tay). Nơ to, hoa, quạt giấy… vẫn phải vẽ (loại C, xem bang-ve.md mục 3.4).
# Chạy: python3 ghe_lop.py   → ghe-lop.jpg (dùng cùng ảnh mẫu với khan_lop.py; số đo lưng ghế là của riêng tấm đó)
import sys, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import khan_lop as K
from hoa_van import mau

a = K.a; H, W = K.H, K.W
r, g, b = a[..., 0], a[..., 1], a[..., 2]
HOP_GHE = K.GHE_HOP + [(196, 66, 284, 140), (438, 66, 528, 140)]        # thêm hai ghế phía sau bàn
trong = np.zeros((H, W), bool)
for x0, y0, x1, y1 in HOP_GHE: trong[y0:y1, x0:x1] = True
co = ((g > r + 2) & (g > b + 18)) | ((g - b > 44) & (r - g < 6)) | (g - b > 75)   # cỏ, cả cỏ nắng vàng (ghế kem: đỏ nhỉnh hơn lục)
KHUNG = trong & (K.MN < 0.3) & (K.MD < 0.3) & ~co & (a.mean(2) > 90) & ~(K.o_mat & ((r - b) < 28))   # đĩa trắng trên bàn không phải ghế
MK = np.asarray(Image.fromarray((KHUNG * 255).astype('uint8')).filter(ImageFilter.GaussianBlur(0.6))).astype(np.float32)[..., None] / 255
GOC_K = np.percentile(a[KHUNG], 85, axis=0)


def to_khung(im, tong):
    x = np.asarray(im).astype(np.float32); q = np.minimum(1.06, x / GOC_K)
    lt = (0.299 * tong[0] + 0.587 * tong[1] + 0.114 * tong[2]) / 255
    c = np.minimum(255, q ** (1 + (1 - lt) * 1.6) * np.array(tong, np.float32))
    return Image.fromarray(np.clip(x * (1 - MK) + c * MK, 0, 255).astype('uint8'))


# Lưng hai ghế phía trước (nhìn từ sau): cột trái và cột phải ở độ cao đặt đai, đo tay trên ảnh cắt
LUNG = [dict(trai=(151, 247), phai=(219, 252), day=11, cot=(150, 156, 214, 221)),
        dict(trai=(435, 268), phai=(522, 272), day=12, cot=(430, 438, 517, 526))]


def dai(im, mau_dai, kieu='nut'):
    """Đai vải quấn ngang lưng ghế; giữa lưng thắt nút, hai đuôi rủ xuống. Vẽ ở 3× rồi thu nhỏ cho mịn."""
    S = 3; big = im.resize((W * S, H * S), Image.LANCZOS); lop = Image.new('RGBA', big.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lop)
    c = np.array(mau_dai, np.float32)
    sang = tuple(int(v) for v in np.minimum(255, c * 1.16 + 12)); toi = tuple(int(v) for v in c * 0.62); vien = tuple(int(v) for v in c * 0.45)
    for L in LUNG:
        (x0, y0), (x1, y1), h = L['trai'], L['phai'], L['day']
        P = lambda x, y: (x * S, y * S)
        # dải ngang, hơi cong võng xuống giữa
        tren = [(x0 + (x1 - x0) * t, y0 + (y1 - y0) * t + 2.0 * np.sin(np.pi * t)) for t in np.linspace(0, 1, 24)]
        duoi = [(x, y + h) for x, y in tren][::-1]
        d.polygon([P(*p) for p in tren + duoi], fill=tuple(int(v) for v in c) + (255,), outline=vien + (255,), width=S)
        d.line([P(x, y + 2) for x, y in tren], fill=sang + (170,), width=2 * S)                       # mép trên bắt sáng
        d.line([P(x, y + h - 2) for x, y in tren], fill=toi + (150,), width=2 * S)                    # mép dưới tối
        cx = (x0 + x1) / 2; cy = (y0 + y1) / 2 + 2 + h / 2
        # hai đuôi rủ, đầu cắt chữ V
        for s_, dx in ((-1, -7), (1, 8)):
            dd = 64 if kieu == 'nut' else 40
            ql = [(cx + s_ * 2, cy), (cx + s_ * 9, cy), (cx + dx + s_ * 6, cy + dd), (cx + dx + s_ * 1, cy + dd - 5), (cx + dx - s_ * 4, cy + dd)]
            d.polygon([P(*p) for p in ql], fill=tuple(int(v) for v in c * 0.9) + (255,), outline=vien + (255,), width=S)
            d.line([P(cx + s_ * 5, cy + 3), P(cx + dx + s_ * 2, cy + dd - 8)], fill=toi + (120,), width=S)
        if kieu == 'no':   # nơ bướm: hai quai tròn
            for s_ in (-1, 1):
                d.ellipse([P(cx + s_ * 3 - 9, cy - 9), P(cx + s_ * 3 + 9 + s_ * 6, cy + 7)], fill=tuple(int(v) for v in c) + (255,), outline=vien + (255,), width=S)
                d.arc([P(cx + s_ * 6 - 5, cy - 5), P(cx + s_ * 6 + 5 + s_ * 4, cy + 3)], 200, 340, fill=toi + (200,), width=S)
        d.ellipse([P(cx - 5, cy - 5), P(cx + 5, cy + 6)], fill=tuple(int(v) for v in c * 0.95) + (255,), outline=vien + (255,), width=S)   # nút
        d.arc([P(cx - 3, cy - 3), P(cx + 3, cy + 3)], 200, 320, fill=sang + (220,), width=S)
    big = big.convert('RGBA'); big.alpha_composite(lop)
    return big.resize((W, H), Image.LANCZOS).convert('RGB')


if __name__ == '__main__':
    TRANG = K.tron_((248, 246, 238))
    MAU = [
        ('Sảnh tiệc Việt: ghế vàng đồng, đệm đỏ, đai đỏ thắt nút', [(K.ca_ban, K.tron_((150, 30, 36)), 1), (K.vuong(1.12), lambda u, v: K.p_gam(u, v), 1)], (150, 30, 36), (196, 156, 80), ((150, 30, 36), 'nut')),
        ('Hiện đại: ghế đen mờ, đệm trắng, đai bạc', [(K.ca_ban, K.tron_((34, 44, 70)), 1), (K.vuong_cheo(1.4), lambda u, v: K.p_kimsa(u, v, (200, 204, 210)), 1)], (240, 238, 232), (44, 44, 48), ((196, 200, 206), 'nut')),
        ('Lãng mạn: ghế trắng, đệm hồng, nơ voan hồng', [(K.ca_ban, K.tron_((226, 182, 178)), 1), (K.tron_hinh(1 + 0.42 * K.L_RU), lambda u, v: K.p_kimsa(u, v, (214, 186, 140)), 1)], (226, 182, 178), (246, 244, 238), ((236, 190, 190), 'no')),
        ('Vườn mộc: ghế gỗ óc chó, đệm xanh xô thơm', [(K.ca_ban, K.tron_((150, 170, 140)), 1), (K.vuong_cheo(1.42), lambda u, v: K.p_ren(u, v, (238, 234, 222), (254, 253, 250)), 1)], (150, 170, 140), (112, 76, 50), None),
    ]
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 22)
    SC = 0.86; tw, th_ = int(W * SC), int(H * SC)
    G = Image.new('RGB', (tw * 2 + 30, (th_ + 40) * 2 + 20), (236, 240, 228)); d = ImageDraw.Draw(G)
    for i, (ten, lop, dm, khung, d_) in enumerate(MAU):
        im = to_khung(K.ve(lop, dm), khung)
        if d_: im = dai(im, *d_)
        x0 = 10 + (i % 2) * (tw + 10); y0 = 10 + (i // 2) * (th_ + 40)
        G.paste(im.resize((tw, th_), Image.LANCZOS), (x0, y0 + 34)); d.text((x0 + 4, y0 + 5), f'{i + 1}. {ten}', fill=(18, 38, 28), font=font)
    G.save('ghe-lop.jpg', quality=86)
    print('xong', G.size, 'GOC khung', GOC_K.round())
