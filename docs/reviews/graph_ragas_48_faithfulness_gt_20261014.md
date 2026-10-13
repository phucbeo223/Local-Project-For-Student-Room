# Câu trả lời, nguồn và điểm RAGAS · Pháp lý & KTX

Cập nhật báo cáo: 2026-10-14T02:47:29.895666+07:00. Đã lưu 48/48 câu trả lời.

Pipeline pháp lý: gemini-3.1-flash-lite → qwen3.5:9b → gemini-3.8-flash-high; model chấm: gemini-3.8-flash-high; RAGAS 0.3.9.

## Phạm vi và cách đọc

- Lượt này có 48 câu từ ngân hàng 66 câu. Các mã đã chọn: 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66.
- Câu trả lời và nguồn được lấy từ hệ thống thật, không dùng đáp án sinh ra làm đáp án chuẩn.
- Schema pháp lý: legal_ctu_ktx_v2_20261007; schema tin trọ: housing_graph_word_repair_v16. Tác nhân bật; Graph RAG bật.
- Đo trực tiếp tầng service với database thật; tắt ghi sự kiện tổng hợp trong lượt đánh giá. Độ trễ không bao gồm trình duyệt và HTTP.
- Nhánh tra cứu danh mục KTX có thể trả lời bằng dữ liệu có cấu trúc; provider thực tế được ghi ở từng câu.
- Faithfulness đo mức câu trả lời được các đoạn truy xuất hỗ trợ; Answer Relevancy đo liên quan câu hỏi; Context Utilization đo mức ngữ cảnh hữu dụng cho phản hồi.
- Context Recall và Context Precision ở lượt này là RAGAS IDBasedContextRecall/IDBasedContextPrecision: so khớp tập tài liệu/nguồn được truy xuất với ID nguồn liên quan gán theo từng câu. Đây là độ bao phủ ở cấp tài liệu, không phải tỷ lệ bao phủ từng mệnh đề trong đáp án.
- Các ID nguồn chuẩn được gán từ corpus và tài liệu KTX được nêu trong câu hỏi, không lấy từ câu trả lời của chatbot. Nhãn hiện do một lượt rà soát tạo; cần rà soát độc lập trước khi dùng như chuẩn vàng đã xác nhận.
- Chưa có đáp án chuẩn dạng nội dung do chuyên gia xác nhận: không báo Answer Correctness hay LLM Context Recall. Điểm ID-based không xác nhận độ đúng pháp lý.
- Nếu không truy xuất nguồn, IDBasedContextRecall là 0 khi bộ nguồn chuẩn không rỗng; IDBasedContextPrecision là N/A vì không có nguồn được xếp hạng. Faithfulness và Context Utilization là N/A; Answer Relevancy vẫn có thể được chấm.
- Điểm RAGAS không chứng minh luật còn hiệu lực hoặc câu trả lời đúng pháp lý. Câu lỗi/chưa chấm không được gán điểm 0.
- Nếu model sinh và chấm cùng họ Gemini thì có thể có thiên lệch. Tên model được ghi theo cấu hình endpoint; alias proxy chưa xác minh mô hình nền.
- Phí, kỳ tính giá, GPS và chỗ trống KTX cần đọc cùng giới hạn nguồn được nêu trong từng phản hồi.
- Faithfulness so với lượt 13/10: 0.5749 → 0.9116 trên cùng 48 mã câu. Đây là so sánh chỉ báo, không hoàn toàn đồng điều kiện vì lượt mới siết hướng dẫn tổng hợp và đưa metadata phạm vi nguồn vào ngữ cảnh judge.

## Điểm tổng hợp

| Chỉ số | Trung bình | Số điểm hợp lệ |
|---|---:|---:|
| faithfulness | 0.9116 | 47/48 |
| answer_relevancy | 0.7655 | 48/48 |
| context_utilization | 0.9431 | 47/48 |
| context_recall | 0.7934 | 48/48 |
| context_precision | 0.8653 | 47/48 |

## Điểm theo nhóm câu hỏi

| Nhóm | Chỉ số | Trung bình | Số điểm hợp lệ |
|---|---|---:|---:|
| Pháp lý | faithfulness | 0.9106 | 36/36 |
| Pháp lý | answer_relevancy | 0.7478 | 36/36 |
| Pháp lý | context_utilization | 0.9303 | 36/36 |
| Pháp lý | context_recall | 0.7755 | 36/36 |
| Pháp lý | context_precision | 0.8426 | 36/36 |
| KTX | faithfulness | 0.9146 | 11/12 |
| KTX | answer_relevancy | 0.8184 | 12/12 |
| KTX | context_utilization | 0.9848 | 11/12 |
| KTX | context_recall | 0.8472 | 12/12 |
| KTX | context_precision | 0.9394 | 11/12 |

## So sánh Faithfulness với lượt 13/10

| Lượt | Điểm | Số câu có điểm |
|---|---:|---:|
| 13/10/2026 | 0.5749 | 47/48 |
| 14/10/2026 | 0.9116 | 47/48 |

Mức tăng mang tính chỉ báo, chưa hoàn toàn đồng điều kiện: lượt này siết hướng dẫn tổng hợp và đưa metadata giới hạn/phạm vi nguồn vào ngữ cảnh chấm Faithfulness; lượt 13/10 chưa dùng cùng metadata.


## Câu 19 · Hợp đồng

Trước khi ký hợp đồng thuê trọ, sinh viên nên kiểm tra những điều khoản nào?

Trạng thái: Đã trả lời · cần rà nguồn. Provider: gemini-agent; model: gemini-3.8-flash-high.

faithfulness: 0.9565 | answer_relevancy: 0.9009 | context_utilization: 1.0 | context_recall: 1.0 | context_precision: 0.6667

ID nguồn chuẩn: housing79-word.json, civil91-word.json

ID nguồn đã truy xuất: housing79-word.json, civil91-word.json, supplement-s02-word.json

Khuyến nghị đối chiếu các nội dung luật định về nhà ở kết hợp đọc kỹ quyền lợi, chi phí và tài sản theo hướng dẫn thực tế trước khi ký hợp đồng [1] [3].

- Nguồn quy định hợp đồng về nhà ở phải gồm thông tin các bên, mô tả đặc điểm nhà ở và thửa đất ở gắn liền, thời hạn thuê và thời gian giao nhận [1].
- Nguồn quy định hợp đồng phải nêu giá thuê, thời hạn và phương thức thanh toán, thời điểm có hiệu lực, ngày tháng năm ký kết cùng chữ ký các bên [1].
- Nguồn quy định các bên thỏa thuận về quyền, nghĩa vụ, cam kết và các thỏa thuận khác trong hợp đồng [1] [2].
- Khuyến nghị đọc kỹ các điều khoản về quyền lợi, trách nhiệm, giá thuê phòng, tiền đặt cọc, giá điện nước, internet và dịch vụ đi kèm [3].
- Khuyến nghị đối chiếu danh mục và tình trạng tài sản trang bị thực tế với hợp đồng trước khi nhận phòng [3].

Nội dung kinh nghiệm kiểm tra thực tế mang tính khuyến cáo tham khảo, không phải điều khoản quy phạm pháp luật bắt buộc [3].

Nguồn là bản Word/trích tuyển được cung cấp, chưa xác minh toàn bộ câu chữ với bản chính thức; không coi ghi chú biên tập là quy định pháp luật.
Hướng dẫn/khuyến cáo của Thư viện Đại học Bách khoa Hà Nội; không phải điều luật. Chỉ lấy phần kiểm tra thuê phòng; thông tin ký túc xá, xe buýt và địa bàn Hà Nội không áp dụng cho CTU. Không có ngày công bố hiển thị trong nội dung đã đọc; đây không phải quy định pháp luật.

### Nguồn và ngữ cảnh

**[1] [Luật Nhà ở — 79/VBHN-VPQH — bản Word cung cấp](https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-79-vbhn-vpqh-469209.htm)**

Điều 163. Hợp đồng về nhà ở · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_corpus_v7_20261005/housing79-word.json

```text
Hợp đồng về nhà ở do các bên thỏa thuận và phải được lập thành văn bản bao gồm các nội dung sau đây:

1. Họ và tên của cá nhân, tên của tổ chức và địa chỉ của các bên;

2. Mô tả đặc điểm của nhà ở giao dịch và đặc điểm của thửa đất ở gắn với nhà ở đó.

Đối với hợp đồng mua bán, hợp đồng thuê mua căn hộ chung cư thì các bên phải ghi rõ phần sở hữu chung, sử dụng chung; thời hạn sử dụng nhà chung cư theo hồ sơ thiết kế; diện tích sử dụng thuộc quyền sở hữu riêng; diện tích sàn căn hộ; mục đích sử dụng của phần sở hữu chung, sử dụng chung trong nhà chung cư theo đúng mục đích thiết kế đã được phê duyệt; giá dịch vụ quản lý vận hành nhà chung cư trong trường hợp chưa tổ chức Hội nghị nhà chung cư lần đầu; trách nhiệm đóng, mức đóng kinh phí bảo trì và thông tin tài khoản nộp kinh phí bảo trì;

3. Giá trị góp vốn, giá giao dịch nhà ở nếu hợp đồng có thỏa thuận về giá; trường hợp mua bán, cho thuê mua, cho thuê nhà ở mà Nhà nước có quy định về giá thì các bên phải thực hiện theo quy định đó;

4. Thời hạn và phương thức thanh toán tiền nếu là trường hợp mua bán, cho thuê mua, cho thuê nhà ở;

5. Thời gian giao nhận nhà ở; thời gian bảo hành nhà ở nếu là mua, thuê mua nhà ở được đầu tư xây dựng mới; thời hạn cho thuê mua, cho thuê, thế chấp, cho mượn, cho ở nhờ, ủy quyền quản lý nhà ở; thời hạn góp vốn; thời hạn sở hữu đối với trường hợp mua bán nhà ở có thời hạn;

6. Quyền và nghĩa vụ của các bên.

Trường hợp thuê mua nhà ở thì phải ghi rõ quyền và nghĩa vụ của các bên về việc sửa chữa hư hỏng của nhà ở trong quá trình thuê mua;

7. Cam kết của các bên;

8. Thỏa thuận khác;

9. Thời điểm có hiệu lực của hợp đồng;

10. Ngày, tháng, năm ký kết hợp đồng;

11. Chữ ký và ghi rõ họ, tên của các bên, nếu là tổ chức thì phải đóng dấu (nếu có) và ghi rõ chức vụ của người ký.
```

**[2] [Bộ luật Dân sự 91/2015/QH13 — Word do cơ quan nhà nước công bố](https://congan.daklak.gov.vn/laws/detail/Bo-luat-Dan-su-163/)**

Điều 398. Nội dung của hợp đồng · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_repair_corpus_v14_20261006/civil91-word.json

```text
1. Các bên trong hợp đồng có quyền thỏa thuận về nội dung trong hợp đồng.

2. Hợp đồng có thể có các nội dung sau đây:

a) Đối tượng của hợp đồng;

b) Số lượng, chất lượng;

c) Giá, phương thức thanh toán;

d) Thời hạn, địa điểm, phương thức thực hiện hợp đồng;

đ) Quyền, nghĩa vụ của các bên;

e) Trách nhiệm do vi phạm hợp đồng;

g) Phương thức giải quyết tranh chấp.
```

**[3] [Kinh nghiệm tìm nhà trọ cho tân sinh viên — Thư viện Đại học Bách khoa Hà Nội](https://library.hust.edu.vn/vi/node/822)**

Kinh nghiệm tìm nhà trọ cho tân sinh viên | Đoạn nguyên văn 23 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_supplement_corpus_v8_20261005/supplement-s02-word.json

```text
Làm hợp đồng khi thuê nhà

Khi thuê nhà bạn cần thuê tại những nơi có hợp đồng thuê trọ rõ ràng, được ký xác nhận và mỗi bên giữ một bản. Trước khi ký vào bản hợp đồng đó, bạn cần đọc kỹ các điều khoản của hợp đồng về quyền lợi, trách nhiệm cũng như giá thuê phòng trọ, tiền đặt cọc, giá điện nước, intenet và các dịch vụ đi kèm.

Một điều lưu ý là bạn cần kiểm tra những tài sản được trang bị cho nơi ở có khớp với hợp đồng hay không và đừng quên kiểm tra tình trạng của những thiết bị này nếu có hư hỏng cần yêu cầu chủ nhà sửa chữa hoặc thay thế. Cuối cùng hãy chốt số điện, nước trên đồng hồ đo trước khi vào ở.

An toàn phòng chống cháy nổ cũng là vấn đề cần lưu ý trong việc lựa chọn nơi ở, các bạn cần lựa chọn những phòng trọ, khu trọ đảm bảo về phòng cháy chữa cháy.
```

**[4] [Bộ luật Dân sự 91/2015/QH13 — Word do cơ quan nhà nước công bố](https://congan.daklak.gov.vn/laws/detail/Bo-luat-Dan-su-163/)**

Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_repair_corpus_v14_20261006/civil91-word.json

```text
Điều 117. Điều kiện có hiệu lực của giao dịch dân sự | Khoản 1
1. Giao dịch dân sự có hiệu lực khi có đủ các điều kiện sau đây:

a) Chủ thể có năng lực pháp luật dân sự, năng lực hành vi dân sự phù hợp
với giao dịch dân sự được xác lập;

b) Chủ thể tham gia giao dịch dân sự hoàn toàn tự nguyện;

c) Mục đích và nội dung của giao dịch dân sự không vi phạm điều cấm của
luật, không trái đạo đức xã hội.

Điều 117. Điều kiện có hiệu lực của giao dịch dân sự | Khoản 2
2. Hình thức của giao dịch dân sự là điều kiện có hiệu lực của giao dịch
dân sự trong trường hợp luật có quy định.
```


## Câu 20 · Hợp đồng

Hợp đồng thuê phòng có cần ghi rõ tiền cọc, tiền thuê và ngày thanh toán không?

Trạng thái: Đã trả lời · cần rà nguồn. Provider: gemini-agent; model: gemini-3.8-flash-high.

faithfulness: 0.9231 | answer_relevancy: 0.8966 | context_utilization: 1.0 | context_recall: 1.0 | context_precision: 1.0

ID nguồn chuẩn: housing79-word.json, civil91-word.json

ID nguồn đã truy xuất: civil91-word.json, housing79-word.json

Hợp đồng về nhà ở theo quy định phải có nội dung về giá giao dịch nếu có thỏa thuận, cùng thời hạn và phương thức thanh toán tiền [2].

- Nguồn quy định hợp đồng về nhà ở phải lập thành văn bản và bao gồm giá giao dịch nhà ở nếu các bên có thỏa thuận về giá [2].
- Nguồn quy định hợp đồng cho thuê nhà ở phải có nội dung về thời hạn và phương thức thanh toán tiền [2].
- Các bên có quyền thỏa thuận các nội dung khác trong hợp đồng, bao gồm biện pháp đặt cọc để bảo đảm giao kết hoặc thực hiện hợp đồng [1] [2] [3].

Nguồn trích dẫn quy định các nội dung bắt buộc của hợp đồng về nhà ở và nguyên tắc đặt cọc chung, không quy định riêng một biểu mẫu cố định bắt buộc cho phòng trọ sinh viên [1] [2].

Nguồn là bản Word/trích tuyển được cung cấp, chưa xác minh toàn bộ câu chữ với bản chính thức; không coi ghi chú biên tập là quy định pháp luật.

### Nguồn và ngữ cảnh

**[1] [Bộ luật Dân sự 91/2015/QH13 — Word do cơ quan nhà nước công bố](https://congan.daklak.gov.vn/laws/detail/Bo-luat-Dan-su-163/)**

Điều 328. Đặt cọc · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_repair_corpus_v14_20261006/civil91-word.json

```text
1. Đặt cọc là việc một bên (sau đây gọi là bên đặt cọc) giao cho bên kia
(sau đây gọi là bên nhận đặt cọc) một khoản tiền hoặc kim khí quý, đá quý
hoặc vật có giá trị khác (sau đây gọi chung là tài sản đặt cọc) trong một
thời hạn để bảo đảm giao kết hoặc thực hiện hợp đồng.

2. Trường hợp hợp đồng được giao kết, thực hiện thì tài sản đặt cọc được
trả lại cho bên đặt cọc hoặc được trừ để thực hiện nghĩa vụ trả tiền; nếu
bên đặt cọc từ chối việc giao kết, thực hiện hợp đồng thì tài sản đặt cọc
thuộc về bên nhận đặt cọc; nếu bên nhận đặt cọc từ chối việc giao kết, thực
hiện hợp đồng thì phải trả cho bên đặt cọc tài sản đặt cọc và một khoản
tiền tương đương giá trị tài sản đặt cọc, trừ trường hợp có thỏa thuận
khác.
```

**[2] [Luật Nhà ở — 79/VBHN-VPQH — bản Word cung cấp](https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-79-vbhn-vpqh-469209.htm)**

Điều 163. Hợp đồng về nhà ở · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_corpus_v7_20261005/housing79-word.json

```text
Hợp đồng về nhà ở do các bên thỏa thuận và phải được lập thành văn bản bao gồm các nội dung sau đây:

1. Họ và tên của cá nhân, tên của tổ chức và địa chỉ của các bên;

2. Mô tả đặc điểm của nhà ở giao dịch và đặc điểm của thửa đất ở gắn với nhà ở đó.

Đối với hợp đồng mua bán, hợp đồng thuê mua căn hộ chung cư thì các bên phải ghi rõ phần sở hữu chung, sử dụng chung; thời hạn sử dụng nhà chung cư theo hồ sơ thiết kế; diện tích sử dụng thuộc quyền sở hữu riêng; diện tích sàn căn hộ; mục đích sử dụng của phần sở hữu chung, sử dụng chung trong nhà chung cư theo đúng mục đích thiết kế đã được phê duyệt; giá dịch vụ quản lý vận hành nhà chung cư trong trường hợp chưa tổ chức Hội nghị nhà chung cư lần đầu; trách nhiệm đóng, mức đóng kinh phí bảo trì và thông tin tài khoản nộp kinh phí bảo trì;

3. Giá trị góp vốn, giá giao dịch nhà ở nếu hợp đồng có thỏa thuận về giá; trường hợp mua bán, cho thuê mua, cho thuê nhà ở mà Nhà nước có quy định về giá thì các bên phải thực hiện theo quy định đó;

4. Thời hạn và phương thức thanh toán tiền nếu là trường hợp mua bán, cho thuê mua, cho thuê nhà ở;

5. Thời gian giao nhận nhà ở; thời gian bảo hành nhà ở nếu là mua, thuê mua nhà ở được đầu tư xây dựng mới; thời hạn cho thuê mua, cho thuê, thế chấp, cho mượn, cho ở nhờ, ủy quyền quản lý nhà ở; thời hạn góp vốn; thời hạn sở hữu đối với trường hợp mua bán nhà ở có thời hạn;

6. Quyền và nghĩa vụ của các bên.

Trường hợp thuê mua nhà ở thì phải ghi rõ quyền và nghĩa vụ của các bên về việc sửa chữa hư hỏng của nhà ở trong quá trình thuê mua;

7. Cam kết của các bên;

8. Thỏa thuận khác;

9. Thời điểm có hiệu lực của hợp đồng;

10. Ngày, tháng, năm ký kết hợp đồng;

11. Chữ ký và ghi rõ họ, tên của các bên, nếu là tổ chức thì phải đóng dấu (nếu có) và ghi rõ chức vụ của người ký.
```

**[3] [Bộ luật Dân sự 91/2015/QH13 — Word do cơ quan nhà nước công bố](https://congan.daklak.gov.vn/laws/detail/Bo-luat-Dan-su-163/)**

Điều 398. Nội dung của hợp đồng · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_repair_corpus_v14_20261006/civil91-word.json

```text
1. Các bên trong hợp đồng có quyền thỏa thuận về nội dung trong hợp đồng.

2. Hợp đồng có thể có các nội dung sau đây:

a) Đối tượng của hợp đồng;

b) Số lượng, chất lượng;

c) Giá, phương thức thanh toán;

d) Thời hạn, địa điểm, phương thức thực hiện hợp đồng;

đ) Quyền, nghĩa vụ của các bên;

e) Trách nhiệm do vi phạm hợp đồng;

g) Phương thức giải quyết tranh chấp.
```

**[4] [Bộ luật Dân sự 91/2015/QH13 — Word do cơ quan nhà nước công bố](https://congan.daklak.gov.vn/laws/detail/Bo-luat-Dan-su-163/)**

Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_repair_corpus_v14_20261006/civil91-word.json

```text
Điều 117. Điều kiện có hiệu lực của giao dịch dân sự | Khoản 1
1. Giao dịch dân sự có hiệu lực khi có đủ các điều kiện sau đây:

a) Chủ thể có năng lực pháp luật dân sự, năng lực hành vi dân sự phù hợp
với giao dịch dân sự được xác lập;

b) Chủ thể tham gia giao dịch dân sự hoàn toàn tự nguyện;

c) Mục đích và nội dung của giao dịch dân sự không vi phạm điều cấm của
luật, không trái đạo đức xã hội.

Điều 117. Điều kiện có hiệu lực của giao dịch dân sự | Khoản 2
2. Hình thức của giao dịch dân sự là điều kiện có hiệu lực của giao dịch
dân sự trong trường hợp luật có quy định.
```


## Câu 21 · Hợp đồng

Nếu chủ trọ muốn tăng giá thuê giữa thời hạn hợp đồng thì cần xem xét những gì?

Trạng thái: Đã trả lời · cần rà nguồn. Provider: gemini-agent; model: gemini-3.8-flash-high.

faithfulness: 0.9091 | answer_relevancy: 0.8959 | context_utilization: 1.0 | context_recall: 0.5 | context_precision: 1.0

ID nguồn chuẩn: housing79-word.json, civil91-word.json

ID nguồn đã truy xuất: housing79-word.json

Việc điều chỉnh giá thuê nhà ở dựa trên thỏa thuận của các bên hoặc theo điều kiện luật định khi có sự kiện cải tạo nhà ở [1] [3].

- Bên cho thuê và bên thuê được thỏa thuận về giá thuê nhà ở, trừ trường hợp Nhà nước có quy định về giá thuê thì phải thực hiện theo quy định đó [3].
- Khi bên cho thuê cải tạo nhà ở và được bên thuê đồng ý, bên cho thuê được quyền điều chỉnh giá thuê nếu thời gian cho thuê còn lại từ một phần ba thời hạn hợp đồng trở xuống [1].
- Giá thuê mới khi cải tạo do các bên tự thỏa thuận; nếu không thỏa thuận được thì bên cho thuê có quyền đơn phương chấm dứt hợp đồng và phải bồi thường theo luật định [1].

Đoạn trích tuyển cung cấp chỉ nêu căn cứ điều chỉnh giá thuê khi có thỏa thuận hoặc khi cải tạo nhà ở, chưa bao quát các trường hợp phát sinh khác [1] [3].

Nguồn là bản Word/trích tuyển được cung cấp, chưa xác minh toàn bộ câu chữ với bản chính thức; không coi ghi chú biên tập là quy định pháp luật.

### Nguồn và ngữ cảnh

**[1] [Luật Nhà ở — 79/VBHN-VPQH — bản Word cung cấp](https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-79-vbhn-vpqh-469209.htm)**

Điều 170. Thời hạn thuê, giá thuê, cho thuê lại nhà ở | Khoản 2 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_corpus_v7_20261005/housing79-word.json

```text
2. Trường hợp bên cho thuê thực hiện cải tạo nhà ở và được bên thuê đồng ý thì bên cho thuê được quyền điều chỉnh giá thuê nhà ở nếu thời gian cho thuê còn lại từ một phần ba thời hạn của hợp đồng thuê nhà ở trở xuống. Giá thuê nhà ở mới do các bên thỏa thuận; trường hợp không thỏa thuận được thì bên cho thuê có quyền đơn phương chấm dứt hợp đồng thuê nhà ở và phải bồi thường cho bên thuê theo quy định của pháp luật.
```

**[2] [Luật Nhà ở — 79/VBHN-VPQH — bản Word cung cấp](https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-79-vbhn-vpqh-469209.htm)**

Điều 163. Hợp đồng về nhà ở | Khoản 3 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_corpus_v7_20261005/housing79-word.json

```text
Hợp đồng về nhà ở do các bên thỏa thuận và phải được lập thành văn bản bao gồm các nội dung sau đây:

3. Giá trị góp vốn, giá giao dịch nhà ở nếu hợp đồng có thỏa thuận về giá; trường hợp mua bán, cho thuê mua, cho thuê nhà ở mà Nhà nước có quy định về giá thì các bên phải thực hiện theo quy định đó;
```

**[3] [Luật Nhà ở — 79/VBHN-VPQH — bản Word cung cấp](https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-79-vbhn-vpqh-469209.htm)**

Điều 170. Thời hạn thuê, giá thuê, cho thuê lại nhà ở | Khoản 1 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_corpus_v7_20261005/housing79-word.json

```text
1. Bên cho thuê và bên thuê nhà ở được thỏa thuận về thời hạn thuê, giá thuê và hình thức trả tiền thuê nhà ở theo định kỳ hoặc trả một lần; trường hợp Nhà nước có quy định về giá thuê nhà ở thì các bên phải thực hiện theo quy định đó.
```


## Câu 22 · Hợp đồng

Khi trả phòng, việc hoàn lại tiền cọc được xác định theo hợp đồng và quy định như thế nào?

Trạng thái: Trả lời một phần. Provider: gemini-agent; model: gemini-3.8-flash-high.

faithfulness: 1.0 | answer_relevancy: 0.925 | context_utilization: 0.8056 | context_recall: 0.5 | context_precision: 0.3333

ID nguồn chuẩn: housing79-word.json, civil91-word.json

ID nguồn đã truy xuất: civil91-word.json, supplement-s02-word.json, supplement-s01-word.json

Theo Bộ luật Dân sự, khi hợp đồng được giao kết và thực hiện thì tài sản đặt cọc được trả lại cho bên đặt cọc hoặc trừ để thực hiện nghĩa vụ trả tiền, trừ trường hợp có thỏa thuận khác [1].

- Nếu bên đặt cọc từ chối thực hiện hợp đồng thì tài sản đặt cọc thuộc về bên nhận đặt cọc, trừ trường hợp có thỏa thuận khác [1].
- Nếu bên nhận đặt cọc từ chối thực hiện hợp đồng thì phải trả lại tài sản đặt cọc và một khoản tiền tương đương giá trị tài sản đặt cọc, trừ trường hợp có thỏa thuận khác [1].
- Giao dịch dân sự có hiệu lực khi chủ thể có năng lực phù hợp, tự nguyện, nội dung không vi phạm điều cấm của luật, không trái đạo đức xã hội và tuân thủ hình thức nếu luật quy định [4].
- Khuyến nghị làm rõ các điều khoản về thời hạn hợp đồng và tiền đặt cọc trong trường hợp kết thúc hợp đồng trước hạn, đồng thời lưu giữ tối thiểu một bản chính biên nhận đặt cọc và hợp đồng thuê [3].

Nguồn trích dẫn không quy định thời hạn hoàn trả cọc cụ thể hay mức khấu trừ chi tiết khi trả phòng trọ [1] [3].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng.
Hướng dẫn/khuyến cáo của Trợ Giúp Chợ Tốt; không phải điều luật. Mẹo giao dịch, không phải điều luật. Không chứng minh hạn hoàn cọc cố định hoặc mức cọc bắt buộc; không thay thế xác minh người được ủy quyền cho thuê. Chỉ đọc phần kiểm tra, không bổ sung mẫu soạn hợp đồng.

### Nguồn và ngữ cảnh

**[1] [Bộ luật Dân sự 91/2015/QH13 — Word do cơ quan nhà nước công bố](https://congan.daklak.gov.vn/laws/detail/Bo-luat-Dan-su-163/)**

Điều 328. Đặt cọc · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_repair_corpus_v14_20261006/civil91-word.json

```text
1. Đặt cọc là việc một bên (sau đây gọi là bên đặt cọc) giao cho bên kia
(sau đây gọi là bên nhận đặt cọc) một khoản tiền hoặc kim khí quý, đá quý
hoặc vật có giá trị khác (sau đây gọi chung là tài sản đặt cọc) trong một
thời hạn để bảo đảm giao kết hoặc thực hiện hợp đồng.

2. Trường hợp hợp đồng được giao kết, thực hiện thì tài sản đặt cọc được
trả lại cho bên đặt cọc hoặc được trừ để thực hiện nghĩa vụ trả tiền; nếu
bên đặt cọc từ chối việc giao kết, thực hiện hợp đồng thì tài sản đặt cọc
thuộc về bên nhận đặt cọc; nếu bên nhận đặt cọc từ chối việc giao kết, thực
hiện hợp đồng thì phải trả cho bên đặt cọc tài sản đặt cọc và một khoản
tiền tương đương giá trị tài sản đặt cọc, trừ trường hợp có thỏa thuận
khác.
```

**[2] [Kinh nghiệm tìm nhà trọ cho tân sinh viên — Thư viện Đại học Bách khoa Hà Nội](https://library.hust.edu.vn/vi/node/822)**

Kinh nghiệm tìm nhà trọ cho tân sinh viên | Đoạn nguyên văn 23 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_supplement_corpus_v8_20261005/supplement-s02-word.json

```text
Làm hợp đồng khi thuê nhà

Khi thuê nhà bạn cần thuê tại những nơi có hợp đồng thuê trọ rõ ràng, được ký xác nhận và mỗi bên giữ một bản. Trước khi ký vào bản hợp đồng đó, bạn cần đọc kỹ các điều khoản của hợp đồng về quyền lợi, trách nhiệm cũng như giá thuê phòng trọ, tiền đặt cọc, giá điện nước, intenet và các dịch vụ đi kèm.

Một điều lưu ý là bạn cần kiểm tra những tài sản được trang bị cho nơi ở có khớp với hợp đồng hay không và đừng quên kiểm tra tình trạng của những thiết bị này nếu có hư hỏng cần yêu cầu chủ nhà sửa chữa hoặc thay thế. Cuối cùng hãy chốt số điện, nước trên đồng hồ đo trước khi vào ở.

An toàn phòng chống cháy nổ cũng là vấn đề cần lưu ý trong việc lựa chọn nơi ở, các bạn cần lựa chọn những phòng trọ, khu trọ đảm bảo về phòng cháy chữa cháy.
```

**[3] [Mẹo khi thuê phòng — Trợ Giúp Chợ Tốt](https://trogiup.chotot.com/nguoi-mua/meo-khi-thue-phong/)**

Mẹo khi thuê phòng | Đoạn nguyên văn 78 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_supplement_corpus_v8_20261005/supplement-s01-word.json

```text
1. Kiểm tra độ uy tín của người cho thuê trên môi trường trực tuyến (Google, Facebook, diễn đàn, …)

Tìm kiếm số điện thoại và địa chỉ muốn thuê trên Google, Facebook, các diễn đàn trực tuyến, … và xem các thông tin giao dịch trước đó như đánh giá của khách hàng về địa chỉ thuê này, …

2. Xác định địa điểm phòng muốn thuê và khảo sát mức giá chung

Tìm hiểu cụ thể địa chỉ muốn thuê gồm số nhà, tên đường, phường, quận.

Hỏi thăm trực tiếp hàng xóm xung quanh địa điểm muốn thuê và tham khảo ý kiến từ người thân, bạn bè hoặc tìm hiểu thông tin trên mạng về địa điểm này.

Mỗi khu vực sẽ có giá thuê khác nhau. Do đó, cần tìm hiểu mức giá chung theo từng khu vực trước khi thuê bằng cách so sánh với các tin đăng bất động sản cùng loại trên Chợ Tốt.

Thận trọng khi tìm được phòng ở trung tâm hoặc phòng tốt nhưng giá rẻ bất thường.

3. Không đặt cọc nếu chưa xác định được chủ nhà

Yêu cầu gặp trực tiếp chủ nhà trước khi đặt cọc.

Yêu cầu chủ nhà cho xem giấy tờ nhà và thẻ Căn Cước/thẻ Căn Cước Công Dân để xác nhận quyền sở hữu của chủ nhà

Nên chủ động hỏi kỹ về giá phòng, giá điện nước, các chi phí khác (nếu có) và các điều kiện sinh hoạt khác trước khi đặt cọc.

4. Phải đọc kỹ hợp đồng đặt cọc và hợp đồng thuê

Khi làm hợp đồng thuê cần đọc kỹ các điều khoản ghi trên hợp đồng: địa chỉ phòng, số phòng, tiền phòng cố định trong bao lâu không thay đổi, số người thuê, tiền điện, tiền nước, tiền gửi xe, sử dụng Internet và các chi phí phát sinh khác (nếu có).

Làm rõ các điều khoản về thời hạn hợp đồng và tiền đặt cọc trong trường hợp kết thúc hợp đồng trước hạn.

Luôn giữ tối thiểu một bản chính biên nhận đặt cọc và hợp đồng thuê.

5. Kiểm tra tình trạng phòng thuê trước khi đến ở

Kiểm tra tình trạng các thiết bị trong nhà và hệ thống đường điện, nước. Nếu có vấn đề hỏng hóc thì phải yêu cầu chủ nhà trọ sửa chữa hoặc thay thế.

Thống nhất số điện/nước (internet nếu có) phải trả ngay khi làm hợp đồng để tránh trường hợp phải trả thêm lượng điện/nước (internet nếu có) đã tiêu thụ trước đó.

Những trường hợp gian lận cần cảnh giác

Yêu cầu khách thuê đặt tiền cọc sau đó lật ngược những thỏa thuận ban đầu, thu thêm hàng loạt phí… là những trường hợp được người đi thuê cảnh báo:
```

**[4] [Bộ luật Dân sự 91/2015/QH13 — Word do cơ quan nhà nước công bố](https://congan.daklak.gov.vn/laws/detail/Bo-luat-Dan-su-163/)**

Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_repair_corpus_v14_20261006/civil91-word.json

```text
Điều 117. Điều kiện có hiệu lực của giao dịch dân sự | Khoản 1
1. Giao dịch dân sự có hiệu lực khi có đủ các điều kiện sau đây:

a) Chủ thể có năng lực pháp luật dân sự, năng lực hành vi dân sự phù hợp
với giao dịch dân sự được xác lập;

b) Chủ thể tham gia giao dịch dân sự hoàn toàn tự nguyện;

c) Mục đích và nội dung của giao dịch dân sự không vi phạm điều cấm của
luật, không trái đạo đức xã hội.

Điều 117. Điều kiện có hiệu lực của giao dịch dân sự | Khoản 2
2. Hình thức của giao dịch dân sự là điều kiện có hiệu lực của giao dịch
dân sự trong trường hợp luật có quy định.
```

### Lỗi và giới hạn đã ghi nhận

```json
{
  "collect": null,
  "ragas": {},
  "unavailable": null,
  "degraded": [
    "Phản hồi chưa đáp ứng đầy đủ yêu cầu chính; đánh dấu theo nội dung thay vì provider."
  ]
}
```


## Câu 23 · Điện

Chủ trọ được thu tiền điện của người thuê như thế nào theo quy định?

Trạng thái: Trả lời một phần. Provider: gemini-agent; model: gemini-3.8-flash-high.

faithfulness: 0.9167 | answer_relevancy: 0.9054 | context_utilization: 1.0 | context_recall: 0.5 | context_precision: 1.0

ID nguồn chuẩn: electricity61-word.json, electricity60-word.json

ID nguồn đã truy xuất: electricity60-word.json

Trường hợp người thuê nhà không giao kết hợp đồng trực tiếp với bên bán điện thì tổng tiền điện chủ nhà cho thuê thu của người thuê nhà không được vượt quá tiền điện trong hoá đơn tiền điện hằng tháng do đơn vị bán lẻ điện phát hành [1].

- Khi người thuê có hợp đồng thuê từ 12 tháng trở lên và có đăng ký tạm trú, thường trú thì chủ nhà trực tiếp giao kết hoặc đại diện bên thuê giao kết hợp đồng mua bán điện [1].
- Nếu thời hạn thuê dưới 12 tháng và chủ nhà không kê khai được đầy đủ số người sử dụng điện thì áp dụng giá bán lẻ điện sinh hoạt của bậc 2 (từ 101 - 200 kWh) cho toàn bộ sản lượng đo đếm tại công tơ [1].
- Nếu chủ nhà kê khai đầy đủ số người sử dụng điện thì bên bán điện cấp định mức với tỷ lệ cứ 04 người tính là một hộ sử dụng điện [1].

Quy định đối với sinh viên và người lao động thuê nhà tại điểm c khoản 5 Điều 12 có hiệu lực thi hành kể từ ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành [1] [2].
Nguồn trích dẫn là bản Word trích tuyển cung cấp và chưa xác minh toàn bộ câu chữ với bản văn bản chính thức [1].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng.
Nguồn có hiệu lực có điều kiện; chưa xác nhận văn bản/sự kiện kích hoạt.
Nguồn là bản Word/trích tuyển được cung cấp, chưa xác minh toàn bộ câu chữ với bản chính thức; không coi ghi chú biên tập là quy định pháp luật.

### Nguồn và ngữ cảnh

**[1] [Thông tư 60/2025/TT-BCT — bản Word trích tuyển cung cấp](https://vanban.chinhphu.vn/?docid=216125&orggroupid=4&pageid=27160)**

Điều 12. Giá bán lẻ điện sinh hoạt | Khoản 5 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_corpus_v7_20261005/electricity60-word.json

```text
5. Bên mua điện sử dụng vào mục đích sinh hoạt của người thuê nhà để ở áp dụng như sau:

a) Tại mỗi địa chỉ nhà cho thuê, bên bán điện chỉ giao kết một hợp đồng mua bán điện duy nhất. Chủ nhà cho thuê có trách nhiệm cung cấp thông tin về cư trú tại địa điểm sử dụng điện của người thuê nhà;

b) Đối với trường hợp cho hộ gia đình thuê: Chủ nhà trực tiếp giao kết hợp đồng mua bán điện hoặc ủy quyền cho hộ gia đình thuê nhà giao kết hợp đồng mua bán điện (có cam kết thanh toán tiền điện), mỗi hộ gia đình thuê nhà được tính một định mức;

c) Trường hợp cho sinh viên và người lao động thuê nhà (bên thuê nhà không phải là một hộ gia đình):

- Đối với trường hợp bên thuê nhà có hợp đồng thuê nhà từ 12 tháng trở lên và có đăng ký tạm trú, thường trú (xác định theo thông tin về cư trú tại địa điểm sử dụng điện) thì chủ nhà trực tiếp giao kết hợp đồng mua bán điện hoặc đại diện bên thuê nhà giao kết hợp đồng mua bán điện (có cam kết thanh toán tiền điện của chủ nhà);

- Trường hợp thời hạn cho thuê nhà dưới 12 tháng và chủ nhà không thực hiện kê khai được đầy đủ số người sử dụng điện thì áp dụng giá bán lẻ điện sinh hoạt của bậc 2: Từ 101 - 200 kWh cho toàn bộ sản lượng điện đo đếm được tại công tơ;

- Trường hợp chủ nhà kê khai được đầy đủ số người sử dụng điện thì bên bán điện có trách nhiệm cấp định mức cho chủ nhà căn cứ vào thông tin về cư trú tại địa điểm sử dụng điện; cứ 04 (bốn) người được tính là một hộ sử dụng điện để tính số định mức áp dụng giá bán lẻ điện sinh hoạt, cụ thể: 01 (một) người được tính là 1/4 định mức, 02 (hai) người được tính là 1/2 định mức, 03 (ba) người được tính là 3/4 định mức, 04 (bốn) người được tính là 01 định mức. Khi có thay đổi về số người thuê nhà, chủ nhà cho thuê có trách nhiệm thông báo cho bên bán điện để điều chỉnh định mức tính toán tiền điện;

- Trường hợp người thuê nhà không giao kết hợp đồng trực tiếp với bên bán điện thì tổng tiền điện chủ nhà cho thuê thu của người thuê nhà không được vượt quá tiền điện trong hoá đơn tiền điện hằng tháng do đơn vị bán lẻ điện phát hành;

- Bên bán điện được phép yêu cầu bên mua điện cung cấp thông tin về cư trú tại địa điểm sử dụng điện để làm căn cứ xác định số người tính số định mức khi tính toán hóa đơn tiền điện.
```

**[2] [Thông tư 60/2025/TT-BCT — bản Word trích tuyển cung cấp](https://vanban.chinhphu.vn/?docid=216125&orggroupid=4&pageid=27160)**

Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_corpus_v7_20261005/electricity60-word.json

```text
Điều 21. Hiệu lực thi hành | Khoản 1
1. Thông tư này có hiệu lực thi hành từ ngày 02 tháng 12 năm 2025, trừ quy định tại khoản 3 Điều 4, khoản 1 và khoản 2 Điều 5, Điều 9, Điều 10, khoản 10 Điều 11, khoản 3 Điều 12, khoản 4 Điều 12, điểm c khoản 5 Điều 12, khoản 6 Điều 14, khoản 6 Điều 15 Thông tư này và Phụ lục ban hành kèm theo Thông tư này có hiệu lực thi hành kể từ ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành.

Điều 20. Điều khoản chuyển tiếp | Khoản 1
1. Các quy định tại Thông tư số 16/2014/TT-BCT ngày 29 tháng 5 năm 2014 của Bộ trưởng Bộ Công Thương quy định về giá bán điện được tiếp tục áp dụng từ ngày Thông tư này có hiệu lực đến ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành, bao gồm:

a) Khoản 1 Điều 5;

b) Khoản 10 Điều 8;

c) Khoản 3 Điều 10 (đã được sửa đổi theo quy định tại khoản 3 Điều 1 của Thông tư số 09/2023/TT-BCT sửa đổi, bổ sung một số điều của Thông tư số 16/2014/TT-BCT và Thông tư số 25/2018/TT-BCT ngày 12 tháng 9 năm 2018 của Bộ trưởng Bộ Công Thương sửa đổi, bổ sung một số điều của Thông tư số 16/2014/TT-BCT);

d) Điểm c khoản 4 Điều 10 (đã được sửa đổi theo quy định tại khoản 5 Điều 1 của Thông tư số 25/2018/TT-BCT và khoản 2 Điều 2 của Thông tư số 09/2023/TT-BCT);

đ) Khoản 6 Điều 12 (đã được sửa đổi theo quy định tại khoản 7 Điều 1 của Thông tư số 09/2023/TT-BCT);

e) Khoản 6 Điều 13 (đã được sửa đổi theo quy định tại khoản 9 Điều 1 của Thông tư số 09/2023/TT-BCT).
```

### Lỗi và giới hạn đã ghi nhận

```json
{
  "collect": null,
  "ragas": {},
  "unavailable": null,
  "degraded": [
    "Phản hồi chưa đáp ứng đầy đủ yêu cầu chính; đánh dấu theo nội dung thay vì provider."
  ]
}
```


## Câu 24 · Điện

Ba sinh viên ở chung một phòng được tính tiền điện ra sao?

Trạng thái: Trả lời một phần. Provider: gemini-agent; model: gemini-3.8-flash-high.

faithfulness: 0.7273 | answer_relevancy: 0.9034 | context_utilization: 1.0 | context_recall: 0.5 | context_precision: 1.0

ID nguồn chuẩn: electricity61-word.json, electricity60-word.json

ID nguồn đã truy xuất: electricity60-word.json

Trường hợp chủ nhà kê khai đầy đủ thông tin cư trú của 03 người, bên bán điện cấp 3/4 định mức để áp dụng giá bán lẻ điện sinh hoạt [1].

- Nếu thuê từ 12 tháng trở lên và có đăng ký cư trú tại nơi sử dụng điện, chủ nhà hoặc đại diện bên thuê giao kết hợp đồng mua bán điện [1].
- Nếu thuê dưới 12 tháng và chủ nhà không kê khai đầy đủ số người, áp dụng giá bán lẻ điện sinh hoạt bậc 2 cho toàn bộ sản lượng đo được tại công tơ [1].
- Trường hợp không giao kết hợp đồng trực tiếp với bên bán điện, tổng tiền điện chủ nhà thu không được vượt quá số tiền trên hoá đơn do đơn vị bán lẻ điện phát hành [1].

Quy định tính định mức cho sinh viên thuê nhà nêu trên có hiệu lực kể từ ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực [1] [2].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng.
Nguồn có hiệu lực có điều kiện; chưa xác nhận văn bản/sự kiện kích hoạt.
Nguồn là bản Word/trích tuyển được cung cấp, chưa xác minh toàn bộ câu chữ với bản chính thức; không coi ghi chú biên tập là quy định pháp luật.

### Nguồn và ngữ cảnh

**[1] [Thông tư 60/2025/TT-BCT — bản Word trích tuyển cung cấp](https://vanban.chinhphu.vn/?docid=216125&orggroupid=4&pageid=27160)**

Điều 12. Giá bán lẻ điện sinh hoạt | Khoản 5 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_corpus_v7_20261005/electricity60-word.json

```text
5. Bên mua điện sử dụng vào mục đích sinh hoạt của người thuê nhà để ở áp dụng như sau:

a) Tại mỗi địa chỉ nhà cho thuê, bên bán điện chỉ giao kết một hợp đồng mua bán điện duy nhất. Chủ nhà cho thuê có trách nhiệm cung cấp thông tin về cư trú tại địa điểm sử dụng điện của người thuê nhà;

b) Đối với trường hợp cho hộ gia đình thuê: Chủ nhà trực tiếp giao kết hợp đồng mua bán điện hoặc ủy quyền cho hộ gia đình thuê nhà giao kết hợp đồng mua bán điện (có cam kết thanh toán tiền điện), mỗi hộ gia đình thuê nhà được tính một định mức;

c) Trường hợp cho sinh viên và người lao động thuê nhà (bên thuê nhà không phải là một hộ gia đình):

- Đối với trường hợp bên thuê nhà có hợp đồng thuê nhà từ 12 tháng trở lên và có đăng ký tạm trú, thường trú (xác định theo thông tin về cư trú tại địa điểm sử dụng điện) thì chủ nhà trực tiếp giao kết hợp đồng mua bán điện hoặc đại diện bên thuê nhà giao kết hợp đồng mua bán điện (có cam kết thanh toán tiền điện của chủ nhà);

- Trường hợp thời hạn cho thuê nhà dưới 12 tháng và chủ nhà không thực hiện kê khai được đầy đủ số người sử dụng điện thì áp dụng giá bán lẻ điện sinh hoạt của bậc 2: Từ 101 - 200 kWh cho toàn bộ sản lượng điện đo đếm được tại công tơ;

- Trường hợp chủ nhà kê khai được đầy đủ số người sử dụng điện thì bên bán điện có trách nhiệm cấp định mức cho chủ nhà căn cứ vào thông tin về cư trú tại địa điểm sử dụng điện; cứ 04 (bốn) người được tính là một hộ sử dụng điện để tính số định mức áp dụng giá bán lẻ điện sinh hoạt, cụ thể: 01 (một) người được tính là 1/4 định mức, 02 (hai) người được tính là 1/2 định mức, 03 (ba) người được tính là 3/4 định mức, 04 (bốn) người được tính là 01 định mức. Khi có thay đổi về số người thuê nhà, chủ nhà cho thuê có trách nhiệm thông báo cho bên bán điện để điều chỉnh định mức tính toán tiền điện;

- Trường hợp người thuê nhà không giao kết hợp đồng trực tiếp với bên bán điện thì tổng tiền điện chủ nhà cho thuê thu của người thuê nhà không được vượt quá tiền điện trong hoá đơn tiền điện hằng tháng do đơn vị bán lẻ điện phát hành;

- Bên bán điện được phép yêu cầu bên mua điện cung cấp thông tin về cư trú tại địa điểm sử dụng điện để làm căn cứ xác định số người tính số định mức khi tính toán hóa đơn tiền điện.
```

**[2] [Thông tư 60/2025/TT-BCT — bản Word trích tuyển cung cấp](https://vanban.chinhphu.vn/?docid=216125&orggroupid=4&pageid=27160)**

Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_corpus_v7_20261005/electricity60-word.json

```text
Điều 21. Hiệu lực thi hành | Khoản 1
1. Thông tư này có hiệu lực thi hành từ ngày 02 tháng 12 năm 2025, trừ quy định tại khoản 3 Điều 4, khoản 1 và khoản 2 Điều 5, Điều 9, Điều 10, khoản 10 Điều 11, khoản 3 Điều 12, khoản 4 Điều 12, điểm c khoản 5 Điều 12, khoản 6 Điều 14, khoản 6 Điều 15 Thông tư này và Phụ lục ban hành kèm theo Thông tư này có hiệu lực thi hành kể từ ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành.

Điều 20. Điều khoản chuyển tiếp | Khoản 1
1. Các quy định tại Thông tư số 16/2014/TT-BCT ngày 29 tháng 5 năm 2014 của Bộ trưởng Bộ Công Thương quy định về giá bán điện được tiếp tục áp dụng từ ngày Thông tư này có hiệu lực đến ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành, bao gồm:

a) Khoản 1 Điều 5;

b) Khoản 10 Điều 8;

c) Khoản 3 Điều 10 (đã được sửa đổi theo quy định tại khoản 3 Điều 1 của Thông tư số 09/2023/TT-BCT sửa đổi, bổ sung một số điều của Thông tư số 16/2014/TT-BCT và Thông tư số 25/2018/TT-BCT ngày 12 tháng 9 năm 2018 của Bộ trưởng Bộ Công Thương sửa đổi, bổ sung một số điều của Thông tư số 16/2014/TT-BCT);

d) Điểm c khoản 4 Điều 10 (đã được sửa đổi theo quy định tại khoản 5 Điều 1 của Thông tư số 25/2018/TT-BCT và khoản 2 Điều 2 của Thông tư số 09/2023/TT-BCT);

đ) Khoản 6 Điều 12 (đã được sửa đổi theo quy định tại khoản 7 Điều 1 của Thông tư số 09/2023/TT-BCT);

e) Khoản 6 Điều 13 (đã được sửa đổi theo quy định tại khoản 9 Điều 1 của Thông tư số 09/2023/TT-BCT).
```

### Lỗi và giới hạn đã ghi nhận

```json
{
  "collect": null,
  "ragas": {},
  "unavailable": null,
  "degraded": [
    "Phản hồi chưa đáp ứng đầy đủ yêu cầu chính; đánh dấu theo nội dung thay vì provider."
  ]
}
```


## Câu 25 · Điện

Nếu tôi nghi tiền điện bị thu cao hơn quy định, nên kiểm tra hóa đơn và căn cứ nào?

Trạng thái: Trả lời một phần. Provider: gemini-agent; model: gemini-3.8-flash-high.

faithfulness: 0.7143 | answer_relevancy: 0.8756 | context_utilization: 1.0 | context_recall: 0.3333 | context_precision: 1.0

ID nguồn chuẩn: electricity61-word.json, electricity60-word.json, evn-cantho-transparency-word.json

ID nguồn đã truy xuất: electricity60-word.json

Trường hợp người thuê không ký hợp đồng trực tiếp với bên bán điện, tổng tiền điện chủ nhà thu không được vượt quá số tiền trên hoá đơn do đơn vị bán lẻ điện phát hành [1].

- Khi thời hạn thuê dưới 12 tháng và chủ nhà không kê khai đủ số người, căn cứ tính là giá bán lẻ điện sinh hoạt bậc 2 từ 101 - 200 kWh cho toàn bộ sản lượng đo được tại công tơ [1].
- Khi kê khai đủ số người, căn cứ tính là định mức do bên bán điện cấp dựa trên thông tin cư trú với tỷ lệ 4 người tính thành một hộ sử dụng điện [1].
- Khuyến nghị đối chiếu số tiền chủ trọ thông báo thu với hoá đơn tiền điện hằng tháng do đơn vị bán lẻ điện phát hành tại địa điểm thuê [1].

Quy định về giá bán lẻ điện cho sinh viên thuê nhà tại điểm c khoản 5 Điều 12 chỉ có hiệu lực từ ngày thực hiện điều chỉnh giá bán lẻ điện bình quân gần nhất sau ngày Quyết định 14/2025/QĐ-TTg có hiệu lực [1] [2].
Nguồn là bản trích tuyển cung cấp và chưa đủ căn cứ về biểu giá chi tiết hay mẫu hoá đơn thực tế [1].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng.
Nguồn có hiệu lực có điều kiện; chưa xác nhận văn bản/sự kiện kích hoạt.
Nguồn là bản Word/trích tuyển được cung cấp, chưa xác minh toàn bộ câu chữ với bản chính thức; không coi ghi chú biên tập là quy định pháp luật.

### Nguồn và ngữ cảnh

**[1] [Thông tư 60/2025/TT-BCT — bản Word trích tuyển cung cấp](https://vanban.chinhphu.vn/?docid=216125&orggroupid=4&pageid=27160)**

Điều 12. Giá bán lẻ điện sinh hoạt | Khoản 5 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_corpus_v7_20261005/electricity60-word.json

```text
5. Bên mua điện sử dụng vào mục đích sinh hoạt của người thuê nhà để ở áp dụng như sau:

a) Tại mỗi địa chỉ nhà cho thuê, bên bán điện chỉ giao kết một hợp đồng mua bán điện duy nhất. Chủ nhà cho thuê có trách nhiệm cung cấp thông tin về cư trú tại địa điểm sử dụng điện của người thuê nhà;

b) Đối với trường hợp cho hộ gia đình thuê: Chủ nhà trực tiếp giao kết hợp đồng mua bán điện hoặc ủy quyền cho hộ gia đình thuê nhà giao kết hợp đồng mua bán điện (có cam kết thanh toán tiền điện), mỗi hộ gia đình thuê nhà được tính một định mức;

c) Trường hợp cho sinh viên và người lao động thuê nhà (bên thuê nhà không phải là một hộ gia đình):

- Đối với trường hợp bên thuê nhà có hợp đồng thuê nhà từ 12 tháng trở lên và có đăng ký tạm trú, thường trú (xác định theo thông tin về cư trú tại địa điểm sử dụng điện) thì chủ nhà trực tiếp giao kết hợp đồng mua bán điện hoặc đại diện bên thuê nhà giao kết hợp đồng mua bán điện (có cam kết thanh toán tiền điện của chủ nhà);

- Trường hợp thời hạn cho thuê nhà dưới 12 tháng và chủ nhà không thực hiện kê khai được đầy đủ số người sử dụng điện thì áp dụng giá bán lẻ điện sinh hoạt của bậc 2: Từ 101 - 200 kWh cho toàn bộ sản lượng điện đo đếm được tại công tơ;

- Trường hợp chủ nhà kê khai được đầy đủ số người sử dụng điện thì bên bán điện có trách nhiệm cấp định mức cho chủ nhà căn cứ vào thông tin về cư trú tại địa điểm sử dụng điện; cứ 04 (bốn) người được tính là một hộ sử dụng điện để tính số định mức áp dụng giá bán lẻ điện sinh hoạt, cụ thể: 01 (một) người được tính là 1/4 định mức, 02 (hai) người được tính là 1/2 định mức, 03 (ba) người được tính là 3/4 định mức, 04 (bốn) người được tính là 01 định mức. Khi có thay đổi về số người thuê nhà, chủ nhà cho thuê có trách nhiệm thông báo cho bên bán điện để điều chỉnh định mức tính toán tiền điện;

- Trường hợp người thuê nhà không giao kết hợp đồng trực tiếp với bên bán điện thì tổng tiền điện chủ nhà cho thuê thu của người thuê nhà không được vượt quá tiền điện trong hoá đơn tiền điện hằng tháng do đơn vị bán lẻ điện phát hành;

- Bên bán điện được phép yêu cầu bên mua điện cung cấp thông tin về cư trú tại địa điểm sử dụng điện để làm căn cứ xác định số người tính số định mức khi tính toán hóa đơn tiền điện.
```

**[2] [Thông tư 60/2025/TT-BCT — bản Word trích tuyển cung cấp](https://vanban.chinhphu.vn/?docid=216125&orggroupid=4&pageid=27160)**

Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_corpus_v7_20261005/electricity60-word.json

```text
Điều 21. Hiệu lực thi hành | Khoản 1
1. Thông tư này có hiệu lực thi hành từ ngày 02 tháng 12 năm 2025, trừ quy định tại khoản 3 Điều 4, khoản 1 và khoản 2 Điều 5, Điều 9, Điều 10, khoản 10 Điều 11, khoản 3 Điều 12, khoản 4 Điều 12, điểm c khoản 5 Điều 12, khoản 6 Điều 14, khoản 6 Điều 15 Thông tư này và Phụ lục ban hành kèm theo Thông tư này có hiệu lực thi hành kể từ ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành.

Điều 20. Điều khoản chuyển tiếp | Khoản 1
1. Các quy định tại Thông tư số 16/2014/TT-BCT ngày 29 tháng 5 năm 2014 của Bộ trưởng Bộ Công Thương quy định về giá bán điện được tiếp tục áp dụng từ ngày Thông tư này có hiệu lực đến ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành, bao gồm:

a) Khoản 1 Điều 5;

b) Khoản 10 Điều 8;

c) Khoản 3 Điều 10 (đã được sửa đổi theo quy định tại khoản 3 Điều 1 của Thông tư số 09/2023/TT-BCT sửa đổi, bổ sung một số điều của Thông tư số 16/2014/TT-BCT và Thông tư số 25/2018/TT-BCT ngày 12 tháng 9 năm 2018 của Bộ trưởng Bộ Công Thương sửa đổi, bổ sung một số điều của Thông tư số 16/2014/TT-BCT);

d) Điểm c khoản 4 Điều 10 (đã được sửa đổi theo quy định tại khoản 5 Điều 1 của Thông tư số 25/2018/TT-BCT và khoản 2 Điều 2 của Thông tư số 09/2023/TT-BCT);

đ) Khoản 6 Điều 12 (đã được sửa đổi theo quy định tại khoản 7 Điều 1 của Thông tư số 09/2023/TT-BCT);

e) Khoản 6 Điều 13 (đã được sửa đổi theo quy định tại khoản 9 Điều 1 của Thông tư số 09/2023/TT-BCT).
```

### Lỗi và giới hạn đã ghi nhận

```json
{
  "collect": null,
  "ragas": {},
  "unavailable": null,
  "degraded": [
    "Phản hồi chưa đáp ứng đầy đủ yêu cầu chính; đánh dấu theo nội dung thay vì provider."
  ]
}
```


## Câu 26 · Điện

Chủ trọ có phải thông báo cách tính tiền điện và số điện đã sử dụng không?

Trạng thái: Trả lời một phần. Provider: gemini-agent; model: gemini-3.8-flash-high.

faithfulness: 1.0 | answer_relevancy: 0.0 | context_utilization: 0.9167 | context_recall: 1.0 | context_precision: 0.6667

ID nguồn chuẩn: electricity61-word.json, evn-cantho-transparency-word.json

ID nguồn đã truy xuất: electricity60-word.json, evn-cantho-transparency-word.json, electricity61-word.json

Chưa đủ căn cứ xác định nghĩa vụ pháp lý bắt buộc chủ trọ phải thông báo riêng số điện đã dùng, nhưng nguồn ghi nhận yêu cầu công khai cách tính và thu tiền điện theo hóa đơn do Điện lực phát hành [1] [2].

- Nguồn hướng dẫn yêu cầu công khai cách tính và thu tiền điện theo đúng hóa đơn do Điện lực phát hành [2].
- Trường hợp người thuê không ký hợp đồng trực tiếp với bên bán điện, tổng tiền điện chủ nhà cho thuê thu không được vượt quá tiền điện trong hóa đơn tiền điện hằng tháng do đơn vị bán lẻ điện phát hành [1].
- Vị trí lắp đặt công tơ đo đếm điện phải bảo đảm an toàn, mỹ quan, thuận lợi cho bên mua điện kiểm tra chỉ số đo điện năng và bên bán điện ghi chỉ số đo điện năng [4].

Điểm c khoản 5 Điều 12 Thông tư 60/2025/TT-BCT có hiệu lực thi hành kể từ ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành [1] [5].
Nguồn cung cấp chưa có quy định trực tiếp về việc chủ trọ phải gửi bảng kê hay thông báo riêng số điện sử dụng cho từng phòng [1] [2].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng.
Nguồn có hiệu lực có điều kiện; chưa xác nhận văn bản/sự kiện kích hoạt.
Nguồn là bản Word/trích tuyển được cung cấp, chưa xác minh toàn bộ câu chữ với bản chính thức; không coi ghi chú biên tập là quy định pháp luật.
Hướng dẫn kiểm tra nhà trọ Cần Thơ đăng ngày 21/09/2026; không phải điều luật hoặc quy định một mẫu bảng kê bắt buộc. Trích đoạn ngắn về công khai cách tính và hóa đơn; không tự suy ra mọi chi tiết kê khai.

### Nguồn và ngữ cảnh

**[1] [Thông tư 60/2025/TT-BCT — bản Word trích tuyển cung cấp](https://vanban.chinhphu.vn/?docid=216125&orggroupid=4&pageid=27160)**

Điều 12. Giá bán lẻ điện sinh hoạt | Khoản 5 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_corpus_v7_20261005/electricity60-word.json

```text
5. Bên mua điện sử dụng vào mục đích sinh hoạt của người thuê nhà để ở áp dụng như sau:

a) Tại mỗi địa chỉ nhà cho thuê, bên bán điện chỉ giao kết một hợp đồng mua bán điện duy nhất. Chủ nhà cho thuê có trách nhiệm cung cấp thông tin về cư trú tại địa điểm sử dụng điện của người thuê nhà;

b) Đối với trường hợp cho hộ gia đình thuê: Chủ nhà trực tiếp giao kết hợp đồng mua bán điện hoặc ủy quyền cho hộ gia đình thuê nhà giao kết hợp đồng mua bán điện (có cam kết thanh toán tiền điện), mỗi hộ gia đình thuê nhà được tính một định mức;

c) Trường hợp cho sinh viên và người lao động thuê nhà (bên thuê nhà không phải là một hộ gia đình):

- Đối với trường hợp bên thuê nhà có hợp đồng thuê nhà từ 12 tháng trở lên và có đăng ký tạm trú, thường trú (xác định theo thông tin về cư trú tại địa điểm sử dụng điện) thì chủ nhà trực tiếp giao kết hợp đồng mua bán điện hoặc đại diện bên thuê nhà giao kết hợp đồng mua bán điện (có cam kết thanh toán tiền điện của chủ nhà);

- Trường hợp thời hạn cho thuê nhà dưới 12 tháng và chủ nhà không thực hiện kê khai được đầy đủ số người sử dụng điện thì áp dụng giá bán lẻ điện sinh hoạt của bậc 2: Từ 101 - 200 kWh cho toàn bộ sản lượng điện đo đếm được tại công tơ;

- Trường hợp chủ nhà kê khai được đầy đủ số người sử dụng điện thì bên bán điện có trách nhiệm cấp định mức cho chủ nhà căn cứ vào thông tin về cư trú tại địa điểm sử dụng điện; cứ 04 (bốn) người được tính là một hộ sử dụng điện để tính số định mức áp dụng giá bán lẻ điện sinh hoạt, cụ thể: 01 (một) người được tính là 1/4 định mức, 02 (hai) người được tính là 1/2 định mức, 03 (ba) người được tính là 3/4 định mức, 04 (bốn) người được tính là 01 định mức. Khi có thay đổi về số người thuê nhà, chủ nhà cho thuê có trách nhiệm thông báo cho bên bán điện để điều chỉnh định mức tính toán tiền điện;

- Trường hợp người thuê nhà không giao kết hợp đồng trực tiếp với bên bán điện thì tổng tiền điện chủ nhà cho thuê thu của người thuê nhà không được vượt quá tiền điện trong hoá đơn tiền điện hằng tháng do đơn vị bán lẻ điện phát hành;

- Bên bán điện được phép yêu cầu bên mua điện cung cấp thông tin về cư trú tại địa điểm sử dụng điện để làm căn cứ xác định số người tính số định mức khi tính toán hóa đơn tiền điện.
```

**[2] [Công khai cách tính tiền điện nhà trọ — PC TP Cần Thơ / EVNSPC](https://cskh.evnspc.vn/TinTuc/TinTucChiTiet?LoaiTinBai=ALL&MaTinBai=3103)**

Công khai cách tính tiền điện nhà trọ — PC TP Cần Thơ / EVNSPC · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_priority7_corpus_v13_20261006/evn-cantho-transparency-word.json

```text
công khai cách tính và thu tiền điện theo đúng hóa đơn do Điện lực phát hành
```

**[3] [Luật Điện lực 61/2024/QH15 — bản Word cung cấp](https://vanban.chinhphu.vn/?docid=212489&pageid=27160)**

Điều 56. Đo đếm điện | Khoản 1 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_corpus_v7_20261005/electricity61-word.json

```text
1. Bên bán điện, đơn vị phát điện, truyền tải điện, phân phối điện có trách nhiệm đầu tư, lắp đặt và quản lý toàn bộ các thiết bị đo đếm điện, thiết bị phụ trợ cho việc đo đếm điện, hệ thống thu thập và quản lý số liệu đo đếm điện, trừ trường hợp các bên có thỏa thuận khác bảo đảm quyền lợi giữa các bên nhưng không trái với quy định của pháp luật.
```

**[4] [Luật Điện lực 61/2024/QH15 — bản Word cung cấp](https://vanban.chinhphu.vn/?docid=212489&pageid=27160)**

Điều 56. Đo đếm điện | Khoản 3 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_corpus_v7_20261005/electricity61-word.json

```text
3. Vị trí lắp đặt công tơ đo đếm điện phải bảo đảm an toàn, mỹ quan, thuận lợi cho bên mua điện kiểm tra chỉ số đo điện năng và bên bán điện ghi chỉ số đo điện năng.
```

**[5] [Thông tư 60/2025/TT-BCT — bản Word trích tuyển cung cấp](https://vanban.chinhphu.vn/?docid=216125&orggroupid=4&pageid=27160)**

Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_corpus_v7_20261005/electricity60-word.json

```text
Điều 21. Hiệu lực thi hành | Khoản 1
1. Thông tư này có hiệu lực thi hành từ ngày 02 tháng 12 năm 2025, trừ quy định tại khoản 3 Điều 4, khoản 1 và khoản 2 Điều 5, Điều 9, Điều 10, khoản 10 Điều 11, khoản 3 Điều 12, khoản 4 Điều 12, điểm c khoản 5 Điều 12, khoản 6 Điều 14, khoản 6 Điều 15 Thông tư này và Phụ lục ban hành kèm theo Thông tư này có hiệu lực thi hành kể từ ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành.

Điều 20. Điều khoản chuyển tiếp | Khoản 1
1. Các quy định tại Thông tư số 16/2014/TT-BCT ngày 29 tháng 5 năm 2014 của Bộ trưởng Bộ Công Thương quy định về giá bán điện được tiếp tục áp dụng từ ngày Thông tư này có hiệu lực đến ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành, bao gồm:

a) Khoản 1 Điều 5;

b) Khoản 10 Điều 8;

c) Khoản 3 Điều 10 (đã được sửa đổi theo quy định tại khoản 3 Điều 1 của Thông tư số 09/2023/TT-BCT sửa đổi, bổ sung một số điều của Thông tư số 16/2014/TT-BCT và Thông tư số 25/2018/TT-BCT ngày 12 tháng 9 năm 2018 của Bộ trưởng Bộ Công Thương sửa đổi, bổ sung một số điều của Thông tư số 16/2014/TT-BCT);

d) Điểm c khoản 4 Điều 10 (đã được sửa đổi theo quy định tại khoản 5 Điều 1 của Thông tư số 25/2018/TT-BCT và khoản 2 Điều 2 của Thông tư số 09/2023/TT-BCT);

đ) Khoản 6 Điều 12 (đã được sửa đổi theo quy định tại khoản 7 Điều 1 của Thông tư số 09/2023/TT-BCT);

e) Khoản 6 Điều 13 (đã được sửa đổi theo quy định tại khoản 9 Điều 1 của Thông tư số 09/2023/TT-BCT).
```

### Lỗi và giới hạn đã ghi nhận

```json
{
  "collect": null,
  "ragas": {},
  "unavailable": null,
  "degraded": [
    "Phản hồi chưa đáp ứng đầy đủ yêu cầu chính; đánh dấu theo nội dung thay vì provider."
  ]
}
```


## Câu 27 · Nước

Giá nước sinh hoạt áp dụng cho phòng trọ ở Cần Thơ được xác định theo căn cứ nào?

Trạng thái: Trả lời một phần. Provider: legal-partial-retained; model: gemini-3.8-flash-high.

faithfulness: 1.0 | answer_relevancy: 0.0 | context_utilization: 1.0 | context_recall: 1.0 | context_precision: 1.0

ID nguồn chuẩn: water215-word.json

ID nguồn đã truy xuất: water215-word.json

Chưa đủ căn cứ từ nguồn để xác định cách tính giá riêng cho phòng trọ, nguồn chỉ quy định giá nước sạch sinh hoạt tại Cần Thơ theo đơn vị cấp nước, khu vực đô thị hay nông thôn và nhóm khách hàng sử dụng [1] [2].
Nguồn quy định giá nước sinh hoạt phân chia theo đơn vị cấp nước, gồm các đơn vị cấp nước nói chung hoặc Trung tâm Nước sạch và Vệ sinh môi trường nông thôn [1] [2].
Mức giá sinh hoạt do các đơn vị cấp nước cung cấp được xác định theo khu vực đô thị hoặc khu vực nông thôn và phân loại theo nhóm khách hàng như hộ dân cư, hộ nghèo có sổ hoặc các nhóm khác [2].
Nước do Trung tâm Nước sạch và Vệ sinh môi trường nông thôn cung cấp phân loại theo nhóm hộ nghèo có sổ, hộ gia đình chính sách, hộ hiến đất hoặc hộ dân cư và nhóm đối tượng khác [1].
Nguồn cung cấp không có quy định riêng về cách tính định mức, giá khoán hay phân chia tiền nước giữa người thuê trọ và chủ trọ [1] [2].

### Nguồn và ngữ cảnh

**[1] [Giá nước Cần Thơ 215/QĐ-UBND — bản Word cung cấp](https://capnuoccantho2.com.vn/View.aspx?wc=63&wp=332)**

Điều 1. Quy định giá nước sạch sinh hoạt tại đô thị và khu vực nông thôn áp dụng đối với các đơn vị kinh doanh nước sạch, các tổ chức và khách hàng sử dụng nước sạch trên địa bàn thành phố Cần Thơ như sau: | Khoản 2 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_corpus_v7_20261005/water215-word.json

```text
2. Giá nước sạch sinh hoạt tại đô thị, khu vực nông thôn do Trung tâm Nước sạch và Vệ sinh môi trường nông thôn cung cấp cho mục đích sinh hoạt:

STT

Nhóm khách hàng sử dụng nước sạch cho mục đích sinh hoạt

Giá tiêu thụ nước sạch (đồng/m3)

Nhóm 1

Hộ dân cư là hộ nghèo có sổ, hộ gia đình chính sách (gia đình Mẹ Việt Nam anh hùng, gia đình thương binh, gia đình liệt sĩ), hộ hiến đất.

4.000

Nhóm 2

Hộ dân cư và các nhóm đối tượng khác

7.450

(Giá đã bao gồm thuế giá trị gia tăng, chưa bao gồm phí bảo vệ môi trường đối với nước thải sinh hoạt)
```

**[2] [Giá nước Cần Thơ 215/QĐ-UBND — bản Word cung cấp](https://capnuoccantho2.com.vn/View.aspx?wc=63&wp=332)**

Điều 1. Quy định giá nước sạch sinh hoạt tại đô thị và khu vực nông thôn áp dụng đối với các đơn vị kinh doanh nước sạch, các tổ chức và khách hàng sử dụng nước sạch trên địa bàn thành phố Cần Thơ như sau: | Khoản 1 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_corpus_v7_20261005/water215-word.json

```text
1. Giá nước sạch sinh hoạt tại đô thị, khu vực nông thôn năm 2024 do các đơn vị cấp nước cung cấp:

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

(Giá đã bao gồm thuế giá trị gia tăng, chưa bao gồm phí bảo vệ môi trường đối với nước thải sinh hoạt)
```

**[3] [Giá nước Cần Thơ 215/QĐ-UBND — bản Word cung cấp](https://capnuoccantho2.com.vn/View.aspx?wc=63&wp=332)**

Điều 2. Điều chỉnh giá nước sạch | Khoản 2 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_corpus_v7_20261005/water215-word.json

```text
2. Hàng năm, các đơn vị cấp nước chủ động rà soát việc thực hiện phương án giá nước sạch và giá nước sạch dự kiến cho năm tiếp theo trên cơ sở quy định tại Điều 4 Thông tư số 44/2021/TT-BTC ngày 18 tháng 6 năm 2021 của Bộ trưởng Bộ Tài chính quy định về khung giá, nguyên tắc, phương pháp xác định giá nước sạch sinh hoạt để thực hiện, đảm bảo tuân thủ đúng quy định.
```

### Lỗi và giới hạn đã ghi nhận

```json
{
  "collect": null,
  "ragas": {},
  "unavailable": null,
  "degraded": [
    "{\"claim_id\": \"steps:3\", \"source_ids\": [3], \"reason\": \"Số điều được khẳng định không khớp điều khoản của nguồn trích dẫn.\", \"code\": \"deterministic_source_guard\"}",
    "Giữ các kết luận đã kiểm chứng; đánh dấu phần chưa có căn cứ.",
    "Phản hồi chưa đáp ứng đầy đủ yêu cầu chính; đánh dấu theo nội dung thay vì provider."
  ]
}
```


## Câu 28 · Nước

Tôi nên kiểm tra gì khi chủ trọ thu tiền nước theo đầu người thay vì đồng hồ?

Trạng thái: Trả lời một phần. Provider: gemini-agent; model: gemini-3.8-flash-high.

faithfulness: 0.75 | answer_relevancy: 0.0 | context_utilization: 0.6792 | context_recall: 0.6667 | context_precision: 0.6667

ID nguồn chuẩn: water215-word.json, civil91-word.json, supplement-s05-word.json

ID nguồn đã truy xuất: water215-word.json, supplement-s01-word.json, civil91-word.json

Nguồn quy định hợp đồng có thể thỏa thuận về giá, phương thức thanh toán và các điều kiện có hiệu lực của giao dịch dân sự [3] [5].

- Khuyến nghị chủ động hỏi kỹ về giá điện nước và các chi phí khác nếu có trước khi đặt cọc [2].
- Khuyến nghị đọc kỹ các điều khoản trên hợp đồng thuê về tiền nước, số người thuê và các chi phí phát sinh khác [2].
- Khuyến nghị kiểm tra tình trạng hệ thống đường nước trước khi đến ở và yêu cầu sửa chữa nếu hỏng hóc [2].
- Nguồn quy định nội dung hợp đồng có thể bao gồm giá, phương thức thanh toán, quyền và nghĩa vụ của các bên [3].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng [2] [3].
Biểu giá nước sinh hoạt Cần Thơ năm 2024 không quy định cụ thể cách chia tiền nước khoán theo đầu người giữa các bên thuê trọ [4].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng.
Nguồn giá nước năm 2024: cần xác nhận địa bàn, đơn vị cấp nước và hiệu lực tại thời điểm áp dụng; bảng tiền chưa được dùng để kết luận mức thu.
Hướng dẫn/khuyến cáo của Trợ Giúp Chợ Tốt; không phải điều luật. Mẹo giao dịch, không phải điều luật. Không chứng minh hạn hoàn cọc cố định hoặc mức cọc bắt buộc; không thay thế xác minh người được ủy quyền cho thuê. Chỉ đọc phần kiểm tra, không bổ sung mẫu soạn hợp đồng.
Nguồn là bản Word/trích tuyển được cung cấp, chưa xác minh toàn bộ câu chữ với bản chính thức; không coi ghi chú biên tập là quy định pháp luật.

### Nguồn và ngữ cảnh

**[1] [Giá nước Cần Thơ 215/QĐ-UBND — bản Word cung cấp](https://capnuoccantho2.com.vn/View.aspx?wc=63&wp=332)**

Điều 2. Điều chỉnh giá nước sạch | Khoản 2 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_corpus_v7_20261005/water215-word.json

```text
2. Hàng năm, các đơn vị cấp nước chủ động rà soát việc thực hiện phương án giá nước sạch và giá nước sạch dự kiến cho năm tiếp theo trên cơ sở quy định tại Điều 4 Thông tư số 44/2021/TT-BTC ngày 18 tháng 6 năm 2021 của Bộ trưởng Bộ Tài chính quy định về khung giá, nguyên tắc, phương pháp xác định giá nước sạch sinh hoạt để thực hiện, đảm bảo tuân thủ đúng quy định.
```

**[2] [Mẹo khi thuê phòng — Trợ Giúp Chợ Tốt](https://trogiup.chotot.com/nguoi-mua/meo-khi-thue-phong/)**

Mẹo khi thuê phòng | Đoạn nguyên văn 78 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_supplement_corpus_v8_20261005/supplement-s01-word.json

```text
1. Kiểm tra độ uy tín của người cho thuê trên môi trường trực tuyến (Google, Facebook, diễn đàn, …)

Tìm kiếm số điện thoại và địa chỉ muốn thuê trên Google, Facebook, các diễn đàn trực tuyến, … và xem các thông tin giao dịch trước đó như đánh giá của khách hàng về địa chỉ thuê này, …

2. Xác định địa điểm phòng muốn thuê và khảo sát mức giá chung

Tìm hiểu cụ thể địa chỉ muốn thuê gồm số nhà, tên đường, phường, quận.

Hỏi thăm trực tiếp hàng xóm xung quanh địa điểm muốn thuê và tham khảo ý kiến từ người thân, bạn bè hoặc tìm hiểu thông tin trên mạng về địa điểm này.

Mỗi khu vực sẽ có giá thuê khác nhau. Do đó, cần tìm hiểu mức giá chung theo từng khu vực trước khi thuê bằng cách so sánh với các tin đăng bất động sản cùng loại trên Chợ Tốt.

Thận trọng khi tìm được phòng ở trung tâm hoặc phòng tốt nhưng giá rẻ bất thường.

3. Không đặt cọc nếu chưa xác định được chủ nhà

Yêu cầu gặp trực tiếp chủ nhà trước khi đặt cọc.

Yêu cầu chủ nhà cho xem giấy tờ nhà và thẻ Căn Cước/thẻ Căn Cước Công Dân để xác nhận quyền sở hữu của chủ nhà

Nên chủ động hỏi kỹ về giá phòng, giá điện nước, các chi phí khác (nếu có) và các điều kiện sinh hoạt khác trước khi đặt cọc.

4. Phải đọc kỹ hợp đồng đặt cọc và hợp đồng thuê

Khi làm hợp đồng thuê cần đọc kỹ các điều khoản ghi trên hợp đồng: địa chỉ phòng, số phòng, tiền phòng cố định trong bao lâu không thay đổi, số người thuê, tiền điện, tiền nước, tiền gửi xe, sử dụng Internet và các chi phí phát sinh khác (nếu có).

Làm rõ các điều khoản về thời hạn hợp đồng và tiền đặt cọc trong trường hợp kết thúc hợp đồng trước hạn.

Luôn giữ tối thiểu một bản chính biên nhận đặt cọc và hợp đồng thuê.

5. Kiểm tra tình trạng phòng thuê trước khi đến ở

Kiểm tra tình trạng các thiết bị trong nhà và hệ thống đường điện, nước. Nếu có vấn đề hỏng hóc thì phải yêu cầu chủ nhà trọ sửa chữa hoặc thay thế.

Thống nhất số điện/nước (internet nếu có) phải trả ngay khi làm hợp đồng để tránh trường hợp phải trả thêm lượng điện/nước (internet nếu có) đã tiêu thụ trước đó.

Những trường hợp gian lận cần cảnh giác

Yêu cầu khách thuê đặt tiền cọc sau đó lật ngược những thỏa thuận ban đầu, thu thêm hàng loạt phí… là những trường hợp được người đi thuê cảnh báo:
```

**[3] [Bộ luật Dân sự 91/2015/QH13 — Word do cơ quan nhà nước công bố](https://congan.daklak.gov.vn/laws/detail/Bo-luat-Dan-su-163/)**

Điều 398. Nội dung của hợp đồng | Khoản 2 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_repair_corpus_v14_20261006/civil91-word.json

```text
2. Hợp đồng có thể có các nội dung sau đây:

a) Đối tượng của hợp đồng;

b) Số lượng, chất lượng;

c) Giá, phương thức thanh toán;

d) Thời hạn, địa điểm, phương thức thực hiện hợp đồng;

đ) Quyền, nghĩa vụ của các bên;

e) Trách nhiệm do vi phạm hợp đồng;

g) Phương thức giải quyết tranh chấp.
```

**[4] [Giá nước Cần Thơ 215/QĐ-UBND — bản Word cung cấp](https://capnuoccantho2.com.vn/View.aspx?wc=63&wp=332)**

Điều 1. Quy định giá nước sạch sinh hoạt tại đô thị và khu vực nông thôn áp dụng đối với các đơn vị kinh doanh nước sạch, các tổ chức và khách hàng sử dụng nước sạch trên địa bàn thành phố Cần Thơ như sau: | Khoản 1 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_corpus_v7_20261005/water215-word.json

```text
1. Giá nước sạch sinh hoạt tại đô thị, khu vực nông thôn năm 2024 do các đơn vị cấp nước cung cấp:

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

(Giá đã bao gồm thuế giá trị gia tăng, chưa bao gồm phí bảo vệ môi trường đối với nước thải sinh hoạt)
```

**[5] [Bộ luật Dân sự 91/2015/QH13 — Word do cơ quan nhà nước công bố](https://congan.daklak.gov.vn/laws/detail/Bo-luat-Dan-su-163/)**

Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_repair_corpus_v14_20261006/civil91-word.json

```text
Điều 117. Điều kiện có hiệu lực của giao dịch dân sự | Khoản 1
1. Giao dịch dân sự có hiệu lực khi có đủ các điều kiện sau đây:

a) Chủ thể có năng lực pháp luật dân sự, năng lực hành vi dân sự phù hợp
với giao dịch dân sự được xác lập;

b) Chủ thể tham gia giao dịch dân sự hoàn toàn tự nguyện;

c) Mục đích và nội dung của giao dịch dân sự không vi phạm điều cấm của
luật, không trái đạo đức xã hội.

Điều 117. Điều kiện có hiệu lực của giao dịch dân sự | Khoản 2
2. Hình thức của giao dịch dân sự là điều kiện có hiệu lực của giao dịch
dân sự trong trường hợp luật có quy định.
```

### Lỗi và giới hạn đã ghi nhận

```json
{
  "collect": null,
  "ragas": {},
  "unavailable": null,
  "degraded": [
    "Phản hồi chưa đáp ứng đầy đủ yêu cầu chính; đánh dấu theo nội dung thay vì provider."
  ]
}
```


## Câu 29 · Nước

Nếu nhà trọ dùng chung đồng hồ nước, cách phân chia chi phí nên được thỏa thuận ra sao?

Trạng thái: Trả lời một phần. Provider: gemini-agent; model: gemini-3.8-flash-high.

faithfulness: 0.7727 | answer_relevancy: 0.9408 | context_utilization: 0.5833 | context_recall: 1.0 | context_precision: 0.6667

ID nguồn chuẩn: water215-word.json, civil91-word.json

ID nguồn đã truy xuất: water215-word.json, supplement-s01-word.json, civil91-word.json

Các bên có quyền tự thỏa thuận nội dung hợp đồng về tiền nước và ghi rõ vào hợp đồng thuê khi dùng chung đồng hồ [2] [3].

- Khuyến nghị chủ động hỏi kỹ về giá nước và các chi phí khác trước khi đặt cọc phòng trọ [2].
- Khuyến nghị đọc kỹ và làm rõ các điều khoản trong hợp đồng thuê về tiền nước, số người thuê cùng các chi phí phát sinh khác [2].
- Khuyến nghị thống nhất số nước phải trả ngay khi ký hợp đồng để tránh phải trả thêm lượng nước đã tiêu thụ trước đó [2].

Chưa đủ căn cứ từ nguồn để xác định công thức chia tiền nước bắt buộc hoặc mức giá khoán cụ thể khi dùng chung đồng hồ [1] [2].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng.
Nguồn giá nước năm 2024: cần xác nhận địa bàn, đơn vị cấp nước và hiệu lực tại thời điểm áp dụng; bảng tiền chưa được dùng để kết luận mức thu.
Nguồn là bản Word/trích tuyển được cung cấp, chưa xác minh toàn bộ câu chữ với bản chính thức; không coi ghi chú biên tập là quy định pháp luật.
Hướng dẫn/khuyến cáo của Trợ Giúp Chợ Tốt; không phải điều luật. Mẹo giao dịch, không phải điều luật. Không chứng minh hạn hoàn cọc cố định hoặc mức cọc bắt buộc; không thay thế xác minh người được ủy quyền cho thuê. Chỉ đọc phần kiểm tra, không bổ sung mẫu soạn hợp đồng.

### Nguồn và ngữ cảnh

**[1] [Giá nước Cần Thơ 215/QĐ-UBND — bản Word cung cấp](https://capnuoccantho2.com.vn/View.aspx?wc=63&wp=332)**

Điều 1. Quy định giá nước sạch sinh hoạt tại đô thị và khu vực nông thôn áp dụng đối với các đơn vị kinh doanh nước sạch, các tổ chức và khách hàng sử dụng nước sạch trên địa bàn thành phố Cần Thơ như sau: | Khoản 1 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_corpus_v7_20261005/water215-word.json

```text
1. Giá nước sạch sinh hoạt tại đô thị, khu vực nông thôn năm 2024 do các đơn vị cấp nước cung cấp:

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

(Giá đã bao gồm thuế giá trị gia tăng, chưa bao gồm phí bảo vệ môi trường đối với nước thải sinh hoạt)
```

**[2] [Mẹo khi thuê phòng — Trợ Giúp Chợ Tốt](https://trogiup.chotot.com/nguoi-mua/meo-khi-thue-phong/)**

Mẹo khi thuê phòng | Đoạn nguyên văn 78 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_supplement_corpus_v8_20261005/supplement-s01-word.json

```text
1. Kiểm tra độ uy tín của người cho thuê trên môi trường trực tuyến (Google, Facebook, diễn đàn, …)

Tìm kiếm số điện thoại và địa chỉ muốn thuê trên Google, Facebook, các diễn đàn trực tuyến, … và xem các thông tin giao dịch trước đó như đánh giá của khách hàng về địa chỉ thuê này, …

2. Xác định địa điểm phòng muốn thuê và khảo sát mức giá chung

Tìm hiểu cụ thể địa chỉ muốn thuê gồm số nhà, tên đường, phường, quận.

Hỏi thăm trực tiếp hàng xóm xung quanh địa điểm muốn thuê và tham khảo ý kiến từ người thân, bạn bè hoặc tìm hiểu thông tin trên mạng về địa điểm này.

Mỗi khu vực sẽ có giá thuê khác nhau. Do đó, cần tìm hiểu mức giá chung theo từng khu vực trước khi thuê bằng cách so sánh với các tin đăng bất động sản cùng loại trên Chợ Tốt.

Thận trọng khi tìm được phòng ở trung tâm hoặc phòng tốt nhưng giá rẻ bất thường.

3. Không đặt cọc nếu chưa xác định được chủ nhà

Yêu cầu gặp trực tiếp chủ nhà trước khi đặt cọc.

Yêu cầu chủ nhà cho xem giấy tờ nhà và thẻ Căn Cước/thẻ Căn Cước Công Dân để xác nhận quyền sở hữu của chủ nhà

Nên chủ động hỏi kỹ về giá phòng, giá điện nước, các chi phí khác (nếu có) và các điều kiện sinh hoạt khác trước khi đặt cọc.

4. Phải đọc kỹ hợp đồng đặt cọc và hợp đồng thuê

Khi làm hợp đồng thuê cần đọc kỹ các điều khoản ghi trên hợp đồng: địa chỉ phòng, số phòng, tiền phòng cố định trong bao lâu không thay đổi, số người thuê, tiền điện, tiền nước, tiền gửi xe, sử dụng Internet và các chi phí phát sinh khác (nếu có).

Làm rõ các điều khoản về thời hạn hợp đồng và tiền đặt cọc trong trường hợp kết thúc hợp đồng trước hạn.

Luôn giữ tối thiểu một bản chính biên nhận đặt cọc và hợp đồng thuê.

5. Kiểm tra tình trạng phòng thuê trước khi đến ở

Kiểm tra tình trạng các thiết bị trong nhà và hệ thống đường điện, nước. Nếu có vấn đề hỏng hóc thì phải yêu cầu chủ nhà trọ sửa chữa hoặc thay thế.

Thống nhất số điện/nước (internet nếu có) phải trả ngay khi làm hợp đồng để tránh trường hợp phải trả thêm lượng điện/nước (internet nếu có) đã tiêu thụ trước đó.

Những trường hợp gian lận cần cảnh giác

Yêu cầu khách thuê đặt tiền cọc sau đó lật ngược những thỏa thuận ban đầu, thu thêm hàng loạt phí… là những trường hợp được người đi thuê cảnh báo:
```

**[3] [Bộ luật Dân sự 91/2015/QH13 — Word do cơ quan nhà nước công bố](https://congan.daklak.gov.vn/laws/detail/Bo-luat-Dan-su-163/)**

Điều 398. Nội dung của hợp đồng | Khoản 1 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_repair_corpus_v14_20261006/civil91-word.json

```text
1. Các bên trong hợp đồng có quyền thỏa thuận về nội dung trong hợp đồng.
```

**[4] [Giá nước Cần Thơ 215/QĐ-UBND — bản Word cung cấp](https://capnuoccantho2.com.vn/View.aspx?wc=63&wp=332)**

Điều 2. Điều chỉnh giá nước sạch | Khoản 2 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_corpus_v7_20261005/water215-word.json

```text
2. Hàng năm, các đơn vị cấp nước chủ động rà soát việc thực hiện phương án giá nước sạch và giá nước sạch dự kiến cho năm tiếp theo trên cơ sở quy định tại Điều 4 Thông tư số 44/2021/TT-BTC ngày 18 tháng 6 năm 2021 của Bộ trưởng Bộ Tài chính quy định về khung giá, nguyên tắc, phương pháp xác định giá nước sạch sinh hoạt để thực hiện, đảm bảo tuân thủ đúng quy định.
```

**[5] [Bộ luật Dân sự 91/2015/QH13 — Word do cơ quan nhà nước công bố](https://congan.daklak.gov.vn/laws/detail/Bo-luat-Dan-su-163/)**

Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_repair_corpus_v14_20261006/civil91-word.json

```text
Điều 117. Điều kiện có hiệu lực của giao dịch dân sự | Khoản 1
1. Giao dịch dân sự có hiệu lực khi có đủ các điều kiện sau đây:

a) Chủ thể có năng lực pháp luật dân sự, năng lực hành vi dân sự phù hợp
với giao dịch dân sự được xác lập;

b) Chủ thể tham gia giao dịch dân sự hoàn toàn tự nguyện;

c) Mục đích và nội dung của giao dịch dân sự không vi phạm điều cấm của
luật, không trái đạo đức xã hội.

Điều 117. Điều kiện có hiệu lực của giao dịch dân sự | Khoản 2
2. Hình thức của giao dịch dân sự là điều kiện có hiệu lực của giao dịch
dân sự trong trường hợp luật có quy định.
```

### Lỗi và giới hạn đã ghi nhận

```json
{
  "collect": null,
  "ragas": {},
  "unavailable": null,
  "degraded": [
    "Phản hồi chưa đáp ứng đầy đủ yêu cầu chính; đánh dấu theo nội dung thay vì provider."
  ]
}
```


## Câu 30 · Nước

Tôi có thể đối chiếu tiền nước trên hóa đơn với đơn vị cấp nước như thế nào?

Trạng thái: Đã trả lời · cần rà nguồn. Provider: gemini-agent; model: gemini-3.8-flash-high.

faithfulness: 1.0 | answer_relevancy: 0.9015 | context_utilization: 0.5 | context_recall: 1.0 | context_precision: 1.0

ID nguồn chuẩn: water215-word.json, supplement-s05-word.json

ID nguồn đã truy xuất: water215-word.json, supplement-s05-word.json

Bạn có thể đối chiếu tiền nước bằng cách tra cứu hóa đơn điện tử trực tiếp trên trang tra cứu của đơn vị cấp nước khi có thông tin biên nhận thanh toán [2].

- Bước 1: Truy cập vào website tra cứu hóa đơn tại https://hddt.ctn-cantho.com.vn [2].
- Bước 2: Nhập thông tin của hóa đơn cần tra cứu vào các ô tương ứng như IDKH và Mã xác nhận trên Biên nhận thanh toán [2].
- Bước 3: Nhấn vào nút Tra cứu hóa đơn để thực hiện tra cứu theo thông tin đã nhập [2].
- Bước 4: Xem thông tin chi tiết về hóa đơn trên màn hình hiển thị hoặc tải các tệp hóa đơn đính kèm định dạng .ZIP và .PDF để đối chiếu [2].

Quy trình tra cứu này áp dụng theo hướng dẫn của CANTHOWASSCO và yêu cầu phải có thông tin IDKH cùng mã xác nhận trên biên nhận thanh toán [2].

Hướng dẫn/khuyến cáo của CANTHOWASSCO Công ty Cổ phần Cấp thoát nước Cần Thơ; không phải điều luật. Chỉ áp dụng hóa đơn CANTHOWASSCO, không mặc định mọi phòng ở Cần Thơ dùng cùng nhà cung cấp. Tra cứu cần thông tin hóa đơn phù hợp; không có công thức bắt buộc chia nước giữa các phòng. Không tải hóa đơn khách hàng trong đợt tìm nguồn này.

### Nguồn và ngữ cảnh

**[1] [Giá nước Cần Thơ 215/QĐ-UBND — bản Word cung cấp](https://capnuoccantho2.com.vn/View.aspx?wc=63&wp=332)**

Điều 1. Quy định giá nước sạch sinh hoạt tại đô thị và khu vực nông thôn áp dụng đối với các đơn vị kinh doanh nước sạch, các tổ chức và khách hàng sử dụng nước sạch trên địa bàn thành phố Cần Thơ như sau: | Khoản 1 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_corpus_v7_20261005/water215-word.json

```text
1. Giá nước sạch sinh hoạt tại đô thị, khu vực nông thôn năm 2024 do các đơn vị cấp nước cung cấp:

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

(Giá đã bao gồm thuế giá trị gia tăng, chưa bao gồm phí bảo vệ môi trường đối với nước thải sinh hoạt)
```

**[2] [Hướng dẫn tra cứu hóa đơn điện tử — CANTHOWASSCO Công ty Cổ phần Cấp thoát nước Cần Thơ](https://hddt.ctn-cantho.com.vn/huong-dan)**

Hướng dẫn tra cứu hóa đơn điện tử | Đoạn nguyên văn 0 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_supplement_corpus_v8_20261005/supplement-s05-word.json

```text
Hướng dẫn tra cứu hóa đơn điện tử

Bước 1: Truy cập vào website tra cứu hóa đơn tại https://hddt.ctn-cantho.com.vn

Bước 2: Nhập thông tin của hóa đơn cần tra cứu vào các ô tương ứng như: IDKH, Mã xác nhận trên Biên nhận thanh toán.

Bước 3: Nhấn vào nút Tra cứu hóa đơn để tra cứu hóa đơn với thông tin đã nhập

Bước 4: Màn hình sẽ hiển thị thông tin chi tiết về hóa đơn và sẽ cho phép tải 2 tệp hóa đơn đính kèm định dạng .ZIP (bao gồm có PDF và file XML) và .PDF
```

**[3] [Giá nước Cần Thơ 215/QĐ-UBND — bản Word cung cấp](https://capnuoccantho2.com.vn/View.aspx?wc=63&wp=332)**

Điều 1. Quy định giá nước sạch sinh hoạt tại đô thị và khu vực nông thôn áp dụng đối với các đơn vị kinh doanh nước sạch, các tổ chức và khách hàng sử dụng nước sạch trên địa bàn thành phố Cần Thơ như sau: | Khoản 2 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_corpus_v7_20261005/water215-word.json

```text
2. Giá nước sạch sinh hoạt tại đô thị, khu vực nông thôn do Trung tâm Nước sạch và Vệ sinh môi trường nông thôn cung cấp cho mục đích sinh hoạt:

STT

Nhóm khách hàng sử dụng nước sạch cho mục đích sinh hoạt

Giá tiêu thụ nước sạch (đồng/m3)

Nhóm 1

Hộ dân cư là hộ nghèo có sổ, hộ gia đình chính sách (gia đình Mẹ Việt Nam anh hùng, gia đình thương binh, gia đình liệt sĩ), hộ hiến đất.

4.000

Nhóm 2

Hộ dân cư và các nhóm đối tượng khác

7.450

(Giá đã bao gồm thuế giá trị gia tăng, chưa bao gồm phí bảo vệ môi trường đối với nước thải sinh hoạt)
```


## Câu 31 · Cư trú

Sinh viên thuê trọ tại Cần Thơ cần làm thủ tục cư trú nào?

Trạng thái: Đã trả lời · cần rà nguồn. Provider: gemini-agent; model: gemini-3.8-flash-high.

faithfulness: 0.9231 | answer_relevancy: 0.8884 | context_utilization: 1.0 | context_recall: 0.5 | context_precision: 1.0

ID nguồn chuẩn: residence68-word.json, residence154-official-word.json

ID nguồn đã truy xuất: residence68-word.json

Sinh viên đến sinh sống tại chỗ ở hợp pháp ngoài phạm vi xã nơi đã đăng ký thường trú từ 30 ngày trở lên để học tập phải thực hiện đăng ký tạm trú [1].

- Công dân sinh sống tại chỗ ở hợp pháp ngoài phạm vi đơn vị hành chính cấp xã nơi đã đăng ký thường trú từ 30 ngày trở lên để học tập phải thực hiện đăng ký tạm trú [1].
- Thời hạn tạm trú theo quy định tối đa là 02 năm và có thể tiếp tục gia hạn nhiều lần [2].

Nguồn trích dẫn chỉ quy định điều kiện và thời hạn tạm trú tối đa, chưa cung cấp thành phần hồ sơ và trình tự nộp chi tiết [1] [2].

Điều 9 quy định nghĩa vụ công dân; Điều 10 quy định chủ hộ/thành viên hộ gia đình, không tự đồng nhất chủ trọ với chủ hộ. Chỉ giải thích trách nhiệm và giấy tờ cơ bản, không điền tờ khai hoặc hướng dẫn hồ sơ chuyên sâu. Điều 26 và 29 phải đọc đúng trường hợp điều chỉnh/xóa; không suy ra hạn nộp 30 ngày hoặc tự động xóa từ điều kiện sinh sống 30 ngày.

### Nguồn và ngữ cảnh

**[1] [Luật Cư trú 68/2020/QH14 — Word Công báo](https://congbao.chinhphu.vn/van-ban/luat-so-68-2020-qh14-32684/33716.htm)**

Điều 27. Điều kiện đăng ký tạm trú | Khoản 1 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_repair_corpus_v16_20261006/residence68-word.json

```text
1. Công dân đến sinh sống tại chỗ ở hợp pháp ngoài phạm vi đơn vị hành
chính cấp xã nơi đã đăng ký thường trú để lao động, học tập hoặc vì mục
đích khác từ 30 ngày trở lên thì phải thực hiện đăng ký tạm trú.
```

**[2] [Luật Cư trú 68/2020/QH14 — Word Công báo](https://congbao.chinhphu.vn/van-ban/luat-so-68-2020-qh14-32684/33716.htm)**

Điều 27. Điều kiện đăng ký tạm trú | Khoản 2 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_repair_corpus_v16_20261006/residence68-word.json

```text
2. Thời hạn tạm trú tối đa là 02 năm và có thể tiếp tục gia hạn nhiều
lần.
```

**[3] [Luật Cư trú 68/2020/QH14 — Word Công báo](https://congbao.chinhphu.vn/van-ban/luat-so-68-2020-qh14-32684/33716.htm)**

Điều 27. Điều kiện đăng ký tạm trú | Khoản 3 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_repair_corpus_v16_20261006/residence68-word.json

```text
3. Công dân không được đăng ký tạm trú mới tại chỗ ở quy định tại Điều
23 của Luật này.

Điều 23. Địa điểm không được đăng ký thường trú mới | Khoản 1
1. Chỗ ở nằm trong địa điểm cấm, khu vực cấm xây dựng hoặc lấn, chiếm
hành lang bảo vệ quốc phòng, an ninh, giao thông, thủy lợi, đê điều, năng
lượng, mốc giới bảo vệ công trình hạ tầng kỹ thuật, di tích lịch sử - văn
hóa đã được xếp hạng, khu vực đã được cảnh báo về nguy cơ lở đất, lũ quét,
lũ ống và khu vực bảo vệ công trình khác theo quy định của pháp luật.

Điều 23. Địa điểm không được đăng ký thường trú mới | Khoản 2
2. Chỗ ở mà toàn bộ diện tích nhà ở nằm trên đất lấn, chiếm trái phép
hoặc chỗ ở xây dựng trên diện tích đất không đủ điều kiện xây dựng theo quy
định của pháp luật.

Điều 23. Địa điểm không được đăng ký thường trú mới | Khoản 3
3. Chỗ ở đã có quyết định thu hồi đất và quyết định phê duyệt phương án
bồi thường, hỗ trợ và tái định cư của cơ quan nhà nước có thẩm quyền; chỗ ở
là nhà ở mà một phần hoặc toàn bộ diện tích nhà ở đang có tranh chấp, khiếu
nại liên quan đến quyền sở hữu, quyền sử dụng nhưng chưa được giải quyết
theo quy định của pháp luật.

Điều 23. Địa điểm không được đăng ký thường trú mới | Khoản 4
4. Chỗ ở bị tịch thu theo quyết định của cơ quan nhà nước có thẩm quyền;
phương tiện được dùng làm nơi đăng ký thường trú đã bị xóa đăng ký phương
tiện hoặc không có giấy chứng nhận an toàn kỹ thuật và bảo vệ môi trường
theo quy định của pháp luật.

Điều 23. Địa điểm không được đăng ký thường trú mới | Khoản 5
5. Chỗ ở là nhà ở đã có quyết định phá dỡ của cơ quan nhà nước có thẩm
quyền.
```


## Câu 32 · Cư trú

Ai có trách nhiệm cung cấp thông tin, giấy tờ để người thuê đăng ký tạm trú?

Trạng thái: Trả lời một phần. Provider: gemini-agent; model: gemini-3.8-flash-high.

faithfulness: 1.0 | answer_relevancy: 0.0 | context_utilization: 1.0 | context_recall: 1.0 | context_precision: 1.0

ID nguồn chuẩn: residence68-word.json, residence154-official-word.json, residence58-official-word.json

ID nguồn đã truy xuất: residence58-official-word.json, residence154-official-word.json, residence68-word.json

Chưa đủ căn cứ từ nguồn để kết luận toàn bộ trách nhiệm riêng của chủ trọ về việc cung cấp giấy tờ tạm trú, nhưng công dân có nghĩa vụ tự cung cấp thông tin, giấy tờ cư trú của mình và chủ hộ có trách nhiệm tạo điều kiện, hướng dẫn thành viên trong hộ gia đình thực hiện đăng ký cư trú [2] [3] [4].

- Công dân có nghĩa vụ cung cấp đầy đủ, chính xác, kịp thời thông tin, giấy tờ, tài liệu về cư trú của mình cho cơ quan có thẩm quyền [3].
- Khi nộp hồ sơ, công dân cung cấp thông tin chứng minh chỗ ở hợp pháp để cơ quan đăng ký cư trú khai thác trên hệ thống định danh, cơ sở dữ liệu quốc gia về dân cư hoặc kho dữ liệu điện tử [2].
- Nếu không khai thác được trên hệ thống dữ liệu, công dân có trách nhiệm cung cấp bản sao, bản chụp hoặc bản điện tử giấy tờ chứng minh chỗ ở hợp pháp khi cơ quan đăng ký cư trú yêu cầu [2].
- Trường hợp đăng ký tạm trú vào chỗ ở hợp pháp do thuê, giấy tờ chứng minh chỗ ở hợp pháp là văn bản cho thuê của cơ quan, tổ chức, cá nhân và không phải công chứng, chứng thực [1].
- Chủ hộ có quyền và nghĩa vụ thực hiện, tạo điều kiện, hướng dẫn thành viên hộ gia đình thực hiện quy định về đăng ký cư trú theo luật định [4].

Nguồn chưa quy định riêng nghĩa vụ pháp lý của bên cho thuê trọ trong việc cung cấp hồ sơ hay giấy tờ đăng ký tạm trú cho người thuê [2] [3] [4].
Quy định về chủ hộ trong Luật Cư trú áp dụng cho hộ gia đình và không được tự đồng nhất chủ hộ với chủ nhà trọ [4].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng.
Nguồn hiện có xác nhận nghĩa vụ của công dân và hồ sơ đăng ký; chưa có căn cứ riêng để kết luận toàn bộ nghĩa vụ cung cấp giấy tờ của chủ trọ.
Khoản 2, 5, 7 Điều 4 sửa điểm a khoản 3 Điều 5, khoản 5 Điều 8 và Điều 10 Nghị định 154/2024/NĐ-CP. Giữ nguyên điều kiện, chủ thể và dẫn chiếu; không coi mọi chuyển trọ đều phải nộp hồ sơ xóa trong 7 ngày. Khoản 2 Điều 6 có mốc hiệu lực riêng cho người chưa thành niên, phần đó không được trích tuyển ở đây.
Chỉ giữ khoản 1 Điều 5 về khai thác thông tin và yêu cầu giấy tờ khi không khai thác được dữ liệu. Không giữ điểm a khoản 3 Điều 5 và Điều 10 bản cũ vì đã sửa bởi Nghị định 58/2026/NĐ-CP.
Điều 9 quy định nghĩa vụ công dân; Điều 10 quy định chủ hộ/thành viên hộ gia đình, không tự đồng nhất chủ trọ với chủ hộ. Chỉ giải thích trách nhiệm và giấy tờ cơ bản, không điền tờ khai hoặc hướng dẫn hồ sơ chuyên sâu. Điều 26 và 29 phải đọc đúng trường hợp điều chỉnh/xóa; không suy ra hạn nộp 30 ngày hoặc tự động xóa từ điều kiện sinh sống 30 ngày.

### Nguồn và ngữ cảnh

**[1] [Nghị định 58/2026/NĐ-CP — Word Công báo](https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-58-2026-nd-cp-468975/62899.htm)**

Điều 4. Sửa đổi, bổ sung một số điều của Nghị định số 154/2024/NĐ-CP quy định chi tiết một số điều và biện pháp thi hành Luật Cư trú (sau đây viết gọn là Nghị định số 154/2024/NĐ-CP) | Khoản 2 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_repair_corpus_v16_20261006/residence58-official-word.json

```text
2. Sửa đổi, bổ sung điểm a khoản 3 Điều 5 như sau:

“a) Một trong những giấy tờ, tài liệu quy định tại khoản 2 Điều này, trừ trường hợp đăng ký tạm trú vào chỗ ở hợp pháp do thuê, mượn, ở nhờ thì giấy tờ, tài liệu chứng minh chỗ ở hợp pháp là văn bản cho thuê, cho mượn, cho ở nhờ chỗ ở hợp pháp của cơ quan, tổ chức, cá nhân và văn bản đó không phải công chứng hoặc chứng thực;”.
```

**[2] [Nghị định 154/2024/NĐ-CP — Word Công báo](https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-154-2024-nd-cp-43275.htm)**

Điều 5. Giấy tờ, tài liệu, thông tin chứng minh chỗ ở hợp pháp | Khoản 1 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_repair_corpus_v16_20261006/residence154-official-word.json

```text
1. Công dân cung cấp thông tin chứng minh về chỗ ở hợp pháp cho cơ quan
đăng ký cư trú khi nộp hồ sơ đăng ký cư trú, cơ quan đăng ký cư trú có
trách nhiệm khai thác thông tin này trong căn cước điện tử, tài khoản định
danh điện tử trên hệ thống định danh và xác thực điện tử qua Ứng dụng định
danh quốc gia hoặc trong Cơ sở dữ liệu quốc gia về dân cư, Cơ sở dữ liệu về
cư trú, Kho quản lý dữ liệu điện tử tổ chức, cá nhân trên Cổng dịch vụ công
quốc gia, Hệ thống thông tin giải quyết thủ tục hành chính cấp bộ, cấp tỉnh
hoặc cơ sở dữ liệu quốc gia, cơ sở dữ liệu chuyên ngành khác.
 Trường hợp không khai thác được thông tin chứng minh về chỗ ở hợp pháp
trong cơ sở dữ liệu, hệ thống thông tin hoặc Ứng dụng định danh quốc gia
thì cơ quan đăng ký cư trú có trách nhiệm kiểm tra, xác minh để giải quyết
thủ tục về cư trú; công dân có trách nhiệm cung cấp bản sao, bản chụp, bản
điện tử một trong các giấy tờ, tài liệu chứng minh về chỗ ở hợp pháp khi cơ
quan đăng ký cư trú có yêu cầu.
```

**[3] [Luật Cư trú 68/2020/QH14 — Word Công báo](https://congbao.chinhphu.vn/van-ban/luat-so-68-2020-qh14-32684/33716.htm)**

Điều 9. Nghĩa vụ của công dân về cư trú | Khoản 2 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_repair_corpus_v16_20261006/residence68-word.json

```text
2. Cung cấp đầy đủ, chính xác, kịp thời thông tin, giấy tờ, tài liệu về
cư trú của mình cho cơ quan, người có thẩm quyền và chịu trách nhiệm về
thông tin, giấy tờ, tài liệu đã cung cấp.
```

**[4] [Luật Cư trú 68/2020/QH14 — Word Công báo](https://congbao.chinhphu.vn/van-ban/luat-so-68-2020-qh14-32684/33716.htm)**

Điều 10. Quyền, nghĩa vụ của chủ hộ và thành viên hộ gia đình về cư trú | Khoản 5 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_repair_corpus_v16_20261006/residence68-word.json

```text
5. Chủ hộ có quyền và nghĩa vụ thực hiện, tạo điều kiện, hướng dẫn thành
viên hộ gia đình thực hiện quy định về đăng ký, quản lý cư trú và những nội
dung khác theo quy định của Luật này; thông báo với cơ quan đăng ký cư trú
về việc trong hộ gia đình có thành viên thuộc trường hợp quy định tại khoản
1 Điều 24, khoản 1 Điều 29 của Luật này.

Điều 29. Xóa đăng ký tạm trú | Khoản 1
1. Người thuộc một trong các trường hợp sau đây thì bị xóa đăng ký tạm
trú:
 a) Chết; có quyết định của Tòa án tuyên bố mất tích hoặc đã chết;
 b) Đã có quyết định hủy bỏ đăng ký tạm trú quy định tại Điều 35 của Luật
này;
 c) Vắng mặt liên tục tại nơi tạm trú từ 06 tháng trở lên mà không đăng
ký tạm trú tại chỗ ở khác;
 d) Đã được cơ quan có thẩm quyền cho thôi quốc tịch Việt Nam, tước quốc
tịch Việt Nam, hủy bỏ quyết định cho nhập quốc tịch Việt Nam;
 đ) Đã được đăng ký thường trú tại chính nơi tạm trú;
 e) Người đã đăng ký tạm trú tại chỗ ở do thuê, mượn, ở nhờ nhưng đã chấm
dứt việc thuê, mượn, ở nhờ mà không đăng ký tạm trú tại chỗ ở khác;
 g) Người đã đăng ký tạm trú tại chỗ ở hợp pháp nhưng sau đó quyền sở hữu
chỗ ở đó đã chuyển cho người khác, trừ trường hợp được chủ sở hữu mới đồng
ý cho tiếp tục sinh sống tại chỗ ở đó;
 h) Người đăng ký tạm trú tại chỗ ở đã bị phá dỡ, tịch thu theo quyết
định của cơ quan nhà nước có thẩm quyền hoặc tại phương tiện đã bị xóa đăng
ký phương tiện theo quy định của pháp luật.
```

**[5] [Nghị định 58/2026/NĐ-CP — Word Công báo](https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-58-2026-nd-cp-468975/62899.htm)**

Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_repair_corpus_v16_20261006/residence58-official-word.json

```text
Điều 6. Hiệu lực thi hành và quy định chuyển tiếp | Khoản 1
1. Nghị định này có hiệu lực thi hành từ ngày 15 tháng 3 năm 2026, trừ quy định tại khoản 2 Điều này.

Điều 6. Hiệu lực thi hành và quy định chuyển tiếp | Khoản 2
2. Quy định tại khoản 4 Điều 4 của Nghị định này có hiệu lực thi hành từ ngày 01 tháng 7 năm 2026.
```

### Lỗi và giới hạn đã ghi nhận

```json
{
  "collect": null,
  "ragas": {},
  "unavailable": null,
  "degraded": [
    "Phản hồi chưa đáp ứng đầy đủ yêu cầu chính; đánh dấu theo nội dung thay vì provider."
  ]
}
```


## Câu 33 · Cư trú

Tôi cần chuẩn bị những giấy tờ gì để đăng ký tạm trú tại phòng trọ?

Trạng thái: Đã trả lời · cần rà nguồn. Provider: gemini-agent; model: gemini-3.8-flash-high.

faithfulness: 1.0 | answer_relevancy: 0.9037 | context_utilization: 0.8333 | context_recall: 0.5 | context_precision: 1.0

ID nguồn chuẩn: residence68-word.json, residence154-official-word.json

ID nguồn đã truy xuất: residence68-word.json

Hồ sơ đăng ký tạm trú theo luật định gồm tờ khai thay đổi thông tin cư trú và giấy tờ chứng minh chỗ ở hợp pháp [1].

- Chuẩn bị tờ khai thay đổi thông tin cư trú [1].
- Chuẩn bị giấy tờ, tài liệu chứng minh chỗ ở hợp pháp [1].
- Đối với người đăng ký là người chưa thành niên, tờ khai phải ghi rõ ý kiến đồng ý của cha, mẹ hoặc người giám hộ, trừ khi đã có văn bản đồng ý riêng [1].
- Nộp hồ sơ đăng ký tạm trú đến cơ quan đăng ký cư trú nơi dự kiến tạm trú [3].

Nguồn trích dẫn không liệt kê cụ thể các loại giấy tờ chi tiết cấu thành giấy tờ chứng minh chỗ ở hợp pháp khi thuê trọ [1].

Điều 9 quy định nghĩa vụ công dân; Điều 10 quy định chủ hộ/thành viên hộ gia đình, không tự đồng nhất chủ trọ với chủ hộ. Chỉ giải thích trách nhiệm và giấy tờ cơ bản, không điền tờ khai hoặc hướng dẫn hồ sơ chuyên sâu. Điều 26 và 29 phải đọc đúng trường hợp điều chỉnh/xóa; không suy ra hạn nộp 30 ngày hoặc tự động xóa từ điều kiện sinh sống 30 ngày.

### Nguồn và ngữ cảnh

**[1] [Luật Cư trú 68/2020/QH14 — Word Công báo](https://congbao.chinhphu.vn/van-ban/luat-so-68-2020-qh14-32684/33716.htm)**

Điều 28. Hồ sơ, thủ tục đăng ký tạm trú, gia hạn tạm trú | Khoản 1 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_repair_corpus_v16_20261006/residence68-word.json

```text
1. Hồ sơ đăng ký tạm trú bao gồm:
 a) Tờ khai thay đổi thông tin cư trú; đối với người đăng ký tạm trú là
người chưa thành niên thì trong tờ khai phải ghi rõ ý kiến đồng ý của cha,
mẹ hoặc người giám hộ, trừ trường hợp đã có ý kiến đồng ý bằng văn bản;
 b) Giấy tờ, tài liệu chứng minh chỗ ở hợp pháp.
```

**[2] [Luật Cư trú 68/2020/QH14 — Word Công báo](https://congbao.chinhphu.vn/van-ban/luat-so-68-2020-qh14-32684/33716.htm)**

Điều 28. Hồ sơ, thủ tục đăng ký tạm trú, gia hạn tạm trú | Khoản 3 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_repair_corpus_v16_20261006/residence68-word.json

```text
3. Trong thời hạn 15 ngày trước ngày kết thúc thời hạn tạm trú đã đăng
ký, công dân phải làm thủ tục gia hạn tạm trú.
 Hồ sơ, thủ tục gia hạn tạm trú thực hiện theo quy định tại khoản 1 và
khoản 2 Điều này. Sau khi thẩm định hồ sơ, cơ quan đăng ký cư trú có trách
nhiệm cập nhật thông tin về thời hạn tạm trú mới của người đăng ký vào Cơ
sở dữ liệu về cư trú và thông báo cho người đăng ký về việc đã cập nhật
thông tin đăng ký tạm trú; trường hợp từ chối đăng ký thì phải trả lời bằng
văn bản và nêu rõ lý do.
```

**[3] [Luật Cư trú 68/2020/QH14 — Word Công báo](https://congbao.chinhphu.vn/van-ban/luat-so-68-2020-qh14-32684/33716.htm)**

Điều 28. Hồ sơ, thủ tục đăng ký tạm trú, gia hạn tạm trú | Khoản 2 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_repair_corpus_v16_20261006/residence68-word.json

```text
2. Người đăng ký tạm trú nộp hồ sơ đăng ký tạm trú đến cơ quan đăng ký
cư trú nơi mình dự kiến tạm trú.
 Khi tiếp nhận hồ sơ đăng ký tạm trú, cơ quan đăng ký cư trú kiểm tra và
cấp phiếu tiếp nhận hồ sơ cho người đăng ký; trường hợp hồ sơ chưa đầy đủ
thì hướng dẫn người đăng ký bổ sung hồ sơ.
 Trong thời hạn 03 ngày làm việc kể từ ngày nhận được hồ sơ đầy đủ và hợp
lệ, cơ quan đăng ký cư trú có trách nhiệm thẩm định, cập nhật thông tin về
nơi tạm trú mới, thời hạn tạm trú của người đăng ký vào Cơ sở dữ liệu về cư
trú và thông báo cho người đăng ký về việc đã cập nhật thông tin đăng ký
tạm trú; trường hợp từ chối đăng ký thì phải trả lời bằng văn bản và nêu rõ
lý do.
```


## Câu 34 · Cư trú

Nếu chuyển sang phòng trọ khác, tôi cần cập nhật thông tin cư trú thế nào?

Trạng thái: Trả lời một phần. Provider: gemini-agent; model: gemini-3.8-flash-high.

faithfulness: 0.9091 | answer_relevancy: 0.8868 | context_utilization: 1.0 | context_recall: 1.0 | context_precision: 1.0

ID nguồn chuẩn: residence68-word.json, residence58-official-word.json

ID nguồn đã truy xuất: residence68-word.json, residence58-official-word.json

Khi chuyển sang chỗ ở mới, người thuê nộp hồ sơ đăng ký tạm trú tại nơi dự kiến tạm trú mới và thực hiện thủ tục xóa đăng ký tạm trú tại nơi ở cũ nếu thuộc trường hợp chấm dứt thuê mà không đăng ký tạm trú tại chỗ ở khác [1] [2] [3].

- Nộp hồ sơ đăng ký tạm trú đến cơ quan đăng ký cư trú nơi dự kiến tạm trú mới [3].
- Trong thời hạn 03 ngày làm việc kể từ ngày nhận đủ hồ sơ hợp lệ, cơ quan đăng ký cư trú thẩm định, cập nhật nơi tạm trú mới vào Cơ sở dữ liệu về cư trú và thông báo kết quả [3].
- Người đã đăng ký tạm trú do thuê nhà nhưng chấm dứt thuê mà không đăng ký tạm trú tại chỗ ở khác thì bị xóa đăng ký tạm trú tại nơi cũ [1].
- Trường hợp thuộc diện phải xóa, người thuộc diện xóa hoặc đại diện nộp 01 bộ hồ sơ trực tuyến qua Cổng dịch vụ công quốc gia hoặc VNeID trong thời hạn 07 ngày [2] [5].

Nguồn trích tuyển chưa nêu chi tiết toàn bộ thành phần hồ sơ đăng ký tạm trú tại nơi mới [3].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng.
Cần đối chiếu điều/khoản được dẫn chiếu còn thiếu; đoạn trích chưa đủ để kết luận toàn bộ điều kiện và ngoại lệ.
Điều 9 quy định nghĩa vụ công dân; Điều 10 quy định chủ hộ/thành viên hộ gia đình, không tự đồng nhất chủ trọ với chủ hộ. Chỉ giải thích trách nhiệm và giấy tờ cơ bản, không điền tờ khai hoặc hướng dẫn hồ sơ chuyên sâu. Điều 26 và 29 phải đọc đúng trường hợp điều chỉnh/xóa; không suy ra hạn nộp 30 ngày hoặc tự động xóa từ điều kiện sinh sống 30 ngày.
Khoản 2, 5, 7 Điều 4 sửa điểm a khoản 3 Điều 5, khoản 5 Điều 8 và Điều 10 Nghị định 154/2024/NĐ-CP. Giữ nguyên điều kiện, chủ thể và dẫn chiếu; không coi mọi chuyển trọ đều phải nộp hồ sơ xóa trong 7 ngày. Khoản 2 Điều 6 có mốc hiệu lực riêng cho người chưa thành niên, phần đó không được trích tuyển ở đây.

### Nguồn và ngữ cảnh

**[1] [Luật Cư trú 68/2020/QH14 — Word Công báo](https://congbao.chinhphu.vn/van-ban/luat-so-68-2020-qh14-32684/33716.htm)**

Điều 29. Xóa đăng ký tạm trú | Khoản 1 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_repair_corpus_v16_20261006/residence68-word.json

```text
1. Người thuộc một trong các trường hợp sau đây thì bị xóa đăng ký tạm
trú:
 a) Chết; có quyết định của Tòa án tuyên bố mất tích hoặc đã chết;
 b) Đã có quyết định hủy bỏ đăng ký tạm trú quy định tại Điều 35 của Luật
này;
 c) Vắng mặt liên tục tại nơi tạm trú từ 06 tháng trở lên mà không đăng
ký tạm trú tại chỗ ở khác;
 d) Đã được cơ quan có thẩm quyền cho thôi quốc tịch Việt Nam, tước quốc
tịch Việt Nam, hủy bỏ quyết định cho nhập quốc tịch Việt Nam;
 đ) Đã được đăng ký thường trú tại chính nơi tạm trú;
 e) Người đã đăng ký tạm trú tại chỗ ở do thuê, mượn, ở nhờ nhưng đã chấm
dứt việc thuê, mượn, ở nhờ mà không đăng ký tạm trú tại chỗ ở khác;
 g) Người đã đăng ký tạm trú tại chỗ ở hợp pháp nhưng sau đó quyền sở hữu
chỗ ở đó đã chuyển cho người khác, trừ trường hợp được chủ sở hữu mới đồng
ý cho tiếp tục sinh sống tại chỗ ở đó;
 h) Người đăng ký tạm trú tại chỗ ở đã bị phá dỡ, tịch thu theo quyết
định của cơ quan nhà nước có thẩm quyền hoặc tại phương tiện đã bị xóa đăng
ký phương tiện theo quy định của pháp luật.
```

**[2] [Nghị định 58/2026/NĐ-CP — Word Công báo](https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-58-2026-nd-cp-468975/62899.htm)**

Điều 4. Sửa đổi, bổ sung một số điều của Nghị định số 154/2024/NĐ-CP quy định chi tiết một số điều và biện pháp thi hành Luật Cư trú (sau đây viết gọn là Nghị định số 154/2024/NĐ-CP) | Khoản 7 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_repair_corpus_v16_20261006/residence58-official-word.json

```text
7. Sửa đổi, bổ sung Điều 10 như sau:

“Điều 10. Hồ sơ, thủ tục xóa đăng ký tạm trú

1. Trong thời hạn 01 ngày kể từ ngày nhận được quyết định hủy bỏ đăng ký tạm trú của thủ trưởng cấp trên trực tiếp hoặc ngay sau khi ra quyết định hủy bỏ đăng ký tạm trú đối với công dân, cơ quan đăng ký cư trú thực hiện việc xóa đăng ký tạm trú đối với công dân và cập nhật việc xóa đăng ký tạm trú vào Cơ sở dữ liệu về cư trú, Cơ sở dữ liệu quốc gia về dân cư.

2. Trong thời hạn 01 ngày làm việc, kể từ ngày hệ thống Cơ sở dữ liệu quốc gia về dân cư, cơ quan đăng ký cư trú tiếp nhận thông tin quy định tại điểm a, d, đ khoản 1 Điều 29 Luật Cư trú thông qua kết nối, chia sẻ, đồng bộ dữ liệu từ cơ sở dữ liệu quốc gia, cơ sở dữ liệu chuyên ngành, cơ sở dữ liệu khác do cơ quan, tổ chức quản lý, cơ quan đăng ký cư trú có trách nhiệm kiểm tra, xác minh, thực hiện xóa đăng ký tạm trú đối với công dân và cập nhật việc xóa đăng ký tạm trú vào Cơ sở dữ liệu về cư trú, Cơ sở dữ liệu quốc gia về dân cư.

3. Trong thời hạn 07 ngày, kể từ ngày hộ gia đình có người thuộc diện xóa đăng ký tạm trú theo quy định tại điểm c, e, g, h khoản 1 Điều 29 Luật Cư trú thì người thuộc diện xóa đăng ký tạm trú hoặc đại diện hộ gia đình hoặc người đại diện hợp pháp có trách nhiệm thực hiện thủ tục xóa đăng ký tạm trú.

a) Hồ sơ xóa đăng ký tạm trú gồm: Tờ khai thay đổi thông tin cư trú và giấy tờ, tài liệu chứng minh thuộc một trong các trường hợp xóa đăng ký tạm trú.

b) Người thực hiện thủ tục nộp 01 hồ sơ trực tuyến qua Cổng dịch vụ công quốc gia hoặc Ứng dụng định danh quốc gia (VNeID) đến cơ quan đăng ký cư trú.

4. Trường hợp người bị đề nghị xóa đăng ký tạm trú có thông tin trong Cơ sở dữ liệu quốc gia về dân cư nhưng không đầy đủ, chính xác thì cơ quan đăng ký cư trú có trách nhiệm cập nhật, điều chỉnh thông tin vào Cơ sở dữ liệu quốc gia về dân cư.

5. Trong thời hạn 03 ngày làm việc, kể từ ngày nhận được hồ sơ hợp lệ thì cơ quan đăng ký cư trú phải xóa đăng ký tạm trú đối với công dân và cập nhật việc xóa đăng ký tạm trú vào Cơ sở dữ liệu về cư trú, Cơ sở dữ liệu quốc gia về dân cư.

6. Trường hợp thuộc diện xóa đăng ký tạm trú theo quy định tại điểm c, e, g, h khoản 1 Điều 29 Luật Cư trú mà hộ gia đình chỉ có 01 người hoặc người thuộc diện xóa đăng ký tạm trú hoặc đại diện hộ gia đình hoặc người đại diện hợp pháp không thực hiện thủ tục xóa đăng ký tạm trú thì cơ quan đăng ký cư trú có trách nhiệm kiểm tra, xác minh, lập biên bản về việc công dân, đại diện hộ gia đình không thực hiện thủ tục xóa đăng ký tạm trú và thực hiện xóa đăng ký tạm trú đối với công dân.

7. Cơ quan, đơn vị quản lý người học tập, công tác, làm việc trong lực lượng vũ trang nhân dân có văn bản đề nghị cơ quan đăng ký cư trú trên địa bàn đóng quân xóa đăng ký tạm trú đối với người thuộc đơn vị mình quản lý. Văn bản đề nghị cần nêu rõ họ, chữ đệm và tên khai sinh; ngày, tháng, năm sinh; số định danh cá nhân của người cần xóa đăng ký tạm trú; lý do đề nghị xóa đăng ký tạm trú.

8. Sau khi thực hiện việc xóa đăng ký tạm trú, cơ quan đăng ký cư trú thông báo bằng văn bản giấy hoặc bản điện tử hoặc hình thức điện tử khác cho người bị xóa đăng ký tạm trú hoặc đại diện hộ gia đình.”.
```

**[3] [Luật Cư trú 68/2020/QH14 — Word Công báo](https://congbao.chinhphu.vn/van-ban/luat-so-68-2020-qh14-32684/33716.htm)**

Điều 28. Hồ sơ, thủ tục đăng ký tạm trú, gia hạn tạm trú | Khoản 2 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_repair_corpus_v16_20261006/residence68-word.json

```text
2. Người đăng ký tạm trú nộp hồ sơ đăng ký tạm trú đến cơ quan đăng ký
cư trú nơi mình dự kiến tạm trú.
 Khi tiếp nhận hồ sơ đăng ký tạm trú, cơ quan đăng ký cư trú kiểm tra và
cấp phiếu tiếp nhận hồ sơ cho người đăng ký; trường hợp hồ sơ chưa đầy đủ
thì hướng dẫn người đăng ký bổ sung hồ sơ.
 Trong thời hạn 03 ngày làm việc kể từ ngày nhận được hồ sơ đầy đủ và hợp
lệ, cơ quan đăng ký cư trú có trách nhiệm thẩm định, cập nhật thông tin về
nơi tạm trú mới, thời hạn tạm trú của người đăng ký vào Cơ sở dữ liệu về cư
trú và thông báo cho người đăng ký về việc đã cập nhật thông tin đăng ký
tạm trú; trường hợp từ chối đăng ký thì phải trả lời bằng văn bản và nêu rõ
lý do.
```

**[4] [Luật Cư trú 68/2020/QH14 — Word Công báo](https://congbao.chinhphu.vn/van-ban/luat-so-68-2020-qh14-32684/33716.htm)**

Điều 29. Xóa đăng ký tạm trú | Khoản 2 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_repair_corpus_v16_20261006/residence68-word.json

```text
2. Cơ quan đã đăng ký tạm trú có thẩm quyền xóa đăng ký tạm trú và phải
ghi rõ lý do, thời điểm xóa đăng ký tạm trú trong Cơ sở dữ liệu về cư trú.
```

**[5] [Nghị định 58/2026/NĐ-CP — Word Công báo](https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-58-2026-nd-cp-468975/62899.htm)**

Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_repair_corpus_v16_20261006/residence58-official-word.json

```text
Điều 6. Hiệu lực thi hành và quy định chuyển tiếp | Khoản 1
1. Nghị định này có hiệu lực thi hành từ ngày 15 tháng 3 năm 2026, trừ quy định tại khoản 2 Điều này.

Điều 6. Hiệu lực thi hành và quy định chuyển tiếp | Khoản 2
2. Quy định tại khoản 4 Điều 4 của Nghị định này có hiệu lực thi hành từ ngày 01 tháng 7 năm 2026.
```

### Lỗi và giới hạn đã ghi nhận

```json
{
  "collect": null,
  "ragas": {},
  "unavailable": null,
  "degraded": [
    "Phản hồi chưa đáp ứng đầy đủ yêu cầu chính; đánh dấu theo nội dung thay vì provider."
  ]
}
```


## Câu 35 · PCCC

Khi xem phòng trọ, tôi nên kiểm tra những điều kiện phòng cháy, chữa cháy nào?

Trạng thái: Đã trả lời · cần rà nguồn. Provider: gemini-agent; model: gemini-3.8-flash-high.

faithfulness: 1.0 | answer_relevancy: 0.9047 | context_utilization: 1.0 | context_recall: 1.0 | context_precision: 1.0

ID nguồn chuẩn: fire55-word.json

ID nguồn đã truy xuất: fire55-word.json

Nguồn quy định nhà ở phải bảo đảm các điều kiện về thiết bị điện, nguồn nhiệt, phương tiện chữa cháy và lối thoát nạn khi sử dụng [1].

- Nguồn quy định nhà ở phải bố trí và duy trì lối thoát nạn, lối ra khẩn cấp hoặc lối đi bảo đảm cho việc thoát nạn [1].
- Nguồn quy định nhà ở phải có phương tiện phòng cháy, chữa cháy phù hợp với khả năng và điều kiện thực tế để sẵn sàng chữa cháy, thoát nạn [1].
- Nguồn quy định việc lắp đặt, sử dụng dây dẫn và thiết bị điện trong nhà phải bảo đảm an toàn điện, kịp thời sửa chữa, thay thế khi không bảo đảm an toàn [1] [3].
- Nguồn quy định phải bố trí nơi đun nấu, thờ cúng an toàn và không để vật, chất dễ cháy nổ gần nguồn lửa, nguồn nhiệt [1].
- Nguồn quy định nơi sạc xe động cơ điện trong nhà phải có giải pháp an toàn phòng cháy, nếu sạc tập trung phải có giải pháp ngăn cháy và phương tiện chữa cháy phù hợp [1] [3].

Nhà ở thuộc danh mục cơ sở quản lý về phòng cháy chữa cháy hoặc nhà ở kết hợp sản xuất, kinh doanh phải đáp ứng thêm các điều kiện an toàn riêng theo luật định [1] [2].

### Nguồn và ngữ cảnh

**[1] [Luật PCCC 55/2024/QH15 — Word Công báo](https://congbao.chinhphu.vn/van-ban-dang-cong-bao/quoc-hoi-c31/trang-19.htm)**

Điều 20. Phòng cháy đối với nhà ở · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_corpus_v7_20261005/fire55-word.json

```text
1. Nhà ở không thuộc loại hình quy định tại khoản 3 và khoản 4 Điều này
phải bảo đảm các điều kiện an toàn về phòng cháy sau đây:
 a) Lắp đặt, sử dụng thiết bị điện bảo đảm điều kiện an toàn về phòng
cháy quy định tại điểm c khoản 1 Điều 24 của Luật này;
 b) Bố trí bếp đun nấu, nơi thờ cúng, đốt vàng mã bảo đảm an toàn; không
để vật, chất dễ cháy, nổ gần nguồn lửa, nguồn nhiệt.

2. Nhà ở không thuộc loại hình quy định tại khoản 3 và khoản 4 Điều này
phải bảo đảm các điều kiện về chữa cháy, thoát nạn sau đây:
 a) Có phương tiện phòng cháy, chữa cháy phù hợp với khả năng, điều kiện
thực tế để sẵn sàng chữa cháy, thoát nạn;
 b) Bố trí, duy trì lối thoát nạn, lối ra khẩn cấp hoặc lối đi bảo đảm
việc thoát nạn.

3. Nhà ở có quy chuẩn kỹ thuật, tiêu chuẩn được viện dẫn trong văn bản
quy phạm pháp luật hoặc trong quy chuẩn kỹ thuật về phòng cháy, chữa cháy
và cứu nạn, cứu hộ thực hiện theo tiêu chuẩn, quy chuẩn kỹ thuật đó.

4. Nhà ở trong danh mục cơ sở thuộc diện quản lý về phòng cháy và chữa
cháy thực hiện theo quy định tại Điều 23 của Luật này.

5. Đối với nhà ở tại thành phố trực thuộc Trung ương thuộc khu vực không
bảo đảm hạ tầng giao thông hoặc nguồn nước phục vụ chữa cháy theo quy định
của pháp luật, quy chuẩn kỹ thuật trong hoạt động phòng cháy, chữa cháy thì
phải trang bị bình chữa cháy, thiết bị truyền tin báo cháy kết nối với hệ
thống Cơ sở dữ liệu về phòng cháy, chữa cháy, cứu nạn, cứu hộ và truyền tin
báo cháy theo lộ trình do Chính phủ quy định.
 Đối với nhà ở tại khu vực khác thì khuyến khích trang bị thiết bị truyền
tin báo cháy kết nối với hệ thống Cơ sở dữ liệu về phòng cháy, chữa cháy,
cứu nạn, cứu hộ và truyền tin báo cháy.
 Ủy ban nhân dân thành phố trực thuộc Trung ương xác định khu vực không
bảo đảm hạ tầng giao thông hoặc nguồn nước phục vụ chữa cháy.

6. Lực lượng Cảnh sát phòng cháy, chữa cháy và cứu nạn, cứu hộ có trách
nhiệm hướng dẫn việc kết nối thiết bị truyền tin báo cháy với hệ thống Cơ
sở dữ liệu về phòng cháy, chữa cháy, cứu nạn, cứu hộ và truyền tin báo cháy
khi có yêu cầu.

Điều 24. Phòng cháy trong lắp đặt, sử dụng điện cho sinh hoạt, sản xuất | Khoản 1
1. Trong lắp đặt, sử dụng điện cho sinh hoạt phải bảo đảm các điều kiện
an toàn về phòng cháy sau đây:
 a) Chấp hành quy định về an toàn trong sử dụng điện cho sinh hoạt theo
quy định của pháp luật về điện lực;
 b) Đơn vị bán lẻ điện khi đấu nối điện sinh hoạt phải tư vấn việc lắp
đặt, sử dụng đối với hệ thống, thiết bị điện để bảo đảm an toàn về phòng
cháy;
 c) Việc lắp đặt, sử dụng dây dẫn điện, thiết bị điện trong nhà phải bảo
đảm yêu cầu về an toàn điện theo quy định của pháp luật; thường xuyên kiểm
tra, kịp thời sửa chữa, thay thế dây dẫn điện, thiết bị điện không bảo đảm
an toàn về phòng cháy;
 d) Chỉ được sử dụng thiết bị sạc điện cho xe động cơ điện bảo đảm quy
chuẩn kỹ thuật quốc gia; nơi sạc điện cho xe động cơ điện trong nhà phải có
giải pháp bảo đảm an toàn về phòng cháy; khu vực sạc điện cho xe động cơ
điện tập trung trong nhà còn phải có giải pháp ngăn cháy và trang bị phương
tiện chữa cháy phù hợp, bảo đảm tiêu chuẩn.

Điều 23. Phòng cháy đối với cơ sở | Khoản 1
1. Cơ sở phải bảo đảm các điều kiện an toàn về phòng cháy sau đây:
 a) Có nội quy phòng cháy, chữa cháy, cứu nạn, cứu hộ phù hợp với từng
loại hình cơ sở;
 b) Trang bị phương tiện, hệ thống phòng cháy, chữa cháy, cứu nạn, cứu hộ
theo quy định của pháp luật;
 c) Trang bị thiết bị truyền tin báo cháy kết nối với hệ thống Cơ sở dữ
liệu về phòng cháy, chữa cháy, cứu nạn, cứu hộ và truyền tin báo cháy; khai
báo, cập nhật dữ liệu về phòng cháy, chữa cháy, cứu nạn, cứu hộ theo lộ
trình do Chính phủ quy định;
 d) Thực hiện các yêu cầu về phòng cháy và chữa cháy quy định tại các
điểm a, b, c, d, đ và e khoản 1 Điều 16 của Luật này;
 đ) Có phương án chữa cháy, cứu nạn, cứu hộ;
 e) Thành lập lực lượng phòng cháy, chữa cháy và cứu nạn, cứu hộ cơ sở
hoặc lực lượng phòng cháy, chữa cháy và cứu nạn, cứu hộ chuyên ngành theo
quy định tại Điều 37 của Luật này hoặc phân công người thực hiện nhiệm vụ
phòng cháy, chữa cháy, cứu nạn, cứu hộ.

Điều 23. Phòng cháy đối với cơ sở | Khoản 2
2. Cơ quan, tổ chức hoạt động trong phạm vi một cơ sở phải bảo đảm các
điều kiện an toàn về phòng cháy sau đây:
 a) Có nội quy phòng cháy, chữa cháy, cứu nạn, cứu hộ phù hợp với tính
chất hoạt động của cơ quan, tổ chức;
 b) Bảo đảm an toàn trong sử dụng nguồn lửa, nguồn nhiệt, thiết bị, dụng
cụ sinh lửa, sinh nhiệt, chất dễ cháy, nổ trong phạm vi quản lý;
 c) Cử người tham gia lực lượng phòng cháy, chữa cháy và cứu nạn, cứu hộ
cơ sở hoặc lực lượng phòng cháy, chữa cháy và cứu nạn, cứu hộ chuyên ngành
theo quy định của pháp luật;
 d) Thực hiện, duy trì điều kiện an toàn về phòng cháy và chữa cháy trong
phạm vi quản lý.
```

**[2] [Luật PCCC 55/2024/QH15 — Word Công báo](https://congbao.chinhphu.vn/van-ban-dang-cong-bao/quoc-hoi-c31/trang-19.htm)**

Điều 21. Phòng cháy đối với nhà ở kết hợp sản xuất, kinh doanh · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_corpus_v7_20261005/fire55-word.json

```text
1. Nhà ở kết hợp sản xuất, kinh doanh phải bảo đảm các điều kiện an toàn
về phòng cháy sau đây:
 a) Các điều kiện an toàn về phòng cháy quy định tại Điều 20 của Luật
này;
 b) Có biển cấm, biển báo, biển chỉ dẫn theo quy định;
 c) Khu vực sản xuất, kinh doanh hàng hóa có nguy cơ cháy, nổ phải có
giải pháp ngăn cách hoặc ngăn cháy với khu vực để ở.

2. Nhà ở kết hợp sản xuất, kinh doanh hàng hóa nguy hiểm về cháy, nổ
phải bảo đảm các điều kiện an toàn về phòng cháy sau đây:
 a) Các điều kiện an toàn về phòng cháy quy định tại khoản 1 Điều này;
 b) Không bố trí chỗ ngủ trong khu vực sản xuất, kinh doanh;
 c) Có phương tiện báo cháy, giải pháp thông gió, thiết bị phát hiện sự
cố rò rỉ chất khí nguy hiểm về cháy, nổ phù hợp với công năng, đặc điểm của
nhà ở kết hợp sản xuất, kinh doanh hàng hóa nguy hiểm về cháy, nổ;
 d) Khu vực sản xuất, kinh doanh hàng hóa nguy hiểm về cháy, nổ phải được
ngăn cháy với lối thoát nạn của khu vực để ở.

Điều 20. Phòng cháy đối với nhà ở | Khoản 1
1. Nhà ở không thuộc loại hình quy định tại khoản 3 và khoản 4 Điều này
phải bảo đảm các điều kiện an toàn về phòng cháy sau đây:
 a) Lắp đặt, sử dụng thiết bị điện bảo đảm điều kiện an toàn về phòng
cháy quy định tại điểm c khoản 1 Điều 24 của Luật này;
 b) Bố trí bếp đun nấu, nơi thờ cúng, đốt vàng mã bảo đảm an toàn; không
để vật, chất dễ cháy, nổ gần nguồn lửa, nguồn nhiệt.

Điều 20. Phòng cháy đối với nhà ở | Khoản 2
2. Nhà ở không thuộc loại hình quy định tại khoản 3 và khoản 4 Điều này
phải bảo đảm các điều kiện về chữa cháy, thoát nạn sau đây:
 a) Có phương tiện phòng cháy, chữa cháy phù hợp với khả năng, điều kiện
thực tế để sẵn sàng chữa cháy, thoát nạn;
 b) Bố trí, duy trì lối thoát nạn, lối ra khẩn cấp hoặc lối đi bảo đảm
việc thoát nạn.

Điều 20. Phòng cháy đối với nhà ở | Khoản 3
3. Nhà ở có quy chuẩn kỹ thuật, tiêu chuẩn được viện dẫn trong văn bản
quy phạm pháp luật hoặc trong quy chuẩn kỹ thuật về phòng cháy, chữa cháy
và cứu nạn, cứu hộ thực hiện theo tiêu chuẩn, quy chuẩn kỹ thuật đó.

Điều 20. Phòng cháy đối với nhà ở | Khoản 4
4. Nhà ở trong danh mục cơ sở thuộc diện quản lý về phòng cháy và chữa
cháy thực hiện theo quy định tại Điều 23 của Luật này.

Điều 20. Phòng cháy đối với nhà ở | Khoản 5
5. Đối với nhà ở tại thành phố trực thuộc Trung ương thuộc khu vực không
bảo đảm hạ tầng giao thông hoặc nguồn nước phục vụ chữa cháy theo quy định
của pháp luật, quy chuẩn kỹ thuật trong hoạt động phòng cháy, chữa cháy thì
phải trang bị bình chữa cháy, thiết bị truyền tin báo cháy kết nối với hệ
thống Cơ sở dữ liệu về phòng cháy, chữa cháy, cứu nạn, cứu hộ và truyền tin
báo cháy theo lộ trình do Chính phủ quy định.
 Đối với nhà ở tại khu vực khác thì khuyến khích trang bị thiết bị truyền
tin báo cháy kết nối với hệ thống Cơ sở dữ liệu về phòng cháy, chữa cháy,
cứu nạn, cứu hộ và truyền tin báo cháy.
 Ủy ban nhân dân thành phố trực thuộc Trung ương xác định khu vực không
bảo đảm hạ tầng giao thông hoặc nguồn nước phục vụ chữa cháy.

Điều 20. Phòng cháy đối với nhà ở | Khoản 6
6. Lực lượng Cảnh sát phòng cháy, chữa cháy và cứu nạn, cứu hộ có trách
nhiệm hướng dẫn việc kết nối thiết bị truyền tin báo cháy với hệ thống Cơ
sở dữ liệu về phòng cháy, chữa cháy, cứu nạn, cứu hộ và truyền tin báo cháy
khi có yêu cầu.
```

**[3] [Luật PCCC 55/2024/QH15 — Word Công báo](https://congbao.chinhphu.vn/van-ban-dang-cong-bao/quoc-hoi-c31/trang-19.htm)**

Điều 24. Phòng cháy trong lắp đặt, sử dụng điện cho sinh hoạt, sản xuất | Khoản 1 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_corpus_v7_20261005/fire55-word.json

```text
1. Trong lắp đặt, sử dụng điện cho sinh hoạt phải bảo đảm các điều kiện
an toàn về phòng cháy sau đây:
 a) Chấp hành quy định về an toàn trong sử dụng điện cho sinh hoạt theo
quy định của pháp luật về điện lực;
 b) Đơn vị bán lẻ điện khi đấu nối điện sinh hoạt phải tư vấn việc lắp
đặt, sử dụng đối với hệ thống, thiết bị điện để bảo đảm an toàn về phòng
cháy;
 c) Việc lắp đặt, sử dụng dây dẫn điện, thiết bị điện trong nhà phải bảo
đảm yêu cầu về an toàn điện theo quy định của pháp luật; thường xuyên kiểm
tra, kịp thời sửa chữa, thay thế dây dẫn điện, thiết bị điện không bảo đảm
an toàn về phòng cháy;
 d) Chỉ được sử dụng thiết bị sạc điện cho xe động cơ điện bảo đảm quy
chuẩn kỹ thuật quốc gia; nơi sạc điện cho xe động cơ điện trong nhà phải có
giải pháp bảo đảm an toàn về phòng cháy; khu vực sạc điện cho xe động cơ
điện tập trung trong nhà còn phải có giải pháp ngăn cháy và trang bị phương
tiện chữa cháy phù hợp, bảo đảm tiêu chuẩn.
```


## Câu 36 · PCCC

Nhà trọ có nhiều phòng cần đáp ứng những yêu cầu an toàn cháy nổ nào?

Trạng thái: Trả lời một phần. Provider: gemini-agent; model: gemini-3.8-flash-high.

faithfulness: 0.8421 | answer_relevancy: 0.9533 | context_utilization: 1.0 | context_recall: 0.5 | context_precision: 1.0

ID nguồn chuẩn: fire55-word.json, fire105-word.json

ID nguồn đã truy xuất: fire55-word.json

Nguồn quy định điều kiện an toàn cháy nổ tùy thuộc vào phân loại nhà trọ là nhà ở thông thường, nhà ở kết hợp kinh doanh hay cơ sở thuộc diện quản lý PCCC [1] [2] [3].

- Nguồn quy định nhà ở thông thường phải bảo đảm an toàn điện, bố trí bếp đun nấu và nơi thờ cúng an toàn, có phương tiện PCCC thực tế và duy trì lối thoát nạn hoặc lối ra khẩn cấp [1].
- Nguồn quy định nhà ở kết hợp sản xuất, kinh doanh phải có biển cấm, biển báo, biển chỉ dẫn và giải pháp ngăn cách hoặc ngăn cháy giữa khu vực kinh doanh có nguy cơ cháy nổ với khu vực để ở [2].
- Nguồn quy định nhà thuộc danh mục cơ sở quản lý PCCC phải có nội quy, phương án chữa cháy, phương tiện hệ thống PCCC, thiết bị truyền tin báo cháy và lực lượng hoặc người làm nhiệm vụ PCCC [1] [3].
- Nguồn quy định nơi sạc điện cho xe động cơ điện trong nhà phải có giải pháp an toàn cháy, và khu vực sạc tập trung phải có giải pháp ngăn cháy cùng phương tiện chữa cháy phù hợp [1].

Nguồn chưa nêu quy định chi tiết riêng theo số lượng phòng mà phân loại điều kiện an toàn theo loại hình sử dụng, quy chuẩn kỹ thuật và danh mục quản lý cơ sở [1] [3].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng.
Cần xác định loại hình sử dụng, số tầng, diện tích và quy chuẩn của nhà trọ để chọn đúng nhóm điều kiện; chưa kết luận chỉ từ số phòng.
Cần đối chiếu điều/khoản được dẫn chiếu còn thiếu; đoạn trích chưa đủ để kết luận toàn bộ điều kiện và ngoại lệ.

### Nguồn và ngữ cảnh

**[1] [Luật PCCC 55/2024/QH15 — Word Công báo](https://congbao.chinhphu.vn/van-ban-dang-cong-bao/quoc-hoi-c31/trang-19.htm)**

Điều 20. Phòng cháy đối với nhà ở · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_corpus_v7_20261005/fire55-word.json

```text
1. Nhà ở không thuộc loại hình quy định tại khoản 3 và khoản 4 Điều này
phải bảo đảm các điều kiện an toàn về phòng cháy sau đây:
 a) Lắp đặt, sử dụng thiết bị điện bảo đảm điều kiện an toàn về phòng
cháy quy định tại điểm c khoản 1 Điều 24 của Luật này;
 b) Bố trí bếp đun nấu, nơi thờ cúng, đốt vàng mã bảo đảm an toàn; không
để vật, chất dễ cháy, nổ gần nguồn lửa, nguồn nhiệt.

2. Nhà ở không thuộc loại hình quy định tại khoản 3 và khoản 4 Điều này
phải bảo đảm các điều kiện về chữa cháy, thoát nạn sau đây:
 a) Có phương tiện phòng cháy, chữa cháy phù hợp với khả năng, điều kiện
thực tế để sẵn sàng chữa cháy, thoát nạn;
 b) Bố trí, duy trì lối thoát nạn, lối ra khẩn cấp hoặc lối đi bảo đảm
việc thoát nạn.

3. Nhà ở có quy chuẩn kỹ thuật, tiêu chuẩn được viện dẫn trong văn bản
quy phạm pháp luật hoặc trong quy chuẩn kỹ thuật về phòng cháy, chữa cháy
và cứu nạn, cứu hộ thực hiện theo tiêu chuẩn, quy chuẩn kỹ thuật đó.

4. Nhà ở trong danh mục cơ sở thuộc diện quản lý về phòng cháy và chữa
cháy thực hiện theo quy định tại Điều 23 của Luật này.

5. Đối với nhà ở tại thành phố trực thuộc Trung ương thuộc khu vực không
bảo đảm hạ tầng giao thông hoặc nguồn nước phục vụ chữa cháy theo quy định
của pháp luật, quy chuẩn kỹ thuật trong hoạt động phòng cháy, chữa cháy thì
phải trang bị bình chữa cháy, thiết bị truyền tin báo cháy kết nối với hệ
thống Cơ sở dữ liệu về phòng cháy, chữa cháy, cứu nạn, cứu hộ và truyền tin
báo cháy theo lộ trình do Chính phủ quy định.
 Đối với nhà ở tại khu vực khác thì khuyến khích trang bị thiết bị truyền
tin báo cháy kết nối với hệ thống Cơ sở dữ liệu về phòng cháy, chữa cháy,
cứu nạn, cứu hộ và truyền tin báo cháy.
 Ủy ban nhân dân thành phố trực thuộc Trung ương xác định khu vực không
bảo đảm hạ tầng giao thông hoặc nguồn nước phục vụ chữa cháy.

6. Lực lượng Cảnh sát phòng cháy, chữa cháy và cứu nạn, cứu hộ có trách
nhiệm hướng dẫn việc kết nối thiết bị truyền tin báo cháy với hệ thống Cơ
sở dữ liệu về phòng cháy, chữa cháy, cứu nạn, cứu hộ và truyền tin báo cháy
khi có yêu cầu.

Điều 24. Phòng cháy trong lắp đặt, sử dụng điện cho sinh hoạt, sản xuất | Khoản 1
1. Trong lắp đặt, sử dụng điện cho sinh hoạt phải bảo đảm các điều kiện
an toàn về phòng cháy sau đây:
 a) Chấp hành quy định về an toàn trong sử dụng điện cho sinh hoạt theo
quy định của pháp luật về điện lực;
 b) Đơn vị bán lẻ điện khi đấu nối điện sinh hoạt phải tư vấn việc lắp
đặt, sử dụng đối với hệ thống, thiết bị điện để bảo đảm an toàn về phòng
cháy;
 c) Việc lắp đặt, sử dụng dây dẫn điện, thiết bị điện trong nhà phải bảo
đảm yêu cầu về an toàn điện theo quy định của pháp luật; thường xuyên kiểm
tra, kịp thời sửa chữa, thay thế dây dẫn điện, thiết bị điện không bảo đảm
an toàn về phòng cháy;
 d) Chỉ được sử dụng thiết bị sạc điện cho xe động cơ điện bảo đảm quy
chuẩn kỹ thuật quốc gia; nơi sạc điện cho xe động cơ điện trong nhà phải có
giải pháp bảo đảm an toàn về phòng cháy; khu vực sạc điện cho xe động cơ
điện tập trung trong nhà còn phải có giải pháp ngăn cháy và trang bị phương
tiện chữa cháy phù hợp, bảo đảm tiêu chuẩn.

Điều 23. Phòng cháy đối với cơ sở | Khoản 1
1. Cơ sở phải bảo đảm các điều kiện an toàn về phòng cháy sau đây:
 a) Có nội quy phòng cháy, chữa cháy, cứu nạn, cứu hộ phù hợp với từng
loại hình cơ sở;
 b) Trang bị phương tiện, hệ thống phòng cháy, chữa cháy, cứu nạn, cứu hộ
theo quy định của pháp luật;
 c) Trang bị thiết bị truyền tin báo cháy kết nối với hệ thống Cơ sở dữ
liệu về phòng cháy, chữa cháy, cứu nạn, cứu hộ và truyền tin báo cháy; khai
báo, cập nhật dữ liệu về phòng cháy, chữa cháy, cứu nạn, cứu hộ theo lộ
trình do Chính phủ quy định;
 d) Thực hiện các yêu cầu về phòng cháy và chữa cháy quy định tại các
điểm a, b, c, d, đ và e khoản 1 Điều 16 của Luật này;
 đ) Có phương án chữa cháy, cứu nạn, cứu hộ;
 e) Thành lập lực lượng phòng cháy, chữa cháy và cứu nạn, cứu hộ cơ sở
hoặc lực lượng phòng cháy, chữa cháy và cứu nạn, cứu hộ chuyên ngành theo
quy định tại Điều 37 của Luật này hoặc phân công người thực hiện nhiệm vụ
phòng cháy, chữa cháy, cứu nạn, cứu hộ.

Điều 23. Phòng cháy đối với cơ sở | Khoản 2
2. Cơ quan, tổ chức hoạt động trong phạm vi một cơ sở phải bảo đảm các
điều kiện an toàn về phòng cháy sau đây:
 a) Có nội quy phòng cháy, chữa cháy, cứu nạn, cứu hộ phù hợp với tính
chất hoạt động của cơ quan, tổ chức;
 b) Bảo đảm an toàn trong sử dụng nguồn lửa, nguồn nhiệt, thiết bị, dụng
cụ sinh lửa, sinh nhiệt, chất dễ cháy, nổ trong phạm vi quản lý;
 c) Cử người tham gia lực lượng phòng cháy, chữa cháy và cứu nạn, cứu hộ
cơ sở hoặc lực lượng phòng cháy, chữa cháy và cứu nạn, cứu hộ chuyên ngành
theo quy định của pháp luật;
 d) Thực hiện, duy trì điều kiện an toàn về phòng cháy và chữa cháy trong
phạm vi quản lý.
```

**[2] [Luật PCCC 55/2024/QH15 — Word Công báo](https://congbao.chinhphu.vn/van-ban-dang-cong-bao/quoc-hoi-c31/trang-19.htm)**

Điều 21. Phòng cháy đối với nhà ở kết hợp sản xuất, kinh doanh · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_corpus_v7_20261005/fire55-word.json

```text
1. Nhà ở kết hợp sản xuất, kinh doanh phải bảo đảm các điều kiện an toàn
về phòng cháy sau đây:
 a) Các điều kiện an toàn về phòng cháy quy định tại Điều 20 của Luật
này;
 b) Có biển cấm, biển báo, biển chỉ dẫn theo quy định;
 c) Khu vực sản xuất, kinh doanh hàng hóa có nguy cơ cháy, nổ phải có
giải pháp ngăn cách hoặc ngăn cháy với khu vực để ở.

2. Nhà ở kết hợp sản xuất, kinh doanh hàng hóa nguy hiểm về cháy, nổ
phải bảo đảm các điều kiện an toàn về phòng cháy sau đây:
 a) Các điều kiện an toàn về phòng cháy quy định tại khoản 1 Điều này;
 b) Không bố trí chỗ ngủ trong khu vực sản xuất, kinh doanh;
 c) Có phương tiện báo cháy, giải pháp thông gió, thiết bị phát hiện sự
cố rò rỉ chất khí nguy hiểm về cháy, nổ phù hợp với công năng, đặc điểm của
nhà ở kết hợp sản xuất, kinh doanh hàng hóa nguy hiểm về cháy, nổ;
 d) Khu vực sản xuất, kinh doanh hàng hóa nguy hiểm về cháy, nổ phải được
ngăn cháy với lối thoát nạn của khu vực để ở.

Điều 20. Phòng cháy đối với nhà ở | Khoản 1
1. Nhà ở không thuộc loại hình quy định tại khoản 3 và khoản 4 Điều này
phải bảo đảm các điều kiện an toàn về phòng cháy sau đây:
 a) Lắp đặt, sử dụng thiết bị điện bảo đảm điều kiện an toàn về phòng
cháy quy định tại điểm c khoản 1 Điều 24 của Luật này;
 b) Bố trí bếp đun nấu, nơi thờ cúng, đốt vàng mã bảo đảm an toàn; không
để vật, chất dễ cháy, nổ gần nguồn lửa, nguồn nhiệt.

Điều 20. Phòng cháy đối với nhà ở | Khoản 2
2. Nhà ở không thuộc loại hình quy định tại khoản 3 và khoản 4 Điều này
phải bảo đảm các điều kiện về chữa cháy, thoát nạn sau đây:
 a) Có phương tiện phòng cháy, chữa cháy phù hợp với khả năng, điều kiện
thực tế để sẵn sàng chữa cháy, thoát nạn;
 b) Bố trí, duy trì lối thoát nạn, lối ra khẩn cấp hoặc lối đi bảo đảm
việc thoát nạn.

Điều 20. Phòng cháy đối với nhà ở | Khoản 3
3. Nhà ở có quy chuẩn kỹ thuật, tiêu chuẩn được viện dẫn trong văn bản
quy phạm pháp luật hoặc trong quy chuẩn kỹ thuật về phòng cháy, chữa cháy
và cứu nạn, cứu hộ thực hiện theo tiêu chuẩn, quy chuẩn kỹ thuật đó.

Điều 20. Phòng cháy đối với nhà ở | Khoản 4
4. Nhà ở trong danh mục cơ sở thuộc diện quản lý về phòng cháy và chữa
cháy thực hiện theo quy định tại Điều 23 của Luật này.

Điều 20. Phòng cháy đối với nhà ở | Khoản 5
5. Đối với nhà ở tại thành phố trực thuộc Trung ương thuộc khu vực không
bảo đảm hạ tầng giao thông hoặc nguồn nước phục vụ chữa cháy theo quy định
của pháp luật, quy chuẩn kỹ thuật trong hoạt động phòng cháy, chữa cháy thì
phải trang bị bình chữa cháy, thiết bị truyền tin báo cháy kết nối với hệ
thống Cơ sở dữ liệu về phòng cháy, chữa cháy, cứu nạn, cứu hộ và truyền tin
báo cháy theo lộ trình do Chính phủ quy định.
 Đối với nhà ở tại khu vực khác thì khuyến khích trang bị thiết bị truyền
tin báo cháy kết nối với hệ thống Cơ sở dữ liệu về phòng cháy, chữa cháy,
cứu nạn, cứu hộ và truyền tin báo cháy.
 Ủy ban nhân dân thành phố trực thuộc Trung ương xác định khu vực không
bảo đảm hạ tầng giao thông hoặc nguồn nước phục vụ chữa cháy.

Điều 20. Phòng cháy đối với nhà ở | Khoản 6
6. Lực lượng Cảnh sát phòng cháy, chữa cháy và cứu nạn, cứu hộ có trách
nhiệm hướng dẫn việc kết nối thiết bị truyền tin báo cháy với hệ thống Cơ
sở dữ liệu về phòng cháy, chữa cháy, cứu nạn, cứu hộ và truyền tin báo cháy
khi có yêu cầu.
```

**[3] [Luật PCCC 55/2024/QH15 — Word Công báo](https://congbao.chinhphu.vn/van-ban-dang-cong-bao/quoc-hoi-c31/trang-19.htm)**

Điều 23. Phòng cháy đối với cơ sở · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_corpus_v7_20261005/fire55-word.json

```text
1. Cơ sở phải bảo đảm các điều kiện an toàn về phòng cháy sau đây:
 a) Có nội quy phòng cháy, chữa cháy, cứu nạn, cứu hộ phù hợp với từng
loại hình cơ sở;
 b) Trang bị phương tiện, hệ thống phòng cháy, chữa cháy, cứu nạn, cứu hộ
theo quy định của pháp luật;
 c) Trang bị thiết bị truyền tin báo cháy kết nối với hệ thống Cơ sở dữ
liệu về phòng cháy, chữa cháy, cứu nạn, cứu hộ và truyền tin báo cháy; khai
báo, cập nhật dữ liệu về phòng cháy, chữa cháy, cứu nạn, cứu hộ theo lộ
trình do Chính phủ quy định;
 d) Thực hiện các yêu cầu về phòng cháy và chữa cháy quy định tại các
điểm a, b, c, d, đ và e khoản 1 Điều 16 của Luật này;
 đ) Có phương án chữa cháy, cứu nạn, cứu hộ;
 e) Thành lập lực lượng phòng cháy, chữa cháy và cứu nạn, cứu hộ cơ sở
hoặc lực lượng phòng cháy, chữa cháy và cứu nạn, cứu hộ chuyên ngành theo
quy định tại Điều 37 của Luật này hoặc phân công người thực hiện nhiệm vụ
phòng cháy, chữa cháy, cứu nạn, cứu hộ.

2. Cơ quan, tổ chức hoạt động trong phạm vi một cơ sở phải bảo đảm các
điều kiện an toàn về phòng cháy sau đây:
 a) Có nội quy phòng cháy, chữa cháy, cứu nạn, cứu hộ phù hợp với tính
chất hoạt động của cơ quan, tổ chức;
 b) Bảo đảm an toàn trong sử dụng nguồn lửa, nguồn nhiệt, thiết bị, dụng
cụ sinh lửa, sinh nhiệt, chất dễ cháy, nổ trong phạm vi quản lý;
 c) Cử người tham gia lực lượng phòng cháy, chữa cháy và cứu nạn, cứu hộ
cơ sở hoặc lực lượng phòng cháy, chữa cháy và cứu nạn, cứu hộ chuyên ngành
theo quy định của pháp luật;
 d) Thực hiện, duy trì điều kiện an toàn về phòng cháy và chữa cháy trong
phạm vi quản lý.
```

### Lỗi và giới hạn đã ghi nhận

```json
{
  "collect": null,
  "ragas": {},
  "unavailable": null,
  "degraded": [
    "Phản hồi chưa đáp ứng đầy đủ yêu cầu chính; đánh dấu theo nội dung thay vì provider."
  ]
}
```


## Câu 37 · PCCC

Nếu lối thoát nạn bị khóa hoặc bị chặn, người thuê nên làm gì?

Trạng thái: Đã trả lời · cần rà nguồn. Provider: gemini-agent; model: gemini-3.8-flash-high.

faithfulness: 0.8261 | answer_relevancy: 0.8873 | context_utilization: 1.0 | context_recall: 1.0 | context_precision: 0.6667

ID nguồn chuẩn: fire55-word.json, fire-emergency114-word.json

ID nguồn đã truy xuất: fire-emergency114-word.json, supplement-s14-word.json, fire55-word.json

Trước khi xảy ra cháy, người thuê cần tự dọn dẹp và yêu cầu chủ trọ bảo đảm lối thoát nạn luôn thông thoáng, còn khi có cháy và bị kẹt thì áp dụng biện pháp phòng khói và báo cứu nạn [2] [3].

- Khuyến nghị người thuê không để đồ đạc lấn chiếm hành lang, cầu thang, lối đi chung và đề nghị chủ trọ duy trì cửa thoát hiểm, lối thoát luôn thông thoáng, không bố trí kho chứa hay bãi xe cản trở [2].
- Nguồn quy định nhà ở phải bố trí, duy trì lối thoát nạn, lối ra khẩn cấp hoặc lối đi bảo đảm việc thoát nạn [4].
- Trường hợp xảy ra cháy mà bị kẹt trong phòng không thể thoát ra, khuyến nghị đóng kín cửa và dùng khăn hoặc chăn ướt bịt kín khe cửa, khe thông gió để ngăn khói, lửa [3].
- Khuyến nghị gọi ngay lực lượng Cảnh sát PCCC và CNCH theo số 114, di chuyển ra ban công hoặc cửa sổ ra tín hiệu cầu cứu chờ hỗ trợ và tuyệt đối không nhảy từ trên cao xuống [1] [3].

Nguồn chỉ nêu số 114 để gọi lực lượng Cảnh sát PCCC và CNCH khi có sự cố, không nêu số này tiếp nhận phản ánh tranh chấp thuê trọ thông thường [1].

Hướng dẫn/khuyến cáo của Công an tỉnh Phú Thọ Phòng Cảnh sát PCCC và CNCH; không phải điều luật. Dùng phần phòng ngừa và nhận biết lối thoát, không tự suy ra định mức thiết bị pháp lý cho từng quy mô nhà. Không chuyển các cách chữa cháy bằng nước thành lời khuyên chung cho cháy điện.
Khuyến cáo khi phát hiện cháy; gọi 114 trong tình huống cháy/khẩn cấp, không trình bày là số tiếp nhận mọi tranh chấp thuê trọ.

### Nguồn và ngữ cảnh

**[1] [Báo cháy 114 — Công an tỉnh Phú Thọ](https://congan.phutho.gov.vn/article/Tang-cuong-bao-dam-an-toan-phong-chay-chua-chay-27208-57)**

Báo cháy 114 — Công an tỉnh Phú Thọ · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_priority7_corpus_v13_20261006/fire-emergency114-word.json

```text
đồng thời gọi ngay lực lượng Cảnh sát PCCC và CNCH theo số 114.
```

**[2] [Tăng cường bảo đảm an toàn PCCC và kỹ năng thoát nạn tại các khu chung cư nhà trọ — Công an tỉnh Phú Thọ Phòng Cảnh sát PCCC và CNCH](https://congan.phutho.gov.vn/article/Tang-cuong-bao-dam-an-toan-phong-chay-chua-chay-27208-57)**

Tăng cường bảo đảm an toàn PCCC và kỹ năng thoát nạn tại các khu chung cư nhà trọ | Đoạn nguyên văn 2 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_supplement_corpus_v8_20261005/supplement-s14-word.json

```text
Nguy cơ cháy, nổ từ thói quen sinh hoạt thiếu an toàn

Các vụ cháy tại chung cư, nhà trọ thường bắt nguồn từ những nguyên nhân quen thuộc nhưng dễ bị bỏ qua như: hệ thống điện quá tải, chập cháy; sử dụng bếp gas, bếp điện, thiết bị đun nấu không đảm bảo an toàn; sạc điện thoại, xe đạp điện, xe máy điện qua đêm; bất cẩn khi hút thuốc, đốt vàng mã; che chắn, khóa cửa thoát hiểm hoặc tự ý thay đổi công năng, cơi nới làm tăng tải đường dây điện.

Đặc biệt, tại nhiều khu chung cư, nhà trọ việc lắp đặt và câu mắc điện không đúng kỹ thuật, không được kiểm tra, bảo dưỡng định kỳ càng làm gia tăng nguy cơ cháy, nổ.

Những việc người dân cần thực hiện để phòng cháy, nổ

Người dân sinh sống tại chung cư, nhà trọ cần nghiêm túc thực hiện các nội dung sau:

- Thường xuyên kiểm tra, bảo dưỡng hệ thống điện trong nhà, kịp thời thay thế dây dẫn, ổ cắm, aptomat bị hư hỏng.

- Ngắt nguồn điện, khóa van gas, tắt các thiết bị đun nấu và thiết bị điện không cần thiết trước khi ra khỏi nhà hoặc trước khi đi ngủ.

- Hạn chế sạc các thiết bị điện (điện thoại, máy tính, xe đạp điện, xe máy điện…) qua đêm khi không có người trông coi.

- Sắp xếp đồ đạc gọn gàng, không để vật dụng dễ cháy gần nguồn nhiệt, không lấn chiếm hành lang, cầu thang, lối đi chung.

Trách nhiệm của chủ nhà trọ, ban quản lý chung cư

- Lắp đặt và duy trì hoạt động thường xuyên hệ thống báo cháy, chữa cháy, hệ thống cấp nước chữa cháy theo đúng quy định.

- Đảm bảo lối thoát nạn, cầu thang bộ, ban công, cửa thoát hiểm luôn thông thoáng, không bố trí kho chứa đồ, bãi xe hoặc hàng hóa cản trở việc thoát nạn.

- Trang bị đầy đủ phương tiện phòng cháy, chữa cháy theo quy định; bố trí bảng nội quy, biển cấm, biển báo, sơ đồ thoát nạn ở vị trí dễ quan sát.

- Thường xuyên phối hợp với cơ quan chức năng tổ chức tuyên truyền, phổ biến kiến thức PCCC và kỹ năng thoát nạn cho người dân sinh sống, làm việc tại cơ sở.

Trong quá trình thoát nạn cần lưu ý:

- Cúi thấp người, di chuyển sát mặt sàn để giảm hít phải khói, khí độc.

- Dùng khăn, vải ẩm che kín mũi, miệng, hạn chế tối đa việc hít khói.

- Giữ bình tĩnh, không chen lấn, xô đẩy gây hỗn loạn tại khu vực cầu thang, cửa ra vào.
```

**[3] [Tăng cường bảo đảm an toàn PCCC và kỹ năng thoát nạn tại các khu chung cư nhà trọ — Công an tỉnh Phú Thọ Phòng Cảnh sát PCCC và CNCH](https://congan.phutho.gov.vn/article/Tang-cuong-bao-dam-an-toan-phong-chay-chua-chay-27208-57)**

Tăng cường bảo đảm an toàn PCCC và kỹ năng thoát nạn tại các khu chung cư nhà trọ | Đoạn nguyên văn 22 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_supplement_corpus_v8_20261005/supplement-s14-word.json

```text
- Ưu tiên thoát nạn theo cầu thang bộ, không sử dụng thang máy khi đang xảy ra cháy.

Trường hợp bị kẹt trong phòng, không thể thoát ra ngoài qua lối đi thông thường, cần:

- Đóng kín cửa, dùng khăn, chăn ướt bịt kín các khe cửa, khe thông gió để ngăn khói, lửa lan vào.

- Di chuyển ra ban công hoặc cửa sổ, sử dụng đèn pin, khăn, quần áo màu sáng… để ra tín hiệu cầu cứu, chờ lực lượng chức năng đến hỗ trợ.

- Tuyệt đối không nhảy từ trên cao xuống để tránh nguy hiểm đến tính mạng.
```

**[4] [Luật PCCC 55/2024/QH15 — Word Công báo](https://congbao.chinhphu.vn/van-ban-dang-cong-bao/quoc-hoi-c31/trang-19.htm)**

Điều 20. Phòng cháy đối với nhà ở · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_corpus_v7_20261005/fire55-word.json

```text
1. Nhà ở không thuộc loại hình quy định tại khoản 3 và khoản 4 Điều này
phải bảo đảm các điều kiện an toàn về phòng cháy sau đây:
 a) Lắp đặt, sử dụng thiết bị điện bảo đảm điều kiện an toàn về phòng
cháy quy định tại điểm c khoản 1 Điều 24 của Luật này;
 b) Bố trí bếp đun nấu, nơi thờ cúng, đốt vàng mã bảo đảm an toàn; không
để vật, chất dễ cháy, nổ gần nguồn lửa, nguồn nhiệt.

2. Nhà ở không thuộc loại hình quy định tại khoản 3 và khoản 4 Điều này
phải bảo đảm các điều kiện về chữa cháy, thoát nạn sau đây:
 a) Có phương tiện phòng cháy, chữa cháy phù hợp với khả năng, điều kiện
thực tế để sẵn sàng chữa cháy, thoát nạn;
 b) Bố trí, duy trì lối thoát nạn, lối ra khẩn cấp hoặc lối đi bảo đảm
việc thoát nạn.

3. Nhà ở có quy chuẩn kỹ thuật, tiêu chuẩn được viện dẫn trong văn bản
quy phạm pháp luật hoặc trong quy chuẩn kỹ thuật về phòng cháy, chữa cháy
và cứu nạn, cứu hộ thực hiện theo tiêu chuẩn, quy chuẩn kỹ thuật đó.

4. Nhà ở trong danh mục cơ sở thuộc diện quản lý về phòng cháy và chữa
cháy thực hiện theo quy định tại Điều 23 của Luật này.

5. Đối với nhà ở tại thành phố trực thuộc Trung ương thuộc khu vực không
bảo đảm hạ tầng giao thông hoặc nguồn nước phục vụ chữa cháy theo quy định
của pháp luật, quy chuẩn kỹ thuật trong hoạt động phòng cháy, chữa cháy thì
phải trang bị bình chữa cháy, thiết bị truyền tin báo cháy kết nối với hệ
thống Cơ sở dữ liệu về phòng cháy, chữa cháy, cứu nạn, cứu hộ và truyền tin
báo cháy theo lộ trình do Chính phủ quy định.
 Đối với nhà ở tại khu vực khác thì khuyến khích trang bị thiết bị truyền
tin báo cháy kết nối với hệ thống Cơ sở dữ liệu về phòng cháy, chữa cháy,
cứu nạn, cứu hộ và truyền tin báo cháy.
 Ủy ban nhân dân thành phố trực thuộc Trung ương xác định khu vực không
bảo đảm hạ tầng giao thông hoặc nguồn nước phục vụ chữa cháy.

6. Lực lượng Cảnh sát phòng cháy, chữa cháy và cứu nạn, cứu hộ có trách
nhiệm hướng dẫn việc kết nối thiết bị truyền tin báo cháy với hệ thống Cơ
sở dữ liệu về phòng cháy, chữa cháy, cứu nạn, cứu hộ và truyền tin báo cháy
khi có yêu cầu.

Điều 24. Phòng cháy trong lắp đặt, sử dụng điện cho sinh hoạt, sản xuất | Khoản 1
1. Trong lắp đặt, sử dụng điện cho sinh hoạt phải bảo đảm các điều kiện
an toàn về phòng cháy sau đây:
 a) Chấp hành quy định về an toàn trong sử dụng điện cho sinh hoạt theo
quy định của pháp luật về điện lực;
 b) Đơn vị bán lẻ điện khi đấu nối điện sinh hoạt phải tư vấn việc lắp
đặt, sử dụng đối với hệ thống, thiết bị điện để bảo đảm an toàn về phòng
cháy;
 c) Việc lắp đặt, sử dụng dây dẫn điện, thiết bị điện trong nhà phải bảo
đảm yêu cầu về an toàn điện theo quy định của pháp luật; thường xuyên kiểm
tra, kịp thời sửa chữa, thay thế dây dẫn điện, thiết bị điện không bảo đảm
an toàn về phòng cháy;
 d) Chỉ được sử dụng thiết bị sạc điện cho xe động cơ điện bảo đảm quy
chuẩn kỹ thuật quốc gia; nơi sạc điện cho xe động cơ điện trong nhà phải có
giải pháp bảo đảm an toàn về phòng cháy; khu vực sạc điện cho xe động cơ
điện tập trung trong nhà còn phải có giải pháp ngăn cháy và trang bị phương
tiện chữa cháy phù hợp, bảo đảm tiêu chuẩn.

Điều 23. Phòng cháy đối với cơ sở | Khoản 1
1. Cơ sở phải bảo đảm các điều kiện an toàn về phòng cháy sau đây:
 a) Có nội quy phòng cháy, chữa cháy, cứu nạn, cứu hộ phù hợp với từng
loại hình cơ sở;
 b) Trang bị phương tiện, hệ thống phòng cháy, chữa cháy, cứu nạn, cứu hộ
theo quy định của pháp luật;
 c) Trang bị thiết bị truyền tin báo cháy kết nối với hệ thống Cơ sở dữ
liệu về phòng cháy, chữa cháy, cứu nạn, cứu hộ và truyền tin báo cháy; khai
báo, cập nhật dữ liệu về phòng cháy, chữa cháy, cứu nạn, cứu hộ theo lộ
trình do Chính phủ quy định;
 d) Thực hiện các yêu cầu về phòng cháy và chữa cháy quy định tại các
điểm a, b, c, d, đ và e khoản 1 Điều 16 của Luật này;
 đ) Có phương án chữa cháy, cứu nạn, cứu hộ;
 e) Thành lập lực lượng phòng cháy, chữa cháy và cứu nạn, cứu hộ cơ sở
hoặc lực lượng phòng cháy, chữa cháy và cứu nạn, cứu hộ chuyên ngành theo
quy định tại Điều 37 của Luật này hoặc phân công người thực hiện nhiệm vụ
phòng cháy, chữa cháy, cứu nạn, cứu hộ.

Điều 23. Phòng cháy đối với cơ sở | Khoản 2
2. Cơ quan, tổ chức hoạt động trong phạm vi một cơ sở phải bảo đảm các
điều kiện an toàn về phòng cháy sau đây:
 a) Có nội quy phòng cháy, chữa cháy, cứu nạn, cứu hộ phù hợp với tính
chất hoạt động của cơ quan, tổ chức;
 b) Bảo đảm an toàn trong sử dụng nguồn lửa, nguồn nhiệt, thiết bị, dụng
cụ sinh lửa, sinh nhiệt, chất dễ cháy, nổ trong phạm vi quản lý;
 c) Cử người tham gia lực lượng phòng cháy, chữa cháy và cứu nạn, cứu hộ
cơ sở hoặc lực lượng phòng cháy, chữa cháy và cứu nạn, cứu hộ chuyên ngành
theo quy định của pháp luật;
 d) Thực hiện, duy trì điều kiện an toàn về phòng cháy và chữa cháy trong
phạm vi quản lý.
```


## Câu 38 · PCCC

Chủ trọ và người thuê có trách nhiệm gì đối với thiết bị điện và an toàn cháy nổ?

Trạng thái: Đã trả lời · cần rà nguồn. Provider: gemini-agent; model: gemini-3.8-flash-high.

faithfulness: 1.0 | answer_relevancy: 0.9091 | context_utilization: 1.0 | context_recall: 0.5 | context_precision: 0.5

ID nguồn chuẩn: fire55-word.json, electricity61-word.json

ID nguồn đã truy xuất: fire55-word.json, supplement-s14-word.json

Người cho thuê có trách nhiệm tuyên truyền, đôn đốc người thuê thực hiện quy định phòng cháy, chữa cháy; người thuê có trách nhiệm như chủ hộ gia đình trực tiếp sử dụng nhà ở trừ trường hợp có thỏa thuận khác [1] [2].

- Người cho thuê, cho mượn nhà ở có trách nhiệm tuyên truyền, đôn đốc, nhắc nhở người thuê thực hiện quy định pháp luật về phòng cháy, chữa cháy và cứu nạn, cứu hộ [1].
- Người thuê nhà ở có trách nhiệm thực hiện quy định về phòng cháy đối với nhà ở và thường xuyên tự kiểm tra, khắc phục nguy cơ cháy nổ, trừ trường hợp có thỏa thuận khác [1] [2].
- Nguồn quy định nhà ở phải lắp đặt, sử dụng thiết bị điện bảo đảm điều kiện an toàn về phòng cháy, bố trí bếp đun nấu an toàn và không để chất dễ cháy gần nguồn lửa, nguồn nhiệt [1] [2].
- Khuyến nghị người dân thường xuyên kiểm tra hệ thống điện, ngắt thiết bị điện không cần thiết khi ra khỏi nhà hoặc đi ngủ và hạn chế sạc thiết bị điện qua đêm không người trông coi [3].

Tài liệu từ Công an tỉnh Phú Thọ mang tính hướng dẫn, khuyến cáo an toàn PCCC, không phải quy định pháp luật bắt buộc về thiết bị điện cho từng quy mô nhà [3].

Hướng dẫn/khuyến cáo của Công an tỉnh Phú Thọ Phòng Cảnh sát PCCC và CNCH; không phải điều luật. Dùng phần phòng ngừa và nhận biết lối thoát, không tự suy ra định mức thiết bị pháp lý cho từng quy mô nhà. Không chuyển các cách chữa cháy bằng nước thành lời khuyên chung cho cháy điện.

### Nguồn và ngữ cảnh

**[1] [Luật PCCC 55/2024/QH15 — Word Công báo](https://congbao.chinhphu.vn/van-ban-dang-cong-bao/quoc-hoi-c31/trang-19.htm)**

Điều 8. Trách nhiệm của cơ quan, tổ chức, hộ gia đình, cá nhân trong | Khoản 8 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_corpus_v7_20261005/fire55-word.json

```text
hoạt động phòng cháy, chữa cháy, cứu nạn, cứu hộ

8. Trách nhiệm về phòng cháy, chữa cháy, cứu nạn, cứu hộ đối với trường
hợp thuê, mượn, ở nhờ nhà ở được quy định như sau:
 a) Người cho thuê, cho mượn, cho ở nhờ nhà ở có trách nhiệm tuyên
truyền, đôn đốc, nhắc nhở người thuê, mượn, ở nhờ thực hiện quy định của
pháp luật về phòng cháy, chữa cháy và cứu nạn, cứu hộ;
 b) Người thuê, mượn, ở nhờ nhà ở có trách nhiệm theo quy định tại khoản
6 Điều này, trừ trường hợp có thỏa thuận khác với người cho thuê, mượn, ở
nhờ nhà ở.
 Trường hợp thuê, mượn, ở nhờ nhà ở kết hợp sản xuất, kinh doanh thì
người thuê, mượn, ở nhờ còn có trách nhiệm bảo đảm điều kiện an toàn về
phòng cháy theo quy định tại Điều 21 của Luật này.

Điều 21. Phòng cháy đối với nhà ở kết hợp sản xuất, kinh doanh | Khoản 1
1. Nhà ở kết hợp sản xuất, kinh doanh phải bảo đảm các điều kiện an toàn
về phòng cháy sau đây:
 a) Các điều kiện an toàn về phòng cháy quy định tại Điều 20 của Luật
này;
 b) Có biển cấm, biển báo, biển chỉ dẫn theo quy định;
 c) Khu vực sản xuất, kinh doanh hàng hóa có nguy cơ cháy, nổ phải có
giải pháp ngăn cách hoặc ngăn cháy với khu vực để ở.

Điều 21. Phòng cháy đối với nhà ở kết hợp sản xuất, kinh doanh | Khoản 2
2. Nhà ở kết hợp sản xuất, kinh doanh hàng hóa nguy hiểm về cháy, nổ
phải bảo đảm các điều kiện an toàn về phòng cháy sau đây:
 a) Các điều kiện an toàn về phòng cháy quy định tại khoản 1 Điều này;
 b) Không bố trí chỗ ngủ trong khu vực sản xuất, kinh doanh;
 c) Có phương tiện báo cháy, giải pháp thông gió, thiết bị phát hiện sự
cố rò rỉ chất khí nguy hiểm về cháy, nổ phù hợp với công năng, đặc điểm của
nhà ở kết hợp sản xuất, kinh doanh hàng hóa nguy hiểm về cháy, nổ;
 d) Khu vực sản xuất, kinh doanh hàng hóa nguy hiểm về cháy, nổ phải được
ngăn cháy với lối thoát nạn của khu vực để ở.

Điều 20. Phòng cháy đối với nhà ở | Khoản 1
1. Nhà ở không thuộc loại hình quy định tại khoản 3 và khoản 4 Điều này
phải bảo đảm các điều kiện an toàn về phòng cháy sau đây:
 a) Lắp đặt, sử dụng thiết bị điện bảo đảm điều kiện an toàn về phòng
cháy quy định tại điểm c khoản 1 Điều 24 của Luật này;
 b) Bố trí bếp đun nấu, nơi thờ cúng, đốt vàng mã bảo đảm an toàn; không
để vật, chất dễ cháy, nổ gần nguồn lửa, nguồn nhiệt.

Điều 20. Phòng cháy đối với nhà ở | Khoản 2
2. Nhà ở không thuộc loại hình quy định tại khoản 3 và khoản 4 Điều này
phải bảo đảm các điều kiện về chữa cháy, thoát nạn sau đây:
 a) Có phương tiện phòng cháy, chữa cháy phù hợp với khả năng, điều kiện
thực tế để sẵn sàng chữa cháy, thoát nạn;
 b) Bố trí, duy trì lối thoát nạn, lối ra khẩn cấp hoặc lối đi bảo đảm
việc thoát nạn.

Điều 20. Phòng cháy đối với nhà ở | Khoản 3
3. Nhà ở có quy chuẩn kỹ thuật, tiêu chuẩn được viện dẫn trong văn bản
quy phạm pháp luật hoặc trong quy chuẩn kỹ thuật về phòng cháy, chữa cháy
và cứu nạn, cứu hộ thực hiện theo tiêu chuẩn, quy chuẩn kỹ thuật đó.

Điều 20. Phòng cháy đối với nhà ở | Khoản 4
4. Nhà ở trong danh mục cơ sở thuộc diện quản lý về phòng cháy và chữa
cháy thực hiện theo quy định tại Điều 23 của Luật này.

Điều 20. Phòng cháy đối với nhà ở | Khoản 5
5. Đối với nhà ở tại thành phố trực thuộc Trung ương thuộc khu vực không
bảo đảm hạ tầng giao thông hoặc nguồn nước phục vụ chữa cháy theo quy định
của pháp luật, quy chuẩn kỹ thuật trong hoạt động phòng cháy, chữa cháy thì
phải trang bị bình chữa cháy, thiết bị truyền tin báo cháy kết nối với hệ
thống Cơ sở dữ liệu về phòng cháy, chữa cháy, cứu nạn, cứu hộ và truyền tin
báo cháy theo lộ trình do Chính phủ quy định.
 Đối với nhà ở tại khu vực khác thì khuyến khích trang bị thiết bị truyền
tin báo cháy kết nối với hệ thống Cơ sở dữ liệu về phòng cháy, chữa cháy,
cứu nạn, cứu hộ và truyền tin báo cháy.
 Ủy ban nhân dân thành phố trực thuộc Trung ương xác định khu vực không
bảo đảm hạ tầng giao thông hoặc nguồn nước phục vụ chữa cháy.

Điều 20. Phòng cháy đối với nhà ở | Khoản 6
6. Lực lượng Cảnh sát phòng cháy, chữa cháy và cứu nạn, cứu hộ có trách
nhiệm hướng dẫn việc kết nối thiết bị truyền tin báo cháy với hệ thống Cơ
sở dữ liệu về phòng cháy, chữa cháy, cứu nạn, cứu hộ và truyền tin báo cháy
khi có yêu cầu.
```

**[2] [Luật PCCC 55/2024/QH15 — Word Công báo](https://congbao.chinhphu.vn/van-ban-dang-cong-bao/quoc-hoi-c31/trang-19.htm)**

Điều 8. Trách nhiệm của cơ quan, tổ chức, hộ gia đình, cá nhân trong | Khoản 6 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_corpus_v7_20261005/fire55-word.json

```text
hoạt động phòng cháy, chữa cháy, cứu nạn, cứu hộ

6. Chủ hộ gia đình trực tiếp sử dụng nhà ở mà không phải là người đứng
đầu cơ sở có trách nhiệm sau đây:
 a) Thực hiện quy định tại Điều 20 và Điều 21 của Luật này;
 b) Tuyên truyền, đôn đốc, nhắc nhở thành viên khác trong gia đình thực
hiện pháp luật về phòng cháy, chữa cháy và cứu nạn, cứu hộ;
 c) Thường xuyên tự kiểm tra, phát hiện và khắc phục kịp thời nguy cơ gây
cháy, nổ, tai nạn, sự cố;
 d) Thực hiện các nhiệm vụ khác về phòng cháy, chữa cháy, cứu nạn, cứu hộ
theo quy định của pháp luật.

Điều 21. Phòng cháy đối với nhà ở kết hợp sản xuất, kinh doanh | Khoản 1
1. Nhà ở kết hợp sản xuất, kinh doanh phải bảo đảm các điều kiện an toàn
về phòng cháy sau đây:
 a) Các điều kiện an toàn về phòng cháy quy định tại Điều 20 của Luật
này;
 b) Có biển cấm, biển báo, biển chỉ dẫn theo quy định;
 c) Khu vực sản xuất, kinh doanh hàng hóa có nguy cơ cháy, nổ phải có
giải pháp ngăn cách hoặc ngăn cháy với khu vực để ở.

Điều 21. Phòng cháy đối với nhà ở kết hợp sản xuất, kinh doanh | Khoản 2
2. Nhà ở kết hợp sản xuất, kinh doanh hàng hóa nguy hiểm về cháy, nổ
phải bảo đảm các điều kiện an toàn về phòng cháy sau đây:
 a) Các điều kiện an toàn về phòng cháy quy định tại khoản 1 Điều này;
 b) Không bố trí chỗ ngủ trong khu vực sản xuất, kinh doanh;
 c) Có phương tiện báo cháy, giải pháp thông gió, thiết bị phát hiện sự
cố rò rỉ chất khí nguy hiểm về cháy, nổ phù hợp với công năng, đặc điểm của
nhà ở kết hợp sản xuất, kinh doanh hàng hóa nguy hiểm về cháy, nổ;
 d) Khu vực sản xuất, kinh doanh hàng hóa nguy hiểm về cháy, nổ phải được
ngăn cháy với lối thoát nạn của khu vực để ở.

Điều 20. Phòng cháy đối với nhà ở | Khoản 1
1. Nhà ở không thuộc loại hình quy định tại khoản 3 và khoản 4 Điều này
phải bảo đảm các điều kiện an toàn về phòng cháy sau đây:
 a) Lắp đặt, sử dụng thiết bị điện bảo đảm điều kiện an toàn về phòng
cháy quy định tại điểm c khoản 1 Điều 24 của Luật này;
 b) Bố trí bếp đun nấu, nơi thờ cúng, đốt vàng mã bảo đảm an toàn; không
để vật, chất dễ cháy, nổ gần nguồn lửa, nguồn nhiệt.

Điều 20. Phòng cháy đối với nhà ở | Khoản 2
2. Nhà ở không thuộc loại hình quy định tại khoản 3 và khoản 4 Điều này
phải bảo đảm các điều kiện về chữa cháy, thoát nạn sau đây:
 a) Có phương tiện phòng cháy, chữa cháy phù hợp với khả năng, điều kiện
thực tế để sẵn sàng chữa cháy, thoát nạn;
 b) Bố trí, duy trì lối thoát nạn, lối ra khẩn cấp hoặc lối đi bảo đảm
việc thoát nạn.

Điều 20. Phòng cháy đối với nhà ở | Khoản 3
3. Nhà ở có quy chuẩn kỹ thuật, tiêu chuẩn được viện dẫn trong văn bản
quy phạm pháp luật hoặc trong quy chuẩn kỹ thuật về phòng cháy, chữa cháy
và cứu nạn, cứu hộ thực hiện theo tiêu chuẩn, quy chuẩn kỹ thuật đó.

Điều 20. Phòng cháy đối với nhà ở | Khoản 4
4. Nhà ở trong danh mục cơ sở thuộc diện quản lý về phòng cháy và chữa
cháy thực hiện theo quy định tại Điều 23 của Luật này.

Điều 20. Phòng cháy đối với nhà ở | Khoản 5
5. Đối với nhà ở tại thành phố trực thuộc Trung ương thuộc khu vực không
bảo đảm hạ tầng giao thông hoặc nguồn nước phục vụ chữa cháy theo quy định
của pháp luật, quy chuẩn kỹ thuật trong hoạt động phòng cháy, chữa cháy thì
phải trang bị bình chữa cháy, thiết bị truyền tin báo cháy kết nối với hệ
thống Cơ sở dữ liệu về phòng cháy, chữa cháy, cứu nạn, cứu hộ và truyền tin
báo cháy theo lộ trình do Chính phủ quy định.
 Đối với nhà ở tại khu vực khác thì khuyến khích trang bị thiết bị truyền
tin báo cháy kết nối với hệ thống Cơ sở dữ liệu về phòng cháy, chữa cháy,
cứu nạn, cứu hộ và truyền tin báo cháy.
 Ủy ban nhân dân thành phố trực thuộc Trung ương xác định khu vực không
bảo đảm hạ tầng giao thông hoặc nguồn nước phục vụ chữa cháy.

Điều 20. Phòng cháy đối với nhà ở | Khoản 6
6. Lực lượng Cảnh sát phòng cháy, chữa cháy và cứu nạn, cứu hộ có trách
nhiệm hướng dẫn việc kết nối thiết bị truyền tin báo cháy với hệ thống Cơ
sở dữ liệu về phòng cháy, chữa cháy, cứu nạn, cứu hộ và truyền tin báo cháy
khi có yêu cầu.
```

**[3] [Tăng cường bảo đảm an toàn PCCC và kỹ năng thoát nạn tại các khu chung cư nhà trọ — Công an tỉnh Phú Thọ Phòng Cảnh sát PCCC và CNCH](https://congan.phutho.gov.vn/article/Tang-cuong-bao-dam-an-toan-phong-chay-chua-chay-27208-57)**

Tăng cường bảo đảm an toàn PCCC và kỹ năng thoát nạn tại các khu chung cư nhà trọ | Đoạn nguyên văn 2 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_supplement_corpus_v8_20261005/supplement-s14-word.json

```text
Nguy cơ cháy, nổ từ thói quen sinh hoạt thiếu an toàn

Các vụ cháy tại chung cư, nhà trọ thường bắt nguồn từ những nguyên nhân quen thuộc nhưng dễ bị bỏ qua như: hệ thống điện quá tải, chập cháy; sử dụng bếp gas, bếp điện, thiết bị đun nấu không đảm bảo an toàn; sạc điện thoại, xe đạp điện, xe máy điện qua đêm; bất cẩn khi hút thuốc, đốt vàng mã; che chắn, khóa cửa thoát hiểm hoặc tự ý thay đổi công năng, cơi nới làm tăng tải đường dây điện.

Đặc biệt, tại nhiều khu chung cư, nhà trọ việc lắp đặt và câu mắc điện không đúng kỹ thuật, không được kiểm tra, bảo dưỡng định kỳ càng làm gia tăng nguy cơ cháy, nổ.

Những việc người dân cần thực hiện để phòng cháy, nổ

Người dân sinh sống tại chung cư, nhà trọ cần nghiêm túc thực hiện các nội dung sau:

- Thường xuyên kiểm tra, bảo dưỡng hệ thống điện trong nhà, kịp thời thay thế dây dẫn, ổ cắm, aptomat bị hư hỏng.

- Ngắt nguồn điện, khóa van gas, tắt các thiết bị đun nấu và thiết bị điện không cần thiết trước khi ra khỏi nhà hoặc trước khi đi ngủ.

- Hạn chế sạc các thiết bị điện (điện thoại, máy tính, xe đạp điện, xe máy điện…) qua đêm khi không có người trông coi.

- Sắp xếp đồ đạc gọn gàng, không để vật dụng dễ cháy gần nguồn nhiệt, không lấn chiếm hành lang, cầu thang, lối đi chung.

Trách nhiệm của chủ nhà trọ, ban quản lý chung cư

- Lắp đặt và duy trì hoạt động thường xuyên hệ thống báo cháy, chữa cháy, hệ thống cấp nước chữa cháy theo đúng quy định.

- Đảm bảo lối thoát nạn, cầu thang bộ, ban công, cửa thoát hiểm luôn thông thoáng, không bố trí kho chứa đồ, bãi xe hoặc hàng hóa cản trở việc thoát nạn.

- Trang bị đầy đủ phương tiện phòng cháy, chữa cháy theo quy định; bố trí bảng nội quy, biển cấm, biển báo, sơ đồ thoát nạn ở vị trí dễ quan sát.

- Thường xuyên phối hợp với cơ quan chức năng tổ chức tuyên truyền, phổ biến kiến thức PCCC và kỹ năng thoát nạn cho người dân sinh sống, làm việc tại cơ sở.

Trong quá trình thoát nạn cần lưu ý:

- Cúi thấp người, di chuyển sát mặt sàn để giảm hít phải khói, khí độc.

- Dùng khăn, vải ẩm che kín mũi, miệng, hạn chế tối đa việc hít khói.

- Giữ bình tĩnh, không chen lấn, xô đẩy gây hỗn loạn tại khu vực cầu thang, cửa ra vào.
```


## Câu 39 · Ký túc xá

Ký túc xá Đại học Cần Thơ năm học 2026–2027 có thông tin đăng ký nào trong tài liệu?

Trạng thái: Đã trả lời · cần rà nguồn. Provider: structured_ktx; model: —.

faithfulness: 1.0 | answer_relevancy: 0.9386 | context_utilization: 1.0 | context_recall: 1.0 | context_precision: 1.0

ID nguồn chuẩn: https://ssc.ctu.edu.vn/images/upload/thong_bao/072026_tb_dk1_2627.pdf, https://tansinhvien.ctu.edu.vn/sinh-hoat/huong-dan-tan-sinh-vien-dang-ky-o-ky-tuc-xa

ID nguồn đã truy xuất: https://ssc.ctu.edu.vn/images/upload/thong_bao/072026_tb_dk1_2627.pdf, https://tansinhvien.ctu.edu.vn/sinh-hoat/huong-dan-tan-sinh-vien-dang-ky-o-ky-tuc-xa

**KTX · năm học 2026-2027**
- Thời gian HKI 2026–2027: HKI năm học 2026–2027 ở từ 07/09/2026 đến 18/12/2026, tính 3,5 tháng. Các mốc đăng ký/thu phí tập trung tháng 8 trong thông báo đã qua; sinh viên mới có nhu cầu cần liên hệ KTX để xác nhận. [1]
- Tân sinh viên: Tân sinh viên chưa có tài khoản hệ thống có thể điền mẫu nhu cầu ở được liên kết trên trang hướng dẫn chính thức. Sinh viên có tài khoản làm theo hướng dẫn đăng ký KTX qua hệ thống. [2]
- Đăng ký ở: Sinh viên đăng ký mới qua Hệ thống Quản lý KTX bằng tài khoản sinh viên, email ktx@ctu.edu.vn hoặc trực tiếp tại Văn phòng Trung tâm Phục vụ Sinh viên. Có thể ghi nguyện vọng và đăng ký nhóm; ưu tiên nhóm đủ số người bằng sức chứa phòng. Kết quả phụ thuộc sắp xếp chỗ của KTX. [1]
- Chuyển chỗ, trả chỗ và hoàn phí: Sinh viên có thể xin chuyển chỗ theo hướng dẫn và chỗ phù hợp còn trống. Trả chỗ trước hạn không được hoàn phí, ngoại lệ trả trong vòng 7 ngày từ ngày được duyệt chỗ qua hệ thống và có lý do chính đáng. Cần đối chiếu quy định với văn phòng trước khi trả chỗ. [1]

### Nguồn và ngữ cảnh

**[1] [Thông báo 307/TB-CTSV · HKI 2026–2027](https://ssc.ctu.edu.vn/images/upload/thong_bao/072026_tb_dk1_2627.pdf)**

Danh mục KTX · cập nhật 2026-10-12

Đường dẫn nguồn: Danh mục KTX dùng chung

```text
HKI năm học 2026–2027 ở từ 07/09/2026 đến 18/12/2026, tính 3,5 tháng. Các mốc đăng ký/thu phí tập trung tháng 8 trong thông báo đã qua; sinh viên mới có nhu cầu cần liên hệ KTX để xác nhận.

Sinh viên đăng ký mới qua Hệ thống Quản lý KTX bằng tài khoản sinh viên, email ktx@ctu.edu.vn hoặc trực tiếp tại Văn phòng Trung tâm Phục vụ Sinh viên. Có thể ghi nguyện vọng và đăng ký nhóm; ưu tiên nhóm đủ số người bằng sức chứa phòng. Kết quả phụ thuộc sắp xếp chỗ của KTX.

Sinh viên có thể xin chuyển chỗ theo hướng dẫn và chỗ phù hợp còn trống. Trả chỗ trước hạn không được hoàn phí, ngoại lệ trả trong vòng 7 ngày từ ngày được duyệt chỗ qua hệ thống và có lý do chính đáng. Cần đối chiếu quy định với văn phòng trước khi trả chỗ.
```

**[2] [Hướng dẫn tân sinh viên đăng ký KTX · 2026–2027](https://tansinhvien.ctu.edu.vn/sinh-hoat/huong-dan-tan-sinh-vien-dang-ky-o-ky-tuc-xa)**

Danh mục KTX · cập nhật 2026-10-12

Đường dẫn nguồn: Danh mục KTX dùng chung

```text
Tân sinh viên chưa có tài khoản hệ thống có thể điền mẫu nhu cầu ở được liên kết trên trang hướng dẫn chính thức. Sinh viên có tài khoản làm theo hướng dẫn đăng ký KTX qua hệ thống.
```


## Câu 40 · Ký túc xá

Sinh viên cần chuẩn bị gì khi đăng ký ở ký túc xá Đại học Cần Thơ?

Trạng thái: Đã trả lời · cần rà nguồn. Provider: structured_ktx; model: —.

faithfulness: 1.0 | answer_relevancy: 0.9136 | context_utilization: 1.0 | context_recall: 1.0 | context_precision: 1.0

ID nguồn chuẩn: https://ssc.ctu.edu.vn/images/upload/thong_bao/072026_tb_dk1_2627.pdf, https://tansinhvien.ctu.edu.vn/sinh-hoat/huong-dan-tan-sinh-vien-dang-ky-o-ky-tuc-xa

ID nguồn đã truy xuất: https://ssc.ctu.edu.vn/images/upload/thong_bao/072026_tb_dk1_2627.pdf, https://tansinhvien.ctu.edu.vn/sinh-hoat/huong-dan-tan-sinh-vien-dang-ky-o-ky-tuc-xa

**KTX · năm học 2026-2027**
- Đăng ký ở: Sinh viên đăng ký mới qua Hệ thống Quản lý KTX bằng tài khoản sinh viên, email ktx@ctu.edu.vn hoặc trực tiếp tại Văn phòng Trung tâm Phục vụ Sinh viên. Có thể ghi nguyện vọng và đăng ký nhóm; ưu tiên nhóm đủ số người bằng sức chứa phòng. Kết quả phụ thuộc sắp xếp chỗ của KTX. [1]
- Tân sinh viên: Tân sinh viên chưa có tài khoản hệ thống có thể điền mẫu nhu cầu ở được liên kết trên trang hướng dẫn chính thức. Sinh viên có tài khoản làm theo hướng dẫn đăng ký KTX qua hệ thống. [2]
- Thời gian HKI 2026–2027: HKI năm học 2026–2027 ở từ 07/09/2026 đến 18/12/2026, tính 3,5 tháng. Các mốc đăng ký/thu phí tập trung tháng 8 trong thông báo đã qua; sinh viên mới có nhu cầu cần liên hệ KTX để xác nhận. [1]
- Chuyển chỗ, trả chỗ và hoàn phí: Sinh viên có thể xin chuyển chỗ theo hướng dẫn và chỗ phù hợp còn trống. Trả chỗ trước hạn không được hoàn phí, ngoại lệ trả trong vòng 7 ngày từ ngày được duyệt chỗ qua hệ thống và có lý do chính đáng. Cần đối chiếu quy định với văn phòng trước khi trả chỗ. [1]

### Nguồn và ngữ cảnh

**[1] [Thông báo 307/TB-CTSV · HKI 2026–2027](https://ssc.ctu.edu.vn/images/upload/thong_bao/072026_tb_dk1_2627.pdf)**

Danh mục KTX · cập nhật 2026-10-12

Đường dẫn nguồn: Danh mục KTX dùng chung

```text
Sinh viên đăng ký mới qua Hệ thống Quản lý KTX bằng tài khoản sinh viên, email ktx@ctu.edu.vn hoặc trực tiếp tại Văn phòng Trung tâm Phục vụ Sinh viên. Có thể ghi nguyện vọng và đăng ký nhóm; ưu tiên nhóm đủ số người bằng sức chứa phòng. Kết quả phụ thuộc sắp xếp chỗ của KTX.

HKI năm học 2026–2027 ở từ 07/09/2026 đến 18/12/2026, tính 3,5 tháng. Các mốc đăng ký/thu phí tập trung tháng 8 trong thông báo đã qua; sinh viên mới có nhu cầu cần liên hệ KTX để xác nhận.

Sinh viên có thể xin chuyển chỗ theo hướng dẫn và chỗ phù hợp còn trống. Trả chỗ trước hạn không được hoàn phí, ngoại lệ trả trong vòng 7 ngày từ ngày được duyệt chỗ qua hệ thống và có lý do chính đáng. Cần đối chiếu quy định với văn phòng trước khi trả chỗ.
```

**[2] [Hướng dẫn tân sinh viên đăng ký KTX · 2026–2027](https://tansinhvien.ctu.edu.vn/sinh-hoat/huong-dan-tan-sinh-vien-dang-ky-o-ky-tuc-xa)**

Danh mục KTX · cập nhật 2026-10-12

Đường dẫn nguồn: Danh mục KTX dùng chung

```text
Tân sinh viên chưa có tài khoản hệ thống có thể điền mẫu nhu cầu ở được liên kết trên trang hướng dẫn chính thức. Sinh viên có tài khoản làm theo hướng dẫn đăng ký KTX qua hệ thống.
```


## Câu 41 · Ký túc xá

Tôi có thể đối chiếu chi phí và điều kiện ở ký túc xá với phòng trọ tư nhân như thế nào?

Trạng thái: Đã trả lời · cần rà nguồn. Provider: structured_housing_advice; model: —.

faithfulness: 0.7143 | answer_relevancy: 0.8628 | context_utilization: 1.0 | context_recall: 1.0 | context_precision: 1.0

ID nguồn chuẩn: Danh mục phòng KTX năm 2026 · bạn cung cấp, https://www.chotot.com/133994707.htm, https://www.chotot.com/134770078.htm

ID nguồn đã truy xuất: Danh mục phòng KTX năm 2026 · bạn cung cấp, https://www.chotot.com/133994707.htm, https://www.chotot.com/134770078.htm

**KTX CTU · năm học 2026-2027**
- Theo danh mục 27 loại phòng bạn cung cấp cho năm 2026, đơn giá từ 220.000 đến 967.000 đồng/người/học kỳ 3,5 tháng. Chưa gồm điện nước; cần xác nhận mức thu và chỗ trống tại thời điểm đăng ký với văn phòng KTX. [1]
- KTX CTU · PT025 · khu chưa xác nhận · sức chứa 8 người. Phòng không được nấu ăn, được sử dụng ấm đun siêu tốc, giường tầng. không được nấu ăn; giường tầng. Giá 220.000 đồng/người/học kỳ 3,5 tháng (2026). Giá theo bảng phòng bạn cung cấp cho năm 2026; xác nhận mức thu và chỗ trống với văn phòng KTX. [1]
- KTX CTU · PT725 · khu chưa xác nhận · sức chứa 7 người. Phòng không được nấu ăn, được sử dụng ấm đun siêu tốc, ít người, giường tầng. không được nấu ăn; giường tầng. Giá 255.000 đồng/người/học kỳ 3,5 tháng (2026). Giá theo bảng phòng bạn cung cấp cho năm 2026; xác nhận mức thu và chỗ trống với văn phòng KTX. [1]

**Nhà trọ trong bộ dữ liệu hiện có**
- Cho sv thuê phòng mới 16m2 cách ĐHYD, ĐHCT 2km — 750.000 đồng/phòng/tháng; khoảng cách lưu trong tin tới CTU 1.033 m (không phải thời gian hoặc lộ trình đã xác minh); tiện nghi tin có nêu: nấu ăn, WC riêng, Wi-Fi, để xe. [2]
- Cho thuê phòng trọ ngang khu công nghiệp Hưng Phú cần Thơ giá rẻ — 800.000 đồng/phòng/tháng; khoảng cách lưu trong tin tới CTU 5.312 m (không phải thời gian hoặc lộ trình đã xác minh); tiện nghi tin có nêu: chưa có xác nhận. [3]
- Giá tin là tiền thuê phòng theo tháng, chưa xác nhận cọc, điện nước, Wi-Fi, gửi xe hoặc số người tối đa. Nhãn tiện nghi không xác nhận chi phí đã bao gồm.

**Gợi ý lựa chọn**
Nếu ưu tiên tiết kiệm và chấp nhận ở chung, nên hỏi KTX trước để chốt biểu phí và chỗ trống; nếu ưu tiên không gian riêng, cân nhắc nhà trọ sau khi xác nhận điều kiện thuê. Cần so sánh cùng kỳ tính giá, số người và chi phí kèm theo trước khi kết luận phương án nào rẻ hơn hoặc nằm trong tổng ngân sách.
Cả danh mục KTX lẫn tin nhà trọ không xác nhận chỗ trống hiện tại. Liên hệ văn phòng KTX hoặc người cho thuê trước khi chuyển vào hay đặt cọc.
Bạn dự kiến bao nhiêu tiền mỗi tháng, tính riêng tiền thuê hay tổng chi phí?

### Nguồn và ngữ cảnh

**[1] Danh mục phòng KTX năm 2026 · bạn cung cấp**



Đường dẫn nguồn: Danh mục KTX dùng chung

```text
Theo danh mục 27 loại phòng bạn cung cấp cho năm 2026, đơn giá từ 220.000 đến 967.000 đồng/người/học kỳ 3,5 tháng. Chưa gồm điện nước; cần xác nhận mức thu và chỗ trống tại thời điểm đăng ký với văn phòng KTX.

KTX CTU · PT025 · khu chưa xác nhận · sức chứa 8 người. Phòng không được nấu ăn, được sử dụng ấm đun siêu tốc, giường tầng. không được nấu ăn; giường tầng. Giá 220.000 đồng/người/học kỳ 3,5 tháng (2026). Giá theo bảng phòng bạn cung cấp cho năm 2026; xác nhận mức thu và chỗ trống với văn phòng KTX.

KTX CTU · PT725 · khu chưa xác nhận · sức chứa 7 người. Phòng không được nấu ăn, được sử dụng ấm đun siêu tốc, ít người, giường tầng. không được nấu ăn; giường tầng. Giá 255.000 đồng/người/học kỳ 3,5 tháng (2026). Giá theo bảng phòng bạn cung cấp cho năm 2026; xác nhận mức thu và chỗ trống với văn phòng KTX.
```

**[2] [Cho sv thuê phòng mới 16m2 cách ĐHYD, ĐHCT 2km](https://www.chotot.com/133994707.htm)**



Đường dẫn nguồn: Danh mục KTX dùng chung

```text
Cho sv thuê phòng mới 16m2 cách ĐHYD, ĐHCT 2km — 750.000 đồng/phòng/tháng; khoảng cách lưu trong tin tới CTU 1.033 m (không phải thời gian hoặc lộ trình đã xác minh); tiện nghi tin có nêu: nấu ăn, WC riêng, Wi-Fi, để xe
Mô tả nguồn: Thông tin quảng cáo theo nguồn; chưa xác minh còn phòng, kỳ thu giá hoặc tiện ích.
Diện tích thiếu là chưa biết, không tự điền. Loại chỗ ở theo tin: room.
Khoảng cách đường chim bay ước tính đến cổng khu II CTU: 1.033 km; tọa độ gần đúng, chưa đo tuyến đường.
- Giá phòng:  750K/tháng-- Ưu tiên các bạn sinh viên nam ĐHYD , ĐHCT năm 1 (lưu ý phòng trọ sinh viên, nên chỉ cho sinh viên thuê).
- Phòng mới 16m2 sạch đẹp, thoáng mát, giá điện nước theo quy định nhà nước!
- Phòng gồm giường ngủ, kệ bếp, sàn rửa chén, phòng vệ sinh riêng, không ngập nước, không có gác.
- Yêu cầu là các bạn sinh viên nam, học tập nghiêm túc, không làm ồn, không đi khuya, thuê lâu dài.
- Gần ngã 4 đ.3/2 và Nguyễn Văn Linh, gần siêu thị Mega, cửa hàng tiện lợi, chợ truyền thống, gần ĐHCT, ĐHYD, gần bến xe, bệnh viện,...
- Có đường đi riêng vào nhà trọ, có sân phơi đồ, nhà để xe, wifi, camera an ninh.
- Vui lòng liên hệ giờ hành chính, gặp chú Đăng.
```

**[3] [Cho thuê phòng trọ ngang khu công nghiệp Hưng Phú cần Thơ giá rẻ](https://www.chotot.com/134770078.htm)**



Đường dẫn nguồn: Danh mục KTX dùng chung

```text
Cho thuê phòng trọ ngang khu công nghiệp Hưng Phú cần Thơ giá rẻ — 800.000 đồng/phòng/tháng; khoảng cách lưu trong tin tới CTU 5.312 m (không phải thời gian hoặc lộ trình đã xác minh); tiện nghi tin có nêu: chưa có xác nhận
Mô tả nguồn: Thông tin quảng cáo theo nguồn; chưa xác minh còn phòng, kỳ thu giá hoặc tiện ích.
Diện tích thiếu là chưa biết, không tự điền. Loại chỗ ở theo tin: room.
Khoảng cách đường chim bay ước tính đến cổng khu II CTU: 5.312 km; tọa độ gần đúng, chưa đo tuyến đường.
Nhà trọ ngang khu Công nghiệp Hưng Phú cần Thơ. Còn 2 căn lẻ và 1 căn đầu rộng rãi như căn hộ có thể vừa ở vừa kinh doanh. Ngang cổng khu công nghiệp.
```


## Câu 42 · Ký túc xá

Nếu tài liệu ký túc xá không nêu một mức phí hoặc thời hạn, hãy nói rõ thông tin nào còn thiếu.

Trạng thái: Đã trả lời · cần rà nguồn. Provider: structured_ktx; model: —.

faithfulness: 1.0 | answer_relevancy: 0.8746 | context_utilization: 1.0 | context_recall: 1.0 | context_precision: 0.6667

ID nguồn chuẩn: Danh mục phòng KTX năm 2026 · bạn cung cấp, https://ssc.ctu.edu.vn/images/upload/thong_bao/072026_tb_dk1_2627.pdf

ID nguồn đã truy xuất: Danh mục phòng KTX năm 2026 · bạn cung cấp, https://ssc.ctu.edu.vn/images/upload/thong_bao/072026_tb_dk1_2627.pdf, https://tansinhvien.ctu.edu.vn/sinh-hoat/huong-dan-tan-sinh-vien-dang-ky-o-ky-tuc-xa

**KTX · năm học 2026-2027**
- Phí ở và đơn vị giá: Theo danh mục 27 loại phòng bạn cung cấp cho năm 2026, đơn giá từ 220.000 đến 967.000 đồng/người/học kỳ 3,5 tháng. Chưa gồm điện nước; cần xác nhận mức thu và chỗ trống tại thời điểm đăng ký với văn phòng KTX. [1]
- Điện nước: Sinh viên nộp phí điện, nước hàng tháng theo lượng sử dụng thực tế của phòng; phí ở chưa bao gồm điện nước. [2]
- Gửi xe: Xe đạp được miễn phí gửi xe. Trang hướng dẫn tân sinh viên 2026–2027 công bố xe máy/xe điện 25.000 đồng/sinh viên/tháng, nộp theo học kỳ. [3]

### Nguồn và ngữ cảnh

**[1] Danh mục phòng KTX năm 2026 · bạn cung cấp**

Danh mục KTX · cập nhật 2026-10-12

Đường dẫn nguồn: Danh mục KTX dùng chung

```text
Theo danh mục 27 loại phòng bạn cung cấp cho năm 2026, đơn giá từ 220.000 đến 967.000 đồng/người/học kỳ 3,5 tháng. Chưa gồm điện nước; cần xác nhận mức thu và chỗ trống tại thời điểm đăng ký với văn phòng KTX.
```

**[2] [Thông báo 307/TB-CTSV · HKI 2026–2027](https://ssc.ctu.edu.vn/images/upload/thong_bao/072026_tb_dk1_2627.pdf)**

Danh mục KTX · cập nhật 2026-10-12

Đường dẫn nguồn: Danh mục KTX dùng chung

```text
Sinh viên nộp phí điện, nước hàng tháng theo lượng sử dụng thực tế của phòng; phí ở chưa bao gồm điện nước.
```

**[3] [Hướng dẫn tân sinh viên đăng ký KTX · 2026–2027](https://tansinhvien.ctu.edu.vn/sinh-hoat/huong-dan-tan-sinh-vien-dang-ky-o-ky-tuc-xa)**

Danh mục KTX · cập nhật 2026-10-12

Đường dẫn nguồn: Danh mục KTX dùng chung

```text
Xe đạp được miễn phí gửi xe. Trang hướng dẫn tân sinh viên 2026–2027 công bố xe máy/xe điện 25.000 đồng/sinh viên/tháng, nộp theo học kỳ.
```


## Câu 43 · Môi giới

Người giới thiệu phòng trọ và thu phí môi giới cần công khai những thông tin gì?

Trạng thái: Trả lời một phần. Provider: gemini-agent; model: gemini-3.8-flash-high.

faithfulness: 1.0 | answer_relevancy: 0.0 | context_utilization: 0.6389 | context_recall: 1.0 | context_precision: 0.5

ID nguồn chuẩn: broker29-word.json

ID nguồn đã truy xuất: civil91-word.json, broker29-word.json

Doanh nghiệp môi giới bất động sản phải cung cấp đầy đủ, trung thực hồ sơ, thông tin về bất động sản môi giới và gửi thông tin doanh nghiệp để đăng tải trên hệ thống thông tin theo quy định [3] [4].

- Doanh nghiệp kinh doanh dịch vụ môi giới có nghĩa vụ cung cấp đầy đủ, trung thực hồ sơ, thông tin về bất động sản do mình môi giới và chịu trách nhiệm về thông tin đó [4].
- Trước khi hoạt động, doanh nghiệp môi giới phải gửi thông tin về doanh nghiệp đến cơ quan quản lý nhà nước về kinh doanh bất động sản cấp tỉnh để được đăng tải trên hệ thống thông tin về nhà ở và thị trường bất động sản [3].
- Hợp đồng dịch vụ môi giới phải thể hiện các nội dung chính về tên địa chỉ các bên, đối tượng, kết quả dịch vụ, phí dịch vụ cùng phương thức thanh toán [2].

Đoạn nguồn cung cấp chưa nêu danh mục tài liệu chi tiết cụ thể riêng cho phòng trọ cho thuê mà chỉ quy định nghĩa vụ cung cấp hồ sơ, thông tin bất động sản nói chung [4].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng.
Cần đối chiếu điều/khoản được dẫn chiếu còn thiếu; đoạn trích chưa đủ để kết luận toàn bộ điều kiện và ngoại lệ.
Nguồn là bản Word/trích tuyển được cung cấp, chưa xác minh toàn bộ câu chữ với bản chính thức; không coi ghi chú biên tập là quy định pháp luật.

### Nguồn và ngữ cảnh

**[1] [Bộ luật Dân sự 91/2015/QH13 — Word do cơ quan nhà nước công bố](https://congan.daklak.gov.vn/laws/detail/Bo-luat-Dan-su-163/)**

Điều 520. Đơn phương chấm dứt thực hiện hợp đồng dịch vụ | Khoản 1 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_repair_corpus_v14_20261006/civil91-word.json

```text
1. Trường hợp việc tiếp tục thực hiện công việc không có lợi cho bên sử
dụng dịch vụ thì bên sử dụng dịch vụ có quyền đơn phương chấm dứt thực hiện
hợp đồng, nhưng phải báo cho bên cung ứng dịch vụ biết trước một thời gian
hợp lý; bên sử dụng dịch vụ phải trả tiền công theo phần dịch vụ mà bên
cung ứng dịch vụ đã thực hiện và bồi thường thiệt hại.
```

**[2] [Luật Kinh doanh bất động sản 29/2023/QH15 — bản Word cung cấp](https://vanban.chinhphu.vn/?classid=1&docid=209624&pageid=27160&typegroupid=3)**

Điều 46. Nội dung chính của hợp đồng trong kinh doanh bất động sản | Khoản 4 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_corpus_v7_20261005/broker29-word.json

```text
4. Hợp đồng kinh doanh dịch vụ bất động sản phải có các nội dung chính sau đây:

a) Tên, địa chỉ của các bên;

b) Đối tượng và nội dung dịch vụ;

c) Yêu cầu và kết quả dịch vụ;

d) Thời hạn thực hiện dịch vụ;

đ) Phí dịch vụ, thù lao, hoa hồng dịch vụ;

e) Phương thức và thời hạn thanh toán;

g) Quyền, nghĩa vụ của các bên;

h) Phương thức giải quyết tranh chấp;

i) Thời điểm có hiệu lực của hợp đồng.
```

**[3] [Luật Kinh doanh bất động sản 29/2023/QH15 — bản Word cung cấp](https://vanban.chinhphu.vn/?classid=1&docid=209624&pageid=27160&typegroupid=3)**

Điều 61. Điều kiện của tổ chức, cá nhân kinh doanh dịch vụ môi giới bất động sản | Khoản 1 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_corpus_v7_20261005/broker29-word.json

```text
1. Tổ chức, cá nhân kinh doanh dịch vụ môi giới bất động sản phải thành lập doanh nghiệp kinh doanh dịch vụ bất động sản theo quy định tại khoản 5 Điều 9 của Luật này và phải đáp ứng các điều kiện sau đây:

a) Phải có quy chế hoạt động dịch vụ môi giới bất động sản;

b) Phải có cơ sở vật chất, kỹ thuật đáp ứng yêu cầu hoạt động theo quy định của Chính phủ;

c) Có tối thiểu 01 cá nhân có chứng chỉ môi giới bất động sản;

d) Trước khi hoạt động kinh doanh dịch vụ môi giới bất động sản, doanh nghiệp kinh doanh dịch vụ môi giới bất động sản gửi thông tin về doanh nghiệp đến cơ quan quản lý nhà nước về kinh doanh bất động sản cấp tỉnh nơi thành lập doanh nghiệp để được đăng tải trên hệ thống thông tin về nhà ở và thị trường bất động sản theo quy định của Luật này.
```

**[4] [Luật Kinh doanh bất động sản 29/2023/QH15 — bản Word cung cấp](https://vanban.chinhphu.vn/?classid=1&docid=209624&pageid=27160&typegroupid=3)**

Điều 65. Nghĩa vụ của doanh nghiệp kinh doanh dịch vụ môi giới bất động sản, cá nhân hành nghề môi giới bất động sản | Khoản 1 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_corpus_v7_20261005/broker29-word.json

```text
1. Doanh nghiệp kinh doanh dịch vụ môi giới bất động sản có các nghĩa vụ sau đây:

a) Cung cấp đầy đủ, trung thực hồ sơ, thông tin về bất động sản do mình môi giới và chịu trách nhiệm về hồ sơ, thông tin do mình cung cấp;

b) Tổ chức đào tạo, bồi dưỡng nâng cao kiến thức hành nghề môi giới bất động sản cho nhân viên môi giới bất động sản làm việc trong doanh nghiệp hằng năm;

c) Thực hiện nghĩa vụ thuế đối với Nhà nước;

d) Bồi thường thiệt hại do lỗi của mình gây ra;

đ) Thực hiện chế độ báo cáo theo quy định của pháp luật và chịu sự kiểm tra, thanh tra của cơ quan nhà nước có thẩm quyền;

e) Nghĩa vụ khác theo hợp đồng.
```

**[5] [Bộ luật Dân sự 91/2015/QH13 — Word do cơ quan nhà nước công bố](https://congan.daklak.gov.vn/laws/detail/Bo-luat-Dan-su-163/)**

Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_repair_corpus_v14_20261006/civil91-word.json

```text
Điều 117. Điều kiện có hiệu lực của giao dịch dân sự | Khoản 1
1. Giao dịch dân sự có hiệu lực khi có đủ các điều kiện sau đây:

a) Chủ thể có năng lực pháp luật dân sự, năng lực hành vi dân sự phù hợp
với giao dịch dân sự được xác lập;

b) Chủ thể tham gia giao dịch dân sự hoàn toàn tự nguyện;

c) Mục đích và nội dung của giao dịch dân sự không vi phạm điều cấm của
luật, không trái đạo đức xã hội.

Điều 117. Điều kiện có hiệu lực của giao dịch dân sự | Khoản 2
2. Hình thức của giao dịch dân sự là điều kiện có hiệu lực của giao dịch
dân sự trong trường hợp luật có quy định.
```

### Lỗi và giới hạn đã ghi nhận

```json
{
  "collect": null,
  "ragas": {},
  "unavailable": null,
  "degraded": [
    "Phản hồi chưa đáp ứng đầy đủ yêu cầu chính; đánh dấu theo nội dung thay vì provider."
  ]
}
```


## Câu 44 · Môi giới

Trước khi chuyển tiền cho người môi giới, tôi nên kiểm tra quyền cho thuê và thông tin phòng như thế nào?

Trạng thái: Trả lời một phần. Provider: gemini-agent; model: gemini-3.8-flash-high.

faithfulness: 1.0 | answer_relevancy: 0.0 | context_utilization: 0.95 | context_recall: 1.0 | context_precision: 0.6667

ID nguồn chuẩn: broker29-word.json, housing79-word.json

ID nguồn đã truy xuất: civil91-word.json, broker29-word.json, housing79-word.json

Chưa đủ căn cứ từ nguồn để hướng dẫn chi tiết cách kiểm tra thực tế quyền cho thuê và thông tin phòng trọ trước khi chuyển tiền [2] [5].

- Giao dịch dân sự có hiệu lực khi chủ thể có năng lực phù hợp, hoàn toàn tự nguyện, mục đích và nội dung không vi phạm điều cấm của luật, không trái đạo đức xã hội và bảo đảm điều kiện về hình thức nếu luật có quy định [5].
- Hợp đồng dịch vụ là sự thỏa thuận giữa các bên, theo đó bên cung ứng dịch vụ thực hiện công việc và bên sử dụng dịch vụ phải trả tiền [3].
- Hợp đồng kinh doanh dịch vụ bất động sản phải có các nội dung chính gồm tên, địa chỉ các bên, đối tượng, nội dung, yêu cầu, kết quả, thời hạn thực hiện dịch vụ, phí dịch vụ, thù lao, hoa hồng, phương thức và thời hạn thanh toán, quyền và nghĩa vụ các bên, phương thức giải quyết tranh chấp và thời điểm có hiệu lực [2].
- Trường hợp tiếp tục thực hiện công việc không có lợi thì bên sử dụng dịch vụ có quyền đơn phương chấm dứt hợp đồng dịch vụ nhưng phải báo trước thời gian hợp lý, trả tiền công theo phần đã thực hiện và bồi thường thiệt hại [1].

Nguồn trích dẫn không quy định cụ thể checklist hoặc quy trình kiểm tra giấy tờ chứng minh quyền cho thuê và tình trạng phòng đối với giao dịch qua môi giới [2] [5].

Nguồn là bản Word/trích tuyển được cung cấp, chưa xác minh toàn bộ câu chữ với bản chính thức; không coi ghi chú biên tập là quy định pháp luật.

### Nguồn và ngữ cảnh

**[1] [Bộ luật Dân sự 91/2015/QH13 — Word do cơ quan nhà nước công bố](https://congan.daklak.gov.vn/laws/detail/Bo-luat-Dan-su-163/)**

Điều 520. Đơn phương chấm dứt thực hiện hợp đồng dịch vụ | Khoản 1 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_repair_corpus_v14_20261006/civil91-word.json

```text
1. Trường hợp việc tiếp tục thực hiện công việc không có lợi cho bên sử
dụng dịch vụ thì bên sử dụng dịch vụ có quyền đơn phương chấm dứt thực hiện
hợp đồng, nhưng phải báo cho bên cung ứng dịch vụ biết trước một thời gian
hợp lý; bên sử dụng dịch vụ phải trả tiền công theo phần dịch vụ mà bên
cung ứng dịch vụ đã thực hiện và bồi thường thiệt hại.
```

**[2] [Luật Kinh doanh bất động sản 29/2023/QH15 — bản Word cung cấp](https://vanban.chinhphu.vn/?classid=1&docid=209624&pageid=27160&typegroupid=3)**

Điều 46. Nội dung chính của hợp đồng trong kinh doanh bất động sản | Khoản 4 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_corpus_v7_20261005/broker29-word.json

```text
4. Hợp đồng kinh doanh dịch vụ bất động sản phải có các nội dung chính sau đây:

a) Tên, địa chỉ của các bên;

b) Đối tượng và nội dung dịch vụ;

c) Yêu cầu và kết quả dịch vụ;

d) Thời hạn thực hiện dịch vụ;

đ) Phí dịch vụ, thù lao, hoa hồng dịch vụ;

e) Phương thức và thời hạn thanh toán;

g) Quyền, nghĩa vụ của các bên;

h) Phương thức giải quyết tranh chấp;

i) Thời điểm có hiệu lực của hợp đồng.
```

**[3] [Bộ luật Dân sự 91/2015/QH13 — Word do cơ quan nhà nước công bố](https://congan.daklak.gov.vn/laws/detail/Bo-luat-Dan-su-163/)**

Điều 513. Hợp đồng dịch vụ · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_repair_corpus_v14_20261006/civil91-word.json

```text
Điều 513. Hợp đồng dịch vụ

Hợp đồng dịch vụ là sự thỏa thuận giữa các bên, theo đó bên cung ứng dịch
vụ thực hiện công việc cho bên sử dụng dịch vụ, bên sử dụng dịch vụ phải
trả tiền dịch vụ cho bên cung ứng dịch vụ.
```

**[4] [Luật Nhà ở — 79/VBHN-VPQH — bản Word cung cấp](https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-79-vbhn-vpqh-469209.htm)**

Điều 160. Điều kiện của nhà ở tham gia giao dịch | Khoản 2 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_corpus_v7_20261005/housing79-word.json

```text
2. Giao dịch về nhà ở sau đây thì nhà ở không bắt buộc phải có Giấy chứng nhận:

a) Mua bán, thuê mua, thế chấp nhà ở hình thành trong tương lai; bán nhà ở trong trường hợp giải thể, phá sản;

b) Tổ chức tặng cho nhà tình nghĩa, nhà tình thương, nhà đại đoàn kết;

c) Mua bán, thuê mua nhà ở có sẵn của chủ đầu tư dự án đầu tư xây dựng nhà ở trong các trường hợp sau đây: nhà ở thuộc tài sản công; nhà ở xã hội, nhà ở cho lực lượng vũ trang nhân dân, nhà ở phục vụ tái định cư không thuộc tài sản công;

d) Cho thuê, cho mượn, cho ở nhờ, ủy quyền quản lý nhà ở;

đ) Nhận thừa kế nhà ở.

Giấy tờ chứng minh điều kiện nhà ở tham gia giao dịch quy định tại khoản này thực hiện theo quy định của Chính phủ.
```

**[5] [Bộ luật Dân sự 91/2015/QH13 — Word do cơ quan nhà nước công bố](https://congan.daklak.gov.vn/laws/detail/Bo-luat-Dan-su-163/)**

Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_repair_corpus_v14_20261006/civil91-word.json

```text
Điều 117. Điều kiện có hiệu lực của giao dịch dân sự | Khoản 1
1. Giao dịch dân sự có hiệu lực khi có đủ các điều kiện sau đây:

a) Chủ thể có năng lực pháp luật dân sự, năng lực hành vi dân sự phù hợp
với giao dịch dân sự được xác lập;

b) Chủ thể tham gia giao dịch dân sự hoàn toàn tự nguyện;

c) Mục đích và nội dung của giao dịch dân sự không vi phạm điều cấm của
luật, không trái đạo đức xã hội.

Điều 117. Điều kiện có hiệu lực của giao dịch dân sự | Khoản 2
2. Hình thức của giao dịch dân sự là điều kiện có hiệu lực của giao dịch
dân sự trong trường hợp luật có quy định.
```

### Lỗi và giới hạn đã ghi nhận

```json
{
  "collect": null,
  "ragas": {},
  "unavailable": null,
  "degraded": [
    "Phản hồi chưa đáp ứng đầy đủ yêu cầu chính; đánh dấu theo nội dung thay vì provider."
  ]
}
```


## Câu 45 · Môi giới

Nếu người môi giới đưa thông tin khác với phòng thực tế, người thuê có thể làm gì?

Trạng thái: Đã trả lời · cần rà nguồn. Provider: gemini-agent; model: gemini-3.8-flash-high.

faithfulness: 0.75 | answer_relevancy: 0.8488 | context_utilization: 0.75 | context_recall: 1.0 | context_precision: 1.0

ID nguồn chuẩn: broker29-word.json, civil91-word.json

ID nguồn đã truy xuất: civil91-word.json, broker29-word.json

Doanh nghiệp môi giới phải cung cấp trung thực thông tin bất động sản và bồi thường thiệt hại do lỗi của mình gây ra, đồng thời bên thuê có quyền đơn phương chấm dứt hợp đồng dịch vụ nếu việc tiếp tục không có lợi [1] [4].

- Yêu cầu bên môi giới chịu trách nhiệm và bồi thường thiệt hại nếu việc cung cấp thông tin sai lệch do lỗi của môi giới gây ra [4].
- Bên sử dụng dịch vụ có quyền đơn phương chấm dứt thực hiện hợp đồng dịch vụ khi việc tiếp tục công việc không có lợi nhưng phải báo trước một thời gian hợp lý [1].
- Khi đơn phương chấm dứt hợp đồng dịch vụ, bên sử dụng dịch vụ phải trả tiền công theo phần dịch vụ đã thực hiện và bồi thường thiệt hại [1].
- Khuyến nghị đối chiếu thông tin phòng thực tế với nội dung cam kết và thỏa thuận cụ thể trong hợp đồng dịch vụ đã xác lập [4] [5].

Nguồn quy định nghĩa vụ cung cấp thông tin trung thực và bồi thường áp dụng trực tiếp đối với doanh nghiệp kinh doanh dịch vụ môi giới bất động sản [4].
Quy định chấm dứt hợp đồng dịch vụ gắn liền với nghĩa vụ thanh toán phần công việc đã làm và bồi thường thiệt hại theo quy định của Bộ luật Dân sự [1].

Nguồn là bản Word/trích tuyển được cung cấp, chưa xác minh toàn bộ câu chữ với bản chính thức; không coi ghi chú biên tập là quy định pháp luật.

### Nguồn và ngữ cảnh

**[1] [Bộ luật Dân sự 91/2015/QH13 — Word do cơ quan nhà nước công bố](https://congan.daklak.gov.vn/laws/detail/Bo-luat-Dan-su-163/)**

Điều 520. Đơn phương chấm dứt thực hiện hợp đồng dịch vụ | Khoản 1 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_repair_corpus_v14_20261006/civil91-word.json

```text
1. Trường hợp việc tiếp tục thực hiện công việc không có lợi cho bên sử
dụng dịch vụ thì bên sử dụng dịch vụ có quyền đơn phương chấm dứt thực hiện
hợp đồng, nhưng phải báo cho bên cung ứng dịch vụ biết trước một thời gian
hợp lý; bên sử dụng dịch vụ phải trả tiền công theo phần dịch vụ mà bên
cung ứng dịch vụ đã thực hiện và bồi thường thiệt hại.
```

**[2] [Bộ luật Dân sự 91/2015/QH13 — Word do cơ quan nhà nước công bố](https://congan.daklak.gov.vn/laws/detail/Bo-luat-Dan-su-163/)**

Điều 520. Đơn phương chấm dứt thực hiện hợp đồng dịch vụ | Khoản 2 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_repair_corpus_v14_20261006/civil91-word.json

```text
2. Trường hợp bên sử dụng dịch vụ vi phạm nghiêm trọng nghĩa vụ thì bên
cung ứng dịch vụ có quyền đơn phương chấm dứt thực hiện hợp đồng và yêu cầu
bồi thường thiệt hại.
```

**[3] [Luật Kinh doanh bất động sản 29/2023/QH15 — bản Word cung cấp](https://vanban.chinhphu.vn/?classid=1&docid=209624&pageid=27160&typegroupid=3)**

Điều 46. Nội dung chính của hợp đồng trong kinh doanh bất động sản | Khoản 4 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_corpus_v7_20261005/broker29-word.json

```text
4. Hợp đồng kinh doanh dịch vụ bất động sản phải có các nội dung chính sau đây:

a) Tên, địa chỉ của các bên;

b) Đối tượng và nội dung dịch vụ;

c) Yêu cầu và kết quả dịch vụ;

d) Thời hạn thực hiện dịch vụ;

đ) Phí dịch vụ, thù lao, hoa hồng dịch vụ;

e) Phương thức và thời hạn thanh toán;

g) Quyền, nghĩa vụ của các bên;

h) Phương thức giải quyết tranh chấp;

i) Thời điểm có hiệu lực của hợp đồng.
```

**[4] [Luật Kinh doanh bất động sản 29/2023/QH15 — bản Word cung cấp](https://vanban.chinhphu.vn/?classid=1&docid=209624&pageid=27160&typegroupid=3)**

Điều 65. Nghĩa vụ của doanh nghiệp kinh doanh dịch vụ môi giới bất động sản, cá nhân hành nghề môi giới bất động sản | Khoản 1 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_corpus_v7_20261005/broker29-word.json

```text
1. Doanh nghiệp kinh doanh dịch vụ môi giới bất động sản có các nghĩa vụ sau đây:

a) Cung cấp đầy đủ, trung thực hồ sơ, thông tin về bất động sản do mình môi giới và chịu trách nhiệm về hồ sơ, thông tin do mình cung cấp;

b) Tổ chức đào tạo, bồi dưỡng nâng cao kiến thức hành nghề môi giới bất động sản cho nhân viên môi giới bất động sản làm việc trong doanh nghiệp hằng năm;

c) Thực hiện nghĩa vụ thuế đối với Nhà nước;

d) Bồi thường thiệt hại do lỗi của mình gây ra;

đ) Thực hiện chế độ báo cáo theo quy định của pháp luật và chịu sự kiểm tra, thanh tra của cơ quan nhà nước có thẩm quyền;

e) Nghĩa vụ khác theo hợp đồng.
```

**[5] [Bộ luật Dân sự 91/2015/QH13 — Word do cơ quan nhà nước công bố](https://congan.daklak.gov.vn/laws/detail/Bo-luat-Dan-su-163/)**

Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_repair_corpus_v14_20261006/civil91-word.json

```text
Điều 117. Điều kiện có hiệu lực của giao dịch dân sự | Khoản 1
1. Giao dịch dân sự có hiệu lực khi có đủ các điều kiện sau đây:

a) Chủ thể có năng lực pháp luật dân sự, năng lực hành vi dân sự phù hợp
với giao dịch dân sự được xác lập;

b) Chủ thể tham gia giao dịch dân sự hoàn toàn tự nguyện;

c) Mục đích và nội dung của giao dịch dân sự không vi phạm điều cấm của
luật, không trái đạo đức xã hội.

Điều 117. Điều kiện có hiệu lực của giao dịch dân sự | Khoản 2
2. Hình thức của giao dịch dân sự là điều kiện có hiệu lực của giao dịch
dân sự trong trường hợp luật có quy định.
```


## Câu 46 · Môi giới

Khoản phí môi giới nên được thỏa thuận và thể hiện trong giấy tờ ra sao?

Trạng thái: Trả lời một phần. Provider: gemini-agent; model: gemini-3.8-flash-high.

faithfulness: 1.0 | answer_relevancy: 0.8319 | context_utilization: 1.0 | context_recall: 1.0 | context_precision: 1.0

ID nguồn chuẩn: broker29-word.json, civil91-word.json

ID nguồn đã truy xuất: civil91-word.json, broker29-word.json

Hợp đồng kinh doanh dịch vụ bất động sản phải có nội dung chính về phí dịch vụ, thù lao, hoa hồng dịch vụ cùng phương thức và thời hạn thanh toán [3].

- Hợp đồng dịch vụ bất động sản phải thể hiện rõ tên, địa chỉ các bên, đối tượng, nội dung, yêu cầu, kết quả và thời hạn thực hiện dịch vụ [3].
- Hợp đồng phải quy định cụ thể phí dịch vụ, thù lao, hoa hồng dịch vụ cũng như phương thức và thời hạn thanh toán [3].
- Trường hợp dịch vụ cung ứng không đạt thỏa thuận hoặc không đúng hạn, bên sử dụng dịch vụ có quyền giảm tiền dịch vụ và yêu cầu bồi thường thiệt hại [1].
- Nếu việc tiếp tục công việc không có lợi, bên sử dụng dịch vụ được đơn phương chấm dứt hợp đồng sau khi báo trước thời gian hợp lý nhưng phải trả tiền công phần việc đã làm và bồi thường thiệt hại [2].

Chưa đủ căn cứ từ các đoạn nguồn để xác định mức phí cụ thể hoặc biểu mẫu hợp đồng dịch vụ môi giới chi tiết [3].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng.
Nguồn là bản Word/trích tuyển được cung cấp, chưa xác minh toàn bộ câu chữ với bản chính thức; không coi ghi chú biên tập là quy định pháp luật.

### Nguồn và ngữ cảnh

**[1] [Bộ luật Dân sự 91/2015/QH13 — Word do cơ quan nhà nước công bố](https://congan.daklak.gov.vn/laws/detail/Bo-luat-Dan-su-163/)**

Điều 519. Trả tiền dịch vụ | Khoản 4 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_repair_corpus_v14_20261006/civil91-word.json

```text
4. Trường hợp dịch vụ được cung ứng không đạt được như thỏa thuận hoặc công
việc không được hoàn thành đúng thời hạn thì bên sử dụng dịch vụ có quyền
giảm tiền dịch vụ và yêu cầu bồi thường thiệt hại.
```

**[2] [Bộ luật Dân sự 91/2015/QH13 — Word do cơ quan nhà nước công bố](https://congan.daklak.gov.vn/laws/detail/Bo-luat-Dan-su-163/)**

Điều 520. Đơn phương chấm dứt thực hiện hợp đồng dịch vụ | Khoản 1 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_repair_corpus_v14_20261006/civil91-word.json

```text
1. Trường hợp việc tiếp tục thực hiện công việc không có lợi cho bên sử
dụng dịch vụ thì bên sử dụng dịch vụ có quyền đơn phương chấm dứt thực hiện
hợp đồng, nhưng phải báo cho bên cung ứng dịch vụ biết trước một thời gian
hợp lý; bên sử dụng dịch vụ phải trả tiền công theo phần dịch vụ mà bên
cung ứng dịch vụ đã thực hiện và bồi thường thiệt hại.
```

**[3] [Luật Kinh doanh bất động sản 29/2023/QH15 — bản Word cung cấp](https://vanban.chinhphu.vn/?classid=1&docid=209624&pageid=27160&typegroupid=3)**

Điều 46. Nội dung chính của hợp đồng trong kinh doanh bất động sản | Khoản 4 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_corpus_v7_20261005/broker29-word.json

```text
4. Hợp đồng kinh doanh dịch vụ bất động sản phải có các nội dung chính sau đây:

a) Tên, địa chỉ của các bên;

b) Đối tượng và nội dung dịch vụ;

c) Yêu cầu và kết quả dịch vụ;

d) Thời hạn thực hiện dịch vụ;

đ) Phí dịch vụ, thù lao, hoa hồng dịch vụ;

e) Phương thức và thời hạn thanh toán;

g) Quyền, nghĩa vụ của các bên;

h) Phương thức giải quyết tranh chấp;

i) Thời điểm có hiệu lực của hợp đồng.
```

**[4] [Bộ luật Dân sự 91/2015/QH13 — Word do cơ quan nhà nước công bố](https://congan.daklak.gov.vn/laws/detail/Bo-luat-Dan-su-163/)**

Điều 513. Hợp đồng dịch vụ · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_repair_corpus_v14_20261006/civil91-word.json

```text
Điều 513. Hợp đồng dịch vụ

Hợp đồng dịch vụ là sự thỏa thuận giữa các bên, theo đó bên cung ứng dịch
vụ thực hiện công việc cho bên sử dụng dịch vụ, bên sử dụng dịch vụ phải
trả tiền dịch vụ cho bên cung ứng dịch vụ.
```

**[5] [Bộ luật Dân sự 91/2015/QH13 — Word do cơ quan nhà nước công bố](https://congan.daklak.gov.vn/laws/detail/Bo-luat-Dan-su-163/)**

Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_repair_corpus_v14_20261006/civil91-word.json

```text
Điều 117. Điều kiện có hiệu lực của giao dịch dân sự | Khoản 1
1. Giao dịch dân sự có hiệu lực khi có đủ các điều kiện sau đây:

a) Chủ thể có năng lực pháp luật dân sự, năng lực hành vi dân sự phù hợp
với giao dịch dân sự được xác lập;

b) Chủ thể tham gia giao dịch dân sự hoàn toàn tự nguyện;

c) Mục đích và nội dung của giao dịch dân sự không vi phạm điều cấm của
luật, không trái đạo đức xã hội.

Điều 117. Điều kiện có hiệu lực của giao dịch dân sự | Khoản 2
2. Hình thức của giao dịch dân sự là điều kiện có hiệu lực của giao dịch
dân sự trong trường hợp luật có quy định.
```

### Lỗi và giới hạn đã ghi nhận

```json
{
  "collect": null,
  "ragas": {},
  "unavailable": null,
  "degraded": [
    "Phản hồi chưa đáp ứng đầy đủ yêu cầu chính; đánh dấu theo nội dung thay vì provider."
  ]
}
```


## Câu 47 · Nền tảng đăng tin

Khi tìm phòng qua một nền tảng trực tuyến, tôi nên kiểm tra người đăng và nguồn tin như thế nào?

Trạng thái: Đã trả lời · cần rà nguồn. Provider: gemini-agent; model: gemini-3.8-flash-high.

faithfulness: 1.0 | answer_relevancy: 0.8767 | context_utilization: 1.0 | context_recall: 0.75 | context_precision: 0.75

ID nguồn chuẩn: supplement-s01-word.json, supplement-s09-word.json, supplement-s11-word.json, supplement-s12-word.json

ID nguồn đã truy xuất: supplement-s09-word.json, google-lens-word.json, supplement-s12-word.json, supplement-s01-word.json

Khuyến nghị người thuê kiểm tra tính xác thực của tài khoản, tra cứu số điện thoại, địa chỉ cụ thể và đối chiếu mức giá cùng hình ảnh trước khi giao dịch [1] [2] [3] [4].

- Khuyến nghị kiểm tra số điện thoại của người đăng qua tính năng xác thực trên nền tảng hoặc tra cứu trên Google, mạng xã hội và diễn đàn trực tuyến [1] [4].
- Khuyến nghị tra cứu địa chỉ cụ thể gồm số nhà, tên đường, phường, quận và hỏi thăm thực tế hoặc tìm hiểu thông tin mạng về địa điểm này [4].
- Khuyến nghị thận trọng trước các tin rao có giá rẻ bất thường so với mức giá chung cùng loại trên nền tảng [1] [4].
- Người dùng có thể dùng Google Ống kính để tìm trang web có hình ảnh hoặc hình ảnh tương tự nhằm đối chiếu nguồn ảnh gốc [2].
- Khuyến nghị cảnh giác với các thủ đoạn sao chép thông tin, dùng tương tác ảo để tạo lòng tin và thúc ép chuyển tiền đặt cọc giữ phòng [3].

Kết quả tìm kiếm hình ảnh tương tự chỉ là công cụ hỗ trợ đối chiếu, không tự chứng minh tin đăng là giả mạo hay xác thực tư cách người cho thuê [2].
Việc xác thực số điện thoại trên nền tảng không thay thế cho việc kiểm tra giấy tờ nhà và căn cước để xác nhận quyền sở hữu của người cho thuê [1] [4].

Hướng dẫn/khuyến cáo của Trợ Giúp Chợ Tốt Nhà Tốt; không phải điều luật. Xác thực số điện thoại không xác minh quyền sở hữu hay quyền cho thuê. Chính sách riêng không bảo đảm mọi tin đều đúng và không xác lập nghĩa vụ giống nhau cho mọi nền tảng.
Hướng dẫn công cụ Google Lens, không phải điều luật. Kết quả ảnh tương tự là đầu mối để đối chiếu, không tự chứng minh tin đăng giả hoặc danh tính người cho thuê.
Hướng dẫn/khuyến cáo của Cổng Thông tin điện tử Bộ Công an bài Công an tỉnh Tuyên Quang; không phải điều luật. Tình huống gốc là đặt khách sạn tại Tuyên Quang. Áp dụng tham khảo cho chứng cứ giao dịch trực tuyến, không gọi là vụ thuê trọ CTU; không phải danh mục hồ sơ bắt buộc hoặc hướng dẫn soạn đơn tập thể.
Hướng dẫn/khuyến cáo của Trợ Giúp Chợ Tốt; không phải điều luật. Mẹo giao dịch, không phải điều luật. Không chứng minh hạn hoàn cọc cố định hoặc mức cọc bắt buộc; không thay thế xác minh người được ủy quyền cho thuê. Chỉ đọc phần kiểm tra, không bổ sung mẫu soạn hợp đồng.

### Nguồn và ngữ cảnh

**[1] [Nhà Tốt bảo vệ người dùng như thế nào — Trợ Giúp Chợ Tốt Nhà Tốt](https://trogiup.chotot.com/nguoi-mua/nha-tot-bao-ve-nguoi-dung-nhu-the-nao/)**

Nhà Tốt bảo vệ người dùng như thế nào | Đoạn nguyên văn 75 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_supplement_corpus_v8_20261005/supplement-s09-word.json

```text
Trong thời gian gần đây, Nền tảng Công nghệ Bất động sản Nhà Tốt nhận thấy tình trạng lừa đảo để trục lợi trên các nền tảng công nghệ ngày càng gia tăng và có xu hướng trở nên tinh vi. Hơn 10 năm đồng hành cùng người dùng Việt, Nhà Tốt luôn nỗ lực để tạo môi trường mua bán Bất Động Sản (BĐS) trực tuyến an toàn, tự do và hiệu quả. Bên cạnh việc tạo nên môi trường mua bán, giao dịch tự do, công bằng giữa Người mua và Người bán, thì Nhà Tốt luôn đặt sự an toàn của Người dùng lên hàng đầu. Vì vậy, về phía Nhà Tốt đã áp dụng nhiều biện pháp nhằm đảm bảo quyền lợi và gia tăng sự bảo vệ cho người dùng như sau:

1. Xây dựng quy trình Kiểm duyệt tin, phát triển các tính năng hỗ trợ mua bán nhanh chóng an toàn

Xác thực số điện thoại cho mỗi tài khoản đăng tin: nhằm tăng cường tính bảo mật tài khoản và tính xác thực cho mỗi người dùng trên Nhà Tốt.

Loại bỏ tin rác, tin trùng lặp: Giúp người mua tìm được sản phẩm nhanh hơn.

Loại bỏ sản phẩm có giá thấp đáng ngờ: Các tin rao có giá quá rẻ thường đi kèm với chất lượng không đảm bảo và khả năng người bán lừa đảo.

2. Hỗ trợ người dùng tức thời thông qua các kênh Chăm sóc Khách hàng

Khi có vấn đề cần hỗ trợ, người dùng có thể liên hệ bộ phận Chăm sóc Khách hàng của Nhà Tốt qua các kênh sau:

Báo tin/người dùng vi phạm: Tính năng “Báo cáo tin đăng” hiển thị bên dưới mỗi tin đăng giúp người dùng thông báo ngay các tin đăng/người dùng vi phạm để Nhà Tốt kiểm tra & xử lý kịp thời.

Chat trực tiếp tại đây. (Thời gian hỗ trợ từ 8h-12h và 13h-17h hàng ngày).

Đường dây nóng: 19003003 (Thời gian hỗ trợ từ 08h-12h và 13h-17h từ thứ 2 đến thứ 6 hàng tuần).

Gửi email về [email protected].

Nhà Tốt cam kết hòm thư CSKH hoạt động 24/7 để tiếp nhận các thắc mắc của người dùng.

3. Truyền thông và cảnh báo người dùng, hợp tác chặt chẽ với cơ quan điều tra đối tượng vi phạm

Nhà Tốt thường xuyên gửi các mẹo giao dịch an toàn đến người dùng qua các kênh như Thông báo trên ứng dụng, Email, Fanpage … giúp người dùng cẩn trọng hơn trong quá trình giao dịch.

Nhà Tốt sẵn sàng cung cấp thông tin các đối tượng có dấu hiệu vi phạm đến các tổ chức điều tra/cơ quan nhà nước có thẩm quyền để hỗ trợ quá trình điều tra/xử lý các đối tượng vi phạm.
```

**[2] [Google Lens: kiểm tra nguồn hình ảnh — Google Search Help](https://support.google.com/websearch/answer/1325808?co=GENIE.Platform%3DDesktop&hl=vi)**

Google Lens — tìm ảnh và trang chứa ảnh tương tự · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_focus3_corpus_v10_20261006/google-lens-word.json

```text
Trang web có hình ảnh đó hoặc có hình ảnh tương tự

nhấp vào Tìm bằng Google Ống kính.
```

**[3] [Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 — Cổng Thông tin điện tử Bộ Công an bài Công an tỉnh Tuyên Quang](https://bocongan.gov.vn/bai-viet/canh-giac-thu-doan-lua-dao-mao-danh-fanpage-khach-san-nha-hang-dat-coc-truc-tuyen-dip-le-hoi-thanh-tuyen-2026-1790041513)**

Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 | Đoạn nguyên văn 12 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_supplement_corpus_v8_20261005/supplement-s12-word.json

```text
Để tạo lòng tin, chúng sao chép hình ảnh, logo, địa chỉ, số điện thoại, nội dung giới thiệu từ trang thật; sử dụng tương tác ảo, tài khoản giả để bình luận tích cực, đánh giá 5 sao. Một số fanpage còn chạy quảng cáo trả phí để tiếp cận người có nhu cầu du lịch.

Khi khách liên hệ, các đối tượng tư vấn nhanh, đưa ra giá thấp hơn thị trường, kèm khuyến mãi “giới hạn” nhằm thúc ép chuyển tiền đặt cọc hoặc thanh toán trước để “giữ phòng”. Sau đó, chúng có thể gửi xác nhận đặt phòng giả, hoặc tiếp tục yêu cầu khách chuyển thêm tiền với lý do sai nội dung chuyển khoản, cần “kế toán xác nhận” để hoàn tiền. Sau nhiều lần nhận tiền, các đối tượng chặn liên lạc, chiếm đoạt toàn bộ số tiền. Nạn nhân thường chỉ phát hiện bị lừa khi đến nơi lưu trú, cơ sở dịch vụ nhưng không có thông tin đặt phòng nào được ghi nhận.

Cơ quan Công an khuyến cáo người dân và du khách cần nâng cao cảnh giác, thực hiện nghiêm túc các quy tắc xác minh thông tin trước khi thực hiện giao dịch chuyển tiền.

Khi phát hiện các Fanpage có dấu hiệu giả mạo, lừa đảo, lập tức thực hiện thao tác "Báo cáo" (Report) trang đó với nền tảng Facebook, đồng thời lưu lại bằng chứng (hình ảnh tin nhắn, tài khoản ngân hàng, phiếu giao dịch).

Khi nghi ngờ hoặc trở thành nạn nhân của các thủ đoạn lừa đảo trực tuyến, người dân cần nhanh chóng thu thập toàn bộ chứng cứ và báo ngay cho Cơ quan Công an nơi gần nhất để được hướng dẫn, tiếp nhận và xử lý kịp thời theo đúng quy định của pháp luật.
```

**[4] [Mẹo khi thuê phòng — Trợ Giúp Chợ Tốt](https://trogiup.chotot.com/nguoi-mua/meo-khi-thue-phong/)**

Mẹo khi thuê phòng | Đoạn nguyên văn 78 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_supplement_corpus_v8_20261005/supplement-s01-word.json

```text
1. Kiểm tra độ uy tín của người cho thuê trên môi trường trực tuyến (Google, Facebook, diễn đàn, …)

Tìm kiếm số điện thoại và địa chỉ muốn thuê trên Google, Facebook, các diễn đàn trực tuyến, … và xem các thông tin giao dịch trước đó như đánh giá của khách hàng về địa chỉ thuê này, …

2. Xác định địa điểm phòng muốn thuê và khảo sát mức giá chung

Tìm hiểu cụ thể địa chỉ muốn thuê gồm số nhà, tên đường, phường, quận.

Hỏi thăm trực tiếp hàng xóm xung quanh địa điểm muốn thuê và tham khảo ý kiến từ người thân, bạn bè hoặc tìm hiểu thông tin trên mạng về địa điểm này.

Mỗi khu vực sẽ có giá thuê khác nhau. Do đó, cần tìm hiểu mức giá chung theo từng khu vực trước khi thuê bằng cách so sánh với các tin đăng bất động sản cùng loại trên Chợ Tốt.

Thận trọng khi tìm được phòng ở trung tâm hoặc phòng tốt nhưng giá rẻ bất thường.

3. Không đặt cọc nếu chưa xác định được chủ nhà

Yêu cầu gặp trực tiếp chủ nhà trước khi đặt cọc.

Yêu cầu chủ nhà cho xem giấy tờ nhà và thẻ Căn Cước/thẻ Căn Cước Công Dân để xác nhận quyền sở hữu của chủ nhà

Nên chủ động hỏi kỹ về giá phòng, giá điện nước, các chi phí khác (nếu có) và các điều kiện sinh hoạt khác trước khi đặt cọc.

4. Phải đọc kỹ hợp đồng đặt cọc và hợp đồng thuê

Khi làm hợp đồng thuê cần đọc kỹ các điều khoản ghi trên hợp đồng: địa chỉ phòng, số phòng, tiền phòng cố định trong bao lâu không thay đổi, số người thuê, tiền điện, tiền nước, tiền gửi xe, sử dụng Internet và các chi phí phát sinh khác (nếu có).

Làm rõ các điều khoản về thời hạn hợp đồng và tiền đặt cọc trong trường hợp kết thúc hợp đồng trước hạn.

Luôn giữ tối thiểu một bản chính biên nhận đặt cọc và hợp đồng thuê.

5. Kiểm tra tình trạng phòng thuê trước khi đến ở

Kiểm tra tình trạng các thiết bị trong nhà và hệ thống đường điện, nước. Nếu có vấn đề hỏng hóc thì phải yêu cầu chủ nhà trọ sửa chữa hoặc thay thế.

Thống nhất số điện/nước (internet nếu có) phải trả ngay khi làm hợp đồng để tránh trường hợp phải trả thêm lượng điện/nước (internet nếu có) đã tiêu thụ trước đó.

Những trường hợp gian lận cần cảnh giác

Yêu cầu khách thuê đặt tiền cọc sau đó lật ngược những thỏa thuận ban đầu, thu thêm hàng loạt phí… là những trường hợp được người đi thuê cảnh báo:
```


## Câu 48 · Nền tảng đăng tin

Nếu một tin đăng nhà trọ có thông tin sai, tôi có thể báo cáo cho nền tảng bằng cách nào?

Trạng thái: Trả lời một phần. Provider: gemini-agent; model: gemini-3.8-flash-high.

faithfulness: 0.871 | answer_relevancy: 0.9195 | context_utilization: 1.0 | context_recall: 1.0 | context_precision: 1.0

ID nguồn chuẩn: supplement-s08-word.json, nhatot-report-proof-word.json, supplement-s16-word.json

ID nguồn đã truy xuất: supplement-s08-word.json, nhatot-report-proof-word.json, supplement-s16-word.json

Người dùng có thể báo cáo tin đăng có thông tin sai lệch qua nút báo cáo trực tiếp dưới tin đăng hoặc liên hệ qua kênh hỗ trợ của nền tảng [1].

- Trên Chợ Tốt, bạn chọn tin đăng cần báo cáo, bấm nút Báo cáo tin đăng bên dưới nội dung tin, chọn lý do như Thông tin không đúng thực tế, điền thông tin rồi chọn Gửi [1].
- Bạn có thể liên hệ trực tiếp qua trò chuyện trực tuyến trên trang hoặc gửi email hỗ trợ công bố trên nền tảng gồm link tin, lý do và số điện thoại liên hệ [1].
- Khuyến nghị cung cấp thêm thông tin hoặc hình ảnh trao đổi với người đăng thể hiện hành vi vi phạm nếu có theo hướng dẫn của Nhà Tốt [2].
- Theo quy định, nền tảng thương mại điện tử phải công khai phương thức tiếp nhận và xử lý phản ánh, bao gồm ít nhất một phương thức trực tuyến cùng thời hạn giải quyết [3].

Thời hạn xử lý 24 giờ của nền tảng áp dụng khi có yêu cầu của cơ quan nhà nước có thẩm quyền chứ không phải cam kết xử lý mọi báo cáo của người dùng trong 24 giờ [3].
Các bước thao tác cụ thể là hướng dẫn trên Chợ Tốt và Nhà Tốt, có thể khác biệt tùy theo giao diện của từng trang giao dịch [1] [2].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng.
Cần đối chiếu điều/khoản được dẫn chiếu còn thiếu; đoạn trích chưa đủ để kết luận toàn bộ điều kiện và ngoại lệ.
Hướng dẫn/khuyến cáo của Trợ Giúp Chợ Tốt; không phải điều luật. Đây là thao tác trên Chợ Tốt; vị trí nút có thể thay đổi. Báo cáo nền tảng không thay thế việc báo cơ quan có thẩm quyền khi có dấu hiệu chiếm đoạt.
Hướng dẫn của Nhà Tốt về hình ảnh trao đổi giúp làm rõ phản ánh tin/người bán vi phạm; không phải điều luật hoặc thời hạn xử lý. Trang nguồn có bối cảnh mua bất động sản; chỉ dùng phần phản ánh tin, không suy sang thủ tục mua bán hoặc quyền trong hợp đồng thuê.
Văn bản TMĐT có hiệu lực 01/07/2026; phải đọc đúng loại nền tảng và điều khoản chuyển tiếp. Điều 52 khoản 2: quy định xác thực điện tử áp dụng từ 01/01/2027, chưa áp dụng ở ngày 05/10/2026.

### Nguồn và ngữ cảnh

**[1] [Làm thế nào để báo cáo tin đăng — Trợ Giúp Chợ Tốt](https://trogiup.chotot.com/nguoi-mua/lam-the-nao-de-bao-cao-tin-dang/)**

Làm thế nào để báo cáo tin đăng | Đoạn nguyên văn 93 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_supplement_corpus_v8_20261005/supplement-s08-word.json

```text
TRÊN TRÌNH DUYỆT WEB MÁY TÍNH

Cách 1: Thông báo trực tiếp trên website

Bước 1: Chọn tin mà bạn muốn báo cáo.

Bước 2: Chọn Báo cáo tin đăng bên dưới nội dung tin.

Bước 3: Chọn lý do báo cáo tin đăng.

Lừa đảo: Tin đăng không trung thực (sản phẩm không chất lượng không giống như tin đăng miêu tả hoặc trường hợp chuyển tiền nhưng người bán không giao hàng).

Trùng lặp: Nội dung, hình ảnh tin đăng này trùng lặp với tin đăng khác.

Hàng đã bán: Mặt hàng đã giao dịch thành công.

Không liên lạc được: Số điện thoại của người bán không liên lạc được.

Thông tin không đúng thực tế: Thông tin miêu tả sản phẩm không đúng với thực tế hoặc sản phẩm không có thực.

Bước 4: Điền đầy đủ thông tin cần cung cấp cho từng lý do báo cáo tin đăng. Sau đó, chọn Gửi.

Cách 2: Liên hệ với Chợ Tốt

Qua chức năng trò chuyện trực tuyến tại đây (Thời gian hỗ trợ từ 08h-12h và 13h – 17h hằng ngày).

Gửi thông tin báo sai phạm qua email về [email protected]. Khi gửi thông tin cần lưu ý cung cấp những thông tin sau: Đường link của tin nghi ngờ không hợp lệ. Lý do bạn cho rằng tin này không hợp lệ. Số điện thoại của bạn để Chợ Tốt có thể liên lạc và tìm hiểu kỹ hơn về vấn đề này.

Đường link của tin nghi ngờ không hợp lệ.

Lý do bạn cho rằng tin này không hợp lệ.

Số điện thoại của bạn để Chợ Tốt có thể liên lạc và tìm hiểu kỹ hơn về vấn đề này.
```

**[2] [Nhà Tốt: hình ảnh trao đổi hỗ trợ phản ánh tin vi phạm](https://trogiup.chotot.com/nguoi-mua/bi-quyet-mua-bat-dong-san-an-toan-voi-nha-tot/)**

Hình ảnh trao đổi khi phản ánh tin đăng/người bán vi phạm · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_focus3_corpus_v11_20261006/nhatot-report-proof-word.json

```text
Thông tin (hình ảnh) trao đổi mua bán của bạn với người bán thể hiện hành vi vi phạm (nếu có).
```

**[3] [Nghị định 248/2026/NĐ-CP hướng dẫn Luật Thương mại điện tử — Chính phủ Công báo Chính phủ](https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-248-2026-nd-cp-469983.htm)**

Điều 17. Trách nhiệm của chủ quản nền tảng thương mại điện tử | Khoản 1 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_priority7_corpus_v13_20261006/supplement-s16-word.json

```text
1. Chủ quản nền tảng thương mại điện tử thực hiện các trách nhiệm quy định tại Điều 15 của Luật Thương mại điện tử, trong đó một số nội dung được thực hiện cụ thể như sau:

a) Công bố đầy đủ, chính xác, rõ ràng các nội dung hoặc có đường liên kết để xem chi tiết các nội dung quy định tại Chương II của Nghị định này tại vị trí trên màn hình chính của nền tảng thương mại điện tử và có dấu hiệu phân biệt rõ ràng; 

b) Báo cáo trực tuyến định kỳ thông qua Hệ thống quản lý hoạt động thương mại điện tử thực hiện theo quy định tại khoản 1 Điều 22 của Nghị định này hoặc cung cấp thông tin theo yêu cầu của cơ quan nhà nước có thẩm quyền;

c) Có biện pháp kiểm tra, rà soát, gỡ bỏ và xử lý kịp thời đối với thông tin hàng hóa, dịch vụ xâm phạm quyền sở hữu trí tuệ, hàng hóa, dịch vụ liên quan đến hành vi kinh doanh vi phạm pháp luật trong thời hạn 24 giờ kể từ khi nhận được yêu cầu của cơ quan nhà nước có thẩm quyền;

d) Cập nhật từ khóa theo khuyến cáo từ cơ quan nhà nước có thẩm quyền và lọc thông tin theo từ khóa trước khi thông tin hàng hóa, dịch vụ hiển thị trên nền tảng thương mại điện tử;

đ) Duy trì, sử dụng tài khoản đã thực hiện thủ tục hành chính tại Hệ thống quản lý hoạt động thương mại điện tử để tiếp nhận và phản hồi thông tin nhằm giải quyết khiếu nại, phản ánh và tranh chấp liên quan đến nền tảng thương mại điện tử;

e) Phối hợp với chủ thể quyền sở hữu trí tuệ rà soát, tạm thời gỡ bỏ hoặc ngăn chặn truy cập đến thông tin hàng hóa, dịch vụ có dấu hiệu xâm phạm quyền sở hữu trí tuệ theo phương thức tiếp nhận và giải quyết phản ánh, yêu cầu, khiếu nại đã công khai trên nền tảng theo quy định tại Điều 7 của Nghị định này.

Điều 7. Phương thức tiếp nhận và giải quyết phản ánh, yêu cầu, khiếu nại
Phương thức tiếp nhận và xử lý phản ánh, yêu cầu, khiếu nại bao gồm ít nhất các nội dung sau đây:

Điều 7. Phương thức tiếp nhận và giải quyết phản ánh, yêu cầu, khiếu nại | Khoản 1
Phương thức tiếp nhận và xử lý phản ánh, yêu cầu, khiếu nại bao gồm ít nhất các nội dung sau đây:

1. Các phương thức tiếp nhận phản ánh, yêu cầu, khiếu nại, bao gồm ít nhất một phương thức liên hệ trực tuyến;

Điều 7. Phương thức tiếp nhận và giải quyết phản ánh, yêu cầu, khiếu nại | Khoản 2
Phương thức tiếp nhận và xử lý phản ánh, yêu cầu, khiếu nại bao gồm ít nhất các nội dung sau đây:

2. Trình tự, thủ tục tiếp nhận và xử lý phản ánh, yêu cầu, khiếu nại, bao gồm các bước cụ thể mà các bên cần thực hiện;

Điều 7. Phương thức tiếp nhận và giải quyết phản ánh, yêu cầu, khiếu nại | Khoản 3
Phương thức tiếp nhận và xử lý phản ánh, yêu cầu, khiếu nại bao gồm ít nhất các nội dung sau đây:

3. Thời hạn cụ thể phản hồi ban đầu và thời hạn dự kiến giải quyết cho từng loại vấn đề phổ biến;

Điều 7. Phương thức tiếp nhận và giải quyết phản ánh, yêu cầu, khiếu nại | Khoản 4
Phương thức tiếp nhận và xử lý phản ánh, yêu cầu, khiếu nại bao gồm ít nhất các nội dung sau đây:

4. Các biện pháp, công cụ mà nền tảng áp dụng để hỗ trợ giải quyết phản ánh, yêu cầu, khiếu nại.
```

**[4] [Nghị định 248/2026/NĐ-CP hướng dẫn Luật Thương mại điện tử — Chính phủ Công báo Chính phủ](https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-248-2026-nd-cp-469983.htm)**

Điều 18. Trách nhiệm của chủ quản nền tảng thương mại điện tử trung gian | Khoản 2 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_priority7_corpus_v13_20261006/supplement-s16-word.json

```text
2. Chủ quản nền tảng thương mại điện tử trung gian có chức năng đặt hàng trực tuyến thực hiện các trách nhiệm quy định tại khoản 2 Điều 17 của Luật Thương mại điện tử, trong đó một số nội dung được thực hiện cụ thể như sau:

a) Trách nhiệm quy định tại khoản 1 Điều này;

b) Tiếp nhận lại hàng hóa đối với trường hợp hàng hóa do người bán cung cấp không theo đúng nội dung đã thông báo, công bố, niêm yết, quảng cáo, giới thiệu, giao kết, cam kết trên nền tảng và thực hiện đổi trả hàng, hoàn tiền theo chính sách đã công bố trên nền tảng theo quy định tại Điều 14 của Nghị định này;

c) Công khai đầy đủ thông tin về việc thu hồi hàng hóa có khuyết tật trên nền tảng ngay khi nhận được thông tin từ người bán hoặc cơ quan nhà nước có thẩm quyền trong vòng 10 ngày liên tục tại một vị trí dễ thấy; công khai thông tin liên hệ của đầu mối tiếp nhận lại hàng hóa; thông tin trực tiếp đến người mua hàng hóa đó trên nền tảng thông qua tài khoản của người mua trên nền tảng hoặc kênh liên hệ khác phù hợp mà người mua đã đăng ký trên nền tảng; 

d) Cung cấp các thông tin cần thiết hỗ trợ các bên có tham gia giao dịch trên nền tảng theo phương thức tiếp nhận và giải quyết phản ánh, yêu cầu, khiếu nại đã công khai theo quy định tại Điều 7 của Nghị định này; cung cấp các thông tin cho cơ quan nhà nước có thẩm quyền về các hành vi có dấu hiệu vi phạm pháp luật hoặc hành vi vi phạm pháp luật thông qua đầu mối được chỉ định và thông qua Hệ thống quản lý hoạt động thương mại điện tử trong thời hạn 24 giờ kể từ thời điểm tiếp nhận yêu cầu để phục vụ công tác thanh tra, kiểm tra, xử lý vi phạm;

đ) Cung cấp công cụ để người bán truy cập tài khoản để tải về dữ liệu về hàng hóa, dịch vụ đã đăng tải trong vòng 01 năm từ thời điểm đăng tải, dữ liệu về hợp đồng giao kết trong vòng 03 năm kể từ thời điểm giao kết hợp đồng, trừ trường hợp người bán chủ động xóa tài khoản. Trường hợp tài khoản người bán bị tạm ngừng hoặc chấm dứt hoạt động, chủ quản nền tảng bảo đảm cho người bán có thể truy cập tài khoản hoặc phương thức khác để tải dữ liệu về hợp đồng giao kết đã thực hiện trước đó trong thời gian ít nhất 03 năm từ thời điểm tài khoản bị tạm ngừng hoặc chấm dứt hoạt động;

e) Tạm ngừng, chấm dứt tài khoản người bán trong thời hạn 24 giờ kể từ khi nhận được yêu cầu của cơ quan nhà nước có thẩm quyền.

Điều 7. Phương thức tiếp nhận và giải quyết phản ánh, yêu cầu, khiếu nại
Phương thức tiếp nhận và xử lý phản ánh, yêu cầu, khiếu nại bao gồm ít nhất các nội dung sau đây:

Điều 7. Phương thức tiếp nhận và giải quyết phản ánh, yêu cầu, khiếu nại | Khoản 1
Phương thức tiếp nhận và xử lý phản ánh, yêu cầu, khiếu nại bao gồm ít nhất các nội dung sau đây:

1. Các phương thức tiếp nhận phản ánh, yêu cầu, khiếu nại, bao gồm ít nhất một phương thức liên hệ trực tuyến;

Điều 7. Phương thức tiếp nhận và giải quyết phản ánh, yêu cầu, khiếu nại | Khoản 2
Phương thức tiếp nhận và xử lý phản ánh, yêu cầu, khiếu nại bao gồm ít nhất các nội dung sau đây:

2. Trình tự, thủ tục tiếp nhận và xử lý phản ánh, yêu cầu, khiếu nại, bao gồm các bước cụ thể mà các bên cần thực hiện;

Điều 7. Phương thức tiếp nhận và giải quyết phản ánh, yêu cầu, khiếu nại | Khoản 3
Phương thức tiếp nhận và xử lý phản ánh, yêu cầu, khiếu nại bao gồm ít nhất các nội dung sau đây:

3. Thời hạn cụ thể phản hồi ban đầu và thời hạn dự kiến giải quyết cho từng loại vấn đề phổ biến;

Điều 7. Phương thức tiếp nhận và giải quyết phản ánh, yêu cầu, khiếu nại | Khoản 4
Phương thức tiếp nhận và xử lý phản ánh, yêu cầu, khiếu nại bao gồm ít nhất các nội dung sau đây:

4. Các biện pháp, công cụ mà nền tảng áp dụng để hỗ trợ giải quyết phản ánh, yêu cầu, khiếu nại.
```

**[5] [Nghị định 248/2026/NĐ-CP hướng dẫn Luật Thương mại điện tử — Chính phủ Công báo Chính phủ](https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-248-2026-nd-cp-469983.htm)**

Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_priority7_corpus_v13_20261006/supplement-s16-word.json

```text
Điều 52. Điều khoản thi hành | Khoản 1
1. Nghị định này có hiệu lực thi hành từ ngày 01 tháng 7 năm 2026, trừ trường hợp quy định tại khoản 2 Điều này.

Điều 52. Điều khoản thi hành | Khoản 2
2. Chủ quản nền tảng thương mại điện tử có trách nhiệm thực hiện việc xác thực điện tử danh tính người bán và người livestream bán hàng kể từ ngày 01 tháng 01 năm 2027.

Điều 52. Điều khoản thi hành | Khoản 3
3. Nghị định số 52/2013/NĐ-CP ngày 16 tháng 5 năm 2013 của Chính phủ về thương mại điện tử và Nghị định số 85/2021/NĐ-CP ngày 25 tháng 9 năm 2021 của Chính phủ sửa đổi, bổ sung một số điều của Nghị định số 52/2013/NĐ-CP ngày 16 tháng 5 năm 2013 của Chính phủ về thương mại điện tử hết hiệu lực thi hành kể từ ngày Nghị định này có hiệu lực, trừ trường hợp quy định tại Điều 53 của Nghị định này.

Điều 52. Điều khoản thi hành | Khoản 4
4. Sửa đổi cụm từ “cung cấp dịch vụ thương mại điện tử” thành “quản lý và vận hành nền tảng thương mại điện tử trung gian, mạng xã hội hoạt động thương mại điện tử, nền tảng thương mại điện tử tích hợp” tại Nghị định số 09/2018/NĐ-CP ngày 15 tháng 01 năm 2018 của Chính phủ quy định chi tiết Luật Thương mại và Luật Quản lý ngoại thương về hoạt động mua bán hàng hóa và các hoạt động liên quan trực tiếp đến mua bán hàng hóa của nhà đầu tư nước ngoài, tổ chức kinh tế có vốn đầu tư nước ngoài tại Việt Nam.

Điều 53. Quy định chuyển tiếp
Điều 53. Quy định chuyển tiếp

Nền tảng thương mại điện tử (website, ứng dụng) đã được xác nhận thông báo hoặc đăng ký hoạt động trước ngày 01 tháng 7 năm 2026 được tiếp tục hoạt động theo nội dung đã xác nhận đến hết ngày 30 tháng 6 năm 2027. Trong thời gian này, chủ quản nền tảng thực hiện thủ tục sửa đổi, bổ sung hồ sơ đã xác nhận theo quy định tại Nghị định này.
```

### Lỗi và giới hạn đã ghi nhận

```json
{
  "collect": null,
  "ragas": {},
  "unavailable": null,
  "degraded": [
    "Phản hồi chưa đáp ứng đầy đủ yêu cầu chính; đánh dấu theo nội dung thay vì provider."
  ]
}
```


## Câu 49 · Nền tảng đăng tin

Nền tảng đăng tin có trách nhiệm gì đối với thông tin người bán hoặc người cho thuê theo tài liệu hiện có?

Trạng thái: Trả lời một phần. Provider: gemini-agent; model: gemini-3.8-flash-high.

faithfulness: 0.7826 | answer_relevancy: 0.8735 | context_utilization: 1.0 | context_recall: 1.0 | context_precision: 1.0

ID nguồn chuẩn: supplement-s16-word.json

ID nguồn đã truy xuất: supplement-s16-word.json

Chủ quản nền tảng có trách nhiệm công khai thông tin người bán, lọc từ khóa, gỡ thông tin vi phạm, tiếp nhận phản ánh, cung cấp dữ liệu cho cơ quan nhà nước và thực hiện xác thực điện tử từ ngày 01 tháng 01 năm 2027 [1] [2] [3] [4].

- Chủ quản nền tảng trung gian phải công khai tên, địa điểm kinh doanh theo đăng ký của doanh nghiệp, hộ kinh doanh; tên, địa chỉ nơi đặt trụ sở của tổ chức; tên, địa chỉ cư trú của cá nhân bằng tiếng Việt hoặc ký tự La-tinh [2].
- Chủ quản nền tảng thương mại điện tử có trách nhiệm thực hiện xác thực điện tử danh tính người bán kể từ ngày 01 tháng 01 năm 2027 [2] [4].
- Nền tảng phải cập nhật từ khóa để lọc thông tin trước khi hiển thị, đồng thời kiểm tra, rà soát, gỡ bỏ và xử lý kịp thời thông tin hàng hóa, dịch vụ vi phạm pháp luật trong 24 giờ kể từ khi nhận được yêu cầu của cơ quan nhà nước có thẩm quyền [1].
- Chủ quản nền tảng phải tiếp nhận và phản hồi thông tin để giải quyết khiếu nại, phản ánh theo quy trình, phương thức đã công khai trên nền tảng [1].
- Nền tảng trung gian có chức năng đặt hàng trực tuyến phải cung cấp thông tin cho cơ quan nhà nước có thẩm quyền về các hành vi có dấu hiệu vi phạm trong thời hạn 24 giờ kể từ thời điểm tiếp nhận yêu cầu [3].

Nghị định 248/2026/NĐ-CP quy định trách nhiệm chung đối với người bán trên nền tảng thương mại điện tử, chưa nêu quy định riêng biệt cụ thể cho thông tin người cho thuê trọ [1] [2] [4].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng.
Cần đối chiếu điều/khoản được dẫn chiếu còn thiếu; đoạn trích chưa đủ để kết luận toàn bộ điều kiện và ngoại lệ.
Văn bản TMĐT có hiệu lực 01/07/2026; phải đọc đúng loại nền tảng và điều khoản chuyển tiếp. Điều 52 khoản 2: quy định xác thực điện tử áp dụng từ 01/01/2027, chưa áp dụng ở ngày 05/10/2026.

### Nguồn và ngữ cảnh

**[1] [Nghị định 248/2026/NĐ-CP hướng dẫn Luật Thương mại điện tử — Chính phủ Công báo Chính phủ](https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-248-2026-nd-cp-469983.htm)**

Điều 17. Trách nhiệm của chủ quản nền tảng thương mại điện tử | Khoản 1 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_priority7_corpus_v13_20261006/supplement-s16-word.json

```text
1. Chủ quản nền tảng thương mại điện tử thực hiện các trách nhiệm quy định tại Điều 15 của Luật Thương mại điện tử, trong đó một số nội dung được thực hiện cụ thể như sau:

a) Công bố đầy đủ, chính xác, rõ ràng các nội dung hoặc có đường liên kết để xem chi tiết các nội dung quy định tại Chương II của Nghị định này tại vị trí trên màn hình chính của nền tảng thương mại điện tử và có dấu hiệu phân biệt rõ ràng; 

b) Báo cáo trực tuyến định kỳ thông qua Hệ thống quản lý hoạt động thương mại điện tử thực hiện theo quy định tại khoản 1 Điều 22 của Nghị định này hoặc cung cấp thông tin theo yêu cầu của cơ quan nhà nước có thẩm quyền;

c) Có biện pháp kiểm tra, rà soát, gỡ bỏ và xử lý kịp thời đối với thông tin hàng hóa, dịch vụ xâm phạm quyền sở hữu trí tuệ, hàng hóa, dịch vụ liên quan đến hành vi kinh doanh vi phạm pháp luật trong thời hạn 24 giờ kể từ khi nhận được yêu cầu của cơ quan nhà nước có thẩm quyền;

d) Cập nhật từ khóa theo khuyến cáo từ cơ quan nhà nước có thẩm quyền và lọc thông tin theo từ khóa trước khi thông tin hàng hóa, dịch vụ hiển thị trên nền tảng thương mại điện tử;

đ) Duy trì, sử dụng tài khoản đã thực hiện thủ tục hành chính tại Hệ thống quản lý hoạt động thương mại điện tử để tiếp nhận và phản hồi thông tin nhằm giải quyết khiếu nại, phản ánh và tranh chấp liên quan đến nền tảng thương mại điện tử;

e) Phối hợp với chủ thể quyền sở hữu trí tuệ rà soát, tạm thời gỡ bỏ hoặc ngăn chặn truy cập đến thông tin hàng hóa, dịch vụ có dấu hiệu xâm phạm quyền sở hữu trí tuệ theo phương thức tiếp nhận và giải quyết phản ánh, yêu cầu, khiếu nại đã công khai trên nền tảng theo quy định tại Điều 7 của Nghị định này.

Điều 7. Phương thức tiếp nhận và giải quyết phản ánh, yêu cầu, khiếu nại
Phương thức tiếp nhận và xử lý phản ánh, yêu cầu, khiếu nại bao gồm ít nhất các nội dung sau đây:

Điều 7. Phương thức tiếp nhận và giải quyết phản ánh, yêu cầu, khiếu nại | Khoản 1
Phương thức tiếp nhận và xử lý phản ánh, yêu cầu, khiếu nại bao gồm ít nhất các nội dung sau đây:

1. Các phương thức tiếp nhận phản ánh, yêu cầu, khiếu nại, bao gồm ít nhất một phương thức liên hệ trực tuyến;

Điều 7. Phương thức tiếp nhận và giải quyết phản ánh, yêu cầu, khiếu nại | Khoản 2
Phương thức tiếp nhận và xử lý phản ánh, yêu cầu, khiếu nại bao gồm ít nhất các nội dung sau đây:

2. Trình tự, thủ tục tiếp nhận và xử lý phản ánh, yêu cầu, khiếu nại, bao gồm các bước cụ thể mà các bên cần thực hiện;

Điều 7. Phương thức tiếp nhận và giải quyết phản ánh, yêu cầu, khiếu nại | Khoản 3
Phương thức tiếp nhận và xử lý phản ánh, yêu cầu, khiếu nại bao gồm ít nhất các nội dung sau đây:

3. Thời hạn cụ thể phản hồi ban đầu và thời hạn dự kiến giải quyết cho từng loại vấn đề phổ biến;

Điều 7. Phương thức tiếp nhận và giải quyết phản ánh, yêu cầu, khiếu nại | Khoản 4
Phương thức tiếp nhận và xử lý phản ánh, yêu cầu, khiếu nại bao gồm ít nhất các nội dung sau đây:

4. Các biện pháp, công cụ mà nền tảng áp dụng để hỗ trợ giải quyết phản ánh, yêu cầu, khiếu nại.
```

**[2] [Nghị định 248/2026/NĐ-CP hướng dẫn Luật Thương mại điện tử — Chính phủ Công báo Chính phủ](https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-248-2026-nd-cp-469983.htm)**

Điều 18. Trách nhiệm của chủ quản nền tảng thương mại điện tử trung gian | Khoản 1 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_priority7_corpus_v13_20261006/supplement-s16-word.json

```text
1. Chủ quản nền tảng thương mại điện tử trung gian thực hiện các trách nhiệm quy định tại Điều 17 của Luật Thương mại điện tử, trong đó một số nội dung được thực hiện cụ thể như sau:

a) Thực hiện việc xác thực điện tử danh tính người bán trong nước thông qua các thông tin sau đây:

Đối với cá nhân trong nước: họ và tên; ngày, tháng, năm sinh; số định danh cá nhân; 

Đối với tổ chức trong nước: tên tổ chức; địa chỉ trụ sở chính; số định danh của tổ chức; họ và tên, ngày, tháng, năm sinh, số định danh cá nhân của người đại diện theo pháp luật;

b) Thực hiện việc xác thực người bán nước ngoài thông qua các giấy tờ hợp pháp sau đây:

Đối với cá nhân nước ngoài: tên, số hộ chiếu, tên quốc gia, vùng lãnh thổ của cá nhân tại hộ chiếu hoặc các giấy tờ tương đương khác còn hiệu lực ít nhất 06 tháng kể từ ngày xét duyệt do cơ quan có thẩm quyền nước ngoài cấp;

Đối với tổ chức nước ngoài: tên tổ chức, địa chỉ trụ sở chính, tên quốc gia, vùng lãnh thổ của tổ chức tại Giấy chứng nhận đăng ký doanh nghiệp hoặc các giấy tờ tương đương khác do cơ quan có thẩm quyền nước ngoài cấp; tên, số hộ chiếu của người đại diện theo pháp luật hoặc các giấy tờ tương đương khác còn hiệu lực ít nhất 06 tháng kể từ ngày xét duyệt do cơ quan có thẩm quyền nước ngoài cấp;

c) Công khai thông tin về tên, địa điểm kinh doanh của doanh nghiệp, hộ kinh doanh theo nội dung đăng ký đã thực hiện với cơ quan đăng ký kinh doanh; tên, địa chỉ nơi đặt trụ sở của tổ chức; tên, địa chỉ cư trú của cá nhân. Các thông tin phải được phiên âm sang tiếng Việt hoặc thể hiện bằng ký tự La-tinh; 

d) Kiểm duyệt nội dung thông tin về hàng hóa, dịch vụ do người bán khởi tạo trước khi cho phép hiển thị trên nền tảng, bảo đảm thông tin không thuộc danh mục ngành, nghề cấm đầu tư kinh doanh, hàng hóa, dịch vụ đang bị tạm dừng lưu thông theo công bố của cơ quan nhà nước có thẩm quyền hoặc cập nhật từ khóa theo yêu cầu của cơ quan nhà nước có thẩm quyền;

đ) Bảo đảm khả năng truy cập thông tin và dữ liệu hàng hóa, dịch vụ đã đăng tải từ tài khoản người bán trong thời gian ít nhất 01 năm kể từ thời điểm đăng tải.
```

**[3] [Nghị định 248/2026/NĐ-CP hướng dẫn Luật Thương mại điện tử — Chính phủ Công báo Chính phủ](https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-248-2026-nd-cp-469983.htm)**

Điều 18. Trách nhiệm của chủ quản nền tảng thương mại điện tử trung gian | Khoản 2 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_priority7_corpus_v13_20261006/supplement-s16-word.json

```text
2. Chủ quản nền tảng thương mại điện tử trung gian có chức năng đặt hàng trực tuyến thực hiện các trách nhiệm quy định tại khoản 2 Điều 17 của Luật Thương mại điện tử, trong đó một số nội dung được thực hiện cụ thể như sau:

a) Trách nhiệm quy định tại khoản 1 Điều này;

b) Tiếp nhận lại hàng hóa đối với trường hợp hàng hóa do người bán cung cấp không theo đúng nội dung đã thông báo, công bố, niêm yết, quảng cáo, giới thiệu, giao kết, cam kết trên nền tảng và thực hiện đổi trả hàng, hoàn tiền theo chính sách đã công bố trên nền tảng theo quy định tại Điều 14 của Nghị định này;

c) Công khai đầy đủ thông tin về việc thu hồi hàng hóa có khuyết tật trên nền tảng ngay khi nhận được thông tin từ người bán hoặc cơ quan nhà nước có thẩm quyền trong vòng 10 ngày liên tục tại một vị trí dễ thấy; công khai thông tin liên hệ của đầu mối tiếp nhận lại hàng hóa; thông tin trực tiếp đến người mua hàng hóa đó trên nền tảng thông qua tài khoản của người mua trên nền tảng hoặc kênh liên hệ khác phù hợp mà người mua đã đăng ký trên nền tảng; 

d) Cung cấp các thông tin cần thiết hỗ trợ các bên có tham gia giao dịch trên nền tảng theo phương thức tiếp nhận và giải quyết phản ánh, yêu cầu, khiếu nại đã công khai theo quy định tại Điều 7 của Nghị định này; cung cấp các thông tin cho cơ quan nhà nước có thẩm quyền về các hành vi có dấu hiệu vi phạm pháp luật hoặc hành vi vi phạm pháp luật thông qua đầu mối được chỉ định và thông qua Hệ thống quản lý hoạt động thương mại điện tử trong thời hạn 24 giờ kể từ thời điểm tiếp nhận yêu cầu để phục vụ công tác thanh tra, kiểm tra, xử lý vi phạm;

đ) Cung cấp công cụ để người bán truy cập tài khoản để tải về dữ liệu về hàng hóa, dịch vụ đã đăng tải trong vòng 01 năm từ thời điểm đăng tải, dữ liệu về hợp đồng giao kết trong vòng 03 năm kể từ thời điểm giao kết hợp đồng, trừ trường hợp người bán chủ động xóa tài khoản. Trường hợp tài khoản người bán bị tạm ngừng hoặc chấm dứt hoạt động, chủ quản nền tảng bảo đảm cho người bán có thể truy cập tài khoản hoặc phương thức khác để tải dữ liệu về hợp đồng giao kết đã thực hiện trước đó trong thời gian ít nhất 03 năm từ thời điểm tài khoản bị tạm ngừng hoặc chấm dứt hoạt động;

e) Tạm ngừng, chấm dứt tài khoản người bán trong thời hạn 24 giờ kể từ khi nhận được yêu cầu của cơ quan nhà nước có thẩm quyền.

Điều 7. Phương thức tiếp nhận và giải quyết phản ánh, yêu cầu, khiếu nại
Phương thức tiếp nhận và xử lý phản ánh, yêu cầu, khiếu nại bao gồm ít nhất các nội dung sau đây:

Điều 7. Phương thức tiếp nhận và giải quyết phản ánh, yêu cầu, khiếu nại | Khoản 1
Phương thức tiếp nhận và xử lý phản ánh, yêu cầu, khiếu nại bao gồm ít nhất các nội dung sau đây:

1. Các phương thức tiếp nhận phản ánh, yêu cầu, khiếu nại, bao gồm ít nhất một phương thức liên hệ trực tuyến;

Điều 7. Phương thức tiếp nhận và giải quyết phản ánh, yêu cầu, khiếu nại | Khoản 2
Phương thức tiếp nhận và xử lý phản ánh, yêu cầu, khiếu nại bao gồm ít nhất các nội dung sau đây:

2. Trình tự, thủ tục tiếp nhận và xử lý phản ánh, yêu cầu, khiếu nại, bao gồm các bước cụ thể mà các bên cần thực hiện;

Điều 7. Phương thức tiếp nhận và giải quyết phản ánh, yêu cầu, khiếu nại | Khoản 3
Phương thức tiếp nhận và xử lý phản ánh, yêu cầu, khiếu nại bao gồm ít nhất các nội dung sau đây:

3. Thời hạn cụ thể phản hồi ban đầu và thời hạn dự kiến giải quyết cho từng loại vấn đề phổ biến;

Điều 7. Phương thức tiếp nhận và giải quyết phản ánh, yêu cầu, khiếu nại | Khoản 4
Phương thức tiếp nhận và xử lý phản ánh, yêu cầu, khiếu nại bao gồm ít nhất các nội dung sau đây:

4. Các biện pháp, công cụ mà nền tảng áp dụng để hỗ trợ giải quyết phản ánh, yêu cầu, khiếu nại.
```

**[4] [Nghị định 248/2026/NĐ-CP hướng dẫn Luật Thương mại điện tử — Chính phủ Công báo Chính phủ](https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-248-2026-nd-cp-469983.htm)**

Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_priority7_corpus_v13_20261006/supplement-s16-word.json

```text
Điều 52. Điều khoản thi hành | Khoản 1
1. Nghị định này có hiệu lực thi hành từ ngày 01 tháng 7 năm 2026, trừ trường hợp quy định tại khoản 2 Điều này.

Điều 52. Điều khoản thi hành | Khoản 2
2. Chủ quản nền tảng thương mại điện tử có trách nhiệm thực hiện việc xác thực điện tử danh tính người bán và người livestream bán hàng kể từ ngày 01 tháng 01 năm 2027.

Điều 52. Điều khoản thi hành | Khoản 3
3. Nghị định số 52/2013/NĐ-CP ngày 16 tháng 5 năm 2013 của Chính phủ về thương mại điện tử và Nghị định số 85/2021/NĐ-CP ngày 25 tháng 9 năm 2021 của Chính phủ sửa đổi, bổ sung một số điều của Nghị định số 52/2013/NĐ-CP ngày 16 tháng 5 năm 2013 của Chính phủ về thương mại điện tử hết hiệu lực thi hành kể từ ngày Nghị định này có hiệu lực, trừ trường hợp quy định tại Điều 53 của Nghị định này.

Điều 52. Điều khoản thi hành | Khoản 4
4. Sửa đổi cụm từ “cung cấp dịch vụ thương mại điện tử” thành “quản lý và vận hành nền tảng thương mại điện tử trung gian, mạng xã hội hoạt động thương mại điện tử, nền tảng thương mại điện tử tích hợp” tại Nghị định số 09/2018/NĐ-CP ngày 15 tháng 01 năm 2018 của Chính phủ quy định chi tiết Luật Thương mại và Luật Quản lý ngoại thương về hoạt động mua bán hàng hóa và các hoạt động liên quan trực tiếp đến mua bán hàng hóa của nhà đầu tư nước ngoài, tổ chức kinh tế có vốn đầu tư nước ngoài tại Việt Nam.

Điều 53. Quy định chuyển tiếp
Điều 53. Quy định chuyển tiếp

Nền tảng thương mại điện tử (website, ứng dụng) đã được xác nhận thông báo hoặc đăng ký hoạt động trước ngày 01 tháng 7 năm 2026 được tiếp tục hoạt động theo nội dung đã xác nhận đến hết ngày 30 tháng 6 năm 2027. Trong thời gian này, chủ quản nền tảng thực hiện thủ tục sửa đổi, bổ sung hồ sơ đã xác nhận theo quy định tại Nghị định này.
```

### Lỗi và giới hạn đã ghi nhận

```json
{
  "collect": null,
  "ragas": {},
  "unavailable": null,
  "degraded": [
    "Phản hồi chưa đáp ứng đầy đủ yêu cầu chính; đánh dấu theo nội dung thay vì provider."
  ]
}
```


## Câu 50 · Nền tảng đăng tin

Nếu người đăng yêu cầu chuyển cọc qua liên kết lạ, tôi nên kiểm tra những dấu hiệu nào trước khi trả tiền?

Trạng thái: Trả lời một phần. Provider: gemini-agent; model: gemini-3.8-flash-high.

faithfulness: 1.0 | answer_relevancy: 0.8617 | context_utilization: 1.0 | context_recall: 1.0 | context_precision: 0.75

ID nguồn chuẩn: online-secrets-1-word.json, supplement-s11-word.json, supplement-s12-word.json

ID nguồn đã truy xuất: supplement-s11-word.json, supplement-s12-word.json, online-secrets-1-word.json, supplement-s16-word.json

Khuyến nghị người thuê không truy cập đường link lạ và cảnh giác với các dấu hiệu thúc ép chuyển tiền đặt cọc giữ chỗ trước khi xác minh rõ ràng [1] [3].

- Khuyến nghị kiểm tra dấu hiệu đối tượng viện lý do phòng giá siêu rẻ, nhiều người hỏi thuê hoặc chủ vắng mặt để thúc ép chuyển cọc giữ chỗ trước khi đến xem phòng [1] [2].
- Khuyến nghị cảnh giác dấu hiệu trang sao chép hình ảnh, logo, địa chỉ, dùng tương tác ảo hoặc quảng cáo trả phí để tạo lòng tin [2].
- Khuyến nghị không cung cấp mã OTP, thông tin tài khoản ngân hàng, Căn cước công dân hoặc dữ liệu cá nhân qua tin nhắn hay liên kết chưa xác minh [1].
- Khuyến nghị không thực hiện bất kỳ giao dịch chuyển tiền nào theo hướng dẫn từ cá nhân, tổ chức chưa được xác minh rõ ràng [1].

Các dấu hiệu trên là khuyến cáo phòng ngừa rủi ro của cơ quan công an, không khẳng định mọi liên kết lạ đều là hành vi lừa đảo [1] [2] [3].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng.
Hướng dẫn/khuyến cáo của Cổng Thông tin điện tử Bộ Công an bài Công an TP Hải Phòng; không phải điều luật. Chỉ lấy phần thuê trọ và an toàn giao dịch; các thủ đoạn học phí, học bổng ngoài mục tiêu dự án. Không suy ra mọi tranh chấp cọc đều là tội phạm hay chắc chắn thu hồi được tiền.
Hướng dẫn/khuyến cáo của Cổng Thông tin điện tử Bộ Công an bài Công an tỉnh Tuyên Quang; không phải điều luật. Tình huống gốc là đặt khách sạn tại Tuyên Quang. Áp dụng tham khảo cho chứng cứ giao dịch trực tuyến, không gọi là vụ thuê trọ CTU; không phải danh mục hồ sơ bắt buộc hoặc hướng dẫn soạn đơn tập thể.
Khuyến cáo trong bối cảnh mua hàng/hoàn tiền trực tuyến, áp dụng tham khảo phòng ngừa; không kết luận mọi link lạ là lừa đảo hoặc tự chứng minh một vụ nhận cọc.

### Nguồn và ngữ cảnh

**[1] [Cảnh báo các thủ đoạn lừa đảo học sinh tân sinh viên mùa tựu trường — Cổng Thông tin điện tử Bộ Công an bài Công an TP Hải Phòng](https://bocongan.gov.vn/bai-viet/catp-hai-phong-canh-bao-cac-thu-doan-lua-dao-bua-vay-hoc-sinh-tan-sinh-vien-mua-tuu-truong-1787629964)**

Cảnh báo các thủ đoạn lừa đảo học sinh tân sinh viên mùa tựu trường | Đoạn nguyên văn 12 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_supplement_corpus_v8_20261005/supplement-s11-word.json

```text
- Bẫy "Phòng trọ giá rẻ, view đẹp"; Kẻ gian đăng tải thông tin cho thuê phòng trọ giá siêu rẻ, vị trí đẹp trên các hội nhóm. Khi liên hệ, chúng sẽ dùng nhiều lý do (nhiều người hỏi thuê, chủ đi vắng...) để yêu cầu chuyển tiền đặt cọc giữ chỗ trước khi đến xem phòng. Nhận được tiền, chúng lập tức chặn liên lạc.

Bảo mật thông tin cá nhân: Không cung cấp Căn cước công dân, Hộ chiếu, thông tin tài khoản ngân hàng, mã OTP hay bất kỳ dữ liệu cá nhân nào qua tin nhắn, số điện thoại hoặc email không thuộc hệ thống chính thức của trường.

Không tự ý chuyển tiền: Không thực hiện bất kỳ giao dịch chuyển tiền hay đóng lệ phí nào theo hướng dẫn từ các cá nhân, tổ chức chưa được xác minh rõ ràng.

Khi có nghi vấn, cần báo ngay cho cơ quan Công an gần nhất để được hướng dẫn và xử lý kịp thời./.
```

**[2] [Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 — Cổng Thông tin điện tử Bộ Công an bài Công an tỉnh Tuyên Quang](https://bocongan.gov.vn/bai-viet/canh-giac-thu-doan-lua-dao-mao-danh-fanpage-khach-san-nha-hang-dat-coc-truc-tuyen-dip-le-hoi-thanh-tuyen-2026-1790041513)**

Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 | Đoạn nguyên văn 12 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_supplement_corpus_v8_20261005/supplement-s12-word.json

```text
Để tạo lòng tin, chúng sao chép hình ảnh, logo, địa chỉ, số điện thoại, nội dung giới thiệu từ trang thật; sử dụng tương tác ảo, tài khoản giả để bình luận tích cực, đánh giá 5 sao. Một số fanpage còn chạy quảng cáo trả phí để tiếp cận người có nhu cầu du lịch.

Khi khách liên hệ, các đối tượng tư vấn nhanh, đưa ra giá thấp hơn thị trường, kèm khuyến mãi “giới hạn” nhằm thúc ép chuyển tiền đặt cọc hoặc thanh toán trước để “giữ phòng”. Sau đó, chúng có thể gửi xác nhận đặt phòng giả, hoặc tiếp tục yêu cầu khách chuyển thêm tiền với lý do sai nội dung chuyển khoản, cần “kế toán xác nhận” để hoàn tiền. Sau nhiều lần nhận tiền, các đối tượng chặn liên lạc, chiếm đoạt toàn bộ số tiền. Nạn nhân thường chỉ phát hiện bị lừa khi đến nơi lưu trú, cơ sở dịch vụ nhưng không có thông tin đặt phòng nào được ghi nhận.

Cơ quan Công an khuyến cáo người dân và du khách cần nâng cao cảnh giác, thực hiện nghiêm túc các quy tắc xác minh thông tin trước khi thực hiện giao dịch chuyển tiền.

Khi phát hiện các Fanpage có dấu hiệu giả mạo, lừa đảo, lập tức thực hiện thao tác "Báo cáo" (Report) trang đó với nền tảng Facebook, đồng thời lưu lại bằng chứng (hình ảnh tin nhắn, tài khoản ngân hàng, phiếu giao dịch).

Khi nghi ngờ hoặc trở thành nạn nhân của các thủ đoạn lừa đảo trực tuyến, người dân cần nhanh chóng thu thập toàn bộ chứng cứ và báo ngay cho Cơ quan Công an nơi gần nhất để được hướng dẫn, tiếp nhận và xử lý kịp thời theo đúng quy định của pháp luật.
```

**[3] [Cảnh báo bảo mật và liên kết lạ — Bộ Công an](https://www.bocongan.gov.vn/bai-viet/xuat-hien-thu-doan-lua-dao-moi-khi-mua-hang-online-1790562304)**

Cảnh báo bảo mật và liên kết lạ — Bộ Công an · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_repair_corpus_v14_20261006/online-secrets-1-word.json

```text
không truy cập đường link lạ
```

**[4] [Nghị định 248/2026/NĐ-CP hướng dẫn Luật Thương mại điện tử — Chính phủ Công báo Chính phủ](https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-248-2026-nd-cp-469983.htm)**

Điều 17. Trách nhiệm của chủ quản nền tảng thương mại điện tử | Khoản 1 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_priority7_corpus_v13_20261006/supplement-s16-word.json

```text
1. Chủ quản nền tảng thương mại điện tử thực hiện các trách nhiệm quy định tại Điều 15 của Luật Thương mại điện tử, trong đó một số nội dung được thực hiện cụ thể như sau:

a) Công bố đầy đủ, chính xác, rõ ràng các nội dung hoặc có đường liên kết để xem chi tiết các nội dung quy định tại Chương II của Nghị định này tại vị trí trên màn hình chính của nền tảng thương mại điện tử và có dấu hiệu phân biệt rõ ràng; 

b) Báo cáo trực tuyến định kỳ thông qua Hệ thống quản lý hoạt động thương mại điện tử thực hiện theo quy định tại khoản 1 Điều 22 của Nghị định này hoặc cung cấp thông tin theo yêu cầu của cơ quan nhà nước có thẩm quyền;

c) Có biện pháp kiểm tra, rà soát, gỡ bỏ và xử lý kịp thời đối với thông tin hàng hóa, dịch vụ xâm phạm quyền sở hữu trí tuệ, hàng hóa, dịch vụ liên quan đến hành vi kinh doanh vi phạm pháp luật trong thời hạn 24 giờ kể từ khi nhận được yêu cầu của cơ quan nhà nước có thẩm quyền;

d) Cập nhật từ khóa theo khuyến cáo từ cơ quan nhà nước có thẩm quyền và lọc thông tin theo từ khóa trước khi thông tin hàng hóa, dịch vụ hiển thị trên nền tảng thương mại điện tử;

đ) Duy trì, sử dụng tài khoản đã thực hiện thủ tục hành chính tại Hệ thống quản lý hoạt động thương mại điện tử để tiếp nhận và phản hồi thông tin nhằm giải quyết khiếu nại, phản ánh và tranh chấp liên quan đến nền tảng thương mại điện tử;

e) Phối hợp với chủ thể quyền sở hữu trí tuệ rà soát, tạm thời gỡ bỏ hoặc ngăn chặn truy cập đến thông tin hàng hóa, dịch vụ có dấu hiệu xâm phạm quyền sở hữu trí tuệ theo phương thức tiếp nhận và giải quyết phản ánh, yêu cầu, khiếu nại đã công khai trên nền tảng theo quy định tại Điều 7 của Nghị định này.

Điều 7. Phương thức tiếp nhận và giải quyết phản ánh, yêu cầu, khiếu nại
Phương thức tiếp nhận và xử lý phản ánh, yêu cầu, khiếu nại bao gồm ít nhất các nội dung sau đây:

Điều 7. Phương thức tiếp nhận và giải quyết phản ánh, yêu cầu, khiếu nại | Khoản 1
Phương thức tiếp nhận và xử lý phản ánh, yêu cầu, khiếu nại bao gồm ít nhất các nội dung sau đây:

1. Các phương thức tiếp nhận phản ánh, yêu cầu, khiếu nại, bao gồm ít nhất một phương thức liên hệ trực tuyến;

Điều 7. Phương thức tiếp nhận và giải quyết phản ánh, yêu cầu, khiếu nại | Khoản 2
Phương thức tiếp nhận và xử lý phản ánh, yêu cầu, khiếu nại bao gồm ít nhất các nội dung sau đây:

2. Trình tự, thủ tục tiếp nhận và xử lý phản ánh, yêu cầu, khiếu nại, bao gồm các bước cụ thể mà các bên cần thực hiện;

Điều 7. Phương thức tiếp nhận và giải quyết phản ánh, yêu cầu, khiếu nại | Khoản 3
Phương thức tiếp nhận và xử lý phản ánh, yêu cầu, khiếu nại bao gồm ít nhất các nội dung sau đây:

3. Thời hạn cụ thể phản hồi ban đầu và thời hạn dự kiến giải quyết cho từng loại vấn đề phổ biến;

Điều 7. Phương thức tiếp nhận và giải quyết phản ánh, yêu cầu, khiếu nại | Khoản 4
Phương thức tiếp nhận và xử lý phản ánh, yêu cầu, khiếu nại bao gồm ít nhất các nội dung sau đây:

4. Các biện pháp, công cụ mà nền tảng áp dụng để hỗ trợ giải quyết phản ánh, yêu cầu, khiếu nại.
```

**[5] [Nghị định 248/2026/NĐ-CP hướng dẫn Luật Thương mại điện tử — Chính phủ Công báo Chính phủ](https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-248-2026-nd-cp-469983.htm)**

Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_priority7_corpus_v13_20261006/supplement-s16-word.json

```text
Điều 52. Điều khoản thi hành | Khoản 1
1. Nghị định này có hiệu lực thi hành từ ngày 01 tháng 7 năm 2026, trừ trường hợp quy định tại khoản 2 Điều này.

Điều 52. Điều khoản thi hành | Khoản 2
2. Chủ quản nền tảng thương mại điện tử có trách nhiệm thực hiện việc xác thực điện tử danh tính người bán và người livestream bán hàng kể từ ngày 01 tháng 01 năm 2027.

Điều 52. Điều khoản thi hành | Khoản 3
3. Nghị định số 52/2013/NĐ-CP ngày 16 tháng 5 năm 2013 của Chính phủ về thương mại điện tử và Nghị định số 85/2021/NĐ-CP ngày 25 tháng 9 năm 2021 của Chính phủ sửa đổi, bổ sung một số điều của Nghị định số 52/2013/NĐ-CP ngày 16 tháng 5 năm 2013 của Chính phủ về thương mại điện tử hết hiệu lực thi hành kể từ ngày Nghị định này có hiệu lực, trừ trường hợp quy định tại Điều 53 của Nghị định này.

Điều 52. Điều khoản thi hành | Khoản 4
4. Sửa đổi cụm từ “cung cấp dịch vụ thương mại điện tử” thành “quản lý và vận hành nền tảng thương mại điện tử trung gian, mạng xã hội hoạt động thương mại điện tử, nền tảng thương mại điện tử tích hợp” tại Nghị định số 09/2018/NĐ-CP ngày 15 tháng 01 năm 2018 của Chính phủ quy định chi tiết Luật Thương mại và Luật Quản lý ngoại thương về hoạt động mua bán hàng hóa và các hoạt động liên quan trực tiếp đến mua bán hàng hóa của nhà đầu tư nước ngoài, tổ chức kinh tế có vốn đầu tư nước ngoài tại Việt Nam.

Điều 53. Quy định chuyển tiếp
Điều 53. Quy định chuyển tiếp

Nền tảng thương mại điện tử (website, ứng dụng) đã được xác nhận thông báo hoặc đăng ký hoạt động trước ngày 01 tháng 7 năm 2026 được tiếp tục hoạt động theo nội dung đã xác nhận đến hết ngày 30 tháng 6 năm 2027. Trong thời gian này, chủ quản nền tảng thực hiện thủ tục sửa đổi, bổ sung hồ sơ đã xác nhận theo quy định tại Nghị định này.
```

### Lỗi và giới hạn đã ghi nhận

```json
{
  "collect": null,
  "ragas": {},
  "unavailable": null,
  "degraded": [
    "Phản hồi chưa đáp ứng đầy đủ yêu cầu chính; đánh dấu theo nội dung thay vì provider."
  ]
}
```


## Câu 51 · Dữ liệu cá nhân

Chủ trọ có thể yêu cầu tôi cung cấp những thông tin cá nhân nào để làm hợp đồng và đăng ký cư trú?

Trạng thái: Đã trả lời · cần rà nguồn. Provider: gemini-agent; model: gemini-3.8-flash-high.

faithfulness: 0.8636 | answer_relevancy: 0.9046 | context_utilization: 1.0 | context_recall: 1.0 | context_precision: 1.0

ID nguồn chuẩn: privacy91-word.json, housing79-word.json, residence68-word.json

ID nguồn đã truy xuất: residence68-word.json, privacy91-word.json, housing79-word.json

Nguồn quy định hợp đồng về nhà ở yêu cầu họ tên cùng địa chỉ của các bên, còn hồ sơ tạm trú gồm tờ khai thay đổi thông tin cư trú và giấy tờ chứng minh chỗ ở hợp pháp [1] [3].

- Hợp đồng về nhà ở do các bên thỏa thuận phải lập thành văn bản và bao gồm họ và tên cá nhân, địa chỉ của các bên [3].
- Hồ sơ đăng ký tạm trú bao gồm tờ khai thay đổi thông tin cư trú và giấy tờ, tài liệu chứng minh chỗ ở hợp pháp [1].
- Trường hợp người đăng ký tạm trú là người chưa thành niên thì trong tờ khai phải ghi rõ ý kiến đồng ý của cha, mẹ hoặc người giám hộ, trừ khi đã có văn bản đồng ý [1].
- Sự đồng ý xử lý dữ liệu chỉ có hiệu lực khi người thuê tự nguyện và biết rõ loại dữ liệu, mục đích xử lý, bên kiểm soát/xử lý cùng quyền và nghĩa vụ của mình [2].

Nguồn trích tuyển chưa liệt kê toàn bộ các trường thông tin cá nhân chi tiết khác có thể thỏa thuận thêm ngoài họ tên và địa chỉ [3].

Điều 9 quy định nghĩa vụ công dân; Điều 10 quy định chủ hộ/thành viên hộ gia đình, không tự đồng nhất chủ trọ với chủ hộ. Chỉ giải thích trách nhiệm và giấy tờ cơ bản, không điền tờ khai hoặc hướng dẫn hồ sơ chuyên sâu. Điều 26 và 29 phải đọc đúng trường hợp điều chỉnh/xóa; không suy ra hạn nộp 30 ngày hoặc tự động xóa từ điều kiện sinh sống 30 ngày.
Nguồn là bản Word/trích tuyển được cung cấp, chưa xác minh toàn bộ câu chữ với bản chính thức; không coi ghi chú biên tập là quy định pháp luật.

### Nguồn và ngữ cảnh

**[1] [Luật Cư trú 68/2020/QH14 — Word Công báo](https://congbao.chinhphu.vn/van-ban/luat-so-68-2020-qh14-32684/33716.htm)**

Điều 28. Hồ sơ, thủ tục đăng ký tạm trú, gia hạn tạm trú | Khoản 1 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_repair_corpus_v16_20261006/residence68-word.json

```text
1. Hồ sơ đăng ký tạm trú bao gồm:
 a) Tờ khai thay đổi thông tin cư trú; đối với người đăng ký tạm trú là
người chưa thành niên thì trong tờ khai phải ghi rõ ý kiến đồng ý của cha,
mẹ hoặc người giám hộ, trừ trường hợp đã có ý kiến đồng ý bằng văn bản;
 b) Giấy tờ, tài liệu chứng minh chỗ ở hợp pháp.
```

**[2] [Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 — bản Word cung cấp](https://vanban.chinhphu.vn/?docid=214590&pageid=27160)**

Điều 9. Sự đồng ý của chủ thể dữ liệu cá nhân | Khoản 2 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_corpus_v7_20261005/privacy91-word.json

```text
2. Sự đồng ý của chủ thể dữ liệu cá nhân chỉ có hiệu lực khi dựa trên sự tự nguyện và biết rõ các thông tin sau đây:

a) Loại dữ liệu cá nhân được xử lý, mục đích xử lý dữ liệu cá nhân;

b) Bên kiểm soát dữ liệu cá nhân hoặc bên kiểm soát và xử lý dữ liệu cá nhân;

c) Các quyền, nghĩa vụ của chủ thể dữ liệu cá nhân.
```

**[3] [Luật Nhà ở — 79/VBHN-VPQH — bản Word cung cấp](https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-79-vbhn-vpqh-469209.htm)**

Điều 163. Hợp đồng về nhà ở | Khoản 1 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_corpus_v7_20261005/housing79-word.json

```text
Hợp đồng về nhà ở do các bên thỏa thuận và phải được lập thành văn bản bao gồm các nội dung sau đây:

1. Họ và tên của cá nhân, tên của tổ chức và địa chỉ của các bên;
```


## Câu 52 · Dữ liệu cá nhân

Ảnh căn cước công dân của người thuê được lưu và sử dụng như thế nào?

Trạng thái: Đã trả lời · cần rà nguồn. Provider: gemini-agent; model: gemini-3.8-flash-high.

faithfulness: 0.8182 | answer_relevancy: 0.9215 | context_utilization: 1.0 | context_recall: 0.3333 | context_precision: 1.0

ID nguồn chuẩn: privacy91-word.json, privacy356-word.json, identity26-word.json

ID nguồn đã truy xuất: privacy91-word.json

Nguồn quy định dữ liệu cá nhân chỉ được thu thập, xử lý đúng phạm vi, mục đích cụ thể và lưu trữ trong thời gian phù hợp với mục đích đó trừ khi pháp luật có quy định khác [1].

- Nguyên tắc bảo vệ dữ liệu cá nhân yêu cầu thực hiện đồng bộ, có hiệu quả các biện pháp, giải pháp về thể chế, kỹ thuật và con người phù hợp [1].
- Bên kiểm soát, bên kiểm soát và xử lý dữ liệu cá nhân cung cấp dữ liệu cho cơ quan, tổ chức, cá nhân khác khi được chủ thể dữ liệu đồng ý, trừ trường hợp pháp luật có quy định khác [2].
- Chủ thể dữ liệu có quyền gửi yêu cầu bằng văn bản hoặc dạng điện tử để rút lại sự đồng ý hoặc hạn chế xử lý dữ liệu của mình theo quy định và thỏa thuận [3].

Nguồn chỉ nêu nguyên tắc chung về bảo vệ và cung cấp dữ liệu cá nhân, không quy định riêng danh mục ảnh căn cước công dân của người thuê trọ [1] [2].

Nguồn là bản Word/trích tuyển được cung cấp, chưa xác minh toàn bộ câu chữ với bản chính thức; không coi ghi chú biên tập là quy định pháp luật.

### Nguồn và ngữ cảnh

**[1] [Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 — bản Word cung cấp](https://vanban.chinhphu.vn/?docid=214590&pageid=27160)**

Điều 3. Nguyên tắc bảo vệ dữ liệu cá nhân · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_corpus_v7_20261005/privacy91-word.json

```text
1. Tuân thủ quy định của Hiến pháp, quy định của Luật này và quy định khác của pháp luật có liên quan.

2. Chỉ được thu thập, xử lý dữ liệu cá nhân đúng phạm vi, mục đích cụ thể, rõ ràng, bảo đảm tuân thủ quy định của pháp luật.

3. Bảo đảm tính chính xác của dữ liệu cá nhân và được chỉnh sửa, cập nhật, bổ sung khi cần thiết; được lưu trữ trong khoảng thời gian phù hợp với mục đích xử lý dữ liệu cá nhân, trừ trường hợp pháp luật có quy định khác.

4. Thực hiện đồng bộ có hiệu quả các biện pháp, giải pháp về thể chế, kỹ thuật, con người phù hợp để bảo vệ dữ liệu cá nhân.

5. Chủ động phòng ngừa, phát hiện, ngăn chặn, đấu tranh, xử lý kịp thời, nghiêm minh mọi hành vi vi phạm pháp luật về bảo vệ dữ liệu cá nhân.

6. Bảo vệ dữ liệu cá nhân gắn với bảo vệ lợi ích quốc gia, dân tộc, phục vụ phát triển kinh tế - xã hội, bảo đảm quốc phòng, an ninh và đối ngoại; bảo đảm hài hòa giữa bảo vệ dữ liệu cá nhân với bảo vệ quyền, lợi ích hợp pháp của cơ quan, tổ chức, cá nhân.
```

**[2] [Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 — bản Word cung cấp](https://vanban.chinhphu.vn/?docid=214590&pageid=27160)**

Điều 15. Cung cấp dữ liệu cá nhân · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_corpus_v7_20261005/privacy91-word.json

```text
1. Chủ thể dữ liệu cá nhân cung cấp dữ liệu cá nhân cho cơ quan, tổ chức, cá nhân theo quy định của pháp luật hoặc theo thỏa thuận với cơ quan, tổ chức, cá nhân đó.

2. Bên kiểm soát dữ liệu cá nhân, bên kiểm soát và xử lý dữ liệu cá nhân cung cấp dữ liệu cá nhân trong các trường hợp sau đây:

a) Cung cấp cho chủ thể dữ liệu cá nhân theo yêu cầu của chủ thể dữ liệu cá nhân phù hợp quy định của pháp luật, thỏa thuận với chủ thể dữ liệu, trừ trường hợp việc cung cấp đó có thể gây tổn hại đến quốc phòng, an ninh quốc gia, trật tự, an toàn xã hội hoặc xâm phạm đến tính mạng, sức khỏe, tài sản của người khác;

b) Cung cấp cho cơ quan, tổ chức, cá nhân khác khi được chủ thể dữ liệu cá nhân đồng ý, trừ trường hợp pháp luật có quy định khác.
```

**[3] [Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 — bản Word cung cấp](https://vanban.chinhphu.vn/?docid=214590&pageid=27160)**

Điều 10. Yêu cầu rút lại sự đồng ý, yêu cầu hạn chế xử lý dữ liệu cá nhân · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_corpus_v7_20261005/privacy91-word.json

```text
1. Chủ thể dữ liệu cá nhân có quyền yêu cầu rút lại sự đồng ý cho phép xử lý dữ liệu cá nhân, yêu cầu hạn chế xử lý dữ liệu cá nhân của mình khi có nghi ngờ phạm vi, mục đích xử lý dữ liệu cá nhân hoặc tính chính xác của dữ liệu cá nhân, trừ trường hợp quy định tại Điều 19 của Luật này hoặc trường hợp pháp luật có quy định khác.

2. Yêu cầu rút lại sự đồng ý, yêu cầu hạn chế xử lý dữ liệu cá nhân của chủ thể dữ liệu cá nhân phải được thể hiện bằng văn bản, bao gồm cả dạng điện tử hoặc định dạng kiểm chứng được và được gửi cho bên kiểm soát dữ liệu cá nhân, bên kiểm soát và xử lý dữ liệu cá nhân. Yêu cầu rút lại sự đồng ý, yêu cầu hạn chế xử lý dữ liệu cá nhân của chủ thể dữ liệu cá nhân được thực hiện theo quy định của pháp luật và theo thỏa thuận giữa các bên.

3. Bên kiểm soát dữ liệu cá nhân, bên kiểm soát và xử lý dữ liệu cá nhân tiếp nhận, thực hiện và yêu cầu bên xử lý dữ liệu cá nhân thực hiện yêu cầu rút lại sự đồng ý, hạn chế xử lý dữ liệu cá nhân của chủ thể dữ liệu cá nhân trong thời gian theo quy định của pháp luật.

4. Việc thực hiện yêu cầu rút lại sự đồng ý, yêu cầu hạn chế xử lý dữ liệu cá nhân không áp dụng đối với hoạt động xử lý dữ liệu cá nhân trước thời điểm chủ thể dữ liệu cá nhân yêu cầu rút lại sự đồng ý hoặc yêu cầu hạn chế xử lý dữ liệu cá nhân.

Điều 19. Xử lý dữ liệu cá nhân trong trường hợp không cần sự đồng ý của chủ thể dữ liệu cá nhân | Khoản 1
1. Các trường hợp xử lý dữ liệu cá nhân không cần sự đồng ý của chủ thể dữ liệu cá nhân bao gồm:

a) Để bảo vệ tính mạng, sức khỏe, danh dự, nhân phẩm, quyền, lợi ích hợp pháp của chủ thể dữ liệu cá nhân hoặc người khác trong trường hợp cấp bách; bảo vệ quyền hoặc lợi ích chính đáng của mình, của người khác hoặc lợi ích của Nhà nước, của cơ quan tổ chức một cách cần thiết trước hành vi xâm phạm lợi ích nói trên. Bên kiểm soát dữ liệu cá nhân, bên xử lý dữ liệu cá nhân, bên kiểm soát và xử lý dữ liệu cá nhân, bên thứ ba có trách nhiệm chứng minh trường hợp này;

b) Để giải quyết tình trạng khẩn cấp; nguy cơ đe dọa an ninh quốc gia nhưng chưa đến mức ban bố tình trạng khẩn cấp; phòng, chống bạo loạn, khủng bố, phòng, chống tội phạm và vi phạm pháp luật;

c) Phục vụ hoạt động của cơ quan nhà nước, hoạt động quản lý nhà nước theo quy định của pháp luật;

d) Thực hiện thỏa thuận của chủ thể dữ liệu cá nhân với cơ quan, tổ chức, cá nhân có liên quan theo quy định của pháp luật;

đ) Trường hợp khác theo quy định của pháp luật.

Điều 19. Xử lý dữ liệu cá nhân trong trường hợp không cần sự đồng ý của chủ thể dữ liệu cá nhân | Khoản 2
2. Cơ quan, tổ chức, cá nhân có liên quan phải thiết lập cơ chế giám sát khi xử lý dữ liệu cá nhân trong trường hợp không cần sự đồng ý của chủ thể dữ liệu cá nhân bao gồm:

a) Thiết lập quy trình, quy định xử lý dữ liệu cá nhân và xác định trách nhiệm của cơ quan, tổ chức, cá nhân trong quá trình xử lý dữ liệu cá nhân;

b) Triển khai các biện pháp bảo vệ dữ liệu cá nhân phù hợp; thường xuyên đánh giá rủi ro có thể xảy ra trong quá trình xử lý dữ liệu cá nhân;

c) Thực hiện kiểm tra, đánh giá định kỳ việc tuân thủ quy định của pháp luật, quy trình, quy định xử lý dữ liệu cá nhân;

d) Có cơ chế tiếp nhận và xử lý phản ánh, kiến nghị từ cơ quan, tổ chức, cá nhân có liên quan.
```

**[4] [Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 — bản Word cung cấp](https://vanban.chinhphu.vn/?docid=214590&pageid=27160)**

Điều 9. Sự đồng ý của chủ thể dữ liệu cá nhân | Khoản 2 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_corpus_v7_20261005/privacy91-word.json

```text
2. Sự đồng ý của chủ thể dữ liệu cá nhân chỉ có hiệu lực khi dựa trên sự tự nguyện và biết rõ các thông tin sau đây:

a) Loại dữ liệu cá nhân được xử lý, mục đích xử lý dữ liệu cá nhân;

b) Bên kiểm soát dữ liệu cá nhân hoặc bên kiểm soát và xử lý dữ liệu cá nhân;

c) Các quyền, nghĩa vụ của chủ thể dữ liệu cá nhân.
```


## Câu 53 · Dữ liệu cá nhân

Chủ trọ có được đăng công khai ảnh giấy tờ hoặc số điện thoại của tôi không?

Trạng thái: Đã trả lời · cần rà nguồn. Provider: gemini-agent; model: gemini-3.8-flash-high.

faithfulness: 0.7222 | answer_relevancy: 0.935 | context_utilization: 1.0 | context_recall: 0.5 | context_precision: 1.0

ID nguồn chuẩn: privacy91-word.json, privacy356-word.json

ID nguồn đã truy xuất: privacy91-word.json

Chủ trọ chỉ được đăng công khai dữ liệu cá nhân khi có sự đồng ý của bạn hoặc thuộc các trường hợp pháp luật cho phép mà không xâm phạm quyền lợi ích hợp pháp [1].

- Dữ liệu cá nhân chỉ được công khai với mục đích cụ thể và phạm vi công khai phải phù hợp với mục đích đó [1].
- Việc công khai chỉ được thực hiện khi có sự đồng ý của chủ thể dữ liệu, theo luật định, thực hiện nghĩa vụ hợp đồng hoặc trường hợp giải quyết khẩn cấp, bảo vệ an ninh, phòng chống vi phạm [1].
- Sự đồng ý của bạn chỉ có hiệu lực khi hoàn toàn tự nguyện và biết rõ loại dữ liệu, mục đích xử lý cùng các quyền, nghĩa vụ liên quan [3].
- Chỉ được thu thập, xử lý dữ liệu cá nhân đúng phạm vi, mục đích cụ thể, rõ ràng và tuân thủ quy định của pháp luật [2].

Nguồn là bản Word được cung cấp và quy định nguyên tắc chung về dữ liệu cá nhân, không có điều khoản riêng biệt cho quan hệ thuê trọ [1].

Nguồn là bản Word/trích tuyển được cung cấp, chưa xác minh toàn bộ câu chữ với bản chính thức; không coi ghi chú biên tập là quy định pháp luật.

### Nguồn và ngữ cảnh

**[1] [Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 — bản Word cung cấp](https://vanban.chinhphu.vn/?docid=214590&pageid=27160)**

Điều 16. Công khai dữ liệu cá nhân · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_corpus_v7_20261005/privacy91-word.json

```text
1. Dữ liệu cá nhân chỉ được công khai với mục đích cụ thể. Phạm vi công khai, loại dữ liệu cá nhân được công khai phải phù hợp với mục đích công khai. Việc công khai dữ liệu cá nhân không được xâm phạm đến quyền, lợi ích hợp pháp của chủ thể dữ liệu cá nhân.

2. Dữ liệu cá nhân chỉ được công khai trong các trường hợp sau đây:

a) Khi có sự đồng ý của chủ thể dữ liệu cá nhân;

b) Thực hiện theo quy định của pháp luật;

c) Trường hợp quy định tại điểm b khoản 1 Điều 19 của Luật này;

d) Thực hiện nghĩa vụ theo hợp đồng.

3. Dữ liệu cá nhân công khai phải bảo đảm phản ánh đúng dữ liệu cá nhân từ nguồn dữ liệu gốc và tạo thuận lợi cho cơ quan, tổ chức, cá nhân trong việc tiếp cận, khai thác, sử dụng.

4. Hình thức công khai dữ liệu cá nhân, bao gồm: đăng tải dữ liệu trên trang thông tin điện tử, cổng thông tin điện tử, phương tiện thông tin đại chúng và các hình thức khác theo quy định của pháp luật.

5. Cơ quan, tổ chức, cá nhân công khai dữ liệu cá nhân phải kiểm soát và giám sát chặt chẽ việc công khai dữ liệu cá nhân để bảo đảm tuân thủ đúng mục đích, phạm vi và quy định của pháp luật; ngăn chặn việc truy cập, sử dụng, tiết lộ, sao chép, sửa đổi, xóa, hủy hoặc các hành vi xử lý trái phép khác đối với dữ liệu cá nhân đã công khai trong khả năng, điều kiện của mình.

Điều 19. Xử lý dữ liệu cá nhân trong trường hợp không cần sự đồng ý của chủ thể dữ liệu cá nhân | Khoản 1
1. Các trường hợp xử lý dữ liệu cá nhân không cần sự đồng ý của chủ thể dữ liệu cá nhân bao gồm:

a) Để bảo vệ tính mạng, sức khỏe, danh dự, nhân phẩm, quyền, lợi ích hợp pháp của chủ thể dữ liệu cá nhân hoặc người khác trong trường hợp cấp bách; bảo vệ quyền hoặc lợi ích chính đáng của mình, của người khác hoặc lợi ích của Nhà nước, của cơ quan tổ chức một cách cần thiết trước hành vi xâm phạm lợi ích nói trên. Bên kiểm soát dữ liệu cá nhân, bên xử lý dữ liệu cá nhân, bên kiểm soát và xử lý dữ liệu cá nhân, bên thứ ba có trách nhiệm chứng minh trường hợp này;

b) Để giải quyết tình trạng khẩn cấp; nguy cơ đe dọa an ninh quốc gia nhưng chưa đến mức ban bố tình trạng khẩn cấp; phòng, chống bạo loạn, khủng bố, phòng, chống tội phạm và vi phạm pháp luật;

c) Phục vụ hoạt động của cơ quan nhà nước, hoạt động quản lý nhà nước theo quy định của pháp luật;

d) Thực hiện thỏa thuận của chủ thể dữ liệu cá nhân với cơ quan, tổ chức, cá nhân có liên quan theo quy định của pháp luật;

đ) Trường hợp khác theo quy định của pháp luật.
```

**[2] [Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 — bản Word cung cấp](https://vanban.chinhphu.vn/?docid=214590&pageid=27160)**

Điều 3. Nguyên tắc bảo vệ dữ liệu cá nhân | Khoản 2 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_corpus_v7_20261005/privacy91-word.json

```text
2. Chỉ được thu thập, xử lý dữ liệu cá nhân đúng phạm vi, mục đích cụ thể, rõ ràng, bảo đảm tuân thủ quy định của pháp luật.
```

**[3] [Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 — bản Word cung cấp](https://vanban.chinhphu.vn/?docid=214590&pageid=27160)**

Điều 9. Sự đồng ý của chủ thể dữ liệu cá nhân | Khoản 2 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_corpus_v7_20261005/privacy91-word.json

```text
2. Sự đồng ý của chủ thể dữ liệu cá nhân chỉ có hiệu lực khi dựa trên sự tự nguyện và biết rõ các thông tin sau đây:

a) Loại dữ liệu cá nhân được xử lý, mục đích xử lý dữ liệu cá nhân;

b) Bên kiểm soát dữ liệu cá nhân hoặc bên kiểm soát và xử lý dữ liệu cá nhân;

c) Các quyền, nghĩa vụ của chủ thể dữ liệu cá nhân.
```


## Câu 54 · Dữ liệu cá nhân

Nếu thông tin cá nhân của tôi bị chia sẻ sai mục đích, tôi nên yêu cầu xử lý như thế nào?

Trạng thái: Đã trả lời · cần rà nguồn. Provider: gemini-agent; model: gemini-3.8-flash-high.

faithfulness: 1.0 | answer_relevancy: 0.8905 | context_utilization: 0.8333 | context_recall: 1.0 | context_precision: 1.0

ID nguồn chuẩn: privacy91-word.json, privacy356-word.json

ID nguồn đã truy xuất: privacy356-word.json, privacy91-word.json

Chủ thể dữ liệu có quyền yêu cầu rút lại sự đồng ý hoặc hạn chế xử lý dữ liệu khi có nghi ngờ về phạm vi, mục đích xử lý dữ liệu cá nhân [3].

- Lập yêu cầu rút lại sự đồng ý hoặc yêu cầu hạn chế xử lý dữ liệu cá nhân bằng văn bản, bao gồm cả dạng điện tử hoặc định dạng kiểm chứng được [3].
- Gửi yêu cầu theo đúng thủ tục cho bên kiểm soát dữ liệu cá nhân hoặc bên kiểm soát và xử lý dữ liệu cá nhân [1] [3].
- Theo dõi việc phản hồi thủ tục trong thời hạn 02 ngày làm việc từ bên kiểm soát dữ liệu cá nhân, bên kiểm soát và xử lý dữ liệu cá nhân [1].
- Chờ bên tiếp nhận thực hiện ngừng xử lý trong thời hạn 15 ngày, hoặc 20 ngày nếu cần yêu cầu bên xử lý dữ liệu cá nhân hay bên thứ ba ngừng xử lý [1].

Quyền rút lại sự đồng ý hoặc hạn chế xử lý không áp dụng với các trường hợp xử lý không cần sự đồng ý theo quy định pháp luật hoặc hoạt động xử lý trước thời điểm yêu cầu [1] [3].
Thời gian xử lý có thể kéo dài thêm tối đa 01 lần gia hạn không quá 15 ngày tùy mức độ phức tạp và bên tiếp nhận phải thông báo lý do cần gia hạn [1].

Nguồn là bản Word/trích tuyển được cung cấp, chưa xác minh toàn bộ câu chữ với bản chính thức; không coi ghi chú biên tập là quy định pháp luật.

### Nguồn và ngữ cảnh

**[1] [Nghị định 356/2025/NĐ-CP — bản Word cung cấp](https://vanban.chinhphu.vn/?classid=1&docid=216387&pageid=27160)**

Điều 5. Thực hiện quyền của chủ thể dữ liệu cá nhân · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_corpus_v7_20261005/privacy356-word.json

```text
1. Bên kiểm soát dữ liệu cá nhân, bên kiểm soát và xử lý dữ liệu cá nhân phải xây dựng quy trình, thủ tục, biểu mẫu rõ ràng để thực hiện các quyền của chủ thể dữ liệu cá nhân phù hợp với hoạt động xử lý dữ liệu cá nhân và trách nhiệm các bộ phận có liên quan; đảm bảo chủ thể dữ liệu cá nhân được biết về thủ tục thực hiện các quyền quy định tại khoản 1 Điều 4 của Luật Bảo vệ dữ liệu cá nhân.

2. Khi nhận được yêu cầu rút lại sự đồng ý cho phép xử lý dữ liệu cá nhân, hạn chế xử lý dữ liệu cá nhân, phản đối xử lý dữ liệu cá nhân theo đúng thủ tục của chủ thể dữ liệu cá nhân, bên kiểm soát dữ liệu cá nhân, bên kiểm soát và xử lý dữ liệu cá nhân phải phản hồi trong thời hạn 02 ngày làm việc, cung cấp đầy đủ thông tin cho chủ thể dữ liệu cá nhân về thủ tục ngừng xử lý dữ liệu cá nhân và thực hiện trong thời hạn 15 ngày, trừ trường hợp xử lý dữ liệu cá nhân không cần sự đồng ý của chủ thể dữ liệu cá nhân theo quy định tại Điều 19 Luật Bảo vệ dữ liệu cá nhân.Trường hợp cần yêu cầu bên xử lý dữ liệu cá nhân, bên thứ ba ngừng xử lý dữ liệu cá nhân của chủ thể dữ liệu cá nhân thì thực hiện trong thời hạn 20 ngày.

Tùy theo tính chất, mức độ phức tạp của yêu cầu, trường hợp cần gia hạn thời gian xử lý thì kéo dài thêm tối đa 01 lần gia hạn trong thời hạn không quá 15 ngày, bên kiểm soát dữ liệu cá nhân, bên kiểm soát và xử lý dữ liệu cá nhân thông báo cho chủ thể dữ liệu cá nhân lý do cần gia hạn và chịu trách nhiệm chứng minh việc gia hạn là cần thiết, hợp lý.

3. Khi nhận được yêu cầu xem, chỉnh sửa hoặc yêu cầu chỉnh sửa dữ liệu cá nhân, cung cấp dữ liệu cá nhân theo đúng thủ tục của chủ thể dữ liệu cá nhân, bên kiểm soát dữ liệu cá nhân, bên kiểm soát và xử lý dữ liệu cá nhân phải phản hồi trong thời hạn 02 ngày làm việc, cung cấp đầy đủ thông tin cho chủ thể dữ liệu cá nhân về thủ tục và thực hiện trong thời hạn 10 ngày. Trường hợp cần yêu cầu bên xử lý dữ liệu cá nhân, bên thứ ba chỉnh sửa dữ liệu cá nhân của chủ thể dữ liệu cá nhân thì thực hiện trong thời hạn 15 ngày.

Tùy theo tính chất, mức độ phức tạp của yêu cầu, trường hợp cần gia hạn thời gian xử lý thì kéo dài thêm tối đa 01 lần gia hạn trong thời hạn không quá 10 ngày, bên kiểm soát dữ liệu cá nhân, bên kiểm soát và xử lý dữ liệu cá nhân thông báo cho chủ thể dữ liệu cá nhân lý do cần gia hạn và chịu trách nhiệm chứng minh việc gia hạn là cần thiết, hợp lý.

4. Khi nhận được yêu cầu xóa dữ liệu cá nhân theo đúng thủ tục của chủ thể dữ liệu cá nhân, bên kiểm soát dữ liệu cá nhân, bên kiểm soát và xử lý dữ liệu cá nhân phải phản hồi trong thời hạn 02 ngày làm việc, cung cấp đầy đủ thông tin cho chủ thể dữ liệu cá nhân về thủ tục và thực hiện trong thời hạn 20 ngày. Trường hợp cần yêu cầu bên xử lý dữ liệu cá nhân, bên thứ ba cung cấp, xóa, hạn chế xử lý dữ liệu của chủ thể dữ liệu cá nhân thì thực hiện trong thời hạn 30 ngày.

Tùy theo tính chất, mức độ phức tạp của yêu cầu, trường hợp cần gia hạn thời gian xử lý thì kéo dài thêm tối đa 01 lần gia hạn trong thời hạn không quá 20 ngày, bên kiểm soát dữ liệu cá nhân, bên kiểm soát và xử lý dữ liệu cá nhân thông báo cho chủ thể dữ liệu cá nhân lý do cần gia hạn và chịu trách nhiệm chứng minh việc gia hạn là cần thiết, hợp lý.

5. Khi nhận được yêu cầu thực hiện các biện pháp, giải pháp bảo vệ dữ liệu cá nhân của mình theo đúng thủ tục của chủ thể dữ liệu cá nhân, cơ quan có thẩm quyền hoặc cơ quan, tổ chức, cá nhân liên quan đến xử lý dữ liệu cá nhân phải phản hồi trong thời hạn 02 ngày làm việc, cung cấp đầy đủ thông tin cho chủ thể dữ liệu cá nhân về thủ tục và thực hiện trong thời hạn 15 ngày.

Tùy theo tính chất, mức độ phức tạp của yêu cầu, trường hợp cần gia hạn thời gian xử lý thì kéo dài thêm tối đa 01 lần gia hạn trong thời hạn không quá 15 ngày, bên kiểm soát dữ liệu cá nhân, bên kiểm soát và xử lý dữ liệu cá nhân thông báo cho chủ thể dữ liệu cá nhân lý do cần gia hạn và chịu trách nhiệm chứng minh việc gia hạn là cần thiết, hợp lý.
```

**[2] [Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 — bản Word cung cấp](https://vanban.chinhphu.vn/?docid=214590&pageid=27160)**

Điều 3. Nguyên tắc bảo vệ dữ liệu cá nhân | Khoản 2 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_corpus_v7_20261005/privacy91-word.json

```text
2. Chỉ được thu thập, xử lý dữ liệu cá nhân đúng phạm vi, mục đích cụ thể, rõ ràng, bảo đảm tuân thủ quy định của pháp luật.
```

**[3] [Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 — bản Word cung cấp](https://vanban.chinhphu.vn/?docid=214590&pageid=27160)**

Điều 10. Yêu cầu rút lại sự đồng ý, yêu cầu hạn chế xử lý dữ liệu cá nhân · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_corpus_v7_20261005/privacy91-word.json

```text
1. Chủ thể dữ liệu cá nhân có quyền yêu cầu rút lại sự đồng ý cho phép xử lý dữ liệu cá nhân, yêu cầu hạn chế xử lý dữ liệu cá nhân của mình khi có nghi ngờ phạm vi, mục đích xử lý dữ liệu cá nhân hoặc tính chính xác của dữ liệu cá nhân, trừ trường hợp quy định tại Điều 19 của Luật này hoặc trường hợp pháp luật có quy định khác.

2. Yêu cầu rút lại sự đồng ý, yêu cầu hạn chế xử lý dữ liệu cá nhân của chủ thể dữ liệu cá nhân phải được thể hiện bằng văn bản, bao gồm cả dạng điện tử hoặc định dạng kiểm chứng được và được gửi cho bên kiểm soát dữ liệu cá nhân, bên kiểm soát và xử lý dữ liệu cá nhân. Yêu cầu rút lại sự đồng ý, yêu cầu hạn chế xử lý dữ liệu cá nhân của chủ thể dữ liệu cá nhân được thực hiện theo quy định của pháp luật và theo thỏa thuận giữa các bên.

3. Bên kiểm soát dữ liệu cá nhân, bên kiểm soát và xử lý dữ liệu cá nhân tiếp nhận, thực hiện và yêu cầu bên xử lý dữ liệu cá nhân thực hiện yêu cầu rút lại sự đồng ý, hạn chế xử lý dữ liệu cá nhân của chủ thể dữ liệu cá nhân trong thời gian theo quy định của pháp luật.

4. Việc thực hiện yêu cầu rút lại sự đồng ý, yêu cầu hạn chế xử lý dữ liệu cá nhân không áp dụng đối với hoạt động xử lý dữ liệu cá nhân trước thời điểm chủ thể dữ liệu cá nhân yêu cầu rút lại sự đồng ý hoặc yêu cầu hạn chế xử lý dữ liệu cá nhân.

Điều 19. Xử lý dữ liệu cá nhân trong trường hợp không cần sự đồng ý của chủ thể dữ liệu cá nhân | Khoản 1
1. Các trường hợp xử lý dữ liệu cá nhân không cần sự đồng ý của chủ thể dữ liệu cá nhân bao gồm:

a) Để bảo vệ tính mạng, sức khỏe, danh dự, nhân phẩm, quyền, lợi ích hợp pháp của chủ thể dữ liệu cá nhân hoặc người khác trong trường hợp cấp bách; bảo vệ quyền hoặc lợi ích chính đáng của mình, của người khác hoặc lợi ích của Nhà nước, của cơ quan tổ chức một cách cần thiết trước hành vi xâm phạm lợi ích nói trên. Bên kiểm soát dữ liệu cá nhân, bên xử lý dữ liệu cá nhân, bên kiểm soát và xử lý dữ liệu cá nhân, bên thứ ba có trách nhiệm chứng minh trường hợp này;

b) Để giải quyết tình trạng khẩn cấp; nguy cơ đe dọa an ninh quốc gia nhưng chưa đến mức ban bố tình trạng khẩn cấp; phòng, chống bạo loạn, khủng bố, phòng, chống tội phạm và vi phạm pháp luật;

c) Phục vụ hoạt động của cơ quan nhà nước, hoạt động quản lý nhà nước theo quy định của pháp luật;

d) Thực hiện thỏa thuận của chủ thể dữ liệu cá nhân với cơ quan, tổ chức, cá nhân có liên quan theo quy định của pháp luật;

đ) Trường hợp khác theo quy định của pháp luật.

Điều 19. Xử lý dữ liệu cá nhân trong trường hợp không cần sự đồng ý của chủ thể dữ liệu cá nhân | Khoản 2
2. Cơ quan, tổ chức, cá nhân có liên quan phải thiết lập cơ chế giám sát khi xử lý dữ liệu cá nhân trong trường hợp không cần sự đồng ý của chủ thể dữ liệu cá nhân bao gồm:

a) Thiết lập quy trình, quy định xử lý dữ liệu cá nhân và xác định trách nhiệm của cơ quan, tổ chức, cá nhân trong quá trình xử lý dữ liệu cá nhân;

b) Triển khai các biện pháp bảo vệ dữ liệu cá nhân phù hợp; thường xuyên đánh giá rủi ro có thể xảy ra trong quá trình xử lý dữ liệu cá nhân;

c) Thực hiện kiểm tra, đánh giá định kỳ việc tuân thủ quy định của pháp luật, quy trình, quy định xử lý dữ liệu cá nhân;

d) Có cơ chế tiếp nhận và xử lý phản ánh, kiến nghị từ cơ quan, tổ chức, cá nhân có liên quan.
```


## Câu 55 · Dấu hiệu lừa đảo

Người đăng yêu cầu đặt cọc trước nhưng không cho xem phòng: tôi nên kiểm tra những dấu hiệu rủi ro nào?

Trạng thái: Đã trả lời · cần rà nguồn. Provider: gemini-agent; model: gemini-3.8-flash-high.

faithfulness: 0.9545 | answer_relevancy: 0.9373 | context_utilization: 1.0 | context_recall: 0.6667 | context_precision: 0.6667

ID nguồn chuẩn: supplement-s01-word.json, supplement-s11-word.json, supplement-s12-word.json

ID nguồn đã truy xuất: supplement-s12-word.json, supplement-s11-word.json, criminal135-word.json

Khuyến nghị người thuê cảnh giác kiểm tra các dấu hiệu rủi ro liên quan đến giá phòng, lý do né tránh xem phòng và hành vi thúc ép chuyển tiền đặt cọc giữ chỗ [1] [2].

- Kiểm tra mức giá cho thuê so với thị trường, đặc biệt là các tin đăng phòng trọ giá siêu rẻ, vị trí hoặc view đẹp kèm ưu đãi giới hạn [1] [2].
- Kiểm tra việc người đăng đưa ra các lý do như nhiều người hỏi thuê hoặc chủ đi vắng để từ chối cho xem phòng trực tiếp [2].
- Khuyến nghị lưu ý dấu hiệu bên cho thuê tư vấn dồn dập nhằm thúc ép chuyển tiền đặt cọc hoặc thanh toán trước để giữ phòng, giữ chỗ [1] [2].
- Kiểm tra các yêu cầu chuyển thêm tiền sau đó với lý do sai nội dung chuyển khoản hoặc cần kế toán xác nhận để hoàn tiền [1].

Các dấu hiệu rủi ro được tổng hợp từ thông tin cảnh báo thủ đoạn lừa đảo của cơ quan Công an và không thay thế kết luận điều tra đối với từng vụ việc cụ thể [1] [2].

Hướng dẫn/khuyến cáo của Cổng Thông tin điện tử Bộ Công an bài Công an tỉnh Tuyên Quang; không phải điều luật. Tình huống gốc là đặt khách sạn tại Tuyên Quang. Áp dụng tham khảo cho chứng cứ giao dịch trực tuyến, không gọi là vụ thuê trọ CTU; không phải danh mục hồ sơ bắt buộc hoặc hướng dẫn soạn đơn tập thể.
Hướng dẫn/khuyến cáo của Cổng Thông tin điện tử Bộ Công an bài Công an TP Hải Phòng; không phải điều luật. Chỉ lấy phần thuê trọ và an toàn giao dịch; các thủ đoạn học phí, học bổng ngoài mục tiêu dự án. Không suy ra mọi tranh chấp cọc đều là tội phạm hay chắc chắn thu hồi được tiền.

### Nguồn và ngữ cảnh

**[1] [Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 — Cổng Thông tin điện tử Bộ Công an bài Công an tỉnh Tuyên Quang](https://bocongan.gov.vn/bai-viet/canh-giac-thu-doan-lua-dao-mao-danh-fanpage-khach-san-nha-hang-dat-coc-truc-tuyen-dip-le-hoi-thanh-tuyen-2026-1790041513)**

Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 | Đoạn nguyên văn 12 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_supplement_corpus_v8_20261005/supplement-s12-word.json

```text
Để tạo lòng tin, chúng sao chép hình ảnh, logo, địa chỉ, số điện thoại, nội dung giới thiệu từ trang thật; sử dụng tương tác ảo, tài khoản giả để bình luận tích cực, đánh giá 5 sao. Một số fanpage còn chạy quảng cáo trả phí để tiếp cận người có nhu cầu du lịch.

Khi khách liên hệ, các đối tượng tư vấn nhanh, đưa ra giá thấp hơn thị trường, kèm khuyến mãi “giới hạn” nhằm thúc ép chuyển tiền đặt cọc hoặc thanh toán trước để “giữ phòng”. Sau đó, chúng có thể gửi xác nhận đặt phòng giả, hoặc tiếp tục yêu cầu khách chuyển thêm tiền với lý do sai nội dung chuyển khoản, cần “kế toán xác nhận” để hoàn tiền. Sau nhiều lần nhận tiền, các đối tượng chặn liên lạc, chiếm đoạt toàn bộ số tiền. Nạn nhân thường chỉ phát hiện bị lừa khi đến nơi lưu trú, cơ sở dịch vụ nhưng không có thông tin đặt phòng nào được ghi nhận.

Cơ quan Công an khuyến cáo người dân và du khách cần nâng cao cảnh giác, thực hiện nghiêm túc các quy tắc xác minh thông tin trước khi thực hiện giao dịch chuyển tiền.

Khi phát hiện các Fanpage có dấu hiệu giả mạo, lừa đảo, lập tức thực hiện thao tác "Báo cáo" (Report) trang đó với nền tảng Facebook, đồng thời lưu lại bằng chứng (hình ảnh tin nhắn, tài khoản ngân hàng, phiếu giao dịch).

Khi nghi ngờ hoặc trở thành nạn nhân của các thủ đoạn lừa đảo trực tuyến, người dân cần nhanh chóng thu thập toàn bộ chứng cứ và báo ngay cho Cơ quan Công an nơi gần nhất để được hướng dẫn, tiếp nhận và xử lý kịp thời theo đúng quy định của pháp luật.
```

**[2] [Cảnh báo các thủ đoạn lừa đảo học sinh tân sinh viên mùa tựu trường — Cổng Thông tin điện tử Bộ Công an bài Công an TP Hải Phòng](https://bocongan.gov.vn/bai-viet/catp-hai-phong-canh-bao-cac-thu-doan-lua-dao-bua-vay-hoc-sinh-tan-sinh-vien-mua-tuu-truong-1787629964)**

Cảnh báo các thủ đoạn lừa đảo học sinh tân sinh viên mùa tựu trường | Đoạn nguyên văn 12 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_supplement_corpus_v8_20261005/supplement-s11-word.json

```text
- Bẫy "Phòng trọ giá rẻ, view đẹp"; Kẻ gian đăng tải thông tin cho thuê phòng trọ giá siêu rẻ, vị trí đẹp trên các hội nhóm. Khi liên hệ, chúng sẽ dùng nhiều lý do (nhiều người hỏi thuê, chủ đi vắng...) để yêu cầu chuyển tiền đặt cọc giữ chỗ trước khi đến xem phòng. Nhận được tiền, chúng lập tức chặn liên lạc.

Bảo mật thông tin cá nhân: Không cung cấp Căn cước công dân, Hộ chiếu, thông tin tài khoản ngân hàng, mã OTP hay bất kỳ dữ liệu cá nhân nào qua tin nhắn, số điện thoại hoặc email không thuộc hệ thống chính thức của trường.

Không tự ý chuyển tiền: Không thực hiện bất kỳ giao dịch chuyển tiền hay đóng lệ phí nào theo hướng dẫn từ các cá nhân, tổ chức chưa được xác minh rõ ràng.

Khi có nghi vấn, cần báo ngay cho cơ quan Công an gần nhất để được hướng dẫn và xử lý kịp thời./.
```

**[3] [Bộ luật Hình sự 135/VBHN-VPQH — bản Word trích tuyển cung cấp](https://congbao.chinhphu.vn/tai-ve-van-ban-so-135-vbhn-vpqh-46165-58894?format=pdf)**

Điều 174. Tội lừa đảo chiếm đoạt tài sản | Khoản 1 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_corpus_v7_20261005/criminal135-word.json

```text
1. Người nào bằng thủ đoạn gian dối chiếm đoạt tài sản của người khác trị giá từ 2.000.000 đồng đến dưới 50.000.000 đồng hoặc dưới 2.000.000 đồng nhưng thuộc một trong các trường hợp sau đây, thì bị phạt cải tạo không giam giữ đến 03 năm hoặc phạt tù từ 06 tháng đến 03 năm:

a) Đã bị xử phạt vi phạm hành chính về hành vi chiếm đoạt tài sản mà còn vi phạm;

b) Đã bị kết án về tội này hoặc về một trong các tội quy định tại các điều 168, 169, 170, 171, 172, 173, 175 và 290 của Bộ luật này, chưa được xóa án tích mà còn vi phạm;

c) Gây ảnh hưởng xấu đến an ninh, trật tự, an toàn xã hội;

d) Tài sản là phương tiện kiếm sống chính của người bị hại và gia đình họ[98].
```


## Câu 56 · Dấu hiệu lừa đảo

Tôi đã chuyển cọc cho một tin trọ có dấu hiệu giả mạo; nên lưu lại bằng chứng gì và trình báo ở đâu?

Trạng thái: Trả lời một phần. Provider: legal-partial-retained; model: gemini-3.8-flash-high.

faithfulness: 1.0 | answer_relevancy: 0.8493 | context_utilization: 1.0 | context_recall: 0.6667 | context_precision: 1.0

ID nguồn chuẩn: criminal135-word.json, procedure17-word.json, supplement-s12-word.json

ID nguồn đã truy xuất: supplement-s12-word.json, procedure17-word.json

Khuyến nghị người bị lừa nhanh chóng lưu lại các chứng cứ giao dịch rồi báo ngay cho cơ quan Công an nơi gần nhất hoặc cơ quan có trách nhiệm tiếp nhận theo luật định [1] [2].
Khuyến nghị lưu lại các bằng chứng gồm hình ảnh tin nhắn, tài khoản ngân hàng và phiếu giao dịch [1].
Khuyến nghị báo ngay cho Cơ quan Công an nơi gần nhất để được hướng dẫn, tiếp nhận và xử lý kịp thời theo đúng quy định của pháp luật [1].
Theo quy định, cơ quan điều tra, Viện kiểm sát tiếp nhận tố giác, tin báo về tội phạm, kiến nghị khởi tố; cơ quan, tổ chức khác tiếp nhận tố giác, tin báo về tội phạm [2].
Nguồn từ Cổng Thông tin điện tử Bộ Công an là nội dung cảnh báo và khuyến cáo phòng ngừa thủ đoạn lừa đảo, không phải văn bản quy phạm pháp luật quy định danh mục hồ sơ bắt buộc [1].

### Nguồn và ngữ cảnh

**[1] [Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 — Cổng Thông tin điện tử Bộ Công an bài Công an tỉnh Tuyên Quang](https://bocongan.gov.vn/bai-viet/canh-giac-thu-doan-lua-dao-mao-danh-fanpage-khach-san-nha-hang-dat-coc-truc-tuyen-dip-le-hoi-thanh-tuyen-2026-1790041513)**

Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 | Đoạn nguyên văn 12 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_supplement_corpus_v8_20261005/supplement-s12-word.json

```text
Để tạo lòng tin, chúng sao chép hình ảnh, logo, địa chỉ, số điện thoại, nội dung giới thiệu từ trang thật; sử dụng tương tác ảo, tài khoản giả để bình luận tích cực, đánh giá 5 sao. Một số fanpage còn chạy quảng cáo trả phí để tiếp cận người có nhu cầu du lịch.

Khi khách liên hệ, các đối tượng tư vấn nhanh, đưa ra giá thấp hơn thị trường, kèm khuyến mãi “giới hạn” nhằm thúc ép chuyển tiền đặt cọc hoặc thanh toán trước để “giữ phòng”. Sau đó, chúng có thể gửi xác nhận đặt phòng giả, hoặc tiếp tục yêu cầu khách chuyển thêm tiền với lý do sai nội dung chuyển khoản, cần “kế toán xác nhận” để hoàn tiền. Sau nhiều lần nhận tiền, các đối tượng chặn liên lạc, chiếm đoạt toàn bộ số tiền. Nạn nhân thường chỉ phát hiện bị lừa khi đến nơi lưu trú, cơ sở dịch vụ nhưng không có thông tin đặt phòng nào được ghi nhận.

Cơ quan Công an khuyến cáo người dân và du khách cần nâng cao cảnh giác, thực hiện nghiêm túc các quy tắc xác minh thông tin trước khi thực hiện giao dịch chuyển tiền.

Khi phát hiện các Fanpage có dấu hiệu giả mạo, lừa đảo, lập tức thực hiện thao tác "Báo cáo" (Report) trang đó với nền tảng Facebook, đồng thời lưu lại bằng chứng (hình ảnh tin nhắn, tài khoản ngân hàng, phiếu giao dịch).

Khi nghi ngờ hoặc trở thành nạn nhân của các thủ đoạn lừa đảo trực tuyến, người dân cần nhanh chóng thu thập toàn bộ chứng cứ và báo ngay cho Cơ quan Công an nơi gần nhất để được hướng dẫn, tiếp nhận và xử lý kịp thời theo đúng quy định của pháp luật.
```

**[2] [Bộ luật Tố tụng hình sự 17/VBHN-VPQH — bản Word trích tuyển cung cấp](https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-17-vbhn-vpqh-468961.htm)**

Điều 145. Trách nhiệm tiếp nhận và thẩm quyền giải quyết tố giác, tin báo về tội phạm, kiến nghị khởi tố | Khoản 2 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_corpus_v7_20261005/procedure17-word.json

```text
2. Cơ quan, tổ chức có trách nhiệm tiếp nhận tố giác, tin báo về tội phạm, kiến nghị khởi tố gồm:

a) Cơ quan điều tra, Viện kiểm sát tiếp nhận tố giác, tin báo về tội phạm, kiến nghị khởi tố;

b) Cơ quan, tổ chức khác tiếp nhận tố giác, tin báo về tội phạm.
```

**[3] [Bộ luật Tố tụng hình sự 17/VBHN-VPQH — bản Word trích tuyển cung cấp](https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-17-vbhn-vpqh-468961.htm)**

Điều 145. Trách nhiệm tiếp nhận và thẩm quyền giải quyết tố giác, tin báo về tội phạm, kiến nghị khởi tố | Khoản 3 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_corpus_v7_20261005/procedure17-word.json

```text
3. Thẩm quyền giải quyết tố giác, tin báo về tội phạm, kiến nghị khởi tố:

a) Cơ quan điều tra giải quyết tố giác, tin báo về tội phạm, kiến nghị khởi tố theo thẩm quyền điều tra của mình;

b) Cơ quan được giao nhiệm vụ tiến hành một số hoạt động điều tra giải quyết tố giác, tin báo về tội phạm theo thẩm quyền điều tra của mình;

c) Viện kiểm sát giải quyết tố giác, tin báo về tội phạm, kiến nghị khởi tố trong trường hợp phát hiện Cơ quan điều tra, cơ quan được giao nhiệm vụ tiến hành một số hoạt động điều tra có vi phạm pháp luật nghiêm trọng trong hoạt động kiểm tra, xác minh tố giác, tin báo về tội phạm, kiến nghị khởi tố hoặc có dấu hiệu bỏ lọt tội phạm mà Viện kiểm sát đã yêu cầu bằng văn bản nhưng không được khắc phục.
```

### Lỗi và giới hạn đã ghi nhận

```json
{
  "collect": null,
  "ragas": {},
  "unavailable": null,
  "degraded": [
    "{\"claim_id\": \"steps:3\", \"source_ids\": [1], \"kind\": \"procedure\", \"supported\": false, \"reason\": \"Phân loại cần sửa từ khuyến nghị sang hướng dẫn thao tác. Thao tác Báo cáo (Report) trang giả mạo trên nền tảng mạng xã hội là hướng dẫn thao tác (procedure), phân loại CLAIM.kind thành recommendation là sai.\", \"declared_kind\": \"recommendation\", \"code\": \"claim_kind_mismatch\"}",
    "Giữ các kết luận đã kiểm chứng; đánh dấu phần chưa có căn cứ."
  ]
}
```


## Câu 57 · Dấu hiệu lừa đảo

Khi nào tranh chấp tiền cọc có thể có dấu hiệu lừa đảo, và khi nào chỉ là tranh chấp hợp đồng?

Trạng thái: Đã trả lời · cần rà nguồn. Provider: gemini-agent; model: gemini-3.8-flash-high.

faithfulness: 0.913 | answer_relevancy: 0.9274 | context_utilization: 1.0 | context_recall: 0.5 | context_precision: 0.3333

ID nguồn chuẩn: criminal135-word.json, civil91-word.json

ID nguồn đã truy xuất: supplement-s01-word.json, criminal135-word.json, supplement-s11-word.json

Khuyến nghị nhận diện dấu hiệu lừa đảo khi có thủ đoạn gian dối nhằm chiếm đoạt tiền cọc rồi cắt liên lạc, còn tranh chấp hợp đồng thường gắn với bất đồng thỏa thuận hoặc chi phí phát sinh [1] [2] [3].

- Người nào bằng thủ đoạn gian dối chiếm đoạt tài sản của người khác từ 2.000.000 đồng trở lên hoặc dưới 2.000.000 đồng nhưng thuộc các trường hợp luật định thì bị xử lý về tội lừa đảo chiếm đoạt tài sản [2].
- Thủ đoạn lừa đảo được cảnh báo gồm việc đăng tin phòng giá rẻ, yêu cầu chuyển cọc giữ chỗ trước khi xem phòng rồi lập tức chặn liên lạc sau khi nhận tiền [3].
- Trường hợp gian lận hoặc tranh chấp hợp đồng được cảnh báo gồm việc yêu cầu đặt cọc rồi lật ngược thỏa thuận ban đầu hoặc thu thêm hàng loạt chi phí phát sinh [1].
- Khuyến nghị làm rõ điều khoản thời hạn và tiền đặt cọc khi kết thúc hợp đồng trước hạn, đồng thời luôn giữ tối thiểu một bản chính biên nhận đặt cọc và hợp đồng thuê [1].

Nguồn chưa cung cấp quy định chi tiết của Bộ luật Dân sự về ranh giới giải quyết tranh chấp hợp đồng dân sự đối với tiền đặt cọc [1] [2] [3].

Hướng dẫn/khuyến cáo của Trợ Giúp Chợ Tốt; không phải điều luật. Mẹo giao dịch, không phải điều luật. Không chứng minh hạn hoàn cọc cố định hoặc mức cọc bắt buộc; không thay thế xác minh người được ủy quyền cho thuê. Chỉ đọc phần kiểm tra, không bổ sung mẫu soạn hợp đồng.
Nguồn là bản Word/trích tuyển được cung cấp, chưa xác minh toàn bộ câu chữ với bản chính thức; không coi ghi chú biên tập là quy định pháp luật.
Hướng dẫn/khuyến cáo của Cổng Thông tin điện tử Bộ Công an bài Công an TP Hải Phòng; không phải điều luật. Chỉ lấy phần thuê trọ và an toàn giao dịch; các thủ đoạn học phí, học bổng ngoài mục tiêu dự án. Không suy ra mọi tranh chấp cọc đều là tội phạm hay chắc chắn thu hồi được tiền.

### Nguồn và ngữ cảnh

**[1] [Mẹo khi thuê phòng — Trợ Giúp Chợ Tốt](https://trogiup.chotot.com/nguoi-mua/meo-khi-thue-phong/)**

Mẹo khi thuê phòng | Đoạn nguyên văn 78 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_supplement_corpus_v8_20261005/supplement-s01-word.json

```text
1. Kiểm tra độ uy tín của người cho thuê trên môi trường trực tuyến (Google, Facebook, diễn đàn, …)

Tìm kiếm số điện thoại và địa chỉ muốn thuê trên Google, Facebook, các diễn đàn trực tuyến, … và xem các thông tin giao dịch trước đó như đánh giá của khách hàng về địa chỉ thuê này, …

2. Xác định địa điểm phòng muốn thuê và khảo sát mức giá chung

Tìm hiểu cụ thể địa chỉ muốn thuê gồm số nhà, tên đường, phường, quận.

Hỏi thăm trực tiếp hàng xóm xung quanh địa điểm muốn thuê và tham khảo ý kiến từ người thân, bạn bè hoặc tìm hiểu thông tin trên mạng về địa điểm này.

Mỗi khu vực sẽ có giá thuê khác nhau. Do đó, cần tìm hiểu mức giá chung theo từng khu vực trước khi thuê bằng cách so sánh với các tin đăng bất động sản cùng loại trên Chợ Tốt.

Thận trọng khi tìm được phòng ở trung tâm hoặc phòng tốt nhưng giá rẻ bất thường.

3. Không đặt cọc nếu chưa xác định được chủ nhà

Yêu cầu gặp trực tiếp chủ nhà trước khi đặt cọc.

Yêu cầu chủ nhà cho xem giấy tờ nhà và thẻ Căn Cước/thẻ Căn Cước Công Dân để xác nhận quyền sở hữu của chủ nhà

Nên chủ động hỏi kỹ về giá phòng, giá điện nước, các chi phí khác (nếu có) và các điều kiện sinh hoạt khác trước khi đặt cọc.

4. Phải đọc kỹ hợp đồng đặt cọc và hợp đồng thuê

Khi làm hợp đồng thuê cần đọc kỹ các điều khoản ghi trên hợp đồng: địa chỉ phòng, số phòng, tiền phòng cố định trong bao lâu không thay đổi, số người thuê, tiền điện, tiền nước, tiền gửi xe, sử dụng Internet và các chi phí phát sinh khác (nếu có).

Làm rõ các điều khoản về thời hạn hợp đồng và tiền đặt cọc trong trường hợp kết thúc hợp đồng trước hạn.

Luôn giữ tối thiểu một bản chính biên nhận đặt cọc và hợp đồng thuê.

5. Kiểm tra tình trạng phòng thuê trước khi đến ở

Kiểm tra tình trạng các thiết bị trong nhà và hệ thống đường điện, nước. Nếu có vấn đề hỏng hóc thì phải yêu cầu chủ nhà trọ sửa chữa hoặc thay thế.

Thống nhất số điện/nước (internet nếu có) phải trả ngay khi làm hợp đồng để tránh trường hợp phải trả thêm lượng điện/nước (internet nếu có) đã tiêu thụ trước đó.

Những trường hợp gian lận cần cảnh giác

Yêu cầu khách thuê đặt tiền cọc sau đó lật ngược những thỏa thuận ban đầu, thu thêm hàng loạt phí… là những trường hợp được người đi thuê cảnh báo:
```

**[2] [Bộ luật Hình sự 135/VBHN-VPQH — bản Word trích tuyển cung cấp](https://congbao.chinhphu.vn/tai-ve-van-ban-so-135-vbhn-vpqh-46165-58894?format=pdf)**

Điều 174. Tội lừa đảo chiếm đoạt tài sản | Khoản 1 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_corpus_v7_20261005/criminal135-word.json

```text
1. Người nào bằng thủ đoạn gian dối chiếm đoạt tài sản của người khác trị giá từ 2.000.000 đồng đến dưới 50.000.000 đồng hoặc dưới 2.000.000 đồng nhưng thuộc một trong các trường hợp sau đây, thì bị phạt cải tạo không giam giữ đến 03 năm hoặc phạt tù từ 06 tháng đến 03 năm:

a) Đã bị xử phạt vi phạm hành chính về hành vi chiếm đoạt tài sản mà còn vi phạm;

b) Đã bị kết án về tội này hoặc về một trong các tội quy định tại các điều 168, 169, 170, 171, 172, 173, 175 và 290 của Bộ luật này, chưa được xóa án tích mà còn vi phạm;

c) Gây ảnh hưởng xấu đến an ninh, trật tự, an toàn xã hội;

d) Tài sản là phương tiện kiếm sống chính của người bị hại và gia đình họ[98].
```

**[3] [Cảnh báo các thủ đoạn lừa đảo học sinh tân sinh viên mùa tựu trường — Cổng Thông tin điện tử Bộ Công an bài Công an TP Hải Phòng](https://bocongan.gov.vn/bai-viet/catp-hai-phong-canh-bao-cac-thu-doan-lua-dao-bua-vay-hoc-sinh-tan-sinh-vien-mua-tuu-truong-1787629964)**

Cảnh báo các thủ đoạn lừa đảo học sinh tân sinh viên mùa tựu trường | Đoạn nguyên văn 12 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_supplement_corpus_v8_20261005/supplement-s11-word.json

```text
- Bẫy "Phòng trọ giá rẻ, view đẹp"; Kẻ gian đăng tải thông tin cho thuê phòng trọ giá siêu rẻ, vị trí đẹp trên các hội nhóm. Khi liên hệ, chúng sẽ dùng nhiều lý do (nhiều người hỏi thuê, chủ đi vắng...) để yêu cầu chuyển tiền đặt cọc giữ chỗ trước khi đến xem phòng. Nhận được tiền, chúng lập tức chặn liên lạc.

Bảo mật thông tin cá nhân: Không cung cấp Căn cước công dân, Hộ chiếu, thông tin tài khoản ngân hàng, mã OTP hay bất kỳ dữ liệu cá nhân nào qua tin nhắn, số điện thoại hoặc email không thuộc hệ thống chính thức của trường.

Không tự ý chuyển tiền: Không thực hiện bất kỳ giao dịch chuyển tiền hay đóng lệ phí nào theo hướng dẫn từ các cá nhân, tổ chức chưa được xác minh rõ ràng.

Khi có nghi vấn, cần báo ngay cho cơ quan Công an gần nhất để được hướng dẫn và xử lý kịp thời./.
```


## Câu 58 · Dấu hiệu lừa đảo

Nếu có nhiều sinh viên cùng bị một người nhận cọc rồi cắt liên lạc, chúng tôi nên cung cấp thông tin gì cho cơ quan có thẩm quyền?

Trạng thái: Đã trả lời · cần rà nguồn. Provider: gemini-agent; model: gemini-3.8-flash-high.

faithfulness: 0.9375 | answer_relevancy: 0.8654 | context_utilization: 1.0 | context_recall: 0.5 | context_precision: 0.5

ID nguồn chuẩn: criminal135-word.json, procedure17-word.json

ID nguồn đã truy xuất: supplement-s12-word.json, procedure17-word.json

Khuyến nghị người dân nhanh chóng thu thập toàn bộ chứng cứ và báo ngay cho Cơ quan Công an nơi gần nhất để được hướng dẫn, tiếp nhận và xử lý kịp thời theo quy định [1].

- Khuyến nghị lưu lại bằng chứng gồm hình ảnh tin nhắn trao đổi với đối tượng [1].
- Khuyến nghị thu thập thông tin về tài khoản ngân hàng liên quan đến giao dịch [1].
- Khuyến nghị lưu lại phiếu giao dịch chuyển tiền để cung cấp cho cơ quan có thẩm quyền [1].
- Cơ quan điều tra, Viện kiểm sát và cơ quan, tổ chức khác có trách nhiệm tiếp nhận tố giác, tin báo về tội phạm theo quy định pháp luật [2].

Cơ quan Công an khuyến cáo người dân thu thập các tài liệu nêu trên khi nghi ngờ hoặc trở thành nạn nhân của thủ đoạn lừa đảo trực tuyến [1].

Hướng dẫn/khuyến cáo của Cổng Thông tin điện tử Bộ Công an bài Công an tỉnh Tuyên Quang; không phải điều luật. Tình huống gốc là đặt khách sạn tại Tuyên Quang. Áp dụng tham khảo cho chứng cứ giao dịch trực tuyến, không gọi là vụ thuê trọ CTU; không phải danh mục hồ sơ bắt buộc hoặc hướng dẫn soạn đơn tập thể.
Nguồn là bản Word/trích tuyển được cung cấp, chưa xác minh toàn bộ câu chữ với bản chính thức; không coi ghi chú biên tập là quy định pháp luật.

### Nguồn và ngữ cảnh

**[1] [Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 — Cổng Thông tin điện tử Bộ Công an bài Công an tỉnh Tuyên Quang](https://bocongan.gov.vn/bai-viet/canh-giac-thu-doan-lua-dao-mao-danh-fanpage-khach-san-nha-hang-dat-coc-truc-tuyen-dip-le-hoi-thanh-tuyen-2026-1790041513)**

Cảnh giác mạo danh Fanpage khách sạn nhà hàng đặt cọc trực tuyến dịp Lễ hội Thành Tuyên 2026 | Đoạn nguyên văn 12 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_supplement_corpus_v8_20261005/supplement-s12-word.json

```text
Để tạo lòng tin, chúng sao chép hình ảnh, logo, địa chỉ, số điện thoại, nội dung giới thiệu từ trang thật; sử dụng tương tác ảo, tài khoản giả để bình luận tích cực, đánh giá 5 sao. Một số fanpage còn chạy quảng cáo trả phí để tiếp cận người có nhu cầu du lịch.

Khi khách liên hệ, các đối tượng tư vấn nhanh, đưa ra giá thấp hơn thị trường, kèm khuyến mãi “giới hạn” nhằm thúc ép chuyển tiền đặt cọc hoặc thanh toán trước để “giữ phòng”. Sau đó, chúng có thể gửi xác nhận đặt phòng giả, hoặc tiếp tục yêu cầu khách chuyển thêm tiền với lý do sai nội dung chuyển khoản, cần “kế toán xác nhận” để hoàn tiền. Sau nhiều lần nhận tiền, các đối tượng chặn liên lạc, chiếm đoạt toàn bộ số tiền. Nạn nhân thường chỉ phát hiện bị lừa khi đến nơi lưu trú, cơ sở dịch vụ nhưng không có thông tin đặt phòng nào được ghi nhận.

Cơ quan Công an khuyến cáo người dân và du khách cần nâng cao cảnh giác, thực hiện nghiêm túc các quy tắc xác minh thông tin trước khi thực hiện giao dịch chuyển tiền.

Khi phát hiện các Fanpage có dấu hiệu giả mạo, lừa đảo, lập tức thực hiện thao tác "Báo cáo" (Report) trang đó với nền tảng Facebook, đồng thời lưu lại bằng chứng (hình ảnh tin nhắn, tài khoản ngân hàng, phiếu giao dịch).

Khi nghi ngờ hoặc trở thành nạn nhân của các thủ đoạn lừa đảo trực tuyến, người dân cần nhanh chóng thu thập toàn bộ chứng cứ và báo ngay cho Cơ quan Công an nơi gần nhất để được hướng dẫn, tiếp nhận và xử lý kịp thời theo đúng quy định của pháp luật.
```

**[2] [Bộ luật Tố tụng hình sự 17/VBHN-VPQH — bản Word trích tuyển cung cấp](https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-17-vbhn-vpqh-468961.htm)**

Điều 145. Trách nhiệm tiếp nhận và thẩm quyền giải quyết tố giác, tin báo về tội phạm, kiến nghị khởi tố | Khoản 2 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_corpus_v7_20261005/procedure17-word.json

```text
2. Cơ quan, tổ chức có trách nhiệm tiếp nhận tố giác, tin báo về tội phạm, kiến nghị khởi tố gồm:

a) Cơ quan điều tra, Viện kiểm sát tiếp nhận tố giác, tin báo về tội phạm, kiến nghị khởi tố;

b) Cơ quan, tổ chức khác tiếp nhận tố giác, tin báo về tội phạm.
```

**[3] [Bộ luật Tố tụng hình sự 17/VBHN-VPQH — bản Word trích tuyển cung cấp](https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-17-vbhn-vpqh-468961.htm)**

Điều 145. Trách nhiệm tiếp nhận và thẩm quyền giải quyết tố giác, tin báo về tội phạm, kiến nghị khởi tố | Khoản 4 · Trang bản trích 1

Đường dẫn nguồn: docs/legal_word_corpus_v7_20261005/procedure17-word.json

```text
4. Cơ quan có thẩm quyền giải quyết tố giác, tin báo về tội phạm, kiến nghị khởi tố có trách nhiệm thông báo kết quả giải quyết cho cá nhân, cơ quan, tổ chức đã tố giác, báo tin về tội phạm, kiến nghị khởi tố.
```


## Câu 59 · Ký túc xá

KTX CTU loại A4 có những tiện nghi gì, sức chứa mấy người và đơn giá bao nhiêu? Hãy nói rõ kỳ tính giá đã xác nhận chưa.

Trạng thái: Đã trả lời · cần rà nguồn. Provider: structured_ktx; model: —.

faithfulness: 0.9091 | answer_relevancy: 0.8861 | context_utilization: 1.0 | context_recall: 0.5 | context_precision: 1.0

ID nguồn chuẩn: Danh mục phòng KTX năm 2026 · bạn cung cấp, https://ssc.ctu.edu.vn/hoat/160-cs1.html

ID nguồn đã truy xuất: Danh mục phòng KTX năm 2026 · bạn cung cấp

**KTX · năm học 2026-2027**
- KTX CTU · A4 · khu A · sức chứa 4 người. phòng được phép nấu ăn, giường tầng, nhà vệ sinh tập thể an toàn trong khuôn viên dãy. được nấu ăn; giường tầng; vệ sinh: Nhà vệ sinh tập thể trong khuôn viên dãy. Giá 285.000 đồng/người/học kỳ 3,5 tháng (2026). Giá theo bảng phòng bạn cung cấp cho năm 2026; xác nhận mức thu và chỗ trống với văn phòng KTX. [1]
Danh mục loại phòng chưa xác nhận số chỗ trống hiện tại; cần kiểm tra với văn phòng KTX.

### Nguồn và ngữ cảnh

**[1] Danh mục phòng KTX năm 2026 · bạn cung cấp**

Danh mục KTX · cập nhật 2026-10-12

Đường dẫn nguồn: Danh mục KTX dùng chung

```text
KTX CTU · A4 · khu A · sức chứa 4 người. phòng được phép nấu ăn, giường tầng, nhà vệ sinh tập thể an toàn trong khuôn viên dãy. được nấu ăn; giường tầng; vệ sinh: Nhà vệ sinh tập thể trong khuôn viên dãy. Giá 285.000 đồng/người/học kỳ 3,5 tháng (2026). Giá theo bảng phòng bạn cung cấp cho năm 2026; xác nhận mức thu và chỗ trống với văn phòng KTX.
```


## Câu 60 · Ký túc xá

Tìm các loại phòng KTX CTU cho 6 người, được nấu ăn và có giường tầng trong bảng tôi cập nhật.

Trạng thái: Đã trả lời · cần rà nguồn. Provider: structured_ktx; model: —.

faithfulness: 0.9333 | answer_relevancy: 0.8911 | context_utilization: 1.0 | context_recall: 1.0 | context_precision: 1.0

ID nguồn chuẩn: Danh mục phòng KTX năm 2026 · bạn cung cấp

ID nguồn đã truy xuất: Danh mục phòng KTX năm 2026 · bạn cung cấp

**KTX · năm học 2026-2027**
- KTX CTU · A62 · khu A · sức chứa 6 người. phòng 6 người, giường tầng, nấu ăn. được nấu ăn; giường tầng. Giá 395.000 đồng/người/học kỳ 3,5 tháng (2026). Giá theo bảng phòng bạn cung cấp cho năm 2026; xác nhận mức thu và chỗ trống với văn phòng KTX. [1]
- KTX CTU · PA625 · khu chưa xác nhận · sức chứa 6 người. Phòng được nấu ăn, giường tầng. được nấu ăn; giường tầng. Giá 395.000 đồng/người/học kỳ 3,5 tháng (2026). Giá theo bảng phòng bạn cung cấp cho năm 2026; xác nhận mức thu và chỗ trống với văn phòng KTX. [1]
Danh mục loại phòng chưa xác nhận số chỗ trống hiện tại; cần kiểm tra với văn phòng KTX.

### Nguồn và ngữ cảnh

**[1] Danh mục phòng KTX năm 2026 · bạn cung cấp**

Danh mục KTX · cập nhật 2026-10-12

Đường dẫn nguồn: Danh mục KTX dùng chung

```text
KTX CTU · A62 · khu A · sức chứa 6 người. phòng 6 người, giường tầng, nấu ăn. được nấu ăn; giường tầng. Giá 395.000 đồng/người/học kỳ 3,5 tháng (2026). Giá theo bảng phòng bạn cung cấp cho năm 2026; xác nhận mức thu và chỗ trống với văn phòng KTX.

KTX CTU · PA625 · khu chưa xác nhận · sức chứa 6 người. Phòng được nấu ăn, giường tầng. được nấu ăn; giường tầng. Giá 395.000 đồng/người/học kỳ 3,5 tháng (2026). Giá theo bảng phòng bạn cung cấp cho năm 2026; xác nhận mức thu và chỗ trống với văn phòng KTX.
```


## Câu 61 · Ký túc xá

Mã PB225 có chắc là phòng thuộc KTX khu B không? Phòng này có giường gì, sức chứa và giá bao nhiêu?

Trạng thái: Đã trả lời · cần rà nguồn. Provider: structured_ktx; model: —.

faithfulness: 0.9091 | answer_relevancy: 0.907 | context_utilization: 1.0 | context_recall: 1.0 | context_precision: 1.0

ID nguồn chuẩn: Danh mục phòng KTX năm 2026 · bạn cung cấp

ID nguồn đã truy xuất: Danh mục phòng KTX năm 2026 · bạn cung cấp

**KTX · năm học 2026-2027**
- KTX CTU · PB225 · khu chưa xác nhận · sức chứa 2 người. Phòng được phép nấu ăn, giường bộ. được nấu ăn; giường bộ. Giá 702.500 đồng/người/học kỳ 3,5 tháng (2026). Giá theo bảng phòng bạn cung cấp cho năm 2026; xác nhận mức thu và chỗ trống với văn phòng KTX. [1]
Danh mục loại phòng chưa xác nhận số chỗ trống hiện tại; cần kiểm tra với văn phòng KTX.

### Nguồn và ngữ cảnh

**[1] Danh mục phòng KTX năm 2026 · bạn cung cấp**

Danh mục KTX · cập nhật 2026-10-12

Đường dẫn nguồn: Danh mục KTX dùng chung

```text
KTX CTU · PB225 · khu chưa xác nhận · sức chứa 2 người. Phòng được phép nấu ăn, giường bộ. được nấu ăn; giường bộ. Giá 702.500 đồng/người/học kỳ 3,5 tháng (2026). Giá theo bảng phòng bạn cung cấp cho năm 2026; xác nhận mức thu và chỗ trống với văn phòng KTX.
```


## Câu 62 · Ký túc xá

Theo phiếu CTU năm 2025, KTX khu B phòng 4 người có phí bao nhiêu và được nấu ăn không? Mức đó có phải giá tháng hoặc giá hiện hành không?

Trạng thái: Chưa đủ căn cứ. Provider: structured_ktx; model: —.

faithfulness: N/A (No retrieved contexts) | answer_relevancy: 0.0 | context_utilization: N/A (No retrieved contexts) | context_recall: 0.0 | context_precision: N/A (No retrieved source IDs; precision is undefined)

ID nguồn chuẩn: ctu_2025.pdf

ID nguồn đã truy xuất: 

**KTX · năm học 2026-2027**
Chưa tìm thấy loại phòng khớp trong danh mục hiện có. Điều này không xác nhận KTX đã hết chỗ.
Danh mục loại phòng chưa xác nhận số chỗ trống hiện tại; cần kiểm tra với văn phòng KTX.

### Nguồn và ngữ cảnh

### Lỗi và giới hạn đã ghi nhận

```json
{
  "collect": null,
  "ragas": {},
  "unavailable": {
    "faithfulness": "No retrieved contexts",
    "context_utilization": "No retrieved contexts",
    "context_precision": "No retrieved source IDs; precision is undefined"
  },
  "degraded": []
}
```


## Câu 63 · Ký túc xá

Cho tôi tọa độ GPS KTX CTU khu A và khu B, nguồn bản đồ và giới hạn độ chính xác.

Trạng thái: Đã trả lời · cần rà nguồn. Provider: structured_ktx; model: —.

faithfulness: 0.8 | answer_relevancy: 0.8495 | context_utilization: 1.0 | context_recall: 1.0 | context_precision: 1.0

ID nguồn chuẩn: https://www.openstreetmap.org/way/89864434, https://www.openstreetmap.org/way/168528554

ID nguồn đã truy xuất: https://www.openstreetmap.org/way/89864434, https://www.openstreetmap.org/way/168528554

**KTX · năm học 2026-2027**
- Ký túc xá khu A: 10.0338798, 105.7702172 — Văn phòng phục vụ sinh viên KTX khu A. Điểm đại diện từ OpenStreetMap; chưa xác nhận cổng vào hoặc vị trí từng phòng. [1]
- Ký túc xá khu B: 10.0301622, 105.7642123 — Điểm đại diện KTX khu B. Điểm đại diện từ OpenStreetMap; chưa xác nhận cổng vào hoặc vị trí từng phòng. [2]
Bạn có thể mở vị trí và chỉ đường trên trang KTX của hệ thống.

### Nguồn và ngữ cảnh

**[1] [Văn phòng phục vụ sinh viên KTX khu A · OpenStreetMap](https://www.openstreetmap.org/way/89864434)**

Danh mục KTX · cập nhật 2026-10-12

Đường dẫn nguồn: Danh mục KTX dùng chung

```text
Ký túc xá khu A: 10.0338798, 105.7702172 — Văn phòng phục vụ sinh viên KTX khu A. Điểm đại diện từ OpenStreetMap; chưa xác nhận cổng vào hoặc vị trí từng phòng.
```

**[2] [Điểm đại diện KTX khu B · OpenStreetMap](https://www.openstreetmap.org/way/168528554)**

Danh mục KTX · cập nhật 2026-10-12

Đường dẫn nguồn: Danh mục KTX dùng chung

```text
Ký túc xá khu B: 10.0301622, 105.7642123 — Điểm đại diện KTX khu B. Điểm đại diện từ OpenStreetMap; chưa xác nhận cổng vào hoặc vị trí từng phòng.
```


## Câu 64 · Ký túc xá

KTX CTU hiện còn phòng A4 không? Nếu chưa có dữ liệu chỗ trống thì nói rõ và cho tôi cách liên hệ xác nhận.

Trạng thái: Đã trả lời · cần rà nguồn. Provider: structured_ktx; model: —.

faithfulness: 1.0 | answer_relevancy: 0.9042 | context_utilization: 1.0 | context_recall: 1.0 | context_precision: 1.0

ID nguồn chuẩn: https://ssc.ctu.edu.vn/images/upload/thong_bao/072026_tb_dk1_2627.pdf

ID nguồn đã truy xuất: https://ssc.ctu.edu.vn/images/upload/thong_bao/072026_tb_dk1_2627.pdf

**KTX · năm học 2026-2027**
- Danh mục loại phòng, hình ảnh và tọa độ khu KTX không xác nhận số chỗ còn trống. Phải xem tình trạng trên Hệ thống Quản lý KTX hoặc liên hệ văn phòng để xác nhận tại thời điểm đăng ký. [1]
- Email KTX: ktx@ctu.edu.vn. Văn phòng khu A: 0292 3872 178; khu B: 0292 3872 275, theo thông báo 2026–2027. Một biểu mẫu cũ ghi số khu A khác; ưu tiên số trong thông báo mới. [1]

### Nguồn và ngữ cảnh

**[1] [Thông báo 307/TB-CTSV · HKI 2026–2027](https://ssc.ctu.edu.vn/images/upload/thong_bao/072026_tb_dk1_2627.pdf)**

Danh mục KTX · cập nhật 2026-10-12

Đường dẫn nguồn: Danh mục KTX dùng chung

```text
Danh mục loại phòng, hình ảnh và tọa độ khu KTX không xác nhận số chỗ còn trống. Phải xem tình trạng trên Hệ thống Quản lý KTX hoặc liên hệ văn phòng để xác nhận tại thời điểm đăng ký.

Email KTX: ktx@ctu.edu.vn. Văn phòng khu A: 0292 3872 178; khu B: 0292 3872 275, theo thông báo 2026–2027. Một biểu mẫu cũ ghi số khu A khác; ưu tiên số trong thông báo mới.
```


## Câu 65 · Ký túc xá

Ở KTX CTU có Wi-Fi, nhà xe và căn tin không? Xe đạp, xe máy và xe điện được tính phí gửi như thế nào theo nguồn đã có?

Trạng thái: Đã trả lời · cần rà nguồn. Provider: structured_ktx; model: —.

faithfulness: 0.9 | answer_relevancy: 0.8896 | context_utilization: 0.8333 | context_recall: 0.6667 | context_precision: 0.6667

ID nguồn chuẩn: https://tansinhvien.ctu.edu.vn/sinh-hoat/huong-dan-tan-sinh-vien-dang-ky-o-ky-tuc-xa, https://ssc.ctu.edu.vn/hoat/160-cs1.html, https://ssc.ctu.edu.vn/images/upload/thong_bao/072026_tb_dk1_2627.pdf

ID nguồn đã truy xuất: https://tansinhvien.ctu.edu.vn/sinh-hoat/huong-dan-tan-sinh-vien-dang-ky-o-ky-tuc-xa, Danh mục phòng KTX năm 2026 · bạn cung cấp, https://ssc.ctu.edu.vn/images/upload/thong_bao/072026_tb_dk1_2627.pdf

**KTX · năm học 2026-2027**
- Wi-Fi và tiện ích: Phòng ở có Wi-Fi riêng từng phòng. Trong khuôn viên có căn tin, siêu thị mini; trang giới thiệu còn nêu nhà xe và khu vực giặt sấy. [1]
- Gửi xe: Xe đạp được miễn phí gửi xe. Trang hướng dẫn tân sinh viên 2026–2027 công bố xe máy/xe điện 25.000 đồng/sinh viên/tháng, nộp theo học kỳ. [1]
- Phí ở và đơn vị giá: Theo danh mục 27 loại phòng bạn cung cấp cho năm 2026, đơn giá từ 220.000 đến 967.000 đồng/người/học kỳ 3,5 tháng. Chưa gồm điện nước; cần xác nhận mức thu và chỗ trống tại thời điểm đăng ký với văn phòng KTX. [2]
- Điện nước: Sinh viên nộp phí điện, nước hàng tháng theo lượng sử dụng thực tế của phòng; phí ở chưa bao gồm điện nước. [3]

### Nguồn và ngữ cảnh

**[1] [Hướng dẫn tân sinh viên đăng ký KTX · 2026–2027](https://tansinhvien.ctu.edu.vn/sinh-hoat/huong-dan-tan-sinh-vien-dang-ky-o-ky-tuc-xa)**

Danh mục KTX · cập nhật 2026-10-12

Đường dẫn nguồn: Danh mục KTX dùng chung

```text
Phòng ở có Wi-Fi riêng từng phòng. Trong khuôn viên có căn tin, siêu thị mini; trang giới thiệu còn nêu nhà xe và khu vực giặt sấy.

Xe đạp được miễn phí gửi xe. Trang hướng dẫn tân sinh viên 2026–2027 công bố xe máy/xe điện 25.000 đồng/sinh viên/tháng, nộp theo học kỳ.
```

**[2] Danh mục phòng KTX năm 2026 · bạn cung cấp**

Danh mục KTX · cập nhật 2026-10-12

Đường dẫn nguồn: Danh mục KTX dùng chung

```text
Theo danh mục 27 loại phòng bạn cung cấp cho năm 2026, đơn giá từ 220.000 đến 967.000 đồng/người/học kỳ 3,5 tháng. Chưa gồm điện nước; cần xác nhận mức thu và chỗ trống tại thời điểm đăng ký với văn phòng KTX.
```

**[3] [Thông báo 307/TB-CTSV · HKI 2026–2027](https://ssc.ctu.edu.vn/images/upload/thong_bao/072026_tb_dk1_2627.pdf)**

Danh mục KTX · cập nhật 2026-10-12

Đường dẫn nguồn: Danh mục KTX dùng chung

```text
Sinh viên nộp phí điện, nước hàng tháng theo lượng sử dụng thực tế của phòng; phí ở chưa bao gồm điện nước.
```


## Câu 66 · Ký túc xá

Theo nội quy KTX CTU, sinh viên có được đưa người ngoài vào ở qua đêm không? Trích đúng điều hoặc mục trong tài liệu và nêu giới hạn nguồn.

Trạng thái: Đã trả lời · cần rà nguồn. Provider: structured_ktx; model: —.

faithfulness: 0.8947 | answer_relevancy: 0.9031 | context_utilization: 1.0 | context_recall: 1.0 | context_precision: 1.0

ID nguồn chuẩn: https://ssc.ctu.edu.vn/images/upload/Noiquy_KTX_trich_092025.pdf

ID nguồn đã truy xuất: https://ssc.ctu.edu.vn/images/upload/Noiquy_KTX_trich_092025.pdf

**KTX · năm học 2026-2027**
Các điều/mục liên quan trong bản nội quy CTU đã lưu:
- Điều 6. Công tác giữ gìn an ninh trật tự | Khoản 2
2. Nghiêm cấm các hành vi sau: 
- Tham gia biểu tình, tự ý tụ tập đông người; Kích động, lôi kéo người khác biểu 
tình, viết truyền đơn, áp-phích trái pháp luật; 
- Chứa chấp, buôn bán vũ khí, chất nổ và hàng cấm theo quy định của nhà nước;

- Tàng trữ, lưu hành, truy cập, sử dụng sản phẩm văn hóa đồi trụy hoặc tham gia 
các hoạt động mê tín dị đoan, hoạt động tôn giáo trái phép; 
- Buôn bán, vận chuyển, tàng trữ, sử dụng và lôi kéo người khác sử dụng ma túy; 
- Tổ chức hoặc tham gia đánh bạc, mại dâm dưới mọi hình thức; 
- Chứa chấp, che giấu hàng lậu, tội phạm; 
- Đánh nhau, tổ chức hoặc tham gia đánh nhau gây mất ANTT; 
- Lấy cắp tài sản, chứa chấp, tiêu thụ tài sản do người khác lấy cắp mà có; 
- Đưa người ngoài vào KTX, gây ảnh hưởng xấu đến ANTT. [1]
- Điều 2. Một số quy định chung | Khoản 5
5. Khi phụ huynh hoặc người thân đến thăm có nhu cầu lưu lại qua đêm, SV phải 
đăng ký với Văn phòng TT. PVSV hoặc Tổ Bảo vệ KTX, sẽ được bố trí ở khu vực riêng. [1]
- Điều 4. Quy định về sử dụng phòng ở | Khoản 8
8. Khi hết hạn ở KTX, SV có trách nhiệm bàn giao chỗ ở cho Giám thị quản lý dãy 
và các tài sản thuộc KTX đúng thời gian, vệ sinh phòng ở và khôi phục lại như hiện trạng 
ban đầu. Nếu quá thời hạn, SV không thực hiện trả phòng, TT. PVSV sẽ tiến hành lập Biên 
bản thu hồi phòng, tài sản của SV còn trong phòng TT. PVSV sẽ không chịu trách nhiệm 
về mất mát và hư hỏng. [1]
Đây là trích đoạn nguồn công khai đã lưu; cần đối chiếu văn phòng KTX nếu có quy định mới hơn.

### Nguồn và ngữ cảnh

**[1] [Nội quy KTX · bản công khai CTU](https://ssc.ctu.edu.vn/images/upload/Noiquy_KTX_trich_092025.pdf)**

Danh mục KTX · cập nhật 2026-10-12

Đường dẫn nguồn: Danh mục KTX dùng chung

```text
Điều 6. Công tác giữ gìn an ninh trật tự | Khoản 2
2. Nghiêm cấm các hành vi sau: 
- Tham gia biểu tình, tự ý tụ tập đông người; Kích động, lôi kéo người khác biểu 
tình, viết truyền đơn, áp-phích trái pháp luật; 
- Chứa chấp, buôn bán vũ khí, chất nổ và hàng cấm theo quy định của nhà nước;

- Tàng trữ, lưu hành, truy cập, sử dụng sản phẩm văn hóa đồi trụy hoặc tham gia 
các hoạt động mê tín dị đoan, hoạt động tôn giáo trái phép; 
- Buôn bán, vận chuyển, tàng trữ, sử dụng và lôi kéo người khác sử dụng ma túy; 
- Tổ chức hoặc tham gia đánh bạc, mại dâm dưới mọi hình thức; 
- Chứa chấp, che giấu hàng lậu, tội phạm; 
- Đánh nhau, tổ chức hoặc tham gia đánh nhau gây mất ANTT; 
- Lấy cắp tài sản, chứa chấp, tiêu thụ tài sản do người khác lấy cắp mà có; 
- Đưa người ngoài vào KTX, gây ảnh hưởng xấu đến ANTT.

Điều 2. Một số quy định chung | Khoản 5
5. Khi phụ huynh hoặc người thân đến thăm có nhu cầu lưu lại qua đêm, SV phải 
đăng ký với Văn phòng TT. PVSV hoặc Tổ Bảo vệ KTX, sẽ được bố trí ở khu vực riêng.

Điều 4. Quy định về sử dụng phòng ở | Khoản 8
8. Khi hết hạn ở KTX, SV có trách nhiệm bàn giao chỗ ở cho Giám thị quản lý dãy 
và các tài sản thuộc KTX đúng thời gian, vệ sinh phòng ở và khôi phục lại như hiện trạng 
ban đầu. Nếu quá thời hạn, SV không thực hiện trả phòng, TT. PVSV sẽ tiến hành lập Biên 
bản thu hồi phòng, tài sản của SV còn trong phòng TT. PVSV sẽ không chịu trách nhiệm 
về mất mát và hư hỏng.
```


Báo cáo JSON gốc lưu toàn bộ provider calls, quyết định chấm, lỗi, hash dữ liệu và cấu hình không chứa khóa API.
