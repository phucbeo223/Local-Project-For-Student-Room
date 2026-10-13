# Thuyết minh kỹ thuật: Chatbot hỗ trợ sinh viên tìm trọ

_Đề tài THS2026-66 · Cập nhật 14/10/2026 · Nội dung được đối chiếu với mã nguồn và lượt đánh giá ngày 13–14/10/2026._

## 1. Mục tiêu và phạm vi

Chatbot hỗ trợ sinh viên Đại học Cần Thơ tra cứu nhà trọ đang hiển thị trên hệ thống, hỏi thông tin ký túc xá CTU và tìm hiểu một số quy định, thủ tục cơ bản liên quan đến thuê trọ. Người dùng có thể diễn đạt yêu cầu bằng tiếng Việt tự nhiên, chẳng hạn nêu mức giá, quận, diện tích, tiện ích hoặc hỏi về tiền đặt cọc. Câu trả lời tìm trọ trả về các tin phù hợp kèm thuộc tính và lý do xếp hạng; câu trả lời pháp lý/KTX dẫn tới tài liệu hoặc đoạn văn bản đã truy xuất.

Chatbot không thay thế tư vấn pháp lý, không soạn hợp đồng hay điền biểu mẫu thủ tục. Nhóm sử dụng các mô hình dựng sẵn để nhúng văn bản và tạo ngôn ngữ; nhóm không huấn luyện mô hình ngôn ngữ hoặc mô hình embedding riêng. Những bước phân luồng, lọc thuộc tính, xếp hạng và kiểm tra cấu trúc được thực hiện bằng mã và quy tắc xác định.

## 2. Kiến trúc hệ thống

Hệ thống được tổ chức thành bốn lớp chính:

1. **Giao diện web:** trang `/tro-ly` dùng React/Next.js để nhận câu hỏi, gửi ngữ cảnh hội thoại, hiển thị câu trả lời, thẻ tin trọ và nguồn tham khảo. Người dùng cần đăng nhập để sử dụng chatbot và xem lịch sử gắn với tài khoản.
2. **API và điều phối hội thoại:** FastAPI cung cấp nhóm endpoint `/chatbot`, gồm gửi câu hỏi, xem/xoá hội thoại và gửi phản hồi. `ChatService` điều phối việc viết lại câu nối tiếp, phân loại ý định, truy xuất dữ liệu, gọi mô hình, kiểm tra căn cứ và dựng cấu trúc phản hồi.
3. **Kho dữ liệu và truy xuất:** PostgreSQL lưu tin trọ, vector embedding, kho tài liệu pháp lý/KTX đã chia đoạn, lịch sử và số liệu vận hành. `ChatRepository` thực hiện truy vấn có cấu trúc và tìm kiếm lai; `legal_knowledge` quản lý việc nạp, phiên bản và trạng thái tài liệu.
4. **Các bộ máy mô hình:** `multilingual-e5-small` tạo vector truy vấn và vector tài liệu. Trong chế độ tác nhân đang bật, Gemini phân tích câu hỏi, Qwen `qwen3.5:9b` chạy qua Ollama chọn nguồn, sau đó Gemini tổng hợp câu trả lời và đối chiếu các mệnh đề với chứng cứ. Nhánh tra cứu danh mục KTX và so sánh theo thuộc tính có thể dựng câu trả lời trực tiếp từ dữ liệu có cấu trúc. Khi mô hình không khả dụng hoặc câu trả lời không qua kiểm tra, hệ thống có thể chuyển sang câu trả lời mẫu dựa trên dữ liệu hoặc trích đoạn nguồn.

Luồng tổng quát:

```text
Người dùng → giao diện web → API /chatbot → quy tắc và phân loại ý định
                                         ├─ tìm trọ → lọc dữ liệu → xếp hạng lai → tạo câu trả lời
                                         └─ pháp lý/KTX → truy xuất đoạn nguồn → sinh/kiểm chứng → trích dẫn
                                  ← câu trả lời + kết quả + nguồn + trạng thái hội thoại
```

