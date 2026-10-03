import json
import pytest
from app.room_service.chatbot.agents import QuestionAnalysisAgent, QuestionPlan
from app.room_service.legal_knowledge.provisions import structure_provisions
from app.room_service.legal_knowledge.storage import legal_sql


def test_analysis_preserves_mixed_subjects_and_rejects_invented_articles():
    class Client:
        model = 'gemini-test'
        def request_json(self, *args, **kwargs):
            return json.dumps({'search_queries':['Điều 999 hoàn cọc'], 'categories':['housing_contract']}), {}
    result = QuestionAnalysisAgent(Client()).analyze('Hợp đồng và hồ sơ tạm trú cần thông tin cá nhân gì?')
    assert result.step['status'] == 'fallback'
    assert {'housing_contract','residence','privacy_data'} <= set(result.plan.categories)
    assert not result.plan.search_queries


def test_analysis_never_supplies_an_answer_and_keeps_original_topics():
    class Client:
        model = 'gemini-test'
        def request_json(self, *args, **kwargs):
            assert 'Không trả lời pháp lý' in args[0]
            return json.dumps({'search_queries':['Hồ sơ đăng ký tạm trú'], 'categories':['residence']}), {}
    result = QuestionAnalysisAgent(Client()).analyze('Hợp đồng thuê trọ và tạm trú')
    assert result.step['provider'] == 'gemini'
    assert result.plan.categories == ['residence','housing_contract']
    with pytest.raises(ValueError):
        QuestionPlan.model_validate({'answer':'invented conclusion'})


def test_provisions_keep_complete_clauses_and_exception_without_editorial_tail():
    text = ('GHI CHÚ NGỮ CẢNH\nKhông dùng phần này.\n\nĐiều 328. Đặt cọc\n'
            '1. Nội dung định nghĩa.\n2. Hoàn trả nếu hợp đồng được giao kết, thực hiện; trừ trường hợp có thoả thuận khác.\n'
            '\nGhi chú: Đây là bản rút gọn.\nKhông phải điều luật.')
    provisions = structure_provisions(text,'a'*64)
    assert len(provisions) == 2
    assert provisions[1].clause == '2'
    assert 'trừ trường hợp có thoả thuận khác.' in provisions[1].content
    assert 'Ghi chú' not in provisions[1].content
    assert provisions[1].content == text[provisions[1].source_start:provisions[1].source_end].strip()


def test_provisions_keep_checklist_points_and_do_not_invent_articles():
    text = 'Điều 28. Hồ sơ\n1. Hồ sơ bao gồm:\na) Tờ khai;\nb) Chứng minh chỗ ở.\n2. Thủ tục nộp hồ sơ.'
    items = structure_provisions(text,'b'*64)
    assert items[0].points == ['a','b']
    assert 'a) Tờ khai' in items[0].content and 'b) Chứng minh' in items[0].content
    assert structure_provisions('Bản diễn giải không có điều luật.','c'*64) == []


def test_legal_namespace_cannot_inject_sql_or_touch_listings():
    with pytest.raises(ValueError): legal_sql('SELECT * FROM legal_chunks','public; DROP TABLE aggregated_listings')
    sql = str(legal_sql('SELECT * FROM legal_chunks JOIN legal_documents ON true','legal_v2'))
    assert 'legal_v2.legal_chunks' in sql and 'legal_v2.legal_documents' in sql
    assert str(legal_sql('SELECT * FROM aggregated_listings','legal_v2')) == 'SELECT * FROM aggregated_listings'


def test_operative_article_line_is_not_discarded():
    text='Điều 3. Thời gian áp dụng: từ ngày 10 tháng 5 năm 2025.'
    result=structure_provisions(text,'d'*64)
    assert len(result)==1 and result[0].content==text


def test_amended_clause_numbers_remain_inside_the_parent_amendment():
    text=('“Stray stamp quote\nĐiều 4. Sửa đổi\n'
          '1. Sửa Điều 30 như sau:\n“Điều 30. Thông báo\n1. Nội dung thứ nhất.\n2. Nội dung thứ hai.”.\n'
          '2. Bãi bỏ một quy định.\nĐiều 6. Hiệu lực\n1. Ngày áp dụng.')
    result=structure_provisions(text,'e'*64)
    assert [(p.article,p.clause) for p in result]==[('4','1'),('4','2'),('6','1')]
    assert '2. Nội dung thứ hai.' in result[0].content


def test_clause_preserves_statutory_introduction_separately():
    text='Điều 163. Hợp đồng về nhà ở\nHợp đồng phải lập thành văn bản bao gồm:\n1. Tên các bên;\n2. Thời hạn.'
    result=structure_provisions(text,'f'*64)
    assert result[1].clause=='1'
    assert result[1].article_context=='Hợp đồng phải lập thành văn bản bao gồm:'
    assert result[1].content=='1. Tên các bên;'


def test_separate_verifier_never_generates_the_answer_and_records_fallback():
    from app.room_service.chatbot.agents import QwenAnswerAgent
    from app.room_service.chatbot.providers import EvidenceIssues
    class Local:
        providers=[]
        def generate(self,*args,**kwargs): return 'local answer'
        def check_legal_evidence(self,*args,**kwargs): return EvidenceIssues(['local issue'])
    class Verifier:
        model='gemini-test'
        def check_legal_evidence(self,*args,**kwargs): return []
    agent=QwenAnswerAgent(Local(),Verifier())
    assert agent.generate('question',[])=='local answer'
    result=agent.check_legal_evidence('question','answer',[])
    assert not result and result.trace['provider']=='gemini'
    class Unavailable:
        model='gemini-test'
        def check_legal_evidence(self,*args,**kwargs): raise RuntimeError('HTTP 429')
    fallback=QwenAnswerAgent(Local(),Unavailable()).check_legal_evidence('question','answer',[])
    assert fallback==['local issue']
    assert fallback.trace['provider']=='qwen_and_rules' and fallback.trace['http_status']==429
    assert fallback.degraded_reasons
