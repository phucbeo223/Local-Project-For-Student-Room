# Datahouse làm kho chính và Graph RAG chỉ dùng nguồn có xuất xứ

Nhánh `codex/source-grounded-datahouse-20261004` tiếp tục từ bản Graph RAG đã đẩy lên GitHub cá nhân. Mục tiêu là cải thiện truy xuất và câu trả lời thực hành có nguồn; đáp án người dùng chỉ dùng để đối chiếu sau sinh, không trở thành tài liệu truy xuất hay câu trả lời cài sẵn.

## Dữ liệu đang dùng

Toàn bộ 1.130 phòng cũ ở `public.aggregated_listings` đã được thay bằng 789 bản ghi từ catalog Datahouse được cung cấp. Cả trang tìm phòng/bản đồ và chatbot lấy dữ liệu từ catalog này. Kho `housing_fresh_v4` được nhập vào schema rỗng và tạo lại toàn bộ 789 vector E5; `housing_graph_v4` và kho public nhận cùng bản ghi/vector đã kiểm chứng. Tọa độ, diện tích, tiện ích và thời gian thiếu được giữ là chưa biết. Không xác minh tin còn phòng hoặc giá quảng cáo là chính xác ngoài thực tế.

Bản dump local được khôi phục thử vào database kiểm chứng trước khi thay dữ liệu. Các liên kết với phòng cũ được xóa theo foreign key, gồm tương tác, nguồn phòng trong lịch sử chat, báo cáo và đánh giá phòng; tài khoản được giữ nguyên. Các schema `housing_v2`, `housing_graph_v1`, `graph_rag_v1`, `housing_graph_v2`, `graph_rag_v2` đã bị xóa sau HTTP smoke của phiên bản mới. Bản sao lưu giữ local để phục hồi. Crawler tự động tắt để không trộn dữ liệu cũ vào catalog. Tệp seed 1.000 phòng giả cũ được xóa khỏi nhánh; launcher không nạp seed khi khởi động bình thường. Tùy chọn -SeedDemoData chỉ dành cho bảng phòng rỗng, phải tạo lại fixture riêng, và bị chặn khi đã có catalog.

Kho pháp lý đang dùng `legal_v6_20261005` có 39 tài liệu, 1.207 đơn vị nguồn và 1.261 vector E5 mới. Kho này giữ nguyên byte 36 tài liệu v5 và bổ sung ba đoạn nguồn của đơn vị cấp nước. Không nạp 11 tài liệu hướng dẫn do dự án biên soạn. Các bản trích tuyển `legacy-*` được loại khỏi manifest; nguồn cần thiết được tách lại từ bản gốc PDF/DOC/DOCX và các đoạn HTML nguyên văn. Hai phần bản ký Bộ luật Dân sự giữ xuất xứ và số trang riêng; Điều 328 được lấy từ phần đầu, trang 86–87. Các bảng giá chép lại đã đối chiếu ảnh gốc có nhãn riêng về chuyển bố cục; không nhận toàn bộ câu chữ của bản chép bảng là nguyên văn máy trích xuất.

