"""Build the requested local knowledge supplement; never index or evaluate models."""
from pathlib import Path
from datetime import datetime, timezone
import concurrent.futures
import hashlib
import json
import re
import shutil
import urllib.request
from pypdf import PdfReader, PdfWriter

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / 'docs/legal_web_supplement_20261004'
OUT = BASE / 'extension_10_topics'
DATE = '2026-10-04'
ATTACHMENT = Path('C:/Users/Admin/.codex/attachments/d526a5a2-949e-4073-8a7c-686f5d15be14/Văn bản đã dán.txt')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def save(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + '\n', encoding='utf-8')

def dump(path, obj):
    save(path, json.dumps(obj, ensure_ascii=False, indent=2))

def link(path, label):
    return f'[{label}]({path.resolve().as_posix()})'

sources = {s['id']: s for s in json.loads((BASE / 'sources.json').read_text(encoding='utf-8'))['sources']}
faq = json.loads((BASE / 'faq_36.json').read_text(encoding='utf-8'))['cases']
reviewed = json.loads((BASE / 'reviewed_new_provisions.json').read_text(encoding='utf-8'))['provisions']

extra_sources = [
    ('cantho_police_contacts', 'Công an Cần Thơ — đường dây nóng', 'https://congan.cantho.gov.vn/page/', 'primary_public_directory'),
    ('cantho_water_contacts', 'Cấp thoát nước Cần Thơ — liên hệ', 'https://ctn-cantho.com.vn/contact/', 'provider_public_directory'),
    ('evnspc_contacts', 'Trung tâm CSKH Điện lực miền Nam', 'https://cskh.evnspc.vn/Home/Index', 'provider_public_directory'),
    ('cantho_fire_call', 'Công an Cần Thơ — chủ động phòng ngừa cháy, nổ', 'https://congan.cantho.gov.vn/phong-chay-chua-chay/chu-dong-phong-ngua-chay-no-tu-nhung-viec-lam-nho-hang-ngay-9651.html', 'primary_safety_guidance'),
    ('national112', 'Báo điện tử Chính phủ — tổng đài khẩn cấp quốc gia 112', 'https://xaydungchinhsach.chinhphu.vn/tong-dai-so-112-tiep-nhan-24-7-cac-thong-tin-ve-su-co-thien-tai-tham-hoa-119250902150528929.htm', 'government_public_guidance'),
    ('fire_directive19', 'Chỉ thị 19/CT-TTg ngày 24/06/2024 — tăng cường PCCC', 'https://chinhphu.vn/?classid=2&docid=210485&pageid=27160', 'primary_directive_metadata'),
    ('fire_standard3890', 'VSQI — danh mục TCVN 3890:2023', 'https://tieuchuan.vsqi.gov.vn/tieuchuan/view?sohieu=TCVN+3890%3A2023', 'official_standard_catalog'),
]

cached = {}
if (OUT / 'sources.json').exists():
    cached = {s['id']: s for s in json.loads((OUT / 'sources.json').read_text(encoding='utf-8-sig'))['sources']}

def capture(item):
    sid, title, url, role = item
    if sid in cached and cached[sid].get('http_status') == 200 and cached[sid].get('url') == url:
        return cached[sid]
    rec = dict(id=sid, title=title, url=url, role=role, accessed_date=DATE,
               verification='Nội dung chọn lọc đã đối chiếu trang công khai; không xác nhận toàn văn. Số điện thoại nếu có chưa gọi thử.',
               full_article_saved=False)
    if sid == 'fire_standard3890':
        rec['review_note'] = 'Chỉ xác minh danh mục, tên và tình trạng tiêu chuẩn; chưa lưu/đọc toàn bộ nội dung kỹ thuật của tiêu chuẩn.'
    if sid == 'fire_directive19':
        rec['review_note'] = 'Chỉ thị ngày 24/06/2024 là văn bản chỉ đạo; không dùng thay luật/nghị định mới hoặc kết luận yêu cầu kỹ thuật mọi nhà trọ.'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (legal source verification)'})
        with urllib.request.urlopen(req, timeout=30) as response:
            body = response.read()
            rec.update(http_status=response.status, resolved_url=response.geturl(),
                       response_sha256=hashlib.sha256(body).hexdigest(), response_bytes=len(body),
                       retrieved_at_utc=datetime.now(timezone.utc).isoformat())
    except Exception as exc:
        rec.update(http_status='fetch_failed', fetch_error=str(exc),
                   retrieval_note='Đã đọc bằng công cụ duyệt web; lần tải lưu mã băm riêng chưa thành công.')
    return rec

OUT.mkdir(parents=True, exist_ok=True)
raw = OUT / 'user_original.txt'
shutil.copyfile(ATTACHMENT, raw)
dump(OUT / 'user_original.metadata.json', dict(source_path=str(ATTACHMENT), sha256=sha(raw),
     bytes=raw.stat().st_size, kind='unverified_user_suggestion', preserved_verbatim=True,
     exclusion='Không tạo biểu mẫu hợp đồng thuê, môi giới hoặc hợp đồng khác.'))

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    captures = list(pool.map(capture, extra_sources))
for rec in captures:
    sources[rec['id']] = rec

# Preserve the official CT01 pages and all instructions, without redrawing a form.
origin = ROOT / 'docs/legal_agent_originals_20261003/residence116.pdf'
reader = PdfReader(origin)
writer = PdfWriter()
for index in (19, 20):
    writer.add_page(reader.pages[index])
writer.add_metadata({'/Title': 'CT01 — Thông tư 116/2026/TT-BCA — trích trang 20–21',
                     '/Subject': 'Bản trích từ PDF gốc Bộ Công an; giữ tờ khai và chú thích'})
form = ROOT / 'Data/residence/CT01-116-2026-trich-ban-goc.pdf'
with form.open('wb') as stream:
    writer.write(stream)
