import sys
import traceback

try:
    from app.database import SessionLocal
    from app.schemas.user import UserCreate
    from app.services import user_service

    db = SessionLocal()
    user_data = UserCreate(email="test@test.com", password="password123")
    user = user_service.create_user(db=db, user=user_data)
    print("User created successfully!")
except Exception as e:
    print("ERROR:")
    traceback.print_exc()
