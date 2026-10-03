# Sửa năm nhóm lỗi pháp lý — 04/10/2026

Lượt cuối đang dùng mã v15 và manifest `db830c71bd0d4c9eed5ed5980f9538a43283bf66d671f917afacf94d953f28da`. V11 dừng sau 9 phản hồi để sửa OCR hợp đồng dịch vụ. V12 dừng khi phản hồi API không chấp nhận kiểu nguồn web. V13 chạy đủ 36 câu, 0 lỗi thực thi nhưng câu 34/36 còn chọn thủ tục nội bộ cơ quan thay cho bằng chứng nạn nhân; đã sửa ở v14. V14 dừng để sửa URL Nghị định 282 bị gắn nhầm Nghị định 347; lượt cuối v15 sử dụng manifest mới. Giữ nguyên các báo cáo thử, không ghép vào lượt cuối. Kho `public` và API chính chưa chuyển.

## 1. Giữ ý câu hỏi gốc

- Dành vị trí truy xuất riêng cho tiền cọc, tiền thuê, thanh toán được hỏi; ưu tiên này sử dụng câu gốc dù Gemini mở rộng truy vấn khác.
- Câu 2: **Hợp đồng thuê phòng có cần ghi rõ tiền cọc, tiền thuê và ngày thanh toán không?** Truy xuất và phản hồi local có Điều 328 khoản 1, Điều 163 khoản 3 và khoản 4. Không suy ra đặt cọc là bắt buộc chỉ từ định nghĩa đặt cọc.
- Qwen chọn thiếu ý sẽ được yêu cầu chọn lại tối đa một lần; nếu vẫn thiếu, báo phần chưa đủ căn cứ.

## 2. Đơn vị điều/khoản và dẫn chiếu

- Ghép hiệu lực/chuyển tiếp theo `provision_id` và phần cha đầy đủ. Không lấy mảnh giữa danh mục bãi bỏ làm căn cứ hiệu lực; không cắt nửa khoản để vừa ngân sách ngữ cảnh.
- Nhận dạng `3.[74]` là khoản 3, giữ chú thích nguyên văn, không gộp vào khoản 2.
- Giữ quy tắc và ngoại lệ dẫn chiếu cùng văn bản khi có đủ nguồn/ngữ cảnh. Dẫn chiếu sang Luật Bảo vệ dữ liệu cá nhân được gắn nguồn và rank riêng, không đặt văn bản luật dưới trích dẫn của nghị định.

## 3. Đúng chủ thể và loại hình

- Phí khách hàng trả môi giới: bổ sung Điều 513–519 Bộ luật Dân sự về hợp đồng dịch vụ, không sử dụng thù lao cá nhân môi giới nhận từ doanh nghiệp để thay thế. Không đặt ra mức phí bắt buộc.
- Nhà trọ nhiều phòng: giữ toàn Điều 20/21 Luật PCCC và các mục phân loại phụ lục I Nghị định 105. Cần biết loại sử dụng, tầng, diện tích; không tự coi mọi nhà nhiều phòng cùng một nhóm.
- Người trình báo/nạn nhân: dành nguồn khuyến cáo Công an lưu tin nhắn, chứng từ chuyển tiền, lịch sử giao dịch; ưu tiên Điều 146 khoản 1 và Điều 145 khoản 2 về tiếp nhận. Không dùng thông báo nội bộ gửi Viện kiểm sát hay kiến nghị khởi tố của cơ quan nhà nước thay câu hỏi của cá nhân.
- Nền tảng đăng tin: phân biệt nền tảng trung gian và chức năng đặt hàng. Trích đúng tên văn bản không đủ để khẳng định quan hệ pháp lý phù hợp.

## 4. Nguồn bổ sung, kiểm chứng và giới hạn

Sổ nguồn: [LEGAL_CORPUS_V2_SOURCES.md](LEGAL_CORPUS_V2_SOURCES.md). URL, ngày tải và SHA bản gốc: [download_manifest.json](legal_fix_originals_20261004/download_manifest.json), [guidance_manifest.json](legal_fix_originals_20261004/guidance_manifest.json).

