"""Local, quote-audited comparison. References never enter generation or embedding."""
import os
os.environ.setdefault('GIT_PYTHON_REFRESH', 'quiet')

import argparse
from collections import Counter
from datetime import datetime
import hashlib
from itertools import combinations, islice
import json
from pathlib import Path
import re
from typing import Literal, Union
from pydantic import BaseModel, ConfigDict, Field, create_model
from quantity_audit import quantity_errors, quantities
import question_bank_ragas as bank

POLICY = 'gemini_parent_context_semantic_audit_v17'


class Point(BaseModel):
    model_config = ConfigDict(extra='forbid')
    status: Literal['matched', 'missing', 'different']
    reference_quote: str = Field(min_length=8, max_length=100000)
    answer_quote: str = Field(max_length=48000)
    answer_quotes: list[str] = Field(default_factory=list, max_length=6)
    explanation: str = Field(min_length=5, max_length=350)


class Review(BaseModel):
    model_config = ConfigDict(extra='forbid')
    agreement: Literal['high', 'partial', 'low']
    points: list[Point] = Field(min_length=1, max_length=100)
    explanation: str = Field(min_length=10, max_length=800)


class SelectedPoint(BaseModel):
    model_config = ConfigDict(extra='forbid')
    status: Literal['matched', 'missing', 'different']
    reference_id: int = Field(ge=1, strict=True)
    answer_ids: list[int] = Field(max_length=6)
    explanation: str = Field(min_length=5, max_length=350)


class SelectedReview(BaseModel):
    model_config = ConfigDict(extra='forbid')
    agreement: Literal['high', 'partial', 'low']
    points: list[SelectedPoint] = Field(min_length=1, max_length=100)
    explanation: str = Field(min_length=10, max_length=800)


def selection_schema(reference_units, answer_units):
    """Constrain available IDs and the status/answer relationship at decoding."""
    if not reference_units or not answer_units: raise ValueError('No comparable fragments')
    ref_id_type = Literal[tuple(u['id'] for u in reference_units)]
    answer_id_type = Literal[tuple(u['id'] for u in answer_units)]
    # Keep the decision field first and the SAME field order in every union
    # branch. Otherwise choosing an early explanation field commits the local
    # grammar to a status before the model has emitted its actual decision.
    compared = create_model('DifferentFragment', __config__=ConfigDict(extra='forbid'),
        status=(Literal['different'], ...),
        reference_id=(ref_id_type, ...),
        answer_ids=(list[answer_id_type], Field(min_length=1, max_length=6)),
        explanation=(str, Field(min_length=5, max_length=350)))
    missing = create_model('MissingFragment', __config__=ConfigDict(extra='forbid'),
        status=(Literal['missing'], ...), reference_id=(ref_id_type, ...),
        answer_ids=(list[answer_id_type], Field(max_length=0)),
        explanation=(str, Field(min_length=5, max_length=350)))
    # If no selected answer combination could contain the required quantity,
    # prohibit matched at decoding, while the judge still chooses different or
    # missing and explains it. This is a rejection constraint, not a new score.
    eligible = tuple(u['id'] for u in reference_units
                     if not quantity_errors(clean(u['text']), clean('\n'.join(a['text'] for a in answer_units))))
    point_type = Union[compared, missing]
    if eligible:
        matched = create_model('MatchedFragment', __config__=ConfigDict(extra='forbid'),
            status=(Literal['matched'], ...), reference_id=(Literal[eligible], ...),
            answer_ids=(list[answer_id_type], Field(min_length=1,max_length=6)),
            explanation=(str,Field(min_length=5,max_length=350)))
        point_type = Union[matched,compared,missing]
    return create_model('FragmentReview', __base__=SelectedReview,
        points=(list[point_type], Field(min_length=1, max_length=100)))


