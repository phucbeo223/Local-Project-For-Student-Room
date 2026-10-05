"""Scope-limited Word-only release; never read PDFs, OCR output or answer keys."""
from pathlib import Path
import hashlib
import json
import re
import sys
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'apps/api'))
from app.room_service.legal_knowledge.extractor import extract_document
from app.room_service.legal_knowledge.provisions import structure_provisions, provision_json

OUT = ROOT / 'docs/legal_word_corpus_v7_20261005'
SCHEMA = 'legal_word_v7_20261005'
# Only useful basic tenant rules. Forms, drafted agreements, construction,
# investment, specialised proceedings and research summaries are not indexed.
SPECS = [
    ('housing79-word', '2026_204_79_VBHN-VPQH.docx', 'housing_contract', 'Luật Nhà ở — 79/VBHN-VPQH — bản Word cung cấp', [10,11,160,161,163,170,171,172,173]),
    ('consumer19-word', 'Luật-19-2023-QH15.docx', 'housing_contract', 'Luật Bảo vệ quyền lợi người tiêu dùng — bản Word cung cấp', [4,10,15,17,18,19]),
    ('electricity61-word', 'Luật-61-2024-QH15.docx', 'electricity', 'Luật Điện lực 61/2024/QH15 — bản Word cung cấp', [48,49,50,56,66,74]),
    ('electricity60-word', 'Thông-tư-60-2025-TT-BCT.docx', 'electricity', 'Thông tư 60/2025/TT-BCT — bản Word trích tuyển cung cấp', [3,12,20,21]),
    ('electricity1279-word', 'Quyết-định-1279-QĐ-BCT.docx', 'electricity', 'Biểu giá điện 1279/QĐ-BCT — bản Word cung cấp', [1,2,3]),
    ('fire105-word', 'Nghị-định-105-2025-NĐ-CP.docx', 'fire_safety', 'Nghị định 105/2025/NĐ-CP — bản Word cung cấp', [3]),
    ('broker29-word', 'Luật-29-2023-QH15.docx', 'real_estate_brokerage', 'Luật Kinh doanh bất động sản 29/2023/QH15 — bản Word cung cấp', [6,46,61,62,63,65]),
    ('identity26-word', 'Luật-26-2023-QH15.docx', 'privacy_data', 'Luật Căn cước 26/2023/QH15 — bản Word cung cấp', [7,20,29]),
    ('privacy91-word', 'Luật-91-2025-QH15.docx', 'privacy_data', 'Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 — bản Word cung cấp', [3,4,7,9,10,11,15,16,17,19]),
    ('privacy356-word', 'Nghị-định-356-2025-NĐ-CP.docx', 'privacy_data', 'Nghị định 356/2025/NĐ-CP — bản Word cung cấp', [5,6,7,8,9,10]),
    ('water215-word', 'Quyết-định-215-QĐ-UBND.docx', 'water_cantho', 'Giá nước Cần Thơ 215/QĐ-UBND — bản Word cung cấp', [1,2,3]),
    ('criminal135-word', 'Văn-bản-hợp-nhất-135-VBHN-VPQH.docx', 'criminal_law', 'Bộ luật Hình sự 135/VBHN-VPQH — bản Word trích tuyển cung cấp', [174,175]),
    ('procedure17-word', 'Văn-bản-hợp-nhất-17-VBHN-VPQH.docx', 'criminal_law', 'Bộ luật Tố tụng hình sự 17/VBHN-VPQH — bản Word trích tuyển cung cấp', [86,87,99,144,145]),
    ('civil91-word', 'civil91-word.doc', 'housing_contract', 'Bộ luật Dân sự 91/2015/QH13 — Word do cơ quan nhà nước công bố', [117,119,328,472,473,474,475,476,477,478,479,480,481,482]),
    ('fire55-word', 'fire55-word.doc', 'fire_safety', 'Luật PCCC 55/2024/QH15 — Word Công báo', [8,20,21,23,24]),
    ('residence68-word', 'residence68-word.doc', 'residence', 'Luật Cư trú 68/2020/QH14 — Word Công báo', [7,8,9,27,28]),
]

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read_word(path):
    if path.suffix.lower() not in ('.docx', '.doc'):
        raise ValueError('Word only: PDFs/images/OCR inputs are forbidden')
    doc = extract_document(path, ROOT / 'Data')
    assert doc.ocr_engine is None and not any(p.ocr_used for p in doc.pages)
    return '\n\n'.join(p.text for p in doc.pages)

