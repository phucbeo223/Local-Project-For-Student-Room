# Sửa riêng câu 47–49 theo bộ đáp án mới — 06/10/2026

Đối chiếu với bộ `external-legal-user-2026-10-06`, giữ nguyên đáp án người dùng. Sinh câu trả lời bằng Qwen chọn nguồn + Gemini phân tích/tổng hợp/kiểm chứng; chấm đối chiếu bằng Qwen cục bộ. Không gửi đáp án mẫu hoặc dữ liệu nhà trọ lên Gemini; không hard-code câu trả lời theo ID.

| Câu | Trước sửa, chấm bằng đáp án mới | Sau sửa | Ký tự | Luồng cuối | Trả lời một phần |
|---|---|---|---:|---|---|
| 47 | Khớp một phần | Khớp cao | 2537 | gemini-agent | Không |
| 48 | Khớp một phần | Khớp một phần | 1840 | gemini-agent | Không |
| 49 | Khớp một phần | Khớp một phần | 2061 | gemini-agent | Có |

Kết quả chấm nội dung: {"high": 1, "partial": 2}. Đây là nhãn khớp nội dung, không phải tỷ lệ đúng pháp luật. Nhãn khớp cao và cờ nguồn/trả lời một phần đo hai việc khác nhau.

## Rà soát trực tiếp câu trả lời

- Câu 47: đủ nhóm tài khoản/người đăng, địa chỉ, hình ảnh, giá. Câu trả lời thực tế có địa chỉ gồm số nhà, tên đường, phường, quận; không thiếu nhóm kiểm tra địa chỉ.
- Câu 48: có thao tác báo tin, lý do, nội dung gửi, link tin, số điện thoại liên hệ của người báo, hỗ trợ chat/email công bố và hình ảnh trao đổi nếu có. Chưa coi link tin là yêu cầu mã tin, hoặc điện thoại người báo là điện thoại người đăng; nguồn xuất bản nêu khác bộ mẫu. Không tự tạo thời hạn gỡ mọi báo cáo trong 24 giờ.
- Câu 49: có công khai/định danh, lọc từ khóa/kiểm duyệt, phản ánh/gỡ tin và cung cấp dữ liệu/tạm ngừng tài khoản theo điều kiện. Có mốc xác thực 2027 và yêu cầu cơ quan có thẩm quyền cho thời hạn 24 giờ. Khác mẫu ở điều kiện pháp lý và phạm vi người bán/người cho thuê.
Các danh sách điểm thiếu/khác ở cuối báo cáo là đầu ra nguyên vẹn của Qwen để kiểm tra, có thể chứa nhận xét sai; dùng cùng câu trả lời thực tế và phần rà soát này.

Theo bộ chấm hiện tại, chưa đạt mức khớp cao cho cả ba câu. Câu 48 còn khác về ảnh chụp màn hình trong biểu mẫu, mã tin/điện thoại người đăng và cam kết xử lý 24 giờ. Câu 49 còn khác về đối tượng cho thuê và điều kiện/thời điểm xác thực. Những chi tiết chưa có căn cứ không được bổ sung như quy định chắc chắn chỉ để tăng nhãn khớp.

## Các khâu đã sửa

- Gemini phân tích: chuẩn hóa trường `missing_information` dạng chuỗi sang danh sách, cung cấp schema trong prompt và ghi rõ trường lỗi; không bỏ kiểm tra các trường khác.
- Truy xuất: phân biệt checklist người thuê với trách nhiệm nền tảng; giữ đủ nguồn tài khoản, địa chỉ, hình ảnh, giá; đọc đầy đủ khoản gốc khi xếp hạng.
- Chọn nguồn bằng Qwen: kiểm tra nhóm ý bị bỏ sót, retry có giới hạn; giữ các nhóm lọc từ khóa/gỡ tin, định danh, phản ánh, cung cấp dữ liệu; không để điều hiệu lực chiếm chỗ nội dung chính.
- Gemini tổng hợp: thao tác báo tin, kênh hỗ trợ, hình ảnh/bằng chứng; nêu các nhóm nghĩa vụ, điều kiện loại nền tảng và ngày áp dụng trong từng câu.
- Kiểm chứng: giữ đúng sự kiện bắt đầu thời hạn 24 giờ; chặn xác thực điện tử được trình bày như nghĩa vụ hiện tại khi chưa đến mốc áp dụng; cảnh báo cuối bài không sửa được câu khẳng định sai. Kiểm tra nhóm trách nhiệm bị Gemini bỏ sót và yêu cầu sửa có giới hạn.
- Giữ câu trả lời và dự phòng dưới 3.500 ký tự; không cắt giữa điều kiện/ngoại lệ pháp luật. Chặn email không có nguyên văn trong nguồn. 108 kiểm thử hồi quy đã đạt; kiểm tra tích hợp truy xuất xác nhận đã lấy được trích đoạn hình ảnh và điều khoản thi hành.

