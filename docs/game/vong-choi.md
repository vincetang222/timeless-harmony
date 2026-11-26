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

## 6. Chương 4 đã dựng thành ván chơi (25/11/2026)

Chủ dự án duyệt vòng chơi (mục 1) và chọn làm chương 4 trước. Bản chơi nằm ở `game/lab/xuong/`. Không dùng lượt Model Studio nào: toàn bộ dùng tranh đã có.

### 6.1 Bảy màn

Người chơi có 200 triệu và một đám cưới 100 khách. Mỗi màn theo nhịp ở mục 1.2.

| Màn | Người chơi làm gì | Điều rút ra |
|---|---|---|
| 1. Nơi tổ chức | Chọn 1 trong 6 nơi. Bố chú rể muốn về quê, mẹ cô dâu thích cảnh đẹp. | Không nơi nào vừa lòng cả hai họ |
| 2. Trang trí | Chọn gói Gọn, Đủ, Trọn; cảnh đổi theo. | Đẹp hơn thì tốn hơn và căng hơn |
| 3. Người phục vụ | Thuê hoặc không thuê MC, ban nhạc, ảnh và phim. | Mỗi người thêm một lợi ích khác nhau |
| 4. Mặc cả | Ba lượt đề nghị giảm giá; có thể dời sang ngày thường. | Đòi quá tay thì mất thiện chí |
| 5. Hợp đồng | Đọc hoặc không đọc chữ nhỏ; chọn ký quỹ hay trả thẳng; thuê hay không thuê nhà bạt. | Đọc hợp đồng, ký quỹ, phương án dự phòng |
| 6. Ngày cưới | Xử lý sự cố thời tiết; có thể có người phục vụ báo huỷ. | Quyết định trước đó mở hoặc đóng lối thoát |
| 7. Tổng kết | Nhận tiền mừng, xem bảng chi tiêu và kết cục. | Nhìn lại cả chuỗi quyết định |

### 6.2 Luật chơi (mọi số là số tạm)

Giá lấy trong cột "số tạm cho bản chơi thử" của `gia-tham-khao.md`. Điểm cộng trừ là do mình đặt để chơi thử, chưa cân bằng với người chơi thật.

- **Giá:**
  - sân vườn 140, nấu tại nhà ở quê 40 (cho 100 khách);
  - gói trang trí 4, 9, 15;
  - MC 3, ban nhạc 6, ảnh và phim 9;
  - nhà bạt dự phòng 8.
- **Lòng hai họ:** nơi ở quê cộng nhiều cho nhà trai, nơi có cảnh cộng nhiều cho nhà gái. Gói Gọn trừ cả hai, gói Trọn cộng cả hai. Dời sang ngày thường trừ cả hai.
- **Mặc cả:**
  - Nhà cung cấp có một mức giảm tối đa mà người chơi không thấy: 5–9% tuỳ giá trị đơn, thêm 6% nếu dời sang ngày thường.
  - Đề nghị trong mức đó thì được. Đề nghị quá thì bị trả giá thấp hơn, mất một phần thiện chí và tăng Căng thẳng.
  - Sau ba lượt là giá cuối.
- **Hợp đồng:**
  - Phần chữ nhỏ có điều khoản phí phục vụ 5%. Đọc thì thấy và xin bỏ được. Không đọc thì bị tính ở màn tổng kết.
  - Trả thẳng được giảm 3%. Ký quỹ giữ nguyên giá.
- **Sự cố:**
  - Thời tiết: xác suất 70%, loại theo nơi tổ chức (mưa, gió, nắng, sương). Có nhà bạt hoặc có đội trang trí trực (gói Đủ, Trọn) thì mở thêm cách xử lý tốt.
  - Người phục vụ báo huỷ: xác suất 15%, cộng 20% cho mỗi phần thiện chí đã mất. Ký quỹ thì được hoàn đủ; trả thẳng thì mất 30% tiền cọc.