dump(OUT / 'ct01_provenance.json', dict(kind='official_form_extract', source_id='residence116',
     original_path=origin.relative_to(ROOT).as_posix(), original_sha256=sha(origin),
     source_url=sources['residence116']['url'],
     download_url='https://bocongan.gov.vn/media/bca-media/library-20260717110413-0c32870e-3f4d-41d8-9da4-8f90638543ff-thong-tu-116-2026.pdf',
     physical_pages_one_based=[20, 21], output_path=form.relative_to(ROOT).as_posix(),
     output_sha256=sha(form), output_pages=2, altered_page_content=False,
     visual_review_images=['qa/ct01-full-20.png', 'qa/ct01-full-21.png'],
     verification='Đã đọc trực tiếp cả hai ảnh trang; bản trích giữ nguyên nội dung trang.'))

topics = [
    ('housing_contract', 'Hợp đồng thuê và tiền cọc', range(1, 5),
     ['civil91', 'housing79'],
     'Giữ kiến thức về quyền, nghĩa vụ và xử lý cọc. Các bên tự lập hợp đồng; tài liệu này chỉ là hướng dẫn kiểm tra và căn cứ pháp luật.',
     'Không có một mức cọc, thời hạn hoàn cọc 3–5 ngày hay quyền nhận lại cọc chỉ vì báo trước 30 ngày áp dụng chung. Khi bàn giao, nên lưu ảnh, danh sách tài sản, công nợ và xác nhận đã nhận chìa khóa; đây là khuyến nghị chứng cứ, không phải mẫu hợp đồng.', []),
    ('electricity', 'Tiền điện phòng trọ', range(5, 9),
     ['electricity25', 'electricity09', 'electricity60', 'electricity133', 'electricity1279', 'electricity_cantho', 'lv_electricity', 'lv_electricity_fine'],
     'Chọn quy định theo kỳ hóa đơn và điều kiện chuyển tiếp tại Điều 20–21 Thông tư 60/2025/TT-BCT. Quyết định 1279 là bảng phiên bản 09/05/2025, không gắn nhãn giá mới nhất mọi thời điểm.',
     'Nhánh kê khai số người đủ điều kiện: 1 người = 1/4; 2 người = 1/2; 3 người = 3/4; 4 người = 1 định mức hộ. Với định mức bậc i của hộ là D_i, định mức nhóm N người là (N/4) × D_i trong nhánh áp dụng. Nếu không kê khai được số người trong nhánh tương ứng, dùng giá bậc 3 cho toàn bộ sản lượng theo quy định, không tự lấy giá này cho mọi phòng. Mức phạt phải đọc Nghị định 133/2026, Điều 13 khoản 7, khoản 11 và quy định đối tượng tại Điều 4; không dùng Nghị định 17/2022 làm căn cứ duy nhất.',
     [('electricity09', '2', '2')]),
    ('water_cantho', 'Nước sinh hoạt tại Cần Thơ', range(9, 13),
     ['water215', 'water_tariff2', 'water_provider1', 'water_invoice1', 'water_invoice2', 'water57', 'civil91'],
     'Áp dụng theo đơn vị cấp nước, địa bàn phục vụ, nhóm sử dụng và kỳ hóa đơn. Bảng công khai từ 01/02/2024 là dữ liệu có phiên bản, không đại diện mọi địa chỉ Cần Thơ sau sắp xếp.',
     'Bỏ khẳng định 4 m³/người/tháng: Mục V bản hợp nhất 57/VBHN-BXD hướng dẫn Nghị định 117 nói về mức tối thiểu theo hộ trong trường hợp dùng chung đồng hồ. Không lấy mức khoán 30–50 nghìn/người làm giá chuẩn vì chưa có khảo sát/căn cứ xác minh. Bản 57 là hợp nhất thông tư hướng dẫn, không phải bản hợp nhất Nghị định 117. Mã khách hàng/danh bộ lấy trên hóa đơn, đối chiếu đơn vị và tháng; không nhập OTP/tài khoản ngân hàng vào liên kết được gửi riêng chưa xác minh.',
     [('water215', '1', '1'), ('water215', '1', '2')]),
    ('residence', 'Tạm trú, chuyển chỗ ở và CT01', range(13, 17),
     ['residence68', 'amend118', 'residence154', 'residence116', 'amend347', 'lv_residence'],
     'Luật Cư trú đọc cùng các sửa đổi liên quan; Thông tư 116/2026/TT-BCA có hiệu lực từ 01/07/2026. Không tiếp tục hướng dẫn bằng biểu mẫu Thông tư 55/2021 đã bị thay thế.',
     'Điều kiện từ 30 ngày trở lên tại Điều 27 là điều kiện phải đăng ký tạm trú, không phải câu khẳng định mọi người được chờ 30 ngày mới nộp. Có thể nộp trực tiếp hoặc qua Cổng dịch vụ công quốc gia/VNeID theo Điều 3 Thông tư 116. Chuẩn bị tài khoản đáp ứng yêu cầu xác thực của kênh nộp tại thời điểm thực hiện; không mô tả tên từng nút trên ứng dụng khi chưa kiểm tra giao diện. CT01 bản gốc và cách ghi được lưu riêng trong Data/legal_templates.md.',
     [('residence116', '3', '5'), ('residence116', '3', '6'), ('residence116', '12', '1'), ('residence116', '12', '3')]),
    ('fire_safety', 'An toàn PCCC và thoát nạn nhà trọ', range(17, 21),
     ['fire58', 'fire105', 'fire106', 'fire69', 'amend347', 'fire1074', 'lv_fire', 'lv_fire1074', 'cantho_fire_call', 'fire_directive19', 'fire_standard3890'],
     'Phân loại công trình, diện tích, số tầng, mục đích sử dụng và thời điểm tồn tại trước khi áp yêu cầu. Không gọi Nghị định 50/2024 là quy định mới nhất năm 2026.',
     'Kiểm tra lối ra sử dụng được, không bị khóa/chặn; khả năng thoát ở khu vực có lồng sắt; vị trí sạc xe, tải điện và khoảng cách vật dễ cháy. Không suy từ tên nhà trọ thành quy tắc bắt buộc chung đúng hai lối thoát hoặc đúng hai bình. Quyết định 1074 có phạm vi riêng đối với công trình tồn tại trước luật và không có khả năng áp dụng tiêu chuẩn/quy chuẩn tương ứng. Khi có cháy, báo động, thoát theo đường an toàn và gọi 114; chỉ cắt điện/chữa cháy ban đầu nếu bảo đảm an toàn, không quay lại lấy tài sản.',
     [('fire58', '20', '1'), ('fire58', '21', '1')]),
    ('real_estate_brokerage', 'Môi giới và phí xem phòng', range(21, 25),
     ['broker29', 'broker06', 'civil91', 'lv_broker'],
     'Xác định môi giới kinh doanh thuộc Luật Kinh doanh bất động sản hay quan hệ giới thiệu/dịch vụ dân sự thông thường trước khi áp căn cứ.',
     'Yêu cầu thông tin người cung cấp dịch vụ, quyền cho thuê hoặc ủy quyền, phòng thực tế, loại phí và thời điểm phát sinh. Có thể từ chối giao dịch khi không đồng ý điều kiện phí; không khẳng định mọi khoản phí xem phòng đều bị cấm hoặc cứ chưa thuê là không phải trả. Nghĩa vụ thanh toán/hoàn phí cần xét thỏa thuận, việc thông tin sai và căn cứ trách nhiệm. Không soạn biểu mẫu hợp đồng môi giới.',
     [('broker06', '46', '4')]),
    ('ecommerce_platform', 'Tìm trọ qua nền tảng và phản ánh tin sai', range(25, 29),
     ['commerce122', 'commerce248', 'lv_commerce', 'lv_commerce248', 'rental_warning'],
     'Dùng Luật Thương mại điện tử 122/2025 và Nghị định 248/2026 theo thời điểm áp dụng; xác định loại nền tảng và chức năng đặt hàng. Không chỉ dựa bộ Nghị định 52/2013–85/2021.',
     'Lưu URL/mã tin, ngày giờ, tài khoản đăng, ảnh quảng cáo và điểm sai; gửi kênh phản ánh/khiếu nại được nền tảng công bố. Không bịa nút Report hay một thời hạn gỡ áp dụng mọi tin. Phòng chống phishing: tự mở tên miền chính thức, kiểm tra địa chỉ đích, không cung cấp mật khẩu/OTP, không cài ứng dụng lạ để giữ phòng. Những bước này là khuyến nghị an toàn, không phải căn cứ khẳng định một tên miền cụ thể phạm tội.',
     [('commerce122', '11', '1')]),
    ('privacy_data', 'Căn cước, số điện thoại và dữ liệu cá nhân', range(29, 33),
     ['privacy91', 'privacy356', 'privacy330', 'lv_privacy', 'residence116'],
     'Luật 91/2025 và Nghị định 356/2025 áp dụng từ 01/01/2026; không dùng Nghị định 13/2023 như căn cứ hiện hành duy nhất. Chế tài phải xác định hành vi, thời điểm và đúng quy định, không tự áp một mức tại Điều 102 Nghị định 15/2020.',
     'Không đăng công khai ảnh căn cước, địa chỉ/số điện thoại để gây áp lực trả cọc. Nếu dùng bản ảnh để xác minh tư nhân, có thể ghi mục đích và bên nhận khi họ chấp nhận; watermark chỉ giúp hạn chế tái sử dụng, không bảo đảm chống giả mạo và không được làm mất thông tin cần xác minh trong hồ sơ chính thức. Yêu cầu xử lý cần nêu dữ liệu, mục đích, quyền đang thực hiện, bằng chứng và kênh phản hồi; thời hạn khác nhau theo Điều 5 Nghị định 356.',
     [('residence116', '3', '5')]),
    ('criminal_law', 'Dấu hiệu chiếm đoạt cọc và tố giác', range(33, 37),
     ['criminal135', 'procedure17', 'cantho_warning', 'rental_warning', 'cantho_police_contacts'],
     'Phân biệt tranh chấp dân sự, rủi ro và dấu hiệu tội phạm. Cơ quan có thẩm quyền đánh giá đầy đủ hành vi và điều kiện, không suy tội chỉ từ số tiền hoặc việc mất liên lạc.',
     'Điều 174 khoản 1: định lượng cơ bản từ 2 triệu đồng; dưới mức này phải kiểm tra từng trường hợp luật liệt kê. Có tổ chức thuộc khoản 2, không tự thay thế điều kiện khoản 1. Điều 175 khoản 1: định lượng cơ bản từ 4 triệu đồng, cùng các trường hợp dưới ngưỡng riêng và hành vi chiếm đoạt luật định. Lưu chứng từ chuyển tiền, chủ tài khoản, URL/tài khoản đăng tin, hội thoại, giấy nhận cọc, ảnh hiện trường và bảng thời gian; không sửa chứng cứ gốc. Tố giác có thể bằng lời hoặc văn bản theo Điều 144–146 Bộ luật Tố tụng hình sự. Khung văn bản tham khảo nằm tại Data/legal_templates.md.', []),
]

