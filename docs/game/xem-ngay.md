# Xem tuổi, xem ngày, xem giờ

Tài liệu đi kèm [đặc tả game](spec.md), mục 3b. Nó ghi **quy tắc tính** để bản chơi thử lập trình được ngay, và để một người am hiểu soát lại.

**Về độ tin cậy.** Tử vi, thần số học và cung hoàng đạo là tín ngưỡng và thói quen văn hoá, không phải khoa học kiểm chứng được. Game đưa chúng vào vì ngoài đời chúng quyết định ngày cưới, giá ngày đẹp và sự đồng thuận của hai họ. Game không dùng chúng để đoán tương lai.

**Về nguồn.** Các bảng dưới đây mình ghi theo những quy tắc phổ biến mà mình nhớ, chưa đối chiếu với lịch vạn niên in. Các sách lịch có nhiều dị bản. Trước khi phát hành cần một người am hiểu soát lại từng bảng.

## 1. Dữ liệu đầu vào

- Ngày sinh dương lịch của hai nhân vật (nhân vật trong game có ngày sinh riêng; người chơi được nhập ngày sinh thật nếu muốn, lưu trên máy, không gửi đi đâu).
- Lịch âm: đổi từ dương lịch bằng thuật toán thiên văn của Hồ Ngọc Đức (múi giờ +7), kiểm chéo với lịch in của vài năm.
- Can chi của năm âm lịch: chi = (năm − 4) chia 12 lấy dư (0 là Tý), can = (năm − 4) chia 10 lấy dư (0 là Giáp). Ví dụ 2020 là Canh Tý.
- Can chi của ngày, tính từ số ngày Julius (JDN): chi = (JDN + 1) chia 12 lấy dư, can = (JDN + 9) chia 10 lấy dư.
- Tuổi mụ = năm xem (âm lịch) − năm sinh (âm lịch) + 1.

## 2. Xem tuổi (hai người có hợp không)

| Quan hệ giữa hai con giáp | Các nhóm | Game hiểu là |
|---|---|---|
| Tam hợp | Thân–Tý–Thìn · Dần–Ngọ–Tuất · Tỵ–Dậu–Sửu · Hợi–Mão–Mùi | rất hợp |
| Lục hợp | Tý–Sửu · Dần–Hợi · Mão–Tuất · Thìn–Dậu · Tỵ–Thân · Ngọ–Mùi | hợp |
| Lục xung (nằm trong tứ hành xung) | Tý–Ngọ · Sửu–Mùi · Dần–Thân · Mão–Dậu · Thìn–Tuất · Tỵ–Hợi | xung |
| Còn lại | | bình thường |

Bản sau có thể thêm mệnh ngũ hành (nạp âm) tương sinh, tương khắc. Lá số tử vi đầy đủ mười hai cung thì không làm: quá phức tạp so với giá trị nó mang lại cho game.

## 3. Xem năm cưới

- **Kim Lâu** (tính theo tuổi mụ của cô dâu): tuổi mụ chia 9 dư 1, 3, 6 hoặc 8 thì phạm.
- **Tam Tai** (tính cho từng người, ba năm liền): tuổi Thân, Tý, Thìn gặp năm Dần, Mão, Thìn · tuổi Dần, Ngọ, Tuất gặp năm Thân, Dậu, Tuất · tuổi Tỵ, Dậu, Sửu gặp năm Hợi, Tý, Sửu · tuổi Hợi, Mão, Mùi gặp năm Tỵ, Ngọ, Mùi.

Cách gỡ theo tục lệ, dùng làm lối ra trong game (cần soát lại theo từng vùng): dời sang năm khác; làm lễ xin dâu hai lần; đợi qua ngày Đông chí.

## 4. Xem ngày

**Ngày hoàng đạo, hắc đạo.** Mười hai ngày theo chi xoay vòng qua mười hai vị thần, bắt đầu bằng Thanh Long. Tính từ ngày Thanh Long, các ngày thứ 1, 2, 5, 6, 8, 11 là hoàng đạo (Thanh Long, Minh Đường, Kim Quỹ, Bảo Quang, Ngọc Đường, Tư Mệnh); sáu ngày còn lại là hắc đạo.

