# So sánh 36 câu sau bổ sung nguồn Word

Snapshot nguồn/lượt sinh bắt đầu 2026-10-05T15:36:04.092169+00:00 (UTC); hoàn tất đối chiếu 2026-10-06T00:30:31.749295+07:00 (giờ Việt Nam). Tên phiên bản 20261005 giữ theo ngày snapshot, không đổi dữ liệu giữa lượt chạy.

Kho mới chỉ để thử nghiệm; kho và API hiện hành giữ nguyên. Pipeline, ngân hàng câu hỏi, Datahouse và chính sách chấm Qwen giống lượt trước.

| Chỉ tiêu | Trước: 16 tài liệu | Sau: 30 tài liệu |
|---|---:|---:|
| Chạy hoàn tất | 36/36 | 36/36 |
| Lỗi chạy | 0 | 0 |
| Khớp cao với đáp án mẫu | 0 | 2 |
| Khớp một phần | 27 | 27 |
| Khớp thấp | 9 | 7 |
| Hệ thống đánh dấu trả lời đầy đủ | 11 | 17 |
| Không có nguồn truy xuất | 3 | 0 |
| Dùng trích đoạn Qwen sau kiểm tra | 3 | 18 |
| Độ dài câu trả lời trung vị (ký tự) | 1332 | 1701 |
| Thời gian p50 (giây) | 42.1 | 54.9 |
| Thời gian p95 (giây) | 80.7 | 89.0 |

**Nhãn khớp là so nội dung với đáp án mẫu chưa xác minh, không phải điểm đúng pháp luật.** Hoàn tất 36 câu chỉ xác nhận lượt chạy, không chứng minh chất lượng 36 câu.

Tăng nhãn khớp: [30, 38, 45, 48, 49, 50, 55, 56, 58]. Giảm nhãn: [26, 28, 32, 37, 52]. Giữ nhãn: [19, 20, 21, 22, 23, 24, 25, 27, 29, 31, 33, 34, 35, 36, 43, 44, 46, 47, 51, 53, 54, 57].
Câu còn khớp thấp cần xem kỹ: [26, 28, 29, 32, 37, 47, 52].
Câu khớp một phần còn cần đối chiếu: [19, 20, 21, 22, 23, 24, 25, 27, 30, 31, 33, 34, 35, 36, 43, 44, 45, 46, 48, 49, 50, 51, 53, 54, 56, 57, 58].
Nguồn bổ sung được truy xuất ở 16/36 câu: [19, 20, 22, 28, 29, 30, 37, 38, 47, 48, 49, 50, 55, 56, 57, 58]. Câu trả lời giữ nguyên từng byte: [31]. Các thay đổi ở câu không dùng nguồn bổ sung có thể do lượt sinh/chấm, chưa chứng minh hiệu quả của dữ liệu mới.

## Dữ liệu và bảo toàn

30 tài liệu gồm 16 Word cũ nguyên byte + 12 bản Word chuyển nguyên văn website + 2 Word luật gốc. Tổng 393 đoạn/điều khoản, 423 vector E5 384 chiều. Đoạn dài chia tối đa 1.200 ký tự, giữ toàn đoạn/điều khoản cha.
789 nhà trọ Datahouse giữ nguyên nội dung và vector; graph thử nghiệm có 1.238 nút và 3.133 cạnh. Không PDF, không OCR, không embedding tóm tắt hay đáp án mẫu.
S07 chưa nạp vì phần nội dung bài là ảnh; S13 chưa nạp vì tải nguyên bản bị HTTP 403. Không dùng bảng giá ở chân trang thay cho nội dung bài.

## Giới hạn cần tiếp tục xử lý

