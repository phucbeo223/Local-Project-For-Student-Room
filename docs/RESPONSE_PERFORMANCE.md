# Response performance: first optimization pass

## Delivered

- `/listings/stats` computes the visible listing count, all eligible listings within 3 km of CTU khu II, and the continuous median of positive prices in SQL. It replaces the home page's extra search and full nearby requests. Counts and median no longer depend on a 300-result cap.
- Redis caches only these aggregate statistics for 30 seconds. Set `LISTING_STATS_CACHE_SECONDS=0` to disable it. Redis has 100 ms connect/read timeouts and a 10-second retry cooldown; missing Redis falls back to SQL. Listing details, map records, visibility and moderation remain fresh database reads.
- `/listings/map` retains the nearest 300 visible listings but returns only fields used by the current map and the first image. `/listings/nearby` keeps its existing contract.
- Migration `97_response_performance.sql` adds the geography-expression GiST index matching `ST_DWithin(geom::geography, ...)`.
- The map uses the same-origin route proxy, aborts obsolete route requests, and loads sidebar images lazily.
- Qwen warms in a background thread at API startup and stays resident for 30 minutes after use. E5 then warms from its local model cache only, without startup downloads. API health is available while warming; requests arriving before warm-up finishes can still wait.
- Qwen and Gemini reuse HTTP clients, closed during API shutdown. Listing generation defaults to 384 output tokens; legal generation retains at least 700. Truncated model responses still fall back to grounded templates.
- E5 query embeddings use a thread-safe, process-local 256-entry/5-minute LRU cache. Keys hash the exact query text; vectors are copied on return and failed results are not cached. There is no shared cache of prompts or generated answers.
- `Server-Timing: api;dur=...` exposes server processing duration, including request dependencies and telemetry writes for JSON endpoints.

## Local measurements

Measured on 2026-09-21 (Asia/Saigon), with `scripts/benchmark_responses.py --samples 10`, a reused HTTP connection to `127.0.0.1`, one warm-up per endpoint, and the same local dataset (813 visible listings; 270 within 3 km). These are small sequential samples, not a concurrent-load benchmark or a production SLA.

| Operation | Before median | After median | Payload |
| --- | ---: | ---: | ---: |
| Home HTML response | 71.28 ms | 47.56 ms | 83,413 bytes after |
| Map data: full nearby → compact map | 31.95 ms | 12.65 ms | 393,910 → 82,354 bytes |
| New cached statistics | n/a | 3.59 ms | 57 bytes |
| Existing listing search | 10.58 ms | 11.33 ms | unchanged |

The map payload shrank by approximately 79%. Home HTML timing does not include browser rendering, images or hydration. The map sample had a 200.92 ms p95 outlier, so its median is not evidence of consistently low tail latency. Earlier ad-hoc measurements via `localhost` included connection/address-resolution overhead and should not be used as a baseline.

An authenticated UI smoke test of local `qwen3.5:4b` returned sourced listing/legal answers successfully with reported service latency of 44,445 ms and 39,015 ms. These were measured after the Qwen warm-up/client changes but before adding E5 startup warm-up. They do **not** demonstrate a chat speed-up: no comparable prior chat baseline was captured. GPU residency was verified using Ollama `/api/ps`. The local override configures a 60-second LLM timeout, whereas Compose defaults to 4 seconds.

## Verification

- Full isolated Docker/PostgreSQL suite: 169 passed, including uncapped statistics, compact map visibility, cache expiration/failure/concurrency and provider lifecycle.
- After adding cached-only E5 warm-up: 25 targeted provider/performance tests passed, including the new warm-up failure regression.
- TypeScript check and Next.js production build passed.
- Three chat rendering/source tests and one map/proxy browser test passed against the new deployment; one authenticated real-Qwen browser test passed.

Use `E2E_BASE_URL=http://127.0.0.1:3000` when validating this Docker setup. A separate process on IPv6 localhost may otherwise serve an older build; a stale process produced a chunk 404 during initial browser verification.

## Deploy and tune

Apply migration 97 to existing databases, then rebuild API/web. `scripts/start_all.ps1 -SkipSeed` applies it as part of the normal upgrade; the Python migration helpers also include it. For a large live table, schedule index creation or use an equivalent `CREATE INDEX CONCURRENTLY` migration outside a transaction to avoid blocking writers.

New environment settings are documented in `.env.example` and passed through Compose:

- `CHATBOT_WARMUP_ENABLED=true`
- `CHATBOT_WARMUP_TIMEOUT_SECONDS=30` (Ollama warm-up request timeout)
- `OLLAMA_KEEP_ALIVE=30m`
- `CHATBOT_MAX_OUTPUT_TOKENS=384` (listing answers; legal minimum remains 700)
- `LISTING_STATS_CACHE_SECONDS=30`

Longer model residency consumes GPU/RAM while idle. Set warm-up to false or shorten keep-alive on memory-constrained machines.

## Remaining work from the initial recommendations

Token streaming, a durable enrichment worker, broad listing-result caching with mutation invalidation, provider circuit breaking and lexical/vector retrieval redesign are not included in this pass. Streaming needs to preserve final citation validation and replacement on failed/incomplete generation. Worker rollout needs persisted job status and retry semantics. Measure retrieval and generation separately before changing model size or adding ANN indexes; current measurements do not establish vector search as the bottleneck.

Implementation references: [Ollama chat API](https://docs.ollama.com/api/chat) and [HTTPX connection pooling](https://www.python-httpx.org/advanced/clients/).
