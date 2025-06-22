from fastapi import FastAPI
from app.api.v1 import users
from fastapi.middleware.cors import CORSMiddleware
from app.bot import instance, handlers
from app.api.v1 import admin, recommend
import asyncio

app = FastAPI(title="Smart Events API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # на проде уточнить
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])

@app.get("/")
async def root():
    return {"message": "Smart Events Backend is alive"}

@app.on_event("startup")
async def startup():
    asyncio.create_task(instance.dp.start_polling(instance.bot))



app.include_router(admin.router, prefix="/api/v1/admin", tags=["Admin"])
app.include_router(recommend.router, prefix="/api/v1", tags=["Recommendations"])
