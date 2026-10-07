"""Regression cases for source outages, bounded repair and useful coverage."""
import json

import httpx
import pytest

from app.room_service.chatbot.agent_workflow import GeminiAnswerSynthesisAgent, LegalAgentWorkflow
from app.room_service.chatbot.answer_coverage import coverage_requirements, missing_answer_facets
from app.room_service.chatbot.claim_verification import check_claims, ClaimIssues
from app.room_service.chatbot.gemini_selection import GeminiEvidenceSelector
from app.room_service.chatbot.providers import FallbackResponseGenerator, GeminiGenerator
from app.room_service.chatbot.schemas import ChatAskRequest
from app.room_service.chatbot.source_selection import render_selection, selection_candidates
from test_agent_workflow import Client, QUESTION, Repo, answer, draft, rows, service, workflow, prompt_data
from test_claim_verification import records, verdicts


class SequenceVerifier:
    def __init__(self, outputs):
        self.outputs = iter(outputs)
        self.prompts = []

    def request_json(self, prompt, schema):
        self.prompts.append(prompt)
        result = next(self.outputs)
        if isinstance(result, Exception):
            raise result
        return result, {}


@pytest.mark.parametrize('malformed', ['not JSON', '{"verdicts":[]}', json.dumps(dict(
    verdicts=[dict(verdicts()[0], source_ids=[999])]))])
def test_verifier_repairs_structure_once_without_changing_source_binding(malformed):
    client = SequenceVerifier([malformed, json.dumps(dict(verdicts=verdicts()))])
    result = check_claims(client, 'Tra cứu?', records()[0]['rendered'],
                          [dict(rank=2, content='Tra cứu theo mã khách hàng.')], records())
    assert not result and len(client.prompts) == 2
    assert result.attempts[0]['status'] == 'schema_retry'
    assert 'source_ids' in client.prompts[-1]


def test_verifier_does_not_retry_valid_rejection_or_service_failure():
    for output in [RuntimeError('HTTP 503'), json.dumps(dict(verdicts=[dict(verdicts()[0], supported=False)]))]:
        client = SequenceVerifier([output])
        if isinstance(output, Exception):
            with pytest.raises(RuntimeError):
                check_claims(client, 'Tra cứu?', records()[0]['rendered'], [dict(rank=2, content='Nguồn.')], records())
        else:
            result = check_claims(client, 'Tra cứu?', records()[0]['rendered'], [dict(rank=2, content='Nguồn.')], records())
            assert result and not result.verdicts[0]['supported']
        assert len(client.prompts) == 1


def test_invalid_verdict_stops_after_one_repair_and_exposes_sanitized_attempts():
    client = SequenceVerifier(['{"verdicts":[]}', '{"verdicts":[]}'])
    with pytest.raises(ValueError) as caught:
        check_claims(client, 'Tra cứu?', records()[0]['rendered'], [dict(rank=2, content='Nguồn.')], records())
    assert len(client.prompts) == 2
    assert [a['status'] for a in caught.value.verification_attempts] == ['schema_retry', 'invalid']


@pytest.mark.parametrize('statuses,success', [([500, 200], True), ([502, 200], True),
    ([504, 504], False), ([503], False), ([429], False)])
def test_transient_http_retry_is_bounded_and_preserves_overload_quota_policy(statuses, success):
    calls = []
    def handler(request):
        calls.append(request.headers['x-goog-api-key'])
        status = statuses[len(calls) - 1]
        return httpx.Response(status, json={'candidates': [{'content': {'parts': [{'text': '{}'}]}}]})
    client = GeminiGenerator('test', 'test', api_keys=['test', 'unused'], transport=httpx.MockTransport(handler))
    try:
        if success:
            assert client.request_json('prompt', {'type': 'object'})[0] == '{}'
        else:
            with pytest.raises(RuntimeError):
                client.request_json('prompt', {'type': 'object'})
        assert calls == ['test'] * len(statuses)
    finally:
        client.close()


