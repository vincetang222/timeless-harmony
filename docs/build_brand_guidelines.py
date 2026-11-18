"""Dựng docs/brand-guidelines.html (tự chứa: SVG nhúng sẵn, logo màu và thảm cỏ dạng data URI).
Chạy: python3 docs/build_brand_guidelines.py .   (từ thư mục gốc repo)
Hệ nhận diện: "Vườn kính" (glass) — nguồn sự thật về màu và kính là theme.css."""
import re, sys, base64
ROOT = sys.argv[1] if len(sys.argv) > 1 else '.'
A = ROOT + '/assets/brand/'
BG = ROOT + '/assets/bg/'

# ── SVG một màu → sprite <symbol> (currentColor) ──
ids = ['logo-mark', 'logo-mark-medium', 'logo-infinity', 'logo-horizontal', 'logo-wordmark', 'logo-tagline', 'logo-lockup', 'logo-compact', 'tulip-top-left', 'tulip-right', 'tulip-bottom', 'tulip-bottom-left']
VB = {}; symbols = []
for i in ids:
    s = open(A + i + '.svg').read()
    vb = re.search(r'viewBox="([^"]+)"', s).group(1); VB[i] = vb
    inner = s[s.index('>') + 1:s.rindex('</svg>')]
    attrs = 'fill="currentColor"' if i.startswith('logo-') else 'fill="currentColor" fill-rule="evenodd"'
    symbols.append(f'<symbol id="{i}" viewBox="{vb}" {attrs}>{inner}</symbol>')
def art(i, cls='', style=''):
    x, y, w, h = VB[i].split()
    return f'<svg class="art {cls}" viewBox="{VB[i]}" style="{style}" aria-hidden="true"><use href="#{i}" x="{x}" y="{y}" width="{w}" height="{h}"/></svg>'

# ── SVG có gradient → <img data:URI> (không đưa vào sprite) ──
def b64(path):
    return 'data:image/svg+xml;base64,' + base64.b64encode(open(path, 'rb').read()).decode()
URI = {n: b64(A + n + '.svg') for n in ['logo-orb', 'logo-lockup-color', 'logo-lockup-color-light', 'logo-horizontal-color', 'logo-horizontal-color-light', 'logo-infinity-color']}
MEADOW_DAY = b64(BG + 'meadow-day.svg'); MEADOW_NIGHT = b64(BG + 'meadow-night.svg')
def img(n, style='', alt=''):
    return f'<img class="cimg" src="{URI[n]}" alt="{alt}" style="{style}">'

# ── Độ tương phản WCAG 2.1 (tính thật) ──
def lum(h):
    h = h.lstrip('#'); c = [int(h[k:k+2], 16) / 255 for k in (0, 2, 4)]
    c = [x / 12.92 if x <= .03928 else ((x + .055) / 1.055) ** 2.4 for x in c]
    return .2126 * c[0] + .7152 * c[1] + .0722 * c[2]
def ratio(a, b):
    x, y = sorted([lum(a), lum(b)], reverse=True); return (x + .05) / (y + .05)
def level(r):
    return ('AAA', 'pass') if r >= 7 else ('AA', 'pass') if r >= 4.5 else ('Chỉ chữ lớn', 'fail') if r >= 3 else ('✕', 'fail')
GLASS_WORST = '#BCE0BD'   # kính trắng 60% phủ lên cỏ
rows = [
 ('#18301F', '#FFFFFF', 'Mực lá', 'Chữ chính'),
 ('#18301F', GLASS_WORST, 'Mực lá', 'Chữ chính, kính xấu nhất'),
 ('#2F4A3A', '#FFFFFF', 'Chữ phụ', 'Đoạn văn phụ'),
 ('#2F4A3A', GLASS_WORST, 'Chữ phụ', 'Đoạn văn phụ, kính xấu nhất'),
 ('#47604F', '#FFFFFF', 'Chữ mờ', 'Chú thích, ngày tháng'),
 ('#47604F', GLASS_WORST, 'Chữ mờ', 'Chú thích, kính xấu nhất'),
 ('#226340', '#FFFFFF', 'Lá', 'Liên kết, icon, nhãn'),
 ('#226340', GLASS_WORST, 'Lá', 'Liên kết, kính xấu nhất'),
 ('#A32545', '#FFFFFF', 'Tulip đậm', 'Chữ nhấn, giá tiền'),
 ('#A32545', GLASS_WORST, 'Tulip đậm', 'Chữ nhấn trên kính xấu nhất'),
 ('#FFFFFF', '#1C563A', 'Chữ trắng', 'Nút chính (đáy gradient)'),
 ('#FFFFFF', '#2F7F55', 'Chữ trắng', 'Nút chính (đỉnh gradient)'),
 ('#F1F6F2', '#0E1C26', 'Chữ chính (tối)', 'Đêm vườn: chữ chính'),
 ('#AEC1B6', '#0E1C26', 'Chữ mờ (tối)', 'Đêm vườn: chú thích'),
 ('#9FDDB0', '#0E1C26', 'Xanh nhấn (tối)', 'Đêm vườn: liên kết, icon'),
 ('#FF9DB8', '#0E1C26', 'Hồng nhấn (tối)', 'Đêm vườn: chữ nhấn, giá'),
]
CT = {}
def contrast_row(fg, bg, name, use):
    r = ratio(fg, bg); lv, cl = level(r); CT[(fg, bg)] = r
    chip = f'<span class="cchip" style="background:{bg};color:{fg}">Aa</span>'
    return f'<tr><td>{chip}{name} <code>{fg}</code> trên <code>{bg}</code></td><td>{r:.2f}:1</td><td class="{cl}">{lv}</td><td>{use}</td></tr>'.replace('.', ',', 0)
CONTRAST_HTML = ''.join(contrast_row(*r).replace(f'{CT[(r[0], r[1])]:.2f}:1', f'{CT[(r[0], r[1])]:.2f}:1'.replace('.', ',')) for r in rows)
for r in rows: print(f'{r[0]} / {r[1]}: {ratio(r[0], r[1]):.2f}')

def swatch(name, vi, hexv, role, dark=False, border=False, bg=None, meta=None):
    if meta is None:
        r, g, b = [int(hexv[k:k+2], 16) for k in (1, 3, 5)]; meta = f'RGB {r} · {g} · {b}'
    return f'''<div class="sw"><div class="sw-chip{' sw-border' if border else ''}" style="background:{bg or hexv};color:{'#FFFFFF' if dark else '#18301F'}"><span>{hexv}</span></div>
      <p class="sw-name">{vi} <em>{name}</em></p><p class="sw-meta">{meta}</p><p class="sw-role">{role}</p></div>'''

