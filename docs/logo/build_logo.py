#!/usr/bin/env python3
"""Dựng lại logo Timeless Harmony thành vector sạch.

Logo được vẽ lại từ artwork gốc (assets/brand/source-coming-soon.jpg):
- Vòng tròn mảnh, ngắt quãng ở hai bên cho chữ T và H.
- Dấu vô cực là MỘT nét liền không cắt nhau, hai đầu nét nở thành hai nụ tulip
  ("hold us together"). Hình đối xứng xoay 180° quanh tâm.
- Chữ T, H dựng bằng hình học. Wordmark: Belleza (khớp artwork gốc, làm đậm nhẹ);
  tagline: Lora 540. Cả hai là phông SIL Open Font License, được phép chuyển
  thành đường nét trong logo.

Mọi hình được xuất thành đường tô (fill) một màu, không cần phông khi mở.

Chạy:
    pip install fonttools brotli skia-pathops uharfbuzz numpy scipy
    npm pack @fontsource/belleza @fontsource-variable/lora  # rồi giải nén từng gói
    python3 docs/logo/build_logo.py --fonts <thư mục chứa các gói đã giải nén>
"""
import argparse
import glob
import io
import math
import os

import numpy as np
import pathops
import uharfbuzz as hb
from fontTools.pens.basePen import BasePen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from scipy.interpolate import PchipInterpolator

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ───────────────────────── Thông số hình học ─────────────────────────
# Đơn vị: biểu tượng nằm trong khung 1000×1000, tâm (500, 500).
C = np.array([500.0, 500.0])
R = 470.0               # bán kính đường tâm vòng tròn
RING_W = 9.0            # độ dày vòng tròn
GAP_HALF = 56.0         # nửa khoảng hở cho chữ T/H (đo theo trục dọc)
TH_CAP = 56.0           # chiều cao chữ T, H
TH_STEM = RING_W        # nét đứng của T, H
TH_BAR = 4.8            # nét ngang của T, H (= nét cánh hoa)
TH_T_W = 37.0           # bề ngang chữ T
TH_H_W = 43.0           # bề ngang chữ H

# Nửa đầu đường tâm dấu vô cực: từ gốc nụ trên-trái → đỉnh thùy trái →
# điểm cực trái → đáy thùy trái → tâm. Nửa sau = xoay 180°.
# Điểm neo đặt tại các cực trị với tay nắm ngang/dọc như vẽ tay trong Illustrator.
HALF = [
    [(406.0, 432.0), (375.0, 410.0), (332.2, 391.2), (300.9, 391.2)],
    [(300.9, 391.2), (238.2, 391.2), (172.7, 435.6), (172.7, 500.6)],
    [(172.7, 500.6), (172.7, 563.1), (236.4, 611.5), (299.5, 611.5)],
    [(299.5, 611.5), (382.2, 611.5), (442.8, 551.3), (500.0, 500.0)],
]
# Độ dày nét theo vị trí (0 = gốc nụ, 0.5 = tâm): mảnh ở nụ, đầy ở giữa.
WIDTH_PROFILE = [(0.0, 5.6), (0.05, 8.4), (0.2, 9.8), (0.32, 11.1), (0.42, 12.6), (0.5, 14.2)]

# Nụ tulip (đơn vị như trên): hai cánh ngoài xoè ±27°, cánh giữa ló ra phía sau.
BUD_AXIS_DEG = 35.5     # hướng trục nụ trên-trái (độ, y hướng xuống)
PETAL_LEN = 64.0
PETAL_SPREAD = 27.0
PETAL_LINE = 4.8        # độ dày nét viền cánh hoa
MID_LEN = 56.0


# ───────────────────────── Tiện ích đường ─────────────────────────
def bez(ctrl, t):
    ctrl = np.asarray(ctrl, float)
    t = np.asarray(t, float)[..., None]
    mt = 1 - t
    return mt**3 * ctrl[0] + 3 * mt**2 * t * ctrl[1] + 3 * mt * t**2 * ctrl[2] + t**3 * ctrl[3]


def rot180(pts):
    return 2 * C - np.asarray(pts, float)


