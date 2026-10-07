import json
from types import SimpleNamespace

import pytest
from pydantic import ValidationError

from app.room_service.chatbot.gemini_selection import (
    GeminiEvidenceSelector, GeminiCombinedWriter, GeminiCombinedWorkflow)
from app.room_service.chatbot.providers import FallbackResponseGenerator, DeterministicFakeEmbedder
from app.room_service.chatbot.schemas import ChatAskRequest
from test_agent_workflow import QUESTION, rows, answer, service


class Client:
    model = 'proxy-test'
    def __init__(self, output=None, error=None):
        self.output = output
        self.error = error
        self.calls = []
    def request_json(self, prompt, schema, **kwargs):
        self.calls.append((prompt, schema))
        if self.error:
            raise self.error
        return json.dumps(self.output, ensure_ascii=False), {'promptTokenCount': 10}
    def check_legal_evidence(self, *args, **kwargs):
        return []
    def close(self): pass


def combined(client):
    selector = FallbackResponseGenerator([GeminiEvidenceSelector(client)])
    return GeminiCombinedWorkflow(selector, GeminiCombinedWriter(client), client)


def test_selector_materializes_only_existing_verbatim_evidence():
    client = Client({'selected_ids': [1], 'insufficient': False})
    result = GeminiEvidenceSelector(client).generate(QUESTION, rows(), context_kind='legal')
    assert result.literal_source_answer and result.provider == 'gemini'
    assert result.selected_evidence[0]['content'] == rows()[0]['content']
    assert rows()[1]['content'] not in result.text


@pytest.mark.parametrize('ids', [[True], ['1'], [1, 1], [99], [1, 2, 3, 4, 5]])
def test_invalid_selection_never_becomes_evidence(ids):
    client = Client({'selected_ids': ids, 'insufficient': False})
    with pytest.raises((ValueError, ValidationError)):
        GeminiEvidenceSelector(client).generate(QUESTION, rows(), context_kind='legal')


def test_empty_and_nonlegal_contexts_do_not_call_proxy():
    client = Client()
    selector = GeminiEvidenceSelector(client)
    selector.generate(QUESTION, [], context_kind='legal')
    selector.generate('Tìm phòng', [], context_kind='listing')
    selector.generate('Tìm phòng', [dict(id=1, rank=1, title='Phòng thử', price=1200000,
        address='Dữ liệu giả trong test', similarity_score=.9)], context_kind='listing')
    for changes in ({'address':'private'}, {'category':'find_listing'}, {'document_id':None}):
        with pytest.raises(ValueError):
            selector.generate(QUESTION, [dict(rows()[0], **changes)], context_kind='legal')
    assert client.calls == []


def test_empty_selection_is_an_explicit_abstention():
    client = Client({'selected_ids': [], 'insufficient': True})
    result = GeminiEvidenceSelector(client).generate(QUESTION, rows(), context_kind='legal')
    assert not result.selected_evidence and not result.literal_source_answer
    client.output['insufficient'] = False
    with pytest.raises(ValueError):
        GeminiEvidenceSelector(client).generate(QUESTION, rows(), context_kind='legal')


def test_combined_uses_one_generation_call_and_verifies_selected_claims():
    client = Client({'selection': {'selected_ids': [1], 'insufficient': False}, 'answer': answer()})
    result = service(combined(client)).ask(ChatAskRequest(message=QUESTION))
    assert len(client.calls) == 1
    assert result.generation_provider == 'gemini-agent'
    assert '[1]' in result.answer and '[2]' not in result.answer
    assert any(s.get('mode') == 'combined' for s in result.agent_trace)


def test_combined_cannot_cite_unselected_source():
    client = Client({'selection': {'selected_ids': [1], 'insufficient': False}, 'answer': answer(ranks=[2])})
    result = combined(client).generate_legal(QUESTION, rows())
    assert result.literal_source_answer
    assert rows()[0]['content'] in result.text and rows()[1]['content'] not in result.text
    assert any(s.get('status') == 'fallback' for s in result.agent_trace)


