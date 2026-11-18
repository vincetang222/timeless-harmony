"""Dựng docs/brand-guidelines.html (tự chứa, SVG nhúng sẵn).
Chạy: python3 docs/build_brand_guidelines.py .   (từ thư mục gốc repo)"""
import re, sys
ROOT = sys.argv[1] if len(sys.argv) > 1 else '.'
A = ROOT + '/assets/brand/'
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

def swatch(name, vi, hexv, role, dark=False, border=False):
    r, g, b = [int(hexv[k:k+2], 16) for k in (1, 3, 5)]
    return f'''<div class="sw"><div class="sw-chip{' sw-border' if border else ''}" style="background:{hexv};color:{'#E8E2D7' if dark else '#2F3523'}"><span>{hexv}</span></div>
      <p class="sw-name">{vi} <em>{name}</em></p><p class="sw-meta">RGB {r} · {g} · {b}</p><p class="sw-role">{role}</p></div>'''

CONTRAST = [('Rừng trên Vải lanh', '8,1:1', 'AAA', 'Chữ chính'), ('Rừng trên Giấy', '9,9:1', 'AAA', 'Chữ trên thẻ'),
            ('Chữ phụ #434B39 trên Vải lanh', '5,8:1', 'AA', 'Đoạn văn phụ'), ('Chữ mờ #525A48 trên Vải lanh', '4,6:1', 'AA', 'Chú thích, ngày tháng'),
            ('Rêu trên Vải lanh', '4,8:1', 'AA', 'Nhãn, liên kết'), ('Tulip trên Vải lanh', '4,7:1', 'AA', 'Giá, chữ nhấn'),
            ('Vải lanh trên Rừng', '8,1:1', 'AAA', 'Nút chính, khối đảo màu'), ('Tulip sáng #E0A58C trên Rừng', '6,0:1', 'AA', 'Chữ nhấn trên nền tối'),
            ('Xô thơm trên Vải lanh', '2,1:1', '✕', 'Chỉ dùng cho viền, trang trí — không dùng cho chữ')]

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
  --linen:#D6CEC1; --paper:#E8E2D7; --ivory:#F3EEE5; --forest:#2F3523; --moss:#4C5A38; --sage:#8A937C; --tulip:#86432D; --tulip-light:#E0A58C; --night:#1F2618;
  --text2:#434B39; --text3:#525A48; --line:rgba(47,53,35,.16);
  --display:'Philosopher','Be Vietnam Pro',Georgia,serif; --body:'Be Vietnam Pro',system-ui,sans-serif; --serif:'Lora',Georgia,serif;
}}
*,*::before,*::after {{ box-sizing:border-box; margin:0; padding:0; }}
html {{ scroll-behavior:smooth; }}
body {{ font-family:var(--body); background:var(--linen); color:var(--forest); line-height:1.7; font-size:15px; -webkit-font-smoothing:antialiased; }}
a {{ color:inherit; }}
.wrap {{ max-width:1040px; margin:0 auto; padding:0 28px; }}
.art {{ display:block; width:100%; height:auto; }}
.sprite {{ position:absolute; width:0; height:0; overflow:hidden; }}

/* cover */
.cover {{ position:relative; overflow:hidden; min-height:92vh; display:flex; align-items:center; justify-content:center; text-align:center; padding:80px 24px; }}
.cover .c-lockup {{ width:min(380px,70vw); margin:0 auto; }}
.cover .c-tl {{ position:absolute; left:0; top:0; width:min(250px,30vw); }}
.cover .c-r {{ position:absolute; right:0; bottom:7%; width:min(170px,20vw); }}
.cover .c-b {{ position:absolute; left:38%; bottom:0; width:min(260px,30vw); }}
.cover .c-bl {{ position:absolute; left:0; bottom:0; width:min(180px,22vw); }}
.cover-title {{ font-family:var(--display); font-weight:700; letter-spacing:.2em; text-transform:uppercase; font-size:13px; margin-top:34px; }}
.cover-sub {{ font-family:var(--serif); font-style:italic; color:var(--text2); margin-top:6px; }}

/* toc */
.toc {{ position:sticky; top:0; z-index:5; background:rgba(214,206,193,.93); backdrop-filter:blur(10px); border-bottom:.5px solid var(--line); }}
.toc .wrap {{ display:flex; gap:4px; overflow-x:auto; padding-top:10px; padding-bottom:10px; scrollbar-width:none; }}
.toc a {{ text-decoration:none; font-size:12px; white-space:nowrap; padding:6px 12px; border-radius:99px; color:var(--text2); }}
.toc a:hover {{ background:rgba(47,53,35,.08); color:var(--forest); }}

