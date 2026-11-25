# Xưởng 3D dùng chung cho đồ tự vẽ (0 lượt): ghế chiavari, khăn bàn tròn có nếp, đồ bàn; máy ảnh trực giao chếch 15°;
# vẽ ba lượt cho mỗi món: tranh (Cycles + nét mực Freestyle có thon), mặt nạ (khăn đỏ, đệm lục, khung lam), toạ độ khăn (ảnh 16 bit).
# Cần bpy (pip install bpy trong venv riêng, không đưa vào repo). Không đụng tới build_kit.py hay game/assets/kit/ (kho khác, chờ duyệt).
import bpy, math, os, json
import numpy as np
from mathutils import Vector

PXM = 260          # px mỗi mét khi vẽ: mọi món cùng một thước, nên nét mực ra cùng độ dày sau khi đặt vào cảnh
GOC = 15           # độ chếch máy ảnh: bàn tròn trong tranh cũ có elip mặt bàn b/a ≈ 0,26 → khoảng 15°
NET = 2.0          # độ dày nét mực (px ở cỡ vẽ)
ID = {}            # tên vật liệu → màu mặt nạ


def moi():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = 64
    try:
        sc.cycles.use_denoising = True; sc.cycles.denoiser = 'OPENIMAGEDENOISE'
    except Exception:
        sc.cycles.use_denoising = False
    sc.render.film_transparent = True; sc.view_settings.view_transform = 'Standard'
    sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGBA'
    w = bpy.data.worlds.new('w'); sc.world = w
    try:
        w.use_nodes = True
    except Exception:
        pass
    bg = w.node_tree.nodes['Background']; bg.inputs['Color'].default_value = (0.78, 0.80, 0.74, 1); bg.inputs['Strength'].default_value = 0.6
    sun = bpy.data.lights.new('sun', 'SUN'); sun.energy = 3.4; sun.angle = math.radians(14)
    so = bpy.data.objects.new('sun', sun); sc.collection.objects.link(so); so.rotation_euler = (math.radians(58), math.radians(-18), math.radians(-40))   # nắng xiên để nếp khăn có bóng
    # mặt đất bắt bóng (trong suốt, chỉ giữ bóng)
    bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, 0)); g = bpy.context.object; g.name = 'dat'; g.is_shadow_catcher = True
    # nét mực: viền ngoài, mép, nếp đã đánh dấu; thon hai đầu và hơi rung
    sc.render.use_freestyle = True; sc.render.line_thickness_mode = 'ABSOLUTE'; sc.render.line_thickness = NET
    fs = sc.view_layers[0].freestyle_settings; ls = fs.linesets.new('net') if not fs.linesets else fs.linesets[0]
    ls.select_by_visibility = True; ls.visibility = 'VISIBLE'; ls.select_by_edge_types = True
    ls.select_silhouette = True; ls.select_border = True; ls.select_crease = True; ls.select_edge_mark = True; fs.crease_angle = math.radians(135)
    ls.select_by_collection = True
    if ls.linestyle is None: ls.linestyle = bpy.data.linestyles.new('muc')
    st = ls.linestyle; st.color = (0.30, 0.22, 0.15); st.thickness = NET
    # (bộ biến đổi độ dày nét của Freestyle làm nét dày vọt lên ở bản bpy 5.3, nên bỏ; độ rung nét thêm ở bước hậu kỳ nếu cần)
    co = bpy.data.collections.new('net'); sc.collection.children.link(co); ls.collection = co
    return sc


def vat_lieu(ten, mau, nham=0.6, id_mau=(0, 0, 0)):
    m = bpy.data.materials.new(ten)
    try:
        m.use_nodes = True
    except Exception:
        pass
    p = m.node_tree.nodes['Principled BSDF']; p.inputs['Base Color'].default_value = (*mau, 1); p.inputs['Roughness'].default_value = nham
    ID[ten] = (id_mau, mau); return m


def _vao(o, mat, sc=None):
    o.data.materials.append(mat)
    if sc is None: sc = bpy.context.scene
    for c in o.users_collection: c.objects.unlink(o)
    bpy.data.collections['net'].objects.link(o)
    return o