generated = [form]
guide_records = []

def reference(sid, locator=''):
    s = sources[sid]
    return f"[{s['title']}]({s['url']})" + (f' — {locator}' if locator else '')

for category, title, ids, source_ids, scope, correction, quote_keys in topics:
    selected = [c for c in faq if c['id'] in ids]
    lines = [f'# CHỦ ĐỀ: {title}', '', f'Tags: {category}', 'Loại nội dung: hướng dẫn biên soạn (editorial_guidance), tách khỏi nguyên văn luật.',
             f'Ngày rà soát nguồn: {DATE}. Ngày này không thay thế ngày hiệu lực của từng văn bản.',
             f'Phạm vi áp dụng: {scope}', '', '## 1. Tóm tắt và điểm sửa tài liệu đề xuất', '', correction, '',
             '## 2. Căn cứ và đoạn trích đối chiếu', '']
    for sid in source_ids:
        lines.append('- ' + reference(sid) + '.')
    lines += ['', 'Các đoạn dưới đây được chọn từ hồ sơ đã đối chiếu ảnh PDF; không phải bản trích đầy đủ mọi điều liên quan.']
    for sid, art, clause in quote_keys:
        match = next(p for p in reviewed if (p['source_id'], p['article'], p['clause']) == (sid, art, clause))
        lines += ['', f"**{reference(sid, match['heading'])}**, trang PDF {match['page_from']}–{match['page_to']}.", '',
                  'Dạng nội dung: ' + ('bảng được chép lại có cấu trúc' if sid == 'water215' else 'trích nguyên văn đoạn đã đối chiếu') + '.', '']
        lines += ['> ' + t for t in match['content'].splitlines()]
        lines += ['', '**Điều kiện áp dụng:** ' + match['applicability_note'],
                  '**Hồ sơ đối chiếu:** ' + link(BASE / 'reviewed_new_provisions.json', 'trang gốc và ảnh đã đọc') + '.']
    if not quote_keys:
        lines += ['', 'Bản trích pháp luật đã có trong thư mục chủ đề. Phần bổ sung này dẫn điều/khoản ở từng câu dưới đây; không gắn nhãn diễn giải là nguyên văn luật.']
    if category == 'privacy_data':
        lines += ['', 'Đoạn Điều 3 Thông tư 116 ở trên chỉ hỗ trợ cơ chế khai thác dữ liệu cư trú; quyền bảo vệ dữ liệu phải áp Luật 91 và Nghị định 356, không suy toàn bộ quyền từ thông tư này.']
    if category == 'fire_safety':
        lines += ['', '**Chỉ thị và tiêu chuẩn được đề xuất:** Chỉ thị 19/CT-TTg ngày 24/06/2024 được bổ sung đúng năm và vai trò văn bản chỉ đạo về nhà ở nhiều tầng/nhiều căn hộ, nhà ở riêng lẻ kết hợp sản xuất, kinh doanh. Không lấy chỉ thị này thay căn cứ phân loại công trình và chế tài đang áp dụng. TCVN 3890:2023 là tiêu chuẩn về trang bị, bố trí phương tiện PCCC cho nhà và công trình; danh mục VSQI ghi tình trạng còn hiệu lực. Chưa đọc/lưu toàn bộ tiêu chuẩn, nên không suy số lượng bình hoặc hệ thống phải lắp cho một nhà trọ cụ thể chỉ từ mục danh bạ tiêu chuẩn. Việc áp dụng cần đọc tiêu chuẩn đầy đủ cùng quy chuẩn và văn bản viện dẫn phù hợp công trình.']
    lines += ['', '## 3. Tình huống thực tế của sinh viên', '']
    for c in selected:
        lines += [f"### Q: {c['question']}", '', 'A: ' + c['answer'], '', '**Khuyến nghị thực tế:** ' + c['practical'], '', '**Căn cứ:**', '']
        for cite in c['citations']:
            lines.append(f"- [{cite['title']}]({cite['url']}) — {cite['locator']}.")
        lines += ['']
        guide_records.append(dict(**c, category=category, output_file=f'Data/{category}/Bo-sung-thuc-te-20261004.md'))
    lines += ['## 4. Thông tin và chứng cứ cần hỏi thêm', '',
              'Địa chỉ hiện tại; ngày sự việc/kỳ hóa đơn; hợp đồng hoặc thỏa thuận thực tế; đơn vị cung cấp dịch vụ; chứng từ liên quan. Hỏi phần thiếu trước khi kết luận quyền, nghĩa vụ, mức giá hoặc mức phạt.', '',
              'Danh bạ: ' + link(ROOT / 'Data/cantho_contacts.md', 'kênh hỗ trợ Cần Thơ') + '.']
    path = ROOT / f'Data/{category}/Bo-sung-thuc-te-20261004.md'
    save(path, '\n'.join(lines)); generated.append(path)

