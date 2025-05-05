import os
from typing import AsyncGenerator

import urllib.parse
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base

db_user = os.environ.get("FLOWER_MONITORING_USER")
db_password = os.environ.get("FLOWER_MONITORING_PASSWORD")
db_host = os.environ.get("FLOWER_MONITORING_HOST")
db_name = os.environ.get("FLOWER_MONITORING_DBNAME")

if not db_user:
    raise ValueError("FLOWER_MONITORING_USER is not set in environment variables.")
if not db_password:
    raise ValueError("FLOWER_MONITORING_PASSWORD is not set in environment variables.")
if not db_host:
    raise ValueError("FLOWER_MONITORING_HOST is not set in environment variables.")
if not db_name:
    raise ValueError("FLOWER_MONITORING_DBNAME is not set in environment variables.")

encoded_password = urllib.parse.quote_plus(db_password)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(engine) as session:
        try:
            yield session
        finally:
            await session.close()


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(BaseDBModel.metadata.create_all)


database_path = (
    f"mysql+asyncmy://{db_user}:{encoded_password}@{db_host}/{db_name}?charset=utf8mb4"
)

engine = create_async_engine(database_path,
                             echo=False)

BaseDBModel = declarative_base()
