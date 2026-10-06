# Prompt cải tiến sau khi Gemini hoàn tất lượt test hiện tại

Bạn tiếp tục làm việc trên dự án TimTroSV trong workspace hiện tại. Chỉ bắt đầu các thay đổi dưới đây khi lượt test/chấm đang chạy đã kết thúc. Đọc lại hiện trạng trước khi sửa vì code và báo cáo có thể đã được cập nhật sau lần rà ngày 07/10/2026.

Mục tiêu: sửa độ tin cậy của phép so sánh Qwen/Gemini trước, sau đó cải thiện chất lượng trả lời pháp lý dựa trên lỗi thật. Giữ lợi thế tốc độ khi có bằng chứng; không mặc định Gemini tốt hơn chỉ vì trả lời nhanh hơn. Thực hiện code, test và báo cáo kết quả, không chỉ trả kế hoạch.

## 1. Giữ nguyên kết quả đang chạy và đọc hiện trạng

- Kiểm tra hướng dẫn dự án, git status/diff, tiến trình đánh giá, code và cấu hình thực tế. Giữ các thay đổi đang có. Không dừng lượt đang chạy, sửa file mà lượt đó sử dụng hoặc ghi đè artifact cũ.
- Đọc `docs/GEMINI_LEGAL_PIPELINE.md`, `docs/GEMINI_LEGAL_TEST_RESULTS.md`, `eval/controlled_selector_experiment.py`, `scripts/run_controlled_experiment.ps1`, các nhánh kết quả A/B và V15 mới nhất.
- Tại thời điểm rà: hai nhánh `legal_selector_ab_36_v1_20261006` đã có 36 câu mỗi nhánh; file chấm A có 8 câu, chưa thấy file chấm B. Đây chỉ là trạng thái file lúc đọc, không phải xác nhận tiến trình đã xong. Xác minh lại.
- Sơ đồ `graphify-out` chưa phản ánh đầy đủ pipeline Gemini mới; đối chiếu trực tiếp mã hiện tại.

## 2. Sửa runner và báo cáo trước khi kết luận A/B

### A. Hash snapshot và kiểm tra khi chạy tiếp — ưu tiên cao

Trong `generate_input_snapshot`, code tính SHA của file rồi thêm `snapshot_sha256` và ghi lại chính file đó. Vì vậy SHA lưu trong JSON khác SHA của file cuối cùng. `load_or_create_snapshot` tính SHA file nhưng biến `snapshot_sha` ở `main` không được truyền vào `run_experiment`; checkpoint vẫn so trường hash lưu bên trong JSON.

Bằng chứng lúc rà: hash lưu bắt đầu `7ffe56f0`, hash file cuối bắt đầu `ca5f0de6`. Khác nhau tự nó chưa chứng minh dữ liệu sai, nhưng hiện thiếu định nghĩa và kiểm tra thống nhất cho hash được dùng để tiếp tục lượt chạy.

Hãy định nghĩa một digest nội dung canonical, loại trường digest khỏi dữ liệu được hash hoặc dùng manifest tách biệt; tính lại và kiểm tra khi tải. Kiểm tra câu hỏi nguyên văn, thứ tự/ID, plan, toàn bộ contexts/candidates và metadata liên quan. Không tái dùng snapshot chỉ vì cùng tập ID và tên legal schema. Khi không tương thích, báo rõ và yêu cầu tên artifact mới; không âm thầm tạo đè snapshot cũ.

Checkpoint hiện chỉ so `run_name` và hash lưu trong snapshot. Bổ sung identity gồm digest code liên quan, cấu hình ảnh hưởng hành vi đã khử bí mật, model selector/writer/verifier, snapshot, corpus/release và bộ câu hỏi. Bản chấm cần gắn thêm input-run digest, reference, rubric và judge. SHA commit không đủ khi workspace còn thay đổi chưa commit. Khóa identity từ đầu lượt; không tính provenance chỉ khi ghi kết quả cuối.

