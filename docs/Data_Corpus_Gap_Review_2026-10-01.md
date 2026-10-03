# Rà soát khoảng trống bộ tài liệu thuê trọ — 01/10/2026

> Cập nhật sau khi chỉnh sửa bộ trích: xem [bảng metadata hiện hành](Legal_Extract_Metadata_Audit_2026-10-01.md). Nhận định cũ rằng khoản 5 Điều 46 NĐ 105/2025 đã bị bãi bỏ từ 15/09/2026 là không đúng: khoản 2 Điều 30 NĐ 347/2026 có hiệu lực riêng theo khoản 2 Điều 41. PDF NĐ 347 đã được thay bằng bản trích DOCX; bản `.doc` BLDS đã được thay bằng bản trích DOCX.

Phạm vi: 27 file hiện có trong `Data`, phục vụ đề tài hỗ trợ sinh viên Đại học Cần Thơ tìm và thuê chỗ ở. Đây là khuyến nghị chọn nguồn cho hệ thống hỏi đáp, không phải kết luận toàn bộ pháp luật đã được rà soát hiệu lực. Không chỉnh sửa tài liệu gốc hoặc cơ sở dữ liệu trong lần rà soát này.

## Kết luận ưu tiên

Bộ nguồn đã phủ các nhánh chính: hợp đồng/cọc/nhà ở, điện, nước Cần Thơ, tạm trú, PCCC, dữ liệu cá nhân và lừa đảo. **Chưa cần nạp thêm một bộ luật toàn văn.** Việc có tác động lớn hơn là hoàn thiện bản trích, nối văn bản sửa đổi và đánh giá truy xuất theo từng tình huống.

| Mức ưu tiên | File/thư mục | Việc cần làm |
|---|---|---|
| 1 | `Data/fire_safety/Nghị-định-105-2025-NĐ-CP.docx` và `Data/residence/Nghị-định-347-2026-NĐ-CP-trích-tuyển.docx` | Đã bổ sung metadata và ghép nội dung sửa đổi liên quan. Khoản 2 Điều 30 NĐ 347/2026 có hiệu lực riêng theo khoản 2 Điều 41; không ghi khoản 5 Điều 46 NĐ 105/2025 là đã bị bãi bỏ từ 15/09/2026. |
| 1 | `Data/housing_contract/Bộ-luật-91-2015-QH13-trích-tuyển.docx` | Đã thay bản `.doc` bằng bản trích 9 trang về giao dịch, cọc, nghĩa vụ, hợp đồng và thuê tài sản. |
| 1 | Toàn bộ bản trích trong `Data` | Gắn tên/số hiệu văn bản, nguồn chính thức, phạm vi, ngày hiệu lực/kiểm tra và quan hệ sửa đổi ở metadata. Chunk theo điều/khoản, giữ điều kiện và ngoại lệ. Thư mục con trong `Data` vẫn bị quét; không dùng `Data/archive` làm nơi loại nguồn khỏi embedding. |
| 2 | `Data/electricity/Thông-tư-60-2025-TT-BCT.docx`, `Data/housing_contract/2026_204_79_VBHN-VPQH.docx`, `Data/privacy_data/Luật-91-2025-QH15.docx` | Thông tư 60 đã có Điều 1–2, 20–21 và ghi hiệu lực riêng của Điều 12. Hai bản trích còn lại cần định danh, phạm vi và nguồn như bảng metadata hiện hành. |
| 2 | `Data/electricity/Quyết-định-1279-QĐ-BCT.docx`, `Data/water_cantho/Quyết-định-215-QĐ-UBND.docx` | Giữ bảng giá hiện có; thêm đơn vị, đối tượng/khu vực áp dụng, thuế/phí, nguồn cập nhật và ngày kiểm tra. Không tự nhận giá trong file là giá mới nhất nếu chưa kiểm tra tại thời điểm trả lời. |
| 2 | `eval/datasets/` | Hiện bộ kiểm thử pháp lý chỉ có 8 tình huống điện (`legal_electricity_eval.json`). Bổ sung câu hỏi chuẩn cho cọc/hợp đồng, tạm trú, PCCC, nước, quyền riêng tư và nghi lừa đảo; đo độ đúng điều/khoản, trích dẫn và tỷ lệ chunk nhiễu trước/sau rút gọn. Đây là dữ liệu đánh giá, không nạp vào kho luật. |

