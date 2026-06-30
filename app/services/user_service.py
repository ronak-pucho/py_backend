from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.user_repo import UserRepository
from app.schemas.user import UserCreate, UserLogin, ChangePassword, UserUpdate
from app.auth.password import verify_password, get_password_hash
from app.auth.security import create_access_token, create_refresh_token
from app.models.user import User
from app.utils.exceptions import CustomException

class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def signup(self, user_in: UserCreate):
        existing_user = self.repo.get_user_by_email(user_in.email)
        if existing_user:
            raise CustomException(status_code=400, detail="Email already registered")
        
        return self.repo.create_user(user_in)

    def login(self, user_in: UserLogin):
        user = self.repo.get_user_by_email(user_in.email)
        if not user:
            raise CustomException(status_code=401, detail="Invalid credentials")
        
        if not verify_password(user_in.password, user.password):
            raise CustomException(status_code=401, detail="Invalid credentials")

        access_token = create_access_token(subject=user.id)
        refresh_token = create_refresh_token(subject=user.id)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": user
        }

    def change_password(self, user: User, password_data: ChangePassword):
        if not verify_password(password_data.old_password, user.password):
            raise CustomException(status_code=400, detail="Invalid old password")
        
        new_hashed = get_password_hash(password_data.new_password)
        self.repo.change_password(user, new_hashed)
        return {"message": "Password updated successfully"}
    
    def get_profile(self, user: User):
        return user

    def update_profile(self, user: User, update_data: UserUpdate):
        return self.repo.update_user(user, update_data)

    def upload_profile_image(self, user: User, file_path: str):
        return self.repo.update_profile_image(user, file_path)

    def delete_account(self, user: User):
        self.repo.delete_user(user)
        return {"message": "Account deleted successfully"}
