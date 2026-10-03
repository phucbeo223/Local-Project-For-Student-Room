# Kiểm thử năm nhóm sửa lỗi pháp lý — v15

Cập nhật UTC: 2026-10-03T20:32:19.904850+00:00

## Trạng thái

- Truy xuất thật: True; 35/35 gate.
- Local riêng: 36/36 phản hồi; 0 lỗi thực thi; 23 phản hồi một phần.
- Kiểm tra nguyên văn local: 36/36 phản hồi có mọi trích đoạn khớp đúng context/rank. Đây là kiểm tra chuỗi, không chứng nhận đúng luật.
- HTTP v14 câu trình báo: True; HTTP v13 câu 8 nguồn web trả về: True. Các kiểm tra HTTP này dùng cùng mã API; toàn bộ corpus cuối được kiểm tra riêng ở lượt v15.
- Worker Gemini: waiting_for_server; phản hồi hoàn thành: 0/36.
- Không điền điểm local vào Gemini. Kho public/API chính giữ nguyên, chờ gate và rà nguồn.

## RAGAS native Gemini — so sánh theo cặp

| Metric | Số điểm v15 | Số cặp cùng phương pháp | Baseline trên cặp | V15 trên cặp | Thay đổi |
|---|---:|---:|---:|---:|---:|
| faithfulness | 0/36 | 0 | N/A | N/A | N/A |
| answer_relevancy | 0/36 | 0 | N/A | N/A | N/A |
| context_utilization | 0/36 | 0 | N/A | N/A | N/A |

HTTP 429: checkpoint đã lưu. Mốc kiểm tra lại UTC: `2026-10-04T07:00:05+00:00`. Worker chỉ chạy tiếp khi probe server thành công.

Chưa đủ 108 điểm native; **chưa kết luận chất lượng tổng thể tăng**. Điểm thiếu giữ N/A.

## Các câu local — tách khỏi lượt Gemini

Phân tích chủ đề local dùng rules vì container này tắt key; Qwen chọn đoạn nguồn. Không dùng như phép đo thay cho cấu hình Gemini phân tích.

| Câu | Trạng thái | Model trả lời | Trích nguyên văn |
|---|---|---|---|
| 1 | trích nguồn | qwen3.5:9b | đạt |
| 2 | một phần | qwen3.5:9b | đạt |
| 3 | một phần | qwen3.5:9b | đạt |
| 4 | một phần | qwen3.5:9b | đạt |
| 5 | một phần | qwen3.5:9b | đạt |
| 6 | một phần | qwen3.5:9b | đạt |
| 7 | một phần | qwen3.5:9b | đạt |
| 8 | một phần | qwen3.5:9b | đạt |
| 9 | một phần | qwen3.5:9b | đạt |
| 10 | một phần | qwen3.5:9b | đạt |
| 11 | một phần | qwen3.5:9b | đạt |
| 12 | một phần | qwen3.5:9b | đạt |
| 13 | một phần | qwen3.5:9b | đạt |
| 14 | một phần | qwen3.5:9b | đạt |
| 15 | trích nguồn | qwen3.5:9b | đạt |
| 16 | trích nguồn | qwen3.5:9b | đạt |
| 17 | trích nguồn | qwen3.5:9b | đạt |
| 18 | một phần | qwen3.5:9b | đạt |
| 19 | một phần | qwen3.5:9b | đạt |
| 20 | trích nguồn | qwen3.5:9b | đạt |
| 21 | một phần | qwen3.5:9b | đạt |
| 22 | một phần | qwen3.5:9b | đạt |
| 23 | một phần | qwen3.5:9b | đạt |
| 24 | một phần | qwen3.5:9b | đạt |
| 25 | một phần | qwen3.5:9b | đạt |
| 26 | một phần | qwen3.5:9b | đạt |
| 27 | một phần | qwen3.5:9b | đạt |
| 28 | trích nguồn | qwen3.5:9b | đạt |
| 29 | trích nguồn | qwen3.5:9b | đạt |
| 30 | một phần | qwen3.5:9b | đạt |
| 31 | trích nguồn | qwen3.5:9b | đạt |
| 32 | trích nguồn | qwen3.5:9b | đạt |
| 33 | trích nguồn | qwen3.5:9b | đạt |
| 34 | trích nguồn | qwen3.5:9b | đạt |
| 35 | trích nguồn | qwen3.5:9b | đạt |
| 36 | trích nguồn | qwen3.5:9b | đạt |

## Rà nguồn local và lỗi còn lại

Hồ sơ rà nguồn: `legal_agent_local_review_v15_2026-10-04.json`. Kiểm tra cơ học đủ 36 câu; rà quan hệ/nguồn tập trung các câu trọng điểm. Không xác nhận pháp lý độc lập cho toàn bộ bộ câu hỏi.
- Câu 34/36 đã trích hướng dẫn bằng chứng dành cho người trình báo, Điều 146 khoản 1 và Điều 145 khoản 2; không chỉ thông báo nội bộ gửi Viện kiểm sát.
- Câu 21 còn chọn đoạn về giá dịch vụ thay cho nghĩa vụ công khai thông tin; câu trả lời một phần, cần xử lý/rà lại lượt native.
- Câu 10/11: quy định hợp đồng đơn vị cấp nước không tự xác lập cách chủ trọ chia tiền nước. Câu 24: có căn cứ trả tiền dịch vụ nhưng phần hình thức giấy tờ còn một phần.
- Hiệu lực điện có điều kiện và phạm vi áp dụng giá nước hiện tại chưa được xác minh. Không thay dữ kiện thiếu bằng suy đoán.

## Dấu vết và giới hạn

- JSON local: `legal_agent_local_v15_2026-10-04.json`, SHA `deff9af52f6192e129b5e8dd446874ab879472ebd502c815f7c64dc5d7026ea2`.
- JSON native: `legal_agent_after_v15_2026-10-04.json`, SHA tại lúc lập báo cáo `0348bf1555c4825ec7881253bdc6b3683e07a89f3130fc5b48be3b31324b5609`; checkpoint còn chạy có thể đổi SHA.
- Baseline: `legal_model_upgrade_after_2026-10-02.json`, SHA `b32743c4ad5b251313f488db5ce794e9e2c0159d5b34da346d70a465e3e4810b`; v10 lịch sử: SHA `a5b3ec7507e4ece633e3bf4469b0575f272e73b4c6ec2e22793996691c2a36ed`. Hai file giữ nguyên.
- Manifest cuối: `db830c71bd0d4c9eed5ed5980f9538a43283bf66d671f917afacf94d953f28da`.
- Các hạn chế còn cần rà: điều kiện hiệu lực điện; nghĩa vụ riêng chủ trọ về hồ sơ cư trú; phạm vi địa bàn/đơn vị cấp nước; phân loại nhà trọ; hướng dẫn công khai điện không phải điều luật.
- Không có đáp án chuẩn độc lập: Answer Correctness/Context Recall N/A. Native judge không thay kiểm tra hiệu lực/đúng chủ thể.
- Sổ nguồn và năm nhóm thay đổi: `docs/LEGAL_CORPUS_V2_SOURCES.md`, `docs/LEGAL_FIXES_20261004.md`.