Các thành phần được cấu hình qua `apps/api/app/config.py` và biến môi trường. Schema kho pháp lý mặc định là `legal_ctu_v1`; tin trọ được đọc từ `public.aggregated_listings`. Mặc định `chatbot_agents_enabled=false` và `chatbot_graph_enabled=false`: luồng nhiều tác nhân và Graph RAG là tuỳ chọn, không nên ghi là cấu hình vận hành mặc định. Tên mô hình sinh thực tế phụ thuộc cấu hình triển khai; cấu hình trong mã đặt embedding `intfloat/multilingual-e5-small`, Gemini mặc định `gemini-3.5-flash-lite` và Qwen `qwen2.5:7b-instruct`.

**Cấu hình triển khai được bật ngày 13/10/2026:** database hiện tại là `nckh_feature`; Graph RAG, tác nhân phân tích và tổng hợp đều được bật qua biến môi trường. Cấu hình này sử dụng release dữ liệu ngày 07/10/2026:

| Thành phần | Cấu hình sử dụng |
|---|---|
| Kho pháp lý/KTX | `legal_ctu_ktx_v2_20261007`: 44 tài liệu, 530 đoạn có vector |
| Kho tin trọ của release | `housing_graph_word_repair_v16`: 789 tin |
| Đồ thị | `graph_ctu_ktx_v2_20261007`: 1.349 nút, 3.264 cạnh |
| Phân tích câu hỏi | Gemini, alias `gemini-3.1-flash-lite` |
| Chọn nguồn | Qwen `qwen3.5:9b`, Ollama cục bộ; thư mục model `D:\Ollama\models` |
| Tổng hợp và kiểm chứng | Gemini, alias `gemini-3.8-flash-high` qua proxy đã cấu hình |

Các tên Gemini trên là alias do endpoint cung cấp; báo cáo ghi đúng cấu hình gọi và không suy diễn mô hình nền của proxy. Luồng tác nhân cho nhánh pháp lý là:

```text
Câu hỏi → Gemini phân tích → tìm kiếm lai và mở rộng đồ thị
        → Qwen chọn nguồn → Gemini tổng hợp → kiểm chứng nguồn và quy tắc
        → câu trả lời kèm trích dẫn hoặc phản hồi nêu phần thiếu căn cứ
```

## 3. Quy trình xử lý câu hỏi

### 3.1 Tiếp nhận, ngữ cảnh và phân loại

API kiểm tra yêu cầu, giới hạn tần suất và lấy lịch sử gần nhất do giao diện gửi lên. `rewrite_query` ghép ngữ cảnh phù hợp cho những câu nối tiếp ngắn như “rẻ hơn”, “gần hơn”, “phòng đó” hoặc “quy định này áp dụng từ khi nào”. Bộ lọc ở từng lượt được cập nhật từ câu người dùng; nội dung do chatbot sinh không được coi là sở thích do người dùng cung cấp.

`parse_query` chuẩn hoá văn bản và phân loại mục đích, đồng thời trích các trường có thể biểu diễn thành bộ lọc như giá, diện tích, khu vực, tiện ích, loại chỗ ở và cách sắp xếp theo giá. Quy tắc ưu tiên xử lý tình huống khẩn cấp, ngoài phạm vi và ngoài khu vực trước khi gọi mô hình. Câu hỏi KTX được chuyển qua mô-đun tư vấn KTX; câu hỏi pháp lý được chuyển sang nhánh RAG pháp lý; các câu tìm kiếm còn lại đi vào nhánh tin trọ.

### 3.2 Nhánh tìm nhà trọ