## Nguồn mới chỉ thêm khi sản phẩm trả lời đúng nhánh đó

1. **Hướng dẫn tạm trú thực hành:** tạo một bản ghi rất ngắn ở `Data/residence/` dẫn tới [thủ tục 1.004194 trên Cổng Dịch vụ công Bộ Công an](https://dichvucong.bocongan.gov.vn/public/link-to/chi-tiet-thu-tuc?ma-thu-tuc=26356). Nguồn hiện nêu nơi nộp, cách nộp và thời hạn xử lý. Chỉ thêm nếu chatbot hướng dẫn từng bước; giữ ngày kiểm tra để tránh lệch khi thủ tục đổi.
2. **Tranh chấp cọc cần khởi kiện:** nếu chatbot tư vấn bước tố tụng dân sự, thêm **trích tuyển nhỏ** từ [Bộ luật Tố tụng dân sự, VBHN 99/VBHN-VPQH](https://vanban.chinhphu.vn/?classid=2629&docid=215211&pageid=27160) vào một nhánh truy xuất riêng. Xác minh điều/khoản áp dụng trước khi tuyển. Nếu chatbot chỉ giải thích hợp đồng, thương lượng và báo tin nghi lừa đảo thì chưa cần thêm.
3. **Ký túc xá ĐH Cần Thơ:** nếu kết quả tìm chỗ ở bao gồm KTX, lưu liên kết [hướng dẫn đăng ký KTX 2026–2027 của trường](https://tansinhvien.ctu.edu.vn/huong-dan-dang-ky-o-ky-tuc-xa) trong nhóm thông tin chỗ ở; phí, điều kiện và thời hạn cần ngày cập nhật. Không trộn nguồn này vào kho quy phạm pháp luật.

## Nguồn động nên đối chiếu thay vì thêm luật dài

- Giá điện: [trang giá điện EVN](https://evn.com.vn/vi-VN/news-l/Gia-dien-60-28) đang công bố Quyết định 1279/QĐ-BCT. Đối chiếu lại trước khi chatbot trả số tiền cụ thể.
- Giá nước: [trang giá nước CANTHOWASSCO](https://ctn-cantho.com.vn/Tin-hoat-dong-cong-ty/gia-nuoc-sach-khu-vuc-do-thi-va-nong-thon-nam-2024-690.html) vẫn đăng giá theo Quyết định 215/QĐ-UBND, áp dụng từ 01/02/2024. Kiểm tra đúng khu vực/đơn vị cấp nước và các khoản phí không nằm trong đơn giá.
- [Nghị định 347/2026/NĐ-CP trên Cổng văn bản Chính phủ](https://vanban.chinhphu.vn/?classid=1&docid=219411&orggroupid=2&pageid=27160) là nguồn sửa đổi chung cho PCCC và cư trú; bản trích DOCX trong `Data/residence/` phải được liên kết tới văn bản gốc tương ứng.

## Lưu ý kỹ thuật khi lập chỉ mục

`apps/api/app/room_service/legal_knowledge/extractor.py` đọc `.docx` thành một trang logic, nên `page_from=1` trong các chunk DOCX không đại diện cho trang Word thật. Ưu tiên trích dẫn số điều/khoản; muốn trích dẫn trang thì lưu số trang gốc riêng trong metadata. File `.doc` cần `antiword`. Sau khi thay nguồn, lập lại chỉ mục và kiểm tra các bản cũ đã được loại khỏi cơ sở dữ liệu; thay file trong `Data` không tự chứng minh chunk cũ đã biến mất.
