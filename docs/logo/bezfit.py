"""Schneider (Graphics Gems I) cubic Bezier fitting for polylines."""
import numpy as np


def q(ctrl, t):
    t = np.asarray(t)[..., None]
    mt = 1 - t
    return (mt**3) * ctrl[0] + 3 * (mt**2) * t * ctrl[1] + 3 * mt * (t**2) * ctrl[2] + (t**3) * ctrl[3]


def qprime(ctrl, t):
    t = np.asarray(t)[..., None]
    mt = 1 - t
    return 3 * (mt**2) * (ctrl[1] - ctrl[0]) + 6 * mt * t * (ctrl[2] - ctrl[1]) + 3 * (t**2) * (ctrl[3] - ctrl[2])


def qprimeprime(ctrl, t):
    t = np.asarray(t)[..., None]
    return 6 * (1 - t) * (ctrl[2] - 2 * ctrl[1] + ctrl[0]) + 6 * t * (ctrl[3] - 2 * ctrl[2] + ctrl[1])


def _norm(v):
    n = np.linalg.norm(v)
    return v / n if n else v


def chord_param(pts):
    d = np.r_[0, np.cumsum(np.linalg.norm(np.diff(pts, axis=0), axis=1))]
    return d / d[-1]


def generate(pts, u, lt, rt):
    first, last = pts[0], pts[-1]
    A = np.stack([np.outer(3 * (1 - u) ** 2 * u, lt), np.outer(3 * (1 - u) * u**2, rt)], axis=1)
    C = np.zeros((2, 2))
    X = np.zeros(2)
    for i in range(len(pts)):
        C[0, 0] += A[i, 0] @ A[i, 0]
        C[0, 1] += A[i, 0] @ A[i, 1]
        C[1, 1] += A[i, 1] @ A[i, 1]
        tmp = pts[i] - q(np.array([first, first, last, last]), u[i])
        X[0] += A[i, 0] @ tmp
        X[1] += A[i, 1] @ tmp
    C[1, 0] = C[0, 1]
    det = C[0, 0] * C[1, 1] - C[1, 0] * C[0, 1]
    if abs(det) < 1e-12:
        al = ar = 0.0
    else:
        al = (X[0] * C[1, 1] - X[1] * C[0, 1]) / det
        ar = (C[0, 0] * X[1] - C[1, 0] * X[0]) / det
    seg = np.linalg.norm(last - first)
    eps = 1e-6 * seg
    if al < eps or ar < eps:
        al = ar = seg / 3.0
    return np.array([first, first + lt * al, last + rt * ar, last])


def max_error(pts, ctrl, u):
    d = np.linalg.norm(q(ctrl, u) - pts, axis=1)
    i = int(np.argmax(d))
    return d[i], i


def reparam(ctrl, pts, u):
    out = []
    for p, t in zip(pts, u):
        d = q(ctrl, t) - p
        qp = qprime(ctrl, t)
        qpp = qprimeprime(ctrl, t)
        num = d @ qp
        den = qp @ qp + d @ qpp
        out.append(t - num / den if den else t)
    return np.clip(np.array(out), 0, 1)


def fit_cubic(pts, lt, rt, err):
    if len(pts) == 2:
        dist = np.linalg.norm(pts[1] - pts[0]) / 3
        return [np.array([pts[0], pts[0] + lt * dist, pts[1] + rt * dist, pts[1]])]
    u = chord_param(pts)
    ctrl = generate(pts, u, lt, rt)
    e, split = max_error(pts, ctrl, u)
    if e < err:
        return [ctrl]
    if e < err * 4:
        for _ in range(30):
            u2 = reparam(ctrl, pts, u)
            ctrl = generate(pts, u2, lt, rt)
            e, split = max_error(pts, ctrl, u2)
            if e < err:
                return [ctrl]
            u = u2
    split = min(max(split, 1), len(pts) - 2)
    ct = _norm(pts[split - 1] - pts[split + 1])
    return fit_cubic(pts[: split + 1], lt, ct, err) + fit_cubic(pts[split:], -ct, rt, err)


def fit(pts, err, lt=None, rt=None):
    pts = np.asarray(pts, float)
    if lt is None:
        lt = _norm(pts[1] - pts[0])
    if rt is None:
        rt = _norm(pts[-2] - pts[-1])
    return fit_cubic(pts, lt, rt, err)
