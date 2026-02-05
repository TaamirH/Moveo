from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..auth import get_current_user
from ..db import get_db
from ..models import User
from ..services.crypto import get_prices
from ..services.news import get_news
from ..services.ai import get_ai_insight
from ..services.memes import get_meme
from ..schemas import DashboardResponse

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("", response_model=DashboardResponse)
async def dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    profile = None
    assets = []
    if current_user.profile:
        assets = current_user.profile.interested_assets or []
        profile = {
            "investor_type": current_user.profile.investor_type,
            "interested_assets": assets,
            "content_preferences": current_user.profile.content_preferences or [],
        }

    news = await get_news(assets)
    prices = await get_prices(assets)
    ai_insight = await get_ai_insight(profile)
    meme = get_meme()

    return {
        "news": news,
        "prices": prices,
        "ai_insight": ai_insight,
        "meme": meme,
    }
