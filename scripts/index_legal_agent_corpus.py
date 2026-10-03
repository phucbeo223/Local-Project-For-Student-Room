"""Fresh embeddings for structured legal_v2; audit that public/listings stay intact."""
from pathlib import Path
import hashlib
import json
import sys
from sqlalchemy import create_engine, text

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'apps/api'))
from app.config import settings
from app.room_service.chatbot.providers import E5EmbeddingProvider
from app.room_service.legal_knowledge.repo import LegalKnowledgeRepository
from app.room_service.legal_knowledge.extractor import ExtractedDocument, ExtractedPage
from app.room_service.legal_knowledge.chunker import LegalChunk


def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot(conn):
    return dict(conn.execute(text('SELECT (SELECT count(*) FROM public.legal_documents) AS old_documents, '
        '(SELECT count(*) FROM public.legal_chunks) AS old_chunks, '
        '(SELECT count(embedding_vector) FROM public.legal_chunks) AS old_vectors, '
        '(SELECT count(*) FROM aggregated_listings) AS listings, '
        '(SELECT count(embedding_vector) FROM aggregated_listings) AS listing_vectors')).mappings().one())


def pieces(value, maximum=1200):
    """Bound E5 input; retain the complete clause as parent, including exceptions."""
    content = value['content']
    if len(content)<=maximum: return [content]
    result, current = [], ''
    for line in content.splitlines(keepends=True):
        if len(current)+len(line)>maximum and current:
            result.append(current.strip()); current=''
        if len(line)>maximum:
            # Physical OCR lines are short; unwrapped DOCX paragraphs can be long.
            for offset in range(0,len(line),maximum):
                if current: result.append(current.strip()); current=''
                result.append(line[offset:offset+maximum].strip())
        else: current+=line
    if current.strip(): result.append(current.strip())
    return result


def main():
    engine = create_engine(settings.database_url,pool_pre_ping=True)
    corpus = ROOT/'docs/legal_corpus_v2'
    manifest = json.loads((corpus/'manifest.json').read_text(encoding='utf-8'))
    with engine.begin() as conn:
        before=snapshot(conn)
        conn.exec_driver_sql((ROOT/'infra/db/migrations/101_isolated_legal_corpus.sql').read_text(encoding='utf-8'))
    repo=LegalKnowledgeRepository(engine,'legal_v2')
    embedder=E5EmbeddingProvider(settings.chatbot_embedding_model)
    embedder.warmup()
    indexed=[]
    for entry in manifest['documents']:
        path=ROOT/entry['file']
        assert sha(path)==entry['sha256']
        data=json.loads(path.read_text(encoding='utf-8'))
        source=data['source']
        if repo.current_hash(entry['file'])==entry['sha256']:
            print('unchanged',source['id'],flush=True); continue
        parents, chunks=[],[]
        for provision in data['provisions']:
            for content in pieces(provision):
                chunks.append(LegalChunk(len(chunks),provision['page_from'],provision['page_to'],provision['heading'],
                                         content,hashlib.sha256(content.encode()).hexdigest()))
                parents.append(provision)
        vectors=[]
        for start in range(0,len(chunks),24):
            # Title and clause label matter for numbered legal retrieval; body remains exact.
            vectors.extend(embedder.embed_passages([source['title']+'\n'+(c.heading or '')+'\n'+c.content for c in chunks[start:start+24]]))
        assert len(vectors)==len(chunks) and all(len(v)==384 for v in vectors)
        doc=ExtractedDocument(path,entry['file'],source['title'],source['category'],'structured_json','application/json',
                              entry['sha256'],tuple(ExtractedPage(n,'',source.get('page_kind')=='physical_pdf')
                              for n in range(1,source.get('pages',1)+1)), 'tesseract' if 'OCR' in source['extraction'] else None)
        doc_id=repo.replace_document(doc,chunks,vectors,settings.chatbot_embedding_model)
        with engine.begin() as conn:
            conn.execute(text('UPDATE legal_v2.legal_documents SET source_metadata=CAST(:meta AS jsonb) WHERE id=:id'),
                         {'id':doc_id,'meta':json.dumps(source,ensure_ascii=False)})
            for index,parent in enumerate(parents):
                meta={k:v for k,v in parent.items() if k!='content'}
                complete_parent = ((parent.get('article_context')+'\n\n') if parent.get('article_context') else '')+parent['content']
                conn.execute(text('UPDATE legal_v2.legal_chunks SET provision_id=:pid,parent_content=:parent,'
                    'source_metadata=CAST(:meta AS jsonb) WHERE document_id=:id AND chunk_index=:index'),
                    {'id':doc_id,'index':index,'pid':parent['provision_id'],'parent':complete_parent,'meta':json.dumps(meta,ensure_ascii=False)})
        indexed.append({'id':source['id'],'chunks':len(chunks),'provisions':len(data['provisions'])})
        print('indexed',source['id'],len(chunks),flush=True)
    with engine.begin() as conn:
        after=snapshot(conn)
        assert after==before, 'The original corpus or listings changed during isolated rebuild'
        counts=dict(conn.execute(text('SELECT count(*) AS chunks,count(embedding_vector) AS vectors,'
            'count(provision_id) AS identified,count(parent_content) AS parented FROM legal_v2.legal_chunks')).mappings().one())
        assert counts['chunks']==counts['vectors']==counts['identified']==counts['parented']>0
        conn.execute(text('UPDATE public.legal_corpus_releases SET manifest_sha256=:sha WHERE schema_name=\'legal_v2\''),
                     {'sha':sha(corpus/'manifest.json')})
    report={'schema':'legal_v2','original_before':before,'original_after':after,'counts':counts,'indexed':indexed,
            'manifest_sha256':sha(corpus/'manifest.json'),'activation':'not activated; evaluation pending'}
    (ROOT/'eval/reports/legal_agent_index_2026-10-03.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False),flush=True)
    engine.dispose()


if __name__=='__main__': main()
