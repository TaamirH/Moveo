from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import User
from ..schemas import UserCreate, UserLogin, Token
from ..auth import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=Token)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    user = User(
        email=user_in.email,
        name=user_in.name,
        password_hash=hash_password(user_in.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_access_token(subject=user.email)
    return Token(access_token=token)


@router.post("/login", response_model=Token)
def login(user_in: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_in.email).first()
    if not user or not verify_password(user_in.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(subject=user.email)
    return Token(access_token=token)


@router.get("/me")
def me(current_user: User = Depends(get_current_user)):
    profile = None
    if current_user.profile:
        profile = {
            "investor_type": current_user.profile.investor_type,
            "interested_assets": current_user.profile.interested_assets or [],
            "content_preferences": current_user.profile.content_preferences or [],
        }
    return {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.name,
        "profile": profile,
    }
