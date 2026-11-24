# Vòng chơi, dữ liệu, giao diện 2D và danh sách cảnh

**Bản nháp chờ chủ dự án duyệt (24/11/2026).** Tài liệu này cập nhật [spec.md](spec.md) theo hướng hình ảnh mới: tranh vẽ tay cho cảnh và nhân vật, còn đồ hoạ 2D vẽ bằng mã cho các lựa chọn. Chưa vẽ gì cho tới khi tài liệu được duyệt.

## 1. Vòng chơi

### 1.1 Vòng lớn: 6 chương

Giữ khung 6 chương của spec. Mỗi chương gồm vài **màn**. Màn là một lần người chơi ra quyết định, kèm một cảnh để nhìn.

| Chương | Các màn | Cảnh (mục 4) | Quyết định chính | Chỉ số bị ảnh hưởng |
|---|---|---|---|---|
| 1. Gặp gỡ | Tạo nhân vật → gặp gỡ → hẹn hò (3–5 lần) | C1–C3 | Ngoại hình (Xưởng nhân vật), quê, nghề, tiền tiết kiệm; gặp ai; hẹn ở đâu, nói gì | Tiền, Tình cảm, Căng thẳng |
| 2. Yêu và cầu hôn | Ra mắt nhà gái → ra mắt nhà trai → chọn nhẫn → cầu hôn | C4–C6 | Quà ra mắt, cách thưa chuyện; nhẫn; nơi và cách cầu hôn | Tiền, Tình cảm, Lòng hai họ |
| 3. Hai họ và kế hoạch | Dạm ngõ → xem tuổi, xem ngày → bàn với hai họ → đặt ngân sách | C7–C9 | Lễ vật dạm ngõ; nguồn xem ngày; ngày cưới, số khách, tiệc chung hay riêng, quê hay phố | Lòng hai họ, Căng thẳng |
| 4. Nhà cung cấp | Chọn địa điểm → chọn gói hoặc may đo → so giá, mặc cả → ký hợp đồng | C10 + cảnh tiệc | Địa điểm, gói Gọn, Đủ, Trọn, nhà cung cấp từng hạng mục | Tiền, Căng thẳng |
| 5. Gom tiền và chuẩn bị | Đóng tiền theo mốc → kiếm thêm → chăm sóc bản thân → chụp ảnh cưới → đăng ký kết hôn | C11–C13 | Làm thêm hay nghỉ, tập luyện, chụp ảnh ở đâu | Tiền, Căng thẳng, Tình cảm |
| 6. Mùa cưới | Ăn hỏi → gia tiên nhà gái → rước dâu → gia tiên nhà trai → tiệc → (lại mặt) → tổng kết | C14–C20 | Xử lý sự cố, các bước nghi lễ ngắn, chào bàn | Lòng hai họ, Căng thẳng, Tiền mừng |

### 1.2 Vòng nhỏ: một màn

Mọi màn đi theo cùng một nhịp, để người chơi quen tay:

1. **Cảnh:** tranh vẽ tay, có cặp đôi và người liên quan đứng đúng chỗ.
2. **Tình huống:** 1–2 câu thoại hoặc một dòng mô tả.
3. **Lựa chọn:** 2–4 thẻ đồ hoạ 2D (mục 3). Mỗi thẻ ghi rõ giá và ước tính ảnh hưởng ("hai họ vui hơn", "tốn thêm 4 triệu").
4. **Phản hồi:** cảnh đổi theo lựa chọn (đổi gói trang trí, thêm người, đổi trang phục), chỉ số chạy lên hoặc xuống, có một câu nhận xét của người trong cảnh.
5. **Sang màn sau** hoặc quay lại sửa, nếu chưa ký hợp đồng.

### 1.3 Thời gian và lịch

- Lịch tính theo **tuần trong game**. Mỗi màn tốn một số ngày.
- Ngày cưới chốt ở chương 3 thành mốc đếm ngược. Các mốc đóng tiền của chương 5 rải trên lịch này.
- Lịch âm, ngày giờ hoàng đạo dùng mô-đun `game/js/lich.js` đã có.

### 1.4 Thắng, thua và kết

- Không có "thua". Hết tiền thì vay hoặc cắt hạng mục, có hậu quả vào Căng thẳng và Lòng hai họ.
- Kết thúc là một **album tổng kết**: ảnh từng lễ ghép từ cảnh và nhân vật của chính người chơi, bảng chi tiêu, tiền mừng, và nhận xét của hai họ.
- Album này là phần thưởng cảm xúc. Nó cũng là chỗ nối sang website: "lên kế hoạch thật với Timeless Harmony".

