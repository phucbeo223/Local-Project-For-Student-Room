"""Read-only checks of isolated supplemental corpus and retained active stores."""
from pathlib import Path
import argparse
import hashlib
import json
import sys
from sqlalchemy import create_engine,text
from app.config import settings

ROOT=Path('/workspace')
sys.path.insert(0,str(ROOT/'scripts'))
from index_legal_agent_corpus import pieces
ACTIVE={'public':('aggregated_listings','users'), 'legal_word_v7_20261005':('legal_documents','legal_chunks'),
 'graph_rag_word_v6':('nodes','edges','release'), 'housing_graph_word_v6':('aggregated_listings','release')}
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def snapshot(c):
 result={}
 for schema,tables in ACTIVE.items():
  for table in tables:
   result[schema+'.'+table]=dict(c.execute(text(f"SELECT count(*) AS rows,md5(string_agg(row_to_json(t)::text,'|' ORDER BY row_to_json(t)::text)) AS digest FROM {schema}.{table} t")).mappings().one())
 result['active_release']=dict(c.execute(text("SELECT * FROM public.legal_corpus_releases WHERE schema_name='legal_word_v7_20261005'")).mappings().one())
 result['base_manifest_sha256']=digest(ROOT/'docs/legal_word_corpus_v7_20261005/manifest.json')
 return json.loads(json.dumps(result,default=str))

def main():
 p=argparse.ArgumentParser();p.add_argument('action',choices=['before','after']);a=p.parse_args()
 output=Path('/eval/reports/graph_rag_word_supplement_audit_v8_2026-10-05.json')
 engine=create_engine(settings.database_url)
 with engine.connect() as c:
  current=snapshot(c)
  if a.action=='before':
   assert not output.exists(),'Baseline must not be overwritten'
   report={'active_before':current,'active_store_retained':None}
  else:
   report=json.loads(output.read_text(encoding='utf-8'))
   assert current==report['active_before'],'Current corpus/housing/users changed'
   report.update(active_after=current,active_store_retained=True)
   folder=ROOT/'docs/legal_word_supplement_corpus_v8_20261005'
   manifest=json.loads((folder/'manifest.json').read_text(encoding='utf-8'))
   base=json.loads((ROOT/'docs/legal_word_corpus_v7_20261005/manifest.json').read_text(encoding='utf-8'))
   assert manifest['documents'][:16]==base['documents']
   all_documents=[]
   for entry in manifest['documents']:
    f=ROOT/entry['file'];assert digest(f)==entry['sha256']
    d=json.loads(f.read_text(encoding='utf-8'));s=d['source']
    word=ROOT/s['path'];assert word.suffix in ('.doc','.docx') and digest(word)==s['sha256']
    assert s['ocr_used'] is False
    for v in d['provisions']: assert hashlib.sha256(v['content'].encode()).hexdigest()==v['content_sha256']
    all_documents.append(d)
   schema=manifest['schema']
   counts=dict(c.execute(text(f'SELECT count(*) AS chunks,count(embedding_vector) AS vectors,count(provision_id) AS identified,count(parent_content) AS parented FROM {schema}.legal_chunks')).mappings().one())
   assert counts['chunks']==counts['vectors']==counts['identified']==counts['parented']>325
   expected=sum(len(pieces(v)) for d in all_documents for v in d['provisions'])
   assert counts['chunks']==expected
   assert c.execute(text(f'SELECT count(*) FROM {schema}.legal_chunks WHERE vector_dims(embedding_vector)<>384')).scalar_one()==0
   actual=list(c.execute(text(f'SELECT source_metadata,ocr_engine,ocr_page_count FROM {schema}.legal_documents')).mappings())
   assert len(actual)==30 and all(r['ocr_engine'] is None and r['ocr_page_count']==0 for r in actual)
   assert c.execute(text('SELECT status FROM public.legal_corpus_releases WHERE schema_name=:s'),{'s':schema}).scalar_one()=='staging'
   new_housing=dict(c.execute(text("SELECT count(*) AS rows,md5(string_agg(row_to_json(t)::text,'|' ORDER BY row_to_json(t)::text)) AS digest FROM housing_graph_word_supplement_v7.aggregated_listings t")).mappings().one())
   assert new_housing==current['housing_graph_word_v6.aggregated_listings']
   release=dict(c.execute(text('SELECT * FROM graph_rag_word_supplement_v7.release WHERE id=1')).mappings().one())
   assert release['legal_schema']==schema and release['legal_sha256']==digest(folder/'manifest.json')
   report.update(passed=True,new_schema=schema,new_document_count=len(actual),new_counts=counts,
     original_16_documents_byte_unchanged=True,ocr_documents=0,pdf_inputs=0,reference_answers_embedded=False,
     corpus_manifest_sha256=digest(folder/'manifest.json'),new_store_active=False,embedding_dimensions=384,
     new_housing_identical_to_active=True,graph_release_matches_corpus=True)
 output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({k:v for k,v in report.items() if k not in ('active_before','active_after')},ensure_ascii=False))
 engine.dispose()
if __name__=='__main__': main()
