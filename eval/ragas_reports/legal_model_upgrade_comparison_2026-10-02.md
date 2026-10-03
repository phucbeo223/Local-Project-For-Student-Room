# Nâng cấp model và kiểm thử 36 câu pháp lý

Phạm vi: hợp đồng, cư trú, PCCC, điện, nước, môi giới, dữ liệu cá nhân, nền tảng và hình sự. Các câu giá phòng, khoảng cách và dữ liệu phòng cũ được loại khỏi lượt đánh giá.

## Máy và model

- Ryzen 5 7535HS; RAM khoảng 15,2 GiB; RTX 4050 Laptop 6.141 MiB VRAM.
- Cài Qwen 3.5 9B Q4_K_M (khoảng 6,6 GB); xóa Qwen 3.5 4B và Qwen 2.5 1.5B sau khi thử model mới thành công.
- Thử local ở cửa sổ 8.192 token: khoảng 25,44 giây, 7,52 token/giây. Ngữ cảnh lớn hơn có thể phải dùng thêm RAM.
- Cấu hình cuối: Gemini 3.5 Flash Lite ưu tiên, Qwen 9B dự phòng. Đọc đầy đủ các khóa đánh số, ưu tiên slot 3 đã gọi thành công; slot 2 bị Google từ chối quyền dự án (HTTP 403), slot 1 gặp quá tải khi thử Gemini 3.8 (HTTP 503). Không ghi khóa vào báo cáo.
- Lượt thử Gemini 3.8 chạm hạn mức ngày 20 lượt (HTTP 429), phải chuyển sang local và chậm. Giữ checkpoint ban đầu và lượt local riêng, rồi chạy đủ 36 câu mới bằng cấu hình cuối. Bộ chấm Gemini 3.5 chạm 500 lượt/ngày; lưu riêng lượt chấm đó, rồi chấm lại cả hai bộ bằng Gemini 3.1 Flash Lite với cùng tham số.

## Sửa hệ thống

- Sửa cấu hình Compose từng ghi đè provider/model; giữ khóa trong .env.
- Phân biệt lỗi quyền với quá tải; tạm ngừng gọi model khi 503/429. Không đổi khóa để vượt hạn mức 429.
- Truy xuất đúng hơn cho công khai dữ liệu cá nhân và phòng tránh lừa đảo; giảm các điều khoản định danh, thông báo sự cố hoặc thẩm quyền tố tụng lệch câu hỏi.
- Phân biệt ‘tài liệu này không nêu’ với ‘pháp luật không quy định’; cho sửa câu trả lời một lần theo lỗi kiểm tra nguồn, rồi kiểm tra lại.
- Bước kiểm tra local chỉ gửi mỗi nguồn một lần, giữ toàn bộ nội dung/ngoại lệ và ánh xạ trích dẫn; giới hạn giải thích lỗi ngắn. Không sinh lại khi bộ kiểm tra không khả dụng; vẫn chuyển về trích đoạn/từ chối khi chưa xác nhận được.
- Chặn kết luận xử phạt/bồi thường/hoàn trả thiếu trích dẫn hoặc thiếu căn cứ trực tiếp; sau khi rà đủ 36 câu, chỉ câu 23 bị phát hiện lỗi mới và được chạy lại. 35 câu còn lại giữ nguyên. Hạn mức ngày dùng thời gian chờ Google cung cấp.
- 89 kiểm tra hồi quy đạt. Kiểm thử câu hỏi dùng ChatService và cơ sở dữ liệu thật; tắt ghi sự kiện chat trong runner.
- Kho đã nạp: 30 tài liệu, 1829/1829 đoạn có embedding; 0 nguồn chưa nạp, 0 nguồn ready vắng trong Data.

## Kết quả vận hành

| Chỉ số | Trước | Sau |
|---|---:|---:|
| Câu đã chạy | 36 | 36 |
| Phản hồi gán trạng thái tổng hợp | 3 | 30 |
| Câu trả lời một phần | 32 | 5 |
| Chưa đủ căn cứ tổng hợp | 1 | 1 |
| Lỗi chạy | 0 | 0 |
| Độ trễ p50 (giây) | 13.97 | 3.05 |
| Độ trễ p95 (giây) | 24.86 | 122.74 |

