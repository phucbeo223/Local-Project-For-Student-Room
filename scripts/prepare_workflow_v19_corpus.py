"""New immutable release from native official Word; references never read."""
from pathlib import Path
import hashlib
import json
import re
from prepare_word_legal_corpus import structure_provisions, provision_json, ROOT, sha
from app.room_service.legal_knowledge.extractor import extract_document

OUT = ROOT / 'docs/legal_word_workflow_v19_20261007'


def save(path, data):
    value = json.dumps(data, ensure_ascii=False, indent=2)+'\n'
    if path.exists() and path.read_text(encoding='utf-8') != value:
        raise ValueError('Immutable corpus bytes changed: ' + str(path))
    path.write_text(value, encoding='utf-8')


def main():
    base = ROOT / 'docs/legal_word_completion_v18_20261007/manifest.json'
    entries = json.loads(base.read_text(encoding='utf-8'))['documents']
    for entry in entries:
        assert sha(ROOT / entry['file']) == entry['sha256']
    provenance = json.loads((OUT / 'originals/provenance.json').read_text(encoding='utf-8'))
    for record in provenance:
        word = ROOT / record['path']
        assert sha(word) == record['sha256'] and record['tls_verified'] and not record['ocr_used']
        document = extract_document(word, OUT)
        assert document.ocr_engine is None and not any(p.ocr_used for p in document.pages)
        body = '\n\n'.join(p.text for p in document.pages)
        save(OUT / (record['id'] + '-extraction.json'), dict(text=body, sha256=hashlib.sha256(body.encode()).hexdigest(), word_sha256=sha(word)))
        fire = record['id'].startswith('fire')
        provisions = []
        selected = [p for p in structure_provisions(body, sha(word))
                    if p.article in ({'3', '4', '5', '6', '8', '9', '10'} if fire else {'12', '20', '21'})]
        for part in selected:
            assert part.content in body
            value = provision_json(part)
            value.update(page_from=1, page_to=1, extraction_text_sha256=hashlib.sha256(body.encode()).hexdigest())
            provisions.append(value)
        # Annex tables must retain row/column relationships. Store each whole
        # annex as its parent, with original delimiters from the Word extractor.
        if fire:
            anchors = list(re.finditer(r'(?mi)^\s*Phụ lục\s+([IVX]+)\s*$', body))
            for i, anchor in enumerate(anchors):
                if anchor[1] not in ('I', 'II', 'III'):
                    continue
                end = anchors[i+1].start() if i+1 < len(anchors) else len(body)
                content = body[anchor.start():end].strip()
                digest = hashlib.sha256(content.encode()).hexdigest()
                provisions.append(dict(provision_id=record['id']+':annex:'+anchor[1], article=None, clause=None,
                    heading='Phụ lục '+anchor[1]+' — phân loại cơ sở theo công năng, số tầng, diện tích; giữ nguyên bảng',
                    content=content, content_sha256=digest, source_start=anchor.start(), source_end=end,
                    page_from=1, page_to=1, points=[], exceptions=[], cross_references=[],
                    kind='source_table', article_context=''))
        if not provisions:
            print('No selected clauses/annexes:', record['id'], flush=True)
            continue
        warning = ('Phân loại theo đúng công năng nhà ở/cơ sở dịch vụ lưu trú; không áp ngưỡng của nhà chung cư '
                   'cho mọi nhà trọ. Chưa đủ căn cứ trong trích tuyển để ấn định số lối thoát hay số bình cho công trình cụ thể.'
                   if fire else 'Điểm c khoản 5 Điều 12 và các phần liên quan có hiệu lực có điều kiện theo Điều 21; '
                   'chưa xác minh sự kiện điều chỉnh giá kích hoạt. Không dùng biểu giá cũ để tính ví dụ trong chế độ mới.')
        source = dict(record, title=('Nghị định 105/2025/NĐ-CP' if fire else 'Thông tư 60/2025/TT-BCT')+' — Word Công báo chính thức',
            category='fire_safety' if fire else 'electricity', original_sha256=sha(word),
            page_kind='logical_document', pages=1, extraction='Native official Word/antiword; no PDF/OCR',
            source_content_kind='published_word', publisher='Công báo Chính phủ',
            effective_date='2025-07-01' if fire else '2025-12-02',
            source_scope_warning=warning, not_exhaustive=True,
            source_policy='Literal official clauses/annex parents with offsets; no answer keys, generated legal facts or OCR.')
        target = OUT / (record['id']+'.json')
        save(target, dict(source=source, provisions=provisions))
        entries.append(dict(id=source['id'], file=target.relative_to(ROOT).as_posix(), sha256=sha(target),
                            category=source['category'], provisions=len(provisions)))
        print(record['id'], 'provisions', len(provisions), 'annexes', [p['heading'] for p in provisions if p['kind']=='source_table'], flush=True)
    save(OUT / 'manifest.json', dict(schema='legal_word_workflow_v19_20261007', documents=entries,
        base_manifest_sha256=sha(base), policy='Immutable v18 extension with official native Word electricity/PCCC; retain v18 and reference isolation. Transitional trigger is unresolved.'))


if __name__ == '__main__':
    main()
