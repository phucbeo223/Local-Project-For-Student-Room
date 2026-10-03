# Kho pháp lý riêng và phân công agent — 03/10/2026

## Trạng thái

- Mã nguồn trước khi sửa đã được đẩy lên nhánh `codex/legal-ocr-retrieval` trong GitHub của chủ dự án, commit `f1c05e6`.
- Nhánh sửa hiện tại: `codex/legal-agent-rebuild`.
- Kho mới: schema PostgreSQL `legal_v2`, bảng tài liệu/chunk và sequence riêng. Embedding mới được tính bằng E5; không sao chép vector cũ.
- Hệ thống đang dùng kho `public` cho đến khi có kết quả đánh giá đủ để chuyển kho. Chưa xóa embedding cũ.

## Phân công

1. **Gemini phân tích câu hỏi**: tạo truy vấn tìm kiếm, nhận diện chủ đề và thông tin tình huống còn thiếu. Không tạo câu trả lời hoặc điều luật. Số điều/số tiền mới không có trong câu hỏi bị từ chối; lỗi API có dấu vết dự phòng.
2. **Bộ truy xuất**: dùng embedding E5, tìm kiếm từ khóa, xếp hạng và giữ đủ các chủ đề được hỏi. Truy vấn được giới hạn vào schema cấu hình. Gemini không ghi hay sửa luật trong kho.
3. **Qwen local**: khi bật agent, chọn ID các đoạn trả lời trong nguồn bằng JSON, không tự viết luật hoặc diễn giải lại số liệu. Hệ thống xác thực ID và chép đúng nguyên văn. Đây là chế độ `source_select`; Gemini không được đăng ký làm model tạo phản hồi cuối cùng.
4. **Kiểm tra căn cứ**: chế độ trích nguồn kiểm tra từng đoạn là chuỗi nguyên văn của đúng nguồn/rank, không phải suy luận về việc áp dụng luật. Ngữ cảnh thiếu hoặc yêu cầu chưa đủ nguồn vẫn được đánh dấu một phần. Chế độ diễn giải cũ có bộ đối chiếu Gemini và Qwen dự phòng; các lượt thử cho thấy cả model trả lời và model kiểm tra có thể diễn giải sai. Dấu vết phân biệt `exact_source_match` với kiểm tra LLM. Quyền gửi câu hỏi, câu trả lời và nguồn luật sang Gemini để kiểm tra/chấm đã được người dùng xác nhận trước đó.

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
- Báo cáo trên là lượt thử ba câu, không phải kết quả toàn bộ 36 câu. Lượt đủ 36 câu hiện tại dùng `eval/reports/legal_agent_after_v10_2026-10-03.json`.
- `eval/reports/legal_agent_after_final_2026-10-03.json`: giữ kết quả hai câu bị chặn ở lượt v2 để truy lỗi; không dùng làm báo cáo hoàn tất.
- Lượt v3 sửa bộ kiểm tra Qwen đọc thiếu danh sách giao dịch trong nguồn, ghép đủ điều về nội dung hợp đồng, và tránh coi hiệu lực của hợp đồng là hiệu lực thi hành văn bản. Lưu cả câu trả lời bị bác bỏ và lý do trong `provider_calls`.
- Lượt v3 vẫn bị Qwen kiểm tra nhầm nội dung có trong nguồn và tự suy ra năm luật từ tên tệp. Giữ lại `legal_agent_after_v3_2026-10-03.json` để truy lỗi. Lượt v4 bổ sung bộ đối chiếu Gemini riêng và cấm suy ra năm luật từ năm của bản hợp nhất.
- Lượt v4 phát hiện pool ứng viên bỏ mất khoản giá hợp đồng, bộ lọc nhầm khoản chung vì chứa điều kiện mua bán, và cách diễn giải 'chỉ' khi nguồn chưa loại trừ các căn cứ khác. Lượt v5 sửa ba lỗi này, buộc bộ đối chiếu kiểm tra nguồn riêng của từng câu khẳng định. Kết quả v4 được giữ ở `legal_agent_after_v4_2026-10-03.json`.
- V5 vẫn bị chặn nhiều do diễn giải sai; giữ checkpoint `legal_agent_after_v5_2026-10-03.json`. Thử bật suy luận trên một câu với giới hạn 2.400 token/300 giây bị `ReadTimeout`, không nhận được câu trả lời; không thể suy ra chất lượng đã cao hơn.
- V6 phân công Qwen tìm ID đoạn trả lời, hệ thống chép nguyên văn nguồn, bỏ suy luận pháp lý tự do trong chế độ agent. Lượt thử `legal_source_selection_smoke_2026-10-03.json` có 3 câu, 0 lỗi thực thi: câu 1 trích đủ danh mục, câu 2–3 vẫn đánh dấu một phần. Phản hồi dài hơn và ít diễn giải hơn; không dùng ba câu để kết luận toàn bộ bank tốt hơn.
- V6 dừng khi rà nguồn phát hiện Điều 24 khoản 3 Nghị định 106 bị gộp vào khoản 2 do ký tự OCR ở lề; câu cư trú thuê trọ chọn nhầm phạm vi ký túc xá. Giữ checkpoint v6 để truy lỗi. V7 sửa nhãn theo ảnh PDF gốc có ghi before/after tại `verified_ocr_corrections.json`, bổ sung Điều 27 Luật Cư trú từ bản gốc và giữ toàn bộ các điểm trong khoản khi chọn nguồn. Các phần chưa xem toàn văn vẫn có metadata giới hạn kiểm chứng.
- V7: 34 tài liệu, 1.221 đơn vị điều/khoản, 1.295 chunk/vector; 59 tài liệu/5.185 vector cũ, 1.130 tin phòng/915 vector tin phòng không đổi. Các gate truy xuất 36 câu, Điều 27, loại phạm vi ký túc xá khi hỏi phòng trọ và khóa cửa đúng khoản 3 đã đạt.
- V7 phát hiện câu 2 trích giá/thanh toán nhưng bỏ tiền cọc và vẫn báo đủ. V8 bổ sung nguồn đặt cọc trong truy xuất, kiểm tra ý tiền cọc đã hỏi nhưng không có trong đoạn chọn thì đánh dấu một phần, thêm gate SQL và test hồi quy. Checkpoint v7 được giữ để truy lỗi.
- V8 phát hiện ghi chú tuyển chọn nằm trong nội dung luật và lẫn phạm vi ký túc xá ở câu điện thuê trọ. V9 tách các ghi chú sang metadata, không đưa vào nội dung vector/trích dẫn; giữ đoạn hiệu lực/chuyển tiếp của cùng tài liệu khi Qwen chọn nội dung, đánh dấu bản tuyển một số điểm là không đủ toàn khoản, tách phụ lục khỏi điều luật. Checkpoint v8 được giữ để truy lỗi; không dùng làm lượt đủ 36 câu.
- V9: 34 tài liệu, 1.213 đơn vị điều/khoản, 1.287 chunk/vector có định danh và phần cha; kho cũ và vector tin phòng không đổi. Manifest `12cda786b35f6e99bf22c3e94ffda4ac139289d69496fecfdecbb3a9e80dc098`.
- V9 hoàn tất 36 phản hồi, không lỗi thực thi. Faithfulness 0,9202 chỉ có 30/36 điểm (6 lỗi chấm JSON); answer relevancy 0,6276 và context utilization 0,6273 có 36/36 điểm. Chưa đủ điều kiện chuyển vì trả lời thiếu tăng và relevancy giảm. Giữ riêng JSON, báo cáo so sánh và trạng thái v9.
- V10 sửa nhãn khoản 8 Thông tư 116 theo trang PDF gốc, giữ cả mốc hiệu lực ngắn và phạm vi mức phạt, ưu tiên cấu thành hành vi khi hỏi phân biệt lừa đảo, sửa nhận diện trích dẫn nhiều dòng. Qwen được thử chọn lại tối đa một lần khi bỏ một chủ đề hoặc tiền cọc đã hỏi và nguồn có sẵn; không tạo nội dung luật mới.
- V10: 34 tài liệu, 1.214 đơn vị điều/khoản, 1.288 chunk/vector/định danh/phần cha. Manifest `ba309b6ef424b0b15a703b019db3537002eabc6729090629e40a7aa3cf44052b`. Tất cả gate truy xuất 36 câu đạt; số liệu kho cũ và tin phòng không đổi. Chạy đánh giá v10 ngày 04/10 theo giờ Việt Nam, tên tệp giữ ngày bắt đầu công việc 03/10.
- Bộ test phần chatbot/pháp lý/agent: 112 test đạt; API và giao diện build thành công. Đây không phải kết quả toàn bộ các kiểm thử tích hợp của dự án.
- HTTP v9 thử với người dùng thường đã trả 200 và dùng `legal_v2`; tài khoản test đã xóa. JWT của runner phải đồng bộ API; thử người dùng thường không yêu cầu ngữ cảnh dành riêng cho admin. Lượt v10 phải kiểm tra HTTP riêng, không dùng kết quả v9 để xác nhận v10.
- `eval/reports/legal_agent_backup_2026-10-03.json`: bản dump 59 tài liệu/5.185 chunk cũ đã khôi phục vào database kiểm chứng riêng, đối chiếu nội dung tất cả dòng trùng nhau. Tệp dump lưu ở `backups/`, không đưa dữ liệu database lên GitHub.

