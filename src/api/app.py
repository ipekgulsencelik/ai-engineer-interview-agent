from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.routes.cv_routes import (
    router as cv_router,
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

    app.state.container = ServiceContainer()

    yield

    app.state.container = None


def create_app() -> FastAPI:
    app = FastAPI(
        title="AI Engineer Interview Agent",
        version="0.1.0",
        lifespan=lifespan,
    )

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

    return app


app = create_app()