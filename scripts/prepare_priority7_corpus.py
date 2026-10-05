"""Extend native Word clauses, never ingest answer keys or authored legal text."""
import hashlib
import json
import sys
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from prepare_word_legal_corpus import extract_document
from app.room_service.legal_knowledge.provisions import structure_provisions, provision_json
import re
import html
import zipfile
from xml.etree import ElementTree as ET

OUT = ROOT / 'docs/legal_word_priority7_corpus_v13_20261006'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def read_word(path):
    assert path.suffix.lower() in ('.doc', '.docx')
    document = extract_document(path, ROOT)
    assert document.ocr_engine is None and not any(p.ocr_used for p in document.pages)
    return '\n\n'.join(p.text for p in document.pages)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    base_path = ROOT / 'docs/legal_word_focus3_corpus_v11_20261006/manifest.json'
    base = json.loads(base_path.read_text(encoding='utf-8'))
    entries = []
    additions = {'residence68-word': {'10'}, 'civil91-word': {'3', '398'},
                 'supplement-s16-word': {'7'}}
    for entry in base['documents']:
        assert sha(ROOT / entry['file']) == entry['sha256']
        if entry['id'] not in additions:
            entries.append(entry)
            continue
        data = json.loads((ROOT / entry['file']).read_text(encoding='utf-8'))
        source = data['source']
        word = ROOT / source['path']
        assert sha(word) == source['sha256'] and not source['ocr_used']
        body = read_word(word)
        parts = [p for p in structure_provisions(body, sha(word))
                 if p.article in additions[entry['id']]]
        assert {p.article for p in parts} == additions[entry['id']]
        for part in parts:
            assert part.content in body
            value = provision_json(part)
            value.update(page_from=1, page_to=1,
                         extraction_text_sha256=hashlib.sha256(body.encode()).hexdigest())
            data['provisions'].append(value)
        if entry['id'] == 'residence68-word':
            # A landlord is not necessarily the head of the household.
            source['source_scope_warning'] = ('Điều 9 quy định nghĩa vụ công dân; Điều 10 quy định chủ hộ/thành viên hộ gia đình, không tự đồng nhất chủ trọ với chủ hộ. Chỉ giải thích trách nhiệm và giấy tờ cơ bản, không điền tờ khai hoặc hướng dẫn hồ sơ chuyên sâu.')
        target = OUT / (entry['id'] + '.json')
        save(target, data)
        entries.append(dict(entry, file=target.relative_to(ROOT).as_posix(),
                            sha256=sha(target), provisions=len(data['provisions'])))

    captures = ROOT / 'eval/provider_sources_20261005/priority7_20261006'
    captures.mkdir(parents=True, exist_ok=True)
    url = 'https://cskh.evnspc.vn/TinTuc/TinTucChiTiet?LoaiTinBai=ALL&MaTinBai=3103'
    raw = captures / 'evn-cantho.html'
    if not raw.exists():
        with urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=45) as response:
            assert response.status == 200 and response.url.startswith('https://cskh.evnspc.vn/')
            raw.write_bytes(response.read())
    literal = 'công khai cách tính và thu tiền điện theo đúng hóa đơn do Điện lực phát hành'
    original = ' '.join(html.unescape(re.sub(r'<[^>]+>', ' ', raw.read_bytes().decode('utf-8'))).split())
    assert literal in original and len(literal.split()) <= 25
    add_excerpt(entries, 'evn-cantho-transparency-word', 'Công khai cách tính tiền điện nhà trọ — PC TP Cần Thơ / EVNSPC',
                'electricity', url, literal, sha(raw),
                'Hướng dẫn kiểm tra nhà trọ Cần Thơ đăng ngày 21/09/2026; không phải điều luật hoặc quy định một mẫu bảng kê bắt buộc. Trích đoạn ngắn về công khai cách tính và hóa đơn; không tự suy ra mọi chi tiết kê khai.', '2026-09-21')
    # Exact short sentence from the previously captured publisher DOM. No OCR.
    old_capture = ROOT / 'eval/provider_sources_20261005/word_supplement_v8/S14.blocks.json'
    blocks = json.loads(old_capture.read_text(encoding='utf-8'))
    literal = 'đồng thời gọi ngay lực lượng Cảnh sát PCCC và CNCH theo số 114.'
    assert literal in blocks[17]
    s14 = json.loads((ROOT / 'docs/legal_word_supplement_corpus_v8_20261005/supplement-s14-word.json').read_text(encoding='utf-8'))['source']
    original_html = ROOT / 'eval/provider_sources_20261005/word_supplement_v8/S14.html'
    assert sha(original_html) == s14['original_html_sha256']
    native_text = ' '.join(html.unescape(re.sub(r'<[^>]+>', ' ', original_html.read_text(encoding='utf-8'))).split())
    assert literal in native_text
    add_excerpt(entries, 'fire-emergency114-word', 'Báo cháy 114 — Công an tỉnh Phú Thọ',
                'fire_safety', s14['source_url'], literal, sha(original_html),
                'Khuyến cáo khi phát hiện cháy; gọi 114 trong tình huống cháy/khẩn cấp, không trình bày là số tiếp nhận mọi tranh chấp thuê trọ.', None)
    save(OUT / 'manifest.json', dict(schema='legal_word_priority7_v13_20261006', documents=entries,
         base_manifest_sha256=sha(base_path), base_documents_unchanged=False,
         unchanged_entries=sum(e in base['documents'] for e in entries),
         expanded_native_articles={k: sorted(v) for k, v in additions.items()},
         policy='Isolated trial retaining active store and v11. Native Word laws and exact publisher excerpts only; no OCR/PDF/forms/answer keys/authored legal summaries.'))
    print(json.dumps(dict(documents=len(entries), manifest_sha256=sha(OUT / 'manifest.json')), ensure_ascii=False))