def build():
    OUT.mkdir(parents=True, exist_ok=True)
    native = {s['id']: s for s in json.loads((ROOT/'Data/word_originals/sources.json').read_text(encoding='utf-8-sig'))}
    entries, included = [], set()
    for key, filename, category, title, articles in SPECS:
        paths = list((ROOT/'Data').rglob(filename))
        assert len(paths) == 1, filename
        path = paths[0]; body = read_word(path); included.add(path.resolve())
        assert 'BẢN TRÍCH TUYỂN NGHIÊN CỨU' not in body, 'Editorial research summaries cannot be called law'
        urls = re.findall(r'https://[^\s;]+', body)
        source_url = native[key]['source_url'] if key in native else (urls[0] if urls else None)
        if key == 'water215-word':
            # Provenance link only, never read its PDF or prior extracted text.
            source_url = 'https://capnuoccantho2.com.vn/View.aspx?wc=63&wp=332'
        host=urlparse(source_url or '').hostname or ''
        assert source_url and (host.endswith('.gov.vn') or host.endswith('.chinhphu.vn') or host=='capnuoccantho2.com.vn'), (key,source_url)
        digest = sha(path)
        if key in native: assert digest == native[key]['sha256']
        parts = [p for p in structure_provisions(body,digest) if p.article in {str(a) for a in articles}]
        if key == 'broker29-word':
            # Article 6 also covers investment projects/future buildings. Only
            # general disclosure and existing-building sections fit rentals.
            parts = [p for p in parts if p.article != '6' or p.clause in ('1','2')]
        assert parts, key
        provisions = []
        for p in parts:
            assert p.content in body
            v = provision_json(p)
            note_pattern = r'(?m)^Ghi chú tuyển chọn:[^\n]*(?:\n|$)'
            notes = re.findall(note_pattern,p.content)
            if notes:
                segments = [s.strip() for s in re.split(note_pattern,p.content) if s.strip()]
                assert all(s in body for s in segments)
                v.update(content='\n\n'.join(segments),source_segments=segments,
                    omitted_editorial_notes=[n.strip() for n in notes])
                v['content_sha256']=hashlib.sha256(v['content'].encode()).hexdigest()
                v['cross_references']=list(dict.fromkeys(re.findall(r'(?:khoản\s+\d+\s+)?Điều\s+\d+[a-z]?',v['content'],re.I)))
            v.update(page_from=1,page_to=1,extraction_text_sha256=hashlib.sha256(body.encode()).hexdigest())
            provisions.append(v)
        if key in ('electricity1279-word','water215-word'):
            start = re.search(r'(?im)^\s*(?:Phụ lục|BẢNG GIÁ|STT)\b',body)
            if start:
                table = body[start.start():]
                end = re.search(r'(?im)^\s*(?:Nơi nhận|TM\. ỦY BAN)',table)
                table = table[:end.start()] if end else table
                if len(table.strip()) > 80:
                    value=table.strip(); h=hashlib.sha256(value.encode()).hexdigest()
                    provisions.append(dict(provision_id=key+':table:'+h[:20],article=None,clause=None,heading='Bảng giá trong Word — thứ tự đoạn/ô, cần đối chiếu bố cục gốc',content=value,content_sha256=h,page_from=1,page_to=1,kind='source_table',points=[],exceptions=[],cross_references=[],article_context='',source_start=start.start(),source_end=start.start()+len(table)))
        source=dict(id=key,title=title,category=category,path=path.relative_to(ROOT).as_posix(),sha256=digest,original_sha256=digest,
                    source_url=source_url,page_kind='logical_document',pages=1,extraction='Native Word XML/antiword text; no PDF or OCR execution',
                    source_content_kind='published_word' if key in native else 'provided_word_excerpt',
                    verification='Word bytes and extracted content retained; supplied excerpts are not certified verbatim official originals.',
                    source_policy='Literal text from the supplied Word; context notes removed by article selection; no authored answers.',
                    scope='Basic accommodation questions only; no forms, agreement drafting, filing or specialised legal procedure.',
                    source_scope_warning='' if key in native else 'Nguồn là bản Word/trích tuyển được cung cấp, chưa xác minh toàn bộ câu chữ với bản chính thức; không coi ghi chú biên tập là quy định pháp luật.',
                    not_exhaustive=True,ocr_used=False)
        if key in native: source.update(download_url=native[key]['download_url'],retrieved_at_utc=native[key]['retrieved_at_utc'])
        target=OUT/(key+'.json')
        target.write_text(json.dumps({'source':source,'provisions':provisions},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        entries.append(dict(id=key,file=target.relative_to(ROOT).as_posix(),sha256=sha(target),category=category,provisions=len(provisions)))
    excluded=[dict(path=p.relative_to(ROOT).as_posix(),reason='Not an allowlisted basic legal Word source; forms, editorial summaries, specialised rules, PDFs and Markdown are excluded.') for p in sorted((ROOT/'Data').rglob('*')) if p.is_file() and p.resolve() not in included]
    manifest=dict(schema=SCHEMA,documents=entries,excluded=excluded,policy='Word only; no OCR/PDF/HTML/Markdown input, no reference answers; basic tenant questions; supplied Word provenance explicitly distinguished.')
    (OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'documents':len(entries),'provisions':sum(e['provisions'] for e in entries),'excluded':len(excluded)},ensure_ascii=False),flush=True)

if __name__ == '__main__':
    build()