- **Tiền mừng:** 0,4 triệu mỗi khách ở quê, 0,7 ở nơi khác, nhân hệ số theo lòng hai họ.
- **Sáu kết cục**, xét theo thứ tự:
  1. Trọn vẹn đôi đường.
  2. Rình rang mà rỗng ví.
  3. Ấm cúng vừa túi tiền.
  4. Sóng gió vẫn nắm tay.
  5. Đám cưới của hai đứa mình.
  6. Còn nhiều điều để học.
- **Kiểm:** đã duyệt 36.864 tổ hợp lựa chọn bằng máy; cả sáu kết cục đều tới được.
- **Sổ lưu niệm:** ghi những nơi đã thử và kết cục đã mở, để người chơi muốn chơi lại.

### 6.3 Giao diện theo "Vườn kính"

Chủ dự án nhận xét giao diện cũ chưa đẹp và muốn giống trang chủ. Bản mới dùng lại bảng màu, phông chữ và công thức kính của `theme.css`:

- **Nền:** cảnh đang chọn, đã làm mờ, phủ cả trang. Đó là ảnh tĩnh nên tấm kính lớn không cần `backdrop-filter` (cùng ý với "kính dựng sẵn" của trang chủ).
- **Ba cấp kính:** tấm (bảng màn chơi, chỉ số), thẻ (lựa chọn, lời thoại), giọt (thanh trên cùng, nút).
- **Sân khấu:** cửa sổ nét nhìn vào cảnh. Ở màn mở đầu và tổng kết trên máy tính, sân khấu cao gần hết cột.
- **Lời thoại:** người thân và nhà cung cấp dùng biểu tượng; cô dâu, chú rể dùng chính hình nhân vật của người chơi.
- **Kế hoạch của hai bạn:** trên máy tính, một bảng dưới sân khấu tóm tắt các quyết định đã chốt.

### 6.4 Bản gọn và danh mục dài (25/11/2026)

Chủ dự án nhận xét bản 6.3 chiếm nhiều diện tích và nhiều chữ, và hỏi về khả năng có khoảng 100 lựa chọn cho mỗi hạng mục. Bản gọn đổi cách trình bày, không đổi luật chơi:

- **Lưới thẻ:** mỗi lựa chọn là một ô hình nhỏ có giá và một dòng tên (3 cột trên điện thoại, 4 cột trên máy tính). Chạm là cảnh đổi ngay; lưới không dựng lại nên danh mục dài không giật.
- **Khay chi tiết:** chữ chỉ hiện cho lựa chọn đang chọn (tên, giá, nhãn ảnh hưởng), bám đáy bảng nên luôn thấy khi cuộn.
- **Lọc và xếp:** hạng mục có trên 8 lựa chọn tự hiện hàng lọc theo nhãn và nút xếp theo giá. Hình trong lưới tải dần khi cuộn tới.
- **Chỉ số:** một hàng mỏng bốn thanh; tiền chỉ nằm ở ví trên cùng. Bỏ các đoạn mở đầu và mô tả dài.
- **Thử 100 lựa chọn:** ở màn mở đầu có nút "Thử danh mục 100 nơi". Nút này nhân 6 nơi thành 100 nơi với hình lặp lại và tên "thử", chỉ để kiểm bố cục; không phải dữ liệu của game. Đã thử ở 1280 và 390, sáng và tối: 100 thẻ, lọc còn 32, không lỗi, không tràn ngang.
- **Dữ liệu:** mỗi nơi có thể có trường `canh` trỏ tới bộ tranh dùng chung, nên nhiều lựa chọn có thể dùng lại một bộ tranh.

### 6.5 Chưa làm

- Chưa có hình bố mẹ và nhà cung cấp (đang dùng biểu tượng). Cần vẽ sau 01/12.
- Mỗi hạng mục mới có một nhà cung cấp; mục 2.4 dự kiến 2–3.
- Chưa có âm thanh.
- Chưa thử trên điện thoại thật và chưa chơi thử với người ngoài.

## 7. Trang trí theo lớp và danh mục 100 lựa chọn (đề xuất, chờ duyệt)

