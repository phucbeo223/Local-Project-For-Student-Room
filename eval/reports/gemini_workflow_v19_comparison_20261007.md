# Bàn giao workflow Gemini — 07/10/2026

Đã sửa mã, chạy đủ 36 câu, 27 lượt lặp, 6 cách hỏi ngoài bộ mẫu và cập nhật API/web cục bộ. Chưa đạt mục tiêu giảm LOW tổng thể hoặc tăng HIGH. Không công bố 0 LOW.

## Kết quả và cách đọc

| Phép đo | HIGH | PARTIAL | LOW | unscored |
|---|---:|---:|---:|---:|
| Lịch sử V15, giữ nguyên | 8 | 25 | 3 | 0 |
| Đầu ra cũ / Gemini V18 | 0 | 27 | 6 | 3 |
| Đầu ra mới / Gemini V18 | 0 | 28 | 8 | 0 |

Trạng thái dịch vụ: **14 complete / 22 partial → 18 complete / 18 partial**. Nhãn đủ nội dung từ pipeline khác với mức khớp mẫu. Cả hai lượt chấm V18 dùng cùng model, hash bộ chấm, bộ tách, kiểm tra định lượng và tham chiếu. Không dùng chênh lệch V15–V18 để kết luận chatbot tốt hơn.

V17 được lưu riêng: quy tắc “không có matched ⇒ LOW” đã hạ nhãn PARTIAL do mô hình chọn, kể cả khi trả lời được ý chính. V18 bỏ phép ép nhãn này và kiểm tra nhãn tổng thể bằng lượt Gemini độc lập. HIGH vẫn yêu cầu mọi ý matched; bất nhất được thử tối đa ba lần rồi unscored. V18 có 3 lỗi giải mã trên đầu ra cũ Q32/Q36/Q47; tất cả 36 đầu ra mới chấm được. Raw output và từng lần thử đều còn trong JSON.

## Những sửa đổi có bằng chứng

- Bộ tách giữ mệnh đề kết thúc bằng dấu hai chấm, số liệu, điều kiện cha và danh sách lồng nhau; lưu nguyên văn, ID và offset. Chỉ bỏ tiêu đề thuần túy. Không có quy tắc theo ID Q24.
- Tái dựng nguyên bộ ánh xạ V15 của Q19/Q36/Q47 cho cùng các điểm/quote/giải thích đã lưu. Lời giải thích lệch chủ đề nằm trong đầu ra chọn fragment; chưa có bằng chứng ứng dụng đổi nhầm ID. Kiểm tra quote tồn tại không phát hiện lỗi ngữ nghĩa này. Xem `gemini_workflow_v19_reproductions_20261007.json`.
- Bộ chấm Gemini tách khỏi sinh, kiểm tra ngữ nghĩa từng ý và nhãn tổng thể, đọc toàn bộ đáp án, giữ raw output, ID và phản hồi thử lại. V15 và hai báo cáo baseline khớp hash ban đầu.
- Yêu cầu bao phủ lấy từ câu hỏi; kiểm tra riêng nguồn trước chọn, nguồn sau chọn và câu trả lời theo nguồn đã dẫn. Rỗng trả not_evaluated. Bổ sung điện, nước, cư trú, PCCC, tin đăng, liên kết đặt cọc và chứng cứ. Một vòng truy xuất bổ sung: tối đa hai truy vấn, tám nguồn, ngân sách khởi chạy 15 giây, không gọi mô hình thêm.
- Giữ các ý đã kiểm chứng khi sửa phần thiếu. Trạng thái có cấu trúc đi từ chọn nguồn/sinh/kiểm chứng đến API; cảnh báo xuất xứ không tự đổi complete sang partial. Nội dung thiếu hoặc điều kiện quyết định chưa rõ vẫn partial. Giao diện vẫn hiển thị cảnh báo.
- Bổ sung Word chính thức Thông tư 60/2025/TT-BCT và Nghị định 105/2025/NĐ-CP, giữ URL, hash, ngày hiệu lực, phạm vi và offset. Không PDF/OCR. Phụ lục dài có phép chọn nguyên hàng và giữ tiêu đề/cột, không cắt giữa điều kiện.
- Sửa lỗi quy tắc từ chối Điều 19 được dẫn chiếu trong nguồn Q54; không mặc định tiêu đề Điều 10 cấm dẫn Điều 19. Sửa câu phủ định “không phải danh mục hồ sơ bắt buộc” Q56; vẫn từ chối nếu cùng câu tự thêm nghĩa vụ. Q45 đã có xử lý phủ định trong workspace trước khi sửa; không áp thêm ngoại lệ khi chưa tái hiện lỗi hiện tại.
- Router không tạo Qwen/Ollama và từ chối cấu hình Qwen. Các mặc định Compose, biến provider/judge trong `.env` và `.env.example` chuyển Gemini. Nhánh tìm phòng dùng mẫu theo dữ liệu local. Các lớp/tệp lịch sử không được gọi trong workflow đo.

