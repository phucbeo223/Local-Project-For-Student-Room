"""Isolated extension of existing native Word, plus short publisher warnings."""
import json
from pathlib import Path
from urllib.request import Request, urlopen
import html
import re

import prepare_priority7_corpus as native

ROOT = native.ROOT
OUT = ROOT / 'docs/legal_word_repair_corpus_v14_20261006'


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    base=ROOT/'docs/legal_word_priority7_corpus_v13_20261006/manifest.json'
    entries=[]
    additions={'residence68-word':{'26','29'}, 'civil91-word':{'513','516','519','520'}}
    for entry in json.loads(base.read_text(encoding='utf-8'))['documents']:
        assert native.sha(ROOT/entry['file'])==entry['sha256']
        if entry['id'] not in additions:
            entries.append(entry);continue
        data=json.loads((ROOT/entry['file']).read_text(encoding='utf-8'))
        source=data['source'];word=ROOT/source['path'];assert native.sha(word)==source['sha256']
        body=native.read_word(word)
        parts=[p for p in native.structure_provisions(body,native.sha(word)) if p.article in additions[entry['id']]]
        assert {p.article for p in parts}==additions[entry['id']]
        for part in parts:
            assert part.content in body
            value=native.provision_json(part)
            value.update(page_from=1,page_to=1,extraction_text_sha256=native.hashlib.sha256(body.encode()).hexdigest())
            data['provisions'].append(value)
        if entry['id']=='residence68-word':
            source['source_scope_warning']+=' Điều 26 và 29 phải đọc đúng trường hợp điều chỉnh/xóa; không suy ra hạn nộp 30 ngày hoặc tự động xóa từ điều kiện sinh sống 30 ngày.'
        target=OUT/(entry['id']+'.json');native.save(target,data)
        entries.append(dict(entry,file=target.relative_to(ROOT).as_posix(),sha256=native.sha(target),provisions=len(data['provisions'])))
    native.OUT=OUT
    captures=ROOT/'eval/provider_sources_20261006/legal_repair';captures.mkdir(parents=True,exist_ok=True)
    sources=[
        ('online-secrets','https://www.bocongan.gov.vn/bai-viet/xuat-hien-thu-doan-lua-dao-moi-khi-mua-hang-online-1790562304',
         ['Tuyệt đối không cung cấp thông tin tài khoản, mật khẩu, mã OTP', 'không truy cập đường link lạ'],
         'Cảnh báo bảo mật và liên kết lạ — Bộ Công an',
         'Khuyến cáo trong bối cảnh mua hàng/hoàn tiền trực tuyến, áp dụng tham khảo phòng ngừa; không kết luận mọi link lạ là lừa đảo hoặc tự chứng minh một vụ nhận cọc.'),
        ('online-fake-link','https://www.bocongan.gov.vn/bai-viet/canh-bao-thu-doan-gia-danh-co-quan-cong-an-gui-tin-nhan-phat-nguoi-kem-duong-link-gia-mao-de-lua-dao-chiem-doat-tai-san-1788945012',
         ['đường link dẫn đến website giả mạo','thúc giục người dân thực hiện theo hướng dẫn'],
         'Nhận diện link giả và thúc ép — Bộ Công an',
         'Khuyến cáo trong bối cảnh giả danh phạt nguội, không gọi là vụ thuê trọ; đoạn trích nhận diện rủi ro, không phải quy định hay kết luận tội phạm.')]
    for key,url,literals,title,warning in sources:
        raw=captures/(key+'.html')
        if not raw.exists():
            with urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=45) as response:
                assert response.status==200 and response.url.startswith('https://www.bocongan.gov.vn/')
                raw.write_bytes(response.read())
        text=' '.join(html.unescape(re.sub(r'<[^>]+>',' ',raw.read_text(encoding='utf-8'))).split())
        assert sum(len(s.split()) for s in literals)<=25
        for i,literal in enumerate(literals):
            assert literal in text
            native.add_excerpt(entries,key+'-'+str(i)+'-word',title,'criminal_law',url,literal,native.sha(raw),warning,None)
    native.save(OUT/'manifest.json',dict(schema='legal_word_repair_v14_20261006',documents=entries,
        base_manifest_sha256=native.sha(base),expanded_native_articles={k:sorted(v) for k,v in additions.items()},
        policy='Isolated native Word extension; no answer keys, authored rules, housing statistics, OCR or PDF ingestion. Original references and active corpus unchanged.'))
    print(json.dumps(dict(documents=len(entries),manifest_sha256=native.sha(OUT/'manifest.json'))))


if __name__=='__main__':main()
