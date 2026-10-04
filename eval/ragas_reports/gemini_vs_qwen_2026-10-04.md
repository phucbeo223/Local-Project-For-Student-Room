# So sánh Gemini và Gemini + Qwen trên 36 câu

## Thiết lập so sánh

- Phương án A: định tuyến bằng quy tắc, truy xuất nguồn; Gemini 3.8 Flash High tổng hợp và kiểm tra nguồn, có đáp án trích xuất trực tiếp hoặc dự phòng theo quy tắc.
- Phương án B: Gemini 3.8 Flash High phân tích câu hỏi, truy xuất theo kế hoạch; Qwen 3.5 9B chọn ID đoạn nguồn ở chế độ `source_select`, hệ thống ghép trích nguyên văn. Đoạn nguyên văn được kiểm tra exact-source; bước Gemini kiểm tra ý nghĩa được bỏ qua trong nhánh này.
- Cả hai dùng kho `public`, bộ 36 câu và E5 hiện hành. API chính không được đổi sang B khi chạy test.
- Bộ chấm chung: Ragas 0.3.9, gemini/gemini-3.1-flash-lite; 4 worker, 8.192 token đầu ra, chấm cả phản hồi một phần có nguồn; cùng endpoint proxy và toàn bộ ngữ cảnh.
- SHA bộ câu hỏi: `0cd8e8f865c9d50fa21ebb38fae22b925e2fd5bbb6e0241ee96d25eed8b0f4fd`.
- Baseline Gemini giữ nguyên SHA: `e1474a6f9523521af2163a15058318cb58fa05b75e0de70837130245d135da34`.
- Cùng các tệp pipeline: True; cùng kiểm kê corpus trước/sau và baseline: True.
- Các thống kê kiểm kê không phải fingerprint đầy đủ của DB ở thời điểm lượt A; không sửa/nạp corpus trong hai lượt.

## Kết quả vận hành

| Chỉ số | A: Gemini | B: Gemini + Qwen |
|---|---:|---:|
| Hoàn thành | 36 | 36 |
| Lỗi thực thi | 0 | 0 |
| Có ngữ cảnh | 36 | 36 |
| Trả lời một phần | 22 | 21 |
| Chưa đủ căn cứ (gồm một phần) | 24 | 21 |
| Suy giảm | 24 | 23 |
| Định dạng trích dẫn trung bình | 1.0 | 1.0 |
| Đủ theo kiểm tra hệ thống | 12 | 15 |
| Độ trễ p50 (giây) | 18.19 | 30.71 |
| Độ trễ p95 (giây) | 25.34 | 66.28 |
| Độ dài phản hồi trung vị (ký tự) | 856 | 2473 |

## Ragas cùng phương pháp

| Chỉ số | A: Gemini (n) | B: Kết hợp (n) | Δ B−A trên các cặp | Khoảng bootstrap 95% | B cao / bằng / thấp |
|---|---:|---:|---:|---|---|
| faithfulness | 0.7705 (33) | 0.9625 (33) | 0.1920 | [0.0922, 0.2984] | 18 / 10 / 5 |
| answer_relevancy | 0.7252 (36) | 0.7206 (36) | -0.0045 | [-0.172, 0.1633] | 11 / 0 / 25 |
| context_utilization | 0.6551 (36) | 0.6481 (36) | -0.0069 | [-0.118, 0.1065] | 7 / 22 / 7 |

Bootstrap chỉ thể hiện biến thiên giữa 36 câu đã chọn (5.000 mẫu, seed 20261004); không đo nhiễu của bộ chấm qua nhiều lần chạy. Điểm Ragas không phải tỷ lệ đúng luật. Cùng proxy cung cấp model sinh/chấm; tên alias chưa xác minh model nền. Qwen trích nguyên văn có thể tăng Faithfulness nhưng vẫn chọn sai phạm vi hoặc thiếu cách áp dụng.

## Xác nhận vai trò và nguồn lực

- Gemini phân tích thành công 28/36; fallback phân tích: 8.
- Lượt gọi Qwen generate: 36; thành công: 36.
- Kiểm tra trích nguyên văn được chấp nhận: 36; lượt Gemini kiểm tra ý nghĩa trong trace: 0.
- Provider cuối A: {'template': 2, 'legal-partial-extractive': 13, 'gemini': 19, 'legal-extractive': 2}.
- Provider cuối B: {'qwen-local': 36}.
- Không có bảng giá thực của proxy; không suy ra chi phí tiền. B dùng thêm tài nguyên Ollama trên máy và vẫn gọi Gemini để phân tích/chấm.
- Corpus có 32 tài liệu, 1927 vector; 12 tệp mới chưa nạp ở cả hai phương án.

## Từng câu

