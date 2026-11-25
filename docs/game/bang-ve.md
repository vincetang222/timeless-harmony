# Bảng vẽ tiếp theo: trang trí, hiệu ứng sân khấu, tiết mục

**Bản đề xuất chờ chủ dự án duyệt (25/11/2026).** Tài liệu này nối tiếp mục 7 của [vong-choi.md](vong-choi.md) (trang trí theo lớp đã thử đạt ở 2 nơi). Mọi giá là số tạm. Tên bộ phong cách, nơi tổ chức và người biểu diễn đều hư cấu.

## 0. Tóm tắt

- **Trang trí:** muốn có hàng nghìn mẫu thì không vẽ từng mẫu. Ta vẽ từng bộ phận (khung cổng, cụm hoa theo loài, bàn, hoa bàn…), rồi để mã ghép, đổi màu và chỉnh sáng. Nếu hai bài thử ở mục 8 đạt, chỉ riêng cổng đã có khoảng 13.000 cách phối từ 37 tấm vẽ. Nếu không đạt, còn khoảng 320.
- **Hiệu ứng sân khấu:** pháo hoa, pháo giấy, pháo lạnh, khói sàn, bong bóng, màn LED, chữ neon… gần như toàn bộ vẽ bằng mã, **không tốn lượt**. Cái cần vẽ là nền đêm và nền trong nhà để hiệu ứng có chỗ diễn.
- **Tiết mục:** 32 tiết mục trong 4 nhóm, mỗi tiết mục là một hình người biểu diễn rời, khoảng 34 tấm. Điệu nhảy của chính cặp đôi là việc khác, cần tư thế mới cho nhân vật (mục 6.6).
- **Hạn mức:** cả bảng này khoảng 106 tấm. Cộng việc đã duyệt và dự phòng sửa thì vừa gói tháng 12 (mục 7).
- **Bước đầu:** 6 tấm thử cho các kỹ thuật chưa chứng minh, chạy được ngay tháng này (mục 8).

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
| **Khung trần + cụm hoa rời ghép bằng mã** | **Chưa thử** | Cụm hoa có thể trông lơ lửng, cuống không bám khung. Thử T1, T2 |
| **Nhiều món trên một tấm, mã cắt rời** | **Chưa thử** | Mô hình có thể vẽ các món chạm nhau, khác góc nhìn, khác cỡ. Thử T2, T3 |
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

Mình không mở được trang báo cáo gốc của Pinterest từ môi trường làm việc. Các xu hướng dưới đây lấy từ trang tin của Pinterest qua công cụ tìm kiếm và từ các bài tổng hợp lại báo cáo (danh sách ở cuối). Game chỉ lấy **ý tưởng chung** của từng xu hướng, đặt tên Việt hư cấu, không chép hình cụ thể nào trên Pinterest.

| Xu hướng (nguồn) | Ý chính | Đưa vào game |
|---|---|---|
| Ethereal Shimmer, sắc xà cừ (Pinterest 2026) | Ánh kim, ánh ngũ sắc, hiệu ứng "phát sáng" | Bảng màu "Ánh xà cừ"; mã phủ ánh ngũ sắc lên khung gương và khăn |
| Cinematic Speakeasy, nơi bất ngờ (Pinterest 2026) | Tiệc ở quán jazz, phòng rượu tầng hầm, nhà hát cũ, nhà kính | Nơi "Câu lạc bộ jazz" và "Nhà kính" (mục 4); bộ "Đêm jazz" |
| Quirky Cakes (Pinterest 2026) | Bánh cưới lạ mắt, vui | Tấm bánh cưới có kiểu "bánh vui" (mục 3.8) |
| Nostalgic Tech Touches (Pinterest 2026) | Máy hát đĩa, máy ảnh lấy liền, giải trí kiểu cũ | Góc ảnh hoài cổ; bộ "Hoài cổ analog" |
| Alt Bouquets, Messy Coquette (Pinterest 2026) | Hoa không theo lối cũ; nơ, quầy hoa tự cắm, trái cây cam quýt làm hoa bàn | Hoa bàn cam quýt, quầy hoa tự cắm; bộ "Nơ và cam quýt" |
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

### 3.3 Khung cổng và phông lễ (vẽ, 20 tấm)

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

### 3.4 Bàn ghế (vẽ, 6 tấm)

