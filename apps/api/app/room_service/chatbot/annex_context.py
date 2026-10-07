"""Bound annexes by whole native Word rows, retaining their original headings."""
import re
from .providers import normalize_text


def whole_annex_rows(parent, question, matched_chunk, limit=5500):
    if not re.match(r'\s*Phụ lục\b', parent, re.I):
        return None
    table = bool(re.search(r'^\s*\|\s*\d+\s*\|', parent, re.M))
    starts = list(re.finditer(r'^\s*\|\s*\d+\s*\|' if table else r'^ *\d+\.\s', parent, re.M))
    if not starts:
        return None
    prefix = parent[:starts[0].start()]
    q = normalize_text(question)
    housing = any(t in q for t in ('nha tro', 'phong tro', 'cho thue', 'luu tru'))
    terms = ('nha chung cu', 'nha o tap', 'luu tru', 'nha nghi', 'nha khach', 'khach san')
    selected = []
    for i, start in enumerate(starts):
        end = starts[i+1].start() if i+1 < len(starts) else len(parent)
        body = parent[start.start():end]
        normalized = normalize_text(body)
        relevant = any(t in normalized for t in terms) if housing else matched_chunk.strip() in body
        if relevant:
            selected.append((start.start(), end, body))
    content = prefix + '\n'.join(row[2] for row in selected)
    if not selected or len(content) > limit:
        return None
    return dict(content=content, context_complete=True, context_scope='whole_annex_rows',
                annex_source_spans=[dict(start=s, end=e) for s, e, _ in selected],
                annex_header_span=dict(start=0, end=starts[0].start()))
