"""Extend v14 with native official residence Word; keep superseded clauses out."""
from pathlib import Path
import shutil
import json
import prepare_priority7_corpus as native

ROOT=native.ROOT
OUT=ROOT/'docs/legal_word_repair_corpus_v16_20261006'


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    base=ROOT/'docs/legal_word_repair_corpus_v14_20261006/manifest.json'
    entries=[]
    for entry in json.loads(base.read_text(encoding='utf-8'))['documents']:
        assert native.sha(ROOT/entry['file'])==entry['sha256']
        if entry['id']!='residence68-word':
            entries.append(entry);continue
        data=json.loads((ROOT/entry['file']).read_text(encoding='utf-8'))
        body=native.read_word(ROOT/data['source']['path'])
        additions=[p for p in native.structure_provisions(body,data['source']['sha256']) if p.article=='23']
        assert additions
        for p in additions:
            assert p.content in body
            v=native.provision_json(p)
            v.update(page_from=1,page_to=1,extraction_text_sha256=native.hashlib.sha256(body.encode()).hexdigest())
            data['provisions'].append(v)
        target=OUT/(entry['id']+'.json');native.save(target,data)
        entries.append(dict(entry,file=target.relative_to(ROOT).as_posix(),sha256=native.sha(target),provisions=len(data['provisions'])))
    specs=[
        ('residence154-official-word','nd154.doc','Nghị định 154/2024/NĐ-CP — Word Công báo',
         'https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-154-2024-nd-cp-43275.htm',
         {('5','1')},'2025-01-10',
         'Chỉ giữ khoản 1 Điều 5 về khai thác thông tin và yêu cầu giấy tờ khi không khai thác được dữ liệu. Không giữ điểm a khoản 3 Điều 5 và Điều 10 bản cũ vì đã sửa bởi Nghị định 58/2026/NĐ-CP.'),
        ('residence58-official-word','nd58.docx','Nghị định 58/2026/NĐ-CP — Word Công báo',
         'https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-58-2026-nd-cp-468975/62899.htm',
         {('4','2'),('4','5'),('4','7'),('6','1'),('6','2')},'2026-03-15',
         'Khoản 2, 5, 7 Điều 4 sửa điểm a khoản 3 Điều 5, khoản 5 Điều 8 và Điều 10 Nghị định 154/2024/NĐ-CP. Giữ nguyên điều kiện, chủ thể và dẫn chiếu; không coi mọi chuyển trọ đều phải nộp hồ sơ xóa trong 7 ngày. Khoản 2 Điều 6 có mốc hiệu lực riêng cho người chưa thành niên, phần đó không được trích tuyển ở đây.')]
    for key,name,title,url,chosen,effective,warning in specs:
        word=OUT/name
        shutil.copyfile(Path('/eval/provider_sources_20261006/residence_native')/name,word)
        body=native.read_word(word);digest=native.sha(word)
        parts=[p for p in native.structure_provisions(body,digest) if (p.article,p.clause) in chosen]
        assert {(p.article,p.clause) for p in parts}==chosen
        provisions=[]
        for p in parts:
            assert p.content in body
            v=native.provision_json(p)
            v.update(page_from=1,page_to=1,extraction_text_sha256=native.hashlib.sha256(body.encode()).hexdigest())
            provisions.append(v)
        source=dict(id=key,title=title,category='residence',path=word.relative_to(ROOT).as_posix(),
            sha256=digest,original_sha256=digest,source_url=url,publisher='Công báo Chính phủ',
            effective_date=effective,page_kind='logical_document',pages=1,ocr_used=False,
            extraction='Native official Word XML/antiword; no PDF or OCR',source_content_kind='published_word',
            source_scope_warning=warning,not_exhaustive=True,
            source_policy='Exact official Word clauses, no answer keys or authored legal summaries.')
        target=OUT/(key+'.json');native.save(target,dict(source=source,provisions=provisions))
        entries.append(dict(id=key,file=target.relative_to(ROOT).as_posix(),sha256=native.sha(target),category='residence',provisions=len(provisions)))
    native.save(OUT/'manifest.json',dict(schema='legal_word_repair_v16_20261006',documents=entries,
        base_manifest_sha256=native.sha(base),policy='Isolated native official Word extension, unchanged original references and active store; no OCR/PDF/forms/housing statistics.'))
    print(json.dumps(dict(documents=len(entries),manifest_sha256=native.sha(OUT/'manifest.json'))))


if __name__=='__main__':main()