Chỉ chuyển sau khi kiểm tra truy xuất đạt, các câu hỏi chạy thật, vai trò model đúng, kết quả được rà soát và có bản sao lưu khôi phục được. Chỉ xóa bảng/chunk/vector pháp lý cũ sau khi kho mới đã được kiểm chứng và ứng dụng thực tế dùng kho mới. Không xóa bản gốc hoặc vector tin phòng.

RAGAS đo faithfulness, answer relevancy và context utilization. Không có đáp án pháp lý chuẩn độc lập thì context recall và answer correctness phải ghi N/A. Trích dẫn đúng số rank không đồng nghĩa đúng pháp luật. So sánh trước/sau cần cùng model chấm và cấu hình, ghi cả phản hồi một phần/từ chối; lỗi chấm không được thay bằng điểm giả.

## Kiểm tra trước chuyển và thu hồi kho cũ

- `eval/validate_legal_agent_release.py` chỉ đọc dữ liệu và ghi báo cáo gate: đủ 36 phản hồi/điểm thật, cùng cấu hình chấm lịch sử, vai trò model, nguồn, review đúng hash phản hồi và backup đã khôi phục. Chính sách gate hiện giữ cả mức hoàn tất và ba metric không thấp hơn baseline; đây là tiêu chí kỹ thuật của lần sửa, không phải chứng nhận đúng luật.
- `eval/probe_legal_agent_http.py` kiểm tra HTTP có xác thực bằng tài khoản test tạm trong database. Không gửi email, không xuất token; tài khoản được xóa trong `finally`. API thử dùng cổng localhost 8001; API chính chỉ được chuyển sau gate.
- `scripts/retire_old_legal_corpus.py` không tự chạy cùng đánh giá. Chỉ thực thi xóa khi dùng `--apply`, API chính đã kiểm tra dùng `legal_v2`, release active đúng manifest, file đánh giá chưa đổi và backup còn đúng hash. Giao dịch xóa chỉ tác động dòng pháp lý `public.legal_documents`/`public.legal_chunks`, kiểm tra vector tin phòng trước/sau, giữ nguyên bảng, dữ liệu gốc và dump khôi phục.
- OCR mới lưu trong `eval/agent_source_ocr/`, không đưa cache dung lượng lớn vào Git. Để tái tạo: tải/xác thực manifest gốc → chạy script OCR → prepare corpus → index riêng → verify retrieval → đánh giá bank → review → gate → API thử/active → thu hồi có điều kiện. Không chạy indexer `public` cũ để thay thế quy trình này.