## Bảng từng câu

| Câu | V15 lịch sử | Cũ / Gemini V18 | Mới / Gemini V18 | Dịch vụ cũ → mới | Bao phủ nguồn / trả lời | Lượt sửa |
|---|---|---|---|---|---|---:|
| Q19 | PARTIAL | PARTIAL | PARTIAL | complete → complete | covered / covered | 1 |
| Q20 | HIGH | PARTIAL | PARTIAL | partial → complete | not_evaluated / not_evaluated | 1 |
| Q21 | PARTIAL | PARTIAL | PARTIAL | partial → complete | not_evaluated / not_evaluated | 0 |
| Q22 | HIGH | PARTIAL | PARTIAL | complete → complete | not_evaluated / not_evaluated | 1 |
| Q23 | PARTIAL | PARTIAL | PARTIAL | partial → partial | covered / covered | 0 |
| Q24 | LOW | PARTIAL | PARTIAL | partial → partial | covered / covered | 0 |
| Q25 | PARTIAL | LOW | LOW | partial → partial | covered / covered | 0 |
| Q26 | PARTIAL | PARTIAL | PARTIAL | partial → partial | covered / covered | 1 |
| Q27 | PARTIAL | PARTIAL | PARTIAL | partial → partial | not_evaluated / not_evaluated | 1 |
| Q28 | LOW | LOW | PARTIAL | partial → partial | covered / covered | 1 |
| Q29 | PARTIAL | LOW | LOW | partial → partial | covered / covered | 1 |
| Q30 | PARTIAL | PARTIAL | PARTIAL | complete → complete | covered / covered | 0 |
| Q31 | PARTIAL | PARTIAL | PARTIAL | complete → complete | covered / covered | 0 |
| Q32 | PARTIAL | UNSCORED | LOW | partial → partial | covered / covered | 0 |
| Q33 | PARTIAL | PARTIAL | PARTIAL | complete → complete | covered / covered | 0 |
| Q34 | PARTIAL | PARTIAL | LOW | partial → partial | covered / covered | 0 |
| Q35 | PARTIAL | PARTIAL | PARTIAL | complete → partial | covered / covered | 1 |
| Q36 | LOW | UNSCORED | PARTIAL | partial → partial | covered / covered | 0 |
| Q37 | HIGH | PARTIAL | PARTIAL | complete → partial | covered / covered | 0 |
| Q38 | HIGH | PARTIAL | PARTIAL | complete → complete | covered / covered | 0 |
| Q43 | HIGH | LOW | PARTIAL | partial → partial | not_evaluated / not_evaluated | 0 |
| Q44 | PARTIAL | LOW | LOW | partial → partial | not_evaluated / not_evaluated | 0 |
| Q45 | PARTIAL | PARTIAL | LOW | partial → complete | not_evaluated / not_evaluated | 0 |
| Q46 | PARTIAL | PARTIAL | PARTIAL | complete → complete | not_evaluated / not_evaluated | 0 |
| Q47 | PARTIAL | UNSCORED | PARTIAL | complete → complete | covered / covered | 0 |
| Q48 | HIGH | PARTIAL | PARTIAL | complete → complete | not_evaluated / not_evaluated | 0 |
| Q49 | PARTIAL | PARTIAL | PARTIAL | complete → partial | covered / partial | 1 |
| Q50 | HIGH | PARTIAL | PARTIAL | partial → partial | covered / covered | 0 |
| Q51 | PARTIAL | PARTIAL | PARTIAL | partial → complete | covered / covered | 0 |
| Q52 | PARTIAL | PARTIAL | LOW | complete → complete | covered / covered | 1 |
| Q53 | PARTIAL | PARTIAL | LOW | partial → complete | not_evaluated / not_evaluated | 0 |
| Q54 | PARTIAL | LOW | PARTIAL | partial → complete | covered / covered | 0 |
| Q55 | PARTIAL | PARTIAL | PARTIAL | complete → complete | covered / covered | 0 |
| Q56 | PARTIAL | PARTIAL | PARTIAL | partial → complete | covered / covered | 0 |
| Q57 | PARTIAL | PARTIAL | PARTIAL | partial → partial | not_evaluated / not_evaluated | 1 |
| Q58 | HIGH | PARTIAL | PARTIAL | partial → partial | covered / covered | 1 |