**Hiện trạng.** Trang trí đang là 3 gói (Gọn, Đủ, Trọn), mỗi gói là một tấm tranh vẽ trọn cảnh cho từng nơi (6 nơi × 3 = 18 tấm). Cổng hoa, bàn ghế, đèn dính liền vào nền, nên người chơi chỉ chọn "ít hay nhiều", không chọn được kiểu. Thêm một lựa chọn nghĩa là vẽ thêm một tấm cho mỗi nơi.

**Vì sao không vẽ thẳng 100 tấm cho mỗi hạng mục.** Mỗi tấm tốn khoảng 0,24% hạn mức tháng. 8 hạng mục × 100 tấm là khoảng 800 tấm, gần gấp đôi hạn mức của một tháng, chưa tính tấm hỏng.

**Đề xuất: tách trang trí thành lớp, giống cách đã làm với nhân vật.**

1. Mỗi nơi có một tấm **nền trống** (không cổng, không bàn) và các **điểm neo** cố định: cổng, lối đi, bàn tiệc, hoa bàn, đèn, phông sân khấu.
2. Mỗi món trang trí là một **hình rời nền trong**, vẽ một lần theo cùng góc nhìn, dùng được ở mọi nơi. Mã chỉnh sáng theo từng cảnh như đang làm với nhân vật.
3. Số lựa chọn đến từ phép nhân **kiểu dáng × tông màu**: tông màu đổi bằng mã (như màu tóc, màu da). Ví dụ 10 kiểu cổng × 10 tông hoa cho 100 lựa chọn cổng từ 10 tấm vẽ.
4. Lựa chọn nằm trong **tệp dữ liệu** (tên, giá, nhãn phong cách, nhãn tông màu). Ảnh hưởng tới hai họ và ngân sách tính từ nhãn, không viết tay cho từng món. Thêm lựa chọn không cần sửa mã.
5. Món trang trí gom theo **bộ phong cách** (ví dụ: vườn pastel, truyền thống đỏ vàng, mộc, tối giản, nhiệt đới, đêm đèn). Người chơi phối tự do; phối hợp tông thì được cộng điểm.

**Giới hạn cần nói rõ.** 100 lựa chọn kiểu này là 10 kiểu dáng với 10 tông màu, không phải 100 thiết kế khác hẳn nhau. Giao diện nên là hai bước (chọn kiểu, rồi chọn tông) thay vì một lưới phẳng 100 ô. Lưới 100 ô hợp với nơi tổ chức và nhà cung cấp hơn.

**Ước lượng (số tạm, chưa thử).** 6 nền trống + 6 bộ phong cách × khoảng 5 loại món ≈ 36 tấm, khoảng 9% hạn mức tháng. Rủi ro chính: hình rời không khớp góc nhìn, không khớp ánh sáng, chân món không bám đất.

**Bước thử trước khi cam kết.** 3 tấm cho một nơi (nền trống Vườn Hồ, một cổng kiểu khác, một bộ bàn), theo đúng quy tắc: bảng duyệt trước, vẽ thử một tấm trước. Chưa vẽ gì khi chưa được duyệt.

### 7.1 Bảng duyệt bước thử 3 tấm (25/11/2026, chủ dự án đã duyệt)

Chủ dự án đã duyệt hướng trang trí theo lớp và duyệt bảng dưới đây. Kết quả ở mục 7.2.

