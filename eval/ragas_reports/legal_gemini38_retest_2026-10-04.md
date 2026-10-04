# Kiểm thử lại 36 câu qua Gemini proxy

Lượt chạy dùng pipeline và DB thật của API chính, kho `public`, agent riêng tắt; runner gọi dịch vụ nội bộ để lưu đầy đủ ngữ cảnh, tắt telemetry. Không dùng bộ đáp án ngoài làm chuẩn đúng/sai.

- Bắt đầu UTC: 2026-10-04T07:20:51.962863+00:00; kết thúc UTC: 2026-10-04T07:34:44.395603+00:00.
- Model trả lời được cấu hình: `gemini-3.8-flash-high` qua proxy local.
- Bộ chấm: Ragas 0.3.9, gemini/gemini-3.1-flash-lite; 4 worker; chấm cả phản hồi một phần có nguồn.
- JSON đầy đủ: `legal_gemini38_retest_2026-10-04_fixed.json`; SHA-256 bộ câu hỏi: `0cd8e8f865c9d50fa21ebb38fae22b925e2fd5bbb6e0241ee96d25eed8b0f4fd`.

## Kết quả thực thi

| Chỉ số | Kết quả |
|---|---:|
| Hoàn thành | 36/36 |
| Lỗi thực thi | 0 |
| Có ngữ cảnh / truy xuất vector | 36 / 36 |
| Có nguồn cùng nhóm câu hỏi | 36/36 |
| Đủ theo kiểm tra hệ thống | 12 |
| Chưa đủ căn cứ, gồm phản hồi một phần | 24 |
| Trả lời một phần | 22 |
| Chế độ suy giảm | 24 |
| Định dạng trích dẫn trung bình | 1.0 |
| Độ trễ p50 / p95 | 18194.5 / 25338 ms |

Gemini được gọi sinh câu trả lời ở 34/36 câu. Một số câu được trả lời trực tiếp bằng nguồn; câu bị kiểm tra bác bỏ có thể chuyển dự phòng. Provider cuối cùng: {'template': 2, 'legal-partial-extractive': 13, 'gemini': 19, 'legal-extractive': 2}.

## Điểm Ragas

| Chỉ số | Trung bình | Số điểm hợp lệ |
|---|---:|---:|
| faithfulness | 0.7871 | 36/36 |
| answer_relevancy | 0.7252 | 36/36 |
| context_utilization | 0.6551 | 36/36 |

Các điểm đo mức bám ngữ cảnh và liên quan câu hỏi. Chưa có đáp án chuẩn độc lập, nên không báo tỷ lệ đúng pháp luật, Answer Correctness hay Context Recall. Model sinh và model chấm đều do cùng proxy cung cấp, thuộc họ Gemini theo tên alias; có thể có thiên lệch và chưa xác minh model nền thực tế.

## Phạm vi dữ liệu và sửa lỗi

Kho chính có 32 tài liệu, 1927 đoạn, 1927 vector. Trong 44 tệp Data, 12 tệp chưa được nạp; 0 đường dẫn chỉ mục vắng tệp nguồn.

Các tệp chưa nạp:

- `cantho_contacts.md`
- `criminal_law/Bo-sung-thuc-te-20261004.md`
- `ecommerce_platform/Bo-sung-thuc-te-20261004.md`
- `electricity/Bo-sung-thuc-te-20261004.md`
- `fire_safety/Bo-sung-thuc-te-20261004.md`
- `housing_contract/Bo-sung-thuc-te-20261004.md`
- `legal_templates.md`
- `privacy_data/Bo-sung-thuc-te-20261004.md`
- `real_estate_brokerage/Bo-sung-thuc-te-20261004.md`
- `residence/Bo-sung-thuc-te-20261004.md`
- `residence/CT01-116-2026-trich-ban-goc.pdf`
- `water_cantho/Bo-sung-thuc-te-20261004.md`

Lượt trước sửa lỗi dừng sau 6 phản hồi và được giữ riêng. Proxy bọc JSON trong Markdown; đã sửa để chỉ bỏ lớp bọc hoàn chỉnh, vẫn giữ kiểm tra JSON/schema và lỗi cắt token. Runner chấm được sửa truyền đúng endpoint proxy. 37 kiểm tra hồi quy đã đạt; API chính đã build lại và kiểm tra JSON proxy thành công.

## Từng câu

