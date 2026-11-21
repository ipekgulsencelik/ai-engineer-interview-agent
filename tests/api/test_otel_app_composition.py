"""Monitored FastAPI composition and SDK lifecycle tests without network."""

from __future__ import annotations

import asyncio
from typing import Any

import pytest

from src.api.otel_app import build_otel_app


class _Telemetry:
    def span(self, *, method: str, route: str) -> Any:
        from contextlib import nullcontext

        return nullcontext()

    def observe(
        self,
        *,
        method: str,
        route: str,
        status_class: str,
        duration_seconds: float,
    ) -> None:
        pass


class _Runtime:
    def __init__(self) -> None:
        self.shutdown_calls = 0
        self.route_templates: frozenset[str] = frozenset()

    def http_server_telemetry(
        self, *, route_templates: frozenset[str]
    ) -> _Telemetry:
        self.route_templates = route_templates
        return _Telemetry()

    def shutdown(self) -> None:
        self.shutdown_calls += 1


def test_factory_refuses_silent_uninstrumented_start(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("INTERVIEW_OTLP_ENDPOINT", raising=False)
    with pytest.raises(RuntimeError, match="required"):
        build_otel_app()


def test_factory_wires_runtime_and_closes_sdk(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import src.api.otel_app as otel_module

    runtime = _Runtime()
    injected: list[dict[str, Any]] = []

    def fake_runtime(**kwargs: Any) -> _Runtime:
        injected.append(kwargs)
        return runtime

    monkeypatch.setattr(
        otel_module, "create_otlp_runtime", fake_runtime
    )
    monkeypatch.setenv(
        "INTERVIEW_OTLP_ENDPOINT", "http://otel-collector:4318"
    )
    monkeypatch.setenv("INTERVIEW_ALLOW_LOCAL_OTLP_HTTP", "true")

    app = build_otel_app()
    assert len(app.user_middleware) == 1
    assert "/api/v1/health/" in runtime.route_templates
    assert injected[0]["allow_insecure_local"] is True
    assert injected[0]["collector_endpoint"] == (
        "http://otel-collector:4318"
    )

    async def exercise() -> None:
        async with app.router.lifespan_context(app):
            assert app.state.container is not None

    asyncio.run(exercise())
    assert runtime.shutdown_calls == 1
    assert app.state.container is None


def test_factory_http_is_not_enabled_without_explicit_flag(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import src.api.otel_app as otel_module

    args: list[dict[str, Any]] = []
    monkeypatch.setenv("INTERVIEW_OTLP_ENDPOINT", "https://otel.local:4318")
    monkeypatch.delenv("INTERVIEW_ALLOW_LOCAL_OTLP_HTTP", raising=False)
    monkeypatch.setattr(
        otel_module, "create_otlp_runtime",
        lambda **kwargs: args.append(kwargs) or _Runtime(),
    )
    build_otel_app()
    assert args[0]["allow_insecure_local"] is False
