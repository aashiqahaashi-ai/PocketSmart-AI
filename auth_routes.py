from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.orm import Session
from ..auth import create_access_token, get_current_user, hash_password, verify_password
from ..database import get_db
from ..models import User
from ..schemas import LoginRequest, RegisterRequest

router = APIRouter(prefix="", tags=["authentication"])

@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    email = data.email.lower()
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(400, "Email is already registered.")
    user = User(name=data.name.strip(), email=email, password_hash=hash_password(data.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_access_token(user.id)
    response = JSONResponse({"message": "Registration successful."})
    response.set_cookie("pocketsmart_token", token, httponly=True, samesite="lax", max_age=86400)
    return response

@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email.lower()).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(401, "Invalid email or password.")
    token = create_access_token(user.id)
    response = JSONResponse({"message": "Login successful."})
    response.set_cookie("pocketsmart_token", token, httponly=True, samesite="lax", max_age=86400)
    return response

@router.post("/logout")
def logout():
    response = JSONResponse({"message": "Logged out."})
    response.delete_cookie("pocketsmart_token")
    return response

@router.get("/token")
def token_info(user: User = Depends(get_current_user)):
    return {"authenticated": True, "user_id": user.id, "email": user.email}

@router.get("/session-info")
def session_info(user: User = Depends(get_current_user)):
    return {"logged_in": True, "user_id": user.id, "name": user.name, "email": user.email}

@router.get("/session-data")
def session_data(user: User = Depends(get_current_user)):
    return {"user": {"id": user.id, "name": user.name, "email": user.email}}