def test_selector_retries_duplicate_ids_once_and_records_both_attempts():
    from test_gemini_selection import Client as SelectionClient
    class RepairClient(SelectionClient):
        def request_json(self, prompt, schema, **kwargs):
            self.output = {'selected_ids': [1, 1] if not self.calls else [1], 'insufficient': False}
            return super().request_json(prompt, schema, **kwargs)
    client = RepairClient()
    result = GeminiEvidenceSelector(client).generate(QUESTION, rows(), context_kind='legal')
    trace = next(s for s in result.agent_trace if s['agent'] == 'selection_decision')
    assert len(client.calls) == 2 and trace['attempts'][0]['status'] == 'schema_retry'
    assert trace['attempts'][1]['selected_ids'] == [1]


def test_selection_outage_keeps_diagnostics_after_extractive_fallback():
    from test_gemini_selection import Client as SelectionClient
    selector_client = SelectionClient(error=RuntimeError('Gemini quá tải (HTTP 503)'))
    writer_client = Client()
    agent = LegalAgentWorkflow(FallbackResponseGenerator([GeminiEvidenceSelector(selector_client)]),
                              GeminiAnswerSynthesisAgent(writer_client), writer_client)
    result = service(agent).ask(ChatAskRequest(message=QUESTION))
    assert len(selector_client.calls) == 1 and writer_client.writes == writer_client.checks == 0
    assert result.degraded and result.no_answer
    assert 'chỉ là nguồn tham khảo' in result.answer
    assert any(s.get('http_status') == 503 for s in result.agent_trace)


@pytest.mark.parametrize('outage_on_recheck', [False, True])
def test_repair_preserves_verified_claims_and_checks_only_changed_or_rejected_claims(outage_on_recheck):
    class ClaimClient(Client):
        supports_claim_records = True
        def check_legal_evidence(self, question, text, contexts, *, claim_records=()):
            self.checks += 1
            ids = [c['claim_id'] for c in claim_records]
            assert ids == (['summary', 'steps:0'] if self.checks == 1 else ['summary'])
            if self.checks == 2 and outage_on_recheck:
                raise RuntimeError('HTTP 503')
            return ClaimIssues([dict(claim_id=c['claim_id'], source_ids=c['source_ranks'], kind=c['kind'],
                supported=c['claim_id'] != 'summary' or self.checks == 2,
                reason='Đối chiếu nội dung trong nguồn.') for c in claim_records])
    agent, selector, client = workflow(ClaimClient())
    result = service(agent).ask(ChatAskRequest(message=QUESTION))
    assert client.writes == client.checks == 2 and selector.calls == 1
    assert answer()['steps'][0]['text'] in result.answer
    assert (answer()['summary']['text'] in result.answer) == (not outage_on_recheck)
    if outage_on_recheck:
        assert result.partial_answer
    assert any(s.get('preserved_claim_ids') == ['steps:0'] for s in result.agent_trace)


def test_shortened_repair_restores_accepted_slots_without_reordering():
    data = answer()
    data['steps'].append(dict(text='Khuyến nghị kiểm tra phương thức thanh toán đã thỏa thuận', source_ranks=[1]))
    agent, _, client = workflow(Client(result=data))
    original = agent.writer.synthesize(QUESTION, draft())
    client.result = answer()
    client.result['steps'] = []
    fixed = agent.repair_legal_answer(QUESTION, original, issues=['Sửa summary'], accepted_ids=['steps:1'])
    assert next(c for c in fixed.claim_records if c['claim_id'] == 'steps:1') == original.claim_records[2]


CONTRACT_QUESTION = 'Trước khi ký hợp đồng thuê trọ, sinh viên nên kiểm tra những điều khoản nào?'
CONTRACT_SOURCE = dict(rows()[0], content='Các bên thỏa thuận giá thuê, thời hạn thanh toán và tiền đặt cọc trong hợp đồng thuê trọ.')


