# Kết quả kiểm thử bộ 58 câu hỏi bằng Ragas

- Bắt đầu (UTC): 2026-10-01T04:25:48.488265+00:00
- Cập nhật (UTC): 2026-10-01T05:37:10.432021+00:00
- SHA-256 bộ câu hỏi: `bc4d62c79c37697718ab5419750daacbbb0a5bdfd0c1992db8677b0823e85792`
- Trình chấm: Ragas 0.3.9; mô hình theo chỉ số: faithfulness=qwen2.5:1.5b, answer_relevancy=qwen3.5:4b, context_utilization=qwen2.5:1.5b
- Mô hình embedding: intfloat/multilingual-e5-small

## Chỉ số hệ thống

| Chỉ số | Kết quả |
|---|---:|
| Câu đã kiểm thử | 58/58 |
| Có ngữ cảnh truy xuất | 53/58 |
| Truy xuất vector | 55/58 |
| Có ít nhất một nguồn cùng nhãn chủ đề dự kiến | 14/40 |
| Không đủ căn cứ / không có kết quả | 12 |
| Chế độ suy giảm | 15 |
| Lỗi chạy câu hỏi | 0 |
| Đúng định dạng trích dẫn, trung bình | 1.0 |
| Độ trễ p50 / p95 | 35869.0 / 121674 ms |

## Chỉ số Ragas

| Chỉ số | Trung bình | Số câu được chấm |
|---|---:|---:|
| Bám sát ngữ cảnh | 0.6365 | 42 |
| Liên quan câu hỏi | 0.7502 | 46 |
| Hữu dụng của ngữ cảnh | 0.7935 | 46 |
| Context recall | N/A | 0 |
| Answer correctness | N/A | 0 |

Hai chỉ số cuối cần đáp án hoặc ngữ cảnh chuẩn được gán nhãn độc lập. Bộ 58 câu hiện chỉ có câu hỏi, nên không lấy câu trả lời của hệ thống làm đáp án chuẩn.

## Theo nhóm câu hỏi

| Nhóm | Đã trả lời / tổng | Có nguồn | Không trả lời | Bám nguồn (n) | Liên quan (n) | Hữu dụng ngữ cảnh (n) |
|---|---:|---:|---:|---:|---:|---:|
| Tìm và lọc phòng | 18/18 | 17 | 1 | 0.730 (16) | 0.767 (17) | 0.912 (17) |
| Hợp đồng | 4/4 | 4 | 1 | 0.417 (3) | 0.825 (3) | 1.000 (3) |
| Điện | 4/4 | 4 | 2 | 0.500 (2) | 0.795 (2) | 1.000 (2) |
| Nước Cần Thơ | 4/4 | 4 | 3 | N/A (0) | 0.780 (1) | 0.500 (1) |
| Cư trú | 4/4 | 4 | 1 | 0.933 (3) | 0.835 (3) | 0.667 (3) |
| PCCC | 4/4 | 4 | 0 | 0.625 (4) | 0.408 (4) | 0.625 (4) |
| Nhà ở sinh viên | 4/4 | 2 | 2 | 0.000 (1) | 0.811 (2) | 0.750 (2) |
| Môi giới | 4/4 | 4 | 0 | 0.000 (4) | 0.786 (4) | 1.000 (4) |
| Nền tảng đăng tin | 4/4 | 2 | 2 | 0.875 (2) | 0.756 (2) | 0.500 (2) |
| Dữ liệu cá nhân | 4/4 | 4 | 0 | 0.938 (4) | 0.764 (4) | 0.250 (4) |
| Dấu hiệu lừa đảo | 4/4 | 4 | 0 | 0.667 (3) | 0.787 (4) | 0.875 (4) |

## Trạng thái kho dữ liệu

Có 29 tệp trong `Data`, 53 tài liệu trong DB. Thiếu trong chỉ mục: 0; còn trong chỉ mục nhưng không còn tệp nguồn: 24.
Embedding: 1821/1821 đoạn của 29 tệp hiện hành; 915/915 tin phòng đủ điều kiện.
Có 19/58 câu đã truy xuất ít nhất một tệp không còn trong `Data` (câu: 17, 20, 21, 22, 23, 24, 25, 26, 28, 30, 32, 33, 34, 35, 41, 46, 51, 55, 57).

Các tài liệu cũ vẫn có thể được truy xuất bởi ứng dụng. Không diễn giải điểm trên là chất lượng của riêng 29 tệp hiện hành.

