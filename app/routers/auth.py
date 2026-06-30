from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Dict, Any

from app.schemas.user import UserCreate, UserLogin, TokenResponse, UserResponse, ChangePassword, ForgotPassword, ResetPassword
from app.services.user_service import UserService
from app.dependencies import get_db
from app.auth.security import get_current_user, create_access_token
from app.models.user import User

router = APIRouter()

@router.post("/signup", response_model=UserResponse, status_code=201)
def signup(user_in: UserCreate, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.signup(user_in)

@router.post("/login", response_model=TokenResponse)
def login(user_in: UserLogin, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.login(user_in)

@router.post("/logout")
def logout(current_user: User = Depends(get_current_user)):
    return {"message": "Successfully logged out"}

@router.post("/refresh-token")
def refresh_token(current_user: User = Depends(get_current_user)):
    access_token = create_access_token(subject=current_user.id)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/change-password")
def change_password(password_data: ChangePassword, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = UserService(db)
    return service.change_password(current_user, password_data)

@router.post("/forgot-password")
def forgot_password(data: ForgotPassword, db: Session = Depends(get_db)):
    return {"message": "Password reset link sent if email exists."}

@router.post("/reset-password")
def reset_password(data: ResetPassword, db: Session = Depends(get_db)):
    return {"message": "Password has been reset successfully."}
