from app.room_service.chatbot.evidence_units import practical_facets
from app.room_service.chatbot.legal_retrieval import rerank_legal, diversified_legal_rows, evidence_issues
from app.room_service.chatbot.source_selection import missing_selection_facets
from app.room_service.chatbot.topics import question_categories
import pytest


def row(i, heading, content, category='privacy_data'):
    return dict(id=i, rank=i, chunk_id=i, document_id=i, heading=heading,
                category=category, content=content, text=content, similarity_score=.6)


def test_privacy_storage_and_disclosure_are_not_replaced_by_consent():
    q = 'Ảnh căn cước của người thuê được lưu và sử dụng như thế nào?'
    rows = [row(1, 'Sự đồng ý', 'Chủ thể đồng ý thu thập dữ liệu.'),
            row(2, 'Nguyên tắc bảo vệ dữ liệu cá nhân', 'Xử lý đúng phạm vi, mục đích; lưu trữ trong khoảng thời gian phù hợp.'),
            row(3, 'Cung cấp dữ liệu cá nhân', 'Cung cấp cho bên khác khi được đồng ý, trừ trường hợp pháp luật quy định khác.')]
    missing = missing_selection_facets(q, rows, '{"selected_ids":[1],"insufficient":false}')
    assert any('lưu trữ' in s for s in missing)
    assert any('bên khác' in s for s in missing)
    selected = diversified_legal_rows(q, rows, 2)
    assert {r['id'] for r in selected} == {2, 3}


def test_water_price_is_not_allocation_evidence():
    q = 'Chung đồng hồ nước thì phân chia chi phí nên thỏa thuận ra sao?'
    price = row(1, 'Biểu giá nước', 'Giá nước sạch sinh hoạt.', 'water_cantho')
    assert practical_facets(q, price) == {'biểu giá nước và phạm vi của nguồn giá'}
    agreement = row(2, 'Nội dung của hợp đồng', 'Các bên thỏa thuận giá và phương thức thanh toán.', 'housing_contract')
    assert len(diversified_legal_rows(q, [price, agreement], 2)) == 2
    assert any('thỏa thuận' in s for s in missing_selection_facets(q, [price, agreement], '{"selected_ids":[1],"insufficient":true}'))


def test_electricity_transparency_keeps_consumer_rights_as_conditional_support():
    q = 'Chủ trọ có phải thông báo cách tính tiền điện không?'
    assert 'housing_contract' in question_categories(q)
    rights = row(1, 'Điều 4. Quyền của người tiêu dùng', 'Được cung cấp hóa đơn, chứng từ và thông tin giao dịch.', 'housing_contract')
    assert rerank_legal(q, [rights])


def test_fire_prevention_and_emergency_are_distinct():
    q = 'Lối thoát nạn bị khóa hoặc bị chặn thì làm gì?'
    rows = [row(1, 'Phòng cháy', 'Chủ nhà trọ đảm bảo lối thoát luôn thông thoáng.', 'fire_safety'),
            row(2, 'Báo cháy', 'Gọi lực lượng PCCC theo số 114.', 'fire_safety'),
            row(3, 'Thoát nạn', 'Khi kẹt trong phòng, đóng kín cửa và ra hiệu cầu cứu.', 'fire_safety')]
    missing = missing_selection_facets(q, rows, '{"selected_ids":[3],"insufficient":false}')
    assert any('chưa có cháy' in s for s in missing)
    assert any('114' in s for s in missing)


def test_household_cooperation_does_not_assert_every_landlord_is_household_head():
    q = 'Ai có trách nhiệm cung cấp giấy tờ đăng ký tạm trú?'
    r = row(1, 'Điều 10', 'Chủ hộ có quyền và nghĩa vụ tạo điều kiện cho thành viên hộ gia đình.', 'residence')
    assert any('không đồng nhất' in facet for facet in practical_facets(q, r))


def test_source_gap_is_not_an_affirmative_remedy():
    source = row(1, 'Khuyến cáo thoát nạn', 'Lối thoát nạn phải thông thoáng.', 'fire_safety')
    answer = 'Các tài liệu này không cung cấp quy trình cưỡng chế hay xử phạt hành chính cụ thể [1].'
    assert not evidence_issues(answer, [source], 'Lối thoát nạn bị chặn thì làm gì?')
    mixed = answer.rstrip('.') + ', nhưng chủ trọ phải bồi thường toàn bộ thiệt hại [1].'
    assert any('bồi thường' in e for e in evidence_issues(mixed, [source], 'Lối thoát nạn bị chặn thì làm gì?'))


def test_negated_source_classification_is_not_a_legal_duty():
    source = row(1, 'Hướng dẫn', 'Công khai cách tính theo hóa đơn.', 'electricity')
    answer = 'Nội dung lấy từ hướng dẫn địa phương, không phải điều luật quy định một biểu mẫu bắt buộc [1].'
    assert not evidence_issues(answer, [source], 'Thông tin gì?')


@pytest.mark.parametrize('classification', [
    'không phải quy định pháp luật bắt buộc về một mẫu bảng kê thông báo cụ thể',
    'không phải điều khoản luật quy định một mẫu bảng kê chi tiết bắt buộc',
    'không phải là quy định pháp luật bắt buộc',
])
def test_negated_classification_variants_keep_other_positive_claims_checked(classification):
    source = row(1, 'Hướng dẫn', 'Chủ nhà trọ công khai cách tính tiền điện theo hóa đơn.', 'electricity')
    answer = f'Tài liệu từ Điện lực nêu cách tính theo hóa đơn, {classification} [1].'
    assert not evidence_issues(answer, [source], 'Cách tính tiền điện?')
    mixed = answer.rstrip('.') + ', nhưng chủ trọ có quyền thu thêm một triệu đồng [1].'
    assert evidence_issues(mixed, [source], 'Cách tính tiền điện?')


