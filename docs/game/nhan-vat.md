# Nhân vật: ngoại hình và tùy chỉnh

Tài liệu thiết kế cho phần dựng nhân vật của game "Về chung một nhà". Bản thử đang ở dạng trang Artifact (Xưởng nhân vật), chưa nằm trong `game/`.

## 1. Cách dựng hình

**Vẽ tay bằng mô hình ảnh, ghép theo lớp.** Bản vẽ bằng mã (canvas, tham số liên tục) đã bị chủ dự án loại vì không đẹp bằng tranh nền. Cách hiện tại:

1. **Người gốc.** Mỗi vai (chú rể, cô dâu) có một bức vẽ toàn thân bằng `qwen-image-3.0-pro` (Alibaba Model Studio):
   - đứng thẳng, nhìn thẳng, trên nền xanh lá thuần để tách nền;
   - cùng nét vẽ tay màu nước với cảnh tiệc;
   - nắng vẽ từ trái, rồi lật ngang khi xuất để khớp nắng từ phải của cảnh.
2. **Biến thể bằng chế độ sửa ảnh.** Mỗi biến thể được sửa từ người gốc với câu lệnh "giữ nguyên mọi thứ khác". Nhờ vậy dáng đứng, khung hình và gương mặt gần như trùng khít giữa các ảnh.
3. **Hai lớp: đầu và thân.** Lựa chọn tăng theo cấp số nhân nếu mỗi tổ hợp là một ảnh. Vì vậy mỗi nhân vật được ghép từ hai lớp, cắt ở cổ:
   - **Lớp đầu:** vóc người × khuôn mặt × kiểu tóc = 3 × 3 × 3 = 27 ảnh mỗi vai. Vóc người nằm ở lớp đầu vì người đầy đặn thì mặt cũng đầy theo.
   - **Lớp thân:** trang phục × vóc người × dáng người = 2 × 3 × 6 = 36 ảnh mỗi vai.
   - **Vết cắt:** lớp thân được giữ đặc tới quá vết cắt, lớp đầu mờ dần qua cổ đè lên. Vì vậy chỗ nối không bị thủng.
   - **Tóc dài:** lớp đầu của cô dâu giữ thêm phần tóc rủ xuống vai, tách theo màu tóc.
   - **Lớp mắt và lông mày:** 3 dáng mặt × (4 dáng mắt + 3 kiểu lông mày), cắt riêng từng bên (mục 4).
   - **Áo dài:** cổ áo cao, nên có thêm một lớp cổ áo vẽ đè lên đầu để che cổ sơ mi của lớp đầu.
   - Mỗi vai có 2 × 3 × 6 × 3 × 3 × 4 × 3 = 3.888 tổ hợp hình dạng (chưa kể màu) từ 78 ảnh vẽ.
4. **Chiều cao (145–195 cm):** phóng hoặc thu cả hình. Trong cảnh, kích thước theo phối cảnh đo trên tranh nền: 1 m tại chân y (% khung) cao 0,307 × (y − 44) % chiều cao khung. Số này đo từ lan can đá (≈1 m), ghế tiệc (≈0,95 m) và bàn (≈0,75 m). Khoảng 145–195 cm là lựa chọn thiết kế, không phải số đo thống kê.
5. **Ánh sáng và bóng:**
   - Bóng ngả dựng lúc chạy từ chính hình vẽ: (x, độ cao u) → (x − 0,75u, chân + 0,2u), cùng hướng với bóng bàn ghế trong tranh. Sau đó làm mờ và nhạt dần ra xa.
   - Dưới chân có thêm bóng tiếp xúc.
   - Vì bóng dựng từ hình vẽ nên đổi theo chiều cao, vóc người và váy.

Game không gọi dịch vụ ngoài: mọi ảnh được vẽ sẵn lúc làm game, trình duyệt chỉ tải ảnh tĩnh.

## 2. Dáng người: vai, eo, bụng, hông

### Nguồn tham khảo

- **FFIT (Female Figure Identification Technique)** của Simmons, Istook và Devarajan, dùng trong nghiên cứu may mặc:
  - xếp dáng nữ từ sáu số đo vòng (ngực, eo, hông và lân cận), không dùng số đo vai;
  - có chín nhóm, gồm đồng hồ cát, hình thìa, chữ nhật, quả trám, bầu dục, tam giác, tam giác ngược.
