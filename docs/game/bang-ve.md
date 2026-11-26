# Bảng vẽ tiếp theo: trang trí, hiệu ứng sân khấu, tiết mục

**Bản đề xuất chờ chủ dự án duyệt (25/11/2026).** Tài liệu này nối tiếp mục 7 của [vong-choi.md](vong-choi.md) (trang trí theo lớp đã thử đạt ở 2 nơi). Mọi giá là số tạm. Tên bộ phong cách, nơi tổ chức và người biểu diễn đều hư cấu.

## 0. Tóm tắt

- **Trang trí:** muốn có hàng nghìn mẫu thì không vẽ từng mẫu. Ta vẽ từng bộ phận (khung cổng, cụm hoa theo loài, bàn, hoa bàn…), rồi để mã ghép, đổi màu và chỉnh sáng. Nếu hai bài thử ở mục 8 đạt, chỉ riêng cổng đã có khoảng 13.000 cách phối từ 37 tấm vẽ. Nếu không đạt, còn khoảng 320.
- **Hiệu ứng sân khấu:** pháo hoa, pháo giấy, pháo lạnh, khói sàn, bong bóng, màn LED, chữ neon… gần như toàn bộ vẽ bằng mã, **không tốn lượt**. Cái cần vẽ là nền đêm và nền trong nhà để hiệu ứng có chỗ diễn.
- **Bàn khách:** bàn, ghế và cách xếp tách rời: bàn tròn, bàn dài (8–20 khách, ngang và chéo) và ghế chiavari đã tự dựng bằng 3D ngày 25/11; bàn vuông, bàn đứng và các kiểu ghế khác dự kiến dựng tiếp (màu gỗ, sơn, kim loại đổi bằng mã); 13 cách xếp bằng mã; từ 30 tới 1000 khách, có sơ đồ nhìn từ trên xuống (mục 3.4).
- **Khăn, ghế, đồ trên bàn:** tìm hiểu ngày 25/11 thấy rất nhiều mẫu: khăn có chất và hoạ tiết, áo ghế, nơ ghế, trang trí bằng giấy. Màu và mặt vải (hoạ tiết, chất vải) làm bằng mã, 0 tấm; đã thử 8 hoạ tiết khăn. Món gắn thêm (nơ, món gắn ghế) và dáng mới (áo ghế, váy quây) thì vẽ, khoảng 9 tấm (cuối mục 3.4).
- **Khăn nhiều lớp, ghế theo lớp:** khăn nền + khăn phủ + khăn chạy bàn ghép bằng mã, 0 tấm; đã thử 7 cách phối trên bàn tròn cũ. Ghế có 7 lớp; khung, đệm, đai làm bằng mã, còn nơ và món gắn phải vẽ. Đã duyệt đổi T9 thành bàn dài phủ khăn trắng chấm đất (cuối mục 3.4).
- **Tiết mục:** 32 tiết mục trong 4 nhóm, mỗi tiết mục là một hình người biểu diễn rời, khoảng 34 tấm. Điệu nhảy của chính cặp đôi là việc khác, cần tư thế mới cho nhân vật (mục 6.6).
- **Màn cận cảnh bàn:** một góc nhìn gần một chỗ ngồi để cặp đôi xem đĩa, ly, dao nĩa hoặc đũa, khăn ăn và so sánh hai phương án; nền, đĩa, ly, dao nĩa, bộ Việt đã tự dựng bằng 3D, còn khăn ăn gấp phải vẽ (khoảng 2 tấm, cuối mục 3.4).
- **Hạn mức:** chủ dự án giới hạn game ở 40% gói Model Studio mỗi tháng, khoảng 166 hình (25/11). Toàn bộ kế hoạch khoảng 355 hình nên chia ra ba tháng 12, 1, 2; tháng 12 làm trang trí và tiết mục là vừa (mục 7). `gen.py` tự chặn lô vượt trần. Mục 7b liệt kê các cách tiết kiệm gói; riêng đổi màu bằng mã đã bớt được 14 tấm.
- **Bước đầu:** tháng 11 không chạy đợt nào (chủ dự án quyết 25/11). Đầu tháng 12 chạy các tấm thử còn cần công cụ vẽ: T2, T3, T4, T5 (mục 8) và T10, T11 (mục 8b); T1, T6, T7, T8, T9, T12, T13 đã tự vẽ.

## 1. Làm sao có hàng nghìn lựa chọn mà không vẽ hàng nghìn tấm

### 1.1 Công thức

Một lựa chọn trang trí = **kiểu dáng** (vẽ) × **loài hoa** (vẽ) × **bảng màu** (mã) × **bố cục** (mã: cụm hoa đặt ở góc nào, bao nhiêu, đối xứng hay lệch).

Với cổng: 16 khung nhận cụm hoa × 17 loài hoa và lá × 3 bố cục × 16 bảng màu ≈ **13.000 cách phối**. Thêm 4 khung vẽ liền (lá dừa, rạp đỏ, tường hoa, tường cây) × 16 bảng màu.

Nói rõ: nhiều cách phối trong số đó chỉ khác nhau một chút. Số thiết kế thật sự khác nhau bằng số khung đã vẽ. Bảng màu và loài hoa tạo ra sự phong phú, không tạo ra kiểu dáng mới.

### 1.2 Đã chứng minh và chưa chứng minh

| Kỹ thuật | Trạng thái | Bằng chứng hoặc rủi ro |
|---|---|---|
| Một món một tấm, vẽ trên nền xanh dương phẳng, mã tách nền | Đã chứng minh | Cổng tròn, bàn dài (mục 7.2) |
| Đặt món theo điểm neo và thước phối cảnh của nhân vật | Đã chứng minh | Vườn Hồ, Sân nhà quê |
| Đổi tông qua mặt nạ | Đã chứng minh, có giới hạn | Hoa: tự động. Khăn bàn: phải khoanh tay một đa giác cho mỗi kiểu bàn |
| Chỉnh sáng món rời theo cảnh | Đã chứng minh | Hệ số đo trên khăn trắng (mục 7.3) |
| Phủ hoạ tiết, chất vải lên khăn theo phối cảnh | Đã thử trên khăn chạy bàn | 8 mặt vải, 0 lượt (cuối mục 3.4). Khăn tròn phủ chấm đất nếp sâu: thử trên T8 |
| Khăn nhiều lớp (nền, phủ, chạy bàn) bằng cách trải phẳng khăn | Đã thử trên bàn tròn tranh cũ | 7 cách phối, 0 lượt. Ghế vẽ liền bàn phải tách tay; bàn rời (T8, T9) thì không cần |
| Khung, đệm ghế đổi màu; đai vẽ bằng mã | Khung, đệm: đạt. Nơ vẽ bằng mã: chưa đạt | Nơ trông như hình dán, phải vẽ (T10) |
| Bàn, ghế, đồ bàn dựng 3D, có mặt nạ và ảnh toạ độ khăn | Đã làm (25/11) | Chờ chủ dự án xem nét; ghép vào Vườn Hồ ngày và đêm đúng thước phối cảnh |
| **Khung trần + cụm hoa rời ghép bằng mã** | **Chưa thử** | Cụm hoa có thể trông lơ lửng, cuống không bám khung. Thử T1, T2 |
| **Nhiều món trên một tấm, mã cắt rời** | **Chưa thử** | Mô hình có thể vẽ các món chạm nhau, khác góc nhìn, khác cỡ. Thử T2, T3, T7, T8 |
| **Ghế rời đặt quanh bàn; bàn dài nối từ mô-đun** | **Chưa thử** | Góc nhìn của 8 ghế phải khớp nhau; mối nối bàn dài có thể lộ. Thử T7, T8, T9 |
| Người biểu diễn rời đặt vào cảnh | Chưa thử | Nét vẽ phải khớp cặp đôi. Thử T4 |
| Nền trong nhà, nền đêm giữ được thước phối cảnh | Chưa thử | Mô hình hay xê dịch cảnh khoảng 10 px. Thử T5, T6 |

Hai điều đã thấy ở bước thử trước, áp vào mọi bài thử mới:
- Mô hình không giữ vị trí và cỡ khi được bảo xoá phần còn lại. Vị trí và cỡ luôn do mã đặt.
- Phần cần đổi tông phải có màu khác hẳn phần còn lại, nếu không phải khoanh tay.

### 1.3 Để 1000 lựa chọn vẫn chơi được

- **Hai bước chọn:** chọn kiểu trước, rồi chọn màu và loài hoa. Không bày một lưới phẳng 13.000 ô.
- **Bộ phong cách:** 21 bộ phối sẵn (mục 3.9), mỗi bộ là một lựa chọn đẹp chắc chắn. Ai muốn thì bấm "Tự phối".
- **Nhãn quyết định chỉ số:** mỗi món có nhãn phong cách (truyền thống, hiện đại, mộc, sang, vui), tông màu và mức giá. Ảnh hưởng tới nhà trai, nhà gái, tình cảm và căng thẳng tính từ nhãn, không viết tay cho từng món. Ví dụ: họ hàng lớn tuổi thích nhãn "truyền thống", bạn bè thích "vui"; các món cùng một bộ hoặc cùng tông thì được cộng điểm "hài hoà".
- **Thêm món không cần sửa mã:** mỗi món là một dòng dữ liệu (tên, tệp hình, nhãn, giá, điểm neo).

## 2. Nguồn cảm hứng

Lần đầu mình không mở được trang báo cáo gốc của Pinterest nên lấy qua công cụ tìm kiếm và các bài tổng hợp. Ngày 25/11, sau khi chủ dự án mở mạng, mình đã đọc trọn báo cáo 2026 và 2025 và đối chiếu lại bảng dưới (danh sách ở cuối). Game chỉ lấy **ý tưởng chung** của từng xu hướng, đặt tên Việt hư cấu, không chép hình cụ thể nào trên Pinterest.

| Xu hướng (nguồn) | Ý chính | Đưa vào game |
|---|---|---|
| Ethereal Shimmer, sắc xà cừ (Pinterest 2026) | Ánh kim, ánh ngũ sắc, hiệu ứng "phát sáng" | Bảng màu "Ánh xà cừ"; mã phủ ánh ngũ sắc lên khung gương và khăn |
| Unexpected Venues, nơi bất ngờ (Pinterest 2026) | Tiệc ở quán jazz, phòng rượu tầng hầm, nhà hát cũ, nhà kính | Nơi "Câu lạc bộ jazz" và "Nhà kính" (mục 4); bộ "Đêm jazz" |
| Quirky Cakes (Pinterest 2026) | Bánh cưới lạ mắt, vui | Tấm bánh cưới có kiểu "bánh vui" (mục 3.8) |
| Nostalgic Tech Touches (Pinterest 2026) | Máy hát đĩa, máy ảnh lấy liền, giải trí kiểu cũ | Góc ảnh hoài cổ; bộ "Hoài cổ analog" |
| Alt Bouquets, Messy Coquette Decor and Sensory Styling (Pinterest 2026) | Hoa không theo lối cũ; xếp lớp vải rủ, ren, nhung, kính màu; quầy hoa, thảo mộc, cam quýt và rau củ làm hoa bàn | Hoa bàn cam quýt, quầy hoa tự cắm; bộ "Nơ và cam quýt" |
| Nâu là màu của năm (Pinterest 2025) | Tông nâu, mocha | Bảng màu "Nâu mocha" |
| Surreal Florals (Pinterest 2025) | Hoa rum, thược dược, hồng môn, hoa giấy, hoa treo | Các loài này có trong mục 3.2; khung "mái hoa treo" |
| Wildflower (Pinterest 2025) | Hoa đồng nội | Loài "hoa đồng nội"; bộ "Đồng nội" |
| Pháo lạnh (The Knot) | Máy phun tia sáng không nóng; theo The Knot, mỗi đợt thường kéo dài 15–30 giây | Hiệu ứng mã (mục 5) |
| Giải trí cho khách (The Knot) | Hoạ sĩ vẽ trực tiếp, giải trí tương tác, hoài cổ | Nhóm tiết mục "tương tác" (mục 6.5) |
| Cổng lễ theo hình (WeddingWire, Singaporebrides) | Tròn, tam giác, lục giác, ống kim loại, tường cây, cổng sắt, cửa gỗ cũ | Danh sách khung (mục 3.3) |
| Việt Nam (VnExpress, Lao Động, Tinh tế) | Cá nhân hoá, tinh gọn có điểm nhấn, ngoài trời, dùng công nghệ | Màn LED kể chuyện cặp đôi, chữ neon tên riêng, nhiều tiệc ngoài trời |

## 3. Danh mục trang trí

"Vẽ" là tốn lượt; "Mã" là không tốn lượt. Số tấm tính theo giả định các bài thử ở mục 8 đạt.

**Món màu xanh dương** (gốm lam, cẩm tú cầu xanh, đồ tông xô thơm): nền tách là xanh dương và mã gỡ ánh xanh khỏi viền, nên các món này vẽ màu trắng hoặc trung tính rồi để mã nhuộm xanh. Món nào bắt buộc vẽ xanh thì vẽ trên nền màu khác và tách với tuỳ chọn `giu_xanh`.

### 3.1 Bảng màu (mã, 0 tấm)

| # | Tên | Màu chính | Gợi từ |
|---|---|---|---|
| 1 | Vườn trắng | trắng ngà, xanh lá | vườn cổ điển |
| 2 | Hồng phấn | hồng phấn, kem | pastel |
| 3 | Đỏ son | đỏ son, vàng kim | cưới truyền thống Việt |
| 4 | Nâu mocha | nâu sữa, kem, nâu đậm | Pinterest 2025 |
| 5 | Ánh xà cừ | trắng ngọc trai ánh ngũ sắc, bạc | Pinterest 2026 |
| 6 | Đen vàng | đen, trắng, vàng đồng | art deco, speakeasy |
| 7 | Đất nung | cam đất, be | mộc boho |
| 8 | Oải hương | tím nhạt, bạc | — |
| 9 | Gốm lam | xanh lam, trắng | gốm Việt |
| 10 | Xô thơm | xanh xám, trắng | — |
| 11 | Đồng nội | vàng bơ, xanh non, tím nhẹ | Pinterest 2025 |
| 12 | Đỏ rượu | đỏ rượu, hồng đào | màu đậm 2026 |
| 13 | Cam quýt | cam, vàng chanh, xanh lá | Pinterest 2026 |
| 14 | Sen Huế | hồng sen, xanh lá sen | Huế |
| 15 | Đào mai | hồng đào, vàng mai | Tết |
| 16 | Rực rỡ | nhiều màu tươi | colourful eclectic |

### 3.2 Loài hoa và lá (vẽ, 17 tấm)

Mỗi tấm là **một loài**, vẽ 4 cụm rời trên nền xanh dương: cụm góc lớn, dải rủ dài, cụm nhỏ tròn, cụm chân đế. Hoa vẽ màu sáng để mã nhuộm được.

hồng · mẫu đơn · cẩm tú cầu · lan hồ điệp · cát tường · hoa baby · rum (calla) · thược dược · hồng môn · sen · cúc hoạ mi · hướng dương · oải hương · hoa giấy (bông giấy) · hoa đồng nội · hoa làm bằng giấy · **cụm lá** (bạch đàn, cỏ lau, dương xỉ)

Sen, cúc hoạ mi và hoa giấy là hoa quen ở Việt Nam. Rum, thược dược, hồng môn, hoa làm bằng giấy theo xu hướng hoa siêu thực.

### 3.3 Khung cổng và phông lễ (20 khung; 6 khung đơn giản đã làm bằng mã, còn 14 tấm vẽ)

