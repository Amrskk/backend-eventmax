from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    interests: Optional[str]
    location: Optional[str]
    budget: Optional[float]

    class Config:
        orm_mode = True