- **Thang Connell** chỉ dùng bốn nhóm: đồng hồ cát, quả lê, chữ nhật, tam giác ngược.
- **Nghiên cứu ở Đại học Loughborough** đo 1.679 phụ nữ. Chỉ cần đặt thước dây lệch một chút, cùng một người đã bị xếp vào nhóm khác. Bản thảo liên quan nói các cách hiểu khác nhau về điểm đo của FFIT xếp cùng một cơ thể vào dáng khác nhau tới 40% trường hợp.
- **Nghiên cứu của Đại học Bang North Carolina** (khoảng năm 2005, hơn 6.000 phụ nữ, phục vụ may mặc), theo Wikipedia dẫn lại:
  - 46% dáng chữ nhật;
  - hơn 20% dáng thìa;
  - gần 14% tam giác ngược;
  - 8% đồng hồ cát.
- **Dáng nam:** các tài liệu chủ yếu là hướng dẫn chọn đồ, không phải chuẩn đo. Năm nhóm hay gặp:
  - chữ nhật: vai, eo, hông gần bằng nhau;
  - tam giác ngược: vai rộng, eo hẹp;
  - hình thang: vai rộng, thu dần về eo;
  - tam giác: hông rộng hơn vai;
  - bầu dục: vai hẹp, bụng đầy.
- **Nghiên cứu may mặc ở Mỹ** dùng dữ liệu quét 3D để chia dáng nam. Tài liệu này cho thấy hệ cỡ chuẩn chung bỏ sót nhiều dáng người thật.
- **Nghiên cứu về phụ nữ Việt Nam:** Đại học Kỹ thuật Liberec có công trình phân dáng phụ nữ Việt 18–50 tuổi từ dữ liệu quét 3D của 480 người ở ba miền. Mình chưa đọc được toàn văn nên chưa dùng số liệu nào từ đó.

### Kết luận cho game

- Nhóm dáng không có ranh giới cứng và các hệ phân loại không thống nhất tên gọi. Vì vậy game **không gắn nhãn hình học khô** (quả lê, quả táo…) lên người chơi. Mỗi lựa chọn được gọi bằng cái mắt thấy: vai, eo, bụng, hông.
- Lựa chọn là **từng dáng trọn gói** thay vì hai thanh kéo vai và bụng độc lập. Lý do:
  - các tài liệu đều mô tả dáng bằng quan hệ giữa vai, eo và hông, không tách rời từng phần;
  - mỗi dáng là một bức vẽ, nên năm dáng chọn kỹ đẹp hơn chín ô ghép máy móc.
- **Vóc người** (mảnh, vừa, đầy đặn) và **dáng người** là hai trục riêng. Ví dụ người mảnh vẫn có thể có bụng, người đầy đặn vẫn có thể vai rộng eo gọn.
- Không có dáng nào là chuẩn đẹp. Mặc định là dáng cân đối chỉ vì đó là ảnh gốc.
- Dáng có ảnh hưởng về sau, không chỉ là hình:
  - nhà may đo vest hoặc váy theo dáng;
  - vest và váy may sẵn hợp dáng này hơn dáng kia.

| Vai | Lựa chọn | Mô tả khi vẽ |
|---|---|---|
| Chú rể | Cân đối | vai, eo, hông gần bằng nhau (ảnh gốc) |
| Chú rể | Vai rộng, eo gọn | ngực vai rộng, thu về eo phẳng, hông gọn |
| Chú rể | Vai rộng, có bụng | vai và ngực chắc, bụng rõ ở eo |
| Chú rể | Vai xuôi, có bụng | vai hẹp xuôi, bụng tròn đẩy vạt áo |
| Chú rể | Vai hẹp, hông rộng | vai ngực hẹp, hông đùi rộng hơn vai |
| Chú rể | Vai rộng, hông rộng, có bụng | to chắc: vai ngực rộng, bụng tròn, hông đùi rộng |
| Cô dâu | Cân đối | vai, eo, hông gần bằng nhau (ảnh gốc) |
| Cô dâu | Eo thon | vai và hông bằng nhau, ngực đầy, eo thắt rõ |
| Cô dâu | Vai rộng | vai vuông rộng, eo hông hẹp |
| Cô dâu | Hông rộng | vai hẹp xuôi, hông rộng dưới váy |
| Cô dâu | Có bụng | vai tròn, eo không rõ, bụng mềm dưới thân váy |
| Cô dâu | Vai rộng, hông rộng, có bụng | vai vuông, bụng mềm, hông rộng |

