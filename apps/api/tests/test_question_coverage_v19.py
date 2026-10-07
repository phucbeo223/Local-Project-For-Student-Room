from dataclasses import replace
import time
import pytest
from app.room_service.chatbot.answer_coverage import source_coverage, answer_coverage, question_facets
from app.room_service.chatbot.legal_retrieval import legal_completion_status
from app.room_service.chatbot.agent_workflow import SynthesizedLegalAnswer
from test_agent_workflow import workflow, draft, answer, service, QUESTION
from app.room_service.chatbot.schemas import ChatAskRequest


def test_empty_requirements_are_not_evaluated():
    assert source_coverage('Câu hỏi không nhận diện', [])['status'] == 'not_evaluated'
    assert answer_coverage('Câu hỏi không nhận diện', [], [])['status'] == 'not_evaluated'


@pytest.mark.parametrize('question', [
    'Ba người thuê ở chung, tiền điện được tính thế nào?',
    'Tiền nước khoán theo đầu người cần làm rõ gì?',
    'Nhà trọ nhiều phòng cần đáp ứng yêu cầu PCCC nào?',
    'Tôi cần kiểm tra người đăng và nguồn tin thế nào?',
    'Link lạ để trả cọc cần kiểm tra gì?',
    'Đã chuyển cọc cho tin giả mạo, lưu bằng chứng gì và trình báo ở đâu?'])
def test_question_requirements_exist_even_when_all_sources_are_absent(question):
    check = source_coverage(question, [])
    assert check['required_facets'] and check['missing_facets'] and check['status'] == 'partial'


def test_fire_specific_exit_question_does_not_require_all_facets_or_penalties():
    assert set(question_facets('PCCC: lối thoát bị khóa thì làm sao?')) == {'fire_exit'}


def test_source_and_answer_gaps_are_distinct_and_require_cited_claims():
    question = 'Link lạ để chuyển cọc có dấu hiệu gì?'
    rows = [dict(rank=1, content='Kiểm tra liên kết giả mạo; không cung cấp mật khẩu OTP; tránh bị thúc ép chuyển tiền.')]
    assert source_coverage(question, rows)['status'] == 'covered'
    claims = [dict(text='Kiểm tra liên kết giả mạo', kind='recommendation', source_ranks=[1])]
    assert answer_coverage(question, rows, claims)['status'] == 'partial'
    assert len(answer_coverage(question, rows, claims)['missing_facets']) == 2


@pytest.mark.parametrize('notice', [
    'Nguồn là bản trích tuyển cung cấp chưa xác minh toàn bộ câu chữ với bản chính thức',
    'Bản Word chưa đối chiếu đầy đủ với nguyên văn chính thức',
    'Chưa xác minh xuất xứ của bản trích tuyển'])
def test_provenance_paraphrase_does_not_change_structured_content_status(notice):
    agent, _, _ = workflow()
    data = answer()
    data['limitations'] = [dict(text=notice, source_ranks=[1], kind='source_limit')]
    result = agent.writer.render_answer(SynthesizedLegalAnswer.model_validate(data),
        replace(draft(), provenance_status='limited'), started=time.perf_counter())
    assert legal_completion_status(result.text, content_completeness=result.content_completeness) == 'complete'
    assert notice in result.text and result.provenance_status == 'limited'


def test_actual_selector_gap_cannot_be_erased_by_complete_writer():
    agent, _, _ = workflow()
    result = agent.writer.render_answer(SynthesizedLegalAnswer.model_validate(answer()), draft(insufficient=True), started=time.perf_counter())
    assert result.content_completeness == 'partial'


def test_api_serializes_coverage_separately_from_provenance():
    agent, _, _ = workflow()
    result = service(agent).ask(ChatAskRequest(message=QUESTION)).model_dump()
    assert result['content_completeness'] == 'complete'
    assert result['answer_coverage_status'] == 'not_evaluated'
    assert 'provenance_status' in result and 'application_status' in result


def test_quoted_cross_reference_not_rejected_by_heading_only_guard():
    from app.room_service.chatbot.legal_retrieval import evidence_issues
    source = dict(rank=1, heading='Điều 10. Xử lý dữ liệu', content='Không áp dụng yêu cầu với trường hợp quy định tại Điều 19.')
    text = 'Không áp dụng yêu cầu với trường hợp quy định tại Điều 19 [1].'
    assert not evidence_issues(text, [source], '')
    assert evidence_issues(text.replace('Điều 19', 'Điều 99'), [source], '')


def test_negated_source_classification_keeps_affirmative_obligation_guard():
    from app.room_service.chatbot.legal_retrieval import evidence_issues
    source = dict(rank=1, content='Cơ quan Công an khuyến nghị lưu tin nhắn và phiếu giao dịch.')
    text = 'Nguồn là khuyến cáo, không phải danh mục hồ sơ bắt buộc [1].'
    record = dict(claim_id='limitations:0', kind='source_limit', source_ranks=[1], text=text[:-5], rendered=text)
    assert not evidence_issues(text, [source], '', claim_records=(record,))
    bad = 'Nguồn là khuyến cáo, không phải danh mục hồ sơ bắt buộc, nhưng chủ trọ phải hoàn trả tiền cọc [1].'
    assert evidence_issues(bad, [source], '', claim_records=(dict(record, rendered=bad),))
