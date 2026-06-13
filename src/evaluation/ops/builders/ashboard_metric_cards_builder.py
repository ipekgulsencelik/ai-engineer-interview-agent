from __future__ import annotations

from src.evaluation.ops.entities.dashboard_metric_card import (
    DashboardMetricCard,
)
from src.evaluation.ops.enums.dashboard_severity import (
    DashboardSeverity,
)


class DashboardMetricCardsBuilder:
    """
    Builds dashboard metric cards from evaluation results.
    """

    @staticmethod
    def build(
        *,
        aggregate_result,
        regression_result,
        ci_policy_result,
    ) -> tuple[
        DashboardMetricCard,
        ...,
    ]:
        cards: list[
            DashboardMetricCard
        ] = [
            DashboardMetricCard(
                card_id="overall_score",
                title="Overall Score",
                value=aggregate_result.overall_score,
                formatted_value=(
                    f"{aggregate_result.overall_score:.2f}"
                ),
                unit=None,
                description="Aggregated benchmark score.",
                severity=DashboardSeverity.SUCCESS,
                sort_order=0,
            ),
            DashboardMetricCard(
                card_id="sample_count",
                title="Sample Count",
                value=float(
                    aggregate_result.sample_count,
                ),
                formatted_value=str(
                    aggregate_result.sample_count,
                ),
                unit=None,
                description="Total evaluated samples.",
                severity=DashboardSeverity.INFO,
                sort_order=1,
            ),
        ]

        if regression_result is not None:
            cards.append(
                DashboardMetricCard(
                    card_id="regression_status",
                    title="Regression",
                    value=(
                        1.0
                        if regression_result.regression_detected
                        else 0.0
                    ),
                    formatted_value=(
                        "Detected"
                        if regression_result.regression_detected
                        else "Not detected"
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
                    sort_order=2,
                )
            )

        if ci_policy_result is not None:
            cards.append(
                DashboardMetricCard(
                    card_id="ci_policy",
                    title="CI Policy",
                    value=(
                        1.0
                        if ci_policy_result.deployment_allowed
                        else 0.0
                    ),
                    formatted_value=(
                        "Allowed"
                        if ci_policy_result.deployment_allowed
                        else "Blocked"
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
                    sort_order=3,
                )
            )

        return tuple(
            sorted(
                cards,
                key=lambda card: card.sort_order,
            )
        )