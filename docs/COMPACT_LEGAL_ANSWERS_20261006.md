# Sửa trả lời quá dài — kiểm thử ngày 06/10/2026

Đã cập nhật bản sửa lên FastAPI cục bộ. `/health` và `/docs` trả HTTP 200; hash năm tệp mã triển khai khớp workspace. API vẫn dùng `legal_word_v7_20261005`, `graph_rag_word_v6` và `housing_graph_word_v6`; kho Word bổ sung v8 chỉ được dùng cho lượt thử 47–49. Kiểm tra hash toàn dòng sau cập nhật xác nhận dữ liệu cũ giữ nguyên.

Đã tách cảnh báo nguồn do ứng dụng thêm khỏi phần kết luận mô hình cần kiểm chứng. Cảnh báo vẫn hiện đầy đủ; kết luận, câu hỏi tiếp theo và giới hạn do mô hình viết vẫn được kiểm tra.

Câu trả lời dự phòng dùng trích đoạn ngắn nguyên vẹn hoặc dẫn nguồn để đối chiếu. Không cắt giữa điều kiện/ngoại lệ; toàn bộ bằng chứng vẫn có cho mô hình kiểm tra.

Câu hỏi người thuê tự kiểm tra tin đăng ưu tiên hướng dẫn kiểm tra và phòng ngừa lừa đảo, không thay bằng trách nhiệm kiểm duyệt của nền tảng.

## Lượt chạy thực tế mới: chỉ câu 47–49

| Câu | Trước (ký tự) | Sau (ký tự) | Phần trả lời cuối |
|---|---:|---:|---|
| 47 | 7986 | 2070 | gemini-agent |
| 48 | 6972 | 1635 | gemini-agent |
| 49 | 10581 | 2171 | gemini-agent |

97 kiểm thử hồi quy đạt. Lượt thử dùng cùng câu hỏi và kho Word thử nghiệm, Qwen + Gemini qua proxy hiện tại; không gửi đáp án mẫu hoặc Datahouse cho Gemini.

Không có điểm khớp đáp án mẫu mới hoặc tỷ lệ đúng pháp luật mới. Chưa chạy lại toàn bộ 36 câu sau sửa mã. Các cảnh báo/thiếu nguồn còn lại:

- Câu 47: Gemini phân tích câu hỏi chưa khả dụng (ValidationError); dùng định tuyến chủ đề dự phòng.; Phản hồi chưa đáp ứng đầy đủ yêu cầu chính; đánh dấu theo nội dung thay vì provider.
- Câu 48: Gemini phân tích câu hỏi chưa khả dụng (ValidationError); dùng định tuyến chủ đề dự phòng.
- Câu 49: Phản hồi chưa đáp ứng đầy đủ yêu cầu chính; đánh dấu theo nội dung thay vì provider.

Đã thử lại cách hiển thị với 10 câu dự phòng dài của lượt cũ: tất cả không quá 3.500 ký tự, giữ nguyên cảnh báo và không cắt câu trích pháp lý. Đây là kiểm tra hiển thị ngoại tuyến, không phải chạy mới mô hình cho 36 câu.

Đối chiếu hash toàn dòng: kho đang dùng, graph, nhà trọ Datahouse và người dùng giữ nguyên. Không xóa kho, không embedding lại, không kích hoạt kho thử nghiệm.

## Câu trả lời mới để đọc

### Câu 47

Khuyến nghị người thuê tra cứu kỹ thông tin trực tuyến của bên cho thuê, cảnh giác dấu hiệu lừa đảo và không chuyển tiền trước khi xác định rõ chủ nhà [1] [2] [3].

- Khuyến nghị tìm kiếm số điện thoại và địa chỉ phòng thuê trên Google, Facebook cùng các diễn đàn để xem đánh giá và các giao dịch trước đó [2].
- Khuyến nghị khảo sát mức giá chung khu vực và cẩn trọng trước các tin đăng phòng vị trí đẹp nhưng giá rẻ bất thường hoặc thúc ép chuyển tiền giữ chỗ [1] [2] [3].
- Khuyến nghị cảnh giác với các trang sao chép thông tin, dùng tương tác ảo hoặc viện lý do chủ vắng mặt để hối thúc đặt cọc [1] [3].
- Khuyến nghị yêu cầu gặp trực tiếp, đối chiếu giấy tờ nhà và thẻ Căn cước công dân của chủ nhà trước khi chuyển bất kỳ khoản cọc nào [2] [3].

Các tài liệu trích dẫn mang tính cẩm nang mẹo vặt và cảnh báo phòng ngừa của cơ quan công an, không phải quy định pháp luật bắt buộc về quy trình xác minh [1] [2] [3].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng.
Hướng dẫn/khuyến cáo của Cổng Thông tin điện tử Bộ Công an bài Công an tỉnh Tuyên Quang; không phải điều luật. Tình huống gốc là đặt khách sạn tại Tuyên Quang. Áp dụng tham khảo cho chứng cứ giao dịch trực tuyến, không gọi là vụ thuê trọ CTU; không phải danh mục hồ sơ bắt buộc hoặc hướng dẫn soạn đơn tập thể.
Hướng dẫn/khuyến cáo của Trợ Giúp Chợ Tốt; không phải điều luật. Mẹo giao dịch, không phải điều luật. Không chứng minh hạn hoàn cọc cố định hoặc mức cọc bắt buộc; không thay thế xác minh người được ủy quyền cho thuê. Chỉ đọc phần kiểm tra, không bổ sung mẫu soạn hợp đồng.
Hướng dẫn/khuyến cáo của Cổng Thông tin điện tử Bộ Công an bài Công an TP Hải Phòng; không phải điều luật. Chỉ lấy phần thuê trọ và an toàn giao dịch; các thủ đoạn học phí, học bổng ngoài mục tiêu dự án. Không suy ra mọi tranh chấp cọc đều là tội phạm hay chắc chắn thu hồi được tiền.

