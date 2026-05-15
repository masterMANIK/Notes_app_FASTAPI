from pydantic import BaseModel, EmailStr

# Schema for when a user signs up
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# Schema for what we return to the user (never return the password!)
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    is_active: bool

    class Config:
        from_attributes = True # This tells Pydantic to read data even if it is not a dict, but an ORM model.

# Schema for the JWT Token
class Token(BaseModel):
    access_token: str
    token_type: str
