"""Rebuild a source-only corpus; evaluation references are never read here."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, re, sys
from urllib.parse import urljoin, urlparse
import httpx
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'apps/api'))
from app.room_service.legal_knowledge.provisions import structure_provisions, provision_json
from app.room_service.legal_knowledge.extractor import extract_document
from prepare_legal_agent_corpus import join_pages
OUT = ROOT/'docs/legal_corpus_v5_20261004'
RAW = ROOT/'docs/source_grounded_originals_20261004'

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def read(path): return json.loads(path.read_text(encoding='utf-8'))
def primary(url):
    host = urlparse(url).hostname or ''
    return urlparse(url).scheme == 'https' and any(host == domain or host.endswith('.'+domain) for domain in ('gov.vn','ctu.edu.vn','chinhphu.vn','cdnchinhphu.vn','capnuoccantho2.com.vn'))

def main():
    OUT.mkdir(parents=True, exist_ok=True); RAW.mkdir(parents=True, exist_ok=True)
    documents, excluded, downloads = {}, [], []
    baseline = read(ROOT/'docs/legal_corpus_v3_20261004/manifest.json')
    for entry in baseline['documents']:
        path = ROOT/entry['file']; assert sha(path) == entry['sha256']
        data = read(path); src = data['source']
        if src.get('page_kind') == 'editorial_guidance' or entry['id'].startswith('legacy-'):
            excluded.append({'id':entry['id'], 'reason':'Project editorial/selected local derivative removed; original-only replacements below.'})
            continue
        original = ROOT/src['path']
        assert original.is_file() and sha(original) == src['sha256'], entry['id']
        assert primary(src['source_url']), entry['id']
        src['original_sha256'] = src['sha256']
        src['source_policy'] = 'Published original or explicitly reviewed literal excerpt; no project-authored guidance.'
        for part in data['provisions']:
            assert hashlib.sha256(part['content'].encode()).hexdigest() == part['content_sha256']
        documents[entry['id']] = data

    def structured(key, source, pages, selected=None):
        if isinstance(pages,dict):pages=pages['pages']
        if pages and isinstance(pages[0],str):pages=[{'page':i+1,'text':p} for i,p in enumerate(pages)]
        body, spans = join_pages(pages)
        parts = structure_provisions(body, source['sha256'])
        if selected is not None: parts = [p for p in parts if p.article in {str(n) for n in selected}]
        assert parts, key
        provisions = []
        for part in parts:
            data = provision_json(part)
            assert part.content in body
            relevant = [p for start,end,p in spans if start < part.source_end and end > part.source_start]
            data.update(page_from=min(relevant), page_to=max(relevant), extraction_text_sha256=hashlib.sha256(body.encode()).hexdigest())
            provisions.append(data)
        source.update(id=key, page_kind=source.get('page_kind','physical_pdf'), pages=max(p['page'] for p in pages),
                      source_policy='Literal original text/OCR; article/clause parsing only, no generated legal content.',
                      original_sha256=source['sha256'], not_exhaustive=selected is not None)
        documents[key] = {'source':source, 'provisions':provisions}

    old = {r['id']:r for r in read(ROOT/'docs/legal_sources_originals_20261003/download_manifest.json')['sources']}
    housing = next(r for r in read(ROOT/'docs/legal_web_supplement_20261004/sources.json')['sources'] if r['id']=='housing79')
    old['housing79']={'id':'housing79','path':'docs/legal_web_supplement_20261004/originals/housing79.pdf',
                      'sha256':housing['original_sha256'],'source_page_url':housing['url']}
    specifications = [
        ('civil91first','housing_contract','Bộ luật Dân sự 91/2015/QH13 — phần đầu bản ký',[117,119,328,*range(351,362)]),
        ('civil91','housing_contract','Bộ luật Dân sự 91/2015/QH13 — phần tiếp theo bản ký',list(range(472,483))),
        ('housing79','housing_contract','Văn bản hợp nhất 79/VBHN-VPQH — Luật Nhà ở',list(range(160,177))),
        ('fire55','fire_safety','Luật Phòng cháy chữa cháy và cứu nạn cứu hộ 55/2024/QH15',[8,20,21,23,24]),
        ('broker29','real_estate_brokerage','Luật Kinh doanh bất động sản 29/2023/QH15',[46,61,62,63,64,65,66]),
        ('residence68','residence','Luật Cư trú 68/2020/QH14',[7,8,9,27,28]),
    ]
    for key,cat,title,articles in specifications:
        raw = old[key]; original=ROOT/raw['path']; assert sha(original)==raw['sha256']
        pages_path=ROOT/('docs/legal_web_supplement_20261004/extracted/housing79.pages.json' if key=='housing79'
                        else f'eval/source_supplement_20261003/{key}.pages.json')
        source=dict(raw,category=cat,title=title,source_url=raw['source_page_url'],extraction='Published PDF page text/OCR, reproducible stored page input',
                    page_input=pages_path.relative_to(ROOT).as_posix(),page_input_sha256=sha(pages_path),
                    verification='Original hash/provenance checked; OCR may contain errors; no blanket current-effectiveness claim.')
        structured(key,source,read(pages_path),articles)
        if key=='civil91first':
            found={part['article'] for part in documents[key]['provisions']}
            assert {'117','119','328'} <= found, ('Missing essential civil articles',found)

    # Original official warnings: strip the project-created headings/labels.
    for key,cat in [('rental_warning','criminal_law'),('online_warning','ecommerce_platform')]:
        raw=old[key]; path=ROOT/raw['path']; assert sha(path)==raw['sha256']
        soup=BeautifulSoup(path.read_text(encoding='utf-8'),'html.parser')
        paragraphs=[p.get_text(' ',strip=True) for p in soup.select('p')]
        matches=[p for p in paragraphs if len(p)>80 and any(t in p.lower() for t in ('khuyến cáo','chuyển tiền','lưu giữ','trình báo','đặt cọc'))]
        matches=list(dict.fromkeys(matches)); assert matches, key
        source=dict(raw,id=key,category=cat,title=soup.title.get_text(' ',strip=True),source_url=raw['source_page_url'],
                    pages=1,page_kind='web_excerpt',extraction='Literal complete native HTML paragraphs',verification='Paragraphs copied from hash-verified original HTML')
        documents[key]={'source':source,'provisions':[unit(key,i,p,'Khuyến cáo công khai',1) for i,p in enumerate(matches)]}

    for key,title,articles in [('procedure17','Văn bản hợp nhất 17/VBHN-VPQH — Bộ luật Tố tụng hình sự',[30,31,32,33,144,145,146,147]),
                               ('criminal135','Văn bản hợp nhất 135/VBHN-VPQH — Bộ luật Hình sự',[174,175])]:
        metadata=read(RAW/(key+'.download.json'))
        origins=metadata if isinstance(metadata,list) else [metadata]
        pages=[]
        for origin in origins:
            path=ROOT/origin['path'];assert sha(path)==origin['sha256'] and primary(origin['source_url']) and primary(origin['download_url'])
            doc=extract_document(path,path.parent)
            for page in doc.pages:pages.append({'page':len(pages)+1,'text':page.text})
        source=dict(origins[0],id=key,title=title,category='criminal_law',origin_documents=origins,
                    page_kind='logical_document',extraction='Native official DOC/DOCX text; complete downloaded parts; whitespace/layout only',
                    verification='TLS-verified download via Windows, original hashes retained; no project-authored paragraphs')
        structured(key,source,pages,articles)
        downloads.extend(origins)
        print('source',key,len(documents[key]['provisions']),flush=True)
    new=[
        ('ctu-2026-registration','https://ssc.ctu.edu.vn/thong-bao/226-dang-ky-o-ky-tuc-xa-hoc-ky-1-nam-hoc-2026-2027.html','student_housing'),
        ('ctu-new-students','https://tansinhvien.ctu.edu.vn/sinh-hoat/huong-dan-tan-sinh-vien-dang-ky-o-ky-tuc-xa','student_housing'),
        ('ctu-ktx-rules','https://ssc.ctu.edu.vn/images/upload/Noiquy_KTX_trich_092025.pdf','student_housing'),
    ]
    with httpx.Client(timeout=90,follow_redirects=True) as client:
        for key,url,cat in new:
            assert primary(url)
            response=client.get(url); response.raise_for_status(); assert primary(str(response.url))
            payload=response.content; resolved=str(response.url)
            if payload[:4]!=b'%PDF' and key in ('procedure17','criminal135'):
                soup=BeautifulSoup(response.text,'html.parser')
                attachments=[urljoin(resolved,a['href']) for a in soup.select('a[href]') if '.pdf' in a.get('href','').lower()]
                assert attachments
                attachment=next((u for u in attachments if 'download' in u),attachments[0])
                assert primary(attachment)
                response=client.get(attachment);response.raise_for_status();payload=response.content;resolved=str(response.url)
            suffix='.pdf' if payload[:4]==b'%PDF' else '.html'
            path=RAW/(key+suffix);path.write_bytes(payload)
            info={'id':key,'source_url':url,'resolved_url':resolved,'path':path.relative_to(ROOT).as_posix(),'sha256':sha(path),
                  'retrieved_at_utc':datetime.now(timezone.utc).isoformat(),'http_status':response.status_code,'bytes':len(payload)}
            downloads.append(info)
            source=dict(info,category=cat,verification='Primary publisher original; text extraction, no authored answers')
            if suffix=='.pdf':
                extracted=extract_document(path,path.parent)
                pages=[{'page':p.number,'text':p.text} for p in extracted.pages]
                (RAW/(key+'.pages.json')).write_text(json.dumps(pages,ensure_ascii=False,indent=2),encoding='utf-8')
                if key in ('criminal135','procedure17'):
                    structured(key,dict(source,title='Văn bản hợp nhất '+('135/VBHN-VPQH — Bộ luật Hình sự' if key=='criminal135' else '17/VBHN-VPQH — Bộ luật Tố tụng hình sự'),extraction='PDF text/OCR'),pages,[174,175] if key=='criminal135' else [30,31,32,33,144,145,146,147])
                else:
                    structured(key,dict(source,title='Nội quy Ký túc xá Đại học Cần Thơ — bản trích công bố 09/2025',extraction='Native PDF text'),pages,list(range(1,10)))
            else:
                soup=BeautifulSoup(payload,'html.parser')
                for node in soup.select('script,style,nav,header,footer'):node.decompose()
                content=soup.select_one('.item-page') or soup.select_one('article')
                assert content is not None,key
                for node in content.select('.article-info,.item-page-title,.actions,.pagenav'):node.decompose()
                body=content.get_text('\n',strip=True)
                assert len(body)>200,key
                # Preserve all source wording including deadlines/conditions; bounded paragraph groups.
                groups=[];current=[];size=0
                for line in body.splitlines():
                    if size+len(line)>2200 and current:groups.append('\n'.join(current));current=[];size=0
                    current.append(line);size+=len(line)
                if current:groups.append('\n'.join(current))
                source.update(title=soup.title.get_text(' ',strip=True),pages=1,page_kind='web_excerpt',extraction='Native article HTML text grouped without paraphrase',
                              original_sha256=sha(path),not_exhaustive=False)
                documents[key]={'source':source,'provisions':[unit(key,i,p,'Thông tin KTX công bố bởi CTU',1) for i,p in enumerate(groups)]}
            print('source',key,len(documents[key]['provisions']),flush=True)
    entries=[]
    for key,data in sorted(documents.items()):
        target=OUT/(key+'.json');target.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        entries.append({'id':key,'file':target.relative_to(ROOT).as_posix(),'sha256':sha(target),'category':data['source']['category'],'provisions':len(data['provisions'])})
    manifest={'schema':'legal_v5_20261004','documents':entries,'excluded':excluded,'new_downloads':downloads,
              'policy':'Original-only corpus, source URL/hash/page trace; references never read or indexed; OCR and current-effectiveness limits retained.'}
    (OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'documents':len(entries),'provisions':sum(e['provisions'] for e in entries),'excluded':len(excluded)}),flush=True)

def unit(key,index,content,heading,page):
    digest=hashlib.sha256(content.encode()).hexdigest()
    return {'provision_id':key+':'+digest[:20], 'article':None,'clause':None,'heading':heading,'content':content,
            'content_sha256':digest,'page_from':page,'page_to':page,'kind':'official_information',
            'points':[],'exceptions':[],'cross_references':[],'article_context':'','source_start':None,'source_end':None}

if __name__=='__main__':main()