section {{ padding:84px 0; border-bottom:.5px solid var(--line); }}
.num {{ font-family:var(--display); color:var(--tulip); font-size:15px; letter-spacing:.1em; }}
h2 {{ font-family:var(--display); font-weight:400; font-size:clamp(30px,4.4vw,46px); line-height:1.12; margin:6px 0 16px; }}
h2 em {{ font-style:italic; color:var(--tulip); }}
h3 {{ font-family:var(--display); font-weight:700; font-size:20px; margin:44px 0 14px; }}
.lead {{ font-size:17px; color:var(--text2); max-width:62ch; }}
p + p {{ margin-top:10px; }}
.note {{ font-size:13px; color:var(--text3); margin-top:12px; }}
.note b {{ color:var(--tulip); font-weight:600; }}
.grid {{ display:grid; gap:18px; }}
.g2 {{ grid-template-columns:repeat(2,1fr); }} .g3 {{ grid-template-columns:repeat(3,1fr); }} .g4 {{ grid-template-columns:repeat(4,1fr); }}
.grid > * {{ min-width:0; }}
@media (max-width:760px) {{ .g2 {{ grid-template-columns:1fr; }} .g3,.g4 {{ grid-template-columns:1fr 1fr; }} section {{ padding:56px 0; }} .board {{ padding:28px 16px 40px; }} .board .art {{ max-width:100%; }} table {{ display:block; overflow-x:auto; }} }}
@media (max-width:480px) {{ .g3,.g4 {{ grid-template-columns:1fr; }} }}
.card {{ background:var(--paper); border:.5px solid var(--line); border-radius:18px; padding:26px; }}
.card h4 {{ font-family:var(--display); font-weight:700; font-size:17px; margin-bottom:6px; }}
.card p {{ font-size:14px; color:var(--text2); }}
.label {{ font-size:10px; font-weight:600; letter-spacing:.16em; text-transform:uppercase; color:var(--moss); margin-bottom:10px; display:block; }}

/* logo boards */
.board {{ border-radius:18px; display:flex; align-items:center; justify-content:center; padding:36px; min-height:230px; position:relative; border:.5px solid var(--line); }}
.board .cap {{ position:absolute; left:16px; bottom:12px; font-size:11px; opacity:.7; }}
.b-linen {{ background:var(--linen); }} .b-paper {{ background:var(--paper); }} .b-forest {{ background:var(--forest); color:var(--linen); border:none; }} .b-night {{ background:var(--night); color:var(--linen); border:none; }}
.clear {{ outline:1px dashed var(--tulip); outline-offset:26px; }}
.dont {{ min-height:170px; padding:22px; overflow:hidden; }}
.dont::after {{ content:'✕'; position:absolute; right:12px; top:8px; color:var(--tulip); font-weight:700; }}
.dont .art {{ width:120px; }}

/* colours */
.sw-chip {{ height:132px; border-radius:16px; display:flex; align-items:flex-end; padding:12px 14px; font-size:13px; font-weight:600; letter-spacing:.04em; }}
.sw-border {{ border:.5px solid var(--line); }}
.sw-name {{ font-family:var(--display); font-weight:700; font-size:17px; margin-top:10px; }}
.sw-name em {{ font-family:var(--body); font-style:normal; font-weight:400; font-size:12px; color:var(--text3); margin-left:4px; }}
.sw-meta {{ font-size:12px; color:var(--text3); margin-top:0; }}
.sw-role {{ font-size:13px; color:var(--text2); margin-top:4px; line-height:1.5; }}
.ratio {{ display:flex; height:54px; border-radius:14px; overflow:hidden; margin-top:8px; font-size:12px; font-weight:600; }}
.ratio div {{ display:flex; align-items:center; justify-content:center; }}
table {{ width:100%; border-collapse:collapse; font-size:14px; margin-top:8px; }}
th {{ text-align:left; font-size:10px; letter-spacing:.14em; text-transform:uppercase; color:var(--text3); font-weight:600; padding:10px 12px; border-bottom:.5px solid var(--line); }}
td {{ padding:11px 12px; border-bottom:.5px solid var(--line); vertical-align:top; }}
td code, p code, li code {{ font-family:ui-monospace,Menlo,monospace; font-size:12.5px; background:rgba(47,53,35,.08); padding:1px 6px; border-radius:5px; }}
.pass {{ color:var(--moss); font-weight:600; }} .fail {{ color:var(--tulip); font-weight:600; }}
.tints {{ display:grid; grid-template-columns:repeat(8,1fr); gap:8px; }}
.tints div {{ height:64px; border-radius:12px; font-size:10px; display:flex; align-items:flex-end; padding:7px; color:var(--text2); }}
@media (max-width:760px) {{ .tints {{ grid-template-columns:repeat(4,1fr); }} }}

/* type */
.spec {{ display:grid; grid-template-columns:150px 1fr; gap:20px; padding:22px 0; border-bottom:.5px solid var(--line); align-items:baseline; }}
.spec small {{ font-size:11px; color:var(--text3); line-height:1.5; display:block; }}
@media (max-width:640px) {{ .spec {{ grid-template-columns:1fr; gap:6px; }} }}
.t-display {{ font-family:var(--display); font-weight:700; font-size:clamp(34px,5.4vw,62px); line-height:1.05; }}
.t-display em, .t-h2 em {{ font-style:italic; font-weight:400; color:var(--tulip); }}
.t-h2 {{ font-family:var(--display); font-weight:400; font-size:34px; line-height:1.15; }}
.t-h3 {{ font-family:var(--display); font-weight:700; font-size:20px; }}
.t-eyebrow {{ font-family:var(--serif); font-style:italic; font-size:18px; color:var(--text2); }}
.t-body {{ font-size:16px; color:var(--text2); max-width:60ch; }}
.t-label {{ font-size:11px; font-weight:600; letter-spacing:.16em; text-transform:uppercase; color:var(--moss); }}
.glyphs {{ font-family:var(--display); font-size:26px; line-height:1.5; word-break:break-word; }}

