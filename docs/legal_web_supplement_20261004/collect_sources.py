"""Collect public legal originals and audit source links; does not index or run evals."""
from __future__ import annotations
import concurrent.futures, datetime, hashlib, html, json, pathlib, re, urllib.parse, urllib.request
from html.parser import HTMLParser
from pypdf import PdfReader

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = pathlib.Path(__file__).resolve().parent
DATE = '2026-10-04'

def source(id, title, url, role, note='', local=None, download=None):
    return dict(id=id, title=title, url=url, role=role, review_note=note,
                local_existing=local, download_url=download, accessed_date=DATE)

SOURCES = [
 source('civil91','Bộ luật Dân sự 91/2015/QH13','https://datafiles.chinhphu.vn/cpp/files/vbpq/2016/01/91.signed.pdf','primary_law','Bản ký; bản trích cũ có điều chưa đối chiếu từng chữ.','docs/legal_sources_originals_20261003/civil91first.pdf'),
 source('housing79','Văn bản hợp nhất 79/VBHN-VPQH — Luật Nhà ở','https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-79-vbhn-vpqh-469209.htm','primary_consolidation','Không coi ngày hợp nhất là ngày phát sinh hiệu lực của toàn bộ luật.'),
 source('broker29','Luật Kinh doanh bất động sản 29/2023/QH15','https://vanban.chinhphu.vn/?classid=1&docid=209624&pageid=27160&typegroupid=3','primary_law','Đối chiếu bản hợp nhất 06 và phạm vi dịch vụ môi giới chuyên nghiệp.'),
 source('broker06','Văn bản hợp nhất 06/VBHN-VPQH năm 2025 — Luật Kinh doanh bất động sản','https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-06-vbhn-vpqh-44399/55348.htm','primary_consolidation','Trang có mốc 01/01/1900: không sử dụng mốc này làm ngày hiệu lực.'),
 source('electricity60','Thông tư 60/2025/TT-BCT','https://congbao.chinhphu.vn/van-ban/thong-tu-so-60-2025-tt-bct-46756/60185.htm','primary_law','Điều 20–21 đặt điều kiện chuyển tiếp cho điểm c khoản 5 Điều 12; cần xác nhận mốc điều chỉnh giá bình quân.','docs/legal_fix_originals_20261004/electricity60.pdf'),
 source('electricity25','Thông tư 25/2018/TT-BCT','https://congbao.chinhphu.vn/tai-ve-van-ban-so-25-2018-tt-bct-27337-23871','primary_transition','Chỉ dùng phần được Điều 20 Thông tư 60 giữ trong chuyển tiếp; không tuyên bố cả thông tư vẫn còn hiệu lực.',download='https://congbao.chinhphu.vn/tai-ve-van-ban-so-25-2018-tt-bct-27337-23871?format=pdf'),
 source('electricity09','Thông tư 09/2023/TT-BCT — sửa quy định giá điện','https://congbao.chinhphu.vn/van-ban-dang-cong-bao/thong-tu-l3/trang-195.htm','primary_transition','Trang danh mục có nhiều văn bản: chỉ tải tệp mang số 09-2023-TT-BCT.'),
 source('electricity1279','Quyết định 1279/QĐ-BCT ngày 09/05/2025 — giá bán điện','https://vanban.chinhphu.vn/?classid=2&docid=213617&pageid=27160','primary_price_version','Biểu giá năm 2025; không tự nhận là giá của mọi kỳ hóa đơn năm 2026.',download='https://www.evn.com.vn/userfile/User/tcdl/files/2025/5/QD1279-QD-BCT-20250509163514982.pdf'),
 source('electricity133','Nghị định 133/2026/NĐ-CP — xử phạt lĩnh vực điện lực','https://vanban.chinhphu.vn/?docid=217612&pageid=27160','primary_law','Điều 4 khoản 3 về đối tượng mức phạt; Điều 13 khoản 7 và khoản 11 điểm c về thu thừa.','docs/legal_agent_originals_20261003/electricity133.pdf'),
 source('electricity_trigger','Bộ Công Thương: chưa áp dụng khung giờ điện mới — 22/05/2026','https://media.chinhphu.vn/bo-cong-thuong-chua-ap-dung-khung-gio-dien-moi-102260522073211616.htm','official_guidance','Chứng cứ theo ngày 22/05/2026, không chứng minh tình trạng mọi thời điểm sau đó.'),
 source('water215','Quyết định 215/QĐ-UBND Cần Thơ ngày 01/02/2024','https://capnuoccantho2.com.vn/View.aspx?wc=63&wp=332','local_price_original','Tệp ký được đơn vị cấp nước dẫn; kiểm tra vùng phục vụ và văn bản giá kỳ hóa đơn.','docs/legal_fix_originals_20261004/water215.pdf'),
 source('water_tariff2','Biểu giá nước sạch từ 02/2024 — Cấp nước Cần Thơ 2','https://capnuoccantho2.com.vn/View.aspx?wc=53&wp=331','provider_price_guidance','Giá đã VAT, chưa phí nước thải và dịch vụ môi trường rừng. Không có định mức 4 m³/người trong bảng này.'),
 source('water_provider1','Công ty Cổ phần Cấp thoát nước Cần Thơ','https://ctn-cantho.com.vn/','provider_official','Trang chính dẫn cổng hóa đơn, CTWCare và biểu giá từ 01/02/2024. Chọn đúng nhà cung cấp trên hóa đơn.'),
 source('water_invoice1','Cổng hóa đơn điện tử — Cấp thoát nước Cần Thơ','https://hddt.ctn-cantho.com.vn/','provider_procedure','Đường dẫn lấy từ trang chính đơn vị; không đăng nhập tài khoản của người dùng.'),
 source('water_invoice2','Hướng dẫn tra cứu hóa đơn — Cấp nước Cần Thơ 2','https://capnuoccantho2.com.vn/View.aspx?wc=78&wp=206','provider_procedure_historical','Hướng dẫn 2018, kiểm tra giao diện mới qua trang chính; không đưa mật khẩu mặc định cũ vào đáp án.'),
 source('water117','Nghị định 117/2007/NĐ-CP — sản xuất, cung cấp, tiêu thụ nước sạch','https://vanban.chinhphu.vn/?docid=33015&pageid=27160','primary_law','Đọc cùng 124/2011 và quy định địa phương. Điều 44/48/49/50 chủ yếu quan hệ đơn vị cấp nước–khách hàng, không phải công thức chia tiền giữa người thuê.'),
 source('water124','Nghị định 124/2011/NĐ-CP — sửa Nghị định 117','https://vanban.chinhphu.vn/?docid=153298&pageid=27160','primary_amendment'),
 source('residence68','Luật Cư trú 68/2020/QH14','https://congan.lamdong.gov.vn/UpLoaded/files/luat/68_2020_QH14.pdf','primary_law','Đọc cùng sửa đổi 118/2025; Điều 27/28 đăng ký tạm trú, Điều 30 lưu trú.'),
 source('residence116','Thông tư 116/2026/TT-BCA — đăng ký, quản lý cư trú','https://vanban.bocongan.gov.vn/co-so-du-lieu-van-ban/thong-tu-quy-dinh-chi-tiet-mot-so-dieu-va-bien-phap-thi-hanh-luat-cu-tru-1784261073','primary_law','Điều 3 khai thác dữ liệu, Điều 12 thay đổi nơi cư trú và trách nhiệm khi kết thúc thuê.','docs/legal_agent_originals_20261003/residence116.pdf'),
 source('residence_procedure_old','Trang thủ tục đăng ký tạm trú, mã 1.004194 — Bộ Công an','https://dichvucong.bocongan.gov.vn/bocongan/bothutuc/tthc?matt=26356','historical_procedure_excluded','Trang còn dẫn biểu mẫu/văn bản 2021; không dùng làm bộ hồ sơ hiện hành sau Thông tư 116.'),
 source('fire58','Văn bản hợp nhất 58/VBHN-VPQH năm 2026 — Luật PCCC và CNCH','https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-58-vbhn-vpqh-469188.htm','primary_consolidation','Điều 20/21/24; phân loại nhà ở, nhà ở kết hợp kinh doanh và công trình, không áp một danh mục kỹ thuật cho mọi nhà trọ.',download='https://congbaocdn.chinhphu.vn/180507251028987904/2026/4/9/469188-1775627122_v1_1775697185_signed.pdf'),
 source('fire69','Nghị định 69/2026/NĐ-CP — sửa Nghị định 106 về xử phạt PCCC','https://chinhphu.vn/?docid=217145&pageid=27160','primary_amendment','Cần đọc cùng 106/2025 và 347/2026 khi xác định chế tài.',download='https://congbaocdn.chinhphu.vn/180507251028987904/2026/3/20/469073-1774000375_v1_1774000947_signed.pdf'),
 source('fire1074','Quyết định 1074/QĐ-BXD ngày 29/06/2026 — giải pháp kỹ thuật nâng cao an toàn PCCC','https://moc.gov.vn/vn/Pages/ChiTietVanBan.aspx?TypeVB=1&vID=5019','primary_technical_decision','Chỉ áp dụng đúng nhóm cơ sở/công trình tồn tại trước Luật 55 có hiệu lực và không có khả năng khắc phục theo tiêu chuẩn; không áp đại trà.'),
 source('privacy91','Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15','https://bocongan.gov.vn/chinh-sach-phap-luat/co-so-du-lieu-van-ban/luat-bao-ve-du-lieu-ca-nhan-1753688803','primary_law','Hiệu lực 01/01/2026; Điều 3/4/9/10/16/19.','docs/legal_fix_originals_20261004/privacy91-cb.pdf'),
 source('privacy356','Nghị định 356/2025/NĐ-CP','https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-356-2025-nd-cp-468371.htm','primary_law','Điều 5 chia thời hạn theo loại yêu cầu; không gom tất cả thành 15 ngày. Điều 42 thay thế Nghị định 13/2023.','docs/legal_fix_originals_20261004/privacy356-cb.pdf'),
 source('commerce122','Luật Thương mại điện tử 122/2025/QH15','https://vanban.chinhphu.vn/?docid=216503&pageid=27160','primary_law','Điều 11 cần bổ sung; Điều 15/17 khác nghĩa vụ chung và nền tảng có chức năng đặt hàng.','docs/legal_agent_originals_20261003/ecommerce122.pdf'),
 source('commerce248','Nghị định 248/2026/NĐ-CP — hướng dẫn Luật Thương mại điện tử','https://vanban.chinhphu.vn/?docid=218747&pageid=27160','primary_law','Áp dụng sau khi xác định loại nền tảng và hoạt động thuộc phạm vi luật.','docs/legal_agent_originals_20261003/ecommerce248.pdf'),
 source('cantho_warning','Công an Cần Thơ cảnh giác các chiêu trò lừa đảo mùa tựu trường','https://bocongan.gov.vn/bai-viet/tp-can-tho-canh-giac-voi-cac-chieu-tro-lua-dao-mua-tuu-truong-1785748998','official_safety_advice','Khuyến cáo thực tế, không phải điều khoản luật; chỉ lưu diễn giải ngắn và đường dẫn.'),
 source('rental_warning','Bộ Công an cảnh giác lừa đảo đặt cọc thuê nhà trọ qua mạng','https://www.bocongan.gov.vn/bai-viet/canh-giac-voi-chieu-tro-lua-dao-dat-coc-thue-nha-tro-qua-mang-1782485063','official_safety_advice','Khuyến cáo thực tế; rủi ro không đồng nghĩa đã chứng minh tội phạm.'),
 source('criminal135','Văn bản hợp nhất 135/VBHN-VPQH — Bộ luật Hình sự','https://congbao.chinhphu.vn/tai-ve-van-ban-so-135-vbhn-vpqh-46165-58894?format=pdf','primary_consolidation','Điều 174/175: phải xét đầy đủ dấu hiệu, không định tội từ mỗi việc không trả cọc.'),
 source('procedure17','Văn bản hợp nhất 17/VBHN-VPQH — Bộ luật Tố tụng hình sự','https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-17-vbhn-vpqh-468961.htm','primary_consolidation','Điều 144–146: tiếp nhận tố giác, tin báo, thông tin và tài liệu chứng cứ.'),
 source('courts81','Nghị quyết 81/2025/UBTVQH15 — Tòa án nhân dân cấp tỉnh và khu vực','https://chinhphu.vn/?classid=1&docid=214391&pageid=27160','primary_institutional','Không tiếp tục chỉ dẫn mặc định TAND cấp huyện; kiểm tra đúng tòa theo thẩm quyền và địa bàn.'),
 source('lv_broker','LuatVietnam — Luật Kinh doanh bất động sản 29/2023/QH15','https://luatvietnam.vn/dat-dai/luat-kinh-doanh-bat-dong-san-cua-quoc-hoi-so-29-2023-qh15-284798-d1.html','secondary_law_mirror','Dùng đối chiếu văn bản công khai; ưu tiên bản ký/hợp nhất cơ quan nhà nước.'),
 source('lv_electricity','LuatVietnam — cách tính điện người thuê nhà, bài 04/12/2025','https://luatvietnam.vn/linh-vuc-khac/cach-tinh-tien-dien-sinh-hoat-cua-nguoi-thue-nha-tu-02-12-2025-the-nao-883-105708-article.html','secondary_explanation_conditional','Tiêu đề có ngày 02/12/2025; phải kiểm tra riêng điều kiện hiệu lực tại Điều 21 Thông tư 60.'),
 source('lv_electricity_fine','LuatVietnam — xử phạt thu tiền điện cao hơn quy định từ 25/05/2026','https://luatvietnam.vn/tin-van-ban-moi/tu-25-5-2026-chu-nha-thu-tien-dien-cua-nguoi-thue-cao-hon-quy-dinh-bi-phat-den-30-trieu-dong-186-108536-article.html','secondary_explanation','Đối chiếu Điều 4/13 Nghị định 133, không nhân đôi mức phạt tùy tiện.'),
 source('lv_old_tariff','LuatVietnam — bài điện nước nhà trọ dùng giá cũ','https://luatvietnam.vn/tin-phap-luat/cach-tinh-tien-dien-nuoc-nha-tro-theo-quy-dinh-moi-230-18375-article.html','historical_explanation_excluded','Giá điện và chế tài cũ; không nạp làm căn cứ giá hiện hành.'),
 source('lv_residence','LuatVietnam — Thông tư 116/2026/TT-BCA','https://luatvietnam.vn/tu-phap/thong-tu-116-2026-tt-bca-quy-dinh-chi-tiet-va-bien-phap-thi-hanh-luat-cu-tru-440199-d1.html','secondary_law_mirror'),
 source('lv_fire','LuatVietnam — Văn bản hợp nhất 58/VBHN-VPQH năm 2026','https://luatvietnam.vn/an-ninh-trat-tu/van-ban-hop-nhat-58-vbhn-vpqh-2026-luat-phong-chay-chua-chay-va-cuu-nan-cuu-ho-429517-d5.html','secondary_law_mirror'),
 source('lv_fire1074','LuatVietnam — Quyết định 1074/QĐ-BXD năm 2026','https://luatvietnam.vn/an-ninh-trat-tu/quyet-dinh-1074-qd-bxd-2026-giai-phap-ky-thuat-nang-cao-an-toan-phong-chay-chua-chay-cho-cong-trinh-khong-dat-yeu-cau-439953-d1.html','secondary_law_mirror'),
 source('lv_privacy','LuatVietnam — Nghị định 356/2025/NĐ-CP','https://luatvietnam.vn/dan-su/nghi-dinh-356-2025-nd-cp-quy-dinh-chi-tiet-luat-bao-ve-du-lieu-ca-nhan-422896-d1.html','secondary_law_mirror'),
 source('lv_commerce','LuatVietnam — Luật Thương mại điện tử 122/2025/QH15','https://luatvietnam.vn/thuong-mai/luat-thuong-mai-dien-tu-2025-so-122-2025-qh15-423356-d1.html','secondary_law_mirror','Điều 11 đối chiếu bản ký trước khi đưa trích nguyên văn vào corpus.'),
 source('lv_commerce248','LuatVietnam — Nghị định 248/2026/NĐ-CP','https://luatvietnam.vn/thuong-maai/nghi-dinh-248-2026-nd-cp-quy-dinh-chi-tiet-luat-thuong-mai-dien-tu-2026-439480-d1.html'.replace('thuong-maai','thuong-mai'),'secondary_law_mirror'),
 source('draft_electricity','Dự thảo sửa Thông tư 60 — công bố lấy ý kiến 2026','https://xaydungchinhsach.chinhphu.vn/toan-van-du-thao-thong-tu-sua-doi-bo-sung-thong-tu-so-60-2025-tt-bct-ve-thuc-hien-gia-ban-dien-119260528110732419.htm','draft_excluded','Không sử dụng dự thảo làm nghĩa vụ đã có hiệu lực.'),
]

