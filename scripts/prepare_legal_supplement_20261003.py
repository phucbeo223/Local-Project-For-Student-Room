"""Create auditable extracts from official sources; archive superseded extracts."""
from pathlib import Path
import hashlib, json, re, shutil, zipfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'Data'
RAW = ROOT / 'docs/legal_sources_originals_20261003'
EXTRACTED = ROOT / 'eval/source_supplement_20261003'
ARCHIVE = ROOT / 'docs/legal_sources_excluded/supplement_20261003'
MANIFEST = RAW / 'prepared_manifest.json'
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def paragraphs(path):
    root = ET.fromstring(zipfile.ZipFile(path).read('word/document.xml'))
    return [''.join(t.text or '' for t in p.findall('.//w:t', NS)) for p in root.findall('.//w:p', NS)]

def clean_native(text):
    lines = [line.strip() for line in text.splitlines()]
    lines = [line for line in lines if line and not re.fullmatch(r'\d+', line) and not line.startswith('CÔNG BÁO/')]
    # Paragraph numbers and point labels are retained; only physical PDF line wraps are joined.
    out = []
    for line in lines:
        if re.match(r'^(Điều \d+\.|\d+\. |[a-zđ]\) )', line): out.append(line)
        elif out: out[-1] += ' ' + line
        else: out.append(line)
    return '\n\n'.join(out)

def native_article(key, number):
    text = (EXTRACTED / (key + '.txt')).read_text(encoding='utf-8')
    match = re.search(r'(?m)^\s*Điều ' + str(number) + r'\.', text)
    assert match, (key, number)
    end = re.search(r'(?m)^\s*Điều \d+\.', text[match.end():])
    article = text[match.start():match.end() + end.start() if end else len(text)]
    article = re.split(r'(?m)^\s*Chương [IVX]+\s*$', article)[0]
    return clean_native(article)

CIVIL328 = '''Điều 328. Đặt cọc
1. Đặt cọc là việc một bên (sau đây gọi là bên đặt cọc) giao cho bên kia (sau đây gọi là bên nhận đặt cọc) một khoản tiền hoặc kim khí quý, đá quý hoặc vật có giá trị khác (sau đây gọi chung là tài sản đặt cọc) trong một thời hạn để bảo đảm giao kết hoặc thực hiện hợp đồng.
2. Trường hợp hợp đồng được giao kết, thực hiện thì tài sản đặt cọc được trả lại cho bên đặt cọc hoặc được trừ để thực hiện nghĩa vụ trả tiền; nếu bên đặt cọc từ chối việc giao kết, thực hiện hợp đồng thì tài sản đặt cọc thuộc về bên nhận đặt cọc; nếu bên nhận đặt cọc từ chối việc giao kết, thực hiện hợp đồng thì phải trả cho bên đặt cọc tài sản đặt cọc và một khoản tiền tương đương giá trị tài sản đặt cọc, trừ trường hợp có thoả thuận khác.'''

