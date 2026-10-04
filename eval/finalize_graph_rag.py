"""Produce a local reviewable report and integrity gates after all tests finish."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from urllib.parse import urlparse, quote
import httpx
from sqlalchemy import create_engine, text
from app.config import settings
import question_bank_ragas as bank


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', type=Path, required=True)
    parser.add_argument('--audit', type=Path, required=True)
    parser.add_argument('--comparison', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--index', type=Path, default=Path('/eval/reports/graph_rag_index_2026-10-04.json'))
    parser.add_argument('--housing-http',type=Path,default=Path('/eval/reports/graph_rag_http_2026-10-04.json'))
    parser.add_argument('--legal-http',type=Path,default=Path('/eval/reports/graph_rag_legal_http_2026-10-04.json'))
    parser.add_argument('--legal-index',type=Path)
    parser.add_argument('--comparison-run',type=Path)
    parser.add_argument('--primary-release',type=Path)
    parser.add_argument('--source-manifest',type=Path)
    parser.add_argument('--comparison-review',type=Path,help='Bound text-level review notes; raw judge labels are preserved')
    args = parser.parse_args()
    run, audit, comparison = read(args.run), read(args.audit), read(args.comparison)
    index = read(args.index)
    housing_http = read(args.housing_http)
    legal_http = read(args.legal_http)
    comparison_run = read(args.comparison_run) if args.comparison_run else run
    review=read(args.comparison_review) if args.comparison_review else None
    review_cases={case['id']:case for case in review['cases']} if review else {}
    reference_path = '/eval/datasets/external_legal_20261004/answers.json'
    references = {case['original_question_id']: case for case in read(reference_path)['cases']}
    expected_comparison = sorted(case['id'] for case in comparison_run['cases'] if case['id'] in references)
    pipeline = Path('/workspace/apps/api/app/room_service/chatbot')
    current_pipeline = hashlib.sha256(b''.join(p.name.encode() + p.read_bytes() for p in sorted(pipeline.glob('*.py')))).hexdigest()
    engine = create_engine(settings.database_url)
    with engine.connect() as conn:
        graph_release = dict(conn.execute(text(f'SELECT * FROM {settings.chatbot_graph_schema}.release WHERE id=1')).mappings().one())
        housing = dict(conn.execute(text('SELECT count(*) AS rows,count(embedding_vector) AS vectors, '
            'min(vector_dims(embedding_vector)) AS min_dims,max(vector_dims(embedding_vector)) AS max_dims '
            f'FROM {settings.chatbot_listing_schema}.aggregated_listings')).mappings().one())
        legal = dict(conn.execute(text('SELECT count(*) AS chunks,count(embedding_vector) AS vectors '
            f'FROM {settings.chatbot_legal_schema}.legal_chunks')).mappings().one())
        graph = dict(conn.execute(text(f'SELECT (SELECT count(*) FROM {settings.chatbot_graph_schema}.nodes) AS nodes,'
            f'(SELECT count(*) FROM {settings.chatbot_graph_schema}.edges) AS edges')).mappings().one())
        if args.primary_release:
            primary = read(args.primary_release)
            primary_live = dict(conn.execute(text("SELECT count(*) AS rows,count(embedding_vector) AS vectors,md5(string_agg(row_to_json(t)::text,'|' ORDER BY id)) AS digest FROM public.aggregated_listings t")).mappings().one())
            obsolete_gone = all(conn.execute(text('SELECT to_regnamespace(:schema)'), {'schema':s}).scalar_one() is None
                                for s in primary.get('retired_housing_schemas',('graph_rag_v1','housing_graph_v1','housing_v2')))
    engine.dispose()
    health = httpx.get('http://api:8000/health/deps', timeout=10)
    failed_provider_calls = [call for case in run['cases'] for call in case.get('provider_calls', []) if call.get('success') is False]
    gates = {
        'all_56_completed': len(run['cases']) == 56 and [case['id'] for case in run['cases']] == list(range(1, 57))
                            and all(case.get('answer') and not case.get('error') for case in run['cases']),
        'same_generation_pipeline': current_pipeline == run['pipeline_sha256'],
        'graph_enabled': run['graph_enabled'] is True,
        'same_graph_release': graph_release['housing_sha256'] == run['housing_catalog_sha256'] == index['housing_sha256']
                              and graph_release['legal_sha256'] == run['legal_manifest_sha256'] == index['legal_sha256']
                              and graph_release['extractor_version'] == run['graph_extractor_version'],
        'complete_real_embeddings': housing['rows'] == housing['vectors'] == 789
                                    and housing['min_dims'] == housing['max_dims'] == 384
                                    and legal['chunks'] == legal['vectors'] == (read(args.legal_index)['counts']['vectors'] if args.legal_index else 1732),
        'same_graph_counts': graph['nodes'] == index['counts']['nodes'] and graph['edges'] == index['counts']['edges'],
        'housing_constraints': audit['phase'] == 'final' and audit['summary']['housing_constraint_violations'] == 0,
        'protected_public_full_rows': audit['summary']['protected_public_full_rows_unchanged'],
        'audit_input_unchanged': audit['run_sha256'] == sha(args.run),
        'local_housing_only': run['graph_summary']['cloud_housing_calls'] == 0,
        'comparison_complete': sorted(case['id'] for case in comparison['cases']) == expected_comparison
                               and all(case.get('comparison') for case in comparison['cases']),
        'comparison_input_unchanged': comparison['run_sha256'] == sha(args.comparison_run or args.run) and comparison['reference_sha256'] == sha(reference_path)
                                      and comparison_run['pipeline_sha256'] == run['pipeline_sha256']
                                      and all(next(c for c in comparison_run['cases'] if c['id']==case['id'])['answer']==case['answer'] for case in run['cases']),
        'comparison_local': comparison['judge_provider'] == 'ollama-local',
        'housing_http': housing_http['passed'] and housing_http['temporary_user_removed'],
        'legal_http': legal_http['passed'] and legal_http['temporary_user_removed']
                      and legal_http['response']['retrieval_mode'].startswith('legal_graph_'),
        'dependencies_healthy': health.status_code == 200 and all(health.json().get(key) == 'ok' for key in ('postgres', 'redis', 'pgvector')),
    }
    if args.primary_release:
        gates.update(primary_is_datahouse=primary_live == primary['public_after'] and primary['public_after']['rows']==789,
                     obsolete_housing_removed=primary.get('retired') is True and obsolete_gone,
                     backup_restore_verified=primary['backup_restore_verified'])
    if args.source_manifest:
        manifest=read(args.source_manifest)
        originals=[]
        for entry in manifest['documents']:
            path=Path('/workspace')/entry['file'];data=read(path);source=data['source']
            originals.append(sha(path)==entry['sha256'] and sha(Path('/workspace')/source['path'])==source['sha256']
                             and all(sha(Path('/workspace')/origin['path'])==origin['sha256'] for origin in source.get('origin_documents',[]))
                             and source.get('page_kind')!='editorial_guidance' and not entry['id'].startswith(('guidance-','legacy-'))
                             and all(p.get('kind')!='editorial_guidance' and not p['heading'].startswith('Q:') for p in data['provisions']))
        gates['original_sources_only']=bool(originals) and all(originals)
        gates['same_source_manifest']=sha(args.source_manifest)==graph_release['legal_sha256']
    if args.comparison_run:
        gates['all_reference_answers_compared']={case['id'] for case in comparison['cases']}==set(references)
    if review:
        gates['comparison_review_bound']=review['comparison_sha256']==sha(args.comparison)
    report = {'created_at_utc': datetime.now(timezone.utc).isoformat(), 'passed': all(gates.values()), 'gates': gates,
        'run_sha256': sha(args.run), 'audit_sha256': sha(args.audit), 'comparison_sha256': sha(args.comparison),
        'pipeline_sha256': current_pipeline, 'counts': {'housing': housing, 'legal': legal, 'graph': graph},
        'summary': run['summary'], 'housing_summary': audit['summary'], 'reference_comparison': comparison['summary'],
        'provider_failures_recovered': dict(Counter(call.get('error_type') or 'unknown' for call in failed_provider_calls)),
        'interpretation': 'Completion/integrity gates; not verified accuracy, not readiness for production.'}
    if review:
        report['comparison_text_review']={'sha256':sha(args.comparison_review),'noted_ids':sorted(review_cases),
                                          'method':review['method'],'raw_labels_preserved':True}
    bank.save_report(args.output, report)
    comparison_cases = {case['id']: case for case in comparison['cases']}
    housing_checks = {case['id']: case for case in audit['housing_cases']}
    summary = run['summary']
    lines = ['# Graph RAG — kiểm thử 56 câu và đối chiếu đáp án', '',
        f"Hoàn thành **{summary['completed']}/56** câu, lỗi thực thi **{summary['errors']}**. Kiểm chứng hoàn tất: **{'ĐẠT' if report['passed'] else 'CẦN XỬ LÝ'}**.", '',
        f"Kho nhà trọ: 789 bản ghi/vector E5; graph: {graph['nodes']} nút, {graph['edges']} cạnh. Kho pháp lý: {legal['vectors']} vector.", '',
        f"Tìm phòng: **{audit['summary']['housing_with_results']}/18** câu có kết quả; **{audit['summary']['housing_constraint_violations']}** vi phạm bộ lọc trong trường trả về. Câu bị chặn dù còn bản ghi khớp: {audit['summary']['housing_abstentions_with_matching_records']}.", '',
        f"Đối chiếu {len(comparison['cases'])} câu có đáp án người dùng bằng Qwen cục bộ: {json.dumps(comparison['summary']['agreement'], ensure_ascii=False)}.", '',
        f"Các lỗi provider đã fallback: {json.dumps(report['provider_failures_recovered'])}. Trung vị toàn bộ đợt: {summary['latency_p50_ms']/1000:.2f} giây; p95: {summary['latency_p95_ms']/1000:.2f} giây.", '',
        '## Cách đọc kết quả', '',
        '- Bộ đã chạy là câu 1–56 trong bộ lưu 58 câu; câu 57–58 không thuộc đợt này.',
        '- Câu 15 sau 14; câu 16 sau 14,15; câu 17–18 độc lập sau 14, có cả lịch sử và conversation state.',
        '- Không vi phạm bộ lọc nghĩa là trường trả về khớp dữ liệu đã nhập; không xác minh quảng cáo, giá hay phòng còn trống.',
        '- Cờ no_answer ở pháp lý có thể đi cùng partial_answer và nội dung trả lời; không đồng nghĩa hoàn toàn không trả lời.',
        '- Nhãn high/partial/low đo khớp văn bản với tham chiếu chưa xác minh; không phải tỷ lệ đúng pháp luật. Mô hình chấm khác bước 1 nên không suy ra tăng/giảm accuracy.',
        '- Đáp án tham chiếu chỉ dùng sau sinh câu trả lời; bộ câu hỏi đã dùng trong phát triển nên đây là hồi quy trên chủ đề đã biết, chưa phải kiểm thử mù.',
        '- Không có đáp án độc lập cho nhà trọ/KTX và không có điểm RAGAS mới. Confidence chưa được hiệu chuẩn thành xác suất đúng.',
        '- Độ trễ là quan sát vận hành trên máy local với tài nguyên dùng chung, chưa phải benchmark tài nguyên cô lập.', '',
        '## Từng câu', '', '| ID gốc | Chủ đề | Nguồn | Cờ thiếu/một phần | Graph trace | Đối chiếu |', '|---|---|---:|---|---|---|']
    extra_cases=[case for case in comparison_run['cases'] if case['id'] not in {c['id'] for c in run['cases']}]
    if review_cases:
        lines += ['', 'Nhận xét Qwen có lỗi chấm đã được ghi chú khi kiểm tra văn bản. Giữ nguyên nhãn thô để đối chiếu; không coi các nhãn là accuracy đã xác minh.', '']
    if extra_cases:
        lines += ['', 'Hai câu 57–58 được chạy thêm để đối chiếu đủ 36 đáp án; không tính vào thống kê 56 câu.', '']
    for case in run['cases']+extra_cases:
        agreement = comparison_cases.get(case['id'], {}).get('comparison', {}).get('agreement', 'không có tham chiếu')
        flags = 'một phần' if case.get('partial_answer') else 'thiếu kết quả' if case.get('no_answer') else '—'
        traced = any(step.get('stage') == 'graph_retrieval' for step in case.get('agent_trace', []))
        lines.append(f"| {case['id']} | {case['category']} | {len(case.get('sources', []))} | {flags} | {'có' if traced else 'không'} | {agreement} |")
    for case in run['cases']+extra_cases:
        lines += ['', f"## Câu {case['id']}: {case['question']}", '', case['answer'], '',
                  f"Provider: `{case['generation_provider']}` · confidence heuristic: {case['confidence']} · retrieval: `{case['retrieval_mode']}`."]
        if case.get('sources'):
            lines += ['', '### Nguồn hệ thống sử dụng', '']
            for source in case['sources']:
                title = source['title'].replace('\\', '\\\\').replace('[', '\\[').replace(']', '\\]').replace('\n', ' ')
                url = source.get('source_url') or ''
                address = urlparse(url)
                host = address.hostname or ''
                trusted = address.scheme == 'https' and (host == 'chotot.com' or host.endswith('.chotot.com')
                    or host.endswith('.gov.vn') or host.endswith('.chinhphu.vn')
                    or host.endswith('.ctu.edu.vn') or host.endswith('.cdnchinhphu.vn') or host=='capnuoccantho2.com.vn')
                label = f"[{title}]({quote(url, safe=':/?#=%&-._~')})" if trusted else title
                source_kind = source.get('page_kind') or source.get('kind')
                unit = 'đơn vị trích' if source_kind=='logical_document' else 'trang'
                pages = f" · {unit} {source['page_from']}–{source.get('page_to') or source['page_from']}" if source.get('page_from') else ''
                lines.append(f"- [{source['rank']}] {label} · `{source_kind}`{pages}")
        if case['id'] in housing_checks:
            check = housing_checks[case['id']]
            lines += ['', f"Nguồn khớp bộ lọc: {check['matching_source_records']} · trả về: {check['returned']} · vi phạm: {check['constraint_violations']}."]
        if case['id'] in comparison_cases:
            comparison_case = comparison_cases[case['id']]
            lines += ['', '### Đáp án bạn gửi', '', comparison_case['user_reference'], '', '### Nhận xét Qwen cục bộ', '',
                      '**Mức khớp văn bản:** ' + comparison_case['comparison']['agreement'], '', comparison_case['comparison']['explanation']]
            if comparison_case['question_text_changed']:
                lines += ['', '**Câu hỏi tham chiếu có khác biệt:** ' + comparison_case['reference_question']]
            for key, label in [('matched_points', 'Ý khớp'), ('missing_reference_points', 'Ý thiếu so với tham chiếu'),
                               ('differing_points', 'Nội dung khác'), ('useful_additions', 'Nội dung thêm'),
                               ('source_cautions', 'Giới hạn nguồn')]:
                points = comparison_case['comparison'].get(key) or []
                if points:
                    lines += ['', '**' + label + '**', '', *['- ' + point for point in points]]
            if case['id'] in review_cases:
                lines += ['', '### Ghi chú kiểm tra văn bản', '']
                for note in review_cases[case['id']]['notes']:
                    lines += ['- '+note['correction'], '', 'Trong câu trả lời: '+note['answer_evidence'], '',
                              'Trong đáp án mẫu: '+note['reference_evidence'], '']
    lines += ['', '## Kiểm chứng', '', *[f"- {name}: {'đạt' if passed else 'chưa đạt'}" for name, passed in gates.items()], '',
              f"Pipeline SHA-256: `{current_pipeline}`", f"Run SHA-256: `{report['run_sha256']}`"]
    args.output.with_suffix('.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(json.dumps({'passed': report['passed'], 'gates': gates, 'summary': summary, 'comparison': comparison['summary']}, ensure_ascii=False), flush=True)
    if not report['passed']:
        raise SystemExit(2)


if __name__ == '__main__':
    main()
