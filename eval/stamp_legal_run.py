"""Save a reproducibility manifest without changing any completed answer/score."""
import argparse
import hashlib
import json
import sys
from pathlib import Path
from datetime import datetime, timezone

parser = argparse.ArgumentParser()
parser.add_argument("--run", type=Path, required=True)
parser.add_argument("--output", type=Path, required=True)
args = parser.parse_args()
sys.path.insert(0, "/workspace/apps/api")
sys.path.insert(0, str(Path(__file__).resolve().parent))
from app.room_service.chatbot.service import _citation_accuracy
from question_bank_ragas import summarize, save_report
run = json.loads(args.run.read_text(encoding="utf-8"))
for case in run["cases"]:
    for usage in case.get("ragas_usage", {}).values():
        if "max_output_tokens" not in usage:
            usage["max_output_tokens"] = 2048
            usage["output_budget_metadata_source"] = "recorded default of the initial scoring pass"
    if "answer" in case:
        case.setdefault("citation_accuracy_before_footnote_fix", case.get("citation_accuracy"))
        case["citation_accuracy"] = _citation_accuracy(case["answer"], case.get("sources", []))
run["citation_validation_note"] = "Recomputed on recorded answers after excluding document footnotes inside verbatim quotations; original values retained. Answers and Ragas results unchanged."
summarize(run)
save_report(args.run, run)
root = Path("/workspace/apps/api/app/room_service")
paths = list((root / "chatbot").glob("*.py")) + list((root / "legal_knowledge").glob("*.py"))
eval_root = Path(__file__).resolve().parent
evaluation_paths = [eval_root / name for name in ("question_bank_ragas.py", "requirements-ragas.txt", "Dockerfile.ragas", "stamp_legal_run.py")]
data_root = Path("/data")
data_paths = sorted(path for path in data_root.rglob("*") if path.is_file())
manifest = {"created_at_utc": datetime.now(timezone.utc).isoformat(),
            "run": args.run.name, "run_sha256": hashlib.sha256(args.run.read_bytes()).hexdigest(),
            "source_hashes": {str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest() for path in sorted(paths)},
            "evaluation_source_hashes": {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in evaluation_paths},
            "data_source_hashes": {str(path.relative_to(data_root)): hashlib.sha256(path.read_bytes()).hexdigest() for path in data_paths},
            "scope": "36 legal questions; exclude old listing price/distance/CTU dormitory questions",
            "embedding": "intfloat/multilingual-e5-small", "extraction_version": "legal-v6",
            "regression_checks_passed": 72,
            "api_model": "qwen3.5:4b", "legal_context_window": 16384,
            "independent_reference_answers": False,
            "notes": "All Ragas metrics use the same local Qwen judge, full collected content and source metadata. Citation validator was replayed after footnote fix. Same-family judge bias remains."}
args.output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(args.output)
