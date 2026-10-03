# Kho pháp lý riêng và phân công agent — 03/10/2026

## Trạng thái

- Mã nguồn trước khi sửa đã được đẩy lên nhánh `codex/legal-ocr-retrieval` trong GitHub của chủ dự án, commit `f1c05e6`.
- Nhánh sửa hiện tại: `codex/legal-agent-rebuild`.
- Kho mới: schema PostgreSQL `legal_v2`, bảng tài liệu/chunk và sequence riêng. Embedding mới được tính bằng E5; không sao chép vector cũ.
- Hệ thống đang dùng kho `public` cho đến khi có kết quả đánh giá đủ để chuyển kho. Chưa xóa embedding cũ.

## Phân công

1. **Gemini phân tích câu hỏi**: tạo truy vấn tìm kiếm, nhận diện chủ đề và thông tin tình huống còn thiếu. Không tạo câu trả lời hoặc điều luật. Số điều/số tiền mới không có trong câu hỏi bị từ chối; lỗi API có dấu vết dự phòng.
2. **Bộ truy xuất**: dùng embedding E5, tìm kiếm từ khóa, xếp hạng và giữ đủ các chủ đề được hỏi. Truy vấn được giới hạn vào schema cấu hình. Gemini không ghi hay sửa luật trong kho.
3. **Qwen local**: tạo câu trả lời từ các đoạn truy xuất. Gemini không được đăng ký làm model trả lời khi bật agent.
4. **Kiểm tra căn cứ**: Gemini đối chiếu từng kết luận với nguồn, kết hợp kiểm tra bằng quy tắc về số điều, số liệu, chủ thể, điều kiện, ngoại lệ. Khi Gemini lỗi, Qwen kiểm tra dự phòng và ghi trạng thái suy giảm. Phản hồi thiếu căn cứ được sửa, đánh dấu một phần hoặc từ chối. Dấu vết ghi model đã thử, model kiểm tra và model tạo phản hồi cuối cùng. Quyền gửi câu hỏi, câu trả lời và nguồn luật sang Gemini để kiểm tra/chấm đã được người dùng xác nhận trước đó.

Đây là quy trình phối hợp agent trong ứng dụng. Truy xuất hiện vẫn dùng hybrid; chưa chuyển sang GraphRAG.

## Cấu trúc nguồn

- `docs/legal_agent_originals_20261003/`: bản gốc tải từ Cổng Chính phủ và Bộ Công an, manifest URL và SHA-256.
- `docs/legal_corpus_v2/`: bản trích có cấu trúc, mỗi tài liệu có nguồn gốc và mỗi khoản có Điều/Khoản, đầy đủ điểm, ngoại lệ, dẫn chiếu, vị trí và hash nội dung.
- Giữ toàn bộ khoản làm phần cha; vector dùng đoạn ngắn. Khi truy xuất một khoản dài vượt giới hạn ngữ cảnh, đánh dấu `context_complete=false`, không coi đoạn trích là khoản đầy đủ.
- Phần giới thiệu quy phạm trước các khoản được giữ riêng trong `article_context`; phần này đi cùng khoản khi cung cấp ngữ cảnh.
- Trang PDF là trang vật lý trong tệp gốc. DOCX/DOC/Markdown chỉ có vị trí trang logic, không được diễn giải thành trang bản PDF gốc.
- `source_start`/`source_end` là vị trí ký tự trong phần trích đã chuẩn hóa, không phải byte của bản gốc. Sổ nguồn chi tiết: `docs/LEGAL_CORPUS_V2_SOURCES.md`.
- Bản tóm tắt biên tập, ghi chú ngữ cảnh và tài liệu KTX được loại khỏi phần điều luật mới. Nguyên bản và dữ liệu cũ vẫn được lưu.

## Những lỗi nguồn đã phát hiện

### Thu tiền điện cao hơn quy định

Bản diễn giải cũ của Nghị định 133/2026 dẫn sai Điều 8 khoản 5. Bản PDF chính phủ ghi hành vi người cho thuê nhà thu tiền điện của người thuê cao hơn quy định tại **Điều 13 khoản 7**, trang PDF 16. Biện pháp hoàn trả liên quan ở **Điều 13 khoản 11 điểm c**, trang PDF 17. Đã xem ảnh hai trang để đối chiếu. Không gộp biện pháp của các điểm khác vào hành vi này.

Nguồn: https://vanban.chinhphu.vn/?docid=217612&pageid=27160

### Giấy tờ chỗ ở hợp pháp khi tạm trú

Giữ riêng Nghị định 154/2024 và văn bản sửa đổi 58/2026. Điều 4 khoản 2 của Nghị định 58 sửa điểm a khoản 3 Điều 5 của Nghị định 154. Đã xem trang PDF 26 của văn bản sửa đổi và trang 5 của văn bản gốc. Không gọi bản trích tự cấu trúc là bản hợp nhất do cơ quan nhà nước ban hành.

