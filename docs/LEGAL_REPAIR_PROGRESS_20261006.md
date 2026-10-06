# Rà bộ chấm và workflow pháp lý — 06/10/2026

Bộ mẫu gốc và `CTU_LEGAL_REVIEW_36.md` được giữ nguyên. Bản đăng ký rà theo từng ý nằm ở `eval/datasets/external_legal_20261004/point_review_20261006.json`: 36 câu, 161 ý; hiện 139 ý còn chờ đối chiếu nguồn từng mệnh đề, 22 ý có ghi chú phạm vi hoặc căn cứ cần xử lý riêng. Đây chưa phải bộ đáp án pháp lý đã xác minh đầy đủ.

## Thông tin giá do chủ trọ cung cấp

Giá điện/nước của từng nhà trọ là biến đầu vào do chủ trọ cung cấp. Có thể để trống và hỏi sau; thiếu giá không phải bằng chứng nhà trọ thu sai và không được tự điền một giá mặc định. Kiểm tra giá trị/đơn vị chỉ áp dụng khi câu trả lời thực sự khẳng định một mức giá. Quy định cách thu điện là câu hỏi pháp lý riêng, cần đọc điều kiện nguồn.

`eval/reports/local_utility_prices_20261006.json` chỉ thống kê các quảng cáo có giá, đơn vị và thời điểm trong 789 bản ghi đang có. Không có trường giá điện/nước có cấu trúc. Có 20 bản ghi ghi nước theo m³ và 2 bản ghi ghi theo người/tháng; chúng không chứng minh mức phổ biến toàn Cần Thơ, mức tiêu thụ 3–5 m³ hay một ngưỡng giá cao chung. Không gửi bản ghi nhà trọ lên Gemini.

## Thay đổi đã thực hiện

- Bộ chấm dùng đoạn nguyên văn theo câu, giữ mệnh đề dài và điều kiện sau dấu chấm phẩy. Một ý chọn được nhiều ID thật; mã khôi phục nguyên văn các đoạn và kiểm tra lỗi số liệu bằng giá trị, đơn vị, chủ thể, sự kiện và điều kiện.
- Lỗi số liệu cung cấp giá trị cần tìm, số liệu đã thấy và các đoạn ứng viên/kế tiếp để Qwen đối chiếu lại. 30.000 đồng/30 nghìn đồng và 3/4 định mức/75% tương đương; ngày/tháng và thời gian sinh sống/thời hạn nộp hồ sơ khác nhau.
- Kết luận tổng hợp có ID riêng và phân loại quy định, thao tác, khuyến nghị hoặc giới hạn nguồn. Kiểm chứng trả ID kết luận, ID nguồn và lý do. Một lần sửa có giới hạn giữ nguyên ý đã được chấp nhận; sau đó có thể giữ các ý còn được nguồn hỗ trợ và đánh dấu phần thiếu. Khi không đủ verdict hoặc toàn bộ bị bác bỏ, không giữ một bản tổng hợp chưa kiểm chứng.
- Truy xuất bổ sung căn cứ về xóa/điều chỉnh cư trú và hợp đồng dịch vụ; nhận diện link giả, yêu cầu OTP/mật khẩu và thúc ép thao tác được lấy từ cảnh báo Bộ Công an. Hướng dẫn phòng ngừa không được diễn đạt thành kết luận phạm tội.

## Rà nguồn cho nhóm ưu tiên

