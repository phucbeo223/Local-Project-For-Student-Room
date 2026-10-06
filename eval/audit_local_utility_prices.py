"""Aggregate explicit utility claims locally; absent/ambiguous prices stay unknown."""
import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import statistics

from quantity_audit import normalized, number_value


def audit(path):
    rows = [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines()]
    groups = defaultdict(list)
    observation_times = defaultdict(list)
    mentions = Counter()
    dated = Counter()
    for row in rows:
        text = normalized(row.get('description') or '')
        for utility in ('dien', 'nuoc'):
            # A price must be immediately attached to its utility and specify a
            # denominator. No inferred currency, unit, consumption or time.
            if re.search(r'\b'+utility+r'\b', text): mentions[utility] += 1
            matches = list(re.finditer(r'\b'+utility+r'\s*(?:[:=]|la|gia)?\s*'
                r'(\d+(?:[.,]\d+)*)\s*(nghin|ngan|trieu|k|dong|vnd|d)\s*'
                r'(?:/|moi|tren)\s*(kwh|kw|m[3³]|khoi|nguoi)(?:\s*/\s*(thang))?', text))
            if len(matches) != 1: continue  # Multiple/ranged rates need review.
            match = matches[0]
            unit = match[3]
            if unit == 'kw': continue  # kW is power, not energy (kWh).
            if unit == 'nguoi' and not match[4]: continue  # Billing period missing.
            if unit not in (('kwh',) if utility == 'dien' else ('m3','m³','khoi','nguoi')): continue
            value = number_value(match[1]) * {'k':1000,'nghin':1000,'ngan':1000,'trieu':1000000}.get(match[2],1)
            if value <= 0: continue
            unit = 'VND/' + ('nguoi/thang' if unit=='nguoi' else 'm3' if unit in ('m3','m³','khoi') else unit)
            timestamp = row.get('last_seen') or row.get('first_seen')
            if not timestamp: continue
            groups[(utility,unit)].append(float(value));dated[utility] += 1
            observation_times[(utility,unit)].append(str(timestamp))
    return dict(catalog_sha256=hashlib.sha256(path.read_bytes()).hexdigest(), rows=len(rows),
        audited_at_utc=datetime.now(timezone.utc).isoformat(),
        utility_fields=sorted({k for r in rows for k in r if re.search('water|electricity|gia_dien|gia_nuoc',k,re.I)}),
        text_mentions=dict(mentions), valid_explicit_dated_records=dict(dated),
        statistics=[dict(utility=u,unit=unit,n=len(values),minimum=min(values),median=statistics.median(values),maximum=max(values),
                        observed_from=min(observation_times[(u,unit)]),observed_to=max(observation_times[(u,unit)]))
                    for (u,unit),values in groups.items()],
        interpretation='Advertisement claims within this catalog only, not independently verified landlord prices or prevalence across Can Tho. Missing prices mean unknown and may be asked of the landlord later. No imputation; no housing records sent to Gemini.',
        excluded='Missing denominator, billing period or observation time; ambiguous units; multiple/ranged rates. Counts do not certify comprehensive extraction.')


if __name__ == '__main__':
    p=argparse.ArgumentParser();p.add_argument('--catalog',type=Path,required=True);p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    result=audit(args.catalog);args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False))
