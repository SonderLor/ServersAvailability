from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import create_engine
from alembic import context

from core.config import settings
from models.server import Base

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def get_url():
    database_url = settings.DATABASE_URL
    return database_url.replace("postgresql+asyncpg", "postgresql+psycopg2")

def run_migrations_online():
    connectable = create_engine(
        get_url(),
        poolclass=pool.NullPool
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

run_migrations_online()
