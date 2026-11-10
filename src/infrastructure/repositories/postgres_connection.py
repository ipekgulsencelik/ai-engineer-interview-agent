"""Optional PostgreSQL driver boundary; no database secrets in logs."""

from __future__ import annotations

import importlib
from typing import Any, Protocol


class PostgresConnectionPort(Protocol):
    """Callable returning a psycopg-compatible transaction connection."""

    def __call__(self) -> Any: ...


class PsycopgConnectionFactory:
    """Create one DB connection per operation, with explicit security policy."""

    def __init__(
        self,
        *,
        dsn: str,
        connect_timeout: int = 5,
        require_tls: bool = True,
    ) -> None:
        if not isinstance(dsn, str) or not dsn.startswith("postgresql://"):
            raise ValueError("dsn must start with postgresql://")
        if type(connect_timeout) is not int or not 1 <= connect_timeout <= 60:
            raise ValueError("connect_timeout must be in [1, 60]")
        if type(require_tls) is not bool:
            raise ValueError("require_tls must be boolean")
        self._dsn = dsn
        self._connect_timeout = connect_timeout
        self._require_tls = require_tls

    def __call__(self) -> Any:
        try:
            driver = importlib.import_module("psycopg")
        except ImportError as exc:
            raise RuntimeError(
                "PostgreSQL support requires psycopg; see requirements-postgres.txt"
            ) from exc
        # Prefer verify-full in deployments, never silently fall back to plaintext.
        if self._require_tls:
            return driver.connect(
                self._dsn,
                connect_timeout=self._connect_timeout,
                sslmode="verify-full",
            )
        return driver.connect(
            self._dsn,
            connect_timeout=self._connect_timeout,
        )