1. **Lọc ứng viên bằng SQL:** chỉ lấy tin đang hoạt động và thoả điều kiện hiển thị chung của giao diện. Các ràng buộc đọc được từ câu hỏi, như giá, diện tích, quận, khoảng cách tới CTU, thời gian di chuyển, tiện ích và giới hạn giới tính, được áp dụng trước khi xếp hạng. Nhờ vậy chatbot không đưa ra tin đã ẩn hoặc không thể mở từ trang danh sách.
2. **Tạo truy vấn ngữ nghĩa:** E5 mã hoá câu hỏi thành vector 384 chiều. Vector tin được tính trước bằng indexer và lưu trong PostgreSQL/pgvector. Nếu embedding không tải được, nhánh này tiếp tục bằng lọc có cấu trúc và BM25.
3. **Tính điểm kết hợp:** trên tập ứng viên, BM25 đo độ khớp từ khoá với tiêu đề, địa chỉ và nội dung tin; vector score đo tương đồng ngữ nghĩa; điểm sở thích đánh giá số điều kiện người dùng nêu được tin đáp ứng; các yếu tố chất lượng, độ mới và độ gần CTU điều chỉnh thứ hạng. Khi có vector, điểm tổng hiện được tính theo trọng số 0,35 vector + 0,25 BM25 + 0,15 sở thích + 0,10 chất lượng + 0,08 độ mới + 0,02 khoảng cách, sau đó chuẩn hoá theo tổng trọng số. Khi không có vector, trọng số của các thành phần còn lại được chuẩn hoá lại. Câu yêu cầu “rẻ nhất” dùng sắp xếp giá tăng dần trong tập tin thoả điều kiện.
4. **Chọn và trình bày kết quả:** tối đa năm tin được trả về kèm điểm BM25, điểm vector, lý do khớp và liên kết nguồn. Với câu hỏi chi tiết về một tin vừa nêu, chatbot dùng ID tin trong trạng thái hội thoại để đọc đúng tin đó thay vì tự thay bằng một tin khác.
5. **Kiểm tra câu trả lời:** các số liệu như giá, tiện ích và trích dẫn được so với tin nguồn. Nếu câu trả lời do mô hình tạo không gắn trích dẫn hợp lệ hoặc nêu giá/tiện ích không được dữ liệu hỗ trợ, API thay bằng mẫu trả lời xác định từ các tin đã lấy.

### 3.3 Nhánh pháp lý và ký túc xá

Tài liệu được chuẩn hoá, lưu thông tin nguồn và chia thành các đoạn có tiêu đề, trang hoặc vị trí tham chiếu khi có. Corpus hiện khai báo 45 tài liệu trong `apps/api/chatbot_corpus/manifest.json`; số đoạn thực tế cần căn cứ vào lần nạp dữ liệu đang chạy trong cơ sở dữ liệu, vì manifest đếm tài liệu chứ không đảm bảo trạng thái index ở mọi môi trường.

Khi nhận câu hỏi, hệ thống mở rộng một số từ khoá pháp lý, nhận diện nhóm chủ đề và các khía cạnh cần trả lời. Truy vấn SQL lấy các ứng viên theo tìm kiếm toàn văn PostgreSQL (`tsvector`/`ts_rank_cd`) và, nếu vector sẵn có, theo tương đồng cosine của embedding. Hai danh sách từ khoá và ngữ nghĩa được hợp nhất; BM25 được tính thêm trên tiêu đề, mục và nội dung. Khi có vector, điểm cơ sở là `0,55 × điểm vector + 0,45 × BM25`; khi không có vector, hệ thống dùng điểm BM25. Hàm `rerank_legal` áp dụng ưu tiên theo chủ đề, thuật ngữ và các điều kiện luật liên quan; một số câu hỏi yêu cầu nhiều khía cạnh có bước giữ lại các đơn vị chứng cứ cần thiết trước khi chọn tối đa năm nguồn hiển thị. Cách này kết hợp khả năng bắt đúng điều khoản nhờ từ khoá với khả năng tìm câu diễn đạt khác nhờ vector. Ngưỡng tin cậy 0,65 là ngưỡng điều phối được cấu hình để quyết định có tiếp tục dùng các đoạn tìm được hay không; đây là điểm heuristic nội bộ, không phải xác suất đúng đã được hiệu chuẩn.

Các đoạn được chọn đưa vào prompt để Gemini hoặc Qwen tổng hợp bằng tiếng Việt và gắn trích dẫn dạng `[n]`. Hệ thống kiểm tra tính hợp lệ của thứ hạng trích dẫn và đối chiếu từng mệnh đề với đúng đoạn nguồn được dẫn. Các kiểm tra xác định bổ sung bao gồm số liệu, chủ thể, điều kiện, ngoại lệ, hiệu lực và những khẳng định không có trích dẫn. Nếu phát hiện mệnh đề không được hỗ trợ, hệ thống thử sửa hoặc chỉ giữ các mệnh đề đã vượt kiểm chứng; nếu không đạt yêu cầu, chuyển sang trích nguyên văn, trích xuất một phần hoặc mẫu có nêu rõ giới hạn căn cứ. Việc này giảm rủi ro trả lời sai nhưng không bảo đảm loại bỏ hoàn toàn sai sót của mô hình hay thiếu sót của corpus.

