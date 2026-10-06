# Báo cáo Phép thử Đối chứng: Qwen Selector vs Gemini Selector (legal_selector_ab_36_v1_20261006)

**Mục tiêu:** Xác định việc thay Qwen bằng Gemini ở **RIÊNG** bước chọn nguồn có cải thiện hệ thống hay không.

## 1. Bằng chứng Phép thử Hợp lệ
- **Git Commit:** `373a3d68d26db755f1e63f2b5557adc02761fab4`
- **Snapshot SHA256:** `7ffe56f0c98e9e8c4978056a8a98e0817e464cf553d5fbf757139af7c66b1619`
- **Corpus Schema:** `legal_word_repair_v16_20261006` (Graph: `graph_rag_word_repair_v16`, Housing: `housing_graph_word_repair_v16`)
- **Biến duy nhất thay đổi:** Model/provider chọn nguồn (`Ollama Qwen` vs `Gemini Proxy`).
- **Điều kiện cố định tuyệt đối:** Cùng snapshot 36 câu (QuestionPlan + candidate chunks nguyên vẹn); cùng Gemini Writer (riêng); cùng Gemini Verifier (riêng); cùng giới hạn sửa tối đa 1 lần; cùng judge V15 cục bộ Qwen.
- **Không dùng combined mode; không sửa prompt viết, prompt kiểm chứng hay rubric chấm.**

## 2. Bảng So sánh Tổng hợp

| Chỉ số | Nhánh A (Qwen chọn nguồn) | Nhánh B (Gemini chọn nguồn) | Chênh lệch (B - A) |
|---|---:|---:|---:|
| Số câu hoàn thành / lỗi | 36 / 0 | 36 / 0 | 0 |
| Thời gian chọn nguồn (Trung vị) | 45.98s | 3.62s | -42.36s |
| Thời gian chọn nguồn (P95) | 75.7s | 7.53s | -68.17s |
| Chọn nguồn đến câu trả lời cuối (Trung vị) | 65.71s | 19.47s | -46.24s |
| Chọn nguồn đến câu trả lời cuối (P95) | 108.32s | 35.4s | -72.92s |
| Tổng request Gemini | 104 | 149 | 45 |
| Số câu phải sửa nội dung (1 lần) | 16 | 15 | -1 |
| Số câu fallback nguồn | 0 | 0 | 0 |
| Số câu trả lời một phần (partial) | 23 | 20 | -3 |
| V15 High / Partial / Low | 8 / 26 / 2 | 7 / 26 / 3 | High: -1, Low: 1 |

> **Lưu ý về thời gian phân tích/truy xuất cố định:**
> - Thời gian phân tích câu hỏi (Gemini Question Analyzer): trung vị 3.97s, P95 6.06s.
> - Thời gian truy xuất E5 + BM25 + Graph: trung vị 0.14s, P95 0.27s.
> - Các thời gian này đã được cố định và lưu trong snapshot dùng chung cho cả hai nhánh.

## 3. Biến động Nhãn V15
- **Giữ nguyên nhãn:** 28 câu
- **Tăng nhãn:** 3 câu (['Q21 (partial->high)', 'Q24 (low->partial)', 'Q50 (partial->high)'])
- **Giảm nhãn:** 5 câu (['Q43 (high->partial)', 'Q44 (partial->low)', 'Q45 (partial->low)', 'Q51 (high->partial)', 'Q58 (high->partial)'])

## 4. Chi tiết Từng Câu: So Sánh Nguồn Được Chọn và V15

