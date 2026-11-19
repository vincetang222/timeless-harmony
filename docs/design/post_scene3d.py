"""Hậu kỳ cho cảnh nền 3D: sương xa theo khoảng cách, quầng sáng, tông màu AgX, rồi xuất WebP vào assets/bg/,
kèm mặt nạ cho pháo hoa chuyển động (fireworks.js).

    python post_scene3d.py .build/day-land.exr --mode day --frame land
    python post_scene3d.py .build/night-port.exr --mode night --frame port

Đầu vào là tệp EXR nhiều lớp do build_scene3d.py dựng (màu tuyến tính + kênh độ sâu + chỉ số vật thể).
Sau khi xuất xong cả bốn khung hình, chạy `node docs/design/build_glass.js` để dựng lại kính làm mờ sẵn.
"""
import argparse
import math
import os

import bpy
import numpy as np
import OpenEXR
from PIL import Image
from scipy.ndimage import gaussian_filter

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
ap = argparse.ArgumentParser()
ap.add_argument("src")
ap.add_argument("--mode", default="day", choices=["day", "night"])
ap.add_argument("--frame", default="land", choices=["land", "port"])
ap.add_argument("--png", default=None, help="giữ lại bản PNG không nén (mặc định: cạnh tệp EXR)")
ap.add_argument("--webp", default=None, help="mặc định: assets/bg/lake-<mode>[-m].webp")
ap.add_argument("--quality", type=int, default=None)
ap.add_argument("--no-mask", action="store_true", help="không xuất mặt nạ pháo hoa")
ap.add_argument("--exposure", type=float, default=None, help="số stop; bỏ trống = mức đã cân sẵn")
ap.add_argument("--stats", action="store_true")
A = ap.parse_args()
NIGHT = A.mode == "night"
PNG = A.png or os.path.splitext(A.src)[0] + ".png"
WEBP = A.webp or os.path.join(ROOT, "assets", "bg", "lake-%s%s.webp" % (A.mode, "-m" if A.frame == "port" else ""))

f = OpenEXR.File(A.src)
ch = {}
for part in f.parts:
    ch.update(part.channels)
names = list(ch)
rgb = np.asarray(ch[[k for k in names if k.endswith("Combined")][0]].pixels, np.float32)[..., :3]
depth = np.asarray(ch[[k for k in names if "Depth" in k][0]].pixels, np.float32)
index = [k for k in names if "Object Index" in k or "IndexOB" in k]
index = np.asarray(ch[index[0]].pixels, np.float32) if index else None
H, W = rgb.shape[:2]
sky = depth > 1e9
lum = lambda a: a @ np.array([0.2126, 0.7152, 0.0722], np.float32)
if A.stats:
    print("channels", names, "size", W, H)
    print("mean rgb", rgb.reshape(-1, 3).mean(0), "sky mean", rgb[sky].mean(0) if sky.any() else None, "lum p50/p90/p99", np.percentile(lum(rgb), [50, 90, 99]))
    print("depth pcts", np.percentile(depth[~sky], [1, 25, 50, 75, 99]) if (~sky).any() else None)

# 1. sương xa (màu cố định theo chế độ, không lấy từ ảnh để khỏi dính màu pháo bông)
haze_col = np.array([9.5, 12.6, 16.4], np.float32) if not NIGHT else np.array([0.016, 0.028, 0.062], np.float32)
D = 40000.0 if not NIGHT else 60000.0
fog = 1 - np.exp(-np.minimum(depth, 1e6) / D)
fog = np.where(sky, 0, fog)[..., None] * (0.92 if not NIGHT else 0.8)
rgb = rgb * (1 - fog) + haze_col * fog

# 1b. màu đậm hơn một chút
sat = 1.14 if not NIGHT else 1.10
rgb = np.maximum(lum(rgb)[..., None] * (1 - sat) + rgb * sat, 0)

# 1c. độ sâu trường ảnh: lấy nét ở cổng hoa, tiền cảnh (cỏ, hàng ghế gần) mềm dần như ảnh chụp ống kính mở lớn.
#     Vừa cho cảm giác chiều sâu, vừa giúp tệp WebP nhẹ hơn (bãi cỏ sắc nét rất tốn dung lượng).
s = (W * H / ((2000.0 * 1250.0) if A.frame == "land" else (900.0 * 1950.0))) ** 0.5     # tỉ lệ so với cỡ xuất chuẩn
FOCUS, DOF = 31.0, 62.0
coc = DOF * s * np.clip(1.0 / np.maximum(depth, 1.0) - 1.0 / FOCUS, 0, None)             # độ nhoè (px) theo khoảng cách
coc = gaussian_filter(np.minimum(coc, 8.0 * s), 1.5 * s)
levels = [0.0, 1.2 * s, 2.6 * s, 5.0 * s, 8.0 * s]
stack = [rgb] + [np.stack([gaussian_filter(rgb[..., c], sg) for c in range(3)], -1) for sg in levels[1:]]
out = np.zeros_like(rgb)
for i in range(len(levels) - 1):
    t = np.clip((coc - levels[i]) / (levels[i + 1] - levels[i]), 0, 1)
    m = ((coc >= levels[i]) & (coc < levels[i + 1]))[..., None]
    out += m * (stack[i] * (1 - t[..., None]) + stack[i + 1] * t[..., None])
