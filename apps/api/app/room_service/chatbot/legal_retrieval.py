"""Legal vocabulary, transparent reranking and conservative evidence checks.

These rules improve recall; they never supply a legal answer or a tariff.
"""
from __future__ import annotations

import re

from .providers import normalize_text
from ..legal_knowledge.quality import usable_legal_text
from .topics import question_categories, required_evidence_categories, TOPICS, has_phrase

LEGAL_STOP_WORDS = {"toi", "minh", "giup", "xin", "hoi", "the", "nao", "sao", "la",
                    "va", "cua", "theo", "quy", "dinh", "duoc", "co", "khong", "ve"}


def legal_tokens(value: str) -> list[str]:
    return [word for word in re.findall(r"[a-z0-9]+", normalize_text(value))
            if len(word) > 1 and word not in LEGAL_STOP_WORDS]


def electricity_question(query: str) -> bool:
    value = normalize_text(query)
    return any(term in value for term in ("tien dien", "gia dien", "thu dien", "tinh dien", "kwh", "dinh muc dien"))


def rental_electricity_question(query: str) -> bool:
    value = normalize_text(query)
    return electricity_question(query) and not any(term in value for term in ("trom cap", "hanh lang", "duong day"))


def expand_legal_query(query: str) -> str:
    value = normalize_text(query)
    additions: list[str] = []
    from .evidence_units import human_reporting_question
    if 'criminal_law' in question_categories(query) and human_reporting_question(query):
        additions.append('khuyến cáo lưu giữ tài liệu tin nhắn chứng từ chuyển tiền lịch sử giao dịch trình báo cơ quan Công an tiếp nhận tố giác')
    if has_phrase(value, "hop dong") and any(term in value for term in ("truoc khi ky", "dieu khoan", "ghi ro")):
        additions.append("hợp đồng về nhà ở nội dung của hợp đồng giá thuê thời hạn phương thức thanh toán quyền nghĩa vụ")
    if any(term in value for term in ("tam tru", "thu tuc cu tru", "dang ky cu tru")) and not any(term in value for term in ("phat", "vi pham")):
        additions.append("đăng ký tạm trú điều kiện hồ sơ tờ khai chỗ ở hợp pháp tiếp nhận đăng ký")
        if 'cung cap' in value and 'trach nhiem' in value:
            additions.append('nghĩa vụ công dân cung cấp đầy đủ chính xác thông tin giấy tờ tài liệu về cư trú')
    if 'cu tru' in value and any(term in value for term in ('chuyen sang', 'chuyen phong', 'thay doi cho o')):
        additions.append('thay đổi chỗ ở đăng ký tạm trú mới')
    if any(term in value for term in ('phong chay', 'pccc', 'chay no')) and any(term in value for term in ('xem phong', 'dieu kien', 'nhieu phong')):
        additions.append('phòng cháy đối với nhà ở thiết bị điện bếp đun nấu phương tiện chữa cháy lối thoát nạn')
        if 'nhieu phong' in value:
            additions.append('danh mục cơ sở dịch vụ lưu trú nhà ở tập thể nhà đa năng nhà hỗn hợp')
    if any(term in value for term in ("thong tin ca nhan", "du lieu ca nhan", "anh can cuoc", "so dien thoai", "anh giay to")):
        additions.append("bảo vệ dữ liệu cá nhân quyền chủ thể sự đồng ý cung cấp tiết lộ công khai xử lý dữ liệu")
        if has_phrase(value, 'hop dong'):
            additions.append('hợp đồng về nhà ở họ tên cá nhân địa chỉ các bên nội dung hợp đồng')
        if any(has_phrase(value, phrase) for phrase in ('cu tru', 'tam tru')):
            additions.append('đăng ký tạm trú hồ sơ tờ khai thay đổi thông tin cư trú chỗ ở hợp pháp')
    if any(term in value for term in ("dau hieu rui ro", "dau hieu lua dao", "khong cho xem phong")):
        additions.append("thủ đoạn gian dối chiếm đoạt tài sản lừa đảo điều kiện giao dịch dân sự đặt cọc")
    if any(term in value for term in ("chu tro", "chu nha")):
        additions.append("người cho thuê nhà")
    if any(term in value for term in ("o ghep", "o chung", "sinh vien")):
        additions.append("người thuê nhà định mức số người sử dụng điện" if electricity_question(query)
                         else "người thuê nhà")
    if rental_electricity_question(query):
        additions.append("thu tiền điện người thuê nhà giá bán lẻ điện sinh hoạt hóa đơn")
    if 'moi gioi' in value and any(t in value for t in ('phi','giay to','thoa thuan')):
        additions.append('hợp đồng dịch vụ trả tiền dịch vụ giá dịch vụ quyền nghĩa vụ bên sử dụng dịch vụ')
    if 'nuoc' in value and 'can tho' in value:
        additions.append('Quy định giá nước sạch sinh hoạt trên địa bàn thành phố Cần Thơ giá tiêu thụ nước')
    if any(t in value for t in ('chia se sai','xu ly nhu the nao','rut lai')) and 'privacy_data' in question_categories(query):
        additions.append('thực hiện quyền chủ thể dữ liệu cá nhân yêu cầu rút lại hạn chế xử lý xóa dữ liệu thủ tục thời hạn')
    if any(term in value for term in ("phat", "xu ly", "thu thua", "hoan tra")):
        additions.append("xử phạt vi phạm hoàn trả số tiền thu thừa khắc phục hậu quả")
    return query + (". " + ". ".join(additions) if additions else "")


