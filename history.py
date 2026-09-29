import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..auth import get_current_user
from ..database import get_db
from ..models import RecommendationHistory, User

router = APIRouter(tags=["history"])

@router.get("/history")
def history(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    rows = (
        db.query(RecommendationHistory)
        .filter(RecommendationHistory.user_id == user.id)
        .order_by(RecommendationHistory.created_at.desc())
        .limit(50)
        .all()
    )
    return [
        {
            "id": row.id,
            "planner_type": row.planner_type,
            "inputs": json.loads(row.input_json),
            "result": json.loads(row.result_json),
            "created_at": row.created_at.isoformat(),
        }
        for row in rows
    ]
