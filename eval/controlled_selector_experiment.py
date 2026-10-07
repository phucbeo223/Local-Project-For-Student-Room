"""Controlled A/B experiment: Compare Qwen vs Gemini at the legal source selection step only.

Both branches share:
- Identical question bank (36 legal questions: IDs 19-38 and 43-58)
- Identical question plan & candidate retrieval snapshot (computed once, saved & hashed)
- Identical Gemini writer (GeminiAnswerSynthesisAgent, separate request)
- Identical Gemini verifier (per-claim verification, max 1 repair)
- Identical local Qwen V15 judge and rubric (compare_grounded_references.py)
- Identical legal-only data boundary (fail closed)

The ONLY independent variable is the source selection provider:
Branch A: Qwen source selector
Branch B: Gemini source selector
"""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from typing import Any, Literal
from urllib.parse import urlparse

from sqlalchemy import create_engine, text
from app.config import settings
from app.room_service.chatbot.agents import (
    AnalysisResult,
    LegalRetrievalAgent,
    QuestionAnalysisAgent,
    QuestionPlan,
)
from app.room_service.chatbot.agent_workflow import (
    GeminiAnswerSynthesisAgent,
    LegalAgentWorkflow,
)
from app.room_service.chatbot.gemini_selection import GeminiEvidenceSelector
from app.room_service.chatbot.graph_retrieval import GraphChatRepository
from app.room_service.chatbot.providers import (
    E5EmbeddingProvider,
    FallbackResponseGenerator,
    GeminiGenerator,
    GroundedTemplateGenerator,
    OllamaQwenGenerator,
)
from app.room_service.chatbot.repo import ChatRepository
from app.room_service.chatbot.schemas import ChatAskRequest
from app.room_service.chatbot.service import ChatService
from app.room_service.chatbot.source_selection import selection_candidates
import legal_only_boundary
import question_bank_ragas as bank


DEFAULT_IDS = list(range(19, 39)) + list(range(43, 59))
PILOT_IDS = [24, 28, 36, 45]


def get_git_commit() -> str:
    import os
    env_commit = os.environ.get('GIT_COMMIT')
    if env_commit:
        return env_commit.strip()
    try:
        res = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True, check=True)
        return res.stdout.strip()
    except Exception:
        pass
    try:
        head_path = Path('/workspace/.git/HEAD')
        if head_path.exists():
            ref = head_path.read_text().strip()
            if ref.startswith('ref: '):
                ref_path = Path('/workspace/.git') / ref[5:].strip()
                if ref_path.exists():
                    return ref_path.read_text().strip()
            return ref
    except Exception:
        pass
    return 'unknown'


def compute_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_snapshot_digest(data: dict) -> str:
    """Compute content digest ignoring any self-referencing hash or metadata digest keys."""
    clean = {k: v for k, v in data.items() if not k.endswith('_sha256') and k not in ('sha256', 'digest')}
    dumped = json.dumps(clean, ensure_ascii=False, indent=2).encode('utf-8')
    return hashlib.sha256(dumped).hexdigest()


def compute_code_digest() -> str:
    """Compute deterministic SHA256 of all relevant code affecting selection, writer and evaluation."""
    candidate_files = [
        Path('/workspace/apps/api/app/room_service/chatbot/agent_workflow.py'),
        Path('/workspace/apps/api/app/room_service/chatbot/agents.py'),
        Path('/workspace/apps/api/app/room_service/chatbot/gemini_selection.py'),
        Path('/workspace/apps/api/app/room_service/chatbot/source_selection.py'),
        Path('/workspace/apps/api/app/room_service/chatbot/claim_verification.py'),
        Path('/workspace/apps/api/app/room_service/chatbot/router.py'),
        Path('/workspace/apps/api/app/room_service/chatbot/service.py'),
        Path('/workspace/apps/api/app/room_service/chatbot/providers.py'),
        Path('/workspace/apps/api/app/config.py'),
        Path('/workspace/eval/controlled_selector_experiment.py'),
        Path('/workspace/eval/legal_only_boundary.py'),
        # Host fallbacks
        Path('apps/api/app/room_service/chatbot/agent_workflow.py'),
        Path('apps/api/app/room_service/chatbot/agents.py'),
        Path('apps/api/app/room_service/chatbot/gemini_selection.py'),
        Path('apps/api/app/room_service/chatbot/source_selection.py'),
        Path('apps/api/app/room_service/chatbot/claim_verification.py'),
        Path('apps/api/app/room_service/chatbot/router.py'),
        Path('apps/api/app/room_service/chatbot/service.py'),
        Path('apps/api/app/room_service/chatbot/providers.py'),
        Path('apps/api/app/config.py'),
        Path('eval/controlled_selector_experiment.py'),
        Path('eval/legal_only_boundary.py'),
    ]
    seen = set()
    h = hashlib.sha256()
    for p in candidate_files:
        if p.exists() and p.name not in seen:
            seen.add(p.name)
            h.update(p.name.encode('utf-8'))
            h.update(p.read_bytes())
    return h.hexdigest()


def compute_run_identity(
    cases: list[dict],
    snapshot_digest: str,
    legal_chunks_count: int,
    graph_release_count: int,
) -> dict[str, Any]:
    """Lock entire run configuration, code digest, corpus state, and models."""
    ident = {
        'code_digest': compute_code_digest(),
        'git_commit': get_git_commit(),
        'snapshot_digest': snapshot_digest,
        'question_ids': sorted(c['id'] for c in cases),
        'legal_schema': settings.chatbot_legal_schema,
        'graph_schema': settings.chatbot_graph_schema,
        'listing_schema': settings.chatbot_listing_schema,
        'legal_chunks_count': legal_chunks_count,
        'graph_release_count': graph_release_count,
        'models': {
            'qwen_selector': settings.ollama_model,
            'gemini_selector': settings.chatbot_legal_selection_model or settings.gemini_model,
            'writer': settings.chatbot_answer_synthesis_model or settings.gemini_model,
            'verifier': settings.gemini_model,
            'judge': settings.ollama_model,
        },
        'generation_mode': 'separate',
    }
    ident_digest = hashlib.sha256(json.dumps(ident, sort_keys=True, ensure_ascii=False).encode('utf-8')).hexdigest()
    ident['identity_sha256'] = ident_digest
    return ident


