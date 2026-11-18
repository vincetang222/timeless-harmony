#!/usr/bin/env python3
"""Vẽ hình nền của Timeless Harmony bằng vector: lễ cưới trong vườn biệt thự bên hồ ở Ý.

Bố cục (1600×1000, neo đáy, cắt hai bên trên điện thoại nên mọi thứ quan trọng nằm ở giữa):
trời → dãy núi bên kia hồ → mặt hồ ngọc lam → lan can đá → thảm cỏ, lối sỏi, hai dãy ghế,
lối đi viền hoa trắng dẫn tới cổng hoa; sau cổng hoa là chùm pháo bông ngày nhiều màu xoè hình quạt.
Khách mời chỉ là hình dáng nhỏ nhìn từ phía sau, không có gương mặt.

Xuất SVG nguồn vào docs/design/.build/, sau đó render_background.js xuất ảnh WebP vào assets/bg/.
Chạy: python3 docs/design/build_background.py && node docs/design/render_background.js
"""
import math
import os
import random

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "docs", "design", ".build")   # SVG nguồn (không commit); ảnh dùng trên web do render_background.js xuất
W, H = 1600, 1000
VP = (800.0, 560.0)          # điểm tụ của phối cảnh sân vườn
ARCH = (800.0, 748.0)        # chân cổng hoa
ORIGIN = (800.0, 676.0)      # gốc chùm pháo bông (sau cổng hoa, sát mép hồ)

DAY = dict(
    sky=[("0", "#4C97E6"), ("0.3", "#86BFF2"), ("0.52", "#CDE6F9")],
    far=("#9DBFCE", "#89B0BE"), mnt=[("0", "#5C9777"), ("0.5", "#447A60"), ("1", "#4F8A72")],
    fold_d="#2B5A46", fold_l="#8EC29B", shore="#E9E2D2", town=["#F4EBDD", "#E9D6BE", "#E2B9A0", "#FFFFFF"],
    lake=[("0", "#4FC0CB"), ("0.5", "#2FA5BC"), ("1", "#238FAC")], shimmer="#FFFFFF",
    stone="#DDD5C6", stone_d="#BFB5A2", gravel="#E8DFCF", gravel_d="#D5CAB6",
    lawn=[("0", "#86C56F"), ("0.5", "#5CAA59"), ("1", "#45934D")], stripe="#FFFFFF", stripe_op=0.055,
    cone=("#3F8559", "#2B6644"), hedge=("#4B8F60", "#35744D"), leafdot="#6FB07C",
    chair="#F6EEE0", chair_line="#CDAE74", guests=["#2B2B33", "#3B4A63", "#F1D9DD", "#E9E2D0", "#6A7F9A", "#B98D8D", "#1F2A38", "#D7C3E3"],
    hair=["#2A211C", "#4A3426", "#7A5636", "#C9A36A", "#1B1B1F"],
    bloom=["#FFFFFF", "#FFFFFF", "#FFF6E8", "#FBE6EA", "#F6F1E4", "#F8D9D0"], bloom_leaf="#A9D3A2",
    platform="#FFFFFF", smoke="#FFFFFF", fw_op=0.95, glow_op=0.5, shadow="#1E4A36", shadow_op=0.22,
    fw=["#FFC53D", "#FF8A2A", "#F2443B", "#E0338A", "#9140D2", "#2E5BE3", "#2F9BEF", "#2CCFD6", "#33C68C"],
)
NIGHT = dict(
    sky=[("0", "#040A1A"), ("0.3", "#0B1D3E"), ("0.52", "#1A3A5E")],
    far=("#13293F", "#102438"), mnt=[("0", "#11303A"), ("0.55", "#0D2731"), ("1", "#0A2029")],
    fold_d="#07171F", fold_l="#2B5560", shore="#3A4A5A", town=["#FFD58A", "#FFC46B", "#FFE9B8", "#FFB36B"],
    lake=[("0", "#143A5C"), ("0.5", "#0E2C4A"), ("1", "#0A2138")], shimmer="#BFD6F5",
    stone="#5C6470", stone_d="#444B57", gravel="#3F4852", gravel_d="#343C46",
    lawn=[("0", "#1B5A45"), ("0.5", "#14483A"), ("1", "#0E3A30")], stripe="#FFFFFF", stripe_op=0.035,
    cone=("#124034", "#0A2B24"), hedge=("#134538", "#0B2E27"), leafdot="#1F6650",
    chair="#B9B4AC", chair_line="#8C7A55", guests=["#15151B", "#232E40", "#A99AA2", "#9D998D", "#44566E", "#7C6163", "#101822", "#8D82A0"],
    hair=["#141110", "#2A1E17", "#4A3524", "#8A7350", "#0E0E12"],
    bloom=["#F3F5FA", "#E6EAF2", "#EDE6DA", "#E9D7DD", "#DDE3EC"], bloom_leaf="#3E7A66",
    platform="#D9DEE8", smoke="#C9D6F0", fw_op=1.0, glow_op=0.75, shadow="#02090C", shadow_op=0.4,
    fw=["#FFD866", "#FFA24A", "#FF5A52", "#FF4FA8", "#B266FF", "#5B86FF", "#55B8FF", "#4EE6EA", "#52E6A6"],
)


