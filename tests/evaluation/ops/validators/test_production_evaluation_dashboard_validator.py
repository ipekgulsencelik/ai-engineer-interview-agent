from __future__ import annotations

from datetime import datetime, timezone

import pytest

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.ops.validators.production_evaluation_dashboard_validator import (
    ProductionEvaluationDashboardValidator,
)
from src.evaluation.ops.value_objects.dashboard_metric_card import DashboardMetricCard
from src.evaluation.ops.value_objects.dashboard_trend_point import DashboardTrendPoint


def _card(card_id: str = "score") -> DashboardMetricCard:
    return DashboardMetricCard(
        card_id=card_id,
        title="Score",
        value=0.91,
        formatted_value="91%",
    )


def _point(
    point_id: str = "point-1",
    occurred_at: datetime | None = None,
) -> DashboardTrendPoint:
    return DashboardTrendPoint(
        point_id=point_id,
        metric_name="overall_score",
        value=0.91,
        occurred_at=occurred_at or datetime(2026, 1, 1, tzinfo=timezone.utc),
    )


def _valid_kwargs() -> dict[str, object]:
    return {
        "dashboard_id": "dashboard-1",
        "title": "Production Evaluation",
        "generated_at": datetime(2026, 1, 3, tzinfo=timezone.utc),
        "metric_cards": (_card(),),
        "trend_points": (_point(),),
        "notes": "valid dashboard",
    }


def test_production_evaluation_dashboard_validator_should_accept_valid_payload() -> (
    None
):
    ProductionEvaluationDashboardValidator.validate(**_valid_kwargs())


def test_production_evaluation_dashboard_validator_should_reject_non_tuple_metric_cards() -> (
    None
):
    kwargs = _valid_kwargs()
    kwargs["metric_cards"] = [_card()]

    with pytest.raises(EvaluationValidationError, match="metric_cards must be tuple"):
        ProductionEvaluationDashboardValidator.validate(**kwargs)


def test_production_evaluation_dashboard_validator_should_reject_invalid_metric_card_item() -> (
    None
):
    kwargs = _valid_kwargs()
    kwargs["metric_cards"] = (object(),)

    with pytest.raises(EvaluationValidationError, match="DashboardMetricCard"):
        ProductionEvaluationDashboardValidator.validate(**kwargs)


def test_production_evaluation_dashboard_validator_should_reject_duplicate_metric_cards() -> (
    None
):
    kwargs = _valid_kwargs()
    kwargs["metric_cards"] = (_card("score"), _card("score"))

    with pytest.raises(EvaluationValidationError, match="duplicate"):
        ProductionEvaluationDashboardValidator.validate(**kwargs)


def test_production_evaluation_dashboard_validator_should_reject_non_tuple_trend_points() -> (
    None
):
    kwargs = _valid_kwargs()
    kwargs["trend_points"] = [_point()]

    with pytest.raises(EvaluationValidationError, match="trend_points must be tuple"):
        ProductionEvaluationDashboardValidator.validate(**kwargs)


def test_production_evaluation_dashboard_validator_should_reject_invalid_trend_point_item() -> (
    None
):
    kwargs = _valid_kwargs()
    kwargs["trend_points"] = (object(),)

    with pytest.raises(EvaluationValidationError, match="DashboardTrendPoint"):
        ProductionEvaluationDashboardValidator.validate(**kwargs)


def test_production_evaluation_dashboard_validator_should_reject_unordered_trend_points() -> (
    None
):
    kwargs = _valid_kwargs()
    kwargs["trend_points"] = (
        _point("newer", datetime(2026, 1, 2, tzinfo=timezone.utc)),
        _point("older", datetime(2026, 1, 1, tzinfo=timezone.utc)),
    )

    with pytest.raises(EvaluationValidationError, match="ordered"):
        ProductionEvaluationDashboardValidator.validate(**kwargs)
