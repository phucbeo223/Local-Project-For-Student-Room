"""Export a public legal-only comparison and citations for every answer line."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
from question_bank_ragas import pipeline_sha256

ROOT = Path('/workspace')
REPORTS = Path('/eval/reports')
IDS = list(range(19,39)) + list(range(43,59))
PRIORITY = [26,28,29,32,37,47,52]


def read(name):
    return json.loads((REPORTS/name).read_text(encoding='utf-8'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def label(case):
    comparison = case.get('comparison')
    if not comparison or not case.get('quote_audit_passed'): return 'unscored'
    points = comparison['points']
    matched = sum(p['status']=='matched' for p in points)
    if not matched: return 'low'
    return 'high' if matched == len(points) else 'partial'


def main():
    run = read('graph_rag_priority7_36_v20_2026-10-06.json')
    old_run = read('graph_rag_word_supplement_36_v8_2026-10-05.json')
    before = read('graph_rag_priority7_baseline_review_v23_2026-10-06.json')
    after = read('graph_rag_priority7_reference_review_v23_2026-10-06.json')
    audit = read('graph_rag_priority7_audit_v13_2026-10-06.json')
    for data in (run,old_run,before,after):
        assert sorted(c['id'] for c in data['cases']) == IDS
        assert all(c.get('answer') and not c.get('error') for c in data['cases'])
    assert before['reference_sha256'] == after['reference_sha256'] == audit['reference_sha256']
    assert before['policy'] == after['policy'] and before['judge_model'] == after['judge_model']
    assert before['reference_audit_sha256'] == after['reference_audit_sha256']
    assert before['scorer_sha256'] == after['scorer_sha256'] == sha(Path('/eval/compare_grounded_references.py'))
    assert all({c['id']:c['question'] for c in before['cases']}[i] == {c['id']:c['question'] for c in after['cases']}[i] for i in IDS)
    assert run['selected_original_ids'] == IDS and run['pipeline_sha256']
    assert run['pipeline_sha256'] == pipeline_sha256(ROOT/'apps/api/app/room_service/chatbot')
    assert audit['passed'] and audit['active_store_unchanged']
    original = {c['id']:c for c in old_run['cases']}
    bmap = {c['id']:c for c in before['cases']}; amap = {c['id']:c for c in after['cases']}
    cases = {c['id']:c for c in run['cases']}
    runtime = dict(total=36,generated=36,errors=0,
        complete=sum(not c.get('partial_answer') for c in run['cases']),
        partial=sum(bool(c.get('partial_answer')) for c in run['cases']),
        providers=dict(Counter(c['generation_provider'] for c in run['cases'])),
        literal_source_answer_ids=[c['id'] for c in run['cases'] if c['generation_provider']=='qwen-local' and c['answer'].startswith('Các đoạn trả lời trực tiếp trong nguồn:')],
        longest_answer_chars=max(len(c['answer']) for c in run['cases']))
    before_runtime = dict(total=36,generated=36,errors=0,
        complete=sum(not c.get('partial_answer') for c in old_run['cases']),
        partial=sum(bool(c.get('partial_answer')) for c in old_run['cases']),
        providers=dict(Counter(c['generation_provider'] for c in old_run['cases'])),
        longest_answer_chars=max(len(c['answer']) for c in old_run['cases']))
    summary = dict(runtime=runtime,before_runtime=before_runtime,before_agreement=dict(Counter(label(c) for c in before['cases'])),
        after_agreement=dict(Counter(label(c) for c in after['cases'])),
        before_quote_audit_passed=sum(c['quote_audit_passed'] for c in before['cases']),
        after_quote_audit_passed=sum(c['quote_audit_passed'] for c in after['cases']),
        priority=[dict(id=i,before=label(bmap[i]),after=label(amap[i]),
                       partial=cases[i]['partial_answer'],provider=cases[i]['generation_provider'],
                       chars=len(cases[i]['answer'])) for i in PRIORITY],
        high_ids=[i for i in IDS if label(amap[i])=='high'],
        partial_ids=[i for i in IDS if label(amap[i])=='partial'],
        low_ids=[i for i in IDS if label(amap[i])=='low'],
        unscored_ids=[i for i in IDS if label(amap[i])=='unscored'],
        pipeline_sha256=run['pipeline_sha256'],reference_sha256=after['reference_sha256'],
        source_manifest_sha256=run['legal_manifest_sha256'],judge_policy=after['policy'],
        scorer_sha256=sha(Path('/eval/compare_grounded_references.py')),
        label_policy='audited_main_point_consistency_v1',
        before_model_agreement=dict(Counter((c.get('comparison') or {}).get('agreement','unscored') for c in before['cases'])),
        after_model_agreement=dict(Counter((c.get('comparison') or {}).get('agreement','unscored') for c in after['cases'])),
        before_label_corrections=[c['id'] for c in before['cases'] if c.get('comparison') and label(c)!=c['comparison']['agreement']],
        after_label_corrections=[c['id'] for c in after['cases'] if c.get('comparison') and label(c)!=c['comparison']['agreement']],
        report_processor_sha256=sha(Path(__file__)),
        active_store_unchanged=True,new_store_active=False,reference_answers_unchanged=True)
    order = {'low':0, 'partial':1, 'high':2}
    jointly_scored = [i for i in IDS if label(bmap[i]) in order and label(amap[i]) in order]
    summary['agreement_improved_ids'] = [i for i in jointly_scored if order[label(amap[i])] > order[label(bmap[i])]]
    summary['agreement_decreased_ids'] = [i for i in jointly_scored if order[label(amap[i])] < order[label(bmap[i])]]
    summary['newly_scored_ids'] = [i for i in IDS if label(bmap[i])=='unscored' and label(amap[i])!='unscored']
    summary['lost_scored_ids'] = [i for i in IDS if label(bmap[i])!='unscored' and label(amap[i])=='unscored']
    (REPORTS/'graph_rag_priority7_summary_v20_2026-10-06.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines = ['# Sửa 7 câu ưu tiên và chạy lại cùng 36 câu — 06/10/2026','',
        'Bản trước sửa đã được push lên nhánh `codex/legal-priority7-20261006` tại GitHub cá nhân, commit `ab0470c`. Lượt này tiếp tục trên cùng nhánh.', '',
        'Cả hai bản được đối chiếu với nguyên bộ đáp án người dùng ngày 06/10/2026 bằng cùng Qwen cục bộ và cùng rubric có kiểm tra trích đoạn. Không gửi đáp án mẫu hoặc nhà trọ lên Gemini; không embedding đáp án, không hard-code câu trả lời theo ID.', '',
        '## Kết quả', '', f'- Sinh được câu trả lời: **36/36**, lỗi thực thi: **0**.',
        f'- Theo cờ bao phủ nguồn: trước **{before_runtime["complete"]} đầy đủ / {before_runtime["partial"]} một phần**; sau **{runtime["complete"]} đầy đủ / {runtime["partial"]} một phần**.',
        f'- Khớp nội dung với mẫu trước sửa: `{summary["before_agreement"]}`.',
        f'- Khớp nội dung với mẫu sau sửa: `{summary["after_agreement"]}`.',
        f'- Các câu chưa qua kiểm tra bộ chấm: `{summary["unscored_ids"]}`; không gán điểm thay thế.',
        f'- Các câu có nhãn low: `{summary["low_ids"]}`.',
        f'- Nhãn tăng ở các câu đã chấm được cả hai bản: `{summary["agreement_improved_ids"]}`; nhãn giảm: `{summary["agreement_decreased_ids"]}`.',
        f'- Trước chưa chấm được, sau chấm được: `{summary["newly_scored_ids"]}`; chiều ngược lại: `{summary["lost_scored_ids"]}`.',
        f'- Kiểm tra trích đoạn bộ chấm: trước **{summary["before_quote_audit_passed"]}/36**, sau **{summary["after_quote_audit_passed"]}/36**.',
        f'- Luồng trả lời cuối: `{runtime["providers"]}`; câu trả các đoạn nguồn đã chọn: `{runtime["literal_source_answer_ids"]}`.',
        f'- Câu dài nhất: trước **{before_runtime["longest_answer_chars"]}**, sau **{runtime["longest_answer_chars"]} ký tự**.', '',
        'Các nhãn high/partial/low đo mức khớp văn bản, không phải tỷ lệ đúng pháp luật. “Một phần” là thiếu nguồn/điều kiện, không phải lỗi chạy. Trích dẫn có đúng định dạng cũng không chứng minh mọi kết luận đúng. Mẫu chưa được chứng nhận toàn bộ; các điểm cần kiểm tra ghi riêng trong `REFERENCE_REVIEW_36_20261006.md`.', '',
        'Câu 27, 30, 31 đều đã gọi Gemini trong workflow. Đầu ra cuối quay về các đoạn Word do Qwen chọn vì kiểm tra quy tắc nguồn còn chặn bản tổng hợp sau lần sửa; provider cuối không mô tả toàn bộ agent đã tham gia. Lý do được giữ bên dưới từng câu.', '',
        'Nhãn tổng hợp lấy từ các ý CHÍNH đã qua audit: high nếu tất cả là matched; partial nếu có cả matched và missing/different; low nếu chưa có ý matched; unscored nếu chưa qua audit. Không dùng trực tiếp nhãn agreement của Qwen, vì có trường hợp cả sáu ý different nhưng mô hình gán high. Nhãn gốc và trích đoạn được giữ nguyên để rà; chưa thẩm định độc lập toàn bộ đánh giá ngữ nghĩa từng ý.', '',
        f'- Nhãn Qwen gốc trước: `{summary["before_model_agreement"]}`; sau: `{summary["after_model_agreement"]}`.',
        f'- Câu chỉnh nhãn tổng hợp do không nhất quán: trước `{summary["before_label_corrections"]}`; sau `{summary["after_label_corrections"]}`.', '',
        'V16 bị Qwen timeout do chạy sinh/chấm đồng thời. V17–18 dừng để sửa lỗi kiểm tra phủ định nguồn; v19 thử riêng bảy câu. Sinh chính thức v20; chấm chính thức v23: Qwen chọn ID đoạn, schema ràng buộc trạng thái/ID, phần mềm lấy quote và nhận đúng 3/4 = 75%. Các điểm hợp lệ từ chấm v22 được kiểm tra lại toàn bộ quote/ID/số liệu bằng rubric cuối trước khi giữ, ghi hash mã gốc và mã tái kiểm tra; các câu lỗi/chưa chấm chạy lại. Chấm thử v20–21 không dùng trong số cuối. Không so sánh tốc độ giữa các lượt này.', '',
        '## Bảy câu ưu tiên', '', '| Câu | Trước | Sau | Bao phủ nguồn | Luồng cuối | Ký tự |','|---|---|---|---|---|---|']
    for c in summary['priority']:
        lines.append(f'| {c["id"]} | {c["before"]} | {c["after"]} | {"một phần" if c["partial"] else "đầy đủ"} | {c["provider"]} | {c["chars"]} |')
    lines += ['', '## Các khâu sửa', '',
        '- Truy xuất giữ các nhóm nguồn riêng: thông tin/hóa đơn/thỏa thuận; mục đích/lưu trữ/cung cấp dữ liệu; phòng ngừa/thoát nạn/114; nghĩa vụ công dân/chủ hộ/hồ sơ cơ bản.',
        '- Qwen chọn nguyên đơn vị nguồn; retry có giới hạn. Nếu còn chỗ trong bốn ID, quy tắc bổ sung đơn vị thật đã truy xuất cho nhóm bỏ sót, ghi `evidence_coverage_completion` trong trace. Nếu vẫn thiếu, đánh dấu một phần.',
        '- Gemini tổng hợp có nguồn trong từng câu; phân biệt khuyến nghị với nghĩa vụ, điều kiện/chủ thể, hiệu lực muộn và ngoại lệ. Giữ giới hạn 3.500 ký tự.',
        '- Kiểm chứng phân biệt phủ định/giới hạn nguồn và câu hỏi về thỏa thuận với khẳng định quyền/nghĩa vụ. Kiểm tra đúng chủ thể trong mệnh đề; nhận điều kiện hiệu lực và điều kiện đồng ý từ nguồn, giữ ngoại lệ. Vẫn chặn khẳng định không có nguồn.',
        '- Gemini trả JSON sai schema được thử sửa một lần với nguyên nguồn đã chọn; không bỏ qua validation. Bản sửa vẫn qua kiểm chứng quy tắc và Gemini.',
        '- Rà riêng đủ 36 mẫu, giữ nguyên bản gốc. Qwen chọn ID đoạn mẫu/trả lời, chương trình lấy quote nguyên văn. Bộ chấm chặn ID bịa, quote thiếu, nhận xét thiếu trong khi nguyên văn có trong câu trả lời, và số liệu/đơn vị khác bị gọi là khớp; số thứ tự không được coi là số liệu.',
        '- Nhãn khớp tổng hợp suy ra từ các trạng thái ý chính đã qua audit, giữ nhãn Qwen gốc riêng; không chấp nhận nhãn high khi toàn bộ ý là different/missing.',
        '- 154 kiểm thử hồi quy đã đạt cho mã xử lý, bộ chấm và tổng hợp nhãn dùng trong lượt này.', '',
        '## Kho thử và dữ liệu giữ nguyên', '',
        '`legal_word_priority7_v13_20261006`: **34 Word, 445 vector E5/384 chiều**. Graph `graph_rag_word_priority7_v13`; housing `housing_graph_word_priority7_v13`: **789 bản ghi/vector** trùng dữ liệu đang dùng theo hash toàn dòng.',
        'Giữ 29 mục v11 nguyên byte; mở rộng từ Word gốc Điều 10 Luật Cư trú, Điều 3/398 BLDS và Điều 7 NĐ248; thêm trích đoạn thật EVNSPC Cần Thơ về công khai cách tính điện và Công an Phú Thọ về 114. Không OCR/PDF/tờ khai/mẫu hợp đồng hoặc nội dung tự soạn đưa vào embedding.',
        'Audit hash toàn dòng của các kho đang dùng, dữ liệu public và người dùng đạt. Kho mới còn staging; chưa chuyển FastAPI sang kho này. Các kết quả dưới đây chạy ChatService thực trên kho thử, không phải kết quả từ HTTP API đang dùng kho v7.', '',
        '## Cả 36 câu', '', '| Câu | Trước | Sau | Bao phủ nguồn sau sửa |','|---|---|---|---|']
    lines += [f'| {i} | {label(bmap[i])} | {label(amap[i])} | {"một phần" if cases[i]["partial_answer"] else "đầy đủ"} |' for i in IDS]
    lines += ['', '## Câu trả lời và nguồn cho từng kết luận', '',
        'Mỗi câu trả lời giữ rank trích dẫn của lượt chạy. Sau đó là ánh xạ từng dòng kết luận sang URL/điều khoản. Đây là bằng chứng xuất xứ và đầu ra kiểm chứng của hệ thống; chưa thay thế thẩm định pháp lý độc lập.']
    for i in IDS:
        c = cases[i]; sources = {int(s['rank']):s for s in c['sources']}
        lines += ['',f'### Câu {i}: {c["question"]}', '', c['answer'], '', '**Nguồn của từng dòng có trích dẫn:**', '']
        for line in c['answer'].splitlines():
            ranks = list(dict.fromkeys(map(int,re.findall(r'\[(\d+)\]',line))))
            if not ranks: continue
            assert all(rank in sources for rank in ranks)
            links = [f'[{rank}: {sources[rank]["title"]} — {sources[rank].get("heading") or "trích đoạn"}]({sources[rank].get("source_url")})' for rank in ranks]
            lines += [f'- {line.lstrip("- ")}', '  ' + '; '.join(links)]
        if i in runtime['literal_source_answer_ids']:
            lines += ['', '**Lý do dùng đoạn nguồn:** ' + '; '.join(c.get('degraded_reasons') or [])]
        review = amap[i]
        lines += ['', '**Đối chiếu nguyên mẫu:**', '', f'Nhãn tổng hợp: **{label(review)}**; nhãn Qwen gốc: **{(review.get("comparison") or {}).get("agreement","unscored")}**. ' + ((review.get('comparison') or {}).get('explanation') or 'Chưa chấm được; không tạo điểm thay thế.'), '',
                  '**Rà mẫu/nguồn:** ' + review['reference_review']['review_note']]
        if not review.get('quote_audit_passed'):
            lines += ['', '**Lỗi kiểm tra bộ chấm:** ' + '; '.join(review.get('judge_errors') or ['Chưa có đối chiếu được chấp nhận.'])]
        if review.get('comparison'):
            lines += ['', '| Điểm | Trích mẫu có thật | Trích câu trả lời có thật | Giải thích |','|---|---|---|---|']
            for point in review['comparison']['points']:
                vals = [point[k].replace('|','/').replace('\n',' ') for k in ('status','reference_quote','answer_quote','explanation')]
                lines.append('| '+' | '.join(vals)+' |')
    lines += ['', '## Khả năng tái lập', '',
        f'- IDs gốc: `{IDS}`.', f'- Bộ đáp án: `{summary["reference_sha256"]}`.',
        f'- Manifest: `{summary["source_manifest_sha256"]}`.', f'- Pipeline: `{summary["pipeline_sha256"]}`.',
        f'- Rubric: `{summary["judge_policy"]}`; mã bộ chấm `{summary["scorer_sha256"]}`.',
        f'- Tổng hợp nhãn: `{summary["label_policy"]}`; mã xử lý báo cáo `{summary["report_processor_sha256"]}`.',
        '- `.gitattributes` giữ nguyên byte các gói Word và bộ mẫu. Các thay đổi xuống dòng khi lưu Git không đổi nội dung; SHA được đối chiếu với byte thực dùng trong lượt chạy.',
        '- Chi tiết cục bộ: `eval/reports/graph_rag_priority7_36_v20_2026-10-06.json`, `graph_rag_priority7_baseline_review_v23_2026-10-06.json`, `graph_rag_priority7_reference_review_v23_2026-10-06.json`, `graph_rag_priority7_audit_v13_2026-10-06.json`.',
        '- Các báo cáo raw giữ cục bộ theo `.gitignore`; báo cáo này chỉ xuất 36 câu pháp lý, không xuất Datahouse hoặc thông tin người dùng.']
    target = ROOT/'docs/PRIORITY7_36_COMPARISON_20261006.md'
    target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False))


if __name__ == '__main__':
    main()
