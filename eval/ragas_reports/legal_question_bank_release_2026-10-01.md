# Kết quả kiểm thử bộ 36 câu hỏi bằng Ragas

- Bắt đầu (UTC): 2026-10-01T06:49:09.151788+00:00
- Cập nhật (UTC): 2026-10-01T07:42:45.320254+00:00
- SHA-256 bộ câu hỏi: `0cd8e8f865c9d50fa21ebb38fae22b925e2fd5bbb6e0241ee96d25eed8b0f4fd`
- Trình chấm: Ragas 0.3.9; mô hình theo chỉ số: faithfulness=qwen3.5:4b, answer_relevancy=qwen3.5:4b, context_utilization=qwen3.5:4b
- Mô hình embedding: intfloat/multilingual-e5-small

## Chỉ số hệ thống

| Chỉ số | Kết quả |
|---|---:|
| Câu đã kiểm thử | 36/36 |
| Có ngữ cảnh truy xuất | 36/36 |
| Truy xuất vector | 36/36 |
| Có ít nhất một nguồn cùng nhãn chủ đề dự kiến | 35/36 |
| Không đủ căn cứ / không có kết quả | 33 |
| Có câu trả lời tổng hợp (chưa kiểm định độc lập) | 3 |
| Câu trả lời một phần bằng trích đoạn nguồn | 32 |
| Chế độ suy giảm | 33 |
| Lỗi chạy câu hỏi | 0 |
| Đúng định dạng trích dẫn, trung bình | 1.0 |
| Độ trễ p50 / p95 | 13971.0 / 24856 ms |

## Chỉ số Ragas

| Chỉ số | Trung bình | Số câu được chấm |
|---|---:|---:|
| Bám sát ngữ cảnh | 0.7054 | 35 |
| Liên quan câu hỏi | 0.6866 | 36 |
| Hữu dụng của ngữ cảnh | 0.821 | 36 |
| Context recall | N/A | 0 |
| Answer correctness | N/A | 0 |

Hai chỉ số cuối cần đáp án hoặc ngữ cảnh chuẩn được gán nhãn độc lập. Bộ câu hỏi hiện chưa có đáp án độc lập, nên không lấy câu trả lời của hệ thống làm đáp án chuẩn.

## Theo nhóm câu hỏi

| Nhóm | Đã kiểm thử / tổng | Có nguồn | Chưa tổng hợp được kết luận | Bám nguồn (n) | Liên quan (n) | Hữu dụng ngữ cảnh (n) |
|---|---:|---:|---:|---:|---:|---:|
| Hợp đồng | 4/4 | 4 | 4 | 0.688 (4) | 0.599 (4) | 0.812 (4) |
| Điện | 4/4 | 4 | 2 | 0.787 (4) | 0.814 (4) | 1.000 (4) |
| Nước Cần Thơ | 4/4 | 4 | 3 | 0.697 (4) | 0.397 (4) | 0.833 (4) |
| Cư trú | 4/4 | 4 | 4 | 0.645 (4) | 0.809 (4) | 0.958 (4) |
| PCCC | 4/4 | 4 | 4 | 0.826 (4) | 0.792 (4) | 0.750 (4) |
| Môi giới | 4/4 | 4 | 4 | 0.643 (3) | 0.775 (4) | 0.625 (4) |
| Nền tảng đăng tin | 4/4 | 4 | 4 | 0.917 (4) | 0.786 (4) | 0.875 (4) |
| Dữ liệu cá nhân | 4/4 | 4 | 4 | 0.658 (4) | 0.612 (4) | 0.833 (4) |
| Dấu hiệu lừa đảo | 4/4 | 4 | 4 | 0.472 (4) | 0.595 (4) | 0.701 (4) |

## Trạng thái kho dữ liệu

Có 30 tệp trong `Data`, 30 tài liệu trong DB. Thiếu trong chỉ mục: 0; còn trong chỉ mục nhưng không còn tệp nguồn: 0.
Embedding: 1829/1829 đoạn của 30 tệp hiện hành; 915/915 tin phòng đủ điều kiện.
Có 0/36 câu đã truy xuất ít nhất một tệp không còn trong `Data` (câu: không có).

Nguồn không còn trong kho đã được ngừng truy xuất và giữ nội dung để khôi phục.

## Các câu cần xem lại