def rental_evidence(content: str) -> bool:
    value = normalize_text(content)
    return any(term in value for term in ("tien dien", "gia dien", "gia ban le dien", "su dung dien", "mua dien")) and any(term in value for term in
                                   ("thue nha", "nha cho thue", "chu nha", "sinh vien"))


def rerank_legal(query: str, rows: list[dict], limit: int = 30) -> list[dict]:
    rental = rental_electricity_question(query)
    question = normalize_text(query)
    penalty = any(word in question for word in ("phat", "xu ly", "thu thua", "hoan tra"))
    categories = question_categories(query)
    private_rental = ("housing_contract" in categories and any(has_phrase(question, term) for term in ("thue", "tro", "phong"))
                      and not any(has_phrase(question, term) for term in ("mua ban", "thue mua", "tai san cong", "nha cong vu")))
    for row in rows:
        value = normalize_text(row["content"])
        base = float(row.get("similarity_score", 0))
        if rental and 'ky tuc xa' in value and 'ky tuc xa' not in question and 'nguoi thue nha' not in value:
            row['similarity_score']=0.0
            continue
        if row.get('category') == 'residence' and 'residence' in categories:
            collective_query = any(term in question for term in ('ky tuc xa', 'khu tap trung', 'co so tap trung', 'dang ky tap the'))
            collective_rule = 'ky tuc xa' in value or ('danh sach' in value and 'don vi quan ly' in value)
            if collective_rule and not collective_query:
                row['similarity_score'] = 0.0
                continue
        if private_rental and row.get("category") == "housing_contract":
            scope_heading = normalize_text(str(row.get('heading') or ''))
            specific_other = any(has_phrase(value, term) for term in ("mua ban", "thue mua", "tai san cong", "nha cong vu"))
            ordinary_rental = re.search(r"\bthue\b(?!\s+mua)", value)
            general_contract = bool(re.search(r'\bdieu\s+\d+[a-z]?[.]?\s+hop dong ve nha o(?:\s+khoan \d+)?$', scope_heading))
            if re.search(r'^(?:\d+[.]\s*)?(?:doi voi|truong hop) (?:hop dong )?(?:mua ban|thue mua|cho thue mua)',value):
                general_contract = False
            if specific_other and not ordinary_rental and not general_contract:
                row["similarity_score"] = 0.0
                continue
        if row.get("category") and categories:
            if row["category"] not in categories:
                row["similarity_score"] = 0.0
                continue
            heading = normalize_text(str(row.get("heading") or ""))
            from .evidence_units import human_reporting_question, reporting_evidence_row
            if row['category']=='criminal_law' and human_reporting_question(query):
                if reporting_evidence_row(row):base += 1.25
                if 'dieu 146.' in heading and 'khoan 1' in heading:base += .9
                if 'dieu 145.' in heading and 'khoan 2' in heading:base += .6
                if 'kien nghi khoi to' in value and 'co quan nha nuoc' in value and 'ca nhan' not in value:base -= 1.1
                if 'thong bao bang van ban' in value and 'vien kiem sat' in value:base -= 1.0
            if row.get('source_id')=='electricity-cantho-guidance':
                if any(t in question for t in ('thong bao','so dien da su dung','cach tinh','kiem tra','hoa don','doi chieu')):
                    base += 1.2
                else:
                    base -= .7
            meaningful = set(legal_tokens(query)) - {"sinh", "vien", "nguoi", "thue", "nha", "tro", "phong", "can", "nen", "nhung", "gi"}
            overlap = len(meaningful & set(legal_tokens(value))) / max(1, len(meaningful))
            heading_overlap = len(meaningful & set(legal_tokens(heading))) / max(1, len(meaningful))
            primary = row["category"] == categories[0]
            direct = any(has_phrase(value + " " + heading, p) for p in TOPICS.get(categories[0], ()))
            own_evidence = any(has_phrase(value + " " + heading, p) for p in TOPICS.get(row["category"], ()))
            contract_identity = (row['category'] == 'housing_contract' and 'privacy_data' in categories
                                 and 'hop dong ve nha o' in heading
                                 and any(term in value for term in ('ho va ten', 'ho ten', 'dia chi')))
            rental_authority = (row['category'] == 'housing_contract' and 'quyen cho thue' in question
                                and any(term in heading for term in ('dieu kien', 'ben tham gia'))
                                and any(term in value for term in ('chu so huu', 'uy quyen', 'cho thue')))
            if not primary and not direct and not contract_identity and not rental_authority and not (own_evidence and overlap >= 0.2):
                row["similarity_score"] = 0.0
                continue
            base = 0.5 * base + 0.3 * overlap + (0.18 if primary else 0.1)
            base += 0.12 * heading_overlap
            if "housing_contract" in categories and any(term in question for term in ("truoc khi ky", "ghi ro")):
                if any(term in heading for term in ("noi dung cua hop dong", "hop dong ve nha o")):
                    base += 0.25
            if row['category'] == 'housing_contract':
                if 'coc' in question and 'dat coc' in heading and any(term in question for term in ('ghi ro', 'ngay thanh toan', 'ghi trong')):
                    base += .8 if 'bao dam giao ket' in value or 'bao dam giao ket' in normalize_text(str(row.get('parent_content') or '')) else .1
                if any(term in question for term in ('tien thue', 'gia thue')) and 'hop dong ve nha o' in heading and 'gia giao dich' in value:
                    base += .45
                if 'tang gia thue' in question and any(term in heading for term in ('sua doi hop dong', 'gia thue')):
                    base += .5
                if 'tien coc' in question and not any(term in question for term in ('huy hop dong','don phuong','vi pham')):
                    if 'huy bo hop dong' in heading:
                        base -= .6
            if "residence" in categories and not penalty and ("xu phat" in value or "phat tien" in value):
                base -= 0.25
            if "privacy_data" in categories and any(term in question for term in ("cong khai", "chia se", "luu", "su dung", "ca nhan")):
                if 'cong khai' in question and 'cong khai du lieu ca nhan' in heading:
                    base += 1.0
                if any(t in question for t in ('chia se sai','xu ly nhu the nao')) and 'thuc hien quyen cua chu the' in heading:
                    base += 1.0
                if any(term in heading + " " + value for term in ("quyen cua chu the", "su dong y", "hanh vi bi nghiem cam", "nguyen tac bao ve", "cung cap du lieu", "tiet lo du lieu")):
                    base += 0.3
                if "xuat nhap canh" in value:
                    base -= 0.55
                if row['category']=='privacy_data':
                    if 'tre em' in heading and not any(term in question for term in ('tre em','chua thanh nien','giam ho')):
                        base -= .65
                    if any(term in heading for term in ('tuyen dung','nguoi lao dong')) and not any(term in question for term in ('tuyen dung','lao dong','viec lam')):
                        base -= .65
                    if 'ghi am, ghi hinh tai noi cong cong' in heading and not any(term in question for term in ('camera','noi cong cong','ghi hinh')):
                        base -= .65
                    if 'nguyen tac bao ve' in heading and 'pham vi' in value and 'muc dich' in value:
                        base += .65
                    if any(term in heading for term in ('su dong y','thu thap, phan tich')):
                        if any(term in value for term in ('tru truong hop phap luat','tu nguyen','muc dich xu ly')):
                            base += .5
                    if any(term in question for term in ('cung cap','yeu cau','hop dong','thu thap','thong tin ca nhan')) and any(term in heading+' '+value for term in ('ngung xu ly','rut lai su dong y','han che xu ly')) and not any(term in question for term in ('ngung','xoa','rut lai','han che','chia se sai')):
                        base -= .5
                if "thong bao vi pham" in heading and not any(term in question for term in ("thong bao vi pham", "su co", "ro ri", "bi chia se")):
                    base -= 0.35
            if 'privacy_data' in categories and 'housing_contract' in categories and row['category'] == 'housing_contract':
                if 'hop dong ve nha o' in heading and any(term in value for term in ('ho va ten', 'ho ten', 'dia chi')):
                    base += .75
            if 'residence' in categories and row['category'] == 'residence' and any(term in question for term in ('giay to', 'thong tin', 'thu tuc', 'dang ky')):
                if 'dieu kien dang ky tam tru' in heading and 'thu tuc' in question:
                    base += .8
                if any(term in heading for term in ('dang ky tam tru', 'ho so', 'thu tuc')):
                    base += .3
                if any(term in question for term in ('giay to', 'thong tin', 'ho so')) and 'ho so' in heading:
                    base += .35
                    if any(term in value for term in ('to khai', 'giay to, tai lieu chung minh')):
                        base += .35
                if 'trach nhiem' in question and 'cung cap' in question and 'nghia vu' in heading and 'cung cap' in value:
                    base += .65
            if row['category']=='residence' and 'cu tru' in question and any(term in question for term in ('chuyen sang','chuyen phong','thay doi cho o')):
                if 'dang ky tam tru' in heading and 'dang ky tam tru moi' in value:
                    base += 1.25
            if row['category'] == 'fire_safety':
                if 'nhieu phong' in question and 'phu luc i.' in heading and 'co so dich vu luu tru' in value:
                    base += 1.1
                if any(term in question for term in ('xem phong', 'dieu kien', 'nhieu phong')) and 'phong chay doi voi nha o' in heading:
                    base += .55
                    if 'ket hop' not in heading:
                        base += .25
                    if any(term in value for term in ('dieu kien an toan', 'dieu kien ve chua chay')):
                        base += .3
                if 'nhieu phong' in question and any(t in heading for t in ('phong chay doi voi co so','phong chay doi voi nha o')):
                    base += .5
                    if 'huong dan viec ket noi' in value and 'ket noi' not in question:
                        base -= .5
                if 'trach nhiem' in question and 'trach nhiem' in heading and any(term in value for term in ('nguoi thue', 'chu ho gia dinh')):
                    base += .45
            if row['category']=='criminal_law' and 'lua dao' in question and 'toi lua dao' in heading:
                if 'thu doan gian doi' in value and not any(term in question for term in ('muc phat','muc an','bao nhieu nam')):
                    base += .8
            if row['category']=='criminal_law' and any(t in question for t in ('co quan co tham quyen','trinh bao','to giac')):
                if any(t in heading for t in ('thu tuc tiep nhan to giac','trach nhiem tiep nhan','to giac, tin bao')):
                    base += .85
            if row['category']=='real_estate_brokerage' and 'moi gioi' in question and any(t in question for t in ('phi','giay to','thoa thuan')):
                if 'ca nhan moi gioi' in value and 'doanh nghiep' in value and 'khach hang' not in value:
                    base -= .9
                if any(t in heading for t in ('tra tien dich vu','hop dong dich vu','quyen cua ben su dung dich vu','noi dung cua hop dong')):
                    base += .85
                if ('noi dung chinh cua hop dong' in heading and 'hop dong kinh doanh dich vu' in value
                        and all(t in value for t in ('phi dich vu','phuong thuc','thoi han thanh toan'))):
                    base += 1.2
            if row['category'] in ('criminal_law', 'ecommerce_platform') and 'khuyen cao' in value:
                if any(term in question for term in ('kiem tra', 'bang chung', 'cung cap thong tin', 'luu lai', 'lien ket la')):
                    base += .45
            if rental_authority:
                base += .35
                if any(term in value for term in ('chu so huu', 'uy quyen')):
                    base += .45
            preventive_risk = "criminal_law" in categories and any(term in question for term in ("truoc khi", "khong cho xem", "dau hieu rui ro"))
            if preventive_risk:
                if any(term in heading + " " + value for term in ("gian doi", "lua dao", "giao dich dan su", "chiem doat")):
                    base += 0.3
                if any(term in heading for term in ("tham quyen giai quyet", "trach nhiem tiep nhan", "kien nghi khoi to")):
                    base -= 0.4
            # Introductory editorial metadata identifies a source but is not
            # an operative legal clause answering a question about obligations.
            if not heading and any(term in value for term in ("ghi chu ngu canh", "ban trich tuyen nghien cuu")):
                row["similarity_score"] = 0.0
                continue
            if heading and any(has_phrase(heading, p) for p in TOPICS.get(categories[0], ())):
                base += 0.1
        if rental:
            if not rental_evidence(str(row.get("heading") or "") + " " + row["content"]):
                row["similarity_score"] = 0.0
                continue
            phrases = ("thu tien dien", "tien dien", "nguoi thue nha", "dinh muc", "hoa don")
            coverage = sum(phrase in value for phrase in phrases) / len(phrases)
            base = 0.45 * base + 0.35 + 0.2 * coverage
            if penalty and any(term in value for term in ("phat tien", "hoan tra", "thu thua")):
                base += 0.15
            elif not penalty and "vi pham" in normalize_text(str(row.get("heading") or "")):
                base -= 0.2
        row['_rerank_score'] = base
        row["similarity_score"] = round(min(1.0, base), 6)
    return sorted((row for row in rows if row["similarity_score"] > 0
                   and usable_legal_text(row["content"])),
                  key=lambda row: (-row.get('_rerank_score', row["similarity_score"]), row["chunk_id"]))[:limit]


