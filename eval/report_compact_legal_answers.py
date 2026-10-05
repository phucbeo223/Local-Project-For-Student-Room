"""Audit retained stores and summarize the three-question compact-answer pilot.

No generation, embedding, activation or comparison to unverified legal gold.
Historical source-display replay is explicitly separate from new model output.
"""
import hashlib
import json
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path

from sqlalchemy import create_engine
from app.config import settings
from app.room_service.chatbot.source_selection import render_source_fallback
from audit_word_supplement import snapshot

ROOT = Path('/workspace')
REPORTS = Path('/eval/reports')


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def main():
    before_path = REPORTS / 'graph_rag_word_supplement_36_v8_2026-10-05.json'
    after_path = REPORTS / 'graph_rag_compact_pilot_v9_2026-10-06.json'
    before, after = read(before_path), read(after_path)
    for key in ('question_bank_sha256', 'legal_manifest_sha256', 'housing_catalog_sha256',
                'legal_schema', 'listing_schema', 'graph_schema'):
        assert before[key] == after[key], key
    assert before['pipeline_sha256'] != after['pipeline_sha256']
    assert after['selected_original_ids'] == [47, 48, 49]
    assert all(case.get('answer') and not case.get('error') for case in after['cases'])
    original = {case['id']: case for case in before['cases']}
    paired = []
    for case in after['cases']:
        old = original[case['id']]
        assert old['question'] == case['question']
        paired.append(dict(id=case['id'], before_chars=len(old['answer']),
                           after_chars=len(case['answer']), provider=case['generation_provider'],
                           citation_accuracy=case['citation_accuracy'],
                           partial_answer=case['partial_answer'],
                           degraded_reasons=case['degraded_reasons'],
                           answer=case['answer']))
    replay = []
    pattern = re.compile(r'^- (.+?) — (.+?): “(.*?)” \[(\d+)\]\.', re.M | re.S)
    for case in before['cases']:
        if case['generation_provider'] != 'qwen-local' or len(case['answer']) <= 3500:
            continue
        matches = list(pattern.finditer(case['answer']))
        assert matches, case['id']
        parts = [dict(document=m[1], heading=m[2], text=m[3], rank=int(m[4])) for m in matches]
        # These are original application notices, not a new model completion.
        tail = case['answer'][matches[-1].end():]
        notices = [p.strip() for p in tail.split('\n\n') if p.strip() and
                   not p.strip().startswith('Thông tin tham khảo từ nguồn')]
        compact = render_source_fallback(parts, notices, insufficient=case['partial_answer'])
        assert len(compact) <= 3500, (case['id'], len(compact))
        for quotation in re.findall(r'“(.*?)” \[\d+\]', compact, re.S):
            assert any(quotation == part['text'] for part in parts)
        assert all(notice in compact for notice in notices)
        replay.append(dict(id=case['id'], before_chars=len(case['answer']), after_chars=len(compact),
                           all_notices_retained=True, no_truncated_legal_quotes=True))
    engine = create_engine(settings.database_url)
    with engine.connect() as connection:
        current = snapshot(connection)
    retained = read(REPORTS / 'graph_rag_word_supplement_audit_v8_2026-10-05.json')
    assert current == retained['active_after'], 'Active data changed'
    engine.dispose()
    report = dict(created_at_vietnam=datetime.now(timezone(timedelta(hours=7))).isoformat(),
                  before_run_sha256=hashlib.sha256(before_path.read_bytes()).hexdigest(),
                  after_run_sha256=hashlib.sha256(after_path.read_bytes()).hexdigest(),
                  before_pipeline_sha256=before['pipeline_sha256'],
                  after_pipeline_sha256=after['pipeline_sha256'],
                  pilot_cases=paired, historical_display_only_replay=replay,
                  active_store_unchanged=True, datahouse_unchanged=True,
                  new_store_activated=False, new_embeddings=False,
                  pilot_passed=all(p['after_chars'] <= 3500 and p['citation_accuracy'] == 1 for p in paired),
                  legal_accuracy_certified=False, full_36_rerun=False,
                  note='Citation accuracy measures valid source ranks, not legal correctness; historical display replay is not fresh model generation.')
    (REPORTS / 'graph_rag_compact_audit_v9_2026-10-06.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    lines = ['# Sửa trả lời quá dài — kiểm thử ngày 06/10/2026', '',
             'Đã tách cảnh báo nguồn do ứng dụng thêm khỏi phần kết luận mô hình cần kiểm chứng. '
             'Cảnh báo vẫn hiện đầy đủ; kết luận, câu hỏi tiếp theo và giới hạn do mô hình viết vẫn được kiểm tra.', '',
             'Câu trả lời dự phòng dùng trích đoạn ngắn nguyên vẹn hoặc dẫn nguồn để đối chiếu. '
             'Không cắt giữa điều kiện/ngoại lệ; toàn bộ bằng chứng vẫn có cho mô hình kiểm tra.', '',
             'Câu hỏi người thuê tự kiểm tra tin đăng ưu tiên hướng dẫn kiểm tra và phòng ngừa lừa đảo, '
             'không thay bằng trách nhiệm kiểm duyệt của nền tảng.', '',
             '## Lượt chạy thực tế mới: chỉ câu 47–49', '',
             '| Câu | Trước (ký tự) | Sau (ký tự) | Phần trả lời cuối |',
             '|---|---:|---:|---|']
    for p in paired:
        lines.append(f"| {p['id']} | {p['before_chars']} | {p['after_chars']} | {p['provider']} |")
    lines += ['', '97 kiểm thử hồi quy đạt. Lượt thử dùng cùng câu hỏi và kho Word thử nghiệm, '
              'Qwen + Gemini qua proxy hiện tại; không gửi đáp án mẫu hoặc Datahouse cho Gemini.', '',
              'Không có điểm khớp đáp án mẫu mới hoặc tỷ lệ đúng pháp luật mới. '
              'Chưa chạy lại toàn bộ 36 câu sau sửa mã. Các cảnh báo/thiếu nguồn còn lại:', '']
    for p in paired:
        lines.append(f"- Câu {p['id']}: " + ('; '.join(p['degraded_reasons']) or 'Không có cảnh báo suy giảm trong lượt chạy này.'))
    lines += ['', f"Đã thử lại cách hiển thị với {len(replay)} câu dự phòng dài của lượt cũ: "
              'tất cả không quá 3.500 ký tự, giữ nguyên cảnh báo và không cắt câu trích pháp lý. '
              'Đây là kiểm tra hiển thị ngoại tuyến, không phải chạy mới mô hình cho 36 câu.', '',
              'Đối chiếu hash toàn dòng: kho đang dùng, graph, nhà trọ Datahouse và người dùng giữ nguyên. '
              'Không xóa kho, không embedding lại, không kích hoạt kho thử nghiệm.', '',
              '## Câu trả lời mới để đọc', '']
    for p in paired:
        lines += [f"### Câu {p['id']}", '', p['answer'], '']
    (ROOT / 'docs/COMPACT_LEGAL_ANSWERS_20261006.md').write_text('\n'.join(lines), encoding='utf-8')
    print(json.dumps(dict(pilot_passed=report['pilot_passed'], paired=[
                          {k: v for k, v in p.items() if k != 'answer'} for p in paired],
                          replay_count=len(replay), active_store_unchanged=True), ensure_ascii=False))


if __name__ == '__main__':
    main()
