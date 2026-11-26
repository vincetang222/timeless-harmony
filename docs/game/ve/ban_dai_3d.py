# Tự vẽ bằng 3D (0 lượt), ngày 25/11: bàn dài phủ khăn trắng chấm đất, ghế chiavari hai bên — thay T9.
# Với 3D không cần ghép mô-đun: vẽ thẳng từng độ dài (8, 12, 20 khách), chạy ngang hoặc chạy chéo.
# Toạ độ khăn (UV) = điểm trải phẳng trên mặt phẳng bàn, đơn vị mét, đưa về 0..1 theo cỡ ghi trong số đo (khan_uv_cao).
# Chạy: GOC_3D=10 <venv có bpy>/bin/python ban_dai_3d.py <thư mục ra>   (GOC_3D: độ chếch máy ảnh, xem xuong_3d.py)
import sys, os, math, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
import numpy as np
import xuong_3d as X

RA = sys.argv[-1] if len(sys.argv) > 1 and not sys.argv[-1].endswith('.py') else '.'
os.makedirs(RA, exist_ok=True)
H = 0.76; RONG = 0.9                       # cao, rộng bàn (m)


def khan_dai(dai, rong, mat, seed=1, bien=0.04, bo=0.06):
    """Khăn chữ nhật phủ chấm đất có nếp. Đường viền mép bàn là hình chữ nhật bo góc; phần rủ đi theo pháp tuyến ra ngoài."""
    rng = np.random.RandomState(seed); a, b = dai / 2 - bo, rong / 2 - bo
    # đường quanh mép: 4 cạnh + 4 cung góc, lấy điểm đều theo độ dài
    chu = 2 * (2 * a + 2 * b) + 2 * math.pi * bo; n = int(chu / 0.012); nH = 30
    def mep(s):   # s ∈ [0, chu) → (điểm, pháp tuyến)
        doan = [(2 * a, 'canh', (-a, -b - bo), (1, 0), (0, -1)), (math.pi * bo / 2, 'goc', (a, -b), -math.pi / 2, None),
                (2 * b, 'canh', (a + bo, -b), (0, 1), (1, 0)), (math.pi * bo / 2, 'goc', (a, b), 0, None),
                (2 * a, 'canh', (a, b + bo), (-1, 0), (0, 1)), (math.pi * bo / 2, 'goc', (-a, b), math.pi / 2, None),
                (2 * b, 'canh', (-a - bo, b), (0, -1), (-1, 0)), (math.pi * bo / 2, 'goc', (-a, -b), math.pi, None)]
        for L, kieu, p0, h, nrm in doan:
            if s <= L:
                if kieu == 'canh': return (p0[0] + h[0] * s, p0[1] + h[1] * s), nrm
                g = h + s / bo; return (p0[0] + bo * math.cos(g), p0[1] + bo * math.sin(g)), (math.cos(g), math.sin(g))
            s -= L
        return mep(0)
    pha = rng.uniform(0, 2 * math.pi, 2); buoc_nep = 0.34
    V, F, UV = [], [], []
    # mặt bàn: lưới chữ nhật
    nx, ny = int(dai / 0.03), int(rong / 0.03)
    for j in range(ny + 1):
        for i in range(nx + 1):
            x = -dai / 2 + dai * i / nx; y = -rong / 2 + rong * j / ny
            V.append((x, y, H)); UV.append((x, y))
    for j in range(ny):
        for i in range(nx):
            k = j * (nx + 1) + i; F.append((k, k + 1, k + nx + 2, k + nx + 1))
    goc0 = len(V)
    for jj in range(nH + 1):
        t = jj / nH
        for i in range(n):
            s = chu * i / n; (px, py), (qx, qy) = mep(s)
            f = 0.65 * math.sin(2 * math.pi * s / buoc_nep + pha[0]) + 0.35 * math.sin(2 * math.pi * s / (buoc_nep * 0.57) + pha[1])
            dd = 0.004 + 0.04 * t + bien * (t ** 1.2) * f
            z = H * (1 - t) if jj < nH else 0.003 * math.sin(3 * s)
            V.append((px + qx * dd, py + qy * dd, max(0.0, z)))
            UV.append((px + qx * t * H, py + qy * t * H))
        if jj:
            a0, a1 = goc0 + (jj - 1) * n, goc0 + jj * n
            for i in range(n): F.append((a0 + i, a0 + (i + 1) % n, a1 + (i + 1) % n, a1 + i))
    me = bpy.data.meshes.new('khan'); me.from_pydata(V, [], F); me.update()
    cao = max(dai, rong) / 2 + H + 0.1
    uvl = me.uv_layers.new(name='trai')
    for poly in me.polygons:
        poly.use_smooth = True
        for li in poly.loop_indices:
            x, y = UV[me.loops[li].vertex_index]; uvl.data[li].uv = (0.5 + 0.5 * x / cao, 0.5 - 0.5 * y / cao)   # v: phía máy ảnh (−y) là dương, như khăn tròn
    # nét nếp ở mặt trước (phía máy ảnh), 60% số hõm, từ 35% độ rủ xuống
    dau = [False] * len(me.edges); canh = {tuple(sorted(e.vertices)): e.index for e in me.edges}
    for i in range(n):
        s = chu * i / n; f = math.sin(2 * math.pi * s / buoc_nep + pha[0])
        if f > -0.985 or rng.rand() > 0.6: continue
        for jj in range(int(0.35 * nH), nH):
            e = canh.get(tuple(sorted((goc0 + jj * n + i, goc0 + (jj + 1) * n + i))))
            if e is not None: dau[e] = True
    at = me.attributes.get('freestyle_edge') or me.attributes.new('freestyle_edge', 'BOOLEAN', 'EDGE'); at.data.foreach_set('value', dau)
    o = bpy.data.objects.new('khan', me); bpy.data.collections['net'].objects.link(o); me.materials.append(mat)
    return o, cao


