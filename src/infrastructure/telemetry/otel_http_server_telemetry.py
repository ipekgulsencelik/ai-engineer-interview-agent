"""OpenTelemetry SDK adapter with bounded HTTP label cardinality."""

from __future__ import annotations

import math
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any

_ALLOWED_METHODS = frozenset({
    "GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD", "OTHER"
})
_STATUS_CLASSES = frozenset({"2xx", "3xx", "4xx", "5xx"})
_ROUTE_LIMIT = 128


class OpenTelemetryHTTPServerTelemetry:
    """Export request count/latency using only registered route templates."""

    def __init__(
        self,
        *,
        meter: Any,
        tracer: Any,
        route_templates: frozenset[str],
    ) -> None:
        if (
            not isinstance(route_templates, frozenset)
            or len(route_templates) > _ROUTE_LIMIT
            or any(not isinstance(path, str) or not path.startswith("/")
                   for path in route_templates)
        ):
            raise ValueError("route_templates must be a bounded set of paths")
        self._routes = route_templates | {"unmatched"}
        self._counter = meter.create_counter(
            "http_server_requests",
            unit="{request}",
            description="Total HTTP server requests by route and status family",
        )
        self._duration = meter.create_histogram(
            "http_server_request_duration",
            unit="s",
            description="HTTP request duration by registered route template",
        )
        self._tracer = tracer

    def _labels(self, *, method: str, route: str) -> None:
        if method not in _ALLOWED_METHODS:
            raise ValueError("HTTP method is not in the bounded allowlist")
        if route not in self._routes:
            raise ValueError("HTTP route must be a registered template")

    @contextmanager
    def span(self, *, method: str, route: str) -> Iterator[None]:
        self._labels(method=method, route=route)
        with self._tracer.start_as_current_span(
            "http.server.request",
            attributes={"http.request.method": method, "http.route": route},
            record_exception=False,
            set_status_on_exception=False,
        ):
            yield

    def observe(
        self,
        *,
        method: str,
        route: str,
        status_class: str,
        duration_seconds: float,
    ) -> None:
        self._labels(method=method, route=route)
        if status_class not in _STATUS_CLASSES:
            raise ValueError("status_class is not permitted")
        if (
            type(duration_seconds) not in (int, float)
            or not math.isfinite(duration_seconds)
            or duration_seconds < 0
        ):
            raise ValueError("duration_seconds must be finite and nonnegative")
        attrs = {"method": method, "route": route, "status_class": status_class}
        self._counter.add(1, attrs)
        self._duration.record(float(duration_seconds), attrs)
