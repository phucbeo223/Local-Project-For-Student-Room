"""Capture public publisher pages for a Word-only, isolated RAG experiment."""
from pathlib import Path
import concurrent.futures
import hashlib
import json
import urllib.request
from datetime import datetime, timezone
from lxml import html

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'eval/provider_sources_20261005/word_supplement_v8'

def fetch(source):
    key = source['id']
    target = OUT / (key + '.html')
    try:
        if not target.exists():
            request = urllib.request.Request(source['url'], headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(request, timeout=45) as response:
                body = response.read()
                assert response.status == 200
            target.write_bytes(body)
        body = target.read_bytes()
        tree = html.fromstring(body.decode('utf-8-sig'))
        for element in tree.xpath('//script|//style|//noscript'):
            element.drop_tree()
        lines = []
        # Leaf text-bearing blocks keep paragraphs and list entries in DOM order.
        for element in tree.xpath('//h1|//h2|//h3|//h4|//p|//li[not(.//p)]|//td[not(.//p)]'):
            if element.tag == 'p' and element.xpath('.//p'): continue
            value = ' '.join(element.text_content().split())
            if value: lines.append(value)
        (OUT / (key + '.blocks.json')).write_text(json.dumps(lines, ensure_ascii=False, indent=2), encoding='utf-8')
        result = dict(id=key, url=source['url'], sha256=hashlib.sha256(body).hexdigest(), bytes=len(body),
                      retrieved_at_utc=datetime.now(timezone.utc).isoformat(), blocks=len(lines), status='captured')
        print(key, len(body), len(lines), flush=True)
        return result
    except Exception as exc:
        print(key, type(exc).__name__, str(exc), flush=True)
        return dict(id=key, url=source['url'], status='unavailable', error=str(exc))

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    sources=json.loads((ROOT/'docs/review_sources_20261005/sources.json').read_text(encoding='utf-8'))['sources']
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        results=list(pool.map(fetch, [s for s in sources if s['format']=='HTML']))
    (OUT/'capture.json').write_text(json.dumps(results, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

if __name__=='__main__': main()
