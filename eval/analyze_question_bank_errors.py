"""Read saved results and replay the deterministic parser without DB or LLM calls."""
from __future__ import annotations

import ast
import inspect
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, "/workspace/apps/api")
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "apps/api"))

from app.room_service.chatbot.parser import parse_query
from app.room_service.chatbot.providers import normalize_text
from app.room_service.chatbot.service import rewrite_query


def main() -> None:
    root = Path(__file__).resolve().parent
    run = json.loads((root / "reports/question_bank_ragas_2026-10-01.json").read_text(encoding="utf-8"))
    audit = json.loads((root / "reports/question_bank_corpus_audit_2026-10-01.json").read_text(encoding="utf-8"))
    stale = set(audit["indexed_but_missing_from_data"])
    terms = {}
    for node in ast.walk(ast.parse(inspect.getsource(parse_query))):
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
            if node.targets[0].id in {"housing_terms", "legal_terms"}:
                terms[node.targets[0].id] = ast.literal_eval(node.value)
    rows = []
    for case in run["cases"]:
        parsed = parse_query(case["question"])
        normalized = normalize_text(case["question"])
        rows.append({
            "id": case["id"], "question": case["question"],
            "expected_category_label": case["category"],
            "saved_intent": case["intent"], "current_parser_intent": parsed.intent,
            "current_parser_filters": parsed.filters.model_dump(),
            "matching_legal_substrings": [t for t in terms["legal_terms"] if t in normalized],
            "matching_housing_substrings": [t for t in terms["housing_terms"] if t in normalized],
            "same_category_label_found": case.get("category_source_match"),
            "source_kinds": sorted({s["kind"] for s in case["sources"]}),
            "source_categories": sorted({s["category"] for s in case["sources"] if s.get("category")}),
            "stale_source_paths": sorted({s["source_path"] for s in case["sources"] if s.get("source_path") in stale}),
            "no_answer": case["no_answer"], "degraded_reasons": case["degraded_reasons"],
        })
    by_id = {case["id"]: case for case in run["cases"]}
    followups = []
    for question_id in (15, 16):
        history = []
        for previous_id in (14, 15):
            if previous_id < question_id:
                prior = by_id[previous_id]
                history.extend([
                    {"role": "user", "content": prior["question"][:2000]},
                    {"role": "assistant", "content": prior["answer"][:2000]},
                ])
        query = by_id[question_id]["question"]
        rewritten = rewrite_query(query, history)
        followups.append({
            "id": question_id, "history_user_ids": [i for i in (14, 15) if i < question_id],
            "rewritten_query": rewritten, "rewrite_changed": rewritten != query,
            "previous_listing_ids": by_id[question_id - 1]["listing_ids"],
            "result_listing_ids": by_id[question_id]["listing_ids"],
        })
    warning_rows = [row for row in rows if row["same_category_label_found"] is False]
    result = {
        "method": "saved run inspection + current parser/rewrite replay; no DB writes or LLM generation",
        "category_label_check": "at least one source.category equals the question's single folder label; not semantic evidence correctness",
        "topic_question_count": 40,
        "topic_intents": dict(Counter(row["saved_intent"] for row in rows[18:])),
        "category_warning_count": len(warning_rows),
        "warning_intents": dict(Counter(row["saved_intent"] for row in warning_rows)),
        "wrong_topic_route_ids": [row["id"] for row in rows[18:] if row["saved_intent"] != "legal_question"],
        "knowledge_route_category_warning_ids": [row["id"] for row in warning_rows if row["saved_intent"] == "legal_question"],
        "no_answer_intents": dict(Counter(row["saved_intent"] for row in rows if row["no_answer"])),
        "stale_source_case_ids": [row["id"] for row in rows if row["stale_source_paths"]],
        "followup_replay": followups,
        "cases": rows,
    }
    output = root / "ragas_reports/question_bank_error_diagnostics_2026-10-01.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in result.items() if key not in {"cases", "followup_replay"}}, ensure_ascii=False, indent=2))
    print(json.dumps({"followup_replay": followups, "filter_replay": [row for row in rows if row["id"] in (1, 2, 9, 14, 17)]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
