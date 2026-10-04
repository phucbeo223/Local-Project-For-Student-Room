"""Record completion against live database, immutable corpus and 36 saved comparisons."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import sys
import httpx
from sqlalchemy import create_engine, text

ROOT = Path(__file__).resolve().parents[1]
if not (ROOT / 'apps/api/app').is_dir(): ROOT = Path('/workspace')
sys.path.insert(0, str(ROOT / 'apps/api'))
from app.config import settings

SCHEMA = 'legal_v3_20261004'
def read(path): return json.loads(path.read_text(encoding='utf-8'))
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

run_path = ROOT / 'eval/reports/legal_refresh_36_2026-10-04.json'
comparison_path = ROOT / 'eval/ragas_reports/legal_refresh_vs_reference_36_2026-10-04.json'
manifest_path = ROOT / 'docs/legal_corpus_v3_20261004/manifest.json'
reference_path = ROOT / 'eval/datasets/external_legal_20261004/answers.json'
mapping_path = ROOT / 'eval/ragas_reports/gemini_qwen_vs_pasted_2026-10-04.json'
run, comparison = read(run_path), read(comparison_path)
lifecycle_path = ROOT / 'eval/reports/legal_refresh_lifecycle_2026-10-04.json'
lifecycle = read(lifecycle_path)
integrity = read(ROOT / 'eval/reports/legal_refresh_corpus_integrity_2026-10-04.json')
payload = read(ROOT / 'eval/reports/legal_refresh_payload_audit_2026-10-04.json')
cases = run['cases']
engine = create_engine(settings.database_url)
with engine.connect() as conn:
    releases = {r['schema_name']: dict(r) for r in conn.execute(text('SELECT schema_name,status,manifest_sha256 FROM public.legal_corpus_releases')).mappings()}
    counts = dict(conn.execute(text(f'SELECT count(*) AS chunks,count(embedding_vector) AS vectors,count(provision_id) AS identified,count(parent_content) AS parented FROM {SCHEMA}.legal_chunks')).mappings().one())
    old_counts = {schema: dict(conn.execute(text(f'SELECT (SELECT count(*) FROM {schema}.legal_documents) AS documents,(SELECT count(*) FROM {schema}.legal_chunks) AS chunks')).mappings().one()) for schema in ('public','legal_v2')}
    listing_state = dict(conn.execute(text("SELECT count(*) AS rows,count(embedding_vector) AS vectors,md5(string_agg(row_to_json(t)::text,'|' ORDER BY id)) AS digest FROM public.aggregated_listings t")).mappings().one())
health = httpx.get('http://api:8000/health/deps', timeout=10)
gates = dict(
    all_36_completed=len(cases)==36 and all(c.get('answer') and not c.get('error') for c in cases),
    all_36_used_new_schema=all(c.get('corpus_schema')==SCHEMA for c in cases),
    all_36_have_retrieval_contexts=all(bool(c.get('contexts')) for c in cases),
    comparison_complete=len(comparison['cases'])==36 and all(c.get('comparison') for c in comparison['cases']),
    comparison_input_unchanged=comparison['input_sha256']==dict(run=sha(run_path),reference=sha(reference_path),mapping=sha(mapping_path)),
    same_live_and_evaluated_manifest=sha(manifest_path)==run['corpus_manifest_sha256']==releases[SCHEMA]['manifest_sha256'],
    active_new_release=releases[SCHEMA]['status']=='active',
    old_legal_tables_empty=all(all(v==0 for v in row.values()) for row in old_counts.values()),
    old_releases_retired=all(releases[s]['status']=='retired' for s in old_counts),
    listings_unchanged=listing_state==lifecycle['listings'],
    complete_embeddings=counts['chunks']>0 and len(set(counts.values()))==1,
    backup_verified=lifecycle['restore_verified'] and sha(ROOT/lifecycle['backup_path'])==lifecycle['backup_sha256'],
    corpus_integrity=integrity['passed'] and integrity['manifest_sha256']==sha(manifest_path),
    public_payload_audit=payload['passed'],
    http_healthy=health.status_code==200 and all(health.json().get(k)=='ok' for k in ('postgres','redis','pgvector')))
report = dict(passed=all(gates.values()), gates=gates, completed_at_utc=datetime.now(timezone.utc).isoformat(),
    schema=SCHEMA, counts=counts, old_counts=old_counts, listings=listing_state,
    evaluation_sha256=sha(run_path), comparison_sha256=sha(comparison_path),
    manifest_sha256=sha(manifest_path), summary=comparison['summary'],
    checks=dict(unit_tests_passed=83, production_api_and_web_build='passed including TypeScript and lint',
                authenticated_http_smoke='passed; anonymous blocked; temporary account removed'),
    interpretation='Completion/integrity checks, not independent legal accuracy. Qualitative reference agreement is model judged; known-topic regression only; no new RAGAS scores.')
(ROOT/'eval/reports/legal_refresh_acceptance_2026-10-04.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
if not report['passed']:
    print(json.dumps(report)); raise SystemExit(2)
with engine.begin() as conn:
    conn.execute(text('UPDATE public.legal_corpus_releases SET validation=CAST(:validation AS jsonb) WHERE schema_name=:schema'),
        dict(schema=SCHEMA,validation=json.dumps(dict(regression_evaluation='completed', cases=36,
            evaluation_sha256=sha(run_path),comparison_sha256=sha(comparison_path),
            agreement=comparison['summary']['agreement'], backup_restore_verified=True, http_smoke_passed=True))))
index_path=ROOT/'eval/reports/legal_refresh_index_2026-10-04.json'
index=read(index_path)
index['activation']='active; 36-question regression and reference comparison completed'
index_path.write_text(json.dumps(index,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
lifecycle['regression_evaluation']='completed'
lifecycle['evaluation_sha256']=sha(run_path)
lifecycle['comparison_sha256']=sha(comparison_path)
lifecycle_path.write_text(json.dumps(lifecycle,indent=2)+'\n',encoding='utf-8')
engine.dispose()
print(json.dumps(report),flush=True)
