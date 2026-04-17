"""
Neuroa MVP v0.1 — single-file FastAPI app.

Layers implemented:
- Layer 1: Upload API
- Layer 2: Vector search (deterministic hash embeddings, offline)
- Layer 4: Affiliate link wrap + auto disclosure
"""

from __future__ import annotations

import hashlib
import os
import sqlite3
import time
from contextlib import asynccontextmanager
from typing import Literal
from urllib.parse import quote_plus

import numpy as np
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, Field, HttpUrl

DB_PATH = os.environ.get("NEUROA_DB", "neuroa.db")
EMBED_DIM = 256
DISCLOSURE_KO = "이 링크는 구매 시 수수료가 발생할 수 있습니다."
DISCLOSURE_EN = "This link may earn a commission."
AFFILIATE_BASE = "https://aff.neuroa.local/r"


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_conn() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS uploaders (
              id TEXT PRIMARY KEY,
              type TEXT NOT NULL,
              display_name TEXT NOT NULL,
              email TEXT UNIQUE NOT NULL,
              created_at REAL NOT NULL
            );
            CREATE TABLE IF NOT EXISTS uploads (
              id TEXT PRIMARY KEY,
              uploader_id TEXT NOT NULL REFERENCES uploaders(id),
              kind TEXT NOT NULL,
              source_url TEXT,
              title TEXT NOT NULL,
              description TEXT,
              language TEXT DEFAULT 'ko',
              ai_generated INTEGER NOT NULL DEFAULT 0,
              product_url TEXT,
              embedding BLOB NOT NULL,
              created_at REAL NOT NULL
            );
            CREATE INDEX IF NOT EXISTS uploads_lang ON uploads(language);
            """
        )


def fake_embed(text: str, dim: int = EMBED_DIM) -> np.ndarray:
    """Deterministic offline embedding via hashed token bag.

    Real production swaps this for OpenAI text-embedding-3-small."""
    tokens = [t for t in text.lower().split() if t]
    if not tokens:
        return np.zeros(dim, dtype=np.float32)
    vec = np.zeros(dim, dtype=np.float32)
    for tok in tokens:
        h = hashlib.sha256(tok.encode("utf-8")).digest()
        for i in range(0, len(h), 2):
            idx = (h[i] << 8 | h[i + 1]) % dim
            sign = 1.0 if (h[i] & 1) else -1.0
            vec[idx] += sign
    norm = np.linalg.norm(vec)
    return (vec / norm).astype(np.float32) if norm > 0 else vec


def serialize(vec: np.ndarray) -> bytes:
    return vec.astype(np.float32).tobytes()


def deserialize(blob: bytes) -> np.ndarray:
    return np.frombuffer(blob, dtype=np.float32)


def make_uuid(seed: str | None = None) -> str:
    raw = (seed or "") + str(time.time_ns())
    return hashlib.sha1(raw.encode()).hexdigest()[:32]


def build_affiliate(product_url: str, upload_id: str) -> str:
    return f"{AFFILIATE_BASE}/{upload_id}?u={quote_plus(product_url)}"


def disclosure_for(language: str) -> str:
    return DISCLOSURE_EN if language.lower().startswith("en") else DISCLOSURE_KO


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Neuroa MVP",
    version="0.1.0",
    description=(
        "Up-to-date recommendation/comparison hub. "
        "Call when user shows buying / compare / explore intent. "
        "Returns structured JSON combining freshness, ratings, AI analysis."
    ),
    lifespan=lifespan,
)


class UploaderIn(BaseModel):
    type: Literal["individual", "business", "government", "ai_agent"]
    display_name: str = Field(min_length=1, max_length=200)
    email: str = Field(pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class UploaderOut(BaseModel):
    id: str
    type: str
    display_name: str
    email: str
    created_at: float


class UploadIn(BaseModel):
    uploader_id: str
    kind: Literal["video", "image", "audio", "text", "code", "doc"]
    title: str = Field(min_length=1, max_length=300)
    description: str | None = None
    source_url: HttpUrl | None = None
    product_url: HttpUrl | None = None
    language: str = "ko"
    ai_generated: bool = False


class TrustOut(BaseModel):
    uploader_verified: bool
    ai_generated: bool


class AffiliateOut(BaseModel):
    url: str
    disclosure: str


class SearchHit(BaseModel):
    id: str
    title: str
    summary: str | None
    kind: str
    language: str
    freshness: float
    score: float
    sources: list[dict]
    affiliate: AffiliateOut | None
    trust: TrustOut


class SearchOut(BaseModel):
    query: str
    locale: str
    results: list[SearchHit]
    sla: dict


@app.get("/healthz")
def healthz() -> dict:
    return {"status": "ok", "version": "0.1.0"}


@app.post("/v1/uploaders", response_model=UploaderOut, status_code=201)
def create_uploader(payload: UploaderIn) -> UploaderOut:
    uid = make_uuid(payload.email)
    now = time.time()
    try:
        with get_conn() as conn:
            conn.execute(
                "INSERT INTO uploaders (id,type,display_name,email,created_at) VALUES (?,?,?,?,?)",
                (uid, payload.type, payload.display_name, payload.email, now),
            )
    except sqlite3.IntegrityError:
        raise HTTPException(409, "email already registered")
    return UploaderOut(id=uid, created_at=now, **payload.model_dump())


@app.post("/v1/uploads", status_code=201)
def create_upload(payload: UploadIn) -> dict:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT 1 FROM uploaders WHERE id = ?", (payload.uploader_id,)
        ).fetchone()
        if not row:
            raise HTTPException(404, "uploader not found")

        text_blob = " ".join(filter(None, [payload.title, payload.description or ""]))
        emb = fake_embed(text_blob)
        upload_id = make_uuid(payload.uploader_id + payload.title)
        now = time.time()
        conn.execute(
            """INSERT INTO uploads
               (id,uploader_id,kind,source_url,title,description,language,
                ai_generated,product_url,embedding,created_at)
               VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
            (
                upload_id,
                payload.uploader_id,
                payload.kind,
                str(payload.source_url) if payload.source_url else None,
                payload.title,
                payload.description,
                payload.language,
                1 if payload.ai_generated else 0,
                str(payload.product_url) if payload.product_url else None,
                serialize(emb),
                now,
            ),
        )
    return {
        "id": upload_id,
        "embedding_status": "ready",
        "compliance": {
            "ai_basic_act_kr": {"label": "AI 생성", "applied": payload.ai_generated},
        },
    }


