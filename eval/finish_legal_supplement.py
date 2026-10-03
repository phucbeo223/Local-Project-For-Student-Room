"""Finish this one evaluation job after collection and the server's quota delay.

This is a finite worker for the current authorized test, not a recurring monitor.
No keys, request headers or project IDs are written to reports.
"""
from pathlib import Path
from datetime import datetime,timezone,timedelta
from zoneinfo import ZoneInfo
import argparse,hashlib,json,subprocess,sys,time,re
import httpx
from app.config import settings

BASE=Path('/eval/reports')
REPORT=BASE/'legal_supplement_release_2026-10-03.json'
STATUS=BASE/'legal_supplement_job_status_2026-10-03.json'
LOG=BASE/'legal_supplement_scoring_2026-10-03.log'

def read(p): return json.loads(p.read_text(encoding='utf-8'))
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def stamp(state,**fields):
    state.update(fields,updated_at_utc=datetime.now(timezone.utc).isoformat())
    temp=STATUS.with_suffix('.tmp')
    temp.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    temp.replace(STATUS)

def verify_sources():
    raw=Path('/source-docs/legal_sources_originals_20261003')
    manifest=read(raw/'download_manifest.json')
    from urllib.parse import urlparse
    allowed={'datafiles.chinhphu.vn','www.bocongan.gov.vn','congan.lamdong.gov.vn'}
    for source in manifest['sources']:
        assert urlparse(source['download_url']).hostname in allowed
        path=raw/Path(source['path']).name
        assert digest(path)==source['sha256'], source['id']
    return len(manifest['sources'])

def availability():
    if not settings.configured_gemini_keys: raise RuntimeError('No configured credential')
    response=httpx.post(settings.gemini_base_url+'/models/gemini-3.1-flash-lite:generateContent',
        headers={'x-goog-api-key':settings.configured_gemini_keys[0]},
        json={'contents':[{'parts':[{'text':'Return OK'}]}],
              'generationConfig':{'maxOutputTokens':64,'thinkingConfig':{'thinkingLevel':'low'}}},timeout=45)
    if response.is_success:return 0,[]
    if response.status_code not in (429,503):raise RuntimeError('Judge HTTP '+str(response.status_code))
    delay=60.0
    quota=[]
    for detail in response.json().get('error',{}).get('details',[]):
        if 'RetryInfo' in detail.get('@type',''):
            m=re.fullmatch(r'(\d+(?:\.\d+)?)s',detail.get('retryDelay',''))
            if m:delay=max(delay,float(m[1]))
        for v in detail.get('violations',[]):
            quota.append({k:v.get(k) for k in ['quotaMetric','quotaId','quotaValue']})
    if any('PerDay' in (q.get('quotaId') or '') for q in quota):
        pacific=datetime.now(ZoneInfo('America/Los_Angeles'))
        reset=datetime.combine(pacific.date()+timedelta(days=1),datetime.min.time(),pacific.tzinfo)
        delay=max(delay,(reset-pacific).total_seconds()+5)
    return delay,quota

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--deployed-image',required=True);args=parser.parse_args()
    state={'started_at_utc':datetime.now(timezone.utc).isoformat(),'phase':'waiting_for_answers',
           'deployed_image':args.deployed_image,'baseline_sha256':digest(BASE/'legal_model_upgrade_after_2026-10-02.json'),
           'verified_official_downloads':verify_sources(),'max_runtime_hours':24,'completed':0}
    deadline=time.monotonic()+24*3600
    stamp(state)
    try:
        last=-1
        while time.monotonic()<deadline:
            report=read(REPORT) if REPORT.exists() else {'cases':[]}
            count=sum('answer' in c for c in report['cases'])
            if count!=last:
                stamp(state,completed=count)
                print('Collected',count,'/36',flush=True);last=count
            if count==36:break
            time.sleep(15)
        else:raise RuntimeError('Collection did not complete within 24 hours')
        # A final retrieval correction prioritizes the actual owner/authorization
        # clause. Preserve the earlier result and rerun only the affected question.
        report=read(REPORT)
        q22=next(c for c in report['cases'] if c['id']==22)
        if not any('Điều 161.' in (s.get('heading') or '') for s in q22.get('sources',[])):
            report.setdefault('rerun_history',[]).append({'id':22,'reason':'Ưu tiên căn cứ chủ sở hữu/người được ủy quyền thay vì chỉ điều kiện nhà ở','previous':q22.copy()})
            preserved={k:q22[k] for k in ['id','question','category']}
            q22.clear();q22.update(preserved)
            REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
            stamp(state,phase='rechecking_affected_question',rerun_ids=[22])
            with LOG.open('a',encoding='utf-8') as log:
                subprocess.run([sys.executable,'/eval/question_bank_ragas.py','--output',str(REPORT),'--phase','collect','--ids','22'],stdout=log,stderr=subprocess.STDOUT,check=True)
        for attempt in range(3):
            while time.monotonic()<deadline:
                delay,quota=availability()
                if not delay:break
                until=time.monotonic()+delay
                stamp(state,phase='waiting_for_judge_quota',quota=quota,
                      retry_at_utc=(datetime.now(timezone.utc)+timedelta(seconds=delay)).isoformat())
                print('Judge quota delay',round(delay),'seconds',flush=True)
                while time.monotonic()<min(until,deadline):time.sleep(min(60,max(.1,until-time.monotonic())))
            else:raise RuntimeError('Judge remained unavailable within 24 hours')
            stamp(state,phase='scoring',scoring_attempt=attempt+1,quota=[])
            with LOG.open('a',encoding='utf-8') as log:
                result=subprocess.run([sys.executable,'/eval/question_bank_ragas.py','--output',str(REPORT),
                    '--phase','score','--judge-model','gemini-3.1-flash-lite','--judge-provider','gemini',
                    '--score-workers','4','--judge-max-output-tokens','8192','--score-abstentions'],stdout=log,stderr=subprocess.STDOUT)
            if result.returncode:raise RuntimeError('Scoring worker exited '+str(result.returncode))
            report=read(REPORT)
            scored={m:report['summary']['ragas'][m]['scored'] for m in ['faithfulness','answer_relevancy','context_utilization']}
            stamp(state,scored=scored)
            if all(n==36 for n in scored.values()):break
        stamp(state,phase='rendering')
        subprocess.run([sys.executable,'/eval/report_legal_supplement.py'],check=True)
        stamp(state,phase='complete' if all(n==36 for n in scored.values()) else 'complete_with_scoring_errors',
              result_report='/eval/ragas_reports/legal_supplement_comparison_2026-10-03.md')
    except Exception as exc:
        stamp(state,phase='blocked',error_type=type(exc).__name__,error=str(exc)[:250])
        raise

if __name__=='__main__':main()