bàn tròn khăn dài, ghế chiavari (vẽ lại bản rời) · bàn dài gỗ, ghế lưng chéo (đã có) · bàn vuông, ghế trong suốt · bàn dài phủ khăn chữ U kiểu bàn tiệc lớn · bàn tre, ghế mây · bàn tròn rạp quê, ghế inox bọc vải

Mỗi kiểu bàn vẽ khăn **màu trắng trên gỗ hoặc kim loại màu khác hẳn**, để mặt nạ khăn làm tự động.

### 3.5 Hoa bàn (vẽ, 3 tấm × 6 kiểu)

thấp tròn · cao trong bình thuỷ tinh · nến trụ và bạch đàn · cam quýt và lá · đèn lồng nhỏ và hoa · chân nến đồng hoa rủ · lọ thuỷ tinh nhỏ rải dọc bàn · hoa và trái cây miền Tây · mâm bồng đỏ (truyền thống) · nến nổi trong bát · rêu và đá · hoa giấy thủ công · bình gốm lam · sen trong bát · lồng chim cổ · ngọn hoa cao vút · khay trái cây · đèn dầu cổ

### 3.6 Lối đi (vẽ, 2 tấm × 6 kiểu; thảm và cánh hoa là mã)

chậu hoa · đèn lồng giấy trên chân · nến trong lọ · cột hoa cao · đèn bão · lồng chim · ghế dài phủ hoa · bó cỏ lau · đá cuội và nến · chậu cây cảnh · cọc tre buộc nơ · đèn lồng đỏ trên chân

### 3.7 Treo trên cao (vẽ, 3 tấm × 6 kiểu; dây đèn là mã)

đèn lồng Hội An · đèn lồng đỏ · chùm hoa treo · chùm đèn pha lê · ô giấy · voan rủ · dây cờ đuôi nheo · quạt giấy · chuông gió · nón lá treo · lồng đèn kéo quân · vòng hoa treo

### 3.8 Góc phụ và bánh cưới (vẽ, 5 tấm)

| Tấm | Có gì |
|---|---|
| Bánh cưới | 6 kiểu: nhiều tầng trắng, tầng hoa tươi, bánh trần, bánh lệch vui, bánh màu đậm, bánh xu xê kiểu Việt |
| Tháp ly | tháp ly sâm panh trên bàn, chai, khăn |
| Quầy hoa tự cắm | quầy gỗ, xô hoa, kéo, giấy gói |
| Góc ảnh hoài cổ | máy ảnh lấy liền trên giá, máy hát đĩa, ghế mây, khung ảnh |
| Bàn đón khách | bảng chào tên cặp đôi (chữ do mã viết), sổ ký tên, hộp mừng |

### 3.9 Bộ phong cách (mã, 0 tấm)

Mỗi bộ chọn sẵn: khung, loài hoa, bố cục, bảng màu, bàn, hoa bàn, lối đi, đồ treo, và gợi ý tiết mục. Người chơi chọn bộ rồi sửa từng món nếu muốn.

| Nhóm | Bộ |
|---|---|
| Theo xu hướng | Ánh xà cừ · Đêm jazz · Nơ và cam quýt · Hoa siêu thực · Nâu mocha · Đồng nội · Hoài cổ analog |
| Kinh điển | Vườn pastel · Tối giản trắng · Mộc boho · Đen vàng art deco · Nhiệt đới · Cổ điển châu Âu |
| Việt Nam | Đỏ son Song Hỷ · Phố đèn lồng · Lá dừa miền Tây · Sen Huế · Đào mai ngày Tết · Cúc hoạ mi đầu đông · Gốm lam · Tre làng |

## 4. Nơi tổ chức cần thêm (vẽ, 16 tấm)

| Nhóm | Nơi | Tấm | Ghi chú |
|---|---|---|---|
| Nền trống ngoài trời | Đồi Thông Sương, Bến Đèn Lồng, Bãi Dừa Xanh, Vườn Sông Quê | 4 | 2 nơi đã có (Vườn Hồ, Sân nhà quê) |
| Trong nhà | Sảnh tiệc có màn LED; sảnh khách sạn chùm đèn; Câu lạc bộ jazz; Nhà kính; rạp cưới quê Bắc Bộ; rạp cưới quê Nam Bộ | 6 | Rạp quê Nam Bộ trùng với đợt 2 của `canh-ngoai-troi.md`, chỉ tính một lần |
| Bản đêm | 6 nơi ngoài trời | 6 | Cần cho pháo hoa và đèn. Tô tối bằng mã thường trông giả, nên vẽ; thử trước ở T6 |

