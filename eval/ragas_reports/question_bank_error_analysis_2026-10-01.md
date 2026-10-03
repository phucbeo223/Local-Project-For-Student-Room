# Phân tích lỗi bộ 58 câu hỏi CTU — 01/10/2026

## 1. “Không đúng nguồn” thực sự có nghĩa gì?

Báo cáo trước dùng cách gọi quá mạnh. Trường `category_source_match` chỉ kiểm tra: **có ít nhất một phần tử trong `sources` mang `category` giống nhãn thư mục dự kiến của câu hỏi hay không**. Nó không đọc nội dung để xác minh từng kết luận trong câu trả lời.

- `false` có thể do lấy tin phòng, không lấy được nguồn nào, lấy tài liệu lệch chủ đề, hoặc lấy tài liệu liên quan nhưng thuộc một chủ đề khác.
- `true` chỉ cần một nguồn cùng nhãn; những nguồn còn lại và câu trả lời vẫn có thể thiếu căn cứ.
- 14/40 là tỷ lệ có nguồn **cùng nhãn**, không phải tỷ lệ trả lời đúng 35%.
- Các câu 1–18 không được kiểm tra bằng tiêu chí nhãn thư mục này. Lỗi của chúng phải kiểm tra riêng theo giá, vị trí, diện tích và lịch sử hội thoại.

Ví dụ: câu 51 hỏi thông tin cá nhân để đăng ký cư trú, nên nguồn `residence` có thể liên quan dù nhãn dự kiến là `privacy_data`. Câu 55 hỏi dấu hiệu rủi ro trước khi đặt cọc; tài liệu hợp đồng hoặc nền tảng đăng tin cũng có thể liên quan dù câu nằm trong nhóm `criminal_law`. Khác thư mục không đủ để kết luận nguồn sai. Cả hai câu vẫn cần kiểm tra phạm vi áp dụng và mức đầy đủ của câu trả lời.

## 2. Kết quả đối chiếu

Phân tích dựa trên JSON của lần kiểm thử thật, audit chỉ mục, nội dung các DOCX hiện có và mã nguồn hiện hành. Đã chạy lại bộ phân loại cho cả 58 câu, cùng phép viết lại câu 15–16, không gọi LLM và không sửa DB. Kết quả phân loại hiện tại khớp kết quả lưu cho 58/58 câu. Vì vậy lỗi định tuyến có thể tái hiện độc lập với mô hình sinh câu trả lời.

| Phân loại cảnh báo | Số câu | Câu |
|---|---:|---|
| Câu hỏi chủ đề bị đưa sang tìm phòng | 16 | 29, 36, 37, 38, 39, 43, 44, 45, 47, 48, 49, 52, 53, 54, 56, 58 |
| Câu hỏi chủ đề bị hỏi lại giá/khu vực | 3 | 40, 42, 50 |
| Đã vào kho tài liệu, thiếu nguồn chính hoặc lệch nội dung | 5 | 19, 28, 31, 41, 57 |
| Đã vào kho tài liệu, có nguồn liên chủ đề cần đánh giá nội dung | 2 | 51, 55 |
| Tổng cảnh báo nhãn nguồn | 26 | Không đồng nghĩa 26 câu đã được kiểm định là sai pháp lý |

Trong 40 câu theo chủ đề, chỉ 21 câu đi vào kho tài liệu; 19 câu còn lại đi vào tìm phòng hoặc hỏi lại thông tin tìm phòng. Ngoài ra câu 17 thuộc nhóm tìm phòng lại bị chuyển sang hỏi pháp lý.

## 3. Lỗi cần sửa trong hệ thống

### P0 — Phân loại câu hỏi sai, lấy nhầm loại dữ liệu

**Bằng chứng:** Câu 37 hỏi lối thoát nạn bị khóa nhưng chatbot gợi ý phòng có thang thoát hiểm. Câu 52 hỏi cách lưu ảnh căn cước nhưng chatbot liệt kê phòng và giá thuê. Câu 56 hỏi chứng cứ sau khi đã chuyển cọc cho tin giả nhưng phần đầu câu trả lời vẫn gợi ý phòng. Đây là lỗi chọn tác vụ trước khi tìm kiếm, không phải thiếu embedding.