def diversified_legal_rows(query: str, rows: list[dict], limit: int) -> list[dict]:
    """Reserve a relevant candidate for each explicit facet before extra matches."""
    categories = required_evidence_categories(query)
    reserved = []
    from .evidence_units import requested_contract_facets, contract_facets, human_reporting_question, reporting_evidence_row
    if human_reporting_question(query):
        candidate=next((r for r in rows if reporting_evidence_row(r)),None)
        if candidate is not None:reserved.append(candidate)
    needed = requested_contract_facets(query)
    for facet in ('deposit','rent','payment'):
        if facet in needed:
            candidate = next((r for r in rows if facet in contract_facets(r)), None)
            if candidate is not None:
                reserved.append(candidate)
    if len(categories) > 1:
        for category in categories:
            candidate = next((row for row in rows if row.get('category') == category), None)
            if candidate is not None:
                reserved.append(candidate)
    unique = []
    seen = set()
    for row in reserved + rows:
        group = (row['document_id'], row.get('heading') or row['chunk_id'])
        if group not in seen:
            seen.add(group)
            unique.append(row)
    return unique[:limit]


def legal_completion_status(answer: str) -> str:
    """Report incomplete answers independently of provider or citation validity."""
    # A quoted statutory condition is evidence, not the assistant's abstention.
    visible = re.sub(r'“[^”]*”|"[^"\n]*"', '', answer, flags=re.S)
    limitation = re.compile(r'\b(?:chua (?:tim thay|co (?:can cu|du lieu|thong tin)|du can cu|xac minh|ket luan|tong hop)|khong (?:du can cu|the ket luan))\b')
    if not limitation.search(normalize_text(visible)):
        return 'complete'
    supported = []
    # A citation after a multiline quotation supports its earlier lines too.
    if any(len(legal_tokens(m[1]))>=8 for m in re.finditer(r'“(.*?)”\s*\[\d+\]',answer,re.S)):
        return 'partial'
    for segment in re.split(r'\n+|(?<=[.!?])\s+', answer):
        norm = normalize_text(segment)
        if limitation.search(norm) or not re.search(r'\[\d+\]', segment):
            continue
        if any(term in norm for term in ('thong tin tham khao', 'mo nguon tham khao', 'kiem tra dieu kien', 'khong thay the tu van')):
            continue
        if len(legal_tokens(segment)) >= 8:
            supported.append(segment)
    return 'partial' if supported else 'insufficient'


