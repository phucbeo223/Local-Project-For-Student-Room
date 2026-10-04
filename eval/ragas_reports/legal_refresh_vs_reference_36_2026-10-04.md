# Kiểm thử kho dữ liệu mới và đối chiếu 36 đáp án — 04/10/2026

Đã chạy đủ **36/36 câu** qua dịch vụ chatbot thật với kho `legal_v3_20261004`.

Khớp cao: **3** · Khớp một phần: **29** · Khớp thấp: **4**.

Câu trả lời một phần: **10** · Lỗi thực thi: **0** · Có ngữ cảnh truy xuất: **36/36** · Trung vị thời gian: **43.6 giây**.

## Giới hạn đánh giá

- Đáp án người dùng là tham chiếu nội dung, chưa phải đáp án pháp lý đã xác minh.
- Hướng dẫn cập nhật chứa chủ đề/câu hỏi tương ứng; đây là kiểm thử hồi quy sau cập nhật, không đo khả năng khái quát trên câu chưa thấy.
- Mô hình so sánh cùng họ với mô hình tổng hợp, có thể thiên lệch; nhận xét cần được đọc cùng hai đáp án.
- Không có điểm RAGAS hoặc tỷ lệ đúng pháp luật mới; nhãn high/partial/low chỉ phản ánh mức khớp văn bản.
- Danh tính mô hình bên dưới alias proxy chưa được xác minh.
- Lượt đánh giá tắt khoảng nghỉ Gemini giữa request; API giữ khoảng nghỉ 5 giây, nên thời gian đo không đại diện trực tiếp cho mọi lượt dùng giao diện.
- Câu 27 của hệ thống thêm “người bán” so với câu tham chiếu chỉ nói “người cho thuê”; ghép theo mapping đã lưu trước và ghi rõ khác biệt phạm vi.

## Đối chiếu từng câu

| Câu | Mức khớp | Nhận xét |
|---|---|---|
| 1 | Một phần | ANSWER bao phủ đầy đủ các nhóm nội dung cốt lõi của USER_REFERENCE (chủ thể, giá cả, tiền cọc, chi phí dịch vụ, tài sản, chấm dứt hợp đồng). Tuy nhiên, ANSWER thiên về trích xuất văn bản nguồn và điều luật (kèm hướng dẫn biên soạn) nên thiếu các ví dụ cụ thể và mốc thời gian ước lượng (30 ngày báo trước, 3-5 ngày trả cọc) có trong USER_REFERENCE. Mức độ đồng thuận được đánh giá là partial do cách tiếp cận nặng về trích nguồn thô. |
| 2 | Một phần | Hai phản hồi thống nhất về việc hợp đồng thuê cần ghi rõ tiền thuê, thời hạn thanh toán và quy định cách hoàn trả/mục đích cọc nếu có cọc. Tuy nhiên, mức độ đồng thuận ở mức partial vì có sự khác biệt về tính chất bắt buộc của điều khoản đặt cọc: USER_REFERENCE cho rằng bắt buộc, ANSWER giải thích đặt cọc chỉ là biện pháp bảo đảm không bắt buộc cho mọi hợp đồng. Ngoài ra ANSWER thiếu các phân tích hậu quả thực tế và lời khuyên dành cho sinh viên có trong USER_REFERENCE. |
| 3 | Một phần | Hai phản hồi cùng nhấn mạnh việc phải kiểm tra điều khoản hợp đồng về giá thuê. Tuy nhiên, USER_REFERENCE tập trung vào quyền từ chối của bên thuê khi chủ nhà tự ý tăng giá trái hợp đồng và chế tài khi bị đuổi (Điều 477 BLDS 2015). Ngược lại, ANSWER bám sát nguồn trích dẫn về trường hợp cải tạo nhà ở theo Điều 170 Luật Nhà ở và các khuyến nghị thương lượng, lập phụ lục. Do ANSWER thiếu các điểm xử lý vi phạm trong USER_REFERENCE nhưng bổ sung quy định luật định riêng biệt, mức độ tương đồng được đánh giá là partial. |
| 4 | Một phần | Cả hai câu trả lời cùng đề cập đến nguyên tắc hoàn trả tiền cọc theo Điều 328 khoản 2 BLDS 2015, việc trừ hao mòn tự nhiên và đối chiếu công nợ. ANSWER thiên về phân tích điều kiện pháp lý chung và bám sát ngữ cảnh hướng dẫn thực tế, trong khi USER_REFERENCE nêu cụ thể hơn quyền lợi/nghĩa vụ của chủ nhà và người thuê khi hết hạn hợp đồng. Có sự khác biệt về việc thông báo trước khi chấm dứt hợp đồng có mặc nhiên bảo đảm nhận lại cọc hay không. |
| 5 | Một phần | Hai văn bản có sự thống nhất về nguyên tắc cấp định mức (4 người = 1 định mức) và việc không cho phép chủ trọ tự ý nâng giá. Tuy nhiên, mức độ tương thích chỉ ở mức partial do có sự khác biệt rõ rệt về bậc giá áp dụng khi không kê khai (bậc 2 theo Thông tư 60 trong trích dẫn của ANSWER so với bậc 3 trong USER_REFERENCE) và hệ thống căn cứ văn bản quy phạm pháp luật (Thông tư 60/2025/TT-BCT kèm điều khoản chuyển tiếp so với Thông tư 25/2018/TT-BCT và Thông tư 09/2023/TT-BCT). Chưa xác minh văn bản nào đúng tại thời điểm tra cứu. |
| 6 | Một phần | Cả hai tài liệu đều thống nhất nguyên tắc tính định mức là 4 người/hộ và 3 người được tính 3/4 định mức. Tuy nhiên, mức độ đồng thuận chỉ ở mức partial vì ANSWER chủ yếu trích dẫn văn bản pháp quy mới (Thông tư 60/2025/TT-BCT với mức áp giá Bậc 2 khi không kê khai), trong khi USER_REFERENCE tính toán cụ thể theo biểu bậc thang và nêu mức áp giá Bậc 3 theo quy định cũ (Thông tư 16/2014 và Thông tư 25/2018). ANSWER cũng đưa thêm nhiều điều kiện pháp lý về hợp đồng thuê và hiệu lực chuyển tiếp. |
| 7 | Một phần | ANSWER và USER_REFERENCE đều trả lời đúng trọng tâm câu hỏi về các bước kiểm tra hóa đơn và căn cứ xử lý khi bị thu tiền điện cao hơn quy định. Tuy nhiên, hai bên khác nhau về căn cứ pháp phạt hành chính (Nghị định 133 so với Nghị định 134/17). ANSWER thiếu mức phạt tiền cụ thể (20-30 triệu đồng) và đầu mối hotline/EVNSPC cụ thể có trong USER_REFERENCE, nhưng bổ sung nhiều chi tiết kiểm tra hóa đơn theo ngữ cảnh được cung cấp. Do đó, mức độ đồng thuận là partial. |
| 8 | Thấp | ANSWER không trả lời trực tiếp câu hỏi (không khẳng định 'Có' hay 'Không') mà chỉ trích dẫn hướng dẫn thực tế tại Cần Thơ và nhận định chưa đủ căn cứ nguồn để kết luận nghĩa vụ bắt buộc chung. Toàn bộ các yêu cầu chi tiết về chốt chỉ số công tơ và các mục bắt buộc trên bảng kê thanh toán có trong USER_REFERENCE đều bị thiếu trong ANSWER. |
| 9 | Một phần | ANSWER bám sát các tiêu chí thực tế và căn cứ pháp lý tại Cần Thơ (Quyết định 215/QĐ-UBND) để trả lời câu hỏi. Tuy nhiên, ANSWER có sự đối lập đáng kể với USER_REFERENCE về việc hiểu định mức 4 m³ (theo người hay theo hộ) cũng như việc giá có tính lũy tiến bậc thang hay theo nhóm đối tượng/khu vực. Vì vậy mức độ tương đồng được đánh giá là partial. |
| 10 | Một phần | Cả hai câu trả lời đều trả lời đúng trọng tâm câu hỏi về các điểm cần kiểm tra khi thu tiền nước theo đầu người (kiểm tra hợp đồng thuê, đối chiếu hóa đơn tổng). ANSWER bám sát văn bản hướng dẫn nghiệp vụ (nhấn mạnh tính pháp lý, ngày chốt nhân khẩu, người ở không đủ tháng, giới hạn quyền đòi lắp đồng hồ). Tuy nhiên, ANSWER không đề cập đến các con số ước lượng thực tế tại địa phương (Cần Thơ) như trong USER_REFERENCE (chưa xác minh tính quy chuẩn của các con số này). Do đó mức độ tương đồng đạt partial. |
| 11 | Cao | Cả ANSWER và USER_REFERENCE đều trả lời trực tiếp câu hỏi và thống nhất về các phương án phân chia chính (theo đầu người, theo đồng hồ phụ, xử lý nước khu vực chung). ANSWER bám sát tài liệu nguồn khi bổ sung thêm các điều khoản cần có trong văn bản thỏa thuận (ngày ở, rò rỉ, kỳ tính tiền, thuế phí) và phân biệt giữa thỏa thuận nội bộ với hợp đồng dịch vụ cấp nước. USER_REFERENCE đưa ra công thức chia hóa đơn cụ thể hơn cho phương án theo đầu người. |
| 12 | Cao | Cả hai câu trả lời đều hướng dẫn phương thức cốt lõi là dùng mã khách hàng trên hóa đơn để tra cứu trên trang web của đơn vị cấp nước tại Cần Thơ. ANSWER bổ sung chi tiết quy trình pháp lý khi phát hiện sai lệch theo Nghị định 117/2007/NĐ-CP và chỉ thiếu kênh Zalo OA được nhắc trong USER_REFERENCE. |
| 13 | Một phần | ANSWER đã trả lời được câu hỏi chính bằng cách trích dẫn căn cứ pháp lý (Điều 27 Luật Cư trú) xác định thủ tục là đăng ký tạm trú khi ở từ 30 ngày trở lên. Tuy nhiên, ANSWER chỉ dừng lại ở trích dẫn nguyên văn Khoản 1 và thiếu các chi tiết bổ sung có trong USER_REFERENCE như thời hạn nộp hồ sơ (30 ngày) và thời hạn của tạm trú (tối đa 2 năm, được gia hạn), do các thông tin này cũng không có trong ngữ cảnh được cấp. |
| 14 | Một phần | ANSWER chỉ bám sát trích đoạn Điều 28 Luật Cư trú được cung cấp nên đã từ chối khẳng định trách nhiệm của chủ nhà trọ và chỉ nêu thành phần hồ sơ, quy trình. Ngược lại, USER_REFERENCE đưa ra câu trả lời trực tiếp phân chia trách nhiệm giữa chủ trọ và người thuê cùng mức phạt theo Nghị định 144/2021/NĐ-CP (vốn không nằm trong ngữ cảnh). Vì ANSWER chỉ bao phủ được phần giấy tờ hồ sơ mà thiếu câu trả lời trực tiếp về trách nhiệm của các chủ thể như reference, mức độ đồng thuận được đánh giá là partial. |
| 15 | Một phần | ANSWER và USER_REFERENCE đều trả lời đúng hai thành phần hồ sơ cơ bản theo luật là tờ khai thay đổi thông tin cư trú và hợp đồng thuê trọ/giấy tờ chứng minh chỗ ở hợp pháp. Tuy nhiên, USER_REFERENCE đưa ra chi tiết về tên mẫu (CT01), chữ ký chủ trọ, bản sao CCCD, tính chất không bắt buộc công chứng của hợp đồng và các kênh nộp hồ sơ (VNeID, Cổng dịch vụ công). ANSWER tiếp cận sát hơn với nguyên văn luật và hướng dẫn biên soạn (nêu cơ chế khai thác dữ liệu thay vì bắt buộc bản sao giấy, trường hợp người chưa thành niên), dẫn đến việc đánh giá độ tương thích ở mức partial. |
| 16 | Một phần | Hai văn bản đồng thuận ở điểm mấu chốt là khi chuyển ra ngoài nơi đăng ký tạm trú cũ thì phải đăng ký tạm trú mới. Tuy nhiên, ANSWER thiếu các chi tiết quan trọng mà USER_REFERENCE đề cập như thời hạn 30 ngày, việc tự động xóa tạm trú cũ và thủ tục điều chỉnh thông tin trên VNeID/Cổng dịch vụ công khi chuyển trọ cùng xã. Ngoài ra, cách tiếp cận xử lý khi chuyển trọ trong phạm vi xã có sự khác biệt (ANSWER phụ thuộc vào việc có trùng xã nơi thường trú hay không theo Thông tư 116/2026/TT-BCA). |
| 17 | Một phần | Cả hai câu trả lời đều cùng đề cập đến các nhóm yếu tố chính cần kiểm tra gồm lối thoát nạn, phương tiện PCCC và hệ thống điện. Tuy nhiên, USER_REFERENCE đưa ra các mẹo thực tế mang tính kỹ thuật/thao tác cụ thể (ống gen, aptomat, vạch xanh đồng hồ áp suất, chìa khóa chuồng cọp), trong khi ANSWER bám sát các điều kiện pháp lý chung của nhà ở (bếp đun nấu, sạc xe điện, kết hợp kinh doanh). Do thiếu các chi tiết kiểm tra thực tế rất đặc thù trong USER_REFERENCE, mức độ đồng thuận là partial. |
| 18 | Một phần | Cả hai nội dung đều đề cập đến các nhóm yêu cầu PCCC đối với nhà trọ như lối thoát nạn, an toàn sạc xe điện/ngăn cháy lan, phương tiện PCCC và nội quy. Tuy nhiên, ANSWER diễn giải theo khung phân loại nhà ở/cơ sở của Luật PCCC mới trong ngữ cảnh được cấp, trong khi USER_REFERENCE nêu các thông số kỹ thuật chi tiết (định mức bình chữa cháy, tối thiểu 2 lối thoát) dựa trên các nghị định và chỉ thị khác nên chỉ đạt mức tương đồng một phần (partial). |
| 19 | Một phần | ANSWER và USER_REFERENCE đồng thuận ở 2 hành động chính: thông báo/yêu cầu chủ trọ giải quyết và báo cơ quan công an/PCCC nếu tình trạng kéo dài. USER_REFERENCE có thêm giải pháp cụ thể về chìa khóa khẩn cấp (hộp đập kính) mà ANSWER không đề cập. Ngược lại, ANSWER bám sát hướng dẫn nguồn, bổ sung quy trình xử lý khẩn cấp khi có cháy (gọi 114, không quay lại lấy đồ) và cách thu thập bằng chứng. |
| 20 | Một phần | USER_REFERENCE tập trung vào các hành vi thực tế kỹ thuật cụ thể (lắp aptomat, thay bình PCCC, không câu nối bừa bãi, sạc xe điện, tắt ấm siêu tốc). ANSWER trả lời bám sát các điều luật trong nguồn (Điều 8, Điều 21 Luật PCCC và hướng dẫn biên soạn), nêu trách nhiệm tuyên truyền đôn đốc của chủ trọ và trách nhiệm tự kiểm tra, tuân thủ an toàn của người thuê. Do hai bên tiếp cận ở hai cấp độ (nguyên tắc pháp lý đối chiếu văn bản vs quy tắc thực hành chi tiết chưa xác minh), mức độ tương đồng là partial. |
| 21 | Một phần | ANSWER và USER_REFERENCE đều thống nhất về nghĩa vụ cung cấp thông tin trung thực về phòng trọ và minh bạch thông tin bên môi giới cũng như phí dịch vụ. Tuy nhiên, ANSWER diễn đạt ở cấp độ quy định khung và điều kiện hợp đồng theo tài liệu hướng dẫn (chunk 3), trong khi USER_REFERENCE liệt kê chi tiết các đề mục cụ thể (chứng chỉ hành nghề, SĐT, giá điện nước, tiền cọc...). Do ANSWER thiếu các chi tiết cụ thể này nên mức độ tương đồng được đánh giá là partial. Chưa xác minh tính chuẩn xác pháp lý giữa các chi tiết cụ thể của USER_REFERENCE và diễn giải trong ANSWER. |
| 22 | Một phần | ANSWER trả lời sát với ngữ cảnh thực tế pháp lý từ nguồn biên soạn và trích luật, đồng thời bao quát một số ý chính về xem phòng trực tiếp và kiểm tra ủy quyền. Tuy nhiên, ANSWER thiếu một số khuyến cáo phòng ngừa rủi ro cụ thể trong USER_REFERENCE như việc không chuyển phí xem phòng/giữ chỗ và trách nhiệm chi trả hoa hồng môi giới. Do có sự khác biệt về góc nhìn kiểm tra giấy tờ sở hữu và một số điểm bỏ sót, mức độ tương đồng được xếp là partial. |
| 23 | Một phần | ANSWER và USER_REFERENCE cùng đề cập đến nghĩa vụ trung thực của môi giới theo Luật Kinh doanh bất động sản và khả năng đòi/hoàn lại phí. Tuy nhiên, ANSWER thiếu các biện pháp như từ chối thuê phòng hay tố cáo công an/báo cáo nền tảng, đồng thời đưa ra góc nhìn thận trọng hơn về việc hoàn phí (không tự động hoàn phí từ mọi sai khác) thay vì khẳng định quyền tuyệt đối như USER_REFERENCE. |
| 24 | Một phần | ANSWER trả lời đúng trọng tâm câu hỏi và bao quát các nguyên tắc thỏa thuận thể hiện phí môi giới trong giấy tờ/hợp đồng dựa trên nguồn hướng dẫn biên soạn. ANSWER bao phủ được phần lớn ý cốt lõi của USER_REFERENCE (hợp đồng văn bản, mức phí, điều kiện trả và hoàn phí), nhưng đưa ra dưới dạng nguyên tắc pháp lý và khuyến nghị chung thay vì các điều khoản mẫu thực tế chi tiết như trong USER_REFERENCE. Do đó, mức độ đồng thuận được xếp loại partial. |
| 25 | Một phần | ANSWER và USER_REFERENCE cùng giải quyết câu hỏi kiểm tra người đăng và nguồn tin khi tìm phòng trọ, nhưng tiếp cận theo hai hướng khác nhau: USER_REFERENCE tập trung vào mẹo kỹ thuật (check tuổi tài khoản, Google Image search, cảnh giác giá sốc), còn ANSWER tập trung vào việc đối chiếu pháp lý/thực tế (quyền cho thuê, lưu mã tin/URL, không quá tin vào dấu xác minh theo nguồn hướng dẫn biên soạn). Do ANSWER thiếu các thủ thuật thực tế cụ thể của reference nên xếp loại partial. |
| 26 | Một phần | Hai câu trả lời tiếp cận theo hai hướng khác nhau: USER_REFERENCE hướng dẫn thao tác giả định có nút Report trực tiếp trên giao diện, trong khi ANSWER bám sát tài liệu nguồn hướng dẫn tìm kênh tiếp nhận khiếu nại qua mục hỗ trợ/quy chế hoạt động và lưu ý không mặc định nền tảng nào cũng có nút báo cáo. Cả hai cùng thống nhất việc cần gửi kèm hình ảnh bằng chứng. |
| 27 | Thấp | Đánh giá mức độ phù hợp là 'low' vì ANSWER không đưa ra câu trả lời trực tiếp về các nghĩa vụ định danh cụ thể của người cho thuê như USER_REFERENCE nêu, mà chủ yếu chỉ ra rằng tài liệu hiện có chưa đủ căn cứ (do thiếu nguyên văn khoản 1 Điều 17) và viện dẫn khung pháp lý khác (Luật 122/2025/QH15 thay vì Nghị định 52/2013/NĐ-CP). Hai câu trả lời tiếp cận vấn đề theo hai nguồn văn bản và kết luận rất khác nhau. |
| 28 | Một phần | Cả hai văn bản đều thống nhất nguyên tắc cảnh giác với liên kết lạ và tuyệt đối không cung cấp mã OTP hay mật khẩu. Tuy nhiên, ANSWER bám sát văn bản hướng dẫn thực tế (kiểm tra tên miền, tài khoản thụ hưởng, tách 3 bước quy trình) và thiếu các dấu hiệu nhận diện cụ thể mà USER_REFERENCE đưa ra (link rút gọn bit.ly, cớ nhận mã hoàn cọc, hành vi hối thúc trong 15 phút), do đó đánh giá mức độ đồng thuận là partial. |
| 29 | Một phần | ANSWER và USER_REFERENCE đồng thuận về nguyên tắc: chỉ thu thập thông tin định danh, địa chỉ phục vụ hợp đồng và cư trú, không được đòi hỏi thông tin nhạy cảm thừa thãi. Tuy nhiên, ANSWER đưa ra câu trả lời dưới dạng trích dẫn nguồn luật và tài liệu biên soạn, thiếu việc liệt kê cụ thể các trường thông tin chi tiết mà USER_REFERENCE đã nêu (CCCD, ngày sinh, mật khẩu, lịch sử duyệt web...), do đó mức độ tương đồng đạt partial. |
| 30 | Một phần | ANSWER trả lời dựa trên các nguyên tắc chung của Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 (hiệu lực từ 01/01/2026) trong SOURCES, bao quát được nguyên tắc xử lý dữ liệu theo mục đích và sự đồng ý. Tuy nhiên, ANSWER thiếu hầu hết các chi tiết thực tế và căn cứ hiện hành mà USER_REFERENCE đưa ra (Nghị định 13/2023/NĐ-CP, mục đích làm tạm trú, nghĩa vụ không chuyển giao cho bên thứ ba của chủ trọ, mẹo watermark). Do đó đánh giá mức độ đồng thuận là partial. |
| 31 | Thấp | Đánh giá mức độ đồng thuận là 'low' vì ANSWER hoàn toàn không đưa ra câu trả lời trực tiếp cho câu hỏi ('Chủ trọ có được đăng công khai... không?'), mà chỉ sao chép một loạt điều khoản của Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15. ANSWER bỏ sót toàn bộ các kết luận thực tế, căn cứ pháp lý và chế tài xử phạt (tiền phạt 10 - 20 triệu đồng, bồi thường thiệt hại) được nêu trong USER_REFERENCE. |
| 32 | Thấp | USER_REFERENCE đưa ra các bước xử lý tranh chấp thực tế gắn với tình huống cụ thể (chủ trọ đăng thông tin, lập vi bằng, tố cáo công an theo Nghị định 15/2020/NĐ-CP). Ngược lại, ANSWER đi theo hướng thực hiện quyền của chủ thể dữ liệu cá nhân (rút lại đồng ý, hạn chế xử lý) gửi Bên kiểm soát dữ liệu theo Luật Bảo vệ dữ liệu cá nhân 2025. Do ANSWER không bao phủ các giải pháp thực tế cốt lõi trong USER_REFERENCE (lập bằng chứng, khiếu nại/tố cáo cơ quan chức năng), mức độ đồng thuận được đánh giá là low (chưa xác minh bên nào đúng/tối ưu hơn theo pháp luật). |
| 33 | Một phần | ANSWER trả lời đúng trọng tâm câu hỏi về các dấu hiệu rủi ro và khuyến nghị an toàn, bám sát các tài liệu hướng dẫn và khuyến cáo của Bộ Công an. Tuy nhiên ANSWER mang tính khái quát quy chuẩn pháp lý và khuyến nghị chung, trong khi USER_REFERENCE nêu các tình huống chi tiết mang tính đời sống (mức cọc 200k-500k, bối cảnh tân sinh viên, Cần Thơ). Ngoài ra hai bên có sự nhìn nhận khác nhau về việc kết luận ngay tội danh lừa đảo. |
| 34 | Cao | Cả hai nội dung đều trả lời trực tiếp và đầy đủ hai ý của câu hỏi: các bằng chứng cần lưu (chứng từ chuyển khoản, tin nhắn, link/bài đăng) và nơi trình báo (cơ quan Công an, liên hệ ngân hàng). USER_REFERENCE đưa ra ví dụ cụ thể về đơn vị tại địa phương (Cần Thơ), trong khi ANSWER nêu thẩm quyền chung theo nguồn (Công an gần nhất hoặc cơ quan có thẩm quyền) và bổ sung thủ tục lập biên bản tiếp nhận. |
| 35 | Một phần | ANSWER trả lời đúng bản chất phân biệt giữa tranh chấp dân sự và dấu hiệu lừa đảo hình sự dựa trên nguồn hướng dẫn biên soạn. Tuy nhiên, so với USER_REFERENCE, ANSWER thiếu các thông tin chi tiết về thẩm quyền cơ quan giải quyết (Tòa án nhân dân cấp quận/huyện vs Cơ quan CSĐT/Công an) cũng như các ví dụ mô tả cụ thể về phòng ảo/bỏ trốn ngay sau khi nhận tiền. Do đó mức độ phù hợp được đánh giá là partial. |
| 36 | Một phần | ANSWER trả lời được các loại thông tin, chứng cứ cần lưu giữ và cung cấp (tin nhắn, chứng từ chuyển tiền, trình báo công an) dựa trên nguồn khuyến cáo của Bộ Công an. Tuy nhiên, ANSWER thiếu các hướng dẫn cụ thể mà USER_REFERENCE đưa ra dành riêng cho tình huống 'nhiều người cùng bị hại' như: lập đơn tố giác tập thể, danh sách từng người kèm số tiền thiệt hại, viện dẫn Điều 174 BLHS và xác định thẩm quyền công an cấp quận/huyện. Do đó mức độ tương đồng đạt partial. |

## Câu 1: Trước khi ký hợp đồng thuê trọ, sinh viên nên kiểm tra những điều khoản nào?

### Chatbot với dữ liệu mới

Các đoạn trả lời trực tiếp trong nguồn:

- Hướng dẫn thực tế: CHỦ ĐỀ: Hợp đồng thuê và tiền cọc — Q: Trước khi ký hợp đồng thuê trọ, sinh viên nên kiểm tra những điều khoản nào?: “HƯỚNG DẪN BIÊN SOẠN — không phải nguyên văn điều luật.
### Q: Trước khi ký hợp đồng thuê trọ, sinh viên nên kiểm tra những điều khoản nào?

A: Kiểm tra người có quyền cho thuê, đúng phòng và hiện trạng bàn giao; giá thuê, kỳ trả tiền, các khoản điện/nước/dịch vụ; thời hạn thuê, sửa chữa, chấm dứt và bàn giao. Hợp đồng về nhà ở phải lập thành văn bản theo Điều 163; thuê nhà không bắt buộc công chứng, chứng thực nếu các bên không có nhu cầu theo khoản 2 Điều 164. Nếu có cọc, ghi mục đích bảo đảm, số tiền, điều kiện xử lý và thời hạn hoàn trả được thỏa thuận.

**Khuyến nghị thực tế:** Lập phụ lục tài sản, ảnh hiện trạng và chỉ số công tơ khi nhận phòng; mỗi bên giữ một bản hợp đồng đã điền đủ thông tin.

**Căn cứ:**

- [Văn bản hợp nhất 79/VBHN-VPQH — Luật Nhà ở](https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-79-vbhn-vpqh-469209.htm) — Điều 160, 161, 163, 164.
- [Bộ luật Dân sự 91/2015/QH13](https://datafiles.chinhphu.vn/cpp/files/vbpq/2016/01/91.signed.pdf) — Điều 328, 472–482.” [1].

- 2026_204_79_VBHN-VPQH — Điều 164. Công chứng, chứng thực hợp đồng và thời điểm có hiệu lực của hợp đồng về nhà ở: “1. Trường hợp mua bán, thuê mua, tặng cho, đổi, góp vốn, thế chấp nhà ở thì phải thực hiện công chứng hoặc chứng thực hợp đồng, trừ trường hợp quy định tại khoản 2 Điều này.

Đối với giao dịch quy định tại khoản này thì thời điểm có hiệu lực của hợp đồng là thời điểm hoàn thành việc công chứng hoặc chứng thực theo quy định của pháp luật về công chứng, chứng thực.

2. Trường hợp tổ chức tặng cho nhà tình nghĩa, nhà tình thương, nhà đại đoàn kết; mua bán, thuê mua nhà ở thuộc tài sản công; mua bán, thuê mua nhà ở mà một bên là tổ chức, bao gồm: nhà ở xã hội, nhà ở cho lực lượng vũ trang nhân dân, nhà ở phục vụ tái định cư; góp vốn bằng nhà ở mà có một bên là tổ chức; thuê, mượn, ở nhờ, ủy quyền quản lý nhà ở thì không phải thực hiện công chứng, chứng thực hợp đồng, trừ trường hợp các bên có nhu cầu.

Đối với giao dịch quy định tại khoản này thì thời điểm có hiệu lực của hợp đồng là do các bên thỏa thuận; trường hợp các bên không có thỏa thuận thì thời điểm có hiệu lực của hợp đồng là thời điểm ký kết hợp đồng.

3. Văn bản thừa kế nhà ở được công chứng hoặc chứng thực theo quy định của pháp luật về dân sự.

4. Việc công chứng hợp đồng về nhà ở được thực hiện tại tổ chức hành nghề công chứng; việc chứng thực hợp đồng về nhà ở được thực hiện tại Ủy ban nhân dân cấp xã nơi có nhà ở.

Mục 2

MUA BÁN NHÀ Ở” [2].

- Bo-luat-91-2015-QH13-doi-chieu-20261003 — Điều 398. Nội dung của hợp đồng: “1. Các bên trong hợp đồng có quyền thỏa thuận về nội dung trong hợp đồng.

2. Hợp đồng có thể có các nội dung sau đây:
a) Đối tượng của hợp đồng;
b) Số lượng, chất lượng;
c) Giá, phương thức thanh toán;
d) Thời hạn, địa điểm, phương thức thực hiện hợp đồng;
đ) Quyền, nghĩa vụ của các bên;
e) Trách nhiệm do vi phạm hợp đồng;
g) Phương thức giải quyết tranh chấp.” [3].

