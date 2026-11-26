# Bố cục và độ đẹp của cảnh trang trí (kế hoạch, 26/11/2026)

Chủ dự án góp ý ngày 26/11: đồ trang trí chèn vào khung hình **không đẹp và bất hợp lý**, cần kế hoạch làm cho đẹp. Tài liệu này gồm: soát lỗi trên bản 31, luật bố cục, các bước làm theo thứ tự hiệu quả trên công sức, và cách kiểm.

Ảnh soát: `ve/mau/soat-truoc.webp` (9 lỗi đánh số). Trước và sau khi làm thử: `ve/mau/truoc-sau.webp`. Bản 32 và bản 33 (bước B–F): `ve/mau/truoc-sau-2.webp`; cận cảnh bàn tròn trước và sau khi sửa lỗi 10, 11: `ve/mau/ban-tron-sua.webp`.

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
| A | Luật 2, 3, 6, 8: trục nhìn, mép khung, loa, hoà nét | mã | 0 | **Đã làm 26/11** (mục 4) |
| B | Luật 4, 5: dây đèn có chỗ bám (cây, cột tre), màn LED theo luật | mã; đo chỗ bám trên từng tranh | 0 | **Đã làm 26/11** (mục 4b) |
| C | Luật 7: bàn cô dâu chú rể trước cổng ở phần Tiệc | dựng 3D (`ve/ban_doi_3d.py`) | 0 | **Đã làm 26/11** |
| D | Luật 9: ghế dự lễ nhạt, thưa, lối rộng | mã | 0 | **Đã làm 26/11** |
| E | Vùng cấm từng nơi (luật 10): gốc bách (Vườn Hồ), lối vào cổng làng (Sân nhà quê), lối dọc lan can, tường | đo trên tranh bằng lưới 1 m | 0 | **Đã làm 26/11** |
| F | Kiểm tự động (mục 6) | mã thử | 0 | **Đã làm 26/11**: 248 cảnh, không lỗi |
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

## 4b. Đã làm tiếp (26/11, sau khi chủ dự án duyệt hướng)

- **Lỗi 10, 11 (bàn tròn):** sửa góc xoay ghế; bàn tròn, bàn dài, ghế 16 hướng dựng lại ở máy ảnh chếch 10° (`ve/README.md`, dòng "Góc máy ảnh"). Lối dọc lan can 2,5 m (Sân nhà quê: 1,5 m dọc tường).
- **Xếp bàn:** hai lưới hàng, phía sau và phía trước cặp đôi. Phía sau cặp đôi để trống phông (Vườn Hồ: cả bãi cỏ giữa hai hàng bách, nửa bề ngang 8,6 m; nơi khác 4,5 m). Sân nhà quê lối giữa hẹp nên chừa thêm 3 m trước mặt cặp đôi cho bàn sát lối. Năm mẫu có sẵn vẫn đủ chỗ cho 100 khách.
- **Vùng cấm (đo trên tranh bằng lưới 1 m chiếu theo phối cảnh):** gốc năm cây bách ở x ≈ ±7,5 m (Vườn Hồ); lối vào cổng làng ở góc sau bên phải (Sân nhà quê); cột đèn. Bàn và ghế dự lễ đều tránh.
- **Dây đèn (bước B):** mỗi nơi 3 dây, buộc vào chỗ bám thật: Vườn Hồ hai tán bách và hai cột gỗ trong chậu trắng có dây thường xuân; Sân nhà quê cành đa (cao khoảng 6 m), cột cổng làng và hai cột tre. Dây treo theo phối cảnh 3D, cao 4–4,8 m ở gần máy quay nên nằm trên trời, không vắt qua hồ. Cột vẽ bằng mã, xếp chung với bàn ghế theo độ sâu. Bóng sát nhau trên hình thì quầng sáng nhạt bớt.
- **Màn LED:** Vườn Hồ không cho chọn màn lớn sau cổng (nút khoá); hai màn nhỏ đứng sát hàng bách, ngoài phần hồ, chân thấp 0,6 m. Sân nhà quê đặt trong lối dọc tường, ngoài lối vào cổng. Có màn thì loa đứng ngoài mép màn (Vườn Hồ: ra ngoài khung hình) để không che chữ. Cỡ màn giữ nguyên nên giá không đổi.
- **Bàn cô dâu chú rể (bước C):** bàn 1,6 × 0,7 m dựng 3D, đặt ngay trước cặp đôi ở phần Tiệc, che từ thắt lưng xuống (chưa có hình nhân vật ngồi); khăn đổi theo khăn nền, ba khóm hoa của luống hoa (T15) ở mép trước, nhuộm theo tông hoa. Bàn dài giữa lối thì cặp đôi ngồi đầu bàn, không có bàn riêng. Có trên mặt bằng và bảng kê.
- **Ghế dự lễ (bước D):** lối giữa 3 m, ghế cách nhau 0,6 m; bóng mềm dưới ghế, nhuộm theo nắng và mù dần như bàn. Sân ngắn thì mỗi hàng thêm ghế (5–8 mỗi bên) để không tràn ra ngoài: Sân nhà quê hết lưu ý "ghế ra ngoài vùng".
- **Kiểm tự động (bước F):** trang thử có `window.thBoCuc()` trả mọi món đã đặt (khung trên hình, chỗ trên mặt bằng); bài thử chạy cảnh mặc định (cả hai nơi, Lễ và Tiệc) và 5 mẫu × (thêm dây đèn, 50 và 200 khách, 6 kiểu bàn kể cả bàn dài vẽ tay, 4 cách xếp ghế dự lễ) ở 1280 và 390, sáng và tối: 280 cảnh, không lỗi. Đã thử làm hỏng từng luật trên bản sao để chắc bài thử bắt được lỗi. Bài thử đã bắt hai lỗi thật: loa trái ở Sân nhà quê đứng lên mép bàn sau; bàn dài xếp chéo ở Sân nhà quê có ghế sau chạm chân tường (bàn chéo sâu hơn chỗ được tính, đã sửa). Số đo nào không phải số hợp lệ cũng tính là lỗi. Chạy: `node ve/kiem_bo_cuc.js`.