contacts = [
    ('Báo cháy, cứu nạn cứu hộ', ['114'], 'cantho_fire_call', 'Có cháy/nguy hiểm: cung cấp địa chỉ, tình trạng và số người mắc kẹt.'),
    ('Tổng đài khẩn cấp quốc gia', ['112'], 'national112', 'Sự cố, thiên tai, thảm họa, tình huống nguy cấp cần trợ giúp; tiếp nhận 24/7.'),
    ('Trực ban Công an TP. Cần Thơ', ['0693672010'], 'cantho_police_contacts', 'Liên hệ trực ban, hỏi đơn vị tiếp nhận theo địa chỉ/sự việc.'),
    ('Trực ban hình sự Công an TP. Cần Thơ', ['0693672216'], 'cantho_police_contacts', 'Cung cấp thông tin dấu hiệu chiếm đoạt; hỏi hướng tiếp nhận hồ sơ.'),
    ('Phòng Cảnh sát quản lý hành chính về trật tự xã hội', ['0693672664'], 'cantho_police_contacts', 'Hỏi hướng dẫn cư trú theo địa chỉ và hồ sơ cụ thể.'),
    ('Công an phường Ninh Kiều', ['02923820938'], 'cantho_police_contacts', 'Chọn theo địa chỉ thực tế, không chỉ theo tên phường cũ.'),
    ('Công an phường An Bình', ['02923846024'], 'cantho_police_contacts', 'Chọn theo địa chỉ thực tế.'),
    ('Công an phường Tân An', ['02923894939', '02923838025'], 'cantho_police_contacts', 'Chọn theo địa chỉ thực tế.'),
    ('Công an phường Cái Khế', ['02923890379'], 'cantho_police_contacts', 'Chọn theo địa chỉ thực tế.'),
    ('Công an phường Bình Thủy', ['02923841019'], 'cantho_police_contacts', 'Chọn theo địa chỉ thực tế.'),
    ('Công an phường Cái Răng', ['02923836205'], 'cantho_police_contacts', 'Chọn theo địa chỉ thực tế.'),
    ('Công an phường Hưng Phú', ['02923916009', '02923836311', '02923916555'], 'cantho_police_contacts', 'Chọn theo địa chỉ thực tế.'),
    ('CSKH Điện lực miền Nam (EVNSPC)', ['19001006', '19009000'], 'evnspc_contacts', 'Hỏi công tơ, hợp đồng mua điện, kê khai người thuê và cách áp giá điện.'),
    ('Công ty CP Cấp thoát nước Cần Thơ', ['02923810188'], 'cantho_water_contacts', 'Hỏi theo mã khách hàng và đơn vị trên hóa đơn.'),
    ('Chi nhánh Cấp nước Số 1', ['02923839946'], 'cantho_water_contacts', 'Đối chiếu đơn vị quản lý cấp nước của phòng trọ.'),
    ('Chi nhánh Cấp nước An Bình', ['02923914757'], 'cantho_water_contacts', 'Đối chiếu đơn vị quản lý cấp nước của phòng trọ.'),
    ('Chi nhánh Cấp nước Bông Vang', ['02923933329'], 'cantho_water_contacts', 'Đối chiếu đơn vị quản lý cấp nước của phòng trọ.'),
    ('Chi nhánh Cấp nước Hưng Phú', ['02923837565'], 'cantho_water_contacts', 'Đối chiếu đơn vị quản lý cấp nước của phòng trọ.'),
    ('Công ty CP Cấp nước Cần Thơ 2', ['02923881690'], 'water_tariff2', 'Đây là đơn vị khác với Công ty CP Cấp thoát nước Cần Thơ; xem đúng hóa đơn.'),
]
contact_records = [dict(name=n, phones=p, source_id=s, source_url=sources[s]['url'], usage=u,
                        verified_date=DATE, verification='published_on_official_site_not_call_tested') for n,p,s,u in contacts]
