"""Compare actual chatbot replies to the user's supplied answer reference.

Each note reports semantic matches, omissions and additions. This is not a new
model test or an assertion that every proposition in the reference is legal gold.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'eval/ragas_reports'
INPUT = OUT / 'gemini_qwen_vs_pasted_2026-10-04.json'

# Reference expectation; actual A matches/omissions; actual B matches/omissions;
# differing or additional content, evaluated as text differences only.
MATCHES = {
    1: ('Checklist sáu nhóm: chủ thể, giá/thanh toán, cọc, phí, bàn giao/sửa chữa, chấm dứt.', 'Không khớp nội dung đáp án: chỉ thông báo chưa tổng hợp được kết luận.', 'Khớp phần giá/thanh toán, thời hạn, quyền/nghĩa vụ ở mức chung; thiếu checklist cọc, phí, bàn giao và báo trước.', 'B thêm hiệu lực giao dịch và khối chuyển tiếp dài; chưa biến căn cứ thành lời hướng dẫn.'),
    2: ('Ghi rõ cọc, giá thuê, ngày thanh toán và không ký mẫu bỏ trống.', 'Khớp định nghĩa cọc và thời hạn/phương thức thanh toán; thiếu kết luận, mục đích/mức/hoàn cọc và cảnh báo mẫu bỏ trống.', 'Thêm được giá giao dịch so với A; vẫn thiếu kết luận và checklist cụ thể của đáp án.', 'C khẳng định bắt buộc; A/B chưa kết luận như C và dùng căn cứ khác.'),
    3: ('Kiểm tra điều khoản tăng giá; quyền khi không thỏa thuận tăng và khi bị ép rời phòng.', 'Khớp kiểm tra hợp đồng/thỏa thuận giá; thiếu cách từ chối giá mới, hoàn cọc và tình huống bị đuổi như C.', 'Chưa khớp hướng dẫn chính của C; chỉ trích trường hợp cải tạo.', 'A/B thêm ngoại lệ cải tạo và quyền chấm dứt có bồi thường; C không nêu ngoại lệ này.'),
    4: ('Hoàn cọc khi đủ nghĩa vụ; các khoản khấu trừ; ảnh/video bàn giao.', 'Khớp nguyên tắc trả/trừ cọc theo Điều 328 và xem hợp đồng; thiếu danh sách nợ/hư hỏng/báo trước và lưu ảnh.', 'Khớp căn cứ Điều 328; thiếu áp dụng khi trả phòng, danh sách khấu trừ và bằng chứng.', 'A/B thêm mất cọc, trả khoản tương đương và ngoại lệ thỏa thuận; C tập trung trả phòng.'),
    5: ('Các nhánh thời hạn/kê khai, bốn người một hộ, bậc 3 và mức giá ví dụ.', 'Khớp chủ đề giới hạn thu tiền điện; không trình bày các nhánh và con số trong C.', 'Khớp nhánh thời hạn/kê khai và bốn người một hộ; không khớp toàn bộ cách lựa chọn/giá ví dụ trong C.', 'B trích bậc 2 thay vì bậc 3 ở C, dùng Thông tư 60/2025 và thêm cảnh báo hiệu lực; khác tham chiếu, chưa tự kết luận bên nào đúng.'),
    6: ('Ba người bằng 3/4 định mức; ví dụ 37,5 kWh từng bậc và nhánh không kê khai.', 'Khớp quy tắc 3/4 khi kê khai; thiếu ví dụ 37,5 kWh và nhánh không kê khai trong C.', 'Khớp quy tắc 3/4; có nhánh không kê khai nhưng khác số bậc, thiếu ví dụ số kWh.', 'A/B thêm điều kiện hiệu lực; B nói bậc 2, C nói bậc 3.'),
    7: ('Chốt công tơ, hóa đơn gốc, căn cứ phạt, hotline/kênh phản ánh.', 'Khớp đối chiếu hóa đơn; thiếu chỉ số đầu/cuối, mức phạt và hotline.', 'Có căn cứ đối chiếu hóa đơn/định mức nhưng chưa hướng dẫn chốt công tơ, phạt và kênh phản ánh.', 'A/B thêm lưu ý hiệu lực quy định điện; chưa tái hiện quy trình bốn bước của C.'),
    8: ('Trả lời có; công khai chỉ số cũ/mới, kWh, đơn giá, thành tiền và cùng chốt công tơ.', 'Không khớp ý chính; nói kê khai cư trú/số người thay vì thông báo tiêu thụ và bảng kê.', 'Không khớp ý chính; trích quy định người thuê mà thiếu nghĩa vụ/bảng kê được C nêu.', 'C khẳng định nghĩa vụ cụ thể; A/B chưa có kết luận tương ứng.'),
    9: ('Giá do UBND ban hành; định mức 4 m³/người; khoảng giá và phần thuế/phí.', 'Khớp căn cứ địa phương, phân nhóm nhà cung cấp; thiếu định mức 4 m³ và khoảng giá của C.', 'Khớp bảng giá theo địa bàn/nhóm; thiếu định mức nước cho người thuê trong C.', 'B dùng số liệu năm 2024 và nói chưa gồm phí môi trường; C nói khoảng giá đã gồm phí.'),
    10: ('Mức khoán phổ biến/cao; yêu cầu giải trình hóa đơn chia theo người; ghi hợp đồng.', 'Khớp kiểm tra thỏa thuận/hợp đồng và hóa đơn; thiếu các mức khoán và công thức chia theo người.', 'Khớp xem thỏa thuận, số đo và hóa đơn; thiếu mức khoán, chia theo người và cách ghi cụ thể.', 'A/B chưa khẳng định thu khoán là phổ biến hay vi phạm chỉ từ số tiền; A thêm nhóm/địa bàn/kỳ hóa đơn.'),
    11: ('Hai phương án: chia hóa đơn theo người hoặc đồng hồ phụ, phân bổ hao hụt/nước chung.', 'Không khớp hai phương án; chỉ nêu nguồn không có công thức và cần xem thỏa thuận.', 'Không khớp hai phương án; cùng chỉ nêu giới hạn nguồn.', 'A/B nêu lý do chưa kết luận, không đưa ví dụ thỏa thuận như C.'),
    12: ('Lấy mã khách hàng/danh bộ, tra cứu website/cổng/Zalo của đơn vị cấp nước.', 'Chỉ khớp chủ đề kiểm tra hóa đơn/đơn vị; thiếu mã khách hàng và các bước tra cứu.', 'Chỉ khớp nhận diện nhà cung cấp/nhóm/kỳ; thiếu toàn bộ quy trình tra cứu bằng mã.', 'A/B thêm phân nhóm giá/phí; A đưa giá lịch sử và lưu ý chưa biết quy trình.'),
    13: ('Đăng ký tạm trú ngoài xã thường trú nếu ở từ 30 ngày; hạn nộp 30 ngày, tối đa hai năm.', 'Khớp điều kiện và tên thủ tục; thiếu hạn nộp và thời hạn tạm trú trong C.', 'Khớp cùng điều kiện/thủ tục; cũng thiếu hai mốc C đưa.', 'A/B chưa khẳng định hạn nộp 30 ngày kể từ chuyển đến như C.'),
    14: ('Chủ trọ phối hợp/chứng minh chỗ ở; sinh viên CCCD/CT01; mức phạt hai bên.', 'Khớp nghĩa vụ người đăng ký cung cấp thông tin và hồ sơ; thiếu việc chủ trọ phải làm, mẫu/ảnh CCCD và mức phạt.', 'Khớp tờ khai/chứng minh chỗ ở; thiếu trách nhiệm riêng chủ trọ và mức phạt.', 'A/B nêu thiếu căn cứ nghĩa vụ riêng chủ trọ; thêm nơi tiếp nhận hoặc thời gian giải quyết.'),
    15: ('CT01 có xác nhận, hợp đồng hợp pháp, CCCD; nộp trực tiếp hoặc online/VNeID.', 'Khớp tờ khai, chứng minh chỗ ở và nơi nộp; thiếu tên mẫu, xác nhận, ví dụ hợp đồng/CCCD và kênh online.', 'Khớp tờ khai/chứng minh chỗ ở/nộp hồ sơ; thiếu các chi tiết và kênh online của C.', 'A/B thêm xử lý ba ngày làm việc và ý kiến cha mẹ khi chưa thành niên; B thêm gia hạn.'),
    16: ('Đăng ký chỗ mới khi đổi xã; xóa nơi cũ; điều chỉnh khi chuyển cùng xã.', 'Không khớp các nhánh chuyển trọ; nói gia hạn/tờ khai.', 'Có hồ sơ/nộp tại nơi dự kiến tạm trú nhưng thiếu giải thích các nhánh đổi địa chỉ và nơi cũ.', 'B có cờ đầy đủ nhưng nội dung chưa khớp đáp án chuyển trọ; không dùng cờ này chấm đạt.'),
    17: ('Năm mục quan sát: lối thứ hai, cửa chuồng cọp/chìa khóa, bình, dây/CB, bãi xe.', 'Khớp nhóm lối thoát, phương tiện và điện; thiếu các dấu hiệu kiểm tra cụ thể, chìa khóa/CB và bãi xe.', 'Khớp ba nhóm lối thoát/phương tiện/điện ở mức chung; thiếu checklist chi tiết như C.', 'A/B thêm bếp, nguồn nhiệt và điều kiện nhà kết hợp kinh doanh; A có dạng khuyến nghị.'),
    18: ('Nội quy/biển, ngăn cháy, hai lối thoát, số bình, tập huấn quản lý.', 'Khớp phương tiện/lối thoát và an toàn điện chung; thiếu hầu hết yêu cầu định lượng và tập huấn của C.', 'Khớp phương tiện/lối thoát chung; thiếu nội quy/biển, số lượng cụ thể và tập huấn.', 'A/B dùng Luật 55/2024, chưa kết luận theo số phòng; B yêu cầu phân loại/tầng/diện tích.'),
    19: ('Yêu cầu mở/dọn, bố trí chìa khóa khẩn cấp và phản ánh cơ quan.', 'Chỉ khớp nguyên tắc duy trì lối thoát; thiếu ba bước hành động của C.', 'Có kiểm tra/thẩm quyền nhưng không chỉ người thuê yêu cầu mở, lấy chìa khóa hoặc gửi phản ánh ra sao.', 'B thêm trích rất dài về kiểm tra, tần suất và thẩm quyền.'),
    20: ('Chủ trọ bảo đảm điện/bình/hướng dẫn; người thuê tránh quá tải, tắt thiết bị nhiệt, sạc xe an toàn.', 'Khớp hai nhóm trách nhiệm, kiểm tra điện/sạc xe và hướng dẫn người thuê; thiếu CB, bình định kỳ và ví dụ hành vi.', 'Khớp trách nhiệm và bảo đảm điện/sạc; thiếu checklist cụ thể cho từng bên trong C.', 'A/B thêm ngoại lệ thỏa thuận trách nhiệm và điều kiện kỹ thuật sạc; A khuyên xem hợp đồng bảo trì.'),
    21: ('Danh tính/liên hệ/chứng chỉ/phí; thông tin phòng, giá, cọc, điện nước, pháp lý trung thực.', 'Khớp thông tin trung thực và phí thỏa thuận; thiếu danh mục công khai cụ thể.', 'Khớp nghĩa vụ thông tin trung thực; thiếu danh tính/liên hệ/chứng chỉ/phí và chi tiết phòng.', 'B thêm đào tạo, thuế, báo cáo và bồi thường; A chưa kết luận trường hợp cá nhân độc lập.'),
    22: ('Không cọc trước xem phòng; xác minh chủ/ủy quyền; người nhận tiền và phí môi giới.', 'Khớp xác minh ủy quyền/tư cách người cho thuê; thiếu xem trực tiếp, không cọc trước và ai chịu phí.', 'Chưa khớp checklist; chỉ trích nhà cho thuê không bắt buộc có Giấy chứng nhận.', 'A/B thêm quy định không bắt buộc Giấy chứng nhận; C yêu cầu ký/trả trực tiếp chủ nhà.'),
    23: ('Từ chối thuê/phí, yêu cầu hoàn phí xem phòng và báo nền tảng/công an khi có dấu hiệu.', 'Khớp nghĩa vụ trung thực; thiếu các quyền và kênh hành động cụ thể trong C.', 'Khớp nghĩa vụ trung thực; chưa hướng dẫn từ chối, hoàn phí hoặc báo cáo.', 'A/B thêm bồi thường do lỗi; A yêu cầu xem hợp đồng và chưa có căn cứ hủy/đòi cọc.'),
    24: ('Hợp đồng/phiếu thu ký hai bên, mức phí, điều kiện phát sinh/hoàn phí.', 'Chỉ khớp phí theo thỏa thuận; thiếu giấy tờ, thành phần và điều kiện.', 'Chỉ khớp quyền thu phí theo thỏa thuận; thiếu mọi mục giấy tờ cụ thể của C.', 'B thêm các quyền doanh nghiệp khác; chưa phải mẫu thỏa thuận cho người thuê.'),
    25: ('Lịch sử/xác thực tài khoản, tìm ngược ảnh, cảnh giác giá rẻ bất thường.', 'Khớp kiểm tra danh tính/liên hệ/xác thực; thiếu lịch sử, tìm ảnh và giá bất thường.', 'Có xác thực/danh tính ở góc nghĩa vụ nền tảng; thiếu các thao tác kiểm tra ảnh/tài khoản/giá.', 'A/B thêm cảnh báo link, OTP và nghĩa vụ nền tảng; không nêu tỷ lệ 99% như C.'),
    26: ('Nút Report, chọn lý do và đính kèm ảnh/tin nhắn bằng chứng.', 'Khớp báo qua kênh công khai; thiếu nút/lý do/bằng chứng trong C.', 'Chỉ khớp nền tảng cần có quy trình phản ánh; chưa chỉ các thao tác báo tin.', 'A nói chưa có dữ liệu về giao diện cụ thể; không giả định luôn có nút Report.'),
    27: ('Định danh người đăng, cơ chế khiếu nại/gỡ tin và cung cấp thông tin cho công an.', 'Khớp xác thực/công khai thông tin, kiểm soát nội dung và phản ánh; thiếu gỡ ngay và cung cấp thông tin điều tra.', 'Khớp cùng các nhóm nghĩa vụ; thiếu hai yêu cầu cụ thể còn lại của C.', 'A/B dùng bộ văn bản 2025/2026 và điều kiện nền tảng trung gian; B thêm nhánh đặt hàng.'),
    28: ('Link giả/rút gọn, đòi thông tin ngân hàng/OTP, thúc ép; không nhấp/không cung cấp.', 'Khớp không truy cập link lạ, không cung cấp tài khoản/mật khẩu/OTP; thiếu ví dụ link giả và thúc ép.', 'Khớp quy tắc tránh link/OTP; thiếu các ví dụ và áp lực thời gian trong C.', 'A/B thêm QR, cài app, xem phòng, ngừng giao dịch, liên hệ ngân hàng/lưu chứng cứ.'),
    29: ('Danh sách dữ liệu cơ bản cần thiết và những thông tin không nên yêu cầu.', 'Chỉ khớp liên hệ hồ sơ cư trú và đồng ý xử lý; thiếu hai danh sách trong C.', 'Chỉ trích sự đồng ý; không trả lời loại thông tin nào như C.', 'A/B dùng nguyên tắc xử lý dữ liệu; chưa phân loại theo mục đích hợp đồng/cư trú.'),
    30: ('Mục đích thông báo, bảo mật/không chuyển trái phép; watermark CCCD.', 'Không khớp nội dung: chỉ trả mẫu chưa tổng hợp được kết luận.', 'Khớp mục đích/phạm vi và thông tin khi đồng ý; thiếu bảo mật, chuyển giao và mẹo watermark.', 'B dùng Luật 91/2025 thay căn cứ C; không có hướng dẫn lưu/xóa cụ thể.'),
    31: ('Không đăng CCCD/điện thoại để đòi nợ; quyền riêng tư, phạt/bồi thường.', 'Khớp giới hạn công khai cần đồng ý; thiếu kết luận vào hành vi chủ trọ, mức phạt và bồi thường.', 'Khớp kiểm soát công khai/đúng mục đích; thiếu kết luận tình huống, phạt và bồi thường.', 'A/B trả lời có điều kiện; B có thêm trường hợp được công khai, khác câu cấm tuyệt đối ở C.'),
    32: ('Yêu cầu gỡ bằng văn bản, lưu bằng chứng, gửi cơ quan xử lý.', 'Khớp quyền yêu cầu xóa; thiếu cách gửi, ảnh/vi bằng và nơi phản ánh.', 'Khớp yêu cầu xóa/ngừng/bảo vệ dữ liệu; thiếu các bước bằng chứng và kênh xử lý như C.', 'A/B thêm thủ tục/thời hạn; B phân biệt loại yêu cầu, không nói gỡ ngay vô điều kiện.'),
    33: ('Nhận diện cớ cọc trước, địa chỉ/ảnh mập mờ, tài khoản ảo/từ chối gặp; không chuyển trước xem.', 'Khớp cọc trước/chưa kiểm chứng, xem phòng/xác minh và không chuyển; thiếu ba ví dụ dấu hiệu chi tiết.', 'Khớp xem phòng/xác minh/không chuyển trước kiểm chứng; thiếu ví dụ địa chỉ/ảnh/tài khoản.', 'A thêm Điều 174 và lưu chứng cứ/trình báo; B cũng thêm lưu chứng cứ/trình báo.'),
    34: ('Chi tiết giao dịch, chat, tài khoản/link/tin đăng; công an và liên hệ ngân hàng.', 'Khớp chứng từ, tin nhắn và công an; thiếu chi tiết tài khoản/link/tin đăng và liên hệ ngân hàng.', 'Khớp chứng từ/chat/cơ quan tiếp nhận; thiếu các trường cụ thể và bước ngân hàng.', 'A/B thêm Viện kiểm sát, thủ tục tiếp nhận và hình thức gửi; không chỉ đơn vị Cần Thơ cụ thể như C.'),
    35: ('Phân biệt tranh chấp hợp đồng có phòng thật với gian dối từ đầu/chiếm đoạt; nơi giải quyết.', 'Chưa khớp phép phân biệt; chỉ định nghĩa cọc và khuyến cáo phòng ngừa.', 'Khớp dấu hiệu gian dối chiếm đoạt ở Điều 174; thiếu so sánh với tranh chấp nghĩa vụ và nơi giải quyết.', 'B thêm ngưỡng/điều kiện hình sự; chưa giải thích tình huống phòng thật/ảo như C.'),
    36: ('Đơn chung, danh sách từng nạn nhân/số tiền, giao dịch chung và hội thoại; nơi nhận.', 'Khớp lưu tài liệu/chat/chứng từ và trình báo; thiếu danh sách từng người/giao dịch/kịch bản chung.', 'Khớp cùng chứng cứ/trình báo, thêm cơ quan tiếp nhận; thiếu tổng hợp vụ nhiều nạn nhân.', 'A/B không khẳng định nhiều nạn nhân tự thành chuyên nghiệp/nặng hơn hoặc chắc chắn khởi tố như C.'),
}


def main():
    before = hashlib.sha256(INPUT.read_bytes()).hexdigest()
    data = json.loads(INPUT.read_text(encoding='utf-8'))
    assert len(data['cases']) == len(MATCHES) == 36
    for row in data['cases']:
        expected, a, b, differences = MATCHES[row['id']]
        row['reference_comparison'] = {'reference_expected': expected, 'chatbot_a_match_and_missing': a,
                                      'chatbot_b_match_and_missing': b, 'additional_or_different': differences}
    data['method'] = 'Manual semantic match/omission/addition comparison: user answers are reference C; A/B are actual saved chatbot replies. No new generation or numerical correctness scoring.'
    data['primary_comparison'] = 'C versus A and C versus B, question by question'
    data['previous_practical_coverage_labels'] = data.pop('coverage_counts')
    out_json = OUT / 'chatbot_vs_reference_36_2026-10-04.json'
    out_md = OUT / 'chatbot_vs_reference_36_2026-10-04.md'
    out_json.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    lines = ['# Câu trả lời chatbot so với bộ đáp án bạn cung cấp — 36 câu', '',
             '**Bộ bạn gửi là đáp án tham chiếu C. A và B là hai cấu hình chatbot hệ thống trả lời cùng bộ câu hỏi.** Bảng dưới đối chiếu C→A và C→B theo ý nghĩa: khớp gì, thiếu gì, khác/thêm gì. Đây không phải so khả năng mô hình tách khỏi chatbot.', '',
             '- A: phản hồi thực tế đã lưu của chatbot Gemini-only trên kho public.',
             '- B: phản hồi thực tế đã lưu của chatbot Gemini phân tích + Qwen chọn đoạn nguồn trên cùng kho public.',
             '- C: nguyên văn 36 đáp án bạn gửi; giữ nguyên làm tham chiếu đối chiếu nội dung.',
             '- Không chạy lại hai cấu hình trong lượt này. Đã đọc 72 phản hồi thực tế và 36 đáp án tham chiếu, ghép theo câu hỏi; câu 27 khác một cụm nhưng cùng ý.', '',
             '## Kết quả đối chiếu', '',
             'Chatbot hiện chưa trả lời chi tiết như đáp án tham chiếu ở nhiều câu. A thường diễn giải dễ đọc; B đưa nhiều căn cứ hơn nhưng phần lớn vẫn trích văn bản. Phần còn thiếu thường là checklist/bước hành động, ví dụ tính toán, trường thông tin cần thu thập và hướng dẫn theo tình huống.', '',
             '- Câu 1 và 30: A chỉ trả mẫu chưa kết luận. B có căn cứ, chưa đủ nội dung của đáp án tham chiếu.',
             '- Câu 8, 11, 16, 19, 24, 29: phản hồi chưa tái hiện được ý trả lời chính mà C đưa ra.',
             '- Câu 6, 13, 15, 28, 33, 34: có các ý trùng rõ, vẫn thiếu ví dụ/chi tiết/bước thực hiện trong C.',
             '- Câu 5–6, 9, 31: có khác biệt nội dung quan trọng, không chỉ khác cách viết; xem cột cuối.', '',
             'Không dùng cờ “đầy đủ” hoặc điểm Faithfulness để kết luận chatbot khớp đáp án C. Các nhãn bao phủ yêu cầu thực hành 0–2 ở báo cáo trước là một tiêu chí khác, không phải điểm khớp reference/Answer Correctness.', '',
             '## So trực tiếp từng câu', '', '| Câu | Ý trong đáp án C | Chatbot A: khớp / thiếu | Chatbot B: khớp / thiếu | Nội dung khác hoặc thêm |', '|---|---|---|---|---|']
    def cell(value):
        return value.replace('|', '\\|').replace('\n', ' ')
    for row in data['cases']:
        c = row['reference_comparison']
        lines.append('| ' + ' | '.join([str(row['id'])] + [cell(c[k]) for k in ('reference_expected', 'chatbot_a_match_and_missing', 'chatbot_b_match_and_missing', 'additional_or_different')]) + ' |')
    lines += ['', '## Đọc nguyên văn và giới hạn', '',
              '[Nguyên văn ba đáp án cho từng câu](gemini_qwen_vs_pasted_2026-10-04_details.md) · [JSON: đủ 108 đáp án và nhận xét reference](chatbot_vs_reference_36_2026-10-04.json)', '',
              'Các đối chiếu trên coi C là văn bản tham chiếu do bạn cung cấp, không tự động coi mỗi mệnh đề là đúng pháp luật. “Thiếu so với C” là nhận xét về nội dung; chatbot khác C chưa tự chứng minh chatbot sai. Việc kiểm tra căn cứ/hiệu lực nằm riêng trong [báo cáo rà tham chiếu](gemini_qwen_vs_pasted_2026-10-04.md). Không có điểm phần trăm khớp hay điểm đúng pháp luật mới trong báo cáo này.', '',
              'Nếu mục tiêu là chatbot trả lời theo độ chi tiết của C, cần bổ sung lớp diễn giải tình huống/checklist sau chọn nguồn và kiểm chứng. Câu trả lời hiện tại của B chưa có lớp này. Đây là hướng cải thiện từ đối chiếu, chưa triển khai hoặc chạy thử.', '',
              f'SHA-256 hồ sơ đầu vào: `{before}`. Các lượt sinh gốc và bộ tham chiếu được giữ nguyên.', '']
    out_md.write_text('\n'.join(lines), encoding='utf-8')
    assert hashlib.sha256(INPUT.read_bytes()).hexdigest() == before
    for path, h in data['input_sha256'].items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == h
    assert set(MATCHES) == {row['id'] for row in data['cases']}
    assert all(row['reference_comparison'] for row in data['cases'])
    print('Verified: 36 reference-to-chatbot comparisons; 108 saved answers; input files unchanged.')


if __name__ == '__main__':
    main()