def full_centerline():
    segs = [np.array(s, float) for s in HALF]
    back = [rot180(s[::-1]) for s in reversed(segs)]
    return segs + back


def sample(segs, n_per=400):
    pts = [bez(s, np.linspace(0, 1, n_per, endpoint=False)) for s in segs]
    pts.append(np.array([segs[-1][3]]))
    return np.vstack(pts)


def stroke(path, width, cap=pathops.LineCap.ROUND_CAP, join=pathops.LineJoin.ROUND_JOIN):
    p = pathops.Path()
    p.addPath(path)
    p.stroke(width, cap, join, 4)
    p.convertConicsToQuads()
    return pathops.simplify(p)


def union(*paths):
    paths = [p for p in paths if p is not None]
    out = paths[0]
    for p in paths[1:]:
        out = pathops.op(out, p, pathops.PathOp.UNION)
    return out


def minus(a, b):
    return pathops.op(a, b, pathops.PathOp.DIFFERENCE)


def poly_path(pts, closed=True):
    p = pathops.Path()
    p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    if closed:
        p.close()
    return p


def cubic_path(segs, closed=False, path=None):
    p = path if path is not None else pathops.Path()
    p.moveTo(*segs[0][0])
    for s in segs:
        p.cubicTo(*s[1], *s[2], *s[3])
    if closed:
        p.close()
    return p


def arc_cubics(cx, cy, r, a0, a1):
    """Cung tròn từ góc a0 tới a1 (radian) bằng các đoạn bezier ≤ 90°."""
    n = max(1, int(math.ceil(abs(a1 - a0) / (math.pi / 2))))
    out = []
    for i in range(n):
        t0 = a0 + (a1 - a0) * i / n
        t1 = a0 + (a1 - a0) * (i + 1) / n
        k = 4 / 3 * math.tan((t1 - t0) / 4)
        p0 = np.array([cx + r * math.cos(t0), cy + r * math.sin(t0)])
        p3 = np.array([cx + r * math.cos(t1), cy + r * math.sin(t1)])
        p1 = p0 + k * r * np.array([-math.sin(t0), math.cos(t0)])
        p2 = p3 - k * r * np.array([-math.sin(t1), math.cos(t1)])
        out.append(np.array([p0, p1, p2, p3]))
    return out


# ───────────────────────── Dấu vô cực ─────────────────────────
def infinity_body(width_scale=1.0, width_add=0.0):
    """Nét vô cực có độ dày thay đổi, xuất thành hình tô."""
    from bezfit import fit  # cùng thư mục

    segs = full_centerline()
    pts = sample(segs)
    d = np.r_[0, np.cumsum(np.linalg.norm(np.diff(pts, axis=0), axis=1))]
    s = d / d[-1]
    xs, ws = zip(*WIDTH_PROFILE)
    xs = list(xs) + [1 - x for x in reversed(xs[:-1])]
    ws = list(ws) + list(reversed(ws[:-1]))
    w = PchipInterpolator(xs, ws)(s) * width_scale + width_add
    tang = np.gradient(pts, axis=0)
    tang /= np.linalg.norm(tang, axis=1)[:, None]
    nrm = np.c_[-tang[:, 1], tang[:, 0]]
    left = pts + nrm * (w / 2)[:, None]
    right = pts - nrm * (w / 2)[:, None]
    # bỏ bớt điểm để khớp đường cong nhanh hơn
    left, right = left[::4], right[::4]
    if not np.allclose(left[-1], (pts + nrm * (w / 2)[:, None])[-1]):
        left = np.vstack([left, (pts + nrm * (w / 2)[:, None])[-1]])
        right = np.vstack([right, (pts - nrm * (w / 2)[:, None])[-1]])
    lf = fit(left, 0.15)
    rf = fit(right[::-1], 0.15)
    p = pathops.Path()
    p.moveTo(*lf[0][0])
    for b in lf:
        p.cubicTo(*b[1], *b[2], *b[3])
    # mũ tròn ở đầu cuối
    end, start = pts[-1], pts[0]
    a_end = math.atan2(*(left[-1] - end)[::-1])
    for b in arc_cubics(end[0], end[1], w[-1] / 2, a_end, a_end - math.pi):
        p.cubicTo(*b[1], *b[2], *b[3])
    for b in rf:
        p.cubicTo(*b[1], *b[2], *b[3])
    a_st = math.atan2(*(right[0] - start)[::-1])
    for b in arc_cubics(start[0], start[1], w[0] / 2, a_st, a_st - math.pi):
        p.cubicTo(*b[1], *b[2], *b[3])
    p.close()
    return pathops.simplify(p), pts


