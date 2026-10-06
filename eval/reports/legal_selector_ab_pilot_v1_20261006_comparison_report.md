# Báo cáo Phép thử Đối chứng: Qwen Selector vs Gemini Selector (legal_selector_ab_pilot_v1_20261006)

**Mục tiêu:** Xác định việc thay Qwen bằng Gemini ở **RIÊNG** bước chọn nguồn có cải thiện hệ thống hay không.

## 1. Bằng chứng Phép thử Hợp lệ
- **Git Commit:** `unknown`
- **Snapshot SHA256:** `7ffe56f0c98e9e8c4978056a8a98e0817e464cf553d5fbf757139af7c66b1619`
- **Corpus Schema:** `legal_word_repair_v16_20261006` (Graph: `graph_rag_word_repair_v16`, Housing: `housing_graph_word_repair_v16`)
- **Biến duy nhất thay đổi:** Model/provider chọn nguồn (`Ollama Qwen` vs `Gemini Proxy`).
- **Điều kiện cố định tuyệt đối:** Cùng snapshot 36 câu (QuestionPlan + candidate chunks nguyên vẹn); cùng Gemini Writer (riêng); cùng Gemini Verifier (riêng); cùng giới hạn sửa tối đa 1 lần; cùng judge V15 cục bộ Qwen.
- **Không dùng combined mode; không sửa prompt viết, prompt kiểm chứng hay rubric chấm.**

## 2. Bảng So sánh Tổng hợp

| Chỉ số | Nhánh A (Qwen chọn nguồn) | Nhánh B (Gemini chọn nguồn) | Chênh lệch (B - A) |
|---|---:|---:|---:|
| Số câu hoàn thành / lỗi | 4 / 0 | 4 / 0 | 0 |
| Thời gian chọn nguồn (Trung vị) | 49.33s | 6.09s | -43.24s |
| Thời gian chọn nguồn (P95) | 64.78s | 7.3s | -57.48s |
| Chọn nguồn đến câu trả lời cuối (Trung vị) | 78.55s | 20.55s | -58.0s |
| Chọn nguồn đến câu trả lời cuối (P95) | 82.45s | 32.99s | -49.46s |
| Tổng request Gemini | 12 | 16 | 4 |
| Số câu phải sửa nội dung (1 lần) | 2 | 1 | -1 |
| Số câu fallback nguồn | 0 | 0 | 0 |
| Số câu trả lời một phần (partial) | 3 | 3 | 0 |
| V15 High / Partial / Low | 0 / 3 / 1 | 0 / 3 / 1 | High: 0, Low: 0 |

> **Lưu ý về thời gian phân tích/truy xuất cố định:**
> - Thời gian phân tích câu hỏi (Gemini Question Analyzer): trung vị 4.53s, P95 6.95s.
> - Thời gian truy xuất E5 + BM25 + Graph: trung vị 0.11s, P95 0.14s.
> - Các thời gian này đã được cố định và lưu trong snapshot dùng chung cho cả hai nhánh.

## 3. Biến động Nhãn V15
- **Giữ nguyên nhãn:** 2 câu
- **Tăng nhãn:** 1 câu (['Q28 (low->partial)'])
- **Giảm nhãn:** 1 câu (['Q24 (partial->low)'])

## 4. Chi tiết Từng Câu: So Sánh Nguồn Được Chọn và V15

| ID | Qwen chọn | Gemini chọn | Điểm chung | Khác biệt | Tác động V15 (A -> B) | Trạng thái B |
|---:|---|---|---|---|:---:|---|
| 24 | [1, 2] | [1, 2] | [1, 2] | Trùng 100% | partial -> low | OK |
| 28 | [2, 3, 4, 5] | [2, 3, 4, 5] | [2, 3, 4, 5] | Trùng 100% | low -> partial | Repaired |
| 36 | [1, 2, 3] | [1, 2, 3] | [1, 2, 3] | Trùng 100% | partial -> partial | OK |
| 45 | [1, 2, 4, 5] | [1, 2, 4, 5] | [1, 2, 4, 5] | Trùng 100% | partial -> partial | OK |

## 5. Bằng chứng Trích đoạn Cụ thể cho Các Câu Khác Biệt Nguồn