### Chuyển phòng và thông tin hợp đồng

Kiểm tra truy xuất ban đầu thiếu quy định trực tiếp về đăng ký tạm trú mới khi đổi chỗ ở và thiếu phần thông tin các bên tại Điều 163. Đã thêm từ tìm kiếm và ưu tiên phù hợp với nội dung hỏi; kiểm tra lại trên SQL thật.

### Nước

Quyết định 215/QĐ-UBND năm 2024 chưa có bản gốc từ máy chủ chính quyền được xác thực trong lần sửa này, nên chưa đưa vào kho mới. Nghị định 117/2007, bản sửa đổi 124/2011 và bản hợp nhất hướng dẫn 57/VBHN-BXD đã được tải từ Cổng Chính phủ. Chỉ nạp các điều đã tách được về hợp đồng cấp nước, đo đếm, thanh toán, thẩm quyền và trách nhiệm. Chưa khẳng định biểu giá hiện tại của Cần Thơ. Hợp đồng cấp nước và hợp đồng thuê trọ có các chủ thể khác nhau, không tự suy ra công thức chia tiền nước theo đầu người.

## Giới hạn cần ghi nhận

Bản gốc do cơ quan nhà nước công bố có thể đối chiếu qua URL và hash. Bản OCR/trích tuyển do hệ thống tạo **không phải tài liệu được Chính phủ phê duyệt riêng**. Các lỗi OCR không được sửa số liệu bằng phỏng đoán. Những trang đã đối chiếu trực quan được ghi rõ; các phần khác, đặc biệt bản trích kế thừa, chưa được xác nhận từng chữ với toàn văn gốc. Metadata xác định phạm vi và lịch sử không thay thế căn cứ hiệu lực.

## Kiểm thử và điều kiện chuyển kho

Các báo cáo độc lập:

- `eval/reports/legal_agent_index_2026-10-03.json`: kiểm tra kho cũ và tin phòng không đổi trong lần nạp, số chunk/vector mới.
- `eval/reports/legal_agent_retrieval_2026-10-03.json`: truy xuất 36 câu thật và các kiểm tra ngoại lệ, hồ sơ, thông tin hợp đồng, chuyển phòng.
- `eval/reports/legal_agent_probe_2026-10-03.json`: kiểm tra Gemini phân tích và danh sách model trả lời thực tế.
- `eval/reports/legal_agent_after_2026-10-03.json`: câu trả lời mới, nguồn, dấu vết agent và RAGAS.
- Báo cáo trên là lượt thử ba câu, không phải kết quả toàn bộ 36 câu. Lượt đủ 36 câu hiện tại dùng `eval/reports/legal_agent_after_v4_2026-10-03.json`.
- `eval/reports/legal_agent_after_final_2026-10-03.json`: giữ kết quả hai câu bị chặn ở lượt v2 để truy lỗi; không dùng làm báo cáo hoàn tất.
- Lượt v3 sửa bộ kiểm tra Qwen đọc thiếu danh sách giao dịch trong nguồn, ghép đủ điều về nội dung hợp đồng, và tránh coi hiệu lực của hợp đồng là hiệu lực thi hành văn bản. Lưu cả câu trả lời bị bác bỏ và lý do trong `provider_calls`.
- Lượt v3 vẫn bị Qwen kiểm tra nhầm nội dung có trong nguồn và tự suy ra năm luật từ tên tệp. Giữ lại `legal_agent_after_v3_2026-10-03.json` để truy lỗi. Lượt v4 bổ sung bộ đối chiếu Gemini riêng và cấm suy ra năm luật từ năm của bản hợp nhất.
- `eval/reports/legal_agent_backup_2026-10-03.json`: bản dump 59 tài liệu/5.185 chunk cũ đã khôi phục vào database kiểm chứng riêng, đối chiếu nội dung tất cả dòng trùng nhau. Tệp dump lưu ở `backups/`, không đưa dữ liệu database lên GitHub.

Chỉ chuyển sau khi kiểm tra truy xuất đạt, các câu hỏi chạy thật, vai trò model đúng, kết quả được rà soát và có bản sao lưu khôi phục được. Chỉ xóa bảng/chunk/vector pháp lý cũ sau khi kho mới đã được kiểm chứng và ứng dụng thực tế dùng kho mới. Không xóa bản gốc hoặc vector tin phòng.

RAGAS đo faithfulness, answer relevancy và context utilization. Không có đáp án pháp lý chuẩn độc lập thì context recall và answer correctness phải ghi N/A. Trích dẫn đúng số rank không đồng nghĩa đúng pháp luật. So sánh trước/sau cần cùng model chấm và cấu hình, ghi cả phản hồi một phần/từ chối; lỗi chấm không được thay bằng điểm giả.
