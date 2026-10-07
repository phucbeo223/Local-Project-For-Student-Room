"""Record protected-table digests and explicit deployment flags without secrets."""
import argparse
import json
from pathlib import Path
from sqlalchemy import create_engine, text
from app.config import settings
import question_bank_ragas as bank


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--phase', choices=['before','after'], required=True)
    args = parser.parse_args()
    path = Path('/eval/reports/gemini_workflow_v19_runtime_'+args.phase+'_20261007.json')
    assert not path.exists()
    engine = create_engine(settings.database_url)
    with engine.connect() as conn:
        protected = {table:dict(conn.execute(text(f"SELECT count(*) AS rows,md5(string_agg(row_to_json(t)::text,'|' ORDER BY id)) AS digest FROM public.{table} t")).mappings().one()) for table in ('users','aggregated_listings')}
    result = dict(protected_tables=protected, legal_schema=settings.chatbot_legal_schema,
        graph_schema=settings.chatbot_graph_schema, listing_schema=settings.chatbot_listing_schema,
        pipeline_sha256=bank.pipeline_sha256(Path('/workspace/apps/api/app/room_service/chatbot')))
    if args.phase=='after':
        before = json.loads(path.with_name('gemini_workflow_v19_runtime_before_20261007.json').read_text(encoding='utf-8'))
        result['protected_tables_unchanged'] = before['protected_tables']==protected
        assert result['protected_tables_unchanged']
    bank.save_report(path,result)
    engine.dispose()
    print(json.dumps(result),flush=True)


if __name__=='__main__':
    main()