def reference_fragments(text):
    """Literal, traceable clauses with inherited conditions, including colons.

    Omit only clearly introductory headings. A colon with an assertion,
    quantity or condition is a scored clause. Ancestor quotes stay separate
    from the literal text, so quote restoration cannot fabricate a span.
    """
    units, stack, cursor = [], [], 0
    for i, part in enumerate(literal_paragraphs(text), 1):
        start = text.index(part, cursor)
        end = start + len(part)
        cursor = end
        line_start = text.rfind('\n', 0, start) + 1
        indent = len(text[line_start:start].expandtabs(4))
        value = clean(part)
        colon = value.endswith(':')
        numbered = bool(re.match(r'\d+[.)]\s', value))
        while stack and (indent < stack[-1]['indent'] or
                         (indent == stack[-1]['indent'] and (colon or numbered))):
            stack.pop()
        # Conservative omission: unformatted prose defaults to a real clause.
        formatted = bool(re.match(r'^\s*(?:#{1,6}\s.+|(?:\d+[.)]\s*)?\*\*[^*]+\*\*\s*:?)\s*$', part))
        introduction = bool(re.match(r'^(?:ví dụ|cụ thể|bao gồm|các bước|các lưu ý|lưu ý|tham khảo)\s*:$', value))
        substantive = bool(re.search(r'\d|\b(?:nếu|khi|trường hợp|được|phải|không|có|cần|áp dụng|tính|từ|dưới|trên)\b', value))
        heading = colon and not substantive and (formatted or introduction)
        unit = dict(id=i, text=part, start=start, end=end,
                    parent_ids=[p['id'] for p in stack],
                    context_quotes=[p['text'] for p in stack])
        if len(value) >= 8 and not heading:
            units.append(unit)
        if colon:
            stack.append(dict(id=i, text=part, indent=indent))
    return units


def judge_schema(reference_units, answer_units):
    """One fixed slot per clause; semantic/numeric guards run after decoding."""
    answer_type = Literal[tuple(u['id'] for u in answer_units)]
    slots = {}
    for ref in reference_units:
        point = create_model('ReferencePoint'+str(ref['id']), __config__=ConfigDict(extra='forbid'),
            status=(Literal['matched', 'different', 'missing'], ...),
            reference_id=(Literal[ref['id']], ...),
            answer_ids=(list[answer_type], Field(max_length=6)),
            explanation=(str, Field(min_length=5, max_length=350)))
        slots['r'+str(ref['id'])] = (point, ...)
    points = create_model('AllReferencePoints', __config__=ConfigDict(extra='forbid'), **slots)
    return create_model('CompleteFragmentReview', __config__=ConfigDict(extra='forbid'),
        agreement=(Literal['high','partial','low'], ...), points=(points, ...),
        explanation=(str, Field(min_length=10, max_length=800)))


def matched_candidates(reference, answer_units):
    """Offer real ID combinations, never auto-select quotations or a status.

    Only numerical eligibility is precomputed. Passing does not establish
    semantic agreement. Include adjacent full clauses when necessary.
    """
    required=quantities(clean(reference))
    if not required: return None
    keys={(tuple(q['values']),q['unit']) for q in required}
    numbered=[u for u in answer_units if any((tuple(q['values']),q['unit']) in keys for q in quantities(clean(u['text'])))]
    present={(tuple(q['values']),q['unit']) for u in numbered for q in quantities(clean(u['text']))}
    if not keys<=present: return []
    by_id={u['id']:u for u in answer_units}
    found=set()
    def add(ids):
        ids=tuple(sorted(set(ids)))
        if 1<=len(ids)<=6 and not quantity_errors(clean(reference),clean('\n'.join(by_id[i]['text'] for i in ids))):
            found.add(ids)
    # Minimal numerical combinations can be disjoint; real model-selected
    # context may also span the preceding/following clause.
    for size in range(1,min(6,len(numbered))+1):
        for group in islice(combinations(numbered,size),4096):
            add([u['id'] for u in group])
            if len(found)>=16: break
        if found: break
    for index,u in enumerate(answer_units):
        if u not in numbered: continue
        for width in range(2,7):
            for start in (index,index-width+1):
                if start>=0 and start+width<=len(answer_units):
                    add([v['id'] for v in answer_units[start:start+width]])
    anchors=sorted(found,key=lambda ids:(len(ids),ids))[:16]
    for ids in anchors:
        for neighbor in (min(ids)-1,max(ids)+1):
            if neighbor in by_id: add([*ids,neighbor])
    return [list(ids) for ids in sorted(found,key=lambda ids:(len(ids),ids))[:40]]