## 5. Cần chủ dự án quyết

1. ~~Hướng làm đẹp trong ảnh trước và sau có đúng ý không.~~ Chủ dự án duyệt 26/11 ("đúng hướng, làm tiếp các bước 2–6").
2. ~~Cảnh ngang tầm mắt chỉ vẽ những bàn nằm đẹp trong khung (đếm đủ trên mặt bằng; xem đủ ở cảnh nhìn từ cao T16).~~ Chủ dự án duyệt cùng câu 1 ngày 26/11; thay cho yêu cầu trước đó "thấy toàn cảnh 100 bàn" ở cảnh ngang tầm mắt.

**Thay đổi chủ dự án sẽ thấy dù không yêu cầu riêng (26/11):** nút "Màn lớn sau cổng" bị khoá ở Vườn Hồ, bản lưu cũ tự đổi sang hai màn (cả trong chương 4); ở Vườn Hồ, có màn LED thì loa đứng ngoài khung hình; mỗi mẫu đắt thêm 0,3–0,9 triệu (bàn cô dâu chú rể, dải hoa trước bàn, dây đèn thứ ba); sức chứa tối đa giảm: Vườn Hồ từ 24 xuống 22 bàn, Sân nhà quê từ 10 xuống 8 bàn 12 khách (lối dọc lan can, phông sau cặp đôi, lối vào cổng, cột đèn). Cân luật chương 4 (`can.js`): tổng chi tăng 0,3–1,1 triệu, kết cục không đổi.

## 6. Kiểm tự động (bước F)

Mỗi món đặt vào cảnh có một khung chữ nhật trên màn hình. Bài thử chạy ở 1280 và 390 điểm ảnh, báo lỗi khi: khung chồng lên trục nhìn hoặc vùng cấm của nơi đó; khung bị mép trái, phải cắt quá 12%; món treo không có chỗ bám; loa hoặc màn LED đứng trong vùng làm lễ.

Đã làm (26/11), thêm các điều kiện: chân ghế phía sau của bàn phải nằm dưới đường chân lan can, tường trên hình (bắt lỗi 11); bàn không lấn lối dọc lan can; dây đèn không vắt qua phông sau cặp đôi; màn LED không che phông ở nơi có cảnh đẹp; loa, màn LED không đè lên bàn trên mặt bằng; cột đèn không đứng trong trục nhìn; ghế dự lễ không đứng vào vùng cấm; trang không cuộn ngang trên điện thoại.
