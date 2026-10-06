# Prompt bàn giao cho Gemini Antigravity

> Cập nhật 06/10/2026: workspace đã có Gemini selector và hai chế độ `separate` /
> `combined`, cùng kiểm thử trong `test_gemini_selection.py`. Đọc
> [GEMINI_LEGAL_PIPELINE.md](GEMINI_LEGAL_PIPELINE.md) và báo cáo thử mới trước khi
> làm tiếp; không triển khai lại phần đã hoàn thành. Nhánh hiện tại lúc cập nhật
> là `codex/legal-review-repair-20261006`; các thông tin lịch sử bên dưới cần xác
> minh lại. Prompt này là nội dung bàn giao; bản cập nhật code hiện tại chưa tự
> commit/push hoặc thay container API chính.
> Đợt thử đã hoàn tất: đọc [GEMINI_LEGAL_TEST_RESULTS.md](GEMINI_LEGAL_TEST_RESULTS.md).
> Combined nhanh hơn nhưng khớp mẫu V15 giảm; không coi nó là bản đã đạt điều kiện
> thay thế mặc định. Separate mới được thử pilot ba câu.

Bạn tiếp quản dự án của tôi và thực hiện công việc đến khi có code, kết quả kiểm thử thật và các commit đã push. Đọc toàn bộ yêu cầu này trước khi sửa. Hãy làm theo thứ tự: **kiểm tra hiện trạng → commit/push checkpoint → làm bản thay Qwen bằng Gemini proxy → kiểm thử và đánh giá → commit/push kết quả**. Không chỉ trả lời bằng kế hoạch.

## 1. Dự án và mục tiêu

- Workspace hiện tại: `D:\AI-powered-system-to-assist-Can-Tho-University-students-in-finding-accommodation--main`.
- Shell: PowerShell trên Windows; ứng dụng chạy bằng Docker Desktop.
- Remote origin tại thời điểm bàn giao: `https://github.com/nhuy2005-alexandors/AI-powered-system-to-assist-Can-Tho-University-students-in-finding-accommodation-.git`.
- Nhánh tại thời điểm bàn giao: `codex/legal-priority7-20261006`. Xác minh lại trước khi thao tác.
- Mục tiêu: dùng Gemini qua proxy đã cấu hình để thay Qwen ở bước **chọn bằng chứng trong luồng trả lời pháp lý**. Gemini tiếp tục phân tích câu hỏi, tổng hợp và kiểm chứng. Giữ E5 embedding cục bộ, truy xuất hybrid, graph và kiểm tra bằng mã.
- Luồng tương tác pháp lý ở chế độ mới phải hoạt động khi Ollama không khả dụng; không âm thầm gọi Qwen để chọn nguồn hoặc kiểm chứng. Giữ khả năng chọn Qwen trong cấu hình đối chứng nếu cần A/B.
- Qwen có thể tiếp tục làm **judge ngoại tuyến** cho bộ chấm V15 để giữ cùng phương pháp so sánh. Việc này tách biệt với thay Qwen trong luồng trả lời. Không đổi judge lẫn rubric giữa hai bản rồi so trực tiếp.
- “Xây dựng lại” nghĩa là sửa/refactor phần cần thiết trên kiến trúc hiện có, build và kiểm thử bản mới; không xóa dự án, database hoặc viết lại toàn bộ ứng dụng.

Bạn được yêu cầu thực hiện sửa code, tạo nhánh, commit, push và chạy kiểm thử liên quan. Tự xử lý lựa chọn triển khai thông thường. Chỉ hỏi khi thực sự thiếu thông tin/credential, có xung đột không xác định được ý người dùng, hoặc gặp thao tác ngoài phạm vi này. Không tự đổi remote, cấp quyền rộng hơn, công khai dữ liệu hoặc merge vào main.

## 2. Kiểm tra và push checkpoint trước khi sửa