def add_excerpt(entries, key, title, category, url, literal, raw_sha, warning, date):
    word = OUT / (key + '.docx')
    if not word.exists():
        # Retain a standard native DOCX package, replacing its text body only.
        template = ROOT / 'docs/legal_word_focus3_corpus_v10_20261006/google-lens-publisher-excerpts.docx'
        ns = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
        with zipfile.ZipFile(template) as src, zipfile.ZipFile(word, 'w', zipfile.ZIP_DEFLATED) as dst:
            root = ET.fromstring(src.read('word/document.xml')); body = root.find('{'+ns+'}body')
            for child in list(body):
                if child.tag != '{'+ns+'}sectPr': body.remove(child)
            paragraph = ET.Element('{'+ns+'}p'); run = ET.SubElement(paragraph, '{'+ns+'}r')
            ET.SubElement(run, '{'+ns+'}t').text = literal; body.insert(0, paragraph)
            for item in src.infolist():
                dst.writestr(item, ET.tostring(root, encoding='utf-8', xml_declaration=True)
                             if item.filename == 'word/document.xml' else src.read(item.filename))
    assert read_word(word).strip() == literal
    source = dict(id=key, title=title, category=category, path=word.relative_to(ROOT).as_posix(),
        sha256=sha(word), source_url=url, publication_date=date, publisher=title.split('—')[-1].strip(),
        page_kind='logical_document', pages=1, ocr_used=False,
        extraction='Native DOCX XML; verified literal publisher excerpt, no OCR/PDF',
        source_content_kind='publisher_guidance_word_conversion', source_scope_warning=warning,
        original_html_sha256=raw_sha, source_policy='Exact source text only; no reference answer.')
    h = hashlib.sha256(literal.encode()).hexdigest()
    provision = dict(provision_id=key + ':excerpt', article=None, clause=None, heading=title,
        content=literal, source_segments=[literal], source_start=0, source_end=len(literal),
        content_sha256=h, extraction_text_sha256=h, points=[], exceptions=[], cross_references=[],
        kind='publisher_guidance', article_context='', page_from=1, page_to=1)
    target = OUT / (key + '.json')
    save(target, dict(source=source, provisions=[provision]))
    entries.append(dict(id=key, file=target.relative_to(ROOT).as_posix(), sha256=sha(target),
                        category=category, provisions=1))


if __name__ == '__main__':
    main()
