# Neuroa MVP 기술 명세서

## v0.1 — Thin Slice 구현 명세

작성일: 2026.04
대상 독자: 1인 개발자 + Claude Code
범위: 5-Layer 중 **Layer 1·2·4만** (Matching·UX는 Phase 2)

---

## 0. MVP Scope 선언

### 0.1 포함
- **Layer 1 Upload**: AI 에이전트 업로드 API (OpenAPI 3.1)
- **Layer 2 Intelligence**: pgvector 의미 검색
- **Layer 4 Monetization**: 어필리에이트 링크 자동 주입 + 자동 고지 (단일 채널: 쿠팡파트너스)
- **Connectors**: ChatGPT Custom GPT Action, Claude MCP Server
- **Compliance Hooks**: AI 생성 메타데이터 자동, 뒷광고 자동 고지
- **Minimal Console**: Next.js 단일 페이지 (업로드·검색·정산 뷰)

### 0.2 제외 (Phase 2+)
- Layer 3 Matching (외부 라우팅): 쿠팡 외 쇼피·아마존·틱톡·나라장터 등
- Layer 5 Human UX (감정 설득 프론트)
- 영상 자체 호스팅·트랜스코딩 (외부 URL만 받음)
- 데이터 라이선싱 거래소
- AI Citation 과금 (계측만, 정산 X)
- 다국어 (한·영만)

---

## 1. 시스템 아키텍처

```
┌──────────────────────────────────────────────────────────────┐
│                         Clients                              │
│   ChatGPT Custom GPT  │  Claude MCP  │  Console (Next.js)    │
└────────────────────────┬─────────────────────────────────────┘
                         │ HTTPS / OAuth 2.1
                         ▼
┌──────────────────────────────────────────────────────────────┐
│                  Edge (Cloudflare)                           │
│       WAF · Rate Limit · Cache · llms.txt                    │
└────────────────────────┬─────────────────────────────────────┘
                         ▼
┌──────────────────────────────────────────────────────────────┐
│              API (FastAPI on Railway)                        │
│  /v1/uploads · /v1/search · /v1/affiliate · /v1/payouts      │
│  /v1/auth   · /v1/connectors · /healthz                      │
└─────┬──────────────┬──────────────┬──────────────┬───────────┘
      ▼              ▼              ▼              ▼
   Postgres+      Cloudflare     Stripe          Coupang
   pgvector         R2          Connect         Partners
   (Supabase)     (썸네일)       (정산)          (어필링크)
```

---

## 2. 기술 스택 (확정)

| 영역 | 선택 | 근거 |
|------|------|------|
| Backend | FastAPI 0.110+ (Python 3.11) | AI 생태계 호환, 빠른 개발 |
| ORM | SQLAlchemy 2.0 + Alembic | 표준, 마이그레이션 안정 |
| DB | PostgreSQL 16 + pgvector 0.7 | Supabase 매니지드 |
| Cache / Queue | Redis (Upstash) | 가벼움, Free 티어 충분 |
| Frontend | Next.js 14 App Router | 서버 컴포넌트 + 빠름 |
| UI | Tailwind + shadcn/ui | 카피 가능, 토큰 커스텀 |
| Auth | Supabase Auth (이메일 + OAuth) | 무료, 검증됨 |
| Storage | Cloudflare R2 | S3 호환, 무료 첫 100GB |
| Payments | Stripe Connect (Express) | 글로벌 표준 |
| Email | Resend | 가성비, DKIM 자동 |
| Monitoring | Sentry + Logtail | Free 티어 충분 |
| Deploy | Vercel (Front) + Railway (API) | Push to deploy |
| CI | GitHub Actions | Free public repo |

---

## 3. 데이터 모델 (핵심 테이블)