# ───────────────────────── Nụ tulip ─────────────────────────
def petal_outline(L):
    """Cánh hoa trong toạ độ riêng: gốc (0,0) → đỉnh; y>0 là phía ngoài.
    Mép ngoài phình tròn ở đáy (đáy chén tulip) rồi hất nhẹ ra ở đầu cánh."""
    P = lambda x, y: (x * L, y * L)
    tip = P(1.0, 0.10)
    return [
        np.array([(0, 0), P(0.15, 0.48), P(0.78, 0.04), tip]),
        np.array([tip, P(0.86, -0.07), P(0.36, -0.28), (0, 0)]),
    ]


def mid_outline(L, half=0.36):
    """Cánh giữa phía sau: hẹp ở gốc (bị hai cánh ngoài che), tròn ở đỉnh."""
    return [
        np.array([(0, 0), (0.45 * L, 0), (0.72 * L, half * L), (L, 0.03 * L)]),
        np.array([(L, 0.03 * L), (0.8 * L, -0.9 * half * L), (0.45 * L, 0), (0, 0)]),
    ]


def place(segs, angle_deg, origin, mirror=False):
    a = math.radians(angle_deg)
    R_ = np.array([[math.cos(a), -math.sin(a)], [math.sin(a), math.cos(a)]])
    out = []
    for s in segs:
        s = np.array(s, float)
        if mirror:
            s = s * np.array([1, -1])
        out.append(s @ R_.T + origin)
    return out


def closed(segs):
    return cubic_path(segs, closed=True)


def bud(origin, axis_deg, solid=False, line=PETAL_LINE, scale=1.0):
    """Một nụ tulip. solid=True: hình đặc cho bản logo nhỏ."""
    L = PETAL_LEN * scale
    # Cánh A xoè theo chiều kim đồng hồ (+), cánh B ngược lại (−, lật gương)
    A = place(petal_outline(L), axis_deg + PETAL_SPREAD, origin)
    B = place(petal_outline(L), axis_deg - PETAL_SPREAD, origin, mirror=True)
    M = place(mid_outline(MID_LEN * scale), axis_deg, origin)
    fa, fb, fm = closed(A), closed(B), closed(M)
    if solid:
        return union(fa, fb, fm)
    sa = stroke(cubic_path(A, closed=True), line)
    sb = stroke(cubic_path(B, closed=True), line)
    sm = stroke(cubic_path(M, closed=True), line)
    vis_a = minus(sa, fb)
    vis_m = minus(minus(sm, fa), fb)
    return union(sb, vis_a, vis_m)


# ───────────────────────── Chữ ─────────────────────────
class _PathopsPen(BasePen):
    def __init__(self, path):
        super().__init__(None)
        self.p = path

    def _moveTo(self, pt):
        self.p.moveTo(*pt)

    def _lineTo(self, pt):
        self.p.lineTo(*pt)

    def _curveToOne(self, p1, p2, p3):
        self.p.cubicTo(*p1, *p2, *p3)

    def _qCurveToOne(self, p1, p2):
        self.p.quadTo(*p1, *p2)

    def _closePath(self):
        self.p.close()

    def _endPath(self):
        self.p.close()


class Font:
    def __init__(self, path, wght=None):
        tt = TTFont(path)
        tt.flavor = None
        if wght is not None and "fvar" in tt:
            tt = instantiateVariableFont(tt, {"wght": wght})
        buf = io.BytesIO()
        tt.save(buf)
        self.data = buf.getvalue()
        self.tt = TTFont(io.BytesIO(self.data))
        self.gs = self.tt.getGlyphSet()
        self.upm = self.tt["head"].unitsPerEm
        self.order = self.tt.getGlyphOrder()
        self.hbfont = hb.Font(hb.Face(self.data))

    def cap_height(self):
        os2 = self.tt["OS/2"]
        return getattr(os2, "sCapHeight", 0) or 0.7 * self.upm

    def glyph_path(self, name):
        p = pathops.Path()
        self.gs[name].draw(_PathopsPen(p))
        return pathops.simplify(p)


