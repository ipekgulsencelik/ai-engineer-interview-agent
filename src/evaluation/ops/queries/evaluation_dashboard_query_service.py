from __future__ import annotations

from src.evaluation.ops.builders.evaluation_dashboard_model_builder import (
    EvaluationDashboardModelBuilder,
)
from src.evaluation.ops.entities.production_evaluation_dashboard import (
    ProductionEvaluationDashboard,
)


class EvaluationDashboardQueryService:
    """
    Query service for evaluation dashboard read model.
    """

    def __init__(
        self,
        *,
        benchmark_aggregation_service,
        trend_visualization_service,
        leaderboard_service,
        regression_detection_service,
        ci_policy_service,
        dashboard_builder: EvaluationDashboardModelBuilder | None = None,
    ) -> None:
        self._benchmark_aggregation_service = (
            benchmark_aggregation_service
        )
        self._trend_visualization_service = (
            trend_visualization_service
        )
        self._leaderboard_service = (
            leaderboard_service
        )
        self._regression_detection_service = (
            regression_detection_service
        )
        self._ci_policy_service = (
            ci_policy_service
        )
        self._dashboard_builder = (
            dashboard_builder
            or EvaluationDashboardModelBuilder()
        )

    def get_dashboard(
        self,
        *,
        benchmark_id: str,
        benchmark_version: str,
    ) -> ProductionEvaluationDashboard:
        return self._dashboard_builder.build(
            dashboard_id=(
                f"{benchmark_id}:{benchmark_version}"
            ),
            aggregate_result=(
                self._benchmark_aggregation_service.get_aggregate_result(
                    benchmark_id=benchmark_id,
                    benchmark_version=benchmark_version,
                )
            ),
            trend_snapshot=(
                self._trend_visualization_service.get_trend_snapshot(
                    benchmark_id=benchmark_id,
                    benchmark_version=benchmark_version,
                )
            ),
            leaderboard_entries=(
                self._leaderboard_service.get_leaderboard(
                    benchmark_id=benchmark_id,
                    benchmark_version=benchmark_version,
                )
            ),
            regression_result=(
                self._regression_detection_service.get_latest_result(
                    benchmark_id=benchmark_id,
                    benchmark_version=benchmark_version,
                )
            ),
            ci_policy_result=(
                self._ci_policy_service.get_latest_result(
                    benchmark_id=benchmark_id,
                    benchmark_version=benchmark_version,
                )
            ),
        )