#!/usr/bin/env python3
"""Vẽ hình nền "Vườn kính" của Timeless Harmony bằng vector (không dùng ảnh ngoài).

Xuất 4 tệp vào assets/bg/:
  meadow-day.svg / meadow-night.svg  — dải đồi, thảm cỏ, hoa; lặp ngang liền mạch (2400×460)
  sky-day.svg / sky-night.svg        — mây + nắng / sao + trăng (nền trong suốt, 1600×1000)
Màu trời là gradient trong theme.css. Chạy: python3 docs/design/build_background.py
"""
import math
import os
import random

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "assets", "bg")
W, H = 2400, 460
TAU = math.tau

DAY = dict(
    far="#BFE0D6", far2="#A9D6C4", mid_a="#9AD6A0", mid_b="#79C386", tree="#5FAE78", tree2="#74BD86",
    near=[("0", "#93D873"), ("0.35", "#5DB65F"), ("1", "#2F8A4C")],
    grass=["#3E9B4F", "#57B25A", "#7DCB63", "#2F8246", "#A2DD7A"],
    stem="#3A8F4C", leaf="#4BA75C", leaf2="#3D9451",
    tulips=["#F26D8F", "#E8425F", "#FFD166", "#FFFFFF", "#F7A1B8", "#FF8FA3", "#C86BD9"],
    daisy=["#FFFFFF", "#FFFFFF", "#FFF3C4", "#FFD9E4"], eye="#F7C948",
    lav=["#8F7BE8", "#A891F2", "#6FA8F5"], dots=["#FFFFFF", "#FFD166", "#F7A1B8", "#F26D8F", "#C9B8FF"],
    fg_leaf="#3F9B57", light="#E9FFC9", light_op=0.5, flower_op=1.0,
)
NIGHT = dict(
    far="#1B3A4A", far2="#173644", mid_a="#17403F", mid_b="#123634", tree="#0E2C2D", tree2="#134038",
    near=[("0", "#1B5540"), ("0.35", "#12402F"), ("1", "#092418")],
    grass=["#14503A", "#1B6045", "#237550", "#0E3B2B", "#2F8A5C"],
    stem="#17573D", leaf="#1D6A49", leaf2="#165840",
    tulips=["#D98CA6", "#C56A84", "#E3CF98", "#E6EEF5", "#D7A9BC", "#DDA0AE", "#A98BC9"],
    daisy=["#E6EEF5", "#DCE7F0", "#E8E2C4", "#E3CFDA"], eye="#D9B95A",
    lav=["#7E78C9", "#948BD6", "#6C93CC"], dots=["#DCE7F0", "#E3CF98", "#D7A9BC", "#B9B0E6"],
    fg_leaf="#124532", light="#8FD6B4", light_op=0.16, flower_op=0.92,
)


def f(v):
    s = f"{v:.1f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def ridge(base, waves):
    """Đường đồi tuần hoàn theo chiều ngang (để lặp liền mạch)."""
    def y(x):
        return base + sum(a * math.sin(TAU * k * x / W + p) for a, k, p in waves)
    return y


def ridge_path(yf, step=40):
    pts = [(x, yf(x)) for x in range(-step, W + step + 1, step)]
    d = f"M{f(pts[0][0])} {f(pts[0][1])}"
    for i in range(1, len(pts) - 1):
        mx, my = (pts[i][0] + pts[i + 1][0]) / 2, (pts[i][1] + pts[i + 1][1]) / 2
        d += f"Q{f(pts[i][0])} {f(pts[i][1])} {f(mx)} {f(my)}"
    return d + f"L{W + step} {H}L{-step} {H}Z"


def wrap(x, margin):
    """Các vị trí cần vẽ để phần tử sát mép xuất hiện ở cả hai bên."""
    xs = [x]
    if x < margin:
        xs.append(x + W)
    if x > W - margin:
        xs.append(x - W)
    return xs


