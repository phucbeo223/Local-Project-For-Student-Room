"""Bounded, source-bound coverage checks; never supply missing legal facts.

Question requirements are independent of retrieval. Source coverage and answer
coverage are separate lexical guards; semantic support is checked by Gemini.
"""
from .providers import normalize_text
from .evidence_units import operator_facets, OPERATOR_LABELS
import re

# Alternatives within each tuple; all tuples must match. No question IDs or
# reference answers enter this registry. Labels describe tasks, never legal facts.
FACETS = {
    'electric_disclosure': ('căn cứ công khai cách tính và sản lượng điện', (('thong bao', 'cong khai', 'minh bach'), ('san luong', 'chi so', 'cach tinh'))),
    'electric_allocation': ('định mức theo số người và điều kiện kê khai', (('dinh muc',), ('ke khai', 'cu tru'))),
    'electric_unreported': ('trường hợp không kê khai đủ và thời hạn thuê', (('khong',), ('ke khai',), ('12 thang',))),
    'electric_invoice': ('giới hạn thu và đối chiếu hóa đơn', (('hoa don',), ('thu', 'doi chieu', 'vuot'))),
    'electric_effective': ('thời điểm áp dụng và điều kiện chuyển tiếp', (('hieu luc', 'ap dung'), ('dieu chinh', 'chuyen tiep'))),
    'water_amount': ('mức khoán hoặc giá nước đã thỏa thuận', (('muc khoan', 'gia nuoc', 'tien nuoc', 'gia giao dich', 'gia thue'),)),
    'water_people': ('số người được tính phí và cách chia', (('so nguoi', 'dau nguoi', 'moi nguoi', 'chia tien', 'chia phi'),)),
    'water_period': ('kỳ thu và cách thanh toán', (('ky thu', 'hang thang', 'thanh toan', 'ky thanh toan'),)),
    'water_includes': ('các khoản đã bao gồm và phí dùng chung', (('bao gom', 'chi phi chung', 'phi dich vu', 'chi phi dich vu'),)),
    'water_change': ('điều kiện thay đổi mức thu', (('thay doi', 'dieu chinh', 'tang gia'),)),
    'water_invoice': ('đối chiếu hóa đơn và đúng đơn vị cấp nước', (('hoa don',), ('doi chieu', 'kiem tra', 'tra cuu'))),
    'privacy_purpose': ('mục đích và phạm vi sử dụng dữ liệu', (('muc dich',), ('pham vi', 'su dung', 'xu ly'))),
    'privacy_storage': ('thời gian lưu và biện pháp bảo vệ', (('luu tru', 'thoi gian luu', 'bao ve du lieu'),)),
    'privacy_transfer': ('điều kiện cung cấp cho bên khác và ngoại lệ', (('cung cap', 'chia se', 'chuyen giao'), ('dong y', 'ngoai le', 'tru truong hop'))),
    'privacy_request': ('yêu cầu ngừng hoặc hạn chế xử lý theo điều kiện nguồn', (('ngung xu ly', 'han che xu ly', 'rut lai su dong y'),)),
    'privacy_form': ('hình thức gửi yêu cầu', (('yeu cau',), ('van ban', 'dien tu'))),
    'privacy_recipient': ('bên tiếp nhận yêu cầu', (('gui', 'tiep nhan'), ('ben kiem soat', 'ben xu ly'))),
    'residence_trigger': ('điều kiện đăng ký cư trú tại nơi ở', (('tam tru', 'cu tru'), ('30 ngay', 'dang ky'))),
    'residence_documents': ('thông tin và giấy tờ cư trú', (('giay to', 'ho so', 'thong tin', 'to khai'),)),
    'residence_recipient': ('nơi tiếp nhận đăng ký', (('co quan dang ky', 'cong an', 'dich vu cong'),)),
    'residence_change': ('đăng ký nơi mới và điều kiện xóa nơi cũ', (('noi moi', 'noi cu', 'xoa dang ky', 'thay doi noi'),)),
    'fire_classification': ('phân loại theo công năng, số tầng và diện tích', (('tang',), ('dien tich',), ('nha o', 'co so', 'cong nang'))),
    'fire_exit': ('đường và lối thoát nạn theo loại công trình', (('thoat nan', 'loi thoat'),)),
    'fire_equipment': ('phương tiện chữa cháy theo phạm vi áp dụng', (('phuong tien', 'binh chua chay', 'thiet bi'), ('chua chay',))),
    'fire_electric': ('an toàn điện và nguồn gây cháy', (('dien',), ('an toan', 'chay'))),
    'listing_identity': ('tài khoản, người đăng và thông tin liên hệ', (('nguoi dang', 'tai khoan', 'so dien thoai', 'chu nha'),)),
    'listing_location': ('địa chỉ và nội dung tin đăng', (('dia chi', 'so nha', 'noi dung tin'),)),
    'listing_images': ('đối chiếu hình ảnh', (('hinh anh', 'tim kiem anh', 'ong kinh', 'google lens'),)),
    'listing_price': ('so sánh giá và dấu hiệu rẻ bất thường', (('gia',), ('re', 'so sanh', 'bat thuong'))),
    'link_destination': ('địa chỉ liên kết và trang giả mạo', (('lien ket', 'duong dan', 'ten mien', 'link'), ('gia mao', 'kiem tra', 'la'))),
    'link_credentials': ('yêu cầu mật khẩu, OTP hoặc thông tin ngân hàng', (('otp', 'mat khau', 'thong tin ngan hang'),)),
    'link_pressure': ('thúc ép hoặc yêu cầu chuyển tiền bất thường', (('thuc ep', 'gap', 'chuyen tien', 'dat coc'),)),
    'evidence_messages': ('lưu tin nhắn và thông tin tin đăng/giao dịch', (('tin nhan', 'anh chup', 'hinh anh', 'bang chung'),)),
    'evidence_payment': ('lưu tài khoản và chứng từ chuyển tiền', (('tai khoan ngan hang', 'phieu giao dich', 'chung tu', 'chuyen khoan'),)),
    'evidence_recipient': ('cơ quan tiếp nhận báo tin', (('cong an', 'co quan dieu tra', 'vien kiem sat'),)),
}


