from pathlib import Path
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session
from ..auth import get_current_user
from ..database import get_db
from ..models import User
from ..recommendation_service import run_planner
from ..schemas import HomeRequest, PartyRequest

router = APIRouter(tags=["planners"])
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}

@router.post("/generate-home")
def generate_home(data: HomeRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    result = run_planner(db, user, "home", data.budget, data.model_dump(exclude={"budget"}))
    return {"planner_type": "home", "budget": data.budget, **result}

@router.post("/generate-party")
def generate_party(data: PartyRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    result = run_planner(db, user, "party", data.budget, data.model_dump(exclude={"budget"}))
    return {"planner_type": "party", "budget": data.budget, **result}

@router.post("/generate-jewelry")
async def generate_jewelry(
    budget: float = Form(...),
    occasion: str = Form(...),
    style: str = Form("Minimal"),
    outfit_notes: str = Form(""),
    outfit_image: UploadFile | None = File(None),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if budget <= 0:
        raise HTTPException(400, "Budget must be greater than zero.")
    image_bytes = None
    mime_type = None
    if outfit_image and outfit_image.filename:
        if outfit_image.content_type not in ALLOWED_IMAGE_TYPES:
            raise HTTPException(400, "Only JPG, PNG, and WEBP images are supported.")
        image_bytes = await outfit_image.read()
        if len(image_bytes) > 5 * 1024 * 1024:
            raise HTTPException(400, "Image must be 5 MB or smaller.")
        mime_type = outfit_image.content_type
    details = {"occasion": occasion, "style": style, "outfit_notes": outfit_notes}
    result = run_planner(db, user, "jewelry", budget, details, image_bytes, mime_type)
    return {"planner_type": "jewelry", "budget": budget, **result}
