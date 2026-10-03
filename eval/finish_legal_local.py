"""Finite local collection and paired evaluation, with resumable checkpoints."""
import argparse
import hashlib
import json
import math
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from app.config import settings
from compare_model_upgrade import clone, METHOD_FIELDS
from finish_legal_supplement import verify_sources
from question_bank_ragas import save_report, summarize

BASE = Path('/eval')
OLD = BASE/'reports/legal_model_upgrade_after_2026-10-02.json'
BEFORE = BASE/'reports/legal_local_before_2026-10-03.json'
AFTER = BASE/'reports/legal_local_after_2026-10-03.json'
STATUS = BASE/'reports/legal_local_status_2026-10-03.json'
REPORT = BASE/'ragas_reports/legal_local_comparison_2026-10-03.md'
LOG = BASE/'reports/legal_local_2026-10-03.log'
METRICS = ('faithfulness', 'answer_relevancy', 'context_utilization')


def read(path):
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else {'cases': []}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def valid(value):
    return isinstance(value, (int, float)) and math.isfinite(value)


def publish(state):
    before, after = read(BEFORE), read(AFTER)
    state['updated_at_utc'] = datetime.now(timezone.utc).isoformat()
    state['completed_answers'] = sum('answer' in c for c in after['cases'])
    state['score_counts'] = {label: {m: sum(valid(c.get('ragas', {}).get(m)) for c in data['cases'])
                          for m in METRICS} for label, data in [('before', before), ('after', after)]}
    save_report(STATUS, state)
    previous = {c['id']: c for c in before['cases']}
    comparable = before.get('judge') and after.get('judge') and all(
        before['judge'].get(k) == after['judge'].get(k) for k in METHOD_FIELDS)
    lines = ['# Chạy và chấm bằng model local — 03/10/2026', '',
             f"Trạng thái: **{state['phase']}**. Cập nhật UTC: {state['updated_at_utc']}.", '',
             f"Câu trả lời mới: {state['completed_answers']}/36. Model trả lời, kiểm tra nguồn và chấm: Qwen 3.5 9B qua Ollama.",
             'Điểm trước được chấm lại từ câu trả lời và ngữ cảnh cũ; giữ nguyên tệp kết quả gốc.', '',
             '| Chỉ số | Trước | Sau | Chênh lệch | Số cặp hợp lệ |', '|---|---:|---:|---:|---:|']
    for m in METRICS:
        pairs = [(previous[c['id']].get('ragas', {}).get(m), c.get('ragas', {}).get(m))
                 for c in after['cases'] if c['id'] in previous] if comparable else []
        pairs = [(a, b) for a, b in pairs if valid(a) and valid(b)]
        if pairs:
            a, b = sum(x for x, y in pairs)/len(pairs), sum(y for x, y in pairs)/len(pairs)
            lines.append(f'| {m} | {a:.4f} | {b:.4f} | {b-a:+.4f} | {len(pairs)} |')
        else:
            lines.append(f'| {m} | N/A | N/A | N/A | 0 |')
    lines += ['', 'Chỉ kết luận cải thiện khi cả hai lượt đã chấm đủ bằng cùng cấu hình. Điểm từ Gemini trước đây không được so trực tiếp với điểm local.', '',
              '- Dùng RAGAS thật, đủ ngữ cảnh truy xuất, E5 multilingual small, nhiệt độ 0, relevancy strictness 1, một luồng chấm, tối đa 8192 token, thời hạn mỗi yêu cầu 300 giây.',
              '- Không có đáp án pháp lý chuẩn độc lập; chưa đo answer correctness/context recall. Model sinh cũng là model chấm nên cần rà soát của người am hiểu pháp luật.',
              '- Các câu giá phòng/khoảng cách đã loại khỏi bộ pháp lý. Giữ dữ liệu nguồn chính thức và vector đã nạp; không tạo thêm quy định.',
              '- Trường hợp thiếu nguồn, hết thời gian hoặc JSON bị cụt được ghi lỗi/N/A, không đổi thành điểm giả.', '',
              '## Kết quả mới từng câu', '', '| Câu | Trạng thái | Model thực tế | Faithfulness | Relevancy | Context utilization |', '|---|---|---|---:|---:|---:|']
    for c in after['cases']:
        label = 'lỗi' if c.get('error') else 'chưa chạy' if 'answer' not in c else 'một phần' if c.get('partial_answer') else 'chưa đủ căn cứ' if c.get('no_answer') else 'tổng hợp'
        values = [f"{c['ragas'][m]:.4f}" if valid(c.get('ragas', {}).get(m)) else 'N/A' for m in METRICS]
        lines.append(f"| {c['id']} | {label} | {c.get('generation_model') or c.get('generation_provider', '')} | {' | '.join(values)} |")
    if state.get('error'):
        lines += ['', 'Lỗi tác vụ: '+state['error']]
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text('\n'.join(lines)+'\n', encoding='utf-8')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--deployed-image', required=True)
    args = parser.parse_args()
    assert settings.chatbot_llm_provider == 'qwen', 'Local-only provider required'
    state = {'phase': 'starting', 'started_at_utc': datetime.now(timezone.utc).isoformat(),
             'deployed_image': args.deployed_image, 'generation_provider': 'qwen',
             'judge_provider': 'ollama', 'model': settings.ollama_model,
             'baseline_sha256': sha(OLD), 'verified_official_downloads': verify_sources(),
             'max_runtime_hours': 24, 'report': str(REPORT)}
    deadline = time.monotonic()+24*3600
    def run(phase, output, extra=()):
        state['phase'] = phase
        publish(state)
        cmd = [sys.executable, '/eval/question_bank_ragas.py', '--output', str(output), *extra]
        with LOG.open('a', encoding='utf-8') as log:
            process = subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT)
            try:
                while process.poll() is None:
                    if time.monotonic() >= deadline:
                        raise TimeoutError('Local evaluation exceeded its 24-hour limit')
                    try:
                        process.wait(timeout=15)
                    except subprocess.TimeoutExpired:
                        pass
                    publish(state)
                if process.returncode:
                    raise RuntimeError(f'{phase} exited with code {process.returncode}; see log')
            finally:
                if process.poll() is None:
                    process.terminate()
                    try:
                        process.wait(timeout=10)
                    except subprocess.TimeoutExpired:
                        process.kill()
                        process.wait()
    try:
        if not BEFORE.exists():
            clone(OLD, BEFORE)
        score_args = ['--phase', 'score', '--judge-provider', 'ollama', '--judge-model', settings.ollama_model,
                      '--judge-max-output-tokens', '8192', '--score-workers', '1', '--score-abstentions']
        run('local_answer_smoke_test', AFTER, ['--phase', 'collect', '--ids', '4'])
        run('local_ragas_smoke_test', AFTER, [*score_args, '--ids', '4'])
        smoke = next(c for c in read(AFTER)['cases'] if c['id'] == 4)
        if not all(valid(smoke.get('ragas', {}).get(m)) for m in METRICS):
            raise RuntimeError('Local RAGAS smoke test did not produce all three valid metrics')
        run('collecting_local_answers', AFTER, ['--phase', 'collect'])
        run('scoring_local_answers', AFTER, score_args)
        run('rescoring_archived_answers', BEFORE, score_args)
        assert sha(OLD) == state['baseline_sha256'], 'Original baseline changed'
        all_scored = all(all(valid(c.get('ragas', {}).get(m)) for m in METRICS)
                         for p in (BEFORE, AFTER) for c in read(p)['cases'])
        state['phase'] = 'complete' if all_scored else 'complete_with_scoring_errors'
        state['baseline_unchanged'] = True
        publish(state)
    except Exception as exc:
        state.update(phase='failed', error=f'{type(exc).__name__}: {exc}')
        publish(state)
        raise


if __name__ == '__main__':
    main()
