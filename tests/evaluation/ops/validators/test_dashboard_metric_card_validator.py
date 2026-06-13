from __future__ import annotations

import pytest

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.ops.enums.dashboard_severity import DashboardSeverity
from src.evaluation.ops.validators.dashboard_metric_card_validator import (
    DashboardMetricCardValidator,
)


def _valid_kwargs() -> dict[str, object]:
    return {
        "card_id": "score",
        "title": "Overall Score",
        "value": 0.91,
        "formatted_value": "91%",
        "unit": "%",
        "description": "Production evaluation score",
        "trend_value": 0.03,
        "trend_label": "+3%",
        "is_positive_trend": True,
        "severity": DashboardSeverity.SUCCESS,
        "sort_order": 1,
    }


def test_dashboard_metric_card_validator_should_accept_valid_payload() -> None:
    DashboardMetricCardValidator.validate(**_valid_kwargs())


@pytest.mark.parametrize("field_name", ["card_id", "title", "formatted_value"])
def test_dashboard_metric_card_validator_should_reject_empty_required_strings(
    field_name: str,
) -> None:
    kwargs = _valid_kwargs()
    kwargs[field_name] = ""

    with pytest.raises(EvaluationValidationError):
        DashboardMetricCardValidator.validate(**kwargs)


@pytest.mark.parametrize("field_name", ["value", "trend_value", "sort_order"])
def test_dashboard_metric_card_validator_should_reject_boolean_numeric_fields(
    field_name: str,
) -> None:
    kwargs = _valid_kwargs()
    kwargs[field_name] = True

    with pytest.raises(EvaluationValidationError):
        DashboardMetricCardValidator.validate(**kwargs)


def test_dashboard_metric_card_validator_should_reject_trend_label_without_value() -> (
    None
):
    kwargs = _valid_kwargs()
    kwargs["trend_value"] = None
    kwargs["trend_label"] = "+3%"

    with pytest.raises(EvaluationValidationError, match="trend_label requires"):
        DashboardMetricCardValidator.validate(**kwargs)


def test_dashboard_metric_card_validator_should_reject_invalid_severity_type() -> None:
    kwargs = _valid_kwargs()
    kwargs["severity"] = "success"

    with pytest.raises(EvaluationValidationError, match="DashboardSeverity"):
        DashboardMetricCardValidator.validate(**kwargs)


def test_dashboard_metric_card_validator_should_reject_negative_sort_order() -> None:
    kwargs = _valid_kwargs()
    kwargs["sort_order"] = -1

    with pytest.raises(EvaluationValidationError):
        DashboardMetricCardValidator.validate(**kwargs)