1. Đọc AGENTS.md và hướng dẫn dự án nếu có. Kiểm tra git status, diff, nhánh, upstream, remote và các tiến trình/container đánh giá đang chạy. Không mặc định workspace sạch.
2. Đọc các thay đổi hiện có để phân biệt công việc đã làm, dữ liệu riêng tư và file sinh ra. Không reset, clean, stash rồi bỏ quên, hoặc ghi đè thay đổi của người dùng.
3. Rà `.gitignore` và những file dự định stage. Đặc biệt các file `legal_repair_*.json` mới có thể chưa được ignore dù các file `graph_rag_*.json` đã được ignore. Không coi một file untracked là được phép public.
4. Chỉ stage rõ từng file code, test, cấu hình mẫu và tài liệu kỹ thuật phù hợp. Không dùng `git add .` hoặc force-add toàn bộ.
5. Không push `.env`, khóa/token, cấu hình proxy chứa credential, `docker-compose.override.yml` riêng tư, DB dump/backup, dữ liệu nhà trọ nội bộ, payload hội thoại, đáp án tham chiếu, báo cáo chứa nguyên văn dữ liệu riêng tư, model cache hoặc log nhạy cảm. Kiểm tra cả diff staged và nội dung nhạy cảm trong commit chưa push.
6. Giữ nguyên các artifact đánh giá ở máy local và ghi hash phục vụ đối chiếu. Nếu cần, bổ sung ignore có phạm vi cụ thể. Không xóa artifact để làm sạch git.
7. Tạo checkpoint commit cho phần công việc hiện tại phù hợp để đưa lên Git; commit message phải nói đây là checkpoint nếu kiểm thử chưa hoàn tất. Push nhánh hiện tại tới origin, không force-push. Xác minh remote branch chứa đúng SHA và báo SHA checkpoint.
8. Nếu push thất bại vì xác thực/quyền, ghi lỗi đã khử bí mật, giữ commit local và yêu cầu đúng phần còn thiếu; không báo push thành công. Chỉ bắt đầu sửa kiến trúc sau khi checkpoint đã push thành công.
9. Từ checkpoint, tạo nhánh mới, ví dụ `codex/gemini-proxy-selector-20261006`, tránh ghi đè nhánh đã tồn tại. Ưu tiên worktree riêng tại vị trí được phép. Các tiến trình đánh giá cũ có thể bind-mount workspace gốc: không sửa file bên dưới một lượt đang chấm hoặc cho hai tiến trình ghi chung JSON.
10. File ignored như cấu hình local/corpus/báo cáo sẽ không tự có trong worktree mới. Cấp cho môi trường thử đường dẫn đọc phù hợp, giữ bí mật ở runtime; không đưa chúng vào Git để giải quyết vấn đề mount.

## 3. Hiện trạng cần hiểu trước khi thay đổi

Thông tin dưới đây là snapshot ngày 06/10/2026, phải kiểm tra lại thực tế:

- Frontend Next.js → `/api/chat/ask` → FastAPI `/chat/ask` → ChatService.
- PostgreSQL lưu dữ liệu, vector pgvector, chỉ mục văn bản và graph dạng bảng nodes/edges.
- Embedding: `intfloat/multilingual-e5-small`, vector 384 chiều.
- API chính dùng `legal_word_v7_20261005`, `housing_graph_word_v6`, `graph_rag_word_v6`.
- Bản thử mới dùng `legal_word_repair_v16_20261006`, `housing_graph_word_repair_v16`, `graph_rag_word_repair_v16`.
- API chính là image cũ, chưa có module kiểm chứng từng kết luận của bản sửa. Workspace hiện có cải tiến per-claim verification, sửa một lượt, giữ các ý đã qua kiểm chứng. Phát triển từ bản sửa này; không làm mất các cải tiến đó.
- Qwen hiện là `qwen3.5:9b` qua Ollama. Tên model Gemini đang cấu hình là `gemini-3.8-flash-high`; đó là alias cấu hình, không tự khẳng định model thực tế phía sau proxy.
- Proxy đã từng dùng đường dẫn `http://127.0.0.1:8317/v1beta` từ host. Trong container, địa chỉ có thể dùng `host.docker.internal`. Đọc cấu hình đang chạy để lấy đúng endpoint. Không hardcode localhost vào container, không tự chuyển sang API Google trực tiếp và không in credential.
- Trace 36 câu bản sửa ghi nhận trung vị: Qwen chọn bằng chứng khoảng 35 giây; toàn bộ trả lời khoảng 60,4 giây. Gemini ở các bước khác có payload khác, nên không suy ra tốc độ Gemini chọn nguồn khi chưa đo.
- 16 câu được selector đánh dấu partial không đồng nghĩa 16 lỗi của Qwen; có thể thiếu nguồn hoặc điều kiện. Cần phân tích nguyên nhân.

Đọc tối thiểu các file sau, đường dẫn tính từ workspace:

