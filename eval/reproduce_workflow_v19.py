"""Read historical mapper without importing or constructing a local LLM."""
import ast
import hashlib
import json
from pathlib import Path
import sys
import types
from compare_grounded_references import reference_fragments

ROOT = Path(__file__).resolve().parents[1]


def main():
    snapshot = ROOT/'eval/compare_grounded_references_v15.py'
    tree = ast.parse(snapshot.read_text(encoding='utf-8'))
    tree.body = [n for n in tree.body if not (isinstance(n,ast.ImportFrom) and n.module=='ollama_judge')]
    module = types.ModuleType('historical_mapper_only')
    module.OllamaRagasLLM = object  # Annotation only; no provider imported or constructed.
    sys.modules[module.__name__] = module
    exec(compile(tree,str(snapshot),'exec'),module.__dict__)
    old = json.loads((ROOT/'eval/reports/gemini_completion_36_final_v18_v15_20261007.json').read_text(encoding='utf-8'))
    cases = []
    for case in old['cases']:
        if case['id'] not in (19,36,47):
            continue
        selected = module.SelectedReview.model_validate(case['selected_fragments'])
        rebuilt = module.materialize(selected,module.reference_fragments(case['user_reference']),module.fragments(case['answer']))
        matches = rebuilt.model_dump()['points']==case['comparison']['points']
        assert matches
        cases.append(dict(id=case['id'],historical_id_mapping_reproduces_saved_comparison=matches,
                          selected_fragments=case['selected_fragments'],comparison=case['comparison']))
    q24 = next(c for c in old['cases'] if c['id']==24)
    report = dict(v15_sha256=hashlib.sha256(snapshot.read_bytes()).hexdigest(),
        no_model_calls=True, method='Execute archived literal mapper only; remove Ollama import via AST. Reconstruct from saved IDs and complete saved inputs.',
        cause='Q19/Q36/Q47 saved IDs reproduce quotes/explanations exactly. The mismatching explanation is already attached to that selected reference in model output; quote membership alone fails to catch semantic drift. No evidence here of application-side ID renumbering.',
        cases=cases,q24=dict(before_units=module.reference_fragments(q24['user_reference']),
                             after_units=reference_fragments(q24['user_reference'])))
    target = ROOT/'eval/reports/gemini_workflow_v19_reproductions_20261007.json'
    target.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print([(c['id'],c['historical_id_mapping_reproduces_saved_comparison']) for c in cases])


if __name__=='__main__':
    main()
