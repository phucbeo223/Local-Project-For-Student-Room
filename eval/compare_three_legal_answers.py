"""Render a reviewed, three-way comparison from immutable saved answers.

Coverage is a manual assessment of the question's practical request, not legal
correctness or semantic similarity to the unverified user reference. No LLM calls.
"""
from __future__ import annotations

import hashlib
import json
import statistics
from collections import Counter
from pathlib import Path

from compare_external_legal_answers import REVIEWS

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / 'eval/datasets/external_legal_20261004/answers.json'
A = ROOT / 'eval/reports/legal_gemini38_retest_2026-10-04_fixed.json'
B = ROOT / 'eval/reports/legal_gemini_qwen_compare_2026-10-04.json'
PAIR = ROOT / 'eval/ragas_reports/gemini_vs_qwen_2026-10-04.json'
OUT = ROOT / 'eval/ragas_reports'

# score A, score B, observed A, observed B, practical comparison/gap.
# These observations were reviewed against the current A/B text, not local v15.
NOTES = {
    1: (0, 1, 'Chỉ trả mẫu chưa tổng hợp được kết luận; không có checklist.', 'Có Điều 398, một phần Điều 163; kéo theo khối chuyển tiếp rất dài.', 'B có nội dung hơn A, nhưng cả hai thiếu checklist sáu nhóm dễ dùng như bản dán.'),
    2: (1, 1, 'Có định nghĩa cọc và thời hạn/phương thức thanh toán.', 'Thêm căn cứ giá giao dịch; vẫn trích dài và thiếu kết luận trực tiếp.', 'Cả hai chưa chuyển thành các mục tiền cọc nếu có, giá thuê, ngày và cách thanh toán.'),
    3: (2, 1, 'Diễn giải thỏa thuận giá, kiểm tra hợp đồng và ngoại lệ cải tạo.', 'Chỉ chọn ngoại lệ cải tạo nhà; thiếu nguyên tắc chung.', 'A trả lời trọng tâm rõ hơn. Không lấy kết luận tuyệt đối trong bản dán làm chuẩn.'),
    4: (1, 1, 'Giải thích Điều 328 và ngoại lệ thỏa thuận; khuyên kiểm tra hợp đồng.', 'Trích Điều 328 khoản 1/2 và ngoại lệ thỏa thuận.', 'Cả hai thiếu checklist bàn giao, chứng cứ nợ/hư hỏng và thời điểm hoàn cọc; A dễ đọc hơn.'),
    5: (1, 1, 'Trích giới hạn tổng tiền thu so với hóa đơn, kèm điều kiện hiệu lực.', 'Có nhiều nhánh kê khai/định mức; cảnh báo chưa xác nhận sự kiện hiệu lực.', 'B rộng hơn nhưng dài; cả hai chưa xác định biểu giá và quy định áp dụng đúng kỳ.'),
    6: (2, 2, 'Nêu ba người bằng 3/4 định mức nếu kê khai đủ, kèm điều kiện hiệu lực.', 'Có cùng quy tắc 3/4 trong trích đoạn dài.', 'Cùng bao phủ nguyên tắc định mức; A gọn hơn. Chưa có phép tính tiền theo biểu giá đã xác minh.'),
    7: (1, 1, 'Hướng dẫn đối chiếu hóa đơn và định mức, có lưu ý hiệu lực.', 'Trích quy định điện và ghi chú hiệu lực, chưa thành quy trình kiểm tra.', 'A dễ thực hiện hơn; cả hai thiếu checklist chỉ số đầu/cuối, kWh và căn cứ xử lý hiện hành.'),
    8: (0, 0, 'Chọn kê khai số người và quyền bên bán điện yêu cầu thông tin cư trú.', 'Trích rộng quy định người thuê, vẫn không trả lời nghĩa vụ thông báo số điện từng phòng.', 'Chưa trả lời đúng trọng tâm; không tự suy ra nghĩa vụ bảng kê bắt buộc từ nguồn này.'),
    9: (1, 1, 'Nêu phân nhóm theo đơn vị, địa bàn; không khẳng định giá trọ cụ thể.', 'Có bảng giá năm 2024 với phạm vi và phần phí chưa gồm.', 'B có số liệu nguồn rõ hơn; cả hai chưa xác nhận giá hiện hành cho đúng nhà cung cấp/phòng trọ.'),
    10: (2, 1, 'Khuyên kiểm tra thỏa thuận, số đo, hóa đơn, đơn vị và kỳ sử dụng.', 'Trích ghi chú giới hạn và yêu cầu xem thỏa thuận/số đo/hóa đơn.', 'A gần cách hướng dẫn thực hành của bản dán hơn; không lặp các mức khoán thiếu khảo sát.'),
    11: (0, 0, 'Nêu biểu giá không quy định công thức chia nước; yêu cầu xem hợp đồng.', 'Cũng chỉ nêu giới hạn nguồn, không đề xuất cách chia.', 'Cả hai thiếu lựa chọn thỏa thuận theo người hoặc đồng hồ phụ, cùng cách chia hao hụt/nước chung.'),
    12: (1, 1, 'Nêu đơn vị, nhóm, khu vực, kỳ; có giá lịch sử và giới hạn chưa có quy trình.', 'Chỉ trích các thuộc tính cần xác định trên hóa đơn.', 'Cả hai thiếu mã khách hàng, chỉ số và cách liên hệ đúng nhà cung cấp; cờ đầy đủ của B chưa chứng minh đủ bước.'),
    13: (1, 1, 'Có điều kiện đăng ký tạm trú ngoài xã thường trú, ở từ 30 ngày.', 'Có cùng điều kiện.', 'Cùng thiếu hướng dẫn hồ sơ/nơi nộp trong câu này; không đồng nhất điều kiện ở 30 ngày với hạn nộp 30 ngày.'),
    14: (1, 1, 'Nêu nghĩa vụ công dân, hồ sơ và thiếu nguồn riêng về chủ trọ.', 'Trích hồ sơ và tiếp nhận; cũng thừa nhận thiếu căn cứ nghĩa vụ chủ trọ.', 'A diễn giải rõ hơn; cả hai chưa giải quyết đầy đủ phần chủ nhà cần phối hợp/cung cấp giấy tờ gì.'),
    15: (2, 2, 'Checklist tờ khai, chứng minh chỗ ở, nơi nộp và thời gian xử lý.', 'Có cùng hồ sơ/thủ tục, thêm đoạn gia hạn không cần cho câu hỏi.', 'Cả hai bao phủ hồ sơ cốt lõi; A dễ dùng hơn. Các yêu cầu CCCD/CT01/kênh online của bản dán cần rà thủ tục hiện hành.'),
    16: (0, 0, 'Chọn gia hạn và tờ khai; không nói rõ thủ tục khi đổi chỗ ở.', 'Có hồ sơ/nộp mới nhưng không giải thích thay đổi địa chỉ và nơi cũ.', 'Cả hai chưa trả lời tình huống chuyển trọ. B được gắn đầy đủ dù thiếu ý cốt lõi.'),
    17: (2, 2, 'Checklist lối thoát, phương tiện, điện/bếp; có điều kiện loại nhà.', 'Có các điều kiện tương ứng từ Luật 55/2024, ở dạng trích dài.', 'Bao phủ nhóm kiểm tra chính; A dễ dùng hơn, bản dán cụ thể hơn nhưng các yêu cầu kỹ thuật cần phân loại.'),
    18: (1, 1, 'Nêu điều kiện chung và thiếu căn cứ riêng cho nhà trọ nhiều phòng.', 'Có điều kiện chung, yêu cầu biết loại sử dụng, tầng và diện tích.', 'Cả hai giữ đúng giới hạn dữ kiện nhưng chưa thành checklist áp dụng cho công trình cụ thể.'),
    19: (0, 0, 'Trích duy trì lối thoát và nội dung kiểm tra.', 'Trích kiểm tra/thẩm quyền rất dài.', 'Cả hai thiếu bước yêu cầu mở/dọn, lưu bằng chứng và kênh phản ánh; bản dán có hành động nhưng tên cơ quan cần cập nhật.'),
    20: (2, 2, 'Chia trách nhiệm người cho thuê/người thuê, an toàn điện và kiểm tra hợp đồng.', 'Có cùng nhóm trách nhiệm và điều kiện điện/sạc xe.', 'Cả hai bao phủ trọng tâm; A diễn giải rõ hơn, chưa thành checklist hành vi cụ thể như bản dán.'),
    21: (1, 1, 'Nêu nghĩa vụ thông tin trung thực và phí thỏa thuận, thiếu danh mục công khai.', 'Chỉ trích nghĩa vụ doanh nghiệp, có nhiều nội dung không liên quan người thuê.', 'Cả hai thiếu checklist chủ thể/liên hệ, quyền môi giới, thông tin phòng và điều kiện phí.'),
    22: (1, 0, 'Khuyên kiểm tra ủy quyền/hợp đồng dịch vụ, tư cách người cho thuê.', 'Chỉ chọn các trường hợp không bắt buộc có Giấy chứng nhận.', 'A sát yêu cầu xác minh hơn; B bỏ mất quyền nhận cọc/thông tin phòng. Cả hai thiếu checklist trước khi chuyển tiền.'),
    23: (1, 1, 'Nêu trung thực, bồi thường do lỗi và xem hợp đồng; chưa có căn cứ hủy/đòi cọc.', 'Trích nghĩa vụ trung thực/bồi thường, không đưa bước xử lý.', 'Cả hai có quyền liên quan nhưng thiếu ghi nhận chênh lệch, yêu cầu giải trình/khắc phục và rà điều kiện phí.'),
    24: (0, 0, 'Có quyền thu phí theo thỏa thuận; chưa nói nội dung giấy tờ.', 'Trích quyền thu phí cùng các quyền khác; chưa có mẫu/thành phần thỏa thuận.', 'Cả hai thiếu chủ thể, dịch vụ, mức phí, điều kiện phát sinh/hoàn phí và biên nhận.'),
    25: (1, 1, 'Có kiểm tra danh tính/liên hệ/xác thực nền tảng và cảnh báo OTP.', 'Có nghĩa vụ nền tảng và cảnh báo trực tuyến, ở dạng trích rộng.', 'Cả hai thiếu đối chiếu phòng thật/ảnh/quyền cho thuê; bản dán có nhiều mẹo hơn nhưng tỷ lệ 99% không có chứng cứ.'),
    26: (1, 1, 'Hướng dẫn dùng kênh công khai, thừa nhận chưa biết nút/biểu mẫu/email cụ thể.', 'Chỉ trích yêu cầu có quy trình phản ánh công khai.', 'A dễ thực hiện hơn; cả hai thiếu checklist bằng chứng và quy trình trên nền tảng cụ thể.'),
    27: (2, 2, 'Nêu xác thực, công khai thông tin, kiểm soát nội dung và khiếu nại có điều kiện phân loại.', 'Có cùng nghĩa vụ, thêm phân biệt có chức năng đặt hàng.', 'Cả hai bao phủ nhóm trách nhiệm chính theo nguồn lưu; B rộng hơn nhưng chưa chứng minh phân loại sản phẩm cụ thể.'),
    28: (2, 2, 'Cảnh báo link/QR/OTP, xem phòng/xác minh và bước khi nghi lừa đảo.', 'Trích đủ hai khuyến cáo tương ứng.', 'Cả hai gần nội dung an toàn của bản dán; A dễ đọc hơn, không tự kết luận tội từ một dấu hiệu.'),
    29: (0, 0, 'Có một mục tờ khai cư trú và nguyên tắc đồng ý.', 'Chỉ chọn nguyên tắc đồng ý.', 'Cả hai chưa liệt kê dữ liệu tối thiểu cho hợp đồng/cư trú theo từng mục đích.'),
    30: (0, 1, 'Chỉ trả mẫu chưa tổng hợp được kết luận.', 'Có giới hạn mục đích/phạm vi và thông tin khi đồng ý xử lý.', 'B có nội dung hơn; vẫn thiếu lưu bao lâu, ai truy cập, bảo mật/xóa và căn cứ ngoại lệ.'),
    31: (1, 1, 'Có công khai khi đồng ý và hình thức công khai, thiếu ngoại lệ khác.', 'Có đầy đủ hơn các trường hợp được công khai và nguyên tắc mục đích.', 'B rộng hơn A; cả hai chưa áp dụng trực tiếp vào việc chủ trọ đăng CCCD/điện thoại trong tình huống cụ thể.'),
    32: (1, 1, 'Có thủ tục/thời hạn yêu cầu xóa và gia hạn.', 'Thêm rút đồng ý/ngừng xử lý và yêu cầu bảo vệ dữ liệu.', 'B có nhiều lựa chọn hơn nhưng vẫn thiếu cách gửi yêu cầu, bằng chứng và hướng dẫn khi bên nhận không xử lý.'),
    33: (2, 2, 'Có dấu hiệu cọc trước/chưa kiểm chứng, xem phòng/xác minh, lưu bằng chứng.', 'Có cùng khuyến cáo xem phòng/xác minh và trình báo.', 'Cả hai gần lời khuyên an toàn của bản dán; A tóm tắt dễ dùng hơn.'),
    34: (2, 2, 'Có loại chứng cứ, cơ quan tiếp nhận và hình thức gửi.', 'Có cùng khuyến cáo và quy định tiếp nhận ở dạng trích nguyên.', 'Cả hai bao phủ trọng tâm; cần thêm tài khoản/link người đăng và kênh cụ thể đã xác minh nếu muốn chi tiết như bản dán.'),
    35: (0, 1, 'Chỉ có định nghĩa cọc và khuyến cáo thuê trọ; chưa phân biệt hai trường hợp.', 'Có định nghĩa cọc và Điều 174 về gian dối chiếm đoạt.', 'B có thêm căn cứ nhưng chưa giải thích tiêu chí dân sự/hình sự; bản dán làm phần phân biệt rõ hơn.'),
    36: (1, 1, 'Có lưu bằng chứng và tiếp nhận tố giác chung.', 'Thêm cơ quan tiếp nhận và hình thức gửi, vẫn là hướng dẫn chung.', 'Cả hai thiếu danh sách từng nạn nhân, từng giao dịch và liên hệ chung; không lặp lời hứa chắc chắn khởi tố của bản dán.'),
}