def ong(a, b, r, mat):
    a, b = Vector(a), Vector(b); d = b - a
    bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=r, depth=d.length, location=(a + b) / 2)
    o = bpy.context.object; o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(d)
    bpy.ops.object.shade_smooth(); return _vao(o, mat)


def cong(pts, r, mat):
    cv = bpy.data.curves.new('c', 'CURVE'); cv.dimensions = '3D'; cv.bevel_depth = r; cv.bevel_resolution = 3
    sp = cv.splines.new('POLY'); sp.points.add(len(pts) - 1)
    for i, p in enumerate(pts): sp.points[i].co = (*p, 1)
    o = bpy.data.objects.new('c', cv); bpy.data.collections['net'].objects.link(o); cv.materials.append(mat); return o


def ghe_chiavari(khung, dem):
    """Một ghế ở gốc toạ độ, mặt ghế hướng về −y. Trả danh sách vật."""
    truoc = set(bpy.data.objects)
    r = 0.013; W, D, HS = 0.40, 0.40, 0.45; x0, x1, y0, y1 = -W / 2, W / 2, -D / 2, D / 2
    for x in (x0 + 0.02, x1 - 0.02):
        ong((x, y0 + 0.02, 0), (x, y0 + 0.02, HS), r, khung)
        cong([(x * 0.98, y1 - 0.01, 0), (x, y1 - 0.02, HS), (x * 0.96, y1 + 0.02, HS + 0.25), (x * 0.92, y1 + 0.05, HS + 0.52)], r, khung)
    cong([(x0, y0, HS), (x1, y0, HS), (x1, y1, HS), (x0, y1, HS), (x0, y0, HS)], r * 1.1, khung)
    for h in (0.14, 0.26):
        ong((x0 + 0.02, y0 + 0.02, h), (x0 + 0.02, y1 - 0.01, h), r * 0.75, khung); ong((x1 - 0.02, y0 + 0.02, h), (x1 - 0.02, y1 - 0.01, h), r * 0.75, khung)
    ong((x0 + 0.02, y0 + 0.02, 0.2), (x1 - 0.02, y0 + 0.02, 0.2), r * 0.75, khung)
    cong([(x0 * 0.92 * math.cos(t), y1 + 0.05 + 0.025 * math.sin(math.pi * (0.5 + 0.5 * math.cos(t))), HS + 0.52 + 0.03 * math.sin(math.pi * (0.5 + 0.5 * math.cos(t))))
          for t in [math.pi * k / 12 for k in range(13)]], r * 1.15, khung)
    ong((x0 * 0.96, y1 + 0.005, HS + 0.08), (x1 * 0.96, y1 + 0.005, HS + 0.08), r, khung)
    for f in (-0.33, 0, 0.33):
        ong((x1 * 0.96 * f, y1 + 0.005, HS + 0.08), (x1 * 0.92 * f, y1 + 0.05, HS + 0.52 + 0.03 * math.sin(math.pi * (0.5 + 0.5 * f))), r * 0.75, khung)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, HS + 0.03)); d = bpy.context.object
    d.scale = (W * 0.97, D * 0.97, 0.05); bpy.ops.object.transform_apply(scale=True)
    m = d.modifiers.new('bo', 'BEVEL'); m.width = 0.018; m.segments = 4; bpy.ops.object.shade_smooth(); _vao(d, dem)
    return [o for o in bpy.data.objects if o not in truoc]


def nhan_ban(vat, vi_tri, quay):
    """Bản sao dùng chung lưới, đặt ở vi_tri, quay quanh trục đứng."""
    goc = bpy.data.objects.new('goc', None); bpy.data.collections['net'].objects.link(goc)
    for o in vat:
        c = o.copy(); bpy.data.collections['net'].objects.link(c); c.parent = goc
    goc.location = vi_tri; goc.rotation_euler = (0, 0, quay); return goc


