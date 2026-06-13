from __future__ import annotations

from datetime import datetime, timezone

import pytest

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.ops.validators.dashboard_trend_point_validator import (
    DashboardTrendPointValidator,
)


def _valid_kwargs() -> dict[str, object]:
    return {
        "point_id": "point-1",
        "metric_name": "overall_score",
        "value": 0.91,
        "occurred_at": datetime(2026, 1, 1, tzinfo=timezone.utc),
        "unit": "%",
        "benchmark_id": "benchmark-1",
        "experiment_id": "experiment-1",
        "model_name": "gpt-5",
        "label": "release",
        "notes": "trend point notes",
    }


def test_dashboard_trend_point_validator_should_accept_valid_payload() -> None:
    DashboardTrendPointValidator.validate(**_valid_kwargs())


@pytest.mark.parametrize("field_name", ["point_id", "metric_name"])
def test_dashboard_trend_point_validator_should_reject_empty_required_strings(
    field_name: str,
) -> None:
    kwargs = _valid_kwargs()
    kwargs[field_name] = ""

    with pytest.raises(EvaluationValidationError):
        DashboardTrendPointValidator.validate(**kwargs)


def test_dashboard_trend_point_validator_should_reject_non_datetime_occurrence() -> (
    None
):
    kwargs = _valid_kwargs()
    kwargs["occurred_at"] = "2026-01-01T00:00:00Z"

    with pytest.raises(EvaluationValidationError, match="occurred_at"):
        DashboardTrendPointValidator.validate(**kwargs)


def test_dashboard_trend_point_validator_should_reject_boolean_value() -> None:
    kwargs = _valid_kwargs()
    kwargs["value"] = True

    with pytest.raises(EvaluationValidationError):
        DashboardTrendPointValidator.validate(**kwargs)
