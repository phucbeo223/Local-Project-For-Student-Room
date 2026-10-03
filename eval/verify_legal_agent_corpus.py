"""Real retrieval regression checks, independent of the generation/judge models."""
import json,re
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
    'every_source_has_government_url':all(urlparse(r.get('source_url') or '').scheme=='https' and
        (urlparse(r.get('source_url') or '').hostname or '').endswith(('.gov.vn', '.chinhphu.vn')) for c in checks for r in c['rows']),
    'contract_checklist_retains_article':has(1,'Điều 163.') and has(1,'1. Họ và tên') and has(1,'11. Chữ ký'),
    'contract_effect_not_statutory_commencement':all(not ('Công chứng, chứng thực hợp đồng' in r['content'])
        for c in checks for r in c['rows'] if r.get('heading')=='Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp'),
    'deposit_exception_preserved':has(4,'trừ trường hợp có thoả thuận khác'),
    'citizen_residence_duties':has(14,'Điều 9.'),
    'rental_residence_checklist_complete':has(15,'Tờ khai thay đổi thông tin cư trú') and has(15,'Giấy tờ, tài liệu chứng minh chỗ ở hợp pháp'),
    'moving_new_residence_direct_rule':has(16,'đăng ký tạm trú mới'),
    'house_fire_escape_requirement':has(17,'lối thoát nạn'),
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
Path('/eval/reports/legal_agent_retrieval_2026-10-03.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'gates':gates,'passed':report['passed']},ensure_ascii=False),flush=True)
engine.dispose()
if not report['passed']:raise SystemExit(2)
