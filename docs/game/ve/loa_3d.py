# Tự vẽ bằng 3D (0 lượt), ngày 26/11: loa cho hạng mục âm thanh của màn trang trí theo lớp.
# Ba món, cùng máy ảnh trực giao chếch 15°, 260 px mỗi mét như bàn ghế (xuong_3d.py), nên đặt vào cảnh bằng cùng thước phối cảnh:
#   loa-keo: loa kéo có bánh xe và tay kéo; loa-chan: loa đứng trên chân ba càng; loa-sub: loa trên cột, cột cắm vào thùng sub.
# Chạy: <venv có bpy>/bin/python loa_3d.py <thư mục ra>  → loa-*.png và loa.json (số đo kiểu TT)
import sys, os, math, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from mathutils import Vector
import xuong_3d as X

RA = sys.argv[-1] if len(sys.argv) > 1 and not sys.argv[-1].endswith('.py') else '.'
os.makedirs(RA, exist_ok=True)


def hop(c, kich, mat, bo=0.012):
    """Hộp bo mép, tâm c, cỡ kich (rộng x, sâu y, cao z)."""
    bpy.ops.mesh.primitive_cube_add(size=1, location=c); o = bpy.context.object; o.scale = kich
    bpy.ops.object.transform_apply(scale=True)
    if bo:
        m = o.modifiers.new('bo', 'BEVEL'); m.width = bo; m.segments = 3
    return X._vao(o, mat)


def dia(c, r, day, mat, truc='y'):
    """Đĩa tròn (màng loa) nằm trên mặt trước, trục theo y."""
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=r, depth=day, location=c)
    o = bpy.context.object
    if truc == 'y': o.rotation_euler = (math.pi / 2, 0, 0)
    bpy.ops.object.shade_smooth(); return X._vao(o, mat)


def thung_loa(z0, rong, sau, cao, M):
    """Thùng loa đứng trên độ cao z0: vỏ, lưới mặt trước, màng bass, họng loa treble."""
    vo, luoi, mang = M['vo'], M['luoi'], M['mang']
    hop((0, 0, z0 + cao / 2), (rong, sau, cao), vo, 0.016)
    hop((0, -sau / 2 - 0.004, z0 + cao / 2), (rong - 0.05, 0.01, cao - 0.05), luoi, 0.004)
    dia((0, -sau / 2 - 0.012, z0 + cao * 0.36), rong * 0.36, 0.012, mang)
    hop((0, -sau / 2 - 0.012, z0 + cao * 0.8), (rong * 0.5, 0.012, cao * 0.14), mang, 0.004)


def chan_ba(cao, r_chan, M):
    """Chân ba càng: ống đứng, ba càng xoè xuống đất (một càng ra sau để không chắn mặt loa)."""
    kl = M['kl']; X.ong((0, 0, 0.42), (0, 0, cao), 0.018, kl)
    for a in (90, 210, 330):
        t = math.radians(a); X.ong((0, 0, 0.5), (r_chan * math.cos(t), r_chan * math.sin(t), 0.01), 0.011, kl)


BO = {
    'loa-keo': 'loa kéo',
    'loa-chan': 'loa đứng trên chân',
    'loa-sub': 'loa trên cột, cột cắm vào sub',
}
so = {}
for ten, mo in BO.items():
    sc = X.moi(); X.ID.clear()
    M = {'vo': X.vat_lieu('vo', (0.035, 0.035, 0.038), 0.55), 'luoi': X.vat_lieu('luoi', (0.075, 0.078, 0.082), 0.95),
         'mang': X.vat_lieu('mang', (0.02, 0.02, 0.022), 0.35), 'kl': X.vat_lieu('kl', (0.42, 0.43, 0.45), 0.35)}
    if ten == 'loa-keo':
        thung_loa(0.07, 0.42, 0.34, 0.74, M)
        for s in (-1, 1):
            dia((s * 0.2, 0.12, 0.06), 0.06, 0.04, M['mang'], truc='x').rotation_euler = (0, math.pi / 2, 0)   # bánh xe sau
            X.ong((s * 0.14, 0.12, 0.81), (s * 0.14, 0.12, 1.08), 0.009, M['kl'])                          # tay kéo rút
        X.ong((-0.15, 0.12, 1.08), (0.15, 0.12, 1.08), 0.012, M['vo'])
    elif ten == 'loa-chan':
        chan_ba(1.5, 0.55, M); thung_loa(1.5, 0.34, 0.3, 0.56, M)
    else:
        hop((0, 0, 0.28), (0.56, 0.6, 0.56), M['vo'], 0.02)
        hop((0, -0.304, 0.28), (0.5, 0.01, 0.5), M['luoi'], 0.004)
        dia((0, -0.312, 0.28), 0.2, 0.012, M['mang'])
        X.ong((0, 0, 0.56), (0, 0, 1.45), 0.018, M['kl'])
        thung_loa(1.45, 0.34, 0.3, 0.56, M)
    m = X.may_anh(sc)
    X.ve(sc, os.path.join(RA, ten))
    m.update(mo=mo); so[ten] = m
    print(ten, m)
json.dump(so, open(os.path.join(RA, 'loa.json'), 'w'), ensure_ascii=False, indent=1)
print('xong')
