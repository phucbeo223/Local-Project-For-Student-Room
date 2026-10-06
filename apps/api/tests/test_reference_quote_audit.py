import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'eval'))
from compare_grounded_references import Point, Review, SelectedPoint, SelectedReview, fragments, materialize, validate_quotes, selection_schema, reusable_cases
from pydantic import ValidationError
from quantity_audit import quantity_errors
import pytest


def review(status, rq, aq='', agreement='partial'):
    return Review(agreement=agreement, points=[Point(status=status, reference_quote=rq,
        answer_quote=aq, explanation='Đối chiếu nội dung câu trả lời.')], explanation='Một ý cần kiểm tra lại với mẫu.')


def test_judge_cannot_invent_missing_reference_deadline():
    value = review('missing', 'Phải giải quyết trong 24 giờ')
    assert validate_quotes(value, 'Có thể báo tin trên nền tảng.', 'Báo tin bằng nút báo cáo.')


def test_judge_cannot_call_a_literal_present_point_missing():
    value = review('missing', 'địa chỉ và số điện thoại')
    assert validate_quotes(value, 'Kiểm tra địa chỉ và số điện thoại.', 'Đối chiếu địa chỉ và số điện thoại.')


def test_valid_paraphrase_has_two_real_distinct_quotes():
    value = review('matched', 'Kiểm tra địa chỉ', 'Đối chiếu địa chỉ')
    assert not validate_quotes(value, 'Kiểm tra địa chỉ và số điện thoại.', 'Đối chiếu địa chỉ trước khi trả tiền.')


def test_invented_answer_quote_is_rejected():
    value = review('different', 'trong 24 giờ', 'trong 03 ngày')
    assert validate_quotes(value, 'Xử lý trong 24 giờ.', 'Chưa có thời hạn được xác nhận.')


def test_different_deadlines_cannot_be_counted_as_matched():
    value = review('matched', 'trong 24 giờ', 'trong 03 ngày')
    assert validate_quotes(value, 'Xử lý trong 24 giờ.', 'Xử lý trong 03 ngày.')


def test_list_ordinals_are_not_numeric_claims():
    value = review('matched', '3. Kiểm tra tiền cọc', 'Kiểm tra tiền cọc')
    assert not validate_quotes(value, '3. Kiểm tra tiền cọc trước khi thuê.', 'Kiểm tra tiền cọc trước khi ký.')


def test_different_percentages_and_range_endpoints_are_rejected():
    assert validate_quotes(review('matched', 'thu 75% định mức', 'thu 80% định mức'), 'thu 75% định mức', 'thu 80% định mức')
    assert validate_quotes(review('matched', 'phạt 20–30 triệu', 'phạt 20–40 triệu'), 'phạt 20–30 triệu', 'phạt 20–40 triệu')


def test_equal_number_with_different_time_unit_is_not_matched():
    assert validate_quotes(review('matched', 'trong 24 giờ', 'trong 24 ngày'), 'trong 24 giờ', 'trong 24 ngày')


def test_same_amount_can_use_different_currency_scale():
    assert not validate_quotes(review('matched', 'thu 30 nghìn đồng', 'thu 30.000 đồng'), 'thu 30 nghìn đồng', 'thu 30.000 đồng')


def test_equal_time_quantity_ignores_leading_zeros():
    assert not validate_quotes(review('matched', 'trong 03 ngày', 'trong 3 ngày'), 'trong 03 ngày', 'trong 3 ngày')


def test_currency_ranges_keep_both_endpoints_and_scale():
    assert not validate_quotes(review('matched', 'phạt 20–30 triệu', 'phạt 20.000.000–30.000.000 đồng'), 'phạt 20–30 triệu', 'phạt 20.000.000–30.000.000 đồng')


def test_vietnamese_decimal_amount_keeps_thousand_separator():
    assert not validate_quotes(review('matched', 'thu 1.000,5 đồng', 'thu 1000,5 đồng'), 'thu 1.000,5 đồng', 'thu 1000,5 đồng')


def selection(status='matched', reference_id=1, answer_ids=None):
    return SelectedReview(agreement='partial', points=[SelectedPoint(status=status, reference_id=reference_id,
        answer_ids=[1] if answer_ids is None else answer_ids, explanation='Đối chiếu nội dung chính.')], explanation='Còn chi tiết cần kiểm tra.')


def test_fragments_remain_literal_across_long_unicode_paragraphs():
    text = '3. **Tiền đặt cọc:** ' + ('Điều kiện thỏa thuận, đúng chủ thể và thời hạn. ' * 12)
    units = fragments(text)
    assert units and all(u['text'] in text for u in units)
    assert [u['id'] for u in units] == list(range(1,len(units)+1))


