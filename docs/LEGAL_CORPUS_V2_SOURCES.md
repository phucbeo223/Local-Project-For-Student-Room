# Sổ nguồn kho pháp lý legal_v2

Được tạo từ manifest và metadata thực tế. Bản gốc do cơ quan nhà nước công bố; bản OCR/trích cấu trúc do dự án tạo, không phải một bản hợp nhất được Chính phủ phê duyệt.
Không suy ra hiệu lực hiện hành chỉ từ việc tải được tệp. Tài liệu trích tuyển kế thừa chưa được xác nhận từng chữ với toàn văn.
`source_start` và `source_end` là vị trí ký tự trong văn bản trích đã chuẩn hóa, không phải vị trí byte/trang của PDF gốc. Số trang PDF là trang vật lý; nguồn DOC/DOCX/Markdown dùng trang trong bản trích.

Manifest SHA-256: `deff554affb9ed10c141b7718822bb2a5bd84d758f3707d1f6ba0a0799f0e20f`.

| Tài liệu đầu vào | Chủ đề | Điều đã chọn | Số đơn vị | Nguồn công bố | Cách trích/kiểm chứng |
|---|---|---|---:|---|---|
| Văn-bản-hợp-nhất-135-VBHN-VPQH | criminal_law | 8, 134, 155, 156, 157, 158, 159, 170, 173, 174, 175, 176, 178, 288, 290, 313, 314 | 63 | [Cơ quan nhà nước](https://congbao.chinhphu.vn/tai-ve-van-ban-so-135-vbhn-vpqh-46165-58894?format=pdf) | existing selected text; editorial header excluded by article parser; not verified word by word against full government original |
| Văn-bản-hợp-nhất-17-VBHN-VPQH | criminal_law | 30, 56, 62, 86, 87, 88, 99, 144, 145, 146, 147 | 36 | [Cơ quan nhà nước](https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-17-vbhn-vpqh-468961.htm) | existing selected text; editorial header excluded by article parser; not verified word by word against full government original |
| rental_warning-Bo-Cong-an-20261003 | criminal_law | Khuyến cáo, không đánh số điều | 1 | [Cơ quan nhà nước](https://www.bocongan.gov.vn/bai-viet/canh-giac-voi-chieu-tro-lua-dao-dat-coc-thue-nha-tro-qua-mang-1782485063) | existing selected text; editorial header excluded by article parser; {'type': 'khuyến cáo', 'scope': 'thuê nhà qua mạng'} |
| online_warning-Bo-Cong-an-20261003 | ecommerce_platform | Khuyến cáo, không đánh số điều | 1 | [Cơ quan nhà nước](https://www.bocongan.gov.vn/bai-viet/xuat-hien-thu-doan-lua-dao-moi-khi-mua-hang-online-1790562304) | existing selected text; editorial header excluded by article parser; {'type': 'khuyến cáo', 'scope': 'mua hàng trực tuyến; không biến thành nghĩa vụ pháp lý thuê trọ'} |
| Luật-61-2024-QH15 | electricity | 2, 9, 44, 48, 49, 50, 56, 57, 63, 66, 74 | 50 | [Cơ quan nhà nước](https://vanban.chinhphu.vn/?docid=212489&pageid=27160) | existing selected text; editorial header excluded by article parser; not verified word by word against full government original |
| Quyết-định-1279-QĐ-BCT | electricity | 1, 2, 3 | 3 | [Cơ quan nhà nước](https://vanban.chinhphu.vn/?classid=2&docid=213617&pageid=27160) | existing selected text; editorial header excluded by article parser; not verified word by word against full government original |
| Thông-tư-60-2025-TT-BCT | electricity | 1, 2, 3, 6, 12, 20, 21 | 18 | [Cơ quan nhà nước](https://vanban.chinhphu.vn/?docid=216125&orggroupid=4&pageid=27160) | existing selected text; editorial header excluded by article parser; not verified word by word against full government original |
| Luat-55-2024-QH15-dieu-8-20-21-23-24 | fire_safety | 8, 20, 21, 23, 24 | 24 | [Cơ quan nhà nước](https://datafiles.chinhphu.vn/cpp/files/vbpq/2025/01/luat55.pdf) | existing selected text; editorial header excluded by article parser; {'articles': [8, 20, 21, 23, 24], 'extraction': 'Văn bản PDF có lớp chữ; bỏ đầu trang Công báo, nối dòng; giữ nguyên khoản, điểm.', 'amendment': 'Luật 118 Điều 10 không sửa các điều được trích này; không suy rộng sang điều khác.'} |
| Nghị-định-105-2025-NĐ-CP | fire_safety | 3, 13, 14, 45, 46 | 14 | [Cơ quan nhà nước](https://vanban.chinhphu.vn/?classid=0&docid=213702&pageid=27160) | existing selected text; editorial header excluded by article parser; not verified word by word against full government original |
| 2026_204_79_VBHN-VPQH | housing_contract | 10, 11, 57, 160, 161, 162, 163, 164, 168, 170, 171, 172, 173, 194 | 58 | [Cơ quan nhà nước](https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-79-vbhn-vpqh-469209.htm) | existing selected text; editorial header excluded by article parser; not verified word by word against full government original |
| Bo-luat-91-2015-QH13-doi-chieu-20261003 | housing_contract | 116, 117, 119, 124, 127, 131, 328, 351, 357, 360, 361, 385, 387, 398, 400, 401, 403, 404, 405, 406, 407, 418, 419, 421, 422, 423, 427, 428, 429, 472, 473, 474, 475, 476, 477, 478, 479, 480, 481, 482, 688, 689 | 109 | [Cơ quan nhà nước](https://datafiles.chinhphu.vn/cpp/files/vbpq/2016/01/91.signed.pdf) | existing selected text; editorial header excluded by article parser; {'replaced': [328, 689], 'visual_pages_328': [86, 87], 'other_articles': 'Giữ nguyên bản trích trước; kiểm tra đuôi đoạn, không khẳng định đã đối chiếu toàn văn từng chữ.'} |
| Luật-19-2023-QH15 | housing_contract | 3, 4, 10, 15, 16, 17, 18, 19 | 38 | [Cơ quan nhà nước](https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-47-vbhn-vpqh-469132.htm) | existing selected text; editorial header excluded by article parser; not verified word by word against full government original |
| Nghị-định-95-2024-NĐ-CP | housing_contract | 1, 2, 41, 42, 93, 94 | 10 | [Cơ quan nhà nước](https://vanban.chinhphu.vn/?classid=0&docid=210761&pageid=27160) | existing selected text; editorial header excluded by article parser; not verified word by word against full government original |
| Luật-26-2023-QH15 | privacy_data | 7, 20, 29 | 19 | [Cơ quan nhà nước](https://vanban.chinhphu.vn/?classid=1&docid=209628&orggroupid=1&pageid=27160) | existing selected text; editorial header excluded by article parser; not verified word by word against full government original |
| Luật-91-2025-QH15 | privacy_data | 3, 4, 5, 7, 8, 9, 10, 11, 15, 16, 17, 18, 19, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39 | 129 | [Cơ quan nhà nước](https://vanban.chinhphu.vn/?docid=214590&pageid=27160) | existing selected text; editorial header excluded by article parser; not verified word by word against full government original |
| Nghị-định-330-2026-NĐ-CP | privacy_data | 1, 7, 13 | 10 | [Cơ quan nhà nước](https://vanban.chinhphu.vn/?classid=1&docid=219266&pageid=27160) | existing selected text; editorial header excluded by article parser; not verified word by word against full government original |
| Nghị-định-356-2025-NĐ-CP | privacy_data | 1, 2, 3, 4, 5, 6, 7, 21, 28, 29 | 46 | [Cơ quan nhà nước](https://vanban.chinhphu.vn/?classid=1&docid=216387&pageid=27160) | existing selected text; editorial header excluded by article parser; not verified word by word against full government original |
| Luật-29-2023-QH15 | real_estate_brokerage | 1, 2, 3, 4, 6, 8, 9, 14, 16, 18, 19, 20, 21, 44, 45, 46, 47, 48, 61, 62, 63, 64, 65 | 83 | [Cơ quan nhà nước](https://vanban.chinhphu.vn/?classid=1&docid=209624&pageid=27160&typegroupid=3) | existing selected text; editorial header excluded by article parser; not verified word by word against full government original |
| Luat-68-2020-QH14-doi-chieu-20261003 | residence | 9, 27, 28, 30 | 13 | [Cơ quan nhà nước](https://congan.lamdong.gov.vn/UpLoaded/files/luat/68_2020_QH14.pdf) | existing selected text; editorial header excluded by article parser; {'articles': [9, 27, 28, 30], 'visual_pages': {'residence68': [5, 15, 16], 'amend118': [12, 13]}, 'amendment': 'Điều 4 khoản 9 Luật 118 thay Điều 30, áp dụng từ 01/07/2026; Điều 9,27,28 giữ nội dung gốc.', 'ocr': 'Chép đối chiếu ảnh: sửa Điền/Hỗ/tài Hiệu/tam tri; giữ đủ khoản, điểm và ngoại lệ.', 'article31': 'Nội dung sửa đổi vẫn có trong tài liệu Luật 118 riêng.'} |
| Nghị-định-282-2025-NĐ-CP | residence | 1, 2, 3, 5, 6, 9, 10, 11, 69, 70 | 41 | [Cơ quan nhà nước](https://vanban.chinhphu.vn/?classid=1&docid=219411&orggroupid=2&pageid=27160) | existing selected text; editorial header excluded by article parser; not verified word by word against full government original |
| Nghị-định-347-2026-NĐ-CP-trích-tuyển | residence | 17, 18, 29, 30, 35, 41 | 11 | [Cơ quan nhà nước](https://vanban.chinhphu.vn/?classid=1&docid=219411&orggroupid=2&pageid=27160) | existing selected text; editorial header excluded by article parser; not verified word by word against full government original |
| Luật Thương mại điện tử 122/2025/QH15 | ecommerce_platform | 1, 2, 3, 4, 5, 15, 16, 17, 18, 19, 20, 40 | 51 | [Cơ quan nhà nước](https://vanban.chinhphu.vn/?docid=216503&pageid=27160) | Tesseract vie+eng from signed government PDF; no automatic legal-word correction; OCR; selected critical pages visually checked, other text requires review |
| Nghị định 248/2026/NĐ-CP | ecommerce_platform | 1, 2, 3, 4, 7, 17, 18, 19, 20, 52 | 57 | [Cơ quan nhà nước](https://vanban.chinhphu.vn/?docid=218747&pageid=27160) | Tesseract vie+eng from signed government PDF; no automatic legal-word correction; OCR; selected critical pages visually checked, other text requires review |
| Quyết định 14/2025/QĐ-TTg | electricity | 1, 2, 3, 4, 6, 7 | 23 | [Cơ quan nhà nước](https://vanban.chinhphu.vn/?docid=213782&pageid=27160) | Tesseract vie+eng from signed government PDF; no automatic legal-word correction; OCR; selected critical pages visually checked, other text requires review |
| Nghị định 133/2026/NĐ-CP | electricity | 1, 2, 4, 13, 30, 31 | 24 | [Cơ quan nhà nước](https://vanban.chinhphu.vn/?docid=217612&pageid=27160) | Tesseract vie+eng from signed government PDF; no automatic legal-word correction; OCR; selected critical pages visually checked, other text requires review |
| Nghị định 106/2025/NĐ-CP | fire_safety | 1, 2, 3, 4, 11, 12, 13, 20, 21, 22, 23, 24, 25, 39, 40 | 89 | [Cơ quan nhà nước](https://vanban.chinhphu.vn/?docid=213672&pageid=27160) | Tesseract vie+eng from signed government PDF; no automatic legal-word correction; OCR; selected critical pages visually checked, other text requires review |
| Nghị định 154/2024/NĐ-CP | residence | 1, 2, 5, 6, 7, 16 | 35 | [Cơ quan nhà nước](https://vanban.chinhphu.vn/?docid=211821&pageid=27160) | Tesseract vie+eng from signed government PDF; no automatic legal-word correction; OCR; selected critical pages visually checked, other text requires review |
| Nghị định 58/2026/NĐ-CP | residence | 4, 6 | 18 | [Cơ quan nhà nước](https://vanban.chinhphu.vn/?docid=216977&pageid=27160) | Tesseract vie+eng from signed government PDF; no automatic legal-word correction; OCR; selected critical pages visually checked, other text requires review |
| Thông tư 116/2026/TT-BCA | residence | 1, 2, 3, 6, 12, 13, 14, 15, 27 | 37 | [Cơ quan nhà nước](https://vanban.bocongan.gov.vn/co-so-du-lieu-van-ban/thong-tu-quy-dinh-chi-tiet-mot-so-dieu-va-bien-phap-thi-hanh-luat-cu-tru-1784261073) | Tesseract vie+eng from signed government PDF; no automatic legal-word correction; OCR; selected critical pages visually checked, other text requires review |
| Luật 118/2025/QH15 | residence | 4, 10, 11 | 18 | [Cơ quan nhà nước](https://datafiles.chinhphu.vn/cpp/files/vbpq/2026/01/luatso118.2025.pdf) | government PDF text/OCR; OCR/raw text; not all words visually reviewed |
| Nghị định 347/2026/NĐ-CP | residence | 17, 18, 19, 29, 30, 32, 33, 35, 41 | 20 | [Cơ quan nhà nước](https://datafiles.chinhphu.vn/cpp/files/vbpq/2026/9/347_2026_nd-cp_08092026_7-signed.signed.pdf) | government PDF text/OCR; OCR/raw text; not all words visually reviewed |
| Nghị định 117/2007/NĐ-CP | water_cantho | 1, 2, 44, 48, 49, 50, 54, 56, 57, 58, 65, 66 | 51 | [Cơ quan nhà nước](https://vanban.chinhphu.vn/?docid=33015&pageid=27160) | antiword from government original; original attachment; no OCR; supply-contract parties distinct from landlord/tenant |
| Nghị định 124/2011/NĐ-CP | water_cantho | 1, 2, 3 | 17 | [Cơ quan nhà nước](https://vanban.chinhphu.vn/?docid=153298&pageid=27160) | antiword from government original; original attachment; no OCR; supply-contract parties distinct from landlord/tenant |

## Dấu vết từng nguồn

SHA đầu vào dưới đây áp dụng cho tệp đầu vào nêu trong metadata. Với bản trích kế thừa, đây là hash bản trích; hash bản gốc được lưu riêng trong manifest tải nguồn và `origin_documents` nếu đã xác thực.

### legacy-c689645e534f

- Tệp cấu trúc: `docs/legal_corpus_v2/legacy-c689645e534f.json`.
- SHA cấu trúc: `72595b20231f0802474088983ddd29397bcb250605356c9ab300db3b0dbdf67d`.
- Đầu vào: `Data/criminal_law/Văn-bản-hợp-nhất-135-VBHN-VPQH.docx`.
- SHA đầu vào: `75794b3769abfb6aa6682494adab15f4856a853a4564b88a42a33bcec29138f1`.
- Nguồn: https://congbao.chinhphu.vn/tai-ve-van-ban-so-135-vbhn-vpqh-46165-58894?format=pdf

### legacy-95df8751459d

- Tệp cấu trúc: `docs/legal_corpus_v2/legacy-95df8751459d.json`.
- SHA cấu trúc: `657f162303c7888536fbe01b95fc28b198d3a7ca0aca87bf75a40c38da56d95b`.
- Đầu vào: `Data/criminal_law/Văn-bản-hợp-nhất-17-VBHN-VPQH.docx`.
- SHA đầu vào: `da4fbd8f39bc46ad96059d54e4baa40236cfbe41e69aaceb11dcedadcb3e1ff5`.
- Nguồn: https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-17-vbhn-vpqh-468961.htm

### legacy-092b57ace14c

- Tệp cấu trúc: `docs/legal_corpus_v2/legacy-092b57ace14c.json`.
- SHA cấu trúc: `71ab2356b7e18b92af80e82383d9521649750176a11041e94f652055d13d4883`.
- Đầu vào: `Data/criminal_law/rental_warning-Bo-Cong-an-20261003.md`.
- SHA đầu vào: `cd12e433ce3cf7fb254a094e138079707c305584b30088728e10739c751d8f1d`.
- Nguồn: https://www.bocongan.gov.vn/bai-viet/canh-giac-voi-chieu-tro-lua-dao-dat-coc-thue-nha-tro-qua-mang-1782485063
- Bản gốc đối chiếu: `docs/legal_sources_originals_20261003/rental_warning.html`; SHA `07146994c89f2a470e49a16b23a819cb0ac92b8bc2ee2d0d6728fa6c2a19cc30`; https://www.bocongan.gov.vn/bai-viet/canh-giac-voi-chieu-tro-lua-dao-dat-coc-thue-nha-tro-qua-mang-1782485063

### legacy-e9adeff06c7a

- Tệp cấu trúc: `docs/legal_corpus_v2/legacy-e9adeff06c7a.json`.
- SHA cấu trúc: `67e6c9c792a73bd385e8cdef723ad9549487d07d84c3566cf5ed358aa2704a38`.
- Đầu vào: `Data/ecommerce_platform/online_warning-Bo-Cong-an-20261003.md`.
- SHA đầu vào: `fef0b5e4f0758f5e19a443296f75915429c0fb3ffa488af40e97a09329c367e3`.
- Nguồn: https://www.bocongan.gov.vn/bai-viet/xuat-hien-thu-doan-lua-dao-moi-khi-mua-hang-online-1790562304
- Bản gốc đối chiếu: `docs/legal_sources_originals_20261003/online_warning.html`; SHA `38580ac8ee4ffac4ecdeef71db7901d94ad329552d0a524eb5dc83247e046a7e`; https://www.bocongan.gov.vn/bai-viet/xuat-hien-thu-doan-lua-dao-moi-khi-mua-hang-online-1790562304

### legacy-790737668504

- Tệp cấu trúc: `docs/legal_corpus_v2/legacy-790737668504.json`.
- SHA cấu trúc: `b69dd3ed61457bd0e1541730e09a246159a0133966681426565b8cee370624a7`.
- Đầu vào: `Data/electricity/Luật-61-2024-QH15.docx`.
- SHA đầu vào: `8e7b189d5dc975d08131945e11368e389f7a68e625762ea90d05344b385b3087`.
- Nguồn: https://vanban.chinhphu.vn/?docid=212489&pageid=27160

### legacy-d9f68871fe49

- Tệp cấu trúc: `docs/legal_corpus_v2/legacy-d9f68871fe49.json`.
- SHA cấu trúc: `dd2dc5525c1bade785c742c721fe1b7d81e7e8fb24d7889d428370ba5107cc72`.
- Đầu vào: `Data/electricity/Quyết-định-1279-QĐ-BCT.docx`.
- SHA đầu vào: `1d243991970650c5dc4bcf2bea1cb21289444f6eace2fcf183a6bae299724486`.
- Nguồn: https://vanban.chinhphu.vn/?classid=2&docid=213617&pageid=27160

### legacy-d873b9410011

- Tệp cấu trúc: `docs/legal_corpus_v2/legacy-d873b9410011.json`.
- SHA cấu trúc: `d1ff53f998c22a85e3e913d40830465f0e159616ee36b2e95a5f11d87775bfe6`.
- Đầu vào: `Data/electricity/Thông-tư-60-2025-TT-BCT.docx`.
- SHA đầu vào: `281c5617cc3a5e567fcbe446e405049fc2d8942cb02ab5a183a8b071af1be94f`.
- Nguồn: https://vanban.chinhphu.vn/?docid=216125&orggroupid=4&pageid=27160

### legacy-da7dcada906d

- Tệp cấu trúc: `docs/legal_corpus_v2/legacy-da7dcada906d.json`.
- SHA cấu trúc: `135c654518b25fc849bfb87807b9091bddd2c7205b5da9998bcecd5958d76b16`.
- Đầu vào: `Data/fire_safety/Luat-55-2024-QH15-dieu-8-20-21-23-24.md`.
- SHA đầu vào: `0ccafc9e862919a86083ac57ecd07b265cc3f7ceb11c32c53c0659700d502434`.
- Nguồn: https://datafiles.chinhphu.vn/cpp/files/vbpq/2025/01/luat55.pdf
- Bản gốc đối chiếu: `docs/legal_sources_originals_20261003/fire55.pdf`; SHA `1b1942dbf11e912a28ac2004d1f3cca3b6e7356796507dda7450ccf27a250462`; https://datafiles.chinhphu.vn/cpp/files/vbpq/2025/01/luat55.pdf
- Bản gốc đối chiếu: `docs/legal_sources_originals_20261003/amend118.pdf`; SHA `a9798bfab6120963834d26559ab8614003ca3012de1d1846305495e8bb4300b6`; https://datafiles.chinhphu.vn/cpp/files/vbpq/2026/01/luatso118.2025.pdf

### legacy-8fb07729dbcb

- Tệp cấu trúc: `docs/legal_corpus_v2/legacy-8fb07729dbcb.json`.
- SHA cấu trúc: `88ce9a98488e8e4918f52464ee3f3078a21a035a2db8d3aae6bb01c64de93384`.
- Đầu vào: `Data/fire_safety/Nghị-định-105-2025-NĐ-CP.docx`.
- SHA đầu vào: `96d3c8812018b49f0968bf43f4d9785c8e7d87536cec262e2a904f7cb4021b23`.
- Nguồn: https://vanban.chinhphu.vn/?classid=0&docid=213702&pageid=27160

### legacy-4bcf6ab450b3

- Tệp cấu trúc: `docs/legal_corpus_v2/legacy-4bcf6ab450b3.json`.
- SHA cấu trúc: `b917938825b162618e93e0b15767c20065064a8ac3f3d3f9689089d904a63821`.
- Đầu vào: `Data/housing_contract/2026_204_79_VBHN-VPQH.docx`.
- SHA đầu vào: `74e00cffe24839460eddf3b266c84eda90bf31370d27498c68a96442dd9172a2`.
- Nguồn: https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-79-vbhn-vpqh-469209.htm

### legacy-e010a14386b4

- Tệp cấu trúc: `docs/legal_corpus_v2/legacy-e010a14386b4.json`.
- SHA cấu trúc: `4be57d06036c732fe8f2b1ff6c5a8ba53af0123437c039d88f2c8709621ca76f`.
- Đầu vào: `Data/housing_contract/Bo-luat-91-2015-QH13-doi-chieu-20261003.md`.
- SHA đầu vào: `e36235277d9ced3a03df409f0a7a167ef48b2156fae4504ebcb3ec46bf2dffde`.
- Nguồn: https://datafiles.chinhphu.vn/cpp/files/vbpq/2016/01/91.signed.pdf
- Bản gốc đối chiếu: `docs/legal_sources_originals_20261003/civil91first.pdf`; SHA `d2f9e486faa8aa205dff952c813251acb82475a614b388d2a52449a05dd37205`; https://datafiles.chinhphu.vn/cpp/files/vbpq/2016/01/91.signed.pdf
- Bản gốc đối chiếu: `docs/legal_sources_originals_20261003/civil91.pdf`; SHA `dd2c45f8dee4e0d7b0416786b236e9588092863edcef64db07ef2b74954bba50`; https://datafiles.chinhphu.vn/cpp/files/vbpq/2016/01/91_.pdf

### legacy-6f667af18760

- Tệp cấu trúc: `docs/legal_corpus_v2/legacy-6f667af18760.json`.
- SHA cấu trúc: `4d4d64426444319fc2bc31014d30c1737f68a86d59fadf9397506139bd772349`.
- Đầu vào: `Data/housing_contract/Luật-19-2023-QH15.docx`.
- SHA đầu vào: `295107f2a9562ec3eefcd5237c6e42b09e12fb84b11fc1010feecc8768f219c7`.
- Nguồn: https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-47-vbhn-vpqh-469132.htm

### legacy-60dd067ea62d

- Tệp cấu trúc: `docs/legal_corpus_v2/legacy-60dd067ea62d.json`.
- SHA cấu trúc: `be5397b73084eda7df8a831115f1ce16faab0802e163ba617a7e00e4fd9c9cc9`.
- Đầu vào: `Data/housing_contract/Nghị-định-95-2024-NĐ-CP.docx`.
- SHA đầu vào: `4474ba0ef040a9ddf0a2504f914c35d28320bac04b09b6b6c45503178c635a2d`.
- Nguồn: https://vanban.chinhphu.vn/?classid=0&docid=210761&pageid=27160

### legacy-f29b4cc9f353

- Tệp cấu trúc: `docs/legal_corpus_v2/legacy-f29b4cc9f353.json`.
- SHA cấu trúc: `4d334b001ac6251738fa2070dbad25066849dac32d35856016788d3e77bcc084`.
- Đầu vào: `Data/privacy_data/Luật-26-2023-QH15.docx`.
- SHA đầu vào: `1b5b0197b978c7fc879045db01f1a3843ff9416050e12c99d6941bb9f5958f15`.
- Nguồn: https://vanban.chinhphu.vn/?classid=1&docid=209628&orggroupid=1&pageid=27160

### legacy-3466ad78b47f

- Tệp cấu trúc: `docs/legal_corpus_v2/legacy-3466ad78b47f.json`.
- SHA cấu trúc: `14e1662ad2c7164fa385b76f252da068c88217eb1cc1d816747cbf011bf4c2d6`.
- Đầu vào: `Data/privacy_data/Luật-91-2025-QH15.docx`.
- SHA đầu vào: `e7d93bdbebca5d2202e0b721f3eeda42c227ba7e81175f8336c73543b214bd3a`.
- Nguồn: https://vanban.chinhphu.vn/?docid=214590&pageid=27160

### legacy-3c1db7d7a4f0

- Tệp cấu trúc: `docs/legal_corpus_v2/legacy-3c1db7d7a4f0.json`.
- SHA cấu trúc: `64708895fd138be27ee85db53cce4160e365c256df219ba17d7d10cc55529a27`.
- Đầu vào: `Data/privacy_data/Nghị-định-330-2026-NĐ-CP.docx`.
- SHA đầu vào: `d61016274577aa6558eeb4275bf75f1ec8deb67fa84ab22bdb8e701e7837d3d0`.
- Nguồn: https://vanban.chinhphu.vn/?classid=1&docid=219266&pageid=27160

### legacy-e2f946f8fa90

- Tệp cấu trúc: `docs/legal_corpus_v2/legacy-e2f946f8fa90.json`.
- SHA cấu trúc: `1d02e28fbf922f33c1d8faf8009af3491249b5084210dc754d6cb0c85ef7d947`.
- Đầu vào: `Data/privacy_data/Nghị-định-356-2025-NĐ-CP.docx`.
- SHA đầu vào: `9265afaa636da509567bfb519a85cc8830b3072b90ded60fdf1635c9a9b00203`.
- Nguồn: https://vanban.chinhphu.vn/?classid=1&docid=216387&pageid=27160

### legacy-97260a1a9fb2

- Tệp cấu trúc: `docs/legal_corpus_v2/legacy-97260a1a9fb2.json`.
- SHA cấu trúc: `bbac9c32b02779c532a66fa47f5c672fb979712e8984e26bd967ea7e2fa7b338`.
- Đầu vào: `Data/real_estate_brokerage/Luật-29-2023-QH15.docx`.
- SHA đầu vào: `147363772a45ea4beb11b6983111046beea45d9ba61d71884353b79c7160a4d9`.
- Nguồn: https://vanban.chinhphu.vn/?classid=1&docid=209624&pageid=27160&typegroupid=3

### legacy-101ff31eaab8

- Tệp cấu trúc: `docs/legal_corpus_v2/legacy-101ff31eaab8.json`.
- SHA cấu trúc: `504d09ee1cc9a8b2c12b5d7483bc7149b7697dd149d6207c2e5d5960a32df2fc`.
- Đầu vào: `Data/residence/Luat-68-2020-QH14-doi-chieu-20261003.md`.
- SHA đầu vào: `1b2041ad5663165a8fcf7c4a3ba17d16dcdf972ce7fcb663cf07a2c224efd467`.
- Nguồn: https://congan.lamdong.gov.vn/UpLoaded/files/luat/68_2020_QH14.pdf
- Bản gốc đối chiếu: `docs/legal_sources_originals_20261003/residence68.pdf`; SHA `fda03bdaa433b3e86807d9fa0e6cdae50d1ea2ae37aa59ffe992f1de1c7f17d1`; https://congan.lamdong.gov.vn/UpLoaded/files/luat/68_2020_QH14.pdf
- Bản gốc đối chiếu: `docs/legal_sources_originals_20261003/amend118.pdf`; SHA `a9798bfab6120963834d26559ab8614003ca3012de1d1846305495e8bb4300b6`; https://datafiles.chinhphu.vn/cpp/files/vbpq/2026/01/luatso118.2025.pdf

### legacy-27f5c84dac1d

- Tệp cấu trúc: `docs/legal_corpus_v2/legacy-27f5c84dac1d.json`.
- SHA cấu trúc: `378fc12fd6d47010fdd0bd2d5842475733bb7a6f6172902fb56294d9cd11f380`.
- Đầu vào: `Data/residence/Nghị-định-282-2025-NĐ-CP.docx`.
- SHA đầu vào: `88364570c14e3ec6a3d4160348014653792c29381215eba9c67fe3de75c503bb`.
- Nguồn: https://vanban.chinhphu.vn/?classid=1&docid=219411&orggroupid=2&pageid=27160

### legacy-a2219789861b

- Tệp cấu trúc: `docs/legal_corpus_v2/legacy-a2219789861b.json`.
- SHA cấu trúc: `123791c12eb5390dd338784801843ab0d19486b27b33b5ae21c913039278a056`.
- Đầu vào: `Data/residence/Nghị-định-347-2026-NĐ-CP-trích-tuyển.docx`.
- SHA đầu vào: `6278d09004af459055079807c7318da3d8a7bb2a89c5233d5bfc9636260d9059`.
- Nguồn: https://vanban.chinhphu.vn/?classid=1&docid=219411&orggroupid=2&pageid=27160

### ecommerce122

- Tệp cấu trúc: `docs/legal_corpus_v2/ecommerce122.json`.
- SHA cấu trúc: `53773c789ec7862a0930de1efb5322d20cc136a659f702da843f0edabfa93b6f`.
- Đầu vào: `docs/legal_agent_originals_20261003/ecommerce122.pdf`.
- SHA đầu vào: `10eb9faf1384bebaff64c30beccdc4dbd2713dc251f5d1c2714c6514c9b58e44`.
- Nguồn: https://vanban.chinhphu.vn/?docid=216503&pageid=27160

### ecommerce248

- Tệp cấu trúc: `docs/legal_corpus_v2/ecommerce248.json`.
- SHA cấu trúc: `36137bf37a16c4bb91d2faf4aa7c749c00c947881c3797b7b24b9eed72b988b8`.
- Đầu vào: `docs/legal_agent_originals_20261003/ecommerce248.pdf`.
- SHA đầu vào: `9829949d91358428be627a613474efebb31748175d133c70410b02118e8c7f3e`.
- Nguồn: https://vanban.chinhphu.vn/?docid=218747&pageid=27160

### electricity14

- Tệp cấu trúc: `docs/legal_corpus_v2/electricity14.json`.
- SHA cấu trúc: `16bb9431cfb32038e39ca546f4c63140334c4f21040c16ebc8d40f91f57cc591`.
- Đầu vào: `docs/legal_agent_originals_20261003/electricity14.pdf`.
- SHA đầu vào: `733bfe8f53bbf8b320e2b501711bd4617768197f7f5bc0f1279236ded7569053`.
- Nguồn: https://vanban.chinhphu.vn/?docid=213782&pageid=27160

### electricity133

- Tệp cấu trúc: `docs/legal_corpus_v2/electricity133.json`.
- SHA cấu trúc: `95c1689896df8597c4a4c80d6d37918b9b1d39505e9bb9d89cd706464e9ef4c9`.
- Đầu vào: `docs/legal_agent_originals_20261003/electricity133.pdf`.
- SHA đầu vào: `87be0af90b962085aa6a4c56fea6d10f6273d0a1ea9841f66aeaf5034628c885`.
- Nguồn: https://vanban.chinhphu.vn/?docid=217612&pageid=27160

### fire106

- Tệp cấu trúc: `docs/legal_corpus_v2/fire106.json`.
- SHA cấu trúc: `bb344e8117f6542b5663a736fa745d6f11cf923927e434dc92613194c6f1416e`.
- Đầu vào: `docs/legal_agent_originals_20261003/fire106.pdf`.
- SHA đầu vào: `67f0d65f360ea44055942dc2639e0dbbbc1c29b22faabdfd7259cbbb224114f2`.
- Nguồn: https://vanban.chinhphu.vn/?docid=213672&pageid=27160

### residence154

- Tệp cấu trúc: `docs/legal_corpus_v2/residence154.json`.
- SHA cấu trúc: `cbd0d85706d90c1f84d1d70a221008691aa472c5205480168a818bc2d3d0477f`.
- Đầu vào: `docs/legal_agent_originals_20261003/residence154.pdf`.
- SHA đầu vào: `ca6079a7dd0b0d2b95f8c94f9175e4d8b57b8a5a79e3079d40ed1000deb665f6`.
- Nguồn: https://vanban.chinhphu.vn/?docid=211821&pageid=27160

### amend58

- Tệp cấu trúc: `docs/legal_corpus_v2/amend58.json`.
- SHA cấu trúc: `0650ebf3b4b060078faac667332a8aeec0652e8a715052d918cf4ae58b902a17`.
- Đầu vào: `docs/legal_agent_originals_20261003/amend58.pdf`.
- SHA đầu vào: `17e965c08c9191c8d9827f29abb1c31bb9ea2ab237ad807c8c803a349f4dcce3`.
- Nguồn: https://vanban.chinhphu.vn/?docid=216977&pageid=27160

### residence116

- Tệp cấu trúc: `docs/legal_corpus_v2/residence116.json`.
- SHA cấu trúc: `989f4d9b0e29ab67061c502b71649144d1ce8169240700876772d7d144fe779a`.
- Đầu vào: `docs/legal_agent_originals_20261003/residence116.pdf`.
- SHA đầu vào: `c7f081986711630f8ecd80a2ef3a07c3c7bf7208ae6c48d37b3effb18994af9f`.
- Nguồn: https://vanban.bocongan.gov.vn/co-so-du-lieu-van-ban/thong-tu-quy-dinh-chi-tiet-mot-so-dieu-va-bien-phap-thi-hanh-luat-cu-tru-1784261073

### amend118

- Tệp cấu trúc: `docs/legal_corpus_v2/amend118.json`.
- SHA cấu trúc: `8bccc00fdab432625772a53a628fbd757757ef6ae18104e2aeaa36abef66eb7a`.
- Đầu vào: `docs/legal_sources_originals_20261003/amend118.pdf`.
- SHA đầu vào: `a9798bfab6120963834d26559ab8614003ca3012de1d1846305495e8bb4300b6`.
- Nguồn: https://datafiles.chinhphu.vn/cpp/files/vbpq/2026/01/luatso118.2025.pdf

### amend347

- Tệp cấu trúc: `docs/legal_corpus_v2/amend347.json`.
- SHA cấu trúc: `b9f8583d30e831f4f3b0f1f1fa9d42d009faa34efdbd85ebbfbe6cb7ab555f94`.
- Đầu vào: `docs/legal_sources_originals_20261003/amend347.pdf`.
- SHA đầu vào: `9559542193426a0f7ab7f3bacb133cd37c810c418ad68616d6f349820bc3f550`.
- Nguồn: https://datafiles.chinhphu.vn/cpp/files/vbpq/2026/9/347_2026_nd-cp_08092026_7-signed.signed.pdf

### water117

- Tệp cấu trúc: `docs/legal_corpus_v2/water117.json`.
- SHA cấu trúc: `ee27cf156658d95519ef6e066796e189c3b930f4c05247e623a999a9990e54cf`.
- Đầu vào: `docs/legal_agent_originals_20261003/water117.doc`.
- SHA đầu vào: `baa30359ccb0743198f23d02fe2b8461603c50e1fe99e4a0d6c02601ded21dd6`.
- Nguồn: https://vanban.chinhphu.vn/?docid=33015&pageid=27160

### water124

- Tệp cấu trúc: `docs/legal_corpus_v2/water124.json`.
- SHA cấu trúc: `e6f28a04aeb8c3937848e9a9946d86f1cf7a3f8d07a3d26b866bfd5298f90ac8`.
- Đầu vào: `docs/legal_agent_originals_20261003/water124.doc`.
- SHA đầu vào: `f3fae17d5f680300060ea959bd352658866bf15b63747ebaf3942684d8582c67`.
- Nguồn: https://vanban.chinhphu.vn/?docid=153298&pageid=27160

## Tài liệu giữ lại nhưng chưa nạp

- `ecommerce_platform/Luật-122-2025-QH15-trích-tuyển.docx`: editorial summary; replace with original source or quarantine.
- `ecommerce_platform/Nghị-định-248-2026-NĐ-CP-trích-tuyển.docx`: editorial summary; replace with original source or quarantine.
- `electricity/Nghị-định-133-2026-NĐ-CP-trích-tuyển.docx`: editorial summary; replace with original source or quarantine.
- `electricity/Quyết-định-14-2025-QĐ-TTg-trích-tuyển.docx`: editorial summary; replace with original source or quarantine.
- `fire_safety/Nghị-định-106-2025-NĐ-CP-trích-tuyển-cập-nhật.docx`: editorial summary; replace with original source or quarantine.
- `residence/Luật-118-2025-QH15-trích-tuyển-điều-chỉnh-Luật-Cư-trú.docx`: editorial summary; replace with original source or quarantine.
- `residence/Nghị-định-154-2024-NĐ-CP-trích-tuyển-cập-nhật.docx`: editorial summary; replace with original source or quarantine.
- `residence/Thông-tư-116-2026-TT-BCA-trích-tuyển-thay-Thông-tư-53-2025.docx`: editorial summary; replace with original source or quarantine.
- `student_housing/CTU-KTX-thong-tin-2026-2027.docx`: editorial summary; replace with original source or quarantine.
- `water_cantho/215-QD-UBND-pham-vi-doi-chieu.md`: editorial summary; replace with original source or quarantine.
- `water_cantho/Quyết-định-215-QĐ-UBND.docx`: original government attachment not yet authenticated; do not claim current tariff.
- `docs/legal_agent_originals_20261003/water57.pdf`: downloaded consolidated guidance; section parser not yet reviewed, not indexed as an article.

Không xóa tài liệu gốc, bản OCR hoặc bản sao lưu khi loại một nguồn khỏi kho truy xuất.