- Bo-luat-91-2015-QH13-doi-chieu-20261003 — Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp: “Điều 117. Điều kiện có hiệu lực của giao dịch dân sự | Khoản 1
1. Giao dịch dân sự có hiệu lực khi có đủ các điều kiện sau đây:
a) Chủ thể có năng lực pháp luật dân sự, năng lực hành vi dân sự phù hợp với giao dịch dân sự được xác lập;
b) Chủ thể tham gia giao dịch dân sự hoàn toàn tự nguyện;
c) Mục đích và nội dung của giao dịch dân sự không vi phạm điều cấm của luật, không trái đạo đức xã hội.

Điều 117. Điều kiện có hiệu lực của giao dịch dân sự | Khoản 2
2. Hình thức của giao dịch dân sự là điều kiện có hiệu lực của giao dịch dân sự trong trường hợp luật có quy định.

Điều 689. Hiệu lực thi hành
Điều 689. Hiệu lực thi hành
Bộ luật này có hiệu lực thi hành từ ngày 01 tháng 01 năm 2017.
Bộ luật dân sự số 33/2005/QH11 hết hiệu lực kể từ ngày Bộ luật này có hiệu lực.

Điều 688. Điều khoản chuyển tiếp | Khoản 1
1. Đối với giao dịch dân sự được xác lập trước ngày Bộ luật này có hiệu lực thì việc áp dụng pháp luật được quy định như sau:
a) Giao dịch dân sự chưa được thực hiện mà có nội dung, hình thức khác với quy định của Bộ luật này thì chủ thể giao dịch tiếp tục thực hiện theo quy định của Bộ luật dân sự số 33/2005/QH11 và các văn bản quy phạm pháp luật quy định chi tiết Bộ luật dân sự số 33/2005/QH11, trừ trường hợp các bên của giao dịch dân sự có thỏa thuận về việc sửa đổi, bổ sung nội dung, hình thức của giao dịch để phù hợp với Bộ luật này và để áp dụng quy định của Bộ luật này.
Giao dịch dân sự đang được thực hiện mà có nội dung, hình thức khác với quy định của Bộ luật này thì áp dụng quy định của Bộ luật dân sự số 33/2005/QH11 và các văn bản quy phạm pháp luật quy định chi tiết Bộ luật dân sự số 33/2005/QH11;
b) Giao dịch dân sự chưa được thực hiện hoặc đang được thực hiện mà có nội dung và hình thức phù hợp với quy định của Bộ luật này thì áp dụng quy định của Bộ luật này;
c) Giao dịch dân sự được thực hiện xong trước ngày Bộ luật này có hiệu lực mà có tranh chấp thì áp dụng quy định của Bộ luật dân sự số 33/2005/QH11 và các văn bản quy phạm pháp luật quy định chi tiết Bộ luật dân sự số 33/2005/QH11 để giải quyết;
d) Thời hiệu được áp dụng theo quy định của Bộ luật này.

Điều 688. Điều khoản chuyển tiếp | Khoản 2
2. Không áp dụng Bộ luật này để kháng nghị theo thủ tục giám đốc thẩm, tái thẩm đối với vụ việc mà Tòa án đã giải quyết theo quy định của pháp luật về dân sự trước ngày Bộ luật này có hiệu lực.” [4].

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng, hiệu lực và bản gốc.

### Đáp án bạn gửi

Khi kiểm tra hợp đồng thuê trọ, sinh viên cần rà soát kỹ 6 nhóm điều khoản cốt lõi sau:
1. **Thông tin các bên & quyền sở hữu:** Tên, CCCD của chủ nhà hoặc người được ủy quyền hợp pháp; địa chỉ chính xác của phòng trọ.
2. **Giá thuê và phương thức thanh toán:** Tiền thuê cố định trong bao lâu? Ngày đóng tiền hàng tháng? Hình thức chuyển khoản hay tiền mặt?
3. **Tiền đặt cọc và điều kiện hoàn cọc:** Số tiền cọc (thường 1 tháng), điều kiện để nhận lại 100% cọc khi hết hạn hợp đồng, và thời hạn chủ nhà phải hoàn trả (ví dụ: trong vòng 3–5 ngày sau khi bàn giao phòng).
4. **Chi phí phát sinh:** Đơn giá điện (VNĐ/kWh), nước (VNĐ/người hoặc VNĐ/m³), internet, rác, gửi xe, phí dịch vụ chung.
5. **Hiện trạng tài sản & sửa chữa:** Biên bản bàn giao liệt kê chi tiết bóng đèn, vòi nước, máy lạnh, quạt, khóa cửa; quy định bên nào chịu phí bảo trì hao mòn tự nhiên.
6. **Chấm dứt hợp đồng trước hạn:** Thời gian phải báo trước (thường 30 ngày) để không bị mất cọc nếu muốn chuyển đi sớm.

### Nhận xét đối chiếu

**Ý khớp:**

- Kiểm tra thông tin chủ thể có quyền cho thuê và đối tượng phòng/địa chỉ thuê.
- Kiểm tra giá thuê, kỳ trả tiền/ngày đóng tiền và các chi phí điện, nước, dịch vụ phát sinh.
- Kiểm tra điều khoản về tiền đặt cọc (số tiền, điều kiện xử lý, thời hạn hoàn trả).
- Kiểm tra hiện trạng bàn giao tài sản và thỏa thuận về nghĩa vụ sửa chữa/bảo trì.
- Kiểm tra quy định về thời hạn thuê và chấm dứt hợp đồng.

**Thiếu so với đáp án:**

- Chi tiết cụ thể: số tiền cọc thông thường (1 tháng), thời hạn hoàn cọc cụ thể (3–5 ngày sau bàn giao).
- Chi tiết ví dụ cụ thể về chi phí: đơn giá điện (VNĐ/kWh), nước (VNĐ/người hoặc m³), internet, rác, gửi xe.
- Quy định thời hạn báo trước khi chấm dứt hợp đồng trước hạn để không mất cọc (thường 30 ngày).

**Nội dung thêm:**

- Căn cứ pháp lý về hình thức: hợp đồng nhà ở phải lập thành văn bản theo Điều 163 Luật Nhà ở, không bắt buộc công chứng/chứng thực nếu không có nhu cầu (khoản 2 Điều 164).
- Khuyến nghị thực tế: lập phụ lục tài sản, chụp ảnh hiện trạng và ghi chỉ số công tơ khi nhận phòng; mỗi bên giữ một bản hợp đồng đã điền đủ thông tin.
- Trích dẫn quy định chung của Bộ luật Dân sự về nội dung hợp đồng (Điều 398) và điều kiện có hiệu lực (Điều 117).

**Giới hạn nguồn:**

- Đoạn trả lời đầu tiên trong ANSWER lấy từ mục 'HƯỚNG DẪN BIÊN SOẠN — không phải nguyên văn điều luật' (housing_contract), cần phân biệt giữa gợi ý biên soạn thực tế và điều luật nguyên văn.
- ANSWER trích dẫn nguyên văn dài các điều luật về điều khoản chuyển tiếp (Điều 688, 689 BLDS 2015) và thủ tục công chứng mua bán/thừa kế không trực tiếp trả lời câu hỏi thực tế của sinh viên khi thuê trọ.


## Câu 2: Hợp đồng thuê phòng có cần ghi rõ tiền cọc, tiền thuê và ngày thanh toán không?

### Chatbot với dữ liệu mới

Hợp đồng thuê phòng cần ghi rõ giá thuê, thời hạn và phương thức thanh toán, còn tiền cọc không bắt buộc phải có trong mọi hợp đồng nhưng nếu có thỏa thuận thì cần ghi nhận cụ thể [3].

- Xác định rõ ràng giá thuê phòng, thời hạn thanh toán và phương thức thanh toán vào hợp đồng [3].
- Xác định rõ mục đích đặt cọc là để bảo đảm giao kết hay thực hiện hợp đồng nếu hai bên có thỏa thuận tiền cọc [3].
- Quy định cụ thể cách thức hoàn trả tiền cọc, các trường hợp khấu trừ và lập chứng từ nhận tiền đầy đủ [3].
- Khuyến nghị ghi rõ ngày đến hạn thanh toán, tài khoản nhận tiền và phân biệt rõ tiền cọc, tiền thuê trả trước với phí dịch vụ [3].

Đặt cọc chỉ là biện pháp bảo đảm theo Bộ luật Dân sự chứ không phải điều kiện bắt buộc của mọi hợp đồng thuê phòng [3].

Để áp dụng vào trường hợp của bạn:
- Hợp đồng thuê phòng của bạn hiện đã có điều khoản về tiền đặt cọc chưa?
- Các bên dự định thanh toán tiền thuê theo kỳ hạn và phương thức nào?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

### Đáp án bạn gửi

**Rất cần thiết và bắt buộc phải ghi rõ.** 
Theo Điều 472 và Điều 473 Bộ luật Dân sự 2015, hợp đồng thuê tài sản là sự thỏa thuận giữa các bên. Việc ghi rõ:
- **Tiền đặt cọc:** Là biện pháp bảo đảm thực hiện nghĩa vụ theo Điều 328 BLDS 2015. Hợp đồng phải ghi rõ mục đích cọc, mức cọc và điều kiện hoàn trả cọc.
- **Tiền thuê:** Tránh việc chủ trọ tự ý tăng giá bất ngờ.
- **Ngày thanh toán:** Xác định mốc thời gian để người thuê không bị coi là chậm trễ nghĩa vụ thanh toán hoặc bị phạt tiền trễ hạn vô lý.
*Lưu ý:* Sinh viên tuyệt đối không ký các mẫu hợp đồng để trống mục tiền cọc hoặc chỉ thỏa thuận miệng về chi phí.

### Nhận xét đối chiếu

**Ý khớp:**

- Cần ghi nhận rõ giá/tiền thuê phòng và thời hạn/ngày thanh toán trong hợp đồng.
- Đặt cọc là biện pháp bảo đảm (theo Bộ luật Dân sự); nếu có thì cần nêu rõ mục đích và điều kiện/cách thức hoàn trả.

**Thiếu so với đáp án:**

- Việc dẫn chiếu cụ thể Điều 472, Điều 473 và Điều 328 BLDS 2015.
- Lý do ghi rõ tiền thuê nhằm tránh việc chủ trọ tự ý tăng giá bất ngờ.
- Lý do ghi rõ ngày thanh toán để tránh bị coi là chậm trễ nghĩa vụ thanh toán hoặc bị phạt vô lý.
- Lưu ý đối với sinh viên không ký hợp đồng để trống tiền cọc hoặc thỏa thuận miệng.

**Nội dung khác:**

- Về tính bắt buộc của tiền cọc: USER_REFERENCE khẳng định việc ghi rõ tiền cọc là 'rất cần thiết và bắt buộc phải ghi rõ', trong khi ANSWER nêu tiền cọc không bắt buộc phải có trong mọi hợp đồng thuê phòng (chỉ cần ghi nhận nếu hai bên có thỏa thuận).

**Nội dung thêm:**

- Nêu rõ quy định phương thức thanh toán, tài khoản nhận tiền và phân biệt tiền cọc với tiền thuê trả trước, phí dịch vụ.
- Lập chứng từ nhận tiền và quy định các trường hợp khấu trừ tiền cọc.

**Giới hạn nguồn:**

- Nguồn chunk [3] là Hướng dẫn biên soạn (editorial guidance), không phải nguyên văn điều luật.
- Trích dẫn Điều 163 Luật Nhà ở tại chunk [2] chỉ trích đoạn khoản 3; chi tiết về thời hạn, phương thức thanh toán lấy từ phần hướng dẫn biên soạn.


## Câu 3: Nếu chủ trọ muốn tăng giá thuê giữa thời hạn hợp đồng thì cần xem xét những gì?

### Chatbot với dữ liệu mới

Khi chủ trọ muốn tăng giá thuê giữa thời hạn hợp đồng, các bên cần xem xét điều khoản về giá, điều kiện điều chỉnh, thỏa thuận sửa đổi hợp đồng hoặc tình huống cải tạo nhà ở đáp ứng đủ điều kiện theo quy định [1] [2].

- Trước hết kiểm tra kỹ điều khoản về giá thuê, các điều kiện điều chỉnh giá và thỏa thuận sửa đổi hợp đồng đã ký kết [1].
- Kiểm tra tình huống bên cho thuê cải tạo nhà ở khi có sự đồng ý của bên thuê và thời gian thuê còn lại từ một phần ba thời hạn hợp đồng trở xuống để xác định quyền điều chỉnh giá [1] [2].
- Thỏa thuận giá thuê mới với chủ trọ, trường hợp không đạt thỏa thuận trong tình huống cải tạo nêu trên thì bên cho thuê có quyền đơn phương chấm dứt hợp đồng và phải bồi thường [1] [2].
- Khuyến nghị yêu cầu chủ trọ thông báo mức tăng và căn cứ bằng văn bản, lưu giữ hợp đồng cùng chứng từ trả tiền [1].
- Khuyến nghị thương lượng lập phụ lục hợp đồng nếu các bên thống nhất được mức giá thuê mới [1].

Quy định điều chỉnh giá do cải tạo nhà ở chỉ áp dụng khi có sự đồng ý của bên thuê và thời hạn thuê còn lại từ một phần ba trở xuống, nhưng nguồn chưa loại trừ các căn cứ điều chỉnh khác [1] [2].
Cần kiểm tra đúng từng tình huống thực tế của hợp đồng trước khi kết luận việc tăng giá có hợp pháp hay không [1].

Để áp dụng vào trường hợp của bạn:
- Hợp đồng thuê phòng của bạn có quy định cụ thể về việc điều chỉnh giá giữa thời hạn không?
- Chủ trọ tăng giá vì lý do cải tạo nhà ở hay do nguyên nhân nào khác?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

### Đáp án bạn gửi

Theo quy định tại Luật Nhà ở 2023 và Bộ luật Dân sự 2015:
1. **Kiểm tra điều khoản thỏa thuận trong hợp đồng:** Trong thời hạn hợp đồng còn hiệu lực, bên cho thuê **không được quyền tự ý điều chỉnh tăng giá thuê** trừ trường hợp trong hợp đồng có điều khoản cho phép tăng giá theo định kỳ hoặc có thỏa thuận trước.
2. **Nếu hợp đồng không quy định việc tăng giá:** Chủ trọ đơn phương tăng giá là **vi phạm hợp đồng**. Người thuê có quyền từ chối mức tăng này và tiếp tục đóng mức giá cũ đến hết thời hạn hợp đồng.
3. **Nếu chủ trọ ép buộc hoặc đòi đuổi người thuê:** Đây là hành vi vi phạm nghĩa vụ bàn giao và duy trì tài sản thuê (Điều 477 BLDS 2015). Người thuê có quyền yêu cầu hoàn trả cọc và bồi thường thiệt hại (nếu có).

### Nhận xét đối chiếu

**Ý khớp:**

- Cần kiểm tra kỹ các điều khoản về giá thuê và điều kiện/thỏa thuận điều chỉnh giá trong hợp đồng đã ký.

**Thiếu so với đáp án:**

- Nếu hợp đồng không quy định việc tăng giá thì việc tự ý tăng giá là vi phạm hợp đồng; người thuê có quyền từ chối và tiếp tục trả theo giá cũ.
- Trường hợp chủ trọ ép buộc hoặc đòi đuổi người thuê là vi phạm nghĩa vụ bàn giao và duy trì tài sản thuê (Điều 477 BLDS 2015), người thuê có quyền đòi lại cọc và yêu cầu bồi thường thiệt hại.

**Nội dung khác:**

- USER_REFERENCE khẳng định chủ trọ tuyệt đối không được tự ý tăng giá nếu không có thỏa thuận trước; trong khi ANSWER nêu trường hợp luật định cho phép điều chỉnh giá khi cải tạo nhà ở có sự đồng ý của bên thuê và thời hạn còn lại từ một phần ba trở xuống (nếu không thỏa thuận được giá mới thì bên cho thuê có quyền đơn phương chấm dứt kèm bồi thường).

**Nội dung thêm:**

- Căn cứ điều chỉnh giá theo luật định: trường hợp bên cho thuê cải tạo nhà ở có sự đồng ý của bên thuê và thời hạn thuê còn lại từ 1/3 trở xuống.
- Khuyến nghị thực tế: yêu cầu chủ trọ thông báo mức tăng và căn cứ bằng văn bản, lưu giữ hợp đồng, chứng từ thanh toán và lập phụ lục hợp đồng nếu thống nhất giá mới.

**Giới hạn nguồn:**

- Đoạn trích chunk 455 là tài liệu hướng dẫn biên soạn, không phải nguyên văn điều luật.
- Quy định về việc điều chỉnh giá do cải tạo nhà ở (Điều 170 khoản 2 Luật Nhà ở) yêu cầu đồng thời hai điều kiện: có sự đồng ý của bên thuê và thời hạn còn lại từ 1/3 trở xuống.


## Câu 4: Khi trả phòng, việc hoàn lại tiền cọc được xác định theo hợp đồng và quy định như thế nào?

### Chatbot với dữ liệu mới

Việc hoàn trả tiền cọc khi trả phòng phụ thuộc vào mục đích đặt cọc, các điều khoản đã thống nhất, phương thức chấm dứt hợp đồng và việc đối chiếu hiện trạng cùng công nợ [1].

- Rà soát lại thỏa thuận về tiền cọc và căn cứ chấm dứt hợp đồng theo quy định xử lý cọc tại Điều 328 khoản 2 Bộ luật Dân sự 2015 [1].
- Kiểm tra hiện trạng phòng khi bàn giao để phân biệt hao mòn tự nhiên với trách nhiệm tài sản trả lại theo Điều 482 Bộ luật Dân sự 2015 [1].
- Khuyến nghị các bên lập biên bản trả phòng, thống nhất bảng công nợ cùng các khoản khấu trừ có chứng cứ rõ ràng [1].
- Khuyến nghị ghi nhận cụ thể thời hạn hoặc ngày hoàn trả số dư tiền cọc còn lại trong biên bản làm việc [1].

Việc thông báo trước đủ thời gian không tự động bảo đảm được hoàn trả toàn bộ tiền cọc nếu việc chấm dứt hợp đồng thiếu căn cứ phù hợp [1].
Quy định xử lý tiền cọc tại Điều 328 khoản 2 Bộ luật Dân sự 2015 vẫn ưu tiên áp dụng theo thỏa thuận khác của các bên nếu có [1].

Để áp dụng vào trường hợp của bạn:
- Hợp đồng thuê phòng của bạn có điều khoản riêng nào về việc khấu trừ hay trả lại tiền cọc không?
- Lý do bạn trả phòng là do hết hạn hợp đồng hay chủ động chấm dứt trước hạn?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

### Đáp án bạn gửi

Căn cứ theo **Khoản 2 Điều 328 Bộ luật Dân sự 2015**:
- Khi hợp đồng thuê chấm dứt đúng thời hạn, bên thuê đã thanh toán đủ tiền nhà, điện nước và bàn giao lại phòng theo đúng hiện trạng (trừ hao mòn tự nhiên), thì **chủ nhà có nghĩa vụ hoàn trả lại toàn bộ số tiền đặt cọc cho người thuê**.
- Chủ nhà chỉ có quyền khấu trừ cọc khi: Người thuê làm hư hỏng tài sản do lỗi chủ quan, nợ tiền nhà/điện nước chưa trả, hoặc đơn phương chấm dứt hợp đồng trái với thời gian báo trước đã cam kết.
- **Kinh nghiệm:** Sinh viên nên chụp ảnh/quay video phòng lúc nhận phòng và lúc dọn đi để làm bằng chứng đối chiếu.

### Nhận xét đối chiếu

**Ý khớp:**

- Việc xử lý và hoàn trả tiền cọc căn cứ theo quy định tại Khoản 2 Điều 328 Bộ luật Dân sự 2015.
- Cần kiểm tra, đối chiếu hiện trạng tài sản khi trả phòng và phân biệt với hao mòn tự nhiên.
- Việc hoàn trả cọc gắn liền với việc đối chiếu công nợ và các khoản khấu trừ hư hỏng/nghĩa vụ tài chính.

**Thiếu so với đáp án:**

- Khẳng định rõ nghĩa vụ cụ thể của chủ nhà: phải hoàn trả lại toàn bộ tiền đặt cọc nếu hợp đồng chấm dứt đúng hạn, thanh toán đủ tiền nhà/điện nước và bàn giao đúng hiện trạng.
- Kinh nghiệm chụp ảnh/quay video hiện trạng phòng lúc nhận và lúc rời đi làm bằng chứng.

**Nội dung khác:**

- Điều kiện khấu trừ cọc: USER_REFERENCE cho rằng đơn phương chấm dứt hợp đồng đúng thời hạn báo trước đã cam kết thì không bị trừ cọc; ANSWER nêu rằng việc thông báo trước đủ thời gian không tự động bảo đảm được hoàn trả toàn bộ cọc nếu chấm dứt thiếu căn cứ phù hợp (chưa xác minh quan điểm nào đúng theo luật thực định).

**Nội dung thêm:**

- Căn cứ Điều 482 Bộ luật Dân sự 2015 về trách nhiệm đối với tài sản thuê trả lại.
- Ưu tiên thỏa thuận khác của các bên theo Điều 328 khoản 2 BLDS 2015.
- Khuyến nghị lập biên bản trả phòng, ghi rõ thời hạn/ngày hoàn trả số dư cọc còn lại.

**Giới hạn nguồn:**

- Đoạn trích nguồn là tài liệu hướng dẫn biên soạn thực tế (editorial guidance), không phải nguyên văn các điều luật trích dẫn (Điều 328, 482 BLDS; Điều 171, 172 Luật Nhà ở).


## Câu 5: Chủ trọ được thu tiền điện của người thuê như thế nào theo quy định?

### Chatbot với dữ liệu mới

Các đoạn trả lời trực tiếp trong nguồn:

- Hướng dẫn thực tế: CHỦ ĐỀ: Tiền điện phòng trọ — Q: Chủ trọ được thu tiền điện của người thuê như thế nào theo quy định?: “HƯỚNG DẪN BIÊN SOẠN — không phải nguyên văn điều luật.
### Q: Chủ trọ được thu tiền điện của người thuê như thế nào theo quy định?

A: Tiền điện sinh hoạt của người thuê phải đối chiếu loại hợp đồng mua điện, số người hoặc hộ được kê khai, công tơ, kỳ ghi số và biểu giá có hiệu lực ở kỳ đó. Thông tư 60 quy định tại khoản 5 Điều 12, nhưng điểm c dành cho sinh viên/người lao động chịu mốc hiệu lực riêng theo Điều 21; Điều 20 giữ quy định cũ tương ứng trong chuyển tiếp. Vì vậy phải xác nhận mốc điều chỉnh giá bình quân với đơn vị điện lực trước khi chọn nhánh tính giá; không mặc nhiên áp một mức đồng/kWh do chủ trọ tự đặt.

**Khuyến nghị thực tế:** Xin bảng tính có sản lượng, định mức, đơn giá, thuế và khoản riêng; hỏi điện lực quản lý địa chỉ trọ nếu không rõ nhánh áp dụng.

**Căn cứ:**

- [Thông tư 60/2025/TT-BCT](https://congbao.chinhphu.vn/van-ban/thong-tu-so-60-2025-tt-bct-46756/60185.htm) — Điều 12 khoản 5, Điều 20 khoản 1 điểm d, Điều 21 khoản 1.
- [Thông tư 25/2018/TT-BCT](https://congbao.chinhphu.vn/tai-ve-van-ban-so-25-2018-tt-bct-27337-23871) — Điều 1 khoản 5, sửa điểm c khoản 4 Điều 10 Thông tư 16.
- [Thông tư 09/2023/TT-BCT — sửa quy định giá điện](https://congbao.chinhphu.vn/van-ban-dang-cong-bao/thong-tu-l3/trang-195.htm) — Các sửa đổi liên quan việc kê khai cư trú.
- [Quyết định 1279/QĐ-BCT ngày 09/05/2025 — giá bán điện](https://vanban.chinhphu.vn/?classid=2&docid=213617&pageid=27160) — Phụ lục giá, phiên bản 2025.
- [LuatVietnam — cách tính điện người thuê nhà, bài 04/12/2025](https://luatvietnam.vn/linh-vuc-khac/cach-tinh-tien-dien-sinh-hoat-cua-nguoi-thue-nha-tu-02-12-2025-the-nao-883-105708-article.html) — Bài giải thích; đối chiếu điều khoản hiệu lực trước khi áp dụng.” [1].

- Thông tư 60/2025/TT-BCT — Điều 12. Giá bán lẻ điện sinh hoạt | Khoản 5: “5. Bên mua điện sử dụng vào mục đích sinh hoạt của người thuê nhà để ở áp 
dụng như sau: 
a) Tại mỗi địa chỉ nhà cho thuê, bên bán điện chỉ giao kết một hợp đồng mua 
bán điện duy nhất. Chủ nhà cho thuê có trách nhiệm cung cấp thông tin về cư trú 
tại địa điểm sử dụng điện của người thuê nhà;  
b) Đối với trường hợp cho hộ gia đình thuê: Chủ nhà trực tiếp giao kết hợp 
đồng mua bán điện hoặc ủy quyền cho hộ gia đình thuê nhà giao kết hợp đồng mua 
bán điện (có cam kết thanh toán tiền điện), mỗi hộ gia đình thuê nhà được tính một 
định mức; 
 c) Trường hợp cho sinh viên và người lao động thuê nhà (bên thuê nhà không 
phải là một hộ gia đình): 
- Đối với trường hợp bên thuê nhà có hợp đồng thuê nhà từ 12 tháng trở lên 
và có đăng ký tạm trú, thường trú (xác định theo thông tin về cư trú tại địa điểm 
sử dụng điện) thì chủ nhà trực tiếp giao kết hợp đồng mua bán điện hoặc đại diện 
bên thuê nhà giao kết hợp đồng mua bán điện (có cam kết thanh toán tiền điện 
của chủ nhà);

- Trường hợp thời hạn cho thuê nhà dưới 12 tháng và chủ nhà không thực 
hiện kê khai được đầy đủ số người sử dụng điện thì áp dụng giá bán lẻ điện sinh 
hoạt của bậc 2: Từ 101 - 200 kWh cho toàn bộ sản lượng điện đo đếm được tại 
công tơ; 
- Trường hợp chủ nhà kê khai được đầy đủ số người sử dụng điện thì bên bán 
điện có trách nhiệm cấp định mức cho chủ nhà căn cứ vào thông tin về cư trú tại 
địa điểm sử dụng điện; cứ 04 (bốn) người được tính là một hộ sử dụng điện để tính 
số định mức áp dụng giá bán lẻ điện sinh hoạt, cụ thể: 01 (một) người được tính là 
1/4 định mức, 02 (hai) người được tính là 1/2 định mức, 03 (ba) người được tính là 
3/4 định mức, 04 (bốn) người được tính là 01 định mức. Khi có thay đổi về số 
người thuê nhà, chủ nhà cho thuê có trách nhiệm thông báo cho bên bán điện để 
điều chỉnh định mức tính toán tiền điện; 
- Trường hợp người thuê nhà không giao kết hợp đồng trực tiếp với bên bán 
điện thì tổng tiền điện chủ nhà cho thuê thu của người thuê nhà không được vượt 
quá tiền điện trong hoá đơn tiền điện hằng tháng do đơn vị bán lẻ điện phát hành; 
- Bên bán điện được phép yêu cầu bên mua điện cung cấp thông tin về cư trú 
tại địa điểm sử dụng điện để làm căn cứ xác định số người tính số định mức khi 
tính toán hóa đơn tiền điện.” [2].

- Thông tư 60/2025/TT-BCT — Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp: “Điều 21. Hiệu lực thi hành | Khoản 1
1. Thông tư này có hiệu lực thi hành từ ngày 02 tháng 12 năm 2025, trừ quy 
định tại khoản 3 Điều 4, khoản 1 và khoản 2 Điều 5, Điều 9, Điều 10, khoản 10 
Điều 11, khoản 3 Điều 12, khoản 4 Điều 12, điểm c khoản 5 Điều 12, khoản 6 
Điều 14, khoản 6 Điều 15 Thông tư này và Phụ lục ban hành kèm theo Thông tư 
này có hiệu lực thi hành kể từ ngày thực hiện điều chỉnh mức giá bán lẻ điện bình 
quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành.

Điều 21. Hiệu lực thi hành | Khoản 3
3. Trong quá trình thực hiện Thông tư này nếu có vướng mắc, đề nghị các đơn 
vị có liên quan báo cáo Bộ Công Thương để xem xét sửa đổi, bổ sung cho phù hợp./.

Điều 20. Điều khoản chuyển tiếp | Khoản 1
1. Các quy định tại Thông tư số 16/2014/TT-BCT ngày 29 tháng 5 năm 2014 
của Bộ trưởng Bộ Công Thương quy định về giá bán điện được tiếp tục áp dụng từ 
ngày Thông tư này có hiệu lực đến ngày thực hiện điều chỉnh mức giá bán lẻ điện 
bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành, 
bao gồm:  
a) Khoản 1 Điều 5; 
b) Khoản 10 Điều 8; 
c) Khoản 3 Điều 10 (đã được sửa đổi theo quy định tại khoản 3 Điều 1 của 
Thông tư số 09/2023/TT-BCT sửa đổi, bổ sung một số điều của Thông tư số 
16/2014/TT-BCT và Thông tư số 25/2018/TT-BCT ngày 12 tháng 9 năm 2018 
của Bộ trưởng Bộ Công Thương sửa đổi, bổ sung một số điều của Thông tư số 
16/2014/TT-BCT); 
d) Điểm c khoản 4 Điều 10 (đã được sửa đổi theo quy định tại khoản 5 Điều 1 
của Thông tư số 25/2018/TT-BCT và khoản 2 Điều 2 của Thông tư số 
09/2023/TT-BCT); 
đ) Khoản 6 Điều 12 (đã được sửa đổi theo quy định tại khoản 7 Điều 1 của 
Thông tư số 09/2023/TT-BCT); 
e) Khoản 6 Điều 13 (đã được sửa đổi theo quy định tại khoản 9 Điều 1 của 
Thông tư số 09/2023/TT-BCT).

