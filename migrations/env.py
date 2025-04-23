import asyncio
from logging.config import fileConfig

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import pool
from alembic import context

from backend.models.database import DATABASE_URL # Подключаем базу и метаданные
from backend.models.models import Base  # Подключаем базу и метаданные


# Подключаем конфиг логирования Alembic
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Устанавливаем асинхронный URL базы данных
config.set_main_option("sqlalchemy.url", DATABASE_URL + "?async_fallback=True")

target_metadata = Base.metadata  # Метаданные для Alembic


def run_migrations_offline() -> None:
    """Запускает миграции в оффлайн-режиме."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Запускает миграции в онлайн-режиме (асинхронно)."""
    connectable = create_async_engine(
        config.get_main_option("sqlalchemy.url"),
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def do_run_migrations(connection):
    """Выполняет миграции в синхронном режиме внутри асинхронного контекста."""
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    try:
        asyncio.run(run_migrations_online())
    except RuntimeError:  # Если уже есть запущенный event loop
        loop = asyncio.get_event_loop()
        loop.run_until_complete(run_migrations_online())