def test_coverage_requires_only_source_supported_facets_and_ignores_uncited_mentions():
    required = coverage_requirements(CONTRACT_QUESTION, [CONTRACT_SOURCE])
    assert {r['facet'] for r in required} == {'contract_rent', 'contract_payment', 'contract_deposit'}
    claim = dict(claim_id='summary', text='Các bên thỏa thuận giá thuê và thanh toán', source_ranks=[1], kind='regulation')
    assert [r['facet'] for r in missing_answer_facets(CONTRACT_QUESTION, [CONTRACT_SOURCE], [claim])] == ['contract_deposit']
    claim['source_ranks'] = [99]
    assert len(missing_answer_facets(CONTRACT_QUESTION, [CONTRACT_SOURCE], [claim])) == 3
    claim.update(source_ranks=[1], text='Chưa đủ căn cứ về giá thuê, thanh toán, tiền đặt cọc', kind='source_limit')
    assert len(missing_answer_facets(CONTRACT_QUESTION, [CONTRACT_SOURCE], [claim])) == 3


@pytest.mark.parametrize('fill_gap', [True, False])
def test_coverage_gap_repairs_once_preserves_good_claims_and_reports_remaining_gap(fill_gap):
    class ContractRepo(Repo):
        def retrieve_legal(self, *args, **kwargs):
            return [CONTRACT_SOURCE]
    class ContractSelector:
        providers = []
        def generate(self, question, contexts, **kwargs):
            return render_selection(question, contexts, selection_candidates(contexts),
                                    '{"selected_ids":[1],"insufficient":false}', 'gemini', 'test')
    class ContractClient(Client):
        supports_claim_records = True
        def request_json(self, prompt, schema, **kwargs):
            data = prompt_data(prompt)
            assert data['REQUIRED_FACETS']
            self.result = answer()
            if self.writes:
                assert data['ACCEPTED_IDS'] == ['summary', 'steps:0']
                assert any('answer_coverage_gap' in str(i) for i in data['ISSUES'])
                if fill_gap:
                    self.result['steps'].append(dict(text='Các bên thỏa thuận tiền đặt cọc trong hợp đồng thuê trọ', source_ranks=[1]))
            return super().request_json(prompt, schema, **kwargs)
        def check_legal_evidence(self, question, text, contexts, *, claim_records=()):
            self.checks += 1
            if self.checks == 2:
                assert [c['claim_id'] for c in claim_records] == ['steps:1']
            return ClaimIssues([dict(claim_id=c['claim_id'], source_ids=c['source_ranks'], kind=c['kind'],
                                     supported=True, reason='Đúng nội dung trong nguồn.') for c in claim_records])
    client = ContractClient()
    agent = LegalAgentWorkflow(ContractSelector(), GeminiAnswerSynthesisAgent(client), client)
    result = service(agent, ContractRepo()).ask(ChatAskRequest(message=CONTRACT_QUESTION))
    assert client.writes == 2 and client.checks == (2 if fill_gap else 1)
    coverage = next(s for s in result.agent_trace if s['agent'] == 'answer_coverage')
    assert coverage['status'] == ('covered' if fill_gap else 'partial')
    assert answer()['summary']['text'] in result.answer
    if not fill_gap:
        assert result.partial_answer and 'thỏa thuận tiền cọc' in result.answer


def test_coverage_does_not_trigger_writer_repair_during_verifier_outage():
    class Unavailable(Client):
        def check_legal_evidence(self, *args, **kwargs):
            self.checks += 1
            raise RuntimeError('HTTP 500')
    agent, _, client = workflow(Unavailable())
    result = service(agent).ask(ChatAskRequest(message=QUESTION))
    assert client.writes == client.checks == 1
    assert result.degraded and 'chỉ là nguồn tham khảo' in result.answer


def test_privacy_coverage_requires_action_before_deadlines_when_source_supports_it():
    question = 'Nếu thông tin cá nhân của tôi bị chia sẻ sai mục đích, tôi nên yêu cầu xử lý như thế nào?'
    source = dict(rank=1, category='privacy_data', content='Yêu cầu hạn chế xử lý được gửi bằng văn bản cho bên kiểm soát dữ liệu; bên tiếp nhận phản hồi theo thời hạn áp dụng.')
    claim = dict(claim_id='summary', kind='regulation', source_ranks=[1], text='Bên tiếp nhận phản hồi theo thời hạn áp dụng')
    missing = {r['facet'] for r in missing_answer_facets(question, [source], [claim])}
    assert {'privacy_form', 'privacy_recipient', 'privacy_request'} <= missing
    assert 'privacy_response' not in missing