Mỗi nơi mới cần đo một lần: chỗ đứng của cặp đôi, điểm neo của cổng và bàn, chỗ cho người biểu diễn, hệ số chỉnh sáng.

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

## 7. Hạn mức tháng 12 trên một trang

Gói tháng ước khoảng **416 tấm** (mỗi tấm khoảng 0,24% gói, đo ngày 24/11). Mọi con số dưới đây là ước lượng.

| Việc | Trạng thái | Nếu thử đạt | Nếu thử không đạt |
|---|---|---|---|
| Lông mày cô dâu | đã duyệt | 9 | 9 |
| Tóc (30 kiểu × 3 dáng mặt) | đã duyệt | 90 | 90 |
| Trang phục (6 bộ × 3 vóc × 2 vai) | đã duyệt | 36 | 36 |
| MC 4 bộ, ban nhạc 3 bộ | đã duyệt | 7 | 7 |
| Cảnh C1–C17, C20 và nhân vật phụ | chờ duyệt | khoảng 50 | khoảng 50 |
| Nơi đợt 2 (trừ rạp quê Nam Bộ) | chờ duyệt | 7 | 7 |
| **Bảng này:** nơi tổ chức | chờ duyệt | 16 | 16 |
| **Bảng này:** khung cổng | chờ duyệt | 20 | 20 (vẽ kèm hoa) |
| **Bảng này:** loài hoa | chờ duyệt | 17 | 0 (hoa vẽ liền vào khung) |
| **Bảng này:** bàn, hoa bàn, lối đi, đồ treo, góc phụ | chờ duyệt | 19 | khoảng 58 (mỗi món một tấm) |
| **Bảng này:** tiết mục | chờ duyệt | 34 | 34 |
| Cộng | | khoảng 305 | khoảng 327 |
| Dự phòng sửa 25% (quy tắc 4) | | khoảng 76 | khoảng 82 |
| **Tổng** | | **khoảng 381** | **khoảng 409** |
| Cách phối cổng | | khoảng 13.000 | khoảng 320 |

Nếu thử đạt thì vừa gói tháng 12 và còn dư khoảng 35 tấm. Nếu không đạt thì chỉ còn dư khoảng 7 tấm: nên dời tiết mục và cảnh C1–C13 sang tháng 1.

**Đề xuất thứ tự trong tháng 12:**

1. **Đầu tháng:** lông mày cô dâu; nền trống 4 nơi; khung cổng; loài hoa; bàn. Trang trí lên trước vì nó làm lại toàn bộ chương 4.
2. **Giữa tháng:** tóc, trang phục, MC và ban nhạc.
3. **Cuối tháng:** nơi trong nhà, bản đêm; hoa bàn, lối đi, đồ treo, góc phụ; 12 tiết mục đầu (mỗi nhóm vài tiết mục).
4. **Tháng 1:** cảnh nghi lễ C14–C17 và các cảnh còn lại; tiết mục còn lại.

Mỗi nhóm vẫn vẽ thử một tấm trước khi chạy cả lô (quy tắc 3).

## 8. Đợt 0: 6 tấm thử, chạy được ngay tháng này

Tháng 11 còn khoảng 24 tấm. Đợt này dùng tối đa 9 tấm (6 tấm và 3 lượt sửa), khoảng 2% gói. Mỗi tấm vẽ trên nền xanh dương phẳng, trừ T5 và T6 là cảnh.

