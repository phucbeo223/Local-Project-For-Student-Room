"""Versioned progress and paired same-judge results; never import local scores."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,json,hashlib,math,re,statistics
from compare_model_upgrade import METHOD_FIELDS,METRICS

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'eval'
def read(path):return json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else 'N/A'
def finite(v):return isinstance(v,(int,float)) and math.isfinite(v)
def status(c):
    return 'lỗi chạy' if c.get('error') else 'chưa chạy' if 'answer' not in c else 'một phần' if c.get('partial_answer') else 'chưa đủ căn cứ' if c.get('no_answer') else 'trích nguồn'
def quotes_valid(c):
    quotes=list(re.finditer(r'“(.*?)”\s*\[(\d+)\]',c.get('answer',''),re.S))
    contexts={s['rank']:text for s,text in zip(c.get('sources',[]),c.get('contexts',[]))}
    return bool(quotes) and all(m[1] in contexts.get(int(m[2]),'') for m in quotes)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--after',type=Path,default=BASE/'reports/legal_agent_after_v15_2026-10-04.json')
    parser.add_argument('--local',type=Path,default=BASE/'reports/legal_agent_local_v15_2026-10-04.json')
    parser.add_argument('--output',type=Path,default=BASE/'ragas_reports/legal_fixes_2026-10-04.md')
    args=parser.parse_args()
    old_path=BASE/'reports/legal_model_upgrade_after_2026-10-02.json'
    v10_path=BASE/'reports/legal_agent_after_v10_2026-10-03.json'
    assert sha(old_path)=='b32743c4ad5b251313f488db5ce794e9e2c0159d5b34da346d70a465e3e4810b'
    assert sha(v10_path)=='a5b3ec7507e4ece633e3bf4469b0575f272e73b4c6ec2e22793996691c2a36ed'
    old,new,local=read(old_path),read(args.after),read(args.local)
    state=read(args.after.with_suffix('.status.json'))
    checks=read(BASE/'reports/legal_agent_retrieval_v15_2026-10-04.json')
    http=read(BASE/'reports/legal_agent_http_v14_2026-10-04.json')
    completed=[c for c in local.get('cases',[]) if 'answer' in c]
    same=bool(new.get('judge')) and all(old.get('judge',{}).get(k)==new['judge'].get(k) for k in METHOD_FIELDS)
    lines=['# Kiểm thử năm nhóm sửa lỗi pháp lý — v15','',
        'Cập nhật UTC: '+datetime.now(timezone.utc).isoformat(),'',
        '## Trạng thái','',
        '- Truy xuất thật: '+str(checks.get('passed'))+'; '+str(sum(checks.get('gates',{}).values()))+'/'+str(len(checks.get('gates',{})))+' gate.',
        '- Local riêng: '+str(len(completed))+'/36 phản hồi; '+str(local.get('summary',{}).get('errors',0))+' lỗi thực thi; '+str(sum(bool(c.get('partial_answer')) for c in completed))+' phản hồi một phần.',
        '- Kiểm tra nguyên văn local: '+str(sum(quotes_valid(c) for c in completed))+'/'+str(len(completed))+' phản hồi có mọi trích đoạn khớp đúng context/rank. Đây là kiểm tra chuỗi, không chứng nhận đúng luật.',
        '- HTTP v14: '+str(http.get('passed','chưa xong'))+'; nguồn web trả về: '+str(http.get('web_source_returned','chưa xong'))+'.',
        '- Worker Gemini: '+state.get('phase','chưa có trạng thái')+'; phản hồi hoàn thành: '+str(sum('answer' in c for c in new.get('cases',[])))+'/36.',
        '- Không điền điểm local vào Gemini. Kho public/API chính giữ nguyên, chờ gate và rà nguồn.', '',
        '## RAGAS native Gemini — so sánh theo cặp','',
        '| Metric | Số điểm v15 | Số cặp cùng phương pháp | Baseline trên cặp | V15 trên cặp | Thay đổi |',
        '|---|---:|---:|---:|---:|---:|']
    indexed={c['id']:c for c in old['cases']}
    for m in METRICS:
        valid=[c for c in new.get('cases',[]) if finite(c.get('ragas',{}).get(m))]
        pairs=[(indexed[c['id']]['ragas'][m],c['ragas'][m]) for c in valid
            if same and finite(indexed.get(c['id'],{}).get('ragas',{}).get(m))]
        values='N/A | N/A | N/A'
        if pairs:
            a,b=statistics.mean(x for x,y in pairs),statistics.mean(y for x,y in pairs)
            values=f'{a:.4f} | {b:.4f} | {b-a:+.4f}'
        lines.append(f'| {m} | {len(valid)}/36 | {len(pairs)} | {values} |')
    quota=state.get('quota') or new.get('quota_state')
    if quota:
        lines+=['','HTTP '+str(quota.get('http_status'))+': checkpoint đã lưu. Mốc kiểm tra lại UTC: `'+str(quota.get('retry_at_utc'))+'`. Worker chỉ chạy tiếp khi probe server thành công.']
    if not all(sum(finite(c.get('ragas',{}).get(m)) for c in new.get('cases',[]))==36 for m in METRICS):
        lines+=['','Chưa đủ 108 điểm native; **chưa kết luận chất lượng tổng thể tăng**. Điểm thiếu giữ N/A.']
    lines+=['','## Các câu local — tách khỏi lượt Gemini','',
        'Phân tích chủ đề local dùng rules vì container này tắt key; Qwen chọn đoạn nguồn. Không dùng như phép đo thay cho cấu hình Gemini phân tích.', '',
        '| Câu | Trạng thái | Model trả lời | Trích nguyên văn |', '|---|---|---|---|']
    for c in local.get('cases',[]):
        literal='đạt' if quotes_valid(c) else 'chưa xong' if 'answer' not in c else 'cần rà'
        lines.append(f"| {c['id']} | {status(c)} | {c.get('generation_model','')} | {literal} |")
    lines+=['','## Dấu vết và giới hạn','',
        '- JSON local: `'+args.local.name+'`, SHA `'+sha(args.local)+'`.',
        '- JSON native: `'+args.after.name+'`, SHA tại lúc lập báo cáo `'+sha(args.after)+'`; checkpoint còn chạy có thể đổi SHA.',
        '- Baseline: `'+old_path.name+'`, SHA `'+sha(old_path)+'`; v10 lịch sử: SHA `'+sha(v10_path)+'`. Hai file giữ nguyên.',
        '- Manifest cuối: `'+str(new.get('corpus_manifest_sha256'))+'`.',
        '- Các hạn chế còn cần rà: điều kiện hiệu lực điện; nghĩa vụ riêng chủ trọ về hồ sơ cư trú; phạm vi địa bàn/đơn vị cấp nước; phân loại nhà trọ; hướng dẫn công khai điện không phải điều luật.',
        '- Không có đáp án chuẩn độc lập: Answer Correctness/Context Recall N/A. Native judge không thay kiểm tra hiệu lực/đúng chủ thể.',
        '- Sổ nguồn và năm nhóm thay đổi: `docs/LEGAL_CORPUS_V2_SOURCES.md`, `docs/LEGAL_FIXES_20261004.md`.']
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps({'local_completed':len(completed),'local_errors':local.get('summary',{}).get('errors',0),
        'worker':state.get('phase'),'output':str(args.output)},ensure_ascii=False))

if __name__=='__main__':main()