Điều 20. Điều khoản chuyển tiếp | Khoản 2
2. Quy định áp dụng giá bán điện cho đơn vị bán lẻ điện nông thôn, đơn vị bán 
lẻ điện khu tập thể, cụm dân cư được cấp giấy phép hoạt động điện lực trước ngày 
01 tháng 7 năm 2025 như sau: 
a) Tiếp tục áp dụng giá bán điện cho đơn vị bán lẻ điện theo khu vực tương 
ứng với cấp đơn vị hành chính trước ngày 01 tháng 7 năm 2025 đến ngày thực hiện

điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 
14/2025/QĐ-TTg có hiệu lực thi hành; 
b) Được thực hiện áp dụng giá bán điện cho đơn vị bán lẻ điện theo quy định 
tại khoản 3 Điều này trong thời gian tối thiểu là 12 tháng kể từ ngày thực hiện điều 
chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 
14/2025/QĐ-TTg có hiệu lực thi hành. Đến ngày thực hiện điều chỉnh mức giá bán 
lẻ điện bình quân lần đầu tiên sau khi hết thời hạn 12 tháng nêu tại điểm này, đơn 
vị bán lẻ điện phải chuyển sang áp dụng giá bán điện quy định cho khu vực mới 
theo quy định về cấp đơn vị hành chính tại Điều 1 Luật Tổ chức chính quyền địa 
phương số 72/2025/QH15 hoặc các văn bản sửa đổi, bổ sung, thay thế;   
c) Trường hợp cấp mới hoặc cấp sửa đổi, bổ sung hoặc cấp lại giấy phép hoạt 
động điện lực từ thời điểm điều chỉnh mức giá bán lẻ điện bình quân lần đầu sau 
ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành mà phạm vi hoạt động 
thu hẹp hoặc không thay đổi thì áp dụng quy định tại điểm b khoản này; 
d) Trường hợp cấp mới hoặc cấp sửa đổi, bổ sung hoặc cấp lại giấy phép hoạt 
động điện lực từ thời điểm điều chỉnh mức giá bán lẻ điện bình quân lần đầu sau 
ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành mà có mở rộng phạm 
vi hoạt động thì đơn vị bán lẻ điện phải chuyển sang áp dụng giá bán điện quy 
định cho khu vực mới theo quy định về cấp đơn vị hành chính tại Điều 1 Luật Tổ 
chức chính quyền địa phương số 72/2025/QH15 hoặc các văn bản sửa đổi, bổ 
sung, thay thế.

Điều 20. Điều khoản chuyển tiếp | Khoản 3
3. Quy định áp dụng giá bán điện cho đơn vị bán lẻ điện như sau: 
  a) Giá cho đơn vị bán lẻ điện tại phường được áp dụng cho: đơn vị bán lẻ 
điện khu tập thể, cụm dân cư có phạm vi hoạt động là nội thị thuộc thành phố, thị 
xã trước ngày 01 tháng 7 năm 2025 đối với đơn vị bán lẻ điện được cấp giấy phép 
hoạt động điện lực trước ngày 01 tháng 7 năm 2025; 
b) Giá cho đơn vị bán lẻ điện tại xã được áp dụng cho: đơn vị bán lẻ điện khu 
tập thể, cụm dân cư có phạm vi hoạt động là nội thị thuộc thị trấn, huyện lỵ trước 
ngày 01 tháng 7 năm 2025 đối với đơn vị bán lẻ điện được cấp giấy phép hoạt 
động điện lực trước ngày 01 tháng 7 năm 2025; 
c) Giá cho đơn vị bán lẻ điện nông thôn được áp dụng cho: đơn vị bán lẻ điện 
nông thôn được cấp giấy phép hoạt động điện lực trước ngày 01 tháng 7 năm 2025.” [3].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng; cần đối chiếu phần còn thiếu.

Nguồn có hiệu lực có điều kiện; chưa xác nhận văn bản/sự kiện kích hoạt.

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng, hiệu lực và bản gốc.

### Đáp án bạn gửi

Theo Thông tư 25/2018/TT-BCT và Thông tư 09/2023/TT-BCT của Bộ Công Thương:
- **Trường hợp người thuê có hợp đồng từ 12 tháng trở lên và có đăng ký tạm trú:** Được cấp định mức điện riêng. Cứ **4 người** được tính là **1 hộ dùng điện** để áp biểu giá bán lẻ điện sinh hoạt bậc thang (từ Bậc 1 đến Bậc 6).
- **Trường hợp thời hạn thuê dưới 12 tháng hoặc chủ trọ không kê khai định mức:** Chủ trọ được lựa chọn:
  1. Tính theo biểu giá bán lẻ bậc thang của công tơ tổng; hoặc
  2. **Áp dụng giá bán lẻ điện bậc 3** (mức 101 - 200 kWh) cộng thêm thuế GTGT (hiện nay khoảng 2.167 VNĐ/kWh chưa VAT, sau VAT khoảng 2.300 - 2.400 VNĐ/kWh) cho toàn bộ sản lượng đo được tại công tơ của phòng trọ.
- **Nghiêm cấm:** Chủ trọ tự ý đặt ra mức giá cao vô lý (như 3.500 – 4.500 VNĐ/kWh) để trục lợi.

### Nhận xét đối chiếu

**Ý khớp:**

- Trường hợp đủ điều kiện (kê khai đầy đủ số người/hợp đồng từ 12 tháng trở lên và có thông tin cư trú): Cứ 04 người được tính là 01 hộ (01 định mức) để áp dụng giá bán lẻ điện sinh hoạt bậc thang.
- Không mặc nhiên cho phép chủ trọ tự ý đặt ra một mức giá điện riêng.

**Thiếu so với đáp án:**

- Các mức giá cụ thể theo ước tính của USER_REFERENCE (khoảng 2.167 VNĐ/kWh chưa VAT, 2.300 - 2.400 VNĐ/kWh sau VAT; ví dụ mức giá cao vô lý 3.500 - 4.500 VNĐ/kWh).
- Phương án lựa chọn tính theo biểu giá bán lẻ bậc thang của công tơ tổng khi thuê dưới 12 tháng hoặc không kê khai.

**Nội dung khác:**

- Trường hợp thuê dưới 12 tháng và không kê khai đủ người: USER_REFERENCE nêu áp dụng giá bán lẻ điện bậc 3 (101 - 200 kWh), trong khi trích dẫn Thông tư 60 trong ANSWER nêu áp dụng giá bán lẻ điện bậc 2 (101 - 200 kWh) (chưa xác minh văn bản nào đang có hiệu lực thi hành tại thời điểm áp dụng).
- Căn cứ pháp lý: USER_REFERENCE viện dẫn Thông tư 25/2018/TT-BCT và Thông tư 09/2023/TT-BCT; ANSWER tập trung viện dẫn Thông tư 60/2025/TT-BCT cùng các điều khoản chuyển tiếp (Điều 20, Điều 21).

**Nội dung thêm:**

- Quy định chi tiết về cách chia lẻ định mức: 1 người là 1/4 định mức, 2 người là 1/2 định mức, 3 người là 3/4 định mức.
- Quy định giới hạn: Tổng số tiền chủ trọ thu không được vượt quá số tiền trên hoá đơn tiền điện do bên bán lẻ điện phát hành.
- Lưu ý pháp lý về hiệu lực thi hành: Điểm c khoản 5 Điều 12 Thông tư 60/2025/TT-BCT có mốc hiệu lực riêng, cần đối chiếu quy định chuyển tiếp và xác nhận với đơn vị điện lực.
- Trường hợp cho hộ gia đình thuê: Mỗi hộ gia đình thuê nhà được tính một định mức.

**Giới hạn nguồn:**

- Đoạn đầu ANSWER dẫn từ 'Hướng dẫn thực tế' mang tính chất biên soạn/khuyến nghị, không phải nguyên văn điều luật.
- Hiệu lực của Thông tư 60/2025/TT-BCT đối với điểm c khoản 5 Điều 12 phụ thuộc vào ngày điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau Quyết định số 14/2025/QĐ-TTg, cần đối chiếu sự kiện kích hoạt thực tế.


## Câu 6: Ba sinh viên ở chung một phòng được tính tiền điện ra sao?

### Chatbot với dữ liệu mới

Các đoạn trả lời trực tiếp trong nguồn:

- Hướng dẫn thực tế: CHỦ ĐỀ: Tiền điện phòng trọ — Q: Ba sinh viên ở chung một phòng được tính tiền điện ra sao?: “HƯỚNG DẪN BIÊN SOẠN — không phải nguyên văn điều luật.
### Q: Ba sinh viên ở chung một phòng được tính tiền điện ra sao?

A: Nếu đủ điều kiện nhánh sinh viên/người lao động thuê nhà và kê khai được số người, quy tắc bốn người một hộ cho phép ba người tương ứng ba phần tư định mức một hộ. Đây là định mức của công tơ/hợp đồng mua điện, chưa phải công thức bắt buộc chia hóa đơn giữa ba bạn. Cần kiểm tra thời hạn thuê, người đứng tên hợp đồng, số người thực tế và Điều 20–21 Thông tư 60 để chọn đúng quy định chuyển tiếp; nhánh không kê khai được số người có cách áp giá khác.

**Khuyến nghị thực tế:** Xác nhận ba người đã được kê khai với điện lực; thỏa thuận riêng cách chia tiền theo thời gian ở hoặc đồng hồ phụ.

**Căn cứ:**

- [Thông tư 60/2025/TT-BCT](https://congbao.chinhphu.vn/van-ban/thong-tu-so-60-2025-tt-bct-46756/60185.htm) — Điều 12 khoản 5 điểm c, Điều 20–21.
- [Thông tư 25/2018/TT-BCT](https://congbao.chinhphu.vn/tai-ve-van-ban-so-25-2018-tt-bct-27337-23871) — Quy tắc định mức tại Điều 1 khoản 5.
- [Thông tư 09/2023/TT-BCT — sửa quy định giá điện](https://congbao.chinhphu.vn/van-ban-dang-cong-bao/thong-tu-l3/trang-195.htm) — Sửa đổi quy định thuê nhà và thông tin cư trú.” [1].

- Thông tư 60/2025/TT-BCT — Điều 12. Giá bán lẻ điện sinh hoạt | Khoản 5: “5. Bên mua điện sử dụng vào mục đích sinh hoạt của người thuê nhà để ở áp 
dụng như sau: 
a) Tại mỗi địa chỉ nhà cho thuê, bên bán điện chỉ giao kết một hợp đồng mua 
bán điện duy nhất. Chủ nhà cho thuê có trách nhiệm cung cấp thông tin về cư trú 
tại địa điểm sử dụng điện của người thuê nhà;  
b) Đối với trường hợp cho hộ gia đình thuê: Chủ nhà trực tiếp giao kết hợp 
đồng mua bán điện hoặc ủy quyền cho hộ gia đình thuê nhà giao kết hợp đồng mua 
bán điện (có cam kết thanh toán tiền điện), mỗi hộ gia đình thuê nhà được tính một 
định mức; 
 c) Trường hợp cho sinh viên và người lao động thuê nhà (bên thuê nhà không 
phải là một hộ gia đình): 
- Đối với trường hợp bên thuê nhà có hợp đồng thuê nhà từ 12 tháng trở lên 
và có đăng ký tạm trú, thường trú (xác định theo thông tin về cư trú tại địa điểm 
sử dụng điện) thì chủ nhà trực tiếp giao kết hợp đồng mua bán điện hoặc đại diện 
bên thuê nhà giao kết hợp đồng mua bán điện (có cam kết thanh toán tiền điện 
của chủ nhà);

- Trường hợp thời hạn cho thuê nhà dưới 12 tháng và chủ nhà không thực 
hiện kê khai được đầy đủ số người sử dụng điện thì áp dụng giá bán lẻ điện sinh 
hoạt của bậc 2: Từ 101 - 200 kWh cho toàn bộ sản lượng điện đo đếm được tại 
công tơ; 
- Trường hợp chủ nhà kê khai được đầy đủ số người sử dụng điện thì bên bán 
điện có trách nhiệm cấp định mức cho chủ nhà căn cứ vào thông tin về cư trú tại 
địa điểm sử dụng điện; cứ 04 (bốn) người được tính là một hộ sử dụng điện để tính 
số định mức áp dụng giá bán lẻ điện sinh hoạt, cụ thể: 01 (một) người được tính là 
1/4 định mức, 02 (hai) người được tính là 1/2 định mức, 03 (ba) người được tính là 
3/4 định mức, 04 (bốn) người được tính là 01 định mức. Khi có thay đổi về số 
người thuê nhà, chủ nhà cho thuê có trách nhiệm thông báo cho bên bán điện để 
điều chỉnh định mức tính toán tiền điện; 
- Trường hợp người thuê nhà không giao kết hợp đồng trực tiếp với bên bán 
điện thì tổng tiền điện chủ nhà cho thuê thu của người thuê nhà không được vượt 
quá tiền điện trong hoá đơn tiền điện hằng tháng do đơn vị bán lẻ điện phát hành; 
- Bên bán điện được phép yêu cầu bên mua điện cung cấp thông tin về cư trú 
tại địa điểm sử dụng điện để làm căn cứ xác định số người tính số định mức khi 
tính toán hóa đơn tiền điện.” [2].

- Thông tư 60/2025/TT-BCT — Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp: “Điều 21. Hiệu lực thi hành | Khoản 1
1. Thông tư này có hiệu lực thi hành từ ngày 02 tháng 12 năm 2025, trừ quy 
định tại khoản 3 Điều 4, khoản 1 và khoản 2 Điều 5, Điều 9, Điều 10, khoản 10 
Điều 11, khoản 3 Điều 12, khoản 4 Điều 12, điểm c khoản 5 Điều 12, khoản 6 
Điều 14, khoản 6 Điều 15 Thông tư này và Phụ lục ban hành kèm theo Thông tư 
này có hiệu lực thi hành kể từ ngày thực hiện điều chỉnh mức giá bán lẻ điện bình 
quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành.

Điều 21. Hiệu lực thi hành | Khoản 3
3. Trong quá trình thực hiện Thông tư này nếu có vướng mắc, đề nghị các đơn 
vị có liên quan báo cáo Bộ Công Thương để xem xét sửa đổi, bổ sung cho phù hợp./.

Điều 20. Điều khoản chuyển tiếp | Khoản 1
1. Các quy định tại Thông tư số 16/2014/TT-BCT ngày 29 tháng 5 năm 2014 
của Bộ trưởng Bộ Công Thương quy định về giá bán điện được tiếp tục áp dụng từ 
ngày Thông tư này có hiệu lực đến ngày thực hiện điều chỉnh mức giá bán lẻ điện 
bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành, 
bao gồm:  
a) Khoản 1 Điều 5; 
b) Khoản 10 Điều 8; 
c) Khoản 3 Điều 10 (đã được sửa đổi theo quy định tại khoản 3 Điều 1 của 
Thông tư số 09/2023/TT-BCT sửa đổi, bổ sung một số điều của Thông tư số 
16/2014/TT-BCT và Thông tư số 25/2018/TT-BCT ngày 12 tháng 9 năm 2018 
của Bộ trưởng Bộ Công Thương sửa đổi, bổ sung một số điều của Thông tư số 
16/2014/TT-BCT); 
d) Điểm c khoản 4 Điều 10 (đã được sửa đổi theo quy định tại khoản 5 Điều 1 
của Thông tư số 25/2018/TT-BCT và khoản 2 Điều 2 của Thông tư số 
09/2023/TT-BCT); 
đ) Khoản 6 Điều 12 (đã được sửa đổi theo quy định tại khoản 7 Điều 1 của 
Thông tư số 09/2023/TT-BCT); 
e) Khoản 6 Điều 13 (đã được sửa đổi theo quy định tại khoản 9 Điều 1 của 
Thông tư số 09/2023/TT-BCT).

Điều 20. Điều khoản chuyển tiếp | Khoản 2
2. Quy định áp dụng giá bán điện cho đơn vị bán lẻ điện nông thôn, đơn vị bán 
lẻ điện khu tập thể, cụm dân cư được cấp giấy phép hoạt động điện lực trước ngày 
01 tháng 7 năm 2025 như sau: 
a) Tiếp tục áp dụng giá bán điện cho đơn vị bán lẻ điện theo khu vực tương 
ứng với cấp đơn vị hành chính trước ngày 01 tháng 7 năm 2025 đến ngày thực hiện

điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 
14/2025/QĐ-TTg có hiệu lực thi hành; 
b) Được thực hiện áp dụng giá bán điện cho đơn vị bán lẻ điện theo quy định 
tại khoản 3 Điều này trong thời gian tối thiểu là 12 tháng kể từ ngày thực hiện điều 
chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 
14/2025/QĐ-TTg có hiệu lực thi hành. Đến ngày thực hiện điều chỉnh mức giá bán 
lẻ điện bình quân lần đầu tiên sau khi hết thời hạn 12 tháng nêu tại điểm này, đơn 
vị bán lẻ điện phải chuyển sang áp dụng giá bán điện quy định cho khu vực mới 
theo quy định về cấp đơn vị hành chính tại Điều 1 Luật Tổ chức chính quyền địa 
phương số 72/2025/QH15 hoặc các văn bản sửa đổi, bổ sung, thay thế;   
c) Trường hợp cấp mới hoặc cấp sửa đổi, bổ sung hoặc cấp lại giấy phép hoạt 
động điện lực từ thời điểm điều chỉnh mức giá bán lẻ điện bình quân lần đầu sau 
ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành mà phạm vi hoạt động 
thu hẹp hoặc không thay đổi thì áp dụng quy định tại điểm b khoản này; 
d) Trường hợp cấp mới hoặc cấp sửa đổi, bổ sung hoặc cấp lại giấy phép hoạt 
động điện lực từ thời điểm điều chỉnh mức giá bán lẻ điện bình quân lần đầu sau 
ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành mà có mở rộng phạm 
vi hoạt động thì đơn vị bán lẻ điện phải chuyển sang áp dụng giá bán điện quy 
định cho khu vực mới theo quy định về cấp đơn vị hành chính tại Điều 1 Luật Tổ 
chức chính quyền địa phương số 72/2025/QH15 hoặc các văn bản sửa đổi, bổ 
sung, thay thế.

Điều 20. Điều khoản chuyển tiếp | Khoản 3
3. Quy định áp dụng giá bán điện cho đơn vị bán lẻ điện như sau: 
  a) Giá cho đơn vị bán lẻ điện tại phường được áp dụng cho: đơn vị bán lẻ 
điện khu tập thể, cụm dân cư có phạm vi hoạt động là nội thị thuộc thành phố, thị 
xã trước ngày 01 tháng 7 năm 2025 đối với đơn vị bán lẻ điện được cấp giấy phép 
hoạt động điện lực trước ngày 01 tháng 7 năm 2025; 
b) Giá cho đơn vị bán lẻ điện tại xã được áp dụng cho: đơn vị bán lẻ điện khu 
tập thể, cụm dân cư có phạm vi hoạt động là nội thị thuộc thị trấn, huyện lỵ trước 
ngày 01 tháng 7 năm 2025 đối với đơn vị bán lẻ điện được cấp giấy phép hoạt 
động điện lực trước ngày 01 tháng 7 năm 2025; 
c) Giá cho đơn vị bán lẻ điện nông thôn được áp dụng cho: đơn vị bán lẻ điện 
nông thôn được cấp giấy phép hoạt động điện lực trước ngày 01 tháng 7 năm 2025.” [3].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng; cần đối chiếu phần còn thiếu.

Nguồn có hiệu lực có điều kiện; chưa xác nhận văn bản/sự kiện kích hoạt.

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng, hiệu lực và bản gốc.

### Đáp án bạn gửi

Theo quy định tại Điều 10 Thông tư 16/2014/TT-BCT (được sửa đổi bởi Thông tư 25/2018/TT-BCT):
- Quy chuẩn định mức: **1 người được tính là 1/4 định mức, 2 người là 2/4 định mức, 3 người được tính là 3/4 định mức hộ gia đình**.
- Cụ thể với **3 sinh viên** có đăng ký tạm trú: Sẽ được hưởng **75% định mức của từng bậc thang điện** sinh hoạt:
  - Bậc 1 (0 - 50 kWh): Định mức được tính là $50 \times 3/4 = 37,5\text{ kWh}$.
  - Bậc 2 (51 - 100 kWh): Định mức là $37,5\text{ kWh}$.
  - Các bậc tiếp theo tính tương tự theo tỷ lệ 3/4.
- Nếu chủ trọ không làm thủ tục kê khai định mức với bên Điện lực thì phải áp dụng **giá điện Bậc 3** cho toàn bộ số điện phòng tiêu thụ.

### Nhận xét đối chiếu

**Ý khớp:**

- Cứ 4 người tính là 1 định mức hộ gia đình; 3 người (sinh viên) nếu được kê khai đầy đủ thì được tính là 3/4 định mức.

**Thiếu so với đáp án:**

- Ví dụ chi tiết cách tính số kWh cụ thể theo từng bậc (Bậc 1: 50 x 3/4 = 37,5 kWh; Bậc 2: 37,5 kWh; các bậc tiếp theo tương tự).

**Nội dung khác:**

- Trường hợp không kê khai số người: USER_REFERENCE nêu áp dụng giá điện Bậc 3 cho toàn bộ sản lượng điện tiêu thụ (dẫn chiếu Thông tư 16/2014 và Thông tư 25/2018); trong khi ANSWER (trích Điều 12 Thông tư 60/2025/TT-BCT) nêu trường hợp thuê dưới 12 tháng không kê khai đầy đủ thì áp dụng giá bán lẻ điện bậc 2 (101 - 200 kWh) cho toàn bộ sản lượng đo đếm được (chưa xác minh văn bản nào đang có hiệu lực thi hành thực tế tại thời điểm xét).

**Nội dung thêm:**

- Lưu ý 3/4 định mức là định mức tính cho công tơ/hợp đồng mua bán điện, không phải công thức bắt buộc để chia nội bộ tiền điện giữa 3 sinh viên.
- Quy định về thời hạn hợp đồng thuê (từ 12 tháng trở lên hoặc dưới 12 tháng) gắn với việc ký hợp đồng và kê khai thông tin cư trú.
- Quy định tổng tiền điện chủ nhà thu của người thuê không được vượt quá hóa đơn do bên bán lẻ điện phát hành.
- Lưu ý về điều khoản chuyển tiếp và hiệu lực thi hành theo Điều 20, Điều 21 Thông tư 60/2025/TT-BCT.

**Giới hạn nguồn:**

- Nguồn 1 là hướng dẫn biên soạn thực tế, không phải nguyên văn điều luật.
- Khoản 5 Điều 12 Thông tư 60/2025/TT-BCT có hiệu lực phụ thuộc vào mốc điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau Quyết định 14/2025/QĐ-TTg, cần đối chiếu văn bản chuyển tiếp và thời điểm áp dụng thực tế.


## Câu 7: Nếu tôi nghi tiền điện bị thu cao hơn quy định, nên kiểm tra hóa đơn và căn cứ nào?

### Chatbot với dữ liệu mới

Bạn cần đối chiếu hóa đơn điện lực với các chỉ số tiêu thụ thực tế và văn bản giá điện đúng kỳ để xác định xem chủ trọ có thu tiền vượt mức quy định hay không [1].

- Kiểm tra hóa đơn điện lực về chỉ số công tơ tổng hoặc phụ, ngày ghi số, sản lượng điện tiêu thụ, số người hoặc hộ được tính định mức, đơn giá từng bậc và tiền thuế [1].
- Chọn văn bản giá điện đúng kỳ tính tiền, kể cả kỳ có biến động giá, để so sánh mức giá quy định với số tiền chủ trọ thực tế thu cùng các khoản chi phí được tách riêng [1].
- Khuyến nghị lưu trữ hình ảnh công tơ điện, bảng thông báo thu tiền và toàn bộ chứng từ thanh toán [1].
- Khuyến nghị yêu cầu bên cho thuê giải thích rõ khoản chênh lệch, đồng thời liên hệ đơn vị điện lực hoặc cơ quan có thẩm quyền xử lý khi phát hiện vi phạm [1].

Chế tài xử phạt và biện pháp hoàn trả tiền thu thừa theo Nghị định 133 áp dụng đối với người cho thuê thu tiền cao hơn quy định khi mua điện theo giá bán lẻ cho sinh hoạt [1].
Mức phạt tiền cụ thể cần được tra cứu kết hợp cùng quy tắc phân loại đối tượng vi phạm tại Điều 4 Nghị định 133 [1].

Để áp dụng vào trường hợp của bạn:
- Chủ nhà trọ hiện đang tính tiền điện cho bạn với mức giá bao nhiêu một kWh?
- Hợp đồng mua bán điện của khu trọ đang được đứng tên cá nhân hay tính theo hình thức nào?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

### Đáp án bạn gửi

Bạn cần thực hiện các bước kiểm tra sau:
1. **Kiểm tra công tơ điện:** Ghi lại chỉ số điện đầu tháng và cuối tháng của đồng hồ phòng mình, tính ra số kWh thực tế đã dùng.
2. **Yêu cầu đối chiếu hóa đơn tiền điện gốc:** Đề nghị chủ trọ cho xem hóa đơn tiền điện tháng đó của Điện lực cấp (hoặc mã khách hàng PE... trên ứng dụng EVNSPC CSKH).
3. **Căn cứ pháp lý xử phạt:** Căn cứ theo **Khoản 6 Điều 12 Nghị định 134/2013/NĐ-CP** (được sửa đổi bởi **Nghị định 17/2022/NĐ-CP**), hành vi thu tiền điện của người thuê nhà cao hơn giá quy định trong trường hợp mua điện theo giá bán lẻ điện sinh hoạt bị **phạt tiền từ 20.000.000 đồng đến 30.000.000 đồng**.
4. **Kênh phản ánh:** Nếu chủ trọ cố tình vi phạm, bạn có thể gọi hotline CSKH Tổng công ty Điện lực miền Nam (EVNSPC: **1900 1006** hoặc **1900 9000**) hoặc phản ánh qua UBND phường/xã nơi đặt phòng trọ.

### Nhận xét đối chiếu

**Ý khớp:**

- Cần kiểm tra/ghi nhận chỉ số công tơ điện và số điện tiêu thụ thực tế.
- Cần đối chiếu với hóa đơn tiền điện do phía điện lực phát hành.
- Đều đề cập đến chế tài xử phạt hành vi người cho thuê thu tiền điện cao hơn quy định khi mua điện theo giá bán lẻ sinh hoạt.
- Liên hệ đơn vị điện lực hoặc cơ quan nhà nước có thẩm quyền để giải quyết/phản ánh khi phát hiện vi phạm.

**Thiếu so với đáp án:**

- Mức phạt tiền cụ thể từ 20.000.000 đồng đến 30.000.000 đồng theo USER_REFERENCE.
- Kênh phản ánh cụ thể: hotline CSKH EVNSPC (1900 1006 hoặc 1900 9000), ứng dụng EVNSPC CSKH, hoặc UBND phường/xã.

**Nội dung khác:**

- Căn cứ pháp lý xử phạt: USER_REFERENCE viện dẫn Khoản 6 Điều 12 Nghị định 134/2013/NĐ-CP (sửa đổi bởi Nghị định 17/2022/NĐ-CP); trong khi ANSWER (theo SOURCE) viện dẫn Nghị định 133 (chưa xác minh văn bản nào có hiệu lực tại thời điểm áp dụng).

**Nội dung thêm:**

- Kiểm tra chi tiết trên hóa đơn: ngày ghi số, số người/hộ được tính định mức, đơn giá từng bậc và tiền thuế.
- Chọn văn bản giá điện đúng kỳ tính tiền (kể cả kỳ biến động giá) và tách riêng các khoản chi phí khác.
- Biện pháp khắc phục hậu quả hoàn trả tiền thu thừa theo quy định.
- Lưu trữ hình ảnh công tơ, bảng thông báo thu tiền và chứng từ thanh toán; yêu cầu bên cho thuê giải thích chênh lệch.
- Câu hỏi làm rõ mức giá thu thực tế và hình thức hợp đồng mua bán điện của khu trọ.

**Giới hạn nguồn:**