out += (coc >= levels[-1])[..., None] * stack[-1]
rgb = out

# 2. phơi sáng
gain = (0.075 if not NIGHT else 1.0) if A.exposure is None else 2.0 ** A.exposure
rgb = rgb * gain
if A.stats:
    print("gain", gain, "haze", haze_col)

# 3. quầng sáng (pháo bông, đèn, ánh nắng trên mặt nước)
thr = 2.2 if not NIGHT else 0.9
bright = np.maximum(rgb - thr, 0)
bright = bright / (1 + lum(bright)[..., None] * 0.08)
glow = sum(w * np.stack([gaussian_filter(bright[..., c], sg * s) for c in range(3)], -1)
           for sg, w in ((3, 0.30), (9, 0.26), (26, 0.22), (70, 0.16)))
rgb = rgb + glow * (0.30 if not NIGHT else 0.85)

# 4. tông màu AgX của Blender rồi lưu PNG
img = bpy.data.images.new("post", W, H, alpha=False, float_buffer=True)
img.colorspace_settings.name = "Linear Rec.709"
buf = np.concatenate([rgb[::-1], np.ones((H, W, 1), np.float32)], -1)
img.pixels.foreach_set(buf.ravel())
sc = bpy.context.scene
sc.view_settings.view_transform = "AgX"
try:
    sc.view_settings.look = "AgX - Medium High Contrast" if not NIGHT else "AgX - High Contrast"
except TypeError as e:
    print("look:", str(e)[:160])
sc.render.image_settings.file_format = "PNG"
sc.render.image_settings.color_mode = "RGB"
sc.render.image_settings.color_depth = "8"
sc.render.image_settings.compression = 20
img.save_render(os.path.abspath(PNG), scene=sc)

# 5. WebP cho website. Người xem có thể bấm "Ngắm cảnh" để nhìn trọn ảnh, nên giữ chất lượng khá cao.
q = A.quality or (80 if A.frame == "land" else 82)
Image.open(PNG).convert("RGB").save(WEBP, "WEBP", quality=q, method=6)
print("saved %s (%d KB, %dx%d, q%d)" % (os.path.relpath(WEBP, ROOT), os.path.getsize(WEBP) // 1024, W, H, q))

# 6. Mặt nạ cho pháo hoa chuyển động. Pháo bắn lên từ sau cổng hoa (FIRE_O trong build_scene3d.py), nên mọi thứ đứng
#    gần máy ảnh hơn phải che được nó. Kênh đỏ = vật che (vườn, cổng hoa, cây, khách, lan can); kênh lục = mặt hồ
#    (nơi ánh pháo hắt xuống). Nửa kích thước, WebP không mất dữ liệu. Các hằng số phải khớp build_scene3d.py.
CAM_Y, CAM_Z, FIRE_Y, FIRE_Z, LAKE_Z = -12.0, 4.2, 58.0, -6.5, -8.0
if A.frame == "land":
    pitch, foc = math.radians(-1.5), (W / 2) / math.tan(math.radians(62.0 / 2))
else:
    pitch, foc = math.radians(3.0), (H / 2) / math.tan(math.radians(62.0 / 2))


def project(y, z):
    """Điểm (0, y, z) của cảnh → (tỉ lệ theo chiều cao ảnh, số điểm ảnh mỗi mét ở cỡ xuất chuẩn)."""
    dy, dz = y - CAM_Y, z - CAM_Z
    fwd, up = dy * math.cos(pitch) + dz * math.sin(pitch), -dy * math.sin(pitch) + dz * math.cos(pitch)
    return (H / 2 - up / fwd * foc) / H, foc / fwd / s


oy, ppm = project(FIRE_Y, FIRE_Z)
print("fireworks.js: oy=%.4f ppm=%.2f water=%.4f" % (oy, ppm, project(FIRE_Y, LAKE_Z)[0]))
if index is not None and not A.no_mask:
    rows = -(np.arange(H, dtype=np.float32) + 0.5 - H / 2) / foc
    world_y = CAM_Y + (math.cos(pitch) - math.sin(pitch) * rows)[:, None] * depth      # kênh độ sâu là khoảng cách theo trục nhìn
    lake = index > 0.5
    near = (world_y < FIRE_Y - 2.0) & ~lake & ~sky
    soft = lambda m, sg: gaussian_filter(m.astype(np.float32), sg * s)
    m = np.stack([soft(near, 1.6), soft(lake, 1.2), np.zeros((H, W), np.float32)], -1)
    MASK = os.path.splitext(WEBP)[0] + "-mask.webp"
    im = Image.fromarray((np.clip(m, 0, 1) * 255 + 0.5).astype(np.uint8), "RGB").resize((W // 2, H // 2), Image.LANCZOS)
    im.save(MASK, "WEBP", lossless=True, method=6)
    print("saved %s (%d KB)" % (os.path.relpath(MASK, ROOT), os.path.getsize(MASK) // 1024))