| Tháng âm lịch | Ngày Thanh Long | Sáu ngày hoàng đạo |
|---|---|---|
| Giêng, Bảy | Tý | Tý, Sửu, Thìn, Tỵ, Mùi, Tuất |
| Hai, Tám | Dần | Dần, Mão, Ngọ, Mùi, Dậu, Tý |
| Ba, Chín | Thìn | Thìn, Tỵ, Thân, Dậu, Hợi, Dần |
| Tư, Mười | Ngọ | Ngọ, Mùi, Tuất, Hợi, Sửu, Thìn |
| Năm, Mười một | Thân | Thân, Dậu, Tý, Sửu, Mão, Ngọ |
| Sáu, Chạp | Tuất | Tuất, Hợi, Dần, Mão, Tỵ, Thân |

**Ngày kiêng.** Tam Nương: mùng 3, 7, 13, 18, 22, 27 âm lịch. Nguyệt Kỵ: mùng 5, 14, 23. Tháng Bảy âm lịch: nhiều nhà tránh cưới. Ngày xung với tuổi cô dâu hoặc chú rể (chi của ngày lục xung với chi của tuổi).

Bản sau có thể thêm: Sát Chủ, Thọ Tử, mười hai trực, hai mươi tám sao.

**Điểm của một ngày trong game** (thang 0–100): bắt đầu 50; hoàng đạo +25, hắc đạo −15; Tam Nương hoặc Nguyệt Kỵ −25; xung tuổi một trong hai người −25; tháng Bảy âm −15; cuối tuần +10 (dễ cho khách, không liên quan tín ngưỡng). Từ 70 trở lên là "ngày đẹp".

## 5. Xem giờ

Giờ hoàng đạo tính như ngày, nhưng lấy mốc theo chi của ngày: ngày Dần, Thân thì Thanh Long ở giờ Tý · Mão, Dậu ở giờ Dần · Thìn, Tuất ở giờ Thìn · Tỵ, Hợi ở giờ Ngọ · Tý, Ngọ ở giờ Thân · Sửu, Mùi ở giờ Tuất. Ví dụ ngày Tý có sáu giờ hoàng đạo: Tý, Sửu, Mão, Ngọ, Thân, Dậu.

Mỗi giờ âm lịch dài hai tiếng (giờ Tý là 23:00–1:00, giờ Sửu 1:00–3:00, cứ thế tiếp). Game dùng giờ hoàng đạo cho ba mốc: xuất phát đi rước dâu, làm lễ gia tiên, đón dâu vào nhà.

## 6. Thần số học

- **Con số chủ đạo:** cộng mọi chữ số của ngày, tháng, năm sinh dương lịch, rồi cộng tiếp các chữ số của kết quả cho tới khi còn một số từ 2 tới 11, hoặc 22. Đây là cách tính đang phổ biến ở Việt Nam (trường phái Pythagoras); các trường phái khác rút về 1–9.
- **Năm cá nhân:** cộng ngày sinh, tháng sinh và năm đang xét theo cùng cách.
- Game dùng thần số học theo kiểu nhẹ nhàng: gợi ý nét tính cách của hai nhân vật, và một dòng nhận xét về ngày cưới. Nó không có sức nặng với hai họ như lịch âm.

## 7. Cung hoàng đạo

Mười hai cung theo ngày sinh dương lịch, chia bốn nhóm: Lửa (Bạch Dương, Sư Tử, Nhân Mã), Đất (Kim Ngưu, Xử Nữ, Ma Kết), Khí (Song Tử, Thiên Bình, Bảo Bình), Nước (Cự Giải, Bọ Cạp, Song Ngư). Quy ước hợp nhau: Lửa với Khí, Đất với Nước, và cùng nhóm.

Game dùng cung hoàng đạo cho chuyện trò lúc hẹn hò, gợi ý phong cách tiệc và quà, và làm chủ đề trang trí. Nhóm bạn bè trong game quan tâm tới nó nhiều hơn bố mẹ.

## 8. Nguyên tắc trình bày

1. Luôn ghi rõ nguồn của nhận định: "theo lịch âm", "theo thần số học". Không viết như một sự thật.
2. Không bao giờ kết luận "không nên cưới". Kết quả chưa hợp luôn đi kèm cách gỡ theo tục lệ và lựa chọn bỏ qua.
3. Tính theo quy tắc công khai, không ngẫu nhiên: cùng ngày sinh thì cùng kết quả, và người chơi bấm vào xem được vì sao.
4. Không bán "giải hạn", không thu tiền thật cho việc xem. Phí thầy trong game trả bằng tiền trong game.
5. Người chơi tắt hẳn phần này được. Khi tắt, hai họ trong game cũng không nhắc tới.
