"""Kho đồ vật 3D cho game "Về chung một nhà": dựng bằng mã, xuất glTF nhị phân (.glb) vào game/assets/kit/.

    python3 docs/game/build_kit.py                       # chỉ cần numpy: dựng lại toàn bộ .glb và kit.json
    .venv3d/bin/python docs/game/build_kit.py --preview kho.png     # thêm ảnh xem trước (cần bpy và Pillow)

Quy ước: đơn vị mét, gốc toạ độ ở giữa mặt đáy, trục Z hướng lên (lúc xuất đổi sang trục Y hướng lên của glTF).
Màu nằm ở từng đỉnh (COLOR_0), không dùng ảnh chất liệu: tệp rất nhẹ, và đổi bảng màu chỉ cần sửa PAL rồi chạy lại.
Phong cách: hình khối bo tròn, ít đa giác, màu nhạt theo bảng màu Timeless Harmony.
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
PAL = dict(gold="#C9A45C", gold_d="#A8823F", cream="#F6F0E4", white="#FBF9F4", jade="#2F6B50", jade_l="#8FC2A6", leaf="#5E9B63",
           leaf_d="#3F7A4B", tulip="#F2A7B8", pink_l="#F9D5DC", peach="#F6C9A8", sky="#A9D4F0", lilac="#CDB8E8", red="#C8372D",
           red_d="#9E2A22", wood="#B8875A", wood_d="#8A5F3C", terra="#C97B54", grey="#C9CDD2", dark="#3A4046", yellow="#F5D26B",
           glass="#DCEEF5", flame="#FFB347")
PAL = {k: np.array([int(v[i:i + 2], 16) / 255 for i in (1, 3, 5)]) for k, v in PAL.items()}
rng = np.random.default_rng(7)


def rotx(a): c, s = math.cos(a), math.sin(a); return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])
def roty(a): c, s = math.cos(a), math.sin(a); return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])
def rotz(a): c, s = math.cos(a), math.sin(a); return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])


class Kit:
    """Gom các khối cơ bản thành một lưới: vị trí, pháp tuyến, màu đỉnh, tam giác."""

    def __init__(self):
        self.P, self.N, self.C, self.I, self.n = [], [], [], [], 0

    def add(self, V, F, col, smooth=True, M=None, t=None, ref=None, nrm=None):
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
        if smooth:
            N = np.zeros_like(V)
            for k in range(3):
                np.add.at(N, F[:, k], fn)
            P, I = V, F
        else:
            P, N, I = V[F].reshape(-1, 3), np.repeat(fn, 3, 0), np.arange(len(F) * 3).reshape(-1, 3)
        N = N / (np.linalg.norm(N, axis=1, keepdims=True) + 1e-12)
        col = PAL[col] if isinstance(col, str) else np.asarray(col, float)
        self.P.append(P); self.N.append(N); self.C.append(np.tile(col, (len(P), 1))); self.I.append(I + self.n)
        self.n += len(P)
        return self

    # ── khối cơ bản ──
    def lathe(self, profile, col, n=20, hard=False, **kw):
        """Tiện tròn quanh trục Z. profile = [(bán kính, cao), …] đi từ đáy lên. hard=True: giữ cạnh sắc giữa các đoạn."""
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
            self.add(V, F, col, smooth=True, nrm=(0, 0, 1 if S[1, 0] < S[0, 0] else -1) if flat else None,
                     ref=None if flat else (0, 0, float(S[:, 1].mean())), **kw)
        return self

    def rbox(self, w, d, h, col, r=0.02, seg=3, t=(0, 0, 0), M=None):
        """Hộp bo góc đứng (mặt cắt chữ nhật bo tròn), đáy ở z = 0 của hệ cục bộ."""
        r = min(r, w / 2 - 1e-4, d / 2 - 1e-4)
        pts = []
        for cx, cy, a0 in ((w / 2 - r, d / 2 - r, 0), (-w / 2 + r, d / 2 - r, 90), (-w / 2 + r, -d / 2 + r, 180), (w / 2 - r, -d / 2 + r, 270)):
            for k in range(seg + 1):
                a = math.radians(a0 + 90 * k / seg)
                pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        pts = np.array(pts); n = len(pts)
        V = np.concatenate([np.c_[pts, np.zeros(n)], np.c_[pts, np.full(n, h)]])
        F = []
        for j in range(n):
            p, q = j, (j + 1) % n
            F += [[p, q, q + n], [p, q + n, p + n]]
        self.add(V, F, col, True, M, t)
        fan = [[0, j, j + 1] for j in range(1, n - 1)]
        self.add(np.c_[pts, np.full(n, h)], fan, col, False, M, t, nrm=(0, 0, 1))
        self.add(np.c_[pts, np.zeros(n)], fan, col, False, M, t, nrm=(0, 0, -1))
        return self

    def cyl(self, p0, p1, r0, col, r1=None, n=10, caps=True):
        """Trụ (hoặc nón cụt) nối hai điểm."""
        p0, p1 = np.asarray(p0, float), np.asarray(p1, float)
        r1 = r0 if r1 is None else r1
        w = p1 - p0; L = np.linalg.norm(w); w = w / L
        u = np.cross(w, [0, 0, 1.0] if abs(w[2]) < 0.9 else [1.0, 0, 0]); u /= np.linalg.norm(u); v = np.cross(w, u)
        a = np.arange(n) * 2 * np.pi / n
        ring = np.outer(np.cos(a), u) + np.outer(np.sin(a), v)
        V = np.concatenate([p0 + ring * r0, p1 + ring * r1])
        F = []
        for j in range(n):
            p, q = j, (j + 1) % n
            F += [[p, q, q + n], [p, q + n, p + n]]
        self.add(V, F, col, True, ref=(p0 + p1) / 2)
        if caps:
            fan = [[0, j, j + 1] for j in range(1, n - 1)]
            if r0 > 1e-4: self.add(p0 + ring * r0, fan, col, False, nrm=-w)
            if r1 > 1e-4: self.add(p1 + ring * r1, fan, col, False, nrm=w)
        return self

    def ball(self, c, rad, col, nu=10, nv=7, M=None, pre=None):
        rad = np.broadcast_to(np.asarray(rad, float), (3,))
        th = np.linspace(0, np.pi, nv + 1)[1:-1]; a = np.arange(nu) * 2 * np.pi / nu
        V = [[0, 0, 1.0]] + [[math.sin(t) * math.cos(x), math.sin(t) * math.sin(x), math.cos(t)] for t in th for x in a] + [[0, 0, -1.0]]
        F = [[0, 1 + j, 1 + (j + 1) % nu] for j in range(nu)]
        for i in range(nv - 2):
            for j in range(nu):
                p, q = 1 + i * nu + j, 1 + i * nu + (j + 1) % nu
                F += [[p, p + nu, q + nu], [p, q + nu, q]]
        last = 1 + (nv - 2) * nu
        F += [[last + j, len(V) - 1, last + (j + 1) % nu] for j in range(nu)]
        V = np.array(V) * rad
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
        Vc = np.repeat(P, n, 0)                                   # hướng ra ngoài = từ tâm ống ra
        fn = np.cross(V[np.array(F)[:, 1]] - V[np.array(F)[:, 0]], V[np.array(F)[:, 2]] - V[np.array(F)[:, 0]])
        if float((fn * (V[np.array(F)].mean(1) - Vc[np.array(F)].mean(1))).sum()) < 0:
            F = [f[::-1] for f in F]
        N = V - Vc; N /= np.linalg.norm(N, axis=1, keepdims=True) + 1e-12
        col = PAL[col] if isinstance(col, str) else np.asarray(col, float)
        self.P.append(V); self.N.append(N); self.C.append(np.tile(col, (len(V), 1))); self.I.append(np.array(F) + self.n)
        self.n += len(V)
        return self

    def ringz(self, R, r, z, col, nu=18, n=6):
        a = np.arange(nu) * 2 * np.pi / nu
        return self.tube(np.c_[R * np.cos(a), R * np.sin(a), np.full(nu, z)], r, col, n, closed=True)

    # ── cụm hoa lá: nhiều quả cầu nhỏ ──
    def blooms(self, pts, size, cols, nu=7, nv=5):
        for p in pts:
            s = size * rng.uniform(0.75, 1.2)
            self.ball(p, (s, s, s * rng.uniform(0.8, 1.0)), cols[rng.integers(len(cols))], nu, nv)
        return self

    def arrays(self):
        return np.concatenate(self.P), np.concatenate(self.N), np.concatenate(self.C), np.concatenate(self.I)


FLOWERS = ["white", "pink_l", "tulip", "peach", "cream"]


def pot(k, r=0.2, h=0.3, col="terra"):
    return k.lathe([(0, 0), (r * 0.72, 0), (r, h * 0.92), (r * 1.06, h * 0.92), (r * 1.06, h), (r * 0.9, h), (r * 0.9, h * 0.9), (0, h * 0.9)], col, 14, hard=True)


# ─────────────────────────────── đồ vật ───────────────────────────────
def ghe_chiavari(k):
    for x in (-0.18, 0.18):
        k.cyl((x, -0.18, 0), (x, -0.18, 0.45), 0.016, "gold", n=8)                     # chân trước
        k.cyl((x, 0.18, 0), (x * 0.94, 0.21, 0.92), 0.016, "gold", n=8)                # chân sau kiêm trụ lưng
        k.cyl((x, -0.18, 0.18), (x, 0.185, 0.18), 0.009, "gold", n=6, caps=False)
    for z, y in ((0.18, -0.18), (0.92, 0.21), (0.72, 0.2), (0.52, 0.19)):
        k.cyl((-0.18, y, z), (0.18, y, z), 0.012 if z > 0.3 else 0.009, "gold", n=6)
    for x in (-0.11, -0.055, 0, 0.055, 0.11):
        k.cyl((x, 0.19, 0.52), (x, 0.205, 0.92), 0.007, "gold", n=6, caps=False)
    k.rbox(0.41, 0.41, 0.03, "gold", 0.05, t=(0, 0, 0.44))
    k.rbox(0.36, 0.36, 0.04, "white", 0.08, t=(0, -0.005, 0.47))


def ban_tron(k):
    k.lathe([(0, 0.76), (0.80, 0.76), (0.815, 0.745), (0.83, 0.55), (0.86, 0.25), (0.84, 0.03), (0.80, 0.02)], "white", 28)
    k.lathe([(0, 0.762), (0.42, 0.762), (0.42, 0.775), (0, 0.775)], "cream", 24, hard=True)          # mâm xoay
    k.lathe([(0, 0.02), (0.30, 0.02), (0.30, 0), (0, 0)], "dark", 12, hard=True)


def ban_dai(k):
    k.rbox(1.84, 0.80, 0.745, "white", 0.06, t=(0, 0, 0.015))
    k.rbox(0.42, 0.815, 0.752, "pink_l", 0.06, t=(0, 0, 0.012))                        # khăn chạy giữa bàn
    k.rbox(1.70, 0.66, 0.02, "dark", 0.03)


def ghe_dau_nhua(k):
    k.lathe([(0, 0), (0.21, 0), (0.165, 0.44), (0.15, 0.455), (0, 0.455)], "red", 4, hard=True, M=rotz(math.pi / 4))
    k.lathe([(0, 0.456), (0.035, 0.456), (0.035, 0.458), (0, 0.458)], "red_d", 10, hard=True)


def ban_ca_phe(k):
    k.lathe([(0, 0), (0.22, 0), (0.22, 0.02), (0.03, 0.045), (0.028, 0.70), (0, 0.70)], "dark", 14, hard=True)
    k.lathe([(0, 0.70), (0.33, 0.70), (0.34, 0.715), (0.33, 0.73), (0, 0.73)], "wood", 24)


GLASS = [(0, 0), (0.034, 0), (0.034, 0.004), (0.004, 0.012), (0.004, 0.09), (0.018, 0.10), (0.036, 0.125), (0.04, 0.165), (0.036, 0.20), (0.032, 0.20)]


def ly_ruou(k, at=(0, 0, 0), n=12):
    k.lathe(GLASS, "glass", n, t=at)
    k.lathe([(0, 0.125), (0.034, 0.125), (0.038, 0.16), (0, 0.16)], "peach", n, t=at)


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
    k.lathe([(0, 0), (0.13, 0), (0.13, 0.01), (0.03, 0.03), (0.03, 0.09), (0.21, 0.10), (0.21, 0.115), (0, 0.115)], "gold", 20, hard=True)
    z = 0.115
    for r, c in ((0.17, "white"), (0.125, "cream"), (0.085, "white")):
        k.lathe([(0, z), (r, z), (r, z + 0.085), (r - 0.012, z + 0.10), (0, z + 0.10)], c, 22)
        k.blooms([(r * math.cos(a), r * math.sin(a), z + 0.012) for a in np.linspace(0, 2 * np.pi, int(r * 90), endpoint=False)], 0.016, ["pink_l", "tulip", "peach"], 6, 4)
        z += 0.10
    k.blooms([(0.0, 0.0, z + 0.02), (0.035, 0.01, z + 0.012), (-0.03, 0.02, z + 0.012), (0.0, -0.035, z + 0.01)], 0.03, ["tulip", "pink_l", "white"], 7, 5)
    k.blooms([(-0.05, -0.02, z + 0.005), (0.045, -0.03, z + 0.004)], 0.022, ["jade_l"], 6, 4)


def cong_hoa(k):
    R, H = 1.05, 1.15
    a = np.linspace(0, np.pi, 17)
    path = np.concatenate([[[R, 0, 0]], np.c_[R * np.cos(a), np.zeros(17), H + R * np.sin(a)], [[-R, 0, 0]]])
    k.tube(path, 0.045, "leaf_d", 6)
    d = np.linalg.norm(np.diff(path, axis=0), axis=1); s = np.concatenate([[0], np.cumsum(d)]) / d.sum()
    pts = []
    for u in np.sort(rng.uniform(0.0, 1.0, 84)):
        p = np.array([np.interp(u, s, path[:, i]) for i in range(3)])
        dense = 0.5 + 0.5 * abs(math.sin(u * math.pi * 1.5 + 0.4))                    # hoa dày từng cụm, không đều tăm tắp
        if rng.uniform() < dense:
            pts.append(p + rng.normal(0, 0.075, 3) * (1.0, 1.3, 1.0))
    k.blooms(pts, 0.105, FLOWERS, 7, 5)
    k.blooms([p + rng.normal(0, 0.09, 3) for p in pts[::3]], 0.075, ["jade_l", "leaf"], 6, 4)


def binh_hoa(k):
    k.lathe([(0, 0), (0.06, 0), (0.095, 0.07), (0.10, 0.14), (0.06, 0.24), (0.045, 0.30), (0.06, 0.33), (0.052, 0.33), (0, 0.30)], "sky", 18)
    tips = [(0.10 * math.cos(a) * s, 0.10 * math.sin(a) * s, 0.50 + 0.07 * (1 - s) + rng.uniform(-0.02, 0.02)) for a, s in
            [(i * 2.4, 0.35 + 0.65 * ((i * 0.37) % 1)) for i in range(9)]]
    for p in tips:
        k.cyl((0, 0, 0.30), p, 0.005, "leaf_d", n=5, caps=False)
    k.blooms(tips, 0.055, FLOWERS, 8, 6)
    k.blooms([(p[0] * 1.25, p[1] * 1.25, p[2] - 0.07) for p in tips[::2]], 0.04, ["jade_l", "leaf"], 6, 4)


def bo_hoa(k):
    k.lathe([(0, 0), (0.018, 0), (0.022, 0.12), (0.06, 0.20), (0, 0.20)], "white", 12)
    k.lathe([(0.024, 0.115), (0.03, 0.125), (0.024, 0.135)], "tulip", 12)             # nơ buộc
    pts = [(0.085 * math.sin(t) * math.cos(a), 0.085 * math.sin(t) * math.sin(a), 0.21 + 0.075 * math.cos(t))
           for t, a in [(0.0, 0.0)] + [(0.65, i * 1.26) for i in range(5)] + [(1.25, i * 0.785 + 0.3) for i in range(8)]]
    k.blooms(pts, 0.05, FLOWERS, 8, 6)
    k.blooms([(p[0] * 1.3, p[1] * 1.3, p[2] - 0.03) for p in pts[6::2]], 0.034, ["jade_l"], 6, 4)


def mam_qua(k):
    k.lathe([(0, 0), (0.20, 0), (0.215, 0.02), (0.215, 0.10), (0.20, 0.11)], "red", 22)
    k.ringz(0.216, 0.008, 0.10, "gold", 22, 5)
    k.lathe([(0.225, 0.085), (0.222, 0.12), (0.17, 0.19), (0.07, 0.232), (0, 0.24)], "red", 22)      # khăn phủ
    k.ringz(0.224, 0.006, 0.088, "gold", 22, 5)
    k.ball((0, 0, 0.25), 0.02, "gold", 8, 6)


def hop_nhan(k):
    k.rbox(0.07, 0.07, 0.032, "jade", 0.012)
    k.rbox(0.058, 0.058, 0.008, "white", 0.01, t=(0, 0, 0.03))
    k.rbox(0.07, 0.07, 0.022, "jade", 0.012, M=rotx(math.radians(-105)), t=(0, 0.035, 0.034))        # nắp mở
    k.tube([(0.011 * math.cos(a), 0, 0.05 + 0.011 * math.sin(a)) for a in np.arange(14) * 2 * np.pi / 14], 0.0022, "gold", 6, closed=True)
    k.ball((0, 0, 0.064), 0.0045, "glass", 6, 4)


def thung_tien_mung(k):
    k.rbox(0.34, 0.26, 0.28, "white", 0.03)
    k.rbox(0.36, 0.28, 0.045, "gold", 0.03, t=(0, 0, 0.275))
    k.rbox(0.16, 0.014, 0.004, "dark", 0.005, t=(0, 0, 0.32))                         # khe bỏ phong bì
    k.rbox(0.045, 0.262, 0.284, "tulip", 0.012, t=(-0.09, 0, -0.001))
    for s in (-1, 1):
        k.ball((-0.09 + s * 0.035, -0.135, 0.20), (0.035, 0.012, 0.022), "tulip", 8, 5)
    k.ball((-0.09, -0.137, 0.20), 0.012, "pink_l", 6, 4)


def chan_nen(k):
    k.lathe([(0, 0), (0.06, 0), (0.06, 0.008), (0.015, 0.03), (0.012, 0.12), (0.028, 0.14), (0.012, 0.16), (0.012, 0.22), (0.04, 0.24), (0.04, 0.25), (0, 0.25)], "gold", 16)
    k.cyl((0, 0, 0.25), (0, 0, 0.43), 0.014, "cream", n=10)
    k.ball((0, 0, 0.455), (0.009, 0.009, 0.022), "flame", 8, 6)


def den_long(k):
    k.cyl((0, 0, 0.62), (0, 0, 0.72), 0.004, "dark", n=5, caps=False)
    k.lathe([(0, 0.60), (0.065, 0.60), (0.065, 0.62), (0, 0.62)], "wood_d", 14, hard=True)
    k.lathe([(0.06, 0.60), (0.15, 0.555), (0.205, 0.44), (0.205, 0.36), (0.15, 0.245), (0.06, 0.20)], "red", 18)
    for a in np.arange(9) * 2 * np.pi / 9:                                             # nan đèn
        k.tube([(r * 1.012 * math.cos(a), r * 1.012 * math.sin(a), z) for r, z in ((0.06, 0.60), (0.15, 0.555), (0.205, 0.44), (0.205, 0.36), (0.15, 0.245), (0.06, 0.20))], 0.004, "red_d", 4)
    k.lathe([(0, 0.18), (0.065, 0.18), (0.065, 0.20), (0, 0.20)], "wood_d", 14, hard=True)
    k.cyl((0, 0, 0.18), (0, 0, 0.10), 0.004, "gold", n=5, caps=False)
    k.lathe([(0, 0), (0.012, 0), (0.02, 0.08), (0.008, 0.10), (0, 0.10)], "gold", 8)   # tua


def day_den(k):
    for x in (-1.5, 1.5):
        k.lathe([(0, 0), (0.12, 0), (0.12, 0.03), (0.022, 0.05), (0.018, 2.6), (0, 2.6)], "dark", 10, hard=True, t=(x, 0, 0))
    u = np.linspace(-1, 1, 21)
    wire = np.c_[u * 1.5, np.zeros(21), 2.58 - 0.38 * (1 - u ** 2)]
    k.tube(wire, 0.006, "dark", 4)
    for p in wire[2:-1:2]:
        k.cyl(p, p - (0, 0, 0.04), 0.012, "dark", n=6)
        k.ball(p - (0, 0, 0.075), (0.034, 0.034, 0.042), "yellow", 8, 6)


def bong_bay(k):
    k.rbox(0.08, 0.08, 0.05, "gold", 0.015)
    for (x, y, z), c in zip(((0.0, 0.0, 1.55), (0.2, 0.06, 1.34), (-0.19, -0.05, 1.38), (0.04, -0.17, 1.22), (-0.06, 0.18, 1.2)), ("tulip", "white", "peach", "lilac", "sky")):
        k.cyl((0, 0, 0.05), (x, y, z - 0.17), 0.0025, "grey", n=4, caps=False)
        k.ball((x, y, z), (0.135, 0.135, 0.165), c, 12, 9)
        k.lathe([(0, 0), (0.012, 0), (0.004, 0.02)], c, 6, t=(x, y, z - 0.185))


def chau_cay_tron(k):
    pot(k, 0.2, 0.3)
    k.cyl((0, 0, 0.27), (0, 0, 0.78), 0.022, "wood_d", n=7, caps=False)
    k.ball((0, 0, 1.0), 0.29, "leaf", 14, 10)
    k.blooms([(0.2 * math.cos(a) * math.sin(t), 0.2 * math.sin(a) * math.sin(t), 1.0 + 0.2 * math.cos(t)) for a, t in rng.uniform((0, 0.3), (6.28, 2.6), (14, 2))], 0.12, ["leaf", "leaf_d"], 7, 5)


def chau_cay_non(k):
    pot(k, 0.2, 0.3)
    k.lathe([(0, 0.27), (0.30, 0.30), (0.26, 0.55), (0.17, 0.95), (0.07, 1.30), (0, 1.42)], "leaf_d", 14)
    k.blooms([(r * math.cos(a), r * math.sin(a), z) for a, z, r in [(i * 2.4, 0.38 + i * 0.062, 0.27 - i * 0.0135) for i in range(16)]], 0.07, ["leaf", "leaf_d"], 6, 4)


def chau_hoa(k):
    pot(k, 0.17, 0.22, "white")
    pts = [(0.13 * math.sin(t) * math.cos(a), 0.13 * math.sin(t) * math.sin(a), 0.25 + 0.12 * math.cos(t)) for t, a in rng.uniform((0, 0), (1.5, 6.28), (16, 2))]
    k.blooms(pts, 0.075, ["leaf", "jade_l"], 7, 5)
    k.blooms([(p[0] * 1.15, p[1] * 1.15, p[2] + 0.045) for p in pts[::2]], 0.045, ["tulip", "pink_l", "white", "peach"], 7, 5)


def den_duong(k):
    k.lathe([(0, 0), (0.16, 0), (0.16, 0.05), (0.07, 0.10), (0.055, 0.50), (0.04, 0.55), (0.035, 3.0), (0, 3.0)], "dark", 12, hard=True)
    k.tube([(0, 0, 2.95), (0, 0, 3.2), (0.12, 0, 3.36), (0.34, 0, 3.4), (0.5, 0, 3.32)], 0.022, "dark", 6)
    k.lathe([(0, 0.02), (0.09, 0.0), (0.14, 0.08), (0.10, 0.16), (0, 0.18)], "cream", 12, t=(0.5, 0, 3.12))
    k.lathe([(0.085, 0.15), (0.11, 0.17), (0.04, 0.24), (0, 0.25)], "dark", 12, t=(0.5, 0, 3.12))


def ghe_bang(k):
    for x in (-0.62, 0.62):
        k.rbox(0.05, 0.46, 0.40, "dark", 0.012, t=(x, 0, 0))
        k.rbox(0.05, 0.05, 0.44, "dark", 0.012, M=rotx(math.radians(-12)), t=(x, 0.20, 0.40))
    for y in (-0.17, -0.06, 0.05, 0.16):
        k.rbox(1.42, 0.09, 0.03, "wood", 0.012, t=(0, y, 0.40))
    for z in (0.56, 0.70):
        k.rbox(1.42, 0.03, 0.10, "wood", 0.012, M=rotx(math.radians(-12)), t=(0, 0.215 + (z - 0.4) * 0.21, z))


def wheel(k, c, r=0.16, w=0.05):
    c = np.asarray(c, float)
    k.cyl(c - (w / 2, 0, 0), c + (w / 2, 0, 0), r, "dark", n=16)
    k.cyl(c - (w / 2 + 0.004, 0, 0), c + (w / 2 + 0.004, 0, 0), r * 0.45, "grey", n=10)


def awning(k, w, d, z, tilt, cols, y0=0.0, n=6):
    """Mái bạt sọc: n dải màu xen kẽ, nghiêng về phía trước."""
    for i in range(n):
        x = -w / 2 + w * (i + 0.5) / n
        k.rbox(w / n + 0.002, d, 0.025, cols[i % 2], 0.008, M=rotx(tilt), t=(x, y0, z))
        k.ball((x, y0 - d / 2 * math.cos(tilt) - 0.005, z - d / 2 * math.sin(-tilt) - 0.03), (w / n / 2, 0.012, 0.045), cols[i % 2], 8, 5)   # diềm bạt


def xe_ca_phe(k):
    k.rbox(1.25, 0.62, 0.62, "jade", 0.05, t=(0, 0, 0.22))
    k.rbox(1.33, 0.70, 0.04, "wood", 0.03, t=(0, 0, 0.84))
    k.rbox(1.0, 0.012, 0.36, "cream", 0.03, M=rotx(0), t=(0, -0.316, 0.36))            # bảng tên phía trước (để trống)
    for x in (-0.58, 0.58):
        for y in (-0.28, 0.28):
            k.cyl((x, y, 0.88), (x, y, 1.82), 0.014, "gold", n=6)
    awning(k, 1.5, 0.95, 1.86, math.radians(8), ("white", "tulip"), 0.0, 8)
    wheel(k, (-0.66, 0.05, 0.16)); wheel(k, (0.66, 0.05, 0.16))
    k.cyl((-0.3, -0.34, 0.1), (-0.3, -0.34, 0.24), 0.02, "dark", n=6)
    for i, x in enumerate((-0.42, -0.28, -0.14)):                                       # ly giấy
        k.lathe([(0, 0), (0.028, 0), (0.038, 0.10), (0, 0.10)], ("white", "peach", "white")[i], 10, hard=True, t=(x, -0.12, 0.88))
    k.rbox(0.26, 0.3, 0.3, "dark", 0.03, t=(0.34, 0.05, 0.88))                          # máy pha
    k.rbox(0.2, 0.04, 0.02, "grey", 0.008, t=(0.34, -0.12, 0.96))


def sap_hang(k):
    k.rbox(1.7, 0.8, 0.74, "red", 0.04, t=(0, 0, 0.015))
    k.rbox(1.78, 0.88, 0.03, "wood", 0.02, t=(0, 0, 0.75))
    for x in (-0.82, 0.82):
        for y in (-0.38, 0.38):
            k.cyl((x, y, 0), (x, y, 2.05 + (0.1 if y > 0 else 0)), 0.018, "dark", n=6)
    awning(k, 2.0, 1.25, 2.12, math.radians(6), ("red", "white"), 0.0, 8)
    for i, (x, c) in enumerate(((-0.6, "peach"), (-0.2, "sky"), (0.2, "yellow"), (0.6, "lilac"))):   # hàng bày bán
        k.rbox(0.3, 0.3, 0.12, "wood_d", 0.02, t=(x, 0.1, 0.78))
        k.blooms([(x + dx, 0.1 + dy, 0.92 + dz) for dx, dy, dz in rng.uniform(-0.09, 0.09, (7, 3)) * (1, 1, 0.3)], 0.05, [c], 7, 5)
    wire = np.c_[np.linspace(-0.8, 0.8, 9), np.full(9, -0.5), 1.98 - 0.08 * (1 - np.linspace(-1, 1, 9) ** 2)]
    k.tube(wire, 0.005, "dark", 4)
    for p in wire[1:-1:2]:
        k.ball(p - (0, 0, 0.05), (0.03, 0.03, 0.038), "yellow", 8, 6)


def bang_don_khach(k):
    for x, y in ((-0.3, -0.05), (0.3, -0.05), (0, 0.42)):
        k.cyl((x, y, 0), (x * 0.25, 0.12, 1.6), 0.016, "wood", n=6)
    k.rbox(0.72, 0.03, 0.03, "wood", 0.008, t=(0, -0.045, 0.5))
    tilt = rotx(math.radians(-9))
    k.rbox(0.66, 0.025, 0.92, "gold", 0.02, M=tilt, t=(0, -0.03, 0.53))
    k.rbox(0.60, 0.012, 0.86, "white", 0.012, M=tilt, t=(0, -0.047, 0.56))
    pts = [(0.25 + dx, -0.16 + dy * 0.4, 0.60 + dz) for dx, dy, dz in rng.uniform(-0.1, 0.1, (10, 3))]
    k.blooms(pts, 0.06, FLOWERS, 7, 5)
    k.blooms([(p[0] - 0.05, p[1], p[2] + 0.07) for p in pts[::3]], 0.045, ["jade_l"], 6, 4)


def loa(k):
    for a in (0.5, 2.6, 4.7):
        k.cyl((0, 0, 0.62), (0.42 * math.cos(a), 0.42 * math.sin(a), 0), 0.014, "dark", n=6)
    k.cyl((0, 0, 0.3), (0, 0, 1.0), 0.02, "dark", n=8)
    k.rbox(0.36, 0.32, 0.58, "dark", 0.04, t=(0, 0, 1.0))
    for z, r in ((1.19, 0.12), (1.44, 0.06)):
        k.lathe([(0, 0), (r, 0.0), (r * 0.92, 0.02), (r * 0.3, 0.008), (0, 0.012)], "grey", 16, M=rotx(math.pi / 2), t=(0, -0.16, z))


def micro(k):
    k.lathe([(0, 0), (0.13, 0), (0.13, 0.015), (0.02, 0.035), (0.012, 0.04), (0.012, 1.42), (0, 1.42)], "dark", 12, hard=True)
    k.cyl((0, 0, 1.40), (0, -0.07, 1.50), 0.016, "grey", n=8)
    k.ball((0, -0.085, 1.522), 0.03, "grey", 10, 7)


def quat_dung(k):
    k.lathe([(0, 0), (0.2, 0), (0.2, 0.02), (0.05, 0.05), (0.02, 0.07), (0.018, 1.05), (0, 1.05)], "grey", 14, hard=True)
    k.ball((0, 0.05, 1.12), (0.07, 0.10, 0.07), "grey", 10, 7)
    for i in range(3):
        k.ball((0, -0.06, 1.12), (0.05, 0.006, 0.105), "sky", 8, 6, M=roty(i * 2 * math.pi / 3), pre=(0, 0, 0.115))
    for y in (-0.10, -0.02):
        a = np.arange(20) * 2 * np.pi / 20
        k.tube(np.c_[0.24 * np.cos(a), np.full(20, y), 1.12 + 0.24 * np.sin(a)], 0.006, "white", 4, closed=True)
    for a in np.arange(12) * 2 * np.pi / 12:
        k.tube([(0.24 * math.cos(a), -0.02, 1.12 + 0.24 * math.sin(a)), (0.25 * math.cos(a), -0.06, 1.12 + 0.25 * math.sin(a)),
                (0.24 * math.cos(a), -0.10, 1.12 + 0.24 * math.sin(a)), (0.03 * math.cos(a), -0.115, 1.12 + 0.03 * math.sin(a))], 0.004, "white", 4)


ITEMS = [
    ("ghe-chiavari", "Ghế tiệc Chiavari", ghe_chiavari), ("ban-tron", "Bàn tròn 10 khách", ban_tron), ("ban-dai", "Bàn dài phủ khăn", ban_dai),
    ("ghe-dau-nhua", "Ghế đẩu nhựa", ghe_dau_nhua), ("ban-ca-phe", "Bàn cà phê", ban_ca_phe), ("ly-ruou", "Ly rượu", ly_ruou),
    ("thap-ly", "Tháp ly", thap_ly), ("banh-cuoi", "Bánh cưới ba tầng", banh_cuoi), ("cong-hoa", "Cổng hoa", cong_hoa),
    ("binh-hoa", "Bình hoa", binh_hoa), ("bo-hoa", "Bó hoa cầm tay", bo_hoa), ("mam-qua", "Mâm quả", mam_qua),
    ("hop-nhan", "Hộp nhẫn", hop_nhan), ("thung-tien-mung", "Thùng tiền mừng", thung_tien_mung), ("chan-nen", "Chân nến", chan_nen),
    ("den-long", "Đèn lồng", den_long), ("day-den", "Dây đèn", day_den), ("bong-bay", "Chùm bóng bay", bong_bay),
    ("chau-cay-tron", "Chậu cây tán tròn", chau_cay_tron), ("chau-cay-non", "Chậu cây hình nón", chau_cay_non), ("chau-hoa", "Chậu hoa", chau_hoa),
    ("den-duong", "Đèn đường", den_duong), ("ghe-bang", "Ghế băng công viên", ghe_bang), ("xe-ca-phe", "Xe cà phê", xe_ca_phe),
    ("sap-hang", "Sạp chợ đêm", sap_hang), ("bang-don-khach", "Bảng đón khách", bang_don_khach), ("loa", "Loa", loa),
    ("micro", "Micro có chân", micro), ("quat-dung", "Quạt đứng", quat_dung),
]


# ─────────────────────────────── xuất glTF ───────────────────────────────
def write_glb(path, P, N, C, I):
    lin = np.where(C <= 0.04045, C / 12.92, ((C + 0.055) / 1.055) ** 2.4)             # màu đỉnh của glTF là màu tuyến tính
    pos = (P[:, [0, 2, 1]] * (1, 1, -1)).astype("<f4"); nrm = (N[:, [0, 2, 1]] * (1, 1, -1)).astype("<f4")
    col = np.c_[np.clip(lin * 255 + 0.5, 0, 255), np.full(len(P), 255)].astype("u1")
    idx = I.astype("<u2" if len(P) < 65536 else "<u4")
    chunks, views, off = [], [], 0
    for arr, target in ((pos, 34962), (nrm, 34962), (col, 34962), (idx, 34963)):
        b = arr.tobytes(); b += b"\0" * (-len(b) % 4)
        views.append({"buffer": 0, "byteOffset": off, "byteLength": arr.nbytes, "target": target}); chunks.append(b); off += len(b)
    gltf = {
        "asset": {"version": "2.0", "generator": "timeless-harmony build_kit.py"}, "scene": 0, "scenes": [{"nodes": [0]}],
        "nodes": [{"mesh": 0, "name": os.path.splitext(os.path.basename(path))[0]}],
        "meshes": [{"primitives": [{"attributes": {"POSITION": 0, "NORMAL": 1, "COLOR_0": 2}, "indices": 3, "material": 0}]}],
        "materials": [{"name": "kit", "pbrMetallicRoughness": {"baseColorFactor": [1, 1, 1, 1], "metallicFactor": 0, "roughnessFactor": 0.75}, "doubleSided": True}],
        "buffers": [{"byteLength": off}], "bufferViews": views,
        "accessors": [
            {"bufferView": 0, "componentType": 5126, "count": len(P), "type": "VEC3", "min": pos.min(0).tolist(), "max": pos.max(0).tolist()},
            {"bufferView": 1, "componentType": 5126, "count": len(P), "type": "VEC3"},
            {"bufferView": 2, "componentType": 5121, "count": len(P), "type": "VEC4", "normalized": True},
            {"bufferView": 3, "componentType": 5123 if len(P) < 65536 else 5125, "count": int(I.size), "type": "SCALAR"}],
    }
    js = json.dumps(gltf, separators=(",", ":")).encode(); js += b" " * (-len(js) % 4)
    blob = b"".join(chunks)
    with open(path, "wb") as f:
        f.write(struct.pack("<4sII", b"glTF", 2, 12 + 8 + len(js) + 8 + len(blob)))
        f.write(struct.pack("<I4s", len(js), b"JSON")); f.write(js)
        f.write(struct.pack("<I4s", len(blob), b"BIN\0")); f.write(blob)


def build_all():
    os.makedirs(OUT, exist_ok=True)
    built, manifest = [], []
    for key, name, fn in ITEMS:
        k = Kit(); fn(k)
        P, N, C, I = k.arrays()
        P[:, :2] -= (P[:, :2].min(0) + P[:, :2].max(0)) / 2; P[:, 2] -= P[:, 2].min()      # gốc ở giữa mặt đáy
        write_glb(os.path.join(OUT, key + ".glb"), P, N, C, I)
        size = (P.max(0) - P.min(0)).round(2).tolist()
        manifest.append({"id": key, "ten": name, "kich_thuoc_m": size, "tam_giac": int(len(I)), "kb": round(os.path.getsize(os.path.join(OUT, key + ".glb")) / 1024, 1)})
        built.append((key, name, P, N, C, I))
    with open(os.path.join(OUT, "kit.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)
    return built, manifest


# ─────────────────────────────── ảnh xem trước (Blender) ───────────────────────────────
def preview(built, out, cols=6):
    import bpy
    from bpy_extras.object_utils import world_to_camera_view
    from mathutils import Vector
    from PIL import Image, ImageDraw, ImageFont
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    mat = bpy.data.materials.new("kit"); mat.use_nodes = True
    nt = mat.node_tree; bsdf = nt.nodes["Principled BSDF"]; bsdf.inputs["Roughness"].default_value = 0.62
    att = nt.nodes.new("ShaderNodeVertexColor"); att.layer_name = "Col"
    nt.links.new(att.outputs["Color"], bsdf.inputs["Base Color"])
    CELL, ROWK, rows, marks = 2.3, 2.1, math.ceil(len(built) / cols), []
    for n, (key, name, P, N, C, I) in enumerate(built):
        s = 1.55 / max(P.max(0) - P.min(0))                                               # mỗi món phóng cho vừa ô (ảnh là bảng kê, không giữ tỉ lệ)
        me = bpy.data.meshes.new(key); me.from_pydata((P * s).tolist(), [], I.tolist())
        lin = np.where(C <= 0.04045, C / 12.92, ((C + 0.055) / 1.055) ** 2.4)
        ca = me.color_attributes.new("Col", "FLOAT_COLOR", "POINT"); ca.data.foreach_set("color", np.c_[lin, np.ones(len(P))].ravel())
        me.polygons.foreach_set("use_smooth", np.ones(len(me.polygons), bool)); me.materials.append(mat)
        ob = bpy.data.objects.new(key, me); sc.collection.objects.link(ob)
        x, y = (n % cols - (cols - 1) / 2) * CELL, ((rows - 1) / 2 - n // cols) * CELL * ROWK
        ob.location = (x, y, 0); marks.append((Vector((x, y - CELL * 0.62, 0)), name))
    g = bpy.data.meshes.new("ground"); g.from_pydata([(-40, -40, 0), (40, -40, 0), (40, 40, 0), (-40, 40, 0)], [], [(0, 1, 2, 3)])
    gm = bpy.data.materials.new("ground"); gm.use_nodes = True
    gm.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.42, 0.58, 0.50, 1)   # nền ngọc nhạt: đồ trắng và vàng nổi lên
    gm.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 1.0
    g.materials.append(gm); sc.collection.objects.link(bpy.data.objects.new("ground", g))
    w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True
    w.node_tree.nodes["Background"].inputs[0].default_value = (0.92, 0.96, 1.0, 1); w.node_tree.nodes["Background"].inputs[1].default_value = 0.55
    sun = bpy.data.lights.new("sun", "SUN"); sun.energy = 2.3; sun.angle = math.radians(14)
    so = bpy.data.objects.new("sun", sun); so.rotation_euler = (math.radians(48), 0, math.radians(-35)); sc.collection.objects.link(so)
    cam = bpy.data.cameras.new("cam"); cam.type = "ORTHO"; cam.ortho_scale = cols * CELL * 1.04
    co = bpy.data.objects.new("cam", cam); pitch = math.radians(58)
    co.rotation_euler = (pitch, 0, 0); co.location = (0, -40 * math.sin(pitch) - 0.1, 40 * math.cos(pitch) + 0.5); sc.collection.objects.link(co); sc.camera = co
    W = 2200; H = int(W * (rows * CELL * ROWK * math.cos(pitch) + 1.6) / (cols * CELL * 1.04))
    sc.render.resolution_x, sc.render.resolution_y = W, H
    sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = 48; sc.cycles.use_denoising = True
    sc.view_settings.view_transform = "Standard"; sc.render.filepath = os.path.abspath(out); sc.render.image_settings.file_format = "PNG"
    bpy.ops.render.render(write_still=True)
    bpy.context.view_layer.update()
    im = Image.open(out).convert("RGB"); d = ImageDraw.Draw(im)
    font = next((ImageFont.truetype(p, 26) for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/dejavu/DejaVuSans.ttf") if os.path.exists(p)), ImageFont.load_default())
    for pos, name in marks:
        v = world_to_camera_view(sc, co, pos)
        tw = d.textlength(name, font=font)
        d.text((v.x * W - tw / 2, (1 - v.y) * H - 14), name, fill=(255, 255, 255), font=font)
    im.save(out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--preview", default=None, help="xuất thêm ảnh bảng kê (cần bpy và Pillow)")
    A = ap.parse_args()
    built, manifest = build_all()
    print("%d món, %d tam giác, %.0f KB" % (len(manifest), sum(m["tam_giac"] for m in manifest), sum(m["kb"] for m in manifest)))
    if A.preview:
        preview(built, A.preview)
        print("preview", A.preview)
