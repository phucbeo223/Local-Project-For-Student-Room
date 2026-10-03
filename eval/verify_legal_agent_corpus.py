"""Real retrieval regression checks, independent of the generation/judge models."""
import json,re,argparse
from pathlib import Path
from urllib.parse import urlparse
from sqlalchemy import create_engine,text
from app.config import settings
from app.room_service.chatbot.repo import ChatRepository
from app.room_service.chatbot.providers import E5EmbeddingProvider,normalize_text
from app.room_service.chatbot.topics import required_evidence_categories
from question_bank_ragas import load_questions

engine=create_engine(settings.database_url)
embedder=E5EmbeddingProvider(settings.chatbot_embedding_model)
repo=ChatRepository(engine,'legal_v2')
checks=[]
parser=argparse.ArgumentParser()
parser.add_argument('--output',type=Path,default=Path('/eval/reports/legal_agent_retrieval_2026-10-03.json'))
args=parser.parse_args()
for case in load_questions(Path('/question_bank.md')):
    embedded=embedder.embed_query(case['question'])
    rows=repo.retrieve_legal(case['question'],embedded.vector,limit=5)
    required=set(required_evidence_categories(case['question']))
    found={r['category'] for r in rows}
    checks.append({'id':case['id'],'question':case['question'],'missing_categories':sorted(required-found),
                   'rows':[{k:r.get(k) for k in ('rank','title','heading','category','source_url','source_path','content','context_complete','provision_id')} for r in rows]})
    print(json.dumps({'id':case['id'],'missing':sorted(required-found),'sources':[(r['category'],r['heading']) for r in rows]},ensure_ascii=False),flush=True)
by_id={c['id']:c for c in checks}
def has(n,word):return any(word in (r.get('heading') or '')+' '+r['content'] for r in by_id[n]['rows'])
gates={
    'all_36_retrieve_contexts':all(c['rows'] for c in checks),
    'all_required_categories':all(not c['missing_categories'] for c in checks),
    'every_source_has_verified_public_provenance':all(urlparse(r.get('source_url') or '').scheme=='https' and
        ((urlparse(r.get('source_url') or '').hostname or '').endswith(('.gov.vn', '.chinhphu.vn','.cdnchinhphu.vn')) or
         r.get('source_url')=='https://capnuoccantho2.com.vn/View.aspx?wc=63&wp=332') for c in checks for r in c['rows']),
    'editorial_notes_not_quoted_as_law':all('Ghi chú tuyển chọn:' not in r['content'] for c in checks for r in c['rows']),
    'rental_electricity_excludes_dormitories':all('ky tuc xa' not in normalize_text(r['content']) for n in (5,6,7,8) for r in by_id[n]['rows'] if 'Hiệu lực' not in (r.get('heading') or '')),
    'contract_checklist_retains_article':has(1,'Điều 163.') and has(1,'1. Họ và tên') and has(1,'11. Chữ ký'),
    'rental_contract_price_and_payment':has(2,'giá giao dịch') and has(2,'Thời hạn và phương thức thanh toán'),
    'rental_contract_deposit_facet':has(2,'Điều 328.'),
    'reporting_people_have_direct_evidence_guidance':all(has(n,'chứng từ chuyển tiền') or has(n,'lịch sử giao dịch') for n in (34,36)),
    'electric_notice_has_local_guidance_not_relabelled_as_statute':any(
        r.get('heading','').startswith('Hướng dẫn công khai') and 'ghi chỉ số công tơ' in r['content']
        and 'btgdv.cantho.gov.vn' in r.get('source_url','') for r in by_id[8]['rows']),
    'fraud_distinction_retrieves_constituent_elements':has(35,'thủ đoạn gian dối'),
    'contract_effect_not_statutory_commencement':all(not ('Công chứng, chứng thực hợp đồng' in r['content'])
        for c in checks for r in c['rows'] if r.get('heading')=='Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp'),
    'deposit_exception_preserved':has(4,'trừ trường hợp có thoả thuận khác'),
    'citizen_residence_duties':has(14,'Điều 9.'),
    'ordinary_rental_residence_conditions':has(13,'Điều 27.') and has(13,'30 ngày trở lên'),
    'ordinary_rental_excludes_dormitory':all('ky tuc xa' not in normalize_text(r['content']) for r in by_id[13]['rows']),
    'rental_residence_checklist_complete':has(15,'Tờ khai thay đổi thông tin cư trú') and has(15,'Giấy tờ, tài liệu chứng minh chỗ ở hợp pháp'),
    'moving_new_residence_direct_rule':has(16,'đăng ký tạm trú mới'),
    'residence_commencement_retained':has(16,'01 tháng 7 năm 2026'),
    'residence_clause_eight_not_swallowed':all('Việc thông báo về kết quả' not in r['content'] for c in checks for r in c['rows'] if 'Điều 3.' in (r.get('heading') or '') and 'Khoản 7' in (r.get('heading') or '')),
    'house_fire_escape_requirement':has(17,'lối thoát nạn'),
    'locked_escape_door_correct_clause':any('Điều 24.' in (r.get('heading') or '') and 'Khoản 3' in (r.get('heading') or '') and 'Khóa cửa đi' in r['content'] for r in by_id[19]['rows']),
    'fire_penalty_scope_and_commencement':has(19,'đối với cá nhân') or has(19,'đôi với cá nhân'),
    'fire_short_commencement_retained':has(19,'01 tháng 7 năm 2025'),
    'no_locked_door_in_clause_two':all('Khóa cửa đi' not in r['content'] for c in checks for r in c['rows'] if 'Điều 24.' in (r.get('heading') or '') and 'Khoản 2' in (r.get('heading') or '')),
    'landlord_authority_rule':has(22,'Điều 161.'),
    'mixed_identity_three_topics':not by_id[29]['missing_categories'],
    'contract_identity_contents':has(29,'Điều 163.'),
}
with engine.connect() as conn:
    integrity=dict(conn.execute(text('SELECT count(*) AS chunks,count(embedding_vector) AS vectors,'
        'count(provision_id) AS identified,count(parent_content) AS parented FROM legal_v2.legal_chunks')).mappings().one())
    gates['all_chunks_embedded_and_parented']=len(set(integrity.values()))==1 and integrity['chunks']>0