| # | Khung | Nhận cụm hoa | Hợp với |
|---|---|---|---|
| 1 | Vòm cong (dáng cổng hiện nay) | có | vườn |
| 2 | Vòng tròn kim loại vàng (đã có, vẽ lại bản trần) | có | hiện đại |
| 3 | Lục giác kim loại đen | có | hiện đại, đen vàng |
| 4 | Tam giác gỗ | có | mộc, biển |
| 5 | Khung chữ nhật gỗ mộc (cột và xà) | có | mộc, vườn |
| 6 | Vòm cao kiểu nhà thờ | có | sang, cổ điển |
| 7 | Cổng sắt rèn cổ | có | cổ điển |
| 8 | Khung tre | có | quê, mộc |
| 9 | Vòng trăng (bức tường có ô tròn, kiểu Á Đông) | có | Huế, sen |
| 10 | Khung gương vòm | có | xà cừ, trong nhà |
| 11 | Khung ống có rèm voan rủ | có | biển, tối giản |
| 12 | Gỗ trôi dạt | có | biển |
| 13 | Ba tấm vòm xếp tầng | có | trong nhà, sân khấu |
| 14 | Cột đá đôi có dầm | có | cổ điển |
| 15 | Khung treo rèm đèn (đèn do mã vẽ) | có | đêm |
| 16 | Mái hoa treo phía trên lối đi | có | hoa siêu thực |
| 17 | Cổng lá dừa | vẽ liền | miền Tây, biển |
| 18 | Cổng rạp đỏ chữ Song Hỷ | vẽ liền | truyền thống |
| 19 | Tường hoa phẳng | vẽ liền | sang, chụp ảnh |
| 20 | Tường cây xanh | vẽ liền | tối giản, vườn |

### 3.4 Bàn khách và cách xếp (bàn ghế phần lớn dựng 3D; cách xếp là mã)

Chủ dự án góp ý (25/11): tiệc ở châu Âu xếp bàn rất đa dạng, kể cả khi có 1000 khách: bàn vuông, tròn, dài, bàn 6, 10, 20 người. Game làm được điều này nếu **bàn, ghế và cách xếp tách rời nhau**.

**Vẽ bộ phận, mã lắp lại:**

- **Bàn tròn** nhìn từ mọi hướng đều như nhau, nên mỗi cỡ chỉ cần một hình.
- **Bàn dài** vẽ thành 3 mảnh: đầu trái, đoạn giữa, đầu phải. Mã nối một đầu, nhiều đoạn giữa, một đầu thành bàn 8, 12, 20 hay 40 người. Bàn chạy ngang khung hình thì các đoạn giữa cùng cỡ nên nối dễ. Bàn chạy dọc vào sâu thì mỗi đoạn nhỏ dần, thử sau.
- **Ghế** vẽ riêng, mỗi kiểu ghế một tấm gồm 8 góc nhìn (trước, sau, hai bên, bốn góc chéo). Mã đặt ghế quanh bàn theo số người, ghế phía sau bị bàn che đúng thứ tự. Nhờ vậy một kiểu bàn ngồi được 6, 8, 10 hay 12 người, với kiểu ghế nào cũng được.
- **Khăn** vẽ màu trắng trên gỗ hoặc kim loại màu khác hẳn, để mặt nạ đổi màu làm tự động.

| Tấm | Có gì |
|---|---|
| Bàn tròn trần | 4 cỡ: 6, 8, 10, 12 người; khăn trắng phủ chấm đất |
| Bàn vuông, bàn chữ nhật | vuông 4 và 8 người; chữ nhật 6 người |
| Bàn dài mô-đun, chạy ngang | đầu trái, đoạn giữa, đầu phải; khăn trắng phủ chấm đất để mã xếp lớp khăn phủ, khăn chạy bàn (đổi ngày 25/11, đã duyệt). Dùng cho bàn hoàng gia, chữ U, chữ E |
| Bàn dài mô-đun, chạy chéo | như trên, theo hướng chéo của bàn dài đã có; lật gương cho bên kia. Dùng cho kiểu xương cá |
| Bàn khác | bàn cocktail đứng, bàn bán nguyệt, bàn cho riêng cặp đôi |
| 4 kiểu ghế × 8 góc nhìn | chiavari, lưng chéo, trong suốt, ghế bọc vải có nơ (sảnh tiệc, rạp quê). Màu gỗ, sơn và kim loại đổi bằng mã: gỗ sáng, óc chó, sơn trắng, sơn đen, vàng, bạc |

**13 cách xếp (mã, 0 tấm):**

| # | Cách xếp | Hợp với |
|---|---|---|
| 1 | Lưới bàn tròn thẳng hàng | tiệc Việt quen thuộc (bàn 10 khách như trong `gia-tham-khao.md`), mọi cỡ |
| 2 | Bàn tròn so le | thoáng, dễ đi chào bàn |
| 3 | Các hàng bàn dài song song | kiểu tiệc gia đình, hai họ ngồi lẫn |
| 4 | Xương cá (bàn dài chéo hai bên lối giữa) | ngoài trời, nhìn rõ cặp đôi |
| 5 | Chữ U | dưới 60 khách, trang trọng |
| 6 | Chữ E, răng lược (bàn hoàng gia và các bàn dài vuông góc) | 100–300 khách, sảnh lớn |
| 7 | Chữ T | tiệc nhỏ |
| 8 | Hình vuông rỗng | tiệc thân mật, ai cũng thấy nhau |
| 9 | Bàn hoàng gia phía trước và bàn tròn | sảnh tiệc |
| 10 | Một bàn dài xuyên suốt | tiệc làng, cả họ một bàn |
| 11 | Bàn dài ở giữa, bàn tròn hai bên | trộn kiểu |
| 12 | Quây quanh sàn nhảy | tiệc tối có tiết mục |
| 13 | Tiệc đứng: bàn cocktail rải rác, vài bàn ngồi cho người lớn tuổi | trẻ trung, rẻ |

**Ghế dự lễ (làm ngày 26/11, theo ảnh tham khảo):** 4 cách xếp đã chạy trong trang thử (thẳng hàng, hình quạt, khối chéo, vòng tròn quanh bục), dùng ghế chiavari 3D ở 16 hướng và phối cảnh đo lại trên tranh. Bàn dài xuyên suốt (giữa lối, hai dãy, ba dãy) dựng 3D bằng máy ảnh phối cảnh khớp tranh; lối đi có thêm thảm trắng, thảm đỏ, lối gương nước bằng mã. Chi tiết ở `tham-khao-thiet-ke-tiec.md` mục 4.

**Từ 30 tới 1000 khách:**

- Mã tính số bàn từ số khách và số chỗ mỗi bàn, rồi rải bàn theo cách xếp đã chọn. Bàn xa nhỏ dần theo cùng thước phối cảnh với nhân vật, vẽ từ xa tới gần cho đúng thứ tự che khuất.
- Mỗi nơi đo một lần **vùng đất đặt được bàn**. Từ đó ra **sức chứa thật** của nơi đó. Đông khách quá thì phải chọn nơi rộng hơn hoặc đổi cách xếp. Đây cũng là một quyết định của người chơi.
- Cảnh vẽ tay chỉ thấy rõ vài hàng bàn gần. Với tiệc vài trăm tới 1000 khách, game có thêm **sơ đồ nhìn từ trên xuống** vẽ bằng mã: người chơi chọn cách xếp, kéo bàn và thấy cả hội trường.

**Ảnh hưởng tới chỉ số (số tạm, tính từ nhãn):**

- Bàn tròn 10 quen với họ hàng lớn tuổi, phục vụ nhanh.
- Bàn dài cho hai họ ngồi lẫn, dễ trò chuyện, nhưng cần nhiều khăn chạy bàn và hoa rải dọc bàn.
- Chữ U, chữ E, hình vuông rỗng trang trọng, ai cũng thấy cặp đôi, nhưng tốn chỗ.
- Tiệc đứng rẻ và trẻ trung, nhưng người lớn tuổi mệt nếu thiếu ghế.
- Chi phí nhân theo số bàn: khăn, hoa bàn, người phục vụ.

**Có thể thêm sau:** trò **xếp chỗ ngồi**. Người chơi đặt các nhóm khách (họ nội, họ ngoại, bạn cô dâu, đồng nghiệp chú rể, ông bà, trẻ con) vào bàn, với vài luật như ông bà ngồi gần sân khấu, hai người đang giận nhau thì không ngồi chung. Kết quả ảnh hưởng tới lòng hai họ.

#### Khăn, ghế và đồ trên bàn (tìm hiểu ngày 25/11)

Chủ dự án góp ý: ngoài đời khăn bàn có rất nhiều thiết kế, còn có áo ghế, nơ ghế, và trang trí bàn ghế bằng nơ, bằng giấy.

**Cách tìm.**
- Ba lượt tìm riêng cho khăn bàn, ghế và đồ trên bàn, bằng tiếng Anh và tiếng Việt. Khoảng 130 trang hiện trong kết quả.
- **Lượt đầu chỉ đọc được đoạn trích**, vì mạng của môi trường làm việc chặn các trang cưới. Phần danh mục dưới đây lấy từ đoạn trích, phần lớn là trang nhà cung cấp và blog.
- **Lượt sau (cùng ngày), chủ dự án đã mở mạng:** đọc trọn 46 trang: 41 bài của CV Linens, 4 trang Pinterest, 1 bài Style Me Pretty (bài tổng hợp Pinterest của họ chỉ dành cho người trả phí). Kết quả nằm ở hai phần "Khăn nhiều lớp" và "Trang trí ghế theo lớp" bên dưới, có ghi mã nguồn như [C1].
- The Knot và WeddingWire trả "Access Denied" cho máy truy cập tự động, mình không vượt. Brides, Martha Stewart và Vogue bị chính công cụ tìm kiếm từ chối.
- Mình bỏ mọi giá và con số thống kê. Danh sách nguồn ở cuối tài liệu.

**Chia theo cách làm ra hình.** Đây là phần quan trọng nhất, vì nó quyết định món nào tốn lượt.

| Loại | Khác nhau ở đâu | Cách làm | Tốn lượt |
|---|---|---|---|
| A. Màu | chỉ màu | nhuộm qua mặt nạ (đã thử, mục 7b) | 0 |
| B1. Chất vải không theo hướng | kim sa, nhung, lanh thô, voan mỏng | mã phủ hạt và ánh lên vùng mặt nạ; dùng được cho mọi món có mặt nạ, kể cả áo ghế và nơ | 0 |
| B2. Hoạ tiết có hướng | ca rô, sọc, hoa in, ren, gấm hoa, thêu | mã phủ theo toạ độ vải; mỗi dáng và mỗi góc nhìn phải đo tay toạ độ vải một lần. Mới thử trên khăn chạy bàn | 0, nhưng tốn công đo |
| C. Món gắn thêm | thêm một vật lên món cũ: nơ, cụm hoa, khăn phủ, bảng tên | vẽ hình rời một lần, nhiều món chung một tấm; mã đặt và nhuộm | ít |
| D. Dáng mới | đổi hình cả món: áo ghế bọc kín, váy quây xếp ly | vẽ món mới | mỗi dáng một tấm; ghế thì mỗi dáng một bộ góc nhìn |

**Đã thử loại B1 và B2 ngày 25/11, 0 lượt.**
- Trên chính tấm bàn dài đã có, mã gán cho mỗi điểm của khăn chạy bàn một toạ độ trên vải: dọc và ngang khăn, tính bằng mét, theo phối cảnh của tấm vẽ. Mã sinh hoạ tiết theo toạ độ đó, rồi nhuộm bằng đúng công thức đổi màu đang dùng.
- Ra 8 mặt vải: kẻ ca rô, sọc, hoa nhí in khuôn, ren trắng trên nền hồng, kim sa vàng, nhuộm loang, hoa văn hình học nền chàm, nhung xanh ngọc.
- Hoạ tiết nhỏ dần về phía xa và nối liền qua chỗ khăn gập xuống đầu bàn. Nếp vải và bóng ly vẫn giữ.

Giới hạn đã thấy:
- Mỗi kiểu khăn phải đo tay một lần vài điểm (mép khăn, chỗ gập) và khoanh bỏ các đĩa đè lên mép khăn. Khi vẽ bàn mới, nên dặn mô hình không đặt đĩa đè lên mép khăn.
- Hoạ tiết nằm theo mặt phẳng, chưa uốn theo nếp vải. Khăn chạy bàn nếp nhỏ nên không lộ. Khăn tròn phủ chấm đất có nếp sâu thì phải thử trên bàn tròn T8: quấn hoạ tiết quanh thân bàn như quanh một hình trụ.
- Màu rất đậm (nhung) làm ly đặt trên khăn tối hẳn. Có thể giảm nhuộm ở chỗ ly.
- Vải có khối nổi (hoa vải nổi, vải nhún) thì mã không làm giả được, nên xếp vào loại D.
- Trong game: mỗi kiểu khăn lưu sẵn một ảnh toạ độ nhỏ, trình duyệt sinh hoạ tiết theo ảnh đó. Mã thử ở `docs/game/ve/hoa_tiet.py`.

**Khăn bàn.**
- **B1, 0 tấm:** lanh thô, satin bóng, nhung, kim sa, voan mỏng phủ trên nền khác màu, nhuộm loang; rải trên khăn: pháo giấy kim tuyến, cánh hoa (mã rải).
- **B2, 0 tấm, đo toạ độ vải mỗi kiểu khăn:** ren phủ, thêu, gấm hoa cùng tông, kẻ ca rô, sọc, hoa nhí in khuôn, tranh đồng quê một màu, sứ xanh trắng, hoa văn hình học, chữ cái tên cặp đôi thêu ở góc.
- **C, vẽ, gộp tấm:** khăn phủ vuông chéo góc trên khăn tròn; khăn chạy bàn bằng vải gạc rủ dài; dây lá thay khăn chạy bàn; rêu chạy bàn; dải vải rủ vòng có hoa ở chỗ túm (bàn cặp đôi, bàn hoàng gia); tấm lót chỗ ngồi đan cói. Gương chạy bàn thì làm bằng mã.
- **D, vẽ dáng mới:**
  - khăn tròn phủ chấm đất (đã có trong T8);
  - khăn ngắn ngang đùi;
  - **váy quây xếp ly**, rất phổ biến ở Việt Nam cho bàn đón khách, bàn trưng ảnh, bàn gia tiên;
  - váy voan xoè nhiều lớp;
  - khăn bọc kín bằng vải thun;
  - lụa phồng rủ thành đống;
  - vải có khối nổi: hoa vải nổi, xếp ô nhỏ, vải nhăn bóng;
  - bàn gỗ trần, không khăn.

**Ghế.**
- **Kiểu ghế (D, mỗi kiểu một bộ góc nhìn):**
  - chiavari (nhà cung cấp Việt Nam gọi là ghế Tiffany);
  - lưng chéo;
  - trong suốt (kiểu Napoleon, Louis);
  - ghế xếp inox có đệm và ghế nhựa đúc (rạp ở quê);
  - ghế banquet khách sạn (thường bọc áo);
  - ghế gỗ uốn;
  - ghế lưng chữ Y;
  - ghế Louis lưng bầu dục bọc vải;
  - ghế nhung;
  - ghế mây lưng công và ghế vua – hoàng hậu cho cặp đôi;
  - ghế trẻ em.
- **Áo ghế (D):** áo thun bó (nhà cung cấp gọi là "áo ghế thun 4 chiều"); áo satin rộng thắt nơ sau lưng; áo có váy xếp ly chấm đất; váy voan xoè; chụp đầu ghế. Mỗi kiểu là một dáng ghế mới. Vẽ màu trắng thì màu và chất vải không theo hướng (kim sa, nhung, voan) làm bằng mã. Hoạ tiết in trên áo ghế thì phải đo toạ độ vải cho từng góc trong 8 góc, nên để sau. Áo xếp ly là dáng riêng (loại D).
- **Nơ và đai ghế (C):**
  - chất: satin, voan, chiffon, vải tuyn, vải bố, ren, nhung, kim sa, vải thun. Nơ cùng dáng thì đổi chất bằng mã;
  - kiểu buộc: nơ bướm, nút đơn, hoa hồng, rủ dọc lưng ghế, bắt chéo, luồn qua song ghế chiavari, nơ đuôi dài, đai có khoá cài đá;
  - nhà cung cấp Việt Nam gọi "ghế trắng nơ vàng" là kiểu cổ điển ở sảnh tiệc.
