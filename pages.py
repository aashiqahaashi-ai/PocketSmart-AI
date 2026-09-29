from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from ..auth import get_current_user
from ..database import get_db
from ..models import User

router = APIRouter()
templates = Jinja2Templates(directory="templates")

def render(request: Request, name: str, **context):
    return templates.TemplateResponse(request=request, name=name, context={"request": request, **context})

@router.get("/")
def index(request: Request):
    return render(request, "index.html")

@router.get("/login")
def login_page(request: Request):
    return render(request, "login.html")

@router.get("/register")
def register_page(request: Request):
    return render(request, "register.html")

@router.get("/dashboard")
def dashboard(request: Request, user: User = Depends(get_current_user)):
    return render(request, "dashboard.html", user=user)

@router.get("/home-planner")
def home_planner(request: Request, user: User = Depends(get_current_user)):
    return render(request, "home_planner.html", user=user)

@router.get("/party-planner")
def party_planner(request: Request, user: User = Depends(get_current_user)):
    return render(request, "party_planner.html", user=user)

@router.get("/jewelry-planner")
def jewelry_planner(request: Request, user: User = Depends(get_current_user)):
    return render(request, "jewelry_planner.html", user=user)

@router.get("/history")
def history_page(request: Request, user: User = Depends(get_current_user)):
    return render(request, "history.html", user=user)

@router.get("/recommendations-details")
def recommendation_details(request: Request, user: User = Depends(get_current_user)):
    return render(request, "recommendations.html", user=user)