dump(ROOT / 'Data/cantho_contacts.json', dict(category='emergency_contacts_cantho', kind='public_contact_directory',
     checked_date=DATE, contacts=contact_records, live_index_updated=False))
generated.append(ROOT / 'Data/cantho_contacts.json')
lines = ['# CHỦ ĐỀ: Danh bạ hỗ trợ sinh viên thuê trọ tại Cần Thơ', '', 'Tags: emergency_contacts_cantho',
         'Loại nội dung: danh bạ công khai; không phải quy phạm pháp luật.', f'Ngày đối chiếu trang nguồn: {DATE}.', '',
         'Chọn cơ quan theo địa chỉ hiện tại và đơn vị ghi trên hóa đơn. Số dưới đây đã đối chiếu trang công bố; chưa gọi thử khả năng kết nối. Nếu không liên lạc được, mở lại trang nguồn hoặc đến cơ quan tiếp nhận.', '',
         '| Cơ quan/kênh | Điện thoại | Khi sử dụng | Nguồn |', '| --- | --- | --- | --- |']
for n,p,s,u in contacts:
    lines.append(f"| {n} | {' / '.join(p)} | {u} | [{sources[s]['title']}]({sources[s]['url']}) |")
lines += ['', '## Tra cứu điện, nước', '',
          '- Điện: tự mở [CSKH EVNSPC](https://cskh.evnspc.vn/Home/Index); chuẩn bị mã khách hàng, địa chỉ, kỳ hóa đơn, ảnh chỉ số công tơ và bảng thu của chủ trọ.',
          '- Nước: xem tên công ty, mã danh bộ/mã khách hàng và kỳ hóa đơn. Cấp thoát nước Cần Thơ có [cổng hóa đơn](https://hddt.ctn-cantho.com.vn/); Cấp nước Cần Thơ 2 có [hướng dẫn tra cứu riêng](https://capnuoccantho2.com.vn/View.aspx?wc=78&wp=206). Mã và cách đăng nhập phụ thuộc nhà cung cấp.', '',
          '## Khi trình báo hoặc cần trợ giúp', '',
          'Nêu địa chỉ có thể xác định, mốc giờ, tình trạng đang xảy ra, thông tin liên hệ và yêu cầu hỗ trợ. Với tiền cọc, giữ chứng từ/hội thoại và mang hồ sơ đến nơi tiếp nhận; gọi điện hỏi hướng dẫn không thay thế biên nhận hồ sơ tố giác. Không tự suy thẩm quyền chỉ từ tên phường trước sắp xếp.', '',
          'Các số cũ và tên miền trong bản người dùng gửi chưa khớp nguồn công bố được ghi ở hồ sơ đối chiếu, không đưa vào bảng sử dụng. Danh bạ này là phần bổ sung; thư mục student_housing của kho hiện tại được giữ nguyên.']
save(ROOT / 'Data/cantho_contacts.md', '\n'.join(lines)); generated.append(ROOT / 'Data/cantho_contacts.md')