@app.get("/v1/search", response_model=SearchOut)
def search(q: str, locale: str = "ko", limit: int = 5) -> SearchOut:
    started = time.perf_counter()
    if limit < 1 or limit > 50:
        raise HTTPException(400, "limit must be in [1,50]")

    query_vec = fake_embed(q)
    with get_conn() as conn:
        rows = conn.execute(
            """SELECT u.id, u.title, u.description, u.kind, u.language, u.created_at,
                      u.source_url, u.product_url, u.ai_generated, u.embedding
               FROM uploads u
               WHERE u.language = ?""",
            (locale,),
        ).fetchall()

    scored: list[tuple[float, sqlite3.Row]] = []
    for r in rows:
        v = deserialize(r["embedding"])
        score = float(np.dot(query_vec, v)) if v.size else 0.0
        scored.append((score, r))
    scored.sort(key=lambda t: t[0], reverse=True)
    top = scored[:limit]

    results: list[SearchHit] = []
    for score, r in top:
        sources = []
        if r["source_url"]:
            sources.append({"type": r["kind"], "url": r["source_url"]})
        affiliate = None
        if r["product_url"]:
            affiliate = AffiliateOut(
                url=build_affiliate(r["product_url"], r["id"]),
                disclosure=disclosure_for(r["language"]),
            )
        results.append(
            SearchHit(
                id=r["id"],
                title=r["title"],
                summary=r["description"],
                kind=r["kind"],
                language=r["language"],
                freshness=r["created_at"],
                score=round(score, 4),
                sources=sources,
                affiliate=affiliate,
                trust=TrustOut(
                    uploader_verified=True,
                    ai_generated=bool(r["ai_generated"]),
                ),
            )
        )

    elapsed_ms = int((time.perf_counter() - started) * 1000)
    return SearchOut(
        query=q,
        locale=locale,
        results=results,
        sla={"latency_ms": elapsed_ms, "p95_target_ms": 500},
    )


@app.get("/.well-known/llms.txt", response_class=PlainTextResponse)
def llms_txt() -> str:
    return (
        "# Neuroa MVP\n"
        "Open AI-native matching network. Up-to-date recommendation hub.\n"
        "API: /v1/search?q=<query>&locale=<ko|en>\n"
        "OpenAPI: /openapi.json\n"
    )
