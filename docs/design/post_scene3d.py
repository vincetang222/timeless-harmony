"""Hậu kỳ cho cảnh nền 3D: sương xa theo khoảng cách, quầng sáng, tông màu AgX, rồi xuất WebP vào assets/bg/.

    python post_scene3d.py .build/day-land.exr --mode day --frame land
    python post_scene3d.py .build/night-port.exr --mode night --frame port

Đầu vào là tệp EXR nhiều lớp do build_scene3d.py dựng (màu tuyến tính + kênh độ sâu).
"""
import argparse
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
ap.add_argument("--webp", default=None, help="mặc định: assets/bg/scene-<mode>[-m].webp")
ap.add_argument("--quality", type=int, default=None)
ap.add_argument("--exposure", type=float, default=None, help="số stop; bỏ trống = mức đã cân sẵn")
ap.add_argument("--stats", action="store_true")
A = ap.parse_args()
NIGHT = A.mode == "night"
PNG = A.png or os.path.splitext(A.src)[0] + ".png"
WEBP = A.webp or os.path.join(ROOT, "assets", "bg", "scene-%s%s.webp" % (A.mode, "-m" if A.frame == "port" else ""))

f = OpenEXR.File(A.src)
ch = {}
for part in f.parts:
    ch.update(part.channels)
names = list(ch)
rgb = np.asarray(ch[[k for k in names if k.endswith("Combined")][0]].pixels, np.float32)[..., :3]
depth = np.asarray(ch[[k for k in names if "Depth" in k][0]].pixels, np.float32)
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

# 5. WebP cho website (ảnh nằm sau kính mờ nên nén mạnh được)
q = A.quality or (74 if A.frame == "land" else 72)
Image.open(PNG).convert("RGB").save(WEBP, "WEBP", quality=q, method=6)
print("saved %s (%d KB, %dx%d, q%d)" % (os.path.relpath(WEBP, ROOT), os.path.getsize(WEBP) // 1024, W, H, q))