def test_combined_semantic_repair_reuses_sources_and_stops_after_one_repair():
    class Rejected(Client):
        checks = 0
        def request_json(self, prompt, schema, **kwargs):
            self.output = ({'selection': {'selected_ids': [1], 'insufficient': False},
                            'answer': answer()} if 'selection' in schema['properties'] else answer())
            return super().request_json(prompt, schema, **kwargs)
        def check_legal_evidence(self, question, text, contexts, **kwargs):
            self.checks += 1
            assert [r['rank'] for r in contexts] == [1]
            return ['Kết luận chưa được nguồn xác nhận.']
    client = Rejected()
    result = service(combined(client)).ask(ChatAskRequest(message=QUESTION))
    assert len(client.calls) == client.checks == 2
    assert sum('selection' in schema['properties'] for _, schema in client.calls) == 1
    assert result.generation_provider == 'gemini'
    assert rows()[0]['content'] in result.answer and rows()[1]['content'] not in result.answer
    assert result.degraded


def test_combined_verifier_failure_does_not_publish_unverified_synthesis():
    class Unavailable(Client):
        def check_legal_evidence(self, *args, **kwargs):
            raise RuntimeError('HTTP 429')
    client = Unavailable({'selection': {'selected_ids': [1], 'insufficient': False}, 'answer': answer()})
    result = service(combined(client)).ask(ChatAskRequest(message=QUESTION))
    assert result.generation_provider != 'gemini-agent'
    assert result.degraded
    assert all(s.get('provider') != 'qwen_and_rules' for s in result.agent_trace)


def test_combined_preserves_partial_selection():
    client = Client({'selection': {'selected_ids': [1], 'insufficient': True}, 'answer': answer()})
    result = combined(client).generate_legal(QUESTION, rows())
    assert result.evidence_limitations and 'Chưa đủ căn cứ' in result.text


def test_combined_schema_retry_is_bounded_and_proxy_error_not_retried():
    client = Client({'selection': {'selected_ids': [True], 'insufficient': False}, 'answer': answer()})
    result = combined(client).generate_legal(QUESTION, rows())
    assert len(client.calls) == 2 and not result.claim_records
    client = Client(error=RuntimeError('HTTP 429'))
    result = combined(client).generate_legal(QUESTION, rows())
    assert len(client.calls) == 1 and not result.claim_records


@pytest.mark.parametrize('mode', ['separate', 'combined'])
def test_router_gemini_mode_never_constructs_or_warms_ollama(monkeypatch, mode):
    from app.config import Settings
    from app.room_service.chatbot import router
    monkeypatch.setattr(router, 'settings', Settings(_env_file=None, chatbot_agents_enabled=True,
        chatbot_graph_enabled=False, chatbot_legal_selection_provider='gemini',
        chatbot_legal_generation_mode=mode, gemini_api_key='test-only'))
    monkeypatch.setattr(router, '_service', None)
    class Forbidden:
        def __init__(self, *a, **kw): raise AssertionError('Ollama must not be constructed')
    monkeypatch.setattr(router, 'OllamaQwenGenerator', Forbidden, raising=False)
    monkeypatch.setattr(router, 'E5EmbeddingProvider', lambda *a: DeterministicFakeEmbedder())
    router.init_chatbot(object())
    providers = router.get_service().generator.providers
    assert len(providers) == 1 and isinstance(providers[0], GeminiEvidenceSelector)
    router.warmup_chatbot()
    router.close_chatbot()


@pytest.mark.parametrize('changes', [dict(chatbot_agents_enabled=False),
    dict(chatbot_legal_selection_provider='qwen'), dict(chatbot_answer_synthesis_enabled=False)])
def test_invalid_combined_configuration_fails_before_constructing_clients(monkeypatch, changes):
    from app.config import Settings
    from app.room_service.chatbot import router
    config = dict(chatbot_agents_enabled=True, chatbot_legal_selection_provider='gemini',
        chatbot_legal_generation_mode='combined', chatbot_answer_synthesis_enabled=True)
    config.update(changes)
    monkeypatch.setattr(router, 'settings', Settings(_env_file=None, **config))
    with pytest.raises(ValueError, match='requires Gemini'):
        router.init_chatbot(object())


def test_boundary_checks_new_cloud_entrypoints_before_call():
    from test_legal_only_boundary import Connection
    from legal_only_boundary import install
    client = Client({'selection': {'selected_ids': [1], 'insufficient': False}, 'answer': answer()})
    agent = combined(client)
    current = service(agent)
    install(current, SimpleNamespace(connect=lambda: Connection()),
            [{'category':'housing_contract','question':QUESTION}], 'legal_test')
    for bad in (dict(rows()[0], document_id=999), dict(rows()[0], phone='private')):
        with pytest.raises(ValueError):
            agent.writer.select_and_synthesize(QUESTION, [bad])
        with pytest.raises(ValueError):
            agent.providers[0].generate(QUESTION, [bad], context_kind='legal')
    assert client.calls == []
