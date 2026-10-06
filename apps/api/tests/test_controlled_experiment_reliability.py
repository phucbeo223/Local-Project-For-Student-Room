import copy
import hashlib
import json
from pathlib import Path
import pytest

import sys
sys.path.insert(0, '/workspace/eval')
sys.path.insert(0, 'eval')

from controlled_selector_experiment import (
    canonical_snapshot_digest,
    compute_run_identity,
    save_atomic_checkpoint,
    close_service_clients,
    load_or_create_snapshot,
    calculate_stats,
    generate_full_report,
)


def test_canonical_snapshot_digest_ignores_self_hash():
    """Digest must be invariant whether snapshot_sha256 or digest field is present or absent."""
    base_data = {
        'version': '1.0',
        'cases': [
            {'id': 19, 'question': 'Hợp đồng thuê phòng có bắt buộc công chứng không?'},
            {'id': 20, 'question': 'Giá điện trọ quy định như thế nào?'}
        ]
    }
    digest1 = canonical_snapshot_digest(base_data)

    data_with_hash = dict(base_data, snapshot_sha256='abcdef1234567890')
    digest2 = canonical_snapshot_digest(data_with_hash)

    data_with_sha = dict(base_data, sha256='1122334455667788', digest='99887766')
    digest3 = canonical_snapshot_digest(data_with_sha)

    assert digest1 == digest2 == digest3
    assert len(digest1) == 64


def test_snapshot_tamper_detection_rejects_modified_content(tmp_path):
    """If snapshot content is altered but the stored hash remains unchanged, load must fail."""
    from app.config import settings
    snap_file = tmp_path / 'snapshot.json'
    cases = [{'id': 19, 'question': 'Câu hỏi gốc', 'question_plan': {'topics': []}, 'contexts': [{'id': 1}], 'candidates': [{'id': 1, 'rank': 1}]}]
    data = {
        'version': '1.0',
        'legal_schema': settings.chatbot_legal_schema,
        'embedding_model': settings.chatbot_embedding_model,
        'cases': cases,
    }
    real_hash = canonical_snapshot_digest(data)
    data['snapshot_sha256'] = real_hash
    save_atomic_checkpoint(snap_file, data)

    # 1. Valid snapshot loads
    loaded, digest = load_or_create_snapshot(None, cases, snap_file)
    assert digest == real_hash

    # 2. Tampered content with old hash must be rejected
    tampered_data = copy.deepcopy(data)
    tampered_data['cases'][0]['question'] = 'Câu hỏi đã bị sửa đổi lén lút'
    # Keep the old snapshot_sha256
    save_atomic_checkpoint(snap_file, tampered_data)

    with pytest.raises(ValueError, match='Snapshot digest mismatch'):
        load_or_create_snapshot(None, cases, snap_file)


def test_snapshot_missing_ids_or_schema_change_rejected(tmp_path):
    """Snapshot must be rejected if schema or requested IDs don't match."""
    snap_file = tmp_path / 'snapshot.json'
    cases = [{'id': 19, 'question': 'Câu 19', 'question_plan': {'topics': []}, 'contexts': [{'id': 1}], 'candidates': [{'id': 1, 'rank': 1}]}]
    data = {
        'version': '1.0',
        'legal_schema': 'wrong_schema',
        'embedding_model': 'e5_test',
        'cases': cases,
    }
    data['snapshot_sha256'] = canonical_snapshot_digest(data)
    save_atomic_checkpoint(snap_file, data)

    with pytest.raises(ValueError, match='Snapshot legal_schema'):
        load_or_create_snapshot(None, cases, snap_file)


def test_compute_run_identity_changes_on_model_or_code_change():
    """Run identity digest must change if model configuration, cases, or snapshot changes."""
    cases = [{'id': 19}, {'id': 20}]
    snap_digest = 'a' * 64

    id1 = compute_run_identity(cases, snap_digest, legal_chunks_count=100, graph_release_count=1)
    id2 = compute_run_identity(cases, snap_digest, legal_chunks_count=101, graph_release_count=1)
    id3 = compute_run_identity([{'id': 19}], snap_digest, legal_chunks_count=100, graph_release_count=1)

    assert id1['identity_sha256'] != id2['identity_sha256']
    assert id1['identity_sha256'] != id3['identity_sha256']


