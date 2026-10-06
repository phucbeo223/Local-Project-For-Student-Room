"""Conservative quantity checks; semantic agreement still belongs to the judge.

Numbers are tied to their clause, rate unit, actor and event. This gate can
reject a match; passing it is never a certificate of legal correctness.
"""
from decimal import Decimal
from fractions import Fraction
import re
import unicodedata


def normalized(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text.casefold().replace('đ', 'd'))
                   if not unicodedata.combining(c))


NUMBER = r'\d+(?:[.,]\d+)*'
QUANTITY = re.compile(r'(?<![\w/])(' + NUMBER + r'(?:\s*(?:[-–]|den)\s*' + NUMBER + r')?)\s*'
                      r'(nghin|ngan|trieu|dong|vnd|gio|ngay|thang|nam|kwh|m[3³]|%)(?=$|\W)')
COUNT = re.compile(r'(?<![\w/])(' + NUMBER + r'(?:\s*(?:[-–]|den)\s*' + NUMBER + r')?|mot|hai|ba|bon)\s*'
                   r'(nguoi|dinh muc(?: ho gia dinh)?|ho so|ho(?: gia dinh)?|loi thoat(?: nan| hiem)?|binh(?: chua chay)?|tang|phong)(?=$|\W)')


def number_value(value):
    if ',' in value:
        value = value.replace('.', '').replace(',', '.')
    elif re.fullmatch(r'[1-9]\d{0,2}(?:\.\d{3})+', value):
        value = value.replace('.', '')
    return Fraction(Decimal(value))


def context_signature(clause, start, end):
    before, after = clause[max(0, start-360):start], clause[end:end+90]
    event = None
    if re.search(r'sinh song|cu tru|o tai|tam tru tu|lao dong,? hoc tap|vi muc dich khac tu', before): event = 'residence_duration'
    elif re.search(r'nop|thoi han dang ky|giai quyet|xu ly|thong bao|bao truoc', before): event = 'procedure_deadline'
    actor = None
    # Use the nearest explicitly named actor, never an actor in another clause.
    actors = [(m.start(), key) for key, pattern in (
        ('individual', r'ca nhan'), ('organization', r'to chuc'),
        ('tenant', r'nguoi thue|ben thue|sinh vien'), ('landlord', r'chu tro|ben cho thue'))
        for m in re.finditer(pattern, before[-60:])]
    if actors: actor = max(actors)[1]
    bound = None
    if re.search(r'tu\s*$', before) and re.search(r'^\s*(?:tro len|vao)', after): bound = 'minimum'
    elif re.search(r'toi thieu|it nhat', before): bound = 'minimum'
    elif re.search(r'trong(?: vong)?\s*$|khong qua\s*$|toi da\s*$', before): bound = 'maximum'
    rate = re.match(r'\s*(?:dong|vnd)?\s*(?:/|moi|tren)\s*(kwh|m[3³]|nguoi|thang|ngay)', after)
    return dict(event=event, actor=actor, bound=bound,
                rate=rate[1].replace('³', '3') if rate else None)


def quantities(text):
    text = normalized(text)
    result = []
    # Decimal/thousand separators are not sentence boundaries.
    for clause in re.split(r'(?<=[.!?;])\s+', text):
        clause=' '.join(clause.split())
        for match in QUANTITY.finditer(clause):
            span, unit = match.groups()
            scale = Fraction(1, 100) if unit == '%' else {'trieu':1000000, 'nghin':1000, 'ngan':1000}.get(unit, 1)
            canonical = 'ratio' if unit == '%' else 'dong' if unit in ('dong','vnd','trieu','nghin','ngan') else unit.replace('³', '3')
            signature=context_signature(clause, match.start(), match.end())
            if canonical not in ('gio','ngay','thang','nam'): signature.update(event=None,bound=None)
            result.append(dict(values=[str(number_value(n)*scale) for n in re.findall(NUMBER, span)],
                unit=canonical, span=match[0], clause=clause,
                **signature))
        for match in COUNT.finditer(clause):
            value,unit=match.groups()
            canonical='ho_so' if unit=='ho so' else 'dinh_muc' if unit=='dinh muc' else 'ho' if unit.startswith(('ho','dinh muc')) else 'loi_thoat' if unit.startswith('loi thoat') else 'binh' if unit.startswith('binh') else unit
            signature=context_signature(clause,match.start(),match.end())
            signature['event']=None
            per=re.match(r'\s*(?:/|moi|tren)\s*(tang|phong)',clause[match.end():])
            if per: signature['rate']=per[1]
            amount={'mot':1,'hai':2,'ba':3,'bon':4}.get(value)
            values=[str(amount)] if amount is not None else [str(number_value(n)) for n in re.findall(NUMBER,value)]
            result.append(dict(values=values,
                unit=canonical,span=match[0],clause=clause,**signature))
        for match in re.finditer(r'(?<![\d/])(\d+)\s*/\s*(\d+)(?![\d/])', clause):
            before, after = clause[:match.start()], clause[match.end():]
            if re.search(r'\bngay\s*$', before) or re.match(r'\s*/\s*\d', after): continue
            # Document numbers/years (TT 60/2025, 25/2018) are not ratios.
            if int(match[2]) >= 1000 or re.search(r'\b(?:tt|nd|qh|qd|so)\s*$', before): continue
            if not re.search(r'dinh muc|ty le|phan|suat', before[-30:]+after[:35]): continue
            if int(match[2]):
                result.append(dict(values=[str(Fraction(int(match[1]),int(match[2])))],
                    unit='ratio', span=match[0], clause=clause,
                    **context_signature(clause,match.start(),match.end())))
    return result


def quantity_errors(reference, answer):
    expected, observed = quantities(reference), quantities(answer)
    errors = []
    for claim in expected:
        equal = [q for q in observed if q['values'] == claim['values'] and q['unit'] == claim['unit']]
        compatible = [q for q in equal if all(not claim[k] or q[k] == claim[k]
                      for k in ('event','bound','rate'))
                      and (not claim['actor'] or not q['actor'] or q['actor']==claim['actor'])]
        if compatible: continue
        errors.append(dict(code='quantity_context_mismatch' if equal else 'quantity_or_unit_missing',
            expected=claim, observed=equal or observed,
            reason='Cần đúng giá trị, đơn vị, chủ thể, sự kiện bắt đầu và điều kiện; số giống nhau chưa đủ.'))
    return errors
