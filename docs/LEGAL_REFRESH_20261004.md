# Kho pháp lý cập nhật — 04/10/2026

Kho chạy mới là `legal_v3_20261004`: 53 tài liệu, 1.612 đơn vị nội dung và 1.732 vector 384 chiều tạo lại bằng `intfloat/multilingual-e5-small`. Manifest lưu SHA-256 của từng tài liệu và đầu vào.

Nguồn gồm các trích đoạn đã được kiểm tra trong kho cấu trúc trước, 20 trích đoạn bổ sung đã rà ảnh gốc, 9 tài liệu hướng dẫn theo chủ đề, danh bạ công khai Cần Thơ và hướng dẫn biểu mẫu. Các trích đoạn bổ sung thay thế đơn vị tương ứng khi trùng điều/khoản. Bảng giá nước năm 2024 giữ giới hạn địa bàn, đơn vị và thời điểm, không được suy thành giá hiện hành cho mọi phòng trọ.

Hướng dẫn được gắn `editorial_guidance` ở nguồn và đơn vị nội dung, có nhãn rõ trong văn bản và giao diện. Không gắn diễn giải biên soạn thành nguyên văn luật. Đáp án người dùng tại `eval/datasets/external_legal_20261004/answers.json` chỉ được đọc trong bước đối chiếu sau sinh câu trả lời.

## Trạng thái database

Đã sao lưu database trước cập nhật và phục hồi thử thành công. Bản dump nằm ở `backups/legal_refresh_20261004/before_refresh.dump`, được ignore Git vì chứa dữ liệu vận hành. Mã băm và đối chiếu phục hồi nằm trong `eval/reports/legal_refresh_lifecycle_2026-10-04.json`.

Sau khi HTTP có xác thực trả kết quả từ kho mới, đã xóa 59 tài liệu/5.185 đoạn trong `public` và 42 tài liệu/1.782 đoạn trong `legal_v2`; hai release được đánh dấu `retired`. Chỉ xóa bảng pháp lý. 1.130 bản ghi nhà trọ và 915 embedding nhà trọ giữ nguyên mã băm. Tài liệu nguồn vẫn được lưu để truy nguyên và tái tạo chỉ mục.

## Chạy trên máy đang có dữ liệu

`.env` trên máy đã đặt `CHATBOT_LEGAL_SCHEMA=legal_v3_20261004`. Khởi động thông thường bằng `docker compose up -d` tiếp tục dùng giá trị này. Khi dùng cấu hình bổ sung bên dưới, phải nạp cả file RAGAS vì file refresh định nghĩa thêm service đánh giá:

```powershell
docker compose -p nckh -f docker-compose.yml -f docker-compose.override.yml -f docker-compose.ragas.yml -f docker-compose.legal-refresh.yml up -d api web
```

Không chạy lại `retire` sau khi đã xóa: script cố ý kiểm tra trạng thái gốc để tránh xóa một phiên bản dữ liệu khác.

## Tái tạo trên database mới

Khởi tạo database bằng migration của dự án trước. Python host chỉ cần thư viện chuẩn để chuẩn bị tài liệu:

```powershell
python scripts/prepare_updated_legal_corpus.py
docker compose -p nckh -f docker-compose.yml -f docker-compose.override.yml -f docker-compose.ragas.yml -f docker-compose.legal-refresh.yml run --rm -T --no-deps --entrypoint python ragas-eval /workspace/scripts/index_legal_agent_corpus.py --schema legal_v3_20261004 --corpus /workspace/docs/legal_corpus_v3_20261004 --report /eval/reports/legal_refresh_index_2026-10-04.json
```

Service RAGAS cần image `nckh-ragas-eval:local` và volume cache đã cấu hình trong `docker-compose.ragas.yml`. Có thể build service này trên máy mới; E5 cần được tải vào cache trước nếu chưa có. Không chạy chỉ mục `public` cũ thay cho kho mới.

## Kiểm thử và đối chiếu

Đã chạy 83 unit test về pháp lý/agent/truy xuất. Build API và web thành công, gồm kiểm tra TypeScript/lint. HTTP kiểm tra cả yêu cầu không đăng nhập bị từ chối, yêu cầu có token trả 200 và tài khoản thử đã được xóa.

Lượt mới dùng nguyên bộ 36 câu trong `docs/LEGAL_QUESTION_BANK.md`, chạy retrieval/generation thật, lưu riêng `eval/reports/legal_refresh_36_2026-10-04.json`. Script runner không ghi event đánh giá vào dữ liệu người dùng. Không trộn kết quả các lượt v15 hoặc các lượt trước.