def _citation_scope_issues(segment: str, cited: list[dict]) -> list[str]:
    issues = []
    norm = normalize_text(segment)
    heading_articles = {n for row in cited for n in re.findall(r'Điều\s+(\d+)\b', str(row.get('heading') or ''), re.I)}
    claim_articles = set(re.findall(r'Điều\s+(\d+)\b', segment, re.I))
    if heading_articles and claim_articles - heading_articles:
        issues.append('Số điều được khẳng định không khớp điều khoản của nguồn trích dẫn.')
    heading_clauses = {n for row in cited for n in re.findall(r'Khoản\s+(\d+)\b', str(row.get('heading') or ''), re.I)}
    claim_clauses = set(re.findall(r'Khoản\s+(\d+)\b', segment, re.I))
    if heading_clauses and claim_clauses - heading_clauses:
        issues.append('Số khoản được khẳng định không khớp khoản của nguồn trích dẫn.')
    evidence = normalize_text(' '.join(str(row.get('heading') or '') + ' ' + row['content'] for row in cited))
    normative = re.search(r'\b(?:phai|bat buoc|co nghia vu|nghia vu cua|co trach nhiem|trach nhiem cua)\b', norm)
    if re.search(r'\bchi (?:duoc|co quyen|co the|phai)\b',norm) and not re.search(r'\bchi\b',evidence):
        issues.append('Nguồn nêu một trường hợp cụ thể, chưa loại trừ các căn cứ khác; không tự kết luận chỉ được áp dụng trong trường hợp đó.')
    if normative and not any(has_phrase(evidence, p) for p in ('phai', 'nghia vu', 'trach nhiem', 'bat buoc', 'khong duoc', 'nghiem cam')):
        issues.append('Nguồn mô tả nội dung/công việc chưa xác nhận nghĩa vụ được khẳng định.')
    if any(has_phrase(norm, p) for p in ('co quyen', 'duoc phep')) and not any(has_phrase(evidence, p) for p in ('quyen', 'duoc', 'cho phep')):
        issues.append('Nguồn được trích chưa xác nhận quyền hoặc sự cho phép được khẳng định.')
    if normative and any(has_phrase(norm, p) for p in ('nguoi thue', 'ben thue')):
        if any(has_phrase(evidence, p) for p in ('uy ban nhan dan', 'co quan cong an')) and not any(has_phrase(evidence, p) for p in ('nguoi thue', 'ben thue', 'nguoi su dung')):
            issues.append('Không chuyển trách nhiệm của cơ quan kiểm tra thành nghĩa vụ của người thuê.')
    if any(re.search(r'(?:\btru(?: truong(?: hop)?)?|\btheo quy|\btru tru[o]?)[ .…]*$', normalize_text(row['content'])) for row in cited):
        issues.append('Nguồn trích dẫn bị cụt điều kiện hoặc ngoại lệ; chưa đủ để kết luận.')
    return issues


