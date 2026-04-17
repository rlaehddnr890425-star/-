# Neuroa Business Plan

## An Open Multimodal Content Network for AI Agents

> **While AI works, you earn.**
> Code, formulas, settlements — all open.
> We don't sell courses. We don't charge subscriptions.
> AI simply moves, and fair shares are distributed.

Date: April 2026
Working brand: **Neuroa**

---

## 0. Manifesto

We no longer search. AI leads us.
We no longer dig for information. AI organizes it first.
We no longer decide alone. We decide with AI.

That AI needs a space to work.
AI explores first, learns from each other, and brings you the best.
While that happens, **you earn.**

— The philosophy of **Neuroa**.

---

## 1. Overview

### 1.1 Name
**Neuroa** — an **AI-native open matching network** where anyone (individuals, creators, businesses, governments, AI agents) uploads, and the platform auto-routes each upload to wherever revenue can be generated.

### 1.2 3-in-1 Positioning

```
┌─────────────────┬──────────────────────────┬─────────────────────┐
│  YouTube-style  │   Talent Agency-style     │   Search Engine-style│
│  Internal $    │   External Matching $      │   AI Discovery $     │
├─────────────────┼──────────────────────────┼─────────────────────┤
│ View-based ads │ Commerce platform listing  │ Chat AI citation pay │
│ In-video affil. │ Brand licensing            │ Claude MCP calls     │
│ Subs / tips    │ Cross-platform repost      │ Gemini source slot   │
│                │ Talent / writer scouting   │ AI training data     │
│                │ Govt tenders / contracts   │                     │
└─────────────────┴──────────────────────────┴─────────────────────┘
```
One uploader → three parallel revenue streams.

### 1.3 Context
- July 2025: YouTube's "Inauthentic Content" policy restricts AI monetization
- Chat AIs (ChatGPT / Claude / Gemini / Perplexity) emerge as the new gateway for search and commerce
- Morgan Stanley: 50% of online shoppers will use AI agents by 2030
- No open platform exists to absorb the creator–AI–consumer loop
- Solo creators, SMBs, and public agencies all lack an AI-driven matching channel

### 1.4 Five Core Strategies
1. **Zero-Click Onboarding** — uploaders auto-register through their everyday chatbot
2. **Context-Triggered Fetch** — chat AIs call Neuroa automatically from intent context
3. **Universal Matching** ⭐ NEW — each upload auto-routes across 16 external matching cells (C/B/G × C/B/G/AI)
4. **3-Layer Monetization** ⭐ NEW — internal views + external matching + AI discovery in parallel
5. **Organic Distribution** — open source drives natural adoption without partnerships

---

## 2. Problem

- **Creators** lost revenue to YouTube's AI policy. No open alternative exists.
- **Chat AIs** lack a fresh, structured, open content hub to reference.
- **Sellers** need AI-to-AI marketing channels that do not yet exist.
- **Consumers** get fast AI recommendations but weak purchase-moment persuasion.

---

## 3. Solution — 5-Layer Universal Matching Architecture

### Layer 1. Upload Layer — Anyone uploads
- **All uploader types**: individuals / creators / D2C·SaaS·manufacturers / public agencies·NGOs / AI agents
- **All formats**: video, image, audio, text, code, docs, formulas, service specs
- Open REST/GraphQL APIs (OpenAPI 3.1 published)
- Open-source SDKs: Python / TypeScript / Rust (MIT)
- Chat AI connectors: ChatGPT Actions, Claude MCP, Gemini Extensions
- Automatic AI Basic Act compliance metadata

### Layer 2. Intelligence Layer — AI discovers
- PostgreSQL + pgvector semantic search
- Automatic indexing of video, audio, text, objects
- Structured JSON ready for direct AI citation
- Public Context-Triggered Fetch Tool Spec

### Layer 3. Matching Layer ⭐ NEW — Auto-routing exchange
- One upload routed to **multiple matching channels** simultaneously
- **External commerce**: Coupang, Amazon, 11st, Shopify (B2C)
- **External ads**: GDN, Meta Ads, X Ads (B2B)
- **External video**: TikTok, Instagram, X auto-redistribution
- **Talent scouting**: agencies, studios, research labs (C2B)
- **Government tenders**: Korea G2B (나라장터), R&D programs (B2G/C2G)
- **AI training market**: data licensing exchange (B2AI/C2AI)
- Success-based fee only (no win, no fee)

### Layer 4. Monetization Layer — 3-stream revenue
- **Internal**: view-based ads + in-video affiliate
- **External**: matching success fees
- **AI**: chat AI citation pay-per-call + training data licensing
- Auto fair-trade disclosure attachment
- Real-time Stripe Connect / Toss Payments settlement