```text
docs/LEGAL_REPAIR_PROGRESS_20261006.md
docs/WORD_ONLY_TENANT_SUPPORT_20261005.md
apps/api/app/config.py
apps/api/app/room_service/chatbot/router.py
apps/api/app/room_service/chatbot/service.py
apps/api/app/room_service/chatbot/providers.py
apps/api/app/room_service/chatbot/agents.py
apps/api/app/room_service/chatbot/agent_workflow.py
apps/api/app/room_service/chatbot/source_selection.py
apps/api/app/room_service/chatbot/claim_verification.py
apps/api/app/room_service/chatbot/evidence_units.py
apps/api/app/room_service/chatbot/legal_retrieval.py
apps/api/app/room_service/chatbot/graph_retrieval.py
eval/graph_rag_question_bank.py
eval/question_bank_ragas.py
eval/legal_only_boundary.py
eval/compare_grounded_references.py
eval/quantity_audit.py
eval/run_legal_repair_comparison.py
eval/report_legal_repair.py
docker-compose.legal-review.yml
```

## 4. Triển khai Gemini chọn bằng chứng

### Cấu hình và nối workflow

Thêm cấu hình provider riêng cho chọn nguồn pháp lý, ví dụ:

```text
CHATBOT_LEGAL_SELECTION_PROVIDER=gemini|qwen
CHATBOT_LEGAL_SELECTION_MODEL=<alias thực sự được proxy hỗ trợ>
CHATBOT_LEGAL_SELECTION_TIMEOUT_SECONDS=<giới hạn hợp lệ>
```

Tên có thể điều chỉnh theo convention của repo. Dùng lại client Gemini hiện có và GEMINI_BASE_URL/runtime credentials. Không thêm API key vào code, prompt bàn giao hoặc báo cáo.

Không chỉ đặt `CHATBOT_LLM_PROVIDER=gemini`: `router.py` hiện vẫn thêm OllamaQwenGenerator khi `chatbot_agents_enabled=true`, với `legal_answer_mode='source_select'`. Phải sửa điểm nối thật. Rà cả warmup, verifier fallback, test runner và metadata provider. Không để warmup Qwen gây chậm startup khi chế độ Gemini không sử dụng nó.

Tách giao diện chọn nguồn dùng chung thay vì sao chép toàn bộ workflow. Qwen và Gemini phải dùng cùng candidate builder, quy tắc kiểm tra và hàm khôi phục nguyên văn để A/B công bằng.

### Hợp đồng đầu vào/đầu ra

Gemini nhận câu hỏi và những đoạn pháp lý được truy xuất, có ID, nội dung, nguồn và trạng thái đầy đủ ngữ cảnh. Đầu ra chỉ chứa:

```json
{"selected_ids": [1, 3], "insufficient": false}
```

- Giữ giới hạn hiện có: tối đa 4 ID chính, cùng giới hạn candidate/ngữ cảnh ở hai nhánh A/B.
- Kiểm tra kiểu dữ liệu nghiêm ngặt, trường bắt buộc, ID tồn tại, không trùng, không vượt số lượng và bool đúng kiểu. Không để true được hiểu thành ID integer.
- Mã lấy nguyên văn từ ID; không yêu cầu model viết lại nguồn rồi coi là bằng chứng.
- Giữ điều kiện, ngoại lệ, chủ thể, số liệu, đơn vị, hiệu lực và scope_warning. Giữ bổ sung nguồn theo nhóm ý đang có trong source_selection/evidence_units.
- Xử lý trường hợp không có nguồn, chọn rỗng, malformed JSON, output bị cắt, timeout, 429/5xx và proxy không thực thi schema. Dùng retry có giới hạn, ghi trace và trả thiếu căn cứ/trích đoạn hợp lệ; không retry vô hạn hoặc xoay khóa để né quota.
- Schema chỉ kiểm tra cấu trúc. Tiếp tục kiểm tra giá trị và ngữ nghĩa theo nguồn ở tầng sau.
- Nếu Gemini hỏng trong chế độ Gemini-only, không âm thầm gọi Ollama. Dùng đường dự phòng bằng mã/nguồn đã xác nhận hoặc thông báo thiếu căn cứ. Qwen chỉ được dùng khi lựa chọn provider/chế độ đối chứng cho phép rõ ràng.
- Giữ một lượt sửa có giới hạn, claim IDs, phân loại regulation/procedure/recommendation/source_limit, accepted_ids và partial retention của bản sửa. Nội dung sửa phải qua kiểm chứng lại.
- Ghi provider/model được yêu cầu và thực tế nếu phản hồi có cung cấp, thời gian từng bước, số retry/fallback, số đoạn và số token nếu API trả về. Không bịa số token hoặc chi phí khi proxy không cung cấp.

