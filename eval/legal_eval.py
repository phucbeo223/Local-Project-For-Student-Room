"""Read-only evaluation against the real indexed corpus and configured generator.

Run inside the API service with /eval mounted. No chat messages or users are saved.
Automated answer checks are necessary checks, NOT a full legal-accuracy score.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, "/app")
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "apps/api"))
from sqlalchemy import create_engine
from app.config import settings
from app.room_service.chatbot.router import init_chatbot, get_service
from app.room_service.chatbot.providers import normalize_text
from app.room_service.chatbot.schemas import ChatAskRequest
from app.room_service.chatbot.legal_retrieval import evidence_issues


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--retrieval-only", action="store_true")
    parser.add_argument("--lexical-only", action="store_true")
    parser.add_argument("--ids", nargs="*")
    parser.add_argument("--out", type=Path, default=Path(__file__).parent / "reports/legal_eval.json")
    args = parser.parse_args()
    cases = json.loads((Path(__file__).parent / "datasets/legal_electricity_eval.json").read_text(encoding="utf-8"))
    engine = create_engine(settings.database_url)
    init_chatbot(engine)
    service = get_service()
    service.repo.record_event = lambda payload: None
    attempts = []
    original_generate = service.generator.generate
    def record_generation(*positional, **keywords):
        result = original_generate(*positional, **keywords)
        attempts.append({"provider": result.provider, "answer": result.text})
        return result
    service.generator.generate = record_generation
    report = {"evaluated_at": datetime.now(timezone.utc).isoformat(),
              "mode": "retrieval" if args.retrieval_only else "generation",
              "lexical_only": args.lexical_only,
              "scope": "Real local corpus; automatic checks plus saved answers for human review.", "cases": []}
    for case in cases:
        if args.ids and case["id"] not in args.ids:
            continue
        attempts.clear()
        print(f"Evaluating {case['id']}...", flush=True)
        if args.retrieval_only:
            vector = None if args.lexical_only else service.embedder.embed_query(case["question"]).vector
            sources = service.repo.retrieve_legal(case["question"], vector)
            answer, no_answer, provider, issues = "", not sources, None, []
            retrieval_mode = "legal_hybrid" if vector is not None else "legal_lexical"
        else:
            result = service.ask(ChatAskRequest(message=case["question"], include_evaluation_contexts=True))
            sources = [dict(source.model_dump(), content=context.content)
                       for source, context in zip(result.sources, result.evaluation_contexts)]
            answer, no_answer, provider, issues = result.answer, result.no_answer, result.generation_provider, result.degraded_reasons
            retrieval_mode = result.retrieval_mode
        checks = [any(expected["path"] in source["source_path"]
                      and normalize_text(expected["text"]) in normalize_text(source["content"])
                      for source in sources) for expected in case["required"]]
        relevant = all(checks)
        answer_checks = None if args.retrieval_only else (
            (not no_answer and provider != "template" and all(normalize_text(term) in normalize_text(answer)
                                                            for term in case["answer_terms"]))
            if case["expect_answer"] else (
                no_answer and
                any(term in normalize_text(answer) for term in ("chua", "khong du", "khong neu", "khong xac dinh"))
                and not any(term in normalize_text(answer) for term in ("vietcombank", "techcombank", "bidv"))))
        if not args.retrieval_only:
            answer_checks = answer_checks and not evidence_issues(answer, sources, case["question"])
            if case["id"] == "overcharge_penalty":
                answer_checks = answer_checks and "ca nhan" in normalize_text(answer) and "do dem" not in normalize_text(answer)
        row = {"id": case["id"], "question": case["question"], "retrieval_pass": relevant,
               "required_checks": checks, "answer_checks_pass": answer_checks,
               "answer": answer, "provider": provider, "no_answer": no_answer, "issues": issues,
               "generation_attempts": list(attempts),
               "retrieval_mode": retrieval_mode,
               "sources": [{key: source.get(key) for key in
                            ("source_path", "heading", "page_from", "page_to", "rank", "chunk_id", "content")}
                           for source in sources]}
        report["cases"].append(row)
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"{case['id']}: retrieval={relevant}, answer_checks={answer_checks}", flush=True)
    engine.dispose()
    if any(not case["retrieval_pass"] or case["answer_checks_pass"] is False for case in report["cases"]):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