JSON `gemini_workflow_v19_comparison_20261007.json` chứa cho từng câu: ý thiếu ở nguồn/chọn nguồn/trả lời, các khác biệt tham chiếu kèm giải thích, giới hạn áp dụng, lỗi quy tắc, số lần sửa/chấm, độ trễ và token thực tế.

## Các câu ưu tiên và phần còn thiếu

- **Q24:** đã giữ 3/4 định mức cùng điều kiện kê khai, kỳ/hợp đồng, hóa đơn và hiệu lực có điều kiện. Không thêm 37,5 kWh hay biểu giá cũ để giống mẫu. Chưa xác nhận sự kiện kích hoạt điểm c khoản 5 Điều 12: PARTIAL có lý do.
- **Q28:** trả lời đủ sáu mục mức khoán, số người, kỳ thu, khoản bao gồm, thay đổi và hóa đơn; gắn nhãn khuyến nghị/thỏa thuận. Không dựng khoảng tiền “phổ biến” hoặc ngưỡng trái luật. Còn cần địa bàn/nhà cung cấp và hiệu lực biểu giá địa phương.
- **Q36:** phân biệt nhà ở, kết hợp kinh doanh và cơ sở quản lý; trả lời điện, phương tiện, lối thoát và giải pháp ngăn cháy có nguồn. Không áp cứng hai lối thoát/hai bình mỗi tầng. Kho đã có phụ lục phân loại nhưng lượt sinh chính chưa chọn đủ hàng phân loại quy mô; câu trả lời còn thiếu phần này. Cảnh báo và câu hỏi thêm không được coi là đã hoàn thành phân loại.
- **Q30/Q47/Q55:** complete ở dịch vụ, vẫn PARTIAL theo mẫu do chi tiết/khẳng định chưa trùng. **Q49:** còn phạm vi và điều kiện pháp luật mới. **Q52:** nguồn chọn cho nguyên tắc dữ liệu nhưng chưa đáp ứng ví dụ watermark/mục đích dùng bản chụp; LOW và không được bổ sung ví dụ vô căn cứ.
- **Q31/Q33:** complete ở dịch vụ nhưng chưa khớp toàn mẫu. **Q32/Q34:** LOW do thiếu phần phối hợp chủ trọ, tình huống chuyển nơi ở/cùng phường và các điều kiện thủ tục; mức phạt hoặc mốc trong mẫu vẫn cần xác minh trước khi thêm.
- **Q54:** lượt chính complete, bộ quy tắc chấp nhận các dẫn chiếu đúng; các lượt lặp vẫn LOW theo mẫu. **Q56:** giữ hướng dẫn chứng cứ/báo tin, không biến hướng dẫn thành hồ sơ bắt buộc; lượt chính và lặp PARTIAL theo mẫu.
- **Nhóm 8 HIGH cũ:** Q20/Q22/Q37/Q38/Q43/Q48/Q50/Q58 đều PARTIAL trong lượt mới/V18; đầu ra cũ/V18 cũng PARTIAL, riêng Q43 LOW. Không tuyên bố giữ tám HIGH chỉ vì baseline V15 từng gán nhãn đó.

