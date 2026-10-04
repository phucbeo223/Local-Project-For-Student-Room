# Kết quả workflow Gemini + Qwen: 36 câu

D: Gemini phân tích → Qwen chọn nguồn → Gemini tổng hợp → kiểm chứng và sửa tối đa một lần.

| Chỉ tiêu | A: Gemini chatbot | B: phân tích + trích nguồn | D: agent |
|---|---:|---:|---:|
| Số câu | 36 | 36 | 36 |
| Trả lời một phần | 22 | 21 | 22 |
| Cờ chưa đủ căn cứ | 24 | 21 | 22 |
| Độ trễ trung vị (giây) | 18.2 | 30.7 | 43.4 |
| Độ dài trung vị (ký tự) | 855.5 | 2473.0 | 1299.0 |

D có **28/36 câu** giữ bản tổng hợp Gemini sau kiểm chứng; provider cuối: `{'gemini-agent': 28, 'qwen-local': 8}`.
Có 13 câu gọi sửa bản tổng hợp. Lỗi writer: `{}`.

## Giới hạn đánh giá

- Đây là thống kê vận hành và nguyên văn đầu ra, chưa có điểm đúng pháp luật hay RAGAS mới.
- Đáp án C do người dùng cung cấp là văn bản tham chiếu; không được đưa vào prompt hoặc tự coi là chuẩn pháp lý.
- A/B là các lượt chatbot được lưu trước đó; khác pipeline và thời điểm, so độ trễ chỉ có tính quan sát.
- Lượt D tắt khoảng nghỉ Gemini giữa request để đánh giá; cấu hình pacing môi trường chạy có thể khác.
- Trích dẫn hợp lệ chỉ xác nhận rank; exact_source_match chỉ xác nhận nguyên văn, không xác nhận đủ căn cứ hay hiệu lực.
- Model Gemini là alias do proxy cung cấp; chưa xác nhận danh tính model bên dưới.
- no_answer có thể đánh dấu câu đã trả lời một phần; không đồng nghĩa không có nội dung trả lời.

## Trạng thái từng câu

| Câu | Provider cuối | Một phần | Giây |
|---|---|---|---:|
| 1 | gemini-agent | False | 102.7 |
| 2 | gemini-agent | True | 64.6 |
| 3 | gemini-agent | True | 33.4 |
| 4 | qwen-local | True | 69.0 |
| 5 | gemini-agent | True | 66.9 |
| 6 | qwen-local | True | 76.6 |
| 7 | gemini-agent | True | 78.3 |
| 8 | gemini-agent | True | 75.8 |
| 9 | gemini-agent | True | 42.2 |
| 10 | gemini-agent | True | 38.2 |
| 11 | gemini-agent | True | 34.9 |
| 12 | gemini-agent | True | 39.4 |
| 13 | qwen-local | True | 34.9 |
| 14 | gemini-agent | True | 32.5 |
| 15 | gemini-agent | False | 32.4 |
| 16 | gemini-agent | False | 28.9 |
| 17 | qwen-local | False | 44.6 |
| 18 | gemini-agent | True | 34.6 |
| 19 | gemini-agent | True | 52.5 |
| 20 | gemini-agent | False | 45.8 |
| 21 | gemini-agent | True | 52.9 |
| 22 | gemini-agent | True | 50.9 |
| 23 | gemini-agent | True | 39.4 |
| 24 | gemini-agent | True | 39.2 |
| 25 | qwen-local | False | 45.5 |
| 26 | gemini-agent | False | 47.6 |
| 27 | gemini-agent | False | 36.1 |
| 28 | gemini-agent | False | 50.7 |
| 29 | qwen-local | True | 69.9 |
| 30 | gemini-agent | True | 42.2 |
| 31 | gemini-agent | True | 39.1 |
| 32 | qwen-local | False | 78.8 |
| 33 | gemini-agent | False | 32.7 |
| 34 | gemini-agent | False | 31.0 |
| 35 | qwen-local | False | 98.0 |
| 36 | gemini-agent | False | 32.4 |

## Nguyên văn đối chiếu

Các câu trả lời được đặt cạnh nhau để kiểm tra nội dung, chưa chấm mức khớp hoặc kết luận bên nào đúng pháp luật. JSON giữ nguyên toàn bộ đáp án; bản Markdown chuẩn hóa khoảng trắng cuối dòng.

### Câu 1: Trước khi ký hợp đồng thuê trọ, sinh viên nên kiểm tra những điều khoản nào?

#### A — Gemini chatbot

Mình tìm thấy tài liệu liên quan nhưng chưa tổng hợp được kết luận đáng tin cậy. [1] [2] [3] [4]

- Mở Nguồn tham khảo bên dưới để xem trích đoạn.
- Kiểm tra điều kiện áp dụng và hiệu lực văn bản.

Thông tin tham khảo, không thay thế tư vấn pháp lý.

#### B — Gemini phân tích + Qwen trích nguồn

Các đoạn trả lời trực tiếp trong nguồn:

- Bo-luat-91-2015-QH13-doi-chieu-20261003 — Điều 398. Nội dung của hợp đồng | Khoản 2: “2. Hợp đồng có thể có các nội dung sau đây:

2. Hợp đồng có thể có các nội dung sau đây: a) Đối tượng của hợp đồng;

2. Hợp đồng có thể có các nội dung sau đây: b) Số lượng, chất lượng;

2. Hợp đồng có thể có các nội dung sau đây: c) Giá, phương thức thanh toán;

2. Hợp đồng có thể có các nội dung sau đây: d) Thời hạn, địa điểm, phương thức thực hiện hợp đồng;

2. Hợp đồng có thể có các nội dung sau đây: đ) Quyền, nghĩa vụ của các bên;

2. Hợp đồng có thể có các nội dung sau đây: e) Trách nhiệm do vi phạm hợp đồng;

2. Hợp đồng có thể có các nội dung sau đây: g) Phương thức giải quyết tranh chấp.” [2].

- 2026_204_79_VBHN-VPQH — Điều 163. Hợp đồng về nhà ở | Khoản 2: “2. Mô tả đặc điểm của nhà ở giao dịch và đặc điểm của thửa đất ở gắn với nhà ở đó.

Đối với hợp đồng mua bán, hợp đồng thuê mua căn hộ chung cư thì các bên phải ghi rõ phần sở hữu chung, sử dụng chung; thời hạn sử dụng nhà chung cư theo hồ sơ thiết kế; diện tích sử dụng thuộc quyền sở hữu riêng; diện tích sàn căn hộ; mục đích sử dụng của phần sở hữu chung, sử dụng chung trong nhà chung cư theo đúng mục đích thiết kế đã được phê duyệt; giá dịch vụ quản lý vận hành nhà chung cư trong trường hợp chưa tổ chức Hội nghị nhà chung cư lần đầu; trách nhiệm đóng, mức đóng kinh phí bảo trì và thông tin tài khoản nộp kinh phí bảo trì;” [3].

- Bo-luat-91-2015-QH13-doi-chieu-20261003 — Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp: “Điều 117. Điều kiện có hiệu lực của giao dịch dân sự
Điều 117. Điều kiện có hiệu lực của giao dịch dân sự

Điều 117. Điều kiện có hiệu lực của giao dịch dân sự | Khoản 1
1. Giao dịch dân sự có hiệu lực khi có đủ các điều kiện sau đây:

Điều 117. Điều kiện có hiệu lực của giao dịch dân sự | Khoản 1 | Điểm a
1. Giao dịch dân sự có hiệu lực khi có đủ các điều kiện sau đây: a) Chủ thể có năng lực pháp luật dân sự, năng lực hành vi dân sự phù hợp với giao dịch dân sự được xác lập;

Điều 117. Điều kiện có hiệu lực của giao dịch dân sự | Khoản 1 | Điểm b
1. Giao dịch dân sự có hiệu lực khi có đủ các điều kiện sau đây: b) Chủ thể tham gia giao dịch dân sự hoàn toàn tự nguyện;

Điều 117. Điều kiện có hiệu lực của giao dịch dân sự | Khoản 1 | Điểm c
1. Giao dịch dân sự có hiệu lực khi có đủ các điều kiện sau đây: c) Mục đích và nội dung của giao dịch dân sự không vi phạm điều cấm của luật, không trái đạo đức xã hội.

Điều 117. Điều kiện có hiệu lực của giao dịch dân sự | Khoản 2
2. Hình thức của giao dịch dân sự là điều kiện có hiệu lực của giao dịch dân sự trong trường hợp luật có quy định.

Điều 689. Hiệu lực thi hành
Điều 689. Hiệu lực thi hành Bộ luật này có hiệu lực thi hành từ ngày 01 tháng 01 năm 2017.

Bộ luật dân sự số 33/2005/QH11 hết hiệu lực kể từ ngày Bộ luật này có hiệu lực.

Điều 688. Điều khoản chuyển tiếp
Điều 688. Điều khoản chuyển tiếp

Điều 688. Điều khoản chuyển tiếp | Khoản 1
1. Đối với giao dịch dân sự được xác lập trước ngày Bộ luật này có hiệu lực thì việc áp dụng pháp luật được quy định như sau:

Điều 688. Điều khoản chuyển tiếp | Khoản 1 | Điểm a
1. Đối với giao dịch dân sự được xác lập trước ngày Bộ luật này có hiệu lực thì việc áp dụng pháp luật được quy định như sau: a) Giao dịch dân sự chưa được thực hiện mà có nội dung, hình thức khác với quy định của Bộ luật này thì chủ thể giao dịch tiếp tục thực hiện theo quy định của Bộ luật dân sự số 33/2005/QH11 và các văn bản quy phạm pháp luật quy định chi tiết Bộ luật dân sự số 33/2005/QH11, trừ trường hợp các bên của giao dịch dân sự có thỏa thuận về việc sửa đổi, bổ sung nội dung, hình thức của giao dịch để phù hợp với Bộ luật này và để áp dụng quy định của Bộ luật này.

Giao dịch dân sự đang được thực hiện mà có nội dung, hình thức khác với quy định của Bộ luật này thì áp dụng quy định của Bộ luật dân sự số 33/2005/QH11 và các văn bản quy phạm pháp luật quy định chi tiết Bộ luật dân sự số 33/2005/QH11;

Điều 688. Điều khoản chuyển tiếp | Khoản 1 | Điểm b
1. Đối với giao dịch dân sự được xác lập trước ngày Bộ luật này có hiệu lực thì việc áp dụng pháp luật được quy định như sau: b) Giao dịch dân sự chưa được thực hiện hoặc đang được thực hiện mà có nội dung và hình thức phù hợp với quy định của Bộ luật này thì áp dụng quy định của Bộ luật này;

Điều 688. Điều khoản chuyển tiếp | Khoản 1 | Điểm c
1. Đối với giao dịch dân sự được xác lập trước ngày Bộ luật này có hiệu lực thì việc áp dụng pháp luật được quy định như sau: c) Giao dịch dân sự được thực hiện xong trước ngày Bộ luật này có hiệu lực mà có tranh chấp thì áp dụng quy định của Bộ luật dân sự số 33/2005/QH11 và các văn bản quy phạm pháp luật quy định chi tiết Bộ luật dân sự số 33/2005/QH11 để giải quyết;

Điều 688. Điều khoản chuyển tiếp | Khoản 1 | Điểm d
1. Đối với giao dịch dân sự được xác lập trước ngày Bộ luật này có hiệu lực thì việc áp dụng pháp luật được quy định như sau: d) Thời hiệu được áp dụng theo quy định của Bộ luật này.

Điều 688. Điều khoản chuyển tiếp | Khoản 2
2. Không áp dụng Bộ luật này để kháng nghị theo thủ tục giám đốc thẩm, tái thẩm đối với vụ việc mà Tòa án đã giải quyết theo quy định của pháp luật về dân sự trước ngày Bộ luật này có hiệu lực.” [4].

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng, hiệu lực và bản gốc.

#### C — Đáp án bạn gửi

Khi kiểm tra hợp đồng thuê trọ, sinh viên cần rà soát kỹ 6 nhóm điều khoản cốt lõi sau:
1. **Thông tin các bên & quyền sở hữu:** Tên, CCCD của chủ nhà hoặc người được ủy quyền hợp pháp; địa chỉ chính xác của phòng trọ.
2. **Giá thuê và phương thức thanh toán:** Tiền thuê cố định trong bao lâu? Ngày đóng tiền hàng tháng? Hình thức chuyển khoản hay tiền mặt?
3. **Tiền đặt cọc và điều kiện hoàn cọc:** Số tiền cọc (thường 1 tháng), điều kiện để nhận lại 100% cọc khi hết hạn hợp đồng, và thời hạn chủ nhà phải hoàn trả (ví dụ: trong vòng 3–5 ngày sau khi bàn giao phòng).
4. **Chi phí phát sinh:** Đơn giá điện (VNĐ/kWh), nước (VNĐ/người hoặc VNĐ/m³), internet, rác, gửi xe, phí dịch vụ chung.
5. **Hiện trạng tài sản & sửa chữa:** Biên bản bàn giao liệt kê chi tiết bóng đèn, vòi nước, máy lạnh, quạt, khóa cửa; quy định bên nào chịu phí bảo trì hao mòn tự nhiên.
6. **Chấm dứt hợp đồng trước hạn:** Thời gian phải báo trước (thường 30 ngày) để không bị mất cọc nếu muốn chuyển đi sớm.

#### D — Chatbot dạng agent

Khuyến nghị sinh viên kiểm tra kỹ các điều khoản về đối tượng, giá, thời hạn, quyền nghĩa vụ và phương thức giải quyết tranh chấp trong hợp đồng [2].

- Khuyến nghị kiểm tra thông tin về đối tượng của hợp đồng, số lượng, chất lượng cùng mô tả đặc điểm của nhà ở giao dịch và thửa đất ở gắn liền [2] [3].
- Khuyến nghị xem xét điều khoản về giá thuê và phương thức thanh toán [2].
- Khuyến nghị đối chiếu thời hạn, địa điểm và phương thức thực hiện hợp đồng thuê trọ [2].
- Khuyến nghị rà soát quyền, nghĩa vụ của các bên cùng trách nhiệm do vi phạm hợp đồng và phương thức giải quyết tranh chấp [2].
- Khuyến nghị kiểm tra tính tự nguyện của các bên và bảo đảm nội dung thỏa thuận không vi phạm điều cấm của luật, không trái đạo đức xã hội [4].

Giao dịch dân sự có hiệu lực khi có đủ các điều kiện theo quy định tại Điều 117 và hình thức là điều kiện có hiệu lực trong trường hợp luật có quy định [4].
Nguồn tài liệu chưa cung cấp đầy đủ các quy định riêng biệt hoặc đặc thù áp dụng cho sinh viên thuê trọ tư nhân [2] [3].

Để áp dụng vào trường hợp của bạn:
- Bạn dự định thuê phòng trọ cá nhân hay thuê căn hộ chung cư?
- Bên cho thuê đã cung cấp bản dự thảo hợp đồng cụ thể chưa?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

Nguồn truy xuất của D (rank dùng trong trích dẫn):

- [1] 2026_204_79_VBHN-VPQH — Điều 164. Công chứng, chứng thực hợp đồng và thời điểm có hiệu lực của hợp đồng về nhà ở | Khoản 2
- [2] Bo-luat-91-2015-QH13-doi-chieu-20261003 — Điều 398. Nội dung của hợp đồng | Khoản 2
- [3] 2026_204_79_VBHN-VPQH — Điều 163. Hợp đồng về nhà ở | Khoản 2
- [4] Bo-luat-91-2015-QH13-doi-chieu-20261003 — Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp

### Câu 2: Hợp đồng thuê phòng có cần ghi rõ tiền cọc, tiền thuê và ngày thanh toán không?

#### A — Gemini chatbot

Các căn cứ liên quan tìm được trong kho (trích nguyên đoạn):

- Bo-luat-91-2015-QH13-doi-chieu-20261003 — Điều 328. Đặt cọc | Khoản 1: “1. Đặt cọc là việc một bên (sau đây gọi là bên đặt cọc) giao cho bên kia (sau đây gọi là bên nhận đặt cọc) một khoản tiền hoặc kim khí quý, đá quý hoặc vật có giá trị khác (sau đây gọi chung là tài sản đặt cọc) trong một thời hạn để bảo đảm giao kết hoặc thực hiện hợp đồng.” [1].

- 2026_204_79_VBHN-VPQH — Điều 163. Hợp đồng về nhà ở | Khoản 4: “4. Thời hạn và phương thức thanh toán tiền nếu là trường hợp mua bán, cho thuê mua, cho thuê nhà ở;” [3].

Đây là câu trả lời một phần từ nguồn; chưa kết luận cách áp dụng cho tình huống riêng của bạn. Cần đối chiếu điều kiện, hiệu lực và bản gốc.

#### B — Gemini phân tích + Qwen trích nguồn

Các đoạn trả lời trực tiếp trong nguồn:

- Bo-luat-91-2015-QH13-doi-chieu-20261003 — Điều 328. Đặt cọc | Khoản 1: “1. Đặt cọc là việc một bên (sau đây gọi là bên đặt cọc) giao cho bên kia (sau đây gọi là bên nhận đặt cọc) một khoản tiền hoặc kim khí quý, đá quý hoặc vật có giá trị khác (sau đây gọi chung là tài sản đặt cọc) trong một thời hạn để bảo đảm giao kết hoặc thực hiện hợp đồng.” [1].

- 2026_204_79_VBHN-VPQH — Điều 163. Hợp đồng về nhà ở | Khoản 3: “3. Giá trị góp vốn, giá giao dịch nhà ở nếu hợp đồng có thỏa thuận về giá; trường hợp mua bán, cho thuê mua, cho thuê nhà ở mà Nhà nước có quy định về giá thì các bên phải thực hiện theo quy định đó;” [2].

- 2026_204_79_VBHN-VPQH — Điều 163. Hợp đồng về nhà ở | Khoản 4: “4. Thời hạn và phương thức thanh toán tiền nếu là trường hợp mua bán, cho thuê mua, cho thuê nhà ở;” [3].

- Bo-luat-91-2015-QH13-doi-chieu-20261003 — Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp: “Điều 117. Điều kiện có hiệu lực của giao dịch dân sự
Điều 117. Điều kiện có hiệu lực của giao dịch dân sự

Điều 117. Điều kiện có hiệu lực của giao dịch dân sự | Khoản 1
1. Giao dịch dân sự có hiệu lực khi có đủ các điều kiện sau đây:

Điều 117. Điều kiện có hiệu lực của giao dịch dân sự | Khoản 1 | Điểm a
1. Giao dịch dân sự có hiệu lực khi có đủ các điều kiện sau đây: a) Chủ thể có năng lực pháp luật dân sự, năng lực hành vi dân sự phù hợp với giao dịch dân sự được xác lập;

Điều 117. Điều kiện có hiệu lực của giao dịch dân sự | Khoản 1 | Điểm b
1. Giao dịch dân sự có hiệu lực khi có đủ các điều kiện sau đây: b) Chủ thể tham gia giao dịch dân sự hoàn toàn tự nguyện;

Điều 117. Điều kiện có hiệu lực của giao dịch dân sự | Khoản 1 | Điểm c
1. Giao dịch dân sự có hiệu lực khi có đủ các điều kiện sau đây: c) Mục đích và nội dung của giao dịch dân sự không vi phạm điều cấm của luật, không trái đạo đức xã hội.

Điều 117. Điều kiện có hiệu lực của giao dịch dân sự | Khoản 2
2. Hình thức của giao dịch dân sự là điều kiện có hiệu lực của giao dịch dân sự trong trường hợp luật có quy định.

Điều 689. Hiệu lực thi hành
Điều 689. Hiệu lực thi hành Bộ luật này có hiệu lực thi hành từ ngày 01 tháng 01 năm 2017.

Bộ luật dân sự số 33/2005/QH11 hết hiệu lực kể từ ngày Bộ luật này có hiệu lực.

Điều 688. Điều khoản chuyển tiếp
Điều 688. Điều khoản chuyển tiếp

Điều 688. Điều khoản chuyển tiếp | Khoản 1
1. Đối với giao dịch dân sự được xác lập trước ngày Bộ luật này có hiệu lực thì việc áp dụng pháp luật được quy định như sau:

Điều 688. Điều khoản chuyển tiếp | Khoản 1 | Điểm a
1. Đối với giao dịch dân sự được xác lập trước ngày Bộ luật này có hiệu lực thì việc áp dụng pháp luật được quy định như sau: a) Giao dịch dân sự chưa được thực hiện mà có nội dung, hình thức khác với quy định của Bộ luật này thì chủ thể giao dịch tiếp tục thực hiện theo quy định của Bộ luật dân sự số 33/2005/QH11 và các văn bản quy phạm pháp luật quy định chi tiết Bộ luật dân sự số 33/2005/QH11, trừ trường hợp các bên của giao dịch dân sự có thỏa thuận về việc sửa đổi, bổ sung nội dung, hình thức của giao dịch để phù hợp với Bộ luật này và để áp dụng quy định của Bộ luật này.

Giao dịch dân sự đang được thực hiện mà có nội dung, hình thức khác với quy định của Bộ luật này thì áp dụng quy định của Bộ luật dân sự số 33/2005/QH11 và các văn bản quy phạm pháp luật quy định chi tiết Bộ luật dân sự số 33/2005/QH11;

Điều 688. Điều khoản chuyển tiếp | Khoản 1 | Điểm b
1. Đối với giao dịch dân sự được xác lập trước ngày Bộ luật này có hiệu lực thì việc áp dụng pháp luật được quy định như sau: b) Giao dịch dân sự chưa được thực hiện hoặc đang được thực hiện mà có nội dung và hình thức phù hợp với quy định của Bộ luật này thì áp dụng quy định của Bộ luật này;

Điều 688. Điều khoản chuyển tiếp | Khoản 1 | Điểm c
1. Đối với giao dịch dân sự được xác lập trước ngày Bộ luật này có hiệu lực thì việc áp dụng pháp luật được quy định như sau: c) Giao dịch dân sự được thực hiện xong trước ngày Bộ luật này có hiệu lực mà có tranh chấp thì áp dụng quy định của Bộ luật dân sự số 33/2005/QH11 và các văn bản quy phạm pháp luật quy định chi tiết Bộ luật dân sự số 33/2005/QH11 để giải quyết;

Điều 688. Điều khoản chuyển tiếp | Khoản 1 | Điểm d
1. Đối với giao dịch dân sự được xác lập trước ngày Bộ luật này có hiệu lực thì việc áp dụng pháp luật được quy định như sau: d) Thời hiệu được áp dụng theo quy định của Bộ luật này.

Điều 688. Điều khoản chuyển tiếp | Khoản 2
2. Không áp dụng Bộ luật này để kháng nghị theo thủ tục giám đốc thẩm, tái thẩm đối với vụ việc mà Tòa án đã giải quyết theo quy định của pháp luật về dân sự trước ngày Bộ luật này có hiệu lực.” [4].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng; cần đối chiếu phần còn thiếu.

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng, hiệu lực và bản gốc.

#### C — Đáp án bạn gửi

**Rất cần thiết và bắt buộc phải ghi rõ.**
Theo Điều 472 và Điều 473 Bộ luật Dân sự 2015, hợp đồng thuê tài sản là sự thỏa thuận giữa các bên. Việc ghi rõ:
- **Tiền đặt cọc:** Là biện pháp bảo đảm thực hiện nghĩa vụ theo Điều 328 BLDS 2015. Hợp đồng phải ghi rõ mục đích cọc, mức cọc và điều kiện hoàn trả cọc.
- **Tiền thuê:** Tránh việc chủ trọ tự ý tăng giá bất ngờ.
- **Ngày thanh toán:** Xác định mốc thời gian để người thuê không bị coi là chậm trễ nghĩa vụ thanh toán hoặc bị phạt tiền trễ hạn vô lý.
*Lưu ý:* Sinh viên tuyệt đối không ký các mẫu hợp đồng để trống mục tiền cọc hoặc chỉ thỏa thuận miệng về chi phí.

#### D — Chatbot dạng agent

Hợp đồng về nhà ở có thỏa thuận giá phải có giá giao dịch, thời hạn và phương thức thanh toán, nhưng nguồn chưa đủ căn cứ quy định bắt buộc phải ghi khoản tiền cọc [2] [3].

- Thỏa thuận rõ giá thuê nhà ở trong hợp đồng hoặc thực hiện theo quy định nếu Nhà nước có quy định về giá [2].
- Ghi nhận rõ thời hạn và phương thức thanh toán tiền trong hợp đồng cho thuê nhà ở [3].
- Xác lập thỏa thuận đặt cọc bằng tài sản đặt cọc trong một thời hạn cụ thể nếu các bên có nhu cầu bảo đảm giao kết hoặc thực hiện hợp đồng [1].
- Đảm bảo các bên tham gia hoàn toàn tự nguyện, có đủ năng lực chủ thể phù hợp và nội dung hợp đồng không vi phạm điều cấm của luật, không trái đạo đức xã hội [4].

Nguồn trích dẫn không quy định cụ thể việc bắt buộc ghi điều khoản đặt cọc vào chung hợp đồng thuê phòng hay lập thành văn bản riêng [1] [2] [3].
Trường hợp thuê nhà ở mà Nhà nước có quy định về giá thì các bên phải tuân thủ mức giá theo quy định đó [2].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng.

Để áp dụng vào trường hợp của bạn:
- Hợp đồng thuê phòng của bạn thuộc đối tượng nhà ở do Nhà nước quy định giá hay hoàn toàn theo giá thỏa thuận?
- Các bên đã ký thỏa thuận hoặc biên bản giao nhận tiền đặt cọc riêng chưa?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

Nguồn truy xuất của D (rank dùng trong trích dẫn):

- [1] Bo-luat-91-2015-QH13-doi-chieu-20261003 — Điều 328. Đặt cọc | Khoản 1
- [2] 2026_204_79_VBHN-VPQH — Điều 163. Hợp đồng về nhà ở | Khoản 3
- [3] 2026_204_79_VBHN-VPQH — Điều 163. Hợp đồng về nhà ở | Khoản 4
- [4] Bo-luat-91-2015-QH13-doi-chieu-20261003 — Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp

Lý do giới hạn/fallback của D:

- Phản hồi chưa đáp ứng đầy đủ yêu cầu chính; đánh dấu theo nội dung thay vì provider.

### Câu 3: Nếu chủ trọ muốn tăng giá thuê giữa thời hạn hợp đồng thì cần xem xét những gì?

#### A — Gemini chatbot

Dựa trên văn bản được cung cấp, việc tăng giá thuê giữa thời hạn hợp đồng cần xem xét các nội dung sau:

* Giá thuê nhà ở do các bên thỏa thuận hoặc thực hiện theo quy định của Nhà nước nếu có quy định [2, 3] (nguồn [2], [3], văn bản 2026_204_79_VBHN-VPQH, Điều 163 Khoản 3 và Điều 170 Khoản 1, trang 1). Khuyến nghị: nên kiểm tra nội dung hợp đồng đã ký về các điều khoản thỏa thuận điều chỉnh giá giữa kỳ.
* Trường hợp cải tạo nhà ở và được bên thuê đồng ý, bên cho thuê được quyền điều chỉnh giá thuê nếu thời gian cho thuê còn lại từ một phần ba thời hạn hợp đồng trở xuống [1] (nguồn [1], văn bản 2026_204_79_VBHN-VPQH, Điều 170 Khoản 2, trang 1).
* Mức giá thuê mới do các bên thỏa thuận; nếu không thỏa thuận được, bên cho thuê có quyền đơn phương chấm dứt hợp đồng nhưng phải bồi thường cho bên thuê theo quy định của pháp luật [1] (nguồn [1], văn bản 2026_204_79_VBHN-VPQH, Điều 170 Khoản 2, trang 1).

*Lưu ý: Đây là thông tin tham khảo, không thay thế tư vấn pháp lý chuyên nghiệp.*

#### B — Gemini phân tích + Qwen trích nguồn

Các đoạn trả lời trực tiếp trong nguồn:

- 2026_204_79_VBHN-VPQH — Điều 170. Thời hạn thuê, giá thuê, cho thuê lại nhà ở | Khoản 2: “2. Trường hợp bên cho thuê thực hiện cải tạo nhà ở và được bên thuê đồng ý thì bên cho thuê được quyền điều chỉnh giá thuê nhà ở nếu thời gian cho thuê còn lại từ một phần ba thời hạn của hợp đồng thuê nhà ở trở xuống. Giá thuê nhà ở mới do các bên thỏa thuận; trường hợp không thỏa thuận được thì bên cho thuê có quyền đơn phương chấm dứt hợp đồng thuê nhà ở và phải bồi thường cho bên thuê theo quy định của pháp luật.” [1].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng; cần đối chiếu phần còn thiếu.

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng, hiệu lực và bản gốc.

#### C — Đáp án bạn gửi

Theo quy định tại Luật Nhà ở 2023 và Bộ luật Dân sự 2015:
1. **Kiểm tra điều khoản thỏa thuận trong hợp đồng:** Trong thời hạn hợp đồng còn hiệu lực, bên cho thuê **không được quyền tự ý điều chỉnh tăng giá thuê** trừ trường hợp trong hợp đồng có điều khoản cho phép tăng giá theo định kỳ hoặc có thỏa thuận trước.
2. **Nếu hợp đồng không quy định việc tăng giá:** Chủ trọ đơn phương tăng giá là **vi phạm hợp đồng**. Người thuê có quyền từ chối mức tăng này và tiếp tục đóng mức giá cũ đến hết thời hạn hợp đồng.
3. **Nếu chủ trọ ép buộc hoặc đòi đuổi người thuê:** Đây là hành vi vi phạm nghĩa vụ bàn giao và duy trì tài sản thuê (Điều 477 BLDS 2015). Người thuê có quyền yêu cầu hoàn trả cọc và bồi thường thiệt hại (nếu có).

#### D — Chatbot dạng agent

Bên cho thuê được quyền điều chỉnh giá thuê nhà ở giữa thời hạn hợp đồng nếu thực hiện cải tạo nhà ở, được bên thuê đồng ý và thời gian cho thuê còn lại từ một phần ba thời hạn hợp đồng trở xuống [1].

- Kiểm tra xem chủ trọ có thực hiện cải tạo nhà ở và đã nhận được sự đồng ý của bên thuê hay chưa [1].
- Xác định thời gian thuê còn lại theo hợp đồng để đối chiếu xem có từ một phần ba thời hạn thuê trở xuống hay không [1].
- Hai bên tiến hành thỏa thuận mức giá thuê nhà ở mới áp dụng sau khi cải tạo [1].
- Trường hợp không thỏa thuận được giá mới, xem xét việc chủ trọ có quyền đơn phương chấm dứt hợp đồng và phải bồi thường cho bên thuê theo luật định [1].

Nguồn trích dẫn chỉ quy định trường hợp tăng giá khi cải tạo nhà ở và chưa đủ căn cứ cho các lý do tăng giá khác giữa thời hạn hợp đồng [1].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng.

Để áp dụng vào trường hợp của bạn:
- Chủ trọ yêu cầu tăng giá thuê với lý do cải tạo nhà hay vì lý do nào khác?
- Hợp đồng thuê phòng của bạn còn lại bao nhiêu thời gian và có điều khoản thỏa thuận riêng về tăng giá không?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

Nguồn truy xuất của D (rank dùng trong trích dẫn):

- [1] 2026_204_79_VBHN-VPQH — Điều 170. Thời hạn thuê, giá thuê, cho thuê lại nhà ở | Khoản 2
- [2] 2026_204_79_VBHN-VPQH — Điều 170. Thời hạn thuê, giá thuê, cho thuê lại nhà ở | Khoản 1
- [3] 2026_204_79_VBHN-VPQH — Điều 163. Hợp đồng về nhà ở | Khoản 3

Lý do giới hạn/fallback của D:

- Phản hồi chưa đáp ứng đầy đủ yêu cầu chính; đánh dấu theo nội dung thay vì provider.

### Câu 4: Khi trả phòng, việc hoàn lại tiền cọc được xác định theo hợp đồng và quy định như thế nào?

#### A — Gemini chatbot

- Đặt cọc là việc bên đặt cọc giao cho bên nhận đặt cọc một khoản tiền hoặc vật có giá trị trong một thời hạn để bảo đảm giao kết hoặc thực hiện hợp đồng theo nguồn [2] Điều 328 Khoản 1 trang 1.
- Khi hợp đồng được giao kết, thực hiện thì tài sản đặt cọc được trả lại cho bên đặt cọc hoặc được trừ để thực hiện nghĩa vụ trả tiền theo nguồn [1] Điều 328 Khoản 2 trang 1; nếu bên đặt cọc từ chối thực hiện hợp đồng thì tài sản thuộc về bên nhận đặt cọc, còn nếu bên nhận đặt cọc từ chối thì phải trả lại tài sản đặt cọc và một khoản tiền tương đương, trừ trường hợp có thỏa thuận khác theo nguồn [1] Điều 328 Khoản 2 trang 1.
- Khuyến nghị: nên kiểm tra và đối chiếu các thỏa thuận trong hợp đồng thuê trọ vì việc hoàn trả tiền cọc ưu tiên áp dụng theo thỏa thuận của các bên; hiện chưa tìm thấy căn cứ về quy trình trả cọc cụ thể tại thời điểm trả phòng trong các đoạn được cung cấp.

Lưu ý: Đây là thông tin tham khảo, không thay thế tư vấn pháp lý chuyên nghiệp.

#### B — Gemini phân tích + Qwen trích nguồn

Các đoạn trả lời trực tiếp trong nguồn:

- Bo-luat-91-2015-QH13-doi-chieu-20261003 — Điều 328. Đặt cọc | Khoản 2: “2. Trường hợp hợp đồng được giao kết, thực hiện thì tài sản đặt cọc được trả lại cho bên đặt cọc hoặc được trừ để thực hiện nghĩa vụ trả tiền; nếu bên đặt cọc từ chối việc giao kết, thực hiện hợp đồng thì tài sản đặt cọc thuộc về bên nhận đặt cọc; nếu bên nhận đặt cọc từ chối việc giao kết, thực hiện hợp đồng thì phải trả cho bên đặt cọc tài sản đặt cọc và một khoản tiền tương đương giá trị tài sản đặt cọc, trừ trường hợp có thoả thuận khác.” [1].

- Bo-luat-91-2015-QH13-doi-chieu-20261003 — Điều 328. Đặt cọc | Khoản 1: “1. Đặt cọc là việc một bên (sau đây gọi là bên đặt cọc) giao cho bên kia (sau đây gọi là bên nhận đặt cọc) một khoản tiền hoặc kim khí quý, đá quý hoặc vật có giá trị khác (sau đây gọi chung là tài sản đặt cọc) trong một thời hạn để bảo đảm giao kết hoặc thực hiện hợp đồng.” [2].

- Bo-luat-91-2015-QH13-doi-chieu-20261003 — Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp: “Điều 117. Điều kiện có hiệu lực của giao dịch dân sự
Điều 117. Điều kiện có hiệu lực của giao dịch dân sự

Điều 117. Điều kiện có hiệu lực của giao dịch dân sự | Khoản 1
1. Giao dịch dân sự có hiệu lực khi có đủ các điều kiện sau đây:

Điều 117. Điều kiện có hiệu lực của giao dịch dân sự | Khoản 1 | Điểm a
1. Giao dịch dân sự có hiệu lực khi có đủ các điều kiện sau đây: a) Chủ thể có năng lực pháp luật dân sự, năng lực hành vi dân sự phù hợp với giao dịch dân sự được xác lập;

Điều 117. Điều kiện có hiệu lực của giao dịch dân sự | Khoản 1 | Điểm b
1. Giao dịch dân sự có hiệu lực khi có đủ các điều kiện sau đây: b) Chủ thể tham gia giao dịch dân sự hoàn toàn tự nguyện;

Điều 117. Điều kiện có hiệu lực của giao dịch dân sự | Khoản 1 | Điểm c
1. Giao dịch dân sự có hiệu lực khi có đủ các điều kiện sau đây: c) Mục đích và nội dung của giao dịch dân sự không vi phạm điều cấm của luật, không trái đạo đức xã hội.

Điều 117. Điều kiện có hiệu lực của giao dịch dân sự | Khoản 2
2. Hình thức của giao dịch dân sự là điều kiện có hiệu lực của giao dịch dân sự trong trường hợp luật có quy định.

Điều 689. Hiệu lực thi hành
Điều 689. Hiệu lực thi hành Bộ luật này có hiệu lực thi hành từ ngày 01 tháng 01 năm 2017.

Bộ luật dân sự số 33/2005/QH11 hết hiệu lực kể từ ngày Bộ luật này có hiệu lực.

Điều 688. Điều khoản chuyển tiếp
Điều 688. Điều khoản chuyển tiếp

Điều 688. Điều khoản chuyển tiếp | Khoản 1
1. Đối với giao dịch dân sự được xác lập trước ngày Bộ luật này có hiệu lực thì việc áp dụng pháp luật được quy định như sau:

Điều 688. Điều khoản chuyển tiếp | Khoản 1 | Điểm a
1. Đối với giao dịch dân sự được xác lập trước ngày Bộ luật này có hiệu lực thì việc áp dụng pháp luật được quy định như sau: a) Giao dịch dân sự chưa được thực hiện mà có nội dung, hình thức khác với quy định của Bộ luật này thì chủ thể giao dịch tiếp tục thực hiện theo quy định của Bộ luật dân sự số 33/2005/QH11 và các văn bản quy phạm pháp luật quy định chi tiết Bộ luật dân sự số 33/2005/QH11, trừ trường hợp các bên của giao dịch dân sự có thỏa thuận về việc sửa đổi, bổ sung nội dung, hình thức của giao dịch để phù hợp với Bộ luật này và để áp dụng quy định của Bộ luật này.

Giao dịch dân sự đang được thực hiện mà có nội dung, hình thức khác với quy định của Bộ luật này thì áp dụng quy định của Bộ luật dân sự số 33/2005/QH11 và các văn bản quy phạm pháp luật quy định chi tiết Bộ luật dân sự số 33/2005/QH11;

Điều 688. Điều khoản chuyển tiếp | Khoản 1 | Điểm b
1. Đối với giao dịch dân sự được xác lập trước ngày Bộ luật này có hiệu lực thì việc áp dụng pháp luật được quy định như sau: b) Giao dịch dân sự chưa được thực hiện hoặc đang được thực hiện mà có nội dung và hình thức phù hợp với quy định của Bộ luật này thì áp dụng quy định của Bộ luật này;

Điều 688. Điều khoản chuyển tiếp | Khoản 1 | Điểm c
1. Đối với giao dịch dân sự được xác lập trước ngày Bộ luật này có hiệu lực thì việc áp dụng pháp luật được quy định như sau: c) Giao dịch dân sự được thực hiện xong trước ngày Bộ luật này có hiệu lực mà có tranh chấp thì áp dụng quy định của Bộ luật dân sự số 33/2005/QH11 và các văn bản quy phạm pháp luật quy định chi tiết Bộ luật dân sự số 33/2005/QH11 để giải quyết;

Điều 688. Điều khoản chuyển tiếp | Khoản 1 | Điểm d
1. Đối với giao dịch dân sự được xác lập trước ngày Bộ luật này có hiệu lực thì việc áp dụng pháp luật được quy định như sau: d) Thời hiệu được áp dụng theo quy định của Bộ luật này.

Điều 688. Điều khoản chuyển tiếp | Khoản 2
2. Không áp dụng Bộ luật này để kháng nghị theo thủ tục giám đốc thẩm, tái thẩm đối với vụ việc mà Tòa án đã giải quyết theo quy định của pháp luật về dân sự trước ngày Bộ luật này có hiệu lực.” [4].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng; cần đối chiếu phần còn thiếu.

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng, hiệu lực và bản gốc.

#### C — Đáp án bạn gửi

Căn cứ theo **Khoản 2 Điều 328 Bộ luật Dân sự 2015**:
- Khi hợp đồng thuê chấm dứt đúng thời hạn, bên thuê đã thanh toán đủ tiền nhà, điện nước và bàn giao lại phòng theo đúng hiện trạng (trừ hao mòn tự nhiên), thì **chủ nhà có nghĩa vụ hoàn trả lại toàn bộ số tiền đặt cọc cho người thuê**.
- Chủ nhà chỉ có quyền khấu trừ cọc khi: Người thuê làm hư hỏng tài sản do lỗi chủ quan, nợ tiền nhà/điện nước chưa trả, hoặc đơn phương chấm dứt hợp đồng trái với thời gian báo trước đã cam kết.
- **Kinh nghiệm:** Sinh viên nên chụp ảnh/quay video phòng lúc nhận phòng và lúc dọn đi để làm bằng chứng đối chiếu.

#### D — Chatbot dạng agent

Các đoạn trả lời trực tiếp trong nguồn:

- Bo-luat-91-2015-QH13-doi-chieu-20261003 — Điều 328. Đặt cọc | Khoản 2: “2. Trường hợp hợp đồng được giao kết, thực hiện thì tài sản đặt cọc được trả lại cho bên đặt cọc hoặc được trừ để thực hiện nghĩa vụ trả tiền; nếu bên đặt cọc từ chối việc giao kết, thực hiện hợp đồng thì tài sản đặt cọc thuộc về bên nhận đặt cọc; nếu bên nhận đặt cọc từ chối việc giao kết, thực hiện hợp đồng thì phải trả cho bên đặt cọc tài sản đặt cọc và một khoản tiền tương đương giá trị tài sản đặt cọc, trừ trường hợp có thoả thuận khác.” [1].

- Bo-luat-91-2015-QH13-doi-chieu-20261003 — Điều 328. Đặt cọc | Khoản 1: “1. Đặt cọc là việc một bên (sau đây gọi là bên đặt cọc) giao cho bên kia (sau đây gọi là bên nhận đặt cọc) một khoản tiền hoặc kim khí quý, đá quý hoặc vật có giá trị khác (sau đây gọi chung là tài sản đặt cọc) trong một thời hạn để bảo đảm giao kết hoặc thực hiện hợp đồng.” [2].

- Bo-luat-91-2015-QH13-doi-chieu-20261003 — Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp: “Điều 117. Điều kiện có hiệu lực của giao dịch dân sự
Điều 117. Điều kiện có hiệu lực của giao dịch dân sự

Điều 117. Điều kiện có hiệu lực của giao dịch dân sự | Khoản 1
1. Giao dịch dân sự có hiệu lực khi có đủ các điều kiện sau đây:

Điều 117. Điều kiện có hiệu lực của giao dịch dân sự | Khoản 1 | Điểm a
1. Giao dịch dân sự có hiệu lực khi có đủ các điều kiện sau đây: a) Chủ thể có năng lực pháp luật dân sự, năng lực hành vi dân sự phù hợp với giao dịch dân sự được xác lập;

Điều 117. Điều kiện có hiệu lực của giao dịch dân sự | Khoản 1 | Điểm b
1. Giao dịch dân sự có hiệu lực khi có đủ các điều kiện sau đây: b) Chủ thể tham gia giao dịch dân sự hoàn toàn tự nguyện;

Điều 117. Điều kiện có hiệu lực của giao dịch dân sự | Khoản 1 | Điểm c
1. Giao dịch dân sự có hiệu lực khi có đủ các điều kiện sau đây: c) Mục đích và nội dung của giao dịch dân sự không vi phạm điều cấm của luật, không trái đạo đức xã hội.

Điều 117. Điều kiện có hiệu lực của giao dịch dân sự | Khoản 2
2. Hình thức của giao dịch dân sự là điều kiện có hiệu lực của giao dịch dân sự trong trường hợp luật có quy định.

Điều 689. Hiệu lực thi hành
Điều 689. Hiệu lực thi hành Bộ luật này có hiệu lực thi hành từ ngày 01 tháng 01 năm 2017.

Bộ luật dân sự số 33/2005/QH11 hết hiệu lực kể từ ngày Bộ luật này có hiệu lực.

Điều 688. Điều khoản chuyển tiếp
Điều 688. Điều khoản chuyển tiếp

Điều 688. Điều khoản chuyển tiếp | Khoản 1
1. Đối với giao dịch dân sự được xác lập trước ngày Bộ luật này có hiệu lực thì việc áp dụng pháp luật được quy định như sau:

Điều 688. Điều khoản chuyển tiếp | Khoản 1 | Điểm a
1. Đối với giao dịch dân sự được xác lập trước ngày Bộ luật này có hiệu lực thì việc áp dụng pháp luật được quy định như sau: a) Giao dịch dân sự chưa được thực hiện mà có nội dung, hình thức khác với quy định của Bộ luật này thì chủ thể giao dịch tiếp tục thực hiện theo quy định của Bộ luật dân sự số 33/2005/QH11 và các văn bản quy phạm pháp luật quy định chi tiết Bộ luật dân sự số 33/2005/QH11, trừ trường hợp các bên của giao dịch dân sự có thỏa thuận về việc sửa đổi, bổ sung nội dung, hình thức của giao dịch để phù hợp với Bộ luật này và để áp dụng quy định của Bộ luật này.

Giao dịch dân sự đang được thực hiện mà có nội dung, hình thức khác với quy định của Bộ luật này thì áp dụng quy định của Bộ luật dân sự số 33/2005/QH11 và các văn bản quy phạm pháp luật quy định chi tiết Bộ luật dân sự số 33/2005/QH11;

Điều 688. Điều khoản chuyển tiếp | Khoản 1 | Điểm b
1. Đối với giao dịch dân sự được xác lập trước ngày Bộ luật này có hiệu lực thì việc áp dụng pháp luật được quy định như sau: b) Giao dịch dân sự chưa được thực hiện hoặc đang được thực hiện mà có nội dung và hình thức phù hợp với quy định của Bộ luật này thì áp dụng quy định của Bộ luật này;

Điều 688. Điều khoản chuyển tiếp | Khoản 1 | Điểm c
1. Đối với giao dịch dân sự được xác lập trước ngày Bộ luật này có hiệu lực thì việc áp dụng pháp luật được quy định như sau: c) Giao dịch dân sự được thực hiện xong trước ngày Bộ luật này có hiệu lực mà có tranh chấp thì áp dụng quy định của Bộ luật dân sự số 33/2005/QH11 và các văn bản quy phạm pháp luật quy định chi tiết Bộ luật dân sự số 33/2005/QH11 để giải quyết;

Điều 688. Điều khoản chuyển tiếp | Khoản 1 | Điểm d
1. Đối với giao dịch dân sự được xác lập trước ngày Bộ luật này có hiệu lực thì việc áp dụng pháp luật được quy định như sau: d) Thời hiệu được áp dụng theo quy định của Bộ luật này.

Điều 688. Điều khoản chuyển tiếp | Khoản 2
2. Không áp dụng Bộ luật này để kháng nghị theo thủ tục giám đốc thẩm, tái thẩm đối với vụ việc mà Tòa án đã giải quyết theo quy định của pháp luật về dân sự trước ngày Bộ luật này có hiệu lực.” [4].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng; cần đối chiếu phần còn thiếu.

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng, hiệu lực và bản gốc.

Nguồn truy xuất của D (rank dùng trong trích dẫn):

- [1] Bo-luat-91-2015-QH13-doi-chieu-20261003 — Điều 328. Đặt cọc | Khoản 2
- [2] Bo-luat-91-2015-QH13-doi-chieu-20261003 — Điều 328. Đặt cọc | Khoản 1
- [3] 2026_204_79_VBHN-VPQH — Điều 172. Đơn phương chấm dứt thực hiện hợp đồng thuê nhà ở | Khoản 2
- [4] Bo-luat-91-2015-QH13-doi-chieu-20261003 — Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp

Lý do giới hạn/fallback của D:

- Kết luận hoặc số liệu chưa gắn trích dẫn trực tiếp.
- Bản tổng hợp chưa được nguồn xác nhận sau lần sửa; dùng trích đoạn Qwen đã chọn.
- Phản hồi chưa đáp ứng đầy đủ yêu cầu chính; đánh dấu theo nội dung thay vì provider.

### Câu 5: Chủ trọ được thu tiền điện của người thuê như thế nào theo quy định?

#### A — Gemini chatbot

Giới hạn thu tiền điện:

- Điều 12. Giá bán lẻ điện sinh hoạt | Khoản 5: “Trường hợp người thuê nhà không giao kết hợp đồng trực tiếp với bên bán điện thì tổng tiền điện chủ nhà cho thuê thu của người thuê nhà không được vượt quá tiền điện trong hoá đơn tiền điện hằng tháng do đơn vị bán lẻ điện phát hành;” [1]

Điều kiện hiệu lực trong nguồn: “có hiệu lực thi hành kể từ ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành” [3].

Thông tin tham khảo từ văn bản đã trích xuất; cần đối chiếu điều kiện áp dụng và bản gốc.

#### B — Gemini phân tích + Qwen trích nguồn

Các đoạn trả lời trực tiếp trong nguồn:

- Thông-tư-60-2025-TT-BCT — Điều 12. Giá bán lẻ điện sinh hoạt | Khoản 5: “5. Bên mua điện sử dụng vào mục đích sinh hoạt của người thuê nhà để ở áp dụng như sau:

5. Bên mua điện sử dụng vào mục đích sinh hoạt của người thuê nhà để ở áp dụng như sau: a) Tại mỗi địa chỉ nhà cho thuê, bên bán điện chỉ giao kết một hợp đồng mua bán điện duy nhất. Chủ nhà cho thuê có trách nhiệm cung cấp thông tin về cư trú tại địa điểm sử dụng điện của người thuê nhà;

5. Bên mua điện sử dụng vào mục đích sinh hoạt của người thuê nhà để ở áp dụng như sau: b) Đối với trường hợp cho hộ gia đình thuê: Chủ nhà trực tiếp giao kết hợp đồng mua bán điện hoặc ủy quyền cho hộ gia đình thuê nhà giao kết hợp đồng mua bán điện (có cam kết thanh toán tiền điện), mỗi hộ gia đình thuê nhà được tính một định mức;

Ghi chú tuyển chọn: Điểm c khoản 5 về sinh viên/người lao động thuê nhà có mốc hiệu lực riêng tại khoản 1 Điều 21; không mặc nhiên áp dụng từ 02/12/2025.

5. Bên mua điện sử dụng vào mục đích sinh hoạt của người thuê nhà để ở áp dụng như sau: c) Trường hợp cho sinh viên và người lao động thuê nhà (bên thuê nhà không phải là một hộ gia đình):

- Đối với trường hợp bên thuê nhà có hợp đồng thuê nhà từ 12 tháng trở lên và có đăng ký tạm trú, thường trú (xác định theo thông tin về cư trú tại địa điểm sử dụng điện) thì chủ nhà trực tiếp giao kết hợp đồng mua bán điện hoặc đại diện bên thuê nhà giao kết hợp đồng mua bán điện (có cam kết thanh toán tiền điện của chủ nhà);

- Trường hợp thời hạn cho thuê nhà dưới 12 tháng và chủ nhà không thực hiện kê khai được đầy đủ số người sử dụng điện thì áp dụng giá bán lẻ điện sinh hoạt của bậc 2: Từ 101 - 200 kWh cho toàn bộ sản lượng điện đo đếm được tại công tơ;

- Trường hợp chủ nhà kê khai được đầy đủ số người sử dụng điện thì bên bán điện có trách nhiệm cấp định mức cho chủ nhà căn cứ vào thông tin về cư trú tại địa điểm sử dụng điện; cứ 04 (bốn) người được tính là một hộ sử dụng điện để tính số định mức áp dụng giá bán lẻ điện sinh hoạt, cụ thể: 01 (một) người được tính là 1/4 định mức, 02 (hai) người được tính là 1/2 định mức, 03 (ba) người được tính là 3/4 định mức, 04 (bốn) người được tính là 01 định mức. Khi có thay đổi về số người thuê nhà, chủ nhà cho thuê có trách nhiệm thông báo cho bên bán điện để điều chỉnh định mức tính toán tiền điện;

- Trường hợp người thuê nhà không giao kết hợp đồng trực tiếp với bên bán điện thì tổng tiền điện chủ nhà cho thuê thu của người thuê nhà không được vượt quá tiền điện trong hoá đơn tiền điện hằng tháng do đơn vị bán lẻ điện phát hành;

ười thuê nhà không giao kết hợp đồng trực tiếp với bên bán điện thì tổng tiền điện chủ nhà cho thuê thu của người thuê nhà không được vượt quá tiền điện trong hoá đơn tiền điện hằng tháng do đơn vị bán lẻ điện phát hành;

- Bên bán điện được phép yêu cầu bên mua điện cung cấp thông tin về cư trú tại địa điểm sử dụng điện để làm căn cứ xác định số người tính số định mức khi tính toán hóa đơn tiền điện.” [1].

- Thông-tư-60-2025-TT-BCT — Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp: “Điều 21. Hiệu lực thi hành
Điều 21. Hiệu lực thi hành

Điều 21. Hiệu lực thi hành | Khoản 1
1. Thông tư này có hiệu lực thi hành từ ngày 02 tháng 12 năm 2025, trừ quy định tại khoản 3 Điều 4, khoản 1 và khoản 2 Điều 5, Điều 9, Điều 10, khoản 10 Điều 11, khoản 3 Điều 12, khoản 4 Điều 12, điểm c khoản 5 Điều 12, khoản 6 Điều 14, khoản 6 Điều 15 Thông tư này và Phụ lục ban hành kèm theo Thông tư này có hiệu lực thi hành kể từ ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành.

Điều 20. Điều khoản chuyển tiếp
Điều 20. Điều khoản chuyển tiếp

Điều 20. Điều khoản chuyển tiếp | Khoản 1
1. Các quy định tại Thông tư số 16/2014/TT-BCT ngày 29 tháng 5 năm 2014 của Bộ trưởng Bộ Công Thương quy định về giá bán điện được tiếp tục áp dụng từ ngày Thông tư này có hiệu lực đến ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành, bao gồm:

Điều 20. Điều khoản chuyển tiếp | Khoản 1 | Điểm a
1. Các quy định tại Thông tư số 16/2014/TT-BCT ngày 29 tháng 5 năm 2014 của Bộ trưởng Bộ Công Thương quy định về giá bán điện được tiếp tục áp dụng từ ngày Thông tư này có hiệu lực đến ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành, bao gồm: a) Khoản 1 Điều 5;

Điều 20. Điều khoản chuyển tiếp | Khoản 1 | Điểm b
1. Các quy định tại Thông tư số 16/2014/TT-BCT ngày 29 tháng 5 năm 2014 của Bộ trưởng Bộ Công Thương quy định về giá bán điện được tiếp tục áp dụng từ ngày Thông tư này có hiệu lực đến ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành, bao gồm: b) Khoản 10 Điều 8;

Điều 20. Điều khoản chuyển tiếp | Khoản 1 | Điểm c
1. Các quy định tại Thông tư số 16/2014/TT-BCT ngày 29 tháng 5 năm 2014 của Bộ trưởng Bộ Công Thương quy định về giá bán điện được tiếp tục áp dụng từ ngày Thông tư này có hiệu lực đến ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành, bao gồm: c) Khoản 3 Điều 10 (đã được sửa đổi theo quy định tại khoản 3 Điều 1 của Thông tư số 09/2023/TT-BCT sửa đổi, bổ sung một số điều của Thông tư số 16/2014/TT-BCT và Thông tư số 25/2018/TT-BCT ngày 12 tháng 9 năm 2018 của Bộ trưởng Bộ Công Thương sửa đổi, bổ sung một số điều của Thông tư số 16/2014/TT-BCT);

Điều 20. Điều khoản chuyển tiếp | Khoản 1 | Điểm d
1. Các quy định tại Thông tư số 16/2014/TT-BCT ngày 29 tháng 5 năm 2014 của Bộ trưởng Bộ Công Thương quy định về giá bán điện được tiếp tục áp dụng từ ngày Thông tư này có hiệu lực đến ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành, bao gồm: d) Điểm c khoản 4 Điều 10 (đã được sửa đổi theo quy định tại khoản 5 Điều 1 của Thông tư số 25/2018/TT-BCT và khoản 2 Điều 2 của Thông tư số 09/2023/TT-BCT);

Điều 20. Điều khoản chuyển tiếp | Khoản 1 | Điểm đ
1. Các quy định tại Thông tư số 16/2014/TT-BCT ngày 29 tháng 5 năm 2014 của Bộ trưởng Bộ Công Thương quy định về giá bán điện được tiếp tục áp dụng từ ngày Thông tư này có hiệu lực đến ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành, bao gồm: đ) Khoản 6 Điều 12 (đã được sửa đổi theo quy định tại khoản 7 Điều 1 của Thông tư số 09/2023/TT-BCT);

Điều 20. Điều khoản chuyển tiếp | Khoản 1 | Điểm e
1. Các quy định tại Thông tư số 16/2014/TT-BCT ngày 29 tháng 5 năm 2014 của Bộ trưởng Bộ Công Thương quy định về giá bán điện được tiếp tục áp dụng từ ngày Thông tư này có hiệu lực đến ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành, bao gồm: e) Khoản 6 Điều 13 (đã được sửa đổi theo quy định tại khoản 9 Điều 1 của Thông tư số 09/2023/TT-BCT).” [3].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng; cần đối chiếu phần còn thiếu.

Nguồn có hiệu lực có điều kiện; chưa xác nhận văn bản/sự kiện kích hoạt.

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng, hiệu lực và bản gốc.

#### C — Đáp án bạn gửi

Theo Thông tư 25/2018/TT-BCT và Thông tư 09/2023/TT-BCT của Bộ Công Thương:
- **Trường hợp người thuê có hợp đồng từ 12 tháng trở lên và có đăng ký tạm trú:** Được cấp định mức điện riêng. Cứ **4 người** được tính là **1 hộ dùng điện** để áp biểu giá bán lẻ điện sinh hoạt bậc thang (từ Bậc 1 đến Bậc 6).
- **Trường hợp thời hạn thuê dưới 12 tháng hoặc chủ trọ không kê khai định mức:** Chủ trọ được lựa chọn:
  1. Tính theo biểu giá bán lẻ bậc thang của công tơ tổng; hoặc
  2. **Áp dụng giá bán lẻ điện bậc 3** (mức 101 - 200 kWh) cộng thêm thuế GTGT (hiện nay khoảng 2.167 VNĐ/kWh chưa VAT, sau VAT khoảng 2.300 - 2.400 VNĐ/kWh) cho toàn bộ sản lượng đo được tại công tơ của phòng trọ.
- **Nghiêm cấm:** Chủ trọ tự ý đặt ra mức giá cao vô lý (như 3.500 – 4.500 VNĐ/kWh) để trục lợi.

#### D — Chatbot dạng agent

Trường hợp người thuê không trực tiếp ký hợp đồng mua bán điện thì tổng tiền điện chủ trọ thu không được vượt quá số tiền trên hoá đơn hằng tháng do đơn vị bán lẻ điện phát hành [1].

- Hợp đồng thuê từ 12 tháng trở lên kèm đăng ký cư trú cho phép chủ nhà hoặc đại diện bên thuê ký hợp đồng mua bán điện [1].
- Nếu thời hạn thuê dưới 12 tháng và chủ nhà không kê khai đủ số người thì áp dụng giá bán lẻ điện sinh hoạt bậc 2 cho toàn bộ sản lượng đo tại công tơ [1].
- Nếu chủ nhà kê khai đầy đủ thông tin cư trú thì bên bán điện cấp định mức với tỷ lệ 04 người tính là một hộ sử dụng điện [1].
- Khuyến nghị người thuê trọ đối chiếu hoá đơn tiền điện thực tế của bên bán điện để kiểm tra số tiền chủ nhà thu [1].

Quy định tính giá điện cho sinh viên và người lao động có hiệu lực riêng từ ngày điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau khi Quyết định 14/2025/QĐ-TTg có hiệu lực [3].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng.
Nguồn có hiệu lực có điều kiện; chưa xác nhận văn bản/sự kiện kích hoạt.

Để áp dụng vào trường hợp của bạn:
- Thời hạn hợp đồng thuê phòng trọ của bạn là bao nhiêu tháng?
- Bạn đã đăng ký tạm trú và được chủ trọ kê khai số người sử dụng điện chưa?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

Nguồn truy xuất của D (rank dùng trong trích dẫn):

- [1] Thông-tư-60-2025-TT-BCT — Điều 12. Giá bán lẻ điện sinh hoạt | Khoản 5
- [2] Thông-tư-60-2025-TT-BCT
- [3] Thông-tư-60-2025-TT-BCT — Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp

Lý do giới hạn/fallback của D:

- Phản hồi chưa đáp ứng đầy đủ yêu cầu chính; đánh dấu theo nội dung thay vì provider.

### Câu 6: Ba sinh viên ở chung một phòng được tính tiền điện ra sao?

#### A — Gemini chatbot

Định mức theo số người thuê:

- Điều 12. Giá bán lẻ điện sinh hoạt | Khoản 5: “Trường hợp chủ nhà kê khai được đầy đủ số người sử dụng điện thì bên bán điện có trách nhiệm cấp định mức cho chủ nhà căn cứ vào thông tin về cư trú tại địa điểm sử dụng điện; cứ 04 (bốn) người được tính là một hộ sử dụng điện để tính số định mức áp dụng giá bán lẻ điện sinh hoạt, cụ thể: 01 (một) người được tính là 1/4 định mức, 02 (hai) người được tính là 1/2 định mức, 03 (ba) người được tính là 3/4 định mức, 04 (bốn) người được tính là 01 định mức. Khi có thay đổi về số người thuê nhà, chủ nhà cho thuê có trách nhiệm thông báo cho bên bán điện để điều chỉnh định mức tính toán tiền điện;” [1]

Điều kiện hiệu lực trong nguồn: “có hiệu lực thi hành kể từ ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành” [3].

Thông tin tham khảo từ văn bản đã trích xuất; cần đối chiếu điều kiện áp dụng và bản gốc.

#### B — Gemini phân tích + Qwen trích nguồn

Các đoạn trả lời trực tiếp trong nguồn:

- Thông-tư-60-2025-TT-BCT — Điều 12. Giá bán lẻ điện sinh hoạt | Khoản 5: “5. Bên mua điện sử dụng vào mục đích sinh hoạt của người thuê nhà để ở áp dụng như sau:

5. Bên mua điện sử dụng vào mục đích sinh hoạt của người thuê nhà để ở áp dụng như sau: a) Tại mỗi địa chỉ nhà cho thuê, bên bán điện chỉ giao kết một hợp đồng mua bán điện duy nhất. Chủ nhà cho thuê có trách nhiệm cung cấp thông tin về cư trú tại địa điểm sử dụng điện của người thuê nhà;

5. Bên mua điện sử dụng vào mục đích sinh hoạt của người thuê nhà để ở áp dụng như sau: b) Đối với trường hợp cho hộ gia đình thuê: Chủ nhà trực tiếp giao kết hợp đồng mua bán điện hoặc ủy quyền cho hộ gia đình thuê nhà giao kết hợp đồng mua bán điện (có cam kết thanh toán tiền điện), mỗi hộ gia đình thuê nhà được tính một định mức;

Ghi chú tuyển chọn: Điểm c khoản 5 về sinh viên/người lao động thuê nhà có mốc hiệu lực riêng tại khoản 1 Điều 21; không mặc nhiên áp dụng từ 02/12/2025.

5. Bên mua điện sử dụng vào mục đích sinh hoạt của người thuê nhà để ở áp dụng như sau: c) Trường hợp cho sinh viên và người lao động thuê nhà (bên thuê nhà không phải là một hộ gia đình):

- Đối với trường hợp bên thuê nhà có hợp đồng thuê nhà từ 12 tháng trở lên và có đăng ký tạm trú, thường trú (xác định theo thông tin về cư trú tại địa điểm sử dụng điện) thì chủ nhà trực tiếp giao kết hợp đồng mua bán điện hoặc đại diện bên thuê nhà giao kết hợp đồng mua bán điện (có cam kết thanh toán tiền điện của chủ nhà);

- Trường hợp thời hạn cho thuê nhà dưới 12 tháng và chủ nhà không thực hiện kê khai được đầy đủ số người sử dụng điện thì áp dụng giá bán lẻ điện sinh hoạt của bậc 2: Từ 101 - 200 kWh cho toàn bộ sản lượng điện đo đếm được tại công tơ;

- Trường hợp chủ nhà kê khai được đầy đủ số người sử dụng điện thì bên bán điện có trách nhiệm cấp định mức cho chủ nhà căn cứ vào thông tin về cư trú tại địa điểm sử dụng điện; cứ 04 (bốn) người được tính là một hộ sử dụng điện để tính số định mức áp dụng giá bán lẻ điện sinh hoạt, cụ thể: 01 (một) người được tính là 1/4 định mức, 02 (hai) người được tính là 1/2 định mức, 03 (ba) người được tính là 3/4 định mức, 04 (bốn) người được tính là 01 định mức. Khi có thay đổi về số người thuê nhà, chủ nhà cho thuê có trách nhiệm thông báo cho bên bán điện để điều chỉnh định mức tính toán tiền điện;

- Trường hợp người thuê nhà không giao kết hợp đồng trực tiếp với bên bán điện thì tổng tiền điện chủ nhà cho thuê thu của người thuê nhà không được vượt quá tiền điện trong hoá đơn tiền điện hằng tháng do đơn vị bán lẻ điện phát hành;

ười thuê nhà không giao kết hợp đồng trực tiếp với bên bán điện thì tổng tiền điện chủ nhà cho thuê thu của người thuê nhà không được vượt quá tiền điện trong hoá đơn tiền điện hằng tháng do đơn vị bán lẻ điện phát hành;

- Bên bán điện được phép yêu cầu bên mua điện cung cấp thông tin về cư trú tại địa điểm sử dụng điện để làm căn cứ xác định số người tính số định mức khi tính toán hóa đơn tiền điện.” [1].

- Thông-tư-60-2025-TT-BCT — Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp: “Điều 21. Hiệu lực thi hành
Điều 21. Hiệu lực thi hành

Điều 21. Hiệu lực thi hành | Khoản 1
1. Thông tư này có hiệu lực thi hành từ ngày 02 tháng 12 năm 2025, trừ quy định tại khoản 3 Điều 4, khoản 1 và khoản 2 Điều 5, Điều 9, Điều 10, khoản 10 Điều 11, khoản 3 Điều 12, khoản 4 Điều 12, điểm c khoản 5 Điều 12, khoản 6 Điều 14, khoản 6 Điều 15 Thông tư này và Phụ lục ban hành kèm theo Thông tư này có hiệu lực thi hành kể từ ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành.

Điều 20. Điều khoản chuyển tiếp
Điều 20. Điều khoản chuyển tiếp

Điều 20. Điều khoản chuyển tiếp | Khoản 1
1. Các quy định tại Thông tư số 16/2014/TT-BCT ngày 29 tháng 5 năm 2014 của Bộ trưởng Bộ Công Thương quy định về giá bán điện được tiếp tục áp dụng từ ngày Thông tư này có hiệu lực đến ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành, bao gồm:

Điều 20. Điều khoản chuyển tiếp | Khoản 1 | Điểm a
1. Các quy định tại Thông tư số 16/2014/TT-BCT ngày 29 tháng 5 năm 2014 của Bộ trưởng Bộ Công Thương quy định về giá bán điện được tiếp tục áp dụng từ ngày Thông tư này có hiệu lực đến ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành, bao gồm: a) Khoản 1 Điều 5;

Điều 20. Điều khoản chuyển tiếp | Khoản 1 | Điểm b
1. Các quy định tại Thông tư số 16/2014/TT-BCT ngày 29 tháng 5 năm 2014 của Bộ trưởng Bộ Công Thương quy định về giá bán điện được tiếp tục áp dụng từ ngày Thông tư này có hiệu lực đến ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành, bao gồm: b) Khoản 10 Điều 8;

Điều 20. Điều khoản chuyển tiếp | Khoản 1 | Điểm c
1. Các quy định tại Thông tư số 16/2014/TT-BCT ngày 29 tháng 5 năm 2014 của Bộ trưởng Bộ Công Thương quy định về giá bán điện được tiếp tục áp dụng từ ngày Thông tư này có hiệu lực đến ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành, bao gồm: c) Khoản 3 Điều 10 (đã được sửa đổi theo quy định tại khoản 3 Điều 1 của Thông tư số 09/2023/TT-BCT sửa đổi, bổ sung một số điều của Thông tư số 16/2014/TT-BCT và Thông tư số 25/2018/TT-BCT ngày 12 tháng 9 năm 2018 của Bộ trưởng Bộ Công Thương sửa đổi, bổ sung một số điều của Thông tư số 16/2014/TT-BCT);

Điều 20. Điều khoản chuyển tiếp | Khoản 1 | Điểm d
1. Các quy định tại Thông tư số 16/2014/TT-BCT ngày 29 tháng 5 năm 2014 của Bộ trưởng Bộ Công Thương quy định về giá bán điện được tiếp tục áp dụng từ ngày Thông tư này có hiệu lực đến ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành, bao gồm: d) Điểm c khoản 4 Điều 10 (đã được sửa đổi theo quy định tại khoản 5 Điều 1 của Thông tư số 25/2018/TT-BCT và khoản 2 Điều 2 của Thông tư số 09/2023/TT-BCT);

Điều 20. Điều khoản chuyển tiếp | Khoản 1 | Điểm đ
1. Các quy định tại Thông tư số 16/2014/TT-BCT ngày 29 tháng 5 năm 2014 của Bộ trưởng Bộ Công Thương quy định về giá bán điện được tiếp tục áp dụng từ ngày Thông tư này có hiệu lực đến ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành, bao gồm: đ) Khoản 6 Điều 12 (đã được sửa đổi theo quy định tại khoản 7 Điều 1 của Thông tư số 09/2023/TT-BCT);

Điều 20. Điều khoản chuyển tiếp | Khoản 1 | Điểm e
1. Các quy định tại Thông tư số 16/2014/TT-BCT ngày 29 tháng 5 năm 2014 của Bộ trưởng Bộ Công Thương quy định về giá bán điện được tiếp tục áp dụng từ ngày Thông tư này có hiệu lực đến ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành, bao gồm: e) Khoản 6 Điều 13 (đã được sửa đổi theo quy định tại khoản 9 Điều 1 của Thông tư số 09/2023/TT-BCT).” [3].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng; cần đối chiếu phần còn thiếu.

Nguồn có hiệu lực có điều kiện; chưa xác nhận văn bản/sự kiện kích hoạt.

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng, hiệu lực và bản gốc.

#### C — Đáp án bạn gửi

Theo quy định tại Điều 10 Thông tư 16/2014/TT-BCT (được sửa đổi bởi Thông tư 25/2018/TT-BCT):
- Quy chuẩn định mức: **1 người được tính là 1/4 định mức, 2 người là 2/4 định mức, 3 người được tính là 3/4 định mức hộ gia đình**.
- Cụ thể với **3 sinh viên** có đăng ký tạm trú: Sẽ được hưởng **75% định mức của từng bậc thang điện** sinh hoạt:
  - Bậc 1 (0 - 50 kWh): Định mức được tính là $50 \times 3/4 = 37,5\text{ kWh}$.
  - Bậc 2 (51 - 100 kWh): Định mức là $37,5\text{ kWh}$.
  - Các bậc tiếp theo tính tương tự theo tỷ lệ 3/4.
- Nếu chủ trọ không làm thủ tục kê khai định mức với bên Điện lực thì phải áp dụng **giá điện Bậc 3** cho toàn bộ số điện phòng tiêu thụ.

#### D — Chatbot dạng agent

Các đoạn trả lời trực tiếp trong nguồn:

- Thông-tư-60-2025-TT-BCT — Điều 12. Giá bán lẻ điện sinh hoạt | Khoản 5: “5. Bên mua điện sử dụng vào mục đích sinh hoạt của người thuê nhà để ở áp dụng như sau:

5. Bên mua điện sử dụng vào mục đích sinh hoạt của người thuê nhà để ở áp dụng như sau: a) Tại mỗi địa chỉ nhà cho thuê, bên bán điện chỉ giao kết một hợp đồng mua bán điện duy nhất. Chủ nhà cho thuê có trách nhiệm cung cấp thông tin về cư trú tại địa điểm sử dụng điện của người thuê nhà;

5. Bên mua điện sử dụng vào mục đích sinh hoạt của người thuê nhà để ở áp dụng như sau: b) Đối với trường hợp cho hộ gia đình thuê: Chủ nhà trực tiếp giao kết hợp đồng mua bán điện hoặc ủy quyền cho hộ gia đình thuê nhà giao kết hợp đồng mua bán điện (có cam kết thanh toán tiền điện), mỗi hộ gia đình thuê nhà được tính một định mức;

Ghi chú tuyển chọn: Điểm c khoản 5 về sinh viên/người lao động thuê nhà có mốc hiệu lực riêng tại khoản 1 Điều 21; không mặc nhiên áp dụng từ 02/12/2025.

5. Bên mua điện sử dụng vào mục đích sinh hoạt của người thuê nhà để ở áp dụng như sau: c) Trường hợp cho sinh viên và người lao động thuê nhà (bên thuê nhà không phải là một hộ gia đình):

- Đối với trường hợp bên thuê nhà có hợp đồng thuê nhà từ 12 tháng trở lên và có đăng ký tạm trú, thường trú (xác định theo thông tin về cư trú tại địa điểm sử dụng điện) thì chủ nhà trực tiếp giao kết hợp đồng mua bán điện hoặc đại diện bên thuê nhà giao kết hợp đồng mua bán điện (có cam kết thanh toán tiền điện của chủ nhà);

- Trường hợp thời hạn cho thuê nhà dưới 12 tháng và chủ nhà không thực hiện kê khai được đầy đủ số người sử dụng điện thì áp dụng giá bán lẻ điện sinh hoạt của bậc 2: Từ 101 - 200 kWh cho toàn bộ sản lượng điện đo đếm được tại công tơ;

- Trường hợp chủ nhà kê khai được đầy đủ số người sử dụng điện thì bên bán điện có trách nhiệm cấp định mức cho chủ nhà căn cứ vào thông tin về cư trú tại địa điểm sử dụng điện; cứ 04 (bốn) người được tính là một hộ sử dụng điện để tính số định mức áp dụng giá bán lẻ điện sinh hoạt, cụ thể: 01 (một) người được tính là 1/4 định mức, 02 (hai) người được tính là 1/2 định mức, 03 (ba) người được tính là 3/4 định mức, 04 (bốn) người được tính là 01 định mức. Khi có thay đổi về số người thuê nhà, chủ nhà cho thuê có trách nhiệm thông báo cho bên bán điện để điều chỉnh định mức tính toán tiền điện;

- Trường hợp người thuê nhà không giao kết hợp đồng trực tiếp với bên bán điện thì tổng tiền điện chủ nhà cho thuê thu của người thuê nhà không được vượt quá tiền điện trong hoá đơn tiền điện hằng tháng do đơn vị bán lẻ điện phát hành;

ười thuê nhà không giao kết hợp đồng trực tiếp với bên bán điện thì tổng tiền điện chủ nhà cho thuê thu của người thuê nhà không được vượt quá tiền điện trong hoá đơn tiền điện hằng tháng do đơn vị bán lẻ điện phát hành;

- Bên bán điện được phép yêu cầu bên mua điện cung cấp thông tin về cư trú tại địa điểm sử dụng điện để làm căn cứ xác định số người tính số định mức khi tính toán hóa đơn tiền điện.” [1].

- Thông-tư-60-2025-TT-BCT — Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp: “Điều 21. Hiệu lực thi hành
Điều 21. Hiệu lực thi hành

Điều 21. Hiệu lực thi hành | Khoản 1
1. Thông tư này có hiệu lực thi hành từ ngày 02 tháng 12 năm 2025, trừ quy định tại khoản 3 Điều 4, khoản 1 và khoản 2 Điều 5, Điều 9, Điều 10, khoản 10 Điều 11, khoản 3 Điều 12, khoản 4 Điều 12, điểm c khoản 5 Điều 12, khoản 6 Điều 14, khoản 6 Điều 15 Thông tư này và Phụ lục ban hành kèm theo Thông tư này có hiệu lực thi hành kể từ ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành.

Điều 20. Điều khoản chuyển tiếp
Điều 20. Điều khoản chuyển tiếp

Điều 20. Điều khoản chuyển tiếp | Khoản 1
1. Các quy định tại Thông tư số 16/2014/TT-BCT ngày 29 tháng 5 năm 2014 của Bộ trưởng Bộ Công Thương quy định về giá bán điện được tiếp tục áp dụng từ ngày Thông tư này có hiệu lực đến ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành, bao gồm:

Điều 20. Điều khoản chuyển tiếp | Khoản 1 | Điểm a
1. Các quy định tại Thông tư số 16/2014/TT-BCT ngày 29 tháng 5 năm 2014 của Bộ trưởng Bộ Công Thương quy định về giá bán điện được tiếp tục áp dụng từ ngày Thông tư này có hiệu lực đến ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành, bao gồm: a) Khoản 1 Điều 5;

Điều 20. Điều khoản chuyển tiếp | Khoản 1 | Điểm b
1. Các quy định tại Thông tư số 16/2014/TT-BCT ngày 29 tháng 5 năm 2014 của Bộ trưởng Bộ Công Thương quy định về giá bán điện được tiếp tục áp dụng từ ngày Thông tư này có hiệu lực đến ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành, bao gồm: b) Khoản 10 Điều 8;

Điều 20. Điều khoản chuyển tiếp | Khoản 1 | Điểm c
1. Các quy định tại Thông tư số 16/2014/TT-BCT ngày 29 tháng 5 năm 2014 của Bộ trưởng Bộ Công Thương quy định về giá bán điện được tiếp tục áp dụng từ ngày Thông tư này có hiệu lực đến ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành, bao gồm: c) Khoản 3 Điều 10 (đã được sửa đổi theo quy định tại khoản 3 Điều 1 của Thông tư số 09/2023/TT-BCT sửa đổi, bổ sung một số điều của Thông tư số 16/2014/TT-BCT và Thông tư số 25/2018/TT-BCT ngày 12 tháng 9 năm 2018 của Bộ trưởng Bộ Công Thương sửa đổi, bổ sung một số điều của Thông tư số 16/2014/TT-BCT);

Điều 20. Điều khoản chuyển tiếp | Khoản 1 | Điểm d
1. Các quy định tại Thông tư số 16/2014/TT-BCT ngày 29 tháng 5 năm 2014 của Bộ trưởng Bộ Công Thương quy định về giá bán điện được tiếp tục áp dụng từ ngày Thông tư này có hiệu lực đến ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành, bao gồm: d) Điểm c khoản 4 Điều 10 (đã được sửa đổi theo quy định tại khoản 5 Điều 1 của Thông tư số 25/2018/TT-BCT và khoản 2 Điều 2 của Thông tư số 09/2023/TT-BCT);

Điều 20. Điều khoản chuyển tiếp | Khoản 1 | Điểm đ
1. Các quy định tại Thông tư số 16/2014/TT-BCT ngày 29 tháng 5 năm 2014 của Bộ trưởng Bộ Công Thương quy định về giá bán điện được tiếp tục áp dụng từ ngày Thông tư này có hiệu lực đến ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành, bao gồm: đ) Khoản 6 Điều 12 (đã được sửa đổi theo quy định tại khoản 7 Điều 1 của Thông tư số 09/2023/TT-BCT);

Điều 20. Điều khoản chuyển tiếp | Khoản 1 | Điểm e
1. Các quy định tại Thông tư số 16/2014/TT-BCT ngày 29 tháng 5 năm 2014 của Bộ trưởng Bộ Công Thương quy định về giá bán điện được tiếp tục áp dụng từ ngày Thông tư này có hiệu lực đến ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành, bao gồm: e) Khoản 6 Điều 13 (đã được sửa đổi theo quy định tại khoản 9 Điều 1 của Thông tư số 09/2023/TT-BCT).” [3].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng; cần đối chiếu phần còn thiếu.

Nguồn có hiệu lực có điều kiện; chưa xác nhận văn bản/sự kiện kích hoạt.

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng, hiệu lực và bản gốc.

Nguồn truy xuất của D (rank dùng trong trích dẫn):

- [1] Thông-tư-60-2025-TT-BCT — Điều 12. Giá bán lẻ điện sinh hoạt | Khoản 5
- [2] Thông-tư-60-2025-TT-BCT
- [3] Thông-tư-60-2025-TT-BCT — Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp

Lý do giới hạn/fallback của D:

- Kết luận hoặc số liệu chưa gắn trích dẫn trực tiếp.
- Bản tổng hợp chưa được nguồn xác nhận sau lần sửa; dùng trích đoạn Qwen đã chọn.
- Phản hồi chưa đáp ứng đầy đủ yêu cầu chính; đánh dấu theo nội dung thay vì provider.

### Câu 7: Nếu tôi nghi tiền điện bị thu cao hơn quy định, nên kiểm tra hóa đơn và căn cứ nào?

#### A — Gemini chatbot

Dưới đây là các căn cứ và nội dung bạn cần lưu ý:

* **Căn cứ hóa đơn tiền điện:** Khi người thuê nhà không ký hợp đồng trực tiếp với bên bán điện, tổng tiền điện chủ nhà thu không được vượt quá số tiền trên hoá đơn tiền điện hằng tháng do đơn vị bán lẻ điện phát hành [1], Thông-tư-60-2025-TT-BCT, Điều 12, trang 1.
* **Căn cứ tính giá và định mức:** Tùy trường hợp kê khai, tiền điện áp dụng theo giá bán lẻ bậc 2 (nếu thuê dưới 12 tháng và không kê khai đủ số người) hoặc cấp định mức sinh hoạt dựa trên thông tin cư trú (cứ 4 người tính là một hộ định mức: 1 người là 1/4, 2 người là 1/2 định mức...) [1], Thông-tư-60-2025-TT-BCT, Điều 12, trang 1.
* **Khuyến nghị:** Nên kiểm tra và đối chiếu hóa đơn tiền điện thực tế của bên bán lẻ điện với số tiền chủ nhà thông báo thu; đồng thời lưu ý quy định tại điểm c khoản 5 Điều 12 nêu trên chỉ có hiệu lực kể từ ngày điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định 14/2025/QĐ-TTg có hiệu lực [3], Thông-tư-60-2025-TT-BCT, Điều 21, trang 1.

*Lưu ý: Đây là thông tin tham khảo, không thay thế tư vấn pháp lý chuyên nghiệp.*

#### B — Gemini phân tích + Qwen trích nguồn

Các đoạn trả lời trực tiếp trong nguồn:

- Thông-tư-60-2025-TT-BCT — Điều 12. Giá bán lẻ điện sinh hoạt | Khoản 5: “5. Bên mua điện sử dụng vào mục đích sinh hoạt của người thuê nhà để ở áp dụng như sau:

5. Bên mua điện sử dụng vào mục đích sinh hoạt của người thuê nhà để ở áp dụng như sau: a) Tại mỗi địa chỉ nhà cho thuê, bên bán điện chỉ giao kết một hợp đồng mua bán điện duy nhất. Chủ nhà cho thuê có trách nhiệm cung cấp thông tin về cư trú tại địa điểm sử dụng điện của người thuê nhà;

5. Bên mua điện sử dụng vào mục đích sinh hoạt của người thuê nhà để ở áp dụng như sau: b) Đối với trường hợp cho hộ gia đình thuê: Chủ nhà trực tiếp giao kết hợp đồng mua bán điện hoặc ủy quyền cho hộ gia đình thuê nhà giao kết hợp đồng mua bán điện (có cam kết thanh toán tiền điện), mỗi hộ gia đình thuê nhà được tính một định mức;

Ghi chú tuyển chọn: Điểm c khoản 5 về sinh viên/người lao động thuê nhà có mốc hiệu lực riêng tại khoản 1 Điều 21; không mặc nhiên áp dụng từ 02/12/2025.

5. Bên mua điện sử dụng vào mục đích sinh hoạt của người thuê nhà để ở áp dụng như sau: c) Trường hợp cho sinh viên và người lao động thuê nhà (bên thuê nhà không phải là một hộ gia đình):

- Đối với trường hợp bên thuê nhà có hợp đồng thuê nhà từ 12 tháng trở lên và có đăng ký tạm trú, thường trú (xác định theo thông tin về cư trú tại địa điểm sử dụng điện) thì chủ nhà trực tiếp giao kết hợp đồng mua bán điện hoặc đại diện bên thuê nhà giao kết hợp đồng mua bán điện (có cam kết thanh toán tiền điện của chủ nhà);

- Trường hợp thời hạn cho thuê nhà dưới 12 tháng và chủ nhà không thực hiện kê khai được đầy đủ số người sử dụng điện thì áp dụng giá bán lẻ điện sinh hoạt của bậc 2: Từ 101 - 200 kWh cho toàn bộ sản lượng điện đo đếm được tại công tơ;

- Trường hợp chủ nhà kê khai được đầy đủ số người sử dụng điện thì bên bán điện có trách nhiệm cấp định mức cho chủ nhà căn cứ vào thông tin về cư trú tại địa điểm sử dụng điện; cứ 04 (bốn) người được tính là một hộ sử dụng điện để tính số định mức áp dụng giá bán lẻ điện sinh hoạt, cụ thể: 01 (một) người được tính là 1/4 định mức, 02 (hai) người được tính là 1/2 định mức, 03 (ba) người được tính là 3/4 định mức, 04 (bốn) người được tính là 01 định mức. Khi có thay đổi về số người thuê nhà, chủ nhà cho thuê có trách nhiệm thông báo cho bên bán điện để điều chỉnh định mức tính toán tiền điện;

- Trường hợp người thuê nhà không giao kết hợp đồng trực tiếp với bên bán điện thì tổng tiền điện chủ nhà cho thuê thu của người thuê nhà không được vượt quá tiền điện trong hoá đơn tiền điện hằng tháng do đơn vị bán lẻ điện phát hành;

ười thuê nhà không giao kết hợp đồng trực tiếp với bên bán điện thì tổng tiền điện chủ nhà cho thuê thu của người thuê nhà không được vượt quá tiền điện trong hoá đơn tiền điện hằng tháng do đơn vị bán lẻ điện phát hành;

- Bên bán điện được phép yêu cầu bên mua điện cung cấp thông tin về cư trú tại địa điểm sử dụng điện để làm căn cứ xác định số người tính số định mức khi tính toán hóa đơn tiền điện.” [1].

- Thông-tư-60-2025-TT-BCT — trích đoạn: “THÔNG TƯ 60 2025 TT BCT TRÍCH TUYỂN

Văn bản gốc: Thông tư số 60/2025/TT-BCT ngày 02/12/2025, quy định về thực hiện giá bán điện.

Phạm vi bản trích: giá điện sinh hoạt cho người thuê nhà, định mức, hóa đơn, điều khoản chuyển tiếp và hiệu lực.

Nguồn chính thức: https://vanban.chinhphu.vn/?docid=216125&orggroupid=4&pageid=27160

Lưu ý hiệu lực: khoản 3, khoản 4 và điểm c khoản 5 Điều 12 có mốc áp dụng riêng theo khoản 1 Điều 21. Trước khi dùng các khoản này để trả lời hiện tại, phải xác minh đã có lần điều chỉnh mức giá bán lẻ điện bình quân sau Quyết định 14/2025/QĐ-TTg hay chưa; xem thêm khoản 1 Điều 20.

Nguồn sửa đổi: tại ngày 01/10/2026 chưa gắn một văn bản sửa đổi ban hành trong bản trích này; cần kiểm tra lại khi cập nhật giá điện.

NỘI DUNG TRÍCH TUYỂN” [2].

- Thông-tư-60-2025-TT-BCT — Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp: “Điều 21. Hiệu lực thi hành
Điều 21. Hiệu lực thi hành

Điều 21. Hiệu lực thi hành | Khoản 1
1. Thông tư này có hiệu lực thi hành từ ngày 02 tháng 12 năm 2025, trừ quy định tại khoản 3 Điều 4, khoản 1 và khoản 2 Điều 5, Điều 9, Điều 10, khoản 10 Điều 11, khoản 3 Điều 12, khoản 4 Điều 12, điểm c khoản 5 Điều 12, khoản 6 Điều 14, khoản 6 Điều 15 Thông tư này và Phụ lục ban hành kèm theo Thông tư này có hiệu lực thi hành kể từ ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành.

Điều 20. Điều khoản chuyển tiếp
Điều 20. Điều khoản chuyển tiếp

Điều 20. Điều khoản chuyển tiếp | Khoản 1
1. Các quy định tại Thông tư số 16/2014/TT-BCT ngày 29 tháng 5 năm 2014 của Bộ trưởng Bộ Công Thương quy định về giá bán điện được tiếp tục áp dụng từ ngày Thông tư này có hiệu lực đến ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành, bao gồm:

Điều 20. Điều khoản chuyển tiếp | Khoản 1 | Điểm a
1. Các quy định tại Thông tư số 16/2014/TT-BCT ngày 29 tháng 5 năm 2014 của Bộ trưởng Bộ Công Thương quy định về giá bán điện được tiếp tục áp dụng từ ngày Thông tư này có hiệu lực đến ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành, bao gồm: a) Khoản 1 Điều 5;

Điều 20. Điều khoản chuyển tiếp | Khoản 1 | Điểm b
1. Các quy định tại Thông tư số 16/2014/TT-BCT ngày 29 tháng 5 năm 2014 của Bộ trưởng Bộ Công Thương quy định về giá bán điện được tiếp tục áp dụng từ ngày Thông tư này có hiệu lực đến ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành, bao gồm: b) Khoản 10 Điều 8;

Điều 20. Điều khoản chuyển tiếp | Khoản 1 | Điểm c
1. Các quy định tại Thông tư số 16/2014/TT-BCT ngày 29 tháng 5 năm 2014 của Bộ trưởng Bộ Công Thương quy định về giá bán điện được tiếp tục áp dụng từ ngày Thông tư này có hiệu lực đến ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành, bao gồm: c) Khoản 3 Điều 10 (đã được sửa đổi theo quy định tại khoản 3 Điều 1 của Thông tư số 09/2023/TT-BCT sửa đổi, bổ sung một số điều của Thông tư số 16/2014/TT-BCT và Thông tư số 25/2018/TT-BCT ngày 12 tháng 9 năm 2018 của Bộ trưởng Bộ Công Thương sửa đổi, bổ sung một số điều của Thông tư số 16/2014/TT-BCT);

Điều 20. Điều khoản chuyển tiếp | Khoản 1 | Điểm d
1. Các quy định tại Thông tư số 16/2014/TT-BCT ngày 29 tháng 5 năm 2014 của Bộ trưởng Bộ Công Thương quy định về giá bán điện được tiếp tục áp dụng từ ngày Thông tư này có hiệu lực đến ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành, bao gồm: d) Điểm c khoản 4 Điều 10 (đã được sửa đổi theo quy định tại khoản 5 Điều 1 của Thông tư số 25/2018/TT-BCT và khoản 2 Điều 2 của Thông tư số 09/2023/TT-BCT);

Điều 20. Điều khoản chuyển tiếp | Khoản 1 | Điểm đ
1. Các quy định tại Thông tư số 16/2014/TT-BCT ngày 29 tháng 5 năm 2014 của Bộ trưởng Bộ Công Thương quy định về giá bán điện được tiếp tục áp dụng từ ngày Thông tư này có hiệu lực đến ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành, bao gồm: đ) Khoản 6 Điều 12 (đã được sửa đổi theo quy định tại khoản 7 Điều 1 của Thông tư số 09/2023/TT-BCT);

Điều 20. Điều khoản chuyển tiếp | Khoản 1 | Điểm e
1. Các quy định tại Thông tư số 16/2014/TT-BCT ngày 29 tháng 5 năm 2014 của Bộ trưởng Bộ Công Thương quy định về giá bán điện được tiếp tục áp dụng từ ngày Thông tư này có hiệu lực đến ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành, bao gồm: e) Khoản 6 Điều 13 (đã được sửa đổi theo quy định tại khoản 9 Điều 1 của Thông tư số 09/2023/TT-BCT).” [3].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng; cần đối chiếu phần còn thiếu.

Nguồn có hiệu lực có điều kiện; chưa xác nhận văn bản/sự kiện kích hoạt.

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng, hiệu lực và bản gốc.

#### C — Đáp án bạn gửi

Bạn cần thực hiện các bước kiểm tra sau:
1. **Kiểm tra công tơ điện:** Ghi lại chỉ số điện đầu tháng và cuối tháng của đồng hồ phòng mình, tính ra số kWh thực tế đã dùng.
2. **Yêu cầu đối chiếu hóa đơn tiền điện gốc:** Đề nghị chủ trọ cho xem hóa đơn tiền điện tháng đó của Điện lực cấp (hoặc mã khách hàng PE... trên ứng dụng EVNSPC CSKH).
3. **Căn cứ pháp lý xử phạt:** Căn cứ theo **Khoản 6 Điều 12 Nghị định 134/2013/NĐ-CP** (được sửa đổi bởi **Nghị định 17/2022/NĐ-CP**), hành vi thu tiền điện của người thuê nhà cao hơn giá quy định trong trường hợp mua điện theo giá bán lẻ điện sinh hoạt bị **phạt tiền từ 20.000.000 đồng đến 30.000.000 đồng**.
4. **Kênh phản ánh:** Nếu chủ trọ cố tình vi phạm, bạn có thể gọi hotline CSKH Tổng công ty Điện lực miền Nam (EVNSPC: **1900 1006** hoặc **1900 9000**) hoặc phản ánh qua UBND phường/xã nơi đặt phòng trọ.

#### D — Chatbot dạng agent

Trường hợp không ký hợp đồng mua bán điện trực tiếp, bạn căn cứ vào hóa đơn tiền điện hằng tháng do bên bán lẻ điện phát hành vì tổng tiền chủ nhà thu không được vượt quá số tiền trên hóa đơn này [1].

- Khuyến nghị kiểm tra thời hạn hợp đồng thuê nhà cùng thông tin đăng ký cư trú để xác định tư cách đứng tên ký hợp đồng trực tiếp với bên bán điện nếu hợp đồng từ 12 tháng trở lên [1].
- Khuyến nghị đối chiếu việc chủ nhà có kê khai đủ số người cư trú hay không, bởi nếu không kê khai được thì áp dụng giá bán lẻ điện sinh hoạt bậc 2 cho toàn bộ sản lượng đo đếm [1].
- Khuyến nghị kiểm tra số định mức được cấp theo thông tin cư trú với nguyên tắc cứ 04 người tính là một hộ sử dụng điện khi chủ nhà kê khai đầy đủ [1].
- Khuyến nghị yêu cầu chủ nhà đối chiếu hóa đơn tiền điện hằng tháng của đơn vị bán lẻ điện để bảo đảm tổng số tiền thu từ người thuê không vượt quá hóa đơn [1].

Quy định áp dụng giá điện sinh hoạt cho sinh viên và người lao động thuê nhà tại điểm c khoản 5 Điều 12 chỉ có hiệu lực kể từ ngày điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực [1] [3].
Chưa đủ căn cứ từ nguồn trích tuyển để hướng dẫn quy trình khiếu nại hay mức phạt cụ thể khi chủ nhà thu tiền điện cao hơn quy định [1] [2] [3].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng.
Nguồn có hiệu lực có điều kiện; chưa xác nhận văn bản/sự kiện kích hoạt.

Để áp dụng vào trường hợp của bạn:
- Hợp đồng thuê phòng của bạn có thời hạn bao nhiêu tháng và đã đăng ký tạm trú chưa?
- Chủ nhà trọ hiện đang tính tiền điện theo mức giá cố định bao nhiêu tiền một kWh?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

Nguồn truy xuất của D (rank dùng trong trích dẫn):

- [1] Thông-tư-60-2025-TT-BCT — Điều 12. Giá bán lẻ điện sinh hoạt | Khoản 5
- [2] Thông-tư-60-2025-TT-BCT
- [3] Thông-tư-60-2025-TT-BCT — Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp

Lý do giới hạn/fallback của D:

- Phản hồi chưa đáp ứng đầy đủ yêu cầu chính; đánh dấu theo nội dung thay vì provider.

### Câu 8: Chủ trọ có phải thông báo cách tính tiền điện và số điện đã sử dụng không?

#### A — Gemini chatbot

Các căn cứ liên quan tìm được trong kho (trích nguyên đoạn):

- Thông-tư-60-2025-TT-BCT — Điều 12. Giá bán lẻ điện sinh hoạt | Khoản 5: “- Trường hợp chủ nhà kê khai được đầy đủ số người sử dụng điện thì bên bán điện có trách nhiệm cấp định mức cho chủ nhà căn cứ vào thông tin về cư trú tại địa điểm sử dụng điện; cứ 04 (bốn) người được tính là một hộ sử dụng điện để tính số định mức áp dụng giá bán lẻ điện sinh hoạt, cụ thể: 01 (một) người được tính là 1/4 định mức, 02 (hai) người được tính là 1/2 định mức, 03 (ba) người được tính là 3/4 định mức, 04 (bốn) người được tính là 01 định mức. Khi có thay đổi về số người thuê nhà, chủ nhà cho thuê có trách nhiệm thông báo cho bên bán điện để điều chỉnh định mức tính toán tiền điện;” [1].

- Thông-tư-60-2025-TT-BCT — Điều 12. Giá bán lẻ điện sinh hoạt | Khoản 5: “- Bên bán điện được phép yêu cầu bên mua điện cung cấp thông tin về cư trú tại địa điểm sử dụng điện để làm căn cứ xác định số người tính số định mức khi tính toán hóa đơn tiền điện.” [1].

Đây là câu trả lời một phần từ nguồn; chưa kết luận cách áp dụng cho tình huống riêng của bạn. Cần đối chiếu điều kiện, hiệu lực và bản gốc.

#### B — Gemini phân tích + Qwen trích nguồn

Các đoạn trả lời trực tiếp trong nguồn:

- Thông-tư-60-2025-TT-BCT — Điều 12. Giá bán lẻ điện sinh hoạt | Khoản 5: “5. Bên mua điện sử dụng vào mục đích sinh hoạt của người thuê nhà để ở áp dụng như sau:

5. Bên mua điện sử dụng vào mục đích sinh hoạt của người thuê nhà để ở áp dụng như sau: a) Tại mỗi địa chỉ nhà cho thuê, bên bán điện chỉ giao kết một hợp đồng mua bán điện duy nhất. Chủ nhà cho thuê có trách nhiệm cung cấp thông tin về cư trú tại địa điểm sử dụng điện của người thuê nhà;

5. Bên mua điện sử dụng vào mục đích sinh hoạt của người thuê nhà để ở áp dụng như sau: b) Đối với trường hợp cho hộ gia đình thuê: Chủ nhà trực tiếp giao kết hợp đồng mua bán điện hoặc ủy quyền cho hộ gia đình thuê nhà giao kết hợp đồng mua bán điện (có cam kết thanh toán tiền điện), mỗi hộ gia đình thuê nhà được tính một định mức;

Ghi chú tuyển chọn: Điểm c khoản 5 về sinh viên/người lao động thuê nhà có mốc hiệu lực riêng tại khoản 1 Điều 21; không mặc nhiên áp dụng từ 02/12/2025.

5. Bên mua điện sử dụng vào mục đích sinh hoạt của người thuê nhà để ở áp dụng như sau: c) Trường hợp cho sinh viên và người lao động thuê nhà (bên thuê nhà không phải là một hộ gia đình):

- Đối với trường hợp bên thuê nhà có hợp đồng thuê nhà từ 12 tháng trở lên và có đăng ký tạm trú, thường trú (xác định theo thông tin về cư trú tại địa điểm sử dụng điện) thì chủ nhà trực tiếp giao kết hợp đồng mua bán điện hoặc đại diện bên thuê nhà giao kết hợp đồng mua bán điện (có cam kết thanh toán tiền điện của chủ nhà);

- Trường hợp thời hạn cho thuê nhà dưới 12 tháng và chủ nhà không thực hiện kê khai được đầy đủ số người sử dụng điện thì áp dụng giá bán lẻ điện sinh hoạt của bậc 2: Từ 101 - 200 kWh cho toàn bộ sản lượng điện đo đếm được tại công tơ;

- Trường hợp chủ nhà kê khai được đầy đủ số người sử dụng điện thì bên bán điện có trách nhiệm cấp định mức cho chủ nhà căn cứ vào thông tin về cư trú tại địa điểm sử dụng điện; cứ 04 (bốn) người được tính là một hộ sử dụng điện để tính số định mức áp dụng giá bán lẻ điện sinh hoạt, cụ thể: 01 (một) người được tính là 1/4 định mức, 02 (hai) người được tính là 1/2 định mức, 03 (ba) người được tính là 3/4 định mức, 04 (bốn) người được tính là 01 định mức. Khi có thay đổi về số người thuê nhà, chủ nhà cho thuê có trách nhiệm thông báo cho bên bán điện để điều chỉnh định mức tính toán tiền điện;

- Trường hợp người thuê nhà không giao kết hợp đồng trực tiếp với bên bán điện thì tổng tiền điện chủ nhà cho thuê thu của người thuê nhà không được vượt quá tiền điện trong hoá đơn tiền điện hằng tháng do đơn vị bán lẻ điện phát hành;

ười thuê nhà không giao kết hợp đồng trực tiếp với bên bán điện thì tổng tiền điện chủ nhà cho thuê thu của người thuê nhà không được vượt quá tiền điện trong hoá đơn tiền điện hằng tháng do đơn vị bán lẻ điện phát hành;

- Bên bán điện được phép yêu cầu bên mua điện cung cấp thông tin về cư trú tại địa điểm sử dụng điện để làm căn cứ xác định số người tính số định mức khi tính toán hóa đơn tiền điện.” [1].

- Thông-tư-60-2025-TT-BCT — Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp: “Điều 21. Hiệu lực thi hành
Điều 21. Hiệu lực thi hành

Điều 21. Hiệu lực thi hành | Khoản 1
1. Thông tư này có hiệu lực thi hành từ ngày 02 tháng 12 năm 2025, trừ quy định tại khoản 3 Điều 4, khoản 1 và khoản 2 Điều 5, Điều 9, Điều 10, khoản 10 Điều 11, khoản 3 Điều 12, khoản 4 Điều 12, điểm c khoản 5 Điều 12, khoản 6 Điều 14, khoản 6 Điều 15 Thông tư này và Phụ lục ban hành kèm theo Thông tư này có hiệu lực thi hành kể từ ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành.

Điều 20. Điều khoản chuyển tiếp
Điều 20. Điều khoản chuyển tiếp

Điều 20. Điều khoản chuyển tiếp | Khoản 1
1. Các quy định tại Thông tư số 16/2014/TT-BCT ngày 29 tháng 5 năm 2014 của Bộ trưởng Bộ Công Thương quy định về giá bán điện được tiếp tục áp dụng từ ngày Thông tư này có hiệu lực đến ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành, bao gồm:

Điều 20. Điều khoản chuyển tiếp | Khoản 1 | Điểm a
1. Các quy định tại Thông tư số 16/2014/TT-BCT ngày 29 tháng 5 năm 2014 của Bộ trưởng Bộ Công Thương quy định về giá bán điện được tiếp tục áp dụng từ ngày Thông tư này có hiệu lực đến ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành, bao gồm: a) Khoản 1 Điều 5;

Điều 20. Điều khoản chuyển tiếp | Khoản 1 | Điểm b
1. Các quy định tại Thông tư số 16/2014/TT-BCT ngày 29 tháng 5 năm 2014 của Bộ trưởng Bộ Công Thương quy định về giá bán điện được tiếp tục áp dụng từ ngày Thông tư này có hiệu lực đến ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành, bao gồm: b) Khoản 10 Điều 8;

Điều 20. Điều khoản chuyển tiếp | Khoản 1 | Điểm c
1. Các quy định tại Thông tư số 16/2014/TT-BCT ngày 29 tháng 5 năm 2014 của Bộ trưởng Bộ Công Thương quy định về giá bán điện được tiếp tục áp dụng từ ngày Thông tư này có hiệu lực đến ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành, bao gồm: c) Khoản 3 Điều 10 (đã được sửa đổi theo quy định tại khoản 3 Điều 1 của Thông tư số 09/2023/TT-BCT sửa đổi, bổ sung một số điều của Thông tư số 16/2014/TT-BCT và Thông tư số 25/2018/TT-BCT ngày 12 tháng 9 năm 2018 của Bộ trưởng Bộ Công Thương sửa đổi, bổ sung một số điều của Thông tư số 16/2014/TT-BCT);

Điều 20. Điều khoản chuyển tiếp | Khoản 1 | Điểm d
1. Các quy định tại Thông tư số 16/2014/TT-BCT ngày 29 tháng 5 năm 2014 của Bộ trưởng Bộ Công Thương quy định về giá bán điện được tiếp tục áp dụng từ ngày Thông tư này có hiệu lực đến ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành, bao gồm: d) Điểm c khoản 4 Điều 10 (đã được sửa đổi theo quy định tại khoản 5 Điều 1 của Thông tư số 25/2018/TT-BCT và khoản 2 Điều 2 của Thông tư số 09/2023/TT-BCT);

Điều 20. Điều khoản chuyển tiếp | Khoản 1 | Điểm đ
1. Các quy định tại Thông tư số 16/2014/TT-BCT ngày 29 tháng 5 năm 2014 của Bộ trưởng Bộ Công Thương quy định về giá bán điện được tiếp tục áp dụng từ ngày Thông tư này có hiệu lực đến ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành, bao gồm: đ) Khoản 6 Điều 12 (đã được sửa đổi theo quy định tại khoản 7 Điều 1 của Thông tư số 09/2023/TT-BCT);

Điều 20. Điều khoản chuyển tiếp | Khoản 1 | Điểm e
1. Các quy định tại Thông tư số 16/2014/TT-BCT ngày 29 tháng 5 năm 2014 của Bộ trưởng Bộ Công Thương quy định về giá bán điện được tiếp tục áp dụng từ ngày Thông tư này có hiệu lực đến ngày thực hiện điều chỉnh mức giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực thi hành, bao gồm: e) Khoản 6 Điều 13 (đã được sửa đổi theo quy định tại khoản 9 Điều 1 của Thông tư số 09/2023/TT-BCT).” [3].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng; cần đối chiếu phần còn thiếu.

Nguồn có hiệu lực có điều kiện; chưa xác nhận văn bản/sự kiện kích hoạt.

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng, hiệu lực và bản gốc.

#### C — Đáp án bạn gửi

**Có.** Theo quy định của Bộ Công Thương và nguyên tắc giao kết hợp đồng dân sự:
- Chủ trọ có trách nhiệm công khai, minh bạch số điện tiêu thụ bằng việc cho phép người thuê cùng chốt chỉ số công tơ vào kỳ thanh toán.
- Bảng kê thanh toán hàng tháng phải nêu rõ: Chỉ số cũ, chỉ số mới, lượng điện tiêu thụ (kWh), đơn giá áp dụng và thành tiền.

#### D — Chatbot dạng agent

Chưa đủ căn cứ từ nguồn để trả lời việc chủ trọ có bắt buộc phải thông báo riêng cách tính tiền điện và số điện đã sử dụng hay không [1].

- Khi người thuê nhà không ký hợp đồng trực tiếp với bên bán điện thì tổng tiền điện chủ nhà thu không được vượt quá số tiền ghi trong hóa đơn hằng tháng của đơn vị bán lẻ điện [1].
- Trường hợp thuê nhà dưới 12 tháng và chủ nhà không kê khai đủ số người thì tiền điện được tính theo giá bán lẻ điện sinh hoạt bậc 2 cho toàn bộ sản lượng đo đếm được tại công tơ [1].
- Trường hợp chủ nhà kê khai đầy đủ số người thì bên bán điện cấp định mức tính tiền điện sinh hoạt theo thông tin cư trú với tỷ lệ bốn người được tính là một định mức [1].
- Khuyến nghị người thuê trọ chủ động đối chiếu hóa đơn tiền điện hằng tháng do đơn vị bán lẻ điện phát hành với số tiền chủ nhà thông báo thu [1].

Quy định áp dụng cho sinh viên và người lao động tại điểm c khoản 5 Điều 12 chỉ có hiệu lực từ ngày thực hiện điều chỉnh giá bán lẻ điện bình quân gần nhất sau ngày Quyết định số 14/2025/QĐ-TTg có hiệu lực [1] [3].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng.
Nguồn có hiệu lực có điều kiện; chưa xác nhận văn bản/sự kiện kích hoạt.

Để áp dụng vào trường hợp của bạn:
- Hợp đồng thuê phòng có điều khoản thỏa thuận về việc thông báo số điện và cách tính tiền điện hằng tháng không?
- Thời hạn hợp đồng thuê trọ của bạn là bao nhiêu tháng và chủ nhà đã đăng ký tạm trú cho bạn chưa?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

Nguồn truy xuất của D (rank dùng trong trích dẫn):

- [1] Thông-tư-60-2025-TT-BCT — Điều 12. Giá bán lẻ điện sinh hoạt | Khoản 5
- [2] Thông-tư-60-2025-TT-BCT
- [3] Thông-tư-60-2025-TT-BCT — Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp

Lý do giới hạn/fallback của D:

- Phản hồi chưa đáp ứng đầy đủ yêu cầu chính; đánh dấu theo nội dung thay vì provider.

### Câu 9: Giá nước sinh hoạt áp dụng cho phòng trọ ở Cần Thơ được xác định theo căn cứ nào?

#### A — Gemini chatbot

* Theo Quyết-định-215-QĐ-UBND, Điều 1, trang 1, giá nước sạch sinh hoạt tại Cần Thơ được quy định theo đơn vị cấp nước, khu vực (đô thị, nông thôn) và từng nhóm khách hàng sử dụng [1].
* Biểu giá tiêu thụ nước sinh hoạt phân loại theo hộ dân cư, hộ nghèo hoặc các đối tượng tổ chức, kinh doanh tùy theo nguồn do các đơn vị cấp nước [3] hoặc Trung tâm Nước sạch và Vệ sinh môi trường nông thôn cung cấp [2].
* Chưa tìm thấy căn cứ trong các đoạn được cung cấp về quy định định mức hay cách tính giá nước cụ thể cho người thuê phòng trọ; Khuyến nghị: nên kiểm tra/đối chiếu hợp đồng thuê và làm việc với bên cung cấp nước để xác định nhóm khách hàng áp dụng.

Thông tin mang tính tham khảo, không thay thế tư vấn pháp lý chuyên nghiệp.

#### B — Gemini phân tích + Qwen trích nguồn

Các đoạn trả lời trực tiếp trong nguồn:

- Quyết-định-215-QĐ-UBND — Điều 1. Quy định giá nước sạch sinh hoạt tại đô thị và khu vực nông thôn áp dụng đối với các đơn vị kinh doanh nước sạch, các tổ chức và khách hàng sử dụng nước sạch trên địa bàn thành phố Cần Thơ như sau: | Khoản 2: “2. Giá nước sạch sinh hoạt tại đô thị, khu vực nông thôn do Trung tâm Nước sạch và Vệ sinh môi trường nông thôn cung cấp cho mục đích sinh hoạt:

STT

Nhóm khách hàng sử dụng nước sạch cho mục đích sinh hoạt

Giá tiêu thụ nước sạch (đồng/m3)

Nhóm 1

Hộ dân cư là hộ nghèo có sổ, hộ gia đình chính sách (gia đình Mẹ Việt Nam anh hùng, gia đình thương binh, gia đình liệt sĩ), hộ hiến đất.

4.000

Nhóm 2

Hộ dân cư và các nhóm đối tượng khác

7.450

(Giá đã bao gồm thuế giá trị gia tăng, chưa bao gồm phí bảo vệ môi trường đối với nước thải sinh hoạt)” [2].

- Quyết-định-215-QĐ-UBND — Điều 1. Quy định giá nước sạch sinh hoạt tại đô thị và khu vực nông thôn áp dụng đối với các đơn vị kinh doanh nước sạch, các tổ chức và khách hàng sử dụng nước sạch trên địa bàn thành phố Cần Thơ như sau: | Khoản 1: “1. Giá nước sạch sinh hoạt tại đô thị, khu vực nông thôn năm 2024 do các đơn vị cấp nước cung cấp:

STT

Nhóm khách hàng sử dụng nước sạch cho mục đích sinh hoạt

Giá tiêu thụ nước sạch (đồng/m3)

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

(Giá đã bao gồm thuế giá trị gia tăng, chưa bao gồm phí bảo vệ môi trường đối với nước thải sinh hoạt)” [3].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng; cần đối chiếu phần còn thiếu.

Cần văn bản địa phương Cần Thơ, phạm vi địa bàn và hiệu lực áp dụng.

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng, hiệu lực và bản gốc.

#### C — Đáp án bạn gửi

- Giá nước sạch sinh hoạt tại Cần Thơ do **UBND TP. Cần Thơ ban hành khung giá** áp dụng cho đơn vị cấp nước (như Cantho Water).
- Đối với sinh viên, người thuê trọ có đăng ký tạm trú: Có thể được chủ trọ đăng ký cấp **định mức nước sinh hoạt hộ gia đình** (thường là **4 m³/người/tháng** theo mức giá ưu đãi bậc 1).
- Mức giá nước sinh hoạt bậc thang dân cư tại Cần Thơ dao động từ khoảng 7.000 – 11.000 VNĐ/m³ (tùy theo khối lượng sử dụng và đã gồm thuế VAT, phí bảo vệ môi trường/thoát nước).

#### D — Chatbot dạng agent

Chưa đủ căn cứ quy định riêng cho phòng trọ, giá nước sinh hoạt tại thành phố Cần Thơ được xác định dựa trên đơn vị cung cấp, khu vực đô thị hay nông thôn và nhóm khách hàng sử dụng theo biểu giá quy định [2] [3].

- Khuyến nghị kiểm tra đơn vị cung cấp nước là Trung tâm Nước sạch và Vệ sinh môi trường nông thôn hay các đơn vị cấp nước khác trên địa bàn thành phố Cần Thơ [2] [3].
- Khuyến nghị xác định vị trí nhà trọ thuộc khu vực đô thị hay khu vực nông thôn theo danh mục biểu giá năm 2024 [3].
- Khuyến nghị đối chiếu nhóm đối tượng sử dụng nước sinh hoạt như hộ dân cư hoặc hộ nghèo có sổ để biết mức giá áp dụng tương ứng [2] [3].

Mức giá trong các bảng quy định đã bao gồm thuế giá trị gia tăng nhưng chưa bao gồm phí bảo vệ môi trường đối với nước thải sinh hoạt [2] [3].
Nguồn tài liệu không nêu quy định cụ thể về định mức, thủ tục đăng ký tạm trú hoặc cách thức tính tiền nước riêng biệt cho đối tượng sinh viên thuê phòng trọ [2] [3].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng.
Cần văn bản địa phương Cần Thơ, phạm vi địa bàn và hiệu lực áp dụng.

Để áp dụng vào trường hợp của bạn:
- Khu trọ của bạn do đơn vị cấp nước nào tại Cần Thơ cung cấp và nằm ở đô thị hay nông thôn?
- Chủ nhà trọ đang tính tiền nước theo hợp đồng hay theo hóa đơn của đơn vị cấp nước?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

Nguồn truy xuất của D (rank dùng trong trích dẫn):

- [1] Quyết-định-215-QĐ-UBND — Điều 1. Quy định giá nước sạch sinh hoạt tại đô thị và khu vực nông thôn áp dụng đối với các đơn vị kinh doanh nước sạch, các tổ chức và khách hàng sử dụng nước sạch trên địa bàn thành phố Cần Thơ như sau:
- [2] Quyết-định-215-QĐ-UBND — Điều 1. Quy định giá nước sạch sinh hoạt tại đô thị và khu vực nông thôn áp dụng đối với các đơn vị kinh doanh nước sạch, các tổ chức và khách hàng sử dụng nước sạch trên địa bàn thành phố Cần Thơ như sau: | Khoản 2
- [3] Quyết-định-215-QĐ-UBND — Điều 1. Quy định giá nước sạch sinh hoạt tại đô thị và khu vực nông thôn áp dụng đối với các đơn vị kinh doanh nước sạch, các tổ chức và khách hàng sử dụng nước sạch trên địa bàn thành phố Cần Thơ như sau: | Khoản 1

Lý do giới hạn/fallback của D:

- Phản hồi chưa đáp ứng đầy đủ yêu cầu chính; đánh dấu theo nội dung thay vì provider.

### Câu 10: Tôi nên kiểm tra gì khi chủ trọ thu tiền nước theo đầu người thay vì đồng hồ?

#### A — Gemini chatbot

Dưới đây là các nội dung bạn cần lưu ý khi đối chiếu tiền nước:

* Quyết định số 215/QĐ-UBND không quy định công thức chia chi phí giữa người thuê chung đồng hồ và không ấn định mức thu cố định theo đầu người [1]. Do đó, chưa tìm thấy căn cứ trong các đoạn được cung cấp để khẳng định việc thu theo đầu người là hợp pháp hay vi phạm [1].
* Khuyến nghị: nên kiểm tra, đối chiếu thỏa thuận về chi phí nước trong hợp đồng thuê phòng, số đo chỉ số nước thực tế và hóa đơn tiền nước của chủ nhà [1].
* Khuyến nghị: khi đối chiếu hóa đơn, cần xác định đúng đơn vị cấp nước, khu vực (đô thị/nông thôn), nhóm khách hàng và kỳ sử dụng theo biểu giá quy định [2], [3]; lưu ý giá theo Quyết định số 215/QĐ-UBND (áp dụng năm 2024 tại Cần Thơ) đã gồm thuế GTGT nhưng chưa gồm phí bảo vệ môi trường đối với nước thải sinh hoạt [2], [3].

*Lưu ý: Đây là thông tin tham khảo từ tài liệu được cung cấp, không thay thế cho tư vấn pháp lý chuyên nghiệp.*

#### B — Gemini phân tích + Qwen trích nguồn

Các đoạn trả lời trực tiếp trong nguồn:

- 215-QD-UBND-pham-vi-doi-chieu — ## Phạm vi chưa được tài liệu này xác định: “## Phạm vi chưa được tài liệu này xác định

Quyết định này không nêu công thức chia chi phí giữa những người thuê chung đồng hồ, không quy định một khoản thu cố định theo đầu người cho mọi phòng trọ. Việc đối chiếu tiền nước thu của người thuê cần xem thêm thỏa thuận trong hợp đồng, số đo và hóa đơn. Không thể kết luận cách chia chi phí hoặc một khoản thu riêng là hợp pháp hay vi phạm chỉ từ biểu giá này.” [2].

- 215-QD-UBND-pham-vi-doi-chieu — Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp: “## Điều 2 và Điều 3 — điều chỉnh và hiệu lực của nguồn
## Điều 2 và Điều 3 — điều chỉnh và hiệu lực của nguồn

Điều 2 quy định đơn vị cấp nước rà soát phương án giá và giá dự kiến năm tiếp theo. Điều 3 ghi thi hành kể từ ngày ký. Ngày có hiệu lực của văn bản gốc không chứng minh biểu giá chưa được điều chỉnh sau đó.” [4].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng; cần đối chiếu phần còn thiếu.

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng, hiệu lực và bản gốc.

#### C — Đáp án bạn gửi

Thu tiền nước theo đầu người là hình thức khoán phổ biến khi nhà trọ không lắp đồng hồ nước riêng cho từng phòng. Bạn nên kiểm tra:
1. **Mức khoán trung bình:** Tại Cần Thơ, mức thu khoán tiền nước phổ biến cho sinh viên dao động từ **30.000 – 50.000 VNĐ/người/tháng** (tương đương 3 – 5 m³ nước sinh hoạt).
2. **Nếu chủ trọ thu quá cao (80.000 – 100.000 VNĐ/người/tháng):** Bạn có quyền yêu cầu chủ trọ giải trình dựa trên hóa đơn tiền nước thực tế của đơn vị cấp nước chia bình quân cho tổng số nhân khẩu đang ở trọ.
3. **Thỏa thuận bằng văn bản:** Mức khoán theo đầu người phải được ghi cụ thể trong hợp đồng thuê nhà để tránh việc chủ trọ tăng giá tùy tiện vào mùa khô hoặc khi có người ở thêm.

#### D — Chatbot dạng agent

Chưa đủ căn cứ pháp lý để kết luận việc thu tiền nước theo đầu người có hợp pháp hay không do tài liệu không quy định công thức chia chi phí hoặc mức thu cố định cho mọi phòng trọ [2].

- Khuyến nghị người thuê trọ kiểm tra thỏa thuận cụ thể về phương thức tính tiền nước đã ghi nhận trong hợp đồng thuê [2].
- Khuyến nghị người thuê đối chiếu thêm số đo đồng hồ dùng chung và hóa đơn tiền nước thực tế phát sinh [2].

Quyết định không nêu công thức phân chia chi phí giữa những người dùng chung đồng hồ và không ấn định mức thu theo đầu người [2].
Không thể kết luận cách chia chi phí tiền nước là hợp pháp hay vi phạm chỉ dựa trên biểu giá của văn bản [2].
Ngày có hiệu lực của văn bản gốc không chứng minh biểu giá chưa được điều chỉnh sau thời điểm ban hành [4].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng.

Để áp dụng vào trường hợp của bạn:
- Hợp đồng thuê phòng của bạn có thỏa thuận cụ thể về cách thu tiền nước không?
- Khu trọ của bạn hiện có hóa đơn tiền nước và chỉ số đồng hồ tổng để đối chiếu không?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

Nguồn truy xuất của D (rank dùng trong trích dẫn):

- [1] 215-QD-UBND-pham-vi-doi-chieu — ## Điều 1 — đối tượng, khu vực và tiền nước trên hóa đơn
- [2] 215-QD-UBND-pham-vi-doi-chieu — ## Phạm vi chưa được tài liệu này xác định
- [3] Quyết-định-215-QĐ-UBND — Điều 1. Quy định giá nước sạch sinh hoạt tại đô thị và khu vực nông thôn áp dụng đối với các đơn vị kinh doanh nước sạch, các tổ chức và khách hàng sử dụng nước sạch trên địa bàn thành phố Cần Thơ như sau: | Khoản 2
- [4] 215-QD-UBND-pham-vi-doi-chieu — Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp

Lý do giới hạn/fallback của D:

- Phản hồi chưa đáp ứng đầy đủ yêu cầu chính; đánh dấu theo nội dung thay vì provider.

### Câu 11: Nếu nhà trọ dùng chung đồng hồ nước, cách phân chia chi phí nên được thỏa thuận ra sao?

#### A — Gemini chatbot

Các căn cứ liên quan tìm được trong kho (trích nguyên đoạn):

- 215-QD-UBND-pham-vi-doi-chieu — ## Phạm vi chưa được tài liệu này xác định: “Quyết định này không nêu công thức chia chi phí giữa những người thuê chung đồng hồ, không quy định một khoản thu cố định theo đầu người cho mọi phòng trọ. Việc đối chiếu tiền nước thu của người thuê cần xem thêm thỏa thuận trong hợp đồng, số đo và hóa đơn. Không thể kết luận cách chia chi phí hoặc một khoản thu riêng là hợp pháp hay vi phạm chỉ từ biểu giá này.” [1].

- 215-QD-UBND-pham-vi-doi-chieu — ## Điều 1 — đối tượng, khu vực và tiền nước trên hóa đơn: “Biểu giá phân theo khu vực đô thị/nông thôn, nhóm khách hàng và đơn vị cung cấp nước. Nhóm hộ dân cư khác nhóm kinh doanh, dịch vụ. Trung tâm Nước sạch và Vệ sinh môi trường nông thôn có nhóm giá riêng. Các bảng trong nguồn ghi giá đã bao gồm thuế giá trị gia tăng, chưa bao gồm phí bảo vệ môi trường đối với nước thải sinh hoạt. Khi đối chiếu hóa đơn cần xác định đúng đơn vị cấp nước, nhóm khách hàng, khu vực và kỳ sử dụng; không suy ra mọi nhà trọ thuộc cùng một nhóm giá.” [2].

Đây là câu trả lời một phần từ nguồn; chưa kết luận cách áp dụng cho tình huống riêng của bạn. Cần đối chiếu điều kiện, hiệu lực và bản gốc.

#### B — Gemini phân tích + Qwen trích nguồn

Các đoạn trả lời trực tiếp trong nguồn:

- 215-QD-UBND-pham-vi-doi-chieu — ## Phạm vi chưa được tài liệu này xác định: “## Phạm vi chưa được tài liệu này xác định

Quyết định này không nêu công thức chia chi phí giữa những người thuê chung đồng hồ, không quy định một khoản thu cố định theo đầu người cho mọi phòng trọ. Việc đối chiếu tiền nước thu của người thuê cần xem thêm thỏa thuận trong hợp đồng, số đo và hóa đơn. Không thể kết luận cách chia chi phí hoặc một khoản thu riêng là hợp pháp hay vi phạm chỉ từ biểu giá này.” [1].

- 215-QD-UBND-pham-vi-doi-chieu — Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp: “## Điều 2 và Điều 3 — điều chỉnh và hiệu lực của nguồn
## Điều 2 và Điều 3 — điều chỉnh và hiệu lực của nguồn

Điều 2 quy định đơn vị cấp nước rà soát phương án giá và giá dự kiến năm tiếp theo. Điều 3 ghi thi hành kể từ ngày ký. Ngày có hiệu lực của văn bản gốc không chứng minh biểu giá chưa được điều chỉnh sau đó.” [4].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng; cần đối chiếu phần còn thiếu.

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng, hiệu lực và bản gốc.

#### C — Đáp án bạn gửi

Khi dùng chung đồng hồ nước tổng, các bên có thể thỏa thuận 1 trong 2 phương án:
1. **Phương án chia theo đầu người:** Lấy tổng số tiền trên hóa đơn nhà nước chia đều cho tổng số người thực tế đang cư trú tại dãy trọ trong tháng.
2. **Lắp đồng hồ nước phụ (tiểu ly) cho từng phòng:** Mỗi phòng tự thanh toán theo số m³ thực tế trên đồng hồ phụ; phần chênh lệch hao hụt hoặc nước dùng chung sân bãi sẽ chia đều cho các phòng theo tỷ lệ thỏa thuận. Đây là phương án minh bạch và ít phát sinh tranh chấp nhất.

#### D — Chatbot dạng agent

Chưa đủ căn cứ từ nguồn để xác định công thức phân chia chi phí tiền nước cụ thể khi dùng chung đồng hồ [1].

- Khuyến nghị các bên xem xét thỏa thuận cụ thể trong hợp đồng thuê trọ cùng với số đo đồng hồ và hóa đơn tiền nước thực tế phát sinh [1].

Tài liệu không quy định một công thức chia chi phí chung hay mức thu cố định theo đầu người cho mọi phòng trọ [1].
Không thể kết luận cách chia chi phí hoặc một khoản thu riêng là hợp pháp hay vi phạm chỉ dựa vào biểu giá trong văn bản [1].
Ngày có hiệu lực của văn bản gốc không chứng minh biểu giá chưa từng được điều chỉnh sau đó [4].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng.

Để áp dụng vào trường hợp của bạn:
- Hợp đồng thuê trọ hiện tại có điều khoản thỏa thuận cụ thể nào về cách chia tiền nước không?
- Nhà trọ của bạn thuộc tỉnh, thành phố nào?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

Nguồn truy xuất của D (rank dùng trong trích dẫn):

- [1] 215-QD-UBND-pham-vi-doi-chieu — ## Phạm vi chưa được tài liệu này xác định
- [2] 215-QD-UBND-pham-vi-doi-chieu — ## Điều 1 — đối tượng, khu vực và tiền nước trên hóa đơn
- [3] Quyết-định-215-QĐ-UBND — Điều 1. Quy định giá nước sạch sinh hoạt tại đô thị và khu vực nông thôn áp dụng đối với các đơn vị kinh doanh nước sạch, các tổ chức và khách hàng sử dụng nước sạch trên địa bàn thành phố Cần Thơ như sau: | Khoản 2
- [4] 215-QD-UBND-pham-vi-doi-chieu — Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp

Lý do giới hạn/fallback của D:

- Phản hồi chưa đáp ứng đầy đủ yêu cầu chính; đánh dấu theo nội dung thay vì provider.

### Câu 12: Tôi có thể đối chiếu tiền nước trên hóa đơn với đơn vị cấp nước như thế nào?

#### A — Gemini chatbot

- Theo nguồn [1], Điều 1 (trang 1), khi đối chiếu hóa đơn tiền nước cần xác định đúng đơn vị cấp nước, nhóm khách hàng, khu vực (đô thị hoặc nông thôn) và kỳ sử dụng; không suy ra mọi nhà trọ thuộc cùng một nhóm giá. Giá trên bảng biểu đã bao gồm thuế giá trị gia tăng nhưng chưa gồm phí bảo vệ môi trường đối với nước thải sinh hoạt [1].
- Theo Quyết định 215/QĐ-UBND, Điều 1, Khoản 1 (trang 1), mức giá nước sinh hoạt năm 2024 tại Cần Thơ được quy định cụ thể theo từng nhóm, như hộ dân cư đô thị là 9.020 đồng/m³ hoặc nông thôn là 8.240 đồng/m³ [3]. Tuy nhiên, ngày có hiệu lực của văn bản gốc không chứng minh biểu giá chưa được điều chỉnh sau đó theo nguồn [4], Điều 2 và Điều 3 (trang 1).
- Chưa tìm thấy căn cứ trong các đoạn được cung cấp về quy trình chi tiết để người thuê khiếu nại hay các bước trực tiếp làm việc với đơn vị cấp nước.

Thông tin mang tính tham khảo, không thay thế tư vấn pháp lý chuyên nghiệp.

#### B — Gemini phân tích + Qwen trích nguồn

Các đoạn trả lời trực tiếp trong nguồn:

- 215-QD-UBND-pham-vi-doi-chieu — ## Điều 1 — đối tượng, khu vực và tiền nước trên hóa đơn: “## Điều 1 — đối tượng, khu vực và tiền nước trên hóa đơn

Biểu giá phân theo khu vực đô thị/nông thôn, nhóm khách hàng và đơn vị cung cấp nước. Nhóm hộ dân cư khác nhóm kinh doanh, dịch vụ. Trung tâm Nước sạch và Vệ sinh môi trường nông thôn có nhóm giá riêng. Các bảng trong nguồn ghi giá đã bao gồm thuế giá trị gia tăng, chưa bao gồm phí bảo vệ môi trường đối với nước thải sinh hoạt. Khi đối chiếu hóa đơn cần xác định đúng đơn vị cấp nước, nhóm khách hàng, khu vực và kỳ sử dụng; không suy ra mọi nhà trọ thuộc cùng một nhóm giá.” [1].

- 215-QD-UBND-pham-vi-doi-chieu — Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp: “## Điều 2 và Điều 3 — điều chỉnh và hiệu lực của nguồn
## Điều 2 và Điều 3 — điều chỉnh và hiệu lực của nguồn

Điều 2 quy định đơn vị cấp nước rà soát phương án giá và giá dự kiến năm tiếp theo. Điều 3 ghi thi hành kể từ ngày ký. Ngày có hiệu lực của văn bản gốc không chứng minh biểu giá chưa được điều chỉnh sau đó.” [4].

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng, hiệu lực và bản gốc.

#### C — Đáp án bạn gửi

- Bạn có thể xem trên hóa đơn giấy/điện tử của chủ nhà để lấy **Mã khách hàng / Danh bộ** (thường in trên hóa đơn của Cantho Water).
- Truy cập website tra cứu hoặc cổng dịch vụ của **Công ty Cổ phần Cấp thoát nước Cần Thơ** (hoặc qua Zalo OA "Cấp thoát nước Cần Thơ") nhập mã danh bộ để kiểm tra chính xác sản lượng nước tiêu thụ và số tiền thực tế phải thanh toán.

#### D — Chatbot dạng agent

Bạn có thể đối chiếu tiền nước dựa trên việc xác định chính xác đơn vị cấp nước, nhóm khách hàng, khu vực và kỳ sử dụng theo biểu giá quy định [1].

- Khuyến nghị xác định rõ đơn vị cung cấp nước thực tế và khu vực sử dụng nước là đô thị hay nông thôn [1].
- Khuyến nghị kiểm tra nhóm khách hàng áp dụng trên hóa đơn vì nhóm hộ dân cư có mức giá khác với nhóm kinh doanh, dịch vụ [1].
- Khuyến nghị đối chiếu kỳ sử dụng và lưu ý giá trong bảng đã gồm thuế giá trị gia tăng nhưng chưa gồm phí bảo vệ môi trường đối với nước thải sinh hoạt [1].

Không được mặc định suy ra mọi nhà trọ đều áp dụng chung một nhóm giá nước [1].
Nguồn chưa cung cấp quy trình nộp đơn hoặc khiếu nại cụ thể tới đơn vị cấp nước, đồng thời ngày hiệu lực của văn bản gốc không chứng minh biểu giá chưa bị điều chỉnh sau đó [4].

Chưa đủ căn cứ để kết luận toàn bộ yêu cầu; cần đối chiếu phần còn thiếu.

Để áp dụng vào trường hợp của bạn:
- Hóa đơn tiền nước của bạn do đơn vị cấp nước nào phát hành?
- Hợp đồng sử dụng nước đứng tên bạn trực tiếp hay qua chủ nhà trọ?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

Nguồn truy xuất của D (rank dùng trong trích dẫn):

- [1] 215-QD-UBND-pham-vi-doi-chieu — ## Điều 1 — đối tượng, khu vực và tiền nước trên hóa đơn
- [2] Quyết-định-215-QĐ-UBND — Điều 1. Quy định giá nước sạch sinh hoạt tại đô thị và khu vực nông thôn áp dụng đối với các đơn vị kinh doanh nước sạch, các tổ chức và khách hàng sử dụng nước sạch trên địa bàn thành phố Cần Thơ như sau:
- [3] Quyết-định-215-QĐ-UBND — Điều 1. Quy định giá nước sạch sinh hoạt tại đô thị và khu vực nông thôn áp dụng đối với các đơn vị kinh doanh nước sạch, các tổ chức và khách hàng sử dụng nước sạch trên địa bàn thành phố Cần Thơ như sau: | Khoản 1
- [4] 215-QD-UBND-pham-vi-doi-chieu — Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp

Lý do giới hạn/fallback của D:

- Phản hồi chưa đáp ứng đầy đủ yêu cầu chính; đánh dấu theo nội dung thay vì provider.

### Câu 13: Sinh viên thuê trọ tại Cần Thơ cần làm thủ tục cư trú nào?

#### A — Gemini chatbot

Các căn cứ liên quan tìm được trong kho (trích nguyên đoạn):

- Luat-68-2020-QH14-doi-chieu-20261003 — Điều 27. Điều kiện đăng ký tạm trú | Khoản 1: “1. Công dân đến sinh sống tại chỗ ở hợp pháp ngoài phạm vi đơn vị hành chính cấp xã nơi đã đăng ký thường trú để lao động, học tập hoặc vì mục đích khác từ 30 ngày trở lên thì phải thực hiện đăng ký tạm trú.” [1].

Đây là câu trả lời một phần từ nguồn; chưa kết luận cách áp dụng cho tình huống riêng của bạn. Cần đối chiếu điều kiện, hiệu lực và bản gốc.

#### B — Gemini phân tích + Qwen trích nguồn

Các đoạn trả lời trực tiếp trong nguồn:

- Luat-68-2020-QH14-doi-chieu-20261003 — Điều 27. Điều kiện đăng ký tạm trú | Khoản 1: “1. Công dân đến sinh sống tại chỗ ở hợp pháp ngoài phạm vi đơn vị hành chính cấp xã nơi đã đăng ký thường trú để lao động, học tập hoặc vì mục đích khác từ 30 ngày trở lên thì phải thực hiện đăng ký tạm trú.” [1].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng; cần đối chiếu phần còn thiếu.

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng, hiệu lực và bản gốc.

#### C — Đáp án bạn gửi

Căn cứ theo **Điều 27 Luật Cư trú 2020**:
- Công dân đến sinh sống tại chỗ ở hợp pháp ngoài phạm vi đơn vị hành chính cấp xã nơi đã đăng ký thường trú từ **30 ngày trở lên** phải thực hiện **Đăng ký tạm trú**.
- **Thời hạn làm thủ tục:** Trong vòng **30 ngày** kể từ ngày chuyển đến phòng trọ mới.
- **Thời hạn tạm trú:** Tối đa là **02 năm** cho một lần đăng ký và có thể gia hạn nhiều lần.

#### D — Chatbot dạng agent

Các đoạn trả lời trực tiếp trong nguồn:

- Luat-68-2020-QH14-doi-chieu-20261003 — Điều 27. Điều kiện đăng ký tạm trú | Khoản 1: “1. Công dân đến sinh sống tại chỗ ở hợp pháp ngoài phạm vi đơn vị hành chính cấp xã nơi đã đăng ký thường trú để lao động, học tập hoặc vì mục đích khác từ 30 ngày trở lên thì phải thực hiện đăng ký tạm trú.” [1].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng; cần đối chiếu phần còn thiếu.

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng, hiệu lực và bản gốc.

Nguồn truy xuất của D (rank dùng trong trích dẫn):

- [1] Luat-68-2020-QH14-doi-chieu-20261003 — Điều 27. Điều kiện đăng ký tạm trú | Khoản 1
- [2] Luat-68-2020-QH14-doi-chieu-20261003 — Điều 27. Điều kiện đăng ký tạm trú | Khoản 2
- [3] Luat-68-2020-QH14-doi-chieu-20261003 — Điều 27. Điều kiện đăng ký tạm trú | Khoản 3

Lý do giới hạn/fallback của D:

- Gemini phân tích câu hỏi chưa khả dụng (ValidationError); dùng định tuyến chủ đề dự phòng.
- Nguồn trích dẫn bị cụt điều kiện hoặc ngoại lệ; chưa đủ để kết luận.
- Bản tổng hợp chưa được nguồn xác nhận sau lần sửa; dùng trích đoạn Qwen đã chọn.
- Phản hồi chưa đáp ứng đầy đủ yêu cầu chính; đánh dấu theo nội dung thay vì provider.

### Câu 14: Ai có trách nhiệm cung cấp thông tin, giấy tờ để người thuê đăng ký tạm trú?

#### A — Gemini chatbot

Dựa trên thông tin được cung cấp:

- Công dân có nghĩa vụ cung cấp đầy đủ, chính xác, kịp thời thông tin, giấy tờ, tài liệu về cư trú của mình cho cơ quan, người có thẩm quyền và tự chịu trách nhiệm về các giấy tờ đã cung cấp theo văn bản Luat-68-2020-QH14-doi-chieu-20261003, Điều 9, Khoản 2, trang 1 [2].
- Người đăng ký tạm trú có trách nhiệm nộp hồ sơ gồm tờ khai thay đổi thông tin cư trú và giấy tờ, tài liệu chứng minh chỗ ở hợp pháp đến cơ quan đăng ký cư trú theo văn bản Luat-68-2020-QH14-doi-chieu-20261003, Điều 28, Khoản 1, 2, trang 1 [1], [3].
- Chưa tìm thấy căn cứ trong các đoạn được cung cấp quy định cụ thể về trách nhiệm của chủ trọ trong việc cung cấp thông tin, giấy tờ; Khuyến nghị: người thuê nên đối chiếu thỏa thuận hợp đồng và liên hệ cơ quan công an địa phương để được hướng dẫn chi tiết.

Lưu ý: Đây là thông tin tham khảo, không thay thế tư vấn pháp lý chuyên nghiệp.

#### B — Gemini phân tích + Qwen trích nguồn

Các đoạn trả lời trực tiếp trong nguồn:

- Luat-68-2020-QH14-doi-chieu-20261003 — Điều 28. Hồ sơ, thủ tục đăng ký tạm trú, gia hạn tạm trú | Khoản 1: “1. Hồ sơ đăng ký tạm trú bao gồm:

1. Hồ sơ đăng ký tạm trú bao gồm: a) Tờ khai thay đổi thông tin cư trú; đối với người đăng ký tạm trú là người chưa thành niên thì trong tờ khai phải ghi rõ ý kiến đồng ý của cha, mẹ hoặc người giám hộ, trừ trường hợp đã có ý kiến đồng ý bằng văn bản;

1. Hồ sơ đăng ký tạm trú bao gồm: b) Giấy tờ, tài liệu chứng minh chỗ ở hợp pháp.” [1].

- Luat-68-2020-QH14-doi-chieu-20261003 — Điều 28. Hồ sơ, thủ tục đăng ký tạm trú, gia hạn tạm trú | Khoản 2: “2. Người đăng ký tạm trú nộp hồ sơ đăng ký tạm trú đến cơ quan đăng ký cư trú nơi mình dự kiến tạm trú.

Khi tiếp nhận hồ sơ đăng ký tạm trú, cơ quan đăng ký cư trú kiểm tra và cấp phiếu tiếp nhận hồ sơ cho người đăng ký; trường hợp hồ sơ chưa đầy đủ thì hướng dẫn người đăng ký bổ sung hồ sơ.

Trong thời hạn 03 ngày làm việc kể từ ngày nhận được hồ sơ đầy đủ và hợp lệ, cơ quan đăng ký cư trú có trách nhiệm thẩm định, cập nhật thông tin về nơi tạm trú mới, thời hạn tạm trú của người đăng ký vào Cơ sở dữ liệu về cư trú và thông báo cho người đăng ký về việc đã cập nhật thông tin đăng ký tạm trú; trường hợp từ chối đăng ký thì phải trả lời bằng văn bản và nêu rõ lý do.” [2].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng; cần đối chiếu phần còn thiếu.

Nguồn hiện có xác nhận nghĩa vụ của công dân và hồ sơ đăng ký; chưa có căn cứ riêng để kết luận toàn bộ nghĩa vụ cung cấp giấy tờ của chủ trọ.

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng, hiệu lực và bản gốc.

#### C — Đáp án bạn gửi

- **Trách nhiệm của chủ nhà trọ:** Phải tạo điều kiện, cung cấp thông tin chỗ ở hợp pháp, ký hợp đồng thuê và phối hợp làm thủ tục (hoặc chủ trọ có thể trực tiếp làm thủ tục đăng ký tạm trú thay cho người thuê trọ theo quy định).
- **Trách nhiệm của sinh viên:** Cung cấp ảnh CCCD, điền Tờ khai thay đổi thông tin cư trú (mẫu CT01).
- **Mức phạt nếu không đăng ký:** Theo Điều 9 Nghị định 144/2021/NĐ-CP, cả người thuê và chủ trọ không thực hiện đúng quy định về đăng ký tạm trú có thể bị phạt tiền từ **500.000 đến 1.000.000 đồng**.

#### D — Chatbot dạng agent

Chưa đủ căn cứ từ nguồn trích dẫn để xác định cụ thể ai có trách nhiệm cung cấp thông tin, giấy tờ cho người thuê, do nguồn chỉ quy định thành phần hồ sơ và trách nhiệm nộp hồ sơ của người đăng ký tạm trú [1] [2].

- Người đăng ký tạm trú chuẩn bị tờ khai thay đổi thông tin cư trú, lưu ý đối với người chưa thành niên phải có ý kiến đồng ý của cha, mẹ hoặc người giám hộ trong tờ khai trừ khi đã có văn bản đồng ý riêng [1].
- Người đăng ký tạm trú chuẩn bị giấy tờ, tài liệu chứng minh chỗ ở hợp pháp [1].
- Người đăng ký tạm trú nộp hồ sơ đến cơ quan đăng ký cư trú nơi mình dự kiến tạm trú và nhận phiếu tiếp nhận hồ sơ hoặc được hướng dẫn bổ sung nếu hồ sơ chưa đầy đủ [2].
- Cơ quan đăng ký cư trú thẩm định, cập nhật thông tin vào Cơ sở dữ liệu về cư trú và thông báo kết quả trong thời hạn 03 ngày làm việc kể từ ngày nhận đủ hồ sơ hợp lệ, hoặc trả lời từ chối bằng văn bản nêu rõ lý do [2].

Nguồn tài liệu chưa quy định trách nhiệm cụ thể của bên cho thuê về việc cung cấp giấy tờ chứng minh chỗ ở hợp pháp cho người thuê [1].
Khuyến nghị người thuê kiểm tra thỏa thuận trong hợp đồng thuê nhà để làm rõ nghĩa vụ cung cấp hồ sơ giữa các bên [1].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng.
Nguồn hiện có xác nhận nghĩa vụ của công dân và hồ sơ đăng ký; chưa có căn cứ riêng để kết luận toàn bộ nghĩa vụ cung cấp giấy tờ của chủ trọ.

Để áp dụng vào trường hợp của bạn:
- Hợp đồng thuê phòng của bạn có điều khoản nào quy định trách nhiệm của chủ trọ trong việc hỗ trợ giấy tờ đăng ký tạm trú không?
- Bạn hiện đã có giấy tờ chứng minh chỗ ở hợp pháp như hợp đồng thuê nhà để tự nộp hồ sơ chưa?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

Nguồn truy xuất của D (rank dùng trong trích dẫn):

- [1] Luat-68-2020-QH14-doi-chieu-20261003 — Điều 28. Hồ sơ, thủ tục đăng ký tạm trú, gia hạn tạm trú | Khoản 1
- [2] Luat-68-2020-QH14-doi-chieu-20261003 — Điều 28. Hồ sơ, thủ tục đăng ký tạm trú, gia hạn tạm trú | Khoản 2
- [3] Luat-68-2020-QH14-doi-chieu-20261003 — Điều 28. Hồ sơ, thủ tục đăng ký tạm trú, gia hạn tạm trú | Khoản 3

Lý do giới hạn/fallback của D:

- Phản hồi chưa đáp ứng đầy đủ yêu cầu chính; đánh dấu theo nội dung thay vì provider.

### Câu 15: Tôi cần chuẩn bị những giấy tờ gì để đăng ký tạm trú tại phòng trọ?

#### A — Gemini chatbot

Căn cứ theo văn bản Luat-68-2020-QH14-doi-chieu-20261003, Điều 28, trang 1, bạn cần chuẩn bị hồ sơ đăng ký tạm trú gồm các giấy tờ sau:

* Tờ khai thay đổi thông tin cư trú; trường hợp người đăng ký là người chưa thành niên thì trong tờ khai phải ghi rõ ý kiến đồng ý của cha, mẹ hoặc người giám hộ, trừ khi đã có văn bản đồng ý riêng [1].
* Giấy tờ, tài liệu chứng minh chỗ ở hợp pháp [1].
* Hồ sơ được nộp đến cơ quan đăng ký cư trú nơi dự kiến tạm trú và được giải quyết cập nhật trong 03 ngày làm việc kể từ khi nhận đủ hồ sơ hợp lệ [2].

Thông tin trên chỉ mang tính tham khảo, không thay thế cho tư vấn pháp lý chuyên nghiệp.

#### B — Gemini phân tích + Qwen trích nguồn

Các đoạn trả lời trực tiếp trong nguồn:

- Luat-68-2020-QH14-doi-chieu-20261003 — Điều 28. Hồ sơ, thủ tục đăng ký tạm trú, gia hạn tạm trú | Khoản 1: “1. Hồ sơ đăng ký tạm trú bao gồm:

1. Hồ sơ đăng ký tạm trú bao gồm: a) Tờ khai thay đổi thông tin cư trú; đối với người đăng ký tạm trú là người chưa thành niên thì trong tờ khai phải ghi rõ ý kiến đồng ý của cha, mẹ hoặc người giám hộ, trừ trường hợp đã có ý kiến đồng ý bằng văn bản;

1. Hồ sơ đăng ký tạm trú bao gồm: b) Giấy tờ, tài liệu chứng minh chỗ ở hợp pháp.” [1].

- Luat-68-2020-QH14-doi-chieu-20261003 — Điều 28. Hồ sơ, thủ tục đăng ký tạm trú, gia hạn tạm trú | Khoản 3: “3. Trong thời hạn 15 ngày trước ngày kết thúc thời hạn tạm trú đã đăng ký, công dân phải làm thủ tục gia hạn tạm trú.

Hồ sơ, thủ tục gia hạn tạm trú thực hiện theo quy định tại khoản 1 và khoản 2 Điều này. Sau khi thẩm định hồ sơ, cơ quan đăng ký cư trú có trách nhiệm cập nhật thông tin về thời hạn tạm trú mới của người đăng ký vào Cơ sở dữ liệu về cư trú và thông báo cho người đăng ký về việc đã cập nhật thông tin đăng ký tạm trú; trường hợp từ chối đăng ký thì phải trả lời bằng văn bản và nêu rõ lý do.” [2].

- Luat-68-2020-QH14-doi-chieu-20261003 — Điều 28. Hồ sơ, thủ tục đăng ký tạm trú, gia hạn tạm trú | Khoản 2: “2. Người đăng ký tạm trú nộp hồ sơ đăng ký tạm trú đến cơ quan đăng ký cư trú nơi mình dự kiến tạm trú.

Khi tiếp nhận hồ sơ đăng ký tạm trú, cơ quan đăng ký cư trú kiểm tra và cấp phiếu tiếp nhận hồ sơ cho người đăng ký; trường hợp hồ sơ chưa đầy đủ thì hướng dẫn người đăng ký bổ sung hồ sơ.

Trong thời hạn 03 ngày làm việc kể từ ngày nhận được hồ sơ đầy đủ và hợp lệ, cơ quan đăng ký cư trú có trách nhiệm thẩm định, cập nhật thông tin về nơi tạm trú mới, thời hạn tạm trú của người đăng ký vào Cơ sở dữ liệu về cư trú và thông báo cho người đăng ký về việc đã cập nhật thông tin đăng ký tạm trú; trường hợp từ chối đăng ký thì phải trả lời bằng văn bản và nêu rõ lý do.” [3].

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng, hiệu lực và bản gốc.

#### C — Đáp án bạn gửi

Căn cứ **Điều 28 Luật Cư trú 2020**, hồ sơ gồm:
1. **Tờ khai thay đổi thông tin cư trú (Mẫu CT01)** (có chữ ký xác nhận đồng ý của chủ trọ/chủ sở hữu chỗ ở hợp pháp).
2. **Giấy tờ chứng minh chỗ ở hợp pháp:** Hợp đồng thuê nhà trọ hợp pháp còn hiệu lực (không bắt buộc công chứng).
3. **Bản sao CCCD/Thẻ căn cước** của người đăng ký.
*Hình thức nộp:* Sinh viên có thể nộp trực tiếp tại Công an phường/xã hoặc **nộp trực tuyến cực kỳ thuận tiện qua Cổng dịch vụ công Bộ Công an** hoặc **Ứng dụng VNeID (định danh mức 2)**.

#### D — Chatbot dạng agent

Bạn cần chuẩn bị hồ sơ gồm tờ khai thay đổi thông tin cư trú và giấy tờ chứng minh chỗ ở hợp pháp để nộp cho cơ quan đăng ký cư trú [1] [3].

- Bạn chuẩn bị tờ khai thay đổi thông tin cư trú theo quy định [1].
- Bạn chuẩn bị giấy tờ, tài liệu chứng minh chỗ ở hợp pháp tại phòng trọ [1].
- Bạn nộp hồ sơ đã chuẩn bị đến cơ quan đăng ký cư trú nơi mình dự kiến tạm trú [3].
- Bạn nhận phiếu tiếp nhận hồ sơ từ cơ quan đăng ký cư trú và bổ sung hồ sơ nếu có hướng dẫn [3].
- Cơ quan đăng ký cư trú thẩm định, cập nhật thông tin vào Cơ sở dữ liệu về cư trú và thông báo kết quả trong 03 ngày làm việc kể từ khi nhận đủ hồ sơ hợp lệ [3].

Đối với người đăng ký tạm trú là người chưa thành niên thì trong tờ khai phải ghi rõ ý kiến đồng ý của cha, mẹ hoặc người giám hộ, trừ trường hợp đã có ý kiến đồng ý bằng văn bản [1].
Trường hợp từ chối đăng ký thì cơ quan đăng ký cư trú phải trả lời bằng văn bản và nêu rõ lý do [3].

Để áp dụng vào trường hợp của bạn:
- Bạn đã đủ tuổi thành niên theo quy định hay chưa?
- Bạn đã có hợp đồng thuê phòng trọ hoặc giấy tờ chứng minh chỗ ở hợp pháp chưa?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

Nguồn truy xuất của D (rank dùng trong trích dẫn):

- [1] Luat-68-2020-QH14-doi-chieu-20261003 — Điều 28. Hồ sơ, thủ tục đăng ký tạm trú, gia hạn tạm trú | Khoản 1
- [2] Luat-68-2020-QH14-doi-chieu-20261003 — Điều 28. Hồ sơ, thủ tục đăng ký tạm trú, gia hạn tạm trú | Khoản 3
- [3] Luat-68-2020-QH14-doi-chieu-20261003 — Điều 28. Hồ sơ, thủ tục đăng ký tạm trú, gia hạn tạm trú | Khoản 2

### Câu 16: Nếu chuyển sang phòng trọ khác, tôi cần cập nhật thông tin cư trú thế nào?

#### A — Gemini chatbot

Các căn cứ liên quan tìm được trong kho (trích nguyên đoạn):

- Luat-68-2020-QH14-doi-chieu-20261003 — Điều 28. Hồ sơ, thủ tục đăng ký tạm trú, gia hạn tạm trú | Khoản 3: “Hồ sơ, thủ tục gia hạn tạm trú thực hiện theo quy định tại khoản 1 và khoản 2 Điều này. Sau khi thẩm định hồ sơ, cơ quan đăng ký cư trú có trách nhiệm cập nhật thông tin về thời hạn tạm trú mới của người đăng ký vào Cơ sở dữ liệu về cư trú và thông báo cho người đăng ký về việc đã cập nhật thông tin đăng ký tạm trú; trường hợp từ chối đăng ký thì phải trả lời bằng văn bản và nêu rõ lý do.” [3].

- Luat-68-2020-QH14-doi-chieu-20261003 — Điều 28. Hồ sơ, thủ tục đăng ký tạm trú, gia hạn tạm trú | Khoản 1: “1. Hồ sơ đăng ký tạm trú bao gồm: a) Tờ khai thay đổi thông tin cư trú; đối với người đăng ký tạm trú là người chưa thành niên thì trong tờ khai phải ghi rõ ý kiến đồng ý của cha, mẹ hoặc người giám hộ, trừ trường hợp đã có ý kiến đồng ý bằng văn bản;” [2].

Đây là câu trả lời một phần từ nguồn; chưa kết luận cách áp dụng cho tình huống riêng của bạn. Cần đối chiếu điều kiện, hiệu lực và bản gốc.

#### B — Gemini phân tích + Qwen trích nguồn

Các đoạn trả lời trực tiếp trong nguồn:

- Luat-68-2020-QH14-doi-chieu-20261003 — Điều 28. Hồ sơ, thủ tục đăng ký tạm trú, gia hạn tạm trú | Khoản 1: “1. Hồ sơ đăng ký tạm trú bao gồm:

1. Hồ sơ đăng ký tạm trú bao gồm: a) Tờ khai thay đổi thông tin cư trú; đối với người đăng ký tạm trú là người chưa thành niên thì trong tờ khai phải ghi rõ ý kiến đồng ý của cha, mẹ hoặc người giám hộ, trừ trường hợp đã có ý kiến đồng ý bằng văn bản;

1. Hồ sơ đăng ký tạm trú bao gồm: b) Giấy tờ, tài liệu chứng minh chỗ ở hợp pháp.” [2].

- Luat-68-2020-QH14-doi-chieu-20261003 — Điều 28. Hồ sơ, thủ tục đăng ký tạm trú, gia hạn tạm trú | Khoản 2: “2. Người đăng ký tạm trú nộp hồ sơ đăng ký tạm trú đến cơ quan đăng ký cư trú nơi mình dự kiến tạm trú.

Khi tiếp nhận hồ sơ đăng ký tạm trú, cơ quan đăng ký cư trú kiểm tra và cấp phiếu tiếp nhận hồ sơ cho người đăng ký; trường hợp hồ sơ chưa đầy đủ thì hướng dẫn người đăng ký bổ sung hồ sơ.

Trong thời hạn 03 ngày làm việc kể từ ngày nhận được hồ sơ đầy đủ và hợp lệ, cơ quan đăng ký cư trú có trách nhiệm thẩm định, cập nhật thông tin về nơi tạm trú mới, thời hạn tạm trú của người đăng ký vào Cơ sở dữ liệu về cư trú và thông báo cho người đăng ký về việc đã cập nhật thông tin đăng ký tạm trú; trường hợp từ chối đăng ký thì phải trả lời bằng văn bản và nêu rõ lý do.” [3].

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng, hiệu lực và bản gốc.

#### C — Đáp án bạn gửi

- Khi chuyển sang chỗ ở trọ mới ngoài xã/phường cũ: Trong thời hạn 30 ngày, bạn phải làm thủ tục **đăng ký tạm trú tại chỗ ở mới**. Khi công an xã/phường mới duyệt tạm trú, hệ thống Cơ sở dữ liệu quốc gia về dân cư sẽ **tự động xóa đăng ký tạm trú tại nơi ở cũ**.
- Nếu chuyển trọ cùng xã/phường nhưng đổi địa chỉ: Làm thủ tục điều chỉnh thông tin về cư trú trên Cổng dịch vụ công/VNeID.

#### D — Chatbot dạng agent

Khi chuyển sang nơi ở mới, bạn cần nộp hồ sơ đăng ký tạm trú đến cơ quan đăng ký cư trú nơi dự kiến tạm trú để được cập nhật thông tin vào Cơ sở dữ liệu về cư trú [3].

- Chuẩn bị tờ khai thay đổi thông tin cư trú và giấy tờ, tài liệu chứng minh chỗ ở hợp pháp theo quy định [2].
- Nộp hồ sơ đăng ký tạm trú đến cơ quan đăng ký cư trú nơi bạn dự kiến tạm trú và nhận phiếu tiếp nhận hồ sơ [3].
- Bổ sung hồ sơ theo hướng dẫn của cơ quan đăng ký cư trú nếu hồ sơ nộp vào chưa đầy đủ [3].
- Chờ cơ quan đăng ký cư trú thẩm định và nhận thông báo về việc đã cập nhật thông tin đăng ký tạm trú trong thời hạn 03 ngày làm việc kể từ ngày nhận đủ hồ sơ hợp lệ [3].

Trường hợp người đăng ký tạm trú là người chưa thành niên thì trong tờ khai phải ghi rõ ý kiến đồng ý của cha, mẹ hoặc người giám hộ, trừ khi đã có ý kiến đồng ý bằng văn bản [2].
Nếu từ chối giải quyết đăng ký tạm trú, cơ quan đăng ký cư trú phải trả lời bằng văn bản và nêu rõ lý do cho người nộp hồ sơ [3].

Để áp dụng vào trường hợp của bạn:
- Bạn đã đủ 18 tuổi hay còn là người chưa thành niên?
- Bạn đã có hợp đồng thuê nhà hoặc giấy tờ chứng minh chỗ ở hợp pháp tại phòng trọ mới chưa?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

Nguồn truy xuất của D (rank dùng trong trích dẫn):

- [1] Luat-68-2020-QH14-doi-chieu-20261003 — Điều 27. Điều kiện đăng ký tạm trú | Khoản 3
- [2] Luat-68-2020-QH14-doi-chieu-20261003 — Điều 28. Hồ sơ, thủ tục đăng ký tạm trú, gia hạn tạm trú | Khoản 1
- [3] Luat-68-2020-QH14-doi-chieu-20261003 — Điều 28. Hồ sơ, thủ tục đăng ký tạm trú, gia hạn tạm trú | Khoản 2

### Câu 17: Khi xem phòng trọ, tôi nên kiểm tra những điều kiện phòng cháy, chữa cháy nào?

#### A — Gemini chatbot

Căn cứ theo văn bản Luat-55-2024-QH15-dieu-8-20-21-23-24, khi xem phòng trọ, bạn có thể tham khảo các điều kiện sau:

* Khuyến nghị: nên kiểm tra lối thoát nạn, lối ra khẩn cấp hoặc lối đi bảo đảm việc thoát nạn, cùng với phương tiện phòng cháy, chữa cháy phù hợp với điều kiện thực tế theo nguồn [1], Điều 20 Khoản 2, trang 1.
* Khuyến nghị: nên kiểm tra an toàn điện, khu vực bếp đun nấu và khoảng cách an toàn, không để vật, chất dễ cháy, nổ gần nguồn lửa, nguồn nhiệt theo nguồn [2], Điều 20 Khoản 1, trang 1.
* Nếu là nhà ở kết hợp kinh doanh hàng nguy hiểm cháy, nổ, khuyến nghị: nên kiểm tra việc không bố trí chỗ ngủ tại khu vực kinh doanh, có phương tiện báo cháy/thông gió và lối thoát nạn khu vực ở phải được ngăn cháy theo nguồn [3], Điều 21 Khoản 2, trang 1.

*Lưu ý: Đây là thông tin tham khảo, không thay thế tư vấn pháp lý chuyên nghiệp.*

#### B — Gemini phân tích + Qwen trích nguồn

Các đoạn trả lời trực tiếp trong nguồn:

- Luat-55-2024-QH15-dieu-8-20-21-23-24 — Điều 20. Phòng cháy đối với nhà ở | Khoản 1: “1. Nhà ở không thuộc loại hình quy định tại khoản 3 và khoản 4 Điều này phải bảo đảm các điều kiện an toàn về phòng cháy sau đây:

1. Nhà ở không thuộc loại hình quy định tại khoản 3 và khoản 4 Điều này phải bảo đảm các điều kiện an toàn về phòng cháy sau đây: a) Lắp đặt, sử dụng thiết bị điện bảo đảm điều kiện an toàn về phòng cháy quy định tại điểm c khoản 1 Điều 24 của Luật này;

1. Nhà ở không thuộc loại hình quy định tại khoản 3 và khoản 4 Điều này phải bảo đảm các điều kiện an toàn về phòng cháy sau đây: b) Bố trí bếp đun nấu, nơi thờ cúng, đốt vàng mã bảo đảm an toàn; không để vật, chất dễ cháy, nổ gần nguồn lửa, nguồn nhiệt.” [1].

- Luat-55-2024-QH15-dieu-8-20-21-23-24 — Điều 20. Phòng cháy đối với nhà ở | Khoản 2: “2. Nhà ở không thuộc loại hình quy định tại khoản 3 và khoản 4 Điều này phải bảo đảm các điều kiện về chữa cháy, thoát nạn sau đây:

2. Nhà ở không thuộc loại hình quy định tại khoản 3 và khoản 4 Điều này phải bảo đảm các điều kiện về chữa cháy, thoát nạn sau đây: a) Có phương tiện phòng cháy, chữa cháy phù hợp với khả năng, điều kiện thực tế để sẵn sàng chữa cháy, thoát nạn;

2. Nhà ở không thuộc loại hình quy định tại khoản 3 và khoản 4 Điều này phải bảo đảm các điều kiện về chữa cháy, thoát nạn sau đây: b) Bố trí, duy trì lối thoát nạn, lối ra khẩn cấp hoặc lối đi bảo đảm việc thoát nạn.” [2].

- Luat-55-2024-QH15-dieu-8-20-21-23-24 — Điều 21. Phòng cháy đối với nhà ở kết hợp sản xuất, kinh doanh | Khoản 2: “2. Nhà ở kết hợp sản xuất, kinh doanh hàng hóa nguy hiểm về cháy, nổ phải bảo đảm các điều kiện an toàn về phòng cháy sau đây:

2. Nhà ở kết hợp sản xuất, kinh doanh hàng hóa nguy hiểm về cháy, nổ phải bảo đảm các điều kiện an toàn về phòng cháy sau đây: a) Các điều kiện an toàn về phòng cháy quy định tại khoản 1 Điều này;

2. Nhà ở kết hợp sản xuất, kinh doanh hàng hóa nguy hiểm về cháy, nổ phải bảo đảm các điều kiện an toàn về phòng cháy sau đây: b) Không bố trí chỗ ngủ trong khu vực sản xuất, kinh doanh;

2. Nhà ở kết hợp sản xuất, kinh doanh hàng hóa nguy hiểm về cháy, nổ phải bảo đảm các điều kiện an toàn về phòng cháy sau đây: c) Có phương tiện báo cháy, giải pháp thông gió, thiết bị phát hiện sự cố rò rỉ chất khí nguy hiểm về cháy, nổ phù hợp với công năng, đặc điểm của nhà ở kết hợp sản xuất, kinh doanh hàng hóa nguy hiểm về cháy, nổ;

2. Nhà ở kết hợp sản xuất, kinh doanh hàng hóa nguy hiểm về cháy, nổ phải bảo đảm các điều kiện an toàn về phòng cháy sau đây: d) Khu vực sản xuất, kinh doanh hàng hóa nguy hiểm về cháy, nổ phải được ngăn cháy với lối thoát nạn của khu vực để ở.” [3].

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng, hiệu lực và bản gốc.

#### C — Đáp án bạn gửi

Khi đi xem phòng, sinh viên cần quan sát trực tiếp 5 yếu tố sinh mạng sau:
1. **Lối thoát hiểm thứ hai:** Ngoài cửa chính đi vào, phòng hoặc tầng trọ có ban công, lối lên mái thông sang nhà bên cạnh, hoặc thang thoát hiểm bên ngoài không?
2. **Chuồng cọp / Rào sắt lồng bảo vệ:** Nếu ban công bị rào chắn (chuồng cọp), bắt buộc phải có **cửa mở thoát hiểm khẩn cấp** và chìa khóa treo ngay cạnh cửa.
3. **Thiết bị PCCC tại chỗ:** Hành lang có trang bị **bình chữa cháy xách tay** (bình bột ABC hoặc khí CO2) còn nguyên chốt kẹp chì, đồng hồ áp suất vạch xanh hay không.
4. **Hệ thống điện:** Đường dây điện có được đi trong ống gen bảo vệ không? Có aptomat (CB) riêng tự ngắt khi chập điện không?
5. **Khu vực để xe:** Chỗ để xe máy/xe đạp điện có lối đi thông thoáng không, hay bị bít kín chắn ngang cửa thoát nạn chính?

#### D — Chatbot dạng agent

Các đoạn trả lời trực tiếp trong nguồn:

- Luat-55-2024-QH15-dieu-8-20-21-23-24 — Điều 20. Phòng cháy đối với nhà ở | Khoản 2: “2. Nhà ở không thuộc loại hình quy định tại khoản 3 và khoản 4 Điều này phải bảo đảm các điều kiện về chữa cháy, thoát nạn sau đây:

2. Nhà ở không thuộc loại hình quy định tại khoản 3 và khoản 4 Điều này phải bảo đảm các điều kiện về chữa cháy, thoát nạn sau đây: a) Có phương tiện phòng cháy, chữa cháy phù hợp với khả năng, điều kiện thực tế để sẵn sàng chữa cháy, thoát nạn;

2. Nhà ở không thuộc loại hình quy định tại khoản 3 và khoản 4 Điều này phải bảo đảm các điều kiện về chữa cháy, thoát nạn sau đây: b) Bố trí, duy trì lối thoát nạn, lối ra khẩn cấp hoặc lối đi bảo đảm việc thoát nạn.” [1].

- Luat-55-2024-QH15-dieu-8-20-21-23-24 — Điều 20. Phòng cháy đối với nhà ở | Khoản 1: “1. Nhà ở không thuộc loại hình quy định tại khoản 3 và khoản 4 Điều này phải bảo đảm các điều kiện an toàn về phòng cháy sau đây:

1. Nhà ở không thuộc loại hình quy định tại khoản 3 và khoản 4 Điều này phải bảo đảm các điều kiện an toàn về phòng cháy sau đây: a) Lắp đặt, sử dụng thiết bị điện bảo đảm điều kiện an toàn về phòng cháy quy định tại điểm c khoản 1 Điều 24 của Luật này;

1. Nhà ở không thuộc loại hình quy định tại khoản 3 và khoản 4 Điều này phải bảo đảm các điều kiện an toàn về phòng cháy sau đây: b) Bố trí bếp đun nấu, nơi thờ cúng, đốt vàng mã bảo đảm an toàn; không để vật, chất dễ cháy, nổ gần nguồn lửa, nguồn nhiệt.” [2].

- Luat-55-2024-QH15-dieu-8-20-21-23-24 — Điều 21. Phòng cháy đối với nhà ở kết hợp sản xuất, kinh doanh | Khoản 2: “2. Nhà ở kết hợp sản xuất, kinh doanh hàng hóa nguy hiểm về cháy, nổ phải bảo đảm các điều kiện an toàn về phòng cháy sau đây:

2. Nhà ở kết hợp sản xuất, kinh doanh hàng hóa nguy hiểm về cháy, nổ phải bảo đảm các điều kiện an toàn về phòng cháy sau đây: a) Các điều kiện an toàn về phòng cháy quy định tại khoản 1 Điều này;

2. Nhà ở kết hợp sản xuất, kinh doanh hàng hóa nguy hiểm về cháy, nổ phải bảo đảm các điều kiện an toàn về phòng cháy sau đây: b) Không bố trí chỗ ngủ trong khu vực sản xuất, kinh doanh;

2. Nhà ở kết hợp sản xuất, kinh doanh hàng hóa nguy hiểm về cháy, nổ phải bảo đảm các điều kiện an toàn về phòng cháy sau đây: c) Có phương tiện báo cháy, giải pháp thông gió, thiết bị phát hiện sự cố rò rỉ chất khí nguy hiểm về cháy, nổ phù hợp với công năng, đặc điểm của nhà ở kết hợp sản xuất, kinh doanh hàng hóa nguy hiểm về cháy, nổ;

2. Nhà ở kết hợp sản xuất, kinh doanh hàng hóa nguy hiểm về cháy, nổ phải bảo đảm các điều kiện an toàn về phòng cháy sau đây: d) Khu vực sản xuất, kinh doanh hàng hóa nguy hiểm về cháy, nổ phải được ngăn cháy với lối thoát nạn của khu vực để ở.” [3].

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng, hiệu lực và bản gốc.

Nguồn truy xuất của D (rank dùng trong trích dẫn):

- [1] Luat-55-2024-QH15-dieu-8-20-21-23-24 — Điều 20. Phòng cháy đối với nhà ở | Khoản 2
- [2] Luat-55-2024-QH15-dieu-8-20-21-23-24 — Điều 20. Phòng cháy đối với nhà ở | Khoản 1
- [3] Luat-55-2024-QH15-dieu-8-20-21-23-24 — Điều 21. Phòng cháy đối với nhà ở kết hợp sản xuất, kinh doanh | Khoản 2

Lý do giới hạn/fallback của D:

- Số khoản được khẳng định không khớp khoản của nguồn trích dẫn.
- Bản tổng hợp chưa được nguồn xác nhận sau lần sửa; dùng trích đoạn Qwen đã chọn.

### Câu 18: Nhà trọ có nhiều phòng cần đáp ứng những yêu cầu an toàn cháy nổ nào?

#### A — Gemini chatbot

Dựa trên các tài liệu được cung cấp, yêu cầu an toàn phòng cháy đối với nhà ở được quy định như sau:

* Chưa tìm thấy căn cứ riêng biệt trong context quy định trực tiếp cho mô hình "nhà trọ có nhiều phòng"; các quy định hiện có áp dụng chung cho nhà ở không thuộc loại hình tại khoản 3 và khoản 4 Điều 20 [1], [2].
* Nhà ở phải bảo đảm lắp đặt, sử dụng thiết bị điện an toàn; bố trí bếp đun nấu, nơi thờ cúng an toàn, không để vật, chất dễ cháy gần nguồn lửa, nhiệt (nguồn [1], Điều 20 khoản 1, trang 1).
* Nhà ở phải có phương tiện phòng cháy, chữa cháy phù hợp với điều kiện thực tế và bố trí, duy trì lối thoát nạn, lối ra khẩn cấp bảo đảm việc thoát nạn (nguồn [2], Điều 20 khoản 2, trang 1).

*Thông tin mang tính chất tham khảo, không thay thế tư vấn pháp lý chuyên nghiệp.*

#### B — Gemini phân tích + Qwen trích nguồn

Các đoạn trả lời trực tiếp trong nguồn:

- Luat-55-2024-QH15-dieu-8-20-21-23-24 — Điều 20. Phòng cháy đối với nhà ở | Khoản 1: “1. Nhà ở không thuộc loại hình quy định tại khoản 3 và khoản 4 Điều này phải bảo đảm các điều kiện an toàn về phòng cháy sau đây:

1. Nhà ở không thuộc loại hình quy định tại khoản 3 và khoản 4 Điều này phải bảo đảm các điều kiện an toàn về phòng cháy sau đây: a) Lắp đặt, sử dụng thiết bị điện bảo đảm điều kiện an toàn về phòng cháy quy định tại điểm c khoản 1 Điều 24 của Luật này;

1. Nhà ở không thuộc loại hình quy định tại khoản 3 và khoản 4 Điều này phải bảo đảm các điều kiện an toàn về phòng cháy sau đây: b) Bố trí bếp đun nấu, nơi thờ cúng, đốt vàng mã bảo đảm an toàn; không để vật, chất dễ cháy, nổ gần nguồn lửa, nguồn nhiệt.” [1].

- Luat-55-2024-QH15-dieu-8-20-21-23-24 — Điều 20. Phòng cháy đối với nhà ở | Khoản 2: “2. Nhà ở không thuộc loại hình quy định tại khoản 3 và khoản 4 Điều này phải bảo đảm các điều kiện về chữa cháy, thoát nạn sau đây:

2. Nhà ở không thuộc loại hình quy định tại khoản 3 và khoản 4 Điều này phải bảo đảm các điều kiện về chữa cháy, thoát nạn sau đây: a) Có phương tiện phòng cháy, chữa cháy phù hợp với khả năng, điều kiện thực tế để sẵn sàng chữa cháy, thoát nạn;

2. Nhà ở không thuộc loại hình quy định tại khoản 3 và khoản 4 Điều này phải bảo đảm các điều kiện về chữa cháy, thoát nạn sau đây: b) Bố trí, duy trì lối thoát nạn, lối ra khẩn cấp hoặc lối đi bảo đảm việc thoát nạn.” [2].

- Luat-55-2024-QH15-dieu-8-20-21-23-24 — Điều 21. Phòng cháy đối với nhà ở kết hợp sản xuất, kinh doanh | Khoản 2: “2. Nhà ở kết hợp sản xuất, kinh doanh hàng hóa nguy hiểm về cháy, nổ phải bảo đảm các điều kiện an toàn về phòng cháy sau đây:

2. Nhà ở kết hợp sản xuất, kinh doanh hàng hóa nguy hiểm về cháy, nổ phải bảo đảm các điều kiện an toàn về phòng cháy sau đây: a) Các điều kiện an toàn về phòng cháy quy định tại khoản 1 Điều này;

2. Nhà ở kết hợp sản xuất, kinh doanh hàng hóa nguy hiểm về cháy, nổ phải bảo đảm các điều kiện an toàn về phòng cháy sau đây: b) Không bố trí chỗ ngủ trong khu vực sản xuất, kinh doanh;

2. Nhà ở kết hợp sản xuất, kinh doanh hàng hóa nguy hiểm về cháy, nổ phải bảo đảm các điều kiện an toàn về phòng cháy sau đây: c) Có phương tiện báo cháy, giải pháp thông gió, thiết bị phát hiện sự cố rò rỉ chất khí nguy hiểm về cháy, nổ phù hợp với công năng, đặc điểm của nhà ở kết hợp sản xuất, kinh doanh hàng hóa nguy hiểm về cháy, nổ;

2. Nhà ở kết hợp sản xuất, kinh doanh hàng hóa nguy hiểm về cháy, nổ phải bảo đảm các điều kiện an toàn về phòng cháy sau đây: d) Khu vực sản xuất, kinh doanh hàng hóa nguy hiểm về cháy, nổ phải được ngăn cháy với lối thoát nạn của khu vực để ở.” [3].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng; cần đối chiếu phần còn thiếu.

Cần xác định loại hình sử dụng, số tầng, diện tích và quy chuẩn của nhà trọ để chọn đúng nhóm điều kiện; chưa kết luận chỉ từ số phòng.

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng, hiệu lực và bản gốc.

#### C — Đáp án bạn gửi

Theo quy định tại Nghị định 136/2020/NĐ-CP, Nghị định 50/2024/NĐ-CP và Chỉ thị 19/CT-TTg (2024):
- Nhà trọ phải có **nội quy, tiêu lệnh PCCC**, biển chỉ dẫn thoát nạn (đèn Exit/đèn sự cố nếu quy mô từ nhiều tầng trở lên).
- Phải bố trí giải pháp **ngăn cháy lan** giữa khu vực để xe máy/xe điện với khu vực phòng ở và cầu thang bộ thoát hiểm.
- Có tối thiểu **2 lối thoát nạn độc lập**; không để đồ đạc, hàng quán lấn chiếm hành lang và cầu thang.
- Đảm bảo đủ số lượng bình chữa cháy xách tay (bình quân 1 bình/50–100 m² sàn, mỗi tầng tối thiểu 2 bình).
- Người quản lý/chủ nhà trọ phải được tập huấn nghiệp vụ PCCC.

#### D — Chatbot dạng agent

Nguồn trích dẫn chưa đủ căn cứ quy định riêng cho nhà trọ nhiều phòng mà chỉ nêu điều kiện an toàn cháy nổ cho nhà ở nói chung và nhà ở kết hợp sản xuất kinh doanh hàng hóa nguy hiểm về cháy nổ [1] [2] [3].

- Lắp đặt, sử dụng thiết bị điện bảo đảm an toàn phòng cháy và bố trí nơi đun nấu, thờ cúng an toàn, không để chất dễ cháy gần nguồn lửa hoặc nguồn nhiệt [1].
- Trang bị phương tiện phòng cháy, chữa cháy phù hợp với điều kiện thực tế để sẵn sàng ứng phó [2].
- Bố trí và duy trì lối thoát nạn, lối ra khẩn cấp hoặc lối đi bảo đảm yêu cầu thoát hiểm [2].
- Trường hợp nhà ở kết hợp kinh doanh hàng hóa nguy hiểm cháy nổ, phải bảo đảm không bố trí chỗ ngủ tại khu vực kinh doanh và ngăn cháy khu vực này với lối thoát hiểm của khu để ở [3].
- Trang bị phương tiện báo cháy, giải pháp thông gió và thiết bị phát hiện rò rỉ khí nguy hiểm cháy nổ phù hợp nếu thuộc loại hình nhà ở kết hợp kinh doanh hàng nguy hiểm cháy nổ [3].

Nguồn tài liệu chưa cung cấp quy định chi tiết theo quy mô số tầng, diện tích hoặc tính chất kinh doanh dịch vụ lưu trú riêng của nhà trọ [1] [2] [3].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng.
Cần xác định loại hình sử dụng, số tầng, diện tích và quy chuẩn của nhà trọ để chọn đúng nhóm điều kiện; chưa kết luận chỉ từ số phòng.

Để áp dụng vào trường hợp của bạn:
- Nhà trọ của bạn có kết hợp hoạt động sản xuất, kinh doanh hàng hóa nguy hiểm về cháy nổ không?
- Quy mô nhà trọ gồm bao nhiêu tầng và tổng diện tích sàn là bao nhiêu?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

Nguồn truy xuất của D (rank dùng trong trích dẫn):

- [1] Luat-55-2024-QH15-dieu-8-20-21-23-24 — Điều 20. Phòng cháy đối với nhà ở | Khoản 1
- [2] Luat-55-2024-QH15-dieu-8-20-21-23-24 — Điều 20. Phòng cháy đối với nhà ở | Khoản 2
- [3] Luat-55-2024-QH15-dieu-8-20-21-23-24 — Điều 21. Phòng cháy đối với nhà ở kết hợp sản xuất, kinh doanh | Khoản 2

Lý do giới hạn/fallback của D:

- Phản hồi chưa đáp ứng đầy đủ yêu cầu chính; đánh dấu theo nội dung thay vì provider.

### Câu 19: Nếu lối thoát nạn bị khóa hoặc bị chặn, người thuê nên làm gì?

#### A — Gemini chatbot

Các căn cứ liên quan tìm được trong kho (trích nguyên đoạn):

- Luat-55-2024-QH15-dieu-8-20-21-23-24 — Điều 20. Phòng cháy đối với nhà ở | Khoản 2: “2. Nhà ở không thuộc loại hình quy định tại khoản 3 và khoản 4 Điều này phải bảo đảm các điều kiện về chữa cháy, thoát nạn sau đây: b) Bố trí, duy trì lối thoát nạn, lối ra khẩn cấp hoặc lối đi bảo đảm việc thoát nạn.” [1].

- Nghị-định-105-2025-NĐ-CP — Điều 13. Nội dung, thẩm quyền kiểm tra về phòng cháy, chữa cháy | Khoản 1: “1. Nội dung kiểm tra về phòng cháy, chữa cháy theo quy định tại khoản 2 Điều 11 Luật Phòng cháy, chữa cháy và cứu nạn, cứu hộ trong việc: o) Duy trì lối thoát nạn, lối ra khẩn cấp hoặc lối đi bảo đảm việc thoát nạn;” [2].

Đây là câu trả lời một phần từ nguồn; chưa kết luận cách áp dụng cho tình huống riêng của bạn. Cần đối chiếu điều kiện, hiệu lực và bản gốc.

#### B — Gemini phân tích + Qwen trích nguồn

Các đoạn trả lời trực tiếp trong nguồn:

- Nghị-định-105-2025-NĐ-CP — Điều 13. Nội dung, thẩm quyền kiểm tra về phòng cháy, chữa cháy | Khoản 1: “1. Nội dung kiểm tra về phòng cháy, chữa cháy theo quy định tại khoản 2 Điều 11 Luật Phòng cháy, chữa cháy và cứu nạn, cứu hộ trong việc:

1. Nội dung kiểm tra về phòng cháy, chữa cháy theo quy định tại khoản 2 Điều 11 Luật Phòng cháy, chữa cháy và cứu nạn, cứu hộ trong việc: a) Thực hiện trách nhiệm phòng cháy, chữa cháy, cứu nạn, cứu hộ của người đứng đầu cơ sở bao gồm: trách nhiệm trong việc thực hiện quy định tại các điểm a, b, c, đ, e, g và điểm h khoản 3 Điều 8 Luật Phòng cháy, chữa cháy và cứu nạn, cứu hộ; tổ chức thực hiện, kiểm tra, đôn đốc, giám sát cơ quan, tổ chức, cá nhân thuộc phạm vi quản lý về việc thực hiện quy định, nội quy, biện pháp, yêu cầu về phòng cháy, chữa cháy, cứu nạn, cứu hộ;

1. Nội dung kiểm tra về phòng cháy, chữa cháy theo quy định tại khoản 2 Điều 11 Luật Phòng cháy, chữa cháy và cứu nạn, cứu hộ trong việc: c) Trang bị phương tiện, hệ thống phòng cháy, chữa cháy, cứu nạn, cứu hộ, hệ thống điện phục vụ phòng cháy và chữa cháy, nguồn nước chữa cháy theo quy định;

1. Nội dung kiểm tra về phòng cháy, chữa cháy theo quy định tại khoản 2 Điều 11 Luật Phòng cháy, chữa cháy và cứu nạn, cứu hộ trong việc: d) Duy trì hoạt động các phương tiện, hệ thống phòng cháy, chữa cháy, cứu nạn, cứu hộ, hệ thống điện phục vụ phòng cháy và chữa cháy; nguồn nước chữa cháy;

1. Nội dung kiểm tra về phòng cháy, chữa cháy theo quy định tại khoản 2 Điều 11 Luật Phòng cháy, chữa cháy và cứu nạn, cứu hộ trong việc: e) Duy trì điều kiện an toàn phòng cháy trong sử dụng nguồn lửa, nguồn nhiệt, thiết bị, dụng cụ sinh lửa, sinh nhiệt, chất dễ cháy, nổ;

1. Nội dung kiểm tra về phòng cháy, chữa cháy theo quy định tại khoản 2 Điều 11 Luật Phòng cháy, chữa cháy và cứu nạn, cứu hộ trong việc: h) Duy trì giải pháp thoát nạn, ngăn cháy, chống cháy lan, chống khói;

1. Nội dung kiểm tra về phòng cháy, chữa cháy theo quy định tại khoản 2 Điều 11 Luật Phòng cháy, chữa cháy và cứu nạn, cứu hộ trong việc: l) Chấp hành nội quy phòng cháy, chữa cháy, cứu nạn, cứu hộ;

1. Nội dung kiểm tra về phòng cháy, chữa cháy theo quy định tại khoản 2 Điều 11 Luật Phòng cháy, chữa cháy và cứu nạn, cứu hộ trong việc: m) Duy trì các biển cấm, biển báo, biển chỉ dẫn;

1. Nội dung kiểm tra về phòng cháy, chữa cháy theo quy định tại khoản 2 Điều 11 Luật Phòng cháy, chữa cháy và cứu nạn, cứu hộ trong việc: n) Thực hiện trách nhiệm phòng cháy, chữa cháy, cứu nạn, cứu hộ của chủ hộ gia đình trực tiếp sử dụng nhà ở, người thuê, mượn, ở nhờ nhà ở theo quy định tại khoản 6 và khoản 8 Điều 8 Luật Phòng cháy, chữa cháy và cứu nạn, cứu hộ;

1. Nội dung kiểm tra về phòng cháy, chữa cháy theo quy định tại khoản 2 Điều 11 Luật Phòng cháy, chữa cháy và cứu nạn, cứu hộ trong việc: o) Duy trì lối thoát nạn, lối ra khẩn cấp hoặc lối đi bảo đảm việc thoát nạn;” [2].

- Nghị-định-105-2025-NĐ-CP — Điều 13. Nội dung, thẩm quyền kiểm tra về phòng cháy, chữa cháy | Khoản 2: “2. Thẩm quyền kiểm tra:

2. Thẩm quyền kiểm tra: a) Cơ quan Công an theo phân cấp tổ chức kiểm tra: Kiểm tra định kỳ 01 năm một lần đối với cơ sở thuộc nhóm 1 quy định tại Phụ lục II kèm theo Nghị định này, công trình xây dựng trong quá trình thi công thuộc diện phải thẩm duyệt thiết kế, thẩm định thiết kế về phòng cháy và chữa cháy, phương tiện giao thông quy định tại Phụ lục III kèm theo Nghị định này; kiểm tra định kỳ 02 năm một lần đối với cơ sở thuộc nhóm 2 quy định tại Phụ lục II kèm theo Nghị định này. Kiểm tra đột xuất khi có dấu hiệu vi phạm pháp luật, có đơn khiếu nại, tố cáo về vi phạm pháp luật liên quan đến phòng cháy, chữa cháy theo quy định hoặc theo yêu cầu phục vụ bảo đảm an ninh, trật tự của cơ quan có thẩm quyền đối với cơ sở quy định tại Phụ lục II kèm theo Nghị định này và phương tiện giao thông quy định tại Phụ lục III kèm theo Nghị định này. Nội dung kiểm tra định kỳ, đột xuất: đối với cơ sở theo quy định tại các điểm a, c, d và điểm đ khoản 1 Điều này; đối với công trình xây dựng trong quá trình thi công thuộc diện phải thẩm duyệt thiết kế, thẩm định thiết kế về phòng cháy và chữa cháy theo quy định tại các điểm c, d, l và điểm m khoản 1 Điều này; đối với phương tiện giao thông quy định tại Phụ lục III kèm theo Nghị định này theo quy định tại các điểm b, c, d, l và điểm m khoản 1 Điều này;

2. Thẩm quyền kiểm tra: b) Ủy ban nhân dân cấp tỉnh phân công, phân cấp cơ quan chuyên môn về xây dựng tổ chức kiểm tra: Kiểm tra định kỳ 01 năm một lần đối với cơ sở thuộc nhóm 1 quy định tại Phụ lục II kèm theo Nghị định này, 02 năm một lần đối với cơ sở thuộc nhóm 2 quy định tại Phụ lục II kèm theo Nghị định này. Kiểm tra đột xuất khi có dấu hiệu vi phạm pháp luật, có đơn khiếu nại, tố cáo về vi phạm pháp luật liên quan đến phòng cháy, chữa cháy và cứu nạn, cứu hộ theo quy định hoặc khi có yêu cầu phối hợp để phục vụ bảo đảm an ninh, trật tự của cơ quan có thẩm quyền đối với cơ sở thuộc Phụ lục II kèm theo Nghị định này. Nội dung kiểm tra định kỳ, đột xuất theo quy định tại điểm g và điểm h khoản 1 Điều này;

2. Thẩm quyền kiểm tra: c) Ủy ban nhân dân cấp xã tổ chức kiểm tra:

Kiểm tra định kỳ 03 năm một lần đối với cơ sở thuộc Phụ lục I, trừ cơ sở có nguy hiểm về cháy, nổ quy định tại Phụ lục II kèm theo Nghị định này.

Kiểm tra đột xuất khi có dấu hiệu vi phạm pháp luật, có đơn khiếu nại, tố cáo về vi phạm pháp luật liên quan đến phòng cháy, chữa cháy và cứu nạn, cứu hộ theo quy định hoặc theo yêu cầu phục vụ bảo đảm an ninh, trật tự của cơ quan có thẩm quyền đối với: nhà ở, nhà ở kết hợp sản xuất, kinh doanh; cơ sở thuộc Phụ lục I, trừ cơ sở có nguy hiểm về cháy, nổ quy định tại Phụ lục II kèm theo Nghị định này.

Nội dung kiểm tra định kỳ, đột xuất theo quy định tại các điểm a, c, d, đ, g, h và điểm n khoản 1 Điều này;

2. Thẩm quyền kiểm tra: đ) Người đứng đầu cơ sở tự tổ chức kiểm tra thường xuyên, định kỳ đối với cơ sở thuộc phạm vi quản lý. Nội dung kiểm tra thường xuyên theo quy định tại các điểm d, e, h và điểm l khoản 1 Điều này; nội dung kiểm tra định kỳ theo quy định tại các điểm c, d, đ, e, g, h, l và điểm m khoản 1 Điều này;

2. Thẩm quyền kiểm tra: h) Chủ hộ gia đình trực tiếp sử dụng nhà ở, người thuê, mượn, ở nhờ nhà ở tự tổ chức kiểm tra thường xuyên đối với nhà ở thuộc phạm vi quản lý. Nội dung kiểm tra theo quy định tại điểm c và điểm d về trang bị phương tiện, duy trì hoạt động của phương tiện phòng cháy, chữa cháy, cứu nạn, cứu hộ và quy định tại điểm e và điểm o khoản 1 Điều này.

Đối với nhà ở thuộc trường hợp quy định tại khoản 5 Điều 20 Luật Phòng cháy, chữa cháy và cứu nạn, cứu hộ, ngoài kiểm tra các nội dung quy định nêu trên thì còn phải kiểm tra việc duy trì hoạt động của thiết bị truyền tin báo cháy kết nối với hệ thống Cơ sở dữ liệu về phòng cháy, chữa cháy, cứu nạn, cứu hộ và truyền tin báo cháy;” [3].

- Nghị-định-105-2025-NĐ-CP — Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp: “Điều 45. Hiệu lực thi hành
Điều 45. Hiệu lực thi hành

Điều 45. Hiệu lực thi hành | Khoản 1
1. Nghị định này có hiệu lực thi hành từ ngày 01 tháng 7 năm 2025.

Điều 46. Quy định chuyển tiếp
Điều 46. Quy định chuyển tiếp

Ghi chú tuyển chọn: Chỉ giữ khoản 6 mới về cơ sở hoạt động trước 01/07/2025; được bổ sung tại Điều 29 khoản 2 Nghị định 347/2026/NĐ-CP. Bản PDF nguồn ghi “Nghị này” ở cuối câu, giữ nguyên cách ghi của nguồn.

Điều 46. Quy định chuyển tiếp | Khoản 6
6. Đối với cơ sở được xây dựng và hoạt động trước ngày 01 tháng 7 năm 2025 đã được quản lý về phòng cháy, chữa cháy, cứu nạn, cứu hộ theo quy định tại Nghị định số 136/2020/NĐ-CP, Nghị định số 50/2024/NĐ-CP và thuộc danh mục quy định tại Phụ lục I kèm theo Nghị định này, tiếp tục thực hiện việc quản lý, kiểm tra về phòng cháy, chữa cháy đối với cơ sở theo quy định tại Điều 13 và Điều 14 Nghị này.” [4].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng; cần đối chiếu phần còn thiếu.

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng, hiệu lực và bản gốc.

#### C — Đáp án bạn gửi

1. **Yêu cầu chủ nhà giải phóng ngay chướng ngại vật:** Góp ý trực tiếp hoặc nhắn tin vào nhóm trọ yêu cầu dọn dẹp xe cộ, đồ đạc chắn lối đi/cầu thang và mở cửa thoát hiểm ban công/sân thượng.
2. **Chìa khóa khẩn cấp:** Đề nghị chủ trọ cung cấp chìa khóa hoặc đặt hộp chứa chìa khóa thoát hiểm đập kính tại cửa thoát nạn.
3. **Phản ánh đến chính quyền địa phương:** Nếu chủ trọ cố tình phớt lờ, sinh viên có thể phản ánh đến **Công an phường/xã hoặc Đội Cảnh sát PCCC & CNCH quận/huyện** để kiểm tra an toàn PCCC cơ sở trọ theo chuyên đề của Thủ tướng Chính phủ.

#### D — Chatbot dạng agent

Chưa đủ căn cứ từ các tài liệu hiện có để kết luận cụ thể toàn bộ các bước người thuê cần thực hiện khi lối thoát nạn bị chặn hoặc bị khóa [2].

- Khuyến nghị người thuê đối chiếu việc duy trì giải pháp thoát nạn và duy trì lối thoát nạn, lối ra khẩn cấp theo nội dung kiểm tra an toàn phòng cháy chữa cháy [2].
- Khuyến nghị người thuê xem xét trách nhiệm phòng cháy chữa cháy của người đứng đầu cơ sở hoặc trách nhiệm của người thuê nhà theo quy định pháp luật được viện dẫn [2].

Nghị định số 105/2025/NĐ-CP có hiệu lực thi hành từ ngày 01 tháng 7 năm 2025 [4].
Cơ sở hoạt động trước ngày 01 tháng 7 năm 2025 thuộc danh mục áp dụng tiếp tục thực hiện quản lý và kiểm tra theo quy định chuyển tiếp [4].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng.

Để áp dụng vào trường hợp của bạn:
- Lối thoát nạn đang bị khóa hoặc cản trở bởi chủ nhà hay do người thuê khác?
- Hợp đồng thuê phòng trọ của bạn có thỏa thuận cụ thể về an toàn phòng cháy chữa cháy không?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

Nguồn truy xuất của D (rank dùng trong trích dẫn):

- [1] Luat-55-2024-QH15-dieu-8-20-21-23-24 — Điều 20. Phòng cháy đối với nhà ở | Khoản 2
- [2] Nghị-định-105-2025-NĐ-CP — Điều 13. Nội dung, thẩm quyền kiểm tra về phòng cháy, chữa cháy | Khoản 1
- [3] Luat-55-2024-QH15-dieu-8-20-21-23-24 — Điều 21. Phòng cháy đối với nhà ở kết hợp sản xuất, kinh doanh | Khoản 2
- [4] Nghị-định-105-2025-NĐ-CP — Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp

Lý do giới hạn/fallback của D:

- Phản hồi chưa đáp ứng đầy đủ yêu cầu chính; đánh dấu theo nội dung thay vì provider.

### Câu 20: Chủ trọ và người thuê có trách nhiệm gì đối với thiết bị điện và an toàn cháy nổ?

#### A — Gemini chatbot

Dựa trên nguồn văn bản được cung cấp, trách nhiệm được quy định như sau:

* **Người cho thuê (chủ trọ):** Có trách nhiệm tuyên truyền, đôn đốc, nhắc nhở người thuê thực hiện quy định của pháp luật về phòng cháy, chữa cháy và cứu nạn, cứu hộ (theo Luat-55-2024-QH15-dieu-8-20-21-23-24, Điều 8, Khoản 8, trang 1) [1].
* **Người thuê nhà:** Trừ trường hợp có thỏa thuận khác với người cho thuê, có trách nhiệm tự kiểm tra, kịp thời khắc phục nguy cơ gây cháy, nổ, đôn đốc các thành viên, thực hiện các quy định liên quan và bảo đảm điều kiện an toàn phòng cháy nếu thuê để ở kết hợp sản xuất, kinh doanh (theo Luat-55-2024-QH15-dieu-8-20-21-23-24, Điều 8, Khoản 6, Khoản 8, trang 1) [1], [2].
* **Về an toàn thiết bị điện:** Việc lắp đặt, sử dụng dây dẫn, thiết bị điện trong nhà phải bảo đảm an toàn điện; thường xuyên kiểm tra, kịp thời sửa chữa, thay thế thiết bị không bảo đảm an toàn phòng cháy và tuân thủ quy định sạc xe động cơ điện (theo Luat-55-2024-QH15-dieu-8-20-21-23-24, Điều 24, Khoản 1, trang 1) [3]. Khuyến nghị: hai bên nên kiểm tra, đối chiếu hợp đồng thuê để làm rõ trách nhiệm cụ thể đối với việc bảo trì thiết bị điện.

*Lưu ý: Đây là thông tin tham khảo, không thay thế tư vấn pháp lý chuyên nghiệp.*

#### B — Gemini phân tích + Qwen trích nguồn

Các đoạn trả lời trực tiếp trong nguồn:

- Luat-55-2024-QH15-dieu-8-20-21-23-24 — Điều 8. Trách nhiệm của cơ quan, tổ chức, hộ gia đình, cá nhân trong hoạt động phòng cháy, chữa cháy, cứu nạn, cứu hộ | Khoản 8: “8. Trách nhiệm về phòng cháy, chữa cháy, cứu nạn, cứu hộ đối với trường hợp thuê, mượn, ở nhờ nhà ở được quy định như sau:

8. Trách nhiệm về phòng cháy, chữa cháy, cứu nạn, cứu hộ đối với trường hợp thuê, mượn, ở nhờ nhà ở được quy định như sau: a) Người cho thuê, cho mượn, cho ở nhờ nhà ở có trách nhiệm tuyên truyền, đôn đốc, nhắc nhở người thuê, mượn, ở nhờ thực hiện quy định của pháp luật về phòng cháy, chữa cháy và cứu nạn, cứu hộ;

8. Trách nhiệm về phòng cháy, chữa cháy, cứu nạn, cứu hộ đối với trường hợp thuê, mượn, ở nhờ nhà ở được quy định như sau: b) Người thuê, mượn, ở nhờ nhà ở có trách nhiệm theo quy định tại khoản 6 Điều này, trừ trường hợp có thỏa thuận khác với người cho thuê, mượn, ở nhờ nhà ở. Trường hợp thuê, mượn, ở nhờ nhà ở kết hợp sản xuất, kinh doanh thì người thuê, mượn, ở nhờ còn có trách nhiệm bảo đảm điều kiện an toàn về phòng cháy theo quy định tại Điều 21 của Luật này.” [1].

- Luat-55-2024-QH15-dieu-8-20-21-23-24 — Điều 8. Trách nhiệm của cơ quan, tổ chức, hộ gia đình, cá nhân trong hoạt động phòng cháy, chữa cháy, cứu nạn, cứu hộ | Khoản 6: “6. Chủ hộ gia đình trực tiếp sử dụng nhà ở mà không phải là người đứng đầu cơ sở có trách nhiệm sau đây:

6. Chủ hộ gia đình trực tiếp sử dụng nhà ở mà không phải là người đứng đầu cơ sở có trách nhiệm sau đây: a) Thực hiện quy định tại Điều 20 và Điều 21 của Luật này;

6. Chủ hộ gia đình trực tiếp sử dụng nhà ở mà không phải là người đứng đầu cơ sở có trách nhiệm sau đây: b) Tuyên truyền, đôn đốc, nhắc nhở thành viên khác trong gia đình thực hiện pháp luật về phòng cháy, chữa cháy và cứu nạn, cứu hộ;

6. Chủ hộ gia đình trực tiếp sử dụng nhà ở mà không phải là người đứng đầu cơ sở có trách nhiệm sau đây: c) Thường xuyên tự kiểm tra, phát hiện và khắc phục kịp thời nguy cơ gây cháy, nổ, tai nạn, sự cố;

6. Chủ hộ gia đình trực tiếp sử dụng nhà ở mà không phải là người đứng đầu cơ sở có trách nhiệm sau đây: d) Thực hiện các nhiệm vụ khác về phòng cháy, chữa cháy, cứu nạn, cứu hộ theo quy định của pháp luật.” [2].

- Luat-55-2024-QH15-dieu-8-20-21-23-24 — Điều 24. Phòng cháy trong lắp đặt, sử dụng điện cho sinh hoạt, sản xuất | Khoản 1: “1. Trong lắp đặt, sử dụng điện cho sinh hoạt phải bảo đảm các điều kiện an toàn về phòng cháy sau đây:

1. Trong lắp đặt, sử dụng điện cho sinh hoạt phải bảo đảm các điều kiện an toàn về phòng cháy sau đây: a) Chấp hành quy định về an toàn trong sử dụng điện cho sinh hoạt theo quy định của pháp luật về điện lực;

1. Trong lắp đặt, sử dụng điện cho sinh hoạt phải bảo đảm các điều kiện an toàn về phòng cháy sau đây: b) Đơn vị bán lẻ điện khi đấu nối điện sinh hoạt phải tư vấn việc lắp đặt, sử dụng đối với hệ thống, thiết bị điện để bảo đảm an toàn về phòng cháy;

1. Trong lắp đặt, sử dụng điện cho sinh hoạt phải bảo đảm các điều kiện an toàn về phòng cháy sau đây: c) Việc lắp đặt, sử dụng dây dẫn điện, thiết bị điện trong nhà phải bảo đảm yêu cầu về an toàn điện theo quy định của pháp luật; thường xuyên kiểm tra, kịp thời sửa chữa, thay thế dây dẫn điện, thiết bị điện không bảo đảm an toàn về phòng cháy;

1. Trong lắp đặt, sử dụng điện cho sinh hoạt phải bảo đảm các điều kiện an toàn về phòng cháy sau đây: d) Chỉ được sử dụng thiết bị sạc điện cho xe động cơ điện bảo đảm quy chuẩn kỹ thuật quốc gia; nơi sạc điện cho xe động cơ điện trong nhà phải có giải pháp bảo đảm an toàn về phòng cháy; khu vực sạc điện cho xe động cơ điện tập trung trong nhà còn phải có giải pháp ngăn cháy và trang bị phương tiện chữa cháy phù hợp, bảo đảm tiêu chuẩn.” [3].

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng, hiệu lực và bản gốc.

#### C — Đáp án bạn gửi

- **Trách nhiệm của chủ trọ:**
  - Đầu tư hệ thống điện đạt chuẩn an toàn, lắp aptomat chống giật/quá tải cho từng phòng và toàn dãy trọ.
  - Bảo dưỡng, thay thế bình PCCC định kỳ khi hết hạn; hướng dẫn người thuê kỹ năng PCCC.
- **Trách nhiệm của sinh viên (người thuê):**
  - Không tự ý câu móc, đấu nối dây điện bừa bãi hoặc dùng các thiết bị tiêu thụ công suất quá lớn gây quá tải.
  - Tắt các thiết bị điện sinh nhiệt (bếp từ, bàn ủi, ấm siêu tốc) khi ra khỏi phòng.
  - Chú ý an toàn khi sạc pin xe máy điện/xe đạp điện (không sạc liên tục qua đêm khi không có người trông coi hoặc tại nơi dễ cháy).

#### D — Chatbot dạng agent

Chủ trọ có trách nhiệm đôn đốc nhắc nhở, còn người thuê nhà chịu trách nhiệm kiểm tra khắc phục nguy cơ cháy nổ trừ khi có thỏa thuận khác, đồng thời việc dùng điện sinh hoạt phải đảm bảo an toàn kỹ thuật [1] [2] [3].

- Người cho thuê nhà ở có trách nhiệm tuyên truyền, đôn đốc và nhắc nhở người thuê thực hiện đúng các quy định pháp luật về phòng cháy, chữa cháy và cứu nạn, cứu hộ [1].
- Người thuê nhà có trách nhiệm thường xuyên tự kiểm tra, kịp thời phát hiện và khắc phục nguy cơ gây cháy nổ, tai nạn sự cố trừ khi có thỏa thuận khác với người cho thuê [1] [2].
- Việc lắp đặt và sử dụng dây dẫn điện, thiết bị điện trong nhà phải bảo đảm yêu cầu an toàn, thường xuyên kiểm tra, sửa chữa hoặc thay thế khi không bảo đảm an toàn phòng cháy [3].
- Thiết bị sạc điện cho xe động cơ điện phải bảo đảm quy chuẩn kỹ thuật quốc gia, nơi sạc trong nhà phải có giải pháp an toàn phòng cháy và khu sạc tập trung phải có giải pháp ngăn cháy cùng phương tiện chữa cháy phù hợp [3].

Người thuê nhà có trách nhiệm phòng cháy chữa cháy theo quy định đối với chủ hộ gia đình trực tiếp sử dụng trừ trường hợp có thỏa thuận khác với bên cho thuê [1] [2].
Trường hợp thuê nhà ở kết hợp sản xuất, kinh doanh thì người thuê còn phải chịu thêm trách nhiệm bảo đảm điều kiện an toàn theo quy định riêng [1].

Để áp dụng vào trường hợp của bạn:
- Hợp đồng thuê trọ của bạn có thỏa thuận riêng nào về việc kiểm tra và sửa chữa thiết bị điện không?
- Nhà trọ bạn đang thuê là nhà ở đơn thuần hay có kết hợp hoạt động sản xuất, kinh doanh?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

Nguồn truy xuất của D (rank dùng trong trích dẫn):

- [1] Luat-55-2024-QH15-dieu-8-20-21-23-24 — Điều 8. Trách nhiệm của cơ quan, tổ chức, hộ gia đình, cá nhân trong hoạt động phòng cháy, chữa cháy, cứu nạn, cứu hộ | Khoản 8
- [2] Luat-55-2024-QH15-dieu-8-20-21-23-24 — Điều 8. Trách nhiệm của cơ quan, tổ chức, hộ gia đình, cá nhân trong hoạt động phòng cháy, chữa cháy, cứu nạn, cứu hộ | Khoản 6
- [3] Luat-55-2024-QH15-dieu-8-20-21-23-24 — Điều 24. Phòng cháy trong lắp đặt, sử dụng điện cho sinh hoạt, sản xuất | Khoản 1

Lý do giới hạn/fallback của D:

- Gemini phân tích câu hỏi chưa khả dụng (ValidationError); dùng định tuyến chủ đề dự phòng.

### Câu 21: Người giới thiệu phòng trọ và thu phí môi giới cần công khai những thông tin gì?

#### A — Gemini chatbot

Dựa trên ngữ cảnh được cung cấp, việc công khai và cung cấp thông tin của bên môi giới được quy định như sau:

* Doanh nghiệp kinh doanh dịch vụ môi giới bất động sản có nghĩa vụ cung cấp đầy đủ, trung thực hồ sơ, thông tin về bất động sản do mình môi giới và phải chịu trách nhiệm về hồ sơ, thông tin do mình cung cấp theo quy định tại điểm a khoản 1 Điều 65 Luật-29-2023-QH15 [2].
* Doanh nghiệp kinh doanh dịch vụ môi giới có quyền thu phí dịch vụ của khách hàng theo thỏa thuận của các bên theo điểm c khoản 1 Điều 64 Luật-29-2023-QH15 [1].
* Chưa tìm thấy căn cứ trong các đoạn được cung cấp về danh mục thông tin cụ thể bắt buộc phải công khai riêng đối với cá nhân giới thiệu phòng trọ độc lập thu phí hoặc biểu mẫu công khai chi tiết; Khuyến nghị: người thuê nên kiểm tra, đối chiếu hợp đồng dịch vụ và tính pháp lý của người môi giới trước khi giao dịch.

*Lưu ý: Thông tin trên mang tính chất tham khảo dựa trên tài liệu được cung cấp, không thay thế cho tư vấn pháp lý chuyên nghiệp.*

#### B — Gemini phân tích + Qwen trích nguồn

Các đoạn trả lời trực tiếp trong nguồn:

- Luật-29-2023-QH15 — Điều 65. Nghĩa vụ của doanh nghiệp kinh doanh dịch vụ môi giới bất động sản, cá nhân hành nghề môi giới bất động sản | Khoản 1: “1. Doanh nghiệp kinh doanh dịch vụ môi giới bất động sản có các nghĩa vụ sau đây:

1. Doanh nghiệp kinh doanh dịch vụ môi giới bất động sản có các nghĩa vụ sau đây: a) Cung cấp đầy đủ, trung thực hồ sơ, thông tin về bất động sản do mình môi giới và chịu trách nhiệm về hồ sơ, thông tin do mình cung cấp;

1. Doanh nghiệp kinh doanh dịch vụ môi giới bất động sản có các nghĩa vụ sau đây: b) Tổ chức đào tạo, bồi dưỡng nâng cao kiến thức hành nghề môi giới bất động sản cho nhân viên môi giới bất động sản làm việc trong doanh nghiệp hằng năm;

1. Doanh nghiệp kinh doanh dịch vụ môi giới bất động sản có các nghĩa vụ sau đây: c) Thực hiện nghĩa vụ thuế đối với Nhà nước;

1. Doanh nghiệp kinh doanh dịch vụ môi giới bất động sản có các nghĩa vụ sau đây: d) Bồi thường thiệt hại do lỗi của mình gây ra;

1. Doanh nghiệp kinh doanh dịch vụ môi giới bất động sản có các nghĩa vụ sau đây: đ) Thực hiện chế độ báo cáo theo quy định của pháp luật và chịu sự kiểm tra, thanh tra của cơ quan nhà nước có thẩm quyền;

1. Doanh nghiệp kinh doanh dịch vụ môi giới bất động sản có các nghĩa vụ sau đây: e) Nghĩa vụ khác theo hợp đồng.” [1].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng; cần đối chiếu phần còn thiếu.

Nguồn thù lao cá nhân môi giới với doanh nghiệp chưa trả lời phí người thuê trả.

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng, hiệu lực và bản gốc.

#### C — Đáp án bạn gửi

Theo quy định của Luật Kinh doanh Bất động sản 2023:
- Người hành nghề môi giới BĐS phải công khai: Họ tên, số điện thoại, chứng chỉ hành nghề môi giới (nếu hoạt động độc lập/doanh nghiệp), biểu phí dịch vụ môi giới.
- Thông tin phòng trọ cung cấp phải **trung thực, chính xác**: Giá thuê thực tế, tiền cọc, chi phí điện nước, tình trạng pháp lý và hiện trạng phòng ở.

#### D — Chatbot dạng agent

Chưa đủ căn cứ từ nguồn để xác định toàn bộ các nội dung thông tin phòng trọ hoặc mức phí mà người môi giới phải công khai cho người thuê [2].

- Khuyến nghị sinh viên kiểm tra xem tổ chức hoặc cá nhân môi giới đã thành lập doanh nghiệp kinh doanh dịch vụ bất động sản theo quy định hay chưa [2].
- Khuyến nghị người thuê đối chiếu việc doanh nghiệp môi giới có quy chế hoạt động dịch vụ môi giới bất động sản và cơ sở vật chất, kỹ thuật theo quy định [2].
- Khuyến nghị kiểm tra doanh nghiệp có tối thiểu 01 cá nhân sở hữu chứng chỉ môi giới bất động sản hay không [2].
- Doanh nghiệp kinh doanh dịch vụ môi giới bất động sản phải gửi thông tin về doanh nghiệp đến cơ quan quản lý nhà nước về kinh doanh bất động sản cấp tỉnh nơi thành lập trước khi hoạt động để được đăng tải trên hệ thống thông tin về nhà ở và thị trường bất động sản [2].

Nguồn trích dẫn chỉ nêu điều kiện thành lập doanh nghiệp và việc gửi thông tin doanh nghiệp đến cơ quan quản lý cấp tỉnh, chưa quy định danh mục thông tin phòng trọ phải công khai trực tiếp cho khách thuê [2].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng.
Nguồn thù lao cá nhân môi giới với doanh nghiệp chưa trả lời phí người thuê trả.

Để áp dụng vào trường hợp của bạn:
- Người giới thiệu phòng trọ này hoạt động dưới hình thức doanh nghiệp môi giới hay cá nhân tự do?
- Bạn có thỏa thuận hay hợp đồng dịch vụ môi giới cụ thể nào quy định về khoản phí này chưa?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

Nguồn truy xuất của D (rank dùng trong trích dẫn):

- [1] Luật-29-2023-QH15 — Điều 65. Nghĩa vụ của doanh nghiệp kinh doanh dịch vụ môi giới bất động sản, cá nhân hành nghề môi giới bất động sản | Khoản 1
- [2] Luật-29-2023-QH15 — Điều 61. Điều kiện của tổ chức, cá nhân kinh doanh dịch vụ môi giới bất động sản | Khoản 1
- [3] Luật-29-2023-QH15 — Điều 64. Quyền của doanh nghiệp kinh doanh dịch vụ môi giới bất động sản, cá nhân hành nghề môi giới bất động sản | Khoản 1

Lý do giới hạn/fallback của D:

- Phản hồi chưa đáp ứng đầy đủ yêu cầu chính; đánh dấu theo nội dung thay vì provider.

### Câu 22: Trước khi chuyển tiền cho người môi giới, tôi nên kiểm tra quyền cho thuê và thông tin phòng như thế nào?

#### A — Gemini chatbot

- Theo Luật-29-2023-QH15, Điều 65, Khoản 1, doanh nghiệp môi giới có nghĩa vụ cung cấp đầy đủ, trung thực hồ sơ, thông tin bất động sản và chịu trách nhiệm về thông tin cung cấp [1]. Khuyến nghị: nên yêu cầu người môi giới xuất trình thông tin phòng và giấy tờ ủy quyền hoặc hợp đồng dịch vụ để đối chiếu.
- Bên cho thuê phải đáp ứng điều kiện về chủ thể tham gia giao dịch theo pháp luật về dân sự [3] (văn bản 2026_204_79_VBHN-VPQH, Điều 161, Khoản 1). Khuyến nghị: nên kiểm tra tư cách của người cho thuê để đảm bảo đúng thẩm quyền.
- Giao dịch cho thuê nhà ở không bắt buộc phải có Giấy chứng nhận quyền sở hữu, giấy tờ chứng minh thực hiện theo quy định của Chính phủ [2] (văn bản 2026_204_79_VBHN-VPQH, Điều 160, Khoản 2).

Lưu ý: Đây là thông tin tham khảo, không thay thế tư vấn pháp lý chuyên nghiệp.

#### B — Gemini phân tích + Qwen trích nguồn

Các đoạn trả lời trực tiếp trong nguồn:

- 2026_204_79_VBHN-VPQH — Điều 160. Điều kiện của nhà ở tham gia giao dịch | Khoản 2: “2. Giao dịch về nhà ở sau đây thì nhà ở không bắt buộc phải có Giấy chứng nhận:

2. Giao dịch về nhà ở sau đây thì nhà ở không bắt buộc phải có Giấy chứng nhận: a) Mua bán, thuê mua, thế chấp nhà ở hình thành trong tương lai; bán nhà ở trong trường hợp giải thể, phá sản;

2. Giao dịch về nhà ở sau đây thì nhà ở không bắt buộc phải có Giấy chứng nhận: b) Tổ chức tặng cho nhà tình nghĩa, nhà tình thương, nhà đại đoàn kết;

2. Giao dịch về nhà ở sau đây thì nhà ở không bắt buộc phải có Giấy chứng nhận: c) Mua bán, thuê mua nhà ở có sẵn của chủ đầu tư dự án đầu tư xây dựng nhà ở trong các trường hợp sau đây: nhà ở thuộc tài sản công; nhà ở xã hội, nhà ở cho lực lượng vũ trang nhân dân, nhà ở phục vụ tái định cư không thuộc tài sản công;

2. Giao dịch về nhà ở sau đây thì nhà ở không bắt buộc phải có Giấy chứng nhận: d) Cho thuê, cho mượn, cho ở nhờ, ủy quyền quản lý nhà ở;

2. Giao dịch về nhà ở sau đây thì nhà ở không bắt buộc phải có Giấy chứng nhận: đ) Nhận thừa kế nhà ở.

Giấy tờ chứng minh điều kiện nhà ở tham gia giao dịch quy định tại khoản này thực hiện theo quy định của Chính phủ.” [2].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng; cần đối chiếu phần còn thiếu.

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng, hiệu lực và bản gốc.

#### C — Đáp án bạn gửi

- **Nguyên tắc vàng:** **Tuyệt đối không chuyển tiền cọc xem phòng hay phí giữ chỗ** cho người tự xưng là môi giới khi chưa đến xem phòng trực tiếp và chưa gặp chủ nhà.
- Khi đến xem phòng, yêu cầu người môi giới chỉ rõ: Ai là chủ nhà trọ thực sự? Có văn bản ủy quyền cho thuê không?
- Hợp đồng thuê và tiền cọc phải được **ký và trao trực tiếp cho chủ nhà** (kèm xem CCCD đối chiếu giấy tờ nhà). Khoản phí hoa hồng môi giới thông thường do chủ nhà trọ chi trả, không phải nghĩa vụ của sinh viên trừ khi có thỏa thuận riêng từ trước.

#### D — Chatbot dạng agent

Chưa đủ căn cứ từ nguồn để hướng dẫn chi tiết quy trình tự kiểm tra quyền cho thuê, nhưng doanh nghiệp môi giới có nghĩa vụ cung cấp đầy đủ, trung thực hồ sơ, thông tin bất động sản và chịu trách nhiệm về thông tin cung cấp [1].

- Khuyến nghị yêu cầu doanh nghiệp môi giới cung cấp đầy đủ hồ sơ và thông tin về phòng trọ theo nghĩa vụ cung cấp thông tin trung thực của họ [1].
- Khuyến nghị đối chiếu các cam kết và trách nhiệm bồi thường thiệt hại của doanh nghiệp môi giới theo thỏa thuận hợp đồng trước khi chuyển tiền [1].

Nguồn trích dẫn chỉ quy định nghĩa vụ của doanh nghiệp kinh doanh dịch vụ môi giới bất động sản chứ chưa nêu quy trình kiểm tra cụ thể cho người đi thuê [1].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng.
Nguồn thù lao cá nhân môi giới với doanh nghiệp chưa trả lời phí người thuê trả.

Để áp dụng vào trường hợp của bạn:
- Người môi giới của bạn là cá nhân độc lập hay thuộc doanh nghiệp kinh doanh dịch vụ môi giới?
- Bên môi giới đã cung cấp cho bạn những giấy tờ pháp lý nào liên quan đến căn phòng?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

Nguồn truy xuất của D (rank dùng trong trích dẫn):

- [1] Luật-29-2023-QH15 — Điều 65. Nghĩa vụ của doanh nghiệp kinh doanh dịch vụ môi giới bất động sản, cá nhân hành nghề môi giới bất động sản | Khoản 1
- [2] 2026_204_79_VBHN-VPQH — Điều 160. Điều kiện của nhà ở tham gia giao dịch | Khoản 2
- [3] 2026_204_79_VBHN-VPQH — Điều 161. Điều kiện của các bên tham gia giao dịch về nhà ở | Khoản 1

Lý do giới hạn/fallback của D:

- Gemini phân tích câu hỏi chưa khả dụng (ValidationError); dùng định tuyến chủ đề dự phòng.
- Phản hồi chưa đáp ứng đầy đủ yêu cầu chính; đánh dấu theo nội dung thay vì provider.

### Câu 23: Nếu người môi giới đưa thông tin khác với phòng thực tế, người thuê có thể làm gì?

#### A — Gemini chatbot

Dựa trên các đoạn thông tin được cung cấp:

* Doanh nghiệp môi giới có nghĩa vụ cung cấp đầy đủ, trung thực thông tin bất động sản và chịu trách nhiệm về thông tin cung cấp theo Luật-29-2023-QH15, Điều 65, Khoản 1, điểm a, trang 1 [1].
* Nếu thông tin sai lệch dẫn đến thiệt hại, người thuê có thể yêu cầu doanh nghiệp môi giới bồi thường thiệt hại do lỗi của họ gây ra theo Luật-29-2023-QH15, Điều 65, Khoản 1, điểm d, trang 1 [1].
* Về các quyền xử lý khác đối với việc thuê phòng (như hủy giao dịch, đòi cọc), hiện chưa tìm thấy căn cứ cụ thể trong các đoạn được cung cấp. Khuyến nghị: người thuê nên kiểm tra lại các thỏa thuận và nghĩa vụ khác trong hợp đồng dịch vụ đã ký kết theo Luật-29-2023-QH15, Điều 65, Khoản 1, điểm e, trang 1 [1].

*Lưu ý: Đây là thông tin tham khảo, không thay thế tư vấn pháp lý chuyên nghiệp.*

#### B — Gemini phân tích + Qwen trích nguồn

Các đoạn trả lời trực tiếp trong nguồn:

- Luật-29-2023-QH15 — Điều 65. Nghĩa vụ của doanh nghiệp kinh doanh dịch vụ môi giới bất động sản, cá nhân hành nghề môi giới bất động sản | Khoản 1: “1. Doanh nghiệp kinh doanh dịch vụ môi giới bất động sản có các nghĩa vụ sau đây:

1. Doanh nghiệp kinh doanh dịch vụ môi giới bất động sản có các nghĩa vụ sau đây: a) Cung cấp đầy đủ, trung thực hồ sơ, thông tin về bất động sản do mình môi giới và chịu trách nhiệm về hồ sơ, thông tin do mình cung cấp;

1. Doanh nghiệp kinh doanh dịch vụ môi giới bất động sản có các nghĩa vụ sau đây: b) Tổ chức đào tạo, bồi dưỡng nâng cao kiến thức hành nghề môi giới bất động sản cho nhân viên môi giới bất động sản làm việc trong doanh nghiệp hằng năm;

1. Doanh nghiệp kinh doanh dịch vụ môi giới bất động sản có các nghĩa vụ sau đây: c) Thực hiện nghĩa vụ thuế đối với Nhà nước;

1. Doanh nghiệp kinh doanh dịch vụ môi giới bất động sản có các nghĩa vụ sau đây: d) Bồi thường thiệt hại do lỗi của mình gây ra;

1. Doanh nghiệp kinh doanh dịch vụ môi giới bất động sản có các nghĩa vụ sau đây: đ) Thực hiện chế độ báo cáo theo quy định của pháp luật và chịu sự kiểm tra, thanh tra của cơ quan nhà nước có thẩm quyền;

1. Doanh nghiệp kinh doanh dịch vụ môi giới bất động sản có các nghĩa vụ sau đây: e) Nghĩa vụ khác theo hợp đồng.” [1].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng; cần đối chiếu phần còn thiếu.

Nguồn thù lao cá nhân môi giới với doanh nghiệp chưa trả lời phí người thuê trả.

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng, hiệu lực và bản gốc.

#### C — Đáp án bạn gửi

- Bạn có toàn quyền **từ chối thuê và từ chối thanh toán bất kỳ khoản phí môi giới nào** vì người môi giới đã cung cấp thông tin sai sự thật, vi phạm nguyên tắc trung thực theo Luật Kinh doanh Bất động sản.
- Nếu người môi giới đã ép bạn đóng phí "dẫn đi xem phòng" từ trước, bạn có quyền yêu cầu hoàn trả và báo cáo sự việc với ban quản trị nền tảng hoặc cơ quan công an nếu có dấu hiệu cưỡng đoạt/lừa đảo.

#### D — Chatbot dạng agent

Chưa đủ căn cứ từ nguồn để nêu toàn bộ quyền xử lý của người thuê, nhưng doanh nghiệp môi giới phải chịu trách nhiệm về thông tin cung cấp và bồi thường thiệt hại do lỗi của mình gây ra [1].

- Người thuê có thể yêu cầu doanh nghiệp môi giới thực hiện đúng trách nhiệm về hồ sơ, thông tin bất động sản đã cung cấp [1].
- Người thuê có thể yêu cầu doanh nghiệp môi giới bồi thường thiệt hại nếu phát sinh thiệt hại do lỗi cung cấp sai thông tin của bên môi giới [1].
- Khuyến nghị người thuê đối chiếu lại các cam kết và nghĩa vụ khác theo hợp đồng dịch vụ môi giới đã xác lập [1].

Căn cứ được trích dẫn chỉ quy định nghĩa vụ của doanh nghiệp kinh doanh dịch vụ môi giới bất động sản chứ chưa nêu cụ thể quyền hủy cọc hoặc phạt vi phạm của người thuê [1].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng.
Nguồn thù lao cá nhân môi giới với doanh nghiệp chưa trả lời phí người thuê trả.

Để áp dụng vào trường hợp của bạn:
- Bạn đã ký hợp đồng dịch vụ môi giới hoặc đặt cọc giữ phòng hay chưa?
- Thông tin phòng thực tế bị sai lệch ở những điểm cụ thể nào và có gây thiệt hại tài chính không?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

Nguồn truy xuất của D (rank dùng trong trích dẫn):

- [1] Luật-29-2023-QH15 — Điều 65. Nghĩa vụ của doanh nghiệp kinh doanh dịch vụ môi giới bất động sản, cá nhân hành nghề môi giới bất động sản | Khoản 1
- [2] Luật-29-2023-QH15 — Điều 64. Quyền của doanh nghiệp kinh doanh dịch vụ môi giới bất động sản, cá nhân hành nghề môi giới bất động sản | Khoản 1
- [3] Luật-29-2023-QH15 — Điều 61. Điều kiện của tổ chức, cá nhân kinh doanh dịch vụ môi giới bất động sản | Khoản 1

Lý do giới hạn/fallback của D:

- Phản hồi chưa đáp ứng đầy đủ yêu cầu chính; đánh dấu theo nội dung thay vì provider.

### Câu 24: Khoản phí môi giới nên được thỏa thuận và thể hiện trong giấy tờ ra sao?

#### A — Gemini chatbot

Các căn cứ liên quan tìm được trong kho (trích nguyên đoạn):

- Luật-29-2023-QH15 — Điều 64. Quyền của doanh nghiệp kinh doanh dịch vụ môi giới bất động sản, cá nhân hành nghề môi giới bất động sản | Khoản 1: “1. Doanh nghiệp kinh doanh dịch vụ môi giới bất động sản có các quyền sau đây: c) Thu phí dịch vụ của khách hàng theo thỏa thuận của các bên;” [1].

- Luật-29-2023-QH15 — Điều 64. Quyền của doanh nghiệp kinh doanh dịch vụ môi giới bất động sản, cá nhân hành nghề môi giới bất động sản | Khoản 1: “1. Doanh nghiệp kinh doanh dịch vụ môi giới bất động sản có các quyền sau đây: b) Yêu cầu các tổ chức, cá nhân có liên quan cung cấp hồ sơ, thông tin bất động sản thực hiện giao dịch;” [1].

Đây là câu trả lời một phần từ nguồn; chưa kết luận cách áp dụng cho tình huống riêng của bạn. Cần đối chiếu điều kiện, hiệu lực và bản gốc.

#### B — Gemini phân tích + Qwen trích nguồn

Các đoạn trả lời trực tiếp trong nguồn:

- Luật-29-2023-QH15 — Điều 64. Quyền của doanh nghiệp kinh doanh dịch vụ môi giới bất động sản, cá nhân hành nghề môi giới bất động sản | Khoản 1: “1. Doanh nghiệp kinh doanh dịch vụ môi giới bất động sản có các quyền sau đây:

1. Doanh nghiệp kinh doanh dịch vụ môi giới bất động sản có các quyền sau đây: a) Thực hiện môi giới bất động sản theo quy định của Luật này;

1. Doanh nghiệp kinh doanh dịch vụ môi giới bất động sản có các quyền sau đây: b) Yêu cầu các tổ chức, cá nhân có liên quan cung cấp hồ sơ, thông tin bất động sản thực hiện giao dịch;

1. Doanh nghiệp kinh doanh dịch vụ môi giới bất động sản có các quyền sau đây: c) Thu phí dịch vụ của khách hàng theo thỏa thuận của các bên;

1. Doanh nghiệp kinh doanh dịch vụ môi giới bất động sản có các quyền sau đây: d) Từ chối môi giới bất động sản không đủ điều kiện đưa vào kinh doanh;

1. Doanh nghiệp kinh doanh dịch vụ môi giới bất động sản có các quyền sau đây: đ) Yêu cầu các tổ chức, cá nhân có liên quan bồi thường thiệt hại do lỗi của họ gây ra;

1. Doanh nghiệp kinh doanh dịch vụ môi giới bất động sản có các quyền sau đây: e) Quyền khác theo hợp đồng.” [1].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng; cần đối chiếu phần còn thiếu.

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng, hiệu lực và bản gốc.

#### C — Đáp án bạn gửi

- Phí môi giới phải được lập thành **Hợp đồng dịch vụ môi giới** hoặc phiếu thu có chữ ký xác nhận của hai bên.
- Giấy tờ phải ghi rõ: Mức phí dịch vụ, điều kiện phát sinh phí (chỉ trả khi ký kết hợp đồng thuê trọ thành công), cam kết hoàn tiền nếu giao dịch không thành do lỗi của bên môi giới.

#### D — Chatbot dạng agent

Chưa đủ căn cứ pháp lý để kết luận chi tiết về việc thỏa thuận và thể hiện khoản phí môi giới trong giấy tờ ngoài việc các bên thực hiện các nghĩa vụ khác theo hợp đồng [3].

- Khuyến nghị xác lập rõ các cam kết và nghĩa vụ liên quan đến phí dịch vụ vào hợp đồng bằng văn bản với doanh nghiệp kinh doanh dịch vụ môi giới bất động sản [3].
- Khuyến nghị yêu cầu doanh nghiệp kinh doanh dịch vụ môi giới cung cấp đầy đủ và trung thực hồ sơ thông tin về bất động sản trước khi chốt thỏa thuận [3].

Căn cứ được cung cấp chỉ quy định nghĩa vụ của doanh nghiệp kinh doanh dịch vụ môi giới bất động sản mà chưa có quy định cụ thể về mức hay cách ghi nhận phí môi giới của người thuê [3].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng.
Nguồn thù lao cá nhân môi giới với doanh nghiệp chưa trả lời phí người thuê trả.

Để áp dụng vào trường hợp của bạn:
- Bạn đang thỏa thuận trả phí môi giới trực tiếp cho cá nhân môi giới hay cho doanh nghiệp dịch vụ môi giới?
- Các bên dự kiến ghi nhận phí môi giới trong hợp đồng dịch vụ riêng hay đưa vào điều khoản hợp đồng thuê trọ?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

Nguồn truy xuất của D (rank dùng trong trích dẫn):

- [1] Luật-29-2023-QH15 — Điều 64. Quyền của doanh nghiệp kinh doanh dịch vụ môi giới bất động sản, cá nhân hành nghề môi giới bất động sản | Khoản 1
- [2] Luật-29-2023-QH15 — Điều 61. Điều kiện của tổ chức, cá nhân kinh doanh dịch vụ môi giới bất động sản | Khoản 1
- [3] Luật-29-2023-QH15 — Điều 65. Nghĩa vụ của doanh nghiệp kinh doanh dịch vụ môi giới bất động sản, cá nhân hành nghề môi giới bất động sản | Khoản 1

Lý do giới hạn/fallback của D:

- Phản hồi chưa đáp ứng đầy đủ yêu cầu chính; đánh dấu theo nội dung thay vì provider.

### Câu 25: Khi tìm phòng qua một nền tảng trực tuyến, tôi nên kiểm tra người đăng và nguồn tin như thế nào?

#### A — Gemini chatbot

Dưới đây là các lưu ý khi tìm thông tin phòng trọ qua nền tảng trực tuyến:

* Khuyến nghị: nên kiểm tra thông tin danh tính, liên hệ của người đăng và việc xác thực, kiểm duyệt của nền tảng; nếu là nền tảng trung gian, nền tảng có các nghĩa vụ như xác thực điện tử người bán, công khai danh tính/thông tin liên hệ và kiểm duyệt nội dung tin trước khi hiển thị theo quy định tại Nghị định 248/2026/NĐ-CP, Điều 18, trang 1 [2].
* Theo khuyến cáo của cơ quan Công an: Tuyệt đối không cung cấp thông tin tài khoản, mật khẩu, mã OTP; không truy cập đường link lạ, quét mã QR không rõ nguồn gốc; không cài đặt ứng dụng theo hướng dẫn của người gọi và không chuyển tiền để nhận hoàn tiền, bồi thường [1].

*Lưu ý: Đây là thông tin tham khảo, không thay thế tư vấn pháp lý chuyên nghiệp.*

#### B — Gemini phân tích + Qwen trích nguồn

Các đoạn trả lời trực tiếp trong nguồn:

- online_warning-Bo-Cong-an-20261003 — trích đoạn: “KHUYẾN CÁO PHÒNG NGỪA LỪA ĐẢO — KHÔNG PHẢI ĐIỀU LUẬT

Khuyến cáo của cơ quan Công an về lừa đảo mua hàng trực tuyến

Tuyệt đối không cung cấp thông tin tài khoản, mật khẩu, mã OTP; không truy cập đường link lạ, quét mã QR không rõ nguồn gốc; không cài đặt ứng dụng theo hướng dẫn của người gọi và không chuyển tiền để nhận hoàn tiền, bồi thường.

Trường hợp nghi ngờ bị lừa đảo, người dân cần ngừng ngay giao dịch, liên hệ ngân hàng để khóa tài khoản khi cần thiết, lưu giữ tin nhắn, số điện thoại, lịch sử giao dịch và trình báo cơ quan Công an gần nhất để được hỗ trợ.” [1].

- Nghị-định-248-2026-NĐ-CP-trích-tuyển — Điều 18 — nền tảng trung gian: “Điều 18 — nền tảng trung gian

Nếu được phân loại là nền tảng thương mại điện tử trung gian, có các nghĩa vụ như xác thực điện tử người bán, công khai danh tính/thông tin liên hệ, kiểm duyệt nội dung tin trước khi hiển thị và duy trì khả năng truy cập dữ liệu tin theo thời hạn quy định.

Chức năng đặt hàng trực tuyến

Khi có chức năng đặt hàng trực tuyến, khoản 2 Điều 18 bổ sung các trách nhiệm riêng, gồm thông tin hỗ trợ giao dịch và xử lý trường hợp nội dung cung cấp không đúng cam kết. Nếu app nhận đặt cọc/tiền thuê, cần rà soát sâu thêm điều khoản thanh toán, hợp đồng điện tử và bảo vệ người tiêu dùng.

Lược khỏi bản trích

Yêu cầu chỉ dành cho nền tảng rất lớn, tích hợp nền tảng hoặc livestream không đưa vào chunk mặc định; bật lại khi sản phẩm triển khai chức năng tương ứng.

Nguồn đối chiếu

https://vanban.chinhphu.vn/?docid=218747&orggroupid=2&pageid=27160

https://vanban.chinhphu.vn/?classid=1&docid=216503&pageid=27160&typegroupid=3

Ghi chú: Đây là bản rút gọn có biên tập để phục vụ nghiên cứu và truy xuất theo điều khoản. Khi trả lời một tình huống thực tế, cần kiểm tra bản gốc, văn bản sửa đổi, điều khoản chuyển tiếp và dữ kiện cụ thể.” [2].

- Luật-122-2025-QH15-trích-tuyển — Điều 17 — nền tảng trung gian: “Điều 17 — nền tảng trung gian

Nếu sản phẩm được phân loại là nền tảng thương mại điện tử trung gian, giữ trách nhiệm xác thực điện tử người bán và công khai thông tin người bán; tổ chức kiểm soát nội dung, tiếp nhận phản ánh/khiếu nại và bảo đảm dữ liệu theo quy định.” [3].

- Luật-122-2025-QH15-trích-tuyển — Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp: “Điều 40 — hiệu lực
Điều 40 — hiệu lực

Luật áp dụng từ 01/07/2026. Văn bản không tự quyết định hệ thống tìm trọ thuộc loại nền tảng nào; việc phân loại cần lập bản đồ từng luồng chức năng.

Lược khỏi bản trích

Nhánh livestream, hàng hóa số, đấu giá và thương mại xuyên biên giới không cần cho dịch vụ đăng tin phòng trọ, trừ khi sản phẩm mở thêm tính năng tương ứng.

Nguồn đối chiếu

https://vanban.chinhphu.vn/?classid=1&docid=216503&pageid=27160&typegroupid=3

https://datafiles.chinhphu.vn/cpp/files/vbpq/2026/01/luat122.2025.qh15.pdf

Ghi chú: Đây là bản rút gọn có biên tập để phục vụ nghiên cứu và truy xuất theo điều khoản. Khi trả lời một tình huống thực tế, cần kiểm tra bản gốc, văn bản sửa đổi, điều khoản chuyển tiếp và dữ kiện cụ thể.” [4].

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng, hiệu lực và bản gốc.

#### C — Đáp án bạn gửi

- **Kiểm tra tài khoản người đăng:** Tài khoản mới tạo hay đã hoạt động lâu năm? Có tích xanh xác thực danh tính không? Lịch sử đăng tin có nhiều phòng ảo giá rẻ bất thường không?
- **Kiểm tra hình ảnh tin đăng:** Sử dụng tính năng "Tìm kiếm bằng hình ảnh trên Google" để kiểm tra xem ảnh phòng trọ có bị copy từ các khách sạn, căn hộ cao cấp khác ở TP.HCM/Hà Nội hay không.
- **Cảnh giác mức giá "quá hời":** Ví dụ phòng máy lạnh full nội thất tại Ninh Kiều mà đăng giá chỉ 800k - 1 triệu đồng là 99% bẫy lừa cọc.

#### D — Chatbot dạng agent

Các đoạn trả lời trực tiếp trong nguồn:

- online_warning-Bo-Cong-an-20261003 — trích đoạn: “KHUYẾN CÁO PHÒNG NGỪA LỪA ĐẢO — KHÔNG PHẢI ĐIỀU LUẬT

Khuyến cáo của cơ quan Công an về lừa đảo mua hàng trực tuyến

Tuyệt đối không cung cấp thông tin tài khoản, mật khẩu, mã OTP; không truy cập đường link lạ, quét mã QR không rõ nguồn gốc; không cài đặt ứng dụng theo hướng dẫn của người gọi và không chuyển tiền để nhận hoàn tiền, bồi thường.

Trường hợp nghi ngờ bị lừa đảo, người dân cần ngừng ngay giao dịch, liên hệ ngân hàng để khóa tài khoản khi cần thiết, lưu giữ tin nhắn, số điện thoại, lịch sử giao dịch và trình báo cơ quan Công an gần nhất để được hỗ trợ.” [1].

- Nghị-định-248-2026-NĐ-CP-trích-tuyển — Điều 18 — nền tảng trung gian: “Điều 18 — nền tảng trung gian

Nếu được phân loại là nền tảng thương mại điện tử trung gian, có các nghĩa vụ như xác thực điện tử người bán, công khai danh tính/thông tin liên hệ, kiểm duyệt nội dung tin trước khi hiển thị và duy trì khả năng truy cập dữ liệu tin theo thời hạn quy định.

Chức năng đặt hàng trực tuyến

Khi có chức năng đặt hàng trực tuyến, khoản 2 Điều 18 bổ sung các trách nhiệm riêng, gồm thông tin hỗ trợ giao dịch và xử lý trường hợp nội dung cung cấp không đúng cam kết. Nếu app nhận đặt cọc/tiền thuê, cần rà soát sâu thêm điều khoản thanh toán, hợp đồng điện tử và bảo vệ người tiêu dùng.

Lược khỏi bản trích

Yêu cầu chỉ dành cho nền tảng rất lớn, tích hợp nền tảng hoặc livestream không đưa vào chunk mặc định; bật lại khi sản phẩm triển khai chức năng tương ứng.

Nguồn đối chiếu

https://vanban.chinhphu.vn/?docid=218747&orggroupid=2&pageid=27160

https://vanban.chinhphu.vn/?classid=1&docid=216503&pageid=27160&typegroupid=3

Ghi chú: Đây là bản rút gọn có biên tập để phục vụ nghiên cứu và truy xuất theo điều khoản. Khi trả lời một tình huống thực tế, cần kiểm tra bản gốc, văn bản sửa đổi, điều khoản chuyển tiếp và dữ kiện cụ thể.” [2].

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng, hiệu lực và bản gốc.

Nguồn truy xuất của D (rank dùng trong trích dẫn):

- [1] online_warning-Bo-Cong-an-20261003
- [2] Nghị-định-248-2026-NĐ-CP-trích-tuyển — Điều 18 — nền tảng trung gian
- [3] Luật-122-2025-QH15-trích-tuyển — Điều 40 — hiệu lực

Lý do giới hạn/fallback của D:

- Gemini phân tích câu hỏi chưa khả dụng (ValidationError); dùng định tuyến chủ đề dự phòng.
- Nguồn [2] không khẳng định 'mới có nghĩa vụ' (không loại trừ các trường hợp/chủ thể khác theo nguyên tắc không thêm 'chỉ/mới').
- Bản tổng hợp chưa được nguồn xác nhận sau lần sửa; dùng trích đoạn Qwen đã chọn.

### Câu 26: Nếu một tin đăng nhà trọ có thông tin sai, tôi có thể báo cáo cho nền tảng bằng cách nào?

#### A — Gemini chatbot

- Theo văn bản Nghị-định-248-2026-NĐ-CP-trích-tuyển, Điều 7, trang 1, nền tảng phải công khai cách tiếp nhận và quy trình xử lý phản ánh, khiếu nại [3]. Bạn có thể thực hiện báo cáo thông qua các kênh tiếp nhận được nền tảng công khai này [3].
- Trường hợp thuộc nền tảng thương mại điện tử trung gian, nền tảng có trách nhiệm tổ chức tiếp nhận phản ánh, khiếu nại theo văn bản Luật-122-2025-QH15-trích-tuyển, Điều 17 [2].
- Chưa tìm thấy căn cứ trong các đoạn được cung cấp về hình thức kỹ thuật cụ thể (như nút bấm, biểu mẫu hay email) để gửi báo cáo; Khuyến nghị: nên kiểm tra trực tiếp quy trình và kênh báo tin giả được công khai trên giao diện của từng nền tảng [3]. Lưu ý văn bản Luật-122-2025-QH15-trích-tuyển có hiệu lực áp dụng từ 01/07/2026 theo Điều 40 [4].

*Thông tin mang tính chất tham khảo, không thay thế cho tư vấn pháp lý chuyên nghiệp.*

#### B — Gemini phân tích + Qwen trích nguồn

Các đoạn trả lời trực tiếp trong nguồn:

- Nghị-định-248-2026-NĐ-CP-trích-tuyển — Điều 7 — tiếp nhận và xử lý phản ánh, khiếu nại: “Điều 7 — tiếp nhận và xử lý phản ánh, khiếu nại

Nền tảng phải có cách tiếp nhận và quy trình xử lý phản ánh/khiếu nại được công khai. Với dịch vụ tìm trọ, nên giữ kênh báo tin giả, yêu cầu gỡ tin, tranh chấp nội dung quảng cáo và khiếu nại của người dùng.” [3].

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng, hiệu lực và bản gốc.

#### C — Đáp án bạn gửi

- Sử dụng nút **"Báo cáo tin đăng" (Report)** trực tiếp trên giao diện của website/ứng dụng đó, chọn lý do như: "Tin giả/Phòng không có thật", "Sai giá thuê", "Có dấu hiệu lừa đảo cọc".
- Đính kèm ảnh chụp tin nhắn bằng chứng nếu người đăng yêu cầu chuyển khoản qua link lạ hoặc có hành vi gian dối.

#### D — Chatbot dạng agent

Bạn có thể báo cáo tin đăng sai thông qua cách tiếp nhận và quy trình xử lý phản ánh hoặc khiếu nại đã được nền tảng công khai [3].

- Bạn tra cứu cách tiếp nhận và quy trình xử lý phản ánh hoặc khiếu nại mà nền tảng đã công khai [3].
- Đối với dịch vụ tìm trọ, bạn gửi nội dung phản ánh qua kênh báo tin giả hoặc yêu cầu gỡ tin của nền tảng [3].
- Bạn gửi phản ánh qua kênh tranh chấp nội dung quảng cáo và khiếu nại của người dùng nếu có phát sinh tranh chấp liên quan [3].

Nền tảng phải có cách tiếp nhận và quy trình xử lý phản ánh, khiếu nại được công khai theo quy định [3].
Nguồn quy định nền tảng cung cấp dịch vụ tìm trọ nên giữ kênh báo tin giả, yêu cầu gỡ tin, tranh chấp nội dung quảng cáo và khiếu nại của người dùng [3].

Để áp dụng vào trường hợp của bạn:
- Nền tảng bạn đang sử dụng để xem tin đăng nhà trọ có tên là gì?
- Nền tảng đó đã công khai kênh tiếp nhận khiếu nại hoặc báo tin giả cụ thể nào chưa?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

Nguồn truy xuất của D (rank dùng trong trích dẫn):

- [1] Nghị-định-248-2026-NĐ-CP-trích-tuyển — Điều 18 — nền tảng trung gian
- [2] Luật-122-2025-QH15-trích-tuyển — Điều 17 — nền tảng trung gian
- [3] Nghị-định-248-2026-NĐ-CP-trích-tuyển — Điều 7 — tiếp nhận và xử lý phản ánh, khiếu nại
- [4] Luật-122-2025-QH15-trích-tuyển — Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp

### Câu 27: Nền tảng đăng tin có trách nhiệm gì đối với thông tin người bán hoặc người cho thuê theo tài liệu hiện có?

#### A — Gemini chatbot

Các căn cứ liên quan tìm được trong kho (trích nguyên đoạn):

- Luật-122-2025-QH15-trích-tuyển — Điều 17 — nền tảng trung gian: “Nếu sản phẩm được phân loại là nền tảng thương mại điện tử trung gian, giữ trách nhiệm xác thực điện tử người bán và công khai thông tin người bán; tổ chức kiểm soát nội dung, tiếp nhận phản ánh/khiếu nại và bảo đảm dữ liệu theo quy định.” [2].

- Nghị-định-248-2026-NĐ-CP-trích-tuyển — Điều 18 — nền tảng trung gian: “Nếu được phân loại là nền tảng thương mại điện tử trung gian, có các nghĩa vụ như xác thực điện tử người bán, công khai danh tính/thông tin liên hệ, kiểm duyệt nội dung tin trước khi hiển thị và duy trì khả năng truy cập dữ liệu tin theo thời hạn quy định.” [1].

Đây là câu trả lời một phần từ nguồn; chưa kết luận cách áp dụng cho tình huống riêng của bạn. Cần đối chiếu điều kiện, hiệu lực và bản gốc.

#### B — Gemini phân tích + Qwen trích nguồn

Các đoạn trả lời trực tiếp trong nguồn:

- Nghị-định-248-2026-NĐ-CP-trích-tuyển — Điều 18 — nền tảng trung gian: “Điều 18 — nền tảng trung gian

Nếu được phân loại là nền tảng thương mại điện tử trung gian, có các nghĩa vụ như xác thực điện tử người bán, công khai danh tính/thông tin liên hệ, kiểm duyệt nội dung tin trước khi hiển thị và duy trì khả năng truy cập dữ liệu tin theo thời hạn quy định.

Chức năng đặt hàng trực tuyến

Khi có chức năng đặt hàng trực tuyến, khoản 2 Điều 18 bổ sung các trách nhiệm riêng, gồm thông tin hỗ trợ giao dịch và xử lý trường hợp nội dung cung cấp không đúng cam kết. Nếu app nhận đặt cọc/tiền thuê, cần rà soát sâu thêm điều khoản thanh toán, hợp đồng điện tử và bảo vệ người tiêu dùng.

Lược khỏi bản trích

Yêu cầu chỉ dành cho nền tảng rất lớn, tích hợp nền tảng hoặc livestream không đưa vào chunk mặc định; bật lại khi sản phẩm triển khai chức năng tương ứng.

Nguồn đối chiếu

https://vanban.chinhphu.vn/?docid=218747&orggroupid=2&pageid=27160

https://vanban.chinhphu.vn/?classid=1&docid=216503&pageid=27160&typegroupid=3

Ghi chú: Đây là bản rút gọn có biên tập để phục vụ nghiên cứu và truy xuất theo điều khoản. Khi trả lời một tình huống thực tế, cần kiểm tra bản gốc, văn bản sửa đổi, điều khoản chuyển tiếp và dữ kiện cụ thể.” [1].

- Luật-122-2025-QH15-trích-tuyển — Điều 17 — nền tảng trung gian: “Điều 17 — nền tảng trung gian

Nếu sản phẩm được phân loại là nền tảng thương mại điện tử trung gian, giữ trách nhiệm xác thực điện tử người bán và công khai thông tin người bán; tổ chức kiểm soát nội dung, tiếp nhận phản ánh/khiếu nại và bảo đảm dữ liệu theo quy định.” [2].

- Luật-122-2025-QH15-trích-tuyển — Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp: “Điều 40 — hiệu lực
Điều 40 — hiệu lực

Luật áp dụng từ 01/07/2026. Văn bản không tự quyết định hệ thống tìm trọ thuộc loại nền tảng nào; việc phân loại cần lập bản đồ từng luồng chức năng.

Lược khỏi bản trích

Nhánh livestream, hàng hóa số, đấu giá và thương mại xuyên biên giới không cần cho dịch vụ đăng tin phòng trọ, trừ khi sản phẩm mở thêm tính năng tương ứng.

Nguồn đối chiếu

https://vanban.chinhphu.vn/?classid=1&docid=216503&pageid=27160&typegroupid=3

https://datafiles.chinhphu.vn/cpp/files/vbpq/2026/01/luat122.2025.qh15.pdf

Ghi chú: Đây là bản rút gọn có biên tập để phục vụ nghiên cứu và truy xuất theo điều khoản. Khi trả lời một tình huống thực tế, cần kiểm tra bản gốc, văn bản sửa đổi, điều khoản chuyển tiếp và dữ kiện cụ thể.” [4].

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng, hiệu lực và bản gốc.

#### C — Đáp án bạn gửi

Căn cứ theo **Nghị định 52/2013/NĐ-CP** (được sửa đổi bởi **Nghị định 85/2021/NĐ-CP**) về thương mại điện tử:
- Nền tảng có trách nhiệm: Yêu cầu người đăng tin cung cấp thông tin định danh (tên, số điện thoại, địa chỉ);
- Phải thiết lập cơ chế tiếp nhận khiếu nại, phản ánh và **ngăn chặn, gỡ bỏ ngay lập tức** các tin đăng vi phạm pháp luật, tin đăng giả mạo hoặc lừa đảo;
- Cung cấp thông tin của đối tượng vi phạm cho cơ quan công an khi có yêu cầu điều tra.

#### D — Chatbot dạng agent

Nếu được phân loại là nền tảng thương mại điện tử trung gian, nền tảng có trách nhiệm xác thực điện tử và công khai danh tính cùng thông tin liên hệ của người bán [1] [2].

- Nền tảng tiến hành xác thực điện tử danh tính của người bán hoặc người cho thuê theo quy định [1] [2].
- Nền tảng thực hiện công khai danh tính và thông tin liên hệ của người bán hoặc người cho thuê trên hệ thống [1] [2].
- Nền tảng kiểm soát và kiểm duyệt nội dung tin đăng của người bán trước khi hiển thị [1] [2].
- Nền tảng duy trì khả năng truy cập đối với dữ liệu tin đăng theo thời hạn quy định [1].
- Trường hợp có tính năng đặt hàng trực tuyến, nền tảng cung cấp thông tin hỗ trợ giao dịch và xử lý khi nội dung cung cấp không đúng cam kết [1].

Quy định theo Luật 122/2025/QH15 áp dụng từ ngày 01/07/2026 và văn bản không tự quyết định hệ thống tìm trọ thuộc loại nền tảng nào [4].
Khuyến nghị người dùng lập bản đồ từng luồng chức năng để đối chiếu chính xác phân loại nền tảng và kiểm tra bản gốc văn bản [4].

Để áp dụng vào trường hợp của bạn:
- Nền tảng tìm trọ bạn đang dùng có chức năng đặt cọc hoặc thanh toán trực tuyến không?
- Hệ thống đăng tin đó đã được xác định cụ thể là nền tảng thương mại điện tử trung gian hay chưa?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

Nguồn truy xuất của D (rank dùng trong trích dẫn):

- [1] Nghị-định-248-2026-NĐ-CP-trích-tuyển — Điều 18 — nền tảng trung gian
- [2] Luật-122-2025-QH15-trích-tuyển — Điều 17 — nền tảng trung gian
- [3] Luật-122-2025-QH15-trích-tuyển — Điều 1–3 — phạm vi, chủ thể, khái niệm nền tảng
- [4] Luật-122-2025-QH15-trích-tuyển — Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp

### Câu 28: Nếu người đăng yêu cầu chuyển cọc qua liên kết lạ, tôi nên kiểm tra những dấu hiệu nào trước khi trả tiền?

#### A — Gemini chatbot

Dưới đây là các khuyến cáo phòng ngừa rủi ro bạn nên lưu ý:

* **Khuyến nghị:** Cơ quan Công an khuyến cáo tuyệt đối không truy cập đường link lạ, quét mã QR không rõ nguồn gốc, không cài đặt ứng dụng theo hướng dẫn và không cung cấp mật khẩu, thông tin tài khoản hay mã OTP [1].
* **Khuyến nghị:** Cần trực tiếp đến xem phòng trọ, xác minh rõ danh tính chủ nhà hoặc người cho thuê; tuyệt đối không chuyển tiền đặt cọc khi chỉ trao đổi qua mạng hoặc điện thoại mà chưa gặp mặt, chưa kiểm chứng thông tin [2].
* Nếu nghi ngờ bị lừa đảo, bạn cần ngừng giao dịch, liên hệ ngân hàng khóa tài khoản nếu cần thiết, lưu giữ tin nhắn, chứng từ chuyển tiền và trình báo cơ quan Công an gần nhất [1], [2].

*Lưu ý: Đây là thông tin tham khảo, không thay thế tư vấn pháp lý chuyên nghiệp.*

#### B — Gemini phân tích + Qwen trích nguồn

Các đoạn trả lời trực tiếp trong nguồn:

- online_warning-Bo-Cong-an-20261003 — trích đoạn: “KHUYẾN CÁO PHÒNG NGỪA LỪA ĐẢO — KHÔNG PHẢI ĐIỀU LUẬT

Khuyến cáo của cơ quan Công an về lừa đảo mua hàng trực tuyến

Tuyệt đối không cung cấp thông tin tài khoản, mật khẩu, mã OTP; không truy cập đường link lạ, quét mã QR không rõ nguồn gốc; không cài đặt ứng dụng theo hướng dẫn của người gọi và không chuyển tiền để nhận hoàn tiền, bồi thường.

Trường hợp nghi ngờ bị lừa đảo, người dân cần ngừng ngay giao dịch, liên hệ ngân hàng để khóa tài khoản khi cần thiết, lưu giữ tin nhắn, số điện thoại, lịch sử giao dịch và trình báo cơ quan Công an gần nhất để được hỗ trợ.” [1].

- rental_warning-Bo-Cong-an-20261003 — trích đoạn: “KHUYẾN CÁO PHÒNG NGỪA LỪA ĐẢO — KHÔNG PHẢI ĐIỀU LUẬT

Khuyến cáo của cơ quan Công an về đặt cọc thuê nhà qua mạng

Để phòng ngừa loại tội phạm này, cơ quan Công an khuyến cáo người dân cần trực tiếp đến xem phòng trọ, xác minh rõ danh tính chủ nhà hoặc người cho thuê trước khi giao dịch; tuyệt đối không chuyển tiền đặt cọc khi trao đổi qua mạng xã hội hoặc điện thoại mà chưa gặp mặt, chưa kiểm chứng thông tin. Khi phát hiện dấu hiệu nghi vấn hoặc đã trở thành nạn nhân của hành vi lừa đảo, người dân cần nhanh chóng lưu giữ các tài liệu, tin nhắn, chứng từ chuyển tiền và trình báo cơ quan Công an để được hỗ trợ, xử lý kịp thời.” [2].

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng, hiệu lực và bản gốc.

#### C — Đáp án bạn gửi

**Dấu hiệu cảnh báo lừa đảo chiếm đoạt tài khoản:**
1. Bắt nhấn vào liên kết lạ (đường link rút gọn như bit.ly, link giả mạo ngân hàng, cổng thanh toán giả) để "xác nhận giữ phòng" hoặc "nhận mã hoàn cọc".
2. Yêu cầu nhập số tài khoản ngân hàng, mật khẩu internet banking hoặc **mã OTP**.
3. Hối thúc dồn dập: "Đang có nhiều người muốn thuê, chuyển ngay trong 15 phút nếu không sẽ mất phòng".
*Quy tắc an toàn:* Tuyệt đối không bao giờ nhấp link lạ hoặc cung cấp mã OTP cho bất kỳ ai.

#### D — Chatbot dạng agent

Khuyến nghị người dân không truy cập vào các đường link lạ và không chuyển tiền đặt cọc khi chưa trực tiếp gặp mặt hoặc chưa kiểm chứng thông tin của người cho thuê [1] [2].

- Khuyến nghị tuyệt đối không truy cập vào các đường link lạ hay quét mã QR không rõ nguồn gốc từ người đăng [1].
- Khuyến nghị người dân trực tiếp đến xem phòng trọ và xác minh rõ danh tính của chủ nhà hoặc người cho thuê trước khi thực hiện giao dịch [2].
- Khuyến nghị tuyệt đối không chuyển tiền đặt cọc khi chỉ trao đổi qua mạng xã hội hoặc điện thoại mà chưa gặp mặt và chưa kiểm chứng thông tin [2].
- Khuyến nghị ngừng ngay giao dịch và liên hệ ngân hàng khóa tài khoản nếu nghi ngờ bị lừa đảo khi nhận yêu cầu chuyển tiền [1].
- Khuyến nghị lưu giữ toàn bộ tin nhắn, số điện thoại, lịch sử giao dịch và trình báo ngay cho cơ quan Công an gần nhất khi phát hiện dấu hiệu nghi vấn [1] [2].

Nguồn tài liệu là khuyến cáo phòng ngừa tội phạm của cơ quan Công an chứ không phải điều luật quy định cụ thể về dấu hiệu nhận biết chi tiết của liên kết lạ [1] [2].

Để áp dụng vào trường hợp của bạn:
- Bạn đã trực tiếp đến xem phòng trọ và gặp mặt để kiểm chứng danh tính của người cho thuê chưa?
- Người đăng có yêu cầu bạn cung cấp thông tin tài khoản, mật khẩu hoặc mã OTP qua liên kết đó không?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

Nguồn truy xuất của D (rank dùng trong trích dẫn):

- [1] online_warning-Bo-Cong-an-20261003
- [2] rental_warning-Bo-Cong-an-20261003
- [3] Nghị-định-248-2026-NĐ-CP-trích-tuyển — Điều 18 — nền tảng trung gian

### Câu 29: Chủ trọ có thể yêu cầu tôi cung cấp những thông tin cá nhân nào để làm hợp đồng và đăng ký cư trú?

#### A — Gemini chatbot

Các căn cứ liên quan tìm được trong kho (trích nguyên đoạn):

- Luat-68-2020-QH14-doi-chieu-20261003 — Điều 28. Hồ sơ, thủ tục đăng ký tạm trú, gia hạn tạm trú | Khoản 1: “1. Hồ sơ đăng ký tạm trú bao gồm: a) Tờ khai thay đổi thông tin cư trú; đối với người đăng ký tạm trú là người chưa thành niên thì trong tờ khai phải ghi rõ ý kiến đồng ý của cha, mẹ hoặc người giám hộ, trừ trường hợp đã có ý kiến đồng ý bằng văn bản;” [1].

- Luật-91-2025-QH15 — Điều 9. Sự đồng ý của chủ thể dữ liệu cá nhân | Khoản 1: “1. Sự đồng ý của chủ thể dữ liệu cá nhân là việc chủ thể dữ liệu cá nhân cho phép xử lý dữ liệu cá nhân của mình, trừ trường hợp pháp luật có quy định khác.” [2].

Đây là câu trả lời một phần từ nguồn; chưa kết luận cách áp dụng cho tình huống riêng của bạn. Cần đối chiếu điều kiện, hiệu lực và bản gốc.

#### B — Gemini phân tích + Qwen trích nguồn

Các đoạn trả lời trực tiếp trong nguồn:

- Luật-91-2025-QH15 — Điều 9. Sự đồng ý của chủ thể dữ liệu cá nhân | Khoản 1: “1. Sự đồng ý của chủ thể dữ liệu cá nhân là việc chủ thể dữ liệu cá nhân cho phép xử lý dữ liệu cá nhân của mình, trừ trường hợp pháp luật có quy định khác.” [2].

- Luật-91-2025-QH15 — Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp: “Điều 38. Hiệu lực thi hành
Điều 38. Hiệu lực thi hành

Điều 38. Hiệu lực thi hành | Khoản 1
1. Luật này có hiệu lực thi hành từ ngày 01 tháng 01 năm 2026.

Điều 38. Hiệu lực thi hành | Khoản 2
2. Doanh nghiệp nhỏ, doanh nghiệp khởi nghiệp được quyền lựa chọn thực hiện hoặc không thực hiện quy định tại Điều 21, Điều 22 và khoản 2 Điều 33 của Luật này trong thời gian 05 năm kể từ ngày Luật này có hiệu lực thi hành, trừ doanh nghiệp nhỏ, doanh nghiệp khởi nghiệp kinh doanh dịch vụ xử lý dữ liệu cá nhân, trực tiếp xử lý dữ liệu cá nhân nhạy cảm hoặc xử lý dữ liệu cá nhân của số lượng lớn chủ thể dữ liệu cá nhân.

Điều 38. Hiệu lực thi hành | Khoản 3
3. Hộ kinh doanh, doanh nghiệp siêu nhỏ không phải thực hiện quy định tại Điều 21, Điều 22 và khoản 2 Điều 33 của Luật này, trừ hộ kinh doanh, doanh nghiệp siêu nhỏ kinh doanh dịch vụ xử lý dữ liệu cá nhân, trực tiếp xử lý dữ liệu cá nhân nhạy cảm hoặc xử lý dữ liệu cá nhân của số lượng lớn chủ thể dữ liệu cá nhân.

Điều 38. Hiệu lực thi hành | Khoản 4
4. Chính phủ quy định chi tiết khoản 2 và khoản 3 Điều này.

Điều 39. Quy định chuyển tiếp
Điều 39. Quy định chuyển tiếp

Điều 39. Quy định chuyển tiếp | Khoản 1
1. Hoạt động xử lý dữ liệu cá nhân đang thực hiện mà đã được chủ thể dữ liệu cá nhân đồng ý hoặc theo thỏa thuận theo quy định của Nghị định số 13/2023/NĐ-CP ngày 17 tháng 4 năm 2023 của Chính phủ trước ngày Luật này có hiệu lực thi hành thì tiếp tục thực hiện, không phải xin đồng ý lại hoặc thỏa thuận lại.

Điều 39. Quy định chuyển tiếp | Khoản 2
2. Hồ sơ đánh giá tác động xử lý dữ liệu cá nhân, hồ sơ đánh giá tác động chuyển dữ liệu cá nhân ra nước ngoài theo quy định của Nghị định số 13/2023/NĐ-CP ngày 17 tháng 4 năm 2023 của Chính phủ đã được cơ quan chuyên trách bảo vệ dữ liệu cá nhân tiếp nhận trước ngày Luật này có hiệu lực thi hành thì tiếp tục được sử dụng và không phải lập hồ sơ đánh giá tác động xử lý dữ liệu cá nhân, hồ sơ đánh giá tác động chuyển dữ liệu cá nhân xuyên biên giới theo quy định của Luật này; việc cập nhật các hồ sơ đã lập nêu trên sau ngày Luật này có hiệu lực thi hành thì thực hiện theo quy định của Luật này.

__________________________________________________________________________

Luật này được Quốc hội nước Cộng hòa xã hội chủ nghĩa Việt Nam khóa XV, kỳ họp thứ 9 thông qua ngày 26 tháng 6 năm 2025.

CHỦ TỊCH QUỐC HỘI

Trần Thanh Mẫn” [4].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng; cần đối chiếu phần còn thiếu.

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng, hiệu lực và bản gốc.

#### C — Đáp án bạn gửi

- Chủ trọ chỉ có quyền yêu cầu các **thông tin cơ bản cần thiết phục vụ cho việc lập hợp đồng và đăng ký tạm trú** theo quy định pháp luật: Họ và tên, Ngày tháng năm sinh, Số CCCD/Định danh cá nhân, Địa chỉ thường trú, Số điện thoại liên hệ, Giấy xác nhận là sinh viên (nếu có chính sách ưu đãi).
- Chủ trọ **không có quyền** đòi hỏi các thông tin nhạy cảm như: Mật khẩu mạng xã hội, thông tin tài khoản ngân hàng, thu nhập chi tiết của cha mẹ hay lịch sử duyệt web.

#### D — Chatbot dạng agent

Các đoạn trả lời trực tiếp trong nguồn:

- Luật-91-2025-QH15 — Điều 9. Sự đồng ý của chủ thể dữ liệu cá nhân | Khoản 1: “1. Sự đồng ý của chủ thể dữ liệu cá nhân là việc chủ thể dữ liệu cá nhân cho phép xử lý dữ liệu cá nhân của mình, trừ trường hợp pháp luật có quy định khác.” [2].

- Luật-91-2025-QH15 — Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp: “Điều 38. Hiệu lực thi hành
Điều 38. Hiệu lực thi hành

Điều 38. Hiệu lực thi hành | Khoản 1
1. Luật này có hiệu lực thi hành từ ngày 01 tháng 01 năm 2026.

Điều 38. Hiệu lực thi hành | Khoản 2
2. Doanh nghiệp nhỏ, doanh nghiệp khởi nghiệp được quyền lựa chọn thực hiện hoặc không thực hiện quy định tại Điều 21, Điều 22 và khoản 2 Điều 33 của Luật này trong thời gian 05 năm kể từ ngày Luật này có hiệu lực thi hành, trừ doanh nghiệp nhỏ, doanh nghiệp khởi nghiệp kinh doanh dịch vụ xử lý dữ liệu cá nhân, trực tiếp xử lý dữ liệu cá nhân nhạy cảm hoặc xử lý dữ liệu cá nhân của số lượng lớn chủ thể dữ liệu cá nhân.

Điều 38. Hiệu lực thi hành | Khoản 3
3. Hộ kinh doanh, doanh nghiệp siêu nhỏ không phải thực hiện quy định tại Điều 21, Điều 22 và khoản 2 Điều 33 của Luật này, trừ hộ kinh doanh, doanh nghiệp siêu nhỏ kinh doanh dịch vụ xử lý dữ liệu cá nhân, trực tiếp xử lý dữ liệu cá nhân nhạy cảm hoặc xử lý dữ liệu cá nhân của số lượng lớn chủ thể dữ liệu cá nhân.

Điều 38. Hiệu lực thi hành | Khoản 4
4. Chính phủ quy định chi tiết khoản 2 và khoản 3 Điều này.

Điều 39. Quy định chuyển tiếp
Điều 39. Quy định chuyển tiếp

Điều 39. Quy định chuyển tiếp | Khoản 1
1. Hoạt động xử lý dữ liệu cá nhân đang thực hiện mà đã được chủ thể dữ liệu cá nhân đồng ý hoặc theo thỏa thuận theo quy định của Nghị định số 13/2023/NĐ-CP ngày 17 tháng 4 năm 2023 của Chính phủ trước ngày Luật này có hiệu lực thi hành thì tiếp tục thực hiện, không phải xin đồng ý lại hoặc thỏa thuận lại.

Điều 39. Quy định chuyển tiếp | Khoản 2
2. Hồ sơ đánh giá tác động xử lý dữ liệu cá nhân, hồ sơ đánh giá tác động chuyển dữ liệu cá nhân ra nước ngoài theo quy định của Nghị định số 13/2023/NĐ-CP ngày 17 tháng 4 năm 2023 của Chính phủ đã được cơ quan chuyên trách bảo vệ dữ liệu cá nhân tiếp nhận trước ngày Luật này có hiệu lực thi hành thì tiếp tục được sử dụng và không phải lập hồ sơ đánh giá tác động xử lý dữ liệu cá nhân, hồ sơ đánh giá tác động chuyển dữ liệu cá nhân xuyên biên giới theo quy định của Luật này; việc cập nhật các hồ sơ đã lập nêu trên sau ngày Luật này có hiệu lực thi hành thì thực hiện theo quy định của Luật này.

__________________________________________________________________________

Luật này được Quốc hội nước Cộng hòa xã hội chủ nghĩa Việt Nam khóa XV, kỳ họp thứ 9 thông qua ngày 26 tháng 6 năm 2025.

CHỦ TỊCH QUỐC HỘI

Trần Thanh Mẫn” [4].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng; cần đối chiếu phần còn thiếu.

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng, hiệu lực và bản gốc.

Nguồn truy xuất của D (rank dùng trong trích dẫn):

- [1] Luat-68-2020-QH14-doi-chieu-20261003 — Điều 28. Hồ sơ, thủ tục đăng ký tạm trú, gia hạn tạm trú | Khoản 1
- [2] Luật-91-2025-QH15 — Điều 9. Sự đồng ý của chủ thể dữ liệu cá nhân | Khoản 1
- [3] 2026_204_79_VBHN-VPQH — Điều 163. Hợp đồng về nhà ở | Khoản 1
- [4] Luật-91-2025-QH15 — Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp

Lý do giới hạn/fallback của D:

- Gemini phân tích câu hỏi chưa khả dụng (ValidationError); dùng định tuyến chủ đề dự phòng.
- Kết luận hoặc số liệu chưa gắn trích dẫn trực tiếp.
- Bản tổng hợp chưa được nguồn xác nhận sau lần sửa; dùng trích đoạn Qwen đã chọn.
- Phản hồi chưa đáp ứng đầy đủ yêu cầu chính; đánh dấu theo nội dung thay vì provider.

### Câu 30: Ảnh căn cước công dân của người thuê được lưu và sử dụng như thế nào?

#### A — Gemini chatbot

Mình tìm thấy tài liệu liên quan nhưng chưa tổng hợp được kết luận đáng tin cậy. [1] [2] [3] [4]

- Mở Nguồn tham khảo bên dưới để xem trích đoạn.
- Kiểm tra điều kiện áp dụng và hiệu lực văn bản.

Thông tin tham khảo, không thay thế tư vấn pháp lý.

#### B — Gemini phân tích + Qwen trích nguồn

Các đoạn trả lời trực tiếp trong nguồn:

- Luật-91-2025-QH15 — Điều 3. Nguyên tắc bảo vệ dữ liệu cá nhân | Khoản 2: “2. Chỉ được thu thập, xử lý dữ liệu cá nhân đúng phạm vi, mục đích cụ thể, rõ ràng, bảo đảm tuân thủ quy định của pháp luật.” [1].

- Luật-91-2025-QH15 — Điều 9. Sự đồng ý của chủ thể dữ liệu cá nhân | Khoản 2: “2. Sự đồng ý của chủ thể dữ liệu cá nhân chỉ có hiệu lực khi dựa trên sự tự nguyện và biết rõ các thông tin sau đây:

2. Sự đồng ý của chủ thể dữ liệu cá nhân chỉ có hiệu lực khi dựa trên sự tự nguyện và biết rõ các thông tin sau đây: a) Loại dữ liệu cá nhân được xử lý, mục đích xử lý dữ liệu cá nhân;

2. Sự đồng ý của chủ thể dữ liệu cá nhân chỉ có hiệu lực khi dựa trên sự tự nguyện và biết rõ các thông tin sau đây: b) Bên kiểm soát dữ liệu cá nhân hoặc bên kiểm soát và xử lý dữ liệu cá nhân;

2. Sự đồng ý của chủ thể dữ liệu cá nhân chỉ có hiệu lực khi dựa trên sự tự nguyện và biết rõ các thông tin sau đây: c) Các quyền, nghĩa vụ của chủ thể dữ liệu cá nhân.” [2].

- Luật-91-2025-QH15 — Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp: “Điều 38. Hiệu lực thi hành
Điều 38. Hiệu lực thi hành

Điều 38. Hiệu lực thi hành | Khoản 1
1. Luật này có hiệu lực thi hành từ ngày 01 tháng 01 năm 2026.

Điều 38. Hiệu lực thi hành | Khoản 2
2. Doanh nghiệp nhỏ, doanh nghiệp khởi nghiệp được quyền lựa chọn thực hiện hoặc không thực hiện quy định tại Điều 21, Điều 22 và khoản 2 Điều 33 của Luật này trong thời gian 05 năm kể từ ngày Luật này có hiệu lực thi hành, trừ doanh nghiệp nhỏ, doanh nghiệp khởi nghiệp kinh doanh dịch vụ xử lý dữ liệu cá nhân, trực tiếp xử lý dữ liệu cá nhân nhạy cảm hoặc xử lý dữ liệu cá nhân của số lượng lớn chủ thể dữ liệu cá nhân.

Điều 38. Hiệu lực thi hành | Khoản 3
3. Hộ kinh doanh, doanh nghiệp siêu nhỏ không phải thực hiện quy định tại Điều 21, Điều 22 và khoản 2 Điều 33 của Luật này, trừ hộ kinh doanh, doanh nghiệp siêu nhỏ kinh doanh dịch vụ xử lý dữ liệu cá nhân, trực tiếp xử lý dữ liệu cá nhân nhạy cảm hoặc xử lý dữ liệu cá nhân của số lượng lớn chủ thể dữ liệu cá nhân.

Điều 38. Hiệu lực thi hành | Khoản 4
4. Chính phủ quy định chi tiết khoản 2 và khoản 3 Điều này.

Điều 39. Quy định chuyển tiếp
Điều 39. Quy định chuyển tiếp

Điều 39. Quy định chuyển tiếp | Khoản 1
1. Hoạt động xử lý dữ liệu cá nhân đang thực hiện mà đã được chủ thể dữ liệu cá nhân đồng ý hoặc theo thỏa thuận theo quy định của Nghị định số 13/2023/NĐ-CP ngày 17 tháng 4 năm 2023 của Chính phủ trước ngày Luật này có hiệu lực thi hành thì tiếp tục thực hiện, không phải xin đồng ý lại hoặc thỏa thuận lại.

Điều 39. Quy định chuyển tiếp | Khoản 2
2. Hồ sơ đánh giá tác động xử lý dữ liệu cá nhân, hồ sơ đánh giá tác động chuyển dữ liệu cá nhân ra nước ngoài theo quy định của Nghị định số 13/2023/NĐ-CP ngày 17 tháng 4 năm 2023 của Chính phủ đã được cơ quan chuyên trách bảo vệ dữ liệu cá nhân tiếp nhận trước ngày Luật này có hiệu lực thi hành thì tiếp tục được sử dụng và không phải lập hồ sơ đánh giá tác động xử lý dữ liệu cá nhân, hồ sơ đánh giá tác động chuyển dữ liệu cá nhân xuyên biên giới theo quy định của Luật này; việc cập nhật các hồ sơ đã lập nêu trên sau ngày Luật này có hiệu lực thi hành thì thực hiện theo quy định của Luật này.

__________________________________________________________________________

Luật này được Quốc hội nước Cộng hòa xã hội chủ nghĩa Việt Nam khóa XV, kỳ họp thứ 9 thông qua ngày 26 tháng 6 năm 2025.

CHỦ TỊCH QUỐC HỘI

Trần Thanh Mẫn” [4].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng; cần đối chiếu phần còn thiếu.

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng, hiệu lực và bản gốc.

#### C — Đáp án bạn gửi

Căn cứ theo **Nghị định 13/2023/NĐ-CP**:
- Ảnh/bản sao CCCD chỉ được phép sử dụng **cho mục đích hợp pháp đã được thông báo trước** (lưu hồ sơ thuê trọ và nộp cho Công an phường để đăng ký tạm trú).
- Bên lưu trữ (chủ trọ) có trách nhiệm áp dụng các biện pháp bảo mật, không được làm rò rỉ hoặc chuyển giao cho bên thứ ba khi chưa có sự đồng ý của chủ thể dữ liệu.
*Mẹo cho sinh viên:* Khi gửi ảnh CCCD, hãy chèn dòng chữ chìm (watermark) đè lên ảnh: *"Chỉ sử dụng để đăng ký tạm trú tại phòng trọ X - ngày..."*.

#### D — Chatbot dạng agent

Chưa đủ căn cứ từ nguồn để quy định cụ thể quy trình lưu trữ ảnh căn cước công dân của người thuê, nhưng việc thu thập và xử lý phải có sự đồng ý của chủ thể dữ liệu và tuân thủ đúng phạm vi, mục đích rõ ràng [1] [3].

- Bên thu thập phải lấy sự đồng ý của chủ thể dữ liệu cá nhân trước khi thu thập ảnh căn cước công dân, trừ trường hợp pháp luật có quy định khác [3].
- Bảo đảm người thuê tự nguyện và biết rõ loại dữ liệu, mục đích xử lý, bên kiểm soát xử lý dữ liệu cùng các quyền và nghĩa vụ liên quan để sự đồng ý có hiệu lực [2].
- Chỉ thực hiện xử lý dữ liệu đúng phạm vi, mục đích cụ thể đã xác định và bảo đảm tuân thủ quy định pháp luật [1].
- Khuyến nghị người thuê kiểm tra thỏa thuận về mục đích sử dụng và biện pháp bảo quản ảnh căn cước công dân khi giao cho bên cho thuê [1] [2].

Nguồn trích dẫn thuộc văn bản có hiệu lực từ ngày 01 tháng 01 năm 2026 và chưa quy định cụ thể thời hạn hay phương thức lưu trữ chi tiết cho việc thuê trọ [4].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng.

Để áp dụng vào trường hợp của bạn:
- Bên cho thuê yêu cầu cung cấp ảnh căn cước công dân nhằm mục đích gì?
- Hai bên đã có thỏa thuận hoặc cam kết nào về việc bảo mật và lưu giữ ảnh căn cước chưa?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

Nguồn truy xuất của D (rank dùng trong trích dẫn):

- [1] Luật-91-2025-QH15 — Điều 3. Nguyên tắc bảo vệ dữ liệu cá nhân | Khoản 2
- [2] Luật-91-2025-QH15 — Điều 9. Sự đồng ý của chủ thể dữ liệu cá nhân | Khoản 2
- [3] Luật-91-2025-QH15 — Điều 11. Thu thập, phân tích, tổng hợp dữ liệu cá nhân | Khoản 1
- [4] Luật-91-2025-QH15 — Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp

Lý do giới hạn/fallback của D:

- Phản hồi chưa đáp ứng đầy đủ yêu cầu chính; đánh dấu theo nội dung thay vì provider.

### Câu 31: Chủ trọ có được đăng công khai ảnh giấy tờ hoặc số điện thoại của tôi không?

#### A — Gemini chatbot

Các căn cứ liên quan tìm được trong kho (trích nguyên đoạn):

- Luật-91-2025-QH15 — Điều 16. Công khai dữ liệu cá nhân | Khoản 4: “4. Hình thức công khai dữ liệu cá nhân, bao gồm: đăng tải dữ liệu trên trang thông tin điện tử, cổng thông tin điện tử, phương tiện thông tin đại chúng và các hình thức khác theo quy định của pháp luật.” [2].

- Luật-91-2025-QH15 — Điều 16. Công khai dữ liệu cá nhân | Khoản 2: “2. Dữ liệu cá nhân chỉ được công khai trong các trường hợp sau đây: a) Khi có sự đồng ý của chủ thể dữ liệu cá nhân;” [1].

Đây là câu trả lời một phần từ nguồn; chưa kết luận cách áp dụng cho tình huống riêng của bạn. Cần đối chiếu điều kiện, hiệu lực và bản gốc.

#### B — Gemini phân tích + Qwen trích nguồn

Các đoạn trả lời trực tiếp trong nguồn:

- Luật-91-2025-QH15 — Điều 16. Công khai dữ liệu cá nhân | Khoản 2: “2. Dữ liệu cá nhân chỉ được công khai trong các trường hợp sau đây:

2. Dữ liệu cá nhân chỉ được công khai trong các trường hợp sau đây: a) Khi có sự đồng ý của chủ thể dữ liệu cá nhân;

2. Dữ liệu cá nhân chỉ được công khai trong các trường hợp sau đây: b) Thực hiện theo quy định của pháp luật;

2. Dữ liệu cá nhân chỉ được công khai trong các trường hợp sau đây: c) Trường hợp quy định tại điểm b khoản 1 Điều 19 của Luật này;

2. Dữ liệu cá nhân chỉ được công khai trong các trường hợp sau đây: d) Thực hiện nghĩa vụ theo hợp đồng.” [1].

- Luật-91-2025-QH15 — Điều 3. Nguyên tắc bảo vệ dữ liệu cá nhân | Khoản 2: “2. Chỉ được thu thập, xử lý dữ liệu cá nhân đúng phạm vi, mục đích cụ thể, rõ ràng, bảo đảm tuân thủ quy định của pháp luật.” [3].

- Luật-91-2025-QH15 — Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp: “Điều 38. Hiệu lực thi hành
Điều 38. Hiệu lực thi hành

Điều 38. Hiệu lực thi hành | Khoản 1
1. Luật này có hiệu lực thi hành từ ngày 01 tháng 01 năm 2026.

Điều 38. Hiệu lực thi hành | Khoản 2
2. Doanh nghiệp nhỏ, doanh nghiệp khởi nghiệp được quyền lựa chọn thực hiện hoặc không thực hiện quy định tại Điều 21, Điều 22 và khoản 2 Điều 33 của Luật này trong thời gian 05 năm kể từ ngày Luật này có hiệu lực thi hành, trừ doanh nghiệp nhỏ, doanh nghiệp khởi nghiệp kinh doanh dịch vụ xử lý dữ liệu cá nhân, trực tiếp xử lý dữ liệu cá nhân nhạy cảm hoặc xử lý dữ liệu cá nhân của số lượng lớn chủ thể dữ liệu cá nhân.

Điều 38. Hiệu lực thi hành | Khoản 3
3. Hộ kinh doanh, doanh nghiệp siêu nhỏ không phải thực hiện quy định tại Điều 21, Điều 22 và khoản 2 Điều 33 của Luật này, trừ hộ kinh doanh, doanh nghiệp siêu nhỏ kinh doanh dịch vụ xử lý dữ liệu cá nhân, trực tiếp xử lý dữ liệu cá nhân nhạy cảm hoặc xử lý dữ liệu cá nhân của số lượng lớn chủ thể dữ liệu cá nhân.

Điều 38. Hiệu lực thi hành | Khoản 4
4. Chính phủ quy định chi tiết khoản 2 và khoản 3 Điều này.

Điều 39. Quy định chuyển tiếp
Điều 39. Quy định chuyển tiếp

Điều 39. Quy định chuyển tiếp | Khoản 1
1. Hoạt động xử lý dữ liệu cá nhân đang thực hiện mà đã được chủ thể dữ liệu cá nhân đồng ý hoặc theo thỏa thuận theo quy định của Nghị định số 13/2023/NĐ-CP ngày 17 tháng 4 năm 2023 của Chính phủ trước ngày Luật này có hiệu lực thi hành thì tiếp tục thực hiện, không phải xin đồng ý lại hoặc thỏa thuận lại.

Điều 39. Quy định chuyển tiếp | Khoản 2
2. Hồ sơ đánh giá tác động xử lý dữ liệu cá nhân, hồ sơ đánh giá tác động chuyển dữ liệu cá nhân ra nước ngoài theo quy định của Nghị định số 13/2023/NĐ-CP ngày 17 tháng 4 năm 2023 của Chính phủ đã được cơ quan chuyên trách bảo vệ dữ liệu cá nhân tiếp nhận trước ngày Luật này có hiệu lực thi hành thì tiếp tục được sử dụng và không phải lập hồ sơ đánh giá tác động xử lý dữ liệu cá nhân, hồ sơ đánh giá tác động chuyển dữ liệu cá nhân xuyên biên giới theo quy định của Luật này; việc cập nhật các hồ sơ đã lập nêu trên sau ngày Luật này có hiệu lực thi hành thì thực hiện theo quy định của Luật này.

__________________________________________________________________________

Luật này được Quốc hội nước Cộng hòa xã hội chủ nghĩa Việt Nam khóa XV, kỳ họp thứ 9 thông qua ngày 26 tháng 6 năm 2025.

CHỦ TỊCH QUỐC HỘI

Trần Thanh Mẫn” [4].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng; cần đối chiếu phần còn thiếu.

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng, hiệu lực và bản gốc.

#### C — Đáp án bạn gửi

**Hoàn toàn không được phép và là hành vi vi phạm pháp luật.**
- Đăng công khai hình ảnh cá nhân, số CCCD hoặc số điện thoại lên mạng xã hội (kể cả với lý do đòi nợ tiền phòng hoặc bóc phốt) là hành vi **xâm phạm quyền về đời sống riêng tư, bí mật cá nhân** theo Điều 38 BLDS 2015 và vi phạm Nghị định 13/2023/NĐ-CP.
- Người có hành vi này có thể bị xử phạt hành chính từ **10.000.000 đến 20.000.000 đồng** theo Điều 102 Nghị định 15/2020/NĐ-CP và phải bồi thường thiệt hại danh dự, nhân phẩm cho nạn nhân.

#### D — Chatbot dạng agent

Chủ trọ chỉ được công khai dữ liệu cá nhân khi có sự đồng ý của bạn, thực hiện theo quy định pháp luật, thực hiện nghĩa vụ theo hợp đồng hoặc trường hợp luật định khác [1].

- Khuyến nghị kiểm tra hợp đồng thuê trọ xem có điều khoản thỏa thuận cho phép công khai thông tin cá nhân hay không [1].
- Khuyến nghị rà soát xem bạn đã từng thể hiện sự đồng ý cho chủ trọ đăng tải thông tin cá nhân trước đó hay chưa [1].

Quy định về việc công khai dữ liệu cá nhân theo văn bản này có hiệu lực thi hành từ ngày 01 tháng 01 năm 2026 [4].
Hoạt động xử lý dữ liệu đang thực hiện đã được chủ thể dữ liệu đồng ý hoặc theo thỏa thuận trước ngày văn bản có hiệu lực thì tiếp tục thực hiện mà không phải xin đồng ý lại [4].

Chưa đủ căn cứ từ các đoạn này để kết luận toàn bộ yêu cầu hoặc tình huống riêng.

Để áp dụng vào trường hợp của bạn:
- Bạn đã từng ký thỏa thuận hoặc đồng ý cho chủ trọ đăng các thông tin đó chưa?
- Chủ trọ đăng ảnh giấy tờ và số điện thoại của bạn vào thời gian nào và vì mục đích gì?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

Nguồn truy xuất của D (rank dùng trong trích dẫn):

- [1] Luật-91-2025-QH15 — Điều 16. Công khai dữ liệu cá nhân | Khoản 2
- [2] Luật-91-2025-QH15 — Điều 3. Nguyên tắc bảo vệ dữ liệu cá nhân | Khoản 2
- [3] Luật-91-2025-QH15 — Điều 10. Yêu cầu rút lại sự đồng ý, yêu cầu hạn chế xử lý dữ liệu cá nhân | Khoản 1
- [4] Luật-91-2025-QH15 — Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp

Lý do giới hạn/fallback của D:

- Phản hồi chưa đáp ứng đầy đủ yêu cầu chính; đánh dấu theo nội dung thay vì provider.

### Câu 32: Nếu thông tin cá nhân của tôi bị chia sẻ sai mục đích, tôi nên yêu cầu xử lý như thế nào?

#### A — Gemini chatbot

Các căn cứ liên quan tìm được trong kho (trích nguyên đoạn):

- Nghị-định-356-2025-NĐ-CP — Điều 5. Thực hiện quyền của chủ thể dữ liệu cá nhân | Khoản 4: “4. Khi nhận được yêu cầu xóa dữ liệu cá nhân theo đúng thủ tục của chủ thể dữ liệu cá nhân, bên kiểm soát dữ liệu cá nhân, bên kiểm soát và xử lý dữ liệu cá nhân phải phản hồi trong thời hạn 02 ngày làm việc, cung cấp đầy đủ thông tin cho chủ thể dữ liệu cá nhân về thủ tục và thực hiện trong thời hạn 20 ngày. Trường hợp cần yêu cầu bên xử lý dữ liệu cá nhân, bên thứ ba cung cấp, xóa, hạn chế xử lý dữ liệu của chủ thể dữ liệu cá nhân thì thực hiện trong thời hạn 30 ngày.” [1].

- Nghị-định-356-2025-NĐ-CP — Điều 5. Thực hiện quyền của chủ thể dữ liệu cá nhân | Khoản 4: “Tùy theo tính chất, mức độ phức tạp của yêu cầu, trường hợp cần gia hạn thời gian xử lý thì kéo dài thêm tối đa 01 lần gia hạn trong thời hạn không quá 20 ngày, bên kiểm soát dữ liệu cá nhân, bên kiểm soát và xử lý dữ liệu cá nhân thông báo cho chủ thể dữ liệu cá nhân lý do cần gia hạn và chịu trách nhiệm chứng minh việc gia hạn là cần thiết, hợp lý.” [1].

Đây là câu trả lời một phần từ nguồn; chưa kết luận cách áp dụng cho tình huống riêng của bạn. Cần đối chiếu điều kiện, hiệu lực và bản gốc.

#### B — Gemini phân tích + Qwen trích nguồn

Các đoạn trả lời trực tiếp trong nguồn:

- Nghị-định-356-2025-NĐ-CP — Điều 5. Thực hiện quyền của chủ thể dữ liệu cá nhân | Khoản 4: “4. Khi nhận được yêu cầu xóa dữ liệu cá nhân theo đúng thủ tục của chủ thể dữ liệu cá nhân, bên kiểm soát dữ liệu cá nhân, bên kiểm soát và xử lý dữ liệu cá nhân phải phản hồi trong thời hạn 02 ngày làm việc, cung cấp đầy đủ thông tin cho chủ thể dữ liệu cá nhân về thủ tục và thực hiện trong thời hạn 20 ngày. Trường hợp cần yêu cầu bên xử lý dữ liệu cá nhân, bên thứ ba cung cấp, xóa, hạn chế xử lý dữ liệu của chủ thể dữ liệu cá nhân thì thực hiện trong thời hạn 30 ngày.

Tùy theo tính chất, mức độ phức tạp của yêu cầu, trường hợp cần gia hạn thời gian xử lý thì kéo dài thêm tối đa 01 lần gia hạn trong thời hạn không quá 20 ngày, bên kiểm soát dữ liệu cá nhân, bên kiểm soát và xử lý dữ liệu cá nhân thông báo cho chủ thể dữ liệu cá nhân lý do cần gia hạn và chịu trách nhiệm chứng minh việc gia hạn là cần thiết, hợp lý.” [1].

- Nghị-định-356-2025-NĐ-CP — Điều 5. Thực hiện quyền của chủ thể dữ liệu cá nhân | Khoản 2: “2. Khi nhận được yêu cầu rút lại sự đồng ý cho phép xử lý dữ liệu cá nhân, hạn chế xử lý dữ liệu cá nhân, phản đối xử lý dữ liệu cá nhân theo đúng thủ tục của chủ thể dữ liệu cá nhân, bên kiểm soát dữ liệu cá nhân, bên kiểm soát và xử lý dữ liệu cá nhân phải phản hồi trong thời hạn 02 ngày làm việc, cung cấp đầy đủ thông tin cho chủ thể dữ liệu cá nhân về thủ tục ngừng xử lý dữ liệu cá nhân và thực hiện trong thời hạn 15 ngày, trừ trường hợp xử lý dữ liệu cá nhân không cần sự đồng ý của chủ thể dữ liệu cá nhân theo quy định tại Điều 19 Luật Bảo vệ dữ liệu cá nhân.Trường hợp cần yêu cầu bên xử lý dữ liệu cá nhân, bên thứ ba ngừng xử lý dữ liệu cá nhân của chủ thể dữ liệu cá nhân thì thực hiện trong thời hạn 20 ngày.

Tùy theo tính chất, mức độ phức tạp của yêu cầu, trường hợp cần gia hạn thời gian xử lý thì kéo dài thêm tối đa 01 lần gia hạn trong thời hạn không quá 15 ngày, bên kiểm soát dữ liệu cá nhân, bên kiểm soát và xử lý dữ liệu cá nhân thông báo cho chủ thể dữ liệu cá nhân lý do cần gia hạn và chịu trách nhiệm chứng minh việc gia hạn là cần thiết, hợp lý.” [2].

- Nghị-định-356-2025-NĐ-CP — Điều 5. Thực hiện quyền của chủ thể dữ liệu cá nhân | Khoản 5: “5. Khi nhận được yêu cầu thực hiện các biện pháp, giải pháp bảo vệ dữ liệu cá nhân của mình theo đúng thủ tục của chủ thể dữ liệu cá nhân, cơ quan có thẩm quyền hoặc cơ quan, tổ chức, cá nhân liên quan đến xử lý dữ liệu cá nhân phải phản hồi trong thời hạn 02 ngày làm việc, cung cấp đầy đủ thông tin cho chủ thể dữ liệu cá nhân về thủ tục và thực hiện trong thời hạn 15 ngày.

Tùy theo tính chất, mức độ phức tạp của yêu cầu, trường hợp cần gia hạn thời gian xử lý thì kéo dài thêm tối đa 01 lần gia hạn trong thời hạn không quá 15 ngày, bên kiểm soát dữ liệu cá nhân, bên kiểm soát và xử lý dữ liệu cá nhân thông báo cho chủ thể dữ liệu cá nhân lý do cần gia hạn và chịu trách nhiệm chứng minh việc gia hạn là cần thiết, hợp lý.” [3].

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng, hiệu lực và bản gốc.

#### C — Đáp án bạn gửi

1. Gửi yêu cầu bằng văn bản/tin nhắn cho chủ trọ buộc gỡ bỏ ngay lập tức thông tin đã đăng tải.
2. Lập vi bằng hoặc chụp ảnh màn hình lưu giữ bằng chứng vi phạm.
3. Làm đơn tố cáo gửi đến Thanh tra Sở Thông tin và Truyền thông hoặc cơ quan Công an có thẩm quyền để can thiệp xử lý theo Nghị định 15/2020/NĐ-CP.

#### D — Chatbot dạng agent

Các đoạn trả lời trực tiếp trong nguồn:

- Nghị-định-356-2025-NĐ-CP — Điều 5. Thực hiện quyền của chủ thể dữ liệu cá nhân | Khoản 4: “4. Khi nhận được yêu cầu xóa dữ liệu cá nhân theo đúng thủ tục của chủ thể dữ liệu cá nhân, bên kiểm soát dữ liệu cá nhân, bên kiểm soát và xử lý dữ liệu cá nhân phải phản hồi trong thời hạn 02 ngày làm việc, cung cấp đầy đủ thông tin cho chủ thể dữ liệu cá nhân về thủ tục và thực hiện trong thời hạn 20 ngày. Trường hợp cần yêu cầu bên xử lý dữ liệu cá nhân, bên thứ ba cung cấp, xóa, hạn chế xử lý dữ liệu của chủ thể dữ liệu cá nhân thì thực hiện trong thời hạn 30 ngày.

Tùy theo tính chất, mức độ phức tạp của yêu cầu, trường hợp cần gia hạn thời gian xử lý thì kéo dài thêm tối đa 01 lần gia hạn trong thời hạn không quá 20 ngày, bên kiểm soát dữ liệu cá nhân, bên kiểm soát và xử lý dữ liệu cá nhân thông báo cho chủ thể dữ liệu cá nhân lý do cần gia hạn và chịu trách nhiệm chứng minh việc gia hạn là cần thiết, hợp lý.” [1].

- Nghị-định-356-2025-NĐ-CP — Điều 5. Thực hiện quyền của chủ thể dữ liệu cá nhân | Khoản 2: “2. Khi nhận được yêu cầu rút lại sự đồng ý cho phép xử lý dữ liệu cá nhân, hạn chế xử lý dữ liệu cá nhân, phản đối xử lý dữ liệu cá nhân theo đúng thủ tục của chủ thể dữ liệu cá nhân, bên kiểm soát dữ liệu cá nhân, bên kiểm soát và xử lý dữ liệu cá nhân phải phản hồi trong thời hạn 02 ngày làm việc, cung cấp đầy đủ thông tin cho chủ thể dữ liệu cá nhân về thủ tục ngừng xử lý dữ liệu cá nhân và thực hiện trong thời hạn 15 ngày, trừ trường hợp xử lý dữ liệu cá nhân không cần sự đồng ý của chủ thể dữ liệu cá nhân theo quy định tại Điều 19 Luật Bảo vệ dữ liệu cá nhân.Trường hợp cần yêu cầu bên xử lý dữ liệu cá nhân, bên thứ ba ngừng xử lý dữ liệu cá nhân của chủ thể dữ liệu cá nhân thì thực hiện trong thời hạn 20 ngày.

Tùy theo tính chất, mức độ phức tạp của yêu cầu, trường hợp cần gia hạn thời gian xử lý thì kéo dài thêm tối đa 01 lần gia hạn trong thời hạn không quá 15 ngày, bên kiểm soát dữ liệu cá nhân, bên kiểm soát và xử lý dữ liệu cá nhân thông báo cho chủ thể dữ liệu cá nhân lý do cần gia hạn và chịu trách nhiệm chứng minh việc gia hạn là cần thiết, hợp lý.” [2].

- Nghị-định-356-2025-NĐ-CP — Điều 5. Thực hiện quyền của chủ thể dữ liệu cá nhân | Khoản 3: “3. Khi nhận được yêu cầu xem, chỉnh sửa hoặc yêu cầu chỉnh sửa dữ liệu cá nhân, cung cấp dữ liệu cá nhân theo đúng thủ tục của chủ thể dữ liệu cá nhân, bên kiểm soát dữ liệu cá nhân, bên kiểm soát và xử lý dữ liệu cá nhân phải phản hồi trong thời hạn 02 ngày làm việc, cung cấp đầy đủ thông tin cho chủ thể dữ liệu cá nhân về thủ tục và thực hiện trong thời hạn 10 ngày. Trường hợp cần yêu cầu bên xử lý dữ liệu cá nhân, bên thứ ba chỉnh sửa dữ liệu cá nhân của chủ thể dữ liệu cá nhân thì thực hiện trong thời hạn 15 ngày.

Tùy theo tính chất, mức độ phức tạp của yêu cầu, trường hợp cần gia hạn thời gian xử lý thì kéo dài thêm tối đa 01 lần gia hạn trong thời hạn không quá 10 ngày, bên kiểm soát dữ liệu cá nhân, bên kiểm soát và xử lý dữ liệu cá nhân thông báo cho chủ thể dữ liệu cá nhân lý do cần gia hạn và chịu trách nhiệm chứng minh việc gia hạn là cần thiết, hợp lý.” [3].

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng, hiệu lực và bản gốc.

Nguồn truy xuất của D (rank dùng trong trích dẫn):

- [1] Nghị-định-356-2025-NĐ-CP — Điều 5. Thực hiện quyền của chủ thể dữ liệu cá nhân | Khoản 4
- [2] Nghị-định-356-2025-NĐ-CP — Điều 5. Thực hiện quyền của chủ thể dữ liệu cá nhân | Khoản 2
- [3] Nghị-định-356-2025-NĐ-CP — Điều 5. Thực hiện quyền của chủ thể dữ liệu cá nhân | Khoản 3

Lý do giới hạn/fallback của D:

- Số điều được khẳng định không khớp điều khoản của nguồn trích dẫn.
- Bản tổng hợp chưa được nguồn xác nhận sau lần sửa; dùng trích đoạn Qwen đã chọn.

### Câu 33: Người đăng yêu cầu đặt cọc trước nhưng không cho xem phòng: tôi nên kiểm tra những dấu hiệu rủi ro nào?

#### A — Gemini chatbot

Dưới đây là các dấu hiệu rủi ro và khuyến cáo cần lưu ý:

* **Dấu hiệu rủi ro và khuyến nghị kiểm tra:** Yêu cầu chuyển tiền đặt cọc qua mạng xã hội hoặc điện thoại khi chưa gặp mặt, chưa kiểm chứng thông tin và không cho xem phòng là dấu hiệu nghi vấn lừa đảo [1]. Khuyến nghị: người dân cần trực tiếp đến xem phòng trọ, xác minh rõ danh tính chủ nhà hoặc người cho thuê trước khi giao dịch; tuyệt đối không chuyển tiền cọc khi chưa gặp mặt, chưa kiểm chứng [1].
* **Quy định pháp luật liên quan:** Hành vi dùng thủ đoạn gian dối để chiếm đoạt tài sản của người khác có thể bị truy cứu trách nhiệm hình sự về Tội lừa đảo chiếm đoạt tài sản theo nguồn [2], Điều 174, Khoản 1, trang 1 (Văn-bản-hợp-nhất-135-VBHN-VPQH).
* **Xử lý khi nghi vấn:** Khi phát hiện dấu hiệu nghi vấn hoặc đã bị lừa đảo, cần nhanh chóng lưu giữ các tài liệu, tin nhắn, chứng từ chuyển tiền và trình báo cơ quan Công an để được hỗ trợ, xử lý kịp thời [1].

*Lưu ý: Đây là thông tin tham khảo, không thay thế tư vấn pháp lý chuyên nghiệp.*

#### B — Gemini phân tích + Qwen trích nguồn

Các đoạn trả lời trực tiếp trong nguồn:

- rental_warning-Bo-Cong-an-20261003 — trích đoạn: “KHUYẾN CÁO PHÒNG NGỪA LỪA ĐẢO — KHÔNG PHẢI ĐIỀU LUẬT

Khuyến cáo của cơ quan Công an về đặt cọc thuê nhà qua mạng

Để phòng ngừa loại tội phạm này, cơ quan Công an khuyến cáo người dân cần trực tiếp đến xem phòng trọ, xác minh rõ danh tính chủ nhà hoặc người cho thuê trước khi giao dịch; tuyệt đối không chuyển tiền đặt cọc khi trao đổi qua mạng xã hội hoặc điện thoại mà chưa gặp mặt, chưa kiểm chứng thông tin. Khi phát hiện dấu hiệu nghi vấn hoặc đã trở thành nạn nhân của hành vi lừa đảo, người dân cần nhanh chóng lưu giữ các tài liệu, tin nhắn, chứng từ chuyển tiền và trình báo cơ quan Công an để được hỗ trợ, xử lý kịp thời.” [1].

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng, hiệu lực và bản gốc.

#### C — Đáp án bạn gửi

Đây là **thủ đoạn lừa đảo chiếm đoạt tiền cọc kinh điển** nhắm vào tân sinh viên. Các dấu hiệu điển hình:
1. Viện cớ: "Chủ nhà đang ở xa / đi công tác / có nhiều người đang xếp hàng đòi cọc, muốn xem phòng thì phải cọc trước 200k - 500k để giữ chân".
2. Địa chỉ trọ mập mờ, hình ảnh phòng lung linh nhưng không trùng khớp với vị trí thực tế tại Cần Thơ.
3. Chỉ giao tiếp qua Zalo/Facebook ảo, từ chối gặp mặt trực tiếp hoặc gọi video xem phòng thực tế.
**Lời khuyên dứt khoát:** Không xem được phòng thực tế tận mắt $\rightarrow$ **Tuyệt đối không chuyển dù chỉ 1 đồng.**

#### D — Chatbot dạng agent

Theo khuyến cáo phòng ngừa lừa đảo của cơ quan Công an, việc yêu cầu chuyển tiền cọc qua mạng xã hội hoặc điện thoại khi chưa gặp mặt, chưa kiểm chứng thông tin và chưa xem phòng là dấu hiệu rủi ro cao [1].

- Khuyến nghị người thuê cần trực tiếp đến xem phòng trọ trước khi quyết định giao dịch [1].
- Khuyến nghị xác minh rõ danh tính chủ nhà hoặc người cho thuê trước khi chuyển tiền đặt cọc [1].
- Tuyệt đối không chuyển tiền đặt cọc khi chỉ trao đổi qua mạng xã hội hoặc điện thoại mà chưa gặp mặt và chưa kiểm chứng thông tin [1].
- Khuyến nghị nhanh chóng lưu giữ các tài liệu, tin nhắn, chứng từ chuyển tiền nếu phát hiện dấu hiệu nghi vấn lừa đảo [1].
- Khuyến nghị trình báo ngay cho cơ quan Công an để được hỗ trợ và xử lý kịp thời khi trở thành nạn nhân hoặc nghi ngờ bị lừa đảo [1].

Nội dung căn cứ là khuyến cáo phòng ngừa tội phạm của cơ quan Công an, không phải là điều khoản luật định bắt buộc [1].

Để áp dụng vào trường hợp của bạn:
- Bạn đã thực hiện việc chuyển tiền cọc hoặc ký văn bản cam kết nào với người đăng tin chưa?
- Bạn có lưu giữ được thông tin liên lạc, tài khoản ngân hàng hoặc nội dung tin nhắn trao đổi với người đăng tin không?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

Nguồn truy xuất của D (rank dùng trong trích dẫn):

- [1] rental_warning-Bo-Cong-an-20261003
- [2] Văn-bản-hợp-nhất-135-VBHN-VPQH — Điều 174. Tội lừa đảo chiếm đoạt tài sản | Khoản 1
- [3] Văn-bản-hợp-nhất-135-VBHN-VPQH — Điều 174. Tội lừa đảo chiếm đoạt tài sản

### Câu 34: Tôi đã chuyển cọc cho một tin trọ có dấu hiệu giả mạo; nên lưu lại bằng chứng gì và trình báo ở đâu?

#### A — Gemini chatbot

Căn cứ vào các tài liệu được cung cấp, bạn có thể thực hiện như sau:

* **Bằng chứng cần lưu lại:** Theo khuyến cáo của cơ quan Công an, khi phát hiện dấu hiệu nghi vấn hoặc đã là nạn nhân bị lừa đảo, người dân cần nhanh chóng lưu giữ các tài liệu, tin nhắn và chứng từ chuyển tiền [1].
* **Nơi tiếp nhận trình báo:** Theo khuyến cáo, người dân cần trình báo cơ quan Công an để được hỗ trợ, xử lý kịp thời [1]. Pháp luật quy định Cơ quan điều tra, Viện kiểm sát và cơ quan, tổ chức khác có trách nhiệm tiếp nhận tố giác, tin báo về tội phạm theo nguồn [3], Điều 145, Khoản 2, trang 1.
* **Hình thức nộp:** Có thể trực tiếp tố giác (cơ quan tiếp nhận phải lập biên bản, ghi sổ) hoặc gửi qua dịch vụ bưu chính, điện thoại, phương tiện thông tin khác theo nguồn [2], Điều 146, Khoản 1, trang 1.

*Lưu ý: Đây là thông tin tham khảo, không thay thế tư vấn pháp lý chuyên nghiệp.*

#### B — Gemini phân tích + Qwen trích nguồn

Các đoạn trả lời trực tiếp trong nguồn:

- rental_warning-Bo-Cong-an-20261003 — trích đoạn: “KHUYẾN CÁO PHÒNG NGỪA LỪA ĐẢO — KHÔNG PHẢI ĐIỀU LUẬT

Khuyến cáo của cơ quan Công an về đặt cọc thuê nhà qua mạng

Để phòng ngừa loại tội phạm này, cơ quan Công an khuyến cáo người dân cần trực tiếp đến xem phòng trọ, xác minh rõ danh tính chủ nhà hoặc người cho thuê trước khi giao dịch; tuyệt đối không chuyển tiền đặt cọc khi trao đổi qua mạng xã hội hoặc điện thoại mà chưa gặp mặt, chưa kiểm chứng thông tin. Khi phát hiện dấu hiệu nghi vấn hoặc đã trở thành nạn nhân của hành vi lừa đảo, người dân cần nhanh chóng lưu giữ các tài liệu, tin nhắn, chứng từ chuyển tiền và trình báo cơ quan Công an để được hỗ trợ, xử lý kịp thời.” [1].

- Văn-bản-hợp-nhất-17-VBHN-VPQH — Điều 146. Thủ tục tiếp nhận tố giác, tin báo về tội phạm, kiến nghị khởi tố | Khoản 1: “1. Khi cơ quan, tổ chức, cá nhân trực tiếp tố giác, báo tin về tội phạm, kiến nghị khởi tố thì Cơ quan điều tra, Viện kiểm sát, cơ quan được giao nhiệm vụ tiến hành một số hoạt động điều tra có thẩm quyền quy định tại khoản 2 Điều 145 của Bộ luật này phải lập biên bản tiếp nhận và ghi vào sổ tiếp nhận; có thể ghi âm hoặc ghi hình có âm thanh việc tiếp nhận.

Trường hợp tố giác, tin báo về tội phạm, kiến nghị khởi tố gửi qua dịch vụ bưu chính, điện thoại hoặc qua phương tiện thông tin khác thì ghi vào sổ tiếp nhận.” [2].

- Văn-bản-hợp-nhất-17-VBHN-VPQH — Điều 145. Trách nhiệm tiếp nhận và thẩm quyền giải quyết tố giác, tin báo về tội phạm, kiến nghị khởi tố | Khoản 2: “2. Cơ quan, tổ chức có trách nhiệm tiếp nhận tố giác, tin báo về tội phạm, kiến nghị khởi tố gồm:

2. Cơ quan, tổ chức có trách nhiệm tiếp nhận tố giác, tin báo về tội phạm, kiến nghị khởi tố gồm: a) Cơ quan điều tra, Viện kiểm sát tiếp nhận tố giác, tin báo về tội phạm, kiến nghị khởi tố;

2. Cơ quan, tổ chức có trách nhiệm tiếp nhận tố giác, tin báo về tội phạm, kiến nghị khởi tố gồm: b) Cơ quan, tổ chức khác tiếp nhận tố giác, tin báo về tội phạm.” [3].

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng, hiệu lực và bản gốc.

#### C — Đáp án bạn gửi

**1. Thu thập và lưu lại toàn bộ chứng cứ:**
- Biên lai chuyển khoản ngân hàng (lưu rõ số tài khoản, tên chủ tài khoản, mã giao dịch, thời gian).
- Toàn bộ ảnh chụp màn hình tin nhắn thỏa thuận (từ lúc bắt đầu đến khi bị chặn/xóa).
- Số điện thoại, đường link trang cá nhân Facebook/Zalo của đối tượng, hình ảnh bài đăng phòng trọ.

**2. Nơi trình báo:**
- Nộp đơn tố giác tội phạm tại **Công an phường/xã nơi bạn thực hiện giao dịch chuyển tiền**, hoặc **Đội Cảnh sát hình sự / Đội An ninh mạng (PA05) Công an TP. Cần Thơ**.
- Liên hệ ngay với tổng đài ngân hàng của bạn thông báo tài khoản bị lừa đảo để đề nghị hỗ trợ đánh dấu giao dịch gian lận.

#### D — Chatbot dạng agent

Người dân cần nhanh chóng lưu giữ tài liệu, tin nhắn, chứng từ chuyển tiền và trình báo cơ quan Công an hoặc các cơ quan có thẩm quyền tiếp nhận tố giác tội phạm [1] [3].

- Nhanh chóng thu thập và lưu giữ toàn bộ tài liệu, tin nhắn cùng các chứng từ chuyển tiền liên quan đến giao dịch [1].
- Trình báo sự việc tới cơ quan Công an để được hỗ trợ và xử lý kịp thời theo khuyến cáo [1].
- Thực hiện việc tố giác trực tiếp hoặc gửi qua dịch vụ bưu chính, điện thoại hay các phương tiện thông tin khác tới Cơ quan điều tra, Viện kiểm sát hoặc cơ quan, tổ chức có thẩm quyền [2] [3].
- Yêu cầu cơ quan có thẩm quyền lập biên bản tiếp nhận và ghi vào sổ tiếp nhận khi đến tố giác trực tiếp [2].

Nội dung khuyến cáo lưu giữ bằng chứng và báo cơ quan Công an là thông tin phòng ngừa, không phải điều luật [1].
Cơ quan điều tra, Viện kiểm sát và cơ quan được giao nhiệm vụ tiến hành một số hoạt động điều tra có thể ghi âm hoặc ghi hình có âm thanh khi lập biên bản tiếp nhận [2].

Để áp dụng vào trường hợp của bạn:
- Bạn đã chuyển khoản qua ngân hàng, ví điện tử hay giao dịch bằng hình thức nào khác?
- Bạn có lưu giữ được thông tin tài khoản nhận tiền và nội dung tin nhắn trao đổi không?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

Nguồn truy xuất của D (rank dùng trong trích dẫn):

- [1] rental_warning-Bo-Cong-an-20261003
- [2] Văn-bản-hợp-nhất-17-VBHN-VPQH — Điều 146. Thủ tục tiếp nhận tố giác, tin báo về tội phạm, kiến nghị khởi tố | Khoản 1
- [3] Văn-bản-hợp-nhất-17-VBHN-VPQH — Điều 145. Trách nhiệm tiếp nhận và thẩm quyền giải quyết tố giác, tin báo về tội phạm, kiến nghị khởi tố | Khoản 2

### Câu 35: Khi nào tranh chấp tiền cọc có thể có dấu hiệu lừa đảo, và khi nào chỉ là tranh chấp hợp đồng?

#### A — Gemini chatbot

Các căn cứ liên quan tìm được trong kho (trích nguyên đoạn):

- rental_warning-Bo-Cong-an-20261003 — trích đoạn: “Để phòng ngừa loại tội phạm này, cơ quan Công an khuyến cáo người dân cần trực tiếp đến xem phòng trọ, xác minh rõ danh tính chủ nhà hoặc người cho thuê trước khi giao dịch; tuyệt đối không chuyển tiền đặt cọc khi trao đổi qua mạng xã hội hoặc điện thoại mà chưa gặp mặt, chưa kiểm chứng thông tin. Khi phát hiện dấu hiệu nghi vấn hoặc đã trở thành nạn nhân của hành vi lừa đảo, người dân cần nhanh chóng lưu giữ các tài liệu, tin nhắn, chứng từ chuyển tiền và trình báo cơ quan Công an để được hỗ trợ, xử lý kịp thời.” [3].

- Bo-luat-91-2015-QH13-doi-chieu-20261003 — Điều 328. Đặt cọc | Khoản 1: “1. Đặt cọc là việc một bên (sau đây gọi là bên đặt cọc) giao cho bên kia (sau đây gọi là bên nhận đặt cọc) một khoản tiền hoặc kim khí quý, đá quý hoặc vật có giá trị khác (sau đây gọi chung là tài sản đặt cọc) trong một thời hạn để bảo đảm giao kết hoặc thực hiện hợp đồng.” [1].

Đây là câu trả lời một phần từ nguồn; chưa kết luận cách áp dụng cho tình huống riêng của bạn. Cần đối chiếu điều kiện, hiệu lực và bản gốc.

#### B — Gemini phân tích + Qwen trích nguồn

Các đoạn trả lời trực tiếp trong nguồn:

- Bo-luat-91-2015-QH13-doi-chieu-20261003 — Điều 328. Đặt cọc | Khoản 1: “1. Đặt cọc là việc một bên (sau đây gọi là bên đặt cọc) giao cho bên kia (sau đây gọi là bên nhận đặt cọc) một khoản tiền hoặc kim khí quý, đá quý hoặc vật có giá trị khác (sau đây gọi chung là tài sản đặt cọc) trong một thời hạn để bảo đảm giao kết hoặc thực hiện hợp đồng.” [1].

- Văn-bản-hợp-nhất-135-VBHN-VPQH — Điều 174. Tội lừa đảo chiếm đoạt tài sản | Khoản 1: “1. Người nào bằng thủ đoạn gian dối chiếm đoạt tài sản của người khác trị giá từ 2.000.000 đồng đến dưới 50.000.000 đồng hoặc dưới 2.000.000 đồng nhưng thuộc một trong các trường hợp sau đây, thì bị phạt cải tạo không giam giữ đến 03 năm hoặc phạt tù từ 06 tháng đến 03 năm:

1. Người nào bằng thủ đoạn gian dối chiếm đoạt tài sản của người khác trị giá từ 2.000.000 đồng đến dưới 50.000.000 đồng hoặc dưới 2.000.000 đồng nhưng thuộc một trong các trường hợp sau đây, thì bị phạt cải tạo không giam giữ đến 03 năm hoặc phạt tù từ 06 tháng đến 03 năm: a) Đã bị xử phạt vi phạm hành chính về hành vi chiếm đoạt tài sản mà còn vi phạm;

1. Người nào bằng thủ đoạn gian dối chiếm đoạt tài sản của người khác trị giá từ 2.000.000 đồng đến dưới 50.000.000 đồng hoặc dưới 2.000.000 đồng nhưng thuộc một trong các trường hợp sau đây, thì bị phạt cải tạo không giam giữ đến 03 năm hoặc phạt tù từ 06 tháng đến 03 năm: b) Đã bị kết án về tội này hoặc về một trong các tội quy định tại các điều 168, 169, 170, 171, 172, 173, 175 và 290 của Bộ luật này, chưa được xóa án tích mà còn vi phạm;

1. Người nào bằng thủ đoạn gian dối chiếm đoạt tài sản của người khác trị giá từ 2.000.000 đồng đến dưới 50.000.000 đồng hoặc dưới 2.000.000 đồng nhưng thuộc một trong các trường hợp sau đây, thì bị phạt cải tạo không giam giữ đến 03 năm hoặc phạt tù từ 06 tháng đến 03 năm: c) Gây ảnh hưởng xấu đến an ninh, trật tự, an toàn xã hội;

1. Người nào bằng thủ đoạn gian dối chiếm đoạt tài sản của người khác trị giá từ 2.000.000 đồng đến dưới 50.000.000 đồng hoặc dưới 2.000.000 đồng nhưng thuộc một trong các trường hợp sau đây, thì bị phạt cải tạo không giam giữ đến 03 năm hoặc phạt tù từ 06 tháng đến 03 năm: d) Tài sản là phương tiện kiếm sống chính của người bị hại và gia đình họ[98].” [2].

- rental_warning-Bo-Cong-an-20261003 — trích đoạn: “KHUYẾN CÁO PHÒNG NGỪA LỪA ĐẢO — KHÔNG PHẢI ĐIỀU LUẬT

Khuyến cáo của cơ quan Công an về đặt cọc thuê nhà qua mạng

Để phòng ngừa loại tội phạm này, cơ quan Công an khuyến cáo người dân cần trực tiếp đến xem phòng trọ, xác minh rõ danh tính chủ nhà hoặc người cho thuê trước khi giao dịch; tuyệt đối không chuyển tiền đặt cọc khi trao đổi qua mạng xã hội hoặc điện thoại mà chưa gặp mặt, chưa kiểm chứng thông tin. Khi phát hiện dấu hiệu nghi vấn hoặc đã trở thành nạn nhân của hành vi lừa đảo, người dân cần nhanh chóng lưu giữ các tài liệu, tin nhắn, chứng từ chuyển tiền và trình báo cơ quan Công an để được hỗ trợ, xử lý kịp thời.” [3].

- Bo-luat-91-2015-QH13-doi-chieu-20261003 — Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp: “Điều 117. Điều kiện có hiệu lực của giao dịch dân sự
Điều 117. Điều kiện có hiệu lực của giao dịch dân sự

Điều 117. Điều kiện có hiệu lực của giao dịch dân sự | Khoản 1
1. Giao dịch dân sự có hiệu lực khi có đủ các điều kiện sau đây:

Điều 117. Điều kiện có hiệu lực của giao dịch dân sự | Khoản 1 | Điểm a
1. Giao dịch dân sự có hiệu lực khi có đủ các điều kiện sau đây: a) Chủ thể có năng lực pháp luật dân sự, năng lực hành vi dân sự phù hợp với giao dịch dân sự được xác lập;

Điều 117. Điều kiện có hiệu lực của giao dịch dân sự | Khoản 1 | Điểm b
1. Giao dịch dân sự có hiệu lực khi có đủ các điều kiện sau đây: b) Chủ thể tham gia giao dịch dân sự hoàn toàn tự nguyện;

Điều 117. Điều kiện có hiệu lực của giao dịch dân sự | Khoản 1 | Điểm c
1. Giao dịch dân sự có hiệu lực khi có đủ các điều kiện sau đây: c) Mục đích và nội dung của giao dịch dân sự không vi phạm điều cấm của luật, không trái đạo đức xã hội.

Điều 117. Điều kiện có hiệu lực của giao dịch dân sự | Khoản 2
2. Hình thức của giao dịch dân sự là điều kiện có hiệu lực của giao dịch dân sự trong trường hợp luật có quy định.

Điều 689. Hiệu lực thi hành
Điều 689. Hiệu lực thi hành Bộ luật này có hiệu lực thi hành từ ngày 01 tháng 01 năm 2017.

Bộ luật dân sự số 33/2005/QH11 hết hiệu lực kể từ ngày Bộ luật này có hiệu lực.

Điều 688. Điều khoản chuyển tiếp
Điều 688. Điều khoản chuyển tiếp

Điều 688. Điều khoản chuyển tiếp | Khoản 1
1. Đối với giao dịch dân sự được xác lập trước ngày Bộ luật này có hiệu lực thì việc áp dụng pháp luật được quy định như sau:

Điều 688. Điều khoản chuyển tiếp | Khoản 1 | Điểm a
1. Đối với giao dịch dân sự được xác lập trước ngày Bộ luật này có hiệu lực thì việc áp dụng pháp luật được quy định như sau: a) Giao dịch dân sự chưa được thực hiện mà có nội dung, hình thức khác với quy định của Bộ luật này thì chủ thể giao dịch tiếp tục thực hiện theo quy định của Bộ luật dân sự số 33/2005/QH11 và các văn bản quy phạm pháp luật quy định chi tiết Bộ luật dân sự số 33/2005/QH11, trừ trường hợp các bên của giao dịch dân sự có thỏa thuận về việc sửa đổi, bổ sung nội dung, hình thức của giao dịch để phù hợp với Bộ luật này và để áp dụng quy định của Bộ luật này.

Giao dịch dân sự đang được thực hiện mà có nội dung, hình thức khác với quy định của Bộ luật này thì áp dụng quy định của Bộ luật dân sự số 33/2005/QH11 và các văn bản quy phạm pháp luật quy định chi tiết Bộ luật dân sự số 33/2005/QH11;

Điều 688. Điều khoản chuyển tiếp | Khoản 1 | Điểm b
1. Đối với giao dịch dân sự được xác lập trước ngày Bộ luật này có hiệu lực thì việc áp dụng pháp luật được quy định như sau: b) Giao dịch dân sự chưa được thực hiện hoặc đang được thực hiện mà có nội dung và hình thức phù hợp với quy định của Bộ luật này thì áp dụng quy định của Bộ luật này;

Điều 688. Điều khoản chuyển tiếp | Khoản 1 | Điểm c
1. Đối với giao dịch dân sự được xác lập trước ngày Bộ luật này có hiệu lực thì việc áp dụng pháp luật được quy định như sau: c) Giao dịch dân sự được thực hiện xong trước ngày Bộ luật này có hiệu lực mà có tranh chấp thì áp dụng quy định của Bộ luật dân sự số 33/2005/QH11 và các văn bản quy phạm pháp luật quy định chi tiết Bộ luật dân sự số 33/2005/QH11 để giải quyết;

Điều 688. Điều khoản chuyển tiếp | Khoản 1 | Điểm d
1. Đối với giao dịch dân sự được xác lập trước ngày Bộ luật này có hiệu lực thì việc áp dụng pháp luật được quy định như sau: d) Thời hiệu được áp dụng theo quy định của Bộ luật này.

Điều 688. Điều khoản chuyển tiếp | Khoản 2
2. Không áp dụng Bộ luật này để kháng nghị theo thủ tục giám đốc thẩm, tái thẩm đối với vụ việc mà Tòa án đã giải quyết theo quy định của pháp luật về dân sự trước ngày Bộ luật này có hiệu lực.” [4].

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng, hiệu lực và bản gốc.

#### C — Đáp án bạn gửi

- **Trường hợp là Tranh chấp dân sự (Hợp đồng):**
  - Phòng trọ có thật, hai bên có giao kết hợp đồng, người cho thuê đúng là chủ sở hữu hoặc người có thẩm quyền.
  - Tranh chấp phát sinh do bất đồng ý kiến về điều kiện trừ cọc, hư hỏng tài sản hay thời gian báo trước dọn đi. Vụ việc thuộc thẩm quyền giải quyết của **Tòa án nhân dân cấp quận/huyện**.
- **Trường hợp có dấu hiệu Tội phạm hình sự (Lừa đảo - Điều 174 BLHS):**
  - Đối tượng đưa ra thông tin gian dối ngay từ đầu: Dùng phòng ảo, nhà của người khác đóng giả làm chủ trọ để nhận cọc, hứa hẹn cho thuê nhưng thực tế không có quyền cho thuê, sau khi nhận được tiền thì lập tức chặn liên lạc, bỏ trốn để chiếm đoạt tài sản. Vụ việc thuộc thẩm quyền xử lý của **Cơ quan Cảnh sát điều tra (Công an)**.

#### D — Chatbot dạng agent

Các đoạn trả lời trực tiếp trong nguồn:

- Bo-luat-91-2015-QH13-doi-chieu-20261003 — Điều 328. Đặt cọc | Khoản 1: “1. Đặt cọc là việc một bên (sau đây gọi là bên đặt cọc) giao cho bên kia (sau đây gọi là bên nhận đặt cọc) một khoản tiền hoặc kim khí quý, đá quý hoặc vật có giá trị khác (sau đây gọi chung là tài sản đặt cọc) trong một thời hạn để bảo đảm giao kết hoặc thực hiện hợp đồng.” [1].

- Văn-bản-hợp-nhất-135-VBHN-VPQH — Điều 174. Tội lừa đảo chiếm đoạt tài sản | Khoản 1: “1. Người nào bằng thủ đoạn gian dối chiếm đoạt tài sản của người khác trị giá từ 2.000.000 đồng đến dưới 50.000.000 đồng hoặc dưới 2.000.000 đồng nhưng thuộc một trong các trường hợp sau đây, thì bị phạt cải tạo không giam giữ đến 03 năm hoặc phạt tù từ 06 tháng đến 03 năm:

1. Người nào bằng thủ đoạn gian dối chiếm đoạt tài sản của người khác trị giá từ 2.000.000 đồng đến dưới 50.000.000 đồng hoặc dưới 2.000.000 đồng nhưng thuộc một trong các trường hợp sau đây, thì bị phạt cải tạo không giam giữ đến 03 năm hoặc phạt tù từ 06 tháng đến 03 năm: a) Đã bị xử phạt vi phạm hành chính về hành vi chiếm đoạt tài sản mà còn vi phạm;

1. Người nào bằng thủ đoạn gian dối chiếm đoạt tài sản của người khác trị giá từ 2.000.000 đồng đến dưới 50.000.000 đồng hoặc dưới 2.000.000 đồng nhưng thuộc một trong các trường hợp sau đây, thì bị phạt cải tạo không giam giữ đến 03 năm hoặc phạt tù từ 06 tháng đến 03 năm: b) Đã bị kết án về tội này hoặc về một trong các tội quy định tại các điều 168, 169, 170, 171, 172, 173, 175 và 290 của Bộ luật này, chưa được xóa án tích mà còn vi phạm;

1. Người nào bằng thủ đoạn gian dối chiếm đoạt tài sản của người khác trị giá từ 2.000.000 đồng đến dưới 50.000.000 đồng hoặc dưới 2.000.000 đồng nhưng thuộc một trong các trường hợp sau đây, thì bị phạt cải tạo không giam giữ đến 03 năm hoặc phạt tù từ 06 tháng đến 03 năm: c) Gây ảnh hưởng xấu đến an ninh, trật tự, an toàn xã hội;

1. Người nào bằng thủ đoạn gian dối chiếm đoạt tài sản của người khác trị giá từ 2.000.000 đồng đến dưới 50.000.000 đồng hoặc dưới 2.000.000 đồng nhưng thuộc một trong các trường hợp sau đây, thì bị phạt cải tạo không giam giữ đến 03 năm hoặc phạt tù từ 06 tháng đến 03 năm: d) Tài sản là phương tiện kiếm sống chính của người bị hại và gia đình họ[98].” [2].

- rental_warning-Bo-Cong-an-20261003 — trích đoạn: “KHUYẾN CÁO PHÒNG NGỪA LỪA ĐẢO — KHÔNG PHẢI ĐIỀU LUẬT

Khuyến cáo của cơ quan Công an về đặt cọc thuê nhà qua mạng

Để phòng ngừa loại tội phạm này, cơ quan Công an khuyến cáo người dân cần trực tiếp đến xem phòng trọ, xác minh rõ danh tính chủ nhà hoặc người cho thuê trước khi giao dịch; tuyệt đối không chuyển tiền đặt cọc khi trao đổi qua mạng xã hội hoặc điện thoại mà chưa gặp mặt, chưa kiểm chứng thông tin. Khi phát hiện dấu hiệu nghi vấn hoặc đã trở thành nạn nhân của hành vi lừa đảo, người dân cần nhanh chóng lưu giữ các tài liệu, tin nhắn, chứng từ chuyển tiền và trình báo cơ quan Công an để được hỗ trợ, xử lý kịp thời.” [3].

- Bo-luat-91-2015-QH13-doi-chieu-20261003 — Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp: “Điều 117. Điều kiện có hiệu lực của giao dịch dân sự
Điều 117. Điều kiện có hiệu lực của giao dịch dân sự

Điều 117. Điều kiện có hiệu lực của giao dịch dân sự | Khoản 1
1. Giao dịch dân sự có hiệu lực khi có đủ các điều kiện sau đây:

Điều 117. Điều kiện có hiệu lực của giao dịch dân sự | Khoản 1 | Điểm a
1. Giao dịch dân sự có hiệu lực khi có đủ các điều kiện sau đây: a) Chủ thể có năng lực pháp luật dân sự, năng lực hành vi dân sự phù hợp với giao dịch dân sự được xác lập;

Điều 117. Điều kiện có hiệu lực của giao dịch dân sự | Khoản 1 | Điểm b
1. Giao dịch dân sự có hiệu lực khi có đủ các điều kiện sau đây: b) Chủ thể tham gia giao dịch dân sự hoàn toàn tự nguyện;

Điều 117. Điều kiện có hiệu lực của giao dịch dân sự | Khoản 1 | Điểm c
1. Giao dịch dân sự có hiệu lực khi có đủ các điều kiện sau đây: c) Mục đích và nội dung của giao dịch dân sự không vi phạm điều cấm của luật, không trái đạo đức xã hội.

Điều 117. Điều kiện có hiệu lực của giao dịch dân sự | Khoản 2
2. Hình thức của giao dịch dân sự là điều kiện có hiệu lực của giao dịch dân sự trong trường hợp luật có quy định.

Điều 689. Hiệu lực thi hành
Điều 689. Hiệu lực thi hành Bộ luật này có hiệu lực thi hành từ ngày 01 tháng 01 năm 2017.

Bộ luật dân sự số 33/2005/QH11 hết hiệu lực kể từ ngày Bộ luật này có hiệu lực.

Điều 688. Điều khoản chuyển tiếp
Điều 688. Điều khoản chuyển tiếp

Điều 688. Điều khoản chuyển tiếp | Khoản 1
1. Đối với giao dịch dân sự được xác lập trước ngày Bộ luật này có hiệu lực thì việc áp dụng pháp luật được quy định như sau:

Điều 688. Điều khoản chuyển tiếp | Khoản 1 | Điểm a
1. Đối với giao dịch dân sự được xác lập trước ngày Bộ luật này có hiệu lực thì việc áp dụng pháp luật được quy định như sau: a) Giao dịch dân sự chưa được thực hiện mà có nội dung, hình thức khác với quy định của Bộ luật này thì chủ thể giao dịch tiếp tục thực hiện theo quy định của Bộ luật dân sự số 33/2005/QH11 và các văn bản quy phạm pháp luật quy định chi tiết Bộ luật dân sự số 33/2005/QH11, trừ trường hợp các bên của giao dịch dân sự có thỏa thuận về việc sửa đổi, bổ sung nội dung, hình thức của giao dịch để phù hợp với Bộ luật này và để áp dụng quy định của Bộ luật này.

Giao dịch dân sự đang được thực hiện mà có nội dung, hình thức khác với quy định của Bộ luật này thì áp dụng quy định của Bộ luật dân sự số 33/2005/QH11 và các văn bản quy phạm pháp luật quy định chi tiết Bộ luật dân sự số 33/2005/QH11;

Điều 688. Điều khoản chuyển tiếp | Khoản 1 | Điểm b
1. Đối với giao dịch dân sự được xác lập trước ngày Bộ luật này có hiệu lực thì việc áp dụng pháp luật được quy định như sau: b) Giao dịch dân sự chưa được thực hiện hoặc đang được thực hiện mà có nội dung và hình thức phù hợp với quy định của Bộ luật này thì áp dụng quy định của Bộ luật này;

Điều 688. Điều khoản chuyển tiếp | Khoản 1 | Điểm c
1. Đối với giao dịch dân sự được xác lập trước ngày Bộ luật này có hiệu lực thì việc áp dụng pháp luật được quy định như sau: c) Giao dịch dân sự được thực hiện xong trước ngày Bộ luật này có hiệu lực mà có tranh chấp thì áp dụng quy định của Bộ luật dân sự số 33/2005/QH11 và các văn bản quy phạm pháp luật quy định chi tiết Bộ luật dân sự số 33/2005/QH11 để giải quyết;

Điều 688. Điều khoản chuyển tiếp | Khoản 1 | Điểm d
1. Đối với giao dịch dân sự được xác lập trước ngày Bộ luật này có hiệu lực thì việc áp dụng pháp luật được quy định như sau: d) Thời hiệu được áp dụng theo quy định của Bộ luật này.

Điều 688. Điều khoản chuyển tiếp | Khoản 2
2. Không áp dụng Bộ luật này để kháng nghị theo thủ tục giám đốc thẩm, tái thẩm đối với vụ việc mà Tòa án đã giải quyết theo quy định của pháp luật về dân sự trước ngày Bộ luật này có hiệu lực.” [4].

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng, hiệu lực và bản gốc.

Nguồn truy xuất của D (rank dùng trong trích dẫn):

- [1] Bo-luat-91-2015-QH13-doi-chieu-20261003 — Điều 328. Đặt cọc | Khoản 1
- [2] Văn-bản-hợp-nhất-135-VBHN-VPQH — Điều 174. Tội lừa đảo chiếm đoạt tài sản | Khoản 1
- [3] rental_warning-Bo-Cong-an-20261003
- [4] Bo-luat-91-2015-QH13-doi-chieu-20261003 — Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp

Lý do giới hạn/fallback của D:

- Nguồn trích dẫn chưa nêu căn cứ cho kết luận về xử lý, bồi thường hoặc hoàn trả.
- Bản tổng hợp chưa được nguồn xác nhận sau lần sửa; dùng trích đoạn Qwen đã chọn.

### Câu 36: Nếu có nhiều sinh viên cùng bị một người nhận cọc rồi cắt liên lạc, chúng tôi nên cung cấp thông tin gì cho cơ quan có thẩm quyền?

#### A — Gemini chatbot

Các căn cứ liên quan tìm được trong kho (trích nguyên đoạn):

- rental_warning-Bo-Cong-an-20261003 — trích đoạn: “Để phòng ngừa loại tội phạm này, cơ quan Công an khuyến cáo người dân cần trực tiếp đến xem phòng trọ, xác minh rõ danh tính chủ nhà hoặc người cho thuê trước khi giao dịch; tuyệt đối không chuyển tiền đặt cọc khi trao đổi qua mạng xã hội hoặc điện thoại mà chưa gặp mặt, chưa kiểm chứng thông tin. Khi phát hiện dấu hiệu nghi vấn hoặc đã trở thành nạn nhân của hành vi lừa đảo, người dân cần nhanh chóng lưu giữ các tài liệu, tin nhắn, chứng từ chuyển tiền và trình báo cơ quan Công an để được hỗ trợ, xử lý kịp thời.” [1].

- Văn-bản-hợp-nhất-17-VBHN-VPQH — Điều 146. Thủ tục tiếp nhận tố giác, tin báo về tội phạm, kiến nghị khởi tố | Khoản 1: “1. Khi cơ quan, tổ chức, cá nhân trực tiếp tố giác, báo tin về tội phạm, kiến nghị khởi tố thì Cơ quan điều tra, Viện kiểm sát, cơ quan được giao nhiệm vụ tiến hành một số hoạt động điều tra có thẩm quyền quy định tại khoản 2 Điều 145 của Bộ luật này phải lập biên bản tiếp nhận và ghi vào sổ tiếp nhận; có thể ghi âm hoặc ghi hình có âm thanh việc tiếp nhận.” [2].

Đây là câu trả lời một phần từ nguồn; chưa kết luận cách áp dụng cho tình huống riêng của bạn. Cần đối chiếu điều kiện, hiệu lực và bản gốc.

#### B — Gemini phân tích + Qwen trích nguồn

Các đoạn trả lời trực tiếp trong nguồn:

- rental_warning-Bo-Cong-an-20261003 — trích đoạn: “KHUYẾN CÁO PHÒNG NGỪA LỪA ĐẢO — KHÔNG PHẢI ĐIỀU LUẬT

Khuyến cáo của cơ quan Công an về đặt cọc thuê nhà qua mạng

Để phòng ngừa loại tội phạm này, cơ quan Công an khuyến cáo người dân cần trực tiếp đến xem phòng trọ, xác minh rõ danh tính chủ nhà hoặc người cho thuê trước khi giao dịch; tuyệt đối không chuyển tiền đặt cọc khi trao đổi qua mạng xã hội hoặc điện thoại mà chưa gặp mặt, chưa kiểm chứng thông tin. Khi phát hiện dấu hiệu nghi vấn hoặc đã trở thành nạn nhân của hành vi lừa đảo, người dân cần nhanh chóng lưu giữ các tài liệu, tin nhắn, chứng từ chuyển tiền và trình báo cơ quan Công an để được hỗ trợ, xử lý kịp thời.” [1].

- Văn-bản-hợp-nhất-17-VBHN-VPQH — Điều 146. Thủ tục tiếp nhận tố giác, tin báo về tội phạm, kiến nghị khởi tố | Khoản 1: “1. Khi cơ quan, tổ chức, cá nhân trực tiếp tố giác, báo tin về tội phạm, kiến nghị khởi tố thì Cơ quan điều tra, Viện kiểm sát, cơ quan được giao nhiệm vụ tiến hành một số hoạt động điều tra có thẩm quyền quy định tại khoản 2 Điều 145 của Bộ luật này phải lập biên bản tiếp nhận và ghi vào sổ tiếp nhận; có thể ghi âm hoặc ghi hình có âm thanh việc tiếp nhận.

Trường hợp tố giác, tin báo về tội phạm, kiến nghị khởi tố gửi qua dịch vụ bưu chính, điện thoại hoặc qua phương tiện thông tin khác thì ghi vào sổ tiếp nhận.” [2].

- Văn-bản-hợp-nhất-17-VBHN-VPQH — Điều 145. Trách nhiệm tiếp nhận và thẩm quyền giải quyết tố giác, tin báo về tội phạm, kiến nghị khởi tố | Khoản 2: “2. Cơ quan, tổ chức có trách nhiệm tiếp nhận tố giác, tin báo về tội phạm, kiến nghị khởi tố gồm:

2. Cơ quan, tổ chức có trách nhiệm tiếp nhận tố giác, tin báo về tội phạm, kiến nghị khởi tố gồm: a) Cơ quan điều tra, Viện kiểm sát tiếp nhận tố giác, tin báo về tội phạm, kiến nghị khởi tố;

2. Cơ quan, tổ chức có trách nhiệm tiếp nhận tố giác, tin báo về tội phạm, kiến nghị khởi tố gồm: b) Cơ quan, tổ chức khác tiếp nhận tố giác, tin báo về tội phạm.” [3].

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng, hiệu lực và bản gốc.

#### C — Đáp án bạn gửi

Khi có nhiều nạn nhân, hành vi có tính chất chuyên nghiệp, mức độ nguy hiểm cao và giá trị thiệt hại cộng dồn sẽ cấu thành khung hình phạt nặng hơn theo Điều 174 Bộ luật Hình sự:
1. **Lập Đơn tố giác tội phạm tập thể (đồng đứng tên các nạn nhân):** Liệt kê danh sách từng người, số tiền bị chiếm đoạt, phương thức liên lạc.
2. **Tài liệu chứng minh kèm theo:** Bảng sao kê giao dịch ngân hàng của tất cả nạn nhân chuyển vào cùng số tài khoản thụ hưởng của kẻ lừa đảo; các cuộc hội thoại thể hiện cùng một kịch bản gian dối.
3. **Nơi tiếp nhận:** Nộp đơn đến **Cơ quan Cảnh sát điều tra Công an quận/huyện** nơi đối tượng cư trú hoặc nơi người thuê nhà thực hiện chuyển khoản. Cơ quan điều tra sẽ thụ lý và khởi tố vụ án theo thẩm quyền.

#### D — Chatbot dạng agent

Khi phát hiện bị lừa đảo tiền đặt cọc, các sinh viên cần nhanh chóng lưu giữ các tài liệu, tin nhắn, chứng từ chuyển tiền và trình báo cơ quan Công an để được xử lý kịp thời [1].

- Nhanh chóng thu thập và lưu giữ toàn bộ tài liệu, tin nhắn trao đổi liên quan đến việc đặt cọc [1].
- Tập hợp các chứng từ chuyển tiền đã thực hiện với đối tượng nhận cọc [1].
- Trực tiếp tố giác hoặc gửi tin báo đến Cơ quan điều tra, Viện kiểm sát hoặc các cơ quan có thẩm quyền tiếp nhận theo quy định [2] [3].

Khuyến nghị của cơ quan Công an về việc lưu giữ tài liệu, tin nhắn và chứng từ chỉ mang tính chất hướng dẫn phòng ngừa, hỗ trợ xử lý chứ không phải điều luật cụ thể [1].
Cơ quan tiếp nhận trực tiếp có trách nhiệm lập biên bản tiếp nhận và vào sổ tiếp nhận, đồng thời có thể ghi âm hoặc ghi hình có âm thanh việc tiếp nhận [2].

Để áp dụng vào trường hợp của bạn:
- Các bạn đã lưu giữ được những sao kê ngân hàng hay ảnh chụp tin nhắn trao đổi nào chưa?
- Các bạn dự định gửi đơn trực tiếp hay nộp qua dịch vụ bưu chính tới cơ quan Công an nào?

Thông tin tham khảo từ nguồn, cần đối chiếu điều kiện áp dụng và hiệu lực.

Nguồn truy xuất của D (rank dùng trong trích dẫn):

- [1] rental_warning-Bo-Cong-an-20261003
- [2] Văn-bản-hợp-nhất-17-VBHN-VPQH — Điều 146. Thủ tục tiếp nhận tố giác, tin báo về tội phạm, kiến nghị khởi tố | Khoản 1
- [3] Văn-bản-hợp-nhất-17-VBHN-VPQH — Điều 145. Trách nhiệm tiếp nhận và thẩm quyền giải quyết tố giác, tin báo về tội phạm, kiến nghị khởi tố | Khoản 2
