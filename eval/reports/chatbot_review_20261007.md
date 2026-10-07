# Review chatbot: giảm LOW, tăng HIGH và cải thiện PARTIAL

Ngày review: 07/10/2026. Phạm vi: mã đang có trong workspace và kết quả 36 câu của kho v18. Đây là review, chưa sửa pipeline, đáp án tham chiếu hoặc nhãn đã công bố; chưa chạy lại mô hình.

## Kết quả làm mốc

- Nguồn: `gemini_completion_36_final_v18_v15_20261007.json` và `gemini_completion_36_final_v18_20261007.json` trong cùng thư mục.
- V15: **8 HIGH, 25 PARTIAL, 3 LOW**.
- HIGH: Q20, Q22, Q37, Q38, Q43, Q48, Q50, Q58.
- LOW: **Q24, Q28, Q36**.
- PARTIAL: Q19, Q21, Q23, Q25, Q26, Q27, Q29, Q30, Q31, Q32, Q33, Q34, Q35, Q44, Q45, Q46, Q47, Q49, Q51, Q52, Q53, Q54, Q55, Q56, Q57.
- Trạng thái dịch vụ: 14 câu không gắn partial, 22 câu gắn partial. Chỉ số này khác với nhãn V15. Ví dụ Q20 là HIGH theo V15 nhưng partial trên dịch vụ.
- Đây là số liệu lượt chạy đã lưu, không phải kết quả đo lại mã hiện tại. So sánh đáp án, độ bao phủ nguồn và tính đúng của nguồn pháp luật phải được đánh giá riêng.

## 1. [P1] Bộ tách đáp án làm mất ý chính và điều kiện của câu hỏi

Vị trí: `eval/compare_grounded_references.py:88–91`, hàm `reference_fragments`.

Mã loại mọi đoạn kết thúc bằng dấu hai chấm sau khi làm sạch định dạng. Với Q24, đoạn bị loại gồm chính mệnh đề **3 sinh viên được cấp 3/4 (75%) định mức**, cùng các dòng điều kiện kê khai và hợp đồng dưới 12 tháng. Các đoạn ví dụ 37,5 kWh và những ý phía sau vẫn được chấm. Điều này làm mất cơ hội đánh giá phần trả lời đúng trọng tâm và tách các ý con khỏi điều kiện cha.

Đã tái hiện trực tiếp bằng các hàm tách đoạn hiện tại trên đáp án gốc, không gọi mô hình. Báo cáo Q24 chỉ còn năm điểm, tất cả `different`; việc sửa tách đoạn chưa bảo đảm Q24 thành HIGH vì còn khác biệt về ví dụ và nguồn áp dụng.

**Cần sửa:** phân biệt tiêu đề thuần túy với đoạn có mệnh đề thực chất; giữ mệnh đề và gắn ngữ cảnh điều kiện cha cho các ý con. Không dùng dấu `:` làm tiêu chí duy nhất để loại đoạn. Tạo phiên bản bộ chấm mới, giữ kết quả V15 cũ.

**Kiểm tra:** Q24 phải giữ được ý 3/4 và hai nhánh điều kiện; tiêu đề giới thiệu chung vẫn có thể không tính điểm. Đáp án thiếu điều kiện không được tự coi là khớp chỉ vì có cùng con số.

## 2. [P1] Audit trích dẫn chưa phát hiện chấm lệch ý

Vị trí: `eval/compare_grounded_references.py:252–274` và bước nhận kết quả `:398–403`.

`validate_quotes` kiểm tra đoạn trích có tồn tại, tính nhất quán của chuỗi ghép và số liệu khi `matched`. Chưa có kiểm tra rằng giải thích thực sự nói về ý tham chiếu và đoạn trả lời đang được chọn. ID đúng và quote có thật không bảo đảm ý nghĩa được đối chiếu đúng.

Bằng chứng trong lượt v18, dù cả 36 câu đều qua quote audit:

- Q19: ý tham chiếu về tiền cọc được giải thích bằng thiếu đơn giá điện nước; ý chấm dứt hợp đồng được giải thích bằng thiếu thẩm quyền cho thuê.
- Q36: ý trang bị phương tiện chữa cháy được giải thích bằng thiếu tập huấn quản lý.
- Q47: ý cảnh giác giá rẻ được giải thích bằng thiếu tìm kiếm Google Hình ảnh.

Chưa có bằng chứng đây là lỗi ánh xạ ID trong Python; phần khôi phục quote lấy đúng ID. Vấn đề đã xác nhận là kết quả chấm không nhất quán về ý nghĩa vẫn được chấp nhận.