def khan_tron(R, H, mat, so_nep=None, bien=0.05, loe=0.05, seed=1):
    """Khăn tròn phủ chấm đất có nếp. Toạ độ UV = toạ độ trải phẳng (X, Z) / (1 + L), đưa về 0..1 (xem khan_lop.py)."""
    rng = np.random.RandomState(seed); L = H / R; Rm = 1 + L
    so_nep = so_nep or int(round(2 * math.pi * R / 0.42))
    nT, nH, nR = 360, 36, 24
    pha = rng.uniform(0, 2 * math.pi, 3)
    def bk(th, t):  # bán kính ở góc th, độ rủ t (0 mép bàn → 1 chấm đất)
        f = 0.62 * math.sin(so_nep * th + pha[0]) + 0.28 * math.sin(1.7 * so_nep * th + pha[1]) + 0.1 * math.sin(3.1 * so_nep * th + pha[2])
        return R * (1 + loe * t) + bien * (t ** 1.2) * f
    V, F, UV = [], [], []
    # mặt bàn: các vòng tròn đồng tâm
    V.append((0, 0, H)); UV.append((0.5, 0.5))
    for i in range(1, nR + 1):
        rr = R * i / nR
        for k in range(nT):
            th = 2 * math.pi * k / nT; V.append((rr * math.sin(th), -rr * math.cos(th), H)); UV.append((0.5 + 0.5 * (rr / R) * math.sin(th) / Rm, 0.5 + 0.5 * (rr / R) * math.cos(th) / Rm))
    for k in range(nT): F.append((0, 1 + k, 1 + (k + 1) % nT))
    for i in range(1, nR):
        a0, a1 = 1 + (i - 1) * nT, 1 + i * nT
        for k in range(nT): F.append((a0 + k, a1 + k, a1 + (k + 1) % nT, a0 + (k + 1) % nT))
    # phần rủ: từ mép bàn (bo tròn nhẹ) xuống sàn; gấu hơi gợn
    goc0 = len(V) - nT
    for j in range(1, nH + 1):
        t = j / nH
        for k in range(nT):
            th = 2 * math.pi * k / nT; rr = bk(th, t); z = H * (1 - t) + (0.004 * math.sin(5 * th + pha[1]) if j == nH else 0)
            V.append((rr * math.sin(th), -rr * math.cos(th), max(0.0, z))); s = (1 + t * L) / Rm
            UV.append((0.5 + 0.5 * s * math.sin(th), 0.5 + 0.5 * s * math.cos(th)))
        a0 = goc0 + (j - 1) * nT if j > 1 else goc0; a1 = goc0 + j * nT
        for k in range(nT): F.append((a0 + k, a0 + (k + 1) % nT, a1 + (k + 1) % nT, a1 + k))
    me = bpy.data.meshes.new('khan'); me.from_pydata(V, [], F); me.update()
    uvl = me.uv_layers.new(name='trai')
    for poly in me.polygons:
        for li in poly.loop_indices: uvl.data[li].uv = UV[me.loops[li].vertex_index]
    for poly in me.polygons: poly.use_smooth = True
    # đánh dấu nét nếp: ở các hõm nếp, từ 35% độ rủ xuống gấu (như nét vẽ tay)
    # nét nếp: ở khoảng 60% số hõm nếp, một nét liền từ 35% độ rủ xuống gấu (như nét vẽ tay)
    dau = [False] * len(me.edges); canh = {tuple(sorted(e.vertices)): e.index for e in me.edges}
    j0 = int(0.35 * nH)
    for mm in range(so_nep):
        if rng.rand() > 0.6: continue
        th = ((-math.pi / 2 - pha[0]) + 2 * math.pi * mm) / so_nep
        k = int(round(th / (2 * math.pi) * nT)) % nT
        for j in range(max(1, j0), nH):
            v0 = goc0 + j * nT + k; v1 = goc0 + (j + 1) * nT + k
            e = canh.get(tuple(sorted((v0, v1))))
            if e is not None: dau[e] = True
    at = me.attributes.get('freestyle_edge') or me.attributes.new('freestyle_edge', 'BOOLEAN', 'EDGE')   # Blender 4+: dấu nét lưu thành thuộc tính
    at.data.foreach_set('value', dau)
    o = bpy.data.objects.new('khan', me); bpy.data.collections['net'].objects.link(o); me.materials.append(mat)
    return o, Rm


