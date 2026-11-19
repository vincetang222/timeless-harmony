# Quy tắc làm việc (tiết kiệm token)

Áp dụng cho mọi phiên Claude làm việc trong repo này.

## Chọn model

1. Việc hằng ngày chạy **Sonnet**; **Opus** chỉ làm advisor (`.claude/settings.json`: `{"model": "sonnet", "advisorModel": "opus"}`).
2. Chỉ hỏi advisor ở ba lúc: trước khi chốt kế hoạch · khi gặp cùng một lỗi lần thứ hai · trước khi báo xong.
3. Việc khó, rủi ro cao (cơ sở dữ liệu, migration, bảo mật, thanh toán, lỗi khó tìm): `/model opus`. Xong đổi lại Sonnet.
4. **Việc cần thiết kế đẹp** (giao diện, logo, hình nền, bố cục, ấn phẩm): `/model claude-fable-5-2`. Xong đổi lại Sonnet. Trong phiên Fable không cần hỏi advisor; phần cơ học (cập nhật tài liệu, sửa hàng loạt, chạy test) giao agent phụ Sonnet.
5. Tra cứu đơn giản giao agent phụ **Haiku** chỉ đọc (`docs`, `grep`, `search`); agent phụ chỉ trả về kết luận.
6. Lịch chạy tự động dùng Sonnet: prompt ngắn, không hỏi advisor, không mở agent phụ, báo cáo tối đa 15 dòng.

## Khi làm việc

7. Tìm trước, rồi chỉ đọc đoạn cần của tệp lớn. Sửa xong không đọc lại.
8. Việc chỉ mất vài lệnh thì tự làm, không mở agent phụ.
9. Lệnh nào không phụ thuộc nhau thì gửi chung một lượt.
10. Trả lời ngắn, không nhắc lại điều đã chốt.
11. Hội thoại dài thì `/compact`. Luật cần nhớ lâu ghi vào `CLAUDE.md` hoặc `docs/`; giữ `CLAUDE.md` thật ngắn vì nó được nạp ở mọi lượt.
12. Mỗi phiên một vai: một phiên marketing, một phiên vận hành, một phiên thiết kế.
13. Supabase `execute_sql`: mỗi câu SQL một lần gọi.
14. Tệp nháp, ảnh chụp kiểm tra để trong scratchpad, không cho vào repo.
15. Soát giao diện bằng ảnh ghép thu nhỏ (nhiều trang trong một ảnh), không chụp từng trang cỡ lớn.

## Phút GitHub Actions

16. Đẩy lên nhánh làm việc thì không tốn phút. Gom thay đổi thành ít PR. PR chỉ sửa tài liệu thì ghi `[skip ci]` ở commit đầu nhánh và ở commit merge.