| Câu | Kết quả và giới hạn |
|---|---|
| 26 | [EVNSPC](https://cskh.evnspc.vn/TinTuc/TinTucChiTiet?LoaiTinBai=ALL&MaTinBai=3103) hướng dẫn công khai cách tính, đối chiếu hóa đơn; bài này chưa chứng minh mọi chủ trọ phải có bảng kê đủ các cột của mẫu. Phân biệt khuyến nghị đối chiếu với nghĩa vụ luật định. |
| 28 | Thống kê quảng cáo cục bộ có mẫu số/thời điểm; chưa có nguồn cho mức khoán phổ biến, lượng tiêu thụ hay ngưỡng cao trong mẫu. |
| 29 | Cách phân chia chi phí theo người/đồng hồ phụ cần được trình bày là phương án thỏa thuận, không gọi là công thức bắt buộc. |
| 31 | Điều kiện sinh sống từ 30 ngày trở lên không phải căn cứ cho thời hạn nộp trong 30 ngày. |
| 32 | Trọng tâm là trách nhiệm công dân/chủ hộ và chứng minh chỗ ở, có xét khai thác dữ liệu thay giấy tờ. Phần phạt là ý phụ: [Chính phủ](https://xaydungchinhsach.chinhphu.vn/muc-phat-hanh-vi-khong-thuc-hien-dung-quy-dinh-cua-phap-luat-ve-dang-ky-tam-tru-119251104164040733.htm) giới thiệu NĐ282/2025 có hiệu lực 15/12/2025; cần phân biệt cá nhân/tổ chức, hành vi và cảnh cáo/phạt tiền. Không giữ căn cứ cũ chỉ để khớp mẫu. |
| 34 | Bổ sung Điều 26/29 từ Word Luật Cư trú đang có; không suy ra tự động xóa đăng ký cũ, mọi đổi phòng cùng phường là điều chỉnh, hoặc hạn nộp 30 ngày. Thao tác hệ thống cần nguồn thủ tục riêng. |
| 36 | Chưa xác nhận hai lối thoát và hai bình mỗi tầng là yêu cầu chung; cần công năng, tầng, quy mô và tiêu chuẩn tương ứng. Giữ giải thích cơ bản theo phần nguồn đang có. |
| 45 | Bổ sung Điều 513/516/519/520 BLDS từ Word; quyền giảm phí/chấm dứt và thanh toán phần đã làm phụ thuộc điều kiện. Chưa có căn cứ tự động hoàn 100% phí. |
| 50 | Bổ sung trích đoạn cảnh báo chính thức cho link giả, bí mật tài khoản và thúc ép; các dấu hiệu phải được trình bày trực tiếp trong câu trả lời, có giữ bối cảnh nguồn. |
| 58 | Tập hợp chứng cứ chung và từng giao dịch; không biến mẫu đơn tập thể thành điều kiện tiếp nhận hay tự suy ra tính chuyên nghiệp/khung tăng nặng từ nhiều người bị hại. |

## Corpus thử và bảo toàn dữ liệu

Corpus thử `legal_word_repair_v14_20261006` có 38 tài liệu, 465 chunk/vector 384 chiều; graph thử `graph_rag_word_repair_v14` và dữ liệu nhà trọ `housing_graph_word_repair_v14` giữ đủ 789 bản ghi/vector. Không OCR/PDF, không nhúng đáp án mẫu hoặc thống kê giá nhà trọ vào corpus pháp lý.

`eval/reports/legal_repair_audit_v14_20261006.json` xác nhận hash bộ mẫu và các bảng đang dùng không đổi; dữ liệu nhà trọ thử giống dữ liệu đang dùng. Corpus mới còn staging, chưa chuyển cấu hình API đang chạy.

## Chạy thử

Các lượt `saved_focus_v9b`, `v9c`, `v10`, `v11`, `v12` là thử nghiệm phát triển bộ chấm; không dùng chúng để công bố cải thiện. Phiên bản v11 thống nhất thứ tự trường của các nhánh schema. Phiên bản v12 bắt buộc một slot cho mỗi đoạn/ý mẫu, giữ nguyên mệnh đề trong đoạn gốc. Phiên bản v13 giới hạn `matched` cho ý có số liệu vào các tổ hợp ID thật đã qua kiểm tra giá trị/đơn vị/sự kiện; mã không tự chọn quote hoặc đổi nhãn. Danh sách tổ hợp được tìm có giới hạn, không chứng minh tương đương ngữ nghĩa; Qwen vẫn phải đối chiếu chủ thể/điều kiện và có thể chọn `different`/`missing`. Ví dụ câu 31 phải rà cả điều kiện sinh sống và mệnh đề thời hạn nộp trong mẫu, dù mệnh đề thứ hai chưa có căn cứ.

Đã chấm lại các câu đã lưu 23/27/31 bằng v13: 3/3 qua kiểm tra nguyên văn/số liệu, cả ba khớp mẫu một phần. Các khác biệt trong mẫu vẫn được giữ trong báo cáo, gồm mệnh đề hạn nộp ở câu 31.

Lượt sinh đầu bị phê duyệt tự động từ chối vì nghi ngại cấu hình agents/synthesis có thể gửi listing tới Gemini. Đã thêm chốt chặn `--legal-only`: chỉ câu hỏi pháp lý trong bank, vô hiệu truy xuất listing, kiểm tra cặp document_id/chunk_id thuộc corpus pháp lý trước tổng hợp và kiểm chứng cloud. Compose thử không mount catalog nhà trọ. Kiểm tra trước chạy xác nhận 16/16 tuyến pháp lý, không gọi model; 3 kiểm thử chặn listing/nguồn giả đạt. Lệnh có chốt chặn đã được phê duyệt và nhóm 16 câu đang sinh trong `legal_repair_pilot_v14_20261006.json`.

Bộ kiểm tra số liệu v14 bổ sung số lượng người/hộ, lối thoát, bình, tầng/phòng và hồ sơ; phân biệt hồ sơ với hộ gia đình, giữ hai đầu mút khoảng số tầng. 44 kiểm thử bộ chấm đã đạt. Báo cáo cuối phải chấm lại cả hai bản bằng cùng v14/hash; không trộn điểm các phiên bản thử trước.

Lượt thử v14 đã sinh đủ 16/16 câu, không lỗi, trích dẫn 1,0, không gọi cloud với housing. Tìm được lỗi còn lại: bỏ dấu nhầm “trú” thành “trừ” ở cuối khoản; điều kiện nhập IDKH trong hướng dẫn bị coi là nghĩa vụ luật; phủ định “không phải đường dây...” bị coi là “phải”; lý do kiểm chứng hiển thị không đủ ngữ cảnh khiến bộ kiểm tra đọc như một kết luận mới. Đã sửa, tái hiện trên các bản tổng hợp đã lưu của 30/31/37 đều không còn lỗi chặn giả. Các ngoại lệ thực sự bị cắt và các nghĩa vụ/hoàn tiền không có nguồn vẫn bị chặn.

111 kiểm thử workflow/nguồn/chốt chặn đã đạt sau sửa. Lượt thử mới `legal_repair_pilot_v15_20261006.json` đang sinh cùng 16 ID trên cùng corpus v14, với hash pipeline mới. Lỗi kind được đánh dấu ở từng kết luận và có loại cũ/loại cần sửa; không làm mất verdict hợp lệ của ý khác. Đây là lượt cần kiểm tra trước khi chạy đủ 36 câu.

Khi lượt thử đạt mới sinh đủ 36 câu cùng ID/câu hỏi của bank. Chỉ chấm sau khi câu trả lời hoàn tất và so sánh cả baseline `c8dba04` lẫn bản sửa bằng cùng hash tiêu chí. Câu 49 trong bank có thêm “người bán” so với câu hỏi đi kèm mẫu; hai lượt giữ cùng câu hỏi bank, báo cáo phải công khai khác biệt với mẫu. Không coi cờ kiểm chứng lúc chạy là chứng nhận hiệu lực pháp luật độc lập.

## Cập nhật nguồn cư trú và lượt thử v16

Lượt thử v15 hoàn tất 16/16, không lỗi thực thi, trích dẫn 1,0. Câu 30/31/37 đã giữ bản tổng hợp kiểm chứng. Câu 34/45 cho thấy còn vấn đề chọn khoản: khoản cấm nơi đăng ký được ưu tiên hơn cập nhật nơi mới, khoản giá thị trường được chọn thay khoản giảm phí do chất lượng không đạt thỏa thuận. Đã sửa truy xuất theo nội dung nguồn và thêm kiểm thử. Khi writer sửa không hợp lệ, giữ bản trước để kiểm chứng từng ý và giữ phần được hỗ trợ; không mất mọi kết luận chỉ do JSON sửa lỗi hỏng.

Đã lấy Word gốc từ [Công báo NĐ154/2024](https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-154-2024-nd-cp-43275.htm) và [Công báo NĐ58/2026](https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-58-2026-nd-cp-468975/62899.htm). Trích khoản 1 Điều 5 về khai thác dữ liệu và cung cấp giấy tờ có điều kiện; khoản 2/5/7 Điều 4 NĐ58 về văn bản chỗ thuê, hình thức lấy ý kiến và xóa tạm trú theo từng trường hợp; giữ điều hiệu lực. Không dùng bản trích tuyển nghiên cứu làm nguyên văn luật, không giữ Điều 10 và điểm a khoản 3 Điều 5 bản cũ đã sửa. Bổ sung Điều 23 Luật Cư trú để đọc đúng dẫn chiếu về nơi không được đăng ký mới.

Corpus thử cuối `legal_word_repair_v16_20261006`: 40 tài liệu, 478 chunk/vector; graph thử 1.300 node, 3.216 edge; 789 bản ghi/vector nhà trọ cục bộ. Audit v16 xác nhận dữ liệu đang dùng, mẫu gốc và housing không đổi; corpus vẫn staging. 114 kiểm thử workflow/truy xuất/chốt chặn và 44 kiểm thử bộ chấm đạt. Lượt `legal_repair_pilot_v16_20261006.json` đang chạy 12 câu ưu tiên và 4 câu hồi quy với chốt pháp lý.

Hash pipeline nguyên byte của `c8dba04` là `de8b30183da45706a7cf5f757c550c097a65da17a2cfa7c4e86e8b8e359f275b`, khớp baseline v20 đã lưu. Bộ chấm đóng băng: `f52d08cda4ccc8284f2e57bac0979309ab88c8cafc712771105a0da31327ffe1`; kiểm tra số liệu: `7f3cca4957b5e72323d925d63a7cff966ba4df50c8ff95c07f3b281069784eb3`.

Lượt thử v16 hoàn tất 16/16, không lỗi thực thi, trích dẫn 1,0, không gọi cloud với housing. Câu 32/34/45 giữ được phần tổng hợp theo nguồn mới; câu 28 cho thấy lý do bác bỏ do verifier viết có thể bị hiểu như kết luận luật mới khi chèn vào bản giữ lại. Đã giữ nguyên toàn bộ lý do và ID trong trace, bỏ việc chèn các chẩn đoán chưa được kiểm chứng vào câu trả lời. Tái hiện câu 28 đã lưu: các ý hợp lệ được giữ, không còn lỗi quy tắc. 115 kiểm thử workflow đạt sau sửa này.

Bắt đầu lượt đầy đủ `legal_repair_36_v17_20261006.json`, cùng corpus v16 và 36 câu hỏi bank. Chưa công bố điểm; hai lượt chấm cùng bộ chấm v14 sẽ thực hiện sau khi sinh xong.

## Kiểm tra lượt đầy đủ và sửa cảnh báo ngắn

Lượt v17 đã sinh 36/36 câu, không lỗi thực thi, mọi câu dưới 3.500 ký tự (dài nhất 2.644), trích dẫn theo định dạng đạt 1,0; provider cuối cả 36 là Gemini-agent. Cờ nguồn có 11 câu đầy đủ và 25 câu một phần, so với baseline 20/16. Không gọi cloud với dữ liệu nhà trọ. Đây chưa phải bằng chứng cải thiện tổng thể; cần xem từng ý và chấm cùng tiêu chí.

Các câu có cờ một phần vẫn có câu trả lời. Trường `no_answer` lúc chạy cũng được bật cho phản hồi một phần; không được tính nó thành số câu rỗng hoặc dùng `not no_answer` làm số câu đã sinh. Câu 37 giữ hướng dẫn phòng ngừa, thoát nạn và gọi 114 nhưng bỏ kết luận phụ “chỉ được gọi…” chưa được nguồn xác nhận như một giới hạn pháp lý tuyệt đối.

Đối chiếu câu 50 tìm được đoạn cảnh báo “không truy cập đường link lạ” đã truy xuất nhưng bị bộ chọn nguồn loại vì dưới 30 ký tự. Đã cho phép đoạn hướng dẫn ngắn nguyên văn có metadata nguồn chuyển đổi từ bài của cơ quan phát hành và cảnh báo phạm vi; đoạn ngắn không có provenance hoặc chỉ có một từ vẫn bị loại. Kiểm thử xác nhận đoạn này còn nguyên văn và được bổ sung khi checklist thiếu phần liên kết. Writer được nhắc dùng đúng loại chứng cứ nguồn nêu cho câu 58; verifier phân biệt khuyến nghị nhóm từng người với việc thêm giấy tờ hoặc nghĩa vụ mới.

116 kiểm thử workflow/truy xuất/chốt dữ liệu đã đạt sau sửa; 44 kiểm thử bộ chấm đã đạt và bộ chấm vẫn giữ nguyên hash v14. Bắt đầu `legal_repair_pilot_v18_20261006.json` với cùng 12 câu ưu tiên và 4 câu hồi quy, corpus v16. Bản chấm baseline đã lưu 5 câu hợp lệ sẽ tiếp tục bằng cùng tiêu chí; chưa có bảng so sánh đầy đủ.

Sau gián đoạn, lượt thử v18 tiếp tục từ hai câu đã lưu bằng cùng hash pipeline `407412542bfaba1e4965b2a6d2d90f6a471489ae394a95c910f7416f76888157`. Audit corpus/dữ liệu sau khi Docker khởi động lại vẫn đạt. Bản rà từng ý bổ sung bảy ghi chú: giá do chủ trọ cung cấp là biến tùy chọn; điều kiện đồng thời của điện; bảng nước theo nhóm chưa chứng minh bậc thang hoặc định mức theo người; chú thích VAT trong bản Word trái mệnh đề mẫu; hướng dẫn hóa đơn chưa chứng minh trần thu nước nội bộ; chứng từ cùng kịch bản chưa tự xác lập tính có tổ chức. Còn 139 ý chờ xác minh, 22 ý được ghi vấn đề/phạm vi cụ thể; không coi 22 ý này là đã xác nhận đúng luật. Cập nhật bản rà không thay `answers.json`, câu hỏi bank hoặc file tiêu chí nguồn dùng trong hai lượt chấm đã đóng băng.

Lượt v18 hoàn tất 16/16, không lỗi thực thi, trích dẫn 1,0, không có cloud housing. Câu 50 đã có checklist trực tiếp về link, OTP/thông tin ngân hàng và thúc ép chuyển cọc; câu 58 giữ tin nhắn, tài khoản ngân hàng và phiếu giao dịch của từng người. Còn lỗi ở câu 31: writer lặp nhãn procedure cho quy định thời hạn dù đã nhận lỗi kind cụ thể. Đã chuẩn hóa riêng nhãn của ID bị bác bỏ theo đề xuất phân loại của verifier, giữ các ý đã chấp nhận, rồi vẫn chạy lại toàn bộ kiểm chứng nội dung/nguồn/phân loại. Kiểm thử xác nhận nội dung sai vẫn bị loại sau khi nhãn được sửa; không tự chấp nhận verdict cũ.

Câu 45 thiếu khoản giảm phí trong truy xuất thật dù corpus có nguồn. Bổ sung từ vựng chất lượng dịch vụ/giảm phí trong query; tái hiện với E5 và DB staging (không Qwen/Gemini) đã lấy khoản 4 Điều 519 ở hạng đầu. Sửa cờ phạm vi để không nhầm nghĩa vụ doanh nghiệp và hợp đồng khách hàng thành thù lao giữa cá nhân môi giới/doanh nghiệp; cờ thù lao riêng vẫn được giữ khi đúng phạm vi. 125 kiểm thử workflow và 44 kiểm thử bộ chấm đạt, tổng 169. Bắt đầu lượt xác nhận `legal_repair_pilot_v19_20261006.json`; các lượt v17/v18 là bản phát triển và sẽ không trộn vào bảng so sánh cuối.

## Giá điện do chủ trọ cung cấp

Theo làm rõ của người dùng, giá điện thực tế là biến có thể bổ sung sau khi hỏi chủ trọ; việc có dữ liệu phụ thuộc nhà trọ cung cấp. Trường này là tùy chọn. Thiếu giá được hiểu là chưa có thông tin, không gán bằng 0, không suy từ tin khác và không tính thành lỗi thiếu dữ liệu nhà trọ. Khi câu trả lời nêu một giá cụ thể mới kiểm tra giá trị, đơn vị, nguồn và thời điểm. Các điều kiện tính/thu tiền trong câu hỏi pháp lý được rà riêng theo nguồn, không dùng sự vắng mặt của giá trong listing làm bằng chứng sai pháp luật.

Lượt xác nhận v19 hoàn tất 16/16, không lỗi thực thi, mọi provider cuối là Gemini-agent, trích dẫn định dạng 1,0, dài nhất 2.421 ký tự và không có cloud housing. Cờ nguồn có 6 đầy đủ/10 một phần. Câu 31 giữ điều kiện sinh sống 30 ngày, thời hạn tạm trú hai năm và gia hạn; câu 45 lấy khoản giảm phí theo chất lượng thỏa thuận, không hứa tự động hoàn toàn bộ; câu 50 có checklist trực tiếp và câu 58 giữ các loại chứng cứ giao dịch. Các câu hồi quy 37/47/52 có cờ đầy đủ; câu 29 giữ giới hạn nguồn về công thức chia tiền nước. Hash pipeline đóng băng cho lượt đầy đủ là `ef42a4633f539a7734bc3d484213d0d9575be0a70427ea1a1da017062603cab2`. Bắt đầu sinh đủ 36 câu trong `legal_repair_36_v20_20261006.json`, không trộn câu trả lời của các pipeline phát triển trước.

## Lượt đầy đủ cuối v20

Đã sinh đủ 36/36 câu, cùng ID và câu hỏi với baseline `c8dba04`, không lỗi thực thi. Provider cuối cả 36 là Gemini-agent; cờ nguồn có 14 đầy đủ và 22 một phần, trích dẫn định dạng 1,0, không có cloud housing. Đây là cờ kiểm chứng lúc chạy, chưa chứng minh cải thiện chất lượng pháp lý tổng thể so với baseline 20 đầy đủ/16 một phần.

Không câu nào vượt 1.000 từ khi đếm theo khoảng trắng. Câu 32 dài nhất theo số từ: 583 từ/2.559 ký tự. Độ dài lớn nhất theo ký tự của toàn bộ lượt là 2.673, dưới giới hạn 3.500 ký tự. Giới hạn ký tự và phép đếm từ là hai chỉ số riêng, không đổi giới hạn chỉ vì người dùng hỏi thống kê.

Hash câu trả lời đầy đủ cuối: `243ef304ea04ce7bd22352e8852d19d51d22b5e7a654beb4f5350f8f9c93c3d0`. Không chạy lại chương trình sinh trên file này sau khi hoàn tất, để giữ nguyên đầu vào chấm. Wrapper `eval/run_legal_repair_comparison.py` đã kiểm tra đủ 36 câu/cùng câu hỏi/hash pipeline/chốt legal-only trước khi tiếp tục bản chấm baseline đã lưu năm câu. Sau baseline sẽ chấm bản sửa bằng cùng bộ chấm v14 rồi xuất bảng so sánh; chưa công bố nhãn của phần chưa chấm.

## Bộ chấm cuối v15: giữ xuống dòng Word trong mệnh đề

Rà nguyên văn trace câu 31 cho thấy ba dòng Word của cùng một mệnh đề cư trú còn được coi là ba ID riêng. Đã gom các xuống dòng giữa mệnh đề theo vị trí nguyên văn; giữ tách đoạn trống, gạch đầu dòng, câu hoàn tất và giữ chữ viết tắt địa danh như `TP. Cần Thơ`. Điều kiện và chủ thể nằm cùng đoạn; các mệnh đề độc lập vẫn chọn được nhiều ID. Không nối lại bằng chữ do model viết và không sửa câu trả lời đã lưu.

49 kiểm thử bộ chấm đạt, gồm năm trường hợp mới về xuống dòng, chủ thể cư trú/thời hạn nộp, CRLF/điều kiện, các đoạn riêng và viết tắt địa danh. Cộng 125 kiểm thử workflow đã đạt, tổng 174. Bộ chấm đóng băng v15 có hash `6dadc7d34a6a1f49a6e3f7f6b4463dc6de75fe933bb4ae5c1020d1f12fcb198a`; hash kiểm tra số liệu giữ `7f3cca4957b5e72323d925d63a7cff966ba4df50c8ff95c07f3b281069784eb3`.

Lượt chấm v14 dừng sau 19 câu baseline và chỉ giữ như kết quả phát triển. Cả baseline và bản sửa được chấm lại từ đầu bằng cùng v15 trong `legal_repair_baseline_36_v15_20261006.json` và `legal_repair_new_36_v15_20261006.json`. Không trộn nhãn của hai giao thức đoạn. Hash pipeline/corpus, 36 câu hỏi, mẫu gốc và toàn bộ câu trả lời vẫn giữ nguyên. Bảng so sánh cuối sẽ dùng hai file v15.

## Kết quả chấm cuối

Hai lượt v15 đã chấm đủ 36/36, tổng 72/72 câu qua kiểm tra nguyên văn, không có câu chưa chấm. Cùng ID/câu hỏi, model, hash mẫu/bản rà nguồn, bộ chấm và bộ kiểm tra số liệu; `answers.json` và bản thảo gốc không đổi. Khớp mẫu sau audit: baseline 9 high/25 partial/2 low; bản sửa 12 high/23 partial/1 low. Câu 36 từ low lên partial; 38/43/49/51/56 từ partial lên high; 30/48 từ high xuống partial. Các câu hồi quy 29/37/47/52 giữ nhãn. Không diễn giải các nhãn này thành phần trăm chính xác pháp luật.

Cờ nguồn lúc chạy: baseline 20 đầy đủ/16 một phần (hai đầu ra đầy đủ không có kiểm chứng độc lập sau fallback); bản sửa 14 đầy đủ/22 một phần, cả 36 provider cuối Gemini-agent. Các cờ dùng workflow/corpus khác phiên bản, không phải phép đo độ chính xác pháp lý cùng tiêu chí. Không còn lỗi kind ở lần kiểm chứng cuối; bốn câu giữ các ý đã được hỗ trợ. Các kết luận ứng viên bị bác bỏ về nội dung ở 38/54 không được đưa vào phần giữ lại. Bản rà 161 ý vẫn có 139 ý chờ đối chiếu nguồn, 22 ghi chú cụ thể; không chấm bản rà như gold đã xác minh.

Không câu nào vượt 1.000 từ trong cả baseline và bản sửa, đếm theo khoảng trắng. Bản sửa dài nhất 583 từ ở câu 32; dài nhất theo ký tự 2.673. Giá điện/nước do chủ trọ cung cấp vẫn là biến tùy chọn, chưa có thì hỏi sau, không mặc định 0 hoặc tính là lỗi thiếu dữ liệu tin trọ. Không chuyển corpus staging sang API đang dùng.

Bản đọc cuối: `docs/LEGAL_REPAIR_36_COMPARISON_20261006.md`; dữ liệu chi tiết: `eval/reports/legal_repair_36_comparison_v15_20261006.json`. Báo cáo nêu cả hai câu giảm nhãn, câu 28 còn low do những khẳng định thống kê chưa có căn cứ, khác biệt câu hỏi 49 với mẫu và giới hạn của cờ nguồn. 174 kiểm thử đã đạt (125 workflow, 49 bộ chấm).
