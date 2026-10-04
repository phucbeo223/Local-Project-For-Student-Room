import os
import pytest
from sqlalchemy import create_engine, text
from app.room_service.chatbot.graph_retrieval import GraphChatRepository, graph_schema, location_entities
from app.room_service.chatbot.repo import ChatRepository
from app.room_service.chatbot.schemas import ChatFilters
from app.room_service.chatbot.providers import _grounded_prompt


def test_graph_location_is_one_constraint_and_source_namespace_survives_response():
    from app.room_service.chatbot.providers import DeterministicFakeEmbedder, GroundedTemplateGenerator
    from app.room_service.chatbot.service import ChatService
    from app.room_service.chatbot.schemas import ChatAskRequest
    class Repo:
        graph_enabled = True
        listing_schema = 'housing_graph_v1'
        def retrieve(self, *args, **kwargs):
            return [dict(id=i, rank=i, title='Phòng Xuân Khánh', source='chotot', similarity_score=.79,
                _graph_trace={'stage': 'graph_retrieval', 'seed_entities': ['location:xuan_khanh', 'location:street_3_2']})
                for i in (1, 2)]
    result = ChatService(Repo(), DeterministicFakeEmbedder(), GroundedTemplateGenerator()).ask(
        ChatAskRequest(message='Có phòng nào gần đường 3/2 hoặc khu Xuân Khánh không?'))
    assert not result.no_answer
    assert result.confidence == .6762
    assert result.listings[0].corpus_schema == 'housing_graph_v1'
    assert result.retrieval_mode == 'graph_hybrid'
    assert result.agent_trace[0]['stage'] == 'graph_retrieval'


@pytest.mark.parametrize('value', ['public', 'graph_v1;DROP TABLE users', 'graph_../housing', 'Graph_v1'])
def test_graph_identifiers_reject_sql_injection(value):
    with pytest.raises(ValueError):
        graph_schema(value)


def test_explicit_location_entities_have_no_district_guess():
    assert location_entities('Quận Ninh Kiều') == []
    assert location_entities('Đường 3/20') == []
    assert location_entities('Gần đường 3/2 hoặc Xuân Khánh') == ['location:xuan_khanh', 'location:street_3_2']


def test_listing_schema_rejects_unsafe_identifier():
    with pytest.raises(ValueError):
        ChatRepository(None, listing_schema='housing_v2;DROP SCHEMA public')


def test_graph_context_retains_approximate_distance_method():
    prompt = _grounded_prompt('gần trường', [{'id': 123, 'rank': 1, 'graph_facts': [
        {'relation': 'distance_to', 'target': 'campus:ctu_khu_ii',
         'evidence': {'field': 'distance_to_ctu', 'method': 'approximate_haversine'}}]}])
    assert 'approximate_haversine' in prompt
    assert 'route_time_campus_minutes":null' in prompt


@pytest.fixture
def graph_repo():
    if os.getenv('RUN_GRAPH_DB_TESTS') != '1':
        pytest.skip('Explicit opt-in to read-only graph release integration checks')
    from app.config import settings
    engine = create_engine(settings.database_url)
    yield GraphChatRepository(engine, 'legal_v3_20261004', 'housing_graph_v1')
    engine.dispose()


def test_location_walk_cannot_return_wrong_neighborhood_or_over_budget(graph_repo):
    rows = graph_repo.retrieve('Tìm phòng ở Xuân Khánh dưới 2 triệu',
                               ChatFilters(listing_type='phong_tro', max_price=2_000_000), None)
    assert rows
    for row in rows:
        assert row['price'] <= 2_000_000
        assert any(fact['target'] == 'location:xuan_khanh' for fact in row['graph_facts'])
        assert row['_graph_trace']['traversed_edges'] > 0


def test_graph_amenity_evidence_is_grounded_and_missing_capacity_stays_unknown(graph_repo):
    rows = graph_repo.retrieve('phòng có nhà vệ sinh riêng và giờ giấc tự do',
        ChatFilters(listing_type='phong_tro', amenities=['private_bathroom', 'flexible_hours']), None)
    assert rows
    for row in rows:
        for key in ['private_bathroom', 'flexible_hours']:
            assert row['parsed_amenities'][key] is True
            assert any(fact['target'] == 'amenity:' + key and fact['evidence']['value'] is True for fact in row['graph_facts'])
        assert all(fact['relation'] != 'capacity' for fact in row['graph_facts'])


def test_legal_walk_is_bounded_and_never_attaches_another_law_as_same_source(graph_repo):
    with graph_repo.engine.connect() as conn:
        seed = conn.execute(text("SELECT n.document_id,n.provision_id,n.label FROM graph_rag_v1.edges e "
            "JOIN graph_rag_v1.nodes n ON n.id=e.source WHERE e.relation='cites' LIMIT 1")).mappings().one()
    rows = graph_repo.retrieve_legal(seed['label'], None)
    assert rows
    assert all(row['_graph_trace']['max_hops'] == 2 for row in rows if row.get('_graph_trace'))
    with graph_repo.engine.connect() as conn:
        for row in rows:
            for provision in row.get('graph_provision_ids', []):
                assert conn.execute(text('SELECT count(*) FROM legal_v3_20261004.legal_chunks WHERE document_id=:doc AND provision_id=:pid'),
                    {'doc': row['document_id'], 'pid': provision}).scalar_one() > 0


def test_graph_release_refuses_mismatched_source_schema(graph_repo):
    with pytest.raises(ValueError, match='does not match'):
        GraphChatRepository(graph_repo.engine, 'legal_v3_20261004', 'housing_v2')
