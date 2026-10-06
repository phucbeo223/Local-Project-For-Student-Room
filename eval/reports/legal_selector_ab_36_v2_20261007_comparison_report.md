# Báo cáo Phép thử Đối chứng: Qwen Selector vs Gemini Selector (legal_selector_ab_36_v2_20261007)

**Mục tiêu:** Xác định việc thay Qwen bằng Gemini ở **RIÊNG** bước chọn nguồn có cải thiện hệ thống hay không.

## 1. Bằng chứng Phép thử Hợp lệ & Khóa Identity
- **Git Commit:** `e84deade06e3f5f41f51a749f1891cbc486402a7`
- **Run Identity SHA256:** `057d2ddfa6fe2cb652b3f5e065d8e50a36458c049debd98f33da7b1361272d54`
- **Code Digest SHA256:** `75ac395718276059377dc99bea340ed1e3cb1d172418f22244c6d35accef7015`
- **Snapshot SHA256:** `7ffe56f0c98e9e8c4978056a8a98e0817e464cf553d5fbf757139af7c66b1619`
- **Corpus Schema:** `legal_word_repair_v16_20261006` (Graph: `graph_rag_word_repair_v16`, Housing: `housing_graph_word_repair_v16`)
- **Biến độc lập duy nhất:** Model/provider chọn nguồn (`Ollama Qwen` vs `Gemini Proxy`).
- **Điều kiện cố định tuyệt đối:** Cùng snapshot 36 câu (QuestionPlan + candidate chunks nguyên vẹn); cùng Gemini Writer (riêng); cùng Gemini Verifier (riêng); cùng giới hạn sửa tối đa 1 lần; cùng judge V15 cục bộ Qwen.
- **Không dùng combined mode; không sửa prompt viết, prompt kiểm chứng hay rubric chấm.**

## 2. Bảng So sánh Tổng hợp

| Chỉ số | Nhánh A (Qwen chọn nguồn) | Nhánh B (Gemini chọn nguồn) | Chênh lệch (B - A) |
|---|---:|---:|---:|
| Số câu hoàn thành / lỗi | 36 / 0 | 36 / 0 | 0 |
| Thời gian chọn nguồn (Trung vị) | 49.47s | 2.81s | -46.66s |
| Thời gian chọn nguồn (P95) | 80.98s | 7.92s | -73.06s |
| Replay từ chọn nguồn đến trả lời (Trung vị) | 67.05s | 24.68s | -42.37s |
| Replay từ chọn nguồn đến trả lời (P95) | 110.31s | 34.01s | -76.3s |
| Tổng request Gemini cấp workflow | 112 | 155 | 43 |
| Số câu phải sửa nội dung (1 lần) | 20 | 19 | -1 |
| Số câu fallback nguồn | 2 | 3 | 1 |
| Số câu trả lời một phần (partial) | 23 | 24 | 1 |
| V15 High / Partial / Low / Unscored | 7 / 25 / 4 / 0 | 7 / 24 / 5 / 0 | High: 0, Low: 1 |

> **Lưu ý về định nghĩa thời gian và token:**
> - *Replay từ chọn nguồn đến trả lời:* Đo riêng từ lúc bắt đầu chọn nguồn đến khi hoàn thành sinh/kiểm chứng câu trả lời cuối. Không bao gồm phân tích câu hỏi và truy xuất vector/BM25 đã được lưu cố định trong snapshot.
> - *Thời gian phân tích/truy xuất cố định trong snapshot:* Phân tích câu hỏi trung vị 3.97s (P95 6.06s); Truy xuất E5+BM25 trung vị 0.14s (P95 0.27s).
> - *Token usage:* Nhánh A: `Proxy does not return token usage headers`; Nhánh B: `Proxy does not return token usage headers`.

## 3. Biến động Nhãn V15
- **Giữ nguyên nhãn:** 29 câu
- **Tăng nhãn:** 3 câu (['Q28 (low->partial)', 'Q29 (low->partial)', 'Q48 (partial->high)'])
- **Giảm nhãn:** 4 câu (['Q19 (partial->low)', 'Q30 (high->partial)', 'Q45 (partial->low)', 'Q54 (partial->low)'])