def f(v):
    s = f"{v:.1f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def lerp(a, b, t):
    return a + (b - a) * t


def mix(c1, c2, t):
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(lerp(x, y, t)):02X}" for x, y in zip(a, b))


def ramp(cols, t):
    t = min(max(t, 0), 0.9999) * (len(cols) - 1)
    i = int(t)
    return mix(cols[i], cols[i + 1], t - i)


def smooth(pts):
    """Đường cong mềm qua các điểm (Catmull-Rom → Bézier)."""
    d = f"M{f(pts[0][0])} {f(pts[0][1])}"
    for i in range(len(pts) - 1):
        p0, p1, p2, p3 = pts[max(i - 1, 0)], pts[i], pts[i + 1], pts[min(i + 2, len(pts) - 1)]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f"C{f(c1[0])} {f(c1[1])} {f(c2[0])} {f(c2[1])} {f(p2[0])} {f(p2[1])}"
    return d


def interp(pts, x):
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if x0 <= x <= x1:
            return lerp(y0, y1, (x - x0) / (x1 - x0))
    return pts[-1][1]


def gx(xb, y):
    """Hoành độ tại cao độ y của đường trên mặt sân đi qua điểm tụ và chạm đáy ảnh ở xb."""
    return VP[0] + (xb - VP[0]) * (y - VP[1]) / (H - VP[1])


def grad(id_, stops, x2=0, y2=1):
    return f'<linearGradient id="{id_}" x1="0" y1="0" x2="{x2}" y2="{y2}">' + "".join(f'<stop offset="{a}" stop-color="{c}"/>' for a, c in stops) + "</linearGradient>"