def embolden(path, wx, wy):
    """Làm đậm nét theo hai chiều: wx cho nét đứng, wy cho nét ngang (đơn vị phông)."""
    if wx <= 0:
        return path
    s = wx / max(wy, 1e-3)
    tall = path.transform(1, 0, 0, s, 0, 0)
    st = stroke(tall, wx, join=pathops.LineJoin.ROUND_JOIN)
    return union(tall, st).transform(1, 0, 0, 1 / s, 0, 0)


def text_path(font, text, size, x=0.0, baseline=0.0, tracking=0.0, bold=(0, 0), align="left"):
    """Đường nét của một dòng chữ. size = cỡ em (đơn vị đầu ra); tracking theo em."""
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(font.hbfont, buf, {"kern": True, "liga": False})
    k = size / font.upm
    pen_x = 0.0
    out = pathops.Path()
    items = []
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        name = font.order[info.codepoint]
        gp = font.glyph_path(name)
        if bold != (0, 0):
            gp = embolden(gp, *bold)
        items.append((gp, pen_x + pos.x_offset, pos.y_offset))
        pen_x += pos.x_advance + tracking * font.upm
    pen_x -= tracking * font.upm
    for gp, gx, gy in items:
        out.addPath(gp.transform(k, 0, 0, -k, x + gx * k, baseline - gy * k))
    out = pathops.simplify(out)
    if align != "left":
        b = out.bounds
        w = b[2] - b[0]
        shift = x - (b[0] + w / 2) if align == "center" else 0
        out = out.transform(1, 0, 0, 1, shift, 0)
    return out


# ───────────────────────── Xuất SVG ─────────────────────────
def fmt(v):
    s = f"{v:.1f}"
    s = s.rstrip("0").rstrip(".") if "." in s else s
    return "0" if s in ("-0", "") else s


def svg_d(path):
    parts = []
    for verb, pts in path.segments:
        if verb == "moveTo":
            parts.append("M" + " ".join(f"{fmt(x)} {fmt(y)}" for x, y in pts))
        elif verb == "lineTo":
            parts.append("L" + " ".join(f"{fmt(x)} {fmt(y)}" for x, y in pts))
        elif verb == "curveTo":
            parts.append("C" + " ".join(f"{fmt(x)} {fmt(y)}" for x, y in pts))
        elif verb == "qCurveTo":
            # chuỗi quad TrueType: chuyển từng đoạn
            for a, b in pathops.decompose_quadratic_segment(pts):
                parts.append(f"Q{fmt(a[0])} {fmt(a[1])} {fmt(b[0])} {fmt(b[1])}")
        elif verb == "closePath":
            parts.append("Z")
    return "".join(parts)


def bounds(path, pad=0.0):
    x0, y0, x1, y1 = path.bounds
    return x0 - pad, y0 - pad, x1 + pad, y1 + pad


def write_svg(path, filename, color="currentColor", title=None, pad=2.0, box=None):
    x0, y0, x1, y1 = box or bounds(path, pad)
    # làm tròn khung về số nguyên cho gọn
    x0, y0 = math.floor(x0), math.floor(y0)
    x1, y1 = math.ceil(x1), math.ceil(y1)
    w, h = x1 - x0, y1 - y0
    t = f"<title>{title}</title>" if title else ""
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0} {y0} {w} {h}" '
        f'fill="{color}"{" role=\"img\"" if title else ""}>{t}'
        f'<path d="{svg_d(path)}"/></svg>\n'
    )
    with open(filename, "w") as f:
        f.write(svg)
    return (x0, y0, w, h)


