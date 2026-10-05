"""Read-only integration check of evidence inclusion before invoking models."""
import json
from sqlalchemy import create_engine
from app.config import settings
from app.room_service.chatbot.repo import ChatRepository
from app.room_service.chatbot.legal_retrieval import expand_legal_query
import question_bank_ragas as bank
from pathlib import Path

engine = create_engine(settings.database_url)
repo = ChatRepository(engine, legal_schema='legal_word_focus3_v11_20261006')
cases = [c for c in bank.load_questions(Path('/housing_bank.md')) if c['id'] in (48, 49)]
for case in cases:
    rows = repo.retrieve_legal(case['question'], None, limit=5)
    if case['id'] == 48:
        assert any(r.get('source_id') == 'nhatot-report-proof-word' for r in rows), 'Missing literal image evidence'
    else:
        assert any('01 tháng 01 năm 2027' in r['content'] for r in rows), 'Missing delayed commencement source'
        assert any('24 giờ' in r['content'] and 'cung cấp' in r['content'].lower() for r in rows)
        assert any('số định danh cá nhân' in r['content'] for r in rows), 'Missing identity fields'
    print(json.dumps(dict(id=case['id'], query=expand_legal_query(case['question']),
                          sources=[dict(rank=r['rank'], id=r.get('source_id'), heading=r['heading'], chars=len(r['content'])) for r in rows]), ensure_ascii=False))
engine.dispose()
