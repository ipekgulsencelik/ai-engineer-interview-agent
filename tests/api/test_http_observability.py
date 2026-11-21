"""ASGI HTTP middleware tests: bounded templates, status, safety and streaming."""

from __future__ import annotations

import asyncio
from collections.abc import Iterator
from contextlib import contextmanager

import pytest
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from src.api.http_observability import (
    HTTPRequestObservabilityMiddleware,
    safe_method,
    status_family,
)


class TelemetrySpy:
    def __init__(self, *, broken: bool = False) -> None:
        self.broken = broken
        self.observations: list[tuple[str, str, str, float]] = []
        self.spans: list[tuple[str, str]] = []

    @contextmanager
    def span(self, *, method: str, route: str) -> Iterator[None]:
        if self.broken:
            raise RuntimeError("SECRET=do-not-log-this")
        self.spans.append((method, route))
        yield

    def observe(
        self,
        *,
        method: str,
        route: str,
        status_class: str,
        duration_seconds: float,
    ) -> None:
        if self.broken:
            raise RuntimeError("SECRET=do-not-log-this")
        self.observations.append(
            (method, route, status_class, duration_seconds)
        )


def _app(spy: TelemetrySpy) -> FastAPI:
    app = FastAPI()

    @app.get("/items/{item_id}")
    def item(item_id: str) -> dict[str, str]:
        return {"value": item_id}

    @app.get("/broken")
    def broken() -> dict[str, str]:
        raise RuntimeError("sensitive application failure")

    @app.get("/stream")
    async def streaming() -> StreamingResponse:
        async def produce():
            yield b"first"
            yield b"second"
        return StreamingResponse(produce())

    app.add_middleware(
        HTTPRequestObservabilityMiddleware,
        routes=tuple(app.routes),
        telemetry=spy,
    )
    return app


async def _invoke(
    app: FastAPI,
    *,
    path: str,
    method: str = "GET",
) -> list[dict]:
    events: list[dict] = []
    receive_count = 0

    async def receive() -> dict:
        nonlocal receive_count
        receive_count += 1
        if receive_count == 1:
            return {
                "type": "http.request",
                "body": b"",
                "more_body": False,
            }
        return {"type": "http.disconnect"}

    async def send(message: dict) -> None:
        events.append(message)

    scope = {
        "type": "http",
        "asgi": {"version": "3.0"},
        "http_version": "1.1",
        "scheme": "http",
        "server": ("testserver", 80),
        "client": ("127.0.0.1", 12345),
        "root_path": "",
        "method": method,
        "path": path,
        "raw_path": path.encode(),
        "query_string": b"secret-password=DO_NOT_EXPORT",
        "headers": [(b"authorization", b"PRIVATE-TOKEN")],
    }
    await app(scope, receive, send)
    return events


def test_http_success_records_template_and_2xx_without_raw_url() -> None:
    spy = TelemetrySpy()
    app = _app(spy)
    result = asyncio.run(_invoke(app, path="/items/secret-user-123"))
    assert result[0]["status"] == 200
    assert len(spy.observations) == 1
    assert spy.observations[0][:3] == (
        "GET", "/items/{item_id}", "2xx"
    )
    assert spy.spans == [("GET", "/items/{item_id}")]
    assert spy.observations[0][3] >= 0.0
    assert "secret-user-123" not in repr(spy.observations)
    assert "PRIVATE-TOKEN" not in repr(spy.spans)


def test_404_and_method_not_allowed_use_unmatched_label() -> None:
    spy = TelemetrySpy()
    app = _app(spy)
    assert asyncio.run(_invoke(app, path="/users/SECRET"))[0]["status"] == 404
    assert asyncio.run(
        _invoke(app, path="/items/123", method="DELETE")
    )[0]["status"] == 405
    assert [record[1:3] for record in spy.observations] == [
        ("unmatched", "4xx"), ("unmatched", "4xx"),
    ]


def test_unhandled_exception_is_counted_as_5xx_and_propagates() -> None:
    spy = TelemetrySpy()
    app = _app(spy)
    with pytest.raises(RuntimeError, match="sensitive application failure"):
        asyncio.run(_invoke(app, path="/broken"))
    assert spy.observations[0][:3] == ("GET", "/broken", "5xx")
    assert "sensitive application failure" not in repr(spy.observations)


def test_exporter_failure_does_not_change_successful_response(
    caplog: pytest.LogCaptureFixture,
) -> None:
    spy = TelemetrySpy(broken=True)
    events = asyncio.run(_invoke(_app(spy), path="/items/42"))
    assert events[0]["status"] == 200
    assert "HTTP telemetry backend unavailable" in caplog.text
    assert "SECRET=do-not-log-this" not in caplog.text


def test_streaming_is_not_buffered_or_modified() -> None:
    spy = TelemetrySpy()
    events = asyncio.run(_invoke(_app(spy), path="/stream"))
    assert events[0]["status"] == 200
    assert spy.observations[0][:3] == ("GET", "/stream", "2xx")


def test_health_app_routes_and_opt_in_instrumentation() -> None:
    from src.api.app import create_app, registered_route_templates

    spy = TelemetrySpy()
    app = create_app(http_telemetry=spy)
    assert "/api/v1/health/" in registered_route_templates(app)
    result = asyncio.run(_invoke(app, path="/api/v1/health/"))
    assert result[0]["status"] == 200
    assert spy.observations[0][:3] == (
        "GET", "/api/v1/health/", "2xx"
    )

    default_app = create_app()
    assert default_app.user_middleware == []


def test_normalization_has_bounded_methods_and_status_family() -> None:
    assert safe_method("GET") == "GET"
    assert safe_method("GET PRIVATE-ID") == "OTHER"
    assert safe_method(None) == "OTHER"
    assert status_family(204) == "2xx"
    assert status_family(302) == "3xx"
    assert status_family(422) == "4xx"
    assert status_family(503) == "5xx"


def test_non_http_scope_passes_without_instrumentation() -> None:
    spy = TelemetrySpy()
    seen: list[str] = []

    async def app(scope, receive, send):
        seen.append(scope["type"])

    middleware = HTTPRequestObservabilityMiddleware(
        app, telemetry=spy, routes=()
    )

    async def receive():
        return {"type": "websocket.disconnect", "code": 1000}

    async def send(message):
        return None

    asyncio.run(
        middleware(
            {"type": "websocket", "path": "/ws"},
            receive,
            send,
        )
    )
    assert seen == ["websocket"]
    assert spy.spans == []
    assert spy.observations == []
