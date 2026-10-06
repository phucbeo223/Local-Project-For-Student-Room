"""Read-only retention/provenance audit of an isolated Word trial."""
import argparse
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
    parser=argparse.ArgumentParser()
    parser.add_argument('--version',choices=['14','16'],default='16')
    args=parser.parse_args()
    folder = ROOT / f'docs/legal_word_repair_corpus_v{args.version}_20261006'
    manifest = json.loads((folder / 'manifest.json').read_text(encoding='utf-8'))
    for entry in manifest['documents']:
        path = ROOT / entry['file']
        assert sha(path) == entry['sha256']
        data = json.loads(path.read_text(encoding='utf-8'))
        source = data['source']
        word = ROOT / source['path']
        assert word.suffix.lower() in ('.doc', '.docx')
        assert sha(word) == source['sha256'] and source['ocr_used'] is False
        assert 'external_legal' not in source['path'] and 'answers' not in source['path']
        for p in data['provisions']:
            assert hashlib.sha256(p['content'].encode()).hexdigest() == p['content_sha256']
    baseline = json.loads((REPORTS / 'graph_rag_priority7_audit_v13_2026-10-06.json').read_text(encoding='utf-8'))
    engine = create_engine(settings.database_url)
    schema = manifest['schema']
    with engine.connect() as conn:
        current = snapshot(conn)
        assert current == baseline['active_snapshot'], 'Active data changed'
        counts = dict(conn.execute(text(f'SELECT count(*) AS chunks,count(embedding_vector) AS vectors FROM {schema}.legal_chunks')).mappings().one())
        import sys
        sys.path.insert(0,str(ROOT/'scripts'))
        from index_legal_agent_corpus import pieces
        expected=sum(len(pieces(p)) for entry in manifest['documents'] for p in json.loads((ROOT/entry['file']).read_text(encoding='utf-8'))['provisions'])
        assert counts == {'chunks': expected, 'vectors': expected}
        assert conn.execute(text(f'SELECT count(*) FROM {schema}.legal_chunks WHERE vector_dims(embedding_vector)<>384')).scalar_one() == 0
        documents = list(conn.execute(text(f'SELECT ocr_engine,ocr_page_count FROM {schema}.legal_documents')).mappings())
        assert len(documents) == len(manifest['documents']) and all(d['ocr_engine'] is None and d['ocr_page_count'] == 0 for d in documents)
        assert conn.execute(text('SELECT status FROM public.legal_corpus_releases WHERE schema_name=:s'), {'s': schema}).scalar_one() == 'staging'
        housing = dict(conn.execute(text(f"SELECT count(*) AS rows,md5(string_agg(row_to_json(t)::text,'|' ORDER BY row_to_json(t)::text)) AS digest FROM housing_graph_word_repair_v{args.version}.aggregated_listings t")).mappings().one())
        assert housing == current['housing_graph_word_v6.aggregated_listings']
        release = dict(conn.execute(text(f'SELECT * FROM graph_rag_word_repair_v{args.version}.release WHERE id=1')).mappings().one())
        assert release['legal_schema'] == schema and release['legal_sha256'] == sha(folder / 'manifest.json')
    engine.dispose()
    report = dict(passed=True, active_store_unchanged=True, active_snapshot=current,
        new_store_active=False, legal_schema=schema, documents=len(documents), counts=counts,
        embedding_dimensions=384, ocr_documents=0, pdf_inputs=0,
        reference_answers_embedded=False, new_housing_identical_to_active=True,
        graph_release_matches_corpus=True, corpus_manifest_sha256=sha(folder / 'manifest.json'),
        reference_sha256=sha(Path('/eval/datasets/external_legal_20261004/answers.json')))
    assert report['reference_sha256'] == baseline['reference_sha256']
    (REPORTS / f'legal_repair_audit_v{args.version}_20261006.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in report.items() if k != 'active_snapshot'}, ensure_ascii=False))


if __name__ == '__main__':
    main()
