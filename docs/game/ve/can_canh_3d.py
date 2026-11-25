# Tự vẽ màn cận cảnh bàn bằng 3D (0 lượt), ngày 25/11: thay T12 (nền cận cảnh) + T13 (đồ bàn ở góc cận).
# Khung theo quy tắc ở bang-ve.md: một chỗ ngồi ở giữa, chỗ hai bên bị mép khung cắt, lưng ghế dưới khung, giữa bàn ở mép trên.
# Hai cách bày: kiểu Âu (đĩa lót, đĩa, khăn ăn, dao nĩa, 3 ly, đĩa bánh mì) và kiểu Việt (đĩa kê, chén, thìa, đũa và gác đũa, ly).
# Mỗi bản ra: tranh, mặt nạ màu ID (khăn đỏ, đĩa lục, đĩa lót lam, dao nĩa vàng, ly lục lam, khăn ăn tím), toạ độ khăn 16 bit.
# Chạy: <venv có bpy>/bin/python can_canh_3d.py <thư mục ra>
import sys, os, math, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy, bmesh
from mathutils import Vector
import xuong_3d as X

RA = sys.argv[-1] if len(sys.argv) > 1 and not sys.argv[-1].endswith('.py') else '.'
os.makedirs(RA, exist_ok=True)
H_BAN, R_BAN = 0.76, 0.9


def xoay(profile, mat, n=64, day=0.0, vi_tri=(0, 0, 0), ten='xoay'):
    """Vật tròn xoay từ đường viền [(r, z)] (đĩa, chén, ly). day > 0 thì thêm bề dày."""
    bm = bmesh.new(); vong = []
    for k in range(n):
        a = 2 * math.pi * k / n
        vong.append([bm.verts.new((r * math.cos(a), r * math.sin(a), z)) for r, z in profile])
    for k in range(n):
        A, B = vong[k], vong[(k + 1) % n]
        for i in range(len(profile) - 1): bm.faces.new((A[i], B[i], B[i + 1], A[i + 1]))
    me = bpy.data.meshes.new(ten); bm.to_mesh(me); bm.free()
    for p in me.polygons: p.use_smooth = True
    o = bpy.data.objects.new(ten, me); bpy.data.collections['net'].objects.link(o); me.materials.append(mat); o.location = vi_tri
    if day: s = o.modifiers.new('day', 'SOLIDIFY'); s.thickness = day
    return o


def hop(kich, vi_tri, mat, quay=0, bo=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=vi_tri); o = bpy.context.object; o.scale = kich; bpy.ops.object.transform_apply(scale=True)
    o.rotation_euler = (0, 0, quay)
    if bo: m = o.modifiers.new('bo', 'BEVEL'); m.width = bo; m.segments = 3
    return X._vao(o, mat)


def dao_nia(loai, x, y, mat):
    z = H_BAN + 0.004
    if loai == 'nia':
        hop((0.012, 0.13, 0.004), (x, y - 0.03, z), mat, bo=0.002)
        for i in range(4): hop((0.0025, 0.05, 0.003), (x - 0.009 + i * 0.006, y + 0.065, z), mat)
        hop((0.026, 0.012, 0.004), (x, y + 0.038, z), mat, bo=0.002)
    elif loai == 'dao':
        hop((0.012, 0.11, 0.005), (x, y - 0.045, z), mat, bo=0.002); hop((0.018, 0.11, 0.002), (x + 0.002, y + 0.065, z), mat, bo=0.004)
    elif loai == 'thia':
        hop((0.011, 0.12, 0.004), (x, y - 0.04, z), mat, bo=0.002)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.02, location=(x, y + 0.055, z + 0.004)); o = bpy.context.object; o.scale = (0.85, 1.25, 0.25); X._vao(o, mat)
    elif loai == 'dua':   # đôi đũa nằm trên gác đũa
        for dx in (-0.006, 0.006):
            X.ong((x + dx, y - 0.11, z + 0.006), (x + dx * 1.6, y + 0.13, z + 0.012), 0.0035, mat)
        hop((0.03, 0.012, 0.01), (x, y - 0.06, z + 0.002), mat, bo=0.003)


