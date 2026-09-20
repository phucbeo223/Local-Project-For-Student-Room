"""Opt-in smoke test for the local Docker + Mailpit stack.

Creates one clearly named test account; never deletes existing data. Credentials,
OTP, reset links and cookies are deliberately not printed. Run inside api:
  python /app/scripts/smoke_local_deployment.py --create-test-account
"""
from __future__ import annotations

import argparse
import json
import re
import secrets
import time
from urllib.parse import parse_qs, urlparse

import httpx


def checked(response: httpx.Response, status: int = 200) -> httpx.Response:
    if response.status_code != status:
        raise RuntimeError(f"{response.request.method} {response.request.url.path}: HTTP {response.status_code}, expected {status}")
    return response


def mailbox_text(mail: httpx.Client, email: str, *, reset: bool = False) -> str:
    for _ in range(20):
        messages = checked(mail.get('/api/v1/messages')).json().get('messages', [])
        for message in messages:
            if not any(recipient.get('Address') == email for recipient in message.get('To', [])):
                continue
            body = checked(mail.get('/api/v1/message/' + message['ID'])).json().get('Text', '')
            if ('reset-password?' in body) == reset:
                return body
        time.sleep(0.5)
    raise RuntimeError('Expected test email did not arrive in Mailpit')


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--create-test-account', action='store_true', required=True)
    parser.add_argument('--chat', action='store_true', help='Also exercise retrieval and the configured LLM provider')
    args = parser.parse_args()
    email = f'deploy-smoke-{secrets.token_hex(6)}@example.com'
    password = secrets.token_urlsafe(24)
    with httpx.Client(base_url='http://web:3000', timeout=180) as web, httpx.Client(base_url='http://mailpit:8025', timeout=10) as mail, httpx.Client(base_url='http://127.0.0.1:8000', timeout=30) as api:
        for attempt in range(30):
            try:
                checked(api.get('/health'))
                break
            except (httpx.TransportError, RuntimeError):
                if attempt == 29:
                    raise RuntimeError('API did not become ready') from None
                time.sleep(1)
        checked(web.get('/'))
        checked(web.get('/login'))
        checked(web.get('/register'))
        dependencies = checked(api.get('/health/deps')).json()
        assert dependencies['postgres'] == dependencies['redis'] == dependencies['pgvector'] == 'ok'
        checked(web.post('/api/chat/ask', json={'message': 'Tìm phòng trọ'}), 401)
        checked(web.post('/api/auth/register', json={'email': email, 'password': password, 'name': 'Local deployment smoke test'}), 202)
        code = re.search(r'\b\d{6}\b', mailbox_text(mail, email))
        if code is None:
            raise RuntimeError('No OTP found in the test email')
        checked(web.post('/api/auth/verify-email', json={'email': email, 'code': code.group()}))
        user = checked(web.get('/api/auth/me')).json()
        assert user['email'] == email
        print(json.dumps({'account_created': user['id'], 'email': email, 'otp_and_cookie_login': 'ok'}), flush=True)
        response = checked(api.get('/listings', params={'size': 3, 'max_price': 3000000, 'max_area': 40})).json()
        assert response['items'], 'No eligible listings; import project data before running this smoke test'
        for listing in response['items']:
            assert listing['price'] <= 3000000 and listing['area'] <= 40
        listing_id = response['items'][0]['id']
        checked(web.get(f'/api/listings/{listing_id}'))
        checked(web.get(f'/listings/{listing_id}'))
        risk = checked(api.get(f'/risk/listings/{listing_id}')).json()
        assert not risk['persisted']
        checked(web.get('/compare', params={'ids': ','.join(str(item['id']) for item in response['items'])}))
        checked(web.post('/api/recommend/quiz', json={'max_price': 3000000, 'max_distance_ctu': 5000, 'amenities': []}))
        recommendations = checked(api.get('/recommend/for-you', headers={'Authorization': 'Bearer ' + web.cookies.get('access_token')})).json()
        for item in recommendations['items']:
            assert item['listing']['price'] <= 3000000
            assert item['listing']['distance_to_ctu'] <= 5000
        print(json.dumps({'filtered_search_detail_compare': 'ok', 'quiz': 'ok', 'recommendations': len(recommendations['items']), 'risk_preview': risk['evaluation_status'], 'risk_statistical': risk['statistical_status']}), flush=True)
        for path in ('/?max_price=3000000', '/recommendations', '/map', '/compare', '/chat'):
            checked(web.get(path, follow_redirects=True))
        print('web search/recommend pages: ok', flush=True)
        if args.chat:
            result = checked(web.post('/api/chat/ask', json={'message': 'Tìm phòng trọ Ninh Kiều dưới 3 triệu'})).json()
            print(json.dumps({key: result.get(key) for key in ('intent', 'confidence', 'degraded', 'degraded_reasons', 'retrieval_mode', 'generation_provider', 'generation_model', 'latency_ms')}, ensure_ascii=False), flush=True)
            print(json.dumps({'chat_listings': len(result.get('listings', [])), 'chat_sources': len(result.get('sources', []))}), flush=True)
        checked(web.post('/api/auth/forgot-password', json={'email': email}))
        reset_url = mailbox_text(mail, email, reset=True).strip()
        reset_token = parse_qs(urlparse(reset_url).query)['token'][0]
        new_password = secrets.token_urlsafe(24)
        checked(web.post('/api/auth/reset-password', json={'email': email, 'token': reset_token, 'password': new_password}))
        checked(web.get('/api/auth/me'), 401)
        checked(web.post('/api/auth/login', json={'email': email, 'password': password}), 401)
        checked(web.post('/api/auth/login', json={'email': email, 'password': new_password}))
        checked(web.get('/api/auth/me'))
        checked(web.post('/api/auth/logout'))
        checked(web.get('/api/auth/me'), 401)
        print('password reset, session revocation, login, logout: ok', flush=True)
        print('PASS (test account retained; no credentials printed)', flush=True)


if __name__ == '__main__':
    main()