**Nguyên nhân đã xác minh trong `parser.py`:**

- `legal_terms` chủ yếu phủ hợp đồng, cư trú và điện/nước; chưa phủ đủ ký túc xá, môi giới, dữ liệu cá nhân, cháy nổ, thoát nạn, tin giả, chuyển/nhận cọc và trình báo.
- Khớp bằng `term in text`, không xét ranh giới từ. Câu 54 có “cá nhân”, chuỗi `nhan` chứa `nha`, nên bị coi là hỏi nhà ở rồi chuyển sang tìm phòng.
- Chuỗi `dieu ` nhận cả “điều kiện”. Câu 17 hỏi nới lỏng điều kiện tìm phòng nhưng bị coi là câu hỏi pháp lý.
- Không có tác vụ riêng cho hỏi thông tin ký túc xá hoặc hướng dẫn sử dụng nền tảng. Các câu này cần kho kiến thức nhưng không nhất thiết là câu hỏi về luật.

**Cách khắc phục:** Phân biệt tìm/so sánh phòng với hỏi kiến thức, quyền lợi, an toàn và hướng dẫn nền tảng. Khớp từ/cụm từ có ranh giới; chỉ nhận “Điều” là viện dẫn luật khi có cấu trúc phù hợp, chẳng hạn “Điều 12”. Bổ sung ví dụ tiếng Việt cho đủ 10 nhóm, dùng bộ phân loại tác vụ cho trường hợp mơ hồ. Sau khi đã xác định hỏi kiến thức, không dùng mẫu hỏi lại ngân sách/khu vực hoặc gợi ý phòng để thay cho câu trả lời.

**Điều kiện nghiệm thu:** 19 câu chủ đề nêu trên phải đi vào kho kiến thức; câu 17 phải đi vào luồng xử lý điều kiện tìm phòng. Kiểm tra cả cách diễn đạt mới, không chỉ các từ giống hệt bộ 58 câu.

### P1 — Truy xuất trong kho tài liệu chưa xác định đủ chủ đề và phạm vi

**Bằng chứng:**

- Câu 19 hỏi hợp đồng thuê trọ nhưng nguồn đầu là hướng dẫn KTX, tiếp theo là điện và cư trú.
- Câu 31 hỏi thủ tục cư trú nhưng nguồn đầu thuộc KTX, nước và điện.
- Câu 41 hỏi chi phí/điều kiện KTX so với phòng tư nhân nhưng lấy đoạn về hỗ trợ người được huy động PCCC, bán nhà ở tài sản công và sửa quy hoạch.
- Câu 57 hỏi phân biệt dấu hiệu lừa đảo với tranh chấp hợp đồng nhưng chủ yếu lấy án phí và thẩm quyền giải quyết dân sự. Nội dung trả lời cũng thừa nhận thiếu căn cứ về dấu hiệu tội phạm.

**Nguyên nhân đã xác minh:** `retrieve_legal()` chỉ ưu tiên/lọc nhãn `electricity` cho câu tiền điện. Các chủ đề còn lại tìm trên toàn bộ tài liệu `ready`. Điểm từ khóa BM25 được chia cho điểm cao nhất trong tập ứng viên; tài liệu đứng đầu vẫn có thể nhận điểm chuẩn hóa cao khi mọi ứng viên đều chưa đủ liên quan. Trộn điểm vector và BM25 rồi tính confidence không chứng minh nguồn trực tiếp trả lời câu hỏi: câu 31 nhận confidence 0,9189 dù nguồn lệch nhóm.

Với tối đa 5 nguồn, đường truy xuất thông thường giữ khoảng 3 đoạn chính rồi dành chỗ cho hiệu lực/chuyển tiếp. Khi các đoạn chính đã lệch, phần bổ sung vẫn theo các tài liệu lệch đó. Câu trả lời pháp lý cũng chỉ được kiểm tra giao từ vựng, chưa kiểm tra đầy đủ đối tượng, phạm vi và kết luận được nguồn hỗ trợ.

