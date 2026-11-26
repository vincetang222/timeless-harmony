# Tự vẽ bằng 3D (0 lượt), ngày 26/11: bàn cô dâu chú rể cho phần Tiệc (bo-cuc-canh.md luật 7).
# Bàn dài 1,6 × 0,7 m phủ khăn chấm đất (cùng kiểu khăn với ban_dai_3d.py), không ghế: cặp đôi đứng sau bàn nên ghế bị che hết.
# Bản chơi đặt bàn ngay trước chỗ cặp đôi đứng, che từ thắt lưng xuống; khăn đổi màu theo khăn nền như bàn khách.
# Chạy: GOC_3D=10 <venv có bpy>/bin/python ban_doi_3d.py <thư mục ra>  → ban-doi.png, -id.png, -uv.png, ban-doi.json
# Đưa vào trang thử: DOI_3D=<thư mục ra> python3 xuat_lab.py … doi
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
import xuong_3d as X
from ban_dai_3d import khan_dai

RA = sys.argv[-1] if len(sys.argv) > 1 and not sys.argv[-1].endswith('.py') else '.'
os.makedirs(RA, exist_ok=True)
DAI, RONG = 1.6, 0.7
sc = X.moi(); X.ID.clear()
vai = X.vat_lieu('khan', (0.94, 0.92, 0.87), 0.85, (1, 0, 0))
khan, cao = khan_dai(DAI, RONG, vai, seed=3)
m = X.may_anh(sc)
X.ve(sc, os.path.join(RA, 'ban-doi'), uv_vat=khan)
m.update(dai=DAI, rong=RONG, khach=2, xoay_do=0, khan_uv_cao=round(cao, 4))
json.dump({'ban-doi': m}, open(os.path.join(RA, 'ban-doi.json'), 'w'), ensure_ascii=False, indent=1)
print('ban-doi', m)
