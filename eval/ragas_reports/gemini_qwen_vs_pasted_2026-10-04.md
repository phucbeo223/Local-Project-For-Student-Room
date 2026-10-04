# Đối chiếu Gemini, Gemini + Qwen và 36 đáp án bạn dán

Đã rà đủ **36 câu / 108 đáp án** từ ba bộ dữ liệu. Bản bạn dán tốt hơn về checklist và hướng dẫn hành động. Gemini thường diễn giải dễ đọc hơn Qwen; Gemini + Qwen bám nguồn tốt hơn nhưng hiện chủ yếu xuất trích đoạn. Cả hai chưa đạt mức hướng dẫn thực hành của bản dán ở nhiều câu.

## Phạm vi

- A: lượt Gemini-only đã hoàn tất, kho `public`; không dùng lượt local v15 làm kết quả A.
- B: Gemini phân tích câu hỏi + Qwen3.5:9b chọn đoạn nguồn (`source_select`); code xuất trích dẫn. B chưa có bước Gemini viết lại câu trả lời và kiểm chứng ngữ nghĩa sau đó cho đầu ra trích nguyên văn.
- C: nguyên văn bộ bạn dán; SHA-256 trùng bản đã lưu. Ghép 35 câu nguyên văn, câu 27 ghép cùng ý do phía hệ thống thêm “người bán hoặc”.
- Đối chiếu nội dung đã sinh; không chạy lại mô hình, thay corpus hoặc chấm RAGAS theo C. C chưa là đáp án đúng pháp luật độc lập.

## Số liệu và cách hiểu

| Tiêu chí | A: Gemini | B: Gemini + Qwen | C: bản dán |
|---|---:|---:|---|
| Faithfulness trên cùng 33 câu | 0,771 | 0,962 | Chưa chấm với context |
| Answer Relevancy, 36 câu | 0,725 | 0,721 | Chưa chấm cùng cách |
| Độ trễ p50 | 18,2 giây | 30,7 giây | Không có dữ liệu chạy |
| Ký tự trung vị/đáp án | 855.5 | 2473 | 527 |
| Cờ hệ thống “đầy đủ” | 12/36 | 15/36 | Không có cờ tương đương |

Faithfulness đo mức bám nguồn đã đưa vào context, không đo đúng pháp luật hay mức giống C. B thiếu điểm Faithfulness ở câu 6–8 sau một lần thử lại. Cờ đầy đủ không là nhãn chất lượng: B câu 16 vẫn chưa giải thích chuyển chỗ ở, câu 36 vẫn thiếu bảng từng nạn nhân.

Rà **độ bao phủ yêu cầu thực hành** bằng tay: 0 = thiếu ý trả lời trực tiếp; 1 = một phần; 2 = bao phủ yêu cầu chính. Nhãn xét yêu cầu câu hỏi và các ý hữu ích trong C, bỏ các khẳng định chưa xác minh làm điều kiện bắt buộc. Không chấm phần trăm giống C hoặc phần trăm đúng pháp luật.

| Nhãn nội dung | A | B |
|---|---:|---:|
| Thiếu ý cốt lõi | 9 | 7 |
| Bao phủ một phần | 17 | 21 |
| Bao phủ yêu cầu chính | 10 | 8 |

Đây là nhận xét của một người rà, có căn cứ từng câu bên dưới; chưa có đánh giá độc lập của chuyên gia. Hai luồng cùng có điểm nghẽn là thiếu hướng dẫn áp dụng. Lợi thế Faithfulness của B không đồng nghĩa B giải quyết nhiều yêu cầu thực hành hơn.

## Các khác biệt đáng chú ý

- Câu 1/30: A trả mẫu không kết luận; B có căn cứ nhưng chưa thành checklist hợp đồng/lưu CCCD.
- Câu 3/10/22: A diễn giải nguyên tắc hoặc bước kiểm tra sát câu hỏi hơn; B chọn đoạn hẹp và bỏ mất phần áp dụng.
- Câu 8/11/16/19/24/29: cả hai thiếu ý thực hành cốt lõi dù tìm được nguồn cùng chủ đề.
- Câu 31/32/35: B có nhiều căn cứ hơn A, vẫn cần diễn giải giới hạn công khai, cách yêu cầu xử lý và phân biệt tranh chấp/lừa đảo.
- Câu 36: C có bảng từng người/từng giao dịch; cả hai mới nói lưu bằng chứng/trình báo chung.

