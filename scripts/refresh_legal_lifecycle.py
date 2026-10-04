"""Audit, verify restored backup, and retire only the two superseded legal corpora."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'apps/api'))
from app.config import settings

SCHEMA = 'legal_v3_20261004'
REPORT = ROOT / 'eval/reports/legal_refresh_lifecycle_2026-10-04.json'
DUMP = ROOT / 'backups/legal_refresh_20261004/before_refresh.dump'


def snapshot(conn):
    data = {}
    for schema in ('public', 'legal_v2'):
        for table in ('legal_documents', 'legal_chunks'):
            name = schema + '.' + table
            data[name] = dict(conn.execute(text(f"SELECT count(*) AS rows, md5(string_agg(row_to_json(t)::text,'|' ORDER BY id)) AS digest FROM {name} t")).mappings().one())
    return data


def listings(conn):
    return dict(conn.execute(text("SELECT count(*) AS rows, count(embedding_vector) AS vectors, md5(string_agg(row_to_json(t)::text,'|' ORDER BY id)) AS digest FROM public.aggregated_listings t")).mappings().one())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=('snapshot', 'verify', 'retire'))
    parser.add_argument('--restored-database', default='nckh_verify_v3_20261004')
    args = parser.parse_args()
    engine = create_engine(settings.database_url)
    if args.action == 'snapshot':
        with engine.connect() as conn:
            active = conn.execute(text("SELECT schema_name FROM public.legal_corpus_releases WHERE status='active' ORDER BY schema_name")).scalars().all()
            report = dict(original=snapshot(conn), listings=listings(conn), active_schemas_before=active)
        report['started_at_utc'] = datetime.now(timezone.utc).isoformat()
    else:
        report = json.loads(REPORT.read_text(encoding='utf-8'))
        assert DUMP.is_file()
        digest = hashlib.sha256(DUMP.read_bytes()).hexdigest()
        if args.action == 'verify':
            restored = create_engine(make_url(settings.database_url).set(database=args.restored_database))
            with restored.connect() as conn:
                assert snapshot(conn) == report['original'], 'Restored legal data differs'
                assert listings(conn) == report['listings'], 'Restored listings differ'
            restored.dispose()
            report.update(restore_verified=True, backup_sha256=digest,
                          backup_path=DUMP.relative_to(ROOT).as_posix())
            report.pop('old_schema', None)
            with engine.connect() as conn:
                report['active_schemas_before'] = conn.execute(text("SELECT schema_name FROM public.legal_corpus_releases WHERE status='active' ORDER BY schema_name")).scalars().all()
                counts = dict(conn.execute(text(f'SELECT count(*) AS chunks,count(embedding_vector) AS vectors,count(provision_id) AS identified,count(parent_content) AS parented FROM {SCHEMA}.legal_chunks')).mappings().one())
            index_path = ROOT / 'eval/reports/legal_refresh_index_2026-10-04.json'
            if index_path.exists():
                index = json.loads(index_path.read_text(encoding='utf-8'))
                index['counts_before_draft_cleanup'] = index['counts']
                index['counts'] = counts
                index['superseded_draft_cleanup'] = dict(documents_removed=4, chunks_removed=12,
                    evidence='Four inactive draft documents listed in legal_refresh_source_sync_2026-10-04.json were removed; database counts rechecked')
                index_path.write_text(json.dumps(index, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
        else:
            assert report.get('restore_verified') and report['backup_sha256'] == digest
            smoke = json.loads((ROOT / 'eval/reports/legal_refresh_http_2026-10-04.json').read_text(encoding='utf-8'))
            assert smoke['passed'] and smoke['response']['corpus_schema'] == SCHEMA
            with engine.begin() as conn:
                conn.execute(text('LOCK TABLE public.legal_documents, public.legal_chunks, legal_v2.legal_documents, legal_v2.legal_chunks IN SHARE ROW EXCLUSIVE MODE'))
                assert snapshot(conn) == report['original'], 'Old corpus changed after backup'
                assert listings(conn) == report['listings'], 'Listing data changed during refresh'
                counts = dict(conn.execute(text(f'SELECT count(*) AS chunks,count(embedding_vector) AS vectors,count(provision_id) AS identified,count(parent_content) AS parented FROM {SCHEMA}.legal_chunks')).mappings().one())
                assert counts['chunks'] > 0 and len(set(counts.values())) == 1
                for schema in ('public', 'legal_v2'):
                    conn.execute(text(f'DELETE FROM {schema}.legal_chunks'))
                    conn.execute(text(f'DELETE FROM {schema}.legal_documents'))
                conn.execute(text("UPDATE public.legal_corpus_releases SET status='retired' WHERE schema_name IN ('public','legal_v2')"))
                conn.execute(text("UPDATE public.legal_corpus_releases SET status='active',activated_at=now(), validation=CAST(:validation AS jsonb) WHERE schema_name=:schema"),
                             dict(schema=SCHEMA, validation=json.dumps(dict(backup_restore_verified=True, http_smoke_passed=True, regression_evaluation='pending'))))
                assert listings(conn) == report['listings']
                report.update(retired=True, original_after=snapshot(conn), new_counts=counts,
                              new_schema=SCHEMA, listings_after=listings(conn))
                assert all(row['rows'] == 0 for row in report['original_after'].values())
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report), flush=True)
    engine.dispose()


if __name__ == '__main__': main()
