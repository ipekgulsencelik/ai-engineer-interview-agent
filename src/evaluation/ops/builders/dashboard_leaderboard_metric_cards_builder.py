from __future__ import annotations

from src.evaluation.ops.builders.ci_policy_metric_value_builder import (
    CIPolicyMetricValueBuilder,
)
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
from src.evaluation.ops.resolvers.ci_policy_dashboard_severity_resolver import (
    CIPolicyDashboardSeverityResolver,
)


class CIPolicyDashboardMetricCardsBuilder:
    """
    Builds dashboard metric cards from CI policy results.
    """

    def __init__(
        self,
        *,
        metric_value_builder: (
            CIPolicyMetricValueBuilder | None
        ) = None,
        severity_resolver: (
            CIPolicyDashboardSeverityResolver | None
        ) = None,
    ) -> None:
        self._metric_value_builder = (
            metric_value_builder
            or CIPolicyMetricValueBuilder()
        )

        self._severity_resolver = (
            severity_resolver
            or CIPolicyDashboardSeverityResolver()
        )

    def build(
        self,
        *,
        ci_policy_result,
    ) -> tuple[
        DashboardMetricCard,
        ...,
    ]:
        if ci_policy_result is None:
            return ()

        deployment_allowed = (
            ci_policy_result.deployment_allowed
        )

        return (
            DashboardMetricCard(
                card_id=CI_POLICY_CARD_ID,
                title=CI_POLICY_TITLE,
                value=self._metric_value_builder.build(
                    deployment_allowed=deployment_allowed,
                ),
                formatted_value=(
                    CI_ALLOWED_LABEL
                    if deployment_allowed
                    else CI_BLOCKED_LABEL
                ),
                unit=None,
                description=(
                    ci_policy_result.interpretation
                ),
                severity=self._severity_resolver.resolve(
                    deployment_allowed=deployment_allowed,
                ),
                sort_order=CI_POLICY_SORT_ORDER,
            ),
        )