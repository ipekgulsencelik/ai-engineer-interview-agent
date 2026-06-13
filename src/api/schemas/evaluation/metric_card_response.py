from __future__ import annotations

from pydantic import BaseModel
from pydantic import ConfigDict


class MetricCardResponse(
    BaseModel,
):
    model_config = ConfigDict(
        frozen=True,
    )

    title: str

    value: float

    interpretation: str