**Cách khắc phục:** Nhận diện nhiều chủ đề cùng lúc, ưu tiên tài liệu chính rồi mở rộng sang chủ đề liên quan. Câu 51 cần cả cư trú và dữ liệu cá nhân; câu 57 cần cả hợp đồng/dân sự và hình sự. Chấm lại ứng viên theo khả năng trả lời câu hỏi, đối tượng áp dụng và loại văn bản; loại đoạn về mua nhà tài sản công khi hỏi thuê trọ tư nhân. Tính ngưỡng “đủ căn cứ” từ nhãn kiểm định, không coi điểm xếp hạng đã chuẩn hóa là xác suất đúng. Chỉ thêm hiệu lực/chuyển tiếp cho tài liệu chính đã đạt tiêu chí liên quan.

**Điều kiện nghiệm thu:** Câu 19, 28, 31, 41, 57 lấy được nguồn trực tiếp hoặc nói rõ phần thiếu; nguồn liên chủ đề hợp lý không bị loại chỉ vì khác thư mục.

### P1 — Chỉ mục chưa đồng bộ với tập nguồn hiện hành

29 tệp hiện có đã được nạp đủ, có 1.821/1.821 đoạn được embedding. Tuy nhiên DB còn 53 tài liệu `ready`, gồm 24 đường dẫn không còn trong `Data`. Có 19/58 câu truy xuất ít nhất một tệp như vậy.

`index_folder()` duyệt và cập nhật các đường dẫn đang tồn tại; không đối chiếu toàn bộ chỉ mục để xử lý đường dẫn đã biến mất. `replace_document()` nhận diện tài liệu bằng `source_path`, nên đổi tên/chuyển từ PDF sang DOCX tạo bản mới và không tự xử lý bản ở đường dẫn cũ. Truy xuất chỉ kiểm tra trạng thái `ready`, không kiểm tra phiên bản kho nguồn đang đánh giá.

Không thể gọi mọi tài liệu này là “hết hiệu lực”: điều đã xác minh là **không còn tệp trong tập nguồn hiện hành**. Tuy vậy chúng có thể gây trùng bản, đưa OCR cũ trở lại, làm sai tên/số hiệu văn bản và chiếm chỗ của nguồn mới. Câu 51 nêu `154/2020/NĐ-CP` theo nguồn có đường dẫn cũ, trong khi tập hiện hành chứa bản trích `154/2024/NĐ-CP`; cần đối chiếu số hiệu từ metadata/bản gốc, không suy từ tên tệp.

**Cách khắc phục:** Quản lý manifest và phiên bản kho nguồn, quan hệ thay thế/trùng bản, số hiệu/ngày hiệu lực metadata độc lập với tên tệp. Chạy audit sau mỗi lần nạp và xác định rõ phiên bản dùng cho đánh giá. Việc loại/xóa 24 bản ghi hiện có vẫn cần xử lý riêng theo quyết định của người dùng; phân tích này không sửa hoặc xóa chúng.

### P1 — Có trích dẫn nhưng kết luận chưa được nguồn hỗ trợ

`_citation_accuracy()` chỉ kiểm tra số `[n]` có trong danh sách nguồn. Nếu danh sách nguồn rỗng, hàm trả 1,0. Vì vậy 1,0 trong lần chạy không có nghĩa mọi mệnh đề đều được nguồn chứng minh.

- Câu 56 thêm hướng dẫn về chứng cứ/cơ quan tiếp nhận trong khi nguồn cung cấp chỉ là tin phòng. Cần nguồn nghiệp vụ tương ứng, không dùng tin phòng làm căn cứ cho hướng dẫn này.
- Câu 58 xuất hiện tên giữ chỗ “Tên phòng” nhưng vẫn có `[1]`, `[4]`; số tham chiếu hợp lệ không ngăn được nội dung sai hoặc vô ích.
- Câu 51 lấy nội dung khai thác cơ sở dữ liệu cư trú để trả lời quyền thu thập thông tin của chủ trọ; cần kiểm tra đúng hoạt động và chủ thể áp dụng, thay vì coi hai hoạt động là tương đương.
- Câu 55 có nguồn dân sự/nền tảng liên quan, nhưng chưa đưa được các dấu hiệu cần kiểm tra theo đúng yêu cầu; không thể đánh giá chỉ bằng nhãn `criminal_law`.

