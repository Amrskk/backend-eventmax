from pydantic import BaseModel
from typing import List
from datetime import datetime

class RecommendRequest(BaseModel):
    interests: str
    mood: str
    location: str
    budget: float

class EventOut(BaseModel):
    title: str
    description: str
    tags: List[str]
    location: str
    price: float
    date: datetime

    class Config:
        orm_mode = True