- SOURCE trích từ phần 'HƯỚNG DẪN BIÊN SOẠN — không phải nguyên văn điều luật', là nội dung biên soạn giải thích chứ không phải văn bản luật gốc.
- Cần kiểm tra hiệu lực áp dụng giữa Nghị định 133/2026/NĐ-CP nêu trong SOURCES và Nghị định 134/2013/NĐ-CP (sửa đổi bởi Nghị định 17/2022/NĐ-CP) trong USER_REFERENCE.


## Câu 8: Chủ trọ có phải thông báo cách tính tiền điện và số điện đã sử dụng không?

### Chatbot với dữ liệu mới

Các đoạn trả lời trực tiếp trong nguồn:

- Hướng dẫn công khai cách tính tiền điện nhà trọ Cần Thơ — 21/09/2026 — Hướng dẫn công khai cách tính tiền điện nhà trọ Cần Thơ: “Đoàn kiểm tra cũng hướng dẫn người thuê trọ cách tính tiền điện sinh hoạt theo quy định, giúp chủ động kiểm tra, đối chiếu số tiền phải thanh toán hằng tháng. Đối với chủ nhà trọ, đoàn lưu ý cần thực hiện đúng quy định về giá bán điện, công khai cách tính và thu tiền điện theo đúng hóa đơn do Điện lực phát hành.

Tại các điểm giao dịch và thanh toán trung gian, công ty tiếp tục công khai thông tin về giá điện, việc ghi chỉ số công tơ, lập hóa đơn, mua bán điện, các quy định về đo đếm, an toàn điện, sử dụng điện tiết kiệm cũng như các trường hợp ngừng, giảm hoặc chấm dứt cung cấp điện. Qua đó, người thuê trọ có thêm thông tin để bảo vệ quyền lợi của mình khi sử dụng điện.” [1].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng; cần đối chiếu phần còn thiếu.

Chưa có nguồn trực tiếp về thông báo cách tính và sản lượng điện.

Nguồn công khai cách tính điện tại Cần Thơ là hướng dẫn thực tế, chưa phải điều khoản xác lập nghĩa vụ thông báo bắt buộc cho mọi chủ trọ; chưa xác nhận sự kiện kích hoạt hiệu lực của quy định điện có điều kiện.

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng, hiệu lực và bản gốc.

### Đáp án bạn gửi

**Có.** Theo quy định của Bộ Công Thương và nguyên tắc giao kết hợp đồng dân sự:
- Chủ trọ có trách nhiệm công khai, minh bạch số điện tiêu thụ bằng việc cho phép người thuê cùng chốt chỉ số công tơ vào kỳ thanh toán.
- Bảng kê thanh toán hàng tháng phải nêu rõ: Chỉ số cũ, chỉ số mới, lượng điện tiêu thụ (kWh), đơn giá áp dụng và thành tiền.

### Nhận xét đối chiếu

**Ý khớp:**

- Cả hai đều đề cập đến việc chủ trọ cần công khai/minh bạch cách tính tiền điện đối với người thuê.

**Thiếu so với đáp án:**

- Khẳng định trực tiếp câu trả lời 'Có'.
- Trách nhiệm công khai minh bạch số điện tiêu thụ bằng cách cho phép người thuê cùng chốt chỉ số công tơ vào kỳ thanh toán.
- Bảng kê thanh toán hàng tháng phải nêu rõ: Chỉ số cũ, chỉ số mới, lượng điện tiêu thụ (kWh), đơn giá áp dụng và thành tiền.

**Nội dung khác:**

- USER_REFERENCE khẳng định dứt khoát chủ trọ 'Có' nghĩa vụ thông báo/công khai các nội dung trên theo quy định Bộ Công Thương và giao kết hợp đồng, trong khi ANSWER kết luận chưa đủ căn cứ từ nguồn để xác lập nghĩa vụ bắt buộc cho mọi chủ trọ và chưa có nguồn trực tiếp về thông báo sản lượng điện (chưa xác minh bên nào đúng theo quy định pháp luật hiện hành).

**Nội dung thêm:**

- Dẫn thông tin từ hướng dẫn kiểm tra thực tế tại Cần Thơ về việc chủ nhà trọ cần thực hiện đúng giá bán điện, công khai cách tính và thu tiền điện theo đúng hóa đơn Điện lực phát hành.
- Lưu ý người dùng rằng thông tin từ bài viết tại Cần Thơ mang tính hướng dẫn thực tế tại địa phương, chưa đủ để khái quát thành quy định bắt buộc cho toàn bộ chủ trọ.

**Giới hạn nguồn:**

- Đoạn trích từ bài viết về Cần Thơ chỉ là bản tin/hướng dẫn thực tế của đoàn kiểm tra địa phương, không phải văn bản quy phạm pháp luật quy định nghĩa vụ chung.
- Chunk 428 là tài liệu biên soạn nội bộ ('HƯỚNG DẪN BIÊN SOẠN — không phải nguyên văn điều luật') giải quyết tình huống ba sinh viên chung phòng, không quy định về nghĩa vụ thông báo số điện và cách tính của chủ trọ.


## Câu 9: Giá nước sinh hoạt áp dụng cho phòng trọ ở Cần Thơ được xác định theo căn cứ nào?

### Chatbot với dữ liệu mới

Giá nước sinh hoạt tại Cần Thơ được xác định căn cứ vào đơn vị cấp nước, mã khách hàng, vùng phục vụ, khu vực đô thị hay nông thôn, nhóm đối tượng sử dụng và quyết định giá của kỳ thu theo Quyết định 215/QĐ-UBND [1] [2].

- Kiểm tra hóa đơn để xác định chính xác đơn vị cấp nước, mã khách hàng và kỳ thu tiền nước của phòng trọ [1].
- Xác định khu vực phòng trọ thuộc đô thị hay nông thôn cùng nhóm mục đích sử dụng nước theo bảng giá [1] [2].
- Đối chiếu mức giá áp dụng năm 2024 theo Quyết định 215/QĐ-UBND đối với công ty cấp nước hoặc Trung tâm Nước sạch và Vệ sinh môi trường nông thôn [1] [2].
- Khuyến nghị liên hệ nhà cung cấp nước để xác nhận đúng nhóm giá và văn bản áp dụng theo đúng địa chỉ cùng tháng hóa đơn [1].

Bảng giá theo Quyết định 215/QĐ-UBND từ ngày 01/02/2024 có phạm vi theo phiên bản năm 2024 và không mặc nhiên áp dụng cho mọi địa chỉ sau thay đổi địa giới [1] [2].
Mức giá trong quyết định đã gồm thuế giá trị gia tăng nhưng chưa bao gồm phí bảo vệ môi trường đối với nước thải sinh hoạt [1] [2].
Quy định khối lượng tối thiểu 4 m³/hộ gia đình/tháng khi dùng chung đồng hồ không phải là định mức giá 4 m³ cho từng cá nhân thuê trọ [1].

Để áp dụng vào trường hợp của bạn:
- Đơn vị nào đang trực tiếp cấp nước cho khu phòng trọ của bạn?
- Phòng trọ của bạn nằm ở khu vực đô thị hay nông thôn tại Cần Thơ?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

### Đáp án bạn gửi

- Giá nước sạch sinh hoạt tại Cần Thơ do **UBND TP. Cần Thơ ban hành khung giá** áp dụng cho đơn vị cấp nước (như Cantho Water).
- Đối với sinh viên, người thuê trọ có đăng ký tạm trú: Có thể được chủ trọ đăng ký cấp **định mức nước sinh hoạt hộ gia đình** (thường là **4 m³/người/tháng** theo mức giá ưu đãi bậc 1).
- Mức giá nước sinh hoạt bậc thang dân cư tại Cần Thơ dao động từ khoảng 7.000 – 11.000 VNĐ/m³ (tùy theo khối lượng sử dụng và đã gồm thuế VAT, phí bảo vệ môi trường/thoát nước).

### Nhận xét đối chiếu

**Ý khớp:**

- Giá nước sạch tại Cần Thơ do cơ quan có thẩm quyền ban hành (UBND TP. Cần Thơ thông qua Quyết định 215/QĐ-UBND) áp dụng cho các đơn vị cấp nước.
- Có đề cập đến mức định mức/khối lượng 4 m³ liên quan đến nước sinh hoạt.

**Thiếu so với đáp án:**

- Ý kiến cho rằng người thuê trọ có đăng ký tạm trú có thể được chủ trọ đăng ký cấp định mức nước sinh hoạt hộ gia đình 4 m³/người/tháng theo giá ưu đãi bậc 1.
- Khung giá nước sinh hoạt bậc thang dao động khoảng 7.000 – 11.000 VNĐ/m³ (đã gồm thuế VAT và phí bảo vệ môi trường/thoát nước).

**Nội dung khác:**

- Cơ chế định mức 4 m³: USER_REFERENCE cho rằng người thuê trọ có thể được cấp định mức 4 m³/người/tháng; trong khi ANSWER nêu khối lượng tối thiểu 4 m³/hộ gia đình/tháng khi dùng chung đồng hồ không phải là định mức giá 4 m³ cho từng cá nhân thuê trọ (chưa xác minh bên nào đúng theo quy định hiện hành).
- Thành phần giá và cơ chế tính giá: USER_REFERENCE nêu giá nước tính theo bậc thang dân cư và đã gồm phí bảo vệ môi trường/thoát nước; ANSWER nêu căn cứ theo khu vực đô thị/nông thôn, đơn vị cấp nước, nhóm đối tượng theo Quyết định 215/QĐ-UBND và giá chưa bao gồm phí bảo vệ môi trường đối với nước thải sinh hoạt.

**Nội dung thêm:**

- Nêu căn cứ cụ thể vào Quyết định 215/QĐ-UBND ngày 01/02/2024 của Cần Thơ.
- Chỉ ra các căn cứ xác định thực tế: đơn vị cấp nước, mã khách hàng trên hóa đơn, vùng phục vụ, khu vực đô thị hay nông thôn, và kỳ thu tiền nước.
- Phân biệt giữa công ty cấp nước thông thường và Trung tâm Nước sạch và Vệ sinh môi trường nông thôn.

**Giới hạn nguồn:**

- Tài liệu trích dẫn mang nhãn 'HƯỚNG DẪN BIÊN SOẠN — không phải nguyên văn điều luật', cần phân biệt diễn giải hướng dẫn với văn bản quy phạm pháp luật gốc.
- Bảng giá theo Quyết định 215/QĐ-UBND có hiệu lực từ 01/02/2024 theo phiên bản năm 2024, không mặc nhiên áp dụng cho mọi địa chỉ sau thay đổi địa giới hành chính.


## Câu 10: Tôi nên kiểm tra gì khi chủ trọ thu tiền nước theo đầu người thay vì đồng hồ?

### Chatbot với dữ liệu mới

Bạn cần kiểm tra điều khoản hợp đồng thuê về mức thu, ngày chốt số người và cách tính khi ở không đủ tháng, đồng thời mức thu thỏa thuận vẫn phải phù hợp với các quy định bắt buộc áp dụng [1].

- Kiểm tra hợp đồng thuê phòng xem tiền nước được ghi nhận cố định theo đầu người hay theo khối lượng sử dụng thực tế cùng các mức phí đi kèm [1].
- Rà soát quy định về ngày chốt số lượng người ở thực tế và phương án xử lý chi phí đối với trường hợp người thuê ở không đủ tháng [1].
- Yêu cầu bên cho thuê giải thích rõ ràng cách thức hình thành mức thu, phân biệt khoản tiền nước với các loại chi phí khác và so sánh với hóa đơn công tơ tổng nếu có [1].
- Khuyến nghị đề nghị chủ nhà trọ cung cấp bảng kê thu tiền minh bạch hoặc lắp đặt đồng hồ phụ để theo dõi [1].

Quy định kiểm định đồng hồ tại Điều 50 Nghị định 117 không xác lập công thức tính tiền nước theo đầu người giữa bên cho thuê và người thuê trọ [1].
Người thuê không thể tự nhận việc đề nghị bảng thu minh bạch hoặc đồng hồ phụ là quyền bắt buộc chủ trọ phải lắp đồng hồ riêng trong mọi trường hợp [1].
Không phải mọi mức thu đã ghi nhận trong hợp đồng thuê đều đương nhiên hợp pháp nếu không phù hợp với quy định bắt buộc áp dụng [1].

Để áp dụng vào trường hợp của bạn:
- Hợp đồng thuê trọ của bạn hiện có điều khoản cụ thể nào về mức thu tiền nước và ngày chốt nhân khẩu không?
- Chủ nhà trọ có cung cấp hóa đơn tiền nước từ công tơ tổng để đối chiếu chi phí thực tế hay không?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

### Đáp án bạn gửi

Thu tiền nước theo đầu người là hình thức khoán phổ biến khi nhà trọ không lắp đồng hồ nước riêng cho từng phòng. Bạn nên kiểm tra:
1. **Mức khoán trung bình:** Tại Cần Thơ, mức thu khoán tiền nước phổ biến cho sinh viên dao động từ **30.000 – 50.000 VNĐ/người/tháng** (tương đương 3 – 5 m³ nước sinh hoạt).
2. **Nếu chủ trọ thu quá cao (80.000 – 100.000 VNĐ/người/tháng):** Bạn có quyền yêu cầu chủ trọ giải trình dựa trên hóa đơn tiền nước thực tế của đơn vị cấp nước chia bình quân cho tổng số nhân khẩu đang ở trọ.
3. **Thỏa thuận bằng văn bản:** Mức khoán theo đầu người phải được ghi cụ thể trong hợp đồng thuê nhà để tránh việc chủ trọ tăng giá tùy tiện vào mùa khô hoặc khi có người ở thêm.

### Nhận xét đối chiếu

**Ý khớp:**

- Cần kiểm tra điều khoản và mức thu cụ thể được ghi nhận trong hợp đồng thuê phòng.
- Yêu cầu bên cho thuê giải trình, làm rõ cơ sở hình thành mức thu và đối chiếu với hóa đơn tiền nước thực tế (hóa đơn công tơ tổng).

**Thiếu so với đáp án:**

- Mức khoán tham khảo thực tế tại Cần Thơ phổ biến từ 30.000 – 50.000 VNĐ/người/tháng (tương đương 3 – 5 m³ nước).
- Tình huống cụ thể nếu chủ trọ thu quá cao (80.000 – 100.000 VNĐ/người/tháng) và việc chia bình quân theo tổng số nhân khẩu để tránh tăng giá tùy tiện vào mùa khô hoặc khi có người ở thêm.

**Nội dung thêm:**

- Kiểm tra ngày chốt số lượng người và phương án tính toán chi phí đối với trường hợp ở không đủ tháng.
- Lưu ý phân biệt khoản tiền nước với các loại chi phí khác.
- Đề nghị chủ trọ lập bảng kê minh bạch hoặc lắp đặt đồng hồ phụ theo dõi.
- Lưu ý pháp lý: Điều 50 Nghị định 117/2007/NĐ-CP không quy định công thức tính theo đầu người và người thuê không có quyền mặc nhiên buộc chủ trọ phải lắp đồng hồ riêng trong mọi trường hợp; mức thu thỏa thuận trong hợp đồng vẫn phải phù hợp quy định pháp luật bắt buộc.

**Giới hạn nguồn:**

- Tài liệu nguồn là 'HƯỚNG DẪN BIÊN SOẠN — không phải nguyên văn điều luật', các nội dung kiểm tra mang tính khuyến nghị thực tế chứ không phải quy định bắt buộc của pháp luật.


## Câu 11: Nếu nhà trọ dùng chung đồng hồ nước, cách phân chia chi phí nên được thỏa thuận ra sao?

### Chatbot với dữ liệu mới

Các bên nên thống nhất bằng văn bản phương pháp phân chia chi phí như theo đồng hồ phụ, số người và ngày ở, hoặc khoản cố định để đảm bảo minh bạch [1].

- Các bên thống nhất phương pháp tính chi phí cụ thể bằng văn bản thông qua đồng hồ phụ, số người thực tế cùng số ngày lưu trú hoặc khoản tiền cố định [1].
- Ghi rõ các nội dung về kỳ tính tiền, thuế, phí, lượng nước sử dụng tại khu vực chung và chi phí phát sinh do rò rỉ trong thỏa thuận [1].
- Xác định rõ cách thức kiểm tra, đối soát giữa các bên khi xuất hiện chênh lệch chỉ số tiêu thụ nước [1].
- Khuyến nghị xây dựng quy tắc riêng cho lượng nước dùng chung nếu áp dụng phương án chia tiền theo số ngày ở thực tế của mỗi người [1].

Các phương án phân chia chỉ nhằm mục đích minh bạch nội bộ và không phải là công thức bắt buộc chung theo quy định của pháp luật [1].
Quy định về hợp đồng dịch vụ cấp nước giữa đơn vị cấp nước và khách hàng không thay thế thỏa thuận nội bộ giữa người thuê và người thu tiền trọ [1].

Để áp dụng vào trường hợp của bạn:
- Nhà trọ của bạn hiện có lắp đồng hồ nước phụ riêng cho từng phòng hay không?
- Hợp đồng thuê trọ hiện tại đã có điều khoản nào thỏa thuận về tiền nước chưa?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

### Đáp án bạn gửi

Khi dùng chung đồng hồ nước tổng, các bên có thể thỏa thuận 1 trong 2 phương án:
1. **Phương án chia theo đầu người:** Lấy tổng số tiền trên hóa đơn nhà nước chia đều cho tổng số người thực tế đang cư trú tại dãy trọ trong tháng.
2. **Lắp đồng hồ nước phụ (tiểu ly) cho từng phòng:** Mỗi phòng tự thanh toán theo số m³ thực tế trên đồng hồ phụ; phần chênh lệch hao hụt hoặc nước dùng chung sân bãi sẽ chia đều cho các phòng theo tỷ lệ thỏa thuận. Đây là phương án minh bạch và ít phát sinh tranh chấp nhất.

### Nhận xét đối chiếu

**Ý khớp:**

- Các bên có thể thỏa thuận chia tiền nước theo đồng hồ phụ cho từng phòng.
- Các bên có thể thỏa thuận chia tiền nước theo số người thực tế cư trú.
- Cần có quy tắc/thỏa thuận xử lý đối với lượng nước dùng chung tại khu vực chung (sân bãi, hành lang).

**Thiếu so với đáp án:**

- Cách tính cụ thể của phương án theo đầu người: lấy tổng hóa đơn nhà nước chia đều cho tổng số người ở trong tháng.
- Đánh giá phương án lắp đồng hồ phụ là cách minh bạch và ít phát sinh tranh chấp nhất.

**Nội dung thêm:**

- Khuyến nghị thỏa thuận lập thành văn bản và có thể bổ sung phương án tính theo số ngày ở thực tế hoặc khoản tiền cố định.
- Cần quy định rõ các chi tiết: kỳ tính tiền, thuế/phí, chi phí phát sinh do rò rỉ và cơ chế kiểm tra, đối soát khi có chênh lệch chỉ số.
- Lưu ý pháp lý: Các phương án phân chia là thỏa thuận nội bộ nhằm minh bạch chứ không phải công thức luật định bắt buộc; hợp đồng cấp nước không thay thế thỏa thuận nội bộ này.

**Giới hạn nguồn:**

- Nội dung trả lời chủ yếu dựa trên 'HƯỚNG DẪN BIÊN SOẠN' của tài liệu nguồn (guidance), không phải trích dẫn nguyên văn quy định pháp luật bắt buộc.


## Câu 12: Tôi có thể đối chiếu tiền nước trên hóa đơn với đơn vị cấp nước như thế nào?

### Chatbot với dữ liệu mới

Bạn có thể đối chiếu tiền nước bằng cách lấy thông tin từ hóa đơn gốc để tra cứu trên cổng thông tin của đơn vị cấp nước hoặc yêu cầu đơn vị này xem xét lại số tiền [1] [2].

- Thu thập tên đơn vị, mã khách hàng, số hóa đơn và kỳ ghi số từ hóa đơn gốc để kiểm tra các chỉ số, khối lượng tiêu thụ, nhóm giá, thuế và phí [1].
- Truy cập cổng hddt.ctn-cantho.com.vn nếu thuộc Cấp thoát nước Cần Thơ, hoặc vào mục tra cứu từ trang capnuoccantho2.com.vn nếu thuộc Cấp nước Cần Thơ 2 [1].
- Đề nghị chủ trọ cung cấp bản hóa đơn hoặc cùng liên hệ đơn vị cấp nước nếu công tơ đứng tên chủ trọ thay vì tự ý dùng tài khoản của họ khi chưa được phép [1].
- Gửi yêu cầu đơn vị cấp nước xem xét lại số tiền nước phải thanh toán nếu phát hiện có sai lệch [2].
- Khuyến nghị liên hệ đơn vị cấp nước để hỏi về việc ghi số, rò rỉ, thủ tục kiểm tra đồng hồ và chi phí kiểm định trước khi yêu cầu nếu thấy chỉ số bất thường [1].

Đơn vị cấp nước có trách nhiệm giải quyết yêu cầu xem xét lại tiền nước trong thời hạn 15 ngày làm việc kể từ khi nhận được yêu cầu [2].
Trong thời gian chờ giải quyết khiếu nại, khách hàng sử dụng nước vẫn phải thanh toán tiền nước và đơn vị cấp nước không được ngừng dịch vụ cấp nước [2].

Để áp dụng vào trường hợp của bạn:
- Hóa đơn tiền nước hiện tại do chủ trọ tự lập hay do đơn vị cấp nước phát hành trực tiếp?
- Đơn vị cấp nước sạch tại khu vực phòng trọ của bạn tên là gì?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

### Đáp án bạn gửi

- Bạn có thể xem trên hóa đơn giấy/điện tử của chủ nhà để lấy **Mã khách hàng / Danh bộ** (thường in trên hóa đơn của Cantho Water).
- Truy cập website tra cứu hoặc cổng dịch vụ của **Công ty Cổ phần Cấp thoát nước Cần Thơ** (hoặc qua Zalo OA "Cấp thoát nước Cần Thơ") nhập mã danh bộ để kiểm tra chính xác sản lượng nước tiêu thụ và số tiền thực tế phải thanh toán.

### Nhận xét đối chiếu

**Ý khớp:**

- Lấy thông tin từ hóa đơn (mã khách hàng/danh bộ) để tra cứu thông tin tiền nước.
- Truy cập website/cổng tra cứu thông tin của đơn vị cấp nước (như Cấp thoát nước Cần Thơ) để kiểm tra lượng tiêu thụ và số tiền.

**Thiếu so với đáp án:**

- Kênh tra cứu qua Zalo OA "Cấp thoát nước Cần Thơ".

**Nội dung thêm:**

- Địa chỉ website/cổng tra cứu cụ thể: hddt.ctn-cantho.com.vn và capnuoccantho2.com.vn.
- Thu thập thêm số hóa đơn, kỳ ghi số để kiểm tra nhóm giá, thuế và phí.
- Xử lý khi công tơ đứng tên chủ trọ (đề nghị chủ trọ cung cấp hóa đơn hoặc cùng liên hệ đơn vị cấp nước).
- Quy trình khiếu nại theo Điều 48 Nghị định 117/2007/NĐ-CP: đơn vị giải quyết trong 15 ngày làm việc, khách hàng vẫn phải trả tiền và đơn vị không được cắt nước trong thời gian chờ giải quyết.

**Giới hạn nguồn:**

- Nguồn chunk 520 là hướng dẫn biên soạn thực tế, không phải nguyên văn văn bản quy phạm pháp luật.
- Quy định về thời hạn giải quyết khiếu nại 15 ngày và nghĩa vụ thanh toán căn cứ theo Điều 48 Nghị định 117/2007/NĐ-CP.


## Câu 13: Sinh viên thuê trọ tại Cần Thơ cần làm thủ tục cư trú nào?

### Chatbot với dữ liệu mới

Các đoạn trả lời trực tiếp trong nguồn:

- Luật Cư trú 68/2020/QH14 — Điều 27. Điều kiện đăng ký tạm trú | Khoản 1: “1. Công dân đến sinh sống tại chỗ ở hợp pháp ngoài phạm vi đơn vị hành
chính cấp xã nơi đã đăng ký thường trú để lao động, học tập hoặc vì mục đích
khác từ 30 ngày trở lên thì phải thực hiện đăng ký tạm trú.” [1].

- Luat-68-2020-QH14-doi-chieu-20261003 — Điều 27. Điều kiện đăng ký tạm trú | Khoản 1: “1. Công dân đến sinh sống tại chỗ ở hợp pháp ngoài phạm vi đơn vị hành chính cấp xã nơi đã đăng ký thường trú để lao động, học tập hoặc vì mục đích khác từ 30 ngày trở lên thì phải thực hiện đăng ký tạm trú.” [2].

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng, hiệu lực và bản gốc.

### Đáp án bạn gửi

Căn cứ theo **Điều 27 Luật Cư trú 2020**:
- Công dân đến sinh sống tại chỗ ở hợp pháp ngoài phạm vi đơn vị hành chính cấp xã nơi đã đăng ký thường trú từ **30 ngày trở lên** phải thực hiện **Đăng ký tạm trú**.
- **Thời hạn làm thủ tục:** Trong vòng **30 ngày** kể từ ngày chuyển đến phòng trọ mới.
- **Thời hạn tạm trú:** Tối đa là **02 năm** cho một lần đăng ký và có thể gia hạn nhiều lần.

### Nhận xét đối chiếu

**Ý khớp:**

- Căn cứ Điều 27 Luật Cư trú 2020 (Luật Cư trú số 68/2020/QH14).
- Thủ tục cần thực hiện là đăng ký tạm trú khi công dân đến sinh sống tại chỗ ở hợp pháp ngoài phạm vi xã nơi thường trú từ 30 ngày trở lên (để học tập, lao động...).

**Thiếu so với đáp án:**

- Thời hạn làm thủ tục: Trong vòng 30 ngày kể từ ngày chuyển đến chỗ ở mới.
- Thời hạn tạm trú: Tối đa là 02 năm cho một lần đăng ký và có thể gia hạn nhiều lần.

**Nội dung thêm:**

- Trích dẫn trực tiếp nguyên văn Khoản 1 Điều 27 Luật Cư trú 2020 quy định về mục đích học tập, lao động hoặc mục đích khác.

**Giới hạn nguồn:**

- Các nguồn trích dẫn cung cấp (Khoản 1 và Khoản 3 Điều 27 Luật Cư trú 2020) không chứa nội dung về thời hạn phải hoàn thành thủ tục trong vòng 30 ngày hay thời hạn tạm trú tối đa 02 năm như USER_REFERENCE nêu.


## Câu 14: Ai có trách nhiệm cung cấp thông tin, giấy tờ để người thuê đăng ký tạm trú?

### Chatbot với dữ liệu mới

Chưa đủ căn cứ xác định ai có trách nhiệm cung cấp thông tin, giấy tờ, nguồn chỉ nêu hồ sơ cần tờ khai thay đổi thông tin cư trú và giấy tờ chứng minh chỗ ở hợp pháp [1].

- Người đăng ký tạm trú chuẩn bị tờ khai thay đổi thông tin cư trú và giấy tờ, tài liệu chứng minh chỗ ở hợp pháp theo quy định [1].
- Trường hợp người đăng ký tạm trú là người chưa thành niên thì trong tờ khai phải ghi rõ ý kiến đồng ý của cha, mẹ hoặc người giám hộ, trừ khi đã có văn bản đồng ý [1].
- Người đăng ký tạm trú nộp hồ sơ đến cơ quan đăng ký cư trú nơi mình dự kiến tạm trú và nhận phiếu tiếp nhận hồ sơ [2].
- Cơ quan đăng ký cư trú thẩm định, cập nhật thông tin vào Cơ sở dữ liệu về cư trú và thông báo kết quả trong thời hạn 03 ngày làm việc kể từ khi nhận đủ hồ sơ hợp lệ [2].

Nguồn trích dẫn chưa nêu rõ nghĩa vụ của chủ nhà trọ trong việc cung cấp tài liệu cho người thuê [1].
Khuyến nghị đối chiếu thỏa thuận trong hợp đồng thuê nhà để xác định cụ thể bên chịu trách nhiệm cung cấp hồ sơ chỗ ở hợp pháp [1].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng.
Nguồn hiện có xác nhận nghĩa vụ của công dân và hồ sơ đăng ký; chưa có căn cứ riêng để kết luận toàn bộ nghĩa vụ cung cấp giấy tờ của chủ trọ.

Để áp dụng vào trường hợp của bạn:
- Hợp đồng thuê nhà giữa bạn và chủ trọ có điều khoản quy định bên nào hỗ trợ giấy tờ đăng ký tạm trú không?
- Bạn hay chủ nhà là bên dự kiến trực tiếp đứng tên nộp hồ sơ tại cơ quan đăng ký cư trú?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

### Đáp án bạn gửi

- **Trách nhiệm của chủ nhà trọ:** Phải tạo điều kiện, cung cấp thông tin chỗ ở hợp pháp, ký hợp đồng thuê và phối hợp làm thủ tục (hoặc chủ trọ có thể trực tiếp làm thủ tục đăng ký tạm trú thay cho người thuê trọ theo quy định).
- **Trách nhiệm của sinh viên:** Cung cấp ảnh CCCD, điền Tờ khai thay đổi thông tin cư trú (mẫu CT01).
- **Mức phạt nếu không đăng ký:** Theo Điều 9 Nghị định 144/2021/NĐ-CP, cả người thuê và chủ trọ không thực hiện đúng quy định về đăng ký tạm trú có thể bị phạt tiền từ **500.000 đến 1.000.000 đồng**.

