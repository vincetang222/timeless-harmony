"""Sa bàn thử kỹ thuật (giai đoạn 1b): một góc tiệc vườn ghép từ kho đồ vật, cho trang game/lab/sa-ban/.

    python3 docs/game/build_saban.py                             # bố cục và gói mô hình (chỉ cần numpy)
    .venv3d/bin/python docs/game/build_saban.py --nen             # thêm ảnh mặt đảo đã tính sẵn ánh sáng, bóng đổ (Blender, vài phút)
    .venv3d/bin/python docs/game/build_saban.py --anh goc.png     # thêm ảnh xem trước đẹp (Blender)

Xuất vào game/lab/sa-ban/:
  bo-cuc.json   vị trí từng món, vật cản, hướng nắng. Toạ độ kiểu Blender: x, y trên mặt đất, z hướng lên, xoay quanh z tính bằng độ.
                Trang đổi sang three.js theo (x, z, -y).
  mo-hinh.json  các lưới trang cần: đồ vật có trong bố cục, và phần trang trí (cây, bụi hoa, dây đèn, mép đảo).
                Mỗi lưới: vị trí lượng tử Int16 trong hộp bao, màu sRGB 8 bit, chỉ số tam giác xếp theo chất liệu; phần nhị phân mã base64.
                Gói thành JSON vì trang Artifact không phục vụ tệp .glb. Trang tự tính lại pháp tuyến.
  nen-dao.webp  mặt đảo nhìn thẳng từ trên xuống: cỏ, lối đi, thảm, cánh hoa, cùng bóng và ánh hắt của mọi thứ (Cycles).
                Đồ vật và cây tàng hình với máy quay nhưng vẫn đổ bóng, nên ảnh chỉ còn mặt đất.
"""
import argparse
import base64
import json
import math
import os

import numpy as np

import build_kit as K
from build_kit import FLOWERS, PAL, Kit, rng

OUT = os.path.join(K.ROOT, "game", "lab", "sa-ban")
RI = 6.3                                                     # bán kính đảo (m)
SUN_ROT, SUN_RGB, SUN_E = (52, 0, -42), (1.0, 0.84, 0.66), 3.0
SKY_RGB, SKY_E = (0.62, 0.78, 1.0), 0.75
TABLES = ((-3.0, -0.3), (3.0, 0.3))
TREES = ((-4.9, 3.3, 2.9, 0.95), (-2.9, 4.9, 3.3, 1.1), (3.1, 4.8, 3.2, 1.05), (5.0, 3.0, 2.8, 0.9), (0.0, 5.6, 3.4, 1.15))
BUSHES = list(range(22, 160, 9)) + [203, 213, 224, 236, 304, 316, 327, 337]   # góc (độ) quanh mép đảo
POSTS = ((-5.0, -1.9), (5.0, -1.9), (-4.4, 3.0), (4.4, 3.0))


def layout():
    L = []

    def put(key, x, y, rot=0.0, z=0.0, s=1.0):
        L.append(dict(id=key, x=round(x, 3), y=round(y, 3), xoay=round(rot, 2), z=z, s=s))
    put("cong-hoa", 0, 3.3)
    for s in (-1, 1):
        put("chau-cay-non", s * 1.75, 3.4)
        for y in (-2.0, -0.3, 1.4):
            put("chau-hoa", s * 0.98, y, y * 40)
    for tx, ty in TABLES:
        put("ban-tron", tx, ty, tx * 20)
        for i in range(8):
            b = math.radians(i * 45 + 22.5)
            put("ghe-chiavari", tx + 1.24 * math.cos(b), ty + 1.24 * math.sin(b), i * 45 + 22.5 - 90)
    lx, ly, lr = -2.9, 3.3, 8.0                                # bàn dài: bánh cưới và tháp ly

    def on(dx):
        return lx + dx * math.cos(math.radians(lr)), ly + dx * math.sin(math.radians(lr))
    put("ban-dai", lx, ly, lr)
    put("banh-cuoi", *on(-0.62), z=0.767, s=1.5); put("thap-ly", *on(0.62), z=0.767, s=0.9)
    put("ban-ca-phe", -1.8, -3.2); put("thung-tien-mung", -1.8, -3.2, 15, z=0.73)
    put("bang-don-khach", 1.8, -3.0, -18); put("bong-bay", 2.7, -2.8)
    put("xe-ca-phe", 4.3, -3.0, -28); put("ghe-bang", -4.6, -2.9, 62); put("den-duong", -5.5, 1.0, -30)
    put("loa", 2.2, 3.8, -25); put("micro", -1.25, 2.7, 15)
    put("ban-ca-phe", 3.7, 3.2); put("mam-qua", 3.7, 3.2, z=0.73, s=1.3)
    return L


