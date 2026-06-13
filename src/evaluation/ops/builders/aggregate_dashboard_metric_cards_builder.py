from __future__ import annotations

from src.evaluation.ops.constants.dashboard_card_descriptions import (
    AGGREGATED_SCORE_DESCRIPTION,
    TOTAL_SAMPLES_DESCRIPTION,
)
from src.evaluation.ops.constants.dashboard_card_ids import (
    OVERALL_SCORE_CARD_ID,
    SAMPLE_COUNT_CARD_ID,
)
from src.evaluation.ops.constants.dashboard_card_sort_orders import (
    OVERALL_SCORE_SORT_ORDER,
    SAMPLE_COUNT_SORT_ORDER,
)
from src.evaluation.ops.constants.dashboard_card_titles import (
    OVERALL_SCORE_TITLE,
    SAMPLE_COUNT_TITLE,
)
from src.evaluation.ops.entities.dashboard_metric_card import (
    DashboardMetricCard,
)
from src.evaluation.ops.enums.dashboard_severity import (
    DashboardSeverity,
)


class AggregateDashboardMetricCardsBuilder:
    """
    Builds dashboard metric cards from aggregate benchmark results.
    """

    @staticmethod
    def build(
        *,
        aggregate_result,
    ) -> tuple[
        DashboardMetricCard,
        ...,
    ]:
        return (
            DashboardMetricCard(
                card_id=OVERALL_SCORE_CARD_ID,
                title=OVERALL_SCORE_TITLE,
                value=aggregate_result.overall_score,
                formatted_value=(
                    f"{aggregate_result.overall_score:.2f}"
                ),
                unit=None,
                description=(
                    AGGREGATED_SCORE_DESCRIPTION
                ),
                severity=(
                    DashboardSeverity.SUCCESS
                ),
                sort_order=(
                    OVERALL_SCORE_SORT_ORDER
                ),
            ),
            DashboardMetricCard(
                card_id=SAMPLE_COUNT_CARD_ID,
                title=SAMPLE_COUNT_TITLE,
                value=float(
                    aggregate_result.sample_count,
                ),
                formatted_value=str(
                    aggregate_result.sample_count,
                ),
                unit=None,
                description=(
                    TOTAL_SAMPLES_DESCRIPTION
                ),
                severity=(
                    DashboardSeverity.INFO
                ),
                sort_order=(
                    SAMPLE_COUNT_SORT_ORDER
                ),
            ),
        )