**Cần sửa:** kiểm tra riêng từng bộ `reference / selected answer / status / explanation`, đọc lại toàn câu trả lời khi gắn missing. Những điểm bất nhất cần chấm lại hoặc chuyển sang cần rà soát. Giữ raw output, ID và các lần chấm để truy vết; không tự đổi nhãn lên HIGH.

**Kiểm tra:** dùng chính các cặp lệch Q19/Q36/Q47 làm ca hồi quy; audit phải nhận diện bất nhất dù tất cả quote đều tồn tại.

## 3. [P2] PARTIAL phụ thuộc cách viết cảnh báo xuất xứ

Vị trí: `apps/api/app/room_service/chatbot/legal_retrieval.py:409–431`, được dùng tại `service.py:373` và `:424`.

Hàm `legal_completion_status` xóa một câu cảnh báo cố định rồi tìm các cụm như “chưa xác minh” trong toàn văn. Một cách diễn đạt tương đương vẫn làm câu trả lời thành partial.

Tái hiện trên Q20 đã lưu:

- Nguyên câu trả lời: `partial`.
- Chỉ bỏ dòng cảnh báo diễn đạt lại bắt đầu bằng “Nguồn là bản trích tuyển cung cấp…”: `complete`.
- Các phần nội dung trả lời giữ nguyên; cảnh báo chuẩn của ứng dụng vẫn còn. Trace cho thấy chọn nguồn complete, kiểm chứng accepted và coverage covered.

**Cần sửa:** truyền trạng thái có cấu trúc gồm mức bao phủ câu hỏi, mức xác minh nguồn và lý do thiếu. Cảnh báo xuất xứ phải tiếp tục hiển thị nhưng không được tự đồng nghĩa với thiếu nội dung. Không chỉ thay một từ khóa để hết partial; vẫn giữ partial khi thiếu ý chính hoặc thiếu điều kiện áp dụng.

**Kiểm tra:** nhiều cách diễn đạt cùng cảnh báo phải cho cùng kết quả; trường hợp thật sự thiếu nguồn/ý chính vẫn partial. Kiểm tra việc truyền `result.coverage` qua `render_answer` đến API thay vì suy lại hoàn toàn từ văn bản.

## 4. [P1] Danh sách yêu cầu rỗng vẫn được báo covered

Vị trí: `apps/api/app/room_service/chatbot/answer_coverage.py:11–56`, `:59–79`; `service.py:341–345`.

Các quy tắc hiện có chỉ nhận diện bốn nhóm: trách nhiệm nền tảng, checklist hợp đồng, môi giới thông tin sai và yêu cầu xử lý dữ liệu cá nhân. Các nhóm còn lại có thể trả danh sách yêu cầu rỗng; hàm kiểm tra trả không có ý thiếu, sau đó dịch vụ ghi `covered`.

Đã chạy các hàm hiện tại trên câu hỏi và excerpt nguồn đã lưu của **Q24/Q28/Q36/Q47/Q50/Q56**: cả sáu trả `REQUIRED_FACETS=[]`. Đây không phải chứng minh sáu câu đã đầy đủ. Việc dùng lại bộ quy tắc trên nguồn được chọn còn bỏ sót trường hợp một ý quan trọng chưa được truy xuất ngay từ đầu.

**Cần sửa:** phân biệt `not_evaluated`, `covered`, `partial`; bổ sung yêu cầu theo ý định câu hỏi cho điện, nước, cư trú, PCCC và phòng tránh lừa đảo. Tách bước kiểm tra nguồn có đủ các ý cần trả lời khỏi bước kiểm tra câu trả lời đã trình bày các ý có nguồn. Khi thiếu nguồn, thử truy xuất bổ sung có giới hạn theo đúng ý thiếu, rồi mới viết/sửa.

**Kiểm tra:** danh sách rỗng không được coi là covered. Bỏ một ý trọng tâm có nguồn khỏi câu trả lời phải tạo gap; thiếu ngay nguồn cho ý trọng tâm phải được phát hiện trước khi viết. Giữ giới hạn số lần gọi và không tự tạo dữ kiện pháp lý để lấp khoảng trống.

## Xử lý ba câu LOW