def test_imperative_data_protection_is_not_just_descriptive_content():
    source = row(1, 'Điều 3. Nguyên tắc bảo vệ dữ liệu cá nhân', '4. Thực hiện đồng bộ các biện pháp, giải pháp kỹ thuật và con người phù hợp để bảo vệ dữ liệu cá nhân.')
    assert not evidence_issues('Bên lưu trữ phải thực hiện các biện pháp kỹ thuật và con người phù hợp để bảo vệ dữ liệu [1].', [source], 'Ảnh căn cước được lưu và sử dụng ra sao?')
    descriptive = row(1, 'Nội dung', 'Các biện pháp kỹ thuật và con người là nội dung công việc.')
    assert evidence_issues('Bên lưu trữ phải thực hiện các biện pháp kỹ thuật và con người [1].', [descriptive], 'Dữ liệu xử lý ra sao?')


def test_price_schedule_disclosure_is_not_a_mandatory_allocation_rule():
    source = row(1, 'Giá nước sạch', 'Giá nước áp dụng cho khách hàng sinh hoạt.', 'water_cantho')
    answer = 'Biểu giá nước sinh hoạt địa phương không quy định bắt buộc cách chia tiền nước giữa những người thuê trọ dùng chung đồng hồ [1].'
    assert not evidence_issues(answer, [source], 'Dùng chung đồng hồ nước thì chia thế nào?')
    assert evidence_issues(answer.rstrip('.') + ', nhưng chủ trọ có quyền thu thêm một triệu đồng [1].', [source], 'Dùng chung đồng hồ nước thì chia thế nào?')


def test_source_disclosure_does_not_hide_exclusive_positive_clause():
    source = row(1, 'Giá nước sạch', 'Giá nước áp dụng cho khách hàng sinh hoạt.', 'water_cantho')
    answer = 'Biểu giá chỉ áp dụng cho một nhà cung cấp, nguồn chưa cung cấp công thức chia chi phí [1].'
    assert any('chưa loại trừ' in e for e in evidence_issues(answer, [source], 'Chia tiền nước thế nào?'))


def test_agreement_fact_question_is_not_an_uncited_refund_entitlement():
    source = row(1, 'Thỏa thuận', 'Các bên thỏa thuận về khoản đặt cọc.', 'housing_contract')
    question = 'Các bên đã thống nhất cụ thể số tiền đặt cọc và điều kiện hoàn trả tiền cọc chưa?'
    assert not evidence_issues(question, [source], 'Tiền cọc?')
    presupposition = 'Vì chủ trọ phải hoàn trả toàn bộ tiền cọc, các bên đã thống nhất ngày hoàn trả chưa?'
    assert evidence_issues(presupposition, [source], 'Tiền cọc?')


def test_validity_conditions_support_necessity_without_literal_must():
    source = row(1, 'Điều kiện có hiệu lực của giao dịch dân sự',
        'Giao dịch dân sự có hiệu lực khi có đủ các điều kiện sau đây: chủ thể hoàn toàn tự nguyện, mục đích không vi phạm điều cấm của luật.', 'housing_contract')
    answer = 'Thỏa thuận phải đáp ứng điều kiện có hiệu lực: hoàn toàn tự nguyện và mục đích không vi phạm điều cấm [1].'
    assert not evidence_issues(answer, [source], 'Thỏa thuận thế nào?')
    descriptive = row(1, 'Thỏa thuận', 'Tự nguyện và mục đích là nội dung được nghiên cứu.', 'housing_contract')
    assert evidence_issues(answer, [descriptive], 'Thỏa thuận thế nào?')


def test_condition_of_consent_is_not_just_descriptive_data_content():
    source = row(1, 'Cung cấp dữ liệu cá nhân',
        'Cung cấp cho cơ quan, tổ chức, cá nhân khác khi được chủ thể dữ liệu cá nhân đồng ý, trừ trường hợp pháp luật có quy định khác.')
    answer = 'Việc cung cấp dữ liệu cho bên khác phải có sự đồng ý, trừ trường hợp pháp luật có quy định khác [1].'
    assert not evidence_issues(answer, [source], 'Dữ liệu được cung cấp thế nào?')
    descriptive = row(1, 'Nội dung', 'Sự đồng ý là một chủ đề trong dữ liệu nghiên cứu.')
    assert evidence_issues(answer, [descriptive], 'Dữ liệu được cung cấp thế nào?')


def test_actor_check_binds_must_to_tenant_not_neighbouring_clause():
    source = row(1, 'Phòng cháy đối với nhà ở',
        'Nhà ở phải bố trí lối thoát nạn; cơ quan Công an tổ chức kiểm tra phòng cháy.', 'fire_safety')
    answer = 'Nhà ở phải bố trí lối thoát nạn nhưng nguồn chưa quy định thủ tục khiếu nại cụ thể giữa người thuê và bên cho thuê [1].'
    assert not evidence_issues(answer, [source], 'Lối thoát bị chặn?')
    transferred = 'Người thuê phải tổ chức kiểm tra phòng cháy [1].'
    assert any('trách nhiệm của cơ quan' in e for e in evidence_issues(transferred, [source], 'Lối thoát bị chặn?'))
