"""Authenticated HTTP smoke using a temporary local test account, removed afterward."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,json,time,uuid
from urllib.parse import urlparse
import httpx
from sqlalchemy import create_engine,text
from app.config import settings
from app.auth.security import make_access_token

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--base-url',default='http://nckh-api-legal-preview-v10:8000')
    parser.add_argument('--output',type=Path,default=Path('/eval/reports/legal_agent_http_preview_2026-10-03.json'))
    parser.add_argument('--message',default='Khi chuyển sang phòng trọ khác, sinh viên nên cập nhật thông tin cư trú như thế nào?')
    parser.add_argument('--expect-web-source',action='store_true')
    parser.add_argument('--expect-schema',default='legal_v2')
    args=parser.parse_args()
    address=urlparse(args.base_url)
    if address.scheme!='http' or address.hostname not in ('nckh-api-legal-preview-v10','nckh-api-legal-preview-v11','nckh-api-legal-preview-v12','nckh-api-legal-preview-v13','nckh-api-legal-preview-v14','api','127.0.0.1','localhost'):
        raise ValueError('Smoke test only supports the local application')
    engine=create_engine(settings.database_url)
    email='legal-agent-smoke-'+uuid.uuid4().hex+'@example.test'
    user_id=None
    result={'base_url':args.base_url,'started_at_utc':datetime.now(timezone.utc).isoformat(),
            'temporary_user_removed':False,'passed':False}
    try:
        with engine.begin() as conn:
            user=dict(conn.execute(text('INSERT INTO users(email,name,email_verified) VALUES(:email,:name,true) '
                'RETURNING id,role,auth_version'),{'email':email,'name':'Legal agent HTTP evaluation'}).mappings().one())
            user_id=user['id']
        token=make_access_token(user_id,user['role'],user['auth_version'])
        with httpx.Client(timeout=480,follow_redirects=False) as client:
            health=client.get(args.base_url+'/health',timeout=10)
            result['health_status']=health.status_code
            message=args.message
            anonymous=client.post(args.base_url+'/chat/ask',json={'message':message},timeout=10)
            result['anonymous_status']=anonymous.status_code
            started=time.perf_counter()
            response=client.post(args.base_url+'/chat/ask',json={'message':message},
                                  headers={'Authorization':'Bearer '+token})
            result['http_status']=response.status_code
            result['latency_ms']=round((time.perf_counter()-started)*1000)
            if response.status_code!=200:raise RuntimeError('Chat endpoint returned HTTP '+str(response.status_code))
            body=response.json()
            result['response']=body
            result['passed']=(health.status_code==200 and anonymous.status_code in (401,403) and
                body.get('corpus_schema')==args.expect_schema and bool(body.get('sources')) and
                any((t.get('agent')=='answer' and t.get('attempted_provider')=='qwen-local') or
                    (t.get('agent')=='evidence_selection' and t.get('provider')=='qwen-local')
                    for t in body.get('agent_trace',[])) and
                body.get('generation_provider')!='gemini')
            if args.expect_web_source:
                result['web_source_returned']=any(s.get('page_kind')=='web_excerpt' for s in body.get('sources',[]))
                result['passed']=result['passed'] and result['web_source_returned']
    except Exception as exc:
        result['error_type']=type(exc).__name__
    finally:
        if user_id is not None:
            with engine.begin() as conn:
                deleted=conn.execute(text('DELETE FROM users WHERE id=:id AND email=:email'),{'id':user_id,'email':email})
                result['temporary_user_removed']=deleted.rowcount==1
        result['passed']=result['passed'] and result['temporary_user_removed']
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(json.dumps({k:v for k,v in result.items() if k!='response'},ensure_ascii=False),flush=True)
        engine.dispose()
    if not result['passed']:raise SystemExit(2)

if __name__=='__main__':main()