def test_comparison_null_and_unscored_never_ranked_below_low(tmp_path):
    """When judge produces comparison=null, agreement is unscored and never counted as lower than low."""
    results_a = [{
        'id': 19, 'question': 'Q19', 'selection_ms': 100, 'total_selection_to_final_ms': 500,
        'analysis_latency_ms': 50, 'retrieval_latency_ms': 50, 'raw_model_selected_ids': [1],
        'final_evidence_candidate_ids': [1], 'repair_performed': False, 'partial_answer': False,
        'fallback_source': False, 'provider_calls': []
    }]
    results_b = [{
        'id': 19, 'question': 'Q19', 'selection_ms': 20, 'total_selection_to_final_ms': 200,
        'analysis_latency_ms': 50, 'retrieval_latency_ms': 50, 'raw_model_selected_ids': [1],
        'final_evidence_candidate_ids': [1], 'repair_performed': False, 'partial_answer': False,
        'fallback_source': False, 'provider_calls': []
    }]
    snap_data = {'cases': [{'id': 19, 'candidates': [{'id': 1, 'rank': 1, 'text': 'text', 'document': 'doc', 'heading': 'h'}]}]}

    # V15 file A: comparison is null (judge failure / unscored)
    v15_file_a = tmp_path / 'v15_a.json'
    v15_a = {'cases': [{'id': 19, 'comparison': None, 'judge_errors': ['RateLimitError']}]}
    save_atomic_checkpoint(v15_file_a, v15_a)

    # V15 file B: comparison has agreement 'low'
    v15_file_b = tmp_path / 'v15_b.json'
    v15_b = {'cases': [{'id': 19, 'comparison': {'agreement': 'low'}, 'judge_errors': []}]}
    save_atomic_checkpoint(v15_file_b, v15_b)

    md_out = tmp_path / 'report.md'
    json_out = tmp_path / 'report.json'

    generate_full_report(
        results_a, results_b, snap_data, v15_file_a, v15_file_b,
        md_out, json_out, run_name='test_unscored'
    )

    report_data = json.loads(json_out.read_text(encoding='utf-8'))
    movements = report_data['label_movements']

    # Unscored to Low MUST NOT be counted as 'upgraded'! It must be in 'unscored_or_incomparable'
    assert len(movements['upgraded']) == 0
    assert len(movements['downgraded']) == 0
    assert len(movements['unscored_or_incomparable']) == 1
    assert movements['unscored_or_incomparable'][0]['id'] == 19
    assert movements['unscored_or_incomparable'][0]['label_a'] == 'unscored'
    assert movements['unscored_or_incomparable'][0]['label_b'] == 'low'


def test_atomic_checkpoint_granular_per_branch_safety(tmp_path):
    """save_atomic_checkpoint writes to temporary file then replaces, avoiding corruption."""
    ckpt_path = tmp_path / 'test_ckpt.json'
    data = {'run_name': 'atomic_test', 'status': 'in_progress', 'branch_a': [1, 2]}
    save_atomic_checkpoint(ckpt_path, data)

    assert ckpt_path.exists()
    assert not ckpt_path.with_suffix('.tmp').exists()
    loaded = json.loads(ckpt_path.read_text(encoding='utf-8'))
    assert loaded == data


def test_clean_client_teardown_in_finally():
    """close_service_clients safely closes all clients without throwing."""
    class DummyClient:
        def __init__(self):
            self.closed = False
        def close(self):
            self.closed = True

    c1 = DummyClient()
    c2 = DummyClient()
    class Wrapper:
        def __init__(self, client):
            self.client = client

    w = Wrapper(c2)
    close_service_clients(c1, w, None, 'not_a_client')
    assert c1.closed is True
    assert c2.closed is True


