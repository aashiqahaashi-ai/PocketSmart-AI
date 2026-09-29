import json
from sqlalchemy.orm import Session
from .gemini_utils import generate_recommendations
from .models import RecommendationHistory, User

def save_history(db: Session, user: User, planner: str, inputs: dict, result: dict) -> RecommendationHistory:
    record = RecommendationHistory(
        user_id=user.id,
        planner_type=planner,
        input_json=json.dumps(inputs, ensure_ascii=False),
        result_json=json.dumps(result, ensure_ascii=False),
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def run_planner(db: Session, user: User, planner: str, budget: float, details: dict, image_bytes=None, mime_type=None):
    result = generate_recommendations(planner, budget, details, image_bytes, mime_type)
    inputs = {"budget": budget, **details}
    save_history(db, user, planner, inputs, result)
    return result
