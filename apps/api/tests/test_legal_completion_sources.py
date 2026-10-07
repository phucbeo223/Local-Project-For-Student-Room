import json
from app.room_service.chatbot.source_selection import render_selection, selection_candidates, coverage_notice
from app.room_service.chatbot.answer_coverage import missing_answer_facets


def test_named_law_dependency_keeps_separate_citation():
    question = 'Nền tảng có trách nhiệm gì về thông tin người bán?'
    rows = [dict(rank=1, document_id=30, title='Nghị định 248', category='ecommerce_platform',
                 source_id='supplement-s16-word', content='Thực hiện khoản 2 Điều 17 của Luật Thương mại điện tử.',
                 context_complete=True, provision_metadata=dict(article='18', clause='2')),
            dict(rank=2, document_id=29, title='Luật 122', category='ecommerce_platform',
                 source_id='supplement-s15-word', content='Công khai phương thức tiếp nhận và xử lý phản ánh, khiếu nại.',
                 context_complete=True, provision_metadata=dict(article='17', clause='2'))]
    result = render_selection(question, rows, selection_candidates(rows),
                              json.dumps(dict(selected_ids=[1], insufficient=False)), 'test', 'test')
    assert {s['rank'] for s in result.selected_evidence} == {1, 2}
    assert result.selected_evidence[1]['document_id'] == 29
    assert result.agent_trace[0]['agent'] == 'evidence_dependency_completion'


def test_coverage_combines_accepted_checklist_lines_for_same_source():
    question = 'Nền tảng có trách nhiệm gì về thông tin người bán?'
    rows = [dict(rank=1, category='ecommerce_platform', content='Cập nhật từ khóa và gỡ bỏ nội dung vi phạm.')]
    claims = [dict(kind='regulation', source_ranks=[1], text='Cập nhật từ khóa.'),
              dict(kind='regulation', source_ranks=[1], text='Gỡ bỏ nội dung vi phạm.')]
    assert not missing_answer_facets(question, rows, claims)
    assert missing_answer_facets(question, rows, [dict(claims[1], source_ranks=[2]), claims[0]])


def test_link_check_warning_does_not_claim_all_sources_are_missing():
    notice = coverage_notice('Cần kiểm tra dấu hiệu gì trước khi chuyển tiền qua liên kết lạ?')
    assert 'kiểm tra liên kết và giao dịch cụ thể' in notice
    assert 'Chưa đủ căn cứ' not in notice


def test_general_statutory_price_can_support_rental_price_checklist():
    q = 'Hợp đồng thuê trọ cần kiểm tra điều khoản nào?'
    rows = [dict(rank=1, category='housing_contract', content='Nội dung hợp đồng: giá, phương thức thanh toán.')]
    claims = [dict(kind='regulation', source_ranks=[1], text='Kiểm tra giá thuê và phương thức thanh toán.')]
    assert not missing_answer_facets(q, rows, claims)
    from app.room_service.chatbot.answer_coverage import source_facets
    assert 'contract_rent' not in source_facets(q, dict(rows[0], content='Các bên tham gia ký kết.'))


def test_copula_question_does_not_become_uncited_legal_obligation():
    from app.room_service.chatbot.legal_retrieval import evidence_issues
    rows = [dict(rank=1, content='Công khai thông tin người bán.')]
    assert not evidence_issues('Nền tảng bạn sử dụng có phải là nền tảng trung gian?', rows, 'Kiểm tra nền tảng?')
    assert evidence_issues('Nền tảng bạn sử dụng có phải là bên phải hoàn trả tiền cọc?', rows, 'Kiểm tra nền tảng?')


def test_listing_requests_use_only_the_separate_local_generator():
    from app.room_service.chatbot.providers import FallbackResponseGenerator, GenerationResult
    class Cloud:
        def generate(self, *args, **kwargs):
            raise AssertionError('Housing reached cloud selector')
    class Local:
        def generate(self, *args, **kwargs):
            return GenerationResult('Phòng trọ phù hợp.', 'qwen-local')
    generator = FallbackResponseGenerator([Cloud()])
    generator.listing_generator = FallbackResponseGenerator([Local()])
    result = generator.generate('Tìm phòng', [dict(id=1)], context_kind='listing')
    assert result.provider == 'qwen-local'