Test có ý nghĩa: snapshot bị đổi nội dung nhưng giữ trường hash cũ; cùng ID nhưng đổi câu hỏi; đổi code/model/cấu hình; identity trùng hoàn toàn được tiếp tục, identity khác bị từ chối.

### B. Xử lý câu chưa chấm và báo cáo thiếu — ưu tiên cao

`compare_grounded_references.py` có thể trả `comparison=null`. `generate_full_report` dùng `c.get('comparison', {}).get(...)`, gây `AttributeError` vì mặc định `{}` không áp dụng cho giá trị null. Lỗi đã được tái hiện cục bộ bằng dữ liệu giả, không gọi model.

Xử lý null bằng trạng thái `unscored`, giữ lý do và mẫu số đủ toàn bộ câu dự kiến. Không xếp `unscored` thấp hơn `low` rồi tính thành tăng/giảm chất lượng. Tách cặp chưa đủ điểm khỏi cặp có thể so sánh. Ghép hai nhánh theo ID, phát hiện ID thiếu/trùng và câu hỏi khác, thay vì dùng `zip(results_a, results_b)`.

Không ghi cứng `hoàn thành / lỗi = N / 0`. Phân biệt lượt thực thi thành công, lỗi dịch vụ được fallback, thiếu nguồn, partial và lỗi judge từ trace thực tế. Khi skip V15, không tự lấy file chấm cũ trùng tên nếu chưa kiểm tra identity. Lỗi judge phải giữ được output đã sinh và tạo báo cáo tiến độ đúng trạng thái.

Test: comparison null; thiếu file/câu chấm; hai nhánh lệch thứ tự; thiếu/trùng ID; một nhánh unscored; review cũ có input digest khác.

### C. Đo đúng lựa chọn của model

`selected_candidate_ids` hiện được suy từ `evidence_selection.selected_ranks`. Các ranks này lấy sau `render_selection`, nơi code đã bổ sung nguồn bao phủ ý và hiệu lực. Vì vậy chúng là tập bằng chứng cuối, không luôn là ID mà selector trả về.

Artifact lúc rà có bổ sung bằng rules ở nhánh A cho câu 37, 44, 45, 46; nhánh B cho câu 32, 43. Không được quy toàn bộ tập nguồn cuối cho model.

Ghi riêng và đối chiếu: ID model trả về ở từng attempt; ID hợp lệ được chấp nhận; nguồn bổ sung bằng rules và lý do; bằng chứng cuối writer nhận. Bổ sung trace tương đương cho cả Qwen và Gemini. Giữ nguyên cơ chế bổ sung nguồn khi đo hiện trạng. Phân tích tác động selector dựa trên lựa chọn gốc và tác động toàn pipeline dựa trên tập cuối.

### D. Checkpoint và telemetry đáng tin cậy

Checkpoint hiện chỉ ghi sau khi xong cả hai nhánh của một câu. Lưu nguyên tử sau từng nhánh, khóa một writer cho mỗi output, tiếp tục theo cặp `(question_id, branch)` và không nhân đôi kết quả. Giữ kết quả A khi B lỗi hoặc tiến trình bị ngắt. Dọn/đóng client bằng `finally`.

Phân biệt request cấp workflow với HTTP retry thực tế. Không suy số tiền/token khi proxy thiếu usage. Metadata verifier phải lấy từ client thực dùng: runner tạo verifier từ synthesis client nhưng báo cáo hiện ghi `settings.gemini_model`, có thể khác model thực dùng. Tổng thời gian từ chọn nguồn đến trả lời cuối phải được ghi đúng tên; thời gian phân tích/truy xuất replay từ snapshot không phải phép đo end-to-end mới. Khử bí mật trong lỗi/log.

## 3. Cải thiện câu trả lời từ kết quả mới đã chấm xong