## 5. Dữ liệu và phép so sánh

- Giữ câu hỏi, tham chiếu, rubric V15, kiểm tra số liệu và corpus v16 trong phép A/B đầu tiên. Chỉ thay selector. Nếu phát hiện cần sửa corpus/rubric, tách thành phiên bản/lượt riêng, không gộp vào kết luận selector tốt hơn.
- Không đưa đáp án mẫu vào prompt sinh, embedding hoặc corpus. Không sửa mẫu cho giống câu trả lời hệ thống.
- Giữ dữ liệu nhà trọ và tài khoản cục bộ. Nhánh tìm phòng tiếp tục truy xuất có bộ lọc và trình bày có cấu trúc; không chuyển dữ liệu nhà trọ lên proxy khi thay selector pháp lý.
- `eval/legal_only_boundary.py` đã chặn listing retrieval và kiểm tra nguồn trước writer/verifier. Khi thêm selector Gemini, bổ sung chốt kiểm tra **trước lần gọi cloud selector mới**, không dựa vào tên biến context_kind hoặc kiểm tra sau khi đã gửi.
- Rà mounts thực tế; một comment “không mount catalog” không chứng minh dữ liệu chưa được mount/gửi. Không thay cấu hình DB/corpus API chính khi đang thử.
- Không drop/truncate/reset database, không chạy seed/reset_all, không xóa corpus hoặc khởi động crawler/seed lịch sử. Giữ 789 bản ghi nhà trọ và các tài khoản hiện có.

Ba artifact lịch sử cần giữ nguyên nếu còn tồn tại:

```text
eval/reports/graph_rag_priority7_36_v20_2026-10-06.json
eval/reports/legal_repair_36_v20_20261006.json
eval/reports/legal_repair_baseline_36_v15_20261006.json
```

Chúng lần lượt phục vụ baseline lịch sử, bản sửa với Qwen selector và kết quả chấm đã lưu. Kiểm tra tình trạng thật, không giả định lượt chấm đã xong. Baseline lịch sử khác cả code/corpus nên không dùng một mình để kết luận tác động riêng của đổi selector.

## 6. Kiểm thử theo thứ tự

### A. Unit/regression, không gọi model thật

Chạy các nhóm liên quan và bổ sung test có ý nghĩa cho thay đổi mới:

```text
apps/api/tests/test_agent_workflow.py
apps/api/tests/test_legal_agents.py
apps/api/tests/test_source_grounded.py
apps/api/tests/test_claim_verification.py
apps/api/tests/test_rule_claim_classification.py
apps/api/tests/test_legal_only_boundary.py
apps/api/tests/test_reference_quote_audit.py
apps/api/tests/test_priority_legal_facets.py
apps/api/tests/test_compact_legal_answers.py
```

Test mới phải bao phủ chọn provider thực sự, bảo toàn nguyên văn/ID/điều kiện, lỗi proxy/JSON/ID, retry giới hạn, không gọi Qwen khi Ollama bị tắt, không gửi listing/reference lên cloud và không làm mất claim đã được xác nhận. Thêm spy/mock để xác minh client Ollama không được gọi trong lượt chat Gemini.

Tài liệu cũ ghi 125 test workflow + 49 test bộ chấm; đây là lịch sử, không phải kết quả chạy của bạn. Báo số test thực tế. Dùng runtime/container dự án phù hợp; tránh chạy test CRUD rộng làm phát sinh dữ liệu vào DB người dùng.

### B. Smoke và pilot với proxy thật

1. Xác minh endpoint/model bằng một request pháp lý công khai tối thiểu, không log key. Không suy ra proxy hoạt động chỉ từ config.
2. Audit nguồn/hash/schema, rồi preflight legal-only trước khi gọi model hàng loạt.
3. Chạy pilot các câu 19, 23, 26, 27, 28, 29, 30, 31, 32, 34, 36, 37, 45, 47, 50, 58 (ID ngân hàng gốc).
4. Kiểm tra các bẫy đã gặp: điều kiện 30 ngày khác hạn nộp 30 ngày; điều kiện thu điện; phân chia nước là thỏa thuận khi nguồn chỉ hỗ trợ thỏa thuận; giảm phí dịch vụ không tự động hoàn 100%; cảnh báo link/OTP; phạm vi người bán/nền tảng; giấy tờ và chứng cứ có trong nguồn; nguyên văn điều kiện xuống dòng.
5. Rà trực tiếp trace và nguồn các câu ưu tiên, không chỉ nhìn nhãn complete/partial. Sửa lỗi thực tế rồi chạy lại đúng phần bị ảnh hưởng bằng artifact mới; chỉ dùng một pipeline đóng băng cho lượt đầy đủ.

