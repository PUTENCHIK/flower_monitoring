from contextlib import asynccontextmanager

from fastapi import FastAPI
from src.devices import devices_router
from src.database import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("App starting")
    await create_db_and_tables()
    yield
    print("App terminating")


app = FastAPI(lifespan=lifespan)
app.include_router(devices_router)


@app.post("/test")
async def test(data: str):
    return {'Server received': data}
