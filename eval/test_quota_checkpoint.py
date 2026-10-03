from datetime import datetime,timezone
import threading
import httpx,pytest
from quota_checkpoint import quota_metadata,QuotaCoordinator,QuotaPause,bounded_scoring,checkpoint_pause


def test_retry_after_and_daily_reset_do_not_expose_project_or_key():
    response=httpx.Response(429,headers={'Retry-After':'120'},json={'error':{'details':[
        {'@type':'RetryInfo','retryDelay':'180s'},
        {'violations':[{'quotaId':'RequestsPerDay','quotaMetric':'requests','quotaValue':'20','quotaDimensions':{'project':'secret'}}]}]}})
    state=quota_metadata(response,datetime(2026,10,4,6,50,tzinfo=timezone.utc))
    assert state['retry_at_utc']=='2026-10-04T07:00:05+00:00'
    assert 'secret' not in str(state) and state['daily_quota']


def test_quota_stops_queue_and_saves_inflight_successes():
    coordinator=QuotaCoordinator();barrier=threading.Barrier(2);pause_received=threading.Event();called=[];saved=[]
    def work(n):
        called.append(n);barrier.wait(timeout=5)
        if n==0:
            coordinator.state={'status':'paused'};pause_received.set();raise QuotaPause('429')
        assert pause_received.wait(5)
        return .75
    with pytest.raises(QuotaPause):
        bounded_scoring([(n,) for n in range(108)],work,lambda task,value:saved.append((task,value)),coordinator,2)
    assert sorted(called)==[0,1] and saved==[((1,),.75)]


def test_checkpoint_does_not_turn_unfinished_question_into_error(tmp_path):
    import json
    coordinator=QuotaCoordinator();coordinator.state={'status':'paused','retry_at_utc':'2026-10-04T07:00:05+00:00'}
    report={'cases':[{'id':1,'question':'one','category':'electricity','answer':'literal','ragas':{'faithfulness':.9}},
                     {'id':2,'question':'two','category':'electricity'}]}
    checkpoint_pause(report,tmp_path/'report.json',coordinator,'collect')
    actual=json.loads((tmp_path/'report.json').read_text())
    assert actual['cases'][0]['ragas']['faithfulness']==.9
    assert 'error' not in actual['cases'][1] and 'answer' not in actual['cases'][1]
    assert actual['quota_state']['phase']=='collect'