RESIDENCE = '''Điều 9. Nghĩa vụ của công dân về cư trú
1. Thực hiện việc đăng ký cư trú theo quy định của Luật này và quy định khác của pháp luật có liên quan.
2. Cung cấp đầy đủ, chính xác, kịp thời thông tin, giấy tờ, tài liệu về cư trú của mình cho cơ quan, người có thẩm quyền và chịu trách nhiệm về thông tin, giấy tờ, tài liệu đã cung cấp.
3. Nộp lệ phí đăng ký cư trú theo quy định của pháp luật về phí và lệ phí.

Điều 27. Điều kiện đăng ký tạm trú
1. Công dân đến sinh sống tại chỗ ở hợp pháp ngoài phạm vi đơn vị hành chính cấp xã nơi đã đăng ký thường trú để lao động, học tập hoặc vì mục đích khác từ 30 ngày trở lên thì phải thực hiện đăng ký tạm trú.
2. Thời hạn tạm trú tối đa là 02 năm và có thể tiếp tục gia hạn nhiều lần.
3. Công dân không được đăng ký tạm trú mới tại chỗ ở quy định tại Điều 23 của Luật này.

Điều 28. Hồ sơ, thủ tục đăng ký tạm trú, gia hạn tạm trú
1. Hồ sơ đăng ký tạm trú bao gồm:
a) Tờ khai thay đổi thông tin cư trú; đối với người đăng ký tạm trú là người chưa thành niên thì trong tờ khai phải ghi rõ ý kiến đồng ý của cha, mẹ hoặc người giám hộ, trừ trường hợp đã có ý kiến đồng ý bằng văn bản;
b) Giấy tờ, tài liệu chứng minh chỗ ở hợp pháp.
2. Người đăng ký tạm trú nộp hồ sơ đăng ký tạm trú đến cơ quan đăng ký cư trú nơi mình dự kiến tạm trú.
Khi tiếp nhận hồ sơ đăng ký tạm trú, cơ quan đăng ký cư trú kiểm tra và cấp phiếu tiếp nhận hồ sơ cho người đăng ký; trường hợp hồ sơ chưa đầy đủ thì hướng dẫn người đăng ký bổ sung hồ sơ.
Trong thời hạn 03 ngày làm việc kể từ ngày nhận được hồ sơ đầy đủ và hợp lệ, cơ quan đăng ký cư trú có trách nhiệm thẩm định, cập nhật thông tin về nơi tạm trú mới, thời hạn tạm trú của người đăng ký vào Cơ sở dữ liệu về cư trú và thông báo cho người đăng ký về việc đã cập nhật thông tin đăng ký tạm trú; trường hợp từ chối đăng ký thì phải trả lời bằng văn bản và nêu rõ lý do.
3. Trong thời hạn 15 ngày trước ngày kết thúc thời hạn tạm trú đã đăng ký, công dân phải làm thủ tục gia hạn tạm trú.
Hồ sơ, thủ tục gia hạn tạm trú thực hiện theo quy định tại khoản 1 và khoản 2 Điều này. Sau khi thẩm định hồ sơ, cơ quan đăng ký cư trú có trách nhiệm cập nhật thông tin về thời hạn tạm trú mới của người đăng ký vào Cơ sở dữ liệu về cư trú và thông báo cho người đăng ký về việc đã cập nhật thông tin đăng ký tạm trú; trường hợp từ chối đăng ký thì phải trả lời bằng văn bản và nêu rõ lý do.

Điều 30. Thông báo lưu trú
1. Khi có người lưu trú qua đêm, thành viên hộ gia đình, người đại diện cơ sở chữa bệnh, cơ sở lưu trú du lịch, chủ sở hữu hoặc người được giao quản lý phương tiện, các cơ sở lưu trú khác có trách nhiệm thông báo việc lưu trú với cơ quan đăng ký cư trú; trường hợp người đến lưu trú tại chỗ ở của cá nhân, hộ gia đình mà cá nhân, thành viên hộ gia đình không có mặt tại chỗ ở đó thì người đến lưu trú có trách nhiệm thông báo việc lưu trú với cơ quan đăng ký cư trú.
2. Nội dung thông báo về lưu trú bao gồm họ và tên, ngày, tháng, năm sinh, số định danh cá nhân hoặc số hộ chiếu của người lưu trú; lý do lưu trú; thời gian lưu trú; địa chỉ lưu trú.
3. Việc thông báo lưu trú được thực hiện trước 23 giờ của ngày bắt đầu lưu trú; trường hợp người đến lưu trú sau 23 giờ thì việc thông báo lưu trú được thực hiện trước 08 giờ ngày hôm sau.
4. Bộ trưởng Bộ Công an quy định chi tiết việc thông báo lưu trú.'''

def write_source(relative, title, body, origin, notes, previous=None):
    target = DATA / relative
    archive_info = None
    if previous:
        old = DATA / previous
        archive = ARCHIVE / previous
        assert old.resolve().is_relative_to(DATA.resolve()) and archive.resolve().is_relative_to(ROOT.resolve())
        if old.exists():
            archive.parent.mkdir(parents=True, exist_ok=True)
            old_hash = sha(old)
            if archive.exists(): assert sha(archive) == old_hash
            else: shutil.copy2(old, archive)
            old.unlink()
            archive_info = {'path': str(archive.relative_to(ROOT)), 'sha256': old_hash}
        elif archive.exists(): archive_info = {'path': str(archive.relative_to(ROOT)), 'sha256': sha(archive)}
    target.parent.mkdir(parents=True, exist_ok=True)
    # Provenance stays outside operative text so it cannot masquerade as a legal rule.
    target.write_text(title + '\n\n' + body.strip() + '\n', encoding='utf-8')
    return {'path': relative, 'sha256': sha(target), 'origin': origin, 'notes': notes, 'archived': archive_info}

