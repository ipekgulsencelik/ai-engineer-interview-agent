from __future__ import annotations

from datetime import datetime

from src.evaluation.metrics.value_objects.benchmark_aggregate_result import (
    BenchmarkAggregateResult,
)
from src.evaluation.metrics.value_objects.trend_visualization_snapshot import (
    TrendVisualizationSnapshot,
)
from src.api.mappers.ci_policy_summary_response_mapper import (
    CIPolicySummaryResponseMapper,
)
from src.api.mappers.leaderboard_entry_response_mapper import (
    LeaderboardEntryResponseMapper,
)
from src.api.mappers.metric_card_response_mapper import (
    MetricCardResponseMapper,
)
from src.api.mappers.regression_summary_response_mapper import (
    RegressionSummaryResponseMapper,
)
from src.api.mappers.trend_point_response_mapper import (
    TrendPointResponseMapper,
)
from src.api.schemas.evaluation.evaluation_dashboard_response import (
    EvaluationDashboardResponse,
)
from src.evaluation.ops.value_objects.ci_benchmark_policy_result import (
    CIBenchmarkPolicyResult,
)
from src.evaluation.ops.value_objects.leaderboard_entry import (
    LeaderboardEntry,
)
from src.evaluation.ops.value_objects.regression_detection_result import (
    RegressionDetectionResult,
)


class EvaluationDashboardResponseMapper:
    """
    Dashboard response mapper.
    """

    @staticmethod
    def map(
        *,
        dashboard_id: str,
        aggregate_result: BenchmarkAggregateResult,
        trend_snapshot: TrendVisualizationSnapshot,
        leaderboard_entries: tuple[
            LeaderboardEntry,
            ...
        ] = (),
        regression_result: (
            RegressionDetectionResult
            | None
        ) = None,
        ci_policy_result: (
            CIBenchmarkPolicyResult
            | None
        ) = None,
    ) -> EvaluationDashboardResponse:
        return EvaluationDashboardResponse(
            dashboard_id=dashboard_id,
            benchmark_id=aggregate_result.benchmark_id,
            benchmark_name=aggregate_result.benchmark_name,
            benchmark_version=(
                aggregate_result.benchmark_version
            ),
            generated_at=datetime.utcnow(),
            overall_score=(
                aggregate_result.mean_score
            ),
            metric_cards=(
                MetricCardResponseMapper.map(
                    aggregate_result=aggregate_result,
                )
            ),
            trend_points=(
                TrendPointResponseMapper.map(
                    trend_snapshot=trend_snapshot,
                )
            ),
            leaderboard=(
                LeaderboardEntryResponseMapper.map(
                    leaderboard_entries=leaderboard_entries,
                )
            ),
            regression_summary=(
                None
                if regression_result is None
                else RegressionSummaryResponseMapper.map(
                    regression_result=regression_result,
                )
            ),
            ci_policy_summary=(
                None
                if ci_policy_result is None
                else CIPolicySummaryResponseMapper.map(
                    ci_policy_result=ci_policy_result,
                )
            ),
        )