| Câu | Nguyên nhân thấy trong dữ liệu | Việc cần làm |
|---|---|---|
| Q24 – Điện cho ba sinh viên | Mất ý 3/4 khi tách đáp án; ví dụ định mức trong mẫu còn cần xác minh; kho đánh dấu hiệu lực có điều kiện | Sửa tách/chấm; bổ sung nguồn xác nhận biểu giá và mốc áp dụng trước khi tạo ví dụ tính toán. Nếu cần tính tiền thực tế, hỏi kỳ hóa đơn, mức tiêu thụ và điều kiện hợp đồng. |
| Q28 – Nước tính theo người | Câu trả lời lặp kiểm tra hợp đồng, còn chung chung; mẫu đòi các khoảng tiền và lượng tiêu thụ mà sổ rà nguồn đã đánh dấu chưa được hỗ trợ | Ưu tiên checklist mức khoán, số người tính phí, kỳ thu, khoản bao gồm và điều kiện đổi mức thu; bổ sung nguồn cho việc đối chiếu hóa đơn/cách chia. Không đưa các khoảng tiền của mẫu vào chatbot chỉ để tăng điểm. |
| Q36 – PCCC nhà nhiều phòng | Có các nhóm yêu cầu nhưng thiếu nguồn phân loại công trình; mẫu đòi định mức cụ thể còn phụ thuộc loại nhà; một số lời giải thích chấm lệch ý | Bổ sung nguồn phân loại và yêu cầu theo quy mô/công năng, kiểm tra bao phủ, nêu điều kiện ngay trong từng ý. Rà lại bộ chấm; không áp cứng số lối thoát hoặc bình chữa cháy cho mọi nhà trọ. |

Nhận xét về các điểm nguồn chưa xác minh ở bảng trên dựa vào sổ rà nội bộ `eval/datasets/external_legal_20261004/point_review_20261006.json` và `gemini_completion_source_audit_final_v18_20261007.json`; review này chưa xác minh lại pháp luật hiện hành qua nguồn bên ngoài.

## Thứ tự tăng HIGH trong nhóm PARTIAL

1. Sửa tách đoạn và kiểm tra chấm lệch trước; nếu không, số HIGH/LOW chưa đủ tin cậy để quyết định tối ưu chatbot.
2. Rà nhóm có ít điểm chưa khớp: Q30, Q47, Q49, Q52, Q55. Đây chỉ là nhóm ưu tiên kiểm tra, không phải cam kết có thể nâng tất cả lên HIGH. Ví dụ điểm còn thiếu của Q49 liên quan phạm vi/thời hạn; Q52 liên quan ví dụ ghi chú trên bản chụp; cần kiểm chứng tính cần thiết và nguồn trước khi bổ sung.
3. Bổ sung truy xuất theo ý thiếu cho nhóm cư trú Q31–Q34 và chứng cứ/báo tin Q54/Q56; chỉ thêm các ý thuộc câu hỏi và có nguồn.
4. Rà các lần giữ một phần ở Q45/Q54/Q56: trace cho thấy có ý được mô hình kiểm chứng chấp nhận nhưng bộ quy tắc từ chối. Đối chiếu lại với mã hiện tại trước khi sửa vì workspace đã có thay đổi xử lý câu phủ định/giới hạn nguồn; không mặc định đây vẫn là lỗi còn tồn tại.
5. Giữ nhóm tám câu HIGH làm kiểm tra hồi quy. Bổ sung cách hỏi khác ngoài 36 câu để tránh tối ưu riêng bộ mẫu.

## Điều kiện nghiệm thu đề xuất

- Giữ nguyên đầu ra và nhãn V15 lịch sử; mọi thay đổi bộ chấm phải có phiên bản, lý do và bảng so sánh riêng.
- Đánh giá riêng: đúng nguồn, đủ ý chính, khớp mẫu, và trạng thái chạy. Không nâng nhãn bằng cách bỏ cảnh báo hoặc tắt kiểm chứng.
- Với pipeline mới, chạy lại toàn bộ 36 câu trên cùng kho/cấu hình được ghi nhận; lặp các câu LOW và câu dễ dao động ít nhất ba lần để kiểm tra ổn định.
- Mục tiêu 0 LOW phải đạt trên bộ tiêu chí đã được kiểm tra và có nguồn; không thể khẳng định đạt trước khi sửa và đo lại. Không gây lùi chất lượng nhóm HIGH hiện có; ghi lại số lần sửa, lỗi và độ trễ.

## Cách kiểm tra trong review

- Đọc report gốc, trace từng bước và mã hiện tại; chưa chỉnh mã sản phẩm hoặc đáp án.
- Tái hiện các hàm thuần hiện tại bằng cách trích AST, dùng dữ liệu đã lưu: lọc đoạn Q24, nhận diện trạng thái Q20 và danh sách facet của sáu câu nêu trên. Không gọi dịch vụ trả phí.
- Chưa chạy kiểm thử toàn dịch vụ: Python cục bộ thiếu FastAPI và kết nối Docker bị từ chối quyền truy cập. Các tái hiện trên không thay thế kiểm thử tích hợp.
- Graph hiện có chỉ dẫn tới sơ đồ chatbot tổng quát, không chứa đủ pipeline v18; các kết luận review được đối chiếu trực tiếp từ mã và báo cáo thay vì suy từ graph cũ.
