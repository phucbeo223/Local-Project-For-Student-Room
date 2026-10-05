# Word và pháp lý thuê trọ cơ bản — 05/10/2026

Phiên bản này hỗ trợ tìm/so sánh nhà trọ cho sinh viên CTU và giải thích quyền lợi, tiền cọc, tiền thuê, điện/nước, cư trú, PCCC, dữ liệu cá nhân và rủi ro lừa đảo ở mức cơ bản. Yêu cầu soạn hợp đồng, điền tờ khai CT01, lập đơn hoặc hướng dẫn thủ tục chuyên sâu được trả về ngoài phạm vi.

## Dữ liệu đang chạy

| Thành phần | Namespace | Số lượng |
|---|---|---:|
| Phòng chính | `public.aggregated_listings` | 789 phòng Datahouse |
| Phòng cho Graph RAG | `housing_graph_word_v6` | 789 vector E5, 384 chiều |
| Pháp lý Word | `legal_word_v7_20261005` | 16 tài liệu, 314 điều/khoản, 325 vector E5 |
| Graph | `graph_rag_word_v6` | 1.144 nút, 3.016 cạnh |

Pháp lý được đọc trực tiếp bằng XML Word/antiword, chia theo điều/khoản và giữ phần điều kiện, ngoại lệ. Không đọc PDF, HTML, Markdown hoặc kết quả OCR làm nội dung kho mới. PDF CT01 và `Data/legal_templates.md` đã xóa. Các tệp khác không nằm trong danh sách Word cho phép được liệt kê là loại trừ trong manifest; tài liệu lịch sử trong Git không phải kho truy xuất đang chạy.

Ba Word do cơ quan nhà nước công bố được tải nguyên byte: Bộ luật Dân sự 91/2015/QH13, Luật PCCC 55/2024/QH15 và Luật Cư trú 68/2020/QH14. 13 Word còn lại là bản cung cấp/trích tuyển: giữ cảnh báo chưa đối chiếu toàn bộ câu chữ với bản chính thức. Hash chỉ chứng minh byte dữ liệu không thay đổi, không chứng minh pháp lý hiện hành. Ghi chú biên tập xen trong điều luật đã loại khỏi nội dung nhúng; các đoạn nguyên văn hai bên vẫn có bằng chứng đối chiếu riêng. Không dùng đáp án mẫu làm nguồn nhúng.

Nguồn và hash nằm trong `docs/legal_word_corpus_v7_20261005/manifest.json`; URL, xuất xứ và điều/khoản nằm trong từng JSON. `Data/word_originals/sources.json` lưu URL tải, thời điểm và hash ba Word công bố. Liên kết gốc đôi khi trỏ đến PDF để mô tả xuất xứ; pipeline mới không tải hoặc OCR liên kết đó.

## Dọn kho cũ và xác minh

Đã sao lưu toàn DB, khôi phục thử sang DB tạm, đối chiếu toàn bộ dòng của kho pháp lý cũ cùng dữ liệu phòng/tài khoản, rồi mới xóa 5 namespace `legal_v2`, `legal_v3_20261004`, `legal_v4_20261004`, `legal_v5_20261004`, `legal_v6_20261005` và các graph cũ. DB phục hồi tạm đã dọn. Kho pháp lý ở `public` trống; corpus đang chạy không có metadata OCR. 789 phòng và 84 tài khoản có hash toàn dòng không đổi sau khi dọn.

108 kiểm thử liên quan đến câu trả lời, định tuyến, nguồn Word và truy xuất graph đã qua; kiểm tra HTTP có đăng nhập cho tìm trọ và hỏi pháp lý đã qua, tài khoản thử được xóa. Audit truy xuất 36 câu đã qua các kiểm tra nguồn/hash/vector/phạm vi; audit này không phải lượt sinh trả lời hoặc đối chiếu đáp án.

Một lượt chạy nhầm bộ test CRUD rộng tạo 9 tài khoản và 5 phòng test; đã xác minh mọi dòng gốc không đổi và xóa chính xác các dòng test đó. Bộ test rộng có 8 lỗi, trong đó phần lớn do fixture/cấu hình cũ không phù hợp với release đang chạy. Không báo bộ test rộng là đã qua.

## Lượt 36 câu

