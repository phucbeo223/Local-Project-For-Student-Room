# Bổ sung nguồn và sửa xử lý pháp lý — 03/10/2026

## Nguyên tắc nguồn

Chỉ tải bản gốc được đăng trên cổng cơ quan nhà nước. Không dùng câu trả lời của model để tạo điều luật, điều khoản hay đáp án chuẩn. Bản trích phục vụ truy xuất không phải văn bản hợp nhất chính thức. Khuyến cáo nghiệp vụ được phân biệt với quy phạm pháp luật.

URL, thời điểm tải, mã SHA-256, dung lượng và vị trí bản gốc được ghi trong [sổ tải](legal_sources_originals_20261003/download_manifest.json). Các đoạn được đưa vào Data, lý do sửa, số điều, trang đối chiếu và bản cũ lưu riêng được ghi trong [sổ trích đoạn](legal_sources_originals_20261003/prepared_manifest.json).

## Tài liệu bổ sung và đối chiếu

| Tài liệu | Nguồn cơ quan nhà nước | Nội dung sử dụng |
|---|---|---|
| Bộ luật Dân sự 91/2015/QH13, phần 1 | [Cổng Chính phủ](https://datafiles.chinhphu.vn/cpp/files/vbpq/2016/01/91.signed.pdf) | Chép đối chiếu toàn Điều 328, trang PDF 86–87; khôi phục ngoại lệ bị cụt |
| Bộ luật Dân sự, phần 2 | [Cổng Chính phủ](https://datafiles.chinhphu.vn/cpp/files/vbpq/2016/01/91_.pdf) | Khôi phục nội dung hiệu lực Điều 689; đối chiếu OCR với các điều đã có |
| Luật Cư trú 68/2020/QH14 | [Công an tỉnh Lâm Đồng](https://congan.lamdong.gov.vn/UpLoaded/files/luat/68_2020_QH14.pdf) | Chép theo ảnh Điều 9, 27, 28; giữ đủ hồ sơ, thời hạn, ngoại lệ |
| Luật 118/2025/QH15 | [Cổng Chính phủ](https://datafiles.chinhphu.vn/cpp/files/vbpq/2026/01/luatso118.2025.pdf) | Điều 4 khoản 9 thay Điều 30 về lưu trú; đối chiếu các sửa đổi PCCC tại Điều 10 |
| Luật 55/2024/QH15 | [Công báo trên Cổng Chính phủ](https://datafiles.chinhphu.vn/cpp/files/vbpq/2025/01/luat55.pdf) | Trích nguyên Điều 8, 20, 21, 23, 24; tách trách nhiệm chủ hộ, người cho thuê, người thuê và cơ quan |
| Nghị định 105/2025/NĐ-CP | [Cổng Chính phủ](https://datafiles.chinhphu.vn/cpp/files/vbpq/2025/5/105-ndcp.signed.pdf) | Lưu PDF gốc; giữ bản trích trước đã cập nhật Điều 13–14 |
| Nghị định 347/2026/NĐ-CP | [Cổng Chính phủ](https://datafiles.chinhphu.vn/cpp/files/vbpq/2026/9/347_2026_nd-cp_08092026_7-signed.signed.pdf) | Đối chiếu Điều 17–19 sửa 105 và mốc hiệu lực Điều 41; không mặc định mọi sửa đổi cùng hiệu lực |
| Luật Kinh doanh bất động sản 29/2023/QH15 | [Công báo trên Cổng Chính phủ](https://datafiles.chinhphu.vn/cpp/files/vbpq/2024/01/luat29.pdf) | Lưu bản gốc để đối chiếu; sửa lỗi suy nội dung công việc thành nghĩa vụ |
| Cảnh báo đặt cọc thuê nhà qua mạng | [Bộ Công an](https://www.bocongan.gov.vn/bai-viet/canh-giac-voi-chieu-tro-lua-dao-dat-coc-thue-nha-tro-qua-mang-1782485063) | Chỉ giữ đoạn khuyến cáo xem phòng, xác minh người cho thuê, lưu bằng chứng, trình báo |
| Cảnh báo mua hàng trực tuyến | [Bộ Công an](https://www.bocongan.gov.vn/bai-viet/xuat-hien-thu-doan-lua-dao-moi-khi-mua-hang-online-1790562304) | Chỉ giữ khuyến cáo về liên kết lạ, QR, OTP, tài khoản và lưu bằng chứng; ghi rõ phạm vi mua hàng trực tuyến |

Ba bản trích cũ được lưu tại `docs/legal_sources_excluded/supplement_20261003`, ngừng truy xuất nhưng giữ bản và hash để khôi phục. Trong 42 điều của bản trích Dân sự, ngoài Điều 328 và 689 được sửa, các điều khác giữ nội dung bản trích trước; đã so khớp OCR theo điều trong `civil_ocr_comparison.json`. Đây không phải chứng nhận đối chiếu từng chữ của toàn bộ luật. Điều 482 trước chỉ chọn khoản 1, 4; việc bỏ khoản khác được ghi rõ, không kết luận các khoản đó không tồn tại.

OCR chỉ hỗ trợ đọc ảnh. Các đoạn cư trú mới và Điều 328 được chép đối chiếu ảnh gốc; sửa lỗi nhận dạng như “Điền”, “Hỗ”, “tài Hiệu”, không tạo thêm quy định. Với PDF có lớp chữ, bỏ đầu trang Công báo, số trang và nối dòng, giữ số khoản/điểm.

Không tải được từ một số địa chỉ VBPL do lỗi DNS và từ CDN Công báo do lỗi chuỗi chứng chỉ. Không tắt kiểm tra HTTPS để tải. Bản Dân sự đầu tiên tải là phần 2; đã tải thêm phần 1 và ghi hai tệp riêng.

## Bốn nhóm sửa

1. Kiểm tra điều, khoản và chủ thể theo chính nguồn được dẫn; không chuyển nội dung công việc thành nghĩa vụ, không dùng đoạn bị cụt ngoại lệ để kết luận.
2. Thay bản rút gọn thiếu nội dung bằng trích đoạn có căn cứ; tách ghi chú nguồn khỏi nội dung điều luật. Không tạo giá thuê, khoảng cách hay dữ liệu tin phòng mới.
3. Lấy ứng viên theo từng chủ đề, giữ nguồn cho từng phần câu hỏi, ghép các điểm trong cùng khoản; ưu tiên thông tin hợp đồng, hồ sơ cư trú và điều kiện an toàn nhà ở.
4. Xác định câu trả lời đầy đủ/một phần/chưa đủ theo nội dung, không theo tên model. Lời thừa nhận chưa tìm thấy căn cứ không được coi là câu trả lời đầy đủ.

## Kiểm tra và trạng thái

- 108 kiểm tra tự động đã qua sau các sửa đổi.
- Đã nạp 5 tệp mới/thay thế, giữ 27 tệp không đổi, ngừng truy xuất 3 tệp cũ; không có lỗi nạp.
- Kho hiện có 32 tài liệu sẵn sàng, 1.927 đoạn và 1.927 vector; không thiếu tệp hoặc vector. 915 tin phòng và vector của chúng được giữ nguyên, không dùng để chấm bộ pháp lý.
- Kiểm tra truy xuất thực tế đã thấy đủ ba nhóm cho câu 29 và đúng Điều 163 khoản 1; câu 14 lấy được Điều 9; câu 17 lấy được điều kiện nhà ở Điều 20. Điều 161 về chủ sở hữu/người được ủy quyền được ưu tiên cho câu hỏi quyền cho thuê; nếu câu 22 trong lượt dài chưa dùng bản sửa cuối, tác vụ lưu kết quả cũ và chạy lại riêng câu đó trước khi chấm.
- Số trang hiển thị của tệp Markdown là trang của bản trích; trang PDF gốc được ghi riêng trong sổ nguồn, không coi trang 1 của bản trích là trang 1 của văn bản gốc.
- Bộ 36 câu đang chạy lại. Chưa công bố điểm tăng/giảm khi chưa có kết quả đủ.
- Trong phiên này cả Gemini 3.5 và 3.1 báo hết hạn mức 500 lượt/ngày. Đã thêm Gemini 3.1 làm dự phòng trước Qwen 9B và giãn nhịp gọi 5 giây/model; khi cả hai không khả dụng hệ thống dùng Qwen 9B. Phải báo cáo model thực tế từng câu và hạn chế so sánh do khác tỷ lệ dùng model. Quota áp dụng theo dự án/model; không xoay khóa để vượt quota. [Tài liệu hạn mức của Google](https://ai.google.dev/gemini-api/docs/rate-limits).
- Các lượt thử ban đầu được giữ riêng trong các tệp `legal_supplement_after_2026-10-03.json`, `legal_supplement_final_2026-10-03.json`. Lượt cuối dùng `legal_supplement_release_2026-10-03.json`. Không thay kết quả cũ bằng số giả.
- Tiến độ công việc dài và trạng thái chờ quota được ghi tại `eval/reports/legal_supplement_job_status_2026-10-03.json`; nhật ký chấm tại `eval/reports/legal_supplement_scoring_2026-10-03.log`. Báo cáo so sánh chỉ được tạo sau khi đã có đủ câu trả lời và đã thực hiện bước chấm thật.

Điểm RAGAS phản ánh mức bám nguồn và liên quan; chưa có đáp án chuẩn độc lập nên chưa chứng minh được đúng pháp lý toàn diện hoặc đo context recall/answer correctness.

## Chuyển sang local theo yêu cầu — 03/10/2026

- Đã dừng hai tác vụ đánh giá trước, giữ nguyên kết quả và nhật ký. Cấu hình chạy thực tế chuyển thành `CHATBOT_LLM_PROVIDER=qwen`; phần trả lời và kiểm tra nguồn chỉ khởi tạo Ollama Qwen 3.5 9B, không gọi Gemini. Khóa có sẵn được giữ kín.
- Nguồn chính thức, các bản trích có ghi xuất xứ và vector đã nạp được sử dụng tiếp. Không tải thêm hoặc tạo thêm quy định trong bước chuyển model này.
- Chạy một lượt mới toàn bộ 36 câu, bắt đầu kiểm tra câu 4 (đặt cọc) và ba chỉ số RAGAS thật. Không gắn nhãn kết quả cũ thành kết quả mới. Tệp mới: `eval/reports/legal_local_after_2026-10-03.json`.
- Chấm lại bản sao câu trả lời/ngữ cảnh cũ tại `eval/reports/legal_local_before_2026-10-03.json` bằng cùng Qwen và cùng cấu hình. Giữ hash và không sửa kết quả gốc `legal_model_upgrade_after_2026-10-02.json`. Không so trực tiếp điểm Gemini với điểm Qwen.
- Bộ chấm lưu phán xét JSON và lượng token; từ chối đầu ra bị cụt thay vì tính điểm từ nội dung chưa hoàn tất. Chấm một luồng với ngữ cảnh đầy đủ; thời hạn yêu cầu 300 giây. Tác vụ có giới hạn 24 giờ và lưu tiến độ từng chỉ số.
- 110 kiểm tra tự động đạt, gồm kiểm tra chỉ khởi tạo local dù có key cloud, lưu phán xét và từ chối JSON bị cụt.
- Tiến độ: `eval/reports/legal_local_status_2026-10-03.json`; nhật ký: `eval/reports/legal_local_2026-10-03.log`; báo cáo cập nhật: `eval/ragas_reports/legal_local_comparison_2026-10-03.md`. Chỉ kết luận tăng/giảm khi hai lượt chấm đủ và có các cặp điểm hợp lệ.
- Model sinh cũng là model chấm nên có khả năng tự thiên vị. Bộ chấm không thay thế kiểm tra pháp lý độc lập.
- Câu thử số 4 đã chạy đủ hai lượt sinh/kiểm tra bằng Qwen. Bộ kiểm tra local báo thiếu ngoại lệ “trừ trường hợp có thoả thuận khác” dù nguồn Điều 328 khoản 2 có nguyên cụm này; đồng thời nhận xét thiếu điều kiện thực hiện dù nguồn có “được giao kết, thực hiện”. Hệ thống vì vậy trả trích đoạn một phần. Đây là dấu hiệu bác bỏ nhầm cần rà tiếp, không phải bằng chứng tài liệu thiếu. Giữ nguyên lý do và kết quả để chấm trung thực; chưa kết luận model local cải thiện chất lượng.
- RAGAS native local cho câu 4: faithfulness 0,5556 (= 5/9 phát biểu được chấp nhận). Phán xét lưu trong JSON cho thấy cả 5 phát biểu về Điều 328 khoản 2 được chấp nhận; 4 phát biểu bị bác là câu giới thiệu kho, nhãn trả lời một phần, giới hạn áp dụng và lời khuyên đối chiếu. Bộ trích phát biểu cũng không liệt kê nội dung định nghĩa khoản 1 đã có trong phản hồi. Vì vậy điểm này không chứng minh 44,44% quy định được trả lời sai; giữ điểm native và ghi rõ giới hạn bộ chấm, không xóa câu hoặc sửa điểm để làm đẹp kết quả.
- Kiểm tra đầu cuối câu 4 đã có đủ ba điểm RAGAS thực: faithfulness 0,5556; answer relevancy 0,7763; context utilization 1,0000. Đây là một câu thử, không phải điểm trung bình bộ 36 câu và chưa có đối chiếu trước/sau bằng cùng judge. Tác vụ tiếp tục chạy những câu còn lại, chấm lượt mới và chấm lại bản sao cũ.