- Câu 1: chế độ suy giảm; chưa đủ căn cứ trả lời.
- Câu 2: chế độ suy giảm; trả lời một phần bằng trích đoạn, chưa kết luận áp dụng.
- Câu 3: chế độ suy giảm; trả lời một phần bằng trích đoạn, chưa kết luận áp dụng.
- Câu 4: chế độ suy giảm; trả lời một phần bằng trích đoạn, chưa kết luận áp dụng.
- Câu 7: chế độ suy giảm; trả lời một phần bằng trích đoạn, chưa kết luận áp dụng.
- Câu 8: chế độ suy giảm; trả lời một phần bằng trích đoạn, chưa kết luận áp dụng.
- Câu 9: chế độ suy giảm; trả lời một phần bằng trích đoạn, chưa kết luận áp dụng.
- Câu 10: chế độ suy giảm; trả lời một phần bằng trích đoạn, chưa kết luận áp dụng.
- Câu 11: chế độ suy giảm; trả lời một phần bằng trích đoạn, chưa kết luận áp dụng.
- Câu 13: chế độ suy giảm; trả lời một phần bằng trích đoạn, chưa kết luận áp dụng.
- Câu 14: chế độ suy giảm; trả lời một phần bằng trích đoạn, chưa kết luận áp dụng.
- Câu 15: chế độ suy giảm; trả lời một phần bằng trích đoạn, chưa kết luận áp dụng.
- Câu 16: chế độ suy giảm; trả lời một phần bằng trích đoạn, chưa kết luận áp dụng.
- Câu 17: chế độ suy giảm; trả lời một phần bằng trích đoạn, chưa kết luận áp dụng.
- Câu 18: chế độ suy giảm; trả lời một phần bằng trích đoạn, chưa kết luận áp dụng.
- Câu 19: chế độ suy giảm; trả lời một phần bằng trích đoạn, chưa kết luận áp dụng.
- Câu 20: chế độ suy giảm; trả lời một phần bằng trích đoạn, chưa kết luận áp dụng.
- Câu 21: chế độ suy giảm; trả lời một phần bằng trích đoạn, chưa kết luận áp dụng.
- Câu 22: chế độ suy giảm; trả lời một phần bằng trích đoạn, chưa kết luận áp dụng.
- Câu 23: lỗi Ragas: faithfulness; chế độ suy giảm; trả lời một phần bằng trích đoạn, chưa kết luận áp dụng.
- Câu 24: chế độ suy giảm; trả lời một phần bằng trích đoạn, chưa kết luận áp dụng.
- Câu 25: chế độ suy giảm; trả lời một phần bằng trích đoạn, chưa kết luận áp dụng.
- Câu 26: chế độ suy giảm; trả lời một phần bằng trích đoạn, chưa kết luận áp dụng.
- Câu 27: chế độ suy giảm; trả lời một phần bằng trích đoạn, chưa kết luận áp dụng.
- Câu 28: chế độ suy giảm; trả lời một phần bằng trích đoạn, chưa kết luận áp dụng.
- Câu 29: chưa có nguồn mang nhãn chủ đề dự kiến; chế độ suy giảm; trả lời một phần bằng trích đoạn, chưa kết luận áp dụng.
- Câu 30: chế độ suy giảm; trả lời một phần bằng trích đoạn, chưa kết luận áp dụng.
- Câu 31: chế độ suy giảm; trả lời một phần bằng trích đoạn, chưa kết luận áp dụng.
- Câu 32: chế độ suy giảm; trả lời một phần bằng trích đoạn, chưa kết luận áp dụng.
- Câu 33: chế độ suy giảm; trả lời một phần bằng trích đoạn, chưa kết luận áp dụng.
- Còn 3 câu cần xem lại trong JSON chi tiết.

## Giới hạn

- Faithfulness đo mức nhất quán với các đoạn đã lấy, không chứng minh văn bản đúng hoặc còn hiệu lực.
- Context utilization so với câu trả lời của chính hệ thống; đây không phải context precision so với đáp án độc lập.
- Giới hạn ngữ cảnh Ragas: 5 đoạn, giới hạn ký tự mỗi đoạn N/A; Answer Relevancy strictness=1. Cửa sổ token của mô hình vẫn có giới hạn.
- Mô hình sinh và chấm thuộc cùng họ Qwen local; điểm có thể thiên lệch. Cần người đánh giá độc lập cho kết luận pháp lý.
- Câu không có ngữ cảnh không bị gán điểm 0. Câu từ chối tổng hợp có nguồn được chấm nếu bật score_abstentions; điểm được tính thật, không giả lập.
- Tỷ lệ cùng nhãn chủ đề chỉ kiểm tra source.category với một nhãn dự kiến của câu hỏi. Nguồn khác nhóm có thể liên quan; đây là cảnh báo định tuyến/truy xuất, không phải tỷ lệ câu trả lời đúng hoặc trích dẫn được nguồn hỗ trợ.
- JSON chi tiết lưu từng câu, nguồn, ngữ cảnh, loại truy xuất, mô hình, độ trễ và lỗi chấm để kiểm tra lại.