- **Món gắn lên ghế (C).** Thường chỉ gắn ở ghế đầu hàng lối đi hoặc ghế cặp đôi:
  - cụm hoa; bó lá buộc ruy băng; dây lá vắt qua cả hàng ghế; bó cỏ lau;
  - phễu giấy đựng cánh hoa; quả cầu hoa treo; vòng hoa tròn;
  - tuyn và ruy băng dài; tua rua; đèn lồng nhỏ;
  - bảng tên (Cô dâu, Chú rể, họ hai nhà);
  - nơ thật to bằng satin, nhung hay tuyn;
  - quạt giấy tròn đặt trên mỗi ghế (khách cầm quạt luôn); chong chóng giấy; hoa giấy nhún.

**Ghế làm số tấm nhân lên, nên chỉ vẽ những góc mà cảnh dùng tới:**
- **Kiểu ghế và áo ghế:** đủ 8 góc, vì quanh bàn tròn ghế quay đủ hướng.
- **Nơ và đai:** nằm sau lưng ghế, nên chỉ cần 3 góc (sau, sau chéo, ngang) và lật gương ra phía kia. Ghế quay mặt ra phía trước thì nơ gần như khuất, mã vẽ thêm một dải vải ngang lưng ghế là đủ.
- **Món gắn ghế lối đi:** 1 góc (sau chéo), lật gương cho bên kia lối đi.
- **Ghế cặp đôi:** 1 góc (trước chéo).

**Đồ trên bàn.**
- **Bộ chỗ ngồi:**
  - đĩa lót: thuỷ tinh viền hạt vàng, viền hạt đen, gương viền pha lê, mây, mica; dáng tròn, hình hoa, lượn sóng;
  - bát đĩa cổ, mỗi chỗ một kiểu;
  - ly: thuỷ tinh màu (hổ phách, hồng), pha lê cắt, ly gân, viền vàng; dáng coupe, flute, ly chân cao;
  - dao nĩa: vàng, vàng mờ, đen mờ.
- **Khăn ăn:**
  - chất và màu (loại B, A);
  - kiểu gấp (loại D): mũ giám mục, quạt, hoa hồng, túi đựng dao nĩa, nút thắt, kim tự tháp, hoa sen, vương miện, cây nến, chong chóng, búp măng, áo sơ mi, gấp phẳng kẹp thực đơn;
  - vòng và dây buộc (loại C): vòng khăn, ruy băng, dây gai, nhánh hoa.
- **Đồ giấy:** thiệp tên; thực đơn; số bàn; tên viết trên lá, trái cây, viên ngói; niêm phong sáp.
- **Trang trí bằng giấy:**
  - hoa giấy nhún; quả cầu tổ ong; hạc giấy; quạt giấy; đèn lồng giấy nhỏ;
  - khăn chạy bàn bằng giấy kraft đóng dấu hoặc giấy ren;
  - **chữ Hỷ** ép kim hoặc cắt laser (có nguồn Việt Nam);
  - pháo giấy rải bàn.
  - Hạc giấy: chủ dự án để mình đặt ở đâu cũng được (25/11). Hạc giấy có ở bốn chỗ: chuỗi hạc treo trên cao (mục 3.7), một con hạc nhỏ giữ thiệp tên ở mỗi chỗ ngồi, tường hạc làm phông chụp ảnh (mục 3.8), và bộ phong cách "Nghìn hạc" (mục 3.9). Hạc gấp giấy là khối phẳng ít mặt, dựng 3D được, nên dự kiến 0 tấm.
- **Món nhỏ khác:**
  - nến cây màu, nến trụ, nến cốc, đèn bão, chân nến nhiều nhánh, nơ buộc chân nến;
  - trái cây (cam quýt, lựu, nho, lê) bày như tranh tĩnh vật;
  - bình hoa nhỏ một cành; gương; pha lê;
  - quà ở mỗi chỗ: nến thơm, sô-cô-la, sen đá nhỏ, gói hạt giống;
  - nơ trên chân ly, trên dao nĩa.

**Nhỏ quá thì không thấy trong cảnh, nên thêm màn cận cảnh bàn.** Ở cỡ cảnh, khăn ăn gấp, thiệp tên, dao nĩa và đĩa lót chỉ còn vài điểm ảnh. Chủ dự án chọn (25/11): thêm **một góc nhìn cận cảnh vào bàn** để cặp đôi xem rõ và ra quyết định. Kế hoạch ở phần "Màn cận cảnh bàn" bên dưới.

Món đủ lớn để thấy trong cảnh (nến, chân nến, đèn lồng nhỏ, quạt giấy, quả cầu tổ ong, chữ Hỷ cắt giấy, trái cây) đi cùng hoa bàn ở mục 3.5.

**Đang thịnh và đã cũ** (theo đoạn trích, không có số liệu):
- **Đang thịnh 2025–2026:**
  - bàn "sưu tầm": mỗi chỗ một kiểu bát đĩa;
  - vải có chất (lanh, nhung, ren) và có màu; đồ thêu;
  - nơ; trái cây trên bàn; nến màu;
  - vải rủ thành nếp lớn; chrome và gương.
- **Màu hay gặp:** xanh xô thơm, hồng đất, vàng bơ, xanh phấn, đất nung, oải hương. Ở Việt Nam năm 2026 có thêm cappuccino, mocha.
- **Bị chê là cũ:** khăn polyester trắng trơn; mọi thứ cùng một màu; áo ghế rộng thắt nơ (theo vài blog và diễn đàn nước ngoài). Ở Việt Nam áo ghế có nơ vẫn rất phổ biến.
- **Sảnh tiệc ở Việt Nam:** bàn tròn 10 người; khăn satin chấm đất màu trắng, vàng, đỏ hoặc xanh, thường hai lớp; ghế bọc áo có nơ voan hoặc satin.
- **Rạp ở quê:** bàn tròn 8–10 người; khăn trắng hoặc đỏ; ghế inox có đệm hoặc ghế nhựa. Gói nâng cấp có ghế nơ và khăn hai lớp.

**Thành chỉ số** (số tạm, tính từ nhãn như mục 1.3):
- Áo ghế có nơ: họ hàng lớn tuổi khen sang, bạn trẻ thấy cũ.
- Bàn "sưu tầm": ngược lại.
- Khăn và ghế cùng bảng màu với cổng: được cộng "hài hoà".

**Vẽ thêm (đã tính vào mục 7):**

| Tấm | Có gì | Loại |
|---|---|---|
| Váy quây xếp ly | bàn dài và bàn đón khách phủ váy quây xếp ly trắng | D |
| Áo ghế thun bó, 8 góc | ghế banquet bọc áo thun trắng | D |
| Nơ ghế, 3 tấm | 8 kiểu nơ và đai màu trắng; mỗi tấm một góc: sau, sau chéo, ngang | C |
| Món gắn ghế lối đi | cụm hoa, bó lá, phễu giấy, vòng hoa, quạt giấy, bảng tên, tua rua, đèn lồng nhỏ; góc sau chéo | C |
| Khăn phủ và khăn chạy bàn | khăn phủ vuông trên bàn tròn, khăn gạc rủ, dây lá, rêu | C |
| Nến và giấy trên bàn | 6 kiểu nến và chân nến; quạt giấy, quả cầu tổ ong, chữ Hỷ, đèn lồng giấy nhỏ, hoa giấy | C |
| Ghế cặp đôi | ghế mây lưng công, ghế vua – hoàng hậu, ghế Louis; góc trước chéo | D |

Cộng 9 tấm nếu vẽ được nhiều món trên một tấm (T2, T3, T7, T8). Nếu không được thì khoảng 19 tấm, và phải bớt số kiểu nơ và số món gắn ghế. Màn cận cảnh bàn tính riêng (phần dưới).

#### Khăn nhiều lớp (thử ngày 25/11, 0 lượt)

Chủ dự án hỏi: ngoài một lớp khăn, có thêm được một lớp khăn phủ cả bàn và khăn chạy bàn bên trên không? Được. Ngoài đời cũng làm đúng như vậy.

**Ngoài đời xếp lớp thế nào** (đọc trọn các bài của CV Linens; số đo giữ đơn vị inch như trang gốc):
- **Thứ tự từ dưới lên:** khăn nền chấm đất, khăn phủ, khăn chạy bàn, rồi đĩa lót và khăn ăn. Một bài gọi ba lớp khăn này là chuẩn của bàn tiệc sang [C1].
- **Bàn khách và bàn chính:** bàn khách thường chỉ có khăn nền, khăn chạy bàn và khăn ăn; khăn phủ để dành cho bàn chính, bàn bánh, bàn cặp đôi [C10]. Mỗi bàn chỉ nên có một lớp nổi bật [C2].
- **Khăn phủ** rộng bằng đường kính bàn cộng hai lần độ rủ muốn có, không nhất thiết chấm đất [C3]. Khăn vuông đặt chéo trên bàn tròn thì rủ thành bốn mũi nhọn [C2][C3].
- **Khăn chạy bàn** dài bằng bàn cộng hai lần độ rủ, rộng khoảng một phần ba bàn, và không rủ thấp hơn khăn nền [C8]. Có thể đặt dọc, đặt ngang giữa các chỗ ngồi, hoặc bắt chéo trên bàn tròn [C8][C9][C17]. Hai dải thì đặt song song, chữ thập, lệch chéo, hoặc chồng dải hẹp lên dải rộng [C7].
- **Phối chất vải** [C1][C3][C7]:
  - voan trên satin ngà; ren trên satin hồng; ren trắng trên satin xanh bụi;
  - khăn trắng chấm đất với khăn phủ kim sa vàng;
  - chạy bàn kim sa vàng trên satin đỏ đô; kim sa bạc trên nền xanh than.
- **Kiểu khác:** vén khăn thành những vòng rủ dọc cạnh bàn dài [C12]; váy quây xếp hộp, nhún, voan, tutu [C13].
- **Xu hướng:**
  - CV Linens 2026 xếp "nhiều lớp chất liệu, trộn vải" vào mục đang thịnh, và "lấp lánh quá đà" (kim sa, đá) vào mục đã cũ [C15]. Một bài khác của cùng trang vẫn dùng kim sa cho bàn chính [C1].
  - Pinterest 2026, mục "Messy Coquette Decor and Sensory Styling": xếp lớp vải rủ, kính màu, ren, nhung; trong các từ khoá có "lace napkin", "moss tablescape" [P1].

**Cách làm bằng mã: trải phẳng khăn.**
- Mã quy mỗi điểm trên khăn về một toạ độ trên mặt phẳng bàn. Điểm trên mặt bàn giữ nguyên toạ độ. Điểm ở phần rủ, ở góc θ và rủ xuống một đoạn t, là điểm vải cách tâm bàn 1 + t (tính theo bán kính).
- Nhờ vậy mỗi lớp khăn chỉ là một hình phẳng: tròn, vuông, vuông chéo góc, dải chạy bàn. Phần vải thừa ra ngoài mép bàn tự rủ xuống đúng chỗ. Khăn vuông chéo góc rủ thành bốn mũi nhọn; khăn tròn ngắn có gấu nằm ngang.
- Mỗi lớp có màu và chất vải riêng (dùng các hoạ tiết ở phần trên). Nếp vải và bóng lấy từ tranh gốc. Mã thêm bóng mờ dưới gấu của lớp trên và một đường viền gấu.
- Bàn dài làm y hệt, chỉ thay hình trụ bằng hình hộp: mặt bàn chữ nhật và bốn mặt rủ.
- Mã: `docs/game/ve/khan_lop.py`.

**Đã thử trên bàn tròn của tranh cũ "cảnh gọn".** Ra 7 cách phối:
1. vuông chéo góc bằng ren trên nền xanh xô thơm;
2. vuông gấm vàng trên nền đỏ;
3. tròn ngắn kim sa trên nền hồng;
4. ba lớp: nền trắng, vuông chéo góc hồng đất, chạy bàn nhung;
5. voan trắng mỏng trên nền vàng bơ;
6. nền chàm, khăn phủ tròn hoa nhí, hai dải chạy bàn chữ thập;
7. nền xanh than, vuông chéo góc kim sa bạc, chạy bàn ngang.

Đệm ghế đổi màu theo khăn.

Giới hạn đã thấy:
- Tranh cũ vẽ ghế liền với bàn, nên phải tách khăn khỏi ghế bằng tay, chọn từng mảnh vải lọt giữa các nan ghế. Trên khăn màu đậm còn vài đốm sáng ở chân ghế, và vài cái đĩa bị nhuộm nhầm.
- Khăn phủ dùng nếp vải của khăn nền, nên nếp của hai lớp trùng nhau. Ở cỡ cảnh thì không lộ.

**Còn bàn dài đang có thì sao?** Gỗ, khăn chạy bàn và 12 ghế của nó nằm chung một hình, và bốn ghế phía trước che mặt trước bàn. Muốn phủ khăn nền lên bàn này thì phải tách ghế bằng tay như trên, còn khó hơn.

Cách gọn là **đổi T9** (chủ dự án đã duyệt ngày 25/11): vẽ bàn dài phủ khăn trắng chấm đất, không khăn chạy bàn, không ghế, không đĩa đè lên mép khăn. Khi đó khăn phủ, khăn chạy bàn và vòng rủ đều do mã làm. Bàn gỗ có khăn chạy bàn đang có thì giữ làm kiểu "bàn gỗ trần".

**Kết luận thiết kế:** xếp lớp rất dễ khi bàn và ghế là hình rời (T7 ghế, T8 bàn tròn, T9 bàn dài). Việc tách tay chỉ cần cho tranh cũ.

**Trong game:** bản đồ trải phẳng được tính sẵn một lần cho mỗi hình bàn và lưu thành một ảnh nhỏ. Trình duyệt ghép các lớp một lần cho mỗi kiểu khăn, rồi dùng lại kết quả cho mọi bàn giống nhau.

**Lựa chọn cho người chơi (đều 0 tấm):**
- **Khăn nền:** chấm đất (có trong T8, T9). Khăn ngắn ngang đùi và váy quây thì phải vẽ thêm. Màu và chất vải tự do.
- **Khăn phủ:** không có, tròn ngắn, vuông thẳng, vuông chéo góc, voan mỏng chấm đất; chỉnh được độ rủ.
- **Khăn chạy bàn:** không có, dọc, ngang, chữ thập, hai dải song song, dải hẹp chồng lên dải rộng; chỉnh được độ rủ.
- **Gợi ý theo nguồn:** bàn khách 2 lớp, bàn chính 3 lớp. Bàn nào cũng 3 lớp có hoạ tiết thì game trừ điểm "rối mắt" (số tạm).

#### Trang trí ghế theo lớp

