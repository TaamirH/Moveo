from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..auth import get_current_user
from ..db import get_db
from ..models import Feedback, User
from ..schemas import FeedbackIn

router = APIRouter(prefix="/feedback", tags=["feedback"])


@router.post("")
def submit_feedback(
    payload: FeedbackIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    feedback = Feedback(
        user_id=current_user.id,
        content_type=payload.content_type,
        content_id=payload.content_id,
        vote=payload.vote,
    )
    db.add(feedback)
    db.commit()
    return {"status": "ok"}