| Nguồn | Đã nạp | Giới hạn |
|---|---|---|
| Luật 91/2025/QH15, Nghị định 356/2025/NĐ-CP từ Công báo Chính phủ | Điều khoản quy phạm, quyền và thủ tục, ngoại lệ dẫn chiếu | Không coi chữ trong OCR chưa rà toàn bộ là đã được chứng nhận |
| Thông tư 60/2025/TT-BCT từ Công báo | Điều 1–4, 12, 20, 21, cả điều kiện hiệu lực và chuyển tiếp | Chưa xác minh chắc chắn sự kiện điều chỉnh giá kích hoạt mốc hiệu lực có điều kiện; phản hồi phải nêu thiếu này |
| Quyết định 50/2026/QĐ-UBND từ cổng Sở Tư pháp Cần Thơ | Phân công/quản lý hoạt động cấp nước | Không phải bảng giá mới thay Quyết định 215 |
| Quyết định 215/QĐ-UBND ngày 01/02/2024, bản ký do đơn vị cấp nước công khai | Căn cứ phạm vi, khoản 2 Điều 2, Điều 3 | Số hiệu/ngày/tên đối chiếu kết quả công khai cổng Cần Thơ; đường dẫn đối chiếu trực tiếp trả HTTP 404 (ghi trong hồ sơ, không giả là tải thành công); chưa khẳng định phạm vi áp dụng hiện nay trên địa bàn sau sắp xếp hoặc giá hóa đơn cụ thể |
| Hướng dẫn công khai cách tính tiền điện nhà trọ Cần Thơ, 21/09/2026 | Hai đoạn HTML đầy đủ có cách tính/chỉ số/hóa đơn | Là hướng dẫn thực tế được cổng Cần Thơ công bố, không gọi là điều luật xác lập nghĩa vụ thông báo bắt buộc cho mọi chủ trọ |
| Bộ luật Dân sự từ PDF Chính phủ | Điều 513–519, phiên âm kiểm tra từng chữ trên trang PDF 34–35 | Căn cứ hợp đồng dịch vụ chung; không chứng minh mọi người giới thiệu phòng đều có quyền thu phí |

Đối chiếu ảnh: Quyết định 215 trang 1/3 và tiêu đề Điều 2 tại trang 2; BLDS trang vật lý 34/35 (trang in 128/129). Hai bản trích thủ công gắn SHA PDF gốc: `water215_verified_extract.json`, `civil_service_verified_extract.json`. Bảng tiền và tỷ lệ điều chỉnh số trong Quyết định 215 không nạp vào kết luận mức thu. Phần 520/521 chưa rà từng chữ được bỏ khỏi bản trích dịch vụ; PDF gốc vẫn giữ.

Hướng dẫn Hà Nội đã tải để lưu dấu vết nhưng loại khỏi kho Cần Thơ vì khác địa bàn. Quy định hợp đồng/đồng hồ giữa đơn vị cấp nước và khách hàng không tự xác lập cách chủ trọ phân chia tiền cho nhiều người thuê; câu 10/11 cần rà đúng quan hệ và giữ trả lời một phần khi chưa có căn cứ trực tiếp. Nghĩa vụ riêng của chủ trọ cung cấp toàn bộ giấy tờ tạm trú vẫn chưa được xác nhận đầy đủ; không đổi nghĩa vụ của công dân/cơ quan tiếp nhận thành nghĩa vụ của chủ trọ. Không suy ra một sự kiện chưa xảy ra chỉ vì chưa tìm thấy trên công cụ tìm kiếm.

URL Nghị định 282 đã sửa về trang Chính phủ có số ký hiệu 282/2025/NĐ-CP, bản PDF ký giữ trong `residence282.pdf`; `source_url_corrections.json` ghi cả URL cũ, URL mới, lý do, ngày tải và SHA. Nghị định 347 sửa đổi vẫn là nguồn riêng. Bản trích kế thừa chưa được xác nhận từng chữ với PDF 96 trang này.

Tài liệu tải từ nguồn công bố minh bạch không làm bản trích của dự án trở thành bản hợp nhất được Chính phủ phê duyệt. Không dùng Gemini/Qwen tạo chữ luật còn thiếu.

## 5. Chạy lại và ghi điểm

