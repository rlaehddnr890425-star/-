"""Smoke test for the Neuroa MVP.

Runs against an already-started uvicorn (host/port via env)."""

from __future__ import annotations

import os
import sys

import httpx

BASE = os.environ.get("NEUROA_BASE", "http://127.0.0.1:8000")


def main() -> int:
    client = httpx.Client(base_url=BASE, timeout=10.0)

    health = client.get("/healthz").json()
    assert health["status"] == "ok", health
    print("✓ healthz")

    uploader = client.post(
        "/v1/uploaders",
        json={
            "type": "individual",
            "display_name": "Demo Uploader",
            "email": f"demo+{os.getpid()}@example.com",
        },
    )
    assert uploader.status_code == 201, uploader.text
    uid = uploader.json()["id"]
    print(f"✓ create uploader → {uid[:8]}…")

    fixtures = [
        {
            "title": "Best portable monitors 2026",
            "description": "Comparison of ASUS ROG, LG Gram view, MSI Modern.",
            "language": "en",
            "ai_generated": True,
            "product_url": "https://example.com/product/asus-rog",
        },
        {
            "title": "MacBook Pro M5 review",
            "description": "Battery life and thermals deep dive.",
            "language": "en",
            "ai_generated": False,
            "product_url": "https://example.com/product/mbp",
        },
        {
            "title": "노트북 추천 2026 한국어",
            "description": "휴대성·성능·가격 3가지 기준 비교.",
            "language": "ko",
            "ai_generated": True,
            "product_url": "https://example.com/product/lg-gram",
        },
    ]
    for f in fixtures:
        r = client.post(
            "/v1/uploads",
            json={"uploader_id": uid, "kind": "video", **f},
        )
        assert r.status_code == 201, r.text
    print(f"✓ created {len(fixtures)} uploads")

    en = client.get("/v1/search", params={"q": "portable monitor", "locale": "en"}).json()
    assert en["results"], en
    top = en["results"][0]
    assert "portable" in top["title"].lower(), top
    assert top["affiliate"]["disclosure"].startswith("This link"), top
    print(f"✓ EN search top hit: {top['title']!r} (score={top['score']})")

    ko = client.get("/v1/search", params={"q": "노트북 추천", "locale": "ko"}).json()
    assert ko["results"], ko
    top_ko = ko["results"][0]
    assert "노트북" in top_ko["title"], top_ko
    assert "수수료" in top_ko["affiliate"]["disclosure"], top_ko
    print(f"✓ KO search top hit: {top_ko['title']!r} (score={top_ko['score']})")

    llms = client.get("/.well-known/llms.txt").text
    assert "Neuroa MVP" in llms
    print("✓ llms.txt served")

    spec = client.get("/openapi.json").json()
    assert "/v1/search" in spec["paths"], list(spec["paths"])
    print("✓ OpenAPI spec served")

    print("\nALL CHECKS PASSED ✅")
    return 0


if __name__ == "__main__":
    sys.exit(main())
