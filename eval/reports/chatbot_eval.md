# Chatbot evaluation report

Dataset: 200 cases; failures: 0.

| Metric | Value | Threshold | Status |
|---|---:|---:|---|
| recall_at_5 | 1.0 | 0.7 | PASS |
| precision_at_5 | 1.0 | 0.7 | PASS |
| no_answer_accuracy | 1.0 | 0.9 | PASS |
| citation_accuracy | N/A (chạy ragas_eval.py) | 1.0 | NOT RUN |
| filter_accuracy | 1.0 | 0.9 | PASS |
| intent_accuracy | 1.0 | None | PASS |
| query_understanding_accuracy | 1.0 | 0.9 | PASS |
| faithfulness_groundedness | N/A (chạy ragas_eval.py) | 0.7 | NOT RUN |
| p95_latency_ms | 1.174 | 5000 | PASS |
