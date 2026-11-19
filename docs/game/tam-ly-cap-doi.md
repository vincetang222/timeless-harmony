# Ma trận tâm lý của cặp đôi sắp cưới

**Bản nháp 0.1. Chủ dự án đã đọc và đánh giá: chưa sát với các cặp đôi ngoài đời.** Bản này sẽ được viết lại từ chuyện thật của vài cặp đôi (họ cãi nhau vì chuyện gì, ai quyết, điều gì suýt làm hỏng đám cưới). Cho tới lúc đó, đừng coi các trục và các kiểu cặp đôi dưới đây là đã chốt; bản chơi thử phải đọc ma trận từ tệp dữ liệu, không viết cứng vào mã. Một thiếu sót đã rõ: chưa có mức **tin vào tâm linh** (xem tuổi, xem ngày) của hai người và của hai họ, xem [xem-ngay.md](xem-ngay.md).

Tài liệu này dùng cho hai việc:

- **Trong game:** mỗi nhân vật có tính cách ẩn, quyết định họ muốn gì, khó chịu vì điều gì, và cãi nhau theo kiểu nào.
- **Trên nền tảng thật:** Harmony AI hỏi vài câu, xếp cặp đôi vào ma trận, rồi gợi ý kế hoạch hợp với họ và chỉ ra chuyện nên bàn trước khi nó thành cãi nhau.

Đây là mô hình thiết kế, không phải công cụ chẩn đoán tâm lý. Cơ sở và giới hạn ở mục 8.

## 1. Chín trục

Mỗi người có một điểm từ −2 đến +2 trên từng trục. Không có cực nào "đúng".

| # | Trục | Cực trái (−2) | Cực phải (+2) | Quyết định chịu ảnh hưởng |
|---|---|---|---|---|
| 1 | Tiền | **Giữ**: sợ nợ, tính từng khoản | **Tiêu**: đáng thì chi, cả đời có một lần | ngân sách, vay, hạng gói |
| 2 | Quy mô | **Riêng tư**: ít khách, thân thiết | **Rình rang**: càng đông càng vui | số khách, địa điểm, số tiệc |
| 3 | Phong tục | **Giữ lễ**: đủ nghi thức, đúng ngày giờ | **Phá cách**: làm theo ý mình | nghi lễ, trang phục, chương trình |
| 4 | Gia đình | **Theo bố mẹ**: người lớn quyết | **Tự quyết**: đám cưới của hai đứa | ai quyết, ai trả, mời ai |
| 5 | Thể diện | **Cho mình**: thấy vui là được | **Cho người ta nhìn**: phải đẹp mặt | trang trí, ảnh, những thứ khách thấy |
| 6 | Kiểm soát | **Tự tay**: việc gì cũng muốn nắm | **Giao phó**: thuê người lo | người lên kế hoạch, gói sẵn hay may đo |
| 7 | Chuẩn mực | **Dễ tính**: sao cũng được | **Cầu toàn**: từng chi tiết phải đúng | số lần đổi ý, mức hài lòng |
| 8 | Nhịp | **Lo xa**: xong sớm mới yên | **Tuỳ hứng**: nước tới chân mới nhảy | đặt sớm, hạn chót, mốc đóng tiền |
| 9 | Khi căng thẳng | **Rút lui**: im lặng, lánh đi | **Nói ra**: phải giải quyết ngay | cách cãi nhau và cách làm lành |

Bố mẹ hai bên cũng có điểm ở bốn trục: Tiền, Quy mô, Phong tục, Thể diện.

## 2. Khi hai người lệch nhau

Lệch từ 2 điểm trở lên trên một trục là có chuyện để bàn.