| Câu | Chủ đề | Trạng thái A → B | Độ trễ A / B (s) | F A / B | AR A / B | CU A / B |
|---|---|---|---|---|---|---|
| 1 | housing_contract | chưa đủ căn cứ → đủ theo hệ thống | 26.95 / 74.95 | 0.0000 / 1.0000 | 0.0000 / 0.8547 | 0.0000 / 1.0000 |
| 2 | housing_contract | một phần → một phần | 20.24 / 56.96 | 1.0000 / 0.8462 | 0.9087 / 0.8744 | 0.3333 / 0.0000 |
| 3 | housing_contract | đủ theo hệ thống → một phần | 10.51 / 24.36 | 0.7273 / 1.0000 | 0.9332 / 0.0000 | 1.0000 / 1.0000 |
| 4 | housing_contract | một phần → một phần | 19.11 / 51.84 | 0.7000 / 1.0000 | 0.9438 / 0.8580 | 1.0000 / 1.0000 |
| 5 | electricity | đủ theo hệ thống → một phần | 0.11 / 58.15 | 1.0000 / 1.0000 | 0.9244 / 0.0000 | 1.0000 / 1.0000 |
| 6 | electricity | đủ theo hệ thống → một phần | 0.11 / 58.70 | 0.9091 / N/A | 0.8696 / 0.0000 | 1.0000 / 1.0000 |
| 7 | electricity | đủ theo hệ thống → một phần | 13.06 / 59.97 | 1.0000 / N/A | 0.8912 / 0.8598 | 1.0000 / 1.0000 |
| 8 | electricity | một phần → một phần | 19.90 / 58.44 | 1.0000 / N/A | 0.8838 / 0.0000 | 0.0000 / 0.5000 |
| 9 | water_cantho | một phần → một phần | 19.76 / 33.48 | 0.6000 / 0.9091 | 0.9708 / 0.9234 | 0.5833 / 0.0000 |
| 10 | water_cantho | một phần → một phần | 19.72 / 32.27 | 1.0000 / 1.0000 | 0.8771 / 0.0000 | 1.0000 / 0.9167 |
| 11 | water_cantho | một phần → một phần | 25.34 / 33.61 | 1.0000 / 1.0000 | 0.9327 / 0.9136 | 1.0000 / 1.0000 |
| 12 | water_cantho | một phần → đủ theo hệ thống | 18.03 / 32.30 | 0.8667 / 0.9375 | 0.8466 / 0.8541 | 1.0000 / 1.0000 |
| 13 | residence | một phần → một phần | 19.95 / 23.41 | 1.0000 / 0.6667 | 0.8635 / 0.0000 | 0.8333 / 1.0000 |
| 14 | residence | một phần → một phần | 11.80 / 22.96 | 0.7143 / 1.0000 | 0.9482 / 0.9145 | 0.0000 / 0.0000 |
| 15 | residence | đủ theo hệ thống → đủ theo hệ thống | 10.18 / 25.28 | 0.7778 / 0.9500 | 0.9106 / 0.9004 | 1.0000 / 1.0000 |
| 16 | residence | một phần → đủ theo hệ thống | 18.48 / 21.91 | 0.8182 / 0.9167 | 0.8471 / 0.8608 | 0.5000 / 0.5833 |
| 17 | fire_safety | đủ theo hệ thống → đủ theo hệ thống | 11.59 / 27.51 | 0.0909 / 1.0000 | 0.9335 / 0.8770 | 0.0000 / 1.0000 |
| 18 | fire_safety | một phần → một phần | 18.27 / 27.18 | 0.8889 / 0.8333 | 0.9468 / 0.8790 | 0.5000 / 0.0000 |
| 19 | fire_safety | một phần → một phần | 12.01 / 55.03 | 1.0000 / 1.0000 | 0.0000 / 0.8061 | 0.0000 / 0.0000 |
| 20 | fire_safety | đủ theo hệ thống → đủ theo hệ thống | 18.12 / 32.03 | 0.7000 / 1.0000 | 0.9069 / 0.8981 | 1.0000 / 1.0000 |
| 21 | real_estate_brokerage | một phần → một phần | 15.40 / 30.68 | 0.5714 / 1.0000 | 0.9420 / 0.8570 | 0.5000 / 0.0000 |
| 22 | real_estate_brokerage | đủ theo hệ thống → một phần | 10.03 / 40.94 | 0.5000 / 1.0000 | 0.8742 / 0.8647 | 0.8333 / 0.0000 |
| 23 | real_estate_brokerage | một phần → một phần | 10.48 / 30.68 | 0.6250 / 1.0000 | 0.0000 / 0.8683 | 1.0000 / 1.0000 |
| 24 | real_estate_brokerage | một phần → một phần | 16.98 / 30.55 | 1.0000 / 1.0000 | 0.8621 / 0.8740 | 1.0000 / 1.0000 |
| 25 | ecommerce_platform | đủ theo hệ thống → đủ theo hệ thống | 20.53 / 30.02 | 0.7500 / 1.0000 | 0.9332 / 0.8560 | 0.5000 / 0.5000 |
| 26 | ecommerce_platform | một phần → đủ theo hệ thống | 18.44 / 26.99 | 1.0000 / 1.0000 | 0.9034 / 0.8125 | 0.3333 / 0.3333 |
| 27 | ecommerce_platform | một phần → đủ theo hệ thống | 20.61 / 27.87 | 1.0000 / 1.0000 | 0.0000 / 0.8803 | 1.0000 / 1.0000 |
| 28 | ecommerce_platform | đủ theo hệ thống → đủ theo hệ thống | 9.94 / 25.51 | 1.0000 / 1.0000 | 0.8731 / 0.8608 | 0.0000 / 0.0000 |
| 29 | privacy_data | một phần → một phần | 22.36 / 42.93 | 1.0000 / 1.0000 | 0.8882 / 0.8352 | 0.0000 / 0.0000 |
| 30 | privacy_data | chưa đủ căn cứ → một phần | 21.38 / 32.26 | 0.0000 / 1.0000 | 0.0000 / 0.8191 | 0.0000 / 0.0000 |
| 31 | privacy_data | một phần → một phần | 19.02 / 30.74 | 0.5714 / 1.0000 | 0.0000 / 0.8335 | 1.0000 / 1.0000 |
| 32 | privacy_data | một phần → đủ theo hệ thống | 21.10 / 28.30 | 1.0000 / 0.9524 | 0.8834 / 0.8757 | 1.0000 / 0.5000 |
| 33 | criminal_law | đủ theo hệ thống → đủ theo hệ thống | 10.95 / 27.58 | 0.8750 / 0.8750 | 0.8982 / 0.8523 | 1.0000 / 1.0000 |
| 34 | criminal_law | đủ theo hệ thống → đủ theo hệ thống | 7.83 / 25.79 | 0.9000 / 0.9167 | 0.8679 / 0.8562 | 1.0000 / 1.0000 |
| 35 | criminal_law | một phần → đủ theo hệ thống | 23.26 / 66.28 | 1.0000 / 0.9583 | 0.8418 / 0.8764 | 0.8333 / 1.0000 |
| 36 | criminal_law | một phần → đủ theo hệ thống | 16.24 / 24.65 | 0.7500 / 1.0000 | 0.0000 / 0.8470 | 0.8333 / 1.0000 |

