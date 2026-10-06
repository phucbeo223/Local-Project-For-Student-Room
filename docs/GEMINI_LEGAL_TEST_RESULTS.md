# Kết quả triển khai và thử nghiệm — 06/10/2026

Đã triển khai Gemini selector và hai chế độ: chọn nguồn rồi viết riêng (`separate`),
hoặc chọn nguồn và viết trong một request (`combined`). Cả hai giữ bước phân tích,
truy xuất E5/BM25/graph, kiểm chứng từng ý và sửa nội dung tối đa một lần.

**Khuyến nghị hiện tại: giữ Qwen/separate làm mặc định.** Gemini combined nhanh hơn
trong lượt thử này nhưng độ khớp đáp án tham chiếu V15 giảm. Code mới có thể bật qua
cấu hình để thử tiếp; container API chính chưa được thay hoặc khởi động lại.

## Kiểm thử đã hoàn thành

- 196/196 unit và regression tests đạt, gồm đường tìm phòng, cấu hình sai, ID nguồn
  sai/trùng, trích dẫn ngoài nguồn, giới hạn sửa, lỗi proxy và chặn payload nhà trọ.
- Gemini combined: 36/36 câu qua service thật, DB/corpus thật và proxy hiện có;
  không có lỗi lượt trả lời, không có lời gọi Qwen trong luồng sinh câu trả lời.
- Audit mọi rank trích dẫn trong câu trả lời: 36/36 thuộc nguồn trả về.
- V15: chấm đủ 36/36 câu bằng Qwen cục bộ; audit quote đạt 36/36, không có câu
  chưa chấm được. Không sửa scorer, quantity audit hoặc đáp án tham chiếu.
- Gemini separate: pilot 3/3 câu (19, 30, 55) qua proxy, không lỗi dịch vụ;
  trung vị 32,6 giây. Chế độ này chưa được chấm đủ 36 câu bằng V15.
- `git diff --check` đạt; hash pipeline hiện tại khớp hash của lượt chạy đã chấm.

## So với lượt Qwen đã lưu

| Chỉ số | Qwen chọn nguồn, Gemini viết | Gemini chọn nguồn + viết |
|---|---:|---:|
| Câu hoàn thành / lỗi dịch vụ | 36 / 0 | 36 / 0 |
| Độ trễ trung vị | 60,4 giây | 27,5 giây |
| P95 | 116,1 giây | 37,1 giây |
| Đủ căn cứ theo runtime | 14 | 12 |
| Trả lời một phần | 22 | 24 |
| Không có phần trả lời được hỗ trợ | 0 | 0 |
| Câu phải sửa nội dung một lần | 16 | 22 |
| V15 high / partial / low | 12 / 23 / 1 | 7 / 25 / 4 |
| Request Gemini ở cấp workflow, gồm phân tích | 140 | 153 |

Trung vị giảm khoảng 54,5% so với lượt lịch sử. Số request Gemini tăng vì nhiều câu
cần sửa và kiểm chứng lại; đây không phải kết quả giảm quota hoặc chi phí đã được
xác nhận. Đếm request ở cấp workflow không bao gồm các lần thử lại HTTP bên trong
client/proxy. Tên model `gemini-3.8-flash-high` là alias cấu hình của proxy.

Theo nhãn V15 đã audit: 2 câu tăng nhãn (48, 52), 10 câu giảm nhãn
(21, 24, 26, 36, 37, 38, 45, 49, 51, 56), 24 câu giữ nhãn.
Bốn câu mức low là 24, 28, 36, 45. Không sửa lại câu trả lời đã chấm hoặc bổ sung
số liệu thiếu nguồn để tăng độ khớp mẫu.

## Giới hạn của kết luận

V15 đo khớp nội dung với mẫu, không chứng nhận đúng pháp luật. Audit quote đạt nghĩa
là trích dẫn đối chiếu có thật trong văn bản, không bảo đảm mọi phán đoán ngữ nghĩa
của model chấm đều đúng. Trạng thái đủ căn cứ của runtime cũng là một chỉ số riêng.

Hai lượt dùng cùng bộ câu hỏi và corpus sửa v16, cùng model chấm/đáp án/rubric được
kiểm tra bằng hash. Pipeline code khác nhau và Gemini phân tích câu hỏi lại ở mỗi
lượt, nên đây là so sánh end-to-end với bản lịch sử, không phải A/B dùng nguyên
cùng tập ứng viên truy xuất. Pilot ba câu không đủ để xếp hạng hai chế độ Gemini.

## Báo cáo và cách chạy lại

- [Bảng tổng hợp](../eval/reports/gemini-legal-comparison-v1-20261006.md)
- [Metrics, hash, cấu hình](../eval/reports/gemini-legal-comparison-v1-20261006.json)
- [36 câu trả lời mới](../eval/reports/gemini-combined-36-v1-20261006.json)
- [Kết quả V15 đầy đủ](../eval/reports/gemini-combined-36-v1-v15-review-20261006.json)
- [Pilot hai chế độ](../eval/reports/gemini-pilot-comparison-v1-20261006.json)
- [Kiến trúc và cấu hình](GEMINI_LEGAL_PIPELINE.md)

Báo cáo chứa toàn văn nguồn và quyết định model được giữ cục bộ, đã thêm quy tắc
ignore cho các file thử Gemini. Chưa commit/push các thay đổi của đợt triển khai này.
