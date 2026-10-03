# Kết quả sửa và kiểm thử phần pháp lý, điện và nước

Phạm vi: 36 câu pháp lý tương ứng câu 19–38 và 43–58 của bộ cũ. Tạm bỏ câu giá thuê, khoảng cách, tin phòng và KTX theo yêu cầu; không dùng dữ liệu phòng cũ để kết luận chất lượng tìm phòng.

## Các sửa đổi đã thực hiện

| Nhóm | Thay đổi |
|---|---|
| Định tuyến | Khớp cụm từ có ranh giới; bổ sung chủ đề điện, nước, cư trú, PCCC, môi giới, dữ liệu cá nhân, nền tảng và hình sự. |
| Truy xuất | Lọc chủ đề chính và nguồn hỗ trợ liên chủ đề; ưu tiên điều khoản hợp đồng/hồ sơ cư trú, giảm nguồn xử phạt khi hỏi thủ tục; bỏ đoạn giới thiệu biên tập làm nguồn kết luận. |
| Vòng đời nguồn | Ngừng dùng 24 đường dẫn vắng trong Data; giữ đoạn/vectors cũ và lưu metadata trước thay đổi. Không coi vắng tệp là hết hiệu lực pháp luật. |
| Tách đoạn/tài liệu | Nhận tiêu đề Điều dạng dấu gạch và Markdown. Sửa tham chiếu ‘và Phụ lục’ làm mất tiêu đề hiệu lực. Thêm tóm tắt phạm vi nước, giữ nguyên DOCX đầu vào. |
| Kiểm tra kết luận | Kiểm tra kết luận chưa trích dẫn, số tiền không có trong nguồn, khẳng định sai về thiếu quy định; đối chiếu từng câu với chính nguồn được trích. Nếu không xác nhận được, chỉ trích nguyên đoạn phù hợp và đánh dấu câu trả lời một phần. |
| Đánh giá | Chỉ đánh giá 36 câu pháp lý; nạp embedding trước; lưu từng câu, nguồn, ngữ cảnh, độ trễ, lỗi và ba chỉ số Ragas. Giá thuê/khoảng cách/hội thoại chọn phòng chờ Data mới. |

## Đối chiếu cùng 36 câu

| Chỉ số vận hành | Trước | Sau |
|---|---:|---:|
| Đi vào kho pháp lý | 20/36 | 36/36 |
| Có ít nhất một nguồn cùng nhãn câu hỏi | 14/36 | 35/36 |
| Truy xuất đường dẫn không còn trong Data | 17/36 | 0/36 |
| Không đủ căn cứ tổng hợp / không có kết quả | 9 | 33 |

Trong các câu chưa tổng hợp được kết luận, lượt sau có 32 câu đưa được trích đoạn liên quan, gắn cờ `partial_answer`. Chúng không được coi là câu trả lời hoàn chỉnh.

Cùng nhãn chỉ phản ánh chọn nhóm nguồn, không phải tỷ lệ trả lời đúng. Nguồn liên chủ đề cần xem nội dung. Từ chối tổng hợp có thể do thiếu nguồn, sai kết luận hoặc bước kiểm tra bằng mô hình không xác nhận được; không đồng nghĩa luật không có quy định.

## Nạp dữ liệu và kiểm tra

- Nguồn đang truy xuất: 30 tài liệu; 1829/1829 đoạn có vector.
- Nguồn chưa nạp: 0; nguồn ready vắng trong Data: 0.
- Hồi quy: 72 kiểm tra qua. Kiểm thử câu hỏi chạy bằng ChatService thực, DB thật, embedding E5 và Qwen local; tắt ghi sự kiện chat trong runner.

## Metrics Ragas của lượt sau

| Metric | Trung bình | Số câu có điểm |
|---|---:|---:|
| faithfulness | 0.7054 | 35 |
| answer_relevancy | 0.6866 | 36 |
| context_utilization | 0.821 | 36 |
| context_recall | N/A: chưa có đáp án độc lập | 0 |
| answer_correctness | N/A: chưa có đáp án độc lập | 0 |

Mô hình chấm: {'faithfulness': 'qwen3.5:4b', 'answer_relevancy': 'qwen3.5:4b', 'context_utilization': 'qwen3.5:4b'}. Lượt sau dùng toàn bộ ngữ cảnh; lượt cũ chỉ dùng 2 đoạn × 1.200 ký tự và mô hình khác cho hai metric. Không suy ra mức cải thiện Ragas trực tiếp giữa hai phương pháp.

Ragas và bước kiểm tra kết luận đều dùng mô hình local; điểm không chứng minh văn bản còn hiệu lực hoặc câu trả lời đúng pháp lý. Cần gán nhãn độc lập để đo mức đúng và đầy đủ. Câu không đủ căn cứ được báo riêng, không giả lập đáp án chuẩn từ chính câu trả lời.

## Hạn chế còn phải khắc phục

Lượt này hoàn tất nạp dữ liệu, sửa luồng truy xuất và đo lại. Chất lượng trả lời pháp lý chưa đạt mức nghiệm thu: phần lớn phản hồi chỉ trích đoạn và chưa giải thích cách áp dụng cho câu hỏi.