/* components */
.row {{ display:flex; flex-wrap:wrap; gap:10px; align-items:center; }}
.btn {{ font:500 14px var(--body); padding:12px 24px; border-radius:999px; border:.5px solid transparent; cursor:default; }}
.btn-p {{ background:var(--forest); color:var(--paper); }} .btn-s {{ background:transparent; color:var(--forest); border-color:rgba(47,53,35,.3); }}
.btn-i {{ background:var(--linen); color:var(--forest); }} .btn-io {{ background:transparent; color:var(--linen); border-color:var(--linen); }}
.pill {{ font-size:12px; padding:7px 16px; border-radius:99px; border:.5px solid rgba(47,53,35,.26); color:var(--text3); }}
.pill.on {{ background:var(--forest); color:var(--paper); border-color:var(--forest); }}
.badge {{ font-size:9px; font-weight:600; letter-spacing:.12em; text-transform:uppercase; padding:4px 10px; border-radius:99px; background:rgba(76,90,56,.1); color:var(--moss); border:.5px solid rgba(76,90,56,.3); }}
.input {{ font:400 14px var(--body); background:var(--ivory); border:.5px solid rgba(47,53,35,.26); border-radius:999px; padding:12px 20px; color:var(--text3); min-width:240px; }}
.demo-card {{ background:var(--paper); border:.5px solid var(--line); border-radius:14px; overflow:hidden; max-width:300px; }}
.demo-thumb {{ height:140px; background:#C3CBB6; display:flex; align-items:flex-start; padding:12px; }}
.demo-body {{ padding:16px; }}
.demo-body .t-label {{ font-size:10px; }}
.demo-foot {{ display:flex; justify-content:space-between; font-size:12px; color:var(--text3); border-top:.5px solid var(--line); margin-top:12px; padding-top:12px; }}
.demo-foot b {{ color:var(--tulip); font-weight:500; }}

/* voice */
.vs td:first-child {{ font-weight:600; width:34%; }}
.eg {{ border-left:2px solid var(--moss); padding:4px 0 4px 16px; margin-top:12px; font-size:14px; color:var(--text2); }}
.eg.bad {{ border-color:var(--tulip); }}
.eg b {{ display:block; font-size:10px; letter-spacing:.14em; text-transform:uppercase; margin-bottom:3px; color:var(--moss); }}
.eg.bad b {{ color:var(--tulip); }}

/* social mock-ups */
.post {{ aspect-ratio:1/1; border-radius:6px; position:relative; overflow:hidden; display:flex; flex-direction:column; justify-content:center; padding:11%; }}
.post .art {{ position:absolute; }}
.post-q {{ background:var(--linen); border:.5px solid var(--line); }}
.post-q blockquote {{ font-family:var(--display); font-size:clamp(17px,2.3vw,25px); line-height:1.25; }}
.post-q blockquote em {{ color:var(--tulip); }}
.post-q cite {{ font-family:var(--serif); font-size:12px; color:var(--text3); margin-top:14px; }}
.post-a {{ background:var(--forest); color:var(--linen); text-align:center; align-items:center; }}
.post-a p.k {{ font-size:10px; letter-spacing:.2em; text-transform:uppercase; opacity:.75; }}
.post-a p.h {{ font-family:var(--display); font-size:clamp(20px,2.8vw,30px); line-height:1.15; margin:8px 0; }}
.post-a p.h em {{ font-style:italic; color:var(--tulip-light); }}
.post-t {{ background:var(--paper); border:.5px solid var(--line); justify-content:flex-start; }}
.post-t .n {{ font-family:var(--display); color:var(--tulip); font-size:15px; }}
.post-t .h {{ font-family:var(--display); font-weight:700; font-size:clamp(18px,2.5vw,27px); line-height:1.15; margin-top:8px; }}
.post-t .s {{ font-size:12px; color:var(--text2); margin-top:10px; }}
.post-t .f {{ position:absolute; left:11%; bottom:8%; width:42%; }}

ul.rules {{ list-style:none; }}
ul.rules li {{ padding:9px 0 9px 26px; position:relative; border-bottom:.5px solid var(--line); font-size:14px; color:var(--text2); }}
ul.rules li::before {{ content:'—'; position:absolute; left:0; color:var(--moss); }}
ul.rules.no li::before {{ content:'✕'; color:var(--tulip); font-size:12px; top:11px; }}
footer {{ padding:56px 0 72px; text-align:center; color:var(--text3); font-size:12px; }}
footer .art {{ width:150px; margin:0 auto 10px; color:var(--forest); }}
@media print {{ .toc {{ display:none; }} section {{ break-inside:avoid; }} }}
</style>
</head>
<body>
<svg class="sprite" aria-hidden="true">{''.join(symbols)}</svg>

<header class="cover">
  {art('tulip-top-left','c-tl')}{art('tulip-right','c-r')}{art('tulip-bottom','c-b')}{art('tulip-bottom-left','c-bl')}
  <div>
    {art('logo-lockup','c-lockup')}
    <p class="cover-title">Brand Guideline</p>
    <p class="cover-sub">Phiên bản 1.1 · tháng 11, 2026</p>
  </div>
</header>

<nav class="toc"><div class="wrap">
  <a href="#cot-loi">01 Cốt lõi</a><a href="#logo">02 Logo</a><a href="#mau">03 Màu sắc</a><a href="#chu">04 Kiểu chữ</a>
  <a href="#tulip">05 Hình vẽ tulip</a><a href="#anh">06 Hình ảnh</a><a href="#giao-dien">07 Giao diện</a><a href="#giong">08 Giọng nói</a>
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
  <div class="grid g3">
    <div class="card"><h4>Vô cực</h4><p>Tình yêu không có điểm kết — <i>timeless</i>.</p></div>
    <div class="card"><h4>Hai nụ tulip</h4><p>Hai người trên cùng một đường — <i>harmony</i>. Tulip là loài hoa của tình yêu trọn vẹn.</p></div>
    <div class="card"><h4>Vòng tròn T · H</h4><p>Chiếc nhẫn và sự trọn vẹn; hai chữ cái đầu ở hai bên, mở ra chứ không khép kín.</p></div>
  </div>
  <p class="note"><b>Cần xác nhận:</b> đây là diễn giải đề xuất từ artwork gốc. Nếu ý nghĩa ban đầu của bạn khác, hãy sửa ở đây để mọi nội dung kể cùng một câu chuyện.</p>
</div></section>

<section id="logo"><div class="wrap">
  <span class="num">02</span>
  <h2>Logo</h2>
  <p class="lead">Logo được vẽ lại thành vector từ artwork gốc. Có một bản đầy đủ, một bản ngang, logo chữ và ba cỡ biểu tượng. Chọn theo kích thước hiển thị; không tự vẽ lại hay sắp xếp lại các thành phần.</p>
  <div class="grid g2" style="margin-top:30px">
    <div class="board b-linen">{art('logo-lockup','',"width:210px")}<span class="cap">Bản đầy đủ — ưu tiên dùng</span></div>
    <div class="board b-linen">{art('logo-horizontal','',"width:min(340px,100%)")}<span class="cap">Bản ngang — chữ ký email, tiêu đề tài liệu, bìa hồ sơ</span></div>
    <div class="board b-linen"><div style="width:270px">{art('logo-wordmark')}{art('logo-tagline','',"width:52%;margin:8px auto 0")}</div><span class="cap">Logo chữ + tagline — chân trang, khi biểu tượng đã có ở chỗ khác</span></div>
    <div class="board b-linen"><div class="row" style="gap:22px;align-items:center">{art('logo-mark','',"width:120px")}{art('logo-mark-medium','',"width:72px")}{art('logo-compact','',"width:32px")}</div><span class="cap">Biểu tượng theo cỡ — đầy đủ · nét vừa · thu nhỏ</span></div>
  </div>

  <h3>Cấu trúc biểu tượng</h3>
  <div class="grid g2">
    <div class="board b-paper" style="min-height:230px">{art('logo-infinity','',"width:min(300px,100%)")}<span class="cap">Một nét liền, không cắt nhau — hai đầu nét nở thành hai nụ tulip</span></div>
    <ul class="rules" style="margin:0">
      <li><b>Dấu vô cực</b> là một nét duy nhất: mảnh ở hai nụ, đầy dần về giữa. Hình đối xứng khi xoay 180°.</li>
      <li><b>Hai nụ tulip</b> giống hệt nhau, mỗi nụ có hai cánh ngoài và một cánh giữa ló ra phía sau.</li>
      <li><b>Vòng tròn</b> ngắt ở hai bên cho chữ <b>T</b> và <b>H</b>. Nét đứng của T, H bằng độ dày vòng tròn; nét ngang bằng nét cánh hoa.</li>
      <li><b>Chữ logo</b>: Belleza làm đậm nhẹ (khớp artwork gốc). <b>Tagline</b>: Lora 540. Cả hai đã chuyển thành đường nét, không cần cài phông.</li>
      <li>Tệp nguồn dựng logo: <code>docs/logo/build_logo.py</code>. Sửa thông số ở đầu tệp rồi chạy lại, không sửa SVG bằng tay.</li>
    </ul>
  </div>

  <h3>Trên nền nào</h3>
  <div class="grid g4">
    <div class="board b-linen" style="min-height:170px">{art('logo-mark','',"width:110px")}<span class="cap">Vải lanh ✓</span></div>
    <div class="board b-paper" style="min-height:170px">{art('logo-mark','',"width:110px")}<span class="cap">Giấy ✓</span></div>
    <div class="board b-forest" style="min-height:170px">{art('logo-mark','',"width:110px")}<span class="cap">Rừng ✓</span></div>
    <div class="board b-night" style="min-height:170px">{art('logo-mark','',"width:110px")}<span class="cap">Rừng đêm ✓</span></div>
  </div>
  <p class="note">Logo chỉ có một màu: <b>Rừng</b> trên nền sáng, <b>Vải lanh</b> trên nền tối. Trên ảnh chụp: đặt logo trong một mảng màu đặc, không đặt trực tiếp lên ảnh.</p>

  <h3>Vùng an toàn &amp; kích thước tối thiểu</h3>
  <div class="grid g2">
    <div class="board b-paper" style="min-height:300px">{art('logo-lockup','clear',"width:170px")}<span class="cap">Khoảng trống quanh logo ≥ chiều cao chữ “H” trong vòng tròn × 2</span></div>
    <div class="card"><table>
      <tr><th>Phiên bản</th><th>Màn hình</th><th>In ấn</th></tr>
      <tr><td>Bản đầy đủ</td><td>≥ 150 px rộng</td><td>≥ 32 mm</td></tr>
      <tr><td>Bản ngang</td><td>≥ 200 px rộng</td><td>≥ 45 mm</td></tr>
      <tr><td>Logo chữ</td><td>≥ 100 px rộng</td><td>≥ 25 mm</td></tr>
      <tr><td>Biểu tượng đầy đủ</td><td>≥ 120 px</td><td>≥ 25 mm</td></tr>
      <tr><td>Biểu tượng nét vừa</td><td>48–120 px</td><td>12–25 mm</td></tr>
      <tr><td>Bản thu nhỏ</td><td>16–48 px</td><td>6–12 mm</td></tr>
    </table><p class="note">Nhỏ hơn 120px thì vòng tròn mảnh và chữ T, H bị mất: chuyển sang bản nét vừa. Nhỏ hơn 48px: dùng bản thu nhỏ.</p></div>
  </div>

  <h3>Không làm</h3>
  <div class="grid g3">
    <div class="board b-paper dont">{art('logo-mark','',"transform:scaleX(1.5)")}<span class="cap">Kéo giãn, bóp méo</span></div>
    <div class="board b-paper dont">{art('logo-mark','',"color:#C2185B")}<span class="cap">Đổi sang màu ngoài bảng màu</span></div>
    <div class="board dont" style="background:repeating-linear-gradient(45deg,#b9a98f 0 12px,#8a937c 12px 24px)">{art('logo-mark')}<span class="cap" style="color:#fff">Đặt trên nền rối, ảnh nhiều chi tiết</span></div>
    <div class="board b-paper dont">{art('logo-mark','',"filter:drop-shadow(4px 5px 3px rgba(0,0,0,.45))")}<span class="cap">Thêm bóng đổ, viền, hiệu ứng</span></div>
    <div class="board b-paper dont">{art('logo-mark','',"transform:rotate(-18deg)")}<span class="cap">Xoay, nghiêng</span></div>
    <div class="board b-paper dont">{art('logo-mark','',"width:34px")}<span class="cap">Dùng biểu tượng đầy đủ ở kích thước quá nhỏ</span></div>
  </div>
</div></section>

<section id="mau"><div class="wrap">
  <span class="num">03</span>
  <h2>Màu <em>sắc</em></h2>
  <p class="lead">Bảng màu lấy trực tiếp từ artwork gốc: vải lanh ấm và mực xanh rừng. Thương hiệu gần như hai màu — sự tiết chế chính là nét sang.</p>
  <h3>Màu chính</h3>
  <div class="grid g4">
    {swatch('Linen','Vải lanh','#D6CEC1','Nền chính của mọi thứ. Lấy từ artwork gốc.',border=True)}
    {swatch('Forest','Rừng','#2F3523','Chữ, logo, nét vẽ, nút chính. Lấy từ artwork gốc.',dark=True)}
    {swatch('Paper','Giấy','#E8E2D7','Thẻ, bề mặt nổi trên nền vải lanh.',border=True)}
    {swatch('Ivory','Ngà','#F3EEE5','Ô nhập liệu; điểm sáng nhất.',border=True)}
  </div>
  <h3>Màu bổ trợ</h3>
  <div class="grid g4">
    {swatch('Moss','Rêu','#4C5A38','Icon, nhãn, liên kết.',dark=True)}
    {swatch('Sage','Xô thơm','#8A937C','Viền, chi tiết trang trí. Không dùng cho chữ.',dark=True)}
    {swatch('Tulip','Tulip','#86432D','Điểm nhấn ấm: chữ nghiêng trong tiêu đề, giá. Dùng tiết chế.',dark=True)}
    {swatch('Night','Rừng đêm','#1F2618','Nền của chế độ tối.',dark=True)}
  </div>
  <h3>Tỷ lệ sử dụng</h3>
  <div class="ratio"><div style="flex:60;background:var(--linen);border:.5px solid var(--line)">Vải lanh &amp; Giấy · 60%</div><div style="flex:30;background:var(--forest);color:var(--linen)">Rừng · 30%</div><div style="flex:10;background:var(--tulip);color:var(--paper)">Tulip ≤ 10%</div></div>
  <p class="note">Mỗi màn hình hoặc mỗi bài đăng chỉ nên có <b>một</b> chỗ dùng màu Tulip.</p>

  <h3>Độ tương phản (WCAG 2.1)</h3>
  <table><tr><th>Cặp màu</th><th>Tỷ lệ</th><th>Mức</th><th>Dùng cho</th></tr>
  {''.join(f'<tr><td>{a}</td><td>{b}</td><td class="{"fail" if c=="✕" else "pass"}">{c}</td><td>{d}</td></tr>' for a,b,c,d in CONTRAST)}
  </table>

  <h3>Màu theo hạng mục dịch vụ</h3>
  <p style="color:var(--text2);font-size:14px;max-width:70ch">Dùng làm nền giữ chỗ khi chưa có ảnh và để phân biệt hạng mục. Tất cả cùng độ sáng, độ bão hòa thấp để không cạnh tranh với màu chính.</p>
  <div class="tints" style="margin-top:14px">
    <div style="background:#DBCFB6">Kế hoạch</div><div style="background:#C3CBB6">Nhiếp ảnh</div><div style="background:#DFC7BC">Hoa</div><div style="background:#DCC6C6">Làm đẹp</div>
    <div style="background:#CBC8CF">Âm nhạc</div><div style="background:#DDD0B0">Ẩm thực</div><div style="background:#C2CDC9">Địa điểm</div><div style="background:#D9C1AD">Độc đáo</div>
  </div>
</div></section>

<section id="chu"><div class="wrap">
  <span class="num">04</span>
  <h2>Kiểu <em>chữ</em></h2>
  <p class="lead">Ba phông, ba vai trò. Cả ba đều miễn phí trên Google Fonts và hiển thị đầy đủ dấu tiếng Việt.</p>
  <div class="grid g3" style="margin-top:30px">
    <div class="card"><span class="label">Tiêu đề</span><p style="font-family:var(--display);font-size:40px;line-height:1.1;color:var(--forest)">Philosopher</p><p style="margin-top:8px">Phông của artwork gốc. Dùng 700 cho tiêu đề lớn, 400 cho tiêu đề phụ, <i>nghiêng</i> cho chữ nhấn.</p></div>
    <div class="card"><span class="label">Giao diện &amp; đoạn văn</span><p style="font-family:var(--body);font-size:34px;font-weight:500;line-height:1.1;color:var(--forest)">Be Vietnam Pro</p><p style="margin-top:8px">Thiết kế riêng cho tiếng Việt. 400 cho văn bản, 500–600 cho nút và nhãn.</p></div>
    <div class="card"><span class="label">Tagline &amp; trích dẫn</span><p style="font-family:var(--serif);font-size:40px;font-style:italic;line-height:1.1;color:var(--forest)">Lora</p><p style="margin-top:8px">Dùng nghiêng cho tagline, lời dẫn, trích dẫn. Không dùng cho tiêu đề chính.</p></div>
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
    <li>Chữ nhấn trong tiêu đề: đặt trong thẻ <code>&lt;em&gt;</code> — tự động thành Philosopher nghiêng, màu Tulip. Mỗi tiêu đề chỉ nhấn một cụm.</li>
    <li>Không viết HOA toàn bộ tiêu đề tiếng Việt (dấu chồng lên nhau, khó đọc). Chữ hoa chỉ dùng cho nhãn ngắn.</li>
    <li>Chiều dài dòng văn bản: 55–70 ký tự. Căn trái; không căn đều hai bên.</li>
    <li>Chữ trong logo “TIMELESS HARMONY” là hình vẽ, không gõ lại bằng phông.</li>
  </ul>
  <h3>Kiểm tra dấu tiếng Việt</h3>
  <p class="glyphs">Ầ Ẩ Ẫ Ậ Ắ Ằ Ẳ Ẵ Ặ Đ Ễ Ệ Ỗ Ộ Ờ Ở Ỡ Ợ Ữ Ự ỳ ỷ ỹ ỵ<br><span style="font-style:italic">Giữ chúng mình bên nhau — những điều nhỏ, thật lòng</span></p>
</div></section>

<section id="tulip"><div class="wrap">
  <span class="num">05</span>
  <h2>Hình vẽ <em>tulip</em></h2>
  <p class="lead">Tulip nét mảnh là dấu hiệu nhận biết thứ hai sau logo. Có bốn cụm, tách từ artwork gốc thành vector — đủ nét cho web; khi cần in khổ lớn nên vẽ lại như logo.</p>
  <div class="grid g4" style="margin-top:30px;align-items:end">
    <div class="board b-paper">{art('tulip-top-left','',"width:120px")}<span class="cap">Góc trên trái</span></div>
    <div class="board b-paper">{art('tulip-right','',"width:120px")}<span class="cap">Cạnh phải</span></div>
    <div class="board b-paper">{art('tulip-bottom','',"width:150px")}<span class="cap">Cạnh dưới</span></div>
    <div class="board b-paper">{art('tulip-bottom-left','',"width:130px")}<span class="cap">Góc dưới trái</span></div>
  </div>
  <div class="grid g2" style="margin-top:26px">
    <div><h3 style="margin-top:0">Nên</h3><ul class="rules">
      <li>Đặt sát mép, như đang mọc vào từ ngoài khung — đúng vị trí tên gọi của từng cụm.</li>
      <li>Một màu duy nhất: Rừng trên nền sáng, Vải lanh trên nền tối.</li>
      <li>Làm nền chìm phía sau chữ: giảm độ đậm còn 15–25%.</li>
      <li>Tối đa ba cụm trong một bố cục; để lại khoảng trống ở giữa.</li>
    </ul></div>
    <div><h3 style="margin-top:0">Không</h3><ul class="rules no">
      <li>Tô màu bên trong cánh hoa, dùng chuyển sắc.</li>
      <li>Đặt lơ lửng giữa trang, tách khỏi mép.</li>
      <li>Lật, xoay tới mức thân hoa hướng ngược tự nhiên.</li>
      <li>Trộn với hình vẽ hoa kiểu khác hoặc icon hoa có sẵn.</li>
    </ul></div>
  </div>
</div></section>

<section id="anh"><div class="wrap">
  <span class="num">06</span>
  <h2>Hình <em>ảnh</em></h2>
  <p class="lead">Ảnh phải giống như được chụp bởi một người bạn có mắt nhìn — không phải ảnh quảng cáo.</p>
  <div class="grid g2" style="margin-top:26px">
    <div><h3 style="margin-top:0">Hướng tới</h3><ul class="rules">
      <li>Ánh sáng tự nhiên; tông ấm, trầm; hợp với nền vải lanh.</li>
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
  <p class="lead">Hình khối mềm, viền mảnh, không đổ bóng. Chiều sâu đến từ ba lớp màu: Vải lanh → Giấy → Ngà.</p>
  <h3>Nút</h3>
  <div class="row"><span class="btn btn-p">Khám phá nhà cung cấp</span><span class="btn btn-s">Lên kế hoạch cùng Harmony AI</span></div>
  <div class="board b-forest" style="min-height:0;padding:22px;justify-content:flex-start;margin-top:12px"><div class="row"><span class="btn btn-i">Bắt đầu ngay</span><span class="btn btn-io">Tôi là nhà cung cấp</span></div></div>
  <p class="note">Mỗi màn hình một nút chính. Nút bo tròn hoàn toàn; chữ 13–14px, đậm 500. Động từ đứng đầu: “Khám phá…”, “Gửi…”, “Lưu…”.</p>
  <h3>Bộ lọc, nhãn, ô nhập</h3>
  <div class="row"><span class="pill on">Tất cả</span><span class="pill">Nhiếp ảnh &amp; Quay phim</span><span class="pill">Hoa cưới</span><span class="badge">Mới</span><span class="badge">✦ Độc đáo</span><span class="input">Tìm nhiếp ảnh gia, hoa cưới…</span></div>
  <h3>Thẻ</h3>
  <div class="grid g2" style="align-items:start">
    <div class="demo-card"><div class="demo-thumb"><span class="badge">Mới</span></div><div class="demo-body"><span class="t-label">Nhiếp ảnh &amp; Quay phim</span><p style="font-weight:500;font-size:15px;margin-top:4px">Ánh Dương Studio</p><p style="font-size:12px;color:var(--text3);margin:0">Sài Gòn</p><div class="demo-foot"><span>Film Analog · Vintage</span><b>Từ 6 triệu</b></div></div></div>
    <table>
      <tr><th>Thuộc tính</th><th>Giá trị</th></tr>
      <tr><td>Bo góc</td><td>Thẻ 14px · khối lớn 28px · nút và ô nhập bo tròn</td></tr>
      <tr><td>Viền</td><td>0,5px, Rừng 14–26%</td></tr>
      <tr><td>Bóng đổ</td><td>Không dùng</td></tr>
      <tr><td>Khoảng cách</td><td>Bội số của 4: 8 · 12 · 16 · 24 · 32 · 48 · 72</td></tr>
      <tr><td>Chuyển động</td><td>Nhẹ, 0,2–0,6 giây; tắt khi người dùng bật “giảm chuyển động”</td></tr>
      <tr><td>Chế độ tối</td><td>“Rừng đêm”: nền <code>#1F2618</code>, chữ <code>#E6DFD2</code>; khối đảo màu thành Vải lanh</td></tr>
    </table>
  </div>
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
  <p class="lead">Ba mẫu bài đăng vuông cho Instagram. Giữ đúng bố cục; chỉ thay chữ.</p>
  <div class="grid g3" style="margin-top:28px">
    <div><div class="post post-q">{art('tulip-top-left','',"width:34%;left:0;top:0;opacity:.2")}<blockquote>Đám cưới nhỏ không phải xu hướng — đó là <em>lựa chọn có chủ đích.</em></blockquote><cite>hold us together</cite>{art('logo-compact','',"width:9%;right:8%;bottom:7%")}</div><p class="note">Trích dẫn · nền Vải lanh</p></div>
    <div><div class="post post-a">{art('tulip-bottom','',"width:52%;left:24%;bottom:0;opacity:.3")}{art('logo-mark-medium','',"position:static;width:30%;margin-bottom:12px")}<p class="k">Sắp ra mắt</p><p class="h">Đặt dịch vụ cưới,<br><em>không sợ mất cọc</em></p></div><p class="note">Thông báo · nền Rừng</p></div>
    <div><div class="post post-t">{art('tulip-right','',"width:30%;right:0;bottom:6%;opacity:.85")}<p class="n">01 / 05</p><p class="h">Ký quỹ là gì?<br>30 giây để hiểu</p><p class="s">Vuốt để xem tiền của bạn đi đâu →</p>{art('logo-wordmark','f')}</div><p class="note">Bìa chuỗi mẹo · nền Giấy</p></div>
  </div>
  <h3>Ảnh đại diện &amp; ảnh chia sẻ</h3>
  <ul class="rules">
    <li>Ảnh đại diện mạng xã hội: <code>docs/logo/social/avatar-linen.png</code> (Rừng trên Vải lanh) hoặc <code>avatar-forest.png</code> (Ngà trên Rừng), 1080×1080, đã chừa lề cho khung cắt tròn.</li>
    <li>Ảnh xem trước khi chia sẻ link (1200×630): <code>og-image.png</code>.</li>
    <li>Chữ ký email: bản ngang <code>docs/logo/png/logo-horizontal-forest.png</code>, hiển thị rộng 200px; chữ Be Vietnam Pro 13px màu Rừng.</li>
  </ul>
</div></section>

<section id="tep"><div class="wrap">
  <span class="num">10</span>
  <h2>Tệp &amp; <em>việc còn mở</em></h2>
  <h3 style="margin-top:20px">Tệp thương hiệu trong repo</h3>
  <table>
    <tr><th>Tệp</th><th>Dùng cho</th></tr>
    <tr><td><code>assets/brand/logo-lockup.svg</code></td><td>Bản đầy đủ: biểu tượng + chữ + tagline</td></tr>
    <tr><td><code>assets/brand/logo-horizontal.svg</code></td><td>Bản ngang: biểu tượng nét vừa + chữ + tagline</td></tr>
    <tr><td><code>assets/brand/logo-mark.svg</code> · <code>logo-mark-medium.svg</code></td><td>Biểu tượng đầy đủ · nét vừa</td></tr>
    <tr><td><code>assets/brand/logo-compact.svg</code> · <code>favicon.svg</code> · <code>apple-touch-icon.png</code></td><td>Bản thu nhỏ dưới 48px, biểu tượng trình duyệt và iPhone</td></tr>
    <tr><td><code>assets/brand/logo-wordmark.svg</code> · <code>logo-tagline.svg</code> · <code>logo-infinity.svg</code></td><td>Chữ “TIMELESS HARMONY” · “hold us together” · riêng dấu vô cực</td></tr>
    <tr><td><code>docs/logo/svg/</code> · <code>png/</code> · <code>pdf/</code> · <code>social/</code></td><td>Bộ tệp gửi đối tác, nhà in: màu cố định Rừng và Ngà, PNG nền trong, PDF vector, ảnh đại diện</td></tr>
    <tr><td><code>assets/brand/tulip-*.svg</code></td><td>Bốn cụm tulip</td></tr>
    <tr><td><code>theme.css</code></td><td>Mã màu và phông cho website — nguồn duy nhất</td></tr>
    <tr><td><code>.claude/brand-voice-guidelines.md</code></td><td>Giọng thương hiệu đầy đủ</td></tr>
    <tr><td><code>docs/marketing-playbook.md</code></td><td>Chiến lược và kế hoạch marketing</td></tr>
  </table>
  <p class="note">Mọi tệp SVG dùng <code>currentColor</code> — tự đổi theo màu chữ nơi đặt nó.</p>
  <h3>Việc còn mở</h3>
  <ul class="rules">
    <li><b style="color:var(--tulip)">Duyệt bản vẽ lại.</b> Logo đã được vẽ lại thành vector (tháng 11, 2026), giữ nguyên bố cục artwork gốc. Khác biệt có chủ đích: hai nụ tulip giống hệt nhau, chữ T, H nằm đúng giữa vòng tròn, độ dày nét vô cực đối xứng. Bạn xem lại và báo nếu muốn giữ chi tiết nào của bản vẽ tay.</li>
    <li><b style="color:var(--tulip)">Ý nghĩa biểu tượng</b> ở mục 01 cần bạn xác nhận.</li>
    <li><b style="color:var(--tulip)">Ảnh thật</b> của nhà cung cấp và cặp đôi để thay nền màu giữ chỗ.</li>
    <li><b style="color:var(--tulip)">Màu Tulip</b> là đề xuất mới (artwork gốc chỉ có hai màu). Nếu muốn thương hiệu thuần hai màu, đổi biến <code>--th-tulip</code> trong <code>theme.css</code> thành <code>#4C5A38</code>.</li>
  </ul>
</div></section>
</main>

<footer><div class="wrap">{art('logo-wordmark')}<p>hold us together · Brand Guideline 1.1</p></div></footer>
</body>
</html>
'''
open(ROOT + '/docs/brand-guidelines.html', 'w').write(html)
print(len(html) // 1024, 'KB')