### Nhận xét đối chiếu

**Ý khớp:**

- Cả hai đều đề cập đến việc người đăng ký tạm trú cần có tờ khai thay đổi thông tin cư trú và giấy tờ chứng minh chỗ ở hợp pháp.

**Thiếu so với đáp án:**

- Trách nhiệm cụ thể của chủ nhà trọ: tạo điều kiện, cung cấp thông tin chỗ ở hợp pháp, ký hợp đồng thuê và phối hợp làm thủ tục (hoặc trực tiếp làm thủ tục thay cho người thuê).
- Trách nhiệm cụ thể của sinh viên/người thuê: cung cấp ảnh CCCD, điền Tờ khai theo mẫu CT01.
- Mức xử phạt vi phạm hành chính từ 500.000 đến 1.000.000 đồng theo Điều 9 Nghị định 144/2021/NĐ-CP đối với người thuê và chủ trọ nếu không đăng ký đúng quy định.

**Nội dung khác:**

- USER_REFERENCE khẳng định rõ ràng trách nhiệm của chủ nhà trọ và người thuê; trong khi ANSWER cho rằng chưa đủ căn cứ pháp lý từ nguồn để xác định ai có trách nhiệm cung cấp giấy tờ và nguồn chưa nêu rõ nghĩa vụ của chủ nhà trọ (chưa xác minh bên nào đúng theo pháp luật hiện hành).

**Nội dung thêm:**

- Quy định đối với người chưa thành niên đăng ký tạm trú phải có ý kiến đồng ý của cha, mẹ hoặc người giám hộ trong tờ khai (hoặc văn bản đồng ý).
- Thủ tục nộp hồ sơ tại cơ quan đăng ký cư trú và thời hạn giải quyết, thông báo kết quả trong 03 ngày làm việc kể từ ngày nhận đủ hồ sơ hợp lệ.
- Khuyến nghị đối chiếu thỏa thuận trong hợp đồng thuê nhà để xác định bên chịu trách nhiệm cung cấp hồ sơ.

**Giới hạn nguồn:**

- Các trích dẫn pháp lý được cung cấp (Điều 28 Luật Cư trú 2020) chỉ quy định thành phần hồ sơ và trình tự giải quyết thủ tục đăng ký tạm trú, không có điều khoản quy định cụ thể về trách nhiệm cung cấp giấy tờ của chủ nhà trọ hay mức phạt vi phạm hành chính.
- USER_REFERENCE viện dẫn Nghị định 144/2021/NĐ-CP và mẫu CT01, nhưng các văn bản này hoàn toàn không có trong CONTEXTS được cung cấp.


## Câu 15: Tôi cần chuẩn bị những giấy tờ gì để đăng ký tạm trú tại phòng trọ?

### Chatbot với dữ liệu mới

Hồ sơ đăng ký tạm trú tại phòng trọ theo quy định gồm tờ khai thay đổi thông tin cư trú và giấy tờ chứng minh chỗ ở hợp pháp [1] [2].

- Chuẩn bị tờ khai thay đổi thông tin cư trú theo mẫu quy định [1].
- Chuẩn bị giấy tờ hoặc tài liệu chứng minh chỗ ở hợp pháp như hợp đồng thuê trọ đáp ứng điều kiện thủ tục [1] [2].
- Ghi rõ ý kiến đồng ý của cha mẹ hoặc người giám hộ trong tờ khai nếu người đăng ký là người chưa thành niên trừ khi đã có văn bản đồng ý riêng [1].
- Khuyến nghị chuẩn bị thông tin định danh, địa chỉ chính xác và xem biểu mẫu hiện tại tại cơ quan hoặc cổng chính thức trước khi nộp [2].

Trường hợp có dữ liệu khai thác được thì xử lý theo cơ chế dữ liệu chứ không bắt buộc danh sách bản sao giấy cho mọi trường hợp [2].

Để áp dụng vào trường hợp của bạn:
- Bạn là người đã thành niên hay chưa thành niên khi làm thủ tục đăng ký tạm trú?
- Bạn dự định nộp hồ sơ đăng ký tạm trú trực tiếp hay nộp trực tuyến qua cổng dịch vụ công?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

### Đáp án bạn gửi

Căn cứ **Điều 28 Luật Cư trú 2020**, hồ sơ gồm:
1. **Tờ khai thay đổi thông tin cư trú (Mẫu CT01)** (có chữ ký xác nhận đồng ý của chủ trọ/chủ sở hữu chỗ ở hợp pháp).
2. **Giấy tờ chứng minh chỗ ở hợp pháp:** Hợp đồng thuê nhà trọ hợp pháp còn hiệu lực (không bắt buộc công chứng).
3. **Bản sao CCCD/Thẻ căn cước** của người đăng ký.
*Hình thức nộp:* Sinh viên có thể nộp trực tiếp tại Công an phường/xã hoặc **nộp trực tuyến cực kỳ thuận tiện qua Cổng dịch vụ công Bộ Công an** hoặc **Ứng dụng VNeID (định danh mức 2)**.

### Nhận xét đối chiếu

**Ý khớp:**

- Cần chuẩn bị tờ khai thay đổi thông tin cư trú.
- Cần chuẩn bị giấy tờ, tài liệu chứng minh chỗ ở hợp pháp (như hợp đồng thuê phòng trọ).

**Thiếu so với đáp án:**

- Tên cụ thể của biểu mẫu là Mẫu CT01 và yêu cầu có chữ ký xác nhận đồng ý của chủ trọ/chủ sở hữu chỗ ở hợp pháp.
- Bản sao CCCD/Thẻ căn cước của người đăng ký.
- Hợp đồng thuê nhà trọ hợp pháp còn hiệu lực không bắt buộc công chứng.
- Hình thức nộp hồ sơ: nộp trực tiếp tại Công an phường/xã hoặc trực tuyến qua Cổng dịch vụ công Bộ Công an, Ứng dụng VNeID (định danh mức 2).

**Nội dung khác:**

- USER_REFERENCE liệt kê việc nộp bản sao CCCD/Thẻ căn cước, trong khi ANSWER nêu rõ nếu có dữ liệu khai thác được thì xử lý theo cơ chế dữ liệu chứ không bắt buộc danh sách bản sao giấy cho mọi trường hợp (chưa xác minh bên nào đúng theo quy định thực tế).

**Nội dung thêm:**

- Quy định riêng cho người chưa thành niên: phải ghi rõ ý kiến đồng ý của cha, mẹ hoặc người giám hộ trong tờ khai trừ khi đã có văn bản đồng ý riêng.
- Khuyến nghị chuẩn bị thông tin định danh, kiểm tra địa chỉ và biểu mẫu hiện tại trên cổng/cơ quan chính thức trước khi nộp.

**Giới hạn nguồn:**

- Trích đoạn nguồn số 2 là 'HƯỚNG DẪN BIÊN SOẠN — không phải nguyên văn điều luật', cần phân biệt với nguyên văn Điều 28 Luật Cư trú (nguồn số 1).
- Nội dung nguồn số 2 có viện dẫn các văn bản quy phạm như Thông tư 116/2026/TT-BCA, Luật 118/2025/QH15, Nghị định 154/2024/NĐ-CP cần kiểm tra hiệu lực áp dụng thực tế.


## Câu 16: Nếu chuyển sang phòng trọ khác, tôi cần cập nhật thông tin cư trú thế nào?

### Chatbot với dữ liệu mới

Khi chuyển sang chỗ ở ngoài nơi đã đăng ký tạm trú, công dân có trách nhiệm thực hiện đăng ký tạm trú mới, trừ trường hợp chỗ ở mới nằm trong phạm vi đơn vị hành chính cấp xã nơi đã đăng ký thường trú [1].

- Bạn cần thực hiện đăng ký tạm trú mới khi dọn đến chỗ ở khác nằm ngoài địa điểm đã đăng ký tạm trú trước đó [1].
- Nếu phòng trọ mới thuộc cùng xã nơi bạn đã đăng ký thường trú, cơ quan đăng ký cư trú sẽ rà soát và cập nhật thông tin nơi ở hiện tại vào Cơ sở dữ liệu về cư trú trong quá trình kiểm tra, quản lý [1].

Quy định tại văn bản này có hiệu lực thi hành kể từ ngày 01 tháng 7 năm 2026 [4].
Nguồn chưa cung cấp hồ sơ cụ thể, trình tự nộp giấy tờ cũng như thời hạn cần hoàn tất thủ tục đăng ký tạm trú mới [1].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng.

Để áp dụng vào trường hợp của bạn:
- Phòng trọ mới của bạn có thuộc cùng xã, phường nơi bạn đang có đăng ký thường trú hay không?
- Bạn đã từng đăng ký tạm trú tại phòng trọ cũ trước khi chuyển đi chưa?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

### Đáp án bạn gửi

- Khi chuyển sang chỗ ở trọ mới ngoài xã/phường cũ: Trong thời hạn 30 ngày, bạn phải làm thủ tục **đăng ký tạm trú tại chỗ ở mới**. Khi công an xã/phường mới duyệt tạm trú, hệ thống Cơ sở dữ liệu quốc gia về dân cư sẽ **tự động xóa đăng ký tạm trú tại nơi ở cũ**.
- Nếu chuyển trọ cùng xã/phường nhưng đổi địa chỉ: Làm thủ tục điều chỉnh thông tin về cư trú trên Cổng dịch vụ công/VNeID.

### Nhận xét đối chiếu

**Ý khớp:**

- Khi chuyển sang chỗ ở mới ngoài nơi đã đăng ký tạm trú, công dân cần thực hiện thủ tục đăng ký tạm trú mới.

**Thiếu so với đáp án:**

- Thời hạn thực hiện đăng ký tạm trú tại chỗ ở mới là trong vòng 30 ngày.
- Cơ sở dữ liệu quốc gia về dân cư sẽ tự động xóa đăng ký tạm trú tại nơi ở cũ sau khi cơ quan công an phê duyệt nơi mới.
- Trường hợp chuyển trọ cùng xã/phường nhưng đổi địa chỉ thì thực hiện thủ tục điều chỉnh thông tin về cư trú trên Cổng dịch vụ công/VNeID.

**Nội dung khác:**

- Xử lý khi chuyển trọ trong cùng phạm vi xã: USER_REFERENCE hướng dẫn làm thủ tục điều chỉnh thông tin về cư trú (qua Cổng Dịch vụ công/VNeID); trong khi ANSWER nêu trường hợp chỗ ở mới thuộc cùng xã nơi đăng ký thường trú thì cơ quan đăng ký cư trú sẽ rà soát, cập nhật thông tin nơi ở hiện tại trong quá trình kiểm tra, quản lý cư trú (chưa xác minh bên nào đúng theo quy định hiện hành).

**Nội dung thêm:**

- Lưu ý quy định trích dẫn từ Thông tư 116/2026/TT-BCA có hiệu lực từ ngày 01/07/2026.
- Nêu rõ các nguồn cung cấp chưa có thông tin chi tiết về thành phần hồ sơ và trình tự nộp giấy tờ.

**Giới hạn nguồn:**

- Trích dẫn Thông tư 116/2026/TT-BCA có hiệu lực từ ngày 01/07/2026, cần lưu ý áp dụng đúng thời điểm có hiệu lực thi hành.
- Các nguồn văn bản cung cấp không có thông tin về thời hạn 30 ngày hay cơ chế tự động xóa đăng ký tạm trú cũ như trong USER_REFERENCE.


## Câu 17: Khi xem phòng trọ, tôi nên kiểm tra những điều kiện phòng cháy, chữa cháy nào?

### Chatbot với dữ liệu mới

Khi xem phòng trọ là nhà ở thông thường, bạn cần kiểm tra lối thoát nạn, phương tiện phòng cháy chữa cháy thực tế, an toàn thiết bị điện và vị trí đun nấu theo luật định [1] [2].

- Khuyến nghị kiểm tra việc bố trí, duy trì lối thoát nạn, lối ra khẩn cấp hoặc lối đi bảo đảm việc thoát nạn thông thoáng [1] [2] [3].
- Khuyến nghị xem xét sự sẵn có của các phương tiện phòng cháy, chữa cháy phù hợp với điều kiện thực tế của ngôi nhà [1] [2] [3].
- Khuyến nghị kiểm tra hệ thống dây dẫn điện, thiết bị điện trong nhà và khu vực sạc xe điện xem có giải pháp ngăn cháy an toàn không [1] [2].
- Khuyến nghị quan sát khu vực đun nấu, thờ cúng để bảo đảm không để các chất dễ cháy gần nguồn lửa và nguồn nhiệt [1] [2] [3].
- Trường hợp nhà ở có kết hợp kinh doanh, khuyến nghị kiểm tra thêm biển cấm, biển báo chỉ dẫn và giải pháp ngăn cách khu vực kinh doanh với nơi ở [3].

Nhà ở có quy chuẩn kỹ thuật hoặc thuộc danh mục cơ sở quản lý về phòng cháy và chữa cháy phải áp dụng tiêu chuẩn riêng hoặc quy định đối với cơ sở [1] [2] [3].
Quy định trang bị bình chữa cháy và thiết bị truyền tin báo cháy đối với nhà ở tại thành phố trực thuộc Trung ương không bảo đảm hạ tầng giao thông hoặc nguồn nước áp dụng theo lộ trình của Chính phủ [2].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng.
Cần đối chiếu điều/khoản được dẫn chiếu còn thiếu; đoạn trích chưa đủ để kết luận toàn bộ điều kiện và ngoại lệ.

Để áp dụng vào trường hợp của bạn:
- Khu trọ bạn dự định thuê thuộc loại hình nhà ở riêng lẻ hay cơ sở thuộc diện quản lý phòng cháy và chữa cháy?
- Nhà trọ nằm ở tỉnh, thành phố nào và có kết hợp sản xuất, kinh doanh hàng hóa không?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

### Đáp án bạn gửi

Khi đi xem phòng, sinh viên cần quan sát trực tiếp 5 yếu tố sinh mạng sau:
1. **Lối thoát hiểm thứ hai:** Ngoài cửa chính đi vào, phòng hoặc tầng trọ có ban công, lối lên mái thông sang nhà bên cạnh, hoặc thang thoát hiểm bên ngoài không?
2. **Chuồng cọp / Rào sắt lồng bảo vệ:** Nếu ban công bị rào chắn (chuồng cọp), bắt buộc phải có **cửa mở thoát hiểm khẩn cấp** và chìa khóa treo ngay cạnh cửa.
3. **Thiết bị PCCC tại chỗ:** Hành lang có trang bị **bình chữa cháy xách tay** (bình bột ABC hoặc khí CO2) còn nguyên chốt kẹp chì, đồng hồ áp suất vạch xanh hay không.
4. **Hệ thống điện:** Đường dây điện có được đi trong ống gen bảo vệ không? Có aptomat (CB) riêng tự ngắt khi chập điện không?
5. **Khu vực để xe:** Chỗ để xe máy/xe đạp điện có lối đi thông thoáng không, hay bị bít kín chắn ngang cửa thoát nạn chính?

### Nhận xét đối chiếu

**Ý khớp:**

- Kiểm tra lối thoát hiểm/lối thoát nạn và lối ra khẩn cấp bảo đảm thông thoáng.
- Kiểm tra sự sẵn có của các phương tiện phòng cháy, chữa cháy tại chỗ.
- Kiểm tra an toàn hệ thống đường dây điện và thiết bị điện trong nhà.

**Thiếu so với đáp án:**

- Chi tiết kiểm tra chuồng cọp/rào sắt lồng bảo vệ ban công phải có cửa mở thoát hiểm khẩn cấp và chìa khóa treo cạnh cửa.
- Chi tiết kiểm tra bình chữa cháy xách tay (loại bột ABC/CO2, còn kẹp chì, kim đồng hồ áp suất ở vạch xanh).
- Chi tiết kiểm tra dây điện đi trong ống gen và có aptomat (CB) ngắt tự động riêng.
- Quan sát cụ thể lối thoát nạn thứ hai qua ban công, lối lên mái thông sang nhà bên cạnh hoặc thang thoát hiểm bên ngoài.
- Kiểm tra khu vực để xe máy/xe đạp điện xem có bít kín chắn ngang cửa thoát nạn chính hay không.

**Nội dung thêm:**

- Kiểm tra khu vực đun nấu, nơi thờ cúng để bảo đảm không để chất dễ cháy gần nguồn lửa, nguồn nhiệt.
- Kiểm tra khu vực sạc xe điện về giải pháp ngăn cháy theo quy định.
- Trường hợp nhà trọ kết hợp kinh doanh: kiểm tra biển cấm, biển chỉ dẫn và giải pháp ngăn cách khu vực kinh doanh với nơi ở.
- Lưu ý các quy định riêng đối với cơ sở thuộc diện quản lý PCCC và lộ trình trang bị bình chữa cháy, thiết bị truyền tin báo cháy tại các thành phố trực thuộc Trung ương.

**Giới hạn nguồn:**

- Các nguồn trích dẫn quy định chung về an toàn PCCC đối với nhà ở (Điều 20) và nhà ở kết hợp sản xuất, kinh doanh (Điều 21 Luật PCCC và CNCH), không quy định riêng danh mục kiểm tra cụ thể dành riêng cho người đi thuê/xem phòng trọ.
- Quy định trang bị bình chữa cháy và thiết bị truyền tin báo cháy tại thành phố trực thuộc Trung ương áp dụng theo lộ trình của Chính phủ và khu vực do UBND cấp tỉnh xác định.


## Câu 18: Nhà trọ có nhiều phòng cần đáp ứng những yêu cầu an toàn cháy nổ nào?

### Chatbot với dữ liệu mới

Nhà trọ cần bảo đảm an toàn điện, nguồn lửa, nguồn nhiệt, lối thoát nạn và phương tiện chữa cháy tùy theo việc áp dụng quy định nhà ở thông thường, nhà ở kết hợp kinh doanh hay cơ sở thuộc diện quản lý [2] [3].

- Lắp đặt, sử dụng dây dẫn và thiết bị điện bảo đảm an toàn, thường xuyên kiểm tra, sửa chữa và có giải pháp an toàn tại nơi sạc xe điện [1] [2].
- Bố trí nơi đun nấu, thờ cúng an toàn và không để đồ dễ cháy nổ gần nguồn lửa hoặc nguồn nhiệt [1] [2] [3].
- Bố trí và duy trì lối thoát nạn, lối ra khẩn cấp hoặc lối đi thoát nạn thông thoáng, sẵn sàng phương tiện phòng cháy chữa cháy phù hợp thực tế [1] [2] [3].
- Trường hợp là nhà ở kết hợp sản xuất kinh doanh thì phải gắn biển báo theo quy định và có giải pháp ngăn cách với khu vực để ở [3].
- Trường hợp thuộc danh mục cơ sở quản lý thì phải có nội quy, phương án chữa cháy, trang bị phương tiện, truyền tin báo cháy và phân công người hoặc lập lực lượng phòng cháy chữa cháy [2].

Chưa đủ căn cứ xác định các điều kiện cụ thể nếu chưa rõ quy mô, số tầng, diện tích hoặc việc công trình có thuộc danh mục cơ sở diện quản lý phòng cháy chữa cháy hay không [1] [2] [3].
Khuyến nghị người thuê và chủ nhà đối chiếu trực tiếp hồ sơ công trình với cơ quan có thẩm quyền để áp dụng đúng quy chuẩn kỹ thuật [2] [3].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng.
Cần xác định loại hình sử dụng, số tầng, diện tích và quy chuẩn của nhà trọ để chọn đúng nhóm điều kiện; chưa kết luận chỉ từ số phòng.
Cần đối chiếu điều/khoản được dẫn chiếu còn thiếu; đoạn trích chưa đủ để kết luận toàn bộ điều kiện và ngoại lệ.

Để áp dụng vào trường hợp của bạn:
- Nhà trọ của bạn có bao nhiêu tầng và thuộc loại hình nhà ở riêng lẻ cho thuê hay cơ sở kinh doanh độc lập?
- Nhà trọ có nằm trong khu vực không bảo đảm hạ tầng giao thông hoặc nguồn nước chữa cháy tại thành phố trực thuộc Trung ương không?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

### Đáp án bạn gửi

Theo quy định tại Nghị định 136/2020/NĐ-CP, Nghị định 50/2024/NĐ-CP và Chỉ thị 19/CT-TTg (2024):
- Nhà trọ phải có **nội quy, tiêu lệnh PCCC**, biển chỉ dẫn thoát nạn (đèn Exit/đèn sự cố nếu quy mô từ nhiều tầng trở lên).
- Phải bố trí giải pháp **ngăn cháy lan** giữa khu vực để xe máy/xe điện với khu vực phòng ở và cầu thang bộ thoát hiểm.
- Có tối thiểu **2 lối thoát nạn độc lập**; không để đồ đạc, hàng quán lấn chiếm hành lang và cầu thang.
- Đảm bảo đủ số lượng bình chữa cháy xách tay (bình quân 1 bình/50–100 m² sàn, mỗi tầng tối thiểu 2 bình).
- Người quản lý/chủ nhà trọ phải được tập huấn nghiệp vụ PCCC.

### Nhận xét đối chiếu

**Ý khớp:**

- Cần bảo đảm lối thoát nạn thông thoáng, bố trí lối thoát hiểm/lối ra khẩn cấp.
- Phải có giải pháp an toàn, ngăn cách/ngăn cháy liên quan đến khu vực sạc xe điện hoặc khu vực kinh doanh với khu vực để ở.
- Trang bị phương tiện phòng cháy chữa cháy phù hợp thực tế.
- Cần có nội quy, biển báo/biển chỉ dẫn và phân công người/lực lượng PCCC (đối với cơ sở thuộc diện quản lý).

**Thiếu so với đáp án:**

- Yêu cầu cụ thể có tối thiểu 2 lối thoát nạn độc lập.
- Định mức cụ thể về bình chữa cháy (1 bình/50–100 m² sàn, mỗi tầng tối thiểu 2 bình).
- Yêu cầu người quản lý/chủ nhà trọ phải được tập huấn nghiệp vụ PCCC.
- Dẫn chiếu các văn bản: Nghị định 136/2020/NĐ-CP, Nghị định 50/2024/NĐ-CP, Chỉ thị 19/CT-TTg.

**Nội dung khác:**

- Cách tiếp cận căn cứ pháp lý: USER_REFERENCE viện dẫn Nghị định 136/2020, Nghị định 50/2024 và Chỉ thị 19/CT-TTg; trong khi ANSWER căn cứ vào Luật PCCC và CNCH (Luật số 55/2024/QH15) phân loại theo nhà ở thông thường, nhà ở kết hợp kinh doanh và cơ sở thuộc diện quản lý (chưa xác minh văn bản nào áp dụng chính xác cho tình huống thực tế).

**Nội dung thêm:**

- Yêu cầu an toàn về hệ thống điện sinh hoạt, dây dẫn, thường xuyên kiểm tra và thiết bị sạc xe điện theo Điều 24.
- Yêu cầu an toàn nơi đun nấu, thờ cúng, không để đồ dễ cháy gần nguồn lửa, nguồn nhiệt.
- Quy định về thiết bị truyền tin báo cháy kết nối cơ sở dữ liệu đối với nhà ở tại thành phố trực thuộc Trung ương nơi hạ tầng giao thông/nguồn nước không bảo đảm.

**Giới hạn nguồn:**

- Các trích dẫn pháp lý trong ngữ cảnh (Điều 20, 21, 23, 24) thuộc Luật PCCC và CNCH mới (Luật 55/2024/QH15 / VBHN 58), không chứa các số liệu chi tiết về số lượng bình chữa cháy trên m² hay yêu cầu cụ thể tối thiểu 2 lối thoát nạn độc lập như trong USER_REFERENCE.


## Câu 19: Nếu lối thoát nạn bị khóa hoặc bị chặn, người thuê nên làm gì?

### Chatbot với dữ liệu mới

Nếu lối thoát bị khóa hoặc chặn, người thuê cần thông báo chủ trọ yêu cầu khắc phục, tìm phương án ra ngoài an toàn và ưu tiên thoát nạn, gọi 114 khi có nguy hiểm trực tiếp [1].

- Thông báo ngay cho chủ trọ để yêu cầu khắc phục tình trạng cửa hoặc lối thoát bị khóa, bị chặn và chủ động tìm phương án ra ngoài an toàn [1].
- Khi xảy ra cháy hoặc nguy hiểm trực tiếp, ưu tiên thoát nạn ngay lập tức, cảnh báo cho người khác, gọi 114 và tuyệt đối không quay lại lấy tài sản [1].
- Nếu tình trạng cản trở lối thoát kéo dài, người thuê lưu lại hình ảnh khi bảo đảm an toàn và phản ánh tới cơ quan công an hoặc PCCC địa phương [1].
- Khuyến nghị ghi rõ vị trí, thời gian cửa bị khóa, số người bị ảnh hưởng và các lần đã thông báo để phục vụ cơ quan kiểm tra xử lý [1].

Việc xác định vi phạm và mức phạt phải căn cứ theo loại công trình, hành vi thực tế và văn bản xử phạt đã được sửa đổi thay vì áp dụng trực tiếp từ hình ảnh đơn lẻ [1].
Mức phạt tiền theo quy định áp dụng với cá nhân, trong khi tổ chức có cùng hành vi vi phạm sẽ bị phạt gấp hai lần [4].

Để áp dụng vào trường hợp của bạn:
- Lối thoát nạn hiện đang bị ai khóa hoặc chặn và chủ trọ đã nhận được phản ánh chưa?
- Nhà trọ bạn đang thuê thuộc loại hình nhà ở riêng lẻ, chung cư mini hay dãy phòng trọ?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

### Đáp án bạn gửi

1. **Yêu cầu chủ nhà giải phóng ngay chướng ngại vật:** Góp ý trực tiếp hoặc nhắn tin vào nhóm trọ yêu cầu dọn dẹp xe cộ, đồ đạc chắn lối đi/cầu thang và mở cửa thoát hiểm ban công/sân thượng.
2. **Chìa khóa khẩn cấp:** Đề nghị chủ trọ cung cấp chìa khóa hoặc đặt hộp chứa chìa khóa thoát hiểm đập kính tại cửa thoát nạn.
3. **Phản ánh đến chính quyền địa phương:** Nếu chủ trọ cố tình phớt lờ, sinh viên có thể phản ánh đến **Công an phường/xã hoặc Đội Cảnh sát PCCC & CNCH quận/huyện** để kiểm tra an toàn PCCC cơ sở trọ theo chuyên đề của Thủ tướng Chính phủ.

### Nhận xét đối chiếu

**Ý khớp:**

- Yêu cầu chủ trọ khắc phục ngay tình trạng lối thoát/cửa thoát nạn bị khóa hoặc bị chặn.
- Báo cáo, phản ánh tới cơ quan công an hoặc lực lượng PCCC địa phương khi tình trạng không được xử lý.

**Thiếu so với đáp án:**

- Đề nghị chủ trọ cung cấp chìa khóa khẩn cấp hoặc lắp hộp chứa chìa khóa thoát hiểm đập kính tại cửa thoát nạn.
- Chi tiết cách yêu cầu: góp ý trực tiếp hoặc nhắn tin vào nhóm trọ yêu cầu dọn dẹp xe cộ, đồ đạc chắn lối đi/cầu thang và mở cửa thoát hiểm ban công/sân thượng.

**Nội dung thêm:**

- Khi có cháy hoặc nguy hiểm trực tiếp: ưu tiên thoát nạn ngay, cảnh báo người khác, gọi 114 và không quay lại lấy tài sản.
- Lưu lại hình ảnh bảo đảm an toàn, ghi rõ vị trí, thời gian bị khóa, số người bị ảnh hưởng và số lần đã thông báo để phục vụ cơ quan kiểm tra xử lý.
- Lưu ý việc xác định vi phạm, mức xử phạt căn cứ theo loại công trình, hành vi thực tế và nguyên tắc phạt tổ chức gấp 2 lần cá nhân.

**Giới hạn nguồn:**

- Nguồn 1 là hướng dẫn biên soạn thực tế, không phải nguyên văn văn bản quy phạm pháp luật.
- Cần lưu ý các văn bản sửa đổi Nghị định 106/2025/NĐ-CP (như Nghị định 69/2026/NĐ-CP, Nghị định 347/2026/NĐ-CP) khi tra cứu chế tài cụ thể.


## Câu 20: Chủ trọ và người thuê có trách nhiệm gì đối với thiết bị điện và an toàn cháy nổ?

### Chatbot với dữ liệu mới

Chủ nhà có trách nhiệm tuyên truyền và đôn đốc an toàn phòng cháy chữa cháy, trong khi người thuê trọ có trách nhiệm tuân thủ quy định an toàn, sử dụng điện đúng cách và kiểm tra khắc phục nguy cơ cháy nổ trừ khi có thỏa thuận khác [1] [2] [3].

- Người thuê cần sử dụng điện, nguồn lửa, nguồn nhiệt và các phương tiện phòng cháy đúng quy định nhằm tránh gây nguy hiểm cháy nổ [1].
- Người thuê có trách nhiệm thường xuyên tự kiểm tra để kịp thời phát hiện và khắc phục nguy cơ gây cháy nổ, tai nạn hoặc sự cố [2] [3].
- Chủ cho thuê trọ thực hiện tuyên truyền, đôn đốc và nhắc nhở người thuê thực hiện đúng các quy định pháp luật về phòng cháy, chữa cháy và cứu nạn, cứu hộ [2].
- Khuyến nghị các bên thống nhất đầu mối tiếp nhận thông tin báo hỏng thiết bị điện trong nhà trọ [1].
- Khuyến nghị dừng ngay việc sử dụng thiết bị điện có dấu hiệu nóng, bốc mùi khét hoặc phóng điện và yêu cầu người có chuyên môn đến xử lý [1].

