# Tham khảo: phần mềm thiết kế tiệc chuyên nghiệp

Chủ dự án gửi ngày 26/11/2026 một ảnh chụp phần mềm thiết kế sự kiện chuyên nghiệp: rạp khung truss 26 × 45 m, 500 khách ngồi bàn tròn. Game chỉ lấy **ý tưởng chức năng**. Không chép giao diện, tên, hình hay dữ liệu của phần mềm đó.

## 1. Phần mềm có gì

- **Cảnh 3D của cả hội trường:** sân khấu, màn LED, khung truss, đèn rọi, thảm đỏ, bàn check-in. Món nào cũng có nhãn tên.
- **Mặt bằng nhìn từ trên:** có số đo (rạp 26 × 45 m, sân khấu 16 × 5 m), ghim đánh số nối mặt bằng với cảnh, dòng "Bàn ghế tự xếp · 500 khách", nút phóng to, thu nhỏ, vừa khung.
- **Thanh chỉ số trên cùng:** số lưu ý ("7 lưu ý"), tổng điện, dự toán.
- **Chạy show:** dòng thời gian các tiết mục (ví dụ "Vũ đạo tương tác màn LED mở màn", mục Khai mạc), bấm chạy thử 30 giây, có 10 mẫu.
- **Các thẻ việc:** thư viện mẫu, cấu hình của tôi, sàn sân khấu và màn LED, khung truss, mockup 2D, bàn ghế, ánh sáng, âm thanh, bóc tách và kết cấu, AR, tiết mục, dự toán.
- **Công cụ:** đổi góc nhìn, dời thiết bị, đo kích thước, xuất bản vẽ.

## 2. Đưa vào game thế nào

Người chơi của game là cặp đôi, không phải kỹ thuật viên sự kiện. Vì vậy mỗi chức năng giữ phần giúp hai bạn **thấy và quyết**, bỏ phần kỹ thuật.

| Chức năng | Trong game | Trạng thái |
|---|---|---|
| Mặt bằng nhìn từ trên | Góc nhìn "Mặt bằng": vùng đặt bàn, lối giữa, cổng, cặp đôi. Bàn tự xếp hai bên lối cho đủ số khách, màu khăn và màu ghế theo lựa chọn, đánh số từng bàn. Thiếu chỗ thì báo. | Đã làm (26/11) |
| Số lưu ý | Mục "Lưu ý" và số đếm ở đầu bảng. Hiện có: thiếu bàn hay thiếu chỗ, chưa có cổng, tiệc tối cần đèn, nơi ngoài trời hay mưa thì nên tính rạp. Sau này nối với chỉ số Căng thẳng. | Đã làm (26/11) |
| Bóc tách, dự toán | Mục "Bảng kê": số bàn, ghế, khăn nền, khăn phủ (kèm cỡ tính từ bàn 3D), bộ đồ bàn theo số khách. Món có giá số tạm trong `gia-tham-khao.md` thì cộng thành khoảng tiền; món chưa có giá thì ghi "chưa có giá". | Đã làm (26/11) |
| Thư viện mẫu | "Mẫu có sẵn": 5 bộ, một lần bấm đặt cả cổng, hoa, bàn, khăn, ghế. Đây là hạt giống của 21 bộ phong cách (`bang-ve.md` mục 3.9). | Đã làm (26/11) |
| Cấu hình của tôi | Lưu vài phương án rồi đặt cạnh nhau để so (`bang-ve.md` mục 9). | Chưa làm |
| Chạy show 30 giây | "Xem thử buổi lễ": chạy nhanh dòng thời gian tiết mục trên chính cảnh đã trang trí. Ngày chuyển dần sang đêm, có cánh hoa, pháo giấy, đèn (hiệu ứng mã ở `bang-ve.md` mục 5), dải tiết mục chạy bên dưới. Cần màn chương trình (`spec.md` mục 4) có trước. | Chưa làm |
| Ánh sáng, âm thanh, màn LED | Ánh sáng (vẽ bằng mã): dây đèn bóng tròn, đom đóm quấn cổng, 4 đèn rọi 5 màu, nến trên bàn; ban đêm có đèn thì đồ trang trí sáng ấm lên. Màn LED (mã): hai màn hai bên hoặc một màn lớn sau cổng, chiếu tên hai bạn, lời chào chạy chữ, pháo hoa hoặc hoa rơi. Âm thanh (dựng 3D, `ve/loa_3d.py`): loa kéo, hai loa đứng, loa trên cột cắm vào sub. | Đã làm (26/11) |
| Điện | Không hiện thành thanh số. Bảng kê ghi điện ước lượng và nguồn tại chỗ (số tạm: Vườn Hồ 15 kW, Sân nhà quê 4 kW); vượt thì có lưu ý và thêm dòng máy phát. Lưu ý khác: tiệc tối thiếu đèn, chưa có loa, loa kéo không đủ cho 100 khách, đèn rọi ban ngày không rõ, màn lớn sau cổng che cảnh hồ. | Đã làm (26/11) |
| Kích thước, dời thiết bị | Kéo bàn trên mặt bằng, chọn trong 13 cách xếp (`bang-ve.md` mục 3.4). | Chưa làm |
| Cảnh 3D xoay tự do, AR, khung truss, kết cấu | Không làm: nặng máy, không giúp cặp đôi quyết. Game giữ tranh vẽ tay, thêm cận cảnh và mặt bằng. | Bỏ |

## 3. Số đo và giới hạn