def ground():
    """Mặt đảo: cỏ cắt sọc, lối đi, thảm dưới bàn tròn, cánh hoa rắc. Chỉ dùng để tính ảnh nen-dao.webp."""
    k = Kit(); NA = 96
    rr = np.linspace(0, RI, 34); a = np.arange(NA) * 2 * np.pi / NA
    V = np.stack([np.outer(rr, np.cos(a)), np.outer(rr, np.sin(a)), np.zeros((34, NA))], -1).reshape(-1, 3); F = []
    for i in range(33):
        for j in range(NA):
            p, q = i * NA + j, i * NA + (j + 1) % NA
            F += [[p, q, q + NA], [p, q + NA, p + NA]]
    tone = 0.5 + 0.5 * np.tanh(np.sin(V[:, 0] * 2.0 + V[:, 1] * 0.7) * 4)
    k.add(V, F, PAL["grass"] + (PAL["grass_d"] - PAL["grass"]) * tone[:, None], nrm=(0, 0, 1))
    k.rbox(1.3, 6.2, 0.012, "cream", 0.1, t=(0, 0.2, 0))
    for tx, ty in TABLES:
        k.lathe([(1.95, 0.008), (0, 0.008)], (0.90, 0.85, 0.76), 44, hard=True, t=(tx, ty, 0))
    for x, y in rng.uniform((-0.95, -2.8), (0.95, 3.2), (170, 2)):
        if abs(x) > 0.5:
            k.ball((x, y, 0.016), (0.04, 0.03, 0.006), ("tulip", "pink_l", "rose", "white")[int(abs(x * 97 + y * 31)) % 4], 5, 3)
    return k


def decor():
    """Phần trang trí đứng trên đảo: mép đảo, hàng cây, bụi hoa, cột và dây đèn. Trả về (Kit, vật cản)."""
    k, obst = Kit(), []
    k.lathe([(0, -1.6), (3.8, -1.3), (5.8, -0.55), (RI, -0.1), (RI, 0)], "wood_d", 96)
    for x, y, h, r in TREES:
        k.cyl((x, y, 0), (x, y, h * 0.6), 0.10, "wood_d", 0.06, n=7, caps=False)
        k.foliage((x, y, h * 0.72), r, ("leaf", "leaf_m", "leaf"), nu=14, nv=10, rough=0.16)
        for b in range(5):
            k.foliage((x + r * 0.62 * math.cos(b * 1.257 + x), y + r * 0.62 * math.sin(b * 1.257 + x), h * 0.72 + r * 0.3 * math.sin(b * 2.1)),
                      r * 0.55, ("leaf", "leaf_m", "leaf_l"), nu=9, nv=6)
        obst.append(dict(x=x, y=y, r=0.3))
    for d in BUSHES:
        bx, by = 5.85 * math.cos(math.radians(d)), 5.85 * math.sin(math.radians(d)); s = 0.36 + 0.1 * math.sin(d * 1.7)
        k.foliage((bx, by, s * 0.7), (s * 1.25, s * 1.25, s), nu=10, nv=6)
        for j in range(4):
            dr = np.array((math.cos(j * 1.6 + d), math.sin(j * 1.6 + d), 1.2)); dr /= np.linalg.norm(dr)
            k.rose((bx, by, s * 0.7) + dr * s * 0.95, dr, 0.11, FLOWERS[(d + j) % len(FLOWERS)], 0)
        obst.append(dict(x=round(bx, 3), y=round(by, 3), r=round(s * 1.15, 3)))
    for x, y in POSTS:
        k.m("satin").lathe([(0, 0), (0.1, 0), (0.1, 0.03), (0.03, 0.05), (0.025, 3.3), (0, 3.3)], "dark", 8, hard=True, t=(x, y, 0)).m()
        obst.append(dict(x=x, y=y, r=0.14))
    for i, j in ((0, 3), (1, 2), (0, 1), (2, 3)):
        u = np.linspace(0, 1, 27)[:, None]; w = np.c_[np.array(POSTS[i]) + (np.array(POSTS[j]) - POSTS[i]) * u, 3.28 - 0.75 * 4 * u * (1 - u)]
        k.tube(w, 0.008, "dark", 4)
        for q in w[2:-1:2]:
            k.ball(q - (0, 0, 0.09), (0.055, 0.055, 0.07), "yellow", 8, 6)
    return k, obst


