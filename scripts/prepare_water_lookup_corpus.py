"""Append bounded literal publisher excerpts; never read evaluation answers."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, re, shutil, sys
from urllib.parse import urlparse
import httpx
from bs4 import BeautifulSoup
from prepare_source_grounded_corpus import unit

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT/'docs/legal_corpus_v5_20261004'
OUT = ROOT/'docs/legal_corpus_v6_20261005'
RAW = ROOT/'eval/provider_sources_20261005'
EXCERPTS = ROOT/'docs/provider_excerpts_20261005'

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def normalized(value): return re.sub(r'\s+', ' ', value).strip()
def allowed(url):
    parsed = urlparse(url); host = parsed.hostname or ''
    return parsed.scheme == 'https' and any(host == domain or host.endswith('.'+domain)
        for domain in ('ctn-cantho.com.vn', 'capnuoccantho2.com.vn'))

def main():
    for directory in (OUT, RAW, EXCERPTS): directory.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((BASE/'manifest.json').read_text(encoding='utf-8'))
    for entry in manifest['documents']:
        original = ROOT/entry['file']; assert sha(original) == entry['sha256']
        target = OUT/original.name; shutil.copyfile(original, target)
        entry['file'] = target.relative_to(ROOT).as_posix()
    sources = [
        ('water-cantho-invoice-guide', 'https://ctn-cantho.com.vn/tin-khoa-hoc-cong-nghe/huong-dan-truy-cap-website-de-tra-cuu-va-tai-hoa-don-tien-nuoc-331.html',
         'CANTHOWASSCO — tra cứu', [
             'IDKH và Mã xác nhận (số này được in trên Giấy báo/Biên nhận tiền nước).',
             'TRA CỨU HÓA ĐƠN']),
        ('water-cantho-invoice-portal', 'https://hddt.ctn-cantho.com.vn/',
         'CANTHOWASSCO — cổng hóa đơn', [
             'TRA CỨU HÓA ĐƠN ĐIỆN TỬ', 'Nhập IDKH để tra cứu', 'Mã xác nhận', 'Tra cứu hóa đơn']),
        ('water-cantho2-invoice-faq', 'https://capnuoccantho2.com.vn/View.aspx?wp=253',
         'Cấp nước CT2 — tra cứu', [
             'Mã khách hàng trên biên nhận tiền nước (mục IDKH)', 'Zalo OA Cấp nước Cần Thơ 2']),
    ]
    with httpx.Client(timeout=90, follow_redirects=True) as client:
        for key, url, title, fragments in sources:
            assert allowed(url)
            path = RAW/(key+'.html')
            if not path.exists():
                response = client.get(url); response.raise_for_status()
                assert allowed(str(response.url))
                path.write_bytes(response.content)
            soup = BeautifulSoup(path.read_bytes(), 'html.parser')
            for node in soup.select('script,style'): node.decompose()
            native = normalized(soup.get_text(' ', strip=True))
            native += ' ' + ' '.join(normalized(node.get('placeholder','')) for node in soup.select('input'))
            assert sum(len(fragment.split()) for fragment in fragments) <= 25
            assert all(normalized(fragment) in native for fragment in fragments), key
            excerpt = EXCERPTS/(key+'.txt')
            excerpt.write_text('\n'.join(fragments)+'\n', encoding='utf-8')
            origin = {'path':path.relative_to(ROOT).as_posix(), 'sha256':sha(path), 'source_url':url,
                      'retrieved_at_utc':datetime.now(timezone.utc).isoformat()}
            source = {'id':key, 'title':title, 'category':'water_cantho', 'source_url':url,
                'path':excerpt.relative_to(ROOT).as_posix(), 'sha256':sha(excerpt), 'original_sha256':sha(path),
                'origin_documents':[origin], 'pages':1, 'page_kind':'web_excerpt', 'not_exhaustive':True,
                'extraction':'Bounded literal native HTML text/form labels; whitespace normalization only.',
                'source_policy':'Public publisher excerpts only; complete fetched HTML retained locally for hash verification.',
                'verification':'Publisher-specific instructions, not a universal water tariff or rental allocation rule.'}
            parts = [unit(key, 0, '\n'.join(fragments), 'Tra cứu hóa đơn — thông tin công bố', 1)]
            target = OUT/(key+'.json')
            target.write_text(json.dumps({'source':source, 'provisions':parts}, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
            manifest['documents'].append({'id':key,'file':target.relative_to(ROOT).as_posix(), 'sha256':sha(target),
                'category':'water_cantho', 'provisions':len(parts)})
            print(key, len(parts), flush=True)
    manifest.update(schema='legal_v6_20261005', parent_manifest_sha256=sha(BASE/'manifest.json'),
        policy='Immutable v5 originals plus bounded literal provider excerpts; private references never read or indexed.')
    (OUT/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'documents':len(manifest['documents']), 'provisions':sum(d['provisions'] for d in manifest['documents'])}))

if __name__ == '__main__': main()
