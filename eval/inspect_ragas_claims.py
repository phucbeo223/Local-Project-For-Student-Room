"""Inspect native Faithfulness verdicts separately; never overwrite recorded scores."""
import argparse
import asyncio
import json
from pathlib import Path
from ragas.llms.base import InstructorBaseRagasLLM
from ragas.metrics.collections import Faithfulness
from app.config import settings
from app.room_service.chatbot.providers import GeminiGenerator


class TracedJudge(InstructorBaseRagasLLM):
    def __init__(self, model):
        self.model = model
        self.calls = []
        self.client = GeminiGenerator("", model, api_keys=settings.configured_gemini_keys,
                                     legal_timeout_seconds=180, per_request_timeout_seconds=180)

    def generate(self, prompt, response_model):
        raw, usage = self.client.request_json(prompt, response_model.model_json_schema(), max_output_tokens=8192)
        result = response_model.model_validate_json(raw)
        self.calls.append({"schema": response_model.__name__, "output": result.model_dump(mode="json"), "usage": usage})
        return result

    async def agenerate(self, prompt, response_model):
        return await asyncio.to_thread(self.generate, prompt, response_model)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--ids", type=int, nargs="+", required=True)
    args = parser.parse_args()
    run = json.loads(args.input.read_text(encoding="utf-8"))
    results = {"method": "Separate native Ragas Faithfulness diagnostic rerun; original scores preserved",
               "judge": run["judge"], "cases": []}
    for case in run["cases"]:
        if case["id"] not in args.ids:
            continue
        judge = TracedJudge(run["judge"]["model"])
        row = {"id": case["id"], "recorded_faithfulness": case.get("ragas", {}).get("faithfulness")}
        try:
            contexts = [json.dumps({"rank": source.get("rank"), "document": source.get("title"),
                "category": source.get("category"), "heading": source.get("heading"),
                "page_from": source.get("page_from"), "page_to": source.get("page_to"),
                "content": context}, ensure_ascii=False) for source, context in zip(case["sources"], case["contexts"])]
            row["diagnostic_faithfulness"] = float(Faithfulness(llm=judge).score(
                user_input=case["question"], response=case["answer"], retrieved_contexts=contexts).value)
        except Exception as exc:
            row["error"] = type(exc).__name__
        row["calls"] = judge.calls
        judge.client.close()
        results["cases"].append(row)
        args.output.write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(case["id"], row.get("diagnostic_faithfulness"), row.get("error"), flush=True)


if __name__ == "__main__":
    main()