def sun_to():
    """Vector đơn vị chỉ về phía mặt trời, trong toạ độ three.js."""
    rx, ry, rz = (math.radians(a) for a in SUN_ROT)
    d = -(K.rotz(rz) @ K.roty(ry) @ K.rotx(rx) @ np.array((0, 0, -1.0)))
    return [round(float(v), 4) for v in (d[0], d[2], -d[1])]


def pack(P, C, I, T):
    """Một lưới → bản ghi gọn cho mo-hinh.json."""
    Y = P[:, [0, 2, 1]] * (1, 1, -1)                          # Z hướng lên → Y hướng lên, như glTF
    lo, hi = Y.min(0), Y.max(0); span = np.maximum(hi - lo, 1e-6)
    pos = np.round((Y - lo) / span * 65535 - 32768).astype("<i2")
    srgb = np.where(C <= 0.0031308, C * 12.92, 1.055 * np.power(np.clip(C, 0, 1), 1 / 2.4) - 0.055)
    col = np.clip(np.round(srgb * 255), 0, 255).astype("u1")
    order = np.argsort(T, kind="stable"); Ts = T[order]
    big = len(P) >= 65536
    idx = I[order].astype("<u4" if big else "<u2")
    groups, start = [], 0
    for m in np.unique(Ts):
        n = int((Ts == m).sum()) * 3
        groups.append([K.MKEYS[m], start, n]); start += n
    b = pos.tobytes() + col.tobytes(); b += b"\0" * (-len(b) % 4)
    return dict(n=int(len(P)), lo=[round(float(v), 5) for v in lo], hi=[round(float(v), 5) for v in hi], u32=bool(big),
                nhom=groups, b64=base64.b64encode(b + idx.tobytes()).decode())


def bl_world(bpy, sc, mats, built, L, dk, gk, ground_only):
    """Dựng cả sa bàn trong Blender. ground_only: mọi thứ trừ mặt đảo tàng hình với máy quay (vẫn đổ bóng)."""
    mesh = {}
    for p in L:
        key = p["id"]
        if key not in mesh:
            _, P, C, I, T = built[key]; mesh[key] = K.bl_mesh(bpy, mats, key, P, C, I, T)
        ob = bpy.data.objects.new(key, mesh[key]); ob.location = (p["x"], p["y"], p["z"])
        ob.rotation_euler = (0, 0, math.radians(p["xoay"])); ob.scale = (p["s"],) * 3; sc.collection.objects.link(ob)
        ob.visible_camera = not ground_only
    for name, k, cam in (("trang-tri", dk, not ground_only), ("mat-dao", gk, True)):
        P, N, C, I, T = k.arrays()
        ob = bpy.data.objects.new(name, K.bl_mesh(bpy, mats, name, P, C, I, T)); sc.collection.objects.link(ob); ob.visible_camera = cam
    K.bl_light(bpy, sc, SUN_RGB, SUN_E, SKY_RGB, SKY_E, SUN_ROT)


