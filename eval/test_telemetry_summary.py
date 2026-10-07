from telemetry_summary import summarize_calls


def test_native_usage_and_http_retry_do_not_double_count_wrapper():
    rows = [dict(provider_calls=[dict(provider='gemini', request_kind='workflow_wrapper'),
        dict(provider='gemini', success=True, http_request_count=2, http_attempts=[dict(http_status=500), dict(http_status=200)],
             usage=dict(promptTokenCount=10, candidatesTokenCount=4, thoughtsTokenCount=2, totalTokenCount=16))])]
    result = summarize_calls(rows)
    assert result['model_calls'] == 1 and result['http_requests'] == 2
    assert result['total_tokens'] == 16 and result['thought_tokens'] == 2
    assert result['http_errors'] == 1 and result['usage_complete']


def test_missing_usage_is_unknown_and_incomplete():
    result = summarize_calls([dict(provider_calls=[dict(provider='gemini', success=False)])])
    assert result['total_tokens'] is None
    assert not result['usage_complete']
