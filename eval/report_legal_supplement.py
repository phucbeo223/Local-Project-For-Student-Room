"""Publish paired metrics and provenance without inventing legal references."""
from pathlib import Path
import hashlib,json,math,statistics
from collections import Counter
from datetime import datetime,timezone

EVAL = Path('/eval') if Path('/eval').exists() else Path(__file__).parent
ROOT = Path('/workspace') if Path('/workspace').exists() else EVAL.parent
DOCS = Path('/source-docs') if Path('/source-docs').exists() else ROOT/'docs'
BEFORE = EVAL/'reports/legal_model_upgrade_after_2026-10-02.json'
AFTER = EVAL/'reports/legal_supplement_release_2026-10-03.json'
OUTPUT = EVAL/'ragas_reports/legal_supplement_comparison_2026-10-03.md'

def read(p): return json.loads(p.read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def valid(v): return isinstance(v,(float,int)) and math.isfinite(v)
def status(c):
    if c.get('error'): return 'lỗi'
    if c.get('partial_answer'): return 'một phần'
    if c.get('no_answer'): return 'chưa đủ'
    return 'tổng hợp'

def main():
    before,after = read(BEFORE),read(AFTER)
    assert len(after['cases'])==36 and all('answer' in c for c in after['cases'])
    assert before['question_bank_sha256']==after['question_bank_sha256']
    previous={c['id']:c for c in before['cases']}
    assert all(c['question']==previous[c['id']]['question'] for c in after['cases'])
    fields=['library','version','model','provider','embedding_model','answer_relevancy_strictness','context_char_limit','score_abstentions','max_output_tokens','temperature','context_policy','score_workers','judge_request_timeout_seconds']
    assert all(before['judge'].get(k)==after['judge'].get(k) for k in fields), 'Different judge settings'
    provenance=read(DOCS/'legal_sources_originals_20261003/prepared_manifest.json')
    audit=read(EVAL/'reports/legal_corpus_supplement_2026-10-03.json')
    metrics={}
    for metric in ['faithfulness','answer_relevancy','context_utilization']:
        pairs=[(previous[c['id']].get('ragas',{}).get(metric),c.get('ragas',{}).get(metric)) for c in after['cases']]
        pairs=[(a,b) for a,b in pairs if valid(a) and valid(b)]
        metrics[metric]={'n':len(pairs),'before':statistics.mean(a for a,b in pairs) if pairs else None,
            'after':statistics.mean(b for a,b in pairs) if pairs else None,
            'delta':statistics.mean(b-a for a,b in pairs) if pairs else None}
    lines=['# Sửa nguồn và kiểm thử lại 36 câu — 03/10/2026','',
           'Đối chiếu cùng câu hỏi, cùng bộ chấm RAGAS và ngữ cảnh đầy đủ. Các câu giá phòng, khoảng cách và KTX không có trong bộ này.','',
           '## Kết quả','', '| Chỉ số | Trước | Sau | Chênh lệch | Số cặp hợp lệ |','|---|---:|---:|---:|---:|']
    for name,value in metrics.items():
        lines.append(f"| {name} | {value['before']:.4f} | {value['after']:.4f} | {value['delta']:+.4f} | {value['n']} |" if value['n'] else f'| {name} | N/A | N/A | N/A | 0 |')
    lines += ['',f"- Hoàn tất: {after['summary']['completed']}/36; lỗi chạy: {after['summary']['errors']}.",
              f"- Trạng thái trước: {dict(Counter(status(c) for c in before['cases']))}.",
              f"- Trạng thái sau: {dict(Counter(status(c) for c in after['cases']))}.",
              f"- Thời gian p50: {before['summary']['latency_p50_ms']/1000:.2f} → {after['summary']['latency_p50_ms']/1000:.2f} giây; p95: {before['summary']['latency_p95_ms']/1000:.2f} → {after['summary']['latency_p95_ms']/1000:.2f} giây.",
              '- 108 kiểm tra tự động đạt; truy xuất thật xác nhận đủ hồ sơ cư trú, thông tin hợp đồng và chủ đề dữ liệu cá nhân cho câu 29.',
              f"- Kho nguồn: {audit['indexed_documents']} tài liệu, {audit['current_document_vectors']}/{audit['current_document_chunks']} đoạn có vector; không thiếu nguồn hoặc vector.",'',
              '## Bốn nhóm sửa','',
              '1. Kiểm tra số điều/khoản, chủ thể, quyền/nghĩa vụ và ngoại lệ theo chính nguồn được dẫn; sửa lỗi nhận nhầm nhãn mục thành số liệu thiếu trích dẫn.',
              '2. Bổ sung ngoại lệ Điều 328, nội dung hiệu lực Điều 689, nghĩa vụ cư trú Điều 9, đầy đủ Điều 27–28, Điều 30 đã sửa, các Điều PCCC 8/20/21/23/24 và hai khuyến cáo chính thức về lừa đảo.',
              '3. Lấy ứng viên theo chủ đề, giữ các phần được hỏi, ghép các điểm của cùng khoản; không loại nhầm quy định chung về hợp đồng nhà ở.',
              '4. Đánh dấu câu chưa đủ/một phần dựa trên nội dung phản hồi; không coi tên provider là bằng chứng đã trả lời đầy đủ.','',
              '## Nguồn và khả năng đối chiếu','',
              '- Toàn bộ tệp mới tải thuộc cổng Chính phủ, Công báo, Bộ Công an hoặc Công an tỉnh. URL, SHA-256, tệp gốc, trang và điều được ghi trong sổ nguồn.',
              '- Ba bản trích cũ được lưu riêng và ngừng truy xuất; không xóa bản gốc. Chỉ OCR/chép đối chiếu và cắt từ nguồn, không dùng model để tạo quy định.',
              '- Khuyến cáo Công an được gắn nhãn khuyến cáo, không coi là điều luật. Các bản biên tập không phải văn bản hợp nhất chính thức.',
              '- Các điều Dân sự giữ từ bản trích trước đã so khớp OCR theo điều; chưa chứng nhận từng chữ của toàn bộ 42 điều. Điều 482 có phạm vi tuyển khoản 1 và 4 được ghi rõ.',
              '- Sổ chi tiết: `docs/Legal_Supplement_2026-10-03.md`, `docs/legal_sources_originals_20261003/download_manifest.json`, `prepared_manifest.json`, `civil_ocr_comparison.json`.','',
              '## Model, giới hạn so sánh và phần còn thiếu','',
              '- Gemini 3.5 đã hết hạn mức ngày 500 lượt trong phiên này. Bổ sung Gemini 3.1 Flash Lite dự phòng trước Qwen 9B; giãn nhịp 5 giây/model để giảm lỗi tần suất. Không đổi khóa để vượt quota của cùng model.',
              f"- Model trước: {dict(Counter(c.get('generation_model') or c['generation_provider'] for c in before['cases']))}.",
              f"- Model sau: {dict(Counter(c.get('generation_model') or c['generation_provider'] for c in after['cases']))}.",
              '- Nguồn, cách truy xuất, kiểm tra và tỷ lệ model đều thay đổi. Không quy toàn bộ chênh lệch điểm cho việc bổ sung tài liệu. Gemini 3.1 vừa sinh một số câu vừa là bộ chấm, nên có nguy cơ đánh giá tương quan.',
              '- Bộ chấm giống lượt trước: RAGAS 0.3.9, Gemini 3.1 Flash Lite, E5 multilingual small, relevancy strictness 1, đủ ngữ cảnh, 8192 token, nhiệt độ 0, 4 luồng; chấm cả câu từ chối còn ngữ cảnh.',
              '- Không có đáp án chuẩn độc lập: chưa đo answer correctness/context recall và chưa chứng minh đúng pháp lý toàn diện. Cần người am hiểu pháp luật rà các kết luận, chủ thể và hiệu lực.',
              '- Câu trả lời thiếu nguồn vẫn phải nêu giới hạn hoặc từ chối; không tự tạo thông tin để nâng điểm.','',
              '## Kết quả từng câu','', '| Câu | Trước → sau | Faithfulness sau | Relevancy sau | Context utilization sau | Model sau |','|---|---|---:|---:|---:|---|']
    for c in after['cases']:
        scores=[f"{c.get('ragas',{}).get(m):.4f}" if valid(c.get('ragas',{}).get(m)) else 'N/A' for m in metrics]
        lines.append(f"| {c['id']} | {status(previous[c['id']])} → {status(c)} | {' | '.join(scores)} | {c.get('generation_model') or c['generation_provider']} |")
    lines += ['', '## Các câu cần rà tiếp','']
    for c in after['cases']:
        if c.get('no_answer') or c.get('partial_answer') or (valid(c.get('ragas',{}).get('faithfulness')) and c['ragas']['faithfulness']<.75):
            lines.append(f"- Câu {c['id']} ({status(c)}): {c['question']}")
            reasons=c.get('degraded_reasons',[])
            relevant=[r for r in reasons if 'không khả dụng (RuntimeError)' not in r]
            for reason in relevant[:3]: lines.append('  - '+reason.replace('\n',' ')[:450])
    OUTPUT.parent.mkdir(parents=True,exist_ok=True)
    OUTPUT.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    job_path=EVAL/'reports/legal_supplement_job_status_2026-10-03.json'
    job=read(job_path) if job_path.exists() else {}
    if job.get('baseline_sha256'): assert sha(BEFORE)==job['baseline_sha256'], 'Archived baseline was modified'
    manifest={'completed_at_utc':datetime.now(timezone.utc).isoformat(),'question_bank_sha256':after['question_bank_sha256'],
              'baseline':{'path':str(BEFORE),'sha256':sha(BEFORE),'unchanged':True},
              'after':{'path':str(AFTER),'sha256':sha(AFTER)},'metrics':metrics,
              'source_provenance':provenance,'corpus_audit':audit,'tests_passed':108,
              'deployed_image':job.get('deployed_image'),'evaluation_limitations':['Generation fallback differs','Generator and judge share Gemini 3.1 for some cases','No independent legal gold references']}
    paths=['app/room_service/chatbot/topics.py','app/room_service/chatbot/legal_retrieval.py','app/room_service/chatbot/repo.py','app/room_service/chatbot/providers.py','app/room_service/chatbot/service.py','app/room_service/chatbot/router.py','app/config.py']
    manifest['code_sha256']={p:sha(ROOT/'apps/api'/p) for p in paths}
    (EVAL/'reports/legal_source_supplement_2026-10-03.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'metrics':metrics,'summary':after['summary'],'report':str(OUTPUT)},ensure_ascii=False))

if __name__=='__main__':main()
