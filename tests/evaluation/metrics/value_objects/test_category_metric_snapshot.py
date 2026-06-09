from __future__ import annotations

import pytest

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.metrics.value_objects.category_metric_snapshot import (
    CategoryMetricSnapshot,
)
from tests.evaluation.metrics.factories import (
    agreement_result,
    correlation_result,
    regression_result,
)


def _snapshot(**overrides: object) -> CategoryMetricSnapshot:
    values = {
        "category": "RAG",
        "average_human_score": 3.0,
        "average_llm_score": 4.0,
        "correlation_result": correlation_result(),
        "agreement_result": agreement_result(),
        "regression_result": regression_result(),
        "overall_alignment_score": 0.80,
        "interpretation": "strong_alignment",
        "notes": "snapshot",
    }
    values.update(overrides)
    return CategoryMetricSnapshot(**values)  # type: ignore[arg-type]


def test_category_metric_snapshot_should_expose_metric_properties() -> None:
    snapshot = _snapshot()

    assert snapshot.sample_count == 4
    assert snapshot.score_delta == pytest.approx(1.0)
    assert snapshot.absolute_score_delta == pytest.approx(1.0)
    assert snapshot.pearson_correlation == pytest.approx(0.90)
    assert snapshot.kappa_score == pytest.approx(0.80)
    assert snapshot.agreement_ratio == pytest.approx(0.80)
    assert snapshot.mae == pytest.approx(0.10)
    assert snapshot.mse == pytest.approx(0.01)
    assert snapshot.rmse == pytest.approx(0.10)
    assert snapshot.r2_score == pytest.approx(0.70)
    assert snapshot.has_positive_bias is True
    assert snapshot.has_negative_bias is False
    assert snapshot.is_neutral_bias is False


def test_category_metric_snapshot_should_detect_negative_and_neutral_bias() -> None:
    negative_snapshot = _snapshot(
        average_human_score=4.0,
        average_llm_score=3.0,
    )
    neutral_snapshot = _snapshot(
        average_human_score=4.0,
        average_llm_score=4.0,
    )

    assert negative_snapshot.has_negative_bias is True
    assert negative_snapshot.has_positive_bias is False
    assert negative_snapshot.is_neutral_bias is False
    assert neutral_snapshot.is_neutral_bias is True


@pytest.mark.parametrize(
    "field_name",
    [
        "category",
        "interpretation",
    ],
)
def test_category_metric_snapshot_should_raise_for_empty_string_fields(
    field_name: str,
) -> None:
    with pytest.raises(EvaluationValidationError):
        _snapshot(**{field_name: ""})


def test_category_metric_snapshot_should_raise_for_invalid_metric_result_type() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="correlation_result must be CorrelationResult",
    ):
        _snapshot(correlation_result=object())


def test_category_metric_snapshot_should_be_immutable() -> None:
    snapshot = _snapshot()

    with pytest.raises(AttributeError):
        snapshot.category = "changed"  # type: ignore[misc]