def meadow(P, seed=11, night=False):
    R = random.Random(seed)
    far = ridge(62, [(16, 2, 0.4), (9, 5, 1.9)])
    mid = ridge(104, [(20, 3, 2.2), (10, 7, 0.3)])
    near = ridge(166, [(13, 2, 4.0), (7, 5, 1.1), (3, 11, 2.0)])
    o = []
    o.append(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}">')
    stops = "".join(f'<stop offset="{a}" stop-color="{c}"/>' for a, c in P["near"])
    o.append(
        "<defs>"
        f'<linearGradient id="n" x1="0" y1="0" x2="0" y2="1">{stops}</linearGradient>'
        f'<linearGradient id="m" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{P["mid_a"]}"/><stop offset="1" stop-color="{P["mid_b"]}"/></linearGradient>'
        f'<linearGradient id="fr" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{P["far"]}"/><stop offset="1" stop-color="{P["far2"]}"/></linearGradient>'
        '<filter id="b1"><feGaussianBlur stdDeviation="1.4"/></filter>'
        '<filter id="b3"><feGaussianBlur stdDeviation="3"/></filter>'
        '<filter id="b8" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="7"/></filter>'
        '<filter id="b20" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="22"/></filter>'
        # hoa tulip: thân + lá (tl), đài hoa (tc, tô theo currentColor)
        f'<g id="tl"><path d="M0 0C1-18-1-36 0-52" fill="none" stroke="{P["stem"]}" stroke-width="2.4" stroke-linecap="round"/>'
        f'<path d="M0 0C-9-10-15-26-11-40C-7-28-3-14 0 0Z" fill="{P["leaf"]}"/><path d="M0-2C8-10 12-22 9-32C6-22 3-10 0-2Z" fill="{P["leaf2"]}"/></g>'
        '<g id="tc"><path d="M0-79C5-72 6-62 0-53C-6-62-5-72 0-79Z" fill="currentColor"/><path d="M0-79C5-72 6-62 0-53C-6-62-5-72 0-79Z" fill="#000" opacity=".16"/>'
        '<path d="M0-52C-9-52-12-62-7.5-76C-3.5-71-1-62 0-52Z" fill="currentColor"/><path d="M0-52C9-52 12-62 7.5-76C3.5-71 1-62 0-52Z" fill="currentColor"/>'
        '<path d="M0-52C9-52 12-62 7.5-76C3.5-71 1-62 0-52Z" fill="#000" opacity=".07"/><path d="M-2-55C-8-56-9.5-64-7-72C-5-66-3-60-2-55Z" fill="#fff" opacity=".28"/></g>'
        # cúc: cánh theo currentColor
        f'<g id="ds"><path d="M0 0C1-12-1-24 0-34" fill="none" stroke="{P["stem"]}" stroke-width="1.6" stroke-linecap="round"/>'
        + "".join(f'<ellipse cx="0" cy="-41" rx="2.3" ry="6.2" fill="currentColor" transform="rotate({a} 0 -34)"/>' for a in range(0, 360, 36))
        + f'<circle cx="0" cy="-34" r="3.3" fill="{P["eye"]}"/></g>'
        # oải hương
        f'<g id="lv"><path d="M0 0C1-14-1-30 0-46" fill="none" stroke="{P["stem"]}" stroke-width="1.5" stroke-linecap="round"/>'
        + "".join(f'<ellipse cx="{2.6 if i % 2 else -2.6}" cy="{-22 - i * 3.4}" rx="2.7" ry="3.5" fill="currentColor"/>' for i in range(8))
        + '<ellipse cx="0" cy="-50" rx="2.4" ry="3.4" fill="currentColor"/></g>'
        "</defs>"
    )
    # đồi xa, đồi giữa + hàng cây, thảm cỏ gần
    o.append(f'<path d="{ridge_path(far)}" fill="url(#fr)"/>')
    o.append(f'<path d="{ridge_path(mid)}" fill="url(#m)"/>')
    trees = []
    for _ in range(46):
        x = R.uniform(0, W)
        r = R.uniform(7, 17)
        col = R.choice([P["tree"], P["tree2"]])
        for xx in wrap(x, 60):
            y = mid(x) + r * 0.25
            trees.append(f'<circle cx="{f(xx)}" cy="{f(y - r * 0.5)}" r="{f(r)}" fill="{col}"/>')
            trees.append(f'<circle cx="{f(xx + r * 0.9)}" cy="{f(y - r * 0.2)}" r="{f(r * 0.75)}" fill="{col}"/>')
            trees.append(f'<circle cx="{f(xx - r * 0.8)}" cy="{f(y - r * 0.1)}" r="{f(r * 0.7)}" fill="{col}"/>')
    o.append(f'<g filter="url(#b1)">{"".join(trees)}</g>')
    o.append(f'<path d="{ridge_path(near)}" fill="url(#n)"/>')
    # mảng nắng trên cỏ
    lights = []
    for _ in range(9):
        x = R.uniform(0, W)
        y = R.uniform(190, 330)
        for xx in wrap(x, 320):
            lights.append(f'<ellipse cx="{f(xx)}" cy="{f(y)}" rx="{f(R.uniform(140, 300))}" ry="{f(R.uniform(16, 38))}" fill="{P["light"]}"/>')
    o.append(f'<g filter="url(#b20)" opacity="{P["light_op"]}">{"".join(lights)}</g>')
    # hoa li ti phía xa
    dots = []
    for _ in range(420):
        x = R.uniform(0, W)
        t = R.random() ** 1.7
        y = near(x) + 6 + t * 150
        dots.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(0.8 + t * 1.9)}" fill="{R.choice(P["dots"])}" opacity="{f(0.55 + 0.4 * R.random())}"/>')
    o.append("".join(dots))

    # cỏ + hoa theo từng lớp chiều sâu (xa → gần)
    bands = 12
    for b in range(bands):
        t0, t1 = b / bands, (b + 1) / bands
        blades = {c: [] for c in P["grass"]}
        s_mid = 0.42 + 1.65 * ((t0 + t1) / 2) ** 1.25
        n = int(W / (15 * s_mid))
        for _ in range(n):
            x = R.uniform(0, W)
            t = R.uniform(t0, t1)
            s = 0.42 + 1.65 * t ** 1.25
            y = near(x) + 8 + t * (H - 150)
            h = R.uniform(16, 44) * s
            w = R.uniform(1.6, 3.4) * s
            dx = R.uniform(-0.5, 0.5) * h
            col = R.choice(P["grass"])
            for xx in wrap(x, 60):
                blades[col].append(
                    f"M{f(xx - w / 2)} {f(y)}q{f(dx * 0.3)} {f(-h * 0.6)} {f(dx + w / 2)} {f(-h)}q{f(-dx * 0.55 + w * 0.3)} {f(h * 0.45)} {f(-dx + w / 2)} {f(h)}z"
                )
        for col, ds in blades.items():
            if ds:
                o.append(f'<path d="{"".join(ds)}" fill="{col}"/>')
        flowers = []
        nf = int(22 - b * 0.9)
        for _ in range(nf):
            x = R.uniform(0, W)
            t = R.uniform(t0, t1)
            s = 0.42 + 1.5 * t ** 1.15
            y = near(x) + 10 + t * (H - 150)
            kind = R.choices(["t", "d", "l"], [0.5, 0.3, 0.2])[0]
            rot = R.uniform(-9, 9)
            if kind == "t":
                col = R.choice(P["tulips"])
                body = '<use xlink:href="#tl"/><use xlink:href="#tc"/>'
            elif kind == "d":
                col = R.choice(P["daisy"])
                body = '<use xlink:href="#ds"/>'
            else:
                col = R.choice(P["lav"])
                body = '<use xlink:href="#lv"/>'
            for xx in wrap(x, 90):
                flowers.append((y, f'<g transform="translate({f(xx)} {f(y)}) rotate({f(rot)}) scale({f(s)})" color="{col}">{body}</g>'))
        flowers.sort()
        o.append(f'<g opacity="{P["flower_op"]}">{"".join(fl for _, fl in flowers)}</g>')

    # tiền cảnh mờ: lá to và vài bông tulip sát ống kính
    fg = []
    for i in range(9):
        x = (i + R.uniform(0.15, 0.85)) * W / 9
        col = R.choice(P["tulips"][:3] + P["tulips"][4:6])
        s = R.uniform(2.6, 3.8)
        rot = R.uniform(-14, 14)
        for xx in wrap(x, 260):
            fg.append(f'<ellipse cx="{f(xx + 46)}" cy="{H + 20}" rx="{f(9 * s)}" ry="{f(46 * s)}" fill="{P["fg_leaf"]}" opacity=".8" transform="rotate({f(rot + 26)} {f(xx + 46)} {H + 20})"/>')
            if i % 3 != 1:
                fg.append(f'<g transform="translate({f(xx)} {H + 70}) rotate({f(rot)}) scale({f(s)})" color="{col}"><use xlink:href="#tl"/><use xlink:href="#tc"/></g>')
    o.append(f'<g filter="url(#b8)" opacity=".93">{"".join(fg)}</g>')

    if night:  # đom đóm
        ff = []
        for _ in range(46):
            x, y = R.uniform(0, W), R.uniform(150, 430)
            r = R.uniform(1.6, 3.2)
            ff.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r * 2.6)}" fill="#FFE9A3" opacity=".22"/><circle cx="{f(x)}" cy="{f(y)}" r="{f(r * 0.7)}" fill="#FFF6D0"/>')
        o.append(f'<g filter="url(#b1)">{"".join(ff)}</g>')
    o.append("</svg>")
    return "".join(o)


