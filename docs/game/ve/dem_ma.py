# Thử làm bản đêm của nền trống bằng mã (0 lượt), ngày 25/11: thay tấm T6 (Vườn Hồ ban đêm) nếu trông đủ thật.
# Không xê dịch cảnh (đạt tiêu chí "cảnh xê dịch không quá 1%" của T6 một cách tự nhiên).
# Các bước: tách trời theo màu và vị trí → thay bằng trời đêm (dải màu, mây tối viền trăng, sao); phần còn lại tô tối ngả lam;
# đèn ấm trên các trụ lan can và đèn làng xa bên kia hồ, có vệt phản chiếu trên mặt nước. Toạ độ đèn đo tay trên nền Vườn Hồ 1600×889.
# Chạy: python3 dem_ma.py <nen-ho.webp>   → dem-ma.jpg (ngày | đêm) và nen-ho-dem.webp
import sys
import numpy as np
from PIL import Image, ImageFilter, ImageDraw, ImageFont

src = Image.open(sys.argv[1] if len(sys.argv) > 1 else 'nen-ho.webp').convert('RGB')
a = np.asarray(src).astype(np.float32) / 255
H, W = a.shape[:2]
r, g, b = a[..., 0], a[..., 1], a[..., 2]
yy, xx = np.mgrid[:H, :W].astype(np.float32)


def buoc(x, a_, b_): t = np.clip((x - a_) / (b_ - a_), 0, 1); return t * t * (3 - 2 * t)


# 1. Trời: xanh nhạt hoặc mây kem, không phải lá cây (lá: lục trội), ở nửa trên; làm mượt rồi lấp lỗ
la = (g > r + 0.02) & (g > b - 0.02) & (g - b > -0.02) & ~((b > g) & (b > r))
troi = ((b >= r - 0.03) | ((r + g + b) / 3 > 0.78)) & ~((g > r + 0.03) & (g > b + 0.03)) & (yy < 0.47 * H)
troi = np.asarray(Image.fromarray((troi * 255).astype('uint8')).filter(ImageFilter.MedianFilter(7)).filter(ImageFilter.GaussianBlur(1.2))).astype(np.float32) / 255
lum = 0.3 * r + 0.59 * g + 0.11 * b
may = buoc(-(b - r), -0.12, 0.14)                                   # mây kem: đỏ trội hơn lam; trời: lam trội (đo trên nền: trời b−r ≈ +46, mây ≈ −50)
may = np.asarray(Image.fromarray((may * 255).astype('uint8')).filter(ImageFilter.GaussianBlur(1.5))).astype(np.float32) / 255
# 2. Trời đêm: dải màu từ xanh thẫm xuống lam tím ở chân trời; mây giữ khối sáng tối của tranh gốc, đổi sang xám lam ánh trăng
t = yy / (0.47 * H)
tren, duoi = np.array([0.03, 0.05, 0.13]), np.array([0.13, 0.17, 0.30])
nen_troi = tren + (duoi - tren) * (t[..., None] ** 1.4)
s_may = buoc(lum, 0.72, 0.97)[..., None]
mau_may = np.array([0.09, 0.11, 0.19]) * (1 - s_may) + np.array([0.40, 0.44, 0.57]) * s_may
troi_dem = nen_troi * (1 - may[..., None]) + mau_may * may[..., None]
rng = np.random.RandomState(3)
sao = np.zeros((H, W), np.float32); n = 420
sy, sx = rng.randint(0, int(0.42 * H), n), rng.randint(0, W, n); sao[sy, sx] = rng.uniform(0.35, 1.0, n)
sao = np.asarray(Image.fromarray((sao * 255).astype('uint8')).filter(ImageFilter.GaussianBlur(0.6))).astype(np.float32) / 255 * 2.2
troi_dem += (sao * (1 - may) * troi)[..., None] * np.array([0.9, 0.92, 1.0])
# 3. Phần còn lại: tô tối ngả lam (ánh trăng), giữ tương phản
dem = (a ** 1.25) * np.array([0.30, 0.36, 0.55]) + np.array([0.01, 0.015, 0.035])
out = dem * (1 - troi[..., None]) + troi_dem * troi[..., None]
# 4. Đèn: trụ lan can (đèn ấm trên chậu đá) và đèn làng xa
DEN_LAN_CAN = [(465, 533), (717, 535), (886, 535), (1130, 530)]
DEN_XA = [(x, 0) for x in (380, 430, 470, 520, 990, 1040, 1080, 1150, 1210, 1260)]
anh = np.zeros((H, W, 3), np.float32)


def cham(x, y, ban_kinh, mau, manh):
    d2 = (xx - x) ** 2 + (yy - y) ** 2
    anh[...] += np.exp(-d2 / (2 * ban_kinh ** 2))[..., None] * np.array(mau) * manh


for x, y in DEN_LAN_CAN:
    cham(x, y - 6, 3.0, (1.0, 0.85, 0.55), 1.2); cham(x, y, 26, (1.0, 0.65, 0.3), 0.35)
# bờ hồ xa: lấy đường bờ là hàng đầu tiên có nước (lam trội) dưới đồi, ở mỗi cột
for x, _ in DEN_XA:
    col = (b[:, x] > g[:, x]) & (b[:, x] > r[:, x] + 0.05)
    ys = np.nonzero(col[int(0.4 * H):int(0.6 * H)])[0]
    if not len(ys): continue
    y = int(0.4 * H) + ys[0] - 2
    cham(x, y, 1.4, (1.0, 0.8, 0.45), 1.3); cham(x, y, 7, (1.0, 0.6, 0.3), 0.18)
    # vệt phản chiếu trên mặt hồ
    for k in range(1, 26):
        cham(x + rng.uniform(-1.5, 1.5), y + 3 + k * 2.2, 1.2 + k * 0.05, (1.0, 0.7, 0.4), 0.22 * (1 - k / 26))
out = 1 - (1 - np.clip(out, 0, 1)) * (1 - np.clip(anh, 0, 1))      # cộng ánh đèn kiểu "screen"
dem_im = Image.fromarray((np.clip(out, 0, 1) * 255).astype('uint8'))

if __name__ == '__main__':
    dem_im.save('nen-ho-dem.webp', quality=86)
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 20)
    w2, h2 = W // 2, H // 2
    G = Image.new('RGB', (w2 * 2 + 30, h2 + 50), (236, 240, 228)); d = ImageDraw.Draw(G)
    for i, (ten, im) in enumerate([('Nền trống Vườn Hồ (vẽ tay)', src), ('Bản đêm bằng mã (thay T6)', dem_im)]):
        x0 = 10 + i * (w2 + 10); G.paste(im.resize((w2, h2), Image.LANCZOS), (x0, 40)); d.text((x0 + 4, 10), ten, fill=(18, 38, 28), font=font)
    G.save('dem-ma.jpg', quality=88)
    # hệ số chỉnh sáng cho món rời: tỉ lệ màu ở lối đi đá (khăn trắng chưa có trong nền trống)
    loi = (slice(int(0.78 * H), int(0.95 * H)), slice(int(0.44 * W), int(0.56 * W)))
    print('xong; hệ số chỉnh sáng món rời (đo trên lối đi đá):', (np.asarray(dem_im).astype(np.float32)[loi].mean((0, 1)) / (a[loi].mean((0, 1)) * 255)).round(3))
