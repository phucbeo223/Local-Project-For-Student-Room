"""Repeated full-service legal requests with bounded concurrent users."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import json
import math
from pathlib import Path
import statistics
import time
from sqlalchemy import create_engine
from app.config import settings
from app.room_service.chatbot.router import init_chatbot, get_service
from app.room_service.chatbot.schemas import ChatAskRequest
from app.room_service.chatbot.request_telemetry import collect_gemini_calls
import question_bank_ragas as bank
from legal_only_boundary import assert_legal_cases, install
from telemetry_summary import summarize_calls


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--questions-json', type=Path)
    p.add_argument('--ids', type=int, nargs='+', default=[49, 50, 54])
    p.add_argument('--repeats', type=int, default=2)
    p.add_argument('--workers', type=int, nargs='+', default=[1, 3])
    args = p.parse_args()
    if args.output.exists():
        raise ValueError('Use a new output path; never mix benchmark versions')
    if not 1 <= args.repeats <= 5 or any(not 1 <= n <= 4 for n in args.workers):
        raise ValueError('Benchmark exceeds bounded load')
    source_cases = json.loads(args.questions_json.read_text(encoding='utf-8')) if args.questions_json else bank.load_questions(Path('/housing_bank.md'))
    cases = [c for c in source_cases if c['id'] in args.ids]
    assert len(cases) == len(set(args.ids))
    assert_legal_cases(cases)
    pipeline = Path('/workspace/apps/api/app/room_service/chatbot')
    digest = bank.pipeline_sha256(pipeline)
    engine = create_engine(settings.database_url)
    init_chatbot(engine)
    service = get_service()
    boundary = install(service, engine, cases, settings.chatbot_legal_schema)
    service.repo.record_event = lambda payload: None
    report = dict(started_at_utc=datetime.now(timezone.utc).isoformat(), pipeline_sha256=digest,
        legal_schema=settings.chatbot_legal_schema, graph_schema=settings.chatbot_graph_schema,
        configuration=dict(selection_provider=settings.chatbot_legal_selection_provider,
            selection_model=settings.chatbot_legal_selection_model or settings.gemini_model,
            synthesis_model=settings.chatbot_answer_synthesis_model or settings.gemini_model,
            analysis_model=settings.chatbot_question_analysis_model,
            min_request_interval_seconds=settings.gemini_min_request_interval_seconds),
        legal_only_boundary=boundary, method='Full service: analysis, E5 retrieval, selection, synthesis, verification, repair and response serialization. Shared service, thread-local telemetry. No HTTP/auth/transport time.',
        selected_ids=args.ids, repeats=args.repeats, worker_levels=args.workers, cases=[], groups=[])
    manifest = Path('/workspace/docs/legal_word_workflow_v19_20261007/manifest.json')
    report['corpus_manifest_sha256'] = __import__('hashlib').sha256(manifest.read_bytes()).hexdigest() if manifest.exists() else None
    report['runner_sha256'] = __import__('hashlib').sha256(Path(__file__).read_bytes()).hexdigest()

    def request(case, repeat, workers):
        calls = []
        start = time.perf_counter()
        record = dict(case, repeat=repeat, workers=workers)
        try:
            with collect_gemini_calls(calls.append):
                result = service.ask(ChatAskRequest(message=case['question'], include_evaluation_contexts=True))
                data = result.model_dump(mode='json')
            record.update(data)
        except Exception as exc:
            record['error_type'] = type(exc).__name__
        record.update(full_service_latency_ms=round((time.perf_counter()-start)*1000), provider_calls=calls)
        if any(c.get('provider') != 'gemini' for c in calls):
            raise ValueError('Evaluation observed a non-Gemini model call')
        return record

    # Keep warm-up visible; don't hide its requests or cost in load samples.
    report['warmup'] = request(cases[0], 0, 1)
    bank.save_report(args.output, report)
    for workers in args.workers:
        assert bank.pipeline_sha256(pipeline) == digest, 'Code changed during benchmark'
        started = time.perf_counter()
        group = []
        with ThreadPoolExecutor(max_workers=workers) as pool:
            jobs = [pool.submit(request, c, repeat, workers) for repeat in range(1, args.repeats+1) for c in cases]
            for job in as_completed(jobs):
                row = job.result()
                group.append(row)
                report['cases'].append(row)
                bank.save_report(args.output, report)
                print(f"users={workers} Q{row['id']} repeat={row['repeat']} {row['full_service_latency_ms']}ms error={row.get('error_type')}", flush=True)
        elapsed = time.perf_counter()-started
        times = sorted(r['full_service_latency_ms'] for r in group)
        report['groups'].append(dict(workers=workers, requests=len(group), p50_ms=statistics.median(times),
            p95_ms=times[math.ceil(.95*len(times))-1], wall_seconds=round(elapsed, 2),
            throughput_per_minute=round(len(group)/elapsed*60, 2), errors=sum('error_type' in r for r in group),
            partial=sum(bool(r.get('partial_answer')) for r in group), telemetry=summarize_calls(group)))
        bank.save_report(args.output, report)
    assert bank.pipeline_sha256(pipeline) == digest
    report.update(completed=True, finished_at_utc=datetime.now(timezone.utc).isoformat(), telemetry=summarize_calls(report['cases']))
    bank.save_report(args.output, report)
    print(json.dumps(report['groups']), flush=True)
    engine.dispose()


if __name__ == '__main__':
    main()