def question_facets(question):
    """Scope only what was asked; no sanctions or deep procedures by default."""
    q = normalize_text(question)
    keys = []
    if 'dien' in q and any(t in q for t in ('tien dien', 'tinh dien', 'tinh tien', 'thu tien dien')):
        if 'thong bao' in q or 'san luong' in q or 'so dien' in q:
            keys += ['electric_disclosure', 'electric_invoice']
        elif 'hoa don' in q or 'thu cao' in q:
            keys += ['electric_invoice', 'electric_effective']
        else:
            keys += ['electric_allocation', 'electric_unreported', 'electric_invoice', 'electric_effective']
    if 'nuoc' in q and any(t in q for t in ('dau nguoi', 'theo nguoi', 'chia', 'khoan')):
        keys += ['water_amount', 'water_people', 'water_period', 'water_includes', 'water_change', 'water_invoice']
    elif 'nuoc' in q and 'hoa don' in q:
        keys += ['water_invoice']
    if any(t in q for t in ('tam tru', 'cu tru', 'chuyen noi o')):
        if any(t in q for t in ('thu tuc', 'khi nao', 'bao lau')):
            keys += ['residence_trigger', 'residence_recipient']
        if any(t in q for t in ('giay to', 'ho so', 'thong tin', 'trach nhiem', 'thu tuc')):
            keys += ['residence_documents']
        if any(t in q for t in ('o dau', 'thu tuc')):
            keys += ['residence_recipient']
        if any(t in q for t in ('chuyen', 'thay doi', 'noi moi', 'noi cu')):
            keys += ['residence_change']
    if any(t in q for t in ('pccc', 'phong chay', 'chua chay', 'chay no', 'loi thoat nan')):
        if any(t in q for t in ('nhieu phong', 'yeu cau', 'dieu kien', 'quy dinh', 'trang bi')):
            keys += ['fire_classification', 'fire_exit', 'fire_equipment', 'fire_electric']
        elif 'thoat' in q:
            keys += ['fire_exit']
        elif 'thiet bi dien' in q:
            keys += ['fire_electric']
    if any(t in q for t in ('kiem tra nguoi dang', 'nguon tin', 'kiem tra tin dang')):
        keys += ['listing_identity', 'listing_location', 'listing_images', 'listing_price']
    elif 'khong cho xem phong' in q:
        keys += ['listing_identity', 'listing_location']
    if any(t in q for t in ('lien ket la', 'link la', 'duong dan la')):
        keys += ['link_destination', 'link_credentials', 'link_pressure']
    if any(t in q for t in ('bang chung', 'chung cu', 'trinh bao', 'co quan co tham quyen')) and any(t in q for t in ('coc', 'gia mao', 'cat lien lac', 'lua dao')):
        keys += ['evidence_messages', 'evidence_payment', 'evidence_recipient']
    if any(t in q for t in ('anh can cuoc', 'anh cccd', 'anh giay to')) and any(t in q for t in ('luu', 'su dung')):
        keys += ['privacy_purpose', 'privacy_storage', 'privacy_transfer']
    if 'thong tin ca nhan' in q and any(t in q for t in ('sai muc dich', 'yeu cau xu ly')):
        keys += ['privacy_request', 'privacy_form', 'privacy_recipient']
    return {k: FACETS[k][0] for k in dict.fromkeys(keys)}


def _expresses(key, text):
    return all(any(t in text for t in alternatives) for alternatives in FACETS[key][1])


