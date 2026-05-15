from pydantic import BaseModel, EmailStr, ConfigDict

# Schema for when a user signs up
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# Schema for what we return to the user (never return the password!)
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

# Schema for the JWT Token
class Token(BaseModel):
    access_token: str
    token_type: str