## Khác biệt cần giữ so với đáp án mẫu

Câu 48: không cam kết mọi phản ánh của người dùng đều được gỡ trong 24 giờ. Điều 17 khoản 1 điểm c Nghị định 248/2026/NĐ-CP trong nguồn gắn mốc này với yêu cầu của cơ quan nhà nước có thẩm quyền. Các thao tác và kênh hỗ trợ được ghi rõ là hướng dẫn Chợ Tốt/Nhà Tốt, không áp dụng nguyên xi cho mọi nền tảng.

Câu 49: nghĩa vụ cung cấp dữ liệu 24 giờ của Điều 18 khoản 2 cần giữ điều kiện nền tảng trung gian có chức năng đặt hàng và yêu cầu cơ quan có thẩm quyền. Xác thực điện tử phải giữ mốc 01/01/2027 trong nguồn hiệu lực; không diễn đạt đã bắt buộc ở ngày chạy. Chưa coi các quy định về người bán tự động áp dụng giống nhau cho mọi người cho thuê hoặc trang đăng tin.

[Nghị định trên Công báo Chính phủ](https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-248-2026-nd-cp-469983.htm). Đáp án người dùng chưa được xác minh toàn bộ; các điểm này được ghi nhận riêng, không sửa bộ mẫu để tăng điểm.

## Dữ liệu và nguồn

Mã xử lý cuối đã được cập nhật lên FastAPI cục bộ: `/health` và `/docs` trả HTTP 200; hash 9 mô-đun khớp workspace. Phiếu triển khai: `docs/FOCUS3_API_DEPLOYMENT_20261006.json`. Các kết quả ba câu trong báo cáo này thuộc kho thử, chưa phải kết quả chạy trên kho đang phục vụ API.

Kho thử riêng `legal_word_focus3_v11_20261006`: 32 tài liệu Word, 425 vector E5/384 chiều; graph `graph_rag_word_focus3_v11`, nhà trọ `housing_graph_word_focus3_v11`. 31 mục nguồn của v10 giữ nguyên byte; v10 kế thừa nguyên 30 mục của kho bổ sung v8. Không OCR, không PDF, không embedding đáp án mẫu.

Nguồn bổ sung là trích nguyên văn ngắn được đối chiếu với HTML nhà xuất bản, chuyển thành Word và kiểm tra lại nội dung/hash:

