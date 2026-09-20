"""Full API + RAGAS evaluation for the scientific report.

Requires a running API and an LLM configured for RAGAS. Unlike chatbot_eval.py,
this runner evaluates the actual DB retrieval and generated answer.
"""
from __future__ import annotations

import argparse
import json
import os
import statistics
import sys
import time
from pathlib import Path

import httpx
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import answer_relevancy, context_precision, context_recall, faithfulness


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--api-url", default=os.getenv("API_URL", "http://localhost:8000"))
    parser.add_argument("--dataset", type=Path, default=ROOT / "eval/datasets/chatbot_eval.jsonl")
    parser.add_argument("--output", type=Path, default=ROOT / "eval/reports/ragas_eval.json")
    parser.add_argument("--limit", type=int, default=200)
    parser.add_argument(
        "--admin-token",
        default=os.getenv("ADMIN_ACCESS_TOKEN"),
        help="Optional token used to publish the run to /admin/evaluation-runs.",
    )
    args = parser.parse_args()

    cases = [
        json.loads(line)
        for line in args.dataset.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ][: args.limit]
    rows: list[dict] = []
    latencies: list[float] = []
    citation_scores: list[float] = []
    providers: set[str] = set()
    models: set[str] = set()
    with httpx.Client(base_url=args.api_url, timeout=60) as client:
        for case in cases:
            started = time.perf_counter()
            response = client.post(
                "/chat/ask",
                json={
                    "message": case["question"],
                    "conversation_history": case.get("conversation_history", []),
                    "include_evaluation_contexts": True,
                },
            )
            response.raise_for_status()
            result = response.json()
            latencies.append((time.perf_counter() - started) * 1000)
            citation_scores.append(float(result.get("citation_accuracy", 0)))
            providers.add(str(result.get("generation_provider") or "unknown"))
            if result.get("generation_model"):
                models.add(str(result["generation_model"]))
            rows.append(
                {
                    "question": case["question"],
                    "answer": result["answer"],
                    "contexts": [item["content"] for item in result["evaluation_contexts"]],
                    "ground_truth": case["reference_answer"],
                }
            )

    scores = evaluate(
        Dataset.from_list(rows),
        metrics=[faithfulness, answer_relevancy, context_precision, context_recall],
    ).to_pandas()
    report = {
        "dataset_version": cases[0]["dataset_version"] if cases else "unknown",
        "evaluation_scope": "running_api_end_to_end_ragas",
        "generation_providers": sorted(providers),
        "generation_models": sorted(models),
        "cases": len(cases),
        "metrics": {
            name: round(float(scores[name].dropna().mean()), 4)
            for name in ("faithfulness", "answer_relevancy", "context_precision", "context_recall")
        },
        "p95_latency_ms": round(
            statistics.quantiles(latencies, n=100)[94] if len(latencies) > 1 else (latencies[0] if latencies else 0),
            2,
        ),
    }
    report["metrics"]["citation_format_accuracy"] = round(
        statistics.mean(citation_scores) if citation_scores else 0.0, 4
    )
    thresholds = {
        "faithfulness": 0.70,
        "answer_relevancy": 0.75,
        "context_precision": 0.70,
        "context_recall": 0.70,
        "citation_format_accuracy": 0.95,
    }
    report["acceptance_thresholds"] = thresholds
    report["passed"] = all(report["metrics"].get(key, 0) >= value for key, value in thresholds.items())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.admin_token:
        with httpx.Client(base_url=args.api_url, timeout=30) as client:
            published = client.post(
                "/admin/evaluation-runs",
                headers={"Authorization": f"Bearer {args.admin_token}"},
                json={
                    "dataset_version": report["dataset_version"],
                    "model_version": ",".join(report["generation_models"] or report["generation_providers"]),
                    "prompt_version": "ctu-rag-grounded-v1",
                    "metrics": report["metrics"],
                    "passed": report["passed"],
                },
            )
            published.raise_for_status()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
