# Quy trình vẽ và tách lớp (Model Studio)

Các script đã dùng để tạo tranh cho `game/lab/xuong/`. Chạy trong một thư mục làm việc riêng (không chạy trong repo), nơi chứa các ảnh PNG gốc do mô hình trả về. Ảnh PNG gốc (2736 px, mỗi ảnh khoảng 3 MB) không nằm trong repo.

| Tệp | Việc |
|---|---|
| `gen.py` | Gọi `qwen-image-3.0-pro` qua cổng Token Plan. Đầu vào là một tệp JSON gồm các dòng `[tên, câu lệnh, ảnh gốc để sửa]`. Khoá API do môi trường tự gắn, không nằm trong mã. Biến `SONG` là số ảnh chạy cùng lúc (nên để 1–2 vì giới hạn tốc độ). |
| `lenh/*.json` | Toàn bộ câu lệnh đã dùng (`nv-*` cho nhân vật, `canh-*` cho cảnh), để vẽ lại hoặc vẽ tiếp cho đúng nét. |
| `key.py` | Tách nền xanh lá thành trong suốt. |
| `prep.py` | Tách nền và hoà tông ảnh nhân vật. |
| `toc.py` | Tìm vùng tóc bằng cách loang từ đỉnh đầu. |
| `process2.py` | Cắt lớp đầu, lớp thân và lớp cổ áo dài; xuất `.webp` và `meta.json`. |
| `patches.py` | Cắt mảnh mắt, lông mày và dò vị trí khớp trên từng đầu; xuất `manh.json`. |
| `co_lai.py` | Dựng lại riêng lớp cổ áo dài. |

### Sửa lông mày và đóng gói (bản 14, không dùng AI)

Chạy theo thứ tự: `luu_prep.py` → `may_moi.py` → `dong_goi.py <thư mục bản chơi>`.

| Tệp | Việc |
|---|---|
| `luu_prep.py` | Lưu sẵn ảnh đã tách nền của 54 đầu và 18 ảnh lông mày vào `work/`. |
| `may_lib.py` | Toạ độ mắt, lông mày của từng đầu trong ảnh nguồn. |
| `may_xoa.py` | Tách nét lông mày khỏi tóc, mi mắt và da; xoá lông mày, lấp da bằng nội suy Laplace. |
| `may_net.py` | Cắt lông mày thành lớp chỉ có nét (không da, không tóc). |
| `may_sua.py` | Chỉnh tay cho ảnh nguồn mà quy tắc chung chưa xử lý được (hiện để trống). |
| `may_moi.py` | Xoá lông mày gốc trên 9 đầu chú rể Vuốt ngược; xuất lớp nét `mayA`. Phần thử cho cô dâu (`mayS`) không dùng, ghi chú trong tệp. |
| `dong_goi.py` | Gom mảnh mắt, lông mày thành tấm ghép `manh-*.webp`; dựng tấm cỡ nhỏ `nho-*.webp`; cắt hình thẻ địa điểm `anh/t-*.webp`; thu nhỏ hình người phục vụ; ghi `manh.json`. |

### Trang trí theo lớp (bước thử ở Vườn Hồ và Sân nhà quê)

Bốn ảnh mô hình trả về (`lenh/tt-j1.json`): `nen-ho.png`, `nen-langque.png` (nền trống), `cong-tron.png` và `ban-dai.png` (hình rời trên nền xanh dương). Chạy `python3 trang_tri.py <thư mục bản chơi>` trong thư mục chứa các ảnh đó.

