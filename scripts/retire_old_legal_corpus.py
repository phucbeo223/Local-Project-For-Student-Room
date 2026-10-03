"""Delete old legal rows only after verified backup, active new API and release gates."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,sys
from sqlalchemy import create_engine,text

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'apps/api'))
from app.config import settings

def load(name):return json.loads((ROOT/'eval/reports'/name).read_text(encoding='utf-8'))
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def old_snapshot(conn):
    return {table:dict(conn.execute(text(f'SELECT count(*) AS rows,md5(string_agg(row_to_json(t)::text,\'|\' ORDER BY id)) AS digest FROM public.{table} t')).mappings().one())
            for table in ('legal_documents','legal_chunks')}

def listing_snapshot(conn):
    return dict(conn.execute(text('SELECT count(*) AS rows,count(embedding_vector) AS vectors,'
        "md5(string_agg(id::text||coalesce(embedding_vector::text,''),'|' ORDER BY id)) AS vector_digest "
        'FROM public.aggregated_listings')).mappings().one())

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--apply',action='store_true')
    args=parser.parse_args()
    gate=load('legal_agent_release_gate_2026-10-03.json')
    backup=load('legal_agent_backup_2026-10-03.json')
    live=load('legal_agent_http_active_2026-10-03.json')
    assert gate['passed'] is True,'Evaluation/source gates have not passed'
    evaluation=ROOT/'eval/reports'/gate['evaluation_file']
    assert evaluation.parent.resolve()==(ROOT/'eval/reports').resolve()
    assert digest(evaluation)==gate['evaluation_sha256'],'Evaluated answers changed after release validation'
    assert live['passed'] is True and live['base_url']=='http://api:8000','Active API has not been tested'
    assert live['response']['corpus_schema']=='legal_v2','Active API still uses the original corpus'
    assert backup['restore_verified'] is True
    dump=ROOT/backup['backup_path']
    assert dump.is_file() and digest(dump)==backup['backup_sha256'],'Verified backup is missing or changed'
    engine=create_engine(settings.database_url)
    report={'apply':args.apply,'executed_at_utc':datetime.now(timezone.utc).isoformat(),
            'backup_path':backup['backup_path'],'backup_sha256':backup['backup_sha256']}
    with engine.begin() as conn:
        release=dict(conn.execute(text("SELECT * FROM public.legal_corpus_releases WHERE schema_name='legal_v2' FOR UPDATE")).mappings().one())
        assert release['status']=='active' and release['manifest_sha256']==gate['corpus_manifest_sha256']
        conn.execute(text('LOCK TABLE public.legal_documents,public.legal_chunks IN SHARE ROW EXCLUSIVE MODE'))
        before=old_snapshot(conn)
        listings=listing_snapshot(conn)
        assert before==backup['original'],'Original corpus changed since the verified backup'
        report.update(original_before=before,listings_before=listings)
        if args.apply:
            conn.execute(text('DELETE FROM public.legal_chunks'))
            conn.execute(text('DELETE FROM public.legal_documents'))
            conn.execute(text("UPDATE public.legal_corpus_releases SET status='retired' WHERE schema_name='public'"))
            after=old_snapshot(conn)
            assert all(t['rows']==0 for t in after.values())
            assert listing_snapshot(conn)==listings,'Listing vectors changed; rolling back deletion'
            report.update(original_after=after,listings_after=listing_snapshot(conn),deleted=True)
        else:report.update(deleted=False,action='Validated plan only; use --apply after reviewing this report')
    (ROOT/'eval/reports/legal_agent_retirement_2026-10-03.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report),flush=True);engine.dispose()

if __name__=='__main__':main()