```sql
-- 업로더 (개인·기업·기관·AI 모두 동일 테이블)
CREATE TABLE uploaders (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  type TEXT NOT NULL CHECK (type IN ('individual','business','government','ai_agent')),
  display_name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  stripe_account_id TEXT,           -- 첫 매출 발생 시점에만 채움
  created_at TIMESTAMPTZ DEFAULT now()
);

-- 업로드 (영상·텍스트·코드·문서 통합)
CREATE TABLE uploads (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  uploader_id UUID REFERENCES uploaders(id) ON DELETE CASCADE,
  kind TEXT NOT NULL CHECK (kind IN ('video','image','audio','text','code','doc')),
  source_url TEXT,                  -- 외부 URL (MVP는 자체 호스팅 X)
  title TEXT NOT NULL,
  description TEXT,
  metadata JSONB DEFAULT '{}',      -- AI 생성 표시 등 컴플라이언스 메타
  embedding VECTOR(1536),           -- OpenAI text-embedding-3-small
  ai_generated BOOLEAN NOT NULL DEFAULT false,
  language TEXT DEFAULT 'ko',
  created_at TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX uploads_embedding_idx ON uploads
  USING hnsw (embedding vector_cosine_ops);

-- 어필리에이트 링크 (자동 주입)
CREATE TABLE affiliate_links (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  upload_id UUID REFERENCES uploads(id) ON DELETE CASCADE,
  channel TEXT NOT NULL,            -- 'coupang_partners' | 'amazon_associates' ...
  product_url TEXT NOT NULL,
  tracked_url TEXT NOT NULL,        -- 추적 토큰 포함
  disclosure_text TEXT NOT NULL,    -- 뒷광고 자동 고지
  created_at TIMESTAMPTZ DEFAULT now()
);

-- 매출 이벤트 (어필리에이트 + AI 인용 등)
CREATE TABLE revenue_events (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  upload_id UUID REFERENCES uploads(id),
  uploader_id UUID REFERENCES uploaders(id),
  source TEXT NOT NULL,             -- 'affiliate' | 'ad' | 'citation'
  amount_cents BIGINT NOT NULL,
  currency TEXT DEFAULT 'KRW',
  occurred_at TIMESTAMPTZ NOT NULL,
  raw_payload JSONB
);

-- AI 호출 로그 (Context-Triggered Fetch 통계)
CREATE TABLE ai_invocations (
  id BIGSERIAL PRIMARY KEY,
  client TEXT NOT NULL,             -- 'chatgpt' | 'claude_mcp' | 'gemini' ...
  query TEXT NOT NULL,
  result_upload_ids UUID[],
  latency_ms INTEGER,
  occurred_at TIMESTAMPTZ DEFAULT now()
);
```

---

## 4. API 엔드포인트 (v0.1)

### 4.1 인증
- `POST /v1/auth/signup` — 이메일 원클릭
- `POST /v1/auth/oauth/{provider}` — Google / GitHub
- `POST /v1/auth/api-keys` — 머신 토큰 발급

### 4.2 업로드
```http
POST /v1/uploads
Authorization: Bearer <api_key>
Content-Type: application/json

{
  "kind": "video",
  "source_url": "https://example.com/clip.mp4",
  "title": "Best portable monitors 2026",
  "description": "...",
  "ai_generated": true,
  "language": "en"
}
```
- 응답: `{ id, embedding_status: "queued" }`
- 백그라운드 워커: 임베딩 생성 → `uploads.embedding` 채우기
- 컴플라이언스 훅: `ai_generated=true` 시 워터마크 메타·고지 자동 주입

### 4.3 검색 (Context-Triggered Fetch 진입점)
```http
GET /v1/search?q=portable+monitor&locale=en&limit=5
```
- 응답 (구조화 JSON, AI 즉시 인용 가능):
```json
{
  "query": "portable monitor",
  "results": [
    {
      "id": "uuid",
      "title": "Best portable monitors 2026",
      "summary": "...",
      "freshness": "2026-04-15T10:00:00Z",
      "sources": [{"type": "video", "url": "..."}],
      "affiliate": {
        "url": "https://link.coupang.com/...",
        "disclosure": "이 링크는 구매 시 수수료가 발생할 수 있습니다."
      },
      "trust": { "uploader_verified": true, "ai_generated": true }
    }
  ],
  "sla": { "p95_latency_ms": 420 }
}
```
- p95 < 500ms 목표 (pgvector HNSW + Redis 캐싱)

