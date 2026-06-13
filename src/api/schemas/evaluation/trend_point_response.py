from __future__ import annotations

from pydantic import BaseModel
from pydantic import ConfigDict


class TrendPointResponse(
    BaseModel,
):
    model_config = ConfigDict(
        frozen=True,
    )

    label: str

    score: float