### 3.4 Graph RAG và chọn nguồn bằng tác nhân

`GraphChatRepository` mở rộng bộ truy xuất lai bằng các quan hệ có kiểu đã được dựng trong PostgreSQL. Với tin trọ, hệ thống nhận diện các thực thể địa điểm được khai báo, đi qua quan hệ `located_in` để giới hạn tập tin ứng viên rồi áp dụng bộ lọc SQL và xếp hạng lai. Các địa điểm thay thế được kết hợp bằng OR; tiện ích vẫn là điều kiện giao trong SQL. Quan hệ và chứng cứ của những tin được chọn được trả về trong trace, với phạm vi một bước quan hệ.

Với pháp lý, các điều khoản trong kết quả truy xuất lai là nút khởi đầu. Truy vấn SQL đệ quy đi theo cạnh `cites` tối đa hai bước, kiểm tra đường đi để tránh chu trình và giới hạn 24 liên kết. Hệ thống chỉ bổ sung nội dung điều khoản thuộc cùng tài liệu với đoạn nguồn tương ứng, giữ tổng nội dung mỗi nguồn không quá 5.500 ký tự. Những điều khoản bổ sung giữ thông tin nguồn và trang; các cạnh thành viên/chủ đề không được dùng để mở rộng sang toàn bộ văn bản. Vì vậy, bật Graph RAG không có nghĩa mọi câu đều tìm được cạnh dẫn chiếu để bổ sung.

Sau truy xuất, Qwen nhận các ứng viên chứng cứ và trả về lựa chọn nguồn theo cấu trúc, thay vì tự viết đáp án pháp lý ở bước này. Gemini nhận những nguồn đã chọn để tổng hợp, gắn trích dẫn và nêu giới hạn; một lượt Gemini khác trong cùng workflow kiểm chứng từng mệnh đề. Hệ thống có thể yêu cầu sửa rồi kiểm chứng lại trước khi chấp nhận. Đây là các bước khác nhau trong pipeline; chấm RAGAS sau benchmark là một quy trình đánh giá riêng.

Đồ thị gắn với release của kho tin trọ và pháp lý thông qua schema và SHA-256. Khi khởi tạo, repository đối chiếu các giá trị này và từ chối release không khớp, giúp tránh dùng quan hệ của một phiên bản dữ liệu để giải thích nguồn ở phiên bản khác.

## 4. Thuật toán và kỹ thuật sử dụng

| Kỹ thuật | Vai trò trong chatbot |
|---|---|
| Quy tắc và biểu thức nhận diện | Phát hiện ý định, tình huống ưu tiên, điều kiện tìm trọ và câu hỏi nối tiếp; có thể kiểm tra, giải thích và điều chỉnh trực tiếp. |
| SQL và lọc ràng buộc | Loại tin không phù hợp với điều kiện cứng và chỉ truy xuất tin đang hiển thị; hỗ trợ các trường có cấu trúc như giá, diện tích, loại tin và vị trí. |
| BM25 / PostgreSQL full-text search | Tìm các từ hoặc thuật ngữ xuất hiện trong tin và đoạn tài liệu; hiệu quả với tên văn bản, điều khoản, địa danh và cụm từ chính xác. |
| Embedding E5 và pgvector | Biểu diễn câu hỏi và tài liệu thành vector 384 chiều để tìm nội dung tương tự về nghĩa dù cách dùng từ khác nhau. Đây là suy luận từ mô hình có sẵn, không phải huấn luyện của đề tài. |
| Xếp hạng lai và luật rerank | Kết hợp tín hiệu từ khoá, ngữ nghĩa và mức đáp ứng tiêu chí; riêng pháp lý có ưu tiên chủ đề và bảo toàn các khía cạnh chứng cứ cần thiết. |
| RAG (Retrieval-Augmented Generation) | Đưa các nguồn vừa truy xuất vào ngữ cảnh sinh câu trả lời, giúp gắn câu trả lời với tin trọ hoặc văn bản đã nạp thay vì chỉ dựa vào kiến thức tham số của LLM. |
| Graph RAG và duyệt đồ thị có giới hạn | Kết hợp kết quả tìm kiếm lai với quan hệ địa điểm và dẫn chiếu điều khoản; lưu đường truy xuất và giới hạn số bước, số liên kết, độ dài nguồn. |
| Điều phối tác nhân theo vai trò | Gemini phân tích truy vấn; Qwen chọn nguồn; Gemini tổng hợp và kiểm chứng trước khi trả lời trong nhánh pháp lý. |
| Kiểm chứng căn cứ và mẫu dự phòng | Đối chiếu trích dẫn, mệnh đề và dữ liệu nguồn; hạ cấp sang nội dung trích xuất/mẫu khi không xác minh được. |
| Cache, lịch sử và telemetry | Tái sử dụng một số câu trả lời theo phạm vi cache; lưu hội thoại theo tài khoản; ghi độ trễ, chế độ truy xuất, trạng thái suy giảm và phản hồi để theo dõi chất lượng. |