- Bổ sung nguồn đã giải quyết ba câu không truy xuất được nguồn, nhưng chưa tự giải quyết việc tổng hợp câu trả lời. Lượt mới có 18 câu quay về trích đoạn Qwen, so với 3 câu trước; 15 câu có lý do kiểm tra ghi kết luận/số liệu chưa gắn trích dẫn trực tiếp.
- Ưu tiên trả lời trực tiếp, ngắn theo ý hỏi và gắn nguồn cho từng ý; hạn chế trả toàn bộ điều khoản dài. Câu 47–49 có nguồn mới nhưng câu trả lời dài khoảng 7.000–10.600 ký tự.
- Cần hoàn thiện các điều/khoản được dẫn chiếu còn thiếu và kiểm tra nguyên bản chính thức của Word/trích tuyển cũ; giữ đúng điều kiện, ngoại lệ, loại nền tảng và thời điểm áp dụng.
- Mỗi kho chỉ chạy một lượt; tính ngẫu nhiên và tình trạng mô hình/proxy có thể ảnh hưởng kết quả.
- Cùng Qwen cục bộ tham gia chọn bằng chứng và chấm đối chiếu; nhãn cần người đọc kiểm tra.
- Đáp án mẫu chưa xác minh; số tiền cọc, thời hạn minh họa và luật nền tảng cũ không được mặc nhiên coi là quy định bắt buộc.
- Câu 49 khác cách hỏi trong đáp án mẫu; chỉ so phần phạm vi chung.
- 13 Word/trích tuyển cũ vẫn còn cảnh báo nguồn chưa xác minh toàn văn; hai nguồn bổ sung chưa nạp.
- API hiện hành vẫn dùng v7; v8 chỉ là kho thử nghiệm chưa kích hoạt.
- Đây là 36 câu đã biết, chưa đo khả năng trả lời câu hỏi mới.

## Chi tiết từng câu

| Câu | Trước | Sau | Thay đổi |
|---|---|---|---|
| 19 | Một phần | Một phần | Giữ |
| 20 | Một phần | Một phần | Giữ |
| 21 | Một phần | Một phần | Giữ |
| 22 | Một phần | Một phần | Giữ |
| 23 | Một phần | Một phần | Giữ |
| 24 | Một phần | Một phần | Giữ |
| 25 | Một phần | Một phần | Giữ |
| 26 | Một phần | Thấp | Giảm |
| 27 | Một phần | Một phần | Giữ |
| 28 | Một phần | Thấp | Giảm |
| 29 | Thấp | Thấp | Giữ |
| 30 | Thấp | Một phần | Tăng |
| 31 | Một phần | Một phần | Giữ |
| 32 | Một phần | Thấp | Giảm |
| 33 | Một phần | Một phần | Giữ |
| 34 | Một phần | Một phần | Giữ |
| 35 | Một phần | Một phần | Giữ |
| 36 | Một phần | Một phần | Giữ |
| 37 | Một phần | Thấp | Giảm |
| 38 | Một phần | Cao | Tăng |
| 43 | Một phần | Một phần | Giữ |
| 44 | Một phần | Một phần | Giữ |
| 45 | Thấp | Một phần | Tăng |
| 46 | Một phần | Một phần | Giữ |
| 47 | Thấp | Thấp | Giữ |
| 48 | Thấp | Một phần | Tăng |
| 49 | Thấp | Một phần | Tăng |
| 50 | Thấp | Một phần | Tăng |
| 51 | Một phần | Một phần | Giữ |
| 52 | Một phần | Thấp | Giảm |
| 53 | Một phần | Một phần | Giữ |
| 54 | Một phần | Một phần | Giữ |
| 55 | Một phần | Cao | Tăng |
| 56 | Thấp | Một phần | Tăng |
| 57 | Một phần | Một phần | Giữ |
| 58 | Thấp | Một phần | Tăng |

[Xem ý còn thiếu và nhận xét từng câu](WORD_SUPPLEMENT_36_REVIEW_20261005.md).

Bản đầy đủ chứa câu trả lời và đáp án mẫu được giữ cục bộ tại `eval/reports/graph_rag_word_supplement_vs_reference_36_v8_2026-10-05.md`; báo cáo đối chiếu từng ý tại `eval/reports/graph_rag_word_supplement_paired_36_v8_2026-10-05.json`.
