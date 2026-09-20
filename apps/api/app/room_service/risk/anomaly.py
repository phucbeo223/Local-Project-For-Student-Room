"""IsolationForest on recent, same-district real listings; no pickle loading."""

import math
import threading
import time

_cache = {}
_lock = threading.Lock()


def features(row):
    price, area = row.get("price"), row.get("area")
    if not price or not area or float(price) <= 0 or float(area) <= 0:
        return None
    return [
        math.log1p(float(price)),
        math.log1p(float(area)),
        math.log1p(float(price) / float(area)),
    ]


def anomaly_signal(repo, listing):
    vector = features(listing)
    if vector is None or not listing.get("district"):
        return False, "insufficient_features"
    try:
        from sklearn.ensemble import IsolationForest
    except ImportError:
        return False, "dependency_unavailable"
    # Cache bounded, keyed by engine object (never credentials). Cold start is
    # serialized to avoid concurrent duplicate fits. Refresh at least hourly.
    key = (repo.engine, listing["district"], listing.get("listing_type") or "phong_tro")
    with _lock:
        cached = _cache.get(key)
        if cached is None or time.monotonic() - cached[0] > 3600:
            rows = repo.anomaly_cohort(listing)
            values = [v for row in rows if (v := features(row)) is not None]
            if len(values) < 50:
                return False, "insufficient_cohort"
            model = IsolationForest(
                n_estimators=100, contamination=0.05, random_state=42, n_jobs=1
            ).fit(values)
            if len(_cache) >= 100:
                _cache.clear()
            cached = (time.monotonic(), model)
            _cache[key] = cached
    return bool(cached[1].predict([vector])[0] == -1), "available"
