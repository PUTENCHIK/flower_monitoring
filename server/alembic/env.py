import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import AsyncEngine

from alembic import context
import os

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Получаем URL из переменной окружения
database_url = os.getenv('FLOWER_DATABASE_URL')
if not database_url:
    raise RuntimeError("Переменная окружения FLOWER_DATABASE_URL не установлена")

config.set_main_option('sqlalchemy.url', database_url)

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

# Импорт моделей, если нужно
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = None  # или укажи свою метадату

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online():
    """Run migrations in 'online' mode."""

    connectable = AsyncEngine(
        config.get_section(config.config_ini_section),
        poolclass=pool.NullPool,
        future=True,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

def do_run_migrations(connection: Connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        # здесь можно добавить другие опции, если нужно
    )

    with context.begin_transaction():
        context.run_migrations()

def main():
    if context.is_offline_mode():
        run_migrations_offline()
    else:
        asyncio.run(run_migrations_online())

if __name__ == '__main__':
    main()
