# Chạy và chấm bằng model local — 03/10/2026

Trạng thái: **collecting_local_answers**. Cập nhật UTC: 2026-10-03T04:48:30.608302+00:00.

Câu trả lời mới: 6/36. Model trả lời, kiểm tra nguồn và chấm: Qwen 3.5 9B qua Ollama.
Điểm trước được chấm lại từ câu trả lời và ngữ cảnh cũ; giữ nguyên tệp kết quả gốc.

| Chỉ số | Trước | Sau | Chênh lệch | Số cặp hợp lệ |
|---|---:|---:|---:|---:|
| faithfulness | N/A | N/A | N/A | 0 |
| answer_relevancy | N/A | N/A | N/A | 0 |
| context_utilization | N/A | N/A | N/A | 0 |

Chỉ kết luận cải thiện khi cả hai lượt đã chấm đủ bằng cùng cấu hình. Điểm từ Gemini trước đây không được so trực tiếp với điểm local.

- Dùng RAGAS thật, đủ ngữ cảnh truy xuất, E5 multilingual small, nhiệt độ 0, relevancy strictness 1, một luồng chấm, tối đa 8192 token, thời hạn mỗi yêu cầu 300 giây.
- Không có đáp án pháp lý chuẩn độc lập; chưa đo answer correctness/context recall. Model sinh cũng là model chấm nên cần rà soát của người am hiểu pháp luật.
- Các câu giá phòng/khoảng cách đã loại khỏi bộ pháp lý. Giữ dữ liệu nguồn chính thức và vector đã nạp; không tạo thêm quy định.
- Trường hợp thiếu nguồn, hết thời gian hoặc JSON bị cụt được ghi lỗi/N/A, không đổi thành điểm giả.

## Kết quả mới từng câu

| Câu | Trạng thái | Model thực tế | Faithfulness | Relevancy | Context utilization |
|---|---|---|---:|---:|---:|
| 1 | chưa đủ căn cứ | template | N/A | N/A | N/A |
| 2 | một phần | legal-partial-extractive | N/A | N/A | N/A |
| 3 | một phần | legal-partial-extractive | N/A | N/A | N/A |
| 4 | một phần | legal-partial-extractive | 0.5556 | 0.7763 | 1.0000 |
| 5 | tổng hợp | legal-extractive | N/A | N/A | N/A |
| 6 | tổng hợp | legal-extractive | N/A | N/A | N/A |
| 7 | chưa chạy |  | N/A | N/A | N/A |
| 8 | chưa chạy |  | N/A | N/A | N/A |
| 9 | chưa chạy |  | N/A | N/A | N/A |
| 10 | chưa chạy |  | N/A | N/A | N/A |
| 11 | chưa chạy |  | N/A | N/A | N/A |
| 12 | chưa chạy |  | N/A | N/A | N/A |
| 13 | chưa chạy |  | N/A | N/A | N/A |
| 14 | chưa chạy |  | N/A | N/A | N/A |
| 15 | chưa chạy |  | N/A | N/A | N/A |
| 16 | chưa chạy |  | N/A | N/A | N/A |
| 17 | chưa chạy |  | N/A | N/A | N/A |
| 18 | chưa chạy |  | N/A | N/A | N/A |
| 19 | chưa chạy |  | N/A | N/A | N/A |
| 20 | chưa chạy |  | N/A | N/A | N/A |
| 21 | chưa chạy |  | N/A | N/A | N/A |
| 22 | chưa chạy |  | N/A | N/A | N/A |
| 23 | chưa chạy |  | N/A | N/A | N/A |
| 24 | chưa chạy |  | N/A | N/A | N/A |
| 25 | chưa chạy |  | N/A | N/A | N/A |
| 26 | chưa chạy |  | N/A | N/A | N/A |
| 27 | chưa chạy |  | N/A | N/A | N/A |
| 28 | chưa chạy |  | N/A | N/A | N/A |
| 29 | chưa chạy |  | N/A | N/A | N/A |
| 30 | chưa chạy |  | N/A | N/A | N/A |
| 31 | chưa chạy |  | N/A | N/A | N/A |
| 32 | chưa chạy |  | N/A | N/A | N/A |
| 33 | chưa chạy |  | N/A | N/A | N/A |
| 34 | chưa chạy |  | N/A | N/A | N/A |
| 35 | chưa chạy |  | N/A | N/A | N/A |
| 36 | chưa chạy |  | N/A | N/A | N/A |