| Tấm | Vẽ gì | Có gì | Không có gì | Sửa từ hình | Đạt khi |
|---|---|---|---|---|---|
| 1. Nền trống Vườn Hồ | Cảnh Vườn Hồ không còn đồ trang trí | Bãi cỏ, lối đá, lan can, hồ, núi, hàng bách, mây, ánh sáng như cũ | Cổng, hai bàn tròn, ghế, bóng của chúng | Vườn Hồ gói Gọn (`canh-gon`) | Không còn dấu vết đồ đã xoá; cỏ, lối đá, lan can liền mạch; phần còn lại không xê dịch so với hình gốc |
| 2. Cổng tròn khung vàng, hoa trắng | Một cổng cưới rời, nền một màu để tách | Vòng tròn kim loại màu vàng đồng trên đế thấp; một cụm hoa hồng trắng, lan trắng, lá bạch đàn, cỏ lau ở góc dưới trái và một cụm nhỏ ở góc trên phải | Chữ, người, mặt đất, cảnh nền | Vườn Hồ gói Đủ (`goc-du`): thay cổng hoa hồng đúng chỗ cũ để giữ góc nhìn, cỡ và nét vẽ | Tách nền sạch, không viền màu; đặt lên tấm 1 thì chân cổng nằm đúng lối đá và cỡ khớp với cặp đôi; mã đổi được hoa sang ít nhất 2 tông khác mà khung vàng không đổi màu |
| 3. Bộ bàn dài gỗ mộc | Một bộ bàn ghế rời, nền một màu để tách | Bàn dài gỗ sáng màu đặt dọc theo lối đi, khăn chạy bàn vải lanh màu kem, 8 ghế gỗ lưng chéo, bát đĩa, ly | Hoa bàn, nến (là lớp riêng về sau), người, mặt đất | Vườn Hồ gói Gọn (`canh-gon`): thay bàn tròn bên trái đúng chỗ cũ | Tách nền sạch; ghế đúng cỡ so với nhân vật; đặt lên tấm 1 trông như đứng trên cỏ (bóng chân do mã vẽ); lật gương bằng mã cho bên phải vẫn hợp |

- **Hoa vẽ màu trắng là có chủ ý:** trắng là màu gốc dễ nhuộm nhất, mã nhân màu là ra tông khác. Khăn bàn màu kem cũng vậy.
- **Nền tách dùng màu xanh dương thuần:** hoa lá có nhiều xanh lá nên không dùng nền xanh lá như nhân vật.
- **Việc mã làm, không tốn lượt:** tách nền, đặt vào điểm neo, bóng chân, lật gương, đổi tông hoa và tông khăn, chỉnh sáng theo cảnh.
- **Thứ tự:** vẽ tấm 1 trước và tự đo. Đạt thì vẽ tấm 2 và 3, soát xong mới gửi cả ba một lần. Không đạt thì sửa từng chỗ trên hình đã có.
- **Giới hạn:** tối đa 6 lượt cho cả bước thử (3 tấm và tối đa 3 lượt sửa), khoảng 1,4% hạn mức tháng. Hết 6 lượt mà chưa đạt thì dừng và báo.
- **Kết quả gửi xem:** một màn thử trong `game/lab/xuong/`: nền trống Vườn Hồ, cổng và bàn mới, đổi được tông hoa và tông khăn, có cặp đôi đứng trong cảnh; kèm số đo và những chỗ chưa đạt.
- **Chưa kiểm được trong 3 tấm này:** dùng lại món rời ở nơi có ánh sáng khác. Việc đó cần nền trống của một nơi thứ hai, là tấm thứ 4 nếu bước thử đạt.

### 7.3 Đồ tự vẽ trong màn thử (26/11/2026)

Cùng màn thử, thêm đồ tự vẽ không tốn lượt: 6 khung cổng bằng mã có cụm hoa Canva, ban ngày và ban đêm, 7 bộ bàn 3D với khăn nhiều lớp, đệm, khung ghế đổi màu, và nút "Xem gần" mở cận cảnh một chỗ ngồi kiểu Âu hoặc kiểu Việt. Chi tiết ở `bang-ve.md` mục 9. Phần tải thêm chỉ tải khi chọn món: khung và hoa 50–150 KB mỗi khung, mỗi bộ bàn 100–270 KB (thêm 190–460 KB ảnh toạ độ khăn nếu chọn hoạ tiết hoặc khăn phủ), cận cảnh khoảng 0,3 MB, có ảnh toạ độ thì khoảng 0,8 MB.

### 7.2 Kết quả bước thử (25/11/2026)

Dùng 3 lượt vẽ cho 3 tấm, không lượt sửa nào (khoảng 0,7% hạn mức tháng). Màn thử nằm trong `game/lab/xuong/`: màn mở đầu, nút "Thử trang trí theo lớp (Vườn Hồ)".

