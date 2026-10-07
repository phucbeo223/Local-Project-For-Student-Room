# Cập nhật nguồn và kiểm tra Gemini — 07/10/2026

Đã xóa 22 báo cáo pilot/kiểm tra HTTP cũ không còn được tham chiếu, giữ dữ liệu nguồn, đáp án gốc, các lượt đầy đủ và báo cáo mới. [Danh sách và hàm băm các tệp đã xóa](<D:/AI-powered-system-to-assist-Can-Tho-University-students-in-finding-accommodation--main/docs/report_cleanup_20261007.json>).

## Câu 49 và 50

Câu 49: bổ sung nguyên văn Word từ Công báo: Điều 12, 13 của Luật 122/2025/QH15 và Điều 14, 22 của Nghị định 248/2026/NĐ-CP. Điều 15, 17 của luật đã có trong kho trước đó; lỗi còn nằm ở việc không truy xuất dẫn chiếu sang luật. Đã sửa truy xuất và giữ trích dẫn riêng cho từng văn bản, bổ sung điều khoản phụ thuộc sau lựa chọn. Kho mới `legal_word_completion_v18_20261007` có 40 tài liệu, 497 đoạn, 497 vector E5 thật 384 chiều; đã đối chiếu hàm băm, bản Word, liên kết và giữ kho v16.

