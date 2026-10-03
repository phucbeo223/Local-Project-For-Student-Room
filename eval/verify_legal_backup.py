"""Compare restored legal tables to their originals; never inspect authentication data."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
from sqlalchemy import create_engine,text
from sqlalchemy.engine import make_url
from app.config import settings

RESTORED='legal_backup_verify_20261003_1410'
original=create_engine(settings.database_url)
copy=create_engine(make_url(settings.database_url).set(database=RESTORED))


def snapshot(engine):
    result={}
    with engine.connect() as conn:
        for table in ('legal_documents','legal_chunks'):
            result[table]=dict(conn.execute(text(f'SELECT count(*) AS rows,md5(string_agg(row_to_json(t)::text,\'|\' ORDER BY id)) AS digest FROM public.{table} t')).mappings().one())
    return result


before,after=snapshot(original),snapshot(copy)
assert before==after,'Restored backup differs from original legal tables'
path=Path('/workspace/backups/legal_agent_rebuild_20261003/old_legal.dump')
report={'verified_at_utc':datetime.now(timezone.utc).isoformat(),'restored_database':RESTORED,
        'backup_path':'backups/legal_agent_rebuild_20261003/old_legal.dump',
        'backup_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'original':before,'restored':after,'restore_verified':True}
Path('/eval/reports/legal_agent_backup_2026-10-03.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report),flush=True)
original.dispose();copy.dispose()
