import json
import httpx
import pytest
from pydantic import BaseModel
from ollama_judge import OllamaRagasLLM


class Verdict(BaseModel):
    supported: bool


def test_local_mode_constructs_only_ollama_even_with_cloud_keys(monkeypatch):
    from app.config import Settings
    from app.room_service.chatbot import router
    from app.room_service.chatbot.providers import OllamaQwenGenerator
    monkeypatch.setattr(router, 'settings', Settings(_env_file=None, chatbot_llm_provider='qwen', gemini_api_key_1='unused'))
    monkeypatch.setattr(router, '_service', None)
    router.init_chatbot(None)
    providers = router.get_service().generator.providers
    assert len(providers) == 1 and isinstance(providers[0], OllamaQwenGenerator)
    providers[0].close()


def test_local_judge_saves_verdict_and_rejects_truncated_json(monkeypatch):
    calls = []
    def post(url, **kwargs):
        calls.append(kwargs)
        return httpx.Response(200, request=httpx.Request('POST', url), json={
            'message': {'content': json.dumps({'supported': True})}, 'done_reason': 'stop',
            'prompt_eval_count': 30, 'eval_count': 5})
    monkeypatch.setattr(httpx, 'post', post)
    judge = OllamaRagasLLM('http://localhost:11434', 'qwen3.5:9b')
    assert judge.generate('claim', Verdict).supported
    assert judge.judgements == [{'schema': 'Verdict', 'output': {'supported': True}}]
    assert calls[0]['timeout'] == 300
    assert calls[0]['json']['think'] is False
    response = httpx.Response(200, request=httpx.Request('POST', judge.url), json={
        'message': {'content': '{"supported":true}'}, 'done_reason': 'length'})
    with pytest.raises(RuntimeError, match='token limit'):
        judge._parse(response, Verdict)
    assert len(judge.judgements) == 1
