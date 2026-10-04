"""Source fidelity and behavior checks; references never become runtime data."""
import hashlib,json
from pathlib import Path
from app.room_service.chatbot.legal_retrieval import rerank_legal,evidence_issues
from app.room_service.chatbot.agent_workflow import SynthesizedLegalAnswer
from app.room_service.chatbot.evidence_units import contract_facets

ROOT=Path(__file__).resolve().parents[3]
def test_source_only_manifest_excludes_authored_guidance_and_every_body_has_a_hash():
    corpus=ROOT/'docs/legal_corpus_v5_20261004'
    manifest=json.loads((corpus/'manifest.json').read_text(encoding='utf-8'))
    assert manifest['documents']
    for entry in manifest['documents']:
        path=ROOT/entry['file'];assert hashlib.sha256(path.read_bytes()).hexdigest()==entry['sha256']
        doc=json.loads(path.read_text(encoding='utf-8'))
        assert doc['source']['source_url'].startswith('https://')
        assert doc['source'].get('page_kind')!='editorial_guidance'
        assert not entry['id'].startswith(('guidance-','legacy-'))
        for part in doc['provisions']:
            assert hashlib.sha256(part['content'].encode()).hexdigest()==part['content_sha256']
            assert part.get('kind')!='editorial_guidance'
            assert not part['heading'].startswith('Q:')

def test_brokerage_paperwork_retrieves_actual_fee_and_payment_clause():
    doc=json.loads((ROOT/'docs/legal_corpus_v5_20261004/broker06.json').read_text(encoding='utf-8'))
    part=doc['provisions'][0]
    rows=[dict(chunk_id=1,title=doc['source']['title'],heading=part['heading'],category='real_estate_brokerage',
               content=part['content'],similarity_score=.5,source_id='broker06')]
    ranked=rerank_legal('Khoản phí môi giới nên được thỏa thuận và thể hiện trong giấy tờ ra sao?',rows,5)
    assert ranked and ranked[0]['_rerank_score']>1
    assert 'thời hạn thanh toán' in ranked[0]['content']

def test_deposit_evidence_exists_in_signed_original_first_part():
    doc=json.loads((ROOT/'docs/legal_corpus_v5_20261004/civil91first.json').read_text(encoding='utf-8'))
    parts=[part for part in doc['provisions'] if part['article']=='328']
    assert parts and min(part['page_from'] for part in parts)==86 and max(part['page_to'] for part in parts)==87
    assert any('Đặt cọc' in part['heading'] for part in parts)
    assert doc['source']['path'].endswith('/civil91first.pdf')

def test_price_facet_recognizes_original_pdf_ocr_without_rewriting_source():
    doc=json.loads((ROOT/'docs/legal_corpus_v5_20261004/housing79.json').read_text(encoding='utf-8'))
    part=next(p for p in doc['provisions'] if p['article']=='163' and p['clause']=='3')
    assert 'giá giao d ịch' in part['content']
    assert 'rent' in contract_facets(dict(category='housing_contract',content=part['content']))

def test_invoice_check_question_does_not_demote_published_checking_guidance():
    doc=json.loads((ROOT/'docs/legal_corpus_v5_20261004/electricity-cantho-guidance.json').read_text(encoding='utf-8'))
    part=doc['provisions'][0]
    row=dict(chunk_id=1,category='electricity',title=doc['source']['title'],heading=part['heading'],
             content=part['content'],source_id=doc['source']['id'],similarity_score=.5)
    ranked=rerank_legal('Nếu tôi nghi tiền điện bị thu cao hơn quy định, nên kiểm tra hóa đơn và căn cứ nào?',[row],5)
    assert ranked and ranked[0]['_rerank_score']>.8

def test_application_scope_warning_does_not_reject_a_cited_synthesis():
    from app.room_service.chatbot.source_selection import selection_candidates,render_selection
    doc=json.loads((ROOT/'docs/legal_corpus_v5_20261004/electricity-cantho-guidance.json').read_text(encoding='utf-8'))
    row=dict(rank=1,title=doc['source']['title'],category='electricity',source_id=doc['source']['id'],
             heading=doc['provisions'][0]['heading'],content=doc['provisions'][0]['content'])
    query='Nếu tôi nghi tiền điện bị thu cao hơn quy định, nên kiểm tra hóa đơn và căn cứ nào?'
    draft=render_selection(query,[row],selection_candidates([row]),'{"selected_ids":[1],"insufficient":false}','qwen-local','test')
    issues=evidence_issues('\n'.join(draft.evidence_limitations),[row],query)
    assert not any('chưa gắn trích dẫn' in issue for issue in issues)

def test_numeric_case_question_is_not_an_uncited_claim_but_legal_premise_is():
    row=dict(rank=1,heading='Nguồn thử',content='Hợp đồng thuê có thể có thời hạn 12 tháng.')
    assert not evidence_issues('Hợp đồng thuê của bạn có thời hạn từ 12 tháng trở lên không?',[row],'Hợp đồng thuê phòng?')
    assert not evidence_issues('Hợp đồng thuê phòng của bạn có điều khoản thỏa thuận riêng nào về việc hoàn trả hoặc trừ tiền cọc khi chấm dứt hợp đồng không?',[row],'Hợp đồng thuê phòng?')
    assert not evidence_issues('Hợp đồng của bạn có quy định về bồi thường hư hỏng khi trả phòng không?',[row],'Hợp đồng thuê phòng?')
    issues=evidence_issues('Có phải chủ trọ bắt buộc hoàn trả 99 triệu đồng không?',[row],'Hợp đồng thuê phòng?')
    assert any('chưa gắn trích dẫn' in issue for issue in issues)
    assert evidence_issues('Theo hợp đồng, chủ trọ có nghĩa vụ hoàn trả 99 triệu đồng đúng không?',[row],'Hợp đồng thuê phòng?')

