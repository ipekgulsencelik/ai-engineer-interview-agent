"""Alembic environment: explicit URL via environment, never checked-in secrets."""

from __future__ import annotations

import os

from alembic import context
from sqlalchemy import create_engine, pool

config = context.config
target_metadata = None


def _url() -> str:
    value = os.environ.get("POSTGRES_DATABASE_URL", "").strip()
    if not value or not value.startswith("postgresql+psycopg://"):
        raise RuntimeError(
            "POSTGRES_DATABASE_URL must be a postgresql+psycopg:// DSN"
        )
    return value


def run_migrations_offline() -> None:
    context.configure(
        url=_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    engine = create_engine(_url(), poolclass=pool.NullPool)
    try:
        with engine.connect() as conn:
            context.configure(
                connection=conn,
                target_metadata=target_metadata,
                transactional_ddl=True,
            )
            with context.begin_transaction():
                context.run_migrations()
    finally:
        engine.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
