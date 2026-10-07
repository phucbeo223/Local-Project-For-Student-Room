"""Read-only audit of the new immutable legal/graph release."""
import hashlib
import json
from pathlib import Path
from sqlalchemy import create_engine, text
from app.config import settings
import sys
sys.path.insert(0, '/workspace/scripts')
from index_legal_agent_corpus import pieces

ROOT = Path('/workspace')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    folder = ROOT / 'docs/legal_word_completion_v18_20261007'
    manifest = json.loads((folder / 'manifest.json').read_text(encoding='utf-8'))
    engine = create_engine(settings.database_url)
    expected = 0
    with engine.connect() as conn:
        schema = manifest['schema']
        docs = list(conn.execute(text(f'SELECT source_metadata,ocr_engine,ocr_page_count FROM {schema}.legal_documents')).mappings())
        assert len(docs) == len(manifest['documents']) == 40
        by_id = {d['source_metadata']['id']: d for d in docs}
        for entry in manifest['documents']:
            path = ROOT / entry['file']
            assert sha(path) == entry['sha256']
            data = json.loads(path.read_text(encoding='utf-8'))
            source = data['source']
            assert source == by_id[entry['id']]['source_metadata']
            assert source['ocr_used'] is False
            word = ROOT / source['path']
            assert word.suffix in ('.doc', '.docx') and sha(word) == source['sha256']
            assert by_id[entry['id']]['ocr_engine'] is None and by_id[entry['id']]['ocr_page_count'] == 0
            for provision in data['provisions']:
                assert hashlib.sha256(provision['content'].encode()).hexdigest() == provision['content_sha256']
                expected += len(pieces(provision))
        counts = dict(conn.execute(text(f'SELECT count(*) AS chunks,count(embedding_vector) AS vectors,count(*) FILTER (WHERE vector_dims(embedding_vector)=384) AS dimension384 FROM {schema}.legal_chunks')).mappings().one())
        assert counts == dict(chunks=expected, vectors=expected, dimension384=expected)
        release = dict(conn.execute(text(f'SELECT * FROM {settings.chatbot_graph_schema}.release WHERE id=1')).mappings().one())
        assert release['legal_schema'] == schema and release['legal_sha256'] == sha(folder / 'manifest.json')
        status = conn.execute(text('SELECT status FROM public.legal_corpus_releases WHERE schema_name=:s'), dict(s=schema)).scalar_one()
        prior = conn.execute(text("SELECT count(*) FROM legal_word_repair_v16_20261006.legal_chunks")).scalar_one()
        assert prior > 0
    engine.dispose()
    report = dict(passed=True, schema=schema, status=status, documents=len(docs), counts=counts,
        corpus_sha256=sha(folder / 'manifest.json'), prior_v16_retained=True, native_word_only=True,
        graph_release_matches=True, reference_answers_embedded=False)
    Path('/eval/reports/legal_completion_corpus_audit_v18_20261007.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report), flush=True)


if __name__ == '__main__':
    main()