**Ngoài đời** (đọc trọn các bài của CV Linens):
- **Đai voan luồn song ghế chiavari** có 4 kiểu [H2]: đan thang (mỗi dải thay đổi trên dưới, rủ xuống sàn), đan thang đều thành một "thác" phía trước, đan ngang lưng ghế, và thác một bên cột.
- **Kiểu buộc:** túm ba vòng, chéo góc, quấn đôi, nơ hộp quà, nơ hai vòng, rủ thác, nút bên [H3]–[H8]. Kiểu đang được gợi ý: hai màu chồng nhau, trộn chất vải, cài trâm hoặc hoa vào nơ [H8].
- **Đai thun:** đai ren chồng lên đai trơn; trâm đá đặt lệch một bên; đai giữ một bông hồng to hay một cành liễu cong [H10]. Có cả đai kết hoa hồng vải và đai nhung nhún [H11].
- **Áo lưng ghế:** năm tầng bèo taffeta, đi cùng chụp đầu ghế [H12]; áo voan kiểu cành liễu, đồng bộ với váy bàn [H13]; hoa voan cỡ lớn gắn lưng ghế [H14].
- **Hoa trên ghế:** gắn ở đỉnh lưng, bên hông, hoặc sát mặt ngồi; mùa xuân dùng hoa giấy, quả bông [H15]. Buộc bằng dây kẽm cắm hoa hoặc dây rút; hay dùng bạch đàn, vòng hoa [H16].
- **Tiết chế:**
  - "biển áo ghế trắng" đã hết thời [H1];
  - ghế chiavari để trần, chỉ thêm một đai [H12];
  - ghế lưng chéo chỉ cần đai và trâm [H1];
  - ghế xếp ở lễ chỉ trang trí ghế đầu hàng lối đi [H1];
  - màu đai nên trùng một lớp khăn [C1].

**Bảy lớp, từ dưới lên:**

| Lớp | Có gì | Cách làm | Tốn lượt |
|---|---|---|---|
| 1. Khung ghế | chiavari, lưng chéo, ghế xếp, ghế banquet… | vẽ mỗi kiểu đủ 8 góc (T7); màu khung bằng mã | mỗi kiểu 1 tấm |
| 2. Đệm ngồi | màu, chất vải, hoạ tiết | mã (đã thử) | 0 |
| 3. Áo ghế | thun bó, satin, bèo nhiều tầng, chụp đầu ghế | vẽ màu trắng, 8 góc; màu và chất vải bằng mã | mỗi kiểu 1 tấm |
| 4. Đai | dải vải ngang lưng ghế | mã vẽ theo lưng ghế (đã thử) | 0 |
| 5. Nơ, nút, trâm | nơ bướm, nơ hai vòng, hoa hồng vải, trâm | vẽ (T10), 3 góc | 3 tấm (đã tính) |
| 6. Món gắn | hoa, lá, phễu cánh hoa, bảng tên, quạt… | vẽ, 1 góc (sau chéo) | 1 tấm (đã tính) |
| 7. Dây nối các ghế | voan võng, dây đèn, dây lá dọc hàng ghế lối đi | voan và dây đèn bằng mã; dây lá vẽ một đoạn rồi lặp lại | 0 hoặc 1 |

**Đã thử bằng mã, trên cùng bàn tròn:**
- Khung vàng đồng, đen mờ, trắng, gỗ óc chó, và đệm đổi màu theo khăn: đạt. Bản đầu đệm đổi màu không đều (chỉ nhuộm phần sáng, sót hai ghế bên trái); đã sửa bằng cách khoanh tay mặt ngồi từng ghế, lấy cả đường viền đệm, trừ cột và thanh lưng ghế chắn phía trước.
- Đai và nơ vẽ bằng mã trông phẳng như hình dán, không hợp nét vẽ tay. Vì vậy đai trơn làm bằng mã được, còn nơ, nút và trâm phải vẽ (T10).
- Mã: `docs/game/ve/ghe_lop.py`.

**Ý tưởng cho game.** Mình tách rõ cái nào ngoài đời có và cái nào là ý tưởng mới.

Ngoài đời có (theo nguồn):
- đai hai màu chồng nhau, cài trâm hoặc hoa [H8];
- đai voan đan thang chảy thành thác xuống sàn [H2];
- hoa giấy, quả bông trên ghế [H15]; quạt giấy tròn đặt trên ghế (đoạn trích, lượt đầu);
- ghế cặp đôi quấn dây lá; ghế mây lưng công cho cặp đôi (đoạn trích The Knot, lượt đầu).

Ý tưởng cho game, chưa thấy nguồn nói có trong đám cưới:
- áo ghế kiểu áo dài: hai tà vải rủ sau lưng ghế, viền thêu;
- nón lá nhỏ buộc ruy băng ở lưng ghế đầu hàng lối đi;
- búp sen bó buộc lưng ghế lối đi;
- khăn rằn thắt nơ ở lưng ghế cho tiệc miền Tây;
- đèn lồng Hội An nhỏ treo ở đầu hàng ghế;
- con cào cào bằng lá dừa gắn lưng ghế (đan lá dừa là nghề có thật);
- ghế gỗ khảm xà cừ cho ông bà và lễ gia tiên (khảm xà cừ là nghề có thật);
- thẻ tên viết thư pháp treo ở lưng ghế, thay cho thiệp chỗ ngồi;
- gối tựa thêu chữ Hỷ cho ghế cặp đôi và ghế ông bà;
- dây đèn đom đóm quấn lưng ghế cho tiệc tối.

**Thành luật chơi (số tạm):**
- Tiền nhân theo số ghế: áo ghế và nơ cho 300 khách là khoản lớn; chỉ trang trí ghế đầu hàng thì rẻ.
- Ghế ông bà có đệm dày, có tựa lưng: người lớn tuổi vui.
- Màu đai trùng một lớp khăn: được cộng "hài hoà", vì nguồn [C1] khuyên như vậy.

#### Màn cận cảnh bàn (chủ dự án chọn ngày 25/11)

**Để làm gì:** cặp đôi nhìn gần bộ bàn đang chọn (khăn, đĩa, ly, dao nĩa hoặc đũa, khăn ăn, thiệp) và đặt hai phương án cạnh nhau để quyết.

**Khung hình: ba quy tắc để không nhân số tấm**
1. **Một chỗ ngồi ở chính giữa.** Hai chỗ bên cạnh bị mép khung cắt, hoặc mã làm mờ. Trên bàn tròn, chỗ bên cạnh xoay theo tâm bàn. Đĩa và ly đối xứng nên dùng lại được, nhưng dao nĩa, đũa, khăn ăn gấp và thiệp thì không: mỗi chỗ bên cạnh sẽ cần hình mới. Bàn dài không gặp chuyện này (chỗ bên cạnh chỉ dời ngang), nên cận cảnh bàn dài để sau.
2. **Lưng ghế nằm dưới khung hình.** Nếu không, nơ ghế phải vẽ thêm một góc nữa. Muốn thấy ghế trong cận cảnh thì đó là một quyết định riêng, có chi phí riêng.
3. **Hoa bàn ở mép trên, bị cắt hoặc mờ.** Hoa bàn ở mục 3.5 vẽ theo góc của cảnh xa, không khớp góc gần; vẽ lại sẽ gấp đôi số tấm hoa bàn.

**Ngoài đời bày thế nào**
- **Kiểu Âu** (đọc trọn các bài của CV Linens):
  - xếp chồng: đĩa lót, đĩa ăn, rồi đĩa salad hoặc bát súp [D1][D2];
  - đĩa bánh mì và dao bơ ở góc trên bên trái [D2];
  - nĩa bên trái; dao bên phải, lưỡi quay vào đĩa; thìa ở ngoài dao; dùng từ ngoài vào trong; dao nĩa tráng miệng đặt phía trên đĩa [D2][D17];
  - ly nước là ly lớn nhất, đặt trên đầu dao; các ly khác xếp chéo theo thứ tự dùng. Tiệc trang trọng có 3 đến 5 ly, tiệc thường có ly nước và ly vang [D2][D3];
  - khăn ăn đặt trên đĩa (hay gặp ở tiệc cưới), bên trái, hoặc cắm trong ly [D4][D8]; thiệp tên đặt trên khăn ăn hoặc ở mép trên đĩa lót [D1][D4];
  - tiệc kiểu gia đình để trống giữa bàn cho đĩa chung; tiệc buffet mỗi chỗ chỉ có đĩa lót, khăn ăn và ly [D2].
- **Kiểu Việt và Á** (đọc trọn bài của Sapo "Cách set up bàn ăn kiểu Á" ngày 25/11; bài nói về nhà hàng món Á nói chung, không riêng tiệc cưới):
  - bàn tiệc kiểu Á thường là bàn tròn, **có mâm xoay** để khách dễ gắp; lọ muối tiêu, lọ tăm, lọ hoa đặt giữa bàn;
  - đĩa kê bằng sứ, 18–20 cm, đặt chính diện chỗ ngồi, cách mép bàn khoảng 2 cm; đĩa ăn 12–15 cm đặt trên đĩa kê;
  - **bát ăn đặt úp** trên đĩa kê;
  - đũa đặt trên gác đũa ở khoảng ⅓ chiều dài đũa, cách đĩa kê 2 cm, chân đũa cách mép bàn 1–2 cm; thìa đặt trên gác thìa, bên trái đũa, cách 2–3 cm;
  - chén nước chấm đặt trước đĩa kê, cách 1–2 cm; ly ở phía trước bên phải đĩa kê;
  - khăn ăn hoặc giấy ăn gấp cách điệu, đặt trên đĩa ăn hoặc trên miệng cốc nước;
  - mỗi chỗ có đĩa ăn, đĩa lót, đũa và gác đũa, thìa, bát cơm, nước chấm, cốc nước, chén rượu.
  - Bản 3D kiểu Việt đã sửa theo bài này: bát úp, đĩa kê 19 cm, thìa trên gác bên trái đũa, khăn ăn gấp quạt trên miệng cốc.
  - Điện máy Xanh và Brands Vietnam đã được mở mạng, nhưng chính hai trang chặn máy truy cập tự động (ngắt kết nối, lỗi 403); mình không vượt.
- **Mâm xoay:** theo Sapo, bàn tròn kiểu Á thường có mâm xoay. Trong game là một lựa chọn bật tắt (dựng 3D, 0 tấm).
- **Bao đũa in chữ Hỷ hoặc tên khách, dùng thay thiệp chỗ ngồi:** chỉ thấy ở cửa hàng của người Hoa ở nước ngoài, không phải nguồn Việt.

**Danh mục đồ bàn** (A màu, B mặt và hoa văn, C món gắn, D dáng):
- **Đĩa lót:**
  - A: vàng, bạc, champagne, đen, xanh than, đỏ, thuỷ tinh màu trong [D15]; đen mờ, hồng phấn, trong suốt là các màu đang dùng [D6];
  - B: viền hạt (vàng, bạc, đen), viền gợn sóng, viền tia nắng, viền bện, giả mây đan, giả gỗ, dập nổi (ren, baroque), in hoa (toile, mẫu đơn) [D15][D12];
  - D: viền lượn sóng, viền cánh sen, viền cánh hoa, hình nơ [D15][D11]; đĩa vuông đặt trên đĩa lót tròn cũng được chấp nhận [D12];
  - chưa thấy trang đọc được nào nói tới đĩa lót nhung hay đĩa lót gương.
- **Đĩa** (đoạn trích trang cho thuê): sứ trắng, viền chỉ vàng, viền lượn sóng có chỉ vàng, dập nổi hình thoi, gốm đen mờ, đĩa hoa cổ mỗi chỗ một kiểu.
- **Bộ Việt:** chén cơm, chén nước chấm, thìa, đũa (gỗ, inox, nhựa; đũa mạ vàng chỉ thấy trong một tin bán hàng), gác đũa.
- **Ly:**
  - D: ly nước chân cao, ly vang, flute, coupe, ly không chân, chén rượu nhỏ [D3];
  - A: hồng, đỏ, tím nhạt, xanh, ô liu, đen [D3][D15]; hổ phách (đoạn trích);
  - B: ly gợn sóng, ly ép hoa văn kiểu cổ [D15]; ly gân viền vàng (đoạn trích).
- **Dao nĩa:**
  - A: vàng cho sang, bạc cho cổ điển, đen hoặc mờ cho hiện đại [D8]; trộn kim loại ngày càng được chấp nhận [D5];
  - B: cán hai màu vàng đen, cán xà cừ (đoạn trích).
- **Khăn ăn:** 13 kiểu gấp ở phần "Đồ trên bàn" (loại D); cuộn bọc dao nĩa đặt trên đĩa [D14]; thêu chữ cái tên (loại B) [D7].
- **Giấy:** thiệp tên, thực đơn, số bàn, niêm phong sáp, vòng khăn ăn (loại C).

**Xu hướng** (đọc trọn):
- CV Linens 2026: đĩa lót chồng nhiều lớp, khăn ăn thêu chữ cái, thực đơn riêng; bề mặt mờ và ánh nhẹ thay cho kim sa, đá [D7].
- Pinterest Predicts 2026, mục "Opera Aesthetic": ly tách sang trọng, chân nến nhiều nhánh [P3]. Báo cáo cưới 2026 của Pinterest không nêu đồ bàn cụ thể.
- Đoạn trích: đĩa viền lượn sóng; bàn "sưu tầm", mỗi chỗ một kiểu đĩa; ly màu phấn đi với đĩa lượn sóng.

**Vẽ gì:**

| Tấm | Có gì | Loại |
|---|---|---|
| T12. Nền cận cảnh bàn tròn | khăn trắng, mặt bàn trống, vườn mờ phía sau | nền |
| Đĩa lót và đĩa | 6 dáng đĩa lót (trơn, viền hạt, lượn sóng, cánh sen, mây đan, vuông); 4 dáng đĩa (tròn, lượn sóng, vuông, bát súp); tất cả màu sáng | D |
| Ly | ly nước chân cao, ly vang, flute, coupe, ly không chân, ly gân, ly ép hoa văn, chén rượu nhỏ | D, B |
| Dao nĩa và bộ Việt | dao nĩa trơn, dao nĩa mảnh, dao nĩa cán hai màu; đũa, gác đũa, thìa, chén cơm, chén nước chấm | D |
| Khăn ăn gấp, 2 tấm | 12 kiểu: mũ giám mục, quạt, hoa hồng, túi dao nĩa, nút thắt, kim tự tháp, hoa sen, vương miện, cây nến, búp măng, cuộn bọc dao nĩa, gấp phẳng | D |
| Giấy và món nhỏ | thiệp tên, thực đơn, số bàn, bao đũa, niêm phong sáp, vòng khăn ăn, nhánh lá, quà nhỏ | C |
| Nến ở góc gần | nến cây, nến trụ, nến cốc, chân nến | C |

Kế hoạch ban đầu là 8 tấm (16 nếu không vẽ được nhiều món trên một tấm). Ngày 25/11 mình đã tự dựng bằng 3D nền cận cảnh, đĩa lót, đĩa, 4 dáng ly, dao nĩa và bộ Việt; nến và đồ giấy dự kiến dựng 3D tiếp; chỉ còn khăn ăn gấp phải vẽ (khoảng 2 tấm).

**Mã làm, 0 tấm:**
- màu đĩa lót, màu viền đĩa (vàng, bạc, màu);
- hoa văn viền đĩa: mã trải viền hình elip thành một dải thẳng, in hoa văn, rồi cuộn lại;
- màu ly, kim loại dao nĩa, màu và chất vải khăn ăn;
- chữ trên thiệp, thực đơn, bao đũa (tên cặp đôi, tên khách);
- khăn nhiều lớp ở mép bàn (cùng cách trải phẳng); rải cánh hoa, pháo giấy; ánh nến.

**Trong màn chơi, 0 tấm:**
- cảnh xa và cận cảnh dùng chung một bộ lựa chọn; nút "Xem gần";
- so sánh hai phương án đặt cạnh nhau;
- cô dâu và chú rể mỗi người nói một câu khen hay chê theo nhãn của món (ví dụ một người thích bàn "sưu tầm", người kia thích đồng bộ). Hai người cùng thích thì cộng tình cảm; khác ý thì phải chọn nhường ai (số tạm).
- kiểu bày Âu hay Việt là một lựa chọn; cùng một bộ món, mã đổi cách đặt.

### 3.5 Hoa bàn (vẽ, 3 tấm × 6 kiểu)