# ───────────────────────── Dựng các phiên bản ─────────────────────────
def ring(width=RING_W, gaps=True):
    p = pathops.Path()
    if gaps:
        g = math.asin(GAP_HALF / R)
        for a in (arc_cubics(*C, R, math.pi + g, 2 * math.pi - g), arc_cubics(*C, R, g, math.pi - g)):
            cubic_path(a, path=p)
        return stroke(p, width, cap=pathops.LineCap.BUTT_CAP)
    cubic_path(arc_cubics(*C, R, 0, 2 * math.pi), closed=True, path=p)
    return stroke(p, width)


def infinity(solid_buds=False, width_scale=1.0, width_add=0.0, bud_scale=1.0, bud_line=PETAL_LINE,
             bud_turn=0.0, size=1.0):
    """bud_turn: xoay nụ (độ, âm = xa nét chéo); size: phóng cả hình quanh tâm."""
    body, pts = infinity_body(width_scale, width_add)
    b1 = bud(pts[0], BUD_AXIS_DEG + bud_turn, solid=solid_buds, line=bud_line, scale=bud_scale)
    b2 = bud(pts[-1], BUD_AXIS_DEG + 180 + bud_turn, solid=solid_buds, line=bud_line, scale=bud_scale)
    p = union(body, b1, b2)
    if size != 1.0:
        p = p.transform(size, 0, 0, size, C[0] * (1 - size), C[1] * (1 - size))
    return p


def letters_th():
    """Chữ T và H dựng hình học: nét đứng = độ dày vòng tròn, nét ngang = nét cánh hoa."""
    stem, bar, cap = TH_STEM, TH_BAR, TH_CAP
    y0, y1 = C[1] - cap / 2, C[1] + cap / 2

    def rect(x0, ya, x1, yb):
        return poly_path([(x0, ya), (x1, ya), (x1, yb), (x0, yb)])

    tx = C[0] - R
    t = union(rect(tx - TH_T_W / 2, y0, tx + TH_T_W / 2, y0 + bar),
              rect(tx - stem / 2, y0, tx + stem / 2, y1))
    hx = C[0] + R
    h = union(rect(hx - TH_H_W / 2, y0, hx - TH_H_W / 2 + stem, y1),
              rect(hx + TH_H_W / 2 - stem, y0, hx + TH_H_W / 2, y1),
              rect(hx - TH_H_W / 2, C[1] - bar / 2, hx + TH_H_W / 2, C[1] + bar / 2))
    return union(t, h)


# ───────────────────────── Chữ của logo ─────────────────────────
# Đo từ artwork gốc rồi đổi sang đơn vị biểu tượng (1 px ảnh gốc = K đơn vị).
K = R / 215.72
WORD_TEXT = "TIMELESS HARMONY"
WORD_CAP = 42.0 * K           # chiều cao chữ hoa
WORD_TRACK = -0.03            # khoảng chữ (em)
WORD_BOLD = (0.030, 0.006)    # làm đậm Belleza: nét đứng, nét ngang (× chiều cao chữ hoa)
TAG_TEXT = "hold us together"
TAG_ASC = 30.5 * K            # chiều cao chữ "l"
TAG_TRACK = 0.029
TAG_WGHT = 540                # độ đậm Lora (biến thiên 400–700)
GAP_MARK_WORD = 39.4 * K      # vòng tròn → đỉnh chữ hoa
GAP_WORD_TAG = 24.5 * K       # chân chữ hoa → đỉnh chữ "l"


def shift(path, dx, dy):
    return path.transform(1, 0, 0, 1, dx, dy)


def fit_box(path, x0=None, y0=None, cx=None, cy=None):
    b = path.bounds
    dx = (x0 - b[0]) if x0 is not None else (cx - (b[0] + b[2]) / 2) if cx is not None else 0
    dy = (y0 - b[1]) if y0 is not None else (cy - (b[1] + b[3]) / 2) if cy is not None else 0
    return shift(path, dx, dy)


def wordmark(belleza):
    cap = belleza.cap_height()
    bold = (WORD_BOLD[0] * cap, WORD_BOLD[1] * cap)
    h = embolden(belleza.glyph_path(belleza.tt.getBestCmap()[ord("H")]), *bold)
    hb_ = h.bounds
    size = WORD_CAP / (hb_[3] - hb_[1]) * belleza.upm
    p = text_path(belleza, WORD_TEXT, size, tracking=WORD_TRACK, bold=bold)
    # baseline = 0 → đỉnh chữ hoa ở y = -WORD_CAP
    return p


