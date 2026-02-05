import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from .db import Base, engine
from .routers import auth, onboarding, dashboard, feedback

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Crypto Advisor API")

origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(onboarding.router)
app.include_router(dashboard.router)
app.include_router(feedback.router)


@app.get("/")
def root():
    return {"status": "ok"}
