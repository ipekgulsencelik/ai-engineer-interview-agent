from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class RegressionSummaryResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    regression_detected: bool
    score_delta: float
    interpretation: str