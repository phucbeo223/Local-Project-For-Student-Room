"""Replay saved legal writer/verifier decisions without model calls."""
import argparse
import json
from pathlib import Path
from app.room_service.chatbot.providers import GenerationResult
from app.room_service.chatbot.claim_verification import retained_answer,ClaimIssues
from app.room_service.chatbot.legal_retrieval import evidence_issues
from app.room_service.chatbot.source_selection import selection_candidates,render_selection
from app.room_service.chatbot.claim_verification import identify_rule_issues

p=argparse.ArgumentParser();p.add_argument('--run',type=Path,required=True);p.add_argument('--ids',type=int,nargs='+',required=True);a=p.parse_args()
for c in json.loads(a.run.read_text(encoding='utf-8'))['cases']:
    if c['id'] not in a.ids or not c.get('answer'):continue
    decisions=[x['structured_decision'] for x in c['provider_calls'] if 'summary' in x.get('structured_decision',{})]
    checks=[x['claim_verdicts'] for x in c['agent_trace'] if x.get('claim_verdicts')]
    if not decisions or not checks:continue
    data=decisions[0];records=[]
    for claim_id,line in [('summary',data['summary']),*[(f'steps:{i}',v) for i,v in enumerate(data['steps'])],*[(f'limitations:{i}',v) for i,v in enumerate(data['limitations'])]]:
        rendered=line['text'].rstrip('.!?')+' '+' '.join(f'[{n}]' for n in line['source_ranks'])+'.'
        records.append(dict(claim_id=claim_id,**line,rendered=rendered))
    rows=[dict(source,content=content) for source,content in zip(c['sources'],c['contexts'])]
    selection=next((x['structured_decision'] for x in c['provider_calls'] if 'selected_ids' in x.get('structured_decision',{})),None)
    candidates=selection_candidates(rows)
    if selection is None:
        ranks=next(x['selected_ranks'] for x in c['agent_trace'] if x.get('agent')=='evidence_selection')
        selection=dict(selected_ids=[x['id'] for x in candidates if x['rank'] in ranks][:4],insufficient=c['partial_answer'])
    draft=render_selection(c['question'],rows,candidates,json.dumps(selection),'qwen-local','saved')
    generated=GenerationResult('\n'.join(r['rendered'] for r in records),'gemini-agent',claim_records=tuple(records),evidence_limitations=draft.evidence_limitations,source_fallback=draft)
    issues=evidence_issues(generated.text_for_verification,rows,c['question'],claim_records=records)
    blocked={x['claim_id'] for x in identify_rule_issues(issues,generated,rows)}
    verdicts=[dict(v,supported=False) if v['claim_id'] in blocked else v for v in checks[-1]]
    kept=retained_answer(generated,ClaimIssues(verdicts))
    print('Q',c['id'],'retained',len(kept.text) if kept else None)
    if kept:
        for record in kept.claim_records:
            print(record['claim_id'],evidence_issues(record['rendered'],rows,'',claim_records=(record,)))
        print('RULE ISSUES',evidence_issues(kept.text,rows,c['question'],claim_records=kept.claim_records))
        print(kept.text)
