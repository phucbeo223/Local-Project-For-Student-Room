# Đánh giá thực nghiệm AI

Thư mục này tách rõ ba mức bằng chứng. Không được dùng kết quả mô phỏng trên dữ liệu giả để tuyên bố độ chính xác ngoài thực tế.

## 1. Ba mức đánh giá

| Mức | Runner | Đo gì | Có thể đưa vào kết luận khoa học? |
|---|---|---|---|
| Unit/regression | `pytest` | Logic parser, ranking, fallback, rule risk | Chỉ chứng minh phần mềm chạy đúng đặc tả |
| Mô phỏng tái lập | `chatbot_eval.py` | Intent, filter, Precision/Recall@5 trên corpus có seed cố định | Có, nhưng phải ghi rõ là **synthetic simulation** |
| End-to-end/nhãn độc lập | `ragas_eval.py`, `risk_eval.py`, `recommendation_eval.py` | RAGAS trên API thật; risk và recommendation trên nhãn người dùng/kiểm duyệt độc lập | Có, kèm giới hạn mẫu và quy trình gán nhãn |

`chatbot_eval.py` không tự gán Faithfulness hay Answer Relevancy. Hai trường cần LLM judge được ghi `N/A / NOT RUN` cho đến khi `ragas_eval.py` thực sự chạy.

## 2. Dữ liệu giả có kiểm soát

Chạy lại corpus và Q&A bằng seed cố định:

```powershell
& .\.venv\Scripts\python.exe scripts\generate_fake_listings.py --seed 2026
& .\.venv\Scripts\python.exe eval\chatbot_eval.py
```

Provenance nằm tại `eval/datasets/metadata.json`: version dataset, seed, số mẫu, generator và giao thức ground truth. Các ID liên quan được tính từ bộ lọc nghiệp vụ, không được viết tay theo kết quả của chatbot. Trước khi công bố, cần khóa một golden subset được hai người đánh giá độc lập và báo cáo mức đồng thuận.

## 3. RAGAS end-to-end

RAGAS được chọn vì bài báo gốc phân tách evaluation theo retrieval, faithfulness và chất lượng câu trả lời. Runner gọi API `/chat/ask` thật, lấy context thật, sau đó đo:

- `faithfulness`, `answer_relevancy`;
- `context_precision`, `context_recall`;
- citation format accuracy và p95 latency do hệ thống đo trực tiếp.

```powershell
& .\.venv\Scripts\python.exe -m pip install -r eval\requirements.txt
& .\.venv\Scripts\python.exe eval\ragas_eval.py --api-url http://localhost:8000 --limit 200
```

Có thể thêm `--admin-token <token>` để ghi run vào dashboard AI. Model judge, model sinh câu trả lời, prompt version, dataset version và thời điểm chạy phải được giữ trong artifact. Điểm LLM-as-a-judge có tính ngẫu nhiên; nên chạy lặp lại và đối chiếu một tập nhỏ do con người chấm. ARES cũng cho thấy đánh giá tự động đáng tin hơn khi hiệu chỉnh bằng một tập nhãn người thật nhỏ.

### Bộ câu hỏi CTU trên kho dữ liệu hiện hành

`question_bank_ragas.py` mặc định đọc `docs/LEGAL_QUESTION_BANK.md` qua Compose (36 câu pháp lý). Bộ 58 câu `docs/CHATBOT_QUESTION_BANK.md` giữ cho lịch sử; các câu giá phòng và khoảng cách chưa dùng lại khi dữ liệu mới chưa nạp. Runner gọi dịch vụ chatbot với DB thật, lưu từng câu trả lời, nguồn, toàn bộ đoạn truy xuất, trạng thái suy giảm, độ trễ và điểm trích dẫn; tắt ghi telemetry. `audit_legal_corpus.py` chỉ đọc DB để kiểm tra chỉ mục.