Thỏa thuận về việc ai chịu trách nhiệm sửa chữa thiết bị trong hợp đồng không làm thay đổi các nghĩa vụ an toàn mà pháp luật quy định cho từng bên [1].
Trường hợp thuê nhà ở kết hợp sản xuất kinh doanh thì người thuê còn phải bảo đảm thêm các điều kiện an toàn phòng cháy theo quy định riêng [2].

Để áp dụng vào trường hợp của bạn:
- Hợp đồng thuê trọ của bạn hiện có điều khoản thỏa thuận riêng nào về trách nhiệm bảo trì thiết bị điện không?
- Nhà trọ bạn đang thuê là nhà ở đơn thuần hay có kết hợp hoạt động sản xuất, kinh doanh?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

### Đáp án bạn gửi

- **Trách nhiệm của chủ trọ:**
  - Đầu tư hệ thống điện đạt chuẩn an toàn, lắp aptomat chống giật/quá tải cho từng phòng và toàn dãy trọ.
  - Bảo dưỡng, thay thế bình PCCC định kỳ khi hết hạn; hướng dẫn người thuê kỹ năng PCCC.
- **Trách nhiệm của sinh viên (người thuê):**
  - Không tự ý câu móc, đấu nối dây điện bừa bãi hoặc dùng các thiết bị tiêu thụ công suất quá lớn gây quá tải.
  - Tắt các thiết bị điện sinh nhiệt (bếp từ, bàn ủi, ấm siêu tốc) khi ra khỏi phòng.
  - Chú ý an toàn khi sạc pin xe máy điện/xe đạp điện (không sạc liên tục qua đêm khi không có người trông coi hoặc tại nơi dễ cháy).

### Nhận xét đối chiếu

**Ý khớp:**

- Chủ trọ có trách nhiệm tuyên truyền, đôn đốc, nhắc nhở/hướng dẫn người thuê về an toàn phòng cháy chữa cháy.
- Người thuê có trách nhiệm sử dụng điện đúng quy định, bảo đảm an toàn phòng chống cháy nổ.

**Thiếu so với đáp án:**

- Trách nhiệm của chủ trọ: Đầu tư hệ thống điện đạt chuẩn an toàn, lắp aptomat chống giật/quá tải cho từng phòng và toàn dãy trọ.
- Trách nhiệm của chủ trọ: Bảo dưỡng, thay thế bình PCCC định kỳ khi hết hạn.
- Trách nhiệm cụ thể của người thuê: Không tự ý câu móc, đấu nối bừa bãi hoặc dùng thiết bị công suất quá lớn gây quá tải.
- Trách nhiệm cụ thể của người thuê: Tắt các thiết bị điện sinh nhiệt (bếp từ, bàn ủi, ấm siêu tốc) khi ra khỏi phòng.
- Trách nhiệm cụ thể của người thuê: Chú ý an toàn khi sạc pin xe máy điện/xe đạp điện (không sạc qua đêm không người trông coi, không sạc nơi dễ cháy).

**Nội dung thêm:**

- Người thuê có trách nhiệm thường xuyên tự kiểm tra để phát hiện, khắc phục nguy cơ cháy nổ, sự cố.
- Thỏa thuận sửa chữa thiết bị trong hợp đồng không làm thay đổi nghĩa vụ an toàn pháp luật quy định cho từng bên.
- Trường hợp thuê nhà ở kết hợp sản xuất kinh doanh thì người thuê phải bảo đảm thêm các điều kiện PCCC theo luật định.
- Khuyến nghị thống nhất đầu mối báo hỏng và dừng sử dụng ngay thiết bị có dấu hiệu nóng, khét, phóng điện.

**Giới hạn nguồn:**

- Nguồn 1 là hướng dẫn biên soạn thực tế, không phải nguyên văn điều luật.
- Các trách nhiệm cụ thể trong USER_REFERENCE (aptomat, sạc xe điện, bình PCCC, tắt bàn ủi/ấm siêu tốc) là các biện pháp an toàn thực tế nhưng không có trong trích đoạn Luật PCCC được cung cấp.


## Câu 21: Người giới thiệu phòng trọ và thu phí môi giới cần công khai những thông tin gì?

### Chatbot với dữ liệu mới

Nếu thuộc đối tượng điều chỉnh của Luật Kinh doanh bất động sản, người môi giới phải cung cấp đầy đủ và trung thực hồ sơ cùng thông tin bất động sản, đồng thời nêu rõ thông tin các bên, nội dung, phí và điều khoản thanh toán trong hợp đồng dịch vụ [3].

- Yêu cầu bên môi giới cung cấp đầy đủ, trung thực hồ sơ và thông tin liên quan đến phòng trọ cũng như trách nhiệm về thông tin cung cấp theo quy định [3].
- Kiểm tra hợp đồng dịch vụ để bảo đảm có đủ thông tin về bên cung cấp, nội dung, kết quả thực hiện, mức phí, thời hạn thanh toán và phương thức giải quyết tranh chấp [3].
- Khuyến nghị người thuê hỏi rõ tên doanh nghiệp, người trực tiếp thực hiện, phạm vi được giao, căn cứ quyền cho thuê và mức phí cụ thể trước khi sử dụng dịch vụ [3].

Cần phân biệt rõ giữa cá nhân giới thiệu phòng trọ thông thường và chủ thể kinh doanh dịch vụ môi giới bất động sản chịu sự điều chỉnh của Luật Kinh doanh bất động sản [3].
Không được dùng riêng quy định về giá dịch vụ theo Bộ luật Dân sự để thay thế cho nghĩa vụ minh bạch hồ sơ bất động sản [3].

Để áp dụng vào trường hợp của bạn:
- Người giới thiệu phòng trọ cho bạn là cá nhân tự do hay thuộc tổ chức kinh doanh dịch vụ môi giới?
- Hai bên đã lập văn bản hợp đồng dịch vụ thể hiện mức phí và thông tin bên cung cấp chưa?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

### Đáp án bạn gửi

Theo quy định của Luật Kinh doanh Bất động sản 2023:
- Người hành nghề môi giới BĐS phải công khai: Họ tên, số điện thoại, chứng chỉ hành nghề môi giới (nếu hoạt động độc lập/doanh nghiệp), biểu phí dịch vụ môi giới.
- Thông tin phòng trọ cung cấp phải **trung thực, chính xác**: Giá thuê thực tế, tiền cọc, chi phí điện nước, tình trạng pháp lý và hiện trạng phòng ở.

### Nhận xét đối chiếu

**Ý khớp:**

- Phải cung cấp đầy đủ, trung thực thông tin/hồ sơ liên quan đến phòng trọ/bất động sản.
- Phải công khai thông tin về phí dịch vụ/biểu phí môi giới và thông tin bên môi giới.

**Thiếu so với đáp án:**

- Các thông tin cụ thể của người hành nghề: họ tên, số điện thoại, chứng chỉ hành nghề môi giới.
- Các thông tin cụ thể về phòng trọ cần cung cấp: giá thuê thực tế, tiền cọc, chi phí điện nước, tình trạng pháp lý và hiện trạng phòng ở.

**Nội dung thêm:**

- Nêu rõ phạm vi điều chỉnh: phân biệt cá nhân giới thiệu thông thường với chủ thể chịu sự điều chỉnh của Luật Kinh doanh bất động sản.
- Nội dung cần có trong hợp đồng dịch vụ: thời hạn thanh toán, phương thức giải quyết tranh chấp.
- Lưu ý không dùng riêng quy định về giá dịch vụ theo Bộ luật Dân sự để thay thế nghĩa vụ minh bạch hồ sơ bất động sản.
- Khuyến nghị thực tế về việc kiểm tra tư cách pháp nhân, thẩm quyền và căn cứ quyền cho thuê.

**Giới hạn nguồn:**

- Chunk [3] là 'HƯỚNG DẪN BIÊN SOẠN — không phải nguyên văn điều luật', chứa khuyến nghị và phân tích diễn giải, không phải văn bản quy phạm pháp luật trực tiếp.
- Các trích dẫn Bộ luật Dân sự (Điều 513, Điều 519) chỉ quy định chung về hợp đồng dịch vụ và giá dịch vụ, không quy định cụ thể danh mục thông tin phải công khai khi môi giới phòng trọ.


## Câu 22: Trước khi chuyển tiền cho người môi giới, tôi nên kiểm tra quyền cho thuê và thông tin phòng như thế nào?

### Chatbot với dữ liệu mới

Trước khi chuyển tiền, bạn cần đối chiếu danh tính người nhận tiền, thông tin phòng cụ thể, tư cách của người có quyền cho thuê và căn cứ đại diện hoặc cho thuê lại [1].

- Kiểm tra danh tính người nhận tiền, thông tin căn phòng thực tế và người có quyền cho thuê [1].
- Xác minh căn cứ ủy quyền đại diện hoặc quyền cho thuê lại nếu người làm việc không phải chủ sở hữu [1].
- Kiểm tra đơn vị công tác và thẩm quyền nhận phí hoặc nhận cọc theo hồ sơ nếu làm việc với môi giới chuyên nghiệp [1].
- Khuyến nghị hẹn xem phòng trực tiếp, kiểm tra sự thống nhất giữa địa chỉ và bên cho thuê, đồng thời ghi rõ người nhận và mục đích thanh toán trên chứng từ [1].

Giao dịch cho thuê nhà ở không bắt buộc phải có Giấy chứng nhận quyền sở hữu nên việc thiếu giấy này không tự đủ để kết luận là lừa đảo [1] [3].
Người môi giới không tự đương nhiên có quyền nhận tiền đặt cọc thay cho chủ nhà [1].

Để áp dụng vào trường hợp của bạn:
- Người môi giới đang yêu cầu bạn chuyển khoản khoản tiền gì?
- Người cho thuê đã cung cấp giấy tờ chứng minh quyền sở hữu hoặc giấy ủy quyền nào chưa?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

### Đáp án bạn gửi

- **Nguyên tắc vàng:** **Tuyệt đối không chuyển tiền cọc xem phòng hay phí giữ chỗ** cho người tự xưng là môi giới khi chưa đến xem phòng trực tiếp và chưa gặp chủ nhà.
- Khi đến xem phòng, yêu cầu người môi giới chỉ rõ: Ai là chủ nhà trọ thực sự? Có văn bản ủy quyền cho thuê không?
- Hợp đồng thuê và tiền cọc phải được **ký và trao trực tiếp cho chủ nhà** (kèm xem CCCD đối chiếu giấy tờ nhà). Khoản phí hoa hồng môi giới thông thường do chủ nhà trọ chi trả, không phải nghĩa vụ của sinh viên trừ khi có thỏa thuận riêng từ trước.

### Nhận xét đối chiếu

**Ý khớp:**

- Khuyến nghị xem phòng trực tiếp trước khi giao dịch.
- Kiểm tra tư cách chủ nhà thực sự, căn cứ ủy quyền/đại diện nếu người làm việc không phải chủ sở hữu.
- Lưu ý về việc người môi giới không đương nhiên có quyền nhận cọc thay cho chủ nhà.

**Thiếu so với đáp án:**

- Nguyên tắc tuyệt đối không chuyển tiền cọc xem phòng hay phí giữ chỗ khi chưa xem phòng và chưa gặp chủ nhà.
- Hợp đồng thuê và tiền cọc phải được ký và trao trực tiếp cho chủ nhà (kèm xem CCCD đối chiếu giấy tờ nhà).
- Phí hoa hồng môi giới thông thường do chủ nhà chi trả, không phải nghĩa vụ của sinh viên/người thuê trừ khi có thỏa thuận riêng.

**Nội dung khác:**

- USER_REFERENCE đặt yêu cầu cứng là hợp đồng và cọc phải ký/trao trực tiếp cho chủ nhà kèm đối chiếu giấy tờ nhà; trong khi ANSWER nêu rõ pháp luật cho phép giao dịch thuê nhà không bắt buộc phải có Giấy chứng nhận quyền sở hữu (thiếu giấy không tự đủ kết luận lừa đảo) và người môi giới có thể nhận cọc nếu có thẩm quyền/hồ sơ ủy quyền.

**Nội dung thêm:**

- Kiểm tra đơn vị công tác và thẩm quyền nhận phí hoặc nhận cọc của môi giới chuyên nghiệp theo hồ sơ.
- Ghi rõ người nhận và mục đích thanh toán trên chứng từ.
- Lưu ý pháp lý: Giao dịch cho thuê nhà ở không bắt buộc phải có Giấy chứng nhận quyền sở hữu (theo Luật Nhà ở Điều 160).

**Giới hạn nguồn:**

- Nguồn 1 (chunk 486) là tài liệu hướng dẫn thực tế/biên soạn, không phải nguyên văn điều luật.
- Điều 160 Khoản 2 Luật Nhà ở (chunk 605) quy định trường hợp cho thuê nhà ở không bắt buộc phải có Giấy chứng nhận, cần lưu ý chưa xác minh tính bắt buộc của việc kiểm tra giấy tờ quyền sở hữu như USER_REFERENCE nêu.


## Câu 23: Nếu người môi giới đưa thông tin khác với phòng thực tế, người thuê có thể làm gì?

### Chatbot với dữ liệu mới

Các đoạn trả lời trực tiếp trong nguồn:

- Hướng dẫn thực tế: CHỦ ĐỀ: Môi giới và phí xem phòng — Q: Nếu người môi giới đưa thông tin khác với phòng thực tế, người thuê có thể làm gì?: “HƯỚNG DẪN BIÊN SOẠN — không phải nguyên văn điều luật.
### Q: Nếu người môi giới đưa thông tin khác với phòng thực tế, người thuê có thể làm gì?

A: Đối chiếu tin đăng, thông tin môi giới cung cấp và cam kết dịch vụ với phòng thực tế. Nếu thuộc môi giới chuyên nghiệp, Điều 65 quy định nghĩa vụ trung thực và bồi thường thiệt hại do lỗi; trong quan hệ dịch vụ, BLDS quy định nghĩa vụ thực hiện và trách nhiệm phù hợp. Có thể yêu cầu sửa thông tin, thực hiện đúng, thương lượng hoàn phí hoặc bồi thường khi có căn cứ. Hoàn toàn bộ phí và cọc không tự động phát sinh từ mọi sai khác; cần xem tính chất sai khác, hợp đồng, người nhận cọc và thiệt hại.

**Khuyến nghị thực tế:** Lưu ảnh/tin đăng và cam kết trước thanh toán, lập bảng các sai khác, gửi yêu cầu với chứng cứ và số tiền cụ thể.

**Căn cứ:**

- [Văn bản hợp nhất 06/VBHN-VPQH năm 2025 — Luật Kinh doanh bất động sản](https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-06-vbhn-vpqh-44399/55348.htm) — Điều 65.
- [Bộ luật Dân sự 91/2015/QH13](https://datafiles.chinhphu.vn/cpp/files/vbpq/2016/01/91.signed.pdf) — Điều 360, 513–519.” [1].

- Luật-29-2023-QH15 — Điều 65. Nghĩa vụ của doanh nghiệp kinh doanh dịch vụ môi giới bất động sản, cá nhân hành nghề môi giới bất động sản | Khoản 1: “1. Doanh nghiệp kinh doanh dịch vụ môi giới bất động sản có các nghĩa vụ sau đây:

a) Cung cấp đầy đủ, trung thực hồ sơ, thông tin về bất động sản do mình môi giới và chịu trách nhiệm về hồ sơ, thông tin do mình cung cấp;

b) Tổ chức đào tạo, bồi dưỡng nâng cao kiến thức hành nghề môi giới bất động sản cho nhân viên môi giới bất động sản làm việc trong doanh nghiệp hằng năm;

c) Thực hiện nghĩa vụ thuế đối với Nhà nước;

d) Bồi thường thiệt hại do lỗi của mình gây ra;

đ) Thực hiện chế độ báo cáo theo quy định của pháp luật và chịu sự kiểm tra, thanh tra của cơ quan nhà nước có thẩm quyền;

e) Nghĩa vụ khác theo hợp đồng.” [3].

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng, hiệu lực và bản gốc.

### Đáp án bạn gửi

- Bạn có toàn quyền **từ chối thuê và từ chối thanh toán bất kỳ khoản phí môi giới nào** vì người môi giới đã cung cấp thông tin sai sự thật, vi phạm nguyên tắc trung thực theo Luật Kinh doanh Bất động sản.
- Nếu người môi giới đã ép bạn đóng phí "dẫn đi xem phòng" từ trước, bạn có quyền yêu cầu hoàn trả và báo cáo sự việc với ban quản trị nền tảng hoặc cơ quan công an nếu có dấu hiệu cưỡng đoạt/lừa đảo.

### Nhận xét đối chiếu

**Ý khớp:**

- Môi giới có nghĩa vụ cung cấp thông tin trung thực theo Luật Kinh doanh bất động sản (Điều 65).
- Người thuê có thể yêu cầu hoàn phí/thương lượng hoàn trả khoản phí dịch vụ đã nộp.

**Thiếu so với đáp án:**

- Quyền từ chối thuê căn phòng.
- Báo cáo sự việc với ban quản trị nền tảng hoặc cơ quan công an nếu có dấu hiệu cưỡng đoạt hoặc lừa đảo.

**Nội dung khác:**

- Điều kiện và phạm vi hoàn phí/từ chối phí: USER_REFERENCE cho rằng người thuê có toàn quyền từ chối trả bất kỳ khoản phí môi giới nào hoặc đòi lại toàn bộ phí dẫn đi xem; trong khi ANSWER (dẫn từ hướng dẫn) nêu việc hoàn toàn bộ phí và cọc không tự động phát sinh từ mọi sai khác mà cần thương lượng có căn cứ, xem xét tính chất sai khác, hợp đồng và thiệt hại (chưa xác minh quan điểm nào đúng theo quy định áp dụng).

**Nội dung thêm:**

- Khuyến nghị đối chiếu tin đăng, lưu bằng chứng/ảnh chụp, lập bảng sai khác và gửi yêu cầu cụ thể.
- Yêu cầu sửa đổi thông tin hoặc bồi thường thiệt hại khi có căn cứ theo Điều 65 Luật Kinh doanh bất động sản và Bộ luật Dân sự.

**Giới hạn nguồn:**

- Đoạn trả lời của ANSWER dựa một phần vào tài liệu biên soạn nội bộ ('HƯỚNG DẪN BIÊN SOẠN — không phải nguyên văn điều luật'), cần phân biệt với nguyên văn quy định tại Điều 65 Luật Kinh doanh bất động sản 2023.


## Câu 24: Khoản phí môi giới nên được thỏa thuận và thể hiện trong giấy tờ ra sao?

### Chatbot với dữ liệu mới

Các đoạn trả lời trực tiếp trong nguồn:

- Hướng dẫn thực tế: CHỦ ĐỀ: Môi giới và phí xem phòng — Q: Khoản phí môi giới nên được thỏa thuận và thể hiện trong giấy tờ ra sao?: “HƯỚNG DẪN BIÊN SOẠN — không phải nguyên văn điều luật.
### Q: Khoản phí môi giới nên được thỏa thuận và thể hiện trong giấy tờ ra sao?

A: Với hợp đồng kinh doanh dịch vụ bất động sản thuộc luật chuyên ngành, Điều 44 quy định hình thức văn bản; khoản 4 Điều 46 nêu nội dung chính gồm phí/thù lao/hoa hồng, phương thức và thời hạn thanh toán cùng các nội dung dịch vụ. Trong quan hệ giới thiệu/dịch vụ dân sự khác, hình thức và giá xét theo Điều 119 và các điều 513–519 BLDS; không áp điều kiện chuyên ngành khi chưa xác định phạm vi. Phí môi giới phải phân biệt với tiền cọc thuê và khoản thu hộ.

**Khuyến nghị thực tế:** Ghi số tiền/cách tính, sự kiện được hưởng phí, lúc trả, điều kiện hoàn, bên nhận và chứng từ; một phiếu chuyển tiền không thay đủ nội dung hợp đồng.

**Căn cứ:**

