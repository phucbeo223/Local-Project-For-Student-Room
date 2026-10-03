"""Government originals covering supply contracts, metering and payment, not old room prices."""
from pathlib import Path
from urllib.parse import urlparse
from datetime import datetime, timezone
import hashlib,json,re,requests,certifi

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/legal_agent_originals_20261003'
SOURCES=[('water117','https://vanban.chinhphu.vn/?docid=33015&pageid=27160','34374_nd117cp.doc'),
         ('water124','https://vanban.chinhphu.vn/?docid=153298&pageid=27160','124nd.doc'),
         ('water57','https://vanban.chinhphu.vn/?docid=218699&pageid=27160','57-vbhn-bxd.signed.pdf')]


def main():
    sources=[]
    for key,source,name in SOURCES:
        response=requests.get(source,timeout=60,verify=certifi.where()); response.raise_for_status()
        urls=re.findall(r'(?:href|src)=[\"\']([^\"\']+)[\"\']',response.text)
        url=next(u for u in urls if u.rsplit('/',1)[-1].lower()==name.lower())
        assert urlparse(url).hostname=='datafiles.chinhphu.vn'
        path=OUT/(key+Path(name).suffix)
        if not path.exists():
            response=requests.get(url,timeout=90,verify=certifi.where());response.raise_for_status()
            assert response.content.startswith((b'%PDF-',bytes.fromhex('d0cf11e0a1b11ae1')))
            path.write_bytes(response.content)
        sources.append({'id':key,'source_url':source,'download_url':url,'path':path.relative_to(ROOT).as_posix(),
            'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'verified_at_utc':datetime.now(timezone.utc).isoformat()})
        print(key,path.stat().st_size,flush=True)
    (OUT/'water_manifest.json').write_text(json.dumps({'sources':sources},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':main()
