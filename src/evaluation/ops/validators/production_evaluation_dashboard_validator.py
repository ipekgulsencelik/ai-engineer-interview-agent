from __future__ import annotations

from datetime import datetime

from src.domain.validation.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.ops.constants.production_evaluation_dashboard import (
    DASHBOARD_DUPLICATE_METRIC_CARD_ID_ERROR,
    DASHBOARD_METRIC_CARD_TYPE_ERROR,
    DASHBOARD_METRIC_CARDS_TYPE_ERROR,
    DASHBOARD_TREND_POINT_ORDER_ERROR,
    DASHBOARD_TREND_POINT_TYPE_ERROR,
    DASHBOARD_TREND_POINTS_TYPE_ERROR,
)
from src.evaluation.ops.entities.dashboard_metric_card import (
    DashboardMetricCard,
)
from src.evaluation.ops.schemas.production_evaluation_dashboard_schema import (
    PRODUCTION_EVALUATION_DASHBOARD_SCHEMA,
)
from src.evaluation.ops.value_objects.dashboard_trend_point import (
    DashboardTrendPoint,
)


class ProductionEvaluationDashboardValidator:
    """
    ProductionEvaluationDashboard validation service.
    """

    @staticmethod
    def validate(
        *,
        dashboard_id: str,
        title: str,
        generated_at: datetime,
        metric_cards: tuple[
            DashboardMetricCard,
            ...,
        ],
        trend_points: tuple[
            DashboardTrendPoint,
            ...,
        ],
        notes: str | None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "dashboard_id": dashboard_id,
                "title": title,
                "generated_at": generated_at,
                "notes": notes,
            },
            schema=(
                PRODUCTION_EVALUATION_DASHBOARD_SCHEMA
            ),
            error_factory=(
                EvaluationValidationError
            ),
        )

        if not isinstance(
            metric_cards,
            tuple,
        ):
            raise EvaluationValidationError(
                DASHBOARD_METRIC_CARDS_TYPE_ERROR
            )

        if not isinstance(
            trend_points,
            tuple,
        ):
            raise EvaluationValidationError(
                DASHBOARD_TREND_POINTS_TYPE_ERROR
            )

        seen_card_ids: set[str] = set()

        for metric_card in metric_cards:
            if not isinstance(
                metric_card,
                DashboardMetricCard,
            ):
                raise EvaluationValidationError(
                    DASHBOARD_METRIC_CARD_TYPE_ERROR
                )

            if metric_card.card_id in seen_card_ids:
                raise EvaluationValidationError(
                    DASHBOARD_DUPLICATE_METRIC_CARD_ID_ERROR
                )

            seen_card_ids.add(
                metric_card.card_id,
            )

        previous_occurred_at: datetime | None = None

        for trend_point in trend_points:
            if not isinstance(
                trend_point,
                DashboardTrendPoint,
            ):
                raise EvaluationValidationError(
                    DASHBOARD_TREND_POINT_TYPE_ERROR
                )

            if (
                previous_occurred_at is not None
                and trend_point.occurred_at < previous_occurred_at
            ):
                raise EvaluationValidationError(
                    DASHBOARD_TREND_POINT_ORDER_ERROR
                )

            previous_occurred_at = (
                trend_point.occurred_at
            )