def bo_cho(kieu, mats, goc_vi=0.0):
    """Một chỗ ngồi ở mép bàn tại góc goc_vi (0 = phía máy ảnh)."""
    vai, dia, lot, kl, ly, khan = mats
    c, s = math.cos(goc_vi), math.sin(goc_vi); tam = Vector((0, -R_BAN + (0.22 if kieu == 'au' else 0.12), 0))
    goc = bpy.data.objects.new('cho', None); bpy.data.collections['net'].objects.link(goc)
    truoc = set(bpy.data.objects)
    z = H_BAN
    if kieu == 'au':
        xoay([(0.002, 0.001), (0.15, 0.002), (0.165, 0.008), (0.168, 0.01)], lot, day=0.003, vi_tri=(tam.x, tam.y, z))        # đĩa lót 33 cm
        for k in range(48):                                                                                                    # viền hạt
            a = 2 * math.pi * k / 48; bpy.ops.mesh.primitive_uv_sphere_add(segments=8, ring_count=5, radius=0.0045, location=(tam.x + 0.16 * math.cos(a), tam.y + 0.16 * math.sin(a), z + 0.011)); X._vao(bpy.context.object, lot)
        xoay([(0.002, 0.013), (0.09, 0.014), (0.105, 0.02), (0.13, 0.028), (0.133, 0.03)], dia, day=0.003, vi_tri=(tam.x, tam.y, z))   # đĩa ăn 27 cm
        hop((0.14, 0.09, 0.022), (tam.x, tam.y, z + 0.045), khan, bo=0.008)                                                    # khăn ăn gấp phẳng
        hop((0.07, 0.004, 0.04), (tam.x, tam.y + 0.03, z + 0.075), khan, bo=0.001)                                              # thiệp tên đứng
        dao_nia('nia', tam.x - 0.2, tam.y, kl); dao_nia('nia', tam.x - 0.225, tam.y, kl)
        dao_nia('dao', tam.x + 0.2, tam.y, kl); dao_nia('thia', tam.x + 0.23, tam.y, kl)
        xoay([(0.002, 0.008), (0.07, 0.009), (0.08, 0.014)], dia, day=0.003, vi_tri=(tam.x - 0.21, tam.y + 0.2, z))                 # đĩa bánh mì
        for (dx, dy, loai) in ((0.16, 0.2, 'nuoc'), (0.22, 0.15, 'vang'), (0.1, 0.24, 'flute')):
            prof = {'nuoc': [(0.035, 0), (0.035, 0.004), (0.006, 0.01), (0.005, 0.07), (0.03, 0.09), (0.042, 0.13), (0.04, 0.17)],
                    'vang': [(0.032, 0), (0.032, 0.004), (0.005, 0.01), (0.004, 0.08), (0.028, 0.1), (0.038, 0.14), (0.032, 0.18)],
                    'flute': [(0.03, 0), (0.03, 0.004), (0.004, 0.01), (0.004, 0.09), (0.018, 0.12), (0.024, 0.18), (0.022, 0.22)]}[loai]
            xoay(prof, ly, n=40, day=0.0015, vi_tri=(tam.x + dx, tam.y + dy, z))
    else:   # kiểu Việt, theo Sapo "Cách set up bàn ăn kiểu Á" (đọc trọn 25/11): đĩa kê 18–20 cm cách mép bàn 2 cm, đĩa ăn 12–15 cm
            # trên đĩa kê, bát úp, đũa trên gác (cách đĩa kê 2 cm), thìa trên gác bên trái đũa, chén nước chấm trước đĩa kê, ly phía trước bên phải,
            # khăn ăn gấp đặt trên miệng cốc nước
        xoay([(0.002, 0.001), (0.085, 0.002), (0.094, 0.008), (0.096, 0.01)], lot, day=0.003, vi_tri=(tam.x, tam.y, z))         # đĩa kê 19 cm
        xoay([(0.002, 0.011), (0.055, 0.012), (0.066, 0.018), (0.068, 0.02)], dia, day=0.003, vi_tri=(tam.x, tam.y, z))         # đĩa ăn 14 cm
        xoay([(0.056, 0.02), (0.055, 0.035), (0.046, 0.058), (0.032, 0.07), (0.03, 0.075), (0.026, 0.075), (0.025, 0.071), (0.002, 0.071)], dia, day=0.003, vi_tri=(tam.x, tam.y, z))   # bát úp, có chân đế kín
        dao_nia('dua', tam.x + 0.135, tam.y + 0.02, kl)
        hop((0.014, 0.012, 0.008), (tam.x + 0.11, tam.y - 0.035, z + 0.004), dia, bo=0.003)                                  # gác thìa
        dao_nia('thia', tam.x + 0.11, tam.y + 0.01, dia)                                                                         # thìa sứ
        xoay([(0.002, 0.0), (0.028, 0.004), (0.034, 0.02), (0.035, 0.028)], dia, day=0.002, vi_tri=(tam.x - 0.02, tam.y + 0.15, z))   # chén nước chấm
        xoay([(0.032, 0), (0.033, 0.004), (0.036, 0.12), (0.037, 0.13)], ly, n=40, day=0.0015, vi_tri=(tam.x + 0.12, tam.y + 0.16, z))   # cốc nước
        q = xoay([(0.002, 0.10), (0.03, 0.14), (0.055, 0.2)], khan, n=16, vi_tri=(tam.x + 0.12, tam.y + 0.16, z))           # khăn ăn gấp quạt trên miệng cốc
        q.scale = (1, 0.22, 1); q.rotation_euler = (0, 0, math.radians(15))                                                   # ép dẹt thành hình quạt
        xoay([(0.032, 0), (0.032, 0.004), (0.005, 0.01), (0.004, 0.08), (0.028, 0.1), (0.038, 0.14), (0.032, 0.18)], ly, n=40, day=0.0015, vi_tri=(tam.x + 0.2, tam.y + 0.1, z))   # ly vang (phục vụ hạng VIP)
    for o in bpy.data.objects:
        if o not in truoc and o.parent is None and o != goc: o.parent = goc
    goc.rotation_euler = (0, 0, goc_vi)
    return goc