**Cách khắc phục:** Kiểm tra từng kết luận với đoạn được trích, gồm tên văn bản, Điều/Khoản, số tiền, đối tượng và điều kiện áp dụng. Kiểm tra cả các kết luận không có trích dẫn. Nguồn rỗng nên ghi “không áp dụng” cho độ hợp lệ số trích dẫn. Đối với câu rủi ro, PCCC và dữ liệu cá nhân, thiếu nguồn trực tiếp phải nêu giới hạn; không ghép lời khuyên pháp lý vào câu trả lời tìm phòng.

### P1 — Sai lọc số liệu và mất trạng thái hội thoại

| Câu | Bằng chứng tái hiện | Cách sửa |
|---|---|---|
| 2 | “Từ 1,5 đến 2 triệu” được phân tích thành `min_price=1`, `max_price=2000000`. Kết quả đã có phòng 850.000 đồng. | Kế thừa đơn vị “triệu” cho cả hai đầu khoảng; giữ số thập phân trước khi đổi đơn vị. |
| 9 | “Từ 20 m² trở lên” cho `min_area=null`. | Chuẩn hóa đơn vị/Unicode; nhận cả “từ … trở lên”, “ít nhất”, “tối thiểu”. |
| 14 | “Từ 18 m² trở lên” cũng cho `min_area=null`. | Kiểm tra bộ lọc đã trích và dữ liệu thực tế, không chỉ đọc lời mô hình nói rằng phòng phù hợp. |
| 15 | Dù có lịch sử câu 14, `rewrite_query()` trả nguyên văn; kết quả tìm lại chỉ còn một ID trùng với 5 phòng trước. | Giữ bộ lọc và danh sách ID của lượt tìm trước; thao tác “rẻ nhất trong các phòng vừa tìm” phải chạy trên tập đó. |
| 16 | Có lịch sử câu 14–15 nhưng không viết lại; 5 ID kết quả hoàn toàn khác câu 15, gợi ý phòng 3,4 triệu. | Xác định “phòng đó” bằng ID phòng vừa chọn; trả tiện ích của phòng đó thay vì tìm một tập phòng mới. |
| 17 | Từ “điều kiện” kích hoạt `dieu `, chuyển sang luật. | Nhận tác vụ nới điều kiện tìm kiếm; chỉ rõ điều kiện nào đã làm tập kết quả rỗng. |
| 3 | Chatbot gọi phòng 900.000 đồng là rẻ nhất; những câu khác trong cùng lần chạy đã truy xuất tin 750.000 đồng. | Dùng truy vấn/sắp xếp giá trên toàn bộ tập đủ điều kiện, không gọi rẻ nhất toàn kho từ 5 kết quả xếp theo ngữ nghĩa. |
| 18 | Hỏi tin “vừa gợi ý” có mới không nhưng trả lại mô tả phòng, không trả ngày cập nhật. | Giữ ID trước đó và đưa thời điểm thu thập/cập nhật vào ngữ cảnh; trả rõ dữ liệu thiếu. |

`FOLLOW_UP_MARKERS` chưa có “phòng đó”, “vừa tìm được”; điều kiện độ dài tối đa 8 từ cũng không nhận đúng câu 15–16. Việc chỉ ghép câu chữ chưa đủ để bảo toàn phòng đã chọn: cần trạng thái gồm bộ lọc, ID kết quả và ID đang được hỏi.

Trường hợp “dưới 2 triệu” hiện dùng `price <= 2000000`; câu 1 có gợi ý đúng 2 triệu. Cần quy định rõ trong đặc tả cách hiểu “dưới” và “không quá”, rồi kiểm tra biên tương ứng.

