"""Minimal ASGI HTTP instrumentation; never reads bodies, headers or raw paths.

Captures registered route templates, not concrete parameter values. Instrument
only HTTP scopes; no network listener or SDK is initialized here.
"""

from __future__ import annotations

import time
from collections.abc import Callable
from typing import Any

from starlette.routing import Match
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from src.application.observability.http_server_telemetry import (
    HTTPServerTelemetryPort,
    SafeHTTPServerTelemetry,
)

_METHODS = frozenset({
    "GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"
})
_MAX_ROUTES = 128


def safe_method(method: object) -> str:
    return method if isinstance(method, str) and method in _METHODS else "OTHER"


def status_family(status: int) -> str:
    if 200 <= status < 300:
        return "2xx"
    if 300 <= status < 400:
        return "3xx"
    if 400 <= status < 500:
        return "4xx"
    return "5xx"


class HTTPRequestObservabilityMiddleware:
    """Pure ASGI middleware, including streamed responses and raised errors."""

    def __init__(
        self,
        app: ASGIApp,
        *,
        telemetry: HTTPServerTelemetryPort | None = None,
        routes: tuple[Any, ...] = (),
        monotonic_clock: Callable[[], float] | None = None,
    ) -> None:
        self.app = app
        self.telemetry = SafeHTTPServerTelemetry(telemetry)
        self._clock = monotonic_clock or time.perf_counter
        # The endpoint list comes from FastAPI route declarations, not users.
        self._routes = routes[:_MAX_ROUTES]
        self._allowlist = frozenset(
            route.path
            for route in self._routes
            if isinstance(getattr(route, "path", None), str)
        )

    def _route_template(self, scope: Scope) -> str:
        for route in self._routes:
            try:
                match, _ = route.matches(scope)
            except (AttributeError, KeyError, TypeError, ValueError):
                continue
            if match is Match.FULL:
                route_path = getattr(route, "path", None)
                if isinstance(route_path, str) and route_path in self._allowlist:
                    return route_path
        return "unmatched"

    async def __call__(
        self, scope: Scope, receive: Receive, send: Send
    ) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        method = safe_method(scope.get("method"))
        route = self._route_template(scope)
        started = self._clock()
        http_status = 500
        raised = False

        async def send_observed(message: Message) -> None:
            nonlocal http_status
            if message["type"] == "http.response.start":
                status = message.get("status")
                if type(status) is int and 100 <= status <= 599:
                    http_status = status
            await send(message)

        with self.telemetry.span(method=method, route=route):
            try:
                await self.app(scope, receive, send_observed)
            except BaseException:
                raised = True
                raise
            finally:
                duration = max(0.0, self._clock() - started)
                self.telemetry.observe(
                    method=method,
                    route=route,
                    status_class=status_family(500 if raised else http_status),
                    duration_seconds=duration,
                )