Theo yêu cầu ngày 03/10/2026, hệ thống hiện trả lời và kiểm tra nguồn bằng Qwen 3.5 9B local (`CHATBOT_LLM_PROVIDER=qwen`); RAGAS 0.3.9 cũng dùng Ollama Qwen (`RAGAS_JUDGE_PROVIDER=ollama`, `RAGAS_JUDGE_MODEL=qwen3.5:9b`). E5 là embedding cho Answer Relevancy; volume `nckh_chat-model-cache` giữ E5. Chấm một luồng, giữ đủ ngữ cảnh, lưu phát biểu/phán định và token từng chỉ số. Các lượt Gemini trước được giữ riêng, không so trực tiếp điểm giữa hai bộ chấm. Chạy tuần tự, dùng tên output mới cho mỗi phiên bản hệ thống:

```powershell
ollama pull qwen3.5:9b
docker compose --profile tools run --rm --no-deps legal-indexer --data-dir /data --no-apply-migration --batch-size 8
docker build -f eval/Dockerfile.ragas -t nckh-ragas-eval:local .
docker compose -f docker-compose.yml -f docker-compose.override.yml -f docker-compose.ragas.yml run --rm --no-deps ragas-eval --phase collect --output /eval/reports/legal_NEW_TIMESTAMP.json
docker compose -f docker-compose.yml -f docker-compose.override.yml -f docker-compose.ragas.yml run --rm --no-deps ragas-eval --phase score --output /eval/reports/legal_NEW_TIMESTAMP.json --judge-provider ollama --judge-model qwen3.5:9b --judge-max-output-tokens 8192 --score-workers 1 --score-abstentions
```

Runner ghi checkpoint sau mỗi câu và mỗi metric; chạy lại cùng output tiếp tục phần chưa xong. Chỉ một tiến trình được ghi một JSON. Khi chấm song song, mỗi worker có judge riêng; tiến trình chính lưu checkpoint. Bộ câu hỏi chưa có đáp án chuẩn độc lập: chỉ chấm Faithfulness, Answer Relevancy và Context Utilization; Context Recall/Answer Correctness để N/A. Điểm judge không thay thế kiểm tra tính đúng và hiệu lực của văn bản.

Để so sánh nâng cấp model, dùng `compare_model_upgrade.py --clone --before <JSON cũ> --after <JSON bản sao>` giữ nguyên câu trả lời/ngữ cảnh cũ; chấm bản sao và lượt mới bằng cùng judge, cùng tham số. Sau đó dùng `--before <bản sao> --after <lượt mới> --audit <audit> --output <báo cáo.md>` để đối chiếu các câu có điểm ở cả hai lượt. Không so trực tiếp điểm Qwen chấm cũ với điểm Gemini chấm mới.

### Kho riêng và agent — lần sửa 03–04/10/2026

Quy trình hiện tại xem tại `docs/LEGAL_AGENT_REBUILD.md`. Kho `legal_v2` được nạp riêng; các lệnh index `public` ở phần lịch sử phía trên không phải lệnh xây kho mới. Gemini phân tích truy vấn, Qwen local chọn đoạn nguồn, hệ thống kiểm tra và trích nguyên văn. Chấm so với baseline Gemini lịch sử phải dùng cùng Gemini/cấu hình, dù model trả lời là Qwen.

Ví dụ chạy từ thư mục gốc bằng PowerShell, sau khi có corpus và manifest đã xác thực:

```powershell
$legalCompose = @('-f', 'docker-compose.yml', '-f', 'docker-compose.override.yml', '-f', 'docker-compose.ragas.yml')
$legalOutput = '/eval/reports/legal_agents_' + (Get-Date -Format 'yyyyMMdd_HHmmss') + '.json'
docker compose @legalCompose run --rm --no-deps --entrypoint python -v "${PWD}/docs:/workspace/docs" -v "${PWD}/eval:/workspace/eval" ragas-eval /workspace/scripts/index_legal_agent_corpus.py
docker compose @legalCompose run --rm --no-deps --entrypoint python ragas-eval /eval/verify_legal_agent_corpus.py
docker compose @legalCompose run --rm --no-deps -e CHATBOT_LEGAL_SCHEMA=legal_v2 -e CHATBOT_AGENTS_ENABLED=true -e CHATBOT_QUESTION_ANALYSIS_MODEL=gemini-3.1-flash-lite -e CHATBOT_LEGAL_TIMEOUT_SECONDS=180 ragas-eval --phase collect --output $legalOutput
docker compose @legalCompose run --rm --no-deps ragas-eval --phase score --output $legalOutput --judge-provider gemini --judge-model gemini-3.1-flash-lite --judge-max-output-tokens 8192 --score-workers 4 --score-abstentions
```

