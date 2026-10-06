"""Summarize saved legal runs without another model call or changing the rubric."""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
import math
from pathlib import Path
import re
import statistics


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def describe(values):
    values = sorted(values)
    return dict(count=len(values), median_ms=round(statistics.median(values)),
                p95_ms=values[max(0, math.ceil(len(values) * .95) - 1)]) if values else {}


def summarize(path, comparison=None):
    report = json.loads(path.read_text(encoding='utf-8'))
    cases = report['cases']
    if len(cases) != 36 or any(not c.get('answer') or c.get('error') for c in cases):
        raise ValueError(f'Expected 36 completed answers: {path}')
    durations = defaultdict(list)
    statuses = Counter()
    citations = []
    repairs = []
    for case in cases:
        allowed = {s['rank'] for s in case['sources']}
        used = {int(v) for v in re.findall(r'\[(\d+)\]', case['answer'])}
        citations.append(used <= allowed)
        repair_count = 0
        for step in case.get('agent_trace', []):
            agent = step.get('agent', step.get('stage'))
            if 'duration_ms' in step:
                durations[agent].append(step['duration_ms'])
            if agent == 'source_verification':
                statuses[step.get('status')] += 1
            if agent == 'answer_synthesis' and step.get('repair'):
                repair_count += 1
        repairs.append(repair_count)
    if not all(citations) or max(repairs) > 1:
        raise ValueError(f'Citation or repair limit failed: {path}')
    calls = [call for case in cases for call in case.get('provider_calls', [])]
    selection_requests = sum(len(step.get('attempts', [])) for case in cases
                             for step in case.get('agent_trace', [])
                             if step.get('agent') == 'selection_decision')
    # request_json traces include combined/write/verification, whereas the
    # selector's generate trace wraps one or two actual selection requests.
    measured_cloud_calls = sum(call.get('method') == 'request_json' and call.get('provider') == 'gemini'
                               for call in calls) + selection_requests
    analysis_calls = sum(step.get('agent') == 'question_analysis' and step.get('provider') == 'gemini'
                         for case in cases for step in case.get('agent_trace', []))
    result = dict(file=path.name, sha256=digest(path), pipeline_sha256=report['pipeline_sha256'],
        corpus_manifest_sha256=report['corpus_manifest_sha256'],
        question_bank_sha256=report['question_bank_sha256'],
        configuration=report['run_configuration'], completed=len(cases),
        runtime_complete=sum(not c.get('no_answer') and not c.get('partial_answer') for c in cases),
        runtime_partial=sum(bool(c.get('partial_answer')) for c in cases),
        no_supported_answer=sum(bool(c.get('no_answer')) and not c.get('partial_answer') for c in cases),
        degraded=sum(bool(c.get('degraded')) for c in cases),
        generation_providers=dict(Counter(c['generation_provider'] for c in cases)),
        latency=describe([c['latency_ms'] for c in cases]), stage_durations={k:describe(v) for k,v in durations.items()},
        verification_statuses=dict(statuses), cases_with_semantic_repair=sum(bool(v) for v in repairs),
        max_semantic_repairs=max(repairs), all_citation_ranks_exist=all(citations),
        failed_traced_calls=sum(call.get('success') is False for call in calls),
        qwen_generation_calls=sum(call.get('provider') == 'qwen-local' and call.get('method') == 'generate' for call in calls),
        qwen_total_traced_calls=sum(call.get('provider') == 'qwen-local' for call in calls),
        traced_gemini_requests_excluding_analysis=measured_cloud_calls,
        gemini_analysis_stages=analysis_calls,
        cloud_housing_calls=report.get('graph_summary', {}).get('cloud_housing_calls'),
        cloud_boundary=report.get('cloud_boundary'))
    if comparison:
        scored = json.loads(comparison.read_text(encoding='utf-8'))
        if scored['run_sha256'] != digest(path) or len(scored['cases']) != len(cases):
            raise ValueError('Comparison is not for this complete run')
        result['reference_comparison'] = dict(file=comparison.name, sha256=digest(comparison),
            policy=scored['policy'], scorer_sha256=scored['scorer_sha256'],
            quantity_audit_sha256=scored['quantity_audit_sha256'],
            reference_sha256=scored['reference_sha256'], reference_audit_sha256=scored['reference_audit_sha256'],
            judge_model=scored['judge_model'],
            summary=scored['summary'])
    return result, {c['id']:c['question'] for c in cases}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', type=Path, action='append', required=True)
    parser.add_argument('--comparison', type=Path, action='append', default=[])
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    comparisons = {json.loads(p.read_text(encoding='utf-8'))['run_sha256']:p for p in args.comparison}
    results = [summarize(p, comparisons.get(digest(p))) for p in args.run]
    if any(questions != results[0][1] for _, questions in results):
        raise ValueError('Question sets differ')
    rubric_keys = ('policy', 'scorer_sha256', 'quantity_audit_sha256',
                   'reference_sha256', 'reference_audit_sha256', 'judge_model')
    rubrics = {tuple(r['reference_comparison'][k] for k in rubric_keys)
               for r,_ in results if 'reference_comparison' in r}
    if len(rubrics) > 1:
        raise ValueError('Reference inputs, judge or rubric changed between comparisons')
    data = dict(runs=[r for r,_ in results], identical_questions=True,
        caveats=['Runtime coverage and text agreement are separate from legal accuracy.',
                 'Historical runs may differ in pipeline; see stored hashes.',
                 'End-to-end runs use live model analysis, not identical frozen retrieval candidates.',
                 'Timings are one sequential run per mode and include model/cache variability.',
                 'Configured Gemini model is the proxy alias, not independently verified backend identity.'])
    args.output.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    lines = ['# Kết quả thử Gemini RAG', '',
             '| Luồng | Đủ căn cứ theo runtime | Một phần | Không có phần được hỗ trợ | Trung vị | P95 | Sửa nội dung |',
             '|---|---:|---:|---:|---:|---:|---:|']
    for r,_ in results:
        name = r['configuration'].get('legal_selection_provider', 'qwen') + '/' + r['configuration'].get('legal_generation_mode', 'separate')
        lines.append(f"| {name} | {r['runtime_complete']}/36 | {r['runtime_partial']} | {r['no_supported_answer']} | {r['latency']['median_ms']/1000:.1f}s | {r['latency']['p95_ms']/1000:.1f}s | {r['cases_with_semantic_repair']} |")
    scored_runs = [r for r,_ in results if 'reference_comparison' in r]
    if scored_runs:
        lines += ['', '## Độ khớp với đáp án tham chiếu — bộ chấm V15', '',
                  '| Luồng | High | Partial | Low | Chưa chấm được | Audit trích dẫn đạt |',
                  '|---|---:|---:|---:|---:|---:|']
        for r in scored_runs:
            score = r['reference_comparison']['summary']
            agreement = score['agreement']
            name = r['configuration'].get('legal_selection_provider', 'qwen') + '/' + r['configuration'].get('legal_generation_mode', 'separate')
            lines.append(f"| {name} | {agreement.get('high',0)} | {agreement.get('partial',0)} | {agreement.get('low',0)} | {agreement.get('unscored',0)} | {score['quote_audit_passed']}/36 |")
    lines += ['', 'Số liệu chi tiết, hash và kết quả chấm tham chiếu (nếu có) nằm trong JSON cùng tên.', '',
              'Đây là kết quả một lượt chạy, không phải phần trăm đúng pháp luật. Chạy end-to-end nên Gemini có thể phân tích câu hỏi khác nhau giữa các lượt. Bản lịch sử có thể khác pipeline; đối chiếu hash trước khi suy ra quan hệ nhân quả.', '']
    args.output.with_suffix('.md').write_text('\n'.join(lines), encoding='utf-8')
    print(json.dumps([dict(file=r['file'], completed=r['completed'], complete=r['runtime_complete'],
                          partial=r['runtime_partial'], latency=r['latency']) for r,_ in results]))


if __name__ == '__main__':
    main()