templates = '''# CHỦ ĐỀ: CT01 và hướng dẫn trình bày tố giác

Tags: residence | criminal_law
Ngày đối chiếu nguồn: 2026-10-04.
Loại nội dung: hướng dẫn biên soạn, kèm bản trích biểu mẫu hành chính chính thức.
Phạm vi: CT01 về cư trú và khung trình bày tố giác. Hợp đồng do các bên tự lập.

## 1. CT01 — dùng bản gốc kèm Thông tư 116/2026/TT-BCA

{form_link} gồm tờ khai và toàn bộ chú thích, trích trang vật lý 20–21 từ PDF Bộ Công an. Không vẽ lại hoặc đổi nội dung mẫu. [Trang văn bản Bộ Công an]({residence_url}); [bản ký PDF]({download_url}); [LuatVietnam để đối chiếu]({lv_url}). Nguồn và mã băm được lưu tại {provenance}.

### Các mục cần chuẩn bị

| Mục trên mẫu | Cách chuẩn bị thông tin |
| --- | --- |
| Kính gửi (1) | Cơ quan đăng ký cư trú tiếp nhận theo địa chỉ đăng ký. |
| 1–6 | Họ tên khai sinh, ngày sinh, giới tính, số định danh cá nhân, điện thoại và email của người kê khai. |
| 7–9 | Thông tin chủ hộ gia đình mới khi đăng ký thường trú, tạm trú hoặc tách hộ theo chú thích (2); xác định với người quản lý/chủ chỗ ở và cơ quan tiếp nhận, không tự mặc định người cho thuê luôn là chủ hộ. |
| 10 | Nêu rõ đề nghị đăng ký tạm trú, địa chỉ cụ thể và nội dung có liên quan. Nếu địa giới đã thay đổi, ghi địa chỉ mới đồng thời ghi chú địa chỉ theo giấy tờ chứng minh chỗ ở như chú thích (3). |
| 11 | Các thành viên trong hộ gia đình cùng thay đổi, nếu có; khai theo tình huống thực tế. |
| Chữ ký/ý kiến | Đọc đúng chú thích (4)–(8), tùy thủ tục và vai trò; không ký thay người khác. |

### Ý kiến chủ hộ, chủ sở hữu chỗ ở hợp pháp

Chú thích (4) và (5) quy định các trường hợp cần lấy ý kiến; có các phương thức ghi rõ nội dung đồng ý, ký và ghi họ tên vào tờ khai; xác nhận qua VNeID/dịch vụ công trực tuyến; hoặc văn bản đồng ý riêng không phải công chứng/chứng thực. Xác định trường hợp của mình trước khi yêu cầu chữ ký ở tất cả các cột.

Chú thích (5) nói đến ý kiến đồng sở hữu và các trường hợp đại diện/ngoại lệ. Ngoại lệ chỉ cần một chủ sở hữu ở điểm a khoản 2 Điều 20 Luật Cư trú là trường hợp đăng ký **thường trú** được nêu; không áp mở rộng thành quy tắc cho mọi đăng ký tạm trú.

Chú thích (6) hướng dẫn ý kiến cha/mẹ/người giám hộ trong các trường hợp tương ứng. Chú thích (7) phân biệt nộp trực tiếp với nộp qua cổng dịch vụ công/VNeID và người kê khai đồng thời là chủ hộ/chủ sở hữu/cha mẹ hoặc người giám hộ. Chú thích (8) chỉ yêu cầu phần thông tin đó khi đề nghị xác nhận nội dung đồng ý qua VNeID. Đọc bản gốc để áp đúng trường hợp.

### Nộp hồ sơ trực tuyến

Theo Điều 3 Thông tư 116, có kênh Cổng dịch vụ công quốc gia và VNeID. Tự truy cập [Cổng dịch vụ công quốc gia](https://dichvucong.gov.vn/), tìm thủ tục đăng ký tạm trú, kiểm tra cơ quan nhận và yêu cầu xác thực tài khoản trên kênh hiện tại. Điền đúng nội dung, cung cấp giấy tờ theo hồ sơ và cơ chế khai thác dữ liệu, thực hiện xác nhận đồng ý theo hướng dẫn, lưu mã hồ sơ và theo dõi yêu cầu bổ sung. Đây là quy trình khái quát; tên nút trên ứng dụng cần kiểm tra tại lúc thực hiện.

Điều 28 Luật Cư trú quy định thành phần hồ sơ, đọc cùng Nghị định 154/2024 và Thông tư 116. Khoản 5 Điều 3 Thông tư 116 không cho yêu cầu nộp/xuất trình giấy tờ đã chia sẻ và khai thác được; nếu không khai thác được thì áp khoản 6. Không biến hướng dẫn này thành danh sách bản sao căn cước/hợp đồng bắt buộc giống nhau cho mọi hồ sơ. [Luật Cư trú]({law_url}), [Nghị định 154]({proof_url}).

## 2. Khung trình bày tố giác về việc nhận tiền cọc có dấu hiệu chiếm đoạt

**Khung dưới đây do dự án biên soạn để sắp xếp thông tin, không phải mẫu hành chính bắt buộc của cơ quan Công an.** Điều 144–146 [Bộ luật Tố tụng hình sự]({procedure_url}) cho phép tố giác bằng lời hoặc bằng văn bản; người tiếp nhận thực hiện việc ghi nhận theo quy định. Người gửi mô tả sự thật và dấu hiệu, không cần tự kết luận tội danh.

### Nội dung tham khảo để người gửi tự điền

**VĂN BẢN TỐ GIÁC VỀ SỰ VIỆC CÓ DẤU HIỆU CHIẾM ĐOẠT TIỀN CỌC THUÊ TRỌ**

Kính gửi: [Cơ quan tiếp nhận thực tế].

Người tố giác: [Họ tên, ngày sinh, thông tin định danh phù hợp, địa chỉ liên hệ, điện thoại/kênh nhận thông báo].

Người/tài khoản liên quan, nếu biết: [Họ tên hoặc tên tài khoản, đường dẫn tin, số điện thoại, tài khoản nhận tiền; ghi rõ thông tin nào chưa kiểm chứng].

Diễn biến: [Ngày giờ thấy tin; địa chỉ phòng được giới thiệu; nội dung hứa hẹn; việc xem phòng/xác minh; ngày giờ chuyển tiền; số tiền, ngân hàng, mã giao dịch; việc nhận giấy cọc; diễn biến sau chuyển tiền; liên hệ và phản hồi].

Căn cứ nghi ngờ: [Thông tin giả mạo/sai được phát hiện, người không có quyền cho thuê, cùng phòng nhận cọc nhiều người, thông tin liên lạc thay đổi… chỉ ghi điều có chứng cứ hoặc chỉ rõ nguồn người cung cấp].

Thiệt hại và người liên quan: [Số tiền của bản thân, khoản đã nhận lại nếu có; tên/liên hệ người khác khi được họ đồng ý cung cấp. Nếu nhiều người gửi chung, ghi riêng diễn biến và số tiền từng người, không cộng cơ học để tự kết luận khung hình phạt].

Tài liệu kèm theo: [Danh mục đánh số: sao kê/biên nhận chuyển tiền, hội thoại có mốc giờ, URL/mã tin, ảnh quảng cáo, giấy cọc, tài liệu xác minh phòng, thông tin người làm chứng]. Giữ bản gốc; nếu giao bản gốc thì đề nghị ghi nhận cụ thể việc nhận tài liệu.

Đề nghị: Tiếp nhận, kiểm tra, xác minh sự việc theo thẩm quyền; thông báo kết quả theo quy định và hướng dẫn thủ tục bảo vệ quyền lợi. [Nêu nhu cầu bảo vệ thông tin/liên hệ an toàn nếu có].

Tôi trình bày đúng sự việc theo thông tin mình biết; thông tin chưa xác minh đã được ghi rõ. [Địa điểm, ngày, họ tên và chữ ký của người trình bày].

### Nộp và theo dõi

Liên hệ Công an gần nhất hoặc cơ quan có thẩm quyền; dùng {contacts_link} để hỏi nơi tiếp nhận theo địa chỉ. Khi nộp, đề nghị ghi nhận việc nhận nội dung và tài liệu, lưu bản đã gửi cùng mã/biên nhận nếu được cấp. Gọi tổng đài hoặc đăng lên mạng không thay cho hồ sơ tiếp nhận. Không công khai căn cước, địa chỉ hoặc tài khoản của người khác để gây áp lực.

Phân biệt Điều 174 và Điều 175 [Bộ luật Hình sự]({criminal_url}): định lượng cơ bản lần lượt 2 triệu và 4 triệu đồng, có điều kiện riêng cho tài sản dưới mức đó; “có tổ chức” không tự thay điều kiện định tội. Hành vi gian dối, thời điểm nhận tiền, mục đích chiếm đoạt và các dấu hiệu khác phải được xác minh. Một tranh chấp hoàn cọc không mặc nhiên là tội phạm.
'''
save(ROOT / 'Data/legal_templates.md', templates.format(
     form_link=link(form, 'Tải CT01 bản trích từ PDF gốc (2 trang)'), residence_url=sources['residence116']['url'],
     download_url='https://bocongan.gov.vn/media/bca-media/library-20260717110413-0c32870e-3f4d-41d8-9da4-8f90638543ff-thong-tu-116-2026.pdf',
     lv_url=sources['lv_residence']['url'], provenance=link(OUT / 'ct01_provenance.json', 'hồ sơ nguồn CT01'),
     law_url=sources['residence68']['url'], proof_url=sources['residence154']['url'],
     procedure_url=sources['procedure17']['url'], criminal_url=sources['criminal135']['url'],
     contacts_link=link(ROOT / 'Data/cantho_contacts.md', 'danh bạ Cần Thơ')))