| ID | Qwen chọn | Gemini chọn | Điểm chung | Khác biệt | Tác động V15 (A -> B) | Trạng thái B |
|---:|---|---|---|---|:---:|---|
| 19 | [1, 2, 3, 4] | [1, 2, 3, 4] | [1, 2, 3, 4] | Trùng 100% | partial -> partial | Repaired |
| 20 | [1, 2, 3, 4] | [1, 2, 3, 4] | [1, 2, 3, 4] | Trùng 100% | high -> high | OK |
| 21 | [1, 3] | [1, 3] | [1, 3] | Trùng 100% | partial -> high | Repaired |
| 22 | [1, 3, 4] | [1, 4] | [1, 4] | Qwen-only: [3] | partial -> partial | OK |
| 23 | [1, 2] | [1, 2] | [1, 2] | Trùng 100% | partial -> partial | OK |
| 24 | [1, 2] | [1, 2] | [1, 2] | Trùng 100% | low -> partial | Repaired |
| 25 | [1, 2] | [1, 2] | [1, 2] | Trùng 100% | partial -> partial | OK |
| 26 | [1, 2, 4, 5] | [1, 2, 4, 5] | [1, 2, 4, 5] | Trùng 100% | partial -> partial | OK |
| 27 | [1, 2, 3] | [1, 2] | [1, 2] | Qwen-only: [3] | partial -> partial | OK |
| 28 | [2, 3, 4, 5] | [2, 3, 4, 5] | [2, 3, 4, 5] | Trùng 100% | low -> low | Repaired |
| 29 | [1, 2, 3, 5] | [1, 2, 3, 5] | [1, 2, 3, 5] | Trùng 100% | partial -> partial | Repaired |
| 30 | [2] | [2] | [2] | Trùng 100% | partial -> partial | OK |
| 31 | [1, 2] | [1] | [1] | Qwen-only: [2] | partial -> partial | Repaired |
| 32 | [1, 2, 3, 4, 5] | [1, 2, 3, 4, 5] | [1, 2, 3, 4, 5] | Trùng 100% | partial -> partial | OK |
| 33 | [1, 2, 3] | [1] | [1] | Qwen-only: [2, 3] | partial -> partial | OK |
| 34 | [1, 2, 3, 4, 5] | [1, 2, 3, 5] | [1, 2, 3, 5] | Qwen-only: [4] | partial -> partial | OK |
| 35 | [1, 2, 3] | [1, 2, 3] | [1, 2, 3] | Trùng 100% | partial -> partial | Repaired |
| 36 | [1, 2, 3] | [1, 2, 3] | [1, 2, 3] | Trùng 100% | partial -> partial | OK |
| 37 | [1, 2, 3, 4] | [1, 2, 3] | [1, 2, 3] | Qwen-only: [4] | high -> high | Repaired |
| 38 | [1, 2, 3] | [1, 3] | [1, 3] | Qwen-only: [2] | partial -> partial | Repaired |
| 43 | [1, 2, 3, 4, 5] | [1, 4, 5] | [1, 4, 5] | Qwen-only: [2, 3] | high -> partial | OK |
| 44 | [1, 2, 3, 5] | [] | [] | Qwen-only: [1, 2, 3, 5] | partial -> low | OK |
| 45 | [1, 2, 4, 5] | [1, 2, 4, 5] | [1, 2, 4, 5] | Trùng 100% | partial -> low | Repaired |
| 46 | [1, 2, 3, 5] | [1, 2, 3, 4, 5] | [1, 2, 3, 5] | Gemini-only: [4] | partial -> partial | OK |
| 47 | [1, 2, 3, 4] | [2, 4] | [2, 4] | Qwen-only: [1, 3] | partial -> partial | Repaired |
| 48 | [1, 2, 3, 4, 5] | [1, 2, 3, 5] | [1, 2, 3, 5] | Qwen-only: [4] | high -> high | OK |
| 49 | [1, 2, 3, 4] | [1, 2, 3, 4] | [1, 2, 3, 4] | Trùng 100% | partial -> partial | Repaired |
| 50 | [1, 2, 3] | [1, 2, 3] | [1, 2, 3] | Trùng 100% | partial -> high | OK |
| 51 | [1, 2, 3] | [1, 2, 3] | [1, 2, 3] | Trùng 100% | high -> partial | OK |
| 52 | [1, 2, 3, 4] | [1, 2] | [1, 2] | Qwen-only: [3, 4] | high -> high | OK |
| 53 | [1, 2, 3] | [1] | [1] | Qwen-only: [2, 3] | partial -> partial | OK |
| 54 | [1, 2, 3] | [1, 2] | [1, 2] | Qwen-only: [3] | partial -> partial | OK |
| 55 | [1, 2] | [2] | [2] | Qwen-only: [1] | high -> high | OK |
| 56 | [1, 2, 3] | [1, 2] | [1, 2] | Qwen-only: [3] | partial -> partial | Repaired |
| 57 | [1, 2, 3] | [2, 3] | [2, 3] | Qwen-only: [1] | partial -> partial | Repaired |
| 58 | [1, 2, 3] | [1] | [1] | Qwen-only: [2, 3] | high -> partial | Repaired |

