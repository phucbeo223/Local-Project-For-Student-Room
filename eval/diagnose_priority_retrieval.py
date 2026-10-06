"""Replay public legal retrieval against the real staging database; no LLM calls."""
import json
from pathlib import Path
from sqlalchemy import create_engine
from app.config import settings
from app.room_service.chatbot.agents import LegalRetrievalAgent, QuestionPlan
from app.room_service.chatbot.graph_retrieval import GraphChatRepository
from app.room_service.chatbot.providers import E5EmbeddingProvider, normalize_text


def main():
    report=json.loads(Path('/eval/reports/legal_repair_pilot_v18_20261006.json').read_text(encoding='utf-8'))
    case=next(c for c in report['cases'] if c['id']==45)
    plan=next(s['plan'] for s in case['agent_trace'] if s.get('agent')=='question_analysis')
    engine=create_engine(settings.database_url)
    repo=GraphChatRepository(engine,settings.chatbot_legal_schema,settings.chatbot_listing_schema,settings.chatbot_graph_schema)
    embedder=E5EmbeddingProvider(settings.chatbot_embedding_model)
    try:
        rows,embedding,trace=LegalRetrievalAgent(repo,embedder).retrieve(case['question'],QuestionPlan.model_validate(plan))
        result=dict(id=45,question=case['question'],llm_calls=0,local_embedding_calls=1,housing_retrieved=False,
            previous_headings=[s.get('heading') for s in case['sources']],
            repaired_sources=[{k:r.get(k) for k in ('rank','document_id','chunk_id','heading','source_url')} for r in rows],
            quality_remedy_retrieved=any('giam tien dich vu' in normalize_text(r['content']) and 'khong dat' in normalize_text(r['content']) for r in rows),
            trace=trace)
        Path('/eval/reports/legal_repair_retrieval_45_v19_20261006.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(json.dumps(result,ensure_ascii=False))
        assert result['quality_remedy_retrieved'], 'Quality remedy is still missing from actual retrieval'
    finally:
        engine.dispose()


if __name__=='__main__':main()