Váy xòe che gần hết hông và đùi, nên dáng cô dâu chủ yếu đọc được ở vai, ngực và eo. Hông sẽ rõ khi có thêm áo dài và đầm ôm.

### Vai, eo-bụng, hông là ba thanh kéo riêng (cập nhật)

Chủ dự án góp ý: gộp vai, eo, bụng, hông vào một lựa chọn là không hợp lý. Giờ trang chia như sau:
- **Vai, Eo và bụng, Hông:** ba thanh kéo độc lập, từ −1 tới +1.
  - Máy nắn ngang lớp thân theo từng dải, mỗi dải mềm theo hình chuông quanh vai, eo, hông.
  - Dải mạnh nhất co giãn 22%.
  - Không tốn lượt vẽ.
- **Dáng mẫu vẽ tay:** vẫn giữ, nhưng chỉ là điểm xuất phát giống bộ cơ thể dựng sẵn của The Sims; thanh kéo chỉnh tiếp trên đó.

### Đầu không phóng theo chiều cao (cập nhật)

- Ngoài đời, cỡ đầu thay đổi ít hơn nhiều so với chiều cao.
- Giờ cỡ đầu tỉ lệ với chiều cao mũ 0,3. Phần dưới cổ co giãn bù vào cho đủ chiều cao; bề ngang thân theo chiều cao mũ 0,6.
- Kết quả: người 148 cm có đầu to hơn so với thân, người 190 cm có đầu nhỏ hơn so với thân, thay vì phóng to cả hình.

## 3. Khuôn mặt và tóc

| Mục | Lựa chọn |
|---|---|
| Dáng mặt | Trái xoan; Tròn; Vuông |
| Dáng mắt | Hạnh nhân; Một mí; To tròn; Mắt phượng |
| Lông mày | Mảnh, cong; Tự nhiên; Đậm, ngang |
| Màu da | 6 nấc từ trắng hồng tới nâu đậm, hoặc như ảnh vẽ |
| Màu mắt | Nâu đen; Nâu; Hổ phách; Xám |
| Màu tóc | Đen; Nâu đen; Hạt dẻ; Nâu sáng; Đỏ rượu; Xám khói |
| Trang phục | Chú rể: vest ngọc lục, áo dài gấm ngọc lục. Cô dâu: váy cưới, áo dài đỏ thêu phượng |
| Tóc chú rể | Rẽ ngôi; Vuốt ngược; Xoăn ngắn |
| Tóc cô dâu | Búi cao; Dài thẳng; Ngang cằm |

Chi tiết mặt chỉ đọc được ở ô chân dung. Trong cảnh tiệc, một người cao vài trăm điểm ảnh nên chỉ còn đọc được chiều cao, dáng, tóc và trang phục.

## 4. Học từ cách tạo nhân vật của The Sims

### The Sims 4 làm thế nào

Theo tin của EA và các hướng dẫn:
- **Hai tầng chỉnh.** Người chơi bắt đầu từ khuôn mặt và cơ thể dựng sẵn, rồi tinh chỉnh.
  - Kéo đẩy trực tiếp trên mặt và người: bấm vào một vùng rồi kéo, gần như điểm nào trên mặt và người cũng chỉnh được.
  - Độ béo và độ cơ bắp là thanh kéo chung, còn từng bộ phận chỉnh riêng.
  - Bộ cơ thể dựng sẵn không khóa thanh kéo, chọn xong vẫn chỉnh tiếp được.
