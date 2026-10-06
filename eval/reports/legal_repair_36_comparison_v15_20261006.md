# So sánh 36 câu sau sửa bộ chấm và workflow

Baseline `c8dba04` và bản sửa dùng cùng 36 ID/câu hỏi của question bank; câu trả lời được sinh hoàn tất trước khi chấm. Hai lượt chấm dùng cùng hash bộ chấm, bộ kiểm tra số liệu và mẫu gốc. Không thay mẫu gốc bằng bản rà còn thiếu xác minh.

Nhãn khớp mẫu sau kiểm tra: high khi mọi đoạn/ý mẫu đều matched; partial khi có ít nhất một ý matched và còn ý khác/thiếu; low khi không có ý matched. Nhãn do Qwen đề xuất được lưu riêng trong JSON. Mỗi matched phải có ID đoạn thật, nguyên văn và qua kiểm tra số liệu; kiểm tra này vẫn cần đối chiếu ngữ nghĩa.

| Kết quả | Baseline | Bản sửa |
|---|---|---|
| Khớp mẫu: high | 9 | 12 |
| Khớp mẫu: partial | 25 | 23 |
| Khớp mẫu: low | 2 | 1 |
| Khớp mẫu: unscored | 0 | 0 |
| Cờ bao phủ nguồn lúc chạy: complete | 20 | 14 |
| Cờ bao phủ nguồn lúc chạy: partial | 16 | 22 |
| Số từ dài nhất (đếm theo khoảng trắng) | 683 | 583 |
| Số ký tự dài nhất | 3137 | 2673 |

Cả hai bản đều đã sinh đủ 36 câu trả lời. Trường no_answer lúc chạy cũng có thể được bật cho câu trả lời một phần; bảng trên dùng partial_answer để phân biệt cờ nguồn một phần, không đếm các câu có nội dung này thành câu rỗng.

Hai lượt chấm khớp mẫu dùng chung v15. Các cờ nguồn là kết quả lưu từ từng workflow/corpus, có bộ kiểm chứng khác phiên bản; chưa phải đánh giá lại bằng cùng một bộ kiểm chứng pháp lý. Baseline có 2 câu không có kiểm chứng độc lập trên đầu ra cuối. Không suy ra mức cải thiện độ chính xác pháp luật từ chênh lệch các cờ này.

Các cờ nguồn chỉ mô tả kiểm chứng với chứng cứ được trích lúc chạy; không chứng nhận toàn bộ nội dung là pháp luật hiện hành. Bản rà từng ý có 161 ý, trong đó 139 ý còn chờ đối chiếu nguồn. Chưa công bố điểm với bản rà như một bộ gold đã xác minh.

| Câu ưu tiên/hồi quy | Khớp mẫu trước → sau | Bao phủ nguồn bản sửa | Provider cuối |
|---|---|---|---|
| 23 | partial → partial | một phần | gemini-agent |
| 26 | high → high | một phần | gemini-agent |
| 27 | partial → partial | một phần | gemini-agent |
| 28 | low → low | một phần | gemini-agent |
| 30 | high → partial | đủ theo cờ lúc chạy | gemini-agent |
| 31 | partial → partial | đủ theo cờ lúc chạy | gemini-agent |
| 32 | partial → partial | một phần | gemini-agent |
| 34 | partial → partial | một phần | gemini-agent |
| 36 | low → partial | một phần | gemini-agent |
| 45 | partial → partial | đủ theo cờ lúc chạy | gemini-agent |
| 50 | high → high | một phần | gemini-agent |
| 58 | partial → partial | một phần | gemini-agent |
| 29 | partial → partial | một phần | gemini-agent |
| 37 | high → high | đủ theo cờ lúc chạy | gemini-agent |
| 47 | high → high | đủ theo cờ lúc chạy | gemini-agent |
| 52 | partial → partial | đủ theo cờ lúc chạy | gemini-agent |

| Các câu đổi nhãn trong toàn bộ 36 câu | Trước → sau |
|---|---|
| 30 | high → partial |
| 36 | low → partial |
| 38 | partial → high |
| 43 | partial → high |
| 48 | high → partial |
| 49 | partial → high |
| 51 | partial → high |
| 56 | partial → high |

Câu 30 và 48 giảm nhãn khớp mẫu. Câu 30 dùng hướng dẫn CANTHOWASSCO có điều kiện IDKH/mã xác nhận và định dạng ZIP/PDF; mẫu nêu PDF/XML cùng các trường chi tiết chưa được toàn bộ đoạn hướng dẫn xác nhận. Câu 48 giữ phạm vi thao tác theo nền tảng và không hứa gỡ mọi tin trong 24 giờ như mẫu. Các khác biệt này cần được đọc cùng nguồn, không tự diễn giải thành câu trả lời sai pháp luật.

Câu 28 vẫn low về khớp mẫu: chưa giữ các mức khoán được gọi là phổ biến, mức tiêu thụ và ngưỡng cao trong mẫu. Dữ liệu đang có chưa chứng minh các khẳng định thống kê đó; giá thực tế vẫn cần hỏi chủ trọ. Không bổ sung số liệu suy đoán để nâng nhãn.

Câu hỏi trong question bank khác câu hỏi đi kèm mẫu ở ID 49. Cả baseline và bản sửa giữ cùng câu hỏi bank; khác biệt với mẫu được lưu trong JSON, không che giấu bằng việc sửa mẫu.

Trace bản sửa: 16 câu được Qwen đánh dấu chọn nguồn một phần; 4 câu giữ riêng các kết luận đã kiểm chứng. Các nhóm này có thể trùng nhau.
Những câu còn lỗi phân loại ở lần kiểm chứng cuối: không có. Những câu có kết luận bị bác bỏ về nội dung ở lần kiểm chứng cuối: 38, 54. Các ID kết luận và lý do nằm trong JSON. Ở các lượt giữ một phần, các ý bị bác bỏ đã được loại khỏi câu trả lời cuối. Đây là chẩn đoán tại lần chạy, không coi mọi cờ một phần là thiếu văn bản nguồn.

Giá điện/nước thực tế của nhà trọ là dữ liệu chủ trọ cung cấp, có thể chưa có và hỏi sau. Không suy đoán giá và không phạt thiếu giá trong tin. Thống kê quảng cáo cục bộ không chứng minh mức phổ biến toàn Cần Thơ.

Chi tiết nguyên văn, các điểm thiếu/khác và trace kiểm chứng từng kết luận nằm trong [báo cáo JSON](D:/AI-powered-system-to-assist-Can-Tho-University-students-in-finding-accommodation--main/eval/reports/legal_repair_36_comparison_v15_20261006.json). Các bản chấm phát triển v9–v14 không tham gia bảng so sánh này; hai bản trong bảng dùng cùng v15, có giữ mệnh đề qua xuống dòng Word.

Corpus mới vẫn là thử riêng; xem [audit nguồn và dữ liệu](D:/AI-powered-system-to-assist-Can-Tho-University-students-in-finding-accommodation--main/eval/reports/legal_repair_audit_v16_20261006.json) về hash dữ liệu đang dùng và nguồn Word.
