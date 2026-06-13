from __future__ import annotations

from src.evaluation.metrics.value_objects.benchmark_aggregate_result import (
    BenchmarkAggregateResult,
)
from src.api.schemas.evaluation.metric_card_response import (
    MetricCardResponse,
)


class MetricCardResponseMapper:
    """
    Maps benchmark aggregate metrics to dashboard cards.
    """

    @staticmethod
    def map(
        *,
        aggregate_result: BenchmarkAggregateResult,
    ) -> list[MetricCardResponse]:
        return [
            MetricCardResponse(
                metric_name="Mean Score",
                metric_value=aggregate_result.mean_score,
                interpretation=aggregate_result.interpretation,
            ),
            MetricCardResponse(
                metric_name="Median Score",
                metric_value=aggregate_result.median_score,
                interpretation=aggregate_result.interpretation,
            ),
            MetricCardResponse(
                metric_name="Best Score",
                metric_value=aggregate_result.max_score,
                interpretation=aggregate_result.interpretation,
            ),
            MetricCardResponse(
                metric_name="Worst Score",
                metric_value=aggregate_result.min_score,
                interpretation=aggregate_result.interpretation,
            ),
        ]