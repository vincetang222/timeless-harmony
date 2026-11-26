# Tự vẽ bằng 3D (0 lượt), ngày 26/11: bàn dài xuyên suốt chạy dọc lối đi, theo ảnh tham khảo (bàn dài dưới vòm đá, bàn dài bên hồ).
# Khác các bộ bàn khác (máy ảnh trực giao, mã đặt vào cảnh), bàn chạy vào sâu cần phối cảnh thật, nên vẽ thẳng bằng máy ảnh phối cảnh
# khớp tranh (đo 26/11): máy cao 1/0,307 ≈ 3,257 m, nhìn ngang, tiêu cự 1,1 lần bề ngang khung, đường chân trời ở 44% chiều cao khung,
# điểm tụ giữa khung (bản chơi dời ngang theo lối đi của từng nơi). Cặp đôi đứng cách máy 17,62 m (Vườn Hồ).
#   ban-xuyen-giua: một bàn trên lối đi, đầu bàn ngay trước cặp đôi, chạy ra phía máy ảnh;
#   ban-xuyen-doc: hai dãy bàn trên cỏ hai bên lối (tâm cách lối 3,6 m), từ gần lan can ra tới đáy khung.
# Mỗi bộ: tranh, mặt nạ (khăn đỏ, đệm lục, khung ghế lam), toạ độ khăn 16 bit, cỡ đầy khung 1600 × 889.
# Chạy: <venv có bpy>/bin/python ban_xuyen_3d.py [thu] <thư mục ra>   (thu: 8 mẫu, không nét, để soát vị trí nhanh)
import sys, os, math, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
import xuong_3d as X
import ban_dai_3d as BD

RA = sys.argv[-1] if len(sys.argv) > 1 and not sys.argv[-1].endswith('.py') else '.'
THU = 'thu' in sys.argv
os.makedirs(RA, exist_ok=True)
W, H, HC, FW, D0 = 1600, 889, 1 / 0.307, 1.1, 17.62


def may_pc(sc):
    cam = bpy.data.cameras.new('cam'); cam.type = 'PERSP'; cam.sensor_fit = 'HORIZONTAL'; cam.sensor_width = 36; cam.lens = FW * 36
    cam.shift_y = -(0.50 - 0.44) * H / W; cam.clip_start = 0.5; cam.clip_end = 300
    co = bpy.data.objects.new('cam', cam); sc.collection.objects.link(co); sc.camera = co
    co.location = (0, 0, HC); co.rotation_euler = (math.pi / 2, 0, 0)
    sc.render.resolution_x = W; sc.render.resolution_y = H; sc.render.line_thickness = 1.3


def mot_ban(vai, khung, dem, cx, y0, y1, seed):
    """Bàn dài chạy dọc (theo trục y, từ y0 tới y1), tâm ngang cx; ghế hai bên quay vào bàn. Trả (khăn, số ghế mỗi bên, dài)."""
    moi_ben = int((y1 - y0 - 0.3) / 0.62); dai = moi_ben * 0.62 + 0.3
    khan, cao = BD.khan_dai(dai, BD.RONG, vai, seed=seed)
    ghe = X.ghe_chiavari(khung, dem); goc = bpy.data.objects.new('ban', None); bpy.data.collections['net'].objects.link(goc)
    for i in range(moi_ben):
        x = -dai / 2 + 0.15 + 0.31 + i * 0.62
        X.nhan_ban(ghe, (x, -BD.RONG / 2 - 0.3, 0), math.pi).parent = goc
        X.nhan_ban(ghe, (x, BD.RONG / 2 + 0.3, 0), 0.0).parent = goc
    for o in ghe: bpy.data.objects.remove(o)
    khan.parent = goc; goc.rotation_euler = (0, 0, math.pi / 2); goc.location = (cx, (y0 + y1) / 2, 0)
    return khan, moi_ben, dai, cao


BO = {'ban-xuyen-giua': [(0.0, D0 - 1.6 - 6.0, D0 - 1.6)], 'ban-xuyen-doc': [(-3.6, D0 - 6.5, D0 + 6.5), (3.6, D0 - 6.5, D0 + 6.5)]}
so = {}
for ten, ds in BO.items():
    sc = X.moi(); X.ID.clear(); may_pc(sc)
    vai = X.vat_lieu('khan', (0.94, 0.92, 0.87), 0.85, (1, 0, 0)); khung = X.vat_lieu('khung', (0.84, 0.76, 0.60), 0.45, (0, 0, 1))
    dem = X.vat_lieu('dem', (0.93, 0.91, 0.86), 0.8, (0, 1, 0))
    kq = [mot_ban(vai, khung, dem, cx, y0, y1, 3 + i) for i, (cx, y0, y1) in enumerate(ds)]
    if THU: sc.cycles.samples = 8; sc.render.use_freestyle = False
    bpy.context.view_layer.update()
    X.ve(sc, os.path.join(RA, ten), uv_vat=kq[0][0])
    so[ten] = dict(w=W, h=H, khach=2 * kq[0][1], dai=round(kq[0][2], 3), rong=BD.RONG, khan_uv_cao=round(kq[0][3], 4), ban=[[cx, y0, y1] for cx, y0, y1 in ds], d0=D0)
    print(ten, so[ten])
json.dump(so, open(os.path.join(RA, 'ban-xuyen.json'), 'w'), indent=1)
print('xong')
