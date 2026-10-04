"""Build a reviewable supplementary material package, preserving the paused v15 corpus."""
from __future__ import annotations
import collections, datetime, hashlib, json, pathlib, re
from pypdf import PdfReader

ROOT=pathlib.Path(__file__).resolve().parents[2]
OUT=pathlib.Path(__file__).resolve().parent
BASELINE_SHA='db830c71bd0d4c9eed5ed5980f9538a43283bf66d671f917afacf94d953f28da'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def writejson(p,data):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def readjson(p):return json.loads(p.read_text(encoding='utf-8'))

def main():
    catalog=readjson(OUT/'sources.json');sources={s['id']:s for s in catalog['sources']}
    for p in sorted((OUT/'originals').glob('*.pdf')):
        if p.read_bytes()[:4]!=b'%PDF':raise ValueError('Not a PDF: '+str(p))
        pages=[x.extract_text() or '' for x in PdfReader(p).pages]
        writejson(OUT/'extracted'/(p.stem+'.pages.json'),pages)
        if p.stem not in sources:
            if p.stem=='fire1074-annex':
                s=dict(id=p.stem,title='Phụ lục Quyết định 1074/QĐ-BXD',url=sources['fire1074']['url'],role='primary_technical_annex',accessed_date='2026-10-04',review_note='Phạm vi riêng theo quyết định; bản quét không trích tự động.')
                catalog['sources'].append(s);sources[p.stem]=s
            else:raise ValueError('Unknown original '+p.stem)
        s=sources[p.stem]
        s.update(original_path=p.relative_to(ROOT).as_posix(),original_sha256=sha(p),original_bytes=p.stat().st_size,pages=len(pages),native_chars=sum(map(len,pages)),extraction='native_pdf_text_unreviewed' if any(pages) else 'scan_requires_manual_review')
        if p.stem in ['housing79','broker06','electricity25','electricity09']:
            choices=[a for a in s['discovered_attachments'] if a['label'].endswith('.pdf')]
            if p.stem=='electricity09':choices=[a for a in choices if '09-2023-TT-BCT' in a['label']]
            s.update(download_url=choices[0]['url'],download_status='retrieved_with_windows_tls_trust')
            s['previous_fetch_error']=s.pop('fetch_error',None)
        if p.stem.startswith('fire1074'):
            s.update(download_url='https://moc.gov.vn/Images/FileVanBan/BXD_1074-QD-BXD_29062026'+('_Phuluc' if p.stem.endswith('annex') else '')+'.pdf',download_status='retrieved_with_windows_tls_trust')
            s['previous_fetch_error']=s.pop('fetch_error',None)
    writejson(OUT/'sources.json',catalog)
    original=readjson(ROOT/'eval/datasets/external_legal_20261004/answers.json')
    editorial=readjson(OUT/'faq_content.json')
    comparison=readjson(ROOT/'eval/reports/external_legal_comparison_2026-10-04.json')
    questions={c['id']:c for c in original['cases']}
    assert [c['id'] for c in editorial['cases']]==list(range(1,37))
    faq=[]
    for c in editorial['cases']:
        c=dict(c,question=questions[c['id']]['question'],original_question_id=questions[c['id']]['original_question_id'],kind='editorial_guidance',evaluation_ground_truth=False)
        c['citations']=[dict(source_id=id,title=sources[id]['title'],url=sources[id]['url'],locator=loc,source_role=sources[id]['role']) for id,loc in c['citations']]
        assert any(x['source_role'].startswith(('primary','local_price','provider','official')) for x in c['citations'])
        faq.append(c)
    writejson(OUT/'faq_36.json',dict(version='legal-web-supplement-2026-10-04',status=editorial['status'],live_index_updated=False,cases=faq))
    # Exact provisions already available in the corpus, linked as immutable review candidates.
    select={
      'legacy-e010a14386b4':['119','328','385','398','401','421','472','473','477','479','481','482','360'],
      'legacy-4bcf6ab450b3':['160','161','163','164','170','171','172'],
      'legacy-97260a1a9fb2':['44','46','61','63','65'],
      'civil-service-contract':['513','514','515','516','517','518','519'],
      'electricity60':['12','20','21'],'electricity133':['4','13'],
      'water117':['44','48','49','50','54'],
      'water124':['1'], 'water215':['1','2','3'],
      'legacy-101ff31eaab8':['9','27','28','30'],
      'residence116':['3','6','12'],
      'privacy91-cb':['3','4','9','10','16','19','38'],
      'privacy356-cb':['5','42'],
      'ecommerce122':['1','3','5','15','17','40'],
      'ecommerce248':['17','18'],
      'legacy-c689645e534f':['174','175'],
      'legacy-95df8751459d':['144','145','146'],
      'fire105-annex-I':None,
      'electricity-cantho-guidance':None,
    }
    reuse=[]
    for id,arts in select.items():
        p=ROOT/'docs/legal_corpus_v2'/(id+'.json');d=readjson(p)
        prov=[v for v in d['provisions'] if arts is None or v['article'] in arts]
        found={v['article'] for v in prov}
        reuse.append(dict(source_id=id,source_file=p.relative_to(ROOT).as_posix(),source_file_sha256=sha(p),source=d['source'],provision_ids=[v['provision_id'] for v in prov],articles_found=sorted(found),requested_articles_not_in_existing_selection=sorted(set(arts or [])-found),verification='inherited_from_existing_corpus_not_new_full_word_verification'))
    writejson(OUT/'existing_evidence_map.json',dict(documents=reuse))
    reviewed=readjson(OUT/'reviewed_new_provisions.json') if (OUT/'reviewed_new_provisions.json').exists() else dict(provisions=[])
    # Ready-to-review exact supplemental excerpts; activate only with a new corpus/eval version.
    candidates=collections.defaultdict(list)
    for item in reviewed['provisions']:
        v=dict(item)
        assert v['source_id'] in sources
        for image in v['review_images']:
            assert (OUT/image).is_file(), image
        v.update(kind=v.get('kind','legal_provision'),content_sha256=hashlib.sha256(v['content'].encode('utf-8')).hexdigest(),page_kind='physical_pdf',verification='listed_excerpt_visually_checked_against_original',source_start=None,source_end=None,not_exhaustive=True)
        v['provision_id']=f"web20261004:{v['source_id']}:{v['article']}:{v['clause']}"
        candidates[v['source_id']].append(v)
    candidate_manifest=[]
    for id,provisions in candidates.items():
        s=sources[id];file=OUT/'candidate_corpus'/(id+'.json')
        source_metadata=dict(id='web20261004-'+id,title=s['title'],source_url=s['url'],download_url=s.get('download_url'),path=s.get('original_path') or s.get('local_existing'),sha256=s.get('original_sha256'),extraction='manual_verified_excerpt_transcription',not_exhaustive=True,verification=reviewed['verification_policy'],activation_status='candidate_not_indexed',category='review_before_category_assignment')
        writejson(file,dict(source=source_metadata,provisions=provisions))
        candidate_manifest.append(dict(id=source_metadata['id'],file=file.relative_to(ROOT).as_posix(),sha256=sha(file),provisions=len(provisions)))
    writejson(OUT/'candidate_corpus'/'manifest.json',dict(version='legal-web-supplement-2026-10-04',status='candidate_not_indexed',documents=candidate_manifest,policy='Preserve parent clauses and applicability; assign category and review effective periods before activation. Editorial FAQ is not statute or model ground truth.'))
    new_docs=[]
    for id in ['housing79','broker06','electricity25','electricity09','fire58','fire69','water57']:
        p=OUT/'extracted'/(id+'.pages.json')
        if p.exists():
            pages=readjson(p)
            # Native extraction retained as supporting original, not labelled all legally reviewed.
            new_docs.append(dict(source_id=id,file=p.relative_to(ROOT).as_posix(),sha256=sha(p),pages=len(pages),native_chars=sum(map(len,pages)),status='native_text_supporting_original_not_live_index',reviewed_articles=[x['article'] for x in reviewed['provisions'] if x['source_id']==id]))
    current=sha(ROOT/'docs/legal_corpus_v2/manifest.json')
    counts=dict(faq_cases=len(faq),catalog_sources=len(sources),luatvietnam_sources=sum(s['url'].startswith('https://luatvietnam.vn/') for s in sources.values()),downloaded_original_pdfs=len(list((OUT/'originals').glob('*.pdf'))),existing_evidence_documents=len(reuse),existing_provision_references=sum(len(d['provision_ids']) for d in reuse),new_reviewed_provisions=len(reviewed['provisions']))
    manifest=dict(version='legal-web-supplement-2026-10-04',created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),purpose='Bổ sung nguồn và giải thích có căn cứ cho 36 câu thuê trọ; tách khỏi bản đánh giá v15 đang tạm dừng.',live_index_updated=False,model_evaluations_run=False,baseline_manifest_sha256=BASELINE_SHA,current_legal_v2_manifest_sha256=current,baseline_preserved=current==BASELINE_SHA,counts=counts,faq_file='docs/legal_web_supplement_20261004/faq_36.json',sources_file='docs/legal_web_supplement_20261004/sources.json',existing_evidence_file='docs/legal_web_supplement_20261004/existing_evidence_map.json',new_original_texts=new_docs,reviewed_provisions_file='docs/legal_web_supplement_20261004/reviewed_new_provisions.json',not_indexable_as_statute=['editorial_guidance','secondary_explanation','provider_procedure_historical','historical_explanation_excluded','historical_procedure_excluded','draft_excluded'])
    writejson(OUT/'manifest.json',manifest)
    lines=['# Bổ sung tài liệu pháp lý thuê trọ — 04/10/2026','',f"Đã lập tài liệu cho **36/36 câu**, danh mục **{len(sources)} nguồn** (gồm **{counts['luatvietnam_sources']} trang LuatVietnam**) và lưu **{counts['downloaded_original_pdfs']} PDF bổ sung**. Nội dung được biên soạn theo nguồn, không coi đáp án bên ngoài là chuẩn pháp lý.",'','Tài liệu này được lưu độc lập. Chưa cập nhật chỉ mục truy xuất đang chạy; chưa chạy lại đánh giá mô hình. Bản v15 và yêu cầu tạm dừng được giữ để lần đánh giá sau dùng phiên bản mới, tránh trộn kết quả.','','## Cách đọc và sử dụng nguồn','','- Bản ký, Công báo và cơ quan ban hành là căn cứ chính; LuatVietnam dùng đối chiếu và giải thích, không thay căn cứ gốc.','- Mỗi câu có căn cứ và điều/khoản, phần áp dụng/khuyến nghị riêng, cùng điểm sửa đáp án bên ngoài.','- Dữ liệu gốc lưu mã SHA-256, đường dẫn, ngày truy cập và trạng thái tải. Bài giải thích chỉ lưu đường dẫn, ghi chú ngắn; không sao chép nguyên bài.','- Ngày truy cập không phải xác nhận mọi văn bản đã được rà soát toàn bộ lịch sử hiệu lực. Giá điện/nước phải kiểm tra theo kỳ hóa đơn, địa chỉ và nhà cung cấp.','','## Những bổ sung và sửa quan trọng','','1. Hợp đồng/cọc: thêm nội dung bắt buộc, cọc tùy thỏa thuận, ngoại lệ tăng giá do cải tạo; không hứa hoàn cọc chỉ vì báo trước 30 ngày.','2. Điện: thêm cặp quy định chuyển tiếp Thông tư 25/09 và Điều 20–21 Thông tư 60; bản giá 1279 được ghi phiên bản. Chế tài đọc theo Nghị định 133 và đối tượng mức phạt.','3. Nước: thêm bảng công khai và cổng hóa đơn của đơn vị cấp nước; tách hợp đồng cấp nước với thỏa thuận chia tiền trong nhà trọ.','4. Cư trú: thêm trách nhiệm chủ trọ khi kết thúc thuê, cách khai thác dữ liệu theo Thông tư 116; loại hướng dẫn thủ tục còn dẫn mẫu cũ.','5. PCCC: bổ sung Luật hợp nhất 58, Nghị định sửa đổi 69 và Quyết định 1074 có phạm vi riêng; phân loại trước khi áp yêu cầu kỹ thuật.','6. Môi giới: thêm hình thức/nội dung hợp đồng, công khai trung thực hồ sơ theo Điều 44/46/61/65; tách môi giới chuyên nghiệp và giới thiệu dân sự.','7. Nền tảng: thêm Điều 11 về kênh phản ánh; phân biệt loại nền tảng và chức năng đặt hàng trước khi áp nghĩa vụ.','8. Dữ liệu cá nhân: dùng Luật 91 và Nghị định 356; tách thời hạn ngừng xử lý/chỉnh sửa/xóa, ngoại lệ có căn cứ hợp pháp.','9. Lừa đảo: thêm cảnh báo thuê trọ tại Cần Thơ, hồ sơ tố giác và phân biệt rủi ro–tranh chấp–dấu hiệu tội phạm.','','## Các điểm còn phải xác nhận khi áp dụng','','- Điện: mốc điều chỉnh giá bình quân kích hoạt một số phần Thông tư 60; biểu giá thật của kỳ hỏi. Tin tháng 05/2026 không chứng minh tình trạng mọi tháng sau đó.','- Nước: nhà cung cấp, vùng phục vụ và quyết định giá tại địa chỉ cụ thể; không áp bảng 215 cho mọi địa bàn Cần Thơ sau sắp xếp.','- PCCC: số tầng, diện tích, mục đích sử dụng, thời điểm công trình và các sửa đổi chế tài trước khi kết luận đủ điều kiện hoặc mức phạt.','- Thủ tục: dùng biểu mẫu đang được cơ quan cư trú tiếp nhận; trang hướng dẫn cũ được đánh dấu loại khỏi căn cứ hiện hành.','- Corpus cũ có OCR/trích tuyển chưa kiểm tra từng chữ. Hồ sơ kế thừa ghi đúng hạn chế này, không đổi nhãn thành đã xác minh toàn bộ.','','## Bổ sung theo từng câu','']
    # Keep the package navigation explicit, with local files clickable in the desktop app.
    navigation=['## Hồ sơ đã lưu','',
      f"- [Danh mục nguồn và giới hạn sử dụng]({(OUT/'SOURCES.md').as_posix()})",
      f"- [Đối chiếu 36 câu với đáp án hệ thống đã lưu]({(OUT/'SYSTEM_CROSSCHECK.md').as_posix()})",
      f"- [Nội dung 36 câu dạng JSON]({(OUT/'faq_36.json').as_posix()})",
      f"- [20 đoạn/bảng có ảnh đối chiếu]({(OUT/'reviewed_new_provisions.json').as_posix()})",
      f"- [Manifest bộ trích ứng viên, chưa nạp chỉ mục]({(OUT/'candidate_corpus'/'manifest.json').as_posix()})",'']
    position=lines.index('## Bổ sung theo từng câu')
    lines[position:position]=navigation
    for c in faq:
        lines += [f"### Câu {c['id']}. {c['question']}",'',c['answer'],'',f"**Kiểm tra thực tế:** {c['practical']}",'',f"**Điểm sửa đáp án bên ngoài:** {c['correction']}",'','**Căn cứ:**','']
        for ref in c['citations']:lines.append(f"- [{ref['title']}]({ref['url']}) — {ref['locator']}.")
        lines.append('')
    (OUT/'README.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    sourcelines=['# Danh mục nguồn minh bạch — 04/10/2026','','Mã nguồn được dùng trong faq_36.json. Phân loại phản ánh vai trò và giới hạn; trạng thái tải không phải xác nhận toàn bộ hiệu lực.','']
    for s in catalog['sources']:
        sourcelines += [f"## {s['id']} — {s['title']}",'',f"- Trang nguồn: [{s['title']}]({s['url']})",f"- Vai trò: `{s['role']}`; truy cập: {s['accessed_date']}; tải trang: `{s.get('http_status','n/a')}`."]
        if s.get('download_url'):sourcelines.append(f"- Tệp gốc: [tải văn bản]({s['download_url']}).")
        local=s.get('original_path') or s.get('local_existing')
        if local:sourcelines.append(f"- Bản lưu: [{pathlib.Path(local).name}]({(ROOT/local).as_posix()}); SHA-256: `{s.get('original_sha256','chưa có')}`.")
        if s.get('review_note'):sourcelines.append('- Giới hạn: '+s['review_note'])
        if s.get('fetch_error'):sourcelines.append('- Lỗi tải được giữ minh bạch: '+s['fetch_error'])
        sourcelines.append('')
    (OUT/'SOURCES.md').write_text('\n'.join(sourcelines)+'\n',encoding='utf-8')
    auditlines=['# Đối chiếu bổ sung với đáp án hệ thống đã lưu','','Đối chiếu tài liệu với bản local v15 cũ; không chạy lại hệ thống, không chấm điểm đúng/sai bằng mô hình. Các ghi nhận dưới đây lấy từ hồ sơ so sánh đã lưu và gắn với phần bổ sung mới.','','| Câu | Ghi nhận ở đáp án hệ thống local v15 | Bổ sung / điều chỉnh nguồn |','|---|---|---|']
    for old,c in zip(comparison['cases'],faq):
        assert old['id']==c['id']
        obs=old['review']['system_observation'].replace('|','\\|').replace('\n',' ')
        adjustment=old['review']['suggested_action'].replace('|','\\|').replace('\n',' ')
        refs='; '.join(f"[{r['source_id']}]({r['url']})" for r in c['citations'])
        auditlines.append(f"| {c['id']} | {obs} | {adjustment} Nguồn: {refs}. |")
    auditlines += ['','Các câu 10, 11, 21, 24, 25, 26, 27 cần sửa lựa chọn/phạm vi nguồn, không chỉ thêm số lượng tài liệu. Bộ bổ sung đã cung cấp căn cứ và phần diễn giải theo câu; hiệu quả truy xuất chưa được đánh giá lại vì các lượt đánh giá đang tạm dừng.','']
    (OUT/'SYSTEM_CROSSCHECK.md').write_text('\n'.join(auditlines),encoding='utf-8')
    print(json.dumps(manifest['counts'],ensure_ascii=False))
    print('baseline_preserved',manifest['baseline_preserved'])

if __name__=='__main__':main()