## 4. Lỗi hoặc giới hạn trong cách kiểm thử cần sửa

1. **Nhãn một thư mục quá hẹp.** Gán `expected_intent`, nhiều `acceptable_categories`, loại nguồn và các ý bắt buộc/được phép thiếu. Câu 51 và 55 cần nhiều loại nguồn. Đổi nhãn báo cáo thành “chưa có nguồn mang nhãn chủ đề dự kiến”; giữ JSON gốc làm bằng chứng.
2. **Lịch sử hội thoại chưa đủ.** Runner chỉ cung cấp lịch sử cho câu 15–16. Câu 17–18 cũng nói về lượt tìm trước nhưng hiện được hỏi độc lập. Cần khai báo chuỗi hội thoại và lưu lịch sử thực tế từng câu; đánh giá đúng cả ID phòng và bộ lọc giữ lại.
3. **RAGAS chưa đo đủ tiêu chí của sản phẩm.** Faithfulness/Context Utilization chỉ nhìn hai đoạn đầu, tối đa 1.200 ký tự mỗi đoạn, khác ngữ cảnh đầy đủ mô hình trả lời đã nhận. Điểm không chứng minh đúng tác vụ, đúng giá/diện tích hay đúng phạm vi pháp lý. Cần thêm tỷ lệ đúng tác vụ, tuân thủ bộ lọc, giữ ID hội thoại, nguồn hỗ trợ từng kết luận và khả năng từ chối khi thiếu căn cứ.
4. **Mô hình giám khảo chưa ổn định.** Faithfulness và Context Utilization dùng Qwen2.5:1.5b; vẫn còn 4 lỗi Faithfulness ở câu 7, 29, 39, 55. Answer Relevancy đã được chấm lại bằng Qwen3.5:4b sau khi mô hình nhẹ chấm sai lệch rõ ở câu mẫu. Phải báo mô hình theo metric, cỡ mẫu, lỗi và kiểm định bằng người; không gộp các điểm thành “độ chính xác tổng thể”.
5. **Chưa có đáp án chuẩn độc lập.** Context Recall/Answer Correctness chưa thể công bố. Cần người kiểm định chọn điều khoản/nguồn và các ý đúng, cùng những ý không được suy diễn. Không lấy câu trả lời của chatbot làm đáp án chuẩn.
6. **Lượt chạy có gián đoạn dịch vụ.** Ghi nhận 7 ReadTimeout, 1 RemoteProtocolError và 1 ConnectError. Trong quá trình đánh giá có thao tác khôi phục Ollama; đặc biệt câu 48–49 cần chạy lại ở trạng thái ổn định trước khi coi lỗi kết nối là lỗi thường trực của sản phẩm. Tỷ lệ từ chối và p95 121,7 giây trong lượt này cũng cần đo lại. Các lỗi định tuyến vẫn có thể tái hiện không cần Ollama.

## 5. Thứ tự khắc phục đề nghị

1. Sửa tác vụ/định tuyến, gồm câu 17 và 19 câu chủ đề đi sai kho; bổ sung chặn trả lời nghiệp vụ từ tin phòng.
2. Sửa số tiền, diện tích, danh sách phòng trước đó và tham chiếu “phòng đó”. Đây là các lỗi đã tái hiện bằng mã phân tích, không cần đổi mô hình để xác nhận.
3. Xác định phiên bản kho nguồn, xử lý trùng/bản cũ theo quyết định của người dùng; nhận diện nhiều chủ đề và kiểm tra phạm vi đoạn truy xuất.
4. Kiểm tra từng kết luận với nguồn; tách nguồn pháp luật, thông tin nhà trường và hướng dẫn chức năng nền tảng.
5. Chuẩn hóa tập kiểm thử và nhãn độc lập; chạy lại trong môi trường Ollama cố định, không đồng thời chuyển mô hình/sửa dịch vụ; so sánh cùng câu và cùng phiên bản nguồn.

