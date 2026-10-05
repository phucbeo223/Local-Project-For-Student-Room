"""Paired 36-case comparison; qualitative agreement is not legal accuracy."""
from pathlib import Path
from collections import Counter
from datetime import datetime,timezone,timedelta
import hashlib
import json
import statistics

ROOT=Path(__file__).resolve().parents[1]
if Path(__file__).resolve().parent==Path('/eval'):
 ROOT=Path('/workspace')
REPORTS=Path(__file__).resolve().parent/'reports'
IDS=list(range(19,39))+list(range(43,59))
LABELS={'high':'Cao','partial':'Một phần','low':'Thấp','improved':'Tăng','regressed':'Giảm','same':'Giữ'}
def read(name):return json.loads((REPORTS/name).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def stats(run,comparison):
 cases=run['cases'];groups={g:[c['id'] for c in comparison['cases'] if c['comparison']['agreement']==g] for g in ('high','partial','low')}
 complete=[c['id'] for c in cases if not c.get('no_answer') and not c.get('partial_answer') and not c.get('error')]
 return dict(completed=sum(bool(c.get('answer')) and not c.get('error') for c in cases),runtime_errors=sum(bool(c.get('error')) for c in cases),
   agreement_counts={g:len(v) for g,v in groups.items()},agreement_groups=groups,
   marked_complete_ids=complete,marked_complete=len(complete),partial=sum(bool(c.get('partial_answer')) for c in cases),
   no_answer=sum(bool(c.get('no_answer')) for c in cases),without_sources=[c['id'] for c in cases if not c.get('sources')],
   generation_providers=dict(Counter(c.get('generation_provider') for c in cases)),
   generation_models=dict(Counter(c.get('generation_model') for c in cases)),
   degraded_ids=[c['id'] for c in cases if c.get('degraded')],
   degradation_reasons=dict(Counter(reason for c in cases for reason in c.get('degraded_reasons',[]))),
   median_answer_characters=statistics.median(len(c['answer']) for c in cases),
   answers_over_6000_characters=[c['id'] for c in cases if len(c['answer'])>6000],
   agent_fallback_counts=dict(Counter(step.get('agent') for c in cases for step in c.get('agent_trace',[]) if step.get('fallback') and step.get('agent'))),
   p50_ms=run['summary']['latency_p50_ms'],
   p95_ms=run['summary']['latency_p95_ms'],
   supplements_used_ids=[c['id'] for c in cases if any('supplement' in s.get('source_path','') for s in c.get('sources',[]))])

def main():
 old=read('graph_rag_word_36_v7_2026-10-05.json');new=read('graph_rag_word_supplement_36_v8_2026-10-05.json')
 old_cmp=read('graph_rag_word_vs_reference_36_v7_2026-10-05.json');new_cmp=read('graph_rag_word_supplement_vs_reference_36_v8_2026-10-05.json')
 audit=read('graph_rag_word_supplement_audit_v8_2026-10-05.json')
 api=read('graph_rag_word_supplement_api_retained_v8_2026-10-05.json')
 gates={'exact_36_ids':all(sorted(c['id'] for c in r['cases'])==IDS for r in (old,new,old_cmp,new_cmp)),
 'same_pipeline':old['pipeline_sha256']==new['pipeline_sha256'],
 'same_question_bank':old['question_bank_sha256']==new['question_bank_sha256'],
 'same_housing_catalog':old['housing_catalog_sha256']==new['housing_catalog_sha256'],
 'same_local_judge_and_prompt':all(old_cmp[k]==new_cmp[k] for k in ('reference_sha256','judge_model','judge_prompt_policy','judge_provider')),
 'comparison_matches_run':new_cmp['run_sha256']==sha(REPORTS/'graph_rag_word_supplement_36_v8_2026-10-05.json'),
 'active_store_retained':audit.get('active_store_retained') is True,
 'live_api_remains_on_old_corpus':api==dict(legal_schema='legal_word_v7_20261005',graph_schema='graph_rag_word_v6',listing_schema='housing_graph_word_v6',docs_http_status=200),
 'new_store_not_active':audit.get('new_store_active') is False,
 'word_fidelity_and_embedding_audit':audit.get('passed') is True,
 'all_new_36_completed':all(c.get('answer') and not c.get('error') for c in new['cases'])}
 assert all(gates.values()),gates
 before=stats(old,old_cmp);after=stats(new,new_cmp)
 old_by={c['id']:c for c in old_cmp['cases']};new_by={c['id']:c for c in new_cmp['cases']};ranks={'low':0,'partial':1,'high':2}
 old_answers={c['id']:c['answer'] for c in old['cases']}
 identical_answers=[c['id'] for c in new['cases'] if c['answer']==old_answers[c['id']]]
 transitions=[]
 for key in IDS:
  a=old_by[key]['comparison']['agreement'];b=new_by[key]['comparison']['agreement']
  transitions.append(dict(id=key,before=a,after=b,change='improved' if ranks[b]>ranks[a] else 'regressed' if ranks[b]<ranks[a] else 'same',
    explanation=new_by[key]['comparison'].get('explanation'),missing_reference_points=new_by[key]['comparison'].get('missing_reference_points'),
    differing_points=new_by[key]['comparison'].get('differing_points')))
 changes={k:[t['id'] for t in transitions if t['change']==k] for k in ('improved','regressed','same')}
 finished=datetime.now(timezone.utc)
 report=dict(created_at_utc=finished.isoformat(),created_at_saigon=finished.astimezone(timezone(timedelta(hours=7))).isoformat(),generation_snapshot_started_at_utc=new['started_at_utc'],technical_checks_passed=True,legal_accuracy_certified=False,gates=gates,before=before,after=after,changes=changes,transitions=transitions,answer_text_identical_ids=identical_answers,
  pipeline_sha256=new['pipeline_sha256'],new_legal_schema=new['legal_schema'],new_graph_schema=new['graph_schema'],new_listing_schema=new['listing_schema'],
  method='Same exact known questions and pipeline; local Qwen qualitative agreement against unverified user answers, not legal correctness or generalization.',
  limitations=['Mỗi kho chỉ chạy một lượt; tính ngẫu nhiên và tình trạng mô hình/proxy có thể ảnh hưởng kết quả.',
   'Cùng Qwen cục bộ tham gia chọn bằng chứng và chấm đối chiếu; nhãn cần người đọc kiểm tra.',
   'Đáp án mẫu chưa xác minh; số tiền cọc, thời hạn minh họa và luật nền tảng cũ không được mặc nhiên coi là quy định bắt buộc.',
   'Câu 49 khác cách hỏi trong đáp án mẫu; chỉ so phần phạm vi chung.',
   '13 Word/trích tuyển cũ vẫn còn cảnh báo nguồn chưa xác minh toàn văn; hai nguồn bổ sung chưa nạp.',
   'API hiện hành vẫn dùng v7; v8 chỉ là kho thử nghiệm chưa kích hoạt.',
   'Đây là 36 câu đã biết, chưa đo khả năng trả lời câu hỏi mới.'])
 (REPORTS/'graph_rag_word_supplement_paired_36_v8_2026-10-05.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 lines=['# So sánh 36 câu sau bổ sung nguồn Word','',
  f"Snapshot nguồn/lượt sinh bắt đầu {new['started_at_utc']} (UTC); hoàn tất đối chiếu {report['created_at_saigon']} (giờ Việt Nam). Tên phiên bản 20261005 giữ theo ngày snapshot, không đổi dữ liệu giữa lượt chạy.", '',
  'Kho mới chỉ để thử nghiệm; kho và API hiện hành giữ nguyên. Pipeline, ngân hàng câu hỏi, Datahouse và chính sách chấm Qwen giống lượt trước.',
  '', '| Chỉ tiêu | Trước: 16 tài liệu | Sau: 30 tài liệu |','|---|---:|---:|',
  f"| Chạy hoàn tất | {before['completed']}/36 | {after['completed']}/36 |",
  f"| Lỗi chạy | {before['runtime_errors']} | {after['runtime_errors']} |",
  f"| Khớp cao với đáp án mẫu | {before['agreement_counts']['high']} | {after['agreement_counts']['high']} |",
  f"| Khớp một phần | {before['agreement_counts']['partial']} | {after['agreement_counts']['partial']} |",
  f"| Khớp thấp | {before['agreement_counts']['low']} | {after['agreement_counts']['low']} |",
  f"| Hệ thống đánh dấu trả lời đầy đủ | {before['marked_complete']} | {after['marked_complete']} |",
  f"| Không có nguồn truy xuất | {len(before['without_sources'])} | {len(after['without_sources'])} |",
  f"| Dùng trích đoạn Qwen sau kiểm tra | {before['generation_providers'].get('qwen-local',0)} | {after['generation_providers'].get('qwen-local',0)} |",
  f"| Độ dài câu trả lời trung vị (ký tự) | {before['median_answer_characters']:.0f} | {after['median_answer_characters']:.0f} |",
  f"| Thời gian p50 (giây) | {before['p50_ms']/1000:.1f} | {after['p50_ms']/1000:.1f} |",
  f"| Thời gian p95 (giây) | {before['p95_ms']/1000:.1f} | {after['p95_ms']/1000:.1f} |",'',
  '**Nhãn khớp là so nội dung với đáp án mẫu chưa xác minh, không phải điểm đúng pháp luật.** Hoàn tất 36 câu chỉ xác nhận lượt chạy, không chứng minh chất lượng 36 câu.',
  '',f"Tăng nhãn khớp: {changes['improved']}. Giảm nhãn: {changes['regressed']}. Giữ nhãn: {changes['same']}.",
  f"Câu còn khớp thấp cần xem kỹ: {after['agreement_groups']['low']}.",
  f"Câu khớp một phần còn cần đối chiếu: {after['agreement_groups']['partial']}.",
  f"Nguồn bổ sung được truy xuất ở {len(after['supplements_used_ids'])}/36 câu: {after['supplements_used_ids']}. Câu trả lời giữ nguyên từng byte: {identical_answers}. Các thay đổi ở câu không dùng nguồn bổ sung có thể do lượt sinh/chấm, chưa chứng minh hiệu quả của dữ liệu mới.",
  '', '## Dữ liệu và bảo toàn', '',
  '30 tài liệu gồm 16 Word cũ nguyên byte + 12 bản Word chuyển nguyên văn website + 2 Word luật gốc. Tổng 393 đoạn/điều khoản, 423 vector E5 384 chiều. Đoạn dài chia tối đa 1.200 ký tự, giữ toàn đoạn/điều khoản cha.',
  '789 nhà trọ Datahouse giữ nguyên nội dung và vector; graph thử nghiệm có 1.238 nút và 3.133 cạnh. Không PDF, không OCR, không embedding tóm tắt hay đáp án mẫu.',
  'S07 chưa nạp vì phần nội dung bài là ảnh; S13 chưa nạp vì tải nguyên bản bị HTTP 403. Không dùng bảng giá ở chân trang thay cho nội dung bài.',
  '', '## Giới hạn cần tiếp tục xử lý', '',
  '- Bổ sung nguồn đã giải quyết ba câu không truy xuất được nguồn, nhưng chưa tự giải quyết việc tổng hợp câu trả lời. Lượt mới có 18 câu quay về trích đoạn Qwen, so với 3 câu trước; 15 câu có lý do kiểm tra ghi kết luận/số liệu chưa gắn trích dẫn trực tiếp.',
  '- Ưu tiên trả lời trực tiếp, ngắn theo ý hỏi và gắn nguồn cho từng ý; hạn chế trả toàn bộ điều khoản dài. Câu 47–49 có nguồn mới nhưng câu trả lời dài khoảng 7.000–10.600 ký tự.',
  '- Cần hoàn thiện các điều/khoản được dẫn chiếu còn thiếu và kiểm tra nguyên bản chính thức của Word/trích tuyển cũ; giữ đúng điều kiện, ngoại lệ, loại nền tảng và thời điểm áp dụng.',
  *['- '+s for s in report['limitations']],
  '', '## Chi tiết từng câu', '', '| Câu | Trước | Sau | Thay đổi |','|---|---|---|---|',
  *[f"| {t['id']} | {LABELS[t['before']]} | {LABELS[t['after']]} | {LABELS[t['change']]} |" for t in transitions],
  '', '[Xem ý còn thiếu và nhận xét từng câu](WORD_SUPPLEMENT_36_REVIEW_20261005.md).', '',
  'Bản đầy đủ chứa câu trả lời và đáp án mẫu được giữ cục bộ tại `eval/reports/graph_rag_word_supplement_vs_reference_36_v8_2026-10-05.md`; báo cáo đối chiếu từng ý tại `eval/reports/graph_rag_word_supplement_paired_36_v8_2026-10-05.json`.']
 (ROOT/'docs/WORD_SUPPLEMENT_COMPARISON_20261005.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
 review=['# Ý cần xem lại trong 36 câu','',
  'Đây là nhận xét Qwen cục bộ khi đối chiếu với đáp án mẫu chưa xác minh. “Thiếu ý mẫu” không mặc nhiên là lỗi pháp luật; cần kiểm tra nguồn trước khi bổ sung số liệu, thời hạn, nghĩa vụ hoặc thủ tục.',
  '',f"Khớp cao: {after['agreement_groups']['high']}. Khớp một phần: {after['agreement_groups']['partial']}. Khớp thấp: {after['agreement_groups']['low']}."]
 for t in transitions:
  case=new_by[t['id']]
  review += ['',f"## Câu {t['id']}: {case['question']}",'',
    f"Mức khớp: **{LABELS[t['before']]} → {LABELS[t['after']]}** ({LABELS[t['change']]}).",'',t['explanation'] or '', '', '**Ý mẫu còn thiếu trong câu trả lời:**','']
  review += ['- '+p for p in t['missing_reference_points']] if t['missing_reference_points'] else ['Không có ý thiếu được bộ chấm liệt kê.']
  if t['differing_points']: review += ['', '**Khác biệt cần đối chiếu:**','',*['- '+p for p in t['differing_points']]]
 (ROOT/'docs/WORD_SUPPLEMENT_36_REVIEW_20261005.md').write_text('\n'.join(review)+'\n',encoding='utf-8')
 print(json.dumps(dict(before=before,after=after,changes=changes,gates=gates),ensure_ascii=False,indent=2))
if __name__=='__main__':main()
