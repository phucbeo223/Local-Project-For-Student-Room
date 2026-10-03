"""Inspect real database retrieval without generation or user event writes."""
import json
from pathlib import Path
from sqlalchemy import create_engine
from app.config import settings
from app.room_service.chatbot.router import init_chatbot, get_service
from app.room_service.chatbot.topics import required_evidence_categories
from question_bank_ragas import load_questions

engine = create_engine(settings.database_url)
init_chatbot(engine)
service = get_service()
checks = []
for case in load_questions(Path('/question_bank.md')):
    if case['id'] not in [4,14,17,22,28,29,33,36]: continue
    embedding = service.embedder.embed_query(case['question'])
    rows = service.repo.retrieve_legal(case['question'], embedding.vector, limit=5)
    required = required_evidence_categories(case['question'])
    found = set(r['category'] for r in rows)
    result = {'id': case['id'], 'question':case['question'], 'required':list(required),
              'missing':sorted(set(required)-found), 'rows':[{k:r.get(k) for k in
              ['rank','heading','category','source_path','content']} for r in rows]}
    checks.append(result)
    print(json.dumps({'id':case['id'], 'missing':result['missing'],
                      'sources':[(r['category'],r['heading']) for r in rows]},ensure_ascii=False),flush=True)
Path('/eval/reports/legal_retrieval_supplement_2026-10-03.json').write_text(
    json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')
assert all(c['rows'] for c in checks), 'Real SQL query returned no contexts'
q29 = next(c for c in checks if c['id']==29)
assert not q29['missing'], 'Mixed request lost an explicit subject'
assert any('163' in (r['heading'] or '') and '1' in (r['heading'] or '') for r in q29['rows'] if r['category']=='housing_contract')
assert any('Giấy tờ, tài liệu chứng minh chỗ ở hợp pháp' in r['content'] and 'Tờ khai thay đổi thông tin cư trú' in r['content'] for r in q29['rows'])
assert any('Điều 9.' in (r['heading'] or '') for r in next(c for c in checks if c['id']==14)['rows'])
assert any('Điều 20.' in (r['heading'] or '') and 'lối thoát nạn' in r['content'] for r in next(c for c in checks if c['id']==17)['rows'])
assert any('trừ trường hợp có thoả thuận khác.' in r['content'] for r in next(c for c in checks if c['id']==4)['rows'])
assert any('Điều 161.' in (r['heading'] or '') for r in next(c for c in checks if c['id']==22)['rows'])
engine.dispose()
