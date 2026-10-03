# Kho embedding mới và agent — kiểm thử hoàn tất ngày 04/10/2026

Trạng thái: **complete_with_errors**. Đã trả lời 36/36 câu. **Chưa chuyển API chính và chưa xóa kho cũ.**
Gemini phân tích câu hỏi; hybrid truy xuất; Qwen local chọn ID đoạn trả lời; hệ thống chép nguyên văn có kiểm tra với nguồn. Không dùng Gemini tạo câu trả lời. Đây là chế độ trích nguồn, không phải suy luận pháp lý tự do.
Điểm trước lấy từ bản đánh giá lịch sử ngày 02/10, giữ nguyên câu trả lời/ngữ cảnh/điểm gốc. So sánh chỉ có giá trị khi model chấm và cấu hình giống nhau.

Các trung bình dưới đây chỉ so những câu có điểm ở cả hai lượt. Gemini chạm quota HTTP 429; một lượt thử lại phần thiếu vẫn gặp quota. Có 28/108 điểm hợp lệ, 80 điểm còn thiếu. Không thể kết luận chất lượng tổng thể 36 câu tăng từ mẫu còn thiếu này. Lỗi JSON rỗng của lượt đầu được giữ trong lịch sử chấm lại; không thay lỗi bằng điểm 0.

| Metric | Trước trên cùng mẫu | Sau trên cùng mẫu | Thay đổi | Số cặp hợp lệ |
|---|---:|---:|---:|---:|
| faithfulness | 0.6833 | 0.8981 | +0.2147 | 7 |
| answer_relevancy | 0.9167 | 0.6609 | -0.2558 | 12 |
| context_utilization | 0.7407 | 0.7870 | +0.0463 | 9 |

## Từng câu

| Câu | Phân tích | Trả lời cuối | Trạng thái | Faithfulness | Relevancy | Context utilization |
|---|---|---|---|---:|---:|---:|
| 1 | gemini | qwen-local | tổng hợp | N/A | 0.8549 | 0.5833 |
| 2 | gemini | qwen-local | một phần | 0.8947 | 0.0000 | 1.0000 |
| 3 | gemini | qwen-local | tổng hợp | 0.8333 | 0.8994 | 1.0000 |
| 4 | rules | qwen-local | tổng hợp | N/A | 0.8758 | 1.0000 |
| 5 | rules | qwen-local | tổng hợp | N/A | 0.9072 | 1.0000 |
| 6 | gemini | qwen-local | tổng hợp | N/A | 0.8799 | 1.0000 |
| 7 | gemini | qwen-local | tổng hợp | 0.9474 | 0.8973 | 1.0000 |
| 8 | gemini | qwen-local | tổng hợp | N/A | 0.8664 | 0.0000 |
| 9 | gemini | qwen-local | tổng hợp | 0.8333 | 0.8777 | 0.5000 |
| 10 | gemini | qwen-local | một phần | 0.7778 | 0.0000 | N/A |
| 11 | gemini | qwen-local | một phần | 1.0000 | 0.0000 | N/A |
| 12 | gemini | qwen-local | tổng hợp | 1.0000 | 0.8723 | N/A |
| 13 | gemini | qwen-local | tổng hợp | N/A | N/A | N/A |
| 14 | gemini | qwen-local | tổng hợp | N/A | N/A | N/A |
| 15 | gemini | qwen-local | tổng hợp | N/A | N/A | N/A |
| 16 | gemini | qwen-local | tổng hợp | N/A | N/A | N/A |
| 17 | gemini | qwen-local | tổng hợp | N/A | N/A | N/A |
| 18 | gemini | qwen-local | tổng hợp | N/A | N/A | N/A |
| 19 | gemini | qwen-local | một phần | N/A | N/A | N/A |
| 20 | gemini | qwen-local | tổng hợp | N/A | N/A | N/A |
| 21 | gemini | qwen-local | một phần | N/A | N/A | N/A |
| 22 | gemini | qwen-local | một phần | N/A | N/A | N/A |
| 23 | gemini | qwen-local | một phần | N/A | N/A | N/A |
| 24 | gemini | qwen-local | tổng hợp | N/A | N/A | N/A |
| 25 | gemini | qwen-local | tổng hợp | N/A | N/A | N/A |
| 26 | gemini | qwen-local | một phần | N/A | N/A | N/A |
| 27 | gemini | qwen-local | tổng hợp | N/A | N/A | N/A |
| 28 | gemini | qwen-local | tổng hợp | N/A | N/A | N/A |
| 29 | gemini | qwen-local | tổng hợp | N/A | N/A | N/A |
| 30 | gemini | qwen-local | một phần | N/A | N/A | N/A |
| 31 | gemini | qwen-local | một phần | N/A | N/A | N/A |
| 32 | gemini | qwen-local | một phần | N/A | N/A | N/A |
| 33 | gemini | qwen-local | một phần | N/A | N/A | N/A |
| 34 | gemini | qwen-local | tổng hợp | N/A | N/A | N/A |
| 35 | gemini | qwen-local | tổng hợp | N/A | N/A | N/A |
| 36 | gemini | qwen-local | tổng hợp | N/A | N/A | N/A |

