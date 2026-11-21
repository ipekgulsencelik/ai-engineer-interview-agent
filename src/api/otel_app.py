"""Explicit OTLP-enabled FastAPI ASGI entrypoint for monitored deployments.

Use uvicorn src.api.otel_app:build_otel_app --factory for opt-in monitoring.
This entrypoint fails closed on missing collector configuration and owns SDK
shutdown through the existing application's lifespan.
"""

from __future__ import annotations

import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.app import (
    create_app,
    instrument_http_app,
    registered_route_templates,
)
from src.infrastructure.telemetry.runtime import (
    create_otlp_runtime,
)


def build_otel_app() -> FastAPI:
    """Build independently per Uvicorn worker; no SDK globals."""
    endpoint = os.environ.get("INTERVIEW_OTLP_ENDPOINT", "")
    if not endpoint:
        raise RuntimeError(
            "INTERVIEW_OTLP_ENDPOINT is required for the monitored app"
        )
    runtime = create_otlp_runtime(
        service_name="ai-engineer-interview-agent",
        collector_endpoint=endpoint,
        allow_insecure_local=(
            os.environ.get("INTERVIEW_ALLOW_LOCAL_OTLP_HTTP") == "true"
        ),
    )
    app = create_app()
    instrument_http_app(
        app,
        telemetry=runtime.http_server_telemetry(
            route_templates=registered_route_templates(app)
        ),
    )
    original_lifespan = app.router.lifespan_context

    @asynccontextmanager
    async def managed_lifespan(api: FastAPI) -> AsyncIterator[None]:
        try:
            async with original_lifespan(api):
                yield
        finally:
            runtime.shutdown()

    app.router.lifespan_context = managed_lifespan
    return app

