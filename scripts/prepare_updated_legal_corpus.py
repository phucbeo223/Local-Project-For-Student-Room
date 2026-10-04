"""Build the October 4 corpus from reviewed source text and labelled guidance.

Never read the user's evaluation answers or reuse persisted embedding vectors.
"""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/legal_corpus_v3_20261004'
SUPPLEMENT = ROOT / 'docs/legal_web_supplement_20261004/candidate_corpus'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    baseline_path = ROOT / 'docs/legal_corpus_v2/manifest.json'
    baseline = read(baseline_path)
    documents = {}
    inputs = {baseline_path.relative_to(ROOT).as_posix(): sha(baseline_path)}
    for entry in baseline['documents']:
        path = ROOT / entry['file']
        assert sha(path) == entry['sha256'], entry['id']
        documents[entry['id']] = read(path)
        inputs[entry['file']] = sha(path)
    candidate = read(SUPPLEMENT / 'manifest.json')
    for entry in candidate['documents']:
        path = ROOT / entry['file']
        assert sha(path) == entry['sha256'], entry['id']
        data = read(path)
        key = entry['id'].removeprefix('web20261004-')
        key = {'commerce122': 'ecommerce122'}.get(key, key)
        data['source']['category'] = {'residence116':'residence', 'ecommerce122':'ecommerce_platform',
            'broker06':'real_estate_brokerage', 'electricity09':'electricity',
            'fire58':'fire_safety', 'water215':'water_cantho'}[key]
        data['source']['activation_status'] = 'reviewed_excerpt_in_refresh_corpus'
        if key in documents and key != 'water215':
            current = documents[key]
            replacements = {(p.get('article'), p.get('clause')) for p in data['provisions']}
            current['provisions'] = [p for p in current['provisions']
                                     if (p.get('article'), p.get('clause')) not in replacements]
            current['provisions'].extend(data['provisions'])
            current['source']['reviewed_update_source'] = data['source']
        else:
            documents.pop(key, None)
            data['source']['id'] = key
            documents[key] = data
        inputs[entry['file']] = sha(path)

    paths = sorted((ROOT / 'Data').glob('*/Bo-sung-thuc-te-20261004.md'))
    paths += [ROOT / 'Data/cantho_contacts.md', ROOT / 'Data/legal_templates.md']
    guidance_count = 0
    for path in paths:
        body = path.read_text(encoding='utf-8')
        digest = sha(path)
        key = 'guidance-20261004-' + path.parent.name if path.parent.name != 'Data' else 'guidance-20261004-' + path.stem
        category = path.parent.name if path.parent.name != 'Data' else ('residence' if path.stem == 'legal_templates' else 'general_legal')
        title = body.splitlines()[0].lstrip('# ').strip()
        sections = re.split(r'(?m)(?=^#{2,3} )', body)
        provisions = []
        for index, section in enumerate(sections):
            if not section.strip(): continue
            heading = section.splitlines()[0].lstrip('# ').strip()
            # The citation and recommendation text remains beside each scenario.
            content = 'HƯỚNG DẪN BIÊN SOẠN — không phải nguyên văn điều luật.\n' + section.strip()
            provisions.append(dict(provision_id=f'{digest}:guidance:{index}', article=None, clause=None,
                heading=heading, content=content, content_sha256=hashlib.sha256(content.encode()).hexdigest(),
                page_from=1, page_to=1, kind='editorial_guidance', points=[], exceptions=[],
                cross_references=[], article_context='', source_start=0, source_end=len(section)))
        documents[key] = dict(source=dict(id=key, title='Hướng dẫn thực tế: ' + title, category=category,
            path=path.relative_to(ROOT).as_posix(), sha256=digest, pages=1,
            extraction='Verbatim local Markdown; reviewed editorial guidance, not statute',
            page_kind='editorial_guidance', source_role='editorial_guidance', not_exhaustive=True,
            accessed_date='2026-10-04', verification='Source links and applicability notes retained in text'),
            provisions=provisions)
        inputs[path.relative_to(ROOT).as_posix()] = digest
        guidance_count += 1
    entries = []
    for key, data in sorted(documents.items()):
        target = OUT / (key + '.json')
        target.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        entries.append(dict(id=key, file=target.relative_to(ROOT).as_posix(), sha256=sha(target),
            category=data['source']['category'], provisions=len(data['provisions'])))
    manifest = dict(schema='legal_v3_20261004', documents=entries, input_sha256=inputs,
        baseline_manifest_sha256=sha(baseline_path), updated_guidance_documents=guidance_count,
        evaluation_policy='Post-update regression on 36 known topics. Guidance overlaps questions; not an unseen benchmark. User answers are comparison-only and never indexed.',
        excluded=baseline.get('excluded', []))
    (OUT / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(dict(documents=len(entries), provisions=sum(e['provisions'] for e in entries),
                         guidance_documents=guidance_count, schema=manifest['schema'])))


if __name__ == '__main__': main()