Các LOW mới:
- **Q25**: ANSWER không trả lời đúng các bước hành động cụ thể theo REFERENCE (thiếu chốt công tơ, thiếu căn cứ xử phạt theo NĐ 134/2013/NĐ-CP và thiếu toàn bộ các kênh tiếp nhận phản ánh). Ý duy nhất liên quan là đối chiếu hóa đơn nhưng cũng thiếu chi tiết tra cứu mã khách hàng qua app EVNSPC.
- **Q29**: Câu trả lời của ANSWER không trình bày 2 phương án thỏa thuận tối ưu theo REFERENCE (chia đều theo đầu người từ hóa đơn gốc và lắp đồng hồ nước phụ từng phòng kèm cơ chế chia hao hụt/nước dùng chung). Thay vào đó, ANSWER chủ yếu đưa ra các khuyến nghị chung chung về ký kết hợp đồng, tính tiền khoán và các lưu ý pháp lý, bỏ sót hầu hết các chi tiết then chốt của REFERENCE.
- **Q32**: ANSWER không trả lời đúng trọng tâm câu hỏi theo REFERENCE. Thay vì xác định trách nhiệm phối hợp giữa chủ trọ và người thuê (sinh viên), ANSWER lại khẳng định nguồn chưa có căn cứ về trách nhiệm của bên cho thuê trọ và chuyển phần lớn trách nhiệm giấy tờ sang cho công dân (người thuê). Ngoài ra, ANSWER hoàn toàn thiếu thông tin về việc ký Tờ khai CT01 và mức phạt vi phạm hành chính.
- **Q34**: ANSWER chỉ đề cập một phần ý đăng ký tạm trú tại nơi ở mới nhưng thiếu các chi tiết chính như thời hạn 30 ngày, hình thức nộp và cơ chế tự động xóa nơi cũ. Đồng thời, ANSWER bỏ sót hoàn toàn trường hợp chuyển phòng cùng xã/phường và lưu ý về gia hạn tạm trú sau 2 năm. Do đó mức độ tương đồng tổng thể là low.
- **Q44**: ANSWER không trả lời được các ý cốt lõi của REFERENCE. Phần lớn các nội dung quan trọng về nguyên tắc không chuyển cọc trước khi xem phòng, giao dịch trực tiếp với chủ trọ và quy tắc trả phí môi giới đều bị thiếu (missing). Ý về kiểm tra quyền cho thuê chỉ được nhắc tới dưới dạng câu hỏi tình huống và chưa đầy đủ (different). Do đó mức độ phù hợp là low.
- **Q45**: ANSWER không khớp với REFERENCE: không đề cập quyền từ chối thuê và không trả phí (thậm chí ANSWER còn yêu cầu phải trả tiền công phần việc đã làm và phủ nhận quyền miễn toàn bộ phí/hoàn cọc), thiếu quyền yêu cầu hoàn trả 100% tiền đã thu, và hoàn toàn thiếu ý báo cáo nền tảng hoặc cơ quan Công an.
- **Q52**: ANSWER không trả lời đúng các nội dung cụ thể trong REFERENCE (mục đích cụ thể là quản lý phòng trọ và nộp công an đăng ký tạm trú; cấm chuyển giao/mua bán/phát tán; mẹo watermark và tác dụng ngăn chặn tài khoản ảo/vay tiền). ANSWER chỉ đưa ra các nguyên tắc xử lý dữ liệu chung chung theo luật bảo vệ dữ liệu cá nhân, làm sai lệch hoặc thiếu toàn bộ các chi tiết chính.
- **Q53**: ANSWER không trả lời đúng trọng tâm khẳng định hành vi là vi phạm pháp luật như REFERENCE mà lại diễn giải theo hướng có các trường hợp ngoại lệ được phép. Đồng thời, ANSWER hoàn toàn thiếu toàn bộ phần nội dung về chế tài xử phạt (phạt hành chính từ 10 - 20 triệu đồng và trách nhiệm bồi thường dân sự). Do đó mức độ tương thích được đánh giá là low.

