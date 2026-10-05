# Kho Word bổ sung để thử nghiệm 36 câu

Đã tạo kho mới cùng bộ 16 tài liệu cũ theo yêu cầu. **Kho/API đang dùng không bị xóa hoặc chuyển sang kho mới.**

| Phần | Hiện đang dùng | Kho thử nghiệm |
|---|---|---|
| Pháp lý | `legal_word_v7_20261005` | `legal_word_supplement_v8_20261005` |
| Graph | `graph_rag_word_v6` | `graph_rag_word_supplement_v7` |
| Nhà trọ | `housing_graph_word_v6` | `housing_graph_word_supplement_v7` |

Kho thử nghiệm gồm 30 tài liệu: 16 cũ giữ nguyên byte, 12 bản chuyển nguyên văn website sang Word, 2 Word luật Công báo gốc. Có 393 đoạn/điều khoản và 423 vector E5 384 chiều; graph có 1.238 nút và 3.133 cạnh. Nhà trọ vẫn là đúng 789 bản ghi Datahouse cùng vector đã xác thực.

Đoạn dài được chia tối đa 1.200 ký tự khi embedding; giữ toàn đoạn/điều khoản cha trong DB. Phần hướng dẫn gom các đoạn liên quan đến khoảng 2.200 ký tự trước khi chia để tránh tách riêng tiêu đề và các bước thực hiện.

## Nguồn mới đã nạp