## 2. Dữ liệu cần chốt trước khi vẽ

Mọi bảng nằm trong `game/data/*.json`. Giá lấy từ [gia-tham-khao.md](gia-tham-khao.md); ô nào chưa có nguồn thì dùng **số tạm** và gắn cờ `tam: true` để thay sau. Không tự đặt số khác.

### 2.1 Địa điểm tiệc ngoài trời

| Mã | Tên hư cấu (đề xuất) | Vùng | Sức chứa (khách) | Giá (số tạm) | Mùa đẹp | Rủi ro | Cảnh |
|---|---|---|---|---|---|---|---|
| `dalat` | Đồi Thông Sương | Tây Nguyên | 30–120 | sân vườn 0,8–2 / khách | khô | sương sớm, lạnh tối | `dd-dalat` |
| `hoian` | Bến Đèn Lồng | Miền Trung | 30–80 | 0,8–2 / khách | đầu năm tới giữa năm | mùa mưa bão, ngập phố | `dd-hoian` |
| `bien` | Bãi Dừa Xanh | Trung, Nam | 30–150 | 0,8–2 / khách | mùa khô của vùng | gió biển, nắng gắt | `dd-bien` |
| `langque` | Sân nhà (quê Bắc Bộ) | Bắc Bộ | 100–400 | nấu tại nhà 1,5–4 / bàn + rạp 5–20 | xuân, thu | mưa phùn, nồm | `dd-langque` |
| `mientay` | Vườn Sông Quê | Nam Bộ | 50–300 | 1,5–4 / bàn + rạp | mùa khô | mưa chiều mùa mưa | `dd-mientay` |
| `ho` | Vườn Hồ (cảnh website) | — | 30–120 | 0,8–2 / khách | — | — | `canh-*` |

"Mùa đẹp" và "rủi ro" chỉ là mô tả chung, không kèm số liệu khí tượng.

### 2.2 Điểm chụp ảnh cưới

| Mã | Tên | Chi phí đi lại (số tạm) | Ngày nghỉ | Cảnh |
|---|---|---|---|---|
| `ruongbac` | Ruộng bậc thang Tây Bắc | 4–8 / hai người | 3 | `dd-ruongbac` |
| `ninhbinh` | Núi đá Tràng An | 2–5 / hai người | 2 | `dd-ninhbinh` |
| `dalat` | Đà Lạt | giá album Đà Lạt 6–40 (có nguồn) | 3 | `dd-dalat` |
| `pho` | Studio trong phố | album 5–13 (có nguồn) | 1 | (cần cảnh mới) |

### 2.3 Gói trang trí theo địa điểm

Mỗi địa điểm có 3 gói, giá lấy từ dòng "Trang trí … cổng hoa" của bảng giá tham khảo (3–12 triệu).

| Gói | Thấy gì trên cảnh | Giá (số tạm) |
|---|---|---|
| Gọn | cổng đơn giản, không hoa bàn | 3–4 |
| Đủ | cổng hoa, chậu hoa dọc lối, hoa bàn | 7–9 |
| Trọn | cổng dày hoa, đèn, cánh hoa, hoa bàn cao | 12–18 |

### 2.4 Nhà cung cấp

- Giữ cấu trúc của `suppliers.js` để sau này thay bằng nhà cung cấp thật.
- Mỗi hạng mục có 2–3 nhà cung cấp hư cấu, khác nhau ở giá, độ tin cậy (xác suất sự cố) và phong cách.
- Các hạng mục gồm: địa điểm, trang trí, ẩm thực, MC và ban nhạc, ảnh và phim, trang phục, trang điểm, mâm quả, xe hoa, thiệp, người lên kế hoạch.

### 2.5 Nghi lễ và lễ vật

| Lễ | Lựa chọn | Dữ liệu cần |
|---|---|---|
| Dạm ngõ | lễ vật trầu cau, chè, rượu, bánh | giá (số tạm), bên nào coi trọng |
| Ăn hỏi | số mâm quả (5, 7, 9, 11), đội bưng quả | 3–8 trọn gói, 1,5–3 đội bưng quả |
| Gia tiên, rước dâu | giờ hoàng đạo, số xe | 1,5–2,5 / xe hoa |
| Lại mặt | giữ, làm gọn, bỏ | — |

