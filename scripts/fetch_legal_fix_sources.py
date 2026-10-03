"""Download official originals without treating website snippets as legislation."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, re
from urllib.parse import urljoin, urlparse
import requests

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/legal_fix_originals_20261004'
PAGES={
    'privacy356':'https://vanban.chinhphu.vn/?classid=1&docid=216387&pageid=27160',
    'privacy91':'https://vanban.chinhphu.vn/?docid=214590&pageid=27160',
    'electricity60':'https://congbao.chinhphu.vn/van-ban/thong-tu-so-60-2025-tt-bct-46756/60185.htm',
    'water50':'https://pbgdpl.cantho.gov.vn/attachment/8224',
    'privacy91-cb':'https://congbao.chinhphu.vn/detail/tai-ve?id=45578&slug=91-2025-qh15',
    'privacy356-cb':'https://congbao.cdnchinhphu.vn/180507251028987904/2026/1/17/356signed-1768638052103952849513.pdf',
    'water215':'https://capnuoccantho2.com.vn/View.aspx?wc=63&wp=332',
}

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    manifest={'downloaded_at_utc':datetime.now(timezone.utc).isoformat(),'sources':[]}
    session=requests.Session()
    for key,url in PAGES.items():
        response=session.get(url,timeout=90)
        if not response.ok:
            manifest['sources'].append({'id':key,'source_url':url,'download_error':'HTTP '+str(response.status_code)})
            continue
        if response.content.startswith(b'%PDF'):
            path=OUT/(key+'.pdf');path.write_bytes(response.content)
            manifest['sources'].append({'id':key,'source_url':url,'attachments':[{
                'download_url':url,'path':path.relative_to(ROOT).as_posix(),
                'sha256':hashlib.sha256(response.content).hexdigest()}]})
            continue
        path=OUT/(key+'.html');path.write_bytes(response.content)
        record={'id':key,'source_url':url,'path':path.relative_to(ROOT).as_posix(),
                'sha256':hashlib.sha256(response.content).hexdigest(),'attachments':[]}
        links=list(dict.fromkeys(urljoin(url,u.replace('&amp;','&')) for u in re.findall(r'(?:href|src)=[\"\']([^\"\']+)',response.text)))
        # Print only public links, never credentials or environment variables.
        for link in links:
            if '/api/download/' in link:continue
            if key in ('water50','water215'):continue # Only the attachment explicitly associated with this decision.
            if re.search(r'\.(pdf|doc)(?:\?|$)',link,re.I):
                print(key,link,flush=True)
                if '.pdf' in link.lower() or (key=='electricity60' and '.doc' in link.lower()):
                    host=urlparse(link).hostname or ''
                    if not (host.endswith('.gov.vn') or host.endswith('.chinhphu.vn') or host.endswith('.cdnchinhphu.vn')):continue
                    payload=session.get(link,timeout=120);payload.raise_for_status()
                    suffix='.doc' if '.doc' in link.lower() else '.pdf'
                    if suffix=='.pdf' and not payload.content.startswith(b'%PDF'):raise ValueError('Not PDF')
                    target=OUT/(key+suffix);target.write_bytes(payload.content)
                    record['attachments'].append({'download_url':link,'path':target.relative_to(ROOT).as_posix(),
                        'sha256':hashlib.sha256(payload.content).hexdigest()})
        manifest['sources'].append(record)
        if key in ('water50','water215'):
            if key=='water215':
                anchors=re.findall(r'<a[^>]+href=[\"\']([^\"\']+)[\"\'][^>]*>(.*?)</a>',response.text,re.I|re.S)
                drive=next((urljoin(url,href) for href,body in anchors if 'Quyết định số 215' in re.sub('<[^>]+>','',body)),None)
            else:drive=next((link for link in links if 'drive.google.com/file/d/' in link),None)
            if drive:
                file_id=drive.split('/file/d/')[1].split('/')[0]
                direct='https://drive.google.com/uc?export=download&id='+file_id
                payload=session.get(direct,timeout=120);payload.raise_for_status()
                if not payload.content.startswith(b'%PDF'):
                    record['attachment_error']='Public government-linked Drive download unavailable; no derived law indexed'
                    continue
                target=OUT/(key+'.pdf');target.write_bytes(payload.content)
                record['attachments'].append({'download_url':direct,'official_attachment_link':drive,
                    'path':target.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(payload.content).hexdigest(),
                    'provenance':('public Drive file explicitly linked by Can Tho Justice Department government publication' if key=='water50' else 'signed government decision explicitly linked by the accountable water utility; corroborate number/date/title with government publication; verify territorial/current application separately')})
    (OUT/'download_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

if __name__=='__main__':main()
