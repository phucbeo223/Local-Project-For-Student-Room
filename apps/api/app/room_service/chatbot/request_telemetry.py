"""Request-local Gemini telemetry; no prompts, responses or credentials."""
from contextlib import contextmanager
from contextvars import ContextVar
import time

_sink = ContextVar('gemini_telemetry_sink', default=None)
_http_attempts = ContextVar('gemini_http_attempts', default=None)


@contextmanager
def collect_gemini_calls(sink):
    token = _sink.set(sink)
    try:
        yield
    finally:
        _sink.reset(token)


@contextmanager
def json_call(model, schema):
    properties = schema.get('properties', {})
    stage = ('selection_and_synthesis' if 'selection' in properties else
             'answer_synthesis' if 'summary' in properties else
             'question_analysis' if 'search_queries' in properties else
             'evidence_selection' if 'selected_ids' in properties else
             'evaluation_audit' if 'checks' in properties else
             'evaluation_comparison' if any(k.startswith('r') and k[1:].isdigit() for k in properties) else
             'source_verification')
    record = dict(provider='gemini', model=model, method='request_json', agent=stage,
                  request_kind='model_call', success=False, http_attempts=[])
    started = time.perf_counter()
    token = _http_attempts.set(record['http_attempts'])
    try:
        yield record
        record['success'] = True
    except Exception as exc:
        record['error_type'] = type(exc).__name__
        raise
    finally:
        _http_attempts.reset(token)
        record['latency_ms'] = round((time.perf_counter() - started) * 1000)
        record['http_request_count'] = len(record['http_attempts'])
        sink = _sink.get()
        if sink is not None:
            sink(record)


def post_with_telemetry(client, *args, **kwargs):
    started = time.perf_counter()
    attempt = {}
    try:
        response = client.post(*args, **kwargs)
        attempt['http_status'] = response.status_code
        return response
    except Exception as exc:
        attempt['error_type'] = type(exc).__name__
        raise
    finally:
        attempt['latency_ms'] = round((time.perf_counter() - started) * 1000)
        current = _http_attempts.get()
        if current is not None:
            current.append(attempt)