| Trục | Lệch nhau thường thành chuyện gì | Dấu hiệu sớm | Cách gỡ | Kế hoạch nên theo hướng |
|---|---|---|---|---|
| Tiền | Cãi về từng khoản chi. Người giữ thấy bất an, người tiêu thấy bị bó. | Một người giấu hoá đơn; người kia hỏi giá mọi thứ | Chốt trần ngân sách chung; mỗi người một khoản tự quyết không cần hỏi | Gói sẵn giá chốt, ký quỹ theo mốc để thấy trước từng đợt tiền |
| Quy mô | Một người kiệt sức vì đông, người kia thấy "không ra đám cưới" | Danh sách khách cứ dài ra hoặc bị gạch liên tục | Hai phần: lễ thân mật và tiệc mở | Lễ gia tiên ít người, tiệc có góc yên tĩnh |
| Phong tục | Tranh cãi giữ nghi lễ nào | "Làm vậy người ta cười" đối lại "làm vậy để làm gì" | Giữ phần cốt lõi với hai họ, phá cách ở tiệc và tiệc sau cưới | Gia tiên đủ lễ, tiệc theo ý hai người |
| Gia đình | Một người nghe bố mẹ, người kia thấy mất quyền | Quyết định đổi sau mỗi lần về nhà | Chia rõ việc của hai họ và việc của hai đứa; ai là con thì người đó nói với bố mẹ mình | Ghi rõ ai quyết hạng mục nào ngay từ buổi dạm ngõ |
| Thể diện | Tiền dồn vào thứ khách thấy, hay thứ hai người cảm nhận | So với đám cưới của người quen | Chọn hai ba "điểm sáng" để đầu tư, còn lại giản dị | Một hạng mục may đo, phần khác dùng gói sẵn |
| Kiểm soát | Người tự tay ôm hết rồi trách người kia thờ ơ; người giao phó thấy bị soi | "Để em làm cho nhanh" | Chia hạng mục, mỗi người toàn quyền phần mình | Thuê điều phối ngày cưới để người tự tay được nghỉ |
| Chuẩn mực | Người cầu toàn đổi ý liên tục; "sao cũng được" bị hiểu là không quan tâm | Một hạng mục chọn mãi không xong | Mỗi hạng mục chỉ xét ba lựa chọn, có hạn chót | Người cầu toàn quyết thứ họ quý nhất; phần còn lại người kia chốt |
| Nhịp | Người lo xa sốt ruột; người tuỳ hứng thấy bị giục | Việc dồn về tháng cuối | Lịch chung có mốc, nhắc trước một tuần | Đặt sớm thứ dễ kín lịch (địa điểm, ảnh), thứ khác để sau |
| Khi căng thẳng | Người nói ra càng đuổi, người rút lui càng lánh | Cãi xong không ai nhắc lại, rồi nổ ra to hơn | Hẹn giờ nói chuyện; quá nóng thì nghỉ hai mươi phút rồi quay lại | Mỗi tuần một buổi bàn chuyện cưới, những buổi khác không nhắc |

## 3. Khi hai người giống nhau ở cùng một cực

Giống nhau không có nghĩa là an toàn: không còn ai phanh.

| Trục | Cùng cực trái | Cùng cực phải |
|---|---|---|
| Tiền | Cắt quá tay, sau này tiếc vì thiếu kỷ niệm | Vượt ngân sách, nợ sau cưới |
| Quy mô | Hai họ chạnh lòng vì không được mời | Tiệc lớn mà không nói được với nhau câu nào |
| Phong tục | Lễ nghi dày đặc, hai người mệt | Bỏ hết lễ, mất lòng người lớn |
| Gia đình | Đám cưới của bố mẹ, không phải của hai đứa | Hai họ đứng ngoài, thiếu người giúp |
| Thể diện | Giản dị quá mức, ảnh không có gì để nhớ | Đẹp cho khách xem, hai người không vui |
| Kiểm soát | Ôm hết việc, kiệt sức trước ngày cưới | Không ai kiểm, nhà cung cấp làm sao hay vậy |
| Chuẩn mực | Qua loa, ngày cưới lộ thiếu sót | Không bao giờ thấy đủ, đổi ý tới phút chót |
| Nhịp | Xong quá sớm rồi đổi ý, mất cọc | Trễ mọi mốc, giá tăng vì đặt gấp |
| Khi căng thẳng | Không ai nói ra, vấn đề nằm đó | Cãi to, nói lời khó rút lại |