Nguồn bổ sung gồm [thông báo đăng ký KTX học kỳ 1 năm học 2026–2027](https://ssc.ctu.edu.vn/thong-bao/226-dang-ky-o-ky-tuc-xa-hoc-ky-1-nam-hoc-2026-2027.html), [hướng dẫn tân sinh viên CTU](https://tansinhvien.ctu.edu.vn/sinh-hoat/huong-dan-tan-sinh-vien-dang-ky-o-ky-tuc-xa), [nội quy KTX công bố bởi CTU](https://ssc.ctu.edu.vn/images/upload/Noiquy_KTX_trich_092025.pdf), [VBHN 17 về Bộ luật Tố tụng hình sự](https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-17-vbhn-vpqh-468961.htm) và đủ bốn phần [VBHN 135 về Bộ luật Hình sự](https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-135-vbhn-vpqh-46165/58894.htm).

Manifest và mỗi tài liệu giữ URL, mã băm bản gốc, tệp trang/đoạn nguồn, cách trích xuất và giới hạn OCR/hiệu lực. Các bản chép thủ công được giữ đúng nhãn đoạn đã đối chiếu ảnh PDF. Việc kiểm tra mã băm không thay thế kiểm chứng từng chữ OCR, lịch sử hiệu lực hay áp dụng vào trường hợp cá nhân. Thông báo KTX có thời hạn của từng đợt; không mặc định thời hạn đó vẫn đang mở.

Nguồn tra cứu nước gồm [hướng dẫn CANTHOWASSCO](https://ctn-cantho.com.vn/tin-khoa-hoc-cong-nghe/huong-dan-truy-cap-website-de-tra-cuu-va-tai-hoa-don-tien-nuoc-331.html), [cổng hóa đơn của công ty](https://hddt.ctn-cantho.com.vn/) và [FAQ Cấp nước Cần Thơ 2](https://capnuoccantho2.com.vn/View.aspx?wp=253). Mỗi trang chỉ có đoạn nguyên văn ngắn hoặc nhãn biểu mẫu trong corpus; HTML đầy đủ giữ local, không publish lên GitHub. Manifest ghi mã băm bản tải và đoạn công khai. Không truy vấn hóa đơn hay tài khoản khách hàng. Hướng dẫn của mỗi công ty có phạm vi riêng, không cung cấp căn cứ cho mức thu theo đầu người hoặc cách chia tiền giữa các phòng.

Đồ thị `graph_rag_v4` có 2.036 nút và 4.037 cạnh có trường bằng chứng. Vector/BM25 tạo seed, graph duyệt quan hệ địa điểm/tiện ích và tham chiếu cùng văn bản theo giới hạn hiện có. Phạm vi trang trích dẫn được mở rộng khi bổ sung một điều khoản ở trang khác. Các câu hỏi ghi nội dung hợp đồng và đặt cọc giữ đủ các khoản cùng điều trong giới hạn 5.500 ký tự, tránh làm mất giá thuê, thời hạn thanh toán hoặc điều kiện trả/mất cọc.

## Thay đổi phản hồi

Tìm phòng trên graph được render trực tiếp từ các trường nguồn; không gọi mô hình để viết lại giá, diện tích, tiện ích hay khoảng cách. Câu hỏi pháp lý giữ Qwen chọn bằng chứng, Gemini tổng hợp/kiểm chứng theo workflow pháp lý công khai hiện có, và fallback nguyên văn khi chưa xác nhận được tổng hợp.

Rerank ưu tiên điều khoản thực sự nêu phí dịch vụ và phương thức/thời hạn thanh toán khi người thuê hỏi giấy tờ môi giới. Kiểm tra trích dẫn phân biệt câu hỏi bổ sung dữ kiện và danh sách chủ đề nguồn chưa cung cấp với khẳng định nghĩa vụ, quyền hoặc số tiền; các khẳng định có thêm vẫn bị kiểm tra. Checklist có thể trình bày tối đa bảy ý có nguồn, giảm hỏi thêm dữ kiện cá nhân đối với câu hỏi quy tắc chung. Không thêm số tiền, thời hạn, nghĩa vụ hay nơi tiếp nhận chỉ để giống đáp án mẫu. Đối chiếu đáp án mẫu dùng Qwen cục bộ, kèm ngày snapshot và URL nguồn trong metadata. Ngày snapshot không xác minh hiệu lực. Nhãn chỉ đo khớp văn bản; các lỗi gán số liệu khi kiểm tra văn bản được ghi chú và nhãn thô được giữ nguyên. Prompt v2 khác lượt đối chiếu cũ, không dùng hai nhãn để suy ra mức tăng accuracy.

## Vận hành và chạy lại

Danh sách so sánh trong trình duyệt dùng khóa riêng theo mã băm catalog Datahouse; khóa cũ được xóa khi đọc danh sách để bỏ các ID phòng trước thay kho. Sau khi đổi kho, tải lại giao diện và bắt đầu cuộc trò chuyện mới để bỏ các ID phòng cũ. `.env` local đã trỏ tới pháp lý v6 và graph/phòng v4. Lớp compose mới giữ cấu hình và bật các agent cho cả API và evaluator; dữ liệu Datahouse, dump và báo cáo nhà trọ chi tiết được Git ignore. Nguồn CTU và các URL hướng dẫn/cổng cấp nước đã kiểm chứng có liên kết trên giao diện chat. Bộ lọc chất lượng dùng cặp ký tự thường–hoa thực sự để nhận chữ lỗi, tránh loại nhãn tiếng Việt viết hoa đúng.

```powershell
$sourceCompose = @('-p','nckh','-f','docker-compose.yml','-f','docker-compose.override.yml','-f','docker-compose.ragas.yml','-f','docker-compose.legal-refresh.yml','-f','docker-compose.graph-rag.yml','-f','docker-compose.source-grounded.yml')
docker compose @sourceCompose build ragas-eval
./scripts/fetch_source_grounded_originals.ps1
docker compose @sourceCompose run --rm --entrypoint python ragas-eval /workspace/scripts/prepare_source_grounded_corpus.py
docker compose @sourceCompose run --rm --entrypoint python ragas-eval /workspace/scripts/prepare_water_lookup_corpus.py
docker compose @sourceCompose run --rm --entrypoint python ragas-eval /workspace/scripts/import_housing_catalog.py --schema housing_fresh_v4 --catalog-dir /catalog/student-housing-789-Docker-INTERNAL/catalog --report /eval/reports/graph_rag_housing_fresh_v4_2026-10-04.json
docker compose @sourceCompose run --rm --entrypoint python ragas-eval /workspace/scripts/index_legal_agent_corpus.py --schema legal_v6_20261005 --corpus /workspace/docs/legal_corpus_v6_20261005 --report /eval/reports/graph_rag_legal_fresh_v6_2026-10-05.json
docker compose @sourceCompose run --rm --entrypoint python ragas-eval /workspace/scripts/index_graph_rag.py --source-schema housing_fresh_v4 --housing-schema housing_graph_v4 --graph-schema graph_rag_v4 --catalog-dir /catalog/student-housing-789-Docker-INTERNAL/catalog --report /eval/reports/graph_rag_index_v6_2026-10-05.json
docker compose @sourceCompose build api
docker compose @sourceCompose up -d --no-deps api
```

Các lệnh dựng lại corpus trên tạo bản nguồn mới khi tải thay đổi; không chạy lại chúng giữa lượt đánh giá đã bắt đầu. Khi nội dung/model/pipeline đổi, dùng schema hoặc output mới. Nguồn OCR đã có và các bản gốc cũ là đầu vào có mã băm; trên máy mới cần chuẩn bị chúng theo các script thu thập/trích xuất của dự án. Gói Datahouse không được đưa lên GitHub.

`promote_datahouse_primary.py` yêu cầu bản dump đã khôi phục và đối chiếu trước khi xóa kho public. Chỉ dùng thao tác promote khi muốn thay toàn bộ phòng cũ và các liên kết phụ thuộc; thao tác retire yêu cầu HTTP smoke mới đã qua. Không chạy lại promote sau khi người dùng đã có tương tác mới với catalog.

## Kiểm thử

121 kiểm tra chatbot/pháp lý/graph/xử lý tài liệu/nguồn đã qua; API/frontend build, kiểm tra kiểu/lint frontend và HTTP có xác thực đã qua. Trang chính, chat, so sánh và bản đồ trả HTTP 200. HTTP hỏi tiếp phòng giữ đúng ID và namespace; tài khoản thử được xóa. Mã băm pipeline bao gồm cả chatbot và legal_knowledge, tránh bỏ sót thay đổi xử lý nguồn. Tệp nguồn và manifest được giữ nguyên byte trong Git; mỗi tài liệu v5 được sao chép nguyên byte sang v6 trước khi thêm nguồn mới.

Đợt chính thức chạy câu 1–56 của bộ lưu 58 câu; chạy thêm 57–58 để đối chiếu đủ 36 đáp án. Thống kê 56 câu được tách khỏi hai câu bổ sung. Câu 15 sau 14; 16 sau 14,15; 17–18 độc lập sau 14. Kết quả và context được lưu từng câu cùng mã băm pipeline/corpus, không trộn kết quả của phiên bản trước.

Lượt cuối v15 hoàn thành 58/58 câu, lỗi thực thi 0; phần chính 56/56 câu có 51 câu có context, 24 phản hồi một phần và 5 câu tìm phòng không có kết quả. Cờ `no_answer` tổng cộng 29 bao gồm cả 24 phản hồi một phần, không phải 29 câu trống. Tìm phòng có kết quả 13/18 câu, vi phạm bộ lọc 0; câu 7 và 12 có bản ghi khớp bộ lọc danh nghĩa nhưng thiếu bằng chứng cho yêu cầu đi lại/sức chứa. Toàn bộ 4 câu KTX có nguồn CTU; câu 41–42 vẫn một phần. Đối chiếu nguyên hàng kho public sau test không phát hiện thay đổi. Câu 30 dùng đúng ba nguồn cấp nước mới để trả lời tra cứu, có cảnh báo phạm vi công ty; không chuyển trọng tâm sang khiếu nại. Câu 43 không còn cờ một phần; câu 57 bổ sung còn một phần và không tính vào 56 câu chính.

Có graph trace ở 53/56 câu và không có lệnh gọi cloud cho dữ liệu nhà trọ. Trung vị lượt cuối 37,38 giây, p95 74,98 giây; đây là quan sát trên máy local có tài nguyên dùng chung, không phải benchmark tài nguyên cô lập. Provider của 56 câu: template 13, structured 5, Gemini-agent 33, Qwen-local 5. Cờ degraded ở 37 câu gồm các phản hồi có giới hạn/fallback, không đồng nghĩa 37 lỗi thực thi. Đối chiếu cơ sở v12 đủ 36 đáp án: high 1, partial 27, low 8. Lượt cuối v15 được sinh và chấm lại từ đầu, không ghép kết quả cơ sở vào báo cáo mới. Đây là hồi quy trên chủ đề đã biết; không phải kiểm thử mù hay tỷ lệ chính xác pháp lý đã được xác minh.

Các lệnh đánh giá dùng những output riêng cho phiên bản cuối, chạy tuần tự để Qwen không bị tranh tài nguyên:

```powershell
docker compose @sourceCompose run --rm --no-deps --entrypoint python ragas-eval /eval/graph_rag_question_bank.py --ids (1..58) --output /eval/reports/graph_rag_grounded_all58_v15_2026-10-05.json
docker compose @sourceCompose run --rm --no-deps --entrypoint python ragas-eval /eval/select_graph_rag_run.py --run /eval/reports/graph_rag_grounded_all58_v15_2026-10-05.json --output /eval/reports/graph_rag_grounded_56_v15_2026-10-05.json
docker compose @sourceCompose run --rm --no-deps --entrypoint python ragas-eval /eval/audit_graph_rag.py --run /eval/reports/graph_rag_grounded_56_v15_2026-10-05.json --index /eval/reports/graph_rag_index_v6_2026-10-05.json --primary-release /eval/reports/graph_rag_primary_v4_2026-10-04.json --output /eval/reports/graph_rag_audit_v15_2026-10-05.json
docker compose @sourceCompose run --rm --no-deps --entrypoint python ragas-eval /eval/compare_graph_legal.py --run /eval/reports/graph_rag_grounded_all58_v15_2026-10-05.json --output /eval/reports/graph_rag_vs_reference_36_v15_2026-10-05.json
```

`graph_rag_primary_v4_2026-10-04.json` giữ bằng chứng thao tác thay kho public ban đầu, đồng thời ghi schema đang hoạt động v6/v4. Đây là báo cáo private có sẵn trên máy làm việc; trên database khác phải tạo báo cáo verify/promote của database đó, không sao chép cờ kiểm chứng từ máy này. Lượt chạy dở trước khi sửa OCR/truy xuất không được tính vào kết quả cuối.
