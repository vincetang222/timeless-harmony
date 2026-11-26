# Bố cục và độ đẹp của cảnh trang trí (kế hoạch, 26/11/2026)

Chủ dự án góp ý ngày 26/11: đồ trang trí chèn vào khung hình **không đẹp và bất hợp lý**, cần kế hoạch làm cho đẹp. Tài liệu này gồm: soát lỗi trên bản 31, luật bố cục, các bước làm theo thứ tự hiệu quả trên công sức, và cách kiểm.

Ảnh soát: `ve/mau/soat-truoc.webp` (9 lỗi đánh số). Trước và sau khi làm thử: `ve/mau/truoc-sau.webp`.

## 1. Soát lỗi trên bản 31

| # | Lỗi | Gốc của lỗi |
|---|---|---|
| 1 | Bàn ghế dựng 3D khác nét tranh (viền xám mảnh, màu phẳng, ban đêm vẫn sáng), không có bóng đổ xuống cỏ: trông như dán lên | hình 3D đặt thẳng lên tranh, không nhuộm theo ánh sáng của cảnh |
| 2 | Quanh mỗi bàn có một hộp tối hình chữ nhật | bóng nền của hình 3D bị cắt thẳng ở mép hình (mép phải còn độ đục tới 140/255) |
| 3 | Bàn bị mép khung cắt đôi; xếp kín như giấy dán tường, không chừa khoảng thở | xếp bàn chỉ theo sức chứa, cảnh vẽ mọi bàn kể cả bàn bị cắt |
| 4 | Loa đứng sát hai bên cặp đôi, che chỗ đẹp nhất | đặt loa theo cổng (cách 2,4 m), không theo bố cục |
| 5 | Dây đèn treo giữa trời, không có chỗ bám; hàng thứ hai vắt ngang hồ, núi | toạ độ dây đèn đặt tay theo khung, không gắn vào cây, cột, mái |
| 6 | Màn LED như hai tấm biển lớn che hồ | màn LED đặt cạnh cổng ở mọi nơi, kể cả nơi có cảnh đẹp phía sau |
| 7 | Phần Tiệc mà cặp đôi vẫn đứng ở cổng như lúc làm lễ | chưa có bàn cô dâu chú rể |
| 8 | Ghế dự lễ xếp dày thành khối, đè nặng nửa dưới khung | xếp đủ 100 ghế trong khung, màu khung ghế đậm |
| 9 | Sân nhà quê: bàn chắn lối vào cổng làng | vùng đặt bàn chưa có vùng cấm (lối, cổng, nhà) |
| 10 | Bàn tròn: ghế quay lưng vào bàn (chủ dự án phát hiện 26/11) | `ban_tron_3d.py` xoay ghế φ + π/2 thay vì φ − π/2; bàn dài đúng nên không lộ khi soát |
| 11 | Ghế phía sau của bàn xa đè lên lan can (chủ dự án phát hiện 26/11) | bàn ghế 3D vẽ chếch 15°, trong khi tranh nhìn bàn ở 12–24 m chỉ chếch 8–15° (bàn tròn vẽ tay đo được b/a ≈ 0,18 ≈ 10,4°, `tham-khao-thiet-ke-tiec.md` mục 4): bàn trông sâu hơn thật, chân ghế sau lên đúng đường chân lan can; lối dọc lan can chỉ chừa 1,2 m; hai hàng bách nằm trong vùng đặt bàn nên bàn đứng lẫn vào gốc cây |

## 2. Luật bố cục

1. **Cảnh ngang tầm mắt là một khung hình dàn dựng**, như tấm ảnh đẹp nhất của buổi tiệc; mặt bằng mới là nơi đếm đủ bàn. Tiệc rất đông xem đủ ở cảnh nhìn từ cao (Vườn Hồ nới rộng, T16). *Cần chủ dự án duyệt (mục 5).*
2. **Trục nhìn luôn thông:** máy quay → lối đi → cặp đôi → cổng → cảnh xa. Vùng làm lễ quanh cổng để trống (3,5 m mỗi bên); phía sau cặp đôi để trống 4,5 m mỗi bên lối làm phông (cổng, hồ); chừa 1,2 m đi lại dọc lan can, tường.
3. **Không để mép trái, phải cắt món** (cho phép tối đa 12% bề ngang món); chỉ mép dưới được cắt, làm tiền cảnh.
4. **Món treo phải có chỗ bám thật trong tranh:** dây đèn buộc vào thân cây, cột, mái, hoặc cột tre, cột gỗ vẽ bằng mã; không vắt qua hồ, núi, trời trống.
5. **Màn LED:** nơi ngoài trời có cảnh đẹp phía sau thì không đặt màn lớn sau cổng (chỉ hiện lưu ý); hai màn nhỏ đặt lệch hẳn ra hai bên, thấp, sát hàng cây. Màn LED chủ yếu dành cho nơi trong nhà (sảnh tiệc).
6. **Loa** ở góc sau, sát hàng cây hoặc tường, quay về phía khách; không đứng cạnh cặp đôi.
7. **Phần Tiệc:** cặp đôi ngồi bàn riêng trước cổng; phần Lễ mới đứng dưới cổng.
8. **Hoà nét bàn ghế 3D vào tranh:** bỏ hộp bóng bị cắt; bóng mềm dưới bàn, lệch theo nắng của tranh; nhuộm theo màu nắng từng nơi, bớt tương phản; bàn càng xa càng mù về màu không khí của cảnh; ban đêm tối theo cảnh, chỉ sáng quanh nguồn đèn.
9. **Ghế dự lễ** màu nhạt hơn, hàng xa thưa hơn, lối giữa rộng.
10. **Mỗi nơi đo một lần:** bãi đặt được, vùng cấm (lối, tường, cổng, nhà, gốc cây), trục nhìn, chỗ bám dây đèn, chỗ đặt loa, hướng nắng, màu nắng, màu mù xa. Đây là phần việc bắt buộc khi thêm nơi mới (`bang-ve.md` mục 4).