## 4. Đường cảm xúc theo giai đoạn

Mỗi người có một thanh **Căng thẳng**. Nó lên xuống theo giai đoạn, không chỉ theo sự cố.

| Giai đoạn | Cảm xúc nổi bật | Điều dễ làm căng | Điều giúp dịu | Trục nóng nhất |
|---|---|---|---|---|
| Sau cầu hôn | Hứng khởi | Hứa quá tay, báo ngày quá sớm | Tận hưởng vài tuần rồi mới bàn | Nhịp, Thể diện |
| Ra mắt, bàn chuyện hai họ | Lo bị đánh giá | Nhượng hết cho yên chuyện | Hai người thống nhất trước khi gặp người lớn | Gia đình, Phong tục |
| Danh sách khách và ngân sách | Choáng vì con số | Lần đầu cãi nhau về tiền | Nhìn tổng trước, chia khoản sau | Tiền, Quy mô |
| Chọn nhà cung cấp | Quá tải lựa chọn, mệt vì phải quyết | So với đám cưới người khác trên mạng | Mỗi hạng mục ba lựa chọn; gói sẵn | Chuẩn mực, Kiểm soát |
| Gom tiền, một hai tháng trước cưới | Áp lực tiền và việc | Ít gặp nhau; một người lo, một người vô tư | Hẹn hò không bàn chuyện cưới; chia việc | Tiền, Nhịp |
| Hai tuần cuối | Lo âu sát ngày, mất ngủ, cáu vì chuyện nhỏ | Thêm việc mới, đổi ý phút chót | Được trấn an; nghỉ ngơi, thư giãn | Khi căng thẳng, Chuẩn mực |
| Ngày cưới | Vỡ oà, kiệt sức | Sự cố nhỏ không ai lo hộ | Có người điều phối; ăn và uống nước đủ | Kiểm soát |
| Sau cưới | Nhẹ nhõm xen hụt hẫng | Nợ, bắt đầu sống chung | Trăng mật; cùng xem lại ảnh, tính sổ một lần cho xong | Tiền |

## 5. Áp lực từ bên ngoài

| Nguồn | Đẩy về phía | Game thể hiện bằng |
|---|---|---|
| Bố mẹ | Giữ lễ, Rình rang, Cho người ta nhìn; tiền hỗ trợ đi kèm tiếng nói | lời đề nghị trong buổi họp hai họ |
| Họ hàng | danh sách khách dài thêm, lời ra tiếng vào | tin nhắn, điện thoại |
| Bạn bè | so sánh, rủ tiệc độc thân | lời mời, bình luận |
| Mạng xã hội | chuẩn đẹp, Cho người ta nhìn | bảng tin trong điện thoại của nhân vật |
| Công việc | hết buổi, mệt | sếp giao việc gấp |
| Tuổi tác, bị giục cưới | cưới nhanh, bỏ qua bước | câu hỏi mỗi lần về quê |

## 6. Mười kiểu cặp đôi

Gom các tổ hợp hay gặp thành mười kiểu, để viết nội dung và để gợi ý kế hoạch.

