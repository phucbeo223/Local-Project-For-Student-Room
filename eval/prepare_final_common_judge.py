"""Archive quota-limited judge runs and prepare a common complete evaluation."""
import hashlib
import json
from pathlib import Path
from question_bank_ragas import save_report, summarize

root = Path(__file__).resolve().parent / "reports"
for role, name in (("before", "legal_upgrade_before_common_judge_2026-10-02"),
                   ("after", "legal_model_upgrade_after_2026-10-02")):
    path = root / (name + ".json")
    archive = root / (name + "_judge35_trial.json")
    if archive.exists():
        raise ValueError("Trial already archived; do not reset valid checkpoints again")
    raw = path.read_bytes()
    archive.write_bytes(raw)
    report = json.loads(raw)
    report["previous_common_judge_artifact"] = {"path": archive.name, "sha256": hashlib.sha256(raw).hexdigest(),
        "reason": "Gemini 3.5 daily quota 500 exhausted before completing both reports"}
    report.pop("judge", None)
    for case in report["cases"]:
        for field in ("ragas", "ragas_usage", "ragas_errors", "ragas_retry_history", "ragas_judgements"):
            case.pop(field, None)
    if role == "after":
        report["incremental_source_guard_retest"] = {
            "changed_case_ids": [23], "unchanged_answers_checked": 35,
            "old_guard_sha256": "9399d28aaae35c3f283ca9a412f276fa4049bfee18808da5ea88846e57e4c28f",
            "method": "Replay deterministic source guard across all saved full answers; rerun only the newly rejected response",
        }
        report["cases"][22] = {k: report["cases"][22][k] for k in ("id", "question", "category")}
    summarize(report)
    save_report(path, report)
    print(role, "archived; prepared for final common judge")
