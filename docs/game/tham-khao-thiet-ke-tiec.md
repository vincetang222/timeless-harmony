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