| Tấm | Kết quả | Số đo, ghi chú |
|---|---|---|
| 1. Nền trống | Đạt | Cổng, bàn ghế và bóng của chúng đã hết; cỏ, lối đá, lan can liền mạch. Cả cảnh lệch xuống khoảng 10 px trên ảnh cao 1520 px (0,7%); lối đá hẹp hơn 28 px ở mép dưới. Chỗ đứng của cặp đôi đã cân lại bằng mã. |
| 2. Cổng tròn | Đạt | Nền phẳng (độ lệch màu nền khoảng 1/255), tách sạch trên nền sáng và nền tối. Mô hình không giữ vị trí và cỡ cũ mà vẽ cổng to gần kín khung (rộng 1367 px): có lợi cho độ nét, vị trí và cỡ do mã đặt. Lá ngoài rìa bị nhuốm xanh dương của nền, đã gỡ bằng mã. |
| 3. Bàn dài | Đạt, có sai khác | 10 ghế thay vì 8. Bàn được vẽ chéo góc chứ không song song lối đi; dùng nguyên cho bên phải, lật gương cho bên trái. Vệt tối giữa chân ghế đã xoá bằng mã. |

**Mã làm được gì trên 3 tấm này.** Đặt cổng và bàn vào điểm neo theo cùng thước phối cảnh với nhân vật (vòng cổng 2,7 m; ghế gần nhất 1 m). Bóng chân. Lật gương bộ bàn. 6 tông hoa và 5 tông khăn, tức 30 cách phối từ một cổng và một bộ bàn. Thêm vào bản chơi khoảng 370 KB, chỉ tải khi mở màn thử.

**Giới hạn đã thấy.**

- Mặt nạ hoa làm tự động. Mặt nạ khăn bàn phải khoanh tay một lần cho mỗi kiểu bàn, vì gỗ sáng, đĩa và khăn có màu quá gần nhau.
- Tông đỏ đậm còn sót vài chấm kem ở nhuỵ hoa hồng.
- Bàn bên trái là bản lật gương nên hướng sáng trên bàn cũng bị lật.
- Phối cảnh trong hình bàn hơi mạnh hơn cảnh.
- Chưa kiểm việc dùng lại ở nơi có ánh sáng khác (cần nền trống của nơi thứ hai). Mới thử trên Chromium ở 1280 và 390, chưa thử điện thoại thật.

**Cách vẽ lô sau, nếu được duyệt.** Mỗi món một lượt, vẽ rời trên nền một màu, không cần sửa từ cảnh; vị trí và cỡ do mã đặt. Yêu cầu phần cần đổi tông có màu trắng và nằm trên vật có màu khác hẳn để mặt nạ làm tự động được.

### 7.3 Tấm 4: dùng lại món rời ở nơi khác (25/11/2026)

Chủ dự án duyệt phong cách của cổng và bàn rời, và duyệt tấm 4.

| Tấm | Vẽ gì | Có gì | Không có gì | Sửa từ hình | Kết quả |
|---|---|---|---|---|---|
| 4. Nền trống Sân nhà quê | Sân nhà quê không còn đồ trang trí | Sân gạch, lối đá, nhà ba gian, cây rơm, giếng, cây đa, cổng làng, tường, ruộng | Cổng cưới lá dừa, hai bàn tròn, ghế, bóng của chúng | Sân nhà quê gói Gọn (`langque-gon`) | Đạt trong 1 lượt. Cảnh lệch nhiều nhất 14 px trên ảnh rộng 2736 px (0,5%). Phần sau cổng cũ được vẽ bù (thêm một chái nhà và một cây). |

**Dùng lại món rời.** Cùng tệp cổng và tệp bàn của Vườn Hồ đặt lên Sân nhà quê, không vẽ thêm. Mỗi nơi chỉ khai báo: tấm nền, chỗ đứng của cặp đôi, điểm neo của cổng và hai bàn, và một hệ số chỉnh sáng. Cỡ vẫn theo thước phối cảnh chung nên không phải chỉnh tay.

