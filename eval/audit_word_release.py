"""Read-only release audit: Word source fidelity, vectors and bounded graph."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from sqlalchemy import create_engine, text
from app.config import settings
from app.room_service.chatbot.graph_retrieval import GraphChatRepository
from app.room_service.chatbot.parser import parse_query
from app.room_service.legal_knowledge.extractor import extract_document
import question_bank_ragas as bank

ROOT=Path('/workspace')
IDS=list(range(19,39))+list(range(43,59))

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    manifest_path=ROOT/'docs/legal_word_corpus_v7_20261005/manifest.json'
    manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
    sources=[]
    for entry in manifest['documents']:
        path=ROOT/entry['file'];assert sha(path)==entry['sha256']
        data=json.loads(path.read_text(encoding='utf-8'));s=data['source'];original=ROOT/s['path']
        assert original.suffix.lower() in ('.doc','.docx') and sha(original)==s['sha256']
        extracted=extract_document(original,ROOT/'Data')
        assert s['ocr_used'] is False and extracted.ocr_engine is None and not any(x.ocr_used for x in extracted.pages)
        body='\n\n'.join(x.text for x in extracted.pages)
        for part in data['provisions']:
            assert all(segment in body for segment in part.get('source_segments',[part['content']]))
            assert sha_content(part['content'])==part['content_sha256']
            assert 'Ghi chú tuyển chọn:' not in part['content']
        sources.append({'id':entry['id'],'path':s['path'],'kind':s['source_content_kind'],
            'sha256':s['sha256'],'provisions':len(data['provisions'])})
    release_audit=json.loads((ROOT/'eval/reports/graph_rag_word_release_v7_2026-10-05.json').read_text())
    engine=create_engine(settings.database_url)
    repo=GraphChatRepository(engine,settings.chatbot_legal_schema,settings.chatbot_listing_schema,settings.chatbot_graph_schema)
    with engine.connect() as c:
        protected={t:dict(c.execute(text(f"SELECT count(*) AS rows,md5(string_agg(row_to_json(t)::text,'|' ORDER BY id)) AS digest FROM public.{t} t")).mappings().one()) for t in ('aggregated_listings','users')}
        assert protected==release_audit['protected_before']
        counts=dict(c.execute(text(f'SELECT count(*) AS chunks,count(embedding_vector) AS vectors,min(vector_dims(embedding_vector)) AS min_dims,max(vector_dims(embedding_vector)) AS max_dims FROM {repo.legal_schema}.legal_chunks')).mappings().one())
        ocr=c.execute(text(f'SELECT count(*) FROM {repo.legal_schema}.legal_documents WHERE ocr_engine IS NOT NULL OR ocr_page_count<>0')).scalar_one()
        old=[s for s in release_audit['old_legal_schemas'] if c.execute(text('SELECT to_regnamespace(:s)'),{'s':s}).scalar()]
        legacy=c.execute(text('SELECT count(*) FROM public.legal_chunks')).scalar_one()
        graph=dict(c.execute(text(f'SELECT * FROM {repo.graph_schema}.release WHERE id=1')).mappings().one())
        assert graph['legal_sha256']==sha(manifest_path)
    cases=[]
    for case in bank.load_questions(Path('/housing_bank.md')):
        if case['id'] not in IDS:continue
        parsed=parse_query(case['question'])
        rows=repo.retrieve_legal(case['question'],None) if parsed.intent=='legal_question' else []
        assert all(row.get('page_kind')=='logical_document' and str(row['source_path']).startswith('docs/legal_word_corpus_v7_20261005/') for row in rows)
        cases.append({'id':case['id'],'intent':parsed.intent,'retrieved_sources':sorted({r.get('source_id') for r in rows}),'retrieved_categories':sorted({r['category'] for r in rows})})
    gates={'word_source_bytes_verified':True,'only_native_word_extraction':True,'literal_word_segments_verified':True,
        'old_indexes_removed':not old and legacy==0,'zero_ocr_metadata':ocr==0,
        'protected_rows_unchanged':True,'complete_real_vectors':counts['chunks']==counts['vectors'] and counts['min_dims']==counts['max_dims']==384,
        'current_graph_matches_word_manifest':True,'all_36_routed_to_basic_legal':len(cases)==36 and all(x['intent']=='legal_question' for x in cases)}
    report={'created_at_utc':datetime.now(timezone.utc).isoformat(),'passed':all(gates.values()),'gates':gates,
        'pipeline_sha256':bank.pipeline_sha256(ROOT/'apps/api/app/room_service/chatbot'),
        'manifest_sha256':sha(manifest_path),'sources':sources,'counts':counts,'protected':protected,
        'graph_schema':repo.graph_schema,'listing_schema':repo.listing_schema,'legal_schema':repo.legal_schema,
        'cases':cases,'provider_calls':0,'scope':'Read-only retrieval audit; not the 36-question generation or reference comparison.'}
    a.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'passed':report['passed'],'gates':gates,'counts':counts,'pipeline_sha256':report['pipeline_sha256']}),flush=True)
    engine.dispose()

def sha_content(value): return hashlib.sha256(value.encode()).hexdigest()

if __name__=='__main__':main()