## 4. Chi tiết Từng Câu: So Sánh Nguồn Được Chọn và V15

| ID | Qwen chọn | Gemini chọn | Điểm chung | Khác biệt | Tác động V15 (A -> B) | Trạng thái B |
|---:|---|---|---|---|:---:|---|
| 19 | [1, 2, 3, 4] | [1, 2, 3, 4] | [1, 2, 3, 4] | Trùng 100% | partial -> low | Fallback |
| 20 | [1, 2, 3, 4] | [1, 2, 3, 4] | [1, 2, 3, 4] | Trùng 100% | high -> high | OK |
| 21 | [1] | [1, 3] | [1] | Gemini-only: [3] | high -> high | OK |
| 22 | [1, 4] | [1, 4] | [1, 4] | Trùng 100% | partial -> partial | Repaired |
| 23 | [1, 2] | [1, 2] | [1, 2] | Trùng 100% | partial -> partial | Repaired |
| 24 | [1, 2] | [1, 2] | [1, 2] | Trùng 100% | low -> low | OK |
| 25 | [1, 2] | [1, 2] | [1, 2] | Trùng 100% | partial -> partial | OK |
| 26 | [1, 2, 4, 5] | [1, 2, 4, 5] | [1, 2, 4, 5] | Trùng 100% | partial -> partial | Repaired |
| 27 | [1, 2] | [1, 2] | [1, 2] | Trùng 100% | partial -> partial | Repaired |
| 28 | [2, 3, 4, 5] | [2, 3, 4, 5] | [2, 3, 4, 5] | Trùng 100% | low -> partial | Repaired |
| 29 | [1, 2, 3, 4, 5] | [1, 2, 3, 5] | [1, 2, 3, 5] | Qwen-only: [4] | low -> partial | Repaired |
| 30 | [2] | [2] | [2] | Trùng 100% | high -> partial | OK |
| 31 | [1, 2] | [1] | [1] | Qwen-only: [2] | partial -> partial | Repaired |
| 32 | [1, 2, 3, 4, 5] | [1, 2, 3, 4, 5] | [1, 2, 3, 4, 5] | Trùng 100% | partial -> partial | OK |
| 33 | [1, 2, 3] | [1] | [1] | Qwen-only: [2, 3] | partial -> partial | OK |
| 34 | [1, 2, 3, 4, 5] | [1, 2, 3, 5] | [1, 2, 3, 5] | Qwen-only: [4] | partial -> partial | Repaired |
| 35 | [1, 2, 3] | [1, 2, 3] | [1, 2, 3] | Trùng 100% | partial -> partial | Repaired |
| 36 | [1, 2] | [1, 2, 3] | [1, 2] | Gemini-only: [3] | partial -> partial | Repaired |
| 37 | [1, 2, 3, 4] | [1, 2, 3] | [1, 2, 3] | Qwen-only: [4] | high -> high | OK |
| 38 | [1, 2, 3] | [1, 2, 3] | [1, 2, 3] | Trùng 100% | high -> high | Repaired |
| 43 | [1, 2, 3, 4, 5] | [1, 2, 4, 5] | [1, 2, 4, 5] | Qwen-only: [3] | high -> high | OK |
| 44 | [1, 2, 4, 5] | [1, 2, 4, 5] | [1, 2, 4, 5] | Trùng 100% | partial -> partial | Repaired |
| 45 | [1, 2, 4, 5] | [1, 2, 4, 5] | [1, 2, 4, 5] | Trùng 100% | partial -> low | Repaired |
| 46 | [1, 2, 3, 5] | [1, 2, 3, 5] | [1, 2, 3, 5] | Trùng 100% | partial -> partial | OK |
| 47 | [1, 2, 3, 4] | [2, 4] | [2, 4] | Qwen-only: [1, 3] | partial -> partial | OK |
| 48 | [2, 4] | [1, 2, 3, 5] | [2] | Qwen-only: [4]; Gemini-only: [1, 3, 5] | partial -> high | OK |
| 49 | [1, 2, 3, 4] | [1, 2, 3, 4] | [1, 2, 3, 4] | Trùng 100% | low -> low | Fallback |
| 50 | [1, 2, 3] | [] | [] | Qwen-only: [1, 2, 3] | partial -> partial | Fallback |
| 51 | [1, 2, 3] | [1, 2, 3] | [1, 2, 3] | Trùng 100% | partial -> partial | Repaired |
| 52 | [1, 2, 3, 4] | [1, 2, 4] | [1, 2, 4] | Qwen-only: [3] | partial -> partial | Repaired |
| 53 | [1, 2, 3] | [1] | [1] | Qwen-only: [2, 3] | partial -> partial | OK |
| 54 | [1, 2, 3] | [1, 2, 3] | [1, 2, 3] | Trùng 100% | partial -> low | Repaired |
| 55 | [1, 2] | [2] | [2] | Qwen-only: [1] | high -> high | OK |
| 56 | [1, 2] | [1, 2] | [1, 2] | Trùng 100% | partial -> partial | Repaired |
| 57 | [1, 2, 3] | [1, 2, 3] | [1, 2, 3] | Trùng 100% | partial -> partial | OK |
| 58 | [1, 2] | [1, 2] | [1, 2] | Trùng 100% | partial -> partial | Repaired |