def normalize_selection(raw, reference_units, answer_units):
    data=raw.model_dump()
    data['points']=list(data['points'].values())
    return selection_schema(reference_units,answer_units).model_validate(data)


def _abbreviation(text):
    return bool(re.search(r'(?:^|\s)(?:TP|TS|PGS|ThS|TX|TT|v\.v)\.$',text.strip(),re.I))


def _line_finished(text):
    value=text.strip()
    if re.fullmatch(r'[-*]?\s*\d+\.',value) or _abbreviation(value): return False
    return bool(re.search(r'(?:[.!?:][*\s\"\'“”’»]*|(?:\[\d+\]\s*)+[.!?]?)$',value))


def literal_paragraphs(text):
    """Preserve literal spans, joining Word soft wraps within a clause.

    Blank lines, list items and completed lines delimit paragraphs. Joining
    uses original offsets, so CRLF, indentation and internal whitespace are
    preserved rather than reconstructed by the model or normalized here.
    """
    parts=[]
    start=end=None
    previous=''
    offset=0
    for line in text.splitlines(keepends=True):
        content=line.rstrip('\r\n')
        structural=bool(re.match(r'^\s*(?:[-*•]\s+|(?:\*\*)?\d+[.)]\s+|#{1,6}\s|\|)',content))
        if start is not None and (not content.strip() or structural or _line_finished(previous)):
            part=text[start:end].strip()
            if part: parts.append(part)
            start=end=None
        if content.strip():
            if start is None: start=offset
            end=offset+len(content)
            previous=content
        offset+=len(line)
    if start is not None:
        part=text[start:end].strip()
        if part: parts.append(part)
    return parts


def fragments(text, max_chars=240):
    """Sentence-sized literal units. max_chars is advisory, never a hard cut.

    Semicolons, commas, Word soft wraps and conditions belong to the sentence.
    Separate complete clauses remain available through multiple selected IDs.
    """
    units = []
    # A numbered list marker is not the end of a sentence; neither is a decimal.
    for line in literal_paragraphs(text):
        start = 0
        for boundary in re.finditer(r'(?<=[.!?])\s+(?=\S)', line):
            candidate = line[start:boundary.start()]
            if re.fullmatch(r'\s*[-*]?\s*\d+\.', candidate): continue
            if _abbreviation(candidate): continue
            part = candidate.strip()
            if part: units.append(dict(id=len(units)+1, text=part))
            start = boundary.end()
        part = line[start:].strip()
        if part: units.append(dict(id=len(units)+1, text=part))
    return units


def materialize(selected, reference_units, answer_units):
    refs = {u['id']:u['text'] for u in reference_units}
    answers = {u['id']:u['text'] for u in answer_units}
    seen, points = set(), []
    for index,p in enumerate(selected.points):
        if p.reference_id not in refs or p.reference_id in seen:
            raise ValueError(f'points[{index}]: unknown or duplicate reference_id={p.reference_id}; select a different available reference_id')
        seen.add(p.reference_id)
        if p.status == 'missing':
            if p.answer_ids: raise ValueError(f'points[{index}]: missing point must have answer_ids=[]')
            quotes = []
        else:
            if not p.answer_ids or len(set(p.answer_ids)) != len(p.answer_ids) or any(i not in answers for i in p.answer_ids):
                raise ValueError(f'points[{index}]: {p.status} needs unique available answer_ids; use missing when no corresponding answer exists')
            quotes = [answers[i] for i in sorted(p.answer_ids)]
        points.append(Point(status=p.status, reference_quote=refs[p.reference_id],
                            answer_quote='\n'.join(quotes), answer_quotes=quotes, explanation=p.explanation))
    if seen != set(refs):
        raise ValueError('Incomplete reference IDs; every substantive clause must be reviewed')
    return Review(agreement=selected.agreement, points=points, explanation=selected.explanation)


