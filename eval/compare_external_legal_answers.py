"""Compare the saved user answers with an existing system run, without LLM calls.

Review notes are qualitative observations of local v15, not correctness labels.
Run from the repository root. Existing evaluation/checkpoint files are read only.
"""
from __future__ import annotations

import hashlib
import json
import re
import statistics
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / 'eval/datasets/external_legal_20261004/answers.json'
SYSTEM = ROOT / 'eval/reports/legal_agent_local_v15_2026-10-04.json'
NATIVE = ROOT / 'eval/reports/legal_agent_after_v15_2026-10-04.json'
REPORT = ROOT / 'eval/reports/external_legal_comparison_2026-10-04.json'
DOC = ROOT / 'eval/ragas_reports/external_legal_comparison_2026-10-04.md'
DETAIL = ROOT / 'eval/ragas_reports/external_legal_comparison_details_2026-10-04.md'

# Each entry: observed system behavior, external-reference risk, next review step.
REVIEWS = {
    1: ('Có Điều 398 BLDS và Điều 163 về nội dung hợp đồng; thiếu checklist ngắn, trích cả điều khoản chuyển tiếp dài.', 'Mức cọc 1 tháng, hoàn 3–5 ngày và báo trước 30 ngày là ví dụ/thỏa thuận; không coi là quy tắc chung.', 'Tóm tắt các mục cần kiểm tra và tách ví dụ khỏi nghĩa vụ luật định.'),
    2: ('Có định nghĩa cọc, giá và thời hạn thanh toán; tự đánh dấu trả lời một phần.', 'Câu “bắt buộc” và dẫn Điều 472/473 chưa chứng minh mọi hợp đồng phải có tiền cọc.', 'Giải thích nghĩa vụ nội dung hợp đồng và điều khoản cọc nếu các bên có thỏa thuận.'),
    3: ('Chọn ngoại lệ cải tạo nhà tại Điều 170 khoản 2; chưa nêu nguyên tắc và cách xử lý tình huống thường gặp.', 'Kết luận luôn được tiếp tục trả giá cũ/luôn được hoàn cọc cần điều kiện, ngoại lệ và căn cứ chấm dứt.', 'Bổ sung nguyên tắc thỏa thuận, ngoại lệ và kiểm tra điều khoản tăng giá.'),
    4: ('Có Điều 328 khoản 2 và ngoại lệ thỏa thuận; thiếu áp dụng vào bàn giao, nợ và thiệt hại.', 'Từ “chỉ” trong danh sách khấu trừ và kết luận hoàn 100% đang giản lược điều kiện hợp đồng.', 'Trả lời theo mục đích cọc, việc thực hiện nghĩa vụ và chứng cứ bàn giao.'),
    5: ('Có Điều 12 khoản 5 Thông tư 60/2025; ghi rõ chưa xác nhận sự kiện kích hoạt hiệu lực.', 'Giá 2.167 đồng/kWh, VAT, sáu bậc và quyền lựa chọn cách tính chưa được xác minh theo kỳ hóa đơn.', 'Xác minh biểu giá/hiệu lực đúng kỳ trước khi đưa số tiền hoặc công thức.'),
    6: ('Dùng cùng khối trích với câu 5; chưa tính ví dụ riêng cho ba người.', '37,5 kWh và cách chia các bậc phụ thuộc biểu giá, điều kiện kê khai và văn bản áp dụng.', 'Sau khi xác minh biểu giá, trình bày công thức 3/4 và ví dụ có điều kiện.'),
    7: ('Có hướng dẫn công khai cách tính và quy định điện; thiếu quy trình đối chiếu gọn và căn cứ phạt trực tiếp trong đáp án.', 'Mức phạt 20–30 triệu, khoản/điều và hotline cần kiểm chứng; không suy ra vi phạm chỉ từ giá cao.', 'Bổ sung kiểm tra chỉ số/hóa đơn; chỉ nêu mức phạt khi đã xác minh chủ thể và hiệu lực.'),
    8: ('Có nguồn hướng dẫn Cần Thơ và cảnh báo chưa có căn cứ nghĩa vụ bắt buộc cho mọi chủ trọ.', 'Câu “có” và bảng kê bắt buộc chưa gắn điều khoản cụ thể; khuyến nghị minh bạch không tự thành nghĩa vụ luật định.', 'Tách việc nên thỏa thuận công khai khỏi nghĩa vụ pháp luật đã được chứng minh.'),
    9: ('Có Quyết định 215/2024 và giới hạn phạm vi; chưa kết luận giá hiện hành.', 'Định mức 4 m³/người và khoảng giá 7.000–11.000 chưa có nguồn/địa bàn/đơn vị cấp nước cụ thể.', 'Xác minh đơn vị cấp nước, địa bàn và kỳ hóa đơn; tránh dùng khoảng giá thiếu nguồn.'),
    10: ('Đáp án chọn kiểm định đồng hồ ở Điều 50 Nghị định 117; lệch câu hỏi thu khoán theo người.', 'Khoảng 30–50 nghìn và 80–100 nghìn chưa có khảo sát; mức cao tự nó chưa chứng minh sai quy định.', 'Ưu tiên hợp đồng thuê, mức khoán, số người và hóa đơn tổng; ghi rõ đây là tư vấn kiểm tra.'),
    11: ('Chọn hợp đồng đơn vị cấp nước–khách hàng tại Điều 44; chưa trả lời thỏa thuận chia tiền giữa người thuê.', 'Hai phương án là gợi ý thỏa thuận, chưa phải hai cách bắt buộc theo luật.', 'Bổ sung căn cứ thỏa thuận dân sự và cách minh bạch nước chung/hao hụt.'),
    12: ('Có quyền yêu cầu đơn vị cấp nước xem xét khoản thanh toán; thiếu hướng dẫn thực hành với mã khách hàng.', 'Tên website/Zalo OA và cách tra cứu cần xác minh với đúng nhà cung cấp.', 'Hướng dẫn đọc mã khách hàng/chỉ số, rồi liên hệ kênh chính thức của đơn vị trên hóa đơn.'),
    13: ('Có điều kiện ngoài xã thường trú và ở từ 30 ngày; lặp hai bản cùng điều, chưa nêu đủ quy trình.', 'Điều kiện ở từ 30 ngày trở lên không tự chứng minh thời hạn nộp hồ sơ là 30 ngày sau chuyển đến.', 'Tách điều kiện phải đăng ký, thời hạn tạm trú và thời hạn làm thủ tục có căn cứ.'),
    14: ('Có nghĩa vụ công dân/hồ sơ, ghi thiếu căn cứ nghĩa vụ riêng của chủ trọ.', 'Mức phạt theo Nghị định 144/2021 và quy trách nhiệm đồng thời hai bên cần cập nhật/xác minh.', 'Tìm nghĩa vụ trực tiếp của chủ trọ; giữ riêng trách nhiệm người đăng ký và cơ quan tiếp nhận.'),
    15: ('Có Điều 28 khoản 1/2 về hồ sơ và cơ quan tiếp nhận; cần chuyển thành checklist.', 'Bản sao CCCD, chữ ký chủ nhà trên CT01 và kênh VNeID không được mặc định bắt buộc trong mọi hồ sơ.', 'Đối chiếu thủ tục công bố hiện hành và phân biệt thông tin đã khai thác được với giấy tờ phải nộp.'),
    16: ('Có Thông tư 116/2026 về đăng ký tại chỗ mới và ngoại lệ trong xã thường trú.', 'Mốc 30 ngày, tự động xóa nơi cũ và chỉ điều chỉnh nếu cùng phường chưa được chứng minh trong bản ngoài.', 'Giải thích theo chỗ ở mới/ngoại lệ; không thêm thao tác tự động nếu thiếu căn cứ.'),
    17: ('Có Điều 20/21/24 Luật 55/2024; trích dài thay vì checklist dễ dùng khi xem phòng.', 'Lối thoát thứ hai, chìa khóa và kiểm tra bình phải phân biệt khuyến cáo với yêu cầu theo loại công trình.', 'Viết checklist quan sát thực tế, kèm điều kiện phân loại cho nghĩa vụ pháp lý.'),
    18: ('Có Luật 55/2024 và phụ lục Nghị định 105/2025; giữ trả lời một phần do cần phân loại nhà.', 'Dẫn hệ văn bản PCCC cũ; hai lối thoát và mật độ bình bị khẳng định chung khi thiếu thông tin quy mô.', 'Hỏi loại sử dụng, tầng, diện tích rồi chọn quy định phù hợp; kiểm tra hiệu lực văn bản.'),
    19: ('Có quy định hành vi khóa/chặn thoát nạn và kiểm tra; thiếu hướng dẫn hành động theo mức khẩn cấp.', 'Tên Đội PCCC quận/huyện cần cập nhật theo tổ chức địa phương, không mặc định tồn tại.', 'Đưa bước yêu cầu mở lối, lưu bằng chứng, phản ánh kênh hiện hành; phân biệt cháy đang xảy ra.'),
    20: ('Có Điều 8 phân trách nhiệm các chủ thể; thiếu diễn giải hành vi nên thực hiện.', 'CB từng phòng và các yêu cầu kỹ thuật cụ thể chưa gắn tiêu chuẩn/loại nhà trong bản ngoài.', 'Tóm tắt trách nhiệm chủ trọ/người thuê và gắn nguồn cho yêu cầu kỹ thuật.'),
    21: ('Chỉ chọn Điều 519 khoản 2 về giá dịch vụ; không trực tiếp trả lời công khai thông tin.', 'Chứng chỉ, biểu phí và cách nói hành nghề độc lập cần kiểm tra điều kiện chủ thể/điều luật.', 'Sửa lựa chọn nguồn đúng câu hỏi công khai thông tin, phân biệt người giới thiệu và người hành nghề môi giới.'),
    22: ('Có nghĩa vụ trung thực và điều kiện nhà cho thuê; thiếu checklist xác minh người có quyền nhận cọc.', 'Bắt buộc chỉ ký/trả tiền trực tiếp chủ nhà có thể bỏ qua đại diện được ủy quyền hợp pháp.', 'Hướng dẫn xác minh chủ thể hoặc đại diện, quyền nhận tiền và chứng từ giao dịch.'),
    23: ('Có nghĩa vụ thông tin và bồi thường; chưa chứng minh quyền từ chối mọi loại phí.', 'Quyền từ chối bất kỳ khoản phí và hoàn phí tự động cần hợp đồng, vi phạm và căn cứ áp dụng.', 'Nêu bước yêu cầu giải trình/khắc phục, rà hợp đồng dịch vụ và quyền khiếu nại.'),
    24: ('Có Điều 519 khoản 1/2 về phí thỏa thuận; còn thiếu hình thức giấy tờ.', 'Điều kiện chỉ trả khi ký thuê thành công và luôn hoàn tiền là nội dung cần thỏa thuận, không mặc định.', 'Bổ sung cách ghi chủ thể, mức phí, thời điểm phát sinh, hoàn phí và chứng từ.'),
    25: ('Chọn khuyến cáo mua hàng trực tuyến về OTP/link; thiếu xác minh người đăng, ảnh và phòng.', 'Con số 99% lừa đảo không có dữ liệu; tích xanh và tuổi tài khoản không bảo đảm quyền cho thuê.', 'Truy xuất khuyến cáo thuê trọ phù hợp, xác minh thực địa và tránh xác suất tự đặt.'),
    26: ('Có nghĩa vụ nền tảng trong Nghị định 248/2026; chưa đưa bước báo cáo trên giao diện.', 'Nút Report và chức năng đính kèm bằng chứng chưa được xác nhận trên nền tảng cụ thể.', 'Nêu quy trình báo cáo theo chức năng thực tế; hỗ trợ kênh liên hệ nếu thiếu nút.'),
    27: ('Có luật TMĐT 122/2025, Nghị định 248/2026; chọn cả nhánh có đặt hàng trực tuyến, vẫn thiếu căn cứ đầy đủ.', 'Dẫn Nghị định 52/85 và yêu cầu gỡ ngay cần rà chuyển tiếp, loại nền tảng và thời hạn cụ thể.', 'Kiểm tra loại nền tảng/địa vị người đăng, chọn đúng nhánh nghĩa vụ và hiệu lực.'),
    28: ('Khuyến cáo thuê trọ và trực tuyến cùng bao phủ xem phòng, liên kết lạ, OTP và bằng chứng.', 'Các dấu hiệu là cảnh báo rủi ro; không kết luận tội phạm chỉ từ liên kết rút gọn.', 'Giữ nội dung an toàn, tóm tắt thành các bước trước khi chuyển tiền.'),
    29: ('Có hồ sơ cư trú, thông tin hợp đồng và đồng ý xử lý dữ liệu theo Luật 91/2025; thiếu danh sách tối thiểu.', 'Không coi toàn bộ danh sách ngày sinh, điện thoại, giấy sinh viên là bắt buộc cho mọi hợp đồng.', 'Liệt kê thông tin cần cho từng mục đích và căn cứ xử lý, tránh thu thập dư thừa.'),
    30: ('Có mục đích/phạm vi và quyền rút đồng ý; tự ghi trả lời một phần về lưu ảnh CCCD.', 'Nghị định 13/2023 đã được văn bản mới thay thế; cấm chuyển giao khi chưa đồng ý cần xét ngoại lệ luật.', 'Bổ sung thời gian lưu, bảo mật, căn cứ xử lý và ngoại lệ; watermark là mẹo, không phải bảo đảm pháp lý.'),
    31: ('Có Điều 16 và ngoại lệ Điều 19 của Luật 91/2025; giữ trường hợp được công khai.', 'Câu “hoàn toàn không” và mức phạt 10–20 triệu quá chung; cần xác định hành vi, chủ thể và văn bản hiện hành.', 'Giải thích giới hạn công khai, xử lý trường hợp đòi nợ; không đưa mức phạt thiếu căn cứ.'),
    32: ('Có quy trình quyền chủ thể ở Điều 5 Nghị định 356 và Điều 10 Luật 91; chưa chuyển thành hướng dẫn ngắn.', 'Chỉ dẫn Sở Thông tin và Truyền thông và dùng Nghị định 13/2023 cần cập nhật cơ quan/văn bản.', 'Trình bày yêu cầu ngừng/gỡ, lưu chứng cứ, thời hạn theo đúng loại yêu cầu và kênh hiện hành.'),
    33: ('Khuyến cáo Công an phù hợp: xem phòng, xác minh chủ thể và không chuyển tiền khi chưa kiểm chứng.', 'Các dấu hiệu không đủ tự kết luận đã cấu thành tội lừa đảo.', 'Giữ khuyến cáo và tóm tắt dấu hiệu; phân biệt nguy cơ với kết luận hình sự.'),
    34: ('Có khuyến cáo lưu chứng cứ và Điều 145/146 về tiếp nhận; có thể viết rõ từng loại tài liệu.', 'Tên đơn vị PA05/Đội và nơi tiếp nhận cụ thể cần rà; không bảo đảm ngân hàng sẽ thu hồi được tiền.', 'Checklist giao dịch/tin nhắn/tài khoản/người đăng và kênh Công an hiện hành.'),
    35: ('Có định nghĩa cọc và Điều 174/175; cần giải thích ý định gian dối và tranh chấp nghĩa vụ.', 'Tòa án cấp quận/huyện là tên mô hình cũ; việc không hoàn cọc tự nó chưa quyết định dân sự/hình sự.', 'Viết tiêu chí tình huống, tránh kết luận tội; cập nhật thẩm quyền và cơ quan giải quyết.'),
    36: ('Có khuyến cáo lưu chứng cứ và tiếp nhận tố giác; thiếu cấu trúc danh sách từng nạn nhân.', 'Công an quận/huyện là chỉ dẫn cũ; nhiều nạn nhân không tự chứng minh tính chuyên nghiệp, tăng khung hay chắc chắn khởi tố.', 'Hướng dẫn tổng hợp từng giao dịch/nạn nhân và bằng chứng liên hệ; không hứa kết quả tố tụng.'),
}