| Việc | Cách làm |
|---|---|
| Tách nền | Alpha theo khoảng cách màu tới màu nền thật; gỡ màu nền khỏi viền; gỡ ánh xanh dương trên toàn vật (mô hình vẽ lá ngoài rìa nhuốm màu nền). Đồ có lá thì không dùng nền xanh lá. |
| Mặt nạ đổi tông | Hoa: tự động, theo màu và mật độ (cỏ lau, khung vàng không bị nhuộm). Khăn bàn: khoanh tay một đa giác cho mỗi kiểu bàn, vì gỗ sáng, đĩa và khăn có màu quá gần nhau. |
| Bóng chân | Nướng sẵn vào hình rời, nằm ngay dưới vật nên lật gương vẫn dùng được. |
| Số đo | Script in ra cỡ, điểm neo và số px mỗi mét; chép vào `TT` trong `index.html` của bản chơi. |
| Chỉnh sáng theo cảnh | Bản chơi nhân màu món rời với một hệ số riêng của từng nơi (`sang` trong `LOP`). Hệ số là tỉ lệ màu khăn trắng của nơi đó so với Vườn Hồ, đo trên tranh gốc. |
| Hoạ tiết khăn (thử 25/11) | `python3 hoa_tiet.py` trong cùng thư mục, cạnh `trang_tri.py` và `hoa_van.py` (các hoạ tiết dùng chung). Mỗi điểm trên khăn chạy bàn có toạ độ vải (dọc, ngang, mét) theo phối cảnh, đo tay trên tấm bàn dài: hai mép khăn, chỗ gập, các đĩa đè lên mép khăn. Hoạ tiết sinh theo toạ độ đó rồi nhuộm bằng công thức đổi tông. Ra `khan-hoatiet.jpg` với 8 mặt vải. 0 lượt vẽ. |
| Khăn nhiều lớp (thử 25/11) | `python3 khan_lop.py` → `khan-lop.jpg`. Đầu vào là `mau/ban-tron-gon.webp`: bàn tròn cắt từ ảnh gốc 2736×1520 của cảnh gọn, không nén mất dữ liệu. Mỗi điểm trên khăn được trải phẳng về mặt bàn (phần rủ = vải thừa ra ngoài mép), nên khăn phủ, khăn chạy bàn chỉ là hình phẳng. Mặt nạ khăn tách khỏi ghế bằng các luật và số đo riêng của tấm này; bàn vẽ rời (T8, T9) không cần. |
| Ghế theo lớp (thử 25/11) | `python3 ghe_lop.py` → `ghe-lop.jpg`, dùng cùng ảnh mẫu. Đổi màu khung, đệm; đai và nơ vẽ bằng mã (kết quả: nơ trông như hình dán, nên nơ phải vẽ). Số đo lưng ghế là của riêng tấm này. |
| Khung cổng bằng mã (thử 25/11) | `python3 khung_ma.py <nen-ho.webp> <cong-tron.webp>` → `khung-ma.jpg`. Khung lục giác, tròn, tam giác: ống kim loại có viền mực, vệt sáng, vệt tối, nét hơi rung, vân giấy; đặt đúng thước phối cảnh của game. |
| Bản đêm bằng mã (25/11) | `python3 dem_ma.py <nền trống 1600×889> <ho|langque>` → `dem-ma-<nơi>.jpg`, `nen-<nơi>-dem.webp`. Vườn Hồ: tách trời theo màu (trời lam trội, mây đỏ trội). Sân nhà quê: trời sáng không phải lá, nối với mép trên hoặc cao hơn mái nhà. Đèn lan can, đèn cổng, cửa sổ sáng, đèn làng xa. In ra hệ số chỉnh sáng món rời. |
| Ghế 3D (thử 25/11) | `<venv>/bin/python ghe_3d.py <thư mục ra>`; cần `pip install bpy` trong venv riêng (không đưa venv vào repo). Ghế chiavari dựng bằng mã, vẽ bằng Cycles CPU + nét Freestyle, 8 góc, nền trong suốt, kèm ảnh mặt nạ đệm cho từng góc. Khoảng 1 phút cho 8 góc. |
| Xưởng 3D dùng chung (25/11) | `xuong_3d.py`: ghế chiavari, khăn tròn có nếp (toạ độ UV = toạ độ trải phẳng), máy ảnh trực giao chếch 15° với 260 px mỗi mét cho mọi món, ba lượt vẽ: tranh (Cycles CPU + nét Freestyle), mặt nạ màu ID, toạ độ khăn 16 bit. |
| Bàn tròn, bàn dài 3D (25/11) | `<venv>/bin/python ban_tron_3d.py <ra>` (6, 10, 12 khách) và `ban_dai_3d.py <ra>` (8, 12, 20 khách, ngang và chéo). Mỗi bộ: `.png`, `-id.png`, `-uv.png` và số đo kiểu `TT` (w, h, pxm, ax, ay) trong `ban-tron.json`, `ban-dai.json`. |
| Cận cảnh bàn 3D (25/11) | `<venv>/bin/python can_canh_3d.py [au,viet] <ra>`: một chỗ ngồi ở giữa, hai chỗ bên bị khung cắt; kiểu Âu (đĩa lót viền hạt, đĩa, khăn ăn, thiệp, dao nĩa, 3 ly, đĩa bánh mì) và kiểu Việt (đĩa kê, chén, thìa, đũa, chén nước chấm, ly). Khoảng 2,5 phút mỗi kiểu. |
| Ghép cảnh từ đồ tự vẽ (25/11) | `python3 canh_3d.py <thư mục bàn 3D> <nen-ho.webp> <nen-ho-dem.webp>` → `canh-3d.jpg`. Khăn nhiều lớp và đệm đổi màu đọc thẳng mặt nạ và ảnh toạ độ khăn của 3D (`bo_ban`, có thêm `nhuom_id` để đổi màu đĩa lót, dao nĩa). Cần `pypng` để đọc ảnh 16 bit. |
| Đưa vào trang thử (26/11) | `python3 xuat_lab.py <bản chơi> <thư mục nền đêm> <bàn tròn 3D> <bàn dài 3D> <cận cảnh 3D> <t14-xuat.png> [nen,khung,ban,gan,vai]` → `anh/`, `anh/tt/` của bản chơi và `tt-lab.json` (số đo, chép vào `SO3` trong `index.html`). Khung cổng vẽ ở 2× thước cũ, 4 màu; cụm hoa Canva gắn sẵn theo từng khung, mặt nạ cánh mẫu đơn hồng riêng (mặt nạ cũ làm cho hoa trắng). Bàn và cận cảnh: mặt nạ 3 kênh và toạ độ khăn gói 12 bit (R, G = bit cao của u, v; B = 4 bit thấp mỗi số), lưu không nén mất dữ liệu, kèm một điểm mẫu để trang tự kiểm. Mặt nạ cận cảnh bóc phần ly trong suốt trước rồi chia khăn, đĩa lót, dao nĩa. Ô hoạ tiết vải (ren, kim sa, gấm) lặp liền mạch, 512 px và 128 px. Khoảng 4 phút cho cả bộ. |
| Loa 3D (26/11) | `<venv>/bin/python loa_3d.py <ra>` → `loa-keo`, `loa-chan`, `loa-sub` (`.png`, `-id.png`) và `loa.json`; cùng máy ảnh, cùng thước với bàn ghế. Đưa vào trang thử bằng `LOA_3D=<ra> python3 xuat_lab.py … loa`. Đèn và màn LED vẽ bằng mã ngay trong trang (`index.html`, các hàm `veDen`, `noiDungLED`), không có tệp tranh. |
| Ghế 16 hướng (26/11) | `<venv>/bin/python ghe_xoay_3d.py <ra>` → `ghe-0..15.png`, `-id.png`, `ghe.json`: ghế chiavari của bộ bàn quay mỗi bước 22,5°. `GHE_3D=<ra> python3 xuat_lab.py … ghe` gộp thành một tấm ngang `ghe-xoay.webp` + mặt nạ `ghe-xoay-mn.webp` (lục: đệm, lam: khung) và ghi vị trí từng hướng vào `SO3.ghe`. Bản chơi xếp ghế dự lễ bằng hàm `xepLe` và chiếu theo phối cảnh của tranh (`PC_K`). |
| Bàn dài xuyên suốt (26/11) | `<venv>/bin/python ban_xuyen_3d.py [thu] <ra>` → `ban-xuyen-giua`, `ban-xuyen-doc` (`.png`, `-id.png`, `-uv.png`, đầy khung 1600 × 889) và `ban-xuyen.json`. Máy ảnh phối cảnh khớp tranh: cao 1/0,307 m, tiêu cự 1,1 bề ngang khung, chân trời ở 44% (dịch ống kính, không ngửa máy). `thu`: 8 mẫu, không nét, để soát vị trí trước. `XUYEN_3D=<ra> python3 xuat_lab.py … xuyen` cắt gọn theo vùng có hình, ghi vị trí cắt (`ox`, `oy`) và làm hình thẻ. `khan_dai` lấy từ `ban_dai_3d.py` (đã thêm `if __name__ == '__main__'` để nhập được). |
| Luống hoa T15 (26/11) | Ảnh Canva 6 khóm hoa trắng (`t15-xuat.png`, nền xanh đậm). `T15=<ảnh> python3 xuat_lab.py … luong` tách nền (`trang_tri.tach(…, nguong=90)`), cắt 6 khóm, gộp thành `luong.webp` + mặt nạ cánh `luong-mn.webp`, ghi `SO3.luong` (bề rộng thật 0,65 m mỗi khóm). Bản chơi xếp khóm trong hàm `veGhe`, chung thứ tự xa gần với ghế dự lễ. |
| Hoa bàn T3 (26/11) | Ảnh Canva 6 món trên nền xanh (`t3-xuat.png`). `T3=<ảnh> python3 xuat_lab.py … hoaban` tách nền (`trang_tri.tach(…, nguong=90, ra_hop=True)`), làm kính trong suốt, cắt 6 món theo thứ tự hàng rồi cột, gộp thành `hoaban.webp` + mặt nạ cánh `hoaban-mn.webp` (bỏ thân nến, đáy bình, mái đèn lồng), hình thẻ `t-hoaban-0..5.webp`, ghi `SO3.hoaban` (mỗi món: vị trí, cỡ, điểm đáy, bề rộng thật). Bản chơi đặt hoa trong `veGhe` ngay sau bàn của nó, bàn xuyên suốt trong `veDen`. |

Kinh nghiệm viết câu lệnh: mô hình không giữ vị trí và cỡ của vật khi được bảo xoá hết phần còn lại (nó vẽ vật to gần kín khung), nên vị trí và cỡ luôn do mã đặt. Lần sau nên yêu cầu phần cần đổi tông (khăn, hoa) màu trắng và đặt trên vật có màu khác hẳn.

Quy tắc dùng lượt vẽ nằm ở `../canh-ngoai-troi.md`, mục 4. Mỗi ảnh tốn khoảng 0,24% gói tháng (đo ngày 24/11/2026). **Trần: game dùng tối đa 40% gói mỗi tháng (khoảng 166 hình).** `gen.py` ghi sổ `so-luot.json` cạnh nó (theo đường dẫn thật, nên bản sao dạng liên kết vẫn ghi đúng sổ) và từ chối lô vượt trần trước khi gọi. Sau mỗi lô, đưa `so-luot.json` vào repo.