for kieu in (sys.argv[-2].split(',') if len(sys.argv) > 2 and not sys.argv[-2].endswith('.py') else ('au', 'viet')):
    sc = X.moi(); X.ID.clear()
    mats = (X.vat_lieu('khan', (0.94, 0.92, 0.87), 0.85, (1, 0, 0)), X.vat_lieu('dia', (0.95, 0.95, 0.94), 0.25, (0, 1, 0)),
            X.vat_lieu('lot', (0.80, 0.64, 0.32), 0.3, (0, 0, 1)), X.vat_lieu('kl', (0.78, 0.66, 0.40), 0.3, (1, 1, 0)),
            X.vat_lieu('ly', (0.92, 0.95, 0.96), 0.05, (0, 1, 1)), X.vat_lieu('khanan', (0.93, 0.91, 0.86), 0.8, (1, 0, 1)))
    for m, kl in ((mats[2], 1.0), (mats[3], 1.0)): m.node_tree.nodes['Principled BSDF'].inputs['Metallic'].default_value = kl
    p = mats[4].node_tree.nodes['Principled BSDF']; p.inputs['Alpha'].default_value = 0.28   # ly kiểu tranh vẽ: trong mờ, có nét viền; không khúc xạ (khúc xạ ra vệt đen)
    sc.view_layers[0].freestyle_settings.linesets[0].select_crease = False   # bỏ nét nếp gấp: mặt đĩa tròn xoay sinh tia nan quạt
    sc.cycles.samples = 64
    khan, Rm = X.khan_tron(R_BAN, H_BAN, mats[0], seed=3)
    for g in (0.0, -0.95, 0.95): bo_cho(kieu, mats, g)            # chỗ giữa và hai chỗ bên (bị khung cắt)
    # máy ảnh phối cảnh: người đứng sau ghế, mắt cao 1,45 m, lùi 0,55 m khỏi mép bàn, nhìn xuống khoảng 40°
    cam = bpy.data.cameras.new('cam'); cam.lens = 46; co = bpy.data.objects.new('cam', cam); sc.collection.objects.link(co); sc.camera = co
    co.location = (0, -R_BAN - 0.42, 1.42); co.rotation_euler = (math.radians(46), 0, 0)
    sc.render.resolution_x = 1280; sc.render.resolution_y = 860; sc.render.line_thickness = 2.2
    ten = f'can-canh-{kieu}'; X.ve(sc, os.path.join(RA, ten), uv_vat=khan)
    json.dump(dict(Rm=round(Rm, 4), R=R_BAN), open(os.path.join(RA, ten + '.json'), 'w'))
    print(ten, 'xong')