CHECKED_SOURCES = [
    {'url': 'https://bocongan.gov.vn/chinh-sach-phap-luat/co-so-du-lieu-van-ban/luat-bao-ve-du-lieu-ca-nhan-1753688803', 'title': 'Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15', 'observation': 'Nguồn Bộ Công an công bố ngày có hiệu lực 01/01/2026.'},
    {'url': 'https://datafiles.chinhphu.vn/cpp/files/vbpq/2026/01/356-nd.signed.pdf', 'title': 'Nghị định 356/2025/NĐ-CP, Điều 42', 'observation': 'Bản PDF ký trên Cổng Chính phủ; bản trích dự án Điều 42 khoản 1/2 nêu hiệu lực 01/01/2026 và Nghị định 13/2023 hết hiệu lực cùng ngày. Đây không phải rà toàn bộ mọi điều của bộ đáp án.'},
    {'url': 'https://vanban.chinhphu.vn/?classid=1&docid=212483&pageid=27160', 'title': 'Luật PCCC và CNCH 55/2024/QH15', 'observation': 'Nguồn Chính phủ công bố ngày có hiệu lực 01/07/2025; bản ngoài câu 18 còn dẫn hệ nghị định trước đó, cần rà quy định áp dụng.'},
    {'url': 'https://chinhphu.vn/?classid=1&docid=214391&pageid=27160', 'title': 'Nghị quyết 81/2025/UBTVQH15', 'observation': 'Thành lập Tòa án nhân dân khu vực, hiệu lực 01/07/2025; cần cập nhật tên Tòa án cấp quận/huyện ở câu 35.'},
    {'url': 'https://bocongan.gov.vn/bai-viet/hoat-dong-cua-cong-an-cac-don-vi-dia-phuong-deu-dien-ra-on-dinh-khong-bi-gian-doan-co-ban-khong-co-vuong-mac-d2-t43825', 'title': 'Bộ Công an thông tin mô hình tổ chức mới, 05/03/2025', 'observation': 'Có hướng dẫn phân cấp khi không tổ chức Công an cấp huyện; cần cập nhật chỉ dẫn Công an quận/huyện ở câu 36 và xác minh đơn vị cụ thể ở các câu khác.'},
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    external = json.loads(DATASET.read_text(encoding='utf-8'))
    system = json.loads(SYSTEM.read_text(encoding='utf-8'))
    native_bytes = NATIVE.read_bytes()
    native = json.loads(native_bytes)
    saved = {c['id']: c for c in system['cases']}
    assert len(saved) == len(external['cases']) == len(REVIEWS) == 36
    assert set(saved) == set(REVIEWS) == set(range(1, 37))
    rows = []
    for ext in external['cases']:
        case = saved[ext['id']]
        assert case.get('answer') and not case.get('error')
        exact = ext['question'] == case['question']
        assert exact or ext['id'] == 27
        review = dict(zip(('system_observation', 'external_reference_risk', 'suggested_action'), REVIEWS[ext['id']]))
        rows.append({**ext, 'category': case['category'], 'question_match': 'exact' if exact else 'semantic_manual_review', 'question_difference': None if exact else 'Câu hệ thống có thêm cụm “người bán hoặc”; giữ nguyên hai câu, ghép theo ID và nội dung.', 'system_case': case, 'review': review})
    lengths = [len(c['system_case']['answer']) for c in rows]
    external_lengths = [len(c['external_answer']) for c in rows]
    summary = {
        'matched_cases': len(rows),
        'exact_question_matches': sum(c['question_match'] == 'exact' for c in rows),
        'semantic_question_matches': sum(c['question_match'] != 'exact' for c in rows),
        'system_partial_answers': sum(bool(c['system_case'].get('partial_answer')) for c in rows),
        'system_no_answer_flags': sum(bool(c['system_case'].get('no_answer')) for c in rows),
        'system_execution_errors': sum(bool(c['system_case'].get('error')) for c in rows),
        'native_answers_available_at_snapshot': sum(bool(c.get('answer')) for c in native['cases']),
        'system_mean_answer_characters': round(statistics.mean(lengths)),
        'external_mean_answer_characters': round(statistics.mean(external_lengths)),
        'mean_character_length_ratio': round(statistics.mean(lengths) / statistics.mean(external_lengths), 2),
        'priority_system_case_ids': [10, 11, 21, 24, 25],
        'legal_correctness_score': None,
        'answer_correctness_score': None,
        'context_recall_score': None,
    }
    payload = {
        'created_at_utc': datetime.now(timezone.utc).isoformat(),
        'method': 'Qualitative per-case comparison of saved external answers and saved local v15 outputs; no new API/LLM evaluation',
        'limitations': ['External answers are user-supplied, not independently verified ground truth.', 'Local v15 uses rules-local analysis + Qwen source selection on legal_v2. This is not a fresh test of the main production API or native Gemini pipeline.', 'Partial/no_answer flags are pipeline metadata, not an independent legal correctness score.', 'Web checks cover selected authority/commencement issues only. Other risk notes request verification rather than declare legal invalidity.'],
        'external_dataset': str(DATASET.relative_to(ROOT)),
        'external_dataset_sha256': digest(DATASET),
        'external_original_sha256': external['original_sha256'],
        'system_run': str(SYSTEM.relative_to(ROOT)),
        'system_run_sha256': digest(SYSTEM),
        'system_started_at_utc': system.get('started_at_utc'),
        'run_configuration': system.get('run_configuration'),
        'native_run': str(NATIVE.relative_to(ROOT)),
        'native_run_sha256_at_snapshot': hashlib.sha256(native_bytes).hexdigest(),
        'summary': summary,
        'selected_primary_sources_checked': CHECKED_SOURCES,
        'cases': rows,
    }
    REPORT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    lines = [
        '# Đối chiếu bộ đáp án ngoài với phản hồi hệ thống — 04/10/2026', '',
        'Đã ghép và rà đủ **36/36 câu**. Bản ngoài dễ đọc và có nhiều chỉ dẫn thực hành; bản hệ thống có nguồn/rank nhưng thường chỉ xuất trích đoạn dài. Cần sửa độ bám câu hỏi và cách diễn giải của hệ thống; không dùng bản ngoài làm chuẩn đúng/sai ngay.', '',
        '## Phạm vi và nguồn dữ liệu', '',
        '- Bộ ngoài: [bản Markdown](../datasets/external_legal_20261004/answers.md), [bản gốc](../datasets/external_legal_20261004/original.txt), [JSON](../datasets/external_legal_20261004/answers.json). Giữ nguyên nội dung người dùng gửi; trạng thái `user_supplied_unverified`.',
        '- Hệ thống: [phản hồi local v15](../reports/legal_agent_local_v15_2026-10-04.json), phân tích `rules-local`, Qwen `qwen3.5:9b`, kho `legal_v2`, chế độ `source_select`. Đây là lượt thử đã lưu, không phải chạy mới API chính.',
        f"- Lượt native v15 tại thời điểm đọc có **{summary['native_answers_available_at_snapshot']}/36 đáp án**. Không dùng lượt local thay kết quả native Gemini/RAGAS.",
        '- Ghép 35 câu trùng nguyên văn; câu 27 thêm “người bán hoặc” ở phía hệ thống, được rà và ghép theo ý nghĩa. Bản ngoài chia 8 chủ đề trình bày; hệ thống có 9 category do tách môi giới và nền tảng.',
        '- So sánh định tính từng câu; chưa chấm Answer Correctness/Context Recall hay tỷ lệ đúng pháp luật. Khác bản ngoài không đồng nghĩa hệ thống sai.', '',
        '## Kết quả quan sát', '',
        f"- Hệ thống có 36 đáp án, 0 lỗi thực thi trong snapshot; **{summary['system_partial_answers']} câu tự đánh dấu trả lời một phần**. `no_answer=True` cũng ở 23 câu này dù vẫn có nội dung; không diễn giải thành 23 phản hồi rỗng.",
        f"- Độ dài trung bình: hệ thống **{summary['system_mean_answer_characters']:,} ký tự**, bản ngoài **{summary['external_mean_answer_characters']:,} ký tự**, tỷ lệ **{summary['mean_character_length_ratio']} lần**. Đây là số ký tự, không phải thước đo đúng pháp luật.",
        '- Ưu tiên câu **10, 11, 21, 24, 25**: thu nước khoán bị thay bằng kiểm định đồng hồ; chia nước bị thay bằng hợp đồng cấp nước; công khai thông tin môi giới bị thay bằng giá dịch vụ; giấy tờ phí môi giới chưa được trả lời; xác minh người đăng bị thay bằng cảnh báo OTP chung.',
        '- Câu **5–8** chưa xác nhận điều kiện hiệu lực nguồn điện; **9/12** còn giới hạn địa bàn/nhà cung cấp; **18** cần phân loại công trình; **27** cần chọn đúng loại nền tảng. Không tăng độ chắc chắn chỉ để giống bản ngoài.',
        '- Câu **28, 33, 34, 36** có khuyến cáo phù hợp về xem phòng, OTP hoặc lưu bằng chứng; cần chuyển sang checklist gọn. Câu **31/32** đã lấy nguồn dữ liệu cá nhân mới nhưng còn trích dài.', '',
        '## Kiểm tra chọn lọc nguồn chính thức', '',
    ]
    for source in CHECKED_SOURCES:
        lines.append(f"- [{source['title']}]({source['url']}): {source['observation']}")
    lines += ['', 'Các kiểm tra này không xác nhận toàn bộ giá điện/nước, mức phạt, deadline, thuật ngữ hoặc điều kiện áp dụng trong 36 đáp án. Các điểm chưa chứng minh được ghi là cần kiểm chứng.', '', '## Bảng rà từng câu', '', '| Câu | Chủ đề | Một phần | Phản hồi hệ thống | Điểm cần rà ở bản ngoài | Bước tiếp theo |', '|---|---|---|---|---|---|']
    def cell(value: str) -> str:
        return value.replace('|', '\\|').replace('\n', ' ')
    for row in rows:
        r = row['review']
        lines.append('| ' + ' | '.join([str(row['id']), row['category'], 'Có' if row['system_case'].get('partial_answer') else 'Không', cell(r['system_observation']), cell(r['external_reference_risk']), cell(r['suggested_action'])]) + ' |')
    lines += ['', '## Hồ sơ chi tiết và tái lập', '',
        '[Mở nguyên văn hai đáp án và nguồn theo từng câu](external_legal_comparison_details_2026-10-04.md). [JSON đối chiếu](../reports/external_legal_comparison_2026-10-04.json) giữ toàn bộ system case, nguồn, context và nhận xét.', '',
        'Chạy `python eval/compare_external_legal_answers.py` từ gốc dự án để dựng lại hồ sơ từ hai bộ dữ liệu đã lưu. Script không gọi API/LLM; nhận xét được viết riêng cho local v15, không dùng chúng chấm một phiên bản khác.', '',
        'Chưa thay đáp án sinh, corpus, ground truth, checkpoint hay điểm RAGAS. Bản ngoài hiện dùng làm tài liệu so sánh về nội dung và cách trình bày; muốn dùng chấm đúng pháp luật cần rà từng mệnh đề theo nguồn/hiệu lực/điều kiện áp dụng.', '',
        f"SHA-256 bản gốc ngoài: `{external['original_sha256']}`.",
        f"SHA-256 phản hồi hệ thống: `{payload['system_run_sha256']}`.",
    ]
    DOC.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    details = ['# Nguyên văn đối chiếu 36 câu — bộ ngoài và local v15', '', 'Nội dung bên dưới được sao từ hai tệp đã lưu. Nhận xét là rà định tính, không phải chứng nhận đúng pháp luật. Xem [báo cáo tổng hợp](external_legal_comparison_2026-10-04.md) để biết phạm vi.', '']
    for row in rows:
        c = row['system_case']
        details += [f"## Câu {row['id']}: {row['question']}", '', f"Category: `{row['category']}`; partial_answer: `{c.get('partial_answer')}`; no_answer: `{c.get('no_answer')}`.", '']
        if row['question_difference']:
            details += [row['question_difference'], '', f"Câu hệ thống: {c['question']}", '']
        details += ['### Đáp án ngoài', '', row['external_answer'], '', '### Đáp án hệ thống', '', c['answer'], '', '### Nguồn hệ thống', '']
        for source in c.get('sources', []):
            details.append(f"- Rank {source.get('rank')}; chunk {source.get('chunk_id')}; {source.get('title')}; [nguồn]({source.get('source_url')})")
        details += ['', '### Nhận xét đối chiếu', '', f"- Hệ thống: {row['review']['system_observation']}", f"- Bản ngoài: {row['review']['external_reference_risk']}", f"- Tiếp theo: {row['review']['suggested_action']}", '']
    DETAIL.write_text('\n'.join(details) + '\n', encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
