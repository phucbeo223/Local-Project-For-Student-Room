"""Clarify collection-only metadata without altering any generated answers."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
if not (ROOT / 'apps/api/app').is_dir(): ROOT = Path('/workspace')
path = ROOT / 'eval/reports/legal_refresh_36_2026-10-04.json'
report = json.loads(path.read_text(encoding='utf-8'))
assert len(report['cases']) == 36 and all(c.get('answer') and not c.get('error') for c in report['cases'])
def answer_digest(cases):
    return hashlib.sha256(json.dumps(cases, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
before = answer_digest(report['cases'])
report.setdefault('runner_default_method', report['method'])
report['method'] = 'Real DB and configured agent workflow; collection only. User reference comparison is a separate post-generation stage. No RAGAS scores were run.'
report['phase'] = 'collect'
report['evaluated_schema'] = 'legal_v3_20261004'
report['evaluation_scope'] = 'Regression on 36 known legal topics after indexing editorial guidance; not an unseen benchmark.'
report['reference_isolation'] = 'The runner does not load user answers; the comparator loads them only after generation.'
report['summary']['context_recall'] = 'Not measured in this collection; user reference compared separately.'
report['summary']['answer_correctness'] = 'Not measured; text agreement labels are not legal accuracy.'
report['api_pacing_difference'] = 'Evaluation Gemini min interval=0 seconds; active API=5 seconds.'
report['collected_cases_sha256'] = before
assert before == answer_digest(report['cases'])
path.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps(dict(cases=36, answers_unchanged_sha256=before, phase='collect')))