- [Google Search Help: tìm ảnh bằng Google Lens](https://support.google.com/websearch/answer/1325808?co=GENIE.Platform%3DDesktop&hl=vi): 19 từ nguyên văn để hỗ trợ tìm nguồn hình ảnh; kết quả ảnh không tự chứng minh gian lận.
- [Trợ Giúp Nhà Tốt: phản ánh tin/người bán, hình ảnh trao đổi](https://trogiup.chotot.com/nguoi-mua/bi-quyet-mua-bat-dong-san-an-toan-voi-nha-tot/): 21 từ nguyên văn về hình ảnh trao đổi thể hiện vi phạm; giữ cảnh báo bối cảnh mua bất động sản.

Kiểm tra hash toàn dòng xác nhận kho đang dùng `legal_word_v7_20261005`, graph `graph_rag_word_v6`, nhà trọ `housing_graph_word_v6`, dữ liệu public và người dùng giữ nguyên. Bản thử Datahouse có cùng 789 dòng/vector. Kho thử v11 còn staging; chưa đổi kho đang phục vụ API. Không chạy lại toàn bộ 36/56 câu trong lượt sửa này.

Hash bộ đáp án: `876e38dba5c2faeba797d02503680b82c1eb7d6bd30b148737cf47db84e36983`.
Hash manifest nguồn: `b7f10153a074cc89f2dc46978186dcee70e71bce44fc171b733385ddd1f95cd7`.
Hash mã pipeline của lượt chạy: `004b52ada216e98ed42ffbc8b8d21fa973235ae0e4b7b26c6238796d9d00f2cf`.

Bằng chứng chi tiết: `eval/reports/graph_rag_focus3_pilot_v14_2026-10-06.json`, `graph_rag_focus3_reference_v14_2026-10-06.json`, `graph_rag_focus3_audit_v11_2026-10-06.json`, `gemini_focus3_analysis_diagnostics_2026-10-06.json`.

## Câu trả lời thực tế và đối chiếu từng câu

### Câu 47: Khi tìm phòng qua một nền tảng trực tuyến, tôi nên kiểm tra người đăng và nguồn tin như thế nào?

Khuyến nghị người thuê trọ chủ động rà soát tài khoản đăng tin, đối chiếu địa chỉ và liên hệ, kiểm tra nguồn gốc hình ảnh cùng mức giá trước khi giao dịch [1] [2] [3] [4].

- Về tài khoản và người đăng: kiểm tra việc xác thực số điện thoại trên nền tảng, tìm kiếm số điện thoại trên Google, Facebook hoặc diễn đàn để xem đánh giá giao dịch trước đó và cảnh giác tài khoản ảo tạo tương tác giả [1] [3] [4].
- Về nội dung, địa chỉ và liên hệ: xác minh cụ thể số nhà, tên đường, phường, quận, hỏi thăm trực tiếp xung quanh hoặc người thân, đồng thời cảnh giác thông tin sao chép từ nơi khác [3] [4].
- Về hình ảnh: sử dụng công cụ Google Lens để tìm kiếm ảnh hoặc trang web chứa hình ảnh tương tự nhằm phát hiện tình trạng sao chép ảnh quảng bá [2] [3].
- Về mức giá: khảo sát mức giá chung khu vực bằng cách so sánh tin đăng cùng loại và hết sức thận trọng với các tin rao phòng tốt ở vị trí trung tâm nhưng giá thấp bất thường [1] [3] [4].

Các bước kiểm tra dựa trên hướng dẫn và mẹo giao dịch của nền tảng cùng khuyến cáo của cơ quan công an, không phải quy định pháp luật bắt buộc [1] [3] [4].
Kết quả tìm kiếm hình ảnh tương tự hay xác thực số điện thoại của nền tảng chỉ mang tính đối chiếu, không tự chứng minh quyền sở hữu hoặc quyền cho thuê phòng [1] [2].

Hướng dẫn/khuyến cáo của Trợ Giúp Chợ Tốt Nhà Tốt; không phải điều luật. Xác thực số điện thoại không xác minh quyền sở hữu hay quyền cho thuê. Chính sách riêng không bảo đảm mọi tin đều đúng và không xác lập nghĩa vụ giống nhau cho mọi nền tảng.
Hướng dẫn công cụ Google Lens, không phải điều luật. Kết quả ảnh tương tự là đầu mối để đối chiếu, không tự chứng minh tin đăng giả hoặc danh tính người cho thuê.
Hướng dẫn/khuyến cáo của Cổng Thông tin điện tử Bộ Công an bài Công an tỉnh Tuyên Quang; không phải điều luật. Tình huống gốc là đặt khách sạn tại Tuyên Quang. Áp dụng tham khảo cho chứng cứ giao dịch trực tuyến, không gọi là vụ thuê trọ CTU; không phải danh mục hồ sơ bắt buộc hoặc hướng dẫn soạn đơn tập thể.
Hướng dẫn/khuyến cáo của Trợ Giúp Chợ Tốt; không phải điều luật. Mẹo giao dịch, không phải điều luật. Không chứng minh hạn hoàn cọc cố định hoặc mức cọc bắt buộc; không thay thế xác minh người được ủy quyền cho thuê. Chỉ đọc phần kiểm tra, không bổ sung mẫu soạn hợp đồng.

Để áp dụng vào trường hợp của bạn:
- Bạn đã có số điện thoại hoặc hình ảnh phòng đăng tải để đối chiếu chưa?
- Tin đăng bạn đang xem thuộc nền tảng nào và có hiển thị dấu hiệu xác thực tài khoản không?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

Đối chiếu cục bộ: Khớp cao. ANSWER đáp ứng đầy đủ 4 bước chính của USER_REFERENCE: kiểm tra tài khoản, xác minh nội dung/địa chỉ, tìm kiếm hình ảnh và cảnh giác giá rẻ. ANSWER bổ sung thêm các chi tiết hữu ích như kiểm tra đánh giá trên mạng xã hội và làm rõ tính chất khuyến cáo thay vì luật bắt buộc. Khác biệt chủ yếu nằm ở phạm vi địa lý (Cần Thơ/Ninh Kiều so với tổng quát) và độ cụ thể của tình huống.

Điểm thiếu theo mô hình chấm (cần đọc cùng đáp án thực tế):

- Không yêu cầu kiểm tra 'thâm niên hoạt động' của tài khoản người đăng.
- Không nhắc đến việc tìm kiếm đánh giá trên các diễn đàn bên ngoài nền tảng.

Khác biệt theo mô hình chấm:

- USER_REFERENCE giới hạn địa chỉ cụ thể tại Cần Thơ và Ninh Kiều, trong khi ANSWER mang tính tổng quát cho mọi khu vực.
- USER_REFERENCE tập trung vào tình huống cụ thể (phòng đầy đủ nội thất), ANSWER mở rộng sang cảnh giác chung về tin đăng lừa đảo.

Nguồn đã truy xuất:

- [1] Nhà Tốt bảo vệ người dùng như thế nào — Trợ Giúp Chợ Tốt Nhà Tốt — Nhà Tốt bảo vệ người dùng như thế nào | Đoạn nguyên văn 75 — [bản gốc](https://trogiup.chotot.com/nguoi-mua/nha-tot-bao-ve-nguoi-dung-nhu-the-nao/)
- [2] Google Lens: kiểm tra nguồn hình ảnh — Google Search Help — Google Lens — tìm ảnh và trang chứa ảnh tương tự — [bản gốc](https://support.google.com/websearch/answer/1325808?co=GENIE.Platform%3DDesktop&hl=vi)
- [3] Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 — Cổng Thông tin điện tử Bộ Công an bài Công an tỉnh Tuyên Quang — Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 | Đoạn nguyên văn 12 — [bản gốc](https://bocongan.gov.vn/bai-viet/canh-giac-thu-doan-lua-dao-mao-danh-fanpage-khach-san-nha-hang-dat-coc-truc-tuyen-dip-le-hoi-thanh-tuyen-2026-1790041513)
- [4] Mẹo khi thuê phòng — Trợ Giúp Chợ Tốt — Mẹo khi thuê phòng | Đoạn nguyên văn 78 — [bản gốc](https://trogiup.chotot.com/nguoi-mua/meo-khi-thue-phong/)

### Câu 48: Nếu một tin đăng nhà trọ có thông tin sai, tôi có thể báo cáo cho nền tảng bằng cách nào?

Theo hướng dẫn của Chợ Tốt, bạn có thể báo cáo tin đăng sai sự thật trực tiếp trên bài đăng hoặc liên hệ qua kênh hỗ trợ của nền tảng [1].

- Trên website Chợ Tốt, chọn mục Báo cáo tin đăng bên dưới nội dung tin, chọn lý do như Thông tin không đúng thực tế hoặc Lừa đảo, điền thông tin được yêu cầu rồi nhấn Gửi [1].
- Bạn có thể liên hệ Chợ Tốt qua trò chuyện trực tuyến trong khung giờ hỗ trợ hoặc gửi email hỗ trợ công bố trên nền tảng gồm đường link tin đăng, lý do không hợp lệ và số điện thoại liên hệ [1].
- Theo Nhà Tốt, bạn có thể cung cấp thêm thông tin hoặc hình ảnh trao đổi mua bán với người bán thể hiện hành vi vi phạm nếu có [2].
- Chợ Tốt tiếp nhận phản ánh và có quyền xử lý theo cơ chế giải quyết tranh chấp nếu xác định người bán có hành vi vi phạm [4].

Các bước báo cáo được trích dẫn theo quy trình của Chợ Tốt và Nhà Tốt, không phải quy định chung bắt buộc cho mọi nền tảng thuê trọ [1] [4].

Hướng dẫn/khuyến cáo của Trợ Giúp Chợ Tốt; không phải điều luật. Đây là thao tác trên Chợ Tốt; vị trí nút có thể thay đổi. Báo cáo nền tảng không thay thế việc báo cơ quan có thẩm quyền khi có dấu hiệu chiếm đoạt.
Hướng dẫn của Nhà Tốt về hình ảnh trao đổi giúp làm rõ phản ánh tin/người bán vi phạm; không phải điều luật hoặc thời hạn xử lý. Trang nguồn có bối cảnh mua bất động sản; chỉ dùng phần phản ánh tin, không suy sang thủ tục mua bán hoặc quyền trong hợp đồng thuê.
Hướng dẫn/khuyến cáo của Trợ Giúp Chợ Tốt; không phải điều luật. Quy trình riêng của Chợ Tốt. Không phải cam kết nền tảng tự hoàn tiền cọc hoặc giải quyết mọi tranh chấp thuê nhà; một phần quy trình trên trang nói về hàng hóa khuyến mại, cần giữ đúng phạm vi.

Để áp dụng vào trường hợp của bạn:
- Bạn đang xem tin đăng sai sự thật trên Chợ Tốt hay một nền tảng nào khác?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

Đối chiếu cục bộ: Khớp một phần. ANSWER bao phủ được hai cách chính (báo cáo trực tiếp và liên hệ hỗ trợ) nhưng thiếu cam kết về thời gian xử lý (24h) và yêu cầu bằng chứng hình ảnh cụ thể có trong USER_REFERENCE. ANSWER bổ sung thêm cảnh báo pháp lý về việc không thay thế cơ quan chức năng và làm rõ phạm vi áp dụng chỉ cho từng nền tảng.

Điểm thiếu theo mô hình chấm (cần đọc cùng đáp án thực tế):

- Cam kết về thời gian xử lý tối đa là 24 giờ.
- Yêu cầu đính kèm ảnh chụp màn hình làm bằng chứng trong bước báo cáo trực tiếp.

Khác biệt theo mô hình chấm:

- USER_REFERENCE đề cập nghĩa vụ pháp lý của sàn (gỡ bỏ trong 24h), ANSWER chỉ nói về quyền xử lý theo cơ chế nội bộ.
- ANSWER mở rộng phạm vi sang nền tảng khác và nhấn mạnh đây là quy trình riêng, không phải luật bắt buộc chung.

Nguồn đã truy xuất:

- [1] Làm thế nào để báo cáo tin đăng — Trợ Giúp Chợ Tốt — Làm thế nào để báo cáo tin đăng | Đoạn nguyên văn 93 — [bản gốc](https://trogiup.chotot.com/nguoi-mua/lam-the-nao-de-bao-cao-tin-dang/)
- [2] Nhà Tốt: hình ảnh trao đổi hỗ trợ phản ánh tin vi phạm — Hình ảnh trao đổi khi phản ánh tin đăng/người bán vi phạm — [bản gốc](https://trogiup.chotot.com/nguoi-mua/bi-quyet-mua-bat-dong-san-an-toan-voi-nha-tot/)
- [3] Nghị định 248/2026/NĐ-CP hướng dẫn Luật Thương mại điện tử — Chính phủ Công báo Chính phủ — Điều 17. Trách nhiệm của chủ quản nền tảng thương mại điện tử | Khoản 1 — [bản gốc](https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-248-2026-nd-cp-469983.htm)
- [4] Cơ chế giải quyết tranh chấp của Chợ Tốt — Trợ Giúp Chợ Tốt — Cơ chế giải quyết tranh chấp của Chợ Tốt | Đoạn nguyên văn 75 — [bản gốc](https://trogiup.chotot.com/nguoi-mua/co-che-giai-quyet-tranh-chap-cua-cho-tot/)
- [5] Nghị định 248/2026/NĐ-CP hướng dẫn Luật Thương mại điện tử — Chính phủ Công báo Chính phủ — Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp — [bản gốc](https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-248-2026-nd-cp-469983.htm)

### Câu 49: Nền tảng đăng tin có trách nhiệm gì đối với thông tin người bán hoặc người cho thuê theo tài liệu hiện có?

Nền tảng thương mại điện tử có trách nhiệm công khai thông tin người bán, kiểm duyệt và lưu trữ dữ liệu tin đăng, tiếp nhận phản ánh, đồng thời thực hiện xác thực điện tử người bán từ ngày 01/01/2027 [1] [2] [4].

- Nền tảng trung gian phải công khai tên và địa chỉ cư trú của cá nhân hoặc tên, địa điểm kinh doanh, trụ sở của tổ chức theo nội dung đăng ký bằng tiếng Việt hoặc ký tự La-tinh [2].
- Chủ quản nền tảng có trách nhiệm xác thực điện tử danh tính người bán kể từ ngày 01/01/2027 với cá nhân trong nước gồm họ tên, ngày sinh, số định danh cá nhân và tổ chức gồm tên, trụ sở, số định danh tổ chức cùng thông tin người đại diện [2] [4].
- Nền tảng phải kiểm duyệt nội dung tin đăng trước khi hiển thị, lọc từ khóa, gỡ bỏ thông tin vi phạm trong vòng 24 giờ khi cơ quan nhà nước có thẩm quyền yêu cầu và bảo đảm truy cập dữ liệu đã đăng tải ít nhất 01 năm [1] [2].
- Nếu có chức năng đặt hàng trực tuyến, nền tảng phải cung cấp thông tin cho cơ quan nhà nước có thẩm quyền và tạm ngừng hoặc chấm dứt tài khoản người bán trong thời hạn 24 giờ kể từ khi nhận được yêu cầu [3].

Quy định xác thực điện tử danh tính người bán áp dụng kể từ ngày 01/01/2027 nên chưa bắt buộc áp dụng tại ngày 06/10/2026 [4].
Tài liệu trích dẫn quy định về trách nhiệm đối với người bán trên nền tảng thương mại điện tử nói chung, chưa có quy định riêng biệt trực tiếp cho người cho thuê phòng trọ [1] [2].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng.
Cần đối chiếu điều/khoản được dẫn chiếu còn thiếu; đoạn trích chưa đủ để kết luận toàn bộ điều kiện và ngoại lệ.
Văn bản TMĐT có hiệu lực 01/07/2026; phải đọc đúng loại nền tảng và điều khoản chuyển tiếp. Điều 52 khoản 2: quy định xác thực điện tử áp dụng từ 01/01/2027, chưa áp dụng ở ngày 05/10/2026.

Để áp dụng vào trường hợp của bạn:
- Nền tảng bạn đang sử dụng là website đăng tin đơn thuần hay có chức năng đặt phòng trực tuyến?
- Người đăng tin cho thuê trên nền tảng là cá nhân hay tổ chức kinh doanh?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

Đối chiếu cục bộ: Khớp một phần. ANSWER chỉ đạt 'partial' vì tuy bao phủ đúng các nghĩa vụ cốt lõi (định danh, kiểm duyệt, cung cấp dữ liệu) nhưng lại bổ sung nhiều chi tiết kỹ thuật (lưu trữ 1 năm, xác thực điện tử cụ thể) và nhấn mạnh tính chưa bắt buộc của quy định mới tại thời điểm đánh giá. USER_REFERENCE tập trung vào quy trình đăng tin và xử lý vi phạm cơ bản mà không đi sâu vào các điều kiện áp dụng theo thời gian hay phân loại nền tảng như ANSWER.

Điểm thiếu theo mô hình chấm (cần đọc cùng đáp án thực tế):

- USER_REFERENCE yêu cầu xác thực danh tính trước khi đăng; ANSWER chỉ nêu quy định áp dụng từ 01/01/2027 và ghi nhận chưa bắt buộc tại thời điểm đánh giá (06/10/2026).
- USER_REFERENCE đề cập cụ thể đến việc cung cấp thông tin cho cơ quan Công An phục vụ điều tra; ANSWER dùng khái quát 'cơ quan nhà nước có thẩm quyền'.

Khác biệt theo mô hình chấm:

- ANSWER nêu rõ trách nhiệm lưu trữ dữ liệu tối thiểu 01 năm và xác thực điện tử chi tiết (số định danh, trụ sở...); USER_REFERENCE không đề cập các điểm này.
- ANSWER phân biệt loại nền tảng (đăng tin đơn thuần vs đặt hàng trực tuyến) ảnh hưởng đến nghĩa vụ; USER_REFERENCE áp dụng chung cho 'người cho thuê'.

Nguồn đã truy xuất:

- [1] Nghị định 248/2026/NĐ-CP hướng dẫn Luật Thương mại điện tử — Chính phủ Công báo Chính phủ — Điều 17. Trách nhiệm của chủ quản nền tảng thương mại điện tử | Khoản 1 — [bản gốc](https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-248-2026-nd-cp-469983.htm)
- [2] Nghị định 248/2026/NĐ-CP hướng dẫn Luật Thương mại điện tử — Chính phủ Công báo Chính phủ — Điều 18. Trách nhiệm của chủ quản nền tảng thương mại điện tử trung gian | Khoản 1 — [bản gốc](https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-248-2026-nd-cp-469983.htm)
- [3] Nghị định 248/2026/NĐ-CP hướng dẫn Luật Thương mại điện tử — Chính phủ Công báo Chính phủ — Điều 18. Trách nhiệm của chủ quản nền tảng thương mại điện tử trung gian | Khoản 2 — [bản gốc](https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-248-2026-nd-cp-469983.htm)
- [4] Nghị định 248/2026/NĐ-CP hướng dẫn Luật Thương mại điện tử — Chính phủ Công báo Chính phủ — Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp — [bản gốc](https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-248-2026-nd-cp-469983.htm)

