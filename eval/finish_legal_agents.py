"""Finite 36-question evaluation; retain checkpoints and a truthful historical comparison."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,math,statistics,subprocess,sys,time
from compare_model_upgrade import METHOD_FIELDS
from question_bank_ragas import save_report

BASE=Path('/eval')
BEFORE=BASE/'reports/legal_model_upgrade_after_2026-10-02.json'
AFTER=BASE/'reports/legal_agent_after_v9_2026-10-03.json'
STATUS=BASE/'reports/legal_agent_status_2026-10-03.json'
REPORT=BASE/'ragas_reports/legal_agent_comparison_2026-10-03.md'
LOG=BASE/'reports/legal_agent_v9_2026-10-03.log'
METRICS=('faithfulness','answer_relevancy','context_utilization')


def read(p):return json.loads(p.read_text(encoding='utf-8')) if p.exists() else {'cases':[]}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def valid(x):return isinstance(x,(int,float)) and math.isfinite(x)


def publish(state):
    old,new=read(BEFORE),read(AFTER)
    state['updated_at_utc']=datetime.now(timezone.utc).isoformat()
    state['completed_answers']=sum('answer' in c for c in new['cases'])
    state['score_counts']={m:sum(valid(c.get('ragas',{}).get(m)) for c in new['cases']) for m in METRICS}
    save_report(STATUS,state)
    common=bool(new.get('judge')) and all(old.get('judge',{}).get(k)==new['judge'].get(k) for k in METHOD_FIELDS)
    previous={c['id']:c for c in old['cases']}
    lines=['# Kho embedding mới và agent — kết quả 03/10/2026','',
           f"Trạng thái: **{state['phase']}**. Đã trả lời {state['completed_answers']}/36 câu.",
           'Gemini phân tích câu hỏi; hybrid truy xuất; Qwen local chọn ID đoạn trả lời; hệ thống chép nguyên văn có kiểm tra với nguồn. Không dùng Gemini tạo câu trả lời. Đây là chế độ trích nguồn, không phải suy luận pháp lý tự do.',
           'Điểm trước lấy từ bản đánh giá lịch sử ngày 02/10, giữ nguyên câu trả lời/ngữ cảnh/điểm gốc. So sánh chỉ có giá trị khi model chấm và cấu hình giống nhau.', '',
           '| Metric | Trước | Sau | Thay đổi | Số cặp hợp lệ |','|---|---:|---:|---:|---:|']
    for m in METRICS:
        pairs=[(previous[c['id']].get('ragas',{}).get(m),c.get('ragas',{}).get(m)) for c in new['cases']] if common else []
        pairs=[(a,b) for a,b in pairs if valid(a) and valid(b)]
        if pairs:
            a,b=statistics.mean(x for x,y in pairs),statistics.mean(y for x,y in pairs)
            lines.append(f'| {m} | {a:.4f} | {b:.4f} | {b-a:+.4f} | {len(pairs)} |')
        else:lines.append(f'| {m} | N/A | N/A | N/A | 0 |')
    lines+=['','## Từng câu','', '| Câu | Phân tích | Trả lời cuối | Trạng thái | Faithfulness | Relevancy | Context utilization |',
            '|---|---|---|---|---:|---:|---:|']
    for c in new['cases']:
        trace=c.get('agent_trace',[])
        analysis=next((s.get('provider','') for s in trace if s.get('agent')=='question_analysis'),'chưa chạy')
        status='lỗi' if c.get('error') else 'chưa chạy' if 'answer' not in c else 'một phần' if c.get('partial_answer') else 'chưa đủ căn cứ' if c.get('no_answer') else 'tổng hợp'
        values=[f"{c['ragas'][m]:.4f}" if valid(c.get('ragas',{}).get(m)) else 'N/A' for m in METRICS]
        lines.append(f"| {c['id']} | {analysis} | {c.get('generation_provider','')} | {status} | {' | '.join(values)} |")
    lines+=['','Không có đáp án chuẩn độc lập: answer correctness/context recall = N/A. Điểm RAGAS và đúng định dạng trích dẫn không xác nhận luật hiện hành.',
            'Các JSON lưu câu trả lời, ngữ cảnh, agent/model thật, lỗi, token và kết quả chấm để rà soát. Chưa xóa kho cũ chỉ vì bộ kiểm tra truy xuất đạt.']
    if state.get('error'):lines+=['','Lỗi tác vụ: '+state['error']]
    REPORT.parent.mkdir(parents=True,exist_ok=True);REPORT.write_text('\n'.join(lines)+'\n',encoding='utf-8')


def main():
    state={'phase':'starting','started_at_utc':datetime.now(timezone.utc).isoformat(),'baseline_sha256':sha(BEFORE),
           'max_runtime_hours':24,'corpus_schema':'legal_v2','cutover':'pending verified results'}
    deadline=time.monotonic()+24*3600
    def run(phase,args):
        state['phase']=phase;publish(state)
        with LOG.open('a',encoding='utf-8') as out:
            process=subprocess.Popen([sys.executable,'/eval/question_bank_ragas.py','--output',str(AFTER),*args],stdout=out,stderr=subprocess.STDOUT)
            try:
                while process.poll() is None:
                    if time.monotonic()>deadline:raise TimeoutError('Evaluation exceeded finite runtime')
                    try:process.wait(timeout=15)
                    except subprocess.TimeoutExpired:pass
                    publish(state)
                if process.returncode:raise RuntimeError(f'{phase} exited {process.returncode}; see log')
            finally:
                if process.poll() is None:
                    process.terminate()
                    try:process.wait(timeout=10)
                    except subprocess.TimeoutExpired:process.kill();process.wait()
    try:
        assert read(BASE/'reports/legal_agent_retrieval_2026-10-03.json')['passed']
        run('collecting_answers',['--phase','collect'])
        run('scoring_ragas',['--phase','score','--judge-provider','gemini','--judge-model','gemini-3.1-flash-lite',
            '--score-workers','4','--judge-max-output-tokens','8192','--score-abstentions'])
        assert sha(BEFORE)==state['baseline_sha256']
        data=read(AFTER)
        state['baseline_unchanged']=True
        complete=all('answer' in c and all(valid(c.get('ragas',{}).get(m)) for m in METRICS) for c in data['cases'])
        state['phase']='complete' if complete else 'complete_with_errors'
        publish(state)
    except Exception as exc:
        state.update(phase='failed',error=f'{type(exc).__name__}: {exc}');publish(state);raise


if __name__=='__main__':main()