SOURCES = [
    ('Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15', 'https://vanban.bocongan.gov.vn/co-so-du-lieu-van-ban/luat-bao-ve-du-lieu-ca-nhan-1753688803', 'Nguồn Bộ Công an xác nhận hiệu lực 01/01/2026; nhóm câu 29–32 phải rà theo khung hiện hành.'),
    ('Nghị định 356/2025/NĐ-CP', 'https://datafiles.chinhphu.vn/cpp/files/vbpq/2026/01/356-nd.signed.pdf', 'Bản ký chính thức. Danh mục văn bản của cơ quan Cà Mau bên dưới xác nhận Nghị định 13/2023 hết hiệu lực từ 01/01/2026.'),
    ('Danh mục văn bản tháng 12/2025, mục 45', 'https://files-vnportal.camau.gov.vn/gov-cmu/2649/FileQuanTriTinTuc/danh-muc-nd-qd-thang-12-2025.signed.signed.signed-1-639040686316440730.pdf', 'Xác nhận hiệu lực của Nghị định 356/2025 và việc Nghị định 13/2023 hết hiệu lực. Đây là kiểm tra hiệu lực, không xác minh mọi mức phạt/ngoại lệ của bộ đáp án.'),
    ('Luật PCCC và CNCH 55/2024/QH15', 'https://vanban.chinhphu.vn/?classid=1&docid=212483&pageid=27160', 'Cổng Chính phủ xác nhận hiệu lực 01/07/2025; câu 18 không thể chỉ dẫn hệ văn bản cũ mà thiếu rà phạm vi/chuyển tiếp.'),
    ('Nghị quyết 81/2025/UBTVQH15', 'https://chinhphu.vn/?classid=1&docid=214391&pageid=27160', 'Thành lập Tòa án nhân dân khu vực, hiệu lực 01/07/2025; tên Tòa án quận/huyện trong câu 35 cần cập nhật.'),
    ('Bộ Công an: hướng dẫn tố giác từ 01/03/2025', 'https://www.bocongan.gov.vn/bai-viet/huong-dan-to-giac-bao-tin-ve-toi-pham-kien-nghi-khoi-to-tu-ngay-0132025-d2-t43729', 'Công an địa phương tổ chức theo cấp tỉnh/cấp xã; chỉ dẫn Công an quận/huyện trong câu 36 đã cũ.'),
]