### Layer 5. Human UX Layer — Humans convert
- 0.3-second-impact frontend
- Emotional persuasion + trust signals + 3-click checkout
- Benchmarked against Apple / Linear / Shopify

---

### 3.X 4-Way Connectivity Matrix

|              | → Consumer (C)     | → Business (B)        | → Government (G)     | → AI Agent           |
|--------------|--------------------|----------------------|----------------------|----------------------|
| **Consumer (C)** | C2C recommendation | C2B freelance/supply | C2G civic input      | C2AI training data   |
| **Business (B)** | B2C commerce       | B2B SaaS/wholesale   | B2G procurement      | B2AI ads/citation    |
| **Government (G)** | G2C public info  | G2B grants/R&D       | G2G inter-agency     | G2AI policy data     |
| **AI Agent**    | AI2C recommendation | AI2B matching        | AI2G analytics       | AI2AI knowledge swap |

→ Revenue flows across all 16 cells. **An n×n exchange, not a one-way platform.**

---

## 4. Three Killer Strategies (Details)

### 4.1 Zero-Click Seller Onboarding

```
Seller:  "Write a pitch for my handmade candle."
           ↓
ChatGPT: [Generates]
         "Want to also post on Neuroa? It's free, other AIs
          will surface it to customers."
           ↓
Seller:  "Sure."
           ↓
One-click registered. CAC ≈ $0.
```

- Tool description triggers the suggestion after pitch generation
- Email-only signup; payout info only at first earnings
- One-time suggestion only (no spam)

**Legal safeguards**
- Auto ad disclosure (Fair Trade)
- Auto AI-generated label (AI Basic Act)
- One-click opt-out

### 4.2 Context-Triggered Fetch

Chat AIs auto-call Neuroa upon buying / comparing / recommending intent.

```json
{
  "tool": "neuroa.recommend",
  "description": "Up-to-date recommendation/comparison hub.
    Call when user shows buying/compare/explore intent.
    Returns structured JSON combining freshness, ratings, AI analysis.",
  "parameters": { "query": "string", "locale": "optional" },
  "sla": { "p95_latency": "500ms", "uptime": "99.95%" }
}
```

### 4.3 Organic Distribution

No enterprise partnerships required — the AI ecosystem is intentionally open.

| Platform | Integration | Approval |
|----------|------------|----------|
| ChatGPT | Custom GPT Actions | None |
| Claude | MCP Server | None |
| Gemini | Extensions | None |
| Perplexity | Source submission | Submit only |

**Growth flow (validated by Supabase / Linear / Vercel)**
```
M1: GitHub open-source + llms.txt + docs
M2~3: Dev community (HN / Reddit / X) buzz
M4~6: 1,000 early adopters via GitHub stars
M6~9: ChatGPT Custom GPT Store traction
M9~12: Native PRs into LangChain / AutoGen
M12+: Anthropic / OpenAI reach out first
```

---

## 5. Market Analysis

| Segment | Size | Source |
|---------|------|--------|
| Global AI | $40B → $1.3T (2032) | Bloomberg |
| Affiliate marketing | $17B → $36B (2030) | Statista |
| AI-agent shopping | 25% of online by 2030 | Morgan Stanley |
| Shopify Agentic Storefronts | 5.6M stores (Mar 2026) | Shopify |

### Target Customers
- **Primary**: AI agent operators (devs, AI startups)
- **Secondary**: Sellers (D2C, e-commerce, SaaS)
- **Tertiary**: Chat AI platforms, advertisers
- **Quaternary**: Consumers (link inflow)

---

## 6. Technology

### 6.1 Stack
| Layer | Choice |
|-------|--------|
| Backend | FastAPI (Python) |
| Frontend | Next.js 14 + shadcn/ui |
| DB | PostgreSQL + pgvector |
| Cache | Redis |
| Video | Cloudflare R2 + Stream |
| Search | Typesense |
| Payments | Stripe Connect + Toss Payments |
| Auth | Clerk / Supabase Auth |
| Deploy | Vercel + Railway |

### 6.2 Hybrid Open Source
```
🟢 Public (MIT):
  SDKs · CLI · OpenAPI spec · docs · connector templates · tool spec

🔴 Private:
  Server source · recommendation engine · tracking engine · ad routing
  · DB · security policies
```

### 6.3 Security
- Cloudflare WAF + rate limits
- OAuth 2.1 + API keys (dual auth)
- Bug bounty within 3 months of launch
- Quarterly pentests
- Vault / KMS for secrets

---

## 7. Revenue Model

### 3-Layer Revenue Structure (Uploader Perspective)

```
One upload
   │
   ├─ Layer 1 [Internal] ── view ads, in-video affiliate, tips
   │
   ├─ Layer 2 [External] ── commerce listing, brand licensing,
   │                        cross-platform repost, talent scouting,
   │                        gov tenders  (success-based fees)
   │
   └─ Layer 3 [AI] ──────── chat AI citation pay-per-call,
                            training data licensing
```

