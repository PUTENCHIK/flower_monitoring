from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from src.devices import devices_router
from src.database import create_db_and_tables
from src.config import Config


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("App starting")
    await create_db_and_tables()
    yield
    print("App terminating")


app = FastAPI(lifespan=lifespan)
app.include_router(devices_router)


app.add_middleware(CORSMiddleware,
                   allow_origins=Config.app.origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])