# FAiN — Progress Map

**Platform:** Web (Next.js frontend + FastAPI backend)
**Tech Stack:** Python/FastAPI, Next.js/React, PostgreSQL, Redis, Celery, FFmpeg, Anthropic Claude, OpenAI Whisper
**GitHub:** TBD
**Orchestration File:** backend/main.py
**Last Updated:** 2026-05-16

---

## Phases

### Phase 1 — Trend Predictor
- [ ] Component: trend_fetcher — Polls YouTube Data API for trending videos, hashtags, audio
- [ ] Component: trend_analyzer — Scores and ranks fetched trends; predicts 48–72h peak window

### Phase 2 — YouTube Channel Automation
- [ ] Component: script_generator — Calls Anthropic Claude to produce a monetizable script from trend data
- [ ] Component: clip_assembler — FFmpeg pipeline: selects footage, adds voiceover, subtitles, music
- [ ] Component: upload_manager — Authenticates via OAuth and uploads finished video to YouTube
- [ ] Component: job_queue — Celery + Redis: schedules and tracks async jobs across all components

### Phase 3 — Frontend
- [ ] Component: dashboard — Main UI: trend feed, job status, channel settings
- [ ] Component: auth_ui — Google OAuth login / channel connect flow

---

## Known Issues / Blockers
- None

## Completed Phases
(move completed phases here)
