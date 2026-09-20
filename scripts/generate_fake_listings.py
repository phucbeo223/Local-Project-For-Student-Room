"""Generate deterministic, controlled development data for the chatbot.

Outputs SQL only; it never connects to a database. The SQL owns the `dev_seed`
namespace and is idempotent. Embeddings are intentionally NULL and must be
created later by index_listing_embeddings.py using multilingual-e5-small.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATASET_VERSION = "ctu-housing-chatbot-v1.0.0"


def sql(value) -> str:
    if value is None:
        return "NULL"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    return "'" + str(value).replace("'", "''") + "'"


DISTRICTS = [
    ("Ninh Kiều", "Xuân Khánh", 10.0302, 105.7680),
    ("Cái Răng", "Hưng Phú", 10.0020, 105.7860),
    ("Bình Thủy", "An Thới", 10.0710, 105.7470),
    ("Phong Điền", "Nhơn Ái", 9.9990, 105.6650),
]


def listing_record(index: int, rng: random.Random) -> dict:
    district, ward, base_lat, base_lng = DISTRICTS[index % len(DISTRICTS)]
    category = "golden" if index < 100 else "normal" if index < 850 else "noisy" if index < 950 else "invalid"
    listing_type = "phong_tro" if index < 750 else "nha_nguyen_can" if index < 850 else "mat_bang" if index < 930 else "khac"
    status = "active" if index < 800 else "expired" if index < 900 else "flagged" if index < 950 else "hidden"
    cleaning = "cleaned" if index < 850 else "raw" if index < 950 else "rejected"
    cheap_far = index % 10 == 0
    near_expensive = index % 10 == 1
    price = 900_000 + (index % 19) * 100_000
    if cheap_far:
        price = 750_000 + (index % 3) * 100_000
    if near_expensive:
        price = 3_200_000 + (index % 4) * 200_000
    area = 12 + (index % 29)
    distance = 3500 + (index % 12) * 220 if cheap_far else 180 + (index % 22) * 125
    lat = base_lat + rng.uniform(-0.012, 0.012)
    lng = base_lng + rng.uniform(-0.012, 0.012)
    has_ac = index % 2 == 0
    has_mezzanine = index % 3 != 0
    pets = index % 7 == 0
    flexible = index % 4 != 0
    gender = "female" if index % 17 == 0 else "male" if index % 19 == 0 else "any"
    amenities = {
        "wifi": index % 9 != 0,
        "air_conditioner": has_ac,
        "mezzanine": has_mezzanine,
        "parking": index % 8 != 0,
        "private_bathroom": index % 5 != 0,
        "pets_allowed": pets,
        "flexible_hours": flexible,
        "gender": gender,
        "deposit_months": 1 if index % 6 else 2,
        "electricity_vnd_kwh": 3500 + (index % 4) * 500,
        "water_vnd_month": 50_000 + (index % 4) * 20_000,
        "internet_vnd_month": 0 if index % 5 else 100_000,
        "campus": (index % 3) + 1,
    }
    feature_text = ["wifi tốc độ cao"]
    feature_text.append("có máy lạnh" if has_ac else "không có máy lạnh")
    feature_text.append("có gác" if has_mezzanine else "không gác")
    feature_text.append("cho nuôi thú cưng" if pets else "không nhận thú cưng")
    feature_text.append("giờ giấc tự do" if flexible else "đóng cổng 23 giờ")
    if gender == "female":
        feature_text.append("chỉ cho nữ thuê")
    elif gender == "male":
        feature_text.append("chỉ cho nam thuê")
    title = f"{('Phòng trọ' if listing_type == 'phong_tro' else 'Nhà cho thuê')} {ward} #{index + 1:04d}"
    description = (
        f"{', '.join(feature_text)}. Cọc {amenities['deposit_months']} tháng; điện "
        f"{amenities['electricity_vnd_kwh']}đ/kWh, nước {amenities['water_vnd_month']}đ/tháng. "
        f"Cách cơ sở CTU gần nhất khoảng {distance:.0f}m."
    )
    if category == "noisy":
        # Pairwise near-duplicates with real duplicate hashes, never duplicate source IDs.
        pair = (index - 850) // 2
        title = f"Phòng trọ đăng lại nhóm {pair:02d}"
        description = f"Tin đăng gần trùng nhóm {pair:02d}. wifi, giá tốt, liên hệ ngay."
    address = f"Hẻm {20 + index % 180}, phường {ward}, {district}, Cần Thơ"
    if category == "invalid" and index % 2 == 0:
        address = None
    if category == "invalid" and index % 2 == 1:
        price = None
    canonical = f"{title}|{description}|{address}|{price}|{area}"
    return {
        "source_id": f"dev-2026-{index + 1:04d}",
        "title": title,
        "price": price,
        "area": area,
        "address": address,
        "district": district if address else None,
        "lat": lat if address else None,
        "lng": lng if address else None,
        "description": description,
        "amenities": amenities,
        "content_hash": hashlib.sha256(canonical.encode("utf-8")).hexdigest(),
        "distance": distance if address else None,
        "route": [round(distance / speed, 1) for speed in (180, 230, 160)] if address else None,
        "status": status,
        "cleaning": cleaning,
        "listing_type": listing_type,
        "quality": round(0.62 + (index % 31) / 100, 2) if category != "invalid" else 0.15,
        "risk": round(0.7 + (index % 20) / 100, 2) if status == "flagged" else round((index % 12) / 100, 2),
        "freshness": round(max(0.05, 1.0 - (index % 40) / 50), 2),
    }


def generate_sql(seed: int) -> str:
    rng = random.Random(seed)
    listings = [listing_record(i, rng) for i in range(1000)]
    lines = [
        "-- Generated by scripts/generate_fake_listings.py --seed 2026",
        "-- DEVELOPMENT/TEST ONLY. Embeddings stay NULL until the real E5 indexer runs.",
        "BEGIN;",
    ]
    user_values = ",\n".join(
        f"('dev2026.user{i:02d}@example.test', 'Sinh viên thử nghiệm {i:02d}', 'user', true)"
        for i in range(1, 51)
    )
    lines.append(
        "INSERT INTO users (email, name, role, email_verified) VALUES\n"
        + user_values
        + "\nON CONFLICT (email) DO UPDATE SET name = EXCLUDED.name;"
    )
    identity_values = []
    for i in range(1, 51):
        identity_values.append(
            f"((SELECT id FROM users WHERE email='dev2026.user{i:02d}@example.test'), 'dev_seed', 'dev2026-{i:02d}', NULL)"
        )
    for i in range(1, 11):
        identity_values.append(
            f"((SELECT id FROM users WHERE email='dev2026.user{i:02d}@example.test'), 'dev_seed_alt', 'dev2026-alt-{i:02d}', NULL)"
        )
    lines.append(
        "INSERT INTO user_identities (user_id, provider, provider_user_id, secret_hash) VALUES\n"
        + ",\n".join(identity_values)
        + "\nON CONFLICT (provider, provider_user_id) DO NOTHING;"
    )

    listing_values = []
    for item in listings:
        geom = (
            f"ST_SetSRID(ST_MakePoint({item['lng']:.6f}, {item['lat']:.6f}), 4326)"
            if item["lat"] is not None
            else "NULL"
        )
        route = "ARRAY[" + ",".join(map(str, item["route"])) + "]::REAL[]" if item["route"] else "NULL"
        listing_values.append(
            "(" + ", ".join(
                (
                    sql(item["title"]), sql(item["price"]), sql(item["area"]), sql(item["address"]),
                    sql(item["district"]), geom, sql(item["description"]), "'dev_seed'",
                    sql(f"https://example.test/listings/{item['source_id']}"), sql(item["source_id"]),
                    sql(item["content_hash"]), sql(json.dumps(item["amenities"], ensure_ascii=False)) + "::jsonb",
                    sql(item["risk"]), sql(item["distance"]), sql(item["status"]), route,
                    sql(item["cleaning"]), sql(item["listing_type"]), sql(item["quality"]), sql(item["freshness"]),
                    "'dev-seed-label-v1'", "now()", "'evaluated'",
                )
            ) + ")"
        )
    lines.append(
        "INSERT INTO aggregated_listings "
        "(title, price, area, address, district, geom, description, source, source_url, source_id, "
        "content_hash, parsed_amenities, risk_score, distance_to_ctu, status, route_time_campus, "
        "cleaning_status, listing_type, quality_score, freshness_score, "
        "risk_model, risk_evaluated_at, risk_status) VALUES\n"
        + ",\n".join(listing_values)
        + "\nON CONFLICT (source, source_id) DO UPDATE SET "
        "title=EXCLUDED.title, price=EXCLUDED.price, area=EXCLUDED.area, address=EXCLUDED.address, "
        "district=EXCLUDED.district, geom=EXCLUDED.geom, description=EXCLUDED.description, "
        "content_hash=EXCLUDED.content_hash, parsed_amenities=EXCLUDED.parsed_amenities, "
        "risk_score=EXCLUDED.risk_score, distance_to_ctu=EXCLUDED.distance_to_ctu, "
        "status=EXCLUDED.status, route_time_campus=EXCLUDED.route_time_campus, "
        "cleaning_status=EXCLUDED.cleaning_status, listing_type=EXCLUDED.listing_type, "
        "quality_score=EXCLUDED.quality_score, freshness_score=EXCLUDED.freshness_score, "
        "risk_model=EXCLUDED.risk_model, risk_evaluated_at=EXCLUDED.risk_evaluated_at, "
        "risk_status=EXCLUDED.risk_status, "
        "embedding_vector=NULL, embedding_model=NULL, embedded_content_hash=NULL, embedded_at=NULL;"
    )

    seed_users = "SELECT id FROM users WHERE email LIKE 'dev2026.user%@example.test'"
    seed_listings = "SELECT id FROM aggregated_listings WHERE source = 'dev_seed'"
    lines.extend(
        [
            f"DELETE FROM user_interactions WHERE user_id IN ({seed_users}) AND listing_id IN ({seed_listings});",
            f"DELETE FROM saved_searches WHERE user_id IN ({seed_users});",
        ]
    )
    interactions = []
    for i in range(1000):
        user_no = i % 50 + 1
        listing_no = (i * 37) % 1000 + 1
        kind = ("view", "bookmark", "click_source", "click_phone")[i % 4]
        interactions.append(
            f"((SELECT id FROM users WHERE email='dev2026.user{user_no:02d}@example.test'), "
            f"(SELECT id FROM aggregated_listings WHERE source='dev_seed' AND source_id='dev-2026-{listing_no:04d}'), "
            f"'{kind}', {500 + (i % 120) * 250})"
        )
    lines.append(
        "INSERT INTO user_interactions (user_id, listing_id, type, duration_ms) VALUES\n"
        + ",\n".join(interactions) + ";"
    )
    searches = []
    for i in range(100):
        user_no = i % 50 + 1
        criteria = {"max_price": 1_500_000 + (i % 8) * 250_000, "district": DISTRICTS[i % 4][0], "amenities": ["wifi"]}
        searches.append(
            f"((SELECT id FROM users WHERE email='dev2026.user{user_no:02d}@example.test'), "
            f"{sql(f'Tìm trọ thử nghiệm {i + 1:03d}')}, "
            f"{sql(json.dumps(criteria, ensure_ascii=False))}::jsonb)"
        )
    lines.append("INSERT INTO saved_searches (user_id, name, criteria) VALUES\n" + ",\n".join(searches) + ";")

    lines.extend(["COMMIT;", ""])
    return "\n".join(lines)


def generate_eval(seed: int) -> list[dict]:
    rng = random.Random(seed)
    cases: list[dict] = []
    records = [listing_record(i, random.Random(seed + i)) for i in range(1000)]

    def relevant_ids(filters: dict) -> list[str]:
        output: list[str] = []
        for item in records:
            if item["status"] != "active" or item["cleaning"] != "cleaned":
                continue
            if filters.get("listing_type") and item["listing_type"] != filters["listing_type"]:
                continue
            if filters.get("max_price") is not None and (
                item["price"] is None or item["price"] > filters["max_price"]
            ):
                continue
            if filters.get("district") and item["district"] != filters["district"]:
                continue
            if any(item["amenities"].get(key) is not True for key in filters.get("amenities", [])):
                continue
            if filters.get("gender") and item["amenities"].get("gender", "any") not in (
                "any",
                filters["gender"],
            ):
                continue
            if filters.get("max_distance_ctu") is not None and (
                item["distance"] is None or item["distance"] > filters["max_distance_ctu"]
            ):
                continue
            output.append(item["source_id"])
        return output

    def case_payload(*, filters: dict, should_answer: bool) -> dict:
        ids = relevant_ids(filters) if should_answer else []
        by_id = {item["source_id"]: item for item in records}
        reference_rows = [by_id[item_id] for item_id in ids[:5]]
        if reference_rows:
            choices = []
            for rank, item in enumerate(reference_rows[:3], 1):
                price = f"{int(item['price']):,} đồng/tháng".replace(",", ".")
                choices.append(
                    f"[{rank}] {item['title']}, giá {price}, khu vực {item['district']}"
                )
            reference_answer = "Các lựa chọn phù hợp gồm: " + "; ".join(choices) + "."
        else:
            reference_answer = "Không có kết quả phù hợp hoặc yêu cầu nằm ngoài phạm vi hỗ trợ."
        return {
            "dataset_version": DATASET_VERSION,
            "expected_listing_ids": ids,
            "reference_context_ids": ids[:5],
            "reference_answer": reference_answer,
        }
    districts = [item[0] for item in DISTRICTS]
    amenities = [
        ("wifi", "wifi"),
        ("air_conditioner", "máy lạnh"),
        ("mezzanine", "gác"),
        ("pets_allowed", "nuôi thú cưng"),
    ]
    for i in range(120):
        district = districts[i % len(districts)]
        max_price = 1_500_000 + (i % 7) * 250_000
        # Rotate until the requested combination has at least one true positive.
        # This prevents calling an impossible synthetic combination an answer case.
        filters = {}
        amenity = amenity_label = ""
        for offset in range(len(amenities)):
            amenity, amenity_label = amenities[(i + offset) % len(amenities)]
            filters = {"max_price": max_price, "district": district, "amenities": [amenity], "listing_type": "phong_tro"}
            if relevant_ids(filters):
                break
        cases.append({
            "id": f"answer-{i + 1:03d}",
            "question": f"Tìm phòng trọ dưới {max_price // 1000}k ở {district}, có {amenity_label}",
            "conversation_history": [],
            "expected_filters": filters,
            "expected_intent": "find_listing",
            "should_answer": True,
            "forbidden_listing_ids": [],
            "notes": "structured-filter",
            "tags": ["answer", "vietnamese"],
            **case_payload(filters=filters, should_answer=True),
        })
    for i in range(30):
        filters = {"max_price": 100_000, "listing_type": "phong_tro"}
        cases.append({
            "id": f"no-answer-{i + 1:03d}",
            "question": f"Phòng trọ dưới 100k có hồ bơi riêng tại Cần Thơ mẫu {i}",
            "conversation_history": [],
            "expected_filters": filters,
            "expected_intent": "find_listing",
            "should_answer": False,
            "forbidden_listing_ids": [f"dev-2026-{n:04d}" for n in range(951, 1001)],
            "notes": "must not hallucinate",
            "tags": ["no-answer"],
            **case_payload(filters=filters, should_answer=False),
        })
    outside = ["thời tiết", "bóng đá", "lập trình Python", "chứng khoán", "nấu ăn"]
    for i in range(20):
        topic = outside[i % len(outside)]
        cases.append({
            "id": f"out-of-scope-{i + 1:03d}",
            "question": f"Cho mình hỏi về {topic}?",
            "conversation_history": [],
            "expected_filters": {},
            "expected_intent": "out_of_scope",
            "should_answer": False,
            "forbidden_listing_ids": [],
            "notes": "scope refusal",
            "tags": ["out-of-scope"],
            **case_payload(filters={}, should_answer=False),
        })
    conversation_queries = [
        ("Tìm phòng dưới 2 triệu gần CTU", {"max_price": 2_000_000, "listing_type": "phong_tro"}, []),
        ("Phòng nữ có wifi ở Ninh Kiều", {"district": "Ninh Kiều", "amenities": ["wifi"], "gender": "female", "listing_type": "phong_tro"}, []),
        ("Phòng có gác cách trường dưới 2 km", {"amenities": ["mezzanine"], "max_distance_ctu": 2000, "listing_type": "phong_tro"}, []),
        ("Còn phòng nào rẻ hơn?", {"max_price": 2_000_000, "district": "Ninh Kiều", "listing_type": "phong_tro"}, [
            {"role": "user", "content": "Tìm phòng trọ dưới 2 triệu ở Ninh Kiều"},
            {"role": "assistant", "content": "Mình đã tìm được một số phòng phù hợp."},
        ]),
    ]
    for i in range(30):
        question, filters, history = conversation_queries[i % len(conversation_queries)]
        cases.append({
            "id": f"stateless-{i + 1:03d}",
            "question": question,
            "conversation_history": history,
            "expected_filters": filters,
            "expected_intent": "find_listing",
            "should_answer": True,
            "forbidden_listing_ids": [],
            "notes": "client-side conversation context; no server-side message persistence",
            "tags": ["conversation", "hybrid"],
            **case_payload(filters=filters, should_answer=True),
        })
    rng.shuffle(cases)
    return cases


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=2026)
    parser.add_argument("--output-sql", type=Path, default=ROOT / "infra/db/seeds/dev_chatbot.sql")
    parser.add_argument("--output-eval", type=Path, default=ROOT / "eval/datasets/chatbot_eval.jsonl")
    parser.add_argument("--output-metadata", type=Path, default=ROOT / "eval/datasets/metadata.json")
    args = parser.parse_args()
    args.output_sql.parent.mkdir(parents=True, exist_ok=True)
    args.output_eval.parent.mkdir(parents=True, exist_ok=True)
    args.output_metadata.parent.mkdir(parents=True, exist_ok=True)
    args.output_sql.write_text(generate_sql(args.seed), encoding="utf-8", newline="\n")
    cases = generate_eval(args.seed)
    args.output_eval.write_text(
        "\n".join(json.dumps(case, ensure_ascii=False) for case in cases) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    args.output_metadata.write_text(
        json.dumps(
            {
                "dataset_version": DATASET_VERSION,
                "seed": args.seed,
                "listing_count": 1000,
                "question_count": len(cases),
                "generator": "scripts/generate_fake_listings.py",
                "purpose": "Development and reproducible offline evaluation only",
                "ground_truth_protocol": (
                    "Expected listing IDs are deterministically derived from documented business filters. "
                    "A manually reviewed golden subset must be recorded before publication."
                ),
                "research_sources": [
                    "10.18653/v1/2024.eacl-demo.16",
                    "10.5555/3495724.3496517"
                ],
            },
            ensure_ascii=False,
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )
    print("Generated 1000 listings, 50 users, 60 identities, 1000 interactions, 100 searches")
    print(f"Generated 200 evaluation cases; dataset={DATASET_VERSION}")
    print("Embeddings: 0 random vectors (run index_listing_embeddings.py for real E5 vectors)")


if __name__ == "__main__":
    main()
