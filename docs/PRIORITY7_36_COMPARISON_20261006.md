# Sửa 7 câu ưu tiên và chạy lại cùng 36 câu — 06/10/2026

Bản trước sửa đã được push lên nhánh `codex/legal-priority7-20261006` tại GitHub cá nhân, commit `ab0470c`. Lượt này tiếp tục trên cùng nhánh.

Cả hai bản được đối chiếu với nguyên bộ đáp án người dùng ngày 06/10/2026 bằng cùng Qwen cục bộ và cùng rubric có kiểm tra trích đoạn. Không gửi đáp án mẫu hoặc nhà trọ lên Gemini; không embedding đáp án, không hard-code câu trả lời theo ID.

## Kết quả

- Sinh được câu trả lời: **36/36**, lỗi thực thi: **0**.
- Theo cờ bao phủ nguồn: trước **17 đầy đủ / 19 một phần**; sau **20 đầy đủ / 16 một phần**.
- Khớp nội dung với mẫu trước sửa: `{'high': 9, 'partial': 21, 'unscored': 4, 'low': 2}`.
- Khớp nội dung với mẫu sau sửa: `{'partial': 14, 'high': 15, 'unscored': 3, 'low': 4}`.
- Các câu chưa qua kiểm tra bộ chấm: `[23, 27, 31]`; không gán điểm thay thế.
- Các câu có nhãn low: `[34, 36, 45, 50]`.
- Nhãn tăng ở các câu đã chấm được cả hai bản: `[21, 24, 28, 29, 37, 43, 47, 49, 57]`; nhãn giảm: `[36, 50, 58]`.
- Trước chưa chấm được, sau chấm được: `[34, 45]`; chiều ngược lại: `[27]`.
- Kiểm tra trích đoạn bộ chấm: trước **32/36**, sau **33/36**.
- Luồng trả lời cuối: `{'gemini-agent': 33, 'qwen-local': 3}`; câu trả các đoạn nguồn đã chọn: `[27, 30, 31]`.
- Câu dài nhất: trước **11136**, sau **3137 ký tự**.

Các nhãn high/partial/low đo mức khớp văn bản, không phải tỷ lệ đúng pháp luật. “Một phần” là thiếu nguồn/điều kiện, không phải lỗi chạy. Trích dẫn có đúng định dạng cũng không chứng minh mọi kết luận đúng. Mẫu chưa được chứng nhận toàn bộ; các điểm cần kiểm tra ghi riêng trong `REFERENCE_REVIEW_36_20261006.md`.

Câu 27, 30, 31 đều đã gọi Gemini trong workflow. Đầu ra cuối quay về các đoạn Word do Qwen chọn vì kiểm tra quy tắc nguồn còn chặn bản tổng hợp sau lần sửa; provider cuối không mô tả toàn bộ agent đã tham gia. Lý do được giữ bên dưới từng câu.

Nhãn tổng hợp lấy từ các ý CHÍNH đã qua audit: high nếu tất cả là matched; partial nếu có cả matched và missing/different; low nếu chưa có ý matched; unscored nếu chưa qua audit. Không dùng trực tiếp nhãn agreement của Qwen, vì có trường hợp cả sáu ý different nhưng mô hình gán high. Nhãn gốc và trích đoạn được giữ nguyên để rà; chưa thẩm định độc lập toàn bộ đánh giá ngữ nghĩa từng ý.

- Nhãn Qwen gốc trước: `{'high': 29, 'partial': 3, 'unscored': 4}`; sau: `{'partial': 4, 'high': 29, 'unscored': 3}`.
- Câu chỉnh nhãn tổng hợp do không nhất quán: trước `[21, 25, 19, 24, 27, 28, 29, 32, 33, 37, 43, 44, 46, 47, 48, 49, 51, 53, 54, 56, 57]`; sau `[25, 26, 32, 33, 34, 36, 44, 45, 46, 48, 50, 51, 53, 54, 56, 58]`.

V16 bị Qwen timeout do chạy sinh/chấm đồng thời. V17–18 dừng để sửa lỗi kiểm tra phủ định nguồn; v19 thử riêng bảy câu. Sinh chính thức v20; chấm chính thức v23: Qwen chọn ID đoạn, schema ràng buộc trạng thái/ID, phần mềm lấy quote và nhận đúng 3/4 = 75%. Các điểm hợp lệ từ chấm v22 được kiểm tra lại toàn bộ quote/ID/số liệu bằng rubric cuối trước khi giữ, ghi hash mã gốc và mã tái kiểm tra; các câu lỗi/chưa chấm chạy lại. Chấm thử v20–21 không dùng trong số cuối. Không so sánh tốc độ giữa các lượt này.

## Bảy câu ưu tiên

| Câu | Trước | Sau | Bao phủ nguồn | Luồng cuối | Ký tự |
|---|---|---|---|---|---|
| 26 | partial | partial | một phần | gemini-agent | 2002 |
| 28 | low | partial | một phần | gemini-agent | 2065 |
| 29 | low | high | một phần | gemini-agent | 1603 |
| 32 | partial | partial | một phần | gemini-agent | 2001 |
| 37 | partial | high | đầy đủ | gemini-agent | 1555 |
| 47 | partial | high | đầy đủ | gemini-agent | 2497 |
| 52 | high | high | đầy đủ | gemini-agent | 1433 |

## Các khâu sửa

- Truy xuất giữ các nhóm nguồn riêng: thông tin/hóa đơn/thỏa thuận; mục đích/lưu trữ/cung cấp dữ liệu; phòng ngừa/thoát nạn/114; nghĩa vụ công dân/chủ hộ/hồ sơ cơ bản.
- Qwen chọn nguyên đơn vị nguồn; retry có giới hạn. Nếu còn chỗ trong bốn ID, quy tắc bổ sung đơn vị thật đã truy xuất cho nhóm bỏ sót, ghi `evidence_coverage_completion` trong trace. Nếu vẫn thiếu, đánh dấu một phần.
- Gemini tổng hợp có nguồn trong từng câu; phân biệt khuyến nghị với nghĩa vụ, điều kiện/chủ thể, hiệu lực muộn và ngoại lệ. Giữ giới hạn 3.500 ký tự.
- Kiểm chứng phân biệt phủ định/giới hạn nguồn và câu hỏi về thỏa thuận với khẳng định quyền/nghĩa vụ. Kiểm tra đúng chủ thể trong mệnh đề; nhận điều kiện hiệu lực và điều kiện đồng ý từ nguồn, giữ ngoại lệ. Vẫn chặn khẳng định không có nguồn.
- Gemini trả JSON sai schema được thử sửa một lần với nguyên nguồn đã chọn; không bỏ qua validation. Bản sửa vẫn qua kiểm chứng quy tắc và Gemini.
- Rà riêng đủ 36 mẫu, giữ nguyên bản gốc. Qwen chọn ID đoạn mẫu/trả lời, chương trình lấy quote nguyên văn. Bộ chấm chặn ID bịa, quote thiếu, nhận xét thiếu trong khi nguyên văn có trong câu trả lời, và số liệu/đơn vị khác bị gọi là khớp; số thứ tự không được coi là số liệu.
- Nhãn khớp tổng hợp suy ra từ các trạng thái ý chính đã qua audit, giữ nhãn Qwen gốc riêng; không chấp nhận nhãn high khi toàn bộ ý là different/missing.
- 154 kiểm thử hồi quy đã đạt cho mã xử lý, bộ chấm và tổng hợp nhãn dùng trong lượt này.

## Kho thử và dữ liệu giữ nguyên

`legal_word_priority7_v13_20261006`: **34 Word, 445 vector E5/384 chiều**. Graph `graph_rag_word_priority7_v13`; housing `housing_graph_word_priority7_v13`: **789 bản ghi/vector** trùng dữ liệu đang dùng theo hash toàn dòng.
Giữ 29 mục v11 nguyên byte; mở rộng từ Word gốc Điều 10 Luật Cư trú, Điều 3/398 BLDS và Điều 7 NĐ248; thêm trích đoạn thật EVNSPC Cần Thơ về công khai cách tính điện và Công an Phú Thọ về 114. Không OCR/PDF/tờ khai/mẫu hợp đồng hoặc nội dung tự soạn đưa vào embedding.
Audit hash toàn dòng của các kho đang dùng, dữ liệu public và người dùng đạt. Kho mới còn staging; chưa chuyển FastAPI sang kho này. Các kết quả dưới đây chạy ChatService thực trên kho thử, không phải kết quả từ HTTP API đang dùng kho v7.

## Cả 36 câu

| Câu | Trước | Sau | Bao phủ nguồn sau sửa |
|---|---|---|---|
| 19 | partial | partial | đầy đủ |
| 20 | high | high | đầy đủ |
| 21 | partial | high | đầy đủ |
| 22 | high | high | một phần |
| 23 | unscored | unscored | một phần |
| 24 | partial | high | một phần |
| 25 | partial | partial | một phần |
| 26 | partial | partial | một phần |
| 27 | partial | unscored | một phần |
| 28 | low | partial | một phần |
| 29 | low | high | một phần |
| 30 | high | high | đầy đủ |
| 31 | unscored | unscored | đầy đủ |
| 32 | partial | partial | một phần |
| 33 | partial | partial | đầy đủ |
| 34 | unscored | low | đầy đủ |
| 35 | high | high | đầy đủ |
| 36 | partial | low | một phần |
| 37 | partial | high | đầy đủ |
| 38 | high | high | đầy đủ |
| 43 | partial | high | một phần |
| 44 | partial | partial | một phần |
| 45 | unscored | low | một phần |
| 46 | partial | partial | đầy đủ |
| 47 | partial | high | đầy đủ |
| 48 | partial | partial | đầy đủ |
| 49 | partial | high | một phần |
| 50 | high | low | đầy đủ |
| 51 | partial | partial | đầy đủ |
| 52 | high | high | đầy đủ |
| 53 | partial | partial | một phần |
| 54 | partial | partial | đầy đủ |
| 55 | high | high | một phần |
| 56 | partial | partial | đầy đủ |
| 57 | partial | high | đầy đủ |
| 58 | high | partial | đầy đủ |

## Câu trả lời và nguồn cho từng kết luận

Mỗi câu trả lời giữ rank trích dẫn của lượt chạy. Sau đó là ánh xạ từng dòng kết luận sang URL/điều khoản. Đây là bằng chứng xuất xứ và đầu ra kiểm chứng của hệ thống; chưa thay thế thẩm định pháp lý độc lập.

### Câu 19: Trước khi ký hợp đồng thuê trọ, sinh viên nên kiểm tra những điều khoản nào?

Trước khi ký hợp đồng thuê trọ, sinh viên cần kiểm tra kỹ các nội dung pháp lý bắt buộc của hợp đồng thuê nhà ở cùng các điều khoản chi phí và quyền nghĩa vụ thực tế [1] [2] [3].

- Kiểm tra thông tin các bên, địa chỉ, mô tả đặc điểm phòng trọ và thời hạn thuê cũng như thời điểm có hiệu lực của hợp đồng [2].
- Kiểm tra giá thuê phòng, thời hạn và phương thức thanh toán tiền thuê theo thỏa thuận giữa các bên [1] [2] [3].
- Kiểm tra các khoản chi phí thực tế gồm tiền đặt cọc, giá điện nước, internet và các dịch vụ đi kèm [3].
- Kiểm tra quyền và nghĩa vụ của các bên, trách nhiệm do vi phạm hợp đồng và phương thức giải quyết tranh chấp [1] [2] [3].
- Kiểm tra danh mục tài sản, thiết bị được trang bị gắn liền với nơi ở để đối chiếu tình trạng thực tế trước khi nhận phòng [3].
- Khuyến nghị chốt số điện, số nước trên đồng hồ đo trước khi chuyển vào ở và ký nhận hợp đồng thành văn bản có đủ chữ ký mỗi bên giữ một bản [2] [3].

Nguồn thông tin về tiền đặt cọc, internet và kiểm tra thiết bị là hướng dẫn khuyến cáo thực hành, không phải quy định pháp luật bắt buộc của Nhà nước [3].
Hợp đồng thuê nhà ở phải tuân thủ điều kiện có hiệu lực của giao dịch dân sự về chủ thể tự nguyện, nội dung không vi phạm điều cấm và hình thức văn bản [2] [4].

Nguồn là bản Word/trích tuyển được cung cấp, chưa xác minh toàn bộ câu chữ với bản chính thức; không coi ghi chú biên tập là quy định pháp luật.
Hướng dẫn/khuyến cáo của Thư viện Đại học Bách khoa Hà Nội; không phải điều luật. Chỉ lấy phần kiểm tra thuê phòng; thông tin ký túc xá, xe buýt và địa bàn Hà Nội không áp dụng cho CTU. Không có ngày công bố hiển thị trong nội dung đã đọc; đây không phải quy định pháp luật.

Để áp dụng vào trường hợp của bạn:
- Hợp đồng thuê trọ của bạn dự kiến ký bằng văn bản giấy hay phương thức nào khác?
- Chủ nhà trọ đã cung cấp dự thảo hợp đồng có các điều khoản về đặt cọc và chi phí dịch vụ cụ thể chưa?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

**Nguồn của từng dòng có trích dẫn:**

- Trước khi ký hợp đồng thuê trọ, sinh viên cần kiểm tra kỹ các nội dung pháp lý bắt buộc của hợp đồng thuê nhà ở cùng các điều khoản chi phí và quyền nghĩa vụ thực tế [1] [2] [3].
  [1: Bộ luật Dân sự 91/2015/QH13 — Word do cơ quan nhà nước công bố — Điều 398. Nội dung của hợp đồng](https://congan.daklak.gov.vn/laws/detail/Bo-luat-Dan-su-163/); [2: Luật Nhà ở — 79/VBHN-VPQH — bản Word cung cấp — Điều 163. Hợp đồng về nhà ở](https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-79-vbhn-vpqh-469209.htm); [3: Kinh nghiệm tìm nhà trọ cho tân sinh viên — Thư viện Đại học Bách khoa Hà Nội — Kinh nghiệm tìm nhà trọ cho tân sinh viên | Đoạn nguyên văn 23](https://library.hust.edu.vn/vi/node/822)
- Kiểm tra thông tin các bên, địa chỉ, mô tả đặc điểm phòng trọ và thời hạn thuê cũng như thời điểm có hiệu lực của hợp đồng [2].
  [2: Luật Nhà ở — 79/VBHN-VPQH — bản Word cung cấp — Điều 163. Hợp đồng về nhà ở](https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-79-vbhn-vpqh-469209.htm)
- Kiểm tra giá thuê phòng, thời hạn và phương thức thanh toán tiền thuê theo thỏa thuận giữa các bên [1] [2] [3].
  [1: Bộ luật Dân sự 91/2015/QH13 — Word do cơ quan nhà nước công bố — Điều 398. Nội dung của hợp đồng](https://congan.daklak.gov.vn/laws/detail/Bo-luat-Dan-su-163/); [2: Luật Nhà ở — 79/VBHN-VPQH — bản Word cung cấp — Điều 163. Hợp đồng về nhà ở](https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-79-vbhn-vpqh-469209.htm); [3: Kinh nghiệm tìm nhà trọ cho tân sinh viên — Thư viện Đại học Bách khoa Hà Nội — Kinh nghiệm tìm nhà trọ cho tân sinh viên | Đoạn nguyên văn 23](https://library.hust.edu.vn/vi/node/822)
- Kiểm tra các khoản chi phí thực tế gồm tiền đặt cọc, giá điện nước, internet và các dịch vụ đi kèm [3].
  [3: Kinh nghiệm tìm nhà trọ cho tân sinh viên — Thư viện Đại học Bách khoa Hà Nội — Kinh nghiệm tìm nhà trọ cho tân sinh viên | Đoạn nguyên văn 23](https://library.hust.edu.vn/vi/node/822)
- Kiểm tra quyền và nghĩa vụ của các bên, trách nhiệm do vi phạm hợp đồng và phương thức giải quyết tranh chấp [1] [2] [3].
  [1: Bộ luật Dân sự 91/2015/QH13 — Word do cơ quan nhà nước công bố — Điều 398. Nội dung của hợp đồng](https://congan.daklak.gov.vn/laws/detail/Bo-luat-Dan-su-163/); [2: Luật Nhà ở — 79/VBHN-VPQH — bản Word cung cấp — Điều 163. Hợp đồng về nhà ở](https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-79-vbhn-vpqh-469209.htm); [3: Kinh nghiệm tìm nhà trọ cho tân sinh viên — Thư viện Đại học Bách khoa Hà Nội — Kinh nghiệm tìm nhà trọ cho tân sinh viên | Đoạn nguyên văn 23](https://library.hust.edu.vn/vi/node/822)
- Kiểm tra danh mục tài sản, thiết bị được trang bị gắn liền với nơi ở để đối chiếu tình trạng thực tế trước khi nhận phòng [3].
  [3: Kinh nghiệm tìm nhà trọ cho tân sinh viên — Thư viện Đại học Bách khoa Hà Nội — Kinh nghiệm tìm nhà trọ cho tân sinh viên | Đoạn nguyên văn 23](https://library.hust.edu.vn/vi/node/822)
- Khuyến nghị chốt số điện, số nước trên đồng hồ đo trước khi chuyển vào ở và ký nhận hợp đồng thành văn bản có đủ chữ ký mỗi bên giữ một bản [2] [3].
  [2: Luật Nhà ở — 79/VBHN-VPQH — bản Word cung cấp — Điều 163. Hợp đồng về nhà ở](https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-79-vbhn-vpqh-469209.htm); [3: Kinh nghiệm tìm nhà trọ cho tân sinh viên — Thư viện Đại học Bách khoa Hà Nội — Kinh nghiệm tìm nhà trọ cho tân sinh viên | Đoạn nguyên văn 23](https://library.hust.edu.vn/vi/node/822)
- Nguồn thông tin về tiền đặt cọc, internet và kiểm tra thiết bị là hướng dẫn khuyến cáo thực hành, không phải quy định pháp luật bắt buộc của Nhà nước [3].
  [3: Kinh nghiệm tìm nhà trọ cho tân sinh viên — Thư viện Đại học Bách khoa Hà Nội — Kinh nghiệm tìm nhà trọ cho tân sinh viên | Đoạn nguyên văn 23](https://library.hust.edu.vn/vi/node/822)
- Hợp đồng thuê nhà ở phải tuân thủ điều kiện có hiệu lực của giao dịch dân sự về chủ thể tự nguyện, nội dung không vi phạm điều cấm và hình thức văn bản [2] [4].
  [2: Luật Nhà ở — 79/VBHN-VPQH — bản Word cung cấp — Điều 163. Hợp đồng về nhà ở](https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-79-vbhn-vpqh-469209.htm); [4: Bộ luật Dân sự 91/2015/QH13 — Word do cơ quan nhà nước công bố — Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp](https://congan.daklak.gov.vn/laws/detail/Bo-luat-Dan-su-163/)

**Đối chiếu nguyên mẫu:**

Nhãn tổng hợp: **partial**; nhãn Qwen gốc: **partial**. Đáp án bao quát các nhóm điều khoản chính nhưng thiếu chi tiết về thẩm quyền cho thuê, văn bản ủy quyền và các con số cụ thể về đặt cọc cũng như thời hạn hoàn tiền so với tài liệu tham khảo.

**Rà mẫu/nguồn:** Checklist hữu ích; phân biệt điều luật liệt kê nội dung hợp đồng với khuyến nghị kiểm tra giấy tờ/ủy quyền.

| Điểm | Trích mẫu có thật | Trích câu trả lời có thật | Giải thích |
|---|---|---|---|
| different | Trước khi đặt bút ký hợp đồng, sinh viên cần rà soát kỹ **6 nhóm điều khoản cốt lõi**: | Trước khi ký hợp đồng thuê trọ, sinh viên cần kiểm tra kỹ các nội dung pháp lý bắt buộc của hợp đồng thuê nhà ở cùng các điều khoản chi phí và quyền nghĩa vụ thực tế [1] [2] [3]. | Đáp án tổng hợp các nhóm điều khoản nhưng thiếu chi tiết cụ thể về thẩm quyền cho thuê và ủy quyền. |
| matched | **Thông tin các bên & thẩm quyền cho thuê:** Họ tên, số CCCD/Căn cước, địa chỉ thường trú của chủ trọ. | - Kiểm tra thông tin các bên, địa chỉ, mô tả đặc điểm phòng trọ và thời hạn thuê cũng như thời điểm có hiệu lực của hợp đồng [2]. | Đáp án đề cập thông tin các bên và địa chỉ, khớp với yêu cầu kiểm tra chủ thể hợp đồng. |
| different | Nếu ký với người đại diện/quản lý, yêu cầu xuất trình văn bản ủy quyền hợp pháp từ chủ sở hữu. | Trước khi ký hợp đồng thuê trọ, sinh viên cần kiểm tra kỹ các nội dung pháp lý bắt buộc của hợp đồng thuê nhà ở cùng các điều khoản chi phí và quyền nghĩa vụ thực tế [1] [2] [3]. | Đáp án thiếu điều khoản về văn bản ủy quyền khi ký với người đại diện như trong tài liệu tham khảo. |
| matched | **Giá thuê & phương thức thanh toán:** Mức tiền thuê phòng cố định trong bao lâu? | - Kiểm tra giá thuê phòng, thời hạn và phương thức thanh toán tiền thuê theo thỏa thuận giữa các bên [1] [2] [3]. | Đáp án liệt kê giá thuê và phương thức thanh toán, khớp với các mục về chi phí dịch vụ phát sinh. |
| different | Ngày thanh toán định kỳ hàng tháng? | - Kiểm tra các khoản chi phí thực tế gồm tiền đặt cọc, giá điện nước, internet và các dịch vụ đi kèm [3]. | Đáp án thiếu thông tin cụ thể về mức tiền đặt cọc, điều kiện hoàn cọc và thời hạn trả lại tiền. |
| matched | Phương thức trả (chuyển khoản hay tiền mặt)? | - Kiểm tra danh mục tài sản, thiết bị được trang bị gắn liền với nơi ở để đối chiếu tình trạng thực tế trước khi nhận phòng [3]. | Đáp án đề cập danh mục tài sản và tình trạng thực tế, khớp với yêu cầu kiểm tra biên bản hiện trạng. |

### Câu 20: Hợp đồng thuê phòng có cần ghi rõ tiền cọc, tiền thuê và ngày thanh toán không?

Hợp đồng về nhà ở bắt buộc phải có nội dung thỏa thuận về giá giao dịch cùng thời hạn và phương thức thanh toán tiền khi cho thuê [2].

- Ghi nhận cụ thể giá thuê nhà ở hoặc mức giá theo thỏa thuận vào văn bản hợp đồng [2].
- Xác định rõ thời hạn thanh toán tiền thuê định kỳ và phương thức trả tiền trong nội dung hợp đồng [2].
- Thỏa thuận rõ khoản tài sản đặt cọc, thời hạn và mục đích bảo đảm giao kết hoặc thực hiện hợp đồng theo quy định đặt cọc [1].
- Khuyến nghị đối chiếu và ghi rõ cách xử lý tài sản đặt cọc khi hợp đồng được thực hiện hoặc khi một bên từ chối thực hiện [1].

Nguồn trích dẫn quy định chung về nội dung hợp đồng nhà ở và biện pháp đặt cọc mà không ấn định mức tiền cọc hoặc ngày thanh toán cụ thể [1] [2].

Nguồn là bản Word/trích tuyển được cung cấp, chưa xác minh toàn bộ câu chữ với bản chính thức; không coi ghi chú biên tập là quy định pháp luật.

Để áp dụng vào trường hợp của bạn:
- Hợp đồng thuê phòng của bạn hiện đã lập thành văn bản và có điều khoản về tiền cọc chưa?
- Hai bên dự kiến thanh toán tiền thuê theo chu kỳ từng tháng hay theo khoảng thời gian nào khác?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

**Nguồn của từng dòng có trích dẫn:**

- Hợp đồng về nhà ở bắt buộc phải có nội dung thỏa thuận về giá giao dịch cùng thời hạn và phương thức thanh toán tiền khi cho thuê [2].
  [2: Luật Nhà ở — 79/VBHN-VPQH — bản Word cung cấp — Điều 163. Hợp đồng về nhà ở](https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-79-vbhn-vpqh-469209.htm)
- Ghi nhận cụ thể giá thuê nhà ở hoặc mức giá theo thỏa thuận vào văn bản hợp đồng [2].
  [2: Luật Nhà ở — 79/VBHN-VPQH — bản Word cung cấp — Điều 163. Hợp đồng về nhà ở](https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-79-vbhn-vpqh-469209.htm)
- Xác định rõ thời hạn thanh toán tiền thuê định kỳ và phương thức trả tiền trong nội dung hợp đồng [2].
  [2: Luật Nhà ở — 79/VBHN-VPQH — bản Word cung cấp — Điều 163. Hợp đồng về nhà ở](https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-79-vbhn-vpqh-469209.htm)
- Thỏa thuận rõ khoản tài sản đặt cọc, thời hạn và mục đích bảo đảm giao kết hoặc thực hiện hợp đồng theo quy định đặt cọc [1].
  [1: Bộ luật Dân sự 91/2015/QH13 — Word do cơ quan nhà nước công bố — Điều 328. Đặt cọc](https://congan.daklak.gov.vn/laws/detail/Bo-luat-Dan-su-163/)
- Khuyến nghị đối chiếu và ghi rõ cách xử lý tài sản đặt cọc khi hợp đồng được thực hiện hoặc khi một bên từ chối thực hiện [1].
  [1: Bộ luật Dân sự 91/2015/QH13 — Word do cơ quan nhà nước công bố — Điều 328. Đặt cọc](https://congan.daklak.gov.vn/laws/detail/Bo-luat-Dan-su-163/)
- Nguồn trích dẫn quy định chung về nội dung hợp đồng nhà ở và biện pháp đặt cọc mà không ấn định mức tiền cọc hoặc ngày thanh toán cụ thể [1] [2].
  [1: Bộ luật Dân sự 91/2015/QH13 — Word do cơ quan nhà nước công bố — Điều 328. Đặt cọc](https://congan.daklak.gov.vn/laws/detail/Bo-luat-Dan-su-163/); [2: Luật Nhà ở — 79/VBHN-VPQH — bản Word cung cấp — Điều 163. Hợp đồng về nhà ở](https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-79-vbhn-vpqh-469209.htm)

**Đối chiếu nguyên mẫu:**

Nhãn tổng hợp: **high**; nhãn Qwen gốc: **high**. ANSWER bao phủ đầy đủ các ý chính về tính bắt buộc, nội dung tiền cọc, tiền thuê và ngày thanh toán so với REFERENCE.

**Rà mẫu/nguồn:** Không coi khoản đặt cọc là nội dung bắt buộc của mọi hợp đồng hoặc mọi thỏa thuận cọc phải viết riêng; phân biệt Điều 163 Luật Nhà ở với Điều 328 BLDS và thỏa thuận cụ thể.

| Điểm | Trích mẫu có thật | Trích câu trả lời có thật | Giải thích |
|---|---|---|---|
| matched | **Rất cần thiết và bắt buộc phải ghi rõ bằng văn bản.** | - Ghi nhận cụ thể giá thuê nhà ở hoặc mức giá theo thỏa thuận vào văn bản hợp đồng [2]. | REFERENCE khẳng định việc ghi rõ là bắt buộc, ANSWER đồng ý với nội dung này. |
| matched | - **Tiền đặt cọc:** Là biện pháp bảo đảm thực hiện nghĩa vụ theo Điều 328 BLDS 2015. | - Thỏa thuận rõ khoản tài sản đặt cọc, thời hạn và mục đích bảo đảm giao kết hoặc thực hiện hợp đồng theo quy định đặt cọc [1]. | REFERENCE nêu tiền cọc là biện pháp bảo đảm, ANSWER xác nhận thỏa thuận về khoản đặt cọc [1]. |
| matched | Hợp đồng phải nêu rõ mức tiền cọc, mục đích giữ cọc và điều kiện cụ thể để được hoàn trả hoặc cấn trừ tiền phòng. | - Khuyến nghị đối chiếu và ghi rõ cách xử lý tài sản đặt cọc khi hợp đồng được thực hiện hoặc khi một bên từ chối thực hiện [1]. | REFERENCE yêu cầu ghi rõ mục đích và điều kiện hoàn trả cọc, ANSWER khuyến nghị ghi cách xử lý tài sản đặt cọc [1]. |
| matched | - **Tiền thuê phòng:** Phải được ấn định con số cụ thể nhằm bảo vệ người thuê khỏi việc chủ trọ tự ý tăng giá bất thường giữa chừng. | - Ghi nhận cụ thể giá thuê nhà ở hoặc mức giá theo thỏa thuận vào văn bản hợp đồng [2]. | REFERENCE nhấn mạnh tiền thuê phải có con số cụ thể, ANSWER ghi nhận giá thuê vào văn bản [2]. |
| matched | - **Ngày thanh toán:** Xác định rõ mốc thời gian hoàn thành nghĩa vụ trả tiền để tránh tranh chấp bị phạt tiền trễ hạn vô lý. | - Xác định rõ thời hạn thanh toán tiền thuê định kỳ và phương thức trả tiền trong nội dung hợp đồng [2]. | REFERENCE yêu cầu xác định mốc thời gian thanh toán, ANSWER xác định rõ thời hạn và phương thức trả tiền [2]. |

### Câu 21: Nếu chủ trọ muốn tăng giá thuê giữa thời hạn hợp đồng thì cần xem xét những gì?

Bên cho thuê và bên thuê được thỏa thuận về giá thuê nhà ở, trừ trường hợp Nhà nước có quy định về giá thuê thì phải thực hiện theo quy định đó [3].

- Kiểm tra sự đồng thuận của bên thuê đối với việc cải tạo nhà ở khi bên cho thuê tiến hành cải tạo [1].
- Xác định thời gian cho thuê còn lại có từ một phần ba thời hạn của hợp đồng thuê nhà ở trở xuống hay không khi bên cho thuê thực hiện cải tạo và được bên thuê đồng ý [1].
- Thỏa thuận về mức giá thuê nhà ở mới giữa các bên trong trường hợp bên cho thuê được quyền điều chỉnh giá [1].
- Xem xét quyền đơn phương chấm dứt hợp đồng và nghĩa vụ bồi thường cho bên thuê của bên cho thuê nếu hai bên không thỏa thuận được giá mới sau cải tạo [1].

Nguồn trích tuyển nêu cụ thể điều kiện điều chỉnh giá khi cải tạo nhà ở, chưa loại trừ các căn cứ điều chỉnh giá khác theo thỏa thuận chung của hợp đồng [1] [3].

Nguồn là bản Word/trích tuyển được cung cấp, chưa xác minh toàn bộ câu chữ với bản chính thức; không coi ghi chú biên tập là quy định pháp luật.

Để áp dụng vào trường hợp của bạn:
- Hợp đồng thuê phòng của bạn hiện có điều khoản nào quy định về việc điều chỉnh giá thuê không?
- Chủ trọ muốn tăng giá do cải tạo phòng hay vì lý do nào khác?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

**Nguồn của từng dòng có trích dẫn:**

- Bên cho thuê và bên thuê được thỏa thuận về giá thuê nhà ở, trừ trường hợp Nhà nước có quy định về giá thuê thì phải thực hiện theo quy định đó [3].
  [3: Luật Nhà ở — 79/VBHN-VPQH — bản Word cung cấp — Điều 170. Thời hạn thuê, giá thuê, cho thuê lại nhà ở | Khoản 1](https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-79-vbhn-vpqh-469209.htm)
- Kiểm tra sự đồng thuận của bên thuê đối với việc cải tạo nhà ở khi bên cho thuê tiến hành cải tạo [1].
  [1: Luật Nhà ở — 79/VBHN-VPQH — bản Word cung cấp — Điều 170. Thời hạn thuê, giá thuê, cho thuê lại nhà ở | Khoản 2](https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-79-vbhn-vpqh-469209.htm)
- Xác định thời gian cho thuê còn lại có từ một phần ba thời hạn của hợp đồng thuê nhà ở trở xuống hay không khi bên cho thuê thực hiện cải tạo và được bên thuê đồng ý [1].
  [1: Luật Nhà ở — 79/VBHN-VPQH — bản Word cung cấp — Điều 170. Thời hạn thuê, giá thuê, cho thuê lại nhà ở | Khoản 2](https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-79-vbhn-vpqh-469209.htm)
- Thỏa thuận về mức giá thuê nhà ở mới giữa các bên trong trường hợp bên cho thuê được quyền điều chỉnh giá [1].
  [1: Luật Nhà ở — 79/VBHN-VPQH — bản Word cung cấp — Điều 170. Thời hạn thuê, giá thuê, cho thuê lại nhà ở | Khoản 2](https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-79-vbhn-vpqh-469209.htm)
- Xem xét quyền đơn phương chấm dứt hợp đồng và nghĩa vụ bồi thường cho bên thuê của bên cho thuê nếu hai bên không thỏa thuận được giá mới sau cải tạo [1].
  [1: Luật Nhà ở — 79/VBHN-VPQH — bản Word cung cấp — Điều 170. Thời hạn thuê, giá thuê, cho thuê lại nhà ở | Khoản 2](https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-79-vbhn-vpqh-469209.htm)
- Nguồn trích tuyển nêu cụ thể điều kiện điều chỉnh giá khi cải tạo nhà ở, chưa loại trừ các căn cứ điều chỉnh giá khác theo thỏa thuận chung của hợp đồng [1] [3].
  [1: Luật Nhà ở — 79/VBHN-VPQH — bản Word cung cấp — Điều 170. Thời hạn thuê, giá thuê, cho thuê lại nhà ở | Khoản 2](https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-79-vbhn-vpqh-469209.htm); [3: Luật Nhà ở — 79/VBHN-VPQH — bản Word cung cấp — Điều 170. Thời hạn thuê, giá thuê, cho thuê lại nhà ở | Khoản 1](https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-79-vbhn-vpqh-469209.htm)

**Đối chiếu nguyên mẫu:**

Nhãn tổng hợp: **high**; nhãn Qwen gốc: **high**. Đáp án bao phủ đầy đủ các điều kiện pháp lý về cải tạo nhà và thỏa thuận giá thuê trong thời hạn hợp đồng.

**Rà mẫu/nguồn:** Bản Word cung cấp Điều 170 khoản 2 có cụm một phần ba trở xuống như mẫu; chưa chứng nhận bản trích tuyển là nguyên văn chính thức. Giữ điều kiện cải tạo, đồng ý, thỏa thuận giá và bồi thường, không suy ra mọi trường hợp đương nhiên hoàn toàn bộ cọc.

| Điểm | Trích mẫu có thật | Trích câu trả lời có thật | Giải thích |
|---|---|---|---|
| matched | **Thỏa thuận trong hợp đồng:** Trong thời hạn hợp đồng còn hiệu lực, bên cho thuê **không được tự ý tăng giá thuê** trừ trường hợp hợp đồng có điều khoản quy định rõ lộ trình điều chỉnh giá. | Bên cho thuê và bên thuê được thỏa thuận về giá thuê nhà ở, trừ trường hợp Nhà nước có quy định về giá thuê thì phải thực hiện theo quy định đó [3]. | Chủ trọ không được tự ý tăng giá nếu hợp đồng chưa có điều khoản quy định lộ trình điều chỉnh. |
| matched | **Trường hợp cải tạo nhà ở:** Theo Khoản 2 Điều 170 Luật Nhà ở, bên cho thuê chỉ được quyền điều chỉnh giá thuê nếu đã thực hiện cải tạo nhà ở, **được bên thuê đồng ý** và thời gian thuê còn lại từ $1/3$ thời hạn hợp đồng trở xuống. | - Kiểm tra sự đồng thuận của bên thuê đối với việc cải tạo nhà ở khi bên cho thuê tiến hành cải tạo [1]. | Việc tăng giá chỉ được phép khi đã cải tạo nhà, có sự đồng ý của bên thuê và thời gian còn lại dưới 1/3 hợp đồng. |
| matched | **Quyền của sinh viên:** Nếu không có thỏa thuận tăng giá, người thuê có quyền từ chối mức giá mới và tiếp tục trả giá cũ đến hết hạn hợp đồng. | - Xác định thời gian cho thuê còn lại có từ một phần ba thời hạn của hợp đồng thuê nhà ở trở xuống hay không khi bên cho thuê thực hiện cải tạo và được bên thuê đồng ý [1]. | Người thuê có quyền từ chối mức giá mới nếu không có thỏa thuận trước đó trong hợp đồng. |

### Câu 22: Khi trả phòng, việc hoàn lại tiền cọc được xác định theo hợp đồng và quy định như thế nào?

Khi hợp đồng được thực hiện, tài sản đặt cọc được trả lại cho bên đặt cọc hoặc được trừ để thực hiện nghĩa vụ trả tiền, trừ trường hợp các bên có thỏa thuận khác [1].

- Khuyến nghị đối chiếu các điều khoản đã ghi trong hợp đồng thuê và hợp đồng đặt cọc về thời hạn hợp đồng cũng như việc xử lý tiền đặt cọc khi kết thúc trước hạn [3].
- Khuyến nghị kiểm tra bản chính biên nhận đặt cọc và hợp đồng thuê đã lưu giữ để xác định số tiền cọc thực tế đã giao [3].
- Trường hợp bên nhận đặt cọc từ chối thực hiện hợp đồng thì phải trả cho bên đặt cọc tài sản đặt cọc và một khoản tiền tương đương giá trị tài sản đặt cọc, trừ trường hợp có thỏa thuận khác [1].
- Trường hợp bên đặt cọc từ chối thực hiện hợp đồng thì tài sản đặt cọc thuộc về bên nhận đặt cọc, trừ trường hợp có thỏa thuận khác [1].

Chưa đủ căn cứ từ nguồn để quy định thời hạn hoàn cọc cố định hoặc các khoản cấn trừ chi phí cụ thể khi bàn giao trả phòng [1] [3].
Giao dịch dân sự về đặt cọc và thuê phòng phải đáp ứng các điều kiện có hiệu lực về chủ thể, sự tự nguyện, mục đích và nội dung không vi phạm điều cấm của luật, không trái đạo đức xã hội [4].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng.
Hướng dẫn/khuyến cáo của Trợ Giúp Chợ Tốt; không phải điều luật. Mẹo giao dịch, không phải điều luật. Không chứng minh hạn hoàn cọc cố định hoặc mức cọc bắt buộc; không thay thế xác minh người được ủy quyền cho thuê. Chỉ đọc phần kiểm tra, không bổ sung mẫu soạn hợp đồng.

Để áp dụng vào trường hợp của bạn:
- Hợp đồng thuê của bạn có điều khoản riêng về thời hạn hoàn cọc hoặc trừ tiền cọc khi trả phòng không?
- Bạn trả phòng khi hết hạn hợp đồng hay chấm dứt hợp đồng trước hạn?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

**Nguồn của từng dòng có trích dẫn:**

- Khi hợp đồng được thực hiện, tài sản đặt cọc được trả lại cho bên đặt cọc hoặc được trừ để thực hiện nghĩa vụ trả tiền, trừ trường hợp các bên có thỏa thuận khác [1].
  [1: Bộ luật Dân sự 91/2015/QH13 — Word do cơ quan nhà nước công bố — Điều 328. Đặt cọc](https://congan.daklak.gov.vn/laws/detail/Bo-luat-Dan-su-163/)
- Khuyến nghị đối chiếu các điều khoản đã ghi trong hợp đồng thuê và hợp đồng đặt cọc về thời hạn hợp đồng cũng như việc xử lý tiền đặt cọc khi kết thúc trước hạn [3].
  [3: Mẹo khi thuê phòng — Trợ Giúp Chợ Tốt — Mẹo khi thuê phòng | Đoạn nguyên văn 78](https://trogiup.chotot.com/nguoi-mua/meo-khi-thue-phong/)
- Khuyến nghị kiểm tra bản chính biên nhận đặt cọc và hợp đồng thuê đã lưu giữ để xác định số tiền cọc thực tế đã giao [3].
  [3: Mẹo khi thuê phòng — Trợ Giúp Chợ Tốt — Mẹo khi thuê phòng | Đoạn nguyên văn 78](https://trogiup.chotot.com/nguoi-mua/meo-khi-thue-phong/)
- Trường hợp bên nhận đặt cọc từ chối thực hiện hợp đồng thì phải trả cho bên đặt cọc tài sản đặt cọc và một khoản tiền tương đương giá trị tài sản đặt cọc, trừ trường hợp có thỏa thuận khác [1].
  [1: Bộ luật Dân sự 91/2015/QH13 — Word do cơ quan nhà nước công bố — Điều 328. Đặt cọc](https://congan.daklak.gov.vn/laws/detail/Bo-luat-Dan-su-163/)
- Trường hợp bên đặt cọc từ chối thực hiện hợp đồng thì tài sản đặt cọc thuộc về bên nhận đặt cọc, trừ trường hợp có thỏa thuận khác [1].
  [1: Bộ luật Dân sự 91/2015/QH13 — Word do cơ quan nhà nước công bố — Điều 328. Đặt cọc](https://congan.daklak.gov.vn/laws/detail/Bo-luat-Dan-su-163/)
- Chưa đủ căn cứ từ nguồn để quy định thời hạn hoàn cọc cố định hoặc các khoản cấn trừ chi phí cụ thể khi bàn giao trả phòng [1] [3].
  [1: Bộ luật Dân sự 91/2015/QH13 — Word do cơ quan nhà nước công bố — Điều 328. Đặt cọc](https://congan.daklak.gov.vn/laws/detail/Bo-luat-Dan-su-163/); [3: Mẹo khi thuê phòng — Trợ Giúp Chợ Tốt — Mẹo khi thuê phòng | Đoạn nguyên văn 78](https://trogiup.chotot.com/nguoi-mua/meo-khi-thue-phong/)
- Giao dịch dân sự về đặt cọc và thuê phòng phải đáp ứng các điều kiện có hiệu lực về chủ thể, sự tự nguyện, mục đích và nội dung không vi phạm điều cấm của luật, không trái đạo đức xã hội [4].
  [4: Bộ luật Dân sự 91/2015/QH13 — Word do cơ quan nhà nước công bố — Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp](https://congan.daklak.gov.vn/laws/detail/Bo-luat-Dan-su-163/)

**Đối chiếu nguyên mẫu:**

Nhãn tổng hợp: **high**; nhãn Qwen gốc: **high**. Đáp án bao phủ đầy đủ nghĩa vụ hoàn trả, các trường hợp khấu trừ hợp pháp và điều kiện hiệu lực của hợp đồng đặt cọc so với văn bản tham chiếu.

**Rà mẫu/nguồn:** Hoàn/khấu trừ cọc phụ thuộc mục đích bảo đảm, nghĩa vụ và thỏa thuận; Điều 328 không phải danh sách đóng tất cả tình huống khấu trừ. Tách khuyến nghị bàn giao khỏi quy định luật.

| Điểm | Trích mẫu có thật | Trích câu trả lời có thật | Giải thích |
|---|---|---|---|
| matched | **Nghĩa vụ trả lại tiền cọc:** Khi hợp đồng chấm dứt đúng thời hạn, người thuê đã thanh toán đủ tiền nhà, điện nước và bàn giao lại phòng theo đúng hiện trạng ban đầu (trừ hao mòn tự nhiên theo thời gian), **chủ trọ có nghĩa vụ hoàn trả lại | Khi hợp đồng được thực hiện, tài sản đặt cọc được trả lại cho bên đặt cọc hoặc được trừ để thực hiện nghĩa vụ trả tiền, trừ trường hợp các bên có thỏa thuận khác [1]. | Khi hợp đồng chấm dứt đúng hạn và bàn giao phòng đúng hiện trạng, chủ trọ có nghĩa vụ hoàn trả toàn bộ tiền cọc. |
| matched | **Các trường hợp được khấu trừ cọc hợp pháp:** Chủ nhà chỉ được trừ cọc khi: (i) Người thuê làm hư hại tài sản trong phòng do lỗi chủ quan; | Khi hợp đồng được thực hiện, tài sản đặt cọc được trả lại cho bên đặt cọc hoặc được trừ để thực hiện nghĩa vụ trả tiền, trừ trường hợp các bên có thỏa thuận khác [1]. | Tiền cọc chỉ được khấu trừ khi người thuê làm hư hại tài sản do lỗi chủ quan, còn nợ tiền hoặc đơn phương dọn đi sớm không báo trước. |
| matched | **Khuyến nghị thực tế:** Chụp ảnh/quay video phòng lúc nhận phòng và lúc dọn đi; | Giao dịch dân sự về đặt cọc và thuê phòng phải đáp ứng các điều kiện có hiệu lực về chủ thể, sự tự nguyện, mục đích và nội dung không vi phạm điều cấm của luật, không trái đạo đức xã hội [4]. | Giao dịch dân sự về đặt cọc và thuê phòng phải đáp ứng các điều kiện có hiệu lực về chủ thể, sự tự nguyện và nội dung hợp pháp. |

### Câu 23: Chủ trọ được thu tiền điện của người thuê như thế nào theo quy định?

Trường hợp người thuê không trực tiếp ký hợp đồng mua bán điện, tổng tiền điện chủ trọ thu không được vượt quá số tiền trên hoá đơn hằng tháng do đơn vị bán lẻ điện phát hành [1].

- Nếu có hợp đồng thuê từ 12 tháng trở lên và có đăng ký tạm trú hoặc thường trú, chủ trọ đứng tên ký hợp đồng hoặc để đại diện bên thuê ký kết nếu có cam kết thanh toán của chủ trọ [1].
- Nếu thời hạn thuê dưới 12 tháng và chủ trọ không kê khai đủ số người, tiền điện tính theo giá bán lẻ bậc 2 từ 101 đến 200 kWh cho toàn bộ sản lượng đo đếm được [1].
- Nếu chủ trọ kê khai đủ số người sử dụng điện dựa trên thông tin cư trú, bên bán điện cấp định mức với tỷ lệ 4 người tính thành một hộ dùng điện [1].
- Khuyến nghị người thuê đối chiếu số lượng người cư trú thực tế và hóa đơn tiền điện hằng tháng của bên bán lẻ điện để kiểm tra mức thu của chủ nhà [1].

Quy định về giá bán lẻ điện cho sinh viên và người lao động thuê trọ tại điểm c khoản 5 Điều 12 có hiệu lực từ ngày thực hiện điều chỉnh giá bán lẻ điện bình quân gần nhất sau khi Quyết định 14/2025/QĐ-TTg có hiệu lực thi hành [1] [2].
Văn bản trích dẫn là bản Word được cung cấp và chưa xác minh toàn bộ nội dung với bản lưu trữ chính thức [1] [2].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng.
Nguồn có hiệu lực có điều kiện; chưa xác nhận văn bản/sự kiện kích hoạt.
Nguồn là bản Word/trích tuyển được cung cấp, chưa xác minh toàn bộ câu chữ với bản chính thức; không coi ghi chú biên tập là quy định pháp luật.

Để áp dụng vào trường hợp của bạn:
- Hợp đồng thuê trọ của bạn có thời hạn dưới 12 tháng hay từ 12 tháng trở lên?
- Chủ trọ hiện đã thực hiện kê khai thông tin cư trú của bạn với bên bán điện chưa?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

**Nguồn của từng dòng có trích dẫn:**

- Trường hợp người thuê không trực tiếp ký hợp đồng mua bán điện, tổng tiền điện chủ trọ thu không được vượt quá số tiền trên hoá đơn hằng tháng do đơn vị bán lẻ điện phát hành [1].
  [1: Thông tư 60/2025/TT-BCT — bản Word trích tuyển cung cấp — Điều 12. Giá bán lẻ điện sinh hoạt | Khoản 5](https://vanban.chinhphu.vn/?docid=216125&orggroupid=4&pageid=27160)
- Nếu có hợp đồng thuê từ 12 tháng trở lên và có đăng ký tạm trú hoặc thường trú, chủ trọ đứng tên ký hợp đồng hoặc để đại diện bên thuê ký kết nếu có cam kết thanh toán của chủ trọ [1].
  [1: Thông tư 60/2025/TT-BCT — bản Word trích tuyển cung cấp — Điều 12. Giá bán lẻ điện sinh hoạt | Khoản 5](https://vanban.chinhphu.vn/?docid=216125&orggroupid=4&pageid=27160)
- Nếu thời hạn thuê dưới 12 tháng và chủ trọ không kê khai đủ số người, tiền điện tính theo giá bán lẻ bậc 2 từ 101 đến 200 kWh cho toàn bộ sản lượng đo đếm được [1].
  [1: Thông tư 60/2025/TT-BCT — bản Word trích tuyển cung cấp — Điều 12. Giá bán lẻ điện sinh hoạt | Khoản 5](https://vanban.chinhphu.vn/?docid=216125&orggroupid=4&pageid=27160)
- Nếu chủ trọ kê khai đủ số người sử dụng điện dựa trên thông tin cư trú, bên bán điện cấp định mức với tỷ lệ 4 người tính thành một hộ dùng điện [1].
  [1: Thông tư 60/2025/TT-BCT — bản Word trích tuyển cung cấp — Điều 12. Giá bán lẻ điện sinh hoạt | Khoản 5](https://vanban.chinhphu.vn/?docid=216125&orggroupid=4&pageid=27160)
- Khuyến nghị người thuê đối chiếu số lượng người cư trú thực tế và hóa đơn tiền điện hằng tháng của bên bán lẻ điện để kiểm tra mức thu của chủ nhà [1].
  [1: Thông tư 60/2025/TT-BCT — bản Word trích tuyển cung cấp — Điều 12. Giá bán lẻ điện sinh hoạt | Khoản 5](https://vanban.chinhphu.vn/?docid=216125&orggroupid=4&pageid=27160)
- Quy định về giá bán lẻ điện cho sinh viên và người lao động thuê trọ tại điểm c khoản 5 Điều 12 có hiệu lực từ ngày thực hiện điều chỉnh giá bán lẻ điện bình quân gần nhất sau khi Quyết định 14/2025/QĐ-TTg có hiệu lực thi hành [1] [2].
  [1: Thông tư 60/2025/TT-BCT — bản Word trích tuyển cung cấp — Điều 12. Giá bán lẻ điện sinh hoạt | Khoản 5](https://vanban.chinhphu.vn/?docid=216125&orggroupid=4&pageid=27160); [2: Thông tư 60/2025/TT-BCT — bản Word trích tuyển cung cấp — Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp](https://vanban.chinhphu.vn/?docid=216125&orggroupid=4&pageid=27160)
- Văn bản trích dẫn là bản Word được cung cấp và chưa xác minh toàn bộ nội dung với bản lưu trữ chính thức [1] [2].
  [1: Thông tư 60/2025/TT-BCT — bản Word trích tuyển cung cấp — Điều 12. Giá bán lẻ điện sinh hoạt | Khoản 5](https://vanban.chinhphu.vn/?docid=216125&orggroupid=4&pageid=27160); [2: Thông tư 60/2025/TT-BCT — bản Word trích tuyển cung cấp — Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp](https://vanban.chinhphu.vn/?docid=216125&orggroupid=4&pageid=27160)

**Đối chiếu nguyên mẫu:**

Nhãn tổng hợp: **unscored**; nhãn Qwen gốc: **unscored**. Chưa chấm được; không tạo điểm thay thế.

**Rà mẫu/nguồn:** Mệnh đề không vượt hóa đơn nhưng lại cộng hao hụt có thể tự mâu thuẫn; nguồn Điều 12 khoản 5 TT60 không xác nhận khoản cộng thêm này. Giữ điều kiện chuyển tiếp trước khi áp bậc giá.

**Lỗi kiểm tra bộ chấm:** points[3]: matched numeric point lacks corresponding answer quantities and units

### Câu 24: Ba sinh viên ở chung một phòng được tính tiền điện ra sao?

Tiền điện của ba sinh viên ở chung phòng phụ thuộc vào việc kê khai số người cư trú hoặc thời hạn hợp đồng thuê nhà theo quy định áp dụng từ ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành [1] [2].

- Nếu chủ nhà kê khai đầy đủ thông tin cư trú của 03 người sử dụng điện thì được tính 3/4 định mức áp dụng giá bán lẻ điện sinh hoạt theo quy định có hiệu lực từ ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành [1] [2].
- Nếu hợp đồng thuê dưới 12 tháng và chủ nhà không kê khai đầy đủ số người thì áp dụng giá bán lẻ điện sinh hoạt bậc 2 cho toàn bộ sản lượng đo đếm theo quy định có hiệu lực từ ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành [1] [2].
- Trường hợp thuê từ 12 tháng trở lên có đăng ký cư trú thì chủ nhà trực tiếp ký hoặc đại diện sinh viên ký hợp đồng mua bán điện theo quy định có hiệu lực từ ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành [1] [2].
- Nếu không giao kết hợp đồng trực tiếp với bên bán điện thì tổng tiền điện chủ nhà thu không được vượt quá hóa đơn tiền điện hằng tháng do bên bán lẻ điện phát hành theo quy định có hiệu lực từ ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành [1] [2].

Quy định về giá bán lẻ điện cho sinh viên thuê nhà tại điểm c khoản 5 Điều 12 Thông tư 60/2025/TT-BCT chỉ có hiệu lực thi hành kể từ ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực [1] [2].
Văn bản trích dẫn là bản Word trích tuyển được cung cấp, chưa được đối chiếu toàn văn với văn bản chính thức [1].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng.
Nguồn có hiệu lực có điều kiện; chưa xác nhận văn bản/sự kiện kích hoạt.
Nguồn là bản Word/trích tuyển được cung cấp, chưa xác minh toàn bộ câu chữ với bản chính thức; không coi ghi chú biên tập là quy định pháp luật.

Để áp dụng vào trường hợp của bạn:
- Hợp đồng thuê phòng của các bạn có thời hạn từ 12 tháng trở lên hay dưới 12 tháng?
- Chủ nhà trọ đã thực hiện đăng ký tạm trú và kê khai số lượng 03 người với bên bán điện chưa?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

**Nguồn của từng dòng có trích dẫn:**

- Tiền điện của ba sinh viên ở chung phòng phụ thuộc vào việc kê khai số người cư trú hoặc thời hạn hợp đồng thuê nhà theo quy định áp dụng từ ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành [1] [2].
  [1: Thông tư 60/2025/TT-BCT — bản Word trích tuyển cung cấp — Điều 12. Giá bán lẻ điện sinh hoạt | Khoản 5](https://vanban.chinhphu.vn/?docid=216125&orggroupid=4&pageid=27160); [2: Thông tư 60/2025/TT-BCT — bản Word trích tuyển cung cấp — Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp](https://vanban.chinhphu.vn/?docid=216125&orggroupid=4&pageid=27160)
- Nếu chủ nhà kê khai đầy đủ thông tin cư trú của 03 người sử dụng điện thì được tính 3/4 định mức áp dụng giá bán lẻ điện sinh hoạt theo quy định có hiệu lực từ ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành [1] [2].
  [1: Thông tư 60/2025/TT-BCT — bản Word trích tuyển cung cấp — Điều 12. Giá bán lẻ điện sinh hoạt | Khoản 5](https://vanban.chinhphu.vn/?docid=216125&orggroupid=4&pageid=27160); [2: Thông tư 60/2025/TT-BCT — bản Word trích tuyển cung cấp — Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp](https://vanban.chinhphu.vn/?docid=216125&orggroupid=4&pageid=27160)
- Nếu hợp đồng thuê dưới 12 tháng và chủ nhà không kê khai đầy đủ số người thì áp dụng giá bán lẻ điện sinh hoạt bậc 2 cho toàn bộ sản lượng đo đếm theo quy định có hiệu lực từ ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành [1] [2].
  [1: Thông tư 60/2025/TT-BCT — bản Word trích tuyển cung cấp — Điều 12. Giá bán lẻ điện sinh hoạt | Khoản 5](https://vanban.chinhphu.vn/?docid=216125&orggroupid=4&pageid=27160); [2: Thông tư 60/2025/TT-BCT — bản Word trích tuyển cung cấp — Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp](https://vanban.chinhphu.vn/?docid=216125&orggroupid=4&pageid=27160)
- Trường hợp thuê từ 12 tháng trở lên có đăng ký cư trú thì chủ nhà trực tiếp ký hoặc đại diện sinh viên ký hợp đồng mua bán điện theo quy định có hiệu lực từ ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành [1] [2].
  [1: Thông tư 60/2025/TT-BCT — bản Word trích tuyển cung cấp — Điều 12. Giá bán lẻ điện sinh hoạt | Khoản 5](https://vanban.chinhphu.vn/?docid=216125&orggroupid=4&pageid=27160); [2: Thông tư 60/2025/TT-BCT — bản Word trích tuyển cung cấp — Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp](https://vanban.chinhphu.vn/?docid=216125&orggroupid=4&pageid=27160)
- Nếu không giao kết hợp đồng trực tiếp với bên bán điện thì tổng tiền điện chủ nhà thu không được vượt quá hóa đơn tiền điện hằng tháng do bên bán lẻ điện phát hành theo quy định có hiệu lực từ ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành [1] [2].
  [1: Thông tư 60/2025/TT-BCT — bản Word trích tuyển cung cấp — Điều 12. Giá bán lẻ điện sinh hoạt | Khoản 5](https://vanban.chinhphu.vn/?docid=216125&orggroupid=4&pageid=27160); [2: Thông tư 60/2025/TT-BCT — bản Word trích tuyển cung cấp — Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp](https://vanban.chinhphu.vn/?docid=216125&orggroupid=4&pageid=27160)
- Quy định về giá bán lẻ điện cho sinh viên thuê nhà tại điểm c khoản 5 Điều 12 Thông tư 60/2025/TT-BCT chỉ có hiệu lực thi hành kể từ ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực [1] [2].
  [1: Thông tư 60/2025/TT-BCT — bản Word trích tuyển cung cấp — Điều 12. Giá bán lẻ điện sinh hoạt | Khoản 5](https://vanban.chinhphu.vn/?docid=216125&orggroupid=4&pageid=27160); [2: Thông tư 60/2025/TT-BCT — bản Word trích tuyển cung cấp — Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp](https://vanban.chinhphu.vn/?docid=216125&orggroupid=4&pageid=27160)
- Văn bản trích dẫn là bản Word trích tuyển được cung cấp, chưa được đối chiếu toàn văn với văn bản chính thức [1].
  [1: Thông tư 60/2025/TT-BCT — bản Word trích tuyển cung cấp — Điều 12. Giá bán lẻ điện sinh hoạt | Khoản 5](https://vanban.chinhphu.vn/?docid=216125&orggroupid=4&pageid=27160)

**Đối chiếu nguyên mẫu:**

Nhãn tổng hợp: **high**; nhãn Qwen gốc: **high**. Đoạn trả lời bao phủ đầy đủ các trường hợp kê khai, tỷ lệ định mức và điều kiện hợp đồng ngắn hạn từ nguồn tham khảo.

**Rà mẫu/nguồn:** Kiểm tra không trộn cấu trúc bậc cũ với TT60 và Quyết định 14; nguồn có điều kiện hiệu lực chưa xác nhận sự kiện kích hoạt. Tỷ lệ ba phần tư và phép tính minh họa không phải xác nhận biểu giá đang dùng.

| Điểm | Trích mẫu có thật | Trích câu trả lời có thật | Giải thích |
|---|---|---|---|
| matched | Việc tính tiền điện cho 3 sinh viên ở chung phòng được áp dụng theo 2 trường hợp: | - Nếu chủ nhà kê khai đầy đủ thông tin cư trú của 03 người sử dụng điện thì được tính 3/4 định mức áp dụng giá bán lẻ điện sinh hoạt theo quy định có hiệu lực từ ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày | Việc tính tiền điện phụ thuộc vào hai trường hợp: chủ trọ kê khai đầy đủ hoặc không kê khai. |
| matched | **Chủ trọ kê khai đầy đủ thông tin cư trú với Điện lực:** | - Nếu chủ nhà kê khai đầy đủ thông tin cư trú của 03 người sử dụng điện thì được tính 3/4 định mức áp dụng giá bán lẻ điện sinh hoạt theo quy định có hiệu lực từ ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày | Khi chủ trọ kê khai đầy đủ thông tin cư trú của 03 người sử dụng điện. |
| matched | - Căn cứ quy tắc 4 người bằng 1 định mức hộ gia đình, **3 sinh viên được cấp $3/4$ (75%) định mức** của từng bậc thang điện sinh hoạt: | - Nếu chủ nhà kê khai đầy đủ thông tin cư trú của 03 người sử dụng điện thì được tính 3/4 định mức áp dụng giá bán lẻ điện sinh hoạt theo quy định có hiệu lực từ ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày | Ba sinh viên được cấp 75% định mức hộ gia đình để tính tiền theo bậc thang. |
| matched | **Chủ trọ không kê khai định mức (hợp đồng dưới 12 tháng):** | - Nếu hợp đồng thuê dưới 12 tháng và chủ nhà không kê khai đầy đủ số người thì áp dụng giá bán lẻ điện sinh hoạt bậc 2 cho toàn bộ sản lượng đo đếm theo quy định có hiệu lực từ ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần | Nếu hợp đồng dưới 12 tháng và không kê khai, toàn bộ sản lượng áp dụng giá bán lẻ điện sinh hoạt. |
| matched | **Lời khuyên:** 3 sinh viên nên cung cấp CCCD và yêu cầu chủ trọ làm thủ tục kê khai định mức với Điện lực để được hưởng giá điện bậc thang ưu đãi. | - Chủ nhà trọ đã thực hiện đăng ký tạm trú và kê khai số lượng 03 người với bên bán điện chưa? | Chủ nhà nên cung cấp CCCD và yêu cầu làm thủ tục kê khai để được hưởng giá ưu đãi. |

### Câu 25: Nếu tôi nghi tiền điện bị thu cao hơn quy định, nên kiểm tra hóa đơn và căn cứ nào?

Để kiểm tra việc tiền điện bị thu cao hơn quy định, người thuê cần căn cứ vào hóa đơn tiền điện hằng tháng do bên bán lẻ điện phát hành và các quy định về định mức, giá bán lẻ điện sinh hoạt áp dụng cho đối tượng thuê trọ [1].

- Khuyến nghị kiểm tra hóa đơn tiền điện hằng tháng của đơn vị bán lẻ điện để đối chiếu nguyên tắc tổng số tiền chủ nhà thu của người thuê không được vượt quá số tiền ghi trên hóa đơn nếu không ký hợp đồng trực tiếp [1].
- Đối chiếu điều kiện hợp đồng thuê từ 12 tháng trở lên kèm đăng ký tạm trú hoặc thường trú để xem xét quyền trực tiếp hoặc đại diện ký hợp đồng mua bán điện [1].
- Đối chiếu quy định trường hợp thuê dưới 12 tháng không kê khai đủ số người thì áp dụng giá bán lẻ điện sinh hoạt bậc 2 cho toàn bộ sản lượng đo đếm tại công tơ [1].
- Kiểm tra việc kê khai số người cư trú để xác định việc cấp định mức sinh hoạt với tỷ lệ cứ 4 người tính là một hộ sử dụng điện [1].

Quy định về giá bán lẻ điện sinh hoạt cho sinh viên và người lao động thuê nhà tại điểm c khoản 5 Điều 12 chỉ có hiệu lực thi hành kể từ ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành [1] [2].
Nguồn cung cấp là bản trích tuyển nên chưa đủ căn cứ xác minh hiệu lực thực tế của văn bản và các biểu giá tiền điện cụ thể [1] [2].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng.
Nguồn có hiệu lực có điều kiện; chưa xác nhận văn bản/sự kiện kích hoạt.
Nguồn là bản Word/trích tuyển được cung cấp, chưa xác minh toàn bộ câu chữ với bản chính thức; không coi ghi chú biên tập là quy định pháp luật.

Để áp dụng vào trường hợp của bạn:
- Hợp đồng thuê phòng của bạn có thời hạn từ 12 tháng trở lên và đã đăng ký tạm trú chưa?
- Chủ nhà trọ hiện có thực hiện kê khai số người cư trú thực tế để tính định mức điện không?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

**Nguồn của từng dòng có trích dẫn:**

- Để kiểm tra việc tiền điện bị thu cao hơn quy định, người thuê cần căn cứ vào hóa đơn tiền điện hằng tháng do bên bán lẻ điện phát hành và các quy định về định mức, giá bán lẻ điện sinh hoạt áp dụng cho đối tượng thuê trọ [1].
  [1: Thông tư 60/2025/TT-BCT — bản Word trích tuyển cung cấp — Điều 12. Giá bán lẻ điện sinh hoạt | Khoản 5](https://vanban.chinhphu.vn/?docid=216125&orggroupid=4&pageid=27160)
- Khuyến nghị kiểm tra hóa đơn tiền điện hằng tháng của đơn vị bán lẻ điện để đối chiếu nguyên tắc tổng số tiền chủ nhà thu của người thuê không được vượt quá số tiền ghi trên hóa đơn nếu không ký hợp đồng trực tiếp [1].
  [1: Thông tư 60/2025/TT-BCT — bản Word trích tuyển cung cấp — Điều 12. Giá bán lẻ điện sinh hoạt | Khoản 5](https://vanban.chinhphu.vn/?docid=216125&orggroupid=4&pageid=27160)
- Đối chiếu điều kiện hợp đồng thuê từ 12 tháng trở lên kèm đăng ký tạm trú hoặc thường trú để xem xét quyền trực tiếp hoặc đại diện ký hợp đồng mua bán điện [1].
  [1: Thông tư 60/2025/TT-BCT — bản Word trích tuyển cung cấp — Điều 12. Giá bán lẻ điện sinh hoạt | Khoản 5](https://vanban.chinhphu.vn/?docid=216125&orggroupid=4&pageid=27160)
- Đối chiếu quy định trường hợp thuê dưới 12 tháng không kê khai đủ số người thì áp dụng giá bán lẻ điện sinh hoạt bậc 2 cho toàn bộ sản lượng đo đếm tại công tơ [1].
  [1: Thông tư 60/2025/TT-BCT — bản Word trích tuyển cung cấp — Điều 12. Giá bán lẻ điện sinh hoạt | Khoản 5](https://vanban.chinhphu.vn/?docid=216125&orggroupid=4&pageid=27160)
- Kiểm tra việc kê khai số người cư trú để xác định việc cấp định mức sinh hoạt với tỷ lệ cứ 4 người tính là một hộ sử dụng điện [1].
  [1: Thông tư 60/2025/TT-BCT — bản Word trích tuyển cung cấp — Điều 12. Giá bán lẻ điện sinh hoạt | Khoản 5](https://vanban.chinhphu.vn/?docid=216125&orggroupid=4&pageid=27160)
- Quy định về giá bán lẻ điện sinh hoạt cho sinh viên và người lao động thuê nhà tại điểm c khoản 5 Điều 12 chỉ có hiệu lực thi hành kể từ ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành [1] [2].
  [1: Thông tư 60/2025/TT-BCT — bản Word trích tuyển cung cấp — Điều 12. Giá bán lẻ điện sinh hoạt | Khoản 5](https://vanban.chinhphu.vn/?docid=216125&orggroupid=4&pageid=27160); [2: Thông tư 60/2025/TT-BCT — bản Word trích tuyển cung cấp — Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp](https://vanban.chinhphu.vn/?docid=216125&orggroupid=4&pageid=27160)
- Nguồn cung cấp là bản trích tuyển nên chưa đủ căn cứ xác minh hiệu lực thực tế của văn bản và các biểu giá tiền điện cụ thể [1] [2].
  [1: Thông tư 60/2025/TT-BCT — bản Word trích tuyển cung cấp — Điều 12. Giá bán lẻ điện sinh hoạt | Khoản 5](https://vanban.chinhphu.vn/?docid=216125&orggroupid=4&pageid=27160); [2: Thông tư 60/2025/TT-BCT — bản Word trích tuyển cung cấp — Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp](https://vanban.chinhphu.vn/?docid=216125&orggroupid=4&pageid=27160)

**Đối chiếu nguyên mẫu:**

Nhãn tổng hợp: **partial**; nhãn Qwen gốc: **high**. Đáp án bao phủ các bước kiểm tra hóa đơn, căn cứ pháp lý phạt và hoàn trả, tuy nhiên thiếu thông tin về kênh tiếp nhận phản ánh cụ thể và số tiền phạt chi tiết.

**Rà mẫu/nguồn:** Cần cập nhật căn cứ xử phạt, cơ quan và địa bàn hiện tại; không biến con số phạt theo nghị định cũ thành mức hiện hành nếu chưa xác minh. Phân biệt người thuê có thể yêu cầu đối chiếu với quyền truy cập tài khoản người khác.

| Điểm | Trích mẫu có thật | Trích câu trả lời có thật | Giải thích |
|---|---|---|---|
| matched | **Chốt công tơ phòng:** Ghi lại chỉ số điện đầu kỳ và cuối kỳ trên công tơ riêng của phòng mình để xác định chính xác số kWh đã dùng. | Để kiểm tra việc tiền điện bị thu cao hơn quy định, người thuê cần căn cứ vào hóa đơn tiền điện hằng tháng do bên bán lẻ điện phát hành và các quy định về định mức, giá bán lẻ điện sinh hoạt áp dụng cho đối tượng thuê trọ [1]. | Ghi lại chỉ số điện đầu kỳ và cuối kỳ trên công tơ riêng của phòng để xác định chính xác số kWh đã dùng. |
| matched | **Yêu cầu đối chiếu hóa đơn gốc:** Đề nghị chủ trọ cung cấp hóa đơn tiền điện hằng tháng do Điện lực phát hành (hoặc lấy Mã khách hàng "PK..."/"PE..." để tra cứu trên App EVNSPC CSKH). | - Khuyến nghị kiểm tra hóa đơn tiền điện hằng tháng của đơn vị bán lẻ điện để đối chiếu nguyên tắc tổng số tiền chủ nhà thu của người thuê không được vượt quá số tiền ghi trên hóa đơn nếu không ký hợp đồng trực tiếp [1]. | Đề nghị chủ trọ cung cấp hóa đơn tiền điện hằng tháng do Điện lực phát hành hoặc tra cứu trên App EVNSPC CSKH. |
| different | **Căn cứ pháp lý xử phạt:** Căn cứ Khoản 6 Điều 12 Nghị định 134/2013/NĐ-CP (sửa đổi bởi Nghị định 17/2022/NĐ-CP), hành vi thu tiền điện của người thuê nhà cao hơn giá quy định bị **phạt tiền từ 20.000.000 đồng đến 30.000.000 đồng**, đồng | Để kiểm tra việc tiền điện bị thu cao hơn quy định, người thuê cần căn cứ vào hóa đơn tiền điện hằng tháng do bên bán lẻ điện phát hành và các quy định về định mức, giá bán lẻ điện sinh hoạt áp dụng cho đối tượng thuê trọ [1]. | Hành vi thu tiền điện cao hơn quy định bị phạt tiền từ 20.000.000 đồng đến 30.000.000 đồng. |
| missing | thời buộc hoàn trả lại toàn bộ số tiền đã thu chênh lệch. |  | Thời buộc hoàn trả lại toàn bộ số tiền đã thu chênh lệch. |
| different | **Kênh tiếp nhận phản ánh:** | Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực. | Tổng đài Chăm sóc khách hàng Tổng công ty Điện lực Miền Nam (EVNSPC): 1900 1006 hoặc 1900 9000. |
| matched | - UBND hoặc Đội Quản lý thị trường phường/xã nơi đặt phòng trọ. | Quy định về giá bán lẻ điện sinh hoạt cho sinh viên và người lao động thuê nhà tại điểm c khoản 5 Điều 12 chỉ có hiệu lực thi hành kể từ ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg | Chưa xác nhận văn bản/sự kiện kích hoạt hiệu lực thực tế của quy định giá tiền điện cụ thể. |

### Câu 26: Chủ trọ có phải thông báo cách tính tiền điện và số điện đã sử dụng không?

Chưa đủ căn cứ từ nguồn để khẳng định quy định pháp luật bắt buộc chủ trọ phải thông báo riêng từng lần về cách tính và chỉ số, nhưng nguồn ghi nhận yêu cầu công khai cách tính và bảo đảm điều kiện kiểm tra chỉ số đo [2] [4].

- Vị trí lắp đặt công tơ đo đếm điện phải bảo đảm an toàn, mỹ quan và thuận lợi cho bên mua điện kiểm tra chỉ số đo điện năng [4].
- Chủ trọ thực hiện công khai cách tính và thu tiền điện theo đúng hóa đơn do Điện lực phát hành [2].
- Khi người thuê không ký hợp đồng trực tiếp với bên bán điện, điểm c khoản 5 Điều 12 quy định tổng tiền điện chủ nhà thu không được vượt quá tiền điện trong hóa đơn hằng tháng, có hiệu lực từ ngày điều chỉnh giá bán lẻ điện bình quân gần nhất sau ngày Quyết định 14/2025/QĐ-TTg có hiệu lực [1] [5].
- Khuyến nghị người thuê đối chiếu chỉ số công tơ với hóa đơn tiền điện do Điện lực phát hành để kiểm tra số tiền phải nộp [1] [2] [4].

Nguồn hướng dẫn của Điện lực Cần Thơ về công khai cách tính không phải là điều luật quy định một mẫu bảng kê chi tiết bắt buộc [2].
Điểm c khoản 5 Điều 12 Thông tư 60/2025/TT-BCT có hiệu lực theo điều kiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định 14/2025/QĐ-TTg có hiệu lực [1] [5].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng.
Nguồn có hiệu lực có điều kiện; chưa xác nhận văn bản/sự kiện kích hoạt.
Nguồn là bản Word/trích tuyển được cung cấp, chưa xác minh toàn bộ câu chữ với bản chính thức; không coi ghi chú biên tập là quy định pháp luật.
Hướng dẫn kiểm tra nhà trọ Cần Thơ đăng ngày 21/09/2026; không phải điều luật hoặc quy định một mẫu bảng kê bắt buộc. Trích đoạn ngắn về công khai cách tính và hóa đơn; không tự suy ra mọi chi tiết kê khai.

Để áp dụng vào trường hợp của bạn:
- Bạn có đang trực tiếp kiểm tra được công tơ điện tại phòng trọ không?
- Chủ trọ hiện đang thu tiền điện theo công tơ riêng từng phòng hay chia chung trên hóa đơn Điện lực?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

**Nguồn của từng dòng có trích dẫn:**

- Chưa đủ căn cứ từ nguồn để khẳng định quy định pháp luật bắt buộc chủ trọ phải thông báo riêng từng lần về cách tính và chỉ số, nhưng nguồn ghi nhận yêu cầu công khai cách tính và bảo đảm điều kiện kiểm tra chỉ số đo [2] [4].
  [2: Công khai cách tính tiền điện nhà trọ — PC TP Cần Thơ / EVNSPC — Công khai cách tính tiền điện nhà trọ — PC TP Cần Thơ / EVNSPC](https://cskh.evnspc.vn/TinTuc/TinTucChiTiet?LoaiTinBai=ALL&MaTinBai=3103); [4: Luật Điện lực 61/2024/QH15 — bản Word cung cấp — Điều 56. Đo đếm điện | Khoản 3](https://vanban.chinhphu.vn/?docid=212489&pageid=27160)
- Vị trí lắp đặt công tơ đo đếm điện phải bảo đảm an toàn, mỹ quan và thuận lợi cho bên mua điện kiểm tra chỉ số đo điện năng [4].
  [4: Luật Điện lực 61/2024/QH15 — bản Word cung cấp — Điều 56. Đo đếm điện | Khoản 3](https://vanban.chinhphu.vn/?docid=212489&pageid=27160)
- Chủ trọ thực hiện công khai cách tính và thu tiền điện theo đúng hóa đơn do Điện lực phát hành [2].
  [2: Công khai cách tính tiền điện nhà trọ — PC TP Cần Thơ / EVNSPC — Công khai cách tính tiền điện nhà trọ — PC TP Cần Thơ / EVNSPC](https://cskh.evnspc.vn/TinTuc/TinTucChiTiet?LoaiTinBai=ALL&MaTinBai=3103)
- Khi người thuê không ký hợp đồng trực tiếp với bên bán điện, điểm c khoản 5 Điều 12 quy định tổng tiền điện chủ nhà thu không được vượt quá tiền điện trong hóa đơn hằng tháng, có hiệu lực từ ngày điều chỉnh giá bán lẻ điện bình quân gần nhất sau ngày Quyết định 14/2025/QĐ-TTg có hiệu lực [1] [5].
  [1: Thông tư 60/2025/TT-BCT — bản Word trích tuyển cung cấp — Điều 12. Giá bán lẻ điện sinh hoạt | Khoản 5](https://vanban.chinhphu.vn/?docid=216125&orggroupid=4&pageid=27160); [5: Thông tư 60/2025/TT-BCT — bản Word trích tuyển cung cấp — Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp](https://vanban.chinhphu.vn/?docid=216125&orggroupid=4&pageid=27160)
- Khuyến nghị người thuê đối chiếu chỉ số công tơ với hóa đơn tiền điện do Điện lực phát hành để kiểm tra số tiền phải nộp [1] [2] [4].
  [1: Thông tư 60/2025/TT-BCT — bản Word trích tuyển cung cấp — Điều 12. Giá bán lẻ điện sinh hoạt | Khoản 5](https://vanban.chinhphu.vn/?docid=216125&orggroupid=4&pageid=27160); [2: Công khai cách tính tiền điện nhà trọ — PC TP Cần Thơ / EVNSPC — Công khai cách tính tiền điện nhà trọ — PC TP Cần Thơ / EVNSPC](https://cskh.evnspc.vn/TinTuc/TinTucChiTiet?LoaiTinBai=ALL&MaTinBai=3103); [4: Luật Điện lực 61/2024/QH15 — bản Word cung cấp — Điều 56. Đo đếm điện | Khoản 3](https://vanban.chinhphu.vn/?docid=212489&pageid=27160)
- Nguồn hướng dẫn của Điện lực Cần Thơ về công khai cách tính không phải là điều luật quy định một mẫu bảng kê chi tiết bắt buộc [2].
  [2: Công khai cách tính tiền điện nhà trọ — PC TP Cần Thơ / EVNSPC — Công khai cách tính tiền điện nhà trọ — PC TP Cần Thơ / EVNSPC](https://cskh.evnspc.vn/TinTuc/TinTucChiTiet?LoaiTinBai=ALL&MaTinBai=3103)
- Điểm c khoản 5 Điều 12 Thông tư 60/2025/TT-BCT có hiệu lực theo điều kiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định 14/2025/QĐ-TTg có hiệu lực [1] [5].
  [1: Thông tư 60/2025/TT-BCT — bản Word trích tuyển cung cấp — Điều 12. Giá bán lẻ điện sinh hoạt | Khoản 5](https://vanban.chinhphu.vn/?docid=216125&orggroupid=4&pageid=27160); [5: Thông tư 60/2025/TT-BCT — bản Word trích tuyển cung cấp — Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp](https://vanban.chinhphu.vn/?docid=216125&orggroupid=4&pageid=27160)

**Đối chiếu nguyên mẫu:**

Nhãn tổng hợp: **partial**; nhãn Qwen gốc: **high**. Đoạn trả lời phủ nhận bắt buộc thông báo riêng từng lần nhưng thừa nhận yêu cầu công khai cách tính và bảo đảm kiểm tra chỉ số, đồng thời ghi nhận các điều kiện hiệu lực và nguồn gốc văn bản khác biệt so với quy định pháp luật chung.

**Rà mẫu/nguồn:** Nguồn EVNSPC Cần Thơ hướng dẫn công khai cách tính theo hóa đơn; chưa chứng minh mọi chủ trọ bị luật buộc lập bảng kê đủ bốn trường hoặc cho người thuê cùng chốt công tơ. Tách quyền thông tin trong giao dịch kinh doanh và khuyến nghị đối chiếu.

| Điểm | Trích mẫu có thật | Trích câu trả lời có thật | Giải thích |
|---|---|---|---|
| matched | **Có, chủ trọ có nghĩa vụ minh bạch số liệu đo đếm và cách tính tiền điện.** | Chưa đủ căn cứ từ nguồn để khẳng định quy định pháp luật bắt buộc chủ trọ phải thông báo riêng từng lần về cách tính và chỉ số, nhưng nguồn ghi nhận yêu cầu công khai cách tính và bảo đảm điều kiện kiểm tra chỉ số đo [2] [4]. | Có, chủ trọ có nghĩa vụ minh bạch số liệu đo đếm và cách tính tiền điện. |
| matched | - **Nguyên tắc:** Tổng số tiền điện thu từ người thuê không được vượt quá số tiền trên hóa đơn thực tế của Điện lực. | - Chủ trọ thực hiện công khai cách tính và thu tiền điện theo đúng hóa đơn do Điện lực phát hành [2]. | Tổng số tiền điện thu từ người thuê không được vượt quá số tiền trên hóa đơn thực tế của Điện lực. |
| matched | Do đó, chủ nhà phải công khai dữ liệu đo đếm để làm cơ sở thu tiền. | Chưa đủ căn cứ từ nguồn để khẳng định quy định pháp luật bắt buộc chủ trọ phải thông báo riêng từng lần về cách tính và chỉ số, nhưng nguồn ghi nhận yêu cầu công khai cách tính và bảo đảm điều kiện kiểm tra chỉ số đo [2] [4]. | Chủ nhà phải công khai dữ liệu đo đếm để làm cơ sở thu tiền. |
| different | - **Bảng kê tiền điện hàng tháng phải thể hiện rõ:** | Chưa đủ căn cứ từ nguồn để khẳng định quy định pháp luật bắt buộc chủ trọ phải thông báo riêng từng lần về cách tính và chỉ số, nhưng nguồn ghi nhận yêu cầu công khai cách tính và bảo đảm điều kiện kiểm tra chỉ số đo [2] [4]. | Bảng kê tiền điện hàng tháng phải thể hiện rõ các chỉ số và thành tiền. |
| matched | - Người thuê có quyền cùng chủ trọ đối chiếu trực tiếp mặt số công tơ vào ngày chốt điện định kỳ. | Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng. | Chưa đủ căn cứ để kết luận toàn bộ yêu cầu hoặc tình huống riêng từ đoạn này. |

### Câu 27: Giá nước sinh hoạt áp dụng cho phòng trọ ở Cần Thơ được xác định theo căn cứ nào?

Các đoạn trả lời trực tiếp trong nguồn:

- Giá nước Cần Thơ 215/QĐ-UBND — bản Word cung cấp — Điều 1. Quy định giá nước sạch sinh hoạt tại đô thị và khu vực nông thôn áp dụng đối với các đơn vị kinh doanh nước sạch, các tổ chức và khách hàng sử dụng nước sạch trên địa bàn thành phố Cần Thơ như sau: | Khoản 2: “2. Giá nước sạch sinh hoạt tại đô thị, khu vực nông thôn do Trung tâm Nước sạch và Vệ sinh môi trường nông thôn cung cấp cho mục đích sinh hoạt:

STT

Nhóm khách hàng sử dụng nước sạch cho mục đích sinh hoạt

Giá tiêu thụ nước sạch (đồng/m3)

Nhóm 1

Hộ dân cư là hộ nghèo có sổ, hộ gia đình chính sách (gia đình Mẹ Việt Nam anh hùng, gia đình thương binh, gia đình liệt sĩ), hộ hiến đất.

4.000

Nhóm 2

Hộ dân cư và các nhóm đối tượng khác

7.450

(Giá đã bao gồm thuế giá trị gia tăng, chưa bao gồm phí bảo vệ môi trường đối với nước thải sinh hoạt)” [1].

- Giá nước Cần Thơ 215/QĐ-UBND — bản Word cung cấp — Điều 1. Quy định giá nước sạch sinh hoạt tại đô thị và khu vực nông thôn áp dụng đối với các đơn vị kinh doanh nước sạch, các tổ chức và khách hàng sử dụng nước sạch trên địa bàn thành phố Cần Thơ như sau: | Khoản 1: “1. Giá nước sạch sinh hoạt tại đô thị, khu vực nông thôn năm 2024 do các đơn vị cấp nước cung cấp:

STT

Nhóm khách hàng sử dụng nước sạch cho mục đích sinh hoạt

Giá tiêu thụ nước sạch (đồng/m3)

1

Khu vực đô thị

Nhóm 1

Hộ dân cư là Hộ nghèo có sổ

5.640

Hộ dân cư

9.020

Nhóm 2

Cơ quan hành chính; đơn vị sự nghiệp công lập; trường học, bệnh viện, cơ sở khám, chữa bệnh (công lập và tư nhân); phục vụ mục đích công cộng (phi lợi nhuận).

11.170

Nhóm 3

Tổ chức, cá nhân sản xuất vật chất

12.400

Nhóm 4

Tổ chức, cá nhân kinh doanh, dịch vụ

15.580

2

Khu vực nông thôn

Nhóm 1

Hộ dân cư là hộ nghèo có sổ

4.820

Hộ dân cư

8.240

Nhóm 2

Cơ quan hành chính; đơn vị sự nghiệp công lập; trường học, bệnh viện, cơ sở khám, chữa bệnh (công lập và tư nhân); phục vụ mục đích công cộng (phi lợi nhuận).

9.310

Nhóm 3

Tổ chức, cá nhân sản xuất vật chất

9.930

Nhóm 4

Tổ chức, cá nhân kinh doanh, dịch vụ

11.520

(Giá đã bao gồm thuế giá trị gia tăng, chưa bao gồm phí bảo vệ môi trường đối với nước thải sinh hoạt)” [2].

- Giá nước Cần Thơ 215/QĐ-UBND — bản Word cung cấp — Điều 2. Điều chỉnh giá nước sạch | Khoản 2: “2. Hàng năm, các đơn vị cấp nước chủ động rà soát việc thực hiện phương án giá nước sạch và giá nước sạch dự kiến cho năm tiếp theo trên cơ sở quy định tại Điều 4 Thông tư số 44/2021/TT-BTC ngày 18 tháng 6 năm 2021 của Bộ trưởng Bộ Tài chính quy định về khung giá, nguyên tắc, phương pháp xác định giá nước sạch sinh hoạt để thực hiện, đảm bảo tuân thủ đúng quy định.” [3].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng; cần đối chiếu phần còn thiếu.

Nguồn giá nước năm 2024: cần xác nhận địa bàn, đơn vị cấp nước và hiệu lực tại thời điểm áp dụng; bảng tiền chưa được dùng để kết luận mức thu.

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng, hiệu lực và bản gốc.

Nguồn là bản Word/trích tuyển được cung cấp, chưa xác minh toàn bộ câu chữ với bản chính thức; không coi ghi chú biên tập là quy định pháp luật.

**Nguồn của từng dòng có trích dẫn:**

- (Giá đã bao gồm thuế giá trị gia tăng, chưa bao gồm phí bảo vệ môi trường đối với nước thải sinh hoạt)” [1].
  [1: Giá nước Cần Thơ 215/QĐ-UBND — bản Word cung cấp — Điều 1. Quy định giá nước sạch sinh hoạt tại đô thị và khu vực nông thôn áp dụng đối với các đơn vị kinh doanh nước sạch, các tổ chức và khách hàng sử dụng nước sạch trên địa bàn thành phố Cần Thơ như sau: | Khoản 2](https://capnuoccantho2.com.vn/View.aspx?wc=63&wp=332)
- (Giá đã bao gồm thuế giá trị gia tăng, chưa bao gồm phí bảo vệ môi trường đối với nước thải sinh hoạt)” [2].
  [2: Giá nước Cần Thơ 215/QĐ-UBND — bản Word cung cấp — Điều 1. Quy định giá nước sạch sinh hoạt tại đô thị và khu vực nông thôn áp dụng đối với các đơn vị kinh doanh nước sạch, các tổ chức và khách hàng sử dụng nước sạch trên địa bàn thành phố Cần Thơ như sau: | Khoản 1](https://capnuoccantho2.com.vn/View.aspx?wc=63&wp=332)
- Giá nước Cần Thơ 215/QĐ-UBND — bản Word cung cấp — Điều 2. Điều chỉnh giá nước sạch | Khoản 2: “2. Hàng năm, các đơn vị cấp nước chủ động rà soát việc thực hiện phương án giá nước sạch và giá nước sạch dự kiến cho năm tiếp theo trên cơ sở quy định tại Điều 4 Thông tư số 44/2021/TT-BTC ngày 18 tháng 6 năm 2021 của Bộ trưởng Bộ Tài chính quy định về khung giá, nguyên tắc, phương pháp xác định giá nước sạch sinh hoạt để thực hiện, đảm bảo tuân thủ đúng quy định.” [3].
  [3: Giá nước Cần Thơ 215/QĐ-UBND — bản Word cung cấp — Điều 2. Điều chỉnh giá nước sạch | Khoản 2](https://capnuoccantho2.com.vn/View.aspx?wc=63&wp=332)

**Lý do dùng đoạn nguồn:** Không thể kết luận pháp luật không có quy định từ các đoạn truy xuất.; Bản tổng hợp chưa được nguồn xác nhận sau lần sửa; dùng trích đoạn Qwen đã chọn.; Phản hồi chưa đáp ứng đầy đủ yêu cầu chính; đánh dấu theo nội dung thay vì provider.

**Đối chiếu nguyên mẫu:**

Nhãn tổng hợp: **unscored**; nhãn Qwen gốc: **unscored**. Chưa chấm được; không tạo điểm thay thế.

**Rà mẫu/nguồn:** Cần xác minh phạm vi Cần Thơ sau sắp xếp, nhà cung cấp và biểu giá hiện hành. Mức 4 m3/người/tháng và phần trăm phụ phí không được dùng làm mức chung nếu thiếu nguồn.

**Lỗi kiểm tra bộ chấm:** points[2]: matched numeric point lacks corresponding answer quantities and units

### Câu 28: Tôi nên kiểm tra gì khi chủ trọ thu tiền nước theo đầu người thay vì đồng hồ?

Chưa đủ căn cứ pháp lý quy định bắt buộc cách chia tiền nước giữa người thuê, do đó việc thu tiền nước theo đầu người phụ thuộc vào thỏa thuận hợp đồng về giá và phương thức thanh toán [3].

- Khuyến nghị kiểm tra thỏa thuận cụ thể trong hợp đồng thuê về tiền nước, số người thuê cùng các chi phí phát sinh khác trước khi đặt cọc hoặc ký kết [2] [3].
- Khuyến nghị làm rõ phương thức thanh toán và mức giá khoán áp dụng cho mỗi đầu người để bảo đảm nội dung hợp đồng được các bên tự nguyện thống nhất [3] [5].
- Khuyến nghị kiểm tra tình trạng hệ thống đường nước trong phòng trước khi đến ở để kịp thời yêu cầu sửa chữa nếu có hư hỏng [2].
- Thống nhất rõ mức chi trả nước ngay khi ký hợp đồng nhằm tránh việc bị yêu cầu trả thêm các khoản chi phí khác chưa thỏa thuận ban đầu [2].

Biểu giá nước sinh hoạt địa phương dành cho đơn vị kinh doanh cấp nước và khách hàng sử dụng nước, không phải quy định bắt buộc về cách chia tiền giữa những người thuê trọ [4].
Nguồn từ nền tảng hỗ trợ chỉ mang tính chất hướng dẫn, khuyến cáo kinh nghiệm giao dịch thuê phòng mà không phải điều luật bắt buộc [2].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng.
Nguồn giá nước năm 2024: cần xác nhận địa bàn, đơn vị cấp nước và hiệu lực tại thời điểm áp dụng; bảng tiền chưa được dùng để kết luận mức thu.
Hướng dẫn/khuyến cáo của Trợ Giúp Chợ Tốt; không phải điều luật. Mẹo giao dịch, không phải điều luật. Không chứng minh hạn hoàn cọc cố định hoặc mức cọc bắt buộc; không thay thế xác minh người được ủy quyền cho thuê. Chỉ đọc phần kiểm tra, không bổ sung mẫu soạn hợp đồng.
Nguồn là bản Word/trích tuyển được cung cấp, chưa xác minh toàn bộ câu chữ với bản chính thức; không coi ghi chú biên tập là quy định pháp luật.

Để áp dụng vào trường hợp của bạn:
- Hợp đồng thuê phòng của bạn đã có điều khoản cụ thể nào về mức thu và phương thức tính tiền nước chưa?
- Nhà trọ của bạn thuộc tỉnh, thành phố nào để đối chiếu thêm biểu giá nước sinh hoạt địa phương nếu cần?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

**Nguồn của từng dòng có trích dẫn:**

- Chưa đủ căn cứ pháp lý quy định bắt buộc cách chia tiền nước giữa người thuê, do đó việc thu tiền nước theo đầu người phụ thuộc vào thỏa thuận hợp đồng về giá và phương thức thanh toán [3].
  [3: Bộ luật Dân sự 91/2015/QH13 — Word do cơ quan nhà nước công bố — Điều 398. Nội dung của hợp đồng | Khoản 2](https://congan.daklak.gov.vn/laws/detail/Bo-luat-Dan-su-163/)
- Khuyến nghị kiểm tra thỏa thuận cụ thể trong hợp đồng thuê về tiền nước, số người thuê cùng các chi phí phát sinh khác trước khi đặt cọc hoặc ký kết [2] [3].
  [2: Mẹo khi thuê phòng — Trợ Giúp Chợ Tốt — Mẹo khi thuê phòng | Đoạn nguyên văn 78](https://trogiup.chotot.com/nguoi-mua/meo-khi-thue-phong/); [3: Bộ luật Dân sự 91/2015/QH13 — Word do cơ quan nhà nước công bố — Điều 398. Nội dung của hợp đồng | Khoản 2](https://congan.daklak.gov.vn/laws/detail/Bo-luat-Dan-su-163/)
- Khuyến nghị làm rõ phương thức thanh toán và mức giá khoán áp dụng cho mỗi đầu người để bảo đảm nội dung hợp đồng được các bên tự nguyện thống nhất [3] [5].
  [3: Bộ luật Dân sự 91/2015/QH13 — Word do cơ quan nhà nước công bố — Điều 398. Nội dung của hợp đồng | Khoản 2](https://congan.daklak.gov.vn/laws/detail/Bo-luat-Dan-su-163/); [5: Bộ luật Dân sự 91/2015/QH13 — Word do cơ quan nhà nước công bố — Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp](https://congan.daklak.gov.vn/laws/detail/Bo-luat-Dan-su-163/)
- Khuyến nghị kiểm tra tình trạng hệ thống đường nước trong phòng trước khi đến ở để kịp thời yêu cầu sửa chữa nếu có hư hỏng [2].
  [2: Mẹo khi thuê phòng — Trợ Giúp Chợ Tốt — Mẹo khi thuê phòng | Đoạn nguyên văn 78](https://trogiup.chotot.com/nguoi-mua/meo-khi-thue-phong/)
- Thống nhất rõ mức chi trả nước ngay khi ký hợp đồng nhằm tránh việc bị yêu cầu trả thêm các khoản chi phí khác chưa thỏa thuận ban đầu [2].
  [2: Mẹo khi thuê phòng — Trợ Giúp Chợ Tốt — Mẹo khi thuê phòng | Đoạn nguyên văn 78](https://trogiup.chotot.com/nguoi-mua/meo-khi-thue-phong/)
- Biểu giá nước sinh hoạt địa phương dành cho đơn vị kinh doanh cấp nước và khách hàng sử dụng nước, không phải quy định bắt buộc về cách chia tiền giữa những người thuê trọ [4].
  [4: Giá nước Cần Thơ 215/QĐ-UBND — bản Word cung cấp — Điều 1. Quy định giá nước sạch sinh hoạt tại đô thị và khu vực nông thôn áp dụng đối với các đơn vị kinh doanh nước sạch, các tổ chức và khách hàng sử dụng nước sạch trên địa bàn thành phố Cần Thơ như sau: | Khoản 1](https://capnuoccantho2.com.vn/View.aspx?wc=63&wp=332)
- Nguồn từ nền tảng hỗ trợ chỉ mang tính chất hướng dẫn, khuyến cáo kinh nghiệm giao dịch thuê phòng mà không phải điều luật bắt buộc [2].
  [2: Mẹo khi thuê phòng — Trợ Giúp Chợ Tốt — Mẹo khi thuê phòng | Đoạn nguyên văn 78](https://trogiup.chotot.com/nguoi-mua/meo-khi-thue-phong/)

**Đối chiếu nguyên mẫu:**

Nhãn tổng hợp: **partial**; nhãn Qwen gốc: **partial**. ANSWER thiếu các con số cụ thể về mức giá và quy trình giải trình khi giá cao như REFERENCE, dẫn đến sự khác biệt đáng kể trong nội dung.

**Rà mẫu/nguồn:** Chưa có khảo sát có phương pháp xác nhận 30–50 nghìn/người là mức phổ biến hoặc 3–5 m3 là tiêu thụ thực tế. Khoán, hóa đơn, số người và điều kiện đổi mức thu là nội dung kiểm tra/thỏa thuận; không tạo ngưỡng đắt trái luật.

| Điểm | Trích mẫu có thật | Trích câu trả lời có thật | Giải thích |
|---|---|---|---|
| different | Khi chủ trọ thu tiền nước khoán theo đầu người, bạn cần kiểm tra 3 nội dung: | - Khuyến nghị kiểm tra thỏa thuận cụ thể trong hợp đồng thuê về tiền nước, số người thuê cùng các chi phí phát sinh khác trước khi đặt cọc hoặc ký kết [2] [3]. | REFERENCE nêu rõ cần kiểm tra 3 nội dung cụ thể trong khi ANSWER chỉ đề cập đến thỏa thuận hợp đồng và thiếu các điểm về mức giá mặt bằng và |
| different | **Mức giá khoán mặt bằng chung:** Tại Cần Thơ, mức thu khoán tiền nước phổ biến đối với sinh viên dao động từ **30.000 – 50.000 VNĐ/người/tháng** (tương đương khối lượng tiêu thụ thực tế khoảng 3 – 5 m³/người). | - Khuyến nghị kiểm tra thỏa thuận cụ thể trong hợp đồng thuê về tiền nước, số người thuê cùng các chi phí phát sinh khác trước khi đặt cọc hoặc ký kết [2] [3]. | REFERENCE cung cấp con số mức giá khoán phổ biến tại Cần Thơ (30.000 – 50.000 VNĐ) mà ANSWER không đề cập đến bất kỳ giá trị cụ thể nào, |
| different | **Yêu cầu giải trình khi mức khoán quá cao:** Nếu chủ trọ thu từ 70.000 – 100.000 VNĐ/người/tháng, sinh viên có quyền yêu cầu chủ nhà cho xem hóa đơn tiền nước thực tế của đơn vị cấp nước, sau đó lấy tổng tiền chia đều cho tổng số người | - Khuyến nghị kiểm tra thỏa thuận cụ thể trong hợp đồng thuê về tiền nước, số người thuê cùng các chi phí phát sinh khác trước khi đặt cọc hoặc ký kết [2] [3]. | REFERENCE yêu cầu giải trình khi mức khoán quá cao (70.000 – 100.000 VNĐ) nhưng ANSWER không nhắc đến ngưỡng giá này hay quyền yêu cầu xem, |
| different | đang ở để đối chiếu. | - Khuyến nghị làm rõ phương thức thanh toán và mức giá khoán áp dụng cho mỗi đầu người để bảo đảm nội dung hợp đồng được các bên tự nguyện thống nhất [3] [5]. | REFERENCE hướng dẫn chia đều tiền nước dựa trên hóa đơn thực tế mà ANSWER chỉ nói chung về thỏa thuận thanh toán và mức giá, |
| matched | **Thỏa thuận bằng văn bản:** Mức khoán cố định phải được ghi rõ trong hợp đồng thuê phòng, cam kết không tự ý nâng giá đột xuất vào mùa khô hoặc khi có người ở thêm ngắn hạn. | - Thống nhất rõ mức chi trả nước ngay khi ký hợp đồng nhằm tránh việc bị yêu cầu trả thêm các khoản chi phí khác chưa thỏa thuận ban đầu [2]. | REFERENCE nhấn mạnh việc ghi rõ mức khoán cố định trong hợp đồng để tránh nâng giá đột xuất, điều này được ANSWER đề cập một phần, |

### Câu 29: Nếu nhà trọ dùng chung đồng hồ nước, cách phân chia chi phí nên được thỏa thuận ra sao?

Các bên có quyền tự do thỏa thuận nội dung hợp đồng về tiền nước nhưng phải đảm bảo tự nguyện và không vi phạm điều cấm của luật [3] [5].

- Khuyến nghị chủ động hỏi kỹ và thống nhất rõ ràng về giá nước cùng các chi phí phát sinh khác trước khi đặt cọc [2].
- Ghi cụ thể cách tính tiền nước, số người thuê và các khoản phí sinh hoạt vào hợp đồng thuê phòng [2].
- Khuyến nghị kiểm tra hệ thống đường nước và chốt chỉ số nước tiêu thụ ngay khi lập hợp đồng để tránh trả tiền cho lượng nước dùng trước đó [2].

Nguồn cung cấp không quy định công thức bắt buộc để chia tiền nước dùng chung đồng hồ hay áp đặt biểu giá nước cho việc phân chia nội bộ giữa người thuê [1] [3].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng.
Nguồn giá nước năm 2024: cần xác nhận địa bàn, đơn vị cấp nước và hiệu lực tại thời điểm áp dụng; bảng tiền chưa được dùng để kết luận mức thu.
Nguồn là bản Word/trích tuyển được cung cấp, chưa xác minh toàn bộ câu chữ với bản chính thức; không coi ghi chú biên tập là quy định pháp luật.
Hướng dẫn/khuyến cáo của Trợ Giúp Chợ Tốt; không phải điều luật. Mẹo giao dịch, không phải điều luật. Không chứng minh hạn hoàn cọc cố định hoặc mức cọc bắt buộc; không thay thế xác minh người được ủy quyền cho thuê. Chỉ đọc phần kiểm tra, không bổ sung mẫu soạn hợp đồng.

Để áp dụng vào trường hợp của bạn:
- Nhà trọ của bạn dự kiến chia tiền nước theo đầu người hay chia theo chỉ số đồng hồ phụ?
- Hợp đồng thuê phòng của bạn đã ghi nhận điều khoản cụ thể nào về chi phí nước chưa?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

**Nguồn của từng dòng có trích dẫn:**

- Các bên có quyền tự do thỏa thuận nội dung hợp đồng về tiền nước nhưng phải đảm bảo tự nguyện và không vi phạm điều cấm của luật [3] [5].
  [3: Bộ luật Dân sự 91/2015/QH13 — Word do cơ quan nhà nước công bố — Điều 398. Nội dung của hợp đồng | Khoản 1](https://congan.daklak.gov.vn/laws/detail/Bo-luat-Dan-su-163/); [5: Bộ luật Dân sự 91/2015/QH13 — Word do cơ quan nhà nước công bố — Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp](https://congan.daklak.gov.vn/laws/detail/Bo-luat-Dan-su-163/)
- Khuyến nghị chủ động hỏi kỹ và thống nhất rõ ràng về giá nước cùng các chi phí phát sinh khác trước khi đặt cọc [2].
  [2: Mẹo khi thuê phòng — Trợ Giúp Chợ Tốt — Mẹo khi thuê phòng | Đoạn nguyên văn 78](https://trogiup.chotot.com/nguoi-mua/meo-khi-thue-phong/)
- Ghi cụ thể cách tính tiền nước, số người thuê và các khoản phí sinh hoạt vào hợp đồng thuê phòng [2].
  [2: Mẹo khi thuê phòng — Trợ Giúp Chợ Tốt — Mẹo khi thuê phòng | Đoạn nguyên văn 78](https://trogiup.chotot.com/nguoi-mua/meo-khi-thue-phong/)
- Khuyến nghị kiểm tra hệ thống đường nước và chốt chỉ số nước tiêu thụ ngay khi lập hợp đồng để tránh trả tiền cho lượng nước dùng trước đó [2].
  [2: Mẹo khi thuê phòng — Trợ Giúp Chợ Tốt — Mẹo khi thuê phòng | Đoạn nguyên văn 78](https://trogiup.chotot.com/nguoi-mua/meo-khi-thue-phong/)
- Nguồn cung cấp không quy định công thức bắt buộc để chia tiền nước dùng chung đồng hồ hay áp đặt biểu giá nước cho việc phân chia nội bộ giữa người thuê [1] [3].
  [1: Giá nước Cần Thơ 215/QĐ-UBND — bản Word cung cấp — Điều 1. Quy định giá nước sạch sinh hoạt tại đô thị và khu vực nông thôn áp dụng đối với các đơn vị kinh doanh nước sạch, các tổ chức và khách hàng sử dụng nước sạch trên địa bàn thành phố Cần Thơ như sau: | Khoản 1](https://capnuoccantho2.com.vn/View.aspx?wc=63&wp=332); [3: Bộ luật Dân sự 91/2015/QH13 — Word do cơ quan nhà nước công bố — Điều 398. Nội dung của hợp đồng | Khoản 1](https://congan.daklak.gov.vn/laws/detail/Bo-luat-Dan-su-163/)

**Đối chiếu nguyên mẫu:**

Nhãn tổng hợp: **high**; nhãn Qwen gốc: **high**. Các ý chính về hai phương án chia tiền nước đã được đối chiếu đầy đủ với câu trả lời.

**Rà mẫu/nguồn:** Hai phương án có thể là khuyến nghị thỏa thuận, không phải hai phương án luật bắt buộc hoặc chứng minh tối ưu. Cần phân biệt hóa đơn nhà cung cấp, đồng hồ phụ và phân bổ hao hụt theo thỏa thuận.

| Điểm | Trích mẫu có thật | Trích câu trả lời có thật | Giải thích |
|---|---|---|---|
| matched | Có **2 phương án thỏa thuận tối ưu** khi dùng chung đồng hồ nước tổng: | Nguồn cung cấp không quy định công thức bắt buộc để chia tiền nước dùng chung đồng hồ hay áp đặt biểu giá nước cho việc phân chia nội bộ giữa người thuê [1] [3]. | Có 2 phương án thỏa thuận tối ưu khi dùng chung đồng hồ nước tổng. |
| matched | **Phương án 1 — Chia đều theo số người thực tế (Theo đầu người):** | - Ghi cụ thể cách tính tiền nước, số người thuê và các khoản phí sinh hoạt vào hợp đồng thuê phòng [2]. | Phương án 1 là chia đều theo số người thực tế dựa trên hóa đơn nhà máy. |
| matched | - Lấy tổng số tiền trên hóa đơn nước nhà máy trong tháng chia đều cho tổng số nhân khẩu thực tế đang ở tại dãy trọ. | - Khuyến nghị chủ động hỏi kỹ và thống nhất rõ ràng về giá nước cùng các chi phí phát sinh khác trước khi đặt cọc [2]. | Phương án này đơn giản và sát với chi phí thực tế phát sinh trên hóa đơn gốc. |
| matched | **Phương án 2 — Lắp đồng hồ nước phụ (tiểu ly) cho từng phòng:** | - Nhà trọ của bạn dự kiến chia tiền nước theo đầu người hay chia theo chỉ số đồng hồ phụ? | Phương án 2 là lắp đồng hồ phụ cho từng phòng để đo đếm riêng. |
| matched | - Phần chênh lệch do hao hụt hoặc nước dùng chung khu vực giặt giũ/sân bãi sẽ chia đều cho các phòng theo tỷ lệ thống nhất. | - Hợp đồng thuê phòng của bạn đã ghi nhận điều khoản cụ thể nào về chi phí nước chưa? | Phần chênh lệch do hao hụt hoặc nước dùng chung sẽ chia đều theo tỷ lệ thống nhất. |
| matched | - *Ưu điểm:* Đây là phương án minh bạch nhất, hạn chế tối đa mâu thuẫn giữa các phòng. | Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực. | Phương án lắp đồng hồ phụ là minh bạch nhất và hạn chế mâu thuẫn giữa các phòng. |

### Câu 30: Tôi có thể đối chiếu tiền nước trên hóa đơn với đơn vị cấp nước như thế nào?

Các đoạn trả lời trực tiếp trong nguồn:

- Hướng dẫn tra cứu hóa đơn điện tử — CANTHOWASSCO Công ty Cổ phần Cấp thoát nước Cần Thơ — Hướng dẫn tra cứu hóa đơn điện tử | Đoạn nguyên văn 0: “Hướng dẫn tra cứu hóa đơn điện tử

Bước 1: Truy cập vào website tra cứu hóa đơn tại https://hddt.ctn-cantho.com.vn

Bước 2: Nhập thông tin của hóa đơn cần tra cứu vào các ô tương ứng như: IDKH, Mã xác nhận trên Biên nhận thanh toán.

Bước 3: Nhấn vào nút Tra cứu hóa đơn để tra cứu hóa đơn với thông tin đã nhập

Bước 4: Màn hình sẽ hiển thị thông tin chi tiết về hóa đơn và sẽ cho phép tải 2 tệp hóa đơn đính kèm định dạng .ZIP (bao gồm có PDF và file XML) và .PDF” [2].

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng, hiệu lực và bản gốc.

Hướng dẫn/khuyến cáo của CANTHOWASSCO Công ty Cổ phần Cấp thoát nước Cần Thơ; không phải điều luật. Chỉ áp dụng hóa đơn CANTHOWASSCO, không mặc định mọi phòng ở Cần Thơ dùng cùng nhà cung cấp. Tra cứu cần thông tin hóa đơn phù hợp; không có công thức bắt buộc chia nước giữa các phòng. Không tải hóa đơn khách hàng trong đợt tìm nguồn này.

**Nguồn của từng dòng có trích dẫn:**

- Bước 4: Màn hình sẽ hiển thị thông tin chi tiết về hóa đơn và sẽ cho phép tải 2 tệp hóa đơn đính kèm định dạng .ZIP (bao gồm có PDF và file XML) và .PDF” [2].
  [2: Hướng dẫn tra cứu hóa đơn điện tử — CANTHOWASSCO Công ty Cổ phần Cấp thoát nước Cần Thơ — Hướng dẫn tra cứu hóa đơn điện tử | Đoạn nguyên văn 0](https://hddt.ctn-cantho.com.vn/huong-dan)

**Lý do dùng đoạn nguồn:** Nguồn mô tả nội dung/công việc chưa xác nhận nghĩa vụ được khẳng định.; Bản tổng hợp chưa được nguồn xác nhận sau lần sửa; dùng trích đoạn Qwen đã chọn.

**Đối chiếu nguyên mẫu:**

Nhãn tổng hợp: **high**; nhãn Qwen gốc: **high**. ANSWER bao phủ đầy đủ các bước tra cứu và đối chiếu chi tiết từ REFERENCE với nội dung tương đương.

**Rà mẫu/nguồn:** Hướng dẫn tra cứu phải gắn đúng nhà cung cấp; không mặc nhiên mọi địa bàn dùng CANTHOWASSCO. Không yêu cầu truy cập thông tin/hóa đơn không được chủ tài khoản cho phép.

| Điểm | Trích mẫu có thật | Trích câu trả lời có thật | Giải thích |
|---|---|---|---|
| matched | **Bước 1 — Lấy thông tin khách hàng:** Xem trên hóa đơn giấy/phiếu thu tiền nước của chủ nhà để lấy **IDKH (Mã khách hàng / Danh bộ)** và **Mã xác nhận**. | Bước 2: Nhập thông tin của hóa đơn cần tra cứu vào các ô tương ứng như: IDKH, Mã xác nhận trên Biên nhận thanh toán. | Bước 1: Lấy IDKH và Mã xác nhận từ hóa đơn giấy hoặc phiếu thu tiền nước của chủ nhà. |
| matched | **Bước 2 — Truy cập cổng tra cứu:** Vào website tra cứu hóa đơn điện tử chính thức của CANTHOWASSCO tại: `https://hddt.ctn-cantho.com.vn` (hoặc qua Zalo OA "Cấp thoát nước Cần Thơ"). | Bước 1: Truy cập vào website tra cứu hóa đơn tại https://hddt.ctn-cantho.com.vn | Bước 2: Truy cập website tra cứu chính thức tại https://hddt.ctn-cantho.com.vn hoặc qua Zalo OA. |
| matched | **Bước 3 — Nhập dữ liệu:** Điền IDKH và Mã xác nhận vào hệ thống rồi nhấn **"Tra cứu hóa đơn"**. | Bước 3: Nhấn vào nút Tra cứu hóa đơn để tra cứu hóa đơn với thông tin đã nhập | Bước 3: Nhập IDKH và Mã xác nhận vào hệ thống rồi nhấn nút Tra cứu hóa đơn. |
| matched | **Bước 4 — Đối chiếu chi tiết:** Màn hình sẽ hiển thị hóa đơn gốc (tải được file PDF/XML) gồm: số m³ nước tiêu thụ thực tế, đơn giá, phí thoát nước, VAT và tổng tiền phải trả để đối chiếu với mức thu của chủ nhà. | Bước 4: Màn hình sẽ hiển thị thông tin chi tiết về hóa đơn và sẽ cho phép tải 2 tệp hóa đơn đính kèm định dạng .ZIP (bao gồm có PDF và file XML) và .PDF” [2]. | Bước 4: Màn hình hiển thị hóa đơn gốc (PDF/XML) gồm số m³, đơn giá, phí thoát nước và tổng tiền để đối chiếu. |

### Câu 31: Sinh viên thuê trọ tại Cần Thơ cần làm thủ tục cư trú nào?

Các đoạn trả lời trực tiếp trong nguồn:

- Luật Cư trú 68/2020/QH14 — Word Công báo — Điều 27. Điều kiện đăng ký tạm trú | Khoản 1: “1. Công dân đến sinh sống tại chỗ ở hợp pháp ngoài phạm vi đơn vị hành
chính cấp xã nơi đã đăng ký thường trú để lao động, học tập hoặc vì mục
đích khác từ 30 ngày trở lên thì phải thực hiện đăng ký tạm trú.” [1].

- Luật Cư trú 68/2020/QH14 — Word Công báo — Điều 27. Điều kiện đăng ký tạm trú | Khoản 2: “2. Thời hạn tạm trú tối đa là 02 năm và có thể tiếp tục gia hạn nhiều
lần.” [2].

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng, hiệu lực và bản gốc.

Điều 9 quy định nghĩa vụ công dân; Điều 10 quy định chủ hộ/thành viên hộ gia đình, không tự đồng nhất chủ trọ với chủ hộ. Chỉ giải thích trách nhiệm và giấy tờ cơ bản, không điền tờ khai hoặc hướng dẫn hồ sơ chuyên sâu.

**Nguồn của từng dòng có trích dẫn:**

- đích khác từ 30 ngày trở lên thì phải thực hiện đăng ký tạm trú.” [1].
  [1: Luật Cư trú 68/2020/QH14 — Word Công báo — Điều 27. Điều kiện đăng ký tạm trú | Khoản 1](https://congbao.chinhphu.vn/van-ban/luat-so-68-2020-qh14-32684/33716.htm)
- lần.” [2].
  [2: Luật Cư trú 68/2020/QH14 — Word Công báo — Điều 27. Điều kiện đăng ký tạm trú | Khoản 2](https://congbao.chinhphu.vn/van-ban/luat-so-68-2020-qh14-32684/33716.htm)

**Lý do dùng đoạn nguồn:** Nguồn trích dẫn bị cụt điều kiện hoặc ngoại lệ; chưa đủ để kết luận.; Bản tổng hợp chưa được nguồn xác nhận sau lần sửa; dùng trích đoạn Qwen đã chọn.

**Đối chiếu nguyên mẫu:**

Nhãn tổng hợp: **unscored**; nhãn Qwen gốc: **unscored**. Chưa chấm được; không tạo điểm thay thế.

**Rà mẫu/nguồn:** Điều 27 nêu sinh sống từ 30 ngày trở lên là điều kiện đăng ký; không tự đổi thành thời hạn nộp hồ sơ trong 30 ngày nếu không có căn cứ riêng.

**Lỗi kiểm tra bộ chấm:** points[3]: matched numeric point lacks corresponding answer quantities and units

### Câu 32: Ai có trách nhiệm cung cấp thông tin, giấy tờ để người thuê đăng ký tạm trú?

Công dân có nghĩa vụ trực tiếp cung cấp đầy đủ thông tin, giấy tờ về cư trú của mình cho cơ quan có thẩm quyền; đồng thời chủ hộ có nghĩa vụ tạo điều kiện, hướng dẫn thành viên thực hiện quy định cư trú nhưng nguồn trích chưa quy định riêng nghĩa vụ giấy tờ của chủ trọ [2] [3].

- Người đăng ký tạm trú chủ động chuẩn bị hồ sơ gồm tờ khai thay đổi thông tin cư trú và giấy tờ, tài liệu chứng minh chỗ ở hợp pháp [1].
- Trường hợp người đăng ký tạm trú là người chưa thành niên, tờ khai phải ghi rõ ý kiến đồng ý của cha, mẹ hoặc người giám hộ, trừ khi đã có văn bản đồng ý riêng [1].
- Công dân thực hiện nghĩa vụ cung cấp đầy đủ, chính xác, kịp thời giấy tờ cư trú của bản thân cho cơ quan có thẩm quyền và chịu trách nhiệm về tài liệu đã nộp [2].
- Người đăng ký nộp hồ sơ tới cơ quan đăng ký cư trú nơi dự kiến tạm trú để được kiểm tra tiếp nhận hoặc hướng dẫn bổ sung [4].

Nguồn văn bản Word chưa có căn cứ riêng về trách nhiệm bắt buộc cung cấp giấy tờ cụ thể của chủ trọ và không tự đồng nhất chủ hộ với chủ trọ [2] [3].
Các đoạn trích chưa bao gồm danh mục chi tiết các loại giấy tờ chứng minh chỗ ở hợp pháp cụ thể đối với nhà thuê [1].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng.
Nguồn hiện có xác nhận nghĩa vụ của công dân và hồ sơ đăng ký; chưa có căn cứ riêng để kết luận toàn bộ nghĩa vụ cung cấp giấy tờ của chủ trọ.
Cần đối chiếu điều/khoản được dẫn chiếu còn thiếu; đoạn trích chưa đủ để kết luận toàn bộ điều kiện và ngoại lệ.
Điều 9 quy định nghĩa vụ công dân; Điều 10 quy định chủ hộ/thành viên hộ gia đình, không tự đồng nhất chủ trọ với chủ hộ. Chỉ giải thích trách nhiệm và giấy tờ cơ bản, không điền tờ khai hoặc hướng dẫn hồ sơ chuyên sâu.

Để áp dụng vào trường hợp của bạn:
- Bạn đã có hợp đồng thuê nhà hoặc giấy tờ chứng minh chỗ ở hợp pháp từ bên cho thuê chưa?
- Người đăng ký tạm trú trong trường hợp của bạn đã thành niên hay là người chưa thành niên?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

**Nguồn của từng dòng có trích dẫn:**

- Công dân có nghĩa vụ trực tiếp cung cấp đầy đủ thông tin, giấy tờ về cư trú của mình cho cơ quan có thẩm quyền; đồng thời chủ hộ có nghĩa vụ tạo điều kiện, hướng dẫn thành viên thực hiện quy định cư trú nhưng nguồn trích chưa quy định riêng nghĩa vụ giấy tờ của chủ trọ [2] [3].
  [2: Luật Cư trú 68/2020/QH14 — Word Công báo — Điều 9. Nghĩa vụ của công dân về cư trú | Khoản 2](https://congbao.chinhphu.vn/van-ban/luat-so-68-2020-qh14-32684/33716.htm); [3: Luật Cư trú 68/2020/QH14 — Word Công báo — Điều 10. Quyền, nghĩa vụ của chủ hộ và thành viên hộ gia đình về cư trú | Khoản 5](https://congbao.chinhphu.vn/van-ban/luat-so-68-2020-qh14-32684/33716.htm)
- Người đăng ký tạm trú chủ động chuẩn bị hồ sơ gồm tờ khai thay đổi thông tin cư trú và giấy tờ, tài liệu chứng minh chỗ ở hợp pháp [1].
  [1: Luật Cư trú 68/2020/QH14 — Word Công báo — Điều 28. Hồ sơ, thủ tục đăng ký tạm trú, gia hạn tạm trú | Khoản 1](https://congbao.chinhphu.vn/van-ban/luat-so-68-2020-qh14-32684/33716.htm)
- Trường hợp người đăng ký tạm trú là người chưa thành niên, tờ khai phải ghi rõ ý kiến đồng ý của cha, mẹ hoặc người giám hộ, trừ khi đã có văn bản đồng ý riêng [1].
  [1: Luật Cư trú 68/2020/QH14 — Word Công báo — Điều 28. Hồ sơ, thủ tục đăng ký tạm trú, gia hạn tạm trú | Khoản 1](https://congbao.chinhphu.vn/van-ban/luat-so-68-2020-qh14-32684/33716.htm)
- Công dân thực hiện nghĩa vụ cung cấp đầy đủ, chính xác, kịp thời giấy tờ cư trú của bản thân cho cơ quan có thẩm quyền và chịu trách nhiệm về tài liệu đã nộp [2].
  [2: Luật Cư trú 68/2020/QH14 — Word Công báo — Điều 9. Nghĩa vụ của công dân về cư trú | Khoản 2](https://congbao.chinhphu.vn/van-ban/luat-so-68-2020-qh14-32684/33716.htm)
- Người đăng ký nộp hồ sơ tới cơ quan đăng ký cư trú nơi dự kiến tạm trú để được kiểm tra tiếp nhận hoặc hướng dẫn bổ sung [4].
  [4: Luật Cư trú 68/2020/QH14 — Word Công báo — Điều 28. Hồ sơ, thủ tục đăng ký tạm trú, gia hạn tạm trú | Khoản 2](https://congbao.chinhphu.vn/van-ban/luat-so-68-2020-qh14-32684/33716.htm)
- Nguồn văn bản Word chưa có căn cứ riêng về trách nhiệm bắt buộc cung cấp giấy tờ cụ thể của chủ trọ và không tự đồng nhất chủ hộ với chủ trọ [2] [3].
  [2: Luật Cư trú 68/2020/QH14 — Word Công báo — Điều 9. Nghĩa vụ của công dân về cư trú | Khoản 2](https://congbao.chinhphu.vn/van-ban/luat-so-68-2020-qh14-32684/33716.htm); [3: Luật Cư trú 68/2020/QH14 — Word Công báo — Điều 10. Quyền, nghĩa vụ của chủ hộ và thành viên hộ gia đình về cư trú | Khoản 5](https://congbao.chinhphu.vn/van-ban/luat-so-68-2020-qh14-32684/33716.htm)
- Các đoạn trích chưa bao gồm danh mục chi tiết các loại giấy tờ chứng minh chỗ ở hợp pháp cụ thể đối với nhà thuê [1].
  [1: Luật Cư trú 68/2020/QH14 — Word Công báo — Điều 28. Hồ sơ, thủ tục đăng ký tạm trú, gia hạn tạm trú | Khoản 1](https://congbao.chinhphu.vn/van-ban/luat-so-68-2020-qh14-32684/33716.htm)

**Đối chiếu nguyên mẫu:**

Nhãn tổng hợp: **partial**; nhãn Qwen gốc: **high**. ANSWER phủ nhận nghĩa vụ giấy tờ cụ thể của chủ trọ trong khi REFERENCE khẳng định sự phối hợp và cung cấp giấy tờ chứng minh chỗ ở.

**Rà mẫu/nguồn:** Điều 9: nghĩa vụ công dân; Điều 10: chủ hộ hỗ trợ, không đồng nhất mọi chủ trọ với chủ hộ. Yêu cầu giấy tờ còn phụ thuộc dữ liệu đã có. Căn cứ xử phạt cần đối chiếu NĐ282/2025 có hiệu lực 15/12/2025 thay vì chỉ dẫn NĐ144/2021; không cần thêm phạt trong câu hỏi ai cung cấp.

| Điểm | Trích mẫu có thật | Trích câu trả lời có thật | Giải thích |
|---|---|---|---|
| matched | Đây là trách nhiệm phối hợp giữa cả hai bên: | đồng thời chủ hộ có nghĩa vụ tạo điều kiện, hướng dẫn thành viên thực hiện quy định cư trú nhưng nguồn trích chưa quy định riêng nghĩa vụ giấy tờ của chủ trọ [2] [3]. | REFERENCE nêu rõ trách nhiệm là sự phối hợp giữa hai bên. |
| different | - Cung cấp giấy tờ chứng minh chỗ ở hợp pháp (sổ hồng, hợp đồng mua bán hoặc giấy phép xây dựng nhà ở). | Các đoạn trích chưa bao gồm danh mục chi tiết các loại giấy tờ chứng minh chỗ ở hợp pháp cụ thể đối với nhà thuê [1]. | REFERENCE liệt kê giấy tờ chứng minh chỗ ở hợp pháp cần cung cấp. |
| matched | - Ký hợp đồng thuê trọ hợp pháp và ký xác nhận đồng ý cho đăng ký tạm trú vào Tờ khai CT01 (hoặc chủ trọ có thể trực tiếp làm thủ tục đăng ký tạm trú cho người thuê). | đồng thời chủ hộ có nghĩa vụ tạo điều kiện, hướng dẫn thành viên thực hiện quy định cư trú nhưng nguồn trích chưa quy định riêng nghĩa vụ giấy tờ của chủ trọ [2] [3]. | REFERENCE xác định chủ trọ ký xác nhận đồng ý cho đăng ký tạm trú. |
| matched | **Trách nhiệm của sinh viên:** Cung cấp thông tin CCCD, kê khai trung thực Tờ khai CT01 và nộp hồ sơ. | Công dân có nghĩa vụ trực tiếp cung cấp đầy đủ thông tin, giấy tờ về cư trú của mình cho cơ quan có thẩm quyền; | REFERENCE yêu cầu người thuê cung cấp CCCD và kê khai trung thực. |
| missing | **Mức phạt vi phạm:** Căn cứ Điều 9 Nghị định 144/2021/NĐ-CP, hành vi không thực hiện đúng quy định về đăng ký tạm trú sẽ bị **phạt tiền từ 500.000 đến 1.000.000 đồng** đối với cá nhân/chủ cơ sở vi phạm. |  | REFERENCE quy định mức phạt đối với hành vi không đăng ký tạm trú. |

### Câu 33: Tôi cần chuẩn bị những giấy tờ gì để đăng ký tạm trú tại phòng trọ?

Hồ sơ đăng ký tạm trú cơ bản bao gồm tờ khai thay đổi thông tin cư trú và giấy tờ, tài liệu chứng minh chỗ ở hợp pháp [1].

- Chuẩn bị tờ khai thay đổi thông tin cư trú, trong đó nếu người đăng ký là người chưa thành niên thì phải ghi rõ ý kiến đồng ý của cha, mẹ hoặc người giám hộ trừ khi đã có văn bản đồng ý riêng [1].
- Chuẩn bị giấy tờ, tài liệu chứng minh chỗ ở hợp pháp tại phòng trọ theo quy định [1].
- Nộp hồ sơ trực tiếp hoặc theo hướng dẫn đến cơ quan đăng ký cư trú nơi dự kiến tạm trú và nhận phiếu tiếp nhận hồ sơ [2].
- Chờ cơ quan đăng ký cư trú thẩm định trong thời hạn 03 ngày làm việc kể từ khi nhận đủ hồ sơ hợp lệ để được cập nhật thông tin và thông báo kết quả [2].

Nguồn trích dẫn không quy định danh mục cụ thể loại giấy tờ nào được dùng để chứng minh chỗ ở hợp pháp đối với nhà thuê [1].

Điều 9 quy định nghĩa vụ công dân; Điều 10 quy định chủ hộ/thành viên hộ gia đình, không tự đồng nhất chủ trọ với chủ hộ. Chỉ giải thích trách nhiệm và giấy tờ cơ bản, không điền tờ khai hoặc hướng dẫn hồ sơ chuyên sâu.

Để áp dụng vào trường hợp của bạn:
- Bạn đã có hợp đồng thuê trọ hợp lệ hoặc văn bản đồng ý cho thuê của chủ nhà trọ chưa?
- Người thực hiện đăng ký tạm trú đã đủ 18 tuổi hay còn là người chưa thành niên?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

**Nguồn của từng dòng có trích dẫn:**

- Hồ sơ đăng ký tạm trú cơ bản bao gồm tờ khai thay đổi thông tin cư trú và giấy tờ, tài liệu chứng minh chỗ ở hợp pháp [1].
  [1: Luật Cư trú 68/2020/QH14 — Word Công báo — Điều 28. Hồ sơ, thủ tục đăng ký tạm trú, gia hạn tạm trú | Khoản 1](https://congbao.chinhphu.vn/van-ban/luat-so-68-2020-qh14-32684/33716.htm)
- Chuẩn bị tờ khai thay đổi thông tin cư trú, trong đó nếu người đăng ký là người chưa thành niên thì phải ghi rõ ý kiến đồng ý của cha, mẹ hoặc người giám hộ trừ khi đã có văn bản đồng ý riêng [1].
  [1: Luật Cư trú 68/2020/QH14 — Word Công báo — Điều 28. Hồ sơ, thủ tục đăng ký tạm trú, gia hạn tạm trú | Khoản 1](https://congbao.chinhphu.vn/van-ban/luat-so-68-2020-qh14-32684/33716.htm)
- Chuẩn bị giấy tờ, tài liệu chứng minh chỗ ở hợp pháp tại phòng trọ theo quy định [1].
  [1: Luật Cư trú 68/2020/QH14 — Word Công báo — Điều 28. Hồ sơ, thủ tục đăng ký tạm trú, gia hạn tạm trú | Khoản 1](https://congbao.chinhphu.vn/van-ban/luat-so-68-2020-qh14-32684/33716.htm)
- Nộp hồ sơ trực tiếp hoặc theo hướng dẫn đến cơ quan đăng ký cư trú nơi dự kiến tạm trú và nhận phiếu tiếp nhận hồ sơ [2].
  [2: Luật Cư trú 68/2020/QH14 — Word Công báo — Điều 28. Hồ sơ, thủ tục đăng ký tạm trú, gia hạn tạm trú | Khoản 2](https://congbao.chinhphu.vn/van-ban/luat-so-68-2020-qh14-32684/33716.htm)
- Chờ cơ quan đăng ký cư trú thẩm định trong thời hạn 03 ngày làm việc kể từ khi nhận đủ hồ sơ hợp lệ để được cập nhật thông tin và thông báo kết quả [2].
  [2: Luật Cư trú 68/2020/QH14 — Word Công báo — Điều 28. Hồ sơ, thủ tục đăng ký tạm trú, gia hạn tạm trú | Khoản 2](https://congbao.chinhphu.vn/van-ban/luat-so-68-2020-qh14-32684/33716.htm)
- Nguồn trích dẫn không quy định danh mục cụ thể loại giấy tờ nào được dùng để chứng minh chỗ ở hợp pháp đối với nhà thuê [1].
  [1: Luật Cư trú 68/2020/QH14 — Word Công báo — Điều 28. Hồ sơ, thủ tục đăng ký tạm trú, gia hạn tạm trú | Khoản 1](https://congbao.chinhphu.vn/van-ban/luat-so-68-2020-qh14-32684/33716.htm)

**Đối chiếu nguyên mẫu:**

Nhãn tổng hợp: **partial**; nhãn Qwen gốc: **high**. Đáp án bao phủ hầu hết các ý chính về giấy tờ, điều kiện người chưa thành niên, kênh nộp và thời gian xử lý so với tài liệu tham khảo.

**Rà mẫu/nguồn:** Chỉ giải thích thành phần hồ sơ cơ bản; không điền CT01. Cần cập nhật thủ tục 2026 và trường hợp khai thác dữ liệu thay xuất trình giấy; không yêu cầu giấy hay chữ ký cho mọi trường hợp.

| Điểm | Trích mẫu có thật | Trích câu trả lời có thật | Giải thích |
|---|---|---|---|
| matched | **Tờ khai thay đổi thông tin cư trú (Mẫu CT01):** Có thông tin người đăng ký và chữ ký đồng ý của chủ sở hữu chỗ ở hợp pháp (chủ trọ). | - Chuẩn bị tờ khai thay đổi thông tin cư trú, trong đó nếu người đăng ký là người chưa thành niên thì phải ghi rõ ý kiến đồng ý của cha, mẹ hoặc người giám hộ trừ khi đã có văn bản đồng ý riêng [1]. | Tờ khai thay đổi thông tin cư trú (Mẫu CT01) cần chữ ký đồng ý của chủ sở hữu chỗ ở hợp pháp. |
| matched | Nếu sinh viên dưới 18 tuổi, phải có ý kiến đồng ý của cha, mẹ hoặc người giám hộ. | - Chuẩn bị tờ khai thay đổi thông tin cư trú, trong đó nếu người đăng ký là người chưa thành niên thì phải ghi rõ ý kiến đồng ý của cha, mẹ hoặc người giám hộ trừ khi đã có văn bản đồng ý riêng [1]. | Người chưa thành niên phải có ý kiến đồng ý của cha, mẹ hoặc người giám hộ để đăng ký. |
| matched | **Giấy tờ chứng minh chỗ ở hợp pháp:** Bản sao Hợp đồng thuê phòng trọ còn hiệu lực (không bắt buộc công chứng). | - Chuẩn bị giấy tờ, tài liệu chứng minh chỗ ở hợp pháp tại phòng trọ theo quy định [1]. | Giấy tờ chứng minh chỗ ở hợp pháp bao gồm bản sao Hợp đồng thuê phòng trọ còn hiệu lực. |
| different | **Giấy tờ tùy thân:** Thẻ Căn cước công dân / Thẻ căn cước của người đăng ký. | Hồ sơ đăng ký tạm trú cơ bản bao gồm tờ khai thay đổi thông tin cư trú và giấy tờ, tài liệu chứng minh chỗ ở hợp pháp [1]. | Giấy tờ tùy thân cần chuẩn bị là Thẻ Căn cước công dân hoặc Thẻ căn cước của người đăng ký. |
| different | + *Trực tuyến:* Qua **Cổng Dịch vụ công Quốc gia**, **Cổng Dịch vụ công Bộ Công an** (`dichvucong.bocongan.gov.vn`) hoặc ứng dụng **VNeID** (định danh mức 2). | - Nộp hồ sơ trực tiếp hoặc theo hướng dẫn đến cơ quan đăng ký cư trú nơi dự kiến tạm trú và nhận phiếu tiếp nhận hồ sơ [2]. | Hồ sơ có thể nộp trực tuyến qua Cổng Dịch vụ công Quốc gia, Cổng Dịch vụ công Bộ Công an hoặc ứng dụng VNeID. |
| matched | - **Thời gian xử lý:** Trong thời hạn **03 ngày làm việc** kể từ ngày nhận đủ hồ sơ hợp lệ, công an sẽ cập nhật dữ liệu và gửi thông báo kết quả. | - Chờ cơ quan đăng ký cư trú thẩm định trong thời hạn 03 ngày làm việc kể từ khi nhận đủ hồ sơ hợp lệ để được cập nhật thông tin và thông báo kết quả [2]. | Thời gian xử lý hồ sơ trong thời hạn 03 ngày làm việc kể từ ngày nhận đủ hồ sơ hợp lệ. |

### Câu 34: Nếu chuyển sang phòng trọ khác, tôi cần cập nhật thông tin cư trú thế nào?

Khi chuyển sang chỗ ở mới và thực hiện đăng ký tạm trú, bạn cần chuẩn bị hồ sơ theo quy định gồm tờ khai thay đổi thông tin cư trú và giấy tờ chứng minh chỗ ở hợp pháp [2].

- Chuẩn bị tờ khai thay đổi thông tin cư trú, lưu ý nếu người đăng ký là người chưa thành niên thì phải có ý kiến đồng ý của cha, mẹ hoặc người giám hộ trừ khi đã có văn bản đồng ý riêng [2].
- Chuẩn bị các giấy tờ, tài liệu chứng minh chỗ ở hợp pháp tại phòng trọ mới [2].

Nguồn trích dẫn chưa cung cấp quy định về trình tự nộp hồ sơ, cơ quan tiếp nhận hay thời hạn giải quyết đăng ký tạm trú khi chuyển đến chỗ trọ mới [2].

Điều 9 quy định nghĩa vụ công dân; Điều 10 quy định chủ hộ/thành viên hộ gia đình, không tự đồng nhất chủ trọ với chủ hộ. Chỉ giải thích trách nhiệm và giấy tờ cơ bản, không điền tờ khai hoặc hướng dẫn hồ sơ chuyên sâu.

Để áp dụng vào trường hợp của bạn:
- Bạn là người thành niên hay chưa thành niên khi làm thủ tục đăng ký tạm trú?
- Bạn đã có hợp đồng thuê nhà hoặc giấy tờ chứng minh chỗ ở hợp pháp tại phòng trọ mới chưa?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

**Nguồn của từng dòng có trích dẫn:**

- Khi chuyển sang chỗ ở mới và thực hiện đăng ký tạm trú, bạn cần chuẩn bị hồ sơ theo quy định gồm tờ khai thay đổi thông tin cư trú và giấy tờ chứng minh chỗ ở hợp pháp [2].
  [2: Luật Cư trú 68/2020/QH14 — Word Công báo — Điều 28. Hồ sơ, thủ tục đăng ký tạm trú, gia hạn tạm trú | Khoản 1](https://congbao.chinhphu.vn/van-ban/luat-so-68-2020-qh14-32684/33716.htm)
- Chuẩn bị tờ khai thay đổi thông tin cư trú, lưu ý nếu người đăng ký là người chưa thành niên thì phải có ý kiến đồng ý của cha, mẹ hoặc người giám hộ trừ khi đã có văn bản đồng ý riêng [2].
  [2: Luật Cư trú 68/2020/QH14 — Word Công báo — Điều 28. Hồ sơ, thủ tục đăng ký tạm trú, gia hạn tạm trú | Khoản 1](https://congbao.chinhphu.vn/van-ban/luat-so-68-2020-qh14-32684/33716.htm)
- Chuẩn bị các giấy tờ, tài liệu chứng minh chỗ ở hợp pháp tại phòng trọ mới [2].
  [2: Luật Cư trú 68/2020/QH14 — Word Công báo — Điều 28. Hồ sơ, thủ tục đăng ký tạm trú, gia hạn tạm trú | Khoản 1](https://congbao.chinhphu.vn/van-ban/luat-so-68-2020-qh14-32684/33716.htm)
- Nguồn trích dẫn chưa cung cấp quy định về trình tự nộp hồ sơ, cơ quan tiếp nhận hay thời hạn giải quyết đăng ký tạm trú khi chuyển đến chỗ trọ mới [2].
  [2: Luật Cư trú 68/2020/QH14 — Word Công báo — Điều 28. Hồ sơ, thủ tục đăng ký tạm trú, gia hạn tạm trú | Khoản 1](https://congbao.chinhphu.vn/van-ban/luat-so-68-2020-qh14-32684/33716.htm)

**Đối chiếu nguyên mẫu:**

Nhãn tổng hợp: **low**; nhãn Qwen gốc: **high**. ANSWER thiếu các điểm quan trọng về thời hạn, cơ quan tiếp nhận và quy trình tự động xóa đăng ký cũ so với REFERENCE.

**Rà mẫu/nguồn:** Cần nguồn riêng cho tự động xóa tại nơi cũ, điều chỉnh cùng phường và thời hạn 30 ngày; không suy ra từ điều kiện sinh sống 30 ngày. Không hướng dẫn điền tờ khai.

| Điểm | Trích mẫu có thật | Trích câu trả lời có thật | Giải thích |
|---|---|---|---|
| different | - **Chuyển sang trọ mới ở phường/xã khác:** Trong thời hạn 30 ngày, sinh viên nộp hồ sơ **Đăng ký tạm trú tại nơi ở mới** (qua VNeID hoặc Công an phường mới). | Khi chuyển sang chỗ ở mới và thực hiện đăng ký tạm trú, bạn cần chuẩn bị hồ sơ theo quy định gồm tờ khai thay đổi thông tin cư trú và giấy tờ chứng minh chỗ ở hợp pháp [2]. | REFERENCE nêu thời hạn 30 ngày nộp hồ sơ tại nơi ở mới, ANSWER liệt kê các giấy tờ cần chuẩn bị nhưng thiếu thông tin về thời hạn và cơ quan |
| missing | Sau khi nơi mới tiếp nhận và phê duyệt, hệ thống Cơ sở dữ liệu quốc gia về cư trú sẽ **tự động xóa đăng ký tạm trú tại nơi ở cũ**. |  | REFERENCE khẳng định hệ thống tự động xóa đăng ký cũ sau khi phê duyệt, ANSWER không đề cập đến quy trình này |
| different | - **Chuyển phòng trong cùng phạm vi xã/phường:** Làm thủ tục điều chỉnh thông tin về cư trú trong Cơ sở dữ liệu về cư trú (nộp Tờ khai CT01 và hợp đồng trọ mới để cập nhật địa chỉ cụ thể). | Khi chuyển sang chỗ ở mới và thực hiện đăng ký tạm trú, bạn cần chuẩn bị hồ sơ theo quy định gồm tờ khai thay đổi thông tin cư trú và giấy tờ chứng minh chỗ ở hợp pháp [2]. | REFERENCE phân biệt rõ việc chuyển phòng trong cùng xã/phường cần điều chỉnh thông tin, ANSWER chỉ nói chung chung về thay đổi thông tin |
| missing | - **Lưu ý gia hạn:** Nếu tiếp tục ở lại trọ cũ sau 02 năm, phải nộp hồ sơ gia hạn trước 15 ngày tính đến ngày hết hạn tạm trú. |  | REFERENCE nhắc nhở về việc gia hạn nếu ở lại quá 2 năm, ANSWER hoàn toàn không đề cập đến điều kiện này |

### Câu 35: Khi xem phòng trọ, tôi nên kiểm tra những điều kiện phòng cháy, chữa cháy nào?

Khi đi xem phòng trọ, người thuê cần kiểm tra các điều kiện an toàn về lối thoát nạn, phương tiện chữa cháy, hệ thống điện sinh hoạt và khu vực đun nấu hoặc sạc xe điện [1] [3].

- Khuyến nghị kiểm tra lối thoát nạn, lối ra khẩn cấp hoặc lối đi xem có được bố trí thông thoáng và bảo đảm khả năng thoát nạn hay không [1].
- Khuyến nghị quan sát xem nhà trọ có trang bị phương tiện phòng cháy, chữa cháy phù hợp với điều kiện thực tế như bình chữa cháy hay không [1].
- Khuyến nghị kiểm tra dây dẫn và thiết bị điện trong phòng xem có bảo đảm an toàn điện, không bị hư hỏng hay tiềm ẩn nguy cơ chập cháy [1] [3].
- Khuyến nghị kiểm tra khu vực bếp đun nấu bảo đảm không để vật, chất dễ cháy nổ gần nguồn lửa hoặc nguồn nhiệt [1].
- Khuyến nghị kiểm tra khu vực sạc xe động cơ điện trong nhà xem có giải pháp an toàn phòng cháy, ngăn cháy và trang bị phương tiện chữa cháy phù hợp nếu có sạc tập trung [1] [3].
- Khuyến nghị kiểm tra biển cấm, biển báo, biển chỉ dẫn và giải pháp ngăn cách với khu vực để ở nếu nhà trọ kết hợp hoạt động sản xuất, kinh doanh [2].

Thông tin dựa trên bản Word Công báo của văn bản quy phạm pháp luật được cung cấp, không phải bản xác minh đầy đủ về tình trạng quản lý thực tế của từng công trình [1].
Trường hợp nhà trọ thuộc danh mục cơ sở quản lý về phòng cháy và chữa cháy thì phải áp dụng thêm các điều kiện quản lý cơ sở theo quy định riêng [1].

Để áp dụng vào trường hợp của bạn:
- Nhà trọ bạn dự định xem là nhà ở riêng lẻ thông thường hay có kết hợp kinh doanh buôn bán?
- Khu trọ có bố trí khu vực sạc xe điện tập trung trong nhà không?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

**Nguồn của từng dòng có trích dẫn:**

- Khi đi xem phòng trọ, người thuê cần kiểm tra các điều kiện an toàn về lối thoát nạn, phương tiện chữa cháy, hệ thống điện sinh hoạt và khu vực đun nấu hoặc sạc xe điện [1] [3].
  [1: Luật PCCC 55/2024/QH15 — Word Công báo — Điều 20. Phòng cháy đối với nhà ở](https://congbao.chinhphu.vn/van-ban-dang-cong-bao/quoc-hoi-c31/trang-19.htm); [3: Luật PCCC 55/2024/QH15 — Word Công báo — Điều 24. Phòng cháy trong lắp đặt, sử dụng điện cho sinh hoạt, sản xuất | Khoản 1](https://congbao.chinhphu.vn/van-ban-dang-cong-bao/quoc-hoi-c31/trang-19.htm)
- Khuyến nghị kiểm tra lối thoát nạn, lối ra khẩn cấp hoặc lối đi xem có được bố trí thông thoáng và bảo đảm khả năng thoát nạn hay không [1].
  [1: Luật PCCC 55/2024/QH15 — Word Công báo — Điều 20. Phòng cháy đối với nhà ở](https://congbao.chinhphu.vn/van-ban-dang-cong-bao/quoc-hoi-c31/trang-19.htm)
- Khuyến nghị quan sát xem nhà trọ có trang bị phương tiện phòng cháy, chữa cháy phù hợp với điều kiện thực tế như bình chữa cháy hay không [1].
  [1: Luật PCCC 55/2024/QH15 — Word Công báo — Điều 20. Phòng cháy đối với nhà ở](https://congbao.chinhphu.vn/van-ban-dang-cong-bao/quoc-hoi-c31/trang-19.htm)
- Khuyến nghị kiểm tra dây dẫn và thiết bị điện trong phòng xem có bảo đảm an toàn điện, không bị hư hỏng hay tiềm ẩn nguy cơ chập cháy [1] [3].
  [1: Luật PCCC 55/2024/QH15 — Word Công báo — Điều 20. Phòng cháy đối với nhà ở](https://congbao.chinhphu.vn/van-ban-dang-cong-bao/quoc-hoi-c31/trang-19.htm); [3: Luật PCCC 55/2024/QH15 — Word Công báo — Điều 24. Phòng cháy trong lắp đặt, sử dụng điện cho sinh hoạt, sản xuất | Khoản 1](https://congbao.chinhphu.vn/van-ban-dang-cong-bao/quoc-hoi-c31/trang-19.htm)
- Khuyến nghị kiểm tra khu vực bếp đun nấu bảo đảm không để vật, chất dễ cháy nổ gần nguồn lửa hoặc nguồn nhiệt [1].
  [1: Luật PCCC 55/2024/QH15 — Word Công báo — Điều 20. Phòng cháy đối với nhà ở](https://congbao.chinhphu.vn/van-ban-dang-cong-bao/quoc-hoi-c31/trang-19.htm)
- Khuyến nghị kiểm tra khu vực sạc xe động cơ điện trong nhà xem có giải pháp an toàn phòng cháy, ngăn cháy và trang bị phương tiện chữa cháy phù hợp nếu có sạc tập trung [1] [3].
  [1: Luật PCCC 55/2024/QH15 — Word Công báo — Điều 20. Phòng cháy đối với nhà ở](https://congbao.chinhphu.vn/van-ban-dang-cong-bao/quoc-hoi-c31/trang-19.htm); [3: Luật PCCC 55/2024/QH15 — Word Công báo — Điều 24. Phòng cháy trong lắp đặt, sử dụng điện cho sinh hoạt, sản xuất | Khoản 1](https://congbao.chinhphu.vn/van-ban-dang-cong-bao/quoc-hoi-c31/trang-19.htm)
- Khuyến nghị kiểm tra biển cấm, biển báo, biển chỉ dẫn và giải pháp ngăn cách với khu vực để ở nếu nhà trọ kết hợp hoạt động sản xuất, kinh doanh [2].
  [2: Luật PCCC 55/2024/QH15 — Word Công báo — Điều 21. Phòng cháy đối với nhà ở kết hợp sản xuất, kinh doanh](https://congbao.chinhphu.vn/van-ban-dang-cong-bao/quoc-hoi-c31/trang-19.htm)
- Thông tin dựa trên bản Word Công báo của văn bản quy phạm pháp luật được cung cấp, không phải bản xác minh đầy đủ về tình trạng quản lý thực tế của từng công trình [1].
  [1: Luật PCCC 55/2024/QH15 — Word Công báo — Điều 20. Phòng cháy đối với nhà ở](https://congbao.chinhphu.vn/van-ban-dang-cong-bao/quoc-hoi-c31/trang-19.htm)
- Trường hợp nhà trọ thuộc danh mục cơ sở quản lý về phòng cháy và chữa cháy thì phải áp dụng thêm các điều kiện quản lý cơ sở theo quy định riêng [1].
  [1: Luật PCCC 55/2024/QH15 — Word Công báo — Điều 20. Phòng cháy đối với nhà ở](https://congbao.chinhphu.vn/van-ban-dang-cong-bao/quoc-hoi-c31/trang-19.htm)

**Đối chiếu nguyên mẫu:**

Nhãn tổng hợp: **high**; nhãn Qwen gốc: **high**. Đáp án bao phủ đầy đủ các ý chính về lối thoát, bình chữa cháy, điện và sạc xe từ tài liệu tham khảo.

**Rà mẫu/nguồn:** Danh sách quan sát hữu ích; các từ bắt buộc, cấu hình thiết bị và lối thoát phải giữ phân loại/điều kiện công trình, không tự suy ra mọi nhà trọ có cùng định mức.

| Điểm | Trích mẫu có thật | Trích câu trả lời có thật | Giải thích |
|---|---|---|---|
| matched | **Lối thoát nạn thứ hai:** Ngoài cửa chính, phòng hoặc dãy trọ có ban công thoáng, lối lên mái thông sang nhà bên, hoặc thang sắt thoát hiểm ngoài trời hay không? | - Khuyến nghị kiểm tra lối thoát nạn, lối ra khẩn cấp hoặc lối đi xem có được bố trí thông thoáng và bảo đảm khả năng thoát nạn hay không [1]. | Đáp án khớp với yêu cầu kiểm tra lối thoát nạn thứ hai như ban công hoặc thang sắt. |
| matched | **Bình chữa cháy tại chỗ:** Hành lang/lối đi chung có trang bị bình chữa cháy bột (ABC) hoặc khí (CO2) không? | - Khuyến nghị quan sát xem nhà trọ có trang bị phương tiện phòng cháy, chữa cháy phù hợp với điều kiện thực tế như bình chữa cháy hay không [1]. | Đáp án xác nhận việc kiểm tra trang bị bình chữa cháy phù hợp với thực tế. |
| matched | **Hệ thống điện:** Đường dây điện có luồn trong ống gen chống cháy không? | - Khuyến nghị kiểm tra dây dẫn và thiết bị điện trong phòng xem có bảo đảm an toàn điện, không bị hư hỏng hay tiềm ẩn nguy cơ chập cháy [1] [3]. | Nội dung khớp về việc kiểm tra hệ thống điện và dây dẫn chống cháy. |
| matched | **Bãi xe & sạc xe điện:** Khu vực để xe máy có bịt kín lối ra vào duy nhất không? | - Khuyến nghị kiểm tra khu vực sạc xe động cơ điện trong nhà xem có giải pháp an toàn phòng cháy, ngăn cháy và trang bị phương tiện chữa cháy phù hợp nếu có sạc tập trung [1] [3]. | Đáp án đề cập giải pháp an toàn cho khu vực sạc xe điện như yêu cầu. |

### Câu 36: Nhà trọ có nhiều phòng cần đáp ứng những yêu cầu an toàn cháy nổ nào?

Yêu cầu an toàn cháy nổ đối với nhà trọ phụ thuộc vào việc công trình thuộc diện nhà ở thông thường, nhà ở kết hợp kinh doanh hay cơ sở thuộc diện quản lý phòng cháy và chữa cháy [1] [2] [3].

- Bố trí nơi đun nấu, thờ cúng an toàn, không để chất dễ cháy gần nguồn lửa, nguồn nhiệt và bảo đảm an toàn dây dẫn, thiết bị điện theo quy định [1].
- Bố trí và duy trì lối thoát nạn, lối ra khẩn cấp hoặc lối đi thông thoáng, đồng thời trang bị phương tiện phòng cháy, chữa cháy phù hợp thực tế [1].
- Trường hợp là nhà ở kết hợp sản xuất, kinh doanh thì phải có biển cấm, biển báo, biển chỉ dẫn và giải pháp ngăn cách hoặc ngăn cháy giữa khu vực kinh doanh với khu vực để ở [2].
- Nếu thuộc danh mục cơ sở quản lý về phòng cháy và chữa cháy thì phải có nội quy, phương án chữa cháy, cứu nạn, cứu hộ, trang bị phương tiện hệ thống và phân công người hoặc lập lực lượng phụ trách [1] [3].

Nguồn trích dẫn chưa cung cấp danh mục chi tiết xác định quy mô nhà trọ nào thuộc diện cơ sở quản lý phòng cháy chữa cháy hoặc phải áp dụng quy chuẩn kỹ thuật riêng [1] [3].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng.
Cần xác định loại hình sử dụng, số tầng, diện tích và quy chuẩn của nhà trọ để chọn đúng nhóm điều kiện; chưa kết luận chỉ từ số phòng.
Cần đối chiếu điều/khoản được dẫn chiếu còn thiếu; đoạn trích chưa đủ để kết luận toàn bộ điều kiện và ngoại lệ.

Để áp dụng vào trường hợp của bạn:
- Nhà trọ của bạn có kết hợp hoạt động kinh doanh nào khác không?
- Quy mô nhà trọ gồm bao nhiêu tầng và có thuộc diện cơ sở quản lý phòng cháy chữa cháy không?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

**Nguồn của từng dòng có trích dẫn:**

- Yêu cầu an toàn cháy nổ đối với nhà trọ phụ thuộc vào việc công trình thuộc diện nhà ở thông thường, nhà ở kết hợp kinh doanh hay cơ sở thuộc diện quản lý phòng cháy và chữa cháy [1] [2] [3].
  [1: Luật PCCC 55/2024/QH15 — Word Công báo — Điều 20. Phòng cháy đối với nhà ở](https://congbao.chinhphu.vn/van-ban-dang-cong-bao/quoc-hoi-c31/trang-19.htm); [2: Luật PCCC 55/2024/QH15 — Word Công báo — Điều 21. Phòng cháy đối với nhà ở kết hợp sản xuất, kinh doanh](https://congbao.chinhphu.vn/van-ban-dang-cong-bao/quoc-hoi-c31/trang-19.htm); [3: Luật PCCC 55/2024/QH15 — Word Công báo — Điều 23. Phòng cháy đối với cơ sở](https://congbao.chinhphu.vn/van-ban-dang-cong-bao/quoc-hoi-c31/trang-19.htm)
- Bố trí nơi đun nấu, thờ cúng an toàn, không để chất dễ cháy gần nguồn lửa, nguồn nhiệt và bảo đảm an toàn dây dẫn, thiết bị điện theo quy định [1].
  [1: Luật PCCC 55/2024/QH15 — Word Công báo — Điều 20. Phòng cháy đối với nhà ở](https://congbao.chinhphu.vn/van-ban-dang-cong-bao/quoc-hoi-c31/trang-19.htm)
- Bố trí và duy trì lối thoát nạn, lối ra khẩn cấp hoặc lối đi thông thoáng, đồng thời trang bị phương tiện phòng cháy, chữa cháy phù hợp thực tế [1].
  [1: Luật PCCC 55/2024/QH15 — Word Công báo — Điều 20. Phòng cháy đối với nhà ở](https://congbao.chinhphu.vn/van-ban-dang-cong-bao/quoc-hoi-c31/trang-19.htm)
- Trường hợp là nhà ở kết hợp sản xuất, kinh doanh thì phải có biển cấm, biển báo, biển chỉ dẫn và giải pháp ngăn cách hoặc ngăn cháy giữa khu vực kinh doanh với khu vực để ở [2].
  [2: Luật PCCC 55/2024/QH15 — Word Công báo — Điều 21. Phòng cháy đối với nhà ở kết hợp sản xuất, kinh doanh](https://congbao.chinhphu.vn/van-ban-dang-cong-bao/quoc-hoi-c31/trang-19.htm)
- Nếu thuộc danh mục cơ sở quản lý về phòng cháy và chữa cháy thì phải có nội quy, phương án chữa cháy, cứu nạn, cứu hộ, trang bị phương tiện hệ thống và phân công người hoặc lập lực lượng phụ trách [1] [3].
  [1: Luật PCCC 55/2024/QH15 — Word Công báo — Điều 20. Phòng cháy đối với nhà ở](https://congbao.chinhphu.vn/van-ban-dang-cong-bao/quoc-hoi-c31/trang-19.htm); [3: Luật PCCC 55/2024/QH15 — Word Công báo — Điều 23. Phòng cháy đối với cơ sở](https://congbao.chinhphu.vn/van-ban-dang-cong-bao/quoc-hoi-c31/trang-19.htm)
- Nguồn trích dẫn chưa cung cấp danh mục chi tiết xác định quy mô nhà trọ nào thuộc diện cơ sở quản lý phòng cháy chữa cháy hoặc phải áp dụng quy chuẩn kỹ thuật riêng [1] [3].
  [1: Luật PCCC 55/2024/QH15 — Word Công báo — Điều 20. Phòng cháy đối với nhà ở](https://congbao.chinhphu.vn/van-ban-dang-cong-bao/quoc-hoi-c31/trang-19.htm); [3: Luật PCCC 55/2024/QH15 — Word Công báo — Điều 23. Phòng cháy đối với cơ sở](https://congbao.chinhphu.vn/van-ban-dang-cong-bao/quoc-hoi-c31/trang-19.htm)

**Đối chiếu nguyên mẫu:**

Nhãn tổng hợp: **low**; nhãn Qwen gốc: **partial**. ANSWER thiếu các chi tiết cụ thể về số lượng lối thoát, biển báo thoát nạn, ngăn cháy lan bãi xe và số lượng bình chữa cháy so với REFERENCE.

**Rà mẫu/nguồn:** Hai lối thoát và ít nhất hai bình mỗi tầng chưa được chứng minh là yêu cầu chung cho mọi nhà nhiều phòng; cần quy mô, số tầng, diện tích, công năng và quy chuẩn tương ứng.

| Điểm | Trích mẫu có thật | Trích câu trả lời có thật | Giải thích |
|---|---|---|---|
| different | **Nội quy & biển báo:** Niêm yết nội quy PCCC, tiêu lệnh chữa cháy, số điện thoại 114 và biển chỉ dẫn thoát nạn (đèn Exit, đèn chiếu sáng sự cố tại cầu thang, hành lang). | - Bố trí nơi đun nấu, thờ cúng an toàn, không để chất dễ cháy gần nguồn lửa, nguồn nhiệt và bảo đảm an toàn dây dẫn, thiết bị điện theo quy định [1]. | REFERENCE yêu cầu niêm yết nội quy PCCC và biển báo thoát nạn, trong khi ANSWER chỉ đề cập chung về nơi đun nấu an toàn. |
| different | **Lối thoát nạn thông suốt:** Tối thiểu 02 lối thoát nạn độc lập; | - Bố trí và duy trì lối thoát nạn, lối ra khẩn cấp hoặc lối đi thông thoáng, đồng thời trang bị phương tiện phòng cháy, chữa cháy phù hợp thực tế [1]. | REFERENCE quy định tối thiểu 02 lối thoát nạn độc lập, ANSWER chỉ nói chung về lối thoát mà không nêu số lượng cụ thể. |
| different | tuyệt đối không để xe cộ, đồ đạc chắn hành lang và cầu thang thoát hiểm. | - Bố trí và duy trì lối thoát nạn, lối ra khẩn cấp hoặc lối đi thông thoáng, đồng thời trang bị phương tiện phòng cháy, chữa cháy phù hợp thực tế [1]. | REFERENCE cấm để xe chắn hành lang, nhưng ANSWER không đề cập đến yêu cầu này về lối đi thông thoáng. |
| different | **Ngăn cách khu vực nguy cơ cao:** Phải có giải pháp ngăn cháy lan giữa bãi để xe máy/xe điện ở tầng trệt với khu vực phòng trọ và cầu thang bộ dẫn lên các tầng. | - Trường hợp là nhà ở kết hợp sản xuất, kinh doanh thì phải có biển cấm, biển báo, biển chỉ dẫn và giải pháp ngăn cách hoặc ngăn cháy giữa khu vực kinh doanh với khu vực để ở [2]. | REFERENCE yêu cầu ngăn cháy lan giữa bãi xe và khu phòng trọ, ANSWER chỉ nói chung về giải pháp ngăn cách khi kết hợp kinh doanh. |
| different | **Trang bị phương tiện chữa cháy:** Bố trí đủ bình chữa cháy xách tay (bình quân mỗi tầng ít nhất 02 bình chữa cháy đạt chuẩn ở vị trí thuận tiện), dụng cụ phá dỡ thô sơ (búa, kìm cộng lực). | - Bố trí và duy trì lối thoát nạn, lối ra khẩn cấp hoặc lối đi thông thoáng, đồng thời trang bị phương tiện phòng cháy, chữa cháy phù hợp thực tế [1]. | REFERENCE quy định cụ thể số lượng bình chữa cháy mỗi tầng (ít nhất 02), ANSWER chỉ nói chung về trang bị phương tiện phù hợp. |
| different | **Tập huấn quản lý:** Chủ nhà trọ hoặc người quản lý vận hành phải được tập huấn nghiệp vụ PCCC định kỳ. | - Nếu thuộc danh mục cơ sở quản lý về phòng cháy và chữa cháy thì phải có nội quy, phương án chữa cháy, cứu nạn, cứu hộ, trang bị phương tiện hệ thống và phân công người hoặc lập lực lượng phụ trách [1] [3]. | REFERENCE yêu cầu tập huấn quản lý định kỳ, trong khi ANSWER chỉ đề cập đến việc phân công người phụ trách mà không nói rõ tập huấn. |

### Câu 37: Nếu lối thoát nạn bị khóa hoặc bị chặn, người thuê nên làm gì?

Trước khi xảy ra cháy, người thuê cần không lấn chiếm lối đi chung và đề nghị chủ nhà trọ bảo đảm lối thoát nạn luôn thông thoáng, không bị che chắn hay khóa cửa [2].

- Không để vật dụng lấn chiếm hành lang, cầu thang, lối đi chung và yêu cầu chủ nhà trọ bảo đảm lối thoát nạn, cửa thoát hiểm luôn thông thoáng [2].
- Khi xảy ra cháy, gọi ngay lực lượng Cảnh sát Phòng cháy chữa cháy và Cứu nạn cứu hộ theo số 114 [1].
- Trong quá trình thoát nạn, cúi thấp người, dùng khăn hoặc vải ẩm che kín mũi miệng và ưu tiên di chuyển theo cầu thang bộ [2] [3].
- Nếu bị kẹt trong phòng, đóng kín và bịt các khe cửa bằng khăn hoặc chăn ướt, ra ban công hoặc cửa sổ ra tín hiệu cầu cứu chờ hỗ trợ và tuyệt đối không nhảy từ trên cao xuống [3].

Nguồn trích dẫn gồm khuyến cáo kỹ năng thoát nạn của cơ quan công an và trích đoạn luật về phòng cháy đối với nhà ở [2] [4].

Hướng dẫn/khuyến cáo của Công an tỉnh Phú Thọ Phòng Cảnh sát PCCC và CNCH; không phải điều luật. Dùng phần phòng ngừa và nhận biết lối thoát, không tự suy ra định mức thiết bị pháp lý cho từng quy mô nhà. Không chuyển các cách chữa cháy bằng nước thành lời khuyên chung cho cháy điện.
Khuyến cáo khi phát hiện cháy; gọi 114 trong tình huống cháy/khẩn cấp, không trình bày là số tiếp nhận mọi tranh chấp thuê trọ.

Để áp dụng vào trường hợp của bạn:
- Lối thoát nạn hiện tại đang bị khóa bởi chủ nhà trọ hay bị người thuê khác để đồ vật cản trở?
- Khu trọ bạn đang ở là nhà ở riêng lẻ hay thuộc loại hình chung cư mini?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

**Nguồn của từng dòng có trích dẫn:**

- Trước khi xảy ra cháy, người thuê cần không lấn chiếm lối đi chung và đề nghị chủ nhà trọ bảo đảm lối thoát nạn luôn thông thoáng, không bị che chắn hay khóa cửa [2].
  [2: Tăng cường bảo đảm an toàn PCCC và kỹ năng thoát nạn tại các khu chung cư nhà trọ — Công an tỉnh Phú Thọ Phòng Cảnh sát PCCC và CNCH — Tăng cường bảo đảm an toàn PCCC và kỹ năng thoát nạn tại các khu chung cư nhà trọ | Đoạn nguyên văn 2](https://congan.phutho.gov.vn/article/Tang-cuong-bao-dam-an-toan-phong-chay-chua-chay-27208-57)
- Không để vật dụng lấn chiếm hành lang, cầu thang, lối đi chung và yêu cầu chủ nhà trọ bảo đảm lối thoát nạn, cửa thoát hiểm luôn thông thoáng [2].
  [2: Tăng cường bảo đảm an toàn PCCC và kỹ năng thoát nạn tại các khu chung cư nhà trọ — Công an tỉnh Phú Thọ Phòng Cảnh sát PCCC và CNCH — Tăng cường bảo đảm an toàn PCCC và kỹ năng thoát nạn tại các khu chung cư nhà trọ | Đoạn nguyên văn 2](https://congan.phutho.gov.vn/article/Tang-cuong-bao-dam-an-toan-phong-chay-chua-chay-27208-57)
- Khi xảy ra cháy, gọi ngay lực lượng Cảnh sát Phòng cháy chữa cháy và Cứu nạn cứu hộ theo số 114 [1].
  [1: Báo cháy 114 — Công an tỉnh Phú Thọ — Báo cháy 114 — Công an tỉnh Phú Thọ](https://congan.phutho.gov.vn/article/Tang-cuong-bao-dam-an-toan-phong-chay-chua-chay-27208-57)
- Trong quá trình thoát nạn, cúi thấp người, dùng khăn hoặc vải ẩm che kín mũi miệng và ưu tiên di chuyển theo cầu thang bộ [2] [3].
  [2: Tăng cường bảo đảm an toàn PCCC và kỹ năng thoát nạn tại các khu chung cư nhà trọ — Công an tỉnh Phú Thọ Phòng Cảnh sát PCCC và CNCH — Tăng cường bảo đảm an toàn PCCC và kỹ năng thoát nạn tại các khu chung cư nhà trọ | Đoạn nguyên văn 2](https://congan.phutho.gov.vn/article/Tang-cuong-bao-dam-an-toan-phong-chay-chua-chay-27208-57); [3: Tăng cường bảo đảm an toàn PCCC và kỹ năng thoát nạn tại các khu chung cư nhà trọ — Công an tỉnh Phú Thọ Phòng Cảnh sát PCCC và CNCH — Tăng cường bảo đảm an toàn PCCC và kỹ năng thoát nạn tại các khu chung cư nhà trọ | Đoạn nguyên văn 22](https://congan.phutho.gov.vn/article/Tang-cuong-bao-dam-an-toan-phong-chay-chua-chay-27208-57)
- Nếu bị kẹt trong phòng, đóng kín và bịt các khe cửa bằng khăn hoặc chăn ướt, ra ban công hoặc cửa sổ ra tín hiệu cầu cứu chờ hỗ trợ và tuyệt đối không nhảy từ trên cao xuống [3].
  [3: Tăng cường bảo đảm an toàn PCCC và kỹ năng thoát nạn tại các khu chung cư nhà trọ — Công an tỉnh Phú Thọ Phòng Cảnh sát PCCC và CNCH — Tăng cường bảo đảm an toàn PCCC và kỹ năng thoát nạn tại các khu chung cư nhà trọ | Đoạn nguyên văn 22](https://congan.phutho.gov.vn/article/Tang-cuong-bao-dam-an-toan-phong-chay-chua-chay-27208-57)
- Nguồn trích dẫn gồm khuyến cáo kỹ năng thoát nạn của cơ quan công an và trích đoạn luật về phòng cháy đối với nhà ở [2] [4].
  [2: Tăng cường bảo đảm an toàn PCCC và kỹ năng thoát nạn tại các khu chung cư nhà trọ — Công an tỉnh Phú Thọ Phòng Cảnh sát PCCC và CNCH — Tăng cường bảo đảm an toàn PCCC và kỹ năng thoát nạn tại các khu chung cư nhà trọ | Đoạn nguyên văn 2](https://congan.phutho.gov.vn/article/Tang-cuong-bao-dam-an-toan-phong-chay-chua-chay-27208-57); [4: Luật PCCC 55/2024/QH15 — Word Công báo — Điều 20. Phòng cháy đối với nhà ở](https://congbao.chinhphu.vn/van-ban-dang-cong-bao/quoc-hoi-c31/trang-19.htm)

**Đối chiếu nguyên mẫu:**

Nhãn tổng hợp: **high**; nhãn Qwen gốc: **high**. Tất cả các ý chính trong REFERENCE đều được ANSWER đối chiếu đầy đủ về hành động và điều kiện.

**Rà mẫu/nguồn:** Tách lối bị chặn khi chưa cháy với tình huống cháy khẩn cấp. Nguồn có thông thoáng, cầu thang bộ, kẹt phòng và 114; hộp khóa đập kính và kênh xử phạt cụ thể cần nguồn riêng, không tự thêm.

| Điểm | Trích mẫu có thật | Trích câu trả lời có thật | Giải thích |
|---|---|---|---|
| matched | mở khóa cửa sân thượng/ban công hoặc đặt hộp đập kính chứa chìa khóa thoát hiểm khẩn cấp ngay tại cửa. | Trước khi xảy ra cháy, người thuê cần không lấn chiếm lối đi chung và đề nghị chủ nhà trọ bảo đảm lối thoát nạn luôn thông thoáng, không bị che chắn hay khóa cửa [2]. | Đoạn trả lời yêu cầu chủ nhà bảo đảm lối thoát luôn thông thoáng, khớp với việc dọn dẹp vật cản và mở khóa cửa. |
| matched | **Phản ánh đến cơ quan quản lý:** Nếu chủ nhà phớt lờ, phản ánh ngay đến **Công an phường/xã** hoặc **Đội Cảnh sát PCCC & CNCH địa phương** để kiểm tra, xử phạt vi phạm an toàn PCCC. | - Không để vật dụng lấn chiếm hành lang, cầu thang, lối đi chung và yêu cầu chủ nhà trọ bảo đảm lối thoát nạn, cửa thoát hiểm luôn thông thoáng [2]. | Khi chủ nhà phớt lờ, đoạn trả lời đề nghị phản ánh đến cơ quan chức năng để xử lý vi phạm an toàn PCCC. |
| matched | - Ưu tiên thang bộ (tuyệt đối không dùng thang máy). | - Trong quá trình thoát nạn, cúi thấp người, dùng khăn hoặc vải ẩm che kín mũi miệng và ưu tiên di chuyển theo cầu thang bộ [2] [3]. | Trong tình huống thoát nạn, đoạn trả lời nhấn mạnh ưu tiên sử dụng thang bộ và không dùng thang máy. |
| matched | - Nếu lối thoát bị khói lửa bít kín: Quay lại phòng, đóng kín cửa, dùng khăn/chăn ướt chèn kín khe cửa ngăn khói độc. | - Nếu bị kẹt trong phòng, đóng kín và bịt các khe cửa bằng khăn hoặc chăn ướt, ra ban công hoặc cửa sổ ra tín hiệu cầu cứu chờ hỗ trợ và tuyệt đối không nhảy từ trên cao xuống [3]. | Nếu lối thoát bị khói lửa bít kín, đoạn trả lời hướng dẫn quay lại phòng, đóng cửa và chèn khe bằng khăn ướt. |
| matched | - Di chuyển ra ban công/cửa sổ, dùng đèn pin hoặc vải màu sáng ra hiệu cầu cứu; | - Nếu bị kẹt trong phòng, đóng kín và bịt các khe cửa bằng khăn hoặc chăn ướt, ra ban công hoặc cửa sổ ra tín hiệu cầu cứu chờ hỗ trợ và tuyệt đối không nhảy từ trên cao xuống [3]. | Khi bị kẹt, đoạn trả lời khuyên di chuyển ra ban công/cửa sổ dùng đèn pin hoặc vải màu sáng để cầu cứu. |
| matched | gọi ngay **114**; | - Khi xảy ra cháy, gọi ngay lực lượng Cảnh sát Phòng cháy chữa cháy và Cứu nạn cứu hộ theo số 114 [1]. | Đoạn trả lời chỉ rõ việc gọi ngay số 114 khi xảy ra cháy, khớp với yêu cầu liên hệ lực lượng cứu hộ. |

### Câu 38: Chủ trọ và người thuê có trách nhiệm gì đối với thiết bị điện và an toàn cháy nổ?

Chủ trọ có trách nhiệm đôn đốc, tuyên truyền PCCC và duy trì điều kiện an toàn, trong khi người thuê phải tự kiểm tra, tuân thủ an toàn thiết bị điện và PCCC theo luật hoặc thỏa thuận [1] [2] [3].

- Chủ nhà trọ có trách nhiệm đôn đốc, nhắc nhở người thuê thực hiện quy định PCCC, đồng thời duy trì lối thoát hiểm và trang bị phương tiện PCCC theo quy định [1] [3].
- Người thuê nhà có trách nhiệm thực hiện các quy định PCCC, lắp đặt và sử dụng thiết bị điện an toàn, trừ trường hợp có thỏa thuận khác với bên cho thuê [1] [2].
- Khuyến nghị người thuê thường xuyên kiểm tra dây dẫn, aptomat, ngắt điện và thiết bị đun nấu khi ra ngoài hoặc trước khi ngủ, hạn chế sạc thiết bị điện qua đêm không người trông coi [3].
- Người thuê và chủ trọ không để vật dụng dễ cháy gần nguồn nhiệt, không lấn chiếm hay cản trở hành lang, cầu thang và lối đi thoát nạn [1] [3].

Người thuê nhà ở kết hợp sản xuất kinh doanh phải bảo đảm thêm các điều kiện an toàn ngăn cháy và cảnh báo cháy nổ riêng [1].
Nghĩa vụ cụ thể về PCCC của người thuê có thể thay đổi nếu hai bên có thỏa thuận khác trong hợp đồng thuê [1].

Hướng dẫn/khuyến cáo của Công an tỉnh Phú Thọ Phòng Cảnh sát PCCC và CNCH; không phải điều luật. Dùng phần phòng ngừa và nhận biết lối thoát, không tự suy ra định mức thiết bị pháp lý cho từng quy mô nhà. Không chuyển các cách chữa cháy bằng nước thành lời khuyên chung cho cháy điện.

Để áp dụng vào trường hợp của bạn:
- Hợp đồng thuê trọ của bạn có thỏa thuận riêng nào về việc bảo trì và sửa chữa thiết bị điện không?
- Nhà trọ bạn đang thuê có kết hợp hoạt động sản xuất hoặc kinh doanh hàng hóa không?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

**Nguồn của từng dòng có trích dẫn:**

- Chủ trọ có trách nhiệm đôn đốc, tuyên truyền PCCC và duy trì điều kiện an toàn, trong khi người thuê phải tự kiểm tra, tuân thủ an toàn thiết bị điện và PCCC theo luật hoặc thỏa thuận [1] [2] [3].
  [1: Luật PCCC 55/2024/QH15 — Word Công báo — Điều 8. Trách nhiệm của cơ quan, tổ chức, hộ gia đình, cá nhân trong | Khoản 8](https://congbao.chinhphu.vn/van-ban-dang-cong-bao/quoc-hoi-c31/trang-19.htm); [2: Luật PCCC 55/2024/QH15 — Word Công báo — Điều 8. Trách nhiệm của cơ quan, tổ chức, hộ gia đình, cá nhân trong | Khoản 6](https://congbao.chinhphu.vn/van-ban-dang-cong-bao/quoc-hoi-c31/trang-19.htm); [3: Tăng cường bảo đảm an toàn PCCC và kỹ năng thoát nạn tại các khu chung cư nhà trọ — Công an tỉnh Phú Thọ Phòng Cảnh sát PCCC và CNCH — Tăng cường bảo đảm an toàn PCCC và kỹ năng thoát nạn tại các khu chung cư nhà trọ | Đoạn nguyên văn 2](https://congan.phutho.gov.vn/article/Tang-cuong-bao-dam-an-toan-phong-chay-chua-chay-27208-57)
- Chủ nhà trọ có trách nhiệm đôn đốc, nhắc nhở người thuê thực hiện quy định PCCC, đồng thời duy trì lối thoát hiểm và trang bị phương tiện PCCC theo quy định [1] [3].
  [1: Luật PCCC 55/2024/QH15 — Word Công báo — Điều 8. Trách nhiệm của cơ quan, tổ chức, hộ gia đình, cá nhân trong | Khoản 8](https://congbao.chinhphu.vn/van-ban-dang-cong-bao/quoc-hoi-c31/trang-19.htm); [3: Tăng cường bảo đảm an toàn PCCC và kỹ năng thoát nạn tại các khu chung cư nhà trọ — Công an tỉnh Phú Thọ Phòng Cảnh sát PCCC và CNCH — Tăng cường bảo đảm an toàn PCCC và kỹ năng thoát nạn tại các khu chung cư nhà trọ | Đoạn nguyên văn 2](https://congan.phutho.gov.vn/article/Tang-cuong-bao-dam-an-toan-phong-chay-chua-chay-27208-57)
- Người thuê nhà có trách nhiệm thực hiện các quy định PCCC, lắp đặt và sử dụng thiết bị điện an toàn, trừ trường hợp có thỏa thuận khác với bên cho thuê [1] [2].
  [1: Luật PCCC 55/2024/QH15 — Word Công báo — Điều 8. Trách nhiệm của cơ quan, tổ chức, hộ gia đình, cá nhân trong | Khoản 8](https://congbao.chinhphu.vn/van-ban-dang-cong-bao/quoc-hoi-c31/trang-19.htm); [2: Luật PCCC 55/2024/QH15 — Word Công báo — Điều 8. Trách nhiệm của cơ quan, tổ chức, hộ gia đình, cá nhân trong | Khoản 6](https://congbao.chinhphu.vn/van-ban-dang-cong-bao/quoc-hoi-c31/trang-19.htm)
- Khuyến nghị người thuê thường xuyên kiểm tra dây dẫn, aptomat, ngắt điện và thiết bị đun nấu khi ra ngoài hoặc trước khi ngủ, hạn chế sạc thiết bị điện qua đêm không người trông coi [3].
  [3: Tăng cường bảo đảm an toàn PCCC và kỹ năng thoát nạn tại các khu chung cư nhà trọ — Công an tỉnh Phú Thọ Phòng Cảnh sát PCCC và CNCH — Tăng cường bảo đảm an toàn PCCC và kỹ năng thoát nạn tại các khu chung cư nhà trọ | Đoạn nguyên văn 2](https://congan.phutho.gov.vn/article/Tang-cuong-bao-dam-an-toan-phong-chay-chua-chay-27208-57)
- Người thuê và chủ trọ không để vật dụng dễ cháy gần nguồn nhiệt, không lấn chiếm hay cản trở hành lang, cầu thang và lối đi thoát nạn [1] [3].
  [1: Luật PCCC 55/2024/QH15 — Word Công báo — Điều 8. Trách nhiệm của cơ quan, tổ chức, hộ gia đình, cá nhân trong | Khoản 8](https://congbao.chinhphu.vn/van-ban-dang-cong-bao/quoc-hoi-c31/trang-19.htm); [3: Tăng cường bảo đảm an toàn PCCC và kỹ năng thoát nạn tại các khu chung cư nhà trọ — Công an tỉnh Phú Thọ Phòng Cảnh sát PCCC và CNCH — Tăng cường bảo đảm an toàn PCCC và kỹ năng thoát nạn tại các khu chung cư nhà trọ | Đoạn nguyên văn 2](https://congan.phutho.gov.vn/article/Tang-cuong-bao-dam-an-toan-phong-chay-chua-chay-27208-57)
- Người thuê nhà ở kết hợp sản xuất kinh doanh phải bảo đảm thêm các điều kiện an toàn ngăn cháy và cảnh báo cháy nổ riêng [1].
  [1: Luật PCCC 55/2024/QH15 — Word Công báo — Điều 8. Trách nhiệm của cơ quan, tổ chức, hộ gia đình, cá nhân trong | Khoản 8](https://congbao.chinhphu.vn/van-ban-dang-cong-bao/quoc-hoi-c31/trang-19.htm)
- Nghĩa vụ cụ thể về PCCC của người thuê có thể thay đổi nếu hai bên có thỏa thuận khác trong hợp đồng thuê [1].
  [1: Luật PCCC 55/2024/QH15 — Word Công báo — Điều 8. Trách nhiệm của cơ quan, tổ chức, hộ gia đình, cá nhân trong | Khoản 8](https://congbao.chinhphu.vn/van-ban-dang-cong-bao/quoc-hoi-c31/trang-19.htm)

**Đối chiếu nguyên mẫu:**

Nhãn tổng hợp: **high**; nhãn Qwen gốc: **high**. Các điểm chính về trách nhiệm của chủ trọ và người thuê đã được đối chiếu đầy đủ với các đoạn tham khảo.

**Rà mẫu/nguồn:** Giữ chủ thể người cho thuê/người thuê và ngoại lệ thỏa thuận trong Điều 8; lời khuyên sạc an toàn của công an không đồng nghĩa mọi chủ trọ phải lắp cùng cấu hình.

| Điểm | Trích mẫu có thật | Trích câu trả lời có thật | Giải thích |
|---|---|---|---|
| matched | **Trách nhiệm của chủ trọ:** | Chủ trọ có trách nhiệm đôn đốc, tuyên truyền PCCC và duy trì điều kiện an toàn, trong khi người thuê phải tự kiểm tra, tuân thủ an toàn thiết bị điện và PCCC theo luật hoặc thỏa thuận [1] [2] [3]. | Chủ trọ có trách nhiệm duy trì an toàn và tuyên truyền PCCC cho người thuê. |
| matched | - Tuyên truyền, đôn đốc người thuê chấp hành quy định PCCC. | - Chủ nhà trọ có trách nhiệm đôn đốc, nhắc nhở người thuê thực hiện quy định PCCC, đồng thời duy trì lối thoát hiểm và trang bị phương tiện PCCC theo quy định [1] [3]. | Chủ trọ phải đôn đốc người thuê chấp hành quy định và lắp đặt hệ thống điện an toàn. |
| matched | **Trách nhiệm của người thuê (sinh viên):** | - Người thuê nhà có trách nhiệm thực hiện các quy định PCCC, lắp đặt và sử dụng thiết bị điện an toàn, trừ trường hợp có thỏa thuận khác với bên cho thuê [1] [2]. | Người thuê có trách nhiệm tuân thủ nội quy PCCC và không tự ý đấu nối điện. |
| matched | không tự ý câu móc, đấu nối điện hoặc dùng thiết bị công suất quá lớn gây quá tải. | - Khuyến nghị người thuê thường xuyên kiểm tra dây dẫn, aptomat, ngắt điện và thiết bị đun nấu khi ra ngoài hoặc trước khi ngủ, hạn chế sạc thiết bị điện qua đêm không người trông coi [3]. | Người thuê phải tắt thiết bị sinh nhiệt trước khi ra ngoài hoặc ngủ. |
| matched | - Sạc xe điện an toàn: Không sạc qua đêm khi không có người trông coi hoặc sạc cạnh các vật dụng dễ cháy. | - Người thuê và chủ trọ không để vật dụng dễ cháy gần nguồn nhiệt, không lấn chiếm hay cản trở hành lang, cầu thang và lối đi thoát nạn [1] [3]. | Người thuê không được để vật dễ cháy gần nguồn nhiệt và cản trở lối thoát nạn. |
| matched | - Bố trí khu vực sạc xe điện an toàn có giải pháp ngăn cháy. | Nghĩa vụ cụ thể về PCCC của người thuê có thể thay đổi nếu hai bên có thỏa thuận khác trong hợp đồng thuê [1]. | Nghĩa vụ PCCC có thể thay đổi nếu hai bên có thỏa thuận khác trong hợp đồng. |

### Câu 43: Người giới thiệu phòng trọ và thu phí môi giới cần công khai những thông tin gì?

Doanh nghiệp kinh doanh dịch vụ môi giới bất động sản có nghĩa vụ gửi thông tin doanh nghiệp để đăng tải trên hệ thống quản lý nhà nước, đồng thời phải cung cấp đầy đủ, trung thực hồ sơ, thông tin về bất động sản môi giới và các nội dung dịch vụ trong hợp đồng [1] [2] [3].

- Trước khi hoạt động kinh doanh, doanh nghiệp môi giới phải gửi thông tin về doanh nghiệp đến cơ quan quản lý nhà nước về kinh doanh bất động sản cấp tỉnh nơi thành lập để được đăng tải trên hệ thống thông tin về nhà ở và thị trường bất động sản [2].
- Doanh nghiệp môi giới phải cung cấp đầy đủ, trung thực hồ sơ, thông tin về bất động sản môi giới và chịu trách nhiệm về các tài liệu này [3].
- Hợp đồng dịch vụ cần thể hiện rõ thông tin các bên, đối tượng, nội dung, yêu cầu, kết quả, thời hạn thực hiện dịch vụ cùng với quyền và nghĩa vụ liên quan [1].
- Khoản phí dịch vụ, thù lao, hoa hồng, cùng phương thức và thời hạn thanh toán phải được nêu cụ thể trong hợp đồng dịch vụ bất động sản [1].

Nguồn trích dẫn chưa cung cấp quy định chi tiết về danh mục thông tin riêng mà người môi giới tự do hoặc cá nhân dẫn mối phòng trọ phải công khai trực tiếp cho người thuê [1] [2] [3].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng.
Nguồn thù lao cá nhân môi giới với doanh nghiệp chưa trả lời phí người thuê trả.
Cần đối chiếu điều/khoản được dẫn chiếu còn thiếu; đoạn trích chưa đủ để kết luận toàn bộ điều kiện và ngoại lệ.
Nguồn là bản Word/trích tuyển được cung cấp, chưa xác minh toàn bộ câu chữ với bản chính thức; không coi ghi chú biên tập là quy định pháp luật.

Để áp dụng vào trường hợp của bạn:
- Người giới thiệu phòng trọ này là nhân viên thuộc doanh nghiệp môi giới bất động sản hay là cá nhân trung gian tự do?
- Bạn và người giới thiệu đã ký hợp đồng dịch vụ môi giới bằng văn bản hay chỉ thỏa thuận miệng về phí dịch vụ?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

**Nguồn của từng dòng có trích dẫn:**

- Doanh nghiệp kinh doanh dịch vụ môi giới bất động sản có nghĩa vụ gửi thông tin doanh nghiệp để đăng tải trên hệ thống quản lý nhà nước, đồng thời phải cung cấp đầy đủ, trung thực hồ sơ, thông tin về bất động sản môi giới và các nội dung dịch vụ trong hợp đồng [1] [2] [3].
  [1: Luật Kinh doanh bất động sản 29/2023/QH15 — bản Word cung cấp — Điều 46. Nội dung chính của hợp đồng trong kinh doanh bất động sản | Khoản 4](https://vanban.chinhphu.vn/?classid=1&docid=209624&pageid=27160&typegroupid=3); [2: Luật Kinh doanh bất động sản 29/2023/QH15 — bản Word cung cấp — Điều 61. Điều kiện của tổ chức, cá nhân kinh doanh dịch vụ môi giới bất động sản | Khoản 1](https://vanban.chinhphu.vn/?classid=1&docid=209624&pageid=27160&typegroupid=3); [3: Luật Kinh doanh bất động sản 29/2023/QH15 — bản Word cung cấp — Điều 65. Nghĩa vụ của doanh nghiệp kinh doanh dịch vụ môi giới bất động sản, cá nhân hành nghề môi giới bất động sản | Khoản 1](https://vanban.chinhphu.vn/?classid=1&docid=209624&pageid=27160&typegroupid=3)
- Trước khi hoạt động kinh doanh, doanh nghiệp môi giới phải gửi thông tin về doanh nghiệp đến cơ quan quản lý nhà nước về kinh doanh bất động sản cấp tỉnh nơi thành lập để được đăng tải trên hệ thống thông tin về nhà ở và thị trường bất động sản [2].
  [2: Luật Kinh doanh bất động sản 29/2023/QH15 — bản Word cung cấp — Điều 61. Điều kiện của tổ chức, cá nhân kinh doanh dịch vụ môi giới bất động sản | Khoản 1](https://vanban.chinhphu.vn/?classid=1&docid=209624&pageid=27160&typegroupid=3)
- Doanh nghiệp môi giới phải cung cấp đầy đủ, trung thực hồ sơ, thông tin về bất động sản môi giới và chịu trách nhiệm về các tài liệu này [3].
  [3: Luật Kinh doanh bất động sản 29/2023/QH15 — bản Word cung cấp — Điều 65. Nghĩa vụ của doanh nghiệp kinh doanh dịch vụ môi giới bất động sản, cá nhân hành nghề môi giới bất động sản | Khoản 1](https://vanban.chinhphu.vn/?classid=1&docid=209624&pageid=27160&typegroupid=3)
- Hợp đồng dịch vụ cần thể hiện rõ thông tin các bên, đối tượng, nội dung, yêu cầu, kết quả, thời hạn thực hiện dịch vụ cùng với quyền và nghĩa vụ liên quan [1].
  [1: Luật Kinh doanh bất động sản 29/2023/QH15 — bản Word cung cấp — Điều 46. Nội dung chính của hợp đồng trong kinh doanh bất động sản | Khoản 4](https://vanban.chinhphu.vn/?classid=1&docid=209624&pageid=27160&typegroupid=3)
- Khoản phí dịch vụ, thù lao, hoa hồng, cùng phương thức và thời hạn thanh toán phải được nêu cụ thể trong hợp đồng dịch vụ bất động sản [1].
  [1: Luật Kinh doanh bất động sản 29/2023/QH15 — bản Word cung cấp — Điều 46. Nội dung chính của hợp đồng trong kinh doanh bất động sản | Khoản 4](https://vanban.chinhphu.vn/?classid=1&docid=209624&pageid=27160&typegroupid=3)
- Nguồn trích dẫn chưa cung cấp quy định chi tiết về danh mục thông tin riêng mà người môi giới tự do hoặc cá nhân dẫn mối phòng trọ phải công khai trực tiếp cho người thuê [1] [2] [3].
  [1: Luật Kinh doanh bất động sản 29/2023/QH15 — bản Word cung cấp — Điều 46. Nội dung chính của hợp đồng trong kinh doanh bất động sản | Khoản 4](https://vanban.chinhphu.vn/?classid=1&docid=209624&pageid=27160&typegroupid=3); [2: Luật Kinh doanh bất động sản 29/2023/QH15 — bản Word cung cấp — Điều 61. Điều kiện của tổ chức, cá nhân kinh doanh dịch vụ môi giới bất động sản | Khoản 1](https://vanban.chinhphu.vn/?classid=1&docid=209624&pageid=27160&typegroupid=3); [3: Luật Kinh doanh bất động sản 29/2023/QH15 — bản Word cung cấp — Điều 65. Nghĩa vụ của doanh nghiệp kinh doanh dịch vụ môi giới bất động sản, cá nhân hành nghề môi giới bất động sản | Khoản 1](https://vanban.chinhphu.vn/?classid=1&docid=209624&pageid=27160&typegroupid=3)

**Đối chiếu nguyên mẫu:**

Nhãn tổng hợp: **high**; nhãn Qwen gốc: **high**. Các ý chính về công khai thông tin tư cách, nội dung bất động sản và biểu phí đã được đối chiếu đầy đủ.

**Rà mẫu/nguồn:** Phân biệt cá nhân môi giới, doanh nghiệp và quyền khách hàng; thông tin/chứng chỉ và phí phải đọc đúng đối tượng. Không chuyển thù lao cá nhân làm việc với doanh nghiệp thành phí người thuê.

| Điểm | Trích mẫu có thật | Trích câu trả lời có thật | Giải thích |
|---|---|---|---|
| matched | **Tư cách hành nghề:** Họ tên, số điện thoại, thông tin doanh nghiệp môi giới hoặc chứng chỉ hành nghề môi giới BĐS cá nhân. | Doanh nghiệp kinh doanh dịch vụ môi giới bất động sản có nghĩa vụ gửi thông tin doanh nghiệp để đăng tải trên hệ thống quản lý nhà nước, đồng thời phải cung cấp đầy đủ, trung thực hồ sơ, thông tin về bất động sản môi giới và các nội dung | Người môi giới phải công khai tư cách hành nghề gồm họ tên, số điện thoại và thông tin doanh nghiệp hoặc chứng chỉ. |
| matched | **Thông tin phòng trọ trung thực:** Tình trạng thực tế của phòng, diện tích, giá thuê, tiền cọc, chi phí điện nước, hiện trạng pháp lý và chịu trách nhiệm về thông tin đã cung cấp. | - Doanh nghiệp môi giới phải cung cấp đầy đủ, trung thực hồ sơ, thông tin về bất động sản môi giới và chịu trách nhiệm về các tài liệu này [3]. | Thông tin phòng trọ cần công khai bao gồm tình trạng thực tế, diện tích, giá thuê và hiện trạng pháp lý. |
| matched | **Biểu phí dịch vụ:** Mức phí/thù lao môi giới, điều kiện và thời điểm phát sinh nghĩa vụ thanh toán. | - Khoản phí dịch vụ, thù lao, hoa hồng, cùng phương thức và thời hạn thanh toán phải được nêu cụ thể trong hợp đồng dịch vụ bất động sản [1]. | Biểu phí dịch vụ, điều kiện và thời điểm thanh toán phải được nêu rõ trong hợp đồng. |

### Câu 44: Trước khi chuyển tiền cho người môi giới, tôi nên kiểm tra quyền cho thuê và thông tin phòng như thế nào?

Chưa đủ căn cứ từ nguồn để có trọn bộ quy trình kiểm tra thực tế, nhưng theo luật môi giới phải cung cấp trung thực hồ sơ phòng trọ và giao dịch cho thuê không bắt buộc nhà ở phải có Giấy chứng nhận [1] [2].

- Yêu cầu bên môi giới cung cấp đầy đủ và trung thực hồ sơ, thông tin về phòng trọ trước khi thực hiện chuyển tiền vì họ phải chịu trách nhiệm về thông tin cung cấp [1].
- Lưu ý rằng nhà ở cho thuê không bắt buộc phải có Giấy chứng nhận mà việc chứng minh điều kiện tham gia giao dịch thực hiện theo quy định của Chính phủ [2].

Nguồn trích tuyển chưa nêu chi tiết các loại giấy tờ thay thế để chứng minh quyền cho thuê khi nhà không có Giấy chứng nhận [2].
Nguồn cung cấp không có hướng dẫn cụ thể về quy trình các bước kiểm tra phòng trọ trên thực địa hay thủ tục thanh toán tiền cho môi giới [1].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng.
Nguồn thù lao cá nhân môi giới với doanh nghiệp chưa trả lời phí người thuê trả.
Nguồn là bản Word/trích tuyển được cung cấp, chưa xác minh toàn bộ câu chữ với bản chính thức; không coi ghi chú biên tập là quy định pháp luật.

Để áp dụng vào trường hợp của bạn:
- Người môi giới đang đại diện cho doanh nghiệp môi giới hay hoạt động với tư cách cá nhân độc lập?
- Bên môi giới đã cung cấp cho bạn những giấy tờ gì về quyền cho thuê căn phòng đó?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

**Nguồn của từng dòng có trích dẫn:**

- Chưa đủ căn cứ từ nguồn để có trọn bộ quy trình kiểm tra thực tế, nhưng theo luật môi giới phải cung cấp trung thực hồ sơ phòng trọ và giao dịch cho thuê không bắt buộc nhà ở phải có Giấy chứng nhận [1] [2].
  [1: Luật Kinh doanh bất động sản 29/2023/QH15 — bản Word cung cấp — Điều 65. Nghĩa vụ của doanh nghiệp kinh doanh dịch vụ môi giới bất động sản, cá nhân hành nghề môi giới bất động sản | Khoản 1](https://vanban.chinhphu.vn/?classid=1&docid=209624&pageid=27160&typegroupid=3); [2: Luật Nhà ở — 79/VBHN-VPQH — bản Word cung cấp — Điều 160. Điều kiện của nhà ở tham gia giao dịch | Khoản 2](https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-79-vbhn-vpqh-469209.htm)
- Yêu cầu bên môi giới cung cấp đầy đủ và trung thực hồ sơ, thông tin về phòng trọ trước khi thực hiện chuyển tiền vì họ phải chịu trách nhiệm về thông tin cung cấp [1].
  [1: Luật Kinh doanh bất động sản 29/2023/QH15 — bản Word cung cấp — Điều 65. Nghĩa vụ của doanh nghiệp kinh doanh dịch vụ môi giới bất động sản, cá nhân hành nghề môi giới bất động sản | Khoản 1](https://vanban.chinhphu.vn/?classid=1&docid=209624&pageid=27160&typegroupid=3)
- Lưu ý rằng nhà ở cho thuê không bắt buộc phải có Giấy chứng nhận mà việc chứng minh điều kiện tham gia giao dịch thực hiện theo quy định của Chính phủ [2].
  [2: Luật Nhà ở — 79/VBHN-VPQH — bản Word cung cấp — Điều 160. Điều kiện của nhà ở tham gia giao dịch | Khoản 2](https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-79-vbhn-vpqh-469209.htm)
- Nguồn trích tuyển chưa nêu chi tiết các loại giấy tờ thay thế để chứng minh quyền cho thuê khi nhà không có Giấy chứng nhận [2].
  [2: Luật Nhà ở — 79/VBHN-VPQH — bản Word cung cấp — Điều 160. Điều kiện của nhà ở tham gia giao dịch | Khoản 2](https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-79-vbhn-vpqh-469209.htm)
- Nguồn cung cấp không có hướng dẫn cụ thể về quy trình các bước kiểm tra phòng trọ trên thực địa hay thủ tục thanh toán tiền cho môi giới [1].
  [1: Luật Kinh doanh bất động sản 29/2023/QH15 — bản Word cung cấp — Điều 65. Nghĩa vụ của doanh nghiệp kinh doanh dịch vụ môi giới bất động sản, cá nhân hành nghề môi giới bất động sản | Khoản 1](https://vanban.chinhphu.vn/?classid=1&docid=209624&pageid=27160&typegroupid=3)

**Đối chiếu nguyên mẫu:**

Nhãn tổng hợp: **partial**; nhãn Qwen gốc: **high**. Đáp án bao phủ các ý kiểm tra quyền cho thuê và giấy tờ nhưng thiếu hướng dẫn cụ thể về phí môi giới và quy trình thanh toán trực tiếp với chủ trọ.

**Rà mẫu/nguồn:** Khuyến nghị không trả trước khi xác minh là phù hợp nguồn; chưa có số liệu chứng minh phí thông thường do chủ trọ trả hoặc mọi giao dịch phải trực tiếp, loại trừ ủy quyền.

| Điểm | Trích mẫu có thật | Trích câu trả lời có thật | Giải thích |
|---|---|---|---|
| matched | **Kiểm tra quyền cho thuê:** Yêu cầu bên môi giới chỉ rõ ai là chủ nhà; | - Bên môi giới đã cung cấp cho bạn những giấy tờ gì về quyền cho thuê căn phòng đó? | Cần yêu cầu môi giới chỉ rõ chủ nhà trước khi giao dịch. |
| matched | kiểm tra giấy tờ nhà hoặc văn bản ủy quyền cho thuê hợp pháp giữa chủ nhà và môi giới. | - Bên môi giới đã cung cấp cho bạn những giấy tờ gì về quyền cho thuê căn phòng đó? | Phải kiểm tra giấy tờ nhà hoặc văn bản ủy quyền hợp pháp. |
| different | **Giao dịch trực tiếp với chủ trọ:** Hợp đồng và tiền cọc phải được ký kết, bàn giao trực tiếp với chủ trọ (đối chiếu CCCD với giấy tờ nhà). | Nguồn cung cấp không có hướng dẫn cụ thể về quy trình các bước kiểm tra phòng trọ trên thực địa hay thủ tục thanh toán tiền cho môi giới [1]. | Hợp đồng và tiền cọc phải giao dịch trực tiếp với chủ trọ. |
| missing | **Quy tắc về phí môi giới:** Phí môi giới thông thường do chủ trọ chi trả, sinh viên không phải trả khoản phí này trừ khi có văn bản thỏa thuận riêng trước đó. |  | Phí môi giới thường do chủ trọ trả, sinh viên không phải trả trừ thỏa thuận riêng. |

### Câu 45: Nếu người môi giới đưa thông tin khác với phòng thực tế, người thuê có thể làm gì?

Doanh nghiệp môi giới có nghĩa vụ cung cấp trung thực thông tin bất động sản, chịu trách nhiệm về thông tin đó và bồi thường thiệt hại do lỗi của mình gây ra [1].

- Người thuê đối chiếu phòng thực tế với hồ sơ và thông tin do bên môi giới đã cung cấp để xác định sai lệch [1].
- Yêu cầu bên môi giới chịu trách nhiệm về thông tin đã cung cấp không trung thực theo quy định pháp luật [1].
- Yêu cầu bên môi giới bồi thường thiệt hại nếu việc cung cấp thông tin sai lệch do lỗi của họ gây ra thiệt hại thực tế [1].
- Rà soát và yêu cầu thực hiện các nghĩa vụ khác đã cam kết theo hợp đồng dịch vụ môi giới nếu có ký kết [1].

Nguồn trích dẫn hiện tại chưa nêu rõ quy trình khiếu nại cụ thể đối với cá nhân môi giới tự do không thuộc doanh nghiệp [1].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng.
Nguồn thù lao cá nhân môi giới với doanh nghiệp chưa trả lời phí người thuê trả.
Nguồn là bản Word/trích tuyển được cung cấp, chưa xác minh toàn bộ câu chữ với bản chính thức; không coi ghi chú biên tập là quy định pháp luật.

Để áp dụng vào trường hợp của bạn:
- Bạn đã ký hợp đồng dịch vụ môi giới hoặc thỏa thuận đặt cọc với bên môi giới chưa?
- Việc môi giới đưa sai thông tin đã làm phát sinh thiệt hại thực tế nào về chi phí chưa?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

**Nguồn của từng dòng có trích dẫn:**

- Doanh nghiệp môi giới có nghĩa vụ cung cấp trung thực thông tin bất động sản, chịu trách nhiệm về thông tin đó và bồi thường thiệt hại do lỗi của mình gây ra [1].
  [1: Luật Kinh doanh bất động sản 29/2023/QH15 — bản Word cung cấp — Điều 65. Nghĩa vụ của doanh nghiệp kinh doanh dịch vụ môi giới bất động sản, cá nhân hành nghề môi giới bất động sản | Khoản 1](https://vanban.chinhphu.vn/?classid=1&docid=209624&pageid=27160&typegroupid=3)
- Người thuê đối chiếu phòng thực tế với hồ sơ và thông tin do bên môi giới đã cung cấp để xác định sai lệch [1].
  [1: Luật Kinh doanh bất động sản 29/2023/QH15 — bản Word cung cấp — Điều 65. Nghĩa vụ của doanh nghiệp kinh doanh dịch vụ môi giới bất động sản, cá nhân hành nghề môi giới bất động sản | Khoản 1](https://vanban.chinhphu.vn/?classid=1&docid=209624&pageid=27160&typegroupid=3)
- Yêu cầu bên môi giới chịu trách nhiệm về thông tin đã cung cấp không trung thực theo quy định pháp luật [1].
  [1: Luật Kinh doanh bất động sản 29/2023/QH15 — bản Word cung cấp — Điều 65. Nghĩa vụ của doanh nghiệp kinh doanh dịch vụ môi giới bất động sản, cá nhân hành nghề môi giới bất động sản | Khoản 1](https://vanban.chinhphu.vn/?classid=1&docid=209624&pageid=27160&typegroupid=3)
- Yêu cầu bên môi giới bồi thường thiệt hại nếu việc cung cấp thông tin sai lệch do lỗi của họ gây ra thiệt hại thực tế [1].
  [1: Luật Kinh doanh bất động sản 29/2023/QH15 — bản Word cung cấp — Điều 65. Nghĩa vụ của doanh nghiệp kinh doanh dịch vụ môi giới bất động sản, cá nhân hành nghề môi giới bất động sản | Khoản 1](https://vanban.chinhphu.vn/?classid=1&docid=209624&pageid=27160&typegroupid=3)
- Rà soát và yêu cầu thực hiện các nghĩa vụ khác đã cam kết theo hợp đồng dịch vụ môi giới nếu có ký kết [1].
  [1: Luật Kinh doanh bất động sản 29/2023/QH15 — bản Word cung cấp — Điều 65. Nghĩa vụ của doanh nghiệp kinh doanh dịch vụ môi giới bất động sản, cá nhân hành nghề môi giới bất động sản | Khoản 1](https://vanban.chinhphu.vn/?classid=1&docid=209624&pageid=27160&typegroupid=3)
- Nguồn trích dẫn hiện tại chưa nêu rõ quy trình khiếu nại cụ thể đối với cá nhân môi giới tự do không thuộc doanh nghiệp [1].
  [1: Luật Kinh doanh bất động sản 29/2023/QH15 — bản Word cung cấp — Điều 65. Nghĩa vụ của doanh nghiệp kinh doanh dịch vụ môi giới bất động sản, cá nhân hành nghề môi giới bất động sản | Khoản 1](https://vanban.chinhphu.vn/?classid=1&docid=209624&pageid=27160&typegroupid=3)

**Đối chiếu nguyên mẫu:**

Nhãn tổng hợp: **low**; nhãn Qwen gốc: **partial**. ANSWER thiếu quyền từ chối thuê và không thanh toán phí như REFERENCE; cũng thiếu hướng dẫn báo cáo cơ quan chức năng.

**Rà mẫu/nguồn:** Quyền từ chối, hoàn phí và bồi thường phụ thuộc thỏa thuận, vi phạm và thiệt hại; không coi mọi mô tả sai tự động cho quyền không trả mọi phí và hoàn 100%.

| Điểm | Trích mẫu có thật | Trích câu trả lời có thật | Giải thích |
|---|---|---|---|
| different | - Có toàn quyền **từ chối thuê phòng và kiên quyết không thanh toán bất kỳ khoản phí môi giới nào** vì bên môi giới đã vi phạm nghĩa vụ cung cấp thông tin trung thực theo Điều 65 Luật Kinh doanh BĐS. | Doanh nghiệp môi giới có nghĩa vụ cung cấp trung thực thông tin bất động sản, chịu trách nhiệm về thông tin đó và bồi thường thiệt hại do lỗi của mình gây ra [1]. | REFERENCE đề xuất từ chối thuê và không thanh toán phí, trong khi ANSWER chỉ nêu nghĩa vụ bồi thường chung mà thiếu quyền từ chối cụ thể. |
| different | - Yêu cầu hoàn trả lại 100% số tiền đã thu (nếu bị ép đóng phí xem phòng trước đó) và yêu cầu bồi thường thiệt hại nếu thông tin sai gây tổn thất thực tế. | - Yêu cầu bên môi giới bồi thường thiệt hại nếu việc cung cấp thông tin sai lệch do lỗi của họ gây ra thiệt hại thực tế [1]. | REFERENCE yêu cầu hoàn trả 100% tiền và bồi thường, ANSWER cũng đề cập bồi thường nhưng thiếu ý hoàn trả toàn bộ số tiền đã thu. |
| missing | - Báo cáo tài khoản môi giới vi phạm cho nền tảng đăng tin hoặc báo cơ quan Công an nếu có dấu hiệu ép buộc, lừa đảo. |  | REFERENCE hướng dẫn báo cáo cơ quan chức năng hoặc nền tảng, ANSWER không đề cập đến hành động này. |

### Câu 46: Khoản phí môi giới nên được thỏa thuận và thể hiện trong giấy tờ ra sao?

Khoản phí dịch vụ, thù lao hoặc hoa hồng môi giới phải được thỏa thuận rõ ràng trong hợp đồng kinh doanh dịch vụ bất động sản cùng với các nội dung bắt buộc theo luật định [1].

- Ghi nhận rõ mức phí dịch vụ, thù lao hoặc hoa hồng môi giới trong điều khoản hợp đồng [1].
- Xác định cụ thể phương thức thanh toán và thời hạn thanh toán khoản phí môi giới [1].
- Gắn liền khoản phí với đối tượng dịch vụ, nội dung dịch vụ cùng yêu cầu và kết quả dịch vụ cần đạt được [1].
- Thể hiện đầy đủ quyền, nghĩa vụ của các bên và phương thức giải quyết tranh chấp phát sinh từ dịch vụ [1].

Nguồn trích dẫn quy định các nội dung chính của hợp đồng dịch vụ bất động sản nhưng không quy định mức phí cụ thể [1].

Nguồn là bản Word/trích tuyển được cung cấp, chưa xác minh toàn bộ câu chữ với bản chính thức; không coi ghi chú biên tập là quy định pháp luật.

Để áp dụng vào trường hợp của bạn:
- Bạn đã ký hợp đồng dịch vụ bằng văn bản với bên môi giới chưa?
- Bên môi giới đang yêu cầu mức phí cụ thể là bao nhiêu và vào thời điểm nào?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

**Nguồn của từng dòng có trích dẫn:**

- Khoản phí dịch vụ, thù lao hoặc hoa hồng môi giới phải được thỏa thuận rõ ràng trong hợp đồng kinh doanh dịch vụ bất động sản cùng với các nội dung bắt buộc theo luật định [1].
  [1: Luật Kinh doanh bất động sản 29/2023/QH15 — bản Word cung cấp — Điều 46. Nội dung chính của hợp đồng trong kinh doanh bất động sản | Khoản 4](https://vanban.chinhphu.vn/?classid=1&docid=209624&pageid=27160&typegroupid=3)
- Ghi nhận rõ mức phí dịch vụ, thù lao hoặc hoa hồng môi giới trong điều khoản hợp đồng [1].
  [1: Luật Kinh doanh bất động sản 29/2023/QH15 — bản Word cung cấp — Điều 46. Nội dung chính của hợp đồng trong kinh doanh bất động sản | Khoản 4](https://vanban.chinhphu.vn/?classid=1&docid=209624&pageid=27160&typegroupid=3)
- Xác định cụ thể phương thức thanh toán và thời hạn thanh toán khoản phí môi giới [1].
  [1: Luật Kinh doanh bất động sản 29/2023/QH15 — bản Word cung cấp — Điều 46. Nội dung chính của hợp đồng trong kinh doanh bất động sản | Khoản 4](https://vanban.chinhphu.vn/?classid=1&docid=209624&pageid=27160&typegroupid=3)
- Gắn liền khoản phí với đối tượng dịch vụ, nội dung dịch vụ cùng yêu cầu và kết quả dịch vụ cần đạt được [1].
  [1: Luật Kinh doanh bất động sản 29/2023/QH15 — bản Word cung cấp — Điều 46. Nội dung chính của hợp đồng trong kinh doanh bất động sản | Khoản 4](https://vanban.chinhphu.vn/?classid=1&docid=209624&pageid=27160&typegroupid=3)
- Thể hiện đầy đủ quyền, nghĩa vụ của các bên và phương thức giải quyết tranh chấp phát sinh từ dịch vụ [1].
  [1: Luật Kinh doanh bất động sản 29/2023/QH15 — bản Word cung cấp — Điều 46. Nội dung chính của hợp đồng trong kinh doanh bất động sản | Khoản 4](https://vanban.chinhphu.vn/?classid=1&docid=209624&pageid=27160&typegroupid=3)
- Nguồn trích dẫn quy định các nội dung chính của hợp đồng dịch vụ bất động sản nhưng không quy định mức phí cụ thể [1].
  [1: Luật Kinh doanh bất động sản 29/2023/QH15 — bản Word cung cấp — Điều 46. Nội dung chính của hợp đồng trong kinh doanh bất động sản | Khoản 4](https://vanban.chinhphu.vn/?classid=1&docid=209624&pageid=27160&typegroupid=3)

**Đối chiếu nguyên mẫu:**

Nhãn tổng hợp: **partial**; nhãn Qwen gốc: **high**. Đáp án bao phủ hầu hết ý chính nhưng thiếu chi tiết về điều kiện phát sinh phí và cam kết hoàn tiền cụ thể.

**Rà mẫu/nguồn:** Phải tách nghĩa vụ ghi nội dung hợp đồng dịch vụ với điều kiện phí sau ký thuê thành công/hoàn tiền: các điều kiện đó cần thỏa thuận hoặc căn cứ cụ thể, không tự thành quy tắc bắt buộc.

| Điểm | Trích mẫu có thật | Trích câu trả lời có thật | Giải thích |
|---|---|---|---|
| matched | Phí môi giới phải được lập thành văn bản (Hợp đồng dịch vụ môi giới hoặc phiếu thu xác nhận dịch vụ) với các nội dung: | Khoản phí dịch vụ, thù lao hoặc hoa hồng môi giới phải được thỏa thuận rõ ràng trong hợp đồng kinh doanh dịch vụ bất động sản cùng với các nội dung bắt buộc theo luật định [1]. | Phải lập thành văn bản như hợp đồng dịch vụ hoặc phiếu thu xác nhận. |
| different | Họ tên, thông tin pháp nhân/CCCD của hai bên. | Khoản phí dịch vụ, thù lao hoặc hoa hồng môi giới phải được thỏa thuận rõ ràng trong hợp đồng kinh doanh dịch vụ bất động sản cùng với các nội dung bắt buộc theo luật định [1]. | Cần ghi rõ thông tin pháp lý của hai bên tham gia giao dịch. |
| matched | Nội dung dịch vụ, yêu cầu về phòng trọ và thời hạn thực hiện. | - Gắn liền khoản phí với đối tượng dịch vụ, nội dung dịch vụ cùng yêu cầu và kết quả dịch vụ cần đạt được [1]. | Phải xác định nội dung dịch vụ, yêu cầu và thời hạn thực hiện. |
| matched | Mức phí dịch vụ cụ thể và phương thức thanh toán. | - Xác định cụ thể phương thức thanh toán và thời hạn thanh toán khoản phí môi giới [1]. | Cần ghi rõ mức phí cụ thể và phương thức thanh toán. |
| different | **Điều kiện phát sinh phí:** Phải ghi rõ *phí môi giới chỉ được thanh toán sau khi người thuê đã ký hợp đồng thuê phòng trọ thành công với chủ trọ*. | Khoản phí dịch vụ, thù lao hoặc hoa hồng môi giới phải được thỏa thuận rõ ràng trong hợp đồng kinh doanh dịch vụ bất động sản cùng với các nội dung bắt buộc theo luật định [1]. | Phải ghi rõ điều kiện phát sinh phí khi người thuê ký hợp đồng thành công. |
| different | Cam kết hoàn tiền nếu giao dịch bất thành do lỗi thông tin sai từ bên môi giới. | - Thể hiện đầy đủ quyền, nghĩa vụ của các bên và phương thức giải quyết tranh chấp phát sinh từ dịch vụ [1]. | Cần có cam kết hoàn tiền nếu giao dịch bất thành do lỗi thông tin sai. |

### Câu 47: Khi tìm phòng qua một nền tảng trực tuyến, tôi nên kiểm tra người đăng và nguồn tin như thế nào?

Khuyến nghị người thuê đối chiếu tài khoản, nội dung liên hệ, hình ảnh và mức giá để nhận diện nguy cơ gian lận trước khi chuyển tiền [1] [2] [3] [4].

- Kiểm tra độ uy tín của người cho thuê bằng cách tìm kiếm số điện thoại và địa chỉ trên Google, Facebook, diễn đàn hoặc xem đánh giá giao dịch trước đó [4].
- Xác minh tài khoản người đăng, cảnh giác thủ đoạn sao chép thông tin thật kết hợp tương tác ảo hoặc đánh giá tích cực giả mạo [3].
- Kiểm tra hình ảnh bài đăng bằng công cụ Google Ống kính để tìm trang web có hình ảnh đó hoặc ảnh tương tự nhằm phát hiện sao chép [2] [3].
- Xác định địa chỉ cụ thể gồm số nhà, tên đường, phường, quận và khảo sát mức giá chung theo khu vực trên nền tảng [4].
- Cảnh giác với tin đăng có mức giá quá rẻ bất thường hoặc thúc ép chuyển tiền đặt cọc giữ chỗ [1] [3] [4].
- Yêu cầu gặp trực tiếp chủ nhà, kiểm tra thẻ Căn cước hoặc Căn cước công dân và giấy tờ nhà để xác nhận quyền sở hữu trước khi đặt cọc [4].

Biện pháp xác thực số điện thoại trên nền tảng hỗ trợ bảo mật tài khoản nhưng không tự chứng minh quyền sở hữu hay quyền cho thuê phòng [1].
Kết quả tìm kiếm ảnh qua Google Ống kính chỉ đóng vai trò đầu mối đối chiếu, không tự chứng minh toàn bộ tính xác thực của tin đăng [2].

Hướng dẫn/khuyến cáo của Trợ Giúp Chợ Tốt Nhà Tốt; không phải điều luật. Xác thực số điện thoại không xác minh quyền sở hữu hay quyền cho thuê. Chính sách riêng không bảo đảm mọi tin đều đúng và không xác lập nghĩa vụ giống nhau cho mọi nền tảng.
Hướng dẫn công cụ Google Lens, không phải điều luật. Kết quả ảnh tương tự là đầu mối để đối chiếu, không tự chứng minh tin đăng giả hoặc danh tính người cho thuê.
Hướng dẫn/khuyến cáo của Cổng Thông tin điện tử Bộ Công an bài Công an tỉnh Tuyên Quang; không phải điều luật. Tình huống gốc là đặt khách sạn tại Tuyên Quang. Áp dụng tham khảo cho chứng cứ giao dịch trực tuyến, không gọi là vụ thuê trọ CTU; không phải danh mục hồ sơ bắt buộc hoặc hướng dẫn soạn đơn tập thể.
Hướng dẫn/khuyến cáo của Trợ Giúp Chợ Tốt; không phải điều luật. Mẹo giao dịch, không phải điều luật. Không chứng minh hạn hoàn cọc cố định hoặc mức cọc bắt buộc; không thay thế xác minh người được ủy quyền cho thuê. Chỉ đọc phần kiểm tra, không bổ sung mẫu soạn hợp đồng.

Để áp dụng vào trường hợp của bạn:
- Bạn đã liên hệ người đăng và nhận được yêu cầu chuyển tiền cọc trước khi xem phòng chưa?
- Bạn đã có địa chỉ cụ thể của phòng trọ để đối chiếu thực tế chưa?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

**Nguồn của từng dòng có trích dẫn:**

- Khuyến nghị người thuê đối chiếu tài khoản, nội dung liên hệ, hình ảnh và mức giá để nhận diện nguy cơ gian lận trước khi chuyển tiền [1] [2] [3] [4].
  [1: Nhà Tốt bảo vệ người dùng như thế nào — Trợ Giúp Chợ Tốt Nhà Tốt — Nhà Tốt bảo vệ người dùng như thế nào | Đoạn nguyên văn 75](https://trogiup.chotot.com/nguoi-mua/nha-tot-bao-ve-nguoi-dung-nhu-the-nao/); [2: Google Lens: kiểm tra nguồn hình ảnh — Google Search Help — Google Lens — tìm ảnh và trang chứa ảnh tương tự](https://support.google.com/websearch/answer/1325808?co=GENIE.Platform%3DDesktop&hl=vi); [3: Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 — Cổng Thông tin điện tử Bộ Công an bài Công an tỉnh Tuyên Quang — Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 | Đoạn nguyên văn 12](https://bocongan.gov.vn/bai-viet/canh-giac-thu-doan-lua-dao-mao-danh-fanpage-khach-san-nha-hang-dat-coc-truc-tuyen-dip-le-hoi-thanh-tuyen-2026-1790041513); [4: Mẹo khi thuê phòng — Trợ Giúp Chợ Tốt — Mẹo khi thuê phòng | Đoạn nguyên văn 78](https://trogiup.chotot.com/nguoi-mua/meo-khi-thue-phong/)
- Kiểm tra độ uy tín của người cho thuê bằng cách tìm kiếm số điện thoại và địa chỉ trên Google, Facebook, diễn đàn hoặc xem đánh giá giao dịch trước đó [4].
  [4: Mẹo khi thuê phòng — Trợ Giúp Chợ Tốt — Mẹo khi thuê phòng | Đoạn nguyên văn 78](https://trogiup.chotot.com/nguoi-mua/meo-khi-thue-phong/)
- Xác minh tài khoản người đăng, cảnh giác thủ đoạn sao chép thông tin thật kết hợp tương tác ảo hoặc đánh giá tích cực giả mạo [3].
  [3: Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 — Cổng Thông tin điện tử Bộ Công an bài Công an tỉnh Tuyên Quang — Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 | Đoạn nguyên văn 12](https://bocongan.gov.vn/bai-viet/canh-giac-thu-doan-lua-dao-mao-danh-fanpage-khach-san-nha-hang-dat-coc-truc-tuyen-dip-le-hoi-thanh-tuyen-2026-1790041513)
- Kiểm tra hình ảnh bài đăng bằng công cụ Google Ống kính để tìm trang web có hình ảnh đó hoặc ảnh tương tự nhằm phát hiện sao chép [2] [3].
  [2: Google Lens: kiểm tra nguồn hình ảnh — Google Search Help — Google Lens — tìm ảnh và trang chứa ảnh tương tự](https://support.google.com/websearch/answer/1325808?co=GENIE.Platform%3DDesktop&hl=vi); [3: Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 — Cổng Thông tin điện tử Bộ Công an bài Công an tỉnh Tuyên Quang — Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 | Đoạn nguyên văn 12](https://bocongan.gov.vn/bai-viet/canh-giac-thu-doan-lua-dao-mao-danh-fanpage-khach-san-nha-hang-dat-coc-truc-tuyen-dip-le-hoi-thanh-tuyen-2026-1790041513)
- Xác định địa chỉ cụ thể gồm số nhà, tên đường, phường, quận và khảo sát mức giá chung theo khu vực trên nền tảng [4].
  [4: Mẹo khi thuê phòng — Trợ Giúp Chợ Tốt — Mẹo khi thuê phòng | Đoạn nguyên văn 78](https://trogiup.chotot.com/nguoi-mua/meo-khi-thue-phong/)
- Cảnh giác với tin đăng có mức giá quá rẻ bất thường hoặc thúc ép chuyển tiền đặt cọc giữ chỗ [1] [3] [4].
  [1: Nhà Tốt bảo vệ người dùng như thế nào — Trợ Giúp Chợ Tốt Nhà Tốt — Nhà Tốt bảo vệ người dùng như thế nào | Đoạn nguyên văn 75](https://trogiup.chotot.com/nguoi-mua/nha-tot-bao-ve-nguoi-dung-nhu-the-nao/); [3: Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 — Cổng Thông tin điện tử Bộ Công an bài Công an tỉnh Tuyên Quang — Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 | Đoạn nguyên văn 12](https://bocongan.gov.vn/bai-viet/canh-giac-thu-doan-lua-dao-mao-danh-fanpage-khach-san-nha-hang-dat-coc-truc-tuyen-dip-le-hoi-thanh-tuyen-2026-1790041513); [4: Mẹo khi thuê phòng — Trợ Giúp Chợ Tốt — Mẹo khi thuê phòng | Đoạn nguyên văn 78](https://trogiup.chotot.com/nguoi-mua/meo-khi-thue-phong/)
- Yêu cầu gặp trực tiếp chủ nhà, kiểm tra thẻ Căn cước hoặc Căn cước công dân và giấy tờ nhà để xác nhận quyền sở hữu trước khi đặt cọc [4].
  [4: Mẹo khi thuê phòng — Trợ Giúp Chợ Tốt — Mẹo khi thuê phòng | Đoạn nguyên văn 78](https://trogiup.chotot.com/nguoi-mua/meo-khi-thue-phong/)
- Biện pháp xác thực số điện thoại trên nền tảng hỗ trợ bảo mật tài khoản nhưng không tự chứng minh quyền sở hữu hay quyền cho thuê phòng [1].
  [1: Nhà Tốt bảo vệ người dùng như thế nào — Trợ Giúp Chợ Tốt Nhà Tốt — Nhà Tốt bảo vệ người dùng như thế nào | Đoạn nguyên văn 75](https://trogiup.chotot.com/nguoi-mua/nha-tot-bao-ve-nguoi-dung-nhu-the-nao/)
- Kết quả tìm kiếm ảnh qua Google Ống kính chỉ đóng vai trò đầu mối đối chiếu, không tự chứng minh toàn bộ tính xác thực của tin đăng [2].
  [2: Google Lens: kiểm tra nguồn hình ảnh — Google Search Help — Google Lens — tìm ảnh và trang chứa ảnh tương tự](https://support.google.com/websearch/answer/1325808?co=GENIE.Platform%3DDesktop&hl=vi)

**Đối chiếu nguyên mẫu:**

Nhãn tổng hợp: **high**; nhãn Qwen gốc: **high**. Đáp án bao phủ đầy đủ các bước kiểm tra người đăng, nguồn tin, hình ảnh và cảnh báo giá cả so với tham chiếu.

**Rà mẫu/nguồn:** Bốn nhóm kiểm tra có nguồn thực hành; tuổi tài khoản và địa danh/ví dụ giá là chi tiết phụ cần nguồn. Tìm ảnh chỉ cung cấp dấu vết, không tự chứng minh gian lận.

| Điểm | Trích mẫu có thật | Trích câu trả lời có thật | Giải thích |
|---|---|---|---|
| matched | **Kiểm tra tài khoản người đăng:** Xem tài khoản đã được xác thực danh tính/SĐT trên nền tảng chưa, thâm niên hoạt động, đánh giá từ người dùng khác. | - Xác minh tài khoản người đăng, cảnh giác thủ đoạn sao chép thông tin thật kết hợp tương tác ảo hoặc đánh giá tích cực giả mạo [3]. | Kiểm tra tài khoản người đăng qua xác thực danh tính, thâm niên và đánh giá. |
| matched | **Xác minh nội dung bài đăng:** Địa chỉ phòng có chi tiết số nhà, tên đường, phường tại Cần Thơ không; | - Xác định địa chỉ cụ thể gồm số nhà, tên đường, phường, quận và khảo sát mức giá chung theo khu vực trên nền tảng [4]. | Xác minh nội dung bài đăng gồm địa chỉ chi tiết số nhà, tên đường, phường. |
| matched | có số điện thoại liên hệ rõ ràng không. | - Kiểm tra độ uy tín của người cho thuê bằng cách tìm kiếm số điện thoại và địa chỉ trên Google, Facebook, diễn đàn hoặc xem đánh giá giao dịch trước đó [4]. | Kiểm tra số điện thoại liên hệ rõ ràng trong bài đăng. |
| matched | **Tìm kiếm bằng hình ảnh (Reverse Image Search):** Dùng Google Hình ảnh để kiểm tra ảnh phòng có bị sao chép từ các bài đăng ở tỉnh thành khác hay không. | - Kiểm tra hình ảnh bài đăng bằng công cụ Google Ống kính để tìm trang web có hình ảnh đó hoặc ảnh tương tự nhằm phát hiện sao chép [2] [3]. | Dùng Google Hình ảnh hoặc Ống kính để tìm kiếm bằng hình ảnh phát hiện sao chép. |
| matched | **Cảnh giác giá rẻ bất thường:** Phòng đầy đủ nội thất, máy lạnh ở trung tâm Ninh Kiều nhưng để giá vài trăm ngàn là dấu hiệu mồi nhử lừa cọc. | - Cảnh giác với tin đăng có mức giá quá rẻ bất thường hoặc thúc ép chuyển tiền đặt cọc giữ chỗ [1] [3] [4]. | Cảnh giác giá rẻ bất thường và yêu cầu chuyển tiền trước khi xem phòng. |

### Câu 48: Nếu một tin đăng nhà trọ có thông tin sai, tôi có thể báo cáo cho nền tảng bằng cách nào?

Bạn có thể báo cáo tin đăng sai lệch trực tiếp trên giao diện bài đăng hoặc liên hệ qua kênh hỗ trợ trực tuyến của nền tảng kèm bằng chứng vi phạm [1] [4].

- Trên Chợ Tốt, bạn chọn mục Báo cáo tin đăng bên dưới nội dung tin, chọn lý do như thông tin không đúng thực tế hoặc lừa đảo, điền thông tin mô tả rồi chọn Gửi [1].
- Bạn cũng có thể liên hệ bộ phận hỗ trợ của Chợ Tốt qua trò chuyện trực tuyến hoặc gửi thư đến email hỗ trợ công bố trên nền tảng kèm đường dẫn tin vi phạm, lý do và số điện thoại liên hệ [1].
- Theo hướng dẫn của Nhà Tốt, bạn nên gửi kèm thông tin hoặc hình ảnh trao đổi thể hiện hành vi vi phạm khi phản ánh tin đăng để làm rõ sai phạm [2].
- Hệ thống của nền tảng thương mại điện tử trung gian tiếp nhận phản ánh, cho phép gửi bằng chứng sơ bộ, theo dõi tiến trình và xử lý kịp thời theo quy trình đã công khai [4].

Thao tác báo cáo trên bài đăng và liên hệ chăm sóc khách hàng được trích từ hướng dẫn của Chợ Tốt và Nhà Tốt, vị trí nút bấm có thể khác nhau tùy giao diện từng nền tảng [1] [2].
Quy định về hệ thống tiếp nhận, xử lý phản ánh của nền tảng trung gian có hiệu lực từ ngày 01 tháng 7 năm 2026, nhưng không ấn định cam kết giải quyết mọi báo cáo người dùng trong 24 giờ [4] [5].

Hướng dẫn/khuyến cáo của Trợ Giúp Chợ Tốt; không phải điều luật. Đây là thao tác trên Chợ Tốt; vị trí nút có thể thay đổi. Báo cáo nền tảng không thay thế việc báo cơ quan có thẩm quyền khi có dấu hiệu chiếm đoạt.
Hướng dẫn của Nhà Tốt về hình ảnh trao đổi giúp làm rõ phản ánh tin/người bán vi phạm; không phải điều luật hoặc thời hạn xử lý. Trang nguồn có bối cảnh mua bất động sản; chỉ dùng phần phản ánh tin, không suy sang thủ tục mua bán hoặc quyền trong hợp đồng thuê.
Văn bản TMĐT có hiệu lực 01/07/2026; phải đọc đúng loại nền tảng và điều khoản chuyển tiếp. Điều 52 khoản 2: quy định xác thực điện tử áp dụng từ 01/01/2027, chưa áp dụng ở ngày 05/10/2026.

Để áp dụng vào trường hợp của bạn:
- Bạn đang xem tin đăng phòng trọ trên Chợ Tốt hay một nền tảng trực tuyến nào khác?
- Bạn đã lưu lại hình ảnh hoặc nội dung tin nhắn trao đổi làm bằng chứng sai lệch chưa?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

**Nguồn của từng dòng có trích dẫn:**

- Bạn có thể báo cáo tin đăng sai lệch trực tiếp trên giao diện bài đăng hoặc liên hệ qua kênh hỗ trợ trực tuyến của nền tảng kèm bằng chứng vi phạm [1] [4].
  [1: Làm thế nào để báo cáo tin đăng — Trợ Giúp Chợ Tốt — Làm thế nào để báo cáo tin đăng | Đoạn nguyên văn 93](https://trogiup.chotot.com/nguoi-mua/lam-the-nao-de-bao-cao-tin-dang/); [4: Nghị định 248/2026/NĐ-CP hướng dẫn Luật Thương mại điện tử — Chính phủ Công báo Chính phủ — Điều 18. Trách nhiệm của chủ quản nền tảng thương mại điện tử trung gian | Khoản 4](https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-248-2026-nd-cp-469983.htm)
- Trên Chợ Tốt, bạn chọn mục Báo cáo tin đăng bên dưới nội dung tin, chọn lý do như thông tin không đúng thực tế hoặc lừa đảo, điền thông tin mô tả rồi chọn Gửi [1].
  [1: Làm thế nào để báo cáo tin đăng — Trợ Giúp Chợ Tốt — Làm thế nào để báo cáo tin đăng | Đoạn nguyên văn 93](https://trogiup.chotot.com/nguoi-mua/lam-the-nao-de-bao-cao-tin-dang/)
- Bạn cũng có thể liên hệ bộ phận hỗ trợ của Chợ Tốt qua trò chuyện trực tuyến hoặc gửi thư đến email hỗ trợ công bố trên nền tảng kèm đường dẫn tin vi phạm, lý do và số điện thoại liên hệ [1].
  [1: Làm thế nào để báo cáo tin đăng — Trợ Giúp Chợ Tốt — Làm thế nào để báo cáo tin đăng | Đoạn nguyên văn 93](https://trogiup.chotot.com/nguoi-mua/lam-the-nao-de-bao-cao-tin-dang/)
- Theo hướng dẫn của Nhà Tốt, bạn nên gửi kèm thông tin hoặc hình ảnh trao đổi thể hiện hành vi vi phạm khi phản ánh tin đăng để làm rõ sai phạm [2].
  [2: Nhà Tốt: hình ảnh trao đổi hỗ trợ phản ánh tin vi phạm — Hình ảnh trao đổi khi phản ánh tin đăng/người bán vi phạm](https://trogiup.chotot.com/nguoi-mua/bi-quyet-mua-bat-dong-san-an-toan-voi-nha-tot/)
- Hệ thống của nền tảng thương mại điện tử trung gian tiếp nhận phản ánh, cho phép gửi bằng chứng sơ bộ, theo dõi tiến trình và xử lý kịp thời theo quy trình đã công khai [4].
  [4: Nghị định 248/2026/NĐ-CP hướng dẫn Luật Thương mại điện tử — Chính phủ Công báo Chính phủ — Điều 18. Trách nhiệm của chủ quản nền tảng thương mại điện tử trung gian | Khoản 4](https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-248-2026-nd-cp-469983.htm)
- Thao tác báo cáo trên bài đăng và liên hệ chăm sóc khách hàng được trích từ hướng dẫn của Chợ Tốt và Nhà Tốt, vị trí nút bấm có thể khác nhau tùy giao diện từng nền tảng [1] [2].
  [1: Làm thế nào để báo cáo tin đăng — Trợ Giúp Chợ Tốt — Làm thế nào để báo cáo tin đăng | Đoạn nguyên văn 93](https://trogiup.chotot.com/nguoi-mua/lam-the-nao-de-bao-cao-tin-dang/); [2: Nhà Tốt: hình ảnh trao đổi hỗ trợ phản ánh tin vi phạm — Hình ảnh trao đổi khi phản ánh tin đăng/người bán vi phạm](https://trogiup.chotot.com/nguoi-mua/bi-quyet-mua-bat-dong-san-an-toan-voi-nha-tot/)
- Quy định về hệ thống tiếp nhận, xử lý phản ánh của nền tảng trung gian có hiệu lực từ ngày 01 tháng 7 năm 2026, nhưng không ấn định cam kết giải quyết mọi báo cáo người dùng trong 24 giờ [4] [5].
  [4: Nghị định 248/2026/NĐ-CP hướng dẫn Luật Thương mại điện tử — Chính phủ Công báo Chính phủ — Điều 18. Trách nhiệm của chủ quản nền tảng thương mại điện tử trung gian | Khoản 4](https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-248-2026-nd-cp-469983.htm); [5: Nghị định 248/2026/NĐ-CP hướng dẫn Luật Thương mại điện tử — Chính phủ Công báo Chính phủ — Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp](https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-248-2026-nd-cp-469983.htm)

**Đối chiếu nguyên mẫu:**

Nhãn tổng hợp: **partial**; nhãn Qwen gốc: **high**. ANSWER phủ nhận cam kết 24h của REFERENCE ID5 nên là different; các ý còn lại khớp nội dung.

**Rà mẫu/nguồn:** Các bước báo tin/kênh hỗ trợ phụ thuộc nền tảng. 24 giờ gỡ tin trong nguồn gắn yêu cầu cơ quan có thẩm quyền, không phải cam kết mọi báo cáo người dùng; link tin/điện thoại người báo không đồng nhất ID tin/điện thoại người đăng.

| Điểm | Trích mẫu có thật | Trích câu trả lời có thật | Giải thích |
|---|---|---|---|
| matched | - **Cách 1 — Báo cáo trực tiếp trên bài đăng:** Nhấn vào nút **"Báo cáo tin đăng"** (Report) bên dưới bài; | - Trên Chợ Tốt, bạn chọn mục Báo cáo tin đăng bên dưới nội dung tin, chọn lý do như thông tin không đúng thực tế hoặc lừa đảo, điền thông tin mô tả rồi chọn Gửi [1]. | Báo cáo trực tiếp trên bài đăng bằng nút Report. |
| matched | chọn lý do (*Lừa đảo*, *Thông tin không đúng thực tế*, *Hàng/phòng đã bán*); | - Trên Chợ Tốt, bạn chọn mục Báo cáo tin đăng bên dưới nội dung tin, chọn lý do như thông tin không đúng thực tế hoặc lừa đảo, điền thông tin mô tả rồi chọn Gửi [1]. | Chọn lý do báo cáo như thông tin không đúng thực tế. |
| matched | nhập mô tả và đính kèm ảnh chụp màn hình bằng chứng. | - Trên Chợ Tốt, bạn chọn mục Báo cáo tin đăng bên dưới nội dung tin, chọn lý do như thông tin không đúng thực tế hoặc lừa đảo, điền thông tin mô tả rồi chọn Gửi [1]. | Nhập mô tả và đính kèm ảnh chụp màn hình bằng chứng. |
| matched | - **Cách 2 — Liên hệ Chăm sóc khách hàng của sàn:** Gửi email hoặc liên hệ tổng đài của sàn, cung cấp ID tin đăng, số điện thoại người đăng và nội dung sai lệch. | - Bạn cũng có thể liên hệ bộ phận hỗ trợ của Chợ Tốt qua trò chuyện trực tuyến hoặc gửi thư đến email hỗ trợ công bố trên nền tảng kèm đường dẫn tin vi phạm, lý do và số điện thoại liên hệ [1]. | Liên hệ Chăm sóc khách hàng qua email hoặc tổng đài. |
| different | Sàn có nghĩa vụ tiếp nhận và gỡ bỏ tin vi phạm trong vòng 24 giờ. | Quy định về hệ thống tiếp nhận, xử lý phản ánh của nền tảng trung gian có hiệu lực từ ngày 01 tháng 7 năm 2026, nhưng không ấn định cam kết giải quyết mọi báo cáo người dùng trong 24 giờ [4] [5]. | Nền tảng có nghĩa vụ xử lý trong vòng 24 giờ. |

### Câu 49: Nền tảng đăng tin có trách nhiệm gì đối với thông tin người bán hoặc người cho thuê theo tài liệu hiện có?

Nền tảng thương mại điện tử có trách nhiệm công khai thông tin người bán, rà soát gỡ bỏ tin vi phạm, tiếp nhận khiếu nại và cung cấp dữ liệu cho cơ quan nhà nước theo quy định [1] [2].

- Nền tảng trung gian phải công khai tên, địa chỉ cư trú của cá nhân hoặc tên, địa điểm kinh doanh, trụ sở của tổ chức, hộ kinh doanh theo đăng ký bằng tiếng Việt hoặc ký tự La-tinh [2].
- Chủ quản nền tảng có trách nhiệm thực hiện việc xác thực điện tử danh tính người bán kể từ ngày 01/01/2027 qua họ tên, ngày sinh, số định danh cá nhân đối với cá nhân trong nước hoặc thông tin tổ chức, người bán nước ngoài [2] [4].
- Nền tảng phải cập nhật từ khóa theo cơ quan nhà nước, kiểm duyệt nội dung trước khi hiển thị và gỡ bỏ thông tin vi phạm trong thời hạn 24 giờ kể từ khi nhận được yêu cầu của cơ quan có thẩm quyền [1] [2].
- Nền tảng phải công khai phương thức tiếp nhận, giải quyết phản ánh và cung cấp thông tin vi phạm cho cơ quan nhà nước có thẩm quyền trong thời hạn 24 giờ kể từ khi tiếp nhận yêu cầu nếu có chức năng đặt hàng trực tuyến [1] [3].

Quy định về việc thực hiện xác thực điện tử danh tính người bán chỉ bắt đầu áp dụng từ ngày 01/01/2027 theo quy định chuyển tiếp [4].
Thời hạn cung cấp dữ liệu và tạm ngừng tài khoản trong 24 giờ áp dụng theo yêu cầu của cơ quan nhà nước có thẩm quyền chứ không phải cam kết xử lý mọi phản ánh của người dùng [1] [3].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng.
Cần đối chiếu điều/khoản được dẫn chiếu còn thiếu; đoạn trích chưa đủ để kết luận toàn bộ điều kiện và ngoại lệ.
Văn bản TMĐT có hiệu lực 01/07/2026; phải đọc đúng loại nền tảng và điều khoản chuyển tiếp. Điều 52 khoản 2: quy định xác thực điện tử áp dụng từ 01/01/2027, chưa áp dụng ở ngày 05/10/2026.

Để áp dụng vào trường hợp của bạn:
- Nền tảng bạn đang quan tâm là trang đăng tin thông thường hay sàn có chức năng đặt hàng trực tuyến?
- Người đăng tin cho thuê phòng là cá nhân hay tổ chức, doanh nghiệp?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

**Nguồn của từng dòng có trích dẫn:**

- Nền tảng thương mại điện tử có trách nhiệm công khai thông tin người bán, rà soát gỡ bỏ tin vi phạm, tiếp nhận khiếu nại và cung cấp dữ liệu cho cơ quan nhà nước theo quy định [1] [2].
  [1: Nghị định 248/2026/NĐ-CP hướng dẫn Luật Thương mại điện tử — Chính phủ Công báo Chính phủ — Điều 17. Trách nhiệm của chủ quản nền tảng thương mại điện tử | Khoản 1](https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-248-2026-nd-cp-469983.htm); [2: Nghị định 248/2026/NĐ-CP hướng dẫn Luật Thương mại điện tử — Chính phủ Công báo Chính phủ — Điều 18. Trách nhiệm của chủ quản nền tảng thương mại điện tử trung gian | Khoản 1](https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-248-2026-nd-cp-469983.htm)
- Nền tảng trung gian phải công khai tên, địa chỉ cư trú của cá nhân hoặc tên, địa điểm kinh doanh, trụ sở của tổ chức, hộ kinh doanh theo đăng ký bằng tiếng Việt hoặc ký tự La-tinh [2].
  [2: Nghị định 248/2026/NĐ-CP hướng dẫn Luật Thương mại điện tử — Chính phủ Công báo Chính phủ — Điều 18. Trách nhiệm của chủ quản nền tảng thương mại điện tử trung gian | Khoản 1](https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-248-2026-nd-cp-469983.htm)
- Chủ quản nền tảng có trách nhiệm thực hiện việc xác thực điện tử danh tính người bán kể từ ngày 01/01/2027 qua họ tên, ngày sinh, số định danh cá nhân đối với cá nhân trong nước hoặc thông tin tổ chức, người bán nước ngoài [2] [4].
  [2: Nghị định 248/2026/NĐ-CP hướng dẫn Luật Thương mại điện tử — Chính phủ Công báo Chính phủ — Điều 18. Trách nhiệm của chủ quản nền tảng thương mại điện tử trung gian | Khoản 1](https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-248-2026-nd-cp-469983.htm); [4: Nghị định 248/2026/NĐ-CP hướng dẫn Luật Thương mại điện tử — Chính phủ Công báo Chính phủ — Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp](https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-248-2026-nd-cp-469983.htm)
- Nền tảng phải cập nhật từ khóa theo cơ quan nhà nước, kiểm duyệt nội dung trước khi hiển thị và gỡ bỏ thông tin vi phạm trong thời hạn 24 giờ kể từ khi nhận được yêu cầu của cơ quan có thẩm quyền [1] [2].
  [1: Nghị định 248/2026/NĐ-CP hướng dẫn Luật Thương mại điện tử — Chính phủ Công báo Chính phủ — Điều 17. Trách nhiệm của chủ quản nền tảng thương mại điện tử | Khoản 1](https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-248-2026-nd-cp-469983.htm); [2: Nghị định 248/2026/NĐ-CP hướng dẫn Luật Thương mại điện tử — Chính phủ Công báo Chính phủ — Điều 18. Trách nhiệm của chủ quản nền tảng thương mại điện tử trung gian | Khoản 1](https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-248-2026-nd-cp-469983.htm)
- Nền tảng phải công khai phương thức tiếp nhận, giải quyết phản ánh và cung cấp thông tin vi phạm cho cơ quan nhà nước có thẩm quyền trong thời hạn 24 giờ kể từ khi tiếp nhận yêu cầu nếu có chức năng đặt hàng trực tuyến [1] [3].
  [1: Nghị định 248/2026/NĐ-CP hướng dẫn Luật Thương mại điện tử — Chính phủ Công báo Chính phủ — Điều 17. Trách nhiệm của chủ quản nền tảng thương mại điện tử | Khoản 1](https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-248-2026-nd-cp-469983.htm); [3: Nghị định 248/2026/NĐ-CP hướng dẫn Luật Thương mại điện tử — Chính phủ Công báo Chính phủ — Điều 18. Trách nhiệm của chủ quản nền tảng thương mại điện tử trung gian | Khoản 2](https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-248-2026-nd-cp-469983.htm)
- Quy định về việc thực hiện xác thực điện tử danh tính người bán chỉ bắt đầu áp dụng từ ngày 01/01/2027 theo quy định chuyển tiếp [4].
  [4: Nghị định 248/2026/NĐ-CP hướng dẫn Luật Thương mại điện tử — Chính phủ Công báo Chính phủ — Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp](https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-248-2026-nd-cp-469983.htm)
- Thời hạn cung cấp dữ liệu và tạm ngừng tài khoản trong 24 giờ áp dụng theo yêu cầu của cơ quan nhà nước có thẩm quyền chứ không phải cam kết xử lý mọi phản ánh của người dùng [1] [3].
  [1: Nghị định 248/2026/NĐ-CP hướng dẫn Luật Thương mại điện tử — Chính phủ Công báo Chính phủ — Điều 17. Trách nhiệm của chủ quản nền tảng thương mại điện tử | Khoản 1](https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-248-2026-nd-cp-469983.htm); [3: Nghị định 248/2026/NĐ-CP hướng dẫn Luật Thương mại điện tử — Chính phủ Công báo Chính phủ — Điều 18. Trách nhiệm của chủ quản nền tảng thương mại điện tử trung gian | Khoản 2](https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-248-2026-nd-cp-469983.htm)

**Đối chiếu nguyên mẫu:**

Nhãn tổng hợp: **high**; nhãn Qwen gốc: **high**. Các điểm chính về trách nhiệm xác thực, kiểm duyệt, gỡ bỏ và cung cấp dữ liệu đều được khớp đầy đủ giữa tài liệu tham khảo và câu trả lời.

**Rà mẫu/nguồn:** Giữ đúng loại nền tảng. Xác thực điện tử nguồn NĐ248 áp dụng từ 01/01/2027; không trình bày là đã bắt buộc ngày 06/10/2026. 24 giờ cung cấp dữ liệu cần yêu cầu cơ quan và loại nền tảng tương ứng.

| Điểm | Trích mẫu có thật | Trích câu trả lời có thật | Giải thích |
|---|---|---|---|
| matched | **Định danh người đăng:** Yêu cầu người cho thuê cung cấp thông tin xác thực danh tính (họ tên, SĐT, địa chỉ, mã số thuế hoặc định danh điện tử) trước khi đăng tin. | - Chủ quản nền tảng có trách nhiệm thực hiện việc xác thực điện tử danh tính người bán kể từ ngày 01/01/2027 qua họ tên, ngày sinh, số định danh cá nhân đối với cá nhân trong nước hoặc thông tin tổ chức, người bán nước ngoài [2] [4]. | Nền tảng yêu cầu người cho thuê cung cấp thông tin xác thực danh tính trước khi đăng tin. |
| matched | **Kiểm duyệt và ngăn chặn:** Thiết lập bộ lọc từ khóa, tiếp nhận phản ánh để kịp thời ngăn chặn các bài đăng sai lệch, lừa đảo. | - Nền tảng phải cập nhật từ khóa theo cơ quan nhà nước, kiểm duyệt nội dung trước khi hiển thị và gỡ bỏ thông tin vi phạm trong thời hạn 24 giờ kể từ khi nhận được yêu cầu của cơ quan có thẩm quyền [1] [2]. | Nền tảng thiết lập bộ lọc và tiếp nhận phản ánh để ngăn chặn bài đăng sai lệch. |
| matched | **Gỡ bỏ tin vi phạm:** Duy trì cơ chế giải quyết khiếu nại công khai; | - Nền tảng phải công khai phương thức tiếp nhận, giải quyết phản ánh và cung cấp thông tin vi phạm cho cơ quan nhà nước có thẩm quyền trong thời hạn 24 giờ kể từ khi tiếp nhận yêu cầu nếu có chức năng đặt hàng trực tuyến [1] [3]. | Nền tảng duy trì cơ chế giải quyết khiếu nại công khai và gỡ bỏ tin vi phạm. |
| matched | **Cung cấp dữ liệu cho cơ quan điều tra:** Cung cấp thông tin tài khoản người đăng cho cơ quan Công an có thẩm quyền trong thời hạn 24 giờ kể từ khi nhận được yêu cầu phục vụ điều tra xử lý vi phạm. | Thời hạn cung cấp dữ liệu và tạm ngừng tài khoản trong 24 giờ áp dụng theo yêu cầu của cơ quan nhà nước có thẩm quyền chứ không phải cam kết xử lý mọi phản ánh của người dùng [1] [3]. | Nền tảng cung cấp thông tin tài khoản cho cơ quan Công an trong thời hạn 24 giờ. |

### Câu 50: Nếu người đăng yêu cầu chuyển cọc qua liên kết lạ, tôi nên kiểm tra những dấu hiệu nào trước khi trả tiền?

Khuyến nghị người thuê không vội chuyển tiền và cần nâng cao cảnh giác, thực hiện nghiêm túc quy tắc xác minh thông tin khi đối phương có dấu hiệu thúc ép thanh toán qua liên kết lạ [2].

- Kiểm tra tài khoản và trang đăng tin xem có dấu hiệu sao chép thông tin, dùng tương tác ảo hoặc đánh giá giả mạo để tạo lòng tin hay không [2].
- Cảnh giác nếu nội dung đưa ra mức giá thấp hơn thị trường kèm ưu đãi giới hạn nhằm thúc ép chuyển tiền đặt cọc giữ chỗ thật nhanh [2].
- Kiểm tra dấu hiệu đối phương gửi giấy tờ xác nhận giả hoặc liên tục viện cớ sai nội dung chuyển khoản để đòi chuyển tiền thêm [2].
- Lưu lại toàn bộ bằng chứng như hình ảnh tin nhắn, thông tin tài khoản ngân hàng và phiếu giao dịch trước khi thực hiện thao tác báo cáo trang giả mạo lên nền tảng [2].

Nguồn trích dẫn là khuyến cáo phòng chống lừa đảo trực tuyến của cơ quan công an địa phương, không quy định cụ thể kỹ thuật kiểm tra an toàn mã độc của từng liên kết web [2].

Hướng dẫn/khuyến cáo của Cổng Thông tin điện tử Bộ Công an bài Công an tỉnh Tuyên Quang; không phải điều luật. Tình huống gốc là đặt khách sạn tại Tuyên Quang. Áp dụng tham khảo cho chứng cứ giao dịch trực tuyến, không gọi là vụ thuê trọ CTU; không phải danh mục hồ sơ bắt buộc hoặc hướng dẫn soạn đơn tập thể.
Hướng dẫn/khuyến cáo của Trợ Giúp Chợ Tốt; không phải điều luật. Có nội dung và viện dẫn theo nhiều thời kỳ; không sử dụng tính năng đã ngừng như dịch vụ hiện tại. Chỉ dùng mô tả chính sách nền tảng, đối chiếu nghĩa vụ pháp luật với S15 và S16 cùng điều khoản chuyển tiếp.

Để áp dụng vào trường hợp của bạn:
- Bạn đã chuyển khoản hoặc nhập thông tin tài khoản vào liên kết lạ đó chưa?
- Bạn có lưu lại bằng chứng tin nhắn và thông tin tài khoản của người đăng tin không?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

**Nguồn của từng dòng có trích dẫn:**

- Khuyến nghị người thuê không vội chuyển tiền và cần nâng cao cảnh giác, thực hiện nghiêm túc quy tắc xác minh thông tin khi đối phương có dấu hiệu thúc ép thanh toán qua liên kết lạ [2].
  [2: Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 — Cổng Thông tin điện tử Bộ Công an bài Công an tỉnh Tuyên Quang — Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 | Đoạn nguyên văn 12](https://bocongan.gov.vn/bai-viet/canh-giac-thu-doan-lua-dao-mao-danh-fanpage-khach-san-nha-hang-dat-coc-truc-tuyen-dip-le-hoi-thanh-tuyen-2026-1790041513)
- Kiểm tra tài khoản và trang đăng tin xem có dấu hiệu sao chép thông tin, dùng tương tác ảo hoặc đánh giá giả mạo để tạo lòng tin hay không [2].
  [2: Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 — Cổng Thông tin điện tử Bộ Công an bài Công an tỉnh Tuyên Quang — Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 | Đoạn nguyên văn 12](https://bocongan.gov.vn/bai-viet/canh-giac-thu-doan-lua-dao-mao-danh-fanpage-khach-san-nha-hang-dat-coc-truc-tuyen-dip-le-hoi-thanh-tuyen-2026-1790041513)
- Cảnh giác nếu nội dung đưa ra mức giá thấp hơn thị trường kèm ưu đãi giới hạn nhằm thúc ép chuyển tiền đặt cọc giữ chỗ thật nhanh [2].
  [2: Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 — Cổng Thông tin điện tử Bộ Công an bài Công an tỉnh Tuyên Quang — Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 | Đoạn nguyên văn 12](https://bocongan.gov.vn/bai-viet/canh-giac-thu-doan-lua-dao-mao-danh-fanpage-khach-san-nha-hang-dat-coc-truc-tuyen-dip-le-hoi-thanh-tuyen-2026-1790041513)
- Kiểm tra dấu hiệu đối phương gửi giấy tờ xác nhận giả hoặc liên tục viện cớ sai nội dung chuyển khoản để đòi chuyển tiền thêm [2].
  [2: Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 — Cổng Thông tin điện tử Bộ Công an bài Công an tỉnh Tuyên Quang — Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 | Đoạn nguyên văn 12](https://bocongan.gov.vn/bai-viet/canh-giac-thu-doan-lua-dao-mao-danh-fanpage-khach-san-nha-hang-dat-coc-truc-tuyen-dip-le-hoi-thanh-tuyen-2026-1790041513)
- Lưu lại toàn bộ bằng chứng như hình ảnh tin nhắn, thông tin tài khoản ngân hàng và phiếu giao dịch trước khi thực hiện thao tác báo cáo trang giả mạo lên nền tảng [2].
  [2: Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 — Cổng Thông tin điện tử Bộ Công an bài Công an tỉnh Tuyên Quang — Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 | Đoạn nguyên văn 12](https://bocongan.gov.vn/bai-viet/canh-giac-thu-doan-lua-dao-mao-danh-fanpage-khach-san-nha-hang-dat-coc-truc-tuyen-dip-le-hoi-thanh-tuyen-2026-1790041513)
- Nguồn trích dẫn là khuyến cáo phòng chống lừa đảo trực tuyến của cơ quan công an địa phương, không quy định cụ thể kỹ thuật kiểm tra an toàn mã độc của từng liên kết web [2].
  [2: Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 — Cổng Thông tin điện tử Bộ Công an bài Công an tỉnh Tuyên Quang — Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 | Đoạn nguyên văn 12](https://bocongan.gov.vn/bai-viet/canh-giac-thu-doan-lua-dao-mao-danh-fanpage-khach-san-nha-hang-dat-coc-truc-tuyen-dip-le-hoi-thanh-tuyen-2026-1790041513)

**Đối chiếu nguyên mẫu:**

Nhãn tổng hợp: **low**; nhãn Qwen gốc: **high**. Câu trả lời đề cập đến việc nâng cao cảnh giác và kiểm tra tài khoản nhưng thiếu các dấu hiệu đặc trưng của lừa đảo qua liên kết lạ như link giả, yêu cầu OTP hay áp lực thời gian.

**Rà mẫu/nguồn:** Dấu hiệu rủi ro không tự chứng minh mọi link lạ đã cấu thành lừa đảo. Không nhập bí mật ngân hàng; ví dụ tên miền là minh họa mẫu, không nguồn chứng minh vụ việc thực tế.

| Điểm | Trích mẫu có thật | Trích câu trả lời có thật | Giải thích |
|---|---|---|---|
| different | **Đường link giả mạo:** Link rút gọn (bit.ly, tinyurl...) hoặc có tên miền lạ mạo danh cổng thanh toán/ngân hàng (ví dụ: `vnpay-xacnhancoc.com`, `vietcombank-nhantien.site`...). | Khuyến nghị người thuê không vội chuyển tiền và cần nâng cao cảnh giác, thực hiện nghiêm túc quy tắc xác minh thông tin khi đối phương có dấu hiệu thúc ép thanh toán qua liên kết lạ [2]. | Đoạn trả lời không liệt kê cụ thể các dấu hiệu link giả mạo như bit.ly hay tên miền lạ. |
| different | **Đòi thông tin bảo mật:** Yêu cầu nhập Tên đăng nhập ngân hàng, Mật khẩu, hoặc **Mã xác thực OTP/Smart OTP** để "xác nhận phòng" hoặc "nhận tiền hoàn cọc". | Khuyến nghị người thuê không vội chuyển tiền và cần nâng cao cảnh giác, thực hiện nghiêm túc quy tắc xác minh thông tin khi đối phương có dấu hiệu thúc ép thanh toán qua liên kết lạ [2]. | Trả lời thiếu cảnh báo về việc nhập thông tin bảo mật hoặc mã OTP để xác nhận phòng. |
| different | **Tạo áp lực gấp gáp:** Thúc ép "chuyển cọc qua link trong 10 phút kẻo người khác lấy mất phòng". | Khuyến nghị người thuê không vội chuyển tiền và cần nâng cao cảnh giác, thực hiện nghiêm túc quy tắc xác minh thông tin khi đối phương có dấu hiệu thúc ép thanh toán qua liên kết lạ [2]. | Đoạn trả lời không đề cập đến dấu hiệu tạo áp lực gấp gáp hay thúc ép chuyển tiền nhanh. |
| different | - **Quy tắc vàng:** **Không bấm vào link lạ; | Khuyến nghị người thuê không vội chuyển tiền và cần nâng cao cảnh giác, thực hiện nghiêm túc quy tắc xác minh thông tin khi đối phương có dấu hiệu thúc ép thanh toán qua liên kết lạ [2]. | Trả lời thiếu quy tắc vàng cụ thể như không bấm link lạ hoặc dừng ngay giao dịch. |

### Câu 51: Chủ trọ có thể yêu cầu tôi cung cấp những thông tin cá nhân nào để làm hợp đồng và đăng ký cư trú?

Chủ trọ có thể yêu cầu họ tên, địa chỉ để lập hợp đồng thuê nhà cùng thông tin kê khai tờ khai cư trú và tài liệu chứng minh chỗ ở hợp pháp để làm hồ sơ tạm trú trên cơ sở bạn tự nguyện, biết rõ mục đích xử lý dữ liệu [1] [2] [3].

- Cung cấp họ và tên cùng địa chỉ của bạn để đưa vào nội dung bắt buộc của văn bản hợp đồng thuê nhà [3].
- Kê khai thông tin theo Tờ khai thay đổi thông tin cư trú phục vụ hồ sơ đăng ký tạm trú [1].
- Cung cấp ý kiến đồng ý của cha, mẹ hoặc người giám hộ trong tờ khai hoặc bằng văn bản nếu bạn là người chưa thành niên [1].
- Xác định rõ loại dữ liệu, mục đích xử lý và bên kiểm soát dữ liệu trước khi đồng ý cho chủ trọ thu thập thông tin cá nhân [2].

Hồ sơ đăng ký tạm trú còn cần giấy tờ chứng minh chỗ ở hợp pháp theo quy định cư trú [1].
Nguồn trích dẫn chưa nêu chi tiết toàn bộ các trường thông tin cụ thể bên trong Tờ khai thay đổi thông tin cư trú [1].

Điều 9 quy định nghĩa vụ công dân; Điều 10 quy định chủ hộ/thành viên hộ gia đình, không tự đồng nhất chủ trọ với chủ hộ. Chỉ giải thích trách nhiệm và giấy tờ cơ bản, không điền tờ khai hoặc hướng dẫn hồ sơ chuyên sâu.
Nguồn là bản Word/trích tuyển được cung cấp, chưa xác minh toàn bộ câu chữ với bản chính thức; không coi ghi chú biên tập là quy định pháp luật.

Để áp dụng vào trường hợp của bạn:
- Bạn đã đủ tuổi thành niên khi ký hợp đồng và làm thủ tục tạm trú chưa?
- Chủ trọ tự làm thủ tục đăng ký tạm trú cho bạn hay bạn là người trực tiếp đi nộp hồ sơ?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

**Nguồn của từng dòng có trích dẫn:**

- Chủ trọ có thể yêu cầu họ tên, địa chỉ để lập hợp đồng thuê nhà cùng thông tin kê khai tờ khai cư trú và tài liệu chứng minh chỗ ở hợp pháp để làm hồ sơ tạm trú trên cơ sở bạn tự nguyện, biết rõ mục đích xử lý dữ liệu [1] [2] [3].
  [1: Luật Cư trú 68/2020/QH14 — Word Công báo — Điều 28. Hồ sơ, thủ tục đăng ký tạm trú, gia hạn tạm trú | Khoản 1](https://congbao.chinhphu.vn/van-ban/luat-so-68-2020-qh14-32684/33716.htm); [2: Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 — bản Word cung cấp — Điều 9. Sự đồng ý của chủ thể dữ liệu cá nhân | Khoản 2](https://vanban.chinhphu.vn/?docid=214590&pageid=27160); [3: Luật Nhà ở — 79/VBHN-VPQH — bản Word cung cấp — Điều 163. Hợp đồng về nhà ở | Khoản 1](https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-79-vbhn-vpqh-469209.htm)
- Cung cấp họ và tên cùng địa chỉ của bạn để đưa vào nội dung bắt buộc của văn bản hợp đồng thuê nhà [3].
  [3: Luật Nhà ở — 79/VBHN-VPQH — bản Word cung cấp — Điều 163. Hợp đồng về nhà ở | Khoản 1](https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-79-vbhn-vpqh-469209.htm)
- Kê khai thông tin theo Tờ khai thay đổi thông tin cư trú phục vụ hồ sơ đăng ký tạm trú [1].
  [1: Luật Cư trú 68/2020/QH14 — Word Công báo — Điều 28. Hồ sơ, thủ tục đăng ký tạm trú, gia hạn tạm trú | Khoản 1](https://congbao.chinhphu.vn/van-ban/luat-so-68-2020-qh14-32684/33716.htm)
- Cung cấp ý kiến đồng ý của cha, mẹ hoặc người giám hộ trong tờ khai hoặc bằng văn bản nếu bạn là người chưa thành niên [1].
  [1: Luật Cư trú 68/2020/QH14 — Word Công báo — Điều 28. Hồ sơ, thủ tục đăng ký tạm trú, gia hạn tạm trú | Khoản 1](https://congbao.chinhphu.vn/van-ban/luat-so-68-2020-qh14-32684/33716.htm)
- Xác định rõ loại dữ liệu, mục đích xử lý và bên kiểm soát dữ liệu trước khi đồng ý cho chủ trọ thu thập thông tin cá nhân [2].
  [2: Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 — bản Word cung cấp — Điều 9. Sự đồng ý của chủ thể dữ liệu cá nhân | Khoản 2](https://vanban.chinhphu.vn/?docid=214590&pageid=27160)
- Hồ sơ đăng ký tạm trú còn cần giấy tờ chứng minh chỗ ở hợp pháp theo quy định cư trú [1].
  [1: Luật Cư trú 68/2020/QH14 — Word Công báo — Điều 28. Hồ sơ, thủ tục đăng ký tạm trú, gia hạn tạm trú | Khoản 1](https://congbao.chinhphu.vn/van-ban/luat-so-68-2020-qh14-32684/33716.htm)
- Nguồn trích dẫn chưa nêu chi tiết toàn bộ các trường thông tin cụ thể bên trong Tờ khai thay đổi thông tin cư trú [1].
  [1: Luật Cư trú 68/2020/QH14 — Word Công báo — Điều 28. Hồ sơ, thủ tục đăng ký tạm trú, gia hạn tạm trú | Khoản 1](https://congbao.chinhphu.vn/van-ban/luat-so-68-2020-qh14-32684/33716.htm)

**Đối chiếu nguyên mẫu:**

Nhãn tổng hợp: **partial**; nhãn Qwen gốc: **high**. Đáp án bao phủ đầy đủ các thông tin hợp pháp, nguyên tắc thu thập và giới hạn thông tin so với văn bản mẫu.

**Rà mẫu/nguồn:** Không coi mọi trường ngày/nơi cấp, điện thoại, thông tin cha mẹ là dữ liệu tối thiểu bắt buộc cho mọi giao dịch. Thu thập đúng mục đích và căn cứ; giải thích cơ bản, không điền tờ khai.

| Điểm | Trích mẫu có thật | Trích câu trả lời có thật | Giải thích |
|---|---|---|---|
| matched | **Thông tin hợp pháp được phép yêu cầu:** Họ tên, số CCCD/Căn cước, ngày cấp/nơi cấp, địa chỉ thường trú, số điện thoại liên hệ (và thông tin cha mẹ/người giám hộ nếu người thuê dưới 18 tuổi). | Chủ trọ có thể yêu cầu họ tên, địa chỉ để lập hợp đồng thuê nhà cùng thông tin kê khai tờ khai cư trú và tài liệu chứng minh chỗ ở hợp pháp để làm hồ sơ tạm trú trên cơ sở bạn tự nguyện, biết rõ mục đích xử lý dữ liệu [1] [2] [3]. | Chủ trọ được phép yêu cầu họ tên, CCCD, ngày cấp, nơi cấp, địa chỉ thường trú và số điện thoại. |
| matched | Đây là thông tin tối thiểu để lập hợp đồng thuê và điền Tờ khai CT01 đăng ký tạm trú. | - Kê khai thông tin theo Tờ khai thay đổi thông tin cư trú phục vụ hồ sơ đăng ký tạm trú [1]. | Thông tin này là tối thiểu cần thiết để lập hợp đồng thuê và điền tờ khai CT01 đăng ký tạm trú. |
| matched | **Nguyên tắc thu thập:** Chỉ thu thập đúng phạm vi, mục đích rõ ràng và dựa trên sự đồng ý tự nguyện của người thuê. | - Xác định rõ loại dữ liệu, mục đích xử lý và bên kiểm soát dữ liệu trước khi đồng ý cho chủ trọ thu thập thông tin cá nhân [2]. | Việc thu thập thông tin phải dựa trên sự đồng ý tự nguyện của người thuê với mục đích rõ ràng. |
| different | **Thông tin chủ trọ KHÔNG ĐƯỢC PHÉP yêu cầu:** Mật khẩu mạng xã hội, thông tin tài khoản ngân hàng, mật khẩu thiết bị cá nhân hoặc đời tư không liên quan đến quan hệ thuê trọ. | Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực. | Chủ trọ không được yêu cầu mật khẩu mạng xã hội, thông tin tài khoản ngân hàng hay đời tư không liên quan. |

### Câu 52: Ảnh căn cước công dân của người thuê được lưu và sử dụng như thế nào?

Ảnh căn cước công dân của người thuê chỉ được thu thập, xử lý đúng phạm vi, mục đích rõ ràng, lưu trữ trong thời hạn phù hợp với mục đích và chỉ cung cấp cho bên khác khi có sự đồng ý hoặc theo quy định pháp luật [1] [2].

- Xác định rõ loại dữ liệu, mục đích xử lý và chủ thể kiểm soát dữ liệu trước khi đồng ý cung cấp ảnh căn cước công dân [4].
- Áp dụng đồng bộ các giải pháp kỹ thuật, con người phù hợp để bảo vệ dữ liệu và chỉ lưu trữ trong khoảng thời gian phù hợp mục đích xử lý, trừ khi pháp luật có quy định khác [1].
- Chỉ chuyển giao thông tin cho bên khác khi người thuê đồng ý, trừ các trường hợp ngoại lệ theo luật định như phục vụ cơ quan nhà nước hoặc tình huống cấp bách [2] [3].
- Gửi yêu cầu bằng văn bản hoặc dạng điện tử để rút lại sự đồng ý hoặc hạn chế xử lý dữ liệu khi có nghi ngờ về mục đích, phạm vi lưu trữ [3].

Dữ liệu cá nhân vẫn có thể được xử lý mà không cần sự đồng ý trong các trường hợp cấp bách, phục vụ quản lý nhà nước hoặc theo thỏa thuận hợp pháp [3].

Nguồn là bản Word/trích tuyển được cung cấp, chưa xác minh toàn bộ câu chữ với bản chính thức; không coi ghi chú biên tập là quy định pháp luật.

Để áp dụng vào trường hợp của bạn:
- Bên cho thuê đang yêu cầu cung cấp ảnh căn cước công dân nhằm mục đích gì?
- Hợp đồng thuê trọ của bạn đã có thỏa thuận về thời hạn lưu trữ hoặc việc chia sẻ dữ liệu cá nhân chưa?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

**Nguồn của từng dòng có trích dẫn:**

- Ảnh căn cước công dân của người thuê chỉ được thu thập, xử lý đúng phạm vi, mục đích rõ ràng, lưu trữ trong thời hạn phù hợp với mục đích và chỉ cung cấp cho bên khác khi có sự đồng ý hoặc theo quy định pháp luật [1] [2].
  [1: Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 — bản Word cung cấp — Điều 3. Nguyên tắc bảo vệ dữ liệu cá nhân](https://vanban.chinhphu.vn/?docid=214590&pageid=27160); [2: Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 — bản Word cung cấp — Điều 15. Cung cấp dữ liệu cá nhân](https://vanban.chinhphu.vn/?docid=214590&pageid=27160)
- Xác định rõ loại dữ liệu, mục đích xử lý và chủ thể kiểm soát dữ liệu trước khi đồng ý cung cấp ảnh căn cước công dân [4].
  [4: Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 — bản Word cung cấp — Điều 9. Sự đồng ý của chủ thể dữ liệu cá nhân | Khoản 2](https://vanban.chinhphu.vn/?docid=214590&pageid=27160)
- Áp dụng đồng bộ các giải pháp kỹ thuật, con người phù hợp để bảo vệ dữ liệu và chỉ lưu trữ trong khoảng thời gian phù hợp mục đích xử lý, trừ khi pháp luật có quy định khác [1].
  [1: Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 — bản Word cung cấp — Điều 3. Nguyên tắc bảo vệ dữ liệu cá nhân](https://vanban.chinhphu.vn/?docid=214590&pageid=27160)
- Chỉ chuyển giao thông tin cho bên khác khi người thuê đồng ý, trừ các trường hợp ngoại lệ theo luật định như phục vụ cơ quan nhà nước hoặc tình huống cấp bách [2] [3].
  [2: Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 — bản Word cung cấp — Điều 15. Cung cấp dữ liệu cá nhân](https://vanban.chinhphu.vn/?docid=214590&pageid=27160); [3: Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 — bản Word cung cấp — Điều 10. Yêu cầu rút lại sự đồng ý, yêu cầu hạn chế xử lý dữ liệu cá nhân](https://vanban.chinhphu.vn/?docid=214590&pageid=27160)
- Gửi yêu cầu bằng văn bản hoặc dạng điện tử để rút lại sự đồng ý hoặc hạn chế xử lý dữ liệu khi có nghi ngờ về mục đích, phạm vi lưu trữ [3].
  [3: Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 — bản Word cung cấp — Điều 10. Yêu cầu rút lại sự đồng ý, yêu cầu hạn chế xử lý dữ liệu cá nhân](https://vanban.chinhphu.vn/?docid=214590&pageid=27160)
- Dữ liệu cá nhân vẫn có thể được xử lý mà không cần sự đồng ý trong các trường hợp cấp bách, phục vụ quản lý nhà nước hoặc theo thỏa thuận hợp pháp [3].
  [3: Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 — bản Word cung cấp — Điều 10. Yêu cầu rút lại sự đồng ý, yêu cầu hạn chế xử lý dữ liệu cá nhân](https://vanban.chinhphu.vn/?docid=214590&pageid=27160)

**Đối chiếu nguyên mẫu:**

Nhãn tổng hợp: **high**; nhãn Qwen gốc: **high**. Câu trả lời bao phủ đầy đủ các mục đích sử dụng, trách nhiệm bảo mật và điều kiện chuyển giao từ văn bản gốc.

**Rà mẫu/nguồn:** Điều 15 khoản 2 và Điều 17 có trường hợp cung cấp/chuyển giao hợp pháp; không cấm tuyệt đối mọi bên thứ ba. Mục đích phải cụ thể, lưu đủ thời gian cần thiết và bảo vệ. Chưa có căn cứ rằng watermark ngăn được việc lạm dụng.

| Điểm | Trích mẫu có thật | Trích câu trả lời có thật | Giải thích |
|---|---|---|---|
| matched | **Mục đích sử dụng:** Chỉ được sử dụng cho mục đích đã thông báo: (i) Lưu hồ sơ quản lý phòng trọ; | Ảnh căn cước công dân của người thuê chỉ được thu thập, xử lý đúng phạm vi, mục đích rõ ràng, lưu trữ trong thời hạn phù hợp với mục đích và chỉ cung cấp cho bên khác khi có sự đồng ý hoặc theo quy định pháp luật [1] [2]. | Chỉ dùng cho mục đích thông báo như lưu hồ sơ và nộp tạm trú. |
| matched | (ii) Nộp cho Công an xã/phường để đăng ký tạm trú theo quy định. | - Chỉ chuyển giao thông tin cho bên khác khi người thuê đồng ý, trừ các trường hợp ngoại lệ theo luật định như phục vụ cơ quan nhà nước hoặc tình huống cấp bách [2] [3]. | Chuyển giao chỉ khi có đồng ý hoặc theo quy định pháp luật. |
| matched | **Trách nhiệm bảo mật:** Chủ trọ có trách nhiệm lưu trữ an toàn, tuyệt đối không được chuyển giao, mua bán hoặc phát tán ảnh CCCD của người thuê cho bất kỳ bên thứ ba nào. | Ảnh căn cước công dân của người thuê chỉ được thu thập, xử lý đúng phạm vi, mục đích rõ ràng, lưu trữ trong thời hạn phù hợp với mục đích và chỉ cung cấp cho bên khác khi có sự đồng ý hoặc theo quy định pháp luật [1] [2]. | Lưu trữ an toàn và tuyệt đối không chuyển giao cho bên thứ ba. |

### Câu 53: Chủ trọ có được đăng công khai ảnh giấy tờ hoặc số điện thoại của tôi không?

Chủ trọ không được tự ý đăng công khai hình ảnh giấy tờ hoặc số điện thoại của bạn trừ khi có sự đồng ý của bạn hoặc thuộc các trường hợp pháp luật cho phép [1].

- Dữ liệu cá nhân chỉ được công khai khi bạn đồng ý, thực hiện theo quy định pháp luật, thực hiện nghĩa vụ hợp đồng hoặc để phòng chống tội phạm và vi phạm pháp luật theo quy định [1].
- Sự đồng ý của bạn chỉ có hiệu lực khi hoàn toàn tự nguyện và bạn được biết rõ loại dữ liệu, mục đích xử lý cùng các quyền, nghĩa vụ liên quan [3].
- Việc xử lý và công khai thông tin phải có mục đích cụ thể, phạm vi phù hợp và không được xâm phạm đến quyền, lợi ích hợp pháp của bạn [1] [2].
- Người công khai dữ liệu phải kiểm soát chặt chẽ việc công khai và ngăn chặn các hành vi tiếp cận, phát tán trái phép thông tin đó [1].

Nội dung căn cứ vào bản trích tuyển được cung cấp và chưa xác minh đối chiếu toàn văn với văn bản chính thức ban hành [1].

Nguồn là bản Word/trích tuyển được cung cấp, chưa xác minh toàn bộ câu chữ với bản chính thức; không coi ghi chú biên tập là quy định pháp luật.

Để áp dụng vào trường hợp của bạn:
- Bạn và chủ trọ có thỏa thuận nào trong hợp đồng về việc sử dụng thông tin cá nhân chưa?
- Chủ trọ đang đăng công khai thông tin của bạn vì mục đích cụ thể nào?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

**Nguồn của từng dòng có trích dẫn:**

- Chủ trọ không được tự ý đăng công khai hình ảnh giấy tờ hoặc số điện thoại của bạn trừ khi có sự đồng ý của bạn hoặc thuộc các trường hợp pháp luật cho phép [1].
  [1: Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 — bản Word cung cấp — Điều 16. Công khai dữ liệu cá nhân](https://vanban.chinhphu.vn/?docid=214590&pageid=27160)
- Dữ liệu cá nhân chỉ được công khai khi bạn đồng ý, thực hiện theo quy định pháp luật, thực hiện nghĩa vụ hợp đồng hoặc để phòng chống tội phạm và vi phạm pháp luật theo quy định [1].
  [1: Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 — bản Word cung cấp — Điều 16. Công khai dữ liệu cá nhân](https://vanban.chinhphu.vn/?docid=214590&pageid=27160)
- Sự đồng ý của bạn chỉ có hiệu lực khi hoàn toàn tự nguyện và bạn được biết rõ loại dữ liệu, mục đích xử lý cùng các quyền, nghĩa vụ liên quan [3].
  [3: Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 — bản Word cung cấp — Điều 9. Sự đồng ý của chủ thể dữ liệu cá nhân | Khoản 2](https://vanban.chinhphu.vn/?docid=214590&pageid=27160)
- Việc xử lý và công khai thông tin phải có mục đích cụ thể, phạm vi phù hợp và không được xâm phạm đến quyền, lợi ích hợp pháp của bạn [1] [2].
  [1: Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 — bản Word cung cấp — Điều 16. Công khai dữ liệu cá nhân](https://vanban.chinhphu.vn/?docid=214590&pageid=27160); [2: Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 — bản Word cung cấp — Điều 3. Nguyên tắc bảo vệ dữ liệu cá nhân | Khoản 2](https://vanban.chinhphu.vn/?docid=214590&pageid=27160)
- Người công khai dữ liệu phải kiểm soát chặt chẽ việc công khai và ngăn chặn các hành vi tiếp cận, phát tán trái phép thông tin đó [1].
  [1: Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 — bản Word cung cấp — Điều 16. Công khai dữ liệu cá nhân](https://vanban.chinhphu.vn/?docid=214590&pageid=27160)
- Nội dung căn cứ vào bản trích tuyển được cung cấp và chưa xác minh đối chiếu toàn văn với văn bản chính thức ban hành [1].
  [1: Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 — bản Word cung cấp — Điều 16. Công khai dữ liệu cá nhân](https://vanban.chinhphu.vn/?docid=214590&pageid=27160)

**Đối chiếu nguyên mẫu:**

Nhãn tổng hợp: **partial**; nhãn Qwen gốc: **high**. Đáp án khớp cao với các nguyên tắc pháp lý về bảo vệ dữ liệu cá nhân và quyền riêng tư.

**Rà mẫu/nguồn:** Không được bêu riếu/trái mục đích nhưng luật Điều 16 có các trường hợp công khai hợp pháp; không kết luận mọi công khai đều cấm. Căn cứ/mức phạt cần xác minh hiện hành.

| Điểm | Trích mẫu có thật | Trích câu trả lời có thật | Giải thích |
|---|---|---|---|
| matched | **Hoàn toàn KHÔNG ĐƯỢC PHÉP và là hành vi vi phạm pháp luật.** | Chủ trọ không được tự ý đăng công khai hình ảnh giấy tờ hoặc số điện thoại của bạn trừ khi có sự đồng ý của bạn hoặc thuộc các trường hợp pháp luật cho phép [1]. | Chủ trọ hoàn toàn không được phép đăng công khai thông tin cá nhân vì đây là hành vi vi phạm pháp luật. |
| matched | **Xâm phạm đời tư:** Dữ liệu cá nhân chỉ được công khai khi có sự đồng ý của bạn. | - Dữ liệu cá nhân chỉ được công khai khi bạn đồng ý, thực hiện theo quy định pháp luật, thực hiện nghĩa vụ hợp đồng hoặc để phòng chống tội phạm và vi phạm pháp luật theo quy định [1]. | Dữ liệu cá nhân chỉ được công khai khi có sự đồng ý tự nguyện của bạn hoặc thuộc trường hợp pháp luật cho phép. |
| different | Chủ trọ không được lấy cớ nợ tiền phòng hay tranh chấp cọc để đăng ảnh CCCD, số điện thoại của người thuê lên mạng xã hội để bêu rếu, đòi nợ. | - Bạn và chủ trọ có thỏa thuận nào trong hợp đồng về việc sử dụng thông tin cá nhân chưa? | Chủ trọ không thể lấy cớ tranh chấp để đăng ảnh CCCD hay số điện thoại nhằm bêu rếu người thuê. |

### Câu 54: Nếu thông tin cá nhân của tôi bị chia sẻ sai mục đích, tôi nên yêu cầu xử lý như thế nào?

Dữ liệu cá nhân chỉ được xử lý đúng mục đích, nên khi nghi ngờ bị chia sẻ sai phạm vi hoặc mục đích, bạn có quyền gửi văn bản yêu cầu rút lại sự đồng ý hoặc hạn chế xử lý dữ liệu [2] [3].

- Lập yêu cầu bằng văn bản dưới dạng giấy, dạng điện tử hoặc định dạng kiểm chứng được gửi đến bên kiểm soát dữ liệu cá nhân hoặc bên kiểm soát và xử lý dữ liệu cá nhân [2].
- Nêu rõ nội dung rút lại sự đồng ý, yêu cầu hạn chế xử lý, phản đối xử lý hoặc yêu cầu xóa dữ liệu cá nhân bị chia sẻ sai mục đích [1] [2].
- Theo dõi thời hạn phản hồi thủ tục trong 02 ngày làm việc từ bên kiểm soát dữ liệu cá nhân hoặc bên kiểm soát và xử lý dữ liệu cá nhân [1].
- Đôn đốc bên tiếp nhận thực hiện ngừng xử lý trong thời hạn 15 ngày, hoặc 20 ngày nếu cần yêu cầu bên thứ ba hoặc bên xử lý dữ liệu cá nhân ngừng xử lý [1].

Quyền rút lại sự đồng ý hoặc hạn chế xử lý không áp dụng đối với hoạt động xử lý dữ liệu diễn ra trước thời điểm bạn đưa ra yêu cầu [2].
Quy định cho phép không cần sự đồng ý của chủ thể dữ liệu trong các trường hợp luật định như tình trạng khẩn cấp, bảo vệ tính mạng sức khỏe cấp bách hoặc phục vụ quản lý nhà nước [1] [2].

Nguồn là bản Word/trích tuyển được cung cấp, chưa xác minh toàn bộ câu chữ với bản chính thức; không coi ghi chú biên tập là quy định pháp luật.

Để áp dụng vào trường hợp của bạn:
- Bên thu thập và chia sẻ thông tin cá nhân của bạn hiện là chủ trọ, bên môi giới hay một bên thứ ba nào khác?
- Mục đích sử dụng dữ liệu cá nhân ban đầu giữa bạn và bên thu thập đã được thỏa thuận như thế nào?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

**Nguồn của từng dòng có trích dẫn:**

- Dữ liệu cá nhân chỉ được xử lý đúng mục đích, nên khi nghi ngờ bị chia sẻ sai phạm vi hoặc mục đích, bạn có quyền gửi văn bản yêu cầu rút lại sự đồng ý hoặc hạn chế xử lý dữ liệu [2] [3].
  [2: Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 — bản Word cung cấp — Điều 10. Yêu cầu rút lại sự đồng ý, yêu cầu hạn chế xử lý dữ liệu cá nhân](https://vanban.chinhphu.vn/?docid=214590&pageid=27160); [3: Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 — bản Word cung cấp — Điều 3. Nguyên tắc bảo vệ dữ liệu cá nhân | Khoản 2](https://vanban.chinhphu.vn/?docid=214590&pageid=27160)
- Lập yêu cầu bằng văn bản dưới dạng giấy, dạng điện tử hoặc định dạng kiểm chứng được gửi đến bên kiểm soát dữ liệu cá nhân hoặc bên kiểm soát và xử lý dữ liệu cá nhân [2].
  [2: Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 — bản Word cung cấp — Điều 10. Yêu cầu rút lại sự đồng ý, yêu cầu hạn chế xử lý dữ liệu cá nhân](https://vanban.chinhphu.vn/?docid=214590&pageid=27160)
- Nêu rõ nội dung rút lại sự đồng ý, yêu cầu hạn chế xử lý, phản đối xử lý hoặc yêu cầu xóa dữ liệu cá nhân bị chia sẻ sai mục đích [1] [2].
  [1: Nghị định 356/2025/NĐ-CP — bản Word cung cấp — Điều 5. Thực hiện quyền của chủ thể dữ liệu cá nhân](https://vanban.chinhphu.vn/?classid=1&docid=216387&pageid=27160); [2: Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 — bản Word cung cấp — Điều 10. Yêu cầu rút lại sự đồng ý, yêu cầu hạn chế xử lý dữ liệu cá nhân](https://vanban.chinhphu.vn/?docid=214590&pageid=27160)
- Theo dõi thời hạn phản hồi thủ tục trong 02 ngày làm việc từ bên kiểm soát dữ liệu cá nhân hoặc bên kiểm soát và xử lý dữ liệu cá nhân [1].
  [1: Nghị định 356/2025/NĐ-CP — bản Word cung cấp — Điều 5. Thực hiện quyền của chủ thể dữ liệu cá nhân](https://vanban.chinhphu.vn/?classid=1&docid=216387&pageid=27160)
- Đôn đốc bên tiếp nhận thực hiện ngừng xử lý trong thời hạn 15 ngày, hoặc 20 ngày nếu cần yêu cầu bên thứ ba hoặc bên xử lý dữ liệu cá nhân ngừng xử lý [1].
  [1: Nghị định 356/2025/NĐ-CP — bản Word cung cấp — Điều 5. Thực hiện quyền của chủ thể dữ liệu cá nhân](https://vanban.chinhphu.vn/?classid=1&docid=216387&pageid=27160)
- Quyền rút lại sự đồng ý hoặc hạn chế xử lý không áp dụng đối với hoạt động xử lý dữ liệu diễn ra trước thời điểm bạn đưa ra yêu cầu [2].
  [2: Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 — bản Word cung cấp — Điều 10. Yêu cầu rút lại sự đồng ý, yêu cầu hạn chế xử lý dữ liệu cá nhân](https://vanban.chinhphu.vn/?docid=214590&pageid=27160)
- Quy định cho phép không cần sự đồng ý của chủ thể dữ liệu trong các trường hợp luật định như tình trạng khẩn cấp, bảo vệ tính mạng sức khỏe cấp bách hoặc phục vụ quản lý nhà nước [1] [2].
  [1: Nghị định 356/2025/NĐ-CP — bản Word cung cấp — Điều 5. Thực hiện quyền của chủ thể dữ liệu cá nhân](https://vanban.chinhphu.vn/?classid=1&docid=216387&pageid=27160); [2: Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 — bản Word cung cấp — Điều 10. Yêu cầu rút lại sự đồng ý, yêu cầu hạn chế xử lý dữ liệu cá nhân](https://vanban.chinhphu.vn/?docid=214590&pageid=27160)

**Đối chiếu nguyên mẫu:**

Nhãn tổng hợp: **partial**; nhãn Qwen gốc: **high**. Đáp án thiếu bước thu thập bằng chứng nhưng có các biện pháp xử lý khác.

**Rà mẫu/nguồn:** Ưu tiên quyền yêu cầu chấm dứt, hạn chế/xóa theo điều kiện và lưu chứng cứ. Vi bằng, thủ tục tố cáo chuyên sâu và tên cơ quan cần cập nhật; không mặc định xóa ngay trong mọi trường hợp.

| Điểm | Trích mẫu có thật | Trích câu trả lời có thật | Giải thích |
|---|---|---|---|
| matched | **Bước 1 — Yêu cầu gỡ bỏ ngay lập tức:** Gửi tin nhắn/văn bản yêu cầu chủ trọ rút lại hành vi, xóa bài đăng và chấm dứt chia sẻ thông tin theo quy định của Luật Bảo vệ dữ liệu cá nhân. | - Nêu rõ nội dung rút lại sự đồng ý, yêu cầu hạn chế xử lý, phản đối xử lý hoặc yêu cầu xóa dữ liệu cá nhân bị chia sẻ sai mục đích [1] [2]. | Yêu cầu gỡ bỏ ngay lập tức thông tin bị chia sẻ sai mục đích. |
| different | **Bước 3 — Trình báo cơ quan chức năng:** Làm đơn tố cáo gửi đến **Thanh tra Sở Thông tin và Truyền thông TP. | Dữ liệu cá nhân chỉ được xử lý đúng mục đích, nên khi nghi ngờ bị chia sẻ sai phạm vi hoặc mục đích, bạn có quyền gửi văn bản yêu cầu rút lại sự đồng ý hoặc hạn chế xử lý dữ liệu [2] [3]. | Trình báo cơ quan chức năng như Thanh tra Sở TT&TT hoặc Công an để xử lý. |
| matched | Cần Thơ** hoặc **Phòng An ninh mạng & PCTP công nghệ cao (PA05) Công an TP. | - Đôn đốc bên tiếp nhận thực hiện ngừng xử lý trong thời hạn 15 ngày, hoặc 20 ngày nếu cần yêu cầu bên thứ ba hoặc bên xử lý dữ liệu cá nhân ngừng xử lý [1]. | Yêu cầu bên kiểm soát dữ liệu thực hiện ngừng xử lý trong thời hạn quy định. |
| missing | **Bước 2 — Thu thập bằng chứng:** Chụp ảnh màn hình toàn bộ bài đăng, link bài viết, các bình luận liên quan, thời gian đăng; |  | Thu thập bằng chứng như chụp ảnh màn hình bài đăng và liên quan. |

### Câu 55: Người đăng yêu cầu đặt cọc trước nhưng không cho xem phòng: tôi nên kiểm tra những dấu hiệu rủi ro nào?

Khuyến nghị người thuê không tự ý chuyển tiền khi chưa xác minh rõ ràng vì việc thúc ép đặt cọc giữ chỗ trước khi xem phòng là dấu hiệu lừa đảo phổ biến [1] [2].

- Kiểm tra mức giá và nội dung bài đăng nếu phòng trọ được quảng cáo giá siêu rẻ hoặc thấp hơn nhiều so với thị trường kèm vị trí đẹp [1] [2].
- Cảnh giác khi tài khoản đăng tin có tương tác ảo hoặc bài đăng sao chép lại hình ảnh và địa chỉ từ nơi khác [1].
- Nhận diện việc người đăng viện cớ chủ đi vắng hoặc có nhiều người đang hỏi thuê để thúc ép chuyển tiền cọc giữ chỗ trước khi đến xem phòng [1] [2].
- Đề phòng thủ đoạn gửi giấy tờ xác nhận giả hoặc đòi chuyển thêm tiền với lý do sai nội dung chuyển khoản trước khi chặn liên lạc [1].

Thông tin dựa trên khuyến cáo cảnh báo thủ đoạn lừa đảo của cơ quan Công an và không thay thế cho các quy định pháp luật về giao dịch đặt cọc nhà ở [1] [2].

Hướng dẫn/khuyến cáo của Cổng Thông tin điện tử Bộ Công an bài Công an tỉnh Tuyên Quang; không phải điều luật. Tình huống gốc là đặt khách sạn tại Tuyên Quang. Áp dụng tham khảo cho chứng cứ giao dịch trực tuyến, không gọi là vụ thuê trọ CTU; không phải danh mục hồ sơ bắt buộc hoặc hướng dẫn soạn đơn tập thể.
Hướng dẫn/khuyến cáo của Cổng Thông tin điện tử Bộ Công an bài Công an TP Hải Phòng; không phải điều luật. Chỉ lấy phần thuê trọ và an toàn giao dịch; các thủ đoạn học phí, học bổng ngoài mục tiêu dự án. Không suy ra mọi tranh chấp cọc đều là tội phạm hay chắc chắn thu hồi được tiền.

Để áp dụng vào trường hợp của bạn:
- Bạn đã chuyển khoản bất kỳ khoản tiền nào cho người đăng tin này hay chưa?
- Người đăng tin có cung cấp giấy tờ tùy thân hoặc hợp đồng biên nhận đặt cọc nào không?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

**Nguồn của từng dòng có trích dẫn:**

- Khuyến nghị người thuê không tự ý chuyển tiền khi chưa xác minh rõ ràng vì việc thúc ép đặt cọc giữ chỗ trước khi xem phòng là dấu hiệu lừa đảo phổ biến [1] [2].
  [1: Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 — Cổng Thông tin điện tử Bộ Công an bài Công an tỉnh Tuyên Quang — Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 | Đoạn nguyên văn 12](https://bocongan.gov.vn/bai-viet/canh-giac-thu-doan-lua-dao-mao-danh-fanpage-khach-san-nha-hang-dat-coc-truc-tuyen-dip-le-hoi-thanh-tuyen-2026-1790041513); [2: Cảnh báo các thủ đoạn lừa đảo học sinh tân sinh viên mùa tựu trường — Cổng Thông tin điện tử Bộ Công an bài Công an TP Hải Phòng — Cảnh báo các thủ đoạn lừa đảo học sinh tân sinh viên mùa tựu trường | Đoạn nguyên văn 12](https://bocongan.gov.vn/bai-viet/catp-hai-phong-canh-bao-cac-thu-doan-lua-dao-bua-vay-hoc-sinh-tan-sinh-vien-mua-tuu-truong-1787629964)
- Kiểm tra mức giá và nội dung bài đăng nếu phòng trọ được quảng cáo giá siêu rẻ hoặc thấp hơn nhiều so với thị trường kèm vị trí đẹp [1] [2].
  [1: Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 — Cổng Thông tin điện tử Bộ Công an bài Công an tỉnh Tuyên Quang — Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 | Đoạn nguyên văn 12](https://bocongan.gov.vn/bai-viet/canh-giac-thu-doan-lua-dao-mao-danh-fanpage-khach-san-nha-hang-dat-coc-truc-tuyen-dip-le-hoi-thanh-tuyen-2026-1790041513); [2: Cảnh báo các thủ đoạn lừa đảo học sinh tân sinh viên mùa tựu trường — Cổng Thông tin điện tử Bộ Công an bài Công an TP Hải Phòng — Cảnh báo các thủ đoạn lừa đảo học sinh tân sinh viên mùa tựu trường | Đoạn nguyên văn 12](https://bocongan.gov.vn/bai-viet/catp-hai-phong-canh-bao-cac-thu-doan-lua-dao-bua-vay-hoc-sinh-tan-sinh-vien-mua-tuu-truong-1787629964)
- Cảnh giác khi tài khoản đăng tin có tương tác ảo hoặc bài đăng sao chép lại hình ảnh và địa chỉ từ nơi khác [1].
  [1: Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 — Cổng Thông tin điện tử Bộ Công an bài Công an tỉnh Tuyên Quang — Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 | Đoạn nguyên văn 12](https://bocongan.gov.vn/bai-viet/canh-giac-thu-doan-lua-dao-mao-danh-fanpage-khach-san-nha-hang-dat-coc-truc-tuyen-dip-le-hoi-thanh-tuyen-2026-1790041513)
- Nhận diện việc người đăng viện cớ chủ đi vắng hoặc có nhiều người đang hỏi thuê để thúc ép chuyển tiền cọc giữ chỗ trước khi đến xem phòng [1] [2].
  [1: Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 — Cổng Thông tin điện tử Bộ Công an bài Công an tỉnh Tuyên Quang — Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 | Đoạn nguyên văn 12](https://bocongan.gov.vn/bai-viet/canh-giac-thu-doan-lua-dao-mao-danh-fanpage-khach-san-nha-hang-dat-coc-truc-tuyen-dip-le-hoi-thanh-tuyen-2026-1790041513); [2: Cảnh báo các thủ đoạn lừa đảo học sinh tân sinh viên mùa tựu trường — Cổng Thông tin điện tử Bộ Công an bài Công an TP Hải Phòng — Cảnh báo các thủ đoạn lừa đảo học sinh tân sinh viên mùa tựu trường | Đoạn nguyên văn 12](https://bocongan.gov.vn/bai-viet/catp-hai-phong-canh-bao-cac-thu-doan-lua-dao-bua-vay-hoc-sinh-tan-sinh-vien-mua-tuu-truong-1787629964)
- Đề phòng thủ đoạn gửi giấy tờ xác nhận giả hoặc đòi chuyển thêm tiền với lý do sai nội dung chuyển khoản trước khi chặn liên lạc [1].
  [1: Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 — Cổng Thông tin điện tử Bộ Công an bài Công an tỉnh Tuyên Quang — Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 | Đoạn nguyên văn 12](https://bocongan.gov.vn/bai-viet/canh-giac-thu-doan-lua-dao-mao-danh-fanpage-khach-san-nha-hang-dat-coc-truc-tuyen-dip-le-hoi-thanh-tuyen-2026-1790041513)
- Thông tin dựa trên khuyến cáo cảnh báo thủ đoạn lừa đảo của cơ quan Công an và không thay thế cho các quy định pháp luật về giao dịch đặt cọc nhà ở [1] [2].
  [1: Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 — Cổng Thông tin điện tử Bộ Công an bài Công an tỉnh Tuyên Quang — Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 | Đoạn nguyên văn 12](https://bocongan.gov.vn/bai-viet/canh-giac-thu-doan-lua-dao-mao-danh-fanpage-khach-san-nha-hang-dat-coc-truc-tuyen-dip-le-hoi-thanh-tuyen-2026-1790041513); [2: Cảnh báo các thủ đoạn lừa đảo học sinh tân sinh viên mùa tựu trường — Cổng Thông tin điện tử Bộ Công an bài Công an TP Hải Phòng — Cảnh báo các thủ đoạn lừa đảo học sinh tân sinh viên mùa tựu trường | Đoạn nguyên văn 12](https://bocongan.gov.vn/bai-viet/catp-hai-phong-canh-bao-cac-thu-doan-lua-dao-bua-vay-hoc-sinh-tan-sinh-vien-mua-tuu-truong-1787629964)

**Đối chiếu nguyên mẫu:**

Nhãn tổng hợp: **high**; nhãn Qwen gốc: **high**. Đoạn trả lời bao phủ hầu hết các dấu hiệu rủi ro chính được nêu trong tài liệu tham khảo.

**Rà mẫu/nguồn:** Nhận diện dấu hiệu, không kết luận tội phạm chỉ từ yêu cầu cọc hoặc giá rẻ. Ví dụ 300–500 nghìn là minh họa của mẫu, không mức cọc pháp luật hoặc số liệu khảo sát.

| Điểm | Trích mẫu có thật | Trích câu trả lời có thật | Giải thích |
|---|---|---|---|
| matched | Đây là **thủ đoạn lừa cọc kinh điển** đối với tân sinh viên. | Khuyến nghị người thuê không tự ý chuyển tiền khi chưa xác minh rõ ràng vì việc thúc ép đặt cọc giữ chỗ trước khi xem phòng là dấu hiệu lừa đảo phổ biến [1] [2]. | Đoạn trả lời xác nhận việc thúc ép đặt cọc trước khi xem phòng là dấu hiệu lừa đảo phổ biến. |
| matched | **Viện lý do không gặp trực tiếp:** Viện cớ chủ nhà đi vắng/bận công tác, hoặc "phòng đang có nhiều người hỏi, chuyển cọc 300k – 500k giữ chỗ rồi mới dắt đi xem". | - Nhận diện việc người đăng viện cớ chủ đi vắng hoặc có nhiều người đang hỏi thuê để thúc ép chuyển tiền cọc giữ chỗ trước khi đến xem phòng [1] [2]. | Nội dung khớp với các lý do viện cớ chủ đi vắng hoặc nhiều người hỏi để ép chuyển tiền giữ chỗ. |
| matched | **Phòng ảnh đẹp, giá rẻ bất thường:** Hình ảnh phòng rất đẹp, giá rẻ hơn mặt bằng chung, nhưng địa chỉ mập mờ hoặc đến nơi thì là nhà của người khác không hề cho thuê. | - Kiểm tra mức giá và nội dung bài đăng nếu phòng trọ được quảng cáo giá siêu rẻ hoặc thấp hơn nhiều so với thị trường kèm vị trí đẹp [1] [2]. | Đoạn trả lời cảnh báo về giá siêu rẻ kèm vị trí đẹp nhưng địa chỉ mập mờ hoặc không phải phòng cho thuê. |
| matched | **Tài khoản ảo, từ chối video call:** Sử dụng tài khoản mạng xã hội ảo, số điện thoại rác; | - Cảnh giác khi tài khoản đăng tin có tương tác ảo hoặc bài đăng sao chép lại hình ảnh và địa chỉ từ nơi khác [1]. | Trả lời đề phòng tài khoản ảo, tương tác giả và bài đăng sao chép hình ảnh từ nơi khác. |
| matched | - **Nguyên tắc an toàn:** **Không xem được phòng tận mắt $\rightarrow$ Tuyệt đối không chuyển bất kỳ khoản tiền nào.** | Khuyến nghị người thuê không tự ý chuyển tiền khi chưa xác minh rõ ràng vì việc thúc ép đặt cọc giữ chỗ trước khi xem phòng là dấu hiệu lừa đảo phổ biến [1] [2]. | Khuyến nghị không chuyển tiền khi chưa xác minh rõ ràng trước khi xem phòng tận mắt. |

### Câu 56: Tôi đã chuyển cọc cho một tin trọ có dấu hiệu giả mạo; nên lưu lại bằng chứng gì và trình báo ở đâu?

Bạn cần lưu giữ toàn bộ chứng cứ trao đổi, chuyển khoản và báo ngay cho cơ quan Công an nơi gần nhất hoặc cơ quan có trách nhiệm tiếp nhận tin báo để được xử lý theo quy định [1] [2].

- Khuyến nghị lưu lại đầy đủ bằng chứng gồm hình ảnh tin nhắn trao đổi, thông tin tài khoản ngân hàng nhận tiền và biên lai hoặc phiếu giao dịch chuyển khoản [1].
- Khuyến nghị thực hiện thao tác Báo cáo đối với trang hoặc tài khoản có dấu hiệu giả mạo trên nền tảng mạng xã hội nếu giao dịch diễn ra qua Facebook [1].
- Mang toàn bộ hồ sơ chứng cứ đến trình báo tại Cơ quan Công an nơi gần nhất hoặc Cơ quan điều tra, Viện kiểm sát để được hướng dẫn tiếp nhận tố giác, tin báo về tội phạm [1] [2].

Khuyến cáo về bằng chứng thu thập dựa trên cảnh báo lừa đảo trực tuyến của cơ quan Công an và không thay thế cho danh mục hồ sơ tố tụng chính thức [1].
Nguồn trích tuyển quy định trách nhiệm tiếp nhận thuộc Cơ quan điều tra, Viện kiểm sát và cơ quan khác, việc thẩm quyền giải quyết cụ thể phụ thuộc vào từng giai đoạn điều tra [2] [3].

Hướng dẫn/khuyến cáo của Cổng Thông tin điện tử Bộ Công an bài Công an tỉnh Tuyên Quang; không phải điều luật. Tình huống gốc là đặt khách sạn tại Tuyên Quang. Áp dụng tham khảo cho chứng cứ giao dịch trực tuyến, không gọi là vụ thuê trọ CTU; không phải danh mục hồ sơ bắt buộc hoặc hướng dẫn soạn đơn tập thể.
Nguồn là bản Word/trích tuyển được cung cấp, chưa xác minh toàn bộ câu chữ với bản chính thức; không coi ghi chú biên tập là quy định pháp luật.

Để áp dụng vào trường hợp của bạn:
- Bạn đã chuyển tiền qua tài khoản ngân hàng nào và còn giữ biên lai xác nhận giao dịch không?
- Bạn tiếp cận tin đăng phòng trọ qua nền tảng nào và hiện đối tượng đã chặn liên lạc chưa?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

**Nguồn của từng dòng có trích dẫn:**

- Bạn cần lưu giữ toàn bộ chứng cứ trao đổi, chuyển khoản và báo ngay cho cơ quan Công an nơi gần nhất hoặc cơ quan có trách nhiệm tiếp nhận tin báo để được xử lý theo quy định [1] [2].
  [1: Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 — Cổng Thông tin điện tử Bộ Công an bài Công an tỉnh Tuyên Quang — Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 | Đoạn nguyên văn 12](https://bocongan.gov.vn/bai-viet/canh-giac-thu-doan-lua-dao-mao-danh-fanpage-khach-san-nha-hang-dat-coc-truc-tuyen-dip-le-hoi-thanh-tuyen-2026-1790041513); [2: Bộ luật Tố tụng hình sự 17/VBHN-VPQH — bản Word trích tuyển cung cấp — Điều 145. Trách nhiệm tiếp nhận và thẩm quyền giải quyết tố giác, tin báo về tội phạm, kiến nghị khởi tố | Khoản 2](https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-17-vbhn-vpqh-468961.htm)
- Khuyến nghị lưu lại đầy đủ bằng chứng gồm hình ảnh tin nhắn trao đổi, thông tin tài khoản ngân hàng nhận tiền và biên lai hoặc phiếu giao dịch chuyển khoản [1].
  [1: Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 — Cổng Thông tin điện tử Bộ Công an bài Công an tỉnh Tuyên Quang — Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 | Đoạn nguyên văn 12](https://bocongan.gov.vn/bai-viet/canh-giac-thu-doan-lua-dao-mao-danh-fanpage-khach-san-nha-hang-dat-coc-truc-tuyen-dip-le-hoi-thanh-tuyen-2026-1790041513)
- Khuyến nghị thực hiện thao tác Báo cáo đối với trang hoặc tài khoản có dấu hiệu giả mạo trên nền tảng mạng xã hội nếu giao dịch diễn ra qua Facebook [1].
  [1: Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 — Cổng Thông tin điện tử Bộ Công an bài Công an tỉnh Tuyên Quang — Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 | Đoạn nguyên văn 12](https://bocongan.gov.vn/bai-viet/canh-giac-thu-doan-lua-dao-mao-danh-fanpage-khach-san-nha-hang-dat-coc-truc-tuyen-dip-le-hoi-thanh-tuyen-2026-1790041513)
- Mang toàn bộ hồ sơ chứng cứ đến trình báo tại Cơ quan Công an nơi gần nhất hoặc Cơ quan điều tra, Viện kiểm sát để được hướng dẫn tiếp nhận tố giác, tin báo về tội phạm [1] [2].
  [1: Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 — Cổng Thông tin điện tử Bộ Công an bài Công an tỉnh Tuyên Quang — Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 | Đoạn nguyên văn 12](https://bocongan.gov.vn/bai-viet/canh-giac-thu-doan-lua-dao-mao-danh-fanpage-khach-san-nha-hang-dat-coc-truc-tuyen-dip-le-hoi-thanh-tuyen-2026-1790041513); [2: Bộ luật Tố tụng hình sự 17/VBHN-VPQH — bản Word trích tuyển cung cấp — Điều 145. Trách nhiệm tiếp nhận và thẩm quyền giải quyết tố giác, tin báo về tội phạm, kiến nghị khởi tố | Khoản 2](https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-17-vbhn-vpqh-468961.htm)
- Khuyến cáo về bằng chứng thu thập dựa trên cảnh báo lừa đảo trực tuyến của cơ quan Công an và không thay thế cho danh mục hồ sơ tố tụng chính thức [1].
  [1: Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 — Cổng Thông tin điện tử Bộ Công an bài Công an tỉnh Tuyên Quang — Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 | Đoạn nguyên văn 12](https://bocongan.gov.vn/bai-viet/canh-giac-thu-doan-lua-dao-mao-danh-fanpage-khach-san-nha-hang-dat-coc-truc-tuyen-dip-le-hoi-thanh-tuyen-2026-1790041513)
- Nguồn trích tuyển quy định trách nhiệm tiếp nhận thuộc Cơ quan điều tra, Viện kiểm sát và cơ quan khác, việc thẩm quyền giải quyết cụ thể phụ thuộc vào từng giai đoạn điều tra [2] [3].
  [2: Bộ luật Tố tụng hình sự 17/VBHN-VPQH — bản Word trích tuyển cung cấp — Điều 145. Trách nhiệm tiếp nhận và thẩm quyền giải quyết tố giác, tin báo về tội phạm, kiến nghị khởi tố | Khoản 2](https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-17-vbhn-vpqh-468961.htm); [3: Bộ luật Tố tụng hình sự 17/VBHN-VPQH — bản Word trích tuyển cung cấp — Điều 145. Trách nhiệm tiếp nhận và thẩm quyền giải quyết tố giác, tin báo về tội phạm, kiến nghị khởi tố | Khoản 3](https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-17-vbhn-vpqh-468961.htm)

**Đối chiếu nguyên mẫu:**

Nhãn tổng hợp: **partial**; nhãn Qwen gốc: **high**. Đáp án bao phủ đầy đủ các bằng chứng cần lưu và địa điểm trình báo chính xác theo tài liệu tham khảo.

**Rà mẫu/nguồn:** Nêu chứng cứ và nơi tiếp nhận cơ bản; không lập đơn hoặc điền mẫu. Không hạn chế trình báo duy nhất nơi chuyển tiền nếu nguồn luật cho phép nhiều nơi tiếp nhận.

| Điểm | Trích mẫu có thật | Trích câu trả lời có thật | Giải thích |
|---|---|---|---|
| matched | - Biên lai chuyển tiền ngân hàng (chụp rõ số tài khoản người nhận, tên chủ tài khoản, ngân hàng, mã giao dịch, thời gian chuyển). | - Khuyến nghị lưu lại đầy đủ bằng chứng gồm hình ảnh tin nhắn trao đổi, thông tin tài khoản ngân hàng nhận tiền và biên lai hoặc phiếu giao dịch chuyển khoản [1]. | Lưu biên lai chuyển tiền với đầy đủ thông tin tài khoản và mã giao dịch. |
| matched | - Toàn bộ ảnh chụp màn hình tin nhắn thỏa thuận qua Zalo/Messenger từ đầu đến khi bị chặn. | - Khuyến nghị lưu lại đầy đủ bằng chứng gồm hình ảnh tin nhắn trao đổi, thông tin tài khoản ngân hàng nhận tiền và biên lai hoặc phiếu giao dịch chuyển khoản [1]. | Lưu toàn bộ ảnh chụp màn hình tin nhắn trao đổi từ đầu đến khi bị chặn. |
| different | - Số điện thoại, link trang cá nhân, ảnh đại diện, ảnh bài đăng phòng trọ giả mạo. | - Khuyến nghị lưu lại đầy đủ bằng chứng gồm hình ảnh tin nhắn trao đổi, thông tin tài khoản ngân hàng nhận tiền và biên lai hoặc phiếu giao dịch chuyển khoản [1]. | Lưu số điện thoại, link trang cá nhân và ảnh đại diện của đối tượng lừa đảo. |
| matched | - Nộp Đơn tố giác tội phạm tại **Công an phường/xã nơi bạn thực hiện chuyển tiền**, hoặc Công an quận/huyện sở tại. | Bạn cần lưu giữ toàn bộ chứng cứ trao đổi, chuyển khoản và báo ngay cho cơ quan Công an nơi gần nhất hoặc cơ quan có trách nhiệm tiếp nhận tin báo để được xử lý theo quy định [1] [2]. | Trình báo tại Công an phường/xã nơi thực hiện chuyển tiền hoặc quận/huyện sở tại. |
| different | - Trình báo đến **Đội Cảnh sát hình sự** hoặc **Phòng An ninh mạng & PCTP công nghệ cao (PA05) Công an TP. | Bạn cần lưu giữ toàn bộ chứng cứ trao đổi, chuyển khoản và báo ngay cho cơ quan Công an nơi gần nhất hoặc cơ quan có trách nhiệm tiếp nhận tin báo để được xử lý theo quy định [1] [2]. | Trình báo đến Đội Cảnh sát hình sự hoặc Phòng An ninh mạng & PCTP công nghệ cao. |

### Câu 57: Khi nào tranh chấp tiền cọc có thể có dấu hiệu lừa đảo, và khi nào chỉ là tranh chấp hợp đồng?

Vụ việc có dấu hiệu lừa đảo khi một bên dùng thủ đoạn gian dối như đưa thông tin sai sự thật để nhận tiền cọc rồi chặn liên lạc nhằm chiếm đoạt tài sản, trong khi tranh chấp hợp đồng là mâu thuẫn phát sinh trong quá trình thực hiện cam kết thuê trọ và các khoản chi phí giữa hai bên [1] [2] [3].

- Dấu hiệu nghi ngờ lừa đảo xuất hiện khi bên nhận tiền dùng thủ đoạn gian dối như đăng tin phòng giá rẻ rồi viện lý do thúc ép cọc giữ chỗ trước khi xem phòng, sau đó lập tức chặn liên lạc để chiếm đoạt tiền [2] [3].
- Tranh chấp hợp đồng thường xảy ra khi các bên đã xác lập thỏa thuận nhưng phát sinh bất đồng về việc thay đổi thỏa thuận ban đầu, thu thêm các khoản phí hoặc xử lý tiền cọc khi chấm dứt thuê trước hạn [1].
- Khuyến nghị người thuê không đặt cọc nếu chưa gặp trực tiếp chủ nhà và chưa kiểm tra giấy tờ nhà cùng căn cước để xác nhận quyền sở hữu [1].
- Khuyến nghị đọc kỹ, giữ tối thiểu một bản chính hợp đồng hoặc biên nhận đặt cọc, và báo ngay cơ quan Công an gần nhất khi phát hiện dấu hiệu nghi vấn lừa đảo [1] [3].

Căn cứ về tội lừa đảo chiếm đoạt tài sản được trích từ bản Word văn bản hợp nhất được cung cấp, chưa đối chiếu toàn bộ với văn bản chính thức [2].
Các dấu hiệu nhận biết và khuyến cáo giao dịch từ Chợ Tốt và Công an thành phố Hải Phòng mang tính cảnh báo thực tế, không phải quy định phân định tranh chấp hợp đồng trong mọi tình huống [1] [3].

Hướng dẫn/khuyến cáo của Trợ Giúp Chợ Tốt; không phải điều luật. Mẹo giao dịch, không phải điều luật. Không chứng minh hạn hoàn cọc cố định hoặc mức cọc bắt buộc; không thay thế xác minh người được ủy quyền cho thuê. Chỉ đọc phần kiểm tra, không bổ sung mẫu soạn hợp đồng.
Nguồn là bản Word/trích tuyển được cung cấp, chưa xác minh toàn bộ câu chữ với bản chính thức; không coi ghi chú biên tập là quy định pháp luật.
Hướng dẫn/khuyến cáo của Cổng Thông tin điện tử Bộ Công an bài Công an TP Hải Phòng; không phải điều luật. Chỉ lấy phần thuê trọ và an toàn giao dịch; các thủ đoạn học phí, học bổng ngoài mục tiêu dự án. Không suy ra mọi tranh chấp cọc đều là tội phạm hay chắc chắn thu hồi được tiền.

Để áp dụng vào trường hợp của bạn:
- Bên nhận cọc có đưa ra thông tin giả mạo về phòng trọ hoặc chủ sở hữu rồi lập tức cắt đứt liên lạc sau khi nhận tiền không?
- Hai bên đã ký kết hợp đồng hoặc biên nhận cọc bằng văn bản với các điều khoản cụ thể về việc xử lý tiền cọc chưa?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

**Nguồn của từng dòng có trích dẫn:**

- Vụ việc có dấu hiệu lừa đảo khi một bên dùng thủ đoạn gian dối như đưa thông tin sai sự thật để nhận tiền cọc rồi chặn liên lạc nhằm chiếm đoạt tài sản, trong khi tranh chấp hợp đồng là mâu thuẫn phát sinh trong quá trình thực hiện cam kết thuê trọ và các khoản chi phí giữa hai bên [1] [2] [3].
  [1: Mẹo khi thuê phòng — Trợ Giúp Chợ Tốt — Mẹo khi thuê phòng | Đoạn nguyên văn 78](https://trogiup.chotot.com/nguoi-mua/meo-khi-thue-phong/); [2: Bộ luật Hình sự 135/VBHN-VPQH — bản Word trích tuyển cung cấp — Điều 174. Tội lừa đảo chiếm đoạt tài sản | Khoản 1](https://congbao.chinhphu.vn/tai-ve-van-ban-so-135-vbhn-vpqh-46165-58894?format=pdf); [3: Cảnh báo các thủ đoạn lừa đảo học sinh tân sinh viên mùa tựu trường — Cổng Thông tin điện tử Bộ Công an bài Công an TP Hải Phòng — Cảnh báo các thủ đoạn lừa đảo học sinh tân sinh viên mùa tựu trường | Đoạn nguyên văn 12](https://bocongan.gov.vn/bai-viet/catp-hai-phong-canh-bao-cac-thu-doan-lua-dao-bua-vay-hoc-sinh-tan-sinh-vien-mua-tuu-truong-1787629964)
- Dấu hiệu nghi ngờ lừa đảo xuất hiện khi bên nhận tiền dùng thủ đoạn gian dối như đăng tin phòng giá rẻ rồi viện lý do thúc ép cọc giữ chỗ trước khi xem phòng, sau đó lập tức chặn liên lạc để chiếm đoạt tiền [2] [3].
  [2: Bộ luật Hình sự 135/VBHN-VPQH — bản Word trích tuyển cung cấp — Điều 174. Tội lừa đảo chiếm đoạt tài sản | Khoản 1](https://congbao.chinhphu.vn/tai-ve-van-ban-so-135-vbhn-vpqh-46165-58894?format=pdf); [3: Cảnh báo các thủ đoạn lừa đảo học sinh tân sinh viên mùa tựu trường — Cổng Thông tin điện tử Bộ Công an bài Công an TP Hải Phòng — Cảnh báo các thủ đoạn lừa đảo học sinh tân sinh viên mùa tựu trường | Đoạn nguyên văn 12](https://bocongan.gov.vn/bai-viet/catp-hai-phong-canh-bao-cac-thu-doan-lua-dao-bua-vay-hoc-sinh-tan-sinh-vien-mua-tuu-truong-1787629964)
- Tranh chấp hợp đồng thường xảy ra khi các bên đã xác lập thỏa thuận nhưng phát sinh bất đồng về việc thay đổi thỏa thuận ban đầu, thu thêm các khoản phí hoặc xử lý tiền cọc khi chấm dứt thuê trước hạn [1].
  [1: Mẹo khi thuê phòng — Trợ Giúp Chợ Tốt — Mẹo khi thuê phòng | Đoạn nguyên văn 78](https://trogiup.chotot.com/nguoi-mua/meo-khi-thue-phong/)
- Khuyến nghị người thuê không đặt cọc nếu chưa gặp trực tiếp chủ nhà và chưa kiểm tra giấy tờ nhà cùng căn cước để xác nhận quyền sở hữu [1].
  [1: Mẹo khi thuê phòng — Trợ Giúp Chợ Tốt — Mẹo khi thuê phòng | Đoạn nguyên văn 78](https://trogiup.chotot.com/nguoi-mua/meo-khi-thue-phong/)
- Khuyến nghị đọc kỹ, giữ tối thiểu một bản chính hợp đồng hoặc biên nhận đặt cọc, và báo ngay cơ quan Công an gần nhất khi phát hiện dấu hiệu nghi vấn lừa đảo [1] [3].
  [1: Mẹo khi thuê phòng — Trợ Giúp Chợ Tốt — Mẹo khi thuê phòng | Đoạn nguyên văn 78](https://trogiup.chotot.com/nguoi-mua/meo-khi-thue-phong/); [3: Cảnh báo các thủ đoạn lừa đảo học sinh tân sinh viên mùa tựu trường — Cổng Thông tin điện tử Bộ Công an bài Công an TP Hải Phòng — Cảnh báo các thủ đoạn lừa đảo học sinh tân sinh viên mùa tựu trường | Đoạn nguyên văn 12](https://bocongan.gov.vn/bai-viet/catp-hai-phong-canh-bao-cac-thu-doan-lua-dao-bua-vay-hoc-sinh-tan-sinh-vien-mua-tuu-truong-1787629964)
- Căn cứ về tội lừa đảo chiếm đoạt tài sản được trích từ bản Word văn bản hợp nhất được cung cấp, chưa đối chiếu toàn bộ với văn bản chính thức [2].
  [2: Bộ luật Hình sự 135/VBHN-VPQH — bản Word trích tuyển cung cấp — Điều 174. Tội lừa đảo chiếm đoạt tài sản | Khoản 1](https://congbao.chinhphu.vn/tai-ve-van-ban-so-135-vbhn-vpqh-46165-58894?format=pdf)
- Các dấu hiệu nhận biết và khuyến cáo giao dịch từ Chợ Tốt và Công an thành phố Hải Phòng mang tính cảnh báo thực tế, không phải quy định phân định tranh chấp hợp đồng trong mọi tình huống [1] [3].
  [1: Mẹo khi thuê phòng — Trợ Giúp Chợ Tốt — Mẹo khi thuê phòng | Đoạn nguyên văn 78](https://trogiup.chotot.com/nguoi-mua/meo-khi-thue-phong/); [3: Cảnh báo các thủ đoạn lừa đảo học sinh tân sinh viên mùa tựu trường — Cổng Thông tin điện tử Bộ Công an bài Công an TP Hải Phòng — Cảnh báo các thủ đoạn lừa đảo học sinh tân sinh viên mùa tựu trường | Đoạn nguyên văn 12](https://bocongan.gov.vn/bai-viet/catp-hai-phong-canh-bao-cac-thu-doan-lua-dao-bua-vay-hoc-sinh-tan-sinh-vien-mua-tuu-truong-1787629964)

**Đối chiếu nguyên mẫu:**

Nhãn tổng hợp: **high**; nhãn Qwen gốc: **high**. Đoạn trả lời bao phủ đầy đủ các ý chính về phân định tranh chấp hợp đồng và dấu hiệu lừa đảo so với văn bản tham khảo.

**Rà mẫu/nguồn:** Thủ đoạn, ý định chiếm đoạt và chứng cứ quyết định phân biệt; không suy ra mọi cắt liên lạc là tội phạm. Tên TAND quận/huyện cần cập nhật theo tổ chức hiện hành; tránh tư vấn tố tụng chuyên sâu.

| Điểm | Trích mẫu có thật | Trích câu trả lời có thật | Giải thích |
|---|---|---|---|
| matched | - **Tranh chấp hợp đồng dân sự:** Phòng trọ có thật, người cho thuê đúng là chủ nhà hoặc người được ủy quyền hợp pháp. | - Tranh chấp hợp đồng thường xảy ra khi các bên đã xác lập thỏa thuận nhưng phát sinh bất đồng về việc thay đổi thỏa thuận ban đầu, thu thêm các khoản phí hoặc xử lý tiền cọc khi chấm dứt thuê trước hạn [1]. | Tranh chấp hợp đồng xảy ra khi có phòng trọ thật và người cho thuê là chủ nhà hoặc được ủy quyền. |
| matched | Tranh chấp phát sinh do bất đồng về tiền cọc hoàn trả, hư hỏng đồ đạc, tiền điện nước hoặc việc chuyển đi sớm. | Vụ việc có dấu hiệu lừa đảo khi một bên dùng thủ đoạn gian dối như đưa thông tin sai sự thật để nhận tiền cọc rồi chặn liên lạc nhằm chiếm đoạt tài sản, trong khi tranh chấp hợp đồng là mâu thuẫn phát sinh trong quá trình thực hiện cam kết | Tranh chấp hợp đồng phát sinh từ bất đồng về tiền cọc hoàn trả, hư hỏng đồ đạc hoặc việc chuyển đi sớm. |
| matched | - **Dấu hiệu lừa đảo chiếm đoạt tài sản (Điều 174 BLHS):** Đối tượng dùng **thủ đoạn gian dối ngay từ đầu**: dùng phòng ảo, giả mạo chủ nhà, lấy cọc của nhiều người cho một phòng rồi cố tình chặn liên lạc, bỏ trốn để chiếm đoạt tiền. | Vụ việc có dấu hiệu lừa đảo khi một bên dùng thủ đoạn gian dối như đưa thông tin sai sự thật để nhận tiền cọc rồi chặn liên lạc nhằm chiếm đoạt tài sản, trong khi tranh chấp hợp đồng là mâu thuẫn phát sinh trong quá trình thực hiện cam kết | Dấu hiệu lừa đảo là khi đối tượng dùng thủ đoạn gian dối ngay từ đầu như dùng phòng ảo, giả mạo chủ nhà để chiếm đoạt tiền. |
| matched | Vụ việc thuộc thẩm quyền tiếp nhận, điều tra của **Cơ quan Cảnh sát điều tra (Công an)**. | - Khuyến nghị đọc kỹ, giữ tối thiểu một bản chính hợp đồng hoặc biên nhận đặt cọc, và báo ngay cơ quan Công an gần nhất khi phát hiện dấu hiệu nghi vấn lừa đảo [1] [3]. | Vụ việc có dấu hiệu lừa đảo thuộc thẩm quyền điều tra của Cơ quan Cảnh sát điều tra (Công an). |

### Câu 58: Nếu có nhiều sinh viên cùng bị một người nhận cọc rồi cắt liên lạc, chúng tôi nên cung cấp thông tin gì cho cơ quan có thẩm quyền?

Khi nghi ngờ hoặc trở thành nạn nhân của hành vi lừa đảo trực tuyến, người dân cần thu thập toàn bộ chứng cứ liên quan và báo ngay cho Cơ quan Công an nơi gần nhất để được hướng dẫn, tiếp nhận và xử lý theo quy định [1].

- Thu thập và lưu lại hình ảnh tin nhắn trao đổi giữa các bên làm chứng cứ giao dịch [1].
- Cung cấp thông tin tài khoản ngân hàng của đối tượng đã nhận tiền đặt cọc [1].
- Cung cấp các phiếu giao dịch hoặc sao kê chuyển khoản chứng minh việc đã chuyển tiền đặt cọc [1].
- Thực hiện thao tác báo cáo trang có dấu hiệu giả mạo, lừa đảo với nền tảng trực tuyến [1].

Cơ quan điều tra, Viện kiểm sát và các cơ quan, tổ chức khác có trách nhiệm tiếp nhận tố giác, tin báo về tội phạm theo quy định của pháp luật [2].
Cơ quan có thẩm quyền giải quyết tố giác, tin báo về tội phạm có trách nhiệm thông báo kết quả giải quyết cho cá nhân, tổ chức đã tố giác [3].

Hướng dẫn/khuyến cáo của Cổng Thông tin điện tử Bộ Công an bài Công an tỉnh Tuyên Quang; không phải điều luật. Tình huống gốc là đặt khách sạn tại Tuyên Quang. Áp dụng tham khảo cho chứng cứ giao dịch trực tuyến, không gọi là vụ thuê trọ CTU; không phải danh mục hồ sơ bắt buộc hoặc hướng dẫn soạn đơn tập thể.
Nguồn là bản Word/trích tuyển được cung cấp, chưa xác minh toàn bộ câu chữ với bản chính thức; không coi ghi chú biên tập là quy định pháp luật.

Để áp dụng vào trường hợp của bạn:
- Bạn và các sinh viên khác đã tập hợp đầy đủ hình ảnh tin nhắn và biên lai chuyển khoản chưa?
- Bạn đã xác định được cơ quan Công an nơi gần nhất để đến trình báo chưa?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

**Nguồn của từng dòng có trích dẫn:**

- Khi nghi ngờ hoặc trở thành nạn nhân của hành vi lừa đảo trực tuyến, người dân cần thu thập toàn bộ chứng cứ liên quan và báo ngay cho Cơ quan Công an nơi gần nhất để được hướng dẫn, tiếp nhận và xử lý theo quy định [1].
  [1: Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 — Cổng Thông tin điện tử Bộ Công an bài Công an tỉnh Tuyên Quang — Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 | Đoạn nguyên văn 12](https://bocongan.gov.vn/bai-viet/canh-giac-thu-doan-lua-dao-mao-danh-fanpage-khach-san-nha-hang-dat-coc-truc-tuyen-dip-le-hoi-thanh-tuyen-2026-1790041513)
- Thu thập và lưu lại hình ảnh tin nhắn trao đổi giữa các bên làm chứng cứ giao dịch [1].
  [1: Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 — Cổng Thông tin điện tử Bộ Công an bài Công an tỉnh Tuyên Quang — Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 | Đoạn nguyên văn 12](https://bocongan.gov.vn/bai-viet/canh-giac-thu-doan-lua-dao-mao-danh-fanpage-khach-san-nha-hang-dat-coc-truc-tuyen-dip-le-hoi-thanh-tuyen-2026-1790041513)
- Cung cấp thông tin tài khoản ngân hàng của đối tượng đã nhận tiền đặt cọc [1].
  [1: Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 — Cổng Thông tin điện tử Bộ Công an bài Công an tỉnh Tuyên Quang — Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 | Đoạn nguyên văn 12](https://bocongan.gov.vn/bai-viet/canh-giac-thu-doan-lua-dao-mao-danh-fanpage-khach-san-nha-hang-dat-coc-truc-tuyen-dip-le-hoi-thanh-tuyen-2026-1790041513)
- Cung cấp các phiếu giao dịch hoặc sao kê chuyển khoản chứng minh việc đã chuyển tiền đặt cọc [1].
  [1: Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 — Cổng Thông tin điện tử Bộ Công an bài Công an tỉnh Tuyên Quang — Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 | Đoạn nguyên văn 12](https://bocongan.gov.vn/bai-viet/canh-giac-thu-doan-lua-dao-mao-danh-fanpage-khach-san-nha-hang-dat-coc-truc-tuyen-dip-le-hoi-thanh-tuyen-2026-1790041513)
- Thực hiện thao tác báo cáo trang có dấu hiệu giả mạo, lừa đảo với nền tảng trực tuyến [1].
  [1: Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 — Cổng Thông tin điện tử Bộ Công an bài Công an tỉnh Tuyên Quang — Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 | Đoạn nguyên văn 12](https://bocongan.gov.vn/bai-viet/canh-giac-thu-doan-lua-dao-mao-danh-fanpage-khach-san-nha-hang-dat-coc-truc-tuyen-dip-le-hoi-thanh-tuyen-2026-1790041513)
- Cơ quan điều tra, Viện kiểm sát và các cơ quan, tổ chức khác có trách nhiệm tiếp nhận tố giác, tin báo về tội phạm theo quy định của pháp luật [2].
  [2: Bộ luật Tố tụng hình sự 17/VBHN-VPQH — bản Word trích tuyển cung cấp — Điều 145. Trách nhiệm tiếp nhận và thẩm quyền giải quyết tố giác, tin báo về tội phạm, kiến nghị khởi tố | Khoản 2](https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-17-vbhn-vpqh-468961.htm)
- Cơ quan có thẩm quyền giải quyết tố giác, tin báo về tội phạm có trách nhiệm thông báo kết quả giải quyết cho cá nhân, tổ chức đã tố giác [3].
  [3: Bộ luật Tố tụng hình sự 17/VBHN-VPQH — bản Word trích tuyển cung cấp — Điều 145. Trách nhiệm tiếp nhận và thẩm quyền giải quyết tố giác, tin báo về tội phạm, kiến nghị khởi tố | Khoản 4](https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-17-vbhn-vpqh-468961.htm)

**Đối chiếu nguyên mẫu:**

Nhãn tổng hợp: **partial**; nhãn Qwen gốc: **high**. Đáp án bao phủ hầu hết ý chính về chứng cứ và nơi nộp đơn nhưng khác biệt ở danh sách nạn nhân chi tiết và địa điểm cụ thể.

**Rà mẫu/nguồn:** Nhiều người bị hại không tự chứng minh tính chuyên nghiệp hoặc tự động một khung tăng nặng. Tổng hợp giao dịch/chứng cứ hữu ích; không lập đơn tập thể hoặc kết luận định tội thay cơ quan có thẩm quyền.

| Điểm | Trích mẫu có thật | Trích câu trả lời có thật | Giải thích |
|---|---|---|---|
| matched | **Đơn tố giác tội phạm tập thể:** Có chữ ký, thông tin CCCD, số điện thoại của toàn bộ nạn nhân; | - Cung cấp thông tin tài khoản ngân hàng của đối tượng đã nhận tiền đặt cọc [1]. | Cần cung cấp danh sách nạn nhân với chữ ký và thông tin CCCD. |
| matched | tường trình chi tiết thủ đoạn gian dối của đối tượng. | - Thu thập và lưu lại hình ảnh tin nhắn trao đổi giữa các bên làm chứng cứ giao dịch [1]. | Phải tường trình chi tiết thủ đoạn gian dối của đối tượng. |
| different | **Bảng thống kê danh sách nạn nhân:** Liệt kê họ tên, số tiền bị chiếm đoạt, ngày chuyển tiền, số tài khoản thụ hưởng. | - Cung cấp các phiếu giao dịch hoặc sao kê chuyển khoản chứng minh việc đã chuyển tiền đặt cọc [1]. | Cần cung cấp bảng thống kê danh sách nạn nhân với số tiền và ngày chuyển. |
| matched | **Tài liệu chứng cứ tập thể:** Toàn bộ sao kê/biên lai chuyển tiền của tất cả các nạn nhân vào cùng tài khoản đối tượng; | - Cung cấp các phiếu giao dịch hoặc sao kê chuyển khoản chứng minh việc đã chuyển tiền đặt cọc [1]. | Phải nộp toàn bộ sao kê/biên lai chuyển tiền của tất cả nạn nhân. |
| matched | ảnh chụp các đoạn tin nhắn thể hiện cùng một kịch bản lừa đảo. | - Thu thập và lưu lại hình ảnh tin nhắn trao đổi giữa các bên làm chứng cứ giao dịch [1]. | Cần cung cấp ảnh chụp tin nhắn thể hiện cùng một kịch bản lừa đảo. |
| different | **Nơi tiếp nhận:** Nộp trực tiếp tại **Cơ quan Cảnh sát điều tra Công an quận/huyện** nơi xảy ra vụ việc hoặc **Phòng Cảnh sát hình sự Công an TP. | Khi nghi ngờ hoặc trở thành nạn nhân của hành vi lừa đảo trực tuyến, người dân cần thu thập toàn bộ chứng cứ liên quan và báo ngay cho Cơ quan Công an nơi gần nhất để được hướng dẫn, tiếp nhận và xử lý theo quy định [1]. | Nộp trực tiếp tại Cơ quan Cảnh sát điều tra Công an quận/huyện nơi xảy ra vụ việc. |

## Khả năng tái lập

- IDs gốc: `[19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58]`.
- Bộ đáp án: `876e38dba5c2faeba797d02503680b82c1eb7d6bd30b148737cf47db84e36983`.
- Manifest: `30fa24717c1c333b750ea4079f6a15771ed58391d26b820ff161c86f39e7ffb8`.
- Pipeline: `de8b30183da45706a7cf5f757c550c097a65da17a2cfa7c4e86e8b8e359f275b`.
- Rubric: `local_selected_fragment_quote_audit_text_agreement_v8`; mã bộ chấm `769756dbc33ae04c28c9702bec94f80d53f44b0f4b20f1661558f3f17cf8fad8`.
- Tổng hợp nhãn: `audited_main_point_consistency_v1`; mã xử lý báo cáo `28d5ee53589e364c868f261f9970d229b29b1cb848ad97f6bfa7f49be6c7fdf6`.
- `.gitattributes` giữ nguyên byte các gói Word và bộ mẫu. Các thay đổi xuống dòng khi lưu Git không đổi nội dung; SHA được đối chiếu với byte thực dùng trong lượt chạy.
- Chi tiết cục bộ: `eval/reports/graph_rag_priority7_36_v20_2026-10-06.json`, `graph_rag_priority7_baseline_review_v23_2026-10-06.json`, `graph_rag_priority7_reference_review_v23_2026-10-06.json`, `graph_rag_priority7_audit_v13_2026-10-06.json`.
- Các báo cáo raw giữ cục bộ theo `.gitignore`; báo cáo này chỉ xuất 36 câu pháp lý, không xuất Datahouse hoặc thông tin người dùng.