def clean(text):
    return ' '.join(re.sub(r'[*_`]', '', text).casefold().split())


def validate_quotes(review, reference, answer):
    """Do not accept invented reference facts or misattributed answer quotations."""
    errors = []
    for i, point in enumerate(review.points):
        rq, aq = clean(point.reference_quote), clean(point.answer_quote)
        if rq not in clean(reference): errors.append(f'points[{i}]: reference_quote absent from reference')
        if point.status == 'missing':
            if aq: errors.append(f'points[{i}]: missing point cannot contain an answer quotation')
            if rq in clean(answer): errors.append(f'points[{i}]: alleged missing quotation occurs in answer')
        elif len(aq) < 8 or any(clean(q) not in clean(answer) for q in (point.answer_quotes or [point.answer_quote])):
            errors.append(f'points[{i}]: answer_quote absent or too short')
        if point.answer_quotes and point.answer_quote != '\n'.join(point.answer_quotes):
            errors.append(f'points[{i}]: answer_quote differs from restored fragments')
        if point.status == 'matched':
            # List ordinals and citation/article IDs are not quantitative claims.
            # Compare quantities and units: 24 days is not 24 hours, while
            # 30 thousand dong and 30,000 dong represent the same amount.
            for error in quantity_errors(rq, aq):
                errors.append(dict(point_index=i, reference_quote=point.reference_quote, **error))
    if review.agreement == 'low' and all(p.status == 'matched' for p in review.points):
        errors.append('Low agreement inconsistent with all reviewed main points matched')
    return errors


def repair_feedback(errors, selection, reference_units, answer_units):
    """Show exact failure and adjacent/quantitative candidates, never invent IDs."""
    candidates = set()
    for point in getattr(selection, 'points', ()):
        for selected_id in point.answer_ids:
            candidates.update((selected_id-1, selected_id, selected_id+1))
    for error in errors:
        if not isinstance(error, dict): continue
        expected = error.get('expected', {})
        for unit in answer_units:
            if any(q['unit'] == expected.get('unit') for q in quantities(unit['text'])):
                candidates.add(unit['id'])
    return dict(errors=errors, candidate_answer_fragments=[u for u in answer_units if u['id'] in candidates],
        instruction='Đọc lại cả đoạn kế tiếp và điều kiện; chọn nhiều answer_ids nếu cần. Không matched khi khác chủ thể, đơn vị hoặc sự kiện.')


def audited_agreement(review):
    statuses={p.status for p in review.points}
    return 'high' if statuses=={'matched'} else 'partial' if 'matched' in statuses else 'low'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reusable_cases(legacy, cases, refs):
    """Keep a real prior judgement only after revalidating its complete evidence."""
    current = {c['id']:c for c in cases}
    kept = []
    for candidate in legacy['cases']:
        if not candidate.get('comparison') or candidate['id'] not in current: continue
        case = current[candidate['id']]; reference = refs[case['id']]['external_answer']
        if candidate['answer'] != case['answer'] or candidate['user_reference'] != reference: continue
        ru, au = reference_fragments(reference), fragments(case['answer'])
        try:
            selected = selection_schema(ru,au).model_validate(candidate['selected_fragments'])
            review = materialize(selected,ru,au)
            if review.model_dump() != candidate['comparison'] or validate_quotes(review,reference,case['answer']): continue
        except (ValueError,KeyError,TypeError): continue
        kept.append(dict(candidate, reaudited_from_policy=legacy['policy'],
            original_scorer_sha256=legacy['scorer_sha256'], reaudited_scorer_sha256=sha(Path(__file__))))
    return kept



def main():
    from compare_grounded_gemini import main as gemini_main
    gemini_main()


if __name__ == '__main__':
    main()
