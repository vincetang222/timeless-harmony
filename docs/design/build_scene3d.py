"""Cảnh nền 3D của Timeless Harmony: lễ cưới trong vườn biệt thự bên hồ ở Ý,
pháo bông cầu vồng sau cổng hoa. Dựng bằng Blender (module `bpy`) + Cycles, không dùng tài nguyên ngoài:
núi, hồ, cây, hoa, ghế, khách và pháo bông đều sinh bằng mã.

    python build_scene3d.py --mode day   --frame land --out .build/day-land.exr
    python build_scene3d.py --mode night --frame port --out .build/night-port.exr

Bốn khung hình: day|night × land (2000×1250, máy tính) | port (900×1950, điện thoại).
Thêm --scale 0.5 --spp 32 để xem thử nhanh (khoảng 40 giây). Sau đó chạy post_scene3d.py để ra WebP.
Toạ độ: mét, Z hướng lên, máy quay nhìn về +Y. Sân vườn ở z=0, mặt hồ ở z=LAKE.
"""
import argparse
import math
import os
import sys
import time

import bpy
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("--mode", default="day", choices=["day", "night"])
ap.add_argument("--frame", default="land", choices=["land", "port"])
ap.add_argument("--scale", type=float, default=1.0)
ap.add_argument("--spp", type=int, default=160)
ap.add_argument("--out", default="out.exr")
ap.add_argument("--fireworks", action="store_true", help="vẽ sẵn pháo bông vào ảnh (ảnh chia sẻ link); mặc định bỏ, vì trên web pháo hoa là chuyển động (fireworks.js)")
ap.add_argument("--skip", default="", help="bỏ bớt nhóm vật thể khi thử: terrain,grass,trees,people,fire")
A = ap.parse_args(sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:])
NIGHT = A.mode == "night"
SKIP = set(filter(None, A.skip.split(",")))
rng = np.random.default_rng(11)

LAKE = -8.0                       # mặt hồ thấp hơn sân vườn 8 m
ARCH_Y = 21.0                     # cổng hoa
RAIL_Y = 22.0                     # lan can đá ở mép sân
CAM = np.array([0.0, -12.0, 4.2])

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene


# ───────────────────────── lưới & hình cơ bản (numpy) ─────────────────────────
def lerp(a, b, t):
    return a + (b - a) * t


def sstep(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0.0, 1.0)
    return t * t * (3 - 2 * t)


def norm(v):
    v = np.asarray(v, float)
    n = np.linalg.norm(v, axis=-1, keepdims=True)
    return v / np.where(n == 0, 1, n)


def merge(parts):
    """Gộp nhiều (V, F[, C]) thành một lưới."""
    Vs, Fs, Cs, off = [], [], [], 0
    has_c = any(len(p) > 2 and p[2] is not None for p in parts)
    for p in parts:
        V, F = np.asarray(p[0], float), np.asarray(p[1], np.int64)
        Vs.append(V)
        Fs.append(F + off)
        if has_c:
            C = p[2] if len(p) > 2 and p[2] is not None else (0.8, 0.8, 0.8, 1)
            C = np.asarray(C, float)
            Cs.append(np.broadcast_to(C, (len(V), 4)) if C.ndim == 1 else C)
        off += len(V)
    return (np.concatenate(Vs), np.concatenate(Fs), np.concatenate(Cs) if has_c else None)


def xform(mesh, M=None, s=None, t=None, col=None):
    V, F = mesh[0], mesh[1]
    C = mesh[2] if len(mesh) > 2 else None
    V = np.asarray(V, float)
    if s is not None:
        V = V * np.asarray(s, float)
    if M is not None:
        V = V @ np.asarray(M, float).T
    if t is not None:
        V = V + np.asarray(t, float)
    return (V, F, col if col is not None else C)


def rotz(a):
    c, s = math.cos(a), math.sin(a)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1.0]])


def rotx(a):
    c, s = math.cos(a), math.sin(a)
    return np.array([[1.0, 0, 0], [0, c, -s], [0, s, c]])


def roty(a):
    c, s = math.cos(a), math.sin(a)
    return np.array([[c, 0, s], [0, 1.0, 0], [-s, 0, c]])


def box(size, center=(0, 0, 0)):
    sx, sy, sz = np.asarray(size, float) / 2
    V = np.array([[x, y, z] for z in (-sz, sz) for y in (-sy, sy) for x in (-sx, sx)], float) + center
    F = [[0, 2, 3], [0, 3, 1], [4, 5, 7], [4, 7, 6], [0, 1, 5], [0, 5, 4],
         [2, 6, 7], [2, 7, 3], [0, 4, 6], [0, 6, 2], [1, 3, 7], [1, 7, 5]]
    return (V, np.array(F))


def lathe(profile, n=16, cap=True):
    """Xoay biên dạng [(r, z), …] quanh trục Z."""
    prof = np.asarray(profile, float)
    k = len(prof)
    th = np.linspace(0, 2 * np.pi, n, endpoint=False)
    V = np.stack([np.outer(prof[:, 0], np.cos(th)), np.outer(prof[:, 0], np.sin(th)),
                  np.repeat(prof[:, 1:2], n, axis=1)], -1).reshape(-1, 3)
    F = []
    for i in range(k - 1):
        for j in range(n):
            a, b = i * n + j, i * n + (j + 1) % n
            c, d = a + n, b + n
            F += [[a, b, d], [a, d, c]]
    if cap:
        for i, flip in ((0, True), (k - 1, False)):
            ci = len(V)
            V = np.vstack([V, [0, 0, prof[i, 1]]])
            for j in range(n):
                a, b = i * n + j, i * n + (j + 1) % n
                F.append([ci, b, a] if flip else [ci, a, b])
    return (V, np.array(F))


def cyl(p0, p1, r0, r1=None, n=8):
    """Trụ / nón cụt nối hai điểm."""
    p0, p1 = np.asarray(p0, float), np.asarray(p1, float)
    r1 = r0 if r1 is None else r1
    d = p1 - p0
    L = np.linalg.norm(d)
    V, F = lathe([(r0, 0), (r1, L)], n)
    z = d / L
    x = norm(np.cross([0, 0, 1.0] if abs(z[2]) < 0.99 else [1.0, 0, 0], z))
    y = np.cross(z, x)
    return (V @ np.stack([x, y, z]) + p0, F)


def ball(center=(0, 0, 0), radii=(1, 1, 1), nu=12, nv=7):
    t = np.linspace(-np.pi / 2, np.pi / 2, nv + 2)[1:-1]
    V, F = lathe(np.stack([np.cos(t), np.sin(t)], 1), nu, cap=False)
    k = len(V)
    V = np.vstack([V, [0, 0, -1], [0, 0, 1]])
    F = list(F)
    for j in range(nu):
        F.append([k, (j + 1) % nu, j])
        F.append([k + 1, (nv - 1) * nu + j, (nv - 1) * nu + (j + 1) % nu])
    return (V * np.asarray(radii, float) + center, np.array(F))


def tube(P, R, n=6, C=None):
    """Ống quét dọc đường gấp khúc P (k,3), bán kính R (k,)."""
    P = np.asarray(P, float)
    k = len(P)
    R = np.broadcast_to(np.asarray(R, float), (k,))
    T = norm(np.gradient(P, axis=0))
    ref = np.array([0.0, 1.0, 0.0]) if abs(T[0][1]) < 0.9 else np.array([1.0, 0, 0])
    X = norm(np.cross(ref, T))
    Y = np.cross(T, X)
    th = np.linspace(0, 2 * np.pi, n, endpoint=False)
    V = (P[:, None, :] + R[:, None, None] * (np.cos(th)[None, :, None] * X[:, None, :] + np.sin(th)[None, :, None] * Y[:, None, :])).reshape(-1, 3)
    i = np.arange(k - 1)[:, None] * n
    j = np.arange(n)[None, :]
    a, b = i + j, i + (j + 1) % n
    F = np.concatenate([np.stack([a, b, b + n], -1).reshape(-1, 3), np.stack([a, b + n, a + n], -1).reshape(-1, 3)])
    col = None if C is None else np.repeat(np.asarray(C, float), n, axis=0)
    return (V, F, col)


def instances(proto, M, T, C=None):
    """Nhân bản lưới mẫu theo N phép biến đổi (M: N×3×3, T: N×3); màu C: N×4."""
    V, F = np.asarray(proto[0], float), np.asarray(proto[1], np.int64)
    N, nv = len(T), len(V)
    Vo = np.einsum("nij,vj->nvi", M, V) + T[:, None, :]
    Fo = F[None] + (np.arange(N) * nv)[:, None, None]
    Co = None if C is None else np.repeat(np.asarray(C, float), nv, axis=0)
    return (Vo.reshape(-1, 3), Fo.reshape(-1, 3), Co)


def frames(z, roll=None, up=(0, 0, 1.0)):
    """Ma trận xoay N×3×3 có trục Z cục bộ hướng theo z (N,3)."""
    z = norm(z)
    N = len(z)
    ref = np.tile(np.asarray(up, float), (N, 1))
    bad = np.abs((z * ref).sum(1)) > 0.97
    ref[bad] = [1.0, 0, 0]
    x = norm(np.cross(ref, z))
    y = np.cross(z, x)
    if roll is not None:
        c, s = np.cos(roll)[:, None], np.sin(roll)[:, None]
        x, y = x * c + y * s, -x * s + y * c
    return np.stack([x, y, z], -1)


def obj(name, mesh, mat=None, smooth=True, shadow=True):
    V, F = np.asarray(mesh[0], np.float32), np.asarray(mesh[1], np.int32)
    C = mesh[2] if len(mesh) > 2 else None
    me = bpy.data.meshes.new(name)
    me.vertices.add(len(V))
    me.vertices.foreach_set("co", V.ravel())
    me.loops.add(len(F) * 3)
    me.loops.foreach_set("vertex_index", F.ravel())
    me.polygons.add(len(F))
    me.polygons.foreach_set("loop_start", np.arange(0, len(F) * 3, 3, dtype=np.int32))
    me.polygons.foreach_set("loop_total", np.full(len(F), 3, np.int32))
    me.update(calc_edges=True)
    if smooth:
        me.polygons.foreach_set("use_smooth", np.ones(len(F), bool))
    if C is not None:
        ca = me.color_attributes.new("Col", "FLOAT_COLOR", "POINT")
        ca.data.foreach_set("color", np.asarray(C, np.float32).ravel())
    ob = bpy.data.objects.new(name, me)
    scene.collection.objects.link(ob)
    if mat is not None:
        me.materials.append(mat)
    if not shadow:
        ob.visible_shadow = False
    return ob


# ───────────────────────────────── chất liệu ─────────────────────────────────
def material(name):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    return m, nt, out


def N(nt, kind, **kw):
    n = nt.nodes.new(kind)
    for k, v in kw.items():
        if k in n.inputs:
            n.inputs[k].default_value = v
        else:
            setattr(n, k, v)
    return n


def L(nt, a, b):
    nt.links.new(a, b)


