"""Read-only public HTTP benchmark. No accounts, prompts or credentials are stored.

Run before/after deployment with the same dataset and host:
  python scripts/benchmark_responses.py --samples 10
"""
import argparse
import json
import math
import statistics
import time

import httpx


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--api", default="http://127.0.0.1:8000")
    parser.add_argument("--web", default="http://127.0.0.1:3000")
    parser.add_argument("--samples", type=int, default=10)
    args = parser.parse_args()
    if not 1 <= args.samples <= 100:
        parser.error("samples must be between 1 and 100")
    coords = "?lat=10.0322&lng=105.7683&radius=3000"
    targets = {
        "listings": args.api + "/listings?page=1&size=12",
        "nearby_full": args.api + "/listings/nearby" + coords,
        "map_summary": args.api + "/listings/map" + coords,
        "stats": args.api + "/listings/stats",
        "home": args.web + "/",
    }
    output = {}
    with httpx.Client(timeout=30, trust_env=False) as client:
        for name, url in targets.items():
            warmup = client.get(url)
            if warmup.status_code != 200:
                output[name] = {"status": warmup.status_code}
                continue
            durations = []
            for _ in range(args.samples):
                started = time.perf_counter()
                response = client.get(url)
                response.raise_for_status()
                durations.append((time.perf_counter() - started) * 1000)
            output[name] = {
                "samples": len(durations),
                "median_ms": round(statistics.median(durations), 2),
                "p95_ms": round(sorted(durations)[math.ceil(len(durations) * 0.95) - 1], 2),
                "decoded_bytes": len(response.content),
                "server_timing": response.headers.get("server-timing"),
            }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