def firework(P, R, night):
    ox, oy = ORIGIN
    o = []

    def ray(a_deg, r0, r1, bend):
        a = math.radians(a_deg)
        dx, dy = math.cos(a), -math.sin(a)
        px, py = -dy, dx
        x0, y0 = ox + dx * r0, oy + dy * r0
        r1 *= 1 + 0.14 * max(0.0, -dx)                                 # cánh trái xoè rộng hơn
        x1, y1 = ox + dx * r1, oy + dy * r1 + (r1 / 560) ** 2 * 26      # đầu tia hơi rủ xuống
        cx, cy = ox + dx * (r0 + r1) / 2 + px * bend, oy + dy * (r0 + r1) / 2 + py * bend
        return f"M{f(x0)} {f(y0)}Q{f(cx)} {f(cy)} {f(x1)} {f(y1)}", (x1, y1), (dx, dy)

    def col(a_deg):
        return ramp(P["fw"], (168 - a_deg) / 156 + R.uniform(-0.05, 0.05))

    # khói màu: các vệt rộng, nhoè
    glow = []
    for _ in range(130):
        a = R.uniform(12, 168)
        d, _, _ = ray(a, R.uniform(40, 120), R.uniform(300, 520), R.uniform(-14, 14))
        glow.append(f'<path d="{d}" stroke="{col(a)}" stroke-width="{f(R.uniform(14, 34))}" opacity="{f(R.uniform(0.35, 0.8))}"/>')
    o.append(f'<g filter="url(#b5)" fill="none" stroke-linecap="round" opacity="{P["glow_op"]}">{"".join(glow)}</g>')
    soft = []
    for _ in range(240):
        a = R.uniform(10, 170)
        d, _, _ = ray(a, R.uniform(30, 110), R.uniform(280, 540), R.uniform(-12, 12))
        soft.append(f'<path d="{d}" stroke="{col(a)}" stroke-width="{f(R.uniform(3, 8))}" opacity="{f(R.uniform(0.3, 0.7))}"/>')
    o.append(f'<g filter="url(#b3)" fill="none" stroke-linecap="round">{"".join(soft)}</g>')
    # tia mảnh
    rays, tips = [], []
    for _ in range(980):
        a = R.uniform(10, 170) if R.random() < 0.85 else R.gauss(90, 40)
        if not 8 < a < 172:
            continue
        r1 = R.uniform(300, 560) * (0.82 + 0.18 * math.sin(math.radians(a)))
        d, tip, dirv = ray(a, R.uniform(18, 110), r1, R.uniform(-10, 10))
        rays.append(f'<path d="{d}" stroke="{mix(col(a), "#FFFFFF", R.uniform(0, 0.35))}" stroke-width="{f(R.uniform(0.6, 1.9))}" opacity="{f(R.uniform(0.4, 1))}"/>')
        tips.append((tip, dirv, a))
    o.append(f'<g filter="url(#b1)" fill="none" stroke-linecap="round">{"".join(rays)}</g>')
    # tia trắng nổ lách tách + hạt sáng ở đầu tia
    crack = []
    for _ in range(16):
        a = R.uniform(25, 155)
        r = R.uniform(170, 360)
        x, y = ox + math.cos(math.radians(a)) * r, oy - math.sin(math.radians(a)) * r
        d = f"M{f(x)} {f(y)}"
        for _ in range(R.randint(4, 7)):
            x += R.uniform(-16, 16)
            y += R.uniform(-22, -6)
            d += f"L{f(x)} {f(y)}"
        crack.append(f'<path d="{d}" stroke="#fff" stroke-width="{f(R.uniform(0.7, 1.4))}" opacity="{f(R.uniform(0.5, 0.9))}"/>')
    o.append(f'<g fill="none" stroke-linejoin="round">{"".join(crack)}</g>')
    sp = []
    for (tx, ty), (dx, dy), a in R.sample(tips, 420):
        for k in range(R.randint(1, 3)):
            t = R.uniform(0.02, 0.2) * k
            sp.append(f'<circle cx="{f(tx + dx * 40 * t + R.uniform(-6, 6))}" cy="{f(ty + dy * 40 * t + R.uniform(-6, 6))}" r="{f(R.uniform(0.7, 1.9))}" fill="{"#fff" if R.random() < 0.6 else "#FFF2B8"}" opacity="{f(R.uniform(0.5, 1))}"/>')
    return f'<g mask="url(#fwm)" opacity="{P["fw_op"]}">{"".join(o)}</g><g>{"".join(sp)}</g>'