B chuyển từ chưa đủ sang đủ theo hệ thống: [1, 12, 16, 26, 27, 32, 35, 36].
B chuyển từ đủ sang chưa đủ: [3, 5, 6, 7, 22].

Metric còn lỗi: {'A': [], 'B': [(6, ['faithfulness']), (7, ['faithfulness']), (8, ['faithfulness'])]}.

Faithfulness của B còn thiếu 3 điểm. Nếu các điểm này nhận bất kỳ giá trị nào trong [0,1], trung bình toàn bộ 36 câu sẽ nằm trong [0.8823, 0.9656]. Đây là biên toán học, không phải điểm được chấm; các điểm lỗi vẫn giữ N/A. Trung bình A trên 36 câu là 0.7871.

## Khuyến nghị chọn phương án

**Đề xuất chọn phương án B — Gemini phân tích, Qwen chọn trích đoạn — cho phần hỏi đáp pháp lý khi ưu tiên bám nguồn.** B có 15/36 câu đủ theo kiểm tra hệ thống, so với 12/36 của A. Trên các cặp có điểm, mức bám nguồn của B cao hơn; ngay cả khi ba điểm Faithfulness còn thiếu nhận giá trị thấp nhất, trung bình toàn bộ B vẫn cao hơn A. Điểm liên quan câu hỏi và hữu dụng ngữ cảnh gần với A, nên không kết luận B cải thiện rõ hai chỉ số này.

Đánh đổi là thời gian và độ dài: p50 của B là 30,7 giây, A là 18,2 giây; p95 tương ứng 66,3 và 25,3 giây. Phản hồi B dài trung vị 2.473 ký tự, A khoảng 856 ký tự. Nếu cần trả lời ngắn và nhanh, A phù hợp hơn. B hiện chọn và ghép nguồn nguyên văn, chưa phải một luồng giải thích/tư vấn áp dụng luật đã kiểm định.

Khuyến nghị này giới hạn ở bộ 36 câu pháp lý và máy hiện tại, không suy ra hiệu quả tìm phòng. B vẫn có 21 phản hồi một phần; Gemini phân tích thành công 28/36 câu và fallback bằng quy tắc ở 8 câu. Ba điểm Faithfulness ở câu 6–8 giữ N/A sau một lượt thử lại; so sánh điểm này dùng 33 cặp tương ứng. Chưa có đáp án chuẩn độc lập, nên không gọi điểm bám nguồn là tỷ lệ đúng pháp luật.

Cả hai còn thiếu 12 tệp mới trong chỉ mục. Bước tiếp theo nên nạp và xác minh các nguồn bổ sung, rà thủ công những câu thay đổi kết quả (đặc biệt điện, PCCC và dữ liệu cá nhân), rồi chạy lại trước khi nghiệm thu. Cải thiện cách rút gọn và giải thích đáp án Qwen là đề xuất tiếp theo, chưa được kiểm thử trong lượt này.


