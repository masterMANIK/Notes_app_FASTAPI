from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.schemas.user import UserCreate
from app.repositories import user_repo
from app.core import security

def create_user(db: Session, user: UserCreate):
    """Business logic for creating a new user."""
    # 1. Check if user already exists
    existing_user = user_repo.get_user_by_email(db, email=user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # 2. Hash the password
    hashed_password = security.get_password_hash(user.password)
    
    # 3. Save to database
    return user_repo.create_user(db=db, email=user.email, hashed_password=hashed_password)
