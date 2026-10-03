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
from app.room_service.legal_knowledge.provisions import structure_provisions, provision_json, Provision

OUT = ROOT/'docs/legal_corpus_v2'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def join_pages(pages):
    """Only remove standalone physical page numbers. Keep source wording and line wraps."""
    parts, spans, pos = [], [], 0
    for page in pages:
        text = re.sub(r'(?m)^\s*\d{1,3}\s*$', '', page['text'])
        text = re.sub(r'(?m)^[ \t]*CÔNG BÁO/[^\n]*\n?', '', text)
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
    annotations=[]
    for page in pages:
        notes=re.findall(r'(?m)^[ \t]*Ghi chú tuyển chọn:[^\n]*',page['text'])
        annotations.extend({'page':page['page'],'text':note} for note in notes)
        page['text']=re.sub(r'(?m)^[ \t]*Ghi chú tuyển chọn:[^\n]*','',page['text'])
    if annotations:
        source=dict(source,editorial_annotations=annotations,
                    contains_selected_points=any('Chỉ tuyển các điểm' in note['text'] for note in annotations))
    text, spans = join_pages(pages)
    annex = re.search(r'(?im)^[ \t]*Phụ lục(?:[ \t]+[IVX\d]+)?(?:[ \t]*[.:][^\n]*)?[ \t]*$',text)
    if annex:
        text = text[:annex.start()]
    provisions = structure_provisions(text, source['sha256'], advisory=advisory)
    if selected is not None:
        provisions = [p for p in provisions if p.article in {str(n) for n in selected}]
    if source['id']=='water215':
        # OCR tables have not been audited cell by cell. Index the legal basis
        # and duties only; never expose unverified monetary cells as a tariff.
        provisions=[p for p in provisions if p.article!='1' or p.clause is None]
        source=dict(source,tariff_tables_excluded=True,application_verified=False,
            verification='Number/date/title corroborated with government reply; selected clauses transcribed against signed pages 1/3; tables/numeric adjustment limit excluded; current territory/effectiveness requires confirmation')
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
        if relative in ('privacy_data/Luật-91-2025-QH15.docx','privacy_data/Nghị-định-356-2025-NĐ-CP.docx','electricity/Thông-tư-60-2025-TT-BCT.docx'):
            excluded.append({'path':relative,'reason':'replace selected legacy text with full official original downloaded 2026-10-04'})
            continue
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
        overrides_path = ROOT/'docs/legal_fix_originals_20261004/source_url_corrections.json'
        if overrides_path.exists():
            correction = next((c for c in json.loads(overrides_path.read_text(encoding='utf-8'))
                               if c['source_path']=='Data/'+relative), None)
            if correction:
                if source['source_url'] != correction['old_url']:
                    raise ValueError('Source correction does not match legacy input')
                source = dict(source,source_url=correction['new_url'],
                              source_url_correction=correction,
                              origin_documents=origins+correction.get('origin_documents',[]))
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
    fix_root=ROOT/'docs/legal_fix_originals_20261004'
    supplements=json.loads((fix_root/'download_manifest.json').read_text(encoding='utf-8'))
    specifications={
        'privacy91-cb':('privacy_data','Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15',None),
        'privacy356-cb':('privacy_data','Nghị định 356/2025/NĐ-CP',None),
        'electricity60':('electricity','Thông tư 60/2025/TT-BCT',[1,2,3,4,12,20,21]),
        'water50':('water_cantho','Quyết định 50/2026/QĐ-UBND Cần Thơ',None),
        'water215':('water_cantho','Quyết định 215/QĐ-UBND ngày 01/02/2024 Cần Thơ',None),
    }
    for row in supplements['sources']:
        if row['id'] not in specifications or not row.get('attachments'):continue
        raw=next((a for a in row['attachments'] if a['path'].endswith('.doc')),row['attachments'][0])
        assert sha(ROOT/raw['path'])==raw['sha256']
        category,title,articles=specifications[row['id']]
        pages=json.loads((ROOT/'eval/legal_fix_ocr_20261004'/(row['id']+'.json')).read_text(encoding='utf-8'))
        if row['id']=='water215':
            reviewed=json.loads((fix_root/'water215_verified_extract.json').read_text(encoding='utf-8'))
            assert reviewed['original_sha256']==raw['sha256']
            pages=reviewed['pages']
        source=dict(raw,id=row['id'],source_url=row['source_url'],category=category,title=title,
            extraction='official original PDF text/Tesseract vie+eng; clause structure generated locally',
            page_kind='physical_pdf',not_exhaustive=articles is not None,
            verification='original provenance/hash verified; critical extracted pages reviewed separately; no blanket current-effectiveness claim')
        if row['id']=='water215':
            source.update(extraction=reviewed['method'],not_exhaustive=True,
                reviewed_extract='docs/legal_fix_originals_20261004/water215_verified_extract.json')
        entries.append(build(source,pages,articles))
    raw=by_id['civil91']
    reviewed=json.loads((fix_root/'civil_service_verified_extract.json').read_text(encoding='utf-8'))
    assert reviewed['original_sha256']==raw['sha256']==sha(ROOT/raw['path'])
    pages=reviewed['pages']
    source=dict(raw,id='civil-service-contract',category='real_estate_brokerage',
        title='Bộ luật Dân sự 91/2015/QH13 — hợp đồng dịch vụ',source_url=raw['source_page_url'],
        extraction=reviewed['method'],page_kind='physical_pdf',
        reviewed_extract='docs/legal_fix_originals_20261004/civil_service_verified_extract.json',
        not_exhaustive=True,verification='Articles 513-519 checked against physical pages 34/35. General service contract rules; does not establish a mandatory broker fee or infer employment relationship')
    entries.append(build(source,pages,[513,514,515,516,517,518,519]))
    guidance=json.loads((fix_root/'guidance_manifest.json').read_text(encoding='utf-8'))
    for raw in guidance['sources']:
        if not raw['indexed']:continue
        assert sha(ROOT/raw['path'])==raw['sha256']
        assert sha(ROOT/raw['excerpt_path'])==raw['excerpt_sha256']
        source=dict(raw,category='electricity',title='Hướng dẫn công khai cách tính tiền điện nhà trọ Cần Thơ — 21/09/2026',
            extraction='Two complete native HTML paragraphs, no LLM paraphrase; public local guidance, not a legal article',
            page_kind='web_excerpt',not_exhaustive=True,verification=raw['limitation'])
        record=provision_json(Provision(raw['sha256']+':guidance',None,None,
            'Hướng dẫn công khai cách tính tiền điện nhà trọ Cần Thơ',
            (ROOT/raw['excerpt_path']).read_text(encoding='utf-8').strip(),0,
            len((ROOT/raw['excerpt_path']).read_text(encoding='utf-8').strip()),[],[],[],kind='official_guidance'))
        record.update(page_from=1,page_to=1)
        target=OUT/(raw['id']+'.json');target.write_text(json.dumps({'source':source,'provisions':[record]},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        entries.append({'file':target.relative_to(ROOT).as_posix(),'sha256':sha(target),'id':raw['id'],
            'category':'electricity','provisions':1,'articles':[None]})
    raw=by_id['fire105']
    pages=json.loads((ROOT/'eval/source_supplement_20261003/fire105.pages.json').read_text(encoding='utf-8'))
    text,spans=join_pages(pages)
    start=re.search(r'(?im)^Phụ lục I\s*$',text)
    end=re.search(r'(?im)^Phụ lục II\s*$',text[start.end():]) if start else None
    if not start or not end:raise ValueError('Missing full annex boundaries for fire105')
    finish=start.end()+end.start()
    items=list(re.finditer(r'(?m)^\s*(\d+)\.[ \t]+',text[start.end():finish]))
    introduction=text[start.start():start.end()+items[0].start()].strip()
    records=[]
    for i,item in enumerate(items):
        if item[1] not in ('1','14','17'):continue
        a=start.end()+item.start();b=start.end()+items[i+1].start() if i+1<len(items) else finish
        provision=Provision(raw['sha256'][:20]+':annexI:'+item[1],None,item[1],
            'Phụ lục I. Danh mục cơ sở thuộc diện quản lý về phòng cháy, chữa cháy | Mục '+item[1],
            text[a:b].strip(),a,b,[],[],[],kind='legal_annex',article_context=introduction)
        record=provision_json(provision);nums=[n for x,y,n in spans if x<b and y>a]
        record.update(page_from=min(nums),page_to=max(nums));records.append(record)
    source=dict(raw,id='fire105-annex-I',category='fire_safety',title='Nghị định 105/2025/NĐ-CP — Phụ lục I',
        source_url=raw['source_page_url'],extraction='original cached government PDF text; complete selected annex items, retained annex introduction',
        page_kind='physical_pdf',not_exhaustive=True,
        verification='Classification candidates only; no inference that an unspecified many-room house is a lodging business, collective housing or mixed-use building')
    target=OUT/'fire105-annex-I.json';target.write_text(json.dumps({'source':source,'provisions':records},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    entries.append({'file':target.relative_to(ROOT).as_posix(),'sha256':sha(target),'id':source['id'],
        'category':source['category'],'provisions':len(records),'articles':['annex I']})
    (OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'documents':len(entries),'provisions':sum(e['provisions'] for e in entries),'excluded':len(excluded)},ensure_ascii=False),flush=True)


if __name__ == '__main__':
    main()
