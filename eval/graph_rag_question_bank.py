"""Checkpointed Graph RAG regression: private housing contexts stay local.

Legal analysis/synthesis uses the existing public legal workflow. Housing is
processed solely by Ollama or grounded templates. No cloud scoring is performed.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
from sqlalchemy import create_engine, text
from app.config import settings
import question_bank_ragas as bank


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--questions', type=Path, default=Path('/housing_bank.md'))
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--ids', type=int, nargs='+', default=list(range(1, 57)))
    parser.add_argument('--baseline', action='store_true')
    args = parser.parse_args()
    if args.baseline:
        settings.chatbot_graph_enabled = False
    if settings.chatbot_listing_schema != 'housing_graph_v1' or settings.chatbot_llm_provider != 'qwen':
        raise ValueError('Use isolated graph housing corpus with local Qwen housing provider')
    all_cases = bank.load_questions(args.questions)
    selected = [case for case in all_cases if case['id'] in args.ids]
    if len(selected) != len(set(args.ids)):
        raise ValueError('Selected question IDs are missing or duplicated')
    engine = create_engine(settings.database_url)
    with engine.connect() as conn:
        release = dict(conn.execute(text('SELECT * FROM graph_rag_v1.release WHERE id=1')).mappings().one())
        if conn.execute(text('SELECT count(embedding_vector) FROM housing_graph_v1.aggregated_listings')).scalar_one() != 789:
            raise ValueError('Housing embedding corpus is incomplete')
    engine.dispose()
    bank_sha = hashlib.sha256(args.questions.read_bytes()).hexdigest()
    pipeline = Path('/workspace/apps/api/app/room_service/chatbot')
    pipeline_sha = hashlib.sha256(b''.join(p.name.encode() + p.read_bytes() for p in sorted(pipeline.glob('*.py')))).hexdigest()
    identity = {'question_bank_sha256': bank_sha, 'pipeline_sha256': pipeline_sha,
                'selected_original_ids': sorted(args.ids), 'graph_enabled': settings.chatbot_graph_enabled,
                'graph_extractor_version': release['extractor_version'],
                'housing_catalog_sha256': release['housing_sha256'], 'legal_manifest_sha256': release['legal_sha256']}
    report = json.loads(args.output.read_text(encoding='utf-8')) if args.output.exists() else dict(
        identity, started_at_utc=datetime.now(timezone.utc).isoformat(), cases=selected,
        method='real service regression; E5 + bounded typed graph + grounded generation; no invented accuracy score',
        housing_payload_policy='local Qwen only; full report remains local; no cloud housing judge',
        follow_up_protocol='Q15 after Q14; Q16 after Q14,Q15; Q17 and Q18 independently after Q14; full conversation state passed',
        total_original_bank=len(all_cases))
    if any(report.get(key) != value for key, value in identity.items()):
        raise ValueError('Evaluation inputs changed; use a new output path')
    import app.room_service.chatbot.service as service
    from app.room_service.chatbot.providers import _grounded_prompt
    service._evaluation_context = lambda item: _grounded_prompt('', [item]).split('CONTEXT LISTING (JSON):\n', 1)[1]
    try:
        bank.collect(report, args.output, None, args.ids)
    except bank.QuotaPause:
        bank.checkpoint_pause(report, args.output, bank.QUOTA, 'collect')
        raise SystemExit(75)
    bank.summarize(report)
    report['graph_summary'] = {
        'cases_with_graph_trace': sum(any(step.get('stage') == 'graph_retrieval' for step in case.get('agent_trace', [])) for case in report['cases']),
        'selected_cases': len(selected),
        'cloud_housing_calls': sum(call.get('provider') == 'gemini' for case in report['cases'] if case['category'] == 'find_listing' for call in case.get('provider_calls', [])),
    }
    if report['graph_summary']['cloud_housing_calls']:
        raise ValueError('Unexpected cloud housing calls')
    report['updated_at_utc'] = datetime.now(timezone.utc).isoformat()
    bank.save_report(args.output, report)
    print(json.dumps({'summary': report['summary'], 'graph': report['graph_summary']}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
