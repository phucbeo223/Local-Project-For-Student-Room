"""Diagnose Gemini schema failures using only the three public questions."""
import json
from pathlib import Path
from pydantic import ValidationError
from app.config import settings
from app.room_service.chatbot.agents import QuestionAnalysisAgent, QuestionPlan
from app.room_service.chatbot.providers import GeminiGenerator


def main():
    questions = json.loads(Path('/eval/reports/graph_rag_compact_pilot_v9_2026-10-06.json').read_text())['cases']
    client = GeminiGenerator('', settings.chatbot_question_analysis_model,
                             base_url=settings.gemini_base_url, api_keys=settings.configured_gemini_keys,
                             legal_timeout_seconds=60, per_request_timeout_seconds=60)
    request = client.request_json
    captured = []

    def capture(*args, **kwargs):
        raw, usage = request(*args, **kwargs)
        captured.append(dict(raw=raw, usage=usage))
        return raw, usage

    client.request_json = capture
    analyzer = QuestionAnalysisAgent(client)
    report = []
    try:
        for question in questions:
            captured.clear()
            result = analyzer.analyze(question['question'])
            errors = []
            if captured:
                try:
                    QuestionPlan.model_validate_json(captured[-1]['raw'])
                except ValidationError as exc:
                    errors = [dict(field='.'.join(map(str, e['loc'])), type=e['type'], message=e['msg'])
                              for e in exc.errors()]
            item = dict(id=question['id'], trace=result.step, errors=errors,
                        public_question=question['question'], captures=list(captured))
            report.append(item)
            print(json.dumps({k: item[k] for k in ('id', 'trace', 'errors')}, ensure_ascii=False), flush=True)
    finally:
        client.close()
    Path('/eval/reports/gemini_focus3_analysis_diagnostics_2026-10-06.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