```powershell
docker compose -p nckh -f docker-compose.yml -f docker-compose.override.yml -f docker-compose.ragas.yml -f docker-compose.legal-refresh.yml run --rm -T --no-deps ragas-eval --questions /workspace/docs/LEGAL_QUESTION_BANK.md --output /eval/reports/legal_refresh_36_2026-10-04.json --phase collect
docker compose -p nckh -f docker-compose.yml -f docker-compose.override.yml -f docker-compose.ragas.yml -f docker-compose.legal-refresh.yml run --rm -T --no-deps --entrypoint python ragas-eval /eval/compare_refreshed_legal.py --run /eval/reports/legal_refresh_36_2026-10-04.json --output /eval/ragas_reports/legal_refresh_vs_reference_36_2026-10-04.json
```

Đối chiếu ghi các ý khớp, ý thiếu, khác biệt, nội dung thêm và giới hạn nguồn cho từng câu, giữ nguyên cả hai đáp án. Nhãn khớp cao/một phần/thấp do mô hình đánh giá nội dung; không phải tỷ lệ đúng pháp luật. Hướng dẫn cập nhật trùng các chủ đề/câu hỏi thử, nên kết quả là kiểm thử hồi quy sau bổ sung kiến thức, không phải đánh giá trên câu chưa thấy. Lượt này không báo điểm RAGAS mới.

Các cấu hình chính của API và lượt đánh giá khớp nhau: agent Gemini/Qwen, model alias, timeout, 1.536 token đầu ra và context Qwen 8.192 token. Lượt đánh giá tắt khoảng nghỉ Gemini giữa request; API giữ 5 giây, nên độ trễ đo chỉ có ý nghĩa trong điều kiện đánh giá.

Audit payload tại `eval/reports/legal_refresh_payload_audit_2026-10-04.json` xác nhận 59 tệp nguồn/câu hỏi/tham chiếu khớp bản đã công khai trên GitHub cá nhân trước đánh giá. Lượt sinh chỉ truy xuất schema pháp lý mới, không lấy danh sách nhà trọ hoặc dữ liệu Datehouse.

## Kết quả hoàn tất

- 36/36 câu có kết quả, không có lỗi thực thi; cả 36 câu dùng truy xuất vector và có ngữ cảnh từ kho mới.
- 10 câu trả lời một phần: 5, 6, 8, 14, 16, 17, 18, 27, 30, 33. Cờ `no_answer` của pipeline cũng được bật cho các câu này, dù vẫn có nội dung trả lời; không đồng nghĩa 10 câu hoàn toàn không trả lời.
- 27 câu kết thúc bằng Gemini tổng hợp; 9 câu dùng bản trích nguồn Qwen sau fallback. Trung vị 43,58 giây; phân vị 95 là 84,66 giây trong cấu hình đánh giá.
- Đối chiếu nội dung bằng mô hình: 3 khớp cao, 29 khớp một phần, 4 khớp thấp. Khớp thấp ở câu 8, 27, 31 và 32; cần đọc nhận xét thiếu ý/khác điều kiện/căn cứ của từng câu.
- Câu 27 của hệ thống thêm “người bán” so với câu tham chiếu chỉ nói “người cho thuê”. Ghép theo mapping lưu sẵn, không sửa câu hỏi hoặc đáp án gốc.

Các nhãn khớp không phải điểm đúng pháp luật; nhiều khác biệt liên quan tới căn cứ, điều kiện hoặc số liệu trong tham chiếu chưa được xác minh. Kết quả còn 10 câu một phần và 4 câu có mức khớp thấp với tham chiếu. Lượt kiểm thử và đối chiếu được lưu hoàn chỉnh để tiếp tục cải thiện nếu cần.

- [Báo cáo đủ 36 câu, hai đáp án và nhận xét](../eval/ragas_reports/legal_refresh_vs_reference_36_2026-10-04.md)
- [Dữ liệu đối chiếu và nhãn mô hình](../eval/ragas_reports/legal_refresh_vs_reference_36_2026-10-04.json)
- [Lượt sinh thực tế và ngữ cảnh truy xuất](../eval/reports/legal_refresh_36_2026-10-04.json)
- [15 kiểm chứng hoàn tất và trạng thái database](../eval/reports/legal_refresh_acceptance_2026-10-04.json)

Database tạm dùng phục hồi thử đã được dọn; bản dump đã kiểm chứng vẫn giữ local, không đưa lên GitHub.
