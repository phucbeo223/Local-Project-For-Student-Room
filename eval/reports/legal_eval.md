# Kết quả kiểm thử chatbot tiền điện

Ngày chạy: 21/09/2026 (Asia/Ho_Chi_Minh). Kho dữ liệu: PDF cục bộ đã OCR,
không dùng đáp án pháp luật viết sẵn làm dữ liệu truy xuất.

## Kết quả

- Backend: **191 kiểm thử đạt**, một cảnh báo deprecation từ thư viện Starlette/AnyIO.
  Chạy bằng `docker-compose.test.yml` với cơ sở dữ liệu thử nghiệm riêng.
- Frontend: `npm run build` thành công, 37 tuyến trang.
- Hai PDF được lập chỉ mục lại bằng `legal-v4`: Nghị định 133/2026 có 392 đoạn,
  Thông tư 60/2025 có 226 đoạn; tổng 72 trang dùng OCR.
- Tìm kiếm kết hợp vector/từ khóa: đạt các kiểm tra của 8/8 tình huống.
- Tìm kiếm chỉ dùng từ khóa: đạt các kiểm tra của 8/8 tình huống.
- Kiểm tra câu trả lời: **8/8 đạt**; 7 câu trả lời trích nguồn trực tiếp
  (`legal-extractive`), 1 câu thông báo thiếu căn cứ (`legal-insufficient`).
  Đây không phải điểm đánh giá khả năng sinh câu trả lời của mô hình Qwen.

| Tình huống | Hành vi đã kiểm tra |
|---|---|
| Chủ trọ thu tiền điện thế nào | Trích giới hạn theo hóa đơn và điều kiện hiệu lực |
| Thu 4.000 đồng/kWh | Yêu cầu đối chiếu hóa đơn/sản lượng, không tự kết luận đúng hoặc sai |
| Ba sinh viên ở chung | Trích định mức 3/4, điều kiện kê khai và hiệu lực |
| Thu cao hơn quy định | Trích mức phạt, hoàn trả và phạm vi mức phạt cá nhân |
| Tiền điện thu thừa | Giữ điều kiện hoàn trả và lãi suất do hai bên thỏa thuận |
| Thuê dưới 12 tháng | Giữ đồng thời điều kiện thời hạn và không kê khai đủ người |
| Thời điểm áp dụng | Trích điều kiện điều chỉnh giá, không tự suy ra ngày |
| Ngân hàng/tài khoản bắt buộc | `no_answer=true`; thiếu căn cứ không đồng nghĩa không có quy định |

Câu hỏi ngân hàng không có điều khoản kỳ vọng: kết quả truy xuất của câu này
không được tính là bằng chứng tìm đúng luật; mục tiêu là kiểm tra khả năng từ chối
kết luận khi chưa có căn cứ.

## Bằng chứng và giới hạn

- [Câu hỏi và tiêu chí](../datasets/legal_electricity_eval.json)
- [Câu trả lời, nguồn và kết quả kiểm tra](legal_generation.json)
- [Kết quả truy xuất kết hợp](legal_retrieval_hybrid.json)
- [Kết quả truy xuất từ khóa](legal_retrieval_lexical.json)
- [Cách chạy lại và kiến trúc](../../docs/LEGAL_RAG_QUALITY.md)

Đã đọc lại tám câu trả lời lưu trong báo cáo, kiểm tra điều kiện hóa đơn, hiệu lực,
lãi suất, phạm vi xử phạt và việc không bịa ngân hàng. Trích đoạn vẫn giữ một số lỗi
chữ OCR như “Bude” hoặc “bán lề”; hệ thống không tự sửa con số pháp lý bằng suy đoán.
Các bài kiểm tra gồm lỗi font, trang chỉ có chữ ký, khoảng tiền đảo ngược, câu tiếp
nối qua trang, nguồn cũ bị hơn 600 đoạn mới lấn át và trích dẫn không hỗ trợ kết luận.

Bộ tám câu là kiểm thử hồi quy cho vấn đề được báo cáo, không đại diện toàn bộ
câu hỏi pháp luật. Kiểm tra tự động dựa vào nguồn, cụm từ và điều kiện; không xác
nhận tính chính xác của mọi ký tự OCR, mức giá hiện hành hoặc sửa đổi ngoài kho.
Các câu hỏi khác vẫn qua mô hình cấu hình và cần được mở rộng đánh giá riêng.