Tiêu chí hoàn thành phải được xác định từ yêu cầu dự án. Tối thiểu các trường hợp tái hiện nêu trên phải đạt: đúng tác vụ, đúng bộ lọc số liệu, giữ phòng đang được hỏi, có nguồn hỗ trợ kết luận hoặc nêu rõ thiếu căn cứ. Chưa đặt thêm ngưỡng số học cho RAGAS vì chưa có tập nhãn độc lập để hiệu chỉnh.

## 6. Dấu vết để sửa mã

| Khu vực | Vị trí | Nội dung cần xem |
|---|---|---|
| Phân loại và lọc số | `apps/api/app/room_service/chatbot/parser.py:66`, `:82`, `:100` | Đơn vị khoảng tiền, từ khóa tác vụ, diện tích |
| Hội thoại | `apps/api/app/room_service/chatbot/service.py:21`, `:48`, `:246` | Nhận câu tiếp nối, bảo toàn bộ lọc và ID |
| Hợp lệ trích dẫn | `apps/api/app/room_service/chatbot/service.py:79`, `:312` | Số nguồn hợp lệ chưa kiểm chứng kết luận |
| Xếp hạng và nguồn | `apps/api/app/room_service/chatbot/repo.py:91`, `:290`, `:306`, `:386` | Chuẩn hóa điểm, chủ đề, phiên bản chỉ mục, số đoạn chính |
| Kiểm tra bằng chứng | `apps/api/app/room_service/chatbot/legal_retrieval.py` | Giao từ vựng và quy tắc mới chủ yếu cho điện |
| Nạp dữ liệu | `apps/api/app/room_service/legal_knowledge/ingestion.py:39`, `legal_knowledge/repo.py:44` | Định danh theo đường dẫn, manifest và bản thay thế |
| Bộ kiểm thử | `eval/question_bank_ragas.py:110`, `:144`, `:250` | Chuỗi hội thoại, nhãn nguồn và cắt ngữ cảnh |

Tệp bằng chứng: `eval/reports/question_bank_ragas_2026-10-01.json`, `eval/reports/question_bank_corpus_audit_2026-10-01.json`, `eval/ragas_reports/question_bank_error_diagnostics_2026-10-01.json`. Phân tích này sửa cách diễn giải cảnh báo trong báo cáo và bổ sung chẩn đoán; chưa thay đổi hành vi chatbot.

## 7. Đối chiếu toàn bộ 26 câu cảnh báo