- Vùng đặt bàn (Vườn Hồ 30 × 22 m, lối giữa 3 m; Sân nhà quê 24 × 16 m, lối giữa 2 m) là **ước lượng trên tranh, chưa đo**. Trang ghi rõ "ước lượng". Khi dựng bộ xếp bàn thật thì đo lại từng nơi theo thước phối cảnh.
- Cách xếp hiện chỉ có một kiểu cho mỗi loại bàn: bàn tròn theo lưới, bàn dài thành hàng, bàn chéo kiểu xương cá. Khoảng cách tính từ chỗ ghế và lối đi tối thiểu (số tạm của bản thử).
- Điện mỗi món là ước lượng của bản thử: màn LED 0,3 kW mỗi m², hai loa đứng 1 kW, loa và sub 2,6 kW, dây đèn 0,15 kW, đèn rọi 0,24 kW. Cần thay bằng thông số của nhà cung cấp.
- Giá trong bảng kê chỉ dùng số tạm đã có. Không thêm giá mới cho khăn, ghế, đồ bàn khi chưa có báo giá.

## 4. Cách xếp chỗ theo ảnh tham khảo thứ hai (26/11/2026)

Chủ dự án gửi thêm một loạt ảnh tiệc cưới ở Ý: góp ý là game đang bó vào vài cách xếp bàn ghế đơn giản. Những cách xếp thấy trong ảnh:

| Thấy trong ảnh | Trong game | Trạng thái |
|---|---|---|
| Ghế dự lễ hai khối thẳng hàng hai bên lối đi, nhìn ra cổng hoa và cảnh biển, cảnh hồ | "Phần: Lễ", xếp "Thẳng hàng" | Đã làm (26/11) |
| Hai khối ghế xoay chéo về phía cổng | "Khối chéo" (mỗi hàng nghiêng 20°) | Đã làm (26/11) |
| Hàng ghế cong ôm lấy chỗ làm lễ | "Hình quạt" (các cung tròn quanh cặp đôi, chừa lối giữa) | Đã làm (26/11) |
| Ghế xếp vòng tròn đồng tâm quanh bục tròn ở giữa quảng trường, có lối xuyên tâm | "Vòng tròn" (4 vòng, 4 lối) | Đã làm (26/11) |
| Một bàn dài xuyên suốt dưới vòm đá, bên hồ: nến, hoa rủ ở đầu bàn, dây đèn trên cao | Ba kiểu trong "Bàn tiệc": bàn dài giữa lối (đầu bàn ngay trước cặp đôi), hai dãy dọc lối (trên cỏ hai bên, lùi tới gần lan can), ba dãy. Dựng 3D bằng máy ảnh phối cảnh khớp tranh (`ve/ban_xuyen_3d.py`), nên bàn lùi xa đúng như ảnh; vẫn đổi được khăn nhiều lớp, đệm, khung ghế; nến chạy dọc bàn | Đã làm (26/11) |
| Lối đi có dải nước soi bóng, hai bên là luống hoa trắng | "Lối đi": lối gương nước (vẽ bằng mã: trời phản chiếu qua đường chân trời, cổng và cặp đôi phản chiếu qua đường chân của chính nó, có gợn nước và gờ đá), thảm trắng, thảm đỏ. Luống hoa hai bên là món vẽ, chờ duyệt | Đã làm (26/11) |
| Hoa trắng trên chân trụ cao, chậu đá kiểu Ý, ô che nắng, luống hoa dọc lối | Là món vẽ, phải qua bảng duyệt trước khi vẽ (`bang-ve.md` mục 3.6) | Chờ duyệt |

**Cách làm.** Một hàm xếp chỗ chung cho cả mặt bằng và cảnh, đơn vị mét quanh chỗ cặp đôi đứng. Cảnh chiếu từng ghế lên tranh theo phối cảnh đo lại ngày 26/11 trên bàn tròn vẽ tay: mặt bàn dẹt b/a ≈ 0,18, chân bàn ở 93% khung, nên máy quay cao khoảng 3,26 m, tiêu cự khoảng 1,1 lần bề ngang khung (góc nhìn khoảng 49°). Ở Vườn Hồ, đáy khung cách máy quay khoảng 11,5 m, cặp đôi khoảng 17,6 m, lan can khoảng 26 m; lưới 1 m vẽ theo cách này khớp hai mép lối đá (lối rộng khoảng 2 m). Ghế là ghế chiavari của bộ bàn, dựng 3D ở 16 hướng (`ve/ghe_xoay_3d.py`). Mỗi ghế chọn hướng gần nhất sau khi trừ góc nhìn lệch sang bên, vẽ từ xa tới gần, chia hai lớp trước và sau cặp đôi. Đổi màu đệm, màu khung một lần cho cả 16 hướng.

**Bàn dài và lối đi.** Bàn dài chạy vào sâu không ghép được từ hình trực giao, nên vẽ thẳng bằng máy ảnh phối cảnh cùng thông số trên, mỗi kiểu một tấm đầy khung; bản chơi chỉ dời ngang theo lối đi của từng nơi. Mặt bằng tính bàn dài theo vùng: hai dãy đủ 100 chỗ, một bàn giữa lối chỉ được khoảng 36 chỗ ở Vườn Hồ (có lưu ý thiếu chỗ), ba dãy khoảng 136 chỗ. Phần bàn thấy trong tranh ngắn hơn trên mặt bằng vì đoạn gần máy ảnh nằm dưới khung hình.

**Giới hạn.** Từ chỗ cặp đôi ra tới đáy khung chỉ khoảng 6 m, nên kiểu thẳng hàng thấy được 4–5 hàng gần cặp đôi; các hàng còn lại nằm dưới khung hình, mặt bằng vẫn vẽ đủ. Hình quạt và vòng tròn dùng phần cỏ hai bên và sau cặp đôi nên thấy nhiều ghế hơn.