## 5. Bằng chứng Trích đoạn Cụ thể cho Các Câu Khác Biệt Nguồn
### Câu 22: Khi trả phòng, việc hoàn lại tiền cọc được xác định theo hợp đồng và quy định như thế nào?
**Qwen chọn nhưng Gemini bỏ:**
- `Candidate ID 3` [Mẹo khi thuê phòng — Trợ Giúp Chợ Tốt - Mẹo khi thuê phòng | Đoạn nguyên văn 78]: "1. Kiểm tra độ uy tín của người cho thuê trên môi trường trực tuyến (Google, Facebook, diễn đàn, …)

Tìm kiếm số điện thoại và địa chỉ muốn thuê trên Google, Facebook, các diễn đàn trực tuyến, … và xem các thông tin giao dịch trước đó như đ..."
- **Nhãn V15:** Qwen `partial` vs Gemini `partial`

### Câu 27: Giá nước sinh hoạt áp dụng cho phòng trọ ở Cần Thơ được xác định theo căn cứ nào?
**Qwen chọn nhưng Gemini bỏ:**
- `Candidate ID 3` [Giá nước Cần Thơ 215/QĐ-UBND — bản Word cung cấp - Điều 2. Điều chỉnh giá nước sạch | Khoản 2]: "2. Hàng năm, các đơn vị cấp nước chủ động rà soát việc thực hiện phương án giá nước sạch và giá nước sạch dự kiến cho năm tiếp theo trên cơ sở quy định tại Điều 4 Thông tư số 44/2021/TT-BTC ngày 18 tháng 6 năm 2021 của Bộ trưởng Bộ Tài chín..."
- **Nhãn V15:** Qwen `partial` vs Gemini `partial`

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

### Câu 37: Nếu lối thoát nạn bị khóa hoặc bị chặn, người thuê nên làm gì?
**Qwen chọn nhưng Gemini bỏ:**
- `Candidate ID 4` [Luật PCCC 55/2024/QH15 — Word Công báo - Điều 20. Phòng cháy đối với nhà ở]: "1. Nhà ở không thuộc loại hình quy định tại khoản 3 và khoản 4 Điều này
phải bảo đảm các điều kiện an toàn về phòng cháy sau đây:
 a) Lắp đặt, sử dụng thiết bị điện bảo đảm điều kiện an toàn về phòng
cháy quy định tại điểm c khoản 1 Điều 24..."
- **Nhãn V15:** Qwen `high` vs Gemini `high`

### Câu 38: Chủ trọ và người thuê có trách nhiệm gì đối với thiết bị điện và an toàn cháy nổ?
**Qwen chọn nhưng Gemini bỏ:**
- `Candidate ID 2` [Luật PCCC 55/2024/QH15 — Word Công báo - Điều 8. Trách nhiệm của cơ quan, tổ chức, hộ gia đình, cá nhân trong | Khoản 6]: "hoạt động phòng cháy, chữa cháy, cứu nạn, cứu hộ

6. Chủ hộ gia đình trực tiếp sử dụng nhà ở mà không phải là người đứng
đầu cơ sở có trách nhiệm sau đây:
 a) Thực hiện quy định tại Điều 20 và Điều 21 của Luật này;
 b) Tuyên truyền, đôn đốc..."
- **Nhãn V15:** Qwen `partial` vs Gemini `partial`

### Câu 43: Người giới thiệu phòng trọ và thu phí môi giới cần công khai những thông tin gì?
**Qwen chọn nhưng Gemini bỏ:**
- `Candidate ID 2` [Luật Kinh doanh bất động sản 29/2023/QH15 — bản Word cung cấp - Điều 46. Nội dung chính của hợp đồng trong kinh doanh bất động sản | Khoản 4]: "4. Hợp đồng kinh doanh dịch vụ bất động sản phải có các nội dung chính sau đây:

a) Tên, địa chỉ của các bên;

b) Đối tượng và nội dung dịch vụ;

c) Yêu cầu và kết quả dịch vụ;

d) Thời hạn thực hiện dịch vụ;

đ) Phí dịch vụ, thù lao, hoa h..."
- `Candidate ID 3` [Luật Kinh doanh bất động sản 29/2023/QH15 — bản Word cung cấp - Điều 61. Điều kiện của tổ chức, cá nhân kinh doanh dịch vụ môi giới bất động sản | Khoản 1]: "1. Tổ chức, cá nhân kinh doanh dịch vụ môi giới bất động sản phải thành lập doanh nghiệp kinh doanh dịch vụ bất động sản theo quy định tại khoản 5 Điều 9 của Luật này và phải đáp ứng các điều kiện sau đây:

a) Phải có quy chế hoạt động dịch..."
- **Nhãn V15:** Qwen `high` vs Gemini `partial`

### Câu 44: Trước khi chuyển tiền cho người môi giới, tôi nên kiểm tra quyền cho thuê và thông tin phòng như thế nào?
**Qwen chọn nhưng Gemini bỏ:**
- `Candidate ID 1` [Bộ luật Dân sự 91/2015/QH13 — Word do cơ quan nhà nước công bố - Điều 520. Đơn phương chấm dứt thực hiện hợp đồng dịch vụ | Khoản 1]: "1. Trường hợp việc tiếp tục thực hiện công việc không có lợi cho bên sử
dụng dịch vụ thì bên sử dụng dịch vụ có quyền đơn phương chấm dứt thực hiện
hợp đồng, nhưng phải báo cho bên cung ứng dịch vụ biết trước một thời gian
hợp lý; bên sử dụ..."
- `Candidate ID 2` [Luật Kinh doanh bất động sản 29/2023/QH15 — bản Word cung cấp - Điều 46. Nội dung chính của hợp đồng trong kinh doanh bất động sản | Khoản 4]: "4. Hợp đồng kinh doanh dịch vụ bất động sản phải có các nội dung chính sau đây:

a) Tên, địa chỉ của các bên;

b) Đối tượng và nội dung dịch vụ;

c) Yêu cầu và kết quả dịch vụ;

d) Thời hạn thực hiện dịch vụ;

đ) Phí dịch vụ, thù lao, hoa h..."
- `Candidate ID 3` [Bộ luật Dân sự 91/2015/QH13 — Word do cơ quan nhà nước công bố - Điều 513. Hợp đồng dịch vụ]: "Điều 513. Hợp đồng dịch vụ

Hợp đồng dịch vụ là sự thỏa thuận giữa các bên, theo đó bên cung ứng dịch
vụ thực hiện công việc cho bên sử dụng dịch vụ, bên sử dụng dịch vụ phải
trả tiền dịch vụ cho bên cung ứng dịch vụ...."
- `Candidate ID 5` [Bộ luật Dân sự 91/2015/QH13 — Word do cơ quan nhà nước công bố - Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp]: "Điều 117. Điều kiện có hiệu lực của giao dịch dân sự | Khoản 1
1. Giao dịch dân sự có hiệu lực khi có đủ các điều kiện sau đây:

a) Chủ thể có năng lực pháp luật dân sự, năng lực hành vi dân sự phù hợp
với giao dịch dân sự được xác lập;

b)..."
- **Nhãn V15:** Qwen `partial` vs Gemini `low`

### Câu 46: Khoản phí môi giới nên được thỏa thuận và thể hiện trong giấy tờ ra sao?
**Gemini chọn nhưng Qwen bỏ:**
- `Candidate ID 4` [Bộ luật Dân sự 91/2015/QH13 — Word do cơ quan nhà nước công bố - Điều 513. Hợp đồng dịch vụ]: "Điều 513. Hợp đồng dịch vụ

Hợp đồng dịch vụ là sự thỏa thuận giữa các bên, theo đó bên cung ứng dịch
vụ thực hiện công việc cho bên sử dụng dịch vụ, bên sử dụng dịch vụ phải
trả tiền dịch vụ cho bên cung ứng dịch vụ...."
- **Nhãn V15:** Qwen `partial` vs Gemini `partial`

### Câu 47: Khi tìm phòng qua một nền tảng trực tuyến, tôi nên kiểm tra người đăng và nguồn tin như thế nào?
**Qwen chọn nhưng Gemini bỏ:**
- `Candidate ID 1` [Nhà Tốt bảo vệ người dùng như thế nào — Trợ Giúp Chợ Tốt Nhà Tốt - Nhà Tốt bảo vệ người dùng như thế nào | Đoạn nguyên văn 75]: "Trong thời gian gần đây, Nền tảng Công nghệ Bất động sản Nhà Tốt nhận thấy tình trạng lừa đảo để trục lợi trên các nền tảng công nghệ ngày càng gia tăng và có xu hướng trở nên tinh vi. Hơn 10 năm đồng hành cùng người dùng Việt, Nhà Tốt luôn..."
- `Candidate ID 3` [Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 — Cổng Thông tin điện tử Bộ Công an bài Công an tỉnh Tuyên Quang - Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 | Đoạn nguyên văn 12]: "Để tạo lòng tin, chúng sao chép hình ảnh, logo, địa chỉ, số điện thoại, nội dung giới thiệu từ trang thật; sử dụng tương tác ảo, tài khoản giả để bình luận tích cực, đánh giá 5 sao. Một số fanpage còn chạy quảng cáo trả phí để tiếp cận ngườ..."
- **Nhãn V15:** Qwen `partial` vs Gemini `partial`

