"""Add exact official Article 22 to the immutable v16 Word release."""
import hashlib
import json
from pathlib import Path
import zipfile
from xml.etree import ElementTree as ET
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'apps/api'))
from app.room_service.legal_knowledge.provisions import structure_provisions, provision_json


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    base = ROOT / 'docs/legal_word_repair_corpus_v16_20261006/manifest.json'
    out = ROOT / 'docs/legal_word_completion_v18_20261007'
    out.mkdir(exist_ok=True)
    manifest = json.loads(base.read_text(encoding='utf-8'))
    provenance = {r['id']: r for r in json.loads((ROOT / 'docs/review_sources_20261005/originals/provenance.json').read_text(encoding='utf-8'))}
    entries = []
    for entry in manifest['documents']:
        path = ROOT / entry['file']
        assert sha(path) == entry['sha256']
        data = json.loads(path.read_text(encoding='utf-8'))
        if entry['id'] in ('supplement-s15-word', 'supplement-s16-word'):
            key = 'S15' if entry['id'] == 'supplement-s15-word' else 'S16'
            source = data['source']
            word = ROOT / source['path']
            assert sha(word) == provenance[key]['sha256'] == source['sha256']
            assert provenance[key]['tls_verified'] and not source['ocr_used']
            if key == 'S15':
                assert {'15', '17'} <= {p['article'] for p in data['provisions']}
            if key in ('S15', 'S16'):
                with zipfile.ZipFile(word) as z:
                    tree = ET.fromstring(z.read('word/document.xml'))
                ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
                body = '\n\n'.join(''.join(t.text or '' for t in p.findall('.//w:t', ns)) for p in tree.findall('.//w:p', ns))
                wanted = {'12', '13'} if key == 'S15' else {'14', '22'}
                additions = [p for p in structure_provisions(body, sha(word)) if p.article in wanted]
                assert {p.article for p in additions} == wanted
                for part in additions:
                    assert part.content in body
                    value = provision_json(part)
                    value.update(page_from=1, page_to=1, extraction_text_sha256=hashlib.sha256(body.encode()).hexdigest())
                    data['provisions'].append(value)
                source['not_exhaustive'] = True
                target = out / (entry['id'] + '.json')
                target.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
                entry = dict(entry, file=target.relative_to(ROOT).as_posix(), sha256=sha(target), provisions=len(data['provisions']))
        entries.append(entry)
    result = dict(schema='legal_word_completion_v18_20261007', documents=entries,
        base_manifest_sha256=sha(base), official_sources_verified=['https://vanban.chinhphu.vn/?docid=216503&pageid=27160', provenance['S16']['source_url']],
        policy='Exact native official Word; Law Articles 12/13 and Decree Articles 14/22 added; existing Law Articles 15/17 retained. No OCR, summaries or reference answers. Prior releases retained.')
    (out / 'manifest.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(dict(schema=result['schema'], documents=len(entries), manifest_sha256=sha(out / 'manifest.json'))))


if __name__ == '__main__':
    main()