| Câu | Chủ đề | Trạng thái | Provider / model cuối | F | AR | CU |
|---|---|---|---|---:|---:|---:|
| 1 | housing_contract | chưa đủ căn cứ | template / — | 0.0 | 0.0 | 0.0 |
| 2 | housing_contract | trả lời một phần | legal-partial-extractive / — | 1.0 | 0.9087 | 0.3333 |
| 3 | housing_contract | đủ theo kiểm tra hệ thống | gemini / gemini-3.8-flash-high | 0.7273 | 0.9332 | 1.0 |
| 4 | housing_contract | trả lời một phần | gemini / gemini-3.8-flash-high | 0.7 | 0.9438 | 1.0 |
| 5 | electricity | đủ theo kiểm tra hệ thống | legal-extractive / — | 1.0 | 0.9244 | 1.0 |
| 6 | electricity | đủ theo kiểm tra hệ thống | legal-extractive / — | 0.9091 | 0.8696 | 1.0 |
| 7 | electricity | đủ theo kiểm tra hệ thống | gemini / gemini-3.8-flash-high | 1.0 | 0.8912 | 1.0 |
| 8 | electricity | trả lời một phần | legal-partial-extractive / — | 1.0 | 0.8838 | 0.0 |
| 9 | water_cantho | trả lời một phần | gemini / gemini-3.8-flash-high | 0.6 | 0.9708 | 0.5833 |
| 10 | water_cantho | trả lời một phần | gemini / gemini-3.8-flash-high | 1.0 | 0.8771 | 1.0 |
| 11 | water_cantho | trả lời một phần | legal-partial-extractive / — | 1.0 | 0.9327 | 1.0 |
| 12 | water_cantho | trả lời một phần | gemini / gemini-3.8-flash-high | 0.8667 | 0.8466 | 1.0 |
| 13 | residence | trả lời một phần | legal-partial-extractive / — | 1.0 | 0.8635 | 0.8333 |
| 14 | residence | trả lời một phần | gemini / gemini-3.8-flash-high | 0.7143 | 0.9482 | 0.0 |
| 15 | residence | đủ theo kiểm tra hệ thống | gemini / gemini-3.8-flash-high | 0.7778 | 0.9106 | 1.0 |
| 16 | residence | trả lời một phần | legal-partial-extractive / — | 0.8182 | 0.8471 | 0.5 |
| 17 | fire_safety | đủ theo kiểm tra hệ thống | gemini / gemini-3.8-flash-high | 0.0909 | 0.9335 | 0.0 |
| 18 | fire_safety | trả lời một phần | gemini / gemini-3.8-flash-high | 0.8889 | 0.9468 | 0.5 |
| 19 | fire_safety | trả lời một phần | legal-partial-extractive / — | 1.0 | 0.0 | 0.0 |
| 20 | fire_safety | đủ theo kiểm tra hệ thống | gemini / gemini-3.8-flash-high | 0.7 | 0.9069 | 1.0 |
| 21 | real_estate_brokerage | trả lời một phần | gemini / gemini-3.8-flash-high | 0.5714 | 0.942 | 0.5 |
| 22 | real_estate_brokerage | đủ theo kiểm tra hệ thống | gemini / gemini-3.8-flash-high | 0.5 | 0.8742 | 0.8333 |
| 23 | real_estate_brokerage | trả lời một phần | gemini / gemini-3.8-flash-high | 0.625 | 0.0 | 1.0 |
| 24 | real_estate_brokerage | trả lời một phần | legal-partial-extractive / — | 1.0 | 0.8621 | 1.0 |
| 25 | ecommerce_platform | đủ theo kiểm tra hệ thống | gemini / gemini-3.8-flash-high | 0.75 | 0.9332 | 0.5 |
| 26 | ecommerce_platform | trả lời một phần | gemini / gemini-3.8-flash-high | 1.0 | 0.9034 | 0.3333 |
| 27 | ecommerce_platform | trả lời một phần | legal-partial-extractive / — | 1.0 | 0.0 | 1.0 |
| 28 | ecommerce_platform | đủ theo kiểm tra hệ thống | gemini / gemini-3.8-flash-high | 1.0 | 0.8731 | 0.0 |
| 29 | privacy_data | trả lời một phần | legal-partial-extractive / — | 1.0 | 0.8882 | 0.0 |
| 30 | privacy_data | chưa đủ căn cứ | template / — | 0.0 | 0.0 | 0.0 |
| 31 | privacy_data | trả lời một phần | legal-partial-extractive / — | 0.5714 | 0.0 | 1.0 |
| 32 | privacy_data | trả lời một phần | legal-partial-extractive / — | 1.0 | 0.8834 | 1.0 |
| 33 | criminal_law | đủ theo kiểm tra hệ thống | gemini / gemini-3.8-flash-high | 0.875 | 0.8982 | 1.0 |
| 34 | criminal_law | đủ theo kiểm tra hệ thống | gemini / gemini-3.8-flash-high | 0.9 | 0.8679 | 1.0 |
| 35 | criminal_law | trả lời một phần | legal-partial-extractive / — | 1.0 | 0.8418 | 0.8333 |
| 36 | criminal_law | trả lời một phần | legal-partial-extractive / — | 0.75 | 0.0 | 0.8333 |

Câu chưa đủ căn cứ: 1, 2, 4, 8, 9, 10, 11, 12, 13, 14, 16, 18, 19, 21, 23, 24, 26, 27, 29, 30, 31, 32, 35, 36.
Câu trả lời một phần: 2, 4, 8, 9, 10, 11, 12, 13, 14, 16, 18, 19, 21, 23, 24, 26, 27, 29, 31, 32, 35, 36.

Trạng thái đủ là kết quả kiểm tra của hệ thống, không phải chứng nhận độc lập về đúng luật.

Ưu tiên rà thủ công các câu có Faithfulness dưới 0,5: [(1, 0.0), (17, 0.0909), (30, 0.0)]. Đặc biệt câu 17 đã được kiểm tra của hệ thống chấp nhận nhưng bộ chấm báo bám nguồn thấp.

Số metric đã thử lại có lưu lỗi trước đó: 5. Các metric vẫn lỗi: không có.