## 5. Dữ liệu, lưu trữ và vận hành

Tin trọ dùng bảng `aggregated_listings`; trường embedding và hash nội dung giúp nhận biết tin cần lập chỉ mục lại. Corpus pháp lý/KTX được quản lý theo schema riêng, có bảng tài liệu, đoạn văn bản, vector, trạng thái bật/tắt và thông tin nguồn. Indexer `index_listings` cập nhật vector cho tin mới hoặc thay đổi; `legal_knowledge.index_corpus` kiểm tra manifest rồi nạp tài liệu và vector vào schema đã chọn.

Hội thoại và lượt hỏi được lưu theo tài khoản trong `chatbot_conversations` và `chatbot_turns`; quyền truy cập hội thoại được giới hạn theo chủ sở hữu. Câu hỏi không được ghi vào bảng sự kiện tổng hợp; bảng `chatbot_events` lưu thông tin vận hành như ý định, độ tin cậy, chế độ truy xuất, nhà cung cấp sinh câu trả lời, số kết quả và độ trễ. Phản hồi đánh giá được lưu riêng trong `chatbot_feedback`. Khoá API Gemini được cấu hình qua môi trường triển khai, không đặt trong mã nguồn.

## 6. Đánh giá và giới hạn

Lượt đánh giá ngày 13–14/10/2026 sử dụng nguyên văn 48 câu hỏi mã 19–66 trong ngân hàng ngày 12/10/2026, gồm 36 câu pháp lý và 12 câu KTX. Runner gọi trực tiếp `ChatService.ask` với database `nckh_feature`, lưu phản hồi, nguồn, ngữ cảnh sinh và trace tác nhân; việc ghi sự kiện tổng hợp được tắt trong lượt đánh giá. Phạm vi đo là tầng service, nên độ trễ không bao gồm trình duyệt, HTTP và xác thực API.

Hệ thống đã trả phản hồi cho 48/48 câu, không có lỗi thu thập. Trong 36 câu pháp lý, 11 phản hồi không bị đánh dấu thiếu căn cứ và 25 phản hồi được hệ thống đánh dấu trả lời một phần. Trong 12 câu KTX, 11 phản hồi có căn cứ truy xuất; mã 62 không tìm được nguồn cho yêu cầu về phiếu CTU năm 2025 và trả về thông báo không khớp danh mục. Đây là trạng thái do hệ thống tự phân loại, cần được đọc cùng nội dung phản hồi và nguồn.

Tất cả 36 câu pháp lý ghi nhận chế độ `legal_graph_hybrid`. Trace của 10 câu có cạnh đồ thị được duyệt; 4 câu có điều khoản liên kết được ghi trong trường `included_provisions`. Độ trễ trung vị của nhánh pháp lý là 73,715 giây, của nhóm KTX là 0,061 giây; các câu KTX được trả lời từ dữ liệu có cấu trúc. Trên toàn bộ 48 câu, trung vị là 64,832 giây và phân vị 95 là 141,736 giây. Các số đo này mô tả cấu hình đang chạy và không đủ để quy riêng thay đổi chất lượng cho đồ thị nếu chưa có lượt bật/tắt với cùng dữ liệu và mô hình.

