from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from typing import Any
import shutil
import os
import uuid

from app.schemas.user import UserResponse, UserUpdate
from app.services.user_service import UserService
from app.dependencies import get_db
from app.auth.security import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("", response_model=UserResponse)
def get_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = UserService(db)
    return service.get_profile(current_user)

@router.put("", response_model=UserResponse)
def update_profile(update_data: UserUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = UserService(db)
    return service.update_profile(current_user, update_data)

@router.post("/upload", response_model=UserResponse)
def upload_profile_image(
    file: UploadFile = File(...), 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    # Ensure directory exists
    os.makedirs("uploads", exist_ok=True)
    
    file_ext = file.filename.split('.')[-1]
    unique_filename = f"{uuid.uuid4()}.{file_ext}"
    file_path = f"uploads/{unique_filename}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    image_url = f"https://domain.com/{file_path}" # Ideally use request.base_url in production

    service = UserService(db)
    return service.upload_profile_image(current_user, image_url)

@router.delete("")
def delete_account(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = UserService(db)
    return service.delete_account(current_user)