- **Hình dạng tách khỏi màu sắc.** Màu da, màu tóc, màu mắt là bảng màu riêng, đổi màu không đổi hình.
- **Có giới hạn:** bản gốc không có thanh chiều cao; thanh kéo không dùng cho trẻ nhỏ.
- **Hệ quả kỹ thuật:** vì cơ thể thay đổi rất mạnh, đội làm game phải cho chuyển động biết hình dáng cơ thể, ví dụ chỉnh đường tay để không xuyên qua bụng.

### Áp dụng cho game vẽ tay 2D này

The Sims dùng mô hình 3D co giãn được, game này dùng tranh vẽ tay. Mình giữ tinh thần, đổi cách làm:

| The Sims 4 | Về chung một nhà |
|---|---|
| Mặt và cơ thể dựng sẵn để bắt đầu | Người gốc, nút Ngẫu nhiên, và (sắp có) vài bộ dựng sẵn |
| Thanh béo và cơ bắp | Vóc người (mảnh, vừa, đầy đặn) và dáng (vai, eo, bụng, hông) |
| Kéo đẩy từng bộ phận | Chọn từng bộ phận đã vẽ sẵn: dáng mặt, dáng mắt, lông mày, kiểu tóc. Mỗi bộ phận là một lớp ảnh riêng |
| Bảng màu da, tóc, mắt | Đổi màu ngay trong trình duyệt trên tranh vẽ, giữ nguyên bóng sáng |
| Chuyển động biết hình dáng | Bóng đổ dựng từ chính hình vẽ, nên tự khớp theo dáng, váy, chiều cao |

**Cách ghép lớp:**
- Thứ tự: thân (trang phục × vóc × dáng) → đầu (vóc × dáng mặt × tóc) → lông mày → hai mắt.
- Mắt và lông mày vẽ trên ba khuôn mặt gốc, cắt riêng từng bên, rồi dò vị trí khớp trên từng đầu.
- Cùng một dáng mắt dùng được cho mọi vóc người và kiểu tóc.
- Tóc ngang cằm có mái che lông mày, nên lông mày lấy theo đầu.

**Cách đổi màu:**
- **Da:** nhân theo tỉ lệ màu, giữ bóng và má hồng.
- **Tóc và lông mày:** ánh xạ theo độ sáng sang bảng màu mới. Vùng tóc tìm bằng cách loang từ đỉnh đầu, để không dính nét viền áo.
- **Tròng mắt:** ánh xạ trong vùng mắt.

## 5. Việc tiếp theo

- **Trang phục:** vest màu khác, đầm ôm, khăn vấn và khăn xếp đi cùng áo dài. Mỗi bộ cần vẽ lại lớp thân (3 vóc × 6 dáng). Áo dài cô dâu hiện vẫn đi với voan vì voan nằm trong lớp đầu.
- **Tư thế:** nắm tay, quay nghiêng, chào bàn. Mỗi tư thế là một bộ người gốc mới.
- **Màu da và màu tóc:** thử đổi bằng chế độ sửa ảnh trên lớp đầu, hoặc pha màu lúc chạy.
- **Nhân vật phụ** (bố mẹ, khách, nhà cung cấp): dùng cùng quy trình, ít lựa chọn hơn.

## Nguồn

- [Body shape (Wikipedia)](https://www.wikipedia.com/wiki/Body_shape)
- [Female body shape (Wikipedia)](https://wikipedia.com/wiki/Female_body)
- [Why you might not be the body shape you think – Loughborough University](https://www.lboro.ac.uk/media-centre/press-releases/2021/may/you-might-not-be-the-body-shape-you-think/)
- [Bản thảo Ergonomics về FFIT (Manchester Metropolitan University)](https://e-space.mmu.ac.uk/627583/5/Ergonomics%20Manuscript%20%28v9%29.pdf)
- [Luận văn NC State về dáng nam từ dữ liệu SizeUSA](https://repository.lib.ncsu.edu/server/api/core/bitstreams/fe578c1f-8c9b-428a-924c-ae5c4cd3d39a/content)
- [Whole body shapes and fit problems among overweight and obese men in the United States](https://emerald.com/insight/content/doi/10.1108/JFMM-02-2021-0039)
- [Analysis of Vietnamese women's body shape from anthropometric data – TU Liberec](https://dspace.tul.cz/handle/15240/175245)
