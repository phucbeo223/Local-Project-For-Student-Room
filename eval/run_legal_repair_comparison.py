"""Wait for completed legal generation, then judge both runs sequentially.

This is an execution wrapper around the frozen comparer. It does not change
questions, answers, selected fragments, labels, or reference inputs.
"""
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path('/eval')
REPORTS = ROOT / 'reports'
BASELINE = REPORTS / 'graph_rag_priority7_36_v20_2026-10-06.json'
REPAIRED = REPORTS / 'legal_repair_36_v20_20261006.json'
EXPECTED_IDS = list(range(19, 39)) + list(range(43, 59))
EXPECTED_PIPELINE = 'ef42a4633f539a7734bc3d484213d0d9575be0a70427ea1a1da017062603cab2'


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def main():
    baseline = read(BASELINE)
    last_progress = None
    while True:
        if REPAIRED.exists():
            try:
                repaired = read(REPAIRED)
            except json.JSONDecodeError:
                time.sleep(5)
                continue
            assert repaired['pipeline_sha256'] == EXPECTED_PIPELINE
            progress = repaired.get('summary', {}).get('completed', 0)
            if progress != last_progress:
                print(f'Waiting for completed generation: {progress}/36', flush=True)
                last_progress = progress
            if repaired.get('summary', {}).get('errors'):
                raise RuntimeError('Generation has errors; comparison was not started')
            if progress == 36 and repaired.get('graph_summary') is not None:
                break
        time.sleep(10)
    assert repaired['graph_summary']['cloud_housing_calls'] == 0
    assert repaired['legal_only'] is True
    before = {c['id']: c for c in baseline['cases']}
    after = {c['id']: c for c in repaired['cases']}
    assert sorted(before) == sorted(after) == EXPECTED_IDS
    assert baseline['question_bank_sha256'] == repaired['question_bank_sha256']
    for qid in EXPECTED_IDS:
        assert before[qid]['question'] == after[qid]['question']
        assert after[qid].get('answer') and not after[qid].get('error')
        assert len(after[qid]['answer']) <= 3500
    print('All 36 answers completed; start sequential local comparisons', flush=True)
    pairs = (
        (BASELINE, REPORTS / 'legal_repair_baseline_36_v15_20261006.json'),
        (REPAIRED, REPORTS / 'legal_repair_new_36_v15_20261006.json'),
    )
    for run, output in pairs:
        subprocess.run([sys.executable, str(ROOT / 'compare_grounded_references.py'),
                        '--run', str(run), '--output', str(output)], check=True)
    subprocess.run([
        sys.executable, str(ROOT / 'report_legal_repair.py'),
        '--baseline-run', str(BASELINE), '--repaired-run', str(REPAIRED),
        '--baseline-review', str(pairs[0][1]), '--repaired-review', str(pairs[1][1]),
        '--point-review', str(ROOT / 'datasets/external_legal_20261004/point_review_20261006.json'),
        '--output-json', str(REPORTS / 'legal_repair_36_comparison_v15_20261006.json'),
        '--output-md', str(REPORTS / 'legal_repair_36_comparison_v15_20261006.md'),
    ], check=True)


if __name__ == '__main__':
    main()