Provider của phản hồi cuối: {'gemini/gemini-3.5-flash-lite': 26, 'legal-partial-extractive/-': 5, 'legal-extractive/-': 2, 'qwen-local/qwen3.5:9b': 2, 'template/-': 1}.
Các lần gọi model, bao gồm thử trước khi chuyển về trích đoạn: {'gemini/gemini-3.5-flash-lite/generate': 47, 'gemini/gemini-3.5-flash-lite/check_legal_evidence': 47, 'qwen-local/qwen3.5:9b/generate': 5, 'qwen-local/qwen3.5:9b/check_legal_evidence': 5}.
Lỗi gọi model: {'gemini/RuntimeError/429': 5, 'gemini/RuntimeError/-': 5}. JSON lưu thời gian từng lần gọi.

## Ragas: chấm lại bằng cùng phương pháp

Phương pháp khớp: có. Mô hình: gemini-3.1-flash-lite; Ragas 0.3.9; dùng toàn bộ nguồn đã đưa vào sinh câu trả lời, chấm cả câu từ chối, Answer Relevancy strictness=1, E5 đa ngôn ngữ.

Các trung bình dưới đây chỉ lấy những câu có điểm ở **cả hai lượt**. Mỗi metric có số cặp riêng; lỗi chấm được giữ trong JSON.

| Metric | Trước | Sau | Chênh lệch | Số cặp |
|---|---:|---:|---:|---:|
| faithfulness | 0.9191 | 0.6749 | -0.2443 | 35 |
| answer_relevancy | 0.6987 | 0.7553 | +0.0565 | 36 |
| context_utilization | 0.5486 | 0.6042 | +0.0556 | 36 |

### Đọc kết quả

Không xem số câu tổng hợp tăng là bằng chứng độ đúng tăng. Đối chiếu cả ba metric và từng phán định nguồn; giữ nguyên điểm native Ragas, không loại câu hoặc sửa prompt chấm để nâng điểm.
Độ trễ p50 đo câu điển hình; p95 phản ánh các lượt chuyển về local khi Gemini hết quota. Model 9B đã chạy được trên máy, nhưng không đáp ứng cùng tốc độ với Gemini cho kiểm tra pháp lý dài.

### Phân tích các điểm bám nguồn thấp

Các ví dụ dưới đây là phán định tự động, chưa phải kết luận của chuyên gia luật:

- Judge ghi noncommittal ở 6 câu: [14, 28, 29, 33, 35, 36]. Trong đó [14, 28, 29, 36] vẫn được hệ thống gán trạng thái tổng hợp dù nội dung nói chưa tìm thấy căn cứ cho yêu cầu chính. Vì vậy số 30 không phải số câu đã giải quyết đúng; cần rà cách đánh dấu mức hoàn thành và bổ sung nguồn đúng câu hỏi.
- Câu 2: 3 phát biểu bị chấm không được nguồn hỗ trợ; chi tiết ở JSON.
  - Phát biểu: Văn bản 2026_204_79_VBHN-VPQH, Điều 163, trang 1 quy định hợp đồng phải bao gồm nội dung về thời hạn và phương thức thanh toán tiền thuê nhà ở. Lý do judge: The context in document 2026_204_79_VBHN-VPQH, Article 163, Clause 4, mentions the term and payment method for buying, renting, or lease-purchasing housing, but it does not explicitly state that the contract *must* include these specific contents as a mandatory requirement for all housing contracts in the general definition provided in the first part of Article 163.
  - Phát biểu: Thông tin trên là thông tin tham khảo. Lý do judge: The provided context contains legal text excerpts but does not contain any disclaimer or statement indicating that the information is for reference purposes only.
