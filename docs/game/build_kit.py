"""Kho đồ vật 3D cho game "Về chung một nhà": dựng bằng mã, xuất glTF nhị phân (.glb) vào game/assets/kit/.

    python3 docs/game/build_kit.py                                    # chỉ cần numpy: dựng lại toàn bộ .glb và kit.json
    .venv3d/bin/python docs/game/build_kit.py --preview kho.png       # thêm ảnh bảng kê (cần bpy và Pillow)
    (ảnh góc tiệc ghép từ kho, và sa bàn cho trang thử kỹ thuật: docs/game/build_saban.py)

Quy ước: đơn vị mét, gốc toạ độ ở giữa mặt đáy, trục Z hướng lên (lúc xuất đổi sang trục Y hướng lên của glTF).
Không dùng ảnh chất liệu. Màu nằm ở từng đỉnh (COLOR_0) và đã tô sẵn bóng ở hốc, khe (hàm bake).
Mỗi tệp chia theo chất liệu trong bảng MATS: vải mờ, nhựa bóng, kim loại, kính trong, đèn tự sáng.
Phong cách: hình khối bo tròn; hoa có cánh, lá có gập; khăn bàn có nếp. Mỗi món phải nhận ra được khi nhìn nhỏ.
Thêm món mới: viết một hàm nhận Kit, rồi ghi vào danh sách ITEMS ở cuối tệp.
"""
import argparse
import json
import math
import os
import struct

import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
OUT = os.path.join(ROOT, "game", "assets", "kit")
PAL = dict(gold="#D8B36A", gold_d="#B08A45", cream="#F7EFE2", white="#FDFBF7", jade="#1E5A40", jade_l="#8FC2A6", leaf="#6BA95C",
           leaf_d="#3E8050", leaf_l="#A5CF7B", tulip="#F48FA8", pink_l="#FBD3DC", rose="#E55D82", peach="#F9C4A0", coral="#F08A6B",
           sky="#9CCDEE", blue="#3C78C8", lilac="#C9B1EA", butter="#FBE6A6", red="#D4362C", red_d="#A32620", wood="#C08E5E",
           wood_d="#8A5F3C", terra="#CF7F56", grey="#C9CDD2", steel="#AEB6BD", dark="#2E3A36", ink="#12261C", yellow="#FFD777",
           glass="#E3F2F7", fizz="#EDBB4F", flame="#FFB648", orange="#F29A38", lime="#B8D65A", grass="#A9D686", grass_d="#7FBA68", leaf_m="#559659")
PAL = {k: np.array([int(v[i:i + 2], 16) / 255 for i in (1, 3, 5)]) for k, v in PAL.items()}
# chất liệu: (kim loại, độ nhám, độ đục, màu tự sáng, cường độ sáng trong ảnh xem trước)
MATS = {"matte": (0, 0.85, 1, None, 0), "satin": (0, 0.36, 1, None, 0), "metal": (1, 0.3, 1, None, 0), "glass": (0, 0.05, 0.28, None, 0),
        "glow": (0, 0.6, 1, (1.0, 0.74, 0.38), 3), "lantern": (0, 0.6, 1, (0.6, 0.09, 0.04), 1.1)}
MKEYS = list(MATS)
MAT_OF = {"gold": "metal", "gold_d": "metal", "steel": "metal", "glass": "glass", "flame": "glow", "yellow": "glow"}   # chất liệu mặc định theo tên màu
rng = np.random.default_rng(7)


def rotx(a): c, s = math.cos(a), math.sin(a); return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])
def roty(a): c, s = math.cos(a), math.sin(a); return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])
def rotz(a): c, s = math.cos(a), math.sin(a); return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])


def frame(axis):
    """Ma trận xoay đưa trục Z cục bộ về hướng axis."""
    w = np.asarray(axis, float); w = w / np.linalg.norm(w)
    u = np.cross([0, 0, 1.0] if abs(w[2]) < 0.9 else [1.0, 0, 0], w); u /= np.linalg.norm(u)
    return np.stack([u, np.cross(w, u), w], 1)


def circle(R, n):
    a = np.arange(n) * 2 * np.pi / n
    return np.c_[R * np.cos(a), R * np.sin(a)]


def rrect(w, d, r, step=0.05):
    """Đường viền chữ nhật bo góc, các điểm cách đều khoảng step."""
    P = np.array([(cx + r * math.cos(math.radians(a0 + 15 * k)), cy + r * math.sin(math.radians(a0 + 15 * k)))
                  for cx, cy, a0 in ((w / 2 - r, d / 2 - r, 0), (-w / 2 + r, d / 2 - r, 90), (-w / 2 + r, -d / 2 + r, 180), (w / 2 - r, -d / 2 + r, 270))
                  for k in range(7)])
    out = []
    for i in range(len(P)):
        a, b = P[i], P[(i + 1) % len(P)]; m = max(1, int(np.linalg.norm(b - a) / step))
        out += [a + (b - a) * j / m for j in range(m)]
    return np.array(out)


def _sphere(nu, nv):
    th = np.linspace(0, np.pi, nv + 1)[1:-1]; a = np.arange(nu) * 2 * np.pi / nu
    V = [[0, 0, 1.0]] + [[math.sin(t) * math.cos(x), math.sin(t) * math.sin(x), math.cos(t)] for t in th for x in a] + [[0, 0, -1.0]]
    F = [[0, 1 + j, 1 + (j + 1) % nu] for j in range(nu)]
    for i in range(nv - 2):
        for j in range(nu):
            p, q = 1 + i * nu + j, 1 + i * nu + (j + 1) % nu
            F += [[p, p + nu, q + nu], [p, q + nu, q]]
    last = 1 + (nv - 2) * nu
    return np.array(V), F + [[last + j, len(V) - 1, last + (j + 1) % nu] for j in range(nu)]


