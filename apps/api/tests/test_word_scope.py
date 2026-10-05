import hashlib
import json
from pathlib import Path

import pytest
from app.room_service.chatbot.parser import parse_query
from app.room_service.chatbot.source_selection import selection_candidates, render_selection
from app.room_service.legal_knowledge.extractor import extract_document

ROOT=Path(__file__).resolve().parents[3]
CORPUS=ROOT/'docs/legal_word_corpus_v7_20261005'

@pytest.mark.parametrize('question',[
    'Soạn giúp tôi hợp đồng thuê phòng trọ',
    'Hướng dẫn điền tờ khai CT01',
    'Viết giúp tôi đơn khởi kiện đòi tiền cọc',
])
def test_forms_and_document_drafting_are_outside_product_scope(question):
    assert parse_query(question).intent=='out_of_scope'

@pytest.mark.parametrize('question',[
    'Hợp đồng thuê phòng có cần ghi rõ tiền cọc, tiền thuê và ngày thanh toán không?',
    'Tôi cần chuẩn bị những giấy tờ gì để đăng ký tạm trú tại phòng trọ?',
    'Nếu nhà trọ dùng chung đồng hồ nước, cách phân chia chi phí nên được thỏa thuận ra sao?',
])
def test_basic_tenant_questions_remain_in_scope(question):
    assert parse_query(question).intent=='legal_question'

def test_word_release_has_no_pdf_ocr_or_editorial_summary_input():
    manifest=json.loads((CORPUS/'manifest.json').read_text(encoding='utf-8'))
    assert len(manifest['documents'])==16
    for entry in manifest['documents']:
        path=ROOT/entry['file']
        assert hashlib.sha256(path.read_bytes()).hexdigest()==entry['sha256']
        data=json.loads(path.read_text(encoding='utf-8')); source=data['source']
        original=ROOT/source['path']
        assert original.suffix in ('.doc','.docx')
        assert source['page_kind']=='logical_document' and source['ocr_used'] is False
        assert hashlib.sha256(original.read_bytes()).hexdigest()==source['sha256']
        document=extract_document(original,ROOT/'Data')
        assert document.ocr_engine is None and not any(p.ocr_used for p in document.pages)
        text='\n\n'.join(p.text for p in document.pages)
        assert 'BẢN TRÍCH TUYỂN NGHIÊN CỨU' not in text
        for part in data['provisions']:
            assert all(segment in text for segment in part.get('source_segments',[part['content']]))
            assert 'GHI CHÚ NGỮ CẢNH' not in part['content']
            assert 'Ghi chú tuyển chọn:' not in part['content']

def test_housing_word_source_replaces_split_ocr_characters():
    data=json.loads((CORPUS/'housing79-word.json').read_text(encoding='utf-8'))
    text='\n'.join(p['content'] for p in data['provisions'] if p['article']=='163')
    assert 'thỏa thuận' in text and 'văn bản' in text
    assert 'th ỏa thuận' not in text and 'văn b ản' not in text
    assert 'giá giao dịch' in text

def test_provided_word_provenance_warning_survives_evidence_selection():
    warning='Nguồn là bản Word/trích tuyển được cung cấp, chưa xác minh toàn bộ câu chữ với bản chính thức.'
    row=dict(rank=1,title='Nguồn Word',category='privacy_data',heading='Sự đồng ý',
        source_scope_warning=warning,source_content_kind='provided_word_excerpt',
        content='Việc cung cấp dữ liệu cá nhân cần có sự đồng ý của chủ thể dữ liệu.')
    answer=render_selection('Ảnh căn cước được sử dụng như thế nào?',[row],selection_candidates([row]),
        '{"selected_ids":[1],"insufficient":false}','qwen-local','test')
    assert warning in answer.evidence_limitations and warning in answer.text

def test_word_provenance_notice_does_not_hide_actual_answer_gaps():
    from app.room_service.chatbot.legal_retrieval import legal_completion_status
    warning='Nguồn là bản Word/trích tuyển được cung cấp, chưa xác minh toàn bộ câu chữ với bản chính thức; không coi ghi chú biên tập là quy định pháp luật.'
    supported='Hợp đồng về nhà ở phải được lập thành văn bản, bao gồm thông tin và chữ ký của các bên [1].'
    assert legal_completion_status(supported+'\n'+warning)=='complete'
    assert legal_completion_status(supported+'\nChưa có nguồn cho điều kiện hoàn tiền.\n'+warning)=='partial'
