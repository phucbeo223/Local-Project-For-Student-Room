"""Add related official sources from existing provenance, without changing the live corpus."""
import json, pathlib
from collect_sources import OUT, ROOT, fetch, source
from pypdf import PdfReader

if __name__=='__main__':
    p=OUT/'sources.json';catalog=json.loads(p.read_text(encoding='utf-8'));seen={x['id'] for x in catalog['sources']}
    extra=[source('water57','Văn bản hợp nhất 57/VBHN-BXD ngày 30/06/2026 — hướng dẫn Nghị định 117','https://vanban.chinhphu.vn/?docid=218699&pageid=27160','primary_guidance','Hợp nhất Thông tư 01/2008 được sửa bởi 09/2025; không nhầm là bản hợp nhất chính Nghị định 117. Mẫu hợp đồng chỉ dùng đúng quan hệ đơn vị cấp nước–khách hàng.','docs/legal_agent_originals_20261003/water57.pdf')]
    for id,newid,role in [('fire105-annex-I','fire105','primary_law'),('amend118','amend118','primary_amendment'),('amend347','amend347','primary_amendment'),('fire106','fire106','primary_law'),('legacy-3c1db7d7a4f0','privacy330','primary_law'),('electricity-cantho-guidance','electricity_cantho','official_guidance'),('residence154','residence154','primary_law')]:
        d=json.loads((ROOT/'docs/legal_corpus_v2'/(id+'.json')).read_text(encoding='utf-8'))['source']
        extra.append(source(newid,d['title'],d['source_url'],role,'Nguồn có trong hồ sơ hiện tại; bản trích và giới hạn kiểm chứng được giữ trong existing_evidence_map. Đọc đúng phạm vi và văn bản sửa đổi.',d.get('path')))
    for s in extra:
        if s['id'] not in seen:
            r=fetch(s);catalog['sources'].append(r);print(r['id'],r['http_status'],r.get('fetch_error',''))
    water=next(x for x in catalog['sources'] if x['id']=='water57')
    pages=[x.extract_text() or '' for x in PdfReader(ROOT/water['local_existing']).pages]
    (OUT/'extracted'/'water57.pages.json').write_text(json.dumps(pages,ensure_ascii=False,indent=2),encoding='utf-8')
    water.update(extraction='native_pdf_text_section_structure_not_live_index',pages=len(pages),native_chars=sum(map(len,pages)))
    p.write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    f=OUT/'faq_content.json';d=json.loads(f.read_text(encoding='utf-8'))
    for c in d['cases']:
        for cite in c['citations']:
            if cite[0]=='residence116':cite[1]=cite[1].replace('Điều 3 khoản 6','Điều 3 khoản 5–6')
            if c['id']==9 and cite[0]=='water117':cite[1]='Điều 54; giá địa phương đối chiếu Quyết định 215'
            if c['id']==16 and cite[0]=='residence68':cite[1]='Điều 27, 28; đọc cùng sửa đổi 118/2025'
        if c['id']==8:c['citations'].append(['electricity_cantho','Hướng dẫn thực tế về minh bạch bảng tính; phân biệt với nghĩa vụ luật định'])
        if c['id'] in [10,11,12]:c['citations'].append(['water57','Mục VI về hợp đồng dịch vụ cấp nước; Mục VII kiểm định, chỉ đúng quan hệ cấp nước'])
        if c['id'] in [13,14,15,16]:c['citations'].append(['amend118','Sửa đổi Luật Cư trú; đọc cùng bản luật gốc'])
        if c['id']==15:c['citations'].append(['residence154','Quy định chi tiết chứng minh chỗ ở hợp pháp; đối chiếu dữ liệu đã khai thác được'])
        if c['id'] in [17,18]:c['citations'].append(['fire105','Phụ lục I, phân loại cơ sở và quy mô'])
        if c['id']==19:
            c['citations'] += [['fire106','Nghị định xử phạt, đọc cùng sửa đổi'],['amend347','Các sửa đổi chế tài liên quan; không áp bản cũ độc lập']]
        if c['id']==32:c['citations'].append(['privacy330','Chế tài phải theo hành vi và đối tượng, không tự chọn mức phạt chung'])
        if c['id']==9 and 'Bản ký còn có bảng riêng' not in c['answer']:
            c['answer'] += ' Bản ký còn có bảng riêng cho Trung tâm Nước sạch và Vệ sinh môi trường nông thôn (nhóm thông thường 7.450 đồng/m³ năm 2024), vì vậy phải kiểm tra đúng đơn vị cung cấp.'
        c['citations'] = [list(x) for x in dict.fromkeys(tuple(x) for x in c['citations'])]
    f.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