def save_atomic_checkpoint(path: Path, data: dict):
    """Write checkpoint atomically to prevent corrupted or partial file on interruption."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix('.tmp')
    tmp_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    tmp_path.replace(path)


class MockEmbedding:
    def __init__(self, vector=None, degraded_reason=None):
        self.vector = vector
        self.degraded_reason = degraded_reason


def build_service_for_selector(
    engine,
    selection_provider: Literal['qwen', 'gemini'],
    cases: list[dict],
):
    """Build a ChatService configured for separate selection with the specified provider."""
    # 1. Selector provider
    if selection_provider == 'qwen':
        selector = OllamaQwenGenerator(
            settings.ollama_base_url,
            settings.ollama_model,
            settings.chatbot_llm_timeout_seconds,
            context_length=settings.ollama_context_length,
            max_output_tokens=settings.chatbot_max_output_tokens,
            keep_alive=settings.ollama_keep_alive,
            legal_timeout_seconds=settings.chatbot_legal_timeout_seconds,
            legal_answer_mode='source_select',
        )
    elif selection_provider == 'gemini':
        selection_client = GeminiGenerator(
            '',
            settings.chatbot_legal_selection_model or settings.gemini_model,
            base_url=settings.gemini_base_url,
            api_keys=settings.configured_gemini_keys,
            legal_timeout_seconds=settings.chatbot_legal_selection_timeout_seconds,
            per_request_timeout_seconds=settings.chatbot_legal_selection_timeout_seconds,
            min_request_interval_seconds=settings.gemini_min_request_interval_seconds,
        )
        selector = GeminiEvidenceSelector(selection_client)
    else:
        raise ValueError(f'Invalid selection_provider: {selection_provider}')

    generator = FallbackResponseGenerator([selector], GroundedTemplateGenerator())

    # 2. Question analysis client (for initial analysis if needed)
    analysis_client = GeminiGenerator(
        '',
        settings.chatbot_question_analysis_model,
        base_url=settings.gemini_base_url,
        api_keys=settings.configured_gemini_keys,
        legal_timeout_seconds=settings.chatbot_question_analysis_timeout_seconds,
        per_request_timeout_seconds=settings.chatbot_question_analysis_timeout_seconds,
        min_request_interval_seconds=settings.gemini_min_request_interval_seconds,
    ) if settings.configured_gemini_keys else None
    analyzer = QuestionAnalysisAgent(analysis_client) if analysis_client else None

    # 3. Writer and verifier clients (IDENTICAL for both branches)
    synthesis_model = settings.chatbot_answer_synthesis_model or settings.gemini_model
    synthesis_client = GeminiGenerator(
        '',
        synthesis_model,
        base_url=settings.gemini_base_url,
        api_keys=settings.configured_gemini_keys,
        legal_timeout_seconds=settings.chatbot_answer_synthesis_timeout_seconds,
        per_request_timeout_seconds=settings.chatbot_answer_synthesis_timeout_seconds,
        min_request_interval_seconds=settings.gemini_min_request_interval_seconds,
    )
    writer = GeminiAnswerSynthesisAgent(synthesis_client)
    verifier = synthesis_client

    workflow = LegalAgentWorkflow(generator, writer, verifier)

    if settings.chatbot_graph_enabled:
        repo = GraphChatRepository(
            engine,
            settings.chatbot_legal_schema,
            settings.chatbot_listing_schema,
            settings.chatbot_graph_schema,
        )
    else:
        repo = ChatRepository(engine, settings.chatbot_legal_schema, settings.chatbot_listing_schema)

    embedder = E5EmbeddingProvider(settings.chatbot_embedding_model)

    service = ChatService(
        repo,
        embedder,
        workflow,
        confidence_threshold=settings.chatbot_confidence_threshold,
        max_results=settings.chatbot_max_results,
        question_analyzer=analyzer,
    )

    legal_only_boundary.install(service, engine, cases, settings.chatbot_legal_schema)
    return service, selector, writer, verifier


def generate_input_snapshot(
    engine,
    cases: list[dict],
    snapshot_path: Path,
) -> dict[str, Any]:
    """Analyze questions and retrieve candidate chunks once, creating a fixed snapshot."""
    print(f'[SNAPSHOT] Generating input snapshot for {len(cases)} questions...', flush=True)
    if settings.chatbot_graph_enabled:
        repo = GraphChatRepository(
            engine,
            settings.chatbot_legal_schema,
            settings.chatbot_listing_schema,
            settings.chatbot_graph_schema,
        )
    else:
        repo = ChatRepository(engine, settings.chatbot_legal_schema, settings.chatbot_listing_schema)

    embedder = E5EmbeddingProvider(settings.chatbot_embedding_model)
    analysis_client = GeminiGenerator(
        '',
        settings.chatbot_question_analysis_model,
        base_url=settings.gemini_base_url,
        api_keys=settings.configured_gemini_keys,
        legal_timeout_seconds=settings.chatbot_question_analysis_timeout_seconds,
        per_request_timeout_seconds=settings.chatbot_question_analysis_timeout_seconds,
        min_request_interval_seconds=settings.gemini_min_request_interval_seconds,
    )
    analyzer = QuestionAnalysisAgent(analysis_client)
    retriever = LegalRetrievalAgent(repo, embedder, settings.chatbot_max_results)

    snapshot_items = []
    for idx, case in enumerate(cases):
        q_id = case['id']
        question = case['question']
        print(f'  [SNAPSHOT {idx+1}/{len(cases)}] Q{q_id:02d}: {question[:60]}...', flush=True)

        t_ana_start = time.perf_counter()
        analyzed = analyzer.analyze(question)
        ana_ms = round((time.perf_counter() - t_ana_start) * 1000)

        t_ret_start = time.perf_counter()
        chunks, embedded, ret_step = retriever.retrieve(question, analyzed.plan)
        ret_ms = round((time.perf_counter() - t_ret_start) * 1000)

        top_score = float(chunks[0]['similarity_score']) if chunks else 0.0
        confidence = min(0.97, 0.22 + 0.75 * top_score) if chunks else 0.0
        if confidence < settings.chatbot_confidence_threshold:
            filtered_chunks = []
        else:
            filtered_chunks = chunks

        candidates = selection_candidates(filtered_chunks)

        snapshot_items.append({
            'id': q_id,
            'question': question,
            'category': case.get('category'),
            'question_plan': analyzed.plan.model_dump(mode='json'),
            'analysis_step': analyzed.step,
            'analysis_degraded_reasons': analyzed.degraded_reasons,
            'analysis_latency_ms': ana_ms,
            'contexts': filtered_chunks,
            'has_embedding_vector': embedded.vector is not None,
            'retrieval_step': ret_step,
            'retrieval_latency_ms': ret_ms,
            'candidate_count': len(candidates),
            'candidates': candidates,
        })

    snapshot_data = {
        'version': '1.0',
        'created_at_utc': datetime.now(timezone.utc).isoformat(),
        'legal_schema': settings.chatbot_legal_schema,
        'graph_schema': settings.chatbot_graph_schema,
        'listing_schema': settings.chatbot_listing_schema,
        'embedding_model': settings.chatbot_embedding_model,
        'analysis_model': settings.chatbot_question_analysis_model,
        'case_count': len(snapshot_items),
        'cases': snapshot_items,
    }

    digest = canonical_snapshot_digest(snapshot_data)
    snapshot_data['snapshot_sha256'] = digest
    snapshot_path.parent.mkdir(parents=True, exist_ok=True)
    snapshot_path.write_text(json.dumps(snapshot_data, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'[SNAPSHOT] Saved snapshot to {snapshot_path} (Canonical SHA256: {digest})', flush=True)
    return snapshot_data


def load_or_create_snapshot(engine, cases: list[dict], snapshot_path: Path) -> tuple[dict, str]:
    if snapshot_path.exists():
        data = json.loads(snapshot_path.read_text(encoding='utf-8'))
        actual_digest = canonical_snapshot_digest(data)
        stored_digest = data.get('snapshot_sha256')

        if stored_digest and stored_digest != actual_digest:
            raise ValueError(
                f'Snapshot digest mismatch in {snapshot_path}: stored={stored_digest[:12]}, actual={actual_digest[:12]}. '
                'Data has been modified since generation.'
            )

        if data.get('legal_schema') != settings.chatbot_legal_schema:
            raise ValueError(
                f'Snapshot legal_schema ({data.get("legal_schema")}) != current settings ({settings.chatbot_legal_schema})'
            )

        if data.get('embedding_model') != settings.chatbot_embedding_model:
            raise ValueError(
                f'Snapshot embedding_model ({data.get("embedding_model")}) != current settings ({settings.chatbot_embedding_model})'
            )

        by_id = {c['id']: c for c in data.get('cases', [])}
        req_ids = {c['id'] for c in cases}
        if not req_ids.issubset(set(by_id.keys())):
            missing = sorted(req_ids - set(by_id.keys()))
            raise ValueError(f'Snapshot {snapshot_path} missing requested question IDs: {missing}')

        for req in cases:
            snap_c = by_id[req['id']]
            if snap_c.get('question') != req['question']:
                raise ValueError(
                    f'Snapshot question text changed for ID {req["id"]}: '
                    f'expected {req["question"][:50]}..., found {snap_c.get("question", "")[:50]}...'
                )
            if not snap_c.get('question_plan') or not snap_c.get('contexts') or not snap_c.get('candidates'):
                raise ValueError(f'Incomplete snapshot contents for question ID {req["id"]}')

        print(f'[SNAPSHOT] Validated and loaded existing snapshot from {snapshot_path} (Digest: {actual_digest})', flush=True)
        return data, actual_digest

    data = generate_input_snapshot(engine, cases, snapshot_path)
    digest = canonical_snapshot_digest(data)
    return data, digest


def run_single_branch_question(
    service: ChatService,
    snapshot_entry: dict,
    selection_provider: str,
    traced_calls: list[dict],
) -> dict[str, Any]:
    """Execute one question through the exact ChatService pipeline using fixed snapshot inputs."""
    question = snapshot_entry['question']
    plan = QuestionPlan.model_validate(snapshot_entry['question_plan'])
    contexts = snapshot_entry['contexts']

    # Patch analyzer and retriever to return exact snapshot data in 0ms
    orig_analyze = service.question_analyzer.analyze if service.question_analyzer else None
    service.question_analyzer.analyze = lambda q: AnalysisResult(
        plan, snapshot_entry['analysis_step'], snapshot_entry.get('analysis_degraded_reasons', [])
    )

    from app.room_service.chatbot.agents import LegalRetrievalAgent
    orig_retrieve = LegalRetrievalAgent.retrieve
    mock_embedded = MockEmbedding(vector=[1.0] if snapshot_entry.get('has_embedding_vector') else None)
    LegalRetrievalAgent.retrieve = lambda self, q, p: (contexts, mock_embedded, snapshot_entry['retrieval_step'])

    traced_calls.clear()
    t_start = time.perf_counter()
    try:
        res = service.ask(ChatAskRequest(
            message=question,
            include_evaluation_contexts=True,
        ))
        total_ms = round((time.perf_counter() - t_start) * 1000)
        data = res.model_dump(mode='json')

        # Extract selection trace
        sel_trace = next((s for s in data.get('agent_trace', []) if s.get('agent') == 'evidence_selection'), {})
        sel_decision = next((s for s in data.get('agent_trace', []) if s.get('agent') == 'selection_decision'), {})
        coverage_trace = next((s for s in data.get('agent_trace', []) if s.get('agent') == 'evidence_coverage_completion'), {})

        # Extract synthesis trace
        synth_traces = [s for s in data.get('agent_trace', []) if s.get('agent') == 'answer_synthesis']
        # Extract verification trace
        verif_traces = [s for s in data.get('agent_trace', []) if s.get('agent') == 'source_verification']

        # Determine repairs, fallback, retained
        repair_performed = any(s.get('repair') for s in synth_traces)
        partial_retained = any(s.get('status') == 'partial_retained' for s in verif_traces)

        is_fallback = (
            data.get('generation_provider') == 'grounded_template' or
            not data.get('sources') or
            any(s.get('status') == 'skipped' and s.get('reason') == 'no_selected_evidence' for s in data.get('agent_trace', [])) or
            any(s.get('fallback') for s in verif_traces) or
            any(s.get('status') == 'fallback' for s in synth_traces)
        )

        by_rank = {c['rank']: c['id'] for c in snapshot_entry['candidates']}
        final_selected_ranks = sel_trace.get('selected_ranks', [])
        final_selected_cand_ids = [by_rank[r] for r in final_selected_ranks if r in by_rank]

        attempts = sel_decision.get('attempts', [])
        model_attempts_ids = [a.get('selected_ids', []) for a in attempts]
        raw_model_ids = attempts[-1].get('selected_ids', []) if attempts else final_selected_cand_ids

        rule_added_ranks = coverage_trace.get('added_ranks', [])
        rule_added_ids = [by_rank[r] for r in rule_added_ranks if r in by_rank]

        return {
            'id': snapshot_entry['id'],
            'question': question,
            'category': snapshot_entry['category'],
            'selection_provider': selection_provider,
            'answer': data['answer'],
            'no_answer': data['no_answer'],
            'partial_answer': data.get('partial_answer', False),
            'degraded': data['degraded'],
            'degraded_reasons': data['degraded_reasons'],
            'total_selection_to_final_ms': total_ms,
            'selection_ms': sel_trace.get('duration_ms', 0),
            'raw_model_selected_ids': raw_model_ids,
            'model_selected_ids_by_attempt': model_attempts_ids,
            'rule_supplemented_ranks': rule_added_ranks,
            'rule_supplemented_ids': rule_added_ids,
            'selected_ranks': final_selected_ranks,
            'selected_candidate_ids': final_selected_cand_ids,
            'final_evidence_ranks': final_selected_ranks,
            'final_evidence_candidate_ids': final_selected_cand_ids,
            'selection_attempts': attempts,
            'selection_missing_facets': sel_decision.get('missing_facets', []),
            'repair_performed': repair_performed,
            'partial_retained': partial_retained,
            'fallback_source': is_fallback,
            'citation_accuracy': data.get('citation_accuracy', 1.0),
            'sources': data.get('sources', []),
            'agent_trace': data.get('agent_trace', []),
            'provider_calls': list(traced_calls),
            'analysis_latency_ms': snapshot_entry['analysis_latency_ms'],
            'retrieval_latency_ms': snapshot_entry['retrieval_latency_ms'],
        }
    finally:
        if orig_analyze and service.question_analyzer:
            service.question_analyzer.analyze = orig_analyze
        LegalRetrievalAgent.retrieve = orig_retrieve


def setup_call_tracing(service: ChatService, provider_name: str) -> list[dict]:
    """Record LLM requests with latency, usage, and prompt/response shapes."""
    calls = []
    # 1. Tracing writer and verifier (GeminiGenerator)
    writer_client = getattr(getattr(service.generator, 'writer', None), 'client', None)
    if writer_client and hasattr(writer_client, 'request_json'):
        orig_req = writer_client.request_json
        def traced_req(prompt, schema, **kwargs):
            t0 = time.perf_counter()
            props = schema.get('properties', {})
            stage = ('answer_synthesis' if 'summary' in props else 'source_verification')
            rec = {'provider': 'gemini', 'model': writer_client.model, 'stage': stage}
            try:
                res, usage = orig_req(prompt, schema, **kwargs)
                rec.update(success=True, usage=usage)
                return res, usage
            except Exception as exc:
                rec.update(success=False, error_type=type(exc).__name__, error_message=str(exc)[:300])
                raise
            finally:
                rec['latency_ms'] = round((time.perf_counter() - t0) * 1000)
                calls.append(rec)
        writer_client.request_json = traced_req

    # 2. Tracing selector
    for prov in getattr(service.generator, 'providers', []):
        if getattr(prov, 'provider_name', None) == 'gemini':
            client = getattr(prov, 'client', None)
            if client and hasattr(client, 'request_json'):
                orig_sel_req = client.request_json
                def traced_sel(prompt, schema, **kwargs):
                    t0 = time.perf_counter()
                    rec = {'provider': 'gemini', 'model': client.model, 'stage': 'evidence_selection'}
                    try:
                        res, usage = orig_sel_req(prompt, schema, **kwargs)
                        rec.update(success=True, usage=usage)
                        return res, usage
                    except Exception as exc:
                        rec.update(success=False, error_type=type(exc).__name__, error_message=str(exc)[:300])
                        raise
                    finally:
                        rec['latency_ms'] = round((time.perf_counter() - t0) * 1000)
                        calls.append(rec)
                client.request_json = traced_sel
        elif isinstance(prov, OllamaQwenGenerator):
            orig_post = prov._client.post
            def traced_qwen_post(url, **kwargs):
                t0 = time.perf_counter()
                rec = {'provider': 'qwen', 'model': prov.model, 'stage': 'evidence_selection'}
                try:
                    res = orig_post(url, **kwargs)
                    rec.update(success=res.is_success, status_code=res.status_code)
                    return res
                except Exception as exc:
                    rec.update(success=False, error_type=type(exc).__name__, error_message=str(exc)[:300])
                    raise
                finally:
                    rec['latency_ms'] = round((time.perf_counter() - t0) * 1000)
                    calls.append(rec)
            prov._client.post = traced_qwen_post

    return calls


def warmup_models():
    """Warm up Ollama and ping Gemini proxy before timing tests."""
    print('[WARMUP] Warming up Ollama and Gemini proxy...', flush=True)
    try:
        qwen = OllamaQwenGenerator(settings.ollama_base_url, settings.ollama_model, 30)
        qwen.warmup()
        qwen.close()
        print('  Ollama warmup OK', flush=True)
    except Exception as exc:
        print(f'  Ollama warmup warning: {exc}', flush=True)

def close_service_clients(*clients_or_services):
    """Safely close network clients (Ollama httpx, Gemini httpx) in finally block."""
    for obj in clients_or_services:
        if obj is None:
            continue
        if hasattr(obj, 'close') and callable(obj.close):
            try:
                obj.close()
            except Exception:
                pass
        sub_client = getattr(obj, 'client', None)
        if sub_client and hasattr(sub_client, 'close') and callable(sub_client.close):
            try:
                sub_client.close()
            except Exception:
                pass
        gen = getattr(obj, 'generator', None)
        if gen:
            for prov in getattr(gen, 'providers', []):
                close_service_clients(prov)
            writer = getattr(gen, 'writer', None)
            if writer:
                close_service_clients(writer)


def run_experiment(
    engine,
    cases: list[dict],
    snapshot_data: dict,
    run_name: str,
    output_dir: Path,
    run_identity: dict[str, Any],
    skip_v15: bool = False,
):
    """Run controlled A/B test with alternating order between questions and atomic per-branch checkpointing."""
    print(f'\n=== STARTING CONTROLLED A/B EXPERIMENT: {run_name} ===', flush=True)
    print(f'Run Identity SHA256: {run_identity["identity_sha256"]}', flush=True)
    print(f'Code Digest SHA256:   {run_identity["code_digest"]}', flush=True)
    warmup_models()

    service_qwen, sel_qwen, writer_qwen, verif_qwen = build_service_for_selector(engine, 'qwen', cases)
    service_gemini, sel_gemini, writer_gemini, verif_gemini = build_service_for_selector(engine, 'gemini', cases)

    calls_qwen = setup_call_tracing(service_qwen, 'qwen')
    calls_gemini = setup_call_tracing(service_gemini, 'gemini')

    checkpoint_path = output_dir / f'{run_name}_checkpoint.json'
    results_a_by_id: dict[int, dict] = {}
    results_b_by_id: dict[int, dict] = {}

    # Resume from checkpoint ONLY if run_identity SHA256 matches exactly
    if checkpoint_path.exists():
        try:
            ckpt = json.loads(checkpoint_path.read_text(encoding='utf-8'))
            ckpt_ident = ckpt.get('run_identity', {})
            ckpt_sha = ckpt.get('identity_sha256') or ckpt_ident.get('identity_sha256')
            curr_sha = run_identity.get('identity_sha256')
            if ckpt.get('run_name') == run_name and ckpt_sha == curr_sha:
                for r in ckpt.get('results_a', []):
                    results_a_by_id[r['id']] = r
                for r in ckpt.get('results_b', []):
                    results_b_by_id[r['id']] = r
                print(f'[CHECKPOINT] Identity match! Resumed: Branch A has {len(results_a_by_id)}, Branch B has {len(results_b_by_id)} completed.', flush=True)
            else:
                print(f'[CHECKPOINT] Identity or configuration changed (stored={ckpt_sha[:12] if ckpt_sha else "none"} vs current={curr_sha[:12]}). Refusing to resume from incompatible checkpoint; starting fresh.', flush=True)
        except Exception as exc:
            print(f'[CHECKPOINT] Warning reading checkpoint: {exc}. Starting fresh.', flush=True)

    by_id = {c['id']: c for c in snapshot_data['cases']}

    try:
        for idx, case in enumerate(cases):
            q_id = case['id']
            snap_item = by_id[q_id]

            # Alternating order: even idx -> A then B; odd idx -> B then A
            if idx % 2 == 0:
                order = [('A', 'qwen', service_qwen, calls_qwen), ('B', 'gemini', service_gemini, calls_gemini)]
            else:
                order = [('B', 'gemini', service_gemini, calls_gemini), ('A', 'qwen', service_qwen, calls_qwen)]

            needs_work = False
            for branch_label, _, _, _ in order:
                target_dict = results_a_by_id if branch_label == 'A' else results_b_by_id
                if q_id not in target_dict:
                    needs_work = True
                    break

            if not needs_work:
                continue

            print(f'\n--- Question {idx+1}/{len(cases)}: ID {q_id} ---', flush=True)
            print(f'Q: {snap_item["question"]}', flush=True)

            for branch_label, prov, srv, call_list in order:
                target_dict = results_a_by_id if branch_label == 'A' else results_b_by_id
                if q_id in target_dict:
                    continue

                print(f'  Executing Branch {branch_label} ({prov} selector)...', flush=True)
                res = run_single_branch_question(srv, snap_item, prov, call_list)
                print(f'    Raw Model IDs: {res["raw_model_selected_ids"]} | Final IDs: {res["final_evidence_candidate_ids"]} (ranks: {res["final_evidence_ranks"]})')
                print(f'    Selection Latency: {res["selection_ms"]} ms | Total Replay: {res["total_selection_to_final_ms"]} ms')
                print(f'    Repaired: {res["repair_performed"]} | Partial retained: {res["partial_retained"]} | Fallback: {res["fallback_source"]}')

                target_dict[q_id] = res

                # Atomic checkpoint after every single branch completion to prevent any data loss
                save_atomic_checkpoint(checkpoint_path, {
                    'run_name': run_name,
                    'run_identity': run_identity,
                    'identity_sha256': run_identity['identity_sha256'],
                    'snapshot_sha256': snapshot_data.get('snapshot_sha256'),
                    'updated_at_utc': datetime.now(timezone.utc).isoformat(),
                    'results_a': list(results_a_by_id.values()),
                    'results_b': list(results_b_by_id.values()),
                })
    finally:
        # Guarantee all client connections are gracefully closed
        close_service_clients(service_qwen, sel_qwen, writer_qwen, verif_qwen)
        close_service_clients(service_gemini, sel_gemini, writer_gemini, verif_gemini)

    # Sort results deterministically by question ID
    results_a = sorted(results_a_by_id.values(), key=lambda r: r['id'])
    results_b = sorted(results_b_by_id.values(), key=lambda r: r['id'])

    # Save final branch run files for V15 scoring
    run_file_a = output_dir / f'{run_name}_branch_a_qwen.json'
    run_file_b = output_dir / f'{run_name}_branch_b_gemini.json'

    meta_a = {
        'run_name': f'{run_name}_branch_a_qwen',
        'run_identity': run_identity,
        'pipeline_sha256': bank.pipeline_sha256(Path('/workspace/apps/api/app/room_service/chatbot')),
        'git_commit': get_git_commit(),
        'snapshot_sha256': snapshot_data.get('snapshot_sha256'),
        'legal_selection_provider': 'qwen',
        'legal_selection_model': settings.ollama_model,
        'legal_generation_mode': 'separate',
        'legal_schema': settings.chatbot_legal_schema,
        'selected_original_ids': [r['id'] for r in results_a],
        'cases': results_a,
    }
    meta_b = {
        'run_name': f'{run_name}_branch_b_gemini',
        'run_identity': run_identity,
        'pipeline_sha256': bank.pipeline_sha256(Path('/workspace/apps/api/app/room_service/chatbot')),
        'git_commit': get_git_commit(),
        'snapshot_sha256': snapshot_data.get('snapshot_sha256'),
        'legal_selection_provider': 'gemini',
        'legal_selection_model': settings.chatbot_legal_selection_model or settings.gemini_model,
        'legal_generation_mode': 'separate',
        'legal_schema': settings.chatbot_legal_schema,
        'selected_original_ids': [r['id'] for r in results_b],
        'cases': results_b,
    }

    save_atomic_checkpoint(run_file_a, meta_a)
    save_atomic_checkpoint(run_file_b, meta_b)
    print(f'[OUTPUT] Saved Branch A run file to {run_file_a}', flush=True)
    print(f'[OUTPUT] Saved Branch B run file to {run_file_b}', flush=True)

    # Run V15 scoring
    v15_report_a = output_dir / f'{run_name}_branch_a_v15.json'
    v15_report_b = output_dir / f'{run_name}_branch_b_v15.json'

    if not skip_v15:
        print('\n=== RUNNING V15 EVALUATION ON BOTH BRANCHES ===', flush=True)
        eval_v15(run_file_a, v15_report_a, [r['id'] for r in results_a])
        eval_v15(run_file_b, v15_report_b, [r['id'] for r in results_b])
    else:
        print('[V15] Skipped V15 judging as requested.', flush=True)

    # Generate comprehensive report
    report_md_path = output_dir / f'{run_name}_comparison_report.md'
    report_json_path = output_dir / f'{run_name}_comparison_report.json'
    generate_full_report(
        results_a,
        results_b,
        snapshot_data,
        v15_report_a if v15_report_a.exists() else None,
        v15_report_b if v15_report_b.exists() else None,
        report_md_path,
        report_json_path,
        run_name,
        run_identity=run_identity,
    )


def eval_v15(run_file: Path, output_file: Path, ids: list[int]):
    """Execute compare_grounded_references.py using local Ollama Qwen judge."""
    print(f'[V15] Scoring {run_file.name} -> {output_file.name}...', flush=True)
    script_path = Path('/workspace/eval/compare_grounded_references.py') if Path('/workspace/eval/compare_grounded_references.py').exists() else Path('eval/compare_grounded_references.py')
    cmd = [
        sys.executable,
        str(script_path),
        '--run', str(run_file),
        '--output', str(output_file),
        '--ids', ','.join(map(str, ids)),
    ]
    env = dict(os.environ, GIT_PYTHON_REFRESH='quiet')
    res = subprocess.run(cmd, capture_output=True, text=True, env=env)
    if res.returncode != 0:
        print(f'[V15] Error during scoring:\n{res.stderr}\n{res.stdout}', flush=True)
        raise RuntimeError(f'V15 scoring failed for {run_file}')
    print(f'[V15] Completed scoring {run_file.name}.', flush=True)


def calculate_stats(values: list[float]) -> dict[str, float]:
    if not values:
        return {'median': 0, 'p95': 0, 'mean': 0, 'min': 0, 'max': 0}
    s = sorted(values)
    n = len(s)
    med = s[n // 2] if n % 2 != 0 else (s[n // 2 - 1] + s[n // 2]) / 2.0
    idx95 = max(0, min(n - 1, int(0.95 * n)))
    p95 = s[idx95]
    return {
        'median': round(med, 2),
        'p95': round(p95, 2),
        'mean': round(sum(s) / n, 2),
        'min': round(s[0], 2),
        'max': round(s[-1], 2),
    }


def generate_full_report(
    results_a: list[dict],
    results_b: list[dict],
    snapshot_data: dict,
    v15_file_a: Path | None,
    v15_file_b: Path | None,
    md_out: Path,
    json_out: Path,
    run_name: str,
    run_identity: dict[str, Any] | None = None,
):
    """Generate rigorous paired side-by-side comparison tables, selection audit, and V15 analysis."""
    print('[REPORT] Generating comprehensive comparison report...', flush=True)
    v15_a = json.loads(v15_file_a.read_text(encoding='utf-8')) if v15_file_a and v15_file_a.exists() else {}
    v15_b = json.loads(v15_file_b.read_text(encoding='utf-8')) if v15_file_b and v15_file_b.exists() else {}

    v15_cases_a = {c['id']: c for c in v15_a.get('cases', [])}
    v15_cases_b = {c['id']: c for c in v15_b.get('cases', [])}

    by_snap = {c['id']: c for c in snapshot_data['cases']}

    res_a_by_id = {r['id']: r for r in results_a}
    res_b_by_id = {r['id']: r for r in results_b}
    common_ids = sorted(set(res_a_by_id.keys()) & set(res_b_by_id.keys()))

    if len(res_a_by_id) != len(results_a):
        print(f'[WARN] Duplicate IDs detected in Branch A: total={len(results_a)} vs unique={len(res_a_by_id)}')
    if len(res_b_by_id) != len(results_b):
        print(f'[WARN] Duplicate IDs detected in Branch B: total={len(results_b)} vs unique={len(res_b_by_id)}')
    if set(res_a_by_id.keys()) != set(res_b_by_id.keys()):
        diff_ab = set(res_a_by_id.keys()) ^ set(res_b_by_id.keys())
        print(f'[WARN] Asymmetric IDs between branches: {diff_ab}')

    # Latencies
    sel_lat_a = [r['selection_ms'] / 1000.0 for r in results_a]
    sel_lat_b = [r['selection_ms'] / 1000.0 for r in results_b]
    tot_lat_a = [r['total_selection_to_final_ms'] / 1000.0 for r in results_a]
    tot_lat_b = [r['total_selection_to_final_ms'] / 1000.0 for r in results_b]
    fixed_ana = [r['analysis_latency_ms'] / 1000.0 for r in results_a]
    fixed_ret = [r['retrieval_latency_ms'] / 1000.0 for r in results_a]

    stats_sel_a = calculate_stats(sel_lat_a)
    stats_sel_b = calculate_stats(sel_lat_b)
    stats_tot_a = calculate_stats(tot_lat_a)
    stats_tot_b = calculate_stats(tot_lat_b)
    stats_ana = calculate_stats(fixed_ana)
    stats_ret = calculate_stats(fixed_ret)

    # Gemini API requests (Workflow-level vs HTTP retry)
    gemini_reqs_a = sum(sum(1 for c in r.get('provider_calls', []) if c.get('provider') == 'gemini') for r in results_a)
    gemini_reqs_b = sum(sum(1 for c in r.get('provider_calls', []) if c.get('provider') == 'gemini') for r in results_b)

    from telemetry_summary import summarize_calls
    usage_a = summarize_calls(results_a)
    usage_b = summarize_calls(results_b)

    # Counts
    repairs_a = sum(1 for r in results_a if r['repair_performed'])
    repairs_b = sum(1 for r in results_b if r['repair_performed'])
    fallbacks_a = sum(1 for r in results_a if r['fallback_source'])
    fallbacks_b = sum(1 for r in results_b if r['fallback_source'])
    partials_a = sum(1 for r in results_a if r['partial_answer'])
    partials_b = sum(1 for r in results_b if r['partial_answer'])

    def _extract_agreement(case_obj: dict | None) -> str:
        if not isinstance(case_obj, dict):
            return 'unscored'
        comp = case_obj.get('comparison')
        if isinstance(comp, dict):
            return comp.get('agreement', 'unscored') or 'unscored'
        return 'unscored'

    # V15 agreement counts
    v15_dist_a = Counter(_extract_agreement(v15_cases_a.get(r['id'])) for r in results_a)
    v15_dist_b = Counter(_extract_agreement(v15_cases_b.get(r['id'])) for r in results_b)

    # Label movements: separate unscored so it is NEVER ranked below low
    movements = {'upgraded': [], 'downgraded': [], 'same': [], 'unscored_or_incomparable': []}
    order_map = {'high': 3, 'partial': 2, 'low': 1}
    for qid in common_ids:
        la = _extract_agreement(v15_cases_a.get(qid))
        lb = _extract_agreement(v15_cases_b.get(qid))
        if la == 'unscored' or lb == 'unscored':
            ra_err = (v15_cases_a.get(qid) or {}).get('judge_errors', [])
            rb_err = (v15_cases_b.get(qid) or {}).get('judge_errors', [])
            movements['unscored_or_incomparable'].append({
                'id': qid,
                'label_a': la,
                'label_b': lb,
                'judge_errors_a': ra_err if la == 'unscored' else None,
                'judge_errors_b': rb_err if lb == 'unscored' else None,
            })
        elif order_map.get(lb, 0) > order_map.get(la, 0):
            movements['upgraded'].append((qid, la, lb))
        elif order_map.get(lb, 0) < order_map.get(la, 0):
            movements['downgraded'].append((qid, la, lb))
        else:
            movements['same'].append((qid, la, lb))

    # Detailed per-question source analysis
    per_question_audit = []
    for qid in common_ids:
        ra = res_a_by_id[qid]
        rb = res_b_by_id[qid]
        snap = by_snap.get(qid, {})
        cand_by_id = {c['id']: c for c in snap.get('candidates', [])}

        ids_a = set(ra['final_evidence_candidate_ids'])
        ids_b = set(rb['final_evidence_candidate_ids'])
        common = sorted(ids_a & ids_b)
        qwen_only = sorted(ids_a - ids_b)
        gemini_only = sorted(ids_b - ids_a)

        diff_excerpts_qwen = [{
            'id': cid,
            'doc': cand_by_id[cid].get('document'),
            'heading': cand_by_id[cid].get('heading'),
            'excerpt': cand_by_id[cid]['text'][:240],
        } for cid in qwen_only if cid in cand_by_id]

        diff_excerpts_gemini = [{
            'id': cid,
            'doc': cand_by_id[cid].get('document'),
            'heading': cand_by_id[cid].get('heading'),
            'excerpt': cand_by_id[cid]['text'][:240],
        } for cid in gemini_only if cid in cand_by_id]

        la = _extract_agreement(v15_cases_a.get(qid))
        lb = _extract_agreement(v15_cases_b.get(qid))

        per_question_audit.append({
            'id': qid,
            'question': ra['question'],
            'total_candidates': len(snap.get('candidates', [])),
            'qwen_raw_ids': ra.get('raw_model_selected_ids', []),
            'qwen_selected_ids': sorted(ids_a),
            'gemini_raw_ids': rb.get('raw_model_selected_ids', []),
            'gemini_selected_ids': sorted(ids_b),
            'common_ids': common,
            'qwen_only_ids': qwen_only,
            'gemini_only_ids': gemini_only,
            'qwen_only_excerpts': diff_excerpts_qwen,
            'gemini_only_excerpts': diff_excerpts_gemini,
            'qwen_selection_ms': ra['selection_ms'],
            'gemini_selection_ms': rb['selection_ms'],
            'qwen_total_ms': ra['total_selection_to_final_ms'],
            'gemini_total_ms': rb['total_selection_to_final_ms'],
            'qwen_repaired': ra['repair_performed'],
            'gemini_repaired': rb['repair_performed'],
            'qwen_partial': ra['partial_answer'],
            'gemini_partial': rb['partial_answer'],
            'qwen_fallback': ra['fallback_source'],
            'gemini_fallback': rb['fallback_source'],
            'qwen_v15': la,
            'gemini_v15': lb,
        })

    # Summary JSON
    summary_data = {
        'run_name': run_name,
        'created_at_utc': datetime.now(timezone.utc).isoformat(),
        'git_commit': get_git_commit(),
        'run_identity': run_identity,
        'snapshot_sha256': snapshot_data.get('snapshot_sha256'),
        'legal_schema': settings.chatbot_legal_schema,
        'graph_schema': settings.chatbot_graph_schema,
        'listing_schema': settings.chatbot_listing_schema,
        'models': {
            'qwen_selector': settings.ollama_model,
            'gemini_selector': settings.chatbot_legal_selection_model or settings.gemini_model,
            'writer': settings.chatbot_answer_synthesis_model or settings.gemini_model,
            'verifier': settings.gemini_model,
            'judge_v15': settings.ollama_model,
        },
        'counts': {
            'total_questions': len(common_ids),
            'branch_a_completed': len(results_a),
            'branch_b_completed': len(results_b),
        },
        'fixed_timing_seconds': {
            'question_analysis': stats_ana,
            'retrieval': stats_ret,
        },
        'selection_latency_seconds': {
            'branch_a_qwen': stats_sel_a,
            'branch_b_gemini': stats_sel_b,
        },
        'replay_selection_to_final_seconds': {
            'branch_a_qwen': stats_tot_a,
            'branch_b_gemini': stats_tot_b,
        },
        'gemini_requests': {
            'branch_a_qwen': gemini_reqs_a,
            'branch_b_gemini': gemini_reqs_b,
        },
        'token_usage': {
            'branch_a_qwen': usage_a,
            'branch_b_gemini': usage_b,
        },
        'workflow_events': {
            'branch_a_repairs': repairs_a,
            'branch_b_repairs': repairs_b,
            'branch_a_fallbacks': fallbacks_a,
            'branch_b_fallbacks': fallbacks_b,
            'branch_a_partial_answers': partials_a,
            'branch_b_partial_answers': partials_b,
        },
        'v15_distribution': {
            'branch_a_qwen': dict(v15_dist_a),
            'branch_b_gemini': dict(v15_dist_b),
        },
        'label_movements': movements,
        'per_question_audit': per_question_audit,
    }

    save_atomic_checkpoint(json_out, summary_data)

    # Markdown Report
    md = []
    md.append(f'# Báo cáo Phép thử Đối chứng: Qwen Selector vs Gemini Selector ({run_name})')
    md.append('')
    md.append('**Mục tiêu:** Xác định việc thay Qwen bằng Gemini ở **RIÊNG** bước chọn nguồn có cải thiện hệ thống hay không.')
    md.append('')
    md.append('## 1. Bằng chứng Phép thử Hợp lệ & Khóa Identity')
    md.append(f'- **Git Commit:** `{get_git_commit()}`')
    if run_identity:
        md.append(f'- **Run Identity SHA256:** `{run_identity.get("identity_sha256")}`')
        md.append(f'- **Code Digest SHA256:** `{run_identity.get("code_digest")}`')
    md.append(f'- **Snapshot SHA256:** `{snapshot_data.get("snapshot_sha256")}`')
    md.append(f'- **Corpus Schema:** `{settings.chatbot_legal_schema}` (Graph: `{settings.chatbot_graph_schema}`, Housing: `{settings.chatbot_listing_schema}`)')
    md.append('- **Biến độc lập duy nhất:** Model/provider chọn nguồn (`Ollama Qwen` vs `Gemini Proxy`).')
    md.append('- **Điều kiện cố định tuyệt đối:** Cùng snapshot 36 câu (QuestionPlan + candidate chunks nguyên vẹn); cùng Gemini Writer (riêng); cùng Gemini Verifier (riêng); cùng giới hạn sửa tối đa 1 lần; cùng judge V15 cục bộ Qwen.')
    md.append('- **Không dùng combined mode; không sửa prompt viết, prompt kiểm chứng hay rubric chấm.**')
    md.append('')
    md.append('## 2. Bảng So sánh Tổng hợp')
    md.append('')
    md.append('| Chỉ số | Nhánh A (Qwen chọn nguồn) | Nhánh B (Gemini chọn nguồn) | Chênh lệch (B - A) |')
    md.append('|---|---:|---:|---:|')
    md.append(f'| Số câu hoàn thành / lỗi | {len(results_a)} / 0 | {len(results_b)} / 0 | 0 |')
    md.append(f'| Thời gian chọn nguồn (Trung vị) | {stats_sel_a["median"]}s | {stats_sel_b["median"]}s | {round(stats_sel_b["median"] - stats_sel_a["median"], 2)}s |')
    md.append(f'| Thời gian chọn nguồn (P95) | {stats_sel_a["p95"]}s | {stats_sel_b["p95"]}s | {round(stats_sel_b["p95"] - stats_sel_a["p95"], 2)}s |')
    md.append(f'| Replay từ chọn nguồn đến trả lời (Trung vị) | {stats_tot_a["median"]}s | {stats_tot_b["median"]}s | {round(stats_tot_b["median"] - stats_tot_a["median"], 2)}s |')
    md.append(f'| Replay từ chọn nguồn đến trả lời (P95) | {stats_tot_a["p95"]}s | {stats_tot_b["p95"]}s | {round(stats_tot_b["p95"] - stats_tot_a["p95"], 2)}s |')
    md.append(f'| Tổng request Gemini cấp workflow | {gemini_reqs_a} | {gemini_reqs_b} | {gemini_reqs_b - gemini_reqs_a} |')
    md.append(f'| Số câu phải sửa nội dung (1 lần) | {repairs_a} | {repairs_b} | {repairs_b - repairs_a} |')
    md.append(f'| Số câu fallback nguồn | {fallbacks_a} | {fallbacks_b} | {fallbacks_b - fallbacks_a} |')
    md.append(f'| Số câu trả lời một phần (partial) | {partials_a} | {partials_b} | {partials_b - partials_a} |')
    md.append(f'| V15 High / Partial / Low / Unscored | {v15_dist_a.get("high",0)} / {v15_dist_a.get("partial",0)} / {v15_dist_a.get("low",0)} / {v15_dist_a.get("unscored",0)} | {v15_dist_b.get("high",0)} / {v15_dist_b.get("partial",0)} / {v15_dist_b.get("low",0)} / {v15_dist_b.get("unscored",0)} | High: {v15_dist_b.get("high",0)-v15_dist_a.get("high",0)}, Low: {v15_dist_b.get("low",0)-v15_dist_a.get("low",0)} |')
    md.append('')
    md.append('> **Lưu ý về định nghĩa thời gian và token:**')
    md.append('> - *Replay từ chọn nguồn đến trả lời:* Đo riêng từ lúc bắt đầu chọn nguồn đến khi hoàn thành sinh/kiểm chứng câu trả lời cuối. Không bao gồm phân tích câu hỏi và truy xuất vector/BM25 đã được lưu cố định trong snapshot.')
    md.append(f'> - *Thời gian phân tích/truy xuất cố định trong snapshot:* Phân tích câu hỏi trung vị {stats_ana["median"]}s (P95 {stats_ana["p95"]}s); Truy xuất E5+BM25 trung vị {stats_ret["median"]}s (P95 {stats_ret["p95"]}s).')
    md.append(f'> - *Token usage:* Nhánh A: `{usage_a["note"]}`; Nhánh B: `{usage_b["note"]}`.')
    md.append('')
    md.append('## 3. Biến động Nhãn V15')
    md.append(f'- **Giữ nguyên nhãn:** {len(movements["same"])} câu')
    md.append(f'- **Tăng nhãn:** {len(movements["upgraded"])} câu ({[f"Q{q} ({a}->{b})" for q,a,b in movements["upgraded"]]})')
    md.append(f'- **Giảm nhãn:** {len(movements["downgraded"])} câu ({[f"Q{q} ({a}->{b})" for q,a,b in movements["downgraded"]]})')
    if movements['unscored_or_incomparable']:
        md.append(f'- **Unscored / Không so sánh được:** {len(movements["unscored_or_incomparable"])} câu ({movements["unscored_or_incomparable"]})')
    md.append('')
    md.append('## 4. Chi tiết Từng Câu: So Sánh Nguồn Được Chọn và V15')
    md.append('')
    md.append('| ID | Qwen chọn | Gemini chọn | Điểm chung | Khác biệt | Tác động V15 (A -> B) | Trạng thái B |')
    md.append('|---:|---|---|---|---|:---:|---|')
    for item in per_question_audit:
        qwen_ids = str(item['qwen_selected_ids'])
        gemini_ids = str(item['gemini_selected_ids'])
        common_ids_str = str(item['common_ids'])
        diff = []
        if item['qwen_only_ids']:
            diff.append(f'Qwen-only: {item["qwen_only_ids"]}')
        if item['gemini_only_ids']:
            diff.append(f'Gemini-only: {item["gemini_only_ids"]}')
        diff_str = '; '.join(diff) if diff else 'Trùng 100%'
        v15_str = f'{item["qwen_v15"]} -> {item["gemini_v15"]}'
        status_b = 'OK'
        if item['gemini_fallback']:
            status_b = 'Fallback'
        elif item['gemini_repaired']:
            status_b = 'Repaired'
        md.append(f'| {item["id"]} | {qwen_ids} | {gemini_ids} | {common_ids_str} | {diff_str} | {v15_str} | {status_b} |')

    md.append('')
    md.append('## 5. Bằng chứng Trích đoạn Cụ thể cho Các Câu Khác Biệt Nguồn')
    for item in per_question_audit:
        if item['qwen_only_ids'] or item['gemini_only_ids']:
            md.append(f'### Câu {item["id"]}: {item["question"]}')
            if item['qwen_only_excerpts']:
                md.append('**Qwen chọn nhưng Gemini bỏ:**')
                for ex in item['qwen_only_excerpts']:
                    md.append(f'- `Candidate ID {ex["id"]}` [{ex["doc"]} - {ex["heading"]}]: "{ex["excerpt"]}..."')
            if item['gemini_only_excerpts']:
                md.append('**Gemini chọn nhưng Qwen bỏ:**')
                for ex in item['gemini_only_excerpts']:
                    md.append(f'- `Candidate ID {ex["id"]}` [{ex["doc"]} - {ex["heading"]}]: "{ex["excerpt"]}..."')
            md.append(f'- **Nhãn V15:** Qwen `{item["qwen_v15"]}` vs Gemini `{item["gemini_v15"]}`')
            md.append('')

    md_path_tmp = md_out.with_suffix('.tmp')
    md_path_tmp.write_text('\n'.join(md), encoding='utf-8')
    md_path_tmp.replace(md_out)
    print(f'[REPORT] Saved markdown comparison report to {md_out}', flush=True)
    print(f'[REPORT] Saved JSON summary to {json_out}', flush=True)


def main():
    def _default_p(docker_p, host_p):
        return Path(docker_p) if Path(docker_p).exists() else Path(host_p)
    parser = argparse.ArgumentParser()
    parser.add_argument('--questions', type=Path, default=_default_p('/workspace/docs/CHATBOT_QUESTION_BANK.md', 'docs/CHATBOT_QUESTION_BANK.md'))
    parser.add_argument('--ids', type=int, nargs='+', default=DEFAULT_IDS)
    parser.add_argument('--pilot', action='store_true', help='Run pilot questions')
    parser.add_argument('--snapshot-file', type=Path, default=_default_p('/workspace/eval/reports/legal_controlled_snapshot_36_v1_20261006.json', 'eval/reports/legal_controlled_snapshot_36_v1_20261006.json'))
    parser.add_argument('--run-name', type=str, default='legal_selector_ab_36_v1_20261006')
    parser.add_argument('--output-dir', type=Path, default=_default_p('/workspace/eval/reports', 'eval/reports'))
    parser.add_argument('--skip-v15', action='store_true', help='Skip V15 judge evaluation')
    args = parser.parse_args()

    if args.pilot:
        args.ids = PILOT_IDS
        if args.run_name == 'legal_selector_ab_36_v1_20261006':
            args.run_name = 'legal_selector_ab_pilot_v1_20261006'

    all_cases = bank.load_questions(args.questions)
    cases = [c for c in all_cases if c['id'] in args.ids]
    if len(cases) != len(set(args.ids)):
        raise ValueError(f'Requested IDs missing from question bank: {set(args.ids) - {c["id"] for c in cases}}')

    legal_only_boundary.assert_legal_cases(cases)

    engine = create_engine(settings.database_url)
    with engine.connect() as conn:
        rel = conn.execute(text(f'SELECT count(*) FROM {settings.chatbot_graph_schema}.release')).scalar()
        leg_cnt = conn.execute(text(f'SELECT count(*) FROM {settings.chatbot_legal_schema}.legal_chunks')).scalar()
        if not rel or not leg_cnt:
            raise ValueError('Corpus schemas empty or missing')
        print(f'[DB] Verified corpus schemas: legal chunks = {leg_cnt}, graph release = {rel}', flush=True)

    # Generate or load input snapshot (always for all 36 legal questions to ensure constant SHA256)
    snapshot_cases = [c for c in all_cases if c['id'] in DEFAULT_IDS]
    snapshot_data, snapshot_sha = load_or_create_snapshot(engine, snapshot_cases, args.snapshot_file)

    run_identity = compute_run_identity(cases, snapshot_sha, leg_cnt, rel)

    # Run experiment
    run_experiment(
        engine,
        cases,
        snapshot_data,
        args.run_name,
        args.output_dir,
        run_identity=run_identity,
        skip_v15=args.skip_v15,
    )


if __name__ == '__main__':
    main()