def test_cited_missing_topics_are_not_affirmative_penalties_or_refunds():
    rows=[dict(rank=1,heading='Hướng dẫn',content='Kiểm tra hóa đơn và định mức điện.'),
          dict(rank=2,heading='Giá điện',content='Đối chiếu cách tính tiền điện với hóa đơn.')]
    for answer in (
        'Nguồn tài liệu chưa cung cấp mức biểu giá tiền cụ thể bằng đồng cũng như chế tài xử phạt khi chủ nhà trọ thu sai quy định [2].',
        'Nguồn chưa nêu căn cứ pháp lý về quy trình xử lý, khiếu nại, mức phạt hoặc việc bồi thường, hoàn trả tiền thu thừa [1] [2].',
    ):
        assert not evidence_issues(answer,rows,'Nên kiểm tra hóa đơn và căn cứ nào?')
    for answer in (
        'Chưa đủ căn cứ xác định chế tài, nhưng người thuê có quyền được hoàn trả 99 triệu đồng [1].',
        'Nguồn chưa nêu mức phạt, và chủ nhà phải hoàn trả 99 triệu đồng [1].',
        'Nguồn chưa nêu mức phạt, nhưng người thuê được hoàn trả 99 triệu đồng [1].',
        'Pháp luật không quy định việc hoàn trả [1].',
    ):
        assert evidence_issues(answer,rows,'Nên kiểm tra hóa đơn và căn cứ nào?')

def test_writer_can_cover_more_than_five_requested_facets_without_uncited_claims():
    line={'text':'Kiểm tra nội dung có căn cứ trong nguồn.','source_ranks':[1]}
    value=SynthesizedLegalAnswer.model_validate(dict(summary=line,steps=[line]*7,limitations=[],follow_up_questions=[],coverage='complete'))
    assert len(value.steps)==7

def test_provider_lookup_excerpt_has_provenance_and_beats_unrelated_complaint():
    corpus=ROOT/'docs/legal_corpus_v6_20261005'
    doc=json.loads((corpus/'water-cantho-invoice-guide.json').read_text(encoding='utf-8'))
    source=doc['source'];part=doc['provisions'][0]
    assert source['source_url'].startswith('https://ctn-cantho.com.vn/')
    assert hashlib.sha256((ROOT/source['path']).read_bytes()).hexdigest()==source['sha256']
    assert source['origin_documents'][0]['sha256']==source['original_sha256']
    assert 'IDKH' in part['content'] and 'Giấy báo/Biên nhận' in part['content']
    assert len(part['content'].split())<=25
    rows=[dict(chunk_id=1,category='water_cantho',title=source['title'],heading=part['heading'],
               content=part['content'],source_id=source['id'],similarity_score=.5),
          dict(chunk_id=2,category='water_cantho',title='Giải quyết khiếu nại',heading='Khiếu nại',
               content='Giải quyết khiếu nại về tiền nước trong thời hạn quy định.',source_id='water117',similarity_score=.8)]
    assert rerank_legal('Muốn tra cứu hóa đơn tiền nước để đối chiếu thì làm như thế nào?',rows,5)[0]['chunk_id']==1

def test_water_publisher_scope_is_preserved_without_inventing_rental_tariff():
    from app.room_service.chatbot.source_selection import selection_candidates,render_selection
    doc=json.loads((ROOT/'docs/legal_corpus_v6_20261005/water-cantho-invoice-guide.json').read_text(encoding='utf-8'))
    row=dict(rank=1,title=doc['source']['title'],category='water_cantho',source_id=doc['source']['id'],
             heading=doc['provisions'][0]['heading'],content=doc['provisions'][0]['content'])
    query='Tôi muốn tra cứu hóa đơn tiền nước để đối chiếu số tiền.'
    draft=render_selection(query,[row],selection_candidates([row]),'{"selected_ids":[1],"insufficient":false}','qwen-local','test')
    assert any('đơn vị trên hóa đơn' in value for value in draft.evidence_limitations)
    assert not any('chưa gắn trích dẫn' in issue for issue in evidence_issues('\n'.join(draft.evidence_limitations),[row],query))

def test_water_lookup_expands_customer_code_without_suppressing_dispute_questions():
    from app.room_service.chatbot.legal_retrieval import expand_legal_query
    query='Tôi có thể đối chiếu tiền nước trên hóa đơn với đơn vị cấp nước như thế nào?'
    assert 'IDKH' in expand_legal_query(query)
    row=dict(chunk_id=2,category='water_cantho',title='Tiền nước',heading='Yêu cầu xem xét',
             content='Khách hàng yêu cầu xem xét lại số tiền nước; có thể đề nghị hòa giải.',source_id='water117',similarity_score=.8)
    assert not rerank_legal(query,[dict(row)],5)
    assert rerank_legal('Tôi muốn khiếu nại tranh chấp tiền nước và đề nghị hòa giải',[dict(row)],5)

def test_native_uppercase_form_labels_are_usable_but_broken_font_text_is_not():
    from app.room_service.legal_knowledge.quality import usable_legal_text
    doc=json.loads((ROOT/'docs/legal_corpus_v6_20261005/water-cantho-invoice-portal.json').read_text(encoding='utf-8'))
    assert usable_legal_text(doc['provisions'][0]['content'])
    assert not usable_legal_text('diQn diQn diQn chri th6ng b6n')