## 5. Bằng chứng Trích đoạn Cụ thể cho Các Câu Khác Biệt Nguồn
### Câu 21: Nếu chủ trọ muốn tăng giá thuê giữa thời hạn hợp đồng thì cần xem xét những gì?
**Gemini chọn nhưng Qwen bỏ:**
- `Candidate ID 3` [Luật Nhà ở — 79/VBHN-VPQH — bản Word cung cấp - Điều 170. Thời hạn thuê, giá thuê, cho thuê lại nhà ở | Khoản 1]: "1. Bên cho thuê và bên thuê nhà ở được thỏa thuận về thời hạn thuê, giá thuê và hình thức trả tiền thuê nhà ở theo định kỳ hoặc trả một lần; trường hợp Nhà nước có quy định về giá thuê nhà ở thì các bên phải thực hiện theo quy định đó...."
- **Nhãn V15:** Qwen `high` vs Gemini `high`

### Câu 29: Nếu nhà trọ dùng chung đồng hồ nước, cách phân chia chi phí nên được thỏa thuận ra sao?
**Qwen chọn nhưng Gemini bỏ:**
- `Candidate ID 4` [Giá nước Cần Thơ 215/QĐ-UBND — bản Word cung cấp - Điều 1. Quy định giá nước sạch sinh hoạt tại đô thị và khu vực nông thôn áp dụng đối với các đơn vị kinh doanh nước sạch, các tổ chức và khách hàng sử dụng nước sạch trên địa bàn thành phố Cần Thơ như sau: | Khoản 2]: "2. Giá nước sạch sinh hoạt tại đô thị, khu vực nông thôn do Trung tâm Nước sạch và Vệ sinh môi trường nông thôn cung cấp cho mục đích sinh hoạt:

STT

Nhóm khách hàng sử dụng nước sạch cho mục đích sinh hoạt

