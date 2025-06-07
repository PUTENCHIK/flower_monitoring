import os
from typing import AsyncGenerator

import urllib.parse
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base

db_url= os.environ.get("FLOWER_DATABASE_URL")


if not db_url:
    raise ValueError("FLOWER_DATABASE_URL is not set in environment variables.")



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
    db_url
)

engine = create_async_engine(database_path,
                             echo=False)

BaseDBModel = declarative_base()
