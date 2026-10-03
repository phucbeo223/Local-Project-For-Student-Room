"""Download authorized official public sources, preserving URLs and byte hashes."""
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urlparse, urljoin
from html.parser import HTMLParser
from datetime import datetime, timezone
import hashlib
import json
import re
import zipfile
import ssl
import certifi
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/legal_sources_originals_20261003'
SOURCES = [
    ('civil91', 'https://datafiles.chinhphu.vn/cpp/files/vbpq/2016/01/91_.pdf', 'pdf'),
    ('civil91first', 'https://datafiles.chinhphu.vn/cpp/files/vbpq/2016/01/91.signed.pdf', 'pdf'),
    ('residence68', 'https://congan.lamdong.gov.vn/UpLoaded/files/luat/68_2020_QH14.pdf', 'pdf'),
    ('amend118', 'https://datafiles.chinhphu.vn/cpp/files/vbpq/2026/01/luatso118.2025.pdf', 'pdf'),
    ('fire55', 'https://datafiles.chinhphu.vn/cpp/files/vbpq/2025/01/luat55.pdf', 'pdf'),
    ('fire105', 'https://datafiles.chinhphu.vn/cpp/files/vbpq/2025/5/105-ndcp.signed.pdf', 'pdf'),
    ('amend347', 'https://datafiles.chinhphu.vn/cpp/files/vbpq/2026/9/347_2026_nd-cp_08092026_7-signed.signed.pdf', 'pdf'),
    ('broker29', 'https://datafiles.chinhphu.vn/cpp/files/vbpq/2024/01/luat29.pdf', 'pdf'),
    ('rental_warning', 'https://www.bocongan.gov.vn/bai-viet/canh-giac-voi-chieu-tro-lua-dao-dat-coc-thue-nha-tro-qua-mang-1782485063', 'html'),
    ('online_warning', 'https://www.bocongan.gov.vn/bai-viet/xuat-hien-thu-doan-lua-dao-moi-khi-mua-hang-online-1790562304', 'html'),
]

class TextParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.parts = []; self.links = []; self.skip = 0
    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'): self.skip += 1
        if tag in ('p', 'div', 'br', 'li', 'tr', 'h1', 'h2', 'h3'): self.parts.append('\n')
        for key, value in attrs:
            if key == 'href' and value: self.links.append(value)
    def handle_endtag(self, tag):
        if tag in ('script', 'style'): self.skip = max(0, self.skip - 1)
        if tag in ('p', 'div', 'li', 'tr'): self.parts.append('\n')
    def handle_data(self, data):
        if not self.skip: self.parts.append(data)

def fetch(url):
    host = urlparse(url).hostname or ''
    if not any(host == d or host.endswith('.' + d) for d in ('chinhphu.vn', 'cdnchinhphu.vn', 'moj.gov.vn', 'congan.lamdong.gov.vn', 'bocongan.gov.vn')):
        raise ValueError('Non-official source rejected')
    context = ssl.create_default_context(cafile=certifi.where())
    with urlopen(Request(url, headers={'User-Agent': 'LegalResearch/1.0'}), timeout=60, context=context) as response:
        return response.read(), response.url

def main():
    import fitz
    OUT.mkdir(parents=True, exist_ok=True)
    previous = json.loads((OUT / 'download_manifest.json').read_text(encoding='utf-8')) if (OUT / 'download_manifest.json').exists() else {'sources': []}
    previous_urls = {s['id']: s['download_url'] for s in previous['sources']}
    manifest = []
    for key, url, kind in SOURCES:
        path = OUT / (key + '.' + kind)
        actual_url = previous_urls.get(key, url)
        if not path.exists():
            raw, actual_url = fetch(url)
            if kind in ('docx', 'pdf') and not raw.startswith((b'PK', b'%PDF')):
                portal = TextParser(); portal.feed(raw.decode('utf-8', errors='replace'))
                candidates = [u for u in portal.links if re.search(r'\.' + kind + r'(?:$|[?&])', u, re.I)]
                if not candidates: raise RuntimeError(f'{key}: no official download link')
                raw, actual_url = fetch(urljoin(url, candidates[0]))
            if kind == 'pdf' and not raw.startswith(b'%PDF'): raise ValueError('Not a PDF')
            if kind == 'docx' and not raw.startswith(b'PK'): raise ValueError('Not a DOCX')
            path.write_bytes(raw)
        raw = path.read_bytes()
        pages = []
        if kind == 'pdf':
            document = fitz.open(path)
            pages = [{'page': i + 1, 'text': page.get_text()} for i, page in enumerate(document)]
        elif kind == 'docx':
            ns = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
            with zipfile.ZipFile(path) as archive:
                tree = ElementTree.fromstring(archive.read('word/document.xml'))
            pages = [{'page': 1, 'text': '\n'.join(''.join(n.text or '' for n in p.iter(ns+'t')) for p in tree.iter(ns+'p'))}]
        else:
            parser = TextParser(); parser.feed(raw.decode('utf-8', errors='replace'))
            pages = [{'page': 1, 'text': re.sub(r'\n\s*\n+', '\n', ''.join(parser.parts))}]
        (OUT / (key + '.pages.json')).write_text(json.dumps(pages, ensure_ascii=False, indent=2), encoding='utf-8')
        (OUT / (key + '.txt')).write_text('\n'.join(p['text'] for p in pages), encoding='utf-8')
        manifest.append({'id': key, 'source_page_url': url, 'download_url': actual_url,
                         'path': path.relative_to(ROOT).as_posix(), 'sha256': hashlib.sha256(raw).hexdigest(),
                         'bytes': len(raw), 'pages': len(pages), 'text_chars': sum(len(p['text']) for p in pages)})
        (OUT / 'download_manifest.json').write_text(json.dumps({'client_date': '2026-10-03',
            'recorded_at_utc': datetime.now(timezone.utc).isoformat(), 'sources': manifest}, ensure_ascii=False, indent=2), encoding='utf-8')
        print(key, len(raw), 'bytes;', len(pages), 'pages;', manifest[-1]['text_chars'], 'chars', flush=True)

if __name__ == '__main__': main()