def test_selected_ids_restore_exact_quotes_without_model_copying():
    refs, answers = fragments('Kiểm tra địa chỉ trước khi thuê.'), fragments('Đối chiếu địa chỉ trước khi ký.')
    value = materialize(selection(), refs, answers)
    assert value.points[0].reference_quote == refs[0]['text']
    assert value.points[0].answer_quote == answers[0]['text']
    assert not validate_quotes(value, refs[0]['text'], answers[0]['text'])


def test_unknown_fragment_id_is_rejected():
    with pytest.raises(ValueError, match='reference_id'):
        materialize(selection(reference_id=999), fragments('Kiểm tra địa chỉ.'), fragments('Đối chiếu địa chỉ.'))


def test_missing_fragment_cannot_have_answer_id():
    with pytest.raises(ValueError, match='answer_ids'):
        materialize(selection(status='missing'), fragments('Kiểm tra địa chỉ.'), fragments('Đối chiếu địa chỉ.'))


def test_fragment_selection_still_rejects_matching_wrong_units():
    refs, answers = fragments('Xử lý trong 24 giờ.'), fragments('Xử lý trong 24 ngày.')
    assert validate_quotes(materialize(selection(), refs, answers), refs[0]['text'], answers[0]['text'])


def test_decode_schema_rejects_unknown_ids_and_matched_null_answer():
    model = selection_schema(fragments('Kiểm tra địa chỉ.'), fragments('Đối chiếu địa chỉ.'))
    for field,value in [('reference_id',999),('answer_ids',[999]),('answer_ids',[])]:
        data = selection().model_dump(); data['points'][0][field] = value
        with pytest.raises(ValidationError): model.model_validate(data)


def test_decode_schema_accepts_missing_null_without_inventing_answer_quote():
    refs, answers = fragments('Kiểm tra địa chỉ.'), fragments('Kiểm tra tiền cọc.')
    model = selection_schema(refs,answers)
    selected = model.model_validate(selection(status='missing',answer_ids=[]).model_dump())
    assert materialize(selected,refs,answers).points[0].answer_quote == ''


def test_quota_fraction_and_percentage_are_equivalent_quantities():
    assert not validate_quotes(review('matched','75% định mức','3/4 định mức'), '75% định mức', '3/4 định mức')


def test_different_quota_fraction_cannot_match_percentage():
    assert validate_quotes(review('matched','75% định mức','1/2 định mức'), '75% định mức', '1/2 định mức')


def test_calendar_fraction_is_not_a_quota_ratio():
    assert validate_quotes(review('matched','75% định mức','Ngày 3/4 công bố định mức'), '75% định mức', 'Ngày 3/4 công bố định mức')


def test_reuse_reaudits_real_quotations_and_rejects_changed_answer():
    reference, answer_text = 'Kiểm tra địa chỉ.', 'Đối chiếu địa chỉ.'
    selected = selection(); value=materialize(selected,fragments(reference),fragments(answer_text))
    candidate = dict(id=19, answer=answer_text,user_reference=reference,comparison=value.model_dump(),selected_fragments=selected.model_dump())
    legacy = dict(policy='prior',scorer_sha256='prior-hash',cases=[candidate])
    assert len(reusable_cases(legacy,[dict(id=19,answer=answer_text)],{19:dict(external_answer=reference)}))==1
    assert not reusable_cases(legacy,[dict(id=19,answer='Câu trả lời đã đổi.')],{19:dict(external_answer=reference)})


def test_long_clause_and_its_semicolon_condition_are_never_cut():
    text = 'Người thuê ' + 'đối chiếu thông tin ' * 20 + '; áp dụng khi sinh sống từ 30 ngày trở lên.'
    assert fragments(text) == [dict(id=1, text=text)]


def test_multiple_ids_restore_disjoint_verbatim_fragments():
    reference = 'Thu 30 nghìn đồng.'
    answer = 'Mức thu được thỏa thuận. Một thông tin khác. Thu 30.000 đồng.'
    ru, au = fragments(reference), fragments(answer)
    selected = selection(answer_ids=[1,3])
    value = materialize(selected, ru, au)
    assert value.points[0].answer_quotes == [au[0]['text'],au[2]['text']]
    assert not validate_quotes(value,reference,answer)