## Các câu cần xem lại

- Câu 7: lỗi Ragas: faithfulness.
- Câu 8: chế độ suy giảm; không trả lời.
- Câu 19: chưa có nguồn mang nhãn chủ đề dự kiến.
- Câu 22: chế độ suy giảm; không trả lời.
- Câu 25: chế độ suy giảm; không trả lời.
- Câu 26: chế độ suy giảm; không trả lời.
- Câu 27: chế độ suy giảm; không trả lời.
- Câu 28: chưa có nguồn mang nhãn chủ đề dự kiến; chế độ suy giảm; không trả lời.
- Câu 29: lỗi Ragas: faithfulness; chưa có nguồn mang nhãn chủ đề dự kiến; chế độ suy giảm.
- Câu 30: chế độ suy giảm; không trả lời.
- Câu 31: chưa có nguồn mang nhãn chủ đề dự kiến; chế độ suy giảm; không trả lời.
- Câu 36: chưa có nguồn mang nhãn chủ đề dự kiến.
- Câu 37: chưa có nguồn mang nhãn chủ đề dự kiến.
- Câu 38: chưa có nguồn mang nhãn chủ đề dự kiến.
- Câu 39: lỗi Ragas: faithfulness; chưa có nguồn mang nhãn chủ đề dự kiến; chế độ suy giảm.
- Câu 40: chưa có nguồn mang nhãn chủ đề dự kiến; không trả lời.
- Câu 41: chưa có nguồn mang nhãn chủ đề dự kiến.
- Câu 42: chưa có nguồn mang nhãn chủ đề dự kiến; không trả lời.
- Câu 43: chưa có nguồn mang nhãn chủ đề dự kiến.
- Câu 44: chưa có nguồn mang nhãn chủ đề dự kiến.
- Câu 45: chưa có nguồn mang nhãn chủ đề dự kiến.
- Câu 47: chưa có nguồn mang nhãn chủ đề dự kiến; chế độ suy giảm; không trả lời.
- Câu 48: chưa có nguồn mang nhãn chủ đề dự kiến; chế độ suy giảm.
- Câu 49: chưa có nguồn mang nhãn chủ đề dự kiến; chế độ suy giảm.
- Câu 50: chưa có nguồn mang nhãn chủ đề dự kiến; không trả lời.
- Câu 51: chưa có nguồn mang nhãn chủ đề dự kiến.
- Câu 52: chưa có nguồn mang nhãn chủ đề dự kiến; chế độ suy giảm.
- Câu 53: chưa có nguồn mang nhãn chủ đề dự kiến; chế độ suy giảm.
- Câu 54: chưa có nguồn mang nhãn chủ đề dự kiến.
- Câu 55: lỗi Ragas: faithfulness; chưa có nguồn mang nhãn chủ đề dự kiến.
- Còn 3 câu cần xem lại trong JSON chi tiết.

## Giới hạn

- Faithfulness đo mức nhất quán với các đoạn đã lấy, không chứng minh văn bản đúng hoặc còn hiệu lực.
- Context utilization so với câu trả lời của chính hệ thống; đây không phải context precision so với đáp án độc lập.
- Để giám khảo local chạy được, Ragas chỉ đọc hai ngữ cảnh đầu (mỗi đoạn tối đa 1.200 ký tự); Answer Relevancy dùng một câu hỏi tái tạo (strictness=1).
- Qwen3.5:4b vừa sinh câu trả lời vừa chấm Answer Relevancy; Qwen2.5:1.5b chấm hai chỉ số còn lại và đã có lỗi JSON. Điểm có thể thiên lệch; cần người đánh giá độc lập cho kết luận pháp lý.
- Các câu không có ngữ cảnh hoặc hệ thống chủ động không trả lời không được gán điểm Ragas bằng 0; số lượng được nêu riêng.
- Tỷ lệ cùng nhãn chủ đề chỉ kiểm tra source.category với một nhãn dự kiến của câu hỏi. Nguồn khác nhóm có thể liên quan; đây là cảnh báo định tuyến/truy xuất, không phải tỷ lệ câu trả lời đúng hoặc trích dẫn được nguồn hỗ trợ.
- JSON chi tiết lưu từng câu, nguồn, ngữ cảnh, loại truy xuất, mô hình, độ trễ và lỗi chấm để kiểm tra lại.
