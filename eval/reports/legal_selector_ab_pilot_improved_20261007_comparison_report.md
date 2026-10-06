# Báo cáo Phép thử Đối chứng: Qwen Selector vs Gemini Selector (legal_selector_ab_pilot_improved_20261007)

**Mục tiêu:** Xác định việc thay Qwen bằng Gemini ở **RIÊNG** bước chọn nguồn có cải thiện hệ thống hay không.

## 1. Bằng chứng Phép thử Hợp lệ & Khóa Identity
- **Git Commit:** `e84deade06e3f5f41f51a749f1891cbc486402a7`
- **Run Identity SHA256:** `c745afcf1a874d7fec3afe0a0fa925ef77e4a265d9f6f3445cb3334c3c5e33e8`
- **Code Digest SHA256:** `75ac395718276059377dc99bea340ed1e3cb1d172418f22244c6d35accef7015`
- **Snapshot SHA256:** `7ffe56f0c98e9e8c4978056a8a98e0817e464cf553d5fbf757139af7c66b1619`
- **Corpus Schema:** `legal_word_repair_v16_20261006` (Graph: `graph_rag_word_repair_v16`, Housing: `housing_graph_word_repair_v16`)
- **Biến độc lập duy nhất:** Model/provider chọn nguồn (`Ollama Qwen` vs `Gemini Proxy`).
- **Điều kiện cố định tuyệt đối:** Cùng snapshot 36 câu (QuestionPlan + candidate chunks nguyên vẹn); cùng Gemini Writer (riêng); cùng Gemini Verifier (riêng); cùng giới hạn sửa tối đa 1 lần; cùng judge V15 cục bộ Qwen.
- **Không dùng combined mode; không sửa prompt viết, prompt kiểm chứng hay rubric chấm.**

## 2. Bảng So sánh Tổng hợp

| Chỉ số | Nhánh A (Qwen chọn nguồn) | Nhánh B (Gemini chọn nguồn) | Chênh lệch (B - A) |
|---|---:|---:|---:|
| Số câu hoàn thành / lỗi | 4 / 0 | 4 / 0 | 0 |
| Thời gian chọn nguồn (Trung vị) | 47.5s | 8.29s | -39.21s |
| Thời gian chọn nguồn (P95) | 73.2s | 9.1s | -64.1s |
| Replay từ chọn nguồn đến trả lời (Trung vị) | 73.6s | 30.58s | -43.02s |
| Replay từ chọn nguồn đến trả lời (P95) | 86.56s | 32.54s | -54.02s |
| Tổng request Gemini cấp workflow | 14 | 21 | 7 |
| Số câu phải sửa nội dung (1 lần) | 3 | 3 | 0 |
| Số câu fallback nguồn | 0 | 0 | 0 |
| Số câu trả lời một phần (partial) | 3 | 3 | 0 |
| V15 High / Partial / Low / Unscored | 1 / 3 / 0 / 0 | 1 / 3 / 0 / 0 | High: 0, Low: 0 |

> **Lưu ý về định nghĩa thời gian và token:**
> - *Replay từ chọn nguồn đến trả lời:* Đo riêng từ lúc bắt đầu chọn nguồn đến khi hoàn thành sinh/kiểm chứng câu trả lời cuối. Không bao gồm phân tích câu hỏi và truy xuất vector/BM25 đã được lưu cố định trong snapshot.
> - *Thời gian phân tích/truy xuất cố định trong snapshot:* Phân tích câu hỏi trung vị 4.24s (P95 5.66s); Truy xuất E5+BM25 trung vị 0.14s (P95 0.21s).
> - *Token usage:* Nhánh A: `Proxy does not return token usage headers`; Nhánh B: `Proxy does not return token usage headers`.

## 3. Biến động Nhãn V15
- **Giữ nguyên nhãn:** 2 câu
- **Tăng nhãn:** 1 câu (['Q58 (partial->high)'])
- **Giảm nhãn:** 1 câu (['Q43 (high->partial)'])

## 4. Chi tiết Từng Câu: So Sánh Nguồn Được Chọn và V15

| ID | Qwen chọn | Gemini chọn | Điểm chung | Khác biệt | Tác động V15 (A -> B) | Trạng thái B |
|---:|---|---|---|---|:---:|---|
| 43 | [1, 2, 3, 4, 5] | [1, 2, 4, 5] | [1, 2, 4, 5] | Qwen-only: [3] | high -> partial | Repaired |
| 44 | [1, 2, 4, 5] | [1, 2, 4, 5] | [1, 2, 4, 5] | Trùng 100% | partial -> partial | Repaired |
| 45 | [1, 2, 4, 5] | [1, 2, 4, 5] | [1, 2, 4, 5] | Trùng 100% | partial -> partial | OK |
| 58 | [1, 2] | [1, 2] | [1, 2] | Trùng 100% | partial -> high | Repaired |

## 5. Bằng chứng Trích đoạn Cụ thể cho Các Câu Khác Biệt Nguồn
### Câu 43: Người giới thiệu phòng trọ và thu phí môi giới cần công khai những thông tin gì?
**Qwen chọn nhưng Gemini bỏ:**
- `Candidate ID 3` [Luật Kinh doanh bất động sản 29/2023/QH15 — bản Word cung cấp - Điều 61. Điều kiện của tổ chức, cá nhân kinh doanh dịch vụ môi giới bất động sản | Khoản 1]: "1. Tổ chức, cá nhân kinh doanh dịch vụ môi giới bất động sản phải thành lập doanh nghiệp kinh doanh dịch vụ bất động sản theo quy định tại khoản 5 Điều 9 của Luật này và phải đáp ứng các điều kiện sau đây:

a) Phải có quy chế hoạt động dịch..."
- **Nhãn V15:** Qwen `high` vs Gemini `partial`
