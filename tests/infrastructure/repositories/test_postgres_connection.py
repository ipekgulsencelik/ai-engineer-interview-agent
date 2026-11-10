"""Production connection policy without a PostgreSQL driver dependency."""

from __future__ import annotations

import pytest

from src.infrastructure.repositories.postgres_connection import (
    PsycopgConnectionFactory,
)


def test_postgres_connection_requires_explicit_postgresql_dsn() -> None:
    for dsn in ("", "sqlite:///tmp/database", "postgresql+psycopg://host/db"):
        with pytest.raises(ValueError, match="dsn"):
            PsycopgConnectionFactory(dsn=dsn)


def test_postgres_connection_defaults_to_tls_verification() -> None:
    factory = PsycopgConnectionFactory(
        dsn="postgresql://user:password@localhost/test"
    )
    assert factory._require_tls is True


def test_postgres_connection_rejects_bad_timeout() -> None:
    for timeout in (0, 61, True):
        with pytest.raises(ValueError, match="connect_timeout"):
            PsycopgConnectionFactory(
                dsn="postgresql://host/db",
                connect_timeout=timeout,
            )


def test_postgres_connection_rejects_invalid_tls_toggle() -> None:
    with pytest.raises(ValueError, match="require_tls"):
        PsycopgConnectionFactory(
            dsn="postgresql://host/db",
            require_tls="off",  # type: ignore[arg-type]
        )
