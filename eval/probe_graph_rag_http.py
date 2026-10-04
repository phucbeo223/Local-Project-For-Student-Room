"""Authenticated local HTTP probe with deterministic housing follow-up answers."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
from urllib.parse import urlparse
import uuid
import httpx
from sqlalchemy import create_engine, text
from app.config import settings
from app.auth.security import make_access_token


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base-url', default='http://api:8000')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    address = urlparse(args.base_url)
    if address.scheme != 'http' or address.hostname not in ('api', 'localhost', '127.0.0.1'):
        raise ValueError('Only the local application is supported')
    engine = create_engine(settings.database_url)
    email = 'graph-rag-smoke-' + uuid.uuid4().hex + '@example.test'
    user_id = None
    report = {'started_at_utc': datetime.now(timezone.utc).isoformat(), 'passed': False, 'temporary_user_removed': False}
    try:
        with engine.begin() as conn:
            user = dict(conn.execute(text('INSERT INTO public.users(email,name,email_verified) VALUES(:email,:name,true) '
                'RETURNING id,role,auth_version'), {'email': email, 'name': 'Graph RAG HTTP smoke'}).mappings().one())
            user_id = user['id']
        token = make_access_token(user_id, user['role'], user['auth_version'])
        message = 'Tìm phòng có giá thuê thấp nhất trong các tin còn hiệu lực.'
        with httpx.Client(timeout=120, follow_redirects=False) as client:
            report['health_status'] = client.get(args.base_url + '/health', timeout=10).status_code
            report['anonymous_status'] = client.post(args.base_url + '/chat/ask', json={'message': message}, timeout=10).status_code
            response = client.post(args.base_url + '/chat/ask', json={'message': message}, headers={'Authorization': 'Bearer ' + token})
            report['http_status'] = response.status_code
            response.raise_for_status()
            body = response.json()
            report['initial_response'] = body
            if not body['listings']:
                raise ValueError('Price minimum query returned no listing')
            first = body['listings'][0]
            follow = client.post(args.base_url + '/chat/ask', json={
                'message': 'Phòng đó có chỗ để xe và Wi-Fi không?',
                'conversation_state': body['conversation_state'],
                'conversation_history': [{'role': 'user', 'content': message},
                                         {'role': 'assistant', 'content': body['answer'][:2000]}]},
                headers={'Authorization': 'Bearer ' + token})
            report['follow_up_http_status'] = follow.status_code
            follow.raise_for_status()
            detail = follow.json()
            report['follow_up_response'] = detail
            report['same_listing_follow_up'] = bool(detail['listings']) and detail['listings'][0]['id'] == first['id']
            report['passed'] = (report['health_status'] == 200 and report['anonymous_status'] in (401, 403)
                and body['retrieval_mode'] == detail['retrieval_mode'] == 'graph_hybrid'
                and body['generation_provider'] == detail['generation_provider'] == 'structured'
                and all(item['corpus_schema'] == 'housing_graph_v1' for item in body['listings'] + detail['listings'])
                and any(step.get('stage') == 'graph_retrieval' for step in body['agent_trace'])
                and report['same_listing_follow_up'])
    except Exception as exc:
        report['error_type'] = type(exc).__name__
    finally:
        if user_id is not None:
            with engine.begin() as conn:
                deleted = conn.execute(text('DELETE FROM public.users WHERE id=:id AND email=:email'), {'id': user_id, 'email': email})
                report['temporary_user_removed'] = deleted.rowcount == 1
        report['passed'] = report['passed'] and report['temporary_user_removed']
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(json.dumps({key: value for key, value in report.items() if not key.endswith('_response')}, ensure_ascii=False), flush=True)
        engine.dispose()
    if not report['passed']:
        raise SystemExit(2)


if __name__ == '__main__':
    main()