Nguồn chính thống: [Luật Thương mại điện tử](https://vanban.chinhphu.vn/?docid=216503&pageid=27160), [Nghị định 248](https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-248-2026-nd-cp-469983.htm). Giới hạn tám nguồn thay giới hạn năm để hiển thị đủ văn bản và điều khoản thi hành.

Câu 50: cảnh báo mới là “Các dấu hiệu này giúp nhận diện rủi ro; cần kiểm tra liên kết và giao dịch cụ thể để kết luận.” Vẫn giữ phạm vi khuyến cáo của từng nhà cung cấp/cơ quan và loại bỏ ý không được kiểm chứng. Trong lượt 36 câu, câu 49 đã được đánh dấu đủ căn cứ; câu 50 vẫn partial do kiểm tra bao phủ và nhận diện cụm từ thận trọng. Cảnh báo mới đã hiện qua HTTP, nhưng chưa coi việc đổi câu cảnh báo là giải quyết mọi nhãn partial. Nhãn trên giao diện đổi thành “Câu trả lời còn giới hạn; hãy đọc lưu ý và đối chiếu nguồn.” để không gọi nhầm câu trả lời Gemini một phần là phương án dự phòng.

## Bước 4: nguồn và bộ chấm

Giữ nguyên đáp án và bộ chấm V15. Rà riêng câu 24: tỷ lệ 3/4 có điều kiện kê khai; không coi phép tính 37,5 kWh hoặc bảng bậc cũ là chuẩn pháp lý khi chưa xác minh biểu giá và mốc hiệu lực riêng. Rà câu 30: thao tác tra cứu phải gắn đúng nhà cung cấp trên hóa đơn; thêm giới hạn đó không chứng minh trả lời sai nguồn. Các nhãn khác mẫu được ghi riêng để rà lại, không tự nâng điểm. Các ý còn pending trong bộ tham chiếu chưa được chứng nhận là đáp án chuẩn.

Nguồn đối chiếu: [Thông tư 60](https://vanban.chinhphu.vn/?docid=216125&orggroupid=4&pageid=27160), [hướng dẫn CANTHOWASSCO](https://hddt.ctn-cantho.com.vn/huong-dan). [Kết quả rà nguồn](<D:/AI-powered-system-to-assist-Can-Tho-University-students-in-finding-accommodation--main/eval/reports/gemini_completion_source_audit_final_v18_20261007.json>); [đối chiếu V15](<D:/AI-powered-system-to-assist-Can-Tho-University-students-in-finding-accommodation--main/eval/reports/gemini_completion_36_final_v18_v15_20261007.json>).

## Bước 5: đo lại

Đủ 36/36 yêu cầu hoàn thành, không lỗi thu thập. 14 câu trả lời đầy đủ theo kiểm tra thời điểm chạy; 22 câu có giới hạn. Không diễn giải số yêu cầu hoàn thành thành tỷ lệ đúng pháp luật.

Thời gian toàn dịch vụ p50 19.84s, p95 36.55s. Bao gồm phân tích, E5, truy xuất, chọn nguồn, viết, kiểm chứng, sửa và tạo phản hồi; chưa gồm HTTP/xác thực. Lượt 36 câu chạy với hai yêu cầu đồng thời; warm-up và token của nó lưu riêng. Có tác vụ xây ứng dụng cùng lúc nên không coi đây là phép đo hiệu năng độc lập. Không so trực tiếp với thời gian replay chọn nguồn của A/B cũ.

Ghi nhận 183 lần gọi mô hình, 183 yêu cầu HTTP, 0 lỗi gọi mô hình, 0 lỗi HTTP. Token được trả về: 734877; mức đầy đủ: 183/183 lần gọi có usage. Warm-up của lượt 36 câu ghi riêng 23356 token, không cộng vào số trên. Số thiếu là chưa biết, không phải 0; không tính lặp wrapper và không suy đoán chi phí.

Số lần gọi mô hình theo bước: question_analysis: 36; evidence_selection: 48; answer_synthesis: 49; source_verification: 50. Gồm các lượt sửa trong giới hạn; không chỉ đo bước viết câu trả lời.

Đo lặp hai lần mỗi câu 49/50/54, ở mức một và ba yêu cầu đồng thời; warm-up lưu riêng. Khoảng cách tối thiểu giữa các lần gọi Gemini trong phép đo là 0 giây; API đang dùng 5 giây. Đây là mẫu tải nhỏ, chưa xác lập SLA:

| Yêu cầu đồng thời | Mẫu | p50 | p95 | Lỗi | Trả lời một phần |
|---:|---:|---:|---:|---:|---:|
| 1 | 6 | 31.69s | 36.44s | 0 | 3 |
| 3 | 6 | 32.59s | 37.09s | 0 | 1 |

Độ ổn định theo câu: câu 49: 1/4 lượt partial; câu 50: 3/4 lượt partial; câu 54: 0/4 lượt partial. Có thêm nguồn không bảo đảm mọi lượt sinh đều đủ ý.

Các nhãn V15: `{"high": 8, "partial": 25, "low": 3}`. Đây là độ giống mẫu, không phải tỷ lệ đúng pháp luật.

252 kiểm thử pipeline và báo cáo đạt; 126 kiểm thử liên quan cũng đạt trong ảnh ứng dụng mới. Đã kích hoạt kho v18, API khỏe và kiểm tra HTTP đạt cho câu 49, 50 cùng tìm phòng. Tài khoản thử đã được xóa. Các chỉ số HTTP lưu riêng với thời gian dịch vụ. Hàm băm của lượt chạy và dữ liệu nguồn được lưu trong báo cáo JSON. Không sửa đáp án để tăng điểm.

[Bản đính chính usage Gemini của A/B cũ](<D:/AI-powered-system-to-assist-Can-Tho-University-students-in-finding-accommodation--main/eval/reports/legal_selector_ab_v2_usage_correction_20261007.json>) — 710.843 token Gemini ghi nhận ở nhánh chọn nguồn Qwen (viết/kiểm chứng) và 793.987 ở nhánh chọn nguồn Gemini; bốn lần lỗi Gemini không có usage. Không coi đây là tổng token của cả Qwen và Gemini hoặc tổng toàn luồng phân tích câu hỏi. Báo cáo gốc giữ nguyên.

Tệp kết quả chính: [lượt chạy 36 câu](<D:/AI-powered-system-to-assist-Can-Tho-University-students-in-finding-accommodation--main/eval/reports/gemini_completion_36_final_v18_20261007.json>), [đo tải lặp](<D:/AI-powered-system-to-assist-Can-Tho-University-students-in-finding-accommodation--main/eval/reports/gemini_completion_load_v18_20261007.json>), [tổng hợp số liệu](<D:/AI-powered-system-to-assist-Can-Tho-University-students-in-finding-accommodation--main/eval/reports/gemini_completion_summary_20261007.json>).
