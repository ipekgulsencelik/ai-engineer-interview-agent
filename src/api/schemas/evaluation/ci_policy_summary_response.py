from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class CIPolicySummaryResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    passed: bool
    blocking_failure_count: int
    interpretation: str