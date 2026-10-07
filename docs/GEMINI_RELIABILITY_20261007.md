# Cải tiến độ tin cậy và độ đầy đủ câu trả lời Gemini — 07/10/2026

Phạm vi: thực hiện mục 1–3 theo yêu cầu người dùng: xử lý lỗi chọn nguồn/kiểm chứng, giữ ý đúng khi sửa, và trả lời đủ các ý được nguồn hỗ trợ. Thay đổi nằm trong mã nguồn workspace; lượt thử dùng container đánh giá riêng, không dựng lại API chính.

## Thay đổi

- Kiểm chứng từng ý được sửa JSON tối đa một lần nếu sai schema, thiếu/thừa ID hoặc thay ID nguồn. Phản hồi từ chối hợp lệ không bị gọi lại để tìm một kết quả đồng ý. Trace lưu số lần thử và loại lỗi, không lưu nội dung lỗi thô.
- Bộ chọn Gemini sửa một lần cả lỗi ID trùng/không tồn tại. Hai lần thử là ngân sách chung cho sửa cấu trúc và bổ sung nguồn còn thiếu.
- HTTP 500/502/504 được thử lại tối đa một lần trong thời hạn request ban đầu. Giữ cơ chế dừng/cooldown khi 429/503 và không thử lại timeout. Không đổi khóa để vượt quota.
- Lỗi chọn nguồn vẫn còn trong trace và trạng thái degraded sau khi chuyển sang trích nguồn. Phản hồi dự phòng nói rõ chưa có câu trả lời tổng hợp được kiểm chứng. Khi bộ kiểm chứng không khả dụng, không gọi writer sửa ngữ nghĩa rồi kiểm chứng lại vô ích.
- Khi sửa, giữ nguyên nội dung, thứ tự, nguồn và phân loại của các ý đã được xác nhận và không bị quy tắc kiểm tra bác bỏ. Chỉ kiểm chứng lại các ý mới/đã sửa hoặc chưa đạt. Nếu bước kiểm chứng mới lỗi, các ý cũ còn nguyên và đã được xác nhận vẫn có thể được giữ; ý mới chưa kiểm chứng bị loại.
- Sửa phân loại chỉ áp dụng đúng ID, nội dung và tập nguồn cũ, rồi kiểm chứng lại. Prompt thống nhất rằng hình thức yêu cầu, bên nhận và thời hạn được quy định bởi luật thuộc `regulation` kể cả trong danh sách bước thực hiện.
- Bỏ chỉ dẫn suy ra quyền từ chối ký hợp đồng chỉ từ điều kiện giao dịch tự nguyện. Môi giới: chỉ nêu quyền và điều kiện có nguồn trực tiếp.
- Thêm yêu cầu bao phủ ý dựa trên nguồn đã chọn cho checklist hợp đồng, xử lý dịch vụ môi giới, trách nhiệm nền tảng và yêu cầu xử lý dữ liệu cá nhân. Không lấy câu hỏi bổ sung, cảnh báo chung hoặc trích nguồn không liên quan để tính đủ ý.
- Thiếu ý có nguồn được gửi vào lượt sửa nội dung duy nhất, riêng với lỗi nội dung. Các ý đúng vẫn được giữ. Nếu vẫn thiếu, trả phần đã kiểm chứng và chỉ rõ nhóm ý còn thiếu.

Kiểm tra bao phủ dùng các dấu hiệu từ vựng có phạm vi, không thay thế kiểm chứng ngữ nghĩa và không bảo đảm nhận diện mọi cách diễn đạt. Nguồn không chứa một ý thì cơ chế này không tự bổ sung quy định hoặc số liệu cho ý đó.

## Kiểm thử

- 75 bài kiểm thử liên quan đạt trước thay đổi.
- 20 ca hồi quy mới đạt: sửa JSON/ID, dừng đúng giới hạn, lỗi proxy, giữ ý đã xác nhận, kiểm chứng phần mới, mất dịch vụ trong lúc sửa, phục hồi vị trí ý, bổ sung và thông báo thiếu ý.
- Bộ hồi quy sau sửa: **232 passed**, gồm selector separate/combined, workflow, claim verification, nguồn pháp lý, định tuyến, kiểm tra ranh giới dữ liệu cloud và chatbot. `git diff --check` đạt.
- Khi chạy rộng hơn có test dữ liệu cũ thiếu `infra/db/seeds/dev_chatbot.sql`; test tích hợp API không thu thập được trong môi trường Python máy chủ vì thiếu `selectolax`. Không coi các test này đã đạt. Hai test OCR ban đầu lỗi quyền thư mục tạm đã chạy đạt với thư mục tạm riêng trong workspace và được đưa vào lượt 232 test.

