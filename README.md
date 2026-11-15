# JEE Squad

A mastery-based, squad-powered weekly study app for JEE Main and Advanced aspirants.

## MVP status
This repository starts with a product specification and a runnable FastAPI backend foundation. The first release is a responsive web app: student experience + admin workflows. Native Android/iOS clients are deferred until the weekly learning loop is validated.

## Quick start
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp ../.env.example .env
uvicorn app.main:app --reload
```
Open `http://localhost:8000/docs`.

Local development defaults to SQLite. Set `DATABASE_URL` to PostgreSQL for staging/production. Do not use SQLite for production multi-user workloads.

## Repository layout
- `docs/PRODUCT_SPEC.md` — product rules, UX, architecture, business model, pilot and roadmap.
- `backend/app/` — FastAPI API, SQLAlchemy models and progression logic.
- `content/sample_questions.csv` — original sample questions.
- `.env.example` — local configuration template.

## Non-negotiable rules
- Daily test: exactly 7 unseen questions; pass at 5/7.
- Daily mix: 3 easy, 3 medium, 1 hard.
- Saturday: revision only; no test.
- Sunday: 25-question weekly exam; pass at 20/25.
- Failed topic repeats with a fresh set. Never recycle a question for that learner/topic.
- No public leaderboard, open DMs, profile photos, or public feed.
- Commitment deposit is disabled by default and excluded from the MVP.

## Safety and content
Only original or properly licensed questions may be uploaded. Guardian consent, data minimisation, report/block, moderation and no open direct messaging are launch requirements. The included OTP endpoint is explicitly a development stub, not production authentication.
