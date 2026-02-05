from typing import List, Optional
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ProfileIn(BaseModel):
    investor_type: Optional[str] = None
    interested_assets: List[str]
    content_preferences: List[str]


class ProfileOut(ProfileIn):
    user_id: int


class DashboardResponse(BaseModel):
    news: list
    prices: dict
    ai_insight: str
    ai_source: str
    meme: dict


class FeedbackIn(BaseModel):
    content_type: str
    content_id: str
    vote: bool