def source_facets(question, row):
    q = normalize_text(question)
    text = normalize_text(row.get('content', ''))
    category = row.get('category')
    found = {}
    found.update({k: label for k, label in question_facets(question).items() if _expresses(k, text)})
    if ('nen tang' in q and 'trach nhiem' in q
            and any(t in q for t in ('thong tin nguoi', 'nguoi dang', 'nguoi ban', 'nguoi cho thue'))):
        found.update({'platform_' + f: OPERATOR_LABELS[f] for f in operator_facets(
            dict(row, text=row.get('content', ''), parent_content=None))})
    if ('hop dong' in q and any(t in q for t in ('kiem tra', 'dieu khoan nao', 'luu y'))
            and category in ('housing_contract', 'student_housing')):
        groups = {
            'parties': ('thông tin các bên', ('ho ten', 'ten cua ca nhan', 'thong tin cac ben', 'chu the')),
            'rent': ('giá thuê', ('gia thue', 'tien thue')),
            'payment': ('thời hạn và cách thanh toán', ('thanh toan', 'tra tien')),
            'deposit': ('thỏa thuận tiền cọc', ('dat coc', 'tien coc', 'hoan coc')),
            'charges': ('chi phí dịch vụ', ('tien dien', 'tien nuoc', 'phi dich vu')),
            'handover': ('bàn giao và hiện trạng', ('ban giao', 'hien trang')),
            'termination': ('thời hạn và chấm dứt hợp đồng', ('cham dut', 'thoi han thue')),
        }
        found.update({'contract_' + f: label for f, (label, terms) in groups.items()
                      if any(t in text for t in terms)})
        # General contract provisions use "giá" / "giá giao dịch nhà ở";
        # they still support a rental-price checklist. Don't require the
        # writer to cite a secondary guide merely for its explicit "giá thuê".
        if re.search(r'\bgiá\b', row.get('content', ''), re.I):
            found['contract_rent'] = 'giá thuê'
    if ('moi gioi' in q and any(t in q for t in ('sai', 'khong dung', 'xu ly'))
            and category == 'housing_contract'):
        if any(t in text for t in ('giam tien dich vu', 'giam phi')):
            found['broker_fee'] = 'điều kiện giảm phí dịch vụ'
        if 'boi thuong' in text:
            found['broker_compensation'] = 'điều kiện bồi thường'
        if 'cham dut' in text and any(t in text for t in ('dich vu', 'hop dong')):
            found['broker_termination'] = 'chấm dứt dịch vụ và nghĩa vụ kèm theo'
    if ('thong tin ca nhan' in q and any(t in q for t in ('sai muc dich', 'yeu cau xu ly'))
            and category == 'privacy_data'):
        if 'yeu cau' in text and any(t in text for t in ('van ban', 'dien tu')):
            found['privacy_form'] = 'hình thức gửi yêu cầu'
        if any(t in text for t in ('gui', 'tiep nhan')) and any(t in text for t in ('ben kiem soat', 'ben xu ly')):
            found['privacy_recipient'] = 'bên tiếp nhận yêu cầu'
        if 'phan hoi' in text:
            found['privacy_response'] = 'phản hồi yêu cầu và điều kiện thời hạn'
        if any(t in text for t in ('ngung xu ly', 'han che xu ly', 'rut lai su dong y')):
            found['privacy_request'] = 'yêu cầu ngừng hoặc hạn chế xử lý theo điều kiện nguồn'
    return found


def coverage_requirements(question, contexts):
    required = {}
    for row in contexts:
        for key, label in source_facets(question, row).items():
            item = required.setdefault(key, dict(facet=key, label=label, source_ranks=[]))
            if row['rank'] not in item['source_ranks']:
                item['source_ranks'].append(row['rank'])
    return list(required.values())


def source_coverage(question, contexts):
    required = question_facets(question)
    supported = coverage_requirements(question, contexts)
    present = {r['facet'] for r in supported}
    missing = [dict(facet=k, label=label, source_ranks=[]) for k, label in required.items() if k not in present]
    return dict(status='partial' if missing else 'covered' if required or supported else 'not_evaluated',
                required_facets=list(required), supported_facets=supported, missing_facets=missing)


def answer_coverage(question, contexts, claim_records):
    required = coverage_requirements(question, contexts)
    missing = missing_answer_facets(question, contexts, claim_records)
    return dict(status='partial' if missing else 'covered' if required and claim_records else 'not_evaluated',
                required_facets=required, missing_facets=missing)


def missing_answer_facets(question, contexts, claim_records):
    expressed = set()
    for row in contexts:
        # A checklist can explain one source facet in separate accepted lines.
        # Join only claims citing this exact source, excluding source caveats.
        text = '\n\n'.join(c['text'] for c in claim_records
                           if c['kind'] != 'source_limit' and row['rank'] in c['source_ranks'])
        source_keys = source_facets(question, row)
        expressed.update(source_keys.keys() & source_facets(
            question, dict(row, content=text, parent_content=None, text=text)).keys())
    return [r for r in coverage_requirements(question, contexts) if r['facet'] not in expressed]


def coverage_repair_issues(missing):
    return [dict(claim_id='answer', code='answer_coverage_gap', facet=r['facet'],
                 source_ids=r['source_ranks'], reason='Chưa trình bày ý có trong nguồn đã chọn: ' + r['label'])
            for r in missing]