def test_decode_schema_uses_actual_nonconsecutive_ids():
    model = selection_schema([dict(id=7,text='Mức thu tiền nước.')], [dict(id=12,text='Mức thu thỏa thuận.')])
    assert model.model_validate(selection(reference_id=7,answer_ids=[12]).model_dump())
    with pytest.raises(ValidationError):
        model.model_validate(selection(reference_id=1,answer_ids=[1]).model_dump())


def test_duplicate_answer_ids_are_rejected():
    with pytest.raises(ValueError):
        materialize(selection(answer_ids=[1,1]), fragments('Thu 30 nghìn đồng.'), fragments('Thu 30.000 đồng.'))


@pytest.mark.parametrize('reference,answer', [
    ('Sinh sống từ 30 ngày trở lên.', 'Nộp hồ sơ trong 30 ngày.'),
    ('Nộp hồ sơ trong 30 ngày.', 'Sinh sống từ 30 ngày trở lên.'),
    ('Cá nhân bị phạt 30.000 đồng.', 'Tổ chức bị phạt 30 nghìn đồng.'),
    ('Thu 30.000 đồng/người.', 'Thu 30 nghìn đồng/m3.'),
    ('Xử lý trong 30 ngày.', 'Xử lý trong 30 tháng.'),
])
def test_same_number_with_wrong_event_actor_rate_or_time_is_rejected(reference,answer):
    errors=validate_quotes(review('matched',reference,answer),reference,answer)
    assert errors and isinstance(errors[0],dict) and errors[0]['expected']


def test_numeric_repair_includes_selected_and_next_real_candidate():
    from compare_grounded_references import repair_feedback
    ru, au = fragments('Thu 30 nghìn đồng.'), fragments('Theo mức thỏa thuận. Thu 30.000 đồng.')
    selected=selection()
    errors=validate_quotes(materialize(selected,ru,au),ru[0]['text'],'Theo mức thỏa thuận. Thu 30.000 đồng.')
    feedback=repair_feedback(errors,selected,ru,au)
    assert feedback['errors'][0]['code']=='quantity_or_unit_missing'
    assert [u['id'] for u in feedback['candidate_answer_fragments']]==[1,2]


def test_written_range_is_equivalent_and_document_id_is_not_ratio():
    reference='TT 60/2025 áp dụng bậc 2 từ 101–200 kWh khi không kê khai định mức.'
    answer='Áp dụng bậc 2 từ 101 đến 200 kWh khi không kê khai định mức.'
    assert not validate_quotes(review('matched',reference,answer),reference,answer)


def test_decode_cannot_match_quantities_absent_from_entire_answer():
    model=selection_schema(fragments('Thu 30 nghìn đồng.'),fragments('Chưa biết mức thu thực tế.'))
    with pytest.raises(ValidationError):model.model_validate(selection().model_dump())
    assert model.model_validate(selection(status='different').model_dump())


def test_union_branches_emit_status_before_explanation_with_same_field_order():
    model=selection_schema(fragments('Thu 30 nghìn đồng.'),fragments('Thu 30.000 đồng.'))
    branches=[v for v in model.model_json_schema()['$defs'].values() if 'status' in v.get('properties',{})]
    assert len(branches)==3
    assert all(list(v['properties'])==['status','reference_id','answer_ids','explanation'] for v in branches)


def test_wrapped_statutory_residence_condition_is_not_submission_deadline():
    reference='Sinh sống từ 30 ngày trở lên.'
    answer='Đến sinh sống tại chỗ ở hợp pháp ngoài phạm vi đơn vị hành chính cấp xã nơi đã đăng ký thường trú\nđể lao động, học tập hoặc vì mục đích khác từ 30 ngày trở lên thì phải đăng ký tạm trú.'
    assert not validate_quotes(review('matched',reference,answer),reference,answer)
    deadline='Thời hạn đăng ký: trong vòng 30 ngày.'
    assert validate_quotes(review('matched',deadline,answer),deadline,answer)


def test_high_label_cannot_override_all_different_points():
    from compare_grounded_references import audited_agreement
    assert audited_agreement(review('different','Thu 30 nghìn đồng.','Thu 50 nghìn đồng.',agreement='high'))=='low'


