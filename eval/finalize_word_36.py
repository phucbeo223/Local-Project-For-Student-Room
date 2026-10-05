"""Bind a 36-question Word release report to actual generation and comparison."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib,json
from pathlib import Path
import question_bank_ragas as bank

ROOT=Path('/workspace')
REPORTS=Path('/eval/reports')
IDS=list(range(19,39))+list(range(43,59))

def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    p=argparse.ArgumentParser();p.add_argument('--live-pipeline-sha',required=True);a=p.parse_args()
    paths={k:REPORTS/name for k,name in {
        'run':'graph_rag_word_36_v7_2026-10-05.json',
        'comparison':'graph_rag_word_vs_reference_36_v7_2026-10-05.json',
        'audit':'graph_rag_word_audit_v7_2026-10-05.json',
        'release':'graph_rag_word_release_v7_2026-10-05.json',
        'graph':'graph_rag_word_graph_v7_2026-10-05.json',
        'housing_http':'graph_rag_word_housing_http_v7_2026-10-05.json',
        'legal_http':'graph_rag_word_legal_http_v7_2026-10-05.json'}.items()}
    data={k:read(v) for k,v in paths.items()};run=data['run'];cmp=data['comparison'];audit=data['audit']
    reference=Path('/eval/datasets/external_legal_20261004/answers.json')
    pipeline=bank.pipeline_sha256(ROOT/'apps/api/app/room_service/chatbot')
    manifest=ROOT/'docs/legal_word_corpus_v7_20261005/manifest.json'
    gates={
        'exact_36_original_ids':sorted(c['id'] for c in run['cases'])==IDS,
        'all_36_completed_without_runtime_error':all(c.get('answer') and not c.get('error') for c in run['cases']) and len(run['cases'])==36,
        'comparison_covers_all_36':sorted(c['id'] for c in cmp['cases'])==IDS,
        'comparison_inputs_unchanged':cmp['run_sha256']==sha(paths['run']) and cmp['reference_sha256']==sha(reference),
        'local_text_comparison':cmp['judge_provider']=='ollama-local',
        'same_frozen_live_pipeline':pipeline==run['pipeline_sha256']==audit['pipeline_sha256']==a.live_pipeline_sha,
        'same_word_manifest':sha(manifest)==run['legal_manifest_sha256']==audit['manifest_sha256']==data['graph']['legal_sha256'],
        'word_audit_passed':audit['passed'] and all(audit['gates'].values()),
        'backup_restore_verified':data['release']['backup_restore_verified'],
        'old_indexes_removed':data['release']['old_indexes_removed'],
        'protected_rows_unchanged':data['release']['protected_after']==data['release']['protected_before']==audit['protected'],
        'authenticated_http_passed':all(data[k]['passed'] and data[k]['temporary_user_removed'] for k in ('housing_http','legal_http')),
        'active_word_namespaces':run['legal_schema']==audit['legal_schema'] and run['graph_schema']==audit['graph_schema'] and run['listing_schema']==audit['listing_schema'],
        'no_pdf_ocr_contexts':all(s.get('page_kind')=='logical_document' and str(s.get('source_path','')).startswith('docs/legal_word_corpus_v7_20261005/') for c in run['cases'] for s in c.get('sources',[])),
        'no_reference_answers_in_corpus':all(not s['id'].startswith(('guidance-','legacy-')) for s in audit['sources']),
    }
    groups={grade:sorted(c['id'] for c in cmp['cases'] if c['comparison']['agreement']==grade) for grade in ('high','partial','low')}
    baseline=read(REPORTS/'graph_rag_vs_reference_36_v15_2026-10-05.json')
    provider_counts=dict(Counter(c.get('generation_provider') for c in run['cases']))
    fallback_counts=dict(Counter(step.get('agent') for c in run['cases'] for step in c.get('agent_trace',[]) if step.get('status')=='fallback'))
    summary={'completed':sum(bool(c.get('answer')) for c in run['cases']),
        'runtime_errors':sum(bool(c.get('error')) for c in run['cases']),
        'high_agreement':len(groups['high']),'needs_review':len(groups['partial'])+len(groups['low']),
        'partial_agreement':len(groups['partial']),'low_agreement':len(groups['low']),
        'partial_answers':sum(bool(c.get('partial_answer')) for c in run['cases']),
        'marked_complete_answers':sum(not c.get('no_answer') for c in run['cases']),
        'marked_complete_ids':[c['id'] for c in run['cases'] if not c.get('no_answer')],
        'no_answer_flags':sum(bool(c.get('no_answer')) for c in run['cases']),
        'generation_providers':provider_counts,'agent_fallback_counts':fallback_counts,
        'without_sources':[c['id'] for c in run['cases'] if not c.get('sources')],
        'question_text_changed_ids':[c['id'] for c in cmp['cases'] if c.get('question_text_changed')]}
    report={'created_at_utc':datetime.now(timezone.utc).isoformat(),'passed':all(gates.values()),
        'gates':gates,'input_sha256':{k:sha(v) for k,v in paths.items()},'pipeline_sha256':pipeline,
        'summary':summary,'agreement_groups':groups,'previous_text_agreement':baseline['summary'],
        'legal_vectors':audit['counts'],'graph_counts':data['graph']['counts'],
        'scope':'Known-question regression and local qualitative text agreement; not legal accuracy or blind testing.',
        'limitations':['13 supplied Word excerpts are not certified verbatim originals.',
            'Same Qwen model selects evidence and judges text agreement; selection bias is possible.',
            'Word-only source policy removes prior HTML platform/invoice guidance; omissions must not be filled with invented text.',
            'References are user-provided, unverified; matching does not establish legal correctness.'],
        'manual_review_notes':[
            {'id':20,'note':'Tham chiếu khẳng định bắt buộc ghi tiền cọc; phản hồi phân biệt nội dung hợp đồng và thỏa thuận đặt cọc. Đây là khác biệt văn bản, chưa kết luận bên nào đúng pháp luật.'},
            {'id':21,'note':'Cờ API đánh dấu đủ, nhưng câu trả lời tự nêu nguồn chưa bao quát các trường hợp thay đổi giá khác. Nhận xét Qwen về giới hạn chỉ cải tạo mạnh hơn cách phản hồi diễn đạt; cần đọc toàn câu. Cờ đủ không phải đánh giá chất lượng độc lập.'},
            {'ids':[47,48,49],'note':'Thiếu nguồn Word phù hợp sau khi loại tài liệu trích tuyển nghiên cứu; không được gọi ba câu này là đã giải đáp chỉ vì request chạy không lỗi.'}]}
    target=REPORTS/'graph_rag_word_acceptance_v7_2026-10-05.json'
    target.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines=['# Kết quả 36 câu — corpus Word', '',
        f"Đã chạy {summary['completed']}/36 câu; lỗi thực thi: {summary['runtime_errors']}.",
        f"Khớp cao với đáp án mẫu: {summary['high_agreement']}; cần rà soát: {summary['needs_review']} (khớp một phần {summary['partial_agreement']}, thấp {summary['low_agreement']}).",'',
        'Đây là mức khớp văn bản do Qwen cục bộ chấm; không phải tỷ lệ đúng pháp luật. Các đáp án mẫu chưa được xác minh.','',
        f"Khớp cao: {groups['high']}",f"Khớp một phần: {groups['partial']}",f"Khớp thấp: {groups['low']}",'',
        f"Câu trả lời một phần: {summary['partial_answers']}; cờ no_answer: {summary['no_answer_flags']}; không có nguồn: {summary['without_sources']}.",
        f"Provider sinh: {provider_counts}; fallback agent: {fallback_counts}.",'',
        f"Câu ngân hàng và câu trong tham chiếu khác cách diễn đạt: {summary['question_text_changed_ids']}; cần đối chiếu phần chung.",'',
        '| ID | Mức khớp | Điểm mẫu còn thiếu | Khác biệt cần đối chiếu |', '|---|---|---|---|']
    for c in sorted(cmp['cases'],key=lambda c:c['id']):
        x=c['comparison']
        missing='; '.join(x['missing_reference_points']).replace('|','/').replace('\n',' ')
        differing='; '.join(x['differing_points']).replace('|','/').replace('\n',' ')
        lines.append(f"| {c['id']} | {x['agreement']} | {missing} | {differing} |")
    lines+=['','## Kiểm tra phát hành','',json.dumps(gates,ensure_ascii=False,indent=2),'',
        '## Rà soát thủ công','',
        'Câu 20: khác biệt về tính bắt buộc ghi tiền cọc giữa tham chiếu và phản hồi; chưa kết luận bên nào đúng pháp luật.',
        'Câu 21: API đánh dấu đủ nhưng phản hồi tự nêu nguồn chưa bao quát hết trường hợp thay đổi giá. Nhận xét Qwen về giới hạn chỉ cải tạo mạnh hơn cách phản hồi diễn đạt. Không coi cờ đủ là đánh giá chất lượng độc lập.',
        'Câu 47–49: thiếu nguồn Word, không được coi là đã giải đáp chỉ vì request chạy không lỗi.','',
        '13 Word cung cấp chưa được chứng nhận nguyên văn. Cần bổ sung Word có xuất xứ cho nền tảng đăng tin, hướng dẫn hóa đơn nước và khuyến cáo thực tế phù hợp; không tạo nguồn từ đáp án mẫu.','',
        'Lượt test CRUD rộng từng tạo dữ liệu test; 9 tài khoản và 5 phòng test đã được dọn, mọi dòng gốc đã đối chiếu với backup. 108 kiểm thử đúng phạm vi đã qua; không báo toàn bộ suite là qua.']
    target.with_suffix('.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps({'passed':report['passed'],'summary':summary,'groups':groups},ensure_ascii=False),flush=True)
    if not report['passed']:raise SystemExit(1)

if __name__=='__main__':main()
