# Kiểm thử năm nhóm sửa lỗi pháp lý — v15

Cập nhật UTC: 2026-10-03T20:07:32.003812+00:00

## Trạng thái

- Truy xuất thật: True; 35/35 gate.
- Local riêng: 1/36 phản hồi; 0 lỗi thực thi; 0 phản hồi một phần.
- Kiểm tra nguyên văn local: 1/1 phản hồi có mọi trích đoạn khớp đúng context/rank. Đây là kiểm tra chuỗi, không chứng nhận đúng luật.
- HTTP v14: True; nguồn web trả về: chưa xong.
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
| 2 | chưa chạy |  | chưa xong |
| 3 | chưa chạy |  | chưa xong |
| 4 | chưa chạy |  | chưa xong |
| 5 | chưa chạy |  | chưa xong |
| 6 | chưa chạy |  | chưa xong |
| 7 | chưa chạy |  | chưa xong |
| 8 | chưa chạy |  | chưa xong |
| 9 | chưa chạy |  | chưa xong |
| 10 | chưa chạy |  | chưa xong |
| 11 | chưa chạy |  | chưa xong |
| 12 | chưa chạy |  | chưa xong |
| 13 | chưa chạy |  | chưa xong |
| 14 | chưa chạy |  | chưa xong |
| 15 | chưa chạy |  | chưa xong |
| 16 | chưa chạy |  | chưa xong |
| 17 | chưa chạy |  | chưa xong |
| 18 | chưa chạy |  | chưa xong |
| 19 | chưa chạy |  | chưa xong |
| 20 | chưa chạy |  | chưa xong |
| 21 | chưa chạy |  | chưa xong |
| 22 | chưa chạy |  | chưa xong |
| 23 | chưa chạy |  | chưa xong |
| 24 | chưa chạy |  | chưa xong |
| 25 | chưa chạy |  | chưa xong |
| 26 | chưa chạy |  | chưa xong |
| 27 | chưa chạy |  | chưa xong |
| 28 | chưa chạy |  | chưa xong |
| 29 | chưa chạy |  | chưa xong |
| 30 | chưa chạy |  | chưa xong |
| 31 | chưa chạy |  | chưa xong |
| 32 | chưa chạy |  | chưa xong |
| 33 | chưa chạy |  | chưa xong |
| 34 | chưa chạy |  | chưa xong |
| 35 | chưa chạy |  | chưa xong |
| 36 | chưa chạy |  | chưa xong |

## Dấu vết và giới hạn

- JSON local: `legal_agent_local_v15_2026-10-04.json`, SHA `916f799f212eb4e4229024d265580e068f57d8be5b42f2ff19363bbddfbec3d9`.
- JSON native: `legal_agent_after_v15_2026-10-04.json`, SHA tại lúc lập báo cáo `0348bf1555c4825ec7881253bdc6b3683e07a89f3130fc5b48be3b31324b5609`; checkpoint còn chạy có thể đổi SHA.
- Baseline: `legal_model_upgrade_after_2026-10-02.json`, SHA `b32743c4ad5b251313f488db5ce794e9e2c0159d5b34da346d70a465e3e4810b`; v10 lịch sử: SHA `a5b3ec7507e4ece633e3bf4469b0575f272e73b4c6ec2e22793996691c2a36ed`. Hai file giữ nguyên.
- Manifest cuối: `db830c71bd0d4c9eed5ed5980f9538a43283bf66d671f917afacf94d953f28da`.
- Các hạn chế còn cần rà: điều kiện hiệu lực điện; nghĩa vụ riêng chủ trọ về hồ sơ cư trú; phạm vi địa bàn/đơn vị cấp nước; phân loại nhà trọ; hướng dẫn công khai điện không phải điều luật.
- Không có đáp án chuẩn độc lập: Answer Correctness/Context Recall N/A. Native judge không thay kiểm tra hiệu lực/đúng chủ thể.
- Sổ nguồn và năm nhóm thay đổi: `docs/LEGAL_CORPUS_V2_SOURCES.md`, `docs/LEGAL_FIXES_20261004.md`.
