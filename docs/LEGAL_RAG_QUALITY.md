# Kiểm tra chất lượng chatbot pháp luật

## Vấn đề và cách xử lý

Câu hỏi về chủ trọ thu tiền điện từng lấy nhầm các đoạn về hành lang an toàn,
đường dây và trộm cắp điện. Thông tư 60 có lớp chữ PDF hỏng nhưng đủ dài nên
không được OCR; trang đầu Nghị định 133 chỉ có chữ ký số trong lớp chữ.

- Kiểm tra chất lượng chữ và trang scan có lớp chữ ký; lựa chọn kết quả OCR theo
  chất lượng thay vì độ dài. Không sửa số tiền bằng phỏng đoán.
- Chia theo Điều, khoản, điểm; mỗi điểm giữ phần dẫn của khoản và số trang.
  Tách phụ lục/nơi nhận để không gắn nhầm vào điều khoản hiệu lực.
- Lưu phiên bản trích xuất và cảnh báo chất lượng. Chỉ mục cũ tự được làm lại
  khi chạy indexer; PDF nguồn không bị sửa. Các đoạn hỏng hoặc có khoảng tiền
  đảo ngược không được dùng để trả lời.
- Tìm kiếm pháp luật giữ từ chỉ quan hệ thuê nhà, mở rộng từ đồng nghĩa và lấy
  ứng viên từ cả từ khóa, cụm từ và vector. Nhóm câu hỏi tiền điện ưu tiên kho điện.
- Xếp hạng lại tối đa 30 ứng viên, ghép phần tiếp nối cùng điều khoản và bổ sung
  điều kiện hiệu lực/chuyển tiếp của tài liệu được chọn. Không nhúng sẵn câu trả lời
  hoặc mức giá vào công cụ tìm kiếm.
- Khi thiếu nguồn, thử lại bằng từ khóa pháp lý. Khi câu trả lời vi phạm kiểm tra
  căn cứ, cho mô hình sửa một lần rồi dùng thông báo chưa đủ căn cứ nếu vẫn lỗi.
- Phân biệt thiếu căn cứ truy xuất với kết luận pháp luật không có quy định.
  Giữ giới hạn hóa đơn, điều kiện đồng thời, lãi suất thỏa thuận và thời điểm áp dụng.
- Khi nguồn trực tiếp có điều khoản về thu tiền điện, định mức, hoàn trả hoặc xử
  phạt, trả lời bằng trích đoạn có nguồn (`legal-extractive`) để giữ nguyên điều kiện;
  không yêu cầu mô hình nhỏ diễn giải lại các quan hệ tài chính. Các câu khác vẫn
  dùng mô hình đang cấu hình. Điều kiện hiệu lực bị bỏ sót được bổ sung bằng chính
  câu điều kiện trong nguồn, không tự suy ra ngày áp dụng.
- API chỉ nạp embedding đã có trong cache; tải mô hình thuộc bước lập chỉ mục.
  Thiếu cache thì báo chế độ tìm từ khóa, không chờ tải mạng trong một câu hỏi.

Các kiểm tra từ vựng, con số và điều kiện là **heuristic**, không phải chứng minh
mọi câu trả lời đúng về pháp lý. OCR vẫn có thể sai số hoặc ngày mà heuristic không
phát hiện; cần đối chiếu bản ký đối với dữ kiện quan trọng. Bộ kiểm thử tự động
không xác nhận giá điện hiện hành hoặc mọi sửa đổi pháp luật ngoài kho dữ liệu.

## Cập nhật dữ liệu

```powershell
docker compose build legal-indexer
docker compose --profile tools run --rm legal-indexer --data-dir /data
```

Indexer áp migration 94 và 98, xử lý lại bản trích xuất cũ và tạo embedding mới.
Dùng `--category electricity` để chỉ xử lý nhóm điện; `--source` có thể lặp lại
để chọn các đường dẫn tương đối mà vẫn giữ đúng danh tính tài liệu:

```powershell
docker compose --profile tools run --rm legal-indexer --data-dir /data --source "electricity/thong tu so 60 2025.pdf" --source "electricity/nghi dinh so 133 2026.pdf"
```

`--force-ocr` cũng buộc lập lại chỉ mục file không đổi. Mặc định ưu tiên lớp chữ
đọc tốt; không cần ép OCR toàn bộ tài liệu. `CHATBOT_LEGAL_TIMEOUT_SECONDS=120`
tách thời gian chờ câu hỏi luật khỏi câu hỏi tìm phòng.

## Kiểm thử tái lập

Toàn bộ backend dùng cơ sở dữ liệu thử nghiệm riêng:

```powershell
docker compose -f docker-compose.test.yml up --build --abort-on-container-exit --exit-code-from api
```

Đánh giá kho dữ liệu thực bằng 8 câu trong `eval/datasets/legal_electricity_eval.json`:

```powershell
docker compose --profile tools run --rm --no-deps -v "${PWD}/eval:/eval" api python /eval/legal_eval.py --retrieval-only --lexical-only --out /eval/reports/legal_retrieval_lexical.json
docker compose --profile tools run --rm --no-deps -v "${PWD}/eval:/eval" api python /eval/legal_eval.py --retrieval-only --out /eval/reports/legal_retrieval_hybrid.json
docker compose --profile tools run --rm --no-deps -v "${PWD}/eval:/eval" api python /eval/legal_eval.py --out /eval/reports/legal_generation.json
```

Phải build lại API trước khi chạy để dùng mã hiện tại. Script dùng cấu hình mô hình
của API, chỉ đọc kho luật, không tạo tài khoản hay lưu hội thoại/telemetry. Báo cáo
chứa câu hỏi, câu trả lời, nguồn, kiểm tra tìm điều khoản và kiểm tra câu trả lời;
`provider=template` không được tính là trả lời thành công cho câu có căn cứ.

Các báo cáo JSON lưu bằng chứng chạy thực tế; xem thêm `eval/reports/legal_eval.md`
để biết kết quả và giới hạn của lần đánh giá được công bố.