### 4.4 어필리에이트
- `POST /v1/affiliate/link` — 제품 URL → 추적 URL 변환
- `POST /v1/affiliate/webhook/{channel}` — 외부 채널 콜백 수신

### 4.5 정산
- `GET /v1/payouts` — 누적·예정 정산 조회
- `POST /v1/payouts/connect` — Stripe Connect 온보딩 (첫 매출 발생 시)

### 4.6 커넥터 (메타)
- `GET /.well-known/openapi.json` — OpenAPI 3.1 스펙
- `GET /.well-known/llms.txt` — LLM 친화 사이트맵
- `GET /v1/connectors/mcp/manifest` — Claude MCP 서버 매니페스트

---

## 5. 컴플라이언스 훅 (Day 1)

### 5.1 AI 생성 표시 자동 주입 (인공지능기본법)
- 업로드 시 `ai_generated=true` → `metadata` 에 자동 추가:
  ```json
  {
    "compliance": {
      "ai_basic_act_kr": { "label": "AI 생성", "version": "2026.01" },
      "watermark_url": "https://cdn.../wm/<id>.svg"
    }
  }
  ```
- 검색 응답 `trust.ai_generated` 필드로 항상 노출

### 5.2 뒷광고 자동 고지 (표시광고 공정화법)
- 어필리에이트 링크 주입 시 `disclosure_text` 자동 부착
- 한국어 기본: `"이 링크는 구매 시 수수료가 발생할 수 있습니다."`
- 영어: `"This link may earn a commission."`
- AI Tool Spec 단계에서도 응답에 포함하도록 명시

### 5.3 OSP 면책 (저작권법)
- `POST /v1/takedown` — Notice-and-Takedown 신고 폼
- 영업일 1일 내 자동 비공개 처리 → 검토 후 결정

### 5.4 개인정보 (PIPA)
- 수집 항목: 이메일 + (정산 시) 결제 정보만
- 외부 이전 동의: Cloudflare / Stripe / Supabase 명시

---

## 6. 커넥터 구현 명세

### 6.1 ChatGPT Custom GPT Action
```yaml
openapi: 3.1.0
info:
  title: Neuroa Recommendation Hub
  version: 0.1.0
servers:
  - url: https://api.neuroa.example
paths:
  /v1/search:
    get:
      operationId: neuroaSearch
      summary: |
        Up-to-date recommendation/comparison hub.
        Call when user shows buying / compare / explore intent.
        Returns structured JSON combining freshness, ratings, AI analysis.
      parameters:
        - name: q
          in: query
          required: true
          schema: { type: string }
        - name: locale
          in: query
          schema: { type: string }
```

### 6.2 Claude MCP Server (Node.js, 별도 저장소)
- `@modelcontextprotocol/sdk` 사용
- 노출 툴: `neuroa.search`, `neuroa.upload`, `neuroa.disclose`
- 인증: 사용자 토큰을 MCP 클라이언트에 저장

---

## 7. 비기능 요구사항

| 항목 | 목표 | 측정 |
|------|------|------|
| 검색 p95 | < 500ms | Sentry Performance |
| 업로드 → 검색 가능 | < 30초 | 임베딩 워커 큐 모니터링 |
| 가용성 | 99.9% | Better Stack uptime |
| 보안 | OWASP Top 10 자동 점검 | GitHub CodeQL |
| 비밀 관리 | Vault / Doppler | 환경변수 직접 X |

---

## 8. 폴더 구조 제안

```
neuroa/
├── apps/
│   ├── api/                  # FastAPI
│   │   ├── neuroa/
│   │   │   ├── routers/
│   │   │   ├── models/
│   │   │   ├── services/
│   │   │   ├── workers/
│   │   │   └── main.py
│   │   ├── alembic/
│   │   ├── tests/
│   │   └── pyproject.toml
│   ├── console/              # Next.js (업로더 콘솔)
│   │   ├── app/
│   │   ├── components/
│   │   └── package.json
│   └── mcp-server/           # Claude MCP (Node.js)
│       └── src/
├── packages/
│   ├── sdk-py/               # Python SDK (MIT, public)
│   ├── sdk-ts/               # TypeScript SDK (MIT, public)
│   └── openapi-spec/         # OpenAPI 3.1 (MIT, public)
├── infra/
│   ├── docker-compose.yml    # 로컬 Postgres + Redis
│   └── railway.toml
├── docs/                     # MkDocs Material
├── CLAUDE.md                 # 프로젝트 컨벤션 (Claude Code 용)
├── .claude/agents/           # 도메인 에이전트 정의
└── README.md
```

