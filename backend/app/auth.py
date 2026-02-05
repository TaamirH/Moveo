import os
from datetime import datetime, timedelta
from typing import Optional

from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from .db import get_db
from .models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)


def create_access_token(subject: str, expires_minutes: Optional[int] = None) -> str:
    secret_key = os.getenv("APP_SECRET_KEY", "dev-secret")
    expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))
    if expires_minutes is not None:
        expire_minutes = expires_minutes
    expire = datetime.utcnow() + timedelta(minutes=expire_minutes)
    to_encode = {"sub": subject, "exp": expire}
    return jwt.encode(to_encode, secret_key, algorithm="HS256")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    secret_key = os.getenv("APP_SECRET_KEY", "dev-secret")
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except JWTError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user
