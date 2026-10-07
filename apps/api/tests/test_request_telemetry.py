from concurrent.futures import ThreadPoolExecutor
import httpx
import pytest
from app.room_service.chatbot.providers import GeminiGenerator
from app.room_service.chatbot.request_telemetry import collect_gemini_calls


def test_retry_records_both_http_attempts_and_one_model_call():
    responses = iter([httpx.Response(500), httpx.Response(200, json={
        'candidates': [{'content': {'parts': [{'text': '{}'}]}}],
        'usageMetadata': {'promptTokenCount': 11, 'candidatesTokenCount': 3, 'totalTokenCount': 14}})])
    client = GeminiGenerator('test', 'test', transport=httpx.MockTransport(lambda request: next(responses)))
    calls = []
    with collect_gemini_calls(calls.append):
        _, usage = client.request_json('test', {'properties': {'selected_ids': {}}})
    assert len(calls) == 1
    assert calls[0]['http_request_count'] == 2
    assert [a['http_status'] for a in calls[0]['http_attempts']] == [500, 200]
    assert calls[0]['agent'] == 'evidence_selection'
    assert calls[0]['usage'] == usage
    assert 'test' not in str(calls[0]['http_attempts'])
    client.close()


def test_failed_http_call_is_recorded_without_usage():
    client = GeminiGenerator('test', 'test', transport=httpx.MockTransport(lambda request: httpx.Response(503)))
    calls = []
    with collect_gemini_calls(calls.append), pytest.raises(RuntimeError):
        client.request_json('test', {})
    assert calls[0]['success'] is False
    assert calls[0]['http_attempts'][0]['http_status'] == 503
    assert 'usage' not in calls[0]
    client.close()


def test_concurrent_request_collectors_remain_separate():
    client = GeminiGenerator('test', 'test', transport=httpx.MockTransport(lambda request: httpx.Response(200,
        json={'candidates': [{'content': {'parts': [{'text': '{}'}]}}]})))
    def invoke(stage):
        calls = []
        with collect_gemini_calls(calls.append):
            client.request_json('test', {'properties': {stage: {}}})
        return calls
    with ThreadPoolExecutor(max_workers=2) as pool:
        a, b = list(pool.map(invoke, ['summary', 'search_queries']))
    assert len(a) == len(b) == 1
    assert a[0]['agent'] == 'answer_synthesis'
    assert b[0]['agent'] == 'question_analysis'
    client.close()
