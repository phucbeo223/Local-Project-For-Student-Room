"""FR4: versioned 384D structured content vectors (not E5 text embeddings)."""

import hashlib
import math
import random

DIMENSIONS = 384
VERSION = "structured-cosine-v1"
WEIGHTS = {"view": 1, "click_source": 2, "click_phone": 3, "bookmark": 4}


def normalize(values):
    length = math.sqrt(sum(v * v for v in values))
    return [v / length for v in values] if length else values


def content_vector(row: dict, *, quiz: bool = False) -> list[float]:
    vector = [0.0] * DIMENSIONS
    price = row.get("max_price") if quiz else row.get("price")
    distance = row.get("max_distance_ctu") if quiz else row.get("distance_to_ctu")
    # Disjoint numeric ranges; nearby bins overlap smoothly. No Python hash()
    # (randomized per worker); categorical bins use stable SHA256.
    for value, width, start, count in ((price, 250000, 0, 80), (distance, 500, 80, 40)):
        if value is not None:
            position = min(count - 1, max(0, float(value) / width))
            for i in range(count):
                vector[start + i] = math.exp(-(((i - position) / 3) ** 2))
    labels = []
    if row.get("district"):
        labels.append("district:" + row["district"].strip().casefold())
    amenities = (
        row.get("amenities", [])
        if quiz
        else [k for k, v in (row.get("parsed_amenities") or {}).items() if v is True]
    )
    labels.extend("amenity:" + key for key in amenities)
    for label in labels:
        index = (
            120
            + int.from_bytes(hashlib.sha256(label.encode()).digest()[:4], "big") % 264
        )
        vector[index] += 2
    return normalize(vector)


def profile_vector(preferences: dict | None, history: list[dict]) -> list[float] | None:
    base = content_vector(preferences, quiz=True) if preferences else [0.0] * DIMENSIONS
    result = [v * 8 for v in base]
    seen = set()
    for row in history:
        key = (row["id"], row["type"])
        weight = WEIGHTS.get(row["type"], 0)
        if key in seen or not weight:
            continue
        seen.add(key)
        result = [a + b * weight for a, b in zip(result, content_vector(row))]
    return normalize(result) if any(result) else None


def rank(candidates, history, preferences, limit=10, rng=None):
    rng = rng or random.SystemRandom()
    profile = profile_vector(preferences, history)
    dismissed = {r["id"] for r in history if r["type"] == "dismiss"}
    rows = []
    for row in candidates:
        if row["id"] in dismissed or (
            row.get("risk_evaluated_at") and float(row.get("risk_score") or 0) >= 0.6
        ):
            continue
        if preferences:
            if row.get("price") is None or row["price"] > preferences["max_price"]:
                continue
            if (
                row.get("distance_to_ctu") is None
                or row["distance_to_ctu"] > preferences["max_distance_ctu"]
            ):
                continue
            if any(
                (row.get("parsed_amenities") or {}).get(k) is not True
                for k in preferences.get("amenities", [])
            ):
                continue
        score = (
            sum(a * b for a, b in zip(profile, content_vector(row)))
            if profile
            else float(row.get("popularity") or 0)
        )
        rows.append((score, row))
    rows.sort(
        key=lambda pair: (
            -pair[0],
            -float(pair[1].get("quality_score") or 0),
            pair[1]["id"],
        )
    )
    size = min(limit, len(rows))
    exploration = math.floor(size * 0.2) if profile else 0
    exploit = rows[: size - exploration]
    explore = rng.sample(rows[size - exploration :], exploration) if exploration else []
    ranked = [(score, row, False) for score, row in exploit] + [
        (score, row, True) for score, row in explore
    ]
    return profile, ranked
