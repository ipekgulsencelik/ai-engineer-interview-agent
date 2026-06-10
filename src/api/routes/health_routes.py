from __future__ import annotations

from fastapi import APIRouter

from src.api.constants.health import (
    HEALTH_STATUS_OK,
)
from src.api.schemas.health import (
    HealthCheckResponse,
)


router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get(
    "/",
    response_model=HealthCheckResponse,
    summary="Health check",
    description="Returns API liveness status.",
)
def health_check() -> HealthCheckResponse:
    """
    API liveness endpoint.
    """

    return HealthCheckResponse(
        status=HEALTH_STATUS_OK,
    )