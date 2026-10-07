"""Produce one current report with explicit quality/latency/usage limits."""
import hashlib
import json
import math
from pathlib import Path
import statistics
from collections import Counter
from telemetry_summary import summarize_calls

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / 'eval/reports'


def load(name):
    return json.loads((REPORTS / name).read_text(encoding='utf-8'))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def file_link(relative, label=None):
    path = ROOT / relative
    assert path.exists(), relative
    return f'[{label or path.name}](<{path.as_posix()}>)'


def stats(values):
    values = sorted(values)
    return dict(n=len(values), p50_ms=statistics.median(values), p95_ms=values[math.ceil(.95*len(values))-1]) if values else dict(n=0, p50_ms=None, p95_ms=None)


def main():
    cleanup = json.loads((ROOT / 'docs/report_cleanup_20261007.json').read_text(encoding='utf-8'))
    assert all(not (ROOT / c['file']).exists() for c in cleanup['deleted'])
    run_name = 'gemini_completion_36_final_v18_20261007.json'
    run = load(run_name)
    cases = run['cases']
    assert sorted(c['id'] for c in cases) == list(range(19, 39))+list(range(43, 59))
    assert all('answer' in c for c in cases) and not any(c.get('error') or c.get('error_type') for c in cases)
    benchmark = load('gemini_completion_load_v18_20261007.json')
    assert benchmark['completed']
    assert benchmark['pipeline_sha256'] == run['pipeline_sha256']
    assert len(benchmark['cases']) == 12 and not any(c.get('error_type') for c in benchmark['cases'])
    review = load('gemini_completion_36_final_v18_v15_20261007.json')
    assert review['run_sha256'] == digest(REPORTS / run_name)
    assert sorted(c['id'] for c in review['cases']) == sorted(c['id'] for c in cases)
    assert review['summary']['completed'] == 36
    audit = load('gemini_completion_source_audit_final_v18_20261007.json')
    assert audit['run_sha256'] == digest(REPORTS / run_name)
    activation = load('gemini_completion_activation_20261007.json')
    assert activation['activated'] and activation['pipeline_sha256'] == run['pipeline_sha256']
    http = load('gemini_completion_http_v2_20261007.json')
    assert http['passed'] and http['temporary_user_removed']
    live = load('gemini_completion_live_verification_20261007.json')
    assert live['pipeline_matches'] and live['api_healthy'] and live['http_smoke_passed']
    assert live['frontend_build_passed'] and live['new_warning_in_live_bundle'] and live['frontend_http_status'] == 200
    assert live['live_pipeline_sha256'] == run['pipeline_sha256']
    assert live['http_smoke_sha256'] == digest(REPORTS / 'gemini_completion_http_v2_20261007.json')
    latest_verdict = [next((s.get('status') for s in reversed(c.get('agent_trace', [])) if s.get('agent') == 'source_verification'), 'not_recorded') for c in cases]
    stages = {}
    calls = [call for c in cases for call in c.get('provider_calls', []) if call.get('request_kind') == 'model_call']
    for stage in sorted({c['agent'] for c in calls}):
        stages[stage] = stats([c['latency_ms'] for c in calls if c['agent'] == stage])
    result = dict(run=run_name, run_sha256=digest(REPORTS / run_name), pipeline_sha256=run['pipeline_sha256'],
        report_cleanup=dict(deleted=len(cleanup['deleted']), bytes_freed=sum(c['bytes'] for c in cleanup['deleted'])),
        completed=len(cases), errors=0, partial_ids=[c['id'] for c in cases if c.get('partial_answer')],
        complete_answers=sum(not c.get('no_answer') for c in cases),
        repair_cases=sum(any(s.get('repair') for s in c.get('agent_trace', []) if s.get('agent') == 'answer_synthesis') for c in cases),
        final_runtime_verification=dict(Counter(latest_verdict)),
        focused_answers=[dict(id=c['id'], partial=c['partial_answer'], degraded=c['degraded'],
            provider=c['generation_provider'], sources=len(c['sources']),
            full_service_latency_ms=c['full_service_latency_ms'], degraded_reasons=c['degraded_reasons'])
            for c in cases if c['id'] in (49, 50, 54)],
        full_service_latency=stats([c['full_service_latency_ms'] for c in cases]),
        stage_model_call_latency=stages, telemetry=summarize_calls(cases),
        model_calls_by_stage=dict(Counter(c['agent'] for c in calls)),
        v15_similarity=review['summary'], load_groups=benchmark['groups'],
        load_case_stability=[dict(id=i, requests=sum(c['id'] == i for c in benchmark['cases']),
            partial=sum(c['id'] == i and bool(c.get('partial_answer')) for c in benchmark['cases']))
            for i in sorted(set(c['id'] for c in benchmark['cases']))],
        benchmark_warmup_telemetry=summarize_calls([benchmark['warmup']]),
        runtime_warmup_telemetry=summarize_calls([run['warmup']]),
        configuration=run['configuration'], live_min_request_interval_seconds=live['production_min_request_interval_seconds'],
        http_smoke={k:v for k,v in http.items() if k != 'cases'},
        live_verification=live,
        http_cases=[{k:v for k,v in c.items() if k != 'response'} for c in http['cases']],
        focused_source_and_v15_audit=[dict(id=f['id'], source_review=f['source_review'],
            current_v15=next(c['comparison'] for c in review['cases'] if c['id'] == f['id']),
            disposition='Preserve frozen text-similarity score. Source scope, missing steps, illustration validity and fragment-selection anomalies require separate review; do not automatically upgrade labels.')
            for f in audit['focused_source_and_judge_audit']],
        method='Fresh retrieval, 36 questions at two concurrent requests with a separate visible warm-up; repeated load at one and three concurrent requests. Evaluation pacing is zero, live pacing five seconds. Not fixed-input A/B. Similarity is not legal correctness. Small load samples are not a production SLA.')
    (REPORTS / 'gemini_completion_summary_20261007.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    t = result['telemetry']
    lat = result['full_service_latency']
    lines = ['# Cập nhật nguồn và kiểm tra Gemini — 07/10/2026', '',
        f"Đã xóa {len(cleanup['deleted'])} báo cáo pilot/kiểm tra HTTP cũ không còn được tham chiếu, giữ dữ liệu nguồn, đáp án gốc, các lượt đầy đủ và báo cáo mới. {file_link('docs/report_cleanup_20261007.json', 'Danh sách và hàm băm các tệp đã xóa')}.", '',
        '## Câu 49 và 50', '',
        'Câu 49: bổ sung nguyên văn Word từ Công báo: Điều 12, 13 của Luật 122/2025/QH15 và Điều 14, 22 của Nghị định 248/2026/NĐ-CP. Điều 15, 17 của luật đã có trong kho trước đó; lỗi còn nằm ở việc không truy xuất dẫn chiếu sang luật. Đã sửa truy xuất và giữ trích dẫn riêng cho từng văn bản, bổ sung điều khoản phụ thuộc sau lựa chọn. Kho mới `legal_word_completion_v18_20261007` có 40 tài liệu, 497 đoạn, 497 vector E5 thật 384 chiều; đã đối chiếu hàm băm, bản Word, liên kết và giữ kho v16.', '',
        'Nguồn chính thống: [Luật Thương mại điện tử](https://vanban.chinhphu.vn/?docid=216503&pageid=27160), [Nghị định 248](https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-248-2026-nd-cp-469983.htm). Giới hạn tám nguồn thay giới hạn năm để hiển thị đủ văn bản và điều khoản thi hành.', '',
        'Câu 50: cảnh báo mới là “Các dấu hiệu này giúp nhận diện rủi ro; cần kiểm tra liên kết và giao dịch cụ thể để kết luận.” Vẫn giữ phạm vi khuyến cáo của từng nhà cung cấp/cơ quan và loại bỏ ý không được kiểm chứng. Trong lượt 36 câu, câu 49 đã được đánh dấu đủ căn cứ; câu 50 vẫn partial do kiểm tra bao phủ và nhận diện cụm từ thận trọng. Cảnh báo mới đã hiện qua HTTP, nhưng chưa coi việc đổi câu cảnh báo là giải quyết mọi nhãn partial. Nhãn trên giao diện đổi thành “Câu trả lời còn giới hạn; hãy đọc lưu ý và đối chiếu nguồn.” để không gọi nhầm câu trả lời Gemini một phần là phương án dự phòng.', '',
        '## Bước 4: nguồn và bộ chấm', '',
        'Giữ nguyên đáp án và bộ chấm V15. Rà riêng câu 24: tỷ lệ 3/4 có điều kiện kê khai; không coi phép tính 37,5 kWh hoặc bảng bậc cũ là chuẩn pháp lý khi chưa xác minh biểu giá và mốc hiệu lực riêng. Rà câu 30: thao tác tra cứu phải gắn đúng nhà cung cấp trên hóa đơn; thêm giới hạn đó không chứng minh trả lời sai nguồn. Các nhãn khác mẫu được ghi riêng để rà lại, không tự nâng điểm. Các ý còn pending trong bộ tham chiếu chưa được chứng nhận là đáp án chuẩn.', '',
        'Nguồn đối chiếu: [Thông tư 60](https://vanban.chinhphu.vn/?docid=216125&orggroupid=4&pageid=27160), [hướng dẫn CANTHOWASSCO](https://hddt.ctn-cantho.com.vn/huong-dan). '+file_link('eval/reports/gemini_completion_source_audit_final_v18_20261007.json', 'Kết quả rà nguồn')+'; '+file_link('eval/reports/gemini_completion_36_final_v18_v15_20261007.json', 'đối chiếu V15')+'.', '',
        '## Bước 5: đo lại', '',
        f"Đủ {len(cases)}/36 yêu cầu hoàn thành, không lỗi thu thập. {result['complete_answers']} câu trả lời đầy đủ theo kiểm tra thời điểm chạy; {len(result['partial_ids'])} câu có giới hạn. Không diễn giải số yêu cầu hoàn thành thành tỷ lệ đúng pháp luật.", '',
        f"Thời gian toàn dịch vụ p50 {lat['p50_ms']/1000:.2f}s, p95 {lat['p95_ms']/1000:.2f}s. Bao gồm phân tích, E5, truy xuất, chọn nguồn, viết, kiểm chứng, sửa và tạo phản hồi; chưa gồm HTTP/xác thực. Lượt 36 câu chạy với hai yêu cầu đồng thời; warm-up và token của nó lưu riêng. Có tác vụ xây ứng dụng cùng lúc nên không coi đây là phép đo hiệu năng độc lập. Không so trực tiếp với thời gian replay chọn nguồn của A/B cũ.", '',
        f"Ghi nhận {t['model_calls']} lần gọi mô hình, {t['http_requests']} yêu cầu HTTP, {t['model_call_errors']} lỗi gọi mô hình, {t['http_errors']} lỗi HTTP. Token được trả về: {t['total_tokens']}; mức đầy đủ: {t['usage_coverage_calls']}/{t['model_calls']} lần gọi có usage. Warm-up của lượt 36 câu ghi riêng {result['runtime_warmup_telemetry']['total_tokens']} token, không cộng vào số trên. Số thiếu là chưa biết, không phải 0; không tính lặp wrapper và không suy đoán chi phí.", '',
        'Số lần gọi mô hình theo bước: '+ '; '.join(f"{k}: {v}" for k,v in result['model_calls_by_stage'].items())+'. Gồm các lượt sửa trong giới hạn; không chỉ đo bước viết câu trả lời.', '',
        'Đo lặp hai lần mỗi câu 49/50/54, ở mức một và ba yêu cầu đồng thời; warm-up lưu riêng. Khoảng cách tối thiểu giữa các lần gọi Gemini trong phép đo là 0 giây; API đang dùng 5 giây. Đây là mẫu tải nhỏ, chưa xác lập SLA:', '',
        '| Yêu cầu đồng thời | Mẫu | p50 | p95 | Lỗi | Trả lời một phần |', '|---:|---:|---:|---:|---:|---:|']
    for g in benchmark['groups']:
        lines.append(f"| {g['workers']} | {g['requests']} | {g['p50_ms']/1000:.2f}s | {g['p95_ms']/1000:.2f}s | {g['errors']} | {g['partial']} |")
    lines += ['', 'Độ ổn định theo câu: '+ '; '.join(f"câu {s['id']}: {s['partial']}/{s['requests']} lượt partial" for s in result['load_case_stability'])+'. Có thêm nguồn không bảo đảm mọi lượt sinh đều đủ ý.', '',
        'Các nhãn V15: `'+json.dumps(review['summary'].get('agreement'), ensure_ascii=False)+'`. Đây là độ giống mẫu, không phải tỷ lệ đúng pháp luật.', '',
        '252 kiểm thử pipeline và báo cáo đạt; 126 kiểm thử liên quan cũng đạt trong ảnh ứng dụng mới. Đã kích hoạt kho v18, API khỏe và kiểm tra HTTP đạt cho câu 49, 50 cùng tìm phòng. Tài khoản thử đã được xóa. Các chỉ số HTTP lưu riêng với thời gian dịch vụ. Hàm băm của lượt chạy và dữ liệu nguồn được lưu trong báo cáo JSON. Không sửa đáp án để tăng điểm.', '',
        file_link('eval/reports/legal_selector_ab_v2_usage_correction_20261007.json', 'Bản đính chính usage Gemini của A/B cũ')+' — 710.843 token Gemini ghi nhận ở nhánh chọn nguồn Qwen (viết/kiểm chứng) và 793.987 ở nhánh chọn nguồn Gemini; bốn lần lỗi Gemini không có usage. Không coi đây là tổng token của cả Qwen và Gemini hoặc tổng toàn luồng phân tích câu hỏi. Báo cáo gốc giữ nguyên.', '',
        'Tệp kết quả chính: '+', '.join(file_link('eval/reports/'+name, label) for name,label in [('gemini_completion_36_final_v18_20261007.json','lượt chạy 36 câu'),('gemini_completion_load_v18_20261007.json','đo tải lặp'),('gemini_completion_summary_20261007.json','tổng hợp số liệu')])+'.']
    (ROOT / 'docs/GEMINI_COMPLETION_20261007.md').write_text('\n'.join(lines)+'\n', encoding='utf-8')
    print(json.dumps({k: result[k] for k in ('completed', 'errors', 'partial_ids', 'full_service_latency', 'telemetry')}, ensure_ascii=False))


if __name__ == '__main__':
    main()
