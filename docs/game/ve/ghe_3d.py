# Thử dựng ghế chiavari bằng 3D (0 lượt vẽ), ngày 25/11: thay tấm T7 (ghế 8 góc nhìn) nếu nét giống tranh vẽ tay.
# Ghế mảnh: 4 chân, khung mặt ngồi, đệm, lưng có thanh trên cong, 3 nan dọc, thanh giằng. Vẽ bằng Cycles (CPU) + nét mực Freestyle,
# nền trong suốt, mỗi góc một ảnh; thêm một lượt chỉ có đệm để lấy mặt nạ đệm (không cần khoanh tay).
# Cần bpy (pip install bpy, chạy trong venv riêng, không đưa vào repo):   <venv>/bin/python ghe_3d.py <thư mục ra>
import bpy, math, os, sys
from mathutils import Vector

RA = sys.argv[-1] if len(sys.argv) > 1 and not sys.argv[-1].endswith('.py') else '.'
os.makedirs(RA, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene


def vat_lieu(ten, mau, nham=0.55):
    m = bpy.data.materials.new(ten); m.use_nodes = True
    p = m.node_tree.nodes['Principled BSDF']; p.inputs['Base Color'].default_value = (*mau, 1); p.inputs['Roughness'].default_value = nham
    return m


KHUNG = vat_lieu('khung', (0.84, 0.76, 0.60), 0.45)    # kem ngà như ghế trong tranh cũ
DEM = vat_lieu('dem', (0.93, 0.91, 0.86), 0.8)


def ong(a, b, r, mat=KHUNG):
    a, b = Vector(a), Vector(b); d = b - a
    bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=r, depth=d.length, location=(a + b) / 2)
    o = bpy.context.object; o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(d)
    o.data.materials.append(mat); bpy.ops.object.shade_smooth(); return o


def duong(pts, r, mat=KHUNG):
    for a, b in zip(pts[:-1], pts[1:]): ong(a, b, r, mat)


def khop(p, r):   # vòng "đốt tre" ở khớp
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=8, radius=r, location=p); o = bpy.context.object
    o.data.materials.append(KHUNG); bpy.ops.object.shade_smooth()


r = 0.013; W, D, HS = 0.40, 0.40, 0.45            # bán kính ống, rộng, sâu, cao mặt ngồi (m)
x0, x1, y0, y1 = -W / 2, W / 2, -D / 2, D / 2
# chân trước thẳng, chân sau chạy lên thành cột lưng, hơi ngả ra sau
for x in (x0 + 0.02, x1 - 0.02):
    ong((x, y0 + 0.02, 0), (x, y0 + 0.02, HS), r)
    duong([(x * 0.98, y1 - 0.01, 0), (x, y1 - 0.02, HS), (x * 0.96, y1 + 0.02, HS + 0.25), (x * 0.92, y1 + 0.05, HS + 0.52)], r)
# khung mặt ngồi
duong([(x0, y0, HS), (x1, y0, HS), (x1, y1, HS), (x0, y1, HS), (x0, y0, HS)], r * 1.1)
# thanh giằng chân
for h in (0.14, 0.26):
    duong([(x0 + 0.02, y0 + 0.02, h), (x0 + 0.02, y1 - 0.01, h)], r * 0.75); duong([(x1 - 0.02, y0 + 0.02, h), (x1 - 0.02, y1 - 0.01, h)], r * 0.75)
duong([(x0 + 0.02, y0 + 0.02, 0.2), (x1 - 0.02, y0 + 0.02, 0.2)], r * 0.75)
# lưng: thanh trên cong, thanh dưới, 3 nan dọc
tren = [(x0 * 0.92 * math.cos(t), y1 + 0.05 + 0.025 * math.sin(math.pi * (0.5 + 0.5 * math.cos(t))), HS + 0.52 + 0.03 * math.sin(math.pi * (0.5 + 0.5 * math.cos(t))))
        for t in [math.pi * k / 12 for k in range(13)]]
cv = bpy.data.curves.new('tren', 'CURVE'); cv.dimensions = '3D'; cv.bevel_depth = r * 1.15; cv.bevel_resolution = 3
sp = cv.splines.new('POLY'); sp.points.add(len(tren) - 1)
for i, p in enumerate(tren): sp.points[i].co = (*p, 1)
o = bpy.data.objects.new('tren', cv); sc.collection.objects.link(o); cv.materials.append(KHUNG)   # thanh trên liền một nét, không lộ khớp
duoi = [(x0 * 0.96, y1 + 0.005, HS + 0.08), (x1 * 0.96, y1 + 0.005, HS + 0.08)]
duong(duoi, r)
for f in (-0.33, 0, 0.33):
    ong((x1 * 0.96 * f, y1 + 0.005, HS + 0.08), (x1 * 0.92 * f, y1 + 0.05, HS + 0.52 + 0.03 * math.sin(math.pi * (0.5 + 0.5 * f))), r * 0.75)