**Việc cần bạn chốt ở mục 2:**
- tên hư cấu của các địa điểm;
- những vùng nào làm trước;
- số tạm nào cần thay bằng báo giá thật trước khi chơi thử với người ngoài.

## 3. Giao diện lựa chọn bằng đồ hoạ 2D (không dùng Model Studio)

Thay danh sách chữ bằng **thẻ có hình**, vẽ bằng mã (SVG và canvas) theo bảng màu Timeless Harmony. Không tốn lượt vẽ.

| Thành phần | Cách vẽ | Ví dụ |
|---|---|---|
| **Thẻ lựa chọn** | khung bo tròn; hình minh hoạ trên, tên, giá và tác động bên dưới; khi chọn thì nổi lên, viền vàng đồng | gói Gọn, Đủ, Trọn; nhà cung cấp |
| **Biểu tượng hạng mục** | SVG nét đơn, một màu theo `currentColor`, bộ khoảng 40 hình: cổng hoa, bàn tiệc, micro, máy ảnh, nhẫn, mâm quả, xe hoa, áo dài, vest, bánh cưới, thiệp, lư hương… | thanh hạng mục chương 4 |
| **Hình thu nhỏ cắt từ tranh có sẵn** | máy cắt và thu nhỏ từ cảnh đã vẽ (cổng, bàn, cảnh nền) | thẻ địa điểm, thẻ gói trang trí |
| **Hình nhân vật thu nhỏ** | lấy từ Xưởng nhân vật, cắt ngang ngực | thẻ thoại, thẻ người thân |
| **Đồng hồ chỉ số** | vòng tròn và thanh có màu theo chỉ số; khi đổi thì chạy số và hiện mũi tên | Tiền, Tình cảm, Lòng hai họ, Căng thẳng |
| **Lịch và đếm ngược** | lịch dương và âm vẽ bằng mã, ngày hoàng đạo có dấu riêng | chương 3, 5 |
| **Mâm quả, bàn thờ** | dựng bằng SVG từ hình khối đơn giản (mâm tròn, tráp đỏ, nắp, chữ Song Hỷ) | chọn số mâm quả |
| **Hợp đồng** | tờ giấy có điều khoản, chỗ ký và con dấu đỏ vẽ bằng mã | chương 4 |
| **Phong bì tiền mừng** | phong bì đỏ, bay lên rồi xếp chồng khi đếm | tổng kết |

**Nguyên tắc:**
- Hình 2D đi kèm tranh vẽ tay, không thay tranh; nét đơn và màu phẳng để không tranh chấp với tranh.
- Mỗi thẻ đọc được cả ở chế độ sáng và tối, và ở bản nhẹ không có làm mờ.
- Bộ biểu tượng vẽ một lần, dùng chung cho game và website.

**Đã dựng mẫu** ở `game/lab/xuong/`: bốn bước Cặp đôi → Địa điểm → Trang trí → Ngày cưới, thẻ hình, đồng hồ chỉ số, bộ biểu tượng nét đơn. Chờ chủ dự án duyệt rồi mới làm các màn còn lại (lịch, mâm quả, hợp đồng, phong bì).

## 4. Danh sách cảnh theo giai đoạn

Hiện mới có cảnh tiệc ngoài trời. Các giai đoạn khác cần cảnh riêng. Mọi cảnh giữ chung một quy ước:
- góc máy ngang tầm mắt, hơi cao;
- nắng từ phía sau bên phải;
- có chỗ đứng cho cặp đôi ở giữa, đo thước tỉ lệ ngay khi vẽ xong.

