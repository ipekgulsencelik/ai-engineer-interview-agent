from __future__ import annotations

from src.evaluation.ops.constants.dashboard_card_ids import (
    REGRESSION_STATUS_CARD_ID,
)
from src.evaluation.ops.constants.dashboard_card_labels import (
    REGRESSION_DETECTED_LABEL,
    REGRESSION_NOT_DETECTED_LABEL,
)
from src.evaluation.ops.constants.dashboard_card_sort_orders import (
    REGRESSION_SORT_ORDER,
)
from src.evaluation.ops.constants.dashboard_card_titles import (
    REGRESSION_TITLE,
)
from src.evaluation.ops.entities.dashboard_metric_card import (
    DashboardMetricCard,
)
from src.evaluation.ops.enums.dashboard_severity import (
    DashboardSeverity,
)


class RegressionDashboardMetricCardsBuilder:
    """
    Builds dashboard metric cards from regression results.
    """

    @staticmethod
    def build(
        *,
        regression_result,
    ) -> tuple[
        DashboardMetricCard,
        ...,
    ]:
        if regression_result is None:
            return ()

        return (
            DashboardMetricCard(
                card_id=REGRESSION_STATUS_CARD_ID,
                title=REGRESSION_TITLE,
                value=(
                    1.0
                    if regression_result.regression_detected
                    else 0.0
                ),
                formatted_value=(
                    REGRESSION_DETECTED_LABEL
                    if regression_result.regression_detected
                    else REGRESSION_NOT_DETECTED_LABEL
                ),
                unit=None,
                description=(
                    regression_result.interpretation
                ),
                severity=(
                    DashboardSeverity.CRITICAL
                    if regression_result.regression_detected
                    else DashboardSeverity.SUCCESS
                ),
                sort_order=REGRESSION_SORT_ORDER,
            ),
        )