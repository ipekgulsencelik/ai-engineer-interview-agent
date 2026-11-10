"""Dependency-inverted, privacy-preserving HTTP telemetry application port."""

from __future__ import annotations

import logging
from collections.abc import Iterator
from contextlib import AbstractContextManager, contextmanager
from typing import Protocol


class HTTPServerTelemetryPort(Protocol):
    """No request bodies, request IDs, URLs, or headers may cross this port."""

    def span(
        self, *, method: str, route: str
    ) -> AbstractContextManager[None]: ...

    def observe(
        self,
        *,
        method: str,
        route: str,
        status_class: str,
        duration_seconds: float,
    ) -> None: ...


class NoopHTTPServerTelemetry:
    """Safe default without an installed OpenTelemetry SDK."""

    @contextmanager
    def span(self, *, method: str, route: str) -> Iterator[None]:
        yield

    def observe(
        self,
        *,
        method: str,
        route: str,
        status_class: str,
        duration_seconds: float,
    ) -> None:
        return


class SafeHTTPServerTelemetry:
    """Metrics/tracing failures must never change an HTTP response."""

    def __init__(self, backend: HTTPServerTelemetryPort | None = None) -> None:
        self._backend = backend if backend is not None else NoopHTTPServerTelemetry()
        self._logger = logging.getLogger(__name__)

    def _warn(self) -> None:
        # Never log vendor exception strings; they may contain secrets or URLs.
        self._logger.warning("HTTP telemetry backend unavailable")

    @contextmanager
    def span(self, *, method: str, route: str) -> Iterator[None]:
        context: AbstractContextManager[None] | None = None
        try:
            context = self._backend.span(method=method, route=route)
            context.__enter__()
        except Exception:
            context = None
            self._warn()
        try:
            yield
        finally:
            if context is not None:
                try:
                    context.__exit__(None, None, None)
                except Exception:
                    self._warn()

    def observe(
        self,
        *,
        method: str,
        route: str,
        status_class: str,
        duration_seconds: float,
    ) -> None:
        try:
            self._backend.observe(
                method=method,
                route=route,
                status_class=status_class,
                duration_seconds=duration_seconds,
            )
        except Exception:
            self._warn()
