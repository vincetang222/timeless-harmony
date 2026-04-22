const SUPPLIERS_DATA = {

  // ── 1. LÊN KẾ HOẠCH CƯỚI ──
  'y-linh-planner': {
    name: 'Ý Linh Planner',
    cat: 'plan', catLabel: 'Lên kế hoạch cưới',
    city: 'Sài Gòn · Đà Lạt', cityFull: 'Sài Gòn — hoạt động toàn quốc',
    styles: ['Boutique', 'Tối giản', 'Luxury', 'Intimate'],
    about: 'Ý Linh Planner chuyên tổ chức đám cưới intimate quy mô nhỏ dưới 80 khách — nơi từng chi tiết được thiết kế có chủ đích và mỗi khoảnh khắc đều có ý nghĩa riêng. Chúng tôi tiếp cận đám cưới như một boutique event: không template, không copy-paste, chỉ có câu chuyện của riêng bạn.',
    about2: 'Với hơn 4 năm kinh nghiệm và hơn 60 đám cưới đã đồng hành, đặc biệt yêu thích các concept ngoài trời, garden party và destination wedding tại Đà Lạt.',
    stats: {deals: 62, rating: '5.0', exp: '4 năm', reply: '100%'},
    packages: [
      {name: 'Gói Seed', price: '3–5 tr', note: 'tư vấn concept', desc: 'Dành cho cặp đôi tự tổ chức nhưng cần định hướng ban đầu.',
       includes: ['1 buổi tư vấn concept 90 phút', 'Moodboard phong cách', 'Checklist chi tiết theo timeline', 'Danh sách supplier gợi ý'], featured: false},
      {name: 'Gói Bloom', price: '15–25 tr', note: 'partial planning', desc: 'Đồng hành từ ý tưởng đến ngày cưới — bạn quyết định, chúng tôi thực thi.',
       includes: ['Tất cả gói Seed', 'Kết nối & đàm phán 3–5 supplier', '1 buổi site visit', 'Hỗ trợ online suốt quá trình', 'Có mặt ngày cưới 4 giờ'], featured: true},
      {name: 'Gói Full', price: '40–70 tr', note: 'full experience', desc: 'Trải nghiệm trọn vẹn từ A–Z với concept độc quyền cho cặp đôi.',
       includes: ['Tất cả gói Bloom', 'Concept độc quyền', 'Thiết kế trò chơi gắn kết khách mời', 'Kết nối toàn bộ supplier', 'Có mặt trọn ngày cưới'], featured: false},
    ],
    reviews: [
      {name: 'Phương & Khoa', date: 'Tháng 2, 2025 · Đà Lạt', text: 'Ý Linh hiểu đúng thứ mình muốn chỉ sau 1 buổi nói chuyện. Đám cưới 35 người của tụi mình diễn ra hoàn hảo giữa rừng thông Đà Lạt — không một chi tiết nào bị bỏ sót.'},
      {name: 'Ngân & Tuấn', date: 'Tháng 12, 2024 · Sài Gòn', text: 'Lần đầu nghe đến Timeless Harmony mình còn nghi ngại, nhưng hệ thống ký quỹ thực sự yên tâm. Ý Linh vừa sáng tạo vừa chu đáo — giá trị xứng đáng với từng đồng.'},
    ],
    available: 'Tháng 7, 2026', thumb: ['#1a2820','#22201a','#1a2024'],
  },

  'dam-cuoi-xanh': {
    name: 'Đám Cưới Xanh',
    cat: 'plan', catLabel: 'Lên kế hoạch cưới',
    city: 'Hội An · Đà Nẵng', cityFull: 'Hội An — Đà Nẵng',
    styles: ['Rustic', 'Garden', 'Organic', 'Boho'],
    about: 'Đám Cưới Xanh chuyên tổ chức đám cưới kết nối với thiên nhiên — vườn, rừng, bãi biển, trang trại. Mỗi đám cưới đều hướng đến tối giản hóa rác thải và sử dụng nguyên liệu địa phương.',
    about2: 'Phù hợp cho những cặp đôi yêu thiên nhiên và muốn đám cưới có dấu ấn bền vững.',
    stats: {deals: 38, rating: '4.9', exp: '3 năm', reply: '< 12 giờ'},
    packages: [
      {name: 'Garden Starter', price: '5–8 tr', note: 'concept + checklist', desc: 'Tư vấn và lên kế hoạch cho đám cưới ngoài trời quy mô nhỏ.', includes: ['Tư vấn concept 2 giờ', 'Moodboard thiên nhiên', 'Checklist outdoor wedding', 'Gợi ý địa điểm Hội An / Đà Nẵng'], featured: false},
      {name: 'Bloom & Grow', price: '20–35 tr', note: 'partial planning', desc: 'Đồng hành lên kế hoạch và điều phối ngày cưới ngoài trời.', includes: ['Concept & moodboard', 'Kết nối supplier xanh địa phương', 'Điều phối ngày cưới', 'Xử lý phát sinh tại chỗ', 'Gói zero-waste cơ bản'], featured: true},
      {name: 'Full Nature', price: '45–65 tr', note: 'full eco-wedding', desc: 'Đám cưới xanh trọn vẹn — từ trang trí đến menu đều thuần tự nhiên.', includes: ['Toàn bộ Bloom & Grow', 'Trang trí hoàn toàn bằng vật liệu tái chế', 'Menu farm-to-table', 'Trải nghiệm độc quyền cho khách mời'], featured: false},
    ],
    reviews: [
      {name: 'Linh & Minh', date: 'Tháng 3, 2025 · Hội An', text: 'Đám cưới của tụi mình tổ chức trong một khu vườn nhỏ với 40 khách — rau củ trang trí, menu địa phương, không nhựa. Khách mời ai cũng nói chưa đi đám cưới nào ý nghĩa như vậy.'},
      {name: 'Hà & Long', date: 'Tháng 1, 2025 · Đà Nẵng', text: 'Rất ấn tượng khi Đám Cưới Xanh biết cân bằng giữa tính thẩm mỹ và tính bền vững. Không hề cảm giác "xanh = đơn giản" — ngược lại còn đẹp hơn mình tưởng.'},
    ],
    available: 'Tháng 6, 2026', thumb: ['#182218','#20241a','#1a2018'],
  },

  'muse-events': {
    name: 'Muse Events',
    cat: 'plan', catLabel: 'Lên kế hoạch cưới',
    city: 'Sài Gòn', cityFull: 'Sài Gòn — hoạt động toàn quốc',
    styles: ['Luxury', 'Editorial', 'Nghệ thuật', 'Tối giản'],
    about: 'Muse Events tiếp cận mỗi đám cưới như một dự án nghệ thuật — nơi thời trang, nhiếp ảnh, thiết kế không gian và âm nhạc hòa quyện thành một tác phẩm hoàn chỉnh. Chúng tôi phục vụ những cặp đôi có gu thẩm mỹ rõ ràng và không muốn đám cưới của mình trông giống bất kỳ ai.',
    about2: 'Chuyên tổ chức đám cưới quy mô 20–60 khách cho cặp đôi trong ngành sáng tạo — nhiếp ảnh gia, designer, kiến trúc sư.',
    stats: {deals: 29, rating: '5.0', exp: '2 năm', reply: '100%'},
    packages: [
      {name: 'Creative Brief', price: '4–6 tr', note: 'concept & direction', desc: 'Xây dựng creative brief và direction cho đám cưới của bạn.', includes: ['Deep dive interview 2 giờ', 'Creative brief document', 'Moodboard editorial', 'Supplier shortlist theo gu'], featured: false},
      {name: 'Art Direction', price: '25–40 tr', note: 'partial planning', desc: 'Đảm nhận toàn bộ creative direction và điều phối supplier.', includes: ['Creative Brief đầy đủ', 'Art direction từng chi tiết', 'Kết nối 5–8 supplier', 'Có mặt ngày cưới 6 giờ', 'Post-event report'], featured: true},
      {name: 'Full Production', price: '60–100 tr', note: 'full creative production', desc: 'Đám cưới như một buổi production — mỗi góc đều là một bức ảnh.', includes: ['Toàn bộ Art Direction', 'Set design & props', 'Lighting concept', 'Styling cặp đôi', 'Behind-the-scenes content'], featured: false},
    ],
    reviews: [
      {name: 'An & Duy', date: 'Tháng 4, 2025 · Sài Gòn', text: 'Mình là photographer và partner là graphic designer — tụi mình cực kỳ khó tính. Muse là team duy nhất hiểu tụi mình cần gì mà không cần giải thích nhiều. Kết quả đẹp đến mức chính tụi mình không tin là đám cưới của mình.'},
      {name: 'Thy & Khải', date: 'Tháng 2, 2025 · Sài Gòn', text: 'Đám cưới 35 người tại một gallery nghệ thuật ở quận 1. Muse biến không gian đó thành thứ gì đó không thể diễn tả bằng lời. Thanh toán qua Timeless Harmony cũng rất chuyên nghiệp.'},
    ],
    available: 'Tháng 8, 2026', thumb: ['#201e28','#1e1a22','#22202a'],
  },

  // ── 2. NHIẾP ẢNH & QUAY PHIM ──
  'anh-duong-studio': {
    name: 'Ánh Dương Studio',
    cat: 'photo', catLabel: 'Nhiếp ảnh & Quay phim',
    city: 'Sài Gòn', cityFull: 'Sài Gòn — hoạt động toàn quốc',
    styles: ['Film Analog', 'Vintage', 'Documentary', 'Pre-wedding'],
    about: 'Ánh Dương Studio chuyên chụp ảnh và quay phim cưới theo phong cách film analog — nơi mỗi khoảnh khắc được ghi lại như một thước phim điện ảnh. Chúng tôi tin rằng hình ảnh đẹp nhất không phải là hình ảnh hoàn hảo, mà là hình ảnh chân thật nhất.',
    about2: 'Với hơn 3 năm kinh nghiệm và 47 đám cưới đã đồng hành, đặc biệt yêu thích những đám cưới intimate — nơi cảm xúc được đặt lên hàng đầu.',
    stats: {deals: 47, rating: '4.9', exp: '3 năm', reply: '< 24 giờ'},
    packages: [
      {name: 'Film Only', price: '8–12 tr', note: 'tùy số cuộn', desc: 'Gói chụp thuần film analog — mỗi khoảnh khắc mang hơi thở của điện ảnh cổ điển.', includes: ['3 giờ chụp', '1–2 cuộn film (36–72 kiểu)', 'Scan & giao file HD', 'Tư vấn phong cách trước chụp'], featured: false},
      {name: 'Documentary Wedding', price: '18–25 tr', note: 'trọn gói', desc: 'Kết hợp film và digital — ghi lại toàn bộ câu chuyện ngày cưới.', includes: ['8 giờ chụp', '2 cuộn film + digital song song', '200+ ảnh digital edit', 'Video highlight 3–5 phút', 'Giao file trong 30 ngày'], featured: true},
      {name: 'Pre + After Party', price: '6–10 tr', note: '3 giờ', desc: 'Chụp buổi tiệc nhỏ trước hoặc sau đám cưới — picnic, brunch với nhóm bạn thân.', includes: ['3 giờ chụp tự nhiên', '100+ ảnh edit', 'Phong cách casual, không dàn dựng'], featured: false},
    ],
    reviews: [
      {name: 'Thảo & Lâm', date: 'Tháng 3, 2025 · Sài Gòn', text: 'Ánh Dương chụp đám cưới nhỏ của tụi mình theo phong cách film — không dàn dựng, không chỉ đạo quá nhiều. Xem lại ảnh mà khóc vì đẹp và chân thật quá.'},
      {name: 'Minh & Hà', date: 'Tháng 1, 2025 · Đà Lạt', text: 'Qua Timeless Harmony thấy có hợp đồng rõ ràng nên mạnh dạn đặt cọc. Kết quả vượt mong đợi — ảnh có hồn, video highlight làm mình xem đi xem lại mãi.'},
    ],
    available: 'Tháng 6, 2026', thumb: ['#1a231c','#221c14','#14202a'],
  },

  'van-huong-studio': {
    name: 'Vân Hương Studio',
    cat: 'photo', catLabel: 'Nhiếp ảnh & Quay phim',
    city: 'Đà Nẵng · Hội An', cityFull: 'Đà Nẵng — hoạt động miền Trung',
    styles: ['Documentary', 'Phim tài liệu', 'Candid', 'Outdoor'],
    about: 'Vân Hương Studio ghi lại đám cưới như một bộ phim tài liệu ngắn — không pose, không chỉ đạo, chỉ quan sát và chụp những khoảnh khắc thật nhất. Phong cách này đặc biệt phù hợp với đám cưới ngoài trời và destination wedding.',
    about2: 'Được biết đến với khả năng chụp trong ánh sáng vàng (golden hour) và các điều kiện ánh sáng tự nhiên khác nhau.',
    stats: {deals: 55, rating: '4.8', exp: '5 năm', reply: '< 12 giờ'},
    packages: [
      {name: 'Candid Story', price: '10–15 tr', note: 'nửa ngày', desc: 'Ghi lại câu chuyện ngày cưới theo phong cách candid thuần túy.', includes: ['5 giờ chụp', '150+ ảnh edit', 'Gallery online trong 3 tuần'], featured: false},
      {name: 'Full Documentary', price: '20–30 tr', note: 'trọn ngày', desc: 'Bộ phim tài liệu về ngày cưới của bạn — từ sáng đến đêm.', includes: ['Trọn ngày (10–12 giờ)', '300+ ảnh edit', 'Video documentary 8–12 phút', 'Raw footage bàn giao', 'Album photobook 30 trang'], featured: true},
      {name: 'GoPro Add-on', price: '4–6 tr', note: 'bổ sung', desc: 'Gắn thêm GoPro góc nhìn thứ nhất — cảm giác như người trong cuộc.', includes: ['1 GoPro gắn cố định', 'Edit highlights 3 phút', 'Bổ sung vào bất kỳ gói nào'], featured: false},
    ],
    reviews: [
      {name: 'Trúc & Hiếu', date: 'Tháng 2, 2025 · Hội An', text: 'Destination wedding của tụi mình ở Hội An với 25 khách. Vân Hương bắt được từng ánh mắt, từng nụ cười một cách tự nhiên đến mức quên mất có người đang chụp.'},
      {name: 'Mai & Bảo', date: 'Tháng 11, 2024 · Đà Nẵng', text: 'Video documentary 10 phút của tụi mình được gia đình xem đi xem lại. Không có bài nhạc chỉnh sửa giả tạo — chỉ có âm thanh thật và cảm xúc thật.'},
    ],
    available: 'Tháng 5, 2026', thumb: ['#14202a','#1a1e24','#202428'],
  },

  'khoi-film': {
    name: 'Khói Film Studio',
    cat: 'photo', catLabel: 'Nhiếp ảnh & Quay phim',
    city: 'Sài Gòn', cityFull: 'Sài Gòn — hoạt động toàn quốc',
    styles: ['Cinematic', 'Moody', 'Dark & Dramatic', 'Tối giản'],
    about: 'Khói Film chuyên về cinematic wedding videography — mỗi video là một short film với nhân vật chính là cặp đôi của bạn. Sử dụng thiết bị điện ảnh chuyên nghiệp và kỹ thuật dựng phim nâng cao.',
    about2: 'Đặc biệt yêu thích những cảnh quay trong ánh sáng tự nhiên, khói, và các yếu tố nghệ thuật. Phù hợp cho cặp đôi muốn video cưới có chiều sâu điện ảnh.',
    stats: {deals: 34, rating: '4.9', exp: '4 năm', reply: '< 24 giờ'},
    packages: [
      {name: 'Short Film', price: '12–18 tr', note: '5 phút', desc: 'Short film 5 phút kể câu chuyện ngày cưới của bạn.', includes: ['6 giờ quay', 'Short film 5 phút', '1 bài nhạc licensed', 'Colour grade chuyên nghiệp'], featured: false},
      {name: 'Cinema Wedding', price: '25–38 tr', note: 'trọn gói', desc: 'Trải nghiệm điện ảnh đầy đủ — từ quay đến dựng phim.', includes: ['Trọn ngày quay (10 giờ)', 'Phim chính 8–12 phút', 'Highlight reel 2 phút cho mạng xã hội', 'Drone shot (nếu địa điểm cho phép)', 'Colour grade + Sound design'], featured: true},
      {name: 'Same Day Edit', price: '8–12 tr', note: 'bổ sung', desc: 'Video highlight chiếu ngay trong đêm tiệc cưới — khoảnh khắc wow nhất.', includes: ['Dựng video tại chỗ trong 2–3 giờ', 'Video 2–3 phút', 'Chiếu trực tiếp tại tiệc', 'Bổ sung vào Cinema Wedding'], featured: false},
    ],
    reviews: [
      {name: 'Yến & Toàn', date: 'Tháng 3, 2025 · Sài Gòn', text: 'Tụi mình muốn video cưới khác hoàn toàn với cái kiểu nhạc to ầm ĩ thông thường. Khói Film làm ra một short film mà mình tự hào mang đi show mọi người.'},
      {name: 'Ngọc & Phát', date: 'Tháng 1, 2025 · Đà Lạt', text: 'Same day edit là highlight của đêm tiệc — khách mời ồ lên khi thấy video được chiếu. Xứng đáng từng đồng.'},
    ],
    available: 'Tháng 7, 2026', thumb: ['#1e1a14','#18161e','#201e1a'],
  },

  // ── 3. HOA CƯỚI & TRANG TRÍ ──
  'bloom-petal': {
    name: 'Bloom & Petal',
    cat: 'flower', catLabel: 'Hoa cưới & Trang trí',
    city: 'Hội An', cityFull: 'Hội An — ship toàn quốc',
    styles: ['Bohemian', 'Garden', 'Wildflower', 'Romantic'],
    about: 'Bloom & Petal thiết kế hoa cưới theo phong cách vườn tự nhiên — không đối xứng, không cứng nhắc, chỉ có sự chảy tràn tự nhiên của hoa dại và lá xanh. Sử dụng 100% hoa tươi theo mùa từ vườn địa phương.',
    about2: 'Đặc biệt yêu thích các thiết kế hoa cho đám cưới ngoài trời và intimate wedding dưới 60 khách.',
    stats: {deals: 83, rating: '4.9', exp: '5 năm', reply: '< 24 giờ'},
    packages: [
      {name: 'Bridal Basics', price: '3–5 tr', note: 'hoa cô dâu', desc: 'Hoa cầm tay cô dâu và phụ kiện hoa cơ bản cho ngày cưới.', includes: ['Hoa cầm tay cô dâu', 'Hoa gài áo chú rể', 'Hoa cho 2 phù dâu', 'Tư vấn màu sắc & phong cách'], featured: false},
      {name: 'Garden Party', price: '12–20 tr', note: 'trọn gói hoa', desc: 'Hoa cô dâu và trang trí không gian tiệc theo phong cách vườn.', includes: ['Hoa cầm tay + phụ kiện cô dâu', 'Backdrop hoa lễ cưới', 'Trang trí 5–8 bàn tiệc', 'Hoa trang trí lối đi', 'Setup & thu dọn'], featured: true},
      {name: 'Full Bloom', price: '25–40 tr', note: 'trang trí toàn bộ', desc: 'Trang trí hoa toàn bộ không gian — từ cổng vào đến từng góc nhỏ.', includes: ['Toàn bộ Garden Party', 'Cổng hoa chào', 'Hoa treo & đèn', 'Photo corner', 'Hoa tươi cho bàn tiếp khách'], featured: false},
    ],
    reviews: [
      {name: 'Hương & Nam', date: 'Tháng 4, 2025 · Hội An', text: 'Bloom & Petal biến sân vườn nhỏ của villa thành một khu vườn cổ tích thật sự. Tụi mình chỉ nói muốn "wildflower, không quá cứng" và họ hiểu hoàn toàn.'},
      {name: 'Lan & Đức', date: 'Tháng 2, 2025 · Đà Nẵng', text: 'Hoa cầm tay đẹp hơn cả mình tưởng tượng — tự nhiên, chảy tràn, rất phù hợp với phong cách boho của đám cưới. Ship từ Hội An vào Đà Nẵng vẫn tươi nguyên.'},
    ],
    available: 'Tháng 5, 2026', thumb: ['#1a2218','#221a1c','#1c2218'],
  },

  'studio-xanh-decor': {
    name: 'Studio Xanh Decor',
    cat: 'flower', catLabel: 'Hoa cưới & Trang trí',
    city: 'Sài Gòn', cityFull: 'Sài Gòn — Bình Dương',
    styles: ['Minimalist', 'Modern', 'Monochrome', 'Luxury'],
    about: 'Studio Xanh chuyên thiết kế không gian cưới theo phong cách tối giản hiện đại — ít hoa nhưng đắt giá, ít màu sắc nhưng có chiều sâu. Chúng tôi tin rằng vẻ đẹp thật sự đến từ sự tiết chế.',
    about2: 'Phù hợp cho những cặp đôi yêu thích phong cách editorial và muốn không gian cưới trông như một trang tạp chí.',
    stats: {deals: 41, rating: '4.8', exp: '3 năm', reply: '< 12 giờ'},
    packages: [
      {name: 'Minimal Touch', price: '5–8 tr', note: 'hoa cô dâu', desc: 'Hoa cưới tối giản — ít nhưng tinh, mỗi cành đều có lý do tồn tại.', includes: ['Hoa cầm tay single-stem hoặc cascading', 'Boutonnière chú rể', 'Phụ kiện hoa cài tóc'], featured: false},
      {name: 'Editorial Space', price: '18–28 tr', note: 'không gian tiệc', desc: 'Trang trí không gian theo phong cách editorial — mỗi góc đều là một bức ảnh.', includes: ['Backdrop tối giản cao cấp', 'Centerpiece 8–10 bàn', 'Greenery & sculptural elements', 'Điều phối setup ngày cưới'], featured: true},
      {name: 'Full Monochrome', price: '35–55 tr', note: 'toàn không gian', desc: 'Không gian đơn sắc hoàn toàn — một màu duy nhất, nhiều tone và texture.', includes: ['Toàn bộ Editorial Space', 'Cổng & lối đi monochrome', 'Bảng menu & seating chart', 'Nến & đèn trang trí'], featured: false},
    ],
    reviews: [
      {name: 'Tú & Khoa', date: 'Tháng 3, 2025 · Sài Gòn', text: 'Mình muốn đám cưới trắng đen hoàn toàn — nghe có vẻ lạ nhưng Studio Xanh làm ra thứ gì đó cực kỳ đẹp và sang trọng. Ảnh chụp ra trông như editorial thật sự.'},
      {name: 'Vi & Quân', date: 'Tháng 1, 2025 · Sài Gòn', text: 'Centerpiece trên bàn tiệc là thứ khách mời nhắc đến nhiều nhất. Không phải hoa nhiều mà là hoa đúng — mỗi cành đều có câu chuyện riêng.'},
    ],
    available: 'Tháng 6, 2026', thumb: ['#1e201e','#1a1e1a','#202220'],
  },

  'petite-blooms': {
    name: 'Petite Blooms',
    cat: 'flower', catLabel: 'Hoa cưới & Trang trí',
    city: 'Đà Lạt', cityFull: 'Đà Lạt — ship toàn quốc',
    styles: ['Vintage', 'Romantic', 'Pastel', 'Cottage'],
    about: 'Petite Blooms sử dụng hoa trực tiếp từ vườn Đà Lạt — tươi nhất, đa dạng nhất, và rẻ hơn nhiều so với hoa nhập. Chuyên thiết kế cho đám cưới vintage và romantic với tông màu pastel.',
    about2: 'Đặc biệt mạnh về hoa hướng dương, cúc họa mi, lavender và các loài hoa đặc trưng của Đà Lạt.',
    stats: {deals: 67, rating: '4.9', exp: '6 năm', reply: '< 24 giờ'},
    packages: [
      {name: 'Đà Lạt Bloom', price: '2–4 tr', note: 'hoa cô dâu', desc: 'Hoa cưới từ vườn Đà Lạt — tươi, thơm, và mang hơi thở cao nguyên.', includes: ['Hoa cầm tay thiết kế riêng', 'Boutonnière chú rể', 'Hoa cài tóc cô dâu'], featured: false},
      {name: 'Cottage Garden', price: '8–15 tr', note: 'trọn gói', desc: 'Đám cưới cottage với hoa Đà Lạt — ấm áp, thơm ngát, cổ điển.', includes: ['Hoa cô dâu đầy đủ', 'Trang trí bàn tiệc vintage', 'Floral arch hoặc backdrop', 'Hoa tươi trang trí cổng'], featured: true},
      {name: 'Full Garden', price: '18–28 tr', note: 'toàn bộ', desc: 'Trang trí toàn bộ không gian với hoa tươi từ vườn Đà Lạt.', includes: ['Toàn bộ Cottage Garden', 'Trang trí từng góc không gian', 'Hoa treo chandelier', 'Flower wall cho photobooth'], featured: false},
    ],
    reviews: [
      {name: 'Ngọc & Minh', date: 'Tháng 4, 2025 · Đà Lạt', text: 'Cưới ở Đà Lạt mà dùng hoa Đà Lạt — Petite Blooms biến ý tưởng đó thành hiện thực đẹp hơn mình mơ. Hoa tươi và thơm suốt cả ngày.'},
      {name: 'Phúc & Uyên', date: 'Tháng 12, 2024 · Sài Gòn', text: 'Ship từ Đà Lạt vào Sài Gòn vẫn tươi nguyên nhờ đóng gói kỹ. Giá rất hợp lý cho chất lượng này — không thể tìm được ở nơi khác.'},
    ],
    available: 'Tháng 5, 2026', thumb: ['#20181c','#1e1820','#22181e'],
  },

  // ── 4. LÀM ĐẸP & TRANG PHỤC ──
  'luna-bridal': {
    name: 'Luna Bridal Studio',
    cat: 'beauty', catLabel: 'Làm đẹp & Trang phục',
    city: 'Sài Gòn', cityFull: 'Sài Gòn — phục vụ tại chỗ',
    styles: ['Tinh tế', 'Tự nhiên', 'Glow', 'Editorial'],
    about: 'Luna Bridal Studio chuyên makeup và làm tóc cho cô dâu theo phong cách natural glow — tôn vẻ đẹp thật của từng người thay vì che đi. Sử dụng 100% sản phẩm cao cấp an toàn cho da.',
    about2: 'Đặc biệt có kinh nghiệm với các cô dâu có da nhạy cảm và các điều kiện thời tiết ngoài trời khắc nghiệt.',
    stats: {deals: 120, rating: '4.9', exp: '6 năm', reply: '< 12 giờ'},
    packages: [
      {name: 'Bridal Glow', price: '2–3.5 tr', note: 'makeup + tóc', desc: 'Makeup và làm tóc cô dâu theo phong cách natural glow.', includes: ['Makeup cô dâu', 'Làm tóc cô dâu', 'Chăm sóc da trước makeup', 'Touch-up kit'], featured: false},
      {name: 'Full Bridal', price: '4–6 tr', note: 'cô dâu + 2 phù dâu', desc: 'Gói đầy đủ cho cô dâu và đội hình phù dâu.', includes: ['Makeup + tóc cô dâu', 'Makeup 2 phù dâu', 'Nail cô dâu', 'Lông mi tự nhiên', 'Có mặt tại địa điểm'], featured: true},
      {name: 'Pre-wedding Glam', price: '1.5–2.5 tr', note: 'chụp pre-wed', desc: 'Makeup nhẹ và tự nhiên cho buổi chụp ảnh pre-wedding.', includes: ['Makeup pre-wedding', 'Làm tóc sóng nhẹ', 'Phù hợp outdoor & indoor'], featured: false},
    ],
    reviews: [
      {name: 'Trang & Hùng', date: 'Tháng 4, 2025 · Sài Gòn', text: 'Mình có da dầu và rất lo makeup sẽ trôi. Luna dùng kỹ thuật setting đặc biệt và mình beautiful từ 6 giờ sáng đến 11 giờ đêm không cần touch-up nhiều.'},
      {name: 'Như & Việt', date: 'Tháng 2, 2025 · Sài Gòn', text: 'Cưới ngoài trời 35 độ mà makeup vẫn đẹp trong suốt ngày. Luna chụp ảnh check lại liên tục và touch-up kịp thời — rất chuyên nghiệp.'},
    ],
    available: 'Tháng 6, 2026', thumb: ['#201820','#1e1c20','#22202a'],
  },

  'ao-cuoi-mai-linh': {
    name: 'Áo Cưới Mai Linh',
    cat: 'beauty', catLabel: 'Làm đẹp & Trang phục',
    city: 'Sài Gòn', cityFull: 'Sài Gòn',
    styles: ['Cổ điển', 'A-line', 'Mermaid', 'Việt phục'],
    about: 'Áo Cưới Mai Linh chuyên may và cho thuê váy cưới theo đơn đặt hàng riêng — không có gì là "off-the-rack". Mỗi váy được đo may theo đúng số đo và phong cách của cô dâu.',
    about2: 'Đặc biệt mạnh về váy A-line cổ điển, mermaid và áo dài cưới. Có thêm dịch vụ cho thuê vest chú rể cao cấp.',
    stats: {deals: 95, rating: '4.8', exp: '8 năm', reply: '< 24 giờ'},
    packages: [
      {name: 'Thuê Váy', price: '3–6 tr', note: 'thuê 2 ngày', desc: 'Thuê váy cưới từ bộ sưu tập — đủ size và phong cách.', includes: ['Chọn váy từ 50+ mẫu', 'Chỉnh sửa vừa người', 'Thuê 2 ngày', 'Bảo hiểm váy'], featured: false},
      {name: 'May Riêng', price: '8–18 tr', note: 'đặt may theo yêu cầu', desc: 'Váy cưới may riêng theo số đo và phong cách của cô dâu.', includes: ['Tư vấn phong cách', '3 buổi đo thử', 'Chất liệu cao cấp', 'Hoàn thiện trong 60 ngày', 'Chỉnh sửa không giới hạn'], featured: true},
      {name: 'Combo Cô Dâu Chú Rể', price: '6–12 tr', note: 'thuê đầy đủ', desc: 'Thuê váy + vest đồng bộ cho cả hai — không phải lo phối màu.', includes: ['Váy cưới cho cô dâu', 'Vest + sơ mi + phụ kiện cho chú rể', 'Áo dài phụ cho nghi lễ', 'Chỉnh sửa vừa người'], featured: false},
    ],
    reviews: [
      {name: 'Duyên & Phong', date: 'Tháng 3, 2025 · Sài Gòn', text: 'May váy riêng tại Mai Linh là quyết định đúng nhất — chiếc váy vừa như đúc, không cần kéo hay sợi hay bất kỳ thứ gì. Tự tin từ sáng đến tối.'},
      {name: 'Hồng & Thắng', date: 'Tháng 1, 2025 · Sài Gòn', text: 'Thuê combo cho cả hai tiết kiệm được kha khá mà vẫn đẹp và đồng bộ. Staff ở đây rất tận tâm tư vấn.'},
    ],
    available: 'Tháng 5, 2026', thumb: ['#221e20','#201e22','#1e1e22'],
  },

  'spa-trinh-nguyen': {
    name: 'Spa Trinh Nguyễn',
    cat: 'beauty', catLabel: 'Làm đẹp & Trang phục',
    city: 'Sài Gòn · Bình Dương', cityFull: 'Sài Gòn — Bình Dương',
    styles: ['Skincare', 'Chăm sóc da', 'Nail', 'Wax'],
    about: 'Spa Trinh Nguyễn chuyên về chăm sóc da và làm đẹp toàn thân cho cô dâu trong giai đoạn 3 tháng trước ngày cưới. Mỗi liệu trình được thiết kế riêng theo tình trạng da của từng người.',
    about2: 'Đặc biệt hiệu quả với các vấn đề da như thâm, mụn, da xỉn màu. Được nhiều cô dâu tin tưởng sau khi thấy kết quả rõ rệt.',
    stats: {deals: 200, rating: '4.9', exp: '7 năm', reply: '< 12 giờ'},
    packages: [
      {name: 'Bridal Glow 1 tháng', price: '3–5 tr', note: '4 buổi', desc: 'Liệu trình chăm sóc da 1 tháng trước ngày cưới.', includes: ['4 buổi facial chuyên sâu', 'Mask tươi mỗi buổi', 'Skincare routine tư vấn riêng', 'Sản phẩm chăm sóc tại nhà'], featured: false},
      {name: 'Bridal Package 3 tháng', price: '8–12 tr', note: '12 buổi', desc: 'Liệu trình 3 tháng — da đẹp từ từ, bền lâu.', includes: ['12 buổi facial', 'Wax toàn thân 2 lần', 'Chăm sóc nail 2 lần', 'Massage thư giãn 4 lần', 'Tư vấn dinh dưỡng cơ bản'], featured: true},
      {name: 'Wedding Day Ready', price: '1.5–2.5 tr', note: '1 ngày trước cưới', desc: 'Chăm sóc toàn diện ngay ngày trước đám cưới.', includes: ['Facial làm sạch sâu', 'Mask dưỡng ẩm cao cấp', 'Nail ngày cưới', 'Lông mày & lông mi'], featured: false},
    ],
    reviews: [
      {name: 'Quỳnh & Bình', date: 'Tháng 4, 2025 · Sài Gòn', text: 'Làm liệu trình 3 tháng và kết quả rõ ràng từ tháng đầu. Ngày cưới không cần foundation nhiều mà da vẫn căng bóng. Makeup artist cũng khen da tốt.'},
      {name: 'Thủy & Hải', date: 'Tháng 2, 2025 · Bình Dương', text: 'Không ngờ 3 tháng có thể thay đổi da nhiều đến vậy. Mụn và thâm giảm rõ rệt. Mình chỉ ước biết sớm hơn để bắt đầu sớm hơn.'},
    ],
    available: 'Tháng 5, 2026', thumb: ['#1e2022','#20221e','#1e1e22'],
  },

  // ── 5. ÂM NHẠC & GIẢI TRÍ ──
  'moc-band': {
    name: 'Mộc Band',
    cat: 'music', catLabel: 'Âm nhạc & Giải trí',
    city: 'Hà Nội', cityFull: 'Hà Nội — hoạt động toàn quốc',
    styles: ['Acoustic', 'Jazz', 'Indie', 'Chill'],
    about: 'Mộc Band là ban nhạc acoustic jazz với 5 thành viên — guitar, violin, piano, bass và vocal. Chuyên biểu diễn nhạc sống cho đám cưới intimate với âm thanh ấm áp, không ồn ào, phù hợp cho buổi tiệc thân mật.',
    about2: 'Repertoire đa dạng từ jazz cổ điển đến pop Việt Nam và international hits. Có thể học bài theo yêu cầu.',
    stats: {deals: 58, rating: '4.9', exp: '5 năm', reply: '< 12 giờ'},
    packages: [
      {name: 'Cocktail Set', price: '6–8 tr', note: '2 giờ', desc: 'Nhạc nền acoustic cho giờ cocktail và đón khách.', includes: ['2 giờ biểu diễn', '3 nhạc công', 'Setup & soundcheck', 'Playlist tùy chỉnh theo yêu cầu'], featured: false},
      {name: 'Full Wedding', price: '12–18 tr', note: 'trọn buổi tiệc', desc: 'Âm nhạc sống cho toàn bộ buổi tiệc — từ đón khách đến tạm biệt.', includes: ['5 giờ biểu diễn', '5 nhạc công đầy đủ', '2 bài hát đặc biệt theo yêu cầu', 'Nhạc nền giữa các tiết mục', 'MC nhẹ cho các khoảnh khắc quan trọng'], featured: true},
      {name: 'First Dance Song', price: '2–3 tr', note: 'bổ sung', desc: 'Học và biểu diễn bài hát đặc biệt của cặp đôi — live, không có bản thu sẵn.', includes: ['Học bài theo yêu cầu', 'Biểu diễn live cho first dance', 'Tập thử với cặp đôi trước ngày cưới'], featured: false},
    ],
    reviews: [
      {name: 'Lan & Minh', date: 'Tháng 3, 2025 · Hà Nội', text: 'Mộc Band chơi "Can\'t Help Falling in Love" bằng violin và guitar cho first dance — cả phòng im lặng nghe. Đó là khoảnh khắc đẹp nhất trong đám cưới của tụi mình.'},
      {name: 'Thư & Dũng', date: 'Tháng 1, 2025 · Sài Gòn', text: 'Bay vào Sài Gòn chơi cho đám cưới 40 người của tụi mình. Chuyên nghiệp từ soundcheck đến tiết mục cuối — không một lỗi kỹ thuật nào.'},
    ],
    available: 'Tháng 6, 2026', thumb: ['#1a1e22','#181e20','#1c2022'],
  },

  'nha-acoustic': {
    name: 'Nhã Acoustic',
    cat: 'music', catLabel: 'Âm nhạc & Giải trí',
    city: 'Sài Gòn', cityFull: 'Sài Gòn — Đồng Nai',
    styles: ['Acoustic', 'Chill', 'Ballad', 'Pop Việt'],
    about: 'Nhã Acoustic là duo guitar và vocal — âm thanh tối giản, cảm xúc tối đa. Chuyên các bài ballad Việt và acoustic cover nhạc quốc tế. Phù hợp cho đám cưới nhỏ muốn không khí ấm áp, thân mật.',
    about2: 'Không cần hệ thống âm thanh lớn — duo có thể biểu diễn hoàn toàn acoustic cho không gian nhỏ dưới 50 người.',
    stats: {deals: 42, rating: '4.8', exp: '3 năm', reply: '< 24 giờ'},
    packages: [
      {name: 'Acoustic Set', price: '3–5 tr', note: '2 giờ', desc: 'Biểu diễn acoustic thuần — không cần amp, không cần setup phức tạp.', includes: ['2 giờ biểu diễn', 'Guitar + vocal', 'Phù hợp không gian nhỏ ≤50 người', '10+ bài theo yêu cầu'], featured: false},
      {name: 'Extended Set', price: '5–8 tr', note: '4 giờ', desc: 'Biểu diễn suốt buổi tiệc với nhạc nền giữa các tiết mục.', includes: ['4 giờ biểu diễn', 'Playlist acoustic background', '2 bài hát đặc biệt theo yêu cầu', 'Có thể thêm cajon percussion'], featured: true},
      {name: 'Wedding Song', price: '1–2 tr', note: 'bổ sung', desc: 'Học và biểu diễn 1 bài hát đặc biệt của cặp đôi.', includes: ['Học bài theo yêu cầu', 'Biểu diễn live', 'Tập thử 1 lần trước'], featured: false},
    ],
    reviews: [
      {name: 'Linh & Tuấn', date: 'Tháng 2, 2025 · Sài Gòn', text: 'Cưới rooftop 30 người không có amp vẫn nghe rõ và đẹp — Nhã Acoustic hoàn toàn acoustic mà vẫn đủ âm lượng. Không khí cực kỳ intimate.'},
      {name: 'Châu & Huy', date: 'Tháng 12, 2024 · Sài Gòn', text: 'Họ học bài "Cô Ấy" theo yêu cầu và hát trong lúc mình bước vào. Khoảnh khắc đó tụi mình sẽ không bao giờ quên.'},
    ],
    available: 'Tháng 5, 2026', thumb: ['#181c20','#1a1c1e','#1c1e22'],
  },

  'dj-soleil': {
    name: 'DJ Soleil',
    cat: 'music', catLabel: 'Âm nhạc & Giải trí',
    city: 'Sài Gòn', cityFull: 'Sài Gòn — toàn quốc',
    styles: ['DJ', 'Electronic', 'House', 'Chill vibes'],
    about: 'DJ Soleil chuyên set nhạc cho đám cưới intimate muốn không khí sôi động nhưng không ồn ào. Phong cách mix độc đáo — chill house, indie dance, và tropical beats phù hợp cho tiệc ngoài trời.',
    about2: 'Không chỉ DJ mà còn tư vấn playlist cho toàn bộ ngày cưới — từ nhạc nền đám cưới đến after party.',
    stats: {deals: 33, rating: '4.9', exp: '4 năm', reply: '< 12 giờ'},
    packages: [
      {name: 'Chill Set', price: '4–6 tr', note: '3 giờ', desc: 'DJ set chill cho cocktail hour và dinner — không quá sôi động.', includes: ['3 giờ DJ set', 'Equipment cơ bản', 'Playlist tùy chỉnh', 'Chill house & lounge vibes'], featured: false},
      {name: 'Party Mode', price: '8–12 tr', note: '5 giờ', desc: 'DJ set trọn buổi — từ dinner đến after party.', includes: ['5 giờ DJ set', 'Equipment đầy đủ (loa, đèn LED)', 'Playlist theo từng giai đoạn', 'Read the crowd & adjust live', 'Mic cho MC'], featured: true},
      {name: 'Playlist Consult', price: '500k', note: 'tư vấn', desc: 'Tư vấn và xây dựng playlist cho toàn bộ ngày cưới — không cần thuê DJ.', includes: ['Playlist ceremony', 'Playlist cocktail', 'Playlist dinner', 'Playlist after party', 'File nhạc licensed'], featured: false},
    ],
    reviews: [
      {name: 'An & Duy', date: 'Tháng 3, 2025 · Sài Gòn', text: 'DJ Soleil đọc không khí cực tốt — biết khi nào cần chill, khi nào đẩy lên. After party của đám cưới 40 người mà sôi hơn cả bar.'},
      {name: 'Tú & Bảo', date: 'Tháng 1, 2025 · Sài Gòn', text: 'Thuê tư vấn playlist 500k là deal tốt nhất tụi mình từng làm. Cả ngày cưới có nhạc mượt mà, không bị hở hay trùng lặp.'},
    ],
    available: 'Tháng 6, 2026', thumb: ['#1e1a20','#20181e','#221a22'],
  },

  // ── 6. ẨM THỰC & ĐỒ UỐNG ──
  'garden-table': {
    name: 'Garden Table Catering',
    cat: 'food', catLabel: 'Ẩm thực & Đồ uống',
    city: 'Hội An · Đà Nẵng', cityFull: 'Hội An — Đà Nẵng',
    styles: ['Picnic', 'Farm-to-table', 'Buffet ngoài trời', 'Plated'],
    about: 'Garden Table chuyên catering cho đám cưới intimate ngoài trời — từ picnic style đến plated dinner trang trọng. Nguyên liệu 100% từ nông trại địa phương, menu thay đổi theo mùa.',
    about2: 'Phù hợp cho tiệc cưới từ 20–80 khách, đặc biệt xuất sắc với format buffet ngoài trời và grazing table.',
    stats: {deals: 45, rating: '4.8', exp: '4 năm', reply: '< 24 giờ'},
    packages: [
      {name: 'Picnic Style', price: '180–250k/khách', note: 'tối thiểu 20 khách', desc: 'Tiệc picnic thoải mái — khách ngồi đất, thảm, đệm thay vì bàn ghế.', includes: ['8 món ăn nhẹ', 'Grazing board', 'Đồ uống không cồn', 'Setup thảm & đệm', 'Thu dọn sau tiệc'], featured: false},
      {name: 'Garden Dinner', price: '350–500k/khách', note: 'tối thiểu 20 khách', desc: 'Tiệc tối ngoài vườn với bàn ghế trang trọng và menu 4 món.', includes: ['Menu 4 món theo mùa', 'Bread & amuse-bouche', 'Đồ uống có cồn cơ bản', 'Bàn ghế & décor đơn giản', 'Phục vụ tại bàn'], featured: true},
      {name: 'Grazing Table', price: '3–6 tr', note: 'bổ sung hoặc standalone', desc: 'Bàn thức ăn kiểu Mỹ — pho mát, charcuterie, trái cây, bánh mì thủ công.', includes: ['Grazing table 1.5m x 1m', 'Pho mát nhập khẩu & local', 'Charcuterie & deli meats', 'Trái cây theo mùa', 'Bánh mì thủ công'], featured: false},
    ],
    reviews: [
      {name: 'Hương & Trung', date: 'Tháng 3, 2025 · Hội An', text: 'Garden Table làm tiệc picnic cho đám cưới 25 người của tụi mình dưới tán cây — không có khái niệm nào khác đẹp hơn. Thức ăn ngon và fresh từng món.'},
      {name: 'Quỳnh & Nam', date: 'Tháng 12, 2024 · Đà Nẵng', text: 'Grazing table của họ là điểm nhấn của buổi tiệc — khách mời chụp ảnh suốt. Và quan trọng hơn là ngon thật sự chứ không phải chỉ đẹp.'},
    ],
    available: 'Tháng 5, 2026', thumb: ['#1a2018','#1c221a','#182018'],
  },

  'mobile-bar-vn': {
    name: 'The Wandering Bar',
    cat: 'food', catLabel: 'Ẩm thực & Đồ uống',
    city: 'Sài Gòn', cityFull: 'Sài Gòn — hoạt động toàn quốc',
    styles: ['Cocktail', 'Mocktail', 'Craft bar', 'Mobile'],
    about: 'The Wandering Bar là mobile cocktail bar trên xe gỗ vintage — mang đến trải nghiệm bar craft ngay tại tiệc cưới của bạn. Mỗi cocktail signature được thiết kế riêng cho từng cặp đôi.',
    about2: 'Chuyên tạo signature cocktail và mocktail theo câu chuyện của cặp đôi — có thể đặt tên và thiết kế menu card riêng.',
    stats: {deals: 67, rating: '5.0', exp: '3 năm', reply: '< 12 giờ'},
    packages: [
      {name: 'Signature Duo', price: '5–8 tr', note: '3 giờ', desc: '2 cocktail signature của cặp đôi — phục vụ trong 3 giờ tiệc.', includes: ['2 signature cocktails', '1 mocktail version', '3 giờ phục vụ', 'Bartender có kinh nghiệm', 'Setup xe bar vintage'], featured: false},
      {name: 'Full Bar Experience', price: '10–16 tr', note: '5 giờ', desc: 'Bar experience đầy đủ — từ aperitif đến digestif.', includes: ['4+ loại cocktail signature', 'Full mocktail menu', '5 giờ phục vụ', '2 bartenders', 'Menu card thiết kế riêng', 'Ice sculpture nếu cần'], featured: true},
      {name: 'Coffee & Tea Station', price: '3–5 tr', note: 'bổ sung', desc: 'Trạm cà phê & trà thủ công cho khách không uống rượu.', includes: ['Specialty coffee', 'Hand-brew tea', 'Bánh nhỏ đi kèm', 'Setup trang trí đẹp'], featured: false},
    ],
    reviews: [
      {name: 'Châu & Khánh', date: 'Tháng 4, 2025 · Sài Gòn', text: 'Signature cocktail của tụi mình được đặt tên "First Date" — vị chanh leo và mật ong nhắc đến buổi hẹn đầu tiên ở quán cà phê. Khách mời ai cũng hỏi công thức.'},
      {name: 'Trang & Minh', date: 'Tháng 2, 2025 · Đà Lạt', text: 'Xe bar vintage đỗ giữa vườn hoa Đà Lạt — góc chụp ảnh đẹp nhất của đám cưới luôn. Cocktail ngon và bartender rất thân thiện với khách.'},
    ],
    available: 'Tháng 6, 2026', thumb: ['#201e18','#1e1c18','#221e18'],
  },

  'banh-cuoi-atelier': {
    name: 'Bánh Cưới Atelier',
    cat: 'food', catLabel: 'Ẩm thực & Đồ uống',
    city: 'Sài Gòn · Hà Nội', cityFull: 'Sài Gòn — Hà Nội',
    styles: ['Naked cake', 'Minimalist', 'Floral', 'Tiramisu'],
    about: 'Bánh Cưới Atelier chuyên thiết kế và làm bánh cưới theo đơn đặt hàng — mỗi chiếc bánh là một tác phẩm nghệ thuật được thiết kế riêng theo concept đám cưới. Không có mẫu cố định, mỗi bánh là duy nhất.',
    about2: 'Đặc biệt xuất sắc với naked cake, semi-naked và bánh trang trí hoa tươi. Sử dụng nguyên liệu nhập khẩu và không chất bảo quản.',
    stats: {deals: 89, rating: '4.9', exp: '5 năm', reply: '< 24 giờ'},
    packages: [
      {name: 'Mini Cake', price: '1.5–3 tr', note: '2 tầng, ≤20 phần', desc: 'Bánh cưới nhỏ cho đám cưới intimate — thiết kế riêng, đầy đủ ý nghĩa.', includes: ['2 tầng, ≤20 phần ăn', 'Thiết kế theo concept', 'Hoa tươi hoặc hoa kem', 'Delivery & setup'], featured: false},
      {name: 'Wedding Centerpiece', price: '3–6 tr', note: '3–4 tầng, 30–60 phần', desc: 'Bánh cưới trung tâm — điểm nhấn của không gian tiệc.', includes: ['3–4 tầng theo yêu cầu', 'Thiết kế custom hoàn toàn', 'Hoa tươi hoặc fondant', 'Topper cá nhân hóa', 'Delivery, setup & cake stand'], featured: true},
      {name: 'Dessert Table', price: '5–10 tr', note: 'bàn bánh', desc: 'Bàn bánh ngọt đa dạng — cupcake, macaroon, mini tart và bánh cưới chính.', includes: ['Bánh cưới chính 2 tầng', '24 cupcakes', '24 macaroons', 'Mini tarts', 'Bàn & décor trang trí'], featured: false},
    ],
    reviews: [
      {name: 'Ngọc & Hùng', date: 'Tháng 4, 2025 · Sài Gòn', text: 'Bánh Atelier làm naked cake hoa dại cho đám cưới bohemian của tụi mình — đẹp đến mức mình không nỡ cắt. Và quan trọng là ngon thật, không phải bánh đẹp mà nhạt.'},
      {name: 'My & Khang', date: 'Tháng 2, 2025 · Hà Nội', text: 'Giao bánh từ Sài Gòn ra Hà Nội vẫn hoàn hảo nhờ đóng gói chuyên nghiệp. Dessert table là highlight của buổi tiệc — khách xếp hàng chụp ảnh trước khi lấy bánh.'},
    ],
    available: 'Tháng 5, 2026', thumb: ['#201e18','#221e1a','#1e1c18'],
  },

  // ── 7. ĐỊA ĐIỂM ──
  'the-loft-venue': {
    name: 'The Loft Venue',
    cat: 'venue', catLabel: 'Địa điểm',
    city: 'Đà Lạt', cityFull: 'Đà Lạt, Lâm Đồng',
    styles: ['Industrial', 'Rustic', 'Loft', 'Vintage'],
    about: 'The Loft Venue là không gian loft công nghiệp giữa lòng Đà Lạt — trần cao, gạch mộc, ánh sáng tự nhiên tràn ngập và view thông ra khu vườn xanh mướt. Phù hợp cho đám cưới intimate từ 20–60 khách.',
    about2: 'Địa điểm mang tính linh hoạt cao — có thể setup theo nhiều concept khác nhau từ rustic đến minimalist luxury.',
    stats: {deals: 52, rating: '4.9', exp: '3 năm', reply: '< 12 giờ'},
    packages: [
      {name: 'Loft Half Day', price: '8–12 tr', note: '5 giờ', desc: 'Thuê không gian loft 5 giờ — phù hợp cho tiệc trưa hoặc brunch cưới.', includes: ['5 giờ sử dụng không gian', 'Bàn ghế cơ bản', 'Đèn & điện', 'Bãi đỗ xe'], featured: false},
      {name: 'Full Day Exclusive', price: '18–28 tr', note: 'cả ngày', desc: 'Thuê độc quyền cả ngày — chuẩn bị, tổ chức và thu dọn thoải mái.', includes: ['12 giờ sử dụng', 'Bàn ghế đầy đủ (≤60 khách)', 'Hệ thống ánh sáng', 'Khu vực ngoài vườn', 'Hỗ trợ coordinator tại chỗ'], featured: true},
      {name: 'Garden Only', price: '5–8 tr', note: 'khu vườn ngoài trời', desc: 'Sử dụng riêng khu vườn ngoài trời cho ceremony hoặc cocktail hour.', includes: ['Khu vườn 200m²', '3 giờ sử dụng', 'Ghế ceremony cơ bản', 'Arch chào'], featured: false},
    ],
    reviews: [
      {name: 'Trà & Việt', date: 'Tháng 4, 2025 · Đà Lạt', text: 'The Loft có ánh sáng tự nhiên đẹp nhất mình từng thấy trong bất kỳ venue nào. Đám cưới 40 người của tụi mình diễn ra cả trong nhà lẫn ngoài vườn — hai không gian rất khác nhau nhưng bổ trợ hoàn hảo.'},
      {name: 'Nga & Tuấn', date: 'Tháng 1, 2025 · Đà Lạt', text: 'Venue rustic industrial hiếm có ở Đà Lạt — không phải vintage giả tạo mà là cái gạch mộc, sắt thép thật sự. Ảnh chụp ra cực đẹp không cần chỉnh nhiều.'},
    ],
    available: 'Tháng 7, 2026', thumb: ['#1e2024','#201e1e','#1e1c20'],
  },

  'villa-xanh': {
    name: 'Villa Xanh Đà Lạt',
    cat: 'venue', catLabel: 'Địa điểm',
    city: 'Đà Lạt', cityFull: 'Đà Lạt, Lâm Đồng',
    styles: ['Villa', 'Garden', 'Private', 'Romantic'],
    about: 'Villa Xanh là biệt thự vườn riêng tư tại Đà Lạt — hồ bơi, vườn hoa, view đồi thông và không gian trong nhà đầy đủ. Có thể thuê nguyên villa cho cả đám cưới và lưu trú của khách mời.',
    about2: 'Sức chứa linh hoạt từ 20–80 khách. Đặc biệt phù hợp cho đám cưới kết hợp nghỉ dưỡng — khách mời lưu trú 2–3 ngày.',
    stats: {deals: 38, rating: '5.0', exp: '4 năm', reply: '< 12 giờ'},
    packages: [
      {name: 'Wedding Day', price: '12–18 tr', note: 'chỉ ngày cưới', desc: 'Thuê villa trong ngày cưới — không bao gồm lưu trú qua đêm.', includes: ['8 giờ sử dụng toàn bộ villa', 'Hồ bơi & vườn', 'Bàn ghế cơ bản', 'Bếp để catering sử dụng'], featured: false},
      {name: 'Wedding Weekend', price: '28–45 tr', note: '2 đêm', desc: 'Thuê villa cả cuối tuần — đám cưới thứ 7, khách lưu trú thứ 6 và thứ 7.', includes: ['2 đêm lưu trú (8 phòng ngủ)', 'Toàn bộ không gian villa', 'Hỗ trợ setup & décor', 'Welcome dinner thứ 6 tối', 'Breakfast sáng thứ 7 & CN'], featured: true},
      {name: 'Elopement Package', price: '6–10 tr', note: '4 giờ', desc: 'Cho cặp đôi chỉ muốn chụp ảnh và tổ chức nhỏ tại villa đẹp.', includes: ['4 giờ sử dụng villa + vườn', 'Setup trang trí nhỏ', 'Phù hợp 2–10 người', 'Welcome drinks'], featured: false},
    ],
    reviews: [
      {name: 'Linh & Phong', date: 'Tháng 3, 2025 · Đà Lạt', text: 'Thuê cả cuối tuần và đó là quyết định tốt nhất. Khách mời từ Sài Gòn lên, ở lại 2 đêm, cùng nhau chuẩn bị ngày cưới — cảm giác như một kỳ nghỉ với những người thân nhất.'},
      {name: 'Vy & Khoa', date: 'Tháng 12, 2024 · Đà Lạt', text: 'Hồ bơi với view đồi thông là thứ mình không thể tìm được ở nơi nào khác với giá này. Đám cưới 30 người — ai cũng bảo đây là đám cưới đẹp nhất họ từng dự.'},
    ],
    available: 'Tháng 6, 2026', thumb: ['#182220','#1a2418','#1c2218'],
  },

  'rooftop-saigon': {
    name: 'Rooftop Social',
    cat: 'venue', catLabel: 'Địa điểm',
    city: 'Sài Gòn', cityFull: 'Quận 1, Sài Gòn',
    styles: ['Rooftop', 'Urban', 'Skyline', 'Modern'],
    about: 'Rooftop Social là không gian sân thượng độc quyền tại trung tâm Quận 1 — view toàn cảnh skyline Sài Gòn, không khí thoáng mát và ánh đèn thành phố về đêm. Một trong số ít rooftop được phép tổ chức sự kiện riêng tư tại Sài Gòn.',
    about2: 'Đặc biệt ấn tượng vào buổi tối — sunset và skyline về đêm là background không venue nào có thể thay thế.',
    stats: {deals: 44, rating: '4.8', exp: '2 năm', reply: '< 12 giờ'},
    packages: [
      {name: 'Sunset Ceremony', price: '10–15 tr', note: '3 giờ', desc: 'Lễ cưới lúc hoàng hôn trên rooftop — khoảnh khắc không thể quên.', includes: ['3 giờ sử dụng rooftop', 'Setup ceremony cơ bản', 'Arch & ghế ngồi (≤40 khách)', 'Welcome cocktail'], featured: false},
      {name: 'Night Exclusive', price: '20–32 tr', note: 'tối đến khuya', desc: 'Buổi tối độc quyền trên rooftop — skyline Sài Gòn là backdrop.', includes: ['6 giờ sử dụng (18h–24h)', 'Bàn tiệc đầy đủ (≤60 khách)', 'Hệ thống đèn fairy light', 'Hệ thống âm thanh cơ bản', 'Security & parking'], featured: true},
      {name: 'Cocktail Hour', price: '6–10 tr', note: '2 giờ', desc: 'Cocktail party trên rooftop — format đứng, tự nhiên, sôi động.', includes: ['2 giờ sử dụng', 'Bar setup', '≤80 khách đứng', 'DJ nhạc nền'], featured: false},
    ],
    reviews: [
      {name: 'An & Bình', date: 'Tháng 4, 2025 · Sài Gòn', text: 'Cưới lúc 6 giờ chiều, mặt trời lặn ngay trong lúc trao nhẫn — khoảnh khắc đó không thể diễn tả bằng lời. View skyline Sài Gòn sau đó còn đẹp hơn nữa.'},
      {name: 'Nhi & Quân', date: 'Tháng 2, 2025 · Sài Gòn', text: 'Khách mời 55 người nhưng không ai cảm thấy chật — rooftop thoáng và view đẹp khiến mọi người cứ muốn ra ngoài. After party tự nhiên thôi vì ai cũng không muốn về.'},
    ],
    available: 'Tháng 5, 2026', thumb: ['#1e2028','#201e28','#1c1e26'],
  },

  // ── 8. TRẢI NGHIỆM ĐỘC ĐÁO ──
  'disposable-camera': {
    name: 'Disposable Camera Bar',
    cat: 'unique', catLabel: 'Trải nghiệm độc đáo',
    city: 'Sài Gòn', cityFull: 'Sài Gòn — toàn quốc',
    styles: ['Film', 'Analog', 'Vintage', 'DIY'],
    about: 'Disposable Camera Bar mang đến trải nghiệm chụp ảnh film dùng một lần cho khách mời — không phải photographer chuyên nghiệp chụp mà chính khách mời là người ghi lại những khoảnh khắc tự nhiên và chân thật nhất.',
    about2: 'Sau đám cưới, tất cả máy được thu lại, rửa phim và giao ảnh cho cặp đôi. Đây là bộ ảnh chân thật nhất từ góc nhìn của khách mời.',
    stats: {deals: 29, rating: '5.0', exp: '2 năm', reply: '< 24 giờ'},
    packages: [
      {name: 'Mini Bar', price: '3–5 tr', note: '5 máy', desc: 'Bar 5 máy ảnh film — đủ cho đám cưới ≤30 khách.', includes: ['5 máy Fujifilm Disposable', 'Setup bar + hướng dẫn dùng', 'Thu máy & rửa phim sau đám cưới', 'Scan & giao 150+ ảnh analog'], featured: false},
      {name: 'Full Bar', price: '6–9 tr', note: '10 máy', desc: 'Bar 10 máy — đủ cho 40–60 khách, mỗi bàn 1–2 máy.', includes: ['10 máy Fujifilm Disposable', 'Setup & hướng dẫn khách', 'Card hướng dẫn tại bàn', 'Thu máy & rửa phim', 'Scan 300+ ảnh', 'Handmade photo album giao sau'], featured: true},
      {name: 'Film Lab Add-on', price: '1–2 tr', note: 'bổ sung', desc: 'Rửa & scan film từ máy ảnh cá nhân của khách mời.', includes: ['Nhận phim từ khách mang đến', 'Rửa & scan chất lượng cao', 'Giao file online'], featured: false},
    ],
    reviews: [
      {name: 'Thi & Hoàng', date: 'Tháng 3, 2025 · Sài Gòn', text: 'Bộ ảnh từ disposable camera là thứ tụi mình trân trọng nhất sau đám cưới — không pose, không đèn flash chuyên nghiệp, chỉ có khoảnh khắc thật. Có ảnh tụi mình không biết là đang được chụp.'},
      {name: 'Mai & Bình', date: 'Tháng 1, 2025 · Hội An', text: 'Khách mời thích thú hết — nhiều người lần đầu cầm máy film. Ảnh rửa ra có grain đặc trưng của film rất đẹp, không digital nào làm được.'},
    ],
    available: 'Tháng 5, 2026', thumb: ['#1e1a2e','#201a2a','#1c1828'],
  },

  'live-sketch': {
    name: 'Live Sketch Studio',
    cat: 'unique', catLabel: 'Trải nghiệm độc đáo',
    city: 'Sài Gòn · Hà Nội', cityFull: 'Sài Gòn — Hà Nội',
    styles: ['Live art', 'Ký họa', 'Watercolor', 'Portrait'],
    about: 'Live Sketch Studio cung cấp dịch vụ họa sĩ vẽ trực tiếp tại tiệc cưới — khách mời đến bàn, ngồi xuống, và nhận chân dung ký họa của mình trong vòng 5–10 phút như một món quà đặc biệt.',
    about2: 'Phong cách vẽ đa dạng từ ký họa nhanh đến watercolor chi tiết hơn. Có thể vẽ chân dung cặp đôi hoặc toàn cảnh tiệc cưới.',
    stats: {deals: 22, rating: '5.0', exp: '3 năm', reply: '< 12 giờ'},
    packages: [
      {name: 'Portrait Corner', price: '3–5 tr', note: '3 giờ', desc: 'Họa sĩ ngồi tại một góc — khách mời đến để được vẽ chân dung.', includes: ['1 họa sĩ, 3 giờ', 'Vẽ ký họa nhanh 5–8 phút/người', '25–30 chân dung', 'Giấy & vật liệu'], featured: false},
      {name: 'Duo Artist', price: '6–9 tr', note: '4 giờ', desc: '2 họa sĩ — phục vụ nhiều khách hơn, đồng thời vẽ cặp đôi chính thức hơn.', includes: ['2 họa sĩ, 4 giờ', '40–50 chân dung', 'Vẽ chân dung cặp đôi (watercolor)', 'Framing cho cặp đôi', 'Ký họa toàn cảnh không gian tiệc'], featured: true},
      {name: 'Wedding Portrait', price: '2–4 tr', note: 'chân dung cặp đôi', desc: 'Một tác phẩm watercolor chi tiết về cặp đôi — quà lưu niệm đặc biệt.', includes: ['Vẽ từ ảnh hoặc live', 'Watercolor A3', 'Khung & giao tận nơi', 'Hoàn thiện trong 7 ngày'], featured: false},
    ],
    reviews: [
      {name: 'Dương & Khánh', date: 'Tháng 4, 2025 · Sài Gòn', text: 'Khách mời xếp hàng để được vẽ — không ngờ một "corner" nhỏ lại là highlight của cả buổi tiệc. Nhiều người nói đây là đám cưới duy nhất họ được mang về nhà quà thủ công.'},
      {name: 'Tâm & Phú', date: 'Tháng 2, 2025 · Hà Nội', text: 'Tụi mình có chân dung cặp đôi được vẽ live trong buổi tiệc — treo lên tường phòng ngủ rồi. Đó là thứ không thể mua được bằng bất kỳ dịch vụ nào khác.'},
    ],
    available: 'Tháng 6, 2026', thumb: ['#1a2218','#1c2218','#182218'],
  },

  'booth-360': {
    name: '360° Booth Vietnam',
    cat: 'unique', catLabel: 'Trải nghiệm độc đáo',
    city: 'Sài Gòn', cityFull: 'Sài Gòn — Bình Dương — Đồng Nai',
    styles: ['360°', 'Slow-motion', 'Video', 'Viral'],
    about: '360° Booth Vietnam cung cấp trải nghiệm quay video slow motion 360 độ — khách mời đứng trên platform, máy quay xoay 360 độ trong 10–15 giây, video được overlay text và nhạc rồi gửi ngay qua QR code.',
    about2: 'Video format dọc tối ưu cho Instagram & TikTok — khách mời share ngay tại tiệc. Mỗi video là kỷ niệm duy nhất.',
    stats: {deals: 51, rating: '4.9', exp: '2 năm', reply: '< 12 giờ'},
    packages: [
      {name: 'Standard 360', price: '6–9 tr', note: '4 giờ', desc: 'Booth 360 tiêu chuẩn với overlay template cố định.', includes: ['4 giờ vận hành', 'Máy quay 360 + platform', 'Overlay text & nhạc', 'QR code gửi video instant', 'Kỹ thuật viên tại chỗ'], featured: false},
      {name: 'Premium 360', price: '10–15 tr', note: '6 giờ', desc: 'Booth 360 cao cấp với overlay thiết kế riêng cho đám cưới.', includes: ['6 giờ vận hành', 'Overlay thiết kế custom theo concept', 'Nhạc signature của cặp đôi', 'Confetti cannon option', 'LED arch trang trí', 'Video recap toàn buổi'], featured: true},
      {name: 'Mini Session', price: '3–5 tr', note: '2 giờ', desc: 'Session ngắn cho cocktail hour — tạo không khí vui khi đón khách.', includes: ['2 giờ vận hành', 'Overlay template standard', 'QR gửi video instant', '≤40 lượt quay'], featured: false},
    ],
    reviews: [
      {name: 'Hân & Vũ', date: 'Tháng 3, 2025 · Sài Gòn', text: 'Khách mời quay đến 3–4 lần mỗi người vì thích quá. Video slow motion nhìn cực chất, overlay tên tụi mình thiết kế riêng rất đẹp. Sau đám cưới Instagram của họ hàng toàn video 360.'},
      {name: 'Yến & Lộc', date: 'Tháng 1, 2025 · Sài Gòn', text: 'Thuê cả confetti cannon — khoảnh khắc giấy confetti bay chậm 360 độ đẹp không thể tả. Đó là khoảnh khắc mọi người nhớ mãi.'},
    ],
    available: 'Tháng 5, 2026', thumb: ['#1c1a2a','#1e1828','#201a2a'],
  },

};
