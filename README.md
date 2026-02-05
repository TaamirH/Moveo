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
- `COINGECKO_API_KEY` (optional, helps avoid rate limits)
- `OPENROUTER_API_KEY` 
- `OPENROUTER_MODEL` 

Frontend `.env`:
- `VITE_API_URL`

## Deployment
- Frontend: Vercel (set `VITE_API_URL` to backend URL)
- Backend: Render or Railway (set same env vars as local)

## Bonus: Feedback for Future Model Improvements
Every thumbs up/down is saved with the user, content type, and content id. Later on, this can be used to rank content per profile (show more of what was liked, less of what was disliked) and to tune topic weights over time without retraining the base model.

## AI Usage Summary
This project was built with the help of an AI coding assistant and directed by me. I used it to:
- Analyze the assignment and design the architecture.
- Scaffold the FastAPI + React app and core flows (auth, onboarding, dashboard).
- Integrate external APIs (CryptoPanic, CoinGecko, OpenRouter) and add fallbacks.
- Improve UX details (validation, source badges) and deployment readiness.
