"""Keep official guidance separate from statutes and foreign local rules."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,requests,re
from html.parser import HTMLParser

class Paragraphs(HTMLParser):
    def __init__(self):super().__init__();self.parts=[];self.lines=[];self.hidden=False
    def flush(self):
        line=re.sub(r'\s+',' ',''.join(self.parts)).strip()
        if line:self.lines.append(line)
        self.parts=[]
    def handle_starttag(self,tag,attrs):
        if tag in ('script','style'):self.hidden=True
        if tag in ('p','div','br','h1','h2','h3'):self.flush()
    def handle_data(self,data):
        if not self.hidden:self.parts.append(data)
    def handle_endtag(self,tag):
        if tag in ('script','style'):self.hidden=False
        if tag in ('p','div','h1','h2','h3'):self.flush()

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/legal_fix_originals_20261004'
SOURCES={
    'electricity-cantho-guidance':'https://btgdv.cantho.gov.vn/vi/news/thong-tin-tong-hop/nha-tro-minh-bach-gia-dien-nguoi-thue-them-yen-tam-4629.html',
    'electricity-hanoi-guidance':'https://phucloi.hanoi.gov.vn/thong-tin-tuyen-truyen/tuyen-truyen-thuc-hien-gia-ban-le-dien-tai-cac-diem-cho-thue-nha-de-o-theo-chi-thi-so-04-ct-ubnd-cua-ubnd-thanh-pho-ha-noi-2702260518144621697.htm',
}

def main():
    manifest={'downloaded_at_utc':datetime.now(timezone.utc).isoformat(),'sources':[]}
    for key,url in SOURCES.items():
        response=requests.get(url,timeout=90);response.raise_for_status()
        target=OUT/(key+'.html');target.write_bytes(response.content)
        record={'id':key,'source_url':url,'path':target.relative_to(ROOT).as_posix(),
            'sha256':hashlib.sha256(response.content).hexdigest(),
            'kind':'public_official_guidance_not_statutory_provision','indexed':False}
        parser=Paragraphs();parser.feed(response.content.decode('utf-8'));lines=parser.lines
        if key=='electricity-cantho-guidance':
            relevant=[line for line in lines if line.startswith(('Đoàn kiểm tra cũng hướng dẫn người thuê trọ cách tính',
                'Tại các điểm giao dịch và thanh toán trung gian,'))]
            if len(relevant)!=2:raise ValueError('Guidance page structure changed; inspect original before cutting')
            text='\n\n'.join(relevant)
            if len(text.split())>200:raise ValueError('Review a shorter excerpt')
            excerpt=OUT/(key+'.txt');excerpt.write_text(text+'\n',encoding='utf-8')
            record.update(excerpt_path=excerpt.relative_to(ROOT).as_posix(),
                excerpt_sha256=hashlib.sha256(excerpt.read_bytes()).hexdigest(),indexed=True,
                limitation='Local guidance supports checking how electricity is charged; not a statutory article establishing a universal notification obligation or conditional commencement event.')
            print(text,flush=True)
        else:record['limitation']='Hanoi territorial rule: retained as research trace, excluded from Can Tho corpus; no cross-locality inference.'
        manifest['sources'].append(record)
    (OUT/'guidance_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

if __name__=='__main__':main()
