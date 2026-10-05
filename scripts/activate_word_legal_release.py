"""Verify a restorable backup, activate Word release, remove old legal indexes."""
from pathlib import Path
import argparse
import hashlib
import json
import re
from sqlalchemy import create_engine,text
from sqlalchemy.engine import make_url
from app.config import settings
from index_legal_agent_corpus import pieces

ROOT=Path(__file__).resolve().parents[1]
SCHEMA='legal_word_v7_20261005'
REPORT=ROOT/'eval/reports/graph_rag_word_release_v7_2026-10-05.json'
BACKUP=ROOT/'backups/word_scope_20261005/before_word_scope.dump'

def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def protected(conn):
    return {table:dict(conn.execute(text(f"SELECT count(*) AS rows,md5(string_agg(row_to_json(t)::text,'|' ORDER BY id)) AS digest FROM public.{table} t")).mappings().one()) for table in ('aggregated_listings','users')}
def legal_snapshot(conn,schema):
    assert re.fullmatch(r'legal_[a-z0-9_]+',schema)
    return {table:dict(conn.execute(text(f"SELECT count(*) AS rows,md5(string_agg(row_to_json(t)::text,'|' ORDER BY id)) AS digest FROM {schema}.{table} t")).mappings().one()) for table in ('legal_documents','legal_chunks')}

def main():
    p=argparse.ArgumentParser();p.add_argument('action',choices=('verify','activate','remove-old'));p.add_argument('--http',type=Path)
    a=p.parse_args(); engine=create_engine(settings.database_url)
    if a.action=='verify':
        restored=create_engine(make_url(settings.database_url).set(database='nckh_verify_word_v7'))
        with engine.connect() as c,restored.connect() as r:
            before=protected(c); assert before==protected(r)
            old=[s for s in c.execute(text("SELECT schema_name FROM public.legal_corpus_releases WHERE schema_name<>:new AND schema_name<>'public'"),{'new':SCHEMA}).scalars() if c.execute(text('SELECT to_regnamespace(:s)'),{'s':s}).scalar()]
            for s in old: assert legal_snapshot(c,s)==legal_snapshot(r,s),s
        report={'backup_restore_verified':True,'backup_sha256':digest(BACKUP),'protected_before':before,'old_legal_schemas':old}
        restored.dispose()
    else:
        report=json.loads(REPORT.read_text(encoding='utf-8'))
        assert report['backup_restore_verified'] and report['backup_sha256']==digest(BACKUP)
        with engine.begin() as c:
            assert protected(c)==report['protected_before'],'Housing or user rows changed'
            rows=list(c.execute(text(f'SELECT source_metadata FROM {SCHEMA}.legal_documents')).scalars())
            assert len(rows)==16 and all(m['path'].endswith(('.doc','.docx')) and m['ocr_used'] is False and digest(ROOT/m['path'])==m['sha256'] for m in rows)
            counts=dict(c.execute(text(f'SELECT count(*) AS chunks,count(embedding_vector) AS vectors FROM {SCHEMA}.legal_chunks')).mappings().one())
            manifest=json.loads((ROOT/'docs/legal_word_corpus_v7_20261005/manifest.json').read_text(encoding='utf-8'))
            expected=sum(len(pieces(p)) for entry in manifest['documents']
                for p in json.loads((ROOT/entry['file']).read_text(encoding='utf-8'))['provisions'])
            assert counts['chunks']==counts['vectors']==expected and expected>0
            # Correct the old importer's substring-based OCR label. Source
            # extraction has been checked above: native Word with ocr_used=false.
            c.execute(text(f'UPDATE {SCHEMA}.legal_documents SET ocr_engine=NULL,ocr_page_count=0'))
            assert c.execute(text(f'SELECT count(*) FROM {SCHEMA}.legal_documents WHERE ocr_engine IS NOT NULL OR ocr_page_count<>0')).scalar_one()==0
            if a.action=='activate':
                c.execute(text("UPDATE public.legal_corpus_releases SET status='retired' WHERE status='active' AND schema_name<>:schema"),{'schema':SCHEMA})
                c.execute(text("UPDATE public.legal_corpus_releases SET status='active',activated_at=now() WHERE schema_name=:schema"),{'schema':SCHEMA})
                report['activated']=True
            else:
                smoke=json.loads(a.http.read_text(encoding='utf-8'))
                assert smoke['passed'] and smoke['temporary_user_removed'] and report.get('activated')
                for s in report['old_legal_schemas']:
                    assert s!=SCHEMA and re.fullmatch(r'legal_[a-z0-9_]+',s)
                    c.execute(text(f'DROP SCHEMA IF EXISTS {s} CASCADE'))
                c.execute(text('DELETE FROM public.legal_documents'))
                graphs=list(c.execute(text("SELECT nspname FROM pg_namespace WHERE nspname ~ '^graph_rag_[a-z0-9_]+$' AND nspname<>:new"),{'new':settings.chatbot_graph_schema}).scalars())
                for s in graphs: c.execute(text(f'DROP SCHEMA {s} CASCADE'))
                report['removed_legal_schemas']=report['old_legal_schemas'];report['removed_graph_schemas']=graphs
                report['old_indexes_removed']=True
            report.update(protected_after=protected(c),counts=counts,active_legal_schema=SCHEMA,ocr_documents=0)
    REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False),flush=True);engine.dispose()

if __name__=='__main__': main()
