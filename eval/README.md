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

Các ngưỡng trong dự án là tiêu chí nghiệm thu được nhóm đăng ký trước, không phải “chuẩn phổ quát” do RAGAS hay các bài báo bảo đảm. Báo cáo phải có cả giá trị, cỡ mẫu, dataset/model/prompt version, CI hoặc độ biến thiên giữa các lần chạy, và các failure case.

## 6. Nguồn nghiên cứu chính

1. Es et al. (2024), *RAGAS: Automated Evaluation of Retrieval Augmented Generation*, EACL Demo, DOI [10.18653/v1/2024.eacl-demo.16](https://aclanthology.org/2024.eacl-demo.16/).
2. Saad-Falcon et al. (2024), *ARES: An Automated Evaluation Framework for Retrieval-Augmented Generation Systems*, NAACL, DOI [10.18653/v1/2024.naacl-long.20](https://aclanthology.org/2024.naacl-long.20/).
3. Lewis et al. (2020), *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*, [NeurIPS 2020](https://papers.neurips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html).
4. Järvelin & Kekäläinen (2002), *Cumulated gain-based evaluation of IR techniques*, DOI [10.1145/582415.582418](https://doi.org/10.1145/582415.582418).
5. Hu, Koren & Volinsky (2008), *Collaborative Filtering for Implicit Feedback Datasets*, DOI [10.1109/ICDM.2008.22](https://doi.org/10.1109/ICDM.2008.22).
6. Liu, Ting & Zhou (2008), *Isolation Forest*, [IEEE ICDM 2008](https://doi.org/10.1109/ICDM.2008.17).
7. NIST (2024), *AI RMF: Generative AI Profile*, DOI [10.6028/NIST.AI.600-1](https://doi.org/10.6028/NIST.AI.600-1).