for p in [(x0 + 0.02, y0 + 0.02, 0.2), (x1 - 0.02, y0 + 0.02, 0.2), (x0 + 0.02, y0 + 0.02, 0.14), (x1 - 0.02, y0 + 0.02, 0.14)]:
    khop(p, r * 1.5)
# đệm: hộp bo tròn
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, HS + 0.03)); dem = bpy.context.object
dem.scale = (W * 0.97, D * 0.97, 0.05); bpy.ops.object.transform_apply(scale=True)
m = dem.modifiers.new('bo', 'BEVEL'); m.width = 0.018; m.segments = 4
dem.data.materials.append(DEM); bpy.ops.object.shade_smooth()

# gộp ghế dưới một gốc để xoay
goc = bpy.data.objects.new('goc', None); sc.collection.objects.link(goc)
for o in list(sc.objects):
    if o.type in ('MESH', 'CURVE'): o.parent = goc
# máy ảnh nhìn chếch xuống như bàn tiệc trong cảnh (khoảng 28°), ống kính dài để ít méo
cam = bpy.data.cameras.new('cam'); cam.lens = 85; co = bpy.data.objects.new('cam', cam); sc.collection.objects.link(co); sc.camera = co
goc_nhin = math.radians(20); kc = 4.2          # 20°: gần góc nhìn ghế trong tranh cũ
co.location = (0, -kc * math.cos(goc_nhin), 0.45 + kc * math.sin(goc_nhin)); co.rotation_euler = (math.pi / 2 - goc_nhin, 0, 0)
# ánh sáng mềm: mặt trời chếch trái phía trên + trời
sun = bpy.data.lights.new('sun', 'SUN'); sun.energy = 3.2; sun.angle = math.radians(12)
so = bpy.data.objects.new('sun', sun); sc.collection.objects.link(so); so.rotation_euler = (math.radians(50), math.radians(-25), math.radians(-35))
w = bpy.data.worlds.new('w'); w.use_nodes = True; w.node_tree.nodes['Background'].inputs['Color'].default_value = (0.75, 0.78, 0.72, 1)
w.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.9; sc.world = w
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = 48
sc.render.resolution_x = 420; sc.render.resolution_y = 560; sc.render.film_transparent = True
sc.view_settings.view_transform = 'Standard'
# nét mực
sc.render.use_freestyle = True; sc.render.line_thickness_mode = 'ABSOLUTE'; sc.render.line_thickness = 1.6
vl = sc.view_layers[0]; fs = vl.freestyle_settings
ls = fs.linesets.new('net') if not fs.linesets else fs.linesets[0]
ls.select_by_visibility = True; ls.visibility = 'VISIBLE'; ls.select_by_edge_types = True
ls.select_silhouette = True; ls.select_border = True; ls.select_crease = True; fs.crease_angle = math.radians(140)
if ls.linestyle is None: ls.linestyle = bpy.data.linestyles.new('muc')
ls.linestyle.color = (0.30, 0.22, 0.15); ls.linestyle.thickness = 1.6

for k in range(8):
    goc.rotation_euler = (0, 0, math.radians(45 * k))
    DEM.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (0.93, 0.91, 0.86, 1)
    sc.render.filepath = os.path.join(RA, f'ghe-{k}.png'); bpy.ops.render.render(write_still=True)
    # lượt mặt nạ đệm: khung đen, đệm trắng, không nét, tắt bóng
    sc.render.use_freestyle = False
    KHUNG.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (0, 0, 0, 1)
    emit = DEM.node_tree.nodes['Principled BSDF']; emit.inputs['Emission Color'].default_value = (1, 1, 1, 1); emit.inputs['Emission Strength'].default_value = 20
    sc.render.filepath = os.path.join(RA, f'ghe-{k}-dem.png'); bpy.ops.render.render(write_still=True)
    emit.inputs['Emission Strength'].default_value = 0; KHUNG.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (0.84, 0.76, 0.60, 1)
    sc.render.use_freestyle = True
print('xong')
