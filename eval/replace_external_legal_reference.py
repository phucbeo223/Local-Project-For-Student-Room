"""Replace the user reference, preserving IDs, source bytes and a version backup."""
import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / 'eval/datasets/external_legal_20261004'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('attachment', type=Path)
    parser.add_argument('--date', required=True)
    args = parser.parse_args()
    raw = args.attachment.read_bytes()
    text = raw.decode('utf-8-sig')
    old_bytes = (DATASET / 'answers.json').read_bytes()
    old = json.loads(old_bytes)
    questions = list(re.finditer(r'^### Câu (\d+): (.+)$', text, re.M))
    topics = list(re.finditer(r'^## (\d+)\. (.+?) \(`([^`]+)`\)', text, re.M))
    assert [int(q[1]) for q in questions] == list(range(1, 37))
    assert len(topics) == 9 and len(old['cases']) == 36
    cases = []
    for index, question in enumerate(questions):
        end = questions[index + 1].start() if index + 1 < len(questions) else len(text)
        section = text[question.end():end]
        section = re.split(r'^## \d+\.', section, maxsplit=1, flags=re.M)[0]
        basis = re.search(r'^- \*\*Căn cứ pháp lý:\*\* (.+)$', section, re.M)
        answer = re.search(r'^- \*\*Câu trả lời mẫu:\*\*\s*\r?\n', section, re.M)
        assert basis and answer, question[1]
        value = re.sub(r'\s*\n---\s*$', '', section[answer.end():]).strip()
        assert value and value in text
        topic = next(t for t in reversed(topics) if t.start() < question.start())
        previous = next(c for c in old['cases'] if c['id'] == int(question[1]))
        assert previous['question'].strip() == question[2].strip()
        cases.append({
            'id': int(question[1]), 'original_question_id': previous['original_question_id'],
            'topic': topic[3], 'question': question[2].strip(),
            'legal_basis': basis[1].strip(), 'external_answer': value,
            'reference_status': 'user_supplied_unverified',
        })
    new = dict(old)
    new.update(
        dataset_version=f'external-legal-user-{args.date}', received_date=args.date,
        original_filename=args.attachment.name, original_sha256=hashlib.sha256(raw).hexdigest(),
        supersedes_dataset_version=old['dataset_version'],
        previous_reference_sha256=hashlib.sha256(old_bytes).hexdigest(), cases=cases,
    )
    backup = DATASET / 'archive' / old['dataset_version']
    originals = {name: (DATASET / name).read_bytes()
                 for name in ('original.txt', 'answers.md', 'answers.json')}
    for name, content in originals.items():
        target = backup / name
        if target.exists():
            assert target.read_bytes() == content, f'Conflicting backup: {target}'
    backup.mkdir(parents=True, exist_ok=True)
    for name, content in originals.items():
        (backup / name).write_bytes(content)
    (DATASET / 'original.txt').write_bytes(raw)
    (DATASET / 'answers.md').write_bytes(raw)
    (DATASET / 'answers.json').write_text(
        json.dumps(new, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    loaded = json.loads((DATASET / 'answers.json').read_bytes())
    assert loaded == new
    assert len({c['topic'] for c in cases}) == 9
    assert (DATASET / 'original.txt').read_bytes() == raw
    assert (DATASET / 'answers.md').read_bytes() == raw
    assert all((backup / n).read_bytes() == b for n, b in originals.items())
    print(json.dumps({
        'version': loaded['dataset_version'], 'cases': len(cases), 'topics': 9,
        'changed_answers': sum(a['external_answer'] != b['external_answer']
                               for a, b in zip(old['cases'], cases)),
        'source_byte_match': True, 'old_dataset_backup_verified': True,
    }))


if __name__ == '__main__':
    main()