def principled(name, color=(0.8, 0.8, 0.8, 1), rough=0.6, vcol=False, vmix=1.0, bump=0.0, bump_scale=40.0,
               noise=0.0, noise_scale=6.0, metal=0.0, sss=0.0, sss_r=0.05, coat=0.0, sheen=0.0, spec=0.5, emit=None, emit_s=0.0):
    """Chất liệu Principled; vcol=True lấy màu từ thuộc tính đỉnh 'Col'."""
    m, nt, out = material(name)
    p = N(nt, "ShaderNodeBsdfPrincipled", Roughness=rough, Metallic=metal)
    p.inputs["Specular IOR Level"].default_value = spec
    base = None
    if vcol:
        at = N(nt, "ShaderNodeAttribute", attribute_name="Col")
        base = at.outputs["Color"]
        if vmix != 1.0:
            mx = N(nt, "ShaderNodeMix", data_type="RGBA", blend_type="MULTIPLY")
            mx.inputs[0].default_value = 1.0
            L(nt, base, mx.inputs[6])
            mx.inputs[7].default_value = (vmix, vmix, vmix, 1)
            base = mx.outputs[2]
    else:
        p.inputs["Base Color"].default_value = color
    if noise > 0:
        tx = N(nt, "ShaderNodeTexNoise", Scale=noise_scale, Detail=5.0, Roughness=0.6)
        ramp = N(nt, "ShaderNodeMapRange")
        ramp.inputs[1].default_value, ramp.inputs[2].default_value = 0.3, 0.7
        ramp.inputs[3].default_value, ramp.inputs[4].default_value = 1 - noise, 1 + noise
        L(nt, tx.outputs["Fac"], ramp.inputs[0])
        mx = N(nt, "ShaderNodeMix", data_type="RGBA", blend_type="MULTIPLY")
        mx.inputs[0].default_value = 1.0
        if base is not None:
            L(nt, base, mx.inputs[6])
        else:
            mx.inputs[6].default_value = color
        L(nt, ramp.outputs[0], mx.inputs[7])
        base = mx.outputs[2]
    if base is not None:
        L(nt, base, p.inputs["Base Color"])
    if bump > 0:
        tx = N(nt, "ShaderNodeTexNoise", Scale=bump_scale, Detail=6.0, Roughness=0.65)
        bp = N(nt, "ShaderNodeBump", Strength=bump, Distance=0.02)
        L(nt, tx.outputs["Fac"], bp.inputs["Height"])
        L(nt, bp.outputs[0], p.inputs["Normal"])
    if sss > 0:
        p.inputs["Subsurface Weight"].default_value = sss
        p.inputs["Subsurface Radius"].default_value = (sss_r, sss_r * 0.6, sss_r * 0.4)
        p.inputs["Subsurface Scale"].default_value = 1.0
    if coat > 0:
        p.inputs["Coat Weight"].default_value = coat
    if sheen > 0:
        p.inputs["Sheen Weight"].default_value = sheen
    if emit is not None:
        p.inputs["Emission Color"].default_value = emit
        p.inputs["Emission Strength"].default_value = emit_s
    L(nt, p.outputs[0], out.inputs[0])
    return m


def leaf_material(name, translucency=0.35, rough=0.7):
    """Lá cây: khuếch tán + xuyên sáng (nắng lọt qua lá) + một chút bóng."""
    m, nt, out = material(name)
    at = N(nt, "ShaderNodeAttribute", attribute_name="Col")
    d = N(nt, "ShaderNodeBsdfDiffuse")
    tr = N(nt, "ShaderNodeBsdfTranslucent")
    L(nt, at.outputs["Color"], d.inputs[0])
    hs = N(nt, "ShaderNodeHueSaturation")
    hs.inputs["Saturation"].default_value, hs.inputs["Value"].default_value = 1.15, 1.6
    L(nt, at.outputs["Color"], hs.inputs["Color"])
    L(nt, hs.outputs[0], tr.inputs[0])
    mx = N(nt, "ShaderNodeMixShader")
    mx.inputs[0].default_value = translucency
    L(nt, d.outputs[0], mx.inputs[1])
    L(nt, tr.outputs[0], mx.inputs[2])
    gl = N(nt, "ShaderNodeBsdfGlossy", Roughness=rough)
    gl.inputs[0].default_value = (1, 1, 1, 1)
    fr = N(nt, "ShaderNodeFresnel", IOR=1.4)
    mx2 = N(nt, "ShaderNodeMixShader")
    sc = N(nt, "ShaderNodeMath", operation="MULTIPLY")
    sc.inputs[1].default_value = 0.22
    L(nt, fr.outputs[0], sc.inputs[0])
    L(nt, sc.outputs[0], mx2.inputs[0])
    L(nt, mx.outputs[0], mx2.inputs[1])
    L(nt, gl.outputs[0], mx2.inputs[2])
    L(nt, mx2.outputs[0], out.inputs[0])
    return m


# ─────────────────────────────── nhiễu (numpy) ───────────────────────────────
def _perm(seed):
    p = np.arange(256)
    np.random.default_rng(seed).shuffle(p)
    return np.concatenate([p, p, p])


def perlin(x, y, seed=0):
    p = _perm(seed)
    xi, yi = np.floor(x).astype(np.int64), np.floor(y).astype(np.int64)
    xf, yf = x - xi, y - yi
    xi, yi = xi & 255, yi & 255
    u, v = xf * xf * xf * (xf * (xf * 6 - 15) + 10), yf * yf * yf * (yf * (yf * 6 - 15) + 10)

    def g(h, a, b):
        ang = h * (2 * np.pi / 256.0)
        return np.cos(ang) * a + np.sin(ang) * b

    aa, ab = p[p[xi] + yi], p[p[xi] + yi + 1]
    ba, bb = p[p[xi + 1] + yi], p[p[xi + 1] + yi + 1]
    return lerp(lerp(g(aa, xf, yf), g(ba, xf - 1, yf), u), lerp(g(ab, xf, yf - 1), g(bb, xf - 1, yf - 1), u), v) * 1.41


def fbm(x, y, octaves=6, gain=0.5, seed=0):
    s, a, f = 0.0, 1.0, 1.0
    for o in range(octaves):
        s = s + a * perlin(x * f, y * f, seed + o)
        a *= gain
        f *= 2.0
    return s


def ridged(x, y, octaves=6, gain=0.5, seed=0):
    s, a, f, w = 0.0, 1.0, 1.0, 1.0
    for o in range(octaves):
        n = (1.0 - np.abs(perlin(x * f, y * f, seed + o))) ** 2
        s = s + a * n * w
        w = np.clip(n * 2.0, 0, 1)
        a *= gain
        f *= 2.0
    return s


# ─────────────────────────────── núi và mặt hồ ───────────────────────────────
def lake_cx(y):
    return 260.0 * np.sin(y / 2100.0) + 0.000085 * np.maximum(y - 2800.0, 0) ** 2


def lake_hw(y):
    return (1080.0 + 300.0 * np.sin(y / 2900.0 + 0.6)) * (1 - sstep(11500.0, 15500.0, y))


def height(x, y):
    """Độ cao địa hình (m, so với mặt hồ). Âm = dưới nước."""
    u = np.abs(x - lake_cx(y)) - lake_hw(y)                 # >0: đất liền
    wob = 260.0 * fbm(x / 1900.0, y / 1900.0, 3, seed=40)   # đường bờ ngoằn ngoèo
    u = u + wob
    side = np.where(x > lake_cx(y), 1.0, 0.0)
    hmax = 1150.0 + 380.0 * perlin(x / 5200.0 + 3.1, y / 5200.0, 9) + 180.0 * side
    rise = 1 - np.exp(-np.maximum(u, 0) / 1050.0)
    rd = ridged(x / 3100.0, y / 3100.0, 6, 0.52, seed=3)
    h = hmax * rise * (0.38 + 0.50 * rd)
    h += 34.0 * fbm(x / 330.0, y / 330.0, 4, seed=21) * sstep(40.0, 500.0, u)
    # dãy Alps xa ở cuối hồ
    alps = sstep(15000.0, 26000.0, y)
    h += alps * 1500.0 * ridged(x / 6400.0 + 1.7, y / 6400.0, 6, 0.55, seed=77)
    h = np.where(u > 0, h + 0.012 * u, u * 0.05)
    prom = 980.0 * np.exp(-(((x - 2050.0) / 760.0) ** 2 + ((y - 4300.0) / 1500.0) ** 2) / 2)
    h = np.maximum(h, prom * (0.55 + 0.42 * rd) - 55.0 + 22.0 * fbm(x / 300.0, y / 300.0, 3, seed=31))
    # mũi đất nơi có khu vườn: không cho núi chặn trước mặt
    return h


def terrain_mesh(x0, x1, y0, y1, step):
    xs = np.arange(x0, x1 + step, step)
    ys = np.arange(y0, y1 + step, step)
    X, Y = np.meshgrid(xs, ys)
    H = height(X, Y)
    nx, ny = len(xs), len(ys)
    V = np.stack([X, Y, H + LAKE], -1).reshape(-1, 3)
    i = (np.arange(ny - 1)[:, None] * nx + np.arange(nx - 1)[None, :]).ravel()
    F = np.concatenate([np.stack([i, i + 1, i + nx + 1], 1), np.stack([i, i + nx + 1, i + nx], 1)])
    # màu theo độ cao, độ dốc, nhiễu
    gy, gx = np.gradient(H, step)
    slope = np.sqrt(gx ** 2 + gy ** 2)
    n1 = fbm(X / 420.0, Y / 420.0, 4, seed=5)
    n2 = fbm(X / 90.0, Y / 90.0, 3, seed=6)
    forest = lerp(np.array([0.040, 0.095, 0.030]), np.array([0.095, 0.175, 0.045]), sstep(-0.5, 0.6, n1 + 0.4 * n2)[..., None])
    meadow = np.array([0.20, 0.27, 0.08])
    rock = lerp(np.array([0.30, 0.28, 0.25]), np.array([0.42, 0.40, 0.37]), sstep(-0.4, 0.5, n2)[..., None])
    snow = np.array([0.86, 0.88, 0.92])
    col = lerp(forest, meadow, (sstep(0.25, 0.75, n1) * sstep(250, 700, H) * (1 - sstep(0.35, 0.6, slope)))[..., None])
    rk = np.clip(sstep(1.5, 2.2, slope) + sstep(1250, 1700, H + 160 * n1), 0, 1)
    col = lerp(col, rock, rk[..., None])
    col = lerp(col, snow, (sstep(2050, 2500, H + 220 * n1) * (1 - 0.6 * sstep(0.9, 1.4, slope)))[..., None])
    shore = sstep(5.0, 0.5, H)
    col = lerp(col, np.array([0.34, 0.31, 0.25]), shore[..., None] * 0.8)
    C = np.concatenate([col.reshape(-1, 3), np.ones((nx * ny, 1))], 1)
    keep = (H > -6).ravel()                                # bỏ tam giác chìm hẳn dưới nước
    F = F[keep[F].any(1)]
    return (V, F, C)


def build_terrain():
    mat = principled("Terrain", vcol=True, rough=0.92, spec=0.2)
    nt = mat.node_tree
    p = nt.nodes["Principled BSDF"]
    geo = N(nt, "ShaderNodeNewGeometry")
    n1 = N(nt, "ShaderNodeTexNoise", Scale=0.045, Detail=7.0, Roughness=0.62)   # tán rừng ~20 m
    n2 = N(nt, "ShaderNodeTexNoise", Scale=0.012, Detail=5.0, Roughness=0.6)
    for n in (n1, n2):
        L(nt, geo.outputs["Position"], n.inputs["Vector"])
    add = N(nt, "ShaderNodeMath", operation="ADD")
    L(nt, n1.outputs["Fac"], add.inputs[0])
    L(nt, n2.outputs["Fac"], add.inputs[1])
    bp = N(nt, "ShaderNodeBump", Strength=1.0, Distance=14.0)
    L(nt, add.outputs[0], bp.inputs["Height"])
    L(nt, bp.outputs[0], p.inputs["Normal"])
    at = nt.nodes["Attribute"]
    mr = N(nt, "ShaderNodeMapRange")
    mr.inputs[1].default_value, mr.inputs[2].default_value, mr.inputs[3].default_value, mr.inputs[4].default_value = 0.35, 0.7, 0.62, 1.3
    L(nt, n1.outputs["Fac"], mr.inputs[0])
    mx = N(nt, "ShaderNodeMix", data_type="RGBA", blend_type="MULTIPLY")
    mx.inputs[0].default_value = 1.0
    L(nt, at.outputs["Color"], mx.inputs[6])
    L(nt, mr.outputs[0], mx.inputs[7])
    L(nt, mx.outputs[2], p.inputs["Base Color"])
    obj("TerrainNear", terrain_mesh(-7000, 7000, 60, 9000, 22), mat)
    obj("TerrainFar", terrain_mesh(-26000, 26000, 8800, 46000, 90), mat)


