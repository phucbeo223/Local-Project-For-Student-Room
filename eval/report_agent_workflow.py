"""Report a completed agent collection beside preserved chatbot/reference replies.

Operational counts only: this does not infer legal accuracy from model verdicts.
Run after collection has finished; incomplete collections are rejected.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def statistics(cases):
    return {
        'questions': len(cases),
        'providers': dict(Counter(c.get('generation_provider') for c in cases)),
        'partial_answers': sum(bool(c.get('partial_answer')) for c in cases),
        'no_answer_flags': sum(bool(c.get('no_answer')) for c in cases),
        'degraded': sum(bool(c.get('degraded')) for c in cases),
        'latency_median_ms': median(c['latency_ms'] for c in cases),
        'answer_characters_median': median(len(c['answer']) for c in cases),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', type=Path, required=True)
    parser.add_argument('--reference', type=Path, default=ROOT / 'eval/ragas_reports/gemini_qwen_vs_pasted_2026-10-04.json')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    run, reference = read(args.run), read(args.reference)
    cases, refs = run['cases'], reference['cases']
    if len(cases) != 36 or any(not c.get('answer') or c.get('error') for c in cases):
        raise ValueError('Expected 36 completed chatbot replies without generation errors')
    by_id = {c['id']: c for c in refs}
    if set(by_id) != {c['id'] for c in cases}:
        raise ValueError('Question IDs do not match the preserved reference comparison')
    if any(c['question'] != by_id[c['id']]['system_question'] for c in cases):
        raise ValueError('Question text differs from preserved chatbot questions')
    a = [by_id[c['id']]['gemini_case'] for c in cases]
    b = [by_id[c['id']]['hybrid_case'] for c in cases]
    trace = [s for c in cases for s in c.get('agent_trace', [])]
    synthesized = [c for c in cases if c.get('generation_provider') == 'gemini-agent']
    summary = statistics(cases)
    summary.update({
        'gemini_analysis_completed': sum(s.get('agent') == 'question_analysis' and s.get('status') == 'completed' for s in trace),
        'questions_with_writer_repair': sum(any(s.get('agent') == 'answer_synthesis' and s.get('repair') for s in c.get('agent_trace', [])) for c in cases),
        'writer_failures_by_type': dict(Counter(s.get('error_type') for s in trace if s.get('agent') == 'answer_synthesis' and s.get('status') == 'fallback')),
        'verification_events': dict(Counter(f"{s.get('provider')}:{s.get('status')}" for s in trace if s.get('agent') == 'source_verification')),
        'synthesized_answer_characters_median': median(len(c['answer']) for c in synthesized) if synthesized else None,
    })
    limitations = [
        'Đây là thống kê vận hành và nguyên văn đầu ra, chưa có điểm đúng pháp luật hay RAGAS mới.',
        'Đáp án C do người dùng cung cấp là văn bản tham chiếu; không được đưa vào prompt hoặc tự coi là chuẩn pháp lý.',
        'A/B là các lượt chatbot được lưu trước đó; khác pipeline và thời điểm, so độ trễ chỉ có tính quan sát.',
        'Lượt D tắt khoảng nghỉ Gemini giữa request để đánh giá; cấu hình pacing môi trường chạy có thể khác.',
        'Trích dẫn hợp lệ chỉ xác nhận rank; exact_source_match chỉ xác nhận nguyên văn, không xác nhận đủ căn cứ hay hiệu lực.',
        'Model Gemini là alias do proxy cung cấp; chưa xác nhận danh tính model bên dưới.',
        'no_answer có thể đánh dấu câu đã trả lời một phần; không đồng nghĩa không có nội dung trả lời.',
    ]
    data = {
        'method': 'completed real chatbot collection; operational comparison without reference correctness scoring',
        'input_sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in (args.run.resolve(), args.reference.resolve())},
        'pipeline_sha256': run.get('pipeline_sha256'),
        'corpus_manifest_sha256': run.get('corpus_manifest_sha256'),
        'run_configuration': run.get('run_configuration'),
        'summary': summary,
        'baseline_summary': {'A': statistics(a), 'B': statistics(b)},
        'limitations': limitations,
        'cases': [{
            'id': c['id'], 'question': c['question'],
            'A_gemini_chatbot': by_id[c['id']]['gemini_case']['answer'],
            'B_gemini_analysis_qwen_quotes': by_id[c['id']]['hybrid_case']['answer'],
            'C_user_reference': by_id[c['id']]['reference_answer'],
            'D_agent_chatbot': c['answer'],
            'agent_provider': c.get('generation_provider'),
            'partial_answer': c.get('partial_answer'),
            'latency_ms': c.get('latency_ms'),
            'agent_trace': c.get('agent_trace', []),
            'degraded_reasons': c.get('degraded_reasons', []),
            'sources': c.get('sources', []),
        } for c in cases],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.with_suffix('.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    lines = ['# Kết quả workflow Gemini + Qwen: 36 câu', '',
             'D: Gemini phân tích → Qwen chọn nguồn → Gemini tổng hợp → kiểm chứng và sửa tối đa một lần.', '',
             '| Chỉ tiêu | A: Gemini chatbot | B: phân tích + trích nguồn | D: agent |',
             '|---|---:|---:|---:|']
    stats = [statistics(a), statistics(b), summary]
    for label, key, transform in [
        ('Số câu', 'questions', str),
        ('Trả lời một phần', 'partial_answers', str),
        ('Cờ chưa đủ căn cứ', 'no_answer_flags', str),
        ('Độ trễ trung vị (giây)', 'latency_median_ms', lambda x: f'{x / 1000:.1f}'),
        ('Độ dài trung vị (ký tự)', 'answer_characters_median', str),
    ]:
        lines.append('| ' + label + ' | ' + ' | '.join(transform(s[key]) for s in stats) + ' |')
    lines.extend(['', f"D có **{len(synthesized)}/36 câu** giữ bản tổng hợp Gemini sau kiểm chứng; provider cuối: `{summary['providers']}`.",
                  f"Có {summary['questions_with_writer_repair']} câu gọi sửa bản tổng hợp. Lỗi writer: `{summary['writer_failures_by_type']}`.",
                  '', '## Giới hạn đánh giá', '', *['- ' + item for item in limitations], '',
                  '## Trạng thái từng câu', '', '| Câu | Provider cuối | Một phần | Giây |', '|---|---|---|---:|'])
    for c in cases:
        lines.append(f"| {c['id']} | {c.get('generation_provider')} | {c.get('partial_answer')} | {c['latency_ms']/1000:.1f} |")
    lines.extend(['', '## Nguyên văn đối chiếu', '',
                  'Các câu trả lời dưới đây được giữ nguyên; đặt cạnh nhau để kiểm tra nội dung, chưa chấm mức khớp hoặc kết luận bên nào đúng pháp luật.', ''])
    for c in data['cases']:
        lines.extend([f"### Câu {c['id']}: {c['question']}", ''])
        for label, key in [('A — Gemini chatbot', 'A_gemini_chatbot'), ('B — Gemini phân tích + Qwen trích nguồn', 'B_gemini_analysis_qwen_quotes'), ('C — Đáp án bạn gửi', 'C_user_reference'), ('D — Chatbot dạng agent', 'D_agent_chatbot')]:
            lines.extend([f'#### {label}', '', c[key], ''])
        if c['sources']:
            lines.extend(['Nguồn truy xuất của D (rank dùng trong trích dẫn):', '', *[
                f"- [{s['rank']}] {s.get('title', '')} — {s.get('heading') or ''}"
                for s in c['sources']], ''])
        if c['degraded_reasons']:
            lines.extend(['Lý do giới hạn/fallback của D:', '', *['- ' + item for item in c['degraded_reasons']], ''])
    args.output.with_suffix('.md').write_text('\n'.join(lines), encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == '__main__':
    main()
