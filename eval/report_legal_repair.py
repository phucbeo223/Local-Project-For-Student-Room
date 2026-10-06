"""Compare completed runs using identical frozen reference-scoring inputs."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

FOCUS = (23, 26, 27, 28, 30, 31, 32, 34, 36, 45, 50, 58)
REGRESSION = (29, 37, 47, 52)


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def agreement(case):
    return case['comparison']['agreement'] if case.get('comparison') else 'unscored'


def runtime(case):
    trace = [s for s in case.get('agent_trace', []) if s.get('agent') == 'source_verification']
    verdicts = next((s['claim_verdicts'] for s in reversed(trace) if s.get('claim_verdicts')), [])
    rejected = [v for v in verdicts if not v.get('supported')]
    return dict(provider=case.get('generation_provider'), partial=bool(case.get('partial_answer')),
        no_answer=bool(case.get('no_answer')), answer_characters=len(case['answer']),
        answer_words_by_whitespace=len(case['answer'].split()),
        source_count=len(case.get('sources', [])), verification_trace=trace,
        verification_diagnostics=dict(
            selection_marked_partial=any(s.get('agent')=='evidence_selection' and s.get('status')=='partial' for s in case.get('agent_trace',[])),
            partial_retained=any(s.get('status')=='partial_retained' for s in trace),
            remaining_kind_mismatch_ids=[v['claim_id'] for v in rejected if v.get('code')=='claim_kind_mismatch'],
            remaining_content_rejection_ids=[v['claim_id'] for v in rejected if v.get('code')!='claim_kind_mismatch']),
        source_pipeline=dict(
            retrieved_sources=[{k:s.get(k) for k in ('document_id','chunk_id','rank','category','heading','source_url')} for s in case.get('sources',[])],
            retrieval=[s for s in case.get('agent_trace',[]) if s.get('agent')=='legal_retrieval'],
            selection=[s for s in case.get('agent_trace',[]) if s.get('agent')=='evidence_selection'],
            synthesis=[s for s in case.get('agent_trace',[]) if s.get('agent')=='answer_synthesis'],
            rule_checks=[s for s in case.get('agent_trace',[]) if s.get('agent')=='citation_and_rule_checks'],
            diagnostics=case.get('degraded_reasons',[])),
        scope='Only cited evidence/runtime checks; not an independent certification of current law.')


def main():
    p = argparse.ArgumentParser()
    for name in ('baseline-run', 'repaired-run', 'baseline-review', 'repaired-review', 'point-review', 'output-json', 'output-md'):
        p.add_argument('--' + name, type=Path, required=True)
    a = p.parse_args()
    runs = [read(a.baseline_run), read(a.repaired_run)]
    reviews = [read(a.baseline_review), read(a.repaired_review)]
    register = read(a.point_review)
    expected = {c['original_question_id']: c['question'] for c in register['cases']}
    assert len(expected) == 36
    for key in ('policy', 'scorer_sha256', 'quantity_audit_sha256', 'reference_sha256', 'reference_audit_sha256', 'judge_model', 'selected_original_ids'):
        assert reviews[0][key] == reviews[1][key], f'Different rubric/input: {key}'
    assert reviews[0]['reference_sha256'] == register['original_reference_sha256']
    by_run, by_review = [], []
    for run, review, path in zip(runs, reviews, (a.baseline_run, a.repaired_run)):
        cases = {c['id']: c for c in run['cases']}
        scored = {c['id']: c for c in review['cases']}
        assert len(run['cases']) == len(review['cases']) == 36
        assert set(cases) == set(scored) == set(expected)
        assert review['run_sha256'] == sha(path)
        for qid, reference_question in expected.items():
            case, score = cases[qid], scored[qid]
            assert case['question'] == score['question']
            assert case.get('answer') and not case.get('error')
            assert len(case['answer']) <= 3500
            assert score['answer'] == case['answer']
            assert score['question_text_changed'] == (case['question'] != reference_question)
            assert not score.get('comparison') or score['quote_audit_passed']
        by_run.append(cases)
        by_review.append(scored)
    transitions = []
    for qid in sorted(expected):
        assert by_run[0][qid]['question'] == by_run[1][qid]['question'], f'Changed benchmark question: {qid}'
        before, after = (agreement(scores[qid]) for scores in by_review)
        transitions.append(dict(id=qid, question=by_run[0][qid]['question'], reference_question=expected[qid],
            question_differs_from_reference=by_run[0][qid]['question'] != expected[qid], original_reference_before=before,
            original_reference_after=after,
            runtime_before=runtime(by_run[0][qid]), runtime_after=runtime(by_run[1][qid]),
            original_reference_differences=by_review[1][qid].get('comparison'),
            quote_audit_passed=by_review[1][qid]['quote_audit_passed']))
    statuses = Counter(point['source_review_status'] for case in register['cases'] for point in case['points'])
    report = dict(baseline_commit='c8dba04', baseline_run_sha256=sha(a.baseline_run),
        repaired_run_sha256=sha(a.repaired_run),
        baseline_pipeline_sha256=runs[0]['pipeline_sha256'],repaired_pipeline_sha256=runs[1]['pipeline_sha256'],
        baseline_corpus_manifest_sha256=runs[0]['legal_manifest_sha256'],repaired_corpus_manifest_sha256=runs[1]['legal_manifest_sha256'],
        baseline_generation_models=sorted({(call.get('provider'),call.get('model')) for c in runs[0]['cases'] for call in c.get('provider_calls',[])}),
        repaired_generation_models=sorted({(call.get('provider'),call.get('model')) for c in runs[1]['cases'] for call in c.get('provider_calls',[])}),
        cloud_boundary=runs[1].get('cloud_boundary'),cloud_housing_calls=runs[1].get('graph_summary',{}).get('cloud_housing_calls'),
        rubric={k: reviews[0][k] for k in ('policy','scorer_sha256','quantity_audit_sha256','reference_sha256','reference_audit_sha256','judge_model')},
        identical_ids_and_questions=True, original_references_unchanged=True,
        benchmark_question_differs_from_reference=[r['id'] for r in transitions if r['question_differs_from_reference']],
        original_reference_agreement={label: dict(Counter(agreement(s) for s in scores.values()))
                                     for label, scores in zip(('before','after'), by_review)},
        runtime_source_support={label: dict(Counter(c['source_support']['status'] for c in scores.values()))
                                for label,scores in zip(('before','after'),by_review)},
        runtime_source_flags_use_common_verifier=False,
        runtime_source_flag_scope='Saved flags use different workflow verifiers and source corpora. They are descriptive runtime checks, not a common-rubric legal accuracy measurement.',
        runtime_source_coverage={label: dict(partial=sum(bool(c.get('partial_answer')) for c in cases.values()),
                                             complete=sum(not c.get('partial_answer') and not c.get('no_answer') for c in cases.values()),
                                             no_answer=sum(bool(c.get('no_answer')) for c in cases.values()),
                                             no_answer_without_partial=sum(bool(c.get('no_answer')) and not c.get('partial_answer') for c in cases.values()),
                                             generated_answers=sum(bool(c.get('answer')) for c in cases.values()),
                                             providers=dict(Counter(c.get('generation_provider') for c in cases.values())))
                                 for label, cases in zip(('before','after'), by_run)},
        answer_lengths={label: dict(
            word_count_method='Whitespace-separated units; Vietnamese compounds may contain more than one unit.',
            maximum_words=max(len(c['answer'].split()) for c in cases.values()),
            longest_word_case_ids=[qid for qid,c in cases.items() if len(c['answer'].split())==max(len(x['answer'].split()) for x in cases.values())],
            maximum_characters=max(len(c['answer']) for c in cases.values()),
            over_1000_word_cases=[qid for qid,c in cases.items() if len(c['answer'].split())>1000])
            for label,cases in zip(('before','after'),by_run)},
        verification_diagnostics={label: dict(
            selection_marked_partial=sum(runtime(c)['verification_diagnostics']['selection_marked_partial'] for c in cases.values()),
            partial_retained=sum(runtime(c)['verification_diagnostics']['partial_retained'] for c in cases.values()),
            remaining_kind_mismatch_cases=[qid for qid,c in cases.items() if runtime(c)['verification_diagnostics']['remaining_kind_mismatch_ids']],
            remaining_content_rejection_cases=[qid for qid,c in cases.items() if runtime(c)['verification_diagnostics']['remaining_content_rejection_ids']])
            for label,cases in zip(('before','after'),by_run)},
        reviewed_reference=dict(point_register_sha256=sha(a.point_review), point_statuses=dict(statuses),
            scored_as_gold=False, reason='Source review is incomplete. Do not treat manuscript citations as verified law or replace the original reference score.'),
        scope='Text agreement, runtime source coverage and independent legal source review are separate results. No accuracy percentage is inferred from labels.',
        cases=transitions)
    a.output_json.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines = ['# So sánh 36 câu sau sửa bộ chấm và workflow', '',
        'Baseline `c8dba04` và bản sửa dùng cùng 36 ID/câu hỏi của question bank; câu trả lời được sinh hoàn tất trước khi chấm. Hai lượt chấm dùng cùng hash bộ chấm, bộ kiểm tra số liệu và mẫu gốc. Không thay mẫu gốc bằng bản rà còn thiếu xác minh.', '',
        'Nhãn khớp mẫu sau kiểm tra: high khi mọi đoạn/ý mẫu đều matched; partial khi có ít nhất một ý matched và còn ý khác/thiếu; low khi không có ý matched. Nhãn do Qwen đề xuất được lưu riêng trong JSON. Mỗi matched phải có ID đoạn thật, nguyên văn và qua kiểm tra số liệu; kiểm tra này vẫn cần đối chiếu ngữ nghĩa.', '',
        '| Kết quả | Baseline | Bản sửa |', '|---|---|---|']
    for status in ('high','partial','low','unscored'):
        lines.append(f"| Khớp mẫu: {status} | {report['original_reference_agreement']['before'].get(status,0)} | {report['original_reference_agreement']['after'].get(status,0)} |")
    for status in ('complete','partial'):
        lines.append(f"| Cờ bao phủ nguồn lúc chạy: {status} | {report['runtime_source_coverage']['before'][status]} | {report['runtime_source_coverage']['after'][status]} |")
    for field, title in (('maximum_words','Số từ dài nhất (đếm theo khoảng trắng)'),('maximum_characters','Số ký tự dài nhất')):
        lines.append(f"| {title} | {report['answer_lengths']['before'][field]} | {report['answer_lengths']['after'][field]} |")
    lines += ['', 'Cả hai bản đều đã sinh đủ 36 câu trả lời. Trường no_answer lúc chạy cũng có thể được bật cho câu trả lời một phần; bảng trên dùng partial_answer để phân biệt cờ nguồn một phần, không đếm các câu có nội dung này thành câu rỗng.', '',
        'Hai lượt chấm khớp mẫu dùng chung v15. Các cờ nguồn là kết quả lưu từ từng workflow/corpus, có bộ kiểm chứng khác phiên bản; chưa phải đánh giá lại bằng cùng một bộ kiểm chứng pháp lý. Baseline có '+str(report['runtime_source_support']['before'].get('not_independently_verified',0))+' câu không có kiểm chứng độc lập trên đầu ra cuối. Không suy ra mức cải thiện độ chính xác pháp luật từ chênh lệch các cờ này.', '',
        'Các cờ nguồn chỉ mô tả kiểm chứng với chứng cứ được trích lúc chạy; không chứng nhận toàn bộ nội dung là pháp luật hiện hành. Bản rà từng ý có '+str(sum(statuses.values()))+' ý, trong đó '+str(statuses['pending_per_point_source_verification'])+' ý còn chờ đối chiếu nguồn. Chưa công bố điểm với bản rà như một bộ gold đã xác minh.', '',
        '| Câu ưu tiên/hồi quy | Khớp mẫu trước → sau | Bao phủ nguồn bản sửa | Provider cuối |', '|---|---|---|---|']
    for qid in (*FOCUS, *REGRESSION):
        row=next(r for r in transitions if r['id']==qid)
        state='một phần' if row['runtime_after']['partial'] else 'thiếu căn cứ' if row['runtime_after']['no_answer'] else 'đủ theo cờ lúc chạy'
        lines.append(f"| {qid} | {row['original_reference_before']} → {row['original_reference_after']} | {state} | {row['runtime_after']['provider']} |")
    changed=[r for r in transitions if r['original_reference_before']!=r['original_reference_after']]
    lines += ['', '| Các câu đổi nhãn trong toàn bộ 36 câu | Trước → sau |', '|---|---|']
    for row in changed:
        lines.append(f"| {row['id']} | {row['original_reference_before']} → {row['original_reference_after']} |")
    lines += ['',
        'Câu 30 và 48 giảm nhãn khớp mẫu. Câu 30 dùng hướng dẫn CANTHOWASSCO có điều kiện IDKH/mã xác nhận và định dạng ZIP/PDF; mẫu nêu PDF/XML cùng các trường chi tiết chưa được toàn bộ đoạn hướng dẫn xác nhận. Câu 48 giữ phạm vi thao tác theo nền tảng và không hứa gỡ mọi tin trong 24 giờ như mẫu. Các khác biệt này cần được đọc cùng nguồn, không tự diễn giải thành câu trả lời sai pháp luật.', '',
        'Câu 28 vẫn low về khớp mẫu: chưa giữ các mức khoán được gọi là phổ biến, mức tiêu thụ và ngưỡng cao trong mẫu. Dữ liệu đang có chưa chứng minh các khẳng định thống kê đó; giá thực tế vẫn cần hỏi chủ trọ. Không bổ sung số liệu suy đoán để nâng nhãn.']
    mismatches=report['benchmark_question_differs_from_reference']
    if mismatches:
        lines += ['', 'Câu hỏi trong question bank khác câu hỏi đi kèm mẫu ở ID '+', '.join(map(str,mismatches))+'. Cả baseline và bản sửa giữ cùng câu hỏi bank; khác biệt với mẫu được lưu trong JSON, không che giấu bằng việc sửa mẫu.']
    diag=report['verification_diagnostics']['after']
    lines += ['', 'Trace bản sửa: '+str(diag['selection_marked_partial'])+' câu được Qwen đánh dấu chọn nguồn một phần; '+str(diag['partial_retained'])+' câu giữ riêng các kết luận đã kiểm chứng. Các nhóm này có thể trùng nhau.',
        'Những câu còn lỗi phân loại ở lần kiểm chứng cuối: '+(', '.join(map(str,diag['remaining_kind_mismatch_cases'])) or 'không có')+'. Những câu có kết luận bị bác bỏ về nội dung ở lần kiểm chứng cuối: '+(', '.join(map(str,diag['remaining_content_rejection_cases'])) or 'không có')+'. Các ID kết luận và lý do nằm trong JSON. Ở các lượt giữ một phần, các ý bị bác bỏ đã được loại khỏi câu trả lời cuối. Đây là chẩn đoán tại lần chạy, không coi mọi cờ một phần là thiếu văn bản nguồn.']
    lines += ['', 'Giá điện/nước thực tế của nhà trọ là dữ liệu chủ trọ cung cấp, có thể chưa có và hỏi sau. Không suy đoán giá và không phạt thiếu giá trong tin. Thống kê quảng cáo cục bộ không chứng minh mức phổ biến toàn Cần Thơ.', '',
        'Chi tiết nguyên văn, các điểm thiếu/khác và trace kiểm chứng từng kết luận nằm trong [báo cáo JSON]('+a.output_json.resolve().as_posix()+'). Các bản chấm phát triển v9–v14 không tham gia bảng so sánh này; hai bản trong bảng dùng cùng v15, có giữ mệnh đề qua xuống dòng Word.', '',
        'Corpus mới vẫn là thử riêng; xem [audit nguồn và dữ liệu]('+(a.output_json.parent/'legal_repair_audit_v16_20261006.json').resolve().as_posix()+') về hash dữ liệu đang dùng và nguồn Word.']
    a.output_md.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='cases'},ensure_ascii=False))


if __name__ == '__main__':
    main()
