# Bổ sung dữ liệu KTX cho chatbot — 07/10/2026

Chatbot local trước thay đổi đang trỏ đến `legal_word_v7_20261005` và `graph_rag_word_v6`. Kho này không có nhóm `student_housing`, dù ba tài liệu KTX đã có ở corpus v5. Vì vậy các câu hỏi KTX không lấy được dữ liệu.

Bản `legal_ctu_ktx_v1_20261007` giữ nguyên tài liệu và vector của kho đang phục vụ, bổ sung 4 nguồn CTU, 46 đơn vị nội dung và 52 vector thật từ `intfloat/multilingual-e5-small` (384 chiều). Graph `graph_ctu_ktx_v1_20261007` bổ sung nút tài liệu, đơn vị nội dung và chủ đề KTX, giữ kho phòng `housing_graph_word_v6`. Snapshot trong `eval/reports/ctu_ktx_index_20261007.json` xác nhận kho gốc không thay đổi.

Nguồn:

- [Thông báo đăng ký KTX HK1 năm học 2026–2027](https://ssc.ctu.edu.vn/thong-bao/226-dang-ky-o-ky-tuc-xa-hoc-ky-1-nam-hoc-2026-2027.html).
- [Hướng dẫn tân sinh viên đăng ký KTX](https://tansinhvien.ctu.edu.vn/sinh-hoat/huong-dan-tan-sinh-vien-dang-ky-o-ky-tuc-xa).
- [Nội quy KTX công bố 09/2025](https://ssc.ctu.edu.vn/images/upload/Noiquy_KTX_trich_092025.pdf).
- [Cơ sở vật chất, loại phòng và phí KTX](https://ssc.ctu.edu.vn/hoat/160-cs1.html), tải ngày 07/10/2026.

Giữ nguyên ngày học kỳ trong nguồn. Bài cơ sở vật chất không ghi ngày công bố; mức phí chỉ là mức được trang đó công bố, không xác nhận phòng trống hoặc mức phí của một phòng cụ thể. Không suy diễn bảng phí từ ảnh, không lấy đáp án đánh giá để lập chỉ mục.

`scripts/prepare_ctu_ktx_corpus.py` kiểm tra hash của nguồn KTX sẵn có, tải bài cơ sở vật chất và xuất manifest tại `docs/ctu_ktx_corpus_20261007/`. `scripts/index_ctu_ktx.py` tạo bản riêng từ cấu hình API đang chạy, sinh vector, giữ đầy đủ nội dung cha và kiểm tra hash nguồn/graph. Khi chạy trong API image với repo ở `/workspace`, đặt `PYTHONPATH=/app`. Chạy lại cùng manifest bỏ qua tài liệu không đổi; dữ liệu khác phải dùng tên release mới.

Sau khi đã chuyển API sang bản KTX, chạy lại indexer cần chỉ rõ `--base-schema legal_word_v7_20261005 --base-graph-schema graph_rag_word_v6 --listing-schema housing_graph_word_v6` để đối chiếu đúng bản gốc.

Để khởi động đúng bản local đã cập nhật:

```powershell
docker compose -f docker-compose.yml -f docker-compose.override.yml -f docker-compose.ragas.yml -f docker-compose.legal-refresh.yml -f docker-compose.graph-rag.yml -f docker-compose.source-grounded.yml -f docker-compose.word-legal.yml -f docker-compose.ctu-ktx.yml up -d --no-deps --no-build api web
```

Image API `nckh-api:ctu-ktx-20261007` được tạo từ image đang phục vụ, cập nhật `topics.py` để ưu tiên KTX khi câu hỏi nêu rõ KTX/ký túc xá/kí túc xá và sửa bộ lọc điện/cư trú để không loại nhầm tài liệu KTX. Image web `nckh-web:ctu-ktx-20261007` được build từ mã giao diện. Dòng lưu ý nguồn Word và nhãn AI/model được gỡ khỏi phần hiển thị; trích dẫn và giới hạn nội dung vẫn có.

Build lại image từ thư mục gốc bằng `docker build -f scripts/Dockerfile.ctu-ktx -t nckh-api:ctu-ktx-20261007 .` và `docker build -t nckh-web:ctu-ktx-20261007 apps/web`. Dockerfile API cần image sao lưu đã có trên máy; nếu build toàn bộ API từ mã nguồn, các sửa KTX cũng nằm trực tiếp trong `topics.py` và `legal_retrieval.py`.

Để khôi phục bản trước, dùng cấu hình Compose trước khi thêm override KTX và image lưu `nckh-api:before-ctu-ktx-20261007`, `nckh-web:before-ctu-ktx-20261007`. Các kho gốc vẫn tồn tại.

Kiểm tra: TypeScript và production build đạt; 33 kiểm thử định tuyến/truy xuất đạt; 5 kiểm thử Playwright giao diện chat đạt. Sáu câu hỏi về Wi-Fi/gửi xe, phí ở, đăng ký, điện nước, hoàn phí và nấu ăn đều truy xuất nguồn KTX CTU; năm câu trả lời đầy đủ và câu điện nước trả lời một phần vì thiếu đơn giá chi tiết. `scripts/probe_ctu_ktx.py` kiểm tra bằng truy xuất, sinh và kiểm chứng thật; kết quả được lưu tại `eval/reports/ctu_ktx_answers_20261007.json`.

Câu hỏi điện nước đã lấy được đúng thông báo CTU: phòng nộp hàng tháng theo thực tế sử dụng. Nguồn chưa có đơn giá cụ thể mỗi kWh/m³ và cách chia phí trong phòng, nên câu trả lời giữ trạng thái một phần (`no_answer=true` trong API hiện có) cùng lời giải thích phần còn thiếu. Không coi trạng thái này là lỗi embedding, cũng không tự tạo đơn giá để chuyển thành câu trả lời đầy đủ. Chạy lại indexer với bản gốc chỉ bỏ qua tài liệu đã có: vẫn 4 tài liệu/52 vector, snapshot kho gốc không đổi.
