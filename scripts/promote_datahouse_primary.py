"""Replace obsolete public rental rows only after a restorable backup and fresh index."""
import argparse, hashlib, json
from pathlib import Path
from datetime import datetime, timezone
from sqlalchemy import create_engine, text
from app.config import settings
from app.room_service.chatbot.graph_retrieval import graph_schema
from app.room_service.legal_knowledge.storage import legal_schema
import re
from sqlalchemy.engine import make_url
import redis

ROOT=Path(__file__).resolve().parents[1]
BACKUP=ROOT/'backups/source_grounded_20261004/before_refresh.dump'
REPORT=ROOT/'eval/reports/graph_rag_primary_v4_2026-10-04.json'
RELATED=('user_interactions','reports','chat_message_sources','risk_assessment_history','listing_favorites','user_notifications','listing_image_hashes','listing_reviews')
def snap(c,schema='public'):
    return dict(c.execute(text(f"SELECT count(*) AS rows,count(embedding_vector) AS vectors,md5(string_agg(row_to_json(t)::text,'|' ORDER BY id)) AS digest FROM {schema}.aggregated_listings t")).mappings().one())
def projection(c):
    return dict(c.execute(text("SELECT count(*) AS rows,count(embedding_vector) AS vectors,md5(string_agg(id::text||coalesce(content_hash,'')||coalesce(embedding_vector::text,''),'|' ORDER BY id)) AS digest FROM public.aggregated_listings")).mappings().one())
def related(c):
    return {table:c.execute(text(f'SELECT count(*) FROM public.{table} WHERE listing_id IS NOT NULL')).scalar_one() for table in RELATED}
def main():
    global BACKUP,REPORT
    p=argparse.ArgumentParser();p.add_argument('action',choices=('verify','promote','retire'))
    p.add_argument('--backup',type=Path,default=BACKUP);p.add_argument('--report',type=Path,default=REPORT)
    p.add_argument('--housing-http',type=Path,default=ROOT/'eval/reports/graph_rag_http_v5_2026-10-04.json')
    a=p.parse_args();BACKUP,REPORT=a.backup,a.report
    listing=settings.chatbot_listing_schema;graph=graph_schema(settings.chatbot_graph_schema);legal=legal_schema(settings.chatbot_legal_schema)
    assert re.fullmatch(r'housing_graph_[a-z0-9_]+',listing) and legal!='public'
    engine=create_engine(settings.database_url)
    if a.action=='verify':
        restored=create_engine(make_url(settings.database_url).set(database='nckh_verify_source_v4'))
        with engine.connect() as c,restored.connect() as r:
            assert snap(c)==snap(r) and related(c)==related(r)
            users=dict(c.execute(text("SELECT count(*) AS rows,md5(string_agg(row_to_json(t)::text,'|' ORDER BY id)) AS digest FROM public.users t")).mappings().one())
            report={'backup_restore_verified':True,'backup_sha256':hashlib.sha256(BACKUP.read_bytes()).hexdigest(),
                    'public_before':snap(c),'dependent_before':related(c),'users_before':users}
        restored.dispose()
    else:
        report=json.loads(REPORT.read_text(encoding='utf-8'))
        assert report['backup_restore_verified'] and report['backup_sha256']==hashlib.sha256(BACKUP.read_bytes()).hexdigest()
        with engine.begin() as c:
            if a.action=='promote':
                c.execute(text('LOCK TABLE public.aggregated_listings IN ACCESS EXCLUSIVE MODE'))
                assert snap(c)==report['public_before'],'Old rental data changed after backup verification'
                assert snap(c,listing)['rows']==snap(c,listing)['vectors']==789
                assert c.execute(text(f"SELECT count(*) FROM {listing}.aggregated_listings WHERE source <> 'chotot'")).scalar_one()==0
                c.execute(text('DELETE FROM public.aggregated_listings'))
                c.execute(text(f'INSERT INTO public.aggregated_listings SELECT * FROM {listing}.aggregated_listings'))
                c.execute(text("SELECT setval(pg_get_serial_sequence('public.aggregated_listings','id'),(SELECT max(id) FROM public.aggregated_listings),true)"))
                assert snap(c)==snap(c,listing)
                users=dict(c.execute(text("SELECT count(*) AS rows,md5(string_agg(row_to_json(t)::text,'|' ORDER BY id)) AS digest FROM public.users t")).mappings().one())
                assert users==report['users_before']
                report.update(promoted=True,public_after=snap(c),public_after_projection=projection(c),dependent_after=related(c),users_after=users,
                              catalog_sha256=c.execute(text(f'SELECT catalog_sha256 FROM {listing}.release WHERE id=1')).scalar_one())
            else:
                smoke=json.loads(a.housing_http.read_text(encoding='utf-8'))
                assert smoke['passed'] and smoke['temporary_user_removed'] and report['promoted']
                assert snap(c)==report['public_after']
                assert snap(c)==snap(c,listing),'Active graph housing differs from primary catalog'
                retired=[s for s in ('graph_rag_v1','housing_graph_v1','housing_v2','graph_rag_v2','housing_graph_v2') if s not in (graph,listing)]
                for schema in retired:
                    c.execute(text(f'DROP SCHEMA IF EXISTS {schema} CASCADE'))
                c.execute(text("UPDATE public.legal_corpus_releases SET status='retired' WHERE schema_name IN ('legal_v3_20261004','legal_v4_20261004') AND schema_name<>:schema"),{'schema':legal})
                c.execute(text("UPDATE public.legal_corpus_releases SET status='active',activated_at=now() WHERE schema_name=:schema"),{'schema':legal})
                report['retired_housing_schemas']=retired
                report['active_schemas']={'graph':graph,'housing':listing,'legal':legal}
                report['retired']=True
        if a.action=='promote':redis.from_url(settings.redis_url).delete('listings:stats:ctu:v1')
    report['updated_at_utc']=datetime.now(timezone.utc).isoformat()
    REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    engine.dispose();print(json.dumps(report,ensure_ascii=False),flush=True)
if __name__=='__main__':main()
