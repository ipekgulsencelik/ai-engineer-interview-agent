from __future__ import annotations

import pytest

from src.evaluation.metrics.value_objects.correlation_result import (
    CorrelationResult,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)


def test_correlation_result_should_create_successfully() -> None:
    result = CorrelationResult(
        metric_x="human_score",
        metric_y="llm_score",
        correlation_coefficient=0.82,
        p_value=0.001,
        sample_count=100,
        method="pearson",
        is_significant=True,
        notes="Strong correlation detected.",
    )

    assert result.metric_x == "human_score"
    assert result.metric_y == "llm_score"
    assert result.correlation_coefficient == 0.82
    assert result.p_value == 0.001
    assert result.sample_count == 100
    assert result.method == "pearson"
    assert result.is_significant is True
    assert result.notes == (
        "Strong correlation detected."
    )


@pytest.mark.parametrize(
    "field_name",
    [
        "metric_x",
        "metric_y",
        "method",
    ],
)
def test_correlation_result_should_raise_for_empty_string_fields(
    field_name: str,
) -> None:
    kwargs = {
        "metric_x": "human_score",
        "metric_y": "llm_score",
        "correlation_coefficient": 0.82,
        "p_value": 0.001,
        "sample_count": 100,
        "method": "pearson",
        "is_significant": True,
        "notes": None,
    }

    kwargs[field_name] = ""

    with pytest.raises(
        EvaluationValidationError,
    ):
        CorrelationResult(
            **kwargs,
        )


@pytest.mark.parametrize(
    "coefficient",
    [
        -1.1,
        1.1,
    ],
)
def test_correlation_result_should_raise_for_invalid_correlation_coefficient(
    coefficient: float,
) -> None:
    with pytest.raises(
        EvaluationValidationError,
    ):
        CorrelationResult(
            metric_x="human_score",
            metric_y="llm_score",
            correlation_coefficient=coefficient,
            p_value=0.001,
            sample_count=100,
            method="pearson",
            is_significant=True,
        )


@pytest.mark.parametrize(
    "p_value",
    [
        -0.01,
        1.01,
    ],
)
def test_correlation_result_should_raise_for_invalid_p_value(
    p_value: float,
) -> None:
    with pytest.raises(
        EvaluationValidationError,
    ):
        CorrelationResult(
            metric_x="human_score",
            metric_y="llm_score",
            correlation_coefficient=0.82,
            p_value=p_value,
            sample_count=100,
            method="pearson",
            is_significant=True,
        )


def test_correlation_result_should_raise_for_invalid_sample_count() -> None:
    with pytest.raises(
        EvaluationValidationError,
    ):
        CorrelationResult(
            metric_x="human_score",
            metric_y="llm_score",
            correlation_coefficient=0.82,
            p_value=0.001,
            sample_count=0,
            method="pearson",
            is_significant=True,
        )


def test_correlation_result_should_raise_for_invalid_significance_type() -> None:
    with pytest.raises(
        EvaluationValidationError,
    ):
        CorrelationResult(
            metric_x="human_score",
            metric_y="llm_score",
            correlation_coefficient=0.82,
            p_value=0.001,
            sample_count=100,
            method="pearson",
            is_significant="yes",  # type: ignore[arg-type]
        )


def test_correlation_result_should_raise_for_invalid_notes_type() -> None:
    with pytest.raises(
        EvaluationValidationError,
    ):
        CorrelationResult(
            metric_x="human_score",
            metric_y="llm_score",
            correlation_coefficient=0.82,
            p_value=0.001,
            sample_count=100,
            method="pearson",
            is_significant=True,
            notes=123,  # type: ignore[arg-type]
        )


def test_correlation_result_should_be_immutable() -> None:
    result = CorrelationResult(
        metric_x="human_score",
        metric_y="llm_score",
        correlation_coefficient=0.82,
        p_value=0.001,
        sample_count=100,
        method="pearson",
        is_significant=True,
    )

    with pytest.raises(
        AttributeError,
    ):
        result.metric_x = "changed"  # type: ignore[misc]