Giá tiêu thụ nước sạch (đồng/m3..."
- **Nhãn V15:** Qwen `low` vs Gemini `partial`

### Câu 31: Sinh viên thuê trọ tại Cần Thơ cần làm thủ tục cư trú nào?
**Qwen chọn nhưng Gemini bỏ:**
- `Candidate ID 2` [Luật Cư trú 68/2020/QH14 — Word Công báo - Điều 27. Điều kiện đăng ký tạm trú | Khoản 2]: "2. Thời hạn tạm trú tối đa là 02 năm và có thể tiếp tục gia hạn nhiều
lần...."
- **Nhãn V15:** Qwen `partial` vs Gemini `partial`

### Câu 33: Tôi cần chuẩn bị những giấy tờ gì để đăng ký tạm trú tại phòng trọ?
**Qwen chọn nhưng Gemini bỏ:**
- `Candidate ID 2` [Luật Cư trú 68/2020/QH14 — Word Công báo - Điều 28. Hồ sơ, thủ tục đăng ký tạm trú, gia hạn tạm trú | Khoản 3]: "3. Trong thời hạn 15 ngày trước ngày kết thúc thời hạn tạm trú đã đăng
ký, công dân phải làm thủ tục gia hạn tạm trú.
 Hồ sơ, thủ tục gia hạn tạm trú thực hiện theo quy định tại khoản 1 và
khoản 2 Điều này. Sau khi thẩm định hồ sơ, cơ quan ..."
- `Candidate ID 3` [Luật Cư trú 68/2020/QH14 — Word Công báo - Điều 28. Hồ sơ, thủ tục đăng ký tạm trú, gia hạn tạm trú | Khoản 2]: "2. Người đăng ký tạm trú nộp hồ sơ đăng ký tạm trú đến cơ quan đăng ký
cư trú nơi mình dự kiến tạm trú.
 Khi tiếp nhận hồ sơ đăng ký tạm trú, cơ quan đăng ký cư trú kiểm tra và
cấp phiếu tiếp nhận hồ sơ cho người đăng ký; trường hợp hồ sơ c..."
- **Nhãn V15:** Qwen `partial` vs Gemini `partial`

### Câu 34: Nếu chuyển sang phòng trọ khác, tôi cần cập nhật thông tin cư trú thế nào?
**Qwen chọn nhưng Gemini bỏ:**
- `Candidate ID 4` [Luật Cư trú 68/2020/QH14 — Word Công báo - Điều 29. Xóa đăng ký tạm trú | Khoản 2]: "2. Cơ quan đã đăng ký tạm trú có thẩm quyền xóa đăng ký tạm trú và phải
ghi rõ lý do, thời điểm xóa đăng ký tạm trú trong Cơ sở dữ liệu về cư trú...."
- **Nhãn V15:** Qwen `partial` vs Gemini `partial`

### Câu 36: Nhà trọ có nhiều phòng cần đáp ứng những yêu cầu an toàn cháy nổ nào?
**Gemini chọn nhưng Qwen bỏ:**
- `Candidate ID 3` [Luật PCCC 55/2024/QH15 — Word Công báo - Điều 23. Phòng cháy đối với cơ sở]: "1. Cơ sở phải bảo đảm các điều kiện an toàn về phòng cháy sau đây:
 a) Có nội quy phòng cháy, chữa cháy, cứu nạn, cứu hộ phù hợp với từng
loại hình cơ sở;
 b) Trang bị phương tiện, hệ thống phòng cháy, chữa cháy, cứu nạn, cứu hộ
theo quy đị..."
- **Nhãn V15:** Qwen `partial` vs Gemini `partial`

### Câu 37: Nếu lối thoát nạn bị khóa hoặc bị chặn, người thuê nên làm gì?
**Qwen chọn nhưng Gemini bỏ:**
- `Candidate ID 4` [Luật PCCC 55/2024/QH15 — Word Công báo - Điều 20. Phòng cháy đối với nhà ở]: "1. Nhà ở không thuộc loại hình quy định tại khoản 3 và khoản 4 Điều này
phải bảo đảm các điều kiện an toàn về phòng cháy sau đây:
 a) Lắp đặt, sử dụng thiết bị điện bảo đảm điều kiện an toàn về phòng
cháy quy định tại điểm c khoản 1 Điều 24..."
- **Nhãn V15:** Qwen `high` vs Gemini `high`

### Câu 43: Người giới thiệu phòng trọ và thu phí môi giới cần công khai những thông tin gì?
**Qwen chọn nhưng Gemini bỏ:**
- `Candidate ID 3` [Luật Kinh doanh bất động sản 29/2023/QH15 — bản Word cung cấp - Điều 61. Điều kiện của tổ chức, cá nhân kinh doanh dịch vụ môi giới bất động sản | Khoản 1]: "1. Tổ chức, cá nhân kinh doanh dịch vụ môi giới bất động sản phải thành lập doanh nghiệp kinh doanh dịch vụ bất động sản theo quy định tại khoản 5 Điều 9 của Luật này và phải đáp ứng các điều kiện sau đây:

a) Phải có quy chế hoạt động dịch..."
- **Nhãn V15:** Qwen `high` vs Gemini `high`