thấp tròn · cao trong bình thuỷ tinh · nến trụ và bạch đàn · cam quýt và lá · đèn lồng nhỏ và hoa · chân nến đồng hoa rủ · lọ thuỷ tinh nhỏ rải dọc bàn · hoa và trái cây miền Tây · mâm bồng đỏ (truyền thống) · nến nổi trong bát · rêu và đá · hoa giấy thủ công · bình gốm lam · sen trong bát · lồng chim cổ · ngọn hoa cao vút · khay trái cây · đèn dầu cổ

### 3.6 Lối đi (vẽ, 2 tấm × 6 kiểu; thảm và cánh hoa là mã)

chậu hoa · đèn lồng giấy trên chân · nến trong lọ · cột hoa cao · đèn bão · lồng chim · ghế dài phủ hoa · bó cỏ lau · đá cuội và nến · chậu cây cảnh · cọc tre buộc nơ · đèn lồng đỏ trên chân

### 3.7 Treo trên cao (vẽ, 3 tấm × 6 kiểu; dây đèn là mã)

đèn lồng Hội An · đèn lồng đỏ · chùm hoa treo · chùm đèn pha lê · ô giấy · voan rủ · dây cờ đuôi nheo · quạt giấy · chuông gió · nón lá treo · lồng đèn kéo quân · vòng hoa treo · chuỗi hạc giấy (dựng 3D)

### 3.8 Góc phụ và bánh cưới (vẽ, 5 tấm)

| Tấm | Có gì |
|---|---|
| Bánh cưới | 6 kiểu: nhiều tầng trắng, tầng hoa tươi, bánh trần, bánh lệch vui, bánh màu đậm, bánh xu xê kiểu Việt |
| Tháp ly | tháp ly sâm panh trên bàn, chai, khăn |
| Quầy hoa tự cắm | quầy gỗ, xô hoa, kéo, giấy gói |
| Tường hạc giấy | phông chụp ảnh bằng nhiều chuỗi hạc giấy treo dày (dựng 3D, 0 tấm) |
| Góc ảnh hoài cổ | máy ảnh lấy liền trên giá, máy hát đĩa, ghế mây, khung ảnh |
| Bàn đón khách | bảng chào tên cặp đôi (chữ do mã viết), sổ ký tên, hộp mừng |

### 3.9 Bộ phong cách (mã, 0 tấm)

Mỗi bộ chọn sẵn: khung, loài hoa, bố cục, bảng màu, bàn, hoa bàn, lối đi, đồ treo, và gợi ý tiết mục. Người chơi chọn bộ rồi sửa từng món nếu muốn.

| Nhóm | Bộ |
|---|---|
| Theo xu hướng | Ánh xà cừ · Đêm jazz · Nơ và cam quýt · Hoa siêu thực · Nâu mocha · Đồng nội · Hoài cổ analog · Nghìn hạc (hạc giấy trắng hồng treo trên cao, hạc giữ thiệp tên, tường hạc) |
| Kinh điển | Vườn pastel · Tối giản trắng · Mộc boho · Đen vàng art deco · Nhiệt đới · Cổ điển châu Âu |
| Việt Nam | Đỏ son Song Hỷ · Phố đèn lồng · Lá dừa miền Tây · Sen Huế · Đào mai ngày Tết · Cúc hoạ mi đầu đông · Gốm lam · Tre làng |

## 4. Nơi tổ chức cần thêm (vẽ, 16 tấm)

| Nhóm | Nơi | Tấm | Ghi chú |
|---|---|---|---|
| Nền trống ngoài trời | Đồi Thông Sương, Bến Đèn Lồng, Bãi Dừa Xanh, Vườn Sông Quê | 4 | 2 nơi đã có (Vườn Hồ, Sân nhà quê) |
| Trong nhà | Sảnh tiệc có màn LED; sảnh khách sạn chùm đèn; Câu lạc bộ jazz; Nhà kính; rạp cưới quê Bắc Bộ; rạp cưới quê Nam Bộ | 6 | Rạp quê Nam Bộ trùng với đợt 2 của `canh-ngoai-troi.md`, chỉ tính một lần |
| Bản đêm | 6 nơi ngoài trời | 0 (làm bằng mã) | Cần cho pháo hoa và đèn. Ngày 25/11 đã làm bằng mã cho Vườn Hồ và Sân nhà quê (`dem_ma.py`); mỗi nơi mới cần một luật tách trời và toạ độ đèn riêng |

Mỗi nơi mới cần đo một lần: chỗ đứng của cặp đôi, điểm neo của cổng và bàn, chỗ cho người biểu diễn, hệ số chỉnh sáng.

### 4.1 Sức chứa từng nơi (cập nhật 26/11)

Xưởng trang trí cho thấy giới hạn thật là **diện tích nơi tổ chức**, không phải hình vẽ: Vườn Hồ (khoảng 30 × 22 m, ước lượng trên tranh) chỉ đặt được khoảng 26 bàn tròn 10 khách. Muốn 100 bàn (1000 khách) cần khoảng 60 × 45 m. Mỗi nơi vì vậy cần ghi kích thước ước lượng và sức chứa mục tiêu; số khách vượt sức chứa là một quyết định trong ván chơi (đổi nơi, đổi kiểu bàn, bớt khách).

| Nơi | Kích thước ước lượng | Sức chứa mục tiêu | Rủi ro | Phải vẽ | Làm bằng mã, 3D |
|---|---|---|---|---|---|
| Vườn Hồ (đã có) | 30 × 22 m | khoảng 26 bàn tròn 10 | nắng gắt, mưa | — | bàn, ghế, khăn, hoa bàn, đèn, màn LED, loa (đã làm) |
| **Vườn Hồ nới rộng** (T16, chủ dự án chọn 26/11) | khoảng 60 × 45 m | 100 bàn tròn 10 | như Vườn Hồ | 1 nền ngày nhìn từ trên cao hơn (thềm biệt thự, chếch xuống 25–30°) | **dựng lại bàn ghế 3D ở góc chếch mới** bằng các tệp dựng sẵn (0 lượt); bản đêm bằng mã như Vườn Hồ |
| Sân nhà quê (đã có) | 24 × 18 m | khoảng 12 bàn tròn 10 | mưa | — | như Vườn Hồ |
| **Nhà kính** (ảnh tham khảo 26/11, xem 4.2) | khoảng 18 × 40 m | lễ 150–200 ghế; tiệc khoảng 25 bàn | không mưa; mái kính nóng giữa trưa (thành rủi ro "nóng", xử lý bằng giờ tiệc hoặc quạt) | 1 nền ngày; bản tối vẽ riêng hoặc làm bằng mã quầng sáng quanh đèn chùm (không dùng cách tách trời của nơi ngoài trời vì đèn chùm là nguồn sáng, trời đêm chỉ lộ qua ô kính) | bàn, ghế, khăn, hoa bàn, loa; đèn chùm là một phần của tranh |
| Sảnh khách sạn chùm đèn | khoảng 25 × 35 m | 40–50 bàn | không mưa; điện, âm thanh có sẵn của sảnh | 1 nền + bản tối | như trên |
| Sảnh tiệc có màn LED (trung tâm tiệc cưới) | khoảng 30 × 50 m | 60–100 bàn: chỗ cho tiệc rất đông trong nhà | không mưa; giờ tiệc theo ca của sảnh | 1 nền; màn LED sân khấu dùng lại mã màn LED | như trên |
| Rạp cưới quê Bắc Bộ, Nam Bộ | theo rạp, khoảng 10 × 30 m | 20–30 bàn | gió làm rạp rung; nóng | 1 nền mỗi rạp | như trên |

Mọi nơi mới (trừ T16) vẽ **cùng góc máy với Vườn Hồ** (ngang tầm mắt, chếch khoảng 15°) để dùng lại toàn bộ bàn ghế 3D; mỗi nơi đo phối cảnh một lần bằng lưới 1 m như Vườn Hồ.

### 4.2 Nhà kính: những gì thấy trong ảnh tham khảo (26/11)

Chủ dự án gửi một ảnh lễ cưới trong nhà kính. Game chỉ lấy ý, không chép ảnh hay tên nơi đó.