def render_ground(built, L, dk, gk, out, res=2048):
    bpy, sc, mats = K.bl_start(64)
    from PIL import Image
    bl_world(bpy, sc, mats, built, L, dk, gk, True)
    cam = bpy.data.cameras.new("cam"); cam.type = "ORTHO"; cam.ortho_scale = 2 * RI
    co = bpy.data.objects.new("cam", cam); co.location = (0, 0, 40); sc.collection.objects.link(co); sc.camera = co
    tmp = os.path.join(os.path.dirname(out), "_nen.png")
    sc.render.resolution_x = sc.render.resolution_y = res; sc.render.film_transparent = True; sc.render.filepath = tmp
    bpy.ops.render.render(write_still=True)
    im = Image.open(tmp).convert("RGBA")
    bg = Image.new("RGBA", im.size, tuple(int(v * 255) for v in PAL["grass_d"]) + (255,))  # ngoài mép đảo: màu cỏ, để mép không loang trắng
    Image.alpha_composite(bg, im).convert("RGB").save(out, "WEBP", quality=82, method=6)
    os.remove(tmp)


def render_preview(built, L, dk, gk, out):
    bpy, sc, mats = K.bl_start(72)
    from mathutils import Vector
    from PIL import Image
    bl_world(bpy, sc, mats, built, L, dk, gk, False)
    cam = bpy.data.cameras.new("cam"); cam.lens = 38
    co = bpy.data.objects.new("cam", cam); co.location = (0.8, -13.6, 7.6)
    co.rotation_euler = (Vector((0, 0.5, 1.0)) - co.location).to_track_quat("-Z", "Y").to_euler(); sc.collection.objects.link(co); sc.camera = co
    sc.render.resolution_x, sc.render.resolution_y = 1900, 1240; sc.render.film_transparent = True; sc.render.filepath = os.path.abspath(out)
    bpy.ops.render.render(write_still=True)
    im = Image.open(out).convert("RGBA"); W, H = im.size
    g = np.linspace(0, 1, H)[:, None, None]
    bg = Image.fromarray(((np.array((253, 244, 232)) * (1 - g) + np.array((247, 214, 214)) * g) * np.ones((1, W, 1))).astype("u1"), "RGB").convert("RGBA")
    K.bloom(Image.alpha_composite(bg, im).convert("RGB")).save(out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--nen", action="store_true", help="tính lại nen-dao.webp bằng Blender")
    ap.add_argument("--anh", default=None, help="xuất ảnh xem trước đẹp (Blender)")
    A = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    built, _ = K.build_all()
    L = layout(); used = sorted({p["id"] for p in L})
    dk, obst = decor(); gk = ground()
    meshes = {key: pack(*built[key][1:]) for key in used}
    P, N, C, I, T = dk.arrays()
    meshes["trang-tri"] = pack(P, K.bake(P, N, C, I, T, np.concatenate(dk.A)), I, T)
    with open(os.path.join(OUT, "mo-hinh.json"), "w", encoding="utf-8") as f:
        json.dump(meshes, f, separators=(",", ":"))
    bo = dict(toa_do="Blender: x, y trên mặt đất, z hướng lên; xoay quanh z, độ. three.js = (x, z, -y).",
              ban_kinh_dao=RI, mat_dat="nen-dao.webp",
              nang=dict(huong_toi_mat_troi=sun_to(), mau=SUN_RGB, cuong_do=SUN_E), troi=dict(mau=SKY_RGB, cuong_do=SKY_E),
              mon=L, vat_can=obst)
    with open(os.path.join(OUT, "bo-cuc.json"), "w", encoding="utf-8") as f:
        json.dump(bo, f, ensure_ascii=False, indent=1)
    kb = os.path.getsize(os.path.join(OUT, "mo-hinh.json")) / 1024
    print("%d món trong bố cục (%d loại), mo-hinh.json %.0f KB, %d tam giác" % (len(L), len(used), kb,
          sum(len(built[k][3]) for k in used) + len(I)))
    if A.nen:
        render_ground(built, L, dk, gk, os.path.join(OUT, "nen-dao.webp")); print("nen-dao.webp")
    if A.anh:
        render_preview(built, L, dk, gk, A.anh); print("anh", A.anh)
