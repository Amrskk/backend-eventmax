from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.db.models.event import Event
from app.schemas.recommendation import RecommendRequest, EventOut
from app.services.recommendation import recommend_events
from sqlalchemy.future import select

router = APIRouter()

@router.post("/recommend", response_model=List[EventOut])
async def recommend(data: RecommendRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Event))
    all_events = result.scalars().all()

    events_list = [  # convert to plain dicts
        {
            "title": e.title,
            "description": e.description,
            "tags": e.tags,
            "location": e.location,
            "price": e.price,
            "date": e.date
        }
        for e in all_events
    ]

    recommended = recommend_events(data.dict(), events_list)
    return recommended