| Mã | Nội dung được chọn | Loại Word | Số đoạn/điều khoản |
|---|---|---|---:|
| S01: [Mẹo khi thuê phòng — Trợ Giúp Chợ Tốt](https://trogiup.chotot.com/nguoi-mua/meo-khi-thue-phong/) | Nguyên văn các mục liên quan; bỏ menu/quảng cáo/biểu mẫu | Chuyển từ HTML, không phải Word chính thức | 2 |
| S02: [Kinh nghiệm tìm nhà trọ cho tân sinh viên — Thư viện Đại học Bách khoa Hà Nội](https://library.hust.edu.vn/vi/node/822) | Nguyên văn các mục liên quan; bỏ menu/quảng cáo/biểu mẫu | Chuyển từ HTML, không phải Word chính thức | 1 |
| S03: [Thông tin giá điện — Trung tâm Chăm sóc khách hàng Điện lực miền Nam EVNSPC](https://cskh.evnspc.vn/TraCuu/ThongTinGiaDien) | Nguyên văn các mục liên quan; bỏ menu/quảng cáo/biểu mẫu | Chuyển từ HTML, không phải Word chính thức | 1 |
| S04: [Cơ chế giải quyết tranh chấp của Chợ Tốt — Trợ Giúp Chợ Tốt](https://trogiup.chotot.com/nguoi-mua/co-che-giai-quyet-tranh-chap-cua-cho-tot/) | Nguyên văn các mục liên quan; bỏ menu/quảng cáo/biểu mẫu | Chuyển từ HTML, không phải Word chính thức | 1 |
| S05: [Hướng dẫn tra cứu hóa đơn điện tử — CANTHOWASSCO Công ty Cổ phần Cấp thoát nước Cần Thơ](https://hddt.ctn-cantho.com.vn/huong-dan) | Nguyên văn các mục liên quan; bỏ menu/quảng cáo/biểu mẫu | Chuyển từ HTML, không phải Word chính thức | 1 |
| S06: [Hướng dẫn cài đặt ứng dụng Chăm sóc khách hàng CTWCare — CANTHOWASSCO](https://ctn-cantho.com.vn/tin-khoa-hoc-cong-nghe/huong-dan-cai-dat-ung-dung-cham-soc-khach-hang-ctwcare-822.html) | Nguyên văn các mục liên quan; bỏ menu/quảng cáo/biểu mẫu | Chuyển từ HTML, không phải Word chính thức | 1 |
| S08: [Làm thế nào để báo cáo tin đăng — Trợ Giúp Chợ Tốt](https://trogiup.chotot.com/nguoi-mua/lam-the-nao-de-bao-cao-tin-dang/) | Nguyên văn các mục liên quan; bỏ menu/quảng cáo/biểu mẫu | Chuyển từ HTML, không phải Word chính thức | 1 |
| S09: [Nhà Tốt bảo vệ người dùng như thế nào — Trợ Giúp Chợ Tốt Nhà Tốt](https://trogiup.chotot.com/nguoi-mua/nha-tot-bao-ve-nguoi-dung-nhu-the-nao/) | Nguyên văn các mục liên quan; bỏ menu/quảng cáo/biểu mẫu | Chuyển từ HTML, không phải Word chính thức | 1 |
| S10: [Quy chế hoạt động website cung cấp dịch vụ thương mại điện tử Chợ Tốt — Trợ Giúp Chợ Tốt](https://trogiup.chotot.com/nguoi-mua/hoat-dong/) | Nguyên văn các mục liên quan; bỏ menu/quảng cáo/biểu mẫu | Chuyển từ HTML, không phải Word chính thức | 4 |
| S11: [Cảnh báo các thủ đoạn lừa đảo học sinh tân sinh viên mùa tựu trường — Cổng Thông tin điện tử Bộ Công an bài Công an TP Hải Phòng](https://bocongan.gov.vn/bai-viet/catp-hai-phong-canh-bao-cac-thu-doan-lua-dao-bua-vay-hoc-sinh-tan-sinh-vien-mua-tuu-truong-1787629964) | Nguyên văn các mục liên quan; bỏ menu/quảng cáo/biểu mẫu | Chuyển từ HTML, không phải Word chính thức | 1 |
| S12: [Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 — Cổng Thông tin điện tử Bộ Công an bài Công an tỉnh Tuyên Quang](https://bocongan.gov.vn/bai-viet/canh-giac-thu-doan-lua-dao-mao-danh-fanpage-khach-san-nha-hang-dat-coc-truc-tuyen-dip-le-hoi-thanh-tuyen-2026-1790041513) | Nguyên văn các mục liên quan; bỏ menu/quảng cáo/biểu mẫu | Chuyển từ HTML, không phải Word chính thức | 1 |
| S14: [Tăng cường bảo đảm an toàn PCCC và kỹ năng thoát nạn tại các khu chung cư nhà trọ — Công an tỉnh Phú Thọ Phòng Cảnh sát PCCC và CNCH](https://congan.phutho.gov.vn/article/Tang-cuong-bao-dam-an-toan-phong-chay-chua-chay-27208-57) | Nguyên văn các mục liên quan; bỏ menu/quảng cáo/biểu mẫu | Chuyển từ HTML, không phải Word chính thức | 2 |
| S15: [Luật Thương mại điện tử 122/2025/QH15 — Quốc hội Công báo Chính phủ](https://congbao.chinhphu.vn/van-ban/luat-so-122-2025-qh15-468683/61714.htm) | Điều 3, 11, 15, 17, 18, 21, 40, 41 | Gốc Công báo | 41 |
| S16: [Nghị định 248/2026/NĐ-CP hướng dẫn Luật Thương mại điện tử — Chính phủ Công báo Chính phủ](https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-248-2026-nd-cp-469983.htm) | Điều 2, 4, 17, 18, 19, 52, 53 | Gốc Công báo | 21 |

## Chưa nạp

- S07: phần nội dung bài giá nước là ảnh; không lấy OCR và không dùng bảng giá ở chân trang thay thế bài viết.
- S13: cơ quan công bố chặn tải nguyên bản HTTP 403; giữ liên kết đọc, chưa dùng làm đầu vào Word.

## Kiểm tra và cách so sánh

Đã kiểm tra toàn bộ bản chuyển Word khớp chính xác các đoạn DOM nguồn sau chuẩn hóa khoảng trắng, SHA của hai Word gốc, SHA của 16 tài liệu cũ, đủ vector và graph khớp manifest. Dấu kiểm tra toàn bộ hàng trong kho cũ/nhà trọ/người dùng được đối chiếu trước và sau nạp; không thay đổi.
Chạy lại đúng ID 19–38 và 43–58. Giữ pipeline và câu hỏi giống baseline v7; chỉ đổi schema cho tiến trình đánh giá. Workflow vẫn Qwen + Gemini qua proxy được bạn cho phép. Đáp án mẫu không embedding, chỉ đưa vào Qwen cục bộ để đối chiếu sau khi sinh xong.
So sánh số câu chạy xong/lỗi, mức khớp cao/một phần/thấp với đáp án mẫu, từng ID tăng/giảm, nguồn truy xuất và thời gian. Mức khớp không phải tỷ lệ đúng pháp luật. Các thời hạn/cọc minh họa trong đáp án mẫu và quy định TMĐT cũ cần đối chiếu lại.

Kết quả: [Bản so sánh 36 câu](WORD_SUPPLEMENT_COMPARISON_20261005.md) sau khi hoàn tất cả lượt sinh và chấm đối chiếu.

## Tái lập

- `scripts/fetch_word_supplement.py`: lưu HTML công khai nguyên byte và dấu nguồn ở thư mục cục bộ bỏ qua Git.
- `scripts/prepare_word_supplement.py`: chọn nguyên văn, chuyển Word, giữ 16 mục manifest cũ, không đọc đáp án mẫu.
- `eval/check_word_supplement_inputs.py`: kiểm tra HTML → Word → đoạn đưa vào embedding.
- `eval/audit_word_supplement.py before/after`: kiểm tra giữ nguyên kho hiện hành và đủ vector/graph mới; baseline không được ghi đè.
- `eval/report_word_supplement_comparison.py`: đối chiếu đúng hai lượt và chính sách chấm, xuất bản tổng hợp sau khi đủ 36 câu.

Không chạy script kích hoạt/xóa kho trong thử nghiệm này. Raw HTML, dữ liệu nhà trọ và toàn văn đáp án mẫu/báo cáo giữ cục bộ.
