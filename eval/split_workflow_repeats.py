"""Freeze separate repeat inputs for a scorer that rejects duplicate IDs."""
import argparse
import hashlib
import json
from pathlib import Path
from question_bank_ragas import save_report
from telemetry_summary import summarize_calls


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', type=Path, required=True)
    parser.add_argument('--prefix', type=Path, required=True)
    args = parser.parse_args()
    run = json.loads(args.run.read_text(encoding='utf-8'))
    assert run.get('completed'), 'Do not split incomplete generation'
    assert len(run['worker_levels']) == 1
    for repeat in range(1, run['repeats']+1):
        rows = sorted([c for c in run['cases'] if c['repeat']==repeat], key=lambda c:c['id'])
        assert len(rows) == len(run['selected_ids']) and {c['id'] for c in rows} == set(run['selected_ids'])
        report = {k:v for k,v in run.items() if k not in ('cases','groups','telemetry','warmup')}
        report.update(cases=rows, telemetry=summarize_calls(rows), source_run=str(args.run),
                      source_run_sha256=hashlib.sha256(args.run.read_bytes()).hexdigest(), repeat=repeat)
        target = args.prefix.with_name(args.prefix.name+f'_r{repeat}.json')
        assert not target.exists(), 'Never overwrite a frozen evaluation input'
        save_report(target, report)
        print(target, flush=True)


if __name__ == '__main__':
    main()