Chỉ chạy bước sau khi bước trước thành công. Dùng output mới khi code hoặc manifest đổi; runner từ chối trộn các phiên bản. Khi tiếp tục phiên đang dở, dùng lại đường dẫn output đã ghi nhận, giữ code/corpus cố định và chỉ một tiến trình ghi file. Indexer không chuyển API chính và không xóa kho cũ. `finish_legal_agents.py` là runner hữu hạn cho lượt v10 cụ thể, không dùng như lịch nền.

HTTP thử bằng người dùng thường không được yêu cầu `include_evaluation_contexts`; runner chấm gọi nội bộ để lấy ngữ cảnh. `probe_legal_agent_http.py` tạo rồi xóa tài khoản test, JWT dùng cùng cấu hình API. Không in token hoặc khóa. Điểm lỗi giữ N/A, chấm lại có giới hạn chỉ phần thiếu; báo cáo ghi cả số phản hồi thiếu và số điểm hợp lệ.

Lượt v10 đã hoàn tất 36 phản hồi nhưng bộ chấm Gemini chạm HTTP 429. `retry_legal_agent_scores.py` đã chạy đúng một lượt thử lại, kiểm tra mọi điểm hợp lệ và payload trả lời/ngữ cảnh không đổi; không đổi khóa để vượt quota. Script từ chối chạy lại cùng lượt. Các trường lỗi ban đầu giữ trong `ragas_retry_history`, kết quả thiếu không được ghép điểm local vào bản so sánh Gemini. Báo cáo và gate cuối giữ quyết định chưa chuyển kho; không có tác vụ tự động chờ quota.

### Năm nhóm sửa và worker chờ quota — 04/10/2026

Lượt cuối v15 và sổ nguồn xem `docs/LEGAL_FIXES_20261004.md`. V11/v12 là lượt thử đã dừng để sửa OCR và schema nguồn web; không chạy lại các lượt đó. Corpus cuối giữ riêng `legal_v2`; không dùng lệnh index `public` lịch sử để thay thế. Báo cáo local và native Gemini tách file.

```powershell
$legalCompose = @('-f', 'docker-compose.yml', '-f', 'docker-compose.override.yml', '-f', 'docker-compose.ragas.yml')
docker compose @legalCompose run --rm --no-deps --entrypoint python -e CHATBOT_LEGAL_SCHEMA=legal_v2 -e CHATBOT_AGENTS_ENABLED=true -e CHATBOT_QUESTION_ANALYSIS_MODEL=gemini-3.1-flash-lite -e CHATBOT_LEGAL_TIMEOUT_SECONDS=180 ragas-eval /eval/resume_legal_evaluation.py --output /eval/reports/legal_NEW_TIMESTAMP.json --max-hours 48
```

Chọn output mới khi code/corpus đổi. Tiếp tục phiên đã có checkpoint thì dùng chính output đó và xác minh không có container/writer đang chạy; worker có khóa một writer. Lượt hiện có container `nckh-legal-agents-eval-v15` và output `legal_agent_after_v15_2026-10-04.json`, đang chờ quota; không khởi động thêm bản trùng.

Khi HTTP 429, runner thoát mã 75 sau atomic checkpoint; không ghi 0 hoặc phản hồi fallback như kết quả kiểm thử thành công. Worker dừng toàn bộ queue, tôn trọng Retry-After/RetryInfo, quota ngày tính mốc reset Pacific, probe nhỏ sau mốc chờ rồi tiếp tục những câu/metric chưa xong. Không xoay key cùng dự án để vượt quota. Worker hữu hạn 48 giờ; hết thời gian vẫn giữ checkpoint. Máy/Docker cần hoạt động. Heartbeat trong chat theo dõi và báo khi có kết quả hoặc lỗi; im lặng khi chạy/chờ bình thường.

