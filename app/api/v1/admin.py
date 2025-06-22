from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.scraper import fetch_events_from_sxodim
from app.db.database import get_db
from app.db.models.event import Event  # your SQLAlchemy Event model

router = APIRouter()

@router.post("/scrape-now")
async def scrape_and_store_events(db: AsyncSession = Depends(get_db)):
    events = fetch_events_from_sxodim()
    added = 0

    for e in events:
        db_event = Event(
            title=e["title"],
            description=e["description"],
            tags=e["tags"],
            location=e["location"],
            price=e["price"],
            date=e["date"]
        )
        db.add(db_event)
        added += 1

    await db.commit()
    return {"message": f"{added} events added"}