class Links(HTMLParser):
    def __init__(self): super().__init__(); self.links=[]; self.href=None; self.label=[]
    def handle_starttag(self,tag,attrs):
        if tag=='a': self.href=dict(attrs).get('href'); self.label=[]
    def handle_data(self,data):
        if self.href is not None:self.label.append(data)
    def handle_endtag(self,tag):
        if tag=='a' and self.href is not None:
            self.links.append((self.href,''.join(self.label).strip()));self.href=None

def get(url):
    req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 Legal-document-source-audit'})
    with urllib.request.urlopen(req,timeout=25) as f:
        return f.read(),f.url,f.headers.get('Content-Type','')

def fetch(s):
    s=dict(s)
    if s['local_existing']:
        p=ROOT/s['local_existing']
        if p.exists():
            raw=p.read_bytes();s['original_sha256']=hashlib.sha256(raw).hexdigest();s['original_bytes']=len(raw)
    try:
        raw,final,ctype=get(s['url'])
        s.update(http_status='retrieved',resolved_url=final,response_sha256=hashlib.sha256(raw).hexdigest(),response_bytes=len(raw),content_type=ctype,retrieved_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
        # HTML used in memory only. Do not archive explanatory/news articles.
        parser=Links();parser.feed(raw.decode('utf-8',errors='replace')) if 'html' in ctype else None
        attachments=[]
        for href,label in parser.links:
            if re.search(r'\.(pdf|docx)(?:[?#]|$)',href,re.I):
                url=urllib.parse.urljoin(final,html.unescape(href))
                if (url,label) not in attachments:attachments.append((url,label))
        s['discovered_attachments']=[dict(url=u,label=l) for u,l in attachments]
        download=s['download_url']
        if not download and s['id'] in {'housing79','broker06','fire1074','electricity09'}:
            choices=attachments
            if s['id']=='electricity09':choices=[(u,l) for u,l in choices if re.search(r'09[-_/]2023',u+' '+l)]
            # DOCX gives an auditable native extraction; retain PDF for visual check as well.
            download=next((u for u,l in choices if '.docx' in u.lower()),None) or next((u for u,l in choices if '.pdf' in u.lower()),None)
        if download:
            data,durl,dtype=get(download)
            suffix='.pdf' if data.startswith(b'%PDF') else '.docx' if data.startswith(b'PK') else None
            if not suffix:raise ValueError('Download did not return PDF or DOCX; metadata preserved')
            p=OUT/'originals'/(s['id']+suffix);p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
            s.update(download_url=download,download_resolved_url=durl,original_path=p.relative_to(ROOT).as_posix(),original_sha256=hashlib.sha256(data).hexdigest(),original_bytes=len(data))
            if suffix=='.pdf':
                reader=PdfReader(p);pages=[x.extract_text() or '' for x in reader.pages]
                s.update(pages=len(pages),native_chars=sum(map(len,pages)),extraction='native_pdf_text_unreviewed' if any(pages) else 'scan_requires_manual_review')
                (OUT/'extracted').mkdir(exist_ok=True)
                (OUT/'extracted'/(s['id']+'.pages.json')).write_text(json.dumps(pages,ensure_ascii=False,indent=2),encoding='utf-8')
            else:
                import zipfile,xml.etree.ElementTree as ET
                with zipfile.ZipFile(p) as z:
                    el=ET.fromstring(z.read('word/document.xml'))
                    text='\n'.join(''.join(x.itertext()) for x in el.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'))
                (OUT/'extracted').mkdir(exist_ok=True)
                (OUT/'extracted'/(s['id']+'.txt')).write_text(text,encoding='utf-8')
                s.update(native_chars=len(text),extraction='native_docx_text_unreviewed')
    except Exception as e:s.update(fetch_error=f'{type(e).__name__}: {e}',http_status=s.get('http_status','failed'))
    return s

if __name__=='__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:records=list(pool.map(fetch,SOURCES))
    result=dict(version='legal-web-supplement-2026-10-04',accessed_date=DATE,source_policy='Primary law controls; mirrors are cross-checks, guidance is advice; no blanket claim of complete currency.',sources=records)
    (OUT/'sources.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    for s in records:print(s['id'],s['http_status'],s.get('original_path',''),s.get('fetch_error',''))