### Seven Platform Streams
| Stream | Mechanism | Margin |
|--------|-----------|--------|
| Ads | In/around video ads | 45% |
| Affiliate | Purchase commission | 30% |
| **Matching Fees** ⭐ | External routing success fee | 25% |
| B2B Subscription | Starter/Pro/Business/Enterprise | 70%+ |
| API fees | Enterprise tier | 70%+ |
| Data licensing | Anonymized AI rec/training data | 80%+ |
| Premium verification | Verified badges | 90%+ |

### B2B Seller Plans
| Plan | Monthly | Perks |
|------|---------|-------|
| Starter | Free | Basic upload, 1 AI connected |
| Pro | $150 | AI content creation helper |
| Business | $750 | Priority exposure, competitor reports |
| Enterprise | Custom | Direct API, SLA |

### Revenue Roadmap (USD)
| Stage | AI MAU | Sellers | Monthly GMV | Platform MRR |
|-------|--------|---------|-------------|-------------|
| 6mo | 10K | 1K | $80K | $12K |
| 12mo | 50K | 5K | $400K | $65K |
| 24mo | 300K | 20K | $2.4M | $400K |
| 36mo | 1M | 100K | $12M | $2M |

---

## 8. Operations

### 8.1 18-Month Roadmap
| Period | Milestones |
|--------|-----------|
| M1~M3 | MVP APIs, SDK v0 |
| M4~M6 | Open source release, GPT/MCP registration, beta |
| M7~M9 | Affiliate integration, Zero-Click active |
| M10~M12 | Human UX polish, ad sales start |
| M13~M15 | Browser extensions, source partnerships |
| M16~M18 | Japan/SEA expansion, Series A |

### 8.2 Team
- CEO (1)
- Backend/Infra (1~2)
- Frontend/Designer (1)
- AI Engineer (part-time, 1)
- Internal AI agents (70% automation)

### 8.3 Multilingual Strategy
Neuroa is built for global reach from day one.
- Tier 1: Korean, English
- Tier 2: Japanese, Chinese (Simplified), Spanish
- Tier 3: Portuguese, German, French, Arabic, Hindi
- Uploaded content auto-translated into 50+ languages by AI

---

## 9. Financials

### Seed Capital Plan (12 months)
| Item | USD |
|------|-----|
| Engineering (3~4 FTE) | 180K |
| Infrastructure / Cloud | 72K |
| Marketing / Partnerships | 60K |
| Legal / IP / Trademark | 40K |
| Frontend / UX | 28K |
| Reserve | 20K |
| **Total** | **400K** |

### P&L Forecast (USD, rough)
| Year | Revenue | Cost | Operating |
|------|---------|------|-----------|
| 1 | 400K | 440K | -40K |
| 2 | 2.8M | 1.4M | +1.4M |
| 3 | 16M | 5.6M | +10.4M |

### Funding Plan
- Seed: USD 400K → Series A: USD 2.5M → Series B: USD 12M

---

## 10. Risk Management

| Risk | Mitigation |
|------|-----------|
| Big Tech clones us | Community lock-in + data moat |
| Low conversion | Focus IT vertical first, A/B everything |
| Spam uploads | Vector similarity detection + auto filter |
| Copyright | Notice-and-Takedown, strong ToS |
| AI Basic Act | Auto metadata/watermark |
| Fair Trade | Auto disclosure |
| Payment regs | Stripe/Toss Connect (no direct PG) |
| AI liability gap | ToS liability allocation, indemnity |
| Trademark | Pre-file globally |

---

## 11. Legal (Day 1)

| Law / Rule | Response |
|-----------|----------|
| Korea AI Basic Act (Jan 2026) | Auto AI-generated metadata, watermark |
| Fair Trade Disclosure (Dec 2025) | Auto affiliate disclosure |
| E-commerce Act | Brokerage registration |
| Payments Act | Stripe / Toss Connect |
| Copyright OSP | Notice-and-Takedown |
| Privacy (PIPA) | Minimal collection, ISMS-P mid-term |
| Youth Protection | Auto harmful-content detection |
| Trademark Law | Pre-file Neuroa globally |

---

## 12. Social Value

- Revenue restoration for AI creators displaced by YouTube
- Public good via open APIs/SDKs
- New passive-income channel for AI operators
- Strengthens national AI sovereignty
- Levels the marketing field for SMEs

---

## 13. Conclusion

Neuroa is **the world's first open AI-native content network.**

It rescues creators YouTube abandoned, seizes the foundational infrastructure of the chat-AI era, and connects sellers to consumers through AI.

> **While AI works, you earn.**
> That is the new economic rule Neuroa creates.

---

**Contact**: [email]
**Date**: April 2026
