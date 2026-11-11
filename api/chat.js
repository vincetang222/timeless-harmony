// Vercel Edge Function — POST /api/chat
// Proxy giữa trang /ke-hoach và Claude API. System prompt nằm ở server
// để endpoint không bị dùng như một proxy Claude miễn phí cho prompt tùy ý.
// Cần biến môi trường ANTHROPIC_API_KEY trên Vercel.

export const config = { runtime: 'edge' };

const MODEL = 'claude-haiku-5-5';
const MAX_MESSAGES = 20;          // chỉ gửi 20 tin gần nhất
const MAX_CHARS_PER_MESSAGE = 4000;

// Khi thêm/sửa nhà cung cấp trong suppliers.js, cập nhật danh sách này.
// Cột đầu là id dùng cho thẻ [SUPPLIERS:...] — phải khớp key trong suppliers.js.
const SUPPLIER_LIST = `
- y-linh-planner | Ý Linh Planner | Lên kế hoạch cưới | Sài Gòn · Đà Lạt | 3–70tr | Boutique, Tối giản, Luxury
- dam-cuoi-xanh | Đám Cưới Xanh | Lên kế hoạch cưới | Hội An · Đà Nẵng | 5–65tr | Rustic, Garden, Organic
- muse-events | Muse Events | Lên kế hoạch cưới | Sài Gòn | 4–100tr | Luxury, Editorial, Nghệ thuật
- anh-duong-studio | Ánh Dương Studio | Nhiếp ảnh & Quay phim | Sài Gòn | 6–25tr | Film Analog, Vintage, Documentary
- van-huong-studio | Vân Hương Studio | Nhiếp ảnh & Quay phim | Đà Nẵng · Hội An | 4–30tr | Documentary, Candid, Outdoor
- khoi-film | Khói Film Studio | Nhiếp ảnh & Quay phim | Sài Gòn | 8–38tr | Cinematic, Moody, Tối giản
- bloom-petal | Bloom & Petal | Hoa cưới & Trang trí | Hội An | 3–40tr | Bohemian, Garden, Wildflower
- studio-xanh-decor | Studio Xanh Decor | Hoa cưới & Trang trí | Sài Gòn | 5–55tr | Minimalist, Modern, Monochrome
- petite-blooms | Petite Blooms | Hoa cưới & Trang trí | Đà Lạt | 2–28tr | Vintage, Romantic, Pastel
- luna-bridal | Luna Bridal Studio | Làm đẹp & Trang phục | Sài Gòn | 1.5–6tr | Tinh tế, Tự nhiên, Glow
- ao-cuoi-mai-linh | Áo Cưới Mai Linh | Làm đẹp & Trang phục | Sài Gòn | 3–18tr | Cổ điển, A-line, Việt phục
- spa-trinh-nguyen | Spa Trinh Nguyễn | Làm đẹp & Trang phục | Sài Gòn · Bình Dương | 1.5–12tr | Skincare, Nail, Wax
- moc-band | Mộc Band | Âm nhạc & Giải trí | Hà Nội | 2–18tr | Acoustic, Jazz, Indie
- nha-acoustic | Nhã Acoustic | Âm nhạc & Giải trí | Sài Gòn | 1–8tr | Acoustic, Chill, Ballad
- dj-soleil | DJ Soleil | Âm nhạc & Giải trí | Sài Gòn | 500k–12tr | DJ, Electronic, House
- garden-table | Garden Table Catering | Ẩm thực & Đồ uống | Hội An · Đà Nẵng | 180–500k/khách | Picnic, Farm-to-table, Plated
- mobile-bar-vn | The Wandering Bar | Ẩm thực & Đồ uống | Sài Gòn | 3–16tr | Cocktail, Mocktail, Mobile bar
- banh-cuoi-atelier | Bánh Cưới Atelier | Ẩm thực & Đồ uống | Sài Gòn · Hà Nội | 1.5–10tr | Naked cake, Minimalist, Floral
- the-loft-venue | The Loft Venue | Địa điểm | Đà Lạt | 5–28tr | Industrial, Rustic, Loft
- villa-xanh | Villa Xanh Đà Lạt | Địa điểm | Đà Lạt | 6–45tr | Villa, Garden, Private
- rooftop-saigon | Rooftop Social | Địa điểm | Sài Gòn | 6–32tr | Rooftop, Urban, Skyline
- disposable-camera | Disposable Camera Bar | Trải nghiệm độc đáo | Sài Gòn | 1–9tr | Film, Analog, Vintage
- live-sketch | Live Sketch Studio | Trải nghiệm độc đáo | Sài Gòn · Hà Nội | 2–9tr | Live art, Ký họa, Watercolor
- booth-360 | 360° Booth Vietnam | Trải nghiệm độc đáo | Sài Gòn | 3–15tr | 360°, Slow-motion, Video
`.trim();