- [Văn bản hợp nhất 06/VBHN-VPQH năm 2025 — Luật Kinh doanh bất động sản](https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-06-vbhn-vpqh-44399/55348.htm) — Điều 44, Điều 46 khoản 4, Điều 63.
- [Bộ luật Dân sự 91/2015/QH13](https://datafiles.chinhphu.vn/cpp/files/vbpq/2016/01/91.signed.pdf) — Điều 119, 513–519.
- [LuatVietnam — Luật Kinh doanh bất động sản 29/2023/QH15](https://luatvietnam.vn/dat-dai/luat-kinh-doanh-bat-dong-san-cua-quoc-hoi-so-29-2023-qh15-284798-d1.html) — Bản luật đối chiếu.” [3].

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng, hiệu lực và bản gốc.

### Đáp án bạn gửi

- Phí môi giới phải được lập thành **Hợp đồng dịch vụ môi giới** hoặc phiếu thu có chữ ký xác nhận của hai bên.
- Giấy tờ phải ghi rõ: Mức phí dịch vụ, điều kiện phát sinh phí (chỉ trả khi ký kết hợp đồng thuê trọ thành công), cam kết hoàn tiền nếu giao dịch không thành do lỗi của bên môi giới.

### Nhận xét đối chiếu

**Ý khớp:**

- Cần lập thành văn bản/hợp đồng dịch vụ thể hiện khoản phí môi giới.
- Giấy tờ cần nêu rõ số tiền/mức phí, sự kiện phát sinh/thời điểm trả phí và điều kiện hoàn tiền.

**Thiếu so với đáp án:**

- Đề xuất có thể dùng phiếu thu có chữ ký xác nhận của hai bên thay thế/bổ sung.
- Điều kiện cụ thể: chỉ trả khi ký kết hợp đồng thuê trọ thành công và cam kết hoàn tiền nếu giao dịch không thành do lỗi của bên môi giới.

**Nội dung khác:**

- Về hình thức chứng từ: USER_REFERENCE gợi ý có thể lập thành phiếu thu có chữ ký xác nhận của hai bên, trong khi ANSWER (dẫn từ khuyến nghị nguồn) lưu ý một phiếu chuyển tiền không thay đủ nội dung hợp đồng (chưa xác minh bên nào đúng theo quy định bắt buộc).

**Nội dung thêm:**

- Phân biệt giữa hợp đồng kinh doanh dịch vụ bất động sản (Luật Kinh doanh bất động sản: Điều 44, khoản 4 Điều 46) và dịch vụ dân sự thông thường (Bộ luật Dân sự 2015: Điều 119, Điều 513–519).
- Lưu ý phân biệt phí môi giới với tiền cọc thuê và các khoản thu hộ.
- Khuyến nghị ghi rõ phương thức thanh toán, bên nhận và chứng từ kèm theo.

**Giới hạn nguồn:**

- Trích dẫn trong ANSWER xuất phát từ tài liệu 'Hướng dẫn thực tế' (editorial_guidance) có ghi chú rõ 'HƯỚNG DẪN BIÊN SOẠN — không phải nguyên văn điều luật'.
- Các điều luật trích dẫn (Điều 44, 46 LKDBĐS; Điều 119, 513-519 BLDS) cần được tra cứu văn bản gốc để xác định đúng phạm vi áp dụng đối với từng loại hình giao dịch môi giới.


## Câu 25: Khi tìm phòng qua một nền tảng trực tuyến, tôi nên kiểm tra người đăng và nguồn tin như thế nào?

### Chatbot với dữ liệu mới

Khi tìm phòng trên nền tảng trực tuyến, bạn cần đối chiếu người đăng với người có quyền cho thuê, kiểm tra thực tế phòng và không phụ thuộc hoàn toàn vào dấu xác minh [1].

- Khuyến nghị đối chiếu người đăng với người có quyền cho thuê, kiểm tra địa chỉ, phòng thực tế, hình ảnh và thời điểm đăng tin [1].
- Khuyến nghị hỏi rõ các khoản thu, điều kiện đặt cọc và sắp xếp lịch xem phòng trực tiếp [1].
- Khuyến nghị tự đối chiếu địa chỉ, trực tiếp gặp bên cho thuê và kiểm tra tình trạng phòng trên thực tế [1].
- Khuyến nghị lưu lại đường dẫn URL hoặc mã tin đăng để kịp thời đối chiếu khi thông tin bị thay đổi [1].

Dấu xác minh của nền tảng chỉ có ý nghĩa theo quy trình xác minh do họ công bố, không bảo đảm quyền cho thuê hoặc tình trạng phòng còn trống [1].

Để áp dụng vào trường hợp của bạn:
- Nền tảng bạn đang xem có hiển thị thông tin quy trình cấp dấu xác minh không?
- Bạn đã liên hệ trực tiếp để hẹn lịch kiểm tra phòng và giấy tờ quyền cho thuê chưa?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

### Đáp án bạn gửi

- **Kiểm tra tài khoản người đăng:** Tài khoản mới tạo hay đã hoạt động lâu năm? Có tích xanh xác thực danh tính không? Lịch sử đăng tin có nhiều phòng ảo giá rẻ bất thường không?
- **Kiểm tra hình ảnh tin đăng:** Sử dụng tính năng "Tìm kiếm bằng hình ảnh trên Google" để kiểm tra xem ảnh phòng trọ có bị copy từ các khách sạn, căn hộ cao cấp khác ở TP.HCM/Hà Nội hay không.
- **Cảnh giác mức giá "quá hời":** Ví dụ phòng máy lạnh full nội thất tại Ninh Kiều mà đăng giá chỉ 800k - 1 triệu đồng là 99% bẫy lừa cọc.

### Nhận xét đối chiếu

**Ý khớp:**

- Cần kiểm tra thông tin về người đăng và các yếu tố liên quan đến dấu xác minh/tích xanh.
- Cần kiểm tra hình ảnh của tin đăng.

**Thiếu so với đáp án:**

- Kiểm tra cụ thể thời gian tạo tài khoản (mới tạo hay lâu năm) và lịch sử đăng tin có nhiều phòng ảo giá rẻ bất thường hay không.
- Sử dụng công cụ tìm kiếm hình ảnh bằng Google để kiểm tra xem ảnh phòng có bị sao chép từ khách sạn, căn hộ khác hay không.
- Cảnh giác trước mức giá quá rẻ bất thường (ví dụ phòng máy lạnh full nội thất giá 800k - 1 triệu đồng là bẫy cọc).

**Nội dung khác:**

- Về dấu xác minh/tích xanh: USER_REFERENCE gợi ý kiểm tra xem tài khoản có tích xanh xác thực danh tính không như một tiêu chí đánh giá uy tín; trong khi ANSWER cảnh báo dấu xác minh của nền tảng chỉ có ý nghĩa theo quy trình xác minh của họ và không bảo đảm quyền cho thuê hay tình trạng phòng trống (chưa xác minh quan điểm nào tối ưu hơn).

**Nội dung thêm:**

- Đối chiếu người đăng với người thực tế có quyền cho thuê phòng.
- Hỏi rõ các khoản thu, điều kiện đặt cọc và sắp xếp lịch xem phòng trực tiếp.
- Lưu lại đường dẫn URL hoặc mã tin đăng để kịp thời đối chiếu khi thông tin bị thay đổi.

**Giới hạn nguồn:**

- Nội dung hướng dẫn kiểm tra tin đăng trọ bắt nguồn từ 'HƯỚNG DẪN BIÊN SOẠN — không phải nguyên văn điều luật' và khuyến cáo thực tế (như khuyến cáo của Công an Cần Thơ), không phải quy phạm pháp luật bắt buộc.


## Câu 26: Nếu một tin đăng nhà trọ có thông tin sai, tôi có thể báo cáo cho nền tảng bằng cách nào?

### Chatbot với dữ liệu mới

Bạn có thể báo cáo tin đăng sai thông qua kênh tiếp nhận phản ánh hoặc khiếu nại được nền tảng công bố trong mục hỗ trợ hoặc quy chế hoạt động [1].

- Tìm kiếm kênh tiếp nhận phản ánh, khiếu nại tại mục hỗ trợ hoặc trong quy chế hoạt động của nền tảng [1].
- Khuyến nghị chuẩn bị thông tin gửi đi gồm đường dẫn URL hoặc mã tin đăng, chỉ rõ phần thông tin sai lệch kèm ảnh chụp đối chiếu và yêu cầu đề nghị xử lý [1].
- Khuyến nghị thực hiện che mờ hoặc ẩn các dữ liệu cá nhân của những người không liên quan trước khi gửi nội dung phản ánh [1].
- Khuyến nghị lưu lại mã số tiếp nhận phản ánh từ nền tảng để tiện theo dõi tiến độ giải quyết vi phạm [1].

Không khẳng định giao diện của mọi nền tảng đều có sẵn nút báo cáo trực tiếp khi chưa kiểm tra thực tế trên từng nền tảng cụ thể [1].
Quy định về việc công khai phương thức tiếp nhận và xử lý vi phạm áp dụng đối với các nền tảng thuộc phạm vi điều chỉnh của Luật Thương mại điện tử [1].

Để áp dụng vào trường hợp của bạn:
- Bạn đang xem tin đăng phòng trọ trên website hay ứng dụng cụ thể nào?
- Thông tin sai lệch trong tin đăng trọ là về giá cả, vị trí hay tiện ích?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

### Đáp án bạn gửi

- Sử dụng nút **"Báo cáo tin đăng" (Report)** trực tiếp trên giao diện của website/ứng dụng đó, chọn lý do như: "Tin giả/Phòng không có thật", "Sai giá thuê", "Có dấu hiệu lừa đảo cọc".
- Đính kèm ảnh chụp tin nhắn bằng chứng nếu người đăng yêu cầu chuyển khoản qua link lạ hoặc có hành vi gian dối.

### Nhận xét đối chiếu

**Ý khớp:**

- Cần chuẩn bị/đính kèm hình ảnh làm bằng chứng đối chiếu thông tin sai lệch khi báo cáo.

**Thiếu so với đáp án:**

- Sử dụng trực tiếp nút 'Báo cáo tin đăng' (Report) trên giao diện website/ứng dụng và chọn lý do cụ thể (như tin giả, sai giá, lừa đảo cọc).
- Trường hợp cụ thể đính kèm ảnh chụp tin nhắn bằng chứng khi người đăng yêu cầu chuyển khoản qua link lạ hoặc có hành vi gian dối.

**Nội dung khác:**

- Phương thức báo cáo: USER_REFERENCE khẳng định bấm trực tiếp nút 'Báo cáo tin đăng' trên giao diện, trong khi ANSWER (dựa vào hướng dẫn) nêu không khẳng định giao diện có sẵn nút báo cáo mà hướng dẫn tìm kênh phản ánh/khiếu nại tại mục hỗ trợ hoặc quy chế hoạt động của nền tảng (chưa xác minh bên nào đúng trên mọi nền tảng thực tế).

**Nội dung thêm:**

- Chuẩn bị thêm đường dẫn URL hoặc mã tin đăng và nêu rõ yêu cầu đề nghị xử lý.
- Khuyến nghị che mờ/ẩn dữ liệu cá nhân của người không liên quan trước khi gửi phản ánh.
- Khuyến nghị lưu lại mã số tiếp nhận phản ánh để theo dõi tiến độ giải quyết.
- Nêu phạm vi áp dụng theo Luật Thương mại điện tử về nghĩa vụ công khai phương thức tiếp nhận và xử lý vi phạm của nền tảng.

**Giới hạn nguồn:**

- Thông tin trong nguồn xuất phát từ 'HƯỚNG DẪN BIÊN SOẠN — không phải nguyên văn điều luật', cần phân biệt nội dung khuyến nghị thực tế với quy định pháp luật viện dẫn (Điều 11, Điều 15 Luật Thương mại điện tử 122/2025/QH15).


## Câu 27: Nền tảng đăng tin có trách nhiệm gì đối với thông tin người bán hoặc người cho thuê theo tài liệu hiện có?

### Chatbot với dữ liệu mới

Chưa đủ căn cứ từ tài liệu hiện có để kết luận chi tiết toàn bộ trách nhiệm đối với thông tin người cho thuê ngoài việc phải phân loại nền tảng và việc xác thực danh tính không đồng nghĩa nền tảng bảo đảm phòng trọ hợp pháp [1].

- Khuyến nghị người thuê đọc kỹ loại dịch vụ và quy chế hoạt động của nền tảng để nắm rõ phạm vi dịch vụ [1].
- Khuyến nghị người thuê chủ động hỏi rõ phạm vi xác minh danh tính người đăng tin phòng trọ [1].
- Nền tảng trung gian có đặt hàng trực tuyến phải cung cấp thông tin cần thiết hỗ trợ các bên giải quyết phản ánh và tranh chấp [2].
- Nền tảng trung gian có đặt hàng trực tuyến phải tạm ngừng hoặc chấm dứt tài khoản người bán khi có yêu cầu của cơ quan nhà nước có thẩm quyền [2].

Tài liệu hiện có chưa cung cấp đầy đủ nội dung nguyên văn về nghĩa vụ xác thực thông tin tại khoản 1 Điều 17 của Luật Thương mại điện tử [1].
Luật Thương mại điện tử 122/2025/QH15 có hiệu lực thi hành từ ngày 01 tháng 7 năm 2026 [4].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng.
Cần đối chiếu điều/khoản được dẫn chiếu còn thiếu; đoạn trích chưa đủ để kết luận toàn bộ điều kiện và ngoại lệ.

Để áp dụng vào trường hợp của bạn:
- Nền tảng bạn đang sử dụng là mạng xã hội, trang đăng tin đơn thuần hay có chức năng đặt hàng trực tuyến?
- Nền tảng có công bố quy chế xác thực danh tính và thông tin của người đăng tin cho thuê phòng không?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

### Đáp án bạn gửi

Căn cứ theo **Nghị định 52/2013/NĐ-CP** (được sửa đổi bởi **Nghị định 85/2021/NĐ-CP**) về thương mại điện tử:
- Nền tảng có trách nhiệm: Yêu cầu người đăng tin cung cấp thông tin định danh (tên, số điện thoại, địa chỉ);
- Phải thiết lập cơ chế tiếp nhận khiếu nại, phản ánh và **ngăn chặn, gỡ bỏ ngay lập tức** các tin đăng vi phạm pháp luật, tin đăng giả mạo hoặc lừa đảo;
- Cung cấp thông tin của đối tượng vi phạm cho cơ quan công an khi có yêu cầu điều tra.

### Nhận xét đối chiếu

**Khác biệt câu hỏi tham chiếu:** Nền tảng đăng tin có trách nhiệm gì đối với thông tin người cho thuê theo tài liệu hiện có?

**Ý khớp:**

- Cả hai đều đề cập đến việc nền tảng có trách nhiệm liên quan đến tiếp nhận, xử lý, hỗ trợ giải quyết phản ánh, khiếu nại hoặc tranh chấp.
- Cả hai đều ghi nhận trách nhiệm xử lý (tạm ngừng/chấm dứt tài khoản hoặc cung cấp thông tin/ngăn chặn tin vi phạm) khi có yêu cầu của cơ quan nhà nước có thẩm quyền.

**Thiếu so với đáp án:**

- Yêu cầu người đăng tin cung cấp thông tin định danh cụ thể (tên, số điện thoại, địa chỉ).
- Trách nhiệm ngăn chặn, gỡ bỏ ngay lập tức các tin đăng vi phạm pháp luật, tin đăng giả mạo hoặc lừa đảo.
- Cung cấp thông tin của đối tượng vi phạm cho cơ quan công an khi có yêu cầu điều tra.

**Nội dung khác:**

- Căn cứ pháp lý viện dẫn: USER_REFERENCE áp dụng Nghị định 52/2013/NĐ-CP (sửa đổi bởi Nghị định 85/2021/NĐ-CP); trong khi ANSWER dựa vào Luật Thương mại điện tử 122/2025/QH15 và tài liệu biên soạn nội bộ (chưa xác minh bên nào đúng theo pháp luật hiện hành).
- Kết luận về mức độ đầy đủ của dữ liệu: USER_REFERENCE khẳng định danh sách trách nhiệm cụ thể đối với người đăng tin; còn ANSWER cho rằng chưa đủ căn cứ từ tài liệu hiện có để kết luận chi tiết toàn bộ trách nhiệm và nội dung khoản 1 Điều 17 chưa có nguyên văn.

**Nội dung thêm:**

- Lưu ý việc xác thực danh tính không đồng nghĩa nền tảng bảo đảm phòng trọ hợp pháp.
- Cần phân loại nền tảng (chỉ đăng tin, trung gian, mạng xã hội, có hay không có chức năng đặt hàng trực tuyến).
- Hiệu lực của Luật Thương mại điện tử 122/2025/QH15 là từ ngày 01/07/2026.
- Khuyến nghị người thuê đọc kỹ quy chế và chủ động hỏi phạm vi xác minh của nền tảng.

**Giới hạn nguồn:**

- Đoạn chunk 414 là 'HƯỚNG DẪN BIÊN SOẠN — không phải nguyên văn điều luật', chỉ mang tính diễn giải định hướng, không phải văn bản quy phạm pháp luật trực tiếp.
- Tài liệu trích dẫn không có nguyên văn khoản 1 Điều 17 Luật 122/2025/QH15 (khoản quy định về trách nhiệm chung/xác thực danh tính người bán), do đó các kết luận về nghĩa vụ cụ thể bị giới hạn.


## Câu 28: Nếu người đăng yêu cầu chuyển cọc qua liên kết lạ, tôi nên kiểm tra những dấu hiệu nào trước khi trả tiền?

### Chatbot với dữ liệu mới

Bạn cần dừng thao tác thanh toán để kiểm tra tên miền, tài khoản thụ hưởng và sự thống nhất với hợp đồng khi chưa rõ người nhận và mục đích [1].

- Kiểm tra tên miền bằng cách tự mở trang chính thức riêng thay vì bấm vào liên kết lạ [1].
- Kiểm tra tên tài khoản thụ hưởng và tính thống nhất với thông tin trong thỏa thuận hoặc hợp đồng thuê [1].
- Tuyệt đối không nhập mã OTP hoặc cung cấp mật khẩu cá nhân cho người đăng tin [1].
- Khuyến nghị tách việc kiểm tra phòng trọ, xác minh bên nhận cọc và rà soát đường thanh toán thành ba bước độc lập [1].
- Khuyến nghị lưu lại toàn bộ lịch sử giao tiếp nếu người đăng yêu cầu thay đổi tài khoản hoặc gửi liên kết thanh toán mới [1].

Sự xuất hiện của liên kết, mã QR, logo hay dấu xác minh không chứng minh giao dịch đó là an toàn [1].
Các khuyến cáo phòng ngừa rủi ro là biện pháp an toàn và chưa phải kết luận người gửi liên kết phạm tội [1].

Để áp dụng vào trường hợp của bạn:
- Bạn đã lỡ cung cấp mã OTP, mật khẩu hay thông tin tài khoản qua liên kết lạ đó chưa?
- Người đăng tin có lập hợp đồng hoặc văn bản thỏa thuận đặt cọc trước khi yêu cầu chuyển tiền không?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

### Đáp án bạn gửi

**Dấu hiệu cảnh báo lừa đảo chiếm đoạt tài khoản:**
1. Bắt nhấn vào liên kết lạ (đường link rút gọn như bit.ly, link giả mạo ngân hàng, cổng thanh toán giả) để "xác nhận giữ phòng" hoặc "nhận mã hoàn cọc".
2. Yêu cầu nhập số tài khoản ngân hàng, mật khẩu internet banking hoặc **mã OTP**.
3. Hối thúc dồn dập: "Đang có nhiều người muốn thuê, chuyển ngay trong 15 phút nếu không sẽ mất phòng".
*Quy tắc an toàn:* Tuyệt đối không bao giờ nhấp link lạ hoặc cung cấp mã OTP cho bất kỳ ai.

### Nhận xét đối chiếu

**Ý khớp:**

- Cảnh báo việc không bấm/nhấp vào liên kết lạ và thay vào đó cần tự kiểm tra hoặc mở trang chính thức riêng.
- Tuyệt đối không nhập hoặc cung cấp mã OTP, mật khẩu cá nhân cho người đăng tin.

**Thiếu so với đáp án:**

- Dấu hiệu dùng các dạng link rút gọn (như bit.ly), link giả mạo ngân hàng hoặc cổng thanh toán giả danh nghĩa 'xác nhận giữ phòng' hay 'nhận mã hoàn cọc'.
- Yêu cầu nhập số tài khoản ngân hàng.
- Hành vi hối thúc dồn dập (ví dụ: giục chuyển tiền trong 15 phút kẻo mất phòng).

**Nội dung thêm:**

- Kiểm tra tên miền, tên tài khoản thụ hưởng và tính thống nhất với hợp đồng/thỏa thuận thuê.
- Sự xuất hiện của mã QR, logo hay dấu xác minh không bảo đảm giao dịch an toàn.
- Khuyến nghị tách việc kiểm tra phòng, xác minh bên nhận cọc và rà soát đường thanh toán thành 3 bước độc lập.
- Lưu lại lịch sử giao tiếp khi có yêu cầu đổi tài khoản hoặc gửi liên kết mới.
- Lưu ý các biện pháp cảnh báo là phòng ngừa an toàn, chưa kết luận người gửi liên kết phạm tội.

**Giới hạn nguồn:**

- Tài liệu nguồn được dán nhãn 'HƯỚNG DẪN BIÊN SOẠN — không phải nguyên văn điều luật', chỉ mang tính chất hướng dẫn nghiệp vụ và cảnh báo thực tế, không trích dẫn trực tiếp điều luật cụ thể.


## Câu 29: Chủ trọ có thể yêu cầu tôi cung cấp những thông tin cá nhân nào để làm hợp đồng và đăng ký cư trú?

### Chatbot với dữ liệu mới

Các đoạn trả lời trực tiếp trong nguồn:

- Luat-68-2020-QH14-doi-chieu-20261003 — Điều 28. Hồ sơ, thủ tục đăng ký tạm trú, gia hạn tạm trú | Khoản 1: “1. Hồ sơ đăng ký tạm trú bao gồm:
a) Tờ khai thay đổi thông tin cư trú; đối với người đăng ký tạm trú là người chưa thành niên thì trong tờ khai phải ghi rõ ý kiến đồng ý của cha, mẹ hoặc người giám hộ, trừ trường hợp đã có ý kiến đồng ý bằng văn bản;
b) Giấy tờ, tài liệu chứng minh chỗ ở hợp pháp.” [1].

- Hướng dẫn thực tế: CHỦ ĐỀ: Căn cước, số điện thoại và dữ liệu cá nhân — Q: Chủ trọ có thể yêu cầu tôi cung cấp những thông tin cá nhân nào để làm hợp đồng và đăng ký cư trú?: “HƯỚNG DẪN BIÊN SOẠN — không phải nguyên văn điều luật.
### Q: Chủ trọ có thể yêu cầu tôi cung cấp những thông tin cá nhân nào để làm hợp đồng và đăng ký cư trú?

A: Cần thông tin định danh, liên hệ và thông tin cư trú phù hợp mục đích ký hợp đồng/đăng ký, nhưng phải xác định dữ liệu thực sự cần và căn cứ xử lý. Luật Bảo vệ dữ liệu cá nhân yêu cầu xử lý đúng phạm vi, mục đích; có trường hợp không cần sự đồng ý tại Điều 19, không có nghĩa được thu mọi dữ liệu. Thủ tục cư trú theo Thông tư 116 ưu tiên khai thác dữ liệu khi đủ điều kiện; không mặc định phải giao ảnh toàn bộ căn cước cho chủ trọ.

**Khuyến nghị thực tế:** Hỏi mục đích từng thông tin, người được truy cập và thời gian giữ; tránh gửi dữ liệu ngân hàng, OTP hoặc thông tin gia đình không phục vụ thủ tục.

**Căn cứ:**

- [Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15](https://bocongan.gov.vn/chinh-sach-phap-luat/co-so-du-lieu-van-ban/luat-bao-ve-du-lieu-ca-nhan-1753688803) — Điều 3, 9, 19.
- [Văn bản hợp nhất 79/VBHN-VPQH — Luật Nhà ở](https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-79-vbhn-vpqh-469209.htm) — Điều 163 khoản 1.
- [Thông tư 116/2026/TT-BCA — đăng ký, quản lý cư trú](https://vanban.bocongan.gov.vn/co-so-du-lieu-van-ban/thong-tu-quy-dinh-chi-tiet-mot-so-dieu-va-bien-phap-thi-hanh-luat-cu-tru-1784261073) — Điều 3 khoản 5–6 và hồ sơ cư trú.” [2].

- 2026_204_79_VBHN-VPQH — Điều 163. Hợp đồng về nhà ở | Khoản 1: “Hợp đồng về nhà ở do các bên thỏa thuận và phải được lập thành văn bản bao gồm các nội dung sau đây:

1. Họ và tên của cá nhân, tên của tổ chức và địa chỉ của các bên;” [3].

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng, hiệu lực và bản gốc.

### Đáp án bạn gửi

- Chủ trọ chỉ có quyền yêu cầu các **thông tin cơ bản cần thiết phục vụ cho việc lập hợp đồng và đăng ký tạm trú** theo quy định pháp luật: Họ và tên, Ngày tháng năm sinh, Số CCCD/Định danh cá nhân, Địa chỉ thường trú, Số điện thoại liên hệ, Giấy xác nhận là sinh viên (nếu có chính sách ưu đãi).
- Chủ trọ **không có quyền** đòi hỏi các thông tin nhạy cảm như: Mật khẩu mạng xã hội, thông tin tài khoản ngân hàng, thu nhập chi tiết của cha mẹ hay lịch sử duyệt web.

### Nhận xét đối chiếu

**Ý khớp:**

- Cần cung cấp các thông tin cơ bản phục vụ ký hợp đồng và đăng ký cư trú (thông tin định danh, họ tên, địa chỉ, liên hệ).
- Không phải và tránh cung cấp các thông tin nhạy cảm/không phục vụ thủ tục (như dữ liệu ngân hàng, thông tin gia đình không liên quan).

**Thiếu so với đáp án:**

- Danh sách liệt kê cụ thể các loại giấy tờ/thông tin như: Ngày tháng năm sinh, Số CCCD/Định danh cá nhân, Giấy xác nhận là sinh viên (nếu có ưu đãi).
- Các ví dụ thông tin nhạy cảm bị cấm đòi hỏi cụ thể: Mật khẩu mạng xã hội, thu nhập chi tiết của cha mẹ, lịch sử duyệt web.

**Nội dung thêm:**

- Trích dẫn quy định Điều 28 Luật Cư trú về thành phần hồ sơ đăng ký tạm trú (Tờ khai thay đổi thông tin cư trú, giấy tờ chứng minh chỗ ở hợp pháp, ý kiến cha mẹ nếu chưa thành niên).
- Trích dẫn Điều 163 Luật Nhà ở về nội dung hợp đồng nhà ở (họ tên, địa chỉ).
- Lưu ý nguyên tắc Luật Bảo vệ dữ liệu cá nhân (thu thập đúng phạm vi, mục đích) và Thông tư 116 (ưu tiên khai thác dữ liệu, không mặc định giao toàn bộ ảnh CCCD).

**Giới hạn nguồn:**

- Mục Hướng dẫn thực tế ghi rõ là 'HƯỚNG DẪN BIÊN SOẠN — không phải nguyên văn điều luật'.
- Văn bản trích dẫn bao gồm các tài liệu dự thảo/đối chiếu tương lai (như Thông tư 116/2026/TT-BCA, Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15) cần kiểm tra hiệu lực áp dụng trên thực tế.


## Câu 30: Ảnh căn cước công dân của người thuê được lưu và sử dụng như thế nào?

### Chatbot với dữ liệu mới

Dữ liệu cá nhân chỉ được thu thập và xử lý đúng phạm vi, mục đích cụ thể, rõ ràng và tuân thủ quy định pháp luật [1].

- Sự đồng ý của bạn chỉ có hiệu lực khi dựa trên tinh thần tự nguyện và bạn được biết rõ loại dữ liệu, mục đích xử lý, bên kiểm soát xử lý cùng các quyền, nghĩa vụ liên quan [2].
- Trường hợp không cần sự đồng ý bao gồm các tình huống cấp bách, phục vụ hoạt động quản lý nhà nước hoặc thực hiện thỏa thuận của bạn với bên liên quan theo quy định pháp luật [3].
- Bạn có quyền gửi yêu cầu bằng văn bản hoặc dạng điện tử kiểm chứng được để rút lại sự đồng ý hoặc yêu cầu hạn chế xử lý dữ liệu khi có nghi ngờ về mục đích hay tính chính xác [3].
- Khuyến nghị người thuê trọ đối chiếu văn bản thỏa thuận thuê để làm rõ mục đích lưu trữ ảnh căn cước công dân [2] [3].

Nguồn trích dẫn có hiệu lực thi hành từ ngày 01 tháng 01 năm 2026 [4].
Nguồn chưa có căn cứ riêng biệt quy định cụ thể về việc bên cho thuê trọ lưu trữ và sử dụng ảnh căn cước công dân [1] [2].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng.

Để áp dụng vào trường hợp của bạn:
- Bên cho thuê trọ yêu cầu giữ ảnh căn cước công dân nhằm mục đích gì?
- Hai bên đã có thỏa thuận bằng văn bản về việc thu thập và bảo mật thông tin chưa?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

### Đáp án bạn gửi

Căn cứ theo **Nghị định 13/2023/NĐ-CP**:
- Ảnh/bản sao CCCD chỉ được phép sử dụng **cho mục đích hợp pháp đã được thông báo trước** (lưu hồ sơ thuê trọ và nộp cho Công an phường để đăng ký tạm trú).
- Bên lưu trữ (chủ trọ) có trách nhiệm áp dụng các biện pháp bảo mật, không được làm rò rỉ hoặc chuyển giao cho bên thứ ba khi chưa có sự đồng ý của chủ thể dữ liệu.
*Mẹo cho sinh viên:* Khi gửi ảnh CCCD, hãy chèn dòng chữ chìm (watermark) đè lên ảnh: *"Chỉ sử dụng để đăng ký tạm trú tại phòng trọ X - ngày..."*.

### Nhận xét đối chiếu

**Ý khớp:**

- Dữ liệu/ảnh CCCD chỉ được thu thập, xử lý cho mục đích cụ thể, rõ ràng, hợp pháp và cần có sự đồng ý của chủ thể dữ liệu (trừ một số trường hợp luật định).

**Thiếu so với đáp án:**

- Căn cứ áp dụng là Nghị định 13/2023/NĐ-CP.
- Ví dụ/mục đích cụ thể: dùng để lưu hồ sơ thuê trọ và nộp Công an phường đăng ký tạm trú.
- Trách nhiệm bảo mật của bên lưu trữ (chủ trọ): không làm rò rỉ, không chuyển giao cho bên thứ ba khi chưa có sự đồng ý.
- Mẹo thực tế cho sinh viên: chèn chữ chìm (watermark) ghi rõ mục đích giới hạn trên ảnh CCCD.

**Nội dung khác:**

- Cơ sở viện dẫn: USER_REFERENCE viện dẫn Nghị định 13/2023/NĐ-CP đang áp dụng, trong khi ANSWER viện dẫn các quy định của Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 (có hiệu lực từ ngày 01/01/2026).

**Nội dung thêm:**

- Các trường hợp không cần sự đồng ý của chủ thể dữ liệu (tình huống cấp bách, phục vụ quản lý nhà nước, thực hiện thỏa thuận).
- Quyền của người thuê yêu cầu rút lại sự đồng ý hoặc hạn chế xử lý dữ liệu bằng văn bản/điện tử kiểm chứng được khi nghi ngờ mục đích, tính chính xác.
- Lưu ý về hiệu lực của Luật Bảo vệ dữ liệu cá nhân từ 01/01/2026 và việc nguồn chưa có quy định riêng biệt chi tiết cho tình huống thuê trọ.

**Giới hạn nguồn:**

- Các trích dẫn đều thuộc Luật Bảo vệ dữ liệu cá nhân số 91/2025/QH15, có hiệu lực từ 01/01/2026, chưa có hiệu lực tại thời điểm trước mốc này.
- Nội dung trong SOURCES quy định nguyên tắc chung về dữ liệu cá nhân, không có điều khoản quy định cụ thể riêng cho việc bên cho thuê trọ lưu trữ ảnh CCCD hay thủ tục tạm trú.


## Câu 31: Chủ trọ có được đăng công khai ảnh giấy tờ hoặc số điện thoại của tôi không?

### Chatbot với dữ liệu mới

Các đoạn trả lời trực tiếp trong nguồn:

- Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 — Điều 16. Công khai dữ liệu cá nhân: “1. Dữ liệu cá nhân chỉ được công khai với mục đích cụ thể. Phạm vi công khai, 
loại dữ liệu cá nhân được công khai phải phù hợp với mục đích công khai. Việc 
công khai dữ liệu cá nhân không được xâm phạm đến quyền, lợi ích hợp pháp của 
chủ thể dữ liệu cá nhân.

2. Dữ liệu cá nhân chỉ được công khai trong các trường hợp sau đây:  
a) Khi có sự đồng ý của chủ thể dữ liệu cá nhân;  
b) Thực hiện theo quy định của pháp luật;  
c) Trường hợp quy định tại điểm b khoản 1 Điều 19 của Luật này;  
d) Thực hiện nghĩa vụ theo hợp đồng.

3. Dữ liệu cá nhân công khai phải bảo đảm phản ánh đúng dữ liệu cá nhân từ 
nguồn dữ liệu gốc và tạo thuận lợi cho cơ quan, tổ chức, cá nhân trong việc tiếp 
cận, khai thác, sử dụng.

4. Hình thức công khai dữ liệu cá nhân, bao gồm: đăng tải dữ liệu trên trang 
thông tin điện tử, cổng thông tin điện tử, phương tiện thông tin đại chúng và các 
hình thức khác theo quy định của pháp luật.

5. Cơ quan, tổ chức, cá nhân công khai dữ liệu cá nhân phải kiểm soát và giám 
sát chặt chẽ việc công khai dữ liệu cá nhân để bảo đảm tuân thủ đúng mục đích, 
phạm vi và quy định của pháp luật; ngăn chặn việc truy cập, sử dụng, tiết lộ, sao 
chép, sửa đổi, xóa, hủy hoặc các hành vi xử lý trái phép khác đối với dữ liệu cá 
nhân đã công khai trong khả năng, điều kiện của mình.

Điều 19. Xử lý dữ liệu cá nhân trong trường hợp không cần sự đồng ý của | Khoản 1
chủ thể dữ liệu cá nhân

1. Các trường hợp xử lý dữ liệu cá nhân không cần sự đồng ý của chủ thể dữ 
liệu cá nhân bao gồm: 
a) Để bảo vệ tính mạng, sức khỏe, danh dự, nhân phẩm, quyền, lợi ích hợp 
pháp của chủ thể dữ liệu cá nhân hoặc người khác trong trường hợp cấp bách; bảo

vệ quyền hoặc lợi ích chính đáng của mình, của người khác hoặc lợi ích của Nhà 
nước, của cơ quan tổ chức một cách cần thiết trước hành vi xâm phạm lợi ích nói 
trên. Bên kiểm soát dữ liệu cá nhân, bên xử lý dữ liệu cá nhân, bên kiểm soát và xử 
lý dữ liệu cá nhân, bên thứ ba có trách nhiệm chứng minh trường hợp này; 
b) Để giải quyết tình trạng khẩn cấp; nguy cơ đe dọa an ninh quốc gia nhưng 
chưa đến mức ban bố tình trạng khẩn cấp; phòng, chống bạo loạn, khủng bố, 
phòng, chống tội phạm và vi phạm pháp luật;  
c) Phục vụ hoạt động của cơ quan nhà nước, hoạt động quản lý nhà nước theo 
quy định của pháp luật; 
d) Thực hiện thỏa thuận của chủ thể dữ liệu cá nhân với cơ quan, tổ chức, cá 
nhân có liên quan theo quy định của pháp luật; 
đ) Trường hợp khác theo quy định của pháp luật.” [1].

- Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 — Điều 9. Sự đồng ý của chủ thể dữ liệu cá nhân | Khoản 2: “2. Sự đồng ý của chủ thể dữ liệu cá nhân chỉ có hiệu lực khi dựa trên sự tự 
nguyện và biết rõ các thông tin sau đây: 
a) Loại dữ liệu cá nhân được xử lý, mục đích xử lý dữ liệu cá nhân; 
b) Bên kiểm soát dữ liệu cá nhân hoặc bên kiểm soát và xử lý dữ liệu cá nhân; 
c) Các quyền, nghĩa vụ của chủ thể dữ liệu cá nhân.” [3].

- Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 — Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp: “Điều 38. Hiệu lực thi hành | Khoản 1
1. Luật này có hiệu lực thi hành từ ngày 01 tháng 01 năm 2026.

Điều 38. Hiệu lực thi hành | Khoản 2
2. Doanh nghiệp nhỏ, doanh nghiệp khởi nghiệp được quyền lựa chọn thực 
hiện hoặc không thực hiện quy định tại Điều 21, Điều 22 và khoản 2 Điều 33 của 
Luật này trong thời gian 05 năm kể từ ngày Luật này có hiệu lực thi hành, trừ

doanh nghiệp nhỏ, doanh nghiệp khởi nghiệp kinh doanh dịch vụ xử lý dữ liệu cá 
nhân, trực tiếp xử lý dữ liệu cá nhân nhạy cảm hoặc xử lý dữ liệu cá nhân của số 
lượng lớn chủ thể dữ liệu cá nhân.

Điều 38. Hiệu lực thi hành | Khoản 3
3. Hộ kinh doanh, doanh nghiệp siêu nhỏ không phải thực hiện quy định tại 
Điều 21, Điều 22 và khoản 2 Điều 33 của Luật này, trừ hộ kinh doanh, doanh nghiệp 
siêu nhỏ kinh doanh dịch vụ xử lý dữ liệu cá nhân, trực tiếp xử lý dữ liệu cá nhân 
nhạy cảm hoặc xử lý dữ liệu cá nhân của số lượng lớn chủ thể dữ liệu cá nhân.

Điều 38. Hiệu lực thi hành | Khoản 4
4. Chính phủ quy định chi tiết khoản 2 và khoản 3 Điều này.