| Tấm | Ai hoặc vật gì | Tư thế, trang phục | Có gì | Không có gì | Sửa từ hình nào | Đạt khi |
|---|---|---|---|---|---|---|
| T1. Khung lục giác trần | khung cổng | đứng thẳng, nhìn chính diện | khung lục giác kim loại đen mờ, chân đế phẳng | hoa, lá, vải, người, đất | `cong-tron.png` (giữ nét vẽ, góc nhìn, nền xanh) | tách nền sạch dù khung mảnh; không méo |
| T2. Cụm mẫu đơn | 4 cụm hoa rời | — | cụm góc lớn, dải rủ dài, cụm nhỏ tròn, cụm chân đế; mẫu đơn hồng nhạt, lá bạch đàn; các cụm cách xa nhau | khung, cuống lơ thơ, người | `cong-tron.png` (thay cổng bằng 4 cụm hoa) | mã cắt được 4 cụm; gắn lên khung T1 và khung tròn trông như cắm thật; nhuộm được tông |
| T3. Hoa bàn 6 kiểu | 6 món, lưới 3 × 2 | góc nhìn hơi cao như bàn tiệc | thấp tròn, cao trong bình, nến và bạch đàn, cam quýt và lá, đèn lồng nhỏ, chân nến đồng | bàn, khăn, người | `ban-dai.png` (giữ góc nhìn, cỡ) | mã cắt được ít nhất 5/6 món; cùng góc nhìn; đặt lên bàn dài và bàn tròn đúng cỡ |
| T4. Tứ tấu đàn dây | 4 nhạc công: 2 violin, 1 viola, 1 cello; 2 nam, 2 nữ | ngồi ghế, đang chơi; nam vest đen, nữ đầm đen dài | 4 ghế, 4 cây đàn, giá nhạc | đất, người khác | một tấm mẫu ghép sẵn bằng mã: ban nhạc (`ban-nhac-b.webp`) và cặp đôi đặt trên nền xanh dương phẳng (công cụ vẽ chỉ nhận một hình mẫu, và hình có nền trong suốt sẽ hiện nền đen) | nét giống ban nhạc và cặp đôi; tay cầm đàn đúng; tách nền sạch; đặt vào Vườn Hồ đúng cỡ |
| T5. Sảnh tiệc có màn LED | nền trống trong nhà | — | sảnh tiệc, lối đi giữa, sân khấu thấp phía sau, màn LED lớn **đen trơn**, chùm đèn pha lê, sàn bóng | bàn ghế, người, hoa | `nen-ho.png` (giữ góc máy và vị trí lối đi) | lối đi và đường chân trời gần như cũ để dùng chung thước phối cảnh; màn LED là hình chữ nhật sạch, mã đo được 4 góc |
| T6. Vườn Hồ ban đêm | nền trống, đêm | — | trời xanh thẫm có sao, đèn lan can sáng ấm, mặt hồ phản chiếu | trăng to, người, đồ trang trí | `nen-ho.png` | cảnh xê dịch không quá 1%; trời đủ tối cho pháo hoa bằng mã; đo được hệ số chỉnh sáng cho món rời |

**Thứ tự:** T1 rồi T2 (cặp này quyết định có 13.000 hay 320 cách phối cổng), sau đó T3, T4, T5, T6. Tấm nào không đạt thì sửa từng chỗ trên chính tấm đó, tối đa 3 lượt sửa cho cả đợt.

## 9. Việc làm được ngay, không tốn lượt

- Dựng các hiệu ứng mã ở mục 5 trong `game/lab/xuong/` và gắn vào màn thử trang trí theo lớp.
- Chuyển danh mục trang trí sang dạng dữ liệu (một dòng mỗi món, có nhãn), và dựng bộ chọn hai bước (kiểu rồi màu).
- Dựng 21 bộ phong cách từ những món đã có, để bộ chọn có dữ liệu chạy thử.
- Dựng màn chương trình: dòng thời gian tiết mục theo `spec.md` mục 4. Màn này phải có trước khi vẽ nhiều người biểu diễn; nếu không, hình tiết mục chưa có chỗ dùng. Vì vậy tháng 12 chỉ vẽ trước vài tiết mục mỗi nhóm.

## 10. Cần chủ dự án quyết

1. Danh sách bộ phong cách (mục 3.9) và tiết mục (mục 6): thêm, bớt hay giữ nguyên?
2. Có duyệt Đợt 0 (6 tấm thử ở mục 8) để chạy ngay tháng này không?
3. Thứ tự tháng 12 ở mục 7: trang trí trước, hay tóc và trang phục trước?

## Nguồn

Xu hướng Pinterest (trang gốc không mở được từ môi trường làm việc; nội dung lấy qua công cụ tìm kiếm và các bài tổng hợp):
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

Việt Nam:
- [VnExpress: Giới trẻ chuộng tiệc cưới cá nhân hoá](https://vnexpress.net/gioi-tre-chuong-tiec-cuoi-ca-nhan-hoa-4868919.html)
- [Lao Động: Những xu hướng tổ chức đám cưới năm 2026](https://news.laodong.vn/gia-dinh-hon-nhan/nhung-xu-huong-to-chuc-dam-cuoi-nam-2026-1738993.ldo)
- [Tinh tế: Xu hướng trang trí tiệc cưới năm 2026](https://tinhte.vn/thread/xu-huong-trang-tri-tiec-cuoi-nam-2026.4174088/)
