"""Reproduce deterministic rejections on saved public-legal synthesis only."""
import json
from pathlib import Path
from app.room_service.chatbot.legal_retrieval import evidence_issues

r=json.loads(Path('/eval/reports/legal_repair_pilot_v14_20261006.json').read_text(encoding='utf-8'))
for c in r['cases']:
    if c['id'] not in (30,31,37) or not c.get('answer'): continue
    rows=[dict(source,content=content) for source,content in zip(c['sources'],c['contexts'])]
    for call in c['provider_calls']:
        data=call.get('structured_decision',{})
        if 'summary' not in data: continue
        records=[('summary',data['summary']),*[(f'steps:{i}',v) for i,v in enumerate(data['steps'])],
            *[(f'limitations:{i}',v) for i,v in enumerate(data['limitations'])]]
        print('Q',c['id'],'writer attempt')
        text=[]
        claims=[]
        for claim_id,line in records:
            rendered=line['text'].rstrip('.!?')+' '+' '.join('['+str(n)+']' for n in line['source_ranks'])+'.'
            text.append(rendered)
            claim=dict(claim_id=claim_id,kind=line['kind'],rendered=rendered)
            claims.append(claim)
            issues=evidence_issues(rendered,rows,'',claim_records=(claim,))
            if issues: print(claim_id,line.get('kind'),issues)
        all_issues=evidence_issues('\n'.join([*text,*data['follow_up_questions']]),rows,c['question'],claim_records=claims)
        print('whole answer:',all_issues)
