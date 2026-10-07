"""Normalize real usage, preserving missing counts instead of inventing zeros."""


def normalize_usage(usage):
    if not isinstance(usage, dict):
        return {}
    aliases = {'prompt_tokens': ('promptTokenCount', 'prompt_tokens', 'prompt_eval_count'),
               'completion_tokens': ('candidatesTokenCount', 'completion_tokens', 'eval_count'),
               'thought_tokens': ('thoughtsTokenCount', 'thought_tokens'),
               'total_tokens': ('totalTokenCount', 'total_tokens')}
    return {key: value for key, names in aliases.items()
            for value in [next((usage[n] for n in names if type(usage.get(n)) is int and usage[n] >= 0), None)]
            if value is not None}


def summarize_calls(cases):
    calls = [c for row in cases for c in row.get('provider_calls', [])
             if c.get('provider') == 'gemini' and c.get('request_kind') != 'workflow_wrapper']
    usage = [normalize_usage(c.get('usage')) for c in calls]
    # Historical artifacts lack model-call traces for some roles. Never add
    # agent usage to those traces: the same request could be counted twice.
    sums = {key: sum(u[key] for u in usage if key in u) if any(key in u for u in usage) else None
            for key in ('prompt_tokens', 'completion_tokens', 'thought_tokens', 'total_tokens')}
    return dict(model_calls=len(calls), model_call_errors=sum(c.get('success') is False for c in calls),
        http_requests=sum(c['http_request_count'] for c in calls if 'http_request_count' in c) if any('http_request_count' in c for c in calls) else None,
        http_coverage_calls=sum('http_request_count' in c for c in calls),
        http_errors=sum(a.get('http_status', 0) >= 400 or 'error_type' in a for c in calls for a in c.get('http_attempts', [])) if any('http_request_count' in c for c in calls) else None,
        usage_reported=any(usage), usage_coverage_calls=sum(bool(u) for u in usage),
        usage_complete=bool(calls) and all('total_tokens' in u for u in usage), **sums,
        note='Reported API response usage only; candidates and thoughts are separate. Missing usage is unknown. Historical traces may omit roles; HTTP attempts are counted only when recorded.')


def summarize_usage(usage):
    normalized = [normalize_usage(item) for item in usage]
    def total(key):
        return sum(item[key] for item in normalized if key in item) if any(key in item for item in normalized) else None
    prompts = [item['prompt_tokens'] for item in normalized if 'prompt_tokens' in item]
    return dict(requests=len(usage), prompt_tokens=total('prompt_tokens'),
                output_tokens=total('completion_tokens'), thought_tokens=total('thought_tokens'),
                total_tokens=total('total_tokens'), max_prompt_tokens=max(prompts, default=None),
                usage_coverage_requests=sum(bool(item) for item in normalized),
                usage_complete=bool(normalized) and all('total_tokens' in item for item in normalized))
