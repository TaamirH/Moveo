from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Profile, User
from ..schemas import ProfileIn, ProfileOut
from ..auth import get_current_user

router = APIRouter(prefix="/onboarding", tags=["onboarding"])


@router.post("", response_model=ProfileOut)
def save_profile(
    profile_in: ProfileIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if profile:
        profile.investor_type = profile_in.investor_type
        profile.interested_assets = profile_in.interested_assets
        profile.content_preferences = profile_in.content_preferences
    else:
        profile = Profile(
            user_id=current_user.id,
            investor_type=profile_in.investor_type,
            interested_assets=profile_in.interested_assets,
            content_preferences=profile_in.content_preferences,
        )
        db.add(profile)
    db.commit()
    db.refresh(profile)
    return ProfileOut(
        user_id=current_user.id,
        investor_type=profile.investor_type,
        interested_assets=profile.interested_assets or [],
        content_preferences=profile.content_preferences or [],
    )
