from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import user as user_schemas
from app.services import user_service
from app.repositories import user_repo
from app.core import security

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup", response_model=user_schemas.UserResponse)
def signup(user: user_schemas.UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    return user_service.create_user(db=db, user=user)

@router.post("/login", response_model=user_schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Authenticate a user and return a JWT token."""
    # 1. Find user by email (OAuth2 uses 'username' field, so we pass that as email)
    user = user_repo.get_user_by_email(db, email=form_data.username)
    
    # 2. Check if user exists and password matches
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. Generate JWT token
    access_token = security.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
