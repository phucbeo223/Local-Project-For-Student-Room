# Rà soát Data cho chatbot hỗ trợ sinh viên thuê trọ

## Cập nhật ngày 23/09/2026: bản trích VBHN 17 đã phù hợp hơn

Đã đọc lại `Data/criminal_law/Văn-bản-hợp-nhất-17-VBHN-VPQH.docx` sau khi người dùng rút ngắn. Phần thân hiện có 13.565 ký tự, gồm 11 điều: 30, 56, 62, 86, 87, 88, 99, 144, 145, 146, 147; metadata Word ghi 5 trang (chưa kiểm chứng phân trang bằng render). **Thay đề xuất bỏ toàn file trước đây bằng giữ bản trích trong nhánh báo tin/tố giác nghi lừa đảo thuê trọ.** Đánh giá cũ về toàn văn khoảng 580.681 ký tự phía dưới chỉ còn là lịch sử.

- Nên giữ Điều 56, 86–87, 99, 144–147: quyền người báo tin, chứng cứ/dữ liệu điện tử, tiếp nhận và giải quyết nguồn tin. Giữ cả điều kiện/gia hạn tại Điều 147, không chỉ lấy thời hạn ở khoản 1.
- Điều 88 có ích ở phần giao nộp/tiếp nhận tài liệu; khoản 5 về chuyển hồ sơ nội bộ có thể không đưa vào embedding mặc định.
- Điều 30 và phần quyền tố tụng sâu của Điều 62 là tùy chọn; không bắt buộc cắt nếu muốn giữ nguyên điều. Năm trang này đã đủ gọn, không cần giảm trang bằng mọi giá.
- Thân bản trích chưa ghi số hiệu/ngày hợp nhất và nguồn; nên bổ sung định danh **17/VBHN-VPQH ngày 12/02/2026**, nhãn “trích tuyển” và [liên kết Công báo gốc](https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-17-vbhn-vpqh-468961.htm). Ngày hợp nhất không phải ngày hiệu lực chung cho mọi điều.
- Còn các ký hiệu chú thích [74]–[78] trong nội dung nhưng không có phần giải thích chú thích trong DOCX. Cần tra bản gốc và lưu thông tin sửa đổi/hiệu lực liên quan trước khi làm sạch ký hiệu; không xóa cơ học làm mất dấu phiên bản.
- Chỉ truy xuất bản này khi câu hỏi thuộc nhánh nghi lừa đảo/tố giác/chứng cứ; không dùng nó để mặc định biến tranh chấp hoàn cọc thành vụ án hình sự. Chưa sửa tài liệu nguồn hoặc index lại database.

---

Ngày rà soát: 22/09/2026. Phạm vi: đề xuất tuyển chọn dữ liệu, không sửa hoặc xóa tài liệu nguồn, không thay đổi database.

Kiểm tra cuối: file `Văn-bản-hợp-nhất-17-VBHN-VPQH.docx` đã được chuyển từ gốc Data vào `Data/criminal_law/` trong lúc rà soát; xuất hiện thêm file khóa Word `~$n-bản-hợp-nhất-17-VBHN-VPQH.docx`. Báo cáo đánh giá 37 tài liệu thật, không tính file khóa. Các thao tác di chuyển/mở Word này không do quy trình rà soát thực hiện.

## Kết luận

Nên thu hẹp kho RAG theo tình huống của người thuê: hợp đồng và đặt cọc; điện, nước; đăng ký tạm trú; PCCC ở mức người thuê cần biết; căn cước và quyền riêng tư. Pháp luật hình sự, tố tụng, hồ sơ xây dựng và nghĩa vụ của đơn vị vận hành nền tảng nên là kho tham khảo riêng, chỉ truy xuất khi có tình huống tương ứng.

Không đánh đồng “bỏ khỏi kho RAG chính” với “xóa file gốc”. Nên lưu bản gốc bên ngoài đường dẫn được index và tạo bản trích tuyển có ánh xạ về điều/khoản/trang gốc.

SRS của dự án, mục 1.2 và FR-6, tập trung hệ thống tìm trọ và chatbot có trích nguồn. Việc bổ sung pháp luật cần phục vụ các tình huống thuê trọ, không mở rộng thành chatbot tư vấn pháp luật tổng quát. Đây là đề xuất phạm vi NCKH, không phải kết luận rằng tài liệu ngoài phạm vi không có giá trị pháp lý.

## Các vấn đề xác nhận trực tiếp