Để áp dụng vào trường hợp của bạn:
- Bạn đã liên hệ trực tiếp hoặc kiểm tra giấy tờ pháp lý của người đăng tin hay chưa?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

### Câu 48

Bạn có thể báo cáo tin đăng sai lệch trực tiếp trên website của nền tảng hoặc liên hệ qua kênh trò chuyện trực tuyến và gửi email khiếu nại [1].

- Truy cập vào tin đăng cần phản ánh và bấm chọn mục Báo cáo tin đăng ở bên dưới nội dung tin [1].
- Lựa chọn lý do phù hợp như Thông tin không đúng thực tế, Lừa đảo, Trùng lặp, Không liên lạc được hoặc Hàng đã bán [1].
- Điền đầy đủ nội dung thông tin được yêu cầu cho lý do đã chọn rồi nhấn nút Gửi [1].
- Liên hệ hỗ trợ qua chức năng trò chuyện trực tuyến từ 08h-12h và 13h-17h hằng ngày hoặc gửi email kèm đường dẫn tin, lý do vi phạm cùng số điện thoại liên hệ [1].

Nền tảng khuyến khích các bên tự thương lượng hòa giải trước khi can thiệp xử lý theo cơ chế riêng [2].
Nếu hai bên không đạt được thỏa thuận giải quyết tranh chấp thì có quyền đưa vụ việc ra Tòa án nhân dân có thẩm quyền [2].

Hướng dẫn/khuyến cáo của Trợ Giúp Chợ Tốt; không phải điều luật. Đây là thao tác trên Chợ Tốt; vị trí nút có thể thay đổi. Báo cáo nền tảng không thay thế việc báo cơ quan có thẩm quyền khi có dấu hiệu chiếm đoạt.
Hướng dẫn/khuyến cáo của Trợ Giúp Chợ Tốt; không phải điều luật. Quy trình riêng của Chợ Tốt. Không phải cam kết nền tảng tự hoàn tiền cọc hoặc giải quyết mọi tranh chấp thuê nhà; một phần quy trình trên trang nói về hàng hóa khuyến mại, cần giữ đúng phạm vi.

Để áp dụng vào trường hợp của bạn:
- Bạn đang thao tác báo cáo trực tiếp trên trang web hay muốn gửi khiếu nại qua email của nền tảng?
- Tin đăng đó có dấu hiệu lừa đảo chiếm đoạt tiền đặt cọc hay chỉ sai lệch thông tin phòng trọ thực tế?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

### Câu 49

Tài liệu hiện có quy định nền tảng trung gian có chức năng đặt hàng trực tuyến phải cung cấp thông tin cần thiết hỗ trợ giải quyết tranh chấp, cung cấp công cụ tải dữ liệu và quản lý tài khoản người bán, đồng thời chưa đủ căn cứ quy định riêng cho người cho thuê trọ [1] [2].

- Cung cấp các thông tin cần thiết để hỗ trợ các bên liên quan trong quá trình giải quyết phản ánh, yêu cầu, khiếu nại và tranh chấp [1] [2].
- Cung cấp thông tin cho cơ quan nhà nước có thẩm quyền trong thời hạn 24 giờ kể từ thời điểm nhận yêu cầu phục vụ thanh tra, kiểm tra, xử lý vi phạm [2].
- Cung cấp công cụ cho người bán truy cập tài khoản để tải dữ liệu về hàng hóa, dịch vụ và hợp đồng giao kết theo thời hạn quy định [1] [2].
- Tạm ngừng hoặc chấm dứt tài khoản người bán trong thời hạn 24 giờ khi nhận được yêu cầu từ cơ quan nhà nước có thẩm quyền, hoặc thông báo trước ít nhất 05 ngày khi có lý do chính đáng [1] [2].

Chưa đủ căn cứ từ các đoạn trích để xác định trách nhiệm riêng biệt đối với thông tin của người cho thuê phòng trọ trên website rao vặt thông thường [1] [2] [3].
Quy định trích dẫn áp dụng đối với chủ quản nền tảng thương mại điện tử trung gian có chức năng đặt hàng trực tuyến theo văn bản có hiệu lực từ ngày 01 tháng 7 năm 2026 [1] [2] [4].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng.
Cần đối chiếu điều/khoản được dẫn chiếu còn thiếu; đoạn trích chưa đủ để kết luận toàn bộ điều kiện và ngoại lệ.
Văn bản TMĐT có hiệu lực 01/07/2026; phải đọc đúng loại nền tảng và điều khoản chuyển tiếp. Điều 41: hồ sơ nền tảng đã xác nhận trước 01/07/2026 được tiếp tục đến 30/06/2027.
Văn bản TMĐT có hiệu lực 01/07/2026; phải đọc đúng loại nền tảng và điều khoản chuyển tiếp. Điều 52 khoản 2: quy định xác thực điện tử áp dụng từ 01/01/2027, chưa áp dụng ở ngày 05/10/2026.

Để áp dụng vào trường hợp của bạn:
- Nền tảng đăng tin bạn đang sử dụng có chức năng đặt hàng trực tuyến hay chỉ là trang mạng xã hội, rao vặt tin phòng trọ?
- Bạn đang cần yêu cầu nền tảng cung cấp thông tin người đăng tin để giải quyết khiếu nại hay phục vụ mục đích nào khác?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.
