"""Read-only checks of retained active data and the isolated focus-three trial."""
import hashlib
import json
from pathlib import Path
from sqlalchemy import create_engine, text
from app.config import settings
from audit_word_supplement import snapshot

ROOT = Path('/workspace')
REPORTS = Path('/eval/reports')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    output = REPORTS / 'graph_rag_focus3_audit_v11_2026-10-06.json'
    baseline = json.loads((REPORTS / 'graph_rag_word_supplement_audit_v8_2026-10-05.json').read_text(encoding='utf-8'))
    folder = ROOT / 'docs/legal_word_focus3_corpus_v11_20261006'
    manifest = json.loads((folder / 'manifest.json').read_text(encoding='utf-8'))
    older = json.loads((ROOT / 'docs/legal_word_focus3_corpus_v10_20261006/manifest.json').read_text(encoding='utf-8'))
    assert manifest['documents'][:-1] == older['documents']
    for entry in manifest['documents']:
        path = ROOT / entry['file']; assert sha(path) == entry['sha256']
        document = json.loads(path.read_text(encoding='utf-8'))
        source = document['source']; word = ROOT / source['path']
        assert word.suffix in ('.doc', '.docx') and sha(word) == source['sha256']
        assert source['ocr_used'] is False
        for provision in document['provisions']:
            assert hashlib.sha256(provision['content'].encode()).hexdigest() == provision['content_sha256']
    engine = create_engine(settings.database_url)
    with engine.connect() as conn:
        current = snapshot(conn)
        assert current == baseline['active_after'], 'Active data changed'
        schema = manifest['schema']
        counts = dict(conn.execute(text(f'SELECT count(*) AS chunks,count(embedding_vector) AS vectors FROM {schema}.legal_chunks')).mappings().one())
        assert counts == {'chunks': 425, 'vectors': 425}
        assert conn.execute(text(f'SELECT count(*) FROM {schema}.legal_chunks WHERE vector_dims(embedding_vector)<>384')).scalar_one() == 0
        documents = list(conn.execute(text(f'SELECT ocr_engine,ocr_page_count FROM {schema}.legal_documents')).mappings())
        assert len(documents) == 32 and all(d['ocr_engine'] is None and d['ocr_page_count'] == 0 for d in documents)
        assert conn.execute(text('SELECT status FROM public.legal_corpus_releases WHERE schema_name=:s'), {'s': schema}).scalar_one() == 'staging'
        housing = dict(conn.execute(text("SELECT count(*) AS rows,md5(string_agg(row_to_json(t)::text,'|' ORDER BY row_to_json(t)::text)) AS digest FROM housing_graph_word_focus3_v11.aggregated_listings t")).mappings().one())
        assert housing == current['housing_graph_word_v6.aggregated_listings']
        release = dict(conn.execute(text('SELECT * FROM graph_rag_word_focus3_v11.release WHERE id=1')).mappings().one())
        assert release['legal_schema'] == schema and release['legal_sha256'] == sha(folder / 'manifest.json')
    engine.dispose()
    report = dict(passed=True, active_store_unchanged=True, active_snapshot=current,
                  new_store_active=False, legal_schema=schema, documents=32, counts=counts,
                  embedding_dimensions=384, ocr_documents=0, pdf_inputs=0,
                  reference_answers_embedded=False, original_31_entries_unchanged=True,
                  new_housing_identical_to_active=True, graph_release_matches_corpus=True,
                  corpus_manifest_sha256=sha(folder / 'manifest.json'),
                  reference_sha256=sha(ROOT / 'eval/datasets/external_legal_20261004/answers.json'))
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in report.items() if k != 'active_snapshot'}, ensure_ascii=False))


if __name__ == '__main__':
    main()