## Bản dán cần rà trước khi dùng làm đáp án chuẩn

- Nhóm dữ liệu cá nhân: đang dựa Nghị định 13/2023. Nguồn hiện hành đã có Luật 91/2025 và Nghị định 356/2025; xem nguồn kiểm tra hiệu lực bên dưới.
- Câu 35/36 và chỉ dẫn đơn vị cấp huyện: tên Tòa án/Công an quận huyện cần cập nhật theo thay đổi tổ chức, không đưa nguyên văn vào sản phẩm.
- Câu 18: dẫn hệ PCCC cũ và áp số lối thoát/số bình cho mọi nhà trọ; cần rà theo pháp luật hiện hành, loại nhà, tầng, diện tích và quy chuẩn.
- Các số giá điện/nước, mức phạt, mốc 30 ngày, hoàn cọc 3–5 ngày, tỷ lệ “99% lừa đảo” và kết luận chắc chắn khởi tố chưa được xác minh đầy đủ trong lần đối chiếu này. Không dùng chúng làm tiêu chí bắt hệ thống phải khớp.

Các nguồn được mở/tra cứu ngày 04/10/2026; kiểm tra có chọn lọc, không chứng nhận toàn bộ 36 đáp án:

- [Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15](https://vanban.bocongan.gov.vn/co-so-du-lieu-van-ban/luat-bao-ve-du-lieu-ca-nhan-1753688803): Nguồn Bộ Công an xác nhận hiệu lực 01/01/2026; nhóm câu 29–32 phải rà theo khung hiện hành.
- [Nghị định 356/2025/NĐ-CP](https://datafiles.chinhphu.vn/cpp/files/vbpq/2026/01/356-nd.signed.pdf): Bản ký chính thức. Danh mục văn bản của cơ quan Cà Mau bên dưới xác nhận Nghị định 13/2023 hết hiệu lực từ 01/01/2026.
- [Danh mục văn bản tháng 12/2025, mục 45](https://files-vnportal.camau.gov.vn/gov-cmu/2649/FileQuanTriTinTuc/danh-muc-nd-qd-thang-12-2025.signed.signed.signed-1-639040686316440730.pdf): Xác nhận hiệu lực của Nghị định 356/2025 và việc Nghị định 13/2023 hết hiệu lực. Đây là kiểm tra hiệu lực, không xác minh mọi mức phạt/ngoại lệ của bộ đáp án.
- [Luật PCCC và CNCH 55/2024/QH15](https://vanban.chinhphu.vn/?classid=1&docid=212483&pageid=27160): Cổng Chính phủ xác nhận hiệu lực 01/07/2025; câu 18 không thể chỉ dẫn hệ văn bản cũ mà thiếu rà phạm vi/chuyển tiếp.
- [Nghị quyết 81/2025/UBTVQH15](https://chinhphu.vn/?classid=1&docid=214391&pageid=27160): Thành lập Tòa án nhân dân khu vực, hiệu lực 01/07/2025; tên Tòa án quận/huyện trong câu 35 cần cập nhật.
- [Bộ Công an: hướng dẫn tố giác từ 01/03/2025](https://www.bocongan.gov.vn/bai-viet/huong-dan-to-giac-bao-tin-ve-toi-pham-kien-nghi-khoi-to-tu-ngay-0132025-d2-t43729): Công an địa phương tổ chức theo cấp tỉnh/cấp xã; chỉ dẫn Công an quận/huyện trong câu 36 đã cũ.

## Bảng đối chiếu từng câu

| Câu | A (bao phủ 0–2) | B (bao phủ 0–2) | So với yêu cầu và bản dán | Điểm bản dán cần rà |
|---|---|---|---|---|
| 1 | 0: Chỉ trả mẫu chưa tổng hợp được kết luận; không có checklist. | 1: Có Điều 398, một phần Điều 163; kéo theo khối chuyển tiếp rất dài. | B có nội dung hơn A, nhưng cả hai thiếu checklist sáu nhóm dễ dùng như bản dán. | Mức cọc 1 tháng, hoàn 3–5 ngày và báo trước 30 ngày là ví dụ/thỏa thuận; không coi là quy tắc chung. |
| 2 | 1: Có định nghĩa cọc và thời hạn/phương thức thanh toán. | 1: Thêm căn cứ giá giao dịch; vẫn trích dài và thiếu kết luận trực tiếp. | Cả hai chưa chuyển thành các mục tiền cọc nếu có, giá thuê, ngày và cách thanh toán. | Câu “bắt buộc” và dẫn Điều 472/473 chưa chứng minh mọi hợp đồng phải có tiền cọc. |
| 3 | 2: Diễn giải thỏa thuận giá, kiểm tra hợp đồng và ngoại lệ cải tạo. | 1: Chỉ chọn ngoại lệ cải tạo nhà; thiếu nguyên tắc chung. | A trả lời trọng tâm rõ hơn. Không lấy kết luận tuyệt đối trong bản dán làm chuẩn. | Kết luận luôn được tiếp tục trả giá cũ/luôn được hoàn cọc cần điều kiện, ngoại lệ và căn cứ chấm dứt. |
| 4 | 1: Giải thích Điều 328 và ngoại lệ thỏa thuận; khuyên kiểm tra hợp đồng. | 1: Trích Điều 328 khoản 1/2 và ngoại lệ thỏa thuận. | Cả hai thiếu checklist bàn giao, chứng cứ nợ/hư hỏng và thời điểm hoàn cọc; A dễ đọc hơn. | Từ “chỉ” trong danh sách khấu trừ và kết luận hoàn 100% đang giản lược điều kiện hợp đồng. |
| 5 | 1: Trích giới hạn tổng tiền thu so với hóa đơn, kèm điều kiện hiệu lực. | 1: Có nhiều nhánh kê khai/định mức; cảnh báo chưa xác nhận sự kiện hiệu lực. | B rộng hơn nhưng dài; cả hai chưa xác định biểu giá và quy định áp dụng đúng kỳ. | Giá 2.167 đồng/kWh, VAT, sáu bậc và quyền lựa chọn cách tính chưa được xác minh theo kỳ hóa đơn. |
| 6 | 2: Nêu ba người bằng 3/4 định mức nếu kê khai đủ, kèm điều kiện hiệu lực. | 2: Có cùng quy tắc 3/4 trong trích đoạn dài. | Cùng bao phủ nguyên tắc định mức; A gọn hơn. Chưa có phép tính tiền theo biểu giá đã xác minh. | 37,5 kWh và cách chia các bậc phụ thuộc biểu giá, điều kiện kê khai và văn bản áp dụng. |
| 7 | 1: Hướng dẫn đối chiếu hóa đơn và định mức, có lưu ý hiệu lực. | 1: Trích quy định điện và ghi chú hiệu lực, chưa thành quy trình kiểm tra. | A dễ thực hiện hơn; cả hai thiếu checklist chỉ số đầu/cuối, kWh và căn cứ xử lý hiện hành. | Mức phạt 20–30 triệu, khoản/điều và hotline cần kiểm chứng; không suy ra vi phạm chỉ từ giá cao. |
| 8 | 0: Chọn kê khai số người và quyền bên bán điện yêu cầu thông tin cư trú. | 0: Trích rộng quy định người thuê, vẫn không trả lời nghĩa vụ thông báo số điện từng phòng. | Chưa trả lời đúng trọng tâm; không tự suy ra nghĩa vụ bảng kê bắt buộc từ nguồn này. | Câu “có” và bảng kê bắt buộc chưa gắn điều khoản cụ thể; khuyến nghị minh bạch không tự thành nghĩa vụ luật định. |
| 9 | 1: Nêu phân nhóm theo đơn vị, địa bàn; không khẳng định giá trọ cụ thể. | 1: Có bảng giá năm 2024 với phạm vi và phần phí chưa gồm. | B có số liệu nguồn rõ hơn; cả hai chưa xác nhận giá hiện hành cho đúng nhà cung cấp/phòng trọ. | Định mức 4 m³/người và khoảng giá 7.000–11.000 chưa có nguồn/địa bàn/đơn vị cấp nước cụ thể. |
| 10 | 2: Khuyên kiểm tra thỏa thuận, số đo, hóa đơn, đơn vị và kỳ sử dụng. | 1: Trích ghi chú giới hạn và yêu cầu xem thỏa thuận/số đo/hóa đơn. | A gần cách hướng dẫn thực hành của bản dán hơn; không lặp các mức khoán thiếu khảo sát. | Khoảng 30–50 nghìn và 80–100 nghìn chưa có khảo sát; mức cao tự nó chưa chứng minh sai quy định. |
| 11 | 0: Nêu biểu giá không quy định công thức chia nước; yêu cầu xem hợp đồng. | 0: Cũng chỉ nêu giới hạn nguồn, không đề xuất cách chia. | Cả hai thiếu lựa chọn thỏa thuận theo người hoặc đồng hồ phụ, cùng cách chia hao hụt/nước chung. | Hai phương án là gợi ý thỏa thuận, chưa phải hai cách bắt buộc theo luật. |
| 12 | 1: Nêu đơn vị, nhóm, khu vực, kỳ; có giá lịch sử và giới hạn chưa có quy trình. | 1: Chỉ trích các thuộc tính cần xác định trên hóa đơn. | Cả hai thiếu mã khách hàng, chỉ số và cách liên hệ đúng nhà cung cấp; cờ đầy đủ của B chưa chứng minh đủ bước. | Tên website/Zalo OA và cách tra cứu cần xác minh với đúng nhà cung cấp. |
| 13 | 1: Có điều kiện đăng ký tạm trú ngoài xã thường trú, ở từ 30 ngày. | 1: Có cùng điều kiện. | Cùng thiếu hướng dẫn hồ sơ/nơi nộp trong câu này; không đồng nhất điều kiện ở 30 ngày với hạn nộp 30 ngày. | Điều kiện ở từ 30 ngày trở lên không tự chứng minh thời hạn nộp hồ sơ là 30 ngày sau chuyển đến. |
| 14 | 1: Nêu nghĩa vụ công dân, hồ sơ và thiếu nguồn riêng về chủ trọ. | 1: Trích hồ sơ và tiếp nhận; cũng thừa nhận thiếu căn cứ nghĩa vụ chủ trọ. | A diễn giải rõ hơn; cả hai chưa giải quyết đầy đủ phần chủ nhà cần phối hợp/cung cấp giấy tờ gì. | Mức phạt theo Nghị định 144/2021 và quy trách nhiệm đồng thời hai bên cần cập nhật/xác minh. |
| 15 | 2: Checklist tờ khai, chứng minh chỗ ở, nơi nộp và thời gian xử lý. | 2: Có cùng hồ sơ/thủ tục, thêm đoạn gia hạn không cần cho câu hỏi. | Cả hai bao phủ hồ sơ cốt lõi; A dễ dùng hơn. Các yêu cầu CCCD/CT01/kênh online của bản dán cần rà thủ tục hiện hành. | Bản sao CCCD, chữ ký chủ nhà trên CT01 và kênh VNeID không được mặc định bắt buộc trong mọi hồ sơ. |
| 16 | 0: Chọn gia hạn và tờ khai; không nói rõ thủ tục khi đổi chỗ ở. | 0: Có hồ sơ/nộp mới nhưng không giải thích thay đổi địa chỉ và nơi cũ. | Cả hai chưa trả lời tình huống chuyển trọ. B được gắn đầy đủ dù thiếu ý cốt lõi. | Mốc 30 ngày, tự động xóa nơi cũ và chỉ điều chỉnh nếu cùng phường chưa được chứng minh trong bản ngoài. |
| 17 | 2: Checklist lối thoát, phương tiện, điện/bếp; có điều kiện loại nhà. | 2: Có các điều kiện tương ứng từ Luật 55/2024, ở dạng trích dài. | Bao phủ nhóm kiểm tra chính; A dễ dùng hơn, bản dán cụ thể hơn nhưng các yêu cầu kỹ thuật cần phân loại. | Lối thoát thứ hai, chìa khóa và kiểm tra bình phải phân biệt khuyến cáo với yêu cầu theo loại công trình. |
| 18 | 1: Nêu điều kiện chung và thiếu căn cứ riêng cho nhà trọ nhiều phòng. | 1: Có điều kiện chung, yêu cầu biết loại sử dụng, tầng và diện tích. | Cả hai giữ đúng giới hạn dữ kiện nhưng chưa thành checklist áp dụng cho công trình cụ thể. | Dẫn hệ văn bản PCCC cũ; hai lối thoát và mật độ bình bị khẳng định chung khi thiếu thông tin quy mô. |
| 19 | 0: Trích duy trì lối thoát và nội dung kiểm tra. | 0: Trích kiểm tra/thẩm quyền rất dài. | Cả hai thiếu bước yêu cầu mở/dọn, lưu bằng chứng và kênh phản ánh; bản dán có hành động nhưng tên cơ quan cần cập nhật. | Tên Đội PCCC quận/huyện cần cập nhật theo tổ chức địa phương, không mặc định tồn tại. |
| 20 | 2: Chia trách nhiệm người cho thuê/người thuê, an toàn điện và kiểm tra hợp đồng. | 2: Có cùng nhóm trách nhiệm và điều kiện điện/sạc xe. | Cả hai bao phủ trọng tâm; A diễn giải rõ hơn, chưa thành checklist hành vi cụ thể như bản dán. | CB từng phòng và các yêu cầu kỹ thuật cụ thể chưa gắn tiêu chuẩn/loại nhà trong bản ngoài. |
| 21 | 1: Nêu nghĩa vụ thông tin trung thực và phí thỏa thuận, thiếu danh mục công khai. | 1: Chỉ trích nghĩa vụ doanh nghiệp, có nhiều nội dung không liên quan người thuê. | Cả hai thiếu checklist chủ thể/liên hệ, quyền môi giới, thông tin phòng và điều kiện phí. | Chứng chỉ, biểu phí và cách nói hành nghề độc lập cần kiểm tra điều kiện chủ thể/điều luật. |
| 22 | 1: Khuyên kiểm tra ủy quyền/hợp đồng dịch vụ, tư cách người cho thuê. | 0: Chỉ chọn các trường hợp không bắt buộc có Giấy chứng nhận. | A sát yêu cầu xác minh hơn; B bỏ mất quyền nhận cọc/thông tin phòng. Cả hai thiếu checklist trước khi chuyển tiền. | Bắt buộc chỉ ký/trả tiền trực tiếp chủ nhà có thể bỏ qua đại diện được ủy quyền hợp pháp. |
| 23 | 1: Nêu trung thực, bồi thường do lỗi và xem hợp đồng; chưa có căn cứ hủy/đòi cọc. | 1: Trích nghĩa vụ trung thực/bồi thường, không đưa bước xử lý. | Cả hai có quyền liên quan nhưng thiếu ghi nhận chênh lệch, yêu cầu giải trình/khắc phục và rà điều kiện phí. | Quyền từ chối bất kỳ khoản phí và hoàn phí tự động cần hợp đồng, vi phạm và căn cứ áp dụng. |
| 24 | 0: Có quyền thu phí theo thỏa thuận; chưa nói nội dung giấy tờ. | 0: Trích quyền thu phí cùng các quyền khác; chưa có mẫu/thành phần thỏa thuận. | Cả hai thiếu chủ thể, dịch vụ, mức phí, điều kiện phát sinh/hoàn phí và biên nhận. | Điều kiện chỉ trả khi ký thuê thành công và luôn hoàn tiền là nội dung cần thỏa thuận, không mặc định. |
| 25 | 1: Có kiểm tra danh tính/liên hệ/xác thực nền tảng và cảnh báo OTP. | 1: Có nghĩa vụ nền tảng và cảnh báo trực tuyến, ở dạng trích rộng. | Cả hai thiếu đối chiếu phòng thật/ảnh/quyền cho thuê; bản dán có nhiều mẹo hơn nhưng tỷ lệ 99% không có chứng cứ. | Con số 99% lừa đảo không có dữ liệu; tích xanh và tuổi tài khoản không bảo đảm quyền cho thuê. |
| 26 | 1: Hướng dẫn dùng kênh công khai, thừa nhận chưa biết nút/biểu mẫu/email cụ thể. | 1: Chỉ trích yêu cầu có quy trình phản ánh công khai. | A dễ thực hiện hơn; cả hai thiếu checklist bằng chứng và quy trình trên nền tảng cụ thể. | Nút Report và chức năng đính kèm bằng chứng chưa được xác nhận trên nền tảng cụ thể. |
| 27 | 2: Nêu xác thực, công khai thông tin, kiểm soát nội dung và khiếu nại có điều kiện phân loại. | 2: Có cùng nghĩa vụ, thêm phân biệt có chức năng đặt hàng. | Cả hai bao phủ nhóm trách nhiệm chính theo nguồn lưu; B rộng hơn nhưng chưa chứng minh phân loại sản phẩm cụ thể. | Dẫn Nghị định 52/85 và yêu cầu gỡ ngay cần rà chuyển tiếp, loại nền tảng và thời hạn cụ thể. |
| 28 | 2: Cảnh báo link/QR/OTP, xem phòng/xác minh và bước khi nghi lừa đảo. | 2: Trích đủ hai khuyến cáo tương ứng. | Cả hai gần nội dung an toàn của bản dán; A dễ đọc hơn, không tự kết luận tội từ một dấu hiệu. | Các dấu hiệu là cảnh báo rủi ro; không kết luận tội phạm chỉ từ liên kết rút gọn. |
| 29 | 0: Có một mục tờ khai cư trú và nguyên tắc đồng ý. | 0: Chỉ chọn nguyên tắc đồng ý. | Cả hai chưa liệt kê dữ liệu tối thiểu cho hợp đồng/cư trú theo từng mục đích. | Không coi toàn bộ danh sách ngày sinh, điện thoại, giấy sinh viên là bắt buộc cho mọi hợp đồng. |
| 30 | 0: Chỉ trả mẫu chưa tổng hợp được kết luận. | 1: Có giới hạn mục đích/phạm vi và thông tin khi đồng ý xử lý. | B có nội dung hơn; vẫn thiếu lưu bao lâu, ai truy cập, bảo mật/xóa và căn cứ ngoại lệ. | Nghị định 13/2023 đã được văn bản mới thay thế; cấm chuyển giao khi chưa đồng ý cần xét ngoại lệ luật. |
| 31 | 1: Có công khai khi đồng ý và hình thức công khai, thiếu ngoại lệ khác. | 1: Có đầy đủ hơn các trường hợp được công khai và nguyên tắc mục đích. | B rộng hơn A; cả hai chưa áp dụng trực tiếp vào việc chủ trọ đăng CCCD/điện thoại trong tình huống cụ thể. | Câu “hoàn toàn không” và mức phạt 10–20 triệu quá chung; cần xác định hành vi, chủ thể và văn bản hiện hành. |
| 32 | 1: Có thủ tục/thời hạn yêu cầu xóa và gia hạn. | 1: Thêm rút đồng ý/ngừng xử lý và yêu cầu bảo vệ dữ liệu. | B có nhiều lựa chọn hơn nhưng vẫn thiếu cách gửi yêu cầu, bằng chứng và hướng dẫn khi bên nhận không xử lý. | Chỉ dẫn Sở Thông tin và Truyền thông và dùng Nghị định 13/2023 cần cập nhật cơ quan/văn bản. |
| 33 | 2: Có dấu hiệu cọc trước/chưa kiểm chứng, xem phòng/xác minh, lưu bằng chứng. | 2: Có cùng khuyến cáo xem phòng/xác minh và trình báo. | Cả hai gần lời khuyên an toàn của bản dán; A tóm tắt dễ dùng hơn. | Các dấu hiệu không đủ tự kết luận đã cấu thành tội lừa đảo. |
| 34 | 2: Có loại chứng cứ, cơ quan tiếp nhận và hình thức gửi. | 2: Có cùng khuyến cáo và quy định tiếp nhận ở dạng trích nguyên. | Cả hai bao phủ trọng tâm; cần thêm tài khoản/link người đăng và kênh cụ thể đã xác minh nếu muốn chi tiết như bản dán. | Tên đơn vị PA05/Đội và nơi tiếp nhận cụ thể cần rà; không bảo đảm ngân hàng sẽ thu hồi được tiền. |
| 35 | 0: Chỉ có định nghĩa cọc và khuyến cáo thuê trọ; chưa phân biệt hai trường hợp. | 1: Có định nghĩa cọc và Điều 174 về gian dối chiếm đoạt. | B có thêm căn cứ nhưng chưa giải thích tiêu chí dân sự/hình sự; bản dán làm phần phân biệt rõ hơn. | Tòa án cấp quận/huyện là tên mô hình cũ; việc không hoàn cọc tự nó chưa quyết định dân sự/hình sự. |
| 36 | 1: Có lưu bằng chứng và tiếp nhận tố giác chung. | 1: Thêm cơ quan tiếp nhận và hình thức gửi, vẫn là hướng dẫn chung. | Cả hai thiếu danh sách từng nạn nhân, từng giao dịch và liên hệ chung; không lặp lời hứa chắc chắn khởi tố của bản dán. | Công an quận/huyện là chỉ dẫn cũ; nhiều nạn nhân không tự chứng minh tính chuyên nghiệp, tăng khung hay chắc chắn khởi tố. |

## Phương án rút ra từ đối chiếu

Với câu hỏi pháp lý, B là ứng viên tốt để chọn bằng chứng; A cho thấy lợi thế khi diễn giải ngắn và sát yêu cầu. Hướng cần thử tiếp là **Gemini phân tích → truy xuất → Qwen chọn bằng chứng → Gemini diễn giải thành câu trả lời ngắn/checklist → kiểm chứng từng mệnh đề với nguồn và hiệu lực**. Đây là thiết kế đề xuất, chưa được chạy hay chứng minh tối ưu bằng kết quả hiện tại.

Đầu ra nên có kết luận có điều kiện, 3–5 bước thực hiện và 1–3 trích dẫn phù hợp; khi thiếu dữ kiện cần hỏi cụ thể. Tránh chèn toàn khối chuyển tiếp vào câu trả lời. Trước khi thử lại, bổ sung nguồn thực hành đã rà, nguồn hiệu lực và quy trình đúng cho các câu thiếu ở bảng.

Bản dán dùng làm mục tiêu về cấu trúc và độ hữu ích; cần rà từng mệnh đề trước khi dùng làm ground truth. Ưu tiên cải thiện câu 1, 8, 11, 16, 19, 24, 29, 30, 35, 36.

[Nguyên văn ba đáp án cho đủ 36 câu](gemini_qwen_vs_pasted_2026-10-04_details.md) · [JSON và nhãn rà](gemini_qwen_vs_pasted_2026-10-04.json) · [Đối chiếu A/B và phương pháp RAGAS](gemini_vs_qwen_2026-10-04.md)

Tái lập: `python -X utf8 eval/compare_three_legal_answers.py`. Script chỉ dựng báo cáo, không gọi model. SHA-256 tệp đầu vào:

- `eval\datasets\external_legal_20261004\answers.json`: `0c5e59da7b3c5abd1d4755b5736421675c8dc40f0bdd132cb187bb4fb587ee8e`
- `eval\reports\legal_gemini38_retest_2026-10-04_fixed.json`: `e1474a6f9523521af2163a15058318cb58fa05b75e0de70837130245d135da34`
- `eval\reports\legal_gemini_qwen_compare_2026-10-04.json`: `7983a51ef9a18ebc832eea68a24f915262560108e704f80df264022bc32415de`
- `eval\ragas_reports\gemini_vs_qwen_2026-10-04.json`: `a941e9ef6cd56593e720d3ec614b73998332dd20da5d2fe22da23e29b1b1fa49`