**Chỉnh sáng theo cảnh.** Món rời để nguyên thì lạnh màu hơn nắng vàng của Sân nhà quê. Mã nhân màu món rời với (0,98; 0,905; 0,83), là tỉ lệ màu khăn trắng của Sân nhà quê so với Vườn Hồ đo trên tranh gốc. Nhân vật chưa được chỉnh sáng theo cảnh.

**Tổng bước thử.** 4 lượt vẽ, không lượt sửa (khoảng 1% hạn mức tháng): hai nền trống, một cổng, một bộ bàn. Mỗi nơi có 30 cách phối tông.

**Còn mở.** Lối đá ở Sân nhà quê lệch tâm (tâm ở 52,8% bề ngang) nên cổng và bàn đặt lệch theo; mỗi nền trống cần đo điểm neo một lần. Chưa thử nơi có nền cát hoặc ánh sáng tối. Các giới hạn ở mục 7.2 vẫn còn.

### 7.4 Kế hoạch vẽ tiếp

Danh mục trang trí, hiệu ứng sân khấu, tiết mục và hạn mức tháng 12 nằm ở [bang-ve.md](bang-ve.md) (chờ duyệt).

## 8. Đưa xưởng trang trí vào ván chơi (đề xuất 26/11/2026; chủ dự án duyệt vòng chơi và bảng giá ngày 26/11)

**Hiện trạng.** Mọi món làm từ 25/11 (khung cổng, hoa, bàn 3D, khăn nhiều lớp, đèn, màn LED, loa, ghế dự lễ, bàn dài, lối đi, toàn cảnh mọi bàn, mặt bằng, lưu ý, bảng kê) nằm ở màn "Xưởng trang trí tiệc" của trang thử. Lựa chọn ở đó **chưa** ảnh hưởng tới ngân sách, chỉ số hay ngày cưới của chương 4; màn "Gói trang trí" của chương 4 vẫn là 3 gói Gọn, Đủ, Trọn.

**Đề xuất vòng chơi trang trí (thay màn "Gói trang trí").**

1. **Số khách → nơi tổ chức.** Số khách lấy từ danh sách khách. Mỗi nơi có sức chứa thật (số bàn xếp được trên mặt bằng). Vượt thì phải đổi nơi, đổi kiểu bàn hoặc bớt khách; đây là một quyết định khó giữa hai họ.
2. **Bố cục.** Phần Lễ: cách xếp ghế dự lễ, lối đi. Phần Tiệc: kiểu bàn và cách xếp.
3. **Trang trí theo lớp.** Cổng, hoa, lối đi, khăn, ghế, hoa bàn, đèn, màn LED, loa. Mỗi món có giá (số tạm, cần bảng giá) trừ vào ngân sách, và có nhãn phong cách; nhãn hợp gu nhà trai, nhà gái hay hai bạn thì tăng chỉ số tương ứng.
4. **Gói sẵn và may đo** (đặc tả mục 5). "Mẫu có sẵn" là gói của nhà cung cấp trang trí, rẻ và nhanh; tự chọn từng lớp là gói may đo, đắt hơn nhưng hợp ý hơn.
5. **Lưu ý thành rủi ro ngày cưới.** Ngoài trời mà không có rạp thì mưa thành sự cố; thiếu điện thì mất điện giữa tiệc; loa yếu thì khách phía sau không nghe; thiếu chỗ thì khách phải đứng. Người chơi xử lý trước (thuê rạp, máy phát, loa) hoặc chấp nhận rủi ro.
6. **Xem trước.** Toàn cảnh, mặt bằng, cận cảnh một chỗ ngồi; sau này thêm chạy thử buổi lễ 30 giây theo chương trình.
7. **Ngày cưới.** Cảnh ngày cưới dùng đúng những món đã chọn.

**Chủ dự án quyết ngày 26/11.**