def main():
    records = []
    previous = 'housing_contract/Bộ-luật-91-2015-QH13-trích-tuyển.docx'
    source = DATA / previous
    if not source.exists(): source = ARCHIVE / previous
    text = '\n'.join(paragraphs(source))
    articles = re.split(r'(?=Điều \d+\.)', text)[1:]
    result = []
    for article in articles:
        if article.startswith('Điều 328.'): article = CIVIL328
        elif article.startswith('Điều 689.'):
            article = 'Điều 689. Hiệu lực thi hành\nBộ luật này có hiệu lực thi hành từ ngày 01 tháng 01 năm 2017.\nBộ luật dân sự số 33/2005/QH11 hết hiệu lực kể từ ngày Bộ luật này có hiệu lực.'
        result.append(article.strip())
    assert len(result) == 42
    records.append(write_source('housing_contract/Bo-luat-91-2015-QH13-doi-chieu-20261003.md', 'BỘ LUẬT DÂN SỰ 91/2015/QH13 — TRÍCH TUYỂN', '\n\n'.join(result), ['civil91first', 'civil91'], {'replaced': [328, 689], 'visual_pages_328': [86, 87], 'other_articles': 'Giữ nguyên bản trích trước; kiểm tra đuôi đoạn, không khẳng định đã đối chiếu toàn văn từng chữ.'}, previous))
    records.append(write_source('residence/Luat-68-2020-QH14-doi-chieu-20261003.md', 'LUẬT CƯ TRÚ 68/2020/QH14 — ĐIỀU 30 ĐÃ SỬA BỞI LUẬT 118/2025/QH15', RESIDENCE, ['residence68', 'amend118'], {'articles': [9,27,28,30], 'visual_pages': {'residence68': [5,15,16], 'amend118': [12,13]}, 'amendment': 'Điều 4 khoản 9 Luật 118 thay Điều 30, áp dụng từ 01/07/2026; Điều 9,27,28 giữ nội dung gốc.', 'ocr': 'Chép đối chiếu ảnh: sửa Điền/Hỗ/tài Hiệu/tam tri; giữ đủ khoản, điểm và ngoại lệ.', 'article31': 'Nội dung sửa đổi vẫn có trong tài liệu Luật 118 riêng.'}, 'residence/Luật-68-2020-QH14-trích-tuyển-cập-nhật.docx'))
    fire = '\n\n'.join(native_article('fire55', n) for n in [8,20,21,23,24])
    records.append(write_source('fire_safety/Luat-55-2024-QH15-dieu-8-20-21-23-24.md', 'LUẬT 55/2024/QH15 — TRÍCH NGUYÊN ĐIỀU VỀ NHÀ Ở, CÁ NHÂN VÀ ĐIỆN', fire, ['fire55','amend118'], {'articles': [8,20,21,23,24], 'extraction': 'Văn bản PDF có lớp chữ; bỏ đầu trang Công báo, nối dòng; giữ nguyên khoản, điểm.', 'amendment': 'Luật 118 Điều 10 không sửa các điều được trích này; không suy rộng sang điều khác.'}, 'fire_safety/Luật-55-2024-QH15-trích-tuyển.docx'))
    downloads = json.loads((RAW/'download_manifest.json').read_text(encoding='utf-8'))
    for key, folder in [('rental_warning','criminal_law'),('online_warning','ecommerce_platform')]:
        raw_text = (RAW/(key+'.txt')).read_text(encoding='utf-8')
        if key == 'rental_warning':
            start = raw_text.index('Để phòng ngừa loại tội phạm này')
            end = raw_text.index('xử lý kịp thời.', start) + len('xử lý kịp thời.')
            body = 'Khuyến cáo của cơ quan Công an về đặt cọc thuê nhà qua mạng\n\n' + raw_text[start:end]
        else:
            segments = []
            for begin, ending in [('Tuyệt đối không cung cấp', 'bồi thường.'),('Trường hợp nghi ngờ bị lừa đảo', 'được hỗ trợ.')]:
                start = raw_text.index(begin); end = raw_text.index(ending,start)+len(ending)
                segments.append(raw_text[start:end])
            body = 'Khuyến cáo của cơ quan Công an về lừa đảo mua hàng trực tuyến\n\n' + '\n\n'.join(segments)
        records.append(write_source(folder+'/'+key+'-Bo-Cong-an-20261003.md', 'KHUYẾN CÁO PHÒNG NGỪA LỪA ĐẢO — KHÔNG PHẢI ĐIỀU LUẬT', body, [key], {'type':'khuyến cáo', 'scope': 'thuê nhà qua mạng' if key=='rental_warning' else 'mua hàng trực tuyến; không biến thành nghĩa vụ pháp lý thuê trọ'}))
    MANIFEST.write_text(json.dumps({'date':'2026-10-03','sources':records,'downloads':downloads,'download_limitations':['vbpl.moj.gov.vn không phân giải DNS trên máy','CDN Công báo lỗi chuỗi chứng chỉ; không tắt kiểm tra TLS','civil91.pdf là phần 2; đã tải thêm civil91first.pdf phần 1'], 'already_current':['Nghị định 105 hiện có đã cập nhật điểm a,b khoản 2 Điều 13 và khoản 3 Điều 14 theo 347; giữ nguyên','Luật nhà ở 79 có Điều 163 khoản 1; tăng ưu tiên truy xuất, không thêm bản trùng']},ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'prepared':len(records),'manifest':str(MANIFEST)},ensure_ascii=False))

if __name__ == '__main__': main()
