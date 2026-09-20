"""Short-lived aggregate cache; Redis is optional and never owns listing data."""
import json
import time

from redis.exceptions import RedisError


class StatsCache:
    def __init__(self, client, ttl: int = 30):
        self.client = client
        self.ttl = ttl
        self.retry_at = 0.0

    def get(self):
        if not self.ttl or time.monotonic() < self.retry_at:
            return None
        try:
            raw = self.client.get("listings:stats:ctu:v1")
            return json.loads(raw) if raw else None
        except (RedisError, ValueError, TypeError):
            self.retry_at = time.monotonic() + 10
            return None

    def put(self, value: dict) -> None:
        if not self.ttl or time.monotonic() < self.retry_at:
            return
        try:
            self.client.setex("listings:stats:ctu:v1", self.ttl, json.dumps(value))
        except RedisError:
            self.retry_at = time.monotonic() + 10
