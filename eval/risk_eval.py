"""Evaluate the risk rules only on independently human-labelled records."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "apps/api"))

from app.room_service.risk.scoring import MODEL_VERSION, score_listing  # noqa: E402

ALLOWED_LABEL_SOURCES = {"manual", "verified_report"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=ROOT / "eval/reports/risk_eval.json")
    parser.add_argument("--threshold", type=float, default=0.6)
    args = parser.parse_args()

    rows = [json.loads(line) for line in args.dataset.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not rows:
        raise SystemExit("Dataset rỗng; cần tập nhãn độc lập trước khi đánh giá risk.")
    invalid = [row.get("id") for row in rows if row.get("label_source") not in ALLOWED_LABEL_SOURCES]
    if invalid:
        raise SystemExit(f"Nhãn không độc lập ở records: {invalid[:10]}")

    tp = fp = tn = fn = 0
    for row in rows:
        predicted = score_listing(
            row["listing"], district_median_price=row.get("district_median_price")
        ).score >= args.threshold
        actual = bool(row["is_risky"])
        tp += int(predicted and actual)
        fp += int(predicted and not actual)
        tn += int(not predicted and not actual)
        fn += int(not predicted and actual)
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    report = {
        "model_version": MODEL_VERSION,
        "evaluation_scope": "independent_human_labels",
        "records": len(rows),
        "threshold": args.threshold,
        "confusion_matrix": {"tp": tp, "fp": fp, "tn": tn, "fn": fn},
        "metrics": {
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1": round(2 * precision * recall / (precision + recall), 4)
            if precision + recall
            else 0.0,
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