def may_anh(sc, le=0.06):
    """Máy ảnh trực giao chếch GOC độ, ôm vừa mọi vật (trừ đất), PXM px mỗi mét."""
    bpy.context.view_layer.update()   # để vị trí vật con (ghế nhân bản) đã cập nhật
    e = math.radians(GOC); fw = Vector((0, math.cos(e), -math.sin(e))); up = Vector((0, math.sin(e), math.cos(e))); rt = Vector((1, 0, 0))
    pts = []
    for o in sc.objects:
        if o.type not in ('MESH', 'CURVE') or o.name == 'dat': continue
        for c in o.bound_box: pts.append(o.matrix_world @ Vector(c))
    xs = [p.dot(rt) for p in pts]; ys = [p.dot(up) for p in pts]
    x0, x1, y0, y1 = min(xs) - le, max(xs) + le, min(ys) - le, max(ys) + le
    cam = bpy.data.cameras.new('cam'); cam.type = 'ORTHO'; cam.sensor_fit = 'HORIZONTAL'; cam.ortho_scale = x1 - x0
    co = bpy.data.objects.new('cam', cam); sc.collection.objects.link(co); sc.camera = co
    tam = rt * (x0 + x1) / 2 + up * (y0 + y1) / 2
    co.location = tam - fw * 20; co.rotation_euler = (math.pi / 2 - e, 0, 0)
    sc.render.resolution_x = round((x1 - x0) * PXM); sc.render.resolution_y = round((y1 - y0) * PXM)
    # điểm neo: hình chiếu gốc toạ độ (tâm bàn trên sàn)
    goc = Vector((0, 0, 0)); ax = (goc.dot(rt) - x0) / (x1 - x0); ay = 1 - (goc.dot(up) - y0) / (y1 - y0)
    return dict(w=sc.render.resolution_x, h=sc.render.resolution_y, pxm=PXM, ax=round(ax, 4), ay=round(ay, 4), goc_nhin=GOC)


def ve(sc, duong_dan, uv_vat=None):
    """Ba lượt: tranh, mặt nạ (màu ID), toạ độ khăn (16 bit, không chuyển màu)."""
    sc.render.filepath = duong_dan + '.png'; bpy.ops.render.render(write_still=True)
    luu = {}
    for m in bpy.data.materials:
        if m.name not in ID: continue
        p = m.node_tree.nodes['Principled BSDF']
        luu[m.name] = (tuple(p.inputs['Base Color'].default_value), tuple(p.inputs['Emission Color'].default_value), p.inputs['Emission Strength'].default_value)
        p.inputs['Base Color'].default_value = (0, 0, 0, 1); p.inputs['Emission Color'].default_value = (*ID[m.name][0], 1); p.inputs['Emission Strength'].default_value = 1
    sc.render.use_freestyle = False; sc.world.node_tree.nodes['Background'].inputs['Strength'].default_value = 0
    bpy.data.objects['sun'].hide_render = True; bpy.data.objects['dat'].hide_render = True
    vt = sc.view_settings.view_transform; sc.view_settings.view_transform = 'Raw'; sm = sc.cycles.samples; sc.cycles.samples = 8
    sc.render.filepath = duong_dan + '-id.png'; bpy.ops.render.render(write_still=True)
    if uv_vat is not None:
        for m in bpy.data.materials:
            if m.name in ID: m.node_tree.nodes['Principled BSDF'].inputs['Emission Strength'].default_value = 0
        m = uv_vat.data.materials[0]; nt = m.node_tree; p = nt.nodes['Principled BSDF']
        tc = nt.nodes.new('ShaderNodeTexCoord'); lk = nt.links.new(tc.outputs['UV'], p.inputs['Emission Color']); p.inputs['Emission Strength'].default_value = 1
        sc.render.image_settings.color_depth = '16'; sc.render.filter_size = 0.5
        sc.render.filepath = duong_dan + '-uv.png'; bpy.ops.render.render(write_still=True)
        nt.links.remove(lk); nt.nodes.remove(tc); sc.render.image_settings.color_depth = '8'; sc.render.filter_size = 1.5
    for ten, (bc, ec, es) in luu.items():
        p = bpy.data.materials[ten].node_tree.nodes['Principled BSDF']; p.inputs['Base Color'].default_value = bc; p.inputs['Emission Color'].default_value = ec; p.inputs['Emission Strength'].default_value = es
    sc.render.use_freestyle = True; sc.world.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.6
    bpy.data.objects['sun'].hide_render = False; bpy.data.objects['dat'].hide_render = False
    sc.view_settings.view_transform = vt; sc.cycles.samples = sm