### Câu 48: Nếu một tin đăng nhà trọ có thông tin sai, tôi có thể báo cáo cho nền tảng bằng cách nào?
**Qwen chọn nhưng Gemini bỏ:**
- `Candidate ID 4` [Cơ chế giải quyết tranh chấp của Chợ Tốt — Trợ Giúp Chợ Tốt - Cơ chế giải quyết tranh chấp của Chợ Tốt | Đoạn nguyên văn 75]: "1. Nguyên tắc giải quyết tranh chấp:

Khi phát sinh tranh chấp hoặc khiếu nại liên quan các hoạt động trên sàn giao dịch thương mại điện tử giữa Người mua và Người bán, Chợ Tốt khuyến khích hai bên có thể tự thương lượng, hoà giải để có thể..."
- **Nhãn V15:** Qwen `high` vs Gemini `high`

### Câu 52: Ảnh căn cước công dân của người thuê được lưu và sử dụng như thế nào?
**Qwen chọn nhưng Gemini bỏ:**
- `Candidate ID 3` [Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 — bản Word cung cấp - Điều 10. Yêu cầu rút lại sự đồng ý, yêu cầu hạn chế xử lý dữ liệu cá nhân]: "1. Chủ thể dữ liệu cá nhân có quyền yêu cầu rút lại sự đồng ý cho phép xử lý dữ liệu cá nhân, yêu cầu hạn chế xử lý dữ liệu cá nhân của mình khi có nghi ngờ phạm vi, mục đích xử lý dữ liệu cá nhân hoặc tính chính xác của dữ liệu cá nhân, tr..."
- `Candidate ID 4` [Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 — bản Word cung cấp - Điều 9. Sự đồng ý của chủ thể dữ liệu cá nhân | Khoản 2]: "2. Sự đồng ý của chủ thể dữ liệu cá nhân chỉ có hiệu lực khi dựa trên sự tự nguyện và biết rõ các thông tin sau đây:

a) Loại dữ liệu cá nhân được xử lý, mục đích xử lý dữ liệu cá nhân;

b) Bên kiểm soát dữ liệu cá nhân hoặc bên kiểm soát v..."
- **Nhãn V15:** Qwen `high` vs Gemini `high`

### Câu 53: Chủ trọ có được đăng công khai ảnh giấy tờ hoặc số điện thoại của tôi không?
**Qwen chọn nhưng Gemini bỏ:**
- `Candidate ID 2` [Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 — bản Word cung cấp - Điều 3. Nguyên tắc bảo vệ dữ liệu cá nhân | Khoản 2]: "2. Chỉ được thu thập, xử lý dữ liệu cá nhân đúng phạm vi, mục đích cụ thể, rõ ràng, bảo đảm tuân thủ quy định của pháp luật...."
- `Candidate ID 3` [Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 — bản Word cung cấp - Điều 9. Sự đồng ý của chủ thể dữ liệu cá nhân | Khoản 2]: "2. Sự đồng ý của chủ thể dữ liệu cá nhân chỉ có hiệu lực khi dựa trên sự tự nguyện và biết rõ các thông tin sau đây:

a) Loại dữ liệu cá nhân được xử lý, mục đích xử lý dữ liệu cá nhân;

b) Bên kiểm soát dữ liệu cá nhân hoặc bên kiểm soát v..."
- **Nhãn V15:** Qwen `partial` vs Gemini `partial`

### Câu 54: Nếu thông tin cá nhân của tôi bị chia sẻ sai mục đích, tôi nên yêu cầu xử lý như thế nào?
**Qwen chọn nhưng Gemini bỏ:**
- `Candidate ID 3` [Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 — bản Word cung cấp - Điều 3. Nguyên tắc bảo vệ dữ liệu cá nhân | Khoản 2]: "2. Chỉ được thu thập, xử lý dữ liệu cá nhân đúng phạm vi, mục đích cụ thể, rõ ràng, bảo đảm tuân thủ quy định của pháp luật...."
- **Nhãn V15:** Qwen `partial` vs Gemini `partial`