generated.append(ROOT / 'Data/legal_templates.md')

dump(OUT / 'faq_by_category.json', dict(kind='editorial_guidance', evaluation_ground_truth=False,
     source_package='legal_web_supplement_20261004/faq_36.json', cases=guide_records))
used_ids = set(c['source_id'] for c in contact_records)
for c in guide_records:
    used_ids.update(x['source_id'] for x in c['citations'])
for topic in topics:
    used_ids.update(topic[3])
used_ids.update(['lv_residence', 'procedure17', 'criminal135', 'residence68', 'residence154'])
catalog = [sources[sid] for sid in sorted(used_ids)]
dump(OUT / 'sources.json', dict(accessed_date=DATE, source_policy='Nguồn gốc/cơ quan công bố ưu tiên; LuatVietnam đối chiếu; bài hướng dẫn chỉ lưu tham chiếu và nội dung ngắn.', sources=catalog))
source_lines = ['# Nguồn của phần bổ sung 10 chủ đề', '', 'Nguồn kế thừa được giữ đúng trạng thái xác minh trong gói 36 câu; nguồn danh bạ có lượt đối chiếu mới. Không xác nhận hiệu lực toàn văn chỉ vì tải thành công.', '']
for s in catalog:
    source_lines += [f"- **{s['id']}** — [{s['title']}]({s['url']}); vai trò: {s['role']}; truy cập: {s.get('accessed_date', DATE)}. " + s.get('review_note', s.get('verification', ''))]
save(OUT / 'SOURCES.md', '\n'.join(source_lines))

audit = ['# Đối chiếu đề xuất 10 chủ đề — 04/10/2026', '',
         'Bản đề xuất của người dùng đã lưu nguyên văn và có mã băm. Các nội dung dưới đây là quyết định biên tập sau đối chiếu nguồn, không sửa bản gốc.', '',
         'Kho Data hiện có 10 thư mục, gồm student_housing. Đề xuất thay mục thứ mười bằng danh bạ; lần bổ sung này giữ student_housing và thêm danh bạ ở cấp Data, không đổi phân loại của pipeline hiện hành.', '',
         '| Chủ đề đề xuất | Nội dung được bổ sung/sửa | Tài liệu |', '| --- | --- | --- |']