Mỗi metric hợp lệ được giữ nguyên khi tiếp tục; điểm NaN/None/lỗi vẫn là phần chưa chấm, không điền điểm từ judge khác. Native Gemini vẫn dùng 8192 token/4 worker/E5/strictness 1/temperature 0/giữ đủ context/chấm abstention như baseline. So sánh bằng `report_legal_fixes.py` trên các cặp có cùng phương pháp. Không sửa báo cáo lịch sử v10 hoặc baseline.

```powershell
& 'C:\Program Files\Python314\python.exe' -X utf8 eval/report_legal_fixes.py
```

Nếu quota đã được xác nhận ở một phiên trống vừa dừng, `inherit_quota_checkpoint.py` chỉ tạo phiên mới có **0 phản hồi/0 điểm**, gắn SHA checkpoint trước và cùng mốc chờ, tránh gọi thêm Gemini trước reset. Script từ chối phiên trước có câu trả lời. Không dùng để sao chép điểm giữa phiên.

## 4. Risk và recommendation

Risk chỉ được công bố recall/precision khi có JSONL nhãn độc lập:

```json
{"id":"R001","label_source":"manual","is_risky":true,"district_median_price":2100000,"listing":{"title":"...","description":"...","price":900000}}
```

```powershell
& .\.venv\Scripts\python.exe eval\risk_eval.py --dataset path\to\risk_labels.jsonl
```

Recommendation cần relevance judgment theo từng người dùng; `relevance` là gain 0–3 và `recommended_ids` là output đã khóa của hệ thống:

```json
{"user_id":"U001","label_source":"student_survey","recommended_ids":[12,9,31],"relevance":{"12":3,"9":1,"31":0}}
```

```powershell
& .\.venv\Scripts\python.exe eval\recommendation_eval.py --dataset path\to\recommendation_labels.jsonl --k 10
```

Runner chủ động từ chối `label_source=synthetic`. Với risk, dữ liệu giả sinh từ chính các rule sẽ gây đánh giá vòng tròn. Với recommendation, lượt tương tác dùng để tạo hồ sơ phải tách theo thời gian khỏi lượt tương tác dùng làm test.

## 5. Ngưỡng và báo cáo

### Lịch sử sửa lỗi ngày 2026-10-01 — pháp lý, điện và nước

Đợt sau sửa lỗi dùng `docs/LEGAL_QUESTION_BANK.md` (36 câu). Không dùng các câu lọc phòng/giá thuê/khoảng cách của dữ liệu phòng cũ. File 58 câu và JSON cũ được giữ để đối chiếu lịch sử. Các câu về điện/nước vẫn kiểm tra căn cứ, đối tượng và điều kiện áp dụng; không coi biểu giá năm 2024 là giá mới nhất.

```powershell
docker compose -f docker-compose.yml -f docker-compose.override.yml -f docker-compose.ragas.yml run --rm --no-deps --entrypoint python ragas-eval /workspace/scripts/index_legal_documents.py --data-dir /data --sync-missing /eval/reports/source_sync_NEW_TIMESTAMP.json
docker compose -f docker-compose.yml -f docker-compose.override.yml -f docker-compose.ragas.yml run --rm --no-deps ragas-eval --phase collect --output /eval/reports/legal_NEW_TIMESTAMP.json
docker compose -f docker-compose.yml -f docker-compose.override.yml -f docker-compose.ragas.yml run --rm --no-deps ragas-eval --phase score --output /eval/reports/legal_NEW_TIMESTAMP.json --judge-provider gemini --judge-model gemini-3.1-flash-lite --judge-max-output-tokens 8192 --score-abstentions
```

Chạy tuần tự nạp → collect → score, không cho hai tiến trình ghi cùng JSON. Đồng bộ chỉ mục giữ nguyên đoạn/vectors cũ, lưu metadata trước đổi trạng thái; đường dẫn vắng trong Data bị loại khỏi truy xuất `ready`, không bị tuyên bố là văn bản hết hiệu lực. Không dùng `--sync-missing` với một nhóm nguồn riêng hoặc thư mục rỗng.