- Câu 13: 4 phát biểu bị chấm không được nguồn hỗ trợ; chi tiết ở JSON.
  - Phát biểu: Sinh viên thuê trọ cần chuẩn bị hồ sơ gồm tờ khai thay đổi thông tin cư trú. Lý do judge: The context in Document 1, Article 28, states that the dossier includes a declaration for changing residence information, but it explicitly notes that these regulations do not directly relate to students renting accommodation.
  - Phát biểu: Sinh viên thuê trọ cần chuẩn bị giấy tờ chứng minh chỗ ở hợp pháp. Lý do judge: The context in Document 1, Article 28, mentions this requirement for a general dossier, but explicitly states that these cases do not directly relate to students renting accommodation.
- Câu 17: 4 phát biểu bị chấm không được nguồn hỗ trợ; chi tiết ở JSON.
  - Phát biểu: Người thuê phòng cần kiểm tra việc duy trì điều kiện an toàn phòng cháy trong việc sử dụng nguồn lửa và nguồn nhiệt. Lý do judge: Văn bản quy định nội dung kiểm tra về phòng cháy, chữa cháy bao gồm việc duy trì điều kiện an toàn khi sử dụng nguồn lửa, nguồn nhiệt, nhưng không quy định trách nhiệm này thuộc về 'người thuê phòng'.
  - Phát biểu: Người thuê phòng cần kiểm tra việc duy trì điều kiện an toàn phòng cháy trong việc sử dụng thiết bị và dụng cụ sinh lửa, sinh nhiệt. Lý do judge: Văn bản quy định nội dung kiểm tra về phòng cháy, chữa cháy bao gồm việc duy trì điều kiện an toàn khi sử dụng thiết bị, dụng cụ sinh lửa, sinh nhiệt, nhưng không quy định trách nhiệm này thuộc về 'người thuê phòng'.
- Câu 19: 4 phát biểu bị chấm không được nguồn hỗ trợ; chi tiết ở JSON.
  - Phát biểu: Trợ lý Trọ CTU là người cung cấp thông tin. Lý do judge: The provided context does not mention any entity named 'Trợ lý Trọ CTU' or identify the source of the information.
  - Phát biểu: Các văn bản hiện tại chưa có quy định cụ thể hướng dẫn người thuê nhà cần làm gì ngay lập tức khi phát hiện lối thoát nạn bị khóa hoặc bị chặn. Lý do judge: The context mentions the responsibility to maintain escape routes, but it does not contain information about what to do immediately if they are blocked or locked, nor does it state that such regulations do not exist.
- Câu 22: 7 phát biểu bị chấm không được nguồn hỗ trợ; chi tiết ở JSON.
  - Phát biểu: Nghĩa vụ của người môi giới được quy định tại Luật 29-2023-QH15, Điều 62, Khoản 3. Lý do judge: Nội dung tại Khoản 3 Điều 62 mô tả các công việc (nội dung) của môi giới bất động sản, không phải là danh mục các nghĩa vụ pháp lý của người môi giới (nghĩa vụ được quy định tại Điều 65).
  - Phát biểu: Các nguồn thông tin hiện tại chưa có quy định chi tiết về các bước người thuê cần tự kiểm tra quyền cho thuê. Lý do judge: Văn bản cung cấp không đề cập đến các bước người thuê cần tự kiểm tra quyền cho thuê.

Lời giới thiệu và lời nhắc tham khảo cũng bị native Faithfulness tính thành phát biểu thiếu nguồn. Đây là giới hạn của phép đo; không bỏ chúng khỏi điểm công bố. Ở câu 13, judge dường như nhầm phần ‘Lược khỏi bản trích’ về các trường hợp đặc thù không liên quan với phần hồ sơ Điều 28 vẫn được giữ trước đó; đây là lỗi chấm cần con người kiểm tra, không đủ để kết luận câu trả lời sai. Câu 17 cần tách lời khuyên kiểm tra với nghĩa vụ được điều luật quy định. Nguồn và lý do chấm lưu nguyên vẹn để rà soát.
Câu 4 có Khoản 2 Điều 328 bị kết thúc ở ‘trừ trườ’ ngay trong DOCX Data/housing_contract/Bộ-luật-91-2015-QH13-trích-tuyển.docx; nguồn được truy xuất cũng kết thúc như vậy. Đây là lỗi tài liệu đầu vào, không phải cắt prompt. Cần bổ sung từ bản gốc chính thức, nạp lại và kiểm thử câu bị ảnh hưởng; không tự điền ngoại lệ từ trí nhớ model.