const SYSTEM_PROMPT = `Bạn là Harmony — trợ lý AI lên kế hoạch cưới của Timeless Harmony, một nền tảng kết nối dịch vụ cưới tại Việt Nam.

NHÂN CÁCH:
- Thân thiện, ấm áp như người bạn thân đã từng tổ chức nhiều đám cưới
- Xưng "mình", gọi người dùng là "bạn" (không dùng "tôi" hay "chúng tôi")
- Trả lời bằng tiếng Việt, ngắn gọn, súc tích; hạn chế emoji

NHIỆM VỤ:
1. Hỏi những thông tin còn thiếu: ngân sách, số khách, khu vực, phong cách, thời gian cưới
2. Lên kế hoạch theo timeline (trước 3 tháng → 2 tháng → 1 tháng → 1 tuần → ngày cưới)
3. Gợi ý phân bổ ngân sách theo hạng mục
4. Gợi ý nhà cung cấp phù hợp từ danh sách bên dưới

DANH SÁCH NHÀ CUNG CẤP (id | tên | hạng mục | khu vực | khoảng giá | phong cách):
${SUPPLIER_LIST}

PHÂN BỔ NGÂN SÁCH THAM KHẢO (đám cưới nhỏ):
- Địa điểm: 25–30%
- Ẩm thực: 25–30%
- Nhiếp ảnh + Quay phim: 15–20%
- Hoa + Trang trí: 10–15%
- Trang phục + Làm đẹp: 8–12%
- Âm nhạc + Giải trí: 5–8%
- Thiệp & văn phòng phẩm: 3–5%
- Dự phòng: 5–10%

ĐỊNH DẠNG ĐẶC BIỆT (giao diện sẽ hiển thị thành thẻ/bảng):
- Khi gợi ý nhà cung cấp, thêm ở cuối tin nhắn: [SUPPLIERS:id1,id2,id3] — chỉ dùng id ở cột đầu của danh sách trên.
- Khi lên timeline, thêm ở cuối tin nhắn: [PLAN:[{"timeline":"Trước 3 tháng","item":"...","status":"pend"}]] — JSON hợp lệ, status là "pend" hoặc "done".
- Chỉ dùng **in đậm** cho định dạng chữ; không dùng tiêu đề markdown (#) hay bảng markdown.

NGUYÊN TẮC:
- Không bịa nhà cung cấp, giá hay khuyến mãi ngoài danh sách trên.
- Nếu khu vực của bạn ấy chưa có nhà cung cấp phù hợp, nói thẳng và gợi ý tiêu chí để tự tìm.
- Luôn nhắc rằng cô dâu chú rể là người quyết định cuối cùng.`;

function json(body, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json; charset=utf-8' },
  });
}

function sanitizeMessages(raw) {
  if (!Array.isArray(raw)) return null;
  const msgs = raw
    .filter(m => m && (m.role === 'user' || m.role === 'assistant') && typeof m.content === 'string')
    .map(m => ({ role: m.role, content: m.content.slice(0, MAX_CHARS_PER_MESSAGE) }))
    .filter(m => m.content.trim() !== '')
    .slice(-MAX_MESSAGES);
  // API yêu cầu bắt đầu bằng user và kết thúc bằng user (model mới không nhận prefill)
  while (msgs.length && msgs[0].role !== 'user') msgs.shift();
  if (!msgs.length || msgs[msgs.length - 1].role !== 'user') return null;
  return msgs;
}

export default async function handler(req) {
  if (req.method !== 'POST') return json({ error: 'Method not allowed' }, 405);

  if (!process.env.ANTHROPIC_API_KEY) {
    // Client sẽ tự chuyển sang chế độ trả lời mẫu
    return json({ error: 'AI chưa được cấu hình' }, 503);
  }

  let body;
  try {
    body = await req.json();
  } catch {
    return json({ error: 'Invalid JSON' }, 400);
  }

  const messages = sanitizeMessages(body?.messages);
  if (!messages) return json({ error: 'Invalid messages' }, 400);

  try {
    const res = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': process.env.ANTHROPIC_API_KEY,
        'anthropic-version': '2023-06-01',
      },
      body: JSON.stringify({
        model: MODEL,
        // Haiku 5.5 bật thinking mặc định và thinking tính vào max_tokens,
        // nên để dư chỗ cho cả phần suy nghĩ lẫn câu trả lời + JSON kế hoạch.
        max_tokens: 4000,
        output_config: { effort: 'low' },
        system: SYSTEM_PROMPT,
        messages,
      }),
    });

    const data = await res.json();

    if (!res.ok) {
      console.error('Anthropic API error', res.status, data?.error?.message);
      return json({ error: 'AI tạm thời không khả dụng' }, 502);
    }

    if (data.stop_reason === 'refusal') {
      return json({
        text: 'Mình không thể hỗ trợ yêu cầu này. Bạn thử hỏi theo cách khác về kế hoạch cưới nhé!',
      });
    }

    // Phản hồi có thể bắt đầu bằng block "thinking" — chỉ lấy các block text
    const text = (data.content || [])
      .filter(b => b.type === 'text')
      .map(b => b.text)
      .join('')
      .trim();

    if (!text) return json({ error: 'Empty response' }, 502);
    return json({ text });
  } catch (err) {
    console.error('Chat handler error', err);
    return json({ error: 'Server error' }, 500);
  }
}
