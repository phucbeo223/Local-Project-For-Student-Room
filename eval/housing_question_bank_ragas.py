"""Only the selected housing questions, with model-visible listing contexts."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,sys
from sqlalchemy import create_engine,text
from app.config import settings
import question_bank_ragas as bank

def main():
    p=argparse.ArgumentParser();p.add_argument('--questions',type=Path,default=Path('/housing_bank.md'));p.add_argument('--output',type=Path,required=True)
    p.add_argument('--phase',choices=('collect','score','all'),default='all');p.add_argument('--ids',type=int,nargs='+',default=list(range(1,13)))
    p.add_argument('--judge-provider',choices=('gemini','ollama'),default='gemini');p.add_argument('--judge-model',default='gemini-3.1-flash-lite')
    p.add_argument('--score-workers',type=int,default=1);p.add_argument('--judge-max-output-tokens',type=int,default=8192);p.add_argument('--score-abstentions',action='store_true')
    a=p.parse_args();all_cases=bank.load_questions(a.questions);selected=[c for c in all_cases if c['id'] in a.ids]
    if len(selected)!=len(set(a.ids)) or any(c['category']!='find_listing' for c in selected):raise ValueError('Select original housing question IDs only')
    engine=create_engine(settings.database_url)
    with engine.connect() as c:
        if c.execute(text('SELECT current_schema()')).scalar_one()!='housing_v2':raise ValueError('Housing evaluator must use isolated housing_v2 search_path')
        digest=c.execute(text('SELECT catalog_sha256 FROM housing_v2.release WHERE id=1')).scalar_one()
        count=c.execute(text('SELECT count(embedding_vector) FROM housing_v2.aggregated_listings')).scalar_one()
        assert count==789
    engine.dispose();qsha=hashlib.sha256(a.questions.read_bytes()).hexdigest()
    report=json.loads(a.output.read_text(encoding='utf-8')) if a.output.exists() else {
        'started_at_utc':datetime.now(timezone.utc).isoformat(),'question_bank_sha256':qsha,
        'method':'real isolated housing DB + Qwen answers + native RAGAS; only selected original bank IDs',
        'cases':selected,'housing_catalog_sha256':digest,'housing_schema':'housing_v2',
        'selected_original_ids':sorted(a.ids),'total_original_question_bank':len(all_cases),
        'context_policy':'Exact listing JSON fields visible to Qwen, including the same description clipping; no extra unseen source text',
        'scope':'internal supplied catalog; old evaluation files not overwritten or merged'}
    if report['question_bank_sha256']!=qsha or report['housing_catalog_sha256']!=digest or report['selected_original_ids']!=sorted(a.ids):raise ValueError('Bank/dataset/selection changed; choose a new output')
    # This changes evaluation evidence formatting only, never generation/retrieval.
    import app.room_service.chatbot.service as svc
    from app.room_service.chatbot.providers import _grounded_prompt
    svc._evaluation_context=lambda item:_grounded_prompt('',[item]).split('CONTEXT LISTING (JSON):\n',1)[1]
    report.pop('quota_state',None)
    try:
        if a.phase in ('collect','all'):bank.collect(report,a.output,None,a.ids)
        if a.phase in ('score','all'):bank.score(report,a.output,None,'http://host.docker.internal:11434',a.judge_model,
            list(bank.METRIC_NAMES),False,a.ids,a.score_abstentions,a.judge_max_output_tokens,a.judge_provider,a.score_workers)
    except bank.QuotaPause:
        bank.checkpoint_pause(report,a.output,bank.QUOTA,a.phase);raise SystemExit(75)
    for case in report['cases']:
        if 'answer' in case and not case.get('contexts'):case['unscorable_reason']='No retrieved listing contexts; native RAGAS undefined, never assign zero'
    bank.summarize(report);report['updated_at_utc']=datetime.now(timezone.utc).isoformat();bank.save_report(a.output,report)
    print(json.dumps(report['summary'],ensure_ascii=False),flush=True)

if __name__=='__main__':main()