def digest(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> None:
    paths = [REF, A, B, PAIR]
    initial_hashes = {str(p.relative_to(ROOT)): digest(p) for p in paths}
    ref, a, b, pair = [json.loads(p.read_text(encoding='utf-8')) for p in paths]
    assert digest(A) == pair['baseline_sha256']
    assert digest(B) == pair['hybrid_sha256']
    assert ref['original_sha256'] == '00f1e2b80f35eb88b8818a622a7a4cec4e41b09c16ae8d5b3a4a1c7a93640c71'
    maps = [{c['id']: c for c in d['cases']} for d in (ref, a, b)]
    assert all(set(m) == set(NOTES) == set(range(1, 37)) for m in maps)
    rows = []
    for i in range(1, 37):
        r, x, y = [m[i] for m in maps]
        assert x['question'] == y['question'] and x['answer'] and y['answer']
        assert not x.get('error') and not y.get('error')
        assert r['question'] == x['question'] or i == 27
        sa, sb, oa, ob, gap = NOTES[i]
        rows.append({'id': i, 'question': r['question'], 'system_question': x['question'],
                     'question_match': 'exact' if r['question'] == x['question'] else 'semantic_review',
                     'reference_answer': r['external_answer'], 'gemini_case': x, 'hybrid_case': y,
                     'review': {'practical_coverage_a': sa, 'practical_coverage_b': sb,
                                'observation_a': oa, 'observation_b': ob, 'comparison': gap,
                                'reference_risk': REVIEWS[i][1]}})
    counts = {label: dict(sorted(Counter(row['review'][f'practical_coverage_{label}'] for row in rows).items())) for label in ('a', 'b')}
    lengths = {label: statistics.median(len(c[key]) for c in data['cases']) for label, data, key in [('reference', ref, 'external_answer'), ('a', a, 'answer'), ('b', b, 'answer')]}
    payload = {'review_date': '2026-10-04', 'method': 'Manual practical-request coverage review of saved 36-case A/B outputs against user-supplied reference; no new model generation or RAGAS scoring.',
               'coverage_rubric': {'0': 'Thiếu ý trả lời trực tiếp cho yêu cầu thực hành cốt lõi; có thể vẫn có nguồn liên quan.', '1': 'Có một phần ý cốt lõi, còn thiếu hướng dẫn/điều kiện/bước áp dụng đáng kể.', '2': 'Bao phủ yêu cầu chính; có thể còn thiếu chi tiết hoặc trình bày dài. Không có nghĩa đúng toàn bộ pháp luật.'},
               'reference_status': 'user_supplied_unverified', 'original_attachment_sha256': ref['original_sha256'],
               'input_sha256': initial_hashes, 'coverage_counts': counts, 'median_characters': lengths,
               'previous_context_based_metrics': pair['paired_metrics'], 'checked_sources': SOURCES,
               'limitations': ['Manual coverage labels are one-reviewer qualitative observations, not an independent gold test or percentage legal accuracy.', 'Reference risks from the earlier review are reused only as verification warnings; no local-v15 output observations are reused.', 'Selected official-source checks establish specific authority/date issues; the other 36-case legal propositions are not fully verified.', 'Pipeline full/partial flags, source faithfulness and practical completeness measure different things.', 'A/B are saved public-corpus runs; no new reference-based RAGAS score, no re-generation, no deployed pipeline change.'],
               'cases': rows}
    out_json = OUT / 'gemini_qwen_vs_pasted_2026-10-04.json'
    out_md = OUT / 'gemini_qwen_vs_pasted_2026-10-04.md'
    out_details = OUT / 'gemini_qwen_vs_pasted_2026-10-04_details.md'
    out_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    md = ['# Đối chiếu Gemini, Gemini + Qwen và 36 đáp án bạn dán', '',
          'Đã rà đủ **36 câu / 108 đáp án** từ ba bộ dữ liệu. Bản bạn dán tốt hơn về checklist và hướng dẫn hành động. Gemini thường diễn giải dễ đọc hơn Qwen; Gemini + Qwen bám nguồn tốt hơn nhưng hiện chủ yếu xuất trích đoạn. Cả hai chưa đạt mức hướng dẫn thực hành của bản dán ở nhiều câu.', '',
          '## Phạm vi', '',
          '- A: lượt Gemini-only đã hoàn tất, kho `public`; không dùng lượt local v15 làm kết quả A.',
          '- B: Gemini phân tích câu hỏi + Qwen3.5:9b chọn đoạn nguồn (`source_select`); code xuất trích dẫn. B chưa có bước Gemini viết lại câu trả lời và kiểm chứng ngữ nghĩa sau đó cho đầu ra trích nguyên văn.',
          '- C: nguyên văn bộ bạn dán; SHA-256 trùng bản đã lưu. Ghép 35 câu nguyên văn, câu 27 ghép cùng ý do phía hệ thống thêm “người bán hoặc”.',
          '- Đối chiếu nội dung đã sinh; không chạy lại mô hình, thay corpus hoặc chấm RAGAS theo C. C chưa là đáp án đúng pháp luật độc lập.', '',
          '## Số liệu và cách hiểu', '',
          '| Tiêu chí | A: Gemini | B: Gemini + Qwen | C: bản dán |',
          '|---|---:|---:|---|',
          '| Faithfulness trên cùng 33 câu | 0,771 | 0,962 | Chưa chấm với context |',
          '| Answer Relevancy, 36 câu | 0,725 | 0,721 | Chưa chấm cùng cách |',
          '| Độ trễ p50 | 18,2 giây | 30,7 giây | Không có dữ liệu chạy |',
          f'| Ký tự trung vị/đáp án | {lengths["a"]:g} | {lengths["b"]:g} | {lengths["reference"]:g} |',
          '| Cờ hệ thống “đầy đủ” | 12/36 | 15/36 | Không có cờ tương đương |', '',
          'Faithfulness đo mức bám nguồn đã đưa vào context, không đo đúng pháp luật hay mức giống C. B thiếu điểm Faithfulness ở câu 6–8 sau một lần thử lại. Cờ đầy đủ không là nhãn chất lượng: B câu 16 vẫn chưa giải thích chuyển chỗ ở, câu 36 vẫn thiếu bảng từng nạn nhân.', '',
          'Rà **độ bao phủ yêu cầu thực hành** bằng tay: 0 = thiếu ý trả lời trực tiếp; 1 = một phần; 2 = bao phủ yêu cầu chính. Nhãn xét yêu cầu câu hỏi và các ý hữu ích trong C, bỏ các khẳng định chưa xác minh làm điều kiện bắt buộc. Không chấm phần trăm giống C hoặc phần trăm đúng pháp luật.', '',
          '| Nhãn nội dung | A | B |', '|---|---:|---:|']
    for score, name in [(0, 'Thiếu ý cốt lõi'), (1, 'Bao phủ một phần'), (2, 'Bao phủ yêu cầu chính')]:
        md.append(f'| {name} | {counts["a"].get(score, 0)} | {counts["b"].get(score, 0)} |')
    md += ['', 'Đây là nhận xét của một người rà, có căn cứ từng câu bên dưới; chưa có đánh giá độc lập của chuyên gia. Hai luồng cùng có điểm nghẽn là thiếu hướng dẫn áp dụng. Lợi thế Faithfulness của B không đồng nghĩa B giải quyết nhiều yêu cầu thực hành hơn.', '',
           '## Các khác biệt đáng chú ý', '',
           '- Câu 1/30: A trả mẫu không kết luận; B có căn cứ nhưng chưa thành checklist hợp đồng/lưu CCCD.',
           '- Câu 3/10/22: A diễn giải nguyên tắc hoặc bước kiểm tra sát câu hỏi hơn; B chọn đoạn hẹp và bỏ mất phần áp dụng.',
           '- Câu 8/11/16/19/24/29: cả hai thiếu ý thực hành cốt lõi dù tìm được nguồn cùng chủ đề.',
           '- Câu 31/32/35: B có nhiều căn cứ hơn A, vẫn cần diễn giải giới hạn công khai, cách yêu cầu xử lý và phân biệt tranh chấp/lừa đảo.',
           '- Câu 36: C có bảng từng người/từng giao dịch; cả hai mới nói lưu bằng chứng/trình báo chung.', '',
           '## Bản dán cần rà trước khi dùng làm đáp án chuẩn', '',
           '- Nhóm dữ liệu cá nhân: đang dựa Nghị định 13/2023. Nguồn hiện hành đã có Luật 91/2025 và Nghị định 356/2025; xem nguồn kiểm tra hiệu lực bên dưới.',
           '- Câu 35/36 và chỉ dẫn đơn vị cấp huyện: tên Tòa án/Công an quận huyện cần cập nhật theo thay đổi tổ chức, không đưa nguyên văn vào sản phẩm.',
           '- Câu 18: dẫn hệ PCCC cũ và áp số lối thoát/số bình cho mọi nhà trọ; cần rà theo pháp luật hiện hành, loại nhà, tầng, diện tích và quy chuẩn.',
           '- Các số giá điện/nước, mức phạt, mốc 30 ngày, hoàn cọc 3–5 ngày, tỷ lệ “99% lừa đảo” và kết luận chắc chắn khởi tố chưa được xác minh đầy đủ trong lần đối chiếu này. Không dùng chúng làm tiêu chí bắt hệ thống phải khớp.', '',
           'Các nguồn được mở/tra cứu ngày 04/10/2026; kiểm tra có chọn lọc, không chứng nhận toàn bộ 36 đáp án:', '']
    for title, url, observation in SOURCES:
        md.append(f'- [{title}]({url}): {observation}')
    md += ['', '## Bảng đối chiếu từng câu', '', '| Câu | A (bao phủ 0–2) | B (bao phủ 0–2) | So với yêu cầu và bản dán | Điểm bản dán cần rà |', '|---|---|---|---|---|']
    def cell(s: str) -> str:
        return s.replace('|', '\\|').replace('\n', ' ')
    for row in rows:
        v = row['review']
        md.append('| ' + ' | '.join([str(row['id']), cell(f"{v['practical_coverage_a']}: {v['observation_a']}"), cell(f"{v['practical_coverage_b']}: {v['observation_b']}"), cell(v['comparison']), cell(v['reference_risk'])]) + ' |')
    md += ['', '## Phương án rút ra từ đối chiếu', '',
           'Với câu hỏi pháp lý, B là ứng viên tốt để chọn bằng chứng; A cho thấy lợi thế khi diễn giải ngắn và sát yêu cầu. Hướng cần thử tiếp là **Gemini phân tích → truy xuất → Qwen chọn bằng chứng → Gemini diễn giải thành câu trả lời ngắn/checklist → kiểm chứng từng mệnh đề với nguồn và hiệu lực**. Đây là thiết kế đề xuất, chưa được chạy hay chứng minh tối ưu bằng kết quả hiện tại.', '',
           'Đầu ra nên có kết luận có điều kiện, 3–5 bước thực hiện và 1–3 trích dẫn phù hợp; khi thiếu dữ kiện cần hỏi cụ thể. Tránh chèn toàn khối chuyển tiếp vào câu trả lời. Trước khi thử lại, bổ sung nguồn thực hành đã rà, nguồn hiệu lực và quy trình đúng cho các câu thiếu ở bảng.', '',
           'Bản dán dùng làm mục tiêu về cấu trúc và độ hữu ích; cần rà từng mệnh đề trước khi dùng làm ground truth. Ưu tiên cải thiện câu 1, 8, 11, 16, 19, 24, 29, 30, 35, 36.', '',
           '[Nguyên văn ba đáp án cho đủ 36 câu](gemini_qwen_vs_pasted_2026-10-04_details.md) · [JSON và nhãn rà](gemini_qwen_vs_pasted_2026-10-04.json) · [Đối chiếu A/B và phương pháp RAGAS](gemini_vs_qwen_2026-10-04.md)', '',
           'Tái lập: `python -X utf8 eval/compare_three_legal_answers.py`. Script chỉ dựng báo cáo, không gọi model. SHA-256 tệp đầu vào:', '']
    md += [f'- `{name}`: `{h}`' for name, h in initial_hashes.items()]
    out_md.write_text('\n'.join(md) + '\n', encoding='utf-8')
    detail = ['# Nguyên văn 36 câu: Gemini, Gemini + Qwen, bản dán', '', '[Báo cáo và giới hạn đánh giá](gemini_qwen_vs_pasted_2026-10-04.md). Bản dán chưa được xác minh như ground truth. Nội dung được giữ nguyên từ snapshot.', '']
    for row in rows:
        v = row['review']
        detail += [f"## Câu {row['id']}: {row['question']}", '']
        if row['question_match'] != 'exact':
            detail += [f"Câu phía hệ thống: {row['system_question']}", '']
        detail += ['### C: Bản bạn dán', '', row['reference_answer'], '', '### A: Gemini', '', row['gemini_case']['answer'], '', '### B: Gemini + Qwen', '', row['hybrid_case']['answer'], '', '### Nhận xét', '', f"A — {v['observation_a']}", '', f"B — {v['observation_b']}", '', v['comparison'], '', f"Bản dán cần rà: {v['reference_risk']}", '', '### Nguồn và trạng thái của hai lượt', '']
        for label, key in [('A', 'gemini_case'), ('B', 'hybrid_case')]:
            case = row[key]
            detail += [f"{label}: partial_answer={case.get('partial_answer')}; no_answer={case.get('no_answer')}; generation_provider={case.get('generation_provider')}; latency_ms={case.get('latency_ms')}", '']
            for source in case.get('sources', []):
                detail.append(f"- [{label}, rank {source.get('rank')}] {source.get('title')}; chunk {source.get('chunk_id')}; {source.get('source_url')}")
            detail.append('')
    out_details.write_text('\n'.join(detail) + '\n', encoding='utf-8')
    assert all(digest(p) == initial_hashes[str(p.relative_to(ROOT))] for p in paths)
    assert len(rows) == 36 and len(detail) > 0
    print(json.dumps({'cases': len(rows), 'coverage_counts': counts, 'median_characters': lengths, 'inputs_unchanged': True}, ensure_ascii=False))


if __name__ == '__main__':
    main()
