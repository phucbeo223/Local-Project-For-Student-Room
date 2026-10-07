"""Evidence-backed handover; keep runtime completeness apart from agreement."""
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from telemetry_summary import summarize_calls

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT/'eval/reports'


def read(name):
    return json.loads((REPORTS/name).read_text(encoding='utf-8'))


def label(case):
    return case['comparison']['agreement'] if case.get('comparison') else 'unscored'


def trace(case, name):
    return next((t for t in reversed(case.get('agent_trace',[])) if t.get('agent')==name), {})


def count_labels(cases):
    counts = Counter(label(c) for c in cases)
    return {k:counts[k] for k in ('high','partial','low','unscored')}


def main():
    baseline = read('gemini_completion_36_final_v18_20261007.json')
    historical = read('gemini_completion_36_final_v18_v15_20261007.json')
    old = read('gemini_workflow_v19_old_scored_v18_20261007.json')
    new = read('gemini_workflow_v19_new_scored_v18_20261007.json')
    run = read('gemini_workflow_v19_36_20261007.json')
    repeats = read('gemini_workflow_v19_repeats_20261007.json')
    paraphrases = read('gemini_workflow_v19_paraphrases_20261007.json')
    repeat_scores = [read(f'gemini_workflow_v19_repeat_r{r}_scored_v18_20261007.json') for r in (1,2,3)]
    http = read('gemini_workflow_v19_http_20261007.json')
    corpus = read('legal_workflow_v19_corpus_audit_20261007.json')
    protected = read('gemini_workflow_v19_runtime_after_20261007.json')
    before = read('gemini_workflow_v19_before_20261007.json')
    for report in (old,new,run,repeats,paraphrases,*repeat_scores):
        assert report['completed'], 'Never publish unfinished runs as passes'
    assert len(run['cases'])==len(old['cases'])==len(new['cases'])==36
    assert all(old[k]==new[k] for k in ('policy','judge_model','scorer_sha256','fragment_code_sha256','quantity_audit_sha256','reference_sha256','reference_audit_sha256'))
    assert run['pipeline_sha256']==repeats['pipeline_sha256']==paraphrases['pipeline_sha256']==protected['pipeline_sha256']
    assert http['passed'] and corpus['passed'] and protected['protected_tables_unchanged']
    h, b, o, n, runtime = [{c['id']:c for c in r['cases']} for r in (historical,baseline,old,new,run)]
    rows = []
    for qid in sorted(runtime):
        current = runtime[qid]
        sc, asc, selected = trace(current,'source_coverage'),trace(current,'answer_coverage'),trace(current,'selected_source_coverage')
        score = n[qid]
        rows.append(dict(id=qid, question=current['question'], historical_v15=label(h[qid]),
            old_same_gemini_evaluator=label(o[qid]), new_same_gemini_evaluator=label(score),
            runtime_before='partial' if b[qid].get('partial_answer') else 'complete',
            runtime_after=current.get('content_completeness'),
            source_coverage=sc, selected_source_coverage=selected, answer_coverage=asc,
            source_missing=sc.get('missing_facets',[]), selected_source_missing=selected.get('missing_facets',[]),
            answer_missing=asc.get('missing_facets',[]), completion_reasons=current.get('completion_reasons',[]),
            provenance_status=current.get('provenance_status'), application_status=current.get('application_status'),
            repair_count=sum(bool(t.get('repair')) for t in current.get('agent_trace',[])),
            full_service_latency_ms=current['full_service_latency_ms'], telemetry=summarize_calls([current]),
            reference_differences=[p for p in (score.get('comparison') or {}).get('points',[]) if p['status']!='matched'],
            reference_review=score.get('reference_review'), judge_errors=score.get('judge_errors'),
            judge_attempt_count=score.get('attempt_count'), verified_against_selected_sources=current.get('citation_accuracy'),
            source_verification=trace(current,'source_verification'), rule_checks=trace(current,'citation_and_rule_checks')))
    stability = []
    for qid in repeats['selected_ids']:
        samples = sorted([c for c in repeats['cases'] if c['id']==qid],key=lambda c:c['repeat'])
        assert len(samples)==3
        labels = [label(next(c for c in r['cases'] if c['id']==qid)) for r in repeat_scores]
        stability.append(dict(id=qid, labels=labels, labels_stable=len(set(labels))==1 and 'unscored' not in labels,
            runtime=[c.get('content_completeness') for c in samples],
            repair_count=[sum(bool(t.get('repair')) for t in c.get('agent_trace',[])) for c in samples],
            full_service_latency_ms=[c['full_service_latency_ms'] for c in samples]))
    generation_runs = [run,repeats,paraphrases]
    generation = summarize_calls([c for r in generation_runs for c in r['cases']])
    warmups = summarize_calls([r['warmup'] for r in generation_runs])
    judging = summarize_calls([c for r in [old,new,*repeat_scores] for c in r['cases']])
    calls = [call for r in [*generation_runs,old,new,*repeat_scores] for c in r['cases'] for call in c.get('provider_calls',[])]
    assert calls and all(c['provider']=='gemini' and c['model'].startswith('gemini-') for c in calls)
    historical_hashes = {}
    for target, original in [('eval/compare_grounded_references_v15.py','eval/compare_grounded_references.py'),
        ('eval/reports/gemini_completion_36_final_v18_20261007.json','eval/reports/gemini_completion_36_final_v18_20261007.json'),
        ('eval/reports/gemini_completion_36_final_v18_v15_20261007.json','eval/reports/gemini_completion_36_final_v18_v15_20261007.json')]:
        actual = hashlib.sha256((ROOT/target).read_bytes()).hexdigest()
        assert actual==before['files'][original.replace('/','\\')]
        historical_hashes[target] = actual
    changed = [path for path,digest in before['files'].items() if (ROOT/path).exists() and hashlib.sha256((ROOT/path).read_bytes()).hexdigest()!=digest]
    report = dict(completed_at_utc=datetime.now(timezone.utc).isoformat(), policy=old['policy'],
        summaries=dict(historical_v15=count_labels(historical['cases']),old_same_evaluator=count_labels(old['cases']),
            new_same_evaluator=count_labels(new['cases']), runtime_before=dict(Counter(r['runtime_before'] for r in rows)),
            runtime_after=dict(Counter(r['runtime_after'] for r in rows))),
        model_calls_gemini_only=True, generation_telemetry=generation, warmup_telemetry=warmups, judging_telemetry=judging,
        hashes=dict(pipeline=run['pipeline_sha256'],corpus_manifest=run['corpus_manifest_sha256'],
                    scorer=old['scorer_sha256'],fragments=old['fragment_code_sha256'],quantity_audit=old['quantity_audit_sha256'],
                    references=old['reference_sha256'],reference_audit=old['reference_audit_sha256']),
        historical_hashes_preserved=historical_hashes,configuration_before=baseline['configuration'], configuration_after=run['configuration'],
        protected_tables=protected, http_smoke=http, corpus_audit=corpus, changed_since_entry_snapshot=changed,
        cases=rows, stability=stability,
        paraphrases=[dict(id=c['id'],question=c['question'],content_completeness=c['content_completeness'],
            source_coverage=trace(c,'selected_source_coverage'),answer_coverage=trace(c,'answer_coverage'),
            completion_reasons=c.get('completion_reasons',[])) for c in paraphrases['cases']],
        caveats=['Reference agreement is not legal accuracy; references contain unverified claims.',
                 'No reduction in total LOW or increase in HIGH is demonstrated by the same-evaluator comparison.',
                 'Supplementary retrieval checks its 15-second launch budget between queries, not a hard cancellation of an in-flight database statement.',
                 'Lexical facets can report coverage for a general clause without proving detailed annex classification; semantic verification remains separate.',
                 'A phrasing about using electricity without the token tiền điện was misrouted to listing; the tested legal paraphrase names tiền điện explicitly.',
                 'Only local containers were updated. New corpus remains staging in the release catalog and is selected explicitly by the overlay.',
                 'HTTP model-call totals are unavailable; complete per-call usage is measured in the independent in-process runs.'])
    (REPORTS/'gemini_workflow_v19_comparison_20261007.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    text = ['# Bàn giao workflow Gemini — 07/10/2026','',
        'Đã sửa mã, chạy đủ 36 câu, 27 lượt lặp, 6 cách hỏi ngoài bộ mẫu và cập nhật API/web cục bộ. Chưa đạt mục tiêu giảm LOW tổng thể hoặc tăng HIGH. Không công bố 0 LOW.','',
        '## Kết quả và cách đọc','',
        '| Phép đo | HIGH | PARTIAL | LOW | unscored |','|---|---:|---:|---:|---:|',
        '| Lịch sử V15, giữ nguyên | 8 | 25 | 3 | 0 |']
    for title, cases in [('Đầu ra cũ / Gemini V18',old['cases']),('Đầu ra mới / Gemini V18',new['cases'])]:
        counts = count_labels(cases)
        text.append('| '+title+' | '+' | '.join(str(counts[k]) for k in ('high','partial','low','unscored'))+' |')
    text += ['', 'Trạng thái dịch vụ: **14 complete / 22 partial → 18 complete / 18 partial**. Nhãn đủ nội dung từ pipeline khác với mức khớp mẫu. Cả hai lượt chấm V18 dùng cùng model, hash bộ chấm, bộ tách, kiểm tra định lượng và tham chiếu. Không dùng chênh lệch V15–V18 để kết luận chatbot tốt hơn.', '',
        'V17 được lưu riêng: quy tắc “không có matched ⇒ LOW” đã hạ nhãn PARTIAL do mô hình chọn, kể cả khi trả lời được ý chính. V18 bỏ phép ép nhãn này và kiểm tra nhãn tổng thể bằng lượt Gemini độc lập. HIGH vẫn yêu cầu mọi ý matched; bất nhất được thử tối đa ba lần rồi unscored. V18 có 3 lỗi giải mã trên đầu ra cũ Q32/Q36/Q47; tất cả 36 đầu ra mới chấm được. Raw output và từng lần thử đều còn trong JSON.', '',
        '## Những sửa đổi có bằng chứng','',
        '- Bộ tách giữ mệnh đề kết thúc bằng dấu hai chấm, số liệu, điều kiện cha và danh sách lồng nhau; lưu nguyên văn, ID và offset. Chỉ bỏ tiêu đề thuần túy. Không có quy tắc theo ID Q24.',
        '- Tái dựng nguyên bộ ánh xạ V15 của Q19/Q36/Q47 cho cùng các điểm/quote/giải thích đã lưu. Lời giải thích lệch chủ đề nằm trong đầu ra chọn fragment; chưa có bằng chứng ứng dụng đổi nhầm ID. Kiểm tra quote tồn tại không phát hiện lỗi ngữ nghĩa này. Xem `gemini_workflow_v19_reproductions_20261007.json`.',
        '- Bộ chấm Gemini tách khỏi sinh, kiểm tra ngữ nghĩa từng ý và nhãn tổng thể, đọc toàn bộ đáp án, giữ raw output, ID và phản hồi thử lại. V15 và hai báo cáo baseline khớp hash ban đầu.',
        '- Yêu cầu bao phủ lấy từ câu hỏi; kiểm tra riêng nguồn trước chọn, nguồn sau chọn và câu trả lời theo nguồn đã dẫn. Rỗng trả not_evaluated. Bổ sung điện, nước, cư trú, PCCC, tin đăng, liên kết đặt cọc và chứng cứ. Một vòng truy xuất bổ sung: tối đa hai truy vấn, tám nguồn, ngân sách khởi chạy 15 giây, không gọi mô hình thêm.',
        '- Giữ các ý đã kiểm chứng khi sửa phần thiếu. Trạng thái có cấu trúc đi từ chọn nguồn/sinh/kiểm chứng đến API; cảnh báo xuất xứ không tự đổi complete sang partial. Nội dung thiếu hoặc điều kiện quyết định chưa rõ vẫn partial. Giao diện vẫn hiển thị cảnh báo.',
        '- Bổ sung Word chính thức Thông tư 60/2025/TT-BCT và Nghị định 105/2025/NĐ-CP, giữ URL, hash, ngày hiệu lực, phạm vi và offset. Không PDF/OCR. Phụ lục dài có phép chọn nguyên hàng và giữ tiêu đề/cột, không cắt giữa điều kiện.',
        '- Sửa lỗi quy tắc từ chối Điều 19 được dẫn chiếu trong nguồn Q54; không mặc định tiêu đề Điều 10 cấm dẫn Điều 19. Sửa câu phủ định “không phải danh mục hồ sơ bắt buộc” Q56; vẫn từ chối nếu cùng câu tự thêm nghĩa vụ. Q45 đã có xử lý phủ định trong workspace trước khi sửa; không áp thêm ngoại lệ khi chưa tái hiện lỗi hiện tại.',
        '- Router không tạo Qwen/Ollama và từ chối cấu hình Qwen. Các mặc định Compose, biến provider/judge trong `.env` và `.env.example` chuyển Gemini. Nhánh tìm phòng dùng mẫu theo dữ liệu local. Các lớp/tệp lịch sử không được gọi trong workflow đo.', '',
        '## Bảng từng câu','',
        '| Câu | V15 lịch sử | Cũ / Gemini V18 | Mới / Gemini V18 | Dịch vụ cũ → mới | Bao phủ nguồn / trả lời | Lượt sửa |',
        '|---|---|---|---|---|---|---:|']
    for row in rows:
        text.append(f"| Q{row['id']} | {row['historical_v15'].upper()} | {row['old_same_gemini_evaluator'].upper()} | {row['new_same_gemini_evaluator'].upper()} | {row['runtime_before']} → {row['runtime_after']} | {row['selected_source_coverage'].get('status','not_evaluated')} / {row['answer_coverage'].get('status','not_evaluated')} | {row['repair_count']} |")
    text += ['', 'JSON `gemini_workflow_v19_comparison_20261007.json` chứa cho từng câu: ý thiếu ở nguồn/chọn nguồn/trả lời, các khác biệt tham chiếu kèm giải thích, giới hạn áp dụng, lỗi quy tắc, số lần sửa/chấm, độ trễ và token thực tế.', '',
        '## Các câu ưu tiên và phần còn thiếu','',
        '- **Q24:** đã giữ 3/4 định mức cùng điều kiện kê khai, kỳ/hợp đồng, hóa đơn và hiệu lực có điều kiện. Không thêm 37,5 kWh hay biểu giá cũ để giống mẫu. Chưa xác nhận sự kiện kích hoạt điểm c khoản 5 Điều 12: PARTIAL có lý do.',
        '- **Q28:** trả lời đủ sáu mục mức khoán, số người, kỳ thu, khoản bao gồm, thay đổi và hóa đơn; gắn nhãn khuyến nghị/thỏa thuận. Không dựng khoảng tiền “phổ biến” hoặc ngưỡng trái luật. Còn cần địa bàn/nhà cung cấp và hiệu lực biểu giá địa phương.',
        '- **Q36:** phân biệt nhà ở, kết hợp kinh doanh và cơ sở quản lý; trả lời điện, phương tiện, lối thoát và giải pháp ngăn cháy có nguồn. Không áp cứng hai lối thoát/hai bình mỗi tầng. Kho đã có phụ lục phân loại nhưng lượt sinh chính chưa chọn đủ hàng phân loại quy mô; câu trả lời còn thiếu phần này. Cảnh báo và câu hỏi thêm không được coi là đã hoàn thành phân loại.',
        '- **Q30/Q47/Q55:** complete ở dịch vụ, vẫn PARTIAL theo mẫu do chi tiết/khẳng định chưa trùng. **Q49:** còn phạm vi và điều kiện pháp luật mới. **Q52:** nguồn chọn cho nguyên tắc dữ liệu nhưng chưa đáp ứng ví dụ watermark/mục đích dùng bản chụp; LOW và không được bổ sung ví dụ vô căn cứ.',
        '- **Q31/Q33:** complete ở dịch vụ nhưng chưa khớp toàn mẫu. **Q32/Q34:** LOW do thiếu phần phối hợp chủ trọ, tình huống chuyển nơi ở/cùng phường và các điều kiện thủ tục; mức phạt hoặc mốc trong mẫu vẫn cần xác minh trước khi thêm.',
        '- **Q54:** lượt chính complete, bộ quy tắc chấp nhận các dẫn chiếu đúng; các lượt lặp vẫn LOW theo mẫu. **Q56:** giữ hướng dẫn chứng cứ/báo tin, không biến hướng dẫn thành hồ sơ bắt buộc; lượt chính và lặp PARTIAL theo mẫu.',
        '- **Nhóm 8 HIGH cũ:** Q20/Q22/Q37/Q38/Q43/Q48/Q50/Q58 đều PARTIAL trong lượt mới/V18; đầu ra cũ/V18 cũng PARTIAL, riêng Q43 LOW. Không tuyên bố giữ tám HIGH chỉ vì baseline V15 từng gán nhãn đó.', '',
        'Các LOW mới:']
    for c in sorted(new['cases'],key=lambda c:c['id']):
        if label(c)=='low':
            text.append(f"- **Q{c['id']}**: {c['comparison']['explanation']}")
    text += ['', 'Đây là lý do khớp tham chiếu, không xác nhận mọi khẳng định/định mức/thời hạn trong mẫu là pháp luật hiện hành. Giữ bản rà tham chiếu tại từng case; không sao chép các khẳng định chưa xác minh vào corpus hoặc prompt sinh.', '',
        '## Ba lượt lặp','', '| Câu | Lần 1 | Lần 2 | Lần 3 | Trạng thái dịch vụ |', '|---|---|---|---|---|']
    for row in stability:
        text.append(f"| Q{row['id']} | {' | '.join(v.upper() for v in row['labels'])} | {' / '.join(row['runtime'])} |")
    text += ['', '27/27 lượt sinh hoàn thành, không lỗi. Có unscored ở một lượt Q24 và hai lượt Q52 do đầu ra chấm không đạt kiểm tra; không tính là đạt. Q45/Q52/Q54 có nhãn thấp hoặc dao động. Cả ba câu LOW cũ chưa được chứng minh ổn định HIGH. Sáu cách hỏi ngoài mẫu đều chạy được, đều PARTIAL; không có đáp án mẫu đưa vào bước sinh.', '',
        '## Độ trễ, usage và kiểm thử','',
        '| Nhóm sinh | Số lượt | p50 | p95 | Lỗi | Model calls | Total tokens API trả về |', '|---|---:|---:|---:|---:|---:|---:|']
    for title,r in [('36 câu',run),('27 lượt lặp',repeats),('6 câu ngoài mẫu',paraphrases)]:
        g = r['groups'][0]
        text.append(f"| {title} | {g['requests']} | {g['p50_ms']/1000:.2f}s | {g['p95_ms']/1000:.2f}s | {g['errors']} | {g['telemetry']['model_calls']} | {g['telemetry']['total_tokens']} |")
    text += ['', f"Tổng sinh trong các nhóm: **{generation['model_calls']} model calls, {generation['total_tokens']:,} total tokens**. Warm-up tách riêng: **{warmups['model_calls']} calls, {warmups['total_tokens']:,} tokens**. Chấm so sánh V18 và lặp: **{judging['model_calls']} calls, {judging['total_tokens']:,} tokens**. Mỗi lượt được đối chiếu usage response, không dùng 0 thay cho thiếu. Lượt V17/pilot là chi phí bổ sung, không trộn vào phép so sánh V18.", '',
        'Cùng model `gemini-3.8-flash-high` cho các bước và chấm. Lượt cũ đặt khoảng nghỉ 0 giây, lượt mới 5 giây; vì vậy không diễn giải chênh lệch độ trễ thành hiệu năng mã thuần. Benchmark đo toàn service, không gồm HTTP/auth; smoke HTTP được lưu riêng và không có telemetry model đầy đủ. Toàn bộ model-call log của các lượt mới/chấm có provider Gemini, không có Qwen/Ollama.', '',
        '- 134 kiểm thử liên quan đã qua theo các lượt kiểm tra: bộ tách/ngữ nghĩa/gom nhãn, bao phủ, điều kiện/citation, selector/workflow, nguồn và telemetry; 25 kiểm thử truy xuất cũng đã qua khi dùng thư mục tạm trong workspace.',
        '- Kiểm tra TypeScript qua; build API và web production qua.',
        '- 5 Playwright UI tests qua, bao gồm điện thoại 390px, desktop 1280px, nguồn, cảnh báo và nội dung dài.',
        '- Smoke HTTP Q20/Q24/Q28/Q36 và tìm phòng đều 200/pass; không xác thực bị chặn; tài khoản thử đã xóa.',
        '- Corpus audit qua: 42 Word, 583 đoạn/vector 384 chiều, nguyên văn official Word khớp offset; graph release khớp manifest. Dữ liệu 84 người dùng và 789 tin trọ giữ nguyên digest trước/sau cập nhật.', '',
        '## Phiên bản, cấu hình và tệp bàn giao','',
        f"- Pipeline/prompt hash: `{run['pipeline_sha256']}`.",
        f"- Corpus manifest hash: `{run['corpus_manifest_sha256']}`.",
        f"- Gemini evaluator V18 hash: `{old['scorer_sha256']}`.",
        '- API local đã chạy `nckh-api:workflow-v19`, web `nckh-web:workflow-v19`; hash mã trong API khớp lượt đo. Overlay `docker-compose.workflow-v19.yml` chọn rõ legal/graph/housing schema mới. Release mới vẫn staging trong catalog; không thay hay xóa các release trước.',
        '- Ảnh khôi phục: `nckh-api:before-workflow-v19-20261007`, `nckh-web:before-workflow-v19-20261007` cùng các corpus cũ. API trước cập nhật thực tế dùng Qwen và Word V7; đó khác với baseline V18 được cung cấp để so sánh chất lượng.',
        '- Các file API sửa từ snapshot ban đầu: '+', '.join('`'+p.replace('\\','/')+'`' for p in changed if p.startswith('apps'))+'.',
        '- Thêm `annex_context.py`; cập nhật config/provider mặc định, `ChatClient.tsx`, kiểm thử UI/API/evaluator; thêm scorer Gemini, corpus fetch/prepare/audit, benchmark/split/reproduction/report/HTTP scripts. JSON bàn giao chứa danh sách thay đổi và hash; không coi toàn bộ `git diff` là công việc mới vì workspace đã có thay đổi trước đó.', '',
        '## Giới hạn còn lại','',
        '- Chưa có kết quả cho phép công bố giảm LOW tổng thể, tăng HIGH hoặc hoàn tất các câu PARTIAL. Một số mẫu đòi khẳng định/định lượng chưa xác minh; tăng điểm bằng cách viết theo mẫu sẽ không giải quyết đúng nguồn.',
        '- Cần tăng khả năng chọn đúng hàng phụ lục PCCC, bổ sung nguồn thực cho chuyển cư trú/báo tin/watermark và kiểm tra lại từng LOW với tham chiếu đã xác minh.',
        '- Bao phủ hiện là kiểm tra từ vựng có ràng buộc nguồn/citation, không phải chứng nhận đã đủ mọi điều kiện pháp lý. Ngân sách 15 giây kiểm tra giữa truy vấn, chưa hủy cưỡng bức truy vấn DB đang chạy.',
        '- Một cách hỏi về kê khai “dùng điện” thiếu từ “tiền điện” đã bị router hiểu là tìm phòng; bộ hỏi ngoài mẫu dùng cách gọi “tiền điện”. Lỗi phân loại này còn cần xử lý và đo lại riêng.', '',
        'Nguồn bổ sung: [Thông tư 60/2025/TT-BCT, Word Công báo](https://congbao.chinhphu.vn/van-ban/thong-tu-so-60-2025-tt-bct-46756/60185.htm), [Nghị định 105/2025/NĐ-CP, Word Công báo](https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-105-2025-nd-cp-44912/56374.htm). URL download, ngày tải, TLS, hash và phạm vi lưu trong `docs/legal_word_workflow_v19_20261007/originals/provenance.json`.', '']
    (REPORTS/'gemini_workflow_v19_comparison_20261007.md').write_text('\n'.join(text),encoding='utf-8')
    print(json.dumps(report['summaries']),flush=True)


if __name__=='__main__':
    main()
