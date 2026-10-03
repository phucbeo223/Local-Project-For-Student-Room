"""Evidence coverage and whole-unit assembly; these rules do not create legal facts."""
import re
from .providers import normalize_text


FACET_LABELS = {'deposit':'tiền cọc', 'rent':'tiền thuê', 'payment':'thanh toán'}


def human_reporting_question(question):
    q=normalize_text(question)
    return any(t in q for t in ('toi','chung toi','sinh vien','nguoi thue')) and any(
        t in q for t in ('trinh bao','luu lai bang chung','cung cap thong tin','luu chung cu'))


def reporting_evidence_row(row):
    body=normalize_text(row.get('text',row.get('content','')))
    return row.get('category')=='criminal_law' and any(t in body for t in ('luu giu','luu lai')) and any(
        t in body for t in ('tin nhan','chung tu chuyen tien','lich su giao dich'))


def requested_contract_facets(question):
    q = normalize_text(question)
    if not any(t in q for t in ('hop dong', 'dieu khoan', 'ghi ro')):
        return set()
    return {name for name, terms in {
        'deposit':('tien coc', 'dat coc', 'hoan coc'),
        'rent':('tien thue', 'gia thue'),
        'payment':('thanh toan', 'ngay tra tien', 'han tra tien'),
    }.items() if any(t in q for t in terms)}


def contract_facets(row):
    if row.get('category') != 'housing_contract':
        return set()
    value = normalize_text(' '.join(str(row.get(k) or '') for k in ('heading','text','content','parent_content')))
    return {name for name, terms in {
        'deposit':('dat coc', 'tien coc'),
        'rent':('gia giao dich', 'gia thue', 'tien thue'),
        'payment':('thoi han thanh toan', 'phuong thuc thanh toan', 'tra tien thue', 'ngay thanh toan'),
    }.items() if any(t in value for t in terms)}


def whole_supplementary_units(rows, budget=5500):
    """Use the full parent before filtering inventories; never emit middle fragments."""
    unique = {}
    for row in rows:
        key = row.get('provision_id') or (row['document_id'], row.get('heading'))
        if key in unique:
            if row.get('parent_content'):
                unique[key]['content'] = row['parent_content']
            continue
        unit = dict(row)
        if row.get('parent_content'):
            unit['content'] = row['parent_content']
            unit['context_complete'] = True
        else:
            siblings = [r for r in rows if (r['document_id'],r.get('heading')) == key]
            unit['content'] = '\n\n'.join(r['content'] for r in sorted(siblings,key=lambda r:r['chunk_index']))
            unit['context_complete'] = bool(siblings)
        unique[key] = unit
    chosen, size = [], 0
    for row in unique.values():
        introduction=(row.get('provision_metadata') or {}).get('article_context','')
        body=row['content'][len(introduction):].lstrip() if introduction and row['content'].startswith(introduction) else row['content']
        value = normalize_text(body)
        if (not value or 'noi nhan:' in value or re.search(
                r'^(?:\d+[.,]\s*)?(?:bai bo\b|cac quy dinh sau(?: day)? het hieu luc\b)', value)):
            continue
        if size + len(row['content']) <= budget:
            chosen.append(row); size += len(row['content'])
    return chosen


def scope_issues(question, parts):
    """Reject known actor mismatches; explain gaps without supplying a legal answer."""
    q = normalize_text(question)
    body = normalize_text(' '.join(p.get('text',p.get('content','')) for p in parts))
    issues = []
    if human_reporting_question(question) and 'criminal_law' in {p.get('category') for p in parts}:
        if not any(reporting_evidence_row(p) for p in parts):
            issues.append('Thủ tục nội bộ của cơ quan tiếp nhận chưa trả lời các tài liệu, tin nhắn hoặc chứng từ người trình báo cần lưu/cung cấp.')
    if 'moi gioi' in q and any(t in q for t in ('sinh vien','nguoi thue','phi','tra')):
        if 'doanh nghiep kinh doanh dich vu moi gioi' in body and not any(
                t in body for t in ('khach hang','nguoi thue','hop dong dich vu')):
            issues.append('Nguồn thù lao cá nhân môi giới với doanh nghiệp chưa trả lời phí người thuê trả.')
    if any(t in q for t in ('nhieu phong','nhieu tang')) and 'fire_safety' in {p.get('category') for p in parts}:
        if not any(t in body for t in ('nhieu tang','nhieu can ho','co so','kinh doanh')):
            issues.append('Cần căn cứ phân loại nhà trọ nhiều phòng và điều kiện tương ứng.')
        else:
            issues.append('Cần xác định loại hình sử dụng, số tầng, diện tích và quy chuẩn của nhà trọ để chọn đúng nhóm điều kiện; chưa kết luận chỉ từ số phòng.')
    if 'nen tang' in q and any(t in q for t in ('dang tin','thong tin','so dien thoai')):
        if 'dat hang truc tuyen' in body and not any(t in body for t in ('khong co chuc nang dat hang','dang tin','nen tang trung gian','dieu 17')):
            issues.append('Cần phân biệt nền tảng đăng tin với nền tảng có chức năng đặt hàng.')
    if 'dien' in q and any(t in q for t in ('thong bao','minh bach','san luong')):
        direct_notice=re.search(r'(?:thong bao|cong khai)[^.]{0,350}(?:nguoi thue|ben thue)',body)
        if not direct_notice or not any(t in body for t in ('san luong','luong dien','chi so')):
            issues.append('Chưa có nguồn trực tiếp về thông báo cách tính và sản lượng điện.')
    if 'nuoc' in q and any(t in q for t in ('can tho','dia phuong','uy ban')):
        if not any('cần thơ' in (p.get('document','')+' '+p.get('text','')).lower() for p in parts):
            issues.append('Cần văn bản địa phương Cần Thơ, phạm vi địa bàn và hiệu lực áp dụng.')
    if 'tam tru' in q and 'ai' in q and 'trach nhiem' in q and 'cung cap' in q:
        if not any(t in body for t in ('chu so huu co trach nhiem','chu ho co trach nhiem','nguoi cho thue co trach nhiem')):
            issues.append('Nguồn hiện có xác nhận nghĩa vụ của công dân và hồ sơ đăng ký; chưa có căn cứ riêng để kết luận toàn bộ nghĩa vụ cung cấp giấy tờ của chủ trọ.')
    if re.search(r'có hiệu lực(?: thi hành)? k[ểê] từ ngày thực hiện', ' '.join(p.get('text','') for p in parts),re.I):
        if not any(p.get('trigger_verified') for p in parts):
            issues.append('Nguồn có hiệu lực có điều kiện; chưa xác nhận văn bản/sự kiện kích hoạt.')
    return issues
