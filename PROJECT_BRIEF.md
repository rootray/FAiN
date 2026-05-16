# FAiN — Project Brief

**Date:** 2026-05-16
**Status:** Signed off — 2026-05-16

---

## What It Is

FAiN is a SaaS platform and white-label API for content creators and agencies.
It automates the full short-form content lifecycle: trend detection → script generation → clip
assembly → publishing → revenue tracking.

---

## Who It Is For

| User Type | Description |
|---|---|
| Solo faceless creator | One person running 1–3 YouTube/TikTok channels with no team |
| Small creator agency | Team managing multiple creator accounts; needs multi-user support |
| The builder | Personal use on own channels; productized after validation |
| SaaS white-label partners | Platforms (e.g. Canva, Hootsuite) embedding the repurposing SDK |

---

## Features (Full Vision)

| # | Feature | Description |
|---|---|---|
| 1 | **Shorts/Reels Trend Predictor** | Analyzes emerging audio, hashtags, and formats 48–72h before peak across TikTok/Instagram/YouTube. Auto-generates templated clips optimized per trend. |
| 2 | **AI Script Ghostwriter** | Ingests Reddit threads, forum posts, or user-submitted stories. Auto-generates monetizable scripts with royalty tracking for original submitters. Feeds into YouTube automation. |
| 3 | **Revenue Stack Dashboard** | Single pane showing affiliate commissions, sponsorship ROI, product sales, and ad revenue per clip. Surfaces what content actually makes money vs. vanity metrics. |
| 4 | **Faceless YouTube Channel Automation** | Takes short-form clips, auto-assembles into compilations with AI voiceover, subtitles, and licensed music. Uploads 3–4x per week hands-free. |
| 5 | **Creator Collab Network** | Connects creators in the same niche. Auto-extracts quotable moments from each other's content, generates tagged cross-promotional clips. |
| 6 | **Engagement Spike Alerter** | Monitors posted content in real-time. When a post hits trending engagement, extracts best 15–60s clip and suggests optimal cross-platform posting windows. |
| 7 | **Short-Form Repurposing API** | White-label SDK for SaaS platforms. Lets their users auto-convert long-form content without leaving the host tool. |

---

## MVP Build Order

1. **Trend Predictor** — highest differentiation, anchors the platform's core value
2. **YouTube Channel Automation** — most direct path to hands-free revenue for creators

All other features are post-MVP.

---

## Explicit Non-Goals (v1)

- TikTok and Instagram API integration (architecture supports it; not built until v2)
- Multi-user roles and agency billing (post-MVP)
- White-label SDK (built after core features are validated)
- Mobile app

---

## Tech Stack

### Frontend
- **Framework:** Next.js (React)
- **Hosting:** Vercel (free tier; custom domain pointed via DNS)
- **Why:** SSR + API routes in one repo, ideal for SaaS dashboards, handles SSL and deployments automatically

### Backend
- **Framework:** Python / FastAPI
- **OS:** Rocky Linux (VMware VM for dev → cloud VPS for production)
- **Why:** Best-in-class for AI/ML pipelines, video processing, and async job queues

### Data & Queue
- **Database:** PostgreSQL
- **Cache / Queue broker:** Redis
- **Task queue:** Celery (async video processing and AI jobs)

### Video Processing
- **Tool:** FFmpeg (clip assembly, subtitles, encoding)

### Storage
- **Dev:** Local filesystem on Rocky Linux VM
- **Prod:** Cloud object storage (S3-compatible — AWS S3 or Cloudflare R2)

### AI / Content
- **Script generation:** Anthropic Claude (primary)
- **Transcription / voiceover:** OpenAI Whisper

### External APIs
| API | Purpose | Status |
|---|---|---|
| YouTube Data API v3 | Trend detection, video upload, analytics | Active (API key + OAuth 2.0 configured) |
| TikTok API | Trend data, hashtag analytics | Future (v2) |
| Instagram Graph API | Trend data, publishing | Future (v2) |

### Payments
- **Stripe** — subscription billing (post-MVP)

---

## Infrastructure & Environments

| Environment | Frontend | Backend | API Key Restriction |
|---|---|---|---|
| Development | localhost (Next.js dev server) | Rocky Linux VM (VMware, local) | None |
| Production | Vercel + custom domain | Cloud VPS (Rocky Linux) | VPS public IP |

- Frontend domain: `yourdomain.com` (to be confirmed)
- Backend API domain: `api.yourdomain.com`
- OAuth redirect URIs: `http://localhost:8000/auth/google/callback` (dev), `https://api.yourdomain.com/auth/google/callback` (prod)

---

## Credentials & Secrets (never committed to git)

| Variable | Description |
|---|---|
| `YOUTUBE_API_KEY` | YouTube Data API key (dev — no restriction) |
| `GOOGLE_CLIENT_ID` | OAuth 2.0 client ID |
| `GOOGLE_CLIENT_SECRET` | OAuth 2.0 client secret |
| `ANTHROPIC_API_KEY` | Anthropic Claude API key |
| `DATABASE_URL` | PostgreSQL connection string |
| `REDIS_URL` | Redis connection string |

All variables documented in `.env.example`. `.env` is always in `.gitignore`.

---

## Sign-off

- [x] User has reviewed and approved this brief — 2026-05-16