Điều 39. Quy định chuyển tiếp | Khoản 1
1. Hoạt động xử lý dữ liệu cá nhân đang thực hiện mà đã được chủ thể dữ liệu 
cá nhân đồng ý hoặc theo thỏa thuận theo quy định của Nghị định số 13/2023/NĐ-CP 
ngày 17 tháng 4 năm 2023 của Chính phủ trước ngày Luật này có hiệu lực thi hành 
thì tiếp tục thực hiện, không phải xin đồng ý lại hoặc thỏa thuận lại.

Điều 39. Quy định chuyển tiếp | Khoản 2
2. Hồ sơ đánh giá tác động xử lý dữ liệu cá nhân, hồ sơ đánh giá tác động 
chuyển dữ liệu cá nhân ra nước ngoài theo quy định của Nghị định số 13/2023/ 
NĐ-CP ngày 17 tháng 4 năm 2023 của Chính phủ đã được cơ quan chuyên trách 
bảo vệ dữ liệu cá nhân tiếp nhận trước ngày Luật này có hiệu lực thi hành thì tiếp 
tục được sử dụng và không phải lập hồ sơ đánh giá tác động xử lý dữ liệu cá nhân, 
hồ sơ đánh giá tác động chuyển dữ liệu cá nhân xuyên biên giới theo quy định của 
Luật này; việc cập nhật các hồ sơ đã lập nêu trên sau ngày Luật này có hiệu lực thi 
hành thì thực hiện theo quy định của Luật này./. 
 
 
Luật này được Quốc hội nước Cộng hòa xã hội chủ nghĩa Việt Nam khóa XV, 
kỳ họp thứ 9 thông qua ngày 26 tháng 6 năm 2025.” [4].

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng, hiệu lực và bản gốc.

### Đáp án bạn gửi

**Hoàn toàn không được phép và là hành vi vi phạm pháp luật.**
- Đăng công khai hình ảnh cá nhân, số CCCD hoặc số điện thoại lên mạng xã hội (kể cả với lý do đòi nợ tiền phòng hoặc bóc phốt) là hành vi **xâm phạm quyền về đời sống riêng tư, bí mật cá nhân** theo Điều 38 BLDS 2015 và vi phạm Nghị định 13/2023/NĐ-CP.
- Người có hành vi này có thể bị xử phạt hành chính từ **10.000.000 đến 20.000.000 đồng** theo Điều 102 Nghị định 15/2020/NĐ-CP và phải bồi thường thiệt hại danh dự, nhân phẩm cho nạn nhân.

### Nhận xét đối chiếu

**Thiếu so với đáp án:**

- Khẳng định rõ ràng: chủ trọ hoàn toàn không được phép đăng công khai và đó là hành vi vi phạm pháp luật (kể cả với mục đích đòi nợ hay bóc phốt).
- Hành vi đăng công khai CCCD, số điện thoại là xâm phạm quyền về đời sống riêng tư, bí mật cá nhân theo Điều 38 BLDS 2015 và vi phạm Nghị định 13/2023/NĐ-CP.
- Khung xử phạt vi phạm hành chính từ 10.000.000 đến 20.000.000 đồng theo Điều 102 Nghị định 15/2020/NĐ-CP.
- Trách nhiệm bồi thường thiệt hại về danh dự, nhân phẩm cho nạn nhân.

**Nội dung khác:**

- Về cách tiếp cận và căn cứ pháp lý: USER_REFERENCE trả lời trực tiếp là không được phép dựa trên BLDS 2015, Nghị định 13/2023/NĐ-CP và Nghị định 15/2020/NĐ-CP; trong khi ANSWER chỉ sao chép nguyên văn các điều luật trích từ Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 mà không đưa ra câu trả lời trực tiếp hay kết luận áp dụng vào tình huống chủ trọ.

**Nội dung thêm:**

- Các trường hợp được công khai dữ liệu cá nhân (khi có sự đồng ý, theo quy định pháp luật, thực hiện hợp đồng...) theo Điều 16 Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15.
- Các trường hợp xử lý dữ liệu không cần sự đồng ý (Điều 19) và điều kiện để sự đồng ý có hiệu lực (Điều 9 Luật 91/2025/QH15).
- Thời điểm có hiệu lực thi hành của Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 (từ ngày 01/01/2026).

**Giới hạn nguồn:**

- ANSWER chủ yếu chép lại văn bản quy phạm pháp luật (Luật 91/2025/QH15) từ trích đoạn SOURCES mà không có phần phân tích, kết luận trực tiếp giải quyết câu hỏi.
- Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 có hiệu lực từ ngày 01/01/2026, cần lưu ý hiệu lực áp dụng so với các văn bản hiện hành như Nghị định 13/2023/NĐ-CP.


## Câu 32: Nếu thông tin cá nhân của tôi bị chia sẻ sai mục đích, tôi nên yêu cầu xử lý như thế nào?

### Chatbot với dữ liệu mới

Bạn có quyền yêu cầu rút lại sự đồng ý hoặc hạn chế xử lý dữ liệu khi có nghi ngờ mục đích xử lý bị vi phạm nguyên tắc chỉ thu thập và xử lý đúng phạm vi đã định [2] [3].

- Lập văn bản yêu cầu rút lại sự đồng ý hoặc hạn chế xử lý dữ liệu ở dạng văn bản giấy hoặc dạng điện tử có định dạng kiểm chứng được [2].
- Gửi yêu cầu theo đúng quy trình và biểu mẫu tới bên kiểm soát hoặc bên kiểm soát và xử lý dữ liệu cá nhân liên quan [1] [2].
- Theo dõi phản hồi thông tin về thủ tục từ bên tiếp nhận trong thời hạn 02 ngày làm việc kể từ khi họ nhận được yêu cầu hợp lệ [1].
- Chờ bên tiếp nhận thực hiện ngừng xử lý trong 15 ngày, hoặc 20 ngày nếu cần yêu cầu bên thứ ba hay bên xử lý ngừng xử lý dữ liệu [1].

Việc rút lại sự đồng ý hoặc hạn chế xử lý không áp dụng đối với các hoạt động xử lý dữ liệu đã diễn ra trước thời điểm bạn đưa ra yêu cầu [2].
Quyền này không áp dụng cho các trường hợp xử lý dữ liệu không cần sự đồng ý theo luật định như tình trạng khẩn cấp hoặc bảo vệ tính mạng cấp bách [2].
Thời gian giải quyết ngừng xử lý có thể bị gia hạn tối đa 01 lần không quá 15 ngày tùy mức độ phức tạp và bên xử lý phải thông báo lý do [1].

Để áp dụng vào trường hợp của bạn:
- Việc chia sẻ thông tin này rơi vào trường hợp khẩn cấp hay phục vụ cơ quan nhà nước không?
- Bên thu thập thông tin của bạn là cá nhân hay tổ chức có quy trình tiếp nhận cụ thể?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

### Đáp án bạn gửi

1. Gửi yêu cầu bằng văn bản/tin nhắn cho chủ trọ buộc gỡ bỏ ngay lập tức thông tin đã đăng tải.
2. Lập vi bằng hoặc chụp ảnh màn hình lưu giữ bằng chứng vi phạm.
3. Làm đơn tố cáo gửi đến Thanh tra Sở Thông tin và Truyền thông hoặc cơ quan Công an có thẩm quyền để can thiệp xử lý theo Nghị định 15/2020/NĐ-CP.

### Nhận xét đối chiếu

**Ý khớp:**

- Đều đề cập đến việc lập văn bản/yêu cầu gửi đến bên đang nắm giữ/xử lý thông tin nhằm ngăn chặn hoặc ngừng việc xử lý thông tin vi phạm.

**Thiếu so với đáp án:**

- Yêu cầu bằng văn bản/tin nhắn cụ thể cho chủ trọ buộc gỡ bỏ ngay lập tức thông tin đã đăng tải.
- Lập vi bằng hoặc chụp ảnh màn hình lưu giữ bằng chứng vi phạm.
- Làm đơn tố cáo gửi đến Thanh tra Sở Thông tin và Truyền thông hoặc cơ quan Công an có thẩm quyền theo Nghị định 15/2020/NĐ-CP.

**Nội dung khác:**

- Chủ thể tiếp nhận và hướng xử lý: USER_REFERENCE hướng dẫn giải quyết theo tình huống thực tế (gửi chủ trọ, lập vi bằng, tố cáo cơ quan Công an/Thanh tra Sở TTTT), trong khi ANSWER hướng dẫn thủ tục hành chính chung theo quy định bảo vệ dữ liệu cá nhân gửi Bên kiểm soát/Bên kiểm soát và xử lý dữ liệu.
- Cơ sở pháp lý: USER_REFERENCE áp dụng Nghị định 15/2020/NĐ-CP, trong khi ANSWER viện dẫn các quy định của Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 và Nghị định 356/2025/NĐ-CP.

**Nội dung thêm:**

- Thời hạn bên kiểm soát dữ liệu phải phản hồi thông tin thủ tục (02 ngày làm việc) và thực hiện ngừng xử lý (15 ngày hoặc 20 ngày nếu liên quan đến bên thứ ba).
- Quy định về việc gia hạn thời gian giải quyết tối đa 01 lần không quá 15 ngày.
- Lưu ý các trường hợp ngoại lệ không áp dụng quyền rút lại sự đồng ý hoặc hạn chế xử lý (như tình trạng khẩn cấp, bảo vệ tính mạng cấp bách, hoạt động xử lý trước thời điểm yêu cầu).

**Giới hạn nguồn:**

- Các nguồn cung cấp gồm Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 và Nghị định 356/2025/NĐ-CP đều có hiệu lực từ ngày 01/01/2026, cần lưu ý thời điểm áp dụng trên thực tế.


## Câu 33: Người đăng yêu cầu đặt cọc trước nhưng không cho xem phòng: tôi nên kiểm tra những dấu hiệu rủi ro nào?

### Chatbot với dữ liệu mới

Bạn cần cảnh giác nếu gặp tình trạng giục chuyển cọc mà không cho xem phòng, mức giá bất thường, thông tin địa chỉ hoặc người nhận tiền có mâu thuẫn, hoặc người đăng không chứng minh được quyền cho thuê phòng [1].

- Khuyến nghị người thuê trực tiếp đến xem phòng trọ và xác minh rõ danh tính chủ nhà hoặc người cho thuê trước khi thực hiện giao dịch [2].
- Tuyệt đối không chuyển tiền đặt cọc khi chỉ trao đổi qua mạng xã hội hoặc điện thoại mà chưa gặp mặt và chưa kiểm chứng thông tin [2].
- Khuyến nghị hoãn việc chuyển tiền nếu chưa xác minh được thông tin, đồng thời đề nghị có lịch xem phòng cụ thể cùng tài liệu phù hợp [1].
- Đảm bảo các điều khoản đặt cọc phải thể hiện rõ ràng mục đích giao kết và phương án xử lý tiền cọc [1].
- Khuyến nghị không chuyển thêm tiền để đòi lại khoản tiền cọc đã gửi trước đó nếu phát sinh dấu hiệu bất thường [1].

Các dấu hiệu nghi vấn nêu trên chỉ hỗ trợ đánh giá rủi ro thực tế, chưa đủ căn cứ để kết luận có tội lừa đảo chiếm đoạt tài sản theo Điều 174 Bộ luật Hình sự [1].

Để áp dụng vào trường hợp của bạn:
- Người đăng tin đưa ra lý do cụ thể nào để từ chối việc bạn đến xem phòng trực tiếp?
- Bạn đã nhận được hình ảnh giấy tờ tùy thân hoặc tài liệu chứng minh quyền cho thuê phòng của người này chưa?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

### Đáp án bạn gửi

Đây là **thủ đoạn lừa đảo chiếm đoạt tiền cọc kinh điển** nhắm vào tân sinh viên. Các dấu hiệu điển hình:
1. Viện cớ: "Chủ nhà đang ở xa / đi công tác / có nhiều người đang xếp hàng đòi cọc, muốn xem phòng thì phải cọc trước 200k - 500k để giữ chân".
2. Địa chỉ trọ mập mờ, hình ảnh phòng lung linh nhưng không trùng khớp với vị trí thực tế tại Cần Thơ.
3. Chỉ giao tiếp qua Zalo/Facebook ảo, từ chối gặp mặt trực tiếp hoặc gọi video xem phòng thực tế.
**Lời khuyên dứt khoát:** Không xem được phòng thực tế tận mắt $\rightarrow$ **Tuyệt đối không chuyển dù chỉ 1 đồng.**

### Nhận xét đối chiếu

**Ý khớp:**

- Cảnh báo rủi ro khi bị yêu cầu/giục chuyển tiền cọc mà không được xem phòng trực tiếp.
- Khuyến nghị tuyệt đối không chuyển tiền cọc khi chỉ trao đổi qua mạng/điện thoại mà chưa gặp mặt, chưa xem phòng tận mắt và chưa kiểm chứng thông tin.
- Cần xác minh thông tin địa chỉ và danh tính người cho thuê/chủ nhà trước khi giao dịch.

**Thiếu so với đáp án:**

- Các viện cớ cụ thể thường gặp: chủ nhà ở xa, đi công tác, nhiều người xếp hàng đòi cọc nên phải cọc trước 200k - 500k để giữ chân.
- Bối cảnh cụ thể: nhắm vào tân sinh viên, địa chỉ thực tế tại Cần Thơ, hình ảnh phòng lung linh mâu thuẫn vị trí thực tế, từ chối gọi video xem phòng.

**Nội dung khác:**

- Về đánh giá bản chất hành vi: USER_REFERENCE khẳng định đây là 'thủ đoạn lừa đảo chiếm đoạt tiền cọc kinh điển', trong khi ANSWER lưu ý các dấu hiệu này chỉ hỗ trợ đánh giá rủi ro thực tế, chưa đủ căn cứ kết luận phạm tội lừa đảo theo Điều 174 BLHS (chưa xác minh bên nào đúng theo chuẩn pháp lý tuyệt đối).

**Nội dung thêm:**

- Khuyến nghị điều khoản đặt cọc phải rõ mục đích và phương án xử lý tiền cọc.
- Khuyên hoãn chuyển tiền, đề nghị lịch hẹn cụ thể và tài liệu phù hợp; tuyệt đối không chuyển thêm tiền để đòi lại khoản cọc cũ.
- Lưu ý về quy định Điều 174 Bộ luật Hình sự và việc chứng minh quyền cho thuê phòng.

**Giới hạn nguồn:**

- Đoạn trích từ nguồn document_id 14 ghi rõ là 'HƯỚNG DẪN BIÊN SOẠN — không phải nguyên văn điều luật'.
- Đoạn trích từ nguồn document_id 24 ghi rõ là 'KHUYẾN CÁO PHÒNG NGỪA LỪA ĐẢO — KHÔNG PHẢI ĐIỀU LUẬT'.


## Câu 34: Tôi đã chuyển cọc cho một tin trọ có dấu hiệu giả mạo; nên lưu lại bằng chứng gì và trình báo ở đâu?

### Chatbot với dữ liệu mới

Khi phát hiện chuyển cọc cho tin trọ có dấu hiệu giả mạo, bạn cần lưu trữ đầy đủ tài liệu giao dịch, tin nhắn, chứng từ và trình báo đến cơ quan Công an để được tiếp nhận, xử lý kịp thời [1] [3].

- Thu thập và sao lưu các tin đăng, đường dẫn URL, tài khoản, nội dung liên lạc, cam kết về phòng trọ và diễn biến sau khi chuyển tiền [1] [3].
- Lưu lại toàn bộ chứng từ chuyển tiền, thông tin tài khoản thụ hưởng, thời điểm thực hiện và số tiền đã giao dịch [1] [3].
- Liên hệ ngay với ngân hàng qua kênh chính thức khi phát hiện giao dịch có dấu hiệu bị chiếm đoạt để tìm phương án xử lý theo thực tế [3].
- Đến cơ quan Công an gần nhất hoặc cơ quan có thẩm quyền theo quy định để nộp đơn trình báo, tố giác tội phạm và nhận hướng dẫn xử lý [1] [2] [3].
- Phối hợp với cơ quan có thẩm quyền lập biên bản tiếp nhận hoặc ghi chép vào sổ tiếp nhận tin báo, tố giác theo quy định tố tụng [2].

Khả năng can thiệp hay xử lý từ phía ngân hàng phụ thuộc vào tình hình thực tế của giao dịch [3].
Thẩm quyền và trình tự lập biên bản tiếp nhận nguồn tin về tội phạm thực hiện theo quy định tố tụng hình sự của cơ quan chức năng [2].

Để áp dụng vào trường hợp của bạn:
- Bạn đã chuyển tiền cọc qua tài khoản ngân hàng nào và vào thời gian nào?
- Bạn hiện có lưu giữ được thông tin liên lạc, tài khoản hoặc đường dẫn bài đăng của người nhận cọc không?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

### Đáp án bạn gửi

**1. Thu thập và lưu lại toàn bộ chứng cứ:**
- Biên lai chuyển khoản ngân hàng (lưu rõ số tài khoản, tên chủ tài khoản, mã giao dịch, thời gian).
- Toàn bộ ảnh chụp màn hình tin nhắn thỏa thuận (từ lúc bắt đầu đến khi bị chặn/xóa).
- Số điện thoại, đường link trang cá nhân Facebook/Zalo của đối tượng, hình ảnh bài đăng phòng trọ.

**2. Nơi trình báo:**
- Nộp đơn tố giác tội phạm tại **Công an phường/xã nơi bạn thực hiện giao dịch chuyển tiền**, hoặc **Đội Cảnh sát hình sự / Đội An ninh mạng (PA05) Công an TP. Cần Thơ**.
- Liên hệ ngay với tổng đài ngân hàng của bạn thông báo tài khoản bị lừa đảo để đề nghị hỗ trợ đánh dấu giao dịch gian lận.

### Nhận xét đối chiếu

**Ý khớp:**

- Lưu trữ chứng từ chuyển tiền/biên lai giao dịch ngân hàng (thời điểm, số tiền, tài khoản nhận).
- Lưu giữ tin nhắn trao đổi, thỏa thuận và bài đăng/đường link tin trọ.
- Liên hệ ngay với ngân hàng để thông báo và tìm phương án xử lý giao dịch nghi bị chiếm đoạt/lừa đảo.
- Trình báo, nộp đơn tố giác tội phạm tới cơ quan Công an để được tiếp nhận và xử lý.

**Thiếu so với đáp án:**

- Gợi ý địa điểm trình báo cụ thể theo địa phương: Công an phường/xã nơi thực hiện giao dịch chuyển tiền, hoặc Đội Cảnh sát hình sự / Đội An ninh mạng (PA05) Công an TP. Cần Thơ.

**Nội dung thêm:**

- Phối hợp với cơ quan có thẩm quyền lập biên bản tiếp nhận hoặc ghi chép vào sổ tiếp nhận tin báo, tố giác tội phạm theo quy định tố tụng hình sự.
- Lưu ý khả năng can thiệp của ngân hàng phụ thuộc vào thực tế giao dịch.

**Giới hạn nguồn:**

- Context 1 và Context 3 mang tính khuyến cáo phòng ngừa và hướng dẫn biên soạn nghiệp vụ, không phải là điều luật chuẩn.
- Điều 146 Bộ luật Tố tụng hình sự (Context 2) chỉ quy định về thủ tục tiếp nhận, lập biên bản và ghi sổ tiếp nhận tố giác, không trực tiếp quy định chi tiết danh mục chứng cứ cụ thể về thuê trọ lừa đảo.


## Câu 35: Khi nào tranh chấp tiền cọc có thể có dấu hiệu lừa đảo, và khi nào chỉ là tranh chấp hợp đồng?

### Chatbot với dữ liệu mới

Tranh chấp tiền cọc là dân sự khi chỉ phát sinh bất đồng về hoàn cọc, khấu trừ, công nợ hoặc điều kiện chấm dứt hợp đồng, còn dấu hiệu lừa đảo xuất hiện khi có hành vi giả mạo, gian dối nhằm nhận tiền rồi chiếm đoạt [3].

- Khuyến nghị lập bảng đối chiếu lời hứa trước khi nhận tiền, thực trạng phòng hoặc quyền cho thuê và diễn biến sau khi nhận tiền [3].
- Rà soát lại thỏa thuận đặt cọc xem cọc bảo đảm giao kết hay thực hiện hợp đồng cùng các quy định về hoàn trả, khấu trừ và chứng từ nhận tiền [1].
- Thu thập đầy đủ chứng từ chuyển tiền và tài liệu liên quan để nộp cơ quan có thẩm quyền xem xét theo quy định [3].

Hành vi không trả tiền hoặc cắt liên lạc riêng lẻ chưa tự đủ để định tội hình sự [3].
Trường hợp nhận tài sản hợp pháp rồi mới thực hiện hành vi chiếm đoạt có thể phải xem xét theo quy định của Điều 175 với đầy đủ điều kiện cấu thành [3].
Đặt cọc chỉ là biện pháp bảo đảm theo Bộ luật Dân sự chứ không phải điều kiện bắt buộc của mọi hợp đồng thuê [1].

Để áp dụng vào trường hợp của bạn:
- Bên nhận đặt cọc có thông tin gian dối hoặc giả mạo quyền cho thuê phòng trước khi nhận tiền không?
- Bạn đã có hợp đồng thuê, biên nhận cọc hoặc chứng từ nhận tiền cụ thể nào chưa?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

### Đáp án bạn gửi

- **Trường hợp là Tranh chấp dân sự (Hợp đồng):** 
  - Phòng trọ có thật, hai bên có giao kết hợp đồng, người cho thuê đúng là chủ sở hữu hoặc người có thẩm quyền. 
  - Tranh chấp phát sinh do bất đồng ý kiến về điều kiện trừ cọc, hư hỏng tài sản hay thời gian báo trước dọn đi. Vụ việc thuộc thẩm quyền giải quyết của **Tòa án nhân dân cấp quận/huyện**.
- **Trường hợp có dấu hiệu Tội phạm hình sự (Lừa đảo - Điều 174 BLHS):** 
  - Đối tượng đưa ra thông tin gian dối ngay từ đầu: Dùng phòng ảo, nhà của người khác đóng giả làm chủ trọ để nhận cọc, hứa hẹn cho thuê nhưng thực tế không có quyền cho thuê, sau khi nhận được tiền thì lập tức chặn liên lạc, bỏ trốn để chiếm đoạt tài sản. Vụ việc thuộc thẩm quyền xử lý của **Cơ quan Cảnh sát điều tra (Công an)**.

### Nhận xét đối chiếu

**Ý khớp:**

- Tranh chấp hợp đồng dân sự xảy ra khi có bất đồng ý kiến về việc hoàn tiền cọc, khấu trừ chi phí hoặc các điều kiện kết thúc hợp đồng.
- Dấu hiệu lừa đảo phát sinh khi có hành vi gian dối, giả mạo quyền cho thuê/thông tin để nhận tiền rồi chiếm đoạt tài sản.

**Thiếu so với đáp án:**

- Cơ quan có thẩm quyền giải quyết cụ thể cho từng trường hợp: Tòa án nhân dân cấp quận/huyện cho tranh chấp dân sự, và Cơ quan Cảnh sát điều tra (Công an) cho vụ việc có dấu hiệu lừa đảo.
- Ví dụ cụ thể về tranh chấp dân sự (phòng trọ có thật, đúng chủ sở hữu/người có thẩm quyền) và lừa đảo hình sự (dùng phòng ảo, giả danh chủ trọ, ngay sau khi nhận tiền lập tức chặn liên lạc/bỏ trốn).

**Nội dung thêm:**

- Lưu ý hành vi không trả tiền hoặc cắt liên lạc riêng lẻ chưa tự đủ để định tội hình sự.
- Nêu trường hợp nhận tài sản hợp pháp rồi mới chiếm đoạt có thể xem xét theo Điều 175 BLHS (Lạm dụng tín nhiệm chiếm đoạt tài sản).
- Khuyến nghị lập bảng đối chiếu lời hứa trước khi nhận tiền với thực trạng phòng/quyền cho thuê, rà soát thỏa thuận đặt cọc và thu thập chứng từ thanh toán.

**Giới hạn nguồn:**

- Đoạn trích [1] và [3] thuộc dạng 'HƯỚNG DẪN BIÊN SOẠN — không phải nguyên văn điều luật', là tài liệu biên soạn diễn giải thực tế, không phải văn bản quy phạm pháp luật trực tiếp.
- Nghị quyết 81/2025/UBTVQH15 được dẫn trong nguồn [3] về TAND khu vực là thông tin tổ chức tòa án, chưa nêu cụ thể trong nội dung trích dẫn thẩm quyền chi tiết.


## Câu 36: Nếu có nhiều sinh viên cùng bị một người nhận cọc rồi cắt liên lạc, chúng tôi nên cung cấp thông tin gì cho cơ quan có thẩm quyền?

### Chatbot với dữ liệu mới

Khi phát hiện dấu hiệu nghi vấn hoặc bị lừa đảo, người thuê cần nhanh chóng lưu giữ các tài liệu, tin nhắn, chứng từ chuyển tiền và trình báo cơ quan Công an để được hỗ trợ giải quyết [1].

- Nhanh chóng thu thập và lưu giữ toàn bộ tin nhắn liên lạc với đối tượng nhận tiền cọc [1].
- Tập hợp các tài liệu và chứng từ chuyển tiền đặt cọc đã thực hiện giao dịch [1].
- Trình báo thông tin và nộp các tài liệu đã lưu giữ cho cơ quan Công an để được xử lý kịp thời [1].
- Cơ quan điều tra, Viện kiểm sát hoặc cơ quan có thẩm quyền sẽ lập biên bản tiếp nhận và ghi vào sổ tiếp nhận khi tiếp nhận trực tiếp tố giác [2] [3].

Khuyến nghị của cơ quan Công an mang tính phòng ngừa và hướng dẫn xử lý khi bị lừa đảo, không phải điều luật cụ thể quy định danh mục hồ sơ tố tụng bắt buộc [1].
Thủ tục lập biên bản và ghi sổ tiếp nhận áp dụng theo thẩm quyền tiếp nhận tố giác, tin báo về tội phạm của các cơ quan theo quy định [2] [3].

Để áp dụng vào trường hợp của bạn:
- Các bạn đã tổng hợp đầy đủ biên lai chuyển tiền và lịch sử tin nhắn của từng người chưa?
- Các bạn dự định nộp đơn tố giác trực tiếp hay gửi qua đường bưu chính?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

### Đáp án bạn gửi

Khi có nhiều nạn nhân, hành vi có tính chất chuyên nghiệp, mức độ nguy hiểm cao và giá trị thiệt hại cộng dồn sẽ cấu thành khung hình phạt nặng hơn theo Điều 174 Bộ luật Hình sự:
1. **Lập Đơn tố giác tội phạm tập thể (đồng đứng tên các nạn nhân):** Liệt kê danh sách từng người, số tiền bị chiếm đoạt, phương thức liên lạc.
2. **Tài liệu chứng minh kèm theo:** Bảng sao kê giao dịch ngân hàng của tất cả nạn nhân chuyển vào cùng số tài khoản thụ hưởng của kẻ lừa đảo; các cuộc hội thoại thể hiện cùng một kịch bản gian dối.
3. **Nơi tiếp nhận:** Nộp đơn đến **Cơ quan Cảnh sát điều tra Công an quận/huyện** nơi đối tượng cư trú hoặc nơi người thuê nhà thực hiện chuyển khoản. Cơ quan điều tra sẽ thụ lý và khởi tố vụ án theo thẩm quyền.

### Nhận xét đối chiếu

**Ý khớp:**

- Cần lưu giữ và cung cấp chứng từ/biên lai chuyển tiền đặt cọc.
- Cần lưu giữ và cung cấp các tin nhắn, nội dung trao đổi liên lạc với đối tượng.
- Trình báo/nộp tài liệu đến cơ quan Công an có thẩm quyền.

**Thiếu so với đáp án:**

- Lập đơn tố giác tội phạm tập thể (đồng đứng tên các nạn nhân), liệt kê danh sách từng người, số tiền bị chiếm đoạt và phương thức liên lạc.
- Đề cập quy định về cấu thành định khung/tình tiết tăng nặng theo Điều 174 Bộ luật Hình sự khi có nhiều nạn nhân, tính chất chuyên nghiệp.
- Chỉ định cụ thể nơi tiếp nhận là Cơ quan Cảnh sát điều tra Công an quận/huyện nơi đối tượng cư trú hoặc nơi người thuê nhà thực hiện chuyển khoản.

**Nội dung thêm:**

- Cơ quan điều tra, Viện kiểm sát hoặc cơ quan có thẩm quyền sẽ lập biên bản tiếp nhận và ghi vào sổ tiếp nhận khi tiếp nhận trực tiếp tố giác (có thể gửi qua bưu chính).
- Lưu ý khuyến nghị của cơ quan Công an mang tính phòng ngừa, hướng dẫn xử lý chứ không phải điều luật cụ thể quy định danh mục hồ sơ tố tụng bắt buộc.

**Giới hạn nguồn:**

- Tài liệu khuyến cáo của Bộ Công an là nội dung tuyên truyền/phòng ngừa, không phải điều khoản quy phạm pháp luật cụ thể.
- Trích dẫn từ Văn bản hợp nhất 17-VBHN-VPQH quy định thủ tục tiếp nhận tố giác chung của cơ quan có thẩm quyền (Điều 145, 146), không quy định chi tiết danh mục tài liệu riêng cho việc tố giác lừa đảo cọc trọ nhiều người.