Điểm Qwen chấm cũ, chỉ để lưu lịch sử và không dùng tính mức tăng: {'faithfulness': {'mean': 0.7054, 'scored': 35}, 'answer_relevancy': {'mean': 0.6866, 'scored': 36}, 'context_utilization': {'mean': 0.821, 'scored': 36}}.

### Điểm lượt sau theo mức trả lời

| Nhóm | Số câu | Faithfulness | Answer relevancy | Context utilization |
|---|---:|---:|---:|---:|
| tổng hợp | 30 | 0.6513 (n=30) | 0.7928 (n=30) | 0.6111 (n=30) |
| một phần | 5 | 0.9500 (n=5) | 0.6812 (n=5) | 0.6833 (n=5) |
| chưa đủ căn cứ | 1 | 0.0000 (n=1) | 0.0000 (n=1) | 0.0000 (n=1) |

### Các lỗi chưa được giải quyết đầy đủ

Lý do dưới đây do bước kiểm tra tự động ghi nhận, cần đọc lại nguồn để phân biệt lỗi thật với từ chối quá mức. Từ chối hoặc trích đoạn không được tính là đã giải quyết câu hỏi.

- Câu 4 (housing_contract): Kết luận hoặc số liệu chưa gắn trích dẫn trực tiếp. Nguồn [1] bị cụt câu ở cuối ('trừ trườ'), dẫn đến việc trích dẫn quy định về việc bên nhận đặt cọc từ chối bị thiếu nội dung ('trừ trường hợp có thỏa thuận khác').
- Câu 23 (real_estate_brokerage): Nguồn trích dẫn chưa nêu căn cứ cho kết luận về xử lý, bồi thường hoặc hoàn trả. Claim 1: Nguồn rank 1 chỉ nêu nghĩa vụ của 'doanh nghiệp', không đề cập trực tiếp đến 'cá nhân' hành nghề trong cùng một điều khoản như claim ngụ ý.
- Câu 26 (ecommerce_platform): Kết luận trích dẫn sai số điều và tên văn bản (Nghị định 248-2026-NĐ-CP, Điều 7 thực tế là Điều 7 theo nguồn [2] nhưng nguồn ghi là Điều 7 không kèm số hiệu Nghị định như vậy, và trích dẫn [2] tương ứng với chunk có heading 'Điều 7 — tiếp nhận và xử lý phản ánh, khiếu nại').
- Câu 31 (privacy_data): Kết luận hoặc số liệu chưa gắn trích dẫn trực tiếp.
- Câu 33 (criminal_law): Chưa đủ căn cứ tổng hợp theo nguồn được truy xuất.
- Câu 35 (criminal_law): Kết luận hoặc số liệu chưa gắn trích dẫn trực tiếp.

### Giới hạn của kết quả

- Chưa có đáp án và nhãn điều khoản độc lập: answer_correctness và context_recall chưa đo được. Faithfulness cao có thể do trả lời ngắn hoặc từ chối; phải đọc cùng mức trả lời đầy đủ.
- Bộ chấm bằng mô hình vẫn có thiên lệch; nếu Gemini cũng sinh câu trả lời thì có thêm nguy cơ thiên lệch cùng họ model. Điểm không xác nhận độ đúng pháp lý hay hiệu lực văn bản.
- Lượt sau thay cả model, truy xuất và bước kiểm tra/sửa câu trả lời; không quy toàn bộ chênh lệch cho riêng model 9B hoặc Gemini.
- Cùng nhãn chủ đề và trích dẫn đúng định dạng không chứng minh điều khoản đúng hoặc bao phủ đầy đủ tình huống. Quá tải Google ảnh hưởng độ trễ và việc chuyển sang local.

