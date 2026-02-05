# AI Crypto Advisor

Personalized crypto investor dashboard with onboarding, AI insight, and feedback.

## Stack
- Frontend: React + Vite
- Backend: FastAPI + SQLite

## Features
- Email/password auth
- Onboarding quiz saved to DB
- Daily dashboard: news, prices, AI insight, meme
- Feedback (thumbs up/down) stored in DB

## Local Setup

### Backend
1. `cd backend`
2. `python -m venv .venv`
3. Activate venv
4. `pip install -r requirements.txt`
5. Create `.env` from `.env.example`
6. `uvicorn app.main:app --reload --port 8000`

### Frontend
1. `cd frontend`
2. `npm install`
3. Create `.env` from `.env.example`
4. `npm run dev`

## Environment Variables

Backend `.env`:
- `APP_SECRET_KEY`
- `DATABASE_URL` (optional: Supabase Postgres connection string)
- `ACCESS_TOKEN_EXPIRE_MINUTES`
- `CRYPTOPANIC_TOKEN` (optional)
- `OPENROUTER_API_KEY` or `HUGGINGFACE_API_KEY` (optional)
- `OPENROUTER_MODEL` / `HUGGINGFACE_MODEL` (optional)

Frontend `.env`:
- `VITE_API_URL`

## Deployment
- Frontend: Vercel (set `VITE_API_URL` to backend URL)
- Backend: Render or Railway (set same env vars as local)

## AI Usage Summary
This project was built with the help of an AI coding assistant. Prompts used:
- Interpreted assignment requirements.
- Generated a full-stack project scaffold (FastAPI + React).
- Implemented auth, onboarding, dashboard aggregation, and feedback storage.
