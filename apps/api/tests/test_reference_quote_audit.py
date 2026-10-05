import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'eval'))
from compare_grounded_references import Point, Review, SelectedPoint, SelectedReview, fragments, materialize, validate_quotes, selection_schema, reusable_cases
from pydantic import ValidationError
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


def selection(status='matched', reference_id=1, answer_id=1):
    return SelectedReview(agreement='partial', points=[SelectedPoint(status=status, reference_id=reference_id,
        answer_id=answer_id, explanation='Đối chiếu nội dung chính.')], explanation='Còn chi tiết cần kiểm tra.')


def test_fragments_remain_literal_across_long_unicode_paragraphs():
    text = '3. **Tiền đặt cọc:** ' + ('Điều kiện thỏa thuận, đúng chủ thể và thời hạn. ' * 12)
    units = fragments(text)
    assert units and all(8 <= len(u['text']) <= 240 and u['text'] in text for u in units)
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
    with pytest.raises(ValueError, match='answer_id=null'):
        materialize(selection(status='missing'), fragments('Kiểm tra địa chỉ.'), fragments('Đối chiếu địa chỉ.'))


def test_fragment_selection_still_rejects_matching_wrong_units():
    refs, answers = fragments('Xử lý trong 24 giờ.'), fragments('Xử lý trong 24 ngày.')
    assert validate_quotes(materialize(selection(), refs, answers), refs[0]['text'], answers[0]['text'])


def test_decode_schema_rejects_unknown_ids_and_matched_null_answer():
    model = selection_schema(fragments('Kiểm tra địa chỉ.'), fragments('Đối chiếu địa chỉ.'))
    for field,value in [('reference_id',999),('answer_id',999),('answer_id',None)]:
        data = selection().model_dump(); data['points'][0][field] = value
        with pytest.raises(ValidationError): model.model_validate(data)


def test_decode_schema_accepts_missing_null_without_inventing_answer_quote():
    refs, answers = fragments('Kiểm tra địa chỉ.'), fragments('Kiểm tra tiền cọc.')
    model = selection_schema(refs,answers)
    selected = model.model_validate(selection(status='missing',answer_id=None).model_dump())
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
