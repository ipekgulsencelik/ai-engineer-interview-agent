from __future__ import annotations

from pydantic import BaseModel
from pydantic import ConfigDict


class HealthCheckResponse(BaseModel):
    """
    Health check endpoint response schema.
    """

    status: str

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        json_schema_extra={
            "example": {
                "status": "ok",
            },
        },
    )