| # | Giai đoạn | Cảnh | Ai có mặt | Biến thể | Sửa từ | Ước tính ảnh |
|---|---|---|---|---|---|---|
| C1 | Gặp gỡ | Quán cà phê phố | cặp đôi | ngày, tối | vẽ mới | 2 |
| C2 | Gặp gỡ | Văn phòng / quán ăn trưa | cặp đôi, đồng nghiệp | — | vẽ mới | 1 |
| C3 | Hẹn hò | Công viên bờ hồ, rạp phim, phố đêm | cặp đôi | 3 nơi | vẽ mới | 3 |
| C4 | Ra mắt | Phòng khách nhà gái (thành phố hoặc quê) | cặp đôi, bố mẹ cô dâu | phố, quê | vẽ mới | 2 |
| C5 | Chọn nhẫn | Tiệm vàng | cặp đôi, người bán | — | vẽ mới | 1 |
| C6 | Cầu hôn | Sân thượng thành phố, bãi biển, đồi thông | cặp đôi | 3 nơi × 2 gói (thường, dựng cảnh) | đồi thông, biển: sửa từ cảnh tiệc có sẵn | 5 |
| C7 | Dạm ngõ | Phòng khách nhà gái, bàn trà, trầu cau | hai họ (bố mẹ hai bên), cặp đôi | phố, quê | sửa từ C4 | 2 |
| C8 | Xem ngày | Nhà thầy xem ngày / điện thoại | thầy, bố mẹ | — | vẽ mới; điện thoại là giao diện 2D | 1 |
| C9 | Bàn với hai họ | Bữa cơm hai gia đình | hai họ, cặp đôi | — | vẽ mới | 1 |
| C10 | Nhà cung cấp | Không cần tranh: thẻ 2D và cảnh tiệc xem trước | — | — | — | 0 |
| C11 | Chụp ảnh cưới | Ruộng bậc thang, Tràng An, Đà Lạt, studio phố | cặp đôi, thợ ảnh | 4 nơi | 3 nơi đã có; studio vẽ mới | 1 |
| C12 | Chăm sóc bản thân | Phòng tập, spa | từng người | — | vẽ mới | 2 |
| C13 | Đăng ký kết hôn | Phòng tiếp dân uỷ ban phường | cặp đôi, cán bộ | — | vẽ mới | 1 |
| C14 | Ăn hỏi | Cổng nhà gái: đội bưng quả xếp hàng, mâm quả đỏ | đội bưng quả, hai họ | phố, quê | vẽ mới; người bưng quả tách lớp | 2 + đội bưng quả 2 |
| C15 | Gia tiên nhà gái (vu quy) | Bàn thờ gia tiên trong nhà gái, hương, mâm quả mở nắp | cặp đôi, bố mẹ cô dâu, đại diện hai họ | phố, quê | vẽ mới | 2 |
| C16 | Rước dâu | Ngõ nhà gái, xe hoa, đoàn nhà trai | cặp đôi, hai họ | phố, quê | vẽ mới | 2 |
| C17 | Gia tiên nhà trai (tân hôn) | Bàn thờ nhà trai | cặp đôi, bố mẹ chú rể | phố, quê | sửa từ C15 | 2 |
| C18 | Tiệc ngoài trời | Đã có 6 địa điểm × 3 gói | — | — | đã xong | 0 |
| C19 | Tiệc trong nhà | Nhà hàng, sảnh khách sạn, rạp cưới quê | — | — | làm sau, theo lời bạn | — |
| C20 | Lại mặt, trăng mật | Bữa cơm nhà gái; biển đảo | cặp đôi, bố mẹ | — | sửa từ C4 và cảnh biển | 2 |

**Tổng ước tính:** khoảng 37 ảnh cảnh, cộng nhân vật phụ:
- bố mẹ hai bên, mỗi bên 2 người, có trang phục thường và áo dài: khoảng 8 ảnh;
- thầy xem ngày, cán bộ, người bán vàng: khoảng 3 ảnh;
- đội bưng quả: đã tính ở C14.

Tất cả khoảng 50 ảnh, tức khoảng 12% gói. Chạy sau 01/12, theo thứ tự ưu tiên của bạn, mỗi cảnh vẽ thử một tấm trước.

**Đề xuất thứ tự ưu tiên:**
1. **Chương 6:** C14–C17, nghi lễ, phần đặc sắc nhất về văn hoá.
2. **Chương 2:** C6, cầu hôn, khoảnh khắc người chơi nhớ nhất.
3. **Chương 3:** C4, C7, C9, gặp hai họ.
4. Các cảnh còn lại.

## 5. Việc tiếp theo, chờ duyệt

1. Bạn duyệt mục 1 (vòng chơi) và mục 2 (dữ liệu, tên hư cấu, số tạm).
2. Mình dựng mẫu đồ hoạ 2D (mục 3) bằng mã. Việc này làm được ngay, không cần chờ 01/12.
3. Bạn chọn thứ tự cảnh (mục 4). Sau 01/12, mình gửi bảng duyệt từng tấm cho cảnh ưu tiên đầu tiên rồi mới vẽ.
