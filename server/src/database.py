from typing import AsyncGenerator
from server.src import Config
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(engine) as session:
        try:
            yield session
        finally:
            await session.close()


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(BaseDBModel.metadata.create_all)


database_path = ("sqlite+aiosqlite:///"
                 f"{Config.paths.storage / Config.database.name}")

engine = create_async_engine(database_path,
                             echo=False)

BaseDBModel = declarative_base()
