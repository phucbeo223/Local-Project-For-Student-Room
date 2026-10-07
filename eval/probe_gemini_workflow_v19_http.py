"""Authenticated local HTTP smoke; ephemeral account, no persisted credentials."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import time
import uuid
import httpx
from sqlalchemy import create_engine, text
from app.config import settings
from app.auth.security import make_access_token
import question_bank_ragas as bank


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    assert not args.output.exists()
    engine = create_engine(settings.database_url)
    email = 'workflow19-smoke-'+uuid.uuid4().hex+'@example.test'
    user_id = None
    result = dict(started_at_utc=datetime.now(timezone.utc).isoformat(), passed=False, cases=[])
    cases = [c for c in bank.load_questions(Path('/housing_bank.md')) if c['id'] in (20,24,28,36)]
    cases.append(dict(id='local_housing', question='Tìm phòng trọ ở Xuân Khánh giá dưới 2 triệu'))
    try:
        with engine.begin() as conn:
            user = dict(conn.execute(text('INSERT INTO users(email,name,email_verified) VALUES(:email,:name,true) RETURNING id,role,auth_version'), dict(email=email, name='Workflow19 HTTP smoke')).mappings().one())
            user_id = user['id']
        token = make_access_token(user_id, user['role'], user['auth_version'])
        with httpx.Client(timeout=480, follow_redirects=False) as client:
            result['health_status'] = client.get('http://api:8000/health').status_code
            result['anonymous_status'] = client.post('http://api:8000/chat/ask', json=dict(message=cases[0]['question'])).status_code
            for case in cases:
                start = time.perf_counter()
                response = client.post('http://api:8000/chat/ask', json=dict(message=case['question']), headers={'Authorization':'Bearer '+token})
                row = dict(id=case['id'], http_status=response.status_code, full_http_latency_ms=round((time.perf_counter()-start)*1000))
                if response.status_code == 200:
                    body = response.json()
                    row['response'] = body
                    if case['id'] == 'local_housing':
                        row['passed'] = body['intent']=='find_listing' and body['generation_provider'] in ('grounded_template','template') and bool(body['listings']) and not any(s.get('provider') in ('gemini','gemini-agent','qwen-local') for s in body.get('agent_trace',[]))
                    else:
                        row['passed'] = body.get('corpus_schema')=='legal_word_workflow_v19_20261007' and bool(body['sources']) and any(s.get('agent')=='evidence_selection' and s.get('provider')=='gemini' for s in body.get('agent_trace',[])) and all(s.get('provider')!='qwen-local' for s in body.get('agent_trace',[])) and 'content_completeness' in body and 'provenance_status' in body
                else:
                    row['passed'] = False
                result['cases'].append(row)
                print(json.dumps({k:v for k,v in row.items() if k!='response'}), flush=True)
        result['passed'] = result['health_status']==200 and result['anonymous_status'] in (401,403) and all(c['passed'] for c in result['cases'])
    except Exception as exc:
        result['error_type'] = type(exc).__name__
    finally:
        if user_id is not None:
            with engine.begin() as conn:
                result['temporary_user_removed'] = conn.execute(text('DELETE FROM users WHERE id=:id AND email=:email'), dict(id=user_id,email=email)).rowcount==1
        result['passed'] = result['passed'] and result.get('temporary_user_removed',False)
        result['finished_at_utc'] = datetime.now(timezone.utc).isoformat()
        bank.save_report(args.output, result)
        print(json.dumps(dict(passed=result['passed'], temporary_user_removed=result.get('temporary_user_removed'))), flush=True)
        engine.dispose()
    if not result['passed']:
        raise SystemExit(2)


if __name__=='__main__':
    main()
