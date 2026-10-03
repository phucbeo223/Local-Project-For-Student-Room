"""One controlled reasoning probe against unchanged, saved government evidence."""
from pathlib import Path
import json,time
import httpx
from app.config import settings
from app.room_service.chatbot.providers import LEGAL_SYSTEM_PROMPT,_legal_prompt,GeminiGenerator
from app.room_service.chatbot.legal_retrieval import evidence_issues

report=json.loads(Path('/eval/reports/legal_agent_after_v5_2026-10-03.json').read_text(encoding='utf-8'))
case=next(c for c in report['cases'] if c['id']==1)
contexts=[dict(source,content=body,context_complete=True) for source,body in zip(case['sources'],case['contexts'])]
started=time.perf_counter()
with httpx.Client(timeout=300) as client:
    response=client.post(settings.ollama_base_url.rstrip('/')+'/api/chat',json={
        'model':settings.ollama_model,'stream':False,'think':True,'keep_alive':settings.ollama_keep_alive,
        'messages':[{'role':'system','content':LEGAL_SYSTEM_PROMPT},{'role':'user','content':_legal_prompt(case['question'],contexts)}],
        'options':{'temperature':0,'num_predict':2400,'num_ctx':max(16384,settings.ollama_context_length)}})
    response.raise_for_status();raw=response.json()
answer=raw.get('message',{}).get('content','').strip()
result={'question_id':1,'model':settings.ollama_model,'thinking':True,'latency_ms':round((time.perf_counter()-started)*1000),
        'answer':answer,'done_reason':raw.get('done_reason'),'prompt_tokens':raw.get('prompt_eval_count'),
        'generated_tokens_including_reasoning':raw.get('eval_count'),'corpus_manifest_sha256':report['corpus_manifest_sha256'],
        'rule_issues':evidence_issues(answer,contexts,case['question']),
        'prior_final_provider':case['generation_provider']}
if settings.configured_gemini_keys:
    checker=GeminiGenerator('',settings.chatbot_question_analysis_model,api_keys=settings.configured_gemini_keys,
        base_url=settings.gemini_base_url,legal_timeout_seconds=60,min_request_interval_seconds=settings.gemini_min_request_interval_seconds)
    try:result['source_issues']=checker.check_legal_evidence(case['question'],answer,contexts)
    except Exception as exc:result['verification_error_type']=type(exc).__name__
    finally:checker.close()
Path('/eval/reports/qwen_reasoning_probe_2026-10-03.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False),flush=True)
