"""Read-only audit of actual Graph RAG results against stored source facts."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from sqlalchemy import create_engine, text
from app.config import settings
import question_bank_ragas as bank
from app.room_service.chatbot.graph_retrieval import location_entities
from app.room_service.chatbot.providers import normalize_text


def violations(row, filters):
    errors = []
    for field, lower, upper in [('price', 'min_price', 'max_price'), ('area', 'min_area', None)]:
        value = row.get(field)
        if filters.get(lower) is not None and (value is None or value < filters[lower]):
            errors.append(lower)
        if upper and filters.get(upper) is not None:
            exclusive = bool(filters.get('max_price_exclusive'))
            if value is None or (value >= filters[upper] if exclusive else value > filters[upper]):
                errors.append(upper)
    district = filters.get('district')
    if district and normalize_text(district) not in normalize_text(row.get('district') or ''):
        errors.append('district')
    if filters.get('max_distance_ctu') is not None:
        distance = row.get('distance_to_ctu')
        if distance is None or distance > filters['max_distance_ctu']:
            errors.append('max_distance_ctu')
    if filters.get('max_route_minutes') is not None:
        times = [value for value in (row.get('route_time_campus') or []) if value is not None]
        if not times or min(times) > filters['max_route_minutes']:
            errors.append('max_route_minutes')
    for key in filters.get('amenities') or []:
        if (row.get('parsed_amenities') or {}).get(key) is not True:
            errors.append('amenity:' + key)
    if filters.get('listing_type') and str(row['listing_type']) != filters['listing_type']:
        errors.append('listing_type')
    if filters.get('listing_ids') and row['id'] not in filters['listing_ids']:
        errors.append('listing_ids')
    if filters.get('gender') and (row.get('parsed_amenities') or {}).get('gender', 'any') not in ('any', filters['gender']):
        errors.append('gender')
    if row['status'] != 'active' or row['cleaning_status'] != 'cleaned':
        errors.append('eligibility')
    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--interim', action='store_true', help='Audit completed housing cases while legal generation continues')
    args = parser.parse_args()
    run = json.loads(args.run.read_text(encoding='utf-8'))
    if (not args.interim and any(not case.get('answer') or case.get('error') for case in run['cases'])) or any(case.get('error') for case in run['cases']):
        raise ValueError('Every selected question must finish without a runtime error before acceptance audit')
    if args.interim and any(not case.get('answer') for case in run['cases'] if case['category'] == 'find_listing'):
        raise ValueError('Complete housing questions before an interim audit')
    engine = create_engine(settings.database_url)
    checks = []
    with engine.connect() as conn:
        rows = {row['id']: dict(row) for row in conn.execute(text('SELECT * FROM housing_graph_v1.aggregated_listings')).mappings()}
        locations = {}
        for row in conn.execute(text("SELECT n.record_id,e.target FROM graph_rag_v1.edges e JOIN graph_rag_v1.nodes n "
                                    "ON n.id=e.source WHERE e.relation='located_in' AND n.kind='listing'")).mappings():
            locations.setdefault(row['record_id'], set()).add(row['target'])
        for case in run['cases']:
            if case['category'] != 'find_listing':
                continue
            filters = case.get('applied_filters') or {}
            requested_locations = location_entities(case['question'])
            matches = [row for row in rows.values() if not violations(row, filters)
                       and (not requested_locations or set(requested_locations) & locations.get(row['id'], set()))]
            issues = []
            for listing in case.get('listings', []):
                source = rows[listing['id']]
                issues.extend(f"{listing['id']}:{issue}" for issue in violations(source, filters))
                if requested_locations and not set(requested_locations) & locations.get(listing['id'], set()):
                    issues.append(f"{listing['id']}:location")
                if listing.get('corpus_schema') != 'housing_graph_v1':
                    issues.append(f"{listing['id']}:wrong_namespace")
                for field in ('price', 'area', 'district', 'distance_to_ctu', 'source_url'):
                    if listing.get(field) != source.get(field):
                        issues.append(f"{listing['id']}:source_field:{field}")
                if listing.get('amenities') != (source.get('parsed_amenities') or {}):
                    issues.append(f"{listing['id']}:source_field:amenities")
            if filters.get('sort_by') == 'price_asc' and case.get('listings') and matches:
                expected = min(matches, key=lambda row: (row['price'], row['id']))['id']
                if case['listings'][0]['id'] != expected:
                    issues.append('wrong_minimum_price')
            checks.append({'id': case['id'], 'question': case['question'], 'returned': len(case.get('listings', [])),
                'matching_source_records': len(matches), 'constraint_violations': issues,
                'confidence_abstention_with_matches': bool(matches) and not case.get('listings'),
                'unknown_capacity': 'hai sinh vien' in normalize_text(case['question']),
                'distance_policy': 'approximate coordinates/haversine, no route or time claim'})
        index = json.loads(Path('/eval/reports/graph_rag_index_2026-10-04.json').read_text(encoding='utf-8'))
        protected = dict(conn.execute(text("SELECT count(*) AS rows,count(embedding_vector) AS vectors, "
            "md5(string_agg(id::text||coalesce(content_hash,'')||coalesce(embedding_vector::text,''),'|' ORDER BY id)) AS digest "
            'FROM public.aggregated_listings')).mappings().one())
        full_protected = dict(conn.execute(text("SELECT count(*) AS rows,count(embedding_vector) AS vectors, "
            "md5(string_agg(row_to_json(t)::text,'|' ORDER BY id)) AS digest FROM public.aggregated_listings t")).mappings().one())
        previous = json.loads(Path('/eval/reports/legal_refresh_acceptance_2026-10-04.json').read_text(encoding='utf-8'))
    engine.dispose()
    violations_count = sum(len(check['constraint_violations']) for check in checks)
    summary = {'questions_completed': sum(bool(case.get('answer')) for case in run['cases']), 'runtime_errors': 0,
        'housing_questions': len(checks), 'housing_with_results': sum(bool(case['returned']) for case in checks),
        'housing_constraint_violations': violations_count,
        'housing_abstentions_with_matching_records': [case['id'] for case in checks if case['confidence_abstention_with_matches']],
        'protected_public_unchanged': protected == index['public_before'],
        'protected_public_full_rows_unchanged': full_protected == previous['listings'],
        'graph_traced_cases': sum(any(step.get('stage') == 'graph_retrieval' for step in case.get('agent_trace', [])) for case in run['cases']),
        'no_answer_ids': [case['id'] for case in run['cases'] if case.get('no_answer')],
        'partial_answer_ids': [case['id'] for case in run['cases'] if case.get('partial_answer')],
        'generation_providers': dict(Counter(case.get('generation_provider') for case in run['cases']))}
    report = {'created_at_utc': datetime.now(timezone.utc).isoformat(),
        'phase': 'interim' if args.interim else 'final',
        'run_sha256': hashlib.sha256(args.run.read_bytes()).hexdigest(), 'summary': summary, 'housing_cases': checks,
        'limitations': ['Constraint audit verifies returned fields against the supplied records, not source truth or vacancy.',
            'No verified independent answers for housing or KTX; no invented overall accuracy percentage.',
            'Legal guide question overlap makes this a known-topic regression; not an unseen benchmark.',
            'Confidence is a heuristic, not calibrated correctness probability.']}
    bank.save_report(args.output, report)
    print(json.dumps(summary, ensure_ascii=False), flush=True)
    if violations_count or not summary['protected_public_unchanged'] or not summary['protected_public_full_rows_unchanged']:
        raise SystemExit(2)


if __name__ == '__main__':
    main()
