from __future__ import annotations

from collections.abc import AsyncIterator, Callable
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.http_observability import HTTPRequestObservabilityMiddleware
from src.application.observability.http_server_telemetry import (
    HTTPServerTelemetryPort,
)

from src.api.routes.cv_routes import (
    router as cv_router,
)
from src.api.routes.evaluation_dashboard_router import (
    router as evaluation_dashboard_router,
)
from src.api.routes.evaluation_routes import (
    router as evaluation_router,
)
from src.api.routes.health_routes import (
    router as health_router,
)
from src.api.routes.interview_routes import (
    router as interview_router,
)
from src.api.routes.retrieval_routes import (
    router as retrieval_router,
)
from src.api.storage.interview_session_store import (
    InMemoryInterviewSessionStore,
)
from src.infrastructure.containers.service_container import (
    ServiceContainer,
)


@asynccontextmanager
async def lifespan(
    app: FastAPI,
) -> AsyncIterator[None]:
    """
    Application lifecycle management.
    """
    factory: Callable[[], ServiceContainer] = getattr(
        app.state, "container_factory", ServiceContainer
    )
    app.state.container = factory()
    app.state.interview_sessions = InMemoryInterviewSessionStore()
    yield
    app.state.container = None
    app.state.interview_sessions = None


def registered_route_templates(app: FastAPI) -> frozenset[str]:
    """Bounded route templates, never concrete incoming URL paths."""
    return frozenset(
        route.path
        for route in app.routes[:128]
        if isinstance(getattr(route, "path", None), str)
        and route.path.startswith("/")
    )


def instrument_http_app(
    app: FastAPI, *, telemetry: HTTPServerTelemetryPort
) -> None:
    """Add optional instrumentation before the application's first request."""
    app.add_middleware(
        HTTPRequestObservabilityMiddleware,
        routes=tuple(app.routes),
        telemetry=telemetry,
    )


def create_app(
    *,
    http_telemetry: HTTPServerTelemetryPort | None = None,
    container_factory: Callable[[], ServiceContainer] | None = None,
) -> FastAPI:
    app = FastAPI(
        title="AI Engineer Interview Agent",
        version="0.1.0",
        lifespan=lifespan,
    )
    if container_factory is not None:
        app.state.container_factory = container_factory

    app.include_router(
        health_router,
        prefix="/api/v1",
    )

    app.include_router(
        evaluation_router,
        prefix="/api/v1",
    )

    app.include_router(
        interview_router,
        prefix="/api/v1",
    )

    app.include_router(
        retrieval_router,
        prefix="/api/v1",
    )

    app.include_router(
        cv_router,
        prefix="/api/v1",
    )

    app.include_router(
        evaluation_dashboard_router,
        prefix="/api/v1",
    )

    if http_telemetry is not None:
        instrument_http_app(app, telemetry=http_telemetry)

    return app


app = create_app()