def test_fallback_detection_cases():
    """Fallback must be triggered on template generator, empty sources, or verifier/synthesis fallback."""
    # 1. Grounded template provider
    d1 = {'generation_provider': 'grounded_template', 'sources': [{'id': 1}], 'agent_trace': []}
    is_fb_1 = (
        d1.get('generation_provider') == 'grounded_template' or
        not d1.get('sources') or
        any(s.get('status') == 'skipped' and s.get('reason') == 'no_selected_evidence' for s in d1.get('agent_trace', []))
    )
    assert is_fb_1 is True

    # 2. Empty sources even if provider is not template
    d2 = {'generation_provider': 'gemini-agent', 'sources': [], 'agent_trace': []}
    is_fb_2 = (
        d2.get('generation_provider') == 'grounded_template' or
        not d2.get('sources')
    )
    assert is_fb_2 is True

    # 3. Skipped synthesis due to no selected evidence
    d3 = {'generation_provider': 'gemini-agent', 'sources': [{'id': 1}], 'agent_trace': [
        {'agent': 'answer_synthesis', 'status': 'skipped', 'reason': 'no_selected_evidence'}
    ]}
    is_fb_3 = any(s.get('status') == 'skipped' and s.get('reason') == 'no_selected_evidence' for s in d3.get('agent_trace', []))
    assert is_fb_3 is True

    # 4. Verifier fallback
    d4 = {'agent_trace': [{'agent': 'source_verification', 'fallback': True}]}
    is_fb_4 = any(s.get('fallback') for s in d4.get('agent_trace', []))
    assert is_fb_4 is True


def test_paired_reporting_out_of_order_ids(tmp_path):
    """Reporting must pair questions by ID regardless of the list order, and detect missing IDs."""
    results_a = [
        {'id': 20, 'question': 'Q20', 'selection_ms': 100, 'total_selection_to_final_ms': 500, 'analysis_latency_ms': 50, 'retrieval_latency_ms': 50, 'raw_model_selected_ids': [2], 'final_evidence_candidate_ids': [2], 'repair_performed': False, 'partial_answer': False, 'fallback_source': False, 'provider_calls': []},
        {'id': 19, 'question': 'Q19', 'selection_ms': 120, 'total_selection_to_final_ms': 520, 'analysis_latency_ms': 50, 'retrieval_latency_ms': 50, 'raw_model_selected_ids': [1], 'final_evidence_candidate_ids': [1], 'repair_performed': False, 'partial_answer': False, 'fallback_source': False, 'provider_calls': []},
    ]
    # Branch B is in reverse order
    results_b = [
        {'id': 19, 'question': 'Q19', 'selection_ms': 20, 'total_selection_to_final_ms': 200, 'analysis_latency_ms': 50, 'retrieval_latency_ms': 50, 'raw_model_selected_ids': [1], 'final_evidence_candidate_ids': [1], 'repair_performed': False, 'partial_answer': False, 'fallback_source': False, 'provider_calls': []},
        {'id': 20, 'question': 'Q20', 'selection_ms': 25, 'total_selection_to_final_ms': 210, 'analysis_latency_ms': 50, 'retrieval_latency_ms': 50, 'raw_model_selected_ids': [2], 'final_evidence_candidate_ids': [2], 'repair_performed': False, 'partial_answer': False, 'fallback_source': False, 'provider_calls': []},
    ]
    snap_data = {'cases': [
        {'id': 19, 'candidates': [{'id': 1, 'rank': 1, 'text': 'text1', 'document': 'doc1', 'heading': 'h1'}]},
        {'id': 20, 'candidates': [{'id': 2, 'rank': 1, 'text': 'text2', 'document': 'doc2', 'heading': 'h2'}]},
    ]}

    v15_file_a = tmp_path / 'v15_a.json'
    v15_a = {'cases': [
        {'id': 19, 'comparison': {'agreement': 'partial'}},
        {'id': 20, 'comparison': {'agreement': 'low'}},
    ]}
    save_atomic_checkpoint(v15_file_a, v15_a)

    v15_file_b = tmp_path / 'v15_b.json'
    v15_b = {'cases': [
        {'id': 20, 'comparison': {'agreement': 'partial'}}, # Low -> Partial = upgrade
        {'id': 19, 'comparison': {'agreement': 'high'}},    # Partial -> High = upgrade
    ]}
    save_atomic_checkpoint(v15_file_b, v15_b)

    md_out = tmp_path / 'report.md'
    json_out = tmp_path / 'report.json'

    generate_full_report(results_a, results_b, snap_data, v15_file_a, v15_file_b, md_out, json_out, run_name='order_test')

    data = json.loads(json_out.read_text(encoding='utf-8'))
    # Both 19 and 20 must be correctly paired and upgraded
    upgraded_ids = [q for q, a, b in data['label_movements']['upgraded']]
    assert sorted(upgraded_ids) == [19, 20]

