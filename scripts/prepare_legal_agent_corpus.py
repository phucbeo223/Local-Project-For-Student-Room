"""Create a separate, auditable clause corpus. Never overwrite Data or invent law."""
from pathlib import Path
import hashlib
import json
import re
import sys
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'apps/api'))
from app.room_service.legal_knowledge.extractor import extract_document
from app.room_service.legal_knowledge.provisions import structure_provisions, provision_json

OUT = ROOT/'docs/legal_corpus_v2'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def join_pages(pages):
    """Only remove standalone physical page numbers. Keep source wording and line wraps."""
    parts, spans, pos = [], [], 0
    for page in pages:
        text = re.sub(r'(?m)^\s*\d{1,3}\s*$', '', page['text'])
        # Scan margin bars are layout marks, never clause numbers or legal words.
        text = re.sub(r'(?m)^[ \t]*[|_#]+[ \t]*(?=Điều\s+\d+[.]|\d+[.]\s|[a-zđ][)]\s)','',text)
        text = text.strip()+'\n\n'
        spans.append((pos, pos+len(text), page['page']))
        parts.append(text)
        pos += len(text)
    return ''.join(parts), spans


def build(source, pages, selected=None, advisory=False):
    # Corrections are page-specific and reviewed against images of the signed PDF.
    # Never infer labels, dates, amounts, or legal words from another provision.
    corrections_path = ROOT/'docs/legal_agent_originals_20261003/verified_ocr_corrections.json'
    corrections = json.loads(corrections_path.read_text(encoding='utf-8')) if corrections_path.exists() else []
    reviewed = [c for c in corrections if c['source_id'] == source['id']]
    pages = [dict(p) for p in pages]
    for correction in reviewed:
        page = next(p for p in pages if p['page'] == correction['page'])
        if page['text'].count(correction['before']) != 1:
            raise ValueError('Reviewed OCR correction no longer matches raw page: '+source['id'])
        page['text'] = page['text'].replace(correction['before'], correction['after'])
    if reviewed:
        source = dict(source, reviewed_ocr_corrections=reviewed)
    text, spans = join_pages(pages)
    annex = re.search(r'(?im)^\s*Phụ lục(?:\s+[IVX\d]+)?\s*$',text)
    if annex:
        text = text[:annex.start()]
    provisions = structure_provisions(text, source['sha256'], advisory=advisory)
    if selected is not None:
        provisions = [p for p in provisions if p.article in {str(n) for n in selected}]
    if not provisions:
        raise ValueError('No legal provisions: '+source['id'])
    records = []
    for p in provisions:
        value = provision_json(p)
        nums = [n for a,b,n in spans if a<p.source_end and b>p.source_start]
        value.update(page_from=min(nums), page_to=max(nums))
        records.append(value)
    result = {'source':source, 'provisions':records}
    target = OUT/(source['id']+'.json')
    target.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return {'file':target.relative_to(ROOT).as_posix(), 'sha256':sha(target),
            'id':source['id'], 'category':source['category'], 'provisions':len(records),
            'articles':list(dict.fromkeys(r['article'] for r in records))}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    inventory = json.loads((ROOT/'eval/reports/legal_rebuild_inventory_2026-10-03.json').read_text(encoding='utf-8'))
    prepared = json.loads((ROOT/'docs/legal_sources_originals_20261003/prepared_manifest.json').read_text(encoding='utf-8'))
    originals = json.loads((ROOT/'docs/legal_sources_originals_20261003/download_manifest.json').read_text(encoding='utf-8'))
    by_id = {s['id']:s for s in originals['sources']}
    prep_by_path = {s['path']:s for s in prepared['sources']}
    entries, excluded = [], []
    for row in inventory:
        relative = row['path']
        if 'BẢN TRÍCH TUYỂN NGHIÊN CỨU' in row['prefix'] or relative.endswith('215-QD-UBND-pham-vi-doi-chieu.md'):
            excluded.append({'path':relative,'reason':'editorial summary; replace with original source or quarantine'})
            continue
        if relative.startswith('water_cantho/'):
            excluded.append({'path':relative,'reason':'original government attachment not yet authenticated; do not claim current tariff'})
            continue
        path = ROOT/'Data'/relative
        doc = extract_document(path, ROOT/'Data')
        origins = []
        if relative in prep_by_path:
            origins = [by_id[k] for k in prep_by_path[relative]['origin']]
        urls = row['urls']+[s.get('source_page_url') for s in origins]
        urls = [u for u in urls if u and (urlparse(u).hostname or '').endswith('.gov.vn') or u and (urlparse(u).hostname or '').endswith('.chinhphu.vn')]
        if not urls:
            excluded.append({'path':relative,'reason':'missing government provenance'})
            continue
        key = 'legacy-'+hashlib.sha256(relative.encode()).hexdigest()[:12]
        source = {'id':key,'title':doc.title,'category':doc.category,'path':'Data/'+relative,
                  'sha256':sha(path),'source_url':urls[0], 'origin_documents':origins,
                  'extraction':'existing selected text; editorial header excluded by article parser',
                  'verification':prep_by_path.get(relative,{}).get('notes', 'not verified word by word against full government original'),
                  'page_kind':'physical_pdf' if path.suffix=='.pdf' else 'logical_document',
                  'not_exhaustive':True}
        entries.append(build(source,[{'page':p.number,'text':p.text} for p in doc.pages],advisory='warning-' in relative))
    new = json.loads((ROOT/'docs/legal_agent_originals_20261003/manifest.json').read_text(encoding='utf-8'))
    selection = {
        'electricity133':('electricity','Nghị định 133/2026/NĐ-CP',[1,2,4,13,30,31]),
        'electricity14':('electricity','Quyết định 14/2025/QĐ-TTg',None),
        'fire106':('fire_safety','Nghị định 106/2025/NĐ-CP',[1,2,3,4,11,12,13,20,21,22,23,24,25,39,40]),
        'residence154':('residence','Nghị định 154/2024/NĐ-CP',[1,2,5,6,7,16,17]),
        'amend58':('residence','Nghị định 58/2026/NĐ-CP',[4,6]),
        'residence116':('residence','Thông tư 116/2026/TT-BCA',[1,2,3,6,12,13,14,15,27]),
        'ecommerce122':('ecommerce_platform','Luật Thương mại điện tử 122/2025/QH15',[1,2,3,4,5,15,16,17,18,19,20,40]),
        'ecommerce248':('ecommerce_platform','Nghị định 248/2026/NĐ-CP',[1,2,3,4,7,17,18,19,20,52]),
    }
    for raw in new['sources']:
        category,title,articles = selection[raw['id']]
        assert sha(ROOT/raw['path']) == raw['sha256']
        pages = json.loads((ROOT/'eval/agent_source_ocr'/(raw['id']+'.json')).read_text(encoding='utf-8'))
        if raw['id']=='residence116':
            pages = [p for p in pages if p['page']<=18] # forms start at physical page 19
        source = dict(raw,category=category,title=title,extraction='Tesseract vie+eng from signed government PDF; no automatic legal-word correction',
                      page_kind='physical_pdf',not_exhaustive=True,verification='OCR; selected critical pages visually checked, other text requires review')
        entries.append(build(source,pages,articles))
    # Keep literal amendments as their own source; never label a derived consolidation official.
    for key, category, title, selection in [('residence68','residence','Luật Cư trú 68/2020/QH14',[27]),
                                           ('amend118','residence','Luật 118/2025/QH15',[4,10,11]),
                                           ('amend347','residence','Nghị định 347/2026/NĐ-CP',[17,18,19,29,30,32,33,35,41])]:
        raw = by_id[key]
        pages = json.loads((ROOT/'eval/source_supplement_20261003'/(key+'.pages.json')).read_text(encoding='utf-8'))
        source = dict(raw,id=key,category=category,title=title,source_url=raw['source_page_url'],
                      extraction='government PDF text/OCR',page_kind='physical_pdf',not_exhaustive=True,
                      verification='OCR/raw text; not all words visually reviewed')
        entries.append(build(source,pages,selection))
    water = json.loads((ROOT/'docs/legal_agent_originals_20261003/water_manifest.json').read_text(encoding='utf-8'))
    for raw in water['sources']:
        path=ROOT/raw['path']
        assert sha(path)==raw['sha256']
        if raw['id']=='water57':
            excluded.append({'path':raw['path'],'reason':'downloaded consolidated guidance; section parser not yet reviewed, not indexed as an article'})
            continue
        doc=extract_document(path,path.parent)
        source=dict(raw,category='water_cantho',title='Nghị định '+('117/2007/NĐ-CP' if raw['id']=='water117' else '124/2011/NĐ-CP'),
                    extraction='antiword from government original',page_kind='logical_document',not_exhaustive=True,
                    verification='original attachment; no OCR; supply-contract parties distinct from landlord/tenant')
        selection=[1,2,44,48,49,50,54,56,57,58,65,66] if raw['id']=='water117' else [1,2,3]
        entries.append(build(source,[{'page':p.number,'text':p.text} for p in doc.pages],selection))
    manifest = {'schema':'legal_v2','documents':entries,'excluded':excluded,
                'policy':'Verbatim source clauses and full points; annotations separate. No current tariff inference. No LLM-created legislation.'}
    (OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'documents':len(entries),'provisions':sum(e['provisions'] for e in entries),'excluded':len(excluded)},ensure_ascii=False),flush=True)


if __name__ == '__main__':
    main()
