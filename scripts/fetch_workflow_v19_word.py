"""Retain official native Word bytes and provenance; no PDF/OCR conversion."""
from datetime import datetime, timezone
import hashlib
import json
import ssl
from pathlib import Path
from urllib.parse import urljoin, urlparse
import httpx
from html.parser import HTMLParser


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.current = [], None
    def handle_starttag(self, tag, attrs):
        if tag == 'a': self.current = [dict(attrs).get('href', ''), '']
    def handle_data(self, data):
        if self.current is not None: self.current[1] += data
    def handle_endtag(self, tag):
        if tag == 'a' and self.current is not None:
            self.links.append(self.current)
            self.current = None

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/legal_word_workflow_v19_20261007/originals'
SOURCES = [
    ('electricity60-official', 'https://congbao.chinhphu.vn/van-ban/thong-tu-so-60-2025-tt-bct-46756/60185.htm', '60-2025-TT-BCT.doc'),
    ('fire105-official', 'https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-105-2025-nd-cp-44912/56374.htm', '105-2025-NĐ-CP.doc'),
]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    records = []
    with httpx.Client(timeout=60, follow_redirects=True, verify=ssl.create_default_context()) as client:
        for key, page, label in SOURCES:
            response = client.get(page)
            response.raise_for_status()
            soup = Links()
            soup.feed(response.text)
            links = list(dict.fromkeys(urljoin(page, href) for href, text in soup.links if label in text))
            if not links:
                raise ValueError('No native official Word attachment: ' + key)
            for i, link in enumerate(links, 1):
                host = urlparse(link)
                if host.scheme != 'https' or not (host.hostname.endswith('.chinhphu.vn') or host.hostname == 'g7.cdnchinhphu.vn'):
                    raise ValueError('Non-official attachment')
                data = client.get(link)
                data.raise_for_status()
                if not data.content.startswith(bytes.fromhex('d0cf11e0')):
                    raise ValueError('Expected native binary Word, not converted or HTML data')
                path = OUT / f'{key}-{i}.doc'
                if path.exists() and path.read_bytes() != data.content:
                    raise ValueError('Official bytes changed; use a new version')
                path.write_bytes(data.content)
                records.append(dict(id=f'{key}-{i}', path=path.relative_to(ROOT).as_posix(),
                    source_url=page, download_url=link, sha256=hashlib.sha256(data.content).hexdigest(),
                    retrieved_at_utc=datetime.now(timezone.utc).isoformat(), tls_verified=True, ocr_used=False))
    (OUT / 'provenance.json').write_text(json.dumps(records, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps([dict(id=r['id'], sha256=r['sha256']) for r in records]))


if __name__ == '__main__':
    main()