if __name__ == '__main__':   # để tệp khác nhập được khan_dai mà không chạy cả lô vẽ
    BO = [(8, 0.0), (12, 0.0), (20, 0.0), (12, math.radians(-28))]     # số khách, góc xoay (0 = chạy ngang khung hình)
    so = {}
    for khach, xoay in BO:
        sc = X.moi(); X.ID.clear()
        vai = X.vat_lieu('khan', (0.94, 0.92, 0.87), 0.85, (1, 0, 0))
        khung = X.vat_lieu('khung', (0.84, 0.76, 0.60), 0.45, (0, 0, 1))
        dem = X.vat_lieu('dem', (0.93, 0.91, 0.86), 0.8, (0, 1, 0))
        moi_ben = khach // 2; dai = moi_ben * 0.62 + 0.3
        khan, cao = khan_dai(dai, RONG, vai, seed=khach)
        ghe = X.ghe_chiavari(khung, dem)
        for i in range(moi_ben):
            x = -dai / 2 + 0.15 + 0.31 + i * 0.62
            X.nhan_ban(ghe, (x, -RONG / 2 - 0.3, 0), math.pi)        # ghế mẫu có mặt hướng −y: hàng trước quay 180° để mặt hướng vào bàn
            X.nhan_ban(ghe, (x, RONG / 2 + 0.3, 0), 0.0)
        for o in ghe: bpy.data.objects.remove(o)
        if xoay:
            goc = bpy.data.objects.new('xoay', None); bpy.data.collections['net'].objects.link(goc)
            for o in list(bpy.data.objects):
                if o.parent is None and o.name not in ('xoay', 'sun', 'dat') and o.type in ('MESH', 'CURVE', 'EMPTY') and o != goc: o.parent = goc
            goc.rotation_euler = (0, 0, xoay)
        m = X.may_anh(sc)
        ten = f'ban-dai-{khach}' + ('-cheo' if xoay else '')
        X.ve(sc, os.path.join(RA, ten), uv_vat=khan)
        m.update(dai=round(dai, 2), rong=RONG, khach=khach, xoay_do=round(math.degrees(xoay)), khan_uv_cao=round(cao, 4)); so[ten] = m
        print(ten, m)
    json.dump(so, open(os.path.join(RA, 'ban-dai.json'), 'w'), ensure_ascii=False, indent=1)
    print('xong')