Bản tách đoạn `legal-v6` giữ tham chiếu “và Phụ lục” trong điều khoản hiệu lực, nhận tiêu đề bản trích dạng “Điều 27 — …” và Markdown. Câu trả lời sinh tự do có thêm bước đối chiếu kết luận với đúng nguồn; nếu không xác nhận được, hệ thống chỉ trích đoạn phù hợp và đánh dấu trả lời một phần, hoặc từ chối khi không có đoạn phù hợp. Đây là kiểm tra bằng mô hình và quy tắc, không phải chứng nhận đúng pháp lý.

Lần chấm mới dùng toàn bộ ngữ cảnh đã cung cấp cho câu trả lời, thay cho giới hạn 2 đoạn × 1.200 ký tự ở lượt cũ. Ragas dùng Qwen 3.5 4B cho cả ba chỉ số. Vì phương pháp và mô hình chấm đã đổi, điểm Ragas cũ không dùng để kết luận mức cải thiện trực tiếp. Context Recall/Answer Correctness vẫn N/A khi chưa có đáp án chuẩn độc lập.

Lượt pháp lý mới bật `--score-abstentions`: chấm cả phản hồi chưa đủ căn cứ tổng hợp khi có nguồn. Không gán giả điểm 0; nếu metric không có phát biểu để chấm hoặc judge lỗi, ghi N/A/lỗi cụ thể. Tỷ lệ từ chối và `partial_answer` báo riêng. Phản hồi một phần trích nguyên đoạn nguồn, giữ điều kiện/ngoại lệ và không tự suy ra cách áp dụng cho tình huống riêng. Lượt cuối lưu ở `legal_question_bank_release_2026-10-01.json`; các tên `after_fixes`, `final`, `verified` lưu quá trình tìm/sửa lỗi, không phải nghiệm thu cuối.

Nếu JSON chấm bị cắt, chỉ chạy lại metric/câu bị lỗi với `--metrics faithfulness --ids 8 23 33 --judge-max-output-tokens 4096`; không bật `--reset-selected-metrics` khi muốn giữ điểm hợp lệ. Giới hạn đầu ra ban đầu là 2.048 token. Mỗi metric lưu giới hạn đầu ra trong `ragas_usage`; lịch sử lỗi chấm lại giữ trong `ragas_retry_history`. Thay giới hạn đầu ra không thay mô hình, câu hỏi hoặc ngữ cảnh.

Các ngưỡng trong dự án là tiêu chí nghiệm thu được nhóm đăng ký trước, không phải “chuẩn phổ quát” do RAGAS hay các bài báo bảo đảm. Báo cáo phải có cả giá trị, cỡ mẫu, dataset/model/prompt version, CI hoặc độ biến thiên giữa các lần chạy, và các failure case.

## 6. Nguồn nghiên cứu chính

1. Es et al. (2024), *RAGAS: Automated Evaluation of Retrieval Augmented Generation*, EACL Demo, DOI [10.18653/v1/2024.eacl-demo.16](https://aclanthology.org/2024.eacl-demo.16/).
2. Saad-Falcon et al. (2024), *ARES: An Automated Evaluation Framework for Retrieval-Augmented Generation Systems*, NAACL, DOI [10.18653/v1/2024.naacl-long.20](https://aclanthology.org/2024.naacl-long.20/).
3. Lewis et al. (2020), *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*, [NeurIPS 2020](https://papers.neurips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html).
4. Järvelin & Kekäläinen (2002), *Cumulated gain-based evaluation of IR techniques*, DOI [10.1145/582415.582418](https://doi.org/10.1145/582415.582418).
5. Hu, Koren & Volinsky (2008), *Collaborative Filtering for Implicit Feedback Datasets*, DOI [10.1109/ICDM.2008.22](https://doi.org/10.1109/ICDM.2008.22).
6. Liu, Ting & Zhou (2008), *Isolation Forest*, [IEEE ICDM 2008](https://doi.org/10.1109/ICDM.2008.17).
7. NIST (2024), *AI RMF: Generative AI Profile*, DOI [10.6028/NIST.AI.600-1](https://doi.org/10.6028/NIST.AI.600-1).