def scene(P, night=False, seed=12):
    R = random.Random(seed)
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMax slice">']
    ox, oy = ORIGIN
    o.append(
        "<defs>" + grad("sky", P["sky"]) + grad("mnt", P["mnt"]) + grad("far", [("0", P["far"][0]), ("1", P["far"][1])])
        + grad("lake", P["lake"]) + grad("lawn", P["lawn"]) + grad("cone", [("0", P["cone"][0]), ("1", P["cone"][1])], 1, 0)
        + grad("hedge", [("0", P["hedge"][0]), ("1", P["hedge"][1])])
        + "".join(f'<filter id="b{n}" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="{d}"/></filter>'
                  for n, d in ((1, 0.6), (2, 1.6), (3, 3.5), (4, 8), (5, 15), (6, 30)))
        + f'<radialGradient id="fwg" gradientUnits="userSpaceOnUse" cx="{ox}" cy="{oy}" r="640"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
        '<stop offset=".05" stop-color="#fff" stop-opacity="1"/><stop offset=".58" stop-color="#fff" stop-opacity="1"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
        '<mask id="fwm" maskUnits="userSpaceOnUse" x="0" y="0" width="1600" height="1000"><rect width="1600" height="1000" fill="url(#fwg)"/></mask>'
        '<radialGradient id="sun"><stop offset="0" stop-color="#fff" stop-opacity=".9"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
        f'<linearGradient id="mlight" x1="1" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="{0.06 if night else 0.2}"/><stop offset=".5" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".14"/></linearGradient>'
        f'<linearGradient id="haze" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{P["sky"][2][1]}" stop-opacity="0"/><stop offset="1" stop-color="{P["sky"][2][1]}" stop-opacity="{0.25 if night else 0.42}"/></linearGradient>'
        "</defs>"
    )
    o.append(f'<rect width="{W}" height="560" fill="url(#sky)"/>')
    # ── trời: mây (ngày) / sao + trăng (đêm)
    if not night:
        o.append('<circle cx="1330" cy="120" r="420" fill="url(#sun)" opacity=".55"/>')
        cl = []
        for cx, cy, w, h, n in ((1250, 96, 360, 86, 8), (1500, 150, 240, 60, 6), (180, 120, 260, 54, 6), (930, 60, 200, 40, 5), (420, 215, 180, 34, 5)):
            parts = [f'<ellipse cx="{cx}" cy="{cy}" rx="{w / 2}" ry="{f(h * 0.3)}"/>']
            for i in range(n * 2):
                u = (i + 0.5) / (n * 2)
                r = h * (0.26 + 0.5 * math.sin(math.pi * u) ** 0.8) * R.uniform(0.7, 1.15)
                parts.append(f'<circle cx="{f(cx - w / 2 + u * w + R.uniform(-10, 10))}" cy="{f(cy - r * R.uniform(0.3, 0.7))}" r="{f(r)}"/>')
            cl.append(f'<g fill="#C9DDF0" transform="translate(0 10)" opacity=".75">{"".join(parts)}</g><g fill="#fff">{"".join(parts)}</g>')
        o.append(f'<g filter="url(#b4)" opacity=".9">{"".join(cl)}</g>')
        o.append('<g filter="url(#b5)" fill="#fff" opacity=".5"><ellipse cx="620" cy="150" rx="300" ry="9"/><ellipse cx="1100" cy="250" rx="260" ry="7"/><ellipse cx="300" cy="300" rx="240" ry="6"/></g>')
    else:
        st = "".join(f'<circle cx="{f(R.uniform(0, W))}" cy="{f(R.uniform(0, 1) ** 1.4 * 470)}" r="{R.choice([0.6, 0.8, 1, 1.3, 1.7])}" opacity="{f(R.uniform(0.3, 1))}"/>' for _ in range(260))
        o.append(f'<g fill="#fff">{st}</g>')
        o.append('<circle cx="300" cy="130" r="300" fill="url(#sun)" opacity=".22"/><circle cx="300" cy="130" r="34" fill="#F4F1E1"/>'
                 '<circle cx="289" cy="121" r="7" fill="#DCD8C4" opacity=".55"/><circle cx="311" cy="141" r="4.6" fill="#DCD8C4" opacity=".5"/>')

    # ── núi xa (xanh khói) và khối núi chính có nếp gấp
    far_r = [(840, 360), (960, 300), (1080, 244), (1210, 208), (1330, 192), (1450, 214), (1560, 246), (1660, 262)]
    far_l = [(-60, 318), (60, 296), (180, 312), (300, 352), (420, 392)]
    o.append(f'<g filter="url(#b2)"><path d="{smooth(far_r)}L1660 540L840 540Z" fill="url(#far)"/><path d="{smooth(far_l)}L420 540L-60 540Z" fill="url(#far)"/></g>')
    ridge = [(-60, 438), (80, 372), (220, 312), (350, 258), (470, 208), (580, 170), (680, 150), (770, 166), (860, 212), (940, 236),
             (1020, 220), (1100, 204), (1180, 232), (1270, 286), (1370, 332), (1480, 362), (1660, 384)]
    o.append(f'<path d="{smooth(ridge)}L1660 532L-60 532Z" fill="url(#mnt)"/>')
    folds_d, folds_l = [], []
    for _ in range(120):
        x = R.uniform(-20, 1620)
        y0 = interp(ridge, min(max(x, -60), 1660)) + R.uniform(6, 34)
        dx = (x - 690) * 0.11 + R.uniform(-12, 12)               # nếp toả ra hai bên đỉnh
        d = f"M{f(x)} {f(y0)}C{f(x + dx * 0.25)} {f(lerp(y0, 526, 0.4))} {f(x + dx * 0.8)} {f(lerp(y0, 526, 0.75))} {f(x + dx)} 528"
        w = R.uniform(4, 15)
        folds_d.append(f'<path d="{d}" stroke-width="{f(w)}"/>')
        folds_l.append(f'<path d="{d}" stroke-width="{f(w * 0.7)}" transform="translate({f(w * 1.1)} 0)"/>')
    o.append(f'<g fill="none" stroke-linecap="round" filter="url(#b3)"><g stroke="{P["fold_d"]}" opacity=".24">{"".join(folds_d)}</g><g stroke="{P["fold_l"]}" opacity=".18">{"".join(folds_l)}</g></g>')
    tex = "".join(f'<circle cx="{f(x)}" cy="{f(lerp(interp(ridge, x) + 8, 520, R.random()))}" r="{f(R.uniform(1, 3.4))}" fill="{R.choice([P["fold_d"], P["fold_l"]])}"/>' for x in [R.uniform(-20, 1620) for _ in range(700)])
    o.append(f'<g filter="url(#b1)" opacity=".2">{tex}</g>')
    o.append(f'<path d="{smooth(ridge)}L1660 532L-60 532Z" fill="url(#mlight)"/><rect x="0" y="400" width="{W}" height="132" fill="url(#haze)"/>')
    # ── bờ hồ bên kia: dải làng nhỏ
    town = "".join(f'<rect x="{f(R.uniform(0, W))}" y="{f(R.uniform(519, 527))}" width="{f(R.uniform(2.5, 7))}" height="{f(R.uniform(2, 5))}" fill="{R.choice(P["town"])}" opacity="{f(R.uniform(0.6, 1))}"/>' for _ in range(210))
    o.append(f'<rect x="0" y="527" width="{W}" height="5" fill="{P["shore"]}" opacity=".5"/><g filter="url(#b1)">{town}</g>')

    # ── mặt hồ
    o.append(f'<rect x="0" y="530" width="{W}" height="150" fill="url(#lake)"/>')
    o.append(f'<path d="{smooth([(x, 530 + (532 - y) * 0.2) for x, y in ridge])}L1660 530L-60 530Z" fill="{P["fold_d"]}" opacity=".28" filter="url(#b4)"/>')
    refl = "".join(f'<ellipse cx="{f(ox + (i - 4) * 64)}" cy="{f(R.uniform(575, 640))}" rx="{f(R.uniform(60, 110))}" ry="{f(R.uniform(12, 24))}" fill="{P["fw"][i]}"/>' for i in range(9))
    o.append(f'<g filter="url(#b5)" opacity="{0.5 if night else 0.3}">{refl}</g>')
    sh = "".join(f'<rect x="{f(R.uniform(-20, W))}" y="{f(R.uniform(536, 676))}" width="{f(R.uniform(16, 130))}" height="{f(R.uniform(0.8, 1.8))}" rx="1" opacity="{f(R.uniform(0.1, 0.4))}"/>' for _ in range(120))
    o.append(f'<g fill="{P["shimmer"]}">{sh}</g>')
    if night:
        lights = "".join(f'<rect x="{f(R.uniform(0, W))}" y="531" width="{f(R.uniform(1.5, 3))}" height="{f(R.uniform(10, 34))}" fill="{R.choice(P["town"])}" opacity="{f(R.uniform(0.25, 0.6))}"/>' for _ in range(90))
        o.append(f'<g filter="url(#b2)">{lights}</g>')
    else:
        o.append('<path d="M1010 584l-34 5 78 3z" fill="#fff" opacity=".8"/><path d="M1052 590q60 2 130 16M1052 592q50 8 96 26" stroke="#fff" stroke-width="1.4" fill="none" opacity=".5"/>')

    # ── pháo bông (sau cổng hoa, trước mặt hồ và núi)
    o.append(f'<g filter="url(#b6)" opacity="{0.55 if night else 0.75}"><ellipse cx="{ox}" cy="{oy - 10}" rx="150" ry="42" fill="{P["smoke"]}"/><ellipse cx="{ox - 90}" cy="{oy - 34}" rx="90" ry="34" fill="{P["smoke"]}"/><ellipse cx="{ox + 100}" cy="{oy - 30}" rx="96" ry="30" fill="{P["smoke"]}"/></g>')
    o.append(firework(P, R, night))

    # ── sân: nền sỏi, lan can đá có ban công cong ở giữa
    edge = [(-20, 664), (640, 664), (690, 656), (740, 646), (800, 642), (860, 646), (910, 656), (960, 664), (1620, 664)]
    o.append(f'<path d="{smooth(edge)}L1620 1000L-20 1000Z" fill="{P["gravel"]}"/>')
    rail = smooth([(x, y - 13) for x, y in edge])
    posts = "".join(f'<path d="M{f(x)} {f(interp(edge, x) - 12)}v12"/>' for x in range(0, W, 11))
    o.append(f'<g fill="none" stroke="{P["stone_d"]}" stroke-width="1.6" opacity=".8">{posts}</g>')
    o.append(f'<path d="{rail}" fill="none" stroke="{P["stone"]}" stroke-width="4.5"/><path d="{smooth(edge)}" fill="none" stroke="{P["stone_d"]}" stroke-width="3"/>')
    for px in (640, 960):
        o.append(f'<rect x="{px - 7}" y="640" width="14" height="28" fill="{P["stone"]}"/><circle cx="{px}" cy="636" r="6.5" fill="{P["stone"]}"/>')

    # ── thảm cỏ theo phối cảnh, vệt cắt cỏ, lối sỏi hai bên
    top = 700

    def quad(xa, xb_, fill, op=1, extra=""):
        return f'<path d="M{f(gx(xa, top))} {top}L{f(gx(xb_, top))} {top}L{f(xb_)} {H}L{f(xa)} {H}Z" fill="{fill}" opacity="{op}"{extra}/>'

    o.append(quad(130, 1470, "url(#lawn)"))
    o.append(f'<path d="M-20 {top}L{f(gx(-240, top))} {top}L-240 {H}L-20 {H}Z" fill="url(#lawn)"/><path d="M1620 {top}L{f(gx(1840, top))} {top}L1840 {H}L1620 {H}Z" fill="url(#lawn)"/>')
    for xb in range(130, 1470, 96):
        o.append(quad(xb, xb + 48, P["stripe"], P["stripe_op"]))
    o.append(f'<g filter="url(#b3)" opacity=".5">{quad(-240, 130, P["gravel_d"], 0.25)}{quad(1470, 1840, P["gravel_d"], 0.25)}</g>')

    peb = []
    for _ in range(900):
        y = R.uniform(668, H)
        xb = R.choice([R.uniform(-240, 130), R.uniform(1470, 1840)]) if y > top else R.uniform(-900, 2500)
        peb.append(f'<circle cx="{f(gx(xb, max(y, top)) if y > top else R.uniform(0, W))}" cy="{f(y)}" r="{f(R.uniform(0.5, 1.5) * (0.5 + (y - 660) / 340))}"/>')
    o.append(f'<g fill="{P["gravel_d"]}" opacity=".55">{"".join(peb)}</g>')
    # ── hàng rào cây, cây tỉa hình nón, cầu bụi
    hed = []
    for side in (-1, 1):
        for i in range(9):
            x = 800 + side * R.uniform(700, 860)
            y = R.uniform(600, 760)
            hed.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(R.uniform(46, 88))}"/>')
    o.append(f'<g fill="url(#hedge)" filter="url(#b2)">{"".join(hed)}</g>')

    def cone(cx, base, h, w):
        dots = "".join(f'<circle cx="{f(cx + R.uniform(-0.36, 0.36) * w * (1 - t))}" cy="{f(base - h * t)}" r="{f(R.uniform(0.8, 2.2))}"/>' for t in [R.uniform(0.03, 0.92) for _ in range(150)])
        return (f'<ellipse cx="{cx - w * 0.55}" cy="{base + 10}" rx="{w * 1.05}" ry="13" fill="{P["shadow"]}" opacity="{P["shadow_op"]}" filter="url(#b3)" transform="rotate(-8 {cx} {base})"/>'
                f'<path d="M{cx - w / 2} {base}Q{cx - w * 0.44} {base - h * 0.56} {cx} {base - h}Q{cx + w * 0.44} {base - h * 0.56} {cx + w / 2} {base}Q{cx} {base + 12} {cx - w / 2} {base}Z" fill="url(#cone)"/>'
                f'<path d="M{cx + w * 0.06} {base - h * 0.96}Q{cx + w * 0.44} {base - h * 0.56} {cx + w / 2} {base}Q{cx + w * 0.3} {base + 6} {cx + w * 0.16} {base + 7}Q{cx + w * 0.3} {base - h * 0.5} {cx + w * 0.06} {base - h * 0.96}Z" fill="{P["leafdot"]}" opacity=".45" filter="url(#b2)"/>'
                f'<g fill="{P["leafdot"]}" opacity=".4" filter="url(#b1)">{dots}</g>')

    def ball(cx, cy, r):
        return (f'<ellipse cx="{cx + 6}" cy="{cy + r * 0.8}" rx="{r * 1.1}" ry="{r * 0.3}" fill="{P["shadow"]}" opacity="{P["shadow_op"]}" filter="url(#b2)"/>'
                f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#cone)"/><circle cx="{cx - r * 0.3}" cy="{cy - r * 0.3}" r="{r * 0.5}" fill="{P["leafdot"]}" opacity=".35" filter="url(#b2)"/>')

    o.append(cone(452, 722, 156, 108) + cone(1148, 722, 156, 108) + cone(120, 742, 190, 130) + cone(1480, 742, 190, 130))
    o.append(ball(676, 740, 24) + ball(924, 740, 24) + ball(560, 716, 18) + ball(1040, 716, 18))

    # ── bục trắng, cô dâu chú rể (hình dáng nhỏ), cổng hoa
    ax, ay = ARCH
    o.append(f'<ellipse cx="{ax + 8}" cy="{ay + 22}" rx="96" ry="10" fill="{P["shadow"]}" opacity="{P["shadow_op"]}" filter="url(#b3)"/>'
             f'<rect x="{ax - 82}" y="{ay - 2}" width="164" height="20" rx="4" fill="{P["platform"]}"/><rect x="{ax - 92}" y="{ay + 12}" width="184" height="9" rx="3" fill="{P["platform"]}" opacity=".85"/>')
    o.append(f'<g transform="translate({ax} {ay - 2}) scale(1.3) translate({-ax} {-(ay - 2)})"><path d="M{ax - 12} {ay - 2}l-12 0q4-16 9-26q2-3 5 0q4 12 6 26z" fill="#fff"/><path d="M{ax - 16} {ay - 30}q-9 8-11 24" stroke="#fff" stroke-width="3" fill="none" opacity=".7"/>'
             f'<circle cx="{ax - 15}" cy="{ay - 33}" r="3.4" fill="#5A3E2E"/><rect x="{ax + 2}" y="{ay - 30}" width="9" height="29" rx="3" fill="#1D2530"/><circle cx="{ax + 6.5}" cy="{ay - 34}" r="3.6" fill="#2A211C"/></g>')
    blooms, leaves = [], []
    for i in range(460):
        a = math.pi + math.pi * R.random()
        thick = R.uniform(-13, 13)
        x, y = ax + (70 + thick) * math.cos(a), ay + (106 + thick) * math.sin(a)
        (leaves if R.random() < 0.12 else blooms).append((x, y, R.uniform(3, 7.5)))
    for sx in (-70, 70):                                    # chân cổng toả xuống bục
        for _ in range(26):
            blooms.append((ax + sx + R.uniform(-13, 13), ay + R.uniform(-8, 10), R.uniform(3, 7)))
    o.append(f'<g fill="{P["shadow"]}" opacity=".2" filter="url(#b2)" transform="translate(3 4)">' + "".join(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}"/>' for x, y, r in blooms[::3]) + "</g>")
    o.append(f'<g fill="{P["bloom_leaf"]}">' + "".join(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}"/>' for x, y, r in leaves) + "</g>")
    o.append("".join(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="{R.choice(P["bloom"])}"/>' for x, y, r in blooms))
    if night:                                               # dây đèn trên cổng hoa
        o.append('<g fill="#FFE3A3">' + "".join(f'<circle cx="{f(ax + 70 * math.cos(math.pi + math.pi * k / 26))}" cy="{f(ay + 106 * math.sin(math.pi + math.pi * k / 26))}" r="1.8"/>' for k in range(27)) + "</g>")

    # ── hai dãy ghế + khách (nhìn từ sau) và hai luống hoa trắng viền lối đi
    rows = [762 + 232 * (k / 10) ** 1.15 for k in range(11)]
    for y in rows:
        s = (y - VP[1]) / (H - VP[1])
        row = []
        for xa, xb_ in ((270, 520), (1080, 1330)):
            x0, x1 = gx(xa, y), gx(xb_, y)
            for i in range(7):
                x = lerp(x0, x1, (i + 0.5) / 7)
                row.append(f'<ellipse cx="{f(x + 5 * s)}" cy="{f(y + 3 * s)}" rx="{f(15 * s)}" ry="{f(4 * s)}" fill="{P["shadow"]}" opacity="{P["shadow_op"]}"/>')
                if R.random() < 0.72:
                    c = R.choice(P["guests"])
                    row.append(f'<path d="M{f(x - 12.5 * s)} {f(y - 6 * s)}q{f(1 * s)} {f(-21 * s)} {f(12.5 * s)} {f(-21 * s)}t{f(12.5 * s)} {f(21 * s)}z" fill="{c}"/><circle cx="{f(x)}" cy="{f(y - 31 * s)}" r="{f(5.2 * s)}" fill="{R.choice(P["hair"])}"/>')
                row.append(f'<path d="M{f(x - 9.5 * s)} {f(y)}v{f(-13 * s)}q0 {f(-10 * s)} {f(9.5 * s)} {f(-10 * s)}t{f(9.5 * s)} {f(10 * s)}v{f(13 * s)}z" fill="{P["chair"]}" stroke="{P["chair_line"]}" stroke-width="{f(1.1 * s)}"/>')
        o.append("".join(row))
    fl_s, fl = [], []
    for xb in (560, 1040):
        for _ in range(360):
            y = lerp(752, H + 10, R.random() ** 0.8)
            s = (y - VP[1]) / (H - VP[1])
            x = gx(xb, y) + R.uniform(-17, 17) * s
            r = R.uniform(3, 9.5) * s
            fl.append((y, x, r))
    fl.sort()
    o.append(f'<g fill="{P["shadow"]}" opacity=".28" filter="url(#b2)" transform="translate(5 5)">' + "".join(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}"/>' for y, x, r in fl[::2]) + "</g>")
    o.append("".join(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="{P["bloom_leaf"] if R.random() < 0.08 else R.choice(P["bloom"])}"/>' for y, x, r in fl))
    if night:                                               # nến dọc lối đi
        o.append('<g filter="url(#b1)">' + "".join(f'<circle cx="{f(gx(xb, y) + sgn * 26 * (y - VP[1]) / (H - VP[1]))}" cy="{f(y)}" r="{f(3.2 * (y - VP[1]) / (H - VP[1]))}" fill="#FFD98A"/>'
                                                   for xb, sgn in ((560, 1), (1040, -1)) for y in rows) + "</g>")
    o.append("</svg>")
    return "".join(o)


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, svg in (("scene-day.svg", scene(DAY)), ("scene-night.svg", scene(NIGHT, night=True))):
        with open(os.path.join(OUT, name), "w") as fh:
            fh.write(svg)
        print(f"{name:16s} {len(svg) / 1024:.0f} KB")


if __name__ == "__main__":
    main()