def tagline(lora):
    lp = lora.glyph_path(lora.tt.getBestCmap()[ord("l")])
    lb = lp.bounds
    size = TAG_ASC / (lb[3] - lb[1]) * lora.upm
    return text_path(lora, TAG_TEXT, size, tracking=TAG_TRACK)


def lockup_stacked(mark, word, tag):
    """Biểu tượng trên, chữ dưới — đúng bố cục artwork gốc."""
    ring_bottom = C[1] + R + RING_W / 2
    base = ring_bottom + GAP_MARK_WORD + WORD_CAP
    w = fit_box(word, cx=C[0])
    w = shift(w, 0, base)
    t = fit_box(tag, cx=C[0])
    t = shift(t, 0, base + GAP_WORD_TAG + TAG_ASC)
    return union(mark, w, t)


def mark_medium():
    """Bản nét vừa cho cỡ 64–160 px và cho logo ngang: bỏ T/H, nét dày hơn, nụ viền."""
    return union(ring(width=24, gaps=False),
                 infinity(width_scale=1.9, width_add=6, bud_line=10, bud_scale=1.1))


def lockup_horizontal(word, tag):
    """Biểu tượng trái, chữ phải — cho chữ ký email, tiêu đề tài liệu, bìa hồ sơ."""
    text_h = WORD_CAP + GAP_WORD_TAG + TAG_ASC
    m = mark_medium()
    mb = m.bounds
    scale = (text_h * 1.9) / (mb[3] - mb[1])
    m = fit_box(m.transform(scale, 0, 0, scale, 0, 0), x0=0, cy=0)
    x_text = m.bounds[2] + WORD_CAP * 0.9
    top = -text_h / 2
    w = shift(fit_box(word, x0=x_text), 0, top + WORD_CAP)
    t = shift(fit_box(tag, x0=x_text + 2), 0, top + WORD_CAP + GAP_WORD_TAG + TAG_ASC)
    return union(m, w, t)


def compact_mark():
    """Bản rút gọn cho cỡ dưới 64 px: bỏ chữ T/H, nét dày, dấu vô cực to hơn trong vòng."""
    return union(ring(width=32, gaps=False),
                 infinity(width_scale=2.3, width_add=8, bud_line=13, bud_scale=1.25, size=1.1))


# ───────────────────────── Bản màu "Vườn kính" ─────────────────────────
INK = "#18301F"                                   # mực lá đậm
PINK = {"m": "#B8325A", "a": "#E0567A", "b": "#F08AA6"}   # cánh sau, cánh trước, cánh sáng
PINK_ON_ORB = {"m": "#FF9DB8", "a": "#FFD3DF", "b": "#FFFFFF"}
ORB_DEFS = (
    '<defs><linearGradient id="o" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2F7FD6"/>'
    '<stop offset=".52" stop-color="#57ADE2"/><stop offset=".8" stop-color="#55B77A"/><stop offset="1" stop-color="#2F8F55"/></linearGradient>'
    '<radialGradient id="s" cx=".3" cy=".18" r=".8"><stop offset="0" stop-color="#fff" stop-opacity=".62"/>'
    '<stop offset=".5" stop-color="#fff" stop-opacity=".07"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
    '<linearGradient id="r" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".95"/>'
    '<stop offset=".5" stop-color="#fff" stop-opacity=".3"/><stop offset="1" stop-color="#fff" stop-opacity=".7"/></linearGradient></defs>'
)