- Bước kiểm tra bằng Qwen có cả dấu hiệu bỏ sót lẫn từ chối quá mức: một số lý do đánh đồng lời khuyên ‘nên kiểm tra’ với nghĩa vụ bắt buộc, hoặc không nhận đủ thông tin trong tiêu đề nguồn. Lý do tự động không phải kết luận của người kiểm định.
- Một số câu tổng hợp đã bị chặn vì bổ sung điều kiện, quyền hoặc thủ tục không xuất hiện trong nguồn được trích; bản trả lời sau cùng chuyển sang trích nguyên văn thay vì giữ kết luận này.
- Một nguồn đúng nhãn chưa bảo đảm đủ điều khoản để trả lời toàn bộ tình huống. Câu 29 lấy nguồn cư trú nhưng thiếu nguồn cùng nhãn dữ liệu cá nhân; phải kiểm tra mức bao phủ hai phần của câu hỏi.
- Cần đáp án tham chiếu và nhãn điều khoản độc lập cho từng câu, rồi đối chiếu cả truy xuất, kết luận và độ đầy đủ. Hiện chưa đo được answer correctness/context recall; không tính câu trích đoạn là đã giải quyết xong yêu cầu tư vấn.

## Chi tiết từng câu

| Câu mới / cũ | Chủ đề | Trạng thái |
|---|---|---|
| 1 / 19 | housing_contract | chưa đủ căn cứ tổng hợp |
| 2 / 20 | housing_contract | một phần: trích đoạn, chưa kết luận áp dụng |
| 3 / 21 | housing_contract | một phần: trích đoạn, chưa kết luận áp dụng |
| 4 / 22 | housing_contract | một phần: trích đoạn, chưa kết luận áp dụng |
| 5 / 23 | electricity | có câu trả lời tổng hợp, chưa kiểm định độc lập |
| 6 / 24 | electricity | có câu trả lời tổng hợp, chưa kiểm định độc lập |
| 7 / 25 | electricity | một phần: trích đoạn, chưa kết luận áp dụng |
| 8 / 26 | electricity | một phần: trích đoạn, chưa kết luận áp dụng |
| 9 / 27 | water_cantho | một phần: trích đoạn, chưa kết luận áp dụng |
| 10 / 28 | water_cantho | một phần: trích đoạn, chưa kết luận áp dụng |
| 11 / 29 | water_cantho | một phần: trích đoạn, chưa kết luận áp dụng |
| 12 / 30 | water_cantho | có câu trả lời tổng hợp, chưa kiểm định độc lập |
| 13 / 31 | residence | một phần: trích đoạn, chưa kết luận áp dụng |
| 14 / 32 | residence | một phần: trích đoạn, chưa kết luận áp dụng |
| 15 / 33 | residence | một phần: trích đoạn, chưa kết luận áp dụng |
| 16 / 34 | residence | một phần: trích đoạn, chưa kết luận áp dụng |
| 17 / 35 | fire_safety | một phần: trích đoạn, chưa kết luận áp dụng |
| 18 / 36 | fire_safety | một phần: trích đoạn, chưa kết luận áp dụng |
| 19 / 37 | fire_safety | một phần: trích đoạn, chưa kết luận áp dụng |
| 20 / 38 | fire_safety | một phần: trích đoạn, chưa kết luận áp dụng |
| 21 / 43 | real_estate_brokerage | một phần: trích đoạn, chưa kết luận áp dụng |
| 22 / 44 | real_estate_brokerage | một phần: trích đoạn, chưa kết luận áp dụng |
| 23 / 45 | real_estate_brokerage | một phần: trích đoạn, chưa kết luận áp dụng; lỗi chấm faithfulness |
| 24 / 46 | real_estate_brokerage | một phần: trích đoạn, chưa kết luận áp dụng |
| 25 / 47 | ecommerce_platform | một phần: trích đoạn, chưa kết luận áp dụng |
| 26 / 48 | ecommerce_platform | một phần: trích đoạn, chưa kết luận áp dụng |
| 27 / 49 | ecommerce_platform | một phần: trích đoạn, chưa kết luận áp dụng |
| 28 / 50 | ecommerce_platform | một phần: trích đoạn, chưa kết luận áp dụng |
| 29 / 51 | privacy_data | một phần: trích đoạn, chưa kết luận áp dụng |
| 30 / 52 | privacy_data | một phần: trích đoạn, chưa kết luận áp dụng |
| 31 / 53 | privacy_data | một phần: trích đoạn, chưa kết luận áp dụng |
| 32 / 54 | privacy_data | một phần: trích đoạn, chưa kết luận áp dụng |
| 33 / 55 | criminal_law | một phần: trích đoạn, chưa kết luận áp dụng |
| 34 / 56 | criminal_law | một phần: trích đoạn, chưa kết luận áp dụng |
| 35 / 57 | criminal_law | một phần: trích đoạn, chưa kết luận áp dụng |
| 36 / 58 | criminal_law | một phần: trích đoạn, chưa kết luận áp dụng |

JSON chi tiết giữ nguyên câu trả lời, nguồn, ngữ cảnh, lý do từ chối và lỗi chấm để kiểm tra lại.