- Duyệt vòng chơi trên. 3 gói Gọn, Đủ, Trọn **giữ lại** làm đường "Gói sẵn" (mọi nơi đều có); thêm đường "Tự thiết kế" dùng xưởng.
- Duyệt bảng giá số tạm cho từng món: `gia-tham-khao.md` mục 6.
- Tiệc rất đông: **vẽ nới rộng từ Vườn Hồ cũ** (tấm thử T16, `bang-ve.md` mục 8b), không dùng sa bàn. Đồng thời thêm nơi mới vào kế hoạch, trong đó có nơi trong nhà (`bang-ve.md` mục 4).

**Các bước làm** (đánh dấu khi xong):

1. Bảng giá số tạm trong bảng kê của xưởng; giá gói sẵn giảm 20% khi trùng một mẫu có sẵn. *(26/11)*
2. Màn "Trang trí" của chương 4 có hai đường: "Gói sẵn" (3 gói như cũ) và "Tự thiết kế" (mở xưởng, mang về giá và ảnh hưởng tới hai họ). Tự thiết kế chỉ có ở nơi đã có nền trống (Vườn Hồ, Sân nhà quê); nơi khác ghi "sắp có". Giá tính bằng một hàm thuần từ lựa chọn trong xưởng, chỉ cộng món trang trí. *(26/11)*
3. Nhãn phong cách: món hợp gu nhà trai (đỏ, gấm, cổng tròn dày hoa), nhà gái (đèn, màn LED, kim sa, hoa bàn), hai bạn (tông trắng xanh, luống hoa, bàn dài gia đình) cộng vào chỉ số tương ứng; thiếu cổng, thiếu đèn khi tiệc tối thì trừ. *(26/11)*
4. Lưu ý thành rủi ro ngày cưới: thiếu điện thì mất điện giữa tiệc, loa yếu thì khách phía sau không nghe, thiếu chỗ thì khách phải đứng. Người chơi xử lý trước hoặc chấp nhận rủi ro. *(chưa làm)*
5. Cảnh ngày cưới vẽ đúng những món đã chọn trong xưởng (hiện ngày cưới vẫn dùng tranh của gói). *(chưa làm)*

**Đã làm ngày 26/11 (bước 1–3), số tạm của bản thử:**
- Trong xưởng, mỗi dòng bảng kê có giá theo `gia-tham-khao.md` mục 6; dòng "Bàn ghế, dụng cụ, người phục vụ" đã nằm trong giá nơi tổ chức nên ghi riêng, không cộng vào trang trí. Giá một con số = trung bình khoảng; trùng đúng một mẫu có sẵn (chưa thêm hoa bàn, lối đi, luống hoa) thì giảm 20%.
- Màn "Trang trí" có thẻ thứ tư "Tự thiết kế" cạnh 3 gói. Ở Vườn Hồ và Sân nhà quê: chọn thẻ rồi "Mở xưởng trang trí"; trong xưởng, nơi và số khách khoá theo ván chơi, chỉ hiện mẫu có sẵn của nơi đó; "Dùng thiết kế này" mang giá và ảnh hưởng về, mặc cả tính lại từ đầu. Ở 4 nơi còn lại thẻ ghi "sắp có".
- Ảnh hưởng (hàm `hqTT`): thiếu cổng như gói Gọn; cổng tròn dày hoa, tông đỏ, vải gấm hợp nhà trai; hoa bàn, kim sa, màn LED, có đèn khi tiệc tối hợp nhà gái; tông trắng xanh, luống hoa, bàn dài gia đình hợp hai bạn; thiếu loa, loa kéo cho hơn 50 khách, thiếu chỗ thì trừ; tự chọn thêm 3 Căng thẳng (mẫu có sẵn bớt 2).
- Sự cố gió ngày cưới: tự thiết kế từ 8 triệu trở lên coi như có đội trang trí trực (như gói Đủ, Trọn).
- Cân thử (Vườn Hồ, có MC và thợ ảnh): mẫu "Vườn trắng xanh" 10,4 triệu cho kết quả gần gói Đủ, thêm Tình cảm; "Đêm kim sa" 18 triệu gần gói Trọn nhưng nhà trai kém hơn vì thiếu màu đỏ. Không đổi ngưỡng kết cục.
6. Chạy thử buổi lễ 30 giây theo chương trình. *(chưa làm, cần màn chương trình)*
