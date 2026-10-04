"""Build a local, atomic graph release from verified existing source corpora.

Only JSONL data is consumed from the supplied package, never its executables.
The release has no inferred room capacity, occupancy, vacancy or travel times.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'apps/api'))
from sqlalchemy import create_engine, text
from app.config import settings
from app.room_service.chatbot.graph_retrieval import location_entities
from import_housing_catalog import snapshot, prepare

GRAPH = 'graph_rag_v1'
HOUSING = 'housing_graph_v1'
SOURCE = 'housing_v2'
VERSION = 'typed-local-graph-1.2'


def main():
    global GRAPH, HOUSING, SOURCE
    parser = argparse.ArgumentParser()
    parser.add_argument('--catalog-dir', type=Path, required=True)
    parser.add_argument('--report', type=Path, required=True)
    parser.add_argument('--rebuild', action='store_true', help='Atomically rebuild this isolated graph, retaining verified housing rows')
    parser.add_argument('--graph-schema', default=GRAPH)
    parser.add_argument('--housing-schema', default=HOUSING)
    parser.add_argument('--source-schema', default=SOURCE)
    args = parser.parse_args()
    from app.room_service.chatbot.graph_retrieval import graph_schema
    GRAPH = graph_schema(args.graph_schema)
    if not all(re.fullmatch(r'housing_[a-z0-9_]{1,48}',s) for s in (args.housing_schema,args.source_schema)):
        raise ValueError('Invalid isolated housing namespace')
    HOUSING, SOURCE = args.housing_schema, args.source_schema
    catalog = args.catalog_dir / 'CATALOG.jsonl'
    digest = hashlib.sha256(catalog.read_bytes()).hexdigest()
    manifest = json.loads((args.catalog_dir.parent / 'SOURCE_MANIFEST.json').read_text(encoding='utf-8'))
    if digest != manifest['files']['CATALOG.jsonl']:
        raise ValueError('Catalog integrity check failed')
    records = [json.loads(line) for line in catalog.read_text(encoding='utf-8').splitlines()]
    if len(records) != 789 or len({record['id'] for record in records}) != 789:
        raise ValueError('Unexpected catalog size or duplicate IDs')
    normalized = {record['id']: prepare(record) for record in records}
    engine = create_engine(settings.database_url)
    legal = settings.chatbot_legal_schema
    if legal == 'public':
        raise ValueError('Graph indexing requires a structured legal corpus')
    with engine.begin() as conn:
        # Importer and graph writers cannot run concurrently.
        conn.execute(text("SELECT pg_advisory_xact_lock(hashtext('graph-rag-release-v1'))"))
        before = snapshot(conn)
        source_hash = conn.execute(text(f'SELECT catalog_sha256 FROM {SOURCE}.release WHERE id=1')).scalar_one()
        if source_hash != digest:
            raise ValueError('Imported housing source differs from supplied JSONL')
        source_rows = [dict(row) for row in conn.execute(text(
            f'SELECT id,row_sha256 FROM {SOURCE}.catalog_records ORDER BY id')).mappings()]
        if {row['id']: row['row_sha256'] for row in source_rows} != {key: value['row_sha'] for key, value in normalized.items()}:
            raise ValueError('Stored source records differ from supplied catalog')
        source_count = conn.execute(text(f'SELECT count(*) FROM {SOURCE}.aggregated_listings WHERE embedding_vector IS NOT NULL')).scalar_one()
        if source_count != 789:
            raise ValueError('Source must have all 789 real embeddings before graph indexing')
        legal_hash = conn.execute(text('SELECT manifest_sha256 FROM public.legal_corpus_releases WHERE schema_name=:schema'),
                                  {'schema': legal}).scalar_one()
        conn.execute(text(f'CREATE SCHEMA IF NOT EXISTS {GRAPH}'))
        conn.execute(text(f'CREATE SCHEMA IF NOT EXISTS {HOUSING}'))
        conn.execute(text(f'CREATE TABLE IF NOT EXISTS {GRAPH}.release (id integer PRIMARY KEY CHECK(id=1), '
            'housing_sha256 text NOT NULL,legal_sha256 text NOT NULL,listing_schema text NOT NULL,legal_schema text NOT NULL,'
            'extractor_version text NOT NULL,created_at timestamptz NOT NULL)'))
        existing = conn.execute(text(f'SELECT * FROM {GRAPH}.release WHERE id=1')).mappings().first()
        if existing and (existing['housing_sha256'] != digest or existing['legal_sha256'] != legal_hash
                         or (existing['extractor_version'] != VERSION and not args.rebuild)):
            raise ValueError('Different graph release already exists; create a new version')
        conn.execute(text(f'CREATE TABLE IF NOT EXISTS {HOUSING}.aggregated_listings '
                          '(LIKE public.aggregated_listings INCLUDING ALL)'))
        conn.execute(text(f'CREATE TABLE IF NOT EXISTS {HOUSING}.release (LIKE {SOURCE}.release INCLUDING ALL)'))
        if not existing:
            count = conn.execute(text(f'SELECT count(*) FROM {HOUSING}.aggregated_listings')).scalar_one()
            if count:
                raise ValueError('Housing target contains an unregistered release')
            # Copy verified immutable embeddings: graph construction does not
            # change the text or manufacture a new embedding version.
            conn.execute(text(f'INSERT INTO {HOUSING}.aggregated_listings SELECT * FROM {SOURCE}.aggregated_listings'))
            conn.execute(text(f'INSERT INTO {HOUSING}.release SELECT * FROM {SOURCE}.release'))
        conn.execute(text(f'CREATE TABLE IF NOT EXISTS {GRAPH}.nodes (id text PRIMARY KEY,kind text NOT NULL '
            "CHECK(kind IN ('listing','amenity','location','district','campus','document','provision','topic')),"
            'record_id integer,document_id integer,provision_id text,label text NOT NULL)'))
        conn.execute(text(f'CREATE TABLE IF NOT EXISTS {GRAPH}.edges (source text REFERENCES {GRAPH}.nodes(id),'
            f'target text REFERENCES {GRAPH}.nodes(id),relation text NOT NULL '
            "CHECK(relation IN ('has_amenity','located_in','distance_to','belongs_to','covers','cites')),"
            'evidence jsonb NOT NULL,PRIMARY KEY(source,target,relation),CHECK(source<>target))'))
        conn.execute(text(f'CREATE INDEX IF NOT EXISTS edges_target_relation_idx ON {GRAPH}.edges(target,relation)'))
        def node(identifier, kind, label, record_id=None, document_id=None, provision_id=None):
            conn.execute(text(f'INSERT INTO {GRAPH}.nodes VALUES(:id,:kind,:record,:doc,:pid,:label) ON CONFLICT(id) DO NOTHING'),
                         {'id': identifier, 'kind': kind, 'record': record_id, 'doc': document_id, 'pid': provision_id, 'label': label})
        def edge(source, target, relation, evidence):
            conn.execute(text(f'INSERT INTO {GRAPH}.edges VALUES(:source,:target,:relation,CAST(:evidence AS jsonb)) '
                              'ON CONFLICT(source,target,relation) DO NOTHING'),
                         {'source': source, 'target': target, 'relation': relation, 'evidence': json.dumps(evidence, ensure_ascii=False)})
        if args.rebuild and existing:
            conn.execute(text(f'DELETE FROM {GRAPH}.edges'))
            conn.execute(text(f'DELETE FROM {GRAPH}.nodes'))
            conn.execute(text(f'DELETE FROM {GRAPH}.release'))
            existing = None
        if not existing:
            node('campus:ctu_khu_ii', 'campus', 'CTU khu II')
            listings = [dict(row) for row in conn.execute(text(
                f'SELECT id,title,address,district,parsed_amenities,distance_to_ctu FROM {HOUSING}.aggregated_listings ORDER BY id')).mappings()]
            for listing in listings:
                identifier = f"housing:{listing['id']}"
                node(identifier, 'listing', listing['title'], record_id=listing['id'])
                evidence_base = {'catalog_sha256': digest, 'record_id': listing['id'], 'origin': 'supplied_catalog'}
                if listing['district']:
                    district_id = 'district:' + listing['district']
                    node(district_id, 'district', listing['district'])
                    edge(identifier, district_id, 'located_in', dict(evidence_base, field='district', value=listing['district']))
                # Location entities use explicit title/address, not district
                # guesses, coordinates or free-form instructions in descriptions.
                for field in ('title', 'address'):
                    for location in location_entities(listing.get(field) or ''):
                        node(location, 'location', location.split(':', 1)[1])
                        edge(identifier, location, 'located_in', dict(evidence_base, field=field, value=listing[field]))
                for key, enabled in (listing['parsed_amenities'] or {}).items():
                    if enabled is True:
                        amenity = 'amenity:' + key
                        node(amenity, 'amenity', key)
                        edge(identifier, amenity, 'has_amenity', dict(evidence_base, field='parsed_amenities.' + key, value=True))
                if listing['distance_to_ctu'] is not None:
                    edge(identifier, 'campus:ctu_khu_ii', 'distance_to', dict(evidence_base,
                        field='distance_to_ctu', metres=listing['distance_to_ctu'], method='approximate_haversine',
                        route_time_known=False, vacancy_verified=False))
            provisions = [dict(row) for row in conn.execute(text(
                f'SELECT DISTINCT ON (c.document_id,c.provision_id) c.document_id,c.provision_id,c.heading,c.parent_content,'
                f'c.source_metadata,d.title,d.category FROM {legal}.legal_chunks c JOIN {legal}.legal_documents d ON d.id=c.document_id '
                "WHERE d.status='ready' AND c.provision_id IS NOT NULL ORDER BY c.document_id,c.provision_id,c.chunk_index")).mappings()]
            lookup = {}
            for part in provisions:
                identifier = f"legal:{part['document_id']}:{part['provision_id']}"
                doc = f"document:{part['document_id']}"
                topic = 'topic:' + part['category']
                node(doc, 'document', part['title'], document_id=part['document_id'])
                node(topic, 'topic', part['category'])
                node(identifier, 'provision', part['heading'] or part['provision_id'], document_id=part['document_id'], provision_id=part['provision_id'])
                evidence = {'manifest_sha256': legal_hash, 'document_id': part['document_id'], 'provision_id': part['provision_id']}
                edge(identifier, doc, 'belongs_to', evidence)
                edge(doc, topic, 'covers', evidence)
                metadata = part['source_metadata'] or {}
                article, clause = str(metadata.get('article') or ''), str(metadata.get('clause') or '')
                if article:
                    lookup.setdefault((part['document_id'], article, clause), []).append(identifier)
            reference_edges = 0
            for part in provisions:
                body = part['parent_content'] or ''
                # Named external references need an explicit document resolver;
                # only unambiguous "law/decree/circular này" links are resolved.
                for clause, article in set(re.findall(r'(?:khoản\s+(\d+)\s+)?Điều\s+(\d+)\s+(?:của\s+)?(?:Luật|Thông tư|Nghị định)\s+này', body, re.I)):
                    targets = lookup.get((part['document_id'], article, clause), [])
                    if not clause:
                        targets = [identifier for (doc_id, article_id, _), identifiers in lookup.items()
                                   if doc_id == part['document_id'] and article_id == article for identifier in identifiers]
                    for target in targets:
                        source = f"legal:{part['document_id']}:{part['provision_id']}"
                        if source != target:
                            edge(source, target, 'cites', {'manifest_sha256': legal_hash, 'reference_article': article,
                                 'reference_clause': clause or None, 'same_document': True})
                            reference_edges += 1
            conn.execute(text(f'INSERT INTO {GRAPH}.release VALUES(1,:housing,:legal,:ls,:ds,:version,now())'),
                         {'housing': digest, 'legal': legal_hash, 'ls': HOUSING, 'ds': legal, 'version': VERSION})
        after = snapshot(conn)
        if after != before:
            raise ValueError('Protected public listing corpus changed')
        counts = {'housing_records': conn.execute(text(f'SELECT count(*) FROM {HOUSING}.aggregated_listings')).scalar_one(),
                  'housing_vectors': conn.execute(text(f'SELECT count(embedding_vector) FROM {HOUSING}.aggregated_listings')).scalar_one(),
                  'nodes': conn.execute(text(f'SELECT count(*) FROM {GRAPH}.nodes')).scalar_one(),
                  'edges': conn.execute(text(f'SELECT count(*) FROM {GRAPH}.edges')).scalar_one()}
        relations = dict(conn.execute(text(f'SELECT relation,count(*) FROM {GRAPH}.edges GROUP BY relation ORDER BY relation')).all())
        kinds = dict(conn.execute(text(f'SELECT kind,count(*) FROM {GRAPH}.nodes GROUP BY kind ORDER BY kind')).all())
    report = {'created_at_utc': datetime.now(timezone.utc).isoformat(), 'graph_schema': GRAPH, 'listing_schema': HOUSING,
              'legal_schema': legal, 'housing_sha256': digest, 'legal_sha256': legal_hash, 'counts': counts,
              'node_kinds': kinds, 'edge_relations': relations, 'public_before': before, 'public_after': after,
              'embedding_policy': 'reuse verified immutable real E5 embeddings; text unchanged',
              'scope': 'internal supplied data; bounded local graph; no cloud housing payloads'}
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'counts': counts, 'relations': relations, 'public_unchanged': before == after}), flush=True)


if __name__ == '__main__':
    main()