### C. A/B có kiểm soát và chạy đủ 36 câu

- Bộ 36 ID là **19–38 và 43–58**. Cùng câu hỏi nguyên văn và thứ tự cho hai nhánh.
- Để đo selector, lưu câu hỏi và tập candidate pháp lý đã truy xuất rồi cho Qwen/Gemini chọn trên đúng cùng tập candidate. Đo độ bao phủ các ý, chọn sai phạm vi, điều kiện bị bỏ, số retry, thời gian và token nếu có. Nhãn insufficient tự khai không phải ground truth.
- Sau pilot, chạy đủ 36 câu qua service thật bằng Gemini selector; chạy đối chứng Qwen trên cùng code/corpus nếu artifact cũ không bảo đảm cùng đầu vào/cấu hình. Không cần sinh lại artifact lịch sử đã đóng băng.
- Lưu output tên mới, chẳng hạn `gemini_selector_36_<timestamp>.json` và `qwen_selector_control_36_<timestamp>.json`. Không ghi đè v20/V15 cũ.
- Snapshot manifest, câu hỏi, cấu hình provider đã khử bí mật, pipeline SHA và model alias. Identity/resume phải phát hiện cả thay đổi cấu hình provider/model, không chỉ hash file Python.
- Chỉ resume khi toàn bộ identity tương thích. Checkpoint sau mỗi câu; không cho nhiều tiến trình ghi chung output.
- Dùng runner thật `eval/graph_rag_question_bank.py` với `--legal-only`; đọc CLI trước khi dùng. Runner hiện bắt buộc global provider qwen để bảo vệ housing. Thêm cấu hình legal selector riêng hoặc sửa guard theo khả năng/routing một cách có kiểm thử; không xóa chốt bảo vệ housing để chạy được Gemini.
- Lắp đúng các lớp Compose hiện có. Dùng tên container/cổng thử riêng; kiểm tra mounts trỏ tới worktree mới và DB/corpus đúng. Không tạo DB rỗng rồi tưởng đã test trên corpus thật.
- Nếu có tiến trình Qwen judge cũ đang chạy, tránh chạy benchmark latency cạnh tranh tài nguyên mà không ghi nhận. Không tự kill lượt đang chạy; dùng thời điểm/môi trường phù hợp hoặc ghi rõ nhiễu đo.

### D. Chấm công bằng và báo cáo

- Giữ nguyên `compare_grounded_references.py` policy V15 và `quantity_audit.py` khi so selector.
- Chấm hai lượt bằng cùng Qwen judge local, cùng rubric, reference, cấu hình và hash. Dùng output mới cho mỗi input. Chỉ tái sử dụng review cũ nếu các identity cần thiết thật sự trùng khớp.
- Lệnh trong container có dạng:
  `python /eval/compare_grounded_references.py --run /eval/reports/<run>.json --output /eval/reports/<review>.json`.
- Wrapper `run_legal_repair_comparison.py` hardcode tên file và pipeline cũ. Tạo wrapper mới/tham số hóa phù hợp; không sửa hash kỳ vọng chỉ để vượt kiểm tra của lượt cũ.
- Thêm báo cáo mới dùng cùng logic đối chiếu, không ghi nhầm mọi baseline thành commit c8dba04. Phải ghi đúng provenance của từng nhánh A/B.
- Nếu judge lỗi/quota, lưu trạng thái unscored và lý do; không thay thành 0 hoặc trộn nhãn từ bộ chấm khác. RAGAS chỉ báo điểm khi thực sự chạy đủ metric; không đổi tên high/partial/low thành RAGAS/accuracy.
- Bảng cuối phải có: số câu hoàn tất/lỗi; high/partial/low/unscored; chuyển nhãn theo từng ID; ý thiếu/khác; nguồn và giới hạn; số câu đủ/một phần; số lần sửa/fallback; latency từng bước và toàn tuyến p50/p95; token/chi phí nếu có số liệu thật; xác nhận không gửi housing lên cloud.
- Lưu cả nhãn Qwen đề xuất và nhãn cuối theo audited_agreement. High của V15 là mọi ý được matched; không tự nới rubric cho bản mới.
- `no_answer=true` có thể đi cùng câu trả lời một phần. Tách rõ không có nội dung, trả lời một phần và đầy đủ. Không lấy cờ nguồn đầy đủ hoặc citation format=1.0 làm tỷ lệ đúng pháp luật.
- Bộ tham chiếu chưa được kiểm chứng toàn bộ; câu 49 có khác biệt câu hỏi giữa bank/reference. Công khai các giới hạn này, không sửa câu hỏi âm thầm.