## Chi tiết từng câu

F/R/C lần lượt là Faithfulness / Answer Relevancy / Context Utilization; dấu — là chưa có điểm hợp lệ.

| Câu | Chủ đề | Trước | Sau | F/R/C trước | F/R/C sau | Provider/model sau | Lỗi chấm trước / sau |
|---|---|---|---|---|---|---|---|
| 1 | housing_contract | chưa đủ căn cứ | tổng hợp | 0.000 / 0.000 / 0.000 | 0.571 / 0.870 / 0.333 | gemini/gemini-3.5-flash-lite | - / - |
| 2 | housing_contract | một phần | tổng hợp | 1.000 / 0.000 / 1.000 | 0.400 / 0.875 / 1.000 | gemini/gemini-3.5-flash-lite | - / - |
| 3 | housing_contract | một phần | tổng hợp | 1.000 / 0.887 / 0.333 | 0.556 / 0.892 / 0.333 | gemini/gemini-3.5-flash-lite | - / - |
| 4 | housing_contract | một phần | một phần | 1.000 / 0.878 / 1.000 | 1.000 / 0.878 / 1.000 | legal-partial-extractive/- | - / - |
| 5 | electricity | tổng hợp | tổng hợp | 0.750 / 0.907 / 1.000 | 0.750 / 0.907 / 1.000 | legal-extractive/- | - / - |
| 6 | electricity | tổng hợp | tổng hợp | 1.000 / 0.873 / 1.000 | 1.000 / 0.873 / 1.000 | legal-extractive/- | - / - |
| 7 | electricity | một phần | tổng hợp | 1.000 / 0.868 / 1.000 | 0.833 / 0.960 / 1.000 | gemini/gemini-3.5-flash-lite | - / - |
| 8 | electricity | một phần | tổng hợp | 1.000 / 0.891 / 0.000 | 0.400 / 0.963 / 1.000 | gemini/gemini-3.5-flash-lite | - / - |
| 9 | water_cantho | một phần | tổng hợp | 1.000 / 0.922 / 0.500 | 0.750 / 0.957 / 0.000 | gemini/gemini-3.5-flash-lite | - / - |
| 10 | water_cantho | một phần | tổng hợp | 1.000 / 0.899 / 1.000 | 0.778 / 0.957 / 1.000 | qwen-local/qwen3.5:9b | - / - |
| 11 | water_cantho | một phần | tổng hợp | 1.000 / 0.944 / 1.000 | 0.667 / 0.940 / 1.000 | gemini/gemini-3.5-flash-lite | - / - |
| 12 | water_cantho | tổng hợp | tổng hợp | 1.000 / 0.908 / 0.833 | 0.800 / 0.929 / 1.000 | gemini/gemini-3.5-flash-lite | - / - |
| 13 | residence | một phần | tổng hợp | 1.000 / 0.000 / 0.833 | 0.500 / 0.940 / 1.000 | gemini/gemini-3.5-flash-lite | - / - |
| 14 | residence | một phần | tổng hợp | 1.000 / 0.000 / 0.000 | 0.600 / 0.000 / 0.000 | qwen-local/qwen3.5:9b | - / - |
| 15 | residence | một phần | tổng hợp | 1.000 / 0.876 / 0.000 | 0.857 / 0.976 / 0.500 | gemini/gemini-3.5-flash-lite | - / - |
| 16 | residence | một phần | tổng hợp | 1.000 / 0.879 / 0.333 | 1.000 / 0.890 / 0.500 | gemini/gemini-3.5-flash-lite | - / - |
| 17 | fire_safety | một phần | tổng hợp | 0.909 / 0.000 / 1.000 | 0.333 / 0.943 / 1.000 | gemini/gemini-3.5-flash-lite | - / - |
| 18 | fire_safety | một phần | tổng hợp | 1.000 / 0.893 / 1.000 | 0.750 / 0.970 / 1.000 | gemini/gemini-3.5-flash-lite | - / - |
| 19 | fire_safety | một phần | tổng hợp | 0.833 / 0.809 / 0.000 | 0.333 / 0.960 / 0.833 | gemini/gemini-3.5-flash-lite | - / - |
| 20 | fire_safety | một phần | tổng hợp | 1.000 / 0.862 / 1.000 | 0.800 / 0.901 / 1.000 | gemini/gemini-3.5-flash-lite | - / - |
| 21 | real_estate_brokerage | một phần | tổng hợp | 1.000 / 0.854 / 0.500 | 0.750 / 0.851 / 0.500 | gemini/gemini-3.5-flash-lite | - / - |
| 22 | real_estate_brokerage | một phần | tổng hợp | 0.700 / 0.855 / 0.000 | 0.300 / 0.943 / 0.333 | gemini/gemini-3.5-flash-lite | - / - |
| 23 | real_estate_brokerage | một phần | một phần | 1.000 / 0.855 / 1.000 | 1.000 / 0.855 / 1.000 | legal-partial-extractive/- | - / - |
| 24 | real_estate_brokerage | một phần | tổng hợp | 1.000 / 0.861 / 1.000 | 0.200 / 0.868 / 0.333 | gemini/gemini-3.5-flash-lite | - / - |
| 25 | ecommerce_platform | một phần | tổng hợp | 1.000 / 0.827 / 1.000 | 1.000 / 0.929 / 0.833 | gemini/gemini-3.5-flash-lite | - / - |
| 26 | ecommerce_platform | một phần | một phần | 1.000 / 0.837 / 0.583 | 1.000 / 0.837 / 0.583 | legal-partial-extractive/- | - / - |
| 27 | ecommerce_platform | một phần | tổng hợp | 1.000 / 0.000 / 1.000 | 1.000 / 0.932 / 1.000 | gemini/gemini-3.5-flash-lite | - / - |
| 28 | ecommerce_platform | một phần | tổng hợp | 0.786 / 0.825 / 0.000 | 1.000 / 0.000 / 0.000 | gemini/gemini-3.5-flash-lite | - / - |
| 29 | privacy_data | một phần | tổng hợp | 1.000 / 0.890 / 0.333 | 0.286 / 0.000 / 0.000 | gemini/gemini-3.5-flash-lite | - / - |
| 30 | privacy_data | một phần | tổng hợp | 1.000 / 0.881 / 0.000 | 0.857 / 0.822 / 0.000 | gemini/gemini-3.5-flash-lite | - / - |
| 31 | privacy_data | một phần | một phần | 1.000 / 0.843 / 0.000 | 0.917 / 0.837 / 0.833 | legal-partial-extractive/- | - / - |
| 32 | privacy_data | một phần | tổng hợp | — / 0.882 / 0.500 | 0.667 / 0.882 / 0.333 | gemini/gemini-3.5-flash-lite | faithfulness / - |
| 33 | criminal_law | một phần | chưa đủ căn cứ | 1.000 / 0.786 / 0.000 | 0.000 / 0.000 / 0.000 | template/- | - / - |
| 34 | criminal_law | một phần | tổng hợp | 0.667 / 0.811 / 0.500 | 0.400 / 0.854 / 0.500 | gemini/gemini-3.5-flash-lite | - / - |
| 35 | criminal_law | một phần | một phần | 0.636 / 0.000 / 0.500 | 0.833 / 0.000 / 0.000 | legal-partial-extractive/- | - / - |
| 36 | criminal_law | một phần | tổng hợp | 0.889 / 0.852 / 0.000 | 0.400 / 0.000 / 0.000 | gemini/gemini-3.5-flash-lite | - / - |

JSON giữ nguyên câu hỏi, câu trả lời, nguồn, ngữ cảnh, thời gian và lý do chặn kết luận để kiểm tra từng lỗi.

## Tài liệu kỹ thuật

- [Qwen 3.5 9B trên Ollama](https://ollama.com/library/qwen3.5:9b).
- [Gemini JSON Schema](https://ai.google.dev/gemini-api/docs/structured-output).
- [Định nghĩa Faithfulness của Ragas](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/faithfulness/).