def cloud(R, cx, cy, w, h, n):
    parts = [f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{f(w / 2)}" ry="{f(h * 0.34)}"/>']
    for i in range(n):
        u = (i + 0.5) / n
        x = cx - w / 2 + u * w + R.uniform(-0.04, 0.04) * w
        r = h * (0.34 + 0.5 * math.sin(math.pi * u) ** 0.8) * R.uniform(0.82, 1.12)
        parts.append(f'<circle cx="{f(x)}" cy="{f(cy - r * 0.55)}" r="{f(r)}"/>')
    return "".join(parts)


def sky(night=False, seed=5):
    R = random.Random(seed)
    o = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 1000">']
    o.append(
        "<defs>"
        '<filter id="c1" x="-20%" y="-40%" width="140%" height="180%"><feGaussianBlur stdDeviation="5.5"/></filter>'
        '<filter id="c2" x="-30%" y="-60%" width="160%" height="220%"><feGaussianBlur stdDeviation="20"/></filter>'
        '<radialGradient id="sun" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#FFFDF2" stop-opacity=".95"/><stop offset=".18" stop-color="#FFF9DE" stop-opacity=".6"/><stop offset=".5" stop-color="#FFF6D6" stop-opacity=".18"/><stop offset="1" stop-color="#FFF6D6" stop-opacity="0"/></radialGradient>'
        '<radialGradient id="moon" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#E9F1FF" stop-opacity=".55"/><stop offset=".35" stop-color="#BFD4F5" stop-opacity=".16"/><stop offset="1" stop-color="#BFD4F5" stop-opacity="0"/></radialGradient>'
        "</defs>"
    )
    clouds = [(300, 215, 430, 120, 7, 1.0), (1265, 300, 350, 96, 6, 0.96), (830, 118, 210, 58, 5, 0.85),
              (120, 520, 230, 52, 5, 0.7), (990, 545, 280, 56, 6, 0.66), (1450, 500, 220, 48, 5, 0.7), (620, 395, 170, 40, 4, 0.6)]
    if not night:
        o.append('<circle cx="1120" cy="160" r="560" fill="url(#sun)"/>')
        o.append('<g filter="url(#c2)" fill="#fff" opacity=".55"><ellipse cx="640" cy="330" rx="330" ry="22"/><ellipse cx="1400" cy="150" rx="260" ry="18"/><ellipse cx="260" cy="640" rx="300" ry="20"/></g>')
        for cx, cy, w, h, n, op in clouds:
            shape = cloud(R, cx, cy, w, h, n)
            o.append(f'<g filter="url(#c1)" opacity="{op}"><g fill="#BFD9EE" transform="translate(0 9)">{shape}</g><g fill="#fff">{shape}</g></g>')
    else:
        stars = []
        for _ in range(230):
            x, y = R.uniform(0, 1600), R.uniform(0, 1) ** 1.5 * 760
            r = R.choice([0.7, 0.8, 0.9, 1.1, 1.3, 1.7])
            stars.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{r}" opacity="{f(R.uniform(0.35, 1))}"/>')
        o.append(f'<g fill="#fff">{"".join(stars)}</g>')
        o.append('<circle cx="1000" cy="128" r="330" fill="url(#moon)"/><circle cx="1000" cy="128" r="40" fill="#F3F0DF"/>'
                 '<circle cx="986" cy="117" r="8" fill="#DDD9C4" opacity=".55"/><circle cx="1013" cy="142" r="5.5" fill="#DDD9C4" opacity=".5"/><circle cx="1008" cy="110" r="3.6" fill="#DDD9C4" opacity=".45"/>')
        for cx, cy, w, h, n, op in clouds[:5]:
            o.append(f'<g filter="url(#c1)" fill="#8FA9C9" opacity="{f(op * 0.22)}">{cloud(R, cx, cy, w, h, n)}</g>')
    o.append("</svg>")
    return "".join(o)


def main():
    os.makedirs(OUT, exist_ok=True)
    files = {
        "meadow-day.svg": meadow(DAY),
        "meadow-night.svg": meadow(NIGHT, night=True),
        "sky-day.svg": sky(),
        "sky-night.svg": sky(night=True),
    }
    for name, svg in files.items():
        with open(os.path.join(OUT, name), "w") as fh:
            fh.write(svg)
        print(f"{name:18s} {len(svg) / 1024:.0f} KB")


if __name__ == "__main__":
    main()