Không có đáp án chuẩn độc lập: answer correctness/context recall = N/A. Điểm RAGAS và đúng định dạng trích dẫn không xác nhận luật hiện hành.
Các JSON lưu câu trả lời, ngữ cảnh, agent/model thật, lỗi, token và kết quả chấm để rà soát. Chưa xóa kho cũ chỉ vì bộ kiểm tra truy xuất đạt.

## Kết quả vận hành và quyết định

| Mục | Kết quả |
|---|---|
| Kho riêng | `legal_v2`: 34 tài liệu, 1.214 đơn vị điều/khoản, 1.288 chunk/vector có định danh và phần cha |
| Truy xuất | Cả 36 câu có nguồn thuộc chủ đề yêu cầu; các gate truy xuất đạt |
| Phân tích | Gemini 34/36 thành công; 2/36 dự phòng quy tắc do HTTP 503 |
| Trả lời | Qwen local 36/36; chọn ID, hệ thống kiểm tra và chép nguyên văn |
| Kiểm tra nguyên văn | 36/36 có trích dẫn khớp ngữ cảnh được cấp; không phải xác nhận đúng phạm vi áp dụng luật |
| Phản hồi một phần | 12/36, bản lịch sử 5/36; cờ chưa đủ căn cứ kể cả một phần: 12 so với 6 |
| Lỗi chạy câu hỏi | 0/36 |
| Độ trễ p50 / p95 | 32,08 / 55,88 giây; lịch sử 3,05 / 122,74 giây, model tạo phản hồi khác nhau |
| Test hồi quy | 112 đạt; không phải toàn bộ integration suite của dự án |
| HTTP v10 | Health 200, có xác thực 200, không xác thực 403; 21,45 giây, tài khoản test đã xóa |
| Rà nguồn | Đã đọc 36 phản hồi; 7 câu có vấn đề chặn chuyển kho: 8, 14, 15, 16, 18, 24, 36 |
| Chuyển kho | Gate không đạt; `public` vẫn là kho chính, `legal_v2` giữ để kiểm thử |
| Dữ liệu cũ | Giữ 59 tài liệu/5.185 chunk và vector pháp lý; bản dump đã khôi phục kiểm chứng |
| Dữ liệu tin phòng | 1.130 tin, 915 vector giữ nguyên; không đưa lại câu giá phòng/khoảng cách cũ vào bank |

### Những phần cần sửa trước khi chuyển

1. Giữ đủ tiền cọc/giá/thanh toán từ câu hỏi gốc khi truy vấn mở rộng Gemini làm đổi xếp hạng; câu 2 vẫn thiếu nguồn tiền cọc trong lượt chạy thật dù gate chỉ dùng câu gốc tìm thấy.
2. Ghép hiệu lực và chuyển tiếp theo toàn bộ `provision_id`/phần cha. Hiện vẫn có mảnh giữa danh sách văn bản bị bãi bỏ ở các câu cư trú, và chú thích làm gộp khoản 3 vào nhãn khoản 2 ở nguồn tố tụng câu 36.
3. Kiểm tra đúng chủ thể/loại hình: nhà trọ nhiều phòng, nền tảng đăng tin so với nền tảng đặt hàng, phí người thuê trả so với thù lao giữa cá nhân môi giới và doanh nghiệp. Trích đúng văn bản chưa bảo đảm đúng quan hệ được hỏi.
4. Bổ sung nguồn trực tiếp cho nghĩa vụ thông báo cách tính/sản lượng điện, căn cứ nước địa phương, ngoại lệ dẫn chiếu và thủ tục bảo vệ dữ liệu trước khi kết luận đủ nguồn. Chưa xác nhận sự kiện kích hoạt mốc hiệu lực có điều kiện của quy định điện thuê nhà.
5. Hoàn tất điểm RAGAS còn thiếu khi có hạn mức của cùng bộ chấm; không ghép điểm Qwen vào các ô Gemini để làm so sánh trước/sau.

Nguồn gốc URL/SHA-256 và các trang đối chiếu được ghi riêng. Bản OCR/trích do hệ thống tạo không phải bản được Chính phủ phê duyệt; các bản kế thừa chưa được đối chiếu từng chữ với toàn văn gốc. Nhận xét nguồn là rà kỹ thuật, không phải đáp án pháp lý chuẩn độc lập.

Chi tiết: `eval/reports/legal_agent_after_v10_2026-10-03.json`, `legal_agent_source_review_2026-10-03.json`, `legal_agent_http_preview_2026-10-03.json`, `legal_agent_release_gate_2026-10-03.json`. Gate và review cùng gắn hash file đánh giá `a5b3ec7507e4ece633e3bf4469b0575f272e73b4c6ec2e22793996691c2a36ed`. Lượt thử lại giữ nguyên 36 phản hồi/ngữ cảnh, mọi điểm hợp lệ và baseline.