for cat,title,ids,sids,scope,correction,keys in topics:
    audit.append(f'| {cat} | {correction} | {link(ROOT / f"Data/{cat}/Bo-sung-thuc-te-20261004.md", title)} |')
audit += [f'| emergency_contacts_cantho | Chọn số từ trang cơ quan/nhà cung cấp hiện công bố, kèm nguồn và ngày đối chiếu. | {link(ROOT / "Data/cantho_contacts.md", "Danh bạ")} |', '',
          '## Số điện thoại và nguồn cũ chưa đủ căn cứ', '',
          '| Nội dung trong bản đề xuất | Kết quả đối chiếu |', '| --- | --- |',
          '| Cấp thoát nước (0292) 3830248; canthowater.vn | Chưa khớp trang liên hệ công ty. Dùng 02923810188, ctn-cantho.com.vn theo nguồn công bố. |',
          '| Xuân Khánh 02923830081; An Khánh 02923897456; Hưng Lợi 02923838527 | Chưa xác minh từ danh bạ hiện tại. Không tự chuyển số hoặc ghép tên phường cũ sang phường mới. |',
          '| An Bình 02923846113 | Danh bạ Công an Cần Thơ hiện công bố 02923846024; dùng số theo nguồn công bố. |', '',
          '## Phạm vi biểu mẫu', '',
          '- Giữ CT01 hành chính chính thức, cả tờ khai lẫn chú thích.',
          '- Thêm khung trình bày tố giác, ghi rõ do dự án biên soạn, không phải mẫu bắt buộc.',
          '- Không tạo mẫu hợp đồng thuê, hợp đồng môi giới hoặc hợp đồng cấp nước; giữ kiến thức pháp lý về các quan hệ này.', '',
          '## Trạng thái dùng trong hệ thống', '',
          'Tài liệu hướng dẫn và danh bạ có loại nội dung riêng, không coi là điều luật hoặc đáp án chuẩn đánh giá. Chưa nạp vào chỉ mục chạy và chưa thay manifest corpus cũ. Yêu cầu tạm dừng kiểm thử vẫn được giữ; không gọi mô hình hoặc tự khởi động lại worker.', '',
          f'Hướng dẫn CT01/tố giác: {link(ROOT / "Data/legal_templates.md", "legal_templates.md")}.',
          f'Danh mục nguồn: {link(OUT / "SOURCES.md", "SOURCES.md")}.']
save(OUT / 'AUDIT.md', '\n'.join(audit))

overview = ['# Bổ sung thực tế theo danh sách 10 chủ đề', '',
            'Đã bổ sung 9 tệp hướng dẫn theo thư mục pháp lý, danh bạ Cần Thơ, hướng dẫn CT01/tố giác và bản trích CT01 chính thức. Giữ kiến thức hợp đồng, để các bên tự lập hợp đồng.', '',
            f'- {link(OUT / "AUDIT.md", "Đối chiếu các điểm cần sửa trong danh sách gửi thêm")}',
            f'- {link(ROOT / "Data/cantho_contacts.md", "Danh bạ Cần Thơ có nguồn từng dòng")}',
            f'- {link(ROOT / "Data/legal_templates.md", "CT01 và khung trình bày tố giác")}',
            f'- {link(form, "CT01 chính thức — 2 trang từ bản ký Bộ Công an")}',
            f'- {link(OUT / "SOURCES.md", "Danh mục nguồn và vai trò nguồn")}', '',
            '## Hướng dẫn theo chủ đề', '']
for cat,title,*_ in topics:
    overview.append('- ' + link(ROOT / f'Data/{cat}/Bo-sung-thuc-te-20261004.md', title))
overview += ['', 'Dữ liệu nguồn có ngày truy cập, mã băm nếu tải thành công và trạng thái xác minh. Giá điện/nước, yêu cầu PCCC và thủ tục cần chọn đúng kỳ, địa chỉ và điều kiện áp dụng; phần diễn giải không mang nhãn nguyên văn luật.', '',
             'Đã lưu vào Data nhưng chưa nạp chỉ mục chạy hoặc chạy lại kiểm thử mô hình. Mốc v15 và trạng thái tạm dừng được giữ.']
save(OUT / 'README.md', '\n'.join(overview))

baseline = ROOT / 'docs/legal_corpus_v2/manifest.json'
checkpoint = ROOT / 'tmp/test_pause_until_gemini.json'
dump(OUT / 'manifest.json', dict(version='legal-practical-extension-20261004', created_at_utc=datetime.now(timezone.utc).isoformat(),
     scope='9 existing legal topics + supplemental emergency directory + CT01 and reporting guidance',
     contract_templates_created=False, legal_contract_knowledge_retained=True, thematic_guide_count=9,
     faq_count=len(guide_records), public_contact_entries=len(contacts), official_ct01_pages=2,
     original_user_sha256=sha(raw), source_count=len(catalog), new_source_captures=captures,
     generated_data_files=[dict(path=p.relative_to(ROOT).as_posix(), sha256=sha(p), bytes=p.stat().st_size) for p in generated],
     corpus_manifest_path=baseline.relative_to(ROOT).as_posix(), corpus_manifest_sha256=sha(baseline),
     pause_status=json.loads(checkpoint.read_text(encoding='utf-8'))['status'],
     live_index_updated=False, model_evaluations_run=False, student_housing_modified=False))
print(json.dumps(dict(guides=9, faqs=len(guide_records), contacts=len(contacts),
                     data_files=len(generated), ct01_pages=len(PdfReader(form).pages),
                     captured_sources=[(x['id'],x['http_status']) for x in captures]),ensure_ascii=False))