| Câu | Chủ đề người dùng hỏi | Hệ thống đã làm | Đánh giá cần khắc phục |
|---:|---|---|---|
| 19 | Điều khoản hợp đồng trước khi thuê | Truy xuất KTX, điện, cư trú | Thiếu căn cứ trực tiếp cho hợp đồng thuê trọ tư nhân; trả lời chuyển sang nội quy KTX. |
| 28 | Thu tiền nước theo đầu người | Truy xuất điện, PCCC, nền tảng; timeout | Cần nguồn về thỏa thuận/phân bổ tiền nước; chạy lại phần sinh sau khi nguồn đúng. |
| 29 | Chia chi phí đồng hồ nước chung | Tìm và gợi ý phòng | Sai tác vụ; nội dung từ khóa “đồng hồ nước/thỏa thuận” chưa được nhận. |
| 31 | Thủ tục cư trú cho sinh viên thuê trọ | Truy xuất KTX, nước, điện; timeout | Sai nguồn chính; ưu tiên hồ sơ/thủ tục cư trú. |
| 36 | Yêu cầu an toàn cháy nổ | Tìm phòng có mô tả PCCC | Tin phòng không đủ làm căn cứ cho yêu cầu an toàn. |
| 37 | Lối thoát nạn bị khóa/chặn | Gợi ý phòng có thang thoát hiểm | Sai tác vụ, không giải quyết tình huống người dùng hỏi. |
| 38 | Trách nhiệm với điện và cháy nổ | Lấy tin phòng và giá điện | Thiếu nguồn về trách nhiệm; không suy từ giá điện của tin đăng. |
| 39 | Thông tin đăng ký KTX 2026–2027 | Gợi ý phòng quanh các trường khác | Sai kho dữ liệu; đã có tài liệu KTX CTU nhưng không được tìm. |
| 40 | Chuẩn bị khi đăng ký KTX | Hỏi lại khu vực, ngân sách, tiện ích | Sai tác vụ hỏi thông tin KTX. |
| 41 | So sánh chi phí/điều kiện KTX và phòng tư nhân | Lấy PCCC, nhà tài sản công, quy hoạch | Chưa có nguồn chính KTX và dữ liệu chi phí; có đoạn sai đối tượng áp dụng. |
| 42 | Nêu thông tin phí/thời hạn còn thiếu trong tài liệu KTX | Hỏi lại khu vực, ngân sách | Sai tác vụ; cần đọc tài liệu và nêu phần thiếu. |
| 43 | Thông tin môi giới phải công khai | Gợi ý phòng rẻ | Sai tác vụ; không đọc tài liệu môi giới. |
| 44 | Kiểm tra quyền cho thuê trước khi chuyển tiền | Lấy tin phòng rồi đưa lời khuyên chung | Lời khuyên cần căn cứ phù hợp; danh sách phòng không xác minh quyền cho thuê. |
| 45 | Môi giới cung cấp thông tin sai | So sánh tiện ích/rủi ro của phòng | Sai tác vụ xử lý thông tin sai. |
| 47 | Kiểm tra người đăng và nguồn tin | Tìm phòng nhưng không có kết quả | Câu hướng dẫn kiểm tra tin bị hiểu thành bộ lọc tìm phòng. |
| 48 | Báo cáo tin đăng sai cho nền tảng | Tìm phòng; lỗi kết nối mô hình; dùng mẫu | Cần hướng dẫn chức năng báo cáo hoặc nguồn trách nhiệm nền tảng; đo lại kết nối. |
| 49 | Trách nhiệm nền tảng với thông tin người đăng | Tìm phòng; lỗi kết nối; dùng mẫu | Sai tác vụ; tài liệu nền tảng không được tìm. |
| 50 | Liên kết chuyển cọc lạ | Hỏi lại khu vực và ngân sách | Sai tác vụ rủi ro giao dịch; từ “chuyển cọc” không được nhận. |
| 51 | Dữ liệu cá nhân để hợp đồng/cư trú | Lấy nguồn cư trú cũ | Nguồn liên chủ đề có thể hợp lý; thiếu phần bảo vệ dữ liệu, phải kiểm tra số hiệu và phạm vi hoạt động. |
| 52 | Lưu/sử dụng ảnh căn cước | Liệt kê phòng | Sai tác vụ dữ liệu cá nhân. |
| 53 | Công khai giấy tờ/số điện thoại | Liệt kê phòng | Sai tác vụ dữ liệu cá nhân. |
| 54 | Chia sẻ dữ liệu sai mục đích | Gợi ý phòng | Lỗi khớp chuỗi `nha` bên trong `nhan`; không có câu yêu cầu tìm phòng. |
| 55 | Rủi ro đặt cọc nhưng không được xem phòng | Lấy dân sự và nền tảng đăng tin | Khác nhãn không đủ để kết luận sai nguồn; cần trả lời đủ yêu cầu rủi ro và kiểm chứng các suy luận. |
| 56 | Bằng chứng và nơi trình báo sau chuyển cọc cho tin giả | Gợi ý phòng rồi thêm hướng dẫn không có nguồn tương ứng | Sai tác vụ và thiếu căn cứ cho phần hướng dẫn nghiệp vụ. |
| 57 | Lừa đảo hay tranh chấp hợp đồng | Lấy án phí/thẩm quyền dân sự | Có liên quan một phần nhưng thiếu căn cứ hình sự trực tiếp để phân biệt. |
| 58 | Nhiều người nhận cọc rồi mất liên lạc | Gợi ý “Tên phòng” | Sai tác vụ; xuất hiện tên giữ chỗ và không giải đáp việc cung cấp thông tin. |
