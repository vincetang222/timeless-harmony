# Tự vẽ bằng 3D (0 lượt), ngày 25/11: bộ bàn tròn phủ khăn trắng chấm đất, ghế chiavari xếp quanh bàn — thay T7 + T8.
# Mỗi bộ (6, 10, 12 khách) ra: tranh, mặt nạ (khăn đỏ, đệm lục, khung ghế lam), toạ độ khăn 16 bit (khan_lop dùng để xếp lớp), số đo kiểu TT.
# Chạy: GOC_3D=10 <venv có bpy>/bin/python ban_tron_3d.py <thư mục ra>   (GOC_3D: độ chếch máy ảnh, xem xuong_3d.py)
import sys, os, math, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
import xuong_3d as X

RA = sys.argv[-1] if len(sys.argv) > 1 and not sys.argv[-1].endswith('.py') else '.'
os.makedirs(RA, exist_ok=True)
BO = [(6, 0.6), (10, 0.9), (12, 1.0)]      # số khách, bán kính bàn (m): bàn 1,2 m, 1,8 m, 2,0 m
so = {}
for khach, R in BO:
    sc = X.moi(); X.ID.clear()
    vai = X.vat_lieu('khan', (0.94, 0.92, 0.87), 0.85, (1, 0, 0))
    khung = X.vat_lieu('khung', (0.84, 0.76, 0.60), 0.45, (0, 0, 1))
    dem = X.vat_lieu('dem', (0.93, 0.91, 0.86), 0.8, (0, 1, 0))
    khan, Rm = X.khan_tron(R, 0.76, vai, seed=khach)
    ghe = X.ghe_chiavari(khung, dem)
    d = R + 0.32                                      # tâm ghế cách tâm bàn
    for i in range(khach):
        phi = 2 * math.pi * i / khach + math.pi / khach * (khach % 4 == 2)   # lệch nửa nhịp để ghế không che chính giữa
        q = phi - math.pi / 2                         # ghế mẫu có mặt hướng −y; quay q thì mặt hướng (sin q, −cos q) = −(cos φ, sin φ): vào tâm bàn
        assert math.sin(q) * -math.cos(phi) + -math.cos(q) * -math.sin(phi) > 0.99, 'ghế phải quay mặt vào bàn'
        X.nhan_ban(ghe, (d * math.cos(phi), d * math.sin(phi), 0), q)   # (bản 25/11 dùng φ + π/2: ghế quay lưng vào bàn, sửa 26/11)
    for o in ghe: bpy.data.objects.remove(o)          # bỏ ghế mẫu ở gốc
    m = X.may_anh(sc)
    ten = f'ban-tron-{khach}'
    X.ve(sc, os.path.join(RA, ten), uv_vat=khan)
    m.update(R=R, khach=khach, khan_uv_Rm=round(Rm, 4)); so[ten] = m
    print(ten, m)
json.dump(so, open(os.path.join(RA, 'ban-tron.json'), 'w'), ensure_ascii=False, indent=1)
print('xong')