RAGAS 0.3.9 sử dụng Gemini alias `gemini-3.8-flash-high` làm judge, tách khỏi các bước kiểm chứng trong luồng trả lời. Answer Relevancy dùng embedding `intfloat/multilingual-e5-small` và `strictness=1`. Các phản hồi một phần vẫn được chấm khi có ngữ cảnh. Với mã 62 không có ngữ cảnh, hai chỉ số phụ thuộc nguồn được ghi N/A; độ liên quan câu hỏi vẫn được đánh giá.

| Chỉ số RAGAS | Trung bình | Số câu có điểm |
|---|---:|---:|
| faithfulness | 0.5749 | 47/48 |
| answer_relevancy | 0.8578 | 48/48 |
| context_utilization | 0.9235 | 47/48 |

| Nhóm | Faithfulness | Answer Relevancy | Context Utilization |
|---|---:|---:|---:|
| 36 câu pháp lý | 0.4756 (36 câu) | 0.8714 (36 câu) | 0.9048 (36 câu) |
| 12 câu KTX | 0.8999 (11 câu) | 0.8170 (12 câu) | 0.9848 (11 câu) |

Giới hạn đầu ra của judge là 8.192 token trong lượt chấm chính; riêng Faithfulness của mã 25 được chấm lại thành công với 16.384 token sau lỗi JSON rỗng. Lịch sử thử lại và quyết định chấm được giữ trong JSON.

Điểm bám nguồn trung bình còn thấp, đặc biệt ở nhóm pháp lý. Các quyết định NLI cho thấy một số khuyến nghị hoặc mệnh đề bổ sung chưa được đoạn nguồn hỗ trợ trực tiếp; cần rà soát từng câu và nguồn trước khi kết luận về chất lượng pháp lý.

Báo cáo chi tiết: `docs/reviews/graph_ragas_48_20261013.html`; checkpoint gốc: `eval/reports/graph_ragas_48_agents_gemini_qwen_20261013.json`; metadata release và checksum: `docs/reviews/graph_ragas_48_20261013.manifest.json`.

Faithfulness đo mức các mệnh đề được ngữ cảnh hỗ trợ; Answer Relevancy đo sự liên quan đến câu hỏi; Context Utilization đánh giá mức hữu dụng của ngữ cảnh theo thứ hạng. Các điểm này chưa đo độ chính xác pháp lý hoặc độ đầy đủ theo một đáp án độc lập. Chưa có bộ đáp án được người độc lập gán nhãn nên không báo Answer Correctness và Context Recall. Mô hình sinh và judge cùng alias Gemini qua proxy có thể tạo thiên lệch; tên alias không xác minh được mô hình nền của proxy.

Chất lượng cuối cùng phụ thuộc vào độ đầy đủ, tính cập nhật và cách chia đoạn của nguồn; chất lượng tin được thu thập; khả năng nạp embedding; hạn mức và độ trễ của nhà cung cấp mô hình. Khi truy xuất yếu hoặc mô hình không sẵn sàng, chatbot có thể trả lời một phần, trích nguồn hoặc dùng mẫu. Việc bổ sung corpus, rà soát nguồn và đánh giá với bộ đáp án độc lập là các hướng cần tiếp tục thực hiện. Mọi số liệu về mô hình và chất lượng cần ghi theo đúng cấu hình cùng thời điểm đo.

## 7. Tóm tắt đóng góp kỹ thuật

Chatbot kết hợp xử lý ngôn ngữ tiếng Việt bằng luật, truy vấn dữ liệu có cấu trúc, tìm kiếm từ khoá, tìm kiếm ngữ nghĩa bằng embedding và mô hình ngôn ngữ lớn có truy xuất nguồn. Thiết kế tách riêng luồng tin trọ với luồng pháp lý/KTX để mỗi loại câu hỏi dùng cách lọc, xếp hạng và kiểm chứng phù hợp. Cơ chế trích dẫn, kiểm tra dữ liệu và hạ cấp có kiểm soát giúp câu trả lời có thể truy ngược tới tin hoặc tài liệu liên quan, đồng thời công khai giới hạn khi chứng cứ hiện có chưa đủ.