def evidence_issues(answer: str, chunks: list[dict], query: str) -> list[str]:
    """Deterministic guard, not a claim of full semantic entailment verification."""
    issues = []
    normalized = normalize_text(answer)
    if any(term in normalized for term in (
        "phap luat khong co quy dinh", "khong co quy dinh cu the", "khong co quy dinh ve",
        "khong co van ban nao", "luat khong quy dinh",
    )) or re.search(r"(?:phap luat|luat).{0,45}khong(?: co)? (?:quy dinh|neu)", normalized):
        issues.append("Không thể kết luận pháp luật không có quy định từ các đoạn truy xuất.")
    if rental_electricity_question(query) and not any(rental_evidence(row["content"]) for row in chunks):
        issues.append("Chưa tìm thấy nguồn trực tiếp về tiền điện của người thuê nhà.")
    evidence_text = normalize_text(" ".join(row["content"] for row in chunks))
    if rental_electricity_question(query):
        if any(term in normalized for term in ("phai bang", "phai dung bang")) and "khong duoc vuot qua" in evidence_text:
            issues.append("Giữ đúng giới hạn 'không được vượt quá'; không đổi thành 'phải bằng'.")
        if "lai suat" in normalized and "thoa thuan" not in normalized and "thoa thuan" in evidence_text:
            issues.append("Lãi suất hoàn trả phải giữ điều kiện do hai bên thỏa thuận trong hợp đồng.")
        if "khong ke khai hoac" in normalized or "khong ke khai du hoac" in normalized:
            issues.append("Không đổi điều kiện đồng thời 'dưới 12 tháng và không kê khai đủ người' thành 'hoặc'.")
        if (any(term in normalized for term in ("bac 2", "3 4", "04 nguoi", "4 nguoi", "bon nguoi"))
                and "ke tu ngay thuc hien" in evidence_text
                and not any(term in normalized for term in ("dieu chinh", "chuyen tiep", "thoi diem ap dung"))):
            issues.append("Phải nêu điều kiện hiệu lực gắn với lần điều chỉnh giá điện; chưa xác minh mốc thì không khẳng định đang áp dụng.")
    sources = {int(row["rank"]): normalize_text(row["content"] + " " + str(row.get("heading") or ""))
               for row in chunks}
    # Each cited sentence must share meaningful vocabulary with its own sources.
    for segment in re.split(r"\n+|(?<=[.!?])\s+", answer):
        refs = [int(ref) for ref in re.findall(r"\[(\d+)\]", segment)]
        if not refs:
            segment_normalized = normalize_text(segment)
            legal_assertion = re.search(r"\b(phải|bắt buộc|được phép|có quyền|có nghĩa vụ|vi phạm|chịu trách nhiệm|bị xử lý|xử phạt|bồi thường|hoàn trả)\b", segment, re.I)
            numeric_claim = re.search(r"\b(?:\d+(?:[.,]\d+)*|một|hai|ba|bốn|năm|sáu|bảy|tám|chín|mười)\s*(?:triệu|đồng|ngày|tháng|năm)\b", segment, re.I)
            # Asking for a case fact (e.g. a 12-month lease) is not asserting a
            # legal entitlement, deadline or amount. Legal premises stay checked.
            contract_fact_question = (re.search(r'\bhop dong\b.*\b(?:dieu khoan|quy dinh|thoa thuan)\b', segment_normalized)
                                      and not re.search(r'\b(?:phai|bat buoc|duoc phep|co quyen|co nghia vu)\b', segment_normalized))
            if segment.rstrip().endswith('?') and (not legal_assertion or contract_fact_question):
                continue
            limitation = any(term in segment_normalized for term in ("chua tim thay", "chua du can cu", "khong du can cu", "chua xac minh", "chua ket luan"))
            advice = any(term in segment_normalized for term in ("kiem tra", "doi chieu", "khuyen nghi", "loi khuyen"))
            if not limitation and (legal_assertion or (numeric_claim and not advice)):
                issues.append("Kết luận hoặc số liệu chưa gắn trích dẫn trực tiếp.")
            continue
        evidence = " ".join(sources.get(ref, "") for ref in refs)
        if not evidence:
            issues.append("Trích dẫn không có nguồn tương ứng.")
            continue
        segment_normalized = normalize_text(segment)
        scoped_absence = (any(term in segment_normalized for term in ('chua tim thay can cu', 'chua du can cu', 'chua xac minh'))
                          or re.search(r'\bnguon(?: tai lieu)?\b.{0,40}\bchua (?:neu|cung cap)\b', segment_normalized))
        # A list of missing topics ("mức phạt, bồi thường, hoàn trả") is not
        # an affirmative entitlement. Keep checking any separate modal or
        # actor/action clause appended to the disclosure of missing evidence.
        additional_assertion = re.search(
            r'(?:\bnhung\b|\btuy nhien\b|\bdo do\b|\bvi vay\b|\bva\b|[,;]).*'
            r'(?:\b(?:phai|bat buoc|co quyen|co nghia vu|bi phat)\b'
            r'|\b(?:chu nha|chu tro|ben cho thue|nguoi thue|ben thue)\b.{0,40}\b(?:boi thuong|hoan tra|hoan lai)\b'
            r'|\b(?:duoc|se)\s+(?:boi thuong|hoan tra|hoan lai)\b)', segment_normalized)
        if scoped_absence and not additional_assertion:
            # A statement about missing evidence cannot share vocabulary with the
            # missing rule. General claims that no law exists are rejected above.
            continue
        issues.extend(_citation_scope_issues(segment, [row for row in chunks if int(row['rank']) in refs]))
        for predicates, source_terms in (
            (("xu ly hanh chinh", "xu phat", "bi phat"), ("xu ly hanh chinh", "xu phat", "bi phat", "phat tien", "canh cao")),
            (("boi thuong",), ("boi thuong",)),
            (("hoan tra", "hoan lai"), ("hoan tra", "hoan lai", "tra lai")),
        ):
            if any(term in segment_normalized for term in predicates) and not any(term in evidence for term in source_terms):
                issues.append("Nguồn trích dẫn chưa nêu căn cứ cho kết luận về xử lý, bồi thường hoặc hoàn trả.")
        terms = set(legal_tokens(re.sub(r"\[\d+\]", "", segment)))
        if terms and len(terms & set(legal_tokens(evidence))) / len(terms) < 0.18:
            issues.append("Nội dung câu trả lời không khớp từ vựng của nguồn trích dẫn.")
        amounts = re.findall(r"\b\d{1,3}(?:[.,]\d{3}){2,}\b", segment)
        for match in re.finditer(r"(\d+(?:[.,]\d+)?)\s*(?:[-–]|đến)?\s*(\d+(?:[.,]\d+)?)?\s*triệu", segment, re.I):
            amounts.extend(str(round(float(value.replace(",", ".")) * 1_000_000))
                           for value in match.groups() if value)
        for amount in amounts:
            digits = re.sub(r"\D", "", amount)
            source_numbers = {re.sub(r"\D", "", n) for n in re.findall(r"\d[\d.,]*", evidence)}
            if digits not in source_numbers:
                issues.append("Số tiền nêu trong câu trả lời chưa được nguồn trích dẫn xác nhận.")
    return list(dict.fromkeys(issues))


def append_commencement_evidence(answer: str, chunks: list[dict], query: str) -> str:
    """Retain an essential commencement condition verbatim, never invent a date.

    Only supplements an otherwise generated answer when its retrieved source has
    an explicit delayed-commencement phrase and the answer omitted that condition.
    """
    issues = evidence_issues(answer, chunks, query)
    if not any(issue.startswith("Phải nêu điều kiện hiệu lực") for issue in issues):
        return answer
    for row in chunks:
        match = re.search(r"có hiệu lực(?: thi hành)? k[ểê] từ ngày thực hiện[^.\n]{20,700}(?:\.|$)", row["content"], re.I)
        if match:
            return answer + f"\n\nĐiều kiện hiệu lực trong nguồn: “{match[0].rstrip('.')}” [{row['rank']}]."
    return answer