### Câu 47: Khi tìm phòng qua một nền tảng trực tuyến, tôi nên kiểm tra người đăng và nguồn tin như thế nào?
**Qwen chọn nhưng Gemini bỏ:**
- `Candidate ID 1` [Nhà Tốt bảo vệ người dùng như thế nào — Trợ Giúp Chợ Tốt Nhà Tốt - Nhà Tốt bảo vệ người dùng như thế nào | Đoạn nguyên văn 75]: "Trong thời gian gần đây, Nền tảng Công nghệ Bất động sản Nhà Tốt nhận thấy tình trạng lừa đảo để trục lợi trên các nền tảng công nghệ ngày càng gia tăng và có xu hướng trở nên tinh vi. Hơn 10 năm đồng hành cùng người dùng Việt, Nhà Tốt luôn..."
- `Candidate ID 3` [Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 — Cổng Thông tin điện tử Bộ Công an bài Công an tỉnh Tuyên Quang - Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 | Đoạn nguyên văn 12]: "Để tạo lòng tin, chúng sao chép hình ảnh, logo, địa chỉ, số điện thoại, nội dung giới thiệu từ trang thật; sử dụng tương tác ảo, tài khoản giả để bình luận tích cực, đánh giá 5 sao. Một số fanpage còn chạy quảng cáo trả phí để tiếp cận ngườ..."
- **Nhãn V15:** Qwen `partial` vs Gemini `partial`

### Câu 48: Nếu một tin đăng nhà trọ có thông tin sai, tôi có thể báo cáo cho nền tảng bằng cách nào?
**Qwen chọn nhưng Gemini bỏ:**
- `Candidate ID 4` [Cơ chế giải quyết tranh chấp của Chợ Tốt — Trợ Giúp Chợ Tốt - Cơ chế giải quyết tranh chấp của Chợ Tốt | Đoạn nguyên văn 75]: "1. Nguyên tắc giải quyết tranh chấp:

Khi phát sinh tranh chấp hoặc khiếu nại liên quan các hoạt động trên sàn giao dịch thương mại điện tử giữa Người mua và Người bán, Chợ Tốt khuyến khích hai bên có thể tự thương lượng, hoà giải để có thể..."
**Gemini chọn nhưng Qwen bỏ:**
- `Candidate ID 1` [Làm thế nào để báo cáo tin đăng — Trợ Giúp Chợ Tốt - Làm thế nào để báo cáo tin đăng | Đoạn nguyên văn 93]: "TRÊN TRÌNH DUYỆT WEB MÁY TÍNH

Cách 1: Thông báo trực tiếp trên website

Bước 1: Chọn tin mà bạn muốn báo cáo.

Bước 2: Chọn Báo cáo tin đăng bên dưới nội dung tin.

Bước 3: Chọn lý do báo cáo tin đăng.

Lừa đảo: Tin đăng không trung thực (..."
- `Candidate ID 3` [Nghị định 248/2026/NĐ-CP hướng dẫn Luật Thương mại điện tử — Chính phủ Công báo Chính phủ - Điều 17. Trách nhiệm của chủ quản nền tảng thương mại điện tử | Khoản 1]: "1. Chủ quản nền tảng thương mại điện tử thực hiện các trách nhiệm quy định tại Điều 15 của Luật Thương mại điện tử, trong đó một số nội dung được thực hiện cụ thể như sau:

a) Công bố đầy đủ, chính xác, rõ ràng các nội dung hoặc có đường li..."
- `Candidate ID 5` [Nghị định 248/2026/NĐ-CP hướng dẫn Luật Thương mại điện tử — Chính phủ Công báo Chính phủ - Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp]: "Điều 52. Điều khoản thi hành | Khoản 1
1. Nghị định này có hiệu lực thi hành từ ngày 01 tháng 7 năm 2026, trừ trường hợp quy định tại khoản 2 Điều này.

Điều 52. Điều khoản thi hành | Khoản 2
2. Chủ quản nền tảng thương mại điện tử có trách..."
- **Nhãn V15:** Qwen `partial` vs Gemini `high`

