"""Separate the requested 56-question summary from supplementary references."""
import argparse,copy,hashlib,json
from pathlib import Path
import question_bank_ragas as bank

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--run',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    source=json.loads(args.run.read_text(encoding='utf-8'))
    assert sorted(case['id'] for case in source['cases'])==list(range(1,59))
    assert all(case.get('answer') and not case.get('error') for case in source['cases'])
    report=copy.deepcopy(source)
    report['cases']=[case for case in report['cases'] if case['id']<=56]
    report['selected_original_ids']=list(range(1,57))
    report['full_run_sha256']=hashlib.sha256(args.run.read_bytes()).hexdigest()
    report['supplementary_original_ids']=[57,58]
    report['graph_summary']['selected_cases']=56
    report['graph_summary']['cases_with_graph_trace']=sum(any(step.get('stage')=='graph_retrieval' for step in case.get('agent_trace',[])) for case in report['cases'])
    bank.summarize(report)
    bank.save_report(args.output,report)
    print(json.dumps(report['summary'],ensure_ascii=False))

if __name__=='__main__':main()