def build_lake():
    m, nt, out = material("Lake")
    deep = (0.006, 0.040, 0.060, 1) if not NIGHT else (0.002, 0.008, 0.016, 1)
    tint = (0.50, 0.72, 0.90, 1) if not NIGHT else (0.75, 0.85, 1.0, 1)
    geo = N(nt, "ShaderNodeNewGeometry")
    mp = N(nt, "ShaderNodeMapping")
    mp.inputs["Scale"].default_value = (0.22, 0.9, 1.0)           # sóng kéo dài theo chiều ngang
    L(nt, geo.outputs["Position"], mp.inputs["Vector"])
    w1 = N(nt, "ShaderNodeTexNoise", Scale=0.55, Detail=4.0, Roughness=0.55)
    w2 = N(nt, "ShaderNodeTexNoise", Scale=0.06, Detail=3.0, Roughness=0.5)
    L(nt, mp.outputs[0], w1.inputs["Vector"])
    L(nt, mp.outputs[0], w2.inputs["Vector"])
    mixw = N(nt, "ShaderNodeMath", operation="MULTIPLY_ADD")
    mixw.inputs[1].default_value = 2.2
    L(nt, w2.outputs["Fac"], mixw.inputs[0])
    L(nt, w1.outputs["Fac"], mixw.inputs[2])
    bp = N(nt, "ShaderNodeBump", Strength=0.42, Distance=0.6)
    L(nt, mixw.outputs[0], bp.inputs["Height"])
    d = N(nt, "ShaderNodeBsdfDiffuse")
    d.inputs[0].default_value = deep
    g = N(nt, "ShaderNodeBsdfGlossy", Roughness=0.045)
    g.inputs[0].default_value = tint
    fr = N(nt, "ShaderNodeFresnel", IOR=1.333)
    for n in (d, g, fr):
        L(nt, bp.outputs[0], n.inputs["Normal"])
    mx = N(nt, "ShaderNodeMixShader")
    L(nt, fr.outputs[0], mx.inputs[0])
    L(nt, d.outputs[0], mx.inputs[1]); L(nt, g.outputs[0], mx.inputs[2])
    L(nt, mx.outputs[0], out.inputs[0])
    s = 60000.0
    obj("Lake", (np.array([[-s, -3000, LAKE], [s, -3000, LAKE], [s, s, LAKE], [-s, s, LAKE]]), np.array([[0, 1, 2], [0, 2, 3]])), m, smooth=False).pass_index = 1   # lớp IndexOB: mặt nạ mặt hồ cho pháo hoa


# ──────────────────────────────── trời và nắng ────────────────────────────────
SUN_AZ = math.radians(70)      # mặt trời lệch trái so với hướng nhìn
SUN_EL = math.radians(44)