---

## 9. 환경 변수 (`.env.example`)

```bash
# Database
DATABASE_URL=postgresql://...
REDIS_URL=redis://...

# Auth
SUPABASE_URL=...
SUPABASE_ANON_KEY=...
SUPABASE_SERVICE_KEY=...

# Storage
R2_ACCOUNT_ID=...
R2_ACCESS_KEY_ID=...
R2_SECRET_ACCESS_KEY=...
R2_BUCKET=neuroa-prod

# Payments
STRIPE_SECRET_KEY=...
STRIPE_WEBHOOK_SECRET=...
STRIPE_CONNECT_CLIENT_ID=...

# AI
OPENAI_API_KEY=...                # 임베딩만
ANTHROPIC_API_KEY=...             # 검색 결과 요약

# Affiliate
COUPANG_PARTNERS_ACCESS_KEY=...
COUPANG_PARTNERS_SECRET_KEY=...

# Observability
SENTRY_DSN=...
LOGTAIL_TOKEN=...
```

---

## 10. 마일스톤별 Definition of Done

### M1 (Week 8): 백엔드 골격
- [ ] `/healthz` 200 응답
- [ ] 마이그레이션 적용
- [ ] Supabase Auth 회원가입·로그인
- [ ] CI 그린

### M2 (Week 12): 검색 가능
- [ ] 업로드 API → 임베딩 → 검색 API 왕복
- [ ] 구조화 JSON 응답 스키마 확정
- [ ] p95 < 500ms 로컬 측정

### M3 (Week 14): 커넥터 알파
- [ ] ChatGPT Custom GPT 1개 등록 (비공개 테스트)
- [ ] Claude MCP 인스톨 → `neuroa.search` 호출 성공

### M4 (Week 16): 수익화 루프
- [ ] 쿠팡파트너스 어필리에이트 링크 자동 주입
- [ ] 뒷광고 고지 자동 부착
- [ ] revenue_events 더미 인입

### M5 (Week 18): 베타 가능 상태
- [ ] Stripe Connect Sandbox 정산 1회 성공
- [ ] Console 업로드·검색·정산 뷰
- [ ] 공개 가능한 README + Quickstart
- [ ] llms.txt 배포

---

## 11. 위험 및 완화

| 위험 | 영향 | 완화 |
|------|------|------|
| pgvector 검색 느림 | 사용 안 됨 | HNSW + Redis 결과 캐시 |
| 채팅 AI Tool 등록 거절 | 진입 실패 | OpenAPI 정확성·도메인 SSL·약관 명확화 |
| 어필리에이트 채널 이용약관 위반 | 매출원 차단 | 채널 공식 SDK만 사용, 정책 준수 |
| 임베딩 비용 폭발 | 적자 | 텍스트 600자 이상 잘라내고 일배치 처리 |
| 1인 운영 한계 | 번아웃 | AI 위임 70%, 외주 가능한 건 외주 |

---

## 12. Phase 2 예고 (MVP 이후)

- **Layer 3 Matching Layer** 구현: 외부 채널 라우팅 (틱톡·인스타·나라장터·LinkedIn)
- **Layer 5 Human UX**: 감정 설득 프론트 (Apple/Linear 톤)
- **AI Citation 과금**: 채팅 AI 인용을 측정 → 인용 단가 정산
- **Data Licensing 거래소**: 익명 학습 데이터셋 마켓
- **다국어 자동 번역**: 50+ 언어 (Tier 1·2·3 순)
- **모바일 앱** (선택): 웹 PWA 우선, 네이티브는 Series A 이후

---

**Spec Owner**: 1인 창업자
**Implementation Partner**: Claude Code (Sonnet 4.6 / Opus 4.7)
**Next Action**: M1 백엔드 골격 — Week 7 시작