### Câu 50: Nếu người đăng yêu cầu chuyển cọc qua liên kết lạ, tôi nên kiểm tra những dấu hiệu nào trước khi trả tiền?
**Qwen chọn nhưng Gemini bỏ:**
- `Candidate ID 1` [Cảnh báo các thủ đoạn lừa đảo học sinh tân sinh viên mùa tựu trường — Cổng Thông tin điện tử Bộ Công an bài Công an TP Hải Phòng - Cảnh báo các thủ đoạn lừa đảo học sinh tân sinh viên mùa tựu trường | Đoạn nguyên văn 12]: "- Bẫy "Phòng trọ giá rẻ, view đẹp"; Kẻ gian đăng tải thông tin cho thuê phòng trọ giá siêu rẻ, vị trí đẹp trên các hội nhóm. Khi liên hệ, chúng sẽ dùng nhiều lý do (nhiều người hỏi thuê, chủ đi vắng...) để yêu cầu chuyển tiền đặt cọc giữ ch..."
- `Candidate ID 2` [Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 — Cổng Thông tin điện tử Bộ Công an bài Công an tỉnh Tuyên Quang - Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 | Đoạn nguyên văn 12]: "Để tạo lòng tin, chúng sao chép hình ảnh, logo, địa chỉ, số điện thoại, nội dung giới thiệu từ trang thật; sử dụng tương tác ảo, tài khoản giả để bình luận tích cực, đánh giá 5 sao. Một số fanpage còn chạy quảng cáo trả phí để tiếp cận ngườ..."
- `Candidate ID 3` [Cảnh báo bảo mật và liên kết lạ — Bộ Công an - Cảnh báo bảo mật và liên kết lạ — Bộ Công an]: "không truy cập đường link lạ..."
- **Nhãn V15:** Qwen `partial` vs Gemini `partial`

### Câu 52: Ảnh căn cước công dân của người thuê được lưu và sử dụng như thế nào?
**Qwen chọn nhưng Gemini bỏ:**
- `Candidate ID 3` [Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 — bản Word cung cấp - Điều 10. Yêu cầu rút lại sự đồng ý, yêu cầu hạn chế xử lý dữ liệu cá nhân]: "1. Chủ thể dữ liệu cá nhân có quyền yêu cầu rút lại sự đồng ý cho phép xử lý dữ liệu cá nhân, yêu cầu hạn chế xử lý dữ liệu cá nhân của mình khi có nghi ngờ phạm vi, mục đích xử lý dữ liệu cá nhân hoặc tính chính xác của dữ liệu cá nhân, tr..."
- **Nhãn V15:** Qwen `partial` vs Gemini `partial`

### Câu 53: Chủ trọ có được đăng công khai ảnh giấy tờ hoặc số điện thoại của tôi không?
**Qwen chọn nhưng Gemini bỏ:**
- `Candidate ID 2` [Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 — bản Word cung cấp - Điều 3. Nguyên tắc bảo vệ dữ liệu cá nhân | Khoản 2]: "2. Chỉ được thu thập, xử lý dữ liệu cá nhân đúng phạm vi, mục đích cụ thể, rõ ràng, bảo đảm tuân thủ quy định của pháp luật...."
- `Candidate ID 3` [Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 — bản Word cung cấp - Điều 9. Sự đồng ý của chủ thể dữ liệu cá nhân | Khoản 2]: "2. Sự đồng ý của chủ thể dữ liệu cá nhân chỉ có hiệu lực khi dựa trên sự tự nguyện và biết rõ các thông tin sau đây:

a) Loại dữ liệu cá nhân được xử lý, mục đích xử lý dữ liệu cá nhân;

b) Bên kiểm soát dữ liệu cá nhân hoặc bên kiểm soát v..."
- **Nhãn V15:** Qwen `partial` vs Gemini `partial`

### Câu 55: Người đăng yêu cầu đặt cọc trước nhưng không cho xem phòng: tôi nên kiểm tra những dấu hiệu rủi ro nào?
**Qwen chọn nhưng Gemini bỏ:**
- `Candidate ID 1` [Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 — Cổng Thông tin điện tử Bộ Công an bài Công an tỉnh Tuyên Quang - Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 | Đoạn nguyên văn 12]: "Để tạo lòng tin, chúng sao chép hình ảnh, logo, địa chỉ, số điện thoại, nội dung giới thiệu từ trang thật; sử dụng tương tác ảo, tài khoản giả để bình luận tích cực, đánh giá 5 sao. Một số fanpage còn chạy quảng cáo trả phí để tiếp cận ngườ..."
- **Nhãn V15:** Qwen `high` vs Gemini `high`