### E. Build và HTTP

Build API với code mới, chạy môi trường thử và kiểm tra HTTP có xác thực. Xác minh dữ liệu nguồn/model/trace thực tế, câu hỏi pháp lý, hỏi tiếp và tìm phòng không bị hồi quy. Kiểm thử tài khoản tạm phải xóa đúng tài khoản do lượt test tạo ra.

Nếu ảnh hưởng cấu hình/giao diện, build web bằng script dự án và kiểm tra hiển thị nguồn, partial và lỗi proxy. Xác nhận code đang chạy trong container đúng commit/cấu hình mới; chỉ sửa file host không chứng minh API đã cập nhật.

Hoàn tất code, benchmark và smoke trên môi trường thử trước khi chuyển mặc định. Nếu kết quả đủ 36 câu chứng minh bản mới chạy đúng, không có hồi quy nghiêm trọng về nguồn/điều kiện và phù hợp mục tiêu tốc độ, cập nhật API local sang cấu hình mới, giữ cấu hình/image trước đó để rollback rồi chạy lại smoke HTTP. Không triển khai sang máy chủ hoặc dịch vụ ngoài môi trường dự án này. Nếu chưa đủ bằng chứng hoặc chất lượng giảm, giữ API chính ở bản hiện có và bàn giao bản thử cùng nguyên nhân; không ép chuyển chỉ để báo hoàn thành. Báo chính xác trạng thái đã triển khai và lệnh rollback. Không cần hỏi lại để làm những bước sửa, thử nghiệm, build, commit/push đã giao ở trên.

## 7. Tiêu chí hoàn thành và bàn giao Git

Hoàn thành khi:

1. Checkpoint ban đầu đã push, có SHA xác minh từ remote.
2. Gemini proxy thực sự chọn bằng chứng bằng ID, các chốt nguồn hoạt động và luồng pháp lý mới chạy được khi Ollama không khả dụng.
3. Test liên quan, pilot, lượt đầy đủ 36 câu, A/B và chấm cùng phương pháp đã có kết quả thật; mọi phần chưa hoàn tất có lý do rõ ràng.
4. Có bằng chứng nguyên văn cho các lỗi còn lại, báo cáo so sánh cùng giới hạn phép đo; không khẳng định Gemini tốt hơn chỉ vì chạy thành công.
5. Dữ liệu gốc/tham chiếu/graph cũ còn nguyên; artifact mới tách riêng và ở local khi chứa dữ liệu nội bộ.
6. Code/test/tài liệu tái lập đã commit và push nhánh mới, không force-push/merge main. Trước push cuối, rà staged diff và bí mật một lần nữa.

Nếu bản Gemini nhanh hơn rõ rệt và chất lượng không giảm, đề xuất dùng làm mặc định. Nếu còn thiếu ý hoặc sai điều kiện quan trọng, trình bày đúng lỗi và giữ ở bản thử; không hạ kiểm tra để đạt số đẹp. Nêu rõ trade-off, không đặt một ngưỡng cải thiện tùy ý rồi coi là yêu cầu người dùng.

Báo cáo cuối bằng tiếng Việt, ngắn gọn nhưng đủ: SHA/link checkpoint; nhánh và SHA/link kết quả; thay đổi kiến trúc; cấu hình bật/tắt; tests đã chạy; bảng Qwen/Gemini; đường dẫn artifact local; giới hạn còn lại; trạng thái API chính và môi trường thử; lệnh triển khai/rollback. Với tác vụ dài, cập nhật tiến độ theo mốc. Nếu bị chặn, nói đúng bước và nguyên nhân, không báo thành công một phần như đã hoàn thành toàn bộ.