Giữ nguyên 36 ID có đáp án mẫu: 19–38 và 43–58. Không đổi câu hỏi hoặc nạp đáp án vào corpus để tăng điểm. **36/36 câu đã chạy, không có lỗi thực thi**. Workflow dùng Qwen chọn bằng chứng, Gemini tổng hợp và kiểm tra nguồn; 30 phản hồi được sinh qua Gemini, 3 dùng Qwen trích xuất dự phòng và 3 trả thông báo thiếu nguồn. Người dùng đã cho phép Qwen + Gemini qua proxy hiện tại `http://127.0.0.1:8317/v1beta`. Dữ liệu nhà trọ, tài khoản và đáp án mẫu không gửi qua proxy. Chưa xác minh dịch vụ hoặc model thực sự phía sau alias cấu hình.

Đối chiếu toàn bộ 36 câu bằng **Qwen cục bộ**: **0 khớp cao, 27 khớp một phần, 9 khớp thấp**. Cả 36 cần rà soát so với đáp án mẫu; chưa đạt mục tiêu trả lời gần giống mẫu. Nhóm khớp thấp theo ID ngân hàng: **29, 30, 45, 47, 48, 49, 50, 56, 58**. Các câu còn lại khớp một phần. Câu 49 trong tham chiếu khác cách diễn đạt so với câu ngân hàng; đánh giá phải xét phần chung. Đây là đánh giá khớp văn bản, không phải tỷ lệ đúng pháp luật; đáp án mẫu chưa được xác minh và Qwen vừa chọn nguồn vừa chấm nên có thể có thiên lệch.

API đánh dấu 11 câu đủ, 22 câu trả lời một phần và 3 câu không có nguồn (47–49). Cờ đủ không phải kiểm định chất lượng độc lập: chẳng hạn câu 21 vẫn tự nêu nguồn chưa bao quát hết tình huống. Kết quả v15 là lịch sử của corpus khác, không áp dụng cho kho Word này. Báo cáo chi tiết cục bộ: `eval/reports/graph_rag_word_acceptance_v7_2026-10-05.md`; toàn bộ câu trả lời và đối chiếu nằm trong `graph_rag_word_vs_reference_36_v7_2026-10-05.md`. Các kiểm tra phát hành nguồn/hash/vector/HTTP đều qua, nhưng không đồng nghĩa chất lượng đáp án đã đạt.

Khoảng trống nguồn còn lại: hướng dẫn thực tế về bàn giao, sửa chữa, báo trước, tiền cọc và phí thuê; tài liệu nền tảng đăng tin cho câu 47–49; tra cứu hóa đơn nước và phân bổ đồng hồ dùng chung; hướng dẫn lưu chứng từ khi nghi bị lừa. Hướng dẫn hóa đơn trước đây là HTML nên đã bị loại. Không tự tạo tài liệu để lấp chỗ thiếu. Điện có điều kiện chuyển tiếp và giá nước còn cần xác nhận địa bàn/hiệu lực. Một số đáp án mẫu yêu cầu soạn đơn hoặc thủ tục chuyên sâu vượt phạm vi hiện tại; không bổ sung quy trình đó chỉ để tăng điểm. Ba Word có bản công bố gốc, còn 13 Word cung cấp vẫn cần đối chiếu nguyên văn. Hai câu dự phòng 36 và 50 còn dài, cần cải thiện cách trình bày khi bổ sung được nguồn phù hợp.

## Vận hành

`scripts/start_all.ps1` tự nạp lớp `docker-compose.word-legal.yml` sau các lớp cũ; crawler và seed phòng cũ bị tắt khi khởi động thường. `-IndexLegal` cũ dừng với hướng dẫn rebuild Word, tránh vô tình nạp lại corpus OCR. Swagger ở `http://127.0.0.1:8000/docs`.

Ví dụ lệnh chỉ audit, không gọi provider:

```powershell
$wordCompose=@('-p','nckh','-f','docker-compose.yml','-f','docker-compose.override.yml','-f','docker-compose.ragas.yml','-f','docker-compose.legal-refresh.yml','-f','docker-compose.graph-rag.yml','-f','docker-compose.source-grounded.yml','-f','docker-compose.word-legal.yml')
docker compose @wordCompose run --rm --no-deps --entrypoint python ragas-eval /eval/audit_word_release.py --output /eval/reports/graph_rag_word_audit_v7_2026-10-05.json
```

Rebuild dùng `prepare_word_legal_corpus.py` → `index_legal_agent_corpus.py --schema legal_word_v7_20261005 --corpus /workspace/docs/legal_word_corpus_v7_20261005` → `index_graph_rag.py` với namespace tương ứng; khi đổi corpus cần tạo graph version mới và kiểm thử trước khi đổi API. Không chạy các script nhập PDF lịch sử. Backup và báo cáo chi tiết/đáp án tham chiếu giữ cục bộ, không đưa vào GitHub.