def infinity_parts(width_scale=1.9, width_add=6, bud_scale=1.32, size=1.0):
    """Dấu vô cực tách phần: thân (body) và ba cánh của mỗi nụ (m, a, b) để tô màu riêng."""
    body, pts = infinity_body(width_scale, width_add)
    parts = [("body", body)]
    for o, ang in ((pts[0], BUD_AXIS_DEG), (pts[-1], BUD_AXIS_DEG + 180)):
        L = PETAL_LEN * bud_scale
        parts.append(("m", closed(place(mid_outline(MID_LEN * bud_scale), ang, o))))
        parts.append(("a", closed(place(petal_outline(L), ang + PETAL_SPREAD, o))))
        parts.append(("b", closed(place(petal_outline(L), ang - PETAL_SPREAD, o, mirror=True))))
    if size != 1.0:
        parts = [(k, p.transform(size, 0, 0, size, C[0] * (1 - size), C[1] * (1 - size))) for k, p in parts]
    return parts


def parts_svg(parts, body_fill, pink):
    return "".join(f'<path fill="{body_fill if k == "body" else pink[k]}" d="{svg_d(p)}"/>' for k, p in parts)


def moved(parts, a, dx, dy):
    return [(k, p.transform(a, 0, 0, a, dx, dy)) for k, p in parts]


def orb_inner(square=False):
    shape = '<rect width="1000" height="1000" fill="url(#o)"/>' if square else '<circle cx="500" cy="500" r="492" fill="url(#o)"/>'
    gloss = '<rect width="1000" height="1000" fill="url(#s)"/>' if square else (
        '<circle cx="500" cy="500" r="492" fill="url(#s)"/><circle cx="500" cy="500" r="481" fill="none" stroke="url(#r)" stroke-width="14"/>')
    mark = parts_svg(infinity_parts(width_scale=2.3, width_add=8, size=1.12 if not square else 1.0), "#fff", PINK_ON_ORB)
    return ORB_DEFS + shape + gloss + mark


def write_raw(filename, viewbox, inner, title=None):
    t = f"<title>{title}</title>" if title else ""
    with open(filename, "w") as fh:
        fh.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}"{" role=\"img\"" if title else ""}>{t}{inner}</svg>\n')


def color_variants(word, tag, site_dir, kit_dir):
    """Logo màu: quả cầu trời–cỏ, dấu vô cực trắng; chữ mực lá đậm (hoặc trắng cho nền tối)."""
    out = {}
    write_raw(os.path.join(site_dir, "logo-orb.svg"), "0 0 1000 1000", orb_inner(), "Timeless Harmony")
    write_raw(os.path.join(ROOT, "favicon.svg"), "0 0 1000 1000", orb_inner())
    write_raw(os.path.join(kit_dir, "logo-orb.svg"), "0 0 1000 1000", orb_inner(), "Timeless Harmony")
    write_raw(os.path.join(kit_dir, "app-icon.svg"), "0 0 1000 1000", orb_inner(square=True))
    # dấu vô cực màu trên nền trong suốt (thân mực, nụ hồng) — đặt trên kính sáng
    inf = infinity_parts(width_scale=1.5, width_add=3, bud_scale=1.25)
    write_raw(os.path.join(site_dir, "logo-infinity-color.svg"), "150 360 700 280", parts_svg(inf, INK, PINK))
    # bản đầy đủ và bản ngang, chữ mực / chữ trắng
    text_h = WORD_CAP + GAP_WORD_TAG + TAG_ASC
    for suffix, ink in (("", INK), ("-light", "#FFFFFF")):
        # dọc: cầu trên, chữ dưới
        orb_d = 760.0
        w = shift(fit_box(word, cx=500), 0, orb_d + 80 + WORD_CAP)
        t = shift(fit_box(tag, cx=500), 0, orb_d + 80 + WORD_CAP + GAP_WORD_TAG + TAG_ASC)
        k = orb_d / 1000
        inner = f'<g transform="translate({500 - orb_d / 2} 0) scale({k})">{orb_inner()}</g><path fill="{ink}" d="{svg_d(w)}"/><path fill="{ink}" d="{svg_d(t)}"/>'
        wb, tb = w.bounds, t.bounds
        x0, x1 = min(wb[0], 500 - orb_d / 2) - 4, max(wb[2], 500 + orb_d / 2) + 4
        vb = f"{math.floor(x0)} -4 {math.ceil(x1 - x0)} {math.ceil(tb[3] + 8)}"
        for d in (site_dir, kit_dir):
            write_raw(os.path.join(d, f"logo-lockup-color{suffix}.svg"), vb, inner, "Timeless Harmony — hold us together")
        out[f"logo-lockup-color{suffix}"] = vb
        # ngang: cầu trái, chữ phải
        od = text_h * 1.9
        k = od / 1000
        xt = od + WORD_CAP * 0.8
        w = shift(fit_box(word, x0=xt), 0, od / 2 - text_h / 2 + WORD_CAP)
        t = shift(fit_box(tag, x0=xt + 2), 0, od / 2 - text_h / 2 + WORD_CAP + GAP_WORD_TAG + TAG_ASC)
        inner = f'<g transform="scale({k:.4f})">{orb_inner()}</g><path fill="{ink}" d="{svg_d(w)}"/><path fill="{ink}" d="{svg_d(t)}"/>'
        vb = f"-4 -4 {math.ceil(w.bounds[2] + 8)} {math.ceil(od + 8)}"
        for d in (site_dir, kit_dir):
            write_raw(os.path.join(d, f"logo-horizontal-color{suffix}.svg"), vb, inner, "Timeless Harmony — hold us together")
        out[f"logo-horizontal-color{suffix}"] = vb
    return out


