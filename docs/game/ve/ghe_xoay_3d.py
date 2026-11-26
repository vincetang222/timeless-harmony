# Tự vẽ bằng 3D (0 lượt), ngày 26/11: ghế chiavari của bộ bàn (xuong_3d.ghe_chiavari) ở 16 hướng, để bản chơi xếp ghế dự lễ
# theo hàng thẳng, hàng cong, khối chéo, vòng tròn. Cùng máy ảnh trực giao chếch 15°, 260 px mỗi mét như bàn ghế.
# Hướng k: ghế quay ngược chiều kim đồng hồ k × 22,5° (k = 0: mặt ghế hướng về máy ảnh).
# Chạy: <venv có bpy>/bin/python ghe_xoay_3d.py <thư mục ra>  → ghe-<k>.png, ghe-<k>-id.png (đỏ: không, lục: đệm, lam: khung), ghe.json
import sys, os, math, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
import xuong_3d as X

RA = sys.argv[-1] if len(sys.argv) > 1 and not sys.argv[-1].endswith('.py') else '.'
os.makedirs(RA, exist_ok=True)
so = {}
for k in range(16):
    sc = X.moi(); X.ID.clear()
    khung = X.vat_lieu('khung', (0.84, 0.76, 0.60), 0.45, (0, 0, 1))
    dem = X.vat_lieu('dem', (0.93, 0.91, 0.86), 0.8, (0, 1, 0))
    ghe = X.ghe_chiavari(khung, dem)
    X.nhan_ban(ghe, (0, 0, 0), k * math.pi / 8)
    for o in ghe: bpy.data.objects.remove(o)
    m = X.may_anh(sc, le=0.03)
    X.ve(sc, os.path.join(RA, f'ghe-{k}'))
    so[k] = m; print(k, m)
json.dump(so, open(os.path.join(RA, 'ghe.json'), 'w'), indent=1)
print('xong')
