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
| `may_moi.py` | Xoá lông mày gốc trên 9 đầu chú rể Vuốt ngược; xuất lớp nét `mayA` và mảnh `mayS` cho cô dâu tóc Dài thẳng. |
| `dong_goi.py` | Gom mảnh mắt, lông mày thành tấm ghép `manh-*.webp`; dựng tấm cỡ nhỏ `nho-*.webp`; cắt hình thẻ địa điểm `anh/t-*.webp`; thu nhỏ hình người phục vụ; ghi `manh.json`. |

Quy tắc dùng lượt vẽ nằm ở `../canh-ngoai-troi.md`, mục 4. Mỗi ảnh tốn khoảng 0,24% gói tháng (đo ngày 24/11/2026).
