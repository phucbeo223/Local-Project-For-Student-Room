"""Summarize actual focus-three runs, local comparisons and provenance audit."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path('/workspace')
REPORTS = Path('/eval/reports')


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', default='v11')
    args = parser.parse_args()
    version = args.version
    run_path = REPORTS / f'graph_rag_focus3_pilot_{version}_2026-10-06.json'
    compare_path = REPORTS / f'graph_rag_focus3_reference_{version}_2026-10-06.json'
    run, compared = read(run_path), read(compare_path)
    baseline = read(REPORTS / 'graph_rag_focus3_reference_v9_2026-10-06.json')
    audit = read(REPORTS / 'graph_rag_focus3_audit_v11_2026-10-06.json')
    reference = ROOT / 'eval/datasets/external_legal_20261004/answers.json'
    assert compared['run_sha256'] == hashlib.sha256(run_path.read_bytes()).hexdigest()
    assert compared['reference_sha256'] == hashlib.sha256(reference.read_bytes()).hexdigest()
    assert baseline['reference_sha256'] == compared['reference_sha256']
    assert run['selected_original_ids'] == [47, 48, 49] and len(run['cases']) == 3
    assert all(c.get('answer') and not c.get('error') for c in run['cases'])
    assert audit['passed'] and run['legal_manifest_sha256'] == audit['corpus_manifest_sha256']
    old = {c['id']: c for c in baseline['cases']}
    comparison = {c['id']: c['comparison'] for c in compared['cases']}
    label = {'high': 'Khớp cao', 'partial': 'Khớp một phần', 'low': 'Khớp thấp'}
    lines = ['# Sửa riêng câu 47–49 theo bộ đáp án mới — 06/10/2026', '',
             'Đối chiếu với bộ `external-legal-user-2026-10-06`, giữ nguyên đáp án người dùng. '
             'Sinh câu trả lời bằng Qwen chọn nguồn + Gemini phân tích/tổng hợp/kiểm chứng; chấm đối chiếu bằng Qwen cục bộ. '
             'Không gửi đáp án mẫu hoặc dữ liệu nhà trọ lên Gemini; không hard-code câu trả lời theo ID.', '',
             '| Câu | Trước sửa, chấm bằng đáp án mới | Sau sửa | Ký tự | Luồng cuối | Trả lời một phần |',
             '|---|---|---|---:|---|---|']
    for case in run['cases']:
        lines.append(f"| {case['id']} | {label[old[case['id']]['comparison']['agreement']]} | {label[comparison[case['id']]['agreement']]} | {len(case['answer'])} | {case['generation_provider']} | {'Có' if case['partial_answer'] else 'Không'} |")
    answers = {c['id']: c['answer'] for c in run['cases']}
    assert 'phường' in answers[47] and 'quận' in answers[47] and 'ảnh' in answers[48] and 'trao đổi' in answers[48]
    assert '24 giờ' in answers[49] and '2027' in answers[49]
    lines += ['', f"Kết quả chấm nội dung: {json.dumps(compared['summary']['agreement'], ensure_ascii=False)}. "
              'Đây là nhãn khớp nội dung, không phải tỷ lệ đúng pháp luật. Nhãn khớp cao và cờ nguồn/trả lời một phần đo hai việc khác nhau.', '',
              '## Rà soát trực tiếp câu trả lời', '',
              '- Câu 47: đủ nhóm tài khoản/người đăng, địa chỉ, hình ảnh, giá. Câu trả lời thực tế có địa chỉ gồm số nhà, tên đường, phường, quận; không thiếu nhóm kiểm tra địa chỉ.',
              '- Câu 48: có thao tác báo tin, lý do, nội dung gửi, link tin, số điện thoại liên hệ của người báo, hỗ trợ chat/email công bố và hình ảnh trao đổi nếu có. Chưa coi link tin là yêu cầu mã tin, hoặc điện thoại người báo là điện thoại người đăng; nguồn xuất bản nêu khác bộ mẫu. Không tự tạo thời hạn gỡ mọi báo cáo trong 24 giờ.',
              '- Câu 49: có công khai/định danh, lọc từ khóa/kiểm duyệt, phản ánh/gỡ tin và cung cấp dữ liệu/tạm ngừng tài khoản theo điều kiện. Có mốc xác thực 2027 và yêu cầu cơ quan có thẩm quyền cho thời hạn 24 giờ. Khác mẫu ở điều kiện pháp lý và phạm vi người bán/người cho thuê.',
              'Các danh sách điểm thiếu/khác ở cuối báo cáo là đầu ra nguyên vẹn của Qwen để kiểm tra, có thể chứa nhận xét sai; dùng cùng câu trả lời thực tế và phần rà soát này.', '',
              'Theo bộ chấm hiện tại, chưa đạt mức khớp cao cho cả ba câu. Câu 48 còn khác về ảnh chụp màn hình trong biểu mẫu, mã tin/điện thoại người đăng và cam kết xử lý 24 giờ. Câu 49 còn khác về đối tượng cho thuê và điều kiện/thời điểm xác thực. Những chi tiết chưa có căn cứ không được bổ sung như quy định chắc chắn chỉ để tăng nhãn khớp.', '',
              '## Các khâu đã sửa', '',
              '- Gemini phân tích: chuẩn hóa trường `missing_information` dạng chuỗi sang danh sách, cung cấp schema trong prompt và ghi rõ trường lỗi; không bỏ kiểm tra các trường khác.',
              '- Truy xuất: phân biệt checklist người thuê với trách nhiệm nền tảng; giữ đủ nguồn tài khoản, địa chỉ, hình ảnh, giá; đọc đầy đủ khoản gốc khi xếp hạng.',
              '- Chọn nguồn bằng Qwen: kiểm tra nhóm ý bị bỏ sót, retry có giới hạn; giữ các nhóm lọc từ khóa/gỡ tin, định danh, phản ánh, cung cấp dữ liệu; không để điều hiệu lực chiếm chỗ nội dung chính.',
              '- Gemini tổng hợp: thao tác báo tin, kênh hỗ trợ, hình ảnh/bằng chứng; nêu các nhóm nghĩa vụ, điều kiện loại nền tảng và ngày áp dụng trong từng câu.',
              '- Kiểm chứng: giữ đúng sự kiện bắt đầu thời hạn 24 giờ; chặn xác thực điện tử được trình bày như nghĩa vụ hiện tại khi chưa đến mốc áp dụng; cảnh báo cuối bài không sửa được câu khẳng định sai. Kiểm tra nhóm trách nhiệm bị Gemini bỏ sót và yêu cầu sửa có giới hạn.',
              '- Giữ câu trả lời và dự phòng dưới 3.500 ký tự; không cắt giữa điều kiện/ngoại lệ pháp luật. Chặn email không có nguyên văn trong nguồn. 108 kiểm thử hồi quy đã đạt; kiểm tra tích hợp truy xuất xác nhận đã lấy được trích đoạn hình ảnh và điều khoản thi hành.', '',
              '## Khác biệt cần giữ so với đáp án mẫu', '',
              'Câu 48: không cam kết mọi phản ánh của người dùng đều được gỡ trong 24 giờ. '
              'Điều 17 khoản 1 điểm c Nghị định 248/2026/NĐ-CP trong nguồn gắn mốc này với yêu cầu của cơ quan nhà nước có thẩm quyền. '
              'Các thao tác và kênh hỗ trợ được ghi rõ là hướng dẫn Chợ Tốt/Nhà Tốt, không áp dụng nguyên xi cho mọi nền tảng.', '',
              'Câu 49: nghĩa vụ cung cấp dữ liệu 24 giờ của Điều 18 khoản 2 cần giữ điều kiện nền tảng trung gian có chức năng đặt hàng và yêu cầu cơ quan có thẩm quyền. '
              'Xác thực điện tử phải giữ mốc 01/01/2027 trong nguồn hiệu lực; không diễn đạt đã bắt buộc ở ngày chạy. '
              'Chưa coi các quy định về người bán tự động áp dụng giống nhau cho mọi người cho thuê hoặc trang đăng tin.', '',
              '[Nghị định trên Công báo Chính phủ](https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-248-2026-nd-cp-469983.htm). '
              'Đáp án người dùng chưa được xác minh toàn bộ; các điểm này được ghi nhận riêng, không sửa bộ mẫu để tăng điểm.', '',
              '## Dữ liệu và nguồn', '',
              'Mã xử lý cuối đã được cập nhật lên FastAPI cục bộ: `/health` và `/docs` trả HTTP 200; hash 9 mô-đun khớp workspace. '
              'Phiếu triển khai: `docs/FOCUS3_API_DEPLOYMENT_20261006.json`. Các kết quả ba câu trong báo cáo này thuộc kho thử, chưa phải kết quả chạy trên kho đang phục vụ API.', '',
              'Kho thử riêng `legal_word_focus3_v11_20261006`: 32 tài liệu Word, 425 vector E5/384 chiều; '
              'graph `graph_rag_word_focus3_v11`, nhà trọ `housing_graph_word_focus3_v11`. '
              '31 mục nguồn của v10 giữ nguyên byte; v10 kế thừa nguyên 30 mục của kho bổ sung v8. '
              'Không OCR, không PDF, không embedding đáp án mẫu.', '',
              'Nguồn bổ sung là trích nguyên văn ngắn được đối chiếu với HTML nhà xuất bản, chuyển thành Word và kiểm tra lại nội dung/hash:', '',
              '- [Google Search Help: tìm ảnh bằng Google Lens](https://support.google.com/websearch/answer/1325808?co=GENIE.Platform%3DDesktop&hl=vi): 19 từ nguyên văn để hỗ trợ tìm nguồn hình ảnh; kết quả ảnh không tự chứng minh gian lận.',
              '- [Trợ Giúp Nhà Tốt: phản ánh tin/người bán, hình ảnh trao đổi](https://trogiup.chotot.com/nguoi-mua/bi-quyet-mua-bat-dong-san-an-toan-voi-nha-tot/): 21 từ nguyên văn về hình ảnh trao đổi thể hiện vi phạm; giữ cảnh báo bối cảnh mua bất động sản.', '',
              'Kiểm tra hash toàn dòng xác nhận kho đang dùng `legal_word_v7_20261005`, graph `graph_rag_word_v6`, '
              'nhà trọ `housing_graph_word_v6`, dữ liệu public và người dùng giữ nguyên. '
              'Bản thử Datahouse có cùng 789 dòng/vector. Kho thử v11 còn staging; chưa đổi kho đang phục vụ API. '
              'Không chạy lại toàn bộ 36/56 câu trong lượt sửa này.', '',
              f"Hash bộ đáp án: `{compared['reference_sha256']}`.",
              f"Hash manifest nguồn: `{run['legal_manifest_sha256']}`.",
              f"Hash mã pipeline của lượt chạy: `{run['pipeline_sha256']}`.", '',
              f'Bằng chứng chi tiết: `eval/reports/{run_path.name}`, `{compare_path.name}`, '
              '`graph_rag_focus3_audit_v11_2026-10-06.json`, `gemini_focus3_analysis_diagnostics_2026-10-06.json`.', '',
              '## Câu trả lời thực tế và đối chiếu từng câu', '']
    for case in run['cases']:
        judged = comparison[case['id']]
        lines += [f"### Câu {case['id']}: {case['question']}", '', case['answer'], '',
                  'Đối chiếu cục bộ: ' + label[judged['agreement']] + '. ' + judged['explanation'], '',
                  'Điểm thiếu theo mô hình chấm (cần đọc cùng đáp án thực tế):', '',
                  *['- ' + p for p in judged['missing_reference_points']], '',
                  'Khác biệt theo mô hình chấm:', '', *['- ' + p for p in judged['differing_points']], '',
                  'Nguồn đã truy xuất:', '',
                  *[f"- [{s['rank']}] {s['title']} — {s['heading']} — [bản gốc]({s['source_url']})" for s in case['sources']], '']
    target = ROOT / 'docs/FOCUS3_IMPROVEMENT_20261006.md'
    target.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(json.dumps(dict(report=str(target), agreement=compared['summary']['agreement'],
                         successful_generations=len(run['cases']), runtime_errors=run['summary'].get('errors')), ensure_ascii=False))


if __name__ == '__main__':
    main()
