from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from src.api.schemas.evaluation.ci_policy_summary_response import (
    CIPolicySummaryResponse,
)
from src.api.schemas.evaluation.leaderboard_entry_response import (
    LeaderboardEntryResponse,
)
from src.api.schemas.evaluation.metric_card_response import (
    MetricCardResponse,
)
from src.api.schemas.evaluation.regression_summary_response import (
    RegressionSummaryResponse,
)
from src.api.schemas.evaluation.trend_point_response import (
    TrendPointResponse,
)


class EvaluationDashboardResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    dashboard_id: str

    benchmark_id: str
    benchmark_name: str
    benchmark_version: str

    generated_at: datetime

    overall_score: float

    metric_cards: list[MetricCardResponse]
    trend_points: list[TrendPointResponse]

    leaderboard: list[LeaderboardEntryResponse] = []

    regression_summary: RegressionSummaryResponse | None = None
    ci_policy_summary: CIPolicySummaryResponse | None = None