- **Không gian:** mái vòm kính khung sắt sơn màu xám xanh cong xuống hai bên; tường và cột đá xám; ba ô cửa vòm kính rất cao ở cuối phòng nhìn ra vườn kiểu Pháp có đài phun nước và hàng cây; sàn đá ô lớn.
- **Ánh sáng:** nắng xuyên mái kính đổ thành ô sáng trên sàn; nhiều chùm đèn pha lê treo dọc giữa phòng; đèn tường chao vải dọc tường đá.
- **Trang trí:** rèm voan trắng buộc hai bên mỗi cửa vòm; cổng hoa trắng, xanh đặt trước cửa vòm giữa; ghế dự lễ xếp thành hai khối có lối giữa.
- **Ghế:** ghế gỗ lưng thanh tiện, mỗi ghế có một dải voan trắng xếp nếp vắt qua đỉnh lưng, thắt túm giữa lưng rồi rủ đuôi xuống sàn. Đây là lớp "đai" và "nơ" trong [Trang trí ghế theo lớp](#trang-trí-ghế-theo-lớp): dải voan xếp nếp vẽ bằng mã theo lưng ghế 3D, phần túm có thể dùng nút nơ của T10.
- **Cho ván chơi:** nơi trong nhà bỏ rủi ro mưa nhưng thêm rủi ro nóng dưới mái kính; ánh nắng qua mái là một hiệu ứng mã rẻ (dải sáng chéo trên sàn) và cũng là lý do chọn giờ tiệc chiều muộn.

## 5. Hiệu ứng sân khấu (gần như toàn bộ là mã, 0 tấm)

| Hiệu ứng | Cách làm | Cần | Luật chơi gợi ý (số tạm) |
|---|---|---|---|
| Pháo hoa | Mã, theo cách của trang chủ; chép sang `game/`, không sửa `fireworks.js` của website | Ngoài trời, bản đêm | Nơi tổ chức phải cho phép; gió mạnh thì hoãn; tốn tiền; khách vui |
| Pháo giấy, pháo kim tuyến | Mã (hạt rơi) | — | Rẻ; vui với bạn bè; tốn công dọn |
| Pháo lạnh | Mã (tia sáng phun từ hai bên lối đi) | — | Hợp lúc cặp đôi bước vào, cắt bánh |
| Khói sàn | Mã (lớp sương sát đất) | Trong nhà hoặc đêm | Hợp điệu nhảy đầu tiên |
| Bong bóng xà phòng | Mã | Ngoài trời, ít gió | Trẻ con thích |
| Cánh hoa rơi | Đã có ở màn tổng kết | — | — |
| Dây đèn, đèn đom đóm | Mã (điểm sáng nhấp nháy) | Đêm hoặc trong nhà | — |
| Đèn sân khấu, đèn đuổi | Mã (vệt sáng màu) | Trong nhà | — |
| Nội dung màn LED | Mã: ảnh album, tên cặp đôi, chữ chạy, pháo hoa ảo | Sảnh tiệc có màn LED | Cá nhân hoá, đúng xu hướng ở Việt Nam |
| Chữ neon tên cặp đôi | Mã (chữ phát sáng) | Tường hoa, trong nhà | — |
| Hoa đăng trôi sông | Mã | Bến Đèn Lồng, Vườn Sông Quê | — |
| Máy phun pháo lạnh, ống pháo giấy | Vẽ chung một tấm với góc phụ, nếu cần | — | — |

Mọi hiệu ứng tắt khi người chơi bật giảm chuyển động (biến `giamDong` đã có) và chỉ chạy vài giây, như pháo hoa của trang chủ. Game không nêu quy định pháp luật về pháo; chỉ coi đó là rủi ro, chi phí và sự cho phép của nơi tổ chức.

## 6. Tiết mục (vẽ, khoảng 34 tấm)

Mỗi tiết mục là hình người biểu diễn rời trên nền xanh dương, **luôn kèm hình ban nhạc hoặc MC hiện có làm mẫu nét** (quy tắc 7). Nhóm đông vẽ tối đa 4–5 người một tấm. Tiết mục đi vào **dòng thời gian chương trình** đã có trong `spec.md` mục 4: mỗi tiết mục có giá, thời lượng, nhóm khách thích (lớn tuổi, bạn bè, đồng nghiệp, trẻ con) và rủi ro.

### 6.1 Âm nhạc (11 tiết mục, 12 tấm)

| Tiết mục | Người | Hợp nơi | Khách thích |
|---|---|---|---|
| Tứ tấu đàn dây | 4 | mọi nơi | lớn tuổi, đồng nghiệp |
| Dàn nhạc thính phòng nhỏ | 8, vẽ 2 tấm | sảnh lớn | lớn tuổi |
| Piano cánh | 1 + đàn | trong nhà | mọi nhóm |
| Đàn hạc | 1 | mọi nơi | lớn tuổi |
| Saxophone | 1 | mọi nơi | bạn bè, đồng nghiệp |
| Ban nhạc jazz | 3 | Câu lạc bộ jazz, đêm | bạn bè |
| Ca sĩ hát sống | 1 | mọi nơi | mọi nhóm |
| DJ | 1 + bàn đĩa | đêm, trong nhà | bạn bè |
| Nhạc dân tộc: đàn tranh, đàn bầu, sáo | 3 | mọi nơi | lớn tuổi |
| Quan họ | 4 | Bắc Bộ | lớn tuổi |
| Đờn ca tài tử | 3 | Nam Bộ | lớn tuổi |

### 6.2 Múa và nhảy (9 tiết mục, 10 tấm)

| Tiết mục | Người | Hợp nơi | Rủi ro, ghi chú |
|---|---|---|---|
| Vũ công ballet | 1, 2 tư thế | trong nhà | — |
| Đôi nhảy waltz chuyên nghiệp | 2 | mọi nơi | — |
| Đôi nhảy tango, latin | 2 | đêm, trong nhà | lớn tuổi có thể ngại |
| Múa áo dài, múa quạt | 4 | mọi nơi | — |
| Múa lân | 3 (lân, ông Địa, trống) | ngoài trời | ồn; trẻ con thích |
| Nhảy hiện đại của bạn bè | 5 | mọi nơi | bạn bè thích |
| Múa lụa trên không | 1 + khung treo | trần cao, Nhà kính | cần khung an toàn |
| Múa lửa | 2 | biển, đêm | gió mạnh thì huỷ |
| Múa sạp | 4 | ngoài trời | khách được nhảy cùng |

### 6.3 Xiếc và ảo thuật (6 tiết mục, 6 tấm)

ảo thuật sân khấu · ảo thuật tại bàn · tung hứng · đi cà kheo · bong bóng khổng lồ (ngoài trời, ít gió) · nhào lộn

### 6.4 Nghệ nhân và tương tác (6 tiết mục, 6 tấm)

hoạ sĩ vẽ trực tiếp cảnh tiệc · ông đồ cho chữ · nặn tò he · vẽ chân dung biếm hoạ · bartender biểu diễn · xe kem, xe cà phê, gánh hàng rong (một tấm 3 xe)

### 6.5 Đã có, giữ nguyên

MC, ban nhạc mộc, thợ ảnh (bản chơi hiện nay). MC 4 bộ và ban nhạc 3 bộ đã duyệt, chờ vẽ.

### 6.6 Điệu nhảy của chính cặp đôi (để riêng)

Waltz hay điệu nhảy đầu tiên của cô dâu chú rể không phải hình người biểu diễn. Nó cần thân nhân vật ở tư thế nhảy, cho mọi vóc người và mọi bộ trang phục, nên tốn rất nhiều tấm. Trước mắt: cặp đôi đứng giữa, mã làm khói sàn, đèn đuổi và cánh hoa. Tư thế nhảy để sau khi tóc và trang phục đã vẽ xong.

## 7. Hạn mức trên một trang

**Giới hạn mới (chủ dự án đặt ngày 25/11): game chỉ dùng tối đa 40% gói Model Studio mỗi tháng**, phần còn lại để việc khác. Mỗi hình khoảng 0,24% gói (đo ngày 24/11), nên trần là **khoảng 166 hình mỗi tháng**, kể cả lượt sửa; video tính quy đổi (1 clip 5 giây ≈ 23 hình). `docs/game/ve/gen.py` tự đếm vào sổ `so-luot.json` và từ chối lô nào làm vượt trần, trước khi gọi.

Vì vậy kế hoạch dưới đây (khoảng 355 hình nếu thử đạt) không còn vừa một tháng, mà chia ra ba tháng (bảng "Chia theo tháng" ở cuối mục). Bảng ngay dưới là tổng khối lượng, chưa chia tháng. Mọi con số là ước lượng.

| Việc | Trạng thái | Nếu thử đạt | Nếu thử không đạt |
|---|---|---|---|
| Lông mày cô dâu | đã duyệt | 9 | 9 |
| Tóc (30 kiểu × 3 dáng mặt) | đã duyệt | 90 | 90 |
| Trang phục (9 bộ vẽ × 3 vóc; màu thêm bằng mã, mục 7b) | đã duyệt, đề xuất bớt | 27 | 27 |
| MC, ban nhạc (4 bộ vẽ; màu thêm bằng mã) | đã duyệt, đề xuất bớt | 4 | 4 |
| Cảnh C1–C17, C20 và nhân vật phụ | chờ duyệt | khoảng 50 | khoảng 50 |
| Nơi đợt 2 (trừ rạp quê Nam Bộ) | chờ duyệt | 7 | 7 |
| **Bảng này:** nơi tổ chức; 6 bản đêm làm bằng mã (đã làm 2, dự kiến 4) | chờ duyệt | 10 | 10 |
| **Bảng này:** khung cổng (6 khung đơn giản làm bằng mã, đã làm) | chờ duyệt | 14 | 20 (vẽ kèm hoa) |
| **Bảng này:** loài hoa | chờ duyệt | 17 | 0 (hoa vẽ liền vào khung) |
| **Bảng này:** bàn ghế (mục 3.4): đã dựng 3D bàn tròn, bàn dài, ghế chiavari (4 trên 9 tấm); dự kiến bàn vuông, bàn đứng, ghế lưng chéo, ghế trong suốt (ghế trong suốt có nét viền chưa chắc đẹp) | chờ duyệt | 1 (ghế bọc vải có nơ) | 1 |
| **Bảng này:** hoa bàn, lối đi, đồ treo, góc phụ | chờ duyệt | 13 | khoảng 52 (mỗi món một tấm) |
| **Bảng này:** khăn, áo ghế, nơ ghế, món gắn ghế, nến và giấy (cuối mục 3.4); khăn phủ, chạy bàn bằng mã; váy quây, áo ghế thun dự kiến dựng 3D | chờ duyệt | 6 | khoảng 14 |
| **Bảng này:** màn cận cảnh bàn: nền, đĩa, ly, dao nĩa, bộ Việt đã dựng 3D; còn khăn ăn gấp | chờ duyệt | 2 | khoảng 4 |
| **Bảng này:** tiết mục | chờ duyệt | 34 | 34 |
| Cộng | | khoảng 284 | khoảng 322 |
| Dự phòng sửa 25% (quy tắc 4) | | khoảng 71 | khoảng 81 |
| **Tổng, tính cả phần dự kiến tự vẽ** | | **khoảng 355** | **khoảng 403** |
| Tổng nếu chỉ tính phần đã làm xong ngày 25/11 | | khoảng 370 | khoảng 424 |
| Cách phối cổng | | khoảng 13.000 | khoảng 320 |

Cập nhật ngày 25/11, sau khi tự vẽ (mã và 3D):
- **Chỉ tính phần đã làm xong** (6 khung, 2 bản đêm, bàn tròn, bàn dài, ghế chiavari, cận cảnh): thử đạt thì dư khoảng 46 tấm; thử không đạt thì thiếu khoảng 8 tấm.
- **Tính cả phần dự kiến tự vẽ tiếp** (4 bản đêm, bàn vuông, bàn đứng, 2 kiểu ghế, váy quây, áo ghế thun, nến, đồ giấy): dư khoảng 61 tấm, hoặc 13 nếu thử không đạt.
- Các con số giả định chủ dự án chấp nhận nét của đồ tự vẽ.

**Chia theo tháng, trần 166 hình mỗi tháng (đã gồm 25% dự phòng sửa):**

Phương án A, trang trí trước (**chủ dự án chọn ngày 26/11**): trang trí đang dựng dở ở chương 4, và phần lớn bàn ghế, cận cảnh đã tự vẽ xong nên tháng 12 còn dư chỗ.

| Tháng | Việc | Hình (thử đạt) | Kể cả 25% sửa |
|---|---|---|---|
| 12 | Tấm thử T2, T3, T4, T5, T10, T11 (là món đầu của các dòng bên dưới); lông mày 9; nơi tổ chức 10; khung cổng 14; loài hoa 17; bàn ghế 1; hoa bàn, lối đi, đồ treo, góc phụ 13; khăn và trang trí ghế 6; cận cảnh 2; MC, ban nhạc 4; tiết mục 34 | 110 | khoảng 138 (dư khoảng 28) |
| 1 | Tóc 90; trang phục 27 | 117 | khoảng 146 (dư khoảng 20) |
| 2 | Cảnh C1–C17, C20 và nhân vật phụ khoảng 50; nơi đợt 2: 7 | 57 | khoảng 71 |

Nếu các bài thử "nhiều món trên một tấm" không đạt, tháng 12 lên khoảng 148 hình (185 kể cả sửa), vượt trần: dời khoảng 20 tiết mục sang tháng 2.

**Nếu T14 đạt (vẽ hoa và đồ trang trí mềm bằng Canva, mục 7c):** khoảng 36 hình của tháng 12 chuyển sang Canva (45 kể cả sửa, trong 100 hình Canva). Phần Model Studio tháng 12 còn khoảng 74 hình (93 kể cả sửa), dư khoảng 73 hình dưới trần 166: có thể bắt đầu tóc ngay trong tháng 12, để tháng 1 xong tóc và trang phục sớm hơn.

Phương án B, nhân vật trước: tháng 12 là lông mày 9, tóc 90, trang phục 27, MC và ban nhạc 4 = 130 hình (khoảng 163 kể cả sửa, sát trần 166, gần như không dư). Tháng 1 là trang trí và tiết mục (106 hình, khoảng 133). Tháng 2 là cảnh (57 hình).

Mỗi nhóm vẫn vẽ thử một tấm trước khi chạy cả lô (quy tắc 3).

## 7b. Cách tiết kiệm gói

Nguyên tắc chung: **mã làm được thì không vẽ** (quy tắc 5). Vẽ mỗi món ở **màu sáng, trung tính**, vì từ màu sáng mã nhuộm ra màu đậm rất đẹp, còn từ màu đậm nhuộm ra màu sáng thì xấu.

**Đã thử bằng mã ngày 25/11** trên bàn dài và cổng tròn đã có:
- khăn ra 8 màu, trong đó có xanh than, mù tạt, tím, đen;
- gỗ ra óc chó, sơn trắng, sơn đen;
- khung cổng ra bạc, đen mờ, vàng hồng.

Kết quả tốt. Còn một lỗi: khung đen làm nhuỵ hoa gần khung bị lấm tấm; sửa được bằng cách giới hạn mặt nạ theo hình vòng. Màu không bị giới hạn ở danh sách: game có thể cho người chơi tự chọn màu bất kỳ.

| Cách | Đã thử? | Bớt được (tấm) | Ghi chú |
|---|---|---|---|
| Đổi màu khăn, hoa, gỗ, sơn, kim loại bằng mặt nạ | đã thử | đã tính trong bảng | mỗi món một tấm vẽ là đủ mọi màu |
| Hoạ tiết và chất vải bằng mã: ca rô, sọc, hoa in, ren, kim sa, nhung, nhuộm loang… | đã thử trên khăn chạy bàn | đã tính trong bảng | mỗi mặt vải 0 tấm. Áo ghế, nơ, khăn ăn vẽ màu trắng thì phủ được màu và chất vải không theo hướng (kim sa, nhung). Hoạ tiết in phải đo toạ độ vải cho từng dáng, từng góc |
| Trang phục vẽ màu sáng rồi nhuộm: vest đen và vest be thành 1 bộ; áo dài chú rể đỏ và trắng thành 1; áo dài cô dâu trắng và hồng thành 1 | cần thử 1 bộ | 9 (đã trừ ở mục 7) | còn có thêm vest xanh than, áo dài vàng… không tốn lượt. Hoạ tiết thêu đổi màu theo vải |
| MC và ban nhạc: 4 bộ vẽ, màu thêm bằng mã | cần thử | 3 (đã trừ) | — |
| Ghế: 4 kiểu vẽ, màu gỗ và kim loại bằng mã | đã thử trên ghế của bàn dài | 2 (đã trừ) | — |
| Nhiều món trên một tấm | thử ở T2, T3, T7, T8 | khoảng 40 | khác biệt giữa hai cột của mục 7 |
| Bàn dài nối từ mô-đun, ghế rời quanh bàn | thử ở T7, T8, T9 | — | một bộ hình cho mọi cỡ bàn |
| Bản đêm bằng mã: tô tối nền trống, thêm đèn và trời sao | đã làm 25/11: Vườn Hồ, Sân nhà quê (`dem_ma.py`) | 6 (đã trừ ở mục 7) | không xê dịch cảnh; mây giữ khối, sao, đèn lan can, đèn cổng, cửa sổ sáng, đèn làng xa có vệt phản chiếu |
| Khung đơn giản vẽ bằng mã: vòm cong, tròn, lục giác, tam giác, vòm nhọn, khung chữ nhật gỗ (màu gỗ, đen, trắng, vàng đồng đổi bằng mã) | đã làm 25/11 (`khung_ma.py`) | 6 (đã trừ) | ống có viền mực, vệt sáng, vệt tối, nét hơi rung, vân giấy. Khung tre, sắt rèn, gỗ trôi dạt vẫn vẽ |
| Bàn, ghế, đồ bàn dựng 3D rồi vẽ nét mực (Blender trên máy làm việc, không cần card đồ hoạ) | đã làm 25/11: ghế chiavari 8 góc; bàn tròn 6, 10, 12 khách có ghế; bàn dài 8, 12, 20 khách, ngang và chéo; cận cảnh kiểu Âu và kiểu Việt | khoảng 17 (đã trừ) | mỗi bộ có sẵn mặt nạ (khăn, đệm, khung, đĩa…) và ảnh toạ độ khăn, nên khăn nhiều lớp và đổi màu chạy thẳng, không khoanh tay. Vẽ thẳng mọi độ dài bàn, không cần ghép mô-đun. Nét đều và sạch hơn tranh vẽ tay |
| Lấy món từ 18 tranh cũ bằng cách trừ nền trống: chậu hoa, dây đèn, đèn lồng, cổng lá dừa, cổng rạp đỏ | chưa thử, 0 lượt | khoảng 3 | mép có thể cần sửa tay |
| Cảnh dùng chung phòng: một phòng khách cho C4, C7, C20; một bàn thờ cho C15, C17; đồ đạc là lớp rời | chưa thử | khoảng 6 | như trang trí theo lớp |
| Lật gương, chỉnh sáng theo cảnh, dùng lại món ở mọi nơi | đã thử | — | đang dùng |

### 7c. Dùng model vẽ khác (chủ dự án cho phép ngày 25/11)

Chủ dự án cho dùng model khác, miễn nét vẽ vẫn đẹp. Hiện có hai đường:

- **Canva** (đã nối với phiên làm việc): tạo hình từ chữ, hoặc vẽ lại theo hình mẫu tải lên. Không tính vào trần 40% của Model Studio. **Chủ dự án cho dùng 100 hình Canva** (26/11); sổ đếm ở `so-luot.json`, mục `canva`.
  - **T3 đã vẽ ngày 26/11 (1 hình Canva):** đủ 6 món (hoa thấp tròn, bình hoa cao, nến trong chụp kính với bạch đàn, hoa và cam trong âu đồng, đèn lồng đồng, chân nến đồng 5 ngọn), cùng góc nhìn. Chỗ nhìn xuyên kính (bình, chụp nến) còn ngả xanh nền nên mã làm gần trong suốt và trung tính; thân nến, đáy bình và đèn lồng không nhuộm theo tông hoa. Trang thử đặt hoa lên giữa mọi bàn tròn, cứ 1,5 m một món dọc bàn dài (cả bàn xếp chéo, bàn vẽ tay, bàn dài xuyên suốt theo phối cảnh), đúng cỡ thật (0,34–0,6 m bề ngang), nhuộm theo tông hoa của cổng; bảng kê đếm số món. Cận cảnh chưa có hoa bàn (giữa bàn nằm ngoài khung).
  - **T15 đã vẽ ngày 26/11 (1 hình Canva):** 6 khóm hồng trắng, cẩm tú cầu, baby, lá bạch đàn trên nền xanh (nền đậm hơn T14 nên `trang_tri.tach` nhận thêm ngưỡng `nguong`). Mặt nạ hoa trắng cũ (`mat_na_hoa`) bắt đúng cánh và hoa baby, bỏ lá. Trang thử xếp khóm cách nhau 0,42 m, rộng 0,65 m, chọn khóm và lật gương theo vị trí, nên thành một luống liền hai bên lối (lối đá, thảm, lối gương), nhuộm theo tông hoa của cổng.
  - **T14 đã vẽ ngày 26/11 (1 hình Canva):** 4 cụm mẫu đơn rời trên nền xanh phẳng, lấy cổng tròn vẽ tay làm mẫu. Tách nền sạch bằng `trang_tri.tach`; gắn lên khung lục giác vẽ bằng mã ở góc trên, dọc cạnh phải và ở chân thì trông như cắm thật. Ở cỡ cảnh, nét gần với cổng tròn vẽ tay; nhìn gần thì hoa Canva đậm màu và chi tiết hơn, ít nét viền hơn. Chờ chủ dự án xem.
  - Nếu đạt: loài hoa (17), hoa bàn, lối đi, đồ treo, góc phụ (13), món gắn ghế và nơ (4), khăn ăn gấp (2) chuyển sang Canva, khoảng 36 hình (45 kể cả sửa). Đồng thời coi như đã thử được ý "khung trần + cụm hoa rời", nên T2 không cần vẽ nữa.
  - Cách lấy ảnh đủ cỡ: công cụ chỉ trả ảnh xem trước 200 điểm ảnh, nên phải đặt hình vào một trang Canva rồi xuất PNG (ảnh gốc 1680×944). Mạng đã mở cho `www.canva.com`, `media.canva.com`, `export-download.canva.com`.
- **Model khác trong Model Studio** (bản rẻ hơn, nếu có trong gói): vẫn tính vào trần 40%, chỉ có lợi nếu mỗi hình tốn ít hơn 0,24% gói. Cần đo trên trang quản lý gói sau một hình thử.
- **Không dùng** dịch vụ trả tiền theo lượt gọi khi chưa được chủ dự án đồng ý.

Hình vẽ bằng model khác vẫn theo đủ quy tắc ở `canh-ngoai-troi.md` mục 4: duyệt bảng trước, vẽ thử một tấm, sửa trên hình đã đạt.

## 8. Đợt 0: tấm thử, chuyển sang tháng 12

**Chủ dự án quyết ngày 25/11: tháng 11 không chạy đợt nào; món nào mình tự vẽ được (mã, 3D) thì tự vẽ.** Đợt 0 và Đợt 8b chuyển sang đầu tháng 12. Các tấm thử đều là món đầu tiên của những dòng đã tính ở mục 7, nên dời sang tháng 12 không làm tăng tổng; 3 lượt sửa nằm trong phần dự phòng. T1, T6, T7 mặc định dùng bản tự vẽ (chủ dự án vẫn xem từng kết quả, chưa phải duyệt phong cách). Mỗi tấm vẽ trên nền xanh dương phẳng, trừ T5 và T6 là cảnh.

| Tấm | Ai hoặc vật gì | Tư thế, trang phục | Có gì | Không có gì | Sửa từ hình nào | Đạt khi |
|---|---|---|---|---|---|---|
| T1. Khung lục giác trần (có thể thay bằng mã, đã thử 25/11) | khung cổng | đứng thẳng, nhìn chính diện | khung lục giác kim loại đen mờ, chân đế phẳng | hoa, lá, vải, người, đất | `cong-tron.png` (giữ nét vẽ, góc nhìn, nền xanh) | tách nền sạch dù khung mảnh; không méo |
| T2. Cụm mẫu đơn | 4 cụm hoa rời | — | cụm góc lớn, dải rủ dài, cụm nhỏ tròn, cụm chân đế; mẫu đơn hồng nhạt, lá bạch đàn; các cụm cách xa nhau | khung, cuống lơ thơ, người | `cong-tron.png` (thay cổng bằng 4 cụm hoa) | mã cắt được 4 cụm; gắn lên khung T1 và khung tròn trông như cắm thật; nhuộm được tông |
| T3. Hoa bàn 6 kiểu (đổi sang Canva ngày 26/11 sau khi T14 đạt; chủ dự án hỏi đồ trang trí trên bàn; đã vẽ 26/11, 1 hình; chờ chủ dự án xem) | 6 món, lưới 3 × 2 | góc nhìn hơi cao như bàn tiệc | thấp tròn, cao trong bình, nến và bạch đàn, cam quýt và lá, đèn lồng nhỏ, chân nến đồng; hoa màu **trắng** để mặt nạ đổi tông; nền xanh dương phẳng | bàn, khăn, người | `cong-tron.png` trên Canva làm mẫu nét (như T14, T15) | mã cắt được ít nhất 5/6 món; cùng góc nhìn; đặt lên bàn tròn, bàn dài và bàn dài xuyên suốt đúng cỡ |
| T4. Tứ tấu đàn dây | 4 nhạc công: 2 violin, 1 viola, 1 cello; 2 nam, 2 nữ | ngồi ghế, đang chơi; nam vest đen, nữ đầm đen dài | 4 ghế, 4 cây đàn, giá nhạc | đất, người khác | một tấm mẫu ghép sẵn bằng mã: ban nhạc (`ban-nhac-b.webp`) và cặp đôi đặt trên nền xanh dương phẳng (công cụ vẽ chỉ nhận một hình mẫu, và hình có nền trong suốt sẽ hiện nền đen) | nét giống ban nhạc và cặp đôi; tay cầm đàn đúng; tách nền sạch; đặt vào Vườn Hồ đúng cỡ |
| T5. Sảnh tiệc có màn LED | nền trống trong nhà | — | sảnh tiệc, lối đi giữa, sân khấu thấp phía sau, màn LED lớn **đen trơn**, chùm đèn pha lê, sàn bóng | bàn ghế, người, hoa | `nen-ho.png` (giữ góc máy và vị trí lối đi) | lối đi và đường chân trời gần như cũ để dùng chung thước phối cảnh; màn LED là hình chữ nhật sạch, mã đo được 4 góc |
| T6. Vườn Hồ ban đêm (có thể thay bằng mã, đã thử 25/11) | nền trống, đêm | — | trời xanh thẫm có sao, đèn lan can sáng ấm, mặt hồ phản chiếu | trăng to, người, đồ trang trí | `nen-ho.png` | cảnh xê dịch không quá 1%; trời đủ tối cho pháo hoa bằng mã; đo được hệ số chỉnh sáng cho món rời |
| T7. Ghế chiavari 8 góc nhìn (có thể thay bằng 3D, đã thử 25/11) | 8 chiếc ghế cùng kiểu, lưới 4 × 2, cách xa nhau | trước, sau, trái, phải, bốn góc chéo; cùng cỡ; góc nhìn hơi cao như bàn tiệc | ghế chiavari trắng, đệm kem | bàn, người, đất | `ban-dai.png` (thay bộ bàn bằng 8 chiếc ghế) | mã cắt được 8 ghế; đặt quanh bàn T8 trông như thật, ghế sau bị bàn che đúng thứ tự |
| T8. Bàn tròn trần 3 cỡ (đã tự vẽ bằng 3D, 25/11) | 3 bàn tròn: 6, 10, 12 người | góc nhìn hơi cao | khăn trắng phủ chấm đất | ghế, hoa, đồ ăn, người | `ban-dai.png` | mã cắt được 3 bàn; mặt bàn đúng góc nhìn; tỉ lệ cỡ giữa ba bàn hợp lý; ghép với ghế T7 ra bàn 6, 10, 12 người |
| T9. Bàn dài mô-đun chạy ngang (đổi ngày 25/11, đã duyệt; đã tự vẽ bằng 3D, không cần mô-đun) | 3 mảnh: đầu trái, đoạn giữa, đầu phải | nhìn chính diện, hơi cao; bàn chạy ngang khung hình | khăn trắng phủ chấm đất, mặt bàn trống; bát đĩa, ly đặt cách xa mép khăn | ghế, khăn chạy bàn, hoa, người, đất | `ban-dai.png` | mã nối thành bàn 8, 20, 40 người không lộ mối nối; mã phủ được khăn phủ, khăn chạy bàn và đổi màu, hoạ tiết khăn nền |

**Sau khi tự vẽ (25/11):** T1, T6, T7, T8, T9 đã có bản tự vẽ; Đợt 0 tháng 12 còn 4 tấm cần công cụ vẽ: T2 (cụm hoa, gắn lên khung lục giác vẽ bằng mã), T3, T4, T5, và 3 lượt sửa, tối đa 7 tấm.

**Thứ tự:** T1 rồi T2 (cặp này quyết định có 13.000 hay 320 cách phối cổng), rồi T7, T8, T9 (quyết định bàn ghế có lắp tự do được không), sau đó T3, T4, T5, T6. Tấm nào không đạt thì sửa từng chỗ trên chính tấm đó, tối đa 3 lượt sửa cho cả đợt.

## 8b. Đợt thử đầu tháng 12: T10–T13 (chủ dự án duyệt ngày 25/11; T12, T13 thử tự vẽ bằng 3D trước)

Bốn tấm thử cho ghế và màn cận cảnh, chạy đầu tháng 12, trước các lô vẽ thật. T12, T13 đã tự vẽ bằng 3D (25/11), nên đợt này còn T10, T11. Tối đa 6 tấm (4 tấm và 2 lượt sửa), lấy từ phần dự phòng sửa của tháng 12. Các tấm này thử những món đã tính trong mục 7, nên không cộng thêm.

| Tấm | Ai hoặc vật gì | Tư thế, trang phục | Có gì | Không có gì | Sửa từ hình nào | Đạt khi |
|---|---|---|---|---|---|---|
| T10. Nơ ghế 8 kiểu | 8 chiếc nơ rời, lưới 4 × 2, cách xa nhau; chỉ gồm nút nơ và đuôi, dải vải quấn lưng ghế do mã vẽ | nhìn từ sau, góc hơi cao như bàn tiệc | nơ satin trắng: nơ bướm, nút đơn, hoa hồng, rủ dọc, bắt chéo, đai có khoá cài, nơ đuôi dài, nơ to | ghế, người, đất | `ban-dai.png` (giữ nét vẽ) | mã cắt được 8 nơ; gắn lên lưng ghế T7 nhìn từ sau trông như buộc thật; nhuộm được màu, đổi được chất (satin, voan, nhung) |
| T11. Món gắn ghế lối đi 8 món | 8 món rời, lưới 4 × 2, cách xa nhau | nhìn từ sau chéo, góc hơi cao | cụm hoa, bó lá bạch đàn buộc ruy băng, phễu giấy đựng cánh hoa, vòng hoa tròn, quạt giấy tròn, bảng tên gỗ (để trống chữ), nón lá nhỏ buộc ruy băng, bó búp sen; màu sáng | ghế, chữ, người, đất | `ban-dai.png` (giữ nét vẽ) | mã cắt được 8 món; gắn lên lưng ghế T7 góc sau chéo trông như buộc thật; nhuộm được ruy băng và hoa |
| T12. Cận cảnh bàn tròn, mặt bàn trống (đã tự vẽ bằng 3D, 25/11) | nền cho màn cận cảnh | người đứng ngay sau ghế nhìn xuống chừng 40°; một chỗ ngồi ở chính giữa khung, mép bàn cong chạy ngang phía dưới; chỗ ngồi hai bên bị mép khung cắt; giữa bàn ở mép trên, mờ | khăn trắng phủ, mặt bàn trống, nếp khăn rủ ở mép trước; vườn mờ phía sau | ghế (lưng ghế nằm dưới khung hình), đĩa, ly, hoa, người | tranh gốc 2736×1520 của cảnh gọn (giữ nét vẽ, khăn trắng, ánh sáng) | mép bàn là đường cong sạch, đo được; mặt khăn phẳng đủ để đặt đồ; nền mờ không lấn vào bàn |
| T13. Bộ đồ bàn thử ở góc cận (đã tự vẽ bằng 3D, 25/11) | 6 món rời, lưới 3 × 2, cách xa nhau | đúng góc nhìn của T12 | đĩa lót viền hạt, đĩa sứ trắng, ly chân cao, ly flute, bộ dao nĩa, khăn ăn gấp hình quạt; tất cả màu sáng | bàn, khăn, người | T12 (giữ góc nhìn, thay bàn bằng nền xanh dương phẳng) | mã cắt được 6 món; đặt lên T12 đúng cỡ, đúng góc; nhuộm được viền đĩa, màu ly, kim loại |
| T14. Thử Canva vẽ cụm hoa (đã duyệt, đã vẽ 26/11, chờ chủ dự án xem) | 4 cụm mẫu đơn rời như T2 | — | cụm góc lớn, dải rủ dài, cụm nhỏ tròn, cụm chân đế; mẫu đơn hồng nhạt, lá bạch đàn; nền xanh dương phẳng | khung, người | tải `cong-tron.png` (cổng tròn vẽ tay) lên Canva làm hình mẫu nét vẽ | nét, màu, ánh sáng giống cổng tròn vẽ tay khi đặt cạnh nhau ở cỡ cảnh; tách nền sạch; gắn được lên khung lục giác vẽ bằng mã. Đạt thì các loài hoa có thể vẽ bằng Canva, bớt khoảng 17 hình Model Studio |
| T15. Luống hoa dọc lối đi (chủ dự án duyệt 26/11, đã vẽ 26/11 bằng Canva, 1 hình; chờ chủ dự án xem) | 6 khóm hoa rời, lưới 3 × 2 | nhìn chính diện, hơi từ trên xuống như máy quay của cảnh | mỗi khóm là một ụ hoa thấp, dài hơn cao (khoảng 0,6 × 0,45 m): hồng trắng, cẩm tú cầu trắng, baby trắng, lá bạch đàn xanh xám; hoa màu **trắng** để mặt nạ đổi tông làm tự động; nền xanh dương phẳng | chậu, đất, bóng, người | `cong-tron.png` (cổng tròn vẽ tay, đã tải lên Canva) làm mẫu nét | tách nền sạch; mã xếp các khóm nối nhau dọc hai bên lối (thảm, lối đá, lối gương) theo phối cảnh của tranh, xa nhỏ gần to, trông thành một luống liền; nét gần cổng tròn vẽ tay và cụm hoa T14 |
| T16. Vườn Hồ nới rộng (chủ dự án chọn 26/11: "vẽ scale up từ cái cũ"; vẽ thử 1 hình Canva, chưa đưa vào trang thử trước khi chủ dự án xem) | nền trống ngày, cùng nơi với Vườn Hồ nhưng bãi cỏ rộng khoảng 60 × 45 m | máy quay đặt cao trên thềm biệt thự, nhìn chếch xuống khoảng 25–30°, thấy trọn bãi cỏ, lan can đá, hồ, núi, hàng bách | bãi cỏ phẳng rộng, một lối đá thẳng bề ngang không đổi chạy từ máy quay tới chỗ làm lễ bên lan can (để đo phối cảnh từ hai mép lối và đường chân trời), lan can đá, hồ, núi, trời mây như Vườn Hồ | bàn, ghế, người, cổng, đài phun nước, đồ trang trí | `nen-ho` (nền trống Vườn Hồ, tải lên Canva) làm mẫu cảnh và nét | cùng nét, màu, cảnh với Vườn Hồ; bãi cỏ đủ chỗ cho 100 bàn khi đo bằng lưới 1 m; lối đá thẳng đo được. Khi đạt: dựng lại bàn ghế 3D ở góc chếch mới (0 lượt), đo phối cảnh, thêm thành một nơi mới trong xưởng (không ghi đè Vườn Hồ) |

**Thứ tự:** T10 và T11 chạy sau khi T7 (ghế 8 góc) đạt, vì cần lưng ghế để gắn thử. T12 rồi T13 (T13 vẽ từ T12 để cùng góc nhìn).

## 9. Việc làm được ngay, không tốn lượt

- Dựng các hiệu ứng mã ở mục 5 trong `game/lab/xuong/` và gắn vào màn thử trang trí theo lớp.
- Chuyển danh mục trang trí sang dạng dữ liệu (một dòng mỗi món, có nhãn), và dựng bộ chọn hai bước (kiểu rồi màu).
- Dựng 21 bộ phong cách từ những món đã có, để bộ chọn có dữ liệu chạy thử.
- Dựng bộ xếp bàn bằng mã: 13 cách xếp, tính số bàn theo số khách, đo vùng đặt bàn và sức chứa của Vườn Hồ và Sân nhà quê, sơ đồ nhìn từ trên xuống. Chạy thử trước với bàn dài đã có.
- Chế độ so sánh hai phương án đặt cạnh nhau (cùng cảnh, hai bộ lựa chọn).
- Theo phần mềm thiết kế tiệc chủ dự án gửi 26/11 (`tham-khao-thiet-ke-tiec.md`): xem thử buổi lễ 30 giây theo dòng thời gian tiết mục; kéo bàn trên mặt bằng.
- Ghế theo lớp còn thiếu đai và nơ: chờ T10 (nơ vẽ bằng mã trông như hình dán).
- Cận cảnh hiện là một hình cho cả chỗ ngồi: muốn đổi từng món (ly, khăn ăn, thiệp) thì vẽ mỗi món một lớp cùng máy ảnh.
- Ảnh toạ độ khăn khá nặng (190–540 KB mỗi bộ, chỉ tải khi chọn hoạ tiết hoặc khăn phủ): thử giảm còn nửa cỡ rồi nội suy.

Đã làm (26/11), 0 lượt: màn thử trang trí theo lớp có đủ đồ tự vẽ. Cổng: cổng tròn vẽ tay và 6 khung bằng mã (4 màu khung), mỗi khung gắn sẵn cụm hoa Canva T14 (bật, tắt; nhuộm 6 tông qua mặt nạ cánh hoa riêng cho mẫu đơn hồng). Nút ban ngày, ban đêm cho cả hai nơi. Bàn: bàn dài vẽ tay và 7 bộ 3D (tròn 6, 10, 12; dài 8, 12, 20; dài xếp chéo). Khăn nền và khăn phủ chọn hình (vuông, vuông chéo, tròn ngắn, chạy bàn; bàn dài: chạy bàn, chạy ngang, phủ ngắn), chất (trơn, ren, kim sa, gấm) và 10 màu; đổi màu đệm, khung ghế. "Xem gần" mở cận cảnh kiểu Âu hoặc kiểu Việt, cùng khăn với bàn, đổi màu đĩa lót (đĩa kê) và dao nĩa (đũa). Ảnh toạ độ khăn gói 12 bit vào RGB, lưu không nén mất dữ liệu; trang tự kiểm một điểm mẫu mỗi ảnh (đúng cả 9 bộ). Mỗi lần ghép một món dưới 80 ms ở bàn lớn nhất. Xuất bằng `ve/xuat_lab.py`.

Đã làm (26/11, theo `tham-khao-thiet-ke-tiec.md`), 0 lượt: góc nhìn "Mặt bằng" (vùng đặt bàn ước lượng, bàn tự xếp đủ số khách, báo thiếu chỗ), mục "Lưu ý" có số đếm ở đầu bảng, mục "Bảng kê" (số lượng, cỡ khăn, khoảng tiền của những món đã có số tạm), 5 "Mẫu có sẵn".

Đã làm (26/11), 0 lượt: ánh sáng (dây đèn, đom đóm quấn cổng, đèn rọi 5 màu, nến bàn), màn LED (hai màn hoặc một màn lớn, 4 nội dung), âm thanh (3 kiểu loa dựng 3D), điện ước lượng và máy phát; chi tiết ở `tham-khao-thiet-ke-tiec.md`.
- Dựng màn chương trình: dòng thời gian tiết mục theo `spec.md` mục 4. Màn này phải có trước khi vẽ nhiều người biểu diễn; nếu không, hình tiết mục chưa có chỗ dùng. Vì vậy tháng 12 chỉ vẽ trước vài tiết mục mỗi nhóm.

## 10. Cần chủ dự án quyết

1. Danh sách bộ phong cách (mục 3.9) và tiết mục (mục 6): thêm, bớt hay giữ nguyên?
2. Các bản tự vẽ (khung cổng, bản đêm, ghế và bàn 3D, cận cảnh) có đủ giống tranh vẽ tay không? Mặc định đang dùng; đã có trong trang thử để chủ dự án xem từng cái.
3. Tấm thử T16 (Vườn Hồ nới rộng, mục 8b) có đạt không, rồi mới đưa vào trang thử.
4. Thứ tự vẽ nơi mới (mục 4): đề xuất Nhà kính trước, rồi sảnh tiệc có màn LED.

Đã xong (25–26/11):
- Duyệt vòng chơi trang trí và bảng giá số tạm (26/11, `vong-choi.md` mục 8, `gia-tham-khao.md` mục 6). Tiệc rất đông: vẽ nới rộng Vườn Hồ cũ (T16); thêm nơi mới vào kế hoạch, có nơi trong nhà (mục 4).
- T14 đạt (26/11): hoa và đồ trang trí mềm vẽ bằng Canva; đã đưa cụm hoa vào trang thử, gắn trên 6 khung cổng.
- Chọn phương án A (trang trí trước) ngày 26/11. Duyệt và đã vẽ T14 bằng Canva; được dùng 100 hình Canva.
- Hạc giấy: đặt ở đâu cũng được; đã đưa vào đồ treo, chỗ ngồi, góc phụ và bộ "Nghìn hạc".
- Chủ dự án mở thêm mạng cho Điện máy Xanh, Sapo, Brands Vietnam; đọc trọn được Sapo.
- Cho dùng model khác nếu nét vẽ vẫn đẹp (mục 7c).
- Game dùng tối đa 40% gói Model Studio mỗi tháng (khoảng 166 hình); `gen.py` tự đếm và chặn.
- Tháng 11 không chạy đợt nào; tự vẽ được thì tự vẽ. Đợt 0, 8b chuyển sang đầu tháng 12.
- Chủ dự án chọn thêm màn cận cảnh bàn.
- Duyệt đổi T9 thành bàn dài phủ khăn trắng chấm đất; T10–T13 chạy đầu tháng 12 (mục 8b).
- Chủ dự án mở mạng; đọc được CV Linens, Pinterest, Style Me Pretty. The Knot và WeddingWire vẫn chặn máy truy cập tự động.

## Nguồn

Xu hướng Pinterest (lượt đầu lấy qua công cụ tìm kiếm; ngày 25/11 đã đọc trọn hai báo cáo 2026 và 2025):
- [Pinterest Wedding Trends Report 2026](https://newsroom.pinterest.com/news/wedding-trend-report-2026/)
- [The Pinterest Annual Wedding Trends Report (2025)](https://newsroom.pinterest.com/news/the-annual-pinterest-wedding-trends-report/)
- [Social Media Today: Pinterest releases 2026 wedding trends report](https://www.socialmediatoday.com/news/pinterest-releases-2026-wedding-trends-report/818774/)
- [JCK: Pinterest Releases 2026 Wedding Trends Report](https://www.jckonline.com/editorial-article/pinterest-26-wedding-report/)
- [Together Journal: Pinterest Wedding Trends Report 2026](https://togetherjournal.com/pinterest-wedding-trends-report-2026/)
- [The Gloss: Pinterest's top proposal, bride and groom, and alt wedding trends](https://thegloss.ie/pinterests-top-proposal-bride-and-groom-and-alt-wedding-trends/)

Hiệu ứng, giải trí, cổng lễ:
- [The Knot: cold sparklers for wedding](https://www.theknot.com/content/cold-sparklers-for-wedding)
- [The Knot: wedding reception trends](https://theknot.com/content/wedding-reception-trends)
- [WeddingWire: ceremony structures for an outdoor wedding](https://www.weddingwire.com/wedding-ideas/stunning-ceremony-structures-for-an-outdoor-wedding)
- [Singaporebrides: wedding arch styles](https://singaporebrides.com/articles/2025/08/wedding-arch-styles/)

Khăn nhiều lớp và trang trí ghế (ngày 25/11, **đã đọc trọn**). Đường dẫn CV Linens bắt đầu bằng `https://www.cvlinens.com/blogs/styling-tips/` nếu không ghi khác:
- [C1] how-wedding-decorators-use-layered-linens-luxury-looks · [C2] overlay-layering-ideas-round-vs-rectangular-tables · [C3] [round-table-overlay-sizing](https://www.cvlinens.com/blogs/product-101/round-table-overlay-sizing) · [C4] rectangular-table-overlay-sizing-combinations · [C5] choosing-right-table-overlay-fabrics · [C6] modern-table-overlay-trends-2025-events
- [C7] can-you-layer-two-table-runners-on-one-table · [C8] how-long-should-table-runner-be · [C9] are-table-runners-out-of-style · [C10] simple-wedding-tablescape-three-linens · [C11] 101-layering-tablescapes-styling-guide · [C12] [swag-a-rectangular-tablecloth](https://www.cvlinens.com/blogs/new-arrivals/swag-a-rectangular-tablecloth)
- [C13] table-skirt-guide-the-basics-to-table-skirting · [C14] are-skirted-tables-in-style · [C15] 2026-wedding-trends-whats-in-whats-out-what-timeless · [C16] overlay-patterns-round-rectangular-tables · [C17] layering-table-linens-for-stunning-tablescapes
- [H1] types-wedding-chair-covers · [H2] how-to-weave-chiffon-sashes-on-chiavari-chairs · [H3] how-to-tie-cinched-chiavari-chair-sash · [H4] how-to-tie-a-diagonal-sash-on-chiavari-chair · [H5] how-to-tie-a-double-wrap-knot-chair-sash-tie · [H6] how-to-tie-gift-box-bow-chair-sash-ideas
- [H7] how-to-tie-sash-on-chiavari-chairs · [H8] diy-chair-sash-ideas-next-event · [H9] how-long-should-chair-sashes-be · [H10] chair-band-decor-inspirations · [H11] [spandex-rosette-chair-bands](https://www.cvlinens.com/blogs/product-101/spandex-rosette-chair-bands)
- [H12] [layered-skirting-chair-back-covers](https://www.cvlinens.com/blogs/new-arrivals/layered-skirting-chair-back-covers) · [H13] [curly-willow-chair-back-covers](https://www.cvlinens.com/blogs/new-arrivals/curly-willow-chair-back-covers) · [H14] [new-chairback-covers-oversize-chair-flowers](https://www.cvlinens.com/blogs/new-arrivals/new-chairback-covers-oversize-chair-flowers-spandex-cocktail-table-covers) · [H15] elevating-chair-decor · [H16] how-to-decorate-chiavari-chairs
- [P1] [Pinterest Wedding Trends Report 2026](https://newsroom.pinterest.com/news/wedding-trend-report-2026/) · [P2] [Pinterest 2025](https://newsroom.pinterest.com/news/the-annual-pinterest-wedding-trends-report/) · [P3] [Pinterest Predicts 2026](https://newsroom.pinterest.com/news/pinterest-predicts-nonconformity-self-preservation-and-escapism-drive-21-trends-for-2026/) · [S1] [Style Me Pretty: 10 wedding trends for 2026](https://perspectives.stylemepretty.com/10-wedding-trends-you-need-to-know-for-2026/)

Đồ bàn (ngày 25/11). **Đọc trọn**; đường dẫn bắt đầu bằng `https://www.cvlinens.com/blogs/styling-tips/` nếu không ghi khác:
- [D1] [what-is-a-charger-plate](https://www.cvlinens.com/blogs/product-101/what-is-a-charger-plate-uses-materials-etiquette-more) · [D2] basic-informal-formal-proper-table-settings · [D3] what-is-a-goblet-and-what-is-it-used-for · [D4] what-side-of-plate-does-napkin-go-to · [D5] should-charger-plates-match-flatware-or-table-linens · [D6] are-charger-plates-old-fashioned
- [D7] 2026-wedding-trends-whats-in-whats-out-what-timeless · [D8] 101-layering-tablescapes-styling-guide · [D11] lunar-new-year-tablescape-ideas · [D12] can-i-use-round-chargers-with-square-plates · [D14] how-to-fold-napkin-with-silverware · [D17] choosing-the-right-tableware-guide · [D15] tên sản phẩm trong sitemap sản phẩm của CV Linens

Đồ bàn, **đọc trọn** ngày 25/11: [Sapo: cách set up bàn ăn kiểu Á](https://www.sapo.vn/blog/set-up-ban-an-kieu-a). **Chỉ có đoạn trích** (trang chặn máy truy cập tự động): [Điện máy Xanh: sắp xếp bàn ăn kiểu Á](https://www.dienmayxanh.com/vao-bep/bat-mi-cach-sap-xep-ban-an-kieu-a-don-gian-va-nhanh-chong-11999) · [Brands Vietnam: quy trình setup bàn ăn](https://www.brandsvietnam.com/congdong/topic/cam-nang-van-hanh-dich-vu-2-quy-trinh-va-tieu-chuan-setup-ban-an) · [Foody: Thành Công Palace](https://www.foody.vn/ha-noi/thanh-cong-palace) · [East Meets Dress: đũa khắc tên](https://eastmeetsdress.com/collections/all/products/custom-chopsticks) · [Offbeat Wed: bao đũa làm thiệp chỗ ngồi](https://offbeatwed.com/chopstick-sleeve-place-cards/) · [Chairish: mismatched china](https://www.chairish.com/blog/mismatched-china/) · [Livingetc: table setting trends 2025](https://www.livingetc.com/us/ideas/table-setting-trends-for-2025) · [Livingetc: scalloped dinnerware](https://livingetc.com/shopping/scalloped-dinnerware) · [C Party Rentals: two-toned flatware](https://cpartyrentals.com/trend-alert-two-toned-flatware/)

Khăn, ghế, đồ trên bàn (lượt đầu ngày 25/11). Các trang này chỉ hiện trong kết quả tìm kiếm, nên nội dung lấy từ đoạn trích:
- [The Knot: wedding decor trends](https://www.theknot.com/content/wedding-decor-trends)
- [The Knot: wedding chairs](https://www.theknot.com/content/wedding-chairs)
- [The Knot: wedding place setting ideas](https://www.theknot.com/content/wedding-place-setting-ideas)
- [CV Linens: 2026 wedding trends, what's in, what's out](https://cvlinens.com/blogs/styling-tips/2026-wedding-trends-whats-in-whats-out-what-timeless)
- [CV Linens: types of wedding chair covers](https://cvlinens.com/blogs/styling-tips/types-wedding-chair-covers)
- [WeddingWire: 11 popular wedding chair styles](https://www.weddingwire.com/wedding-ideas/11-popular-wedding-chair-styles)
- [WeddingWire: types of fabric you can rent](https://www.weddingwire.com/wedding-ideas/types-of-fabric-you-can-rent)
- [WeddingWire forum: 1000 cranes](https://www.weddingwire.com/wedding-forums/1000-cranes/4ab450798118de55.html)
- [Zola: how to choose wedding chair sashes](https://www.zola.com/expert-advice/how-to-choose-wedding-chair-sashes)
- [All Cotton and Linen: wedding decor trends](https://allcottonandlinen.com/blogs/news/wedding-decor-trends)
- [Love Inc.: drapery as decor, 2026](https://loveincmag.com/top-wedding-trend-for-2026-innovative-ways-to-use-drapery-as-decor/)
- [Livingetc: table setting trends 2025](https://www.livingetc.com/us/ideas/table-setting-trends-for-2025)
- [Guides for Brides: bow wedding trend](https://guidesforbrides.co.uk/wedding-ideas/bow-wedding-trend)
- [Domino: DIY paper wedding decorations](https://www.domino.com/content/diy-paper-wedding-decorations-ideas/)
- [Style Me Pretty: Pinterest Predicts 2026 roundup](https://perspectives.stylemepretty.com/pinterest-predicts-2026-the-complete-wedding-trend-roundup/)
- [Mimi: khăn trải bàn tiệc cưới](https://mimi.com.vn/blogs/news/khan-trai-ban-tiec-cuoi-dep/)
- [Xưởng Hoà Phát: khăn trải bàn xếp ly](https://xuonghoaphat.com/khan-trai-ban-xep-ly/)
- [Ninh Khương: xu hướng khăn trải bàn 2026](https://ninhkhuong.com/blogs/cam-nang/xu-huong-khan-trai-ban-2026-top-chat-lieu-duoc-ua-chuong-nhat)
- [Hantexco: nơ ghế](https://hantexco.vn/no-ghe/)
- [Song Lam: trang trí áo ghế tiệc cưới với nơ chéo](https://songlamdecor.com/tin-tuc/trang-tri-ao-cuoi-tiec-cuoi-voi-no-cheo.html)
- [Phúc Hoà: mẫu ghế Tiffany](https://phuchoa.com.vn/mau-ghe-tiffany/)
- [Nội thất Long Vũ: bàn ghế nhựa đám cưới](https://noithatlongvu.com/ban-ghe-nhua-dam-cuoi/)
- [7799 Wedding: thuê trang trí rạp cưới](https://7799wedding.vn/thue-trang-tri-rap-cuoi-dep-ha-noi-nd311845.html)
- [White Wedding: màu sắc xu hướng cưới 2026](https://whitewedding.vn/mau-sac-xu-huong-cuoi-2026/)
- [Chiaki: chữ Hỷ ép kim và cắt laser](https://chiaki.vn/chu-hy-ep-kim-co-dien-den-cac-mau-cat-laser-hien-dai-tinh-xao)
- [Điện máy Xanh: 8 cách xếp khăn ăn](https://www.dienmayxanh.com/vao-bep/8-cach-xep-khan-trang-tri-ban-an-them-dep-mat-va-trang-trong-15657)

Việt Nam:
- [VnExpress: Giới trẻ chuộng tiệc cưới cá nhân hoá](https://vnexpress.net/gioi-tre-chuong-tiec-cuoi-ca-nhan-hoa-4868919.html)
- [Lao Động: Những xu hướng tổ chức đám cưới năm 2026](https://news.laodong.vn/gia-dinh-hon-nhan/nhung-xu-huong-to-chuc-dam-cuoi-nam-2026-1738993.ldo)
- [Tinh tế: Xu hướng trang trí tiệc cưới năm 2026](https://tinhte.vn/thread/xu-huong-trang-tri-tiec-cuoi-nam-2026.4174088/)