Lệnh tái lập bộ hồi quy:

```powershell
.\.venv\Scripts\python.exe -m pytest apps/api/tests/test_legal_answer_reliability.py apps/api/tests/test_claim_verification.py apps/api/tests/test_agent_workflow.py apps/api/tests/test_gemini_selection.py apps/api/tests/test_gemini_upgrade.py apps/api/tests/test_legal_agents.py apps/api/tests/test_rule_claim_classification.py apps/api/tests/test_legal_only_boundary.py apps/api/tests/test_chatbot.py apps/api/tests/test_compact_legal_answers.py apps/api/tests/test_legal_fix_coverage.py apps/api/tests/test_legal_retrieval.py apps/api/tests/test_priority_legal_facets.py apps/api/tests/test_legal_topic_routing.py -q -p no:cacheprovider --basetemp tmp/pytest-gemini-regression-next-run
```

## Pilot qua dịch vụ thật

Artifact: [gemini_reliability_pilot_20261007.json](../eval/reports/gemini_reliability_pilot_20261007.json).

- IDs: 19, 45, 49, 50, 54; Gemini/separate; model alias cấu hình `gemini-3.8-flash-high`.
- Corpus: `legal_word_repair_v16_20261006`.
- Pipeline SHA256: `be1446d382a8fb9e336f54a55e85009544eed698765a2642824edc7c3c72b9f0`; hash mã nguồn sau lượt thử khớp lúc bắt đầu.
- Kiểm tra legal-only đạt trước khi chạy; chỉ câu hỏi công khai và nguồn pháp lý được phép đi qua các điểm gọi cloud; không có lời gọi cloud cho dữ liệu nhà trọ.
- Hoàn thành **5/5**, lỗi thực thi **0**, trace không có lỗi dịch vụ trong lượt này; cả 5 dùng `gemini-agent`, không phải fallback nguyên văn nguồn.
- 2 câu được đánh dấu partial; ở API, `no_answer=true` còn bao gồm trả lời một phần, không có nghĩa là không có văn bản trả lời.
- Trích dẫn theo rank hợp lệ 5/5. Đây không phải chứng nhận đúng pháp luật.

| Câu | Kết quả quan sát | Sửa nội dung | Thời gian toàn luồng |
|---|---|---:|---:|
| 19 | Checklist thông tin các bên, tiền thuê/cọc, thanh toán, chi phí và bàn giao; các ý đạt được giữ khi sửa phần kết luận | 1 | 44,765 giây |
| 45 | Quyền giảm phí, chấm dứt và bồi thường theo điều kiện nguồn; không bị rơi về trích nguồn | 0 | 26,676 giây |
| 49 | Có nhóm tiếp nhận phản ánh; giữ partial vì nguồn còn thiếu điều khoản dẫn chiếu | 1 | 44,323 giây |
| 50 | Có checklist liên kết lạ, thông tin bảo mật và thúc ép chuyển tiền; giữ partial/giới hạn nguồn tham khảo | 0 | 32,588 giây |
| 54 | Có hình thức gửi yêu cầu, bên nhận, phản hồi và điều kiện thời hạn; không mất các bước hướng dẫn | 0 | 22,267 giây |

Pilot đo lại toàn luồng gồm phân tích và truy xuất. Không so trực tiếp thời gian này với phép replay selector→final của A/B v2. Pilot phân tích/truy xuất lại, không phải A/B trên snapshot cố định; chưa chạy lại 36 câu hoặc chấm V15, không kết luận số nhãn high/low đã cải thiện hay lỗi dịch vụ đã bị loại bỏ vĩnh viễn.

## Tệp triển khai chính

- `apps/api/app/room_service/chatbot/claim_verification.py`, `agents.py`: xác thực và thử sửa verdict.
- `providers.py`, `gemini_selection.py`: thử lại có giới hạn và giữ chẩn đoán khi fallback.
- `agent_workflow.py`, `service.py`: bảo toàn ý đã đạt, kiểm chứng phần sửa, thông báo nguồn tham khảo và kiểm tra bao phủ.
- `answer_coverage.py`: các nhóm ý cần có dựa trên nguồn đã chọn.
- `apps/api/tests/test_legal_answer_reliability.py`: các ca hồi quy mới.