Đây là lý do khớp tham chiếu, không xác nhận mọi khẳng định/định mức/thời hạn trong mẫu là pháp luật hiện hành. Giữ bản rà tham chiếu tại từng case; không sao chép các khẳng định chưa xác minh vào corpus hoặc prompt sinh.

## Ba lượt lặp

| Câu | Lần 1 | Lần 2 | Lần 3 | Trạng thái dịch vụ |
|---|---|---|---|---|
| Q24 | PARTIAL | UNSCORED | PARTIAL | partial / partial / partial |
| Q28 | PARTIAL | PARTIAL | PARTIAL | partial / partial / partial |
| Q36 | PARTIAL | PARTIAL | PARTIAL | partial / partial / partial |
| Q45 | PARTIAL | LOW | LOW | partial / complete / partial |
| Q49 | PARTIAL | PARTIAL | PARTIAL | complete / complete / complete |
| Q50 | PARTIAL | PARTIAL | PARTIAL | partial / partial / partial |
| Q52 | UNSCORED | LOW | UNSCORED | complete / partial / partial |
| Q54 | LOW | LOW | LOW | partial / complete / complete |
| Q56 | PARTIAL | PARTIAL | PARTIAL | complete / complete / complete |

27/27 lượt sinh hoàn thành, không lỗi. Có unscored ở một lượt Q24 và hai lượt Q52 do đầu ra chấm không đạt kiểm tra; không tính là đạt. Q45/Q52/Q54 có nhãn thấp hoặc dao động. Cả ba câu LOW cũ chưa được chứng minh ổn định HIGH. Sáu cách hỏi ngoài mẫu đều chạy được, đều PARTIAL; không có đáp án mẫu đưa vào bước sinh.

## Độ trễ, usage và kiểm thử

| Nhóm sinh | Số lượt | p50 | p95 | Lỗi | Model calls | Total tokens API trả về |
|---|---:|---:|---:|---:|---:|---:|
| 36 câu | 36 | 49.14s | 67.37s | 0 | 180 | 776740 |
| 27 lượt lặp | 27 | 58.65s | 70.05s | 0 | 154 | 773807 |
| 6 câu ngoài mẫu | 6 | 53.66s | 68.51s | 0 | 34 | 170870 |

Tổng sinh trong các nhóm: **368 model calls, 1,721,417 total tokens**. Warm-up tách riêng: **12 calls, 58,172 tokens**. Chấm so sánh V18 và lặp: **252 calls, 822,461 tokens**. Mỗi lượt được đối chiếu usage response, không dùng 0 thay cho thiếu. Lượt V17/pilot là chi phí bổ sung, không trộn vào phép so sánh V18.

Cùng model `gemini-3.8-flash-high` cho các bước và chấm. Lượt cũ đặt khoảng nghỉ 0 giây, lượt mới 5 giây; vì vậy không diễn giải chênh lệch độ trễ thành hiệu năng mã thuần. Benchmark đo toàn service, không gồm HTTP/auth; smoke HTTP được lưu riêng và không có telemetry model đầy đủ. Toàn bộ model-call log của các lượt mới/chấm có provider Gemini, không có Qwen/Ollama.

- 134 kiểm thử liên quan đã qua theo các lượt kiểm tra: bộ tách/ngữ nghĩa/gom nhãn, bao phủ, điều kiện/citation, selector/workflow, nguồn và telemetry; 25 kiểm thử truy xuất cũng đã qua khi dùng thư mục tạm trong workspace.
- Kiểm tra TypeScript qua; build API và web production qua.
- 5 Playwright UI tests qua, bao gồm điện thoại 390px, desktop 1280px, nguồn, cảnh báo và nội dung dài.
- Smoke HTTP Q20/Q24/Q28/Q36 và tìm phòng đều 200/pass; không xác thực bị chặn; tài khoản thử đã xóa.
- Corpus audit qua: 42 Word, 583 đoạn/vector 384 chiều, nguyên văn official Word khớp offset; graph release khớp manifest. Dữ liệu 84 người dùng và 789 tin trọ giữ nguyên digest trước/sau cập nhật.

