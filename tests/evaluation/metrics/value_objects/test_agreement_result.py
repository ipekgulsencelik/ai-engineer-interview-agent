from __future__ import annotations

import pytest

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.metrics.value_objects.agreement_result import (
    AgreementResult,
)


def test_agreement_result_should_create_successfully() -> None:
    result = AgreementResult(
        metric_name="overall_score",
        kappa_score=0.82,
        agreement_ratio=0.91,
        sample_count=100,
        evaluator_count=2,
        method="cohen_kappa",
        is_reliable=True,
        interpretation="very_strong",
        p_value=0.01,
        notes="test",
    )

    assert result.metric_name == "overall_score"
    assert result.kappa_score == 0.82
    assert result.agreement_ratio == 0.91
    assert result.sample_count == 100
    assert result.evaluator_count == 2


def test_agreement_result_should_be_immutable() -> None:
    result = AgreementResult(
        metric_name="overall_score",
        kappa_score=0.82,
        agreement_ratio=0.91,
        sample_count=100,
        evaluator_count=2,
        method="cohen_kappa",
        is_reliable=True,
        interpretation="very_strong",
    )

    with pytest.raises(
        AttributeError,
    ):
        result.metric_name = "changed"  # type: ignore[misc]


def test_agreement_result_should_raise_for_invalid_kappa() -> None:
    with pytest.raises(
        EvaluationValidationError,
    ):
        AgreementResult(
            metric_name="overall_score",
            kappa_score=2.0,
            agreement_ratio=0.91,
            sample_count=100,
            evaluator_count=2,
            method="cohen_kappa",
            is_reliable=True,
            interpretation="very_strong",
        )