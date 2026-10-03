# Kho embedding mới và agent — kết quả 03/10/2026

Trạng thái: **complete_with_errors**. Đã trả lời 36/36 câu.
Gemini phân tích câu hỏi; hybrid truy xuất; Qwen local chọn ID đoạn trả lời; hệ thống chép nguyên văn có kiểm tra với nguồn. Không dùng Gemini tạo câu trả lời. Đây là chế độ trích nguồn, không phải suy luận pháp lý tự do.
Điểm trước lấy từ bản đánh giá lịch sử ngày 02/10, giữ nguyên câu trả lời/ngữ cảnh/điểm gốc. So sánh chỉ có giá trị khi model chấm và cấu hình giống nhau.

| Metric | Trước | Sau | Thay đổi | Số cặp hợp lệ |
|---|---:|---:|---:|---:|
| faithfulness | 0.6635 | 0.9202 | +0.2567 | 30 |
| answer_relevancy | 0.7553 | 0.6276 | -0.1277 | 36 |
| context_utilization | 0.6042 | 0.6273 | +0.0232 | 36 |

## Từng câu

| Câu | Phân tích | Trả lời cuối | Trạng thái | Faithfulness | Relevancy | Context utilization |
|---|---|---|---|---:|---:|---:|
| 1 | gemini | qwen-local | tổng hợp | 1.0000 | 0.8669 | 0.3333 |
| 2 | rules | qwen-local | một phần | 1.0000 | 0.0000 | 0.5833 |
| 3 | rules | qwen-local | một phần | 1.0000 | 0.0000 | 1.0000 |
| 4 | rules | qwen-local | một phần | N/A | 0.8677 | 1.0000 |
| 5 | rules | qwen-local | tổng hợp | N/A | 0.9177 | 1.0000 |
| 6 | rules | qwen-local | tổng hợp | N/A | 0.8799 | 1.0000 |
| 7 | gemini | qwen-local | tổng hợp | N/A | 0.9026 | 1.0000 |
| 8 | gemini | qwen-local | tổng hợp | N/A | 0.8681 | 0.0000 |
| 9 | gemini | qwen-local | tổng hợp | 0.8333 | 0.8777 | 0.5000 |
| 10 | gemini | qwen-local | chưa đủ căn cứ | 0.6250 | 0.0000 | 0.0000 |
| 11 | gemini | qwen-local | một phần | 1.0000 | 0.0000 | 0.0000 |
| 12 | gemini | qwen-local | tổng hợp | 1.0000 | 0.8723 | 1.0000 |
| 13 | gemini | qwen-local | tổng hợp | 0.7500 | 0.8662 | 1.0000 |
| 14 | gemini | qwen-local | tổng hợp | 1.0000 | 0.9012 | 0.0000 |
| 15 | gemini | qwen-local | tổng hợp | 1.0000 | 0.8991 | 1.0000 |
| 16 | gemini | qwen-local | một phần | 1.0000 | 0.0000 | 1.0000 |
| 17 | gemini | qwen-local | tổng hợp | 1.0000 | 0.8849 | 1.0000 |
| 18 | gemini | qwen-local | tổng hợp | 1.0000 | 0.8998 | 0.5000 |
| 19 | gemini | qwen-local | một phần | 1.0000 | 0.0000 | 0.0000 |
| 20 | gemini | qwen-local | tổng hợp | 1.0000 | 0.8921 | 1.0000 |
| 21 | gemini | legal-partial-extractive | một phần | 1.0000 | 0.8683 | 0.3333 |
| 22 | gemini | qwen-local | chưa đủ căn cứ | 1.0000 | 0.8563 | 1.0000 |
| 23 | gemini | legal-partial-extractive | một phần | 0.8571 | 0.8553 | 1.0000 |
| 24 | gemini | qwen-local | tổng hợp | 0.6667 | 0.8587 | 0.3333 |
| 25 | gemini | qwen-local | tổng hợp | 0.9643 | 0.8282 | 0.0000 |
| 26 | gemini | qwen-local | một phần | 1.0000 | 0.0000 | 0.0000 |
| 27 | gemini | qwen-local | tổng hợp | 1.0000 | 0.8695 | 0.8333 |
| 28 | gemini | qwen-local | tổng hợp | 1.0000 | 0.8606 | 1.0000 |
| 29 | gemini | qwen-local | một phần | 1.0000 | 0.0000 | 0.8333 |
| 30 | gemini | template | chưa đủ căn cứ | 0.0000 | 0.0000 | 0.0000 |
| 31 | gemini | qwen-local | một phần | 0.9091 | 0.8177 | 0.5000 |
| 32 | gemini | qwen-local | một phần | 1.0000 | 0.0000 | 0.5000 |
| 33 | gemini | qwen-local | một phần | 1.0000 | 0.8549 | 1.0000 |
| 34 | gemini | qwen-local | tổng hợp | 1.0000 | 0.8335 | 1.0000 |
| 35 | gemini | qwen-local | một phần | 1.0000 | 0.8355 | 0.5000 |
| 36 | gemini | qwen-local | tổng hợp | N/A | 0.8575 | 0.8333 |

Không có đáp án chuẩn độc lập: answer correctness/context recall = N/A. Điểm RAGAS và đúng định dạng trích dẫn không xác nhận luật hiện hành.
Các JSON lưu câu trả lời, ngữ cảnh, agent/model thật, lỗi, token và kết quả chấm để rà soát. Chưa xóa kho cũ chỉ vì bộ kiểm tra truy xuất đạt.
