from __future__ import annotations

from fastapi import Request

from src.infrastructure.containers.service_container import (
    ServiceContainer,
)


def get_service_container(
    request: Request,
) -> ServiceContainer:
    """
    Resolve application ServiceContainer
    from FastAPI app state.
    """

    container = getattr(
        request.app.state,
        "container",
        None,
    )

    if not isinstance(
        container,
        ServiceContainer,
    ):
        raise RuntimeError(
            "ServiceContainer is not initialized."
        )

    return container