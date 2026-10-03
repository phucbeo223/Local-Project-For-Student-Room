"""Read-only release gates: compare all 36 cases, provenance and a verified backup."""
from pathlib import Path
import argparse,hashlib,json,math,statistics
from sqlalchemy import create_engine,text
from app.config import settings
from compare_model_upgrade import METHOD_FIELDS

BASE=Path('/eval')
METRICS=('faithfulness','answer_relevancy','context_utilization')
def read(p):return json.loads(p.read_text(encoding='utf-8')) if p.exists() else {}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def finite(v):return isinstance(v,(float,int)) and math.isfinite(v)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--after',type=Path,default=BASE/'reports/legal_agent_after_v8_2026-10-03.json')
    args=parser.parse_args()
    old=read(BASE/'reports/legal_model_upgrade_after_2026-10-02.json');new=read(args.after)
    retrieval=read(BASE/'reports/legal_agent_retrieval_2026-10-03.json')
    backup=read(BASE/'reports/legal_agent_backup_2026-10-03.json')
    review=read(BASE/'reports/legal_agent_source_review_2026-10-03.json')
    cases=new.get('cases',[]);completed=[c for c in cases if 'answer' in c and not c.get('error')]
    scores={m:[c.get('ragas',{}).get(m) for c in cases if finite(c.get('ragas',{}).get(m))] for m in METRICS}
    old_scores={m:[c.get('ragas',{}).get(m) for c in old.get('cases',[]) if finite(c.get('ragas',{}).get(m))] for m in METRICS}
    engine=create_engine(settings.database_url)
    with engine.connect() as conn:
        release=dict(conn.execute(text("SELECT * FROM public.legal_corpus_releases WHERE schema_name='legal_v2'")).mappings().one())
        counts=dict(conn.execute(text('SELECT count(*) AS chunks,count(embedding_vector) AS vectors,count(provision_id) AS identified,count(parent_content) AS parented FROM legal_v2.legal_chunks')).mappings().one())
    dump=Path('/workspace')/backup.get('backup_path','missing')
    gates={
        'retrieval_checks_passed':retrieval.get('passed') is True,
        'all_36_answered_without_execution_error':len(completed)==len(cases)==36,
        'all_cases_used_legal_agents':len(completed)==36 and all(c.get('intent')=='legal_question' and
            c.get('corpus_schema')=='legal_v2' and any(t.get('agent')=='question_analysis' for t in c.get('agent_trace',[])) for c in completed),
        'all_36_native_scores':all(len(scores[m])==36 for m in METRICS),
        'same_judge_and_method':bool(new.get('judge')) and all(old.get('judge',{}).get(k)==new['judge'].get(k) for k in METHOD_FIELDS),
        'same_corpus_as_database':bool(new.get('corpus_manifest_sha256')) and new['corpus_manifest_sha256']==release['manifest_sha256'],
        'all_embeddings_identified_and_parented':counts['chunks']>0 and len(set(counts.values()))==1,
        'qwen_attempted_all_answers':len(completed)==36 and all(any(p.get('provider')=='qwen-local' and p.get('method')=='generate' for p in c.get('provider_calls',[])) for c in completed),
        'no_gemini_answer_generation':len(completed)==36 and all(c.get('generation_provider')!='gemini' for c in completed),
        'gemini_analysis_observed':any(t.get('agent')=='question_analysis' and t.get('provider')=='gemini' and t.get('status')=='completed' for c in completed for t in c.get('agent_trace',[])),
        'backup_restored_and_hash_matches':backup.get('restore_verified') is True and dump.is_file() and sha(dump)==backup.get('backup_sha256'),
        'reviewed_actual_answer_file':args.after.is_file() and review.get('evaluation_sha256')==sha(args.after) and review.get('reviewed_cases')==36 and review.get('critical_issues')==[],
    }
    for m in METRICS:
        gates[m+'_not_regressed']=len(scores[m])==len(old_scores[m])==36 and statistics.mean(scores[m])>=statistics.mean(old_scores[m])
    gates['incomplete_answers_not_increased']=len(completed)==36 and sum(bool(c.get('no_answer')) for c in completed)<=sum(bool(c.get('no_answer')) for c in old['cases'])
    report={'passed':all(gates.values()),'gates':gates,'after':str(args.after),
        'evaluation_file':args.after.name,'evaluation_sha256':sha(args.after) if args.after.is_file() else None,
        'corpus_manifest_sha256':release['manifest_sha256'],
        'score_counts':{m:len(scores[m]) for m in METRICS},
        'scores':{m:statistics.mean(scores[m]) if scores[m] else None for m in METRICS},
        'no_answer':sum(bool(c.get('no_answer')) for c in completed),
        'policy':'Engineering release gate: all cases scored with the historical judge, no metric/completeness regression, source review and restored backup. Not an independent legal correctness certification.',
        'action':'eligible_for_preview_and_cutover' if all(gates.values()) else 'retain_original_corpus'}
    (BASE/'reports/legal_agent_release_gate_2026-10-03.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False),flush=True);engine.dispose()
    if not report['passed']:raise SystemExit(2)

if __name__=='__main__':main()