def build_world():
    w = bpy.data.worlds.new("World")
    scene.world = w
    w.use_nodes = True
    nt = w.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new("ShaderNodeOutputWorld")
    bg = nt.nodes.new("ShaderNodeBackground")
    tc = N(nt, "ShaderNodeTexCoord")
    sep = N(nt, "ShaderNodeSeparateXYZ")
    L(nt, tc.outputs["Generated"], sep.inputs[0])
    # chiếu hướng nhìn lên mặt phẳng mây
    zc = N(nt, "ShaderNodeMath", operation="MAXIMUM")
    zc.inputs[1].default_value = 0.0
    L(nt, sep.outputs["Z"], zc.inputs[0])
    za = N(nt, "ShaderNodeMath", operation="ADD")
    za.inputs[1].default_value = 0.09
    L(nt, zc.outputs[0], za.inputs[0])
    px = N(nt, "ShaderNodeMath", operation="DIVIDE")
    py = N(nt, "ShaderNodeMath", operation="DIVIDE")
    L(nt, sep.outputs["X"], px.inputs[0]); L(nt, za.outputs[0], px.inputs[1])
    L(nt, sep.outputs["Y"], py.inputs[0]); L(nt, za.outputs[0], py.inputs[1])
    cv = N(nt, "ShaderNodeCombineXYZ")
    L(nt, px.outputs[0], cv.inputs["X"]); L(nt, py.outputs[0], cv.inputs["Y"])
    mp = N(nt, "ShaderNodeMapping")
    mp.inputs["Scale"].default_value = (0.42, 0.62, 1.0)
    mp.inputs["Location"].default_value = (CLOUD_LOC[0], CLOUD_LOC[1], 0.0)
    L(nt, cv.outputs[0], mp.inputs["Vector"])
    cn = N(nt, "ShaderNodeTexNoise", Scale=1.0, Detail=9.0, Roughness=0.58, Distortion=0.35)
    L(nt, mp.outputs[0], cn.inputs["Vector"])
    ramp = N(nt, "ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].position, ramp.color_ramp.elements[1].position = (0.55, 0.75) if not NIGHT else (0.6, 0.8)
    L(nt, cn.outputs["Fac"], ramp.inputs[0])
    # mây mỏng dần về chân trời
    hf = N(nt, "ShaderNodeMapRange", interpolation_type="SMOOTHSTEP")
    hf.inputs[1].default_value, hf.inputs[2].default_value = 0.015, 0.16
    L(nt, sep.outputs["Z"], hf.inputs[0])
    cm = N(nt, "ShaderNodeMath", operation="MULTIPLY")
    L(nt, ramp.outputs["Color"], cm.inputs[0]); L(nt, hf.outputs[0], cm.inputs[1])
    # độ dày mây → sáng/tối
    dens = N(nt, "ShaderNodeMapRange")
    dens.inputs[1].default_value, dens.inputs[2].default_value, dens.inputs[3].default_value, dens.inputs[4].default_value = 0.6, 0.95, 1.0, 0.55
    L(nt, cn.outputs["Fac"], dens.inputs[0])
    mix = N(nt, "ShaderNodeMix", data_type="RGBA")
    L(nt, cm.outputs[0], mix.inputs[0])
    if not NIGHT:
        sky = N(nt, "ShaderNodeTexSky", sky_type="MULTIPLE_SCATTERING")
        sky.sun_elevation = SUN_EL
        sky.sun_rotation = SUN_ROT
        sky.sun_size = math.radians(1.6)
        sky.sun_intensity = 1.0
        sky.altitude = 200.0
        sky.air_density, sky.aerosol_density, sky.ozone_density = 1.0, 1.6, 1.0
        L(nt, sky.outputs[0], mix.inputs[6])
        cc = N(nt, "ShaderNodeMix", data_type="RGBA", blend_type="MULTIPLY")
        cc.inputs[0].default_value = 1.0
        cc.inputs[6].default_value = CLOUD_DAY
        L(nt, dens.outputs[0], cc.inputs[7])
        L(nt, cc.outputs[2], mix.inputs[7])
        bg.inputs["Strength"].default_value = 1.0
    else:
        # trời đêm: xanh thẳm, sáng dần về chân trời + sao
        g = N(nt, "ShaderNodeMapRange", interpolation_type="SMOOTHSTEP")
        g.inputs[1].default_value, g.inputs[2].default_value = 0.0, 0.55
        L(nt, sep.outputs["Z"], g.inputs[0])
        sk = N(nt, "ShaderNodeMix", data_type="RGBA")
        sk.inputs[6].default_value = (0.030, 0.052, 0.120, 1)      # chân trời
        sk.inputs[7].default_value = (0.0055, 0.011, 0.036, 1)     # thiên đỉnh
        L(nt, g.outputs[0], sk.inputs[0])
        vor = N(nt, "ShaderNodeTexVoronoi", Scale=170.0, feature="F1")
        L(nt, tc.outputs["Generated"], vor.inputs["Vector"])
        st = N(nt, "ShaderNodeMapRange", interpolation_type="SMOOTHSTEP")
        st.inputs[1].default_value, st.inputs[2].default_value, st.inputs[3].default_value, st.inputs[4].default_value = 0.0, 0.13, 1.0, 0.0
        L(nt, vor.outputs["Distance"], st.inputs[0])
        pw = N(nt, "ShaderNodeMath", operation="POWER")
        pw.inputs[1].default_value = 2.0
        L(nt, st.outputs[0], pw.inputs[0])
        sc_ = N(nt, "ShaderNodeSeparateColor")
        L(nt, vor.outputs["Color"], sc_.inputs[0])
        few = N(nt, "ShaderNodeMapRange")                             # chỉ một phần ô có sao, sáng tối khác nhau
        few.inputs[1].default_value, few.inputs[2].default_value, few.inputs[3].default_value, few.inputs[4].default_value = 0.66, 1.0, 0.0, 7.0
        L(nt, sc_.outputs[0], few.inputs[0])
        tw = N(nt, "ShaderNodeMath", operation="MULTIPLY")
        L(nt, pw.outputs[0], tw.inputs[0]); L(nt, few.outputs[0], tw.inputs[1])
        ssc = N(nt, "ShaderNodeMath", operation="MULTIPLY")           # sao mờ dần về chân trời
        L(nt, tw.outputs[0], ssc.inputs[0]); L(nt, g.outputs[0], ssc.inputs[1])
        sadd = N(nt, "ShaderNodeMix", data_type="RGBA", blend_type="ADD")
        sadd.inputs[0].default_value = 1.0
        L(nt, sk.outputs[2], sadd.inputs[6]); L(nt, ssc.outputs[0], sadd.inputs[7])
        L(nt, sadd.outputs[2], mix.inputs[6])
        cc = N(nt, "ShaderNodeMix", data_type="RGBA", blend_type="MULTIPLY")
        cc.inputs[0].default_value = 1.0
        cc.inputs[6].default_value = (0.030, 0.040, 0.075, 1)
        L(nt, dens.outputs[0], cc.inputs[7])
        L(nt, cc.outputs[2], mix.inputs[7])
        bg.inputs["Strength"].default_value = 1.0
    L(nt, mix.outputs[2], bg.inputs[0])
    L(nt, bg.outputs[0], out.inputs[0])


SUN_ROT = SUN_AZ
CLOUD_LOC = (9.3, 5.1)
CLOUD_DAY = (24.0, 23.4, 22.4, 1)


# ───────────────────────────────── máy quay ──────────────────────────────────
def build_camera():
    cam = bpy.data.cameras.new("Cam")
    ob = bpy.data.objects.new("Cam", cam)
    scene.collection.objects.link(ob)
    scene.camera = ob
    cam.sensor_width = 36.0
    cam.clip_start, cam.clip_end = 0.3, 120000.0
    if A.frame == "land":
        W, H, hfov, pitch = 2000, 1250, 62.0, -1.5
        cam.sensor_fit = "HORIZONTAL"
        cam.lens = 18.0 / math.tan(math.radians(hfov / 2))
    else:
        W, H, vfov, pitch = 900, 1950, 62.0, 3.0
        cam.sensor_fit = "VERTICAL"
        cam.sensor_height = 36.0
        cam.lens = 18.0 / math.tan(math.radians(vfov / 2))
    ob.location = CAM
    ob.rotation_euler = (math.radians(90 + pitch), 0, 0)
    scene.render.resolution_x, scene.render.resolution_y = W, H
    scene.render.resolution_percentage = int(round(100 * A.scale))


def setup_render():
    r = scene.render
    r.engine = "CYCLES"
    c = scene.cycles
    c.device = "CPU"
    c.samples = A.spp
    c.use_adaptive_sampling = True
    c.adaptive_threshold = 0.015
    c.use_denoising = True
    c.denoiser = "OPENIMAGEDENOISE"
    c.max_bounces, c.diffuse_bounces, c.glossy_bounces = 8, 3, 4
    c.transmission_bounces, c.transparent_max_bounces, c.volume_bounces = 6, 48, 0
    c.caustics_reflective = c.caustics_refractive = False
    c.sample_clamp_indirect = 8.0
    r.threads_mode = "AUTO"
    scene.view_layers[0].use_pass_z = True
    scene.view_layers[0].use_pass_object_index = True
    r.image_settings.media_type = "MULTI_LAYER_IMAGE"
    r.image_settings.file_format = "OPEN_EXR_MULTILAYER"
    r.image_settings.color_depth = "32"
    r.filepath = os.path.abspath(A.out)
    r.use_file_extension = False


# ─────────────────────────── tán lá & hoa (thẻ lá) ───────────────────────────
LEAF = (np.array([[0, 0, 0], [-0.5, 0.5, 0.10], [0, 1.0, 0], [0.5, 0.5, 0.10]], float), np.array([[0, 1, 2], [0, 2, 3]]))


def bloom_proto():
    """Bông hoa: khối tròn dẹt có 5 múi cánh xoáy và tâm lõm; trả thêm hệ số màu theo đỉnh (tâm sẫm hơn)."""
    V, F = ball((0, 0, 0), (1, 1, 0.8), 10, 5)
    th, z = np.arctan2(V[:, 1], V[:, 0]), V[:, 2]
    rho2 = V[:, 0] ** 2 + V[:, 1] ** 2
    r = 1 + 0.14 * np.cos(5 * th + 2.6 * z)
    V = V * np.stack([r, r, np.ones_like(r)], -1)
    dip = np.exp(-rho2 / 0.18) * (z > 0)
    V[:, 2] -= 0.30 * dip
    return (V, F), 1.0 - 0.30 * dip


BLOOM, BLOOM_SHADE = bloom_proto()


def rgba(c, n):
    return np.concatenate([np.broadcast_to(np.asarray(c, float)[:3], (n, 3)), np.ones((n, 1))], 1)


def foliage(P, Nn, size, c0, c1, tilt=0.6, up=None, aspect=0.55, lift=0.0):
    """Thẻ lá rải trên bề mặt: P điểm, Nn pháp tuyến hướng ra ngoài."""
    n = len(P)
    z = norm(Nn + tilt * rng.normal(size=(n, 3)))
    roll = rng.uniform(0, 2 * np.pi, n) if up is None else rng.normal(0, up, n)
    R = frames(z, roll)
    s = size * rng.uniform(0.65, 1.35, n)
    M = R * np.stack([s * aspect, s, s], -1)[:, None, :]
    t = rng.random(n)[:, None] ** 1.4
    C = np.concatenate([lerp(np.asarray(c0, float), np.asarray(c1, float), t), np.ones((n, 1))], 1)
    return instances(LEAF, M, P + Nn * lift - R[:, :, 1] * (s * 0.5)[:, None], C)


def blooms(P, size, palette, weights=None):
    """Bông hoa (khối tròn dẹt) tại các điểm P."""
    n = len(P)
    R = frames(norm(rng.normal(size=(n, 3)) + [0, 0, 0.6]), rng.uniform(0, 6.28, n))
    s = size * rng.uniform(0.7, 1.3, n)
    pal = np.asarray(palette, float)
    idx = rng.choice(len(pal), n, p=weights)
    c = pal[idx] * rng.uniform(0.9, 1.05, (n, 1))
    V, F, _ = instances(BLOOM, R * s[:, None, None], P)
    C = np.concatenate([(c[:, None, :] * BLOOM_SHADE[None, :, None]).reshape(-1, 3), np.ones((n * len(BLOOM_SHADE), 1))], 1)
    return (V, F, C)


def on_ellipsoid(c, r, n, zmin=-1.0):
    d = norm(rng.normal(size=(int(n * 2.2) + 8, 3)))
    d = d[d[:, 2] >= zmin][:n]
    r = np.asarray(r, float)
    return np.asarray(c, float) + d * r, norm(d / r)


def on_box(x0, x1, y0, y1, z0, z1, n):
    areas = np.array([(x1 - x0) * (y1 - y0), (x1 - x0) * (z1 - z0), (x1 - x0) * (z1 - z0), (y1 - y0) * (z1 - z0), (y1 - y0) * (z1 - z0)])
    k = rng.choice(5, n, p=areas / areas.sum())
    u, v = rng.random(n), rng.random(n)
    P = np.zeros((n, 3)); Nn = np.zeros((n, 3))
    X, Y, Z = lerp(x0, x1, u), lerp(y0, y1, v), lerp(z0, z1, v)
    Y2 = lerp(y0, y1, u)
    for i, (p, nn) in enumerate([((X, Y, np.full(n, z1)), (0, 0, 1)), ((X, np.full(n, y0), Z), (0, -1, 0)), ((X, np.full(n, y1), Z), (0, 1, 0)),
                                 ((np.full(n, x0), Y2, Z), (-1, 0, 0)), ((np.full(n, x1), Y2, Z), (1, 0, 0))]):
        m = k == i
        P[m] = np.stack(p, -1)[m]
        Nn[m] = nn
    return P, Nn


def on_revolve(rfun, h, base, n, tpow=1.0):
    t = rng.random(n) ** tpow
    th = rng.uniform(0, 2 * np.pi, n)
    r = rfun(t)
    dr = (rfun(np.clip(t + 0.01, 0, 1)) - rfun(np.clip(t - 0.01, 0, 1))) / 0.02 / h
    P = np.asarray(base, float) + np.stack([r * np.cos(th), r * np.sin(th), t * h], -1)
    return P, norm(np.stack([np.cos(th), np.sin(th), -dr], -1))


G_BOX = ((0.020, 0.060, 0.016), (0.075, 0.150, 0.035))        # hoàng dương cắt tỉa
G_CYP = ((0.012, 0.038, 0.016), (0.045, 0.095, 0.034))        # bách Ý
G_PINE = ((0.020, 0.052, 0.018), (0.070, 0.130, 0.038))       # thông dù
CYP_X = 13.0
G_SAGE = ((0.060, 0.100, 0.060), (0.150, 0.200, 0.120))       # lá bạch đàn trong hoa
FLOWERS = [(0.86, 0.84, 0.80), (0.84, 0.78, 0.68), (0.82, 0.56, 0.56), (0.78, 0.36, 0.42), (0.86, 0.62, 0.46)]
FLOWER_W = [0.42, 0.22, 0.20, 0.08, 0.08]

M_LEAF = leaf_material("Leaf")
M_CORE = principled("FoliageCore", color=(0.010, 0.026, 0.010, 1), rough=0.95, spec=0.1)
M_FLOWER = principled("Flower", vcol=True, rough=0.55, sss=0.25, sss_r=0.03, sheen=0.3)
M_STONE = principled("Stone", color=(0.50, 0.45, 0.37, 1), rough=0.82, noise=0.16, noise_scale=3.0, bump=0.35, bump_scale=60.0)
M_STONE_V = principled("StoneV", vcol=True, rough=0.82, bump=0.3, bump_scale=60.0)
M_TERRA = principled("Terracotta", color=(0.46, 0.19, 0.10, 1), rough=0.8, noise=0.15, noise_scale=8.0)
M_GRAVEL = principled("Gravel", color=(0.56, 0.50, 0.41, 1), rough=0.9, noise=0.22, noise_scale=45.0, bump=0.6, bump_scale=220.0)
M_FABRIC = principled("Fabric", color=(0.70, 0.68, 0.63, 1), rough=0.85, sheen=0.5, bump=0.08, bump_scale=30.0)
M_GOLD = principled("GoldWood", color=(0.72, 0.52, 0.22, 1), rough=0.36, metal=0.75)
M_PEOPLE = principled("People", vcol=True, rough=0.72, sheen=0.35, sss=0.08, sss_r=0.02)
M_SATIN = principled("Satin", color=(0.88, 0.87, 0.84, 1), rough=0.42, sheen=0.6)
M_TRUNK = principled("Trunk", color=(0.20, 0.13, 0.085, 1), rough=0.9, noise=0.3, noise_scale=3.0, bump=0.6, bump_scale=14.0)
M_VCOL = principled("Painted", vcol=True, rough=0.8)


def lawn_material():
    m, nt, out = material("Lawn")
    p = N(nt, "ShaderNodeBsdfPrincipled", Roughness=0.78)
    p.inputs["Sheen Weight"].default_value = 0.08
    p.inputs["Specular IOR Level"].default_value = 0.15
    geo = N(nt, "ShaderNodeNewGeometry")
    sep = N(nt, "ShaderNodeSeparateXYZ")
    L(nt, geo.outputs["Position"], sep.inputs[0])
    # sọc cắt cỏ chạy dọc lối đi (1,25 m một sọc)
    sn = N(nt, "ShaderNodeMath", operation="SINE")
    mu = N(nt, "ShaderNodeMath", operation="MULTIPLY")
    mu.inputs[1].default_value = math.pi / 1.25
    L(nt, sep.outputs["X"], mu.inputs[0]); L(nt, mu.outputs[0], sn.inputs[0])
    st = N(nt, "ShaderNodeMapRange", interpolation_type="SMOOTHSTEP")
    st.inputs[1].default_value, st.inputs[2].default_value = -0.25, 0.25
    L(nt, sn.outputs[0], st.inputs[0])
    stripe = N(nt, "ShaderNodeMix", data_type="RGBA")
    stripe.inputs[6].default_value = (0.026, 0.085, 0.012, 1)
    stripe.inputs[7].default_value = (0.042, 0.125, 0.020, 1)
    L(nt, st.outputs[0], stripe.inputs[0])
    n1 = N(nt, "ShaderNodeTexNoise", Scale=0.6, Detail=5.0, Roughness=0.6)
    n2 = N(nt, "ShaderNodeTexNoise", Scale=90.0, Detail=3.0, Roughness=0.7)
    for n in (n1, n2):
        L(nt, geo.outputs["Position"], n.inputs["Vector"])
    mr = N(nt, "ShaderNodeMapRange")
    mr.inputs[1].default_value, mr.inputs[2].default_value, mr.inputs[3].default_value, mr.inputs[4].default_value = 0.3, 0.7, 0.78, 1.22
    L(nt, n1.outputs["Fac"], mr.inputs[0])
    mr2 = N(nt, "ShaderNodeMapRange")
    mr2.inputs[1].default_value, mr2.inputs[2].default_value, mr2.inputs[3].default_value, mr2.inputs[4].default_value = 0.2, 0.8, 0.72, 1.28
    L(nt, n2.outputs["Fac"], mr2.inputs[0])
    m1 = N(nt, "ShaderNodeMix", data_type="RGBA", blend_type="MULTIPLY"); m1.inputs[0].default_value = 1.0
    L(nt, stripe.outputs[2], m1.inputs[6]); L(nt, mr.outputs[0], m1.inputs[7])
    m2 = N(nt, "ShaderNodeMix", data_type="RGBA", blend_type="MULTIPLY"); m2.inputs[0].default_value = 1.0
    L(nt, m1.outputs[2], m2.inputs[6]); L(nt, mr2.outputs[0], m2.inputs[7])
    L(nt, m2.outputs[2], p.inputs["Base Color"])
    bp = N(nt, "ShaderNodeBump", Strength=0.5, Distance=0.02)
    L(nt, n2.outputs["Fac"], bp.inputs["Height"]); L(nt, bp.outputs[0], p.inputs["Normal"])
    L(nt, p.outputs[0], out.inputs[0])
    return m


def quad(x0, x1, y0, y1, z):
    return (np.array([[x0, y0, z], [x1, y0, z], [x1, y1, z], [x0, y1, z]], float), np.array([[0, 1, 2], [0, 2, 3]]))


def disc(c, r, z, n=40, a0=0.0, a1=2 * np.pi):
    th = np.linspace(a0, a1, n)
    V = np.vstack([[c[0], c[1], z], np.stack([c[0] + r * np.cos(th), c[1] + r * np.sin(th), np.full(n, z)], -1)])
    F = np.array([[0, i, i + 1] for i in range(1, n)])
    return (V, F)


def sweep_rect(path, w, z0, z1):
    """Thanh tiết diện chữ nhật chạy theo đường path (k,2) trên mặt bằng."""
    P = np.asarray(path, float)
    T = norm(np.gradient(P, axis=0))
    Nn = np.stack([-T[:, 1], T[:, 0]], -1)
    k = len(P)
    ring = []
    for sgn, z in ((-1, z0), (1, z0), (1, z1), (-1, z1)):
        q = P + sgn * Nn * w / 2
        ring.append(np.concatenate([q, np.full((k, 1), z)], 1))
    V = np.stack(ring, 1).reshape(-1, 3)
    F = []
    for i in range(k - 1):
        for j in range(4):
            a, b = i * 4 + j, i * 4 + (j + 1) % 4
            F += [[a, b, b + 4], [a, b + 4, a + 4]]
    F += [[0, 1, 2], [0, 2, 3], [(k - 1) * 4, (k - 1) * 4 + 2, (k - 1) * 4 + 1], [(k - 1) * 4, (k - 1) * 4 + 3, (k - 1) * 4 + 2]]
    return (V, np.array(F))


BALC_R = 3.4
TERR_X = 15.0


def rail_paths():
    """Lan can: hai đoạn thẳng và ban công cong nhô ra hồ sau cổng hoa."""
    th = np.linspace(np.pi, 0, 34)
    arc = np.stack([BALC_R * np.cos(th), RAIL_Y + BALC_R * np.sin(th)], -1)
    left = np.stack([np.linspace(-TERR_X, -BALC_R, 30), np.full(30, RAIL_Y)], -1)
    right = np.stack([np.linspace(BALC_R, TERR_X, 30), np.full(30, RAIL_Y)], -1)
    return left, arc, right


def along(path, step, inset=0.0):
    P = np.asarray(path, float)
    d = np.r_[0, np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))]
    s = np.arange(inset + step / 2, d[-1] - inset, step)
    return np.stack([np.interp(s, d, P[:, 0]), np.interp(s, d, P[:, 1])], -1)


