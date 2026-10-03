"""One resumable evaluation job. A 429 pauses the whole job, including collection."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,json,sys,time,subprocess,hashlib,os,math
import httpx
from quota_checkpoint import quota_metadata
from question_bank_ragas import save_report


def read(path):return json.loads(path.read_text(encoding='utf-8')) if path.exists() else {'cases':[]}
def completion_phase(report,expected_cases):
    cases=report['cases']
    def scored(c):
        return all(isinstance(c.get('ragas',{}).get(m),(int,float)) and math.isfinite(c['ragas'][m])
            for m in ('faithfulness','answer_relevancy','context_utilization'))
    answered=len(cases)==expected_cases and all('answer' in c and not c.get('error') for c in cases)
    if answered and all(scored(c) for c in cases):return 'complete'
    if answered and all(scored(c) or (not c.get('contexts') and c.get('unscorable_reason')) for c in cases):
        return 'complete_with_unscorable_cases'
    return 'complete_with_errors'

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
    parser.add_argument('--runner',choices=('/eval/question_bank_ragas.py','/eval/housing_question_bank_ragas.py'),default='/eval/question_bank_ragas.py')
    parser.add_argument('--questions',type=Path)
    parser.add_argument('--expected-cases',type=int,default=36)
    parser.add_argument('--score-workers',type=int,choices=range(1,5),default=4)
    parser.add_argument('--report-runner',choices=('/eval/report_housing_evaluation.py',))
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
                cmd=[sys.executable,args.runner,'--output',str(args.output),'--phase',phase]
                if args.questions:cmd+=['--questions',str(args.questions)]
                if phase=='score':cmd+=['--judge-provider','gemini','--judge-model','gemini-3.1-flash-lite',
                    '--score-workers',str(args.score_workers),'--judge-max-output-tokens','8192','--score-abstentions']
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
        publish(phase=completion_phase(report,args.expected_cases))
        if args.report_runner:
            with log.open('a',encoding='utf-8') as stream:
                subprocess.run([sys.executable,args.report_runner,'--input',str(args.output)],
                    stdout=stream,stderr=subprocess.STDOUT,check=True,timeout=120)
    except Exception as exc:
        publish(phase='stopped_with_checkpoint',error_type=type(exc).__name__,error=str(exc)[:300]);raise
    finally:handle.close()

if __name__=='__main__':main()
