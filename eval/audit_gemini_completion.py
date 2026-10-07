"""Separate source checks from frozen V15 similarity; never rewrite scores."""
import argparse
import hashlib
import json
from pathlib import Path
from collections import Counter
from telemetry_summary import summarize_calls

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--run', type=Path)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    reference = ROOT / 'eval/datasets/external_legal_20261004/answers.json'
    point_review = ROOT / 'eval/datasets/external_legal_20261004/point_review_20261006.json'
    historical = ROOT / 'eval/reports/legal_selector_ab_36_v2_20261007_branch_b_v15.json'
    manifest = ROOT / 'docs/legal_word_completion_v18_20261007/manifest.json'
    sources = {}
    for entry in json.loads(manifest.read_text(encoding='utf-8'))['documents']:
        path = ROOT / entry['file']
        assert sha(path) == entry['sha256']
        value = json.loads(path.read_text(encoding='utf-8'))
        assert sha(ROOT / value['source']['path']) == value['source']['sha256']
        sources[entry['id']] = value
    electricity = sources['electricity60-word']
    unit = next(p for p in electricity['provisions'] if p['article'] == '12' and p['clause'] == '5')
    assert '3/4 định mức' in unit['content'] and 'dưới 12 tháng' in unit['content']
    water = sources['supplement-s05-word']
    assert any('IDKH' in p['content'] and 'Mã xác nhận' in p['content'] for p in water['provisions'])
    old = json.loads(historical.read_text(encoding='utf-8'))
    findings = [dict(id=c['id'], original_v15=c['comparison'], disposition='Retain score unchanged; review suspected mismatch against source scope.')
                for c in old['cases'] if c['id'] in (24, 30)]
    notes = {
        24: dict(basis='Khoản 5 Điều 12 TT60/2025/TT-BCT', source_url=electricity['source']['source_url'],
            official_pdf_crosscheck=dict(url='https://datafiles.chinhphu.vn/cpp/files/vbpq/2025/12/60-bct.pdf',
                pages_one_based=[10, 11, 20, 23], reviewed='Khoản 5 Điều 12 xác nhận tỷ lệ 3/4 và điều kiện đồng thời dưới 12 tháng, không kê khai đủ; Điều 21 giữ điều kiện hiệu lực riêng; phụ lục có bậc 1 đến 100 kWh. Không xác nhận sự kiện kích hoạt hoặc biểu giá của một kỳ hóa đơn. PDF chỉ dùng đối chiếu, không nạp hoặc OCR vào kho Word.'),
            source_sha256=electricity['source']['sha256'], provision_id=unit['provision_id'],
            supported='Tỷ lệ 3/4 khi kê khai đầy đủ; bậc 2 cho toàn sản lượng có đồng thời điều kiện dưới 12 tháng và không kê khai đầy đủ.',
            limitation='Chưa xác minh sự kiện kích hoạt hiệu lực riêng. 37,5 kWh và cấu trúc bậc 50 kWh trong mẫu chưa được xác nhận với biểu giá áp dụng; không dùng làm đáp án chuẩn pháp lý.',
            judge_review='Một số explanation mô tả khớp tỷ lệ nhưng status=different. Khớp tỷ lệ không đồng nghĩa đã trả lời phép tính minh họa; cần tách hai ý. Không tự nâng nhãn.'),
        30: dict(basis='Hướng dẫn nhà cung cấp CANTHOWASSCO', source_url=water['source']['source_url'],
            source_sha256=water['source']['sha256'],
            supported='IDKH, mã xác nhận, cổng tra cứu và thao tác tra cứu trong hướng dẫn nhà cung cấp.',
            limitation='Chỉ áp dụng đúng nhà cung cấp trên hóa đơn; không xác nhận kênh Zalo hoặc cổng của đơn vị khác từ hướng dẫn này.',
            judge_review='Bổ sung điều kiện đúng nhà cung cấp là giới hạn cần thiết. V15 đánh giá khác mẫu không đủ chứng minh câu trả lời sai nguồn; cần rà riêng những bước thật sự thiếu.')}
    for finding in findings:
        finding['source_review'] = notes[finding['id']]
    register = json.loads(point_review.read_text(encoding='utf-8'))
    result = dict(reference_sha256=sha(reference), point_review_sha256=sha(point_review),
        historical_review_sha256=sha(historical), corpus_sha256=sha(manifest),
        original_reference_unchanged=True, original_v15_scores_unchanged=True,
        policy='Text similarity, runtime evidence support and independent legal source validity are separate. Pending reference points are not certified gold. No inferred accuracy percentage.',
        source_review_status_counts=dict(Counter(point['source_review_status'] for c in register['cases'] for point in c['points'])),
        focused_source_and_judge_audit=findings)
    if args.run:
        run = json.loads(args.run.read_text(encoding='utf-8'))
        result.update(run_sha256=sha(args.run), telemetry=summarize_calls(run['cases']),
            runtime_quality=dict(completed=sum('answer' in c for c in run['cases']), errors=sum(bool(c.get('error')) for c in run['cases']),
                partial=sum(bool(c.get('partial_answer')) for c in run['cases']),
                source_checks=dict(Counter(s.get('status', 'unknown') for c in run['cases'] for s in c.get('agent_trace', []) if s.get('agent') == 'source_verification')),
                scope='Runtime cited-evidence verification; no certification of source validity for every answer.'))
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(dict(focused_cases=[f['id'] for f in findings], original_reference_unchanged=True, runtime_quality=result.get('runtime_quality')), ensure_ascii=False))


if __name__ == '__main__':
    main()
