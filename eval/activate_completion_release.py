"""Activate the audited release atomically, retaining every previous corpus."""
import hashlib
import json
from pathlib import Path
from sqlalchemy import create_engine, text
from app.config import settings
import question_bank_ragas as bank


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def protected(conn):
    return {table: dict(conn.execute(text(f"SELECT count(*) AS rows,md5(string_agg(row_to_json(t)::text,'|' ORDER BY id)) AS digest FROM public.{table} t")).mappings().one()) for table in ('users', 'aggregated_listings')}


def main():
    reports = Path('/eval/reports')
    run_path = reports / 'gemini_completion_36_final_v18_20261007.json'
    run = json.loads(run_path.read_text(encoding='utf-8'))
    assert run['completed'] and len(run['cases']) == 36
    assert all('answer' in c and not c.get('error_type') for c in run['cases'])
    assert bank.pipeline_sha256(Path('/workspace/apps/api/app/room_service/chatbot')) == run['pipeline_sha256']
    audit = json.loads((reports / 'legal_completion_corpus_audit_v18_20261007.json').read_text(encoding='utf-8'))
    assert audit['passed']
    manifest = Path('/workspace/docs/legal_word_completion_v18_20261007/manifest.json')
    assert sha(manifest) == audit['corpus_sha256']
    engine = create_engine(settings.database_url)
    schema = 'legal_word_completion_v18_20261007'
    with engine.begin() as conn:
        conn.execute(text("SELECT pg_advisory_xact_lock(hashtext('legal-completion-release'))"))
        before = protected(conn)
        previous = list(conn.execute(text("SELECT schema_name FROM public.legal_corpus_releases WHERE status='active'")).scalars())
        graph = conn.execute(text('SELECT legal_sha256 FROM graph_rag_word_completion_v18.release WHERE id=1')).scalar_one()
        assert graph == sha(manifest)
        assert conn.execute(text(f'SELECT count(embedding_vector) FROM {schema}.legal_chunks')).scalar_one() == 497
        conn.execute(text("UPDATE public.legal_corpus_releases SET status='retired' WHERE status='active' AND schema_name<>:s"), dict(s=schema))
        updated = conn.execute(text("UPDATE public.legal_corpus_releases SET status='active',activated_at=now() WHERE schema_name=:s"), dict(s=schema))
        assert updated.rowcount == 1
        after = protected(conn)
        assert before == after
    engine.dispose()
    result = dict(activated=True, schema=schema, previous_active_schemas=previous,
        prior_indexes_retained=True, protected_before=before, protected_after=after,
        runtime_run_sha256=sha(run_path), pipeline_sha256=run['pipeline_sha256'],
        corpus_sha256=sha(manifest), previous_api_image='nckh-api:before-completion-20261007')
    (reports / 'gemini_completion_activation_20261007.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(result), flush=True)


if __name__ == '__main__':
    main()