def test_reference_slots_cannot_skip_a_disagreeing_deadline():
    from compare_grounded_references import reference_fragments,judge_schema,normalize_selection
    ru=reference_fragments('Điều kiện:\nSinh sống từ 30 ngày trở lên.\nNộp hồ sơ trong 30 ngày.')
    au=fragments('Sinh sống từ 30 ngày trở lên thì đăng ký tạm trú.')
    model=judge_schema(ru,au)
    data=dict(agreement='partial',explanation='Còn thời hạn khác chưa có căn cứ.',points={
        'r2':dict(status='matched',reference_id=2,answer_ids=[1],explanation='Cùng điều kiện cư trú.'),
        'r3':dict(status='missing',reference_id=3,answer_ids=[],explanation='Chưa nêu thời hạn nộp hồ sơ.')})
    assert len(normalize_selection(model.model_validate(data),ru,au).points)==2
    del data['points']['r3']
    with pytest.raises(ValidationError): model.model_validate(data)


def test_matched_decoding_only_offers_quantity_checked_real_combinations():
    from compare_grounded_references import matched_candidates,judge_schema
    ru=fragments('Thu 30 nghìn đồng.')
    au=fragments('Đối chiếu hợp đồng. Một thông tin khác. Thu 30.000 đồng.')
    candidates=matched_candidates(ru[0]['text'],au)
    assert [3] in candidates and [1] not in candidates
    assert all(3 in ids and not quantity_errors(ru[0]['text'],'\n'.join(au[i-1]['text'] for i in ids)) for ids in candidates)
    schema=judge_schema(ru,au).model_json_schema()
    assert schema['$defs']['Matched1']['properties']['answer_ids']['enum']==candidates


def test_matched_candidates_reject_same_value_with_wrong_event():
    from compare_grounded_references import matched_candidates
    assert matched_candidates('Sinh sống từ 30 ngày trở lên.',fragments('Nộp hồ sơ trong 30 ngày.'))==[]


def test_fire_counts_require_right_object_and_value_even_when_unit_is_not_time():
    assert quantity_errors('Ít nhất 2 bình chữa cháy mỗi tầng.','Ít nhất 2 tầng.')
    assert quantity_errors('Có 2 lối thoát hiểm.','Có 1 lối thoát nạn.')
    assert not quantity_errors('Ít nhất 2 bình chữa cháy mỗi tầng.','Tối thiểu hai bình chữa cháy mỗi tầng.')


def test_household_quota_accepts_written_one_household_without_losing_person_count():
    assert not quantity_errors('Cứ 04 người được cấp 01 định mức hộ gia đình.','Cứ 4 người được tính thành một hộ gia đình.')


def test_document_packet_is_not_household_and_count_range_keeps_both_endpoints():
    assert quantity_errors('Nộp 01 hồ sơ.','Có một hộ gia đình.')
    assert quantity_errors('Nhà có 2–3 tầng.','Nhà có 3 tầng.')


def test_word_soft_wrap_keeps_residence_actor_and_condition_in_one_literal_unit():
    from compare_grounded_references import matched_candidates
    text=('Công dân đến sinh sống tại chỗ ở hợp pháp ngoài phạm vi đơn vị hành\n'
          'chính cấp xã nơi đã đăng ký thường trú để lao động, học tập hoặc vì mục\n'
          'đích khác từ 30 ngày trở lên thì phải thực hiện đăng ký tạm trú.” [1].')
    units=fragments(text)
    assert units==[dict(id=1,text=text)]
    assert matched_candidates('Sinh sống từ 30 ngày trở lên.',units)==[[1]]
    assert matched_candidates('Nộp hồ sơ trong 30 ngày.',units)==[]


def test_soft_wrapped_condition_does_not_merge_separate_bullets_or_paragraphs():
    first='- Thu 30.000 đồng;\r\n  áp dụng cho người thuê khi\r\n  có thỏa thuận.'
    second='- Khoản khác được hỏi sau.'
    third='Nguồn chưa xác nhận mức bắt buộc.'
    text=first+'\r\n'+second+'\r\n\r\n'+third
    units=fragments(text)
    assert units==[dict(id=1,text=first),dict(id=2,text=second),dict(id=3,text=third)]
    assert all(u['text'] in text for u in units)


def test_reference_word_wrap_is_one_complete_required_slot():
    from compare_grounded_references import reference_fragments
    first='Công dân đến sinh sống tại chỗ ở hợp pháp\nngoài xã nơi thường trú từ 30 ngày trở lên.'
    second='- Thời hạn tạm trú tối đa 2 năm.'
    assert reference_fragments('Điều kiện:\n'+first+'\n'+second)==[
        dict(id=2,text=first),dict(id=3,text=second)]


@pytest.mark.parametrize('separator',[' ','\n'])
def test_city_abbreviation_does_not_cut_applicable_location(separator):
    text='Áp dụng cho người thuê tại TP.'+separator+'Cần Thơ khi có thỏa thuận.'
    assert fragments(text)==[dict(id=1,text=text)]