| Kiểu | Trục nổi bật | Muốn gì | Dễ vấp ở đâu | Kế hoạch hợp |
|---|---|---|---|---|
| Hai đứa tối giản | Giữ, Riêng tư, Tự quyết | tiệc nhỏ, đúng ý | bố mẹ muốn đông | tiệc nhỏ cộng bữa cơm họ hàng ở quê |
| Cả nhà cùng vui | Theo bố mẹ, Rình rang, Giữ lễ | đủ lễ, đủ khách | vượt chi, kiệt sức | gói trọn của nhà hàng, có người điều phối |
| Người lo, người thả | lệch Kiểm soát và Nhịp | một người muốn chắc, một người muốn thoải mái | trách nhau | chia hạng mục, lịch chung |
| Cầu toàn đôi | cùng Cầu toàn, Tự tay | mọi thứ hoàn hảo | kiệt sức, đổi ý | may đo, nhưng giới hạn số lần sửa |
| Mộng mơ ví mỏng | Tiêu, Cho người ta nhìn, ít tiền | đám cưới như mơ | nợ | hai điểm sáng, còn lại gói cơ bản |
| Thực tế lo xa | Giữ, Lo xa | không nợ, xong sớm | cắt quá tay | giữ ảnh và phim cho tốt |
| Phá cách | Phá cách, Tự quyết | cưới điểm đến, không theo lệ | hai họ không thuận | giữ lễ gia tiên riêng với hai nhà |
| Hai miền một nhà | khác quê, lệch Phong tục | đẹp lòng cả hai nhà | nghi lễ chồng chéo | hai lễ nhỏ theo từng nhà, một tiệc chung |
| Cưới gấp | thời gian ngắn, Tuỳ hứng | kịp ngày | kín lịch, giá gấp | gói sẵn, cưới ngày thường |
| Bận rộn giao phó | cùng Giao phó, nhiều tiền ít thời gian | không phải lo | đám cưới không giống mình | người lên kế hoạch trọn gói, ba buổi duyệt |

## 7. Game dùng ma trận này thế nào

- **Điểm ẩn.** Người chơi trả lời vài tình huống đầu game để có chín điểm của mình. Điểm của người yêu bị ẩn và lộ dần qua hẹn hò, trò chuyện. Hiểu người ấy càng nhiều thì càng thấy trước phản ứng của họ.
- **Mỗi quyết định có thẻ trục.** Chọn tiệc 300 khách là +Rình rang. Tình cảm tăng hay giảm tuỳ quyết định đó khớp với người ấy tới đâu, và người chơi có hỏi ý trước hay không.
- **Cầu hôn.** Người Riêng tư không thích bị cầu hôn giữa đám đông; người Cho người ta nhìn thì thích. Chọn sai kiểu là lý do lời cầu hôn bị hoãn.
- **Căng thẳng.** Vượt ngưỡng thì nổ ra cãi nhau, diễn biến theo trục 9 của từng người. Dịch vụ thư giãn, buổi hẹn không bàn chuyện cưới, và việc chia việc làm thanh này hạ xuống.
- **Gói may đo.** Khớp với trục của cả hai thì điểm hài lòng cao hơn gói sẵn cùng giá. Người Dễ tính hoặc Tuỳ hứng lại thấy mệt nếu phải chọn quá nhiều thứ.
- **Hai họ.** Mỗi buổi họp hai họ là một cuộc thương lượng giữa điểm của bố mẹ và điểm của cặp đôi.

## 8. Nền tảng thật, cơ sở và giới hạn

**Harmony AI.** Hỏi mỗi người chín câu ngắn, mỗi trục một câu, rồi trả về: kiểu cặp đôi, quy mô và ngân sách gợi ý, thứ tự việc nên làm, và ba chuyện nên bàn sớm. Câu trả lời là thông tin riêng tư: phải hỏi ý trước khi lưu.

**Cơ sở.** Các trục dựa trên những khung đã được nghiên cứu rộng rãi: phong cách gắn bó trong tình yêu; kiểu xung đột một người đòi nói, một người rút lui; bốn dấu hiệu báo trước đổ vỡ của John Gottman (chỉ trích, khinh thường, phòng thủ, im lặng); các "kịch bản tiền bạc" của Brad Klontz; hiện tượng mệt mỏi vì phải quyết định nhiều. Trục Thể diện và Gia đình thêm vào vì chúng chi phối đám cưới ở Việt Nam.

**Giới hạn.** Cách ghép thành chín trục và mười kiểu là của mình, chưa kiểm chứng trên cặp đôi Việt Nam. Trước khi đưa lên Harmony AI, nên phỏng vấn mười tới mười lăm cặp vừa cưới để chỉnh lại.
