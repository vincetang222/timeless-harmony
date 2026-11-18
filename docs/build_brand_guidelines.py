"""Dựng docs/brand-guidelines.html (tự chứa: SVG nhúng sẵn, logo màu và ảnh cảnh nền dạng data URI).
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
    mime = 'image/webp' if path.endswith('.webp') else 'image/svg+xml'
    return f'data:{mime};base64,' + base64.b64encode(open(path, 'rb').read()).decode()
URI = {n: b64(A + n + '.svg') for n in ['logo-orb', 'logo-lockup-color', 'logo-lockup-color-light', 'logo-horizontal-color', 'logo-horizontal-color-light', 'logo-infinity-color', 'logo-infinity-gold']}
SCENE_DAY = b64(BG + 'scene-day.webp'); SCENE_NIGHT = b64(BG + 'scene-night.webp')
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
# Tỉ lệ trên kính xấu nhất: ĐO THẬT trên website (ảnh chụp tấm kính nằm trên toàn cảnh nền, vùng xấu nhất).
# Tỉ lệ trên nền trắng và trên nút: tính bằng công thức WCAG ở dưới.
GL_L = 'kính sáng xấu nhất (đo)'; GL_D = 'kính tối xấu nhất (đo)'
rows = [
 ('#12261C', '#FFFFFF', 'Mực ngọc lục', 'Chữ chính', None),
 ('#12261C', '#C9D9CB', 'Mực ngọc lục', 'Chữ chính, kính xấu nhất', (10.74, GL_L)),
 ('#2B4336', '#FFFFFF', 'Chữ phụ', 'Đoạn văn phụ', None),
 ('#2B4336', '#C9D9CB', 'Chữ phụ', 'Đoạn văn phụ, kính xấu nhất', (7.24, GL_L)),
 ('#40574A', '#FFFFFF', 'Chữ mờ', 'Chú thích, ngày tháng', None),
 ('#40574A', '#C9D9CB', 'Chữ mờ', 'Chú thích, kính xấu nhất', (5.29, GL_L)),
 ('#765225', '#FFFFFF', 'Vàng đồng', 'Chữ nhấn nhỏ, liên kết, icon, giá', None),
 ('#765225', '#C9D9CB', 'Vàng đồng', 'Chữ nhấn, kính xấu nhất', (4.72, GL_L)),
 ('#FBF7EE', '#1E5A40', 'Chữ ngà', 'Nút chính (ngọc lục)', None),
 ('#F3F5F1', '#26414A', 'Chữ chính (tối)', 'Đêm vườn: chữ chính, kính xấu nhất', (9.60, GL_D)),
 ('#D5DED8', '#26414A', 'Chữ phụ (tối)', 'Đêm vườn: đoạn văn phụ', (7.65, GL_D)),
 ('#AFC0B7', '#26414A', 'Chữ mờ (tối)', 'Đêm vườn: chú thích', (5.54, GL_D)),
 ('#E7CF9B', '#26414A', 'Champagne (tối)', 'Đêm vườn: chữ nhấn, liên kết, giá', (6.92, GL_D)),
]
def contrast_row(fg, bg, name, use, meas):
    r = meas[0] if meas else ratio(fg, bg); lv, cl = level(r)
    bgtxt = meas[1] if meas else f'<code>{bg}</code>'
    chip = f'<span class="cchip" style="background:{bg};color:{fg}">Aa</span>'
    return f'<tr><td>{chip}{name} <code>{fg}</code> trên {bgtxt}</td><td>{f"{r:.2f}".replace(".", ",")}:1</td><td class="{cl}">{lv}</td><td>{use}</td></tr>'
CONTRAST_HTML = ''.join(contrast_row(*r) for r in rows)
for r in rows: print(f'{r[0]} / {r[1]}: {ratio(r[0], r[1]):.2f}  (hiển thị: {r[4][0] if r[4] else "tính"})')

def swatch(name, vi, hexv, role, dark=False, border=False, bg=None, meta=None):
    if meta is None:
        r, g, b = [int(hexv[k:k+2], 16) for k in (1, 3, 5)]; meta = f'RGB {r} · {g} · {b}'
    return f'''<div class="sw"><div class="sw-chip{' sw-border' if border else ''}" style="background:{bg or hexv};color:{'#FBF7EE' if dark else '#12261C'}"><span>{hexv}</span></div>
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
<link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@300;400;500;600;700&family=Lora:ital,wght@0,400;0,500;1,400;1,500&family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500;1,600&display=swap" rel="stylesheet">
<style>
:root {{
  --ink:#12261C; --leaf:#1E5A40; --gold:#765225; --champ:#C7A262; --tulip:#F4A9BC; --sky:#9CC3EE; --sun:#F8E7D2; --night:#081425;
  --gold-grad:linear-gradient(100deg,#7A5A2B,#C7A262 46%,#8A6534);
  --text2:#2B4336; --text3:#40574A; --line:rgba(18,38,28,.12); --line2:rgba(18,38,28,.22);
  --sky-grad:linear-gradient(180deg,#6FA5E3 0%,#9CC3EE 30%,#CFE2F4 55%,#F1ECE4 74%,#F8E7D2 100%);
  --night-grad:linear-gradient(180deg,#060F20 0%,#0C1D3A 45%,#1A3552 78%,#2A4A5E 100%);
  --pane:linear-gradient(135deg,rgba(255,255,255,.8),rgba(255,255,255,.66) 48%,rgba(255,255,255,.72));
  --edge:rgba(255,255,255,.8);
  --rim:inset 0 0 0 1px rgba(255,255,255,.5),inset 0 1.5px 0 rgba(255,255,255,.98),inset 0 -1px 0 rgba(255,255,255,.55);
  --pane-shadow:0 36px 70px -32px rgba(18,44,66,.46),0 3px 8px rgba(18,44,66,.06),var(--rim);
  --card-shadow:0 12px 26px -16px rgba(18,44,66,.4),var(--rim);
  --btn-grad:linear-gradient(180deg,rgba(40,104,76,.94),rgba(14,50,36,.96)); --btn-edge:rgba(231,207,155,.5);
  --btn-shadow:0 16px 28px -14px rgba(12,46,32,.7),inset 0 1px 0 rgba(255,255,255,.45),inset 0 -10px 16px -10px rgba(0,0,0,.35);
  --spring:cubic-bezier(.2,1.4,.4,1);
  --blur:26px;
  --scene-day:url("{SCENE_DAY}"); --scene-night:url("{SCENE_NIGHT}");
  --drop:rgba(255,255,255,.82); --drop2:rgba(255,255,255,.62);
  --display:'Cormorant Garamond','Be Vietnam Pro',Georgia,serif; --body:'Be Vietnam Pro',system-ui,sans-serif; --serif:'Lora',Georgia,serif;
}}
*,*::before,*::after {{ box-sizing:border-box; margin:0; padding:0; }}
html {{ scroll-behavior:smooth; background:#9CC3EE; }}
body {{ font-family:var(--body); background:transparent; color:var(--ink); line-height:1.7; font-size:15px; -webkit-font-smoothing:antialiased; }}
/* Khung cảnh cố định: lễ cưới bên hồ ở Ý, pháo bông ở giữa ảnh */
body::before {{ content:''; position:fixed; z-index:-1; inset:0; pointer-events:none;
  background:var(--scene-day) center bottom / cover no-repeat, linear-gradient(180deg,#4C97E6,#86BFF2 45%,#CDE6F9); }}
a {{ color:var(--gold); }}
.wrap {{ max-width:1040px; margin:0 auto; padding:0 28px; }}
.art {{ display:block; width:100%; height:auto; }}
.cimg {{ display:block; max-width:100%; height:auto; }}
.sprite {{ position:absolute; width:0; height:0; overflow:hidden; }}

/* cover: cả khối đầu trang nằm trong kính, không đặt chữ lên cảnh */
.cover {{ position:relative; min-height:78vh; display:flex; align-items:center; justify-content:center; text-align:center; padding:70px 14px 20px; }}
.cover-pane {{ width:min(640px,100%); padding:clamp(30px,5vw,52px) clamp(20px,4vw,44px); background:var(--pane); -webkit-backdrop-filter:blur(var(--blur)) saturate(1.25) brightness(1.06); backdrop-filter:blur(var(--blur)) saturate(1.25) brightness(1.06); border:1px solid var(--edge); border-radius:40px; box-shadow:var(--pane-shadow); }}
.cover .c-lockup {{ width:min(400px,76vw); margin:0 auto; filter:drop-shadow(0 14px 24px rgba(18,44,66,.28)); }}
.crystal {{ width:min(150px,40vw); aspect-ratio:1; margin:0 auto; border-radius:50%; display:flex; align-items:center; justify-content:center; background:radial-gradient(circle at 32% 26%,rgba(255,255,255,.85),rgba(255,255,255,.28) 46%,rgba(255,255,255,.4)); border:1px solid var(--edge); box-shadow:0 30px 50px -26px rgba(18,44,66,.55),var(--rim); -webkit-backdrop-filter:blur(12px) saturate(1.8); backdrop-filter:blur(12px) saturate(1.8); }}
.crystal img {{ width:62%; }}
.cover-title {{ font-family:var(--display); font-weight:700; color:var(--gold); letter-spacing:.2em; text-transform:uppercase; font-size:13px; margin-top:30px; }}
.cover-sub {{ font-family:var(--serif); font-style:italic; color:var(--text2); margin-top:6px; }}
.cover-sys {{ display:inline-block; margin-top:14px; font-size:12px; font-weight:600; letter-spacing:.14em; text-transform:uppercase; padding:6px 16px; border-radius:99px; background:var(--drop2); -webkit-backdrop-filter:blur(10px) saturate(1.8); backdrop-filter:blur(10px) saturate(1.8); border:1px solid var(--edge); box-shadow:var(--rim); color:var(--ink); }}

/* toc: thanh menu kính nổi */
.toc {{ position:sticky; top:10px; z-index:5; width:min(1100px,calc(100% - 28px)); margin:0 auto; border-radius:999px; background:var(--drop);
  -webkit-backdrop-filter:blur(12px) saturate(1.9); backdrop-filter:blur(12px) saturate(1.9); border:1px solid var(--edge); box-shadow:0 14px 34px -18px rgba(18,44,66,.5),var(--rim); }}
.toc .wrap {{ display:flex; gap:4px; overflow-x:auto; padding:8px 12px; max-width:none; scrollbar-width:none; }}
.toc a {{ text-decoration:none; font-size:12px; white-space:nowrap; padding:6px 12px; border-radius:99px; color:var(--text2); }}
.toc a:hover {{ background:rgba(199,162,98,.2); color:var(--ink); }}

/* mỗi mục = một tấm kính nổi */
main {{ padding:22px 0 0; }}
section {{ padding:0; border:0; }}
section .wrap, footer .wrap {{ position:relative; }}
section .wrap::before {{ content:''; position:absolute; inset:0; border-radius:inherit; pointer-events:none; background:radial-gradient(420px circle at var(--lx,30%) var(--ly,0%),rgba(255,255,255,.35),transparent 60%); }}
section .wrap, footer .wrap {{ background:var(--pane); -webkit-backdrop-filter:blur(var(--blur)) saturate(1.25) brightness(1.06); backdrop-filter:blur(var(--blur)) saturate(1.25) brightness(1.06);
  border:1px solid var(--edge); border-radius:40px; box-shadow:var(--pane-shadow);
  width:min(1100px,calc(100% - 28px)); max-width:none; margin:22px auto; padding:clamp(34px,5vw,60px) clamp(20px,4.4vw,48px); }}
.num {{ font-family:var(--display); font-weight:700; color:var(--gold); font-size:18px; letter-spacing:.1em; }}
h2 {{ font-family:var(--display); font-weight:600; font-size:clamp(32px,4.6vw,50px); line-height:1.1; margin:6px 0 16px; }}
h2 em, .t-display em, .t-h2 em, .post blockquote em, .post .h em {{ font-style:italic; font-weight:500; background:var(--gold-grad); -webkit-background-clip:text; background-clip:text; color:transparent; -webkit-text-fill-color:transparent; }}
h3 {{ font-family:var(--display); font-weight:700; font-size:22px; margin:44px 0 14px; }}
.lead {{ font-size:17px; color:var(--text2); max-width:62ch; }}
p + p {{ margin-top:10px; }}
.note {{ font-size:13px; color:var(--text3); margin-top:12px; }}
.note b {{ color:var(--gold); font-weight:600; }}
.grid {{ display:grid; gap:18px; }}
.g2 {{ grid-template-columns:repeat(2,1fr); }} .g3 {{ grid-template-columns:repeat(3,1fr); }} .g4 {{ grid-template-columns:repeat(4,1fr); }}
.grid > * {{ min-width:0; }}
@media (max-width:760px) {{ .g2 {{ grid-template-columns:1fr; }} .g3,.g4 {{ grid-template-columns:1fr 1fr; }} :root {{ --blur:16px; }}
  section .wrap, footer .wrap {{ width:calc(100% - 16px); margin:14px auto; border-radius:30px; padding:34px 16px 36px; }} .toc {{ width:calc(100% - 16px); }}
  .board {{ padding:28px 16px 40px; }} .board .art {{ max-width:100%; }} table {{ display:block; overflow-x:auto; }} }}
@media (max-width:480px) {{ .g3,.g4 {{ grid-template-columns:1fr; }} }}
/* thẻ nằm trong tấm: trắng 52%, viền trắng, KHÔNG làm mờ */
.card {{ background:linear-gradient(135deg,rgba(255,255,255,.58),rgba(255,255,255,.34)); border:1px solid rgba(255,255,255,.78); border-radius:24px; padding:26px; box-shadow:var(--card-shadow); transition:transform .5s var(--spring); }}
.card:hover {{ transform:translateY(-5px); }}
@media (prefers-reduced-motion:reduce) {{ .card {{ transition:none; }} .card:hover {{ transform:none; }} }}
.card h4 {{ font-family:var(--display); font-weight:700; font-size:19px; margin-bottom:6px; }}
.card p {{ font-size:14px; color:var(--text2); }}
.label {{ font-size:10px; font-weight:600; letter-spacing:.16em; text-transform:uppercase; color:var(--gold); margin-bottom:10px; display:block; }}

/* bảng minh hoạ logo */
.board {{ border-radius:24px; display:flex; align-items:center; justify-content:center; padding:36px; min-height:230px; position:relative; border:1px solid rgba(255,255,255,.85); }}
.board .cap {{ position:absolute; left:16px; right:16px; bottom:12px; font-size:11px; line-height:1.4; color:var(--text3); }}
.b-glass {{ background:linear-gradient(135deg,rgba(255,255,255,.58),rgba(255,255,255,.34)); box-shadow:var(--card-shadow); }}
.b-sky {{ background:var(--sky-grad); }}
.b-deep {{ background:rgba(14,40,30,.9); color:#F3F5F1; border-color:rgba(255,255,255,.3); }}
.b-night {{ background:var(--night-grad); color:#F3F5F1; border-color:rgba(255,255,255,.16); }}
.b-deep .cap, .b-night .cap {{ color:rgba(244,251,246,.88); }}
.clear {{ outline:1px dashed var(--gold); outline-offset:26px; }}
.dont {{ min-height:170px; padding:22px; overflow:hidden; }}
.dont::after {{ content:'✕'; position:absolute; right:12px; top:8px; color:var(--gold); font-weight:700; }}
.dont .art {{ width:120px; }}

/* màu */
.sw-chip {{ height:132px; border-radius:20px; display:flex; align-items:flex-end; padding:12px 14px; font-size:13px; font-weight:600; letter-spacing:.04em; }}
.sw-border {{ border:1px solid var(--edge); }}
.sw-name {{ font-family:var(--display); font-weight:700; font-size:19px; margin-top:10px; }}
.sw-name em {{ font-family:var(--body); font-style:normal; font-weight:400; font-size:12px; color:var(--text3); margin-left:4px; }}
.sw-meta {{ font-size:12px; color:var(--text3); margin-top:0; }}
.sw-role {{ font-size:13px; color:var(--text2); margin-top:4px; line-height:1.5; }}
.ratio {{ display:flex; height:46px; border-radius:16px; overflow:hidden; margin-top:8px; border:1px solid var(--edge); }}
.legend {{ list-style:none; display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:6px 18px; margin-top:12px; font-size:13px; color:var(--text2); }}
.legend i {{ display:inline-block; width:12px; height:12px; border-radius:4px; margin-right:8px; vertical-align:-1px; border:1px solid var(--line2); }}
table {{ width:100%; border-collapse:collapse; font-size:14px; margin-top:8px; }}
th {{ text-align:left; font-size:10px; letter-spacing:.14em; text-transform:uppercase; color:var(--text3); font-weight:600; padding:10px 12px; border-bottom:1px solid var(--line2); }}
td {{ padding:11px 12px; border-bottom:1px solid var(--line); vertical-align:top; }}
td code, p code, li code {{ font-family:ui-monospace,Menlo,monospace; font-size:12.5px; background:rgba(18,38,28,.08); padding:1px 6px; border-radius:6px; }}
.pass {{ color:var(--leaf); font-weight:600; }} .fail {{ color:#765225; font-weight:600; }}
.cchip {{ display:inline-block; width:34px; height:24px; line-height:24px; text-align:center; border-radius:8px; margin-right:10px; font:600 12px var(--body); border:1px solid var(--line2); vertical-align:middle; }}
.tints {{ display:grid; grid-template-columns:repeat(8,1fr); gap:8px; }}
.tints div {{ height:64px; border-radius:16px; font-size:10px; display:flex; align-items:flex-end; padding:7px; color:var(--ink); border:1px solid var(--edge); }}
@media (max-width:760px) {{ .tints {{ grid-template-columns:repeat(4,1fr); }} }}

/* chữ */
.spec {{ display:grid; grid-template-columns:150px 1fr; gap:20px; padding:22px 0; border-bottom:1px solid var(--line); align-items:baseline; }}
.spec small {{ font-size:11px; color:var(--text3); line-height:1.5; display:block; }}
@media (max-width:640px) {{ .spec {{ grid-template-columns:1fr; gap:6px; }} }}
.t-display {{ font-family:var(--display); font-weight:600; font-size:clamp(38px,5.8vw,68px); line-height:1.05; }}
.t-h2 {{ font-family:var(--display); font-weight:600; font-size:36px; line-height:1.15; }}
.t-h3 {{ font-family:var(--display); font-weight:700; font-size:20px; }}
.t-eyebrow {{ font-family:var(--serif); font-style:italic; font-size:18px; color:var(--text2); }}
.t-body {{ font-size:16px; color:var(--text2); max-width:60ch; }}
.t-label {{ font-size:11px; font-weight:600; letter-spacing:.16em; text-transform:uppercase; color:var(--gold); }}
.glyphs {{ font-family:var(--display); font-weight:600; font-size:28px; line-height:1.5; word-break:break-word; }}

/* nền & hoa */
.scene {{ position:relative; height:190px; border-radius:24px; overflow:hidden; border:1px solid rgba(255,255,255,.7); }}
.scene {{ height:230px; background-position:center; background-size:cover; background-repeat:no-repeat; }}
.scene.day {{ background-image:var(--scene-day); }} .scene.night {{ background-image:var(--scene-night); }}

/* thành phần kính (ví dụ minh hoạ — dựng trong khung trời) */
.stage {{ position:relative; border-radius:28px; padding:26px; overflow:hidden; border:1px solid rgba(255,255,255,.7);
  background:radial-gradient(circle at 12% 70%,rgba(244,169,188,.6) 0 60px,transparent 62px),radial-gradient(circle at 88% 30%,rgba(199,162,98,.5) 0 90px,transparent 92px),var(--sky-grad); }}
.stage.night {{ background:radial-gradient(circle at 12% 70%,rgba(244,169,188,.32) 0 60px,transparent 62px),radial-gradient(circle at 88% 30%,rgba(231,207,155,.3) 0 90px,transparent 92px),var(--night-grad); }}
.row {{ display:flex; flex-wrap:wrap; gap:10px; align-items:center; }}
.d-pane {{ background:var(--pane); -webkit-backdrop-filter:blur(26px) saturate(1.25) brightness(1.06); backdrop-filter:blur(26px) saturate(1.25) brightness(1.06); border:1px solid var(--edge); border-radius:40px; box-shadow:var(--pane-shadow); padding:26px; }}
.d-card {{ background:linear-gradient(135deg,rgba(255,255,255,.58),rgba(255,255,255,.34)); border:1px solid rgba(255,255,255,.78); border-radius:24px; box-shadow:var(--card-shadow); padding:16px; transition:transform .5s var(--spring); }}
.d-card:hover {{ transform:translateY(-5px); }}
.d-float {{ background:var(--pane); -webkit-backdrop-filter:blur(26px) saturate(1.25) brightness(1.06); backdrop-filter:blur(26px) saturate(1.25) brightness(1.06); border:1px solid var(--edge); border-radius:28px; box-shadow:var(--pane-shadow); padding:16px; }}
.d-nav {{ display:flex; align-items:center; justify-content:space-between; gap:10px; padding:10px 14px; border-radius:999px; background:var(--drop); -webkit-backdrop-filter:blur(12px) saturate(1.9); backdrop-filter:blur(12px) saturate(1.9); border:1px solid var(--edge); box-shadow:0 14px 34px -18px rgba(18,44,66,.5),var(--rim); font-size:13px; }}
.d-nav .orb {{ width:30px; flex:none; }}
.btn {{ font:500 14px var(--body); padding:12px 24px; border-radius:999px; border:1px solid var(--btn-edge); cursor:default; display:inline-block; transition:transform .4s var(--spring); }}
.btn:active, .pill:active {{ transform:scale(.96); }}
.btn-p {{ background:var(--btn-grad); color:#FBF7EE; box-shadow:var(--btn-shadow); }}
.btn-s {{ background:linear-gradient(135deg,rgba(255,255,255,.82),rgba(255,255,255,.6)); color:var(--ink); border-color:var(--edge); -webkit-backdrop-filter:blur(12px) saturate(1.9); backdrop-filter:blur(12px) saturate(1.9); box-shadow:var(--rim); }}
.pill {{ font-size:12px; padding:7px 16px; border-radius:999px; background:var(--drop2); border:1px solid var(--edge); color:var(--text2); -webkit-backdrop-filter:blur(10px) saturate(1.8); backdrop-filter:blur(10px) saturate(1.8); box-shadow:var(--rim); transition:transform .4s var(--spring); }}
.pill.on {{ background:var(--btn-grad); color:#FBF7EE; border-color:var(--btn-edge); box-shadow:var(--btn-shadow); }}
.badge {{ font-size:9px; font-weight:600; letter-spacing:.12em; text-transform:uppercase; padding:4px 10px; border-radius:99px; background:rgba(199,162,98,.16); color:var(--gold); border:1px solid rgba(122,86,40,.32); }}
.input {{ font:400 14px var(--body); background:var(--drop); -webkit-backdrop-filter:blur(10px) saturate(1.8); backdrop-filter:blur(10px) saturate(1.8); border:1px solid var(--edge); border-radius:999px; padding:12px 20px; color:var(--text3); min-width:240px; box-shadow:var(--rim); }}
.demo-card {{ background:linear-gradient(135deg,rgba(255,255,255,.58),rgba(255,255,255,.34)); border:1px solid rgba(255,255,255,.78); border-radius:24px; box-shadow:var(--card-shadow); overflow:hidden; max-width:300px; }}
.demo-thumb {{ height:140px; background:linear-gradient(135deg,rgba(170,225,200,.8),rgba(255,255,255,.4)); display:flex; align-items:flex-start; padding:12px; }}
.demo-body {{ padding:16px; }}
.demo-foot {{ display:flex; justify-content:space-between; font-size:12px; color:var(--text3); border-top:1px solid var(--line); margin-top:12px; padding-top:12px; }}
.demo-foot b {{ color:var(--gold); font-weight:600; }}
.night .d-pane {{ background:linear-gradient(135deg,rgba(16,32,46,.78),rgba(8,20,32,.66) 48%,rgba(14,28,42,.72)); -webkit-backdrop-filter:blur(26px) saturate(1.25) brightness(.8); backdrop-filter:blur(26px) saturate(1.25) brightness(.8); border-color:rgba(255,255,255,.16); color:#F3F5F1; box-shadow:0 34px 70px -30px rgba(0,0,0,.7),inset 0 0 0 1px rgba(255,255,255,.12),inset 0 1.5px 0 rgba(255,255,255,.34); }}
.night .d-card {{ background:rgba(255,255,255,.07); border-color:rgba(255,255,255,.16); color:#D2DFD7; box-shadow:none; }}
.night .btn-p {{ background:linear-gradient(180deg,#F6E9C6,#D8BA7A); color:#1B2A1F; border-color:rgba(255,255,255,.55); }}
.night .btn-s {{ background:rgba(255,255,255,.1); color:#F3F5F1; border-color:rgba(255,255,255,.16); }}

/* giọng */
.vs td:first-child {{ font-weight:600; width:34%; }}
.eg {{ border-left:3px solid var(--champ); padding:4px 0 4px 16px; margin-top:12px; font-size:14px; color:var(--text2); }}
.eg.bad {{ border-color:#765225; }}
.eg b {{ display:block; font-size:10px; letter-spacing:.14em; text-transform:uppercase; margin-bottom:3px; color:var(--gold); }}
.eg.bad b {{ color:var(--gold); }}

/* mẫu bài đăng: cảnh hồ Ý, chữ nằm trong kính */
.post {{ aspect-ratio:1/1; border-radius:14px; position:relative; overflow:hidden; display:flex; flex-direction:column; padding:8%; background:var(--scene-day) center / cover no-repeat; border:1px solid rgba(255,255,255,.7); }}
.post.n {{ background:var(--scene-night) center / cover no-repeat; }}
.pg {{ flex:1; display:flex; flex-direction:column; justify-content:center; padding:9%; border-radius:22px; background:var(--pane); -webkit-backdrop-filter:blur(16px) saturate(1.25) brightness(1.06); backdrop-filter:blur(16px) saturate(1.25) brightness(1.06); border:1px solid var(--edge); box-shadow:var(--pane-shadow); position:relative; }}
.n .pg {{ background:linear-gradient(135deg,rgba(16,32,46,.78),rgba(8,20,32,.66) 48%,rgba(14,28,42,.72)); -webkit-backdrop-filter:blur(16px) saturate(1.25) brightness(.8); backdrop-filter:blur(16px) saturate(1.25) brightness(.8); border-color:rgba(255,255,255,.16); color:#F3F5F1; box-shadow:0 24px 60px -18px rgba(0,0,0,.6),inset 0 1.5px 0 rgba(255,255,255,.34); text-align:center; align-items:center; }}
.post blockquote {{ font-family:var(--display); font-size:clamp(15px,2vw,23px); line-height:1.25; }}
.n .h em {{ background:none; -webkit-text-fill-color:#E7CF9B; color:#E7CF9B; }}
.post cite {{ font-family:var(--serif); font-size:12px; color:var(--text3); margin-top:12px; font-style:normal; }}
.post .orb {{ width:14%; position:absolute; right:7%; bottom:8%; }}
.post .k {{ font-size:10px; letter-spacing:.2em; text-transform:uppercase; color:#AFC0B7; }}
.post .h {{ font-family:var(--display); font-weight:700; font-size:clamp(17px,2.3vw,26px); line-height:1.15; margin:8px 0; }}
.post .nm {{ font-family:var(--display); font-weight:700; color:var(--gold); font-size:18px; }}
.post .s {{ font-size:12px; color:var(--text2); margin-top:8px; }}
.post .f {{ width:46%; margin-top:14px; color:var(--ink); }}

ul.rules {{ list-style:none; }}
ul.rules li {{ padding:9px 0 9px 26px; position:relative; border-bottom:1px solid var(--line); font-size:14px; color:var(--text2); }}
ul.rules li::before {{ content:'—'; position:absolute; left:0; color:var(--gold); }}
ul.rules.no li::before {{ content:'✕'; color:var(--gold); font-size:12px; top:11px; }}
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
  <div class="cover-pane">
    {img('logo-lockup-color', '', 'Timeless Harmony — hold us together').replace('class="cimg"', 'class="cimg c-lockup"')}
    <p class="cover-title">Brand Guideline</p>
    <p class="cover-sub">Phiên bản 2.2 · tháng 11, 2026 — Vườn kính · kính lỏng</p>
    <span class="cover-sys">Hệ nhận diện “Vườn kính” · kính lỏng</span>
  </div>
</header>

<nav class="toc"><div class="wrap">
  <a href="#cot-loi">01 Cốt lõi</a><a href="#logo">02 Logo</a><a href="#mau">03 Màu sắc</a><a href="#chu">04 Kiểu chữ</a>
  <a href="#nen">05 Hình nền</a><a href="#anh">06 Hình ảnh</a><a href="#giao-dien">07 Giao diện</a><a href="#giong">08 Giọng nói</a>
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
    <div class="card"><h4>Quả cầu</h4><p>Một giọt sương, một viên ngọc giữ lại khoảnh khắc — kính ngọc lục, trong và sâu.</p></div>
    <div class="card"><h4>Vô cực</h4><p>Tình yêu không có điểm kết — <i>timeless</i>.</p></div>
    <div class="card"><h4>Hai nụ tulip</h4><p>Hai người trên cùng một đường — <i>harmony</i>. Tulip là loài hoa của tình yêu trọn vẹn; trong bản màu, hai nụ là điểm hồng duy nhất trên quả cầu.</p></div>
    <div class="card"><h4>Vòng tròn T · H</h4><p>Chiếc nhẫn và sự trọn vẹn; hai chữ cái đầu ở hai bên, mở ra chứ không khép kín. Chỉ còn trong các bản một màu.</p></div>
  </div>
  <p class="note"><b>Cần xác nhận:</b> đây là diễn giải đề xuất từ artwork gốc và hướng “Vườn kính · kính lỏng”. Nếu ý nghĩa ban đầu của bạn khác, hãy sửa ở đây để mọi nội dung kể cùng một câu chuyện.</p>
</div></section>

<section id="logo"><div class="wrap">
  <span class="num">02</span>
  <h2>Logo</h2>
  <p class="lead">Trên màn hình, logo chính là <b>quả cầu kính ngọc lục</b>: dấu vô cực ánh vàng, nụ tulip hồng phấn. Khi cần in một màu, khắc hay dập nổi, dùng các bản nét một màu. Chọn theo cách hiển thị và kích thước; không tự vẽ lại hay sắp xếp lại các thành phần.</p>
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
    <div class="board b-glass" style="min-height:230px">{img('logo-infinity-color', 'width:min(300px,100%)', 'Dấu vô cực màu')}<span class="cap">Một nét liền, không cắt nhau — thân mực ngọc lục, hai đầu nở thành hai nụ tulip hồng. Đặt trên kính sáng.</span></div>
    <ul class="rules" style="margin:0">
      <li><b>Quả cầu</b> là kính ngọc lục (gradient <code>#2F7458 → #164634 → #08221A</code>), bóng sáng nhẹ ở góc trên trái. Dấu vô cực ánh vàng (<code>#F6E7BE → #D9B878</code>) nằm ở giữa; nụ tulip hồng phấn <code>#F4A9BC</code> ở hai đầu.</li>
      <li><b>Dấu vô cực</b> là một nét duy nhất: mảnh ở hai nụ, đầy dần về giữa. Hình đối xứng khi xoay 180°.</li>
      <li><b>Hai nụ tulip</b> giống hệt nhau, mỗi nụ có hai cánh ngoài và một cánh giữa ló ra phía sau.</li>
      <li><b>Bản một màu</b> giữ vòng tròn ngắt ở hai bên cho chữ <b>T</b> và <b>H</b>; nét đứng của T, H bằng độ dày vòng tròn.</li>
      <li><b>Chữ logo</b>: Belleza làm đậm nhẹ. <b>Tagline</b>: Lora 540. Cả hai đã chuyển thành đường nét, không cần cài phông.</li>
      <li>Quả cầu <b>pha lê</b> ở đầu trang chủ dùng dấu vô cực thân ánh vàng <code>logo-infinity-gold.svg</code>.</li>
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
    <tr><td>Dấu vô cực đứng riêng, trang trí</td><td><code>logo-infinity-color.svg</code> (thân mực) hoặc <code>logo-infinity-gold.svg</code> (thân ánh vàng) trên kính</td></tr>
    <tr><td>In một màu, khắc, dập nổi, hoặc nơi không in được gradient</td><td>Bản nét một màu: <code>logo-lockup</code>, <code>logo-horizontal</code>, <code>logo-mark</code>, <code>logo-mark-medium</code>, <code>logo-compact</code>, <code>logo-wordmark</code>, <code>logo-tagline</code>, <code>logo-infinity</code></td></tr>
  </table></div>

  <h3>Bản nét một màu</h3>
  <div class="grid g2">
    <div class="board b-glass">{art('logo-lockup','',"width:170px")}<span class="cap">Bản đầy đủ một màu — mực ngọc lục</span></div>
    <div class="board b-glass"><div style="width:min(300px,100%)">{art('logo-horizontal')}</div><span class="cap">Bản ngang một màu</span></div>
    <div class="board b-glass"><div style="width:270px;max-width:100%">{art('logo-wordmark')}{art('logo-tagline','',"width:52%;margin:8px auto 0")}</div><span class="cap">Logo chữ + tagline — chân trang, khi biểu tượng đã có ở chỗ khác</span></div>
    <div class="board b-glass"><div class="row" style="gap:22px;align-items:center;justify-content:center">{art('logo-mark','',"width:110px")}{art('logo-mark-medium','',"width:72px")}{art('logo-compact','',"width:32px")}</div><span class="cap">Biểu tượng theo cỡ — đầy đủ · nét vừa · thu nhỏ</span></div>
  </div>
  <p class="note">Nhỏ hơn 120px thì vòng tròn mảnh và chữ T, H bị mất: chuyển sang bản nét vừa. Nhỏ hơn 48px: dùng bản thu nhỏ. Riêng quả cầu màu dùng được từ 16px.</p>

  <h3>Trên nền nào</h3>
  <div class="grid g4">
    <div class="board b-sky" style="min-height:190px">{img('logo-orb','width:96px','Quả cầu')}<span class="cap">Trời ✓ · chữ mực</span></div>
    <div class="board b-glass" style="min-height:190px">{img('logo-orb','width:96px','Quả cầu')}<span class="cap">Kính sáng ✓ · chữ mực</span></div>
    <div class="board b-deep" style="min-height:190px">{img('logo-orb','width:96px','Quả cầu')}<span class="cap">Kính ngọc lục đậm ✓ · chữ trắng</span></div>
    <div class="board b-night" style="min-height:190px">{img('logo-orb','width:96px','Quả cầu')}<span class="cap">Đêm vườn ✓ · chữ trắng</span></div>
  </div>
  <p class="note">Quả cầu dùng được trên <b>mọi nền</b>. Phần chữ: <b>mực ngọc lục</b> trên nền sáng; <b>trắng</b> (bản <code>-light</code>) trên nền tối hoặc ảnh. Bản một màu: mực ngọc lục <code>#12261C</code> trên nền sáng, trắng trên nền tối. Trên ảnh chụp: đặt logo trong một mảng kính hoặc màu đặc, không đặt trực tiếp lên ảnh.</p>

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
    <div class="board b-glass dont">{img('logo-orb','width:100px;filter:hue-rotate(150deg)','')}<span class="cap">Đổi màu quả cầu (kính ngọc lục)</span></div>
    <div class="board b-glass dont">{img('logo-infinity-color','width:150px;filter:hue-rotate(110deg)','')}<span class="cap">Tô nụ tulip màu khác hồng phấn</span></div>
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
  <p class="lead">Bảng màu lấy từ một buổi sáng nắng trong vườn: trời, mực ngọc lục cho chữ, ngọc lục cho hành động, một chút vàng đồng. Nền là cảnh vườn; mọi nội dung nằm trong kính trắng.</p>
  <h3>Màu chính</h3>
  <div class="grid g4">
    {swatch('Emerald ink','Mực ngọc lục','#12261C','Chữ, logo, nét vẽ. Chữ phụ <code>#2B4336</code>, <code>#40574A</code>.',dark=True)}
    {swatch('Emerald','Ngọc lục','#1E5A40','Nút chính, hành động. Nút dùng gradient rgba(40,104,76,.94) → rgba(14,50,36,.96), viền vàng mảnh.',dark=True,bg='linear-gradient(180deg,rgba(40,104,76,.94),rgba(14,50,36,.96))',meta='RGB 30 · 90 · 64')}
    {swatch('Bronze gold','Vàng đồng','#765225','Chữ nhấn nhỏ, liên kết, icon, giá tiền. Là màu vàng duy nhất dùng cho chữ nhỏ.',dark=True)}
    {swatch('Champagne','Vàng champagne','#C7A262','Chỉ để trang trí: viền mảnh, gradient chữ lớn. Không dùng cho chữ nhỏ.')}
  </div>
  <h3>Màu bổ trợ</h3>
  <div class="grid g4">
    {swatch('Tulip','Hồng tulip','#F4A9BC','Chỉ trong hình vẽ và nụ hoa của logo. Không dùng cho chữ.')}
    {swatch('Sky','Trời','#9CC3EE','Nền trời, quầng sáng.')}
    {swatch('Morning sun','Nắng sớm','#F8E7D2','Chân trời, ánh nắng ấm cuối gradient trời.',border=True)}
    {swatch('Night sky','Trời đêm','#081425','Chế độ tối “Đêm vườn”.',dark=True)}
  </div>
  <h3>Đêm vườn</h3>
  <div class="grid g4">
    {swatch('Night text','Chữ (tối)','#F3F5F1','Chữ chính; chữ phụ <code>#D5DED8</code>, <code>#AFC0B7</code>.',dark=True,bg='#081425')}
    {swatch('Night accent','Champagne nhấn','#E7CF9B','Chữ nhấn, liên kết, icon trong chế độ tối.',dark=True,bg='#081425')}
    {swatch('Night button','Nút chính (tối)','#F6E9C6 → #D8BA7A','Gradient champagne, chữ mực.',bg='linear-gradient(180deg,#F6E9C6,#D8BA7A)',meta='Chữ mực #1B2A1F')}
    {swatch('Night sky gradient','Gradient trời đêm','#060F20 → #2A4A5E','Trăng, sao, đèn làng ven hồ; dự phòng khi ảnh cảnh đêm chưa tải.',dark=True,bg='var(--night-grad)',meta='4 điểm: 0 · 45 · 78 · 100%')}
  </div>
  <h3>Nền &amp; kính</h3>
  <div class="grid g2">
    {swatch('Glass','Trắng kính','rgba(255,255,255,.6–.82)','Tấm .8 → .66 → .72 · giọt .82 → .6 · thẻ .58 → .34 · viền .8.',border=True,bg='linear-gradient(135deg,rgba(255,255,255,.8),rgba(255,255,255,.66) 48%,rgba(255,255,255,.72)),var(--sky-grad)',meta='Trắng, đục 66–80%')}
    {swatch('Sky gradient','Gradient trời','#6FA5E3 → #F8E7D2','Dự phòng khi ảnh cảnh chưa tải: #4C97E6 → #CDE6F9 trên nền trang, và khung minh hoạ.',bg='var(--sky-grad)',meta='5 điểm: 0 · 30 · 55 · 74 · 100%')}
  </div>
  <h3>Tỷ lệ sử dụng</h3>
  <div class="ratio"><div style="flex:34;background:var(--sky-grad)"></div><div style="flex:30;background:rgba(255,255,255,.8)"></div><div style="flex:20;background:var(--ink)"></div><div style="flex:8;background:var(--btn-grad)"></div><div style="flex:8;background:var(--gold-grad)"></div></div>
  <ul class="legend"><li><i style="background:#9CC3EE"></i>Cảnh nền · phần còn lại</li><li><i style="background:#fff"></i>Kính trắng</li><li><i style="background:#12261C"></i>Mực ngọc lục</li><li><i style="background:#1E5A40"></i>Ngọc lục cho hành động</li><li><i style="background:#C7A262"></i>Vàng · ≤ 8%</li><li><i style="background:#F4A9BC"></i>Hồng · chỉ trong hình</li></ul>
  <p class="note">Mỗi màn hình hoặc mỗi bài đăng chỉ nên có <b>một</b> cụm chữ nhấn vàng. Hồng tulip không bao giờ dùng cho chữ.</p>

  <h3>Độ tương phản (WCAG 2.1)</h3>
  <p style="color:var(--text2);font-size:14px;max-width:70ch">Hàng “kính xấu nhất” là số <b>đo thật</b> trên website: ảnh chụp tấm kính nằm trên toàn cảnh nền (hồ, cỏ, pháo bông), ở vùng xấu nhất. Hàng nền trắng và nút tính bằng công thức WCAG. Chữ thường cần ≥ 4,5:1 (AA); ≥ 7:1 là AAA; chữ lớn (từ 24px, hoặc 19px đậm) cần ≥ 3:1. <b>Quy tắc:</b> độ đục của kính (<code>--pane</code>) đã được chỉnh theo phép đo này; đổi cảnh nền hoặc độ đục thì phải đo lại.</p>
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
    <div class="card"><span class="label">Tiêu đề</span><p style="font-family:var(--display);font-weight:600;font-size:42px;line-height:1.1;color:var(--ink)">Cormorant Garamond</p><p style="margin-top:8px">Dùng 600 cho tiêu đề, 700 cho tiêu đề nhỏ; chữ nhấn <i>nghiêng</i> 500, tô gradient vàng. Phông có chữ thường thấp nên website đặt <code>font-size-adjust: .46</code>.</p></div>
    <div class="card"><span class="label">Giao diện &amp; đoạn văn</span><p style="font-family:var(--body);font-size:34px;font-weight:500;line-height:1.1;color:var(--ink)">Be Vietnam Pro</p><p style="margin-top:8px">Thiết kế riêng cho tiếng Việt. 400 cho văn bản, 500–600 cho nút và nhãn.</p></div>
    <div class="card"><span class="label">Tagline &amp; trích dẫn</span><p style="font-family:var(--serif);font-size:40px;font-style:italic;line-height:1.1;color:var(--ink)">Lora</p><p style="margin-top:8px">Dùng nghiêng cho tagline, lời dẫn, trích dẫn. Không dùng cho tiêu đề chính.</p></div>
  </div>
  <p class="note">Chữ trong logo dùng Belleza (logo chữ) và Lora 540 (tagline), đã chuyển thành hình vẽ. Không dùng Belleza cho chữ trên website hay ấn phẩm: phông này không có dấu tiếng Việt.</p>
  <h3>Thang chữ</h3>
  <div class="spec"><div><span class="t-label">Tiêu đề lớn</span><small>Cormorant Garamond 600 · 38–68px · 1.05</small></div><p class="t-display">Đám cưới của bạn<br><em>bắt đầu từ đây</em></p></div>
  <div class="spec"><div><span class="t-label">Tiêu đề mục</span><small>Cormorant Garamond 600 · 28–38px · 1.15</small></div><p class="t-h2">Được xây dựng trên <em>sự tin tưởng</em></p></div>
  <div class="spec"><div><span class="t-label">Tiêu đề nhỏ</span><small>Cormorant Garamond 700 · 18–22px</small></div><p class="t-h3">Ký quỹ thanh toán an toàn</p></div>
  <div class="spec"><div><span class="t-label">Lời dẫn</span><small>Lora nghiêng · 16–18px</small></div><p class="t-eyebrow">hold us together</p></div>
  <div class="spec"><div><span class="t-label">Đoạn văn</span><small>Be Vietnam Pro 400 · 14–16px · 1.7</small></div><p class="t-body">Tìm đúng nhà cung cấp cho ngày trọng đại — được tuyển chọn kỹ, thanh toán an toàn qua ký quỹ.</p></div>
  <div class="spec"><div><span class="t-label">Nhãn</span><small>Be Vietnam Pro 600 · 10–11px · chữ hoa · giãn 0.16em</small></div><p class="t-label">Nhà cung cấp nổi bật</p></div>
  <h3>Quy tắc</h3>
  <ul class="rules">
    <li>Chữ nhấn trong tiêu đề: đặt trong thẻ <code>&lt;em&gt;</code> — tự động thành Cormorant Garamond nghiêng 500, tô gradient vàng <code>linear-gradient(100deg,#7A5A2B,#C7A262 46%,#8A6534)</code> bằng <code>background-clip:text</code>. Mỗi tiêu đề chỉ nhấn một cụm.</li>
    <li>Cỡ nhỏ nhất cho tiêu đề là <b>18px, đậm 700</b>: dưới cỡ đó nét mảnh của Cormorant dễ mất. Chữ thường thấp nên luôn đặt <code>font-size-adjust: .46</code>.</li>
    <li>Không viết HOA toàn bộ tiêu đề tiếng Việt (dấu chồng lên nhau, khó đọc). Chữ hoa chỉ dùng cho nhãn ngắn.</li>
    <li>Chiều dài dòng văn bản: 55–70 ký tự. Căn trái; không căn đều hai bên.</li>
    <li>Chữ trong logo “TIMELESS HARMONY” là hình vẽ, không gõ lại bằng phông.</li>
  </ul>
  <h3>Kiểm tra dấu tiếng Việt</h3>
  <p class="glyphs">Ầ Ẩ Ẫ Ậ Ắ Ằ Ẳ Ẵ Ặ Đ Ễ Ệ Ỗ Ộ Ờ Ở Ỡ Ợ Ữ Ự ỳ ỷ ỹ ỵ<br><span style="font-style:italic">Giữ chúng mình bên nhau — những điều nhỏ, thật lòng</span></p>
</div></section>

<section id="nen"><div class="wrap">
  <span class="num">05</span>
  <h2>Hình <em>nền</em></h2>
  <p class="lead">Mỗi trang là một lễ cưới trong vườn biệt thự bên hồ ở Ý, nhìn từ trên cao: trời xanh, dãy núi bên kia hồ, mặt hồ ngọc lam, lan can đá có ban công cong, thảm cỏ sọc và lối sỏi. Hai dãy ghế có khách (chỉ là hình dáng nhìn từ sau, không có gương mặt) chạy dọc lối đi viền hoa trắng dẫn tới cổng hoa; cô dâu chú rể nhỏ đứng dưới cổng, và phía sau là chùm pháo bông ngày nhiều màu xoè hình quạt.</p>
  <p class="note">Bản đêm: trăng, sao, đèn làng ven hồ, nến dọc lối đi và pháo bông rực hơn. Pháo bông nhiều màu là <b>điểm nhấn màu duy nhất</b> của cảnh, nên giao diện giữ màu tiết chế: ngọc lục, vàng và kính trắng.</p>
  <div class="grid g2" style="margin-top:30px">
    <div><div class="scene day"></div><p class="note"><code>scene-day.webp</code> · chế độ sáng — hồ Ý, lối hoa trắng, cổng hoa và pháo bông ngày</p></div>
    <div><div class="scene night"></div><p class="note"><code>scene-night.webp</code> · chế độ tối “Đêm vườn” — trăng, sao, đèn làng, nến và pháo bông rực</p></div>
  </div>
  <div class="card" style="margin-top:22px"><table>
    <tr><th>Tệp</th><th>Vai trò</th></tr>
    <tr><td><code>assets/bg/scene-day.webp</code> · <code>scene-night.webp</code></td><td>Cảnh nền máy tính, 2000×1250, ngày và đêm</td></tr>
    <tr><td><code>assets/bg/scene-day-m.webp</code> · <code>scene-night-m.webp</code></td><td>Bản dọc cho điện thoại, 900×1950</td></tr>
    <tr><td><code>docs/design/build_background.py</code> + <code>render_background.js</code></td><td>Vẽ SVG vào <code>docs/design/.build/</code> (không commit), rồi xuất WebP ra <code>assets/bg/</code></td></tr>
  </table></div>
  <div class="grid g2" style="margin-top:26px">
    <div><h3 style="margin-top:0">Nên</h3><ul class="rules">
      <li>Nền luôn <b>cố định</b> (<code>position: fixed</code>, <code>cover</code>): nội dung cuộn, khung cảnh đứng yên.</li>
      <li>Những thứ quan trọng (cổng hoa, pháo bông) nằm <b>giữa ảnh</b>, vì điện thoại cắt hai bên.</li>
      <li><b>Mọi chữ nằm trong kính</b>, kể cả khối tiêu đề đầu trang.</li>
      <li>Chế độ sáng và tối dùng cặp ảnh tương ứng; không trộn ngày với đêm.</li>
    </ul></div>
    <div><h3 style="margin-top:0">Không</h3><ul class="rules no">
      <li>Đặt chữ trực tiếp lên cảnh — cỏ, hồ và pháo bông làm chữ khó đọc.</li>
      <li>Cuộn cảnh theo nội dung, hoặc đặt cổng hoa, pháo bông sát mép ảnh.</li>
      <li>Thay bằng ảnh stock hay nền đặc; thêm khuôn mặt vào khách mời.</li>
      <li>Dùng màu pháo bông làm màu giao diện — chỉ ngọc lục, vàng và kính trắng.</li>
    </ul></div>
  </div>

  <h3>Tulip nét mảnh</h3>
  <p class="lead" style="font-size:15px">Bốn cụm tulip nét mảnh (<code>assets/brand/tulip-*.svg</code>) là hình vẽ của thời artwork gốc. Chúng chỉ còn dùng trên <b>kính ngọc lục đậm</b> (khối kêu gọi hành động) và trên ấn phẩm in. Một màu, trắng ngà trên nền ngọc lục đậm.</p>
  <div class="grid g4" style="margin-top:22px;align-items:end">
    <div class="board b-deep">{art('tulip-top-left','',"width:110px;color:#F3F5F1")}<span class="cap">Góc trên trái</span></div>
    <div class="board b-deep">{art('tulip-right','',"width:110px;color:#F3F5F1")}<span class="cap">Cạnh phải</span></div>
    <div class="board b-deep">{art('tulip-bottom','',"width:140px;color:#F3F5F1")}<span class="cap">Cạnh dưới</span></div>
    <div class="board b-deep">{art('tulip-bottom-left','',"width:120px;color:#F3F5F1")}<span class="cap">Góc dưới trái</span></div>
  </div>
  <div class="grid g2" style="margin-top:22px">
    <ul class="rules">
      <li>Đặt sát mép khối kính ngọc lục đậm, như đang mọc vào từ ngoài khung.</li>
      <li>Tối đa ba cụm trong một bố cục; để lại khoảng trống ở giữa.</li>
    </ul>
    <ul class="rules no">
      <li>Đặt trên kính sáng, trên trời hoặc trên cảnh nền hồ Ý.</li>
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
  <p class="lead">Mọi thứ là kính lỏng: trong, viền bắt sáng, bóng đổ mềm, chuyển động đàn hồi. Chiều sâu đến từ ba cấp: tấm, thẻ, giọt. Nguồn: <code>theme.css</code> mục 7 và <code>liquid.js</code>.</p>

  <h3>Ba cấp kính</h3>
  <div class="stage">
    <div class="d-pane">
      <span class="label">Tấm</span>
      <p style="font-size:14px;color:var(--text2);max-width:62ch">Khối nội dung lớn của một mục. Nền <code>--pane</code> (gradient trắng .8 → .66 → .72), <code>backdrop-filter: blur(26px) saturate(1.25) brightness(1.06)</code> (điện thoại blur 16px; chế độ tối: <code>rgba(16,32,46,.78) → rgba(8,20,32,.66) → rgba(14,28,42,.72)</code>, <code>brightness(.8)</code>), bo 40px, viền bắt sáng <code>--rim</code> (bóng trong sáng ở mép trên, dưới và hai bên). Có vệt sáng chạy theo con trỏ: <code>liquid.js</code> đặt <code>--lx</code>, <code>--ly</code>.</p>
      <div class="grid g2" style="margin-top:16px">
        <div class="d-card"><span class="label" style="margin-bottom:4px">Thẻ</span><p style="font-size:13px;color:var(--text2)">Kính mỏng trong tấm, bo 24px. <b>Không</b> làm mờ lần hai — đã nằm trên kính.</p></div>
        <div class="d-card"><span class="label" style="margin-bottom:4px">Thẻ</span><p style="font-size:13px;color:var(--text2)">Rê chuột: nhấc lên 5px, chuyển động đàn hồi <code>cubic-bezier(.2,1.4,.4,1)</code>.</p></div>
      </div>
    </div>
    <div class="d-float" style="margin-top:18px;max-width:460px"><span class="label" style="margin-bottom:4px">Giọt</span><p style="font-size:13px;color:var(--text2)">Thanh menu viên nang (bo 999px), nút, ô tìm kiếm, nhãn lọc. Kính nhẹ hơn nhưng vẫn đục: nền trắng .82 → .6–.66, blur 10–12px, saturate 1.8–1.9. Nhấn thì co lại <code>scale(.96)</code>.</p></div>
  </div>
  <p class="note">Ví dụ dựng trong một khung trời minh hoạ để thấy hiệu ứng mờ. Kính đục hơn bản trước để đọc được trên cảnh nhiều chi tiết; màu pháo bông hắt qua kính tạo <b>ánh ngũ sắc</b> nhẹ — đó là hiệu ứng mong muốn, không phải lỗi. Class dùng lại: <code>.glass</code> (tấm) và <code>.glass-strong</code> (tấm đặc hơn, cho nội dung dài như bài viết).</p>

  <h3>Quả cầu pha lê</h3>
  <div class="stage" style="display:flex;justify-content:center;padding:34px"><div class="crystal">{img('logo-infinity-gold', '', 'Dấu vô cực ánh vàng')}</div></div>
  <p class="note">Đầu trang chủ: viên pha lê kính trong (blur 12px, saturate 1.8) giữ dấu vô cực thân ánh vàng <code>logo-infinity-gold.svg</code>.</p>

  <h3>Thanh menu</h3>
  <div class="stage"><div class="d-nav"><span class="row" style="gap:8px;flex-wrap:nowrap">{img('logo-orb','width:30px','')}<b style="font-family:var(--display);letter-spacing:.14em;font-size:12px">TIMELESS HARMONY</b></span><span class="row" style="gap:8px;flex-wrap:nowrap"><span class="btn btn-p" style="padding:8px 16px;font-size:12px">Bắt đầu</span></span></div>
  <p class="note" style="color:var(--ink)">Thanh kính nổi dạng viên nang: bo 999px, blur 12px, saturate 1.9, cách mép 10px. Điện thoại: chỉ giữ quả cầu.</p></div>

  <h3>Nút</h3>
  <div class="stage"><div class="row"><span class="btn btn-p">Khám phá nhà cung cấp</span><span class="btn btn-s">Lên kế hoạch cùng Harmony AI</span></div></div>
  <p class="note">Nút chính = <b>viên kính ngọc lục</b> (gradient <code>rgba(40,104,76,.94) → rgba(14,50,36,.96)</code>, chữ ngà <code>#FBF7EE</code>, viền vàng mảnh). Nút phụ = <b>kính trong</b> (trắng .66 → .3, viền trắng, blur 12px). Nhấn thì co lại <code>scale(.96)</code>. Mỗi màn hình một nút chính. Nút bo tròn hoàn toàn; chữ 13–14px, đậm 500. Động từ đứng đầu: “Khám phá…”, “Gửi…”, “Lưu…”.</p>

  <h3>Bộ lọc, nhãn, ô nhập</h3>
  <div class="stage"><div class="row"><span class="pill on">Tất cả</span><span class="pill">Nhiếp ảnh &amp; Quay phim</span><span class="pill">Hoa cưới</span><span class="badge">Mới</span><span class="badge">✦ Độc đáo</span><span class="input">Tìm nhiếp ảnh gia, hoa cưới…</span></div></div>
  <p class="note">Nhãn lọc = <b>viên nang kính nhỏ</b> (trắng 62%, blur 10px); nhãn đang chọn dùng gradient ngọc lục. Ô tìm kiếm = <b>viên nang kính trắng 82%</b>, viền bắt sáng.</p>

  <h3>Thẻ nhà cung cấp</h3>
  <div class="grid g2" style="align-items:start">
    <div class="stage" style="padding:18px"><div class="demo-card"><div class="demo-thumb"><span class="badge">Mới</span></div><div class="demo-body"><span class="t-label" style="font-size:10px">Nhiếp ảnh &amp; Quay phim</span><p style="font-weight:500;font-size:15px;margin-top:4px">Ánh Dương Studio</p><p style="font-size:12px;color:var(--text3);margin:0">Sài Gòn</p><div class="demo-foot"><span>Film Analog · Vintage</span><b>Từ 6 triệu</b></div></div></div></div>
    <table>
      <tr><th>Thuộc tính</th><th>Giá trị</th></tr>
      <tr><td>Bo góc</td><td>Tấm 40px (điện thoại 30px) · thẻ 24px · giọt (menu, nút, nhãn lọc, ô tìm kiếm) 999px</td></tr>
      <tr><td>Viền</td><td>1px trắng .8 + viền bắt sáng <code>--rim</code> (tấm, thẻ) </td></tr>
      <tr><td>Bóng đổ</td><td>Mềm, ngả xanh trời: <code>--pane-shadow</code>, <code>--card-shadow</code>, kèm <code>--rim</code></td></tr>
      <tr><td>Khoảng cách</td><td>Bội số của 4: 8 · 12 · 16 · 24 · 32 · 48 · 72; giữa các tấm 22px</td></tr>
      <tr><td>Chuyển động</td><td>Đàn hồi <code>cubic-bezier(.2,1.4,.4,1)</code>, 0,4–0,6 giây; tắt khi người dùng bật “giảm chuyển động”</td></tr>
      <tr><td>Chế độ tối</td><td>“Đêm vườn”: trời <code>#081425</code>, tấm kính tối, chữ <code>#F3F5F1</code>, nhấn champagne <code>#E7CF9B</code>; nút chính gradient champagne <code>#F6E9C6 → #D8BA7A</code>, chữ mực</td></tr>
    </table>
  </div>
  <h3>Đêm vườn</h3>
  <div class="stage night"><div class="d-pane"><span class="label" style="color:#E7CF9B">Chế độ tối</span><p style="font-size:14px;color:#D5DED8;max-width:56ch;margin-bottom:14px">Cùng ba cấp kính, đổi sang kính tối trên trời đêm; nhấn champagne.</p><div class="row"><span class="btn btn-p">Khám phá</span><span class="btn btn-s">Tìm hiểu thêm</span></div></div></div>

  <h3>Quy tắc</h3>
  <ul class="rules">
    <li><b>Không lồng hai lớp làm mờ.</b> Thẻ nằm trong tấm chỉ dùng nền kính mỏng (trắng .58 → .34), không <code>backdrop-filter</code>.</li>
    <li><b>Điện thoại</b> (≤ 640px): giảm blur (<code>--blur</code>), tấm bo 30px, lề hai bên 8px.</li>
    <li><b>Dự phòng:</b> trình duyệt không hỗ trợ <code>backdrop-filter</code> (<code>@supports not</code>), hoặc người dùng bật giảm trong suốt (<code>prefers-reduced-transparency</code>): tấm chuyển sang trắng đặc 90–95%.</li>
    <li><b>Chữ thường</b> trên kính phải đạt tương phản tối thiểu 4,5:1 — xem bảng ở mục 03. Chữ nhỏ chỉ dùng vàng đồng <code>#765225</code>; champagne chỉ để trang trí.</li>
    <li><b>Đổi cảnh nền hoặc độ đục kính (<code>--pane</code>) thì phải đo lại độ tương phản</b> trên vùng kính xấu nhất.</li>
    <li>Không đặt chữ trực tiếp lên cảnh nền; mọi chữ, kể cả khối đầu trang, nằm trong kính.</li>
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
  <p class="lead">Ba mẫu bài đăng vuông cho Instagram: kính nổi trên cảnh vườn. Giữ đúng bố cục; chỉ thay chữ. Chữ luôn nằm trong kính, không đặt lên cảnh nền.</p>
  <div class="grid g3" style="margin-top:28px">
    <div><div class="post"><div class="pg"><blockquote>Đám cưới nhỏ không phải xu hướng — đó là <em>lựa chọn có chủ đích.</em></blockquote><cite>hold us together</cite>{img('logo-orb','','').replace('class="cimg"','class="cimg orb"')}</div></div><p class="note">Trích dẫn · nền ngày</p></div>
    <div><div class="post n"><div class="pg">{img('logo-orb','width:26%;margin-bottom:12px','')}<p class="k">Sắp ra mắt</p><p class="h">Đặt dịch vụ cưới,<br><em>không sợ mất cọc</em></p></div></div><p class="note">Thông báo · nền Đêm vườn</p></div>
    <div><div class="post"><div class="pg" style="justify-content:flex-start"><p class="nm">01 / 05</p><p class="h">Ký quỹ là gì?<br>30 giây để hiểu</p><p class="s">Vuốt để xem tiền của bạn đi đâu →</p>{art('logo-wordmark','f')}</div></div><p class="note">Bìa chuỗi mẹo · nền ngày</p></div>
  </div>
  <h3>Ảnh đại diện &amp; ảnh chia sẻ</h3>
  <ul class="rules">
    <li>Ảnh đại diện mạng xã hội: quả cầu — <code>docs/logo/social/avatar-orb.png</code>, 1080×1080, tràn khung, tự cắt tròn.</li>
    <li>Ảnh xem trước khi chia sẻ link (1200×630): <code>og-image.png</code>.</li>
    <li>Chữ ký email: bản ngang màu <code>docs/logo/png/logo-horizontal-color.png</code>, hiển thị rộng 200px; chữ Be Vietnam Pro 13px màu Mực ngọc lục.</li>
  </ul>
</div></section>

<section id="tep"><div class="wrap">
  <span class="num">10</span>
  <h2>Tệp &amp; <em>việc còn mở</em></h2>
  <h3 style="margin-top:20px">Tệp thương hiệu trong repo</h3>
  <table>
    <tr><th>Tệp</th><th>Dùng cho</th></tr>
    <tr><td><code>assets/brand/logo-orb.svg</code></td><td>Quả cầu kính ngọc lục — logo chính trên màn hình</td></tr>
    <tr><td><code>assets/brand/logo-lockup-color.svg</code> · <code>logo-lockup-color-light.svg</code></td><td>Bản đầy đủ màu: quả cầu + chữ + tagline; bản chữ sáng cho nền tối</td></tr>
    <tr><td><code>assets/brand/logo-horizontal-color.svg</code> · <code>logo-horizontal-color-light.svg</code></td><td>Bản ngang màu; bản chữ sáng cho nền tối</td></tr>
    <tr><td><code>assets/brand/logo-infinity-color.svg</code></td><td>Dấu vô cực màu (thân mực ngọc lục, nụ hồng), đặt trên kính sáng</td></tr>
    <tr><td><code>assets/brand/logo-infinity-gold.svg</code></td><td>Dấu vô cực thân ánh vàng — dùng trong quả cầu pha lê ở đầu trang chủ</td></tr>
    <tr><td><code>assets/brand/logo-lockup.svg</code> · <code>logo-horizontal.svg</code></td><td>Bản đầy đủ và bản ngang một màu</td></tr>
    <tr><td><code>assets/brand/logo-mark.svg</code> · <code>logo-mark-medium.svg</code> · <code>logo-compact.svg</code></td><td>Biểu tượng nét một màu: đầy đủ · nét vừa · thu nhỏ dưới 48px</td></tr>
    <tr><td><code>assets/brand/logo-wordmark.svg</code> · <code>logo-tagline.svg</code> · <code>logo-infinity.svg</code></td><td>Chữ “TIMELESS HARMONY” · “hold us together” · riêng dấu vô cực (một màu)</td></tr>
    <tr><td><code>favicon.svg</code> · <code>apple-touch-icon.png</code></td><td>Biểu tượng trình duyệt và iPhone</td></tr>
    <tr><td><code>assets/bg/scene-day.webp</code> · <code>scene-night.webp</code></td><td>Cảnh lễ cưới bên hồ ở Ý, máy tính 2000×1250, ngày và đêm</td></tr>
    <tr><td><code>assets/bg/scene-day-m.webp</code> · <code>scene-night-m.webp</code></td><td>Bản dọc cho điện thoại, 900×1950</td></tr>
    <tr><td><code>docs/design/build_background.py</code> · <code>render_background.js</code></td><td>Vẽ lại cảnh nền (SVG trung gian trong <code>docs/design/.build/</code>) và xuất bốn tệp WebP</td></tr>
    <tr><td><code>docs/logo/svg/</code> · <code>png/</code> · <code>pdf/</code> · <code>social/</code></td><td>Bộ tệp gửi đối tác, nhà in: bản màu, bản một màu cố định (mực ngọc lục và ngà), PNG nền trong, PDF vector, ảnh đại diện</td></tr>
    <tr><td><code>assets/brand/tulip-*.svg</code></td><td>Bốn cụm tulip nét mảnh (kính xanh đậm, ấn phẩm in)</td></tr>
    <tr><td><code>og-image.png</code></td><td>Ảnh chia sẻ link, 1200×630</td></tr>
    <tr><td><code>theme.css</code></td><td>Màu, phông và chất liệu kính lỏng cho website — nguồn duy nhất; <code>liquid.js</code> cho vệt sáng theo con trỏ</td></tr>
    <tr><td><code>.claude/brand-voice-guidelines.md</code></td><td>Giọng thương hiệu đầy đủ</td></tr>
    <tr><td><code>docs/marketing-playbook.md</code></td><td>Chiến lược và kế hoạch marketing</td></tr>
  </table>
  <p class="note">Các SVG một màu dùng <code>currentColor</code> — tự đổi theo màu chữ nơi đặt nó. Các SVG màu có gradient cố định, không đổi theo chữ.</p>
  <h3>Việc còn mở</h3>
  <ul class="rules">
    <li><b>Duyệt cảnh nền hồ Ý + pháo bông và bản kính lỏng</b> — màu, độ đục, chuyển động.</li>
    <li><b>Ảnh thật</b> của nhà cung cấp và cặp đôi để thay nền màu giữ chỗ.</li>
    <li><b>Ý nghĩa biểu tượng</b> ở mục 01 (kể cả “quả cầu = giọt sương, viên ngọc giữ khoảnh khắc”) cần bạn xác nhận.</li>
    <li><b>In khổ lớn:</b> nếu cần, vẽ lại bốn cụm tulip nét mảnh như đã làm với logo.</li>
  </ul>
</div></section>
</main>

<footer><div class="wrap">{art('logo-wordmark')}<p>hold us together · Brand Guideline 2.2 · Vườn kính · kính lỏng</p></div></footer>
</body>
</html>
'''
open(ROOT + '/docs/brand-guidelines.html', 'w').write(html)
print(len(html) // 1024, 'KB')