html = f'''<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex">
<title>Timeless Harmony — Brand Guideline</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@300;400;500;600;700&family=Lora:ital,wght@0,400;0,500;1,400;1,500&family=Philosopher:ital,wght@0,400;0,700;1,400;1,700&display=swap" rel="stylesheet">
<style>
:root {{
  --ink:#18301F; --leaf:#226340; --meadow:#57B25A; --sky:#9CD0F5; --sky-deep:#2F7FD6; --tulip:#E0567A; --tulip-deep:#A32545; --sun:#FFD166; --night:#0B1B2E;
  --text2:#2F4A3A; --text3:#47604F; --line:rgba(24,48,31,.12); --line2:rgba(24,48,31,.22);
  --sky-grad:linear-gradient(180deg,#6DB5EE 0%,#9CD0F5 35%,#CFE9FA 68%,#EEF7F4 100%);
  --night-grad:linear-gradient(180deg,#081425 0%,#0F2540 55%,#1D3F57 100%);
  --pane:linear-gradient(135deg,rgba(255,255,255,.74),rgba(255,255,255,.5));
  --edge:rgba(255,255,255,.88);
  --pane-shadow:0 24px 60px -18px rgba(20,60,45,.3),0 2px 8px rgba(20,60,45,.06),inset 0 1px 0 rgba(255,255,255,.95);
  --card-shadow:0 10px 26px -14px rgba(20,60,45,.28),inset 0 1px 0 rgba(255,255,255,.9);
  --btn-grad:linear-gradient(180deg,#2F7F55,#1C563A); --btn-shadow:0 10px 22px -10px rgba(20,80,50,.6),inset 0 1px 0 rgba(255,255,255,.35);
  --blur:24px;
  --meadow-day:url("{MEADOW_DAY}"); --meadow-night:url("{MEADOW_NIGHT}");
  --display:'Philosopher','Be Vietnam Pro',Georgia,serif; --body:'Be Vietnam Pro',system-ui,sans-serif; --serif:'Lora',Georgia,serif;
}}
*,*::before,*::after {{ box-sizing:border-box; margin:0; padding:0; }}
html {{ scroll-behavior:smooth; background:#9CD0F5; }}
body {{ font-family:var(--body); background:transparent; color:var(--ink); line-height:1.7; font-size:15px; -webkit-font-smoothing:antialiased; }}
/* Khung cảnh cố định: trời + thảm cỏ neo đáy */
body::before {{ content:''; position:fixed; z-index:-1; inset:0; pointer-events:none;
  background:var(--meadow-day) center bottom / auto clamp(220px,34vh,460px) repeat-x, var(--sky-grad); }}
a {{ color:var(--leaf); }}
.wrap {{ max-width:1040px; margin:0 auto; padding:0 28px; }}
.art {{ display:block; width:100%; height:auto; }}
.cimg {{ display:block; max-width:100%; height:auto; }}
.sprite {{ position:absolute; width:0; height:0; overflow:hidden; }}

/* cover: chữ nằm trực tiếp trên trời (đầu trang) */
.cover {{ position:relative; min-height:78vh; display:flex; align-items:center; justify-content:center; text-align:center; padding:70px 24px 40px; }}
.cover .c-lockup {{ width:min(400px,76vw); margin:0 auto; filter:drop-shadow(0 14px 24px rgba(30,90,140,.25)); }}
.cover-title {{ font-family:var(--display); font-weight:700; letter-spacing:.2em; text-transform:uppercase; font-size:13px; margin-top:30px; }}
.cover-sub {{ font-family:var(--serif); font-style:italic; color:var(--text2); margin-top:6px; }}
.cover-sys {{ display:inline-block; margin-top:14px; font-size:12px; font-weight:600; letter-spacing:.14em; text-transform:uppercase; padding:6px 16px; border-radius:99px; background:rgba(255,255,255,.5); border:1px solid var(--edge); color:var(--ink); }}

/* toc: thanh menu kính nổi */
.toc {{ position:sticky; top:10px; z-index:5; width:min(1100px,calc(100% - 28px)); margin:0 auto; border-radius:22px; background:rgba(255,255,255,.72);
  -webkit-backdrop-filter:blur(22px) saturate(1.4); backdrop-filter:blur(22px) saturate(1.4); border:1px solid var(--edge); box-shadow:0 14px 34px -18px rgba(20,60,90,.45),inset 0 1px 0 rgba(255,255,255,.7); }}
.toc .wrap {{ display:flex; gap:4px; overflow-x:auto; padding:8px 12px; max-width:none; scrollbar-width:none; }}
.toc a {{ text-decoration:none; font-size:12px; white-space:nowrap; padding:6px 12px; border-radius:99px; color:var(--text2); }}
.toc a:hover {{ background:rgba(34,99,64,.1); color:var(--ink); }}

/* mỗi mục = một tấm kính nổi */
main {{ padding:22px 0 0; }}
section {{ padding:0; border:0; }}
section .wrap, footer .wrap {{ background:var(--pane); -webkit-backdrop-filter:blur(var(--blur)) saturate(1.35); backdrop-filter:blur(var(--blur)) saturate(1.35);
  border:1px solid var(--edge); border-radius:34px; box-shadow:var(--pane-shadow);
  width:min(1100px,calc(100% - 28px)); max-width:none; margin:22px auto; padding:clamp(34px,5vw,60px) clamp(20px,4.4vw,48px); }}
.num {{ font-family:var(--display); color:var(--tulip-deep); font-size:15px; letter-spacing:.1em; }}
h2 {{ font-family:var(--display); font-weight:400; font-size:clamp(30px,4.4vw,46px); line-height:1.12; margin:6px 0 16px; }}
h2 em {{ font-style:italic; color:var(--tulip-deep); }}
h3 {{ font-family:var(--display); font-weight:700; font-size:20px; margin:44px 0 14px; }}
.lead {{ font-size:17px; color:var(--text2); max-width:62ch; }}
p + p {{ margin-top:10px; }}
.note {{ font-size:13px; color:var(--text3); margin-top:12px; }}
.note b {{ color:var(--tulip-deep); font-weight:600; }}
.grid {{ display:grid; gap:18px; }}
.g2 {{ grid-template-columns:repeat(2,1fr); }} .g3 {{ grid-template-columns:repeat(3,1fr); }} .g4 {{ grid-template-columns:repeat(4,1fr); }}
.grid > * {{ min-width:0; }}
@media (max-width:760px) {{ .g2 {{ grid-template-columns:1fr; }} .g3,.g4 {{ grid-template-columns:1fr 1fr; }} :root {{ --blur:16px; }}
  section .wrap, footer .wrap {{ width:calc(100% - 16px); margin:14px auto; border-radius:26px; padding:34px 16px 36px; }} .toc {{ width:calc(100% - 16px); border-radius:18px; }}
  .board {{ padding:28px 16px 40px; }} .board .art {{ max-width:100%; }} table {{ display:block; overflow-x:auto; }} }}
@media (max-width:480px) {{ .g3,.g4 {{ grid-template-columns:1fr; }} }}
/* thẻ nằm trong tấm: trắng 52%, viền trắng, KHÔNG làm mờ */
.card {{ background:rgba(255,255,255,.52); border:1px solid rgba(255,255,255,.85); border-radius:22px; padding:26px; box-shadow:var(--card-shadow); }}
.card h4 {{ font-family:var(--display); font-weight:700; font-size:17px; margin-bottom:6px; }}
.card p {{ font-size:14px; color:var(--text2); }}
.label {{ font-size:10px; font-weight:600; letter-spacing:.16em; text-transform:uppercase; color:var(--leaf); margin-bottom:10px; display:block; }}

/* bảng minh hoạ logo */
.board {{ border-radius:24px; display:flex; align-items:center; justify-content:center; padding:36px; min-height:230px; position:relative; border:1px solid rgba(255,255,255,.85); }}
.board .cap {{ position:absolute; left:16px; right:16px; bottom:12px; font-size:11px; line-height:1.4; color:var(--text3); }}
.b-glass {{ background:rgba(255,255,255,.52); box-shadow:var(--card-shadow); }}
.b-sky {{ background:var(--sky-grad); }}
.b-deep {{ background:rgba(16,56,42,.88); color:#F4FBF6; border-color:rgba(255,255,255,.3); }}
.b-night {{ background:var(--night-grad); color:#F1F6F2; border-color:rgba(255,255,255,.16); }}
.b-deep .cap, .b-night .cap {{ color:rgba(244,251,246,.88); }}
.clear {{ outline:1px dashed var(--tulip-deep); outline-offset:26px; }}
.dont {{ min-height:170px; padding:22px; overflow:hidden; }}
.dont::after {{ content:'✕'; position:absolute; right:12px; top:8px; color:var(--tulip-deep); font-weight:700; }}
.dont .art {{ width:120px; }}

/* màu */
.sw-chip {{ height:132px; border-radius:20px; display:flex; align-items:flex-end; padding:12px 14px; font-size:13px; font-weight:600; letter-spacing:.04em; }}
.sw-border {{ border:1px solid var(--edge); }}
.sw-name {{ font-family:var(--display); font-weight:700; font-size:17px; margin-top:10px; }}
.sw-name em {{ font-family:var(--body); font-style:normal; font-weight:400; font-size:12px; color:var(--text3); margin-left:4px; }}
.sw-meta {{ font-size:12px; color:var(--text3); margin-top:0; }}
.sw-role {{ font-size:13px; color:var(--text2); margin-top:4px; line-height:1.5; }}
.ratio {{ display:flex; height:46px; border-radius:16px; overflow:hidden; margin-top:8px; border:1px solid var(--edge); }}
.legend {{ list-style:none; display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:6px 18px; margin-top:12px; font-size:13px; color:var(--text2); }}
.legend i {{ display:inline-block; width:12px; height:12px; border-radius:4px; margin-right:8px; vertical-align:-1px; border:1px solid var(--line2); }}
table {{ width:100%; border-collapse:collapse; font-size:14px; margin-top:8px; }}
th {{ text-align:left; font-size:10px; letter-spacing:.14em; text-transform:uppercase; color:var(--text3); font-weight:600; padding:10px 12px; border-bottom:1px solid var(--line2); }}
td {{ padding:11px 12px; border-bottom:1px solid var(--line); vertical-align:top; }}
td code, p code, li code {{ font-family:ui-monospace,Menlo,monospace; font-size:12.5px; background:rgba(24,48,31,.08); padding:1px 6px; border-radius:6px; }}
.pass {{ color:var(--leaf); font-weight:600; }} .fail {{ color:var(--tulip-deep); font-weight:600; }}
.cchip {{ display:inline-block; width:34px; height:24px; line-height:24px; text-align:center; border-radius:8px; margin-right:10px; font:600 12px var(--body); border:1px solid var(--line2); vertical-align:middle; }}
.tints {{ display:grid; grid-template-columns:repeat(8,1fr); gap:8px; }}
.tints div {{ height:64px; border-radius:16px; font-size:10px; display:flex; align-items:flex-end; padding:7px; color:var(--ink); border:1px solid var(--edge); }}
@media (max-width:760px) {{ .tints {{ grid-template-columns:repeat(4,1fr); }} }}

/* chữ */
.spec {{ display:grid; grid-template-columns:150px 1fr; gap:20px; padding:22px 0; border-bottom:1px solid var(--line); align-items:baseline; }}
.spec small {{ font-size:11px; color:var(--text3); line-height:1.5; display:block; }}
@media (max-width:640px) {{ .spec {{ grid-template-columns:1fr; gap:6px; }} }}
.t-display {{ font-family:var(--display); font-weight:700; font-size:clamp(34px,5.4vw,62px); line-height:1.05; }}
.t-display em, .t-h2 em {{ font-style:italic; font-weight:400; color:var(--tulip-deep); }}
.t-h2 {{ font-family:var(--display); font-weight:400; font-size:34px; line-height:1.15; }}
.t-h3 {{ font-family:var(--display); font-weight:700; font-size:20px; }}
.t-eyebrow {{ font-family:var(--serif); font-style:italic; font-size:18px; color:var(--text2); }}
.t-body {{ font-size:16px; color:var(--text2); max-width:60ch; }}
.t-label {{ font-size:11px; font-weight:600; letter-spacing:.16em; text-transform:uppercase; color:var(--leaf); }}
.glyphs {{ font-family:var(--display); font-size:26px; line-height:1.5; word-break:break-word; }}

/* nền & hoa */
.scene {{ position:relative; height:190px; border-radius:24px; overflow:hidden; border:1px solid rgba(255,255,255,.7); }}
.scene.day {{ background:var(--sky-grad); }} .scene.night {{ background:var(--night-grad); }}
.scene::after {{ content:''; position:absolute; inset:0; background-position:center bottom; background-repeat:repeat-x; background-size:auto 46%; }}
.scene.day::after {{ background-image:var(--meadow-day); }} .scene.night::after {{ background-image:var(--meadow-night); }}

/* thành phần kính (ví dụ minh hoạ — dựng trong khung trời) */
.stage {{ position:relative; border-radius:28px; padding:26px; overflow:hidden; border:1px solid rgba(255,255,255,.7);
  background:radial-gradient(circle at 12% 70%,rgba(224,86,122,.55) 0 60px,transparent 62px),radial-gradient(circle at 88% 30%,rgba(87,178,90,.55) 0 90px,transparent 92px),var(--sky-grad); }}
.stage.night {{ background:radial-gradient(circle at 12% 70%,rgba(255,157,184,.4) 0 60px,transparent 62px),radial-gradient(circle at 88% 30%,rgba(159,221,176,.35) 0 90px,transparent 92px),var(--night-grad); }}
.row {{ display:flex; flex-wrap:wrap; gap:10px; align-items:center; }}
.d-pane {{ background:var(--pane); -webkit-backdrop-filter:blur(24px) saturate(1.35); backdrop-filter:blur(24px) saturate(1.35); border:1px solid var(--edge); border-radius:34px; box-shadow:var(--pane-shadow); padding:26px; }}
.d-card {{ background:rgba(255,255,255,.52); border:1px solid rgba(255,255,255,.85); border-radius:20px; box-shadow:var(--card-shadow); padding:16px; }}
.d-float {{ background:var(--pane); -webkit-backdrop-filter:blur(20px) saturate(1.35); backdrop-filter:blur(20px) saturate(1.35); border:1px solid var(--edge); border-radius:20px; box-shadow:var(--pane-shadow); padding:16px; }}
.d-nav {{ display:flex; align-items:center; justify-content:space-between; gap:10px; padding:10px 14px; border-radius:22px; background:rgba(255,255,255,.5); -webkit-backdrop-filter:blur(22px) saturate(1.4); backdrop-filter:blur(22px) saturate(1.4); border:1px solid var(--edge); box-shadow:0 14px 34px -18px rgba(20,60,90,.45),inset 0 1px 0 rgba(255,255,255,.7); font-size:13px; }}
.d-nav .orb {{ width:30px; flex:none; }}
.btn {{ font:500 14px var(--body); padding:12px 24px; border-radius:999px; border:1px solid rgba(255,255,255,.3); cursor:default; display:inline-block; }}
.btn-p {{ background:var(--btn-grad); color:#fff; box-shadow:var(--btn-shadow); }}
.btn-s {{ background:rgba(255,255,255,.5); color:var(--ink); border-color:var(--edge); -webkit-backdrop-filter:blur(12px); backdrop-filter:blur(12px); box-shadow:inset 0 1px 0 rgba(255,255,255,.5); }}
.pill {{ font-size:12px; padding:7px 16px; border-radius:99px; background:rgba(255,255,255,.5); border:1px solid var(--edge); color:var(--text2); -webkit-backdrop-filter:blur(10px); backdrop-filter:blur(10px); }}
.pill.on {{ background:var(--btn-grad); color:#fff; border-color:rgba(255,255,255,.3); box-shadow:var(--btn-shadow); }}
.badge {{ font-size:9px; font-weight:600; letter-spacing:.12em; text-transform:uppercase; padding:4px 10px; border-radius:99px; background:rgba(34,99,64,.1); color:var(--leaf); border:1px solid rgba(34,99,64,.3); }}
.input {{ font:400 14px var(--body); background:rgba(255,255,255,.66); border:1px solid var(--edge); border-radius:999px; padding:12px 20px; color:var(--text3); min-width:240px; box-shadow:inset 0 1px 3px rgba(20,60,45,.08); }}
.demo-card {{ background:rgba(255,255,255,.52); border:1px solid rgba(255,255,255,.85); border-radius:20px; box-shadow:var(--card-shadow); overflow:hidden; max-width:300px; }}
.demo-thumb {{ height:140px; background:linear-gradient(135deg,rgba(170,225,200,.8),rgba(255,255,255,.4)); display:flex; align-items:flex-start; padding:12px; }}
.demo-body {{ padding:16px; }}
.demo-foot {{ display:flex; justify-content:space-between; font-size:12px; color:var(--text3); border-top:1px solid var(--line); margin-top:12px; padding-top:12px; }}
.demo-foot b {{ color:var(--tulip-deep); font-weight:600; }}
.night .d-pane {{ background:linear-gradient(135deg,rgba(18,36,48,.64),rgba(10,24,32,.5)); border-color:rgba(255,255,255,.16); color:#F1F6F2; box-shadow:0 24px 60px -18px rgba(0,0,0,.6),inset 0 1px 0 rgba(255,255,255,.12); }}
.night .d-card {{ background:rgba(255,255,255,.07); border-color:rgba(255,255,255,.16); color:#D2DFD7; box-shadow:none; }}
.night .btn-p {{ background:linear-gradient(180deg,#F6FCF8,#D9EDE0); color:#12301F; }}
.night .btn-s {{ background:rgba(255,255,255,.1); color:#F1F6F2; border-color:rgba(255,255,255,.16); }}

/* giọng */
.vs td:first-child {{ font-weight:600; width:34%; }}
.eg {{ border-left:3px solid var(--leaf); padding:4px 0 4px 16px; margin-top:12px; font-size:14px; color:var(--text2); }}
.eg.bad {{ border-color:var(--tulip-deep); }}
.eg b {{ display:block; font-size:10px; letter-spacing:.14em; text-transform:uppercase; margin-bottom:3px; color:var(--leaf); }}
.eg.bad b {{ color:var(--tulip-deep); }}

/* mẫu bài đăng: trời + thảm cỏ, chữ nằm trong kính */
.post {{ aspect-ratio:1/1; border-radius:14px; position:relative; overflow:hidden; display:flex; flex-direction:column; padding:8% 8% 30%; background:var(--meadow-day) center bottom / auto 30% repeat-x, var(--sky-grad); border:1px solid rgba(255,255,255,.7); }}
.post.n {{ background:var(--meadow-night) center bottom / auto 30% repeat-x, var(--night-grad); }}
.pg {{ flex:1; display:flex; flex-direction:column; justify-content:center; padding:9%; border-radius:22px; background:var(--pane); -webkit-backdrop-filter:blur(16px) saturate(1.35); backdrop-filter:blur(16px) saturate(1.35); border:1px solid var(--edge); box-shadow:var(--pane-shadow); position:relative; }}
.n .pg {{ background:linear-gradient(135deg,rgba(18,36,48,.64),rgba(10,24,32,.5)); border-color:rgba(255,255,255,.16); color:#F1F6F2; box-shadow:0 24px 60px -18px rgba(0,0,0,.6),inset 0 1px 0 rgba(255,255,255,.12); text-align:center; align-items:center; }}
.post blockquote {{ font-family:var(--display); font-size:clamp(15px,2vw,23px); line-height:1.25; }}
.post blockquote em, .post .h em {{ color:var(--tulip-deep); font-style:italic; }}
.n .h em {{ color:#FF9DB8; }}
.post cite {{ font-family:var(--serif); font-size:12px; color:var(--text3); margin-top:12px; font-style:normal; }}
.post .orb {{ width:14%; position:absolute; right:7%; bottom:8%; }}
.post .k {{ font-size:10px; letter-spacing:.2em; text-transform:uppercase; color:#AEC1B6; }}
.post .h {{ font-family:var(--display); font-weight:700; font-size:clamp(17px,2.3vw,26px); line-height:1.15; margin:8px 0; }}
.post .nm {{ font-family:var(--display); color:var(--tulip-deep); font-size:15px; }}
.post .s {{ font-size:12px; color:var(--text2); margin-top:8px; }}
.post .f {{ width:46%; margin-top:14px; color:var(--ink); }}

ul.rules {{ list-style:none; }}
ul.rules li {{ padding:9px 0 9px 26px; position:relative; border-bottom:1px solid var(--line); font-size:14px; color:var(--text2); }}
ul.rules li::before {{ content:'—'; position:absolute; left:0; color:var(--leaf); }}
ul.rules.no li::before {{ content:'✕'; color:var(--tulip-deep); font-size:12px; top:11px; }}
footer {{ text-align:center; color:var(--text3); font-size:12px; }}
footer .wrap {{ padding-block:34px 28px; }}
footer .art {{ width:150px; margin:0 auto 10px; color:var(--ink); }}
/* dự phòng: không có backdrop-filter, hoặc người dùng bật giảm trong suốt */
@supports not ((backdrop-filter:blur(1px)) or (-webkit-backdrop-filter:blur(1px))) {{ :root {{ --pane:rgba(255,255,255,.92); }} .toc {{ background:rgba(255,255,255,.94); }} }}
@media (prefers-reduced-transparency:reduce) {{ :root {{ --pane:rgba(255,255,255,.95); }} .toc {{ background:#fff; }} }}
@media print {{ .toc {{ display:none; }} section .wrap {{ break-inside:avoid; }} }}
</style>
</head>
<body>
<svg class="sprite" aria-hidden="true">{''.join(symbols)}</svg>

<header class="cover">
  <div>
    {img('logo-lockup-color', '', 'Timeless Harmony — hold us together').replace('class="cimg"', 'class="cimg c-lockup"')}
    <p class="cover-title">Brand Guideline</p>
    <p class="cover-sub">Phiên bản 2.0 · tháng 11, 2026</p>
    <span class="cover-sys">Hệ nhận diện “Vườn kính”</span>
  </div>
</header>

<nav class="toc"><div class="wrap">
  <a href="#cot-loi">01 Cốt lõi</a><a href="#logo">02 Logo</a><a href="#mau">03 Màu sắc</a><a href="#chu">04 Kiểu chữ</a>
  <a href="#nen">05 Hình nền &amp; hoa</a><a href="#anh">06 Hình ảnh</a><a href="#giao-dien">07 Giao diện</a><a href="#giong">08 Giọng nói</a>
  <a href="#ung-dung">09 Ứng dụng</a><a href="#tep">10 Tệp &amp; việc còn mở</a>
</div></nav>

<main>
<section id="cot-loi"><div class="wrap">
  <span class="num">01</span>
  <h2>Cốt lõi <em>thương hiệu</em></h2>
  <p class="lead">Timeless Harmony là nền tảng kết nối dịch vụ cưới cho những đám cưới nhỏ, có chủ đích. Chúng mình tin rằng điều giữ hai người bên nhau không phải một ngày cưới hoành tráng, mà là những lựa chọn đúng — được làm cùng nhau.</p>
  <div class="grid g3" style="margin-top:34px">
    <div class="card"><span class="label">Lời hứa</span><h4>Đúng người, rõ ràng, an tâm</h4><p>Nhà cung cấp được tuyển chọn, hợp đồng rõ ràng, tiền được giữ an toàn qua ký quỹ.</p></div>
    <div class="card"><span class="label">Tagline</span><h4 style="font-family:var(--serif);font-weight:500;font-style:italic">hold us together</h4><p>Luôn viết thường, tiếng Anh, không chấm câu. Diễn giải tiếng Việt khi cần: “Giữ chúng mình bên nhau”.</p></div>
    <div class="card"><span class="label">Tính cách</span><h4>Người bạn thân trong ngành cưới</h4><p>Ấm áp · thẳng thắn · có căn cứ · tinh tế · đồng hành, không quyết định thay.</p></div>
  </div>
  <h3>Ý nghĩa biểu tượng</h3>
  <div class="grid g2">
    <div class="card"><h4>Quả cầu</h4><p>Khoảng trời và thảm cỏ của một ngày cưới ngoài trời — gradient từ trời xanh xuống cỏ.</p></div>
    <div class="card"><h4>Vô cực</h4><p>Tình yêu không có điểm kết — <i>timeless</i>.</p></div>
    <div class="card"><h4>Hai nụ tulip</h4><p>Hai người trên cùng một đường — <i>harmony</i>. Tulip là loài hoa của tình yêu trọn vẹn; trong bản màu, hai nụ là điểm hồng duy nhất.</p></div>
    <div class="card"><h4>Vòng tròn T · H</h4><p>Chiếc nhẫn và sự trọn vẹn; hai chữ cái đầu ở hai bên, mở ra chứ không khép kín. Chỉ còn trong các bản một màu.</p></div>
  </div>
  <p class="note"><b>Cần xác nhận:</b> đây là diễn giải đề xuất từ artwork gốc và hướng “Vườn kính”. Nếu ý nghĩa ban đầu của bạn khác, hãy sửa ở đây để mọi nội dung kể cùng một câu chuyện.</p>
</div></section>

<section id="logo"><div class="wrap">
  <span class="num">02</span>
  <h2>Logo</h2>
  <p class="lead">Trên màn hình, logo chính là <b>quả cầu màu</b>: trời xanh xuống thảm cỏ, dấu vô cực trắng, nụ tulip hồng. Khi cần in một màu, khắc hay dập nổi, dùng các bản nét một màu. Chọn theo cách hiển thị và kích thước; không tự vẽ lại hay sắp xếp lại các thành phần.</p>
  <h3>Bản màu — dùng trên màn hình</h3>
  <div class="grid g2">
    <div class="board b-sky">{img('logo-orb', 'width:150px', 'Quả cầu Timeless Harmony')}<span class="cap">Quả cầu — logo chính trên màn hình, ảnh đại diện, biểu tượng ứng dụng</span></div>
    <div class="board b-glass">{img('logo-lockup-color', 'width:230px', 'Bản đầy đủ màu')}<span class="cap">Bản đầy đủ màu (quả cầu + chữ + tagline) — ưu tiên dùng khi có chỗ</span></div>
    <div class="board b-glass">{img('logo-horizontal-color', 'width:min(360px,100%)', 'Bản ngang màu')}<span class="cap">Bản ngang màu — chữ ký email, tiêu đề tài liệu, bìa hồ sơ</span></div>
    <div class="board b-night">{img('logo-horizontal-color-light', 'width:min(360px,100%)', 'Bản ngang màu, chữ sáng')}<span class="cap">Bản ngang chữ sáng (<code>-light</code>) — trên nền tối hoặc ảnh</span></div>
  </div>
  <p class="note">Các SVG màu có gradient nên không nằm trong sprite một màu của site; nhúng bằng <code>&lt;img&gt;</code> hoặc <code>background-image</code>. Quả cầu: <code>assets/brand/logo-orb.svg</code>.</p>

  <h3>Cấu trúc biểu tượng</h3>
  <div class="grid g2">
    <div class="board b-glass" style="min-height:230px">{img('logo-infinity-color', 'width:min(300px,100%)', 'Dấu vô cực màu')}<span class="cap">Một nét liền, không cắt nhau — thân mực, hai đầu nở thành hai nụ tulip hồng. Đặt trên kính sáng.</span></div>
    <ul class="rules" style="margin:0">
      <li><b>Quả cầu</b> là gradient trời → cỏ, bóng sáng nhẹ ở góc trên trái. Dấu vô cực trắng nằm ở giữa; nụ tulip hồng ở hai đầu.</li>
      <li><b>Dấu vô cực</b> là một nét duy nhất: mảnh ở hai nụ, đầy dần về giữa. Hình đối xứng khi xoay 180°.</li>
      <li><b>Hai nụ tulip</b> giống hệt nhau, mỗi nụ có hai cánh ngoài và một cánh giữa ló ra phía sau.</li>
      <li><b>Bản một màu</b> giữ vòng tròn ngắt ở hai bên cho chữ <b>T</b> và <b>H</b>; nét đứng của T, H bằng độ dày vòng tròn.</li>
      <li><b>Chữ logo</b>: Belleza làm đậm nhẹ. <b>Tagline</b>: Lora 540. Cả hai đã chuyển thành đường nét, không cần cài phông.</li>
      <li>Tệp nguồn dựng logo: <code>docs/logo/build_logo.py</code>. Sửa thông số ở đầu tệp rồi chạy lại, không sửa SVG bằng tay.</li>
    </ul>
  </div>

  <h3>Dùng bản nào</h3>
  <div class="card"><table>
    <tr><th>Tình huống</th><th>Bản dùng</th></tr>
    <tr><td>Website, ứng dụng, mạng xã hội, ảnh đại diện</td><td>Quả cầu <code>logo-orb.svg</code></td></tr>
    <tr><td>Bìa, trang giới thiệu, ảnh chia sẻ</td><td>Bản đầy đủ màu <code>logo-lockup-color.svg</code></td></tr>
    <tr><td>Chữ ký email, đầu tài liệu, thanh ngang</td><td>Bản ngang màu <code>logo-horizontal-color.svg</code></td></tr>
    <tr><td>Nền tối, nền ảnh</td><td>Bản <code>-light</code> (chữ trắng): <code>logo-lockup-color-light.svg</code>, <code>logo-horizontal-color-light.svg</code></td></tr>
    <tr><td>Dấu vô cực đứng riêng, trang trí</td><td><code>logo-infinity-color.svg</code> trên kính sáng</td></tr>
    <tr><td>In một màu, khắc, dập nổi, hoặc nơi không in được gradient</td><td>Bản nét một màu: <code>logo-lockup</code>, <code>logo-horizontal</code>, <code>logo-mark</code>, <code>logo-mark-medium</code>, <code>logo-compact</code>, <code>logo-wordmark</code>, <code>logo-tagline</code>, <code>logo-infinity</code></td></tr>
  </table></div>

  <h3>Bản nét một màu</h3>
  <div class="grid g2">
    <div class="board b-glass">{art('logo-lockup','',"width:170px")}<span class="cap">Bản đầy đủ một màu — mực lá</span></div>
    <div class="board b-glass"><div style="width:min(300px,100%)">{art('logo-horizontal')}</div><span class="cap">Bản ngang một màu</span></div>
    <div class="board b-glass"><div style="width:270px;max-width:100%">{art('logo-wordmark')}{art('logo-tagline','',"width:52%;margin:8px auto 0")}</div><span class="cap">Logo chữ + tagline — chân trang, khi biểu tượng đã có ở chỗ khác</span></div>
    <div class="board b-glass"><div class="row" style="gap:22px;align-items:center;justify-content:center">{art('logo-mark','',"width:110px")}{art('logo-mark-medium','',"width:72px")}{art('logo-compact','',"width:32px")}</div><span class="cap">Biểu tượng theo cỡ — đầy đủ · nét vừa · thu nhỏ</span></div>
  </div>
  <p class="note">Nhỏ hơn 120px thì vòng tròn mảnh và chữ T, H bị mất: chuyển sang bản nét vừa. Nhỏ hơn 48px: dùng bản thu nhỏ. Riêng quả cầu màu dùng được từ 16px.</p>

  <h3>Trên nền nào</h3>
  <div class="grid g4">
    <div class="board b-sky" style="min-height:190px">{img('logo-orb','width:96px','Quả cầu')}<span class="cap">Trời ✓ · chữ mực</span></div>
    <div class="board b-glass" style="min-height:190px">{img('logo-orb','width:96px','Quả cầu')}<span class="cap">Kính sáng ✓ · chữ mực</span></div>
    <div class="board b-deep" style="min-height:190px">{img('logo-orb','width:96px','Quả cầu')}<span class="cap">Kính xanh đậm ✓ · chữ trắng</span></div>
    <div class="board b-night" style="min-height:190px">{img('logo-orb','width:96px','Quả cầu')}<span class="cap">Đêm vườn ✓ · chữ trắng</span></div>
  </div>
  <p class="note">Quả cầu dùng được trên <b>mọi nền</b>. Phần chữ: <b>mực lá</b> trên nền sáng; <b>trắng</b> (bản <code>-light</code>) trên nền tối hoặc ảnh. Bản một màu: mực lá trên nền sáng, trắng trên nền tối. Trên ảnh chụp: đặt logo trong một mảng kính hoặc màu đặc, không đặt trực tiếp lên ảnh.</p>

  <h3>Vùng an toàn &amp; kích thước tối thiểu</h3>
  <div class="grid g2">
    <div class="board b-glass" style="min-height:300px">{img('logo-lockup-color','width:170px','Bản đầy đủ màu').replace('class="cimg"','class="cimg clear"')}<span class="cap">Khoảng trống quanh logo ≥ bán kính quả cầu ÷ 2</span></div>
    <div class="card"><table>
      <tr><th>Phiên bản</th><th>Màn hình</th><th>In ấn</th></tr>
      <tr><td>Quả cầu màu</td><td>≥ 16 px</td><td>≥ 6 mm</td></tr>
      <tr><td>Bản đầy đủ màu (có chữ)</td><td>≥ 140 px rộng</td><td>≥ 30 mm</td></tr>
      <tr><td>Bản ngang màu</td><td>≥ 180 px rộng</td><td>≥ 40 mm</td></tr>
      <tr><td>Một màu: đầy đủ</td><td>≥ 150 px rộng</td><td>≥ 32 mm</td></tr>
      <tr><td>Một màu: ngang</td><td>≥ 200 px rộng</td><td>≥ 45 mm</td></tr>
      <tr><td>Logo chữ</td><td>≥ 100 px rộng</td><td>≥ 25 mm</td></tr>
      <tr><td>Biểu tượng đầy đủ</td><td>≥ 120 px</td><td>≥ 25 mm</td></tr>
      <tr><td>Biểu tượng nét vừa</td><td>48–120 px</td><td>12–25 mm</td></tr>
      <tr><td>Bản thu nhỏ</td><td>16–48 px</td><td>6–12 mm</td></tr>
    </table></div>
  </div>
  <div class="row" style="margin-top:16px;gap:18px;align-items:flex-end">{img('logo-orb','width:64px','')}{img('logo-orb','width:32px','')}{img('logo-orb','width:24px','')}{img('logo-orb','width:16px','')}<span class="note" style="margin:0">Quả cầu ở 64 · 32 · 24 · 16 px</span></div>

  <h3>Không làm</h3>
  <div class="grid g3">
    <div class="board b-glass dont">{art('logo-mark','',"transform:scaleX(1.5)")}<span class="cap">Kéo giãn, bóp méo</span></div>
    <div class="board b-glass dont">{img('logo-orb','width:100px;filter:hue-rotate(150deg)','')}<span class="cap">Đổi màu gradient của quả cầu</span></div>
    <div class="board b-glass dont">{img('logo-infinity-color','width:150px;filter:hue-rotate(110deg)','')}<span class="cap">Tô nụ tulip màu khác hồng</span></div>
    <div class="board b-glass dont">{art('logo-mark','',"color:#6A1B9A")}<span class="cap">Đổi bản một màu sang màu ngoài bảng màu</span></div>
    <div class="board dont" style="background:repeating-linear-gradient(45deg,#b9a98f 0 12px,#8a937c 12px 24px)">{art('logo-mark')}<span class="cap" style="color:#fff">Đặt trên nền rối, ảnh nhiều chi tiết</span></div>
    <div class="board b-glass dont">{img('logo-orb','width:100px;filter:drop-shadow(4px 5px 3px rgba(0,0,0,.45))','')}<span class="cap">Thêm bóng đổ, viền, hiệu ứng</span></div>
    <div class="board b-glass dont">{img('logo-orb','width:100px;transform:rotate(-18deg)','')}<span class="cap">Xoay, nghiêng</span></div>
    <div class="board b-glass dont">{art('logo-mark','',"width:34px")}<span class="cap">Dùng biểu tượng nét mảnh ở kích thước quá nhỏ</span></div>
  </div>
</div></section>

<section id="mau"><div class="wrap">
  <span class="num">03</span>
  <h2>Màu <em>sắc</em></h2>
  <p class="lead">Bảng màu lấy từ một ngày cưới ngoài trời: trời xanh, thảm cỏ, mực xanh lá cho chữ, và một chút hồng tulip. Nền là trời và cỏ; mọi nội dung nằm trong kính trắng.</p>
  <h3>Màu chính</h3>
  <div class="grid g4">
    {swatch('Ink','Mực lá','#18301F','Chữ, logo, nét vẽ.',dark=True)}
    {swatch('Leaf','Lá','#226340','Liên kết, icon, nút chính. Nút dùng gradient #2F7F55 → #1C563A.',dark=True,bg='linear-gradient(180deg,#2F7F55,#1C563A)',meta='RGB 34 · 99 · 64')}
    {swatch('Meadow','Cỏ non','#57B25A','Thảm cỏ, nhấn nhẹ. Không dùng cho chữ.')}
    {swatch('Sky','Trời','#9CD0F5','Nền trời, quầng sáng.')}
  </div>
  <h3>Màu bổ trợ</h3>
  <div class="grid g4">
    {swatch('Deep sky','Trời đậm','#2F7FD6','Đỉnh gradient quả cầu, nhấn lạnh.',dark=True)}
    {swatch('Tulip','Tulip hồng','#E0567A','Trang trí, nụ hoa. Không dùng cho chữ thường.',dark=True)}
    {swatch('Deep tulip','Tulip đậm','#A32545','Chữ nhấn trong tiêu đề, giá tiền.',dark=True)}
    {swatch('Sun','Nắng','#FFD166','Chi tiết rất nhỏ (mặt trời, tia sáng). Không dùng cho chữ.')}
  </div>
  <h3>Nền &amp; kính</h3>
  <div class="grid g3">
    {swatch('Night','Trời đêm','#0B1B2E','Chế độ tối “Đêm vườn”: gradient #081425 → #0F2540 → #1D3F57.',dark=True)}
    {swatch('Glass','Trắng kính','rgba(255,255,255,.5–.88)','Tấm .74 → .5 · thẻ .52 · ô nhập .66 · viền .88.',border=True,bg='linear-gradient(135deg,rgba(255,255,255,.88),rgba(255,255,255,.5)),var(--sky-grad)',meta='Trắng, trong suốt 50–88%')}
    {swatch('Sky gradient','Gradient trời','#6DB5EE → #EEF7F4','Nền trang chế độ sáng, cố định, phủ thảm cỏ ở đáy.',bg='var(--sky-grad)',meta='4 điểm: 0 · 35 · 68 · 100%')}
  </div>
  <h3>Tỷ lệ sử dụng</h3>
  <div class="ratio"><div style="flex:35;background:var(--sky-grad)"></div><div style="flex:30;background:rgba(255,255,255,.8)"></div><div style="flex:20;background:var(--ink)"></div><div style="flex:10;background:var(--btn-grad)"></div><div style="flex:5;background:var(--tulip)"></div></div>
  <ul class="legend"><li><i style="background:#9CD0F5"></i>Nền trời &amp; cỏ (hình nền) · 35%</li><li><i style="background:#fff"></i>Kính trắng · 30%</li><li><i style="background:#18301F"></i>Mực · 20%</li><li><i style="background:#226340"></i>Xanh lá cho hành động · 10%</li><li><i style="background:#E0567A"></i>Hồng tulip · ≤ 5%</li></ul>
  <p class="note">Mỗi màn hình hoặc mỗi bài đăng chỉ nên có <b>một</b> chỗ dùng hồng tulip.</p>

  <h3>Độ tương phản (WCAG 2.1)</h3>
  <p style="color:var(--text2);font-size:14px;max-width:70ch">Tính bằng công thức WCAG, không ước lượng. “Kính xấu nhất” là <code>#BCE0BD</code>: kính trắng 60% phủ lên cỏ. Chữ thường cần ≥ 4,5:1 (AA); ≥ 7:1 là AAA; chữ lớn (từ 24px, hoặc 19px đậm) cần ≥ 3:1.</p>
  <table><tr><th>Cặp màu</th><th>Tỷ lệ</th><th>Mức</th><th>Dùng cho</th></tr>
  {CONTRAST_HTML}
  </table>

  <h3>Màu theo hạng mục dịch vụ</h3>
  <p style="color:var(--text2);font-size:14px;max-width:70ch">Dùng làm nền giữ chỗ khi chưa có ảnh và để phân biệt hạng mục. Là các gradient kính nhạt trong <code>theme.css</code>, đủ nhẹ để không cạnh tranh với màu chính.</p>
  <div class="tints" style="margin-top:14px">
    <div style="background:linear-gradient(135deg,rgba(255,222,150,.75),rgba(255,255,255,.4))">Kế hoạch</div><div style="background:linear-gradient(135deg,rgba(170,225,200,.8),rgba(255,255,255,.4))">Nhiếp ảnh</div><div style="background:linear-gradient(135deg,rgba(255,186,205,.8),rgba(255,255,255,.4))">Hoa</div><div style="background:linear-gradient(135deg,rgba(245,190,225,.75),rgba(255,255,255,.4))">Làm đẹp</div>
    <div style="background:linear-gradient(135deg,rgba(196,190,250,.8),rgba(255,255,255,.4))">Âm nhạc</div><div style="background:linear-gradient(135deg,rgba(255,205,150,.75),rgba(255,255,255,.4))">Ẩm thực</div><div style="background:linear-gradient(135deg,rgba(160,208,250,.8),rgba(255,255,255,.4))">Địa điểm</div><div style="background:linear-gradient(135deg,rgba(255,180,150,.75),rgba(255,255,255,.4))">Độc đáo</div>
  </div>
</div></section>

<section id="chu"><div class="wrap">
  <span class="num">04</span>
  <h2>Kiểu <em>chữ</em></h2>
  <p class="lead">Ba phông, ba vai trò. Cả ba đều miễn phí trên Google Fonts và hiển thị đầy đủ dấu tiếng Việt.</p>
  <div class="grid g3" style="margin-top:30px">
    <div class="card"><span class="label">Tiêu đề</span><p style="font-family:var(--display);font-size:40px;line-height:1.1;color:var(--ink)">Philosopher</p><p style="margin-top:8px">Phông của artwork gốc. Dùng 700 cho tiêu đề lớn, 400 cho tiêu đề phụ, <i>nghiêng</i> cho chữ nhấn.</p></div>
    <div class="card"><span class="label">Giao diện &amp; đoạn văn</span><p style="font-family:var(--body);font-size:34px;font-weight:500;line-height:1.1;color:var(--ink)">Be Vietnam Pro</p><p style="margin-top:8px">Thiết kế riêng cho tiếng Việt. 400 cho văn bản, 500–600 cho nút và nhãn.</p></div>
    <div class="card"><span class="label">Tagline &amp; trích dẫn</span><p style="font-family:var(--serif);font-size:40px;font-style:italic;line-height:1.1;color:var(--ink)">Lora</p><p style="margin-top:8px">Dùng nghiêng cho tagline, lời dẫn, trích dẫn. Không dùng cho tiêu đề chính.</p></div>
  </div>
  <p class="note">Chữ trong logo dùng Belleza (logo chữ) và Lora 540 (tagline), đã chuyển thành hình vẽ. Không dùng Belleza cho chữ trên website hay ấn phẩm: phông này không có dấu tiếng Việt.</p>
  <h3>Thang chữ</h3>
  <div class="spec"><div><span class="t-label">Tiêu đề lớn</span><small>Philosopher 700 · 38–66px · 1.05</small></div><p class="t-display">Đám cưới của bạn<br><em>bắt đầu từ đây</em></p></div>
  <div class="spec"><div><span class="t-label">Tiêu đề mục</span><small>Philosopher 400 · 26–38px · 1.15</small></div><p class="t-h2">Được xây dựng trên <em>sự tin tưởng</em></p></div>
  <div class="spec"><div><span class="t-label">Tiêu đề nhỏ</span><small>Philosopher 700 · 17–22px</small></div><p class="t-h3">Ký quỹ thanh toán an toàn</p></div>
  <div class="spec"><div><span class="t-label">Lời dẫn</span><small>Lora nghiêng · 16–18px</small></div><p class="t-eyebrow">hold us together</p></div>
  <div class="spec"><div><span class="t-label">Đoạn văn</span><small>Be Vietnam Pro 400 · 14–16px · 1.7</small></div><p class="t-body">Tìm đúng nhà cung cấp cho ngày trọng đại — được tuyển chọn kỹ, thanh toán an toàn qua ký quỹ.</p></div>
  <div class="spec"><div><span class="t-label">Nhãn</span><small>Be Vietnam Pro 600 · 10–11px · chữ hoa · giãn 0.16em</small></div><p class="t-label">Nhà cung cấp nổi bật</p></div>
  <h3>Quy tắc</h3>
  <ul class="rules">
    <li>Chữ nhấn trong tiêu đề: đặt trong thẻ <code>&lt;em&gt;</code> — tự động thành Philosopher nghiêng, màu Tulip đậm <code>#A32545</code>. Mỗi tiêu đề chỉ nhấn một cụm.</li>
    <li>Không viết HOA toàn bộ tiêu đề tiếng Việt (dấu chồng lên nhau, khó đọc). Chữ hoa chỉ dùng cho nhãn ngắn.</li>
    <li>Chiều dài dòng văn bản: 55–70 ký tự. Căn trái; không căn đều hai bên.</li>
    <li>Chữ trong logo “TIMELESS HARMONY” là hình vẽ, không gõ lại bằng phông.</li>
  </ul>
  <h3>Kiểm tra dấu tiếng Việt</h3>
  <p class="glyphs">Ầ Ẩ Ẫ Ậ Ắ Ằ Ẳ Ẵ Ặ Đ Ễ Ệ Ỗ Ộ Ờ Ở Ỡ Ợ Ữ Ự ỳ ỷ ỹ ỵ<br><span style="font-style:italic">Giữ chúng mình bên nhau — những điều nhỏ, thật lòng</span></p>
</div></section>

<section id="nen"><div class="wrap">
  <span class="num">05</span>
  <h2>Hình nền <em>&amp; hoa</em></h2>
  <p class="lead">Mỗi trang là một khoảng trời với thảm cỏ hoa ở đáy. Hình nền vẽ bằng vector, không dùng ảnh ngoài: <code>docs/design/build_background.py</code> xuất ra <code>assets/bg/</code>.</p>
  <div class="grid g2" style="margin-top:30px">
    <div><div class="scene day"></div><p class="note"><code>meadow-day.svg</code> · chế độ sáng — dải đồi, cỏ và hoa, lặp ngang liền mạch (2400×460)</p></div>
    <div><div class="scene night"></div><p class="note"><code>meadow-night.svg</code> · chế độ tối “Đêm vườn”</p></div>
  </div>
  <div class="card" style="margin-top:22px"><table>
    <tr><th>Tệp</th><th>Vai trò</th></tr>
    <tr><td><code>assets/bg/meadow-day.svg</code> · <code>meadow-night.svg</code></td><td>Thảm cỏ neo đáy màn hình, lặp ngang</td></tr>
    <tr><td><code>assets/bg/sky-day.svg</code> · <code>sky-night.svg</code></td><td>Mây và nắng / sao và trăng, nền trong suốt; đặt trên gradient trời trong <code>theme.css</code></td></tr>
  </table></div>
  <div class="grid g2" style="margin-top:26px">
    <div><h3 style="margin-top:0">Nên</h3><ul class="rules">
      <li>Nền luôn <b>cố định</b> (<code>position: fixed</code>): nội dung cuộn, khung cảnh đứng yên.</li>
      <li>Cỏ chiếm khoảng <b>1/3 phía dưới</b> màn hình (<code>clamp(220px, 34vh, 460px)</code>).</li>
      <li>Mọi chữ nằm trong kính. Riêng đầu trang, chữ được phép nằm thẳng trên trời.</li>
      <li>Chế độ sáng và tối dùng cặp ảnh tương ứng; không trộn ngày với đêm.</li>
    </ul></div>
    <div><h3 style="margin-top:0">Không</h3><ul class="rules no">
      <li>Đặt chữ trực tiếp lên cỏ — hoa và bóng đồi làm chữ khó đọc.</li>
      <li>Cuộn cỏ theo nội dung, hoặc kéo giãn cỏ phủ cả màn hình.</li>
      <li>Thay bằng ảnh chụp, ảnh stock hay nền đặc.</li>
      <li>Vẽ thêm hoa lạ vào thảm cỏ ngoài bản dựng từ script.</li>
    </ul></div>
  </div>

  <h3>Tulip nét mảnh</h3>
  <p class="lead" style="font-size:15px">Bốn cụm tulip nét mảnh (<code>assets/brand/tulip-*.svg</code>) là hình vẽ của thời artwork gốc. Chúng chỉ còn dùng trên <b>kính xanh đậm</b> (khối kêu gọi hành động) và trên ấn phẩm in. Một màu, trắng ngà trên nền xanh đậm.</p>
  <div class="grid g4" style="margin-top:22px;align-items:end">
    <div class="board b-deep">{art('tulip-top-left','',"width:110px;color:#F4FBF6")}<span class="cap">Góc trên trái</span></div>
    <div class="board b-deep">{art('tulip-right','',"width:110px;color:#F4FBF6")}<span class="cap">Cạnh phải</span></div>
    <div class="board b-deep">{art('tulip-bottom','',"width:140px;color:#F4FBF6")}<span class="cap">Cạnh dưới</span></div>
    <div class="board b-deep">{art('tulip-bottom-left','',"width:120px;color:#F4FBF6")}<span class="cap">Góc dưới trái</span></div>
  </div>
  <div class="grid g2" style="margin-top:22px">
    <ul class="rules">
      <li>Đặt sát mép khối kính xanh đậm, như đang mọc vào từ ngoài khung.</li>
      <li>Tối đa ba cụm trong một bố cục; để lại khoảng trống ở giữa.</li>
    </ul>
    <ul class="rules no">
      <li>Đặt trên kính sáng, trên trời hoặc trên cỏ.</li>
      <li>Tô màu bên trong cánh hoa, dùng chuyển sắc; lật, xoay ngược thân hoa.</li>
    </ul>
  </div>
</div></section>

<section id="anh"><div class="wrap">
  <span class="num">06</span>
  <h2>Hình <em>ảnh</em></h2>
  <p class="lead">Ảnh phải giống như được chụp bởi một người bạn có mắt nhìn — không phải ảnh quảng cáo.</p>
  <div class="grid g2" style="margin-top:26px">
    <div><h3 style="margin-top:0">Hướng tới</h3><ul class="rules">
      <li>Ánh sáng tự nhiên; tông ấm, sáng; hợp với nền trời và kính.</li>
      <li>Khoảnh khắc thật: bàn tay, ánh nhìn, bàn tiệc nhỏ, hậu trường.</li>
      <li>Đám cưới nhỏ: 20–80 khách, vườn, nhà, rừng thông, bãi biển.</li>
      <li>Chi tiết nghề của nhà cung cấp: cắm hoa, chỉnh máy, viết thiệp.</li>
      <li>Có khoảng trống trong khung hình để đặt chữ.</li>
    </ul></div>
    <div><h3 style="margin-top:0">Tránh</h3><ul class="rules no">
      <li>Ảnh mẫu có sẵn (stock), ảnh lấy trên mạng không xin phép.</li>
      <li>Màu rực, chỉnh sửa nặng, hiệu ứng lóa, da “nhựa”.</li>
      <li>Sảnh tiệc lớn, sân khấu hoành tráng, đèn LED.</li>
      <li>Chữ nổi, khung viền, logo chèn đè lên ảnh.</li>
      <li>Ảnh AI tạo ra giả làm đám cưới thật.</li>
    </ul></div>
  </div>
  <p class="note"><b>Hiện trạng:</b> website chưa có ảnh thật — đang dùng nền màu theo hạng mục, và trang Cẩm nang dùng ảnh ngẫu nhiên tạm thời. Luôn có văn bản đồng ý của cặp đôi và nhà cung cấp trước khi dùng ảnh của họ.</p>
</div></section>

<section id="giao-dien"><div class="wrap">
  <span class="num">07</span>
  <h2>Thành phần <em>giao diện</em></h2>
  <p class="lead">Mọi thứ là kính: nhẹ, trong, viền trắng mảnh, bóng đổ mềm màu xanh lá. Chiều sâu đến từ ba cấp kính. Nguồn: <code>theme.css</code> mục 7.</p>

  <h3>Ba cấp kính</h3>
  <div class="stage">
    <div class="d-pane">
      <span class="label">Tấm</span>
      <p style="font-size:14px;color:var(--text2);max-width:60ch">Khối nội dung lớn của một mục. Tự làm mờ nền: <code>backdrop-filter: blur(24px) saturate(1.35)</code>, bo 34px, viền trắng .88.</p>
      <div class="grid g2" style="margin-top:16px">
        <div class="d-card"><span class="label" style="margin-bottom:4px">Thẻ trong tấm</span><p style="font-size:13px;color:var(--text2)">Trắng 52%, viền trắng, bo 20px. <b>Không</b> làm mờ — đã nằm trên kính.</p></div>
        <div class="d-card"><span class="label" style="margin-bottom:4px">Thẻ trong tấm</span><p style="font-size:13px;color:var(--text2)">Bóng nhẹ <code>--card-shadow</code>. Khi rê chuột: nhấc lên 4px.</p></div>
      </div>
    </div>
    <div class="d-float" style="margin-top:18px;max-width:420px"><span class="label" style="margin-bottom:4px">Thẻ nổi</span><p style="font-size:13px;color:var(--text2)">Đứng riêng trên nền (hộp lập kế hoạch, cửa sổ, bong bóng chat), nên tự làm mờ 20px.</p></div>
  </div>
  <p class="note">Ví dụ dựng trong một khung trời minh hoạ để thấy hiệu ứng mờ. Class dùng lại: <code>.glass</code> (tấm) và <code>.glass-strong</code> (tấm đặc hơn, cho nội dung dài như bài viết).</p>

  <h3>Thanh menu</h3>
  <div class="stage"><div class="d-nav"><span class="row" style="gap:8px;flex-wrap:nowrap">{img('logo-orb','width:30px','')}<b style="font-family:var(--display);letter-spacing:.14em;font-size:12px">TIMELESS HARMONY</b></span><span class="row" style="gap:8px;flex-wrap:nowrap"><span class="btn btn-p" style="padding:8px 16px;font-size:12px">Bắt đầu</span></span></div>
  <p class="note" style="color:var(--ink)">Thanh kính nổi: blur 22px, bo 22px, cách mép 10px. Điện thoại: bo 18px, chỉ giữ quả cầu.</p></div>

  <h3>Nút</h3>
  <div class="stage"><div class="row"><span class="btn btn-p">Khám phá nhà cung cấp</span><span class="btn btn-s">Lên kế hoạch cùng Harmony AI</span></div></div>
  <p class="note">Nút chính = <b>viên kính xanh lá</b> (gradient <code>#2F7F55 → #1C563A</code>, chữ trắng, viền trắng 30%). Nút phụ = <b>kính trong</b> (trắng 50%, viền trắng). Mỗi màn hình một nút chính. Nút bo tròn hoàn toàn; chữ 13–14px, đậm 500. Động từ đứng đầu: “Khám phá…”, “Gửi…”, “Lưu…”.</p>

  <h3>Bộ lọc, nhãn, ô nhập</h3>
  <div class="stage"><div class="row"><span class="pill on">Tất cả</span><span class="pill">Nhiếp ảnh &amp; Quay phim</span><span class="pill">Hoa cưới</span><span class="badge">Mới</span><span class="badge">✦ Độc đáo</span><span class="input">Tìm nhiếp ảnh gia, hoa cưới…</span></div></div>
  <p class="note">Nhãn lọc = <b>viên kính nhỏ</b> (trắng 50%, blur 10px); nhãn đang chọn dùng gradient xanh lá. Ô nhập = <b>kính trắng 66%</b>, viền trắng, bóng trong nhẹ.</p>

  <h3>Thẻ nhà cung cấp</h3>
  <div class="grid g2" style="align-items:start">
    <div class="stage" style="padding:18px"><div class="demo-card"><div class="demo-thumb"><span class="badge">Mới</span></div><div class="demo-body"><span class="t-label" style="font-size:10px">Nhiếp ảnh &amp; Quay phim</span><p style="font-weight:500;font-size:15px;margin-top:4px">Ánh Dương Studio</p><p style="font-size:12px;color:var(--text3);margin:0">Sài Gòn</p><div class="demo-foot"><span>Film Analog · Vintage</span><b>Từ 6 triệu</b></div></div></div></div>
    <table>
      <tr><th>Thuộc tính</th><th>Giá trị</th></tr>
      <tr><td>Bo góc</td><td>Tấm 34px (điện thoại 26px) · thẻ nổi 20–30px · thẻ 20px · menu 22px · nút, nhãn, ô tìm kiếm tròn hoàn toàn</td></tr>
      <tr><td>Viền</td><td>1px trắng .88 (tấm, thẻ nổi) · trắng .85 (thẻ)</td></tr>
      <tr><td>Bóng đổ</td><td>Mềm, ngả xanh lá: <code>--pane-shadow</code>, <code>--card-shadow</code></td></tr>
      <tr><td>Khoảng cách</td><td>Bội số của 4: 8 · 12 · 16 · 24 · 32 · 48 · 72; giữa các tấm 22px</td></tr>
      <tr><td>Chuyển động</td><td>Nhẹ, 0,2–0,6 giây; tắt khi người dùng bật “giảm chuyển động”</td></tr>
      <tr><td>Chế độ tối</td><td>“Đêm vườn”: trời <code>#0B1B2E</code>, tấm kính tối, chữ <code>#F1F6F2</code>, nhấn <code>#9FDDB0</code>, tulip <code>#FF9DB8</code>; nút chính thành kính sáng</td></tr>
    </table>
  </div>
  <h3>Đêm vườn</h3>
  <div class="stage night"><div class="d-pane"><span class="label" style="color:#9FDDB0">Chế độ tối</span><p style="font-size:14px;color:#D2DFD7;max-width:56ch;margin-bottom:14px">Cùng ba cấp kính, đổi sang kính tối trên trời đêm.</p><div class="row"><span class="btn btn-p">Khám phá</span><span class="btn btn-s">Tìm hiểu thêm</span></div></div></div>

  <h3>Quy tắc</h3>
  <ul class="rules">
    <li><b>Không lồng hai lớp làm mờ.</b> Thẻ nằm trong tấm chỉ dùng nền trắng 52%, không <code>backdrop-filter</code>.</li>
    <li><b>Điện thoại</b> (≤ 640px): giảm blur còn 16px (<code>--blur</code>), tấm bo 26px, lề hai bên 8px.</li>
    <li><b>Dự phòng:</b> trình duyệt không hỗ trợ <code>backdrop-filter</code> (<code>@supports not</code>), hoặc người dùng bật giảm trong suốt (<code>prefers-reduced-transparency</code>): tấm chuyển sang trắng đặc 90–95%.</li>
    <li><b>Chữ thường</b> trên kính phải đạt tương phản tối thiểu 4,5:1 — xem bảng ở mục 03. Chữ nhấn Tulip đậm trên kính xấu nhất chỉ dùng cỡ lớn.</li>
    <li>Không đặt chữ trực tiếp lên thảm cỏ; mọi chữ nằm trong kính.</li>
  </ul>
</div></section>

<section id="giong"><div class="wrap">
  <span class="num">08</span>
  <h2>Giọng <em>nói</em></h2>
  <p class="lead">Viết như một người bạn thân từng tổ chức nhiều đám cưới. Bản đầy đủ: <code>.claude/brand-voice-guidelines.md</code>.</p>
  <table class="vs" style="margin-top:22px">
    <tr><th>Chúng mình là</th><th>Chúng mình không là</th></tr>
    <tr><td>Ấm áp</td><td>Sến súa, ủy mị</td></tr>
    <tr><td>Thẳng thắn, minh bạch</td><td>Phũ phàng, dạy đời</td></tr>
    <tr><td>Có căn cứ</td><td>Hàn lâm, bịa số liệu</td></tr>
    <tr><td>Tinh tế, có chủ đích</td><td>Xa hoa, phô trương</td></tr>
    <tr><td>Đáng tin — hứa ít, làm đủ</td><td>“Số 1”, “cam kết 100%”</td></tr>
    <tr><td>Đồng hành</td><td>Quyết định thay, ép chốt</td></tr>
  </table>
  <div class="grid g2" style="margin-top:22px">
    <div class="eg"><b>Nên</b>Mất cọc là nỗi sợ số một khi đặt dịch vụ cưới qua mạng. Ký quỹ giải quyết đúng chỗ đó: tiền của bạn được giữ ở giữa, chỉ chuyển đi khi bạn xác nhận dịch vụ đã xong.</div>
    <div class="eg bad"><b>Không</b>🔥 SIÊU HOT!!! Nền tảng cưới SỐ 1 Việt Nam, cam kết 100% uy tín, giá rẻ nhất thị trường!!! Nhanh tay inbox ngay nàng ơi 💍</div>
  </div>
  <ul class="rules" style="margin-top:22px">
    <li>Xưng “mình / chúng mình”, gọi “bạn”. Văn bản pháp lý: “Timeless Harmony”, “chúng tôi”.</li>
    <li>Viết “nhà cung cấp”, không viết “supplier”. Viết “ký quỹ” và giải thích ở lần đầu.</li>
    <li>Không dùng đánh giá hay số liệu chưa có thật.</li>
  </ul>
</div></section>

<section id="ung-dung"><div class="wrap">
  <span class="num">09</span>
  <h2>Ứng <em>dụng</em></h2>
  <p class="lead">Ba mẫu bài đăng vuông cho Instagram: kính nổi trên nền trời và thảm cỏ. Giữ đúng bố cục; chỉ thay chữ. Chữ luôn nằm trong kính, không đặt lên cỏ.</p>
  <div class="grid g3" style="margin-top:28px">
    <div><div class="post"><div class="pg"><blockquote>Đám cưới nhỏ không phải xu hướng — đó là <em>lựa chọn có chủ đích.</em></blockquote><cite>hold us together</cite>{img('logo-orb','','').replace('class="cimg"','class="cimg orb"')}</div></div><p class="note">Trích dẫn · nền ngày</p></div>
    <div><div class="post n"><div class="pg">{img('logo-orb','width:26%;margin-bottom:12px','')}<p class="k">Sắp ra mắt</p><p class="h">Đặt dịch vụ cưới,<br><em>không sợ mất cọc</em></p></div></div><p class="note">Thông báo · nền Đêm vườn</p></div>
    <div><div class="post"><div class="pg" style="justify-content:flex-start"><p class="nm">01 / 05</p><p class="h">Ký quỹ là gì?<br>30 giây để hiểu</p><p class="s">Vuốt để xem tiền của bạn đi đâu →</p>{art('logo-wordmark','f')}</div></div><p class="note">Bìa chuỗi mẹo · nền ngày</p></div>
  </div>
  <h3>Ảnh đại diện &amp; ảnh chia sẻ</h3>
  <ul class="rules">
    <li>Ảnh đại diện mạng xã hội: quả cầu — <code>docs/logo/social/avatar-orb.png</code>, 1080×1080, tràn khung, tự cắt tròn.</li>
    <li>Ảnh xem trước khi chia sẻ link (1200×630): <code>og-image.png</code>.</li>
    <li>Chữ ký email: bản ngang màu <code>docs/logo/png/logo-horizontal-color.png</code>, hiển thị rộng 200px; chữ Be Vietnam Pro 13px màu Mực lá.</li>
  </ul>
</div></section>

<section id="tep"><div class="wrap">
  <span class="num">10</span>
  <h2>Tệp &amp; <em>việc còn mở</em></h2>
  <h3 style="margin-top:20px">Tệp thương hiệu trong repo</h3>
  <table>
    <tr><th>Tệp</th><th>Dùng cho</th></tr>
    <tr><td><code>assets/brand/logo-orb.svg</code></td><td>Quả cầu màu — logo chính trên màn hình</td></tr>
    <tr><td><code>assets/brand/logo-lockup-color.svg</code> · <code>logo-lockup-color-light.svg</code></td><td>Bản đầy đủ màu: quả cầu + chữ + tagline; bản chữ sáng cho nền tối</td></tr>
    <tr><td><code>assets/brand/logo-horizontal-color.svg</code> · <code>logo-horizontal-color-light.svg</code></td><td>Bản ngang màu; bản chữ sáng cho nền tối</td></tr>
    <tr><td><code>assets/brand/logo-infinity-color.svg</code></td><td>Dấu vô cực màu (thân mực, nụ hồng), đặt trên kính sáng</td></tr>
    <tr><td><code>assets/brand/logo-lockup.svg</code> · <code>logo-horizontal.svg</code></td><td>Bản đầy đủ và bản ngang một màu</td></tr>
    <tr><td><code>assets/brand/logo-mark.svg</code> · <code>logo-mark-medium.svg</code> · <code>logo-compact.svg</code></td><td>Biểu tượng nét một màu: đầy đủ · nét vừa · thu nhỏ dưới 48px</td></tr>
    <tr><td><code>assets/brand/logo-wordmark.svg</code> · <code>logo-tagline.svg</code> · <code>logo-infinity.svg</code></td><td>Chữ “TIMELESS HARMONY” · “hold us together” · riêng dấu vô cực (một màu)</td></tr>
    <tr><td><code>favicon.svg</code> · <code>apple-touch-icon.png</code></td><td>Biểu tượng trình duyệt và iPhone</td></tr>
    <tr><td><code>assets/bg/meadow-day.svg</code> · <code>meadow-night.svg</code></td><td>Thảm cỏ lặp ngang, ngày và đêm</td></tr>
    <tr><td><code>assets/bg/sky-day.svg</code> · <code>sky-night.svg</code></td><td>Mây, nắng / sao, trăng trên nền trời</td></tr>
    <tr><td><code>docs/design/build_background.py</code></td><td>Dựng lại bốn tệp hình nền trong <code>assets/bg/</code></td></tr>
    <tr><td><code>docs/logo/svg/</code> · <code>png/</code> · <code>pdf/</code> · <code>social/</code></td><td>Bộ tệp gửi đối tác, nhà in: bản màu, bản một màu cố định (Rừng và Ngà), PNG nền trong, PDF vector, ảnh đại diện</td></tr>
    <tr><td><code>assets/brand/tulip-*.svg</code></td><td>Bốn cụm tulip nét mảnh (kính xanh đậm, ấn phẩm in)</td></tr>
    <tr><td><code>og-image.png</code></td><td>Ảnh chia sẻ link, 1200×630</td></tr>
    <tr><td><code>theme.css</code></td><td>Màu, phông và chất liệu kính cho website — nguồn duy nhất</td></tr>
    <tr><td><code>.claude/brand-voice-guidelines.md</code></td><td>Giọng thương hiệu đầy đủ</td></tr>
    <tr><td><code>docs/marketing-playbook.md</code></td><td>Chiến lược và kế hoạch marketing</td></tr>
  </table>
  <p class="note">Các SVG một màu dùng <code>currentColor</code> — tự đổi theo màu chữ nơi đặt nó. Các SVG màu có gradient cố định, không đổi theo chữ.</p>
  <h3>Việc còn mở</h3>
  <ul class="rules">
    <li><b style="color:var(--tulip-deep)">Xác nhận hướng “Vườn kính”</b> và <b style="color:var(--tulip-deep)">logo quả cầu</b> — màu, gradient, bản chữ sáng.</li>
    <li><b style="color:var(--tulip-deep)">Ảnh thật</b> của nhà cung cấp và cặp đôi để thay nền màu giữ chỗ.</li>
    <li><b style="color:var(--tulip-deep)">Ý nghĩa biểu tượng</b> ở mục 01 (kể cả “quả cầu = trời và cỏ”) cần bạn xác nhận.</li>
    <li><b style="color:var(--tulip-deep)">In khổ lớn:</b> nếu cần, vẽ lại bốn cụm tulip nét mảnh như đã làm với logo.</li>
  </ul>
</div></section>
</main>

<footer><div class="wrap">{art('logo-wordmark')}<p>hold us together · Brand Guideline 2.0 · Vườn kính</p></div></footer>
</body>
</html>
'''
open(ROOT + '/docs/brand-guidelines.html', 'w').write(html)
print(len(html) // 1024, 'KB')
