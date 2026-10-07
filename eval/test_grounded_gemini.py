import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'apps/api'))
import pytest
from compare_grounded_references import reference_fragments, fragments, materialize, SelectedReview
from compare_grounded_gemini import semantic_audit, compare_case


def test_colon_keeps_proposition_conditions_and_original_offsets():
    text = '**Các bước:**\r\nNếu kê khai đủ số người:\r\n  - Ba người được 3/4 định mức:\r\n    - Áp dụng theo kỳ thanh toán.\r\nNếu không kê khai đủ số người:\r\n  - Áp dụng điều kiện khác.'
    units = reference_fragments(text)
    assert [u['id'] for u in units] == [2, 3, 4, 5, 6]
    assert units[2]['parent_ids'] == [2, 3]
    assert units[2]['context_quotes'] == ['Nếu kê khai đủ số người:', '- Ba người được 3/4 định mức:']
    assert units[-1]['parent_ids'] == [5]
    assert all(text[u['start']:u['end']] == u['text'] for u in units)


def test_unformatted_substantive_colon_is_preserved_without_question_specific_rules():
    units = reference_fragments('Có hợp đồng ít nhất 18 tháng:\n- Cần đối chiếu kỳ thu.')
    assert len(units) == 2 and units[1]['parent_ids'] == [1]
    assert reference_fragments('**Thông tin chung:**') == []


class AuditClient:
    def __init__(self):
        self.prompts = []
    def request_json(self, prompt, schema, **kwargs):
        self.prompts.append(prompt)
        return json.dumps(dict(agreement_consistent=True, agreement_reason='Nhãn tổng thể phù hợp.', checks=[dict(reference_id=1, consistent=False,
            reason='Giải thích nói về chủ đề khác hoặc sai điều kiện.')]), ensure_ascii=False), {}


@pytest.mark.parametrize('reference,answer,explanation', [
    ('Kiểm tra điều kiện hoàn tiền cọc.', 'Kiểm tra tiền cọc và giá điện nước.', 'Thiếu đơn giá điện nước.'),
    ('Trang bị phương tiện chữa cháy.', 'Cần bình chữa cháy phù hợp.', 'Thiếu tập huấn cho quản lý.'),
    ('Cảnh giác phòng giá rẻ bất thường.', 'So sánh giá và thận trọng với phòng quá rẻ.', 'Thiếu Google Hình ảnh.'),
    ('Nếu kê khai đầy đủ: Ba người được 3/4 định mức.', 'Nếu không kê khai: Ba người được 3/4 định mức.', 'Khớp số 3/4.')])
def test_semantic_audit_receives_full_answer_condition_and_explanation(reference, answer, explanation):
    client = AuditClient()
    selected = SelectedReview(agreement='partial', points=[dict(status='different', reference_id=1,
        answer_ids=[1], explanation=explanation)], explanation='Cần kiểm tra các ý được đối chiếu.')
    errors, raw = semantic_audit(client, 'Cần kiểm tra gì?', reference_fragments(reference), fragments(answer), selected)
    assert errors and 'raw_output' in raw
    assert reference in client.prompts[0] and answer in client.prompts[0] and explanation in client.prompts[0]
    assert 'TOÀN BỘ ANSWER' in client.prompts[0]


def test_incomplete_reference_selection_is_rejected():
    selected = SelectedReview(agreement='high', points=[dict(status='matched', reference_id=1,
        answer_ids=[1], explanation='Cùng nội dung.')], explanation='Các nội dung tương ứng.')
    with pytest.raises(ValueError, match='Incomplete reference'):
        materialize(selected, reference_fragments('Một mệnh đề quan trọng.\nMệnh đề quan trọng khác.'), fragments('Một mệnh đề quan trọng.'))


def test_inconsistent_judgements_exhaust_bound_without_high_or_ollama():
    class Client(AuditClient):
        def request_json(self, prompt, schema, **kwargs):
            self.prompts.append(prompt)
            if 'checks' in schema['properties']:
                return json.dumps(dict(agreement_consistent=True, agreement_reason='Nhãn tổng thể phù hợp.', checks=[dict(reference_id=1, consistent=False, reason='Giải thích nói về điện nước thay vì tiền cọc.')])), {}
            return json.dumps(dict(agreement='high', explanation='Nội dung trong hai phần tương ứng.',
                points=dict(r1=dict(status='matched', reference_id=1, answer_ids=[1], explanation='Khớp tiền điện nước.')))), {}
    client = Client()
    result = compare_case(dict(id=1, question='Tiền cọc?', answer='Kiểm tra điều kiện tiền cọc.'),
        dict(question='Tiền cọc?', external_answer='Kiểm tra điều kiện tiền cọc.'), {}, client)
    assert result['comparison'] is None and result['attempt_count'] == 3
    assert len(client.prompts) == 6
    assert all('raw_output' in a and a['errors'] for a in result['audit_attempts'])


def test_all_different_can_remain_partial_when_main_idea_is_answered_and_audited():
    class Client:
        def request_json(self, prompt, schema, **kwargs):
            if 'checks' in schema['properties']:
                return json.dumps(dict(agreement_consistent=True, agreement_reason='Đã trả lời ý chính nhưng thiếu chi tiết.',
                    checks=[dict(reference_id=1, consistent=True, reason='Cùng ý chính nhưng thiếu kỳ thu.')]), ensure_ascii=False), {}
            return json.dumps(dict(agreement='partial', explanation='Đã trả lời việc đối chiếu tiền nước nhưng thiếu kỳ thu.',
                points=dict(r1=dict(status='different', reference_id=1, answer_ids=[1], explanation='Thiếu kỳ thu tiền nước.'))), ensure_ascii=False), {}
    result = compare_case(dict(id=1, question='Tiền nước?', answer='Đối chiếu tiền nước với hợp đồng.'),
        dict(question='Tiền nước?', external_answer='Đối chiếu tiền nước và kỳ thu với hợp đồng.'), {}, Client())
    assert result['comparison']['agreement'] == 'partial'
    assert result['semantic_audit_passed'] and result['attempt_count'] == 1


def test_overall_label_disagreement_is_not_accepted():
    class Client:
        def request_json(self, *args, **kwargs):
            return json.dumps(dict(agreement_consistent=False, agreement_reason='Có ý chính nhưng nhãn LOW không phù hợp.',
                checks=[dict(reference_id=1, consistent=True, reason='Đã có ý tương ứng.')]), ensure_ascii=False), {}
    selected = SelectedReview(agreement='low', points=[dict(status='different', reference_id=1,
        answer_ids=[1], explanation='Thiếu kỳ thu.')], explanation='Có ý chính nhưng thiếu kỳ thu.')
    errors, _ = semantic_audit(Client(), 'Tiền nước?', reference_fragments('Đối chiếu tiền nước và kỳ thu.'),
                              fragments('Đối chiếu tiền nước.'), selected)
    assert any(e.get('kind') == 'overall_agreement' for e in errors)
