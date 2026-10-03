"""One resumable evaluation job. A 429 pauses the whole job, including collection."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,json,sys,time,subprocess,hashlib,os
import httpx
from quota_checkpoint import quota_metadata
from question_bank_ragas import save_report


def read(path):return json.loads(path.read_text(encoding='utf-8')) if path.exists() else {'cases':[]}
def available():
    from app.config import settings
    if not settings.configured_gemini_keys:raise RuntimeError('No Gemini key configured')
    try:
        response=httpx.post(settings.gemini_base_url+'/models/gemini-3.1-flash-lite:generateContent',
            headers={'x-goog-api-key':settings.configured_gemini_keys[0]},json={
                'contents':[{'parts':[{'text':'Return OK'}]}],
                'generationConfig':{'maxOutputTokens':64,'thinkingConfig':{'thinkingLevel':'low'}}},timeout=45)
    except httpx.TransportError as exc:
        from datetime import timedelta
        return {'status':'paused','error_type':type(exc).__name__,
            'retry_at_utc':(datetime.now(timezone.utc)+timedelta(seconds=60)).isoformat()}
    if response.status_code==429:return quota_metadata(response)
    if response.status_code in (500,502,503,504):
        from datetime import timedelta
        return {'status':'paused','http_status':response.status_code,'retry_at_utc':(datetime.now(timezone.utc)+timedelta(seconds=60)).isoformat()}
    response.raise_for_status();return None


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--max-hours',type=float,default=48)
    parser.add_argument('--phase',choices=('collect','score','all'),default='all')
    args=parser.parse_args()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    status=args.output.with_suffix('.status.json');log=args.output.with_suffix('.log')
    # Kernel releases this writer lock even when the container/process crashes.
    import fcntl
    handle=args.output.with_suffix('.lock').open('a')
    fcntl.flock(handle,fcntl.LOCK_EX|fcntl.LOCK_NB)
    state={'phase':'starting','output':str(args.output),'started_at_utc':datetime.now(timezone.utc).isoformat(),
           'max_runtime_hours':args.max_hours,'quota_events':[],'cutover':'retain original corpus pending verified release gate'}
    deadline=time.monotonic()+args.max_hours*3600
    def publish(**values):
        state.update(values,updated_at_utc=datetime.now(timezone.utc).isoformat())
        data=read(args.output)
        state['completed_answers']=sum('answer' in c for c in data['cases'])
        state['scores']=data.get('summary',{}).get('ragas',{})
        save_report(status,state)
    def wait_quota(quota):
        while quota:
            state['quota_events'].append(quota)
            publish(phase='waiting_for_server',quota=quota)
            target=datetime.fromisoformat(quota['retry_at_utc']).timestamp()
            while time.time()<target:
                if time.monotonic()>deadline:raise TimeoutError('Saved checkpoint; resume this job after finite wait budget')
                time.sleep(min(30,max(.1,target-time.time())))
            quota=available()
        publish(quota=None)
    try:
        phases=['collect','score'] if args.phase=='all' else [args.phase]
        for phase in phases:
            prior=read(args.output).get('quota_state')
            if prior:wait_quota(prior)
            while True:
                if time.monotonic()>deadline:raise TimeoutError('Finite evaluation runtime exceeded; checkpoint retained')
                publish(phase=phase)
                cmd=[sys.executable,'/eval/question_bank_ragas.py','--output',str(args.output),'--phase',phase]
                if phase=='score':cmd+=['--judge-provider','gemini','--judge-model','gemini-3.1-flash-lite',
                    '--score-workers','4','--judge-max-output-tokens','8192','--score-abstentions']
                with log.open('a',encoding='utf-8') as stream:
                    process=subprocess.Popen(cmd,stdout=stream,stderr=subprocess.STDOUT)
                    try:
                        while process.poll() is None:
                            if time.monotonic()>deadline:raise TimeoutError('Finite evaluation runtime exceeded')
                            try:process.wait(timeout=15)
                            except subprocess.TimeoutExpired:pass
                            publish()
                    finally:
                        if process.poll() is None:process.terminate();process.wait(timeout=20)
                if process.returncode==75:
                    wait_quota(read(args.output)['quota_state']);continue
                if process.returncode:raise RuntimeError('Evaluation process exited '+str(process.returncode)+'; see local log')
                break
        report=read(args.output)
        complete=len(report['cases'])==36 and all('answer' in c and all(isinstance(c.get('ragas',{}).get(m),(int,float))
            for m in ('faithfulness','answer_relevancy','context_utilization')) for c in report['cases'])
        publish(phase='complete' if complete else 'complete_with_errors')
    except Exception as exc:
        publish(phase='stopped_with_checkpoint',error_type=type(exc).__name__,error=str(exc)[:300]);raise
    finally:handle.close()

if __name__=='__main__':main()
