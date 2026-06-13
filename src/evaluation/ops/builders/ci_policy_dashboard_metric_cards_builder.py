from __future__ import annotations

from src.evaluation.ops.constants.dashboard_card_ids import (
    CI_POLICY_CARD_ID,
)
from src.evaluation.ops.constants.dashboard_card_labels import (
    CI_ALLOWED_LABEL,
    CI_BLOCKED_LABEL,
)
from src.evaluation.ops.constants.dashboard_card_sort_orders import (
    CI_POLICY_SORT_ORDER,
)
from src.evaluation.ops.constants.dashboard_card_titles import (
    CI_POLICY_TITLE,
)
from src.evaluation.ops.entities.dashboard_metric_card import (
    DashboardMetricCard,
)
from src.evaluation.ops.enums.dashboard_severity import (
    DashboardSeverity,
)


class CIPolicyDashboardMetricCardsBuilder:
    """
    Builds dashboard metric cards from CI policy results.
    """

    @staticmethod
    def build(
        *,
        ci_policy_result,
    ) -> tuple[
        DashboardMetricCard,
        ...,
    ]:
        if ci_policy_result is None:
            return ()

        return (
            DashboardMetricCard(
                card_id=CI_POLICY_CARD_ID,
                title=CI_POLICY_TITLE,
                value=(
                    1.0
                    if ci_policy_result.deployment_allowed
                    else 0.0
                ),
                formatted_value=(
                    CI_ALLOWED_LABEL
                    if ci_policy_result.deployment_allowed
                    else CI_BLOCKED_LABEL
                ),
                unit=None,
                description=(
                    ci_policy_result.interpretation
                ),
                severity=(
                    DashboardSeverity.SUCCESS
                    if ci_policy_result.deployment_allowed
                    else DashboardSeverity.CRITICAL
                ),
                sort_order=CI_POLICY_SORT_ORDER,
            ),
        )