def urn(c, s=1.0):
    prof = [(0.16, 0), (0.17, 0.04), (0.07, 0.10), (0.09, 0.16), (0.22, 0.30), (0.27, 0.44), (0.24, 0.52), (0.28, 0.56), (0.25, 0.58), (0.20, 0.50)]
    V, F = lathe(np.array(prof) * s, 14)
    return (V + c, F)


def flower_dome(c, r, h, n, size=0.085, leaf=0.5):
    """Chùm hoa tự nhiên: vài vòm con lệch nhau, hoa to nhỏ xen kẽ, lá vươn ra ngoài. Trả về (hoa, lá)."""
    c = np.asarray(c, float)
    fl, lf = [], []
    k = 1 if r < 0.3 else (3 if r < 0.5 else 6)
    for i in range(k):
        o = (norm(rng.normal(size=3)) * [1, 1, 0.45] * r * 0.5) if k > 1 else np.zeros(3)
        rr = r * (1.0 if k == 1 else rng.uniform(0.5, 0.78))
        m = max(6, n // k)
        P, Nn = on_ellipsoid(c + o, (rr, rr, h * rr / r), m, zmin=-0.25)
        P = P - Nn * rng.uniform(0, 0.3, (len(P), 1)) * rr
        big = rng.random(len(P)) < 0.25
        fl.append(blooms(P[big], size * 1.2, FLOWERS, FLOWER_W))
        fl.append(blooms(P[~big], size * 0.85, FLOWERS, FLOWER_W))
        nl = int(m * leaf)
        Pl, Nl = on_ellipsoid(c + o, (rr * 1.12, rr * 1.12, h * rr / r), nl, zmin=-0.45)
        lf.append(foliage(Pl, Nl, 0.19 if r > 0.4 else 0.15, *G_SAGE, tilt=0.6, lift=0.02))
    return merge(fl), merge(lf)


def build_garden():
    lawn = lawn_material()
    parts_stone, parts_gravel, flowers, leaves, cores, terra = [], [], [], [], [], []
    # nền sân: cỏ + ban công đá
    obj("Lawn", quad(-TERR_X, TERR_X, -60, RAIL_Y, 0.0), lawn, smooth=False)
    parts_gravel.append(disc((0, RAIL_Y), BALC_R, 0.004, 40, 0, np.pi))
    for sgn in (-1, 1):
        parts_gravel.append(quad(sgn * 6.5, sgn * 8.3, -40, RAIL_Y - 0.9, 0.006))
        parts_gravel.append(quad(sgn * 1.2, sgn * TERR_X, RAIL_Y - 1.0, RAIL_Y, 0.005))
    parts_gravel.append(quad(-1.2, 1.2, RAIL_Y - 1.0, RAIL_Y, 0.005))
    # bục tròn dưới cổng hoa + thảm lối đi
    V, F = lathe([(2.55, 0), (2.55, 0.10), (2.45, 0.13), (0, 0.13)], 48, cap=False)
    parts_stone.append((V + [0, ARCH_Y + 0.25, 0], F))
    obj("Runner", quad(-1.05, 1.05, 1.2, ARCH_Y - 2.2, 0.012), M_FABRIC, smooth=False)
    # tường chắn dưới lan can (nhìn từ hồ) và lan can
    parts_stone.append(box((2 * TERR_X + 1, 0.5, 9.0), (0, RAIL_Y + 0.05, -4.5)))
    V, F = lathe([(BALC_R + 0.25, -9.0), (BALC_R + 0.25, 0.0)], 40, cap=False)
    parts_stone.append((V + [0, RAIL_Y, 0], F))
    bal = np.array([(0.075, 0), (0.075, 0.04), (0.045, 0.07), (0.05, 0.10), (0.095, 0.22), (0.10, 0.28), (0.07, 0.40), (0.045, 0.50), (0.06, 0.54), (0.075, 0.58), (0.075, 0.62)])
    BAL = lathe(bal, 10)
    for path in rail_paths():
        parts_stone.append(sweep_rect(path, 0.36, 0.0, 0.16))
        parts_stone.append(sweep_rect(path, 0.40, 0.78, 0.92))
        pts = along(path, 0.27)
        T = np.concatenate([pts, np.full((len(pts), 1), 0.16)], 1)
        parts_stone.append(instances(BAL, np.tile(np.eye(3), (len(T), 1, 1)), T)[:2])
    pier_xy = [(-BALC_R, RAIL_Y), (BALC_R, RAIL_Y)] + [(s * x, RAIL_Y) for s in (-1, 1) for x in (6.6, 9.8, 13.0, TERR_X)]
    pier_xy += [(BALC_R * math.cos(a), RAIL_Y + BALC_R * math.sin(a)) for a in (math.pi / 3, 2 * math.pi / 3)]
    for (x, y) in pier_xy:
        parts_stone.append(box((0.52, 0.52, 1.04), (x, y, 0.52)))
        parts_stone.append(box((0.62, 0.62, 0.07), (x, y, 1.07)))
        parts_stone.append(urn((x, y, 1.10), 0.9))
        f, l = flower_dome((x, y, 1.72), 0.36, 0.30, 70, 0.10)
        flowers.append(f); leaves.append(l)
    # hàng rào hoàng dương thấp + cây cắt tỉa trong chậu đất nung
    for sgn in (-1, 1):
        x0, x1 = sorted((sgn * 8.55, sgn * 9.45))
        cores.append(box((0.8, 60, 0.74), (sgn * 9.0, -10, 0.37)))
        P, Nn = on_box(x0, x1, -40, RAIL_Y - 1.2, 0.0, 0.82, 26000)
        leaves.append(foliage(P, Nn, 0.11, *G_BOX, tilt=0.8))
        for k, y in enumerate(np.arange(2.5, 20.5, 3.0)):
            x = sgn * 5.75
            V, F = lathe([(0.20, 0), (0.30, 0.42), (0.33, 0.46), (0.27, 0.46)], 14)
            terra.append((V + [x, y, 0], F))
            if k % 2 == 0:                                           # nón
                rf = lambda t: 0.46 * (1 - t) ** 0.9 + 0.02
                V, F = lathe([(0.40, 0.0), (0.02, 1.5)], 12)
                cores.append((V + [x, y, 0.46], F))
                P, Nn = on_revolve(rf, 1.62, (x, y, 0.44), 2600, 1.5)
            else:                                                    # cầu
                cores.append(ball((x, y, 0.98), (0.44, 0.44, 0.44)))
                P, Nn = on_ellipsoid((x, y, 0.98), (0.52, 0.52, 0.52), 2400)
            leaves.append(foliage(P, Nn, 0.10, *G_BOX, tilt=0.8))
        # hàng rào cao khép hai bên sân
        cores.append(box((1.3, 70, 2.5), (sgn * (TERR_X - 0.75), -12, 1.25)))
        xa, xb = sorted((sgn * (TERR_X - 1.5), sgn * TERR_X))
        P, Nn = on_box(xa, xb, -40, RAIL_Y, 0.0, 2.65, 60000)
        leaves.append(foliage(P, Nn, 0.16, *G_BOX, tilt=0.8))
    obj("Stone", merge(parts_stone), M_STONE, smooth=False)
    obj("Gravel", merge(parts_gravel), M_GRAVEL, smooth=False)
    obj("Terra", merge(terra), M_TERRA)
    return flowers, leaves, cores


def build_trees(leaves, cores):
    trunks = []
    # bách Ý dọc hai bên
    for sgn in (-1, 1):
        for y in (4.5, 8.4, 12.3, 16.2, 20.1):
            h = rng.uniform(8.0, 10.2)
            R = rng.uniform(0.80, 0.98)
            x = sgn * (CYP_X + rng.uniform(-0.2, 0.2))
            rf = lambda t, R=R: R * np.sin(np.pi * np.clip(t, 0, 1) ** 0.62) ** 0.75 * (1 - 0.25 * t) + 0.03
            ts = np.linspace(0, 1, 14)
            V, F = lathe(np.stack([rf(ts) * 0.82, ts * h], 1), 10)
            cores.append((V + [x, y, 0.35], F))
            trunks.append(cyl((x, y, 0), (x, y, 0.6), 0.16, 0.13))
            P, Nn = on_revolve(rf, h, (x, y, 0.35), 11000)
            leaves.append(foliage(P, Nn + [0, 0, 0.9], 0.30, *G_CYP, tilt=0.45, up=0.5, aspect=0.42))
    # cây lớn tán tròn ngoài mép sân (sồi xanh, ngô đồng)
    for (x, y, hh, cr) in [(-20.5, 21.0, 9.5, 4.6), (-26.0, 32.0, 11.0, 5.6), (-19.5, 8.0, 8.6, 4.2), (20.0, 22.5, 9.0, 4.4), (26.0, 33.0, 11.5, 5.6), (19.5, 9.0, 8.6, 4.0)]:
        c0 = np.array([x, y, hh - cr * 0.6])
        trunks.append(tube(np.array([[x + 0.5, y, -3.0], [x + 0.15, y, c0[2] * 0.5], c0]), [0.40, 0.30, 0.2], 8)[:2])
        for k in range(12):
            dvec = norm(rng.normal(size=3) + [0, 0, 0.5])
            c = c0 + dvec * cr * rng.uniform(0.15, 0.72)
            r = np.array([1, 1, 0.86]) * cr * rng.uniform(0.32, 0.50)
            trunks.append(cyl(c0 - [0, 0, 1.0], c, 0.10, 0.04, 6))
            cores.append(ball(c, r * 0.82, 10, 6))
            P, Nn = on_ellipsoid(c, r, 2300)
            leaves.append(foliage(P, Nn + [0, 0, 0.25], 0.36, *G_PINE, tilt=0.8, aspect=0.55))
    obj("Trunks", merge(trunks), M_TRUNK)


def chair_proto():
    gold, cush = [], []
    for sx in (-0.19, 0.19):
        gold.append(cyl((sx, 0.19, 0), (sx, 0.19, 0.45), 0.016, 0.018, 6))            # chân trước
        gold.append(cyl((sx * 0.92, -0.20, 0), (sx, -0.21, 0.92), 0.017, 0.015, 6))    # chân sau + trụ tựa
    gold.append(box((0.42, 0.42, 0.03), (0, 0, 0.445)))
    for z, hgt in ((0.905, 0.05), (0.70, 0.025), (0.50, 0.025)):
        gold.append(box((0.40, 0.022, hgt), (0, -0.21, z)))
    for sx in np.linspace(-0.14, 0.14, 6):
        gold.append(cyl((sx, -0.21, 0.51), (sx, -0.21, 0.89), 0.007, 0.007, 5))
    for sx in (-0.19, 0.19):
        gold.append(cyl((sx, -0.2, 0.2), (sx, 0.19, 0.2), 0.008, 0.008, 5))
    cush.append(box((0.39, 0.39, 0.05), (0, 0.0, 0.485)))
    return merge(gold)[:2], merge(cush)[:2]


SKIN = [(0.80, 0.56, 0.44), (0.72, 0.48, 0.36), (0.62, 0.40, 0.28), (0.86, 0.64, 0.52), (0.45, 0.28, 0.19)]
HAIR = [(0.03, 0.022, 0.016), (0.09, 0.05, 0.025), (0.22, 0.13, 0.06), (0.45, 0.33, 0.16), (0.012, 0.012, 0.014), (0.30, 0.28, 0.26)]
SUITS = [(0.022, 0.030, 0.060), (0.035, 0.036, 0.040), (0.10, 0.11, 0.13), (0.36, 0.31, 0.24), (0.05, 0.075, 0.12), (0.20, 0.22, 0.24)]
DRESS = [(0.52, 0.60, 0.46), (0.80, 0.56, 0.56), (0.78, 0.68, 0.50), (0.45, 0.58, 0.74), (0.62, 0.52, 0.72), (0.85, 0.80, 0.70), (0.70, 0.30, 0.34), (0.30, 0.48, 0.44), (0.86, 0.66, 0.38)]


def guest(woman):
    """Khách ngồi, gốc toạ độ ở mặt đất dưới ghế, quay mặt về +Y."""
    skin = SKIN[rng.integers(len(SKIN))]
    hair = HAIR[rng.integers(len(HAIR))]
    cl = np.array(DRESS[rng.integers(len(DRESS))] if woman else SUITS[rng.integers(len(SUITS))]) * rng.uniform(0.85, 1.1)
    w = 0.88 if woman else 1.0
    P = []
    P.append(xform(ball((0, 0.06, 0.55), (0.20 * w, 0.25, 0.10)), col=rgba(cl * (0.9 if woman else 0.75), 1)[0]))
    P.append(xform(ball((0, -0.07, 0.83), (0.168 * w, 0.105, 0.30)), col=rgba(cl, 1)[0]))
    P.append(xform(ball((0, -0.07, 1.04), (0.215 * w, 0.10, 0.085)), col=rgba(cl, 1)[0]))
    sleeve = rgba(skin if (woman and rng.random() < 0.7) else cl, 1)[0]
    for sx in (-1, 1):
        P.append(tube(np.array([[sx * 0.21 * w, -0.06, 1.03], [sx * 0.235 * w, -0.02, 0.78], [sx * 0.17 * w, 0.20, 0.62]]), [0.05, 0.043, 0.036], 6)[:2] + (sleeve,))
    P.append(xform(cyl((0, -0.055, 1.08), (0, -0.05, 1.17), 0.046, 0.044, 8), col=rgba(skin, 1)[0]))
    P.append(xform(ball((0, -0.035, 1.255), (0.082, 0.098, 0.112), 12, 7), col=rgba(skin, 1)[0]))
    style = rng.random()
    hc = rgba(hair, 1)[0]
    if not woman:
        P.append(xform(ball((0, -0.052, 1.275), (0.088, 0.098, 0.105), 12, 6), col=hc))
    elif style < 0.22:                                              # mũ rộng vành
        hat = np.array([(0.90, 0.86, 0.76), (0.80, 0.68, 0.50), (0.85, 0.72, 0.72)][rng.integers(3)])
        V, F = lathe([(0.27, 0.0), (0.275, 0.012), (0.10, 0.03), (0.095, 0.10), (0.0, 0.115)], 16, cap=False)
        P.append((V @ rotx(-0.12).T + [0, -0.03, 1.325], F, rgba(hat, 1)[0]))
        P.append(xform(ball((0, -0.07, 1.20), (0.092, 0.08, 0.16), 12, 6), col=hc))
    elif style < 0.6:                                               # tóc dài
        P.append(xform(ball((0, -0.050, 1.275), (0.090, 0.100, 0.108), 12, 6), col=hc))
        P.append(xform(ball((0, -0.085, 1.10), (0.10, 0.06, 0.20), 12, 6), col=hc))
    else:                                                           # búi tóc
        P.append(xform(ball((0, -0.050, 1.275), (0.090, 0.100, 0.108), 12, 6), col=hc))
        P.append(xform(ball((0, -0.125, 1.30), (0.048, 0.048, 0.048), 8, 5), col=hc))
    return merge(P)


def build_seating(flowers, leaves):
    gold, cush = chair_proto()
    rows = np.arange(3.2, 15.5, 1.02)
    xs = np.array([s * (1.78 + 0.5 * i) for s in (-1, 1) for i in range(6)])
    T = np.array([[x, y, 0.0] for y in rows for x in xs])
    n = len(T)
    ang = rng.normal(0, 0.04, n)
    M = np.array([rotz(a) for a in ang])
    T = T + np.c_[rng.normal(0, 0.012, (n, 2)), np.zeros(n)]
    obj("Chairs", instances(gold, M, T), M_GOLD)
    obj("Cushions", instances(cush, M, T), M_FABRIC, smooth=False)
    people = []
    for i in range(n):
        if rng.random() < 0.90:
            g = guest(rng.random() < 0.52)
            s = rng.uniform(0.93, 1.05)
            R = rotz(ang[i] + rng.normal(0, 0.16)) @ rotx(rng.normal(0.0, 0.05))
            people.append(xform(g, M=R * s, t=T[i]))
    # hoa hai bên lối đi + cánh hoa rải trên thảm
    lantern, flames = [], []
    for k, y in enumerate(rows):
        for sgn in (-1, 1):
            f, l = flower_dome((sgn * 1.36, y - 0.1, 0.30), 0.27, 0.34, 55, 0.085)
            flowers.append(f); leaves.append(l)
            if k % 2 == 1:
                c = np.array([sgn * 1.36, y - 0.55, 0.0])
                for dx, dy in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
                    lantern.append(cyl(c + [dx * 0.09, dy * 0.09, 0], c + [dx * 0.09, dy * 0.09, 0.42], 0.008, 0.008, 4))
                lantern.append(box((0.21, 0.21, 0.02), c + [0, 0, 0.01]))
                lantern.append(box((0.22, 0.22, 0.02), c + [0, 0, 0.42]))
                V, F = lathe([(0.11, 0), (0.0, 0.10)], 4)
                lantern.append((V @ rotz(math.pi / 4).T + c + [0, 0, 0.43], F))
                lantern.append(cyl(c + [0, 0, 0.02], c + [0, 0, 0.20], 0.035, 0.035, 8))
                flames.append(ball(c + [0, 0, 0.245], (0.016, 0.016, 0.035), 6, 4))
    plinths = []
    for sgn in (-1, 1):
        c = np.array([sgn * 1.95, 0.9, 0.0])
        V, F = lathe([(0.30, 0), (0.30, 0.08), (0.22, 0.12), (0.20, 1.0), (0.27, 1.05), (0.27, 1.12)], 20)
        plinths.append((V + c, F))
        plinths.append(urn(c + [0, 0, 1.12], 1.1))
        f, l = flower_dome(c + [0, 0, 1.95], 0.62, 0.55, 420, 0.105)
        flowers.append(f); leaves.append(l)
    obj("Plinths", merge(plinths), M_STONE)
    np_ = 2600
    px = np.where(rng.random(np_) < 0.5, -1, 1) * np.abs(rng.normal(0.95, 0.16, np_))
    P = np.stack([px, rng.uniform(1.4, ARCH_Y - 2.4, np_), np.full(np_, 0.016) + rng.random(np_) * 0.004], -1)
    R = frames(norm(rng.normal(0, 0.25, (np_, 3)) + [0, 0, 1]), rng.uniform(0, 6.28, np_))
    pc = rgba((1, 1, 1), np_)
    pc[:, :3] = np.asarray(FLOWERS)[rng.choice(5, np_, p=[0.35, 0.15, 0.3, 0.15, 0.05])]
    flowers.append(instances(LEAF, R * 0.045, P, pc))
    obj("People", merge(people), M_PEOPLE)
    obj("Lanterns", merge(lantern), M_GOLD, smooth=False)
    return merge(flames)


def build_arch(flowers, leaves):
    y0 = ARCH_Y
    R, leg = 1.85, 2.1
    th = np.linspace(np.pi, 0, 40)
    path = np.vstack([np.stack([np.full(12, -R), np.full(12, y0), np.linspace(0.13, leg, 12, endpoint=False)], -1),
                      np.stack([R * np.cos(th), np.full(40, y0), leg + R * np.sin(th)], -1),
                      np.stack([np.full(12, R), np.full(12, y0), np.linspace(leg, 0.13, 13)[1:]], -1)])
    obj("ArchFrame", tube(path, 0.035, 8)[:2], M_GOLD)
    d = np.r_[0, np.cumsum(np.linalg.norm(np.diff(path, axis=0), axis=1))]
    u = d / d[-1]
    # độ dày hoa: dày ở vai trái và chân phải, mỏng dần ở đỉnh (bố cục bất đối xứng)
    thick = 1.3 * (0.20 + 0.20 * np.exp(-((u - 0.30) / 0.16) ** 2) + 0.17 * np.exp(-((u - 0.86) / 0.13) ** 2) + 0.10 * np.exp(-((u - 0.04) / 0.07) ** 2) + 0.06 * np.exp(-((u - 0.62) / 0.1) ** 2))
    nf = 5600
    w = thick ** 2
    idx = rng.choice(len(path), nf, p=w / w.sum())
    off = norm(rng.normal(size=(nf, 3))) * (rng.random((nf, 1)) ** 0.5) * thick[idx][:, None] * [1.0, 0.75, 1.0]
    P = path[idx] + rng.normal(0, 0.05, (nf, 3)) + off
    flowers.append(blooms(P, 0.105, FLOWERS, FLOWER_W))
    nl = 4200
    idx = rng.choice(len(path), nl, p=w / w.sum())
    dirs = norm(rng.normal(size=(nl, 3)))
    Pl = path[idx] + dirs * thick[idx][:, None] * rng.uniform(0.75, 1.25, (nl, 1)) * [1.0, 0.75, 1.0]
    leaves.append(foliage(Pl, dirs, 0.20, *G_SAGE, tilt=0.9))
    # dây hoa rủ ở vai trái + cụm hoa dưới chân cổng
    for k in range(9):
        i0 = int(len(path) * rng.uniform(0.2, 0.42))
        n = rng.integers(8, 20)
        s = np.arange(n) * 0.085
        Ps = path[i0] + np.stack([rng.normal(0, 0.03, n) + rng.uniform(-0.25, 0.25), np.full(n, rng.uniform(-0.2, 0.2)), -thick[i0] - s], -1)
        flowers.append(blooms(Ps, 0.075, FLOWERS, [0.6, 0.2, 0.15, 0.03, 0.02]))
    for (x, r, n) in ((-R - 0.1, 0.66, 300), (R + 0.15, 0.85, 420)):
        f, l = flower_dome((x, y0 - 0.05, 0.28), r, 0.6, n, 0.10)
        flowers.append(f); leaves.append(l)


def build_couple(flowers):
    y = ARCH_Y - 0.35
    # cô dâu (trái), quay mặt sang phải
    bx = -0.38
    skin, hair = (0.82, 0.60, 0.48), (0.07, 0.04, 0.022)
    V, F = lathe([(0.66, 0), (0.64, 0.03), (0.52, 0.34), (0.37, 0.70), (0.23, 0.98), (0.145, 1.09), (0.16, 1.20), (0.165, 1.30), (0.10, 1.36)], 24)
    satin = [(V * [1.0, 0.92, 1.0] + [bx, y, 0], F)]
    satin.append(ball((bx - 0.75, y - 0.1, 0.02), (1.0, 0.55, 0.10), 16, 6))            # đuôi váy
    P = [xform(ball((bx, y, 1.40), (0.17, 0.085, 0.06)), col=rgba(skin, 1)[0])]
    for sy in (-1, 1):
        P.append(tube(np.array([[bx, y + sy * 0.16, 1.40], [bx + 0.08, y + sy * 0.17, 1.17], [bx + 0.30, y + sy * 0.06, 1.05]]), [0.042, 0.036, 0.03], 6)[:2] + (rgba(skin, 1)[0],))
    P.append(xform(cyl((bx, y, 1.42), (bx + 0.01, y, 1.52), 0.042, 0.04, 8), col=rgba(skin, 1)[0]))
    P.append(xform(ball((bx + 0.015, y, 1.60), (0.095, 0.08, 0.108), 12, 7), col=rgba(skin, 1)[0]))
    P.append(xform(ball((bx - 0.005, y, 1.622), (0.097, 0.086, 0.102), 12, 6), col=rgba(hair, 1)[0]))
    P.append(xform(ball((bx - 0.095, y, 1.64), (0.052, 0.052, 0.052), 8, 5), col=rgba(hair, 1)[0]))
    # khăn voan
    veil = np.array([[bx - 0.06, y, 1.70], [bx - 0.22, y, 1.45], [bx - 0.42, y, 0.95], [bx - 0.70, y, 0.30]])
    vt = tube(veil, [0.07, 0.17, 0.26, 0.36], 12)
    m, nt, out = material("Veil")
    d = N(nt, "ShaderNodeBsdfDiffuse"); d.inputs[0].default_value = (0.9, 0.9, 0.88, 1)
    tr = N(nt, "ShaderNodeBsdfTransparent")
    mx = N(nt, "ShaderNodeMixShader"); mx.inputs[0].default_value = 0.42
    L(nt, tr.outputs[0], mx.inputs[1]); L(nt, d.outputs[0], mx.inputs[2]); L(nt, mx.outputs[0], out.inputs[0])
    obj("Veil", (vt[0], vt[1]), m)
    flowers.append(blooms(np.array([bx + 0.32, y, 1.04]) + rng.normal(0, 0.055, (26, 3)), 0.07, FLOWERS, FLOWER_W))
    # chú rể (phải), quay mặt sang trái
    gx = 0.42
    suit, gskin, ghair = (0.016, 0.022, 0.045), (0.74, 0.52, 0.40), (0.03, 0.022, 0.016)
    for sy in (-1, 1):
        P.append(xform(cyl((gx, y + sy * 0.09, 0.04), (gx, y + sy * 0.10, 0.92), 0.072, 0.092, 8), col=rgba(suit, 1)[0]))
        P.append(xform(ball((gx - 0.04, y + sy * 0.09, 0.035), (0.13, 0.05, 0.04), 8, 4), col=rgba((0.01, 0.01, 0.01), 1)[0]))
    V, F = lathe([(0.19, 0.84), (0.20, 0.95), (0.19, 1.15), (0.215, 1.38), (0.20, 1.50), (0.10, 1.56)], 16)
    P.append((V * [0.62, 1.0, 1.0] + [gx, y, 0], F, rgba(suit, 1)[0]))
    for sy in (-1, 1):
        P.append(tube(np.array([[gx, y + sy * 0.215, 1.50], [gx - 0.05, y + sy * 0.23, 1.22], [gx - 0.28, y + sy * 0.07, 1.06]]), [0.058, 0.05, 0.04], 6)[:2] + (rgba(suit, 1)[0],))
    P.append(xform(cyl((gx, y, 1.54), (gx - 0.005, y, 1.63), 0.048, 0.046, 8), col=rgba(gskin, 1)[0]))
    P.append(xform(ball((gx - 0.012, y, 1.725), (0.10, 0.085, 0.115), 12, 7), col=rgba(gskin, 1)[0]))
    P.append(xform(ball((gx + 0.006, y, 1.752), (0.10, 0.09, 0.105), 12, 6), col=rgba(ghair, 1)[0]))
    obj("Couple", merge(P), M_PEOPLE)
    obj("Gown", merge(satin), M_SATIN)


def build_grass():
    """Lá cỏ thật ở vùng máy quay nhìn thấy; sọc cắt cỏ đến từ hướng ngả của lá."""
    n = int(1100000 * min(1.0, 0.35 + A.scale))
    m = int(n * 1.5)
    y0 = -2.5 if A.frame == "land" else -5.5
    y = y0 + (20.8 - y0) * rng.random(m) ** 1.55
    d = y - CAM[1]
    x = (rng.random(m) * 2 - 1) * np.minimum(TERR_X - 1.6, d * 0.68 + 1.5)
    keep = ~((np.abs(x) < 1.07) & (y > 1.2) & (y < ARCH_Y - 2.2))
    keep &= ~((np.abs(x) > 6.5) & (np.abs(x) < 8.3)) & ~((np.abs(x) > 8.5) & (np.abs(x) < 9.5))
    keep &= ~(np.hypot(x, y - (ARCH_Y + 0.25)) < 2.6)
    x, y, d = x[keep][:n], y[keep][:n], d[keep][:n]
    n = len(x)
    stripe = np.sin(x * np.pi / 1.25) > 0
    h = rng.uniform(0.035, 0.075, n) * (1 + d / 45)
    w = rng.uniform(0.010, 0.018, n) * (0.55 + d / 13)
    ang = rng.uniform(0, np.pi, n)
    lean = np.stack([rng.normal(0, 0.35, n), np.where(stripe, 0.6, -0.6) + rng.normal(0, 0.3, n)], -1) * h[:, None]
    base = np.stack([x, y, np.zeros(n)], -1)
    dx = np.stack([np.cos(ang), np.sin(ang), np.zeros(n)], -1) * (w / 2)[:, None]
    tip = base + np.concatenate([lean, h[:, None]], 1)
    V = np.stack([base - dx, base + dx, tip], 1).reshape(-1, 3)
    c = lerp(np.array([0.036, 0.098, 0.014]), np.array([0.110, 0.205, 0.040]), rng.random((n, 1)) ** 1.3)
    c = c * np.where(stripe, 1.12, 0.9)[:, None]
    C = np.concatenate([np.stack([c * 0.55, c * 0.55, c * 1.15], 1).reshape(-1, 3), np.ones((3 * n, 1))], 1)
    obj("Grass", (V, np.arange(3 * n).reshape(-1, 3), C), M_LEAF, smooth=False, shadow=False)


# ─────────────────────────── làng ven hồ và thuyền ───────────────────────────
WALLS = [(0.78, 0.66, 0.46), (0.80, 0.56, 0.40), (0.82, 0.74, 0.60), (0.76, 0.48, 0.40), (0.84, 0.80, 0.72), (0.70, 0.62, 0.42)]


def build_villages():
    """Làng ven hồ (có tháp chuông) và nhà rải rác trên sườn núi; ban đêm thành những đốm đèn."""
    HOUSE = box((1, 1, 1), (0, 0, 0.5))
    ROOF = lathe([(0.78, 1.0), (0.0, 1.32)], 4)
    ROOF = (ROOF[0] @ rotz(math.pi / 4).T, ROOF[1])
    X, Y, Hh, tower = [], [], [], []
    for side in (-1, 1):
        for yc in (1300, 2500, 3700, 5100, 6600, 8300):
            yc = yc + rng.uniform(-300, 300)
            xs = lake_cx(yc) + side * np.linspace(-900, 3200, 800)
            hs = height(xs, np.full_like(xs, yc))
            k = np.argmax(hs > 2.0)
            if hs[k] <= 2.0:
                continue
            nh = rng.integers(45, 110)
            ys = yc + rng.normal(0, 240, nh)
            xh = xs[k] + lake_cx(ys) - lake_cx(yc) + side * rng.exponential(85, nh)
            hh = height(xh, ys)
            ok = (hh > 1.5) & (hh < 170)
            t = np.zeros(ok.sum(), bool)
            if len(t):
                t[0] = True
            X.append(xh[ok]); Y.append(ys[ok]); Hh.append(hh[ok]); tower.append(t)
    n0 = 16000
    xs, ys = rng.uniform(-6500, 6500, n0), rng.uniform(300, 9800, n0)
    hh = height(xs, ys)
    ok = (hh > 3) & (hh < 560) & (rng.random(n0) < np.exp(-hh / 190.0))
    X.append(xs[ok]); Y.append(ys[ok]); Hh.append(hh[ok]); tower.append(np.zeros(ok.sum(), bool))
    xh, ys, hh, tw = (np.concatenate(v) for v in (X, Y, Hh, tower))
    nh = len(xh)
    sx, sy, sz = rng.uniform(8, 16, nh), rng.uniform(8, 13, nh), rng.uniform(7, 15, nh)
    sx[tw], sy[tw], sz[tw] = 6.0, 6.0, 30.0                          # tháp chuông nhà thờ
    Mh = np.array([rotz(a) for a in rng.uniform(0, 3.14, nh)]) * np.stack([sx, sy, sz], -1)[:, None, :]
    T = np.stack([xh, ys, hh + LAKE - 1.0], -1)
    wc = rgba((1, 1, 1), nh); wc[:, :3] = np.asarray(WALLS)[rng.integers(len(WALLS), size=nh)] * rng.uniform(0.85, 1.05, (nh, 1))
    rc = rgba((1, 1, 1), nh); rc[:, :3] = np.array([0.42, 0.17, 0.09]) * rng.uniform(0.8, 1.2, (nh, 1))
    Mr = Mh.copy()
    Mr[:, :, 2] *= (0.42 * np.minimum(sx, sy) / sz * 2.2)[:, None]
    Tr = T + np.stack([np.zeros(nh), np.zeros(nh), sz - Mr[:, 2, 2]], -1)
    obj("Villages", merge([instances(HOUSE, Mh, T, wc), instances(ROOF, Mr, Tr, rc)]), M_VCOL, smooth=False)
    if NIGHT:
        nl = int(nh * 1.4)
        i = rng.integers(nh, size=nl)
        P = np.stack([xh[i] + rng.normal(0, 5, nl), ys[i] + rng.normal(0, 5, nl), hh[i] + LAKE + rng.uniform(1, 9, nl)], -1)
        col = rgba((1, 1, 1), nl); col[:, :3] = lerp(np.array([1.0, 0.60, 0.24]), np.array([1.0, 0.86, 0.62]), rng.random((nl, 1)))
        m = emission_material("TownLights", 300.0, sampling=False, glossy=0.10)     # bóng đèn làng trên mặt hồ chỉ còn là vệt vàng mờ
        obj("TownLights", instances(ball((0, 0, 0), (1, 1, 1), 6, 3), np.tile(np.eye(3) * 2.0, (nl, 1, 1)), P, col), m, shadow=False)


def build_boats():
    parts = []
    white, wood = (0.82, 0.82, 0.80), (0.30, 0.14, 0.06)
    for (x, y, a, s) in ((-130, 250, 0.5, 1.0), (210, 420, -0.9, 1.15), (-380, 700, 1.2, 1.0), (520, 1100, 0.2, 1.3)):
        R = rotz(a) * s
        t = np.array([x, y, LAKE])
        hull = ball((0, 0, 0.15), (1.25, 4.2, 0.75), 12, 6)
        parts.append(xform(hull, M=R, t=t, col=rgba(wood, 1)[0]))
        parts.append(xform(box((2.0, 5.2, 0.08), (0, -0.2, 0.72)), M=R, t=t, col=rgba((0.55, 0.30, 0.14), 1)[0]))
        parts.append(xform(box((1.7, 0.9, 0.5), (0, 0.9, 1.0)), M=R, t=t, col=rgba(white, 1)[0]))
    # thuyền buồm
    for (x, y, a) in ((-620, 1500, 0.3), (330, 2300, -0.4)):
        R, t = rotz(a), np.array([x, y, LAKE])
        parts.append(xform(ball((0, 0, 0.2), (1.5, 5.0, 0.9), 12, 6), M=R, t=t, col=rgba(white, 1)[0]))
        parts.append(xform(cyl((0, 0.4, 0.6), (0, 0.4, 13.0), 0.07, 0.05, 6), M=R, t=t, col=rgba((0.6, 0.6, 0.6), 1)[0]))
        sail = (np.array([[0.05, 0.3, 1.6], [0.05, -4.2, 1.8], [0.05, 0.3, 12.6], [0.05, 0.55, 1.4], [0.05, 4.4, 1.3], [0.05, 0.55, 11.0]]), np.array([[0, 1, 2], [3, 4, 5]]))
        parts.append(xform(sail, M=R, t=t, col=rgba((0.9, 0.9, 0.88), 1)[0]))
    obj("Boats", merge(parts), M_VCOL)


# ────────────────────────────────── pháo bông ──────────────────────────────────
def emission_material(name, strength, sampling=True, alpha=False, glossy=1.0):
    m, nt, out = material(name)
    at = N(nt, "ShaderNodeAttribute", attribute_name="Col")
    em = N(nt, "ShaderNodeEmission", Strength=strength)
    if glossy != 1.0:                              # ảnh phản chiếu (trên mặt hồ) nhạt hơn vật thật
        lp = N(nt, "ShaderNodeLightPath")
        mr = N(nt, "ShaderNodeMapRange")
        mr.inputs[3].default_value, mr.inputs[4].default_value = strength, strength * glossy
        L(nt, lp.outputs["Is Glossy Ray"], mr.inputs[0])
        L(nt, mr.outputs[0], em.inputs["Strength"])
    L(nt, at.outputs["Color"], em.inputs[0])
    if alpha:
        tr = N(nt, "ShaderNodeBsdfTransparent")
        mx = N(nt, "ShaderNodeMixShader")
        L(nt, at.outputs["Alpha"], mx.inputs[0])
        L(nt, tr.outputs[0], mx.inputs[1]); L(nt, em.outputs[0], mx.inputs[2])
        L(nt, mx.outputs[0], out.inputs[0])
    else:
        L(nt, em.outputs[0], out.inputs[0])
    if not sampling:
        m.cycles.emission_sampling = "NONE"
    return m


def hue(h):
    """Cầu vồng dịu: h trong [0,1] → RGB tuyến tính."""
    stops = np.array([[0.95, 0.10, 0.36], [0.98, 0.16, 0.10], [1.0, 0.42, 0.04], [1.0, 0.78, 0.06], [0.42, 0.86, 0.12],
                      [0.05, 0.80, 0.55], [0.06, 0.62, 0.95], [0.16, 0.30, 0.98], [0.50, 0.22, 0.95], [0.90, 0.20, 0.80]])
    x = np.clip(h, 0, 1) * (len(stops) - 1)
    i = np.minimum(x.astype(int), len(stops) - 2)
    return lerp(stops[i], stops[i + 1], (x - i)[..., None])


FIRE_O = np.array([0.0, 58.0, LAKE + 1.5])
FIRE_REFL = 0.10 if not NIGHT else 0.45


def build_fireworks():
    strands, heads, glitter = [], [], []
    plumes = 13
    g, k = 9.81, 0.55
    FAN, VK = (60.0, 1.0) if A.frame == "land" else (44.0, 1.22)
    for i, a0 in enumerate(np.linspace(-FAN, FAN, plumes)):
        ns = int(round(48 - 16 * abs(a0) / FAN))
        a = np.radians(a0 + rng.normal(0, 3.0, ns))
        b = np.radians(rng.normal(0, 3.6, ns))
        d = np.stack([np.sin(a) * np.cos(b), np.sin(b), np.cos(a) * np.cos(b)], -1)
        v0 = VK * rng.uniform(26, 37, ns) * (1.0 - 0.10 * (abs(a0) / FAN) ** 2)
        T = rng.uniform(1.7, 2.7, ns)
        o = FIRE_O + [np.sign(a0) * min(abs(a0) / FAN, 1) * 3.0, 0, 0]
        base = hue(np.full(ns, i / (plumes - 1)) + rng.normal(0, 0.035, ns))
        for j in range(ns):
            t = np.linspace(0.02, 1, 22) ** 0.85 * T[j]
            e = 1 - np.exp(-k * t)
            P = o + d[j] * (v0[j] / k) * e[:, None] + np.array([0, 0, -1.0]) * (g * (t / k - e / k ** 2))[:, None]
            f = t / T[j]
            col = np.concatenate([np.tile(base[j], (len(t), 1)) * lerp(0.75, 1.15, f)[:, None], (0.012 + 0.92 * sstep(0.16, 1.0, f) ** 1.5)[:, None]], 1)
            rad = lerp(0.10, 0.045, f ** 0.7)
            strands.append(tube(P, rad, 4, col))
            hc = np.r_[lerp(base[j], [1, 1, 1], 0.55), 1.0]
            heads.append(xform(ball(P[-1], (0.085, 0.085, 0.085), 6, 3), col=hc))
            ng = 3
            ti = rng.integers(12, 22, ng)
            gp = P[ti] + rng.normal(0, 0.55, (ng, 3))
            gc = rgba((1, 1, 1), ng); gc[:, :3] = lerp(base[j], [1, 1, 1], 0.15)
            glitter.append(instances(ball((0, 0, 0), (1, 1, 1), 5, 2), np.tile(np.eye(3) * 0.05, (ng, 1, 1)), gp, gc))
    s = 1.0 if not NIGHT else 0.15
    fo = [obj("FireStrands", merge(strands), emission_material("Fire", 42.0 * s, sampling=False, alpha=True, glossy=FIRE_REFL), shadow=False),
          obj("FireHeads", merge(heads), emission_material("FireHead", 120.0 * s, sampling=False, glossy=FIRE_REFL), shadow=False),
          obj("FireGlitter", merge(glitter), emission_material("FireGlitter", 90.0 * s, sampling=False, glossy=FIRE_REFL), shadow=False)]
    if not NIGHT:
        for ob in fo:
            ob.visible_diffuse = False
    if NIGHT:                                    # ánh pháo hắt lên khu vườn và mặt hồ
        for (x, z, c) in ((-16, 14, (1.0, 0.35, 0.25)), (0, 20, (0.6, 1.0, 0.4)), (16, 14, (0.3, 0.45, 1.0))):
            lt = bpy.data.lights.new("FireGlow", "POINT")
            lt.energy, lt.color, lt.shadow_soft_size = 26000.0, c, 6.0
            ob = bpy.data.objects.new("FireGlow", lt)
            ob.location = (x, FIRE_O[1], z)
            ob.visible_glossy = False            # chỉ hắt sáng, không hiện thành vệt sáng phản chiếu trên mặt hồ
            scene.collection.objects.link(ob)


# ─────────────────────────────── đèn cho cảnh đêm ───────────────────────────────
def build_night_lights(flames):
    warm = (1.0, 0.56, 0.22)
    obj("Flames", (flames[0], flames[1], rgba(warm, len(flames[0]))), emission_material("Flame", 140.0))
    # dây đèn giăng trên lối đi
    bulbs, wires, poles = [], [], []
    ys = np.arange(1.5, 19.0, 3.4)
    for k, y in enumerate(ys):
        for sgn in (-1, 1):
            poles.append(cyl((sgn * 5.2, y, 0), (sgn * 5.2, y, 4.4), 0.035, 0.03, 6))
    spans = []
    for k in range(len(ys) - 1):
        spans.append(((-5.2, ys[k]), (5.2, ys[k + 1])))
        spans.append(((5.2, ys[k]), (-5.2, ys[k + 1])))
    for (a, b) in spans:
        n = 34
        t = np.linspace(0, 1, n)
        P = np.stack([lerp(a[0], b[0], t), lerp(a[1], b[1], t), 4.35 - 0.75 * np.sin(np.pi * t)], -1)
        wires.append(tube(P, 0.006, 3)[:2])
        Pb = P[2:-1:2] - [0, 0, 0.07]
        bulbs.append(Pb)
    Pb = np.concatenate(bulbs)
    obj("Bulbs", instances(ball((0, 0, 0), (1, 1, 1), 6, 3), np.tile(np.eye(3) * 0.035, (len(Pb), 1, 1)), Pb, rgba(warm, len(Pb))), emission_material("Bulb", 110.0, glossy=0.22))
    obj("Wires", merge(wires), principled("Wire", color=(0.02, 0.02, 0.02, 1)), smooth=False)
    obj("Poles", merge(poles), principled("Pole", color=(0.10, 0.075, 0.05, 1), rough=0.6))     # cột đồng sẫm, không bóng (khỏi hắt sáng pháo bông)

    def spot(loc, target, energy, size=math.radians(70), color=warm, blend=0.6):
        lt = bpy.data.lights.new("Spot", "SPOT")
        lt.energy, lt.color, lt.spot_size, lt.spot_blend, lt.shadow_soft_size = energy, color, size, blend, 0.12
        ob = bpy.data.objects.new("Spot", lt)
        ob.location = loc
        ob.rotation_euler = _look(norm(np.asarray(target, float) - np.asarray(loc, float)))
        scene.collection.objects.link(ob)

    # rọi cổng hoa, cô dâu chú rể, và các cây bách
    spot((-3.2, ARCH_Y - 3.0, 0.2), (0, ARCH_Y, 2.4), 240.0, math.radians(60))
    spot((3.2, ARCH_Y - 3.0, 0.2), (0, ARCH_Y, 2.4), 240.0, math.radians(60))
    spot((0, ARCH_Y - 5.0, 3.6), (0, ARCH_Y - 0.3, 1.2), 70.0, math.radians(36), (1.0, 0.8, 0.6))
    for sgn in (-1, 1):
        for y in (4.5, 8.4, 12.3, 16.2, 20.1):
            spot((sgn * (CYP_X - 1.6), y - 1.6, 0.15), (sgn * CYP_X, y, 5.5), 3800.0, math.radians(46), (1.0, 0.62, 0.3))
        for x in (6.6, 9.8, 13.0):
            spot((sgn * x, RAIL_Y - 0.9, 0.1), (sgn * x, RAIL_Y, 1.6), 26.0, math.radians(70))
    canopy = bpy.data.lights.new("Canopy", "AREA")           # ánh ấm dịu toả xuống từ giàn đèn
    canopy.shape, canopy.size, canopy.size_y, canopy.energy, canopy.color = "RECTANGLE", 9.0, 17.0, 1100.0, (1.0, 0.62, 0.30)
    ob = bpy.data.objects.new("Canopy", canopy)
    ob.location = (0, 9.5, 4.7)
    ob.visible_camera = False
    scene.collection.objects.link(ob)
    moon = bpy.data.lights.new("Moon", "SUN")
    az, el = (math.radians(-23), math.radians(15.5)) if A.frame == "land" else (math.radians(-9), math.radians(27))
    md = np.array([math.sin(az) * math.cos(el), math.cos(az) * math.cos(el), math.sin(el)])
    moon.energy, moon.color, moon.angle = 0.8, (0.55, 0.68, 1.0), math.radians(2.0)
    ob = bpy.data.objects.new("Moon", moon)
    ob.rotation_euler = _look(-md)
    scene.collection.objects.link(ob)
    disc_ = ball(CAM + md * 40000.0, (300.0, 300.0, 300.0), 32, 16)
    mo = obj("MoonDisc", (disc_[0], disc_[1], rgba((1.0, 0.95, 0.84), len(disc_[0]))), emission_material("MoonDisc", 22.0, sampling=False, glossy=0.5), shadow=False)
    mo.visible_diffuse = False


def _look(d):
    """Euler để trục −Z của đèn hướng theo d."""
    from mathutils import Vector
    return Vector(tuple(d)).to_track_quat("-Z", "Y").to_euler()


# ──────────────────────────────────── dựng ────────────────────────────────────
t0 = time.time()
build_world()
if "terrain" not in SKIP:
    build_terrain()
    build_lake()
def seed(k):
    """Mỗi nhóm vật thể có dãy ngẫu nhiên riêng, để bốn khung hình dựng ra cùng một khu vườn."""
    global rng
    rng = np.random.default_rng(k)


seed(1)
if "terrain" not in SKIP:
    build_villages()
    build_boats()
seed(2)
flowers, leaves, cores = build_garden()
seed(3)
if "grass" not in SKIP:
    build_grass()
seed(4)
if "trees" not in SKIP:
    build_trees(leaves, cores)
flames = None
seed(5)
if "people" not in SKIP:
    flames = build_seating(flowers, leaves)
    build_arch(flowers, leaves)
    build_couple(flowers)
obj("Flowers", merge(flowers), M_FLOWER)
obj("Leaves", merge(leaves), M_LEAF, smooth=False)
obj("Cores", merge(cores), M_CORE)
seed(6)
if A.fireworks:
    build_fireworks()
if NIGHT and flames is not None:
    build_night_lights(flames)
build_camera()
setup_render()
print("built in %.1fs, objects=%d" % (time.time() - t0, len(bpy.data.objects)))
bpy.ops.render.render(write_still=True)
print("rendered in %.1fs → %s" % (time.time() - t0, A.out))
