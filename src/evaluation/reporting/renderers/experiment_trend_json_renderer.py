from __future__ import annotations

from src.evaluation.reporting.utils.json_serialization_utils import (
    JSONSerializationUtils,
)
from src.evaluation.tracking.entities.experiment_trend_result import (
    ExperimentTrendResult,
)


class ExperimentTrendJSONRenderer:
    """
    Renders experiment trend results as JSON.
    """

    def __init__(
        self,
        *,
        utils: JSONSerializationUtils | None = None,
    ) -> None:
        self._utils = utils or JSONSerializationUtils()

    def render(
        self,
        *,
        trend: ExperimentTrendResult,
    ) -> str:
        return self._utils.to_json(
            payload={
                "experiment_id": trend.experiment_id,
                "experiment_name": trend.experiment_name,
                "experiment_version": trend.experiment_version,
                "run_count": trend.run_count,
                "first_run_id": trend.first_run_id,
                "latest_run_id": trend.latest_run_id,
                "first_overall_score": trend.first_overall_score,
                "latest_overall_score": trend.latest_overall_score,
                "average_overall_score": trend.average_overall_score,
                "overall_score_delta": trend.overall_score_delta,
                "first_pass_rate": trend.first_pass_rate,
                "latest_pass_rate": trend.latest_pass_rate,
                "pass_rate_delta": trend.pass_rate_delta,
                "best_run_id": trend.best_run_id,
                "best_overall_score": trend.best_overall_score,
                "worst_run_id": trend.worst_run_id,
                "worst_overall_score": trend.worst_overall_score,
                "trend_direction": str(trend.trend_direction),
                "interpretation": trend.interpretation,
                "notes": trend.notes,
            },
        )