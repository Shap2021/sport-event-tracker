from datetime import datetime
from pydantic import BaseModel, EmailStr

class User(BaseModel):
    email: EmailStr
    password: str

class UserSchema(User):
    id: int
    last_updated:datetime

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    last_updated: datetime

    class Config:
        from_attributes = True
