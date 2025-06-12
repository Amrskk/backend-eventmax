from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.db.models.user import User
from app.db.schemas.user import UserCreate, UserResponse
from sqlalchemy.future import select

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    new_user = User(
        name=user.name,
        email=user.email,
        hashed_password=user.password,
        interests="",
        location="",
        budget=None
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user