## 3. Các bước

| Bước | Việc | Cách làm | Tốn lượt | Trạng thái |
|---|---|---|---|---|
| A | Luật 2, 3, 6, 8: trục nhìn, mép khung, loa, hoà nét | mã | 0 | **Làm thử 26/11** (xem mục 4) |
| B | Luật 4, 5: dây đèn có chỗ bám (cây, cột tre), màn LED theo luật | mã; đo chỗ bám trên từng tranh | 0 | chưa làm |
| C | Luật 7: bàn cô dâu chú rể trước cổng ở phần Tiệc | dựng 3D bằng tệp có sẵn | 0 | chưa làm |
| D | Luật 9: ghế dự lễ nhạt, thưa, lối rộng | mã | 0 | chưa làm |
| E | Vùng cấm từng nơi (luật 10): Sân nhà quê có lối vào cổng, sân trước nhà | đo trên tranh | 0 | chưa làm |
| F | Kiểm tự động (mục 6) | mã thử | 0 | chưa làm |
| G | Nếu hoà nét bằng mã vẫn chưa đủ giống tranh: vẽ lại bàn ghế theo nét tranh bằng Canva | qua bảng duyệt, vẽ thử một tấm trước | có | chỉ làm khi chủ dự án thấy cần |

## 4. Đã làm thử (26/11)

Áp cho mọi mẫu ở cả hai nơi, xem kỹ ở Vườn Hồ, mẫu "Vườn trắng xanh":

- Hộp tối hết: bóng nền của hình 3D mờ dần về mép hình.
- Bóng mềm hình bầu dục dưới mỗi bàn, lệch phải theo nắng.
- Nhuộm theo nắng từng nơi (Vườn Hồ ấm nhẹ, Sân nhà quê vàng chiều), bớt 10% tương phản; bàn xa mù dần (3 mức) về màu không khí của cảnh.
- Xếp bàn: chừa 1,2 m dọc lan can; phía sau cặp đôi để trống 4,5 m mỗi bên lối. Sức chứa trên mặt bằng giảm theo (luật này có thật ngoài đời: lối đi và phông chụp ảnh).
- Cảnh không vẽ bàn bị mép trái, phải cắt quá 12% (mặt bằng vẫn có).
- Loa dời ra góc sau, sát hàng bách (Vườn Hồ) hoặc sát nhà và tường (Sân nhà quê).

Kết quả: khung hình thoáng, cổng và hồ không bị che, không còn hộp tối và bàn cụt. Còn lại: dây đèn, màn LED, cặp đôi ở phần Tiệc, ghế dự lễ (bước B–D); bàn ghế vẫn là nét 3D.

## 5. Cần chủ dự án quyết

1. Hướng làm đẹp trong ảnh trước và sau có đúng ý không.
2. Cảnh ngang tầm mắt chỉ vẽ những bàn nằm đẹp trong khung (đếm đủ trên mặt bằng; xem đủ ở cảnh nhìn từ cao T16). Điều này khác với yêu cầu trước đó "thấy toàn cảnh 100 bàn" ở cảnh ngang tầm mắt.

## 6. Kiểm tự động (bước F)

Mỗi món đặt vào cảnh có một khung chữ nhật trên màn hình. Bài thử chạy ở 1280 và 390 điểm ảnh, báo lỗi khi: khung chồng lên trục nhìn hoặc vùng cấm của nơi đó; khung bị mép trái, phải cắt quá 12%; món treo không có chỗ bám; loa hoặc màn LED đứng trong vùng làm lễ.
