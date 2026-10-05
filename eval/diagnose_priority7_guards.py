"""Replay actual Gemini pilot decisions through current deterministic guards."""
import argparse
import json
from pathlib import Path
from app.room_service.chatbot.legal_retrieval import evidence_issues


def main():
    reports = Path('/eval/reports')
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', type=Path, default=reports/'graph_rag_priority7_pilot_v15_2026-10-06.json')
    parser.add_argument('--output', type=Path, default=reports/'graph_rag_priority7_guard_replay_2026-10-06.json')
    args = parser.parse_args()
    pilot = json.loads(args.run.read_text(encoding='utf-8'))
    rows = []
    for case in pilot['cases']:
        if not case.get('answer'): continue
        chunks = [dict(source, content=context) for source,context in zip(case['sources'],case['contexts'])]
        for call in case['provider_calls']:
            if call.get('agent') != 'answer_synthesis' or not call.get('structured_decision'): continue
            data = call['structured_decision']
            claims = [data['summary'],*data['steps'],*data['limitations']]
            answer = '\n'.join(c['text'].rstrip('.!?')+' '+ ' '.join(f'[{r}]' for r in c['source_ranks'])+'.' for c in claims)
            answer += '\n' + '\n'.join(data.get('follow_up_questions', []))
            issues = evidence_issues(answer,chunks,case['question'])
            rows.append(dict(id=case['id'], actual_gemini_decision=True, guard_issues=issues,
                             accepted_after_guard_fix=not issues, claims=claims))
    report = dict(method='Replay existing actual Gemini structured decisions; no new provider call or reference input; not a new end-to-end result.',cases=rows)
    args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps([dict(id=r['id'],accepted=r['accepted_after_guard_fix'],issues=r['guard_issues']) for r in rows],ensure_ascii=False))


if __name__ == '__main__': main()