class Kit:
    """Gom các khối cơ bản thành một lưới: vị trí, pháp tuyến, màu đỉnh, tam giác, chất liệu của từng tam giác."""

    def __init__(self):
        self.P, self.N, self.C, self.I, self.T, self.A, self.n, self.mat, self.aow = [], [], [], [], [], [], 0, None, 1.0

    def m(self, mat=None):
        """Ép chất liệu cho các khối thêm sau đó; gọi không tham số để trả về mặc định (theo tên màu, không thì vải mờ)."""
        self.mat = mat
        return self

    def _push(self, P, N, C, I, name=None):
        mat = self.mat or MAT_OF.get(name, "matte")
        self.P.append(P); self.N.append(N); self.C.append(C); self.I.append(np.asarray(I) + self.n)
        self.T.append(np.full(len(I), MKEYS.index(mat))); self.A.append(np.full(len(P), self.aow)); self.n += len(P)
        return self

    def add(self, V, F, col, smooth=True, M=None, t=None, ref=None, nrm=None):
        """col: tên màu, một màu RGB, hoặc mảng màu cho từng đỉnh."""
        V, F = np.asarray(V, float), np.asarray(F, int)
        if M is not None:
            V = V @ np.asarray(M).T
            nrm = None if nrm is None else np.asarray(M) @ np.asarray(nrm, float)
        if t is not None:
            V = V + np.asarray(t, float)
        fn = np.cross(V[F[:, 1]] - V[F[:, 0]], V[F[:, 2]] - V[F[:, 0]])
        # chiều quay của tam giác: mặt phải hướng ra ngoài (theo nrm nếu là mặt phẳng, không thì tính từ tâm khối)
        if nrm is not None:
            out = float((fn @ np.asarray(nrm, float)).sum())
        else:
            c = V.mean(0) if ref is None else (np.asarray(ref, float) if M is None and t is None else V.mean(0))
            out = float((fn * (V[F].mean(1) - c)).sum())
        if out < 0:
            F, fn = F[:, ::-1], -fn
        name = col if isinstance(col, str) else None
        c = PAL[col] if name else np.asarray(col, float)
        if smooth:
            N = np.zeros_like(V)
            for k in range(3):
                np.add.at(N, F[:, k], fn)
            P, I, C = V, F, (c if c.ndim == 2 else np.tile(c, (len(V), 1)))
        else:
            P, N, I = V[F].reshape(-1, 3), np.repeat(fn, 3, 0), np.arange(len(F) * 3).reshape(-1, 3)
            C = c[F].reshape(-1, 3) if c.ndim == 2 else np.tile(c, (len(P), 1))
        return self._push(P, N / (np.linalg.norm(N, axis=1, keepdims=True) + 1e-12), C, I, name)

    def merge(self, other, s=1.0, t=(0, 0, 0)):
        """Ghép một món đã dựng (Kit khác) vào món này, thu phóng s và dời t."""
        P, N, C, I, T = other.arrays()
        self.P.append(P * s + np.asarray(t, float)); self.N.append(N); self.C.append(C); self.I.append(I + self.n); self.T.append(T)
        self.A.append(np.concatenate(other.A)); self.n += len(P)
        return self

    # ── khối cơ bản ──
    def lathe(self, profile, col, n=20, hard=False, facet=False, **kw):
        """Tiện tròn quanh trục Z. profile = [(bán kính, cao), …] đi từ đáy lên. hard: giữ cạnh sắc giữa các đoạn. facet: giữ cạnh sắc quanh trục."""
        P = np.asarray(profile, float)
        segs = [P[i:i + 2] for i in range(len(P) - 1)] if hard else [P]
        a = np.arange(n) * 2 * np.pi / n
        for S in segs:
            if hard and np.allclose(S[0], S[1]):
                continue
            m = len(S)
            V = np.stack([np.outer(S[:, 0], np.cos(a)), np.outer(S[:, 0], np.sin(a)), np.repeat(S[:, 1][:, None], n, 1)], -1).reshape(-1, 3)
            F = []
            for i in range(m - 1):
                for j in range(n):
                    p, q = i * n + j, i * n + (j + 1) % n
                    F += [[p, q, q + n], [p, q + n, p + n]]
            flat = hard and abs(S[1, 1] - S[0, 1]) < 1e-9          # vành ngang: hướng lên hay xuống tuỳ chiều đi của profile
            self.add(V, F, col, not facet, nrm=(0, 0, 1 if S[1, 0] < S[0, 0] else -1) if flat else None,
                     ref=None if flat else (0, 0, float(S[:, 1].mean())), **kw)
        return self

    def rbox(self, w, d, h, col, r=0.02, seg=3, t=(0, 0, 0), M=None, bev=0.0):
        """Hộp bo góc đứng (mặt cắt chữ nhật bo tròn), đáy ở z = 0 của hệ cục bộ. bev: vát mép trên."""
        r = min(r, w / 2 - 1e-4, d / 2 - 1e-4)
        pts = []
        for cx, cy, a0 in ((w / 2 - r, d / 2 - r, 0), (-w / 2 + r, d / 2 - r, 90), (-w / 2 + r, -d / 2 + r, 180), (w / 2 - r, -d / 2 + r, 270)):
            for k in range(seg + 1):
                a = math.radians(a0 + 90 * k / seg)
                pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        pts = np.array(pts); n = len(pts)
        rings = [(pts, 0.0), (pts, h - bev)] + ([(pts * (1 - 2 * bev / np.array([w, d])), h)] if bev else [])
        V = np.concatenate([np.c_[p, np.full(n, z)] for p, z in rings]); F = []
        for i in range(len(rings) - 1):
            for j in range(n):
                p, q = i * n + j, i * n + (j + 1) % n
                F += [[p, q, q + n], [p, q + n, p + n]]
        self.add(V, F, col, True, M, t)
        fan = [[0, j, j + 1] for j in range(1, n - 1)]
        self.add(np.c_[rings[-1][0], np.full(n, h)], fan, col, False, M, t, nrm=(0, 0, 1))
        return self.add(np.c_[pts, np.zeros(n)], fan, col, False, M, t, nrm=(0, 0, -1))

    def cyl(self, p0, p1, r0, col, r1=None, n=10, caps=True, facet=False):
        """Trụ (hoặc nón cụt) nối hai điểm. n = 4 và facet: thanh vuông."""
        p0, p1 = np.asarray(p0, float), np.asarray(p1, float)
        r1 = r0 if r1 is None else r1
        w = p1 - p0; w = w / np.linalg.norm(w)
        u = np.cross(w, [0, 0, 1.0] if abs(w[2]) < 0.9 else [1.0, 0, 0]); u /= np.linalg.norm(u); v = np.cross(w, u)
        a = np.arange(n) * 2 * np.pi / n
        ring = np.outer(np.cos(a), u) + np.outer(np.sin(a), v)
        V = np.concatenate([p0 + ring * r0, p1 + ring * r1])
        F = []
        for j in range(n):
            p, q = j, (j + 1) % n
            F += [[p, q, q + n], [p, q + n, p + n]]
        self.add(V, F, col, not facet, ref=(p0 + p1) / 2)
        if caps:
            fan = [[0, j, j + 1] for j in range(1, n - 1)]
            if r0 > 1e-4: self.add(p0 + ring * r0, fan, col, False, nrm=-w)
            if r1 > 1e-4: self.add(p1 + ring * r1, fan, col, False, nrm=w)
        return self

    def ball(self, c, rad, col, nu=10, nv=7, M=None, pre=None):
        V, F = _sphere(nu, nv)
        V = V * np.broadcast_to(np.asarray(rad, float), (3,))
        if pre is not None:
            V = V + np.asarray(pre, float)                         # dời trước khi xoay (ví dụ cánh quạt quanh trục)
        if M is not None:
            V = V @ np.asarray(M).T
        return self.add(V + np.asarray(c, float), F, col, True)

    def tube(self, path, r, col, n=8, closed=False):
        """Ống tròn uốn theo một đường gấp khúc."""
        P = np.asarray(path, float); m = len(P)
        T = np.gradient(P, axis=0) if not closed else (np.roll(P, -1, 0) - np.roll(P, 1, 0))
        T /= np.linalg.norm(T, axis=1, keepdims=True)
        u = np.cross(T[0], [0, 0, 1.0] if abs(T[0][2]) < 0.9 else [1.0, 0, 0]); u /= np.linalg.norm(u)
        a = np.arange(n) * 2 * np.pi / n; V = []
        for i in range(m):
            u = u - T[i] * (u @ T[i]); u /= np.linalg.norm(u); v = np.cross(T[i], u)
            V.append(P[i] + r * (np.outer(np.cos(a), u) + np.outer(np.sin(a), v)))
        V = np.concatenate(V); F = []
        for i in range(m if closed else m - 1):
            for j in range(n):
                p, q, k = i * n + j, i * n + (j + 1) % n, ((i + 1) % m) * n
                F += [[p, q, k + (j + 1) % n], [p, k + (j + 1) % n, k + j]]
        F = np.array(F); Vc = np.repeat(P, n, 0)                   # hướng ra ngoài = từ tâm ống ra
        fn = np.cross(V[F[:, 1]] - V[F[:, 0]], V[F[:, 2]] - V[F[:, 0]])
        if float((fn * (V[F].mean(1) - Vc[F].mean(1))).sum()) < 0:
            F = F[:, ::-1]
        N = V - Vc; N /= np.linalg.norm(N, axis=1, keepdims=True) + 1e-12
        name = col if isinstance(col, str) else None
        return self._push(V, N, np.tile(PAL[col] if name else np.asarray(col, float), (len(V), 1)), F, name)

    def ringz(self, R, r, z, col, nu=18, n=6, c=(0, 0)):
        a = np.arange(nu) * 2 * np.pi / nu
        return self.tube(np.c_[c[0] + R * np.cos(a), c[1] + R * np.sin(a), np.full(nu, z)], r, col, n, closed=True)

    # ── vải, hoa, lá ──
    def cloth(self, outline, z1, z0, col, flare=0.04, amp=0.03, folds=12, rows=5):
        """Khăn phủ rủ từ đường viền mặt bàn (z1) xuống gần sàn (z0): càng xuống càng xoè và gợn nếp."""
        O = np.asarray(outline, float); n = len(O)
        T = np.roll(O, -1, 0) - np.roll(O, 1, 0); Nn = np.c_[T[:, 1], -T[:, 0]]; Nn /= np.linalg.norm(Nn, axis=1, keepdims=True)
        seg = np.linalg.norm(np.roll(O, -1, 0) - O, axis=1); s = np.concatenate([[0], np.cumsum(seg)[:-1]]) / seg.sum()
        wave = np.sin(2 * np.pi * folds * s) + 0.4 * np.sin(2 * np.pi * (folds // 3) * s + 1.3) + 0.6
        V = []
        for v in np.linspace(0, 1, rows + 1):
            e = v ** 1.4
            V.append(np.c_[O + Nn * (0.012 * min(v * rows, 1) + flare * e + amp * e * wave)[:, None], np.full(n, z1 - (z1 - z0) * v)])
        V = np.concatenate(V); F = []
        for i in range(rows):
            for j in range(n):
                p, q = i * n + j, i * n + (j + 1) % n
                F += [[p, q, q + n], [p, q + n, p + n]]
        self.add(V, F, col, True, ref=(O[:, 0].mean(), O[:, 1].mean(), (z0 + z1) / 2))
        top = np.r_[[[O[:, 0].mean(), O[:, 1].mean(), z1]], np.c_[O, np.full(n, z1)]]
        return self.add(top, [[0, 1 + j, 1 + (j + 1) % n] for j in range(n)], col, False, nrm=(0, 0, 1))

    def petal(self, M, c, phi, L, W, th0, th1, cup, col, tip=None, nv=3, leaf=False):
        """Một cánh hoa (hoặc lá) mọc từ c. M: hệ trục của bông (Z = trục bông). phi: hướng quanh trục. th0 → th1: góc ngả so với trục,
        từ gốc tới ngọn (0 = dựng đứng, π/2 = xoè ngang). cup: độ khum của mép. Màu chuyển từ col ở gốc sang tip ở ngọn."""
        v = np.linspace(0, 1, nv + 1); th = th0 + (th1 - th0) * v; mid = (th[:-1] + th[1:]) / 2
        r = np.concatenate([[0], np.cumsum(np.sin(mid))]) * L / nv; z = np.concatenate([[0], np.cumsum(np.cos(mid))]) * L / nv
        w = W / 2 * (np.sin(np.pi * v ** 0.8) ** 0.8 if leaf else np.sin(np.pi * (0.12 + 0.8 * v)) ** 0.7)
        V = []
        for i in range(nv + 1):
            for u in (-1, 0, 1):
                d = cup * w[i] * u * u
                V.append((r[i] - d * math.cos(th[i]), u * w[i], z[i] + d * math.sin(th[i])))
        V = np.array(V) @ rotz(phi).T @ np.asarray(M).T + np.asarray(c, float)
        F = []
        for i in range(nv):
            for j in range(2):
                p = i * 3 + j
                F += [[p, p + 1, p + 4], [p, p + 4, p + 3]]
        c0 = PAL[col] if isinstance(col, str) else np.asarray(col, float)
        c1 = c0 if tip is None else (PAL[tip] if isinstance(tip, str) else np.asarray(tip, float))
        self.aow = 0.3                                              # cánh mỏng xếp sát nhau: tô bóng nhẹ thôi, kẻo hoa xám
        self.add(V, F, c0 + (c1 - c0) * np.repeat(v, 3)[:, None]); self.aow = 1.0
        return self

    def rose(self, c, axis, R, col, lod=1):
        """Hoa hồng bán kính R: ba vòng cánh từ khép tới xoè. lod = 0: bản gọn cho hoa nhỏ hoặc ở xa."""
        M = frame(axis); c = np.asarray(c, float); base = PAL[col]; lite = base + (1 - base) * 0.35; spin = rng.uniform(0, 6.28)
        deep = base * (0.93, 0.78, 0.80)                            # gốc cánh ngả hồng ấm chứ không xám
        rings = ((4, 0.10, 0.35, 0.85, 0.80, 0.9), (5, 0.45, 1.0, 1.05, 1.05, 0.6), (6, 0.9, 1.5, 1.1, 1.2, 0.35))
        for q, (n, t0, t1, L, W, cup) in enumerate(rings if lod else rings[1:]):
            for i in range(n):
                self.petal(M, c, spin + q * 0.7 + i * 2 * math.pi / n, L * R, W * R, t0, t1, cup, deep * (0.9 + 0.05 * q), lite, nv=3 if lod else 2)
        return self.ball(c + M[:, 2] * R * 0.36, R * (0.3 if lod else 0.42), deep * 0.86, 6, 4)

    def tulip(self, c, axis, R, col, lod=1):
        """Hoa tulip: sáu cánh khum thành hình quả trứng, bán kính R, cao khoảng 3R."""
        M = frame(axis); base = PAL[col]; spin = rng.uniform(0, 6.28)
        for q in range(2):
            for i in range(3):
                self.petal(M, c, spin + q * math.pi / 3 + i * 2 * math.pi / 3, 3.4 * R, 1.9 * R, 0.75 - 0.08 * q, -0.28, 0.55,
                           base * (0.78 + 0.1 * q), base + (1 - base) * 0.35, nv=4 if lod else 3)
        return self

    def foliage(self, c, rad, cols=("leaf", "leaf_d", "leaf_l"), nu=12, nv=8, rough=0.14):
        """Tán lá: khối cầu gồ ghề, mỗi mặt một sắc xanh."""
        V, F = _sphere(nu, nv); F = np.array(F)
        d = np.sin(V @ (rng.normal(0, 1, (3, 3)) * 3.2).T + rng.uniform(0, 6.28, 3)).mean(1)
        V = V * (1 + rough * d[:, None])
        fc = np.array([PAL[x] for x in cols])[rng.integers(0, len(cols), len(F))] * (0.84 + 0.16 * (V[F].mean(1)[:, 2:3] + 1) / 2)
        Vx = V[F].reshape(-1, 3) * np.broadcast_to(np.asarray(rad, float), (3,)) + np.asarray(c, float)
        return self.add(Vx, np.arange(len(Vx)).reshape(-1, 3), np.repeat(fc, 3, 0), smooth=False)

    def bow(self, c, s, col, yaw=0.0):
        """Nơ: hai vòng, một nút, hai dải rủ. s: cỡ nửa bề ngang."""
        c = np.asarray(c, float); R = rotz(yaw); D = frame((0, 0, -1))
        for sg in (-1, 1):
            self.ball(c + R @ np.array((sg * s * 0.52, 0, 0.02 * s)), (s * 0.52, s * 0.2, s * 0.34), col, 8, 5, M=R @ roty(-sg * 0.3))
            self.petal(D, c, sg * math.pi / 2 - yaw, s * 1.5, s * 0.42, 0.25, 0.75, 0.2, col, nv=2)
        return self.ball(c, s * 0.2, col, 6, 4)

    def heart(self, c, s, col, M=None, th=0.012):
        """Trái tim dẹt rộng s, đứng trong mặt phẳng XZ cục bộ, dày th theo Y."""
        t = np.linspace(0, 2 * np.pi, 28, endpoint=False); n = len(t)
        X = 16 * np.sin(t) ** 3 * s / 32; Z = (13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t) + 2.5) * s / 32
        V = np.concatenate([np.c_[X, np.full(n, y), Z] for y in (-th / 2, th / 2)])
        F = [[j, (j + 1) % n, (j + 1) % n + n] for j in range(n)] + [[j, (j + 1) % n + n, j + n] for j in range(n)]
        self.add(V, F, col, True, M, c)
        for y, sg in ((-th / 2, -1), (th / 2, 1)):
            self.add(np.r_[[[0, y, 0]], np.c_[X, np.full(n, y), Z]], [[0, 1 + j, 1 + (j + 1) % n] for j in range(n)], col, False, M, c, nrm=(0, sg, 0))
        return self

    def arrays(self):
        return np.concatenate(self.P), np.concatenate(self.N), np.concatenate(self.C), np.concatenate(self.I), np.concatenate(self.T)


FLOWERS = ["white", "pink_l", "tulip", "peach", "white", "rose"]


# ─────────────────────────────── cụm dùng chung ───────────────────────────────
def posy(k, c, R, n, size, cols=FLOWERS, tmax=1.25, leaves=8, lod=1, up=(0, 0, 1), kind="rose"):
    """Cụm hoa hình vòm bán kính R quanh c: n bông hướng ra ngoài, lá xoè quanh chân vòm."""
    M = frame(up); c = np.asarray(c, float)
    for i in range(n):
        t = tmax * math.sqrt((i + 0.35) / n); a = i * 2.39996
        d = M @ np.array((math.sin(t) * math.cos(a), math.sin(t) * math.sin(a), math.cos(t)))
        s = size * rng.uniform(0.85, 1.12)
        getattr(k, kind)(c + d * (R - s * 0.35), d, s, cols[(i * 2 + i // 3) % len(cols)], lod)
    for i in range(leaves):
        k.petal(M, c, i * 2 * math.pi / leaves + 0.3, R * 1.55, R * 0.62, 1.1, 1.75, -0.25, "leaf_d", "leaf", nv=2, leaf=True)


def pot(k, r=0.2, h=0.3, col="terra"):
    k.m(None if col == "terra" else "satin")
    k.lathe([(0, 0), (r * 0.72, 0), (r, h * 0.86), (r * 1.08, h * 0.86), (r * 1.08, h), (r * 0.9, h), (r * 0.9, h * 0.9)], col, 14, hard=True)
    return k.m().lathe([(r * 0.9, h * 0.9), (0, h * 0.9)], "wood_d", 14, hard=True)


def plate(k, at, r=0.125):
    k.m("satin").lathe([(0, 0), (r * 0.6, 0), (r, 0.016), (r * 0.62, 0.006), (0, 0.006)], "white", 14, t=at).m()
    k.ringz(r, 0.0035, at[2] + 0.016, "gold", 14, 4, c=at[:2])


def candle(k, at, h=0.16, r=0.012):
    at = np.asarray(at, float)
    k.lathe([(0, 0), (r * 2.4, 0), (r * 2.4, 0.006), (r * 1.2, 0.014), (0, 0.014)], "gold", 10, hard=True, t=at)
    k.cyl(at + (0, 0, 0.014), at + (0, 0, h), r, "cream", n=8)
    k.ball(at + (0, 0, h + 0.022), (r * 0.6, r * 0.6, 0.02), "flame", 6, 5)


def fruit(k, c, r, col):
    c = np.asarray(c, float)
    k.m("satin").ball(c, (r, r, r * 0.92), col, 9, 7).m()
    k.cyl(c + (0, 0, r * 0.85), c + (0, 0, r * 1.15), r * 0.07, "wood_d", n=4, caps=False)
    k.petal(frame((0, 0, 1)), c + (0, 0, r * 0.95), rng.uniform(0, 6.28), r * 0.9, r * 0.45, 1.0, 1.5, -0.2, "leaf_d", "leaf", nv=2, leaf=True)


# ─────────────────────────────── đồ vật ───────────────────────────────
def ghe_chiavari(k):
    g = 0.018
    for x in (-0.18, 0.18):
        k.cyl((x, -0.18, 0), (x, -0.18, 0.45), g, "gold", n=8)                          # chân trước
        k.cyl((x, 0.18, 0), (x * 0.94, 0.215, 0.93), g, "gold", n=8)                    # chân sau kiêm trụ lưng
        k.cyl((x, -0.18, 0.17), (x, 0.185, 0.17), 0.011, "gold", n=6, caps=False)
        k.ball((x * 0.94, 0.215, 0.945), 0.024, "gold", 8, 6)
    for z, y in ((0.17, -0.18), (0.92, 0.213), (0.74, 0.205), (0.56, 0.197)):
        k.cyl((-0.18, y, z), (0.18, y, z), 0.014 if z > 0.3 else 0.011, "gold", n=6)
    for x in (-0.11, -0.055, 0, 0.055, 0.11):
        k.cyl((x, 0.198, 0.56), (x, 0.212, 0.92), 0.009, "gold", n=6, caps=False)
    k.rbox(0.41, 0.41, 0.03, "gold", 0.05, t=(0, 0, 0.44))
    k.rbox(0.37, 0.37, 0.05, "white", 0.09, t=(0, -0.005, 0.47), bev=0.018)             # đệm
    k.m("satin").bow((0, 0.245, 0.72), 0.085, "tulip", math.pi).m()                     # nơ sau lưng ghế


def ban_tron(k):
    k.cloth(circle(0.82, 84), 0.76, 0.03, "white", 0.035, 0.03, 14)
    k.lathe([(0, 0.762), (0.045, 0.762), (0.045, 0.776), (0, 0.776)], "steel", 10, hard=True)
    k.lathe([(0, 0.776), (0.40, 0.776), (0.40, 0.786), (0, 0.786)], "glass", 24, hard=True)       # mâm xoay kính
    for i in range(10):
        plate(k, (0.63 * math.cos(i * math.pi / 5), 0.63 * math.sin(i * math.pi / 5), 0.762))
    k.lathe([(0, 0.786), (0.07, 0.786), (0.10, 0.83), (0.09, 0.83), (0, 0.80)], "gold", 14)       # bát hoa giữa bàn
    posy(k, (0, 0, 0.84), 0.12, 8, 0.055, leaves=7)


def ban_dai(k):
    k.cloth(rrect(1.84, 0.80, 0.06), 0.76, 0.03, "white", 0.03, 0.022, 20)
    k.rbox(1.96, 0.30, 0.006, "jade_l", 0.01, t=(0, 0, 0.761))                          # khăn chạy dọc bàn, rủ hai đầu
    for s in (-1, 1):
        k.rbox(0.006, 0.30, 0.30, "jade_l", 0.002, t=(s * 0.978, 0, 0.465))
        candle(k, (s * 0.42, 0.06, 0.767), 0.22); candle(k, (s * 0.52, -0.05, 0.767), 0.16)
    k.lathe([(0, 0.767), (0.06, 0.767), (0.085, 0.80), (0.075, 0.80), (0, 0.78)], "gold", 12)
    posy(k, (0, 0, 0.81), 0.10, 7, 0.05, leaves=6)


def ghe_dau_nhua(k, col="red"):
    k.m("satin")
    k.rbox(0.30, 0.30, 0.03, col, 0.06, t=(0, 0, 0.43), bev=0.01)                       # mặt ghế
    for sx in (-1, 1):
        for sy in (-1, 1):                                                              # bốn chân choãi
            k.cyl((sx * 0.175, sy * 0.175, 0), (sx * 0.118, sy * 0.118, 0.44), 0.034, col, 0.028, n=4, facet=True)
    k.lathe([(0.214, 0.33), (0.195, 0.44)], col, 4, facet=True, M=rotz(math.pi / 4))    # yếm dưới mặt ghế
    k.lathe([(0.232, 0.15), (0.226, 0.185)], col, 4, facet=True, M=rotz(math.pi / 4))   # đai giằng chân
    k.m().lathe([(0.024, 0.4603), (0, 0.4603)], "ink", 10, hard=True)                   # lỗ giữa mặt ghế


def ban_ca_phe(k):
    k.m("satin").lathe([(0, 0), (0.22, 0), (0.22, 0.02), (0.035, 0.05), (0.03, 0.70), (0, 0.70)], "dark", 14, hard=True).m()
    k.lathe([(0, 0.70), (0.33, 0.70), (0.345, 0.715), (0.33, 0.73), (0, 0.73)], "wood", 24)


GLASS = [(0, 0), (0.034, 0), (0.034, 0.004), (0.004, 0.012), (0.004, 0.09), (0.018, 0.10), (0.036, 0.125), (0.04, 0.165), (0.036, 0.20), (0.032, 0.20)]


def ly_ruou(k, at=(0, 0, 0), n=12):
    k.lathe(GLASS, "glass", n, t=at)
    k.m("satin").lathe([(0, 0.105), (0.02, 0.105), (0.033, 0.125), (0.037, 0.165), (0, 0.165)], "fizz", n, t=at).m()


def thap_ly(k):
    k.lathe([(0, 0), (0.30, 0), (0.30, 0.03), (0, 0.03)], "gold", 20, hard=True)
    z = 0.03
    for lv in (4, 3, 2, 1):
        o = (lv - 1) * 0.085 / 2
        for i in range(lv):
            for j in range(lv):
                ly_ruou(k, (i * 0.085 - o, j * 0.085 - o, z), 8)
        z += 0.2


def banh_cuoi(k):
    k.lathe([(0, 0), (0.13, 0), (0.13, 0.01), (0.03, 0.03), (0.03, 0.09), (0.22, 0.10), (0.22, 0.115), (0, 0.115)], "gold", 20, hard=True)
    z = 0.115
    for r, c in ((0.17, "white"), (0.125, "cream"), (0.085, "white")):
        k.m("satin").lathe([(0, z), (r, z), (r, z + 0.088), (r - 0.012, z + 0.10), (0, z + 0.10)], c, 24)
        for a in np.linspace(0, 2 * np.pi, int(r * 150), endpoint=False):                # viền kem bắt bông
            k.ball((r * math.cos(a), r * math.sin(a), z + 0.008), 0.011, "white", 5, 3)
        k.m().ringz(r + 0.001, 0.004, z + 0.052, "gold", 24, 4)
        z += 0.10
    posy(k, (0, 0, z + 0.005), 0.05, 4, 0.036, ["tulip", "pink_l", "rose", "white"], tmax=1.0, leaves=5, lod=0)
    for i, (r, zz) in enumerate(((0.105, 0.315), (0.15, 0.215), (0.197, 0.115))):       # hoa đổ chéo xuống từng bậc
        for j in range(2):
            a = -1.9 + i * 0.35 + j * 0.42; d = np.array((math.cos(a), math.sin(a), 0.0))
            k.rose(d * r + (0, 0, zz + 0.01), d * 0.8 + (0, 0, 0.6), 0.03, ["rose", "pink_l", "tulip"][(i + j) % 3], 0)


def cong_hoa(k):
    R, H = 1.05, 1.2
    a = np.linspace(0, np.pi, 21)
    path = np.concatenate([[[R, 0, 0]], np.c_[R * np.cos(a), np.zeros(21), H + R * np.sin(a)], [[-R, 0, 0]]])
    k.tube(path, 0.028, "gold", 8)
    for x in (-R, R):
        k.lathe([(0, 0), (0.16, 0), (0.16, 0.02), (0.03, 0.04)], "gold", 14, hard=True, t=(x, 0, 0))
    d = np.linalg.norm(np.diff(path, axis=0), axis=1); s = np.concatenate([[0], np.cumsum(d)]) / d.sum()
    # mảng hoa lệch: dày ở vai trái vắt qua đỉnh, thêm một cụm nhỏ ở chân phải
    for i, u in enumerate(np.concatenate([np.linspace(0.30, 0.86, 30), np.linspace(0.04, 0.14, 7)])):
        p = np.array([np.interp(u, s, path[:, j]) for j in range(3)])
        out = p - (0, 0, H) if p[2] > H else np.array((np.sign(p[0]), 0, 0.0)); out = out / np.linalg.norm(out)
        w = math.sin(math.pi * (u - 0.30) / 0.56) if u > 0.2 else 0.6 * math.sin(math.pi * (u - 0.04) / 0.10)   # 0 ở hai đầu mảng, 1 ở giữa
        for j in range(1 + (w > 0.4) + (w > 0.8)):
            dr = out * rng.uniform(0.2, 0.9) + (0, (-1, 1, 0)[(i + j) % 3] * rng.uniform(0.5, 1.0), rng.uniform(-0.1, 0.4)); dr /= np.linalg.norm(dr)
            k.rose(p + dr * (0.05 + 0.05 * w), dr, (0.07 + 0.06 * w) * rng.uniform(0.85, 1.1), FLOWERS[(i * 3 + j) % len(FLOWERS)], 0)
            lf = rng.normal(0, 1, 3) + out; lf /= np.linalg.norm(lf)
            k.petal(frame(lf), p, rng.uniform(0, 6.28), 0.2 + 0.12 * w, 0.09, 0.9, 1.4, -0.25, "leaf_d", "leaf", nv=2, leaf=True)


def binh_hoa(k):
    k.m("satin").lathe([(0, 0), (0.06, 0), (0.10, 0.07), (0.105, 0.14), (0.06, 0.25), (0.045, 0.30), (0.06, 0.33), (0.052, 0.33), (0, 0.30)], "jade_l", 18).m()
    k.ringz(0.047, 0.005, 0.30, "gold", 14, 4)
    for i in range(5):
        a = i * 1.257 + 0.3; lean = 0.10 + 0.05 * (i % 2)
        tip = np.array((lean * math.cos(a), lean * math.sin(a), 0.56 + 0.05 * ((i * 2) % 3))); mid = tip * (0.35, 0.35, 0) + (0, 0, 0.42)
        k.tube([(0, 0, 0.28), mid, tip], 0.006, "leaf_d", 5)
        k.tulip(tip, tip - mid, 0.034, ["tulip", "pink_l", "rose", "white", "peach"][i])
    for i in range(4):
        k.petal(frame((0, 0, 1)), (0, 0, 0.30), i * 1.571 + 0.9, 0.30, 0.07, 0.25, 0.8, -0.3, "leaf_d", "leaf", nv=3, leaf=True)


def bo_hoa(k):
    for i in range(7):                                                                  # cuống
        a = i * 0.9
        k.cyl((0.012 * math.cos(a), 0.012 * math.sin(a), 0), (0.02 * math.cos(a), 0.02 * math.sin(a), 0.2), 0.005, "leaf_d", n=5)
    k.m("satin").lathe([(0.024, 0.045), (0.028, 0.10), (0.036, 0.165)], "white", 10)    # ruy băng quấn cuống
    k.bow((0, -0.04, 0.15), 0.045, "tulip").m()
    posy(k, (0, 0, 0.21), 0.10, 11, 0.042, tmax=1.45, leaves=9)


def mam_qua(k):
    k.m("satin").lathe([(0, 0), (0.11, 0), (0.12, 0.012), (0.05, 0.04), (0.05, 0.085), (0.20, 0.12), (0.225, 0.15), (0.215, 0.15), (0.19, 0.13), (0, 0.13)], "red", 22).m()
    k.ringz(0.222, 0.006, 0.15, "gold", 22, 5); k.ringz(0.117, 0.005, 0.012, "gold", 16, 4)       # mâm bồng sơn son viền vàng
    cols = ["orange", "red", "lime", "butter", "rose", "orange"]
    for n, r, z, s in ((6, 0.125, 0.18, 0.055), (3, 0.062, 0.26, 0.05), (1, 0.0, 0.335, 0.046)):  # trái cây xếp tháp
        for i in range(n):
            a = i * 2 * math.pi / n + n
            fruit(k, (r * math.cos(a), r * math.sin(a), z), s, cols[(i + n) % len(cols)])
    k.m("satin").bow((0, -0.225, 0.135), 0.045, "red").m()


def hop_nhan(k):
    k.rbox(0.07, 0.07, 0.032, "jade", 0.012)
    k.rbox(0.058, 0.058, 0.008, "white", 0.01, t=(0, 0, 0.03))
    k.rbox(0.07, 0.07, 0.022, "jade", 0.012, M=rotx(math.radians(-105)), t=(0, 0.035, 0.034))     # nắp mở
    k.tube([(0.011 * math.cos(a), 0, 0.05 + 0.011 * math.sin(a)) for a in np.arange(14) * 2 * np.pi / 14], 0.0022, "gold", 6, closed=True)
    k.ball((0, 0, 0.064), 0.0045, "glass", 6, 4)


def thung_tien_mung(k):
    k.m("satin").rbox(0.34, 0.26, 0.28, "white", 0.03).m()
    k.rbox(0.36, 0.28, 0.045, "gold", 0.03, t=(0, 0, 0.275), bev=0.008)
    k.rbox(0.16, 0.014, 0.004, "ink", 0.005, t=(0, 0, 0.32))                             # khe bỏ phong bì
    k.m("satin").rbox(0.045, 0.262, 0.284, "tulip", 0.012, t=(-0.09, 0, -0.001))
    k.bow((-0.09, -0.142, 0.215), 0.05, "tulip").heart((0.065, -0.132, 0.12), 0.13, "rose").m()


def chan_nen(k):
    k.lathe([(0, 0), (0.06, 0), (0.06, 0.008), (0.015, 0.03), (0.012, 0.12), (0.028, 0.14), (0.012, 0.16), (0.012, 0.22), (0.04, 0.24), (0.04, 0.25), (0, 0.25)], "gold", 16)
    k.cyl((0, 0, 0.25), (0, 0, 0.43), 0.014, "cream", n=10)
    k.ball((0, 0, 0.455), (0.009, 0.009, 0.022), "flame", 8, 6)


def den_long(k):
    prof = [(0.06, 0.60), (0.15, 0.555), (0.205, 0.44), (0.205, 0.36), (0.15, 0.245), (0.06, 0.20)]
    k.cyl((0, 0, 0.62), (0, 0, 0.74), 0.004, "dark", n=5, caps=False)
    k.lathe([(0, 0.60), (0.068, 0.60), (0.068, 0.625), (0, 0.625)], "gold", 14, hard=True)
    k.m("lantern").lathe(prof, "red", 20).m()
    for a in np.arange(10) * 2 * np.pi / 10:                                             # nan đèn
        k.tube([(r * 1.012 * math.cos(a), r * 1.012 * math.sin(a), z) for r, z in prof], 0.004, "gold_d", 4)
    k.lathe([(0, 0.175), (0.068, 0.175), (0.068, 0.20), (0, 0.20)], "gold", 14, hard=True)
    k.cyl((0, 0, 0.175), (0, 0, 0.11), 0.004, "gold", n=5, caps=False); k.ball((0, 0, 0.11), 0.014, "gold", 6, 5)
    k.lathe([(0, 0), (0.014, 0), (0.022, 0.085), (0.008, 0.10), (0, 0.10)], "red", 8)    # tua


def day_den(k):
    k.m("satin")
    for x in (-1.5, 1.5):
        k.lathe([(0, 0), (0.12, 0), (0.12, 0.03), (0.024, 0.05), (0.02, 2.6), (0, 2.6)], "dark", 10, hard=True, t=(x, 0, 0))
    u = np.linspace(-1, 1, 21)
    wire = np.c_[u * 1.5, np.zeros(21), 2.58 - 0.38 * (1 - u ** 2)]
    k.m().tube(wire, 0.006, "dark", 4)
    for p in wire[2:-1:2]:
        k.cyl(p, p - (0, 0, 0.04), 0.012, "dark", n=6)
        k.ball(p - (0, 0, 0.08), (0.04, 0.04, 0.05), "yellow", 8, 6)


def bong_bay(k):
    k.lathe([(0, 0), (0.07, 0), (0.07, 0.03), (0.02, 0.06), (0, 0.06)], "gold", 12, hard=True)
    spots = ((0.0, 0.0, 1.78), (0.26, 0.05, 1.56), (-0.25, -0.04, 1.6), (0.05, -0.24, 1.42), (-0.07, 0.25, 1.44), (0.3, -0.2, 1.28), (-0.3, 0.16, 1.26))
    for (x, y, z), c in zip(spots, ("tulip", "white", "peach", "gold", "pink_l", "rose", "white")):
        k.cyl((0, 0, 0.06), (x, y, z - 0.21), 0.003, "grey", n=4, caps=False)
        k.m(None if c == "gold" else "satin").ball((x, y, z), (0.17, 0.17, 0.205), c, 14, 10)
        k.lathe([(0, 0), (0.014, 0), (0.004, 0.022)], c, 6, t=(x, y, z - 0.226)).m()


def chau_cay_tron(k):
    pot(k, 0.2, 0.3)
    k.cyl((0, 0, 0.27), (0, 0, 0.80), 0.024, "wood_d", n=7, caps=False)
    k.foliage((0, 0, 1.02), 0.30, nu=14, nv=10)
    for a, t in rng.uniform((0, 0.4), (6.28, 2.4), (9, 2)):
        k.foliage((0.22 * math.cos(a) * math.sin(t), 0.22 * math.sin(a) * math.sin(t), 1.02 + 0.22 * math.cos(t)), 0.13, nu=8, nv=6)


def chau_cay_non(k):
    pot(k, 0.2, 0.3)
    for i in range(5):                                                                   # tán cắt tầng
        r = 0.30 - i * 0.052
        k.foliage((0, 0, 0.42 + i * 0.235), (r, r, 0.19), ("leaf_d", "leaf", "leaf_d"), nu=12, nv=7, rough=0.10)
    k.foliage((0, 0, 1.52), (0.05, 0.05, 0.10), ("leaf", "leaf_l"), nu=6, nv=5, rough=0.05)


def chau_hoa(k):
    pot(k, 0.17, 0.22, "white")
    k.foliage((0, 0, 0.26), (0.17, 0.17, 0.10), nu=12, nv=6)
    posy(k, (0, 0, 0.27), 0.15, 9, 0.05, ["tulip", "pink_l", "white", "peach", "rose"], tmax=1.2, leaves=7, lod=0)


def den_duong(k):
    k.m("satin").lathe([(0, 0), (0.17, 0), (0.17, 0.05), (0.08, 0.11), (0.065, 0.5), (0.045, 0.56), (0.04, 2.95), (0, 2.95)], "dark", 12, hard=True)
    k.tube([(0, 0, 2.9), (0, 0, 3.2), (0.12, 0, 3.38), (0.34, 0, 3.42), (0.5, 0, 3.34)], 0.024, "dark", 6)
    k.lathe([(0.09, 0.17), (0.12, 0.19), (0.04, 0.27), (0, 0.28)], "dark", 12, t=(0.5, 0, 3.1))   # chụp đèn
    k.m("glow").lathe([(0, 0.0), (0.08, 0.02), (0.13, 0.10), (0.10, 0.18), (0, 0.18)], "cream", 12, t=(0.5, 0, 3.1)).m()


def ghe_bang(k):
    k.m("satin")
    for x in (-0.62, 0.62):
        k.rbox(0.05, 0.46, 0.40, "dark", 0.012, t=(x, 0, 0))
        k.rbox(0.05, 0.05, 0.44, "dark", 0.012, M=rotx(math.radians(-12)), t=(x, 0.20, 0.40))
    k.m()
    for y in (-0.17, -0.06, 0.05, 0.16):
        k.rbox(1.42, 0.09, 0.03, "wood", 0.012, t=(0, y, 0.40), bev=0.006)
    for z in (0.56, 0.70):
        k.rbox(1.42, 0.03, 0.10, "wood", 0.012, M=rotx(math.radians(-12)), t=(0, 0.215 + (z - 0.4) * 0.21, z))


def wheel(k, c, r=0.16, w=0.05):
    c = np.asarray(c, float)
    k.cyl(c - (w / 2, 0, 0), c + (w / 2, 0, 0), r, "dark", n=16)
    k.cyl(c - (w / 2 + 0.004, 0, 0), c + (w / 2 + 0.004, 0, 0), r * 0.45, "steel", n=10)


def awning(k, w, d, z, tilt, cols, y0=0.0, n=6):
    """Mái bạt sọc: n dải màu xen kẽ, nghiêng về phía trước."""
    for i in range(n):
        x = -w / 2 + w * (i + 0.5) / n
        k.rbox(w / n + 0.002, d, 0.025, cols[i % 2], 0.008, M=rotx(tilt), t=(x, y0, z))
        k.ball((x, y0 - d / 2 * math.cos(tilt) - 0.005, z - d / 2 * math.sin(-tilt) - 0.03), (w / n / 2, 0.012, 0.045), cols[i % 2], 8, 5)   # diềm bạt


def xe_ca_phe(k):
    k.m("satin").rbox(1.25, 0.62, 0.62, "jade", 0.05, t=(0, 0, 0.22)).m()
    k.rbox(1.33, 0.70, 0.04, "wood", 0.03, t=(0, 0, 0.84), bev=0.008)
    k.rbox(1.0, 0.012, 0.36, "cream", 0.03, t=(0, -0.316, 0.36))                         # bảng tên phía trước (để trống)
    k.m("satin").heart((0, -0.325, 0.50), 0.16, "tulip", th=0.008).m()
    for x in (-0.58, 0.58):
        for y in (-0.28, 0.28):
            k.cyl((x, y, 0.88), (x, y, 1.82), 0.014, "gold", n=6)
    awning(k, 1.5, 0.95, 1.86, math.radians(8), ("white", "tulip"), 0.0, 8)
    wheel(k, (-0.66, 0.05, 0.16)); wheel(k, (0.66, 0.05, 0.16))
    k.cyl((-0.3, -0.34, 0.1), (-0.3, -0.34, 0.24), 0.02, "dark", n=6)
    for i, x in enumerate((-0.42, -0.28, -0.14)):                                        # ly giấy
        k.lathe([(0, 0), (0.028, 0), (0.038, 0.10), (0, 0.10)], ("white", "peach", "white")[i], 10, hard=True, t=(x, -0.12, 0.88))
    k.rbox(0.26, 0.3, 0.3, "steel", 0.03, t=(0.34, 0.05, 0.88), bev=0.01)                # máy pha
    k.rbox(0.2, 0.04, 0.02, "dark", 0.008, t=(0.34, -0.12, 0.96))
    k.rbox(0.30, 0.02, 0.38, "ink", 0.01, t=(-0.36, 0.26, 0.88))                         # bảng giá viết phấn (để trống)


def sap_hang(k):
    k.rbox(1.7, 0.8, 0.74, "red", 0.04, t=(0, 0, 0.015))
    k.rbox(1.78, 0.88, 0.03, "wood", 0.02, t=(0, 0, 0.75), bev=0.006)
    for x in (-0.82, 0.82):
        for y in (-0.38, 0.38):
            k.cyl((x, y, 0), (x, y, 2.05 + (0.1 if y > 0 else 0)), 0.018, "dark", n=6)
    awning(k, 2.0, 1.25, 2.12, math.radians(6), ("red", "white"), 0.0, 8)
    for x, c in ((-0.6, "orange"), (-0.2, "lime"), (0.2, "butter"), (0.6, "rose")):      # hàng bày bán
        k.rbox(0.3, 0.3, 0.12, "wood_d", 0.02, t=(x, 0.1, 0.78))
        for dx, dy, dz in rng.uniform(-0.09, 0.09, (7, 3)) * (1, 1, 0.3):
            k.m("satin").ball((x + dx, 0.1 + dy, 0.93 + dz), 0.05, c, 7, 5).m()
    lamp = Kit(); den_long(lamp)
    for x in (-0.7, 0.7):
        k.merge(lamp, 0.5, (x, -0.56, 1.58))                                             # đèn lồng treo trước sạp


def bang_don_khach(k):
    for x, y in ((-0.3, -0.05), (0.3, -0.05), (0, 0.42)):
        k.cyl((x, y, 0), (x * 0.25, 0.12, 1.6), 0.018, "wood", n=6)
    k.rbox(0.74, 0.04, 0.03, "wood", 0.008, t=(0, -0.05, 0.5))
    tilt = rotx(math.radians(-9))
    k.rbox(0.68, 0.025, 0.94, "gold", 0.02, M=tilt, t=(0, -0.03, 0.53))
    k.rbox(0.61, 0.012, 0.87, "white", 0.012, M=tilt, t=(0, -0.047, 0.565))

    def on(x, z):                                                                        # điểm trên mặt bảng: x ngang, z dọc theo bảng
        return tilt @ np.array((x, -0.0065, z)) + (0, -0.047, 0.565)
    k.m("satin").heart(on(0, 0.68), 0.14, "rose", M=tilt, th=0.008).m()
    for z, w, c, h in ((0.52, 0.36, "gold_d", 0.032), (0.45, 0.24, "gold_d", 0.032), (0.36, 0.28, "grey", 0.012), (0.325, 0.20, "grey", 0.012)):
        k.rbox(w, 0.004, h, c, 0.004, M=tilt, t=on(0, z))                                # mấy dòng chữ giả
    posy(k, on(0.24, 0.10) + (0, -0.05, 0), 0.10, 6, 0.05, tmax=1.2, leaves=5, lod=0, up=(0.3, -1, 0.5))


def loa(k):
    k.m("satin")
    for a in (0.5, 2.6, 4.7):
        k.cyl((0, 0, 0.62), (0.42 * math.cos(a), 0.42 * math.sin(a), 0), 0.014, "dark", n=6)
    k.cyl((0, 0, 0.3), (0, 0, 1.0), 0.02, "dark", n=8)
    k.rbox(0.36, 0.32, 0.58, "dark", 0.04, t=(0, 0, 1.0), bev=0.012).m()
    for z, r in ((1.19, 0.12), (1.44, 0.06)):
        k.lathe([(0, 0), (r, 0.0), (r * 0.92, 0.02), (r * 0.3, 0.008), (0, 0.012)], "steel", 16, M=rotx(math.pi / 2), t=(0, -0.16, z))


def micro(k):
    k.m("satin").lathe([(0, 0), (0.14, 0), (0.14, 0.018), (0.025, 0.04), (0.014, 0.045), (0.014, 1.40), (0, 1.40)], "dark", 12, hard=True)
    k.cyl((0, 0, 1.38), (0, -0.09, 1.50), 0.018, "dark", n=8).m()
    k.cyl((0, -0.09, 1.50), (0, -0.115, 1.533), 0.021, "gold", n=8)
    k.ball((0, -0.135, 1.56), 0.04, "steel", 10, 7)


def quat_dung(k):
    k.m("satin").lathe([(0, 0), (0.2, 0), (0.2, 0.02), (0.05, 0.05), (0.02, 0.07), (0.018, 1.05), (0, 1.05)], "grey", 14, hard=True)
    k.ball((0, 0.05, 1.12), (0.07, 0.10, 0.07), "grey", 10, 7)
    for i in range(3):
        k.ball((0, -0.06, 1.12), (0.05, 0.006, 0.105), "sky", 8, 6, M=roty(i * 2 * math.pi / 3), pre=(0, 0, 0.115))
    k.m()
    for y in (-0.10, -0.02):
        a = np.arange(20) * 2 * np.pi / 20
        k.tube(np.c_[0.24 * np.cos(a), np.full(20, y), 1.12 + 0.24 * np.sin(a)], 0.006, "steel", 4, closed=True)
    for a in np.arange(12) * 2 * np.pi / 12:
        k.tube([(0.24 * math.cos(a), -0.02, 1.12 + 0.24 * math.sin(a)), (0.25 * math.cos(a), -0.06, 1.12 + 0.25 * math.sin(a)),
                (0.24 * math.cos(a), -0.10, 1.12 + 0.24 * math.sin(a)), (0.03 * math.cos(a), -0.115, 1.12 + 0.03 * math.sin(a))], 0.004, "steel", 4)


ITEMS = [
    ("ghe-chiavari", "Ghế tiệc Chiavari", ghe_chiavari), ("ban-tron", "Bàn tròn 10 khách", ban_tron), ("ban-dai", "Bàn dài phủ khăn", ban_dai),
    ("ghe-dau-nhua", "Ghế đẩu nhựa đỏ", ghe_dau_nhua), ("ghe-dau-nhua-xanh", "Ghế đẩu nhựa xanh", lambda k: ghe_dau_nhua(k, "blue")),
    ("ban-ca-phe", "Bàn cà phê", ban_ca_phe), ("ly-ruou", "Ly rượu", ly_ruou),
    ("thap-ly", "Tháp ly", thap_ly), ("banh-cuoi", "Bánh cưới ba tầng", banh_cuoi), ("cong-hoa", "Cổng hoa", cong_hoa),
    ("binh-hoa", "Bình hoa tulip", binh_hoa), ("bo-hoa", "Bó hoa cầm tay", bo_hoa), ("mam-qua", "Mâm quả", mam_qua),
    ("hop-nhan", "Hộp nhẫn", hop_nhan), ("thung-tien-mung", "Thùng tiền mừng", thung_tien_mung), ("chan-nen", "Chân nến", chan_nen),
    ("den-long", "Đèn lồng", den_long), ("day-den", "Dây đèn", day_den), ("bong-bay", "Chùm bóng bay", bong_bay),
    ("chau-cay-tron", "Chậu cây tán tròn", chau_cay_tron), ("chau-cay-non", "Chậu cây cắt tầng", chau_cay_non), ("chau-hoa", "Chậu hoa", chau_hoa),
    ("den-duong", "Đèn đường", den_duong), ("ghe-bang", "Ghế băng công viên", ghe_bang), ("xe-ca-phe", "Xe cà phê", xe_ca_phe),
    ("sap-hang", "Sạp chợ đêm", sap_hang), ("bang-don-khach", "Bảng đón khách", bang_don_khach), ("loa", "Loa", loa),
    ("micro", "Micro có chân", micro), ("quat-dung", "Quạt đứng", quat_dung),
]


# ─────────────────────────────── tô bóng sẵn và xuất glTF ───────────────────────────────
def bake(P, N, C, I, T, A):
    """Tô bóng vào màu đỉnh: chỗ nào có bề mặt khác ở gần phía trước mặt (hốc, khe, chỗ tiếp giáp) thì sẫm lại, chân món đồ sẫm hơn
    một chút. Cách tính: rải điểm lên bề mặt, đánh dấu vào lưới ô 3D, làm nhoè, rồi đọc mật độ ở phía trước từng đỉnh."""
    lo = P.min(0); cell = max((P.max(0) - lo).max() / 40, 1e-5); pad = 8
    tri = P[I]; area = np.linalg.norm(np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0]), axis=1) / 2
    idx = np.repeat(np.arange(len(I)), np.clip((area / cell ** 2 * 2).astype(int), 1, 40))
    r = np.random.default_rng(1).random((len(idx), 2)); f = r.sum(1) > 1; r[f] = 1 - r[f]
    S = tri[idx, 0] + (tri[idx, 1] - tri[idx, 0]) * r[:, :1] + (tri[idx, 2] - tri[idx, 0]) * r[:, 1:]
    dim = np.ceil((P.max(0) - lo) / cell).astype(int) + 2 * pad + 1
    G = np.zeros(dim, np.float32); q = ((S - lo) / cell).astype(int) + pad; G[q[:, 0], q[:, 1], q[:, 2]] = 1
    for _ in range(2):
        for ax in range(3):
            G = (np.roll(G, 1, ax) + G + np.roll(G, -1, ax)) / 3
    occ = np.zeros(len(P))
    for d in (3.0, 5.0):
        q = np.clip(((P + N * cell * d - lo) / cell).astype(int) + pad, 0, dim - 1); occ += G[q[:, 0], q[:, 1], q[:, 2]]
    shade = 1 - np.clip(occ * 3.0, 0, 1) * 0.40 * A
    shade *= 0.90 + 0.10 * np.clip((P[:, 2] - lo[2]) / max(P[:, 2].max() - lo[2], 1e-6) * 4, 0, 1)
    lit = np.isin(T, [MKEYS.index(x) for x in ("glow", "lantern", "glass")])             # đèn và kính giữ nguyên màu
    shade[np.unique(I[lit])] = 1
    return C * shade[:, None]


def write_glb(path, P, N, C, I, T):
    lin = np.where(C <= 0.04045, C / 12.92, ((C + 0.055) / 1.055) ** 2.4)             # màu đỉnh của glTF là màu tuyến tính
    pos = (P[:, [0, 2, 1]] * (1, 1, -1)).astype("<f4"); nrm = (N[:, [0, 2, 1]] * (1, 1, -1)).astype("<f4")
    col = np.c_[np.clip(lin * 255 + 0.5, 0, 255), np.full(len(P), 255)].astype("u1")
    big = len(P) >= 65536; used = [m for m in range(len(MKEYS)) if (T == m).any()]
    arrs = [(pos, 34962), (nrm, 34962), (col, 34962)] + [(I[T == m].astype("<u4" if big else "<u2"), 34963) for m in used]
    chunks, views, off = [], [], 0
    for arr, target in arrs:
        b = arr.tobytes(); b += b"\0" * (-len(b) % 4)
        views.append({"buffer": 0, "byteOffset": off, "byteLength": arr.nbytes, "target": target}); chunks.append(b); off += len(b)
    mats = []
    for m in used:
        metal, rough, alpha, emis, _ = MATS[MKEYS[m]]
        d = {"name": MKEYS[m], "pbrMetallicRoughness": {"baseColorFactor": [1, 1, 1, alpha], "metallicFactor": metal, "roughnessFactor": rough}, "doubleSided": True}
        if alpha < 1: d["alphaMode"] = "BLEND"
        if emis: d["emissiveFactor"] = list(emis)
        mats.append(d)
    gltf = {
        "asset": {"version": "2.0", "generator": "timeless-harmony build_kit.py"}, "scene": 0, "scenes": [{"nodes": [0]}],
        "nodes": [{"mesh": 0, "name": os.path.splitext(os.path.basename(path))[0]}],
        "meshes": [{"primitives": [{"attributes": {"POSITION": 0, "NORMAL": 1, "COLOR_0": 2}, "indices": 3 + i, "material": i} for i in range(len(used))]}],
        "materials": mats, "buffers": [{"byteLength": off}], "bufferViews": views,
        "accessors": [
            {"bufferView": 0, "componentType": 5126, "count": len(P), "type": "VEC3", "min": pos.min(0).tolist(), "max": pos.max(0).tolist()},
            {"bufferView": 1, "componentType": 5126, "count": len(P), "type": "VEC3"},
            {"bufferView": 2, "componentType": 5121, "count": len(P), "type": "VEC4", "normalized": True}]
        + [{"bufferView": 3 + i, "componentType": 5125 if big else 5123, "count": int((T == m).sum()) * 3, "type": "SCALAR"} for i, m in enumerate(used)],
    }
    js = json.dumps(gltf, separators=(",", ":")).encode(); js += b" " * (-len(js) % 4)
    blob = b"".join(chunks)
    with open(path, "wb") as f:
        f.write(struct.pack("<4sII", b"glTF", 2, 12 + 8 + len(js) + 8 + len(blob)))
        f.write(struct.pack("<I4s", len(js), b"JSON")); f.write(js)
        f.write(struct.pack("<I4s", len(blob), b"BIN\0")); f.write(blob)


def build_all():
    os.makedirs(OUT, exist_ok=True)
    built, manifest = {}, []
    for key, name, fn in ITEMS:
        k = Kit(); fn(k)
        P, N, C, I, T = k.arrays()
        P[:, :2] -= (P[:, :2].min(0) + P[:, :2].max(0)) / 2; P[:, 2] -= P[:, 2].min()      # gốc ở giữa mặt đáy
        C = bake(P, N, C, I, T, np.concatenate(k.A))
        write_glb(os.path.join(OUT, key + ".glb"), P, N, C, I, T)
        size = (P.max(0) - P.min(0)).round(2).tolist()
        manifest.append({"id": key, "ten": name, "kich_thuoc_m": size, "tam_giac": int(len(I)), "kb": round(os.path.getsize(os.path.join(OUT, key + ".glb")) / 1024, 1)})
        built[key] = (name, P, C, I, T)
    with open(os.path.join(OUT, "kit.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)
    return built, manifest


# ─────────────────────────────── ảnh xem trước (Blender) ───────────────────────────────
def bl_start(spp=64):
    import bpy
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc, mats = bpy.context.scene, []
    for name, (metal, rough, alpha, emis, glow) in MATS.items():
        m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
        att = nt.nodes.new("ShaderNodeVertexColor"); att.layer_name = "Col"; nt.links.new(att.outputs["Color"], b.inputs["Base Color"])
        b.inputs["Metallic"].default_value = metal; b.inputs["Roughness"].default_value = rough; b.inputs["Alpha"].default_value = alpha
        if emis:
            b.inputs["Emission Color"].default_value = (*emis, 1); b.inputs["Emission Strength"].default_value = glow
        mats.append(m)
    sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = spp; sc.cycles.use_denoising = True
    sc.view_settings.view_transform = "Standard"; sc.render.image_settings.file_format = "PNG"
    return bpy, sc, mats


def bl_mesh(bpy, mats, key, P, C, I, T, s=1.0):
    me = bpy.data.meshes.new(key); me.from_pydata((P * s).tolist(), [], I.tolist())
    lin = np.where(C <= 0.04045, C / 12.92, ((C + 0.055) / 1.055) ** 2.4)
    me.color_attributes.new("Col", "FLOAT_COLOR", "POINT").data.foreach_set("color", np.c_[lin, np.ones(len(P))].ravel())
    me.polygons.foreach_set("use_smooth", np.ones(len(me.polygons), bool)); me.polygons.foreach_set("material_index", T.astype(np.int32))
    for m in mats:
        me.materials.append(m)
    return me


def bl_light(bpy, sc, sun_rgb, sun_e, sky_rgb, sky_e, rot):
    w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True
    w.node_tree.nodes["Background"].inputs[0].default_value = (*sky_rgb, 1); w.node_tree.nodes["Background"].inputs[1].default_value = sky_e
    sun = bpy.data.lights.new("sun", "SUN"); sun.energy = sun_e; sun.color = sun_rgb; sun.angle = math.radians(10)
    so = bpy.data.objects.new("sun", sun); so.rotation_euler = [math.radians(a) for a in rot]; sc.collection.objects.link(so)


def bloom(im, amount=5):
    """Quầng sáng nhẹ quanh chỗ rất sáng (bóng đèn, nến)."""
    from PIL import ImageChops, ImageFilter
    hot = im.point(lambda v: max(0, v - 232) * amount).filter(ImageFilter.GaussianBlur(im.size[0] / 200))
    return ImageChops.screen(im, hot)


def preview(built, out, cols=6):
    """Bảng kê: mỗi món phóng cho vừa ô (không giữ tỉ lệ giữa các món)."""
    bpy, sc, mats = bl_start(48)
    from bpy_extras.object_utils import world_to_camera_view
    from mathutils import Vector
    from PIL import Image, ImageDraw, ImageFont
    CELL, ROWK, rows, marks = 2.3, 2.25, math.ceil(len(built) / cols), []
    for n, (key, (name, P, C, I, T)) in enumerate(built.items()):
        ob = bpy.data.objects.new(key, bl_mesh(bpy, mats, key, P, C, I, T, 1.7 / max(P.max(0) - P.min(0)))); sc.collection.objects.link(ob)
        x, y = (n % cols - (cols - 1) / 2) * CELL, ((rows - 1) / 2 - n // cols) * CELL * ROWK
        ob.location = (x, y, 0); marks.append((Vector((x, y - CELL * 0.58, 0)), name))
    g = bpy.data.meshes.new("ground"); g.from_pydata([(-40, -40, 0), (40, -40, 0), (40, 40, 0), (-40, 40, 0)], [], [(0, 1, 2, 3)])
    gm = bpy.data.materials.new("ground"); gm.use_nodes = True
    gm.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.62, 0.36, 0.40, 1)   # nền hồng đất: đồ trắng, vàng và lá xanh đều nổi
    gm.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 1.0
    g.materials.append(gm); sc.collection.objects.link(bpy.data.objects.new("ground", g))
    bl_light(bpy, sc, (1.0, 0.9, 0.78), 2.6, (0.86, 0.92, 1.0), 0.6, (48, 0, -35))
    cam = bpy.data.cameras.new("cam"); cam.type = "ORTHO"; cam.ortho_scale = cols * CELL * 1.04
    co = bpy.data.objects.new("cam", cam); pitch = math.radians(58)
    co.rotation_euler = (pitch, 0, 0); co.location = (0, -40 * math.sin(pitch) - 0.1, 40 * math.cos(pitch) + 0.5); sc.collection.objects.link(co); sc.camera = co
    W = 2200; H = int(W * (rows * CELL * ROWK * math.cos(pitch) + 1.6) / (cols * CELL * 1.04))
    sc.render.resolution_x, sc.render.resolution_y = W, H; sc.render.filepath = os.path.abspath(out)
    bpy.ops.render.render(write_still=True)
    bpy.context.view_layer.update()
    im = bloom(Image.open(out).convert("RGB")); d = ImageDraw.Draw(im)
    font = next((ImageFont.truetype(p, 27) for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/dejavu/DejaVuSans.ttf") if os.path.exists(p)), ImageFont.load_default())
    for pos, name in marks:
        v = world_to_camera_view(sc, co, pos)
        d.text((v.x * W - d.textlength(name, font=font) / 2, (1 - v.y) * H - 14), name, fill=(255, 250, 244), font=font)
    im.save(out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--preview", default=None, help="xuất thêm ảnh bảng kê (cần bpy và Pillow)")
    A = ap.parse_args()
    built, manifest = build_all()
    print("%d món, %d tam giác, %.0f KB" % (len(manifest), sum(m["tam_giac"] for m in manifest), sum(m["kb"] for m in manifest)))
    if A.preview:
        preview(built, A.preview); print("preview", A.preview)
