# временно
from app.db.database import Base, engine
from app.db.models.user import User
import asyncio

async def create_all():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(create_all())
