from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class LeaderboardEntryResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    rank: int
    model_name: str
    overall_score: float