- Truy xuất SQL/vector thật: 36 câu, **35/35 gate đạt**; báo cáo `eval/reports/legal_agent_retrieval_v15_2026-10-04.json` áp dụng mã v15 và manifest cuối.
- Hồi quy phần pháp lý/agent/quota/schema: **104 test đạt trên mã agent không đổi**, `legal_agent_tests_v14_2026-10-04.xml`. API và giao diện build thành công. HTTP v13 câu 8 đã kiểm tra nguồn web có xác thực; v14 kiểm tra lại câu 36 với nguồn cho người trình báo ở `legal_agent_http_v14_2026-10-04.json`.
- Kho manifest: **39 tài liệu, 1.507 đơn vị**. DB có 1.782 chunk/vector với định danh và phần cha: 1.585 thuộc 39 tài liệu hoạt động, 197 thuộc 3 tài liệu kế thừa đã ngừng truy xuất. Các nguồn bị thay được đánh dấu không hoạt động, không coi đây là bãi bỏ văn bản pháp luật. Báo cáo index giữ số liệu `public` trước/sau: 59 tài liệu, 5.185 chunk/vector; 1.130 tin phòng và 915 vector tin phòng không đổi.
- Local hoàn tất: **36/36 phản hồi, 0 lỗi thực thi, 23 phản hồi một phần**; mọi trích đoạn khớp context/rank ở 36/36 câu. Qwen được gọi ở đủ 36 câu; phân tích rules ở đủ 36 do container local tắt key. Hai câu 34/36 đã chọn đúng hướng dẫn bằng chứng. Đây chưa phải kiểm định đúng pháp luật hay điểm native tăng.
- Rà nguồn local: `legal_agent_local_review_v15_2026-10-04.json`. Câu 21 còn chọn đoạn giá dịch vụ chưa đáp ứng câu hỏi công khai thông tin; câu 24 còn thiếu phần hình thức giấy tờ; câu 10/11 cần phân biệt quan hệ cấp nước và thuê phòng. Ghi lỗi còn lại để rà/xử lý khi chạy native; chưa nghiệm thu toàn bộ câu trả lời.
- Local: `legal_agent_local_v15_2026-10-04.json`, Qwen trả lời, phân tích chủ đề bằng rules khi tắt key trong container thử. Không dùng lượt này thay lượt Gemini hoặc điền điểm RAGAS Gemini.
- Lượt chính: `legal_agent_after_v15_2026-10-04.json`, Gemini phân tích, Qwen chọn nguồn; RAGAS 0.3.9, Gemini 3.1 Flash Lite, 8.192 output token, 4 worker, E5, strictness 1, temperature 0, giữ đủ ngữ cảnh và chấm cả phản hồi thiếu căn cứ. Cùng phương pháp với baseline ngày 02/10.
- Chỉ so điểm có ở cả hai lượt với cùng judge/phương pháp. Chưa có đáp án pháp lý chuẩn độc lập: Answer Correctness/Context Recall vẫn N/A. Trích nguyên văn khớp nguồn không đồng nghĩa đúng áp dụng pháp luật.

## HTTP 429 và tiếp tục

429 thực tế ở lượt v11 là quota **theo ngày/dự án/model**, giá trị 500. Đã lưu checkpoint, không tạo câu trả lời/điểm 0 do quota. V12/v13/v14/v15 kế thừa mốc chờ này bằng checkpoint trống có ghi SHA báo cáo trước, không sao chép phản hồi hay điểm và không gọi thêm Gemini trước mốc thử lại.

Mốc thử lại đang lưu: `2026-10-04T07:00:05Z`, tương ứng **14:00:05 ngày 04/10 giờ Việt Nam**. Đây là mốc kiểm tra, không bảo đảm server đã có hạn mức. Worker thử một yêu cầu nhỏ sau mốc này; nếu còn 429, tính mốc chờ mới từ phản hồi và giữ checkpoint. Không xoay key để vượt quota dự án.

`resume_legal_evaluation.py` khóa một writer, chạy tuần tự các câu; chấm tối đa 4 metric đồng thời, dừng cấp việc mới khi 429 và lưu kết quả hợp lệ đang hoàn tất. Đợi theo Retry-After/RetryInfo; quota ngày đợi đầu ngày Pacific, rồi kiểm tra server. Worker giới hạn 48 giờ; nếu máy/Docker dừng hoặc hết thời gian, checkpoint vẫn giữ để tiếp tục. Máy và Docker cần hoạt động để worker chạy.

Container cuối: `nckh-legal-local-eval-v15`, `nckh-legal-agents-eval-v15`. Heartbeat theo dõi trong chat này mỗi giờ, giữ im lặng khi chạy/chờ bình thường; thông báo khi có kết quả hoặc lỗi cần xử lý. API thử v14 ở localhost:8002, API chính chưa chuyển. Kho cũ chỉ được thu hồi sau khi đủ điểm, rà nguồn, gate chuyển và backup khôi phục đạt.

Báo cáo tiến độ/kết quả: `eval/ragas_reports/legal_fixes_2026-10-04.md`, tạo lại bằng `eval/report_legal_fixes.py`. Đọc số phản hồi/điểm hiện có trong báo cáo thay vì coi việc sửa code hay gate truy xuất đạt là chất lượng trả lời đã tăng.
