"""Download only government attachments; keep originals and hashes."""
from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import urlparse
import concurrent.futures
import hashlib
import json
import requests
import certifi
import fitz

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'docs/legal_agent_originals_20261003'
SOURCES = [
    ('ecommerce122', 'https://vanban.chinhphu.vn/?docid=216503&pageid=27160', 'https://datafiles.chinhphu.vn/cpp/files/vbpq/2026/01/luat122.2025.qh15.pdf'),
    ('ecommerce248', 'https://vanban.chinhphu.vn/?docid=218747&pageid=27160', 'https://datafiles.chinhphu.vn/cpp/files/vbpq/2026/7/248-ndcp.signed.pdf'),
    ('electricity14', 'https://vanban.chinhphu.vn/?docid=213782&pageid=27160', 'https://datafiles.chinhphu.vn/cpp/files/vbpq/2025/5/14-2025-ttg.signed.pdf'),
    ('electricity133', 'https://vanban.chinhphu.vn/?docid=217612&pageid=27160', 'https://datafiles.chinhphu.vn/cpp/files/vbpq/2026/4/133-ndcp.signed.pdf'),
    ('fire106', 'https://vanban.chinhphu.vn/?docid=213672&pageid=27160', 'https://datafiles.chinhphu.vn/cpp/files/vbpq/2025/5/106-npcp.signed.pdf'),
    ('residence154', 'https://vanban.chinhphu.vn/?docid=211821&pageid=27160', 'https://datafiles.chinhphu.vn/cpp/files/vbpq/2024/11/154-cp.signed.pdf'),
    ('amend58', 'https://vanban.chinhphu.vn/?docid=216977&pageid=27160', 'https://datafiles.chinhphu.vn/cpp/files/vbpq/2026/02/58nd.signed.pdf'),
    ('residence116', 'https://vanban.bocongan.gov.vn/co-so-du-lieu-van-ban/thong-tu-quy-dinh-chi-tiet-mot-so-dieu-va-bien-phap-thi-hanh-luat-cu-tru-1784261073', 'https://bocongan.gov.vn/media/bca-media/library-20260717110413-0c32870e-3f4d-41d8-9da4-8f90638543ff-thong-tu-116-2026.pdf'),
]


def fetch(item):
    name, source, url = item
    assert urlparse(url).hostname in {'datafiles.chinhphu.vn','bocongan.gov.vn'}
    p = OUT/(name+'.pdf')
    if not p.exists():
        response = requests.get(url, timeout=90, verify=certifi.where())
        response.raise_for_status()
        assert response.content.startswith(b'%PDF-')
        p.write_bytes(response.content)
    doc = fitz.open(p)
    result = {'id': name, 'source_url': source, 'download_url': url,
              'path': p.relative_to(ROOT).as_posix(), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest(),
              'pages': len(doc), 'native_chars': sum(len(page.get_text()) for page in doc),
              'verified_at_utc': datetime.now(timezone.utc).isoformat()}
    print(name, result['pages'], result['native_chars'], flush=True)
    return result


if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        sources = list(pool.map(fetch, SOURCES))
    (OUT/'manifest.json').write_text(json.dumps({'sources': sources}, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
