"""One bounded retry of missing native scores, without changing judge or answers."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, math
from question_bank_ragas import METRIC_NAMES, save_report, score, summarize
from finish_legal_agents import AFTER, BEFORE, STATUS, publish
from app.room_service.chatbot.providers import GeminiGenerator, _extract_gemini_text


def valid(value):
    return isinstance(value, (int, float)) and math.isfinite(value)


def answer_hash(report):
    payload=[{k:c.get(k) for k in ('id','question','answer','sources','contexts','agent_trace','provider_calls')}
             for c in report['cases']]
    return hashlib.sha256(json.dumps(payload,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def main():
    state=json.loads(STATUS.read_text(encoding='utf-8'))
    if state.get('phase') not in ('complete','complete_with_errors'):
        raise ValueError('Wait for the original evaluation worker to finish')
    report=json.loads(AFTER.read_text(encoding='utf-8'))
    if report.get('bounded_missing_score_retry'):
        raise ValueError('This evaluation already used its single missing-score retry')
    if len(report['cases'])!=36 or any('answer' not in c for c in report['cases']):
        raise ValueError('Expected 36 collected answers')
    judge=report['judge']
    if not (judge['provider']=='gemini' and judge['model']=='gemini-3.1-flash-lite'
            and judge['max_output_tokens']==8192 and judge['score_workers']==4
            and judge['score_abstentions'] is True):
        raise ValueError('Historical judge configuration must remain unchanged')
    missing=[{'id':c['id'],'metric':m} for c in report['cases'] for m in METRIC_NAMES
             if not valid(c.get('ragas',{}).get(m))]
    if not missing:
        print('All 108 native scores are already present',flush=True)
        return
    baseline_sha=hashlib.sha256(BEFORE.read_bytes()).hexdigest()
    if baseline_sha!=state.get('baseline_sha256'):
        raise ValueError('The historical baseline file changed')
    payload_sha=answer_hash(report)
    existing={(c['id'],m):v for c in report['cases'] for m,v in c.get('ragas',{}).items() if valid(v)}
    report['bounded_missing_score_retry']={'started_at_utc':datetime.now(timezone.utc).isoformat(),
        'missing':missing,'answer_payload_sha256':payload_sha,
        'policy':'One retry of missing scores only; same judge/prompt/tokens/context/answers. No fake zero or reset of valid scores.'}
    for c in report['cases']:
        for m in METRIC_NAMES:
            if m in c.get('ragas',{}) and not valid(c['ragas'][m]):
                c.setdefault('ragas_retry_history',[]).append({'metric':m,'previous_value':c['ragas'].pop(m),
                    'reason':'non-finite native metric','retry_max_output_tokens':8192})
    save_report(AFTER,report)
    state['phase']='retrying_missing_ragas';publish(state)
    original_request=GeminiGenerator._request_content
    def diagnosed_request(self,payload,*args,**kwargs):
        data=original_request(self,payload,*args,**kwargs)
        if payload.get('generationConfig',{}).get('responseMimeType')=='application/json' and not _extract_gemini_text(data):
            # Never include prompt text, API key, request URL or raw response.
            details={'finish_reasons':[c.get('finishReason') for c in data.get('candidates',[])],
                     'prompt_block_reason':data.get('promptFeedback',{}).get('blockReason'),
                     'usage':{k:data.get('usageMetadata',{}).get(k) for k in ('promptTokenCount','candidatesTokenCount','thoughtsTokenCount')}}
            raise RuntimeError('Gemini JSON empty; diagnostics='+json.dumps(details,ensure_ascii=False))
        return data
    GeminiGenerator._request_content=diagnosed_request
    try:
        score(report,AFTER,None,judge['endpoint'],judge['model'],list(METRIC_NAMES),
              ids=sorted({x['id'] for x in missing}),score_abstentions=True,
              judge_max_output_tokens=8192,judge_provider='gemini',score_workers=4)
        assert answer_hash(report)==payload_sha
        assert hashlib.sha256(BEFORE.read_bytes()).hexdigest()==baseline_sha
        now={(c['id'],m):v for c in report['cases'] for m,v in c.get('ragas',{}).items()}
        assert all(now[k]==v for k,v in existing.items())
        report['bounded_missing_score_retry'].update(finished_at_utc=datetime.now(timezone.utc).isoformat(),
            unchanged_answers_and_contexts=True,valid_scores_preserved=True,baseline_unchanged=True)
        summarize(report);save_report(AFTER,report)
        state['phase']='complete' if all(valid(c.get('ragas',{}).get(m)) for c in report['cases'] for m in METRIC_NAMES) else 'complete_with_errors'
        publish(state)
    except Exception as exc:
        report['bounded_missing_score_retry'].update(error_type=type(exc).__name__,
            finished_at_utc=datetime.now(timezone.utc).isoformat())
        save_report(AFTER,report)
        state.update(phase='retry_failed',error=type(exc).__name__);publish(state)
        raise
    finally:
        GeminiGenerator._request_content=original_request


if __name__=='__main__':
    main()
