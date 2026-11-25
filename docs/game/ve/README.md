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
| Bản đêm bằng mã (thử 25/11) | `python3 dem_ma.py <nen-ho.webp>` → `dem-ma.jpg`, `nen-ho-dem.webp`. Tách trời theo màu (trời lam trội, mây đỏ trội), thay bằng trời đêm; phần còn lại tô tối ngả lam; đèn lan can, đèn làng xa có vệt phản chiếu. In ra hệ số chỉnh sáng món rời. |
| Ghế 3D (thử 25/11) | `<venv>/bin/python ghe_3d.py <thư mục ra>`; cần `pip install bpy` trong venv riêng (không đưa venv vào repo). Ghế chiavari dựng bằng mã, vẽ bằng Cycles CPU + nét Freestyle, 8 góc, nền trong suốt, kèm ảnh mặt nạ đệm cho từng góc. Khoảng 1 phút cho 8 góc. |

Kinh nghiệm viết câu lệnh: mô hình không giữ vị trí và cỡ của vật khi được bảo xoá hết phần còn lại (nó vẽ vật to gần kín khung), nên vị trí và cỡ luôn do mã đặt. Lần sau nên yêu cầu phần cần đổi tông (khăn, hoa) màu trắng và đặt trên vật có màu khác hẳn.

Quy tắc dùng lượt vẽ nằm ở `../canh-ngoai-troi.md`, mục 4. Mỗi ảnh tốn khoảng 0,24% gói tháng (đo ngày 24/11/2026).