report={'schema':'legal_v2','gates':gates,'passed':all(gates.values()),'integrity':integrity,'cases':checks,
        'note':'Retrieval gates are not RAGAS scores and do not validate all legal interpretations.'}
q2=by_id[2]['question']
expanded_queries=['Hợp đồng thuê nhà nội dung phương thức thanh toán','Thỏa thuận thuê nhà giá giao dịch thời hạn thuê','Các bên thuê và cho thuê giá tiền thuê']
rows=repo.retrieve_legal(q2,embedder.embed_query(q2+'\n'+'\n'.join(expanded_queries)).vector,
                        search_queries=expanded_queries,limit=5)
from app.room_service.chatbot.evidence_units import requested_contract_facets,contract_facets
gates['original_facets_survive_gemini_style_expansion']=requested_contract_facets(q2)<=set().union(*(contract_facets(r) for r in rows))
gates['moving_residence_reference_resolved']=has(16,'Điều 6.') and has(16,'rà soát, cập nhật')
gates['whole_house_fire_rule_retains_classification']=has(18,'khoản 3') and has(18,'danh mục cơ sở')
gates['tenant_fee_has_service_contract_basis']=has(24,'dịch vụ') and not all('Khoản 2' in (r.get('heading') or '') and 'Điều 63.' in (r.get('heading') or '') for r in by_id[24]['rows'])
gates['local_water_basis_present']=has(9,'Cần Thơ')
gates['repeal_inventory_fragments_excluded']=all(not re.search(r'Thông tư số \d+/\d+/TT-BCA',r['content']) for c in checks for r in c['rows'] if r.get('heading')=='Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp' and r['category']=='residence')
report['expanded_q2']=[{k:r.get(k) for k in ('title','heading','content')} for r in rows]
report['passed']=all(gates.values())
args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'gates':gates,'passed':report['passed']},ensure_ascii=False),flush=True)
engine.dispose()
if not report['passed']:raise SystemExit(2)