## Phiên bản, cấu hình và tệp bàn giao

- Pipeline/prompt hash: `561055a5a24dda7874bd9e89daf61a35a918cdb5ebcc78b720f84cc9575dd301`.
- Corpus manifest hash: `0286e4e842eb012ede0ad72a790ba9bb893ab90ab8269d65f1fefa1612d48085`.
- Gemini evaluator V18 hash: `2986a4b04f444242b06e81eb0d7608883e08ed33687e36ab6e3772ca4c596c14`.
- API local đã chạy `nckh-api:workflow-v19`, web `nckh-web:workflow-v19`; hash mã trong API khớp lượt đo. Overlay `docker-compose.workflow-v19.yml` chọn rõ legal/graph/housing schema mới. Release mới vẫn staging trong catalog; không thay hay xóa các release trước.
- Ảnh khôi phục: `nckh-api:before-workflow-v19-20261007`, `nckh-web:before-workflow-v19-20261007` cùng các corpus cũ. API trước cập nhật thực tế dùng Qwen và Word V7; đó khác với baseline V18 được cung cấp để so sánh chất lượng.
- Các file API sửa từ snapshot ban đầu: `apps/api/app/room_service/chatbot/agent_workflow.py`, `apps/api/app/room_service/chatbot/answer_coverage.py`, `apps/api/app/room_service/chatbot/claim_verification.py`, `apps/api/app/room_service/chatbot/legal_retrieval.py`, `apps/api/app/room_service/chatbot/providers.py`, `apps/api/app/room_service/chatbot/repo.py`, `apps/api/app/room_service/chatbot/request_telemetry.py`, `apps/api/app/room_service/chatbot/router.py`, `apps/api/app/room_service/chatbot/schemas.py`, `apps/api/app/room_service/chatbot/service.py`, `apps/api/app/room_service/chatbot/source_selection.py`.
- Thêm `annex_context.py`; cập nhật config/provider mặc định, `ChatClient.tsx`, kiểm thử UI/API/evaluator; thêm scorer Gemini, corpus fetch/prepare/audit, benchmark/split/reproduction/report/HTTP scripts. JSON bàn giao chứa danh sách thay đổi và hash; không coi toàn bộ `git diff` là công việc mới vì workspace đã có thay đổi trước đó.

## Giới hạn còn lại

- Chưa có kết quả cho phép công bố giảm LOW tổng thể, tăng HIGH hoặc hoàn tất các câu PARTIAL. Một số mẫu đòi khẳng định/định lượng chưa xác minh; tăng điểm bằng cách viết theo mẫu sẽ không giải quyết đúng nguồn.
- Cần tăng khả năng chọn đúng hàng phụ lục PCCC, bổ sung nguồn thực cho chuyển cư trú/báo tin/watermark và kiểm tra lại từng LOW với tham chiếu đã xác minh.
- Bao phủ hiện là kiểm tra từ vựng có ràng buộc nguồn/citation, không phải chứng nhận đã đủ mọi điều kiện pháp lý. Ngân sách 15 giây kiểm tra giữa truy vấn, chưa hủy cưỡng bức truy vấn DB đang chạy.
- Một cách hỏi về kê khai “dùng điện” thiếu từ “tiền điện” đã bị router hiểu là tìm phòng; bộ hỏi ngoài mẫu dùng cách gọi “tiền điện”. Lỗi phân loại này còn cần xử lý và đo lại riêng.

Nguồn bổ sung: [Thông tư 60/2025/TT-BCT, Word Công báo](https://congbao.chinhphu.vn/van-ban/thong-tu-so-60-2025-tt-bct-46756/60185.htm), [Nghị định 105/2025/NĐ-CP, Word Công báo](https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-105-2025-nd-cp-44912/56374.htm). URL download, ngày tải, TLS, hash và phạm vi lưu trong `docs/legal_word_workflow_v19_20261007/originals/provenance.json`.