def find_fonts(fonts_dir):
    def one(pattern):
        hits = sorted(glob.glob(os.path.join(fonts_dir, "**", pattern), recursive=True))
        if not hits:
            raise SystemExit(f"Không thấy phông {pattern} trong {fonts_dir}")
        return hits[0]

    return one("belleza-latin-400-normal.woff2"), one("lora-latin-wght-normal.woff2")


COLORS = {"ink": "#18301F", "white": "#FFFFFF"}   # bản một màu: mực lá / trắng


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fonts", required=True)
    ap.add_argument("--site", default=os.path.join(ROOT, "assets", "brand"),
                    help="thư mục SVG dùng trên website (currentColor)")
    ap.add_argument("--kit", default=os.path.join(ROOT, "docs", "logo", "svg"),
                    help="thư mục SVG có màu cố định để gửi in ấn/đối tác")
    args = ap.parse_args()
    belleza_path, lora_path = find_fonts(args.fonts)
    belleza = Font(belleza_path)
    lora = Font(lora_path, wght=TAG_WGHT)

    inf = infinity()
    mark = union(ring(), letters_th(), inf)
    word = wordmark(belleza)
    tag = tagline(lora)
    variants = {
        "logo-lockup": (lockup_stacked(mark, word, tag), "Timeless Harmony — hold us together"),
        "logo-horizontal": (lockup_horizontal(word, tag), "Timeless Harmony — hold us together"),
        "logo-mark": (mark, "Timeless Harmony"),
        "logo-mark-medium": (mark_medium(), "Timeless Harmony"),
        "logo-infinity": (inf, None),
        "logo-wordmark": (word, "Timeless Harmony"),
        "logo-tagline": (tag, "hold us together"),
        "logo-compact": (compact_mark(), "Timeless Harmony"),
    }
    os.makedirs(args.site, exist_ok=True)
    os.makedirs(args.kit, exist_ok=True)
    info = {}
    # Biểu tượng tròn: khung vuông, tâm vòng tròn ở giữa khung
    boxes = {"logo-mark": (6, 6, 994, 994)}
    for name, (path, title) in variants.items():
        box = boxes.get(name)
        info[name] = write_svg(path, os.path.join(args.site, f"{name}.svg"), box=box)
        if name in ("logo-infinity", "logo-tagline"):
            continue
        for cname, col in COLORS.items():
            write_svg(path, os.path.join(args.kit, f"{name}-{cname}.svg"), color=col, title=title, box=box)

    # Bản màu "Vườn kính": quả cầu, favicon, bản đầy đủ/ngang có màu
    for name, vb in color_variants(word, tag, args.site, args.kit).items():
        x, y, w, h = vb.split()
        info[name] = (x, y, float(w), float(h))
    return info


if __name__ == "__main__":
    import sys

    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    for k, v in main().items():
        print(f"{k:16s} viewBox {v[0]} {v[1]} {v[2]} {v[3]}  tỉ lệ {v[2] / v[3]:.4f}")