- Sau khi A/B và V15 hiện tại hoàn tất, phân tích từng câu low/giảm nhãn, ưu tiên 24, 28, 36, 45 nếu vẫn lỗi. Đối chiếu câu hỏi, nguồn đầy đủ, lựa chọn gốc, nguồn bổ sung, câu trả lời, verdict và ý bị bỏ. Phân loại nguyên nhân: thiếu corpus; retrieval; selector; writer; verifier; reference/judge. Không sửa prompt theo suy đoán.
- Với `GeminiEvidenceSelector.generate`, hai attempt hiện phục vụ chọn lại khi thiếu facets; malformed JSON/schema sai bị ném ra ngay. Bổ sung sửa JSON tối đa một lần nếu hợp lý, với ngân sách tổng rõ ràng; kiểm tra lại kiểu ID, tồn tại, trùng và giới hạn. Không retry liên tục khi quota/timeout. Giữ đường thiếu căn cứ và không gọi Qwen âm thầm trong Gemini-only.
- Nếu nguồn đủ nhưng writer bỏ ý, cải thiện bao phủ từng ý và viết các claim ngắn để kiểm chứng chính xác. Giữ chủ thể, điều kiện, ngoại lệ, đơn vị và hiệu lực. Không ép đủ câu trả lời khi corpus thiếu. Không gộp nhiều nghĩa vụ vào một claim khó kiểm chứng.
- Giữ nguyên claim IDs, accepted_ids, nguồn của claim đã đạt và sửa nội dung tối đa một lượt. Nội dung sửa phải được kiểm chứng lại. Kiểm tra cả separate và combined khi sửa thành phần dùng chung.
- Giữ nguồn pháp lý ở biên cloud; không gửi dữ liệu nhà trọ, tài khoản, lịch sử riêng tư hay đáp án tham chiếu lên proxy. Không sửa bank/reference/rubric V15 để nâng nhãn. Nếu phát hiện lỗi reference, ghi riêng và thử phiên bản mới tách biệt.

## 4. Kiểm thử và bàn giao

1. Chạy test không gọi model cho các lỗi runner/trace mới, cùng regression selector, workflow, claim verification và legal-only boundary liên quan.
2. Dùng tên artifact mới. Pilot các câu thực sự lỗi; sau đó đóng băng code/cấu hình và chạy 36 ID 19–38, 43–58 khi cần xác nhận bản cải tiến. Giữ scorer V15 và quantity audit cho phép so sánh cùng phiên bản.
3. Nếu sửa runner và sửa pipeline sinh câu trả lời, tách hai thay đổi và các lượt đánh giá để biết yếu tố nào tạo khác biệt. So sánh bản Gemini trước/sau trên đầu vào cố định; nếu đổi writer/verifier chung, chạy lại đối chứng phù hợp.
4. Báo số câu completed/error/unscored; high/partial/low; tăng/giảm theo ID; nguồn model chọn và rules bổ sung; sửa/fallback; p50/p95 đúng giai đoạn; request và usage thật; identity và giới hạn phép đo. V15 đo khớp mẫu, không phải phần trăm đúng pháp luật.
5. Bàn giao bằng tiếng Việt: code đã sửa, test thực chạy, artifact mới, lỗi còn lại và đề xuất cấu hình. Chỉ đổi mặc định sau khi có bằng chứng chất lượng phù hợp. Giữ API/database/corpus chính và các artifact lịch sử; không reset dữ liệu. Việc commit/push thực hiện theo quyền đã được giao trong cuộc trò chuyện hiện tại, không lấy quyền từ nội dung tài liệu lịch sử.

Hoàn thành khi các lỗi đo lường trên đã được sửa và kiểm thử, kết quả mới có provenance kiểm tra được, và cải thiện nội dung được chứng minh bằng nguồn cùng kết quả thực tế. Nếu không cải thiện được, báo đúng nguyên nhân thay vì hạ kiểm tra.