- Có **37 file: 20 PDF, 11 DOCX, 6 DOC**. Tổng số trang PDF: **1.029**. Không cộng DOC/DOCX vào số trang vì chưa phân trang bằng trình soạn thảo.
- Hai file `fire_safety/nghi dinh so 347 2026.pdf` và `residence/nghi dinh so 347 nam 2026 bo sung.pdf` trùng SHA-256, tức trùng toàn bộ byte. Nên có một nguồn chuẩn với nhiều nhãn chủ đề.
- `residence/nghi dinh so 154 nam 2020.pdf` đặt sai năm: trang đầu là **154/2024/NĐ-CP**, ngày 26/11/2024. Đã kiểm tra ảnh gốc và [nguồn Chính phủ](https://vanban.chinhphu.vn/?classid=0&docid=211821&pageid=27160).
- `water_cantho/thong tu so 124 2025.pdf` đặt sai số: ảnh trang đầu là **145/2025/TT-BTC**, ngày 31/12/2025, về phương pháp định giá nước sạch. Đã đối chiếu với [nguồn Chính phủ](https://vanban.chinhphu.vn/?classid=1&docid=216468&pageid=27160&typegroupid=6). Code lấy tên file làm tiêu đề nguồn, nên lỗi này ảnh hưởng trực tiếp trích dẫn.
- `housing_contract/Luật-19-2023-QH15.doc` là **Luật Bảo vệ quyền lợi người tiêu dùng**, không phải Luật Nhà ở. Bản hiện có đã trích một số điều, chủ yếu quyền người tiêu dùng và bảo vệ thông tin.
- `Data/criminal_law/Văn-bản-hợp-nhất-17-VBHN-VPQH.docx` (ban đầu ở gốc Data) là **Bộ luật Tố tụng hình sự**, có khoảng **580.681 ký tự** trích xuất ở thời điểm bắt đầu. Đây là ứng viên loại khỏi kho chính rõ nhất.
- `housing_contract/2026_204_79_VBHN-VPQH.docx` là **Luật Nhà ở hợp nhất**, khoảng **328.129 ký tự** trích xuất. Rất cần nhưng không nên index toàn văn. Số hiệu được đối chiếu với [Công báo 79/VBHN-VPQH](https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-79-vbhn-vpqh-469209.htm).
- Các DOCX ở `construction_legality`, `criminal_law`, `privacy_data`, `real_estate_brokerage` có dấu hiệu đã tuyển điều. Tuyển theo điều là đúng hướng, nhưng một số bản thiếu phần hiệu lực/phạm vi hoặc còn nhiều điều ngoài nhu cầu thuê trọ.
- Có **815 trang thuộc các PDF hoàn toàn không có chữ trích xuất được** bằng bộ đọc PDF; một số file khác chỉ có chữ đầu trang hoặc chữ lỗi. Thông tư 60/2025 có lớp chữ lỗi, ví dụ tên cơ quan bị biến dạng. Đây là lỗi chất lượng đầu vào, không giải quyết chỉ bằng giảm kích thước chunk.
- Bảng giá điện trong Quyết định 1279, trang PDF 4, đọc rõ bằng mắt nhưng OCR thử bị hỏng cấu trúc bảng. Phải kiểm tra riêng bảng số trước khi đưa vào câu trả lời tính tiền.

## Nguyên tắc đọc danh sách tuyển chọn

“Trang” bên dưới là **thứ tự trang PDF tính từ 1 trong đúng file hiện tại**, không phải số trang Công báo. Phạm vi trang chỉ giúp tìm nội dung; không phải lệnh cắt tự động. Nếu một trang chứa cả phần cần giữ và phần thừa, chỉ đưa điều/khoản phù hợp vào bản trích. Nếu điều kéo sang trang sau, lấy đủ phần tiếp nối.

Với DOC/DOCX, dùng số điều và tên mục. Bộ trích hiện tại của dự án gom mỗi DOC/DOCX thành một `ExtractedPage(1, ...)`, nên metadata “trang 1” không phản ánh trang thực tế.

Đối với mọi bản trích cần giữ: định danh văn bản; phạm vi và đối tượng áp dụng có liên quan; điều/khoản/điểm; ngoại lệ; hiệu lực và chuyển tiếp liên quan; quy định sửa đổi tác động đến đoạn đang dùng. Không bỏ “hiệu lực” cùng với trang chữ ký chỉ vì chúng nằm cuối văn bản.

## Các file Word: quyết định theo từng file

Đường dẫn trong bảng tính từ `Data/`.

| File | Đề xuất | Phần nên giữ / lược và lý do |
|---|---|---|
| `criminal_law/Văn-bản-hợp-nhất-17-VBHN-VPQH.docx` | **Cập nhật 23/09: giữ bản trích cho nhánh nghi lừa đảo** | Người dùng đã rút còn 11 điều, 13.565 ký tự. Xem nhận xét cập nhật đầu báo cáo; đề xuất loại toàn văn ngày 22/09 không còn áp dụng cho bản rút gọn này. |
| `construction_legality/Nghị-định-217-2026-NĐ-CP.docx` | Kho tham khảo, ưu tiên bỏ khỏi bản NCKH đầu | Bản hiện có gồm Điều 7, 49–51, 55–56, 60, 63, 66–67; phần lớn phục vụ xin phép/quản lý xây dựng. Chỉ cân nhắc Điều 66 về công khai giấy phép khi chức năng kiểm tra thông tin pháp lý công trình được định nghĩa rõ. |
| `construction_legality/Nghị-định-339-2026-NĐ-CP.docx` | Kho tham khảo | Các Điều 25, 30, 33, 62, 66, 73, 85 nói nhiều đến vi phạm của chủ đầu tư/chủ sở hữu và môi giới. Không dùng làm nguồn mặc định cho câu hỏi “nhà trọ này có an toàn không”. Nếu mở nhánh môi giới, tuyển Điều 73 cùng quy tắc mức phạt ở Điều 5 và phần hiệu lực bổ sung. |
| `criminal_law/Văn-bản-hợp-nhất-135-VBHN-VPQH.docx` | Lược mạnh; kho rủi ro tùy chọn | Có thể giữ Điều 8 và các Điều 158, 174, 175, 290 cho tình huống xâm phạm chỗ ở/lừa đảo thuê trọ, kèm căn cứ áp dụng. Các Điều 134, 155–157, 170, 173, 176, 178, 288, 313–314 chỉ thêm khi có câu hỏi kiểm thử tương ứng. Không suy ra tội phạm chỉ từ việc chủ nhà chậm trả cọc. |
| `disputes/2024_1159 + 1160_11-VBHN-VPQH.doc` | Đưa toàn file ra khỏi kho chính; trích nhỏ nếu cần | Đây là phần đầu của Bộ luật Tố tụng dân sự, có nội dung chứng cứ và khởi kiện. Chỉ cần nhánh tranh chấp nâng cao mới tuyển các mục chứng cứ, quyền khởi kiện, nội dung/nộp đơn; phải đối chiếu sửa đổi mới về thẩm quyền tòa án trước khi sử dụng. |
| `disputes/2024_1161 + 1162_11-VBHN-VPQH.doc` | Đưa ra khỏi RAG chính | Nhiều thủ tục phúc thẩm, rút gọn và các việc dân sự; ít phục vụ câu hỏi thuê trọ thường gặp. Ba file tố tụng là các phần nối tiếp, không được mặc định là ba bản trùng. |
| `disputes/2024_1163 + 1164_11-VBHN-VPQH.doc` | Đưa ra khỏi RAG chính | Có phần công nhận bản án/quyết định của tòa nước ngoài, tố tụng và khiếu nại sâu; mức liên quan rất thấp. |
| `fire_safety/2023_1091 + 1092_09-2023-TT-BXD.doc` | Đưa ra khỏi RAG chính | Đây là sửa đổi QCVN 06:2022/BXD, có ngưỡng quy mô và yêu cầu thiết kế kỹ thuật. Không dùng độc lập thay cho cả quy chuẩn hoặc áp đồng loạt cho mọi phòng trọ. Chỉ giữ ở kho kỹ thuật khi làm chức năng đánh giá công trình. |
| `housing_contract/2026_204_79_VBHN-VPQH.docx` | Giữ làm nguồn lõi, tuyển điều | Ưu tiên Điều 1–3 (phần định nghĩa/phạm vi cần thiết), 10–11, 57 nếu có tình huống nhà nhiều tầng nhiều căn hộ, 160–164, 168, 170–173, 194; giữ chú thích sửa đổi và hiệu lực/chuyển tiếp liên quan ở 197–198. Lược phát triển dự án, nhà công vụ, tái định cư, mua bán/thuê mua, sở hữu nước ngoài, quản trị chung cư không liên quan. |
| `housing_contract/Luật-19-2023-QH15.doc` | Lược / chuyển phần lớn sang tài liệu tuân thủ nền tảng | Đã thấy các Điều 3, 4, 10, 15–19. Có thể giữ 3, 4, 10 cho quyền người sử dụng dịch vụ khi đúng đối tượng; 15–19 trùng chủ đề dữ liệu cá nhân nên ưu tiên kho tuân thủ. Bản hiện tại chưa thấy Điều 25 về điều khoản không được phép trong hợp đồng; nếu muốn hỗ trợ tình huống này cần bổ sung từ nguồn chuẩn, không coi dẫn chiếu tới Điều 25 là đã có nội dung điều đó. |
| `privacy_data/Hien-phap-2013.doc` | Đưa khỏi kho chính | Bản đã trích nhóm Điều 14–23 nhưng vẫn quá khái quát. Có thể giữ Điều 21–22 ở kho tham khảo; ưu tiên quy định cụ thể về căn cước, dữ liệu và quyền người thuê cho truy xuất thường ngày. |
| `privacy_data/Luật-26-2023-QH15.docx` | Giữ bản trích gọn | Các Điều 7, 20, 29 phù hợp câu hỏi chủ nhà giữ căn cước, dùng thông tin căn cước. Cần bổ sung metadata hiệu lực từ nguồn gốc; không mở rộng sang toàn bộ thủ tục cấp/cấp lại căn cước. |
| `privacy_data/Luật-91-2025-QH15.docx` | Tách người thuê và tuân thủ hệ thống | Kho người thuê: Điều 3–4, 7, 9–11, 15–19, 31–32 khi liên quan chia sẻ thông tin/camera/vị trí, kèm ngoại lệ. Kho vận hành NCKH: Điều 22–23, 29–30, 37 và các trách nhiệm xử lý dữ liệu. Lược 25–28 về lao động, sức khỏe, ngân hàng, quảng cáo khỏi RAG thuê trọ nếu không có tình huống tương ứng. Giữ 38–39 cho hiệu lực/chuyển tiếp. |
| `privacy_data/Nghị-định-356-2025-NĐ-CP.docx` | Lược; phần lớn làm tài liệu tuân thủ | Bản có Điều 1–7, 21, 28–29. Kho người thuê chỉ cần 1–6 và phần 7 thực sự phục vụ câu hỏi chuyển giao thông tin. Điều 21 về dịch vụ xử lý dữ liệu và 28–29 về thông báo vi phạm ưu tiên tài liệu thiết kế/vận hành. Bản trích thiếu đuôi hiệu lực; cần bổ sung. |
| `privacy_data/Nghị-định-330-2026-NĐ-CP.docx` | Kho tùy chọn, không cần bỏ vì dài | Bản đã gọn: Điều 1, 7, 13. Chỉ đưa vào nhánh xâm phạm thông tin riêng tư trên mạng; giữ Điều 7 cùng Điều 13 để không nhầm mức phạt cá nhân/tổ chức. Bổ sung hiệu lực vì bản trích thiếu. Định danh được đối chiếu ở [Chính phủ](https://vanban.chinhphu.vn/?docid=219266&pageid=27160). |
| `real_estate_brokerage/Luật-29-2023-QH15.docx` | Kho môi giới tùy chọn | Ưu tiên Điều 1–4, 8–9 để xác định phạm vi và Điều 61–65 về môi giới, thù lao, hoa hồng, quyền/nghĩa vụ. Điều 14, 16, 18–21, 44–48 chỉ bật cho tình huống kinh doanh bất động sản phù hợp; tránh cạnh tranh với Luật Nhà ở/Bộ luật Dân sự trong mọi câu hỏi thuê trọ. |
| `water_cantho/Quyết-định-215-QĐ-UBND.docx` | Giữ, kiểm tra phiên bản giá trước khi dùng | Tài liệu gọn, đúng địa bàn. Giữ Điều 1 kèm đủ nhãn nhóm khách hàng/đơn vị cấp nước/khu vực/thuế-phí, Điều 2 về điều chỉnh và Điều 3 về hiệu lực. Lược căn cứ dài và nơi nhận khỏi phần embedding. Bảng ghi giá năm 2024 và cơ chế điều chỉnh: không tự coi là giá hiện hành 2026. |

## Các PDF: quyết định theo từng file và vị trí tuyển chọn

Đã chạy OCR phục vụ rà soát trên 872 trang thiếu chữ, ít chữ hoặc lớp chữ lỗi. Các trang có lớp chữ dùng được được trích trực tiếp; đã xem ảnh gốc tại các điểm quan trọng như số hiệu, bảng giá, trang đầu phụ lục và nội dung người thuê. Đây không phải hiệu đính từng ký tự của 1.029 trang.

| File trong Data | Số trang | Đề xuất và vị trí cần xem |
|---|---:|---|
| `disputes/326_2016_UBTVQH14(16723).pdf` | 28 | **Đưa khỏi kho chính ở bản NCKH đầu.** Án phí/lệ phí chỉ cần khi hỗ trợ khởi kiện. Nếu mở nhánh này, chỉ tuyển án phí dân sự, miễn/giảm và các bảng tương ứng; không lấy án phí hình sự/hành chính/trọng tài. |
| `electricity/luat61 nam 2024 QH15.pdf` | 76 | **Lược mạnh.** Xem Điều 9 ở tr.11–12; Điều 44 ở tr.38–40; Điều 48–50 ở tr.42–45; Điều 56–57 ở tr.51–52; Điều 63 ở tr.56–57; Điều 66 ở tr.59–60; Điều 74 ở tr.68–69; hiệu lực/chuyển tiếp ở tr.73–76. Chỉ trích phần người dùng điện, bán lẻ, thanh toán và an toàn sinh hoạt. Lược quy hoạch, nhà máy điện, điện gió ngoài khơi, thị trường điện, hồ đập. |
| `electricity/nghi dinh so 133 2026.pdf` | 45 | **Giữ trích tuyển xử phạt điện.** Phạm vi/đối tượng/mức phạt ở tr.1–4; Điều 12–13 ở tr.14–17; an toàn điện sinh hoạt tại Điều 19 ở tr.27–28 nếu cần; hiệu lực/chuyển tiếp ở tr.37–39. Điều 12 phân biệt đơn vị bán lẻ, Điều 13 có tình huống sử dụng điện; phải giữ đúng chủ thể và khoản liên quan. Lược phát điện, truyền tải, thị trường điện, hồ đập và các phép tính điện trộm nếu không có tình huống đó. |
| `electricity/quyet dinh so 1279 QD BCT.pdf` | 7 | **Giữ.** Tr.1–2: thông tin quyết định, điều kiện thuế và thời điểm áp dụng; **tr.4: riêng mục 4, giá bán lẻ điện sinh hoạt**. Không index toàn bảng lẫn giá kinh doanh, sản xuất và bán buôn ở tr.3–7. Bảng OCR lỗi, cần chuyển thành dữ liệu có nhãn hàng/cột rồi đối chiếu ảnh gốc. Chỉ dùng giá cho thời kỳ đã kiểm tra. |
| `electricity/quyet dinh so 14 nam 2025.pdf` | 7 | **Giữ bản trích giải thích cơ cấu giá.** Điều 1–3 ở tr.1–2, Điều 6–7 ở tr.3–4; phần cơ cấu điện sinh hoạt trong phụ lục ở tr.7. Lược phần cơ cấu sản xuất, kinh doanh, chiếu sáng ở tr.5–6. Điều khoản chuyển tiếp rất quan trọng; không trộn cơ cấu mới với bảng giá cũ chỉ vì đều có nhãn điện sinh hoạt. |
| `electricity/thong tu so 60 2025.pdf` | 27 | **Nguồn lõi.** Giữ Điều 1–3 tại tr.1–3 ở mức cần thiết; **Điều 12 tại tr.9–12**, nhất là khoản dành cho người thuê nhà; hiệu lực/chuyển tiếp tại tr.19–21. Có thể tuyển phần trách nhiệm kiểm tra thu tiền điện ở Điều 19, tr.18–19. Lược công nghiệp, kinh doanh, bán buôn, mẫu hợp đồng của đơn vị bán lẻ tại tr.22–27 khỏi kho hỏi đáp thuê trọ. Tr.12 có cả cuối Điều 12 và đầu Điều 13: phải chọn đúng điều. Cần OCR lại lớp chữ lỗi. |
| `fire_safety/luat so 55 2024.pdf` | 43 | **Giữ trích tuyển.** Điều 2 về định nghĩa ở tr.1–3; Điều 6 ở tr.5–6; phần trách nhiệm hộ/cá nhân ở Điều 8, tr.6–9; Điều 14 ở tr.12–13; Điều 20–21 ở tr.18–20; Điều 23–25 ở tr.21–23; Điều 54–55 ở tr.41–43. Lược tổ chức lực lượng, trang phục, ngân sách và thẩm định kỹ thuật sâu. Không áp tiêu chuẩn của cơ sở kinh doanh cho mọi nhà ở khi chưa phân loại. |
| `fire_safety/nghi dinh so 105 2025.pdf` | 181 | **Cắt giảm rất mạnh.** Xem Điều 2–4, tr.4–6; phần trách nhiệm chủ cơ sở/tự kiểm tra tại Điều 12–14, tr.17–24 nếu nằm trong phạm vi hỏi đáp; Điều 45–46, tr.67–69; chỉ các dòng nhà ở/nhà ở tập thể/cơ sở lưu trú phù hợp trong Phụ lục I–II, tr.70–77. **Tr.99–181 chủ yếu là bộ biểu mẫu**, nên bỏ khỏi embedding mặc định. Tr.78–98 gồm phụ lục thiết kế, phương tiện, bảo hiểm: chỉ lấy phần nào thật sự cần cho câu hỏi đã xác định. Phải nối sửa đổi tương ứng trong NĐ 347/2026. |
| `fire_safety/nghi dinh so 106 2025.pdf` | 36 | **Kho xử phạt tùy chọn, tuyển gọn.** Điều 2–5, tr.2–5 để giữ chủ thể/mức phạt; Điều 11–12, tr.8–9; Điều 20–24, tr.14–20 nếu hỏi thiết bị, khói, thoát nạn; Điều 39–40, tr.35–36. Không cần chương phân quyền xử phạt dài ở tr.24–34 cho hỏi đáp thường ngày. Các sửa đổi Điều 18 ở NĐ 347 chỉ cần nối nếu giữ nội dung thẩm định/nghiệm thu. |
| `fire_safety/nghi dinh so 347 2026.pdf` | 20 | **Giữ một bản chuẩn, tuyển theo văn bản được sửa.** Tr.6–15: sửa NĐ 105; tr.16: sửa NĐ 106; tr.17–18: sửa NĐ 282; tr.18–19: phần chuyển tiếp/hiệu lực. Với cư trú, ưu tiên **Điều 35 tại tr.17** và phần chung liên quan; với PCCC chỉ giữ sửa đổi tác động đến điều đang dùng. Lược tr.2–5 về dịch vụ dữ liệu và tr.20 là biểu mẫu báo cáo khỏi RAG thuê trọ. Tr.1 lưu định danh. Không index nguyên tr.6–19 thành một khối chung. |
| `housing_contract/Luat Dan Su phan 1.pdf` | 94 | **Nguồn lõi, lược mạnh.** Điều 117–133 về giao dịch ở tr.33–38 khi cần điều kiện/vô hiệu; **Điều 328 về đặt cọc ở tr.86–87**; phần vi phạm nghĩa vụ/chậm trả/bồi thường tại Điều 351, 357, 360–364 ở tr.91–94. Không cắt riêng tr.86 vì khoản 2 về xử lý cọc nằm ở tr.87. Lược pháp nhân, vật quyền, địa dịch, cầm cố/thế chấp không liên quan. |
| `housing_contract/Luat Dan Su phan 2.pdf` | 78 | **Nguồn lõi, lược mạnh.** Tr.4–9: Điều 385–408, chỉ tuyển điều về giao kết, nội dung, hiệu lực, giải thích, hợp đồng mẫu phù hợp; tr.11–15: Điều 418–429 về phạt/bồi thường/chấm dứt; **tr.25–27: Điều 472–482 về thuê tài sản**; tr.77–78: hiệu lực/chuyển tiếp. Lược mua bán, vay, vận chuyển, gia công, thừa kế, quan hệ có yếu tố nước ngoài. Hai phần Dân sự nối tiếp nhau, không phải bản trùng. |
| `housing_contract/nghi dinh 54 nam 2026.pdf` | 22 | **Kho cập nhật, không index toàn văn mặc định.** Văn bản sửa nhiều nghị định; phần sửa NĐ 95 nằm khoảng tr.4–10; tr.11–19 có nhiều nội dung nhà ở xã hội; hiệu lực/chuyển tiếp tại tr.20–21. Chỉ kéo vào kho chính đoạn sửa tác động đến điều nhà ở đang giữ. Nếu mở hướng dẫn ký túc xá/nhà ở xã hội, cần bộ nguồn và tình huống riêng. Không loại văn bản sửa đổi chỉ vì trùng từ khóa với văn bản gốc. |
| `housing_contract/Nghi dinh 95 nam 2024.pdf` | 172 | **Lược rất mạnh.** Trọng tâm hiện tại là **Điều 41–42 tại tr.50–51** về nhà nhiều tầng nhiều căn hộ; lưu Điều 1–2 ở tr.1–3 để xác định phạm vi và phần hiệu lực/chuyển tiếp cần thiết tại tr.107–113. Lược thủ tục đầu tư, sở hữu nước ngoài, nhà công vụ, tái định cư, nhà thuộc tài sản công, đơn vị vận hành chung cư; phụ lục tr.114–172 không cần nạp mặc định. Đặc biệt, mẫu hợp đồng ở tr.130–134 là **nhà ở công vụ**, không dùng làm hợp đồng thuê trọ phổ thông. |
| `residence/luat so 68 nam 2020.pdf` | 23 | **Nguồn lõi, tuyển tạm trú.** Định nghĩa ở tr.1–2; quyền/nghĩa vụ ở tr.4–6; **Điều 27–30 ở tr.15–17**; có thể thêm phần tạm vắng Điều 31 ở tr.17–18; hiệu lực ở tr.22–23. Điều 27 có dẫn chiếu Điều 23: giữ các địa điểm bị loại trừ liên quan tại tr.12–13, đừng bỏ hết phần thường trú rồi mất dẫn chiếu này. Phải đối chiếu luật sửa đổi, vì bản này là bản năm 2020. |
| `residence/nghi dinh so 154 nam 2020.pdf` | 22 | **Giữ bản trích và sửa metadata thành 154/2024.** Điều 5 về chỗ ở hợp pháp, tr.4–6; Điều 7 nếu có sinh viên chưa thành niên và Điều 8 tại tr.8–10; Điều 10 về xóa tạm trú, tr.11–12 nếu cần; Điều 15–16 tại tr.16–17. Lược nơi cư trú trên tàu thuyền, cơ sở dữ liệu/quản trị nhà nước và mẫu khai thác dữ liệu không phục vụ tạm trú. |
| `residence/nghi dinh so 282 2025.pdf` | 96 | **Lược rất mạnh.** Phần chung liên quan chủ thể và mức phạt, tr.2–6; **Điều 9–11 tại tr.12–16** về yên tĩnh, cư trú, căn cước; hiệu lực/chuyển tiếp tại tr.95–96. Lược vũ khí, xuất nhập cảnh, cờ bạc, mại dâm, bạo lực gia đình và thẩm quyền chuyên sâu ngoài phạm vi. Nối Điều 35 NĐ 347/2026 với Điều 10 này để tránh trích quy định chưa cập nhật. |
| `residence/nghi dinh so 347 nam 2026 bo sung.pdf` | 20 | **Bỏ bản trùng khỏi index.** Trùng toàn bộ với file NĐ 347 trong `fire_safety`. Giữ một nguồn chuẩn gắn cả nhãn cư trú và PCCC; không xóa mất nhánh cư trú khi bỏ bản sao. |
| `residence/thong tu so 53 nam 2025.pdf` | 22 | **Giữ tuyển chọn thủ tục cư trú.** Điều 1–2 ở tr.1–4 và hiệu lực ở tr.5–6; **CT01 và hướng dẫn tại tr.7–8** chỉ đưa vào nhánh hướng dẫn điền mẫu, có thể cung cấp file mẫu qua liên kết thay vì embedding các dòng trống. Tr.9–22 là các mẫu khác: bỏ khỏi kho chính nếu không có tình huống sử dụng. Đây là thông tư sửa đổi, không tự thay thế toàn bộ nội dung TT55/2021, TT56/2021 và TT66/2023 được dẫn chiếu. |
| `water_cantho/thong tu so 124 2025.pdf` | 10 | **Sửa định danh thành 145/2025; ưu tiên kho tham khảo.** Nếu cần giải thích nguyên tắc giá nước, chỉ tuyển phạm vi/đối tượng ở tr.1–2, Điều 7 ở tr.6–8, Điều 9–10 ở tr.9–10. Lược công thức chi phí sản xuất, giá thành, lợi nhuận của đơn vị cấp nước ở tr.3–6. Không dùng phương pháp định giá này thay bảng giá bán lẻ cụ thể của Cần Thơ. |

## Thứ tự xử lý đề xuất

1. Sửa định danh hai file đặt sai tên; loại một bản NĐ 347 khỏi danh sách index; lưu ánh xạ nguồn cũ/mới.
2. Đưa Bộ luật Tố tụng hình sự, ba phần tố tụng dân sự, án phí, QCVN thiết kế và hồ sơ xây dựng khỏi kho hỏi đáp mặc định.
3. Tuyển điều của Bộ luật Dân sự, Luật Nhà ở, điện, cư trú và PCCC theo bảng; kiểm tra đầy đủ phần tiếp nối, ngoại lệ, sửa đổi và hiệu lực.
4. Tách bảng giá điện/nước thành dữ liệu có nhãn, kiểm chứng từng mức/bậc/thuế/phí. Loại header, dấu ký số, nơi nhận, dòng chấm của biểu mẫu khỏi embedding.
5. Để dữ liệu gốc bên ngoài đường dẫn index; chỉ index bản tuyển đã kiểm tra, rồi đồng bộ nguồn đang hoạt động trong database.
6. Chạy phép so sánh corpus đầy đủ và corpus tuyển chọn trước khi kết luận giảm nhiễu.

## Vì sao chỉ cắt trang chưa đủ

1. **Dò file còn lấy toàn bộ cây thư mục.** `scan_documents()` đọc cả PDF, DOC, DOCX, TXT, MD trong mọi thư mục con không ẩn. Vì vậy chuyển tài liệu vào `Data/archive/` hoặc đặt báo cáo này trong `Data/` vẫn làm chúng bị index. Đặt kho lưu trữ ngoài `Data` hoặc bổ sung danh sách file/đoạn được phép index.
2. **Lấy file ra không tự gỡ chunk cũ.** `index_folder()` xử lý file đang tồn tại; `replace_document()` thay chunk của nguồn tương ứng. Chưa thấy bước tự vô hiệu hóa nguồn đã bị loại khỏi thư mục. Khi áp dụng bộ tuyển chọn, cần đồng bộ trạng thái nguồn/chunk trong database để chúng không tiếp tục được truy xuất. Chưa thực hiện thay đổi database trong lần rà soát này.
3. **Chưa có bộ lọc thời gian pháp lý tổng quát.** Code truy xuất kiểm tra `status='ready'`; cần metadata hiệu lực, thay thế, sửa đổi và địa bàn để chọn đúng phiên bản. Ngày ban hành không đồng nghĩa ngày bắt đầu áp dụng mọi điều khoản.
4. **Chủ đề chưa được phân luồng đầy đủ.** Có bộ lọc riêng cho câu hỏi điện; phần lớn câu hỏi khác còn tìm chung. Với câu hỏi “giữ cọc”, các đoạn “tạm giữ”, “tịch thu” trong tố tụng/hình sự có thể cạnh tranh với Điều 328 và hợp đồng thuê.
5. **Chunker hiện có điểm tốt cần giữ.** Nó chia theo tiêu đề điều/khoản/điểm, mục tiêu 1.600 ký tự, overlap 220; dừng overlap khi đổi heading, giữ khoản dẫn cho điểm và bỏ một phần nơi nhận/số trang. Vấn đề ưu tiên là tuyển nội dung, hiệu lực, chất lượng OCR và bảng; chưa có căn cứ để chỉ giảm chunk size.
6. **Không cắt mất quan hệ giữa các mảnh.** Một khoản có điều kiện mở đầu và nhiều điểm phải mang theo điều kiện đó. Trích tuyển nên giữ `parent_article_id`, `article`, `clause`, `point`, `original_page_from/to`, `amends`, `valid_from/to`, `jurisdiction`, `source_url`, `is_excerpt`, `reviewed_at`.
7. **Bỏ qua file tạm Word.** Kiểm tra cuối có file tên bắt đầu `~$`. Bộ dò hiện tại chưa loại mẫu tên này, nên có thể thử đọc file khóa như DOCX và báo lỗi. Không tính file khóa vào số tài liệu nguồn hoặc đem chia chunk.

## Cách chứng minh phù hợp NCKH

Tạo bộ câu hỏi có đáp án và điều/trang chuẩn cho các nhóm hợp đồng–cọc, điện, nước, tạm trú, PCCC, căn cước–riêng tư; thêm câu hỏi ngoài phạm vi và câu hỏi phụ thuộc thời điểm. Chia bộ phát triển và bộ đánh giá độc lập trước khi điều chỉnh tuyển chọn.

So sánh A: toàn bộ corpus; B: corpus tuyển chọn, cùng mô hình embedding, cấu hình chunk, truy xuất và bộ câu hỏi. Sau đó mới thử C: B cộng lọc chủ đề/hiệu lực để tách ảnh hưởng của từng thay đổi.

Đo Recall@k của điều khoản chuẩn, độ chính xác trích dẫn, tỷ lệ chunk không liên quan trong top-k, tỷ lệ trả lời sai thời điểm, khả năng từ chối câu ngoài phạm vi, độ trễ và số chunk. Không ghi “giảm nhiễu X%” trước khi chạy phép đo này. Số trang ít hơn không tự chứng minh chất lượng tốt hơn.

## Giới hạn của nhận xét

Đây là rà soát tuyển chọn corpus dựa trên file hiện có và mã nguồn dự án. Đã đối chiếu trực tuyến một số định danh/vấn đề quan trọng, chưa kiểm tra đầy đủ lịch sử hiệu lực của mọi điều khoản trong cả 37 file. DOC cũ được nhận diện nội dung bằng các đoạn Unicode đọc được trong tệp, không phải phân trang Word đáng tin cậy; do đó chỉ đề xuất theo điều/mục và không đưa số trang giả cho DOC/DOCX. OCR thử phục vụ tìm nội dung, không phải bản văn pháp luật đã hiệu đính.
