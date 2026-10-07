"""Prepare literal CTU dormitory sources; do not generate answers or fee tables."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/ctu_ktx_corpus_20261007'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class ArticleText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.depth = 0
        self.skipped = 0
        self.parts = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if not self.depth and 'item-page' in attrs.get('class', '').split():
            self.depth = 1
        elif self.depth and tag == 'div':
            self.depth += 1
        if self.depth:
            if tag in ('script', 'style'):
                self.skipped += 1
            if tag in ('p', 'li', 'h1', 'h2', 'h3', 'br', 'div'):
                self.parts.append('\n')

    def handle_endtag(self, tag):
        if self.depth:
            if tag in ('script', 'style'):
                self.skipped = max(0, self.skipped - 1)
            if tag in ('p', 'li', 'h1', 'h2', 'h3', 'div'):
                self.parts.append('\n')
            if tag == 'div':
                self.depth -= 1

    def handle_data(self, data):
        if self.depth and not self.skipped:
            self.parts.append(data)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    entries = []
    baseline = ROOT / 'docs/legal_corpus_v5_20261004'
    old_manifest = json.loads((baseline / 'manifest.json').read_text(encoding='utf-8'))
    for key in ('ctu-2026-registration', 'ctu-new-students', 'ctu-ktx-rules'):
        entry = next(e for e in old_manifest['documents'] if e['id'] == key)
        path = ROOT / entry['file']
        assert sha(path) == entry['sha256'], key
        data = json.loads(path.read_text(encoding='utf-8'))
        assert sha(ROOT / data['source']['path']) == data['source']['original_sha256'], key
        target = OUT / path.name
        target.write_bytes(path.read_bytes())
        entries.append(dict(entry, file=target.relative_to(ROOT).as_posix()))

    key = 'ctu-ktx-facilities'
    url = 'https://ssc.ctu.edu.vn/hoat/160-cs1.html'
    with urlopen(url, timeout=30) as response:
        raw = response.read()
        resolved_url = response.url
    original = OUT / (key + '.html')
    original.write_bytes(raw)
    parser = ArticleText()
    parser.feed(raw.decode('utf-8'))
    lines = [' '.join(line.split()) for line in ''.join(parser.parts).splitlines() if line.strip()]
    body = '\n'.join(lines)
    assert '220.000' in body and '475.000' in body and 'Khu A' in body, 'Unexpected CTU article'
    groups, current = [], []
    for line in lines:
        if len('\n'.join(current + [line])) > 2200 and current:
            groups.append('\n'.join(current))
            current = []
        current.append(line)
    if current:
        groups.append('\n'.join(current))
    data = {'source': dict(id=key, title='Cơ sở vật chất, loại phòng và mức phí KTX Đại học Cần Thơ',
        category='student_housing', source_url=url, resolved_url=resolved_url,
        path=original.relative_to(ROOT).as_posix(), sha256=sha(original), original_sha256=sha(original),
        retrieved_at_utc=datetime.now(timezone.utc).isoformat(), pages=1, page_kind='web_excerpt',
        extraction='Native article HTML text; no paraphrase', not_exhaustive=False,
        verification='CTU primary publisher; fee range has no publication date in article'), 'provisions': []}
    for i, content in enumerate(groups):
        digest = hashlib.sha256(content.encode()).hexdigest()
        data['provisions'].append(dict(provision_id=f'{key}:{digest[:20]}', heading=f'Thông tin KTX CTU — phần {i+1}',
            content=content, content_sha256=digest, page_from=1, page_to=1, kind='official_information',
            article=None, clause=None, points=[], exceptions=[], cross_references=[], article_context=''))
    target = OUT / (key + '.json')
    target.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    entries.append(dict(id=key, file=target.relative_to(ROOT).as_posix(), sha256=sha(target),
                        category='student_housing', provisions=len(groups)))
    (OUT / 'manifest.json').write_text(json.dumps(dict(documents=entries,
        policy='Literal published CTU sources; semester dates remain explicit; no inferred vacancy or fees.'),
        ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'documents': len(entries), 'provisions': sum(e['provisions'] for e in entries)}))


if __name__ == '__main__':
    main()
