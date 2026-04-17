# Neuroa MVP v0.1

Single-file FastAPI MVP for the Neuroa open matching network.

## Scope (Thin Slice)

- Layer 1: Upload API (uploaders + uploads)
- Layer 2: Vector search (deterministic offline embeddings, hash-based)
- Layer 4: Affiliate URL wrapping + auto disclosure (KR / EN)

Out of scope (Phase 2): Layer 3 external matching, Layer 5 frontend,
Stripe Connect payouts, real OAuth, real embeddings via OpenAI.

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Server: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
- OpenAPI:    http://127.0.0.1:8000/openapi.json
- llms.txt:   http://127.0.0.1:8000/.well-known/llms.txt

## Smoke test

In another terminal, with the server running:

```bash
python test_smoke.py
```

## Quick demo

```bash
# 1. register an uploader
curl -X POST http://127.0.0.1:8000/v1/uploaders \
  -H "Content-Type: application/json" \
  -d '{"type":"individual","display_name":"Alice","email":"alice@example.com"}'
# → {"id":"<uploader_id>", ...}

# 2. upload an item (use the id above)
curl -X POST http://127.0.0.1:8000/v1/uploads \
  -H "Content-Type: application/json" \
  -d '{"uploader_id":"<uploader_id>","kind":"video",
       "title":"Best portable monitors 2026",
       "description":"comparison",
       "language":"en","ai_generated":true,
       "product_url":"https://example.com/p/1"}'

# 3. search
curl 'http://127.0.0.1:8000/v1/search?q=portable+monitor&locale=en'
```

## File layout

```
mvp/
├── main.py            # FastAPI app
├── requirements.txt   # deps (fastapi, uvicorn, pydantic, numpy, httpx)
├── test_smoke.py      # end-to-end check (run after `uvicorn main:app`)
└── README.md
```

## Production swap-outs

| MVP | Production |
|-----|-----------|
| SQLite + BLOB embeddings | PostgreSQL + pgvector (HNSW) |
| Hash-based fake embeddings | OpenAI text-embedding-3-small |
| In-process search | Redis result cache + worker queue |
| No auth | Supabase Auth + API keys |
| Affiliate stub URL | Coupang Partners API |
| Local SQLite file | Railway Postgres + R2 storage |