### Câu 55: Người đăng yêu cầu đặt cọc trước nhưng không cho xem phòng: tôi nên kiểm tra những dấu hiệu rủi ro nào?
**Qwen chọn nhưng Gemini bỏ:**
- `Candidate ID 1` [Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 — Cổng Thông tin điện tử Bộ Công an bài Công an tỉnh Tuyên Quang - Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 | Đoạn nguyên văn 12]: "Để tạo lòng tin, chúng sao chép hình ảnh, logo, địa chỉ, số điện thoại, nội dung giới thiệu từ trang thật; sử dụng tương tác ảo, tài khoản giả để bình luận tích cực, đánh giá 5 sao. Một số fanpage còn chạy quảng cáo trả phí để tiếp cận ngườ..."
- **Nhãn V15:** Qwen `high` vs Gemini `high`

### Câu 56: Tôi đã chuyển cọc cho một tin trọ có dấu hiệu giả mạo; nên lưu lại bằng chứng gì và trình báo ở đâu?
**Qwen chọn nhưng Gemini bỏ:**
- `Candidate ID 3` [Bộ luật Tố tụng hình sự 17/VBHN-VPQH — bản Word trích tuyển cung cấp - Điều 145. Trách nhiệm tiếp nhận và thẩm quyền giải quyết tố giác, tin báo về tội phạm, kiến nghị khởi tố | Khoản 3]: "3. Thẩm quyền giải quyết tố giác, tin báo về tội phạm, kiến nghị khởi tố:

a) Cơ quan điều tra giải quyết tố giác, tin báo về tội phạm, kiến nghị khởi tố theo thẩm quyền điều tra của mình;

b) Cơ quan được giao nhiệm vụ tiến hành một số hoạ..."
- **Nhãn V15:** Qwen `partial` vs Gemini `partial`

### Câu 57: Khi nào tranh chấp tiền cọc có thể có dấu hiệu lừa đảo, và khi nào chỉ là tranh chấp hợp đồng?
**Qwen chọn nhưng Gemini bỏ:**
- `Candidate ID 1` [Mẹo khi thuê phòng — Trợ Giúp Chợ Tốt - Mẹo khi thuê phòng | Đoạn nguyên văn 78]: "1. Kiểm tra độ uy tín của người cho thuê trên môi trường trực tuyến (Google, Facebook, diễn đàn, …)

Tìm kiếm số điện thoại và địa chỉ muốn thuê trên Google, Facebook, các diễn đàn trực tuyến, … và xem các thông tin giao dịch trước đó như đ..."
- **Nhãn V15:** Qwen `partial` vs Gemini `partial`

### Câu 58: Nếu có nhiều sinh viên cùng bị một người nhận cọc rồi cắt liên lạc, chúng tôi nên cung cấp thông tin gì cho cơ quan có thẩm quyền?
**Qwen chọn nhưng Gemini bỏ:**
- `Candidate ID 2` [Bộ luật Tố tụng hình sự 17/VBHN-VPQH — bản Word trích tuyển cung cấp - Điều 145. Trách nhiệm tiếp nhận và thẩm quyền giải quyết tố giác, tin báo về tội phạm, kiến nghị khởi tố | Khoản 2]: "2. Cơ quan, tổ chức có trách nhiệm tiếp nhận tố giác, tin báo về tội phạm, kiến nghị khởi tố gồm:

a) Cơ quan điều tra, Viện kiểm sát tiếp nhận tố giác, tin báo về tội phạm, kiến nghị khởi tố;

b) Cơ quan, tổ chức khác tiếp nhận tố giác, ti..."
- `Candidate ID 3` [Bộ luật Tố tụng hình sự 17/VBHN-VPQH — bản Word trích tuyển cung cấp - Điều 145. Trách nhiệm tiếp nhận và thẩm quyền giải quyết tố giác, tin báo về tội phạm, kiến nghị khởi tố | Khoản 4]: "4. Cơ quan có thẩm quyền giải quyết tố giác, tin báo về tội phạm, kiến nghị khởi tố có trách nhiệm thông báo kết quả giải quyết cho cá nhân, cơ quan, tổ chức đã tố giác, báo tin về tội phạm, kiến nghị khởi tố...."
- **Nhãn V15:** Qwen `high` vs Gemini `partial`
